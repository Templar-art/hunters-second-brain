# Bebita Collective: build log

Owner: Hunter (sister's brand). Store `8r5u0r-gj.myshopify.com`, helper `STORE=bebita ../shopify.sh`.

## Credit tally (Magnific)
Budget: 1,000 credits approved 2026-09-30, on top of the direction-round comps.

| Date | Item | Credits | Running |
|---|---|---|---|
| 2026-09-30 | 3 home-page comps (direction round) | 225 | 225 |
| 2026-09-30 | Bebita / COLLECTIVE logo lockup (budget 1/1000) | 75 | 300 |

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
