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


def overlap(out_a, out_src, in_a, in_src, rise=1.6):
    """One bar where the outgoing bar (out_src from out_a) fades out while the incoming bar (in_src from in_a)
    swells in: equal power, incoming on a delayed curve sin((t**rise)*pi/2) so the swell lands on the downbeat."""
    x, z = s(out_a, out_a + BAR, out_src), s(in_a, in_a + BAR, in_src)
    n = min(x.shape[1], z.shape[1]); t = np.linspace(0, 1, n)
    gi = np.sin(t ** rise * np.pi / 2); go = np.sqrt(1 - gi ** 2)
    return x[:, :n] * go + z[:, :n] * gi


def cut_smooth(out):
    """B shape (chorus at 8.91 s), every join a bar-long overlap (Hunter: B's 0.12 s joins were too harsh).
    Intro bar 1 under bar 14 on the instrumental stem (no verse vocal) -> bar 15 build -> chorus bars 16-19 ->
    bar 20 fading out on the instrumental stem under bar 60 (the ending's lead-in, its vocal rising in) -> bar 61 to the stop.
    Bars 20 and 60 sit in the same 4-bar slot; intro bar 1 is vocal-free (3.25-6.2 s)."""
    parts = [s(0, BAR), overlap(BAR, y, 14 * BAR, nv), build_bar(), s(16 * BAR, 20 * BAR),
             overlap(20 * BAR, nv, 60 * BAR, y), s(61 * BAR, END)]
    mix = parts[0]
    for p in parts[1:]:
        mix = join(mix, p, xf=0.01)  # 10 ms seam guard between contiguous bars
    mix[:, :480] *= np.linspace(0, 1, 480)
    f = int(0.15 * SR); mix[:, -f:] *= np.linspace(1, 0, f)
    sf.write(out, mix.T, SR, subtype="PCM_24")
    print(out, round(mix.shape[1] / SR, 2), "s; chorus hits at", round(3 * BAR, 2), "s")


# Measured downbeat of bar k = k*BAR + offset (onset-envelope cross-correlation against bar 16, the chorus downbeat).
# The fixed grid drifts: the intro sits ~0.1 s late against it, bar 20 32 ms early, bar 60 38 ms late.
DOWN = {1: 0.116, 3: 0.102, 15: 0.009, 16: 0.0, 20: -0.032, 60: 0.038}
t = lambda k: k * BAR + DOWN[k]


def cut_smooth2(out, rise=1.6):
    """B SMOOTH v2 (Hunter: "you can sorta hear it at the start"). Bar 14, the old pre-roll, clashed with the intro
    (chroma 0.58) and sat ~0.1 s off its beat. Now: start one bar in (bar 1, vocal-free), intro bars 1-3, with bar 3
    (chroma 0.98 to the build bar) overlapping bar 15 -> chorus bars 16-19 -> bar 20 (instrumental stem) overlapping
    bar 60 -> the ending. Overlap-add on measured downbeats; chorus still hits at 2 bars + one overlap bar = ~8.9 s."""
    def ramp(n, up):
        g = np.sin(np.linspace(0, 1, n) ** rise * np.pi / 2)
        return g if up else np.sqrt(1 - g ** 2)
    nb = int(BAR * SR)
    p1 = s(t(1), t(3) + BAR)                                     # intro bars 1-3, fades out across bar 3
    p1[:, -nb:] *= ramp(nb, False)
    a, b = t(15), t(20) + BAR                                    # build bar + chorus bars 16-20
    full, inst = s(a, b), s(a, b, nv)
    n = min(full.shape[1], inst.shape[1]); full, inst = full[:, :n], inst[:, :n]
    w = np.ones(n); k, bl = int((45.0 - a) * SR), int(0.1 * SR)
    w[:k] = 0; w[k:k + bl] = np.linspace(0, 1, bl)                # build bar on the instrumental stem until the 45.0 gap
    e = int((t(20) - a) * SR); w[e:e + bl] = np.minimum(w[e:e + bl], np.linspace(1, 0, bl)); w[e + bl:] = 0  # bar 20 instrumental
    p2 = full * w + inst * (1 - w)
    p2[:, :nb] *= ramp(nb, True); p2[:, -nb:] *= ramp(nb, False)
    p3 = s(t(60), END)                                           # the ending's lead-in bar swells in, then plays to the stop
    p3[:, :nb] *= ramp(nb, True)
    o2 = p1.shape[1] - nb                                        # p2's downbeat on p1's bar-3 downbeat
    o3 = o2 + int((t(20) - a) * SR)                              # p3's downbeat on p2's bar-20 downbeat
    mix = np.zeros((2, o3 + p3.shape[1]))
    for o, p in ((0, p1), (o2, p2), (o3, p3)):
        mix[:, o:o + p.shape[1]] += p
    mix[:, :int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))   # 0.3 s fade-in: the reel opens one bar into the song
    f = int(0.15 * SR); mix[:, -f:] *= np.linspace(1, 0, f)
    sf.write(out, mix.T, SR, subtype="PCM_24")
    print(out, round(mix.shape[1] / SR, 2), "s; chorus hits at", round((o2 + int((t(16) - a) * SR)) / SR, 2), "s")


cut(3, "output/getdown-reel/GetDown_reel_PUNCHY-A.wav")
cut(2, "output/getdown-reel/GetDown_reel_PUNCHY-B.wav")
cut_smooth("output/getdown-reel/GetDown_reel_PUNCHY-B-SMOOTH.wav")
cut_smooth2("output/getdown-reel/GetDown_reel_PUNCHY-B-SMOOTH2.wav")
