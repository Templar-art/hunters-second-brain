# Iron Standard — Full Site

Static site, no build step. Open `index.html` directly, or serve the folder with any static host (`.claude/launch.json` has a local preview server registered as `ironstandard-lp` on port 8140).

## Pages

| Page | File | Purpose |
|---|---|---|
| Home | `index.html` | Brand tone, positioning, links to everything else |
| About Us | `about.html` | Founder story — Anthony's own narrative pending |
| The Facility | `facility.html` | The 800m² space, equipment, posing room |
| Coaching | `coaching.html` | Programming, independent PTs, events |
| Join the Waitlist | `waitlist.html` | The founding-member offer and sign-up form |
| FAQ | `faq.html` | Opening timeline, location, audience, founding membership |
| Contact Us | `contact.html` | Contact form, email, social (pending) |

Nav (`.site-header`, hand-duplicated into every page's `<body>` — there's
no templating engine, so it's a copy in each file, same as
`partials/footer.html` already documents itself as "a copy, not an
include") links all 7 pages together. `waitlist.html` carries `id="form"`
inside its form section — every "Join the waitlist" link across the site
points at `waitlist.html`, and the button/scroll-arrow pattern from the
single-page build era is gone (there's nothing to scroll to any more,
Waitlist is its own page).

**The intro flash-and-logo sequence plays once per browser session, not
once per page** (`sessionStorage`, see `assets/js/main.js`). Landing on
any page for the first time in a session plays it; clicking to another
page goes straight in. A new tab (fresh session) sees it again.

## Data flow — Google Sheets, not Brevo

Anthony confirmed he's going with a Google Sheet, replacing the
Brevo-based plan from the original single-page build. See
`google-apps-script/README.md` for the full deployment steps — they
have to run inside Anthony's own Google account, nothing here can be
scripted. Short version: both forms POST to a Google Apps Script Web
App, which appends a row to the "Waitlist" or "Contact" tab of a Sheet
he owns, and emails him a notification per submission.

**Before either form works, `REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL` in
`waitlist.html` and `contact.html` needs to become the real deployed
Web App URL.** Until then, every "Join the waitlist" and "Send" button
on the site submits to a URL that doesn't exist. This is the same kind
of placeholder the single-page build shipped with while waiting on
Brevo — nothing is broken, it's just not live yet.

**Never** switch either form to a `fetch()` call with a credential in
the JavaScript. The Apps Script Web App URL being public is fine — it's
not a secret, that's how Apps Script Web Apps are meant to work — but no
*other* kind of API key belongs in this codebase's client-side JS,
matching the same rule the original Brevo build followed.

## Hosting

Still unresolved as of this rewrite: Anthony asked 10x to host the site
(replacing the original Netlify-under-his-own-account plan), but which
of 10x's existing hosting arrangements that lands on hasn't been decided.
`netlify.toml` is left in place and untouched — it works under Netlify
regardless of whose account it's deployed from, so this doesn't block
building or reviewing the pages themselves. Domain stays at GoDaddy as
registrar either way; only DNS target changes once hosting is decided.

## Export existing leads from the current GoDaddy site first

Before retiring `ironstandard.no`'s current "Launching Soon" page, log
into GoDaddy Website Builder and check the form responses it's been
collecting — export anything there and add it to the new waitlist Sheet
so no early signups are lost.

## Footer partial

`partials/footer.html` is a standalone copy of the footer (self-contained,
loads the same font/CSS with adjusted relative paths) so it can be
grabbed and reused without digging through a full page's markup. It's a
copy, not an include: editing one doesn't update any of the 7 pages'
inline footers.

## What's still needed

- **Real copy for three pages**, all explicitly pending from Anthony:
  the About Us narrative, the Waitlist offer wording, and the FAQ
  questions and answers. Each page currently ships accurate placeholder
  copy built only from his 16 Sep email, flagged with an HTML comment
  at the exact spot to swap it in.
- **Facility photography.** Two client-supplied stills are live
  (`inside-the-facility.jpg`, `posing-room.jpg`); real photos/renders
  follow once the fit-out begins, per Anthony.
- **Social links for Contact** — not yet supplied. The page currently
  says "Social links are coming soon" rather than shipping dead or
  invented links.
- **The Apps Script deployment** — see Data flow above.
- **Hosting target** — see Hosting above.
- No favicon yet — the only logo files on hand are the 3165x370 extended
  wordmark, and Iron Standard's own brand guidelines forbid cropping or
  altering the brandmark. Their monogram mark (the compact square version
  made for exactly this) is listed as "Work In Progress" in their
  guidelines — add a favicon once that ships.
- Analytics if wanted (Plausible or GA4 — not wired in yet).

## Notes carried over from the single-page build

**The hero is a single fixed photo.** It used to rotate through 4 clips
every 2.2s, which read as the page fading to black and back long after
the intro had finished. It's now one still
(`young-man-sportswear-exercise-class-gym-scaled.jpg`) at
`position: fixed`, so it holds steady while the content scrolls up over
it. The clips in `assets/video/` are no longer referenced by anything
and the rotation code is gone from `main.js`. Because the photo is
fixed, everything below the hero has to sit on an opaque band or the
photo shows through it — that's what the `.page-rest` wrapper and the
`background` on `.site-footer` are for, on `index.html` only (the 6
inner pages have no hero and no fixed photo, so they don't need this).

**Mobile hero rules.** Three things in the hero are viewport-dependent
and easy to break by "tidying":
- The h1 is one sentence with two sets of `<br>`. `.br-d` shows above
  640px, `.br-m` shows at 640px and below. Don't replace them with
  duplicated headings.
- `.hero-bg` uses `height: 100lvh`, never `100vh` or `100%`. On a phone
  the URL bar collapses on first scroll, which changes the viewport
  height, which makes `object-fit: cover` re-crop the photo — it looks
  exactly like the image popping and zooming. `lvh` is the largest
  viewport height and never changes, so the crop is computed once.
- `.hero` uses `min-height: 100svh` for the opposite reason: `svh` is
  the smallest viewport height, so the hero's own content always fits
  above the fold with the URL bar showing.
