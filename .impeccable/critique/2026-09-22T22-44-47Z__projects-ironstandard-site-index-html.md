---
target: Iron Standard site (projects/ironstandard-site/index.html)
total_score: 22
p0_count: 1
p1_count: 3
timestamp: 2026-09-22T22-44-47Z
slug: projects-ironstandard-site-index-html
closed: true
---
# Design Critique: Iron Standard site

Target: projects/ironstandard-site/index.html (six-page site). Reviewed at 1440 and 375.

## Design Health Score: 22/40 (Acceptable)

| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of system status | 2 | No per-field form state, no required markers, no aria-invalid |
| 2 | Match system / real world | 3 | Section ordinals and "Elsewhere" are the site's abstractions |
| 3 | User control and freedom | 2 | Header CTA on contact.html reloads and wipes typed input |
| 4 | Consistency and standards | 2 | sec--ruled on 1 of 8 sections; logo href differs on index |
| 5 | Error prevention | 1 | Zero validation runs: it sits behind the live-endpoint check |
| 6 | Recognition over recall | 3 | 7-option select, "Detail" label carries no information |
| 7 | Flexibility and efficiency | 2 | One path only; no email, phone or mailto in ten pages |
| 8 | Aesthetic and minimalist | 3 | Unshaped voids at 1440; founder photo breaks palette |
| 9 | Error recovery | 1 | Error styled as help text, below the button, role=status |
| 10 | Help and documentation | 3 | FAQ not linked from the form |

The visual and content layers score well. The transactional layer drags the whole thing down;
almost every lost point is on the contact page.

## Anti-patterns verdict

Not slop, but not yet authored: a well-executed instance of a known genre.
Fails the first-altitude category-reflex test comprehensively (theme and palette are guessable
from "premium gym" alone). Passes partly at the second altitude, on the strength of the
confirmed/planned table and the ruled index rows.

Three machine-made tells:
1. "X rather than Y" appears 20 times across six pages, plus the same idea in antithesis form
   throughout. One sentence shape, defended repeatedly.
2. Alt text written from imagination: founder.jpg is captioned "Portrait of an athlete on the
   training floor"; the photo is a man outdoors against a blue glass office tower.
3. All six pages run an identical section rhythm. A strong template applied six times, which is
   precisely the client's complaint.

Deterministic scan: 38 findings (13 design-system-color, 11 design-system-font, 10 single-font,
4 numbered-section-markers). Font and colour findings are false positives: TASA Orbiter and the
Iron Standard palette are client-mandated, and 10x's Not-Ours-To-Set rule exempts client palettes.
In-page overlay scan: 8 anti-patterns (oversized-h1, hero-eyebrow-chip, tight-leading x2,
all-caps-body x3, wide-tracking x2, single-font, repeated-section-kickers x3). Tight-leading on
display statements is a false positive; the 57-char all-caps figcaption is a real hit.

## Priority issues

P0 The primary action does not work and there is no alternative. data-endpoint is still
   PASTE_WEB_APP_URL_HERE. No email, phone, mailto or social anywhere in ten files. The site
   converts at zero and the failure is only discovered after the visitor has typed their details.

P1 #extraField is visible when it should be hidden. Confirmed live: hidden=true, display=grid,
   height 79px. .field{display:grid} overrides the UA [hidden] rule. Membership is the default
   select value, so most visitors see a mystery field labelled "Detail".
   Fix: .field[hidden]{ display:none; }

P1 Zero validation currently runs. The validation block sits inside the live-endpoint branch.
   Confirmed live: an empty form submits and returns the launch-timing message.

P1 The founder moment destroys the credibility it exists to create: stock photo, only saturated
   blue on the site, visible "PLACEHOLDER IMAGE" caption, founder never named.

P2 Orange does three contradictory jobs. #routingNote and #formStatus are pixel-identical
   (1px rgba(244,80,42,.38) / rgba(244,80,42,.09)). The form's first feedback on load reads as
   an error. Split them; reserve the orange treatment for errors; move status above the button.

## Persona red flags

Jordan: 7-option select with no "just want to know more"; default Membership triggers an
orange box that reads as an error; 800 m2 never translated.
Riley: empty form submits; PASTE_WEB_APP_URL_HERE in source; og:image is a relative path so
every social share renders imageless; logo href="/" on index breaks on subdirectory deploys.
Casey: header CTA is display:none below 1024px, so mobile has no persistent enquiry route after
the hero; disclosure that the form does not send appears after the submit button.
Serious female lifter, Oslo: hero wins her in three seconds. The word "women" appears once on
the whole site, in a collapsed accordion on page five. Culture copy is two defensive negations.
24/7 unstaffed access raises a safety question nothing on the site addresses.

## Minor observations

ELEIKO legible on four plates in the hero, against the brief's no-named-brands rule.
.stat dt renders "Competition grade" in sentence case inside an all-uppercase system.
--ink-faint is a dead token. Font weight 800 requested and never used.
The close section's CTA pair repeats the hero's verbatim.

## Questions to consider

1. What is the one fact here that no other gym in Oslo could publish?
2. Why is the founder anonymous? A name creates no liability.
3. The client said "template". Would a copy pass do more than another design pass?
4. The confirmed/planned table is the most original idea here. Why is it on page three?

## Accepted by decision, not defects

Numbered section markers and per-section eyebrows are required by the approved strategy and the
client's print guidelines. Owner decision 22 Sep 2026: keep. Their current size and contrast
making them the primary read is a separate, fixable issue.
All imagery is low-resolution placeholder pending the facility shoot.
