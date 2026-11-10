# Log

Append-only record of wiki operations. Entry format: `## [YYYY-MM-DD] ingest|query|lint|migrate | Title

## [2026-09-15] lint | Curtains made a default, not an ask
On the zed-full-house living/dining/kitchen frame, Hunter had to ask twice for curtains before I added them — the rule was already in [[zed-style]]'s global kit but wasn't reaching the actual prompts. Also the first curtain attempt bled one sheer panel across the entire wall instead of per-window, because the instruction wasn't anchored to a frame. Added a standing rule to [[staging-rules]] (check every bare window/door, add sheers unasked, anchor each panel to its own frame width) and a matching auto-memory file `feedback-curtains-default-and-anchor`.

## [2026-09-10] lint | Iron Standard: audit fully cleared (clarify, harden, polish)
Worked through the remaining 3 findings from the 10 Sep `/impeccable audit` (14/20) one command at a time: `/impeccable clarify` reworded the scroll-arrow's stale aria-label ("...waitlist form" → "...join the waitlist", the form doesn't exist right now); `/impeccable harden` gave the details-visual image crossfade a real default (facility's photo shows even without `:has()` support, instead of an empty box); `/impeccable polish` swapped the one hardcoded `#050505` for `var(--bg)`. All verified live in Chrome. Logged to [[iron-standard]].

## [2026-09-10] lint | Iron Standard: optimize pass, one real fix + one corrected false positive
Ran `/impeccable audit` then `/impeccable optimize` on the polish pass above. The audit's P1 finding (lazy-load the accordion's 4 duplicate photo refs) turned out to be a false alarm on measurement: those URLs are already loaded eagerly by the intro flash sequence (10 images, always eager by design), and browsers dedupe identical URLs regardless of how many `<img>` tags reference them, confirmed via network trace (10 requests fired for 10 files despite 3x reuse in markup). No fix made there. The real, measured issue: `flash-8.jpg` was 594KB, 3-8x its siblings, because it was the one full-color stock photo in a set that's grayscale-filtered everywhere it's shown. Re-encoded it to true grayscale via ffmpeg, 594KB → 228KB, visually identical, verified live. Logged to [[iron-standard]].

## [2026-09-10] ingest | Iron Standard: UI/UX polish pass (impeccable)
Hunter reviewed the zip he'd sent to Lach and came back with 5 items: intro hold pause too long, "More details" section flat/boring, pull the waitlist form (adding it back manually once Brevo's live), split the footer into its own file for reuse, and an overall animate-in/premium-feel bump. Used the impeccable skill (brand register) to action all 5: cut the intro's post-reveal hold 35% (1300ms → 845ms), rebuilt the details section as an interactive tab list with a photo panel that crossfades per item via CSS `:has()` (no JS, native `<details name>` grouping for single-open behaviour, inline thumbnail fallback on mobile), pulled the `<form>` out of `#waitlist` leaving a placeholder comment, split `partials/footer.html` out as a standalone reusable copy, and added a scroll-reveal system (IntersectionObserver, content stays visible with JS off). Kept the existing brand identity (dark, orange `#F4502A`, TASA Orbiter) rather than the skill's own DESIGN.md defaults, those belong to 10x's own brand, not a client's. Logged to [[iron-standard]].

## [2026-09-08] ingest | Iron Standard: hyped the accordion labels too
Follow-up: Hunter wanted the collapsed accordion (kicker + 4 summary labels, the only thing visible before clicking) punched up too. "More details" → "What you're getting"; "The facility" → "Inside the facility"; "Who it's for" → "Is this you?"; "What's different" → "Why it's different"; "Founding members" → "Get in first". Body copy underneath unchanged. Logged to [[iron-standard]].

## [2026-09-08] ingest | Iron Standard: hyped copy up without new claims
Hunter wanted more hype/FOMO ("what you're missing") without sounding cocky. Reworked hero-sub, who's-it-for, what's-different pillars, founding-member and waitlist-sub copy to lead with the gap it fills (fighting for a rack, running between three addresses, being the odd one out) rather than superlatives about the gym itself. No new factual claims added, still limited to what Anthony's actually cleared. Logged to [[iron-standard]].

## [2026-09-08] ingest | Iron Standard: condensed info sections into an accordion, stripped em dashes
The 4 restored content sections (facility/who's-it-for/what's-different/founding-member) read too long once actually built, per Hunter. Collapsed them into a single "More details" section using native `<details>/<summary>` (no JS needed), copy trimmed to one short paragraph each, first item open by default so the page doesn't look empty. Also removed every em dash from on-page copy (title, hero sub, waitlist sub, founding-member text) per Hunter's request, swapped for periods/commas. Cache-bust bumped to `?v=4`. Logged to [[iron-standard]].

## [2026-09-08] ingest | Iron Standard: accent colour reverted to original orange
Follow-up to the same-day feedback pass below: after landing on gold `#C9A227`, Hunter saw it live and rejected it ("looks like it came from Claude"). Tried deep forest green `#1B5E3F` next, also rejected. Landed back on the original brand-guideline orange `#F4502A` — accepting the SATS overlap rather than force an alternative nobody likes. `assets/css/style.css` `--accent` reverted, cache-bust bumped to `?v=3`. Logged to [[iron-standard]].

## [2026-09-08] ingest | Iron Standard: client feedback actioned same day
Anthony emailed Lachlan real messaging direction, contradicting the 2 Sep build's simplification to hero+waitlist-only. Restored full page structure (What-it-is / Who's-it-for / What's-different / Founding-member) with copy limited to what he actually cleared (800m², 24/7, top-tier equipment, posing room, coaching/PT/physio, competing-or-not), an explicit location/date/pricing-still-coming line, and new FOMO/scarcity copy that didn't exist before (founding-member priority access, first-come-first-served, capped total spots). Separate email: Anthony flagged SATS also uses orange and deferred the accent colour to 10x's judgement — tested steel-blue/bronze/olive/emerald live against the built page before landing on gold `#C9A227`, which also reinforces the founding-member "tier" framing. Also fixed a stale-CSS-cache issue discovered mid-session (browser was serving an old style.css across reloads; `location.reload(true)` no longer force-bypasses cache in modern engines — added a `?v=` cache-bust param instead). Logged to [[iron-standard]].`

## [2026-09-02] build | Iron Standard waitlist landing page
New client, Anthony McCoy's Oslo powerlifting gym (pre-launch). Built a static waitlist landing page — Brevo for email capture (investor-exportable list, added as a list under 10x's existing Brevo account), Netlify hosting with GoDaddy DNS repoint. Caught and fixed a real security issue mid-build: the first pass would have exposed a Brevo API key in public page JavaScript; corrected to a plain form POST against Brevo's hosted Forms endpoint instead. Spec: `docs/superpowers/specs/2026-09-02-ironstandard-landing-page-design.md`. Plan: `docs/superpowers/plans/2026-09-02-ironstandard-landing-page.md`. Page: [[iron-standard]].

## [2026-08-27] ingest | Per-camera job-folder labeling — non-negotiable standard
Hunter set a hard standing rule from a live example (Shape | Westside HQ job): every job folder gets one subfolder per camera device (`{Camera Model} - {N} Files ({Unit} {Value})`, e.g. `A7R5 - 370 Files (GB 47)`) plus a `Selects` folder, always. Documented in [[archiving-and-backup]]. Also built `ssd-drive-upload` skill (`~/.claude/skills/ssd-drive-upload/`) for the SSD→gdrive rclone upload workflow, and re-ordered a live 11-zip/~975GB upload batch smallest-first on request.

## [2026-07-10] migrate | Genesis — vault restructured to LLM-wiki pattern
Converted the vault to the Karpathy LLM-wiki structure (spec: `docs/superpowers/specs/2026-07-10-llm-wiki-restructure-design.md`). `memory/` retired and translated into `wiki/` (5 people, 5 clients, 6 projects/concepts pages); CLC pack PDFs + capability statement moved to `raw/clc/`; CLC pack markdown, audit, field research, and swipe file became `wiki/sources/` pages; CONTEXT.md → [[music-taxonomy]]; root notes → wiki/projects/; working artifacts (scroll demo, CVA breakdown, dashboard, TASKS) → top-level `projects/`; CLAUDE.md rewritten as the schema.

## [2026-08-19] query | Jang Studio fake-flambient technique theory
Lachlan's theory on how Jang fakes flambient without real flash brackets: depth map → 3D mesh warp (Blender) → virtual flash lights → render lighting pass only → composite masked over real ambient. Matches VIP 24-48hr vs standard 8-12hr turnaround gap. Logged to [[jang-studio]].

## [2026-07-10] ingest | Jarvis phase 1 — spec, prompt, wiki page, scheduled routine
Designed and built Jarvis phase 1 (brain + ops copilot): spec at `docs/superpowers/specs/2026-07-10-jarvis-phase1-design.md`, agent prompt at `projects/jarvis/PROMPT.md`, concept page [[jarvis]]. Weekday 7am Brisbane morning brief from 10x CRM to-dos via push notification; loud failure rules.

## [2026-07-10] ingest | Jarvis phase 2 — JOB.md job-state tracking
Spec `docs/superpowers/specs/2026-07-10-jarvis-phase2-job-tracking-design.md`; template `projects/jarvis/JOB-template.md`; CLAUDE.md job-tracking rule; cross-project auto-memory entry; [[jarvis]] roadmap updated.

## [2026-07-10] ingest | Jarvis phase 3 — push-to-talk voice layer built
Spec + plan in docs/superpowers/; pipeline in `projects/jarvis/voice/` (Hammerspoon right-option push-to-talk → ffmpeg → whisper-cli base.en → `claude -p` voice prompt → say Daniel + overlay). Installed Hammerspoon + whisper base.en model. Pending: CLI re-auth (OAuth expired 17 Jun), first-run mic/accessibility perms, headless CRM verification.

## [2026-07-13] ingest | 10x highlight story content — 18 frames built (3 per bubble), 10x Premium Kit/stories/

## [2026-07-13] migrate | 10x story frames v2 (adaptive scrim, craft titles in sky) + READY TO POST pack on Desktop

## [2026-07-13] ingest | 10x Socials Funnel — new RE + construction accounts designed, launch assets built
Brainstormed with Hunter: split RE/construction into new IG+TikTok accounts, master @10xvisuals.co curates best-of. Handles checked live (10x.realestate free both platforms; 10x.construction free on IG, squatted on TikTok → 10xconstruction). Bios + highlight structure drafted. Recoloured X-mark logo variants (orange construction, deeper-navy real estate) generated via SVG gradient remap — deliberate override of the brand guideline's "never recolour the X" rule, Hunter's call. Wiki page [[10x-socials-funnel]], assets in `projects/10x-socials-funnel/assets/`. Account creation itself left to Hunter (out of scope for Claude).

## [2026-07-13] lint | 10x Socials Funnel — colour plan reversed, logo-file bug found
Hunter's boss overruled the per-vertical recolour (navy RE / orange construction) from earlier today: profile photos go plain white on all three accounts, no colour coding. While building the white variant, found the existing "10xVisuals_10X Symbol White.svg" is mislabelled — only half the X is actually white, the other diagonal is still blue gradient. Built a correct all-white replacement in `projects/10x-socials-funnel/assets/`; corrected the stale claim in auto-memory `reference-brand-assets`. [[10x-socials-funnel]] updated.

## [2026-07-14] ingest | 10x feed pack — 10 posts + captions (10x FEED - READY TO POST); bubble covers reverted to white-mark photo versions per boss

## [2026-07-14] migrate | 10x social engine — tenx.py consolidation, reel + ad formats, gap audit + SOPs (10x-social-engine page); PRODUCT.md + DESIGN.md added

## [2026-07-14] ingest | vertical launch packs (RE + construction: covers, 6 posts each, READMEs) + talking-head system (12 scripts, cadence) — funnel launch-ready

## [2026-07-14] query | live feed sweep via Chrome — handle renamed @10xvisuals_, Broncos posted 7d ago (pulled from pack), highlights hold old shares, Staging bubble missing; posting plan on Desktop; Drive deliverables pull running

## [2026-07-14] query | full Mar-Jul feed registry built (captions read), TO POST list w/ 14 verified-unposted content sources; Drive pull ongoing

## [2026-07-14] ingest | Salisbury scroll-scrub demo built (10x-scroll-salisbury) + Seedance prompt ready; pipeline documented

## [2026-07-14] ingest | Seedance 2.0 render live in Salisbury scroll demo (3,500 cr, approved) + per-niche replication recipe

## [2026-07-14] ingest | Salisbury scroll v2 — 20s built-before-your-eyes film (4 chained Seedance clips + NB Pro stage stills, ~14k cr approved via 174k balance); stage captions on scrub

## [2026-07-14] ingest | MVX Electrical aircon landing page redesign — phone-first conversion rebuild vs T42 competitor; deliverable projects/mvx-aircon/ + new client page

## [2026-07-14] ingest | MVX residential electricians LP built on aircon-page system (projects/mvx-electricians)

## [2026-07-14] ingest | Seedance camera-move look-test (2,800 cr Mini): orbit wins, dolly-in strong, fpv drifted; awaiting Pro-commit direction

## [2026-07-14] ingest | Salisbury scroll v4 — cinematic reveal/orbit/step-inside fly (3 chained Seedance 2.0 Pro clips, ~10,500 cr); 2D rig retired, cross-blend kept; per-niche recipe documented

## [2026-07-14] ingest | Salisbury scroll v5 — full aerial build+fly (6 Pro clips, dirt→slab→frame→house→reveal→orbit→inside); end-keyframe re-anchor to real photo; reused earlier fly clips to save ~7k cr

## [2026-07-15] ingest | Strategic Investing QLD social batch 1 — 9 posts / 20 slides (Quiet Equity system, PIL, 0 cr); new brief re-aligned from its "sans-serif/navy" note to the client's established Marcellus-serif house style; client + source pages filed

## [2026-07-16] lint | 10x socials scrub — White Fox burned (posted 1d), full-drive re-sweep, new master list TO-POST-2026-07-16-SCRUB.md

## [2026-07-16] update | Villa Noosa drop staged for tonight — card + 4:5 film crop + caption, handle verified @ashley_cooper_construction, ACC feed collab-checked clear

## [2026-07-16] project | 10x Prestige World scroll site built (projects/10x-prestige-world) — 5-scene photoreal fly-through, Prestige v2.0 brand, seams eye-verified

## [2026-07-16] ingest | Anthony lead intake → proposal v1 built (projects/anthony-proposal), wiki/clients/anthony.md created, $1,800/mo retainer, 24 posts/month

## [2026-07-16] update | Anthony lead proposal v2 — rebranded for Hattie Boydle (@hattieboydle), 10x branding dropped, dark bronze athletic system, /impeccable pass + mobile QA

## [2026-07-16] update | Anthony/Hattie proposal v3 — $1,500/mo, brand-guidelines palette (cream/ink/orange, Poppins+Lora), no-studio copy fix, PDF exported to project + Desktop

## [2026-07-16] update | Hattie Boydle responded warm; Hunter confirmed direct deal (not 10x); reply drafted at $1,500 all-in

## [2026-07-16] ingest | Agentic OS phase 1 — loop engine (launchd morning brief + nightly lint) + AIOS dashboard (localhost:8770, action buttons), concept page added

## [2026-07-17] query | AIOS morning brief

## [2026-07-17] harvest | anthony-proposal → clients/anthony, concepts/proposal-playbook, overview

## [2026-07-17] update | AIOS L4 live — scrubbed template repo pushed private (Templar-art/aios-template); dashboard button verified end-to-end (morning brief ran from click)

## [2026-07-17] query | weekly review
[[weekly-review-2026-07-17]] filed. Shipped: vault genesis, Jarvis phases 1-3, socials funnel + engine consolidation, Salisbury scroll v2-v5, MVX LPs x2, SIQ social batch (23 posts, 0cr), Prestige World scroll site, Anthony/Hattie proposal → warm reply → harvested, AIOS phase 1 + L4 template. Stalled: Akmal (3d), SIQ ad kit (7d, client-side), Belle Property (7d, awaiting Hunter go), CRM MCP (Vercel auth). Next focus: clear the stalled client queue before new intake.

## [2026-07-17] lint | graph connectivity pass — 12 dead-end pages linked (CLC pack → client, taxonomy → library), 10 broken/ghost links fixed (auto-memory refs unlinked, relative paths corrected), index given inbound from overview. Wiki graph: 0 orphans, 0 dead-ends, 0 broken links

## [2026-07-19] ingest | Craft knowledge base — new `wiki/craft/` reference layer, 29 pages
Built the missing how-to-shoot/edit/sell layer the wiki lacked (it was all client/ops before). New `wiki/craft/` folder + hub [[craft]] and 6 domain MOCs with reference notes: **architectural photography** ([[architectural-photography]] + [[arch-composition]], [[perspective-correction]], [[exposure-blending]], [[light-and-timing]], [[interior-photography]], [[exterior-architecture]], [[photo-gear-and-settings]] — Hunter's current focus), **videography** ([[videography]] + [[video-camera-settings]], [[cinematic-movement]], [[property-film-structure]], [[audio-for-video]]), **post-production** ([[post-production]] + [[photo-editing-pipeline]], [[color-grading]], [[video-edit-pipeline]]), **AI toolkit** ([[ai-toolkit]] + [[ai-image-tools]], [[ai-video-tools]], [[ai-prompting]] — defers routing/money-gate to [[higgsfield-pipelines]]/[[staging-rules]]), **content systems** ([[content-systems]] + [[reel-formats]], [[posting-cadence]] — defers voice/design to [[ig-caption-voice]]/[[brand-system]]), **business** ([[business-craft]] + [[pricing-and-packaging]], [[client-onboarding]], [[lead-gen-and-sales]] — defers recipe to [[proposal-playbook]]). Additive only: no existing page substance changed; craft section added to [[index]], pointer added to [[overview]], cross-links added from higgsfield-pipelines/staging-rules/brand-system/ig-caption-voice/music-taxonomy/proposal-playbook. All craft wikilinks verified resolving; 0 broken links.

## [2026-07-19] ingest | Architectural photography — 10 gap notes added
Deepened the [[architectural-photography]] domain (Hunter's focus) after a coverage review. New reference notes filling genuine gaps: [[tilt-shift-technique]], [[focus-stacking]], [[panorama-stitching]], [[metering-and-dynamic-range]], [[architectural-details]] (detail/abstract/B&W), [[shot-list-and-planning]] (incl. tethered shooting), [[deliverables-and-export]] (web/print + AU portal specs), [[archiving-and-backup]] (3-2-1), [[releases-and-permissions]] (AU: Copyright Act ss65–66 freedom of panorama, property access, model/CASA drone, licensing — carries "not legal advice / verify current CASA + portal specs" caveats), [[real-estate-vs-architectural]] (positioning split). MOC reorganised into sections and index line updated. Additive only; 0 existing pages changed in substance; 0 broken links, 0 orphans. Domain now 18 pages (MOC + 17). Deliberately left out as optional (Hunter's call): standalone HDR-software note, artificial/strobe-lighting-only deep dive, matterport/3D-tour capture, film/large-format, competitions/awards submissions.

## [2026-07-19] ingest | Architectural photography — 5 optional notes added (Hunter took them all)
Added the five previously-deferred topics: [[hdr-software]] (merge vs tone-mapping; quick path vs flambient), [[strobe-lighting]] (flash for interiors — bounce, gels, drag-the-shutter, when it beats natural light), [[matterport-3d-tours]] (virtual-tour capture as an add-on deliverable), [[film-large-format]] (view-camera movements + film tradition, tied back to digital tilt-shift), [[awards-and-competitions]] (which to enter, submission craft, leveraging wins for the 10x brand — carries "verify current rules/deadlines" caveat). MOC reorganised sections updated, index line bumped to MOC (22). Additive only; 0 existing pages changed in substance; 0 broken links, 0 orphans. Architectural photography domain now 23 pages (MOC + 22) — coverage complete.

## [2026-07-21] setup | rclone SSD → Google Drive upload pipeline
Diagnosed slow client-delivery uploads. Verdict: connection is elite (700 Mbps up, gigabit ethernet on UniFi) and NOT the bottleneck — the limit is Google Drive's per-connection browser throttle + the desktop app forcing an internal-disk cache (internal only ~39 GB free) when uploading off external SSDs. Fix = installed rclone (brew, v1.74.4), configured remote `gdrive` → **10x Visuals | Clients** shared drive (OAuth browser auth, full scope). rclone reads straight off the SSD, streams in parallel chunks, no internal copy → solves both space + speed. New page [[rclone-drive-upload]] (indexed) holds setup + daily commands. Cleared competing background sync (Google Drive app, Adobe Core Sync/CCX/Desktop Service) during the diagnosis. Google Drive desktop app left installed but rclone is now the SSD-upload path.

## [2026-07-21] setup | Bulk SSD → Drive backfill system (projects/drive-upload)
Built the "ask and it uploads" pipeline. Inventoried all deliverable zips across 3 SSDs (~2TB, 38 files after junk filter — dropped ._ AppleDouble, 0B empties, non-deliverables). Hunter routed the 24 ambiguous address/name files to client folders (Mystery→"mystery stuff", Jason→Bespoke, address listings→Zed Real Estate/Whitefox/Phillis/Jessica Wallace, etc.). Mapping frozen in projects/drive-upload/upload-map.tsv; resumable uploader projects/drive-upload/upload.sh (--check/--dry-run/run, --drive-stop-on-upload-limit for the 750GB/day cap). --check passed 38/38. Live test: 3049 Boulevard Jason.zip landed in Bespoke ✅ ~19MB/s. Full run pending (multi-day, resumable). Ongoing model: Hunter says "upload X to Client" → append map line + run.

## [2026-07-21] update | Stalled queue cleared — Akmal, Belle Property, SIQ ad kit all delivered
Hunter confirmed three stalled jobs done. Akmal (1007/180 Marine Parade, ZED restyle) intake→delivered. Belle Property Lot 48 (house-into-lot composite) awaiting-go→delivered. Strategic Investing QLD Meta ad kit review→delivered. JOB.md statuses + [[belle-property]] client page bumped. Active job now ZED full-house only.

## [2026-07-21] query | 90-day social content plan (RE + Construction) — planner rebuilt v11
Hunter scoping tomorrow's work. Built the @10xvisuals_ own-feed 90-day content plan, two verticals (Real Estate + Construction), repurposing delivered library (zero new shooting). Prior planner xlsx (v1..v10) gone from ~/Downloads — rebuilt populated as `10x_Visuals_90Day_Growth_Planner_v11.xlsx`: 6 sheets, 65 posts / 13wk (Mon 27 Jul–Fri 23 Oct), weekly rhythm Mon RE / Tue Tyson TH / Wed Construction / Thu BTS / Fri trending+proof+wrap, monthly wraps last Fri, all captions in locked short voice, Status + Audience dropdowns, live Dashboard counts + Growth Tracker. Detail in auto-memory `project-90day-growth-planner`.

## [2026-07-22] query | Bespoke live website — logged + audited (services page)
External team finished and deployed the Bespoke Estate Agents website (WordPress + ElementsKit) at https://bespoke.agents.10xvisuals.co. Logged as a strong, brand-faithful deliverable on [[bespoke-estate-agents]] (Zodiak/Poppins, Bespoke Green, real photography, generous whitespace — Hunter's verdict "very good"). Ran an /impeccable audit of `/services/`. **Health 12/20 (Acceptable), dragged down by one P0:** every body-copy `.reveal` block renders at `opacity:0` — the scroll observer fires (`is-in in` classes added) and images fade in, but the text reveals never un-hide because `.reveal.in { opacity:1 }` loses the cascade inside the WP/ElementsKit stylesheet order, leaving all service copy + process steps + CTA invisible in-browser (verified via computed styles + blank screenshots on this Chromium; flagged "verify in your own browser"). P1s: hero LCP image `loading="lazy"`; 2560px `-scaled.jpg` served full-res with no srcset (heavy mobile payload). P2/P3: eyebrow kicker on every section (AI tell), `lang="en-US"` on an AU business, lowercased WP `<title>`, footer touch targets <44px, one img alt says "interior" over an exterior. Contrast all passes (green section 8.6:1, CTA muted 5.1:1, primary btn 15:1). Mobile clean (no overflow, h1 fits). Fix owner = external team; static concept in `projects/bespoke-site/` unaffected.

## [2026-07-22] correction | Bespoke website audit — P0 retracted (false positive)
The earlier "P0: invisible body copy on Services/Projects" was WRONG — a testing artifact, not a site bug. Root cause: the automation browser pane kept going hidden/backgrounded, and a hidden tab pauses CSS scroll-reveal transitions, so `.reveal` blocks froze at their `opacity:0` start state and never animated in during measurement. Re-verified two ways: (1) static cascade — forcing `transition:none` and reading the resolved state gives `opacity:1; transform:none` (`.reveal.in` wins cleanly, no `!important` theme override, no-JS handled via the `.js` gate); (2) visual — body copy renders on screen. **Corrected verdict: site is clean, renders fully, reads premium; no blocking issues.** Site also clarified to double as a live portfolio piece shown to a separate prospect 10x is closing (must land a "woah" on cold open + free roam — Home's cinematic video hero delivers it). Remaining items are minor polish (eyebrow-on-every-section, lowercase WP `<title>` on Services, `lang=en-US`); photos are deliberate placeholders, out of scope. Lesson: never trust scroll-reveal opacity readings taken while the browser pane is hidden.

## [2026-07-22] query | Bespoke Phase 2 design strategy (editorial luxury + CRM-ready)
Design strategy for the next phase of the Bespoke website (ui-ux-pro-max), adapting WHITEFOX's discovery/editorial STRUCTURE while rejecting its brash national-network voice (Bespoke = boutique GC, understated). Kept the committed brand identity (Zodiak Light + Poppins, Bespoke Green, no accent colours) — overrode the tool's generic teal/Cinzel picks. Confirmed direction: Exaggerated Minimalism / architectural-editorial, full-bleed cinematic photography, curated GC prestige-pocket Suburb Guides, quiet "Recent Results" suburb-record proof band, low-volume evergreen Journal. **Key decision: HYBRID + CRM-ready** — this may become a ~$30k deal that also builds the client a CRM, so architected a schema-first data model (Listing/Region/Agent/Lead/Contact/Deal/Office) with forms as Lead entry points and a shared `status` enum. **Stack recommendation: Next.js + Payload CMS (Postgres, client-owned), NOT WordPress** — WP-as-CRM is a plugin graveyard and live-feed sync into CPT is fragile; WP fallback (CPT+ACF+FacetWP) flagged as capping the CRM ambition. Full brief saved to `projects/bespoke-site/PHASE2-STRATEGY.md`. No build yet — awaiting Hunter on suburb list, Jason-vs-Jason+Barbara face, and stack sign-off.

## [2026-07-22] query | Bespoke Phase 2 — round-2 decisions locked (team, search, suburbs, dual-path stack)
Second clarifying round on the Phase 2 strategy. Locked: **team = Jason & Barbara premium boutique duo** (two Agent records); **search = Standard taxonomy** (Buy/Sold/Upcoming + Suburb/Price/Beds/Baths/Car/Type, no portal-depth this phase); **suburb shortlist proposed** for Hunter's approval (primary 6: Sovereign Islands, Mermaid Waters+Beach, Broadbeach Waters, Paradise Waters/Main Beach, Isle of Capri, Sanctuary Cove/Hope Island; secondary expand-later list), grounded in GC prestige reality + Bespoke's inferred footprint. **Stack = dual-path** (Hunter unsure the other team can do Next.js): Path A preferred (Next.js + Payload, CRM real) vs Path B fallback (WP + ACF + FacetWP + FluentCRM, CRM capped = pay-twice); front-end component contracts specced stack-agnostic so design is identical either way. Brief updated in `projects/bespoke-site/PHASE2-STRATEGY.md`. Still no build. Next: build spec (both paths) for the other team, or Claude prototypes the design language.

## [2026-07-22] query | Bespoke Phase 2 BUILD-SPEC — source of truth written
Turned PHASE2-STRATEGY.md into a build-ready spec: `projects/bespoke-site/BUILD-SPEC.md` (v1.0). Covers approved decisions + remaining assumptions, stack-agnostic design tokens (brand colours/type/spacing/motion/z-index/a11y baseline), full CRM-ready data model (Listing/Region/Agent/Lead + reserved Contact/Deal/Office, enums, relationship rules), component inventory (17 components) with per-component behaviour + states, URL-synced search/filter logic (status→data mapping, min-semantics, sort, empty/loading/error), suburb-guide template + proposed list, page-by-page structure with testable acceptance criteria (Home, Listings index, Listing detail, Suburbs index/guide, Sold, Journal, About/Contact) + global AC, explicit Phase 2 vs [P3+] boundaries, and dual-path implementation notes (A: Next.js+Payload preferred; B: WP+ACF+FacetWP fallback) behind one stack-agnostic data-access contract. Baked in the audit lesson (no content gated behind JS reveals). Handoff notes for Lach. No build yet — awaiting suburb approval + stack-capability confirmation.

## [2026-07-22] build | Bespoke Phase 2 prototype — core buyer journey (PropertyCard, FilterBar, Listings, Listing detail)
Built the first prototype of the design language + core journey from BUILD-SPEC.md, in `projects/bespoke-site/prototype/` (self-contained static HTML/CSS/JS, stack-agnostic). Reuses the existing brand foundation `../assets/css/main.css` (tokens/header/footer/buttons/Zodiak+Poppins fonts/bed-bath-car icons) + new `phase2.css` for Phase 2 components. Files: index.html (Listings archive), listing.html (cinematic detail), data.js (6 seed Listings + 6 Regions + Jason/Barbara Agents matching BUILD-SPEC §4 shapes), app.js (data-access layer getListings/getListing/getRegions as the swap seam, URL-synced FilterBar per §7, progressive reveal with hidden-pane failsafe, lightbox, form→Lead). Property imagery = client's Somerset Dr placeholder set pulled by URL (swapped later). Verified in browser (localhost:8771): Buy/Sold/Upcoming tabs re-filter correctly with URL deep-linking (?status=sold), Suburb Record/Sold/Under Offer markers render, cinematic listing hero + gallery lightbox (1/6) work, enquiry form validates and captures a Lead with source=listing_enquiry + relatedListing (logged), mobile 375 clean (no overflow, cards stack 1-up, filter pills scroll in-container), zero console errors. Dropped the WP build's numbered nav markers (AI tell) per design hook; added header top-scrim for legibility over bright hero media. A 70% starting point for Lach. Not linked from the live site.

## [2026-07-23] build | Bespoke Phase 2 prototype — refinement pass (wiring, copy, cohesion, QA)
Focused polish on the prototype (design language kept). Fixed: (1) no dead links — Suburbs/Journal/About/Contact now route to an on-brand `soon.html` placeholder (per-section heading via ?s=), every "Book a Private Appraisal" opens a centred appraisal modal (event-delegated, writes a Lead source=appraisal), Contact + soon?s=appraisal render an inline appraisal form; (2) filters — suburb dropdown broadened to 13 GC prestige suburbs (primary+secondary), min price now starts $750K, max goes to $10M+; (3) copy — removed all em dashes from user-facing content, tightened; (4) cohesion — full shared footer (brand blurb, Explore, Get in touch, real IG/FB/LinkedIn, "Beyond Luxury Real Estate") injected across all pages, consistent nav. Also fixed two real bugs surfaced by reading main.css: overlay menu needed `body.menu-open` (my `.open` toggle was a no-op), and main.css `.lightbox{opacity:0}` was hiding the lightbox (renamed mine to `.lb`); plus modal centring (main.css `*{margin:0}` killed native dialog `margin:auto`). QA on localhost:8771 desktop+mobile: 0 console errors, 0 dead `#` links, menu opens, modal centred, lightbox visible (1/6), filters+URL sync, soon pages render, mobile 375 no overflow (cards + listing cols stack). Handoff-ready. Files: index.html, listing.html, soon.html, phase2.css, data.js, app.js.

## [2026-07-23] build | Bespoke — integrated Phase 2 Collection into the main site (nav + positioning)
Positioning pass connecting the Phase 2 prototype into the parent static site (`projects/bespoke-site/`) as a dedicated **Collection** section. Unified primary nav across all 6 pages (parent index/services/projects + prototype index/listing/soon): Home · Collection · About · Services · Projects · Contact + "Book a Private Appraisal" CTA. Parent nav/overlay/footer now link into `prototype/index.html` (Collection replaces the old standalone "Sold Listings" nav item — Sold is now a Buy/Sold/Upcoming tab inside Collection). Prototype pages link back to the parent via `../` (Home/About/Services/Projects/Contact → parent sections/pages), Collection marked aria-current, footer Explore realigned. Matched the parent's numbered overlay menu on the Collection pages for cohesion (deliberately re-added the numbers I'd dropped when it was a standalone island — consistency with the established parent identity wins now that it's integrated). Unified CTA label to "Book a Private Appraisal" (was "Book an Appraisal") on parent header + footer. QA on localhost:8771: parent home intact (no console errors, showcase.js/gsap fine), Collection entry present in nav+overlay+footer, two-way navigation resolves correctly (Collection Home → parent index), 0 dead links across all 6 pages, appraisal modal + filters + lightbox still working. Preserved the parent design and all prior prototype work; no redesign. Left the parent's pre-existing single-font + numbered-overlay design-hook findings unchanged (existing identity, explicitly preserved).

## [2026-07-23] build | Open Arms Australia — site header redesign (Elementor widget, handed to Lach)
Redesigned the Open Arms Australia site header (NDIS provider, open.arms.10xvisuals.co, WP+Elementor) from a template-y navbar to a premium editorial-restraint healthcare header, inside the locked brand (Poppins; green #368063 anchor; purple #8080B8 as a single NDIS dot). Ran the full impeccable pipeline: redesign (solid white nav + hairline, green-tint trust strip, pill hover, arrow CTA) → single-phone-number fix → optimize (right-sized logo, preconnect+link instead of @import, dropped weight 700) → polish (focus-ring pill fix, mobile menu overflow scroll, 44x44 tap targets). Then Hunter caught a desktop logo-squash: nav content overflowed the 1240 wrap so flexbox crushed the logo to ~84x48; fixed with flex-shrink:0 on the logo, moving the phone to the top bar (freeing ~130px), and raising the hamburger breakpoint 980→1240px. Verified in real Chrome (logo 195x48 ratio 4.06, no overflow). Deliverable: `projects/open-arms-header/open-arms-header.html` (self-contained .oa-x-namespaced HTML+CSS+JS, paste into one Elementor HTML widget) + `HANDOFF.md` (install steps + Poppins-double-load and active-page notes). Given to Lach. Filed [[open-arms-header]] project page + [[open-arms-australia]] client stub; indexed under Clients + Projects. Reusable header shell for future 10x WP/Elementor clients (swap --oa-* vars, logo, menu items).

## [2026-07-27] lint | Vault + Claude-setup audit — knowledge leaks closed, token report
Full audit pass over the wiki, the auto-memory layer and the Claude config, looking for knowledge that exists somewhere in the system but never made it into the wiki, plus startup token waste.

**Leaks found and closed.** Six `projects/` folders had no wiki representation at all: `akmal`, `zed-full-house`, `elevra-invoices`, `bespoke-scrape`, `bespoke-theme`, `freelance-photo-proposal` — two of them (akmal, zed-full-house) were completed or in-flight paid client jobs with full JOB.md trails and hard-won lessons that were invisible to anyone reading the wiki. Wrote [[akmal]], [[zed-full-house]] and [[elevra-invoices]]; folded bespoke-scrape and bespoke-theme into [[bespoke-estate-agents]] and the freelance proposal into [[proposal-playbook]]; all indexed. Created [[zed-style]] as the single source for the ZED piece-list, which had been restated in full inside two separate JOB.md files and several memory entries. [[staging-rules]] was 17 days stale: eight rules learned between 14 and 22 Jul (ask the room type, ask if low-end, no wall art, single bedside lamp, no detail vignettes in wide frames, matching angles need a reference, `@original`/`@reference` tokens, outdoor furniture outdoors) existed only in auto-memory and never propagated to the vault. Added. Also: `strategic-investing-qld-brief` was the one page missing from [[index]]; a dead wikilink to `project-90day-growth-planner` in this log pointed at an auto-memory file rather than a wiki page (de-linked); ten CLC source pages had no YAML frontmatter (added, `type: source`).

**⚠️ Bank details in the repo.** `projects/elevra-invoices/invoices/*.json` carry a payment block with BSB and account number. The GitHub remote is private and the folder was still untracked, so nothing has been pushed — added to `.gitignore` before it could be. Noted on [[elevra-invoices]].

**Token findings (reported, not actioned).** Roughly 9–11k tokens of every session's opening context is avoidable: two output-style plugins are enabled at once (learning + explanatory, both injected, both fighting the caveman-ultra house rule), superpowers is installed twice from two marketplaces, and six plugin packs that this vault never uses (plugin-dev, agent-sdk-dev, ui-ux-pro-max, pr-review-toolkit, scroll-world, feature-dev) publish ~95 skill descriptions into the system prompt. `MEMORY.md` has also grown to 10 KB of index for 144 KB of memory, and 14 of its 49 entries are staging feedback that now duplicates [[staging-rules]]. Recommendations given to Hunter; no config changed.

## [2026-07-27] tune | MacBook Pro performance audit + monthly maintenance loop
Hunter reported general slowness. Audited the machine (M2 Pro, 16 GB, 460 GB SSD) rather than assuming a disk problem — and it wasn't one: 176 GB free, Spotlight idle, no Time Machine local snapshots, five apps open. The real constraints were **16 GB of RAM against ~23 Electron processes** (Claude desktop 11, Chrome 12 — 7.5 M pageouts and 990 MB swap in a 5-hour uptime), **WindowServer at 45% CPU** driving three displays with one external stuck at 75 Hz, and **Adobe's background stack** (5 launch agents + 3 daemons running with no Adobe app open, one steady at 5.3%).

Actioned with Hunter's go-ahead: disabled the three Adobe autostart agents persistently (`launchctl disable`, verified); cleared ~13 GB of regrowing cache (Claude VM bundle 6.8 GB, Google 3.0 GB, Adobe app caches 967 MB, Adobe logs 647 MB, Homebrew/pip/electron/node-gyp 800 MB); moved Chrome off the Desktop — where it had been installed alongside 59 GB of client footage — into `/Applications` and re-registered it with LaunchServices. Result: swap 990 → 386 MB, load 4.21 → 2.31, WindowServer 45.5% → 29.1%, free disk 176 → 189 GB. **Left the 6.7 GB Adobe Camera Raw cache intact on purpose** — it is the biggest number on any storage report and the worst thing to delete, since Lightroom rebuilds previews for weeks afterwards.

Made it durable: `com.10x.aios.mac-maintenance` (1st of month, 9:14am) runs `projects/aios-dashboard/bin/mac-maintenance.sh` — purges only self-regrowing caches, empties Adobe logs, clears Claude's caches *only when the app is quit*, and re-asserts the Adobe disable, because Adobe re-enables its agents on every CC update. Plain zsh, not an AIOS registry action: it touches the machine, not the vault, so no `claude -p` and no commits. Test run caught a real bug — macOS `pgrep` has no `-q` flag (exits 0 regardless) and `pgrep -f` won't match a full `/Applications/…` path, so the Claude guard failed open and purged the caches of the running app; switched to `ps -axo comm | grep -q` and re-verified it now skips. Filed [[mac-performance]] with the standing rules (never delete Camera Raw, never clear a live Electron cache, judge the machine by swap/load/WindowServer not free GB); indexed under Concepts; loop row added to [[agentic-os]].

Still open and Hunter's to do: drop the 75 Hz external to 60 Hz (System Settings → Displays) — the largest remaining CPU item, unreachable from a shell — and reboot to clear residual swap and stale Adobe processes.

## [2026-07-27] query | Client lead-gen diagnosis — MVX, CVA, 10x Visuals (live-site evidence)
Hunter asked why leads aren't coming in or converting for MVX Electrical, CVA Architects and 10x Visuals itself. No ad-account access this session (the `10x-crm` MCP is unauthorised, so no real pipeline numbers either) — diagnosed from live sites, sitemaps and page markup instead of guessing at campaigns.

**MVX — the hot water gap is structural, not a performance problem.** Matt wants to shift lead mix from aircon toward hot water electrical systems. Pulled the full 29-page sitemap: **zero** hot water / heat pump pages, nav items or mentions anywhere, including on both ad landing pages. Nothing exists for ads to point at, so there are no impressions to convert. Aircon leads flow because aircon is the only funded, page-backed service. **Blocked before building:** MVX holds electrical/ARC/solar/cabler licences but no plumbing licence, and the water side of a QLD hot-water swap is licensed plumbing — needs Matt's call on subbing vs partnering a plumber. Rebate angle if it proceeds: heat pump earns ~$998 in federal STCs, applied as an upfront discount (heat pump ~$2,600–6,300 installed → from ~$1,600), and heat-pump/electric-storage work is genuinely electrician-led.

**MVX — the 14 Jul landing pages shipped, but the form spec didn't.** Both builds went live as dedicated ad LPs (`/air-conditioning-electrician-gold-coast/`, `/gold-coast-electricians/`, sitemap lastmod 14 Jul). Design landed correctly. The Formidable build did not: read the live markup and found **six** `aria-required` fields per form — email and postcode required (spec deleted email outright) and the free-text message **required**, on mobile phone-intent traffic. Site nav also still present on both, which the spec said to strip. Wrote `projects/mvx-lead-fix/FORM-FIX.md` (delete Email, Postcode → Suburb, message optional, keep the `frm_verify` honeypot, strip nav, confirm `tel:` clicks fire as Google Ads conversions since on a phone-first page the calls *are* the leads). Also caught a live bug: the electricians form's job-type validation still reads "How can we help with your **aircon**?". Needs WP admin to apply; baseline 14 days of entries + call conversions first or the lift is unmeasurable. **Lesson: a shipped page is not a shipped spec — re-read the live markup after someone else rebuilds it.**

**10x Visuals — no leads because there is no lead capture.** 10xvisuals.com.au has no form at all; contact is a `tyson@` mailto plus a phone number, and portfolio CTAs go to "View Project". Cross-referenced `projects/fb-ads-handoff.md`: the 20 Jul investment-leads Meta campaign spent ~$160 for **zero** leads and that diagnosis was never closed (the 8 data points were never supplied). If those ads pointed at this site, zero leads is arithmetic. Selling "Lead Gen" as a nav-level service from a site with no lead form is also a credibility problem.

**CVA — no evidence any ads exist to diagnose.** Four pages, every CTA → `/contact`, no lead magnet, no pricing, no video, one testimonial. Architects carry a 6–18 month consideration window, so a bare "Begin Project" form captures only the already-decided; there is no top-of-funnel offer (feasibility / "what can I build on my block"). **Unused asset:** CVA's delivered job produced 19 stills + ~40 clips, already paid for — a finished ad library nobody is running.

**Harvest leak closed — the one thing that actually worked.** Hunter reported Strategic Investing QLD converting **10–15 leads in 4 business days**, a result recorded nowhere in the vault. Added to [[strategic-investing-qld]] and [[index]] — it is the only proven lead-gen pattern in the client book and the thing to copy rather than reinvent. Attribution flagged as unconfirmed: two assets shipped (10 Jul mortgage-freedom Meta ad kit; 15 Jul 23-post organic batch that is deliberately **CTA-free**), and CTA-free organic can't plausibly drive that in four days, so the ad kit is the likely driver — inference, not fact. Need which asset ran, spend, objective, and where leads landed before replicating. **Lesson: a campaign result is knowledge; JOB.md tracked the build and cost but had no field for whether it worked.**

## [2026-07-28] build | Lead Gen Engine — per-niche ad strategy + three landing pages
Hunter asked for ads and landing pages for each client, plus the research on why they work per niche. Built the strategy and all three pages. New project page: [[lead-gen-engine]].

**Research, and the rule it produced.** Match the platform to how the buyer arrives: something broke → Google Search (demand already exists, just be present); considering a big change → Meta (demand has to be created). Each of the three accounts was violating this. Three findings drove the builds: **service-specific landing pages convert ~8–12% against ~2–3% for generic ones**, which is why hot water gets its own page rather than a section; **trades and architects need opposite copy** (emergency intent converts 15–25% and emergency calls book at ~78% vs ~23% for general enquiries, so MVX chases volume — while for architects, qualifying copy with stated project minimums cut one firm's lead volume 22% and raised revenue, so CVA is judged on cost per booked project, never CPL); and **creative volume is the cheapest lever there is** (rotating 30+ creatives cuts CPL up to ~43%) which happens to be the exact thing 10x sells and does not use for itself. Full doc with sources, campaign structures, keyword sets, negatives and paste-ready Google RSA + Meta copy: `projects/lead-audit-2026-07-28/AD-STRATEGY.md`.

**Three pages built**, each self-contained, brand-scoped, mobile-first, nav stripped (ad pages leak through menus), form last, ≤4 required fields, each with a pre-launch checklist in its footer. **MVX hot water** reuses the proven aircon conversion system verbatim (League Gothic/Poppins, volt green, sticky call bar, licence strip) with the heat-pump STC rebate as the hook and the correct 4-field form written inline so the Formidable rebuild can't reintroduce the friction we're fixing on the other two pages; written for Route A (MVX partners a plumber) with every dependent line marked `ROUTE-A` for a one-edit swap to electrical-only. **CVA** is a monochrome architectural-editorial build with fonts and palette read off their own live site (Fahkwang + Poppins, no accent colour), offering a free 30-minute Site & Feasibility Chat, and it deliberately repels price shoppers with a project-minimum block for Cameron to fill. **10x Visuals** finally gets a lead form at all — brand blue, Montserrat/Poppins, offering the "Listing Film Test Drive" (one property, one film, fixed price, 72 hours) behind a three-field form, which converts a retainer decision into a trial an agent can accept without a meeting.

**Bugs and design tells caught during the build.** A nested `<!-- -->` inside the hot water page's instruction comment terminated it early and **leaked dev notes as visible body text at the top of the page** — found by looking at the render rather than the source, which is the whole argument for verifying visually. Also stripped an AI-tell side-tab accent border from the rebate card (the aircon page had already had one removed), dropped the 01/02/03 numbered section markers from CVA in favour of hairlines and headings (restraint is that brand's entire identity), and removed every em dash from user-facing copy across all three pages per the standing no-dashes rule. All three verified rendering in the browser.

**Everything is blocked on people, not on work.** Matt: plumbing route + confirmed rebate/price figures. Cameron: approve the feasibility offer, set the project minimum, release the June job's 19 stills and ~40 clips as ad creative — footage already paid for and sitting unused. Hunter: test-drive price, whether 72-hour turnaround is always deliverable, and which contact details 10x uses (the live site shows `tyson@`, the new page uses Hunter's number). No ad spend has been committed; the money rule applies to ad budgets exactly as it does to credits.

## [2026-07-28] lint | Impeccable audit + fixes on all three landing pages
Ran `/impeccable audit` across the three pages built earlier today, then applied the P1/P2 fixes. Scores before: MVX 15/20, CVA 16/20, 10x 16/20 (all "Good"). Impeccable itself updated 3.8.0 → 4.0.2.

**The finding that mattered: the eyebrow scaffold.** CVA carried a tiny uppercase tracked kicker above **9 of 9** sections and 10x above **7 of 7** — a 1:1 ratio, which is the definition of AI grammar rather than voice, and an explicit ban in the skill. Worse, it was the same reflex as the 01/02/03 markers caught and removed the day before, just one tier up. Stripped all 16 plus their CSS; headings and hairlines now carry the section cadence, which suits CVA's restraint identity better than the labels did. MVX was already clean (it inherits the client's League Gothic display heads).

**Broken imagery was real, and fixed with real client assets.** Verified by HTTP rather than eyeball: all eight `*-placeholder.jpg` references on CVA and 10x returned 404, so both pages were shipping image-free — a brand-register ban on image-led briefs. Scraped the clients' own live sites for actual project photography, verified each URL returns 200, and deliberately chose WordPress's **resized** variants so the image-weight finding got fixed in the same pass (CVA hero 363KB, tiles 74–129KB; 10x hero 155KB, tiles 76–135KB, versus 8–9.6MB originals). CVA now runs Dacelo, Beacons, Mudgeeraba and The Shed; 10x runs 88 Third Avenue, 25 Davenport Drive and Maker Build, with alt text and captions renamed to the real projects. MVX's two images were already live and 200 — no false positive filed — but MVX has **no resized variants on the server**, so its 444KB/512KB weights can only be fixed by uploading smaller files through WP.

**Contrast, computed not guessed.** Wrote a WCAG checker and ran every colour pair. Seven failures: input borders on all three pages at **1.41–1.56:1** against the 3:1 non-text requirement (WCAG 1.4.11) — and the form field is the conversion element on every one of these pages; MVX's rebate disclaimer at 4.23:1 (the one line with compliance weight was the least readable on the page); and 10x's muted body text at 4.23:1 on its own tinted section background. All fixed by walking a grey ramp to the first passing value rather than eyeballing. Re-verified: 0 failures.

**A regression I caused and caught.** Darkening `--tx-muted` to fix body text pushed the 10x figcaptions to 3.20:1, because those captions sit on the dark charcoal figure rather than on white. Re-checking after the change surfaced it; they were already failing at 3.43:1 beforehand and I had missed them in the audit pass because the pair wasn't in my list. Both pages' figcaptions now have explicit colours chosen for the surface they actually sit on. **Lesson: a token fixed for one surface can break another — re-measure every surface a token touches, not just the one that failed.**

Also: touch targets raised to 44px minimum (header/footer/in-body `tel:` links were 20–27px tall on phone-first pages); MVX's sticky call bar was overlapping content because `padding-bottom` was a hardcoded 78px against an 80px bar that also adds `env(safe-area-inset-bottom)`, now `calc(82px + env(...))`; dead `href="#"` logo links converted to spans on both pages (an ad landing page shouldn't offer an exit anyway); dead `--tx-navy` token removed; CVA stopped fetching two unused Fahkwang weights.

**Declared false positive:** the detector flags Montserrat as an overused font. It is 10x's locked brand face per DESIGN.md, and identity preservation outranks the reflex-reject list. Not changed.

**Systemic, still open:** the MVX token block is copy-pasted across three pages (aircon, electricians, hot water) so a brand change means three edits, and DESIGN.md documents only the PIL/Instagram graphics system — it says nothing about web surfaces, which is how the eyebrow reflex got in unchallenged in the first place. A shared web token layer plus a DESIGN.md web section is the fix.

## [2026-07-28] docs | DESIGN.md rewritten as a two-layer system (social + web)
Ran `/impeccable document`. The existing DESIGN.md described only the PIL/Instagram graphics system, which is why the eyebrow scaffold reached two landing pages unchallenged: there was no written web standard to check against. Asked Hunter rather than overwriting; he chose **merge, two layers**, plus keeping the detector hook on.

DESIGN.md is now the official DESIGN.md format: YAML frontmatter carrying machine-readable tokens (13 colours, 6 typography roles, radius/spacing scales, 6 component definitions) followed by the eight canonical sections. **North Star: "The Film House and the Front Door"** — the social layer is a film house (footage carries it, type is quiet), the web layer is a front door (its job is a phone call, not admiration). They share type, blue and voice and share nothing structurally. Everything from the old file survives: the six PIL formats moved into Layout, the scrim and shadow-ink values into Colors and Elevation, logos and imagery rules kept as trailing sections with a web-layer half added.

**Fourteen named rules** now carry the standing doctrine, most of them earned the hard way this week: the No-Eyebrow Rule (a kicker is a named brand system on social, banned as section scaffolding on web), the Four-Field Rule (four required fields, email is not one of them — written against the two live MVX pages that shipped with six), the One-Exit Rule (no nav, no menu, no linked logo, because every nav item is a way to lose a click you paid for), the Calls-Are-The-Leads Rule (track `tel:` clicks as the primary conversion or the platform optimises toward the weaker action), the Surface-Not-Token Rule (from the figcaption regression: re-measure every surface a changed token touches), the No-Side-Stripe Rule, the No-Dashes Rule, and the Not-Ours-To-Set Rule (client palettes are not owned in 10x's design file — MVX green and CVA monochrome live with those clients).

Also wrote the `.impeccable/design.json` sidecar (schemaVersion 2): 8-step OKLCH tonal ramps computed properly via a real sRGB→OKLab conversion rather than eyeballed, plus shadow/motion/breakpoint tokens and **8 drop-in components** with self-contained HTML+CSS including hover and focus states — primary and ghost buttons, the sticky call bar, input, conversion form card, nav-less ad header, work figure, and the trades licence strip. That set is now the reusable starting point for the next client landing page instead of copy-pasting an existing one.

Detector hook confirmed still on; it fired three times during today's build (side-stripe border, numbered markers, em dashes), which is the argument for keeping it.

## [2026-07-28] build | Landing page forms hardened — the conversion actually works now
`/impeccable critique` scored the three landing pages **19/32 (Acceptable)** and found what the technical audit had missed: the pages were beautifully dressed **shells**. Every form carried `action="#"`, `novalidate`, zero JavaScript and zero live regions, so a visitor could submit an empty form and get no error, submit a complete one and get no confirmation, and the data went nowhere. Three heuristics were dragging the score: Visibility 1, Error Prevention 1, Error Recovery **0**. All three were the same defect, which is why one fix moves ten points.

**Built the feedback layer on all three pages** (`/impeccable harden`). Plain-language errors beside each field in each client's own voice, never "invalid input": "We need a phone number to call you back", "Which suburb is the job in? It tells us how fast we can get to you", "Please add your name, so we know who we're speaking with". Errors clear the moment the person fixes the field rather than on the next submit, and they never rely on colour alone (text plus a glyph, 2px border, `aria-invalid`). Typed input is preserved in `sessionStorage`, which closes the Casey-persona hole from the critique: fill three fields, take a real phone call, come back and the form is still there. Double-submit guarded via `aria-busy`. Success replaces the form in place, takes focus, and names the next step and the timeframe. Send failure keeps the form filled and offers the phone. Error ink `#b3261e` and success ink `#1d6b3f` both clear 6:1 on every surface they appear on.

**Progressive enhancement, done properly.** The markup ships **without** `novalidate` so a no-JS visitor still gets the browser's own validation; the script sets `form.noValidate = true` at init once JS is confirmed running. Found this the hard way: with `novalidate` simply removed, native validation blocks the `submit` event before the handler runs, so the custom messages never rendered. The test caught it because it asserted on the messages rather than on "did it not crash".

**Real bug worth remembering: the HTML `pattern` attribute compiles as a RegExp with the `v` flag.** Under `v`, `(`, `)` and `-` are reserved inside a character class and must be escaped, so `pattern="[0-9+()\s-]{8,20}"` failed to compile and the browser **silently ignored the attribute entirely** — "abc" sailed through as a valid phone number. Escaped to `[0-9+\(\)\s\-]{8,20}` and re-verified: rejects `abc` and `123`, accepts `0412 345 678` and `+61 (07) 5555 1234`. A pattern that doesn't compile is not a strict pattern, it is no pattern, and nothing warns you.

Verified in-browser on all three: empty submit shows every message and focuses the first bad field, the screen-reader region announces the count (or the single specific message), a wrong phone errors alone while other typed values survive, fixing it clears the error live, valid submit shows "Sending…" then the success block, and the store is cleared. Endpoints are `data-endpoint="REPLACE_ME"`, which simulates success and logs a console warning so the states can be reviewed but nothing silently pretends in production.

**Open decision:** the detector hook now flags ~14 `design-system-color` / `design-system-font` findings on the client pages, because DESIGN.md declares 10x's palette while these pages correctly use MVX volt green, League Gothic and CVA's monochrome. That is the Not-Ours-To-Set Rule working as intended and the hook not knowing about it. Needs Hunter's call: ignore-file the three client pages, or accept the noise. Two of the findings **were** real drift of mine (an invented error tint and success tint) and were fixed by deriving both from existing tokens with `color-mix()`.

## [2026-07-28] polish | Real client brand guidelines applied — MVX polished, CVA corrected then parked
Hunter supplied the official **MVX Electrical Brand Guidelines v0.1** and **CVA Architects Visual Identity Guide v1.1**, plus real logo artwork for both. Both guides are now in `raw/`; logos in each project's `assets/`. This is what `/impeccable polish` step 1 is supposed to read, and it changed the work materially: I had been inferring both brands from their live websites.

**MVX brand violations found and fixed.** The palette and fonts I had inferred were correct (`#7EC004`, `#5E8519`, black/white, League Gothic + Poppins all match the guide exactly), but three rules were being broken. The guide states **"Green sits only on black or white, never on mid or light grey"** — the green submit button sat on a light-grey `#f7f7f7` card, the green area chip sat on the grey band, and the success block I built used a green-tinted background, which also breaks **"never a background fill"**. Card is now white, the chip is green-on-black, the success block is white. The page also had **no logo at all**, against "always use the supplied artwork, never re-typeset": added a black header with the white wordmark and the phone, no nav, and the plug device intact. Body size aligned to the official 16px. Added ARC L198354 and the approved **"15+ years"** trust asset to the licence strip.

**Copy fixed against "No fear, no urgency, no pressure tactics, ever."** The CTA band read "Showering in cold water right now?", which is manufactured urgency. Now "Hot water, sorted properly", leading with the outcome and the reliability as the writing rules require. ⚠️ Flagged for Matt: the whole page targets emergency search intent, so "Cold shower this morning?" in the hero *describes the situation the searcher typed* rather than inventing pressure. That reading is defensible but it is Matt's call, not ours.

**CVA corrected to its official brand, then parked on the boss's instruction.** The guide contradicted my inferred build on six counts, all now fixed: charcoal `#111111` (not `#1a1a1a`), dark grey `#333333`, mid grey `#737373`, light grey `#E6E6E6`; headings Fahkwang **Regular 400 at +25 tracking (0.06em)** where I had 300 at *negative* tracking; body font **Montserrat, not Poppins**; the official type scale (Display 3.5 / H1 2.75 / H2 2 / H3 1.25rem, Lead 1.125, Caption 0.8/300); and the logo is now the supplied PNG rather than a typeset wordmark, which the guide explicitly forbids. Because the palette permits **no accent colours**, CVA's validation errors are carried by charcoal type, a filled glyph and a heavier border instead of red. One real contrast consequence: official Mid Grey manages only 4.43:1 on the soft ground, so body copy on that layer steps up to official Dark Grey — both palette colours, no new grey invented. No further CVA work.

**A regression my own tests had missed.** Every error row was rendering permanently as a bare "!" glyph with no text, on all three pages, because **an author `display:flex` beats the `hidden` attribute**. My earlier tests queried `.mvx-err:not([hidden])`, which is attribute-based, so they passed while the page was visibly broken. Fixed with `.x-err[hidden]{display:none}` and re-verified by measuring **rendered height**, not attributes. **Lesson: assert on what renders, not on what the DOM says.**

**10x Visuals page parked too** — Hunter didn't like it, which matches the critique's own verdict that it was the most generic of the three. It needs a rebuild, not a polish.

## [2026-07-28] ingest | Paid ads diagnostic rulebook — method extracted from the dead investment-leads campaign
The 10x investment-leads campaign ran four days at $40/day and produced zero leads. Diagnosing it produced a method worth keeping, so the method is now [[paid-ads-diagnostic-rulebook]] and the campaign-specific numbers stay in [fb-ads-handoff.md](../projects/fb-ads-handoff.md).

The load-bearing idea is that **a zero is a different disease from an expensive lead**. Weak creative, a soft offer and mediocre targeting all still leak some leads through — they raise cost per lead, they don't zero it. So a hard zero across real spend points at the conversion path or the objective, and rewriting hooks first just burns another few days. Hence the fixed priority order: objective, then offer, then funnel mechanics, then creative — stop at the first thing actually broken.

Two mechanics in there earn their place. **Link clicks versus landing-page views** is the only column pair that exposes a broken or slow page, and it's invisible everywhere else. And **converting the benchmark into an expected lead rate** is what turns benchmarks from trivia into a diagnosis: at $40/day against a $30–60 investor CPL, a working campaign owes roughly one lead every 1–1.5 days, so four days at zero is structural, not variance. Same arithmetic run the other way would have said "leave it alone, scale it".

Benchmarks came out of a fan-out research pass with three-vote adversarial verification, and that layer paid for itself: a vendor's published real-estate CPC figures ran 2–6x better than independent aggregates and were **refuted** as market averages — a self-selected sample published as marketing. The vendor's CPL figure survived with caveats. Kept: AU real-estate CPM ~$30 (about 52% above global), link CTR ~1.68% in 2025 (down from 2.60%), vendor-lead CPL ~AU$48.71 median, generic real-estate CPL ~AU$26. Standing rule from this: a plausible number from a single source is not a fact, especially when the source sells the product.

⚠️ The CPL and CTR figures come from windows ending Sep 2024 and 2025 respectively, pre- or mid-Andromeda. Treat them as floors, and re-verify before they go in front of a client.

## [2026-07-28] optimize | MVX new-builds landing page — responsive images

`/impeccable optimize` on `projects/mvx-newbuild-lp/`. Measured first: the page was
shipping **431 KB to every visitor**, of which 395 KB was two 1600px photos and a
1181px logo PNG used for a 32px mark. A 390px phone was downloading all of it.

Fixed: hero converted from a CSS background to a real `<img>` with `srcset` and
`fetchpriority="high"` (a background image can't use `srcset` and isn't discoverable
until the CSS parses — and it's the LCP element), both photos wrapped in `<picture>`
with WebP plus a JPEG fallback, logo served at 64/96px densities.

Result, measured in the browser: **112.5 KB on a 390px phone at 2×, down 74%.**
LCP is now the hero image at 96 ms.

Two findings worth keeping:
- **AVIF was worse than WebP here.** Generated and measured, it came out larger at
  the sizes this page serves. Dropped it rather than shipping a third format for a
  negative saving.
- **A 750w step gets skipped.** 390px at 2× needs 780px, so the browser jumped to
  the 1200w file. Added an 800w step, which saves 27 KB on the most common phone.

Still open: the ghost-border alpha fix (`rgba(255,255,255,.1)` → `.4`) has not been
ported to the hot water and aircon pages, which inherited the 1.21:1 control
boundary. See [[mvx-electrical]].

## [2026-07-28] build | MVX new-builds LP — services tiered, form removed

Hunter's two calls on the new-builds landing page.

**Services now read as two tiers.** They were four identical editorial rows, so a
scroller could not tell what MVX actually does or which jobs matter. New builds,
renovations and extensions now run at display scale with a green rule and a scope
line; the smaller planned work is one dark strip underneath. The tier break is
carried by scale, surface and typeface role at once, so it holds without icons or a
fourth lookalike card.

**Form removed. The phone is the only action.** Every CTA is now `tel:0427593990`.
That also removed the `REPLACE_ME` endpoint, which was blocker #1 on this page and
would have shown a **fake success state** if it had ever shipped unwired, plus ~180
lines of validation JS and the whole error surface. 761 lines to 543.

The cost, stated so nobody is surprised: no out-of-hours capture. Someone scrolling
at 11pm can no longer leave details, so that lead now depends on them ringing. Worth
watching once Lach's call tracking is live, since calls are the only thing this page
can produce.

Three copy lines that referred to the form were rewritten, not left to contradict
the page: process step 01, the hero's "ring us instead", and the not-this-page note.

**Tooling note worth keeping:** headless Chrome on this Mac cannot verify a 390px
viewport. Asked for 390 it reports `innerWidth=500`, lays out at 500 and crops to
390, which is indistinguishable from the page overflowing. It produced two false
overflow findings here. Narrow-viewport checks go through the browser pane.

## [2026-07-28] build | MVX new-builds LP — FAQ closes the page, live photos

Two more of Hunter's calls.

**Closing call band removed, FAQ is now the last section.** Also fixes the rhythm
problem flagged an hour earlier: the page had been ending in three dark bands in a
row with no break, so it finished as one mass. Now grey, dark, footer.

**The page now ships zero JavaScript.** Removing the form took the validation
script; removing the call band took the sticky-bar observer, whose only job was
hiding the bar over that band. 761 lines at the start of the day, 511 now.

**Photos moved to live URLs on mvxelectrical.com.au** — `8166` hero, `283` rough-in.
Worth recording why they are not the URLs as given: the bare uploads are 2000px at
**2.4 MB and 1 MB**, which would have made this a ~3.5 MB page and thrown away the
morning's responsive work. WordPress had already generated 768/1024/1536 variants of
both, so `srcset` runs off those and the full file is never served. A phone at 2x
pulls ~212 KB of photo.

Still heavier than the 76 KB the local WebP set managed, because the origin has no
WebP at these sizes. The optimised set stays in `assets/` in case that weight is
worth reclaiming later.

**Measurement note:** cross-origin images report `encodedBodySize` 0 without a
`Timing-Allow-Origin` header, so photo weights have to come from the origin's
`Content-Length`, not from the page's own resource timings.

## [2026-07-28] build | MVX new-builds LP — chrome stripped, new number

**New MVX number: 0468 049 157.** Replaced 0427 593 990 in all four `tel:` links and
every visible instance on the new-builds page, prose in the FAQ included. Zero
occurrences of the old number remain. ⚠️ **The old number is still live on the hot
water, aircon and electricians pages** (8, 8 and 12 `tel:` links respectively) and
presumably across mvxelectrical.com.au and the Google listing. Ask Matt whether 0427
is being kept as a redirect or retired, because that decides whether those pages are
wrong right now.

**Header and footer removed**, so the page runs hero to FAQ. It reads as being
prepared for the MVX WordPress theme, which supplies its own chrome. Two side effects
recorded rather than left to be discovered: the **logo is now nowhere on the page**
(it only ever sat in the header and footer, so `assets/logo-white-*.png` are
unreferenced), and **one of the two licence placeholders went with the footer** —
only the trust-strip marker is left.

Also no phone number is pinned top or bottom now. Mobile has the sticky bar; a
desktop visitor mid-page has to scroll to a CTA to find the number.

The default 8px body margin, previously hidden behind the header, is reset as
`body:has(> .mvx-lp){margin:0}` so it fires standalone but does not fight the theme
once the page is nested.

Page is 476 lines, from 761 this morning. No JS, no form, no chrome.

## [2026-07-29] ingest | Zidane — Meta ads operator tips

Five verbal tips from a mate of Hunter's who runs Meta spend, relayed as a raw dump:
CBO, long videos beat short for VSL, turn text/visual improvements off, get a
pixel/dataset so it collects data, and a dynamic UTM parameter string.

Filed as [[zidane-meta-ads-tips]] with each tip decoded rather than transcribed, plus
a verdict table separating what confirms an existing decision from what is new and
untested. Two corrections made in the process. The pasted UTM string arrived corrupted
— a messaging client had auto-linked every `{{adset.name}}` into
`{{adset.name (http://adset.name/)}}` — so the working string is recorded clean. And
the UTM tip **does not apply to the MVX Meta rebuild at all**: that campaign uses
on-Facebook instant forms, which load no URL, so there are no parameters to populate.
It belongs on the Google Ads landing pages and any future website-destination Meta ad.

[[paid-ads-diagnostic-rulebook]] gained **Rule 8 — set up the measurement before the
campaign that needs it**, which is the gap these tips fill: the existing seven rules
all work backwards from a post-mortem, and dataset-first, enhancements-off and URL
tagging are all cheap before launch and unrecoverable after. [[mvx-electrical]] got a
dated work entry making the three pre-launch changes explicit, since the rebuild is
specced but unpublished — creative enhancements off is the one that would otherwise
have shipped wrong, because Meta rewriting ad copy would quietly remove the
scope-qualification wording and the bad leads would look like a targeting problem.

Long-form VSL is logged as a test, not a plan. It carries no numbers and came with no
account data, but it points at the one asset 10x can make better than any competitor
in trade services, so it earns an A/B slot against the four-angle ad set rather than a
rebuild around it.

## [2026-07-29] query | Meta dataset/pixel setup — and what it doesn't track

Hunter asked how to set up the dataset/pixel and whether it works for forms. The
answer split the question, because "forms" means two different things on this account
and only one of them involves a pixel: **on-Facebook instant forms are recorded by Meta
natively with no dataset at all**, while website forms need a dataset and a fired `Lead`
event. A pixel observes events on a website, and an instant form never loads the
website.

⚠️ **Correction to this morning's entry.** [BUILD.md](../projects/mvx-meta-rebuild/BUILD.md)
listed "dataset installed and the Lead event verified firing" as a pre-launch item for
the MVX hot water campaign — which is instant-form by design, so that event cannot
exist. Corrected in BUILD.md and in [[paid-ads-diagnostic-rulebook]] Rule 8, which now
carries the scope limit explicitly: diagnosing a dead instant-form campaign by checking
the pixel is looking in the wrong place. The tip from [[zidane-meta-ads-tips]] was
sound, it was scoped to the wrong campaign on the way in.

Audited the live site to see what exists: **no Meta pixel anywhere** on the homepage or
either Google Ads landing page. One Google tag (`GT-PLHFWDZJ`), no GTM container,
Formidable handling the forms. So Meta tracking starts from zero.

Filed [[meta-tracking-setup]] with the install path, and three decisions worth keeping.
**GTM is the recommended route** even though it adds a layer, because the same container
serves the Google Ads conversions [FORM-FIX.md](../projects/mvx-lead-fix/FORM-FIX.md)
already needs — one admin session fixes both platforms. **Lead events fire on
thank-you-page redirects, not on the form plugin's AJAX success event**, because the
event name belongs to the plugin and a silent rename looks exactly like a campaign that
stopped converting. And a **`tel:` click is not a call** — worth firing as `Contact` for
intent, never counted as a lead or reported to a client as calls received.

The separation that matters most: the pixel answers *did a lead happen*, and cannot
answer *was it any good*, which is the actual MVX problem. Lead quality runs through
offline conversions / CRM-connected CAPI — Lach's call tracking feeding statuses back,
which then unlocks "Maximise number of conversion leads". That path works for
instant forms; the pixel doesn't.

Everything here is blocked on the same wall as the form fix: client Business Manager,
WordPress admin, and DNS. Bundled into one ask rather than three.

## [2026-07-29] ingest | MVX video ad scripts + one-document shoot brief

Hunter briefed two Meta video ads for [[mvx-electrical]] — general electrical work and
new builds & renos — at 3 hooks, 1 body, 1-2 CTAs each, 20s casual, filming Monday
3 Aug. Also dropped a reference video (`Salisbury Talking Reel.mp4`, Drive). The link
resolves and the file is reachable, but audio can't be transcribed here, so the
reference went unused pending Hunter's call on a frame-only pass.

Wrote the scripts, then rewrote them twice on Hunter's direction. First pass read as
copywriting rather than speech; the brief was "easy for a tradie to say and what a
tradie would say". The fix was mechanical once named: **sentence fragments instead of
clauses**, noun lists cut to three items (reciting five sounds like reading), "sparky"
over "electrician" in the hook, "flick us a message" over "tap below", and one line
deleted outright — *"Building a house is about a hundred decisions"* was writer voice,
not a bloke on site. The most valuable line in the brief turned out to be a delivery
note rather than ad copy: *don't learn it word for word, say it how you'd say it, change
any word that feels wrong in your mouth.* A tradie reciting is worse than a tradie
paraphrasing.

Then Hunter asked for one document, as a PDF, instead of the three audience-split
markdown files. Built `brief.html` → Chrome headless → `MVX-Video-Shoot-Brief.pdf`,
six A4 pages covering the lines, delivery, shoot plan, camera/sound/light,
close-ups, file handoff, edit spec and a pre-Monday checklist.

Two rendering faults were caught only by rendering the PDF and looking at it, not by
the HTML. The masthead used negative margins to bleed off the page edge and **Chrome
clipped it instead of bleeding** — the logo and the first letters of every headline
were cut off. Contained the band inside the page margins instead. And
`break-inside:avoid` on the ad cards had shunted each one to its own page, leaving
three half-empty pages; removing the forced breaks and making page 1 a deliberate cover
fixed it. Lesson worth keeping: **an HTML→PDF job isn't done until the PDF has been
read back page by page.** Both faults were invisible in the markup.

The impeccable hook flagged 16 palette and radius findings against DESIGN.md. Left
unchanged and recorded as out of scope rather than suppressed: DESIGN.md is the
web/landing-page system, specified in px with button, form-field and iOS-zoom rules,
and this is an A4 print document in mm. The DESIGN.md rule that does bind here is the
Not-Ours-To-Set Rule — the document uses 10x blue, not MVX volt green, because it is a
10x deliverable. That holds.

## [2026-07-29] lint | Reconciled the MVX campaign specs; drafted the asks for Matt

Two follow-ons from the video brief, both unblocking work rather than adding any.

**Reconciled the contested settings.** [BUILD.md](../projects/mvx-meta-rebuild/BUILD.md)
and [BUILD-NEWBUILDS.md](../projects/mvx-meta-rebuild/BUILD-NEWBUILDS.md) disagreed on
location setting, Advantage+ audience and Advantage+ placements. That's a defect rather
than a difference of view: those three describe MVX's service area and audience, so they
cannot correctly be ON in one campaign and OFF in another for the same business. Filed
[ACCOUNT-SETTINGS.md](../projects/mvx-meta-rebuild/ACCOUNT-SETTINGS.md) as the single
source, with both build sheets now pointing at it so the conflict can't quietly return.

⚠️ **Corrected an attribution I had wrong.** BUILD.md listed Advantage+ audience among
the causes of the out-of-area leads. Advantage+ audience can exceed the interests, age
and gender you specify, but **location is a hard boundary it does not cross** — so
Sydney and Canberra came from the location dropdown ("living in or recently in", Meta's
default), not from audience expansion. BUILD-NEWBUILDS had the better analysis of the
two and its reasoning is the one carried forward. The geo fix is the locked location
setting; Advantage+ audience is a separate and much lower-stakes question that was never
the root cause. Recommendation is ON with the cost-per-result goal and the form
questions carrying lead quality instead, but either answer is defensible — what isn't is
different answers per campaign, which would make any quality comparison meaningless.
Placements resolved to ON, partly because the creative is now 9:16 vertical built for
Reels and Stories.

⚠️ **Also surfaced: total daily spend is unbudgeted.** Hot water $40/day + new builds
$20/day + anything for general electrical is $60+/day, against ~$18/day across the two
old campaigns. Nobody has agreed to triple the spend. Needs a number before more than
one campaign publishes.

**Drafted the asks for Matt** —
[MATT-ASKS.md](../projects/mvx-meta-rebuild/MATT-ASKS.md), not sent. Eight things were
waiting on him across the shoot, the campaigns and the tracking, which is about six too
many for one message. Split into a same-day text covering only Monday's shoot (site
access, call time, wardrobe, the two flagged script lines) and a call this week for
access plus the three decisions. A tradie answers three texts and ignores an eight-point
email. Also dropped the DNS request from the access ask — domain verification can be
done with a header tag, which the WordPress access already covers, so it was a
needless third thing to chase.

## [2026-07-30] ingest+harvest | 10x Visuals homepage rebuilt on Prestige DS v1.0

Hunter supplied `10x-prestige-design-system.html` (Prata + Montserrat, paper/night, blue as
accent only, one expo curve) and asked for the 10xvisuals.com.au homepage rebuilt to that
standard. Built static and self-contained at `projects/10x-site/`; not deployed. New page
[[10x-website]], indexed. Spec and full build outcome in
`docs/superpowers/specs/2026-07-30-10x-homepage-prestige-rebuild-design.md`.

Five things the vault did not know before:

1. **Prestige DS v1.0 fails WCAG AA in four places**, including its own text blue at 4.39:1.
   Amended and recorded in DESIGN.md as The AA-Amendment Rule; 11 text pairs now measure
   4.68:1 to 6.69:1 with no failures.
2. **⚠️ The DS contradicts DESIGN.md.** It prescribes a tracked kicker plus an oversized roman
   numeral on every section; DESIGN.md's No-Eyebrow and No-Numbers Rules already forbade both
   after two pages were stripped for it earlier in July. Resolved for the learned rule.
   New rule: a system handed down does not outrank a rule the vault learned from shipped work.
3. **Never gate content visibility on JS.** The first reveal pass hid below-fold sections until
   an IntersectionObserver fired, so a deep link to `#close`, which the hero CTA itself points
   at, could land blank. Now armed only when the observer exists, after any anchor scroll
   settles, with a 2.5s failsafe.
4. **Mismatched client logos read cheaper than type.** Recorded as The Roster-Not-Logos Rule.
5. **Judge a photo at full resolution before committing.** The hero was picked off a thumbnail
   for a "dark bottom third" that is actually a bright white roof.

Corrected a wrong vault claim: [[lead-gen-engine]] said 10xvisuals.com.au had no lead form at
all (27 Jul). It has one at `/contact-us/`; the problem is seven fields with a required
free-text message, not absence.

Weight went 6.09MB all-eager to 3.81MB with 634KB above the fold. Anti-pattern detector clean,
0 findings from 17. Zero cost, nothing paid was touched.

## [2026-07-30] ingest | Stonehaven becomes the 10x homepage hero

Hunter flagged the [[sol]] drone cover as not strong enough and asked for the Stonehaven
(47 Somerset Drive, Whitefox) frames instead, plus SOL moved below Elysium. Done: hero is
now the Stonehaven dusk frame, work run is six entries (Stonehaven, Davenport + Bespoke,
Elysium, SOL + Broncos), Whitefox added to the client roster in place of Hour Glass, which
was never verified. Stonehaven has no project page on the live site, so that entry is
deliberately unlinked rather than pointing at a 404.

Two lessons worth keeping, both on [[10x-website]]:

- **A hero is chosen by where the dark is.** SOL is a better photograph and a worse cover:
  its lower third is a bright white roof, exactly where the headline sits. Stonehaven's
  foreground lawn is dark, so ivory type lands in real shadow. Judge the tonal map of the
  region the type occupies, not the image.
- **Burnt-in marketing graphics.** The first White Fox files were all `Whitefox Mappins-*`
  with a map pin composited into the frame, which DESIGN.md bans. Filenames naming a
  marketing treatment rather than a shot are suspect.

Also fixed two rendering errors Hunter spotted, added the scroll animation layer (staged
reveals in reading order, masked heading rise, generalised parallax), and caught a third
bug while testing it: the close background was flush at height 100%, so parallax travel
would have exposed a bare edge. Zero cost, nothing paid was touched.

## [2026-07-30] design+build | 10x site: competitor review, project lightbox, pages restored

Hunter asked to review desirestudio.com.au and x-media.com.au and pull the premium interaction
patterns into the 10x rebuild, then bring the five interior pages back at the same standard.

Real bug the competitor review surfaced: mobile nav had collapsed to a single Contact link,
with no way to reach the other four pages without going through the enquiry form. Replaced with
a full-bleed overlay menu (text "MENU"/"CLOSE" triggers, not a hamburger), real dialog semantics,
focus trap, Escape close, scroll lock. Added a scroll cue and magnetic-pull CTAs as tasteful
translations; explicitly rejected Desire Studio's 3D drag-balloon hero as off-brand.

Built the headline feature: a project lightbox where the clicked work photo's own image element
is measured and animated via transform (FLIP technique) into a fullscreen preview, rather than a
generic modal fading in over it. Real links pass through untouched on modifier-click.

Restored all five interior pages via a generator script (projects/10x-site/scripts/build_pages.py,
checked in), elevated to the homepage's post-rework standard: one statement-scale heading per
page in an editorial split, no repeated hairline eyebrows, left-aligned close sections.

Two real bugs caught mid-build, both patterns already in [[10x-website]]: the lightbox's
"View full project" link inherited paper-tuned blue and measured 3.1:1 on its own night
background (fixed, now 7.07:1); and a test script itself measured a page's on-paper close
section against the wrong background, producing a false 1.02:1 failure. Full writeup on the page.

Zero cost, nothing paid was touched.

## [2026-07-31] build+harvest | 10x site: SOL scaffold, FORM fix, hero copy — partial release committed

Ran as a formal ticket pack (ENG-01/02/09/10), one ticket at a time, in implementation mode.

ENG-01 scaffolded scripts/build_case_studies.py and sol.html (empty sequence, no quote —
real branches, pending real shoot frames). ENG-02 stayed correctly blocked on CONTENT-01:
checked raw/, an external SSD, Desktop, Downloads and the live WP /sol/ page, found nothing
usable, reported blocked rather than inventing placeholder imagery.

ENG-09 added the contact-funnel line "We'll only use this to reply." and, in doing so,
surfaced a real three-way FORM duplication (build_pages.py, a byte-identical copy ENG-01 had
introduced in build_case_studies.py, and index.html's hand-written inline copy). Fixed by
having build_case_studies.py import FORM from build_pages.py, which exposed a real mechanical
hazard: both generators' write loops ran unguarded at module level, so the import would have
silently regenerated every page. Both are now guarded behind `if __name__ == "__main__":`.
index.html's copy stays a documented hand-synced exception.

ENG-10 added a value-restatement line under the hero lede on the four service pages only,
via a new optional value_line param on hero(), reusing the existing .lede-h class. No new CSS
anywhere in this pass.

Assessed release readiness explicitly rather than assuming: not ready for the full release
(5 of 6 case studies don't exist), ready for a partial one. Shipped home + 4 service pages +
contact-us as commit 2e7610f, 9 files staged deliberately. Deploy has nowhere to go yet — no
hosting pipeline exists in this repo; asked Hunter rather than guess, he chose local-only.

Real should-fix, not blocking: the homepage's five case-study tiles link to routes with no
backing page at all, harmless with JS (the lightbox intercepts the click, confirmed live) but
a dead end for no-JS/crawlers. Pre-existing from the lightbox build, flagged not fixed.

Zero cost, nothing paid was touched.

## [2026-07-31] build+harvest | 10x site: video heroes, React widgets, all six case studies shipped

Continued the same session's ticketed pass. Added video heroes to home and SOL
(Hunter's own footage, transcoded down from 4K/120-180MB to ~12MB 1080p; both
re-edited once, final as of today). Fixed three real client-list errors: founders
caption order was wrong (now Tyson/Damon/Lachlan matching the actual photo), Hill
Interior Linings dropped (no longer a client), Ocean Shores renamed to Coastlife
Constructions and moved into the correct category.

Hunter asked for two specific components from a pasted shadcn registry snippet
(3D carousel, hover gallery) — a different stack (React/Tailwind/TS/shadcn) from
this static Python-generated site. Flagged the mismatch and the stock imagery in
the pasted code rather than silently reinterpreting the ask; got explicit
confirmation the real stack was wanted; built it properly at projects/10x-site/web/
via the actual shadcn CLI, real project photos swapping out the Unsplash/picsum
stock, compiled to a self-contained bundle the static site just loads via
<script>/<link> tags.

Hit two real Tailwind v4 bugs, not user error: the content scanner silently skips
digit-leading filenames (3d-carousel.tsx renamed to carousel-3d.tsx), and splitting
the import to skip preflight silently breaks scanning entirely, independent of
that. Both isolated by bisection against a minimal test file before landing on the
fix (@import "tailwindcss" prefix(tdx), with tdx-widgets.css loaded before
prestige.css so the host page's own styles win any cascade tie).

Hunter's call: ENG-02 (SOL image sequence) is closed, not left blocked — SOL ships
with the video instead. Checked and confirmed the other five case studies were in
the identical single-photo, no-sequence situation, and built them anyway to the
same honest standard: real photo, real reused copy, no fabricated sequence or
quote. All six case-study pages exist now. Fixed the homepage work-grid tiles,
which pointed at routes with no backing page, to link to the real files; Stonehaven
previously had no link at all and now does too. Confirmed the JS lightbox still
intercepts every click; this only fixes the no-JS/crawler fallback.

Zero cost, nothing paid was touched.

## [2026-08-03] update | Board headshots delivered, Lot 48 confirmed closed
Hunter confirmed two jobs done. **Board Committee headshots** — 127-RAW cull/retouch pass finished, hero portraits delivered; [[board-committee-headshots]] status bumped, BTS edit remains open (now unblocked — its reveal cut needed a finished portrait). **Belle Property Lot 48** — reconfirmed delivered (already marked so on 21 Jul; [[belle-property]] + index one-liner were stale, pointing at "awaiting run it" — fixed). 10x-site work (bespoke case-study page + wrap) targeted to finish today; tracked as a personal to-do.

## [2026-08-03] lint | Graph connectivity pass — CLC pack wired, remaining orphans fixed
Hunter reported the vault "grew crazy," asked to connect all the nodes. Full orphan/dead-end sweep across all 92 wiki pages (inbound-`[[wikilink]]` count per page).

**The big gap: the whole CLC source pack was disconnected.** All 8 `clc-*.md` files under `wiki/sources/` already pointed *out* to [[clc-pack-readme]]/[[clc-profile-audit]], but every cross-reference between sibling files ([[clc-pack-readme]]'s own file table, `00_profile_audit.md`, `brand_voice.md`, `strategy_guide.md`, `pinned_posts.md`, `master_playbook.md`) was plain backtick filenames, not `[[wikilinks]]` — so nothing linked back in and the pack read as 8 separate islands to any graph view. Converted every one of those refs to real wikilinks across [[clc-pack-readme]], [[clc-profile-audit]], [[clc-master-playbook]], [[clc-brand-voice]], [[clc-strategy-guide]], [[clc-prompt-library]], [[clc-field-research-2026-07-07]], [[clc-swipe-file-2026-07-07]], and [[coast-life-constructions]] itself (its pack table + next-actions list had the same filename-not-link problem). Also linked the two live-research files ([[clc-field-research-2026-07-07]], [[clc-swipe-file-2026-07-07]]) into the readme's table — they postdate the original Fable 5 zip and had never been listed there.

**Other true single-inbound-link pages, fixed:** [[jang-studio]] was named in prose (not linked) from [[photo-editing-pipeline]]'s offshore-handoff section — now a real wikilink. [[rclone-drive-upload]] only had index + [[higgsfield-pipelines]] pointing at it — added it to [[archiving-and-backup]]'s cloud/offsite section, the natural craft-layer home for a delivery-upload tool. [[damon]] and [[tyson]] were bio stubs with no lateral team links (only [[hunter]] cross-referenced [[kris]]) — added a Team line to both matching the roster pattern.

Left alone as correctly sparse, not broken: [[elevra-invoices]], [[strategic-investing-qld-brief]], [[weekly-review-2026-07-17]] — dated ops/source docs naturally have few inbound links and were already reachable from their owning client/project page. Confirmed the new untracked `projects/10x-site/*.html` case-study pages (bespoke, davenport, elysium, stonehaven, broncos) are already fully documented in [[10x-website]] — not a wiki gap, just uncommitted files.

## [2026-08-04] ingest | Bespoke Estate Agents — real photos found for the live site, fake listings removed
Lach's actual current build for `bespoke.agents.10xvisuals.co` is plain HTML/CSS/JS pasted into Elementor HTML widgets, separate from every prior Bespoke build attempt (ElementsKit demo, hand-built theme, static concept, Phase 2 prototype). Saved as source of truth at `projects/bespoke-elementor-source/`. Found and fixed: the About page was a byte-for-byte duplicate of Services (no real About copy exists, still open); three of five "estate/campaign" listings (The Boulevard, Paradise Waters, Monaco Street) had no real photography behind them and were removed rather than left as fake sold-listing claims; the other two (43 Northview, 11 Cairngorm Street) got their real shoots swapped in from Hunter's brand-kit folder and Downloads, and Northview's "Sold" tags were corrected to "For Sale" (it's a current listing, not sold). Every remaining stock/placeholder image sitewide — page heroes, CTA backgrounds, the hero video itself — replaced with real photos or a real transcoded video. 14 photos + 1 video uploaded to Bespoke's WP media library via REST API. Two items still open: `team-ward.jpg`'s authenticity unconfirmed, and two stock backgrounds live only in the site's own inline CSS (unreachable via HTML-widget paste, needs a direct Elementor Custom CSS edit). Full detail in [[bespoke-estate-agents]].

## [2026-08-04] ingest | 10x Website round five — real pillar photography, carousel galleries, WordPress media migration
Replaced all four pillar-hero placeholders with real/premium imagery: Branding got a from-scratch business-card mockup (real [[bespoke-estate-agents]] wordmark, perspective-composited via OpenCV onto a stock concrete-tile photo — corrected once from the wrong sister-brand logo), AI Systems + Content pillars got real 10x BTS photos, Lead Gen got a re-picked free-licensed stock cover after rejecting the cliché "Search Console" screenshot. Converted case-study photo galleries (Salisbury/Stonehaven/Elysium/Davenport/Broncos) from a full-page `.pg-grid` to an edge-to-edge horizontal-scroll `.pg-strip` carousel per Hunter's explicit "too much on one page" call — lightbox untouched. Got WordPress REST API media upload working (app-password auth; first attempt 401'd on a display-name username, the actual account email worked), uploaded all 24 new pillar images, cleared `LOCAL_ONLY` in `build_pages.py`. Full-site link sweep: 87/87 remote WP URLs + 995/995 local asset paths resolve. Deploy decision made (previously open): Hunter deploys the static files himself as a same-domain bypass, WordPress theme port deferred as its own future job pending Lachlan's WP header/footer/menu work. Full detail in [[10x-website]].

## [2026-08-06] query | Urban Core construction site — slow-push video prompt, dolly-vs-zoom redo loop
Wrote a Seedance-style push-in prompt for an unfinished commercial fitout interior (concrete ceiling, ductwork, glass-balustrade stairwell), then iterated the redo loop across three tools as Hunter switched: Higgsfield Seedance (flat zoom, no parallax — fixed by naming a near/far differential-speed anchor), Kling (bobbing — fixed by adding explicit locked-off/no-rotation language, then again after a second bob by dropping Custom Camera Control), Cinema Studio 3.5 (still bobbed on "Push In" — root cause: Push In is FOV/zoom-style, **Dolly In** is the physical-translate preset; once identified, final prompt was pared to scene-only description so it wouldn't fight the preset's own camera handling). No JOB.md exists for this job yet — small/no-cost prompt-only session, not logged as a full 10x job.

## [2026-08-10] build | MVX General Electrical — Meta calls campaign built off the 3 Aug shoot
Hunter reported MVX not getting ads/leads, then supplied the shoot footage. Five files, **three of them ads**: talking-head cuts at 10.1s/12.3s/15.2s, all 1080×1920, same shirt and location, interchangeable — one angle (the General Electrical "list" frame) varying only the hook, as [VIDEO-SCRIPTS.md](../projects/mvx-creatives/VIDEO-SCRIPTS.md) designed. The other two (Green Power Boxes, Broadbeach Library) are commercial project pieces, wrong audience for a homeowner lead campaign, routed to organic. Setup B never happened, so there is still no new-build footage and [BUILD-NEWBUILDS.md](../projects/mvx-meta-rebuild/BUILD-NEWBUILDS.md) stays unbuilt.

**The finding that drove everything: all three cuts end on "give us a call", not "tap below."** Conversion location locks at publish, so the mechanism had to match the creative rather than the other way round. Hunter's call: **Calls**, **$50/day**, **Advantage+ audience ON** — which also closes the last open item in [ACCOUNT-SETTINGS.md](../projects/mvx-meta-rebuild/ACCOUNT-SETTINGS.md), now locked account-wide instead of differing per campaign.

Choosing calls deletes the instant form and every qualifier specced in [BUILD.md](../projects/mvx-meta-rebuild/BUILD.md), so quality control was relocated rather than dropped: the ad set optimises for **quality calls (≥60s)**, which measures commitment where the budget-band question only asked about it. Structure supersedes BUILD.md's five-ad-set floors *for this campaign only* — three hooks on one angle are judged on link CTR and thumbstop, both impression-normalised, so equal spend buys nothing and one ad set concentrates the learning. Two risks the form spec never had, both flagged not hidden: Meta allows dayparting only on a lifetime budget (launching 24/7 deliberately, hour-of-day breakdown at day 7 decides), and a missed call is a wasted click with no record — blocks on Matt confirming who answers the phone. Build sheet: [BUILD-CALLS.md](../projects/mvx-meta-rebuild/BUILD-CALLS.md). Zero cost, nothing published yet.

## [2026-08-10] lint+build | MVX Meta — account inspected, three unlogged campaigns found, calls campaign built
Follow-on from the morning's build sheet, this time with Ads Manager open (Chrome, Hunter's session; every irreversible step his call). **The vault's picture of the account was wrong.** Three August campaigns — General Electrician, Air Cons, New Builds — were already live at $40/day between them and had never been logged anywhere. Meanwhile **Aircon Push (July) had been switched off**, though [BUILD.md](../projects/mvx-meta-rebuild/BUILD.md) explicitly said keep it as the control. Old two campaigns: 14 leads @ $42.84. New three: 5 leads @ $101.19. The rebuild was running at 2.4× the cost per lead of the thing it replaced, with the only proven performer dark. Cause was **$40/day split three ways** — each pool far under the ~50 weekly conversions Meta needs, so none could ever leave learning ([[paid-ads-diagnostic-rulebook]] Rule 5). Not creative, not targeting.

**Four findings that change how these get built.** (1) An **Advantage+ leads campaign cannot be set to "people living in this location"** — Meta removes the control entirely, so the setting [ACCOUNT-SETTINGS.md](../projects/mvx-meta-rebuild/ACCOUNT-SETTINGS.md) locked as non-negotiable was never applicable to any of the three. (2) That dropdown appears **retired account-wide**, replaced by Controls ("we won't reach people beyond these, even with Advantage+ on" — locations, min age) vs Suggestions (soft, Advantage+ overrides). Location is already hard; the hunt for the dropdown was the wrong instinct. (3) **The real out-of-area leak is a default-ticked checkbox under the map, "Reach more people likely to respond to your ads"** — serves to anyone *interested in* the region, anywhere in the country. Unticked; needs checking on every other ad set. (4) **Radius defaults to +40 km**, which by itself put the audience back at 3.9–4.5M, the exact July failure number.

Also learned: no call-duration performance goal exists on this account (so the calls campaign's specced quality lever doesn't exist, and no cost cap was set — a $45 cap binds on nothing when a tap costs $10–25); ad scheduling *is* available on a daily budget for a Calls conversion location, so Mon–Sat 09:00–18:00 is set; min age caps at 25 not 30; "multi-advertiser ads" is on by default and crops creative; and Meta's AI creative step offered **a man who isn't Matt** for an ad whose whole premise is owner-led — zero AI creative selected anywhere.

Changed live: Aircon Push back ON ($10), Air Cons Aug OFF, General Electrician Aug OFF, New Builds untouched ($20). Built as drafts for Hunter to publish: `MVX | General Electrical | Calls | Aug 2026` ($20/day, Calls, 2 ads) and `NB-Renos-Video` inside the existing New Builds campaign. $50/day total once published. Full record and Lachlan handoff: [ACCOUNT-STATE-2026-08-10.md](../projects/mvx-meta-rebuild/ACCOUNT-STATE-2026-08-10.md). Zero cost. Open: Matt on who answers the phone, publish, SMS verification on the New Builds form, 4:5 crops.

## [2026-08-10] correction | MVX General Electrical rebuilt from calls to forms, same session
Correction to the entry above, and the reason is worth keeping: Hunter, on being told the new campaign puts a Call Now button in front of Gold Coast homeowners — *"wouldn't a form be better cause he is bad at answering the phone?"* That inverts the case for calls. A calls campaign makes Matt's phone habits the product: a missed ring is a paid click with **no name, no number, no record** and nothing to follow up, where a form lead simply waits in the inbox. Switched. Free to do only because **conversion location locks at publish, not at build** — an hour later it would have meant a full rebuild.

**What the switch cost, all verified in the UI:** it **silently wiped the video and all copy from both ads** with no warning, so both were rebuilt from scratch (rule: *set conversion location before building ads, never after*); it removed the whole Ad scheduling section, so the Mon–Sat 09:00–18:00 schedule is gone — **dayparting on a daily budget turns out to be a calls-campaign privilege**, and no real loss since that schedule existed only to stop the phone ringing when nobody could answer; and it leaves Matt saying "give us a call" over a *Get quote* button, a knowing mismatch softened by keeping the form's "Call Matt Directly" action. One ad then failed validation with a phantom **WhatsApp error (#2446880)** despite WhatsApp being unticked everywhere visible — it had been duplicated while the campaign was still on Calls and carried state the form UI can't display or clear; deleted and re-duplicated from the clean ad. Rule: *if a stale error survives every visible setting, the object is carrying state from a previous conversion location — rebuild it.*

**Form:** a purpose-built qualifying form was started — **Higher intent** (review step) and, importantly, **Flexible form delivery OFF**, a default-on setting that lets Meta *remove your qualifying questions* to lift volume and would have silently deleted the whole quality strategy. Discarded unsaved on Hunter's call to reuse existing forms. Hunter also correctly killed its opening question: *"why does it matter if you own the property, only people who own would be doing it"* — right, ownership is a hot-water qualifier where a renter can't authorise a $3k system swap; on a fan or a powerpoint it filters nobody and property managers are real buyers. ⚠️ Consequence to watch: the campaign now runs **the same form the old General Electrician campaign used when it produced 1 lead at $125**. Different creative and geo, so not a like-for-like repeat, but it is the first suspect if week one is junk. Final state: `MVX | General Electrical | Leads | Aug 2026`, instant forms, $20/day, 2 ads, still **in draft**. Record updated: [ACCOUNT-STATE-2026-08-10.md](../projects/mvx-meta-rebuild/ACCOUNT-STATE-2026-08-10.md) §3a.

## [2026-08-10] audit | Claude setup, vault security, dead automations
Full audit of the Claude Code install on Hunter's request, after a session installing Agent Reach (15-platform internet access for agents) and Emil Kowalski's 9 UI/animation skills. New page: [[claude-code-setup]]. Two red findings, both fixed in-session.

**The AIOS dashboard was serving the vault to the LAN.** `server.mjs` called `server.listen(PORT)` with no host argument — Node binds `0.0.0.0` in that case — so `http://<lan-ip>:8770` was open to any device on the network with no auth at all. That exposed `/api/data` (a full vault scan: client names, jobs, credits, follow-ups) and, worse, `POST /api/run`, which spawns headless `claude -p` with `Read,Write,Edit` and `git push` allowed. Prompts come from local files so an attacker could not inject arbitrary instructions, but they could trigger any registry action and make an agent write to the vault and push to GitHub. Live that way since the dashboard shipped in July. Bound to `127.0.0.1`, restarted, verified (localhost 200, LAN refused) — `cdac0f6`.

**Every scheduled loop had been silently dead.** All four launchd agents failed identically on `/bin/zsh: can't open input file`. Root cause is macOS TCC, not a path bug: under launchd `/bin/zsh` has no access to `~/Documents`, so it could `cd` into the vault and pass `[[ -r file ]]` but hit `Operation not permitted` on the actual read. `node` is already permitted — which is exactly why the dashboard worked while every clock-triggered job did not, and why the discrepancy went unnoticed. Consequence: no morning brief, no nightly lint, no weekly review for at least a week, and no failure notification either, because the script died before reaching its own error trap. Fixed by moving the runners to node — `bin/run-action.mjs` replaces `run-action.sh`, `bin/run-shell.mjs` pipes the maintenance script into `zsh -s` so zsh never opens the protected path — plists repointed, reloaded, verified under launchd with a throwaway probe agent (`3c20adf`). First real run is tonight's 21:57 lint.

Diagnostic worth keeping: **a passing `[[ -r ]]` test is not proof a read will succeed** — `access(2)` is not blocked by TCC, only the read is. Green permission check, failing `cat`.

Clean elsewhere: vault repo private, tracked-file secret scan clean, `.gitignore` correctly holding back invoice bank details; gh token scoped `repo, workflow, read:org`; 3 MCP servers all known (10x-crm still needs re-auth); 35 skills, only 3 ship executable code and none auto-runs; one hook (impeccable); no permission allowlist, so everything still prompts — kept deliberately, since that friction is what stands between an unattended loop and credit spend. Open risk, not fixed: **Obsidian has no Git or Sync plugin**, so vault backup depends entirely on a Claude session remembering to commit. Zero cost.

## [2026-08-10] lint + harvest | graph orphans, four unharvested folders, vault backup loop
Triggered by Hunter's Obsidian graph view: a wide ring of unconnected dots around the knowledge cluster.

**None of them were wiki pages.** The knowledge layer is fully connected — all 99 wiki pages have inbound and outbound links. The 125 isolated nodes were Obsidian indexing things that are not notes: 52 vendored skill files under `.agents/skills/`, 34 under `.github/skills/` (the Copilot target of the impeccable installer, commit `493ab7a` — **not** a stray duplicate, and left in place), tool scratch under `.impeccable/`, and `projects/` build docs. Fixed by excluding those dirs in `.obsidian/app.json` `userIgnoreFilters` (tracked, so it follows the vault), not by inventing links: **125 isolated → 17**, and the 17 that remain are real `projects/` documents rather than tooling.

**Four project folders had no mention anywhere in `wiki/`** — the leak CLAUDE.md warns about. Harvested: `10x-site-for-lach` and `10x-site-media-export` into [[10x-website]] plus a real [[lachlan]] page (the export strips header/footer for the theme to supply, and deliberately ships almost no media because it points at the live WP library); `bespoke-sold-popups` into [[bespoke-estate-agents]] (delivered 9:16 + 16:9, ProRes 4444 and HEVC alpha, 0 credits); `giovanni-onboarding` into a new [[giovanni]] page.

Two lessons pulled out of those folders rather than left in a JOB.md. From the pop-ups: **a blocked reference is a blocker, not a licence to guess** — the first build was made from a *description* of the reference reel because Instagram's login wall blocked the browser, and it was structurally wrong in every respect; `yt-dlp` plus 2fps stepping showed the real treatment and the rebuild matched it. From the SOP: preserve-fixtures has now been written out in plain English for a new starter, alongside **stop after two failures, do not try a third**, which is the cost gate stated as a training rule.

**Vault backup loop added.** Obsidian has no Git or Sync plugin, so the vault was only ever backed up when a Claude session remembered to commit. New `com.10x.aios.vault-backup` launchd agent runs `bin/vault-backup.mjs` hourly — commits anything dirty, pushes, and also pushes commits a session left behind. Node again, for the TCC reason in [[claude-code-setup]]. Verified: first run committed and pushed on its own. It deliberately does **not** rebase on a diverged remote; it logs and waits for the next hour.

Also fixed this session, before the graph work: the AIOS dashboard was **CSRF-able from any website Hunter visited** — loopback binding stops the LAN, not the browser, and a `text/plain` form post skips the CORS preflight, so `/api/run` (headless Claude with write + push) was reachable cross-site. Mutating requests now require a same-origin-or-absent `Origin` and a JSON content-type; verified refused from a spoofed origin under both content types. See [[claude-code-setup]] and [[agentic-os]]. Zero cost.

Not done, deliberately: the `.git` directory is 1.3GB against 1.1GB of tracked files (two ~40MB hero videos, a 41MB JPG, a 43MB PDF). Shrinking it means rewriting history and force-pushing to the only remote that backs this vault up, and the media in question are real assets — the rewrite would strip them from the repo, not just from history. Left alone as slow-but-correct.

## [2026-08-10] query | Sans serif research for O'Neill Group

Hunter asked for sans serif research without knowing what the term meant, for client work on
**O'Neill Group**. No such entity exists in the vault — the only O'Neill on record is Brian O'Neill
of [[strategic-investing-qld]], whose Quiet Equity system already runs Marcellus + Inter. The work
was written against that system with the mismatch flagged rather than assumed away, on both the
deliverable and [[typography]].

Built a specimen sheet rather than a list of font names: eight free faces, each **rendered in
itself** via base64 `@font-face` data URIs (17 latin woff2 faces, 500KB, embedded because the
artifact CSP blocks font CDNs), all set in identical real client copy so the only variable is the
typeface — [sans-serif-shortlist.html](../projects/oneill-group-type/sans-serif-shortlist.html) ·
[artifact](https://claude.ai/code/artifact/80e5acd5-0afb-45ce-a40a-d7b7fc2d6071). Opens by teaching
the term (a serif is a foot, *sans* is without) and the three families, because that was the actual
question.

**Mid-task the brief changed: no serifs at all** — the client dislikes the pointy parts — which
killed the Marcellus half of the first recommendation and took the serif out of the deliverable's
own headings. Rebuilt as a **sans-only, single-family system: Libre Franklin at 700/600/400**, with
the hierarchy coming from weight, size and tracking instead of from a second kind of letter. Added
three soft-terminal candidates for the no-pointy brief (Manrope, Figtree, Nunito Sans) and set the
client's own name as a wordmark on all eleven cards, since that is the line actually being judged.
Ruled out Outfit (fintech register), Poppins (it is 10x's own face — a client should not wear its
agency's typeface), Inter (the incumbent; flawless and completely undistinctive) and Nunito Sans
(too soft when the subject is somebody's mortgage).

Flagged rather than assumed: if O'Neill Group *is* the SIQ brand, no-serifs means **retiring
Marcellus**, which is a live identity change and a reissue of every asset built on it.

**Second sweep on request: eight more, nineteen total.** Went looking specifically for faces drawn
to carry headline *and* body in one voice, since that is what a serif-free system demands. It turned
up a genuine rival rather than filler: **Schibsted Grotesk**, commissioned by a Nordic news group for
exactly that dual duty and almost unused in Australian property. Libre Franklin keeps the
recommendation on two counts only — a century of civic and financial usage behind the shapes, and
nine weights against six — and the swap is offered rather than buried. Also added Public Sans (a
federal-design-system fork of Libre Franklin, same bones and flatter), Hanken Grotesk, Lexend (drawn
to lower reading effort, a real argument for an older audience), Red Hat Text, Albert Sans, IBM Plex
Sans and Gabarito.

Two build notes worth keeping. Google's CSS endpoint **rate-limits burst loops and returns an HTML
bot page rather than an error code**, which silently poisoned eight font files with identical 6316-byte
payloads; fixed with a retry-and-verify fetch plus an on-disk woff2 cache in the build script. And
the browser pane going hidden reports `clientWidth: 0`, which faked a 1016px overflow — but once it
was visible again the check found a **real** one: `.codeblock` inside a grid item was sizing the `1fr`
track to its own content instead of scrolling, since grid items default to `min-width: auto`. Both the
phantom and the real bug came out of the same measurement, per [[claude-code-setup]]-adjacent lesson:
verify the pane is visible before trusting or dismissing a layout number.

**Third pass, and the correction that mattered: "the ones you gave me were body fonts not header
fonts."** Correct. All twenty-nine so far had been selected on long-copy legibility, which is the
criterion for a *text* face, and the single-family recommendation quietly assumed the headline did
not need a voice. A text face set at 60px is a headline that is merely big. Added a **ten-face header
sweep** judged on presence instead — Jost, Unbounded, Wix Madefor Display, Bricolage Grotesque,
Familjen Grotesk, Chivo, Big Shoulders, Anton, Syne, and Bebas Neue included expressly to be ruled
out as the Australian real-estate cliché. Each header card shows the name at display size **and the
same face at body size underneath**, so the limitation is visible rather than asserted.

Recommendation is now a pairing: **Jost SemiBold headlines + Libre Franklin Regular body**, with Wix
Madefor Display/Text as the zero-clash alternative. That required owning a reversal in writing:
geometric faces were ruled out earlier (Outfit, Poppins) and Jost is geometric. The objection was to
geometry *as a body face*; at 60px used sparingly the same evenness is the premium property register.
Different job, opposite verdict — now stated on the page rather than left to look like inconsistency.

The durable lesson went to [[typography]] as a role table: **ask which job the face is for before
researching**, because the two shortlists share almost no members.

New concept page [[typography]] holds the durable half — the two-family decision table, the
never-Poppins and Inter-is-a-fallback rules, and a licensing note that **Fontshare's free-commercial
fonts are reported to need written consent before self-hosting webfonts**, which is a live risk on
any client site build and is flagged unverified against the licence text itself.

## [2026-08-11] ingest | SSD → Google Drive offload — multi-day project page
New project page [[ssd-to-drive-offload]] documenting the ongoing multi-day job to clear footage off
the 10x SSDs (SSD2/3/5, WD_BLACK) into `Clients/` on Google Drive via `rclone` (remote already
configured). Zip-then-upload convention (staging on SSD2), folder→client mapping, and repeated
gotchas (drives disconnecting mid-job, tmp scratchpad getting recycled across sessions, ~13MB/s
bandwidth ceiling) captured so a future session can resume without re-deriving them. Still running;
most of the backlog (Kodiak, Coast Life, Salisbury, BMW, etc.) not yet started. A separate one-off
raw upload (Whitheriff | Salt PM Shoot, 189GB) is going to `Internal | 10x/Giovanni ` rather than
the Clients archive.

## [2026-08-12] ingest | SSD offload — Whitheriff, Hibiscus Parade, Byron shoot delivered to Giovanni
[[ssd-to-drive-offload]] updated: three raw (unzipped) uploads completed to `Internal | 10x/Giovanni /` —
Whitheriff Salt PM Shoot (226GB, drone photos excluded), 37 Hibiscus Parade Banora Point (Video 93GB +
Drone 6.4GB, Photo excluded), Byron shoot (Video 57GB incl. DJI drone clips, Pictures excluded). New
drive **SSD6** surfaced with its own untouched backlog including a `TO BE UPLOADED | DON'T DELETE`
folder — flagged as next-session priority. Clients/ archive backlog (Kodiak, Coast Life, Salisbury,
BMW, etc.) still not resumed.

## [2026-08-12] ingest | SSD offload — Workshop Sel Studios videos, uploading now
[[ssd-to-drive-offload]] updated: `Workshop | Sel Studios | 12th of Aug 2026` (SSD2) Videos folder
(123GB, 169 files, Photos excluded) uploading raw to `Internal | 10x/Giovanni /`. Same Giovanni
stream as Whitheriff/Hibiscus/Byron — Clients/ archive backlog untouched.

## [2026-08-12] ingest | SSD offload — Workshop Sel Studios done, Bespoke August retainer uploading
Workshop | Sel Studios videos finished uploading (123GB, 169/169 files, matched source exactly).
Now uploading `Project August Content Retainer Bespoke` (SSD6) Video folder (46GB, 92 files, Photo
folder excluded). [[ssd-to-drive-offload]] updated. Clients/ archive backlog still untouched.

## [2026-08-17] ingest | White Fox Real Estate — new web client, brief captured
[[white-fox-real-estate]] created. Old-money/minimal/architectural luxury real estate site.
Studio intro anim (letters corner → top-middle), Coastal Team page. Goal: "luxury for everyone,
property is personal" — families over mansions, premium experience at every price point. Ref
sites for pattern research (not copying): era-residence.com, horizonte-village.com, eleos.la,
awwwards footer-studiofmrg, horizonestatebali.com, minaleandmann.com, makearchitects.com.

## [2026-08-17] migrate | Correction — White Fox was reference, not client; real client is O'Neill Group
Mis-filed above: WhiteFox (goldcoast.whitefoxrealestate.com.au) is a real existing Gold Coast
agency, not our client — kept as UX/structural reference only, no colour/copy. Actual new client
is **[[oneill-group]]**: the principal running [[belle-property]] is leaving with her family to
launch her own agency. 10x is doing full branding (logo, colours) + website from scratch. Design
brief uses 10x colours ([[brand-system]]), WhiteFox site structure as UX base, plus the wider
research pool. All prior pattern/audit research moved to [[real-estate-design-refs]] (now a
source page, not a client page) since it's reusable beyond one client.

## [2026-08-26] ingest | O'Neill Property Brand Book, Edition One — rebuilt and filed
Hunter supplied the existing 18-spread brand book HTML plus four frames from the 37 Southaven
shoot and asked for a creative-director pass. Rebuilt as **23 spreads** at
`projects/oneill-brand-book/oneill-property-brand-book.html`: real photography (the source had
none), a 12-column editorial grid replacing per-spread inline flex bases, reusable components for
rules/callouts/tables/checklists, and three sections the source only had scattered in footnotes —
Website and digital, Open decisions, Quick reference. Source document treated as authority: no
brand fact, measurement or rule invented, and the six unresolved items are labelled rather than
silently resolved.

Verified rather than assumed: the six contrast ratios the source prints all check out
(6.12/8.22/8.22/6.12/2.15/1.34), and every sheet was measured for overflow at 390/1060/1180/1280/
1366/1440/1512/1600/1920 px — two dense spreads (type scale, digital) needed trims.

Knowledge captured in [[oneill-brand-book-edition-one]]. **[[oneill-group]] was stale**: it
recorded the working direction as 10x's own #61a8d8/Poppins palette, and the real brand is Sage
Grey/Basalt/Stone/Deep Sage with Sinhala MN + Inter. The trading name is O'Neill *Property*;
`oneillgroup.com.au` is retired and still on the printed card and photo board. Flagged inline on
the client page with the dated trail kept.

## [2026-08-27] ingest | O'Neill Property Brand Guidelines, Edition Two — designed, verified, filed

Hunter supplied locked copy (26 spreads condensed to 16 sections, 13 pages) and asked for visual
design only, explicitly no reference to Edition One's look. Built as 13 fixed landscape artboards
on a Claude Design canvas, plus a print PDF at 423x299 mm — the sheet ratio is 1.4152 so it drops
onto A3/A4 landscape without letterboxing.

Copy fidelity checked word-by-word against the source draft after build. The only text removed
anywhere was scaffolding 10x had added itself: a "SECTION 0X" eyebrow on 10 pages, which is
kicker-as-grammar — the same tell the [[oneill-group]] site critique caught in August. One
near-miss worth recording: a script deleting those eyebrows also stripped the cover's
"Brand Guidelines / Edition Two" line, which is real locked content. Caught by diffing visible
text against the pre-edit files, restored.

Four rounds of design review (audit, polish, typeset, layout). What they actually found:

- **The masthead was a mutilated logo on 12 of 13 pages.** The secondary lockup does not exist as
  artwork, so the build had CSS-cropped the primary — slicing the wordmark's letterforms in half,
  on a book whose own rule is "never crop the mark". Now the intact icon at 34 px, and page 4's
  secondary slot holds a placeholder. **Client action: supply the wordmark-only SVG.**
- **The four-value palette has no tint ramp**, so `opacity` had been used as one and broke contrast
  in ~40 places (worst 2.76:1 on real copy, on a page that prints "body copy needs 4.5:1").
  Computed the minimum alpha per ground — 0.76 Stone / 0.86 Sage / 0.66 Basalt — and set 0.78/0.88/0.70.
- **The book published a 7-step type scale on page 6 and set itself in 26 sizes**, seven of them
  inside a 3 px band. Now 8 sizes, every one a published step. `font-weight:700` appeared 23 times
  against a spec that says "nothing heavier" than 600 — all gone.
- **Page 6 mislabelled its own specimens** (labelled 64/44/28, rendered 60/42/27). Now exact.
- **Inter was never rendering.** Not installed on this Mac, so the first PDF set the whole book in
  Helvetica Neue and every artifact viewer without Inter saw Arial. Served as a webfont now; the
  PDF embeds real Sinhala MN + Inter 300/400/500/600.
- Four `border-left:2px` accent stripes rewritten with different structure.

Display-face substitute (Edition One's open item 2, still open in the Edition Two copy) is now
**nominated: Antic Didone** — chosen on measured metrics, not vibes. Sinhala MN measures x/cap
0.787 at 64 px, the widest and largest-x-height of every candidate, so its Latin is a Scotch Roman
rather than a Didone. Prata matched width best (+1.6%) but was the reflex pick and its caps
dominate. Also shipped a metric-pinned Georgia fallback that renders 611 px against Sinhala MN's
611 px, so line breaks never move off Apple. **Awaiting Hunter's sign-off.**

Verified rather than assumed: all 13 pages measured in-browser — zero contrast failures, zero text
under 11 px, zero overflow, zero clipped boxes, zero block collisions at 0 px tolerance, zero
broken images. The six contrast ratios page 5 prints were independently re-checked and hold.

Knowledge captured in [[oneill-brand-book-edition-two]]. Deliverable and artboard source filed to
`projects/oneill-brand-book-edition-two/` — it had been sitting in session-temp only, which is how
four passes of work goes missing.

## [2026-08-27] migrate | Correction — the O'Neill secondary lockup does exist; book rebuilt on master SVGs

Filed the Edition Two write-up saying no wordmark-only artwork existed and that the client had to
supply it. **Wrong.** It was in Drive the whole time at
`Clients/O'Neill Property/Branding/Logos/Secondary Logo/SVG/`, four colourways, next to complete
primary and icon sets. The wrong conclusion came from treating the handful of URLs pasted at
briefing as the whole asset set instead of checking the client folder. Found only because Hunter
asked for the PDF to go to Drive, which put me in the folder.

Consequences, all now fixed:

- Page 4's secondary slot held an "Artwork to be supplied" placeholder. Real lockup in.
- The whole book ran on downscaled PNGs whose bounding boxes differ from the masters (primary
  2.31 vs **2.60**, icon 1.19 vs **1.47**), so every logo band was sized against the wrong
  proportion. All 13 pages now use the master SVGs — which is what page 4 itself instructs:
  "Supplied as SVG. Always use the supplied artwork, unmodified."
- The fourth colourway swatch was a plain sage dot standing in for "Sage Grey on Basalt". It shows
  the real primary in Sage Grey now, so all four colourways display the actual mark.

Also removed the decorative cropped wordmark bleeding off the cover. Hunter called it messed up and
he was right — it read as a blob with a detached apostrophe. The brand's own rules 7 and 8
(protect whitespace; premium comes from restraint, not decoration) argue against it existing at
all, so it is gone rather than reframed a second time.

Re-verified after the swap with a deeper check than before — every sibling pair in every container,
plus children spilling fixed-height parents, not just page-level blocks. That deeper check is what
caught two element-level overlaps on page 4 earlier the same day, which the page-level check could
not see. 0 overlaps, 0 spills, 0 broken images across all 13 pages.

Deliverable PDF (13 pages, 423x299 mm, real Sinhala MN + Inter subsets embedded) uploaded to
`Clients/O'Neill Property/Branding/` on the client Drive. Only open items are now the four
decisions on page 13 — none of them 10x's to make.

## [2026-09-02] ingest | Salt PM brand-voice scrub — new client, site+IG scrub for chatbot spec
Site (saltpm.com.au) + IG (@saltpropertymgt) scrubbed: bio, hero copy, 2 sample captions. Two-register voice found — data-led landlord/investor tone vs coastal holiday-guest tone, brand words (considered/tailored/hybrid/stress-free), no hashtags, soft CTAs. Filed [[salt-pm-brand-scrub]], new client page [[salt-pm]], indexed. Chatbot build itself not started.

## [2026-09-02] update | Salt PM handoff doc written for Lach
Condensed the brand scrub into a practical caption-writing brief — two-register rule (landlord/investor vs holiday/guest), brand words, dos/don-ts. `projects/salt-pm-brand-voice-handoff.md`, linked from [[salt-pm]]. Full verbatim scraping of all 259 posts ruled out — no bulk API access without their own IG login, and storing 259 captions verbatim is not something the wiki should hold anyway.

## [2026-09-02] update | Salt PM scrub deepened — 9 posts pulled, four-format model replaces two-register model
Pulled 9 distinct posts via direct URLs (grid clicks were unreliable). Structure sharpened from 2 registers to 4 formats: authority/landlord, team/trust, rigid For-Lease/Leased listing template, and holiday/lifestyle reels (loosest, most voice-driven). Updated [[salt-pm-brand-scrub]] and `projects/salt-pm-brand-voice-handoff.md`. Still 9/259 sampled — bulk export not available (no working API/scraping login) and not appropriate to do wholesale regardless.

## [2026-09-10] update | ZED staging style superseded — white/cream → warm taupe/olive
Zed sent a new listing-photo reference set and confirmed it's the standing style, replacing the white/cream/gold/no-timber spec. New: warm taupe/olive/stone neutrals, bouclé, fluted/reeded timber, oak herringbone floors, black now allowed, emerald velvet living accent. Updated [[zed-style]] (old piece-list kept below as superseded record) and `feedback-zed-outdoor-staging.md` in auto-memory (patio palette flagged TBC pending confirmation with Zed).

## [2026-09-10] update | Bed orientation lock added to staging rules
Hunter caught a bedroom prompt that never named which wall the headboard was against (side-wall bed, not back-wall) — models drift to default placement without an explicit lock. Added standing rule to [[staging-rules]] + `feedback-bed-orientation-lock.md` in auto-memory. Also confirmed and applied the ZED style flip from earlier today across two real master/secondary bedroom raws for [[zed-full-house]].

## [2026-09-11] update | Iron Standard revision round — hero video rotation replaced with a fixed still
Hunter's feedback list actioned end to end. The big one: the 4-clip hero rotation read as the page fading to black and back, so it's now a single fixed photo. That change cascades — a fixed backdrop paints over everything below it, so the accordion and footer needed opaque bands (`.page-rest`, `.site-footer`). Also: headline split to two fixed lines (hero column widened 700→1000px to fit), hero copy rewritten toward mystery rather than repeating the accordion, CTA anchor moved `#waitlist` → `#form`, three accordion photos swapped to client-supplied media-library images, footer logo +50% with a location pin. Verified two-line/no-overflow at 8 breakpoints in both the site build and the WordPress widget (widget checked inside a deliberately hostile fake theme). Updated [[iron-standard]] + project README.

## [2026-09-11] update | Iron Standard mobile pass — 3-line headline, fixed-photo scroll glitch traced to the URL bar
Hunter reported the hero photo "popping/zooming" the instant you start scrolling on mobile. Cause was not the animation: `height:100%` on a `position:fixed` image resolves against the viewport, the phone URL bar collapses on first scroll, the viewport height changes, and `object-fit:cover` re-crops. Fixed with `100lvh` (largest viewport height, constant) plus `100svh` on the hero itself so its content still fits with the bar showing. Also: headline now breaks to 3 lines under 640px via paired `.br-d`/`.br-m` elements on a single un-duplicated sentence (longest line drops 20 chars to 16, which is what funds the 25% size bump), and the hero paragraph is 4px smaller on mobile. Found while testing that the paragraph's declared `1.1rem` had never applied at all, losing to `.section p:not(.kicker)` on specificity. Verified at 13 widths in both the site build and the widget.

## [2026-09-14] update | Iron Standard — client-supplied photos replace two "generic gym" panels
Anthony flagged the "Inside the facility" and "Why it's different" images as looking like the generic gyms already in Oslo, and supplied replacements: a selective-colour red equipment floor and a posing room. Both wired in, local copies in `assets/img/`, but they are NOT in the WordPress media library yet so those two panels are broken until someone uploads them under the exact filenames the page expects. Initially exempted both from the site's blanket `grayscale(1)` filter, reasoning that the facility shot is a selective-colour original whose whole character is the red equipment. Hunter overruled it the same day: all four panels are black and white, one consistent treatment. The colour originals are kept in `assets/img/` if that is ever revisited. His other two questions (DNS cutover, where waitlist signups land) are unanswered and sitting with Hunter, and the honest answer to the second is currently "nowhere" since Brevo still is not set up. See [[iron-standard]].

## [2026-09-15] update | ZED style changes again — "sand & walnut" replaces taupe/olive
Third style shift in three weeks. Zed sent three 3-panel reference boards (interiors / outdoor / bedroom-study-entry): warm sand-cream-greige base, dark walnut timber contrast, olive-green as the only accent, aged stone + antique brass, cream linen sectionals, boucle on timber legs, sheer linen curtains, olive branches in stone urns, plaster-tone abstract art. Emerald velvet, black legs and fluted light-oak are out. Rewrote [[zed-style]] with the live spec on top and a dated trail of both superseded eras beneath, so the `zed-full-house` frames already staged to the 2026-09-10 spec stay explainable. Two open contradictions flagged rather than silently resolved: the new refs use walnut dining tables (against the 2026-09-11 stone-only rule, now marked contested in auto-memory) and put large abstract art above beds (against the standing no-wall-art default). Hunter is running a deeper research pass on the style separately. Also updated the staging-engine skill preset to point at the wiki page.

## [2026-09-15] ingest | ZED style formalised as "Option 01" — canonical staging library
Zed ran a Perplexity deep-research pass and locked a named style option with hex palette, exclusions, per-room reference images and prompt blocks. Ingested `raw/zed/option-01-full-staging-library.md` + `raw/zed/option-01-full-staging-asset-library.html`. Rewrote [[zed-style]] with Option 01 on top (dated trail of the taupe/olive and white/cream eras kept beneath). This resolves two contradictions flagged earlier this session: dining tables ARE timber (walnut pedestal, not stone — `feedback-zed-no-timber-dining-table` marked superseded) and bedrooms DO get large wall art above the headboard (a ZED-specific override of the general no-wall-art default). Flagged an open decision on [[zed-full-house]]: a large batch of taupe/olive-spec prompting happened this session before Option 01 landed, and whether it needs re-running hasn't been decided. Updated the staging-engine skill's ZED preset to point at the raw library.

## [2026-09-16] update | Iron Standard expanded from single-page waitlist to full 7-page site
Anthony's 16 Sep brief replaced the pre-launch scope: 7 pages (Home, About Us, The Facility, Coaching, Join the Waitlist, FAQ, Contact Us), Google Sheets/Apps Script replacing Brevo, 10x hosting replacing Anthony's own Netlify. Built via `superpowers:subagent-driven-development` directly on `main` (Hunter chose skip-the-worktree since this is a solo repo): 10 tasks, each with a fresh implementer subagent and a task-scoped reviewer, plus a final whole-branch review. Final review caught one real cross-task bug — the Apps Script's `MailApp` notification silently fails under the exact deployment config its own README instructs (`Session.getActiveUser()` returns empty for anonymous callers) — which Hunter reviewed and chose to ship as-is (plan-mandated code, a known gap for later). Three other findings were fixed same-session: a mobile-nav keyboard-focus-trap + stale aria-label, missing Open Graph tags on all 6 inner pages, and a fragile `sessionStorage` read that could have silently broken nav/forms if it ever threw — plus a narrow `prefers-reduced-motion` regression the nav fix introduced, caught by the fix wave's own re-review and closed with Hunter's go-ahead. Also found and spun off separately: `preview-local.html` is a stale, out-of-scope leftover file with the old dead links. See [[iron-standard]] for full task-by-task detail and remaining open items (Apps Script deployment, Anthony's pending copy for 3 pages, hosting target, image-hosting risk).

## [2026-09-17] ingest | Jessica Wallace (Harcourts) Coastal Luxury staging — 9 rooms, five new standing rules
New client, first staging job: nine raw interiors of a dated single-level home, re-staged to Jessica's own "Coastal Luxury" concept sheet after another supplier's attempt came back poor. Ran on GPT Image 2.5 Sunburst, every pass from the raw. Client override: no curtains on any shot (logged as an exception on the curtains-by-default rule). Five rules harvested into [[staging-rules]] + auto-memory — framing lock (Sunburst silently re-crops), geometry lock (rug edges tied to grout lines; rugs were rendering twisted), mirror reflections (a mirrored robe reflected an empty room beside a made bed), exact-inventory phrasing (it invented a console and a second rug without it), and prompts-in-prose (the bold-heading format was rejected twice). Also confirmed a general failure mode: assigning furniture to a wall a fixture already occupies makes the model delete the fixture. Underlying limitation noted on [[jessica-wallace]] — no depth map, so perspective alignment can be nudged by naming real lines in the frame but not solved; Hunter finished the set with manual transforms and a raw-over-staged composite.

## [2026-09-22] harvest | ironstandard-site → [[iron-standard]], [[premium-web-build]], index, auto-memory ×2
Built the six-page Iron Standard website from the client's approved Website Strategy & Creative Direction (27pp) plus the IRONSTNDRD Guidelines 2026, in `projects/ironstandard-site/`. The strategy **kills the waitlist entirely** and makes an enquiry the primary action, so this supersedes the 16 Sep 7-page build rather than editing it; `projects/ironstandard-lp/` is left untouched pending a call on retiring it. Six core pages plus four legal stubs so the footer has no dead links, one shared stylesheet, no build step.

Two strategy requirements got real mechanisms rather than lip service: The Facility separates **confirmed from planned** specification with an outlined chip system (the facility is not built, and presenting proposals as finished creates liability), and Contact **routes seven enquiry types to different recipients** so trainer and partnership leads stay out of the member inbox.

**Closed a bug this vault knowingly shipped on 16 Sep:** the old Apps Script notified via `Session.getActiveUser().getEmail()`, which returns empty for anonymous submitters under the exact deployment its own README instructs, so the visitor saw success and nobody was ever emailed. The new handler never calls it, uses an explicit OWNER constant falling back to `getEffectiveUser()`, and ships a `testHandler` that makes proving the routing a required deployment step. Until the Web App URL is pasted in, the form is deliberately inert and says so.

New concept page [[premium-web-build]] carries the durable craft: the no-two-consecutive-sections rule, testing a brand accent against both grounds before choosing a light or dark default (Iron Standard's orange is 3.48:1 on white and 6.03:1 on black, which is *why* the site is dark), the `backdrop-filter`-traps-fixed-children gotcha, the correct full-bleed maths for a grid item, and the measurement checklist. Two cross-project lessons went to auto-memory instead: the Apps Script backend pattern, and the fact that the in-app preview pane returns corrupted composites when a fixed-header page is scrolled — roughly ten tool calls were burned chasing that as a CSS fault before checking the DOM, and real Chrome rendered it correctly all along.

Imagery is all low-resolution moodboard extracted from the brand guidelines PDF; the folder the brief pointed at did not exist. Founder copy, legal copy and photography are outstanding and shipped as visible placeholder notes rather than invented facts. Also flagged: the strategy forbids naming competitors, which collides with Anthony's own SATS Fagerborg background from the About copy, so his history needs rewording.

## [2026-09-22] lint | ironstandard-site → impeccable audit + polish, 11/20 to ~17/20
Client fed back that the site "looks too much like a template". Ran a craft pass first (film grain, hung editorial numerals, visible grid hairlines, scroll hairline, state feedback on every interactive element), then `/impeccable audit`, which scored it **11/20** and found real defects the eye had missed.

Two root causes, both fixed: there was **no muted-text token**, so muted colour was improvised 17 times as raw `rgba()` and produced **39 measured contrast failures** (worst: the footer note at 2.46:1 against a 4.5:1 requirement); and reveals were **hidden by default**, so when IntersectionObserver never fired **69% of page text vanished, including the `h1`**. Reveals now enhance an already-visible default with a failsafe and a print rule. Also removed three **side-stripe borders**, a pattern banned by both the skill and 10x's own DESIGN.md, and raised every tap target past the WCAG 2.2 24px floor. Zero contrast failures and zero regressions after, across 20 page/breakpoint combinations.

**Open conflict, resolved by Hunter and recorded rather than silently fixed:** the numbered section marks and per-section eyebrows are banned by both rulebooks and were stripped from 10x's own homepage in July 2026 for reading as AI scaffolding, but the approved Iron Standard strategy explicitly requires them. Hunter's call is to keep them, since the strategy is signed off and the pattern comes from the client's own print guidelines. Flagged on [[iron-standard]] so a future audit does not undo it. The remaining lever on the template complaint is the imagery: everything on the site is a 588px moodboard crop, and that is a shoot, not a CSS problem.

## [2026-09-29] query | Iron Standard: strategy compliance pass

Hunter re-sent the strategy PDF (byte-identical to the approved one). Audited the site against every page requirement: fixed the Home primary action, removed invented founder credentials, added online programming, nutrition and events to Coaching with a reusable coach-profile template, gave the FAQ a category index and per-answer anchors, and wired Coaching journeys to preselect the enquiry route. Detail on [[iron-standard]].

## [2026-09-29] query | Iron Standard: launch packaging

Coming-soon page is live on WordPress/Elementor; Hunter needs the real site live. Added favicon (client's existing), canonical tags, 404, robots, sitemap, Netlify and Apache configs; upload zip on Desktop. Go-live blocked only on host access. Detail on [[iron-standard]].

## [2026-09-29] query | Iron Standard: harden pass

Found the enquiry form never actually submitted (preventDefault with no re-submit, success faked on a timer). Fixed with explicit submit, postMessage confirmation, busy state, offline and timeout handling; hardened the Apps Script (validation, length caps, formula-injection guard, write lock). Long-word protection for Norwegian compounds and a 320px hero fix. Lessons on [[premium-web-build]].

## [2026-09-29] ingest | One Percent Standard: Shopify store connected

Set up Claude access to Hunter's new white-label store: Shopify Dev MCP at user scope, Dev Dashboard app with scopes (second version, the first had none), credentials in a new ~/.zshrc, and a token-swapping GraphQL helper. Read-only test passed. Detail on [[one-percent-standard-store]].

## [2026-09-29] ingest | One Percent Standard live-prep + Bebita Lifestyle connected

One Percent Standard: supplier specs and corrected unit cost (US$6.63 not $5.60), shipping rates, policies, About/FAQ, menus and home page published via the API; store still password-locked pending photos, payments and a plan. Bebita Lifestyle (sister's activewear/swimwear) created as a second store with its own Claude app; the helper now switches stores with `STORE=bebita`. Detail on [[one-percent-standard-store]] and [[bebita-lifestyle-store]].

## [2026-09-30] ingest | Pain-point research: Bebita activewear + One Percent straps

Two research passes to find positioning. Bebita: see-through/sweat on pastels and sizing fear top the complaints; recommended "build your set" + local dispatch for the sell-off, filmed squat/sweat tests for a relaunch. One Percent: cuffed D-ring straps fail at the ring and stitching; recommended "the cuffed strap that doesn't quit", conditional on testing our own construction first. Bebita store renamed Bebita Collective; its home page comp (row of mirrors) approved. Detail on [[research-activewear-pain-points]] and [[research-lifting-strap-pain-points]].

## [2026-10-02] query | GetHookd connected + first product-research pass

Connected the GetHookd ad-intelligence MCP (user scope, Starter plan, 60 credits) and started its profile survey. Ran a US-winners sweep (4–5 stars, 100–400 active ads), then web research on six candidates (MeasurePro, ToolBox Widget, Camel City socks, EZARC step drills, Muravai shower head, Tumbler sharpener). All scored 3–4/10: each is already in AU via Bunnings/Kmart or an AU clone. About 1.3 credits spent. Detail on [[product-research-gethookd]].

## [2026-10-02] query | GetHookd second pass: 100-point scorecard

Swept 43 tradie keywords (~2.5 credits) and scored 11 more products on a weighted 100-point card (AU gap, margin with a GP ≥ A$30 floor, US proof, demo, shipping, compliance, AOV). Best results: wire fault finder 70, Bolthero offset extension 67, recip pruning blades 62. Nothing reached TEST; US winners are usually already cloned on eBay/Amazon AU. Detail on [[product-research-gethookd]].

## [2026-10-03] query | GetHookd third pass: AU lifestyle categories

Swept 36 lifestyle keywords (4WD, caravan, camping, garden, pool) and scored 9 more products. All skipped (42–63): AU incumbents or Bunnings/Kmart already cover each. 26 products scored in total, none TEST; the US-winner-copy method itself is the problem. Detail on [[product-research-gethookd]].

## [2026-10-03] query | GetHookd fourth pass: AU-running ads in Hunter's niches

Hunter asked to drop the 4WD/caravan drift. Swept ads running in AU (min 20 active ads) and scored 6 products in his niches. Best: SuperGrip magnetic desk arm 69 and Fivalo hinge jig 66, both sold in AU by overseas shippers with slow delivery. Detail on [[product-research-gethookd]].

## [2026-10-03] query | GetHookd fifth pass: camera, fitness, home on brief

Brief locked (100–400 ads, 4–5 stars, Hunter's niches, problem line required). 7 more products scored 39–59, all skip: Kmart A$6–45 copies or brands already in AU. Detail on [[product-research-gethookd]].

## [2026-10-03] query | GetHookd eighth pass: tradie jigs, wall fixes + SimilarWeb traffic

Brief narrowed: no camera/fitness. Added a traffic step (SimilarWeb). Best new: aluminium hinge mortise jig 66 (needs a metric AU version). Key signal: fixiontools.com (19% AU) and norbbshop.com (15.5% AU) are tradie-gadget stores already winning Aussie traffic off Meta. Detail on [[product-research-gethookd]].

## [2026-10-03] query | FixionTools model teardown

fixiontools.com (19% AU traffic, Trustpilot 1.5) shows a multi-SKU tradie-gadget store selling to Aussies from China with awful fulfilment. Opening for an AU-stocked version; 3–5 candidate launch SKUs listed on [[product-research-gethookd]].

## [2026-10-03] query | GetHookd ninth pass: US-only brands

Filtered to US-only ads, then SimilarWeb AU share <2%. MirrorMate stick-on bathroom mirror frames scored 77 (highest yet): no AU seller, GP ~A$91. Murphy Door is a distributor play for builder clients. Detail on [[product-research-gethookd]].

## [2026-10-03] query | GetHookd tenth pass: more US-only brands

Screened 18 more US-only domains, scored 6. Barnakl ceiling-fan air filters 72 (no AU brand, cheap to ship, refill subscription). Others skipped. Detail on [[product-research-gethookd]].

## [2026-10-03] query | Construction shortlist page

Swept 50 construction keywords, built a 42-product shareable list for Hunter's mate (ratchet-strap seller) with GetHookd ad links. Detail on [[product-research-gethookd]].
## [2026-10-04] query | Construction product sweep 5 — 81 products
## [2026-10-04] query | Google Ads AU check on 30 construction keywords (Chrome)
## [2026-10-05] ingest | Bebita store v3: black-and-white redesign, real stock (339 pcs), former model removed (1,200 Magnific credits); blocked on Shopify plan
## [2026-10-05] query | Day trading + AI-assisted trading research → concepts/day-trading-research
## [2026-10-06] ingest | Bebita AI product shots: 50 images for 25 colourways (3,675 credits), stock now 336 pcs / 26 products
## [2026-10-06] ingest | Bebita AI shot redo: 13 shots, 975 credits (V-back waistbands, scrunch back views, blue shades)

## [2026-10-06] ingest | Woomala St 9:16 reframe: 14 images delivered; pad-canvas + NBP 4k + original pasted back 1:1 (88 Higgsfield cr; 50 Magnific cr wasted on Ideogram expand). Higgsfield CLI → 1.1.26, skills synced
## [2026-10-06] ingest | Woomala 9:16 round 2: #11 tower off-frame re-roll, realism pass on 13 (NBP edit-style; Seedream re-composed so dropped), total 149 Higgsfield cr
## [2026-10-06] ingest | Woomala 9:16 reel: 14 Kling 3.0 Pro clips (175 cr) cut into a 44s silent reel; job total 324 Higgsfield cr
## [2026-10-06] ingest | Woomala clips + reel upscaled to 4K via Higgsfield Topaz (~5 cr/clip, 75 cr); Magnific video upscale rejected (~2.3k cr/clip). Job total 399 Higgsfield cr

## [2026-10-07] query | Iron Standard: unified photo grade

ui-ux-pro-max pass. Its generated system (Inter, green accent, glass, bounce) conflicted with the locked brand, so only the diagnosis was used. Applied one warm-monochrome grade to all photography, aligned the founder caption, replaced guideline-speak pull quote. Detail on [[iron-standard]].

## [2026-10-07] lint | Skills audit and update
Audited every skill and plugin against upstream. Updated Impeccable 4.3.1 to 4.5.0 (project + global), Superpowers 6.2.0 to 6.4.1 (removed the duplicate obra-marketplace install and stale settings entry), UI/UX Pro Max 2.11.0 to 2.13.0, nine Emil Kowalski skills, and the Caveman family (added `ultracave`; upstream now forbids arrows and invented abbreviations, which CLAUDE.md still asks for, so the CLAUDE.md house style wins). Higgsfield skills and CLI already current. Patched `staging-engine` and `staging-redo` with the standing rules they lacked (no confirmed default model, camera-framing lock, exact inventory, two bedsides, TV, light/exposure, mirrors, curtains, explain + score) and synced the missing ones into [[staging-rules]].

## [2026-10-07] query | Iron Standard: polish (impeccable 4.5)

Type converted px to rem (default render identical, now honours text-size settings), repeated colours promoted to tokens and two drifting orange tints unified, mk healthhub photo replaced, theme-color, overflow-x clip, empty template src removed. Audit 4.5 had scored 18/20.

## [2026-10-07] query | Iron Standard: polish, large-text wrapping

Text links and section marks now wrap at 200% text on a 320px screen instead of overflowing (64 page/width/scale combos, zero overflow). Default render unchanged.

## [2026-10-07] query | Iron Standard: desktop spacing pass

Client: "feels only optimised for phone". Section padding moved to desktop-scaled tokens (joins 300-430px down to ~190px, pages 600-900px shorter), proof photo runs flush into the band, Who-trains-here and Founder recomposed, founder portrait fixed at 4:5 and capped on tablets. 96 combos regression-clean. Lesson on [[premium-web-build]].

## [2026-10-07] query | Iron Standard: handoff folder

Built `Desktop/10xVisuals Output/Iron Standard - Handoff/` (website, upload zip, form setup, previews, HANDOFF.md). README brought up to date. Copy of HANDOFF.md kept in the project folder.

## [2026-10-07] query | Jessica Wallace office staging, Nano Banana 2.1

Office restaged in her Coastal Luxury style on `nano_banana_2_1` (2cr/run, 3 runs incl. rejected). New client rules: no standing or corner plants, replace existing staging but keep the desk, laptop faces the chair. First read on 2.1: held framing and fixtures. Logged on [[jessica-wallace]] and [[staging-rules]].
## [2026-10-08] ingest | Bebita went live on the Basic plan: products, stock, theme, BEBITA10, shipping threshold $150; password page still on

## [2026-10-09] query | ZED modern-luxury style guide

Drafted three proposed modern-luxury directions (02 Gallery Stone, 03 Smoked Oak Suite, 04 Riviera Resort) beside locked Option 01, with palettes, room kits and example prompts. Published as an artifact, logged on [[zed-style]]. Not approved; Option 01 still canonical.

## [2026-10-09] query | ZED style boards generated

Four 10-room style boards (Options 01–04) on Magnific GPT 2.5 Sunburst, 720cr, stitched into one master sheet. JOB.md in `projects/zed-style-guide/`. Logged on [[zed-style]].

## [2026-10-09] ingest | Deep research: luxury staging trends + AI board prompting

18 of 25 claims survived verification. Room-by-room furniture and price-lift evidence not found. Filed as [[deep-research-2026-10-luxury-staging-prompting]].

## [2026-10-09] ingest | Deep research round 2: AU furniture houses

Jardan/Cosh Living products mapped to ZED directions; every AU staging price-lift stat refuted, so none go in client copy. Appended to [[deep-research-2026-10-luxury-staging-prompting]].

## [2026-10-09] harvest | USE Software Definitions: CRUD episode + template

Five rounds on the CRUD talking head. v1/v2 copied the wrong reference (an Empire Technologies ad); v3–v5 matched USE's own MCP/API episodes. Built a reusable episode template at `projects/use-definitions/`. New pages: [[use-software]], [[use-definitions-series]].

## [2026-10-09] harvest | USE: CRUD v6 + bus case study v1 from the template

CRUD rebuilt through `projects/use-definitions/` (v6). The new 22 Oct clip (bus on-time tracking story) became `episodes/bus-network` v1. SFX engine upgraded to stereo with reverb. Logged on [[use-definitions-series]].

## [2026-10-09] ingest | USE: Magnific SFX library (120cr)

Hunter approved real SFX: 24 takes (whoosh, pop, click, impact, shatter, riser) in `projects/use-definitions/sfx-lib/`, used by `tools/sfx.py`. Bus v2 and CRUD v6 re-mixed with effects about 8 LU under the voice. Hunter is happy with bus v2 and has another clip coming.

## [2026-10-10] harvest | USE: 19-episode batch complete

14 Definitions and 5 Q&A episodes were built through the template. Every one passed the tracked face check and the boss-review loop before sending. The Q&A series name is still a placeholder. Logged on [[use-definitions-series]].
## [2026-10-10] query | Bebita storefront showed no products: API app lacks publications scope, so products need publishing to Online Store

## [2026-10-10] ingest | Ocular Sounds SFX library
Filed 192 Ocular sounds (Foundation, Pendulum, Aperture, Rainforest) into ~/Music/SFX Library with a catalog.csv. The Committed Coaching sfx-lib was rebuilt on Foundation impacts, booms, whooshes, hits and risers. v4 of the not-your-guy reel adds an 80cr Lyria music bed.
## [2026-10-10] ingest | Bebita live polish: size guide, fabric & care, AI colour first, international off, header fix
## [2026-10-11] ingest | Bebita: 13 crumpled flat-lays removed from the live store
## [2026-10-11] query | Bebita: payments not set up (no Shopify Payments account); launch-to-sales plan + 8 ad scripts written
## [2026-10-11] ingest | Bebita: Hunter is the seller; payouts and onboarding in his name
## [2026-10-11] ingest | Bebita: no access to old IG accounts; footer links removed, plan switched to new accounts

## [2026-10-12] query | ZED style boards v2

40 rooms on Nano Banana Pro with anchor references (3,000cr; job total 3,720cr), 4 boards assembled locally. Logged on [[zed-style]].

## [2026-10-12] query | ZED style boards final

01 dining end chairs masked out (75cr), Option 02 rebuilt with timber contrast (750cr). Job total 4,845cr. Delivery folder built for Zed.

## [2026-10-12] migrate | Blender block-out pipeline installed
Blender 5.2.2 + blender-mcp server + addon installed; headless block-out test passed. New page [[blender-blockout-pipeline]].

## [2026-10-12] query | Editorial look is the default
Hunter set an editorial finish as the default for ALL generations. Added to [[higgsfield-pipelines]] hard rules; Blender route default recorded in [[blender-blockout-pipeline]].

## [2026-10-12] decision | Zed picks Riviera Resort

Zed chose Option 04 Riviera Resort for the furnished-home job. Logged on [[zed-style]].

## [2026-10-13] build | Iron Standard: motion system site-wide

Client revisions: scroll line removed, closing title now "Raise your standard.", closing logo halved and overlay lightened. Then the homepage style rolled out to every page: shared motion.css/motion.js (masked reveals, photo wipes, eased scroll engine, icon cards, marquee, closing band with travelling logo, smooth FAQ accordion) plus a cinematic page hero on every inner page. Static fallback with reduced motion. 32 page/width combos clean.

## [2026-10-13] ingest | House twilight reference locked
Hunter supplied the target twilight frame; new page [[house-twilight]], supersedes ZED #21 as default.

## [2026-10-14] ops | Iron Standard handoff pass
Handoff folder re-synced: fresh full-page previews (6 desktop, 4 phone), HANDOFF.md corrected (stylesheet split, text-over-photo claim, revision history). Stale Oct 7 zip and homepage mirror moved to 10xVisuals Output/_archive.

## [2026-10-14] ops | Iron Standard revision round 4
White sticky header (inverted logo), ring label Strength, instant card hover (removed staggered colour transition), closing label "Your move" + logo starts right, About founder rebuilt as editorial feature (framed portrait, lit pull statement, three principles), all on-page notes and footer imagery note removed. Fixed a dangling selector left from the scroll-line removal. Handoff folder, zip, previews and single-file preview rebuilt.

## [2026-10-14] ops | Iron Standard revision round 5
Header gated behind the homepage stage; ring label The gym; site-wide --inset so section content aligns with hero copy; Facility status board (white, confirmed/planned) and Space rebuild (scroll-filled measuring scale); Coaching services as shared pinned horizontal track (hs engine moved from home.js into motion.js, anchors land on panels), How it works merged into CTA; FAQ tabs + single-open accordion; privacy and terms written in full with cookies and accessibility folded in (old URLs 301); Built by 10x Visuals footer credit. Headless test lesson: render-blocking Google Fonts can delay deferred scripts past a fixed wait, so captures now wait for readyState complete.

## [2026-10-16] lint | Overview refresh, nine unharvested folders, memory-slug links
- Overview was frozen at July. Rewrote "current state" for October (web builds, Bebita/One Percent stores, ZED Riviera, USE series, Blender pipeline) and kept the July snapshot as a flagged trail.
- Nine `projects/` folders had no wiki page. New [[zed-4-alex-keith-st]] and [[motion-and-stills-tools]] (logo sting, HIA title, motion-sfx, white-border). Harcourts IG templates + Datum Line canvas → [[jessica-wallace]]; site fixlist → [[oneill-group]]. Index updated.
- 14 `[[feedback-*]]`/`[[reference-*]]`/`[[template-*]]` links pointed at auto-memory files that Obsidian can't resolve. Changed them to code refs in [[staging-rules]], [[zed-style]], [[coast-life-constructions]].
- Open: ~25 memory feedback files aren't named by slug in the wiki (most are summarised by content in [[staging-rules]], so not a real gap). Hattie/Anthony retainer outcome still unknown. The "Coaching reel 2: Brett" commit (latest) has no page.

## [2026-10-16] migrate | Hattie/Anthony retainer removed; Tyson is the founder
- Hunter asked to remove the Anthony / Hattie Boydle retainer. Deleted the `anthony` client page and `projects/anthony-proposal/`, and stripped references from overview, index, iron-standard, lead-gen-and-sales, proposal-playbook and the 17 Jul weekly review. Earlier log entries are left as history.
- **⚠️ Correction:** Tyson is the founder of 10x Visuals (founder & CEO), not Hunter. Fixed in overview, index, [[hunter]], [[tyson]] and CLAUDE.md.

## [2026-10-16] query | ZED 86 Ormeu St style guide

16 real-photo stagings (4 rooms × 4 options) on Sunburst, 2,880cr; boards built in code. Logged on [[zed-style]].

## [2026-10-16] query | ZED 86 Ormeu St full staging

Zed picked Smoked Oak Suite; 15 more interiors staged (2,700cr, job total 6,480cr). No-additions rule held. Logged on [[zed-style]].

## [2026-10-16] query | Blender: material-ID maps, denser scenes, add-on research
Added the material-ID colour-map method, the scene-density lesson and the ranked add-on list to [[blender-blockout-pipeline]].

## [2026-10-18] ingest | LRGR Than Life Apparel creative brief
Ingested the brief (raw/lrgr/). Wrote [[lrgr-than-life-apparel]] and projects/streetwear-ads/LRGR-CREATIVE-PLAN.md: 12 concepts, top 6, execution plans, batch shoot. Flagged the earlier generic production pack's concepts as superseded.

## [2026-10-18] query | LRGR plan v2 (critique and rework)
A multi-agent critique and rework of the LRGR PDF produced a new 12-concept slate, six shoot-ready executions and a batch schedule. Two executions are unreviewed drafts. Filed on [[lrgr-than-life-apparel]].

## [2026-10-18] query | LRGR v2: one-session constraint
All multi-day content was removed. What Goes First? was replaced by The Lift and In The Bag (same-session version). The client PDF v2 was rebuilt.

## [2026-10-19] ingest | CVA Woomala render enhance — 11 stills delivered (NBP recipe, 3,210cr) → [[cva-woomala-render-enhance]]

## [2026-10-19] lint | Claude efficiency pass

Audited per-request context (~80k tokens baseline). Moved the four global MCP servers into vault scope, disabled ui-ux-pro-max / scroll-world / frontend-design for the vault via a new committed `.claude/settings.json`, parked 13 animation/web skills in `~/.claude/skills-parked/`. Backups in `~/.claude/backups/efficiency-2026-10-19/`. Detail on [[claude-code-setup]].

## [2026-10-19] ingest | Sound Lab, local 10x fork
React Bits Sound Lab was pulled out of the react-bits repo (MIT + Commons Clause) into `projects/sound-lab/`, a standalone Vite app on port 8160. It now adds 48k/24 WAV delivery, project file naming, −1 dBFS normalising, kit zip export with a CSV, and picture-sync cueing with timecode and a stem export. All of it was verified in the browser preview. Whether the synth sounds hold up in a real edit is still untested. → [[sound-lab]]

## [2026-10-19] query | Claude improvement research

Second pass on the same day. Turned off superpowers, code-review, commit-commands, hookify and security-guidance for the vault, and parked caveman-help and caveman-review. Ran a docs sweep of Claude Code best practices plus a vault audit, and filed the result as [[claude-improvement-plan]]. Top findings: `.git` is 6.6 GB with media committed, the "no paid ops without asking" rule isn't enforced in config, the CVA JOB.md header and wiki cost are stale (4,035cr vs 3,210cr), and two staging rules have drifted between auto-memory and [[staging-rules]]. Nothing in the plan has been applied yet.

## [2026-10-20] migrate | Media ignore rules + Magnific money gate

Applied priorities 1 and 2 from [[claude-improvement-plan]]. `.gitignore` now blocks video, audio, Blender and zip files vault-wide; tracked files are untouched and history was not rewritten. Built `.claude/hooks/magnific-gate.py`. Finding: under bypass mode a hook's `ask` is silently auto-approved. So the gate denies paid tools in bypass mode until Hunter's latest message starts with yes/go/approved, and asks in normal modes. Live test: `guides_list` passed, `tags_create` was blocked before it reached Magnific. Detail on [[claude-code-setup]].

## [2026-10-20] migrate | Magnific gate v3: transcript-based approval

Two automated security reviews flagged that a file-based approval could be forged, and that the gate could edit its own settings. Rebuilt the gate so approval comes from Hunter's latest typed message in the session transcript; the approval file and the UserPromptSubmit hook are gone. Edits to the hook, the settings and the transcripts now need the same approval, and NotebookEdit was added to the matcher. A 20-case test against fake transcripts passed. On live use it blocked Claude from reading settings until Hunter replied "yes". Detail on [[claude-code-setup]].

## [2026-10-20] ingest | Sound Lab v2 + FCP plugin research
Added nine features to [[sound-lab]]: layering stacks, LUFS levelling (matches ffmpeg ebur128), takes, presets, a trim effect, FCPXML export (valid against FCP 12.4's v1.11 DTD), editor transport keys, frame-exact cut detection and save-to-folder. All were verified in the preview. Importing the XML into Final Cut itself hasn't been tested yet. Started [[fcp-plugin-research]] with an inventory of installed plugins (FCP 12.4, M5 Pro) and two Perplexity prompts. Flagged [[video-edit-pipeline]], which says "Resolve or Premiere" although FCP is the working NLE.

## [2026-10-20] ingest | SFX sorter live

Built `projects/sfx-sorter/sfx-sorter.mjs` and the launchd job `com.10x.sfx-sorter`. When a sound-pack zip lands in Downloads, it is extracted into `~/Music/SFX Library` (Ocular packs to `Ocular Sounds/`, others to `_Incoming/`) and the original zip goes to `_Archives/`. The first dry run showed that Downloads also holds music tracks and client VO, so loose audio is now ignored and only zips newer than 20 Oct 09:00 count. Tested in scratch and live under launchd. Detail on [[sfx-sorter]].

## [2026-10-20] harvest | Beach Blender build: video results

The 16 Oct video pass never reached the wiki. Harvested it to [[blender-blockout-pipeline]]: 7 Seedance clips (672 HF; 3 pass, 1 near-pass, 3 fail) and the shot-06 face test (Kling 3.0 Pro vs Veo 3.1 Fast). Job total 791.5 HF, status review. Committed the job's small working files (run.py, list.txt, face-test prompt and URLs); its mp4s stay local.

## [2026-10-20] query | Job framework v2 + Blender kit design

Hunter put the Veo re-roll (96 HF quoted) on hold to build the system first: "time was shit". Diagnosed the beach job (about 6 h hand-build, a rebuild, 672 HF before any pilot) and interviewed Hunter: the pains were the build wait and bad outputs, the use is off-the-plan plus R&D, the target is under 2 h, and the scope is every job. Wrote the design spec and [[job-framework-v2]]. Not built; awaiting approval.

## [2026-10-20] migrate | Job framework v2, phase 1: gen-runner + ledger

Hunter approved the [[job-framework-v2]] design. Built `projects/gen-runner/gen_runner.py` (estimate, run, log, tally, sheet). Added a `## Ledger` section to JOB.md so the cost header is derived, not hand-kept; seeded beach (791.5 HF) and CVA (4,035 cr, correcting the wiki's 3,210). Fixed the CVA header placeholders and moved ZED-4's status to generating (Hunter's web-app gens, no metered spend). Widened the money gate to `higgsfield generate create` and `gen_runner.py run`. Tests: the real beach estimate came to 96 HF, and a fake-CLI run passed every path. No credits spent.

## [2026-10-20] migrate | Job framework v2, phase 2: gates + routes in 10x-ai

Rewrote the `10x-ai` skill around the three Hunter gates (A spec + cap + pilot spend, B pilot results + batch quote, C finals). Added shot classes, a Blender route, the pilot-before-batch rule, gen-runner for batches, and pilot outcomes written back. New canonical route page [[shot-class-routes]]: vehicles (C4) and drone wides (C5) are pilot-required. Linked from [[higgsfield-pipelines]]. Skill backup is in `~/.claude/backups/10x-ai-2026-10-20/`.

## [2026-10-20] migrate | Job framework v2, phase 3: Blender kit v1

Built `projects/blender-kit/`. `build.py` runs the modules site, landscape, people, cameras and passes, plus an imports step. The asset library (Poly Haven plants, grass, tree, chair, 7 rigged mannequins, materials, world) was extracted from the beach scene. The beach was rebuilt from `beach.scene.json` in 4.3 s (65 s with renders) against about 6 h of hand-building on 16 Oct: 1,729 against 1,768 objects, 78 of 86 families exact, guide frames matching, 0 clearance hits. Fixed in passing: the surf was hidden by the ocean waves, and stray anthurium templates were coming in with the import. The house is still imported until phase 4. No spend. Detail on [[blender-blockout-pipeline]].

## [2026-10-20] migrate | Job framework v2, phase 4: house generator

Added `kit/house.py`: a parametric multi-level house from a spec (openings per side as wall segments with no booleans, roof, alfresco, balconies, lift, observatory, pool). Lot 48 test built from summary facts because the plans PDF is no longer on the Mac: 153 objects, 1.4 s with renders, level areas matching the plans. Fixed the ID pass so the material name wins over the object name (a garage wall had come out timber-red); beach plants now get correct IDs as a bonus. No spend. Detail in [[job-framework-v2]], [[blender-blockout-pipeline]] and [[belle-property]].

## [2026-10-20] migrate | Job framework v2, phase 5: automatic video QC

Added `projects/gen-runner/qc_video.py` and a `qc` command, and the runner now flags every downloaded video: NO_MOTION (median optical flow < 0.12 px/frame at 320 px) and MORPH/DISSOLVE@t (ORB homography inlier ratio < 0.35). Calibrated on the 7 beach Seedance clips plus 2 face tests, 9/9 correct: 01 and 07 flagged no-motion, 06 flagged a dissolve at 2.0 s, and all passes clean. Updated [[shot-class-routes]], the 10x-ai skill's QC step and [[job-framework-v2]] (all 5 phases built). Gate quirk noted: commands that quote the runner's spend command get blocked too. No spend.

## [2026-10-20] query | USE Definitions v2 redo queued

Hunter: redo the 21 sent USE "software videos" with everything improved since, one at a time. Queued in `projects/use-definitions/QUEUE.md` (v2 redo table, 01 CRUD first) and noted on [[use-definitions-series]]. The main upgrade is real SFX (Ocular, free packs, Sound Lab). Not started.

## [2026-10-20] migrate | USE Definitions v2 redo: CRUD v7 built
The first episode of the redo pass. New SFX kit sfx-lib-v2 (Ocular plus Sound Lab UI renders); engine SHUTTER, placeable title shards and an alive end card; gen-runner QC edit mode (`--edit --allow`). QC came back ok after widening one transition window, with FACE CLEAR, TEXT CLEAR and −17.5 LUFS (matching v6). Waiting on Hunter's Gate B before 02 bus-network. See [[use-definitions-series]]. No spend.

## [2026-10-20] migrate | USE Definitions redo: CRUD v7 locked, bus-network v3 built
Hunter locked CRUD v7. Bus-network v3 has the v7 upgrades plus two fixes: the hook shards are off the face, and the panel caption no longer clips (it holds until the panel pushes it up). Added `tools/qc_episode.py`. QC ok, FACE/TEXT CLEAR, loudness equal to v2. Waiting on Gate B. No spend.

## [2026-10-20] lint | USE: headline-overprint check added
Hunter caught overprinting headlines in bus-network v3 (Simple./Standard.). Fixed, and made a standing check: `tools/lint_rise.py` in `qa.sh`, BOSS.md rule 6, and auto-memory `feedback-motion-headlines-never-stack`. All 21 episodes swept clean. The follow-on freeze was caught by gen-runner QC and fixed. Bus-network v3 rebuilt and resent for Gate B.

## [2026-10-20] migrate | USE redo: bus-network v3 locked, CLI v3 built
Hunter locked bus-network v3. CLI v3 has the upgrades ported; QC FREEZE caught 3 dead stretches in the CRT scene (fixed with a cursor click, a CRT roll band and a push), and the engine `cardStack` label padding is fixed. All checks clear. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: CLI v3 locked, JSON v4 built; build.sh stale-picture bug fixed
Hunter locked CLI v3. JSON v4 has the upgrades ported plus an idle float (QC freeze). Found that `build.sh` silently re-muxed a stale picture when the render crashed, and `qa.sh` hid errors behind pipes. Both are fixed (syntax gate, stale-picture delete, a picture-exists check, pipefail). No spend.

## [2026-10-20] ingest | Solis pool cinemagraph delivered
Salt PM, Solis 673 Casuarina Way frame 16 → 10s 9:16 cinemagraph. Seedance 2.5 i2v with camera lock moved only the water and spout (160 hf). Clouds were added free in post with an anchored sky-zoom composite. Harvested into [[solis-pool-cinemagraph]] and linked from [[salt-pm]] + index.

## [2026-10-20] migrate | USE redo: JSON v4 locked, SDK v4 built
Hunter locked JSON v4. SDK v4 has the upgrades ported; QC FREEZE caught 6 dead stretches, fixed with on-story motion (wrap pulse, request packets, stack float). All checks clear, loudness equal to v3. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: SDK v4 locked, UI/UX v2 built first-pass
Hunter locked SDK v4. Added `tools/still_scan.py`, which pre-scans the old render for dead holds. UI/UX v2 passed every check on its first build (phone float pre-fixed). Redo workflow written into QUEUE.md. No spend.

## [2026-10-20] migrate | USE redo: UI/UX v2 locked, IDE v3 built first-pass
Hunter locked UI/UX v2. IDE v3 has the upgrades ported plus a pre-fixed window float, and passed all checks first build (loudness equal to v2). Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: IDE v3 locked, SaaS v2 built first-pass
Hunter locked IDE v3. SaaS v2 has the upgrades ported plus pre-fixed on-story motion, and passed all checks first build. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: SaaS v2 locked, GPU v2 built
Hunter locked SaaS v2. GPU v2 has the upgrades ported plus pre-fixed on-story motion. QC LOOK flags turned out to be tight allow windows (hard cuts need ±0.3 s), fixed without a rebuild. All clear. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: GPU v2 locked, CPU v3 built
Hunter locked GPU v2. CPU v3 has the upgrades ported plus pre-fixed on-story motion. One 0.5 s still at 16.1 s (between traces finishing and pulses starting) was fixed by starting the pulses earlier. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: CPU v3 locked, Git v3 built
Hunter locked CPU v3. Git v3 has the upgrades ported plus on-story motion over all 16 dead holds in v2. All clear after widening one allow window. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: Git v3 locked, Docker v2 built
Hunter locked Git v3. Docker v2 has the upgrades ported plus on-story motion over all 10 dead holds in v1. A float alone froze on the light background, so copy beams and a shine were added. All clear. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: Docker v2 locked, State management v2 built
Hunter locked Docker v2. State management v2 has the upgrades ported plus on-story motion (floating store, tab-clicking cursor tied to the re-fetch log). Rebuilt once for two short holds. All clear. Waiting on Gate B. No spend.

## [2026-10-20] ingest | Full Ocular Sounds set filed
The full Ocular download landed in a Downloads subfolder, which the sorter does not watch. Eight packs were extracted into ~/Music/SFX Library/Ocular Sounds, sorted by CatID, and catalog.csv was rebuilt: 1,547 sounds (was 190). Utility adds computer keys, drives and UI-adjacent foley, useful for the USE kit. See [[sfx-sorter]].

## [2026-10-20] migrate | USE redo: State management v2 locked, ERD v2 built
Hunter locked State management v2. ERD v2 has the upgrades ported, on-story motion (scanner sweep, records along the connector), and the face circle moved off the houses table. All clear. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: ERD v2 locked, Excel wince v4 built
Hunter locked ERD v2. Excel wince v4: the Q&A opener is now alive engine-wide, the end card is alive, and a headline was moved off the face circle (a QA gap: TEXT CLEAR ignores the face circle). All clear. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: Excel wince v4 locked, Scope myth v3 built
Hunter locked Excel wince v4. Scope myth v3 has the upgrades ported, on-story motion (core cards build with progress bars), and the Over-delivered pill moved off the caption. All clear. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: Scope myth v3 locked, Promises v3 built
Hunter locked Scope myth v3. Promises v3 brings the agreement scene alive (pen reads, signs and hovers; turning seal; worst cases ticked). Rebuilt once for a 0.9 s freeze. All clear. Waiting on Gate B. No spend.

## [2026-10-20] migrate | USE redo: Promises v3 locked, Ask the vision v2 built, Scope myth v4 bugfix
Hunter locked Promises v3. Ask the vision v2 is built (alive vision cloud, thoughts between heads). A mid-line // comment bug hid its circles and had silently broken Scope myth v3's pill, so Scope myth v4 was rebuilt with only that fix. build.sh now has a comment gate. All clear. Waiting on Hunter for both. No spend.

## [2026-10-20] ingest | Extra Salt Kollosche gulls comp
Hunter asked for birds flying past a 1.9s Pottsville drone wide with the grade unchanged. Built as a Blender comp: a constrained drone-camera fit to 2D tracks (0.21 px), four procedural silver gulls, an RGBA pass and an ffmpeg overlay. The plate is untouched outside the birds. Delivered mp4 + ProRes for review. New page [[extra-salt-kollosche-birds]]. No spend.

## [2026-10-20] migrate | USE redo: Ask the vision v2 + Scope myth v4 locked, Handover v2 built
Hunter locked Ask the vision v2 and Scope myth v4. Handover v2 is built: upgrades ported and loop-scene dead holds pre-fixed (traveller + blue radar sweep, alive hub, kit and repo pill). Cyan on the light page still froze 0.7 s; the deeper brand blue cleared it. All QC clear. Waiting on Hunter's Gate B for the last episode of the redo pass. No spend.

## [2026-10-20] migrate | USE redo: Handover v2 locked, redo pass complete
Hunter locked Handover v2. Every sent episode in the v2 redo pass is now locked (skipped: API, MCP, SQL, Webhooks). No spend.

## [2026-10-21] query | SFX sourcing, licensing, technique and FCP workflow
Answered Prompt 2 of the FCP plugin research (SFX sources) by web research. Filed [[sfx-sourcing-and-design]], which covers subscriptions and packs with prices and licences, what is cleared for client work and paid social, layering/pitch/reverb/ducking/LUFS technique, design tools (Logic, Vital, Krotos, Tonsturm, Sound Particles, AI generators) and the FCP drop-on-the-cut workflow (Sound Effects alias, Shift-Q backtimed connect). Pick: Soundly Pro plus the free Sonniss GDC bundles, about A$275/yr; Epidemic Pro if music is needed too. Also fixed the stale 192-sound count on [[sfx-library]] (now 1,547). No spend.

## [2026-10-21] query | FCP 12.4 plugin research (Prompt 1)
Answered Prompt 1 of [[fcp-plugin-research]] by web research (five parallel passes: FCP-native features, audio + captions, reframe + colour, organisation + AI + interchange, motion graphics). Key shifts: FCP 12.3 now does burned-in word-by-word captions, Match Color, Auto Mask and HEVC proxies natively; Apple bought motionVFX (16 Mar 2026) and Boris FX bought iZotope (2 Jul 2026); mReal Estate and mLogo are already in the owned DesignStudio. Buy-first: Jumper, dxRevive, DipSync, Neat Video 6, ScriptStar, Arctic, Globe Trotter 3, captionTranslator, about US$592 all one-off. Flagged [[video-edit-pipeline]] as contradicting the FCP setup. No spend.

## [2026-10-21] ingest | plate-vfx skill + pipeline v1
Turned the Kollosche gulls job into a reusable pipeline (projects/plate-vfx) and skill (plate-vfx). It has cut detection, a multi-start constrained drone-camera fit (0.15 px on the benchmark), plate matching (sky, warmth, grain), auto-routed flight paths for 16:9/9:16, and draft/standard/hero tiers. The standard and hero tiers use a rigged CC-BY Sketchfab herring gull. Hunter updated the Blender MCP addon and enabled Sketchfab. New page [[plate-vfx]]. No spend.

## [2026-10-21] migrate | plate-vfx: flock
Added simulate_flock: a leader path plus members in drifting slots, with lag, separation, velocity-derived banking, and individual wingbeats and glides. `layout --flock N`. Benchmark: 2 heroes + 24-bird flock, standard tier 33 s, 0 px plate change. No spend.

## [2026-10-21] migrate | Kollosche gulls: synced wing-flap SFX
Procedural flap SFX synced to each gull's downstrokes, using distance for level and brightness and screen position for pan. The WAV and a preview mp4 are delivered. Next: port it as a `sfx` stage in plate-vfx. No spend.

## [2026-10-21] migrate | Kollosche gulls: ambience instead of flap SFX
The synth flaps were rejected ("like a cloth", too loud). Replaced them with a quiet ambience bed from real local recordings (distant gull window + soft wind) at -43 dB mean, under the clip audio. Lesson logged on [[extra-salt-kollosche-birds]]. No spend.

## [2026-10-21] migrate | Kollosche gulls: real-grain flap SFX
Hunter rejected the ambience (the gull source has speech) and wanted better flaps. Built a custom WAV from 11 real wingbeat grains placed on every rendered downstroke, with distance level/high-cut and pan, -18 dBFS peak. No spend.

## [2026-10-21] ingest | Custom lens-flare SFX
Three procedural lens-flare WAVs (soft, shimmer, sweep) in projects/sfx-custom. Clicks were fixed with a crossfaded filter bank, verified by spectrogram. New page [[sfx-custom]]. No spend.

## [2026-10-21] ingest | Lens-flare SFX: 12 variants
Added glint, sunburst, golden-bloom, anamorphic (both directions), riser-into-flare, dreamy, subtle-air and crystal to `projects/sfx-custom/lens_flare.py`. The script is now a VARIANTS table. Spectrogram QC is clean. Variant table is in [[sfx-custom]].

## [2026-10-21] ingest | Shing SFX: 9 variants
Added `projects/sfx-custom/shing.py`, a metallic blade-ring "shinggg" built from modal synthesis plus a noise scrape. Spectrogram QC is clean. Details are in [[sfx-custom]].

## [2026-10-21] query | Plate-VFX roadmap research
Researched what to build next after the birds. Filed as [[plate-vfx-roadmap]], ranked by client value against effort and reuse of the camera solve and plate match.

## [2026-10-21] ingest | plate-vfx: lines, sky, dusk stages
Built roadmap items #2–4 on the Kollosche benchmark. Lines and sky pass the plate-untouched check. Dusk v1 is graded with a before/after pilot. Status is in [[plate-vfx-roadmap]].

## [2026-10-21] lint | plate-vfx dusk shelved
The day-to-dusk relight (v2, Depth Pro mesh + Cycles) was stopped by Hunter. Window detection at drone scale is the blocker. Lessons are filed in [[plate-vfx-roadmap]].

## [2026-10-21] ingest | Sky library
Hunter asked what real sky looks like at each time of day and for the best real sky at each. All 299 Poly Haven skies were rendered camera-view and ranked, and 4 were picked per time. Physics notes and prompt wording sit alongside them. See [[sky-library]].

## [2026-10-22] query | AI lifestyle people framework
Hunter wants hyper-real AI-generated people (no cast talent) in listing lifestyle shots. Drafted [[ai-lifestyle-people]]: a recurring invented house cast, new shot classes P5 (people into a real photo, composited back onto the raw) and C6 (people in renders/CG), a realism QC checklist, the Topaz 4K50 + Hyperion HDR finish proven on the Lambo side intake, costs, and a ~75 HF pilot. Awaiting the cast list and the pilot photos.

## [2026-10-22] query | Blender-directed lifestyle films
Extended [[ai-lifestyle-people]] with the Blender + AI cinematic route: the kit, MPFB2 posed people and car rigs direct the shot; Sunburst with the cast face makes it photoreal; motion is routed Seedance (architecture), Kling 3.0 Pro / Veo (faces) or a tracked CG car; then the Topaz 4K50 + HDR finish. Includes an 8–10 shot lifestyle film template.

## [2026-10-26] ingest | Claude + Blender guides
Two research docs from 23 Oct, copied to `raw/blender/`: the MCP automation + photoreal render guide and its add-ons companion, which corrects the guide. Wrote [[claude-blender-guides-2026-10]]. Updated [[blender-blockout-pipeline]]: flagged that Archipack 2.x is paid (it was listed as free), noted the Geo-Scatter verdict differs, added fSpy for still-photo camera matching, MCP bridge notes, the photoreal checklist and critique loop for final-pixel renders, and the support-surface floor check. Updated [[claude-code-setup]] with the package rename and safe-mode note. Not adopted: migrating the MCP package, turning on safe mode, or buying any add-ons.

## [2026-10-26] lint | Closed three open items
Hunter confirmed all three are done: the [[ai-lifestyle-people]] pilot, the beach build people-shot pick + re-rolls ([[blender-blockout-pipeline]], JOB.md set to delivered), and Lot 48 ([[belle-property]], delivered 21 Jul; the stale "awaiting go" line in the auto-memory index is fixed). The pilot results and the final beach spend aren't recorded.

## [2026-10-26] ingest | Mac mini Blender install checklist
Copied to `raw/blender/` and linked from [[claude-blender-guides-2026-10]]. Audited this Mac against it in [[blender-blockout-pipeline]]: everything is in place (Blender 5.2.2 LTS arm64, Claude Code, uv, telemetry off, Metal GPU on) except safe mode, which Hunter chose to leave off. Found two identical MCP add-on copies both enabled.

## [2026-10-26] lint | Blender duplicate MCP add-on disabled
Hunter approved. Disabled the `addon` module and kept `blender_mcp`; verified on a fresh Blender start that only one copy loads and the quit exception is gone. See [[blender-blockout-pipeline]].

## [2026-10-26] lint | Blender MCP add-on updated
Updated the add-on from protocol 14 to 15 with the installer, restarted Blender, and checked it live: up to date, one module loaded. The installer rewrites the duplicate `addon.py` too, but that module stays disabled. Poly Haven search is currently off. See [[blender-blockout-pipeline]].

## [2026-10-26] lint | Blender asset libraries on
Hunter turned on Poly Haven, Sketchfab and Poly Pizza search in the MCP add-on; confirmed live. The generators stay off.

## [2026-10-26] ingest | Coastal drone-reveal guide build
Built an invented beach house and a street-to-ocean drone reveal entirely from the kit, with guides and ID maps at 3 frames. Fixed three kit bugs: invisible trees, footpath rendering as timber in the ID map, and tree trunks rendering as stone. See [[blender-blockout-pipeline]]. No credits spent.

## [2026-10-26] ingest | Coastal stills generated
Three Sunburst stills from the coastal drone-reveal guides cost 8.25 HF (matching the quote), and all three passed first time. Recorded in [[blender-blockout-pipeline]] and the job's JOB.md. gen-runner now takes two `--image` refs per row.

## [2026-10-26] ingest | Coastal v3: believable house + flown drone move
Hunter rejected v1 (house not believable, drone move bad). Added screens, extras and per-level wall material to the kit house generator, plus `rot_keys` gimbal cameras. Rebuilt the house with real articulation and the camera as an eased rise-and-push, and rendered a grey motion preview. The v1 stills (8.25 HF) are superseded. See [[blender-blockout-pipeline]].

## [2026-10-26] lint | Coastal audit + approval workflow
Hunter switched Blender work to an approval-based workflow: audit, then a staged proposal, then execution only of the approved stage. Audited coastal v3 read-only (no changes); the audit views are in `projects/blender-blockouts/coastal-test/audit/`. Standing rule added to [[blender-blockout-pipeline]].

## [2026-10-26] lint | Coastal stage A fixes
Hunter approved stage A (A1–A5) only. Fixed the alfresco balustrade and posts, the pool and entry planting clashes, added a lounger under the floating figure, and stopped the driveway at the lot boundary. The diff confirmed nothing else changed. The kit `alfresco` now takes `edge` and `post_height`. Guides were not re-rendered. Details in the job's JOB.md.

## [2026-10-26] lint | Coastal guides re-rendered
Re-rendered only the guide frames after stage A, as Hunter asked; the ID maps and motion preview were left as they were. Hunter has no reference for the house.

## [2026-10-26] lint | Coastal seated figure audit
The lounger figure was floating in an upright chair-sit pose and facing the house. Corrected live: it now faces the ocean, with thighs, soles and hands in contact, measured on the skin mesh. The fix is not persisted and awaits approval. Added the placed-asset contract rule to [[blender-blockout-pipeline]] and to auto-memory.

## [2026-10-26] ingest | Kollosche brand + video pack
Hunter downloaded Kollosche's video asset pack: 476 files, about 1.5 GB. Sorted into `raw/kollosche/`: guidelines, brand-logos, overlays, templates-psd, fonts, examples, end-cards, and team-logos/<agent> for 32 teams. Seven byte-identical re-downloads went to `_duplicates/`. The EPS/AI/PSD/OTF masters are gitignored, and the SVG/PNG/PDF files (~12 MB) are tracked. New pages [[kollosche]] and [[kollosche-video-guidelines]]. Key rules: the K opens every video and never closes it, Söhne Breit Kräftig supers, navy-overlay outro with no logo, auction and Agent Focus variants. Flagged: the pack has four caption specs that disagree (PDF Kräftig 40, example Kräftig 45, Premiere screenshot Leicht 48 with a navy box, our FCP SOP Kräftig 67). Söhne Breit is not yet installed. No spend.

## [2026-10-26] ingest | Architectural scene quality rules
Hunter's standing rule set was filed raw, summarised in [[blender-blockout-pipeline]] and folded into auto-memory. The first check of the seat fix against it found that the soles and the lounger sit 20 mm inside `Lot_Lawn`, which corrects the earlier "paving" claim. It also found the figure is fully hidden from the approved camera at every guide frame.

## [2026-10-26] lint | Coastal lounger raised 20 mm
Approved. The lounger and rig now sit on `Lot_Lawn`, with a 0 mm gap and no skin below the lawn or inside the seat. The fix is live only and not persisted.

## [2026-10-26] lint | Coastal seat fix persisted
The pose and the 20 mm raise went into the spec, and the kit `people` module gained `pose` overrides. Checkpoints were saved first. The headless rebuild matches the live measurements, and nothing was rendered.

## [2026-10-26] update | Kollosche IG handles verified
Hunter screenshotted the profiles: @kollosche_, @taylorkleinberg_kollosche, @thibaultparolini_kollosche. Added to [[kollosche]], plus a 13 Mayra Court posted-work line. Corrected a draft caption that tagged @kollosche.com.au (the email domain, not a handle).

## [2026-10-26] lint | Coastal outputs refreshed
The guides, ID maps and grey motion preview (v4) were re-rendered from the current spec. Nothing in the scene changed, and no credits were spent.

## [2026-10-26] update | @10xrealestate_ profile polish
Bio rewritten to "Property film and photography / By @10xvisuals_" (Hunter wants prestige, nothing that sounds AI). Grid audited, and 5 highlight covers made (black with white Poppins, in projects/10xrealestate-ig/highlights/). Instagram web can't pin posts, edit links or the contact button, or create highlights, so those are listed for the phone in projects/10xrealestate-ig/PHONE-TODO.md.

## [2026-10-26] lint | Coastal C3 ocean-side shot added
The C3 framing was approved and added to the spec as a second timeline slot, with C2 untouched (≤0.84 mm of shake jitter). A grey preview was rendered, with no AI and no credits.

## [2026-10-26] lint | Coastal C4 ground push-in added
This is the first ground-gimbal move: a 28 mm walking push-in through the dune grass to the seated figure. It was added as the third timeline slot, with C2 and C3 untouched, and a grey preview was rendered. No credits were spent.

## [2026-10-26] lint | Coastal stage C (lighting, ocean, solar, pool fence)
One sun, with the HDRI rotated and the lamp matched by the kit. A sphere probe confirms the two agree within 0.1°. The ocean fallback colour is fixed in the kit, the solar panels sit on rails, and a 1.2 m frameless glass pool fence was added as a new kit option. Two of my own errors were caught and fixed: a scope creep into the glass and water roughness, and a flawed support ray.

## [2026-10-26] lint | Coastal stage C closed
All guides and ID maps were re-rendered for C2, C3 and C4. The pool fence is hidden in ID maps by kit design (like balustrades), so prompts must name it. Next is stage D (AI), which needs a quote first.

## [2026-10-26] harvest | @10xrealestate_ carousels v5.2 + posting planner
Built 5 listing carousels: Cylinders, Solis, Pottsville townhouses (merged), Australis, and Somerset (new, Whitefox). Fixed the real suburbs: Mermaid Waters, Pottsville, Mudgeeraba. Planned 12 posts from 28 Oct. Hunter approved the design system, which is saved to auto-memory `template-10xrealestate-carousel.md` and the new [[10xrealestate-ig]] page. New standing rules: punched-in drones OK, no view drones, construction jobs stay off this page, merge identical shoots.

## [2026-10-26] build | 10xConstruction carousels + both posting queues in Finder
@10xrealestate_ has 11 posts in `Posting for 10xRealestate/Ready to Post/`, plus a 00 profile and highlights folder. The Cylinders main went up 26 Oct, so its reel moved last. Construction: Broncos Leagues Club deck is ready, the Grandview reel needs its builder handle, and Kennedys (Salisbury) is built and held for Murph. The Shape hotel set isn't identified yet. Construction stays on the original blue. Notes are in `projects/10xconstruction-ig/README.md`.

## [2026-10-26] build | Every shot set → carousels (Drive pull)
Inventoried 37 client folders on the Drive and pulled 47 finished shoots (12.4 GB) to `~/Documents/10x Drive Pulls/`. Built 21 REA decks (@10xrealestate_ posts 12 to 32) and 21 construction decks (14 queued as posts 04 to 17, 7 held). Ready to Post folders, captions, and planners are done for both pages. Web research fixed four address typos. Unverified handles and the holds are flagged in each READ ME. See [[10xrealestate-ig]].

## [2026-10-27] ingest | Kollosche day-to-night intake (Villas on Esther)
4 clips (4K, 1.5–3.5 s) triaged; Seedance video_modify prompts written to projects/kollosche-day-to-night/prompts.md. Nothing spent.

## [2026-10-27] ingest | Kollosche K pin + logo/super specs
Built a K location pin for 9:16 wide drone shots (`projects/kollosche-pin/`, PNG + ProRes 4444 alpha, $0). Measured the 16:9 logo and address super specs into [[kollosche-video-guidelines]]. The pack's `svg_Kollosche…` files turned out to be Kara Christensen team logos; they were refiled, and clean wordmark PNGs were extracted.

## [2026-10-27] ingest | Kollosche townhouse drone graphics
Made a tracked white lot outline on the top-down Main.mp4 and a roof-locked K pin on the wide View.mp4, both local and $0. The plate-vfx drone fit failed on Main (fast spin and motion blur in the first frames). Chained SIFT homographies from the sharp last frame worked instead, which is the right model for a straight-down shot. In review with Hunter. Job: projects/kollosche-drone-graphics/JOB.md.

## [2026-10-27] harvest | Kollosche townhouse drone graphics delivered
Hunter approved the tracked lot outline and the roof-locked K pin. Status set to delivered in JOB.md and [[kollosche]]. Lesson: for straight-down shots that open on a blurred spin, chain homographies back from the sharpest frame instead of running the drone fit. No spend.

## [2026-10-27] ingest | Kollosche outro generator + Eddie Wardale outro
Built `projects/kollosche-outro/make_outro.py`, which copies Kollosche's own end card (HarfBuzz kerning; the --check re-render matches within 0.2 % of pixels). Rendered Eddie Wardale's outro in 16:9 + 9:16 for the townhouse job. Flagged that Taylor Kleinberg's number differs between the end-card files and the guidelines. No spend.

## [2026-10-27] query | Kollosche reel opening
Recent Kollosche reels open on the K only, with no address super. This contradicts the 2024 guideline PDF and is flagged in [[kollosche-video-guidelines]]. Default for reels is now K only.

## [2026-10-27] ingest | Drone photo pinning tool
Built `projects/drone-pin/`, which auto-places the K pin and the surveyed lot outline on DJI stills using drone XMP data and the QLD cadastre, with a browser review page and render step. Tested on 7 Somerset Dr photos. Found that DJI GimbalYawDegree is 39–55° off, so the tool uses FlightYawDegree. Page: [[drone-photo-pin]]. No spend.

## [2026-10-27] harvest | Esther Pl drone stills delivered, plus drone-pin tool v2
Delivered the Kollosche 5 Esther Place drone stills (6 photos, Print and Web, with pin and outline) at $0. The tool gained hand-edit tools (draw outline, razor, lasso and behind brush with eraser, zoom), export panel, ZED blackout with Bright lasso, and `Drone Pin.app`. Rules learned:
- Kollosche pins the prints and doesn't want top-downs.
- ZED blacks out everything outside the house.
- The app's preview pane blocks `confirm()`.
- Lightroom's EXIF thumbnail fools Finder into showing the clean photo.

Next is Coastal. Page: [[drone-photo-pin]].


## [2026-10-27] ingest | SFX lifted from a reference reel via Demucs
Demucs is installed locally (free). It split the snapgram reel and 32 candidate hits were cut at the scene cuts into SFX Library/_Incoming. Method and caveats are on [[sfx-library]]. No spend.

## [2026-10-27] ingest | Drone Run browser game
Three.js drone game with a Blender-built DJI-style drone and house variants, 0cr. Page: [[drone-run]].

## [2026-10-27] ingest | Street Racer browser game
A 3-lap racer against AI cars, with a Blender-built car and reused houses, 0cr. Page: [[street-racer]].

## [2026-10-27] ingest | Street Racer v2 Night GP
Night stadium, real Huracán x6, drift and smoke, the Huracán recordings as engine audio, bloom. 0cr. Page: [[street-racer]].

## [2026-10-27] ingest | Street Racer v3 Garage
A Forza-style garage with 14 real cars (new-gen BMW M included) baked by a headless Blender pipeline. Paint, finish, wheels, tune, smoke and underglow, a handling rewrite, the folded-track map fix, exhaust spit flames and a drift scoring mode. 0cr. Page: [[street-racer]].

## [2026-10-27] ingest | Street Racer v4 F1 circuit
A harder F1 layout with hills, crests and jumps, a forest, tyre walls and hills around it. Compressed GLBs, fixed wheel pivots and backwards cars, removed the start-line bar, softer steering. 0cr. Page: [[street-racer]].

## [2026-10-28] ingest | Street Racer v5 pits and strategy
A working pit lane, tyre wear and fuel, 5-lap races, AI with braking-distance planning, a racing line, overtakes and its own pit stops, plus a realism pass (racing line, skyline, contact shadows). 0cr. Page: [[street-racer]].

## [2026-10-28] update | Street Racer v6: spinning wheels on all cars, paint/light pass

## [2026-10-28] update | Street Racer v7: 3 maps, story mode, per-car engine synth, harder AI, R34/AE86/M3 fixes

## [2026-10-28] build | Drone pin: client style profiles + auto-align attempts
Per-client style profiles (clients/*.json, 10 clients from a Drive/SSD research sweep), client and address read from the "Client | Address" folder name, agent overrides, ZED's B&W surround, plus ring/disc/mark pins with a line dot. Kollosche output is pixel-identical. Four auto-align methods were tested; none beat a hand drag. See [[drone-photo-pin]].

## [2026-10-28] query | Floor plans as delivered, per client
Pulled one finished plan per client from the Clients Drive (YPA, RE/MAX, The Agency, Belle, Place, Ray White, Coastline, ZED, Harcourts). Found two template generations, per-client logo and agent blocks, and errors that shipped. See [[floor-plan-house-style]]; contact sheet in projects/floorplan-app/refs.

## [2026-10-28] decision | Floor plans: the Oct 2026 template is the 10x standard
Hunter picked Gen B (aerial site plan, m units, title-case area strip) as the standard for the in-house floor-plan app. See [[floor-plan-house-style]].

## [2026-10-28] build | Floor-plan app milestone 1 + 8 CubiCasa sources
Pulled 8 CubiCasa exports from the CubiCasa web account into raw/floorplans/cubicasa, plus 3 supplier finals. Built fp.py + review UI: untrusted-SVG sanitiser, house-style label proposals with human sign-off, areas from CubiCasa text, geometry-unchanged check. Found the supplier area method is inconsistent (walls/garage added on some jobs). See [[floorplan-app]].

## [2026-10-28] project | Floor-plan app milestone 2: 10x A4 page
render.py skins the CubiCasa SVG (true-scale textures, charcoal walls, Poppins labels) and builds the full A4 page with PDF/PNG export; multi-storey plans laid out side by side at one scale. Geometry check passes on all 8 jobs. Open: area rule, north, client logos. See [[floorplan-app]].

## [2026-10-28] ingest | Katrina Walsh (Coastal) profile, video formula and song shortlist
Hunter confirmed that "Coast" means COASTAL° (coastal.com.au) and that it is a different agency from Coastline Prestige. Pulled Katrina's public profile, headshot URL, socials and listings. Studied her IG listing films: the cold open, the COASTAL° wordmark at ~5–9 s, VO with white subtitles, the name and number sunset outro, and the charcoal end card. Credited audio on her reels: Buddha Code "Moment of Peace" and Tony Batts "To Live Again". Found Coastal's drone pin style in the listing photos (white C° on a stem, thin white lot outline). Built a slow earthy shortlist, with 7 of 8 tracks already in the 10x music library. Nothing is on the Clients Drive for Coastal and nothing was downloaded. New pages [[katrina-walsh]] and [[coastal]]; [[drone-photo-pin]] updated.

## [2026-10-28] ingest | Coastal logos
Downloaded the COASTAL° wordmark (white, black and legacy PNGs) and the C° favicon from coastal.com.au into raw/coastal/. Derived a white transparent C° pin mark at projects/drone-pin/logos/coastal-c-white.png. Hunter didn't need Katrina's headshot, so it isn't stored. See [[coastal]] and [[katrina-walsh]].

## [2026-10-28] lint | Katrina Walsh "PRESENTS" title card
Hunter supplied screenshots of her "KATRINA WALSH / PRESENTS" title card (white, centred, thin name over a heavier smaller PRESENTS, laid over footage) and of her charcoal end card. The first pass had mistaken the COASTAL° wordmark for the "presents" beat; this is corrected and flagged on [[katrina-walsh]].

## [2026-10-28] ingest | Coastal balcony day-to-night intake
One shot (Day.mp4, 3.09 s 4K, under 4 s so it needs a re-export). The reference is the same shot already at dusk (Main.mp4). Job at projects/coastal-day-to-night/JOB.md.

## [2026-10-28] project | Katrina Walsh title and end card rebuilds
Rebuilt her "KATRINA WALSH / PRESENTS" title (transparent) and the charcoal end card as 4K PNGs in Helvetica Neue Light and Medium, with the Coastal white wordmark. Script and outputs are in projects/coastal-katrina. See [[katrina-walsh]].

## [2026-10-28] project | Katrina Walsh animated end card and Coastal C° pin
Added animate.py, which renders an 8 s animated end card (the background fades up, then name, number and logo ease in) and a 5 s Coastal pin (the stem draws up, then the C° lands). Both are 4K ProRes 4444 with alpha. The pin size was checked against Coastal's own Lita Ct drone pin. The address treatment is still to be decided: Coastal pins carry no label. See [[katrina-walsh]].

## [2026-10-28] project | Coastal address caption for 34 Albany Avenue, Currumbin
The suburb was confirmed from the QLD address register. Added an address mode to animate.py that makes a caption in her subtitle style (white Helvetica Neue in sentence case, lower centre), as a PNG plus a 5 s alpha MOV. See [[katrina-walsh]].

## [2026-10-28] project | Kollosche pin, navy K version
At Hunter's request (relayed by another session), added a navy option to make_pin.py. The K now comes from the official navy wordmark, the only blue logo on file, with no recolouring. Re-rendered the long and short PNGs and ProRes 4444 MOVs with a -navy suffix; the white originals are kept. See [[kollosche]].

## [2026-10-28] project | Kollosche pin redone with the boxed photo badge
Hunter corrected the navy-K version: the pin head should be the navy boxed K badge from the drone stills. The tracked View clip and the generic 9:16 pin now draw the head with drone-pin's badge() and the kollosche.json style, so it matches the photos. Re-rendered both with a _badge suffix and kept the earlier versions. See [[kollosche]].

## [2026-10-28] build | Auto Sound Design MVP
Built `projects/auto-sound-design/`, a local Python + FFmpeg tool. It takes a video and an owned SFX folder and makes a sparse heuristic SFX pass, delivered as a preview, an SFX-only WAV, FCPXML 1.10 (DTD-valid, not import-tested) and `edit_decisions.json`. 31 tests pass. Real run on the Davenport hero: 8 effects over 41 cuts, with peaks within half a frame. Real media changed four defaults: longer whoosh length, per-category peak caps, skipping `_` folders, and the hot-master warning. See [[auto-sound-design]].

## [2026-10-28] build | Auto Sound Design: test sections + Kollosche Esther Pl test
Added `--start` keyframe-exact test sections (frames byte-identical), `…_SOUND-MIX.mp4` as the main output, `sfx_used/` copies and `relink` for the Mac. The Kollosche Main.mp4 section 16.7–43.8 s got 4 effects and was sent to Hunter for review. The YouTube style reference is blocked by the network policy. 33 tests pass. See [[auto-sound-design]].

## [2026-10-28] build | Auto Sound Design: dense preset, full Kollosche renders
Sent Hunter the full 87 s Kollosche mix: default (9 effects), then `presets/dense.json` (44 effects). Added file rotation, a fallback to the next file when one doesn't fit, and tail trimming. Hunter is downloading the "desire" reference video to upload. See [[auto-sound-design]].

## [2026-10-28] build | Auto Sound Design: tasteful preset
Hunter wants SFX tasteful, not over the top. Added `presets/tasteful.json`; the Kollosche full run placed 19 effects. "Sound bite" SFX generator not verified, so asked which product. See [[auto-sound-design]].

## [2026-10-28] build | Auto Sound Design: scene maps + ambience
Hunter liked the tasteful pass and wants scene-specific SFX plus audible ambience. Claude reviewed 55 shots and wrote a Kollosche scene map. Added per-scene ambience beds, presenter keep-clear, map accents (sun flare, K pin), and a free synthetic ambience kit. The beds were raised from about -20 dB to about -13 dB under the music. 37 tests pass. See [[auto-sound-design]].

## [2026-10-28] ingest | Desire Media "The Pilot" reference
Broke down Desire's Kollosche film (65 shots, 16 transition strips, per-cut audio signatures) into [[desire-the-pilot-reference]]: whooshes on about 1 in 5 cuts, on motion; 2–5 big hits; whip, pillar-wipe and lights-on transitions; lifestyle talent. The tool gained `existing_sfx` (it found 6 effects already in Hunter's Esther Pl edit) and `cut_motion`, and the tasteful preset was retuned. See [[auto-sound-design]].

## [2026-10-28] build | Auto Sound Design v6 after "sounds so bad"
v5 was rejected as too much, especially on interiors. v6 places whooshes only on zone changes (outside/inside/aerial) or camera motion, drops interior ambience and runs quieter: 8 one-shots in 87 s. Hunter flagged that Desire's talent is AI, a possible AI-lifestyle-talent thread. See [[auto-sound-design]].

## [2026-10-28] decision | Synthetic ambience rejected; real recordings needed
Hunter: the ambience doesn't sound good and the wind isn't wind. Day shots get birds and night shots crickets. Every free SFX source is blocked by the cloud network policy, so recordings must be uploaded or the domains allowed. The tool now prefers recorded beds over synthetic, and the aerial wind is off. See [[auto-sound-design]].

## [2026-10-28] build | Auto Sound Design v7: real ambience, preview only
Only GitHub, PyPI and npm are reachable. Pulled birds, crickets and wind from a GitHub "CC0" repo that bundles third-party audio, so they're preview-only and flagged by a new licence warning. Kollosche v7 sent. Delivery needs owned recordings. See [[auto-sound-design]].

## [2026-10-28] build | Auto Sound Design v8: Desire matched by measurement
Desire is -16.2 LUFS with LRA 5.4 and whooshes on 11% of cuts; Hunter's edit already has 19%. v8 counts his own whooshes in the budget and masters the preview to -16 LUFS / LRA 6.3. Sent. See [[auto-sound-design]].

## [2026-10-28] build | Auto Sound Design v9: flavour accents + music-cut smoothing
Found the hard music cut at 42.17 s (the highs return after the dusk section) and smoothed it with a reverse swell from the incoming music plus a filter sweep. Added click/pop foley and on-screen accents (flash, pin, tilt, title, end card) that layer above the density caps. Sent v9. See [[auto-sound-design]].

## [2026-10-28] query | Why Desire's colour looks premium (measured)
Desire has a shadow floor of L 7.5 against our 17, contrast 73 against 60, chroma 12.7 against 17.6, neutral shadows against yellow ones, and 29% cool hues against 4%. A test grade (`grade/desire-match.ffmpeg.txt`) hits the targets except mid yellow. The K pin glint became a soft whoosh. Filed in [[desire-the-pilot-reference]].

## [2026-10-28] build | Auto Sound Design v11 + Desire-match LUT
The 42.17 s music return is now rebuilt phrase-aligned (the music after it was 180 ms off-grid) with a 1-bar filter and level opening, and the fix is exported as a music clip plus a source mute in the XML. Impacts lock to the music hit, whooshes lead the cut by 40 ms, and a day→night ambience story was added. Colour v2 is a statistical-transfer .cube LUT (75%); the ffmpeg grade was rejected as "fucked". See [[auto-sound-design]].

## [2026-10-28] query | Music cut cause + next test video
The 42 s stumble was Hunter's own hand-shortening of the song. A bar-aligned "music fitter" is proposed. A slower, earthy pool/drone edit is coming 29 Oct as the next test. See [[auto-sound-design]].

## [2026-10-28] decision | Keep Hunter's grade; the Desire-match LUT reads as dark
Hunter prefers his own grade on Kollosche Esther Pl. New rule: colour help keeps his brightness and only fixes consistency. See [[auto-sound-design]].

## [2026-10-28] ingest | FCP → Resolve Studio grading workflow
Hunter owns Resolve Studio; Desire grades in Resolve. Wrote [[fcp-resolve-workflow]]: a graded-master path (survives speed ramps and titles) and an XML round trip, project colour settings, a 10x node tree that keeps the brightness, and Studio tools. Draft until run once.

## [2026-10-28] build | Grade assistant (Resolve numbers per shot)
`grade/assist.py` gives per-shot Gain R/G/B matched to the film's own white level and warmth, interiors only, never darkening. Kollosche demo: 13 of 55 shots flagged. Added to [[fcp-resolve-workflow]].

## [2026-10-28] query | Log export, Resolve MCP, PowerGrade, FL Studio
A log master needs FCP's Camera LUT set to None, and Resolve sets the input space per shot. Community Resolve MCP servers exist (Studio scripting), which makes it possible to push CDLs from the grade assistant on the Mac. FL Studio has no practical automation route; sound design from Hunter's library in code is the better path. See [[fcp-resolve-workflow]].

## [2026-10-28] decision | Grade in FCP for now
Hunter doesn't know Resolve. The grade assistant now gives FCP Color Wheels instructions per shot; Resolve waits for MCP automation on the Mac. See [[fcp-resolve-workflow]].

## [2026-10-28] build | Resolve bridge
`grade/resolve_bridge.py` takes the flat master and grade-assist JSON and builds a per-shot Resolve timeline with the house PowerGrade, CDLs and a drone LUT. Dry run and fake-Resolve tests pass (40 tests); untested on a real Resolve. See [[fcp-resolve-workflow]].

## [2026-10-28] build | Grade assistant: hero shots
Hunter's next grade is good on some shots only. `assist.py --contact-sheet` numbers the shots; `--heroes` makes his picks the reference, and the look LUT is learned from those pairs. See [[fcp-resolve-workflow]].

## [2026-10-28] build | Desire look matched per shot type
`grade/desire_match.py` builds per-type LUTs (interior, exterior, aerial, dusk) with midtones locked. Kollosche gets brighter whites, more contrast, less yellow, and isn't darker. Sent a preview, the 4 LUTs and stills. See [[fcp-resolve-workflow]].

## [2026-10-28] build | Desire match v4 (per-type tuning)
After "inside too dark, outside too bright, drone far away": interiors +5 L, exteriors and aerials get a highlight roll-off, and aerials take tone only, not colour. Sent v4. See [[fcp-resolve-workflow]].

## [2026-10-28] decision | Automated Desire colour match parked
Hunter preferred his own colours on most shots, and the matches didn't read as Desire. His grade stays; colour tools are kept for consistency only. See [[fcp-resolve-workflow]].

## [2026-10-29] ingest | Coastal 34 Albany: sound pass, CG birds, tracked pin, Einaudi reel cut
First Mac run of auto-sound-design (layered beds, earthy preset, stems); plate-vfx 4K gate fix; new page coastal-albany-birds.

## [2026-10-29] ingest | Cinematic Reel: Wildfire fitted to picture, reel SFX + shing, Get Down cut
Wildfire (C. James) hit placed on the 22.11 aerial; reel scene map + near-silent existing-sfx fix; reel_mix.py hand-accent shing; Get Down flythrough cut 36.9 s. See [[auto-sound-design]].

## [2026-10-29] ingest | Cinematic Reel: tracked C° pin + 9:16 start/end cards
Re-tracked the reel's coast-wide drone (gate now long-side), pin at 1.4x for vertical, reel_cards.py for Katrina Walsh cards. See [[coastal-albany-birds]].

## [2026-10-29] ingest | Get Down punchy cuts A/B
Chorus-heavy flythrough cuts after Hunter's 'more punchy' note. See [[auto-sound-design]].

## [2026-10-29] ingest | Flythrough VO fitted to Get Down
Katrina's VO transcribed (local Whisper), cleaned, trimmed; Get Down re-cut to 67.5 s, instrumental bed ducked under her. See [[auto-sound-design]].

## [2026-10-29] ingest | Flythrough VO polished (tightened pauses, voice chain), song re-fit 61.5 s
New tools/vo_polish.py. See [[auto-sound-design]].

## [2026-10-29] ingest | Flythrough VO cut to a 37.8 s reel
Fluffed bedrooms line + spec/birdlife/balcony lines dropped (vo_polish --drop); Get Down re-fit 22 -> 60. See [[auto-sound-design]].

## [2026-10-29] ingest | Flythrough reel flow plan + 6 pop-ups
Stem-tag pop-ups (9:16 alpha), cue sheet on VO words/song beats. See [[auto-sound-design]].

## [2026-10-29] ingest | Coastal 34 Albany flythrough reel: SFX pass
SFX-only pass on Hunter's cut `Flythrough.mp4` (36.04 s, 9:16). Scene map `projects/auto-sound-design/scene-maps/coastal-flythrough-reel.json`. 24 effects placed; the two approved whooshes are pinned at 8.09 s (outside → inside) and 16.27 s (inside → pool). Stems are in Desktop `Coastal 34 Albany - FCP/10 Flythrough SFX`.

## [2026-10-29] job | 4-6 Buckingham Way Elanora drones (Kollosche)
Reviewed the 5 drone stills: good to deliver. Pinned the 3 high wides with the Kollosche K badge. QLD cadastre was down, so the pins were placed by hand and there is no outline yet. Print and Web are on the SSD in `Drone Photos Pinned`. See [[drone-photo-pin]].

## [2026-10-30] project | Coastal 34 Albany Flythrough start + end cards
Put the existing COASTAL° start card and Katrina end card on Hunter's new Flythrough export, saved as "Flythrough - start + end cards.mp4" next to the original. The pin was already done. The folder name "43 Albany" is a typo for 34. See [[coastal-albany-birds]].

## [2026-10-30] ingest | Weemala 702 re-render attempt — parked
Tried to re-angle + refurnish 11 AI'd Print/Web stills (architect legal ask). NB 2.1 with own-room ref keeps layout but won't move the camera; bundled refs blend rooms; Magnific change-camera moves the camera but invents space; Blender blockout from stills too imprecise. Spent 42 HF + ~150 Magnific cr. Hunter called it: not working. Files in projects/coastal-weemala-702.

## [2026-11-02] music | Osupa Ti 64 s Kollosche cut (bar-aligned, vocal-gap splices)

## [2026-11-02] music | Low Again 75 s cut + niche-song YouTube shortlist

## [2026-11-02] music | No Bad Vibes 69 s cut (no splices, echo-out ending)
## [2026-11-02] ingest | Osupa Ti 30 s reel cut (osupa_30.py)

## [2026-11-02] ingest | Kollosche 4-6 Buckingham Way overlay pack
Hunter's 63 s edit got the opener (wordmark + address), a tracked lot outline, K badge pins, gulls and Taylor Kleinberg's outro. Delivered as 5 full-length ProRes 4444 alpha overlays for FCP, saved beside the original on SSD1. Taylor's number is now confirmed as 0447 466 177. Pages updated: [[kollosche]], [[kollosche-video-guidelines]]. $0.

## [2026-11-02] ingest | Kollosche Buckingham Way v2 (Hunter review)
Hunter cut the end pin and the gulls, and called the eyeballed lot outline wrong. The outline was rebuilt from his delivered Web-02 still (SIFT-registered, matches QLD cadastre 130RP206900). New rule: lot outlines come from his pinned stills or the cadastre. Pages updated: [[kollosche]], [[plate-vfx]].

## [2026-11-02] ingest | Kollosche Buckingham Way SFX pass
auto-sound-design was run with the locked preset and a scene map whose accents are timed to the overlay events. Delivered as 05 SFX WAVs beside the overlays, plus a preview with sound. Pages updated: [[auto-sound-design]], [[kollosche]].

## [2026-11-02] ingest | Kollosche Buckingham Way: SFX voice fix + birds v2
SFX: the voice was the spoken Kollosche transition tag plus Ocular City Park walla. Both are removed, and the stem is now Whisper-checked. Birds were redone in the sky with the new plate-vfx `--sky-y` option. Pages updated: [[plate-vfx]], [[auto-sound-design]].

## [2026-11-02] ingest | Kollosche Buckingham Way: cicadas out of the SFX
The Provence beds were cicada loops. Beds are now owned Pixabay birds only, verified by a high-band measurement and Whisper. Page updated: [[auto-sound-design]].

## [2026-11-02] ingest | Kollosche Buckingham Way reel: overlay pack
9:16 overlays (K icon, Web-06 outline + pin, sky gulls, Taylor outro) + SFX beds/whooshes, delivered beside Reel.mp4. Pages: [[kollosche]].

## [2026-11-02] ingest | Kollosche Buckingham Way reel: pin only
Outline cut from the reel's pin shot per Hunter. Rule: pin shots get the pin alone. Pages: [[kollosche]].

## [2026-11-02] ingest | Kollosche Buckingham Way: hard-cut opener, Thibault on the outro
Wordmark and address are now separate layers with a hard cut. Thibault Parolini added to the main + reel outros. Pages: [[kollosche]].
## [2026-11-03] ingest | November Kid 60 s + 30 s reel cuts
## [2026-11-03] ingest | November Kid 45 s cut

## [2026-11-03] build | Floor-plan app: site plan from address (cadastre + QLD aerial), Robina labels/fit
## [2026-11-03] build | Floor-plan app: roof-trace site plan (trace page + code drawing); AI repaints rejected as inaccurate
## [2026-11-03] ingest | Broken Plans 60 s cut + onset-refit grid lesson
## [2026-11-03] ingest | Broken Plans 60 s v2 (drop at 8.9 s for establishing shots)
## [2026-11-03] ingest | Broken Plans v3 (drop 16.8 s, 68 s)

## [2026-11-04] ingest | @10xvisuals_ main-page carousels
Built 4 editorial decks (Kollosche x2, Whitefox, Kodiak) from Frame.io Print sets; cut Buckingham + Marine Pde. Page: [[10xvisuals-ig-carousels]].

## [2026-11-04] ingest | Carousel layouts B+C, SHAPE construction decks
Added Gallery/Magazine layouts to build_carousels.py; 6 SHAPE venue decks on the construction page; Belle checked on Drive, nothing editorial. [[10xvisuals-ig-carousels]]
## [2026-11-04] ingest | wildfire (origins) 30 s hype cut + tempo-trap lesson
## [2026-11-04] ingest | wildfire (origins) hype v2: one join, chorus 3 drop, natural decay ending
## [2026-11-04] ingest | wildfire hype v3: punchier start (drop 2.0 s, louder pre-drop FX)

## [2026-11-04] ingest | Main-page carousels batch 3
5 more listing decks + Westside HQ and Lions @ Springwood added to @10xvisuals_ carousels.

## [2026-11-04] ingest | Trivelle Beauty launch build
4-in-1 device ads, 8 store graphics, launch checklist, store copy, packaging draft. New page [[trivelle-beauty]].

## [2026-11-05] ingest | ZOYA Pulled Under song cut, join drift lesson

## [2026-11-05] ingest | SFX toolkit installed (Real SFX, Earshot, SFXMint, Openverse)

## [2026-11-05] ingest | 42 Salerno St listing: lot outline + K pin + graphics composite
New page [[salerno-st-listing]]. Overlays from d4a7af65 QC'd; full composite Main_Kollosche_graphics.mp4 → SSD Edits/Graphics/.

## [2026-11-05] lint | Salerno outline v2
Hunter rejected the v1 outline: it was a hand-fit registration and 21 px thick. Rebuilt with ortho→ECC cadastre registration, the auto-detected kerb and the 13 px spec. Lesson added to [[salerno-st-listing]].
## [2026-11-05] ingest | on rewind 30 s flythrough reel (zero joins) + brute-force grid lesson
## [2026-11-05] ingest | on rewind 40 s reel (zero joins)

## [2026-11-06] query | Salerno St drone stills pinned (auto) — metadata-stripped edits recovered from raw DNGs

## [2026-11-06] query | Trivelle round 2: Sculpiflex research, honest persona + real trial plan

## [2026-11-06] query | u know (Civilian) 60 s main edit — first song cut checked by Earshot, Ocular FX

## [2026-11-06] ingest | REAL Specialists: Connor Hewitt moved there; brand + drone pin style researched

## [2026-11-06] ingest | 21 Albany Ave Currumbin day-to-dusk intake
One 12.9 s ground walk-in (Day.mp4), with Main v2.mp4 as the dusk look reference (a different take). The route is the Coastal balcony one: NB 2.1 still, then Kling Omni Edit 4K. Quoted at about 75 HF, waiting on a go. Job at projects/albany-21-day-to-night/JOB.md.

## [2026-11-06] update | Drone Pin: NSW cadastre lookup (Tweed jobs) + place_color/place_dist label keys; REAL Specialists profile completed

## [2026-11-06] update | REAL Specialists video overlays
Added projects/real-specialists-overlays/make_overlays.py, which renders a logo opener, an address super and an orange agent end card as ProRes 4444 alpha in 16:9 4K and 9:16. It uses Lato (OFL, vendored) and the traced logo. A test render used a placeholder number because Connor's mobile is still needed. Documented in wiki/clients/real-specialists.md.

## [2026-11-06] update | REAL overlays rendered for 21 Albany Ave, Currumbin
The final pack (Connor Hewitt, 0451 514 962) is in /Volumes/10X SSD3/21 Albany Avenue, Currumbin/Video/REAL Overlays/.

## [2026-11-06] ingest | 21 Albany Ave day-to-dusk video delivered
The Day walk-in was relit to dusk:
- A Nano Banana 2.1 still (3 HF).
- Magnific Kling 4.0 `video_modify` at 1080p (4,290 cr; Higgsfield Omni had no credits).
- A local 4K lanczos upscale, retimed to 23.976.

The motion is frame-locked (under 0.5 px). The charcoal walls drift olive under the warm light. The 4K file and a side-by-side are on SSD3 under Twilight Examples. Page: [[albany-21-day-to-night]].

## [2026-11-09] query | Fire Fire 30 s reel — Earshot 22/22, one join, song's own stop

## [2026-11-09] ingest | 21 Albany Ave Main: SFX + REAL pin
The edit had no baked-in SFX. Added 24 calibrated scene beds, 4 whooshes (the approved Coastal picks) and a soft flare, plus a fixed wind bed under the silent tail. The REAL pin is tracked on the wide drone at 36.37 s, with the house confirmed by the cadastre and the QLD aerial photo. Delivered to the SSD under Exports/SFX and Video/REAL Overlays. $0. Page: [[albany-21-main-sfx]].

## [2026-11-09] update | 21 Albany Reel ambience
The reel got ambience only (Hunter did the whooshes and shings): 17 outdoor beds, and silent interiors per Hunter's new no-birds-inside rule. Delivered to Exports/SFX. Page: [[albany-21-main-sfx]].

## [2026-11-09] update | 21 Albany Main new flow
The re-export (boss's flow change) got outdoor-only ambience with silent interiors. The REAL pin overlay was reused because the drone shot is unchanged. Delivered to Exports/SFX, with the old files moved to _old flow. Page: [[albany-21-main-sfx]].

## [2026-11-09] query | Cinema (Judah Earl & boda) 60 s cinematic main edit — hit-to-hit cut, Earshot-shortened ending

## [2026-11-09] update | Drone Pin: Import button + REAL icon-only pin
The review page gets an Import… button (multi-file picker, any folder, per-photo `src`). REAL Specialists pins switch to the square icon only. The 21 Albany job had an empty marks.json; Print-8 and Print-9 are now loaded.
## [2026-11-09] query | Cinema soft variant: no-FX render, Earshot shows the trailer feel is the track itself
## [2026-11-09] query | Experience (Einaudi) 90 s soft cinematic cut for the big property, Earshot-picked + checked
## [2026-11-09] query | Cinema 90 s cut (FX + soft), one repeat join, Earshot close 18/22
## [2026-11-09] query | Cinema 90 s SFX sound-design pass (Ocular, Earshot-ranked, measured levels)

## [2026-11-09] ingest | Amir Prestige brand + drone style
Gathered the wordmark, "ap." monogram, teal #24506A and Garet from amirprestige.com.au, plus three drone references from their 44 Via Roma listing, into `raw/amir-prestige/`. Added the client page and drone-pin profile `amir-prestige.json` (white ap. pin, caps labels, mono surround). Test render matched.

## [2026-11-09] ingest | Amir Prestige listing video style
Broke down the 44 Via Roma YouTube film covering structure, supers, agent outro, black wordmark end card, grey-mat montage, lo-fi beat with no VO, and grade. Frames are in `raw/amir-prestige/video-refs/`, and the video section is on [[amir-prestige]].

## [2026-11-09] update | Amir Prestige overlay pack
Built `projects/amir-prestige-overlays/make_overlays.py`: logo opener, address super, "Bella Vista" property-name title, agent names, black end card and grey montage mat, in 16:9 4K and 9:16. A sample render is in `out/`.

## [2026-11-09] update | Amir overlays for 8 Nassau Ave, Terranora
Rendered the pack ("Bella Vista", address 8 NASSAU AVE, TERRANORA, placeholder agent "Agent Name / 0400 000 000") to T7 `8 Nassau Avenue Terranora/Amir Overlays/`. Re-render the 02 agents card once the agent is known. The SSD shoot folder is labelled "| Coastline".

## [2026-11-09] update | Amir "Bella Vista" title redone
The italic and swash version read tacky. It is replaced by restrained tracked Playfair caps with a hairline and small suburb caps (`--name-style caps`; `lower` and `roman` are alternatives). Re-rendered to T7 `8 Nassau Avenue Terranora/Amir Overlays/`, with an A/B/C comparison sheet.

## [2026-11-09] update | Amir title: Hunter picked B
The title is now lowercase "bella vista" (Playfair SemiBold) with a bolder, larger TERRANORA and no line. It is the default `--name-style lower`, re-rendered to T7.
## [2026-11-09] query | Cinema 90 SFX mid/side polish (ms_polish.py), critique 18 to 19/22

## [2026-11-10] query | Amir Prestige video endings
Checked the endings of 3 more of their YouTube films. They finish on agent names over a scenic drone, with no black card. Flagged this on the client page.

## [2026-11-10] update | Albany address super remade as 5 ALBANY LANE
The REAL Specialists 01b address super for the Albany video now reads 5 ALBANY LANE / CURRUMBIN, in 16:9 and 9:16, on SSD3 `21 Albany Avenue, Currumbin/Video/REAL Overlays/`. The old 21 Albany Avenue version is in `_old (21 Albany Avenue)/`.
