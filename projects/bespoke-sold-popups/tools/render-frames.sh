#!/bin/zsh
# Render the pop-up animation to an MP4: one headless Chrome per frame, 6 at a time.
#
#   tools/render-frames.sh [169|916] [outdir]
#
# Why not drive one browser over CDP? Page.captureScreenshot wedges as soon as the
# page's animations are paused, which is exactly what freezing a frame does.
# Needs the `bespoke-popups` server running (http://localhost:8773).
# Don't pass --user-data-dir: a shared profile serialises the launches and it crawls.
set -e
AR=${1:-169}
OUT=${2:-/tmp/bespoke-popups-$AR}
[[ $AR == 169 ]] && { W=1920; H=1080 } || { W=1080; H=1920 }
FPS=15; STEP=$(( 1000 / FPS ))
HOLD=12                    # frames of settled hold after each scene (~0.8s)
JOBS=6

SEQ="$OUT/frames"; rm -rf "$OUT"; mkdir -p "$SEQ"

# scene:last-ms — motion only; the static hold is padded afterwards
SCENES=(1:2300 2:1500 3:4000)

# build the shot list: <outfile> <scene>:<ms>
LIST="$OUT/shots.txt"; : > "$LIST"
i=0
for s in $SCENES; do
  scene=${s%%:*}; end=${s##*:}
  ms=0
  while (( ms <= end )); do
    printf "%s %s:%s\n" "$(printf "%04d" $i)" "$scene" "$ms" >> "$LIST"
    ms=$(( ms + STEP )); i=$(( i + 1 ))
  done
  # placeholder rows for the hold — filled by copying the settled frame
  for h in {1..$HOLD}; do
    printf "%s HOLD\n" "$(printf "%04d" $i)" >> "$LIST"
    i=$(( i + 1 ))
  done
done

export SEQ W H AR
shoot () {
  local name=$1 frame=$2
  [[ $frame == HOLD ]] && return 0
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless=new --disable-gpu --hide-scrollbars --no-first-run \
    --force-device-scale-factor=1 --window-size=$W,$H \
    --screenshot="$SEQ/$name.png" \
    "http://localhost:8773/popups.html?frame=$frame&ar=$AR&bg=plate" >/dev/null 2>&1
}
functions -t shoot >/dev/null 2>&1 || true

grep -v HOLD "$LIST" | xargs -n 2 -P $JOBS zsh -c '
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless=new --disable-gpu --hide-scrollbars --no-first-run \
    --force-device-scale-factor=1 --window-size='$W','$H' \
    --screenshot="'$SEQ'/$0.png" \
    "http://localhost:8773/popups.html?frame=$1&ar='$AR'&bg=plate" >/dev/null 2>&1
'

# fill the holds by copying the last real frame before each run of HOLDs
prev=""
while read -r name frame; do
  if [[ $frame == HOLD ]]; then cp "$SEQ/$prev.png" "$SEQ/$name.png"
  else prev=$name
  fi
done < "$LIST"

ffmpeg -y -v error -framerate $FPS -i "$SEQ/%04d.png" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -r 30 "$OUT/popups-$AR.mp4"
echo "$(ls "$SEQ" | wc -l | tr -d ' ') frames -> $OUT/popups-$AR.mp4"
