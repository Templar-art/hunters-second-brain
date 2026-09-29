---
type: project
tags: [shopify, ecommerce, activewear, swimwear]
status: setup
updated: 2026-09-29
---

# Bebita Lifestyle (Shopify store)

Activewear and swimwear brand from Hunter's sister, run by Hunter as a separate Shopify store from [[one-percent-standard-store]]. Stock is already in hand.

## Setup
- Store: Bebita Lifestyle, `8r5u0r-gj.myshopify.com` (alias `bebitalifestyle.myshopify.com`), AUD, trial created 2026-09-29 (initially named "My Store 2"). Trial is short (3 days showed on day one), so pick a plan before it locks.
- Claude access: its own Dev Dashboard app, **Claude Bebita**, with the same 26 scopes as the One Percent app. Keys in `~/.zshrc` as `BEBITA_STORE`, `BEBITA_CLIENT_ID`, `BEBITA_CLIENT_SECRET`.
- Same helper as One Percent: `STORE=bebita ./shopify.sh …` in [projects/shopify-store/](../../projects/shopify-store/shopify.sh). The token cache is per store, so they can't cross.
- Hunter has an ABN, so a `.com.au` domain is possible.

## Open
- Product list: styles, sizes, colours, stock counts, cost and price.
- Photos, logo, brand colours.
- Pages (About needs the real brand story from Hunter's sister), home page, theme.

## Done 2026-09-29
- Ship-from location copied from the One Percent address (Upper Coomera QLD 4209).
- Shipping: Standard $9.95 under $100, free Standard at $100+, Express $14.95, international off. Threshold is higher than One Percent's $75 because apparel orders run bigger.
- Refund policy (30-day change of mind, unworn with tags; swimwear only with the hygiene liner intact; sale items exchange-only; ACL faulty cover) and shipping policy, drafts in [bebita/content/](../../projects/shopify-store/bebita/content/). Footer menu links the policies.
