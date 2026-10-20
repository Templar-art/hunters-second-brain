#!/usr/bin/env python3
"""gen-runner — one runner for every 10x generation batch (Job Framework v2, phase 1).

  estimate <jobs.json>              free: `higgsfield generate cost` per row -> table + total,
                                     saved to <jobs>.estimate.json
  run <jobs.json> [--only a,b]      SPENDS: needs a fresh estimate (<2 h) within the job cap.
                                     Runs up to 8 in parallel, retries transient errors,
                                     downloads outputs, appends one ledger line per success to
                                     JOB.md, re-tallies the header, writes a QC contact sheet.
                                     Gated by the money-gate hook (needs Hunter's go).
  log <JOB.md> <amount> <hf|cr|aud> <note...>
                                     add a ledger line by hand (e.g. Magnific MCP spends)
  tally <JOB.md>                    rewrite the JOB.md `cost:` header from the ledger
  sheet <out.jpg> <files...>        QC contact sheet: images as-is, videos as 5 frames
                                     (0/25/50/75/100 %)
  qc <videos...> [--json out.json]  automatic flags: NO_MOTION, MORPH/DISSOLVE@t (qc_video.py);
                                     `run` applies them to every video it downloads

jobs.json (paths relative to the file):
  {"job_md": "JOB.md", "cap_hf": 150,
   "defaults": {"model": "veo3_1", "params": {"variant": "veo-3-1-fast", "quality": "high"}},
   "rows": [{"id": "06_track", "params": {"start-image": "hero/06.png"},
             "prompt": "…", "out": "video/06_track.mp4"}]}
Row keys override defaults; params merge. Rows whose `out` already exists are skipped by run.

JOB.md ledger: a `## Ledger` section of lines `- 2026-10-20 | 32 hf | note`. The header
`cost:` line is derived from it and never edited by hand.
"""
import argparse, concurrent.futures as cf, json, os, re, subprocess, sys, tempfile, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HF = os.environ.get("GEN_RUNNER_HF_BIN", "higgsfield")
ESTIMATE_TTL = 2 * 3600
PARALLEL = 8
RETRIES = 3
TRANSIENT = ("no response", "520", "502", "503", "504", "PUT media", "timeout", "timed out",
             "connection reset", "temporarily", "rate limit")
UNITS = {"hf": "hf_credits", "cr": "credits", "aud": "aud"}
LEDGER_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) \| ([\d.]+) (hf|cr|aud) \| (.*)$")
URL_RE = re.compile(r"https?://[^\s\"'<>]+")
MEDIA_EXT = (".mp4", ".mov", ".webm", ".png", ".jpg", ".jpeg", ".webp")


# ---------- jobs.json ----------

def load_jobs(path):
    path = Path(path).resolve()
    spec = json.loads(path.read_text())
    base = path.parent
    d = spec.get("defaults", {})
    rows = []
    for r in spec["rows"]:
        row = {**d, **r, "params": {**d.get("params", {}), **r.get("params", {})}}
        for k in ("id", "model", "prompt", "out"):
            if not row.get(k):
                sys.exit(f"row {r.get('id', '?')}: missing '{k}'")
        rows.append(row)
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate row ids")
    return spec, rows, base


def hf_args(row):
    args = [row["model"]]
    for k, v in row["params"].items():
        args += [f"--{k}", str(v).lower() if isinstance(v, bool) else str(v)]
    return args + ["--prompt", row["prompt"]]


# ---------- estimate ----------

def cost_of(row, base):
    r = subprocess.run([HF, "generate", "cost", *hf_args(row), "--json"], cwd=base,
                       capture_output=True, text=True, timeout=300)
    try:
        return float(json.loads(r.stdout)["credits"])
    except Exception:
        raise SystemExit(f"cost failed for {row['id']}: {(r.stdout + r.stderr).strip()[-300:]}")


def cmd_estimate(a):
    spec, rows, base = load_jobs(a.jobs)
    with cf.ThreadPoolExecutor(PARALLEL) as ex:
        costs = dict(zip([r["id"] for r in rows], ex.map(lambda r: cost_of(r, base), rows)))
    pending = [r for r in rows if not (base / r["out"]).exists()]
    total = sum(costs[r["id"]] for r in pending)
    print(f"{'id':24} {'model':18} {'hf':>7}  status")
    for r in rows:
        done = (base / r["out"]).exists()
        print(f"{r['id']:24} {r['model']:18} {costs[r['id']]:7g}  {'done (skip)' if done else 'to run'}")
    cap = spec.get("cap_hf")
    print(f"\nTOTAL to run: {total:g} HF across {len(pending)} rows" + (f"  (cap {cap:g})" if cap else ""))
    if cap and total > cap:
        print("⚠️  over the job cap — run will refuse")
    est = {"at": time.time(), "costs": costs, "total_pending": total}
    Path(str(Path(a.jobs).resolve()) + ".estimate.json").write_text(json.dumps(est, indent=1))


# ---------- run ----------

def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    urllib.request.urlretrieve(url, tmp)
    tmp.rename(dest)


def run_row(row, base):
    cmd = [HF, "generate", "create", *hf_args(row), "--wait"]
    out = ""
    for attempt in range(1, RETRIES + 1):
        r = subprocess.run(cmd, cwd=base, capture_output=True, text=True, timeout=3600)
        out = r.stdout + r.stderr
        urls = [u.rstrip(").,") for u in URL_RE.findall(out)]
        media = [u for u in urls if u.split("?")[0].lower().endswith(MEDIA_EXT)] or urls
        if r.returncode == 0 and media:
            download(media[-1], base / row["out"])
            return row["id"], True, media[-1]
        if not any(t.lower() in out.lower() for t in TRANSIENT):
            break
        time.sleep(5 * attempt)
    return row["id"], False, out.strip()[-400:]


def cmd_run(a):
    spec, rows, base = load_jobs(a.jobs)
    est_path = Path(str(Path(a.jobs).resolve()) + ".estimate.json")
    if not est_path.exists() or time.time() - json.loads(est_path.read_text())["at"] > ESTIMATE_TTL:
        sys.exit("refusing: no estimate in the last 2 h — run `estimate` and quote it to Hunter first")
    costs = json.loads(est_path.read_text())["costs"]
    only = set(a.only.split(",")) if a.only else None
    todo = [r for r in rows if not (base / r["out"]).exists() and (not only or r["id"] in only)]
    if not todo:
        return print("nothing to run (all outputs exist)")
    missing = [r["id"] for r in todo if r["id"] not in costs]
    if missing:
        sys.exit(f"refusing: rows not in the estimate: {missing} — re-run estimate")
    total = sum(costs[r["id"]] for r in todo)
    cap = spec.get("cap_hf")
    if cap and total > cap:
        sys.exit(f"refusing: {total:g} HF exceeds the job cap {cap:g}")
    job_md = base / spec.get("job_md", "JOB.md")
    print(f"running {len(todo)} rows, est {total:g} HF")
    ok_files, fails = [], []
    with cf.ThreadPoolExecutor(PARALLEL) as ex:
        for rid, ok, info in ex.map(lambda r: run_row(r, base), todo):
            row = next(r for r in todo if r["id"] == rid)
            if ok:
                ok_files.append(base / row["out"])
                if job_md.exists():
                    ledger_add(job_md, costs[rid], "hf", f"{rid} {row['model']} (gen-runner)")
                print(f"OK   {rid} -> {row['out']}")
            else:
                fails.append(rid)
                print(f"FAIL {rid}: {info}")
    if job_md.exists():
        tally(job_md)
    if ok_files:
        stamp = f"{datetime.now():%Y%m%d-%H%M}"
        flags = qc_videos([f for f in ok_files if f.suffix.lower() in VIDEO_EXT], base / f"qc-{stamp}.json")
        sheet_path = base / f"qc-{stamp}.jpg"
        make_sheet(sheet_path, ok_files, flags)
        print(f"QC sheet: {sheet_path}")
    if fails:
        print(f"{len(fails)} failed (not charged in ledger): {', '.join(fails)}")
        sys.exit(1)


# ---------- ledger / tally ----------

def ledger_add(job_md, amount, unit, note):
    text = Path(job_md).read_text()
    line = f"- {datetime.now(timezone.utc).astimezone():%Y-%m-%d} | {float(amount):g} {unit} | {note}"
    if "\n## Ledger" not in text:
        marker = "\n---\n_Vault:"
        block = "\n## Ledger\n\n<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->\n"
        text = text.replace(marker, block + marker, 1) if marker in text else text.rstrip("\n") + "\n" + block
    head, _, tail = text.partition("\n## Ledger")
    sec_end = tail.find("\n## ", 1)
    sec, rest = (tail, "") if sec_end == -1 else (tail[:sec_end], tail[sec_end:])
    foot = ""
    if "\n---\n_Vault:" in sec:
        sec, f = sec.split("\n---\n_Vault:", 1)
        foot = "\n---\n_Vault:" + f
    sec = sec.rstrip("\n") + "\n" + line + "\n"
    Path(job_md).write_text(head + "\n## Ledger" + sec + foot + rest)


def tally(job_md):
    text = Path(job_md).read_text()
    sums = {u: 0.0 for u in UNITS}
    _, _, tail = text.partition("\n## Ledger")
    for ln in tail.splitlines():
        m = LEDGER_RE.match(ln.strip())
        if m:
            sums[m.group(3)] += float(m.group(2))
    cost = "cost: { " + ", ".join(f"{UNITS[u]}: {sums[u]:g}" for u in ("cr", "hf", "aud")) + " }"
    new, n = re.subn(r"^cost:.*$", cost + "   # derived from ## Ledger", text, count=1, flags=re.M)
    if n == 0:
        sys.exit(f"{job_md}: no 'cost:' line in header")
    Path(job_md).write_text(new)
    return sums


def cmd_log(a):
    if a.unit not in UNITS:
        sys.exit(f"unit must be one of {list(UNITS)}")
    ledger_add(a.job_md, a.amount, a.unit, " ".join(a.note))
    print(tally(a.job_md))


def cmd_tally(a):
    print(tally(a.job_md))


# ---------- contact sheet ----------

VIDEO_EXT = (".mp4", ".mov", ".webm")


def qc_videos(files, json_out=None):
    """Run the automatic video checks; print a table; return {path: [flags]}."""
    if not files:
        return {}
    sys.path.insert(0, str(Path(__file__).parent))
    import qc_video
    results = [qc_video.analyse(f) for f in files]
    print(f"{'video':28} {'motion':>7} {'contin.':>7}  flags")
    for r in results:
        print(f"{Path(r['file']).name:28} {r.get('motion', 0):7.3f} {r.get('continuity_min', 0):7.2f}  {', '.join(r['flags']) or 'ok'}")
    if json_out:
        Path(json_out).write_text(json.dumps(results, indent=1))
    return {str(Path(r["file"])): r["flags"] for r in results}


def cmd_qc(a):
    flags = qc_videos([Path(f) for f in a.files], a.json)
    if a.sheet:
        make_sheet(a.sheet, a.files, flags)
        print(a.sheet)


def video_frames(path, n=5):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip() or 0)
    frames = []
    with tempfile.TemporaryDirectory() as td:
        for i in range(n):
            t = max(0.0, min(dur - 0.05, dur * i / (n - 1))) if dur else 0
            f = Path(td) / f"{i}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(path),
                            "-frames:v", "1", "-vf", "scale=480:-2", str(f)])
            if f.exists():
                from PIL import Image
                frames.append(Image.open(f).convert("RGB").copy())
    return frames


def make_sheet(out, files, flags=None):
    from PIL import Image, ImageDraw, ImageFont
    W, LABEL = 480, 40
    font = ImageFont.load_default(size=22)
    strips = []
    for f in files:
        f = Path(f)
        if f.suffix.lower() in VIDEO_EXT:
            imgs = video_frames(f)
        else:
            im = Image.open(f).convert("RGB")
            imgs = [im.resize((W, max(1, int(im.height * W / im.width))))]
        if not imgs:
            continue
        h = max(i.height for i in imgs)
        strip = Image.new("RGB", (W * 5, h + LABEL), "white")
        fl = (flags or {}).get(str(f), [])
        bad = [x for x in fl if not x.startswith("WARN")]
        label = f.name + (f"   >> {' · '.join(fl)}" if fl else "")
        ImageDraw.Draw(strip).text((10, 8), label, fill="red" if bad else ("darkorange" if fl else "black"), font=font)
        for i, im in enumerate(imgs):
            strip.paste(im, (i * W, LABEL))
        strips.append(strip)
    if not strips:
        return
    sheet = Image.new("RGB", (W * 5, sum(s.height for s in strips)), "white")
    y = 0
    for s in strips:
        sheet.paste(s, (0, y))
        y += s.height
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=85)


def cmd_sheet(a):
    make_sheet(a.out, a.files)
    print(a.out)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("estimate"); s.add_argument("jobs"); s.set_defaults(f=cmd_estimate)
    s = sp.add_parser("run"); s.add_argument("jobs"); s.add_argument("--only"); s.set_defaults(f=cmd_run)
    s = sp.add_parser("log"); s.add_argument("job_md"); s.add_argument("amount", type=float)
    s.add_argument("unit"); s.add_argument("note", nargs="+"); s.set_defaults(f=cmd_log)
    s = sp.add_parser("tally"); s.add_argument("job_md"); s.set_defaults(f=cmd_tally)
    s = sp.add_parser("sheet"); s.add_argument("out"); s.add_argument("files", nargs="+"); s.set_defaults(f=cmd_sheet)
    s = sp.add_parser("qc"); s.add_argument("files", nargs="+"); s.add_argument("--json"); s.add_argument("--sheet")
    s.set_defaults(f=cmd_qc)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
