#!/usr/bin/env python3
"""Load a PLACEHOLDER Bebita catalogue so the store can be built and tested before the real stock list.

Every product is tagged `placeholder`. Prices and stock counts are stand-ins, not real numbers:
replace them from the stock list (or delete the products) before the store password comes off.
Photos are Bebita's own Instagram images from raw/bebita/, resized to 1600px.

Usage: STORE=bebita python3 bebita/load_placeholder_products.py
Re-running updates products by handle instead of duplicating them.
"""
import os, sys, subprocess, mimetypes
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from publish_content import gql  # noqa: E402

RAW = os.path.join(HERE, "..", "..", "..", "raw", "bebita")
OUT = os.path.join(HERE, "products")
LOCATION = "gid://shopify/Location/90998997075"
SIZES = ["XS", "S", "M", "L"]
STOCK = 8  # placeholder per variant

CATALOGUE = [
    dict(handle="seamless-sports-bra", title="Seamless Sports Bra", price="49.00", tags=["active", "top"],
         body="<p>The sports bra from the original Bebita Active run. Sold on its own, so pair it with any bottom in your own size.</p>",
         colours={"Cobalt": "active/005", "Red": "active/109", "Hot pink": "active/092",
                  "Baby blue": "active/260", "Baby pink": "active/227", "Black": "active/250"}),
    dict(handle="seamless-scrunch-shorts", title="Seamless Scrunch Shorts", price="55.00", tags=["active", "bottom"],
         body="<p>Scrunch-back shorts from the original Bebita Active run. Sold on their own, so pair them with any top in your own size.</p>",
         colours={"Cobalt": "active/010", "Red": "active/110", "Hot pink": "active/143",
                  "Baby blue": "active/223", "Baby pink": "active/220", "Black": "active/258"}),
    dict(handle="seamless-leggings", title="Seamless Leggings", price="65.00", tags=["active", "bottom"],
         body="<p>Full-length leggings from the original Bebita Active run. Sold on their own, so pair them with any top in your own size.</p>",
         colours={"Cobalt": "active/189", "Chocolate": "active/190", "Black": "active/199"}),
    dict(handle="triangle-bikini-top", title="Triangle Bikini Top", price="49.00", tags=["swim", "top"],
         body="<p>The triangle top from the original Bebita Swim run. Sold as a separate, so choose the bottom in its own size.</p>",
         colours={"Red": "swim/002", "Cobalt": "swim/067", "Pink": "swim/052",
                  "Chocolate": "swim/005", "Aqua": "swim/053", "White": "swim/074"}),
    dict(handle="triangle-bikini-bottom", title="Triangle Bikini Bottom", price="45.00", tags=["swim", "bottom"],
         body="<p>The tie-side bottom from the original Bebita Swim run. Sold as a separate, so choose the top in its own size.</p>",
         colours={"Red": "swim/046", "Cobalt": "swim/165", "Pink": "swim/043",
                  "Chocolate": "swim/069", "Aqua": "swim/048", "White": "swim/117"}),
]


def prepare(ref, handle, colour):
    acc, num = ref.split("/")
    folder = os.path.join(RAW, f"instagram-{acc}")
    src = next(f for f in os.listdir(folder) if f.startswith(f"bebita{acc}_{num}_"))
    dst = os.path.join(OUT, f"bebita-{handle}-{colour.lower().replace(' ', '-')}.jpg")
    if not os.path.exists(dst):
        im = Image.open(os.path.join(folder, src)).convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(dst, quality=86, optimize=True, progressive=True)
    return dst


def stage(path):
    name = os.path.basename(path)
    t = gql("""mutation($i: [StagedUploadInput!]!) { stagedUploadsCreate(input: $i) {
        stagedTargets { url resourceUrl parameters { name value } } userErrors { message } } }""",
            {"i": [{"filename": name, "mimeType": mimetypes.guess_type(name)[0], "resource": "IMAGE",
                    "httpMethod": "POST", "fileSize": str(os.path.getsize(path))}]})["stagedUploadsCreate"]["stagedTargets"][0]
    cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", t["url"]]
    for p in t["parameters"]:
        cmd += ["-F", f'{p["name"]}={p["value"]}']
    cmd += ["-F", f"file=@{path}"]
    code = subprocess.run(cmd, capture_output=True, text=True).stdout
    if not code.startswith("2"):
        sys.exit(f"upload failed for {name}: HTTP {code}")
    return t["resourceUrl"]


def existing(handle):
    p = gql("query($h: String!) { productByIdentifier(identifier: {handle: $h}) { id } }", {"h": handle})
    return (p.get("productByIdentifier") or {}).get("id")


def main():
    os.makedirs(OUT, exist_ok=True)
    for item in CATALOGUE:
        pid = existing(item["handle"])
        files, variants = [], []
        for colour, ref in item["colours"].items():
            url = None if pid else stage(prepare(ref, item["handle"], colour))
            alt = f'{item["title"]} in {colour}'
            if url:
                files.append({"originalSource": url, "alt": alt, "contentType": "IMAGE"})
            for size in SIZES:
                v = {"optionValues": [{"optionName": "Colour", "name": colour}, {"optionName": "Size", "name": size}],
                     "price": item["price"], "inventoryItem": {"tracked": True},
                     "inventoryQuantities": [{"locationId": LOCATION, "name": "available", "quantity": STOCK}]}
                if url:
                    v["file"] = {"originalSource": url, "alt": alt, "contentType": "IMAGE"}
                if pid:
                    v.pop("inventoryQuantities")  # never overwrite counts on a re-run
                variants.append(v)
        inp = {"handle": item["handle"], "title": item["title"], "descriptionHtml": item["body"],
               "vendor": "Bebita Collective", "productType": "Swim" if "swim" in item["tags"] else "Activewear",
               "tags": item["tags"] + ["placeholder"], "status": "ACTIVE",
               "productOptions": [{"name": "Colour", "values": [{"name": c} for c in item["colours"]]},
                                  {"name": "Size", "values": [{"name": s} for s in SIZES]}],
               "variants": variants}
        if pid:
            inp["id"] = pid
        if files:
            inp["files"] = files
        r = gql("""mutation($input: ProductSetInput!) { productSet(synchronous: true, input: $input) {
            product { id handle variantsCount { count } } userErrors { field message code } } }""", {"input": inp})["productSet"]
        if r["userErrors"]:
            sys.exit(f'{item["handle"]}: {r["userErrors"]}')
        print(("updated" if pid else "created"), r["product"]["handle"], r["product"]["variantsCount"]["count"], "variants")


if __name__ == "__main__":
    main()
