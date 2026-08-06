#!/usr/bin/env python3
"""Extract printable ASCII and UTF-16LE strings without external tools."""
from pathlib import Path
import argparse,re
ap=argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--min",type=int,default=6); args=ap.parse_args()
data=Path(args.path).read_bytes(); n=args.min
patterns=[(re.compile(rb"[ -~]{%d,}"%n),lambda m:m.group().decode("ascii","replace")),(re.compile(rb"(?:[ -~]\x00){%d,}"%n),lambda m:m.group().decode("utf-16le","replace"))]
seen=set()
for rx,fn in patterns:
    for m in rx.finditer(data):
        s=fn(m)
        if s not in seen: print(f"0x{m.start():x}\t{s}"); seen.add(s)
