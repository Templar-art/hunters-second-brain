# Cloud session setup (Claude Code on the web)

How to recreate the working environment in a fresh cloud session. The Mac setup is in README.md.

## What the cloud container already has (checked 28 Oct 2026)
- Ubuntu Linux, 4 CPUs, 15 GB RAM, Python 3.13
- FFmpeg / FFprobe 6.1.1, numpy 2.x, lxml, xmllint: everything the tool needs
- No GPU, no Final Cut Pro, and no access to Hunter's Mac or phone files

## Install steps (all small, no paid services)
```
cd projects/auto-sound-design
python3 sounddesign.py check          # confirms ffmpeg/ffprobe/numpy/lxml
pip install --break-system-packages yt-dlp   # optional, ~3 MB, for reference videos
python3 -m unittest discover -s tests
```

## Network limits
- **youtube.com / www.youtube.com / googlevideo.com are blocked** by this environment's network policy (proxy 403), so yt-dlp can't fetch YouTube references. Either allow those domains in the environment's network settings, or upload the reference video file into the chat.
- PyPI works (pypi.org, files.pythonhosted.org).

## Getting files in and out
- **In:** attach a video in the Claude app chat. It lands in `/root/.claude/uploads/<session>/`. Copy it to `input/`, which is git-ignored.
- **Out:** results are written to `output/` (git-ignored) and sent back through the chat.
- **SFX available in the repo:** `projects/committed-coaching/sfx-lib/` (curated Ocular trims) and `projects/use-definitions/sfx-lib/`. The full Ocular library (`~/Music/SFX Library`) is only on the Mac.

## Never in git
Videos, audio renders, `output/`, `input/`, `sfx/`, `.venv/`, `asd.local.json`, and API keys (environment variables only).
