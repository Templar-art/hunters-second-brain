"""Wildfire (C. James) reel cut, Hunter's cinematic flow: intro -> verse into the stop-bar hit -> chorus -> final-chorus tail + natural fade.
Vocal-safe: the verse pre-roll is instrumental-only (demucs stem) until the singer's breath gap; the chorus jump sits in a vocal gap on both sides."""
import librosa, numpy as np, soundfile as sf
SR = 48000
F = "/Users/10xhunter/Downloads/Wildfire.mp3"
NV = "/private/tmp/claude-502/-Users-10xhunter-Documents-Hunters-Second-Brain/a9457b91-92f8-41fe-9b10-939264c376f9/scratchpad/demucs2/htdemucs/Wildfire/no_vocals.wav"
y, _ = librosa.load(F, sr=SR, mono=False); nv, _ = librosa.load(NV, sr=SR, mono=False)
def s(a, b, src=None):
    src = y if src is None else src
    return src[:, int(a * SR):int(b * SR)].copy()
INTRO_END, J, GAP, BAR = 8.36, 35.25, 34.55, 4 * 0.5108
intro = s(0.0, INTRO_END)
n = int(BAR * SR)
pre, full = s(J - BAR, J, nv)[:, :n], s(J - BAR, J)[:, :n]
n = min(n, pre.shape[1], full.shape[1]); pre, full = pre[:, :n], full[:, :n]
k = int((GAP - (J - BAR)) * SR); bl = int(0.1 * SR)
w = np.zeros(n); w[k:k + bl] = np.linspace(0, 1, bl); w[k + bl:] = 1
pre = pre * (1 - w) + full * w
t = np.linspace(0, 1, n)
intro[:, -n:] = intro[:, -n:] * np.cos(t * np.pi / 2) + pre * np.sin(t * np.pi / 2)
mix = np.concatenate([intro, s(J, 49.74)], axis=1)
m = int(0.25 * SR); tt = np.linspace(0, np.pi / 2, m); nxt = s(115.94 - 0.25, 131.4)
mix[:, -m:] = mix[:, -m:] * np.cos(tt) + nxt[:, :m] * np.sin(tt)
mix = np.concatenate([mix, nxt[:, m:]], axis=1)
f = int(0.5 * SR); mix[:, -f:] *= np.cos(np.linspace(0, np.pi / 2, f)) ** 2
mix[:, :480] *= np.linspace(0, 1, 480)
sf.write("output/wildfire-reel/Wildfire_CJames_reel.wav", mix.T, SR, subtype="PCM_24")
mm = mix.mean(0); h = SR // 2
print(round(mix.shape[1] / SR, 2), "s")
print(" ".join(f"{i/2:.1f}:{20*np.log10(np.sqrt(np.mean(mm[i*h:(i+1)*h]**2))+1e-9):.0f}" for i in range(len(mm) // h)))
