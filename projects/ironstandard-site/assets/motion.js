/* ============================================================
   IRON STANDARD - SHARED MOTION
   Loaded on every page, after site.js.

   - Adds html.motion only when motion is allowed. Without it every
     page is a complete static layout (see motion.css).
   - Native scrolling is never taken over. Scroll position is read
     each frame and the animated values ease toward it, which gives
     the soft, weighted feel without hijacking the wheel.
   - One requestAnimationFrame loop, running only while an animated
     element is on screen.
   - Exposes window.ISM so page scripts (home.js) share the engine.
   ============================================================ */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (reduced.matches || !("IntersectionObserver" in window)) return;

  var root = document.documentElement;
  root.classList.add("motion");

  /* ---------- helpers ---------- */
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function seg(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }   /* progress of p between a and b */
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function lerp(a, b, t) { return a + (b - a) * t; }

  /* ---------- 1. automatic enhancement of ordinary sections ----------
     Inner pages are written as plain sections. Here they pick up the
     same language as the homepage: masked headings, wiping photos. */
  var main = document.getElementById("main");
  if (main) {
    main.querySelectorAll(":scope > section").forEach(function (sec) {
      if (sec.matches(".stage, .hs, .page-hero, .marquee")) return;
      sec.setAttribute("data-reveal", "");
      sec.querySelectorAll("h2").forEach(function (h) {
        if (h.querySelector(".ln") || h.closest(".faq-group")) return;
        h.classList.remove("rv");
        /* move the heading's own nodes into a mask; no markup is re-parsed */
        var outer = document.createElement("span"), inner = document.createElement("span");
        outer.className = "ln";
        while (h.firstChild) inner.appendChild(h.firstChild);
        outer.appendChild(inner);
        h.appendChild(outer);
      });
    });
    main.querySelectorAll(".media-r, .media-l, .alt-media, .who-pair figure, .founder-media, .coach-media").forEach(function (fig) {
      if (fig.classList.contains("wipe")) return;
      fig.classList.remove("rv");
      fig.classList.add("wipe");
      fig.setAttribute("data-reveal", "");
    });
  }

  /* ---------- 2. reveals: mark blocks "in" once ---------- */
  var reveals = document.querySelectorAll("[data-reveal], .hs-intro");
  reveals.forEach(function (sec) {
    sec.querySelectorAll(".ln").forEach(function (ln, i) {
      ln.firstElementChild.style.setProperty("--i", i);
    });
    var n = 0;
    sec.querySelectorAll(
      ".mark, .lede, .support-intro, .founder-copy p, .founder-copy .textlink, .close-sub, .hero-actions, .support-actions, .cta-row, figcaption"
    ).forEach(function (el) {
      if (el.classList.contains("rv") || el.closest(".rv")) return;   /* already animated by site.js */
      el.classList.add("fade");
      el.style.setProperty("--i", n++);
    });
    sec.querySelectorAll(".card").forEach(function (card, i) {
      card.style.setProperty("--i", i);
      card.querySelectorAll(".ico *").forEach(function (shape) {
        var len = shape.getTotalLength ? Math.ceil(shape.getTotalLength()) : 200;
        shape.style.setProperty("--len", len);
      });
    });
  });
  var revealIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); revealIO.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  reveals.forEach(function (s) { revealIO.observe(s); });
  /* Failsafe: never leave content hidden if the observer never fires */
  window.setTimeout(function () {
    reveals.forEach(function (s) { s.classList.add("in"); });
  }, 6000);

  /* ---------- 3. the scroll engine ---------- */
  var scenes = [];
  var sceneIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      scenes.forEach(function (s) { if (s.el === e.target) s.on = e.isIntersecting; });
    });
    kick();
  }, { rootMargin: "25% 0px 25% 0px" });

  function add(el, fn, mode) {
    if (!el) return;
    scenes.push({ el: el, fn: fn, mode: mode || "pin", target: 0, cur: -1, on: false });
    sceneIO.observe(el);
  }

  function measure(s) {
    var r = s.el.getBoundingClientRect();
    var vh = window.innerHeight;
    if (s.mode === "pin") {
      /* 0 when the section top hits the viewport top, 1 when its bottom meets the viewport bottom */
      return clamp(-r.top / Math.max(1, r.height - vh), 0, 1);
    }
    if (s.mode === "top") {
      /* 0 at rest, 1 once the element has scrolled fully off the top */
      return clamp(-r.top / Math.max(1, r.height), 0, 1);
    }
    /* "view": 0 entering at the bottom, 1 leaving at the top */
    return clamp((vh - r.top) / (vh + r.height), 0, 1);
  }

  var running = false;
  function kick() { if (!running) { running = true; requestAnimationFrame(tick); } }
  function tick() {
    var any = false;
    scenes.forEach(function (s) {
      if (!s.on) return;
      any = true;
      s.target = measure(s);
      if (s.cur < 0) s.cur = s.target;
      /* ease toward the scroll position: the "weight" in the motion */
      s.cur += (s.target - s.cur) * 0.12;
      if (Math.abs(s.target - s.cur) < 0.0004) s.cur = s.target;
      s.fn(s.cur);
    });
    if (any) requestAnimationFrame(tick); else running = false;
  }
  window.addEventListener("scroll", kick, { passive: true });
  window.addEventListener("resize", kick, { passive: true });

  function countUp(el) {
    var to = parseInt(el.getAttribute("data-to"), 10) || 0;
    var t0 = performance.now(), dur = 1400;
    function step(now) {
      var t = easeOut(clamp((now - t0) / dur, 0, 1));
      el.textContent = Math.round(to * t);
      if (t < 1) requestAnimationFrame(step);
    }
    el.textContent = "0";
    requestAnimationFrame(step);
  }

  window.ISM = { add: add, kick: kick, clamp: clamp, seg: seg, easeOut: easeOut, lerp: lerp, countUp: countUp };

  /* ---------- 4. page hero: focus pull on load, push-in on scroll ---------- */
  document.querySelectorAll(".page-hero").forEach(function (hero) {
    var img = hero.querySelector(".page-hero-media img");
    var media = hero.querySelector(".page-hero-media");
    var copy = hero.querySelector(".page-hero-copy");
    function go() { hero.classList.add("loaded"); }
    if (!img || img.complete) requestAnimationFrame(function () { requestAnimationFrame(go); });
    else { img.addEventListener("load", go); window.setTimeout(go, 1200); }
    add(hero, function (p) {
      if (media) media.style.transform = "translate3d(0," + (p * 18).toFixed(2) + "%,0) scale(" + lerp(1, 1.08, p).toFixed(4) + ")";
      if (copy) {
        copy.style.transform = "translate3d(0," + (-p * 120).toFixed(1) + "px,0)";
        copy.style.opacity = (1 - easeOut(seg(p, 0.1, 0.7))).toFixed(3);
      }
    }, "top");
  });

  /* ---------- 5. parallax drift on elements with data-speed ---------- */
  document.querySelectorAll("[data-speed]").forEach(function (el) {
    var speed = parseFloat(el.getAttribute("data-speed")) || 0;
    add(el, function (p) {
      var y = (p - 0.5) * speed * window.innerHeight;
      el.style.transform = "translate3d(0," + y.toFixed(1) + "px,0)";
    }, "view");
  });

  /* ---------- 6. words light up as a line crosses the screen ---------- */
  document.querySelectorAll("[data-words]").forEach(function (line) {
    var text = line.textContent.trim().split(/\s+/);
    var words = [];
    line.textContent = "";
    text.forEach(function (w, i) {
      var s = document.createElement("span");
      s.className = "w";
      s.textContent = w + (i < text.length - 1 ? " " : "");
      line.appendChild(s);
      words.push(s);
    });
    add(line, function (p) {
      var lit = Math.round(seg(p, 0.25, 0.6) * words.length);
      words.forEach(function (w, i) { w.classList.toggle("lit", i < lit); });
    }, "view");
  });

  /* ---------- 7. closing band: logo travels, photo settles ---------- */
  document.querySelectorAll(".close").forEach(function (close) {
    var logo = close.querySelector(".close-logo");
    var cbg = close.querySelector(".close-bg img");
    add(close, function (p) {
      if (logo) logo.style.transform = "translate3d(" + lerp(8, -30, p).toFixed(2) + "%,0,0)";
      if (cbg) cbg.style.transform = "scale(" + lerp(1.2, 1, p).toFixed(4) + ")";
    }, "view");
  });

  /* ---------- 8. FAQ: answers open and close smoothly ----------
     Native <details> stays the source of truth (crawlable, keyboard
     works); this only animates the height change around it. */
  document.querySelectorAll(".faq details").forEach(function (d) {
    var summary = d.querySelector("summary");
    var answer = d.querySelector(".answer");
    if (!summary || !answer || !answer.animate) return;
    var anim = null;
    summary.addEventListener("click", function (e) {
      e.preventDefault();
      if (anim) anim.cancel();
      if (d.open) {
        var h = answer.offsetHeight;
        anim = answer.animate([{ height: h + "px", opacity: 1 }, { height: "0px", opacity: 0 }],
          { duration: 380, easing: "cubic-bezier(.16,1,.3,1)" });
        anim.onfinish = function () { d.open = false; anim = null; };
      } else {
        d.open = true;
        var full = answer.offsetHeight;
        anim = answer.animate([{ height: "0px", opacity: 0 }, { height: full + "px", opacity: 1 }],
          { duration: 520, easing: "cubic-bezier(.16,1,.3,1)" });
        anim.onfinish = function () { anim = null; };
      }
    });
  });

  kick();
})();
