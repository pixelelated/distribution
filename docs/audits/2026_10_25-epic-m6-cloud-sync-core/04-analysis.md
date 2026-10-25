# T16 analysis: the cloud sync core (#663)

The first reader's analysis (Opus 5.5, high effort), written before the
seats and before the guest window. A finding marked **(window)** has its
deciding observation in the window's plan (`#663`, 11:52 UTC); its grade
here is provisional until § The guest cycle in `02` carries the record.

## Executive Summary

The core is the most defended code in the fork. Every outcome is written
temp-and-rename. Every bound is applied in one wrapper. The allowlist is
refused when its catch-all is missing, and the sentinels sit above rclone's
range. **The read tree implements D-CLOUD-109/130, not the superseded
D-CLOUD-076**: no launch-cancel path exists in the scripts, and an
automatic run is bounded from its start.

What the read finds are **guards that fall open when their own machinery
breaks**, two **copies that disagree**, and **cost on the exit path**:

| ID | Question | Severity | The finding | proved: |
| --- | --- | --- | --- | --- |
| F-01 | Q3 | Medium | `load_config` (identical in both twins) sources the conf `conf_valid` refused when the `.bak` put-back's `cp` fails, as on a full card: a torn file is run with, and a refused line executes | fixture |
| F-02 | Q3 | Medium (window) | an empty or commented `SAVESPATH` passes `conf_valid`; the `sed` reader of `cloud_saves_root`/`cloud_capture` reads the default instead, and the restore copies `remote:<SAVES_REMOTE>/` into `/` | fixture, tree |
| F-03 | Q3 | Medium (window) | an automatic run's TERM waits behind its foreground `timeout ... rclone` (up to the ceiling's remainder); a TERM-then-KILL to the script alone leaves the transfer running orphaned. KILL2, the oracle's stop cell, runs the deliberate shape, whose `wait` is interruptible | fixture, tree |
| F-04 | Q2 | Low | the `>>> why` sentences for rclone 3/4 and 7/8 differ from `es-player-text.md`'s rc list, and two the scripts print are in no table; the ES fallback map that must change with them is unread | tree |
| F-05 | Q5 | Medium (window) | every twin run, the exit sync's included, starts `cloud_sync_helper` (a rules merge with a `grep` per rule line, two `conf_valid`s, a pass over the defaults); the restore's saves phase and the backup's settings phase each start `rclone help`; `cloud_net_ready` holds 3 s from its own first look on any startup | tree |
| F-06 | Q6 | Low | dead code: `controller_menu`, `get_controller_devices` and `device_folder` in `cloud_restore` (76 lines, no caller); `cloud_backup:2054-2056` adds a flag its loop drops at `:2170`; `logged_moved` at `:1539` reads `LOG_FILE` from its size after the transfer | tree |
| F-07 | Q3 | Low | `cloud_sync_helper` adds a missing key only when no line contains `KEY=` anywhere (`:462`, unanchored `grep -F`); its `-v` edit rewrites the conf in place with no `conf_valid` after (`:536-544`) | tree |
| F-08 | Q3 | Low | the capture's stage GC reads its keep-list from a `jq` whose status is not checked (`:1649-1652`): a failed read keeps nothing, and every seal older than 600 s goes | tree |
| F-09 | Q7 | Low | two comments state invariants the code stopped keeping (`cloud_backup:69-71`, `102-cloud-saves:44`); the brief's "there is no `last-restore`" is the same shape in a document | tree |
| F-10 | Q4 | Low | `package.mk`'s `unpack` deletes the download from the shared source cache (`:58`), so every rebuild fetches rclone again and a container without DNS cannot rebuild it | tree |
| F-11 | Q1 | design | the twins share 34 byte-identical functions and the helper carries a third `conf_valid`: one sourced library would make the gate one thing | design |
| F-12 | Q3/Q5 | Low (window) | the capture ignores TERM (`:136`); its exit mode is bounded at 100 s, its boot `--full` is not, so a pass still running at power-off holds the stop until systemd's kill | tree |
| F-13 | Q3 | Low | unquoted expansions: `mkdir -p ${SETTINGS_BACKUPS}` (`cloud_restore:1993`); `for opt in ${RCLONEOPTS}` (both twins), which globs; `cloud_saves_root check --wait` as the last argument loops for ever on bash's failed `shift 2` (`:126`) | tree |

## Acceptance-criteria scorecard

The slice's criteria are #663's seventeen (brief § 7). At stage C:

| Criterion | State |
| --- | --- |
| folder `00`-`05` | `00`-`04` written; `05` at stage D |
| lint `PASS` | pre-issue lint at stage C's end |
| review plan and provenance | after the seats |
| punch-list issue at Phase 7 | stage D onward |
| `reviewed-at` / `fixed-at`; the 14 at `8ebaf8daad`; nothing under `packages/`, `projects/`, `tools/` | run r2 empty; run r24 empty |
| `01` § Scope | done |
| `02` § Coverage 14 | done (`awk ... | grep -c` prints 14) |
| `02` § The functions 132 | done, generated |
| `02` § The oracle | done, generated; the counts are under Q2 below |
| `02` § The stamps and locks; § The configuration | done |
| `02` § The runs | done |
| `02` § The guest cycle | after the window |
| `00` shows no build, fetch, handheld, hosted account | so far |
| `04` § Q3 bugs with three lines; § Q2; § Q6; § Q7; § Second opinion | Q3-Q7 below; the seats after the window |
| `proved:` cells; `question:` cells | `02` every table; `05` at stage D |
| retro | stage G |
| the five checkers | at hand-back |

## Risk Assessment

- **Highest:**
  - F-02's restore into `/` is the one finding that writes where nothing should. On a device `/` is read-only squashfs, so the likely outcome is a failed restore with rclone's errors; the window shows which.
  - F-03 matters if EmulationStation stops the startup sync by signalling the script alone. That is the ES slice's to read; the window shows what the scripts do under it.
- **Data at risk from F-01:** a torn conf run with missing keys. `SAVES_REMOTE` unset sends a backup to the cloud's root folder.
  - The guard was written for exactly this (D-CLOUD-078, #105).
  - It holds unless the card is full, which is when a torn write is most likely.
- **No finding loses a save already in the cloud:**
  - `copy` is the default both ways;
  - `--delete-excluded` is stripped;
  - `--backup-dir` keeps every replaced copy for one cycle.

## Coverage Boundary

- **Read:** the 14 at `8ebaf8daad` (`02` § Coverage); the harness at `8ebaf8daad` for the oracle; `cloud_content_restore:780-795` for the shared `restore-tree-clean` record (T17's file, one paragraph).
- **Named, not read:** EmulationStation's `ThreadedCloudSync`, `FileData::launchGame`, `GuiCloudTransfer`, `CloudText`. These are the ES slices': how ES invokes and stops these scripts, and its why fallback map.
- **T17's callees:** `cloud_remote`, `cloud_device_id`, `cloud_log_scrub`, `cloud_scan` and the content scripts. Their call sites are read; their internals are not.

## Finding Verification (Phase 4.5)

Each finding was re-read at its lines after `02` was written. Each has a
proof:
- **F-01:** the fixture `fixtures/load-config-fallback.sh`, against both twins at `8ebaf8daad`.
  - With `cp` working, the refused conf is replaced by the `.bak`, nothing it holds runs, and the conf is valid after.
  - **With `cp` failing** (the planted input, standing for a full card), its planted line ran (`sourced_refused=YES`), `load_config` returned 0, and the conf was still the refused one.
  - The same in both twins.
- **F-02:** the readers' disagreement is a fixture (`02` § The configuration). The restore's path is read at `cloud_restore:1758-1760, 1902-1906`; the window settles what it does.
- **F-03:** `fixtures/trap-defer.sh`. A TERM at +1 s ran the trap at +6 s, when the foreground `timeout -k 3 6` child returned (bash runs a trap only between foreground commands). `cloud_backup:372` and `cloud_restore:359` run the automatic call in the foreground; `bounded_rclone` (deliberate) backgrounds it and `wait`s, which a trap interrupts.
- **F-04 to F-13:** read at their lines; each cell above names them.

## Renovation face

### Q1 Modernize

- **F-11, the copy-twin as a design.**
  - 34 of the 39 shared functions are byte-identical (`tools/t16-functions.py`); the 5 that differ do so in a handful of lines.
  - `conf_valid`, the gate that decides what root sources, is in three files.
  - One library sourced by the twins and the helper (`/usr/lib/cloud_sync/common.sh`, say) would make each fix one fix. #307's audits fixed the gate three times, each time in each copy.
  - **A proposal for the coordinator, no edit here.**
- **The three stamp families:** a design sentence.
  - The twins own `last-<run>` and the upload marker;
  - the capture and `cloud_saves_root` own the manifest, its stage and the card;
  - EmulationStation owns `last-sync-<origin>`.

  No file says so. Q7 asks for that sentence.
- **`102-cloud-saves`' detached `--full`:** off the boot's critical path by design (D-CLOUD-057, D-CLOUD-064). Its cost is F-12's at power-off, not at boot.

### Q2 Standards and best practices

- **The oracle verdict.**
  - T13's 79 rows: 25 both ends (`CONTRACT` among them; T13's `04` `:228` names the 24 of the 78: steps 2, 5, 8, 17, 18, 19, 22, 23, 27, 32; A1, A2, A8, A9, A11, A14, RETENTION; LINK2, LINK3, LINK5, LINK6; KILL1, KILL4 (conditional), KILL5), 46 synthetic and 8 device report. No delta.
  - **56 rows run one of the nine scripts**, 8 of them through a harness helper; 15 run only T17's.
  - **This slice trusts, at `3a653eaec4`, the both-ends verdicts of the rows that run its scripts:** steps 2 and 5, A2, A8, A11, A14, LINK2, LINK5, LINK6, KILL1, KILL4 (conditional), KILL5 and `CONTRACT`. Steps 22 and 23 also run `cloud_backup` by name, and A1 and A9 run it through a helper.
  - It does not take a synthetic row as evidence about an input, nor a device-report row as evidence about the code.
  - A5 and RETENTION SKIP (#1057).
  - **The gap the read finds is in the stop:** KILL2, the one cell that stops a run as EmulationStation does, runs the deliberate flags. The automatic run, which is what ES stops at a launch, is not in any KILL row (F-03).
- **The twins' discipline:**
  - `set -o pipefail` appears once in the capture (`seal`'s hash, `:1081`) and nowhere in the twins. Their pipelines that reach a decision are `md5sum | md5sum` (`cloud_backup:2114`, failing toward a send) and `lsf | grep` (`:1566`, failing toward removing nothing). Both fail safe.
  - `set -u` is in none of the nine.
  - The unquoted expansions are F-13's.
- **The conf against its defaults:** 16 and 16, nothing on one side only (run r12).
  - The allowlist's 54 rule lines are the same in the file and its `.defaults`; the 23 differing lines are comments (run r13).
  - The two conf readers disagree on values the gate passes (F-02).
- **F-04, the why sentences:**
  - The scripts and `es-player-text.md`'s rc list disagree on 3/4 (`COULDN'T FIND YOUR CLOUD FOLDER` against `YOUR CLOUD FOLDER WASN'T FOUND`) and 7/8 (`YOUR CLOUD WOULDN'T TAKE THE FILES` against `YOUR CLOUD REFUSED THE TRANSFER`; the D-UI-031 table agrees with the scripts).
  - `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` and `COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN` are in no table.
  - The rule's half is #909's. Whether `ThreadedCloudSync`'s fallback map moved with the scripts is the ES slice's.
- **Busybox:** the scripts run under the image's busybox.
  - `cloud_sync_cleanup_duplicates.sh` calls `gensub`, which `cloud_restore`'s `near_names` comment says busybox awk lacks.
  - `tools/last-good-scripts-test` A48 runs the cleanup and passes, so the comment or the host test's awk is wrong. The window reads `awk` on the image (plan step 5a).

### Q3 Bugs

**Which design the tree implements:** D-CLOUD-109/130. The scripts have
no path that cancels on a launch. The automatic run carries a deadline
from its start (`load_config`, `cloud_backup:1403`), and the `rclone()`
wrapper starts nothing past it (`:366-369`). The superseded D-CLOUD-076 is
not filed against.

**Bug decisions.** Each bug is filed at stage D with these three lines, a
defect in a twin as one bug naming both files:

- **F-01, a bug.**
  - *Trace:* `load_config` at `cloud_backup:1209-1222` and `cloud_restore:1258-1271`. `conf_valid` refuses; `cp -f .bak .tmp.$$ && mv -f .tmp.$$ conf`, neither status read; then `if ! source "${conf}"`, which runs whatever the file holds. A failed `cp` (no space) leaves the refused file in place and a partial `.tmp.$$` beside it. `bash -n` passed the file or `conf_valid` would have said so first, so `source` succeeds and the run goes on.
  - *Already written:* nothing on a device or in a cloud is written by the defect, which is a read. A fixed reader inherits a refused conf and perhaps a `cloud_sync.conf.tmp.<pid>` left by a failed copy. The fix refuses (`YOUR CLOUD SYNC SETTINGS COULDN'T BE READ`) when the put-back does not leave a file `conf_valid` passes, and removes its own temp.
  - *VM line:* `fixtures/load-config-fallback.sh` against the twins is the host proof. On the VM a full `/storage` is planted with `fallocate` on the disposable guest and the run's sourcing observed; that is stage E's, not this window's.
- **F-02, a bug (window).**
  - *Trace:* `conf_valid` passes `SAVESPATH=""` (fixture). `cloud_restore:1758` tests `[ ! -d "" ]` (true) and runs `mkdir -p ""`, which fails and is ignored. `:1902-1906` copies into `"${SAVESPATH}/"`, which is `/`. `cloud_saves_root:46-51` and `cloud_capture:193-198` read the default `/storage/roms` for the same file.
  - *Already written:* any conf a device holds with such a value (none ships); what a restore into `/` wrote, which the window shows.
  - *VM line:* plan step 5b.
- **F-03, a bug if the window or the ES slice shows ES signals the script alone (window).**
  - *Trace:* `cloud_backup:372` runs the automatic call as `command timeout -k 3 "${left}" rclone ...` in the foreground. The `INT TERM` trap at `:2504` runs only when it returns (`fixtures/trap-defer.sh`). A KILL to the script leaves `timeout` and `rclone` running with no parent; the lock is released, since fd 9 is closed in the body.
  - *Already written:* a stamp is not written by a KILLed run, so `last-*` keeps the previous run's. What an orphaned restore wrote under a running game is the window's question.
  - *VM line:* `cloud_restore --automatic --yes --saves-only` throttled on the QA WebDAV, TERM to the script, then `ps` and the cloud and local trees read.
- **F-07, F-08, F-12, F-13:** Low. Each a proposal with its trace in `05`; none is filed as a `bug` unless the window shows an effect on a player's data.

### Q4 Package currency

- **rclone 1.75.2**, a binary zip pinned per arch with its SHA256 (`package.mk`, verified against `SHA256SUMS`, #541).
  - Its author's current release: **CANNOT (no network)**.
  - `tools/fork-package-freshness` is the tool, and is not run (it reads the network).
- **Upstream relation:** nil. ROCKNIX has not changed the directory since the base (run r19).
- **T13's fixes this slice's rows depend on**, all in `tools/` at `3a653eaec4`:
  - #1059 (the restore's empty-cloud exit);
  - #1067 (the SFTP endpoint);
  - KILL1's commit-model expectation;
  - A15's backup landing;
  - CAP13's warning.
- **F-10**, the recipe's `unpack`, is a build-path finding: no player sees it.

### Q5 Efficiency

The exit sync's budget is D-CLOUD-119's 3 s.

- **Measured median:** cited from `docs/vm-qa-log.md` and, if the window allows, re-measured by `tools/time-to-play --vm`.
- **What runs on that path, by the code:**
  1. `cloud_backup`'s top level;
  2. `take_cloud_lock` (at most 1 s when contended);
  3. `check_network_link` (`ip route`);
  4. `check_rclone_config`;
  5. **`cloud_sync_helper`**: a log trim, a rules merge with one `grep -F` per rule line (54), two `conf_valid` runs (`bash -n` and awk), a pass over the defaults with one `grep` per key, and four `grep`/`sed -i` one-shots;
  6. `load_config` (`conf_valid` again, `source`, about 15 `echo | sed | tr` pipelines on `RCLONEOPTS`);
  7. `first_remote` (`cloud_remote`, python3);
  8. the saves phase:
     - `cloud_saves_root check --wait 15`;
     - `find | head -1`;
     - `remote_compares_by_size` (awk over `rclone.conf`);
     - with `--recent`, no `mkdir` and `--no-traverse`;
     - one rclone;
     - `cloud_saves_root record`;
  9. with the settings phase, **`rclone help`** (F-06) and a `rclone size` per archive.
- **Each step's cost** is the window's to time (plan step 5c). F-05 is graded from that, not from this list.
- **`cloud_net_ready`'s 3 s grace** is counted from its own first observation (`cloud_net_ready:199`), so a startup sync on a link up for hours still waits about 3-4 s before it starts. Whether ES runs it on the launch path is the ES slice's.

### Q6 Dead ends

- **Functions with no caller (F-06):** `cloud_restore`'s `controller_menu` (632-693), `get_controller_devices` (616-628, called only by `controller_menu`) and `device_folder` (1476-1482). 76 lines.
  - `cloud_backup` and `cloud_capture` have none (`tools/t16-functions.py`, `uncalled`).
  - **Removals none here**: each is a proposal on the punch list for the coordinator (D-WORKFLOW-209's last clause).
- **Code that runs and does nothing:**
  - `cloud_backup:2054-2056` (`rclone help` for `--progress-terminal-width`, which `:2170` drops); the restore's settings phase has the same pair at `:2028-2030` and `:2173`;
  - `logged_moved`'s `LOG_FILE` half at `cloud_backup:1539` and `cloud_restore`'s twin, whose offset is taken after the transfer.
- **Options parsed and never used:** none. Every `--` option of the twins, the capture, `cloud_net_ready` and `cloud_saves_root` reaches a branch.
- **`gamelist.xml:64,76`'s** `./cloud_backup.sh` and `./cloud_restore.sh` tool entries point at symlinks `post-update:81-86` removes and `package.mk` no longer installs: a dead end in the modules package's slice (the coordinator's lead).

### Q7 Clarity and structure

Can a reader tell, from the directory and the rule, which script runs
when, under which lock, writing which stamp, and on which card the saves
are?

- **Which script runs when:** partly.
  - The scripts' headers say: boot (`102-cloud-saves`: the scrub, then the capture's `--full`), a game's exit (ES: the capture, then `cloud_backup --automatic`), an update (`post-update`: the helper), a menu row (ES: the twins).
  - No one file lists the four, and `102-cloud-saves`'s comment on the lock is stale (F-09).
- **The locks:** two (`02` § The stamps and locks).
  - The twins' header explains theirs at length.
  - The capture's header explains its own and says it never takes the other; its boot hook's comment says it takes none.
- **The stamps:** three families, never named as families anywhere. The twins' `last-<name>` is built at run time, so a literal search finds no `last-restore`: it misled the brief (F-09).
- **The card:** `cloud_saves_root` is clear, and every caller states what it does with a refusal.
- **The rule:** `rclone-cloud-sync.md` carries #909's drift. Its `:375` still says `tools/cloud-round-trip` asserts "the exit-4 timing"; the scripts and the harness use 69.

## Instruction File Recommendations

- **`rclone-cloud-sync.md`**:
  - a short table of the three stamp families and the two locks, with their owners (Q7);
  - the sentence that a conf value the gate passes may be read by two readers (`source` and the `sed` extraction) that disagree on comments, quotes and empties (F-02).

  These are proposals for #909's owner; this lane edits no rule.
- **`engineering-practices.md` § Guards must fail closed:** F-01 is that rule's shape in a fallback. A fallback whose copy fails must not fall through to the thing it replaced. It is offered as an example, not a new rule.

## Second opinion (Phase 4.6)

Not run yet. Astra then Argon, a probe and a refutation each, after the
guest window's record is in `02`, over the packet `tools/t16-packet.py`
builds from `02`, `03`, this file and the 14 at `8ebaf8daad`.

## Quality Self-Check

- **Every finding names its lines and its proof.** The three marked (window) say what observation decides them.
- **Not checked:**
  - how EmulationStation invokes and stops the scripts (named, not read);
  - the capture's lines 1110-1585 line by line (read for writes, removals, `jq` calls and exits);
  - rclone's own currency (no network).
- **The first draft of `02`'s leads carried six line numbers from a comment-free listing**, corrected from the file before its commit. The same check ran over this file's numbers.
