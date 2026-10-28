"""Regrade an AI dusk clip toward the real Kollosche twilight reference: bright creamy warm-white
interior, deep navy sky, darker exterior foliage. Works per pixel in Lab with soft hue masks, so
the interior and exterior are graded separately without a hand-drawn matte.

Usage:
  deorange.py frame in.png out.png                    # test one still
  deorange.py video in.mov out.mov                    # full clip, 16-bit in -> ProRes 422 HQ out
Tuning lives in PARAMS.
"""
import sys, subprocess, json, cv2, numpy as np

PARAMS = dict(
    wb=(0.92, 0.98, 1.08),  # RGB gains: pull the amber cast toward warm-white
    sat=0.80,               # global chroma kept
    gamma=0.88,             # midtone lift so the interior reads bright like the ref
    sky_dark=1.0,           # L multiplier inside the (blurred) sky/blue mask
    sky_chroma=1.0,         # deepen the sky toward the ref's navy
    contrast=1.12,          # S-curve around mid grey so it does not read washed
)

def grade(rgb, p=PARAMS):
    """rgb float32 0-1, returns float32 0-1. Global moves only, plus one heavily blurred
    sky mask, so there is no per-pixel blotching on near-neutral surfaces."""
    rgb = np.clip(rgb * np.array(p["wb"], np.float32), 0, 1)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    L, a, b = cv2.split(lab)
    # sky mask: clearly blue pixels. The sky is a smooth gradient, so a near-sharp mask is
    # stable there; a wide blur haloed around the tree and ceiling edge.
    blue = np.clip((-b - 8) / 14, 0, 1) * np.clip((L - 15) / 20, 0, 1)
    sky = cv2.GaussianBlur(blue, (0, 0), 1.5)
    k = p["sat"] * (1 + (p["sky_chroma"] - 1) * sky)
    a, b = a * k, b * k
    L = 100 * np.power(np.clip(L / 100, 0, 1), p["gamma"])
    L = 50 + (L - 50) * p["contrast"]
    L = L * (1 - (1 - p["sky_dark"]) * sky)
    out = cv2.cvtColor(cv2.merge([L, a, b]), cv2.COLOR_LAB2RGB)
    return np.clip(out, 0, 1)

def do_frame(i, o):
    bgr = cv2.imread(i, cv2.IMREAD_UNCHANGED)
    scale = 65535.0 if bgr.dtype == np.uint16 else 255.0
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / scale
    out = grade(rgb)
    cv2.imwrite(o, cv2.cvtColor((out * 255).round().astype(np.uint8), cv2.COLOR_RGB2BGR))

def do_video(i, o):
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate", "-of", "json", i]))["streams"][0]
    w, h, fps = info["width"], info["height"], info["r_frame_rate"]
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", i, "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le",
        "-s", f"{w}x{h}", "-r", fps, "-i", "-", "-c:v", "prores_ks", "-profile:v", "3",
        "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-colorspace", "bt709", o], stdin=subprocess.PIPE)
    n = w * h * 3 * 2
    while True:
        buf = dec.stdout.read(n)
        if len(buf) < n:
            break
        rgb = np.frombuffer(buf, np.uint16).reshape(h, w, 3).astype(np.float32) / 65535.0
        enc.stdin.write((grade(rgb) * 65535).round().astype(np.uint16).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()

if __name__ == "__main__":
    {"frame": do_frame, "video": do_video}[sys.argv[1]](sys.argv[2], sys.argv[3])
