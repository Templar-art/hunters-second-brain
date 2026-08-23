---
target: "https://oneill.group.10xvisuals.co/"
total_score: 20
p0_count: 2
p1_count: 3
timestamp: 2026-08-23T00-41-33Z
slug: oneill-group-10xvisuals-co
---
## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 1 | The property search is inert (the source comment says "Nothing here is wired up yet"). No submit feedback, no result state, no form success/error. |
| 2 | Match System / Real World | 3 | "Buy It / Sell It / Lease It" is strong plain language. The listing statuses are not: "Own It" and "Preparing It" are house voice where buyers scan for "For Sale" and "Under Offer". |
| 3 | User Control and Freedom | 2 | The 5,400px pinned scroll wall hijacks scroll speed and cannot be skipped. The testimonial marquee cannot be paused. No back-to-top. |
| 4 | Consistency and Standards | 2 | Kicker rules bleed off-viewport on interior heroes but are inset on the homepage. Two contact identities. One header colour for two ground types. Numbered markers on some non-sequences. |
| 5 | Error Prevention | 1 | Required free-text message, required markers at 1.6:1, nine cards that look clickable and aren't, a footer link to a 404. |
| 6 | Recognition Rather Than Recall | 3 | Nav is short and persistent with an active state. Filter state vanishes after search; no position indicator inside the long scroll. |
| 7 | Flexibility and Efficiency | 2 | Six nav items and zero calls to action in the header. No phone number above the footer on a business that runs on phone calls. |
| 8 | Aesthetic and Minimalist Design | 3 | The real strength. Docked for a 13,000px homepage and a headline used twice. |
| 9 | Error Recovery | 1 | `/news/` is a bare 404 reachable from every page. Form error states are unstyled plugin defaults. |
| 10 | Help and Documentation | 2 | The privacy policy is genuinely thorough. Nothing else explains fees, timelines, or what happens after you submit. |
| **Total** | | **20/40** | **Bottom of the normal band** |

## Anti-Patterns Verdict

**Does this look AI-generated? No.** That is a real compliment and it should be said first. The palette is committed and unusual (sage, cream, basalt, no white and no black). The photography is real and it carries the design. There is no gradient text, no glassmorphism, no hero-metric row, no rounded-icon-above-every-heading, no card grid doing work a layout should do. The copy has an actual voice: "A family name, not a call centre", "Put your name to it", "Your address is not a line on a board". Someone made decisions here.

Two house rules do get tripped:

- **A kicker above nearly every section.** ABOUT US, HOW WE WORK, INSIGHTS, GET IN TOUCH, LEGAL, WHAT WE LOOK FOR, CAREERS, OUR PEOPLE. One named kicker is voice; a kicker as section grammar is scaffolding.
- **01 / 02 / 03 on things that are not sequences.** Buy / Sell / Lease are parallel services. "Four things we look for" is a list. The numbering on "How we work" (listen, care, deliver) is legitimate and should stay; the others should go.

**Deterministic scan.** 97 findings across 9 pages, 5 rules.

- **71 x overused font.** Confirmed real. The body face is Inter, the most-used typeface on the web. Elementor is also still pulling Roboto and Roboto Slab. Space Grotesk appears only on `/services/`, which is the freight demo page.
- **18 x layout property animation.** Confirmed real, and it is the site's own CSS, not a plugin. `.op-bar` transitions `width`, and `#op-logo-wrap` transitions `width` and `height`. That is the header pill morphing on scroll, so it thrashes layout on a fixed element during the one interaction that happens constantly.
- **2 x numbered section markers.** Agrees with the finding above.
- **5 x broken image. False positive** as reported, but it surfaced something real: the detector matched the literal string `<img>` inside shipped HTML comments. 20 build notes are live in the production source, including "Three tiles, one photo, three crops", "Replace each .onpl-well with an `<img>`", and "Inert. Nothing here is wired up yet." Anyone who views source reads the to-do list.
- **1 x aphoristic cadence.** On `/services/` only, which is the freight page.

## Overall Impression

This is a good-looking site that has not yet been asked what it is for.

The craft is real. The interior page heroes are the best thing on it: "PUT YOUR NAME TO IT" over a dusk exterior with a three-column fact strip underneath is a confident, composed piece of design that most Gold Coast agencies could not produce. The restraint is genuine rather than timid.

But the homepage opens with 756px of dark video that says nothing, and the site never once asks for a phone call above the footer. An agency website has two jobs: convince a vendor to list, and let a buyer find stock. Right now the design is optimised for a third thing, which is being admired. The single biggest opportunity is not visual. It is deciding what the visitor is supposed to do and then letting the design carry them there.

## What's Working

**The interior page heroes.** Our People and Careers both open with a display headline, a supporting paragraph offset to the right, and a hairline-divided fact strip along the bottom, all sitting on a dusk photograph. The composition is asymmetric without being arbitrary, and the fact strip does real work: three short answers to the three questions a visitor actually has. This is the pattern the homepage should be borrowing from.

**The colour discipline.** Sage, cream and basalt, with no pure white and no pure black anywhere. Three grounds, used consistently, alternating for rhythm rather than decoration. It is a genuinely uncommon palette for the category, which is exactly why it reads as considered. The only failures are places where sage carries text it cannot support, which is a token-application problem, not a palette problem.

**The copy voice.** Plain, Australian, unsentimental, and free of agency cliche. "We're not a franchise, and we're not a boutique that only opens the door for the top end of the market" does more positioning work in one sentence than most agency about-pages manage in a page. The privacy policy is genuinely well-built too, with a working on-this-page index and real Queensland tenancy-database content.

## Priority Issues

### [P0] The first fold makes no argument

**Why it matters.** A prospect landing on the homepage sees a dark, abstract video, six nav items, and nothing else. No headline, no proposition, no search, no phone number, no call to action. The mission statement that would do this work sits below the fold, and on mobile the video crops to unreadable abstract shapes. Every other page on the site opens with a headline and a supporting paragraph; the homepage, which gets the most traffic, is the only one that opens with silence. Meanwhile the interior heroes prove the team can already do this well.

**Fix.** Bring the mission statement up onto the video with the same treatment the Careers hero uses: display headline, one supporting line, and a fact strip or a single primary action along the bottom. Keep the video as ground, not as content.

**Suggested command.** `/impeccable shape`

### [P0] There is no path to a phone call

**Why it matters.** This is an agency. The conversion is a conversation. The header carries six navigation items and zero calls to action, there is no phone number anywhere above the footer, and the footer number is a placeholder. The one real conversion point, the contact form, requires a free-text message before it will submit, which is the heaviest thing you can ask of someone on a phone. The CTA band on the homepage then offers five exits at once (Buy, Sell, Lease, Contact Us, Request a Property Quote) with no primary among them, so the one moment the page does ask for something, it asks for five things.

**Fix.** A persistent call action in the header with the real number. One primary action per section, visually dominant. Make the message field optional on the form.

**Suggested command.** `/impeccable shape`

### [P1] The scroll wall spends the page's whole budget on four sentences

**Why it matters.** "How we work" is 5,400px on desktop, six full viewports, to deliver four short statements. It sits between the About block and the testimonials, so anyone heading for the contact CTA has to scroll through all of it, and the scroll speed is hijacked while they do. It is also the section where the art direction fails: "WE LISTEN" works because the type sits on the dark left third of its frame, but "WE CARE" puts cream type on a white kitchen and is effectively unreadable, and the same happens on the closing two frames. There is no rule governing where the type sits relative to the photo's brightness, so each frame works or fails by luck.

**Fix.** Cut the dwell so the whole wall lands in three viewports or fewer. Add a brightness-adaptive scrim behind the type block, sized to the text and tuned per frame, so it is not luck.

**Suggested command.** `/impeccable distill`

### [P1] The three commercial pages are the emptiest on the site

**Why it matters.** Buy It, Sell It and Lease It are structurally identical: one headline, the shared listings grid, the shared CTA. Nothing between them. Sell It is the highest-value page on the site, because a vendor choosing an agency is the decision that pays for everything, and it currently contains one sentence of unique content. The grid is not even filtered per page, so Lease It shows Sold listings. A vendor comparing three agencies has nothing here to compare.

**Fix.** Each page needs at least one section only it could carry. For Sell It, that is the campaign process, what the fee covers, and proof. Filter the grid per page.

**Suggested command.** `/impeccable shape`

### [P1] Two type voices, and only one of them has character

**Why it matters.** The display face carries the whole brand: it is on every headline, and it is the reason the site looks expensive. The body face is Inter, which is the single most common typeface on the web, so all the personality lives in the headings and none of it survives into the paragraphs. The display face is also Sinhala MN, an Apple system font repurposed with metric overrides, shipped as a 322KB unsubset WOFF. The identity currently rests on a font that was never licensed for this and costs a third of a megabyte.

**Fix.** Replace the display face with a licensed serif of the same voice, subsetted. Replace Inter with a body face chosen against the display face on a real contrast axis rather than defaulted to.

**Suggested command.** `/impeccable typeset`

## Persona Red Flags

**Jordan (first-timer, arrived from a For Sale board).** Lands on the homepage, sees a dark video and no message, and has no idea whether this agency covers their suburb or their price bracket. Scrolls to the listings grid and finds nine cards reading "00 Placeholder Street". Tries the search; it does nothing, because it is inert. Sees status badges saying "Own It" and "Preparing It" and cannot tell which of those means "available". Gives up before the About section.

**The Vendor (homeowner, interviewing three agencies, the decision that matters).** Goes straight to Sell It, because that is the page for them. Finds one headline, a grid of placeholder listings, and a contact form. No process, no fee structure, no recent sales, no named agent. Goes to Our People to see who they would actually be dealing with and finds six cards showing the same stock photograph of the same man, named PLACEHOLDER ONE through SIX, all sharing one phone number. This is the page that was supposed to prove there are real people behind the family name, and it currently proves the opposite.

**The Buyer (on a phone, thumb-first, on the couch).** The hero video crops to abstract dark rings and reads as nothing. The header shows three inline links about 40x20px each plus a hamburger, two navigation systems competing in a 44px strip. Scrolls and the white nav pill sits on top of whatever they were reading: the mission statement, the card badges, the section headings. Reaches the testimonials and the quotes are sliced mid-word at both edges. Wants to call; there is no number until the footer, and it is 07 0000 0000.

## Minor Observations

- 20 HTML build comments ship in the production source, including "Inert. Nothing here is wired up yet."
- "PROPERTY IS PERSONAL" is used twice on the homepage, as the About H2 and as the scroll wall's closing statement. The wall placement is the stronger one.
- The kicker hairline bleeds off the left edge of the viewport on the interior page heroes but is inset to the container gutter on the homepage. Pick one.
- The ON monogram tile at the top of the "Every move starts somewhere" band straddles the section boundary, which reads as mispositioned rather than deliberate.
- A small empty rectangle sits beside the scroll wall's progress dashes with no visible content.
- The Careers page leaves a large empty column beside the "Four things" heading.
- Bracketed contact details, `[ 07 0000 0000 ]`, read as unfilled template slots rather than as a device, especially while the values inside them are placeholders.
- The listing status vocabulary ("Own It", "Preparing It", "Sold It", "Lease It") extends the Buy It / Sell It / Lease It naming to a place it does not work. Nav labels can be voice; status badges need to be scannable.

## Questions to Consider

- If a vendor could only see one page before choosing an agency, which page would you want it to be, and does that page currently earn the choice?
- The interior heroes are better than the homepage hero. What stops the homepage from using the same pattern?
- The scroll wall is the most expensive thing on the site in attention. If it were cut to three frames, which one goes, and does anyone notice?
- What is the site's single most important action, and where is it on the screen right now?
- The restraint is real. Is the silence on the first fold restraint, or is it an unmade decision wearing restraint's clothes?
