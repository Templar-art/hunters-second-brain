# Log

Append-only record of wiki operations. Entry format: `## [YYYY-MM-DD] ingest|query|lint|migrate | Title`

## [2026-07-10] migrate | Genesis — vault restructured to LLM-wiki pattern
Converted the vault to the Karpathy LLM-wiki structure (spec: `docs/superpowers/specs/2026-07-10-llm-wiki-restructure-design.md`). `memory/` retired and translated into `wiki/` (5 people, 5 clients, 6 projects/concepts pages); CLC pack PDFs + capability statement moved to `raw/clc/`; CLC pack markdown, audit, field research, and swipe file became `wiki/sources/` pages; CONTEXT.md → [[music-taxonomy]]; root notes → wiki/projects/; working artifacts (scroll demo, CVA breakdown, dashboard, TASKS) → top-level `projects/`; CLAUDE.md rewritten as the schema.

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
Hunter reported the vault "grew crazy," asked to connect all the nodes. Full orphan/dead-end sweep across all 92 wiki pages (inbound-[[wikilink]] count per page).

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
