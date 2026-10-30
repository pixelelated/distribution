## 1. My own findings

File names below are the packet’s basenames. **Excerpt** means the finding uses one of the three trimmed scripts. These are code findings, not tests I ran.

- **G-01 — High — `cloud_backup:372`, `cloud_restore:359` (excerpt):** GNU `timeout`, without `--foreground`, creates a separate process group. Stopping the script’s process group can therefore leave the automatic downloader alive too; F-03 is not confined to signalling one PID. **Trigger: a stop.**
- **G-02 — High — `cloud_sync_helper:569–578,590–616`:** The migrations write their “applied” markers without checking whether `sed` succeeded. If editing fails but `touch` succeeds, the old setting is permanently exempted from migration—including the destructive `BACKUPMETHOD=sync` setting described at `cloud_sync_helper:548–552`. **Trigger: nobody—a write failure while upgrading an old conf.**
- **G-03 — Medium — `cloud_saves_root:56–84`:** Card identity comes from a lexical path-prefix lookup, without resolving symlinks or decoding mount-table escapes. A saves path through a symlink to the removable card can identify the parent filesystem instead, so swapping the actual saves card does not change the reported identity. **Trigger: the player’s own conf plus a card swap.**
- **G-04 — Medium — `cloud_saves_root:70–84,130–164,166–195`:** Failed identity probes can produce the successful-looking value `dev:unknown`; with no record, or an existing identical value, `check` accepts it, and `record`/`accept` can persist it. An unknown card becomes an accepted identity rather than a refusal. **Trigger: nobody—failed filesystem probes.**
- **G-05 — Medium — `cloud_sync_helper:81–98,119–145,175–177`:** Writes to the temporary user-rule files are unchecked. If `/tmp` cannot hold them, the helper can install a complete defaults-only allowlist and silently discard the player’s exclusions; checking the final catch-all does not detect that loss. **Trigger: nobody—temporary-storage failure.**
- **G-06 — Medium — `cloud_sync_helper:79–98,132–177`:** A truncated existing rules file is merged into the defaults, not refused or recovered from its good `.bak`. Missing custom exclusions are therefore lost while the rebuilt catch-all makes the result look whole. **Trigger: the player’s interrupted rules edit, including a power cut or stop.**
- **G-07 — Medium — `cloud_sync_cleanup_duplicates.sh:15–25`:** Any trailing backslash on a duplicate assignment is treated as a continuation, even one inside a trailing shell comment. A valid line such as `LOG_LEVEL="DEBUG" # comment \` can make cleanup delete the following real assignment. **Trigger: the player’s own conf.**
- **G-08 — Medium — `cloud_restore:238–249` (excerpt):** Failure to create the FIFO disables the deliberate run’s stall guard and starts an untracked foreground `rclone` instead. The failure of the bounding machinery removes the bound precisely when the script should retain one or refuse. **Trigger: nobody—a temporary-directory/FIFO failure.**
- **G-09 — Medium — `cloud_backup:8,1395–1403`, `cloud_restore:347–359` (excerpt), `cloud_saves_root:106–113`:** The automatic deadline and card-wait deadline use wall time. A backward clock correction extends the wait; in particular, the card wait runs outside the rclone timeout. These are not elapsed-time bounds. **Trigger: nobody—a clock correction.**
- **G-10 — Medium — `cloud_restore:1595–1597,1908–1913` (excerpt):** `restore-tree-clean` is written even if the partial-file sweep fails. A read-only or failing saves card can leave partials behind while the writable internal cache records “clean”; later successful runs then skip the sweep. **Trigger: a card fault or card swap.**
- **G-11 — Medium — `cloud_sync_helper:79–82,119,169,343,367,524–625`:** The helper has no lock of its own and shares fixed scratch names between invocations. Concurrent calls can truncate or rename each other’s rules/config candidates, breaking the check-then-install sequence. **Trigger: nobody—overlapping legitimate helper calls.**
- **G-12 — Medium — `cloud_sync-rules.txt:10–19`, `cloud_sync-rules.txt.defaults:21–30`:** The database exclusions omit `.sqlite-wal`, `.sqlite-shm`, and the corresponding `.sqlite3` sidecars. The database itself is excluded while those files are admitted under fully included save directories, defeating the stated protection against syncing database pieces separately. **Trigger: the player’s cloud contents.**
- **G-13 — Low — `cloud_restore:1595–1597,1897–1913` (excerpt), `cloud_sync-rules.txt:18–19`:** The sweep deletes every `*.????????.partial`, not just files known to belong to an interrupted transfer. On a first/dirty-tree restore, an admitted cloud file such as `savestates/note.abcdefgh.partial` can be downloaded successfully and then deleted while the transfer still reports success. **Trigger: the player’s cloud contents.**
- **G-14 — Low — `cloud_saves_root:131–141,166–195`; `guest-cycle/host-leads/k15-at-the-run/out`:** The empty-record refusal tells the player to retry, but `check` refuses that same empty record on every retry, regardless of which cards are inserted. Explicit `record`/`accept` can recover it; the advertised retry cannot. **Trigger: a power cut or stop leaving an empty record, as planted by KILL15.**
- **G-15 — Low — `cloud_net_ready:107–108,130–169,197–208`:** The advertised `N + GRACE` bound does not include the full cost of slow NetworkManager calls: `NOW` is sampled before the probes, and each probe gets five seconds rather than the remaining budget. The five-second timeouts also have no forced-kill deadline. **Trigger: nobody—a slow or stuck local NetworkManager call.**
- **G-16 — Low — `cloud_sync_helper:569–578`, `cloud_sync.conf:124–129`:** A fresh device using `copy` receives no copy-migration marker. Its owner’s first later, deliberate change to `sync` is consequently rewritten to `copy`, despite the conf saying that an explicitly configured mirror is honoured. **Trigger: the player’s own conf.**
- **G-17 — Low — `package.mk:54–58`:** `unpack()` returns the status of the final removal, not extraction. If `unzip` fails and `rm` succeeds, unpack reports success and deletes the archive needed to retry. **Trigger: nobody—a build/extraction failure.**
- **G-18 — Low — `cloud_net_ready:65–74,121–123`:** The numeric check accepts leading-zero durations, but bash arithmetic treats them as octal: `010` means eight seconds and `08`/`09` cause arithmetic errors. **Trigger: nobody through the listed data inputs; a caller supplying such a `--wait` argument.**
- **G-19 — Low — `cloud_sync.conf:40–45`, `cloud_sync.conf.defaults:40–45`, `cloud_sync_helper:462–467`:** Both configuration documents say a missing `CONTENT_REMOTE` is derived from the existing saves layout; the helper explicitly supplies the fresh default instead. The upgrade instructions describe the opposite of the implementation. **Trigger: nobody; the misleading advice concerns the player’s upgrading conf.**

## 2. Refuting the first reader

### F-01 — **Agree: Medium**, with a correction to the claimed effects — excerpt

The unchecked replacement followed by `source` is visible in both twins: `cloud_backup:1209–1225` and `cloud_restore:1258–1274`. The reported `fixtures/load-config-fallback.sh` result, `sourced_refused=YES`, supports that trace.

The assertion that this defect “is a read” and writes nothing does **not** survive: the fixture demonstrates execution of a refused command that creates a file. The execution is as root, but its input here is the owner’s own conf, not an outside attacker.

**It would be false if** a failed copy/rename stopped the run, or sourcing used a verified replacement independently of that failure. **The packet shows neither.** The fixture proves a failed-copy path, not an actual full-card experiment.

### F-02 — **Narrow the empty-path claim; raise the combined finding from Low to Medium** — excerpt

The empty-path result is settled. `cloud_restore:1758–1760` ignores failed directory creation, and `cloud_restore:1902–1906` passes `/` as the destination. The shipped backup directory is inside that destination (`cloud_restore:1869–1871`).

`guest-cycle/host-leads/b-empty-savespath/out` shows both writable-root and read-only-root arms failing **before any save transfer**, with the exact overlap error. It also shows the backup twin refusing earlier. Thus:

- “The current empty-path restore writes saves into `/`” is **false**.
- “The script itself rejects the empty destination” is **false**.
- “The observed restore is stopped by rclone’s overlap check” **survives**.

That narrow empty-path failure remains **Low**. The **combined parser disagreement is Medium**: an accepted, non-default path with a trailing comment can be sourced by the twins while the card checker and capture use `/storage/roms` instead (`cloud_sync_helper:277–280`; `cloud_saves_root:46–50`; `cloud_capture:193–198`, excerpt). Unlike the empty case, that disagreement need not create an overlap and can check or record the wrong saves tree.

**It would be false if** the readers agreed on accepted paths and restore rejected an empty destination before rclone. **They do not.** Removing `--backup-dir` without adding that destination guard would remove the demonstrated protection.

### F-03 — **Agree: High; reject “script PID only” as the full condition** — excerpt

The host evidence is decisive for the tested stop:

- TERM at +5 seconds does not run the trap until +41 seconds.
- Killing the script leaves `timeout` and `rclone` alive.
- The orphan replaces the game’s ten-byte save with the cloud’s 6 MiB file, with no retained copy.

Those are direct observations in `guest-cycle/host-leads/e-term-automatic/out` and `out-game`, matching the foreground call at `cloud_restore:359`, the trap at `cloud_restore:2318`, and descriptor closure at `cloud_restore:2324`.

The condition is broader because of **G-01**: GNU `timeout` has its own process group here. A kill of the script’s group is not automatically a kill of that timeout group. The deliberate KILL2 group-stop result does not answer that automatic-path question.

**It would be false for the interface if** its stop terminates and waits for **all** writers—including the timeout group—before launching the game. **That interface behaviour is not supplied.** Backgrounding a child is also not, by itself, protection against SIGKILL to its parent; that signal cannot run cleanup.

The host establishes the defect. It does not establish the actual EmulationStation stop wiring or the exact timing on the guest’s bash/coreutils versions.

### F-04 — **Narrow; retain Low**

The wording drift is directly established for exit 7: `guest-cycle/host-leads/b-empty-savespath/out` prints `YOUR CLOUD WOULDN'T TAKE THE FILES`, while the supplied `es-player-text.md` Outcome vocabulary specifies `YOUR CLOUD REFUSED THE TRANSFER`.

I cannot independently verify the complete list of other script phrases: the relevant `why_for` and reachability bodies were trimmed out. Nor can I verify a mismatch with EmulationStation’s actual fallback map.

**It would be false if** the applicable rule permitted those alternative sentences, or the alleged differing script text were not emitted. **The supplied rule and exit-7 output establish the narrower documentation defect.** No Medium or High grade is justified.

### F-05 — **Re-grade Medium → Low**

The useless probes are real: `guest-cycle/host-leads/d-terminal-width/out` reports an unsupported flag and 23–24 ms probe times on that host. The helper also constructs temporary config/rules files even when its eventual comparison finds no change (`cloud_sync_helper:119–156,367,479–485`).

The Medium performance verdict is not established. The packet explicitly records that `tools/time-to-play --vm` was **not run**. A list of work is not a measured breach of the three-second exit budget.

The network helper’s initial three-second observation is also its stated settling contract, not independently a defect (`cloud_net_ready:9–12,197–201`). G-15 concerns exceeding its bound, a different issue.

**The wasted-probe finding would be false if** the flag existed or the probe were avoided. **The binary output disproves that.** A Medium budget finding needs the missing device timing.

### F-06 — **Agree, narrowed: Low** — excerpt

The supplied `tools/t16-functions.py … --markdown` output supports the reported dead-function reachability result. The unsupported display probes are independently established by `guest-cycle/host-leads/d-terminal-width/out`.

The post-transfer offset at `cloud_backup:1539` cannot read the transfer’s already-written log entries. But do not remove the whole `logged_moved` call on that basis: its stderr input remains a separate source (`cloud_backup:349–354,1535–1539`). “Can never match” is too absolute for a log another process can append to.

**The separate claims would be false if** a caller existed, the flag were supported, or the offset preceded the transfer. **The packet shows no caller, rejects the flag, and shows the late offset.** I cannot independently reconstruct all callers from the excerpts.

### F-07 — **Re-grade Low → Medium**

Both defects survive, and both can change where saves go—not merely untidy the conf.

The substring test can mistake a comment naming `KEY=` for an actual setting (`cloud_sync_helper:462–467`). The verbose migration operates on the entire file and collapses spaces inside every value (`cloud_sync_helper:536–542`). A legitimate folder containing two spaces is changed when this migration runs; syntactic validation alone would not catch that change.

**It would be false if** key detection matched assignments and the edit affected only the intended option value while preserving folder text. **Neither protection is present.** The shipped conf not triggering it does not excuse corruption of the supported owner-edited conf.

### F-08 — **Re-grade Low → Medium** — excerpt

The failed-read-to-delete path is explicit: the process substitution’s jq status is not checked, and an empty or incomplete reference set permits deletion of old seals (`cloud_capture:1649–1652,1673–1686`).

These are copies supporting current manifest claims, not expendable temporary output: that relationship is stated at `cloud_capture:15–23`. A missing reconciler limits immediate transfer impact; it does not make deleting referenced save versions harmless.

**It would be false if** failure to obtain a complete keep-list cancelled GC. **The shown code does not do that.** This is a Medium preservation defect without needing to claim that today’s transfer scripts consume the stage.

### F-09 — **Agree with the verified portion: Low** — excerpt

Two corrections are directly supported:

- The no-lock comment in `102-cloud-saves:40–46` conflicts with the actual capture-lock calls reported by command output **r10**.
- The “no gensub” comment at `cloud_restore:764–765` is disproved by `guest-cycle/host-leads/a-awk/out`.

The existence of `last-restore` is also directly demonstrated by the host lead outputs, including `b-empty-savespath/out`.

**These would be false findings if** capture took no lock, the shipped awk lacked `gensub`, or no restore stamp existed. **The supplied outputs show the opposite.** I cannot independently verify the full mid-run-69 stamp branch because its implementation is omitted.

### F-10 — **Agree, narrowed: Low**

`package.mk:54–58` plainly removes the downloaded archive, including the architecture-renamed copy.

“Every rebuild fetches again” is broader than the supplied recipe establishes: an incremental build need not unpack, and the surrounding build system’s other caches are not shown. The defensible finding is that **a rebuild needing this archive cannot reuse it from this source-cache location after unpack**.

**It would be false if** unpack retained the archive there. **It explicitly deletes it.** The stronger no-DNS rebuild claim needs the surrounding build/cache behaviour.

### F-11 — **Agree as a design proposal, not a defect**

The reported function-generator output—39 shared functions, 34 identical—supports reducing duplication. The helper’s validator is visible at `cloud_sync_helper:240–323`; the packet reports the corresponding twin copies in its function analysis.

**The maintenance argument would fail if** these bodies required independent behaviour rather than shared implementation. **The reported byte identity supports the proposal.** It does not establish that an arbitrary library extraction is safe, or replace testing of the five differing shared functions.

### F-12 — **Narrow; retain Low** — excerpt

Ignoring TERM is explicit at `cloud_capture:129–136`, and the boot hook starts the full pass detached at `102-cloud-saves:54–56`.

The actual shutdown delay is not demonstrated. The relevant service configuration, stop timeout, and full-mode bound checks are not supplied as source, and no shutdown timing was measured.

**The shutdown-impact claim would be false if** the worker had already finished or an enclosing supervisor bounded and stopped it independently. **The packet does not settle that.** The overly broad TERM immunity survives as a code concern; a measured shutdown regression does not.

### F-13 — **Agree: Low** — excerpt

The unquoted settings-directory creation is visible at `cloud_restore:1993`. An unquoted option-splitting loop also appears at `cloud_backup:1395–1400`. The final bare `cloud_saves_root check --wait` case really does retain its argument after failed `shift 2`, so its loop repeats (`cloud_saves_root:124–129`).

**These would be false if** directory arguments were quoted, option splitting prevented pathname expansion, and `--wait` required a following argument before shifting. **Those protections are absent at the shown sites.**

I do **not** raise this to Medium or High: the packet does not demonstrate save loss from these particular cases. The complete `RCLONEOPTS` parsing claimed in the finding remains partly trimmed.

### F-14 — **Re-grade Medium → High; narrow the ordering claim** — excerpt

The missing-save defect survives unequivocally:

- `guest-cycle/cells-3.out` records two live save names absent after each stop arm.
- `guest-cycle/host-leads/f14-backup-dir-order/out` records all three originals under `replaced/run1`, with no completed replacement and only a partial in the saves tree.
- The enabling option is visible at `cloud_restore:1869–1871`.

Keeping bytes in a cache is not keeping the player’s save available to the game. Under the stated priority, this is **High**, even without claiming those cached bytes are already irrecoverable.

The literal universal claim **“every save is moved before any transfer” does not survive as stated**. The evidence establishes early moves before replacement completion; its sampled progress already includes 220 KiB transferred. It does not establish a global all-checks-before-any-byte barrier for every run. The defect needs no such barrier.

The partial-file admission is also proven by the donor’s `lsf` output. But “litter forever” is false for the demonstrated rerun: KILL2’s final check and `cloud_restore:1908–1913` show cleanup. G-10 identifies a separate failure of that cleanup guarantee.

**The missing-save finding would be false if** originals remained at their live paths until replacements were ready, or interruption restored them before returning. **Both guest stop arms disprove that protection.**

### F-15 — **Agree: Low, oracle-only**

`tools/cloud-round-trip:7763–7766` applies the run-outcome assertion to `cloud_saves_root check` itself. `guest-cycle/host-leads/k15-at-the-run/out` shows that each actual twin supplies the required final outcome sentence and leaves the local save unchanged.

**The oracle criticism would be false if** the helper’s raw output were itself the player-facing run surface being tested. **No such surface is shown; the supplied twin runs demonstrate the proper boundary.**

That does not clear the separate recovery-advice defect in **G-14**. Correct outcome vocabulary is not proof that “try again” can recover the condition.

## 3. What I could not judge

### Claims hidden by trimming

The packet’s description promises more coverage than the supplied excerpts actually contain. In particular, substantial cited bodies—and most of `cloud_backup`’s main—are absent. These claims need the missing source:

1. **All validator copies and the complete configuration-loading contract.** The twins’ `conf_valid` bodies at `cloud_backup:1107–1190` and `cloud_restore:1156–1239` are not supplied. Much of both `load_config` bodies is absent too. I cannot independently verify their equality, all required-key checks, option sanitisation, `--delete-excluded` removal, duplicate-cleanup/re-source ordering, or protection against assigning internal variables such as `RCLONE_OUTER` and run-control flags.

2. **Complete stop cleanup and stamp handling.** `cloud_backup:905–933` and `cloud_restore:898–926`—the `clean_exit` implementations—are absent. So are most stamp-writing bodies. I cannot certify child termination/reaping on every path, `.bak` removal rules, stamp-write failure handling, or the exact `69 gaps` branches. The supplied stop outputs prove their recorded cases, not every cleanup path.

3. **The backup’s full call sequence and option construction.** Most of `cloud_backup:2407–2489` and substantial parts of `cloud_backup:1582–1960` are missing. I cannot independently certify phase ordering, all early exits, effective transfer methods, allowlist enforcement for every option combination, or the complete recency-window behaviour.

4. **The restore’s preflight and post-transfer card handling.** Much of `cloud_restore:1625–1755`, `1769–1860`, and `1922–1950` is absent. I cannot certify all remote-absence decisions, custom filter handling, card checks, or the final record/no-write decisions. The empty-path and stopped-restore outputs establish their specific failures despite that gap.

5. **Settings-archive transfer and retention safety.** Large parts of `cloud_backup:1965–2406` and `cloud_restore:1955–2198` are absent. I cannot verify archive selection and integrity checking end to end, remote filename handling, all upload confirmations, or whether every retention deletion follows the required successful verification.

6. **All player-facing error mappings.** The complete `why_for`, `check_internet`, `network_lost_during_run`, and outcome-formatting bodies are omitted. Beyond the supplied command outputs, I cannot verify F-04’s entire wording inventory or all outcome/exit combinations.

7. **The dead-code and copy-equality claims from source.** The packet supplies the generator’s result, which is evidence for its reported counts. It does not supply enough source to reconstruct every call edge, rule out indirect calls, or independently compare all 34 bodies.

8. **Capture mode parsing and path safety.** Most of `cloud_capture:354–763` and `1110–1585` is absent. I cannot certify argument rejection, path containment, unit/member discovery, adopt/rescan behaviour, or the precise files accepted for `--retire --unlink`.

9. **Capture’s preservation and concurrency protocol.** The full `seal` implementation, manifest loading/transformation, lock functions, retry logic, and commit sequence are omitted (`cloud_capture:252–352,804–1106,1585–1639`). I cannot certify independent-copy verification, concurrent-writer detection, the exit bound’s enforcement, or atomicity of retirement relative to unlink.

10. **Capture’s final reporting and size-limit behaviour.** The excerpt ends at `cloud_capture:1690`; its remaining tail is absent. I cannot judge the complete handling of stage size, final status, or failure reporting after GC.

### Evidence absent for reasons other than trimming

- **Actual EmulationStation invocation and stopping.** No `ThreadedCloudSync`, launch gate, or transfer-page implementation is supplied. The automatic stop needs PID/PGID or cgroup evidence; the recorded automatic host tests signal the script PID, while the recorded guest group-stop test uses the deliberate shape (`e-term-automatic/out`; `cells-3.out`).
- **Guest timing for F-03, F-05, and F-12.** The host identifies its substituted bash/coreutils versions, and the guest-cycle record explicitly says `tools/time-to-play --vm` was not run. No shutdown measurement is supplied.
- **Power-cut durability.** KILL15 plants an empty record (`tools/cloud-round-trip:7762`); it does not interrupt persistent storage writes. Temp-and-rename code such as `cloud_saves_root:94–100` is not, by itself, evidence of survival across power loss.
- **External callees and other writers.** `cloud_remote`, `cloud_device_id`, `cloud_log_scrub`, settings extraction, and the content scripts are not supplied. In particular, I cannot verify the shared `restore-tree-clean` protocol or whether an updater takes the transfer lock before invoking the helper.
- **The whole oracle.** Apart from `fx_kill15`, the harness implementations are not supplied. The generated row descriptions and recorded results do not let me audit every assertion or turn unrun cells into evidence.
- **Current upstream package currency and all supported-image variants.** The recipe pins 1.75.2 (`package.mk:7,36–47`), and the donor tests establish that binary’s observed behaviour. The packet contains no current-release lookup or equivalent observations for every architecture.

**The strongest conclusions need no additional evidence:** the tested stopped restore leaves live save names absent, and the tested orphaned automatic restore destroys a save written after the stop (`cells-3.out`; `e-term-automatic/out-game`). Both deserve High priority.