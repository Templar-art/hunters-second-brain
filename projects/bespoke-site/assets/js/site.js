/* ==========================================================================
   BESPOKE ESTATE AGENTS — site.js
   Injects shared partials, then wires header, menu, reveal, and lightbox.
   Runtime-only include system: each page carries empty [data-include] slots;
   this fetches partials/<name>.html and drops them in. Edit a partial once,
   every page updates. Requires the site be *served* (http), not opened from disk.
   ========================================================================== */

(function () {
  'use strict';

  // Resolve partials relative to site root regardless of page depth.
  // Pages live at root, so partials/ is a sibling. Detail pages in subfolders
  // set <body data-root=".."> to reach back up.
  var ROOT = document.body.getAttribute('data-root') || '.';

  function injectPartials() {
    var slots = Array.prototype.slice.call(document.querySelectorAll('[data-include]'));
    return Promise.all(slots.map(function (slot) {
      var name = slot.getAttribute('data-include');
      return fetch(ROOT + '/partials/' + name + '.html')
        .then(function (r) { if (!r.ok) throw new Error(name + ' ' + r.status); return r.text(); })
        .then(function (html) { slot.outerHTML = html; })
        .catch(function (err) { console.error('[partial]', err); });
    }));
  }

  /* ---- Header: solid background once scrolled past the hero threshold ---- */
  function initHeader() {
    var header = document.querySelector('.site-header');
    if (!header) return;
    // Interior pages (no full-bleed hero) start solid immediately.
    var hasHero = !!document.querySelector('.hero');
    function onScroll() {
      var solid = window.scrollY > (hasHero ? window.innerHeight * 0.7 : 10);
      header.classList.toggle('scrolled', solid);
    }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Slide-over menu ---- */
  function initMenu() {
    var toggle = document.querySelector('.menu-toggle');
    var menu = document.querySelector('.site-menu');
    if (!toggle || !menu) return;
    function setOpen(open) {
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    }
    toggle.addEventListener('click', function () {
      setOpen(!document.body.classList.contains('menu-open'));
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  /* ---- Mark the current nav link ---- */
  function markCurrent() {
    var here = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('[data-nav] a, .nav-desktop a').forEach(function (a) {
      var href = (a.getAttribute('href') || '').split('/').pop();
      if (href === here || (here === 'index.html' && (href === '' || href === 'index.html'))) {
        a.setAttribute('aria-current', 'page');
      }
    });
  }

  /* ---- Scroll reveal ---- */
  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window) || !els.length) {
      els.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---- Gallery lightbox ---- */
  function initLightbox() {
    var imgs = Array.prototype.slice.call(document.querySelectorAll('.gallery img'));
    if (!imgs.length) return;
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.innerHTML =
      '<button class="lightbox__close" aria-label="Close">&times;</button>' +
      '<button class="lightbox__nav prev" aria-label="Previous">&#8249;</button>' +
      '<img alt="">' +
      '<button class="lightbox__nav next" aria-label="Next">&#8250;</button>';
    document.body.appendChild(box);
    var big = box.querySelector('img');
    var i = 0;
    function show(n) { i = (n + imgs.length) % imgs.length; big.src = imgs[i].src; big.alt = imgs[i].alt; }
    function open(n) { show(n); box.classList.add('open'); document.body.style.overflow = 'hidden'; }
    function close() { box.classList.remove('open'); document.body.style.overflow = ''; }
    imgs.forEach(function (im, n) { im.addEventListener('click', function () { open(n); }); });
    box.querySelector('.lightbox__close').addEventListener('click', close);
    box.querySelector('.next').addEventListener('click', function (e) { e.stopPropagation(); show(i + 1); });
    box.querySelector('.prev').addEventListener('click', function (e) { e.stopPropagation(); show(i - 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(i + 1);
      if (e.key === 'ArrowLeft') show(i - 1);
    });
  }

  /* ---- Contact form (front-end only; no backend wired) ---- */
  function initForm() {
    var form = document.querySelector('form[data-contact]');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('[data-form-note]');
      if (note) { note.hidden = false; }
      form.querySelectorAll('input,textarea,select,button').forEach(function (el) { el.disabled = true; });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    injectPartials().then(function () {
      initHeader();
      initMenu();
      markCurrent();
      initReveal();
      initLightbox();
      initForm();
      var y = document.querySelector('[data-year]');
      if (y) y.textContent = String(new Date().getFullYear());
    });
  });
})();
