"""
1) Search Products / catalog links open in a new tab.
2) Interior "Start a Custom Project" CTAs open the shared project dialog
   (same markup + js/main.js as the homepage).
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]

# Modal block shared with index.html — keep in sync when the form changes
PROJECT_MODALS = """
  <!-- Shared custom-project form (same as homepage) -->
  <dialog class="modal" id="custom-project" aria-labelledby="project-title">
    <form class="modal__panel" method="dialog">
      <div class="modal__head">
        <h2 id="project-title">Start a Custom Project</h2>
        <button type="button" class="modal__close" data-close aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <p class="modal__lead">Tell us who to reach and what you need in hand.</p>

      <div class="modal__grid">
        <label>Full name
          <input type="text" name="name" autocomplete="name" required />
        </label>
        <label>Email
          <input type="email" name="email" autocomplete="email" required />
        </label>
        <label>Phone
          <input type="tel" name="phone" autocomplete="tel" />
        </label>
        <label>Department
          <input type="text" name="department" autocomplete="organization" />
        </label>
      </div>

      <label>Scope of work
        <textarea name="scope" rows="5" required placeholder="Quantities, products, branding, budget, shipping, and anything the team should know."></textarea>
      </label>
      <label>In-hands date
        <input type="date" name="in-hands" required />
      </label>

      <div class="modal__actions">
        <button type="button" class="btn btn-ghost-dark" data-close>Cancel</button>
        <button type="submit" class="btn btn-primary" value="submit">Submit request</button>
      </div>
    </form>
  </dialog>

  <dialog class="modal" id="project-sent" aria-labelledby="project-sent-title">
    <div class="modal__panel">
      <div class="modal__head">
        <h2 id="project-sent-title">Request received</h2>
        <button type="button" class="modal__close" data-close-sent aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <p class="modal__lead">A rep will contact you within 30 minutes. If you have any questions, please reach out to <a href="mailto:metroinfo@proforma.com">metroinfo@proforma.com</a>.</p>
      <div class="modal__actions">
        <button type="button" class="btn btn-primary" data-close-sent>Close</button>
      </div>
    </div>
  </dialog>
"""

NEW_TAB = ' target="_blank" rel="noopener noreferrer"'

for path in root.glob("*.html"):
    text = path.read_text(encoding="utf-8")
    original = text

    # --- Search / catalog: open in a new tab ---
    def add_new_tab(match: re.Match) -> str:
        tag = match.group(0)
        if 'target="_blank"' in tag:
            return tag
        # Insert before the closing > of the opening <a ...>
        return tag[:-1] + NEW_TAB + ">"

    text = re.sub(
        r'<a([^>]*href="https://metroprintedproducts\.com"[^>]*)>',
        lambda m: m.group(0)
        if 'target="_blank"' in m.group(0)
        else m.group(0)[:-1] + NEW_TAB + ">",
        text,
    )

    # --- Interior CTAs: open the project modal instead of jumping home ---
    if path.name != "index.html":
        text = re.sub(
            r'<a class="btn btn-primary" href="index\.html#cta">Start a Custom Project</a>',
            '<button type="button" class="btn btn-primary" data-open-project>Start a Custom Project</button>',
            text,
        )
        # Panel CTAs that also sent people to the homepage form
        text = re.sub(
            r'<a class="btn btn-primary" href="index\.html#cta">Talk to Metro about EQP</a>',
            '<button type="button" class="btn btn-primary" data-open-project>Talk to Metro about EQP</button>',
            text,
        )
        # Inject dialogs once if this page can open the form
        if 'data-open-project' in text and 'id="custom-project"' not in text:
            if '<script src="js/main.js"></script>' in text:
                text = text.replace(
                    '<script src="js/main.js"></script>',
                    PROJECT_MODALS + '\n  <script src="js/main.js"></script>',
                )
            else:
                text = text.replace("</body>", PROJECT_MODALS + "\n</body>")

    if text != original:
        path.write_text(text, encoding="utf-8")
        print("updated", path.name)
    else:
        print("unchanged", path.name)

# Keep header generator in sync for Search Products new-tab
unify = root / "scripts" / "unify_headers.py"
if unify.exists():
    u = unify.read_text(encoding="utf-8")
    u2 = u.replace(
        'href="https://metroprintedproducts.com"',
        'href="https://metroprintedproducts.com" target="_blank" rel="noopener noreferrer"',
    )
    # Avoid double-applying if re-run
    u2 = u2.replace(
        'target="_blank" rel="noopener noreferrer" target="_blank" rel="noopener noreferrer"',
        'target="_blank" rel="noopener noreferrer"',
    )
    if u2 != u:
        unify.write_text(u2, encoding="utf-8")
        print("updated scripts/unify_headers.py")
