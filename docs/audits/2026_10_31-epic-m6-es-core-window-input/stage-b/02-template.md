# Forward audit — M6.P2 T35, EmulationStation's window, input and the rest of es-core (#682)

- **reviewed-at:** `b1f2908a55` (the distribution worktree at stage A); **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`, the 96 paths of `.qa-scratch/t35/paths.txt`, read by `git -C <W> show` and never from a working tree.
- **Stage B, composed by `tools/t35-02.py` from this template**: every generated section is the named script's output at the pin, and its last line is `generated, asserted: ...`. Each script was seen to exit 1 on three constructed drifts before it was trusted (§ The runs).
- Every proof carries a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`. Stage C (the host's cases and builds) and the guest window come after this composition, and their rows say `owed` until they run.

## Coverage

<!-- GEN t35-coverage.py rows=96 added=1 modified=12 upstream=83 inv_fork=13 inv_up=83 lines=22575 -->

## The leads

L-01 to L-29 are the brief's § 2 lead table. L-28 and L-29 are T34's PL-05 and PL-04, carried in version 2; § 6 still says *L-01 to L-27*, an erratum. 3.1 to 3.27 are the floor's cases. Each anchor line is checked for its text at the pin.

<!-- GEN t35-leads.py leads=29 cases=27 confirmed=24 contradicted=1 -->

## The surfaces

<!-- GEN t35-surfaces.py rows=21 containers=5 sites=15 -->

**The queue's order (`:339-340`).** The queue drains **newest first**. The pop is upstream's: the base `bccd715707` pops from the back at its `:322-323`. **D-UI-093's decided row says it plainly** (`decision-register.md:404`: *Nothing is dropped; the order is the order things happened.*), as does the fork's comment (`c1c0d6ddc`, `:334-335`). The fork's own re-queue comment (`:1159-1160`) relies on the opposite. **Disposition: a defect against a decided row, contained in `processNotificationMessages`**, the order cited and not re-argued (`decision-register.md` § Read it when), proposed for the pause as a rule-6 fix (pop the front, and reverse the re-queue loop so a returned toast keeps its place). 3.14's FAIL line at stage C is the evidence. G-03 is `CANNOT`.

**The re-queued toast's duration (`:1164`).** A toast taken off the screen by a new card comes back with `notificationDuration(-1)`, a fresh default, not its remainder. **Disposition: by design, recorded.** A toast half-read and then re-shown whole costs the player seconds and loses no words. The pause may rule otherwise (a register row, brief § 9).

**F-ES-24** (the 2026-09-25 audit `02:199`, Low, never dispositioned): every toast waits while *any* card is up (`:336-337`), including the hasher's minutes-long upstream card that D-UI-079 keeps as upstream has it. **Disposition: stands as recorded, with a bound proposed for the pause.** It is the one surface D-UI-093 and D-UI-078 together did not decide, so it is put to the coordinator as brief § 9's first register row, not decided here.

**Item 13, the card's position:** `:1183` (0.02 H from the top) and `:1192` (centred) are re-applied every frame. They agree with the component's own first position (`AsyncNotificationComponent.cpp:112-113`, T34's) and its width `max(text, 0.9 W)` (`:62-64`). G-02 measures the edges at 640 (x 32 and x 608).

## The input

<!-- GEN t35-input.py writes=9 real_writes=5 reads_counted=2 exists=5 rows=12 -->

## The locks

<!-- GEN t35-locks.py lines=67 files=11 locks=10 weak=2 includes=4 -->

## The lifetimes

<!-- GEN t35-lifetimes.py threads=18 detach=4 delete_this=17 posts=6 raw=8 rows=52 -->

## The scripts

<!-- GEN t35-scripts.py sites=4 shell_direct=0 -->

## The words

<!-- GEN t35-words.py lines=86 files=10 occurrences=97 msgids=61 fr_missing=0 tiered=0 plural_calls=28 plural_fr_missing=0 glyph_lines=27 -->

## The structure

<!-- GEN t35-includes.py headers=51 cpp_named_once=44 unregistered=2 batocera=9 batocera_96=7 cmake_ifs=2 rocknix=3 map_titles=0 -->

## The merge debt

`cada856d86` is the merge base against `rocknix/master` (`f6c542872e`), and `bccd715707` is its parent and the stale `upstream/master` (2026-09-22). Upstream has **0** commits on the 96 since the base (14 on any path; numstat 0), **96 of 96** blobs are identical between the base and master, and **83 of 96** between the pin and master. Batocera's **twelve** commits since `1750dded8c` touch **nine** files, six of them fork-modified (`GunManager.cpp`, `InputManager.cpp`, `Log.cpp`, `Window.cpp`, `Window.h`, `guis/GuiMsgBox.cpp`): the reconciliation list only. T21's `3ae9610b0` hunk in `es-core/CMakeLists.txt` (five added lines, § The structure) is the integration's. **T34's ES tip, read at stage B:** local `568ef099d` and `origin` `a9017ff50` at 06:29:09Z (`git -C <W> rev-parse`/`diff --name-only`): **empty inside the 96** (19 and 18 files on other paths). The first read, at 06:08:37Z, was local `db12b1598a` and `origin` `2cbb62d7bd`, also empty inside the 96; the hand-back reads it a third time. L-25's footnote: `guis/GuiTextEditPopupKeyboard.h` carries a fork commit in the inventory and is byte-identical to the base. `proved: tool-run` (stage A's run 5, `stage-a/runs.out`).

## The runs

<!-- GEN t35-runs.py runs=25 generators=9 -->

## The guest cycle

**Not run at stage B.** The window is asked for on #682 at stage B's end, with the plan and bound in `stage-b/window-plan.md`: 30 minutes plus 5 of grace, a 1,560 s plan, G-01 to G-12, two boots. It lands here once granted: the grant's time, the START and RETURN posts with their first lines, the timer's PID and the censuses, the host file's lines, the image's `BUILD_ID` read at 640x480, every frame read back at EN and FR and labelled by side, the second boot, the disk retired with path, size and sha, and the leftover check.

## The streams

Stage E: **written by the coordinator after stage D**, as for T21, T26, T32, T33 and T34. The lane leaves this heading and puts the following to the pause:

- **Four register rows expected** (brief § 9), each put to the coordinator and none decided by the lane: F-ES-24's toast behind a long card; the re-queued toast's duration (L-01, 3.14; the order itself is D-UI-093's, already decided, so the pause rules only whether the fix lands); the second `BUTTON_GRID_HORIZ_PADDING` (L-13); and the CLEAR without a question (L-14).
- **Rule-6 candidates, contained:** L-01 (pop the front), L-03 (take the lock), L-10 (log `item`), L-11 (probe outside the list lock, #1283's es-core half), L-24 (a stack event), L-06's `es_input.cfg` through `AtomicFile`, and L-07's read with `exists(path, false)` once 3.11 has run.
- **The collision:** T34's `s2-window.patch` (#1310), which changes `createAsyncNotificationComponent`'s return. It touches 10 es-app callers in five lanes and the three doubles, so § 1 i names it in the hand-back.
- **#1305:** the window's half (a start the top page can refuse) beside T33's and T2's halves, named for their owners.

## Positives

- `GuiMsgBox::deleteMeAndCall` copies the callback before `delete this` and calls the copy after (`guis/GuiMsgBox.cpp:286-292`): the safe shape, and the model for the other 16. None of them touches a member after the delete. `proved: tree`.
- Every `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), and `removeGui` clears the mouse capture (`Window.cpp:86-87`), so a captured component freed under its page leaves no dangling pointer. `proved: tree`.
- `processPostedFunctions` copies and clears under the lock, then runs outside it (`Window.cpp:1292-1307`), so a post may post again without a deadlock. `proved: tree`.
- One floating surface at a time holds both ways (D-UI-093): a toast waits for the card (`:336-337`), and a card puts the toast's words back (`:1161-1165`). `proved: tree`; G-02 frames it.
- The window and T34's component compute the same centred position (`:1192`, `AsyncNotificationComponent.cpp:112`). `proved: tree`.
- `doOnFinish` masks its logged command (`InputManager.cpp:1270`). `configureEmulators` carries no device name (`:1481-1482`), so the blob it splices is index and hex only. `proved: tree`.
- All 61 msgids and all 28 `pgettext`/`ngettext` entries have their French at the pin. `proved: tool-run`.
- The logger and the watcher thread are joined (`Log.cpp:76-77` from `onExit`; `WatchersManager.cpp:154` from `stop()`). Every `.cpp` of the 96 is registered once in `es-core/CMakeLists.txt`. `proved: tree`.

## The #585 lines owed

One line per upstream-carried defect closed under rule 6, in the lane's shape, **never sent** (D-WORKFLOW-164, D-WORKFLOW-165). At stage B none is closed yet, so each is a line owed **if** the pause rules its fix. They are listed for the coordinator, beginning with T33's never-posted candidate:

- `es-core/src/watchers/WatchersManager.cpp:181-199` (`rocknix/master`): the watcher list lock is held across every `check()`, so `ResetComponent`/`GetComponent`/`Register`/`Unregister` wait on the interface thread for a network probe. Fix: snapshot under the lock and probe outside it, re-validating. Evidence: 3.1. This is T33's candidate and this slice's lock line.
- `es-core/src/Scripting.cpp:88-113` (`rocknix/master`): arguments are quoted only on a space and `"` is stripped, so `$`/backtick reach `/bin/sh -c`. Fix: single-quote every argument. Evidence: 3.4.
- `es-core/src/Window.cpp:339-340` (upstream's queue): the toast queue pops its newest. Fix: pop the front. Evidence: 3.14.
- `es-core/src/Window.cpp:1262-1274`: `unregisterPostedFunctions` walks `mFunctions` without the lock its two siblings take. Fix: take it. Evidence: 3.17.
- `es-core/src/InputManager.cpp:946`, `:960`: the approximate-match log reads the node before it is assigned. Fix: log `item`. Evidence: 3.10.
- `es-core/src/InputManager.cpp:795`: a `new SDL_Event` per F4 press, never freed. Fix: a stack event.
- `es-core/src/guis/GuiTextEditPopupKeyboard.cpp:14`: the second `BUTTON_GRID_HORIZ_PADDING`, **only if** the pause deletes or renames it.
- **No line** for the controllers blob: at the pin it carries no device name (L-20, contradicted).

## What T36 and T37 inherit

Brief § 5 item 3's items, with their lines:

1. **The provenance table:** 1 / 12 / 83, with both bases named (`cada856d86` against `rocknix/master`, `1750dded8c` against `batocera/master`). § Coverage, § The merge debt.
2. **The surfaces table:** the queue's two containers and the lock, and every enqueue, dequeue, layout and free with its invariant (`Window.cpp:293-1307`). § The surfaces.
3. **The input table:** every write site with its mechanism and atomicity, and every `exists(` of the input files with its writer (`InputManager.cpp:893`, `:1187`, `:1225`, `:1232`, `:1250`; `GuiDetectDevice.cpp:127`). § The input.
4. **The locks table:** every lock, its sites and order, and the interface-thread entry points that block (`WatchersManager.cpp:66`, `:78`, `:94`, `:143`, `.h:35`). § The locks.
5. **The lifetimes table:** 18 thread lines, 4 detaches, 17 `delete this`, 6 posts and 8 raw pointers. § The lifetimes.
6. **The scripts table:** the four `ProcessStartInfo` sites and `Platform.cpp:162-181`'s shell. § The scripts.
7. **The `window-input-tests` build recipe** (the doubles, the extracts, the pugixml root, the fakes the first errors forced): owed at stage C, `tools/t35-build-tests.sh`.
8. **The stand-in's rc per file over the 44:** owed at stage C, `stage-a/syntax-check.out`.
9. **The branches it did not parse:** `HAVE_UDEV` (23 lines), `_ENABLE_PULSE_` (7), `_ENABLE_TTS_` (5), `HAVE_LIBCEC` (11), and the WIN32 branches. § The structure's guards.
10. **The `exists` cache's answer for T36's `FileSystemUtil`:** misses are stored (`FileSystemUtil.cpp:296`, `:323`), and a writer outside `Utils::FileSystem` is invisible to the cache. Read at stage B; 3.11 proves it at stage C.
11. **`Window.cpp:29`'s disposition:** recorded as upstream's (L-04, D-UI-079). § The structure.
