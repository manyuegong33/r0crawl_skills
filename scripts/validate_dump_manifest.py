#!/usr/bin/env python3
"""Validate a small dump manifest before importing an artifact."""
from pathlib import Path
import argparse,json,hashlib
ap=argparse.ArgumentParser(); ap.add_argument("manifest"); args=ap.parse_args()
m=json.loads(Path(args.manifest).read_text(encoding="utf-8")); errors=[]
for key in ["artifact","sha256","architecture"]:
    if not m.get(key): errors.append(f"missing:{key}")
p=Path(m.get("artifact",""))
if not p.is_file(): errors.append("artifact-not-found")
else:
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if m.get("sha256") and h.lower()!=m["sha256"].lower(): errors.append("sha256-mismatch")
print("valid" if not errors else "invalid: "+", ".join(errors))
raise SystemExit(0 if not errors else 1)
