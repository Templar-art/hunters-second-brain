#!/bin/zsh
# Full build: graphics (alpha) → composite over talking head (full frame 0–5.4s, PiP 8–19.8s) → mix VO + SFX.
# Usage: ./build.sh v2   (needs NODE_PATH pointing at a playwright install)
set -e; cd "${0:a:h}"; V=${1:-v2}
node render.cjs video
python3 sfx.py
# PiP crop: head+shoulders from the 2160x3840 source, scaled to the PIP rect in graphics.html (660,1380 340x440)
ffmpeg -v error -y -i assets/th-source.mp4 -i build/graphics.mov -i build/sfx.wav -filter_complex "
 color=c=0x070B12:s=1080x1920:r=30:d=22.5[bg];
 [0:v]fps=30,split[a][b];
 [a]scale=1080:1920:flags=lanczos,tpad=stop_mode=clone:stop_duration=3[full];
 [b]crop=1000:1294:650:330,scale=340:440:flags=lanczos,tpad=stop_mode=clone:stop_duration=3[face];
 [bg][full]overlay=enable='lt(t,5.4)'[l1];
 [l1][face]overlay=660:1380:enable='between(t,8,19.8)'[l2];
 [l2][1:v]overlay=shortest=1[v];
 [0:a]atrim=0:19.75,afade=t=out:st=19.5:d=0.25,loudnorm=I=-16:TP=-1.5,apad[vo];
 [2:a]volume=0.9[fx];[vo][fx]amix=inputs=2:duration=shortest:normalize=0,alimiter=limit=0.95[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -c:a aac -b:a 256k -t 22.5 -movflags +faststart use-crud-$V.mp4
echo built use-crud-$V.mp4
