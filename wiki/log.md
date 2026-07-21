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
