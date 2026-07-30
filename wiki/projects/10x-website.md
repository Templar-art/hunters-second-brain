---
type: project
tags: [10x-visuals, website, design-system, prestige, lead-gen]
status: homepage-rebuilt-not-deployed
updated: 2026-07-30
---

# 10x Website

10x Visuals' own front door, `10xvisuals.com.au`. A WordPress site with real content and real case studies whose finish did not match the work it sells. The homepage was rebuilt on 30 Jul 2026 as a static page against [[brand-system|Prestige DS v1.0]]; the other five pages are untouched.

**Build:** [projects/10x-site/](../../projects/10x-site/) · **Spec + outcome:** [design spec](../../docs/superpowers/specs/2026-07-30-10x-homepage-prestige-rebuild-design.md) · **System of record:** [DESIGN.md](../../DESIGN.md), Prestige layer

## What the site is

Six pages: home, `/branding`, `/content-creation`, `/lead-generation`, `/systems-processes`, `/contact-us`. Five real case studies ([[sol]] · Davenport · [[bespoke-estate-agents]] · Elysium · Broncos Leagues Club), sixteen named clients, one testimonial. Structure was sound. Skin, typography, rhythm and motion were not.

## What shipped

A single self-contained `index.html`: full-bleed **Stonehaven** dusk hero under the headline "Presentation decides the price.", a typeset client roster, six case-study plates alternating full-bleed and two-up, a parallax interlude, the four disciplines as hairline rows, founders, testimonial, and a three-field enquiry close. Works over `file://` and HTTP. Not deployed.

**Hero: Stonehaven**, 47 Somerset Drive, marketed by Whitefox, shot at dusk. It replaced the [[sol]] drone frame on 30 Jul. Work order is Stonehaven, Davenport + Bespoke, Elysium, then SOL + Broncos; SOL moved below Elysium at Hunter's request.

## What it taught us

**A handed-down design system can still be wrong, and measuring beats deferring.** Prestige DS v1.0 shipped four token values that fail WCAG AA on the surfaces they actually land on, including its own text blue at 4.39:1. Four amendments are now the real system, recorded under The AA-Amendment Rule. The lesson generalises: a token is only compliant on the surface it lands on, which is the [[brand-system|Surface-Not-Token Rule]] arriving for the third time.

**⚠️ Two of Hunter's systems contradicted each other.** Prestige DS v1.0 prescribes a tracked kicker and an oversized roman numeral on every section. `DESIGN.md` already forbade both, after two pages were stripped for it earlier in July 2026. Resolved in favour of DESIGN.md: the older rule was learned from shipped work, and the pattern is also the most saturated AI landing-page tell of 2026, so it actively worked against the premium read it was meant to produce. **When a new system contradicts a rule the vault learned the hard way, the learned rule wins until Hunter says otherwise.**

**Never gate content visibility on JavaScript.** The first reveal implementation hid every below-fold section until an IntersectionObserver fired. A deep link to `#close`, which the page's own hero CTA points at, could land on a blank section. Reveals must enhance an already-visible default, with a failsafe that clears them regardless. See [[hidden-pane-scroll-reveal]] for the related lesson about not misreading such a pane as broken.

**Mismatched logo files are worse than no logos.** Nine client logos across dark-on-white JPEGs, an inverse navy lockup and a yellow Ray White square cannot be unified by greyscale and multiply; they render as pale boxes of unequal weight. A typeset Prata roster looks more expensive and carries the ten clients that have no logo asset at all. Recorded as The Roster-Not-Logos Rule.

**A hero is chosen by where the dark is, not by how good the photo is.** The SOL drone frame is a strong photograph and still made a poor cover, because its lower third is a bright white roof and pale concrete, exactly where the headline sits. Stonehaven works because its foreground lawn and paving are dark, giving ivory type a real bed. Judge a candidate by the tonal map of the region the type occupies, not by the image as a whole, and judge it at full resolution: SOL was picked off a downscaled preview where that roof read as dark water.

**Watch for burnt-in marketing graphics in client deliverables.** The first White Fox files found were `Whitefox Mappins-0*.jpg`, all four carrying a map-pin graphic composited into the frame, which DESIGN.md bans outright. The usable set was the 47 Somerset Drive prints. Anything named for a marketing treatment rather than a shot is suspect.

## Open

- **No form endpoint.** `FORM_ENDPOINT` is `null`; submit opens a `mailto:` compose. One line at deploy.
- **Founders portrait.** Current frame is a studio-seamless team shot, greyscaled and cropped as a holding treatment. Wants a real environmental portrait, which is a shoot.
- **Plate grading.** Night aerial next to bright daylight frames. A true one-grade pass needs graded exports, not CSS. See [[color-grading]].
- **The other five pages** will visibly clash with the new homepage until they get the same treatment.
- **⚠️ `/contact-us/` still carries a seven-field form with a required free-text message**, the exact friction 10x bills clients to remove. See [[lead-gen-engine]].
- **Not deployed.** Decision still open on whether this replaces the WordPress homepage or is handed to the web team to port.

## Corrections to the vault

The claim that `10xvisuals.com.au` has **no lead form** ([[lead-gen-engine]], verified 27 Jul 2026) was **wrong as of 30 Jul 2026**: a form exists at `/contact-us/`. The real problem was never absence, it was friction.

---
_Vault: [[overview]] · [[brand-system]] · [[lead-gen-engine]] · [[hunter]]_
