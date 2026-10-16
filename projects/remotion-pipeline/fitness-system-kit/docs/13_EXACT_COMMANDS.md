# Command cookbook
Run from the extracted kit folder unless indicated otherwise. Adapt paths, interpreter and project manager to the real environment. Obtain required installation/model-download approval.

## Read-only audit, no installation
```
python scripts/doctor.py --project /YOUR/EXISTING/PROJECT --output new-doctor.json
node --test tests/node.test.mjs
python -m unittest discover -s tests -p 'test_*.py' -v
```

## After isolated dependency setup and model approval
```
python scripts/analyse_media.py /PATH/coach.mp4 /PATH/NEW_analysis_run --source-id coach001 --model small --allow-model-download --language en
```
If start timestamps are unavailable it deliberately stops; supply a verified `--audio-offset` rather than guessing. `--audio-stream-index` is the GLOBAL ffprobe stream index. The wrapper extracts/analyses only; it does not edit or render. A prepared local model path avoids authorising a download. CPU int8 is default; GPU requires the correct environment.

## Timing smoke test (no model required)
```
python scripts/timeline.py templates/timeline-input.json NEW_mapped.json
```
Replace fixture content with actual canonical analyses/clips. Don't mistake fixture timestamps for real word alignment.

## Optional face observations
```
python scripts/detect_faces.py VALIDATED_CFR_VIDEO.mp4 LOCAL_MODEL.tflite NEW_faces.json --every 1
```
Requires a separately tested vision environment. Output remains unapproved source-coordinate observations until transformed/reviewed.

## Audio
```
python scripts/audio_tools.py analyse REAL_MIX.wav NEW_analysis.json
python scripts/audio_tools.py mix DIALOGUE.wav LICENSED_MUSIC.wav NEW_mix.wav --music-db -22
```
For mastering choose actual delivery targets, then use `master ... --integrated TARGET --true-peak CEILING --lra RANGE`. No universal master target is prescribed. Test values in evidence are not your delivery specification.

## Rendering
Merge DemoRegistration into your EXISTING Remotion Root, inspect project scripts and installed APIs, then render FitnessMotionDemo through that project's existing commands/Studio. No universal render command is supplied because entry points differ. Preserve matching Remotion package versions. After a specimen, render the real pilot.

## Evidence and bounded revision
```
node code/evidence-manifest.mjs EXISTING_PREVIEW.mp4 NEW_manifest.json
node code/revision-runner.mjs REVIEWED_LOCAL_CONFIG.json
```
Runner commands must already exist in your project. It supplies control flow, not an LLM API or autonomous critique. The evaluator must refresh actual evidence after every revision; version-string equality alone does not prove freshness. Never execute an untrusted config.
