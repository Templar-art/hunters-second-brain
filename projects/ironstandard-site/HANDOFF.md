# Iron Standard website: handoff

Prepared by 10x Visuals, October 2026.
Built against the approved *Website Strategy & Creative Direction* (Sept 2026) and the
*IRONSTNDRD Guidelines 2026*.

---

## What's in this folder

| Folder | What it is | Who uses it |
|---|---|---|
| `01 Website` | The complete site: 6 core pages, 4 legal pages, a 404 page, all assets. Open `index.html` to view it locally. | Developer, or anyone checking the site |
| `02 Upload zip` | The same site, zipped and ready to upload to hosting. Internal notes are stripped out. | Whoever puts it online |
| `03 Enquiry form setup` | The Google Apps Script that receives contact-form enquiries, plus step-by-step setup. | Whoever owns the Iron Standard Google account |
| `04 Previews` | Full-page stills of the six core pages at desktop size, plus four at phone size. Stills show the resting layout: motion and the fixed photos behind the centred statement bands only appear in a browser. | For showing Anthony |
| `Iron Standard - Website Preview.html` | The whole site in one file. Double-click to open it in a browser and click through every page. For review only, not for uploading. | Anyone reviewing the site |

## The pages

| Page | File | Main button |
|---|---|---|
| Home | `index.html` | Explore the facility |
| About Us | `about.html` | View the facility |
| The Facility | `facility.html` | Explore coaching |
| Coaching | `coaching.html` | Enquire |
| FAQ | `faq.html` | Contact us |
| Contact Us | `contact.html` | Send enquiry |

Footer: Privacy, Cookies, Terms of use, Accessibility. Every page header carries
"Make an enquiry". There is no waitlist anywhere, as the strategy requires.

---

## Putting it live

The current coming-soon page at ironstandard.no runs on WordPress (Elementor) on a separate
host, with the domain's DNS at GoDaddy. Pick one:

**Option A: Netlify (free, recommended)**
1. Unzip `02 Upload zip/Iron Standard - Website.zip`.
2. Drag the unzipped folder onto app.netlify.com/drop.
3. In Netlify, add the custom domain `ironstandard.no` and follow its DNS instructions in GoDaddy.
4. Security headers and old-WordPress-URL redirects are already set in `netlify.toml`.

**Option B: the existing host (cPanel)**
1. Back up the WordPress site first.
2. Clear `public_html` and upload the contents of the zip.
3. `.htaccess` is included: it forces HTTPS, serves the 404 page, and redirects old WordPress URLs.

## Before launch: must do

1. **Connect the enquiry form.** It is deliberately switched off and tells visitors so.
   Either set up the Google Apps Script (`03 Enquiry form setup/README.md`), then paste its
   URL into `contact.html` where it says `PASTE_WEB_APP_URL_HERE`. Or, if hosting on
   Netlify, switch to Netlify Forms (about 10 minutes of work).
2. **Confirm the domain.** Share previews, canonical tags and the sitemap assume
   `https://ironstandard.no/`.

## Waiting on Anthony

- Founder story, credentials and dates, plus Thomas Lilley's advisory role. The About page
  uses general copy until these arrive. Nothing about him has been invented. On-page
  "pending" notes were removed at the client's request, so this list is now the only record.
- OK to name Anthony McCoy and Thomas Lilley publicly.
- Legal copy for the four footer pages (needs a proper legal review).
- Real photography. Every image is a low-resolution stand-in from the brand guidelines.
  The footer no longer says so (client request), so swap them before launch.
- English, Norwegian or both. The strategy says to settle this before content production.
- Address approval. A location block is ready (hidden) in `contact.html` and can go live
  once the address is approved for publication.

---

## Design notes for whoever edits it next

- **Stylesheets.** `assets/site.css` holds the base design (type, colour, layout);
  `motion.css` adds the motion layer on every page; `home.css` is homepage only. Colours are
  black, white and `#F4502A` only, plus greys. Orange buttons use **black** text: white on orange fails accessibility
  contrast (3.48:1), black passes (6.03:1).
- **Motion system.** `assets/motion.css` + `assets/motion.js` load on every page: masked
  headline reveals, photo wipes, eased scroll effects, icon cards, the marquee, the page hero
  and the closing band. `home.css` / `home.js` add only the homepage's pinned stage and
  horizontal proof. Without JavaScript, or with "reduce motion" switched on, every page is a
  complete static layout. Native scrolling is never taken over.
- **Photo grade.** Every photo runs through one warm black-and-white treatment
  (`--grade` in the stylesheet) so the stand-in images read as one shoot. Once the real
  shoot is colour-graded, change that one line to a light correction.
- **Numbered section marks** (01, 02...) come from the approved strategy and the print
  guidelines. Some design tools flag them; keep them.
- **No two sections in a row use the same layout.** Keep that when adding pages; it's what
  stops the site reading as a template.
- Equipment brand names on plates in photos are fine. Another gym's branding is not.

## Revision history

- Round 1: homepage rebuilt with scroll-driven motion (pinned hero and position, horizontal proof,
  centred photo band, icon cards, marquee).
- Round 2: smaller hero heading with Oslo pin, condensed proof, clickable support cards,
  centred founder, big faded logo in the closing band.
- Round 3: header scroll line removed, closing title "Raise your standard.", logo halved,
  lighter overlay. The homepage style then rolled out to every page.
- Round 4: header turns white with a black logo once it sticks; ring label "Strength"; support
  cards change colour instantly on hover; closing label "Your move" on every page, logo starts
  further right; About founder section rebuilt; all on-page notes removed. The contact form's
  "not connected yet" warning stays: it shows only until the form is connected, then disappears.

## Quality checks passed

- Accessibility: text contrast, keyboard navigation, focus states, alt text, form labels,
  one main heading per page. Tested at 320, 375, 768, 1100, 1440 and 1920px wide, at normal
  and 200% text size.
- Text follows the visitor's own text-size setting.
- No sideways scrolling on any page, at any of those sizes. Where text sits over a photo
  (page heroes, statement bands, closing bands) a dark overlay keeps it at readable contrast.
- Long Norwegian words in headings wrap without breaking the layout.
- The enquiry form validates name and email, blocks double sending, and only says
  "thank you" when the server confirms. Spreadsheet formula injection is blocked.
- Whole site is about 1MB. No framework, no build step.
