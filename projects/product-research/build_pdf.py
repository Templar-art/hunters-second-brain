"""Build the printable Construction Product Shortlist (HTML, then PDF via headless Chrome).

Usage: python3 build_pdf.py <data_dir> <out_html>
data_dir holds rows_all.json and img/<key>.jpg (ad creatives pulled from GetHookd).
"""
import base64
import html
import json
import os
import sys

DATA = sys.argv[1]
OUT_HTML = sys.argv[2]
REPORT_DATE = os.environ.get("REPORT_DATE", "Oct 2026")

rows = json.load(open(os.path.join(DATA, "rows_all.json")))
CAT_ORDER = [
    "Loads, ute & trailer", "Concrete, site & machinery", "Fencing & outdoor build",
    "Tools & tool belts", "Measuring & marking", "Electrical & plumbing",
    "Welding & metal", "Doors, cabinets & finishing", "Build & repair materials", "Safety & site gear",
]
for r in rows:
    if r["cat"] == "Safety gear":
        r["cat"] = "Safety & site gear"
LABEL = {"ref": "Reference", "new": "Not yet checked", "maybe": "Maybe", "skip": "Skip"}
ORDER = ["new", "maybe", "ref", "skip"]
CATS = [c for c in CAT_ORDER if any(r["cat"] == c for r in rows)]


def e(s):
    return html.escape(str(s or ""))


def img_tag(key):
    p = os.path.join(DATA, "img", f"{key}.jpg")
    if not os.path.exists(p):
        return '<div class="noimg">No preview</div>'
    return f'<img src="data:image/jpeg;base64,{base64.b64encode(open(p, "rb").read()).decode()}" alt="">'


def card(r):
    links = ""
    if r.get("share"):
        links += f'<a class="btn" href="{e(r["share"])}">Watch the ad</a>'
    if r.get("site"):
        links += f'<a class="btn ghost" href="{e(r["site"])}">Product page</a>'
    days = f'<span class="days">{r["days"]} days running</span>' if r.get("days") else ""
    note = f'<p class="note">{e(r["note"])}</p>' if r.get("note") else ""
    goo = f'<p class="goo"><b>On Google AU now</b>{e(r["google"])}</p>' if r.get("google") else ""
    him = f'<p class="him"><b>Why it could work</b>{e(r["for_him"])}</p>' if r.get("for_him") else ""
    return f'''<article class="card s-{r["status"]}">
  <div class="pic">{img_tag(r["key"])}<span class="tag">{LABEL[r["status"]]}</span></div>
  <div class="info">
    <div class="brand">{e(r["brand"])}</div>
    <h3>{e(r["product"])}</h3>
    {days}
    <p class="fix"><b>Fixes</b>{e(r["problem"])}</p>
    {him}
    {goo}
    {note}
    <div class="links">{links}</div>
    <div class="vote"><span>Your call</span><i></i>Good<i></i>Maybe<i></i>No</div>
  </div>
</article>'''


by_cat = {c: sorted([r for r in rows if r["cat"] == c], key=lambda r: ORDER.index(r["status"])) for c in CATS}
n_total = len(rows)
n_new = sum(1 for r in rows if r["status"] == "new")
longest = max(r["days"] for r in rows if r.get("days"))
toc = "".join(f"<li><span>{e(c)}</span><b>{len(by_cat[c])}</b></li>" for c in CATS)
sections = "".join(
    f'''<section class="cat">
  <header class="cathead"><span class="num">{i:02d}</span><h2>{e(c)}</h2><span class="cnt">{len(by_cat[c])} products</span></header>
  <div class="grid">{"".join(card(r) for r in by_cat[c])}</div>
</section>''' for i, c in enumerate(CATS, 1))

CSS = """
:root{--ink:#17191c;--steel:#2a2e33;--paper:#f4f3ef;--line:#d8d6cf;--muted:#5d6268;--orange:#e8640e;--new:#1f7a4d;--maybe:#b07a0a;--ref:#2f5fa8;--skip:#8a8f96;
--display:"Barlow Condensed","Arial Narrow",Arial,sans-serif;--body:"Barlow",Arial,sans-serif;--mono:"JetBrains Mono",Menlo,monospace}
@page{size:A4;margin:0}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:9.5pt;line-height:1.4}
.cover{height:297mm;background:var(--ink);color:#f4f3ef;position:relative;padding:22mm 18mm;display:flex;flex-direction:column;page-break-after:always;overflow:hidden}
.stripes{position:absolute;left:0;right:0;height:14mm;background:repeating-linear-gradient(-45deg,var(--orange) 0 9mm,var(--ink) 9mm 18mm)}
.stripes.top{top:0}.stripes.bot{bottom:0}
.kicker{font-family:var(--mono);font-size:9pt;letter-spacing:.12em;text-transform:uppercase;color:var(--orange);margin-top:8mm}
.cover h1{font-family:var(--display);font-weight:800;font-size:58pt;line-height:.9;text-transform:uppercase;margin:6mm 0 5mm}
.cover h1 em{font-style:normal;color:var(--orange)}
.lede{font-size:12pt;max-width:150mm;color:#cfd2d6;line-height:1.45;margin:0}
.stats{display:flex;gap:12mm;margin-top:8mm}
.stat b{display:block;font-family:var(--display);font-size:40pt;line-height:1;color:#fff}
.stat span{font-family:var(--mono);font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:#9aa0a6}
.toc{list-style:none;padding:0;margin:8mm 0 0;max-width:125mm;border-top:1px solid #3a3f45}
.toc li{display:flex;justify-content:space-between;padding:1.6mm 0;border-bottom:1px solid #3a3f45;font-family:var(--display);font-weight:600;font-size:12.5pt;text-transform:uppercase}
.toc b{color:var(--orange);font-family:var(--mono);font-size:10pt;font-weight:500}
.howto{margin-top:auto;margin-bottom:16mm;padding-top:6mm;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;font-size:8.5pt;color:#b9bdc2}
.howto b{display:block;font-family:var(--mono);font-size:7.5pt;letter-spacing:.08em;text-transform:uppercase;margin-bottom:1mm}
.k-new b{color:#5fc28f}.k-maybe b{color:#e0b04a}.k-ref b{color:#7aa6e8}.k-skip b{color:#9aa0a6}
.cat{padding:10mm 10mm 4mm;page-break-before:always}
.cathead{display:flex;align-items:baseline;gap:5mm;border-bottom:3px solid var(--ink);padding-bottom:3mm;margin-bottom:6mm}
.num{font-family:var(--mono);font-size:10pt;color:var(--orange)}
.cathead h2{font-family:var(--display);font-weight:800;font-size:28pt;text-transform:uppercase;margin:0;line-height:1}
.cnt{margin-left:auto;font-family:var(--mono);font-size:8.5pt;color:var(--muted)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.card{background:#fff;border:1px solid var(--line);border-radius:2mm;display:grid;grid-template-columns:26mm 1fr;overflow:hidden;break-inside:avoid;page-break-inside:avoid}
.pic{position:relative;background:var(--steel);min-height:48mm}
.pic img{width:100%;height:100%;object-fit:cover;display:block;position:absolute;inset:0}
.noimg{color:#9aa0a6;font-family:var(--mono);font-size:7pt;padding:4mm}
.tag{position:absolute;left:0;bottom:0;right:0;font-family:var(--mono);font-size:6.5pt;letter-spacing:.06em;text-transform:uppercase;color:#fff;padding:1.2mm 2mm;background:var(--c)}
.s-new{--c:var(--new)}.s-maybe{--c:var(--maybe)}.s-ref{--c:var(--ref)}.s-skip{--c:var(--skip)}
.info{padding:3mm 3.2mm;display:flex;flex-direction:column;gap:1.4mm;min-width:0}
.brand{font-family:var(--mono);font-size:7pt;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.info h3{font-family:var(--display);font-weight:700;font-size:13.5pt;line-height:1.05;margin:0;text-transform:uppercase}
.days{font-family:var(--mono);font-size:7pt;color:var(--orange)}
.fix{margin:0;font-size:8.6pt}
.fix b{display:block;font-family:var(--mono);font-size:6.5pt;letter-spacing:.08em;text-transform:uppercase;color:var(--orange);font-weight:500}
.him{margin:0;font-size:8.3pt;background:#f1efe8;padding:1.6mm 2mm;border-radius:1mm}
.him b{display:block;font-family:var(--mono);font-size:6.5pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);font-weight:500}
.goo{margin:0;font-size:7.9pt;border-left:2px solid #2f5fa8;padding-left:2mm}
.goo b{display:block;font-family:var(--mono);font-size:6.5pt;letter-spacing:.08em;text-transform:uppercase;color:#2f5fa8;font-weight:500}
.note{margin:0;font-size:7.8pt;color:var(--muted);border-left:2px solid var(--c);padding-left:2mm}
.links{margin-top:auto;display:flex;gap:2mm;flex-wrap:wrap;padding-top:1mm}
.btn{font-family:var(--display);font-weight:700;font-size:8pt;text-transform:uppercase;letter-spacing:.03em;text-decoration:none;background:var(--ink);color:#fff;padding:1mm 2.2mm;border-radius:1mm}
.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--ink)}
.vote{display:flex;flex-wrap:wrap;row-gap:1mm;align-items:center;gap:1.4mm;font-family:var(--mono);font-size:7pt;text-transform:uppercase;letter-spacing:.05em;border-top:1px dashed var(--line);padding-top:1.6mm;margin-top:.6mm}
.vote span{color:var(--orange);width:100%}
.vote i{display:inline-block;flex:none;width:3.2mm;height:3.2mm;border:1.2px solid var(--ink);border-radius:.6mm;margin-left:0;margin-right:.6mm}
.vote i~i{margin-left:3mm}
.foot{padding:4mm 12mm 12mm;font-size:7.5pt;color:var(--muted)}
"""

doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Construction Product Shortlist</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
<style>{CSS}</style></head><body>
<div class="cover">
  <div class="stripes top"></div>
  <div class="kicker">Product research · GetHookd ad library · {e(REPORT_DATE)}</div>
  <h1>Construction<br>product <em>shortlist</em></h1>
  <p class="lede">Products that make a tradie's or builder's day easier, or that people need to build and fix houses. Every one is advertising right now on Facebook and Instagram in the US, with ads rated 4 to 5 stars, from brands running 100 to 400 active ads. Each card shows the problem it fixes for the buyer and why it could work as a product. Where checked, cards also show who is already selling it through Google Ads in Australia. Tap any card to watch the ad or open the product page, and tick Good, Maybe or No.</p>
  <div class="stats">
    <div class="stat"><b>{n_total}</b><span>Products</span></div>
    <div class="stat"><b>{n_new}</b><span>Not yet checked</span></div>
    <div class="stat"><b>{longest}</b><span>Longest ad (days)</span></div>
  </div>
  <ul class="toc">{toc}</ul>
  <div class="howto">
    <div class="k-new"><b>Not yet checked</b>Fresh lead. Australian shelves and margins still to check.</div>
    <div class="k-maybe"><b>Maybe</b>Passed some checks. Has a catch, noted on the card.</div>
    <div class="k-ref"><b>Reference</b>Shown for comparison, such as ratchet straps.</div>
    <div class="k-skip"><b>Skip</b>Already cheap in Australia or blocked. Reason on the card.</div>
  </div>
  <div class="stripes bot"></div>
</div>
{sections}
<div class="foot">Ad run times and ratings are from GetHookd on the date above. "Watch the ad" opens GetHookd's public ad preview. Skip and Maybe notes come from checks of Bunnings, Kmart, Amazon AU, eBay AU, Australian online stores and website traffic estimates.</div>
</body></html>'''
open(OUT_HTML, "w").write(doc)
print("wrote", OUT_HTML, len(doc) // 1024, "KB,", n_total, "products")
