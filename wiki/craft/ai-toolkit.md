---
type: moc
tags: [ai-generation, craft, moc, tooling]
updated: 2026-07-19
---

# AI Toolkit (generation as a craft)

The practical "which tool, which prompt, which model for which job" layer of 10x's AI generation work.

Routing, hard rules, and the money gate live in [[higgsfield-pipelines]] and [[staging-rules]] — those are the source of truth. This domain is the craft layer on top: tool selection, prompting patterns, and video generation.

## Child notes
- [[ai-image-tools]] — which AI image tool for which job (Higgsfield, Magnific, Freepik, Topaz).
- [[ai-video-tools]] — AI video generation for property/social.
- [[ai-prompting]] — prompting patterns distilled from the staging rules.

## Golden rules (recap — full rules in the linked concept notes)
- **Money gate** — no credit spend without Hunter's explicit go-ahead. Git is free; credits never are.
- **Route before generating** — full-frame generative for interiors/staging/renders/tight exteriors; masked inpaint for targeted edits on detail-heavy exteriors.
- **Never full-frame a drone wide** — it regenerates the ground and wrecks fine detail.
- **Renders vs real photos** — full-frame generate on renders only; real photos get Topaz upscale, never full-frame regeneration.

## Related
[[craft]] · [[higgsfield-pipelines]] · [[staging-rules]] · [[post-production]]
