# Trivelle — full launch to-do

Updated 2026-11-04. Product: **Trivelle 4-in-1 Sculpt & Glow** (heat, red light, EMS, vacuum) + 80 g microcurrent gel. **A$219** kit · **A$389** 2-pack. Supplier ships direct to AU, 7–15 days, landed cost ~A$45. Stock supplier box for now.

Shopify admin works on your phone too. Do the sections in order.

## 1. Product page — ~30 min
- [ ] Products → Trivelle → Media: delete every old image (old 3-in-1 white oval photos).
- [ ] Upload in this order (all in `device-v2/`):
  1. `graphics/01-kit-hero.jpg`
  2. `graphics/02-four-rituals.jpg`
  3. `stills/s1-stomach.png`
  4. `graphics/03-how-to-use.jpg`
  5. `graphics/04-gel.jpg`
  6. `graphics/05-where-to-use.jpg`
  7. `stills/04-hand-screen.png`
  8. `graphics/06-comparison.jpg`
  9. `graphics/07-in-the-box.jpg`
  10. `graphics/08-guarantee.jpg`
- [ ] Title: **Trivelle 4-in-1 Sculpt & Glow**
- [ ] Description: Warm (gentle heat, relaxing massage feel), Glow (red light, radiant-looking finish), Lift (EMS micro-pulses, toning, firming feel), Smooth (vacuum massage, smooths the look of skin). Remove every "3-in-1" mention.
- [ ] In the box: 4-in-1 device, microcurrent gel 80 g, USB charging cable, English user manual. Delete any "face + body heads" line.
- [ ] Usage everywhere: "10 minutes, 3–5 times a week".

## 2. Pricing — ~10 min
- [ ] Kit **$219**, Gift 2-Pack **$389** ("Save $49 vs buying two"). Delete the old $149 variant if it's still there.
- [ ] Each variant: clear Compare-at price.
- [ ] Theme editor: delete the countdown, "Launch offer · save $110" banner, "Save 39% OFF" badge.
- [ ] Price line: "$219 — about a dollar a session". Never "under $1".

## 3. Shipping + legal — ~20 min
- [ ] Banner + FAQ: "Free worldwide shipping" → **"Free shipping Australia-wide"**.
- [ ] Settings → Markets: Australia only.
- [ ] Product page, FAQ, shipping policy: **"Ships within 1–4 business days, then 7–15 business days delivery, tracked."**
- [ ] Settings → Policies: replace "My Store" with business name; add ABN, address, email to Terms + footer.
- [ ] Product FAQ: add "Who shouldn't use Trivelle" (pregnancy, pacemaker/implants, epilepsy, broken or irritated skin).
- [ ] FAQ: "no marks" → "start on the lowest level to avoid marks".
- [ ] Collection: turn off the price filter (`${{amount}}` bug).

## 4. Checkout — ~10 min
- [ ] Settings → Payments: turn on **Afterpay** (or Shop Pay Installments).
- [ ] Test order with a real card → check confirmation email → refund.

## 5. Tracking — ~20 min
- [ ] Install **Facebook & Instagram** app → connect pixel, data sharing "Maximum".
- [ ] Install **TikTok** app → connect pixel.
- [ ] Another test order → confirm a **Purchase** event in Meta Events Manager → refund.

## 6. Meta ads — ~30 min
- [ ] Meta Business: verify trivellebeauty.com, add a payment method.
- [ ] Campaign: **Sales**, Advantage+ audience, Australia, women 35–65.
- [ ] Budget **$20/day for 5 days (~$100 test)**.
- [ ] One ad set, ads from `device-v2/ads/`: D-seated-explainer-30s, A-salon-30s, B-lived-a-little-30s, A-hook-10s (optional long: A-salon ~60 s).
- [ ] Never use `videos/ads/` (old 3-in-1 device).
- [ ] Tick **"AI-generated / altered"** on every ad.
- [ ] Copy — Primary: "Made for skin that's lived a little. Heat, red light, EMS and vacuum massage in one cordless device, for brighter, smoother, firmer-looking skin in about 10 minutes. 30-day money-back guarantee." · Headline: "Four rituals. One device." · Description: "$219 · 30-day money-back guarantee" · CTA: Shop now.

## 7. TikTok (optional)
- [ ] Same 30 s cuts, same AI label.

## 8. Running the test — days 1–5
- [ ] Don't touch anything for 3 days.
- [ ] Day 3+: turn off any ad with ~$40 spent and no add-to-carts.
- [ ] Judge cost per add-to-cart first, then purchases.
- [ ] Day 5: sales → raise budget ~20% every few days. None → new hook/offer before spending more.

## 9. Orders
- [ ] Pass each order to the supplier (or auto-fulfil); add tracking in Shopify.
- [ ] Reply to emails within one business day.

## 10. Once sales are steady
- [ ] Judge.me reviews (real only).
- [ ] hello@trivellebeauty.com email.
- [ ] Meta descriptions for home / product / about.
- [ ] Custom box: ~A$900–1,000 for 500 incl. inserts + sample; ask supplier to quote + pack. Redesign first (draft in `packaging/` too plain — gel-wave pattern, lighter stock, emboss/foil). Needs ~170 × 115 × 180 mm inside; confirm device size.
- [ ] Re-roll ad presenters so they say "Trivelle" properly.

## Known issues
- AI presenters say "Trevolz" / "Trivel"; captions are correct. Fine for testing.
- Kit hero shows a green TRIVELLE box as background styling; customers get the plain supplier box (in-the-box image matches).
- Today's Magnific images still in the library — say "trash them", then empty the trash yourself.
