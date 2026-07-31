---
type: project
tags: [10x-visuals, website, design-system, prestige, lead-gen]
status: partial-release-committed-not-deployed
updated: 2026-07-31
---

# 10x Website

10x Visuals' own front door, `10xvisuals.com.au`. A WordPress site with real content and real case studies whose finish did not match the work it sells. Rebuilt on 30 Jul 2026 as six static pages against [[brand-system|Prestige DS v1.0]]: the homepage plus all five interior pages, generated from a script rather than hand-written.

**Build:** [projects/10x-site/](../../projects/10x-site/) · **Spec + outcome:** [design spec](../../docs/superpowers/specs/2026-07-30-10x-homepage-prestige-rebuild-design.md) · **System of record:** [DESIGN.md](../../DESIGN.md), Prestige layer

## What the site is

Six pages: home, `/branding`, `/content-creation`, `/lead-generation`, `/systems-processes`, `/contact-us`. Five real case studies ([[sol]] · Davenport · [[bespoke-estate-agents]] · Elysium · Broncos Leagues Club), sixteen named clients, one testimonial. Structure was sound. Skin, typography, rhythm and motion were not.

## What shipped

A single self-contained `index.html`: full-bleed **Stonehaven** aerial hero under the headline "Presentation decides the price.", a typeset client roster, six case-study plates alternating full-bleed and two-up, a parallax interlude, the four disciplines as hairline rows, founders, testimonial, and a three-field enquiry close. Works over `file://` and HTTP. Not deployed.

**Hero: Stonehaven**, 47 Somerset Drive, marketed by Whitefox: the late-afternoon aerial. It replaced the [[sol]] drone frame on 30 Jul, and then a dusk patio frame that Hunter rejected the same day. Work order is Stonehaven, Davenport + Bespoke, Elysium, then SOL + Broncos; SOL moved below Elysium at Hunter's request.

## What it taught us

**A handed-down design system can still be wrong, and measuring beats deferring.** Prestige DS v1.0 shipped four token values that fail WCAG AA on the surfaces they actually land on, including its own text blue at 4.39:1. Four amendments are now the real system, recorded under The AA-Amendment Rule. The lesson generalises: a token is only compliant on the surface it lands on, which is the [[brand-system|Surface-Not-Token Rule]] arriving for the third time.

**⚠️ Two of Hunter's systems contradicted each other.** Prestige DS v1.0 prescribes a tracked kicker and an oversized roman numeral on every section. `DESIGN.md` already forbade both, after two pages were stripped for it earlier in July 2026. Resolved in favour of DESIGN.md: the older rule was learned from shipped work, and the pattern is also the most saturated AI landing-page tell of 2026, so it actively worked against the premium read it was meant to produce. **When a new system contradicts a rule the vault learned the hard way, the learned rule wins until Hunter says otherwise.**

**Never gate content visibility on JavaScript.** The first reveal implementation hid every below-fold section until an IntersectionObserver fired. A deep link to `#close`, which the page's own hero CTA points at, could land on a blank section. Reveals must enhance an already-visible default, with a failsafe that clears them regardless. See [[hidden-pane-scroll-reveal]] for the related lesson about not misreading such a pane as broken.

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

## Open

- **No form endpoint.** `FORM_ENDPOINT` is `null`; submit opens a `mailto:` compose. One line at deploy.
- **Founders portrait.** Current frame is a studio-seamless team shot, greyscaled and cropped as a holding treatment. Wants a real environmental portrait, which is a shoot.
- **Plate grading.** Night aerial next to bright daylight frames. A true one-grade pass needs graded exports, not CSS. See [[color-grading]].
- **⚠️ `/contact-us/` still carries a seven-field form with a required free-text message**, the exact friction 10x bills clients to remove. See [[lead-gen-engine]].
- **Not deployed.** Decision still open on whether this replaces the WordPress site or is handed to the web team to port. As of 31 Jul, a partial release (6 of 6 non-case-study pages) is committed and build-verified but has nowhere to go live — no hosting pipeline is configured, and Hunter has chosen local-only for now.
- **Homepage work-grid tiles point nowhere.** `/sol`, `/davenport`, `/bespoke`, `/elysium`, `/broncos-leagues-club` have no backing page. Fine under normal JS operation (the lightbox intercepts the click); a dead end for no-JS or crawlers.

## Corrections to the vault

The claim that `10xvisuals.com.au` has **no lead form** ([[lead-gen-engine]], verified 27 Jul 2026) was **wrong as of 30 Jul 2026**: a form exists at `/contact-us/`. The real problem was never absence, it was friction.

---
_Vault: [[overview]] · [[brand-system]] · [[lead-gen-engine]] · [[hunter]]_
