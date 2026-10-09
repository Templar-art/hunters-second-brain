#!/bin/zsh
# Pre-boss QA pack: face check + a still every second, tiled into contact sheets.
# Usage: tools/qa.sh <episode-name>   → episodes/<name>/build/qa/boss-1.png, boss-2.png, facecheck.json
set -e; ROOT="${0:a:h:h}"; EP="$ROOT/episodes/$1"; export NODE_PATH="$ROOT/tools/node_modules"
node "$ROOT/tools/render.cjs" "$EP" facecheck | tail -1
DUR=$(python3 -c "import json;print(json.load(open('$EP/build/render.json'))['dur'])")
TS=$(python3 -c "print(','.join(f'{t+.5:.1f}' for t in range(int($DUR))))")
setopt nullglob; rm -f "$EP"/build/qa/s_*.png
node "$ROOT/tools/render.cjs" "$EP" stills "$TS" >/dev/null
python3 - "$EP" "$TS" <<'PY'
import sys
from PIL import Image, ImageDraw
ep, ts = sys.argv[1], sys.argv[2].split(',')
for k in range(0, len(ts), 18):
    part = ts[k:k + 18]; S = Image.new('RGB', (6 * 300, 3 * 560), 'black'); d = ImageDraw.Draw(S)
    for i, t in enumerate(part):
        S.paste(Image.open(f'{ep}/build/qa/s_{t}.png').convert('RGB').resize((300, 533)), ((i % 6) * 300, (i // 6) * 560))
        d.text(((i % 6) * 300 + 6, (i // 6) * 560 + 538), f'{t}s', fill='white')
    S.save(f'{ep}/build/qa/boss-{k // 18 + 1}.png')
print('sheets:', (len(ts) + 17) // 18)
PY
