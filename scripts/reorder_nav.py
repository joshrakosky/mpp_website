"""Reorder nav: Home, About Us, Our Team, Why Metro?, EQP — drop Contact."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]

nav_pretty = """<a href="index.html">Home</a>
        <a href="about-us.html">About Us</a>
        <a href="our-team.html">Our Team</a>
        <a href="why-metro.html">Why Metro?</a>
        <a href="eqp-program.html">EQP Program</a>
        <a class="search" href="https://metroprintedproducts.com">Search Promotional Products</a>"""

nav_mini = (
    '<a href="index.html">Home</a>'
    '<a href="about-us.html">About Us</a>'
    '<a href="our-team.html">Our Team</a>'
    '<a href="why-metro.html">Why Metro?</a>'
    '<a href="eqp-program.html">EQP Program</a>'
    '<a class="search" href="https://metroprintedproducts.com">Search Promotional Products</a>'
)

pat = re.compile(
    r'<a href="index\.html">Home</a>.*?<a class="search" href="https://metroprintedproducts\.com">Search Promotional Products</a>',
    re.DOTALL,
)

for path in root.glob("*.html"):
    if path.name == "index.html":
        continue
    text = path.read_text(encoding="utf-8")
    m = re.search(r"<nav[^>]*>(.*?)</nav>", text, re.DOTALL)
    if not m:
        print("no nav", path.name)
        continue
    inner = m.group(1)
    repl = nav_pretty if "\n" in inner else nav_mini
    new_text, n = pat.subn(repl, text, count=1)
    if n:
        path.write_text(new_text, encoding="utf-8")
        print("updated", path.name)
    else:
        print("FAIL", path.name)
