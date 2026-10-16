# Motion library and intentional transitions
Twelve original starter components are supplied in code/components.mjs. They are not brand replicas or final designs. Test each needed component in the actual project before adopting it.

Components: HookStatement, PhraseCaptions, ContrastStatement, WeeklyProgramme, ExerciseLabel, TechniqueCallout, MetricComparison, CoachingProcess, TestimonialQuote, TrainingSectionMarker, OfferEndCard, EvidencePanel.
TechniqueCallout is manual/static, not automatic tracking. Metrics and testimonials require factual records/permission in the workflow. EvidencePanel never creates fake proof. System fonts are placeholders. No auto-fit, face detector or measurement is secretly embedded in these components.

## Motion grammar
Start with a strong static frame. Use short purposeful entrances, readable holds and quiet exits. At 30fps an 8–14 frame entrance and 2–4 frame stagger may be reasonable trials, not universal timings. Preserve intent across fps. Every animation must derive from frame/input data, not CSS keyframes, real-time timers or previous-frame state.

## Transition recipes
1. J-cut/audio lead: next coaching thought begins over relevant B-roll, then return to speaker. Preserve meaning; no default whoosh.
2. Movement match: select genuinely compatible action/direction; cut at meaningful movement. Requires footage inspection.
3. Phrase-to-programme: spoken key concept becomes a schedule title; reveal only useful supplied sessions. Preserve required captions/accessibility.
4. Divider-to-card: a small line establishes an information region; content resolves after the container. Keep all states outside protected regions.
5. Milestone punctuation: original licensed object or typography for real achievement; rare, restrained sound and motion. Complex CG needs a separate asset pipeline.
6. Hard cut/quiet hold: strongest option when performance or message needs no decoration.

## Required transition fields
fromScene, toScene, editorialReason, visualMechanism, timing, audioAction, protectedRegions, preserveList. If the only reason is random variation, use a clean cut or justify the stylistic choice explicitly.

## Test fixtures
Longest text, absent optional fields, 24/30/60fps, target aspect ratios, start/mid/end, font readiness, animated path bounds, footage contrast. Include approved/rejected renders in the library; specifications alone are not quality proof.
