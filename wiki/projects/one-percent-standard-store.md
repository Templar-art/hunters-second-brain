---
type: project
tags: [shopify, ecommerce, white-label]
status: draft-product
updated: 2026-09-29
---

# One Percent Standard (Shopify store)

Hunter's own white-label e-commerce store, separate from 10x client work. 100 units of stock landed with Hunter on 2026-09-29, so this is **self-fulfilled white label, not dropshipping**: Hunter packs and posts (Australia Post MyPost Business via Starshipit/Shippit) until volume justifies a 3PL.

## Setup
- Store: One Percent Standard, `2gasmy-p1.myshopify.com` (alias `onepercentstandard.myshopify.com`), AUD, trial plan. Dev Dashboard org is also named One Percent Standard.
- Claude access: a Dev Dashboard app named **Claude** (version `claude-2`) with product, inventory, order, fulfilment, shipping and location scopes. `claude-1` shipped with no scopes; scopes live in the version, so adding them means releasing a new version and re-approving the install.
- Credentials: `SHOPIFY_STORE`, `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET` in `~/.zshrc` (created 2026-09-29, mode 600). Never in the vault.
- Dev Dashboard apps don't issue a permanent `shpat_` token; [shopify.sh](../../projects/shopify-store/shopify.sh) swaps the client ID/secret for a short-lived token (client-credentials grant) and caches it 20h. Admin GraphQL API `2026-07`.
- Shopify Dev MCP (`@shopify/dev-mcp`) added at user scope for docs and schema lookups.

## Product
**Cuffed D-Ring Lifting Straps** (SKU `OPS-STRAP-DR-01`), one size, sold as a pair. Created 2026-09-29 as a **draft** at A$39.95, 100 in stock at the Upper Coomera location. Copy source: [product.json](../../projects/shopify-store/product.json).
- Supplier: Alibaba, Guangdong (contact Sharon Huang), model LM-WLS260303. Neoprene cuff, hook-and-loop closure, 30cm strap, 1.8mm, 120g gross, "1% One Percent" logo on the cuff, MOQ 100, 25–30 day delivery. Supplier offered a longer velcro tab for thinner wrists (recommended yes).
- **⚠️ Cost corrected:** quoted US$5.60/unit, but the order total was US$663 → US$6.63/unit ≈ A$10.05 (assumed 0.66). Shopify cost set to 10.05, weight 150g packed. The order showed "waiting for supplier to ship" in one screenshot; confirm the stock has actually landed before going live.
- Margin at $39.95 with $9.95 shipping charged: about $27.50 per single order; breakeven on the 100 units about 38 sales. Not GST-registered (under $75k), so the variant is set non-taxable.
- Compliance: low risk, no known AU mandatory standard for lifting straps; Consumer Law accuracy only. Trademark search for the brand name still to do.

## Open
- Weight is a 250g placeholder: weigh one packed unit.
- Strap material and length unconfirmed, so the copy avoids them.
- No photos yet; the product can't go live without them.
- Store details address and a competitor price check.
- Range: ask the same supplier for logo'd complements (figure-8, lasso, wrist wraps, belt) rather than dropshipping unbranded stock under the brand.

## Store copy (drafted 2026-09-29)
Drafts in [content/](../../projects/shopify-store/content/): refund policy (30-day change of mind, ACL faulty cover), shipping policy, home/About/FAQ copy. The copy deliberately claims no founder story, testing or customer counts. Privacy and terms use Shopify's built-in generators. **Published 2026-09-29** by [publish_content.py](../../projects/shopify-store/publish_content.py) (fills [EMAIL] from the store's contact email at publish time; re-runnable): refund + shipping policies, About + FAQ pages, main menu (Home, Shop, About, FAQ, Contact) and footer (Search, FAQ, policies, Contact). Home page (Horizon theme `templates/index.json`): headline hero, "Shop the range" product list, brand statement band; original kept in [theme-backup/](../../projects/shopify-store/theme-backup/). Terms of service still to generate from Shopify's template. App now on `claude-3` with 26 scopes; a new version only takes effect after the store approves it (re-run Install app).

## Related
Hunter's sister's activewear and swimwear brand, Bebita Lifestyle, is a second store to set up (stock already in hand).

## Shipping (set 2026-09-29)
Domestic: Standard $9.95 under $75, free Standard at $75+ (two pairs ship free), Express $14.95. International disabled: a $20 flat rate loses money against AusPost international.

## Lessons (API)
- The app needs `write_locations` to edit a location; `read_locations` only reads it.
- Admin API `2026-07`: `inventorySetQuantities` no longer takes `ignoreCompareQuantity`; `inventoryAdjustQuantities` requires `changeFromQuantity` on each change and an `@idempotent(key:)` directive. `totalInventory` lags a few seconds after an adjustment.
- The default "Standard" rate with a free-over rule is an admin-only multi-condition method; `deliveryProfileUpdate` can't edit its condition. Delete the method and recreate it as two methods with `priceConditionsToCreate` instead.
