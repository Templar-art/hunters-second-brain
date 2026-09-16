document.addEventListener('DOMContentLoaded', () => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // The hero is a single fixed still now, not a 4-clip rotation, so there's
  // nothing left to rotate or lazily prime here. See .hero-bg in style.css.

  // --- Intro splash: quick photo flash, then the logo drags into the exact
  // spot it sits at on the real page. CSS keyframes (.intro-splash /
  // .intro-logo without .js-driven) are the no-JS fallback — if this script
  // never runs, that simpler fade-only version still plays correctly and
  // still never blocks any content underneath (pointer-events: none throughout).
  // Plays once per browser session, not once per page. Without this, every
  // one of the site's 7 pages replays the full ~2.3s flash-and-logo-drag
  // sequence on every click between them. A new tab (fresh sessionStorage)
  // sees it again, same as a first visit should.
  let introAlreadyPlayed = true;
  try {
    introAlreadyPlayed = sessionStorage.getItem('isl-intro-played') === '1';
  } catch (err) {
    // sessionStorage can throw (privacy settings, sandboxed iframes, some
    // enterprise policies). The intro is decorative — fail toward NOT
    // showing it rather than let this abort the rest of the callback below
    // (nav toggle, scroll reveal, form submit all depend on it continuing).
    introAlreadyPlayed = true;
  }
  const splash = document.querySelector('.intro-splash');
  const flashFrames = splash ? Array.from(splash.querySelectorAll('.intro-flash')) : [];
  const flashStack = splash ? splash.querySelector('.intro-flash-stack') : null;
  const caption = splash ? splash.querySelector('.intro-caption') : null;
  const cloneLogo = splash ? splash.querySelector('.intro-logo') : null;
  const whiteFlash = splash ? splash.querySelector('.intro-whiteflash') : null;
  const realLogo = document.querySelector('.hero-logo');

  // Claim the splash synchronously, before waiting on fonts or images. The
  // CSS fallback (for when this script never runs) starts fading the logo in
  // shortly after paint, and .js-driven is what cancels it. Leaving that
  // until the gate below resolves means that on a cold first load the
  // fallback plays first: logo appears, vanishes, photo sequence runs, logo
  // returns. A warm reload hid it because the gate resolved instantly.
  // Only the sequence waits for the gate, never the claim.
  if (splash && !reducedMotion) splash.classList.add('js-driven');

  if (splash && cloneLogo && whiteFlash && realLogo && !reducedMotion && !introAlreadyPlayed) {
    // Wait for the web font to finish loading before doing anything that
    // measures layout. TASA Orbiter swaps in async (Google Fonts) — if it
    // lands mid-intro, the real logo's text above/around it reflows and
    // the position we measured earlier goes stale, so the dragged clone
    // lands slightly off from the real logo and visibly flickers/jumps at
    // the crossfade. Gating the whole sequence on fonts.ready means layout
    // is already final by the time we ever call getBoundingClientRect().
    const fontsReady = document.fonts && document.fonts.ready
      ? document.fonts.ready
      : Promise.resolve();
    fontsReady.then(runIntro).catch(runIntro);
  } else {
    // No-JS-equivalent path (reduced motion, or missing elements): don't
    // wait on an intro that isn't playing.
    if (splash) splash.remove();
  }

  function runIntro() {
    splash.classList.add('js-driven');
    try {
      sessionStorage.setItem('isl-intro-played', '1');
    } catch (err) {
      // No-op: if we can't persist the flag, the intro may replay on the
      // next page, but that's cosmetic and must never block this function.
    }

    // Hide the real logo only for the duration of this same animation —
    // otherwise it's visible underneath the clone the whole time, which
    // reads as two logos instead of one dragging into place. A hard
    // timeout below guarantees it's restored even if something above throws.
    realLogo.style.opacity = '0';
    const restoreRealLogoSafety = setTimeout(() => { realLogo.style.opacity = '1'; }, 5000);

    // "Coming soon" overlays the photo flashes from the very first frame.
    if (caption) caption.classList.add('is-visible');

    const PHOTO_STEP_MS = 70;
    let flashIndex = 0;
    function advanceFlash() {
      flashFrames[flashIndex]?.classList.remove('is-active');
      flashIndex += 1;
      if (flashIndex >= flashFrames.length) {
        popWhiteFlash();
        return;
      }
      flashFrames[flashIndex].classList.add('is-active');
      setTimeout(advanceFlash, PHOTO_STEP_MS);
    }
    setTimeout(advanceFlash, PHOTO_STEP_MS);

    function popWhiteFlash() {
      // Kill the image flash instantly, pop to solid white instantly, and
      // spawn the logo underneath the white veil in the same tick — since
      // the veil sits on top at full opacity, the logo is completely hidden
      // ("on the white but you shouldn't see it"), not just color-matched.
      flashStack.style.opacity = '0';
      if (caption) caption.classList.remove('is-visible');
      whiteFlash.style.transition = 'none';
      whiteFlash.style.opacity = '1';
      cloneLogo.style.transition = 'none';
      cloneLogo.style.opacity = '1';
      cloneLogo.style.transform = 'scale(1)';

      // Hold the flash for a beat, then let it recede — the logo becomes
      // visible purely because the white veil in front of it fades away,
      // revealing it against the splash's black backdrop underneath.
      setTimeout(() => {
        whiteFlash.style.transition = 'opacity 0.45s ease-out';
        whiteFlash.style.opacity = '0';
      }, 120);

      // Hold on black once the logo's revealed, so it has time to register
      // before the page underneath takes over (trimmed 35% per feedback,
      // the original 1300ms felt like a stall rather than a beat).
      setTimeout(dragLogoIntoPlace, 120 + 450 + 845);
    }

    function dragLogoIntoPlace() {
      const from = cloneLogo.getBoundingClientRect();
      const to = realLogo.getBoundingClientRect();
      const scale = to.width / from.width;
      const dx = (to.left + to.width / 2) - (from.left + from.width / 2);
      const dy = (to.top + to.height / 2) - (from.top + from.height / 2);

      // Only the backdrop dissolves here — the logo itself stays fully
      // opaque through the drag so the motion actually reads.
      splash.style.transition = 'background-color 0.6s ease';
      splash.style.backgroundColor = 'transparent';
      cloneLogo.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
      cloneLogo.style.transform = `translate(${dx}px, ${dy}px) scale(${scale})`;

      setTimeout(() => {
        // Reveal the real logo and fade the clone out at the same moment —
        // a seamless crossfade between two identical, identically-placed images.
        clearTimeout(restoreRealLogoSafety);
        realLogo.style.transition = 'opacity 0.15s ease';
        realLogo.style.opacity = '1';
        cloneLogo.style.transition = 'opacity 0.15s ease';
        cloneLogo.style.opacity = '0';
        setTimeout(() => {
          splash.remove();
        }, 150);
      }, 600);
    }
  }

  // --- Scroll reveal: sections animate in as they enter view. The reveal
  // class is only ever added here, at runtime, right before observing —
  // so if JS never runs (disabled, crawler, headless render), every
  // [data-reveal] element stays at its default, fully-visible CSS state.
  // Never gate visibility on the class itself.
  if (!reducedMotion && 'IntersectionObserver' in window) {
    const revealEls = document.querySelectorAll('[data-reveal]');
    revealEls.forEach((el) => el.classList.add('reveal-pending'));
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -60px 0px' }
    );
    revealEls.forEach((el) => io.observe(el));
  }

  // --- Nav: mobile menu toggle. The button only renders below 860px
  // (see .nav-toggle in style.css), so there's no matchMedia guard here —
  // a desktop click can never reach it.
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
      navToggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });
    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Open menu');
      });
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navLinks.classList.contains('is-open')) {
        navLinks.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Open menu');
      }
    });
  }

  // --- Forms: POST to a hidden iframe so the page never navigates away,
  // then swap the form for a success message once the iframe finishes
  // loading (which happens right after the Apps Script backend responds).
  // This works without a fetch() call and without a CORS-enabled endpoint
  // — Apps Script Web Apps don't return CORS headers for cross-origin
  // fetch(), but a classic form POST with a hidden iframe target doesn't
  // need them, since the page never reads the response body. See the
  // <noscript> next to each form for what a non-JS visitor sees instead:
  // the submission still succeeds (the browser POSTs regardless of JS),
  // they just don't get the friendly on-page confirmation.
  document.querySelectorAll('form[data-form-name]').forEach((form) => {
    const targetName = form.getAttribute('target');
    const iframe = targetName ? document.querySelector(`iframe[name="${targetName}"]`) : null;
    const panel = form.closest('.form-panel');
    if (!iframe || !panel) return;
    let submitted = false;
    form.addEventListener('submit', () => { submitted = true; });
    iframe.addEventListener('load', () => {
      // The iframe's own initial blank load also fires 'load' — ignore it,
      // only react once an actual form submission has happened.
      if (!submitted) return;
      panel.classList.add('is-submitted');
    });
  });
});
