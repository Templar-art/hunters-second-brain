"""Clone-format source builder: two takes from a locked-off camera composited into one frame
(coach layer on the left, client layer on the right, feathered seam between them), written as 50fps
JPG frames straight from the original files, plus the speaking take's audio as the episode's source.

Usage: python3 tools/clone.py <episode_dir>   (reads <episode_dir>/clone.json)

clone.json:
{ "footage": "<dir with the takes>",
  "ref": "<take used as the colour reference>",
  "shift": {"<take>": [dx, dy]},             # sub-frame alignment of a take onto the reference (px)
  "seam": [560, 50],                         # centre x and half-width of the feather
  "settle": {"<take>": t},                   # a time where the take's auto-exposure has settled (colour fit + exposure target)
  "segments": [ {"dur": 6.6, "left": ["coachTake", t0], "right": ["clientTake", t0], "audio": ["take", t0]}, ... ] }
Writes build/frames/fNNNN.jpg, build/meta.json, build/clone_words.json (per-take words mapped onto the timeline)
and source.mp4 (audio only, ALAC)."""
import json, os, subprocess, sys, wave
import numpy as np, cv2

EP = sys.argv[1]; C = json.load(open(os.path.join(EP, 'clone.json'))); FOOT = C['footage']; FPS = 50; W, H = 1080, 1920
path = lambda take: os.path.join(FOOT, take + '.MOV')

def reader(take, t0):
    """Raw RGB frames of a take from t0 (autorotated to portrait)."""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-i', path(take), '-vf', f'fps={FPS},scale={W}:{H}:flags=lanczos',
                          '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    last = None
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        last = np.frombuffer(b, np.uint8).reshape(H, W, 3); yield last
    while last is not None: yield last          # past the end of the take: hold the last frame

# colour match: per-channel linear map from each take onto the reference, fitted on static wall + table patches
def patches(take, t):
    im = next(reader(take, t)).astype(np.float32)
    return im[100:450, 380:700].reshape(-1, 3).mean(0), im[1300:1600, 380:700].reshape(-1, 3).mean(0)
takes = sorted({s[k][0] for s in C['segments'] for k in ('left', 'right')})
ST = C.get('settle', {}); st = lambda tk: ST.get(tk, 3.0)
rw, rt = patches(C['ref'], st(C['ref'])); GAIN = {}
for tk in takes:
    w_, t_ = patches(tk, st(tk)); a = (rw - rt) / np.maximum(w_ - t_, 1e-3); GAIN[tk] = (a, rw - a * w_)
    print('colour', tk, 'gain', a.round(3), 'offset', GAIN[tk][1].round(1))
def fix(take, im):
    a, b = GAIN[take]; im = np.clip(im.astype(np.float32) * a + b, 0, 255)
    dx, dy = C.get('shift', {}).get(take, [0, 0])
    if dx or dy: im = cv2.warpAffine(im, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REPLICATE)
    return im

# auto-exposure ramps (iPhone settling at the start of a take): match each layer, per frame, to its settled level
# with a gamma tone curve (keeps the white wall from clipping), smoothed over ~5 frames
PATCH = {'left': (slice(440, 560), slice(250, 400)), 'right': (slice(440, 560), slice(650, 780))}
lum = lambda im, side: float((im[PATCH[side]] @ np.float32([.114, .587, .299])).mean())   # BGR
TARGET = {}
def target(tk, side):
    if (tk, side) not in TARGET: TARGET[(tk, side)] = lum(fix(tk, next(reader(tk, st(tk)))), side)
    return TARGET[(tk, side)]
LUT_X = np.arange(256, dtype=np.float32) / 255
def expose(im, tk, side, state):
    cur, tgt = lum(im, side) / 255, target(tk, side) / 255
    gm = float(np.clip(np.log(max(tgt, 1e-3)) / np.log(min(max(cur, 1e-3), .999)), .6, 1.6))
    state['g'] = gm if state.get('g') is None else state['g'] * .67 + gm * .33
    if abs(state['g'] - 1) < .005: return im
    lut = (255 * LUT_X ** state['g']).astype(np.float32)
    return lut[np.clip(im, 0, 255).astype(np.uint8)]

cx, fw = C.get('seam', [560, 50]); x = np.arange(W, dtype=np.float32)
M = np.clip((x - (cx - fw)) / (2 * fw), 0, 1)[None, :, None]   # 0 = left layer, 1 = right layer
out = os.path.join(EP, 'build', 'frames'); os.makedirs(out, exist_ok=True)
for f in os.listdir(out): os.remove(os.path.join(out, f))
n = 0; t = 0.0; words = []; cuts = []; audio = []
for s in C['segments']:
    N = round(s['dur'] * FPS); L = reader(*s['left']); R = reader(*s['right']); sl, sr = {}, {}
    for _ in range(N):
        a = expose(fix(s['left'][0], next(L)), s['left'][0], 'left', sl); b = expose(fix(s['right'][0], next(R)), s['right'][0], 'right', sr); n += 1
        cv2.imwrite(os.path.join(out, f'f{n:04d}.jpg'), (a * (1 - M) + b * M).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 97])
    tk, a0 = s['audio']; cuts.append(round(t, 3))
    wj = os.path.join(EP, 'build', 'takes', tk + '.json')
    if os.path.exists(wj):
        for w in json.load(open(wj)):
            if a0 - .02 <= w['s'] < a0 + s['dur']: words.append({'w': w['w'], 's': round(w['s'] - a0 + t, 2), 'e': round(min(w['e'], a0 + s['dur']) - a0 + t, 2)})
    audio.append((tk, a0, N / FPS)); t += N / FPS
    print(f'segment {len(cuts)}: {N} frames, {s["left"]} | {s["right"]} → total {n}')
json.dump({'frames': n}, open(os.path.join(EP, 'build', 'meta.json'), 'w'))
json.dump({'cuts': cuts, 'words': words, 'dur': round(t, 3)}, open(os.path.join(EP, 'build', 'clone_words.json'), 'w'))
# audio: speaking take per segment, 8ms fades at every join so cuts never click
parts = []
for i, (tk, a0, d) in enumerate(audio):
    p = os.path.join(EP, 'build', f'a{i}.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a0:.3f}', '-t', f'{d:.3f}', '-i', path(tk), '-vn', '-ac', '1', '-ar', '48000',
                    '-af', f'afade=t=in:d=0.008,afade=t=out:st={d - .008:.3f}:d=0.008', p], check=True); parts.append(p)
lst = os.path.join(EP, 'build', 'alist.txt'); open(lst, 'w').write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:a', 'alac', os.path.join(EP, 'source.mp4')], check=True)
print('frames', n, 'dur', round(t, 2), '→ source.mp4 (audio)')
