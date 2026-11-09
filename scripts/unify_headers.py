"""Rewrite every interior page to use the shared homepage header + css/styles.css."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]

ACTIVE = {
    "about-us.html": "about-us.html",
    "our-team.html": "our-team.html",
    "why-metro.html": "why-metro.html",
    "eqp-program.html": "eqp-program.html",
}

SEARCH = """          <li class="nav-search-mobile">
            <a class="btn btn-search" href="https://metroprintedproducts.com" target="_blank" rel="noopener noreferrer">Search Products</a>
          </li>"""

SEARCH_BTN = """      <a class="btn btn-search btn-search-desktop" href="https://metroprintedproducts.com" target="_blank" rel="noopener noreferrer">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>
          <path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        Search Products
      </a>"""


def header_html(active_href: str | None) -> str:
    items = [
        ("index.html", "Home"),
        ("about-us.html", "About Us"),
        ("our-team.html", "Our Team"),
        ("why-metro.html", "Why Metro?"),
        ("eqp-program.html", "EQP Program"),
    ]
    lis = []
    for href, label in items:
        cls = "nav-link is-active" if href == active_href else "nav-link"
        lis.append(f'          <li><a class="{cls}" href="{href}">{label}</a></li>')
    lis.append(SEARCH)
    return f"""  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Metro Printed Products home">
        <img src="assets/mpp_logo.svg" alt="Metro Printed Products" class="brand-logo" />
      </a>

      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Toggle menu">
        <span></span><span></span><span></span>
      </button>

      <nav class="primary-nav" id="primary-nav" aria-label="Primary">
        <ul class="nav-list">
{chr(10).join(lis)}
        </ul>
      </nav>

{SEARCH_BTN}
    </div>
  </header>"""


head_links = """  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/styles.css" />"""

for path in root.glob("*.html"):
    if path.name == "index.html":
        continue
    text = path.read_text(encoding="utf-8")

    # Stylesheet: always css/styles.css (+ fonts)
    text = re.sub(
        r'<link rel="stylesheet" href="assets/styles\.css"\s*/?>',
        head_links,
        text,
        count=1,
    )
    # If fonts already duplicated somehow, leave as-is

    # Replace entire <header>...</header>
    active = ACTIVE.get(path.name)
    text, n = re.subn(
        r"<header\b.*?</header>",
        header_html(active),
        text,
        count=1,
        flags=re.DOTALL,
    )
    if not n:
        print("NO HEADER", path.name)
        continue

    # Rename interior hero class to avoid colliding with homepage .hero
    text = text.replace('<section class="hero">', '<section class="page-hero">')
    text = text.replace('<section class="cta">', '<section class="page-cta">')
    text = text.replace("<footer>", '<footer class="site-footer">')

    # Shared JS
    if 'src="js/main.js"' not in text:
        text = text.replace('src="assets/nav.js"', 'src="js/main.js"')
        if 'src="js/main.js"' not in text:
            text = text.replace("</body>", '<script src="js/main.js"></script></body>')
    else:
        text = text.replace('<script src="assets/nav.js"></script>', "")

    # Interior CTAs that used bare .btn as orange fill → btn-primary
    text = re.sub(r'class="btn "', 'class="btn btn-primary"', text)
    text = re.sub(r'class="btn"', 'class="btn btn-primary"', text)
    text = text.replace('class="btn btn-primary alt"', 'class="btn alt"')
    text = text.replace('class="btn btn-primary  alt"', 'class="btn alt"')

    path.write_text(text, encoding="utf-8")
    print("unified", path.name, "active=", active)

# Retire duplicate stylesheet — keep a redirect stub so old links still work
stub = '/* Deprecated: use css/styles.css — single site stylesheet */\n@import url("../css/styles.css");\n'
(root / "assets" / "styles.css").write_text(stub, encoding="utf-8")
print("assets/styles.css -> import stub")
