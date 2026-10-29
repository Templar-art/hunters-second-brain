"""Wildfire (C. James) fitted to Hunter's 'Cinematic Reel.mp4' (38.41 s, cut on Einaudi D's grid).
Picture anchors: lifestyle intro, woman at door 10.05, interior build, top-down aerial 22.11 (the hit), balcony 32.49, aerial out.
Song: intro from 0.64 -> 1-bar overlap into the verse at 31.16 (pre-roll instrumental until the breath gap at 30.5)
-> stop bar -> chorus hit at 43.51 lands on 22.11 -> chorus to the gap at 45.6 -> final chorus from 115.94 into its natural fade."""
import librosa, numpy as np, soundfile as sf
SR = 48000
F = "/Users/10xhunter/Downloads/Wildfire.mp3"
NV = "/private/tmp/claude-502/-Users-10xhunter-Documents-Hunters-Second-Brain/a9457b91-92f8-41fe-9b10-939264c376f9/scratchpad/demucs2/htdemucs/Wildfire/no_vocals.wav"
LENGTH = 38.41
y, _ = librosa.load(F, sr=SR, mono=False); nv, _ = librosa.load(NV, sr=SR, mono=False)
def s(a, b, src=None):
    src = y if src is None else src
    return src[:, int(a * SR):int(b * SR)].copy()
START, INTRO_END, J, GAP, BAR = 0.64, 10.40, 31.16, 30.5, 4 * 0.5108
intro = s(START, INTRO_END)
n = int(BAR * SR)
pre, full = s(J - BAR, J, nv)[:, :n], s(J - BAR, J)[:, :n]
n = min(n, pre.shape[1], full.shape[1]); pre, full = pre[:, :n], full[:, :n]
k = int((GAP - (J - BAR)) * SR); bl = int(0.1 * SR)
w = np.zeros(n); w[k:k + bl] = np.linspace(0, 1, bl); w[k + bl:] = 1
pre = pre * (1 - w) + full * w
t = np.linspace(0, 1, n)
intro[:, -n:] = intro[:, -n:] * np.cos(t * np.pi / 2) + pre * np.sin(t * np.pi / 2)
mix = np.concatenate([intro, s(J, 45.6)], axis=1)
print("hit at", round((INTRO_END - START + 43.51 - J), 2), "s; splice at", round(mix.shape[1] / SR, 2))
m = int(0.25 * SR); tt = np.linspace(0, np.pi / 2, m)
rest = LENGTH - mix.shape[1] / SR
nxt = s(115.94 - 0.25, 115.94 + rest)
mix[:, -m:] = mix[:, -m:] * np.cos(tt) + nxt[:, :m] * np.sin(tt)
mix = np.concatenate([mix, nxt[:, m:]], axis=1)[:, :int(LENGTH * SR)]
f = int(1.2 * SR); mix[:, -f:] *= np.cos(np.linspace(0, np.pi / 2, f)) ** 2
mix[:, :1440] *= np.linspace(0, 1, 1440)
out = "output/wildfire-reel/Wildfire_CJames_reel_FIT.wav"
sf.write(out, mix.T, SR, subtype="PCM_24")
mm = mix.mean(0); h = SR // 2
print(round(mix.shape[1] / SR, 2), "s ->", out)
print(" ".join(f"{i/2:.1f}:{20*np.log10(np.sqrt(np.mean(mm[i*h:(i+1)*h]**2))+1e-9):.0f}" for i in range(len(mm) // h)))
