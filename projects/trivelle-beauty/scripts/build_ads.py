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
OUT = os.path.join(V, "ads")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
GREEN, SAGE, RED = (29, 42, 38), (225, 232, 229), (139, 0, 0)
MUSIC = os.path.expanduser("~/Desktop/Ocular Sounds/MUSCSynth_SYNTH-Off Shore Loopable D_Ocular_Pendulum_90 bpm.wav")


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:]); raise SystemExit(1)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())


def words(name):
    d = json.load(open(os.path.join(ASR, name + ".json")))
    out = []
    for s in d["transcription"]:
        t = s["text"].strip()
        if not t:
            continue
        out.append((s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, t))
    return out


FIX = {"trivial": "Trivelle", "Trivial": "Trivelle", "Travelle": "Trivelle", "travelle": "Trivelle",
       "gwasha": "gua sha", "ENS": "EMS", "overpaying": "over paying", "you're checking": "you check in",
       "Glide Gel": "Glide Gel", "glide gel": "Glide Gel"}


def chunks(ws, offset=0.0, n=3):
    """Group words into caption chunks; break on punctuation."""
    res, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= n or w[2][-1] in ".,!?":
            res.append((cur[0][0] + offset, cur[-1][1] + offset, " ".join(x[2] for x in cur)))
            cur = []
    if cur:
        res.append((cur[0][0] + offset, cur[-1][1] + offset, " ".join(x[2] for x in cur)))
    # hold each chunk until the next starts
    fixed = []
    for i, (a, b, t) in enumerate(res):
        nb = res[i + 1][0] if i + 1 < len(res) else b + 0.3
        for k, v in FIX.items():
            t = t.replace(k, v)
        fixed.append((a, max(b, nb), t))
    return fixed


def font(size, display=True):
    if display:
        return ImageFont.truetype(os.path.join(FONTS, "Anton-Regular.ttf"), size)
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat.ttf"), size)
    try:
        f.set_variation_by_name("SemiBold")
    except Exception:
        pass
    return f


def caption_track(caps, total, path):
    """Render captions as a PNG-sequence alpha video at 10 fps."""
    fdir = path + "_frames"
    os.makedirs(fdir, exist_ok=True)
    f = font(78)
    blank = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cache = {}
    n = int(total * 10) + 1
    for i in range(n):
        t = i / 10
        txt = next((c[2] for c in caps if c[0] <= t < c[1]), None)
        if txt not in cache:
            if txt is None:
                cache[txt] = blank
            else:
                im = blank.copy(); d = ImageDraw.Draw(im)
                s = txt.upper()
                bw = d.textlength(s, font=f)
                while bw > W - 140 and f.size > 40:
                    f = font(f.size - 4); bw = d.textlength(s, font=f)
                x, y = (W - bw) / 2, int(H * 0.68)
                d.text((x, y), s, font=f, fill="white", stroke_width=7, stroke_fill=(0, 0, 0))
                cache[txt] = im
                f = font(78)
        cache[txt].save(os.path.join(fdir, f"{i:05d}.png"))
    sh(["ffmpeg", "-v", "error", "-y", "-framerate", "10", "-i", os.path.join(fdir, "%05d.png"),
        "-c:v", "qtrle", path])


def end_card(path, seconds=4):
    im = Image.new("RGB", (W, H), GREEN)
    hero = Image.open(os.path.join(ROOT, "stills", "01-hero-final.png")).convert("RGB").resize((1000, 1000))
    im.paste(hero, (40, 300))
    d = ImageDraw.Draw(im)
    def ctr(txt, y, f, fill):
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=fill)
    ctr("TRIVELLE", 110, font(130), "white")
    ctr("THREE RITUALS. ONE DEVICE.", 1370, font(72), "white")
    ctr("$169 AUD  ·  under $1 a session", 1490, font(50, False), SAGE)
    ctr("30-day money-back guarantee", 1570, font(50, False), SAGE)
    ctr("Free shipping Australia-wide", 1650, font(50, False), SAGE)
    d.rounded_rectangle((290, 1750, 790, 1850), 50, fill=RED)
    ctr("SHOP NOW", 1768, font(60), "white")
    png = path.replace(".mp4", ".png"); im.save(png)
    sh(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", png, "-t", str(seconds), "-vf",
        f"scale={W}:{H},zoompan=z='1+0.0006*on':d={seconds*FPS}:s={W}x{H}:fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-crf", "18", path])


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
        d = dur(src)
        speed = min(1.0, d / length)  # slow down slightly if the slot is longer than the clip
        vf = (f"setpts=PTS/{speed:.4f},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"fps={FPS},format=yuv420p")
        sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-t", f"{length:.3f}", "-vf", vf,
            "-c:v", "libx264", "-crf", "18", "-an", dst])


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
          f"[3:a]volume=0.12,afade=t=in:d=1,afade=t=out:st={total-2}:d=2[mu]"]
    mix = "[vo][mu]"; k = 2
    if hook:
        inputs += ["-i", hook]
        fc.append("[4:a]volume=1.0[hk]"); mix += "[hk]"; k = 3
    fc.append(f"{mix}amix=inputs={k}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    out = os.path.join(OUT, f"{name}.mp4")
    sh(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
        "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
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
UGC = os.path.join(V, "ugc-01-salon-48.mp4")
END = os.path.join(WORK, "endcard.mp4"); end_card(END)


def fill(clips, span):
    """Split span seconds evenly across clips."""
    each = span / len(clips)
    return [(c, each, c.endswith(".png") or c.endswith(".jpg")) for c in clips]


def first_word(ws, word):
    return next(w[0] for w in ws if w[2].lower().startswith(("trivelle", "travelle", "trivial")))


PRODUCT = [B("d1-hero"), B("d2-stomach"), S("stills/roster/r5-middleeastern-50s-arm.png"), B("d4-arm"),
           S("graphics/01-feature-panel.jpg"), B("d3-thigh"), S("stills/roster/r8-black-50s-lifestyle.png"),
           S("graphics/02-how-to-use.jpg")]

results = {}

# ---- Ad A: UGC hook (10s) + VO1 salon cost + end card
w1 = words("vo1-salon-cost"); d1 = dur(os.path.join(V, "vo", "vo1-salon-cost.mp3"))
hook = dur(UGC)
split = first_word(w1, "Trivelle") - 0.1
seqA = [(UGC, hook, False)] + fill([B("p06-salon-wait"), B("p05-phone-bill")], split) \
     + fill(PRODUCT, d1 - split) + [(END, 4, False)]
totalA = hook + d1 + 4
capsA = chunks(words("ugc")) + chunks(w1, hook)
results["A"] = build("trivelle-A-salon-60s", seqA, os.path.join(V, "vo", "vo1-salon-cost.mp3"), capsA, totalA, hook, hook=UGC)

# ---- Ad B: VO2 lived-a-little, pain montage → product → UGC → end card
w2 = words("vo2-lived-a-little"); d2 = dur(os.path.join(V, "vo", "vo2-lived-a-little.mp3"))
split = first_word(w2, "Trivelle") - 0.1
seqB = fill([B("p01-jawline"), B("p02-arm-pinch"), B("p03-shorts-skirt"), B("p08-cardigan"), B("p11-brunch-sleeve")], split) \
     + fill(PRODUCT[:6] + [B("p12-relief-sofa")], d2 - split) + [(END, 4, False)]
totalB = d2 + 4
results["B"] = build("trivelle-B-lived-a-little-50s", seqB, os.path.join(V, "vo", "vo2-lived-a-little.mp3"), chunks(w2), totalB, 0)

# ---- Ad C: VO3 drawer, pain → routine → end card
w3 = words("vo3-drawer"); d3 = dur(os.path.join(V, "vo", "vo3-drawer.mp3"))
split = first_word(w3, "Trivelle") - 0.1
seqC = fill([B("p07-drawer"), B("p09-moisturiser"), B("p04-late-mirror"), B("p10-bed-scroll")], split) \
     + fill([B("d1-hero"), B("d2-stomach"), S("graphics/05-how-it-works.jpg"), B("d4-arm"),
             S("stills/roster/r2-eastasian-40s-arm.png"), B("d3-thigh"), S("graphics/04-in-the-box.jpg"),
             B("p12-relief-sofa")], d3 - split) + [(END, 4, False)]
totalC = d3 + 4
results["C"] = build("trivelle-C-drawer-55s", seqC, os.path.join(V, "vo", "vo3-drawer.mp3"), chunks(w3), totalC, 0)

# ---- Cutdowns: 15s = UGC hook + end card; 30s = first 26s + end card tail
cut(results["A"], "trivelle-A-salon-15s", 0, hook)  # UGC hook alone (talking head with CTA)
for k, v in results.items():
    T = dur(v)
    a = cut(v, f"_tmp_{k}_head", 0, 26)
    tail = cut(v, f"_tmp_{k}_tail", T - 4, 4)
    lst = os.path.join(WORK, f"cut_{k}.txt"); open(lst, "w").write(f"file '{a}'\nfile '{tail}'\n")
    base = os.path.basename(v).rsplit("-", 1)[0]
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
        os.path.join(OUT, f"{base}-30s.mp4")])
    os.remove(a); os.remove(tail)
print("\n".join(sorted(os.listdir(OUT))))
