"""Get Down (Put em up) - Ryan James, PUNCHY flythrough cuts (Hunter: "more punchy, more of the chorus where it goes quicker").
Song map (2.9705 s bars from 0:00): intro 0-23.8, verse 23.8-47.5, chorus 47.53-83, verse 83-130.7, chorus 130.7-end (hard stop 189.45).
Bar 15 (44.56) is the dip/build into the chorus. Cuts: intro bars -> that build bar -> 5 bars of chorus 1 -> the song's own
last chorus bars and ending from bar 61 (181.20; same harmony, same 4-bar phrase slot, vocal gap at 62.38 -> 181.2).
The build bar starts on a verse word's tail, so it comes in on the demucs instrumental stem until the breath gap at 45.0."""
import librosa, numpy as np, soundfile as sf
SR = 48000
F = "/Users/10xhunter/Downloads/ryan james - Get Down (Put em up) _THIS SONG DONATES TO MAKE SCHOOLS HEALTHIER_.mp3"
NV = "/private/tmp/claude-502/-Users-10xhunter-Documents-Hunters-Second-Brain/a9457b91-92f8-41fe-9b10-939264c376f9/scratchpad/demucs3/htdemucs/GetDown/no_vocals.wav"
BAR, END = 2.9705, 189.45
y, _ = librosa.load(F, sr=SR, mono=False); nv, _ = librosa.load(NV, sr=SR, mono=False)
s = lambda a, b, src=y: src[:, int(a * SR):int(b * SR)].copy()


def build_bar():
    """Bar 15 on the instrumental stem, switching to the full mix in the breath gap at 45.0 (0.1 s blend)."""
    a, b = 15 * BAR, 16 * BAR
    inst, full = s(a, b, nv), s(a, b)
    n = min(inst.shape[1], full.shape[1]); inst, full = inst[:, :n], full[:, :n]
    k, bl = int((45.0 - a) * SR), int(0.1 * SR)
    w = np.zeros(n); w[k:k + bl] = np.linspace(0, 1, bl); w[k + bl:] = 1
    return inst * (1 - w) + full * w


def join(x, z, xf=0.12):
    m = int(xf * SR); t = np.linspace(0, np.pi / 2, m)
    x[:, -m:] = x[:, -m:] * np.cos(t) + z[:, :m] * np.sin(t)
    return np.concatenate([x, z[:, m:]], axis=1)


def cut(intro_bars, out):
    mix = s(0, intro_bars * BAR + 0.06)            # 60 ms of the next bar under the fade
    mix = join(mix, build_bar())
    mix = join(mix, s(16 * BAR, 21 * BAR + 0.06))  # chorus 1, five bars
    mix = join(mix, s(61 * BAR, END))              # last chorus bars + the real ending
    mix[:, :480] *= np.linspace(0, 1, 480)
    f = int(0.15 * SR); mix[:, -f:] *= np.linspace(1, 0, f)
    sf.write(out, mix.T, SR, subtype="PCM_24")
    print(out, round(mix.shape[1] / SR, 2), "s; chorus hits at", round((intro_bars + 1) * BAR, 2), "s")


cut(3, "output/getdown-reel/GetDown_reel_PUNCHY-A.wav")
cut(2, "output/getdown-reel/GetDown_reel_PUNCHY-B.wav")
