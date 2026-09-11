# Iron Standard — Waitlist Landing Page

Static page, no build step. Open `index.html` directly, or serve the folder with any static host (`.claude/launch.json` has a local preview server registered as `ironstandard-lp` on port 8140).

**The hero is a single fixed photo (11 Sep).** It used to rotate through 4 clips every 2.2s, which read as the page fading to black and back long after the intro had finished. It's now one still (`young-man-sportswear-exercise-class-gym-scaled.jpg`) at `position: fixed`, so it holds steady while the content scrolls up over it. The clips in `assets/video/` are no longer referenced by anything and the rotation code is gone from `main.js`. Because the photo is fixed, everything below the hero has to sit on an opaque band or the photo shows through it — that's what the `.page-rest` wrapper and the `background` on `.site-footer` are for. Don't remove them.

**Images are remote (11 Sep).** Every `<img>` and the video poster now point at the WordPress media library at `https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/`, not at `assets/img/`. The local files in `assets/img/` are still the originals and are worth keeping as the source, but nothing on the page references them any more. Two consequences: the page needs a network connection to look right (opening `index.html` offline shows a page with no imagery), and if those media items are ever deleted or renamed in WordPress, the page breaks silently. The videos in `assets/video/` are still local.

## 1. Set up Brevo (email storage — this is what you show investors)

A Brevo account already exists under 10x's account. Add Iron Standard as its own list there — no new Brevo signup needed.

**Note (11 Sep):** the waitlist `<form>` was pulled out of `index.html` per Hunter's request, to be added back in manually once the real Brevo values are in hand. There's an HTML comment marking where it goes. **The anchor is `id="form"`, not `id="waitlist"`** — the hero button and the scroll arrow both point at `#form`, and they scroll nowhere until an element with that id exists.

1. In Brevo: **Contacts > Lists > Create a list**, name it "Iron Standard Waitlist".
2. **Contacts > Forms > Create a form** (classic form), select the "Iron Standard Waitlist" list, add Name + Email fields.
3. Brevo generates an embed snippet — copy its `<form>` `action` URL and the hidden `<input>` field names/values it includes for the list ID.
4. In `index.html`, at the marked comment, paste back a form built the same way the old one was: a `<form method="POST" action="...">` pointing at that real action URL, with the two hidden inputs set to whatever field names/values Brevo's snippet actually includes (names vary slightly per account), then Name + Email fields and a submit button.
5. **Do not** switch this to a `fetch()` call against Brevo's REST API with an API key in the JavaScript — that exposes the key to anyone who views the page source. The form-POST pattern above is what Brevo intends for public sites and needs no secret client-side.
6. Anytime you want to show investors the list: Brevo dashboard > Contacts > that list > Export as CSV.

## 2. Export existing leads from the current GoDaddy site first

Before retiring `ironstandard.no`'s current "Launching Soon" page, log into GoDaddy Website Builder and check the form responses it's been collecting — export anything there and add it to the new Brevo list so no early signups are lost.

## 3. Deploy to Netlify

1. Create a free account at netlify.com.
2. Drag-and-drop the `ironstandard-lp` folder onto Netlify's deploy area (or connect it to a git repo for auto-deploys). `netlify.toml` is already in the folder — it sets security headers and long-cache rules for the video/image assets, no extra config needed.
3. Netlify gives you a temporary `*.netlify.app` URL immediately — check the site there first.

## 4. Point ironstandard.no at Netlify

1. In Netlify: Site settings > Domain management > Add custom domain > enter `ironstandard.no`.
2. Netlify shows you the DNS records to set (usually an A record + CNAME for `www`).
3. Log into GoDaddy > My Products > DNS (for ironstandard.no) and add those records. GoDaddy stays your domain registrar — you're only changing where the domain *points*, not who you bought it from.
4. DNS changes can take a few hours to propagate.

## 5. Footer partial

`partials/footer.html` is a standalone copy of `index.html`'s footer (self-contained, loads the same font/CSS with adjusted relative paths) so it can be grabbed and reused on another Iron Standard page without digging through the full page markup. It's a copy, not an include: editing one doesn't update the other, so if the footer changes on the real page, copy the change over manually.

## 6. What's still needed

- Real opening date (currently placeholder "Oslo · Opening 2027" text in the hero).
- Real photography for the accordion panels. Three of the four now use client-supplied images from the media library (`19535.jpg`, `23876.jpg`, `9063.jpg`); the "Get in first" panel still borrows `flash-2.jpg` from the intro sequence.
- No favicon yet — the only logo files on hand are the 3165x370 extended wordmark, and Iron Standard's own brand guidelines forbid cropping or altering the brandmark. Their monogram mark (the compact square version made for exactly this) is listed as "Work In Progress" in their guidelines — add a favicon once that ships.
- Analytics if wanted (Plausible or GA4 — not wired in yet).
