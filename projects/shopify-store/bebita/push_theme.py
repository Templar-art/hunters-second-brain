#!/usr/bin/env python3
"""Push Bebita theme files to the live theme.

Usage: STORE=bebita python3 bebita/push_theme.py sections/bb-cart.liquid assets/bebita.css templates/cart.json=theme-backup/cart.v2.json
A plain path is read from bebita/theme/<path>; `dest=src` uploads a local file (relative to bebita/) to a different theme path.
"""
import base64, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from publish_content import gql  # noqa: E402

THEME = open(os.path.join(HERE, "theme-backup", "theme-id.txt")).read().strip()
if not THEME.startswith("gid://"):
    THEME = f"gid://shopify/OnlineStoreTheme/{THEME}"

files = []
for arg in sys.argv[1:]:
    dest, _, src = arg.partition("=")
    path = os.path.join(HERE, src) if src else os.path.join(HERE, "theme", dest)
    data = open(path, "rb").read()
    if dest.endswith((".woff2", ".png", ".jpg")):
        files.append({"filename": dest, "body": {"type": "BASE64", "value": base64.b64encode(data).decode()}})
    else:
        files.append({"filename": dest, "body": {"type": "TEXT", "value": data.decode()}})

r = gql("""mutation($t: ID!, $f: [OnlineStoreThemeFilesUpsertFileInput!]!) { themeFilesUpsert(themeId: $t, files: $f) {
    upsertedThemeFiles { filename } userErrors { filename code message } } }""", {"t": THEME, "f": files})["themeFilesUpsert"]
for u in r["upsertedThemeFiles"] or []:
    print("live ", u["filename"])
for e in r["userErrors"]:
    print("ERROR", e["filename"], e["code"], e["message"])
sys.exit(1 if r["userErrors"] else 0)
