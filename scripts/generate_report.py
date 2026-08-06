#!/usr/bin/env python3
"""Generate a small Markdown report from a case directory."""
from pathlib import Path
import argparse,datetime
ap=argparse.ArgumentParser(); ap.add_argument("case"); args=ap.parse_args(); c=Path(args.case)
files=sorted(str(x.relative_to(c)) for x in c.rglob("*") if x.is_file())
out=["# Case Report",f"Generated: {datetime.datetime.now().isoformat(timespec='seconds')}","","## Files",""]+[f"- `{x}`" for x in files]
(c/"report.generated.md").write_text("\n".join(out)+"\n",encoding="utf-8"); print(c/"report.generated.md")
