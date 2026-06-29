#!/usr/bin/env python3
"""Generate data/data.jsonl from docs/public/examples/*.json sidecars.

Each JSONL record combines metadata from the .json file with source code from
the corresponding .py file. This `data.jsonl` is the corpus artifact published
(via GitHub release) for the vtk-ontology parser to consume.

Usage:
    python scripts/data/generate_data.py                    # dry-run, first file only
    python scripts/data/generate_data.py --all              # dry-run, all files
    python scripts/data/generate_data.py --write            # write to data/data.jsonl
    python scripts/data/generate_data.py --write --all      # write all files
    python scripts/data/generate_data.py --tag annotation   # process specific tag
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXAMPLES_DIR = ROOT / "docs" / "public" / "examples"
OUTPUT_PATH = ROOT / "data" / "data.jsonl"

# Pattern to match VTK class names that are actually used:
# - Constructor calls: vtkClassName(...)
# - Method access: vtkClassName.method(...)
# - Variable assignments: var = vtkClassName(...)
_VTK_CLASS_PATTERN = re.compile(r"\b(vtk[A-Z][a-zA-Z0-9_]*)\s*[\(\.]")


def extract_vtk_classes_from_code(code: str) -> set[str]:
    """Extract all VTK class names from Python code that are actually used."""
    return set(_VTK_CLASS_PATTERN.findall(code))


def build_record(json_path: Path, tag: str, fix: bool = False) -> dict | None:
    """Build a dataset record from a JSON sidecar and its .py file.

    Returns None if the .py file is missing or JSON is invalid.
    """
    try:
        with open(json_path) as f:
            meta = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ERROR: Could not read {json_path}: {e}")
        return None

    if not isinstance(meta, dict):
        print(f"  ERROR: {json_path} is not a dict")
        return None

    py_filename = meta.get("py_filename", json_path.stem + ".py")
    py_path = json_path.parent / py_filename

    if not py_path.exists():
        print(f"  ERROR: Missing .py file: {py_path}")
        return None

    try:
        code = py_path.read_text(encoding="utf-8")
    except IOError as e:
        print(f"  ERROR: Could not read {py_path}: {e}")
        return None

    # Validate uses_symbols against actual code
    actual_classes = extract_vtk_classes_from_code(code)
    declared_classes = set(meta.get("uses_symbols", []))

    if actual_classes != declared_classes:
        missing = actual_classes - declared_classes
        extra = declared_classes - actual_classes
        if missing or extra:
            if fix:
                print(f"  FIXING: {json_path.name} uses_symbols:")
                if missing:
                    print(f"    Adding: {sorted(missing)}")
                if extra:
                    print(f"    Removing: {sorted(extra)}")
                # Use corrected classes
                uses_symbols = sorted(actual_classes)
            else:
                print(f"  WARNING: {json_path.name} uses_symbols mismatch:")
                if missing:
                    print(f"    Missing in uses_symbols: {sorted(missing)}")
                if extra:
                    print(f"    Extra in uses_symbols: {sorted(extra)}")
                uses_symbols = meta.get("uses_symbols", [])
    else:
        uses_symbols = meta.get("uses_symbols", [])

    record = {
        "id": f"https://github.com/Kitware/vtk-ontology/examples/{tag}/{py_filename}",
        "title": meta.get("title", json_path.stem),
        "source_type": meta.get("source_type", "examples"),
        "tag": tag,
        "language": "Python",
        "py_filename": py_filename,
        "image": meta.get("image", f"{json_path.stem}.png"),
        "metadata_filename": json_path.name,
        "explanation": meta.get("explanation", ""),
        "code": code,
        "uses_symbols": uses_symbols,
        "data_files": meta.get("data_files", []),
        "topology": meta.get("topology", "standard"),
    }

    return record


def main():
    parser = argparse.ArgumentParser(description="Generate data.jsonl from example sidecars")
    parser.add_argument("--all", action="store_true", help="Process all files (not just first)")
    parser.add_argument("--write", action="store_true", help="Write to data/data.jsonl")
    parser.add_argument("--tag", help="Process only a specific tag (e.g., annotation)")
    parser.add_argument("--file", help="Process a specific JSON file (relative to docs/public/examples/)")
    parser.add_argument("--fix", action="store_true", help="Auto-correct uses_symbols to match actual code")
    args = parser.parse_args()

    records = []
    total_json_files = 0

    # Handle --file option: process a specific file
    if args.file:
        json_path = EXAMPLES_DIR / args.file
        if not json_path.exists():
            print(f"ERROR: File not found: {json_path}")
            return
        tag = json_path.parent.name
        record = build_record(json_path, tag, fix=args.fix)
        if record:
            records.append(record)
            total_json_files = 1
    else:
        # Default: iterate through all tag directories
        for tag_dir in sorted(EXAMPLES_DIR.iterdir()):
            if not tag_dir.is_dir() or tag_dir.name.startswith("."):
                continue

            tag = tag_dir.name

            # Skip the data/ directory as requested
            if tag == "data":
                continue

            if args.tag and tag != args.tag:
                continue

            for json_path in sorted(tag_dir.glob("*.json")):
                total_json_files += 1
                record = build_record(json_path, tag, fix=args.fix)
                if record:
                    records.append(record)

                # Stop after first file unless --all is specified
                if not args.all:
                    break

            if not args.all and records:
                break

    print(f"Found {total_json_files} JSON files, built {len(records)} records")

    if args.write:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"Wrote {len(records)} records to {OUTPUT_PATH}")
    else:
        print("DRY RUN (use --write to output to file)")
        if records:
            print("\nFirst record:")
            print(json.dumps(records[0], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
