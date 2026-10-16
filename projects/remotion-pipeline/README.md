# Remotion editing pipeline (kit)

Python + ffmpeg helper kit Hunter supplied for an AI-assisted edit → caption → review pipeline feeding Remotion.

| Script | Purpose |
|---|---|
| `scripts/env_check.py` | Report node/npm/ffmpeg/GPU, Python modules, Remotion deps |
| `scripts/transcribe.py` | faster-whisper transcription with word timestamps + VAD (needs a local model) |
| `scripts/timeline.py` | Map source word timings onto the edited timeline; build caption phrases |
| `scripts/audio.py` | Loudness analyse, voice/music sidechain mix, two-pass loudnorm master |
| `scripts/face_detect.py` | MediaPipe face boxes for caption placement (needs model file) |
| `tests/test_timeline.py` | 20 unit tests — `python3 -m unittest discover -s tests` |
| `templates/` | Example JSON shapes: source clip, edit decision, timeline input, review, style rule |
| `test-results/` | Results from the original environment (28 Node tests; the `.mjs` code itself was not supplied) |

`media/`, `work/`, `models/`, `node_modules/`, `out/` are git-ignored — footage never goes in the repo.

## Setup
```
pip install faster-whisper   # plus opencv-python mediapipe for face_detect
```
A whisper model must be downloaded from Hugging Face (`huggingface.co`, `cdn-lfs.huggingface.co`, `cas-bridge.xethub.hf.co`) — these must be on the cloud environment's allowed domains.
