# Architecture and source-of-truth rules

## Authority
Security/project rules > approved factual/client constraints > approved human feedback within scope > client brand > format rules > kit defaults. Human approval controls final delivery, publishing and activation of permanent taste rules.

## Stages
1. Intake: audience, objective, real assets, permission/rights, brand, target outputs.
2. Probe: media streams, timing origins, duration, fps/timebase, audio offset, hashes.
3. Analyse: transcript/word timing, VAD, optional alignment, shot candidates, protected-region observations, optional music timing.
4. Direct: one main message, relevant source selections, deliberate energy curve, graphic purposes and reference principles.
5. Plan: structured edit decisions, actual source ranges/rates, audio events, captions, transitions, layout decisions.
6. Assemble: existing Remotion components/pipeline; real assets and deterministic frame timing.
7. Evidence: preview, style frames, critical motion windows, technical tests and version manifest.
8. Evaluate: measurable integrity first, supported creative critique second, human review third.
9. Revise: targeted fixes, frozen approvals, at most two creative passes initially.
10. Learn: approved examples and narrowly scoped preference rules; stable benchmarks.

## Files and isolation
Keep client media/credentials in authorised local storage. Avoid giant binaries in Obsidian/chat/Git by default. An Obsidian vault can hold briefs, rules and review notes if already used; link to media rather than duplicate it. Never upload client footage to an external evaluator without consent.
Each project: brief.json, assets.json, analysis/, edit-plan.json, brand.json, evidence/, reviews/, approvals.json. Schema adaptations should preserve existing APIs rather than forcing migrations.

## Timing origins
Whisper and VAD output audio-relative seconds. Record audio stream start relative to the video stream start. Source scene ranges refer to video-relative time. Add that audio offset before mapping into a trim/reordered timeline. Frame/sample conversions must be explicit. Variable-frame-rate footage needs real PTS or an approved conform with a verified mapping, not index/fps guesses.

## Analysis reuse
Cache by source content hash + model/version/settings + timing-origin policy. Changing the cut invalidates mapped captions/ducking/placements, not necessarily the source transcript. Changing transcript wording can invalidate alignment. Manual face regions must stay attached to source/scene coordinates and versions.

## Completion
No checklist counts as an implemented test. No transcript counts as footage inspection. No compile counts as a visual pass. No still counts as temporal/audio review. Human approval is required even when automated checks are green.
