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
});
