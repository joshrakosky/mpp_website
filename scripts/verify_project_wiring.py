from pathlib import Path

for path in sorted(Path(".").glob("*.html")):
    text = path.read_text(encoding="utf-8")
    print(
        f"{path.name:35} "
        f"open={text.count('data-open-project')} "
        f"modal={'custom-project' in text} "
        f"cta_link_left={'index.html#cta\">Start a Custom Project' in text} "
        f"blank={text.count('target=\"_blank\"')}"
    )
