#!/usr/bin/env python3
"""Put the vx storefront live in one go, once the store is unlocked (it returned HTTP 402 on 2026-10-04).

Steps: upload hero/tile/pop-up photos to Files -> load the real stock (deletes placeholders) ->
create the BEBITA10 code -> push vx sections, assets and templates. Theme backups of the v2 bb- look stay in theme-backup/.
Usage: STORE=bebita python3 bebita/go_live_vx.py
"""
import os, subprocess, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from publish_content import gql  # noqa: E402
run = lambda *a: subprocess.run([sys.executable, *a], cwd=ROOT, check=True)

shop = gql("{ shop { name } }")["shop"]["name"]
print("store:", shop)
run("upload_files.py", *[os.path.join(HERE, "assets", f) for f in sorted(os.listdir(os.path.join(HERE, "assets"))) if f.startswith("bebita-vx-")])
run(os.path.join(HERE, "load_stock.py"), "--delete-placeholders")

have = gql('{ codeDiscountNodeByCode(code: "BEBITA10") { id } }').get("codeDiscountNodeByCode")
if not have:
    r = gql("""mutation($d: DiscountCodeBasicInput!) { discountCodeBasicCreate(basicCodeDiscount: $d) {
        codeDiscountNode { id } userErrors { field message } } }""", {"d": {
        "title": "Email sign-up 10% off first order", "code": "BEBITA10",
        "startsAt": datetime.datetime.now(datetime.timezone.utc).isoformat(), "appliesOncePerCustomer": True,
        "customerSelection": {"all": True}, "customerGets": {"value": {"percentage": 0.10}, "items": {"all": True}},
        "combinesWith": {"shippingDiscounts": True}}})["discountCodeBasicCreate"]
    print("discount BEBITA10:", r["userErrors"] or "created")

files = ["assets/vx.css", "assets/vx.js", "snippets/vx-assets.liquid", "snippets/vx-card.liquid"] + \
        [f"sections/{f}" for f in sorted(os.listdir(os.path.join(HERE, "theme", "sections"))) if f.startswith("vx-")]
run(os.path.join(HERE, "push_theme.py"), *files)
run(os.path.join(HERE, "push_theme.py"), "templates/index.json=theme-backup/index.vx.json", "templates/product.json=theme-backup/product.vx.json",
    "templates/collection.json=theme-backup/collection.vx.json", "templates/cart.json=theme-backup/cart.vx.json",
    "sections/header-group.json=theme-backup/header-group.vx.json", "sections/footer-group.json=theme-backup/footer-group.vx.json")
print("live. Roll back: push the *.v2.json backups the same way.")
