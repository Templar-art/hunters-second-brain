"""Build Trivelle 60s/30s/15s vertical ads from B-roll + voiceover.

Usage: python3 build_ads.py <asr_dir> <work_dir>
asr_dir holds whisper-cli word-level JSON (<name>.json) for each VO and ugc.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "videos")
FONTS = os.path.join(ROOT, "fonts")
ASR, WORK = sys.argv[1], sys.argv[2]
os.makedirs(WORK, exist_ok=True)
D2 = os.path.join(ROOT, "device-v2")
OUT = os.path.join(D2, "ads")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
GREEN, SAGE, RED, YELLOW = (29, 42, 38), (225, 232, 229), (139, 0, 0), (255, 222, 60)
MUSIC = os.path.join(ROOT, "videos", "music-soft.mp3")


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:]); raise SystemExit(1)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())


SCRIPTS = {
 'ugc': "I'm forty-eight, and I was so over paying for salon treatments. This is Trivelle. Heat, red light, EMS and a vacuum massage, all in one. Ten minutes, a few nights a week. My skin just looks fresher. And there's a thirty-day money-back guarantee.",
 'vo1-salon-cost': "Salon body treatments add up fast. A hundred dollars here, a hundred and fifty there, and the waitlist never ends. So we made Trivelle. Heat, red light, EMS and a vacuum massage, in one cordless device you use at home. Smooth on the gel, pick a mode on the screen, and glide. About ten minutes, three to five times a week. Gentle heat for a warm, relaxing feel. Red light for a radiant-looking glow. EMS micro-pulses for a toned, firmer feel. And vacuum massage for skin that looks smoother. Face, arms, stomach, thighs. It's about the cost of one salon treatment, and under a dollar a session. Free shipping Australia-wide, and a thirty-day money-back guarantee. Trivelle. Four rituals. One device.",
 'vo2-lived-a-little': "If your skin has lived a little, this one's for you. The arms you keep covered. The jawline you check in every mirror. The shorts that stay in the drawer. Trivelle is a cordless at-home device that brings four salon rituals together. Gentle heat for a warm, relaxing feel. Red light for a radiant-looking glow. EMS micro-pulses for a toned, firmer feel. And a vacuum massage for skin that looks smoother. Ten minutes, a few nights a week. It feels like a warm massage with a gentle tingle. Free shipping Australia-wide, and thirty days to try it. If you don't love it, send it back. Trivelle. Made for skin that's lived a little.",
 'vo3-drawer': "Jade rollers. Gua sha stones. Creams that promised everything. Most of them end up in the bathroom drawer. Trivelle is different, because it does four things at once. Gentle heat for a warm, relaxing feel. Red light for a radiant-looking glow. EMS micro-pulses for a toned, firmer feel. And a vacuum massage that leaves skin looking smoother. Here's the routine. A thin layer of gel. Choose your mode on the screen. Slow upward strokes, about ten minutes. Three to five times a week. That's it. Cordless, rechargeable, and it fits in your hand. Under a dollar a session, with a thirty-day money-back guarantee and free shipping Australia-wide. Clear out the drawer. Trivelle. Four rituals. One device.",
 'seated': "Okay, so a few of you asked what this is. It's called Trivelle, and it does four things in one. Gentle heat, so it feels like a warm massage. Red light, for that glowy, radiant look. EMS, which feels like tiny little pulses, for a toned, firmer feel. And a vacuum massage through this head here, for skin that looks smoother. There's a little screen so you can see your mode and level. I just pop on some gel and do about ten minutes, a few nights a week, while I watch telly. And there's a thirty-day money-back guarantee, so you can try it yourself.",
}
SCRIPTS['ugc2'] = SCRIPTS['ugc']


def _norm(t):
    import re
    t = t.lower().replace("-", " ")
    return re.sub(r"[^a-z0-9 ]", "", t)


NUM = {"trivel": "trivelle", "trivone": "trivelle", "trevolz": "trivelle", "trevelle": "trivelle", "48": "fortyeight", "10": "ten", "30": "thirty", "100": "hundred", "150": "hundredfifty", "169": "onehundredsixtynine"}


def words(name):
    """Exact script words, each timed to the moment it is spoken: script tokens are
    aligned to whisper word tokens (difflib); matched words take whisper's own
    timing, unmatched ones are interpolated between their matched neighbours."""
    import difflib
    d = json.load(open(os.path.join(ASR, name + ".json")))
    asr = [(s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, s["text"].strip())
           for s in d["transcription"] if s["text"].strip()]
    script = SCRIPTS[name].split()
    sa = [_norm(w).replace(" ", "") for w in script]
    aa = [NUM.get(_norm(w[2]).replace(" ", ""), _norm(w[2]).replace(" ", "")) for w in asr]
    times = [None] * len(script)
    sm = difflib.SequenceMatcher(None, sa, aa, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                times[i1 + k] = (asr[j1 + k][0], asr[j1 + k][1])
        elif tag == "replace" and j2 > j1:
            # spread the replaced script words across the replaced asr span
            t0, t1 = asr[j1][0], asr[j2 - 1][1]
            n = i2 - i1
            for k in range(n):
                times[i1 + k] = (t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n)
    # interpolate any gaps
    for i in range(len(script)):
        if times[i] is None:
            prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
            nxt = next((times[j][0] for j in range(i + 1, len(script)) if times[j]), prev + 0.3)
            times[i] = (prev, max(prev + 0.05, nxt))
    return [(a, b, w) for (a, b), w in zip(times, script)]


def chunks(ws, offset=0.0, n=3):
    """Group words into caption chunks (<=3 words, <=22 chars); break on punctuation.
    Each chunk keeps its words for the per-word highlight."""
    res, cur = [], []
    def push():
        ww = [(a + offset, b + offset, t) for a, b, t in cur]
        res.append([ww[0][0], ww[-1][1], " ".join(x[2] for x in ww), ww])
    for w in ws:
        if cur and len(" ".join(x[2] for x in cur + [w])) > 22:
            push(); cur = []
        cur.append(w)
        if len(cur) >= n or w[2][-1] in ".,!?":
            push(); cur = []
    if cur:
        push()
    for i, c in enumerate(res):
        nb = res[i + 1][0] if i + 1 < len(res) else c[1] + 0.3
        c[1] = max(c[1], nb)
    return [tuple(c) for c in res]


def font(size, display=True):
    if display:
        return ImageFont.truetype(os.path.join(FONTS, "Anton-Regular.ttf"), size)
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat.ttf"), size)
    try:
        f.set_variation_by_name("SemiBold")
    except Exception:
        pass
    return f


def cap_font(size):
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat.ttf"), size)
    try:
        f.set_variation_by_name("ExtraBold")
    except Exception:
        try: f.set_variation_by_name("Bold")
        except Exception: pass
    return f


def caption_track(caps, total, path):
    """Premium karaoke captions: white rounded box, black text, the word being
    spoken gets a brand-red pill with white text. Rendered at 15 fps alpha."""
    fdir = path + "_frames"
    os.makedirs(fdir, exist_ok=True)
    f = cap_font(62)
    blank = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cache = {}
    n = int(total * 15) + 1
    for i in range(n):
        t = i / 15
        cap = next((c for c in caps if c[0] <= t < c[1]), None)
        key = None
        if cap:
            ws = cap[3]
            act = max([k for k, w in enumerate(ws) if w[0] <= t] or [0])
            key = (cap[2], act)
        if key not in cache:
            if key is None:
                cache[key] = blank
            else:
                im = blank.copy(); d = ImageDraw.Draw(im)
                toks = [w[2].upper() for w in ws]
                sp = d.textlength(" ", font=f)
                widths = [d.textlength(tk, font=f) for tk in toks]
                padx, pady, gap = 34, 24, sp
                tw = sum(widths) + gap * (len(toks) - 1)
                asc, desc = f.getmetrics(); th = asc + desc
                bx0 = (W - tw) / 2 - padx; by0 = int(H * 0.70)
                d.rounded_rectangle((bx0, by0, bx0 + tw + 2 * padx, by0 + th + 2 * pady), 26, fill=(255, 255, 255, 245))
                x = bx0 + padx; y = by0 + pady
                for k, tk in enumerate(toks):
                    if k == act:
                        d.rounded_rectangle((x - 12, y - 6, x + widths[k] + 12, y + th + 4), 14, fill=YELLOW)
                        d.text((x, y), tk, font=f, fill=(15, 15, 15))
                    else:
                        d.text((x, y), tk, font=f, fill=(15, 15, 15))
                    x += widths[k] + gap
                cache[key] = im
        cache[key].save(os.path.join(fdir, f"{i:05d}.png"))
    sh(["ffmpeg", "-v", "error", "-y", "-framerate", "15", "-i", os.path.join(fdir, "%05d.png"),
        "-c:v", "qtrle", path])


def end_card(path, seconds=3.5):
    """Animated hero clip with a light text overlay. No button: a soft spoken-style CTA."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    # soft fade at the bottom so the type reads on the white bench
    for y in range(H - 620, H):
        a = int(170 * (y - (H - 620)) / 620)
        d.line([(0, y), (W, y)], fill=(29, 42, 38, a))
    def ctr(txt, y, f, fill):
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=fill)
    ctr("TRIVELLE", 1440, font(110), "white")
    ctr("4-in-1  ·  30-day money-back guarantee", 1585, cap_font(44), "white")
    ctr("Tap below to try it", 1665, cap_font(44), YELLOW)
    png = path.replace(".mp4", ".png"); ov.save(png)
    src = os.path.join(ROOT, "device-v2", "stills", "01-hero-v2-pilot.png")
    fr = int(seconds * FPS)
    sh(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-i", png, "-t", str(seconds), "-filter_complex",
        f"[0:v]scale=-2:{H*2}:flags=lanczos,crop={W*2}:{H*2}:iw*0.12:0,zoompan=z='1.0+0.0007*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s={W}x{H}:fps={FPS}[b];"
        f"[b][1:v]overlay=0:0,fade=t=in:d=0.25,format=yuv420p",
        "-c:v", "libx264", "-crf", "16", "-an", path])


def norm(src, dst, length, still=False):
    """Conform a clip or still to W x H, FPS, exact length, silent."""
    if still and src.endswith(".jpg"):  # square graphic: fit whole, on brand green, slow push
        frames = int(length * FPS)
        vf = (f"scale={W}:-2,pad={W}:{H}:0:(oh-ih)/2:color=0x1D2A26,scale={W*2}:{H*2},"
              f"zoompan=z='1.0+0.0004*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p")
        sh(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-t", f"{length:.3f}", "-vf", vf,
            "-c:v", "libx264", "-crf", "18", "-an", dst])
        return
    if still:
        frames = int(length * FPS)
        vf = (f"scale=-2:{H*2},crop={W*2}:{H*2},zoompan=z='1.0+0.0008*on':x='iw/2-(iw/zoom/2)':"
              f"y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p")
        sh(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-t", f"{length:.3f}", "-vf", vf,
            "-c:v", "libx264", "-crf", "18", "-an", dst])
    else:
        ss = 0.0 if src.endswith(("ugc-01-salon-48.mp4",)) or "/stock/" in src else 0.25
        if "#ss=" in src:
            src, off = src.split("#ss="); ss = float(off)
        d = dur(src) - ss if "#" not in src else 99
        speed = max(0.8, min(1.0, d / length))  # gentle slow-down only, never below 80%
        sharp = "" if "/stock/" in src else "unsharp=5:5:0.6:3:3:0.0,"
        vf = (f"setpts=PTS/{speed:.4f},scale={W}:{H}:flags=lanczos:force_original_aspect_ratio=increase,"
              f"crop={W}:{H},{sharp}fps={FPS},format=yuv420p")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.2f}", "-i", src, "-t", f"{length:.3f}", "-vf", vf,
            "-c:v", "libx264", "-crf", "16", "-an", dst])


def build(name, seq, vo, caps, total, vo_offset, hook=None):
    """seq: list of (src, seconds, is_still). hook: ugc clip played first with its own audio."""
    parts = []
    for i, (src, sec, st) in enumerate(seq):
        p = os.path.join(WORK, f"{name}_{i:02d}.mp4"); norm(src, p, sec, st); parts.append(p)
    lst = os.path.join(WORK, f"{name}.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(WORK, f"{name}_v.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid])
    cap = os.path.join(WORK, f"{name}_cap.mov"); caption_track(caps, total, cap)
    # audio: hook audio (if any) + VO at offset + music bed ducked under
    inputs = ["-i", vid, "-i", cap, "-i", vo, "-stream_loop", "-1", "-i", MUSIC]
    fc = [f"[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]",
          f"[2:a]adelay={int(vo_offset*1000)}|{int(vo_offset*1000)},volume=1.0[vo]",
          f"[3:a]volume=0.09,afade=t=in:d=1.5,afade=t=out:st={total-3}:d=3[mu]"]
    mix = "[vo][mu]"; k = 2
    if hook:
        inputs += ["-i", hook]
        fc.append("[4:a]volume=1.0[hk]"); mix += "[hk]"; k = 3
    fc.append(f"{mix}amix=inputs={k}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    out = os.path.join(OUT, f"{name}.mp4")
    sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
        "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "20", "-maxrate", "3.6M", "-bufsize", "7M", "-preset", "slow", "-tune", "film", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", out])
    return out


def cut(src, name, start, length):
    out = os.path.join(OUT, f"{name}.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", src, "-t", f"{length:.3f}",
        "-af", f"afade=t=out:st={length-0.6:.3f}:d=0.6", "-c:v", "libx264", "-crf", "19", "-c:a", "aac",
        "-movflags", "+faststart", out])
    return out


B = lambda n: os.path.join(V, "broll", n + ".mp4")
S = lambda p: os.path.join(ROOT, p)
END = os.path.join(WORK, "endcard.mp4"); end_card(END)


def fill(clips, span, start=0.0, ws=None):
    """Split [start, start+span] across clips, snapping each cut to the nearest
    phrase start (word after punctuation, else any word start) so cuts land on the voice."""
    n = len(clips); end = start + span
    targets = [start + span * k / n for k in range(1, n)]
    cuts = []
    if ws:
        phr = [w[0] for i, w in enumerate(ws) if i and ws[i - 1][2][-1] in ".,!?" and start < w[0] < end]
        anyw = [w[0] for w in ws if start < w[0] < end]
        prev = start
        for t in targets:
            pool = [x for x in phr if abs(x - t) < span / n * 0.45 and x - prev > 2.2] or \
                   [x for x in anyw if abs(x - t) < span / n * 0.45 and x - prev > 2.2]
            c = min(pool, key=lambda x: abs(x - t)) if pool else t
            cuts.append(c); prev = c
    else:
        cuts = targets
    edges = [start] + cuts + [end]
    return [(c, edges[i + 1] - edges[i], c.endswith(".png") or c.endswith(".jpg")) for i, c in enumerate(clips)]


def first_word(ws, word):
    return next(w[0] for w in ws if w[2].lower().startswith("trivelle"))


ST = lambda n: os.path.join(V, "stock", n + ".mp4")
N2 = lambda n: os.path.join(D2, "broll", n + ".mp4")
VO = lambda n: os.path.join(D2, "vo", n + ".mp3")
UGC = os.path.join(D2, "ugc-01-hook-v2.mp4")
results = {}

w1 = words("vo1-salon-cost"); d1 = dur(VO("vo1-salon-cost")); hook = dur(UGC)
split = first_word(w1, "Trivelle") - 0.1
seqA = [(UGC, hook, False)] + fill([B("p06-salon-wait"), B("p05-phone-bill"), ST("s3-mirror-check")], split, 0, w1) \
     + fill([N2("v6-screen-on"), N2("v7-stomach-red"), N2("v3-arm-red"), N2("v1-stomach-glow"), N2("v4-jaw"),
             N2("v2-thigh-back"), N2("v5-thigh-front"), N2("v8-arm-orbit"), B("p12-relief-sofa")], d1 - split, split, w1) + [(END, 3.5, False)]
totalA = hook + d1 + 3.5
results["A"] = build("trivelle-A-salon", seqA, VO("vo1-salon-cost"), chunks(words("ugc2")) + chunks(w1, hook), totalA, hook, hook=UGC)

w2 = words("vo2-lived-a-little"); d2 = dur(VO("vo2-lived-a-little"))
split = first_word(w2, "Trivelle") - 0.1
seqB = fill([B("p02-arm-pinch"), ST("s1-roller-jaw"), B("p03-shorts-skirt"), B("p11-brunch-sleeve")], split, 0, w2) \
     + fill([N2("v6-screen-on"), N2("v1-stomach-glow"), N2("v3-arm-red"), N2("v7-stomach-red"), N2("v5-thigh-front"),
             N2("v4-jaw"), B("p12-relief-sofa")], d2 - split, split, w2) + [(END, 3.5, False)]
results["B"] = build("trivelle-B-lived-a-little", seqB, VO("vo2-lived-a-little"), chunks(w2), d2 + 3.5, 0)

w3 = words("vo3-drawer"); d3 = dur(VO("vo3-drawer"))
split = first_word(w3, "Trivelle") - 0.1
seqC = fill([B("p07-drawer"), ST("s1-roller-jaw"), B("p09-moisturiser")], split, 0, w3) \
     + fill([N2("v6-screen-on"), N2("v7-stomach-red"), N2("v8-arm-orbit"), N2("v1-stomach-glow"), N2("v4-jaw"),
             N2("v2-thigh-back"), N2("v3-arm-red"), N2("v5-thigh-front"), B("p12-relief-sofa")], d3 - split, split, w3) + [(END, 3.5, False)]
results["C"] = build("trivelle-C-drawer", seqC, VO("vo3-drawer"), chunks(w3), d3 + 3.5, 0)

SEAT = os.path.join(D2, "ugc-02-seated-v2.mp4")
if os.path.exists(SEAT):
    wd = words("seated"); ds = dur(SEAT)
    def at(word):
        return next(w[0] for w in wd if _norm(w[2]).startswith(word))
    cuts = [(at("heat"), N2("v1-stomach-glow")), (at("red"), N2("v3-arm-red")), (at("ems"), N2("v7-stomach-red")),
            (at("vacuum"), N2("v2-thigh-back")), (at("screen"), N2("v6-screen-on")), (at("gel"), N2("v5-thigh-front"))]
    seqD, t = [], 0.0
    for i, (c0, clip) in enumerate(cuts):
        c0 = max(t, c0 - 0.15)
        nxt = cuts[i + 1][0] - 0.15 if i + 1 < len(cuts) else ds
        if c0 - t > 0.05:
            seqD.append((SEAT + f"#ss={t:.3f}", c0 - t, False))
        L = min(2.2, nxt - c0)
        seqD.append((clip, L, False)); t = c0 + L
    seqD.append((SEAT + f"#ss={t:.3f}", ds - t, False)); seqD.append((END, 3.5, False))
    results["D"] = build("trivelle-D-seated-explainer", seqD, SEAT, chunks(wd), ds + 3.5, 0)

cut(results["A"], "trivelle-A-hook-10s", 0, hook)
for k, v in results.items():
    T = dur(v)
    a_ = cut(v, f"_tmp_{k}_head", 0, 26)
    tail = cut(v, f"_tmp_{k}_tail", T - 3.5, 3.5)
    lst = os.path.join(WORK, f"cut_{k}.txt"); open(lst, "w").write(f"file '{a_}'\nfile '{tail}'\n")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
        os.path.join(OUT, os.path.basename(v).replace(".mp4", "-30s.mp4"))])
    os.remove(a_); os.remove(tail)
print("\n".join(sorted(os.listdir(OUT))))
