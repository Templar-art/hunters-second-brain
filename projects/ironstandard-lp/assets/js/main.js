document.addEventListener('DOMContentLoaded', () => {
  // Content is already visible in the DOM without this script running —
  // this only adds a fade/rise polish on top. Never gate content on it.
  const heroLogo = document.querySelector('.hero-logo');
  if (heroLogo) {
    requestAnimationFrame(() => {
      setTimeout(() => heroLogo.classList.add('is-visible'), 150);
    });
  }

  // --- Waitlist form -> Brevo ---
  // Replace IRONSTANDARD_BREVO_URL with the real Brevo "Create contact" REST
  // endpoint + list ID once the Brevo account exists (see README.md).
  const IRONSTANDARD_BREVO_URL = 'REPLACE_WITH_BREVO_ENDPOINT';

  const waitlistForm = document.getElementById('waitlist-form');
  if (waitlistForm) {
    waitlistForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const status = document.getElementById('waitlist-status');
      const name = document.getElementById('wl-name').value.trim();
      const email = document.getElementById('wl-email').value.trim();

      if (!name || !email) {
        status.textContent = 'Please fill in both fields.';
        return;
      }

      status.textContent = 'Submitting...';
      try {
        const res = await fetch(IRONSTANDARD_BREVO_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, attributes: { FIRSTNAME: name } })
        });
        if (!res.ok) throw new Error('Request failed');
        status.textContent = "You're on the list. We'll be in touch.";
        waitlistForm.reset();
      } catch (err) {
        status.textContent = 'Something went wrong. Please try again.';
      }
    });
  }
});
