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

<!-- GEN t35-surfaces.py rows=22 containers=5 sites=15 -->

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

- **The grant:** #682 comment 6540234733 (06:45 UTC), queued behind M7. The coordinator's 10:42 block fixed the order (slot 1 M7 native, slot 2 M7's RA guest, slot 3 T35, slot 4 M7's cloud-native guest). M7's slot 2 returned at 11:06:57. **START 11:07:40 UTC** (#682 comment 6542598902; the host file read at 11:07:26; the host-file line with the census `qemu 0, compilers 0, listeners 0`). **RETURN 11:31:00 UTC** (#682 comment 6542812230; the census `qemu 0, compilers 0, listeners 0`), inside the 11:42:40 bound.
- **The timer:** pid 3085742 armed at START for 11:42:41. It carried `--timeout 90`, which `tools/vm-stop` refuses (at most 60 s). That was found when my own stop failed at 11:24:57 (the first boot still up, the second boot refused the disk), then replaced by its PID with pid 3339644 at the same deadline and `--timeout 60` (`guest-cycle/helpers/stop-timer.sh`). It was stopped by its PID at the RETURN, unfired. Supervision was continuous, never 60 s apart.
- **The image:** `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` (sha256 matching its `.sha256`), read from the guest as `BUILD_ID=069fc270442134fe771258418adf4e666e0473fb`, `BUILD_BRANCH=build/m7-signin-20261022-07`, at `640x480-0` (`guest-cycle/g01-identity.txt`). Every frame is **`image`** side (ES sha256 `25155163...1226`, M7's composition).
- **The network:** `restrict=on` plus `guestfwd=tcp:10.0.2.100:9010-tcp:127.0.0.1:9010`, read back from `/proc`. A `tcp:` guestfwd is one connection opened at QEMU's start, so after rclone's first connection the WebDAV did not answer (`curl` rc 28). G-02 and G-09 ran on the unreachable cloud's bounded outcomes, which still draw the card and the page.
- **G-01:** `640x480-0`; theme `es-theme-art-book-next`. The user `es_input.cfg` exists before any configuration (117,859 bytes, the shipped copy: PL-04 lowered). The shipped file has 0 `inputAction` lines. libudev is linked (1). No `/usr/bin/scripts` and no user scripts folder (PL-03 needs an added hook). `curl` is present. `proved: guest`.
- **G-02 and G-03:** under SYNCING SAVES AT STARTUP (`g02-01.png` RECEIVING · STARTING..., `g02-29.png` SENDING · STARTING..., 11:11:51 to 11:12:34), `POST /notify` sent T35 TOAST A then T35 TOAST B at 11:11:48 (guest clock). No toast was drawn while the card was up. After it left, **both appeared together, B above A** (`g02b-001.png`, 11:13:37): newest first, L-01/PL-02 on the image. The card's solid run is x 23 to 616 at row 60 (`tools/t35-png.py`), centred at 319.5 -- 0.9 W plus, by inference, the frame image's outset. `proved: guest`.
- **G-04:** REALLY RESTART EMULATIONSTATION? YES / NO (`g04-2-dialog.png`). B closed it and ES stayed pid 1605 (`g04-pids.txt`). MAIN MENU and QUIT at 640 draw no window help bar (`g04-0-menu-bottom.png`, `g04-1-quit-page.png`, L-21). `proved: guest`.
- **G-05: `CANNOT`.** REMOVE CONNECTION refuses with one OK while the automatic save syncs are on (`g05-4-dialog.png`), and a serial `set_setting cloudsaves.startup 0` did not reach ES's own copy (`g05-6-dialog2.png`). The two-button dialog was not reached. The candidates stay: REMOVE CONNECTION / CANCEL (`GuiMenu.cpp:8057-8058`), USE CONNECTION / CANCEL (`:8025`).
- **G-06:** the keyboard is full-screen at 640 (`g06-walk/03-folder-editor.png`). ESC closes it with SAVES FOLDER unchanged (`g06-1-after-esc.png`). `s` with the keyboard device types into the field rather than acting as X, so L-14's clear-and-commit is not shown by this route (`g06-3-after-s.png`). The startup card drew over the keyboard's field (PL-34). `proved: guest`.
- **G-07 (French):** VRAIMENT REDÉMARRER EMULATIONSTATION ? OUI / NON (`g07-1-quit-dialog-fr.png`). B kept ES pid 6597. The detect page fits at 640 (`g07-4-detect-fr.png`). The AZERTY keyboard shows EFFACER / ANNULER (`g07-walk/03-folder-editor.png`). `proved: guest`.
- **G-08:** HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT. at 640 (`g08-2-detect-page.png`). **One `sendkey x 1000` over the monitor held a key, and the page advanced** to CONFIGURING / KEYBOARD (`g08-3-after-hold.png`): the harness gap is closed. `proved: guest`.
- **G-09:**
  - The screensaver came up after about five idle minutes (`g02b-115.png`, 11:16:42). `shift` woke it with the carousel unmoved (`g09-2-after-shift.png`), and `down` then moved it (`g09-3-after-down.png`).
  - With SCREENSAVER AFTER at 60 s, **the screensaver started over VÉRIFICATION DE VOTRE CLOUD while its job ran** (`g09-4-page-t30.png` at 11:29:33, ÉCOULÉ 0:47; `g09-4-page-t45.png` black at 11:29:49): #1305's window half on the image. `proved: guest`.
- **G-10: `CANNOT`** (no pad).
- **G-11 (1280x800, `1280x800-0`):**
  - The keyboard is a box of about 0.78 W x 0.6 H with the help bar under it (`g11-walk/03-folder-editor.png`). The QUIT box is about 0.6 W wide, with OUI / NON (`g11-1-quit-dialog-1280.png`).
  - **T34 PL-05 reproduced:** the tabbed SCRAPEUR page's bar reads FERMER and RETOUR with a row and with the strip focused (`g11-4-scrapeur-row.png`, `g11-5-scrapeur-strip.png`).
  - The non-tabbed PARAMÈTRES AUDIO page shows FERMER, RETOUR, CHANGER and CHOISIR through the same window (`g11-3-scraper-tabs.png`), so the prompts are lost before the window (L-28). `proved: guest`.
- **G-12:** the disk retired (`guest-cycle/retired.txt`): `/workspace/tmp/m6-t35/guest/disk.qcow2`, 2,312,372,224 bytes, sha256 `c98ec34b491ff866f9d2e135af5374e7bb6cb7f34e695c42b3a77a6c4d1385e7`, now absent. The host's WebDAV is down by its pidfile. Leftover check: `qemu 0, compilers 0, listeners 0`.
- **Time to play** (for the retro): on the unreachable cloud the startup card stayed at STARTING... for about 100 s while the hub row reads AT STARTUP - SKIPPED, NO NETWORK (`g05-0-hub-bottom.png`). That is the cloud lane's bounded sync, recorded for its owner.

## The streams

**Stage E, as the coordinator's stream brief orders it** (`docs/reviews/briefs/t35-streams.md` at `0f9f8f69fe` on the coordinator's branch; twenty-one rulings, D-UI-134 to D-UI-137, Backlogs #1344 to #1347). One row per stream, written as each lands; each before and after line is the build script's own (`stage-e/sN-before.txt`, `sN-after.txt`), asserted by `tools/t35-runs.py` in § The runs, and each stream's other checks are `stage-e/sN-checks.txt`. Every guest half is `fix-walk-pending-image`: the coordinator's, at the integration window, on the image that carries the fix.

| Stream | Items and bugs | Positive before | ES commit | Positive after | `Already written:` | proved: | The guest half; patches and collisions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | PL-15, #1342 (ruling 5) | the drive dialogs' cases (`tools/t35-window-input-tests.cpp`, the pin's accelerator `guis/GuiMsgBox.cpp:116-134` over each call's labels read from `Window.cpp`): back binds YES, MERGE DRIVE on GAME DRIVE DETECTED with an id and YES, FORMAT & MERGE on both NEW DRIVE DETECTED forms -- `window-input-tests` 16 cases, 10 failed (the seven candidates and these three); 3.18 and the two NO-by-name guards PASS | `56aa398b8` (`Window.cpp`, 9 insertions, 6 deletions; the labels and their lambdas reordered, no word changed) | 16 cases, 7 failed (the seven candidates only): back binds NO, IGNORE THIS TIME (both with-id forms), NO, IGNORE, and NO by name; the stand-in 44 of 44; the lane's count 2 three-button calls without OK or NO in the 96, both now ending on the safe choice (es-app's 3 for #1344) | #1342's: a merge already applied by a back press is persisted for future boots and is indistinguishable from one chosen on purpose -- nothing migrated; the fix changes the dialog, not what an earlier press wrote | `fix-unit-test` | `fix-walk-pending-image`: `POST /storage/event` with a `REQUEST_MERGE` line, then `z`; a frame with the dialog closed and no `Merge requested` toast, and no merge request in the journal, at 640x480 and 1280x800 in English and French (the flow step: the drive dialog's back). No patch; no collision (`GuiMsgBox.cpp` untouched, so T34's `s3-msgbox.patch` is unaffected) |
| S2 | PL-02 #1338, PL-07 #1341, PL-25 #1354, PL-26 #1355 (rulings 1, 2, 15) | at S1's tip: `window-input-tests` 19 cases, 10 failed -- 3.14 (`values: CHECK( B second == A first )`), the interruption case (A on screen, B and C queued, a card: `values: CHECK( C queued == B queued )`), and 3.16's two (`left/right CHOOSE \| up/down CHOOSE == up/down/left/right CHOOSE`; the `a` prompt replaced); `SAN tsan-posts ... rc 66`, the first report the post's write of `mTimeSinceLastInput` against update's (`x_posts_post.inc:13` against `x_upd_idle.inc:2`), 3.17's race in its second phase | `453dffd0a` (`Window.cpp`, `Window.h`; 35 insertions, 11 deletions) | 19 cases, 6 failed (3.1, 3.4, 3.5, 3.10, 3.11, 3.19 only); `SAN tsan-posts (-fsanitize=thread): rc 0; no sanitizer report`, the PL-26 phase included; the stand-in 44 of 44; es-app's `main.cpp` syntax-only rc 0 against the atomic flag | nothing inherited (#1338, #1341, #1354, #1355): the queue, the posted functions, the prompt list and the idle count live in memory | `fix-unit-test` | `fix-walk-pending-image`: two `POST /notify` while a card is up, then a frame after it leaves with the toasts in the order posted; a list's help bar at 640x480 in French with the dpad prompt merged (the flow steps: the toast order after a card; the list's help bar). No patch. The one departure from the brief's words: the refresh event stays with the post (it ends the loop's `SDL_WaitEventTimeout`), `mSleeping` atomic for the post's read (`stage-e/s2-checks.txt`). Collision: T34's `s2-window.patch` hunks (`@@ -1149`, `@@ -1165`, `@@ -1245`) sit beside the re-queue edit and `Window.h`'s members; the hand-back dry-runs it |

At stage B the lane left this heading for the pause with the following, which the brief's rulings now dispose:

> Stage E: **written by the coordinator after stage D**, as for T21, T26, T32, T33 and T34. The lane leaves this heading and puts the following to the pause:
>
> - **Four register rows expected** (brief § 9), each put to the coordinator and none decided by the lane: F-ES-24's toast behind a long card; the re-queued toast's duration (L-01, 3.14; the order itself is D-UI-093's, already decided, so the pause rules only whether the fix lands); the second `BUTTON_GRID_HORIZ_PADDING` (L-13); and the CLEAR without a question (L-14).
> - **Rule-6 candidates, contained:** L-01 (pop the front), L-03 (take the lock), L-10 (log `item`), L-11 (probe outside the list lock, #1283's es-core half), L-24 (a stack event), L-06's `es_input.cfg` through `AtomicFile`, and L-07's read with `exists(path, false)` once 3.11 has run.
> - **The collision:** T34's `s2-window.patch` (#1310), which changes `createAsyncNotificationComponent`'s return. It touches 10 es-app callers in five lanes and the three doubles, so § 1 i names it in the hand-back.
> - **#1305:** the window's half (a start the top page can refuse) beside T33's and T2's halves, named for their owners.

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

**Stage E's lines, each stream's `git log -S` saying whose the line is** (ruling 19; never sent, the coordinator posts them after acceptance):

- **S1, PL-15 (#1342):** `es-core/src/Window.cpp:1568-1578`, `:1630-1648` (`rocknix/master`): GAME DRIVE DETECTED and NEW DRIVE DETECTED list NO, IGNORE THIS TIME / NO, IGNORE FOREVER / YES, MERGE DRIVE (or YES, FORMAT & MERGE), and no name is OK or NO, so `GuiMsgBox`'s back falls through to the last button: a merge kept for future boots, or the format's confirmation. Fix: YES first and the choice that changes nothing last, no word changed. Evidence: the drive dialogs' cases. Whose: `git log -S'NO, IGNORE THIS TIME'` names `a8513aec1` and `eeaa8616a` (Daniel Martin, 2026-03-24 and 2025-12-08), both ancestors of `cada856d86`: upstream ROCKNIX's.
- **S2, PL-02 (#1338):** the stage-B line for `Window.cpp:339-340` stands, now closed. Whose: the pop is `49efd94495` (blame) from `ac0fbeac8` (`git log -S'pop_back'`), both ancestors of `cada856d86`: upstream's. The re-queue (`:1163-1164`) is the fork's `c1c0d6ddcf`, so no line for that half.
- **S2, PL-07 (#1341):** the stage-B line for `Window.cpp:1262-1274` stands, now closed. Whose: `c5ceca49a8` (2021-05-13, *Fix potential crash with gameslists*), an ancestor of `cada856d86`: upstream's.
- **S2, PL-25 (#1354):** `es-core/src/Window.cpp:1032-1033` (`rocknix/master`): the help bar's dpad merge compares with `!=`, so the dpad's two halves with one action stay apart, and an unrelated prompt with that action is replaced by `up/down/left/right`. Fix: `==`. Evidence: 3.16's two cases. Whose: `8d7fb7b3e8` (2019-04-25, *the big merge*), an ancestor of `cada856d86`.
- **S2, PL-26 (#1355):** `es-core/src/Window.cpp:1284-1289` (`rocknix/master`): `postToUiThread` writes `mSleeping` and `mTimeSinceLastInput` from the posting thread while `update` and `render` read and write them unlocked. Fix: mark the wake under the queue's lock and apply it in `processPostedFunctions`; keep the refresh event with the post; `mSleeping` atomic for the post's read. Evidence: `tsan-posts`' first phase. Whose: `d1106f674a` and `8c25e2b086` (2022-02-05 and -06), ancestors of `cada856d86`.

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
