# T16 retrospective: the cloud sync core (#663)

Phase 3 of the code-auditor method: what the record of these 14 files
says about how they came to be, before `04` judges them. It is about the
*area*; the slice's own retro is written at stage G
(`docs/retros/<date>-m6-cloud-sync-core.md`).

## The shape of the history

- **151 commits all-time**, every one after the first a fork identity (run r25). The first, `9f1fab30f6`, is ROCKNIX's import of 2025-07-13.
- **By month:** 2025-07 to 2025-10: 6; 2026-07: 7; 2026-08: 14; **2026-09: 110**; 2026-10: 14. The September burst is the release-candidate rounds and the two audits of them (#307, #308, and "the audit of the fixes").
- **Since the base the 14 are +6,976 / -338** (run r20). Five files are new since then: the capture, `cloud_net_ready`, `cloud_saves_root`, the settings-archive helper and the boot hook.
- **Upstream has not touched the directory since the base** (run r19), so nothing here is a merge risk: the next base merge brings none of it.
- **The issues the commits cite most** (subjects): #21 (the save manifest), #141 (bucket presence), #99 (the sentinel exits), #94 (the startup sync moved into ES), #86 (the device id), #83 (the saves root's card), #192, #153 (the deliberate ceiling), #143 (the listing bound), #127, #103.

## What the code itself records

The scripts carry their history as comments, at a density no other slice
has: most functions open with the incident that made them. The comments
are the authors' claims (blindspot 31). Where `02` checked one against the
code, two were stale:
- `cloud_backup:69-71` says neither sentinel writes a stamp, while a 69 from a run the network cut does;
- `102-cloud-saves:44` says the capture takes no lock, while it takes `.capture.lock` since PL-067.

The pattern is blindspot 72's: a comment held an invariant the code had
stopped keeping.

## The recurring classes, from the blindspot register and the code's own comments

- **Success over a no-op** (blindspots 13, 33): `cloud_restore`'s `backup/*.zip` filter, the sentinel 3 and 4 borrowed from rclone, the size-only remote. Each fix in the code is a positive check: `rules_whole`, the size check before the upload marker, 75 and 69 above rclone's range.
- **A guard that falls open when its machinery breaks** (blindspot 22): `ls A B`'s status, the pipeline's last stage, the unquoted list. The read finds two more of the shape (`02` § Leads 1 and 8).
- **Two copies of one thing** (blindspot 28; the copy-twins):
  - the twins share 39 functions, 34 of them byte for byte;
  - `conf_valid` is a third copy in the helper;
  - the conf has two readers that disagree on a value all three copies of the gate pass (`02` § The configuration).
- **Fixed forward, not backward** (blindspots 10, 62): the helper's one-shot edits are the backward half (BACKUPMETHOD to copy, the retry counts, the stamp renames), each guarded by its own marker file.

## Decisions the read found implemented

- **D-CLOUD-109 / D-CLOUD-130, not D-CLOUD-076.**
  - The scripts have no launch-cancel path.
  - An automatic run is bounded from its start (`SYNC_DEADLINE`, the `rclone()` wrapper's `timeout -k 3 <left>`) and ends with an outcome, not a cancel.
  - The question STOP IT AND PLAY / KEEP WAITING is EmulationStation's (named, not read).
- **D-CLOUD-078, the last known good:** the stamps are temp-and-rename; the upload marker only after the size check; the retention only after it; the `.bak` copies removed by a run that completed.
- **D-CLOUD-175/178/179:** no folder migration remains in these 14. `superseded_saves_setting` recognises `/GAMES` and `/ROCKNIX/Saves` only to refuse creating them.

## Carried to `04`

The twelve leads of `02` § Leads, the three uncalled functions, and the
two stale comments above.
