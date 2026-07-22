/* Bespoke — showcase.js
   Cinematic scroll layer: Lenis smooth scroll + GSAP ScrollTrigger.
   Degrades cleanly: no JS = static readable page; reduced-motion = no smooth/parallax/pin. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGSAP = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';

  /* ---------- Preloader (once per session) ---------- */
  function preloader() {
    var pre = document.getElementById('preloader');
    if (!pre) return;
    var seen = false; try { seen = !!sessionStorage.getItem('beaSeen'); } catch (e) {}
    if (seen || reduce) { pre.remove(); return; }
    document.body.classList.add('preloading');
    var vid = pre.querySelector('video'), done = false;
    function dismiss() {
      if (done) return; done = true;
      try { sessionStorage.setItem('beaSeen', '1'); } catch (e) {}
      pre.classList.add('done'); document.body.classList.remove('preloading');
      setTimeout(function () { pre.remove(); if (window.ScrollTrigger) ScrollTrigger.refresh(); }, 950);
    }
    if (vid) { vid.addEventListener('ended', dismiss); vid.addEventListener('error', dismiss);
      var p = vid.play && vid.play(); if (p && p.catch) p.catch(dismiss); }
    setTimeout(dismiss, 5600);
  }

  /* ---------- Header + menu ---------- */
  function chrome() {
    var header = document.querySelector('.site-header');
    if (header) {
      var hasHero = !!document.querySelector('.lux-hero, .hero');
      var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > (hasHero ? window.innerHeight * 0.7 : 10)); };
      onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
    }
    var toggle = document.querySelector('.menu-toggle'), menu = document.querySelector('.site-menu');
    if (toggle && menu) {
      var setOpen = function (o) {
        document.body.classList.toggle('menu-open', o);
        toggle.setAttribute('aria-expanded', String(o));
        if (window.lenis) { o ? window.lenis.stop() : window.lenis.start(); }
        else document.body.style.overflow = o ? 'hidden' : '';
      };
      toggle.addEventListener('click', function () { setOpen(!document.body.classList.contains('menu-open')); });
      menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') setOpen(false); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
    }
    var y = document.querySelector('[data-year]'); if (y) y.textContent = String(new Date().getFullYear());
  }

  /* ---------- Dropdown galleries ---------- */
  function dropdowns() {
    document.querySelectorAll('.drop-toggle').forEach(function (btn) {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      if (!panel) return;
      btn.addEventListener('click', function () {
        var open = panel.getAttribute('data-open') === 'true';
        panel.setAttribute('data-open', String(!open));
        btn.setAttribute('aria-expanded', String(!open));
        btn.querySelector('[data-label]').textContent = !open ? 'Hide gallery' : 'View the gallery';
        // let the height transition run, then recalc scroll positions
        setTimeout(function () { if (window.ScrollTrigger) ScrollTrigger.refresh(); if (window.lenis) window.lenis.resize(); }, 650);
      });
    });
  }

  /* ---------- Lightbox ---------- */
  function lightbox() {
    var imgs = Array.prototype.slice.call(document.querySelectorAll('.gallery img'));
    if (!imgs.length) return;
    var box = document.createElement('div'); box.className = 'lightbox';
    box.innerHTML = '<button class="lightbox__close" aria-label="Close">&times;</button>' +
      '<button class="lightbox__nav prev" aria-label="Previous">&#8249;</button><img alt="">' +
      '<button class="lightbox__nav next" aria-label="Next">&#8250;</button>';
    document.body.appendChild(box);
    var big = box.querySelector('img'), i = 0;
    function show(n) { i = (n + imgs.length) % imgs.length; big.src = imgs[i].src; big.alt = imgs[i].alt; }
    function open(n) { show(n); box.classList.add('open'); if (window.lenis) window.lenis.stop(); else document.body.style.overflow = 'hidden'; }
    function close() { box.classList.remove('open'); if (window.lenis) window.lenis.start(); else document.body.style.overflow = ''; }
    imgs.forEach(function (im, n) { im.addEventListener('click', function () { open(n); }); });
    box.querySelector('.lightbox__close').addEventListener('click', close);
    box.querySelector('.next').addEventListener('click', function (e) { e.stopPropagation(); show(i + 1); });
    box.querySelector('.prev').addEventListener('click', function (e) { e.stopPropagation(); show(i - 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') show(i + 1); if (e.key === 'ArrowLeft') show(i - 1);
    });
  }

  /* ---------- Reduced-motion / no-GSAP fallback: reveal everything ---------- */
  function revealAllStatic() {
    document.querySelectorAll('.r-up, .r-fade, .r-clip').forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- Motion (Lenis + GSAP) ---------- */
  function motion() {
    gsap.registerPlugin(ScrollTrigger);
    // Lenis smooth scroll
    var lenis = new Lenis({ duration: 1.1, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, smoothWheel: true });
    window.lenis = lenis;
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);

    // Anchor links -> smooth scroll via Lenis
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href'); if (id.length < 2) return;
        var t = document.querySelector(id); if (!t) return;
        e.preventDefault(); document.body.classList.remove('menu-open');
        lenis.scrollTo(t, { offset: -10, duration: 1.3 });
      });
    });

    // Reveals
    gsap.utils.toArray('.r-up, .r-fade, .r-clip').forEach(function (el) {
      ScrollTrigger.create({ trigger: el, start: 'top 85%', once: true, onEnter: function () { el.classList.add('is-in'); } });
    });

    // Hero slow zoom + drift
    var heroMedia = document.querySelector('.lux-hero__media');
    if (heroMedia) {
      gsap.fromTo(heroMedia, { scale: 1.08, yPercent: -4 }, {
        scale: 1.16, yPercent: 6, ease: 'none',
        scrollTrigger: { trigger: '.lux-hero', start: 'top top', end: 'bottom top', scrub: true }
      });
    }

    // Parallax on estate figures + enquiry bg
    gsap.utils.toArray('.estate__fig img, .enquire__bg').forEach(function (img) {
      gsap.fromTo(img, { yPercent: -6 }, { yPercent: 6, ease: 'none',
        scrollTrigger: { trigger: img.closest('section') || img, start: 'top bottom', end: 'bottom top', scrub: true } });
    });

    // Featured pinned crossfade (desktop only)
    var mm = gsap.matchMedia();
    mm.add('(min-width: 900px)', function () {
      var featured = document.querySelector('.featured'); if (!featured) return;
      var stage = featured.querySelector('.featured__stage');
      var layers = featured.querySelectorAll('.featured__layer');
      var countEl = featured.querySelector('[data-count]');
      var titleEl = featured.querySelector('[data-title]');
      var nameEl = featured.querySelector('[data-name]');
      var data = JSON.parse(featured.getAttribute('data-estates') || '[]');
      var n = layers.length;
      var tl = gsap.timeline({ scrollTrigger: { trigger: featured, start: 'top top', end: '+=' + (n * 90) + '%', pin: stage, scrub: 0.5,
        onUpdate: function (self) {
          var idx = Math.min(n - 1, Math.floor(self.progress * n + 0.0001));
          if (data[idx] && titleEl && titleEl.textContent !== data[idx].title) {
            countEl.textContent = data[idx].count; titleEl.textContent = data[idx].title; nameEl.textContent = data[idx].name;
          }
        } } });
      for (var i = 1; i < n; i++) { tl.to(layers[i], { opacity: 1, duration: 1, ease: 'power1.inOut' }, i - 0.5); }
    });

    ScrollTrigger.refresh();
  }

  document.addEventListener('DOMContentLoaded', function () {
    preloader(); chrome(); dropdowns(); lightbox();
    if (reduce || !hasGSAP) { revealAllStatic(); return; }
    document.documentElement.classList.add('lenis');
    motion();
  });
})();
