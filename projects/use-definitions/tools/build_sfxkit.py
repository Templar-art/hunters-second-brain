"""Build sfx-lib-v2/ (the v2 redo sound kit) from Ocular Sounds + Sound Lab UI renders.

    python3 tools/build_sfxkit.py [uikit_dir]      # default sfx-src/uikit (from tools/uikit/render_uikit.cjs)

Every take is cut to a usable window, loudness-matched per type (RMS), faded, and written
as 48k 16-bit stereo <type>_N.wav — the naming tools/sfx.py already reads. Select the kit
per build with SFX_LIB=sfx-lib-v2 (older episodes keep sfx-lib). WAVs are gitignored;
this script + kit.json are the record. Ocular = Hunter's purchased licence (commercial).
"""
import json, os, subprocess, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OCULAR = os.path.expanduser("~/Music/SFX Library/Ocular Sounds/Foundation")
UIKIT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "sfx-src", "uikit")
OUT = os.path.join(ROOT, "sfx-lib-v2")
SR = 48000

# type -> list of (source, how to cut). Ocular files are matched by title substring.
KIT = {
    # short, soft whooshes only: cinematic doppler/power ones fight the voice
    "whoosh": [("ocular", "DSGNWhsh", t) for t in
               ["Organic Motion", "Two Steps", "Dark Air", "Speed is Everything", "Passed By",
                "Be Gentle", "Fastlane", "Turn of Events"]],
    "thud":   [("ocular", "DSGNImpt", t) for t in ["Clean Rumble", "Gut Feeling", "Quick and Dirty", "Not What You Think"]],
    "riser":  [("ocular", "DSGNRise", t) for t in ["Lift Off", "Fresh Air", "Into the Light"]],
    "pop":    [("ui", f"pop_{s}") for s in ["bead", "dew", "pebble", "boop", "dot"]],
    "click":  [("ui", f"click_{s}") for s in ["nib", "notch", "tab", "tink"]],
    "key":    [("ui", f"key_{s}") for s in ["keycap", "chiclet", "thock"]],
    "chime":  [("ui", f"chime_{s}") for s in ["chime", "ping"]],
}
# window around the anchor (seconds before, after) and target RMS (dBFS) per type
CUT = {"whoosh": (.45, .35), "thud": (0, 1.1), "riser": (1.6, .35), "pop": (0, .5), "click": (0, .25),
       "key": (0, .15), "chime": (0, 1.2)}
RMS_DB = {"whoosh": -20, "thud": -18, "riser": -22, "pop": -20, "click": -22, "key": -24, "chime": -24}
ANCHOR_PEAK = {"whoosh", "riser"}


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def ocular_file(cat, title):
    d = os.path.join(OCULAR, cat)
    hits = [f for f in os.listdir(d) if f.endswith(".wav") and title.lower() in f.lower()]
    if not hits:
        raise SystemExit(f"Ocular: no '{title}' in {cat}")
    return os.path.join(d, sorted(hits)[0])


def cut(x, kind):
    m = np.abs(x).mean(1)
    env = np.convolve(m, np.ones(480) / 480, "same")             # 10 ms envelope
    pre, post = CUT[kind]
    if kind in ANCHOR_PEAK:
        a = int(np.argmax(env))
    else:
        a = int(np.argmax(env > env.max() * .1))                  # onset
        a = max(0, a - int(.004 * SR))
    y = x[max(0, a - int(pre * SR)): a + int(post * SR)].copy()
    fi, fo = int(.01 * SR), int(min(.12, post * .5) * SR)
    y[:fi] *= np.linspace(0, 1, fi)[:, None]
    y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    rms = np.sqrt((y ** 2).mean()) or 1e-9
    y *= 10 ** (RMS_DB[kind] / 20) / rms
    pk = np.abs(y).max()
    if pk > .95:
        y *= .95 / pk
    return y


def write(path, y):
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".wav"):
            os.remove(os.path.join(OUT, f))
    manifest = {}
    for kind, srcs in KIT.items():
        n = 0
        for s in srcs:
            files = [ocular_file(s[1], s[2])] if s[0] == "ocular" else \
                sorted(os.path.join(UIKIT, f) for f in os.listdir(UIKIT) if f.startswith(s[1] + "_"))
            for src in files:
                n += 1
                y = cut(decode(src), kind)
                name = f"{kind}_{n}.wav"
                write(os.path.join(OUT, name), y)
                manifest[name] = {"source": src.replace(os.path.expanduser("~"), "~"), "dur": round(len(y) / SR, 2)}
        print(f"{kind:7} {n} takes")
    import shutil                                                     # Magnific shatter takes carry over
    for f in sorted(os.listdir(os.path.join(ROOT, "sfx-lib"))):
        if f.startswith("glass_"):
            shutil.copy(os.path.join(ROOT, "sfx-lib", f), os.path.join(OUT, f))
            manifest[f] = {"source": "sfx-lib/" + f + " (Magnific, 9 Oct)"}
    json.dump(manifest, open(os.path.join(ROOT, "sfx-lib-v2.kit.json"), "w"), indent=1)


main()
