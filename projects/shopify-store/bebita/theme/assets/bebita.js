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

// Menu drawer: native <dialog> gives focus trapping and Escape for free.
(() => {
  const dlg = document.querySelector('[data-bb-menu]');
  const open = document.querySelector('[data-bb-menu-open]');
  if (!dlg || !open) return;
  open.addEventListener('click', () => { dlg.showModal(); open.setAttribute('aria-expanded', 'true'); });
  dlg.querySelector('[data-bb-menu-close]').addEventListener('click', () => dlg.close());
  dlg.addEventListener('close', () => { open.setAttribute('aria-expanded', 'false'); open.focus(); });
  dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
})();

// Welcome pop-up: opens once per visitor after a short delay or halfway down the page, and again
// straight away after a sign-up (to show the code) or a failed one (to show the error).
(() => {
  const dlg = document.querySelector('[data-bb-popup]');
  if (!dlg || typeof dlg.showModal !== 'function') return;
  const KEY = 'bb-popup-seen';
  const days = Number(dlg.dataset.days || 14);
  const store = {
    get() { try { return Number(localStorage.getItem(KEY) || 0); } catch (e) { return 0; } },
    set() { try { localStorage.setItem(KEY, String(Date.now())); } catch (e) { /* private mode: show again next visit */ } },
  };
  const open = () => { if (!dlg.open && !document.querySelector('dialog[open]')) { dlg.showModal(); store.set(); } };
  dlg.querySelectorAll('[data-bb-popup-close]').forEach((b) => b.addEventListener('click', () => dlg.close()));
  dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });

  const state = dlg.querySelector('[data-bb-popup-state]');
  if (state || /customer_posted=true/.test(location.search)) { open(); return; }
  if (Date.now() - store.get() < days * 864e5) return;

  let armed = true;
  const fire = () => { if (!armed) return; armed = false; window.removeEventListener('scroll', onScroll); open(); };
  const onScroll = () => { if (window.scrollY > document.documentElement.scrollHeight * 0.45) fire(); };
  window.addEventListener('scroll', onScroll, { passive: true });
  setTimeout(fire, Number(dlg.dataset.delay || 7) * 1000);
  document.addEventListener('mouseout', (e) => { if (!e.relatedTarget && e.clientY <= 0) fire(); });
})();
