document.addEventListener('DOMContentLoaded', () => {
  const heroVideos = document.querySelectorAll('.hero-video');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function startHeroRotation() {
    if (heroVideos.length <= 1 || reducedMotion) return;
    let activeIndex = Array.from(heroVideos).findIndex(v => v.classList.contains('is-active'));
    if (activeIndex === -1) activeIndex = 0;
    setInterval(() => {
      heroVideos[activeIndex].classList.remove('is-active');
      activeIndex = (activeIndex + 1) % heroVideos.length;
      heroVideos[activeIndex].classList.add('is-active');
    }, 2200);
  }

  // --- Intro splash: quick photo flash, then the logo drags into the exact
  // spot it sits at on the real page. CSS keyframes (.intro-splash /
  // .intro-logo without .js-driven) are the no-JS fallback — if this script
  // never runs, that simpler fade-only version still plays correctly and
  // still never blocks any content underneath (pointer-events: none throughout).
  const splash = document.querySelector('.intro-splash');
  const flashFrames = splash ? Array.from(splash.querySelectorAll('.intro-flash')) : [];
  const cloneLogo = splash ? splash.querySelector('.intro-logo') : null;
  const realLogo = document.querySelector('.hero-logo');

  if (splash && cloneLogo && realLogo && !reducedMotion) {
    splash.classList.add('js-driven');

    const FLASH_STEP_MS = 150;
    let flashIndex = 0;
    const flashTimer = setInterval(() => {
      flashFrames[flashIndex]?.classList.remove('is-active');
      flashIndex += 1;
      if (flashIndex >= flashFrames.length) {
        clearInterval(flashTimer);
        beginLogoReveal();
        return;
      }
      flashFrames[flashIndex].classList.add('is-active');
    }, FLASH_STEP_MS);

    function beginLogoReveal() {
      cloneLogo.style.transition = 'opacity 0.4s ease, transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
      cloneLogo.style.opacity = '1';
      cloneLogo.style.transform = 'scale(1)';
      setTimeout(dragLogoIntoPlace, 700);
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
        cloneLogo.style.transition = 'opacity 0.15s ease';
        cloneLogo.style.opacity = '0';
        setTimeout(() => {
          splash.remove();
          startHeroRotation();
        }, 150);
      }, 600);
    }
  } else {
    // No-JS-equivalent path (reduced motion, or missing elements): don't
    // wait on an intro that isn't playing.
    if (splash) splash.remove();
    startHeroRotation();
  }
});
