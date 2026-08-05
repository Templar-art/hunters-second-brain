10x Visuals — site handoff for WordPress/Elementor build

WHAT'S IN HERE
- 12 HTML files: index.html (homepage) + 11 interior/case-study pages
  (branding, content-creation, lead-generation, systems-processes,
  contact-us, sol, davenport, salisbury, elysium,
  broncos-leagues-club, stonehaven).
- assets/prestige.css + assets/prestige.js — all the site's styling and
  behaviour (animations, scroll reveals, work-grid toggle, enquiry form
  logic, etc). Link/script tag both already point at assets/ relatively.
- assets/tdx-widgets/ — a small prebuilt JS/CSS bundle that powers the
  3D-ish "closer look" photo gallery on the homepage. Just include the
  two files as-is; no build step needed on your end.
- assets/logos/ — the real client logos used in the homepage logo strip.
- assets/close-a-1400.webp and assets/founders-800.webp — the only two
  images not already hosted on the live WordPress media library
  (wp-content/uploads/2026/08/) at the time of export.

IMPORTANT
- Every other image and video on the site already points at
  https://10xvisuals.com.au/wp-content/uploads/2026/08/... — so most
  media doesn't need re-uploading, it's already live.
- Site header/nav and footer have been intentionally removed from every
  page — these are meant to be supplied by your WordPress theme /
  Elementor template, not duplicated from the static build.
- Each page is a self-contained <body> of content (hero, sections, the
  enquiry-form CTA) — drop the inner HTML into an Elementor HTML widget
  or template per page.
