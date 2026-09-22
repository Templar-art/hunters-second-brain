(function () {
  "use strict";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---- reveals: IntersectionObserver, one idea per reveal ---- */
  var items = document.querySelectorAll(".rv");
  if (!("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---- header condenses on scroll, via a sentinel not a listener ---- */
  var header = document.getElementById("header");
  var sentinel = document.createElement("div");
  sentinel.style.cssText = "position:absolute;top:0;left:0;width:1px;height:8px;pointer-events:none;";
  document.body.prepend(sentinel);
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (e) {
      header.classList.toggle("is-stuck", !e[0].isIntersecting);
    }).observe(sentinel);
  }

  /* ---- mobile nav ---- */
  var toggle = document.getElementById("navToggle");
  var panel = document.getElementById("navPanel");
  if (toggle && panel) {
    var setOpen = function (open) {
      panel.setAttribute("data-open", String(open));
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      document.body.style.overflow = open ? "hidden" : "";
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    panel.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { setOpen(false); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false); toggle.focus();
      }
    });
  }

  /* ---- hero parallax: desktop only, low intensity, off for reduced motion ---- */
  var media = document.getElementById("heroMedia");
  var img = media && media.querySelector("img");
  var desktop = window.matchMedia("(min-width: 1024px)");
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = Math.min(window.scrollY, 900) * 0.07;   /* max ~63px */
      img.style.transform = "translate3d(0," + y.toFixed(1) + "px,0)";
      ticking = false;
    });
  }
  function syncParallax() {
    var on = desktop.matches && !reduced.matches;
    if (on) {
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    } else {
      window.removeEventListener("scroll", onScroll);
      if (img) img.style.transform = "";
    }
  }
  if (img) {
    syncParallax();
    desktop.addEventListener("change", syncParallax);
    reduced.addEventListener("change", syncParallax);
  }
})();

/* ============================================================
   Contact page: conditional enquiry routing.
   No-ops on every other page.
   ============================================================ */
(function () {
  "use strict";
  var select = document.getElementById("enquiryType");
  if (!select) return;

  var routing = document.getElementById("routingNote");
  var extra = document.getElementById("extraField");
  var extraLabel = document.getElementById("extraLabel");
  var extraInput = document.getElementById("extraInput");

  var MAP = {
    membership:   { note: "Membership enquiries are answered by the membership team." },
    coaching:     { note: "Coaching enquiries go straight to the coaching team.",
                    label: "What are you training for?",
                    placeholder: "A meet, a lift, general strength" },
    trainer:      { note: "Trainer enquiries are handled separately from member enquiries.",
                    label: "Tell us about your practice",
                    placeholder: "How you work and roughly how many clients" },
    physiotherapy:{ note: "Physiotherapy enquiries go to the practitioner team.",
                    label: "What are you dealing with?",
                    placeholder: "Injury, rehabilitation or performance support" },
    partnership:  { note: "Partnership and supplier enquiries are reviewed by the founder.",
                    label: "Company",
                    placeholder: "Company name" },
    media:        { note: "Media enquiries are answered by the founder." },
    general:      { note: "General enquiries are answered by the main inbox." }
  };

  function sync() {
    var cfg = MAP[select.value];
    if (!cfg) { routing.hidden = true; extra.hidden = true; extraInput.required = false; return; }
    routing.textContent = cfg.note;
    routing.hidden = false;
    if (cfg.label) {
      extraLabel.textContent = cfg.label;
      extraInput.placeholder = cfg.placeholder || "";
      extra.hidden = false;
    } else {
      extra.hidden = true;
      extraInput.value = "";
    }
  }

  select.addEventListener("change", sync);
  sync();

  /* Submission. Until a real Web App URL is pasted into data-endpoint the
     form stays deliberately inert and says so, rather than appearing to
     send and silently discarding the enquiry. */
  var form = document.getElementById("enquiryForm");
  var status = document.getElementById("formStatus");
  if (!form || !status) return;

  var PLACEHOLDER = "PASTE_WEB_APP_URL_HERE";

  function say(msg) {
    status.textContent = msg;
    status.hidden = false;
  }

  form.addEventListener("submit", function (e) {
    var endpoint = form.getAttribute("data-endpoint");
    var live = endpoint && endpoint !== PLACEHOLDER;

    if (!live) {
      e.preventDefault();
      say("This form is not connected yet. The enquiry route is set up before launch.");
      return;
    }

    /* Minimal client-side checks so a mistyped address is caught here
       rather than becoming an enquiry nobody can reply to. */
    var email = document.getElementById("email");
    var name = document.getElementById("name");
    if (!name.value.trim()) {
      e.preventDefault(); say("Please add your name."); name.focus(); return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
      e.preventDefault(); say("Please check your email address."); email.focus(); return;
    }

    /* The POST targets a hidden iframe, because Apps Script Web Apps do
       not return CORS headers for fetch(). Let the native submit run. */
    form.action = endpoint;
    say("Sending your enquiry.");
    window.setTimeout(function () {
      say("Thank you. Your enquiry has been sent and goes to the right person.");
      form.reset();
      sync();
    }, 900);
  });
})();
