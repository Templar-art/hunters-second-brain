/* Bespoke Estate Agents — theme interactions.
   Header/footer/menu are server-rendered by PHP, so no partial injection here. */
(function () {
  'use strict';

  function initPreloader() {
    var pre = document.getElementById('preloader');
    if (!pre) return;
    var seen = false;
    try { seen = !!sessionStorage.getItem('beaSeen'); } catch (e) {}
    if (seen) { pre.remove(); return; }
    document.body.classList.add('preloading');
    var vid = pre.querySelector('video');
    var done = false;
    function dismiss() {
      if (done) return; done = true;
      try { sessionStorage.setItem('beaSeen', '1'); } catch (e) {}
      pre.classList.add('done');
      document.body.classList.remove('preloading');
      setTimeout(function () { if (pre.parentNode) pre.remove(); }, 950);
    }
    if (vid) {
      vid.addEventListener('ended', dismiss);
      vid.addEventListener('error', dismiss);
      var p = vid.play && vid.play();
      if (p && p.catch) p.catch(dismiss);
    }
    setTimeout(dismiss, 5600);
  }

  function initHeader() {
    var header = document.querySelector('.site-header');
    if (!header) return;
    var hasHero = !!document.querySelector('.hero');
    function onScroll() {
      header.classList.toggle('scrolled', window.scrollY > (hasHero ? window.innerHeight * 0.7 : 10));
    }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  function initMenu() {
    var toggle = document.querySelector('.menu-toggle');
    var menu = document.querySelector('.site-menu');
    if (!toggle || !menu) return;
    function setOpen(open) {
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    }
    toggle.addEventListener('click', function () { setOpen(!document.body.classList.contains('menu-open')); });
    menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  }

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

  function initLightbox() {
    var imgs = Array.prototype.slice.call(document.querySelectorAll('.gallery img'));
    if (!imgs.length) return;
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.innerHTML = '<button class="lightbox__close" aria-label="Close">&times;</button>' +
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

  function initForm() {
    var form = document.querySelector('form[data-contact]');
    if (!form) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('[data-form-note]');
      if (note) note.hidden = false;
      form.querySelectorAll('input,textarea,select,button').forEach(function (el) { el.disabled = true; });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initPreloader();
    initHeader();
    initMenu();
    initReveal();
    initLightbox();
    initForm();
  });
})();
