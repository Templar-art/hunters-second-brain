#!/bin/bash
# Process one video:  ./run.sh "/path/to/My Video.mp4"  [--sfx "/path/to/SFX"] [--test-seconds 20] [--seed 3]
cd "$(dirname "$0")" || exit 1
PY=python3
[ -x .venv/bin/python ] && PY=.venv/bin/python
if [ $# -eq 0 ]; then
  echo 'Usage: ./run.sh "/path/to/video.mp4" [--sfx "/path/to/SFX folder"] [--test-seconds 20]'
  exit 1
fi
exec "$PY" sounddesign.py process "$@"
