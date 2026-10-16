# Evaluation and learning loop

## Evidence declaration
Declare access to stills, temporal video, audio listening, audio measurements, transcript, layout metadata and source footage. These differ. No motion/editing score without temporal evidence, no audio-quality score without listening, no visual score from transcript alone.

## Technical checks
Render success; required assets/fonts; source bounds; actual delivery settings; caption event ordering/sync; overflow where measured; protection intersections where supplied; audio analysis where implemented. PASS / FAIL / NOT_ASSESSED, with command/evidence and scope. An unimplemented check remains unassessed.

## Creative rubric
Score supported categories 1–5 or null: message, hierarchy, typography, motion, editing, graphic relevance, brand fit, audio. 1 materially weak; 3 functional; 5 polished relative to brief. Do not average away missing evidence. Scores are subjective aids, not conversion predictions or delivery authorisation.

## Findings
Version + scene + timeline range + severity (blocker/important/preference) + observed problem + effect + actual evidence + proposed fix + preserve list + confidence. Prioritise all blockers then at most three creative fixes. Fresh evaluator context can reduce intention bias but does not remove shared model bias.

## Revision
At most two automatic creative passes initially, with configured compute budget and finite technical retry cap. Preserve approved typography/audio/cuts as directed. Re-render affected windows and regressions. Stop on uncertainty, no improvement, budget exhaustion or unresolved approvals. No endless self-scoring or broad restyling.

## Human feedback
Use templates/feedback.json or plain language. Bind note to version/time/scene/source anchors; remap notes after recuts rather than blindly using stale timecodes. Report each note's resolution with evidence.

## Taste memory
Candidate → proposed → human approved → active within scope → revised/retired. Scope: moment, video, client, global candidate. Repeated feedback may trigger a proposal, not automatic global change. Save exceptions, reason, source notes and good/bad examples. Avoid dumping all histories into permanent context.

## Delivery gate
No unresolved blockers, verified export and explicit human approval. No auto-publishing. Claims/consent and aesthetic QA are separate from legal/medical/platform-policy certification.
