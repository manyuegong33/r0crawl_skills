#!/usr/bin/env python3
"""Redact common secrets in text captures before sharing them."""
from pathlib import Path
import argparse,re
ap=argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dst"); args=ap.parse_args()
s=Path(args.src).read_text(encoding="utf-8",errors="replace")
patterns=[(r"(?i)(authorization\s*[:=]\s*Bearer\s+)[^\s,;]+",r"\1<REDACTED>"),(r"(?i)(cookie\s*[:=]\s*)[^\n]+",r"\1<REDACTED>"),(r"(?i)(api[_-]?key|token|secret|password)(\s*[=:]\s*)[^&\s,;]+",r"\1\2<REDACTED>")]
for rx,repl in patterns: s=re.sub(rx,repl,s)
Path(args.dst).write_text(s,encoding="utf-8"); print(args.dst)
