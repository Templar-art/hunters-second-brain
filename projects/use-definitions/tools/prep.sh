#!/bin/zsh
# Prepare a new episode from a raw talking-head clip.
# Usage: tools/prep.sh <clip.mp4> <episode-name> [a-b ...]   (optional: only cut out Sam in these second ranges)
# Makes episodes/<name>/ with source.mp4, build/frames (30fps 1080x1920), build/matte, build/meta.json, words.json.
set -e; ROOT="${0:a:h:h}"; CLIP="$1"; EP="$ROOT/episodes/$2"
[[ -f "$CLIP" && -n "$2" ]] || { echo "usage: prep.sh <clip.mp4> <episode-name>"; exit 1; }
VENV="$ROOT/.venv"; [[ -x "$VENV/bin/python" ]] || { python3 -m venv "$VENV"; "$VENV/bin/pip" -q install -r "$ROOT/tools/requirements.txt"; }
[[ -d "$ROOT/tools/node_modules/playwright" ]] || (cd "$ROOT/tools" && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm i -s)
mkdir -p "$EP/build/frames"
cp "$CLIP" "$EP/source.mp4"
# frames: scale/crop to 9:16 1080x1920, 30fps
ffmpeg -v error -y -i "$EP/source.mp4" -vf "fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920" -q:v 2 "$EP/build/frames/f%04d.jpg"
echo "{\"frames\": $(ls "$EP/build/frames" | wc -l | tr -d ' ')}" > "$EP/build/meta.json"
ffmpeg -v error -y -i "$EP/source.mp4" -ar 16000 -ac 1 "$EP/build/vo16k.wav"
[[ -f "$EP/words.json" ]] || "$VENV/bin/python" "$ROOT/tools/transcribe.py" "$EP/build/vo16k.wav" "$EP/words.json"
"$VENV/bin/python" "$ROOT/tools/facetrack.py" "$EP/build"
"$VENV/bin/python" "$ROOT/tools/matte.py" "$EP/build" "${@:3}"
[[ -f "$EP/episode.js" ]] || cp "$ROOT/episodes/crud/episode.js" "$EP/episode.js"
echo "ready: $EP  (edit episode.js, then tools/build.sh $2)"
