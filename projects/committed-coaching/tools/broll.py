"""Cut a B-roll clip into an episode slot. Usage:
  python3 tools/broll.py <episode_dir> <slot_dir> <clip> <start_s> <dur_s> [x_center 0..1]
Writes <episode_dir>/<slot_dir>/fNNNN.jpg: 50fps, 1080x1920, cropped to 9:16 around x_center (landscape sources),
exactly ceil(dur*50)+2 frames so the slot never runs out. Portrait sources are scaled to fill."""
import sys, os, subprocess, json, shutil
ep, slot, clip, start, dur = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
xc = float(sys.argv[6]) if len(sys.argv) > 6 else .5
info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:stream_side_data=rotation', '-of', 'json', clip]))['streams'][0]
w, h = info['width'], info['height']
rot = abs(int(next((d.get('rotation', 0) for d in info.get('side_data_list', [])), 0)))
if rot in (90, 270): w, h = h, w
if w / h > 9 / 16:   # wider than 9:16: crop a vertical slice around x_center
    cw = int(h * 9 / 16) // 2 * 2; x = int(min(max(0, w * xc - cw / 2), w - cw))
    vf = f'fps=50,crop={cw}:{h}:{x}:0,scale=1080:1920:flags=lanczos'
else:
    vf = 'fps=50,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920'
n = int(dur * 50 + .999) + 2
out = os.path.join(ep, slot); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-i', clip, '-frames:v', str(n), '-vf', vf, '-q:v', '1', '-qmin', '1', os.path.join(out, 'f%04d.jpg')], check=True)
print(slot, len(os.listdir(out)), 'frames')
