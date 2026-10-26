# Punch list — M6.P2 T17, cloud setup, sign-in, connections, content and settings backups (#664)

**Extended depth** (two seats: GPT-6 Astra at `max`, then Gemini 4 Argon at `high`; `04` § Second opinion). The audit issue is opened at stage D as a sub-issue of #664.
- **Twenty-three items:** 2 Medium, 5 Low, and 16 Info, Design or Renovation. PL-23 (F-24) came from the guest window's PL-18 proof at stage E. The coordinator ruled it a `bug` at the hand-back: #1136, fixed by S7.
- **Six `bug`s filed at stage D** (the coordinator's ruling at the pause, 07:5x UTC), each with its trace, `Already written:` line and VM line:
  - #1128, PL-01 with PL-14 (Low, S1);
  - #1129, PL-02 (**Medium**, S2, under D-CLOUD-185);
  - #1130, PL-03 (**Medium**, S3);
  - #1131, PL-04 with PL-08 (Low, S4);
  - #1132, PL-06's selection write (Low, S5);
  - #1133, PL-05's `cloud_setup:797` (Low, S6).
  - The streams are `docs/reviews/briefs/t17-streams.md` at `f59f7cbbc1`.
- **Nothing** in this list changes a file under `packages/`, `projects/` or `tools/` at stages A to D. No item proposes a removal (D-WORKFLOW-209 reaches nothing; the 14 are fork-own).
- **Two guest windows** ran, 07:59:26 to 08:06:04 and 08:18:14 to 08:21:22 UTC (`02` § The guest cycle). **Nothing ran on a person's device or cloud.**
- **Stage E:** seven streams, one commit each, and S3's correction `c3e260861b` (`02` § The streams). The rows for PL-01 to PL-06, PL-08, PL-14 and PL-23 point there.

---

## PL-01: a phone's own icon requests spend the sign-in PIN's ten attempts and lock the right PIN out (a `bug`, #1128)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-01, F-09
- **Owner area:** projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth (fork-own)
- **What:**
  - **The cause:** `_supplied()` (`:2330-2344`) takes a request's first path segment as its PIN. `_gate()` (`:2308-2328`) counts any non-empty mismatch, and at ten `pin_exhausted()` (`:2196-2198`) refuses everything with 403.
  - **The trigger:** `/favicon.ico` and the touch-icon requests a phone's browser makes on its own.
  - **The fix:** count only four ASCII digits, checked before `compare_digest` on GET and POST, and answer icon routes 404 before the gate. This also ends F-09's `TypeError` on a non-ASCII PIN (the seat's A-26).
- **Evidence:** P11, P18
- **Can this be done on the VM?** Yes, on the host now: `tools/t17-pin-fixture.py --expect unfixed` is met at `8ebaf8daad`, and a fixed file must meet `--expect fixed`. The guest repeats it against the installed serve. How often a real phone asks for icons is an open item to test (A-12).
- **Already written:** nothing persisted. The counter lives in the serve's memory, and a new serve starts at 0.
- **Acceptance:** the fixture's ten-icon cases answer 200 for the right PIN on the fixed file and 403 on the unfixed one; ten real wrong PINs still lock out (the control)
- **Disposition note:** **Resolved** -- `59a5a8860e`, S1 under `t17-streams.md` (before `stage-e/s1-before.txt`, after `stage-e/s1-after.txt`); bug #1128, its criteria ticked, open until on `next`; the guest met `--expect unfixed` on the installed file

## PL-02: a flag in `RCLONE_NET_OPTS` reaches the match's deleting `sync`, and `--delete-excluded` there deletes saves (a `bug`, #1129)

- **Severity:** Medium (the coordinator's ruling at the stage-D pause; both seats proposed it, A-27 and R-22)
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-02
- **Owner area:** projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore and cloud_content_backup (fork-own); T16's cloud_restore and cloud_backup for the same seam
- **What:**
  - **The cause:** `:235-279` splits the conf value into `RCLONE_NET_OPTS_ARRAY` with no allowlist. Every `bounded_content_rclone` call takes it: `:750`, the deleting `:1046`, `:1538` and `:1551`, and the backup's `:753` and `:766` (A-8).
  - **The effect:** any rclone flag passes. The preview counts what the flags make it count, and the apply deletes that many. A filter flag ahead of the excludes would reach the saves without `--delete-excluded` (Argon's R-9; read from rclone's documented order, no fixture).
  - **The fix:** an allowlist with checked values (`--contimeout`, `--timeout`, `--low-level-retries`, `--retries`, each value a duration or a count), built once where the array is made in both scripts. Stripping one spelling is not enough.
  - **T16's** `cloud_restore:1406-1411` and `cloud_backup:1367-1371` are the coordinator's to route.
- **Evidence:** P9, P13, P18
- **Can this be done on the VM?** Yes. On the host now: `tools/t17-content-fixture.py --expect unfixed --real-rclone <the donor's 1.75.2>` deletes a save unfixed, and fixed keeps it. On the guest: the flag goes into the guest's conf only, over the seeded synthetic root only, with the conf put back after (the coordinator's condition).
- **Already written:**
  - A device whose `cloud_sync.conf` already holds such a value has lost nothing until it runs `--match --apply`.
  - One that already applied has lost saves the fix cannot bring back.
  - The fixed reader refuses an unknown flag at the next run, or lets the shipped bound stand in. Either way the value on the card is read and not migrated.
- **Acceptance:** the fixture's real-rclone case keeps `a.srm` on the fixed file and loses it on the unfixed one; the fixed scripts refuse, or drop with a log line, every flag outside the allowlist
- **Disposition note:** **Resolved** -- `1def91bdfc`, S2 under D-CLOUD-185 (`stage-e/s2-*.txt`, both cases with the donor's rclone); bug #1129, its criteria ticked; T16's twins routed to #663 by the coordinator; the guest proved the loss on the real paths (`guest-cycle/f02.out`)

## PL-03: `cloud_content_backup` uploads any path it is named, `/storage/.config` among it (a `bug`, #1130)

- **Severity:** Medium (the coordinator's ruling at the stage-D pause; both seats proposed it, A-28 and R-23)
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-03
- **Owner area:** projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup (fork-own)
- **What:**
  - **The cause:** `:583-585` takes the explicit names as given. `SRC="${DEST}/${DIR}"` (`:710`), and `remote_for` (`:484-489`) makes the target `${ROOT}ROMs/../.config`.
  - **What is excluded:** nothing under `rclone/` (`:753-757`).
  - **The restore** checks every name at `:1482-1487`.
  - **The fix:** that loop, before the lock.
- **Evidence:** P13, P18
- **Can this be done on the VM?** Yes. On the host now: the fixture's `backup-traversal` case. On the guest: against the QA backend only, its data directory listed before and after, and what the backup carried removed (the coordinator's condition). That run shows what rclone does with the `..` on the backend.
- **Already written:** nothing on the device. A cloud that already received such an upload keeps it. The fix calls for inspecting it and, where `rclone.conf` went up, rotating the credential, never an automatic deletion (A-28).
- **Acceptance:** the fixture's `../.config` case refuses with no rclone call on the fixed file and copies on the unfixed one; `snes` still copies (the control)
- **Disposition note:** **Resolved** -- `f8feb15bb4`, S3, corrected at `c3e260861b` (explicit names only; `last-good-scripts-test` PASSED; `stage-e/s3-*.txt`); bug #1130, its criteria ticked; the guest proved the upload on the real path (`guest-cycle/f03.out`)

## PL-04: an option-shaped key reaches rclone as a flag, and `--config=` writes the new connection outside `rclone/` (a `bug`, #1131; found by both seats)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-20
- **Owner area:** projects/ROCKNIX/packages/network/rclone/sources/cloud_connections.py and cloud_remote (fork-own)
- **What:**
  - **The cause:** `cloud_remote:329-334` splits any `a=b`, and `save()` (`:161-165`) joins it into rclone's argv. rclone honours `--config=<path>` (the connection, its secret included, is written to `<path>`, and the save refuses) and `--log-file=<path>`.
  - **The fix:** refuse a key outside `^[a-z0-9_]+$` in `save()`, before staging. Checking against the provider's option list is the stronger form.
- **Evidence:** P19
- **Can this be done on the VM?** Yes, on the host now: `tools/t17-option-key-fixture.py` (the outside file written, the save refused). The fixed `save()` refuses before staging and writes nothing. The guest repeats it under the image's rclone.
- **Already written:** nothing a shipped caller wrote. The interface passes the provider's own option names. A file an option-shaped key created holds a connection the fix cannot find.
- **Acceptance:** the fixture's `config` and `dash-key` cases refuse with no outside file on the fixed file, and the control still saves
- **Disposition note:** **Resolved** -- `0ffe7cd94f`, S4 (`stage-e/s4-*.txt`); bug #1131, its criteria ticked

## PL-05: two `>>> why` sentences the interface's table does not know

- **Severity:** Low
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-14
- **Owner area:** cloud_setup:797, backuptool:1495; the ES slice's `CloudText::whySentences`
- **What:** `ANOTHER CLOUD SYNC IS RUNNING` is also the *"Not this"* form (D-UI-031); the rule's word is `A SYNC IS ALREADY RUNNING`. `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` is D-UI-117's proposed words. A French screen shows either in English, if it shows them at all.
- **Evidence:** P15, P16
- **Can this be done on the VM?** Yes: the why lines against the table at the pin (`stage-b/why-lines.txt`). What screen shows them is the ES slice's walk.
- **Already written:** nothing persisted (a printed line)
- **Acceptance:** the coordinator's disposition: the script's word changed to the rule's and the table given its pair (ES slice), or recorded
- **Disposition note:** **Resolved** -- `3e95bf18f4`, S6 for `cloud_setup:797` (`stage-e/s6-*.txt`); bug #1133, its first criterion reworded by the ruling [issuecomment-6411280450](https://github.com/pixelelated/distribution/issues/664#issuecomment-6411280450) and ticked; `backuptool:1495`'s French pair and the why table's pairs are T18's, #665

## PL-06: writes judged by their exit status, or not at all

- **Severity:** Low (the selection write, a `bug` by the coordinator's ruling; the other three hardenings Info)
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-10
- **Owner area:** cloud_content_restore `--set-systems`; backuptool's rotation; cloud_setup's conf writes; cloud_log_scrub's `record()`
- **What:**
  - **`--set-systems`** (`:1405-1406`) installs a partial temp file on a full card. Its comment promises *"whole or not at all"* (A-19, A-35).
  - **`backuptool`'s rotation `mv`** (`:1885`) is unchecked.
  - **`cloud_sync.conf`'s writes** take no lock.
  - **`record()`** keeps only `printf`'s status (A-22).
  - **`backuptool`'s own model, two hardenings** (R-45, R-46): the `:1287` comparison without `2>/dev/null`, and `:655` and `:1342` publishing with `mv -f` unchecked.
- **Evidence:** P7, P18
- **Can this be done on the VM?** Yes, on the host: a full-card fixture (a size-capped tmpfs or a fake `printf`) over the real `--set-systems`
- **Already written:** a selection file already cut short is read as written; the fix cannot tell it from a choice
- **Acceptance:** the coordinator's disposition: a `bug` for the selection write with that fixture, or recorded
- **Disposition note:** **Resolved** -- `1d8271a1f3`, S5 for `--set-systems` (`stage-e/s5-*.txt`); bug #1132, its criteria ticked; the other three hardenings recorded at `3a7fdb0ec2` (`02` F-10)

## PL-07: more fail-open shapes (found by the seats)

- **Severity:** Info
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-21
- **Owner area:** cloud_content_restore:1271; cloud_setup:495-498; cloud_scan:315-353
- **What:**
  - the scan's `mktemp -d` is unchecked;
  - the setup probe keeps only `head`'s status, so an empty probe reads as success;
  - the scan's writes are unchecked before `write_completion`;
  - the probe's `*"not found"*` matches a path holding the words (R-43);
  - `cloud_scan` takes `CONFIG_ID` before its lock, and greps the label as a regex (R-44).
- **Evidence:** P18
- **Can this be done on the VM?** Yes, on the host: each with its failure constructed (an unwritable `/tmp`, an rclone killed without a word, a full `OUT`)
- **Already written:** nothing persisted beyond a scan result the next scan rewrites
- **Acceptance:** the coordinator's disposition
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-21), the stage-D ruling

## PL-08: a kill mid-save leaves credentials staged beside `rclone.conf`, and nothing sweeps them

- **Severity:** Info
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-06
- **Owner area:** cloud_connections.py:74, :157, :238
- **What:** `.connection-*` and `.rclone.conf-*` survive a SIGKILL, holding the old configuration, the new one or both (A-18, A-31). They are 0600 in a 0700 directory, and held back by `backuptool`.
- **Evidence:** P14, P18
- **Can this be done on the VM?** Yes, on the host: kill `save()` at each step and list the directory
- **Already written:** any device cut mid-sign-in holds such a directory today; a sweep under the lock at the start of `save()` removes it
- **Acceptance:** the coordinator's disposition
- **Disposition note:** **Resolved** -- `0ffe7cd94f`, S4's sweep (`stage-e/s4-after.txt`); in #1131

## PL-09: what reaches a screen and the log

- **Severity:** Info
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-07
- **Owner area:** cloud_setup:495, :537, :543, :926, :937, :224; cloud_remote:331
- **What:**
  - rclone's ERROR text on the setup page. Nothing masks it (A-4).
  - The root password on the legacy console flow.
  - A malformed pair echoed to stderr.
  - The override file's first line logged.
  - Fixed categories rather than rclone's text answer both the confidentiality and the player-language sides (A-32).
- **Evidence:** P8, P16
- **Can this be done on the VM?** Yes: the setup page's frame on the guest with a refused folder
- **Already written:** log lines already written stay until rotation
- **Acceptance:** the coordinator's disposition; the setup page's words are the ES slice's
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-07); the setup page's words are the ES slice's

## PL-10: secrets on argv, and a sign-in state file readable by any user

- **Severity:** Info
- **Category:** Design
- **Question:** Q3
- **Source Finding:** F-05
- **Owner area:** cloud_connections.py:161-165; cloud_remote:325-335; cloud_oauth's session.json
- **What:**
  - A typed secret stays on `cloud_remote`'s argv for its whole run, and on `config create`'s for its 40 s (A-1).
  - `session.json` is 0644 and holds the PIN.
  - Every process runs as root.
- **Evidence:** P8, P14
- **Can this be done on the VM?** Yes: `/proc/<pid>/cmdline` and the file's mode on the guest
- **Already written:** nothing proposed
- **Acceptance:** recorded as a design note
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-05), a design note

## PL-11: `cloud_remote` logs a connection's name before `save()` checks it, and the scrubber's allowlist drift (found by the seats)

- **Severity:** Info
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-22
- **Owner area:** cloud_remote:263; cloud_oauth:2455-2457
- **What:** a name holding a newline writes a forged line before the refusal (A-50, R-41). Beside it: the scrubber's allowlist has drifted from today's `Refused` sentences. That affects only lines written before a device's first scrub, and makes one false *"masked"* line at boot (R-6, R-49).
- **Evidence:** P18
- **Can this be done on the VM?** Yes, on the host: `cloud_remote create $'a\nb' local` with the log redirected
- **Already written:** log lines already written stay until rotation
- **Acceptance:** the coordinator's disposition
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-22)

## PL-12: what the `pkill -f` patterns reach

- **Severity:** Info
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-23
- **Owner area:** cloud_setup:775-776; cloud_oauth:357, :2819
- **What:** every process whose command line holds `rclone config` or `rclone authorize`, including `cloud_remote`'s own calls and, on a host, a harness (A-11). The serve's own cleanup walks `/proc`.
- **Evidence:** P18
- **Can this be done on the VM?** Yes, on the guest: a `sleep` named to match, then `cloud_setup --free-auth-port`
- **Already written:** nothing persisted
- **Acceptance:** the coordinator's disposition
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-23)

## PL-13: the match's smaller edges

- **Severity:** Info
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-08
- **Owner area:** cloud_content_restore:837-838, :441, :886-980
- **What:**
  - The plan carries no age check (D-CLOUD-141).
  - `/tmp` falls back to a `.$$` name.
  - `exists_remote` matches by regex; no caller reaches it today (A-33).
- **Evidence:** P9, P18
- **Can this be done on the VM?** Yes, on the host
- **Already written:** a plan already on a device is read as written
- **Acceptance:** recorded
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-08)

## PL-14: the paste flow renders rclone's words as HTML

- **Severity:** Info
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-09
- **Owner area:** cloud_oauth:2271-2290, :480-488
- **What:** the PAGE branch inserts `failure_reason()` raw. It is reached only where no browser stack exists, and behind the PIN. No script execution has been shown (A-14, A-34). The `TypeError` half goes with PL-01.
- **Evidence:** P11, P18
- **Can this be done on the VM?** Yes, on the host: the handler with `browser_stack_available` false and a failure reason holding markup
- **Already written:** nothing persisted
- **Acceptance:** recorded, or escaped with the same fixture
- **Disposition note:** **Resolved** -- `59a5a8860e`, S1's escape (`stage-e/s1-after.txt`, `paste-html: escaped`); in #1128

## PL-15: the device id's hash hides the MAC from a glance, not from a search

- **Severity:** Info
- **Category:** Design
- **Question:** Q3
- **Source Finding:** F-11
- **Owner area:** cloud_device_id:143-145
- **What:** unsalted `md5(MAC|unknown)[:10]`. About 2^24 candidates per vendor, with several preimages; the machine-id fallback is another case (A-36).
- **Evidence:** P2
- **Can this be done on the VM?** No: a design read
- **Already written:** every device's id is already in its cloud folder's name; changing the recipe is a second identity change, never silent (A-36)
- **Acceptance:** recorded as a design note
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-11), a design note

## PL-16: the sign-in window

- **Severity:** Info
- **Category:** Design
- **Question:** Q3
- **Source Finding:** F-12
- **Owner area:** cloud-signin-window.c:532-534, :851; cloud_oauth:917, :990-1000
- **What:**
  - Only gestures are filtered.
  - The allowed host is the last two labels.
  - `CLOUD_SIGNIN_DEBUG` is honoured at any value (A-37) and reaches the window through `cloud_oauth`'s environment.
- **Evidence:** P8
- **Can this be done on the VM?** Yes: the window on the guest with the variable set
- **Already written:** a `window.log` already holding keys stays until the next session truncates it
- **Acceptance:** recorded
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-12)

## PL-17: the tools that exercise these files

- **Severity:** Info
- **Category:** Currency
- **Question:** Q4
- **Source Finding:** F-13
- **Owner area:** cloud_folder_validate:90, :252; tools/pixelelated-cloud-validator-test; tools/pixelelated-content-scope-test
- **What:**
  - The validator runs `rclone` from `PATH`: M7's #1117.
  - Two tool defects: #1127, filed by the coordinator (Backlog under #1047).
- **Evidence:** P10
- **Can this be done on the VM?** Yes, on the host: the tools' own runs
- **Already written:** nothing persisted
- **Acceptance:** deferred to #1127 and #1117
- **Disposition note:** **Deferred** -- deferred:#1127 (the two tool defects, the coordinator's Backlog under #1047) and #1117 (the validator's `rclone` from `PATH`, M7's)

## PL-18: archive member types the name check does not inspect

- **Severity:** Info
- **Category:** Design
- **Question:** Q3
- **Source Finding:** F-04
- **Owner area:** backuptool:551-558
- **What:**
  - The image's busybox `tar` refuses an absolute link with a child.
  - Standalone links, hard links and an existing symlink ancestor are untested (A-29).
  - The guest's full `backuptool restore` is the proof owed.
- **Evidence:** P12
- **Can this be done on the VM?** Yes, on the guest: a hand-made archive of each member type through `backuptool restore`
- **Already written:** an archive already in a cloud is read by the same check
- **Acceptance:** the guest's restore of each type leaves nothing outside `/storage` and reverts
- **The guest window** (`guest-cycle/pl18.out`): nothing was written outside, but a standalone symlink to `/var/tmp` **was restored** (rc 0), and a link with a child failed with **its revert failing** (the mark and a directory left). This is PL-23.
- **Disposition note:** **Resolved** -- the guest window's full restore (`guest-cycle/pl18.out`) found F-24, the coordinator's `bug` #1136, fixed by S7 `479cd96c24` (`stage-e/s7-*.txt`)

## PL-19: the connection model's two asymmetries, and `cloud_oauth`'s seams

- **Severity:** Info
- **Category:** Design
- **Question:** Q1
- **Source Finding:** F-15
- **Owner area:** cloud_connections.py:150, :193-197, :218-224; cloud_oauth
- **What:**
  - `require_manual()` is not applied to a new `create`.
  - A first connection writes no `active-connection`.
  - `select()` is a third writer (A-17).
  - `cloud_oauth`'s four seams are a split proposal.
- **Evidence:** P7
- **Can this be done on the VM?** No: a design read
- **Already written:** a device with one remote and no `active-connection` keeps working through the legacy fallback
- **Acceptance:** recorded as a proposal
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-15; `04` Q1), a proposal

## PL-20: dead ends, kept

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-16
- **Owner area:** backuptool's zip path (`:480-518`); cloud_setup's console flow (`:913-976`)
- **What:**
  - Both are reachable.
  - No shell function is named only once.
  - Three python methods are named once, and the framework calls them.
  - **Removals none.**
- **Evidence:** P2
- **Can this be done on the VM?** No: a design read
- **Already written:** legacy zip archives on devices are why the path stays
- **Acceptance:** recorded in `04` Q6
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-16; `04` Q6); removals none

## PL-21: the rule names no writer of `rclone.conf`

- **Severity:** Info
- **Category:** Documentation
- **Question:** Q7
- **Source Finding:** F-17
- **Owner area:** .claude/rules/rclone-cloud-sync.md
- **What:** § The writers and § The secrets' paths say what the rule does not. They are a map, not proof that the inventory is complete (A-42).
- **Evidence:** P7, P8
- **Can this be done on the VM?** No: a documentation read
- **Already written:** nothing persisted
- **Acceptance:** deferred to #909
- **Disposition note:** **Deferred** -- deferred:#909, the line the coordinator posts at acceptance

## PL-22: bounds and currency, recorded

- **Severity:** Info
- **Category:** Efficiency
- **Question:** Q5
- **Source Finding:** F-18, F-19
- **Owner area:** the 14
- **What:**
  - A connection save is several bounded calls (A-43).
  - The scrubber runs at boot, once per device.
  - The content transfer's ceiling moves with `RCLONE_NET_OPTS` (PL-02).
  - webkitgtk keeps DMABuf off by default.
  - rclone is 1.75.2 on the image and 1.60.1-DEV on the host.
- **Evidence:** P1, P10
- **Can this be done on the VM?** Yes: the guest's timings for the menus that call them
- **Already written:** nothing persisted
- **Acceptance:** recorded in `04` Q4 and Q5
- **Disposition note:** **Resolved** -- recorded at `3a7fdb0ec2` (`02` F-18, F-19; `04` Q4, Q5)

## PL-23: `backuptool restore` plants a symlink an archive carries, and a revert that meets a restored-into directory fails (a `bug`, #1136; found in the guest window)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-24
- **Owner area:** projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool (`foreign_member()` `:551-558`; the revert)
- **What:**
  - A standalone symlink member (`storage/.config/t17-link -> /var/tmp/...`) passes the name check, and the installed restore reports success with the link in place.
  - A symlink member with a child fails in `tar`, and the revert reports *"SOME OF YOUR SETTINGS COULDN'T BE PUT BACK"*, leaving the child's directory and `.restore-in-progress`.
  - A hard link, then a file, fails cleanly.
- **Evidence:** P21 (`guest-cycle/pl18.out`; `backuptool` identical to `8ebaf8daad`, `guest-cycle/hashes.out`)
- **Can this be done on the VM?** Yes. It was, in the window. A host fixture of `foreign_member` with member types, plus the full restore on the guest, is the bug's VM line.
- **Already written:** a device that restored such an archive holds the link, and a fix to the check cannot see it; a device with the mark left keeps it until the next boot's verify (T1's `chksysconfig`)
- **Acceptance:** the coordinator's ruling: a `bug` with that fixture (types other than regular files and directories refused before extraction; the revert of a restored-into directory), or recorded
- **Disposition note:** **Resolved** -- `479cd96c24`, S7 under `t17-streams.md` at `8e6c990a1f` (`stage-e/s7-*.txt`; `last-good-scripts-test` PASSED); bug #1136, its criteria ticked

## Phase 7 resolution gate

The coordinator's dispositions at the stage-D pause (#664, 07:5x UTC) and at the hand-back ([issuecomment-6411280450](https://github.com/pixelelated/distribution/issues/664#issuecomment-6411280450) and the second reading, 09:1x UTC), each read back from the tracker at stage F (09:11:37 UTC: #1127, #1117, #909, #665, #663, #1128 to #1133 and #1136 open; #1134 open).

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | **Resolved** | `59a5a8860e`, S1 under `t17-streams.md` (before `stage-e/s1-before.txt`, after `stage-e/s1-after.txt`); bug #1128, its criteria ticked, open until on `next`; the guest met `--expect unfixed` on the installed file |
| PL-02 | **Resolved** | `1def91bdfc`, S2 under D-CLOUD-185 (`stage-e/s2-*.txt`, both cases with the donor's rclone); bug #1129, its criteria ticked; T16's twins routed to #663 by the coordinator; the guest proved the loss on the real paths (`guest-cycle/f02.out`) |
| PL-03 | **Resolved** | `f8feb15bb4`, S3, corrected at `c3e260861b` (explicit names only; `last-good-scripts-test` PASSED; `stage-e/s3-*.txt`); bug #1130, its criteria ticked; the guest proved the upload on the real path (`guest-cycle/f03.out`) |
| PL-04 | **Resolved** | `0ffe7cd94f`, S4 (`stage-e/s4-*.txt`); bug #1131, its criteria ticked |
| PL-05 | **Resolved** | `3e95bf18f4`, S6 for `cloud_setup:797` (`stage-e/s6-*.txt`); bug #1133, its first criterion reworded by the ruling [issuecomment-6411280450](https://github.com/pixelelated/distribution/issues/664#issuecomment-6411280450) and ticked; `backuptool:1495`'s French pair and the why table's pairs are T18's, #665 |
| PL-06 | **Resolved** | `1d8271a1f3`, S5 for `--set-systems` (`stage-e/s5-*.txt`); bug #1132, its criteria ticked; the other three hardenings recorded at `3a7fdb0ec2` (`02` F-10) |
| PL-07 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-21), the stage-D ruling |
| PL-08 | **Resolved** | `0ffe7cd94f`, S4's sweep (`stage-e/s4-after.txt`); in #1131 |
| PL-09 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-07); the setup page's words are the ES slice's |
| PL-10 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-05), a design note |
| PL-11 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-22) |
| PL-12 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-23) |
| PL-13 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-08) |
| PL-14 | **Resolved** | `59a5a8860e`, S1's escape (`stage-e/s1-after.txt`, `paste-html: escaped`); in #1128 |
| PL-15 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-11), a design note |
| PL-16 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-12) |
| PL-17 | **Deferred** | deferred:#1127 (the two tool defects, the coordinator's Backlog under #1047) and #1117 (the validator's `rclone` from `PATH`, M7's) |
| PL-18 | **Resolved** | the guest window's full restore (`guest-cycle/pl18.out`) found F-24, the coordinator's `bug` #1136, fixed by S7 `479cd96c24` (`stage-e/s7-*.txt`) |
| PL-19 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-15; `04` Q1), a proposal |
| PL-20 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-16; `04` Q6); removals none |
| PL-21 | **Deferred** | deferred:#909, the line the coordinator posts at acceptance |
| PL-22 | **Resolved** | recorded at `3a7fdb0ec2` (`02` F-18, F-19; `04` Q4, Q5) |
| PL-23 | **Resolved** | `479cd96c24`, S7 under `t17-streams.md` at `8e6c990a1f` (`stage-e/s7-*.txt`; `last-good-scripts-test` PASSED); bug #1136, its criteria ticked |

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-01, F-09"
  outcome: "resolved (59a5a8860e)"
- id: PL-02
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-02"
  outcome: "resolved (1def91bdfc)"
- id: PL-03
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-03"
  outcome: "resolved (c3e260861b)"
- id: PL-04
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-20"
  outcome: "resolved (0ffe7cd94f)"
- id: PL-05
  severity: Low
  category: Standards
  question: Q2
  source_finding: "F-14"
  outcome: "resolved (3e95bf18f4)"
- id: PL-06
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-10"
  outcome: "resolved (1d8271a1f3)"
- id: PL-07
  severity: Info
  category: Correctness
  question: Q3
  source_finding: "F-21"
  outcome: "resolved"
- id: PL-08
  severity: Info
  category: Correctness
  question: Q3
  source_finding: "F-06"
  outcome: "resolved (0ffe7cd94f)"
- id: PL-09
  severity: Info
  category: Standards
  question: Q2
  source_finding: "F-07"
  outcome: "resolved"
- id: PL-10
  severity: Info
  category: Design
  question: Q3
  source_finding: "F-05"
  outcome: "resolved"
- id: PL-11
  severity: Info
  category: Correctness
  question: Q3
  source_finding: "F-22"
  outcome: "resolved"
- id: PL-12
  severity: Info
  category: Correctness
  question: Q3
  source_finding: "F-23"
  outcome: "resolved"
- id: PL-13
  severity: Info
  category: Correctness
  question: Q3
  source_finding: "F-08"
  outcome: "resolved"
- id: PL-14
  severity: Info
  category: Correctness
  question: Q3
  source_finding: "F-09"
  outcome: "resolved (59a5a8860e)"
- id: PL-15
  severity: Info
  category: Design
  question: Q3
  source_finding: "F-11"
  outcome: "resolved"
- id: PL-16
  severity: Info
  category: Design
  question: Q3
  source_finding: "F-12"
  outcome: "resolved"
- id: PL-17
  severity: Info
  category: Currency
  question: Q4
  source_finding: "F-13"
  outcome: "deferred:#1127"
- id: PL-18
  severity: Info
  category: Design
  question: Q3
  source_finding: "F-04"
  outcome: "resolved (479cd96c24)"
- id: PL-19
  severity: Info
  category: Design
  question: Q1
  source_finding: "F-15"
  outcome: "resolved"
- id: PL-20
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-16"
  outcome: "resolved"
- id: PL-21
  severity: Info
  category: Documentation
  question: Q7
  source_finding: "F-17"
  outcome: "deferred:#909"
- id: PL-22
  severity: Info
  category: Efficiency
  question: Q5
  source_finding: "F-18, F-19"
  outcome: "resolved"
- id: PL-23
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-24"
  outcome: "resolved (479cd96c24)"
```
