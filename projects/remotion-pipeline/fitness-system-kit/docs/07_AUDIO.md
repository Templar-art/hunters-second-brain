# Audio production and approval

## Stems
Keep original dialogue, music, natural sound and designed accents separately when feasible. Preserve original media. Transcription WAV is analysis-only. Do not assume its mono/16kHz conversion is the final audio master.

## Dialogue
Prioritise intelligibility and consistent perceived level while retaining natural character. Denoise/de-reverb cautiously and compare against source. Watch clipped words, breaths, sibilance, edit clicks, harshness and pumping. No speech-restoration model is bundled; choose one only if the actual audio needs it and licensing/privacy permit.

## Music
Licensed assets only. Choose energy around the story, not a random track. Use purposeful starts/stops, phrase changes and quiet moments. libROSA beat estimates are candidates, not creative judgement. Never assume a popular social track is commercially licensed.

## Automation
code/audio-envelope.mjs supplies deterministic gain from mapped timeline speech intervals, with anticipation/release/fades. Numeric gain must use edited timeline seconds; Sequence-local frame resets need explicit offsets.
scripts/audio_tools.py provides local FFmpeg dialogue-sidechain mixing and analysis/mastering. Sidechain and transcript-envelope methods are alternatives; avoid accidental double-ducking. Default levels are trial settings, not delivery loudness targets. No model is listening in the envelope function.

## Sound design
Use natural training sounds where relevant, subtle UI accents for meaningful information changes, and silence where a point should land. No accent for every word or whoosh for every cut. Source sound must not imply false events/results.

## Mastering
Measure actual mix. Choose explicit integrated loudness, peak ceiling and range targets for the destination/client; do not enforce a universal social-media value. Two-pass loudnorm can fall back to dynamic behaviour when constraints cannot be satisfied: inspect actual output and settings. True-peak ceiling is a limit, not a goal every file must reach.

## Mandatory listening review
Full playback on headphones plus a representative phone/small speaker. Check speech under music, audible processing, transitions, tails, accents, sync and level consistency. A waveform or LUFS measurement does not establish good sound. Without listening evidence audio quality stays NOT_ASSESSED.
