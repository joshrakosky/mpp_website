/**
 * Metro demo — light interactivity.
 * Mobile nav + custom project dialog (same flow as syk_homepage).
 */
(function () {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("#primary-nav");
  const yearEl = document.querySelector("#year");

  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  // --- Mobile nav ---
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });

    // Expand dropdown sections on mobile when parent is tapped
    nav.querySelectorAll(".has-dropdown > .nav-link").forEach((link) => {
      link.addEventListener("click", (event) => {
        if (window.matchMedia("(max-width: 900px)").matches) {
          event.preventDefault();
          link.parentElement.classList.toggle("is-open");
        }
      });
    });

    // Close menu after in-page nav clicks
    nav.querySelectorAll("a[href^='#']").forEach((anchor) => {
      anchor.addEventListener("click", () => {
        if (window.matchMedia("(max-width: 900px)").matches) {
          if (!anchor.parentElement.classList.contains("has-dropdown")) {
            toggle.setAttribute("aria-expanded", "false");
            nav.classList.remove("is-open");
          }
        }
      });
    });
  }

  // --- Custom project modal (open → validate → confirmation) ---
  const projectDialog = document.getElementById("custom-project");
  const projectSent = document.getElementById("project-sent");
  if (!projectDialog || !projectSent) return;

  const form = projectDialog.querySelector("form");

  document.querySelectorAll("[data-open-project]").forEach((button) => {
    button.addEventListener("click", () => {
      form.reset();
      projectDialog.showModal();
    });
  });

  projectDialog.querySelectorAll("[data-close]").forEach((button) => {
    button.addEventListener("click", () => projectDialog.close());
  });

  form.addEventListener("submit", (event) => {
    // Demo only — no network send; show confirmation after HTML5 validation
    event.preventDefault();
    projectDialog.close();
    projectSent.showModal();
  });

  projectSent.querySelectorAll("[data-close-sent]").forEach((button) => {
    button.addEventListener("click", () => projectSent.close());
  });
})();
