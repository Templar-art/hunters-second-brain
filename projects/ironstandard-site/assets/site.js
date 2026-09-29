(function () {
  "use strict";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---- reveals ----
     Content is visible in the stylesheet. JS opts elements INTO the
     animation, and only ones that start below the fold, so nothing above
     it is ever gated and a failed observer can never blank the page. */
  var items = document.querySelectorAll(".rv");
  var canAnimate =
    "IntersectionObserver" in window &&
    !reduced.matches &&
    document.visibilityState === "visible";

  if (canAnimate) {
    var pending = [];
    items.forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight * 0.92) {
        el.classList.add("will-reveal");
        pending.push(el);
      }
    });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.remove("will-reveal");
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    pending.forEach(function (el) { io.observe(el); });

    /* Failsafe. If the observer never fires (an off-screen frame, a
       renderer that does not scroll), everything still resolves. These
       elements are below the fold, so this is invisible to a real reader. */
    window.setTimeout(function () {
      pending.forEach(function (el) { el.classList.remove("will-reveal"); });
    }, 5000);
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

  /* ---- scroll depth: a hairline in the header, not a progress bar ----
     rAF-throttled. Orientation is the one piece of interface the page
     was genuinely missing. */
  var line = document.createElement("div");
  line.className = "scroll-line";
  header.appendChild(line);
  var lineTicking = false;
  function drawLine() {
    if (lineTicking) return;
    lineTicking = true;
    requestAnimationFrame(function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var pct = max > 0 ? Math.min(window.scrollY / max, 1) : 0;
      line.style.transform = "scaleX(" + pct.toFixed(4) + ")";
      lineTicking = false;
    });
  }
  window.addEventListener("scroll", drawLine, { passive: true });
  window.addEventListener("resize", drawLine, { passive: true });
  drawLine();

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

  /* Journeys from Coaching land with the right route already chosen
     (strategy p18: Coaching > Coaching enquiry / Trainer enquiry). */
  var wanted = new URLSearchParams(window.location.search).get("type");
  if (wanted && MAP[wanted]) select.value = wanted;

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

  /* Pre-commitment disclosure: if the endpoint is not live, say so BEFORE
     the visitor fills anything in, not after they press send. */
  (function preflight() {
    var ep = form.getAttribute("data-endpoint");
    if (!ep || ep === PLACEHOLDER) {
      var pre = document.createElement("p");
      pre.className = "form-status";
      pre.textContent = "This form is not connected yet. Nothing sent here reaches us, and the enquiry route goes live before launch.";
      form.insertBefore(pre, form.firstElementChild);
    }
  })();

  function fieldError(id, msg) {
    var el = document.getElementById(id);
    el.closest(".field").classList.add("field-invalid");
    el.setAttribute("aria-invalid", "true");
    say(msg);
    el.focus();
  }

  function clearErrors() {
    form.querySelectorAll(".field-invalid").forEach(function (f) {
      f.classList.remove("field-invalid");
      var i = f.querySelector("input,select,textarea");
      if (i) i.removeAttribute("aria-invalid");
    });
  }

  var button = form.querySelector('button[type="submit"]');
  var sink = document.querySelector('iframe[name="enquirySink"]');
  var sending = false;
  var timer = null;

  function setSending(on) {
    sending = on;
    button.disabled = on;
    button.setAttribute("aria-busy", on ? "true" : "false");
    button.textContent = on ? "Sending\u2026" : "Send enquiry";
  }

  function finish(ok) {
    window.clearTimeout(timer);
    if (!sending) return;
    setSending(false);
    if (ok) {
      say("Thank you. Your enquiry has reached us and goes to the right person.");
      form.reset();
      sync();
    } else {
      /* Input is kept, so trying again costs nothing. */
      say("That did not go through. Your details are still here, so please try again in a moment.");
    }
  }

  /* Apps Script sends no CORS headers, so the response body cannot be read.
     The handler posts a message back to this window instead (see
     enquiry-handler.gs reply()). No answer in 20s is a failure. */
  window.addEventListener("message", function (e) {
    if (!/^https:\/\/([a-z0-9-]+\.)*(google\.com|googleusercontent\.com)$/.test(e.origin)) return;
    var d = e.data;
    if (!d || d.source !== "iron-standard-enquiry") return;
    if (d.ok) { finish(true); return; }
    if (d.error === "invalid") {
      window.clearTimeout(timer);
      setSending(false);
      say("We could not accept those details. Please check your name and email and send again.");
      return;
    }
    finish(false);
  });

  /* Fallback for a handler that does not post a message: a load means the
     server answered. Give the message a moment to arrive first. */
  if (sink) {
    sink.addEventListener("load", function () {
      if (sending) window.setTimeout(function () { finish(true); }, 3000);
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (sending) return;              /* no double submission */
    clearErrors();

    /* Validation runs FIRST. It used to sit inside the live-endpoint branch,
       which meant an empty form submitted cleanly whenever the endpoint was
       still a placeholder. */
    var name = document.getElementById("name");
    var email = document.getElementById("email");
    name.value = name.value.trim();
    email.value = email.value.trim();
    if (!name.value) { fieldError("name", "Please add your name so we know who we are replying to."); return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value)) {
      fieldError("email", "Please check your email address. We reply to this, so a typo means you hear nothing."); return;
    }

    var endpoint = form.getAttribute("data-endpoint");
    if (!endpoint || endpoint === PLACEHOLDER) {
      say("This form is not connected yet, so nothing was sent. The enquiry route goes live before launch.");
      return;
    }

    if (navigator.onLine === false) {
      say("You appear to be offline. Your details are still here, so send again once you have a connection.");
      return;
    }

    /* preventDefault() above stops the native submit, so it has to be
       re-issued explicitly. The earlier version set form.action and never
       submitted, then showed a success message on a timer: every enquiry
       would have been lost the day the endpoint went live. */
    form.action = endpoint;
    setSending(true);
    say("Sending your enquiry.");
    timer = window.setTimeout(function () { finish(false); }, 20000);
    HTMLFormElement.prototype.submit.call(form);
  });
})();

/* ============================================================
   FAQ: a link to an individual answer opens it.
   Answers are native <details>, so the text stays crawlable.
   ============================================================ */
(function () {
  "use strict";
  function openTarget() {
    var id = decodeURIComponent(window.location.hash.slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (el && el.tagName === "DETAILS") el.open = true;
  }
  openTarget();
  window.addEventListener("hashchange", openTarget);
})();
