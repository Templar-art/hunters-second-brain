# Contract rules
Templates are proposed contracts to adapt to existing types. Only the included review/timeline/geometry functions implement selected checks. Do not infer full JSON Schema validation for every file.

- Source and project/clip IDs unique and resolvable; no fabricated paths/hashes/permissions.
- Source duration/ranges finite, nonnegative, within actual media. Timeline mapping supports constant positive rate, not ramps. Source bounds against actual media need probe validation in the project.
- Explicit source/audio/timeline clocks and offsets; never silently assume identical origins.
- Caption phrase times finite and ordered; overlap and accessibility policies set per project.
- Approval defaults pending; candidate preference cannot activate without recorded human approval.
- Review scores null or 1–5 with required evidence modality. No aggregate score authorises delivery.
- Every issue has version/time/scene/evidence/fix/preserve scope.
- Face/region coordinates name their coordinate space. Raw detector output is not approved safe geometry.
- Actual runtime validators and regression tests must be added around project adapters; a template is not a working safety check.
