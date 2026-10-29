"""Polish a phone-recorded agent VO: tighten pauses, then a voice chain for a clearer, more confident read.

  python3 tools/vo_polish.py VO.m4a WORDS.json OUT.wav [--end 62.85] [--tempo 1.04]

1. Denoise first (HPF 90 + afftdn tracking the noise floor; Katrina's take sat only 31 dB over its noise).
2. Pauses from Whisper word timestamps, cut inside the quietest run of each gap with 20 ms equal-power crossfades:
   after a full stop -> 0.40 s, after a comma -> 0.24 s, any other gap -> 0.18 s. Lead-in trimmed to 0.12 s.
3. Voice chain, from her measured spectrum (120-500 Hz +4..+7 dB over the mids, 1-4 kHz down 10-16 dB, nothing over 12 kHz):
   cut the box (300 Hz), trim the boom (160 Hz), lift upper mids + presence (1.6, 3, 5 kHz), a light exciter for air,
   de-ess, 3:1 compression for an even, forward read, a soft gate so the pauses stay clean, then a 4% faster pace (pitch unchanged) and -16 LUFS.
"""
import argparse, json, subprocess
import numpy as np, soundfile as sf

SR = 48000
ap = argparse.ArgumentParser()
ap.add_argument("vo"); ap.add_argument("words"); ap.add_argument("out")
ap.add_argument("--end", type=float, default=62.85)
ap.add_argument("--tempo", type=float, default=1.04)
a = ap.parse_args()


def ff(x, af):
    """Run mono float audio through an ffmpeg filter chain."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af,
                        "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"], input=x.astype(np.float32).tobytes(),
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).astype(np.float64)


raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.vo, "-t", str(a.end), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).astype(np.float64)
x = ff(x, "highpass=f=90:poles=2,afftdn=nr=16:nf=-48:tn=1")

# --- pauses ---
words = [w for s in json.load(open(a.words))["segments"] for w in s["words"]]
words = [w for w in words if w["end"] <= a.end]
hop = int(0.01 * SR)
env = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, "same"))[::hop]
db = 20 * np.log10(env + 1e-9)
thr = np.percentile(db, 15) + 10                      # "silence" = within 10 dB of the noise floor
cuts = []                                             # (start, end) sample ranges to delete
lead = next(i for i, v in enumerate(db) if v > thr) * hop
cuts.append((0, max(0, lead - int(0.12 * SR))))
for w0, w1 in zip(words, words[1:]):
    tail = w0["word"].strip()[-1:]
    target = 0.40 if tail in ".!?" else 0.24 if tail in ",;:" else 0.18
    g0, g1 = int((w0["end"] - 0.12) / 0.01), int((w1["start"] + 0.12) / 0.01)
    quiet = db[g0:g1] < thr
    best, run, start = (0, 0), 0, 0                       # longest quiet run in the gap
    for i, q in enumerate(quiet):
        if q:
            if run == 0: start = i
            run += 1
            if run > best[1] - best[0]: best = (start, start + run)
        else:
            run = 0
    n = (best[1] - best[0]) * hop
    if n <= (target + 0.05) * SR:
        continue
    mid = (g0 + (best[0] + best[1]) // 2) * hop
    cut = n - int(target * SR)
    cuts.append((mid - cut // 2, mid + cut - cut // 2))
xf = int(0.02 * SR); t = np.linspace(0, np.pi / 2, xf)
out, pos, removed = [], 0, 0.0
for c0, c1 in cuts:
    if c1 - c0 < xf * 2: continue
    out.append(x[pos:c0]); pos = c1; removed += (c1 - c0) / SR
pieces = [p for p in out + [x[pos:]] if len(p) > xf]      # the lead-in trim leaves an empty first piece
y = pieces[0]
for seg in pieces[1:]:
    y = np.concatenate([y[:-xf], y[-xf:] * np.cos(t) + seg[:xf] * np.sin(t), seg[xf:]])
fo = int(0.35 * SR); y[-fo:] *= np.linspace(1, 0, fo)
print(f"pauses: {len(cuts) - 1} gaps tightened, {removed:.1f} s removed -> {len(y) / SR:.1f} s")

# --- voice chain ---
chain = ",".join([
    "equalizer=f=160:t=q:w=1.0:g=-2.5",       # boom
    "equalizer=f=320:t=q:w=1.2:g=-3.5",       # box / phone cup
    "equalizer=f=1600:t=q:w=1.0:g=2",         # upper mids: less dark
    "equalizer=f=3000:t=q:w=1.0:g=6",         # presence: words land forward
    "equalizer=f=5200:t=q:w=1.0:g=3",         # articulation
    "highshelf=f=9000:g=3",
    "aexciter=level_in=1:level_out=1:amount=1.5:drive=6:blend=0:freq=7500:ceil=16000",  # air the phone codec lost
    "deesser=i=0.35:m=0.5:f=0.5:s=o",
    "acompressor=threshold=-24dB:ratio=3:attack=4:release=70:makeup=3:knee=4",
    "agate=threshold=0.012:ratio=2:range=0.3:attack=3:release=180:knee=3",  # pauses back down after the compressor lifted the noise
    f"atempo={a.tempo}",
])
y = ff(y, chain)
r = subprocess.run(["ffmpeg", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                   input=y.astype(np.float32).tobytes(), capture_output=True).stderr.decode()
i = float(json.loads(r[r.rindex("{"):r.rindex("}") + 1])["input_i"])
y *= 10 ** ((-16 - i) / 20)
y *= min(1.0, 10 ** (-1.5 / 20) / np.abs(y).max())
sf.write(a.out, np.stack([y, y], 1), SR, subtype="PCM_24")
print(f"-> {a.out}: {len(y) / SR:.2f} s at -16 LUFS (tempo x{a.tempo})")
