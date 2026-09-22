# Iron Standard website

Six-page static site built against the approved Website Strategy & Creative
Direction (Sept 2026) and the IRONSTNDRD Guidelines 2026.

No build step. Plain HTML, one shared stylesheet, one shared script.

## Pages

| File | Primary action |
|---|---|
| `index.html` | Make an enquiry |
| `about.html` | View the facility |
| `facility.html` | Explore coaching |
| `coaching.html` | Enquire |
| `faq.html` | Contact us |
| `contact.html` | Send enquiry |

Plus four legal stubs (`privacy`, `cookies`, `terms`, `accessibility`) that need
real copy from legal review before launch.

## Design system

`assets/site.css` is the single source of truth. Colours are black, white and
`#F4502A` only, plus two functional greys for interface hierarchy. Orange buttons
use black label text: white on orange is 3.48:1 and fails WCAG AA, black on
orange is 6.03:1 and passes. Type is TASA Orbiter from Google Fonts.

No two consecutive sections share a layout pattern. That is deliberate and is the
main thing to preserve when adding pages.

## Local preview

    python3 -m http.server 8145 --directory projects/ironstandard-site

Or `ironstandard-site` in `.claude/launch.json`.

## Before launch

1. Deploy the enquiry handler and paste the Web App URL into `contact.html`
   (`google-apps-script/README.md`). Until then the form is deliberately inert.
2. Replace the founder narrative, credentials and advisory copy. Placeholder
   notes are visible on the page where this is outstanding.
3. Replace all imagery. Everything in `assets/` is low-resolution moodboard
   material from the brand guidelines, standing in until the facility is
   photographed.
4. Legal copy for the four stub pages.
5. Restore the location block in `contact.html` (currently commented out) once
   the address is approved for publication.

## Not on this site, deliberately

No waitlist, pricing, street address, opening date, named equipment brands,
quantities, competitor names or membership terms. None of it is confirmed and
publishing it creates a liability.
