# Jarvis — Phase 2 Design (Job State Tracking)

**Date:** 2026-07-10
**Status:** Approved by Hunter
**Owner:** Hunter / Claude
**Predecessor:** [Phase 1 design](2026-07-10-jarvis-phase1-design.md)

## Gap

Job state (what's generated, approved, delivered, spent) lives in Hunter's head and in folder contents. No session can answer "where's the Salisbury job" or resume a job cold. Phase 2 closes exactly this: **track**. Query/resume/brief-integration are explicitly out of scope — they become trivial later because tracked state exists.

## Design

### JOB.md — one per job folder, created at intake

- **Frontmatter:** `client`, `address`, `opened` (ISO date), `status` (`intake → generating → review → delivered`), `cost` (`{ credits, aud }`).
- **Shots table:** shot number, name, pipeline (`full-frame` | `masked` | `video`), status (`todo` | `generated` | `approved` | `redo`), notes.
- **Log:** append-only dated one-liners (generations, approvals, credit spends, decisions).

### Template

`projects/jarvis/JOB-template.md` — copied into the job folder at intake, placeholders filled.

### Enforcement — two layers (10x-ai skill is vendored read-only, cannot be edited)

1. **Vault CLAUDE.md rule:** any 10x job session creates JOB.md at intake and updates it on every state change — generation, approval, redo, delivery, every credit spent. Cost tally always current.
2. **Auto-memory entry** (cross-project): same rule for job sessions running outside this vault (Desktop job folders etc.).

### Update rules

- `status: delivered` closes the job; the file stays as the record.
- A cold session must be able to state job progress and cost from JOB.md alone.

## Success criteria

Every job started after 2026-07-10 has a JOB.md accurate enough that a fresh session could resume it — even though resume isn't built yet.

---
_Vault: [[jarvis]]_
