"""Generate data/tests/test_manifest.json from data/examples/{tag}/*.json sidecars.

Usage:
    uv run python tests/generate_data_manifest.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT / "docs" / "public" / "examples"
MANIFEST_PATH = ROOT / "tests" / "test_manifest.json"

# Add titles here as problems are discovered during testing
SKIP_TITLES: list[str] = []


def detect_render_window_var(script_path: Path) -> str:
    """Detect the render window variable name from the script source."""
    code = script_path.read_text()
    m = re.search(r"(\w+)\s*=\s*vtkRenderWindow\(\)", code)
    if m:
        return m.group(1)
    m = re.search(r"(\w+)\.AddRenderer\(", code)
    if m:
        return m.group(1)
    return "render_window"


def main():
    manifest = []

    for tag_dir in sorted(EXAMPLES_DIR.iterdir()):
        if not tag_dir.is_dir() or tag_dir.name.startswith("."):
            continue
        tag = tag_dir.name

        for json_path in sorted(tag_dir.glob("*.json")):
            with open(json_path) as f:
                meta = json.load(f)

            if not isinstance(meta, dict):
                continue

            py_filename = meta.get("py_filename", json_path.stem + ".py")
            script_path = tag_dir / py_filename

            if not script_path.exists():
                continue

            title = meta.get("title", json_path.stem)
            render_window_var = detect_render_window_var(script_path)
            skip = title in SKIP_TITLES

            manifest.append({
                "tag": tag,
                "title": title,
                "script_path": str(script_path.relative_to(ROOT)),
                "render_window_var": render_window_var,
                "output_image": f"{tag}_{json_path.stem}.png",
                "skip": skip,
            })

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    total = len(manifest)
    skipped = sum(1 for e in manifest if e["skip"])
    print(f"Generated {total} manifest entries ({total - skipped} runnable, {skipped} skipped)")
    print(f"  → {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
