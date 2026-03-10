"""
Generic parameterized test for VTK Python examples.

Reads test_manifest.json and runs each example offscreen,
capturing a screenshot and verifying the output image.
"""

import json
import sys
import time
import unittest
from pathlib import Path

from vtk_test_utils import capture_image, run_example_offscreen

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = Path(__file__).resolve().parent / "test_manifest.json"
OUTPUT_DIR = PROJECT_ROOT / "data" / "images" / "testing"


def load_manifest():
    """Load test cases from the JSON manifest."""
    with open(MANIFEST_PATH) as f:
        return json.load(f)


_total_tests = len(load_manifest())
_test_counter = 0
_suite_start = None


def make_test(entry):
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

        # Run the example offscreen
        namespace = run_example_offscreen(script_path)

        # Grab the render window from the script's namespace
        render_window_var = entry.get("render_window_var", "render_window")
        render_window = namespace.get(render_window_var)
        self.assertIsNotNone(
            render_window,
            f"'{render_window_var}' not found in {entry['title']} namespace",
        )

        # Capture the image
        capture_image(render_window, output_image)

        self.assertTrue(output_image.exists(), f"Image was not saved: {output_image}")
        self.assertGreater(output_image.stat().st_size, 0, "Saved image is empty")

        elapsed = time.monotonic() - t0
        total = time.monotonic() - _suite_start
        sys.stdout.write(f"{elapsed:.1f}s (total {total:.0f}s)\n")
        sys.stdout.flush()

    test_method.__doc__ = f"Test {entry['category']}/{entry['title']}"
    return test_method


# Dynamically generate test methods from the manifest
class TestExamples(unittest.TestCase):
    pass


for _entry in load_manifest():
    _test_name = f"test_{_entry['category']}_{_entry['title']}"
    if _entry.get("skip", False):
        _test_func = unittest.skip("Marked as skip in manifest")(make_test(_entry))
    else:
        _test_func = make_test(_entry)
    setattr(TestExamples, _test_name, _test_func)


if __name__ == "__main__":
    unittest.main()
