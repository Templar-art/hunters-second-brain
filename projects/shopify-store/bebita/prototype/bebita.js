// Reveal each marked block once as it enters the viewport. Content is visible without JS.
(() => {
  const els = document.querySelectorAll('[data-reveal]');
  if (!('IntersectionObserver' in window) || !els.length) return;
  document.documentElement.classList.add('bb-js');
  document.body.classList.add('bb-js');
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -8% 0px' });
  els.forEach((el) => io.observe(el));
})();
