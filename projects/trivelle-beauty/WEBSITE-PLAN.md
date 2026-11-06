# Trivelle website + offers plan (audit 2026-11-06)

Compared trivellebeauty.com (live) with sculpiflex.com. Goal: same conversion mechanics as Sculpiflex, without copying their fake parts or their assets.

## What the live Trivelle store shows today (needs fixing)
- Price still **A$199** (decided A$169 + gel subscription).
- **Gift 2-Pack A$369 "Best for gifting" still live** (decided to drop it).
- Hero and product page both say $199 and "about a dollar a session".
- Gel upsell is "Add a spare tube +A$34.95" (a one-off, not a subscription).
- Delivery estimate "Wed 18 Nov - Thu 3 Dec" shown under Add to cart (good, keep it honest).
- FAQ already has "Who shouldn't use Trivelle?" (good, keep it).
- 30-day money-back guarantee box under Add to cart (good).
- No email popup seen.

## What Sculpiflex does that is worth mirroring (structure, not content)
1. Announcement bar at the top with the offer + free shipping.
2. Hero with one offer + one button.
3. Bestseller row of 3 products (kit, gel, extras).
4. Social-proof block under the hero ("real results on camera").
5. Email popup: "Congratulations! You've unlocked a mystery discount" with an email box and a "Reveal my secret code" button.
6. Gel / consumables upsell ladder, subscription toggle under the price.
7. Free shipping + 30-day guarantee repeated in a trust bar.
8. Trustpilot badge.

## What we do NOT copy
- Their before/after photo cards ("real results") and the quotes under them. We have no real results yet; those are body before/afters and fake-looking testimonials, which breaks Meta + ACCC rules. Replace with the REAL tester trial (week 7-8) and plain product photos until then.
- Doctor/lab-coat models, "developed by plastic surgeons and dermatologists", "clinic-grade", "tighten loose skin / release stubborn fat / smooth cellulite".
- "Was A$533 / 70% off" struck-through prices.
- Their images, copy, videos, logo, product names: copyright, and they'd look like a clone. We keep Trivelle's brand (green #1D2A26, lime #C4CE26, Anton + Montserrat).

## Discount: how to do it honestly
- Set the kit at **A$169** and show just that. No compare-at price. A "was A$199" needs a genuine period of selling at A$199, and the store has only been live a couple of days.
- Offer discounts as a REAL code or a REAL bundle:
  - Email popup: 10% off first order (A$16.90 off), code e.g. TRIVELLE10, one use per customer.
  - Free shipping Australia-wide (already live).
  - Gel subscription: subscribers save a real % on gel refills.
  - Black Friday / Christmas: a code or automatic discount at checkout, with real dates. No countdown timer unless it genuinely ends.
- No "only 3 left" or fake scarcity.

## Popup spec (Shopify: Shopify Forms or Klaviyo)
- Trigger: 8 s delay or 40% scroll, once per visitor, not on cart or checkout.
- Headline: "10% off your first order." Subline: "Join the Trivelle list and get your code instantly."
- Fields: email only. Button: "Get my code". Fine print: "Unsubscribe any time."
- After submit: show the code + auto-apply at checkout (discount link).
- Follow-up email flow: welcome + code reminder in 24 h, abandoned-cart reminder in 1 h.
- Optional gamified "reveal" like theirs is fine IF every outcome is a real code. Keep it simple at first.

## Page changes (in order)
1. Set kit to **A$169**; delete the Gift 2-Pack variant; update hero + product page prices ("about a dollar a session" stays OK).
2. Turn the gel option into a **subscription** ("fresh gel every 30 days, cancel any time") with a real subscriber saving. Needs Shopify Subscriptions or Seal/Recharge.
3. Announcement bar: "Free shipping Australia-wide. 30-day money-back guarantee."
4. Add the **email popup** above.
5. Replace any "Real results" style block with a "How it feels" block (existing ritual section) until the real trial is done.
6. Add a "Meet the first testers" placeholder block that goes live with the real trial.
7. Trustpilot or Judge.me reviews app: only real reviews, request them after delivery.
8. Page speed + mobile check (most Meta traffic is mobile).
9. Add the "Is it a scam?" advertorial page (SCRIPTS-ROUND2.md section D).

## Approval needed before I touch Shopify
Hunter sets prices and logins himself. If you want me to make these edits through your logged-in Chrome, say go and I'll do them one at a time, screenshot each, and not publish anything that spends money. Steps 1-4 first.

## Status log (2026-11-06, done in Hunter's logged-in Shopify via Chrome)
- DONE: kit price set to A$169 (hero, product, CTA all show it).
- DONE: Gift 2-Pack variant hidden from every sales channel (not deleted; the delete is permanent so Hunter does that himself if wanted). Gone from the product page.
- DONE: TRIVELLE10 created (10% off order, one use per customer, active, no end date).
- DONE: Shopify Forms installed; "Welcome 10% popup" created (email + first name, shows TRIVELLE10 after submit), Forms theme embed switched on and saved, form turned on. Not yet seen on the live storefront at last check, so test in a fresh incognito window; Shopify titled it "10% off entire order".
- NOT DONE: gel subscription (needs Shopify Subscriptions app + the real refill saving), email flows (Shopify Email / Klaviyo; copy ready in COPY-PACK-ROUND2.md), advertorial page.

### Update later 2026-11-06
- DONE: advertorial page live at https://trivellebeauty.com/pages/is-trivelle-a-scam-the-honest-answer (visible, links to the product page).
- DONE: Shopify Messaging permissions approved. "Welcome new subscribers with a discount email" automation created and turned ON (subject "Your Trivelle code is inside", TRIVELLE10 attached). "Recover abandoned checkout" automation was already active.
- NOT DONE yet (templates exist in Messaging > Automations): recover abandoned cart, convert abandoned product browse, thank customers after purchase, review request, gel refill, win-back. Copy ready in COPY-PACK-ROUND2.md.
- NOT DONE: gel subscription (needs the real refill saving), popup not yet seen live (test in incognito).

### Website photos generated 2026-11-06 (Magnific, Nano Banana 2.1, 2K 3:2, 8 x 65 = 520 credits, approved by Hunter)
Files: device-v2/website-photos/ (JPG) and Drive "Trivelle/Website photos" (full-size PNG): 01 hero lifestyle, 02 face in-use, 03 arm in-use, 04 four-modes close-up, 05 flat lay gel+box, 06 comparison, 07 how-it-works, 08 gift / me-time. AI-generated: tick the AI label wherever they run in ads. Not yet uploaded to Shopify.
