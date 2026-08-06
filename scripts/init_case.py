#!/usr/bin/env python3
"""Create a reproducible reverse-engineering case directory."""
from pathlib import Path
import argparse, hashlib, json, datetime

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--out", default="cases")
    args=ap.parse_args()
    safe="".join(c if c.isalnum() or c in "-_" else "-" for c in args.name).strip("-") or "case"
    case=Path(args.out)/safe
    for rel in ["evidence/raw","evidence/derived","notes","repro","tests"]:
        (case/rel).mkdir(parents=True,exist_ok=True)
    (case/"case.yaml").write_text(f"case_id: {safe}\ncreated: {datetime.date.today().isoformat()}\nobjective: locate-or-reproduce\nplatform: unknown\nartifact_sha256: null\n",encoding="utf-8")
    (case/"notes/timeline.md").write_text("# Timeline\n\n| Time | Action | Observation | Evidence |\n|---|---|---|---|\n",encoding="utf-8")
    (case/"notes/hypotheses.md").write_text("# Hypotheses\n\n## H-001\n- Hypothesis:\n- Evidence:\n- Falsifier:\n- Result: pending\n",encoding="utf-8")
    (case/"tests/fixtures.jsonl").write_text("",encoding="utf-8")
    (case/"report.md").write_text("# Report\n\n## Beginner summary\n\n## Evidence\n\n## Reproduction\n\n## Limitations\n",encoding="utf-8")
    print(case)
if __name__ == "__main__": main()
