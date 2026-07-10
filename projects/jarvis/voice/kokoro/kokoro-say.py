#!/usr/bin/env python3
"""Jarvis TTS via Kokoro. Usage: kokoro-say.py "text" [voice]. Speaks aloud."""
import subprocess
import sys
import tempfile
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro

HERE = Path(__file__).parent
DEFAULT_VOICE = "bm_george"


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    voice = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_VOICE
    if not text.strip():
        return
    kokoro = Kokoro(str(HERE / "kokoro-v1.0.onnx"), str(HERE / "voices-v1.0.bin"))
    samples, sample_rate = kokoro.create(text, voice=voice, speed=1.0)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, samples, sample_rate)
        subprocess.run(["afplay", f.name], check=False)
        Path(f.name).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
