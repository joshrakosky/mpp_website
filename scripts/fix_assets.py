"""One-off: clean NWBOC checkerboard + crop hero merch from mockup."""
from PIL import Image

# --- Fix NWBOC: remove baked-in checkerboard, keep black/green logo ---
src = Image.open("assets/nwboc-logo.png").convert("RGBA")
pixels = src.load()
w, h = src.size
out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
out_px = out.load()

for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        # Keep strong black logo ink
        if r < 70 and g < 70 and b < 70:
            out_px[x, y] = (20, 20, 20, 255)
            continue
        # Keep lime/green W + bar
        if g > 120 and g > r + 25 and g > b + 15:
            out_px[x, y] = (r, g, b, 255)
            continue
        # Soften near-black antialias on letter edges
        if r < 110 and g < 110 and b < 110 and (r + g + b) < 280:
            alpha = max(40, 255 - int((r + g + b) / 3 * 1.6))
            out_px[x, y] = (30, 30, 30, alpha)
            continue
        # Soft green antialias
        if g > 90 and g >= r and g >= b and (g - min(r, b)) > 10:
            out_px[x, y] = (r, g, b, min(255, int(g * 1.2)))
            continue
        # Drop checkerboard / light bg
        out_px[x, y] = (0, 0, 0, 0)

bbox = out.getbbox()
if bbox:
    out = out.crop(bbox)
out.save("assets/nwboc-logo.png")
print("nwboc fixed", out.size)

# --- Crop right half of mockup hero for media panel ---
hero = Image.open("assets/hero-banner.png").convert("RGBA")
hw, hh = hero.size
left = int(hw * 0.42)
crop = hero.crop((left, 0, hw, hh))
crop.convert("RGB").save("assets/hero-merch.jpg", "JPEG", quality=90)
print("hero merch cropped", crop.size, "from", hero.size)
