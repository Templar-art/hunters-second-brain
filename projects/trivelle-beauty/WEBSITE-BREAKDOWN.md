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
| 5 | **"Was" prices ($279 / $249 / $558, "Save 39%")** and "Launch price ends… Regular price from 1 December" | ACCC treats a was-price you never actually charged as misleading. A countdown that resets is the same problem. | Only keep the strikethrough if you will genuinely charge $279 from 1 December and keep it there. Otherwise remove the compare-at prices and timer. |
| 6 | **No safety / contraindication info** | EMS and suction devices must warn off pregnancy, pacemakers or implanted electronics, epilepsy, broken skin, recent surgery, etc. Missing warnings = liability and chargebacks. | Add a "Who shouldn't use Trivelle" FAQ + a line in the description. Get the list from the supplier's manual. |

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
