"""Word-level transcript → words.json ([{w, s, e}]). Usage: transcribe.py <audio.wav> <out.json>"""
import json, sys, wave
import numpy as np
from faster_whisper import WhisperModel

src, dst = sys.argv[1], sys.argv[2]
audio = np.frombuffer(wave.open(src).readframes(10**9), dtype="int16").astype("float32") / 32768
segs, _ = WhisperModel("small.en", compute_type="int8").transcribe(audio, word_timestamps=True)
words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in s.words]
json.dump(words, open(dst, "w"), indent=0)
print(f"{len(words)} words → {dst}")
