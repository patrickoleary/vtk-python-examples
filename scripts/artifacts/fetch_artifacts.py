#!/usr/bin/env python3
"""Fetch pinned cross-repo artifacts declared in artifacts.lock.json.

Each artifact has a single editable `source` that is either:
  - an http(s):// URL   (e.g. a GitHub release asset), or
  - a local filesystem path / file:// URL (handy before any remote exists).

The file is fetched to `dest`, then its sha256 is verified against the pinned
value. Use --update to (re)download and rewrite the pinned sha256 in the lock.

Usage:
    python -m scripts.artifacts.fetch_artifacts            # fetch + verify
    python -m scripts.artifacts.fetch_artifacts --update   # fetch + re-pin sha256
    python -m scripts.artifacts.fetch_artifacts --check     # verify existing dest only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
LOCK_PATH = _ROOT / "artifacts.lock.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_url(source: str) -> bool:
    return source.startswith("http://") or source.startswith("https://")


def resolve_local(source: str) -> Path:
    if source.startswith("file://"):
        source = source[len("file://"):]
    p = Path(source).expanduser()
    if not p.is_absolute():
        p = (_ROOT / p).resolve()
    return p


def fetch(source: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if is_url(source):
        req = urllib.request.Request(source, headers={"User-Agent": "fetch-artifacts"})
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req) as r, open(dest, "wb") as out:
            shutil.copyfileobj(r, out)
    else:
        src = resolve_local(source)
        if not src.exists():
            raise SystemExit(f"ERROR: local source not found: {src}")
        shutil.copyfile(src, dest)


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch pinned cross-repo artifacts")
    ap.add_argument("--update", action="store_true", help="Re-download and re-pin sha256 in the lock")
    ap.add_argument("--check", action="store_true", help="Only verify existing dest files (no download)")
    ap.add_argument("--lock", default=str(LOCK_PATH), help="Path to artifacts.lock.json")
    args = ap.parse_args()

    lock_path = Path(args.lock)
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    artifacts = lock.get("artifacts", [])
    failed = False

    for art in artifacts:
        name = art.get("name", "?")
        dest = _ROOT / art["dest"]
        pinned = art.get("sha256", "")

        if args.check:
            if not dest.exists():
                print(f"  MISSING  {name} -> {dest}")
                failed = True
                continue
            digest = sha256_file(dest)
            ok = pinned and digest == pinned
            print(f"  {'OK ' if ok else 'BAD'}     {name}  {digest[:12]}")
            failed = failed or not ok
            continue

        print(f"  fetch    {name} <- {art['source']}")
        fetch(art["source"], dest)
        digest = sha256_file(dest)

        if args.update or not pinned:
            art["sha256"] = digest
            print(f"           pinned sha256 = {digest}")
        elif digest != pinned:
            print(f"  ERROR    sha256 mismatch for {name}:\n"
                  f"           expected {pinned}\n           got      {digest}")
            failed = True
        else:
            print(f"           verified {digest[:12]}")

    if args.update:
        lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {lock_path.name}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
