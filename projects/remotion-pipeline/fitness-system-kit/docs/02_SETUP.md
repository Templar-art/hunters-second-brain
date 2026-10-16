# Environment and dependency setup

## Inspect before install
Run `python scripts/doctor.py --project /path/to/existing/project --output doctor.json` using an existing Python. The doctor is read-only apart from its report; it does not install/download anything. Inspect current node/package-manager versions, lockfiles, Remotion package alignment, Python, FFmpeg and hardware.
Use a Python 3.11 virtual environment as a conservative starting proposal, subject to actual wheel availability and existing project constraints. faster-whisper itself documents Python 3.9+; optional packages can have narrower requirements. Do not force the current project into a new runtime just to match this document.

## Core local baseline
- Claude Code already connected to the repository.
- Node and existing package manager compatible with installed Remotion.
- Existing React/Remotion app; reuse its versions and render scripts.
- FFmpeg AND ffprobe installed as OS executables. faster-whisper can decode via PyAV without system FFmpeg, but this pipeline still needs FFmpeg for extraction, mixing and measurement.
- Isolated Python environment with faster-whisper.
- Explicitly approved model download and local model cache.

## macOS / Linux shell example (after approval)
```
python3.11 -m venv .venv-video
source .venv-video/bin/activate
python -m pip install -r fitness-system-kit/requirements/core.in
```
On Windows use an installed compatible Python, `py -3.11 -m venv .venv-video`, then `.venv-video\Scripts\Activate.ps1` in PowerShell. Do not weaken execution policy globally; use the environment's Python executable directly if activation is blocked.
FFmpeg installation depends on OS/package manager and permissions. Inspect `ffmpeg -version` and `ffprobe -version` first; use the user's existing installer/package manager after approval. Do not execute an arbitrary downloaded shell script.

## CPU / GPU / Apple
CPU int8 is the portable baseline, not a speed promise. NVIDIA acceleration requires compatible CTranslate2/CUDA/cuDNN libraries; inspect the current upstream requirements and GPU before choosing versions. CUDA is not Apple GPU acceleration. On an Apple machine, baseline CPU is acceptable for proving correctness; evaluate a native backend separately only if needed, keeping the same contract.
Start with a smaller model for wiring tests, then compare an accuracy-oriented model on actual accents, gym noise and terminology. Do not claim model selection by name alone guarantees quality.

## Models and credentials
The transcription adapter requires `--model LOCAL_PATH` or explicit `--allow-model-download` for a model identifier. Initial model/VAD downloads may require network. Do not download a giant model silently. Core local operation needs no paid API. Optional diarisation may require a Hugging Face token and model access/terms; never hard-code credentials or log them.

## Optional dependencies
WhisperX alignment/diarisation: install in a separate environment first if required; it may conflict with Torch/CUDA stacks. Missing alignment timings remain flagged.
MediaPipe/OpenCV: needed for optional detector adapter plus a separately supplied model. Check Python/OS wheel support; separate vision env if necessary.
PySceneDetect: candidate scene boundaries, not best-take decisions.
librosa: beat/onset suggestions, not mandatory cuts.
Do not install all optional packages by default. Review licences/model terms for intended commercial use.

## Official Remotion skills
Inspect existing skills. Current documented command: `npx skills add remotion-dev/skills`. Obtain installation/download approval. Preserve project instructions and existing skill folders. Keep installed Remotion package versions aligned; do not blindly upgrade.

## Reproducibility
The .in files list intentionally unpinned starting dependencies, NOT a verified lockfile. After successful installation/smoke tests, save OS/architecture, Python/Node/FFmpeg versions and a resolved requirements lock from the isolated environment. Preserve current Node lockfile. Test a clean install before claiming reproducibility. Model names/revisions, source hashes and settings belong in each analysis manifest.
