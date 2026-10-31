# Mini Retro: T16, the cloud sync core (#663)

**Completed:** 2026-10-31.

**Scope:** stage E of the slice whose brief is `docs/reviews/briefs/cloud-sync-core.md`:
- the 14 paths of `projects/ROCKNIX/packages/network/rclone/` that are T16's (the twins, the capture, the helper, `cloud_saves_root`, `cloud_net_ready`, the rules and the conf, the recipe, the autostart);
- the audit `docs/audits/2026_10_25-epic-m6-cloud-sync-core/` and its issue #1295 (25 items);
- the seven bugs #1298 to #1304;
- the coordinator's stream brief `t16-streams.md` at `2597b8a272`, with its thirteen rulings and ruling 14 (D-CLOUD-192).

**Branch:** `feature/m6-cloud-sync-core-663`. Stage E made 18 commits from `f05f5727e0` to `23dfd53c0e`, each stream with its follow-ups.

**Delta** (the tools' own lines):
- `git diff --shortstat 8ebaf8daad 23dfd53c0e -- projects/ROCKNIX/packages/network/rclone`: `13 files changed, 1183 insertions(+), 355 deletions(-)`, in 12 commits.
- `tools/last-good-scripts-test` whole, with `QA_SYSTEM_ROOT` the donor and 0 SKIP: PASSED 1313 / 0 before (`stage-e/suite-before.out`) and PASSED 1313 / 0 after, at `23dfd53c0e` (`stage-e/suite-after.out`).
- Stage E's commits touching `tools/`: 0. Paths changed outside the rclone package and the audit folder: 0.

## What worked well

- **The unfixed root first.** Every cell ran on `8ebaf8daad`'s bytes before the fix, so each FAIL was observed, not argued. Four of them overturned an expectation:
  - `cloud_backup`'s `check` ran *before* its folder test, the reverse of the brief's reading;
  - PL-015's `--exclude "*.tmp"` never excluded anything, because rclone got its quotes;
  - the S6 cut-rules cell showed nothing until the cut fell inside the player's rules;
  - the `/proc/uptime` bind needed a host path.
- **The suite after every stream.** S1, S2, S6 and S7 each surfaced a FAIL a cell could not: a seventh legacy key, a scanner reading `${CLOUD_SAVESPATH}` as a script name, a supported flag the allowlist dropped, and lifted spans missing a top-level helper. Each was found the same hour and fixed in a follow-up.
- **One root per stream from `mkroot.sh`.** A before and an after differ only in the scripts. The stand-ins (`blkid`, `nmcli`, `date`, `sha256sum`, `mv`, an argv-recording `rclone`) are named in each cell.
- **Questions put on #663 the moment they arose.** `LAYOUT_KEEP` and the filter flags came back as rulings (D-CLOUD-191, D-CLOUD-192) within the session.

## What was harder than expected

- **The sandbox's own facts:**
  - `/usr/bin/sh` was the host's dash, not the image's bash. Five streams went by before a `10#` exposed it.
  - `/dev` has no disk nodes, so `blkid` needed a stand-in.
  - A bind's source is a host path.
  - `new_cell` names a cell by the second, so two runs in one second shared a cell (S4).
- **The suite's lifted spans.** Section d lifts `load_config` and section h lifts the wrapper by their spans. A helper function added at top level (`uptime_s`, `allowed_opts`) makes the span print `command not found` and carry on, and section d's check did not notice. The brief's file list said so (`The suite lifts functions by their span`); S6 and S7 had to meet it.
- **The `git archive` snapshot** cost a suite run: 16 false FAILs from a missing `.git`.
- **Usage limits** cut the stage in three places. The checkpoint posts made each resume exact.

## What did we discover

- **rclone's 9** is reachable only with `--error-on-no-transfer`, and the twins handle it in three places. A flag list read from shipped values alone missed it (A6).
- **The image's `/usr/bin/sh` is bash** (`busybox/package.mk:170-174`). `cloud_net_ready` is the one `#!/bin/sh` script in the slice.
- **A saves root with no UUID** gets no record after PL-18 (ruling 13). The lane found no shipped saves root without one: `/storage` is ext4 with its UUID set at image time (`scripts/mkimage:100-101`, `tune2fs -U`), and a second card's FAT or exFAT carries a volume serial that `blkid` reports as its UUID (the automount reads it with `blkid`). Reading the recipes is not a census of every device, so this is said, not proved.
- **ES at `16dbac5211` needs no patch.** The group stop lands once `timeout` runs `--foreground` (S2).

## What adjustments are needed

- **T15 (merge debt):**
  - `stage-e/patches/last-good-scripts-test.patch` carries six fixture completions (A18, A4, A23, d, h, S315).
  - Section d's lift list should name every function `load_config` calls; an awk over its body would keep it current.
- **T13 (#1296):** `fx_kill15`'s expected wording changes with S4.
- **The brief's errata:** `cloud_backup`'s `check` order; `mkroot.sh`'s shell; `tools/pkgcheck` takes a package name.
- No change to the remaining phases.

## Instruction recommendations

- `es-code-traps.md`'s sibling for shell: a function a suite lifts by its span must not call a top-level helper added later; inline the read, or name the helper in the lift. This is the second time in M6 (T15's sections and this one). It is a candidate for `engineering-practices.md` when the coordinator writes rules.
- A host fixture's root names its `/bin/sh`. `mkroot.sh` does now; other lanes' kits should check theirs.

## Time to play

- **The exit sync:** S5 takes the helper off it under `--recent`, and S7 replaces two `date` forks with `/proc/uptime` reads.
- **The first exit sync after the update** on every device is one full pass, because there is no `last-backup-dest` yet (PL-25).
- **The startup sync:** S5 drops the restore's probe, and the 3 s grace when the link is already up.
- `cloud_net_ready` ends no later than before.
- **The exit sync against D-CLOUD-119's 3 s:** the last logged figure is **0.97 s**, the exit sync's stamp in x64 run 44 at `664ad9ac64` (2026-09-24, `docs/vm-qa-log.md:131`). The runs before it logged 0.97 s and 0.84 s (`:129-130`).
  - That is about 2 s under the 3 s. The same run logged the game's first frame at 1.09 s and the next game's at 1.51 s.
  - It predates this slice's streams. S5 and S7 only take work off the path: the helper under `--recent`, and two `date` forks. S2 runs the same rclone call in the background and waits for it.
  - No guest ran in stage E. This tree's own figures are lead (c)'s, measured at the integration window by `tools/time-to-play --vm`, where PL-08 is re-graded against the 3 s.

## What T17 (#664) inherits

- **`conf_valid` is an allowlist** of the 16 documented keys and the seven legacy ones (D-CLOUD-188, 189, 191), in all three copies. A key `cloud_setup` writes into `cloud_sync.conf` must be on it, or every twin run refuses the conf.
- **`allowed_opts` is T17's `content_net_opts`** with the flag list as arguments (ruling 10). A change to T17's list or its value kinds is a change here too.
- **The helper moves a player's filter flags into the rules file once** (D-CLOUD-192). A setup page that writes `RCLONEOPTS` should not write a filter flag.
- **`cloud_saves_root accept`** (behind `cloud_setup --accept-saves-root`) refuses with no identity, and on a `dev:` identity clears the record rather than keeping a number.
- **`last-backup-dest`** sits beside `last-backup`. A change of saves folder through setup makes the next exit sync one full pass.

## What the integration window inherits

Every guest half is `fix-walk-pending-image`, listed by stream in `02` § The streams:
- `e-term-automatic`'s arms and KILL2 (S2);
- the settings archive with a conf and an executable (S1);
- the full `/storage` (S3);
- KILL15 then a completed restore (S4);
- the timings (S5);
- the capture's TERM, the `--full` bound, and a `SAVES_REMOTE` change then an exit sync (S7).

## Scoped audit (Step 2.5)

- **AC conformance:** PASS. Each bug's fix is in its stream's commit, with its before and after under `stage-e/`. #1295's items are resolved or deferred in `05`'s Phase 7 table, and `lint-audit-artifacts --phase resolution --issue 1295` passes. The bugs stay open for their guest halves and `next`.
- **Cornerstone spot-check:** PASS.
  - Temp-and-rename for every write this stage added (D-CLOUD-078).
  - Fail closed on each new check.
  - No new player sentence and no stamp shape changed (`vocabulary-check` 0 wrong at every stream).
  - Nothing outside the two folders.
- **Interaction-defect scan:** PARTIAL. The suite's lifted spans met S6's and S7's top-level helpers, found by the suite and repaired. Ruling 14's move meets the rules merge and the twins' allowlist, and both orders are proved by `s6/move-cells.sh`.
- **Futro prediction verification:** SKIP. No futro was run; the brief's rulings served as the plan.
- **Housekeeping (full-suite scan):** PASS. PASSED 1313 / 0 before and after, and after each stream as read in `02` § The runs.
- **Harness self-coverage:** PASS. Every cell FAILed on the unfixed root before it PASSed, except where `s7-checks.txt` and `s6-checks.txt` say the pin already behaved: the retire unit, and the refusal path's twins.
- **Documentation:** PARTIAL.
  - `rclone-cloud-sync.md` is #909's (T4's): the sweep, the sidecars, the `.completed` marker, the filter flags' move.
  - `es-player-text.md:270-272` is the coordinator's (PL-11).
  - `rocknix.org`'s queue (#42): the sidecars, the stop, and a filter's place in the rules file.
- **Build-vs-adopt:** SKIP (fixes only).

## Code-verifiable state

| Stream | Items | Commits | Positive |
| --- | --- | --- | --- |
| S1 | #1300 | `f05f5727e0`, `d2fab0e07a` | `s1/cells.sh` |
| S2 | #1298, #1299, #1301, PL-19 | `3a30c99736`, `38cf8c9d10` | `s2/cells.sh`, `cells/e-term-automatic.cmd.sh` |
| S3 | #1302, #1303 | `f86fb5cf1a` | `s3/cells.sh` |
| S4 | #1304, PL-18 | `100eaa4b57` | `s4/cells.sh` |
| S5 | PL-08, 09, 10, 14 | `9df834d183` | `s5/cells.sh`, `tools/pkgcheck rclone` |
| S6 | PL-12, 17, 23, D-CLOUD-185/192 | `02d19b0787`, `61f8fcc5b2`, `23dfd53c0e` | `s6/cells.sh`, `s6/move-cells.sh` |
| S7 | PL-16, 20, 21, 22, 25 | `a174a2dcbf`, `b367ebcf48`, `b2833a6919` | `s7/cells.sh`, `tools/cloud-capture-stamp-test` |
