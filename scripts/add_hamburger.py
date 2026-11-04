"""Add hamburger toggle + nav.js to all interior pages."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
toggle = (
    '<button class="nav-toggle" type="button" aria-expanded="false" '
    'aria-controls="site-nav" aria-label="Toggle menu">'
    "<span></span><span></span><span></span></button>"
)
script = '<script src="assets/nav.js"></script>'

for path in root.glob("*.html"):
    if path.name == "index.html":
        continue
    text = path.read_text(encoding="utf-8")
    original = text

    # Insert hamburger after logo link if missing
    if 'class="nav-toggle"' not in text:
        text = re.sub(
            r'(<a href="index\.html"><img class="logo"[^>]*></a>)',
            r"\1" + toggle,
            text,
            count=1,
        )

    # Ensure nav has id="site-nav"
    if 'id="site-nav"' not in text:
        text = text.replace("<nav>", '<nav id="site-nav">', 1)
        text = text.replace("<nav >", '<nav id="site-nav">', 1)

    # Include nav.js once
    if "assets/nav.js" not in text:
        if "</body>" in text:
            text = text.replace("</body>", f"{script}</body>", 1)
        else:
            text += script

    if text != original:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)
    else:
        print("unchanged", path.name)
