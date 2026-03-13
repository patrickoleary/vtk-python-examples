#!/usr/bin/env python
"""
Test harness for VTK Python examples.

Reads test_manifest.json and runs examples offscreen, capturing screenshots.

Usage:
    # Default: run all categories in separate subprocesses (safest)
    python test_examples.py

    # Run a single category
    python test_examples.py --category GeometricObjects

    # Run a single example
    python test_examples.py --example GeometricObjects/Sphere

    # List available categories
    python test_examples.py --list-categories

    # List examples in a category
    python test_examples.py --list-examples GeometricObjects

When invoked by pytest (e.g. pytest test_examples.py -k "test_Filtering_"),
the test class is generated automatically from the manifest.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import types
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = Path(__file__).resolve().parent / "test_manifest.json"
OUTPUT_DIR = PROJECT_ROOT / "data" / "images" / "testing"

# ---------------------------------------------------------------------------
# Force offscreen rendering before any VTK imports
# ---------------------------------------------------------------------------
os.environ["VTK_DEFAULT_RENDER_WINDOW_OFFSCREEN"] = "1"

import vtkmodules.vtkInteractionStyle  # noqa: F401, E402
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401, E402
from vtkmodules.vtkIOImage import vtkPNGWriter  # noqa: E402
from vtkmodules.vtkRenderingCore import (  # noqa: E402
    vtkRenderWindowInteractor,
    vtkWindowToImageFilter,
)


# ═══════════════════════════════════════════════════════════════════════════
# VTK test utilities (previously vtk_test_utils.py)
# ═══════════════════════════════════════════════════════════════════════════

class _NonBlockingInteractor(vtkRenderWindowInteractor):
    """A vtkRenderWindowInteractor subclass that skips Initialize and Start."""

    def Initialize(self):
        pass

    def Start(self):
        pass


def _make_patched_rendering_core():
    """Create a fake vtkmodules.vtkRenderingCore module with the non-blocking interactor."""
    import vtkmodules.vtkRenderingCore as real_module

    fake = types.ModuleType("vtkmodules.vtkRenderingCore")
    for attr in dir(real_module):
        setattr(fake, attr, getattr(real_module, attr))
    fake.vtkRenderWindowInteractor = _NonBlockingInteractor
    return fake


def run_example_offscreen(script_path):
    """Execute an example script offscreen with a non-blocking interactor.

    Returns the script's global namespace dict after execution.
    """
    fake_module = _make_patched_rendering_core()

    original = sys.modules.get("vtkmodules.vtkRenderingCore")
    sys.modules["vtkmodules.vtkRenderingCore"] = fake_module

    # Patch sys.exit so examples that call sys.exit() don't kill the test
    original_exit = sys.exit
    sys.exit = lambda *args: None

    # Patch QApplication.exec so PyQt examples don't block on the event loop
    _qapp_exec_patched = False
    _original_qapp_exec = None
    try:
        from PyQt6.QtWidgets import QApplication as _QApp

        _original_qapp_exec = _QApp.exec
        _QApp.exec = lambda self=None: 0
        _qapp_exec_patched = True
    except ImportError:
        pass

    try:
        source = script_path.read_text()
        # Strip .Initialize() and .Start() calls so that interactors
        # created internally by C++ view classes (e.g. vtkGraphLayoutView)
        # do not block.  The module-swap above handles examples that
        # construct vtkRenderWindowInteractor explicitly, but view classes
        # create their own C++ interactor instances that cannot be
        # monkey-patched at the class level.
        source = re.sub(r"^[^\n#]*\.Initialize\(\)\s*$", "pass", source, flags=re.MULTILINE)
        source = re.sub(r"^[^\n#]*\.Start\(\)\s*$", "pass", source, flags=re.MULTILINE)
        namespace = {"__file__": str(script_path), "__name__": "__main__"}
        exec(compile(source, str(script_path), "exec"), namespace)
    finally:
        sys.exit = original_exit
        if _qapp_exec_patched:
            _QApp.exec = _original_qapp_exec
        if original is not None:
            sys.modules["vtkmodules.vtkRenderingCore"] = original
        else:
            sys.modules.pop("vtkmodules.vtkRenderingCore", None)

    return namespace


def capture_image(render_window, output_path):
    """Render the window and save a PNG screenshot."""
    render_window.Render()

    window_to_image = vtkWindowToImageFilter()
    window_to_image.SetInput(render_window)
    window_to_image.Update()

    writer = vtkPNGWriter()
    writer.SetFileName(str(output_path))
    writer.SetInputConnection(window_to_image.GetOutputPort())
    writer.Write()


# ═══════════════════════════════════════════════════════════════════════════
# Manifest helpers
# ═══════════════════════════════════════════════════════════════════════════

def load_manifest():
    """Load test cases from the JSON manifest."""
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def get_categories(manifest):
    """Return sorted list of unique categories."""
    return sorted(set(e["category"] for e in manifest))


# ═══════════════════════════════════════════════════════════════════════════
# Single-example runner (in-process)
# ═══════════════════════════════════════════════════════════════════════════

def run_single(entry):
    """Run one example and capture its screenshot. Returns True on success."""
    cat, title = entry["category"], entry["title"]

    if entry.get("skip", False):
        print(f"  SKIP  {cat}/{title} (marked skip in manifest)")
        return True

    script_path = PROJECT_ROOT / entry["script_path"]
    if not script_path.exists():
        print(f"  FAIL  {cat}/{title} — script not found: {script_path}")
        return False

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_image = OUTPUT_DIR / entry["output_image"]

    t0 = time.monotonic()
    try:
        namespace = run_example_offscreen(script_path)

        render_window_var = entry.get("render_window_var", "render_window")
        render_window = namespace.get(render_window_var)
        if render_window is None:
            print(f"  FAIL  {cat}/{title} — '{render_window_var}' not in namespace")
            return False

        capture_image(render_window, output_image)

        if not output_image.exists() or output_image.stat().st_size == 0:
            print(f"  FAIL  {cat}/{title} — image not saved or empty")
            return False

    except Exception as exc:
        elapsed = time.monotonic() - t0
        print(f"  FAIL  {cat}/{title} — {exc} ({elapsed:.1f}s)")
        return False

    elapsed = time.monotonic() - t0
    print(f"  OK    {cat}/{title} ({elapsed:.1f}s)")
    return True


# ═══════════════════════════════════════════════════════════════════════════
# Category batch runner (subprocesses via pytest)
# ═══════════════════════════════════════════════════════════════════════════

def run_category_batch(categories, manifest):
    """Run categories in separate subprocesses using pytest -k."""
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    failed_categories = []
    start = time.monotonic()

    for i, cat in enumerate(categories, 1):
        count = sum(1 for e in manifest if e["category"] == cat)
        sys.stdout.write(f"[{i}/{len(categories)}] {cat} ({count} tests) ... ")
        sys.stdout.flush()

        t0 = time.monotonic()
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "src/tests/test_examples.py",
                "-s", "--tb=line", "-q",
                "-k", f"test_{cat}_",
            ],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        elapsed = time.monotonic() - t0

        last_line = result.stdout.strip().split("\n")[-1] if result.stdout.strip() else ""
        if result.returncode == 0:
            sys.stdout.write(f"OK  {elapsed:.1f}s  {last_line}\n")
            if "passed" in last_line:
                m = re.search(r"(\d+) passed", last_line)
                if m:
                    total_passed += int(m.group(1))
                m = re.search(r"(\d+) skipped", last_line)
                if m:
                    total_skipped += int(m.group(1))
        else:
            sys.stdout.write(f"FAIL  {elapsed:.1f}s\n")
            failed_categories.append(cat)
            for line in result.stdout.split("\n"):
                if "FAILED" in line or "ERROR" in line:
                    print(f"    {line.strip()}")
            total_failed += 1

        sys.stdout.flush()

    total_time = time.monotonic() - start
    print(f"\n{'=' * 60}")
    print(f"Total: {total_passed} passed, {total_skipped} skipped, "
          f"{total_failed} failed categories in {total_time:.0f}s")
    if failed_categories:
        print(f"Failed: {', '.join(failed_categories)}")
        return 1
    return 0


# ═══════════════════════════════════════════════════════════════════════════
# pytest test class (auto-generated from manifest)
# ═══════════════════════════════════════════════════════════════════════════

_manifest_data = load_manifest()
_total_tests = len(_manifest_data)
_test_counter = 0
_suite_start = None


def _make_test(entry):
    """Create a test method for a single manifest entry."""

    def test_method(self):
        global _test_counter, _suite_start
        _test_counter += 1
        if _suite_start is None:
            _suite_start = time.monotonic()
        t0 = time.monotonic()
        cat, title = entry["category"], entry["title"]
        sys.stdout.write(f"[{_test_counter}/{_total_tests}] {cat}/{title} ... ")
        sys.stdout.flush()

        script_path = PROJECT_ROOT / entry["script_path"]
        self.assertTrue(script_path.exists(), f"Example not found: {script_path}")

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_image = OUTPUT_DIR / entry["output_image"]

        namespace = run_example_offscreen(script_path)

        render_window_var = entry.get("render_window_var", "render_window")
        render_window = namespace.get(render_window_var)
        self.assertIsNotNone(
            render_window,
            f"'{render_window_var}' not found in {entry['title']} namespace",
        )

        capture_image(render_window, output_image)
        self.assertTrue(output_image.exists(), f"Image was not saved: {output_image}")
        self.assertGreater(output_image.stat().st_size, 0, "Saved image is empty")

        elapsed = time.monotonic() - t0
        total = time.monotonic() - _suite_start
        sys.stdout.write(f"{elapsed:.1f}s (total {total:.0f}s)\n")
        sys.stdout.flush()

    test_method.__doc__ = f"Test {entry['category']}/{entry['title']}"
    return test_method


class TestExamples(unittest.TestCase):
    pass


for _entry in _manifest_data:
    _test_name = f"test_{_entry['category']}_{_entry['title']}"
    if _entry.get("skip", False):
        _test_func = unittest.skip("Marked as skip in manifest")(_make_test(_entry))
    else:
        _test_func = _make_test(_entry)
    setattr(TestExamples, _test_name, _test_func)


# ═══════════════════════════════════════════════════════════════════════════
# CLI entry point
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Test VTK Python examples.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  python test_examples.py                          # all categories in batches
  python test_examples.py -c GeometricObjects      # one category (in-process)
  python test_examples.py -e GeometricObjects/Cone # one example
  python test_examples.py --list-categories        # list categories
  python test_examples.py --list-examples Filtering # list examples in category
""",
    )
    parser.add_argument(
        "--category", "-c",
        help="Run all examples in this category (in-process).",
    )
    parser.add_argument(
        "--example", "-e",
        help="Run a single example as Category/Title (e.g. Filtering/AppendFilter).",
    )
    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="Force batch mode (subprocess per category). This is the default with no args.",
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List all available categories and exit.",
    )
    parser.add_argument(
        "--list-examples",
        metavar="CATEGORY",
        help="List all examples in a category and exit.",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    categories = get_categories(manifest)

    # --list-categories
    if args.list_categories:
        print(f"{len(categories)} categories:\n")
        for cat in categories:
            count = sum(1 for e in manifest if e["category"] == cat)
            skip = sum(1 for e in manifest if e["category"] == cat and e.get("skip"))
            extra = f" ({skip} skipped)" if skip else ""
            print(f"  {cat:30s} {count:4d} examples{extra}")
        return

    # --list-examples CATEGORY
    if args.list_examples:
        cat = args.list_examples
        entries = [e for e in manifest if e["category"] == cat]
        if not entries:
            print(f"Unknown category '{cat}'. Use --list-categories to see options.")
            sys.exit(1)
        print(f"{cat}: {len(entries)} examples\n")
        for e in entries:
            skip = " [SKIP]" if e.get("skip") else ""
            print(f"  {e['title']}{skip}")
        return

    # --example Category/Title
    if args.example:
        parts = args.example.split("/")
        if len(parts) != 2:
            print("Use Category/Title format, e.g. Filtering/AppendFilter")
            sys.exit(1)
        cat, title = parts
        entry = next(
            (e for e in manifest if e["category"] == cat and e["title"] == title),
            None,
        )
        if entry is None:
            print(f"Example '{cat}/{title}' not found in manifest.")
            sys.exit(1)
        ok = run_single(entry)
        sys.exit(0 if ok else 1)

    # --category CATEGORY (in-process, all examples in the category)
    if args.category:
        cat = args.category
        entries = [e for e in manifest if e["category"] == cat]
        if not entries:
            print(f"Unknown category '{cat}'. Use --list-categories to see options.")
            sys.exit(1)
        print(f"Running {len(entries)} examples in {cat}:\n")
        passed = failed = skipped = 0
        start = time.monotonic()
        for entry in entries:
            if entry.get("skip", False):
                print(f"  SKIP  {entry['title']}")
                skipped += 1
                continue
            ok = run_single(entry)
            if ok:
                passed += 1
            else:
                failed += 1
        elapsed = time.monotonic() - start
        print(f"\n{cat}: {passed} passed, {skipped} skipped, {failed} failed in {elapsed:.0f}s")
        sys.exit(1 if failed else 0)

    # Default: batch mode — all categories in subprocesses
    print(f"Running {len(manifest)} examples across {len(categories)} categories (batch mode):\n")
    rc = run_category_batch(categories, manifest)
    sys.exit(rc)


if __name__ == "__main__":
    main()
