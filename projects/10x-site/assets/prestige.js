/* Shared behaviour: nav state, scroll progress, clamped parallax,
   staged reveals (motion is opt-in and never gates content), enquiry form. */
/* Swap in a real POST endpoint at deploy. While null, the form
     falls back to a mailto: compose so no enquiry is ever lost. */
  const FORM_ENDPOINT = null;
  const CONTACT_EMAIL = 'hello@10xvisuals.com.au';

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduced) document.documentElement.classList.add('anim');
  const nav = document.getElementById('mainNav');
  const progress = document.getElementById('scrollProgress');
  const parallax = [...document.querySelectorAll('[data-par]')].map(el => ({
    el, factor: parseFloat(el.dataset.par) || 0
  }));
  let ticking = false;

  function onScroll(){
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => {
      nav.classList.toggle('scrolled', scrollY > 60);
      const max = document.documentElement.scrollHeight - innerHeight;
      progress.style.transform = 'scaleX(' + (max > 0 ? Math.min(scrollY / max, 1) : 0) + ')';
      /* Parallax: transform only, and only while the frame is actually
         on screen, so offscreen sections cost nothing. */
      if (!reduced) for (const p of parallax) {
        const r = p.el.parentElement.getBoundingClientRect();
        if (r.bottom > 0 && r.top < innerHeight) {
          /* Clamp to the element's own overscan. Travel scales with
             viewport height, so an unclamped factor exposes the frame
             behind the image on tall viewports. */
          const slack = Math.max(0, (p.el.offsetHeight - p.el.parentElement.clientHeight) / 2);
          const raw = (r.top + r.height / 2 - innerHeight / 2) * -p.factor;
          const travel = Math.max(-slack, Math.min(slack, raw));
          p.el.style.transform = 'translateY(' + travel.toFixed(2) + 'px)';
        }
      }
      ticking = false;
    });
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Promote a parallax layer only while its section is near the viewport. */
  if (!reduced && 'IntersectionObserver' in window) {
    const liveIO = new IntersectionObserver(es => es.forEach(e => {
      e.target.classList.toggle('par-live', e.isIntersecting);
    }), { rootMargin: '200px 0px' });
    for (const p of parallax) liveIO.observe(p.el);
  }

  /* Reveals enhance an already-visible default. Content is never left
     depending on the observer: we only hide anything once we know the
     observer exists, we arm after the browser has settled any anchor
     scroll (a deep link like /#close used to leave a section blank),
     and a failsafe clears everything regardless after 2.5s. */
  function armReveals(){
    if (reduced || !('IntersectionObserver' in window)) return;

    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.remove('pending'); io.unobserve(e.target); }
    }), { threshold: 0.14, rootMargin: '0px 0px -6% 0px' });

    document.querySelectorAll('.reveal').forEach(el => {
      if (el.getBoundingClientRect().top > innerHeight * 1.05) {
        el.classList.add('pending');
        io.observe(el);
      }
    });

    setTimeout(() => {
      document.querySelectorAll('.reveal.pending').forEach(el => el.classList.remove('pending'));
    }, 2500);
  }
  requestAnimationFrame(() => requestAnimationFrame(armReveals));

  /* ---- Enquiry form ----
     Validation drives aria-invalid, which drives both the visual state and
     what assistive tech reports, so the two can never disagree. Each error
     paragraph is role="alert" and wired to its input via aria-describedby,
     so a failed submit is announced rather than only coloured. */
  const form = document.getElementById('enquiry');
  const fail = document.getElementById('formFail');
  const done = document.getElementById('formDone');
  const submitBtn = form.querySelector('button[type="submit"]');
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  const TIMEOUT_MS = 12000;

  const rules = {
    name:  v => v.length > 1,
    email: v => EMAIL_RE.test(v),
    phone: v => v.replace(/[^0-9]/g, '').length >= 8
  };

  function mark(input, ok){
    input.setAttribute('aria-invalid', ok ? 'false' : 'true');
    return ok;
  }

  /* Clear a field's error as soon as the user corrects it, rather than
     making them submit again to find out. */
  for (const name of Object.keys(rules)) {
    form[name].addEventListener('input', e => {
      if (e.target.getAttribute('aria-invalid') === 'true'
          && rules[name](e.target.value.trim())) {
        e.target.setAttribute('aria-invalid', 'false');
      }
    });
  }

  let sending = false;

  form.addEventListener('submit', e => {
    e.preventDefault();
    if (sending) return;                 /* no double posts */
    fail.style.display = 'none';

    const values = {};
    let firstBad = null;
    for (const name of Object.keys(rules)) {
      const input = form[name];
      values[name] = input.value.trim();
      if (!mark(input, rules[name](values[name])) && !firstBad) firstBad = input;
    }
    if (firstBad) { firstBad.focus(); return; }

    const succeed = () => {
      form.classList.add('sent');
      sending = false;
      /* Move focus to the confirmation so it is announced and so keyboard
         focus is not left on a button that no longer exists visually. */
      done.focus();
    };
    const stop = () => {
      sending = false;
      submitBtn.removeAttribute('aria-busy');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Send enquiry';
    };

    sending = true;
    submitBtn.setAttribute('aria-busy', 'true');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending';

    if (!FORM_ENDPOINT) {
      /* mailto: compose only. Never a query string, so personal details
         never end up in a URL. */
      const body = 'Name: ' + values.name
                 + '\nEmail: ' + values.email
                 + '\nPhone: ' + values.phone;
      location.href = 'mailto:' + CONTACT_EMAIL
        + '?subject=' + encodeURIComponent('Website enquiry')
        + '&body=' + encodeURIComponent(body);
      succeed();
      return;
    }

    /* Abort a hung request rather than leaving the button dead forever. */
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);

    fetch(FORM_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(values),
      signal: ctrl.signal
    }).then(r => {
      if (!r.ok) throw new Error(r.status);
      succeed();
    }).catch(() => {
      stop();
      fail.style.display = 'block';
    }).finally(() => clearTimeout(timer));
  });

  /* ---------- Menu overlay ----------
     Full-bleed panel, not a dropdown, so it needs its own focus and
     scroll-lock handling rather than piggybacking on the desktop nav. */
  const menuToggle = document.getElementById('menuToggle');
  const menuOverlay = document.getElementById('menuOverlay');
  const menuClose = document.getElementById('menuClose');

  if (menuToggle && menuOverlay) {
    const focusables = () => [...menuOverlay.querySelectorAll('a, button')];

    function openMenu(){
      menuOverlay.classList.add('open');
      menuOverlay.setAttribute('aria-hidden', 'false');
      menuToggle.setAttribute('aria-expanded', 'true');
      document.body.classList.add('menu-open');
      const first = focusables()[0];
      if (first) first.focus();
      document.addEventListener('keydown', onKey);
    }
    function closeMenu(){
      menuOverlay.classList.remove('open');
      menuOverlay.setAttribute('aria-hidden', 'true');
      menuToggle.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('menu-open');
      menuToggle.focus();
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e){
      if (e.key === 'Escape') { e.preventDefault(); closeMenu(); return; }
      /* Manual focus trap: Tab past either end wraps, rather than
         escaping into the hidden page behind the overlay. */
      if (e.key !== 'Tab') return;
      const items = focusables();
      if (!items.length) return;
      const first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }

    menuToggle.addEventListener('click', openMenu);
    if (menuClose) menuClose.addEventListener('click', closeMenu);
  }

  /* ---------- Hero scroll cue ---------- */
  const heroEl = document.getElementById('top');
  if (heroEl) {
    const cueIO = new IntersectionObserver(es => es.forEach(e => {
      heroEl.classList.toggle('scrolled-past', e.intersectionRatio < 0.94);
    }), { threshold: [0, .94, 1] });
    cueIO.observe(heroEl);
  }

  /* ---------- Magnetic CTAs ----------
     A restrained, functional cousin of a drag toy: the two decision-moment
     buttons pull toward the pointer within a small radius. Fine pointers
     only (a touchscreen has no hover to feel this), and off entirely under
     reduced motion. Capped displacement, and the CSS transition on
     .magnetic handles the snap-back, so there is no animation loop here. */
  if (!reduced && matchMedia('(pointer: fine)').matches) {
    const MAX_PULL = 10;
    document.querySelectorAll('.magnetic').forEach(el => {
      el.addEventListener('mousemove', e => {
        const r = el.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width - 0.5) * 2;
        const y = ((e.clientY - r.top) / r.height - 0.5) * 2;
        el.style.transform = `translate(${(x * MAX_PULL).toFixed(1)}px, ${(y * MAX_PULL).toFixed(1)}px)`;
      });
      el.addEventListener('mouseleave', () => { el.style.transform = ''; });
    });
  }
