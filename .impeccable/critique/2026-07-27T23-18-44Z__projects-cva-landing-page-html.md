---
target: the three lead-gen landing pages
total_score: 19
max_score: 32
na_heuristics: 7,10
p0_count: 2
p1_count: 3
timestamp: 2026-07-27T23-18-44Z
slug: projects-cva-landing-page-html
---
⚠️ DEGRADED: single-context (sub-agent tool present but session policy forbids spawning agents unless the user asks)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 1 | Submitting the form produces no visible change of any kind: no loading, no confirmation, no error |
| 2 | Match System / Real World | 4 | Copy is genuinely in-domain ("Cold shower this morning?", Suburb not Postcode, "Prefer we call you?") |
| 3 | User Control and Freedom | 3 | Anchors work both ways, no modals, no traps, phone always reachable |
| 4 | Consistency and Standards | 3 | Strong within each page; MVX's radius scale drifts from the new DESIGN.md (8px vs 6px) |
| 5 | Error Prevention | 1 | `novalidate` with no JS actively removes the browser's own guardrail; `required` is decorative |
| 6 | Recognition Rather Than Recall | 4 | Every field labelled, job type as explicit options, no icon-only anything |
| 7 | Flexibility and Efficiency | n/a | Persuade surface: no repeat-use or power-user path exists to evaluate |
| 8 | Aesthetic and Minimalist Design | 3 | Focused; MVX's 2x2 service tiles and 10x's 4 objection cards are the weakest structures |
| 9 | Error Recovery | 0 | There is no error path at all, so nothing to recover with |
| 10 | Help and Documentation | n/a | Not applicable to a single-purpose ad landing page; the FAQ covers its role |
| **Total** | | **19/32** | **Acceptable (59%)** |

## Design Specificity Verdict

**LLM assessment**: These are authored, not category-interchangeable, and MVX is the strongest of the three. "Cold shower this morning?" as a hero lede, a licence strip placed one second below the fold, "we ARE the electricians so it's one crew, one visit, one bill" as the differentiator, and a repair-or-replace FAQ answer that admits a $200 fix exists: none of that could be lifted onto another trade's page unchanged. CVA is close to the editorial-monochrome lane, but it is CVA's *own* site identity read off their live pages, so identity preservation outranks the lane warning. 10x's page is the most generic of the three; its structure (hero, gap, offer card, work grid, steps, objections, form) would fit any service business, and the only thing making it 10x is the photography.

The deeper specificity problem is not visual, it is functional. All three pages are beautifully dressed **shells**. The single most important element on each, the form, does nothing. That is the gap a technical audit missed and a UX review cannot.

**Deterministic scan**: `detect.mjs` across all three files returns exactly one finding, `overused-font` (Montserrat, 10x page line 41). Declared a false positive: Montserrat is 10x's locked brand face per DESIGN.md, and identity preservation outranks the reflex-reject list. No other slop family detected, which is consistent with the eyebrow scaffold and side-stripe having been stripped earlier today.

**Visual overlays**: not attempted. Targets are `file://` documents rendered as static snapshots in this pane; no live-server or injection overlay was run, so no user-visible overlay exists. Fallback signal used: direct DOM measurement via the browser's evaluate surface (viewport 375 and 800, computed geometry, form submit simulation).

## Overall Impression

They look like work worth paying for, and they cannot currently capture a lead. The writing is the best thing here by a distance: it is specific, unhedged, and it answers real objections instead of listing features. The design is disciplined, fast, and mercifully free of the usual scaffolding. But every page ends at a form with `action="#"`, `novalidate`, zero JavaScript and zero live regions, which means a visitor who fills it in and presses the button gets silence, and Matt gets nothing. Two of the three also carry a literal `$[CONFIRM]` placeholder in visible body copy.

The single biggest opportunity: design the twenty seconds *after* the button press. Right now the emotional journey peaks at "yes, I'll do that" and then falls off a cliff.

## What's Working

1. **The copy earns trust by conceding things.** "No upselling a new tank onto a $200 fix" and "if the tank itself is leaking, replacement is the only real option" both cost the seller something, which is exactly why they land. Same with CVA's "if you're after the cheapest set of plans that will pass council, we're honestly not the right practice."
2. **Objection handling is placed where the doubt actually occurs**, not dumped in a FAQ afterthought. MVX answers "is this expensive?" immediately after the emergency CTA; 10x answers "72 hours seems unlikely" in the voice of the sceptic.
3. **The restraint is real and measurable.** No JavaScript, no motion for decoration, no eyebrows, one accent colour, 44px targets, contrast measured rather than guessed. These pages will load and behave correctly on a bad connection in a driveway, which is where they will actually be read.

## Priority Issues

**[P0] The form is a non-functional shell on all three pages**
- **Why it matters**: This is the conversion. `action="#"`, `novalidate`, no JS handler, no `aria-live`, no `role="alert"`, no success state. A visitor can submit an empty form and receive no error; a visitor can submit a complete form and receive no confirmation, and the data goes nowhere. `novalidate` without JS is worse than doing nothing, because it switches off the browser's own validation and replaces it with silence. Verified by simulating submit in the page: `submitFired: true, visibleFeedbackAfterSubmit: 0`.
- **Fix**: Either wire each form to its real backend (Formidable for MVX, whatever CVA and 10x use) with a visible success state and inline field errors, or drop `novalidate` so native validation works in the interim. Add one `aria-live="polite"` region per form. Design the success state as a real state, not a redirect to a blank thank-you page: confirm what happens next and when ("we'll call you back on this number today").
- **Suggested command**: `$impeccable harden`

**[P0] Visible placeholder money in body copy**
- **Why it matters**: CVA renders `$[CAMERON TO CONFIRM]` inside the qualifying paragraph and 10x renders `$[CONFIRM]` in the offer card. Both sit in the exact sentence that is supposed to filter or convert. If either page goes live unchanged, the page reads as unfinished at the moment of highest scrutiny.
- **Fix**: Get the two numbers, or restructure both sentences so they qualify without a figure ("project minimums apply, we'll cover them in the chat"). Do not ship the bracket.
- **Suggested command**: `$impeccable clarify`

**[P1] MVX never answers the question every emergency visitor has**
- **Why it matters**: The page says "upfront price" or "fixed price" four times and anchors no number anywhere. The only figure on the page is the ~$998 rebate, which applies to the *upgrade* path, not the repair path. On emergency-intent traffic the first question is "what is this going to cost me", and a page that repeats "upfront price" without ever showing a range reads as evasive, which is the opposite of the intended effect.
- **Fix**: Add a price *shape*, not a price: a from-figure for a standard element replacement, or a band for a heat pump changeover after rebate. The comparison table is the natural home and already has an empty column's worth of room. Confirm the figures with Matt first, which is a blocker you already have open.
- **Suggested command**: `$impeccable clarify`

**[P1] 10x makes a commercial guarantee nobody has approved**
- **Why it matters**: "If we ever do, you don't pay for that film" is a refund promise, and "72 hours" is stated five times across the page plus the ad copy. Neither has been signed off, and the page is the artefact that makes them binding in a prospect's mind. A missed turnaround with a written refund promise is worse than never having offered it.
- **Fix**: Get explicit sign-off on both, or soften to a commitment you can always keep ("if we're going to be late, you'll know before the deadline, not after"). This is a business decision, not a copy tweak.
- **Suggested command**: `$impeccable clarify`

**[P1] No page has a next-step state after the primary action**
- **Why it matters**: Peak-end rule. The visitor's last experience of the brand is the moment right after they commit, and on all three pages that moment is currently nothing. This is also where the highest-anxiety questions live: did it send, when will they call, what if I got the number wrong.
- **Fix**: One success block per page, in place, that names the next step and the timeframe, and keeps the phone number visible for anyone who would rather not wait.
- **Suggested command**: `$impeccable onboard`

**[P2] Identical card grids are the weakest structures on two pages**
- **Why it matters**: MVX's four service tiles (icon, heading, paragraph, CTA, repeated) and 10x's four objection cards are the one place these pages fall back on the default answer. They are not fatal, but they are the sections a reader skims.
- **Fix**: MVX's four services are not peers: "no hot water" is an emergency and "heat pump upgrade" is a considered purchase. Splitting them by urgency rather than gridding them as equals would carry information the current layout throws away.
- **Suggested command**: `$impeccable layout`

## Persona Red Flags

**Casey (Distracted Mobile User)** — the primary persona for all three. MVX passes well: the call bar is fixed under the thumb, buttons go full width, targets clear 44px, the table scrolls in its own container. But **nothing is preserved**: Casey fills three of four fields, gets interrupted by an actual phone call, comes back and the form is empty with no indication it was ever touched. And on CVA and 10x there is no sticky action at all, so the only CTA is wherever Casey happens to have scrolled to.

**Jordan (Confused First-Timer)** — mostly well served: every field is labelled, job types are spelled out as options rather than jargon, and the three-step sections tell Jordan what happens after the call. Two failures. First, Jordan submits the form and cannot tell whether it worked, which for this persona means submitting again, then giving up. Second, on CVA, Jordan reads "our work typically suits builds from around $[CAMERON TO CONFIRM]" and concludes the practice is careless.

**Riley (Deliberate Stress Tester)** — finds the sharpest edges. Submits the form empty: no error, no complaint, nothing. Types letters into the phone field: accepted. Submits twice: no way to tell whether one or two enquiries exist. Refreshes mid-fill: everything gone. Riley's verdict is the honest one: the form appears to work and silently fails, which is the specific failure mode this persona exists to catch.

## Minor Observations

- MVX's radius scale (`4/8/12px`) now disagrees with the DESIGN.md written an hour ago (`4/6/10px`). The doc was written from the 10x page; MVX predates it. Pick one and note the client-identity exception if MVX keeps 8px.
- `.mvx-form-or` and the CVA/10x footers now use `min-height:44px` on inline links inside paragraphs, which technically satisfies the target rule but makes the line-height of those paragraphs uneven. Worth checking visually against a real sentence.
- CVA's `The-Shed-1-768x1365.jpg` is portrait inside a 4/3 figure, so `object-fit: cover` crops it hard. It reads fine, but a landscape frame of the same project would read better.
- MVX's hero image is still the shared aircon frame (a technician servicing a wall unit), on a page about hot water. Nobody will notice consciously; it still isn't the right photo.
- All three pages carry `<meta name="robots" content="noindex, nofollow">`, which is correct for paid landing pages and worth keeping deliberate rather than accidental.

## Questions to Consider

- What if the form were the hero on the MVX page rather than the last section? Emergency intent may not need eleven scroll depths of persuasion before it is allowed to convert.
- MVX's four services are not peers. What would the page look like if it were split by urgency (broken now / planning an upgrade) instead of by service type?
- 10x's page argues that the product is visual and then leads with words. What would it look like if the first thing above the fold were a muted autoplaying listing film instead of a headline?
- CVA deliberately repels price shoppers. Is the qualifying paragraph doing that job better buried mid-page, or would it work harder immediately under the hero, where it also filters who bothers to keep reading?
