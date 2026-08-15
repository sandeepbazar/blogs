// SPDX-FileCopyrightText: 2026 Sandeep Bazar
// SPDX-License-Identifier: Apache-2.0
//
// Progressive enhancement only. Every feature here degrades to a working page
// with JavaScript disabled: cards are visible by default, filters simply do
// not appear to do anything, and the theme falls back to dark.

(() => {
  "use strict";

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------- theme -- */

  const toggle = document.getElementById("theme");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch { /* private mode */ }
    });
  }

  /* ---------------------------------------------------------- progress -- */

  const bar = document.querySelector(".progress");
  if (bar) {
    const update = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = max > 0 ? `${(window.scrollY / max) * 100}%` : "0%";
    };
    addEventListener("scroll", update, { passive: true });
    addEventListener("resize", update);
    update();
  }

  /* ------------------------------------------------------------ reveal -- */

  // The hidden start state only exists inside a no-preference media query, so
  // there is nothing to reveal when motion is unwelcome.
  const revealables = document.querySelectorAll(".reveal");
  if (revealables.length && !reduced && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, i) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          el.style.transitionDelay = `${Math.min(i * 55, 260)}ms`;
          el.classList.add("is-in");
          io.unobserve(el);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.06 }
    );
    revealables.forEach((el) => io.observe(el));
  } else {
    revealables.forEach((el) => el.classList.add("is-in"));
  }

  /* ------------------------------------------------------------ filter -- */

  const grid = document.getElementById("grid");
  if (grid) {
    const cards = Array.from(grid.querySelectorAll(".card"));
    const pills = Array.from(document.querySelectorAll(".pill"));
    const search = document.getElementById("q");
    const count = document.getElementById("count");
    const empty = document.getElementById("empty");

    let category = "all";

    const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

    const apply = () => {
      const term = (search?.value || "").trim().toLowerCase();
      let shown = 0;

      cards.forEach((card) => {
        const matchesCategory = category === "all" || card.dataset.category === category;
        const matchesTerm = !term || card.dataset.search.includes(term);
        const visible = matchesCategory && matchesTerm;
        card.hidden = !visible;
        if (visible) shown += 1;
      });

      pills.forEach((p) => p.setAttribute("aria-pressed", String(p.dataset.filter === category)));
      if (count) count.textContent = `${shown} shown`;
      if (empty) empty.hidden = shown !== 0;
    };

    pills.forEach((pill) => {
      pill.addEventListener("click", () => {
        category = pill.dataset.filter;
        const hash = category === "all" ? "" : `#${slug(category)}`;
        history.replaceState(null, "", hash || location.pathname + location.search);
        apply();
      });
    });

    if (search) {
      search.addEventListener("input", apply);
      // Escape clears the field rather than only blurring it.
      search.addEventListener("keydown", (e) => {
        if (e.key === "Escape") { search.value = ""; apply(); }
      });
    }

    // Restore a category from the URL so #agentic-ai is shareable.
    const fromHash = location.hash.slice(1);
    if (fromHash) {
      const match = pills.find((p) => slug(p.dataset.filter) === fromHash);
      if (match) category = match.dataset.filter;
    }

    apply();
  }

  /* --------------------------------------------------------------- toc -- */

  const toc = document.querySelector(".toc");
  if (toc && "IntersectionObserver" in window) {
    const links = new Map();
    toc.querySelectorAll("a").forEach((a) => links.set(a.getAttribute("href").slice(1), a));
    const headings = Array.from(links.keys())
      .map((id) => document.getElementById(id))
      .filter(Boolean);

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          links.forEach((a) => a.classList.remove("is-active"));
          links.get(entry.target.id)?.classList.add("is-active");
        });
      },
      { rootMargin: "-15% 0px -70% 0px" }
    );
    headings.forEach((h) => io.observe(h));
  }
})();
