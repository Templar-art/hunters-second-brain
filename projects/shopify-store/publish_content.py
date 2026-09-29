#!/usr/bin/env python3
"""Push the drafts in content/ to the store: refund + shipping policies, About + FAQ pages.

[EMAIL] is filled from the store's own contact email at publish time, so the address
never lives in the vault. Re-running updates in place (pages matched by handle).
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
CONTENT = HERE / "content"


def gql(query, variables=None):
    qf, vf = HERE / ".q.graphql", HERE / ".v.json"
    qf.write_text(query)
    vf.write_text(json.dumps(variables or {}))
    try:
        out = subprocess.run([str(HERE / "shopify.sh"), "-f", str(qf), str(vf)],
                             capture_output=True, text=True, check=True).stdout
    finally:
        qf.unlink(missing_ok=True)
        vf.unlink(missing_ok=True)
    data = json.loads(out)
    if data.get("errors"):
        sys.exit(f"GraphQL error: {data['errors']}")
    return data["data"]


def inline(text):
    text = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def md_to_html(md):
    """Just enough Markdown for these drafts: h2/h3, paragraphs, lists, tables, bold."""
    out, para, lst, table = [], [], None, []

    def flush():
        nonlocal para, lst, table
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para = []
        if lst:
            tag, items = lst
            out.append(f"<{tag}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{tag}>")
            lst = None
        if table:
            rows = [r for r in table if not re.fullmatch(r"\|[\s|:-]+\|", r)]
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            head = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
            body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
            table = []

    for line in md.splitlines():
        s = line.strip()
        if not s or s == "---":
            flush()
        elif s.startswith("|"):
            if para or lst:
                flush()
            table.append(s)
        elif m := re.match(r"(#{2,3}) (.+)", s):
            flush()
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
        elif m := re.match(r"(-|\d+\.) (.+)", s):
            tag = "ul" if m.group(1) == "-" else "ol"
            if para or table or (lst and lst[0] != tag):
                flush()
            lst = lst or (tag, [])
            lst[1].append(m.group(2))
        else:
            if lst or table:
                flush()
            para.append(s)
    flush()
    return "\n".join(out)


def body_of(path, email):
    md = path.read_text().replace("[EMAIL]", email)
    lines = md.splitlines()
    # Drop the H1 title and any "Placeholders to fill" note; Shopify shows its own title.
    lines = [l for l in lines if not l.startswith("# ") and not l.startswith("Placeholders to fill")]
    return md_to_html("\n".join(lines))


def section(md, heading):
    """Return the text under '## heading' up to the next '## ' or '---'."""
    m = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |^---|\Z)", md, re.S | re.M)
    return m.group(1).strip()


def main():
    email = gql("{ shop { contactEmail } }")["shop"]["contactEmail"]

    for kind, fname in [("REFUND_POLICY", "refund-policy.md"), ("SHIPPING_POLICY", "shipping-policy.md")]:
        r = gql("""mutation($p: ShopPolicyInput!) { shopPolicyUpdate(shopPolicy: $p) {
                   shopPolicy { type url } userErrors { field message } } }""",
                {"p": {"type": kind, "body": body_of(CONTENT / fname, email)}})["shopPolicyUpdate"]
        print(kind, r["userErrors"] or r["shopPolicy"]["url"])

    pages_md = (CONTENT / "pages.md").read_text()
    about = section(pages_md, "About page")
    about = "\n".join(l for l in about.splitlines() if not l.startswith("**Heading:**"))
    faq = section(pages_md, "FAQ")
    # FAQ entries are "**Question?**" then an answer line; render questions as h3.
    faq = re.sub(r"^\*\*(.+?)\*\*$", r"### \1", faq, flags=re.M)
    pages = [("About", "about", md_to_html(about)), ("FAQ", "faq", md_to_html(faq))]

    existing = {p["handle"]: p["id"] for p in gql("{ pages(first:50){ nodes { id handle } } }")["pages"]["nodes"]}
    for title, handle, body in pages:
        page = {"title": title, "handle": handle, "body": body, "isPublished": True}
        if handle in existing:
            r = gql("""mutation($id: ID!, $page: PageUpdateInput!) { pageUpdate(id: $id, page: $page) {
                       page { handle } userErrors { field message } } }""",
                    {"id": existing[handle], "page": page})["pageUpdate"]
        else:
            r = gql("""mutation($page: PageCreateInput!) { pageCreate(page: $page) {
                       page { handle } userErrors { field message } } }""", {"page": page})["pageCreate"]
        print("page", handle, r["userErrors"] or "ok")


if __name__ == "__main__":
    main()
