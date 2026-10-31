# Mini Retro: T35 stage E, the streams (#682)

**Completed:** 21:36 UTC 2026-10-31 (the posting command's `date -u`), posted whole on #682 (comment 6549449227)

**Scope:** S0 to S8 and stage F, from `t35-streams.md` at `0f9f8f69fe` (twenty-one rulings, D-UI-134 to D-UI-137, Backlogs #1344 to #1347).
- **ES:** `16dbac5211` to `d0e5b3432`, eight commits: S1 `56aa398b8`, S2 `453dffd0a`, S3 `5d7707790`, S4 `1d5d3e0db`, S5 `c0ab63bf2`, S6 `f5a698915`, S7 `425fbd4af`, S8 `d0e5b3432`. They touch eleven files of the 96 and the French catalog's one entry.
- **Distribution:** S0 `92ea708fed` to stage F `53113b8bfa`: the audit folder, the day's log, the pointer and the friction log.

**Delta:**
- **The unit build:** `TOTAL: 260 test cases in 7 binaries` at the pin (S0) became `TOTAL: 283 test cases in 8 binaries` at S8's tip. Every binary's test-case summary is at 0 failed, with `may_fail: 1` (3.5, PL-18 recorded under rulings 9 and 20).
- **`window-input-tests`:** 10 cases with 7 failed at stage C, now 31 cases with 0 failed.
- **`floor-tests`:** 11 of 11 throughout.
- **`log-tests`:** new, 2 cases.
- **The sanitizer programs:** three became six (`lsan-f4`, `tsan-log-close` and `tsan-log-flush` added), all six at rc 0.
- **Bugs:** nine filed in stage E (#1348 to #1356).
- **Phase 7:** 17 items Resolved and 17 Deferred.

### What worked well
- **The extractor's refusal.** A case runs only on lines whose first and last line still hold the code it was written for. It refused twice on real moves (S2's dialog specs, 22 lines down; S8's `kb_x` given one line too many) and once on a constructed wrong spec. Each refusal named the spec, so no case ran on lines it was not written for.
- **Whole functions lifted into doubles.** The pin's own code ran in the cases: `setHelpPrompts`, `writeDeviceConfig`, the `GuiMsgBox` accelerator over each dialog's real labels, and `Log.cpp`'s file-local `AsyncLogger`. The defects showed as behaviour, not as text:
  - two pads configured in one session saved one (`1 == 2`);
  - a polling reader saw 3,838 short files in 13,321 reads;
  - the logger lost its last line in 5 of 5 rounds.
- **The case first, against the pin.** Two first shapes passed at the pin (PL-27's 200,000 short lines; `tsan-log-close` with the worker idle), and both were reshaped before any fix. Ruling 10's condition was decided by a tool line, not by reading: `tsan-log-flush` reported the race on `mFile`, so PL-28 was fixed and filed (#1356).
- **Measuring what a fix leaves** (S4, `stage-e/s4-unregister-wait.txt`):
  - another watcher's unregister went from 1,494 ms to 0 ms;
  - a watcher's own unregister mid-probe now waits 1,493 ms, bounded by its own 1,500 ms probe.
- **Reusing what the tree has.** es-core's own `Utils::String::shellQuote` carried S5, and T21's `AtomicFile::writeText` carried S6. Neither was changed.

### What was harder than expected
- **The build script compiled stale extracts** after a refusal, while printing *not built* (S2). It now clears them first, and a constructed wrong spec showed the guard firing (`stage-e/s2-guard-proof.txt`; friction line, written late).
- **doctest prints a case header for a `MESSAGE`**, so the untruncated failing list named passing cases (S4). The list now reads `ERROR` lines and keeps `may_fail` cases apart (friction line, written late).
- **One ThreadSanitizer program with two races** crashed on the first, 3.17's corruption, before it could report the second (S2). It now runs the races as phases.
- **A test double copied an arity.** 3.13's `exists` took one argument, and S6's `exists(path, false)` left `floor-tests` unbuilt. The script said so loudly (`not built`, 6 binaries); fixed under D-WORKFLOW-211.
- **The brief's literal fix for PL-26** (the refresh event pushed from the drain) would have left the drain unreached while the main loop waits in `SDL_WaitEventTimeout`. The event stays with the post, `mSleeping` became atomic for the post's read, and the departure was said on #682.
- **Other interruptions:**
  - The harness refused one checks command for its quoting; script files since.
  - A usage limit cut the turn mid-S3, and work resumed from the pointer and `00`.

### Discoveries that affect future streams and slices
- **`git blame` corrected the record.** The threaded logger is upstream's (`e478a1eda4`); only its per-batch flush is the fork's (#178). So PL-27 and PL-28 get #585 lines. Every other fixed line is upstream's except three: the toast re-queue (`c1c0d6ddcf`), the text popup's CLEAR (`c8dc72cf9e`) and that flush.
- **A reset during a probe must survive the probe.** At the pin the lock across the probe gave that for free. Probing outside the lock needed `resetPending`, and a guard case holds it.
- **A lead outside the punch list:** `PowerSaver::pushRefreshEvent` writes the static `mHasPushedEvent` from posting workers, while the interface thread resets it, unsynchronized. Read, not run, not fixed; put to the coordinator on #682 at S2.
- **es-app's three-button dialogs without OK or NO** are three, and none lands on a destructive choice (`CloudOffer.cpp:51` NOT NOW, `ScraperSearchComponent.cpp:468` CANCEL, `GuiWifi.cpp:251` CANCEL). This is #1344's starting count.

### Adjustments to remaining work (proposals for the coordinator)
- **The integration window owes each stream's guest half** (`fix-walk-pending-image`), with the flow references the changed screens update:
  - S1: the drive dialog after `z`.
  - S2: two toasts after a card, and the French list bar.
  - S3: the screensaver held over the transfer page, with `stage-e/s3-pages.patch` applied.
  - S5: the hook's argv file.
  - S6: the removed `es_input.cfg` reconfigured.
  - S8: CLEAR on the keyboard, the key gap measured from that frame, and the configuring subtitle, in English and French at both sizes.
- **`stage-e/s3-pages.patch`** goes to T18 (#665: `GuiCloudTransfer.h`, `GuiOfflineScan.h`) and T31 (#678: `GuiScraperRun.h`). It applies clean at their tips and needs S3's `GuiComponent.h` first.
- **The sweeps and patches that are the coordinator's:**
  - T34's `MenuComponent.cpp:9-10` sentence about the keyboard's second copy, now false (ruling 3).
  - `es-native-ui.md:30` (ruling 18).
  - `es-code-traps.md`'s sentence on the input file and an uncached `exists`.
  - T34's two patches, dry-run in the hand-back.
- **The PowerSaver lead** is the coordinator's to file or dispose.

### Time to play

Nothing this slice changed lengthens the launch path. Stream by stream:
- **S2:** the toast queue's front pop is an erase over a few entries per toast, and the unregister takes one lock per page close. The wake is applied at the next update's drain, and the refresh event still ends the main loop's wait at once.
- **S4:** the interface thread no longer waits for another watcher's probe; 3.1's 1,492 ms is gone. `WatchersManager::pause`, on the launch path (L-19), is byte-identical to the pin's.
- **S5:** `fireEvent`'s quoting is one string pass per word, and the six directory scans are unchanged.
- **S6:** `writeText` adds two fsyncs per save on the interface thread, at a configuration's OK and on an SDL-mapped device's hot-plug write. Both are off the launch path.
- **S1, S3, S7, S8:** off the path. S3 adds one virtual call per frame while idle past the setting.

The two numbers themselves are **`CANNOT` here**. The guest window closed at stage C, and none of these fixes is in an image yet. The card's linger, the game-to-game dialog's answer, the six directory scans and `pause` are for `tools/time-to-play` on the integration image, which also prices S6's fsyncs (G-10 is `CANNOT` for a hot-plug: no pad on the guest).
- **The window's one reading:** the startup card stayed at STARTING... for about 100 s on the unreachable cloud (`02` § The guest cycle; the cloud lane's, #1345).
- **The last figure on record:** `docs/vm-qa-log.md:171` (2026-10-06): 0.603 s to first pixels, 1.33 s exit with backup, 1.017 s rapid relaunch.

### What T36 (#683) and T37 (#684) inherit
Stage E's additions to `02` § What T36 and T37 inherit:
- **The extractor's `SPECS` at `d0e5b3432`** (`tools/t35-extract.py`, 47 extracts), and the build script's three guards: extracts cleared before extracting, failed cases read from `ERROR` lines, `may_fail` cases listed apart.
- **For T36's cache:** the uncached reads S6 makes (`InputManager.cpp`'s three, `GuiDetectDevice.cpp:127`). A writer outside `Utils::FileSystem` (pugixml, `AtomicFile`) is invisible to the cache, so a read after one is uncached.
- **`InputManager` is `AtomicFile::writeText`'s first caller in the 96** (T21's API unchanged; T36's neighbour).
- **`GuiComponent::allowScreenSaver()`** (S3), and the page patch for its overrides.
- **For T37 (the recipe that moves the pin):** the eight ES commits, the French catalog's `GAMEPAD` entry, and the hand-back's dry-runs of T34's `s2-window.patch` and `s3-msgbox.patch` over T35's tip.

### Scoped audit findings (Step 2.5)
- **AC conformance: PARTIAL.** Every unit criterion is met at `fixed-at-es` `d0e5b3432`. The guest halves wait on the integration window, as the brief places them.
- **Cornerstone spot-check: PASS.**
  - No change outside the 96, the catalog's one entry and the audit folder.
  - `git diff --name-only b51dd8a805 HEAD -- packages projects tools` prints nothing.
  - 0 non-ASCII bytes on any added source line.
  - The four signatures the doubles rely on are unchanged at every stream.
- **Interaction-defect scan: PASS.** `Window.cpp` took S1, S2 and S3 serially, and `InputManager.cpp` took S6. Each later stream's specs were re-derived from the earlier one's lines (D-WORKFLOW-210), and the doubles that copied a changed shape were completed in their stream (D-WORKFLOW-211).
- **Housekeeping: PASS.** The tree's five binaries pass 239 cases at every run: 185, 24, 10, 2 and 18.
- **Harness self-coverage: PASS.** Both harness gaps were closed in the harness and seen to fire.

### Practice adjustments
- **A ThreadSanitizer program that holds two races runs them as phases**, the one that cannot corrupt first.
- **A case for a lost-at-exit race holds the worker busy at the moment it needs** (one large item). Otherwise it passes at the pin and proves nothing.
- **A list of failing test cases reads the failure lines,** never the framework's section headers.
