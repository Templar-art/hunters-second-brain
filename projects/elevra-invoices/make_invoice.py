#!/usr/bin/env python3
"""Render an Elevra Media invoice: JSON config -> HTML -> A4 PDF.

Usage:
    python3 make_invoice.py invoices/EM-260713-001.json

Outputs <stem>.html and <stem>.pdf beside the JSON. Stdlib only.
"""

import base64
import json
import mimetypes
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE / "invoice_template.html"

# Chrome lives on the Desktop on this machine, not /Applications.
CHROME = Path("/Users/10xhunter/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome")


def money(amount):
    return f"${amount:,.2f}"


def keep_spaces(text):
    """HTML collapses runs of whitespace; the original invoice pads the bank
    figures ("BSB:  064486") and the footer separators, so protect them."""
    return re.sub(r"  +", lambda m: "&nbsp;" * len(m.group()), text)


def render_lines(lines, css_class="party-line"):
    return "\n        ".join(
        f'<div class="{css_class}">{keep_spaces(line)}</div>' for line in lines
    )


def render_rows(items):
    rows = []
    for item in items:
        qty = item.get("qty", 1)
        rate = item["rate"]
        total = item.get("total", qty * rate)
        note = item.get("note", "")
        note_html = f'\n            <div class="item-note">{note}</div>' if note else ""
        rows.append(
            "<tr>\n"
            f'          <td>\n            <div class="item-desc">{item["description"]}</div>'
            f"{note_html}\n          </td>\n"
            f"          <td>{qty:g}</td>\n"
            f"          <td>{money(rate)}</td>\n"
            f"          <td>{money(total)}</td>\n"
            "        </tr>"
        )
    return "\n        ".join(rows)


def brand_block(cfg):
    """Header-band brand: an embedded logo image if the config names one
    (path relative to this script, e.g. "assets/harcourts-primary-logo.png"),
    otherwise the original stacked brand-name/sub-line text."""
    logo = cfg.get("brand_logo")
    if logo:
        logo_path = HERE / logo
        if not logo_path.exists():
            raise SystemExit(f"brand_logo not found: {logo_path}")
        mime = mimetypes.guess_type(logo_path.name)[0] or "image/png"
        data = base64.b64encode(logo_path.read_bytes()).decode()
        return f'<img class="brand-logo" src="data:{mime};base64,{data}" alt="{cfg.get("brand", "")}">'
    brand = cfg.get("brand", cfg["from"]["name"].split()[0].upper())
    brand_sub = cfg.get("brand_sub", "— M E D I A —")
    return (
        f'<div><div class="brand">{brand}</div>'
        f'<div class="brand-sub">{brand_sub}</div></div>'
    )


def build_html(cfg):
    items = cfg["items"]
    subtotal = sum(i.get("total", i.get("qty", 1) * i["rate"]) for i in items)

    # GST is a string, not a number: this ABN is not registered, so the invoice
    # must SAY "Not applicable" rather than print $0.00 (which implies a 0% charge).
    gst = cfg.get("gst", "Not applicable")
    total = subtotal if isinstance(gst, str) else subtotal + gst

    sender, client = cfg["from"], cfg["to"]
    swaps = {
        "__TITLE__": f'{cfg["invoice_no"]} · {sender["name"]}',
        "__BRAND_BLOCK__": brand_block(cfg),
        "__BAND_COLOR__": cfg.get("band_color", "#2563eb"),
        "__INVOICE_NO__": cfg["invoice_no"],
        "__DATE__": cfg["date"],
        "__DUE__": cfg.get("due", "On Receipt"),
        "__FROM_NAME__": sender["name"],
        "__FROM_LINES__": render_lines(sender.get("lines", [])),
        "__TO_NAME__": client["name"],
        "__TO_LINES__": render_lines(client.get("lines", [])),
        "__ROWS__": render_rows(items),
        "__SUBTOTAL__": money(subtotal),
        "__GST__": gst if isinstance(gst, str) else money(gst),
        "__CURRENCY__": cfg.get("currency", "AUD"),
        "__TOTAL__": money(total),
        "__PAY_LINES__": render_lines(cfg["payment"]["lines"], "pay-line"),
        "__PAY_NOTE__": cfg["payment"].get(
            "note", "Please include the invoice number as your payment reference."
        ),
        "__FOOTER__": keep_spaces(
            cfg.get("footer") or "  •  ".join(cfg.get("footer_parts", []))
        ),
    }

    html = TEMPLATE.read_text()
    for placeholder, value in swaps.items():
        html = html.replace(placeholder, str(value))

    leftover = [p for p in swaps if p in html]
    if leftover:
        raise SystemExit(f"unreplaced placeholders: {leftover}")
    return html, total


def to_pdf(html_path, pdf_path):
    if not CHROME.exists():
        raise SystemExit(f"Chrome not found at {CHROME} — update CHROME in this script.")
    subprocess.run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
        check=True,
        capture_output=True,
    )


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)

    cfg_path = Path(sys.argv[1]).resolve()
    cfg = json.loads(cfg_path.read_text())
    html, total = build_html(cfg)

    html_path = cfg_path.with_suffix(".html")
    pdf_path = cfg_path.with_suffix(".pdf")
    html_path.write_text(html)
    to_pdf(html_path, pdf_path)

    print(f"{cfg['invoice_no']}  {money(total)} {cfg.get('currency', 'AUD')}")
    print(f"  {html_path}")
    print(f"  {pdf_path}")


if __name__ == "__main__":
    main()
