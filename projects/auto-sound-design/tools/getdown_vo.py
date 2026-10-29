"""Get Down flythrough with Katrina's VO (34 Albany 1.m4a; "I love it." aside cut), polished by tools/vo_polish.py first.
Song: the B SMOOTH v2 opening (bar 1 start, intro bar 3 overlapping the build bar 15, chorus at ~8.9 s), chorus 1 to
OUT_BAR overlapping IN_BAR in chorus 2, then the song's real stop. v1 (raw VO, 62.5 s) used 27 -> 55 for 67.5 s;
v2 (polished VO, 57.4 s) used 25 -> 55 for 61.5 s; v3 (bedrooms line dropped, 54.4 s) used 25 -> 56 for 58.6 s;
v4 (30-40 s reel: spec + birdlife + balcony lines dropped too, VO 32.8 s) uses 22 -> 60 for 37.8 s.
Under the VO the song is the demucs instrumental (no rap over her lines), ducked 11 dB while she speaks (music ~11 dB under her);
after her last word the full mix (vocals) comes back for the ending.
Writes output/getdown-vo/: song full + instrumental fits, the mixed music bed, cleaned VO, and the full mix."""
import json, os, subprocess
import librosa, numpy as np, soundfile as sf
from scipy.ndimage import uniform_filter1d
SR = 48000
F = "/Users/10xhunter/Downloads/ryan james - Get Down (Put em up) _THIS SONG DONATES TO MAKE SCHOOLS HEALTHIER_.mp3"
SP = "/private/tmp/claude-502/-Users-10xhunter-Documents-Hunters-Second-Brain/a9457b91-92f8-41fe-9b10-939264c376f9/scratchpad"
NV = SP + "/demucs3/htdemucs/GetDown/no_vocals.wav"
VO = "output/getdown-vo/vo_polished.wav"   # tools/vo_polish.py: pauses tightened, voice chain, -16 LUFS, 57.4 s
OUT_BAR, IN_BAR = 22, 60             # chorus 1 bar 22 overlaps bar 60, the B SMOOTH v2 ending (chroma 1.00); ~5 s of song after her
VO_END = sf.info(VO).duration
OUT = "output/getdown-vo"
BAR, END = 2.9705, 189.45
# measured downbeats (onset cross-correlation against bar 16, see getdown_punchy.py)
DOWN = {1: 0.116, 3: 0.102, 15: 0.009, 22: -0.046, 25: -0.067, 27: -0.084, 55: 0.078, 56: 0.070, 60: 0.038}
t = lambda k: k * BAR + DOWN[k]
y, _ = librosa.load(F, sr=SR, mono=False); nv, _ = librosa.load(NV, sr=SR, mono=False)
s = lambda a, b, src: src[:, int(a * SR):int(b * SR)].copy()


def ramp(n, up, rise=1.6):
    g = np.sin(np.linspace(0, 1, n) ** rise * np.pi / 2)
    return g if up else np.sqrt(1 - g ** 2)


def song(src, build_switch):
    """Overlap-add of three pieces on measured downbeats. build_switch: the build bar starts on the instrumental
    stem and switches to src at the 45.0 breath gap (only matters for the full mix)."""
    nb = int(BAR * SR)
    p1 = s(t(1), t(3) + BAR, src); p1[:, -nb:] *= ramp(nb, False)
    a, b = t(15), t(OUT_BAR) + BAR
    p2 = s(a, b, src)
    if build_switch:
        inst = s(a, b, nv); n = min(p2.shape[1], inst.shape[1]); p2, inst = p2[:, :n], inst[:, :n]
        w = np.ones(n); k, bl = int((45.0 - a) * SR), int(0.1 * SR); w[:k] = 0; w[k:k + bl] = np.linspace(0, 1, bl)
        p2 = p2 * w + inst * (1 - w)
    p2[:, :nb] *= ramp(nb, True); p2[:, -nb:] *= ramp(nb, False)
    p3 = s(t(IN_BAR), END, src); p3[:, :nb] *= ramp(nb, True)
    o2 = p1.shape[1] - nb; o3 = o2 + int((t(OUT_BAR) - a) * SR)
    mix = np.zeros((2, o3 + p3.shape[1]))
    for o, p in ((0, p1), (o2, p2), (o3, p3)):
        mix[:, o:o + p.shape[1]] += p
    mix[:, :int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    f = int(0.15 * SR); mix[:, -f:] *= np.linspace(1, 0, f)
    return mix


def lufs(x):
    p = os.path.join(SP, "_lufs.wav"); sf.write(p, x.T, SR)
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(json.loads(r[r.rindex("{"):r.rindex("}") + 1])["input_i"])


def gain_to(x, target):
    return x * 10 ** ((target - lufs(x)) / 20)


os.makedirs(OUT, exist_ok=True)
full, inst = song(y, True), song(nv, False)
n = min(full.shape[1], inst.shape[1]); full, inst = full[:, :n], inst[:, :n]

vo = sf.read(VO)[0].T
vo_full = np.zeros((2, n)); vo_full[:, :vo.shape[1]] = vo[:, :n]

# bed: instrumental under the VO, crossfading to the full mix after her last word
k0, kf = int(VO_END * SR), int(1.0 * SR)
xw = np.zeros(n); xw[k0:k0 + kf] = np.sin(np.linspace(0, np.pi / 2, kf)) ** 2; xw[k0 + kf:] = 1
bed = inst * (1 - xw) + full * xw
bed = gain_to(bed, -16.0)
# duck while she speaks: VO activity envelope -> -11 dB, 150 ms in, 600 ms out
env = uniform_filter1d(np.abs(vo_full).mean(0), int(0.05 * SR))
act = (20 * np.log10(env + 1e-9) > -45).astype(float)
hold = uniform_filter1d(act, int(0.6 * SR)) > 0.02          # bridge short pauses between words
duck = np.where(hold, 10 ** (-11 / 20), 1.0)
duck[k0:] = 10 ** (-4 / 20)                                  # after her last line the hook returns, 4 dB down so it swells, not jumps
sm = np.copy(duck)
a_in, a_out = 1 - np.exp(-1 / (0.15 * SR)), 1 - np.exp(-1 / (0.6 * SR))
for i in range(1, n):
    c = a_in if duck[i] < sm[i - 1] else a_out
    sm[i] = sm[i - 1] + c * (duck[i] - sm[i - 1])
bed *= sm

mix = bed + vo_full
mix *= min(1.0, 10 ** (-1 / 20) / np.abs(mix).max())
for name, x in (("1 VO - Katrina (polished, tightened).wav", vo_full), ("2 Music bed - ducked, instrumental under VO.wav", bed),
                ("3 Song fit - full mix (no duck).wav", gain_to(full, -14.0)), ("4 Song fit - instrumental (no duck).wav", gain_to(inst, -14.0)),
                ("0 MIX - VO + song.wav", mix)):
    sf.write(os.path.join(OUT, name), x.T, SR, subtype="PCM_24")
# reference mix to ~-14 LUFS for phone playback: straight gain + a peak limiter at -2 dBFS sample (~-1 dBTP) (stems above stay unlimited)
m = os.path.join(OUT, "0 MIX - VO + song.wav")
g = -14.0 - lufs(mix)
tmp = os.path.join(SP, "_mix.wav"); os.replace(m, tmp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"volume={g:.2f}dB,alimiter=limit=0.79:attack=5:release=80:level=false",
                "-c:a", "pcm_s24le", m], check=True)
print(f"length {n / SR:.2f} s; VO ends {VO_END}; mix gain {g:+.1f} dB into the limiter")
