## 1. My own findings

- **G-01 — Medium — `ViewController.cpp:500,520,615-617,654-656`; `FileData.cpp:767-772,803-809,939` — Save-state lifetime protection starts too late:** a confirmation or animation retains `options.saveStateInfo` before `rememberSaveState` runs; a repository refresh during that wait frees the object that `rememberSaveState` then reads.
- **G-02 — Medium — `FileData.cpp:910-923,993-1056,1295-1306` — A completed capture loses its exit sync before the replacement launch is certain:** the spinner advances the generation and suppresses the old sync, but the retry can meet another question and end with KEEP WAITING, leaving no replacement game exit to perform that sync.
- **G-03 — Medium — `SystemData.cpp:382-387,434,634-635` — Automatic rescanning misses changes inside existing subfolders:** changing their contents does not change the system root’s directory timestamp, so the early return leaves added games absent and removed games listed.
- **G-04 — Medium — `SaveStateBookkeeper.cpp:175-197` — Deletion proceeds without confirmed retirement bookkeeping:** if `cloud_capture` is absent or fails before recording the deletion, the fallback still unlinks the save, losing the durable evidence that this absence was the player’s choice.
- **G-05 — Medium — `SaveState.cpp:81-83,114-133,166-169` — The fallback NEW GAME path strands an existing auto save even after a clean session:** with `racommands` and slot `-2`, setup parks the auto save in `.bak`, but `onGameEnded` returns before restoring it.
- **G-06 — Low — `FileData.cpp:623-648` — Placeholder replacement also rewrites previously inserted data:** in a custom template, a literal `%CONTROLLERSCONFIG%` inside the substituted game name becomes controller configuration instead of remaining part of the name.
- **G-07 — Low — `FileData.cpp:609-615` — Forced-option detection mistakes text for options:** a custom executable or argument containing `-core` or `-emulator` suppresses the corresponding appended option even when no such option exists.
- **G-08 — Low — `LaunchCommand.h:51-54`; `FileData.cpp:719-720` — An explicitly empty option is treated as absent:** with a nonempty fallback, a finished `--core=` or `--emulator=` records the fallback rather than preserving the command’s explicit empty value.
- **G-09 — Low — `FileData.cpp:938,1031-1039` — PLAY NOW permission is global, not attached to the approved launch:** another `launchGame` call arriving before the queued retry consumes that permission and bypasses its own send question.
- **G-10 — Low — `ProxyCards.cpp:253-262,267-284` — The screen-free check expires before card creation:** if a send or sync starts between the worker’s check and the posted callback, that callback still requests a top-up card without checking again.
- **G-11 — Low — `ProxyCards.cpp:253-264` — The three-second card wait is not a bound:** if the interface callback claims `wanted` and then stalls before `set_value`, the worker enters an unlimited `got.get()`.
- **G-12 — Low — `FileData.cpp:1086`; `Scripting.cpp:104-105` — A hook argument beginning with a quote loses its last character even without a closing quote:** the condition tests `startsWith` twice and then removes both ends.
- **G-13 — Low — `FileData.cpp:1088,1103,1115-1203` — Recorded playtime includes return processing:** when save-state refresh, hooks and interface reinitialization push the total past ten seconds, a shorter emulator session is recorded as at least ten seconds of play.

## 2. Refuting the first reader

### SS-1 — **Re-grade High**

The finding survives, but Medium understates it. These are not merely filenames that expand incorrectly. Shell command substitution also runs inside double quotes, so a state filename containing `$(...)` or backticks executes commands with EmulationStation’s privileges. The shipped state-launch path inserts the filename without escaping it (`SaveState.cpp:77,97,111`). Guest G-6, `exec.log:20`, confirms that shell expansion reaches this path.

**False if:** the filename is safely quoted before shell execution, or passed through an argument-vector interface without a shell. The excerpt does neither, and G-6 contradicts effective protection at this boundary.

This is a **High command-execution defect**, not a claim of root privileges or network reachability; neither is established by the packet (`FileData.cpp:1100-1103`).

### SD-2 — **Agree: Medium**

The finding survives. The predicates inspect the whole path, while recursion supports subfolders generally (`SystemData.cpp:627-635`). Guest G-4 directly distinguishes the missing `SportsProbe.gb` from the listed `PuzzleProbe.gb`.

**False if:** the exclusion is restricted to the intended system or directory component. The source shows neither restriction, and G-4 demonstrates the collateral exclusion.

Narrow the examples: the literal `rfind("windows")` is case-sensitive. The packet does not establish that the capital-W example `Windows 95 era` is excluded (`SystemData.cpp:631`; Guest G-4 tests `Sports`, not Windows).

### FD-14 — **Narrow: Low for leftover discs; a Medium containment seam remains live**

G-7 correctly refutes deletion of the two outside sentinels **in that successful-unlink fixture**. It does not establish that DELETE GAME cannot delete outside files.

The game-file removal is unchecked. If it returns without removing a readable playlist, the following call can read that playlist and remove its absolute or parent-relative targets (`FileData.cpp:1434-1451,1503-1506`). Independently, the metadata loop removes existing non-directory `MD_PATH` targets without a containment check at this sink (`FileData.cpp:1487-1494`). The first reader already identified that sibling in its shape sweep; the correction must retain it.

The proof also does not cover `.ccd`: that branch constructs sibling names without opening the descriptor (`FileData.cpp:1424-1430`).

**False if:** failed removal cannot return to the caller, and all removal targets are constrained by a verified ownership/containment rule. Neither guarantee is supplied. G-7 tests successful removal, not these paths.

Thus “the tested playlist left its discs” survives. “Nothing outside the folder can be removed until the order is fixed” does not.

### VC-1 — **Agree with the Low correction; narrow the measurement**

The default-cost correction survives: `GameTransitionStyle` is `instant`, and ROCKNIX defaults `HideWindow` to true (`Settings.cpp:250,372-376`). Guest G-8 shows the question initially appearing over black, not a 750 ms default transition.

The remaining ordering defect also survives: `doLaunchGame` runs after the transition, and only then reaches the gates (`ViewController.cpp:615-617,635-637,654-656`; `FileData.cpp:990-1056`).

**False if:** the gates run before the transition, or the list is restored before the question appears. The source and G-8 show the opposite.

Keep the timing claim confined to **POST /launch with the synthetic top-up marker**. G-8 does not establish physical-button latency or how long the background remains black. Also, return animations are not necessarily as long as outbound animations: the return durations shown are 800 ms for fade, 600 ms for slide and 10 ms for instant (`ViewController.cpp:626,647,666`).

### FD-8 — **Re-grade Medium**

The lifetime defect survives. `launchNow` retains and later dereferences a raw game pointer, with no identity lookup or ownership protection (`FileData.cpp:774-792`). The packet identifies system destruction through the reload callback wired at `main.cpp:818` and `ViewController::reloadAllGames`.

Loopback-only access limits the trigger’s exposure; it does not turn use-after-free into a cosmetic defect.

**False if:** reload invalidates every queued launch before deleting its game, or game destruction is deferred until those callbacks finish. The packet supplies no such guarantee, and `launchNow` itself supplies none.

The runtime crash remains unproved. In particular, “reload the dialog away, then answer it” is not a valid reproduction of an already queued retry. The retry must be queued before the relevant deletion (`FileData.cpp:776,848`; the packet’s reload description at `ViewController.cpp:1437-1447`).

### SD-3 — **Re-grade Medium**

The finding survives. One malformed overlay suppresses unrelated later overlays, including the remaining root, while leaving earlier changes applied (`SystemData.cpp:1026-1050,1075-1091`). Guest G-5 reproduces the loss of the later valid rename.

**False if:** processing continues with subsequent files, or another independent pass applies them. The whole-function `return`s and G-5 show that neither happens in the tested path.

The absence of shipped overlays limits exposure. It does not make persistent loss of valid add-on configuration a minor formatting problem (`git ls-files | grep -E 'es_systems_[^/]*\.cfg$'` reports only the QA fixture; Guest G-5).

### SD-4 / FD-15 — **Re-grade Medium**

The finding survives as a persistent list-opening crash. The stored value is accepted unchanged, and equality with the number of sort types passes the bad bound (`SystemData.cpp:1937-1940`; `FileData.cpp:1658-1662`).

**False if:** the stored value is normalized before use, or the exception is handled without terminating the interface. Guest G-9 contradicts both: 28 crashes and restarts the service; 27 opens the list and keeps the process alive.

The specific historical-upgrade story remains unproved. G-9 establishes a persisted bad value, not which released build previously wrote it.

### MN-3 — **Re-grade Medium, limited to stale command replay**

The frozen-command defect survives. Boot checks the separately stored ROM path, then executes the saved command after replacing only controller configuration (`main.cpp:529-540`). A stale command therefore retains stale core and state arguments; the normal command builder is not consulted on this path.

**False if:** boot rebuilds the command, or every relevant configuration change refreshes the saved command. Boot does not rebuild it, and the packet supplies no complete update mechanism beyond the setter at `GuiMenu.cpp:11325`.

Do not turn every omitted ordinary-launch action into another bug. Boot capture exists (`main.cpp:551-570`), and startup sync is scheduled later (`main.cpp:1117-1118`). The absence of a separate boot-game exit sync is not evidence of lost saves. Likewise, the claimed serialization of selected netplay options needs the setter’s actual option construction, which is not supplied.

### SB-2 — **Narrow: Low unbounded-retry seam; the exact spin claim is unproved**

The retry gap survives: after `transferGone` succeeds, failed lock acquisition retries every 200 ms, with no failure deadline other than shutdown (`SaveStateBookkeeper.cpp:159-173`).

But “an open failure always produces a session-long five-hertz spin with a hidden tile” exceeds the excerpt. `transferGone`, `isFlockHeld` and the pending-job completion path are not supplied. The first reader’s own description says the lock probe fails closed.

**False if:** a permanent acquisition error causes `transferGone` to return false and completes the pending job instead of retrying. The packet does not show whether it does. Therefore the unbounded retry survives; the precise EACCES/descriptor-exhaustion behaviour does not stand as proved.

A confirmed stall would also block later work because the queue permits only one running job (`SaveStateJobQueue.cpp:37-38`).

### FD-18 — **Agree: Low, but it is a real defect**

The data race survives. The interface writes the plain pointer while worker code reads it (`FileData.cpp:83,1094,1111`; `ProxyCards.cpp:269,410-417`). Comparing only against null does not provide synchronization.

**False if:** the accesses use an atomic, a common lock, or a demonstrated ordering that prevents concurrent access. None is shown. A ThreadSanitizer reproduction is not required to establish the race from these accesses.

Low is defensible because the supplied worker reads test presence rather than dereferencing the game, and the packet supplies no resulting crash or save corruption. It does not support High.

### LC-1 — **Narrow: Low, but not unreachable**

Restricted identifier characters do not establish unreachability. A benign custom template can quote an ordinary name: `--core='snes9x'`. `launchToken` preserves those quotes, although the shell removes them from the launched argument (`LaunchCommand.h:39-41`; `FileData.cpp:719-720`). Subsequent `shellQuote` preserves that mistaken value as literal capture data; it does not decode it (`FileData.cpp:1148-1151`).

**False if:** the token reader decodes shell words, or every supported template is constrained to unquoted values. The reader does not decode them. The supplied stock template is unquoted, but no equivalent constraint on custom templates is shown (`config/functions:128`; `LaunchCommand.h:49-54`).

### FD-2 / FD-3 and FD-9 / FD-19 — **Re-grade Medium for their stated optional paths**

These survive as conditional command-execution defects, not merely filenames that split. The unsafe builders preserve shell syntax in data (`FileData.cpp:528-534,624-630`; `Scripting.cpp:103-112`). Installing a benign template or hook is the enabling condition; the template or hook need not itself be malicious.

**False if:** those optional consumers are absent, or data is safely encoded at the shell boundary. Guest G-3 and the reported hook search establish absent stock consumers, so they limit default exposure. They do not refute the conditional defects.

The “custom-only” reachability claim also needs the replacement issue in **G-06** checked against the ROM escaper: counting placeholders in the original templates does not establish which placeholders exist after inserting data (`FileData.cpp:623-630`; Guest G-3).

**High verdict:** SS-1 should be High. The packet does not establish another High with the same shipped-path evidence.

## 3. What I could not judge

- **The complete command-input boundary.** The implementations of `getEscapedPath`, controller serialization and identifier validation are missing. I cannot certify universal `%ROM%` safety, confirm FD-7, or establish that later-placeholder text cannot enter through an escaped ROM path (`FileData.cpp:618,622-630,647-648`). Guest G-3 counts template tokens; it does not test inserted values.

- **The launcher’s actual interpretation and final emulator behaviour.** G-6 proves an altered state argument in `exec.log:20`, not which state the emulator finally loaded. The duplicated parsing, relay/session handling, spectator behaviour and explicit-empty options require the launcher side (`LaunchCommand.h:22-23,51-54`; `FileData.cpp:659-697`). The packet supplies no netplay-host proof.

- **Callback cancellation and notification ownership.** Actual FD-8 and G-01 interleavings need the queue, `GuiLoading`, repository-refresh and reload lifetimes checked together. PC-1 needs notification destruction and `close()` semantics; G-10 needs Window’s card arbitration. Raw pointers and direct calls establish the seams, not the missing teardown contracts (`FileData.cpp:776-792,898-924`; `ProxyCards.cpp:253-286`; `main.cpp:1322,1358`).

- **Filesystem-error and cloud-helper contracts.** Failed-unlink behaviour, `hasContentFiles()` after removal, scan failure handling and `FolderMerge` ownership are not fully supplied (`FileData.cpp:1398,1503-1506`; `SystemData.cpp:400,434,456-486`). Neither are the helper bounds needed to certify SB-3 or top-up completion, or the reconciliation outcome after an unrecorded deletion (`SaveStateBookkeeper.cpp:182-197`; `ProxyCards.cpp:271-288`). G-04 proves deletion without confirmed bookkeeping, not a particular later cloud resurrection.

- **Several proposed end-to-end claims remain untested.** The packet contains no change-core/reboot proof for MN-3, no historical sort-table evidence for the claimed upgrade trigger, and no caller-level failure proof for SS-4 (`main.cpp:533-540`; `SystemData.cpp:86`; `SaveState.cpp:213-239`). Those conclusions need narrower wording than the demonstrated frozen replay, injected sort value and unchecked operation results.

- **Performance and memory beyond the measured workload.** `time-to-play --repeat 3` explicitly reports no cloud to reach. G-10 establishes no measurable difference at 500 states and approximately 61 ms resolution—not zero scan cost or acceptable cost at every library size. `es-launch-memory --cycles 5` establishes no net growth across those cycles—not “nothing left behind,” absence of leaks, or safety across system reloads. The ASan/UBSan unit-test outputs are not ThreadSanitizer evidence.

- **Full coverage and merge safety.** `grep -c '^| \`es-app/src/' 02-forward-audit.md = 20` establishes table-row count, not independently verified whole-file coverage. The reported 370-row reachability result is not accompanied by the full table here. Likewise, `git show <commit> | git apply --check` establishes patch applicability, not behavioural compatibility or correct handling of changed launch signatures. Those remain evidence gaps for the orchestrator, not passes supplied by this second reading.