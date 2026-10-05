# Bebita Collective: build log

Owner: Hunter (sister's brand). Store `8r5u0r-gj.myshopify.com`, helper `STORE=bebita ../shopify.sh`.

## Credit tally (Magnific)
Budget: 1,000 credits approved 2026-09-30, on top of the direction-round comps.

| Date | Item | Credits | Running |
|---|---|---|---|
| 2026-09-30 | 3 home-page comps (direction round) | 225 | 225 |
| 2026-09-30 | Bebita / COLLECTIVE logo lockup (budget 1/1000) | 75 | 300 |
| 2026-10-04 | Face replacement test, a175 (Nano Banana 2 retouch, 2K) | 75 | 375 |
| 2026-10-05 | Face replacement batch: a177, a203, a131, s024, s112, s113 succeeded (a131 came out warped and is unused) | 450 | 825 |
| 2026-10-05 | Glam redo (full makeup) after Hunter said the first face looked plain: a175, a177, a203, s112, s113 succeeded; s024 was blocked by the filter (photo swapped to s078) | 375 | 1,200 |
| 2026-10-05 | s071 face replacement failed twice ("no image content", likely the model's filter); failed jobs should be refunded, so verify on the dashboard | 0–150 | 825–975 |

## Built and live on the store (2026-09-30)
- Custom theme sections, all editable in the theme editor: `bb-header` (script logo, "Collective", menu drawer, bag count), `bb-mirrors`, `bb-build`, `bb-line` (Active and Swim, mirrored), `bb-statement`, `bb-room` and `bb-promise`. Shared CSS and JS are in `theme/assets/`, with self-hosted Parkinsans 800 and Public Sans. Originals of every theme file are in `theme-backup/`.
- Images are Bebita's own Instagram photos. The mirrors are real selfies composited into drawn chrome frames by `.impeccable/build/make_mirrors.py`. Hunter chose real photos over the comp's AI figures, and that override is recorded on the plates and hero gates.
- Photo map: mirror-1 = active 084, mirror-2 = 169, mirror-3 = 058; mix-duo = 063; active-group = 027; swim-beach = swim 001; room-1 = 154; room-2 = 036.
- Collections: Active, Swim, Tops and Bottoms, filled automatically by product tags (`active`, `swim`, `top`, `bottom`).
- Pages: About and FAQ. Main menu: Active, Swim, Tops, Bottoms, About, FAQ, Contact.
- Theme palette: blush #F6D7DD, plum #39242A, pill buttons. Parkinsans and Public Sans apply site-wide.
- Stated copy changes from the comp: "Build your set.", "Shop tops" and "Shop bottoms", "Start building", and "Hot pink" for mirror 1 to match the real photo.

## v2 (2026-09-30): picker, product page, collection page, audit fixes
- New sections:
  - `bb-picker`: the build-your-set picker. Choose a top and a bottom by style, colour and size, see the live total, then add both to the bag in one `cart/add.js` call. It shows real "only N left" counts and handles sold-out sizes. It reads the Tops and Bottoms collections and the `top`, `bottom`, `active` and `swim` tags. Until any products exist it shows a single "being added" message.
  - `bb-product`: gallery, colour swatches and size chips, honest stock counts, a "Complete the set" link to the matching piece (same first word in the title, opposite role) that deep-links into the picker, and fold-out details.
  - `bb-collection`: arched product cards with a hover image and colour counts, plus an empty state.
- Home page: an Active/Swim switch on the mirrors, with three Swim mirror selfies (swim 017 cobalt, 079 red, 018 chocolate). The mobile hero is now a flowing layout instead of absolute positioning. The desktop hero stacks the switch and actions in the left column. The logo is plum for contrast.
- `/impeccable audit` scored 14/20 before fixes. Fixed:
  - control outlines raised from 1.6:1 to 3.7:1
  - every tap target at least 44px (was 8 under)
  - disabled-button contrast raised from 2.3:1 to 6:1
  - colours tokenised
  - hero image loads first
  - variant images at 1200px
  - picker empty state, and no image tags without a source
  - header "COLLECTIVE" legible again

  Remaining detector notes are deliberate: the logotype size, the edge-to-edge mirror row, and display leading. Verified at 390, 1280, 1440 and 1600 with no horizontal overflow.
- Test harnesses: `prototype/home-test.html` and `prototype/picker-test.html` (sample data, local only).

## State
- Positioning: Build your set. Brand: Bebita Collective, with Active and Swim as sections.
- Approved comp: `.impeccable/mocks/home-comp-b-mirror-row.png`. Build phase: review (finish review and DESIGN.md still to run).
- Photos: 789 Instagram images in `raw/bebita/` (git-ignored).
- Waiting on Hunter: stock list (pieces, colours, sizes, counts, prices), payments, a paid plan, domain.

## Stock take received (2026-10-04)
Hunter's stock count has been transcribed into `stock.py`, which is the source of truth and also writes `stock.csv`. It covers **339 pieces across 29 products**: Active 226, Swim 113. The biggest lines are Brazilian Bikini Sets (47), Sarongs (39), Cross Back Straight Top (32), Scrunch Shorts (28), Cross Back Twist Triangle Top (22) and V-Back Leggings (21).

Interpretations to confirm with Hunter:
- Cropped Zip Jacket: "Lilac M 1" was listed twice, so counted as M ×2.
- One Piece Short: "Blue 1 S 3 M" read as S ×1 and M ×3.
- Cross Back Flare Set: Yellow S, quantity 1 assumed.
- Bikini Skirt sizes are XS-S and M-L.
- Names cleaned up: "Weird Scrunch" became Scrunch Shorts and Scrunch Pants, and "Badazzled" became Bedazzled.

Still blocked on prices before loading.

## v3 (2026-10-04): black-and-white storefront redesign, real stock, urgency, pop-up, cart add-ons
Hunter asked for the store to look like velocityactivewear.com.au (a Shopify Symmetry theme) while carrying both Active and Swim. Only the layout and feel were copied; no logo, text or photos.
- **Layout:**
  - black announcement bar
  - header with the nav on the left, a spaced BEBITA wordmark in the centre, and search and bag on the right
  - full-bleed hero, split Active | Swim on desktop
  - edge-to-edge 2/4-column product grid with 2:3 photos, uppercase titles, price on the right and a colour count
  - Shop tops / Shop bottoms image tiles
  - black footer with newsletter
- **Product page:** gallery (a swipe carousel on phones) beside a sticky panel with photo colour swatches, size buttons, a black "Add to bag" button and fold-outs (details, size guide, delivery).
- **Sections:** `vx-announce`, `vx-header`, `vx-hero`, `vx-grid`, `vx-tiles`, `vx-footer`, `vx-collection`, `vx-product`, `vx-cart` and `vx-popup`; snippets `vx-card` and `vx-assets`; assets `vx.css` and `vx.js`. Templates are in `theme-backup/*.vx.json`. The previous bb- look stays in `*.v2.json` for rollback.
- **Prices** (set by Claude, approved by Hunter): shorts $45; leggings, pants and flares $59; tops $39–42 (Open Back $45); 2-in-1 long sleeve $59; zip jacket $69; flare set $95; active one pieces $65 (short) and $75 (long); triangle bikini top $39; Brazilian set $79; V-front one piece $75; bikini skirt $35; sarong $29; bedazzled cover-up $49. Single prices, no fake "was" prices.
- **Products:** `load_stock.py` creates one product per style with Colour × Size variants. Every size of every colour exists, and missing ones have stock 0, so they show as sold out. Colours with nothing left show a struck-through swatch. Photos are matched by eye from the Instagram archive (`PHOTOS` map). Yellow jacket, Navy/Black two-tone and Purple/Teal fall back to the product's main photo; Hunter should shoot or swap these.
- **Urgency:** every label comes from the real stock count. Card badges: "Only N left" (3 or fewer) and "Selling fast" (8 or fewer). The product page says "Selling fast: only N left in <colour>" or "N sizes have already sold out in <colour>". The announcement bar reads "Final stock: when it's gone, it's gone". There are no fake timers.
- **Pop-up:** 25% off the first order, code **BEBITA25** (one use per customer, created by the go-live script). It opens once a week per visitor, after 6 seconds, at 40% scroll or on exit intent. Sign-ups land in Customers tagged newsletter and welcome-popup.
- **Cart add-ons:** below the free-shipping threshold, the bag page shows "Add $X for free shipping" with sarong, triangle top, bikini skirt and halter tops, each with a colour/size picker and an Add button. Checkout itself can't be edited below Shopify Plus.
- **Local preview** with the real data: `prototype/vx/build.py` writes the `prototype/vx/*.html` pages (launch config `bebita-vx`, port 8150). Verified on a phone-width viewport: hero, grid, product page (variant switching, sold-out sizes, stock messages, colour photo first), bag (add-ons, no overflow) and pop-up.
- **⚠️ Blocked:** the store API returned "Unavailable Shop" and the storefront HTTP 402 on 2026-10-04, meaning the trial has ended and a plan is needed. Once Hunter picks a plan, run `STORE=bebita python3 bebita/go_live_vx.py`.

- 2026-10-04 changes: the email offer is now **10% off the first order, code BEBITA10** (pop-up and footer sign-up), replacing 25%. Free shipping is now **over $150**. The header uses the original Bebita script logo in black (`assets/bebita-vx-logo.png`). Hunter asked for fake +15% "was" prices; Claude declined (misleading under the ACL), so prices stay single.
- 2026-10-04: a former team member (the blonde in the pink twist set with a gold name necklace) left the business, so her photos were removed from the site. Excluded: a218 (old hero, swapped for a201), a221 (bottoms tile, swapped for a204), a092 and a143 (hot pink, swapped for a084), a260 (blue twist top, swapped for a226), a089 (red one piece short, swapped for a148) and a220 (peach shorts, swapped for a246). The list is recorded in `load_stock.py`. Never reuse a213–a270 group shots without checking for her.

- 2026-10-05: face replacement for the platinum-blonde former model. AI faces are in `edited/` (one consistent invented face, natural skin texture, tan matched, necklace removed); `load_stock.py` prefers `edited/<ref>.jpg`. Swapped instead of edited: hero (now edited a177), swim hero (s049), active tile (a196), swim tile (s044), Straight Top Blue (a201 right half), One Piece Long Black (a104 right half), Teal sarong (s053). Prompt lessons: tight face masks (a loose mask on a131 warped the face), and say "exactly the same deep golden tan" plus "pores, never airbrushed" for realism.
- 2026-10-05: prepared without store access: footer Instagram links, store-styled search/page/policy/404 templates (pushed by go_live_vx.py), launch copy (`content/launch-copy.md`), and Hunter's to-do list in Apple Notes ("Bebita – Hunter's to-do list").
- 2026-10-05: Cross Back Thin Strap Triangle Top sold out (Hunter) and removed from stock.py; 28 products / 338 pieces. 46 flat-lay photos mapped in photo_map.json; Hunter's real names applied (see renames there).
- 2026-10-05: Scrunch Halter Top and Cross Back Flare Set also gone (Hunter); removed. 26 products / 336 pieces.
