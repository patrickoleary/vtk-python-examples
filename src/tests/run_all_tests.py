#!/usr/bin/env python
"""Run all example tests by category, each in a fresh subprocess."""

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

MANIFEST = Path(__file__).parent / "test_manifest.json"


def main():
    parser = argparse.ArgumentParser(description="Run example tests by category.")
    parser.add_argument(
        "--category", "-c",
        help="Run only this category (case-sensitive). Omit to run all.",
    )
    args = parser.parse_args()

    with open(MANIFEST) as f:
        manifest = json.load(f)

    all_categories = sorted(set(e["category"] for e in manifest))
    if args.category:
        if args.category not in all_categories:
            print(f"Unknown category '{args.category}'. Available: {', '.join(all_categories)}")
            sys.exit(1)
        categories = [args.category]
    else:
        categories = all_categories
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
            cwd=Path(__file__).parent.parent.parent,
        )
        elapsed = time.monotonic() - t0

        # Parse pass/fail from last line
        last_line = result.stdout.strip().split("\n")[-1] if result.stdout.strip() else ""
        if result.returncode == 0:
            sys.stdout.write(f"OK  {elapsed:.1f}s  {last_line}\n")
            # Extract counts
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
            # Show failure output
            for line in result.stdout.split("\n"):
                if "FAILED" in line or "ERROR" in line:
                    print(f"    {line.strip()}")
            total_failed += 1

        sys.stdout.flush()

    total_time = time.monotonic() - start
    print(f"\n{'='*60}")
    print(f"Total: {total_passed} passed, {total_skipped} skipped, "
          f"{total_failed} failed categories in {total_time:.0f}s")
    if failed_categories:
        print(f"Failed: {', '.join(failed_categories)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
