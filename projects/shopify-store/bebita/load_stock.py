#!/usr/bin/env python3
"""Load Bebita's real stock (stock.py) into Shopify: one product per style, Colour x Size variants,
real inventory counts (0 = sold out), prices below, and a photo per colour from the Instagram archive.

Usage: STORE=bebita python3 bebita/load_stock.py [--delete-placeholders]
Re-running updates products by handle; stock counts are only written on create unless --reset-stock.
"""
import os, sys, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from publish_content import gql  # noqa: E402
from load_placeholder_products import stage  # noqa: E402
from stock import STOCK  # noqa: E402

RAW = os.path.join(HERE, "..", "..", "..", "raw", "bebita")
OUT = os.path.join(HERE, "products")
LOCATION = "gid://shopify/Location/90998997075"
SIZE_ORDER = ["XS", "S", "M", "L", "XL", "XS-S", "M-L", "One size"]

PRICE = {
 "Muse Scrunch Shorts": 45, "Dynamic Shorts": 45, "V-Back Scrunch Shorts": 45, "V-Back Scrunch Leggings": 59, "Muse Scrunch Leggings": 59,
 "Dynamic Leggings": 59, "Dynamic Flares": 59, "Signature Cross Back Bralette": 42, "Open Back Top": 45, "Cross Back Straight Top": 42,
 "Signature Halter": 39, "Signature Triangle Bralette": 39, "Signature Triangle Halter": 39, "Dynamic Bra": 42, "Scrunch Halter Top": 39,
 "Signature Twist Bra": 42, "Cross Back Thin Strap Triangle Top": 39, "Two Tone Halter": 42,
 "Two Tone Layered Long Sleeve Crop": 59, "Signature Cropped Zip": 69, "Cross Back Flare Set": 95,
 "One Piece Short": 65, "One Piece Long": 75, "Triangle Bikini Top": 39, "Triangle Bikini Top With Cheeky Brazilian Bottom": 79,
 "V-Front Cheeky Brazilian One Piece": 75, "Ruched Swim Skirt": 35, "Sarong": 29, "Bedazzled Cover Up": 49,
}

# Former team members are kept off the site: the pink-twist-set blonde (a218, a222, a092, a143, a220, a260, a089, a221 group) and the
# platinum-blonde-with-dark-roots model, whose face was AI-replaced in edited/ (a175, a177, a203, s024, s112, s113) or whose shots were
# swapped (a201 and a104 cropped to the right half, a131, a077, a075, a078, a082, a085, a086, a048, s044, s050, s067, s084, s085, s117, a206, s071, s085, s099).
# Instagram photo per colour: a### = @bebitaactive, s### = @bebitaswim. "_" = the product's fallback photo.
PHOTOS = {
 "Muse Scrunch Shorts": {"Red": "a087", "Light Blue": "a223", "Dark Blue": "a005", "Highlighter Pink": "a084", "Peach": "a246", "Black": "a250", "Pink": "a080"},
 "Dynamic Shorts": {"Grey": "a173", "Teal": "a249", "Blue": "a010", "Pink": "a015", "Lilac": "a025", "Coral": "a006", "Baby Blue": "a019", "Baby Pink": "a003"},
 "V-Back Scrunch Shorts": {"Blue": "a205", "Pink": "a187", "Black": "a203", "Brown": "a196"},
 "V-Back Scrunch Leggings": {"Blue": "a189", "Brown": "a190", "Pink": "a179", "Black": "a200", "Highlighter Pink": "a204"},
 "Muse Scrunch Leggings": {"Pink": "a155", "Navy": "a191", "Brown": "a147"},
 "Dynamic Leggings": {"_": "a018"},
 "Dynamic Flares": {"Lilac": "a071", "Black": "a041", "Blue": "a068"},
 "Signature Cross Back Bralette": {"Lilac": "a014", "Blue": "a026", "Black": "a176"},
 "Open Back Top": {"Blue": "a056", "Pink": "a046", "Brown": "a065", "Black": "a076"},
 "Cross Back Straight Top": {"Brown": "a175", "Blue": "a201R", "Highlighter Pink": "a177", "Black": "a203"},
 "Signature Halter": {"Teal": "a174", "Blue": "a164"},
 "Signature Triangle Bralette": {"Blue": "a008", "Bone Grey": "a053", "Grey": "a170"},
 "Signature Triangle Halter": {"_": "a164"},
 "Dynamic Bra": {"Blush Pink": "a013", "Baby Blue": "a019", "Lilac": "a025", "Coral": "a006"},
 "Scrunch Halter Top": {"_": "a014"},
 "Signature Twist Bra": {"Red": "a270", "Highlighter Pink": "a084", "Teal": "a249", "Pink": "a227", "Black": "a250", "Blue": "a226"},
 "Cross Back Thin Strap Triangle Top": {"_": "a198"},
 "Two Tone Halter": {"_": "a069", "Brown/White": "a069"},
 "Two Tone Layered Long Sleeve Crop": {"Brown/White": "a065", "Navy/White": "a056", "Black/White": "a057"},
 "Signature Cropped Zip": {"_": "a016", "Lilac": "a071", "Blue": "a047"},
 "Cross Back Flare Set": {"_": "a071"},
 "One Piece Short": {"Blue": "a149", "Red": "a148", "Pink": "a093", "Black": "a125"},
 "One Piece Long": {"Blue": "a156", "Red": "a127", "Pink": "a095", "Black": "a104R"},
 "Triangle Bikini Top": {"White": "s074", "Hot Pink": "s043", "Black": "s070", "Brown": "s026", "Teal": "s048", "Blue": "s110", "Coral": "s028"},
 "Triangle Bikini Top With Cheeky Brazilian Bottom": {"_": "s053", "White": "s074", "Coral": "s049", "Blue": "s114", "Red": "s046", "Black": "s070", "Teal": "s053", "Hot Pink": "s052", "Brown": "s001"},
 "V-Front Cheeky Brazilian One Piece": {"_": "s112", "Black": "s116"},
 "Ruched Swim Skirt": {"Teal": "s113", "Hot Pink": "s093R", "Black": "s102"},
 "Sarong": {"Red": "s078", "Black": "s070", "Blue": "s068", "White": "s074", "Coral": "s049", "Hot Pink": "s040", "Teal": "s053", "Brown": "s007"},
 "Bedazzled Cover Up": {"_": "s081"},
}

BLURB = {
 "top": "Sold on its own, so you can pair it with any bottom in your own size.",
 "bottom": "Sold on its own, so you can pair it with any top in your own size.",
 "one-piece": "One piece, nothing to match.", "set": "Sold as a set.", "layer": "The layer to throw over any set.",
 "accessory": "One size.",
}


def handle(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def photo(ref, h, colour):
    half = ref[4:] if len(ref) > 4 else ""     # "a201R" = right half of a201 (keeps one person out of shot)
    ref = ref[:4]
    acc = "active" if ref[0] == "a" else "swim"
    folder = os.path.join(RAW, f"instagram-{acc}")
    src = next(f for f in os.listdir(folder) if f.startswith(f"bebita{acc}_{ref[1:]}_"))
    edited = os.path.join(HERE, "edited", f"{ref}.jpg")   # face-replaced versions win over the originals
    if os.path.exists(edited):
        folder, src = os.path.dirname(edited), os.path.basename(edited)
    dst = os.path.join(OUT, f"bebita-{h}-{handle(colour)}.jpg")
    if not os.path.exists(dst):
        im = Image.open(os.path.join(folder, src)).convert("RGB")
        if half:
            w0, h0 = im.size
            im = im.crop((w0 // 2, 0, w0, h0) if half == "R" else (0, 0, w0 // 2, h0))
        w, hgt = im.size; tw = min(w, int(hgt * 2 / 3)); th = int(tw * 3 / 2)   # centre-crop to 2:3 portrait
        left, top = (w - tw) // 2, max(0, (hgt - th) // 3)
        im = im.crop((left, top, left + tw, top + th)); im.thumbnail((1200, 1800))
        im.save(dst, quality=86, optimize=True, progressive=True)
    return dst


def existing(h):
    p = gql("query($h: String!) { productByIdentifier(identifier: {handle: $h}) { id } }", {"h": h})
    return (p.get("productByIdentifier") or {}).get("id")


def delete_placeholders():
    d = gql('{ products(first: 50, query: "tag:placeholder") { nodes { id handle } } }')["products"]["nodes"]
    for p in d:
        gql("mutation($i: ProductDeleteInput!) { productDelete(input: $i) { deletedProductId userErrors { message } } }", {"i": {"id": p["id"]}})
        print("deleted placeholder", p["handle"])


def main():
    os.makedirs(OUT, exist_ok=True)
    if "--delete-placeholders" in sys.argv:
        delete_placeholders()
    reset = "--reset-stock" in sys.argv
    for name, line, role, cols in STOCK:
        h = handle(name)
        pid = existing(h)
        sizes = [s for s in SIZE_ORDER if any(s in v for v in cols.values())]
        refs = PHOTOS.get(name, {})
        fallback = refs.get("_") or next(iter(refs.values()), None)
        uploaded, files, variants = {}, [], []
        for colour in cols:
            ref = refs.get(colour, fallback)
            url = None
            if ref and not pid:
                key = ref
                if key not in uploaded:
                    uploaded[key] = stage(photo(ref, h, colour))
                    files.append({"originalSource": uploaded[key], "alt": f"{name} in {colour}", "contentType": "IMAGE"})
                url = uploaded[key]
            for s in sizes:
                q = cols[colour].get(s, 0)
                v = {"optionValues": [{"optionName": "Colour", "name": colour}, {"optionName": "Size", "name": s}],
                     "price": f"{PRICE[name]:.2f}", "inventoryPolicy": "DENY", "inventoryItem": {"tracked": True},
                     "inventoryQuantities": [{"locationId": LOCATION, "name": "available", "quantity": q}]}
                if url:
                    v["file"] = {"originalSource": url, "alt": f"{name} in {colour}", "contentType": "IMAGE"}
                if pid and not reset:
                    v.pop("inventoryQuantities")
                variants.append(v)
        tags = [line, role] + (["top"] if role == "set" else [])
        inp = {"handle": h, "title": name, "vendor": "Bebita Collective",
               "descriptionHtml": f"<p>From the original Bebita {line.title()} run. {BLURB[role]} Once these are gone, they're gone.</p>",
               "productType": "Swim" if line == "swim" else "Activewear", "tags": tags, "status": "ACTIVE",
               "productOptions": [{"name": "Colour", "values": [{"name": c} for c in cols]},
                                  {"name": "Size", "values": [{"name": s} for s in sizes]}],
               "variants": variants}
        if pid:
            inp["id"] = pid
        if files:
            inp["files"] = files
        r = gql("""mutation($input: ProductSetInput!) { productSet(synchronous: true, input: $input) {
            product { handle variantsCount { count } totalInventory } userErrors { field message code } } }""", {"input": inp})["productSet"]
        if r["userErrors"]:
            sys.exit(f"{h}: {r['userErrors']}")
        p = r["product"]
        print(("updated" if pid else "created"), p["handle"], p["variantsCount"]["count"], "variants,", p["totalInventory"], "in stock")


if __name__ == "__main__":
    main()
