document.addEventListener('DOMContentLoaded', () => {
  // The load-in logo moment lives entirely in CSS now (.intro-splash /
  // .intro-logo keyframes) so it still plays correctly even if this script
  // never runs — it was never gating any content, just an overlay on top.

  // The waitlist form itself posts straight to Brevo's hosted Forms endpoint
  // (see the form's action/hidden fields in index.html and README.md) — it
  // needs no JavaScript submit handler, and deliberately has none, so no
  // Brevo credential ever has to live in this file.

  // Hero video rotation. The first clip is marked is-active directly in the
  // HTML, so it shows correctly even if this script never runs — this only
  // adds the rotation through the rest of the reel on top of that.
  const heroVideos = document.querySelectorAll('.hero-video');
  if (heroVideos.length > 1 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let activeIndex = Array.from(heroVideos).findIndex(v => v.classList.contains('is-active'));
    if (activeIndex === -1) activeIndex = 0;
    setInterval(() => {
      heroVideos[activeIndex].classList.remove('is-active');
      activeIndex = (activeIndex + 1) % heroVideos.length;
      heroVideos[activeIndex].classList.add('is-active');
    }, 2200);
  }
});
