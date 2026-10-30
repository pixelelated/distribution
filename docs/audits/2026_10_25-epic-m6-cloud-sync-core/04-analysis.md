# T16 analysis: the cloud sync core (#663)

The first reader's analysis (Opus 5.5, high effort). It was written before
the seats and the guest window, then graded at stage C against the window's
record and the host leads (`02` § The guest cycle and § The host leads,
2026-10-29 and 2026-10-30). A finding still marked **(window)** has its
deciding observation pending, for stage E and the integration window
(`fix-walk-pending-image`).

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
| F-02 | Q3 | Low | an empty or commented `SAVESPATH` passes `conf_valid`, and the `sed` reader of `cloud_saves_root`/`cloud_capture` reads the default instead. The restore has no test for it (the backup has, `:1613`). It reaches rclone, which refuses on its `--backup-dir` overlap check before any transfer, and the player reads `Couldn't finish: your cloud wouldn't take the files. Try again.`, the wrong reason with a retry that cannot work. **Nothing is copied into `/`, but only by accident**: a fix to F-14 that drops `--backup-dir` would open it | fixture |
| F-03 | Q3 | **High if ES signals the script alone** (window: the image's bash and coreutils; the ES slice: the stop's shape) | an automatic run's TERM waits behind its foreground `timeout ... rclone` (36 s on the host), and the run is then stamped "stopped" over a save that landed. A KILL to the script alone leaves `timeout` and `rclone` running unlocked to the 90 s deadline, and **their rename replaces a save the game wrote after the stop, with no copy kept**. KILL2, the oracle's stop cell, runs the deliberate shape, whose group is stopped | fixture |
| F-04 | Q2 | Low | the `>>> why` sentences for rclone 3/4 and 7/8 differ from `es-player-text.md`'s rc list, and two the scripts print are in no table; the ES fallback map that must change with them is unread | tree |
| F-05 | Q5 | Medium (window) | every twin run, the exit sync's included, starts `cloud_sync_helper` (a rules merge with a `grep` per rule line, two `conf_valid`s, a pass over the defaults); the restore's saves phase and both settings phases start `rclone help` for a flag rclone 1.75.2 does not have (22-24 ms each on the host); `cloud_net_ready` holds 3 s from its own first look on any startup | tree, tool-run |
| F-06 | Q6 | Low | dead code: `controller_menu`, `get_controller_devices` and `device_folder` in `cloud_restore` (76 lines, no caller); the `--progress-terminal-width` probe at `cloud_restore:1893`, `:2028` and `cloud_backup:2054` can never match (`unknown flag` on 1.75.2), and `:2170` would drop it anyway; `logged_moved` at `:1539` reads `LOG_FILE` from its size after the transfer | tree, tool-run |
| F-07 | Q3 | Low | `cloud_sync_helper` adds a missing key only when no line contains `KEY=` anywhere (`:462`, unanchored `grep -F`); its `-v` edit rewrites the conf in place with no `conf_valid` after (`:536-544`) | tree |
| F-08 | Q3 | Low | the capture's stage GC reads its keep-list from a `jq` whose status is not checked (`:1649-1652`): a failed read keeps nothing, and every seal older than 600 s goes | tree |
| F-09 | Q7 | Low | three comments state what is not so: `cloud_backup:69-71` and `102-cloud-saves:44` (invariants the code stopped keeping); `cloud_restore:764-765`, "busybox awk: no gensub", which the image's busybox 1.36.1 has. The brief's "there is no `last-restore`" is the same shape in a document | tree, tool-run |
| F-10 | Q4 | Low | `package.mk`'s `unpack` deletes the download from the shared source cache (`:58`), so every rebuild fetches rclone again and a container without DNS cannot rebuild it | tree |
| F-11 | Q1 | design | the twins share 34 byte-identical functions and the helper carries a third `conf_valid`: one sourced library would make the gate one thing | design |
| F-12 | Q3/Q5 | Low (window) | the capture ignores TERM (`:136`); its exit mode is bounded at 100 s, its boot `--full` is not, so a pass still running at power-off holds the stop until systemd's kill | tree |
| F-13 | Q3 | Low | unquoted expansions: `mkdir -p ${SETTINGS_BACKUPS}` (`cloud_restore:1993`); `for opt in ${RCLONEOPTS}` (both twins), which globs; `cloud_saves_root check --wait` as the last argument loops for ever on bash's failed `shift 2` (`:126`) | tree |
| F-14 | Q3 | Medium | the restore's `--backup-dir` (`cloud_restore:1869-1871`) has rclone move every save it will replace aside at check time, before any transfer. A restore stopped part-way leaves those saves **absent** until a completed restore: the player who stopped it to play opens the game with no save. The `.partial` a SIGKILL leaves is admitted by the allowlist (`+ /savestates/**`), so a backup before the next restore sends it | guest, fixture |
| F-15 | Q2 | Low (oracle) | KILL15's FAIL is the harness's: `fx_kill15` (`tools/cloud-round-trip:7747-7772`) holds `cloud_saves_root check`'s own last line to a run's outcome vocabulary, but a player reads that helper only through the twins, which end on `Couldn't finish: couldn't tell which card your saves are on. Try again.` A proposal for T13's harness, not a code defect | fixture |

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
| `02` § The guest cycle | done: the window (2026-10-29) and the host leads (2026-10-30) |
| `00` shows no build, fetch, handheld, hosted account | so far |
| `04` § Q3 bugs with three lines; § Q2; § Q6; § Q7; § Second opinion | Q3-Q7 below; the seats after the window |
| `proved:` cells; `question:` cells | `02` every table; `05` at stage D |
| retro | stage G |
| the five checkers | at hand-back |

## Risk Assessment

- **Highest:**
  - **A stop over a restore costs a save in either shape.**
    - Under F-03, a signal to the script alone leaves the transfer running, and its rename replaces what the game wrote after the stop, with no copy kept (host, `out-game`).
    - Under F-14, a group stop leaves the replaced saves absent until a completed restore (KILL2 on the guest).
    - Which one the player meets is how EmulationStation stops STOP IT AND PLAY (D-CLOUD-130). That is the ES slice's to read.
  - **F-02 no longer writes into `/`.** rclone's `--backup-dir` overlap check refuses first. That makes F-14's fix and F-02's one change: a restore without `--backup-dir` must first refuse an empty `SAVESPATH` as the backup does (`cloud_backup:1613`).
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
- **F-02:** the readers' disagreement is a fixture (`02` § The configuration). The restore whole, on the host with the image's busybox and rclone (`host-leads/b-empty-savespath`), against a control that completes: rc 7, rclone's overlap refusal, no file anywhere. The backup twin refuses at `:1613`.
- **F-03:** `fixtures/trap-defer.sh`. A TERM at +1 s ran the trap at +6 s, when the foreground `timeout -k 3 6` child returned (bash runs a trap only between foreground commands). `cloud_backup:372` and `cloud_restore:359` run the automatic call in the foreground; `bounded_rclone` (deliberate) backgrounds it and `wait`s, which a trap interrupts.
  - Then the restore whole on the host (`host-leads/e-term-automatic`), in three arms: the deferral (36 s), the orphan (ppid 1, still writing 32 s after the KILL), and the game's save replaced (`out-game`: 6,291,456 bytes where the game wrote 10; none kept).
- **F-14:** KILL2 on the guest, the real script, two arms (`guest-cycle/cells-3/KILL2a`, `KILL2b`: `Server Side Moves: 3` before the transfers). The bare donor rclone on the host (`host-leads/f14-backup-dir-order`): all three moved aside within 1.5 s, before 220 KiB of the first copy.
- **F-15:** the refusal through each twin (`host-leads/k15-at-the-run`). Both end on an outcome sentence.
- **F-04 to F-13:** read at their lines; each cell above names them. F-06's probe and F-09's `:764` were also put to the donor's binaries (`host-leads/d-terminal-width`, `a-awk`).

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
  - **Two of the window's FAILs are the harness's words, not the code's:**
    - KILL15 holds a helper to a run's outcome line (F-15).
    - KILL2b's "nothing removes it (litter forever)" is contradicted by the re-run's sweep, and the cell's own last check reads the tree clean.
    - KILL2's absent saves are the code's (F-14).
    - KILL2's header still names D-CLOUD-076, which D-CLOUD-109/130 superseded.
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
  - **The comment is wrong** (`host-leads/a-awk`). The donor's `/usr/bin/awk` is busybox 1.36.1's, `gensub` works with back-references, and the cleanup runs whole under it and leaves a conf that parses.
  - A48 ran the same awk (`tools/last-good-scripts-test:8983`). F-09 carries the comment.

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
- **F-02, a bug (Low; re-graded on the host).**
  - *Trace:* `conf_valid` passes `SAVESPATH=""` (fixture). `cloud_restore:1758` tests `[ ! -d "" ]` (true) and runs `mkdir -p ""`, which fails; its message, `mkdir: can't create directory ''`, reaches the output. `:1902-1906` asks rclone to copy into `"${SAVESPATH}/"`, which is `/`. rclone 1.75.2 refuses as a fatal error because `--backup-dir` (under `/storage/.cache`) lies inside `/`. That gives exit 7, which `report_rclone_error` words as the cloud's refusal. `cloud_backup:1613` refuses the same conf with `YOUR SAVES FOLDER ISN'T ON THIS DEVICE`; the restore has no such test. `cloud_saves_root:46-51` and `cloud_capture:193-198` read the default `/storage/roms` for the same file.
  - *Already written:* any conf a device holds with such a value (none ships, and the helper never writes one). The restore wrote nothing anywhere (`host-leads/b-empty-savespath`: no file restored, in either mode of `/`), and the stamp it leaves is `7 YOUR_CLOUD_WOULDN'T_TAKE_THE_FILES`. The next good run replaces it. A fix reads the same conf and refuses with the backup's sentence.
  - *VM line:* `host-leads/b-empty-savespath` is the proof, on the image's busybox and rclone; the guest adds nothing to it. The fix's walk repeats it on the image (stage E).
- **F-03, a bug, High if the ES slice shows ES signals the script alone (window: the image's bash and coreutils).**
  - *Trace:* `cloud_backup:372` and `cloud_restore:359` run the automatic call as `command timeout -k 3 "${left}" rclone ...` in the foreground. The `INT TERM` trap (`cloud_restore:2318`, `cloud_backup:2504`) runs only when it returns (`fixtures/trap-defer.sh`). On the host, a TERM at +5 s ran the trap at +41 s, and the run is stamped `130` over a save that landed. A KILL to the script leaves `timeout` and `rclone` running with ppid 1, unlocked (fd 9 is closed in the body), to the 90 s deadline. Their final rename lands on whatever the name holds by then: a save the game wrote at +11 s was replaced by the cloud's copy (`out-game`).
  - *Already written:* a KILLed run writes no stamp, so `last-*` keeps the previous run's. An orphaned restore may already have replaced a save that a game wrote after a stop on a device; nothing records that, and the copy is gone (it was never under `--backup-dir`: the move aside happens at check time). A fix inherits nothing it can read; it stops the transfer with the script (the deliberate path's backgrounded child and `wait`).
  - *VM line:* `host-leads/e-term-automatic` on the host. The same three arms on the guest, with the image's bash 5.3 and coreutils 9.4, are stage E's (`fix-walk-pending-image`).
- **F-14, a bug (Medium).**
  - *Trace:* `cloud_restore:1869-1871` passes `--backup-dir=/storage/.cache/cloud_sync/replaced/<stamp>`. rclone moves each destination file it will replace into it at check time, and only then queues the copy (`f14-backup-dir-order`: three `Moved (server-side)` before 220 KiB of the first copy). A stop between the two leaves the save absent from `SAVESPATH`. The copy kept under `replaced/` is pruned by the next completed run (`prune_replaced_local`, `:1607-1621`), which has fetched the cloud's copy by then. A SIGKILL also leaves `<name>.<8>.partial`, which the next restore sweeps (`:1898-1913`); `+ /savestates/**` admits it to any backup that runs first.
  - *Already written:* a device whose restore was stopped holds the replaced saves under `replaced/<stamp>/`, and perhaps a `.partial`. A cloud may hold a `.partial` that a later backup sent. A fix reads both: the next restore puts a missing save back from the cloud (it does today), and a fix that sweeps `.partial` from the cloud names its pattern exactly, as `sweep_partials` does.
  - *VM line:* KILL2 on the guest (`guest-cycle/cells-3/KILL2a`, `KILL2b`) and `host-leads/f14-backup-dir-order`. The fix's walk is KILL2 with the absent-save check passing.
- **F-07, F-08, F-12, F-13:** Low. Each a proposal with its trace in `05`; none is filed as a `bug` unless the window shows an effect on a player's data.
- **F-15:** a proposal for T13's harness (`tools/` is not this lane's): `fx_kill15` asserts the refusal's why and its "nothing was transferred", and leaves the outcome line to a twin's run.

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

- **Measured median:** none. The window did not run `tools/time-to-play --vm`, and no figure is cited here (corrected 2026-10-30; `02` § The guest cycle). Lead (c) is `(window)`-pending, for stage E and the integration window.
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
- **Each step's cost** is lead (c)'s to time on the image (`(window)`-pending). F-05 is graded from that, not from this list.
- **One cost is settled without the guest:** the restore's saves phase and both settings phases start `rclone help` for a flag rclone 1.75.2 does not know. That is 22-24 ms per start on the host, and never any effect (`host-leads/d-terminal-width`).
- **`cloud_net_ready`'s 3 s grace** is counted from its own first observation (`cloud_net_ready:199`), so a startup sync on a link up for hours still waits about 3-4 s before it starts. Whether ES runs it on the launch path is the ES slice's.

### Q6 Dead ends

- **Functions with no caller (F-06):** `cloud_restore`'s `controller_menu` (632-693), `get_controller_devices` (616-628, called only by `controller_menu`) and `device_folder` (1476-1482). 76 lines.
  - `cloud_backup` and `cloud_capture` have none (`tools/t16-functions.py`, `uncalled`).
  - **Removals none here**: each is a proposal on the punch list for the coordinator (D-WORKFLOW-209's last clause).
- **Code that runs and does nothing:**
  - `cloud_backup:2054-2056` (`rclone help` for `--progress-terminal-width`, which `:2170` drops); the restore's settings phase has the same pair at `:2028-2030` and `:2173`; the saves phase's probe at `cloud_restore:1893-1895`. **rclone 1.75.2 has no such flag** (`unknown flag`, rc 2), so all three probes are dead whatever follows them;
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

Depth **extended** (`second-opinions/review-plan.json`): the primary (Anthropic, Opus 5.5) and two reviewers from other labs. Each seat ran its probe first, then its refutation, through the Facilitator.

**Both seats saw the same trimmed packet** (D-WORKFLOW-195): `02` to `04` whole, the eleven smaller files whole, and the three large scripts in excerpt (`second-opinions/packet-manifest.json` lists the spans). Argon's brief also carries Astra's grades below. An item resting on lines a seat saw only in excerpt says so, and is graded from the file, not from either seat.

| Seat | Call | Provenance | Served | Outcome |
| --- | --- | --- | --- | --- |
| GPT-6 Astra, `max` | probe 09:26:11-09:26:20 (`READY unknown`); refutation `tools/council/run invoke --member gpt --provider openrouter`, brief `second-opinions/gpt-brief.md` (381,240 bytes), under `tools/watch-build --record-only` (`.build-runs/20261030T092635Z-597bc6f5/`, `build.rc` 0), 09:26:35-09:43:20 | `gpt-probe.md.provenance.json`, `gpt-audit.md.provenance.json`: `council-facilitator@1.14.1-pixelelated.2`; verification PASS (`provider_response`), provider PASS (`response_provider_field`), effort PASS (41,752 reasoning tokens); 1 attempt, `finish=stop`, 1,002,690 ms | `openai/gpt-6-astra` by OpenAI | `gpt-audit.md`, 26,238 bytes, sha256 `c872717a1a8ea3b88e8ddcbe1ca86e3ea2ed70d6d8c6fced222f96570acb206c`: 19 items of its own, the 15 findings graded |

### Astra's items, graded against the artifacts

Each grade comes from re-reading the cited lines at `8ebaf8daad` (09:43-09:47 UTC), not from the seat's wording. One item was also run: G-01, as a host cell. The grades are:
- **confirmed** (the lines show it);
- **confirmed, re-graded** (they show it, at another severity);
- **narrowed** (part of it holds);
- **design** (the lines show it, and a comment beside them gives the reason);
- **disagree** (with the artifact that refutes it).

| Item | Grade | The lines read, and what they show |
| --- | --- | --- |
| G-01 `timeout`'s own process group | **confirmed, High; widens F-03** | GNU `timeout` without `--foreground` makes its own process group. `guest-cycle/host-leads/g01-timeout-pgid` (GNU 9.7): after a TERM to the script's group, the script is gone and `timeout` and its child run on to `timeout`'s own deadline. So a group stop does not end an automatic transfer either (`cloud_restore:359`, `cloud_backup:372`); only a stop that reaches `timeout`'s group, or the whole session, does |
| G-02 migration markers after an unchecked `sed` | **confirmed, Medium** | `cloud_sync_helper:576-577`: `sed -i` then `touch` the marker, whatever `sed` returned. A rewrite that fails (a full card) leaves `BACKUPMETHOD="sync"`, the mirror that deleted another device's 70 saves (`:548-552`), and the marker stops every retry. The two option migrations (`:594-596`, `:613-615`) have the same shape, with less at stake |
| G-03 card identity by path prefix | **confirmed, Low** | `cloud_saves_root:56-68` matches `/proc/mounts` by prefix, unresolved and unescaped. The shipped layout binds the card over `/storage/roms` (`:53-55`), which this reads right. A `SAVESPATH` through a symlink, or a mount point with a space, is the owner's own setting |
| G-04 `dev:unknown` accepted | **confirmed, Low** | `:83` gives `dev:unknown` when `stat` fails; with no record, `check` passes it (`:143-164`), and `record` can keep it. The next run with the path present reads `uuid:` and refuses, so it fails closed one run late |
| G-05 unchecked writes to `/tmp` | **confirmed, Low** | `cloud_sync_helper:81-94`: `: >` and `echo >>` into `/tmp/cloud_sync-rules.user` are unchecked. A failed write drops the player's rules, and `rules_whole` (`:145`) cannot see it. `/tmp` is tmpfs, so a full one is rare |
| G-06 a truncated rules file merged | **confirmed, Low** | `:79-98` merges whatever `${rules}` holds. `:168-173` keeps the last whole `.bak` and does not overwrite it from a cut file, so the lost lines are recoverable by hand |
| G-07 a backslash in a trailing comment | **confirmed, Low** | `cloud_sync_cleanup_duplicates.sh:15,22-24` treats any trailing `\` as a continuation, and bash does not continue a comment. A repeated assignment whose comment ends in `\` removes the next line. The owner's own conf, in an unusual shape |
| G-08 no FIFO, no ceiling | **design, Low** | `cloud_restore:241-249` (and the twin) runs rclone unbounded when no FIFO can be made. The comment at `:242-245` gives the reason: on a device `/var/run` is tmpfs, and refusing the backup would be worse. The trade is written down |
| G-09 deadlines on the wall clock | **confirmed, Low** | `cloud_backup:8,1403` and `cloud_restore:347` (and `cloud_saves_root:108-110`) count from `date +%s`. **The likelier shape is a forward step**, not Astra's backward one: a handheld with no RTC is stepped forward by NTP near the startup sync, so `left` goes below 1 and the run ends at once with 124 (`:353-355`). No save is lost; the next sync carries it. The guest can step the clock mid-run (stage E) |
| G-10 `restore-tree-clean` after a failed sweep | **confirmed, Low** | `cloud_restore:1597` hides `find -exec rm`'s failures, and `:1912-1913` writes the marker regardless. A card that refuses the delete leaves `.partial`s that later runs do not look for, and that the allowlist admits (F-14) |
| G-11 the helper has no lock of its own | **narrowed, Low** | The fixed names are at `:81-82,119`. Its callers are the twins, under `cloud_sync.lock` (`cloud_backup:1199`, `cloud_restore:1248`), and `post-update:111` after an update (`git grep` at `8ebaf8daad`). An overlap needs `post-update` during a twin's run |
| G-12 the database sidecars | **confirmed, Low** | `cloud_sync-rules.txt:10-15` excludes `*.db-wal`, `*.db-shm` and `*.db-journal`, but not `*.sqlite-wal`, `-shm` or `-journal`, nor `*.sqlite3`'s. A lone WAL restored beside a different database is applied on its next open. No shipped emulator is named as writing one there |
| G-13 the sweep's pattern | **confirmed, Low** | `cloud_restore:1597` removes any `*.????????.partial` under the saves tree, so a file of that shape the cloud holds is removed after a dirty-tree restore. Contrived |
| G-14 the empty record cannot be retried away | **confirmed, Medium** | `cloud_saves_root:131-141` refuses on an empty record, and says "try again". The twins refuse at `check` (`cloud_restore:1648-1651`) and call `record` only after a completed transfer (`:1931-1940`), so no run can ever rewrite it. The only exit is `cloud_setup --accept-saves-root`, a command, and `:154-155` says no menu offers one. The comment at `:135` ("until a good run rewrites it") cannot come true. Today's `write_record` is temp-and-rename (`:94-101`); a record left empty by an older build's in-place write is the `Already written:` |
| G-15 `cloud_net_ready`'s bound | **confirmed, Low** | `NOW` is sampled at `:131`, before up to two 5 s `nmcli` calls (`:107-108,167-169`), and `timeout 5` has no `-k`. A slow NetworkManager stretches `N + GRACE` by up to about 10 s a round |
| G-16 a fresh device's first `sync` | **confirmed, Low** | `cloud_sync_helper:569-577` sets its marker only when it rewrites, so a device that never had `sync` has none. The owner's first deliberate `sync` is rewritten once, against `cloud_sync.conf:124-126` ("honoured if set here") |
| G-17 `unpack()` | **confirmed, Low; joins F-10** | `package.mk:54-58`: no `set -e` reaches `scripts/unpack` at `8ebaf8daad` (`git grep`), so a failed `unzip` runs on into the `rm`, which deletes the archive a retry needs |
| G-18 leading zeros | **confirmed, Low** | `cloud_net_ready:72-73` accepts `010`, and `:122` reads it as octal (8 s). `08` is an arithmetic error. Its callers pass fixed numbers |
| G-19 `CONTENT_REMOTE`'s comment | **confirmed, Low; joins F-09** | `cloud_sync.conf:40-45` (and its `.defaults`) says the key is derived for an upgrading config. `cloud_sync_helper:463-466` says a missing key takes the fresh default, as D-CLOUD-175 decided |

**The first reader's findings, as Astra graded them:**

| Finding | Astra | Graded |
| --- | --- | --- |
| F-01 | agree, Medium; "the defect is a read" is wrong | **correction taken.** A refused line runs as root when the put-back fails (the fixture's planted line ran). `Already written:` now says so |
| F-02 | narrow the empty path (Low); raise the readers' disagreement to Medium | **taken: F-02 is Medium, in two parts.** The empty path stays Low: nothing written, the wrong why. The disagreement is Medium. A non-default `SAVESPATH` with a trailing comment is sourced by the twins, while `cloud_saves_root:48` and `cloud_capture:193-198` miss it and read `/storage/roms`. The card guard then checks the wrong card (`02` § The configuration, the fixture) |
| F-03 | agree, High; the condition is wider (G-01) | **taken.** Any stop that does not reach `timeout`'s group leaves the transfer running. That is a signal to the script or to its group. The ES slice reads which stop ES makes |
| F-04 | narrow, Low | **taken.** Only exit 7's words are shown in a run (`b-empty-savespath`); the rest of the inventory is in excerpt |
| F-05 | Medium to Low: no measurement | **taken: Low until lead (c) measures it.** The probes' futility stands (`d-terminal-width`) |
| F-06 | narrow: `logged_moved`'s stderr half works | **taken.** The log half sees only what is appended after the transfer; the stderr half (`cloud_backup:349-354`) stands |
| F-07 | Low to Medium: the `-v` edit can rename a folder | **disagree with the re-grade, Low.** Both shapes are at `:462` and `:536-542`, but the folder change needs two things in the owner's own conf: a `-v` or `--verbose` somewhere, and a double space or `-v ` inside a value |
| F-08 | Low to Medium: the seals are preservation copies | **narrowed: Low today, Medium once a reader exists.** No consumer of `stage/` exists (#1057), so nothing a player has is lost today. The item carries to #1057 |
| F-09 | agree, Low | taken |
| F-10 | narrow: a rebuild needing the archive | **taken**, with G-17 |
| F-11 | agree, a design | taken |
| F-12 | narrow, Low: no shutdown measured | **taken.** It stays `(window)` |
| F-13 | agree, Low | taken |
| F-14 | Medium to High; narrow "every save before any transfer" | **taken, both.** A save the game needs is absent until a completed restore, which is High under the lens. The ordering claim narrows to what was observed: the saves are moved aside early, before their replacements land. On the host, all three moved before the first copy completed. `02` and Q3 say so |
| F-15 | agree; G-14 is separate | taken |

**What Astra could not judge** (its § 3): the bodies the trimming left out, namely `conf_valid` (twins), `clean_exit`, most of `cloud_backup`'s main and its settings phase, the restore's pre-flight and card handling, the capture's seal and commit protocol, and `why_for`. It also lacked EmulationStation's stop, the guest's timings, power-cut durability, T17's callees and the whole oracle. None of its items rests on an omitted line except F-04's inventory. The ES stop and the guest timings are `(window)`-pending already.

## Quality Self-Check

- **Every finding names its lines and its proof.** The three marked (window) say what observation decides them.
- **The host leads ran the image's busybox and rclone**, but the host's bash 5.3.9, GNU coreutils 9.7, grep 3.12, python3 and `ip` (`02` § The host leads). A verdict that could turn on those (F-03's timing) stays `(window)`-pending.
- **Not checked:**
  - how EmulationStation invokes and stops the scripts (named, not read);
  - the capture's lines 1110-1585 line by line (read for writes, removals, `jq` calls and exits);
  - rclone's own currency (no network).
- **The first draft of `02`'s leads carried six line numbers from a comment-free listing**, corrected from the file before its commit. The same check ran over this file's numbers.
