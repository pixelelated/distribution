# Punch list (Phases 5 and 6) — M6.P2 T16, the cloud sync core (#663)

reviewed-at: `aeebe31248` (the stage-D record; its 14 paths are `8ebaf8daad`'s bytes) · fixed-at: `23dfd53c0e` (`feature/m6-cloud-sync-core-663`, stage E's last fix; the hand-back tip follows it with the record and the coordinator's branch merged)

The audit issue is #1295, a sub-issue of #663, with one checkbox per item. There is one item per finding of `04` after both seats' grading (`04` § Second opinion), with the severities graded there. A seat's item that extends a finding sits under that finding's item; one that stands alone has its own. Every file of the 14 is the fork's own, so a defect is a `bug` with its trace and `Already written:` line (`04` § Q3), fixed only under a stream brief the coordinator writes. Each item's **Proposed** line is this lane's proposal; the coordinator's ruling goes in § Phase 7 resolution gate.

**Carried for the stream brief, not an item:** D-CLOUD-185 (#663, 2026-10-26 07:38Z). The twins' `RCLONE_NET_OPTS` split (`cloud_restore:1406-1411`, `cloud_backup:1367-1371`) takes the same allowlist, with T17's `tools/t17-content-fixture.py` as the model.


## PL-01: A stop over an automatic restore costs a save: the TERM waits out the transfer, and a stop that does not reach timeout's own process group leaves rclone to replace a save the game wrote after it

- **Severity:** High
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-03, G-01
- **Owner area:** cloud_restore, cloud_backup (the automatic rclone() wrapper)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (F-03, G-01; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: host-proved (`guest-cycle/host-leads/e-term-automatic`, three arms; `g01-timeout-pgid`); on one GENERIC_X64 guest, the same arms under the image's bash 5.3 and coreutils 9.4 (stage E, `fix-walk-pending-image`)
- **Already written:** a stopped run writes no stamp; a save replaced under a running game is gone and was never under `--backup-dir`; a fix inherits nothing it can read
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a bug and a stream: the automatic call run as the deliberate one is, its child killed with its group by the trap, `timeout` given `--foreground` or replaced; the ES slice reads how STOP IT AND PLAY stops the run

## PL-02: A stopped restore leaves the saves it was replacing absent, and the next completed restore that replaces anything else deletes the only copies

- **Severity:** High
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-14, G-21
- **Owner area:** cloud_restore (`:1869-1871`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (F-14, G-21; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: KILL2 on the guest (`guest-cycle/cells-3/KILL2a`, `KILL2b`) and `guest-cycle/host-leads/f14-backup-dir-order`; the fix's walk is KILL2 with its absent-save check passing
- **Already written:** a device whose restore was stopped holds the replaced saves under `/storage/.cache/cloud_sync/replaced/<stamp>/` and perhaps a `.partial`; a cloud may hold a `.partial` a later backup sent; the next completed restore fetches the save again (it does today); a re-run that replaced another file has already deleted `replaced/<stamp1>/` (G-21), and nothing records it
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a bug and a stream, with PL-04's guard in the same change (a restore without `--backup-dir` would copy into `/`)

## PL-03: cloud_sync.conf can set the scripts' own globals: RCLONE_OUTER names the program a deliberate run executes as root, and PARTIALS_CLEAN, LOG_FILE and CEILING_DIR_ROOT steer rm and >>

- **Severity:** High
- **Category:** Security
- **Question:** Q3
- **Source Finding:** G-20
- **Owner area:** cloud_sync_helper (`conf_valid`, `:240-323`), the twins' load_config and globals
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-20; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: `guest-cycle/host-leads/g20-rclone-outer` on the host; on the guest at stage E, a settings archive carrying the conf and an executable, restored, then one deliberate run
- **Already written:** a conf carrying such a key, from its owner or a restored settings archive (backuptool sweeps `/storage/.config`); the fix reads only the allowlisted keys, so the key stops working without the conf being refused
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a bug and a stream: an allowlist of the 16 keys and the legacy names in `conf_valid` and `load_config`, and the scripts' internals set read-only before the conf is sourced

## PL-04: SAVESPATH's two readers: a commented non-default path sends the card guard to /storage/roms; an empty one is refused only by rclone's overlap check, and the player is told the cloud refused

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-02
- **Owner area:** cloud_restore (`:1758-1760`, `:1902-1906`), cloud_saves_root (`:46-51`), cloud_capture (`:193-198`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (F-02; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: `guest-cycle/host-leads/b-empty-savespath` (four arms) and `02` § The configuration's fixture; the fix's walk repeats both on the image
- **Already written:** none ships such a value and the helper never writes one; the empty path wrote nothing and left the stamp `7 YOUR_CLOUD_WOULDN'T_TAKE_THE_FILES`; a card record taken under a commented path names `/storage/roms`'s card, which the fix re-reads
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a bug, fixed with PL-02: one reader for SAVESPATH in all three scripts, and the restore refusing an empty one as `cloud_backup:1613` does; Argon's three more forms (single quotes, an unquoted value with a comment, `BACKUPPATH`) and `mkdir`'s status read

## PL-05: load_config sources the conf it refused when the .bak put-back fails, as on a full card

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-01
- **Owner area:** cloud_backup, cloud_restore (`load_config`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (F-01; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: `fixtures/load-config-fallback.sh` on the host; on a disposable guest, a full `/storage` by `fallocate` (stage E)
- **Already written:** a refused conf ran as root whatever its lines said (the owner's own); perhaps a `cloud_sync.conf.tmp.<pid>` from a failed copy; the fix refuses with YOUR CLOUD SYNC SETTINGS COULDN'T BE READ and removes its own temp
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a bug and a stream

## PL-06: The helper's one-time migrations mark themselves done whatever sed returned: a failed rewrite of BACKUPMETHOD=sync is never retried

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-02
- **Owner area:** cloud_sync_helper (`:569-579`, `:590-598`, `:609-617`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-02; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: the helper whole in the sandbox with `sed -i` failing, then the guest at stage E
- **Already written:** a device may hold `sync` with the marker and no `cloud_sync.conf.pre-copy-default`; the fix reads the value, migrates that case once more, and touches the marker after a re-read
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a bug and a stream

## PL-07: An empty saves-root record stops every sync for good, behind a "try again" that cannot work

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-14, F-15
- **Owner area:** cloud_saves_root (`:131-141`, `:193-199`); the twins' order (`cloud_restore:1648-1651`, `:1931-1940`); tools/cloud-round-trip's fx_kill15
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-14, F-15; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: KILL15's plant on the guest, then a run that completes and a second that passes `check`; `host-leads/k15-at-the-run` shows today's words
- **Already written:** an empty record an older build's in-place write or a power cut left; the fix reads it as no record once, or the page offers ACCEPT
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a bug and a stream; F-15 (the cell's outcome check on a helper) to T13's harness, an issue the coordinator names

## PL-08: The exit path's cost: the helper on every twin run, rclone help for a flag rclone 1.75.2 lacks, cloud_net_ready's 3 s from its own first look

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source Finding:** F-05
- **Owner area:** cloud_sync_helper, the twins, cloud_net_ready
- **Where:** `04-analysis.md` § Risk Assessment, § Q5 and § Second opinion (F-05; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: lead (c)'s timings on one GENERIC_X64 guest (`(window)`-pending: stage E and the integration window); the probe's futility is host-proved (`host-leads/d-terminal-width`)
- **Already written:** nothing inherited: no state is written by the cost
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream: drop the three probes (PL-09); the helper's run gated on its markers; re-graded when the timings meet D-CLOUD-119's 3 s at the integration window

## PL-09: Dead code: three uncalled restore functions, three --progress-terminal-width probes that can never match, logged_moved's log half

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-06
- **Owner area:** cloud_restore, cloud_backup
- **Where:** `04-analysis.md` § Risk Assessment, § Q6 and § Second opinion (F-06; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: `host-leads/d-terminal-width` for the probes; the suite over WebDAV after the removal
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** removals in a stream, as the coordinator rules (D-WORKFLOW-209's last clause); `logged_moved`'s stderr half stays

## PL-10: Four comments say what is not so (cloud_backup:69-71, 102-cloud-saves:44, cloud_restore:764 on busybox awk, cloud_sync.conf:40-45 on CONTENT_REMOTE)

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-09, G-19
- **Owner area:** cloud_backup, cloud_restore, 102-cloud-saves, cloud_sync.conf and its defaults
- **Where:** `04-analysis.md` § Risk Assessment, § Q7 and § Second opinion (F-09, G-19; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes for `:764`: `host-leads/a-awk`; the others are comments against code
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream

## PL-11: The why sentences for rclone 3/4 and 7/8 differ from es-player-text.md, and two are in no table

- **Severity:** Low
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-04
- **Owner area:** the twins; the rule (#909); ThreadedCloudSync (an ES slice)
- **Where:** `04-analysis.md` § Risk Assessment, § Q2 and § Second opinion (F-04; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: the vocabulary suite of `tools/vm-qa` and the card's frame on the guest, after the words are settled
- **Already written:** stamps carry the why as a token; a reader turns it back into words, so a changed sentence reads both shapes
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** #909 for the rule's half; the ES slice for the fallback map; the scripts' half in a stream once the words are ruled

## PL-12: cloud_sync_helper's seams: a substring key test, a -v edit over the whole conf, unchecked /tmp writes, a truncated rules file merged, fixed scratch names, a fresh device's first sync vetoed, a last rules line without a newline dropped, a failed first conf left as .new

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-07, G-05, G-06, G-11, G-16, G-27 (a, b)
- **Owner area:** cloud_sync_helper (`:79-98`, `:119-177`, `:462`, `:536-544`, `:569-579`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (F-07, G-05, G-06, G-11, G-16, G-27; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: the helper run whole in the sandbox on each planted conf (a comment naming a key, a `-v` with a double-spaced folder, a full `/tmp`, a cut rules file, a fresh `sync`)
- **Already written:** a conf missing a key some comment names; a conf whose folder lost a double space; rules merged from a cut file (the last whole copy is the `.bak`); a fix reads each At the hand-back (ruling 14, D-CLOUD-192): a player's filter flag already in `RCLONEOPTS` -- PL-015's `--exclude "*.tmp"` among them, which at `8ebaf8daad` reached rclone with its quotes and excluded nothing -- is **read both** and moved once into the rules file as the player's rule, the line stripped under the `.bak`; fail closed on the move (`stage-e/s6/move-cells.sh`, `s6-move-before.out`, `s6-move-after.out`).
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream

## PL-13: The capture's stage GC: a keep-list from an unchecked jq, and its ten-minute grace on the wall clock

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-08, G-24
- **Owner area:** cloud_capture (`:1649-1652`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (F-08, G-24; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: the capture run in the sandbox with a `jq` shim that fails
- **Already written:** seals older than 600 s removed by a failed read; no consumer of `stage/` exists today (#1057)
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** #1057, Medium once its reconciler reads the stage; or a stream now

## PL-14: The recipe's unpack deletes the download from the shared source cache, and runs on into that rm when unzip fails

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** F-10, G-17
- **Owner area:** rclone's package.mk (`:54-58`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q4 and § Second opinion (F-10, G-17; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** No VM needed: a build-path fact, read at `package.mk:54-58`
- **Already written:** nothing on a device
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream at the next rclone bump

## PL-15: One library for the twins: 34 byte-identical functions and a third conf_valid

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** F-11
- **Owner area:** the twins, cloud_sync_helper
- **Where:** `04-analysis.md` § Risk Assessment, § Q1 and § Second opinion (F-11; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: the suite over WebDAV after the move
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a design for the coordinator; no edit in this slice

## PL-16: The capture ignores TERM, and its boot --full is unbounded

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-12
- **Owner area:** cloud_capture (`:136`), 102-cloud-saves
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (F-12; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: one `--full` timed on the guest's journal (`(window)`-pending)
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream: a bound on `--full`

## PL-17: Unquoted expansions, and cloud_saves_root check --wait as the last argument loops for ever

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-13
- **Owner area:** cloud_restore (`:1993`), the twins, cloud_saves_root (`:126`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (F-13; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: `cloud_saves_root check --wait` run in the sandbox under a timeout
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream

## PL-18: The card's identity: by path prefix, dev:unknown accepted, check run before the saves folder is made, a boot-local number kept

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-03, G-04, G-25
- **Owner area:** cloud_saves_root (`:56-85`, `:143-164`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-03, G-04, G-25; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: a symlinked `SAVESPATH` and a missing path on the guest, `cloud_saves_root identity` read
- **Already written:** a record holding `dev:unknown` or the internal card's UUID for a symlinked path; the next run's compare reads it
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream, with PL-07

## PL-19: The partials sweep: its failure still writes restore-tree-clean, its pattern can match a cloud file, and a .partial from the cloud is never swept on a clean tree

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-10, G-13, G-22
- **Owner area:** cloud_restore (`:1595-1598`, `:1908-1913`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-10, G-13, G-22; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: a read-only saves tree in the sandbox, the marker read after; a cloud file of the pattern's shape restored
- **Already written:** a `restore-tree-clean` written over partials a failed sweep left; the fix removes the marker when the sweep fails
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream, with PL-02

## PL-20: The automatic run's deadline and the card wait count on the wall clock

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-09
- **Owner area:** cloud_backup (`:8`, `:1403`), cloud_restore (`:347`), cloud_saves_root (`:108-110`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-09; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: the guest's clock stepped forward mid-run (`date -s`), the run's exit read (stage E)
- **Already written:** nothing inherited: a run cut short writes its 124 stamp; the next sync carries it
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream: the bounds counted from `/proc/uptime`

## PL-21: cloud_net_ready: its bound stretched by slow nmcli calls, and --wait read as octal with a leading zero; uptime read without 10#

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-15, G-18, G-27 (c)
- **Owner area:** cloud_net_ready (`:72-74`, `:107-108`, `:121-131`, `:167-169`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-15, G-18, G-27; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: an `nmcli` shim that sleeps, in the sandbox; `--wait 010` timed
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream

## PL-22: The allowlist excludes *.sqlite and *.sqlite3 but not their -wal, -shm and -journal sidecars

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-12
- **Owner area:** cloud_sync-rules.txt and its defaults (`:10-15`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-12; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: `rclone lsf --filter-from` on a planted tree, in the sandbox
- **Already written:** a cloud may hold a sidecar a backup sent; the rules' change is additive (an exclusion), and the helper's merge carries it to every device
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream

## PL-23: The duplicate cleanup's continuations: a backslash ending a comment, and a first occurrence's lines read as assignments

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-07, G-26
- **Owner area:** cloud_sync_cleanup_duplicates.sh (`:15-25`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-07, G-26; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: the cleanup whole in the sandbox on the planted conf
- **Already written:** a conf that lost the line after such a comment; the fix cannot restore it, the twins' `.bak` can
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream

## PL-24: No FIFO, no ceiling: the deliberate run goes unbounded rather than refuse

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q3
- **Source Finding:** G-08
- **Owner area:** the twins' bounded_rclone (`cloud_restore:241-249`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-08; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: a read-only `/var/run` in the sandbox, the log's WARN read
- **Already written:** nothing inherited
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a design, recorded with its sentence (`:242-245`)

## PL-25: --recent trusts last-backup's epoch after a change of cloud folder, so the exit syncs send only recent saves until the next boot

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** G-23
- **Owner area:** cloud_backup (`:1805-1814`)
- **Where:** `04-analysis.md` § Risk Assessment, § Q3 and § Second opinion (G-23; file:line at `8ebaf8daad`); `02-forward-audit.md` § Positives
- **Can this be done on the VM?** Yes: on the guest, a change of `SAVES_REMOTE` then an exit sync, the new folder listed
- **Already written:** a new folder holding only recent saves until a boot sync; the fix records the destination in the stamp, as `settings-backup.uploaded` does (`:2121`), and treats a stamp without one as a different destination
- **Acceptance:** the owner's criteria once ruled; the VM proof named above, its line quoted on the owning issue
- **Proposed:** a stream

## For #585: one line each (the coordinator posts them at acceptance)

```
none: every finding is in the fork's own files; the bare-rclone fact under PL-02 (the move to --backup-dir at check time) is rclone's documented order, not a defect to send upstream
```


## Index

```yaml
punch_index:
- id: PL-01
  severity: High
  category: Correctness
  question: Q3
  source_finding: "F-03, G-01"
  tracked: "#1298"
  outcome: resolved:#1298
- id: PL-02
  severity: High
  category: Correctness
  question: Q3
  source_finding: "F-14, G-21"
  tracked: "#1299"
  outcome: resolved:#1299
- id: PL-03
  severity: High
  category: Security
  question: Q3
  source_finding: "G-20"
  tracked: "#1300"
  outcome: resolved:#1300
- id: PL-04
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-02"
  tracked: "#1301"
  outcome: resolved:#1301
- id: PL-05
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-01"
  tracked: "#1302"
  outcome: resolved:#1302
- id: PL-06
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "G-02"
  tracked: "#1303"
  outcome: resolved:#1303
- id: PL-07
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "G-14, F-15"
  tracked: "#1304"
  outcome: resolved:#1304
- id: PL-08
  severity: Low
  category: Renovation
  question: Q5
  source_finding: "F-05"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-09
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-06"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-10
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "F-09, G-19"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-11
  severity: Low
  category: Standards
  question: Q2
  source_finding: "F-04"
  tracked: "#909"
  outcome: deferred:#909
- id: PL-12
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-07, G-05, G-06, G-11, G-16, G-27 (a, b)"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-13
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-08, G-24"
  tracked: "#1057"
  outcome: deferred:#1057
- id: PL-14
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "F-10, G-17"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-15
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "F-11"
  tracked: "#1297"
  outcome: deferred:#1297
- id: PL-16
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-12"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-17
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-13"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-18
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-03, G-04, G-25"
  tracked: "#1304"
  outcome: resolved:#1304
- id: PL-19
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-10, G-13, G-22"
  tracked: "#1299"
  outcome: resolved:#1299
- id: PL-20
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-09"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-21
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-15, G-18, G-27 (c)"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-22
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-12"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-23
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-07, G-26"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-24
  severity: Low
  category: Renovation
  question: Q3
  source_finding: "G-08"
  tracked: "#663"
  outcome: resolved:#663
- id: PL-25
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "G-23"
  tracked: "#663"
  outcome: resolved:#663
```

## Phase 7 resolution gate

From the coordinator's stage-D ruling on #663 (14:36 UTC 2026-10-30); moved at the hand-back of stage E (2026-10-31): each stream's items Resolved at its commits, the bugs open until their guest halves run at the integration window and the branch reaches `next`. A bug's item is Deferred to its issue until its stream's commit, then Resolved with it; an item in a stream without a bug of its own is Deferred to #663's stage-E stream. Each item's **Proposed** line above is the lane's proposal at the pause, kept as it was.

| Item | Outcome | Tracked |
| --- | --- | --- |
| PL-01 | **Resolved** `3a30c99736`, `38cf8c9d10` (S2): ES's group stop leaves nothing alive 2 s after it, a TERM to the script alone ends at +6 s, the game's save stands (`stage-e/s2-after-e-term*.out`); the guest arms `fix-walk-pending-image` | #1298 (open until the guest half and `next`) |
| PL-02 | **Resolved** `3a30c99736` (S2): the absent saves put back, `.completed`/`.recovered` decide the prune, local and remote (`s2-after.out`, `s2-rprune-s2.out`); KILL2's arms `fix-walk-pending-image` | #1299 (open until the guest half and `next`) |
| PL-03 | **Resolved** `f05f5727e0`, `d2fab0e07a` (S1, D-CLOUD-188/189/191): undocumented keys refused by name in all three copies, legacy keys read both and migrated (`s1-after.out`); the archive case `fix-walk-pending-image` | #1300 (open until the guest half and `next`) |
| PL-04 | **Resolved** `3a30c99736`, `38cf8c9d10` (S2): one `SAVESPATH` reader; an empty folder refused before rclone with YOUR SAVES FOLDER ISN'T ON THIS DEVICE (`s2-after-b-empty.out`) | #1301 (open until `next`) |
| PL-05 | **Resolved** `f86fb5cf1a` (S3): a failed put-back is `clean_exit 1`, nothing sourced (`s3-after.out`); the full card on the guest `fix-walk-pending-image` | #1302 (open until the guest half and `next`) |
| PL-06 | **Resolved** `f86fb5cf1a` (S3): no marker on a full card, the values migrated once there is room (`s3-after.out`); ruling 5's already-written line on #1303 | #1303 (open until the guest half and `next`) |
| PL-07 | **Resolved** `100eaa4b57` (S4): an empty record read as none and rewritten by the completed run, `check` passing after (`s4-after.out`); KILL15's plant `fix-walk-pending-image`; F-15 is #1296 | #1304 (open until the guest half and `next`) |
| PL-08 | **Resolved** `9df834d183` (S5): no helper under `--recent`, no grace on connected/full (4 ms), the probes gone (`s5-after.out`); the timings lead (c)'s, `(window)`-pending | #663 |
| PL-09 | **Resolved** `9df834d183` (S5): three functions, three probes, two drop lines and `logged_moved`'s dead half removed, `git log -S` read first; uncalled none | #663 |
| PL-10 | **Resolved** `9df834d183` (S5): the four comments say what the code does | #663 |
| PL-11 | Deferred | #909 (the two sentences in no table, with their texts); the three texts recorded in `02` § The ES stop and the why texts: for rclone 3/4 and 7/8 the scripts and ES's fallback map agree and `es-player-text.md:270-272` differs, so the rule is the coordinator's to correct, named in the hand-back |
| PL-12 | **Resolved** `02d19b0787`, `61f8fcc5b2`, `23dfd53c0e` (S6 and its two follow-ups, rulings 10 and 14): each seam fails closed, the allowlist, the filter flags moved into the rules file once (`s6-after.out`, `s6-move-after.out`) | #663 |
| PL-13 | Deferred | #1057 (the unchecked `jq` keep-list and the wall-clock grace, two lines there); no stream here |
| PL-14 | **Resolved** `9df834d183` (S5): the download kept, a broken zip stops the unpack; `tools/pkgcheck rclone` rc 0 (`s5-after.out`) | #663 |
| PL-15 | Deferred | #1297 (the coordinator's Backlog: the twins' one library, recorded as a design); #1300's stream touches the three `conf_valid` copies identically and no more |
| PL-16 | **Resolved** `a174a2dcbf`, `b367ebcf48` (S7, D-CLOUD-190): TERM a clean stop between files (rc 143, the manifest as planted), the `--full` bound, the retire unit finished first (`s7-after*.out`); the image half `fix-walk-pending-image` | #663 |
| PL-17 | **Resolved** `02d19b0787` (S6): `--wait` with no value refuses (rc 64 in 1 ms); `mkdir -p "${SETTINGS_BACKUPS}"` quoted | #663 |
| PL-18 | **Resolved** `100eaa4b57` (S4): the card by its device in `mountinfo`, no identity refused, `check` after the folder test, no `dev:` kept (`s4-after.out`) | #1304 |
| PL-19 | **Resolved** `3a30c99736` (S2): a failed sweep writes no `restore-tree-clean`, `*.partial` excluded both ways (`s2-after.out`) | #1299 |
| PL-20 | **Resolved** `a174a2dcbf`, `b2833a6919` (S7): deadlines and waits on `/proc/uptime`; a +3600 s step changes nothing (`s7-after.out`) | #663 |
| PL-21 | **Resolved** `a174a2dcbf` (S7): `--wait 010` is 10 s, a slow `nmcli` bounded (3 s), uptime 0.08 read (`s7-after.out`) | #663 |
| PL-22 | **Resolved** `a174a2dcbf` (S7): the six sidecars excluded in both rules files (`s7-after.out`) | #663 |
| PL-23 | **Resolved** `02d19b0787` (S6): the cleanup reads continuations as bash does (`s6-after.out`) | #663 |
| PL-24 | Resolved | #663 (recorded as a design: a deliberate run is unbounded by D-CLOUD-113, which lets it take time and say so on its page; no stream) |
| PL-25 | **Resolved** `a174a2dcbf` (S7): `last-backup-dest`; a changed folder takes one full pass, then the window (`s7-after.out`); the guest half `fix-walk-pending-image` | #663 |
