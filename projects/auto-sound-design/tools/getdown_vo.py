"""Get Down flythrough with Katrina's VO (34 Albany 1.m4a, speech 0.7-62.5 s; her "I love it." aside at 63.2 is cut).
Song: the B SMOOTH v2 opening (bar 1 start, intro bar 3 overlapping the build bar 15, chorus at ~8.9 s), all of chorus 1
(bars 16-26), bar 27 overlapping bar 55 (chroma 0.99, same 4-bar slot) into chorus 2 and the song's real stop: 67.6 s.
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
VO = "/Users/10xhunter/Downloads/34 Albany 1.m4a"
VO_END = 62.85                       # after "together." (62.5) + its tail
OUT = "output/getdown-vo"
BAR, END = 2.9705, 189.45
# measured downbeats (onset cross-correlation against bar 16, see getdown_punchy.py)
DOWN = {1: 0.116, 3: 0.102, 15: 0.009, 27: -0.084, 55: 0.078}
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
    a, b = t(15), t(27) + BAR
    p2 = s(a, b, src)
    if build_switch:
        inst = s(a, b, nv); n = min(p2.shape[1], inst.shape[1]); p2, inst = p2[:, :n], inst[:, :n]
        w = np.ones(n); k, bl = int((45.0 - a) * SR), int(0.1 * SR); w[:k] = 0; w[k:k + bl] = np.linspace(0, 1, bl)
        p2 = p2 * w + inst * (1 - w)
    p2[:, :nb] *= ramp(nb, True); p2[:, -nb:] *= ramp(nb, False)
    p3 = s(t(55), END, src); p3[:, :nb] *= ramp(nb, True)
    o2 = p1.shape[1] - nb; o3 = o2 + int((t(27) - a) * SR)
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

# VO: high-pass, light denoise, gentle leveling, trimmed after her last line, -16 LUFS
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", VO, "-t", str(VO_END + 0.4), "-af",
                      "highpass=f=80,afftdn=nr=8:nf=-60,acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=1",
                      "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
vo = np.frombuffer(raw, np.float32).reshape(-1, 2).T.astype(np.float64)
fo = int(0.4 * SR); vo[:, -fo:] *= np.linspace(1, 0, fo)
vo = gain_to(vo, -16.0)
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
for name, x in (("1 VO - Katrina (cleaned, trimmed).wav", vo_full), ("2 Music bed - ducked, instrumental under VO.wav", bed),
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
