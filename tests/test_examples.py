"""Run VTK examples one at a time, compare screenshots, write a report.

Usage:
    uv run python tests/test_examples.py
    uv run python tests/test_examples.py --tag annotation
    uv run python tests/test_examples.py --name axis_actor2d
"""

import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "tests" / "test_manifest.json"
IMAGES = ROOT / "tests" / "images"
HELPER = ROOT / "tests" / "_run_example.py"
DATA_DIR = ROOT / "docs" / "public" / "examples" / "data"
REPORT = ROOT / "tests" / "results.csv"

SSIM_THRESHOLD = 0.995


def compare_images(test_img: Path, ref_img: Path) -> tuple[bool, float]:
    test = np.asarray(Image.open(test_img).convert("RGB"))
    ref = np.asarray(Image.open(ref_img).convert("RGB"))
    if test.shape != ref.shape:
        return False, 0.0
    ssim = structural_similarity(
        ref, test,
        channel_axis=-1,
        data_range=255,
        gaussian_weights=True,
    )
    return ssim >= SSIM_THRESHOLD, ssim


def run_one(entry: dict) -> dict:
    tag = entry["tag"]
    stem = Path(entry["script_path"]).stem
    name = f"{tag}/{stem}"
    script = ROOT / entry["script_path"]
    rw_var = entry.get("render_window_var", "render_window")

    if not script.exists():
        return {"name": name, "status": "FAIL", "reason": "script not found"}

    IMAGES.mkdir(parents=True, exist_ok=True)
    out_img = IMAGES / entry["output_image"]

    env = os.environ.copy()
    env["VTK_DEFAULT_RENDER_WINDOW_OFFSCREEN"] = "1"
    env["VPE_DATA_DIR"] = str(DATA_DIR)

    try:
        result = subprocess.run(
            [sys.executable, str(HELPER), str(script), str(out_img), rw_var],
            capture_output=True, text=True, timeout=10, env=env,
        )
    except subprocess.TimeoutExpired:
        return {"name": name, "status": "FAIL", "reason": "timeout (10s)"}

    if result.returncode != 0:
        err = result.stderr.strip().split("\n")
        # Skip VTK log/timestamp lines, find the real error
        real = [l for l in err if not l.startswith("20") and "ERR|" not in l and "WARN|" not in l and l.strip()]
        msg = (real[-1] if real else err[-1] if err else "unknown error")[:200]
        return {"name": name, "status": "FAIL", "reason": msg}

    if not out_img.exists() or out_img.stat().st_size == 0:
        return {"name": name, "status": "FAIL", "reason": "no image produced"}

    ref = script.with_suffix(".png")
    if ref.exists():
        passed, ssim = compare_images(out_img, ref)
        if not passed:
            return {"name": name, "status": "FAIL", "reason": f"image mismatch SSIM={ssim:.4f}"}

    return {"name": name, "status": "PASS", "reason": ""}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", help="run only this tag")
    parser.add_argument("--name", help="run only tests matching this substring")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text())

    if args.tag:
        manifest = [e for e in manifest if e["tag"] == args.tag]
    if args.name:
        manifest = [e for e in manifest if args.name in Path(e["script_path"]).stem]

    manifest = [e for e in manifest if not e.get("skip")]

    total = len(manifest)
    results = []
    passed = 0

    for i, entry in enumerate(manifest, 1):
        name = f"{entry['tag']}/{Path(entry['script_path']).stem}"
        print(f"[{i}/{total}] {name} ... ", end="", flush=True)
        r = run_one(entry)
        results.append(r)
        if r["status"] == "PASS":
            passed += 1
            print("PASS")
        else:
            print(f"FAIL  {r['reason']}")

    with open(REPORT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "status", "reason"])
        w.writeheader()
        w.writerows(results)

    failed = total - passed
    print(f"\n{passed} passed, {failed} failed out of {total}")
    print(f"Report: {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
