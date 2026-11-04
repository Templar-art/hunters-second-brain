# trivellebeauty.com — Website Breakdown

Audited 2026-11-04 from the live public site (no admin access). Shopify, Horizon theme, store location Upper Coomera QLD, 1 product, 1 collection, AUD.

## Hosting (the "second laptop" question)

The store runs on **Shopify's servers**, not your laptop. Turning the home laptop off, or it losing internet, does **not** take the site down. The laptop only matters as the place you log into the Shopify admin from — and you can do that from any device, including your phone (Shopify app). Pages load in about 0.5 s, which is fast.

## What's good

- Clear offer: three kits ($149 / $169 / $299), gel bundle positioned as "everything you need", gift pack for Christmas.
- Copy is mostly careful: "radiant-looking", "firmer-looking", "toning massage feel" — cosmetic wording, not medical claims.
- Refund policy is solid and correctly references the Australian Consumer Law.
- Shipping policy is detailed (processing, delivery windows, customs, lost parcels).
- Contact page promises a one-business-day reply. About page is short and human.
- FAQ on the product page answers the real questions (how it works, how it feels, where to use it, what's in the box, gel ingredients).

## Fix first (blocking sales or creating risk)

| # | Issue | Why it matters | Fix |
|---|---|---|---|
| 1 | **Zero product images** on every page | Nobody buys a $169 device they can't see. Ads to this page will burn money. | Upload the new set from `stills/` and `graphics/` (order below). |
| 2 | **No tracking pixels detected** (no Meta, TikTok or Google tags in the page) | You can't run or optimise ads without a pixel. Note: Shopify can load pixels through *Customer events* in a way this check can't see — verify in admin. | Settings → Customer events: connect Meta (Facebook & Instagram app) and TikTok. |
| 3 | **Shipping mismatch**: banner and policy say "Free worldwide shipping", but the store is set to ship to **Australia only**, while the currency selector lists ~45 countries | Overseas customers can browse, add to cart, then fail at checkout. | Either add shipping zones for the countries you'll serve, or change the banner to "Free shipping Australia-wide" and turn off the extra markets. |
| 4 | **Policies say "My Store"** (Privacy + Terms are unedited Shopify templates) | Looks like a scam store, and the legal entity on your terms is undefined. | Replace "My Store" with your business name; add ABN, business address and contact email to Terms and the footer. |
| 5 | **"Was" prices ($279 / $249 / $558, "Save 39%")** with a launch countdown to a fixed date (1 Dec 2026, it does not reset) | The timer itself is honest. The risk is the strikethrough: under the ACCC's reference-pricing rules a "was" price must be one you genuinely charged (or will charge) for a reasonable period. **Do not raise it to $550 to match Sculpiflex** — that number would be invented, and it's the most common way small stores get ACCC letters and Meta ad rejections. | Pick one: (a) keep "Launch price — rises to $279 on 1 December" and actually charge $279 from then; (b) drop the strikethrough and sell on value ("$169 — about the cost of one salon session"). See *Pricing options* below. |
| 6 | **Safety info is only on the FAQ page** (pregnancy, pacemaker, epilepsy, broken skin are covered there — good) | Buyers read the product page, not the FAQ. | Add the same "Who shouldn't use Trivelle" answer to the product page FAQ. |

## Fix next (conversion)

| # | Issue | Fix |
|---|---|---|
| 7 | No reviews app | Install Judge.me (free tier). Add real reviews as they come in — **never** import fake or copied ones (ACCC + Shopify ban). |
| 8 | No Afterpay / Shop Pay Installments | AU beauty buyers expect Afterpay at $169. Add Afterpay or turn on Shop Pay Installments. |
| 9 | Meta descriptions missing on every page | Write one for home, product, about (shows in Google and link previews). |
| 10 | "No static cups and **no marks**" in the FAQ | Suction can leave temporary redness. Change to "start on the lowest level to avoid marks". |
| 11 | "Face head and body head" in the box | The supplier photos show one cup. Confirm with the supplier before promising two heads. |
| 12 | Collection page shows a raw `${{amount}}` in the price filter | Theme bug: turn off the price filter on the collection (only 1 product anyway). |
| 13 | "Real support, Australian-owned" + a store that looks overseas-shipped | Fine if true. Keep it, but make the contact email a real domain address (hello@trivellebeauty.com). |

| 14 | FAQ says "We ship worldwide" | Same mismatch as #3 — update with the banner. |
| 15 | Usage frequency is inconsistent: product page says "10 minutes a day", How to Use + FAQ say "3–5 times a week" | Pick one (the supplier manual decides) and use it everywhere. The how-to graphic now says 3–5x a week. |

## Pages checked

Home, product, collection, About, Contact, FAQ, How to Use, Track order, cart, all four policies, sitemap, robots. All load (200).

## Pricing options (instead of a made-up $550)

1. **Genuine launch price** (current setup, keep it honest): "$169 launch price · $279 from 1 December". Then really move to $279 on 1 Dec, and run sales *down* from that real price later.
2. **Value anchor, no strikethrough:** "$169 — less than two salon sessions" / "about 50c a day over a year". Legal, and it often converts as well.
3. **Bundle saving (always true):** "Gift 2-Pack $299 — save $39 vs buying two" (2 × $169 = $338). Real maths, no reference price needed.
4. **Raise the actual price.** If you want $550 positioning, sell at $550 for a real period first; you can then discount from it legitimately.

**Decision (2026-11-04): value anchor.** Copy changes below.

## Value-anchor copy changes

**Remove in Shopify admin**
- Product → each variant → *Compare-at price*: clear ($279, $249, $558).
- Theme editor → home + product: delete the countdown block ("Launch price ends in…", "Regular price from 1 December").
- Theme editor: delete "Launch offer · save $110" (home banner) and the "Save 39% OFF" badge.

**Replace with**
- Price line: **$169 AUD — about the cost of one salon treatment**
- Under the price: **Under $1 a session.** *(Based on 4 sessions a week for a year.)* — $169 ÷ 208 = 81c, true.
- Kit cards:
  - Device + Glide Gel — **$169** · *Everything you need*
  - Gift 2-Pack — **$299** · *Save $39 vs buying two*
  - Device only — **$149** · *Already have a conductive gel*
- Home hero eyebrow (where "Launch offer" was): **New · Free shipping Australia-wide** (once #3 is fixed)

Keep the 30-day money-back guarantee prominent; with no discount badge it does the urgency work.

## Product page image order (from what's been made)

1. `stills/01-hero-final.png` — hero
2. `graphics/01-feature-panel.jpg` — three rituals
3. `stills/02-stomach-older.png` — in use
4. `graphics/05-how-it-works.jpg` — through the skin
5. `stills/04-thigh-older.png` — in use
6. `graphics/02-how-to-use.jpg`
7. `stills/roster/` — 2–3 diverse models
8. `graphics/03-comparison.jpg`
9. `stills/05-macro.png` — roller close-up
10. `graphics/04-in-the-box.jpg`

## Before running ads — checklist

- [ ] Images uploaded (1)
- [ ] Meta + TikTok pixel connected and a test purchase seen (2)
- [ ] Shipping banner matches shipping zones (3)
- [ ] Policies show your business name + ABN (4)
- [ ] Was-prices genuine or removed (5)
- [ ] Safety FAQ added (6)
- [ ] Reviews app installed (7)
- [ ] Afterpay on (8)

## Brand kit (from Higgsfield, 2026-11-04)

Main #1D2A26 (deep green) · #FFFFFF · #000000 · #E1E8E5 (pale sage) · accent #8B0000 (deep red). Display **Anton**, body **Montserrat** (clean copies in `fonts/`; the system Montserrat files are corrupt). All graphics regenerated in this kit. Note the kit still says "free worldwide shipping" — it was scraped from the site, so it inherits issue #3.
