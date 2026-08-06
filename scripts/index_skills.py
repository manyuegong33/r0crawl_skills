from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
items = []
for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
    text = p.read_text(encoding="utf-8-sig")
    m = re.search(r"^name:\s*(.+)$", text, re.M)
    d = re.search(r"^description:\s*(.+)$", text, re.M)
    items.append((m.group(1).strip() if m else p.parent.name, d.group(1).strip() if d else ""))

out = ["# Generated Skill Index", "", "| Name | Description |", "|---|---|"]
out += [f"| `{n}` | {d} |" for n, d in items]
(ROOT / "references" / "generated-index.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"indexed {len(items)} skills")
