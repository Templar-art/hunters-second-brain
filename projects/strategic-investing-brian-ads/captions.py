"""Resolve renders -> loudness-normalised clean finals + captioned finals.

clean:    loudnorm -14 LUFS / -1 dBTP, video stream copied.
captions: whisper large-v3 word timings on the clean file, words spell-fixed, chunked
          2-4 words (break on punctuation / pauses), burned as ASS (Poppins SemiBold, white,
          soft shadow) at ~70% frame height so it sits on the chest, never the face.
"""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
FONT = ImageFont.truetype(str(Path.home() / "Library/Fonts/Poppins-SemiBold.ttf"), 124)
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "_resolve_renders"
CLEAN = ROOT / "finals_clean"; CAP = ROOT / "finals_captions"; SRT = ROOT / "srt"
for d in (CLEAN, CAP, SRT): d.mkdir(exist_ok=True)
MODEL = Path.home() / ".cache/whisper/ggml-large-v3.bin"
TMP = Path(sys.argv[1])
FIX = {"strategic invest": "Strategic Investing", "strategic investing": "Strategic Investing",
       "lba": "RBA", "nba": "RBA", "rba": "RBA", "cashflow": "cash flow"}

def words(wav):
    j = TMP / (wav.stem + "_w")
    subprocess.run([ "whisper-cli", "-m", str(MODEL), "-f", str(wav), "-l", "en", "-mc", "0", "-ml", "1", "-sow", "-oj", "-of", str(j), "-np"], check=True, capture_output=True)
    out = []
    for s in json.load(open(str(j) + ".json"))["transcription"]:
        t = s["text"].strip()
        if t: out.append([s["offsets"]["from"]/1000, s["offsets"]["to"]/1000, t])
    return out

def fix_text(t):
    for k, v in FIX.items():
        t = re.sub(rf"\b{k}\b", v, t, flags=re.I)
    return t

REF = json.load(open(ROOT / "caption_text.json"))
import difflib
def align(W, ref):
    """put whisper word timings onto the corrected reference words"""
    R = ref.split(); n = lambda t: re.sub(r"[^a-z0-9']", "", t.lower())
    T = [None] * len(R)
    sm = difflib.SequenceMatcher(None, [n(x) for x in R], [n(w[2]) for w in W], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1): T[i1+k] = (W[j1+k][0], W[j1+k][1])
        elif tag == "replace" and j2 > j1:
            a, b = W[j1][0], W[j2-1][1]; m = i2 - i1
            for k in range(m): T[i1+k] = (a + (b-a)*k/m, a + (b-a)*(k+1)/m)
    for i in range(len(R)):  # fill unmatched from neighbours
        if T[i] is None:
            prv = next((T[j][1] for j in range(i-1, -1, -1) if T[j]), 0.0)
            T[i] = (prv, prv + 0.25)
    return [[a, b, r] for (a, b), r in zip(T, R)]

def chunks(W, MAXC=24):
    """one line per caption: break on . ? ! (and , once 2+ words); otherwise fill to ~24 chars,
    but never leave 1-2 orphan words before the next punctuation break"""
    P = lambda t: re.search(r"[.?!,]$", t)
    out, cur = [], []
    for i, w in enumerate(W):
        cur.append(w)
        if re.search(r"[.?!]$", w[2]) or (w[2].endswith(",") and len(cur) >= 2):
            out.append(cur); cur = []; continue
        if i + 1 >= len(W): continue
        nxt_len = len(" ".join(x[2] for x in cur + [W[i+1]]))
        k = i + 1; left = 0
        while k < len(W):
            left += 1
            if P(W[k][2]): break
            k += 1
        if nxt_len > MAXC and left > 2:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return [[c[0][0], c[-1][1], " ".join(x[2] for x in c)] for c in out]

def ts(t, ass=True):
    h, m = int(t//3600), int(t%3600//60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}" if ass else f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s%1)*1000)):03d}"

HDR = """[Script Info]
ScriptType: v4.00+
PlayResX: 2160
PlayResY: 3840
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins SemiBold,128,&H00FFFFFF,&H00FFFFFF,&H64000000,&H8C000000,0,0,0,0,100,100,0,0,1,3,5,2,180,180,1050,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

for mp4 in sorted(SRC.glob("Brian *.mp4")):
    base = mp4.stem
    clean = CLEAN / f"{base} AB clean.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1:LRA=9", "-ar", "48000", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", str(clean)], check=True)
    wav = TMP / (base.replace(" ", "_").replace("'", "") + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clean), "-af", "apad=pad_dur=2", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    jw = TMP / (wav.stem + "_w.json")
    W = [[x['offsets']['from']/1000, x['offsets']['to']/1000, x['text'].strip()] for x in json.load(open(jw))['transcription'] if x['text'].strip()] if jw.exists() else words(wav)
    C = chunks(align(W, REF[base.split()[1]]))
    for k in range(len(C)-1): C[k][1] = min(max(C[k][1], C[k][1]), C[k+1][0] - 0.09)
    ass = TMP / (wav.stem + ".ass")
    ass.write_text(HDR + "".join(f"Dialogue: 0,{ts(a)},{ts(b+0.08)},Cap,,0,0,0,,{t}\n" for a, b, t in C))
    (SRT / f"{base}.srt").write_text("".join(f"{i+1}\n{ts(a,False)} --> {ts(b+0.08,False)}\n{t}\n\n" for i, (a, b, t) in enumerate(C)))
    # this ffmpeg has no libass/drawtext -> PIL caption PNGs overlaid with timed enable
    pngs = []
    for i, (a, b, t) in enumerate(C):
        im = Image.new("RGBA", (2160, 600), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        lines = [t]
        if d.textlength(t, font=FONT) > 1800:  # too wide for safe area -> balanced 2 lines
            ws_ = t.split(); best = min(range(1, len(ws_)), key=lambda k: abs(d.textlength(" ".join(ws_[:k]), font=FONT) - d.textlength(" ".join(ws_[k:]), font=FONT)))
            lines = [" ".join(ws_[:best]), " ".join(ws_[best:])]
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        pos = []
        for li, ln in enumerate(lines):
            x = (2160 - d.textlength(ln, font=FONT)) / 2; y = 200 + li * 175 - (88 if len(lines) == 2 else 0)
            pos.append((x, y, ln)); sd.text((x, y + 8), ln, font=FONT, fill=(0, 0, 0, 150))
        im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), im)
        box = Image.new("RGBA", im.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
        for x, y, ln in pos:  # soft dark pill per line keeps it legible on the gingham shirt
            bb = d.textbbox((x, y), ln, font=FONT)
            bd.rounded_rectangle((bb[0]-44, bb[1]-30, bb[2]+44, bb[3]+30), radius=36, fill=(0, 0, 0, 130))
        im = Image.alpha_composite(box, im); d = ImageDraw.Draw(im)
        for x, y, ln in pos:
            d.text((x, y), ln, font=FONT, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 90))
        pth = TMP / f"{wav.stem}_{i:02d}.png"; im.save(pth); pngs.append((pth, a, b + 0.08))
    args = ["ffmpeg", "-v", "error", "-y", "-i", str(clean)]
    for pth, _, _ in pngs: args += ["-i", str(pth)]
    fc, last = "", "0:v"
    for i, (_, a, b) in enumerate(pngs):
        fc += f"[{last}][{i+1}:v]overlay=0:2500:enable='between(t,{a:.3f},{b:.3f})'[o{i}];"; last = f"o{i}"
    subprocess.run(args + ["-filter_complex", fc.rstrip(";"), "-map", f"[{last}]", "-map", "0:a", "-c:v", "libx264", "-b:v", "45M", "-maxrate", "60M", "-bufsize", "90M", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(CAP / f"{base} AB captions.mp4")], check=True)
    print("ok", base, " | ".join(c[2] for c in C))
