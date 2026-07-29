#!/bin/zsh
# Render the pop-up animation, one headless Chrome per frame, 6 at a time.
#
#   tools/render-frames.sh [169|916] [outdir] [plate|none|black|green|key]
#
# bg = none  -> transparent PNGs + ProRes 4444 .mov (alpha, drop straight on your footage)
# bg = plate -> the test still behind the type + H.264 .mp4 (preview only)
#
# Why not drive one browser over DevTools Protocol? Page.captureScreenshot never returns
# once the page's animations are paused, which is exactly what freezing a frame does.
# Don't pass --user-data-dir either: a shared profile serialises the launches and it crawls.
# Needs the `bespoke-popups` server running (http://localhost:8773).
set -e
AR=${1:-169}
OUT=${2:-/tmp/bespoke-popups-$AR}
BG=${3:-none}
[[ $AR == 169 ]] && { W=1920; H=1080 } || { W=1080; H=1920 }
FPS=15; STEP=$(( 1000 / FPS ))
HOLD=12                    # frames of settled hold after each scene (~0.8s)
JOBS=6

# transparent base layer for alpha renders
[[ $BG == none ]] && ALPHA=(--default-background-color=00000000) || ALPHA=()

SEQ="$OUT/frames"; rm -rf "$OUT"; mkdir -p "$SEQ"

# scene:last-ms — motion only; the static hold is padded afterwards
SCENES=(1:2300 2:1500 3:4000)

LIST="$OUT/shots.txt"; : > "$LIST"
i=0
for s in $SCENES; do
  scene=${s%%:*}; end=${s##*:}
  ms=0
  while (( ms <= end )); do
    printf "%s %s:%s\n" "$(printf "%04d" $i)" "$scene" "$ms" >> "$LIST"
    ms=$(( ms + STEP )); i=$(( i + 1 ))
  done
  for h in {1..$HOLD}; do
    printf "%s HOLD\n" "$(printf "%04d" $i)" >> "$LIST"
    i=$(( i + 1 ))
  done
done

grep -v HOLD "$LIST" | xargs -n 2 -P $JOBS zsh -c '
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless=new --disable-gpu --hide-scrollbars --no-first-run '"${ALPHA[*]}"' \
    --force-device-scale-factor=1 --window-size='$W','$H' \
    --screenshot="'$SEQ'/$0.png" \
    "http://localhost:8773/popups.html?frame=$1&ar='$AR'&bg='$BG'" >/dev/null 2>&1
'

# fill the holds by copying the last real frame before each run of HOLDs
prev=""
while read -r name frame; do
  if [[ $frame == HOLD ]]; then cp "$SEQ/$prev.png" "$SEQ/$name.png"
  else prev=$name
  fi
done < "$LIST"

if [[ $BG == none ]]; then
  # ProRes 4444 keeps the alpha channel; FCP and Resolve both read it directly
  ffmpeg -y -v error -framerate $FPS -i "$SEQ/%04d.png" \
    -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -alpha_bits 16 \
    -r 30 "$OUT/popups-$AR-alpha.mov"
  # VP9/webm alpha as well, for anything web-side
  ffmpeg -y -v error -framerate $FPS -i "$SEQ/%04d.png" \
    -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 4M -r 30 "$OUT/popups-$AR-alpha.webm"
  echo "$(ls "$SEQ" | wc -l | tr -d ' ') frames -> $OUT/popups-$AR-alpha.mov (+ .webm, + PNG sequence in frames/)"
else
  ffmpeg -y -v error -framerate $FPS -i "$SEQ/%04d.png" \
    -c:v libx264 -pix_fmt yuv420p -crf 18 -r 30 "$OUT/popups-$AR.mp4"
  echo "$(ls "$SEQ" | wc -l | tr -d ' ') frames -> $OUT/popups-$AR.mp4"
fi
