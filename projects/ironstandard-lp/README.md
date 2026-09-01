# Iron Standard — Waitlist Landing Page

Static page, no build step. Open `index.html` directly, or serve the folder with any static host (`.claude/launch.json` has a local preview server registered as `ironstandard-lp` on port 8140).

## 1. Set up Brevo (email storage — this is what you show investors)

A Brevo account already exists under 10x's account. Add Iron Standard as its own list there — no new Brevo signup needed.

1. In Brevo: **Contacts > Lists > Create a list**, name it "Iron Standard Waitlist".
2. **Contacts > Forms > Create a form** (classic form), select the "Iron Standard Waitlist" list, add Name + Email fields.
3. Brevo generates an embed snippet — copy its `<form>` `action` URL and the hidden `<input>` field names/values it includes for the list ID.
4. In `index.html`, find the `#waitlist-form` element and replace:
   - `action="REPLACE_WITH_BREVO_FORM_ACTION_URL"` → the real action URL from Brevo's snippet.
   - the two hidden inputs (`REPLACE_WITH_BREVO_LIST_FIELD` / `REPLACE_WITH_LIST_ID`) → whatever hidden fields Brevo's snippet actually includes (names vary slightly per account).
5. **Do not** switch this to a `fetch()` call against Brevo's REST API with an API key in the JavaScript — that exposes the key to anyone who views the page source. The form-POST pattern above is what Brevo intends for public sites and needs no secret client-side.
6. Anytime you want to show investors the list: Brevo dashboard > Contacts > that list > Export as CSV.

## 2. Export existing leads from the current GoDaddy site first

Before retiring `ironstandard.no`'s current "Launching Soon" page, log into GoDaddy Website Builder and check the form responses it's been collecting — export anything there and add it to the new Brevo list so no early signups are lost.

## 3. Deploy to Netlify

1. Create a free account at netlify.com.
2. Drag-and-drop the `ironstandard-lp` folder onto Netlify's deploy area (or connect it to a git repo for auto-deploys).
3. Netlify gives you a temporary `*.netlify.app` URL immediately — check the site there first.

## 4. Point ironstandard.no at Netlify

1. In Netlify: Site settings > Domain management > Add custom domain > enter `ironstandard.no`.
2. Netlify shows you the DNS records to set (usually an A record + CNAME for `www`).
3. Log into GoDaddy > My Products > DNS (for ironstandard.no) and add those records. GoDaddy stays your domain registrar — you're only changing where the domain *points*, not who you bought it from.
4. DNS changes can take a few hours to propagate.

## 5. What's still needed

- Real opening date (currently placeholder "Oslo · Opening 2027" text in the hero).
- An image for the "Who it's for" section — free stock search kept surfacing bright, heavily-branded CrossFit-box photography that clashed with the dark/premium direction. Worth a real shoot or a paid stock license rather than more free-stock searching.
- Hero currently plays a single clip (`assets/video/hero-woman.mp4`, SD preview-quality — fine for v1, upgradeable to Pexels' HD/4K download later). A second, heavier-load male clip is still wanted for the crossfade, but neither free stock (Pexels — outdoor/light-weight/generic-CrossFit only) nor Adobe Stock turned up the right heavy indoor powerlifting look. **Best remaining option: footage of Anthony himself** — he's a competitive powerlifter, so a real clip of him pulling heavy is both on-brand and solves the "real emotion, real weight" ask better than any stock library will. Once a file exists, add it as `assets/video/hero-man.mp4` and reintroduce a crossfade between two `<video>` elements in `index.html`'s `#hero` section (duplicate the current single-video markup, add a second `<source>`, and add a CSS crossfade animation on `.hero-video`).
- Analytics if wanted (Plausible or GA4 — not wired in yet).
