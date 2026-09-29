#!/usr/bin/env python3
"""Upload local images to a store's Files (Content > Files) and print their shopify:// references.

Usage: STORE=bebita python3 upload_files.py path/to/a.jpg path/to/b.png ...
Files that already exist in the store under the same name are skipped, so re-runs are safe.
"""
import json
import mimetypes
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publish_content import gql  # noqa: E402  (shares the token-swapping GraphQL helper)


def existing_names():
    names, cursor = set(), None
    while True:
        after = f', after: "{cursor}"' if cursor else ""
        d = gql(f"{{ files(first: 100{after}) {{ nodes {{ ... on MediaImage {{ image {{ url }} }} }} pageInfo {{ hasNextPage endCursor }} }} }}")["files"]
        for n in d["nodes"]:
            url = (n.get("image") or {}).get("url") or ""
            if url:
                names.add(url.split("/")[-1].split("?")[0])
        if not d["pageInfo"]["hasNextPage"]:
            return names
        cursor = d["pageInfo"]["endCursor"]


def upload(path):
    name = os.path.basename(path)
    mime = mimetypes.guess_type(name)[0] or "image/jpeg"
    target = gql("""mutation($i: [StagedUploadInput!]!) { stagedUploadsCreate(input: $i) {
        stagedTargets { url resourceUrl parameters { name value } } userErrors { message } } }""",
                 {"i": [{"filename": name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST",
                         "fileSize": str(os.path.getsize(path))}]})["stagedUploadsCreate"]["stagedTargets"][0]
    cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", target["url"]]
    for p in target["parameters"]:
        cmd += ["-F", f'{p["name"]}={p["value"]}']
    cmd += ["-F", f"file=@{path}"]
    code = subprocess.run(cmd, capture_output=True, text=True).stdout
    if not code.startswith("2"):
        sys.exit(f"upload failed for {name}: HTTP {code}")
    r = gql("""mutation($f: [FileCreateInput!]!) { fileCreate(files: $f) {
        files { id fileStatus } userErrors { field message } } }""",
            {"f": [{"originalSource": target["resourceUrl"], "contentType": "IMAGE", "filename": name}]})["fileCreate"]
    if r["userErrors"]:
        sys.exit(f"fileCreate failed for {name}: {r['userErrors']}")
    return r["files"][0]["id"]


def main():
    have = existing_names()
    for path in sys.argv[1:]:
        name = os.path.basename(path)
        if name in have:
            print(f"skip   shopify://shop_images/{name}")
            continue
        upload(path)
        print(f"added  shopify://shop_images/{name}")
        time.sleep(0.3)


if __name__ == "__main__":
    main()
