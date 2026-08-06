from pathlib import Path
import sys
root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
bad = []
for p in root.rglob("*"):
    if p.is_file() and p.suffix.lower() in {".md", ".yaml", ".yml", ".py", ".json"}:
        try:
            p.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            bad.append((p, str(e)))
if bad:
    for p,e in bad:
        print(f"BAD {p}: {e}")
    raise SystemExit(1)
print("UTF-8 OK")
