document.addEventListener('DOMContentLoaded', () => {
  // Content is already visible in the DOM without this script running —
  // this only adds a fade/rise polish on top. Never gate content on it.
  const heroLogo = document.querySelector('.hero-logo');
  if (heroLogo) {
    requestAnimationFrame(() => {
      setTimeout(() => heroLogo.classList.add('is-visible'), 150);
    });
  }

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
    }, 6000);
  }
});
