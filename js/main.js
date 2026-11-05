/**
 * Metro site — shared interactivity for homepage + interior pages.
 * Mobile nav (same header everywhere) + optional custom-project dialog.
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

    nav.querySelectorAll(".has-dropdown > .nav-link").forEach((link) => {
      link.addEventListener("click", (event) => {
        if (window.matchMedia("(max-width: 900px)").matches) {
          event.preventDefault();
          link.parentElement.classList.toggle("is-open");
        }
      });
    });

    // Close drawer after any in-nav destination click on small screens
    nav.querySelectorAll("a").forEach((anchor) => {
      anchor.addEventListener("click", () => {
        if (!window.matchMedia("(max-width: 900px)").matches) return;
        if (anchor.parentElement.classList.contains("has-dropdown")) return;
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
      });
    });
  }

  // --- Custom project modal (homepage only) ---
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
    event.preventDefault();
    projectDialog.close();
    projectSent.showModal();
  });

  projectSent.querySelectorAll("[data-close-sent]").forEach((button) => {
    button.addEventListener("click", () => projectSent.close());
  });
})();
