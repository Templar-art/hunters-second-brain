document.addEventListener('DOMContentLoaded', () => {
  const heroVideos = document.querySelectorAll('.hero-video');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Assigns a deferred video's real source and starts it loading/playing.
  // Videos beyond the first ship with no <source> and preload="none", so
  // the browser doesn't download and decode all 4 clips on page load
  // regardless of whether they're ever seen — only the one currently on
  // screen, plus whichever one is coming up next, are ever fetched.
  function primeHeroVideo(video) {
    if (!video || video.dataset.primed) return;
    const src = video.dataset.src;
    if (!src) return; // the first video already has a real <source>
    video.dataset.primed = 'true';
    video.preload = 'auto';
    video.src = src;
    video.play().catch(() => {});
  }

  function startHeroRotation() {
    if (heroVideos.length <= 1 || reducedMotion) return;
    let activeIndex = Array.from(heroVideos).findIndex(v => v.classList.contains('is-active'));
    if (activeIndex === -1) activeIndex = 0;
    // Give the next clip a full rotation cycle (2.2s) to buffer before it's
    // due on screen, rather than waiting until the moment it needs to show.
    primeHeroVideo(heroVideos[(activeIndex + 1) % heroVideos.length]);
    setInterval(() => {
      heroVideos[activeIndex].classList.remove('is-active');
      activeIndex = (activeIndex + 1) % heroVideos.length;
      heroVideos[activeIndex].classList.add('is-active');
      primeHeroVideo(heroVideos[(activeIndex + 1) % heroVideos.length]);
    }, 2200);
  }

  // --- Intro splash: quick photo flash, then the logo drags into the exact
  // spot it sits at on the real page. CSS keyframes (.intro-splash /
  // .intro-logo without .js-driven) are the no-JS fallback — if this script
  // never runs, that simpler fade-only version still plays correctly and
  // still never blocks any content underneath (pointer-events: none throughout).
  const splash = document.querySelector('.intro-splash');
  const flashFrames = splash ? Array.from(splash.querySelectorAll('.intro-flash')) : [];
  const flashStack = splash ? splash.querySelector('.intro-flash-stack') : null;
  const caption = splash ? splash.querySelector('.intro-caption') : null;
  const cloneLogo = splash ? splash.querySelector('.intro-logo') : null;
  const whiteFlash = splash ? splash.querySelector('.intro-whiteflash') : null;
  const realLogo = document.querySelector('.hero-logo');

  if (splash && cloneLogo && whiteFlash && realLogo && !reducedMotion) {
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
    startHeroRotation();
  }

  function runIntro() {
    splash.classList.add('js-driven');

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

      // Hold on black a good while once the logo's revealed, so it has
      // time to actually register before the page underneath takes over.
      setTimeout(dragLogoIntoPlace, 120 + 450 + 1300);
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
          startHeroRotation();
        }, 150);
      }, 600);
    }
  }
});
