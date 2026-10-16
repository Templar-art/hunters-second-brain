# Transcription, VAD and alignment

## Core adapter
scripts/transcribe.py wraps faster-whisper and its integrated Silero VAD. It saves source hash, source-audio offset, explicit model/device/compute settings, transcript segments, word timings/probabilities, timing-review flags and actual VAD regions. Probabilities are model outputs, not calibrated correctness guarantees. Model inference was not executed in this kit environment; run the real smoke test locally.

## Ingest
Probe first. Extract a selected audio stream to a separate 16kHz mono WAV for analysis; never replace the original mix with this file. Record the audio offset in the video timeline, including any trim/conform. Suggested command after checking stream choice:
`ffmpeg -n -i INPUT -map 0:a:0 -vn -ar 16000 -ac 1 -c:a pcm_s16le analysis.wav`
The exact offset is not always simply zero. Use stream/container timestamps and confirm a visible/audible sync point. Do not assume arbitrary extraction flags preserve the intended clock.

## Transcribe
`python scripts/transcribe.py analysis.wav analysis.json --source-id clip001 --audio-offset 0 --model small --allow-model-download --language en`
That model is a wiring-test example, not a final quality recommendation. Use --model LOCAL_PATH without download permission for a prepared local model. Supply verified offset instead of blindly copying zero. Output refuses overwrite.

## Caption/edit use
Review names, exercise terminology, numbers, units, negation and qualifications. Group semantic phrases; avoid emphasis on every word. VAD is a speech-likelihood signal, not a command to cut all silence. Preserve meaning, breaths and useful pauses. Original source timings remain immutable; map to the edit separately.

## Optional WhisperX
Use forced alignment when baseline word timing is insufficient, especially for tight phrase emphasis. WhisperX documents dictionary/alignment gaps, overlapping-speech limitations and imperfect diarisation. Do not invent missing word times. Separate speakers only for multi-speaker projects; avoid unnecessary diarisation costs/dependencies.

## Timeline mapping utility
scripts/timeline.py takes canonical words and explicit source-to-edit clip ranges. Partial words at trim boundaries are omitted AND flagged for review, not silently retimed as complete speech. Speed is constant per clip; speed ramps require a time-warp adapter. Duplicate/reordered source ranges are permitted. Regenerate captions/VAD mappings after recuts.

## Additional analysis
PySceneDetect: cut candidates, not semantic quality.
librosa: beat/onset candidates, not a mandate to cut every beat.
Vision: inspect relevance/framing/movement with capable tools or humans. Do not infer exercise correctness from transcript or arbitrary detector labels.
