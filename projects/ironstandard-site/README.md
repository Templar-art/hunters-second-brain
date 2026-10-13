# Iron Standard website

Six-page static site built against the approved Website Strategy & Creative
Direction (Sept 2026) and the IRONSTNDRD Guidelines 2026.

No build step. Plain HTML, one shared stylesheet, one shared script.

## Pages

| File | Primary action |
|---|---|
| `index.html` | Explore the facility |
| `about.html` | View the facility |
| `facility.html` | Explore coaching |
| `coaching.html` | Enquire |
| `faq.html` | Contact us |
| `contact.html` | Send enquiry |

Plus four legal stubs (`privacy`, `cookies`, `terms`, `accessibility`) that need
real copy from legal review before launch, and a `404.html`.

Primary actions follow the strategy's page table (p19). The header button on
every page is always "Make an enquiry".

## Design system

`assets/site.css` is the single source of truth. Colours are black, white and
`#F4502A` only, plus two functional greys for interface hierarchy. Orange buttons
use black label text: white on orange is 3.48:1 and fails WCAG AA, black on
orange is 6.03:1 and passes. Type is TASA Orbiter from Google Fonts.

No two consecutive sections share a layout pattern. That is deliberate and is the
main thing to preserve when adding pages.

Tokens worth knowing:

- `--grade`: one warm-monochrome treatment applied to every photograph so the
  stand-in imagery reads as one shoot. Swap it for a light correction once the
  real shoot is graded.
- `--sp-section` / `--sp-section-tall` / `--sp-section-tight` / `--sp-statement`:
  vertical rhythm, scaled for desktop.
- All type is in `rem`, so it follows a visitor's text-size setting.

- **Motion system.** `assets/motion.css` + `assets/motion.js` load on every page: masked
  headline reveals, photo wipes, eased scroll effects, icon cards, the marquee, the page hero
  and the closing band. `home.css` / `home.js` add only the homepage's pinned stage and
  horizontal proof. Without JavaScript, or with "reduce motion" switched on, every page is a
  complete static layout. Native scrolling is never taken over.
Numbered section marks (01, 02...) are a client decision from the approved
strategy and print guidelines. Design linters flag them; keep them.

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
   photographed. Equipment brand names visible on plates are fine; another
   gym's branding is not.
4. Legal copy for the four stub pages.
5. Restore the location block in `contact.html` (currently commented out) once
   the address is approved for publication.

6. Confirm the domain: `og:url`, canonical tags and `sitemap.xml` assume
   `https://ironstandard.no/`.

## Not on this site, deliberately

No waitlist, pricing, street address, opening date, named equipment brands,
quantities, competitor names or membership terms. None of it is confirmed and
publishing it creates a liability.
