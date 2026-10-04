"""One-off patch: add the "For you" fit line to the PDF builder and the web page, and merge for_him.json into rows."""
import json
import os
import re

P = os.path.dirname(os.path.abspath(__file__))

p = os.path.join(P, "build_pdf.py")
s = open(p).read()
if "class=\"him\"" not in s:
    s = s.replace(
        '''    note = f'<p class="note">{e(r["note"])}</p>' if r.get("note") else ""''',
        '''    note = f'<p class="note">{e(r["note"])}</p>' if r.get("note") else ""
    him = f'<p class="him"><b>For you</b>{e(r["for_him"])}</p>' if r.get("for_him") else ""''')
    s = s.replace(
        '''    <p class="fix"><b>Fixes</b>{e(r["problem"])}</p>
    {note}''',
        '''    <p class="fix"><b>Fixes</b>{e(r["problem"])}</p>
    {him}
    {note}''')
    s = s.replace(
        ".note{margin:0;",
        ".him{margin:0;font-size:8.3pt;background:#f1efe8;padding:1.6mm 2mm;border-radius:1mm}\n"
        ".him b{display:block;font-family:var(--mono);font-size:6.5pt;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);font-weight:500}\n"
        ".note{margin:0;")
    s = s.replace(
        "Tap any card to watch the ad or open the product page.",
        "Each card shows the problem it fixes for the buyer, and what it means for your business. Tap any card to watch the ad or open the product page.")
    open(p, "w").write(s)

rows = json.load(open(os.path.join(P, "rows_all.json")))
fh = json.load(open(os.path.join(P, "for_him.json")))
for r in rows:
    if r["product"] in fh:
        r["for_him"] = fh[r["product"]]
json.dump(rows, open(os.path.join(P, "rows_all.json"), "w"))

h = os.path.join(P, "construction-shortlist.html")
t = open(h).read()
if 'class="him"' not in t:
    t = t.replace(
        '        ${r.note?`<p class="note">${esc(r.note)}</p>`:""}',
        '        ${r.for_him?`<p class="him"><b>For you</b>${esc(r.for_him)}</p>`:""}\n'
        '        ${r.note?`<p class="note">${esc(r.note)}</p>`:""}')
    t = t.replace(
        ".note{grid-column:1/-1;",
        ".him{grid-column:1/-1;margin:2px 0 0;max-width:72ch;font-size:15px;background:var(--bg);border-radius:4px;padding:8px 10px}\n"
        ".him b{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;margin-right:8px}\n"
        ".note{grid-column:1/-1;")
    t = t.replace("Each card links to the actual ad.", "Each card says what the product fixes for the buyer and what it means for your business, and links to the actual ad.")
t = re.sub(r"const ROWS = \[.*?\];\n", lambda m: "const ROWS = " + json.dumps(rows) + ";\n", t, count=1, flags=re.S)
open(h, "w").write(t)
print("rows with fit line:", sum(1 for r in rows if r.get("for_him")), "of", len(rows))
