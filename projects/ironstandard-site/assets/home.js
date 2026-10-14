/* ============================================================
   IRON STANDARD - HOMEPAGE MOTION
   Loaded on index.html only, after motion.js, which provides the
   shared engine (window.ISM) and every shared effect: reveals,
   wipes, parallax, lit words, the closing band.

   This file adds only what is unique to the homepage: the pinned
   stage (hero + position). The horizontal proof uses the shared
   .hs track in motion.js.
   ============================================================ */
(function () {
  "use strict";
  var M = window.ISM;
  if (!M) return;   /* motion is off (reduced motion or no observer): static page */
  var seg = M.seg, easeOut = M.easeOut, lerp = M.lerp;

  /* ---------- stage: hero + position ---------- */
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

    M.add(stage, function (p) {
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

})();
