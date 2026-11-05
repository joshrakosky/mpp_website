"""Apply homepage-style nav-link + is-active classes on interior pages."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]

# filename -> which href gets is-active (None = no top-nav highlight)
ACTIVE = {
    "about-us.html": "about-us.html",
    "our-team.html": "our-team.html",
    "why-metro.html": "why-metro.html",
    "eqp-program.html": "eqp-program.html",
    # Capability / value pages: no top-nav item selected
}

NAV_HREFS = [
    ("index.html", "Home"),
    ("about-us.html", "About Us"),
    ("our-team.html", "Our Team"),
    ("why-metro.html", "Why Metro?"),
    ("eqp-program.html", "EQP Program"),
]


def build_nav_inner(active_href: str | None, pretty: bool) -> str:
    parts = []
    for href, label in NAV_HREFS:
        cls = "nav-link is-active" if href == active_href else "nav-link"
        parts.append(f'<a class="{cls}" href="{href}">{label}</a>')
    parts.append(
        '<a class="search" href="https://metroprintedproducts.com">Search Products</a>'
    )
    if pretty:
        return "\n        " + "\n        ".join(parts) + "\n      "
    return "".join(parts)


pat = re.compile(r"(<nav[^>]*>)(.*?)(</nav>)", re.DOTALL)

for path in root.glob("*.html"):
    if path.name == "index.html":
        continue
    text = path.read_text(encoding="utf-8")
    m = pat.search(text)
    if not m:
        print("no nav", path.name)
        continue
    inner = m.group(2)
    pretty = "\n" in inner
    active = ACTIVE.get(path.name)  # None for capability pages
    new_inner = build_nav_inner(active, pretty)
    new_text = text[: m.start(2)] + new_inner + text[m.end(2) :]
    path.write_text(new_text, encoding="utf-8")
    print(f"updated {path.name} active={active}")
