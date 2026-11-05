"""
Strip baked-in body copy + CTAs from the new hero banner so HTML can own those.
Keeps headline + 'Everything Your Brand Needs...' in the artwork.
"""
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
src = root / "assets" / "hero-banner-source.jpg"
out = root / "assets" / "hero-banner.jpg"
merch = root / "assets" / "hero-merch.jpg"

im = Image.open(src).convert("RGB")
w, h = im.size
navy = (0, 40, 80)  # brand navy — don't sample from white headline glyphs
draw = ImageDraw.Draw(im)

# Body paragraph + buttons sit under the light-blue subhead (~y 132 on 266px art)
y0 = 132
for y in range(y0, h):
    edge = int(w * (0.55 - 0.12 * (y / max(h - 1, 1))))
    draw.line([(8, y), (edge, y)], fill=navy)

# Scrub leftover light/orange button pixels left of the diagonal
pixels = im.load()
for y in range(y0, h):
    edge = int(w * (0.55 - 0.12 * (y / max(h - 1, 1))))
    for x in range(8, edge):
        r, g, b = pixels[x, y]
        if r > 180 and g > 80 and b < 80:
            continue  # orange seam accent
        if r < 100 and g > 140 and b < 100:
            continue  # plant greens near the cut
        if r > 60 or g > 70 or b > 120:
            pixels[x, y] = navy

im.save(out, quality=92)
print("wrote", out.name, im.size)

x_cut = int(w * 0.42)
im.crop((x_cut, 0, w, h)).resize((900, 500), Image.Resampling.LANCZOS).save(
    merch, quality=90
)
print("wrote", merch.name)
