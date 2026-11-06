from pathlib import Path
from PIL import Image

eqp = Path("assets/eqp-example.png")
im = Image.open(eqp)
print("eqp", im.size, round(eqp.stat().st_size / 1024), "KB")

svg = Path("assets/mpp_logo.svg").read_text(encoding="utf-8", errors="replace")
print("svg chars", len(svg))
print(svg[:500])
