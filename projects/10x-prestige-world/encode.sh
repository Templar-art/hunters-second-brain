#!/bin/bash
# Encode raw legs for scrubbing + extract posters + mobile siblings + SSIM seam gate.
# Idempotent. bash-3.2-safe.
set -u
cd "$(dirname "$0")"
mkdir -p site/assets/vid site/assets/stills

for i in 1 2 3 4 5; do
  raw="clips/leg_${i}_raw.mp4"
  out="site/assets/vid/leg_${i}.mp4"
  mout="site/assets/vid/leg_${i}-m.mp4"
  [ -s "$raw" ] || { echo "[encode] missing $raw"; exit 1; }

  # desktop master: native 1080p, crf20, GOP 8, no audio, light unsharp
  if [ ! -s "$out" ]; then
    ffmpeg -y -i "$raw" -an -vf "unsharp=5:5:0.8:5:5:0.0" \
      -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
      -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart "$out" 2>/dev/null
    echo "[encode] leg_$i master done"
  fi

  # mobile sibling: 720p, GOP 4, crf 23
  if [ ! -s "$mout" ]; then
    ffmpeg -y -i "$raw" -an -vf "scale=1280:720:flags=lanczos,unsharp=5:5:0.6:5:5:0.0" \
      -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
      -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart "$mout" 2>/dev/null
    echo "[encode] leg_$i mobile done"
  fi

  # posters = first frame of the ENCODED clips (seam-zero doctrine)
  [ -s "site/assets/vid/leg_${i}-poster.jpg" ]   || ffmpeg -y -ss 0 -i "$out"  -frames:v 1 -q:v 3 "site/assets/vid/leg_${i}-poster.jpg" 2>/dev/null
  [ -s "site/assets/vid/leg_${i}-m-poster.jpg" ] || ffmpeg -y -ss 0 -i "$mout" -frames:v 1 -q:v 3 "site/assets/vid/leg_${i}-m-poster.jpg" 2>/dev/null
done

# stills for reduced-motion mode (jpeg, web-sized)
for i in 1 2 3 4 5; do
  dst="site/assets/stills/scene_${i}.jpg"
  [ -s "$dst" ] || ffmpeg -y -i "stills/scene_${i}.png" -vf "scale=1920:-2" -q:v 3 "$dst" 2>/dev/null
done

# SSIM seam gate: last frame of encoded leg i vs first frame of encoded leg i+1
echo ""
echo "=== SSIM SEAM GATE ==="
fail=0
for i in 1 2 3 4; do
  n=$((i+1))
  ffmpeg -y -sseof -0.05 -i "site/assets/vid/leg_${i}.mp4" -frames:v 1 -q:v 2 "frames/seam_${i}_a.png" 2>/dev/null
  ffmpeg -y -ss 0        -i "site/assets/vid/leg_${n}.mp4" -frames:v 1 -q:v 2 "frames/seam_${i}_b.png" 2>/dev/null
  ssim=$(ffmpeg -i "frames/seam_${i}_a.png" -i "frames/seam_${i}_b.png" \
    -lavfi "ssim" -f null - 2>&1 | grep -o "All:[0-9.]*" | cut -d: -f2)
  echo "seam $i->$n : SSIM=$ssim"
  ok=$(python3 -c "print(1 if float('${ssim:-0}') >= 0.90 else 0)")
  [ "$ok" = "1" ] || { echo "  *** BELOW 0.90 — REDO, not a QA note ***"; fail=1; }
done
[ "$fail" = "0" ] && echo "SEAM GATE: GREEN" || echo "SEAM GATE: RED"

# swap interim still-posters back to the real extracted-frame posters
for i in 1 2 3 4 5; do
  if [ -s "site/assets/vid/leg_${i}-poster.jpg" ]; then
    sed -i '' "s|poster: 'assets/stills/scene_${i}.jpg'|poster: 'assets/vid/leg_${i}-poster.jpg'|; s|posterMobile: 'assets/stills/scene_${i}.jpg'|posterMobile: 'assets/vid/leg_${i}-m-poster.jpg'|" site/index.html
  fi
done
echo "[encode] posters wired into index.html"
