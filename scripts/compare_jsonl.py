#!/usr/bin/env python3
"""Compare two JSONL fixture files and show the first structural difference."""
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser(); ap.add_argument("left"); ap.add_argument("right"); args=ap.parse_args()
a=[json.loads(x) for x in Path(args.left).read_text(encoding="utf-8").splitlines() if x.strip()]
b=[json.loads(x) for x in Path(args.right).read_text(encoding="utf-8").splitlines() if x.strip()]
print(f"left={len(a)} right={len(b)}")
for i,(x,y) in enumerate(zip(a,b)):
    if x!=y: print(f"first_diff_line={i+1}\nleft={json.dumps(x,ensure_ascii=False)}\nright={json.dumps(y,ensure_ascii=False)}"); break
else:
    if len(a)==len(b): print("parity=match")
    else: print("parity=length-mismatch")
