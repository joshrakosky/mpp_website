"""Point site at crisp SVG logo + full-res EQP PNG."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]

for path in root.glob("*.html"):
    text = path.read_text(encoding="utf-8")
    updated = text.replace("assets/mpp-logo.png", "assets/mpp_logo.svg")
    if path.name == "eqp-program.html":
        updated = updated.replace("assets/eqp-example.jpg", "assets/eqp-example.png")
        updated = updated.replace('width="1024" height="768"', 'width="2000" height="1500"')
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        print("updated", path.name)

for path in [root / "scripts" / "unify_headers.py", root / "README.txt"]:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    updated = text.replace("assets/mpp-logo.png", "assets/mpp_logo.svg").replace(
        "mpp-logo.png", "mpp_logo.svg"
    )
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        print("updated", path.relative_to(root))

jpg = root / "assets" / "eqp-example.jpg"
if jpg.exists():
    jpg.unlink()
    print("removed eqp-example.jpg")
