# Troubleshooting and honest fallbacks

- No faster_whisper module: activate the approved analysis environment or use its interpreter directly. Do not pip-install globally to fix a path mistake.
- Model unavailable offline: provide an actual local model directory/cache and inspect local-files-only behaviour. Do not bypass download approval.
- CUDA/cuDNN/CTranslate2 errors: compare upstream requirements against installed GPU stack. Use CPU int8 to prove wiring rather than randomly downgrading the main environment.
- Optional packages conflict: isolate vision/alignment in separate environments and exchange JSON contracts. Do not force every tool into one Python environment.
- Wrong captions: review transcript, selected language, audio quality and timing origin. Correct terminology with approved context, then realign/review timings. Do not invent confident word times.
- Music ducks at the wrong point: inspect source audio offset, edit trims, reordering, playback rate and sequence-local frame resets. Verify shared timeline clock.
- Empty/low-confidence face detections: keep review required; inspect crop/blur/profile/occlusion and annotate manually. Never place text into an uncertain face region automatically.
- Caption overlaps during entrance: measure full motion envelope/backplate after font load, not just settled text. Simplify if no feasible anchor.
- FFmpeg missing filter: inspect version/build; do not claim feature support from executable presence. Retain source and use a compatible authorised build.
- Mix technically passes but sounds bad: use actual listening and source comparison. Reduce processing, change music, adjust arrangement; measurements alone cannot settle taste.
- Render flicker: check async font/media readiness, nondeterminism, parallel state and installed-version APIs. Workarounds are not root-cause proof.
- Critic gives generic praise: require timecoded evidence, supported modalities and comparison to the brief; never ask it to approve itself.
- Endless edits: stop at pass/budget cap and show a specific unresolved choice. More variants are not inherently progress.
