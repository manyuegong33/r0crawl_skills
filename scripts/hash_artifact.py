#!/usr/bin/env python3
"""Print SHA-256 and size for an artifact."""
from pathlib import Path
import argparse, hashlib
ap=argparse.ArgumentParser(); ap.add_argument("path"); args=ap.parse_args()
p=Path(args.path); h=hashlib.sha256(); size=0
with p.open("rb") as f:
    for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk); size+=len(chunk)
print(f"path: {p.resolve()}\nsize: {size}\nsha256: {h.hexdigest()}")
