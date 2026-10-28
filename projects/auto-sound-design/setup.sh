#!/bin/bash
# One-time setup on a Mac. Checks first, and asks before installing anything.
cd "$(dirname "$0")" || exit 1

ask() { read -r -p "$1 [y/N] " reply; [[ "$reply" =~ ^[Yy] ]]; }

echo "== Auto Sound Design setup =="

if ! command -v python3 >/dev/null; then
  echo "python3 is missing. Install Apple's command line tools with: xcode-select --install"
  exit 1
fi
echo "python3: $(python3 --version)"

if ! command -v ffmpeg >/dev/null || ! command -v ffprobe >/dev/null; then
  echo "FFmpeg is missing. It reads your video and audio files."
  if command -v brew >/dev/null; then
    if ask "Install it now with Homebrew (brew install ffmpeg)?"; then
      brew install ffmpeg || exit 1
    else
      echo "Skipped. Run: brew install ffmpeg"; exit 1
    fi
  else
    echo "Homebrew isn't installed either. See https://brew.sh, then run: brew install ffmpeg"
    exit 1
  fi
fi
echo "ffmpeg: $(command -v ffmpeg)"

if [ ! -x .venv/bin/python ]; then
  echo "This tool needs numpy (number crunching) and lxml (checks the Final Cut XML)."
  echo "They go in a private folder here (.venv), not your system Python."
  if ask "Create .venv and install numpy + lxml (about 30 MB download)?"; then
    python3 -m venv .venv && .venv/bin/pip install --quiet --upgrade pip && .venv/bin/pip install --quiet numpy lxml || exit 1
  else
    echo "Skipped."; exit 1
  fi
fi

.venv/bin/python sounddesign.py check
echo
echo "Setup done. Next: ./run.sh \"/path/to/your video.mp4\" --sfx \"/path/to/your SFX folder\""
