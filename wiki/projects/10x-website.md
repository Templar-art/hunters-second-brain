---
type: project
tags: [10x-visuals, website, design-system, prestige, lead-gen]
status: deploy-in-progress-hunter-and-lach
updated: 2026-08-10
---

# 10x Website

10x Visuals' own front door, `10xvisuals.com.au`. A WordPress site with real content and real case studies whose finish did not match the work it sells. Rebuilt on 30 Jul 2026 as six static pages against [[brand-system|Prestige DS v1.0]]: the homepage plus all five interior pages, generated from a script rather than hand-written.

**Build:** [projects/10x-site/](../../projects/10x-site/) · **Spec + outcome:** [design spec](../../docs/superpowers/specs/2026-07-30-10x-homepage-prestige-rebuild-design.md) · **System of record:** [DESIGN.md](../../DESIGN.md), Prestige layer
**Handoff (6 Aug):** [projects/10x-site-for-lach/](../../projects/10x-site-for-lach/) · **Media:** [projects/10x-site-media-export/](../../projects/10x-site-media-export/)
**Vite/React app:** [projects/10x-site/web/](../../projects/10x-site/web/) ([README](../../projects/10x-site/web/README.md)) — the tooling scaffold behind the showcase widget, distinct from the static export.

## Handoff to [[lachlan]] (6 Aug 2026)

The static build was exported for a WordPress/Elementor rebuild: 12 HTML files (homepage plus 11 interior and case-study pages), `assets/prestige.css` + `prestige.js`, the `tdx-widgets` bundle behind the homepage "closer look" gallery, and the real client logos. `README.txt` in that folder is the handoff note.

Two deliberate choices in the export, both easy to get wrong on the receiving end. **Header and footer are stripped from every page** — those come from the WordPress theme and must not be duplicated out of the static build. And **most media is not in the export at all**: images already point at `10xvisuals.com.au/wp-content/uploads/2026/08/…`, so only the two files that were not yet in the media library ship alongside. The separate media export folder holds the full set at multiple widths (800/1400/1800/2200 + webp) for anything that does need re-uploading.

## What the site is

Six pages: home, `/branding`, `/content-creation`, `/lead-generation`, `/systems-processes`, `/contact-us`. Five real case studies ([[sol]] · Davenport · [[bespoke-estate-agents]] · Elysium · Broncos Leagues Club), sixteen named clients, one testimonial. Structure was sound. Skin, typography, rhythm and motion were not.

## What shipped

A single self-contained `index.html`: full-bleed **Stonehaven** aerial hero under the headline "Presentation decides the price.", a typeset client roster, six case-study plates alternating full-bleed and two-up, a parallax interlude, the four disciplines as hairline rows, founders, testimonial, and a three-field enquiry close. Works over `file://` and HTTP. Not deployed.

**Hero: Stonehaven**, 47 Somerset Drive, marketed by Whitefox: the late-afternoon aerial. It replaced the [[sol]] drone frame on 30 Jul, and then a dusk patio frame that Hunter rejected the same day. Work order is Stonehaven, Davenport + Bespoke, Elysium, then SOL + Broncos; SOL moved below Elysium at Hunter's request.

## What it taught us

**A handed-down design system can still be wrong, and measuring beats deferring.** Prestige DS v1.0 shipped four token values that fail WCAG AA on the surfaces they actually land on, including its own text blue at 4.39:1. Four amendments are now the real system, recorded under The AA-Amendment Rule. The lesson generalises: a token is only compliant on the surface it lands on, which is the [[brand-system|Surface-Not-Token Rule]] arriving for the third time.

**⚠️ Two of Hunter's systems contradicted each other.** Prestige DS v1.0 prescribes a tracked kicker and an oversized roman numeral on every section. `DESIGN.md` already forbade both, after two pages were stripped for it earlier in July 2026. Resolved in favour of DESIGN.md: the older rule was learned from shipped work, and the pattern is also the most saturated AI landing-page tell of 2026, so it actively worked against the premium read it was meant to produce. **When a new system contradicts a rule the vault learned the hard way, the learned rule wins until Hunter says otherwise.**

**Never gate content visibility on JavaScript.** The first reveal implementation hid every below-fold section until an IntersectionObserver fired. A deep link to `#close`, which the page's own hero CTA points at, could land on a blank section. Reveals must enhance an already-visible default, with a failsafe that clears them regardless. The related lesson — not misreading such a pane as broken — is in auto-memory as `feedback-hidden-pane-scroll-reveal`.

**Mismatched logo files are worse than no logos.** Nine client logos across dark-on-white JPEGs, an inverse navy lockup and a yellow Ray White square cannot be unified by greyscale and multiply; they render as pale boxes of unequal weight. A typeset Prata roster looks more expensive and carries the ten clients that have no logo asset at all. Recorded as The Roster-Not-Logos Rule.

**Measure the type zones, do not judge them.** For each zone the photograph's mean luminance in that region is composited through the scrims and the type's own alpha, then read as a contrast ratio. On the Stonehaven aerial the kicker measured 3.45:1 against a 4.5 requirement, purely because the DS sets that label at 62% opacity and it lands where the scrim is weakest. Full opacity fixed it at 6.09:1 without dimming the photograph at all. The instinct would have been to deepen the scrim, which would have cost the subject for no reason.

**A hero is chosen by where the dark is, not by how good the photo is.** The SOL drone frame is a strong photograph and still made a poor cover, because its lower third is a bright white roof and pale concrete, exactly where the headline sits. Stonehaven works because its foreground lawn and paving are dark, giving ivory type a real bed. Judge a candidate by the tonal map of the region the type occupies, not by the image as a whole, and judge it at full resolution: SOL was picked off a downscaled preview where that roof read as dark water.

**Watch for burnt-in marketing graphics in client deliverables.** The first White Fox files found were `Whitefox Mappins-0*.jpg`, all four carrying a map-pin graphic composited into the frame, which DESIGN.md bans outright. The usable set was the 47 Somerset Drive prints. Anything named for a marketing treatment rather than a shot is suspect.

## What it taught us, round two

**A modal that fades in over the trigger reads as generic; a modal that grows out of the trigger reads as premium.** The project lightbox measures the clicked photo's own `getBoundingClientRect()` and animates it via transform only (translate + scale, the FLIP technique) from its exact on-page position into the fullscreen frame. The same photo grows, rather than a box appearing on top of it. Genuinely the highest-leverage single addition for "does this look expensive" of anything built this week, and it cost no new dependency, just careful transform math.

**A tracked-caps text trigger reads more premium than a hamburger icon.** Copied from a competitor review (Desire Studio): "MENU" / "CLOSE" as plain text in the nav's own type voice, not an icon. Also fixed a real bug the review surfaced: the mobile nav had collapsed to a single Contact link with no way to reach the other four pages without going through the enquiry form first.

**Test contrast against the surface the element actually sits on, every time, or the check is fabricated.** Twice this week a contrast measurement compared a colour against the wrong background (once the lightbox's own `.tlink` inherited paper-tuned blue and measured 3.1:1 on night; once a page's on-paper close section was checked against night by mistake in the test script itself). The pattern repeats [[brand-system|the Surface-Not-Token Rule]] for the fourth time: a token, or a test, is only valid for the surface it actually targets.

**Headless Chrome's `--virtual-time-budget` does not reliably advance CSS transitions driven by JS class changes.** Repeated pattern this week: an animated element caught mid-flight or apparently overflowing in a headless capture, while the live browser's computed `getBoundingClientRect()` at the same moment shows the correct, settled, in-bounds state. When a screenshot and a live measurement disagree on anything animated, trust the measurement.

## What shipped, round three (31 Jul) — ticketed pass, partial release

Work ran as a formal ticket pack (ENG-01 through ENG-10) executed one ticket at a time, in implementation mode, against the six existing pages. Three tickets landed; one stayed correctly blocked.

**ENG-01 — [[sol]] case-study scaffold.** New `scripts/build_case_studies.py` mirrors `build_pages.py`'s generator pattern exactly and produces `sol.html`, with an empty image sequence and no quote — both real, intentional branches, not placeholders. Davenport, Bespoke, Elysium and Broncos Leagues Club follow the same shape in later tickets; none are built yet.

**ENG-02 — blocked, correctly.** The SOL image sequence needs real shoot frames. Checked `raw/`, an external SSD, Desktop, Downloads, and the live WordPress site's own `/sol/` page (the same sourcing method used all week) — none held usable SOL photography. Reported as blocked rather than filled with placeholder or invented imagery. Still open.

**ENG-09 — contact-funnel microcopy, and a real duplication fixed.** Added "We'll only use this to reply." to the enquiry form. Doing this surfaced that `FORM` existed in three places, not the assumed two: `build_pages.py`'s own constant, a byte-identical copy `build_case_studies.py` had picked up in ENG-01, and `index.html`'s hand-written inline form. `build_case_studies.py` now imports `FORM` from `build_pages.py` instead of duplicating it. That import exposed a real hazard: both generators' page-writing loops ran unguarded at module level, so importing `FORM` would have silently regenerated every page as a side effect. Both are now wrapped in `if __name__ == "__main__":`. `index.html`'s copy remains a documented hand-synced exception — it isn't generated by anything, so there's nothing to extract it into without a build step that was out of this ticket's scope.

**ENG-10 — hero value-restatement line.** One line added under the hero lede on the four service pages only (not `contact-us.html`, which isn't in `PAGES`), via a new optional `value_line` param on `hero()`, reusing the existing `.lede-h` class. No new CSS.

**Release scope.** Assessed as not ready for the full intended release (five of six case studies don't exist yet) but ready for a partial one. Shipped: home, `/branding`, `/content-creation`, `/lead-generation`, `/systems-processes`, `/contact-us`. Excluded: `sol.html` and all other case studies. Committed as `2e7610f`, all 9 changed files staged deliberately (nothing swept in with `-A`).

**Still not deployed.** No hosting pipeline exists in this repo — no Netlify/Vercel/GitHub Pages config, no deploy workflow. The only git remote is this vault's own backup repo, not a hosting target, and the live `10xvisuals.com.au` is still the separate WordPress site. Asked Hunter directly rather than guess a target; he chose local-only for now. Viewable at `http://localhost:8791/` via the project's dev server while that stands.

**Should-fix, not blocking:** the homepage work-grid's five case-study tiles (`/sol`, `/davenport`, `/bespoke`, `/elysium`, `/broncos-leagues-club`) point at routes with no backing page at all. Harmless with JS on — the project lightbox intercepts the click before navigation, confirmed live — but a real dead end for no-JS visitors or a link-checking crawler. Pre-existing from the lightbox build, not introduced this pass, and will get worse as more tiles get wired to still-unbuilt pages.

## What shipped, round four (31 Jul) — video heroes, React widgets, all six case studies

**Video heroes on home and SOL.** Hunter supplied working cuts (`~/Downloads/WEBSITE VIDEO_v02.mp4` for SOL, `~/Movies/test.mp4` for the homepage), both re-edited once during the session and now final per Hunter. Transcoded from 4K/120-180MB sources down to ~12MB 1080p h264, muted/looped/autoplay, with the original still nested as a no-video-support fallback (home) or reused as the poster frame (SOL, no new asset needed). `hero()` and `cs_hero()` both gained an optional video param; `prestige.js` pauses `.hero-video` for `prefers-reduced-motion` since autoplay/loop/muted are otherwise native, JS-free attributes.

**Client list corrections.** Founders caption reordered to match the actual photo (Tyson · Damon · Lachlan, left to right — it was wrong). Hill Interior Linings dropped from the client list (no longer a client). Ocean Shores renamed to Coastlife Constructions and moved from Venues & Brands into Builders & Developers, where it belongs.

**A real React/shadcn stack, on request.** Hunter asked specifically for two components from a pasted shadcn registry snippet (a 3D drag carousel, a hover-expand gallery row) with their own React/Tailwind/TypeScript/shadcn requirements — a different stack from the rest of this static, Python-generated site. Rather than silently reinterpreting the ask, flagged the mismatch and the pasted code's Unsplash/picsum stock imagery, got explicit confirmation the real stack was wanted, then built it as a genuinely separate concern: `projects/10x-site/web/`, scaffolded with the actual `shadcn` CLI (confirming `/components/ui` really is its default path), building to a self-contained IIFE bundle (`assets/tdx-widgets/`) that the static `index.html` loads via plain `<script>`/`<link>` tags — no Node server at runtime. Real project photography swapped in for every stock image.

**Two real Tailwind v4 bugs, not user error, cost real time here:**
- The content scanner silently skips filenames starting with a digit. The pasted component's own filename, `3d-carousel.tsx`, was never being scanned at all — zero classes generated, no error. Renamed to `carousel-3d.tsx`.
- The "skip Tailwind's preflight reset so it doesn't fight the host page's styles" approach — importing `tailwindcss/theme.css` + `tailwindcss/utilities.css` separately instead of the single `@import "tailwindcss"` — silently breaks content scanning entirely, independent of the filename bug. Reverted to the standard `@import "tailwindcss" prefix(tdx)` (which does include preflight), and contained its blast radius by loading `tdx-widgets.css` *before* `prestige.css` in `<head>`, so prestige.css's own body/heading rules win any cascade tie. Verified live that `h1` still renders in Prata, not Tailwind's reset.

Both bugs were isolated by bisection (a minimal sibling test file, renamed copies, config reverts) rather than guessed at — worth remembering if Tailwind v4 content detection ever silently returns zero classes again on this project.

**ENG-02 closed, not left blocked.** Hunter's call: SOL never gets a separate image sequence — it ships with the hero video instead, and that's sufficient. Confirmed the other five case studies (Davenport, Bespoke, Elysium, Broncos, Stonehaven) are in the identical asset situation SOL was in — exactly one real photo each in `assets/`, nothing further in `raw/` — and built them anyway, to the same honest standard: real hero photo, real brief copy (reused verbatim from the homepage grid, not invented), no sequence, no quote, close block. All six case-study pages now exist and are real.

**Dead work-grid tiles, fixed.** The homepage's six case-study tiles pointed at routes with no backing page (`/sol`, `/davenport`, etc. — extensionless, nothing served there). Now that all six pages are real, every tile's `href` points at the actual generated file (`sol.html`, `davenport.html`, ...); Stonehaven's tile, which previously had no link at all (a bare `role="button"` div), now has one too. Confirmed the project lightbox still intercepts every click under normal JS operation — this only changes behaviour for no-JS visitors and crawlers, from broken to correct.

## What shipped, round five (4 Aug) — real pillar photography, carousel galleries, WordPress media migration

**All four pillar heroes replaced.** Branding, Lead Gen, AI Systems and Content pillars had been shipped with placeholder stock (round four had no real photography for them yet). Now:
- **Branding** — a business-card mockup built from scratch (perspective-warped Bespoke Estate Agents wordmark, real logo pulled from `projects/bespoke-scrape/brand/logos/`, composited onto a stock concrete-tile photo via OpenCV `getPerspectiveTransform` + shading match, not an AI generation). First pass used the wrong Bespoke entity (Staging & Styling, a sister brand) — corrected once Hunter clarified he meant [[bespoke-estate-agents]] itself.
- **AI Systems + homepage card** — real 10x BTS photo (`AI PILLAR.JPG`, laptop showing code + a glowing blue AI network render), sourced from `/Volumes/10X SSD5/10x BTS STUFF/Print/`.
- **Content pillar** — real BTS crew photo (`MVX ELECTRICAL BTS PHOTOS FOR 10x-3.JPG`), from an earlier round-five exchange.
- **Lead Gen** — no real asset existed for this one; sourced free-licensed stock instead (a dual-monitor desk/chart photo, cropped tight to stay abstract). Rejected two earlier candidates first: the extremely overused "Search Console clicks/impressions" screenshot (50M+ views — reads as stock instantly) and a generic Excel-chart-gallery screenshot.
- Pasted-inline images (sent directly in chat) aren't file-accessible to any tool here — each time, Hunter had to save to disk and give a path (Finder "Option-click → Copy as Pathname") before it could go in the pipeline. Recurring limitation, not a one-off.

**Case-study photo galleries converted grid → carousel.** Hunter's explicit call: the `.pg-grid` full-page grid of every delivered photo (Salisbury/Stonehaven/Elysium/Davenport/Broncos, 32-57 photos each) was "too much on one page." Rebuilt as `.pg-strip`, an edge-to-edge horizontal-scroll filmstrip (same break-out technique as `.interlude`/`.disc-split`: `width:100vw;margin-left:50%;transform:translateX(-50%)`), `scroll-snap-type:x proximity`, fixed-width `.pg-item`s. Lightbox click-through (`#pg-lightbox`, prev/next, Escape/click-outside) untouched — same markup, only the container layout changed.

**All new pillar images uploaded to WordPress media library, `LOCAL_ONLY` cleared.** Got WP REST API application-password auth working (`hunter@10xvisuals.com.au` + app password — first attempt used a display name "Claude WP Login" as the username, which 401'd; the actual account email worked). Uploaded 24 files (4 pillars × 3 widths × jpg/webp) via `POST /wp-json/wp/v2/media`; WP's big-image threshold (2560px) auto-scaled the 1800w portrait variants and suffixed them `-scaled`, but confirmed the plain unscaled filename URL also resolves (200), so `MEDIA_BASE + filename` still works unmodified. `build_pages.py`'s `LOCAL_ONLY` set (which routed these four basenames to local `assets/` while they were placeholder stock) is now empty. Full-site link sweep after: 87/87 remote (WP) URLs return 200, 995/995 local asset references (`src`/`srcset`/`href`/`poster`/`data-full-webp`) resolve on disk. Case-study gallery photos and hero videos deliberately stayed local-only — per-job raw delivery assets, not evergreen site chrome, never uploaded to WP by design.

**Deploy decision made.** Previously open ("decision still open on whether this replaces the WordPress site or is handed to the web team to port," round four). Resolved: Hunter deploys it himself as a static-file bypass — upload the finished `.html`/`.css`/`.js`/`assets/` straight onto the same server/domain so they load directly, WordPress keeps running underneath but these pages don't route through it. Considered and passed on for now: a full WP theme port (translating `build_pages.py`/`build_case_studies.py`'s shared `nav()`/`shell()`/`hero()` template functions into PHP template parts) — assessed as genuinely feasible given this site's already-templated structure, but scoped as its own week-sized job, not folded into this pass. Reason to defer further: **Lachlan still needs to build the WordPress header/footer/menu layout** — so the real theme port waits on that anyway.

## Open

- **No form endpoint.** `FORM_ENDPOINT` is `null`; submit opens a `mailto:` compose. One line at deploy.
- **Founders portrait.** Current frame is a studio-seamless team shot, greyscaled and cropped as a holding treatment. Wants a real environmental portrait, which is a shoot.
- **Plate grading.** Night aerial next to bright daylight frames. A true one-grade pass needs graded exports, not CSS. See [[color-grading]].
- **⚠️ `/contact-us/` still carries a seven-field form with a required free-text message**, the exact friction 10x bills clients to remove. See [[lead-gen-engine]].
- **Deploying now, not yet live.** Hunter is uploading the static files to the server himself (FTP/cPanel, not yet handed to Claude — no file-level server access exists here, only WP REST media). Lach separately owns the WordPress header/footer/menu layout; a full WP theme port of this design is a real future option (see round five) but blocked on that work first.
- **Both hero videos are Hunter's own working cuts**, final as of 31 Jul per Hunter — but if he re-edits again, the transcode step (`ffmpeg` crop/scale/crf, see commit history) needs re-running, it isn't automated.

## Corrections to the vault

The claim that `10xvisuals.com.au` has **no lead form** ([[lead-gen-engine]], verified 27 Jul 2026) was **wrong as of 30 Jul 2026**: a form exists at `/contact-us/`. The real problem was never absence, it was friction.

---
_Vault: [[overview]] · [[brand-system]] · [[lead-gen-engine]] · [[hunter]]_
