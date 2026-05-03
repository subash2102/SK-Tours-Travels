(() => {
  const navToggle = document.querySelector("[data-nav-toggle]");
  const navLinks = document.querySelector("[data-nav-links]");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      navLinks.classList.toggle("open");
    });
    navLinks.addEventListener("click", (e) => {
      const a = e.target.closest("a");
      if (a) navLinks.classList.remove("open");
    });
  }

  const io = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) entry.target.classList.add("is-in");
      }
    },
    { threshold: 0.12 }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  document.querySelectorAll("[data-loading-btn]").forEach((btn) => {
    const form = btn.closest("form");
    if (!form) return;
    form.addEventListener("submit", () => {
      btn.disabled = true;
      const old = btn.textContent;
      btn.dataset.oldText = old;
      btn.textContent = "Submitting…";
      window.setTimeout(() => {
        // If the request fails client-side validation, re-enable.
        btn.disabled = false;
        btn.textContent = btn.dataset.oldText || old;
      }, 2000);
    });
  });
})();
