"""Quick local link check for Metro HTML pages."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
missing = []
for f in root.glob("*.html"):
    text = f.read_text(encoding="utf-8")
    for m in re.findall(r"""(?:href|src)=["']([^"']+)["']""", text):
        if m.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        target = m.split("#", 1)[0]
        if not target:
            continue
        p = (f.parent / target).resolve()
        if not p.exists():
            missing.append(f"{f.name} -> {m}")

print(f"checked {len(list(root.glob('*.html')))} html files")
print(f"missing {len(missing)}")
for row in missing:
    print(row)
