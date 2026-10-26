## 1. Where a secret can travel

**A-1 — narrowed: the credential-file and argv rows are substantially right, but their exposure times are not.**  
Evidence: `cloud_connections.py:129-136,157-180,198,253`; `cloud_remote:85-88,263-265,325-335`; `cloud_oauth:588-594` (excerpt).

The supplied mode fixture confirms 0600 installed files and private staging under its umask; this is access control, not redaction of their contents. The OAuth token is on the configuration subprocess’s argv, **not** the subsequent `lsd` argv, so the first reader wrongly extends that particular exposure through verification. Conversely, a secret supplied to `cloud_remote` remains on that parent’s argv throughout its invocation, including provider lookup and verification; provider lookup has no timeout in the shown helper. The table should distinguish those two lifetimes rather than assign both the configuration subprocess’s 40-second bound.

**A-2 — narrowed: the PIN’s ordinary sinks are identified, but the state-file negative claims are not established.**  
Evidence: `cloud_oauth:187-200,1133,2586-2598,2638-2645,2817-2823` (excerpts).

The PIN and PIN-bearing URL are deliberately written without masking to state and stdout, and the phone template embeds the PIN directly. The supplied fixture observes `session.json` as 0644 in a 0755 directory; its predictable temporary has the same creation discipline and can survive an interrupted write. `write_state()` merges fields rather than enforcing a credential-free schema. The implementations of `read_state`, `_fail_owned`, and the complete failure paths are **outside the packet**, so “no token/code can reach state or its error field” is stronger than this evidence permits.

**A-3 — narrowed: the phone-keyboard path and the connection-form argv path must not be conflated.**  
Evidence: `cloud_oauth:74,516,1235-1288,2406-2409,2437-2457,2490,2586-2587,915-917` (excerpts); `cloud-signin-window.c:525-534,654-668,726` (excerpts).

The paste route accepts a code-bearing body and replays its query to loopback; the advertised LAN endpoint is plain HTTP, not a confidential channel. The keyboard route passes plaintext to `RemoteKeyboard`, while the phone’s password box merely masks display and explicitly permits “Show.” The demonstrated CLI-secret route goes through `cloud_remote`; a bridge from a WebDAV/SFTP phone form to that CLI is **outside the packet**. Debug keystroke logging is another unmasked sink, and the page-record exclusion is a host-specific redirect precaution, not a general scrub of credentials from URLs.

**A-4 — refuted: “rclone’s error carries the URL, not its secret” is not a code-supported guarantee.**  
Evidence: `cloud_setup:495-498,537-543,219-224,926-937` (excerpts); `cloud_remote:329-344`; `cloud_connections.py:131-136`; `cloud_folder_validate:43-50` (excerpt).

`connections.run()` substitutes fixed failure sentences, and the validator deliberately discards diagnostics, but the setup probe forwards two lines of raw stderr to the screen. Nothing there removes credentials from a URL, query, or provider diagnostic. The malformed-pair stderr echo, cleartext root-password display at **937**, and raw SSH-override logging are also real sinks. F-07 therefore has a confidentiality dimension, not merely a player-language defect.

**A-5 — confirmed: a scrubber-recognized shape is still written, though that does not prove a current token leak.**  
Evidence: `cloud_oauth:448,588-594` (excerpts); `cloud_remote:90-96`; `cloud_log_scrub:78-95,104-120,140` (excerpt); `GuiMenu.cpp:7414` (supplied context).

The current OAuth failure log still has family F2’s prefix; the visible save failures supply controlled sentences rather than rclone diagnostics. Several current `Refused` sentences are absent from the scrubber’s historical exception list, so that rule would redact even these harmless details. The ordinary `cloud_remote` helper no longer emits F1’s arguments, while F3’s writer is ES, **not one of these 14 files**. The general `redact_credentials` implementation and ES’s `maskSecrets` implementation are **outside the packet**, so their complete masking coverage cannot be certified here.

**A-6 — narrowed: the device-ID row describes a pseudonym, not a protected secret.**  
Evidence: `cloud_device_id:19-36,133-145,272-302` (excerpts); `backuptool:1030-1046` (excerpt).

The ID and previous-ID ledger are unmasked file contents; the host fixture’s 0644 result is consistent with these writes. A 40-bit unsalted digest of a MAC permits inexpensive candidate testing when the vendor prefix is known, but does not mathematically identify one unique MAC in every case. The stated machine-ID fallback is a different entropy case and should not inherit the MAC-search claim. Exact cloud-folder/log/stdout construction and the complete archive exclusion lists are **outside the packet**; moreover, an archive exclusion alone cannot establish that an unconstrained content backup never carries these files.

## 2. What the deleting path can delete

**A-7 — narrowed: the shown deleting branches are guarded, but “spent before anything is read” is wrong.**  
Evidence: `cloud_content_restore:873-909,914-938,963-980,1011-1052` (excerpt).

The code reads the header and body at 886–888, then removes the plan at 890; it spends the plan before cloud work, not before reading it. Within `match_run`, both deleting statements require `apply=1`, a successfully spent plan, the context checks, and a matching per-system verb/count; the deleting command receives the preview’s count. The CLI dispatcher and implementations of the context/selection helpers are **outside the packet**, so I can certify these local guards, not every possible entry path. These are per-system protections, not a transaction or approval of an immutable set of filenames: earlier systems can already have changed when a later system refuses.

**A-8 — confirmed: F-02 is real and is broader than one dangerous flag.**  
Evidence: `cloud_content_restore:235-279,750-752,1015-1018,1046-1050` (excerpts); supplied content fixture.

The variable reaches `sync` as unrestricted rclone arguments, and the real-rclone fixture demonstrates deletion of an excluded save. It can also supply alternative configuration, filters/file lists, link-following, deletion scheduling, `--ignore-errors`, backup destinations, diagnostic dumps, dry-run behavior, and altered timeout/retry values. Appended fixed arguments may override duplicates, so this is **not** proof that every injected `--max-delete` or log-file value wins. The important failure is that the preview can count forbidden deletions and then legitimately authorize them; the count cap has not been bypassed. The local `delete` statement does not take this array.

**A-9 — narrowed: the wrapper is an argument forwarder, not a verb or flag boundary.**  
Evidence: `cloud_content_transfer:85-95,117-125,141-157`; `cloud_content_restore:750,1046` (excerpts).

`bounded_content_rclone` accepts arbitrary arguments and forwards them to rclone without validating the verb or flags. Both visible restore call sites supply literal `sync`; other transfer call sites needed to prove that *every* verb is fixed are **outside the packet**. Quoted array expansion is not shell evaluation, so an extra word does not thereby become a shell command. The wrapper does fail closed when its guard directory/FIFO cannot be created, but leaves stderr unmasked and provides an inactivity guard rather than a command-policy guard.

**A-10 — narrowed: the recursive removals are mostly ownership-by-convention, not a universal confinement proof.**  
Evidence: `cloud_content_transfer:107-121`; `cloud_content_restore:1271-1278` (excerpt); `backuptool:222-227,1183,1274-1341` (excerpts).

The transfer wrapper removes its checked `mktemp` directory, and the scan trap removes the value returned for its scan temporary. Backuptool’s sweep intentionally removes **every matching staging-prefix object**, not just this invocation’s directory. Its prefix definition, staging allocation, and lock acquisition are **outside the packet**, so the complete “own work only” claim cannot be independently established. The scan’s unchecked allocation causes a separate write-confinement failure described in A-46; it does not turn `rm -rf ""` into a root deletion.

**A-11 — refuted: the pattern kills are not confined to their own attempts.**  
Evidence: `cloud_setup:772-779` (excerpt); `cloud_oauth:354-363,854-863,2817-2819` (excerpts); `cloud_remote:102`.

These patterns match command-line text, not a tracked PID, executable identity, session owner, or the process holding the OAuth port. They can kill unrelated authorizations and, for `rclone config`, configuration readers such as provider enumeration. On a host they can also match a shell or harness whose argv contains those words; the source itself documents that class of failure. The `/proc`-based serve cleanup does not make the remaining `pkill -f` calls safe.

## 3. The phone page

**A-12 — confirmed: F-01’s lockout mechanism is demonstrated, but browser frequency is not.**  
Evidence: `cloud_oauth:2062-2066,2196-2206,2322-2348` (excerpts); supplied PIN fixture.

The first path component of `/favicon.ico` is a nonempty supplied candidate, and the fixture demonstrates that ten such requests exhaust the shared counter and reject the correct PIN. Nine requests remaining usable is a useful control. This proves the handler defect, not that each real browser will generate ten uncached icon requests during an ordinary sign-in. The failure is availability of the phone serve, not successful authentication by the icon requester.

**A-13 — narrowed: the guessing and unauthenticated-response claims need several missing lines.**  
Evidence: `cloud_oauth:2062-2066,2196-2206,2322-2328,2406-2415,2437-2444,2647-2649` (excerpts).

The visible code establishes a uniformly generated four-digit PIN, a ten-failure counter, and a serve timer; the fixture establishes the sequential lockout behavior. The full `_gate` orchestration, server concurrency/socket constants, body-length check, and 600-second default are **outside the packet**, so neither the exact concurrent guessing budget nor all reported limits are independently proved here. A non-exhausting wrong request gets the PIN prompt with a fixed mismatch message, but the empty-PIN branch and complete unauthenticated template are also **outside the packet**. The 409 responses are post-authentication window-availability checks, not additional PIN-guessing defenses. Plain HTTP and a readable PIN file also create paths that do not require guessing.

**A-14 — narrowed: F-09’s attacker-controlled HTML chain is not proved by these excerpts.**  
Evidence: `cloud_oauth:508-520,2460-2463,2482-2490` (excerpts).

An authenticated requester controls the `code` value passed to `submit`, and the restart path constructs an error-containing HTML fragment. However, `submit`’s preceding validation, `failure_reason()` at 480–488, and `_render`/`PAGE` substitution at 2271–2290 are **outside the packet**; rclone’s propagation of attacker-supplied OAuth error text is not demonstrated either. Thus the packet does not establish the complete reflected-HTML exploit chain. Also, the visible code-submission route has no “browser stack absent” condition: that restriction may describe which UI is offered, not which authenticated POSTs are accepted.

## 4. What the content backup takes

**A-15 — narrowed: F-03 proves source-path traversal, not the reported upload’s exact contents and destination.**  
Evidence: `cloud_content_backup:583-585` (excerpt); `cloud_content_restore:1482-1487` (excerpt); supplied content fixture.

The backup accepts the explicit arguments unchanged, unlike the restore’s name validation. The fixture proves an rclone copy invocation with `/storage/roms/../.config` as source, which escapes to `/storage/.config` in the fixture’s directory layout. The source construction at 710, copy at 753, `remote_for`, and the complete exclusion arrays are **outside the packet**. Consequently, the claimed `ROMs/../.config` destination and inclusion of `rclone.conf` are credible hypotheses requiring those lines, not a demonstrated real upload: the traversal case used a recording stub.

**A-16 — confirmed: the backup has another unchecked input surface besides system names.**  
Evidence: `cloud_content_backup:229-234,583-585` (excerpts); `cloud_content_transfer:88,124`.

Its network-options string is split and forwarded without an allowlist, just as on restore. That permits rclone options affecting configuration, scope, link following, and diagnostics—not merely networking. Quoted directory arguments avoid shell evaluation but do not provide filesystem confinement. The backup’s content-root reader, automatic directory enumeration, and complete transfer construction are **outside the packet**, so “the explicit system name is the only unchecked backup input” cannot be accepted.

## 5. The writers

**A-17 — narrowed: writer-table rows 1–7 correctly describe the normal installer, not an unconditional single-writer transaction.**  
Evidence: `cloud_connections.py:72-114,140-215,218-258`; `cloud_remote:264,320-335`.

Normal live-file installation uses `atomic()` under the shared flock, with file and directory fsync; the supplied fixture confirms 0600 replacement even over a 0644 file. But `atomic()` itself takes no lock, first-save rollback unlinks `CONFIG`, and active selection also has a direct `select()` path—not only `save`/`remove` as the retrospective says. Staged files are initially written and then chmodded inside a private directory; the fixture stops before rclone and does not measure every subsequent rclone rewrite. Unchecked option-shaped settings also prevent an unconditional claim that all effective configuration writes reach `atomic()`; see A-45.

**A-18 — narrowed: exception rollback is not kill-safe transaction rollback.**  
Evidence: `cloud_connections.py:74-88,157-160,187-214,238-258`; `cloud_oauth:581-594` (excerpt).

A kill before replacement can leave the original file plus staging/atomic temporaries containing credentials. Between selection publication and configuration publication, a save can leave a pinned old selection, while removal can leave a tombstone with the old credentials still present. After configuration replacement but before OAuth state publication, new credentials can be installed while the interface still lacks a success record. SIGKILL does not execute the exception rollback, and failures during rollback itself are not made transactional. Individual-file fsync is strong, but does not atomically commit credentials, selection, and sign-in state together.

**A-19 — narrowed: rows 8–14 need conditional modes and stronger failure descriptions.**  
Evidence: `cloud_device_id:288-302` (excerpt); `cloud_content_restore:296-302,819-821,873-911,1399-1408` (excerpts); `cloud_content_backup:249-255` (excerpt).

The ID, plan, selection, and stamps use temporary-plus-rename publication; 0644 assumes a newly created temporary under umask 022, while the previous-ID append retains an existing file’s mode. ID/ledger writes and selection writing take no visible lock; preview is explicitly unlocked, apply locked, and all stamp-call-site lock claims require code **outside the packet**. A process kill normally leaves the pre-publication target plus a temporary, but preview has already removed its preceding plan, and an interrupted ledger append can leave a partial record. These shell writers show no fsync discipline comparable to `atomic()`. Most importantly, a failed selection write can still be renamed into place: F-10’s “old count” description misses corruption of the selection itself.

**A-20 — narrowed: rows 15–19 mix observed creation modes with unproved library and caller guarantees.**  
Evidence: `cloud_oauth:175-200,911-917,2132-2136,2707-2715,2750-2754` (excerpts); `cloud-signin-window.c:408,726` (excerpts).

The observed state/lock modes are correct for new files, but opening an existing lock with `O_CREAT,0600` does not repair its permissions. `_write_whole()` performs rename publication without fsync; `write_state()` locks it, while the complete other callers are **outside the packet**. Marker writes are in-place empty-file creation, and the table omits the additional marker write at 2708; `window.log` is truncated immediately and preserves an existing inode’s mode. The GLib implementation/version needed to certify the page/field records’ precise mode, replacement behavior, and crash behavior is **outside the packet**—the mode fixture did not exercise it.

**A-21 — narrowed: rows 20–22 describe the scan layout correctly, but “observed” overstates the fixture.**  
Evidence: `cloud_scan:219-229,272-282,294-295,314-355,358-362` (excerpt).

The scan holds its own flock and writes result files in place, then publishes a completion file through a temporary rename. A kill after removal of the old result set can leave missing or partial results without a newly completed set; this is not atomic publication of the whole directory. The supplied fixture measured a **scan-style redirection**, not each actual scan writer, and existing-file modes depend on whether removal succeeded. Several writes are unchecked, as detailed in A-48, so completion must not be equated with proof that every result was produced whole.

**A-22 — narrowed: rows 23–24 are mostly right, with qualifications to mode and record preservation.**  
Evidence: `cloud_log_scrub:63,136-186` (excerpt).

Changed logs receive the temporary file’s mode, but unchanged logs retain their old mode. A kill before rename leaves the original log and a temporary; after log replacement but before the family record, a later run can repeat the work. The stream has pipefail and useful parity checks, but neither log nor record publication shows fsync, and the unlocked size check is not protection against every concurrent append. Also, `record()` ignores the preceding `grep` status because the final `printf` determines the group’s status, so preservation of other record lines is not guaranteed on a read error.

**A-23 — narrowed: rows 25–27 are good partial-file safeguards, not the complete artifact guarantee claimed.**  
Evidence: `backuptool:649-661,1283-1347` (excerpts).

Both archive writers list/count the partial before publication, but final `mv -f` success is not verified against the intended final file. If `TARGET` is a directory, that move can succeed by placing the partial inside it, and these functions return success without the promised archive at `TARGET`. The credential scan is conditional on `STRIP=1`; caller enforcement, `to_log`, and the complete `listed_files` implementation are **outside the packet**. These archive modes and the enclosing flock were not measured by the supplied fixture, and their complete setup is also **outside the packet**.

**A-24 — narrowed: the restore mark is stronger than an unchecked write, but full mark-and-revert soundness remains unproved.**  
Evidence: `backuptool:1608-1620,1821-1828,1890-1892` (excerpts); `backuptool:649-655` (excerpt).

The mark uses `mv -fT` and verifies its first line, last line, and line count before proceeding; that is a useful guard, though not a comparison of every middle record. A kill before mark publication can leave a snapshot/temporary with live settings unchanged; a kill after destructive extraction begins requires the recovery protocol, not merely this mark writer. The extraction, revert, mark-removal sequence, and boot recovery reader are **outside the packet**, including any durability barrier before extraction. Normal backup eventually calls `sync`, but that does not prove interrupted restore durability; the upstream-era archive move, in contrast, visibly checks both source disappearance and destination existence.

**A-25 — confirmed: rows 30–31 identify real weaknesses, with one wording correction.**  
Evidence: `backuptool:1880-1892` (excerpt); `cloud_setup:69-112` (excerpt).

Rotation ignores the move’s result, whereas `conf_set()` checks its temporary write and verifies each **requested** line after publication. It does not verify every inherited line, take a lock, or prevent another writer’s update from being lost between reading and rename. Its non-file target check is stronger than the archive writers’ target handling, but it has no fsync-based crash guarantee. Whether an extra root archive is subsequently uploaded is **outside the packet**; leaving it there is nevertheless demonstrated.

## 6. Findings F-01 to F-19

**A-26 — confirmed: F-01; Low severity is appropriate.**  
Evidence: `cloud_oauth:2062-2066,2196-2206,2322-2344` (excerpts); supplied PIN fixture.

Counting only four **ASCII** digits and rejecting icon routes before authentication addresses the demonstrated defect; validation should precede `compare_digest` on both GET and POST paths. The `Already written:` statement is correct specifically for the failed-attempt counter: it is in memory and needs no state migration. Ordinary session files are a separate retained-secret issue, not persisted F-01 lockout state.

**A-27 — confirmed: F-02; I would raise its state-preservation severity to Medium.**  
Evidence: `cloud_content_restore:235-279,750-752,1046-1050` (excerpts); supplied real-rclone fixture.

The prerequisite is a locally supplied configuration value, not a demonstrated remote exploit, but the consequence is irreversible local save loss. The proposed allowlist is sound only with validated, bounded option values and consistent enforcement at all affected calls; removing one spelling of `--delete-excluded` is insufficient. `Already written:` must distinguish devices that never applied from those that already lost saves: the fix prevents recurrence but cannot repair that loss. Existing dangerous configuration values still need a defined refusal or normalization policy rather than being treated as no preserved-state concern.

**A-28 — narrowed: F-03; Medium priority is warranted for confinement, while token exfiltration remains unproved here.**  
Evidence: `cloud_content_backup:583-585` (excerpt); `cloud_content_restore:1482-1487` (excerpt); supplied traversal fixture.

The proposed name-validation loop closes the demonstrated `../` entry point and should run before using names to construct transfer paths. It does not by itself constrain rclone options, alternate configuration, or possible filesystem aliases. `Already written:` should say that any escaped upload already completed remains in the cloud and may require inspection and credential rotation, not automatic deletion or an inferred migration. Exact uploaded credentials and destination paths require the backup code **outside the packet**.

**A-29 — narrowed: F-04 refutes one tested escape, not all archive-type hazards.**  
Evidence: `backuptool:551-558,1492-1500,1324` (excerpts); supplied archive fixture.

The fixture proves that the donor extractor rejects the particular absolute-link-plus-child archive without an outside write. It does not establish equivalent behavior for standalone links, hardlinks, existing symlink ancestors, or other member types, which the name-only check does not inspect. The full restore/revert is **outside the packet**, so “the device reverts safely” remains a planned proof, not a result of this fixture.

**A-30 — narrowed: F-05’s exposures are real, but its timing and deployment justification overreach.**  
Evidence: `cloud_connections.py:131,161-180`; `cloud_remote:85-88,325-335`; `cloud_oauth:179-193,2594-2598` (excerpts).

The argv and readable-PIN findings stand with the lifetime corrections in A-1. One player using one console does not establish that every present or future process has identical privileges; that stronger deployment claim is **outside the packet**. Moving values off argv can reduce accidental disclosure, but environment variables are not secrecy from the same privileged account.

**A-31 — narrowed: F-06 correctly identifies leftovers, but “never reaches the cloud” is too strong.**  
Evidence: `cloud_connections.py:74-88,157-160,198,238-243`; `backuptool:1030-1046` (excerpt); `cloud_content_backup:583-585` (excerpt).

Depending on the interruption point, staging can contain the old complete configuration, newly obtained credentials, or both—not necessarily a new token on every kill. A sweep under the shared lock is reasonable hardening, but the claimed tree-wide absence of cleanup is **outside the packet**. Settings-archive exclusion does not prove that a separate, path-unconfined content upload cannot carry the same directory.

**A-32 — narrowed: F-07 should not be disposed of solely as UI wording.**  
Evidence: `cloud_setup:224,495,537-543,926-937` (excerpts); `cloud_remote:329-331`.

The password display, override logging, and malformed-pair echo are direct observations. The first reader is wrong to promise that the raw probe diagnostic contains no secret; the code provides no such mask. Controlled diagnostic categories would address both confidentiality and player-language concerns.

**A-33 — narrowed: F-08’s age and temporary-file observations stand; its regex claim cannot be checked here.**  
Evidence: `cloud_content_restore:837-841,886-898,970-980,1418` (excerpts).

The header timestamp is not used in the shown acceptance checks, and count/verb equality does not establish freshness of individual files. The predictable fallback files are genuinely fail-open, with unchecked writes following allocation failure. `exists_remote` at 441 is **outside the packet**; the visible BIOS caller does not itself demonstrate a dot-bearing name exploiting the alleged regex behavior.

**A-34 — narrowed: F-09 combines a demonstrated exception with an unproved HTML exploit chain.**  
Evidence: `cloud_oauth:2205-2206,2406-2409,2482-2490` (excerpts); supplied PIN fixture.

The non-ASCII `TypeError`, dropped request, and unspent attempt are confirmed by the supplied observation. The raw-render reachability needs the missing code identified in A-14, and the visible POST route does not enforce “no browser stack.” This warrants explicit input validation and an escaping review, not an assertion that attacker-chosen script execution has already been demonstrated.

**A-35 — narrowed: F-10 is real, but the selection-write consequence is understated.**  
Evidence: `cloud_content_restore:1405-1408` (excerpt); `backuptool:1885`; `cloud_setup:69-112` (excerpts).

Failure can leave a newly created empty or partial selection temporary which the unconditional next command successfully installs; it need not leave the old selection intact. Calling that merely Info understates a persistent state-loss and false-success bug. The unchecked rotation and unlocked configuration update also stand, while their downstream uploader behavior is **outside the packet**.

**A-36 — narrowed: F-11 is a valid privacy design note, not universal MAC recovery.**  
Evidence: `cloud_device_id:19-36,133-145` (excerpts).

The common MAC-based derivation is enumerable and linkable, especially with a known vendor prefix. The truncated output can have multiple preimages, and the machine-ID fallback is not the same attack. Changing the identity recipe would require deliberate handling of existing cloud names; the finding does not justify silently generating a new identity.

**A-37 — narrowed: F-12’s visible policy is weaker than an ordinary browser sandbox claim.**  
Evidence: `cloud-signin-window.c:532-534,851-858` (excerpts); `cloud_oauth:917,990-1000` (excerpts); `package.mk:10`.

The visible host restriction applies to user-gesture navigation, and the suffix calculation is only a last-two-label approximation. Any presence of `CLOUD_SIGNIN_DEBUG`, including a value such as `0`, enables the shown keystroke logging. The ephemeral-context and popup-policy implementations are **outside the packet**, so those protections cannot be independently confirmed here.

**A-38 — narrowed: F-13’s PATH observation stands; the tool verdicts remain host evidence.**  
Evidence: `cloud_folder_validate:89-99` (excerpt); `cloud_connections.py:19`; supplied host-tool report.

The validator visibly resolves `rclone` through PATH, unlike the connections module’s absolute executable. The exact test implementations, stale-version assertion, and missing-argv-file assertion are **outside the packet**. Their reported outcomes should remain attributed to the first reader’s host runs, not treated as independent guest qualification.

**A-39 — confirmed: F-14 identifies two missing translation-table entries.**  
Evidence: `cloud_setup:797` and `backuptool:1495` (excerpts); supplied `CloudText.cpp:414-466` table.

Neither emitted sentence occurs in the supplied why table. The localization fallback implementation and actual screen routing are **outside the packet**, so a particular French-screen presentation has not been independently demonstrated. The interface/script contract still needs reconciliation.

**A-40 — narrowed: F-15 describes a coherent normal path, not one indivisible transaction.**  
Evidence: `cloud_connections.py:54-62,143-150,193-198,218-258`.

The manual-mode asymmetry and deliberate first-remote fallback are both visible. However, active selection has its own `select()` writer, and multi-file publication plus rollback is not atomic across interruption. The option-forwarding issue in A-45 also needs resolution before claiming that every effective credential write passes through the verified installer.

**A-41 — narrowed: F-16’s preservation disposition is reasonable; the dead-code census is not independently reproducible here.**  
Evidence: `backuptool:480-518` (excerpt); `cloud_setup:926-943` (excerpt).

The legacy archive reader and console instructions remain substantive code, so there is no packet-supported reason to remove them. Their complete dispatch/reachability and the whole-file reference census are **outside the packet**. “Removals none” is safer than converting an unverified census into proof that all retained branches are exercised.

**A-42 — narrowed: F-17’s tables help navigation but are not a complete security map.**  
Evidence: `cloud_connections.py:72-88,161-168`; `cloud_oauth:2454-2457` (excerpt); `cloud_content_restore:1046-1050` (excerpt).

The tables locate important boundaries, but omit or overstate paths identified above: argument-controlled behavior, raw metadata logging, interruption states, and several unproved negative sink claims. The rule document needed to verify “zero mentions of the writer” is **outside the packet**. Generated anchors validate that selected text exists, not that the security inventory is exhaustive.

**A-43 — narrowed: F-18 confuses some per-call bounds with whole-operation bounds.**  
Evidence: `cloud_connections.py:131,168-180`; `cloud_content_transfer:65-95,127-157`; `cloud_folder_validate:22-24,43-68` (excerpt); `cloud_log_scrub:5-6` (excerpt).

A connection save can perform multiple separately bounded subprocesses; it is not generally a 40-second operation. Content inactivity is bounded as described, but user-supplied timeout values can change that ceiling, and several OAuth limit implementations remain **outside the packet**. The blanket menus-only/time-to-play claim is also unsupported: the scrubber explicitly describes boot execution, while actual scheduling and the cited QA log are **outside the packet**.

**A-44 — narrowed: F-19’s build dependency and renderer default are confirmed, not package currency as a whole.**  
Evidence: `package.mk:9,16-21`; `cloud-signin-window.c:941-949` (excerpt).

The recipe links WebKit/GTK and libatomic, and the renderer environment default deliberately respects an existing override. Actual WebKit package version and the rclone package recipe are **outside the packet**. The declared host/donor substitutions remain important qualifications rather than evidence that all installed combinations were tested.

## 7. What the first reader missed

**A-45 — new: option-shaped connection settings undermine the “one verified writer” boundary.**  
Evidence: `cloud_remote:325-335`; `cloud_connections.py:161-168,180-198`.

The CLI checks only that each setting contains `=`, then passes its key unchanged into rclone’s argument list. An option-shaped pair such as `--config=/some/path` is therefore forwarded as a flag, not safely confined to backend configuration data. That creates a route to redirect configuration behavior before the staged verification/commit sequence; the exact rclone 1.75.2 override result is **outside the packet** and needs a focused repeat. Reject option-shaped keys and validate settings against the provider schema before claiming all effective writes reach `atomic()`.

**A-46 — new: scan temporary creation fails open into root-relative writes.**  
Evidence: `cloud_content_restore:1271-1278` (excerpt).

`mktemp -d` is unchecked, so failure can leave `TMP` empty and make the following redirections target `/cloud.raw` and `/cloud`. The immutable root may reject those writes, but that is not a controlled allocation refusal and does not repair the missing boundary. Require a successfully created nonempty directory before any scan command or redirection; the cleanup trap alone provides no such protection.

**A-47 — new: the setup probe can report success from empty diagnostics after command failure.**  
Evidence: `cloud_setup:495-498` (excerpt).

The rclone status is lost behind `head`, and the decision is made from diagnostic text rather than a separately captured status. A failed or killed rclone producing no captured stderr matches the empty-string success branch, just as a successful probe does. Capture status independently and distinguish supported absence responses from unreadability; the validator’s stronger discipline does not cover this probe.

**A-48 — new: scan output writes are unchecked before completion publication.**  
Evidence: `cloud_scan:315,332-344,350-355` (excerpt).

The start stamp, archive-list pipeline, and settings-record group do not have their write failures checked. A failed redirection or partial write does not itself prevent the subsequent content-location read and completion attempt. `result_id` is **outside the packet**, so I cannot assert that every such failure produces an accepted completion, but hashing or successfully reading a partial result would not prove its intended contents. These writers belong beside F-10, not in an unqualified success story.

**A-49 — new: the archive’s staged-count guard loses the producer’s status.**  
Evidence: `backuptool:1177-1179,1283-1287,1324-1335` (excerpts).

The collecting pipeline explicitly enables pipefail in a subshell, but the later `find … | wc -l` count does not preserve `find`’s failure under the reported default shell discipline. A matching count therefore does not by itself establish that enumeration completed successfully. The later member-list `find` is checked, which limits the consequence and prevents claiming that this alone proves a bad archive was published. Nevertheless, the first reader’s “counted means read whole” model needs this producer-status gap recorded.

**A-50 — new: raw metadata provides additional log-secret and log-forgery paths.**  
Evidence: `cloud_remote:263-264`; `cloud_connections.py:141-142`; `cloud_oauth:2446-2457` (excerpt).

`cmd_create()` logs the supplied connection name **before** `save()` rejects newline/tab-containing names, so a rejected name can already have placed cleartext or forged credential-shaped records in the shared log. This is independent of the sanitized rclone-failure helper and contradicts a blanket “no writer can recreate those shapes” claim. The phone log is also not strictly “counts only”: it appends raw `named`; whether `RemoteKeyboard.press()` always prevents arbitrary values from reaching that log is **outside the packet**. Validate metadata before logging and treat unexpected input as data to reject, not text to echo.