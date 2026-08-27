---
type: reference
tags: [backup, archiving, workflow, storage, data-safety]
updated: 2026-08-27
---

# Archiving and Backup

Protecting and organising image files. Non-negotiable for a working photographer — a lost card or dead drive can lose a paid job and your reputation.

## 3-2-1 rule
- **3** copies of every file.
- **2** different media types.
- **1** copy offsite / in the cloud.

## On-site safety
- Shoot to **dual card slots** in backup/record-redundant mode where the body supports it.
- If single-slot, offload to a second drive before formatting.
- **Never format a card until it's backed up and verified.** No exceptions.
- Carry spare formatted cards; rotate, don't reuse mid-shoot. See [[photo-gear-and-settings]].

## Ingest workflow
1. Copy from card to working drive.
2. **Verify** the copy (checksum ingest via Lightroom / Photo Mechanic).
3. Back up to second location.
4. Only then format the card.

Consistent folder structure: `Year / Client / YYYY-MM-DD_Address-Job`. Same every time so you can find anything.

### Per-camera subfolder labeling — **non-negotiable, every job**
Inside every job folder, one subfolder per camera/device used, plus one `Selects` folder:

```
Client | Job Name/
├── {Camera Model} - {File Count} Files ({Size})/
├── {Camera Model} - {File Count} Files ({Size})/
├── ...one per device used on the job...
└── Selects/
```

- **Name format:** `{Camera Model} - {N} Files ({Unit} {Value})` — e.g. `A7R5 - 370 Files (GB 47)`, `A7S3 - 98 Files (GB 73.5)`, `Mavic 4 Pro - 5 Files (MB 274)`.
- **Camera Model** = short device name as it'd appear on the body/product (A7R5, A7S3, Mavic 4 Pro, etc.) — not a serial number or generic "Drone"/"Camera".
- **File Count** = exact item count for that folder (matches Finder's "for N items").
- **Size** = the folder's actual size, unit chosen by magnitude — `GB` once the folder is ≥1GB, `MB` below that (don't force GB for a 274MB drone folder). Value is the rounded number Finder's Get Info shows — no need to hand-calculate, just read it off Get Info and drop it in.
- **`Selects`** = the curated picks folder, always present even before culling starts (create empty, fill as you go).
- One subfolder per **physical device**, not per card or per session — if the A7R5 shot across two cards on the same job, one `A7R5 - ... Files (...)` folder, merged.

This is what makes a job folder instantly readable — camera, volume, and curation status at a glance — without opening anything. Applies to every ingest, every job, no exceptions.

## Lightroom catalog hygiene
- Back up the catalog + previews (catalog holds all edits/metadata — losing it loses your work).
- Set catalog backup on exit.
- Keyword and use collections per job so selects are findable.
- Keep catalog on a fast local drive, backed up like any file.

## Zipping — 30-day minimum age, non-negotiable
Never zip a job folder for archive/delivery until it's **at least 30 days old** (last-touched date, not creation date — check newest file inside, not just the folder mtime). A job under a month old may still be in active edit/revision; zipping locks it in too early. Enforced by the `zip-job-folder` skill (`~/.claude/skills/zip-job-folder/`), which hard-refuses under 30 days and requires Hunter to name the specific folder to override.

Once zipped and verified in `TO BE UPLOADED | DON'T DELETE`, the original source folder moves to Bin (Finder trash, not a permanent delete) — only after the zip is confirmed good. Never trash the source before the zip is verified.

## Delivery archive
- Keep final selects + master edits per job (see [[deliverables-and-export]]).
- RAW retention policy — decide how long you hold RAWs (e.g. keep selects' RAWs indefinitely, purge rejects after delivery + a grace period).
- Archive is your reshoot insurance and future-licensing library.

## Cloud / offsite
- NAS for local redundancy + working archive.
- Cloud (Backblaze / cloud drive) for the offsite copy.
- Automate it — manual backups get skipped.
- Delivery uploads off an SSD to the client Drive: [[rclone-drive-upload]] (fast, no local-copy bottleneck).

## Verify periodically
A backup you never test isn't a backup. Periodically restore a random job and confirm it opens. Check drive health (SMART). Replace ageing drives before they fail.

## Related
[[architectural-photography]] · [[photo-gear-and-settings]] · [[deliverables-and-export]] · [[photo-editing-pipeline]] · [[rclone-drive-upload]]
