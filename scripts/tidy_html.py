"""Light cleanup after unify_headers.py."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for path in root.glob("*.html"):
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        '<script src="js/main.js"></script></body>',
        '  <script src="js/main.js"></script>\n</body>',
    )
    text = text.replace('    <link rel="preconnect"', '  <link rel="preconnect"')
    text = text.replace('    <header class="site-header">', '  <header class="site-header">')
    if text != original:
        path.write_text(text, encoding="utf-8")
        print("tidied", path.name)
