---
type: reference
tags: [backup, archiving, workflow, storage, data-safety]
updated: 2026-07-19
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

## Lightroom catalog hygiene
- Back up the catalog + previews (catalog holds all edits/metadata — losing it loses your work).
- Set catalog backup on exit.
- Keyword and use collections per job so selects are findable.
- Keep catalog on a fast local drive, backed up like any file.

## Delivery archive
- Keep final selects + master edits per job (see [[deliverables-and-export]]).
- RAW retention policy — decide how long you hold RAWs (e.g. keep selects' RAWs indefinitely, purge rejects after delivery + a grace period).
- Archive is your reshoot insurance and future-licensing library.

## Cloud / offsite
- NAS for local redundancy + working archive.
- Cloud (Backblaze / cloud drive) for the offsite copy.
- Automate it — manual backups get skipped.

## Verify periodically
A backup you never test isn't a backup. Periodically restore a random job and confirm it opens. Check drive health (SMART). Replace ageing drives before they fail.

## Related
[[architectural-photography]] · [[photo-gear-and-settings]] · [[deliverables-and-export]] · [[photo-editing-pipeline]]
