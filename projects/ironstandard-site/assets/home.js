/* ============================================================
   IRON STANDARD - HOMEPAGE MOTION
   Loaded on index.html only, after site.js.

   - Adds html.motion only when motion is allowed. Without it the
     page is a complete static layout (see home.css).
   - Native scrolling is never taken over. Scroll position is read
     each frame and the animated values ease toward it, which gives
     the soft, weighted feel without hijacking the wheel.
   - One requestAnimationFrame loop, running only while an animated
     section is on screen.
   ============================================================ */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (reduced.matches || !("IntersectionObserver" in window)) return;

  var root = document.documentElement;
  root.classList.add("motion");

  /* ---------- helpers ---------- */
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  /* progress of p between a and b, clamped 0..1 */
  function seg(p, a, b) { return clamp((p - a) / (b - a), 0, 1); }
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function lerp(a, b, t) { return a + (b - a) * t; }

  /* ---------- 1. reveals: mark sections "in" once ---------- */
  var reveals = document.querySelectorAll("[data-reveal], .hs-intro");
  reveals.forEach(function (sec) {
    sec.querySelectorAll(".ln").forEach(function (ln, i) {
      ln.firstElementChild.style.setProperty("--i", i);
    });
    var n = 0;
    sec.querySelectorAll(
      ".mark, .lede, .support-intro, .founder-copy p, .founder-copy .textlink, .close-sub, .hero-actions, .support-actions, figcaption"
    ).forEach(function (el) {
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
  }, { threshold: 0.18, rootMargin: "0px 0px -6% 0px" });
  reveals.forEach(function (s) { revealIO.observe(s); });
  /* Failsafe: never leave content hidden if the observer never fires */
  window.setTimeout(function () {
    reveals.forEach(function (s) { s.classList.add("in"); });
  }, 6000);

  /* Who pull quote: split into words that light up with scroll */
  var pull = document.querySelector(".who-pull[data-words]");
  var words = [];
  if (pull) {
    var text = pull.textContent.trim().split(/\s+/);
    pull.textContent = "";
    text.forEach(function (w, i) {
      var s = document.createElement("span");
      s.className = "w";
      s.textContent = w + (i < text.length - 1 ? " " : "");
      pull.appendChild(s);
      words.push(s);
    });
  }

  /* ---------- 2. the scroll engine ---------- */
  var scenes = [];
  function add(el, fn, mode) {
    if (!el) return;
    var s = { el: el, fn: fn, mode: mode || "pin", target: 0, cur: -1, on: false };
    scenes.push(s);
    sceneIO.observe(el);
  }
  var sceneIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      scenes.forEach(function (s) { if (s.el === e.target) s.on = e.isIntersecting; });
    });
    kick();
  }, { rootMargin: "25% 0px 25% 0px" });

  function measure(s) {
    var r = s.el.getBoundingClientRect();
    var vh = window.innerHeight;
    if (s.mode === "pin") {
      /* 0 when the section top hits the viewport top, 1 when its bottom meets the viewport bottom */
      return clamp(-r.top / Math.max(1, r.height - vh), 0, 1);
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
  window.addEventListener("resize", function () { layoutHS(); kick(); }, { passive: true });

  /* ---------- 3. stage: hero + position ---------- */
  var stage = document.getElementById("stage");
  if (stage) {
    var s1 = stage.querySelector(".scene-1"),
        s2 = stage.querySelector(".scene-2"),
        img1 = s1.querySelector(".scene-img"),
        img2 = s2.querySelector(".scene-img"),
        copy1 = s1.querySelector(".scene-copy"),
        ring = s2.querySelector(".ring"),
        mark2 = s2.querySelector(".mark"),
        lines2 = s2.querySelectorAll(".ln > span"),
        note2 = s2.querySelector(".scene-note");
    var desktop = window.matchMedia("(min-width:1024px)");

    /* load sequence */
    var img1el = img1.querySelector("img");
    function go() { stage.classList.add("loaded"); }
    if (img1el.complete) requestAnimationFrame(function () { requestAnimationFrame(go); });
    else { img1el.addEventListener("load", go); window.setTimeout(go, 1200); }

    add(stage, function (p) {
      /* scene 1: slow push in, copy lifts and fades as scene 2 arrives */
      var out1 = easeOut(seg(p, 0.12, 0.42));
      img1.style.transform = "scale(" + lerp(1, 1.12, seg(p, 0, 0.5)).toFixed(4) + ")";
      copy1.style.transform = "translate3d(0," + (-out1 * 90).toFixed(1) + "px,0)";
      copy1.style.opacity = (1 - out1).toFixed(3);
      /* a faded-out scene must not stay clickable or focusable under the next one */
      copy1.style.visibility = out1 >= 0.995 ? "hidden" : "visible";

      /* scene 2: cross-fades in out of focus, then sharpens */
      var in2 = seg(p, 0.3, 0.5);
      s2.style.opacity = easeOut(in2).toFixed(3);
      s2.style.visibility = in2 > 0 ? "visible" : "hidden";
      var focus = seg(p, 0.32, 0.6);
      img2.style.filter = "blur(" + ((1 - easeOut(focus)) * 22).toFixed(1) + "px)";
      img2.style.transform = "scale(" + lerp(1.18, 1.02, easeOut(seg(p, 0.3, 1))).toFixed(4) + ")";

      /* ring turns the whole way through and settles in */
      if (ring) {
        var r = lerp(-50, 40, p);
        var base = desktop.matches ? "translateY(-50%) " : "";
        ring.style.transform = base + "rotate(" + r.toFixed(2) + "deg) scale(" + lerp(0.86, 1, easeOut(seg(p, 0.35, 0.7))).toFixed(3) + ")";
        ring.style.opacity = easeOut(seg(p, 0.38, 0.6)).toFixed(3);
      }

      /* position statement: mark, then line by line, then the note */
      var m = easeOut(seg(p, 0.42, 0.52));
      mark2.style.opacity = m.toFixed(3);
      mark2.style.transform = "translate3d(0," + ((1 - m) * 20).toFixed(1) + "px,0)";
      lines2.forEach(function (ln, i) {
        var a = 0.46 + i * 0.035;
        var t = easeOut(seg(p, a, a + 0.12));
        ln.style.transform = "translate3d(0," + ((1 - t) * 105).toFixed(1) + "%,0)";
      });
      var n = easeOut(seg(p, 0.7, 0.8));
      note2.style.opacity = n.toFixed(3);
      note2.style.transform = "translate3d(0," + ((1 - n) * 16).toFixed(1) + "px,0)";
    });
  }

  /* ---------- 4. proof: horizontal track ---------- */
  var hs = document.getElementById("proof");
  var track = hs && hs.querySelector(".hs-track");
  var bar = hs && hs.querySelector(".hs-progress span");
  var hsMedia = hs ? hs.querySelectorAll(".hs-media img") : [];
  var counters = hs ? hs.querySelectorAll(".count") : [];
  var travel = 0;
  function layoutHS() {
    if (!track) return;
    travel = Math.max(0, track.scrollWidth - window.innerWidth);
    /* section height = the horizontal distance, plus one screen to read the last panel */
    hs.style.height = (travel * 0.8 + window.innerHeight) + "px";
  }
  if (track) {
    layoutHS();
    window.addEventListener("load", layoutHS);
    var counted = new WeakSet();
    add(hs, function (p) {
      track.style.transform = "translate3d(" + (-p * travel).toFixed(1) + "px,0,0)";
      if (bar) bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
      var vw = window.innerWidth;
      hsMedia.forEach(function (img) {
        var box = img.parentElement.getBoundingClientRect();
        /* -1 when the panel is off right, +1 off left: photo drifts against the track */
        var d = clamp((box.left + box.width / 2 - vw / 2) / vw, -1, 1);
        img.style.transform = "translate3d(" + (d * -7).toFixed(2) + "%,0,0)";
      });
      counters.forEach(function (c) {
        if (counted.has(c)) return;
        var box = c.getBoundingClientRect();
        if (box.left < vw * 0.85) { counted.add(c); countUp(c); }
      });
    });
  }
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

  /* ---------- 5. parallax drift on figures with data-speed ---------- */
  document.querySelectorAll("[data-speed]").forEach(function (el) {
    var speed = parseFloat(el.getAttribute("data-speed")) || 0;
    add(el, function (p) {
      var y = (p - 0.5) * speed * window.innerHeight;
      el.style.transform = "translate3d(0," + y.toFixed(1) + "px,0)";
    }, "view");
  });

  /* ---------- 6. who: words light up as the quote crosses the screen ---------- */
  if (pull && words.length) {
    add(pull, function (p) {
      var lit = Math.round(seg(p, 0.25, 0.6) * words.length);
      words.forEach(function (w, i) { w.classList.toggle("lit", i < lit); });
    }, "view");
  }

  /* ---------- 7. close: outline type travels, photo settles ---------- */
  var close = document.querySelector(".home .close");
  if (close) {
    var outline = close.querySelector(".close-logo");
    var cbg = close.querySelector(".close-bg img");
    add(close, function (p) {
      if (outline) outline.style.transform = "translate3d(" + lerp(4, -38, p).toFixed(2) + "%,0,0)";
      if (cbg) cbg.style.transform = "scale(" + lerp(1.2, 1, p).toFixed(4) + ")";
    }, "view");
  }

  kick();
})();
