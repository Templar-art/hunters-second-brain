---
type: project
tags: [shopify, ecommerce, activewear, swimwear]
status: setup
updated: 2026-10-06
---

# Bebita Collective (Shopify store)

**⚠️ Renamed 2026-09-30:** was Bebita Lifestyle. Hunter's call: "Collective" sounds more premium and lets the store sell beyond activewear and swim. The page filename keeps the old slug so existing links still resolve.

Activewear and swimwear brand from Hunter's sister, run by Hunter as a separate Shopify store from [[one-percent-standard-store]]. Stock is already in hand.

## Setup
- Store: Bebita Lifestyle, `8r5u0r-gj.myshopify.com` (alias `bebitalifestyle.myshopify.com`), AUD, trial created 2026-09-29 (initially named "My Store 2"). Trial is short (3 days showed on day one), so pick a plan before it locks.
- Claude access: its own Dev Dashboard app, **Claude Bebita**, with the same 26 scopes as the One Percent app. Keys in `~/.zshrc` as `BEBITA_STORE`, `BEBITA_CLIENT_ID`, `BEBITA_CLIENT_SECRET`.
- Same helper as One Percent: `STORE=bebita ./shopify.sh …` in [projects/shopify-store/](../../projects/shopify-store/shopify.sh). The token cache is per store, so they can't cross.
- Hunter has an ABN, so a `.com.au` domain is possible.

## Sources
All products and brand content live on Instagram: [@bebitaactive](https://www.instagram.com/bebitaactive/) and [@bebitaswim](https://www.instagram.com/bebitaswim/). OpenCLI and Jina both failed on 2026-09-29 (429 / blocked); **Claude in Chrome with Hunter's logged-in session worked**.
- **@bebitaactive**: 279 posts, ~3.5k followers, bio "CLOSED DOWN". Seamless scrunch shorts, sports bras and leggings in pastel pink, lilac, baby blue, cobalt and hot pink; gym-shot content; last posts push a 50% off sale.
- **@bebitaswim**: 537 posts, ~7.1k followers, bio "CLOSED DOWN". Triangle bikinis (red, pink, white, peach, cobalt, aqua, brown/metallic); highlights for Drop 1–3, FAQs, "Amarni" and events; also ended on a 50% off sale.
- Brand look: blush-pink circle avatar with a white script "Bebita" wordmark.
- Both accounts say closed down, so the Shopify store is either a relaunch or a sell-through of remaining stock. That decides how much to build.

## Positioning (decided 2026-09-30)
**Build your set.** Tops and bottoms are sold as separate products in any size and colour, with a bundle discount when she buys both (a Shopify automatic discount, set up once the prices are known). The research is in [[research-activewear-pain-points]]. Supporting points: dispatch from the Gold Coast, easy size swaps, and real stock counts. The relaunch angle, a squat and sweat test filmed per colour, waits until that footage exists.

## Home page build
Impeccable comp-led build, direction "gym mirror selfie". Hunter chose the approved comp: a row of arched chrome mirrors, one colourway each ([comp](../../projects/shopify-store/bebita/.impeccable/mocks/home-comp-b-mirror-row.png)). The spec is measured, and the headline face ranks as Parkinsans 700. The next step is the mirror photos. Instagram captures proved unusable (about 600px, video play buttons baked in), so the build waits for the original files. Spend so far: 225 Magnific credits.

## Live build (2026-09-30)
The custom home page is live on the store theme: a row of mirrors with "Build your set.", pick a top and pick a bottom, Active and Swim as mirrored full-bleed lines, "the original run is back", a change-room image pair, and a promise strip. The header has the script logo with "Collective" and a menu drawer. Built from Bebita's own Instagram photos: 789 were saved into `raw/bebita/` (git-ignored). Tag-driven collections, About and FAQ pages, and the main menu are set up. Details, the photo map and the credit tally are in [BUILD-LOG.md](../../projects/shopify-store/bebita/BUILD-LOG.md). The store has since been renamed to Bebita Collective in the admin, and its handle is now `bebitacollective`.

## Open
- Product list: styles, sizes, colours, stock counts, cost and price.
- Photos, logo, brand colours.
- Pages (About needs the real brand story from Hunter's sister), home page, theme.

## Done 2026-09-29
- Ship-from location copied from the One Percent address (Upper Coomera QLD 4209).
- Shipping: Standard $9.95 under $100, free Standard at $100+, Express $14.95, international off. Threshold is higher than One Percent's $75 because apparel orders run bigger.
- Refund policy (30-day change of mind, unworn with tags; swimwear only with the hygiene liner intact; sale items exchange-only; ACL faulty cover) and shipping policy, drafts in [bebita/content/](../../projects/shopify-store/bebita/content/). Footer menu links the policies.

## 2026-10-05: v3 storefront (ready, waiting on a Shopify plan)
- **Redesign:** the store now follows velocityactivewear.com.au's layout in black and white, keeping the original Bebita script logo. Single prices, a 10% sign-up offer (BEBITA10), free shipping over $150, add-ons in the bag below the threshold, and stock-based "Only N left" / "Selling fast" labels. A request for fake +15% "was" prices was declined as misleading under the ACL.
- **Stock:** the real stock take is loaded via `load_stock.py`. ⚠️ Updated 2026-10-06: now 336 pieces across 26 products. Thin Strap Triangle Top, Scrunch Halter and Cross Back Flare Set were dropped, and Hunter's real product names were applied (the rename table is in `photo_map.json` and the Apple Note "Bebita – Product Name Changes").
- **Photos:** a former model has been removed from every photo where her face shows. Her shots were either swapped for the dark-haired model's or had the face AI-replaced with a glam invented face (Magnific Nano Banana 2 retouch, about 1,200 credits in total). Details are in [BUILD-LOG](../../projects/shopify-store/bebita/BUILD-LOG.md).
- **AI product shots (2026-10-06):** each of the 25 colourways Hunter photographed flat now has a Nano Banana Pro on-model shot and a ghost-mannequin studio shot: 50 images in `products/ai/`, 3,675 credits. The model shot leads the product page and the studio shot shows on hover. The other roughly 75 colourways still use their Instagram photos. A redo of 13 shots on 2026-10-06 (975 credits) fixed the missing V-back waistbands, the hidden scrunch backs and three wrong blues. Bebita's Magnific total is about 6,138 credits. Lesson: Hunter expected generated product photography, not cleaned-up versions of his own photos, so ask which one is wanted before any "fix the photos" job. Also, name each product's defining feature in the prompt (V waistband, scrunch, pockets, exact shade), because the product name alone doesn't carry it.
- **Live 2026-10-08:** Hunter bought the Basic plan. `go_live_vx.py` ran: 26 products and 336 pieces with AI photos, BEBITA10 created, the vx theme pushed. The vx-footer schema had to change because Shopify rejects external-URL defaults on `url` settings; the IG links now sit in footer-group.json. Shipping: domestic $9.95 standard under $150, free from $150, $14.95 express, and $20 international. The storefront password page is still on, which only Hunter can switch off in Online Store > Preferences. **⚠️ Gotcha (2026-10-10):** the "claude bebita" API app has no `write_publications` scope, so products created through the API are never added to the Online Store channel and the storefront shows "no products". The fix is to bulk-add them in the admin (Products → select all → Include in sales channel → Online Store) or add the scope to the app. Any future product load needs the same step.
- **Launch (earlier):** the store returned 402 (trial ended). Once a plan is picked, run `STORE=bebita python3 bebita/go_live_vx.py`.

- **2026-10-10 polish:** the site is public (Hunter published all 26 products and removed the password; card and PayPal show at checkout). Product pages gained an AU size table (XS–XL, bust/waist/hips in cm) and a Fabric & care section chosen by product (seamless, performance, swim, sarong, bedazzled). These are generic gym-wear copy at Hunter's request, with no exact blend percentages. Each product now opens on the colour that has the AI model shot (`productOptionsReorder`, and `load_stock.py` sorts the same way). The $20 international rate was switched off to match the Australia-only policy. On 990–1279px screens the nav uses the hamburger menu, because 7 links collided with the logo.
- **2026-10-11:** Hunter said crumpled flat-lays look unprofessional, so 13 were removed from the store and moved to `products/flat-removed/` (where `load_stock.py` won't pick them up): all 6 shorts photos, the 4 twisted or inside-out Sculpt shots, and the tangled bikini, crumpled one piece and bunched Bedazzled. The 31 neat flat-lays stay. Standard: only flat-lays that are laid smooth go on the site.
