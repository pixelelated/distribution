# T35 (#682): the stream brief for stage E

Written at the pause from the lane's punch list (#1337, comment 6542917786 on #682; the record at `5d7650c1dc`), drafted by an agent from T34's shape and ruled by the coordinator on 16:01 UTC 2026-10-31 (the `RULING` lines). The register rows the rulings force are D-UI-134 to D-UI-137; the Backlogs they name are #1344 to #1347. The brief is `es-core-window-input.md` at `8b5d9b9b62`; where this file and the brief differ, this file wins for stage E.

**The coordinator's, drafted at T35's stage-D pause, 15:56 UTC 2026-10-31.** The continue message found no draft on disk (`ls` of this path at 15:42:49 and 15:51:30 UTC: `No such file or directory`), so this file is written whole, not appended. Read from the lane's record at the distribution tip **`5d7650c1dc`** on `feature/m6-es-core-window-input-682` by `git show` only, never the worktree: `05-punch-list.md` (34 items), `04-analysis.md` (§ The questions, § Second opinion, the take-up table), `02-forward-audit.md` (§§ The leads, The surfaces, The input, The locks, The lifetimes, The scripts, The words, The merge debt, The runs, The guest cycle, The streams, The #585 lines owed, What T36 and T37 inherit), `03-retrospective.md`, `00-running-log.md`, `stage-c/build-tests.out`, `stage-c/asan-watchers.out`, `stage-a/syntax-check.out`, `stage-a/runs.out`, `tools/t35-build-tests.sh`, `tools/t35-extract.py`, `tools/t35-window-input-tests.cpp`. The tracker: the punch-list post on #682 (comment 6542917786, 11:43:13Z), the stage-C acceptance and stage-D word (comment 6542863818, 11:37:16Z), the audit issue #1337 (`34 findings (0 critical, 1 high)`), the bugs #1338 (PL-02), #1339 (PL-03), #1340 (PL-04), #1341 (PL-07), #1342 (PL-15, High), #1343 (PL-27), T35's traces on #1283 (comment 6542901479) and #1305 (comment 6542901694). The slice brief `docs/reviews/briefs/es-core-window-input.md` at `8b5d9b9b62` (§ 1 rulings (a) to (i), § 4 Q1 to Q7 and the floor table 3.1 to 3.27, § 7, § 9, § 10). T34's held patches on `feature/m6-es-core-components-681` (`docs/audits/2026_10_30-epic-m6-es-core-components/stage-e/s2-window.patch`, `s2-holders.patch`, `s3-msgbox.patch`), T34's ES tip `52f0ff512` and its amended hand-back (2) (`kit/t34-handback-amended2.md`). A pin line the record does not carry was read at the pin by `git -C <W> show 16dbac5211:<path>` and is marked *(pin read)*. The register at the coordinator worktree's `48c75dea78`: D-UI-093 is `:404`; the highest decided rows are D-UI-133 and D-WORKFLOW-215, so a row this pause writes takes the next ID the coordinator assigns (D-UI-134 onward at this read).

The ES branch `feature/m6-es-core-window-input-682` in `W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682` is at the pin `16dbac5211eea7e70db7394372033be2be7df829` (`git -C <W> rev-parse HEAD`, this draft's read) and not on `origin` (`rev-parse --verify origin/feature/m6-es-core-window-input-682` prints `fatal: Needed a single revision`); it reaches `origin` with S1's push. The distribution worktree `/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-window-input-682` takes only the audit folder's records (`docs/audits/2026_10_31-epic-m6-es-core-window-input/`, its `tools/` included) and the day's log.

**The coordinator's standing rulings for this slice, applied here and not re-asked:** PL-02 is a defect against D-UI-093's decided row (`decision-register.md:404`, *the order is the order things happened*): pop the front, and returned toasts go back at the front. PL-03 and PL-15 are public bugs (#1339; #1342, High as data safety). PL-04 stays Low (G-01). T34's `s2-window.patch` (#1310) and `s3-msgbox.patch` are collisions named for the integration, not adopted by T35; PL-06 is a design ruling (ruling 6 drafts the two options with their costs). Every fix is a `bug` or a rule-6 item with its unit case seen to FAIL at the pin first. Nothing changes outside the 96 paths, and the French catalog changes in the same commit as any changed sentence. `Already written:` is argued per writer: `es_input.cfg`, `es_last_input.cfg`, the favourites file and the log, and *nothing inherited* where no file is written.

## The rulings the pause needs

Each ruling gives the items with their lines (`05`'s), what the lane proposed, the options, and an answer drafted from the rules for the coordinator to edit. The `RULING:` line is the coordinator's.

1. **PL-14, F-ES-24: a toast held behind a long upstream card** (`Window.cpp:336-337`; Low; Q1; a register row, brief § 9's first).
   - **The lane proposed:** *a pause ruling: stands, or a bound* (`05` PL-14); `02` § The surfaces: *stands as recorded, with a bound proposed for the pause*.
   - **Options:**
     - (a) **Stands.** Every toast waits while any card is up, the hasher's minutes-long card included. Nothing is dropped, and the toasts show after the card in the order things happened (S2's PL-02 fix).
     - (b) **A bound.** A toast held past N seconds is shown over the card. That puts a pop-up over a pop-up, which D-UI-093's own quote rules out: *"That should be something we always avoid."*
     - (c) **Fork cards only.** Only the fork's cards hold toasts, and an upstream card lets them through. This is the same overlap, under the hasher's card.
   - **Drafted answer:** (a), as a register row.
     - D-UI-093 decides one floating surface at a time, and D-UI-079 keeps the hasher's card as upstream has it.
     - The one thing the two rows left open is how long a toast may wait. The answer is: as long as the card runs, then in order.
     - The row names its cost. A toast's news can be stale by the time it shows: a pad connected and then disconnected under the hasher's card shows both toasts after the card, in order.
     - `least-surprise.md`: an order the player can follow beats an overlap they cannot read.
   - **RULING (coordinator, 16:01 UTC 2026-10-31):** (a), as D-UI-134: a toast waits as long as any card runs, then shows in order; no bound, no overlap; the row names the cost (stale news after a long card). A long card is the card's own problem, named for its owner (#1345 for the startup sync's 100 s).
2. **PL-13: a re-queued toast returns whole, with a fresh default duration** (`Window.cpp:1164`; Low; Q1; a register row, or folded into ruling 1's).
   - **The lane proposed:** *recorded as written; the pause may rule otherwise* (`05` PL-13). `02` § The surfaces: *a toast half-read then re-shown whole costs the player seconds and loses no words*.
   - **Options:** (a) whole, as at the pin; (b) the remainder of its time.
   - **Drafted answer:** (a), folded into ruling 1's row as its second sentence.
     - A remainder can be a few hundred milliseconds, which is a flash nobody reads (`player-language.md`: clear first).
     - The case `3.14 a re-queued toast returns with the default duration, not its remainder` (`tools/t35-window-input-tests.cpp:69-77`) passes at the pin. It stays as the contract.
   - **RULING (coordinator, 16:01 UTC 2026-10-31):** (a), folded into D-UI-134's second sentence: a re-queued toast returns whole with its default duration; 3.14 stays as the contract.
3. **PL-11: one macro name, two values** (`guis/GuiTextEditPopupKeyboard.cpp:14`, `:220` against T34's `components/MenuComponent.cpp:14`; Low; Q6; a register row).
   - **The lane proposed:** *the keyboard's own name (the value is its design), or one definition* (`05` PL-11).
   - **Options:**
     - (a) **A rename.** The keyboard's constant gets its own name, keeping its value `0.0052083333`.
     - (b) **One definition.** The keyboard reads the house `0.022`.
   - **Drafted answer:** (a), as a register row (one name, one meaning).
     - **Why the keyboard keeps its value.** At `:220` *(pin read)* the value pads every key on all four sides at a quarter of the constant. That is a key grid's inset, not the gap between two buttons on a menu's bar, which `es-native-ui.md` § Spacing protects.
     - **What (b) would cost.** Under (b) every key's inset grows as R4 item 6 measured (the brief § 4 Q6: *the key grid would grow 4.2x*), on a keyboard that is full-screen at 640 (G-06).
     - **The keyboard's destructive key is handled elsewhere.** The thumb's-width danger the house value guards is CLEAR, and ruling 4 stops CLEAR from committing anything.
     - **3.19 changes shape.** As written (`tools/t35-window-input-tests.cpp:183-186`) it asserts the two values are equal, which fits (b). Under (a) it asserts instead that `BUTTON_GRID_HORIZ_PADDING` is defined in one of the two files. That still FAILs at the pin, where both `kb_pad` and `menu_pad` hold the name (`tools/t35-extract.py:20-21`). The re-written stub runs against the pin before the fix, and the `kb_pad` spec changes under D-WORKFLOW-210.
     - **T34's comment goes stale.** At T34's ES tip, `MenuComponent.cpp:9-10` reads *"The keyboard popup keeps a second copy of it (GuiTextEditPopupKeyboard.cpp) until that file reads this one (#1320)"* (`52f0ff512`, read by `git show`). Under (a) that sentence is false. It is merge debt for the integration (T34's file), and the lane does not change it.
   - **RULING (coordinator, 16:01 UTC 2026-10-31):** (a), as D-UI-135: the keyboard's key inset is its own constant with its own name and its value; one name has one meaning, so `BUTTON_GRID_HORIZ_PADDING` is defined once, in `MenuComponent.cpp`. 3.19 is re-shaped to assert the single definition and seen to FAIL at the pin before the fix. T34's comment at `MenuComponent.cpp:9-10` goes stale: merge debt for the integration, not the lane's edit.
4. **PL-12: CLEAR and the keyboard's `x` commit an empty value with no question** (`guis/GuiTextEditPopupKeyboard.cpp:392-397`, `:491-496`; `guis/GuiTextEditPopup.cpp:34`; Low; Q6; a register row).
   - **The lane proposed:** *a pause ruling (a register row)* (`05` PL-12).
   - **Options:**
     - (a) **Ask.** CLEAR asks first (a `GuiMsgBox`). That adds a new sentence and its French, and a dialog over a full-screen keyboard.
     - (b) **Clear only the text.** CLEAR empties the field and keeps the popup open. OK commits, and CANCEL or back discards.
     - (c) **Stands.**
   - **Drafted answer:** (b), as a register row.
     - **Why (b) needs no question.** A consequential action asks (`es-ui-style-guide.md` § Confirmations), and (b) removes the consequence instead of adding a question. Nothing is committed until OK, so no sentence is added and no French is owed.
     - **The lane read.** The two popups' CLEAR is one of D-UI-079's lanes (the brief § 1: *"the two text popups' CLEAR (`c8dc72cf9`)"*).
     - **Least surprise.** CLEAR in a text editor clears the text. One press must not empty a Wi-Fi key or the cloud folder and save it (`least-surprise.md`).
     - **What the player still can do.** A player who wants an empty value presses CLEAR, then OK.
     - **Cost.** The two popups are shared by every page (17 es-app includers each, `02` § The structure). Every page's CLEAR changes behaviour, the upstream pages' included, so the row says this is the lane's surface reaching outside it.
   - **RULING (coordinator, 16:01 UTC 2026-10-31):** (b), as D-UI-136: CLEAR empties the field and keeps the popup open; OK commits, CANCEL or back discards; no question, no new sentence, no French owed. The two popups' CLEAR is within the lane (`c8dc72cf9`); the row says the change reaches every page that uses the popups, upstream's included, as the surface's own behaviour, not a page's.
5. **PL-15's fix shape, and the dialog's fall-through** (`guis/GuiMsgBox.cpp:116-134` (`:132-133`), `:257`; `Window.cpp:1568-1578`; High; Q6; #1342).
   - **The lane proposed:** *a button named exactly `NO` (or the accelerator bound to the non-destructive choice), and the buttons ordered with the safe one last; the component's fall-through put to the pause* (`05` PL-15; #1342's second checkbox).
   - **The dialogs at the pin *(pin read)*:**
     - **GAME DRIVE DETECTED with an id** (`:1568-1578`): NO, IGNORE THIS TIME / NO, IGNORE FOREVER / YES, MERGE DRIVE. Back takes YES, MERGE DRIVE.
     - **GAME DRIVE DETECTED without an id** (`:1583-1586`): YES / NO. Back binds NO by name.
     - **NEW DRIVE DETECTED with an id** (`:1630-1640`): NO, IGNORE THIS TIME / NO, IGNORE FOREVER / YES, FORMAT & MERGE. Back takes YES, FORMAT & MERGE, which opens ARE YOU SURE? NO / YES (`:1622-1625`).
     - **NEW DRIVE DETECTED without an id** (`:1645-1648`): NO, IGNORE / YES, FORMAT & MERGE. Back takes the format's confirmation.
   - **Options:**
     - (a) **Reorder only.** The callers are reordered, YES first and the safe choice last, and the fall-through stays. The dialogs read YES, MERGE DRIVE / NO, IGNORE FOREVER / NO, IGNORE THIS TIME; YES, FORMAT & MERGE / NO, IGNORE FOREVER / NO, IGNORE THIS TIME; and YES, FORMAT & MERGE / NO, IGNORE.
     - (b) **Rename to NO.** The safe button is renamed exactly `NO`, whose French `NON` the catalog already has (`:85-86`). This drops the THIS TIME / FOREVER distinction the player reads.
     - (c) **Change the component.** Back binds nothing when no button is named OK or NO.
   - **Drafted answer:** (a).
     - **What the style guide says.** `es-ui-style-guide.md` § Confirmations documents the fall-through as the component's contract (*"falls through to the last button if neither exists. Never let 'back' land on the destructive choice"*) and asks for YES first. Under (a) the callers keep that contract, back lands on the one choice that changes nothing on this or a future boot, and no word changes. That means no msgid and no French.
     - **Why not (b) or (c).** (b) loses information the player needs. (c) leaves a dialog back cannot leave, and changes every es-app caller's behaviour (`GuiMsgBox.h`: 43 es-app includers, `02` § The structure).
     - **What stays.** `:257` (an unconfigured pad's any button fires the accelerator) is upstream's way out for an unconfigured pad. It becomes safe once the safe button is last, so it stays. ARE YOU SURE? keeps NO / YES: back binds NO by name, and its words are upstream's (D-UI-079). It is recorded.
     - **The lane's grep.** The lane counts the `GuiMsgBox` calls in the 96 with three buttons and none named `OK` or `NO`. es-app's are named for the coordinator as a Backlog, never edited here.
   - **RULING (coordinator, 16:01 UTC 2026-10-31):** (a): reorder only -- YES first, the safe choice last, no word changed, the component's fall-through kept as the style guide's contract; `:257` stays; ARE YOU SURE? stays NO / YES. The es-app dialogs with three buttons and no OK/NO are #1344 (the coordinator's Backlog); the lane's count of es-core's goes in `02`.
6. **PL-06: the window's teardown, and T34's `s2-window.patch`** (`Window.cpp:188-207`, `:49-63`, `:1246-1248`; Medium; Q4; no bug).
   - **The lane proposed:** *a design ruling at the pause: T34's `s2-window.patch` (#1310) is a collision (10 es-app callers, 3 doubles); the window-side alternative frees cards and popups in `deinit` and refuses a close after it* (`05` PL-06).
   - **(A) Defer the card half to #1310.** T34's handle lands at the integration, and T35 makes no teardown change in stage E.
     - **The cost, which is the integration's:**
       - The patch changes `createAsyncNotificationComponent`'s return. Ten es-app call sites in five lanes change with it (`ContentInstaller.cpp:60`; `ProxyCards.cpp:215`, `:257`, `:514`; `ThreadedBluetooth.cpp:15`, `:72`; `ThreadedCloudSync.cpp:46`; `ThreadedHasher.cpp:126`; `guis/GuiMenu.cpp:11717`; `guis/GuiUpdate.cpp:162`), and so do three doubles (`tests/app-unit/fakes/Window.h:11`, `ProxyCardsTests.cpp:154`, `tests/hasher-offline-index.py:65`) (`02` § The surfaces, `:204`).
       - T34's `52f0ff512` makes the holders change only their declarations (its subject: *"the progress card's handle forwards a holder's calls and keeps the pointer's null"*).
       - `s2-holders.patch`'s hunk 3 FAILs over T2's `ProxyCards.cpp` at `:235` (`kit/t34-handback-amended2.md` item 8).
       - The patch's hunks (`@@ -1149`, `@@ -1165`, `@@ -1245`) sit beside S2's PL-02 edit to the re-queue loop (`:1163-1164`), so the hand-back re-proves it by `patch --dry-run` over T35's tip.
     - **The benefit.** A holder's late call after `:1248` becomes safe. That is the half of L-02 that matters.
   - **(B) The window-side teardown, in a T35 stream.** `deinit` and `~Window` free the popups (`stopNotificationPopups`, `:353`, already deletes every popup) and the queue.
     - **The cards.** Freeing them in `deinit` while raw holders live turns a late `updateText` or `close` into a new use after free, from a worker that outlives a game launch. That is the seat's narrowing, verified (`05` PL-06: *"deleting cards in `deinit` alone does not make those holders safe"*). So (B) either leaves the cards, and L-02's card half is unchanged, or needs a "window gone" flag the component reads, which is T34's file.
     - **The cost.** Its lines collide with the patch's hunks in the same two functions. The value is small: a toast redrawn after a game returns, and frees at process end.
   - **Drafted answer:** (A). PL-06 is deferred to #1310 at the integration, and no Window teardown change is made in stage E.
     - **What is already recorded.** `02` § The lifetimes records the teardown order and what a holder may assume: the window is `main`'s stack object, and every holder thread is joined before `window.deinit()` (`main.cpp:1322`, `:1330`, `:1358`) except the four detached storage workers (PL-22).
     - **The hand-back.** It quotes both T34 patches' `patch --dry-run` over T35's ES tip, hunk by hunk.
   - **RULING (coordinator, 16:01 UTC 2026-10-31):** (A): PL-06 is deferred to #1310 at the integration; no Window teardown change in stage E; the hand-back quotes both T34 patches' `patch --dry-run` over T35's ES tip, hunk by hunk.
7. **PL-08: the input files written in place** (`InputManager.cpp:1225`, `:1232`; `FavoriteMusicManager.cpp:71`, `:115`; Low; Q2; D-CLOUD-078's family).
   - **The lane proposed:** *`es_input.cfg` through the fork's `AtomicFile`, the rest recorded* (`05` PL-08).
   - **Options:**
     - (a) `es_input.cfg` alone through `AtomicFile::writeText` (`utils/AtomicFileUtil.h:42`, T21's: write, fsync, rename, fsync the directory; *"on any failure the temporary is removed and `path` is untouched"*, `:30-35` *(pin read)*).
     - (b) (a) plus `es_last_input.cfg`. It is the same function, `writeDeviceConfig` (`:1225`, `:1232`), and the same call.
     - (c) (b) plus the favourites rewrite (`:115`).
   - **Drafted answer:** (b).
     - **The rule.** D-CLOUD-078: a cut write must leave the last good file. The two writes are one function, so one call shape covers both.
     - **The bytes.** pugixml's `save` to a string with `save_file`'s default indent and flags, then `writeText`. The case compares the bytes against `save_file`'s for one document, so the format on disk is unchanged.
     - **The API.** `AtomicFile` is T21's (#668). A use is allowed and a change is not. If the call needs anything the API lacks, the lane posts on #682 and stops that half.
     - **The favourites file.** It is recorded: upstream's music surface (D-UI-079), a #585 line candidate. The log needs nothing (rewritten each start, nothing reads it).
     - **The cost, for time to play.** `writeText` fsyncs twice per save, on the interface thread, at a configuration's OK and on the hot-plug write of an SDL-mapped device (`:605`, inside `mJoysticksLock` `:485-623`; `02` § The input). It is priced on the integration image. G-10 is `CANNOT` for the hot-plug.
   - **RULING (coordinator, 16:01 UTC 2026-10-31):** (b): `es_input.cfg` and `es_last_input.cfg` through `AtomicFile::writeText` (a use of T21's API, never a change to it; a missing capability stops that half and is posted on #682); the bytes compared against `save_file`'s for one document; the favourites file and the log recorded; the fsync cost priced on the integration image (G-10 `CANNOT` for the hot-plug).
8. **PL-17: the per-event `quit` scripts are not waited for** (`Scripting.cpp:142`, `:177`; Low; Q5).
   - **The lane proposed:** *a pause question; recorded* (`05` PL-17).
   - **What happens at the pin *(pin read)*.** The per-event pass calls `executeScript(script, "", ...)` (`:177`), and `waitForExit = (eventName == "quit")` (`:142`), so a `quit` hook in `scripts/quit/` runs detached while EmulationStation exits.
   - **Options:**
     - (a) **Fix.** Pass the wait decision separately from the argument, so per-event `quit` hooks are waited for.
     - (b) **Record.**
   - **Drafted answer:** (b), with a #585 line.
     - **Not the fork's.** The hooks are upstream's, and the fork works in no hook lane (D-UI-079).
     - **Not on the image.** The image ships no hook (G-01).
     - **(a) adds an unbounded wait to the quit path.** `ProcessStartInfo` has no timeout; it is T36's `Platform.cpp:162-181`.
     - **Intent first.** The lane runs `git log -S'waitForExit = (eventName' -- es-core/src/Scripting.cpp` and records the intent before the line is written.
   - **RULING (coordinator, 16:01 UTC 2026-10-31):** (b): recorded, with a #585 line; the intent read (`git log -S'waitForExit = (eventName'`) recorded before the line is quoted. Not the fork's lane, not on the image, and (a) would add an unbounded wait to the quit path.
9. **PL-18: a per-event folder runs every file in it** (`Scripting.cpp:169-178`; Low; Q5; 3.5 FAILs at the pin).
   - **The lane proposed:** *the single-script pass's filter for both passes; 3.5 the covering case* (`05` PL-18).
   - **What happens at the pin *(pin read)*.** On the device `executeScript` runs the path itself through the shell (`:90`, `:140-147`), so a file runs only when it carries its execute bit. A `notes.txt` without it fails at the exec, and nothing runs.
   - **Options:**
     - (a) **The extension filter for both passes** (`.exe .cmd .bat .ps1 .sh .py`, `:151`).
     - (b) **Record.**
   - **Drafted answer:** (b).
     - **(a) breaks working hooks silently.** A player's executable hook without an extension in `scripts/<event>/` works today. Under (a) it stops running after an update, silently: `upgrade-and-install.md` § An upgrade should be invisible, and `Already written:` names exactly those hooks.
     - **The defect is small.** The file has to be executable to run.
     - **What 3.5 becomes.** It is marked `doctest::may_fail` with PL-18 named (ruling 20), and the record says why. A #585 line is not owed.
   - **RULING (coordinator, 16:01 UTC 2026-10-31):** (b): recorded; 3.5 marked `doctest::may_fail` with PL-18 named (ruling 20); no #585 line (the file must be executable to run; the filter would silently stop a player's working hook after an update).
10. **PL-28: the crash handler flushes a C++ stream from a signal** (`Log.cpp:84-99`, `:237-242`, `:282-285`; Low; Q4).
    - **The lane proposed:** *recorded for the pause: a signal-safe path, or the handler's limits written beside it* (`05` PL-28).
    - **What happens at the pin *(pin read)*.**
      - `crashHandler` (`:237-242`) is registered for SIGABRT and SIGTERM (`:282-285`) and calls `emergencyFlush` (`:84-99`).
      - `emergencyFlush` stores an atomic, calls `notify_one`, sleeps up to 200 x 50 us, then calls `mFile.flush()` (`:98`) on the handler's thread.
      - The worker may be writing the same stream in `drainBuffer`/`writeLine` (`:156-177`).
    - **Options:**
      - (a) **A fully signal-safe path.** A self-pipe or eventfd the worker waits on, and `write(2)` alone in the handler. That redesigns the worker's wait.
      - (b) **The narrow fix.** The handler stops flushing the stream itself (`:98` removed), so only the worker ever touches `mFile`. The handler's bounded wait lets the worker flush its own batch, as #178's per-batch flush (`:135-147`) already does. The remaining non-signal-safe calls (`notify_one`, `sleep_for`) are written beside the handler as its stated limits.
      - (c) **Record**, with the limits written as a comment only.
    - **Drafted answer:** (b).
      - **Why it is enough.** Two threads on one `std::ofstream` is the part that can corrupt the log or fault inside the handler. The lost-lines risk is already bounded by #178 to one batch.
      - **The case.** A ThreadSanitizer program over `emergencyFlush` against the worker. It must report the race on `mFile` at the pin before the fix; if it cannot, (b) falls to (c) and the record says so.
      - **The #585 line.** `git log -S'emergencyFlush'` decides whether it is owed (the logger is fork #178's).
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** (b), conditional: the handler's own `mFile.flush()` goes only if a ThreadSanitizer program shows the race on `mFile` at the pin; if it cannot, (c) -- the handler's limits written beside it as a comment, and the record says why. The #585 question by `git log -S'emergencyFlush'`.
11. **PL-34: a progress card draws over the full-screen keyboard's field** (`Window.cpp:782-788`; Low; Q1; G-06).
    - **The lane proposed:** *a card held while a full-screen popup owns the screen, or recorded as the card tier's design* (`05` PL-34).
    - **Options:**
      - (a) **Hold the card** while a full-screen popup is top.
      - (b) **Record** it as the third tier's design.
      - (c) **Move the keyboard's field** below the card's band, which is a layout change.
    - **Drafted answer:** (b).
      - **The card has to show.** D-UI-095 asks that anything automatic that moves data over the network is shown while it runs (`es-native-ui.md` § How wide and where a progress card sits). Holding the card hides a sync the player is entitled to see.
      - **The real cost is the card's length.** On the window's unreachable cloud *"the startup card stayed at STARTING... for about 100 s"* (`02` § The guest cycle, the time-to-play row).
      - **That is the cloud lane's bounded sync.** D-CLOUD-109 says a sync never takes minutes. It is named for its owner as a Backlog the coordinator files.
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** (b): recorded as the third tier's design (D-UI-095: an automatic sync is shown while it runs); the card's 100 s is the cloud lane's, filed as #1345.
12. **PL-05: the window's half of #1305** (`Window.cpp:777-779`, `:1091-1105`, `:1107-1138` (`:1117`); Medium; Q4; 3.27 FAILs at the pin; G-09).
    - **The lane proposed:** *the window's half proposed for the pause (a start the top page can hold off)* (`05` PL-05). #1305's trace adds: *"or the page resets the idle time while its job runs"*.
    - **Options:**
      - (a) **A hold the top page can claim.**
        - The mechanism: a virtual on `GuiComponent` (`GuiComponent.h`, one of the 96; 74 includers, 37 in es-app, `02` § The structure). It defaults to allowing the screensaver, so every upstream page keeps its behaviour (D-UI-079). `startScreenSaver` (`:1091-1105`) asks the top page before it starts, and `mTimeSinceLastInput` keeps running.
        - The page side: the fourth-tier pages (D-UI-078) override it. That is es-app work, done as `stage-e/` patches for their owners (`GuiCloudTransfer`, T18's #665; the others named by the lane from the slices' globs).
      - (b) **The page resets the idle time while its job runs.** Nothing in es-core changes, and every long page must remember to do it.
    - **Drafted answer:** (a).
      - **Why the window.** A page the player is sat in for a job (D-UI-078) must not be covered by a slideshow while the job runs (`least-surprise.md`; G-09: the screensaver over VÉRIFICATION DE VOTRE CLOUD at 11:29:49 while the job ran). One hold that any page can claim is a rule, not something each page has to remember.
      - **3.27 stays FAIL.** It is T33's harness over `SystemScreenSaver.cpp` and `SystemData.cpp`, whose lines S3 does not change. It stays FAIL until T33's or T2's half lands, and the record says so. S3's own case is the window's.
      - **No double changes.** `Window.h`'s signatures do not change (§ 1 (i)'s doubles untouched).
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** (a): a hold the top page can claim -- one virtual on `GuiComponent` defaulting to allow, `startScreenSaver` asking the top page, `mTimeSinceLastInput` still running; the es-app pages' overrides as `stage-e/` patches for their owners (`GuiCloudTransfer` T18's #665, the others by the slices' globs), named in `02` § The merge debt; `Window.h`'s signatures unchanged; 3.27 stays FAIL with its reason until T33's or T2's half lands.
13. **PL-01's keep-alive** (`WatchersManager.cpp:181-199` against `:66`, `:78`, `:94`, `:143`, `.h:35`; Medium; Q3; #1283).
    - **The lane proposed:** *snapshot the due watchers under the lock, probe outside it with both the record and its `IWatcher` kept alive through the probe (re-validating alone is not enough -- the seat, verified), and make `mRunning` atomic* (`05` PL-01). #1283's trace: *"a reference count, or unregistering deferred while a probe runs"*.
    - **Options:**
      - (a) **Unregister waits for its own probe only.** `UnregisterComponent` of a watcher whose probe is in flight waits for that probe alone (a per-record in-flight mark and a condition variable). `Register`, `Reset`, `Get` and every other watcher's unregister return at once.
      - (b) **A reference count on the record.** It frees later, but the registrant may still delete its `IWatcher` after `UnregisterComponent` returns, so the probe would run on a freed watcher.
    - **Drafted answer:** (a).
      - **Why not (b).** The `IWatcher` is the registrant's object, so only a wait keeps it alive through a probe.
      - **What still waits, and for how long.** The wait now covers only the unregistering page's own watcher, for its own probe's bound. That is recorded beside 3.1's figure.
      - **The order holds.** The lock order `mWatchersLock` -> `mNotificationLock` is never reversed. The next check time is written back under the list lock.
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** (a): `UnregisterComponent` waits for its own watcher's in-flight probe only (a per-record in-flight mark and a condition variable); every other call returns at once; `mRunning` atomic; the lock order `mWatchersLock` -> `mNotificationLock` never reversed; the remaining wait and its bound recorded beside 3.1's figure.
14. **PL-16: the configuration page's subtitle** (`guis/GuiInputConfig.cpp:134`; Low; Q6; a sentence and its French).
    - **The lane proposed:** *the seat or the name; a #585 line* (`05` PL-16).
    - **What happens at the pin *(pin read)*.** `:134` formats `_("GAMEPAD %i")` with `target->getDeviceId() + 1`, and `:136` upper-cases it.
    - **Options:**
      - (a) **The device's name.** `target->getDeviceName()`, upper-cased by `:136`; no msgid when the name is shown. When SDL gives no name it falls back to a new msgid `GAMEPAD` with `MANETTE` (the catalog has only `GAMEPAD %i` -> `MANETTE %i`, `:3898-3899`).
      - (b) **The player's seat number.** The seat is not settled while the pad is being configured.
    - **Drafted answer:** (a).
      - **Why the name.** It is the one thing the player can match to the pad in their hand (`player-language.md`: clear first).
      - **The French.** `GAMEPAD` / `MANETTE` goes in the same commit (D-UI-051). The orphaned `GAMEPAD %i` entry is left to `msgmerge`, as D-UI-133 left `up/down`.
      - **The #585 line.** It is owed if `git log -S` shows `:134` is upstream's.
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** (a): the device's name upper-cased by `:136`, the fallback msgid `GAMEPAD` with `MANETTE` in the same commit (D-UI-051); the orphaned `GAMEPAD %i` left to `msgmerge`; the #585 line if `git log -S` shows `:134` upstream's.
15. **Bugs for the fixed items that have none** (PL-08, PL-09, PL-10, PL-11, PL-12, PL-16, PL-25, PL-26, and PL-28 under ruling 10's fix).
    - **The lane proposed:** *Rule-6 candidates without a bug yet: PL-09, PL-10, PL-16, PL-25, PL-26, and PL-18* (the punch-list post). PL-18 is ruling 9's.
    - **Drafted answer:** each item a stream fixes gets a `bug`, filed by the lane before that stream's commit.
      - **The bug's contents.** Its trace, its positive before the fix, its VM line and its `Already written:` line, passing `tools/box-check --issue N`. It is filed with `tools/t35-file-bugs.py`, in the same shape as #1338 to #1343 and T34's one bug per PL.
      - **The posts.** The new numbers are posted on #682 in one line before S1. Each commit body cites its bug.
      - **What the fixes do.** PL-09: `item` logged at `InputManager.cpp:946`, `:960`. PL-10: a stack `SDL_Event` at `:795`. PL-25: `==` for the complementary half at `Window.cpp:1032-1033`. PL-26: the wake applied on the interface thread, from a flag the drain reads.
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** Yes: every item a stream fixes gets its `bug` before that stream's commit (PL-08, PL-09, PL-10, PL-11, PL-12, PL-16, PL-25, PL-26; PL-28 only if ruling 10's (b) runs), filed with `tools/t35-file-bugs.py` in #1338's shape with trace, positive, VM line and `Already written:`, passing `box-check`; the numbers posted on #682 in one line before S1; each commit body cites its bug.
16. **The upstream-only items, recorded under D-UI-079** (PL-19, PL-21, PL-22, PL-24, PL-29, PL-30, PL-31, PL-32, PL-33).
    - **The lane proposed:** these were recorded, as `05` gives them.
    - **The drafted reasons, item by item:**
      - **PL-19**, `doOnFinish` synchronous: the shipped `es_input.cfg` has 0 `inputAction` lines (G-01).
      - **PL-21**, the Ctrl chords: a debugging aid outside the lanes.
      - **PL-22**, `Window.cpp:29` and the four detached storage workers: upstream ROCKNIX's layering. Its lifetime half is Medium (a worker still running a merge or a format at exit posts into a destroyed window). It goes to the coordinator as a Backlog with a #585 line, not a stream: its fix needs a join or a shared lifetime across `ApiSystem`, which is es-app's.
      - **PL-24**: TTS is compiled out on the image.
      - **PL-29**, the stick reversal: no pad on the guest (G-10 `CANNOT`). A #585 line.
      - **PL-30**: ruling 17.
      - **PL-31**, the udev unref: the `HAVE_UDEV` branch is not parsed on the host. A #585 line.
      - **PL-32**, a theme's parse result: checking it changes which themes load, a behaviour change on players' themes. A #585 line.
      - **PL-33**: WIN32-only, not on the fork's images.
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** As drafted: PL-19, PL-21, PL-24, PL-29, PL-31, PL-32, PL-33 recorded with their reasons and the #585 lines ruling 19 names; **PL-22 is #1346** (the coordinator's Backlog, with its #585 line).
17. **PL-20 and PL-30 for T3** (`InputManager.cpp:1105-1107`, `GuiInputConfig.cpp:73`, `:273`, `:279`; `InputManager.cpp:993-996`, `:1096` against `InputConfig.cpp:233-247`).
    - **The lane proposed:** *recorded for T3* (`05` PL-20) and *recorded for T3 and the pause* (`05` PL-30).
    - **Drafted answer:** both recorded with their lines.
      - T3 (#650) is accepted, so the templates' half is a Backlog the coordinator files, naming #650.
      - PL-30's menu half (an auto-mapped stick that does not move the menus) cannot be observed on the guest (G-10 `CANNOT`). It is an open item to test with the Backlog, not a stream.
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** Both recorded with their lines; **#1347** (the coordinator's Backlog naming #650) carries PL-20's templates half and PL-30 as an open item to test (G-10 `CANNOT`).
18. **PL-23 for the coordinator's sweep** (`.claude/rules/es-native-ui.md:30` against `Window.cpp:1192`).
    - **Drafted answer:** the coordinator's acceptance commit on `next` runs `tools/archaeology --reversal 'top-right'` and corrects `:30`. The lane records PL-23 as *the coordinator's, at acceptance*.
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** The coordinator's, at acceptance: `tools/archaeology --reversal 'top-right'` and the correction of `es-native-ui.md:30`; the lane records PL-23 as *the coordinator's, at acceptance*.
19. **The #585 lines** (`02` § The #585 lines owed: seven owed lines and one recorded no-line).
    - **Drafted answer:** one line per upstream-carried defect a stream closes, in the lane's shape, never sent (D-WORKFLOW-164/165). The coordinator posts them after acceptance.
      - **Who wrote each line.** Each stream's record runs `git log -S` on the changed line and says whose it is (T34's acceptance errata: PL-01 and PL-03 there turned out upstream's).
      - **The lines expected:** PL-01 (T33's candidate and this slice's), PL-02, PL-03, PL-07, PL-09, PL-10 (the seven in `02`); PL-15, PL-16, PL-25 and PL-26 if upstream's; PL-04 if `:893`, `:1187` and `:1250` are upstream's.
      - **Recorded-only lines:** PL-17, PL-22, PL-29, PL-31 and PL-32.
      - **None:** PL-08 (the fork's `AtomicFile` API), PL-12 (a design choice, not a defect), PL-11 (a rename of the keyboard's constant only), PL-05 (the hold is generic, but the defect needs the fork's fourth-tier page), PL-27 and PL-28 unless `git log -S` shows the logger lines upstream's, and the controllers blob (L-20, contradicted).
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** As drafted: one line per upstream-carried defect a stream closes, each stream's record saying whose line it is by `git log -S`; the expected, recorded-only and none lists stand; never sent (D-WORKFLOW-164/165); the coordinator posts them after acceptance.
20. **A FAIL-at-pin case whose item is recorded, not fixed** (3.5 under ruling 9; any other the rulings leave).
    - **Drafted answer:** as T34's ruling 9, the case is marked `doctest::may_fail` with its PL named.
      - **Why.** The `TOTAL:` line then reads 0 failed truthfully for the fixed cases.
      - **What the hand-back quotes.** The `may_fail` count beside the line (`1 may_fail: PL-18, recorded`). T34's acceptance errata 9 applies: doctest's assertion summary still counts a `may_fail` case's assertions as failed, so the hand-back cites the test-case summary and says so.
      - **The same rule for 3.27.** It is T33's script, outside the `TOTAL:` line, and is quoted FAIL with its reason (ruling 12).
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** As drafted: a FAIL-at-pin case whose item is recorded, not fixed, is marked `doctest::may_fail` with its PL named; the hand-back quotes the `may_fail` count beside the `TOTAL:` line and cites the test-case summary (T34's acceptance erratum 9); 3.27 quoted FAIL with its reason outside the line.
21. **S0: the floor cases no stream holds** (the floor table, `02` § The leads; stage C wrote only 3.1, 3.4, 3.5, 3.10, 3.11, 3.14 (two cases), 3.15 and 3.19 in `window-input-tests`, the sanitizer programs for 3.2, 3.3 and 3.17, and re-ran 3.27).
    - **Drafted answer:** as T34's ruling 10, the cases no stream's file holds are written in a record-only commit before S1, each run against the pin and recorded FAIL or PASS.
      - **The cases.** 3.6 (the single-script pass), 3.7 (`mapInput` and the XML round trip), 3.8 (`buttonLabel`), 3.9 (`AssignActionButtons`), 3.12 (`select` copied to `hotkey`), 3.13 (`doOnFinish` handed every command), 3.20 (three `say(`, as text), 3.22 (`GuiInfoPopup`'s fade), 3.24 (the favourites' truncate-then-write, as text) and 3.25 (a malformed `MameNames` file). 3.26 has no host case and is recorded (`02`: *parse-only*).
      - **Who holds the rest.** 3.16, 3.18, 3.21 and 3.23 belong to S2, S1, S8 and S7. A case that FAILs at the pin on a line no ruling names is a new bug before any fix (D-WORKFLOW-132).
    - **RULING (coordinator, 16:01 UTC 2026-10-31):** As drafted: S0 is a record-only commit before S1 writing the floor cases no stream holds (3.6, 3.7, 3.8, 3.9, 3.12, 3.13, 3.20, 3.22, 3.24, 3.25; 3.26 recorded as having no host case), each run against the pin and recorded FAIL or PASS; 3.16, 3.18, 3.21, 3.23 in S2, S1, S8, S7; a FAIL at the pin on a line no ruling names is a new `bug` before any fix (D-WORKFLOW-132).
## The rules every stream keeps

- **Test first, then the fix; the test's FAIL is recorded before the fix lands** (`engineering-practices.md` § Guards must fail closed).
  - **Where the positive lives.** It is a case in the lane's `window-input-tests` (`tools/t35-window-input-tests.cpp`, built by `tools/t35-build-tests.sh` over the lines `tools/t35-extract.py` lifts verbatim at `git -C <W> rev-parse HEAD`, `t35-build-tests.sh:136`). An extract whose range no longer holds its first and last line is refused, and `window-input-tests` is then not built: `t35-build-tests.sh:136`, *"the extracts were refused; window-input-tests not built"*. The other homes are a sanitizer program beside it (`stage-c/tsan-posts.cpp`, `tsan-watchers.cpp`, `asan-watchers.cpp`, and the lane's new ones in the same shape, each run by `san()` at `:153-166`) or the stand-in.
  - **The command:** `RAPIDJSON_INCLUDE_DIR=/workspace/tmp/m6-t34/rj/rapidjson-1.1.0/include bash docs/audits/2026_10_31-epic-m6-es-core-window-input/tools/t35-build-tests.sh "$W" /workspace/tmp/m6-t35/build/full`. The rapidjson root is `stage-c/build-tests.out:2`'s and the build directory is `:53`'s; the `PUGIXML_INCLUDE_DIR` the stage-C run used is not in the record (§ Figures not found, item 3).
  - **The lines at the pin, quoted in records, never summed in the head.** The script prints `TOTAL: N test cases in B binaries`. At the pin it printed **`TOTAL: 249 test cases in 6 binaries`** (`stage-c/build-tests.out:96`): es-unit-tests 185, es-file-tests 24, es-conf-tests 10, es-file-tests-win32 2 and app-unit-tests 18, each at 0 failed (`:55-59`), and `RUN window-input-tests: rc 1; [doctest] test cases: 10 | 3 passed | 7 failed | 0 skipped [doctest] assertions: 29 | 19 passed | 10 failed` (`:65`). The sanitizer lines are `SAN tsan-posts (-fsanitize=thread): rc 66; WARNING: ThreadSanitizer: data race` and `SAN tsan-watchers (-fsanitize=thread): rc 66; WARNING: ThreadSanitizer: data race` (`:94-95`). 3.2's record is `stage-c/asan-watchers.out` (`rc=0`, `asan-watchers: done, 1 notification(s)`); the script's own `SAN asan-watchers` line at the pin is not in the record (§ Figures not found, item 2).
  - **Where each run goes.** The output at the pin goes into `stage-e/sN-before.txt`, the output after the fix into `stage-e/sN-after.txt`, and the full checks into `stage-e/sN-checks.txt`.
  - **Every stub against the unfixed code first.** A case written for the fixed shape can fail for a reason the pin never had (T21's S11; `engineering-practices.md`), and a FAIL is evidence only when the double reproduces the pin everywhere else. A case that FAILs at the pin on a line no ruling names is a new bug before any fix (D-WORKFLOW-132).
- **D-WORKFLOW-210, as it lands here.** `tools/t35-extract.py` reads the ES tip, so a stream that moves a spec'd line changes its `SPECS` entry in the stream's record commit, naming what it asserted before and after: `queue_pop` `:339-340` and `queue_requeue` `:1163-1164` in S2; `exec_cmd` `:90-113` in S5; `approx` `:939-965` in S6 if its first or last line moves; `kb_pad` `:14` in S8. A new spec is added for each new lift. The generators that read the pin by argument (`python3 -I <gen> <W> 16dbac5211 ...`, `00`'s stage B) stay the pin's. `tools/t35-runs.py`'s stage-C assertions stay, and the stage-E rows are added beside them. **D-WORKFLOW-211:** a fixture that relied on the defect is completed in the stream's commit, its setup line named. The two cases rulings 3 and 6 reshape (3.19 under ruling 3; 3.11 in S6) say so in their records.
- **The stand-in** is `stage-a/syntax-check.sh` with `stage-a/fakes/` (`t35-sdl-more.h` and the T35 sections; the pugixml root). It gives **44 of 44 at rc 0 at the pin** (`stage-a/syntax-check.out`: `t35-syntax-check: 44 file(s) checked, 44 rc 0, 0 not`). It runs over every `.cpp` a stream edits, PASS before the stream's commit. A `.h` is proved through the `.cpp`s that include it, named. `tools/es-syntax-check` exits 2 on this host (`02` § The runs, row 21: `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)`), so each source is `CANNOT` with that line and the stand-in is the check. `HAVE_UDEV`, `_ENABLE_PULSE_`, `_ENABLE_TTS_`, `HAVE_LIBCEC` and the WIN32 branches are not parsed (`02` § The structure).
- **The French.** Every new or changed player sentence ships in English and French in the same commit (D-UI-051): the msgid byte for byte in `locale/lang/fr/LC_MESSAGES/emulationstation2.po`, in that file's own style. The catalog is the one path outside the 96 a stream may touch, and only for that. After the commit, `tools/es-untranslated --es-src <W> --upstream cada856d86` names the sentence in neither list. At the pin it printed `es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without` and `703 fork string(s) in the source, 703 with French, 0 without` (`stage-a/runs.out:188`, `:190`). Under the drafted rulings only S8 (PL-16's fallback `GAMEPAD` / `MANETTE`) adds a msgid; PL-15 (ruling 5) and PL-12 (ruling 4) change no words.
- **Non-ASCII comments.** The check runs over the lines the stream added (`git diff -U0 HEAD -- <file>`, its `+` lines, `grep -nP '[^\x00-\x7F]'`), never over upstream's lines. The six upstream comment lines (`02` § The runs, row 17: `AudioManager.cpp`, `GunManager.cpp`, `InputManager.cpp`) stay as they are, and French lives in the catalog, never in a `.cpp`.
- **One commit per stream** on the ES branch, subject `es-core: ...`, body `Refs #682, #<bug>`, no closing keyword, the files named. The ES `.githooks/pre-push-test` runs before each push, and `tools/register-check` on the distribution side before each record commit. A source a stream changes cites its bug number in a comment, never a register row; rows are cited in commit bodies.
- **Nothing changes outside the 96 and the audit folder** (the catalog as above).
  - **Other lanes' files.** `es-core/src/components/**` is T34's (its comment at `MenuComponent.cpp:9-10` under ruling 3 included). `resources/`, `utils/` (`FileSystemUtil.cpp`, `Platform.cpp`) are T36's. `HttpReq.*`, `Settings.*`, `SystemConf.*` and `AtomicFileUtil.*` are T21's (`AtomicFile::writeText` used, never changed, ruling 7). `CloudText.*` is T18's. `tests/app-unit/fakes/` and everything under `es-app/src` belong to their owners.
  - **What a stream needs from another lane** is written as a patch under `stage-e/`, proven on a scratch copy of the file read by `git show`, and named under merge debt, never made here: S3's page overrides for the fourth-tier pages.
  - **`es-core/CMakeLists.txt`** is touched by no stream. T21's `3ae9610b0` hunk is the integration's (§ 1 (h)). A stream that would need a CMake line posts on #682 first.
  - **The three doubles** (`tests/app-unit/fakes/Window.h`, `Log.h`, `LocaleES.h`, § 1 (i)): no stream changes `Window.h`'s `postToUiThread` or `createAsyncNotificationComponent` signatures, `Log.h`'s `LogLevel` values or `LocaleES.h`'s macros. The hand-back proves that with a `git diff` of the tip against the pin over those three headers.
- **No guest, no image build, no fetch, no keyed call, nothing on a unit.** The host can build neither EmulationStation nor an image.
  - **Every guest half is `fix-walk-pending-image`.** It is the coordinator's, at the integration window, on the image that carries the fix, at 640x480 and 1280x800, in English and French where words show. `tools/frame-diff` runs against the accepted baseline for every page the fork works in. The flow references `es-ui-style-guide.md` § Keep the flow and its visual evidence together asks for land with those frames. A stream's record names the flow step each frame will cover (S1's dialog order, S2's toast order, S3's held screensaver, S8's CLEAR), and the UI change is complete only then.
  - **Housekeeping.** `rm -rf` only as `"${VAR:?}"/...` or a literal path, in its own short command. The scratch is `/workspace/tmp/m6-t35/` after `df -i`. The shared host file `/workspace/tmp/m7-m6-host-coordination.txt` takes a line when each unit build starts and ends.
- **A question for the coordinator is posted on #682**, never only on the session's screen. A turn ends on a post or a commit. If the harness refuses a stream's content, post the stream's number and stop that stream; the coordinator takes it (D-WORKFLOW-212). **The checkpoints S0 to S8 are posted on #682 one line each, as each lands:** the stream, the commit, the before and after lines.
- **Time to play.** Each stream's record says in one clause what it does to the two numbers. The ones that touch the launch path's surface are S2 (the toast queue and the posts), S4 (`WatchersManager::pause` is on the launch path, L-19) and S6 (`writeText`'s fsyncs on a configuration and a hot-plug write).

## S0 -- the floor cases no stream holds (the distribution branch only; ruling 21)

- **Files:** none in the ES tree. The cases go in `tools/t35-window-input-tests.cpp` (or a sibling binary in the same build script), with new `SPECS` for their lifts:
  - 3.6: `Scripting.cpp:182-207`.
  - 3.7: `InputConfig.cpp:186-189`, `:210-283`, `:285-345`.
  - 3.8: `InputConfig.cpp:353-366`.
  - 3.9: `InputConfig.cpp:347-351`, `:403-414`.
  - 3.12: `InputManager.cpp:1004-1111` (`:1101-1108`).
  - 3.13: `InputManager.cpp:1242-1284`.
  - 3.20: `guis/GuiMsgBox.cpp:44`, `:234`, `:240`, as text.
  - 3.22: `guis/GuiInfoPopup.cpp:88-111`.
  - 3.24: `FavoriteMusicManager.cpp:71`, `:115`, as text.
  - 3.25: `MameNames.cpp`, with the pugixml root.
  - Each line range is the brief's floor table's, `02` § The leads.
- **Positives before:** each run against the pin, and its FAIL or PASS recorded as written. The brief expects PASS for 3.6 to 3.9, 3.12, 3.13 and 3.22, and *recorded* for 3.20, 3.24 and 3.25 (`02` § The leads, the floor table). 3.26 is recorded as *no host case* (`ThemeData.cpp`: parse-only).
- **The record:** `stage-e/s0-floor.txt` with the script's `TOTAL:` line, and `02` § The leads' floor rows moved from `design` to `tool-run`.
- **Commit:** `docs: T35 stage E S0: the floor cases no stream holds, each run at the pin (Refs #682)`.

## S1 -- PL-15 (#1342): back on the drive dialogs (High)

- **Ruling 5.** Upstream ROCKNIX's dialog (`processStorageRequest`, D-UI-079's upstream surface). Removing its destructive default is rule 6's contained fix, and only the order changes.
- **Files:**
  - **Changed:** `Window.cpp`: GAME DRIVE DETECTED with an id `:1568-1578` (the labels `:1569`, `:1570`, `:1577`) and without one `:1583-1586`; NEW DRIVE DETECTED with an id `:1630-1640` and without one `:1645-1648`; the confirmation `:1622-1626` *(pin read)*.
  - **Read, not changed:** `guis/GuiMsgBox.cpp:116-134` (the accelerator: the only button, else the first named `OK` or `NO` at `:125`, else the last at `:132-133`) and `:246-264` (`:257`, an unconfigured pad's any button).
- **Positives before:**
  - **Owed: the drive dialogs' case** (#1342's first checkbox). A new `SPECS` lift of `GuiMsgBox.cpp:116-134` with a `ButtonComponent` double, and the four calls' label lists lifted as text from `Window.cpp`. It FAILs at the pin for GAME DRIVE DETECTED with an id (back binds YES, MERGE DRIVE) and for both NEW DRIVE DETECTED forms (back binds YES, FORMAT & MERGE), and PASSes without an id (back binds NO by name).
  - **3.18** (the accelerator's three branches, as text) as floor.
  - **The intent read.** The lane runs `git log -S'NO, IGNORE THIS TIME' -- es-core/src/Window.cpp` and records whose the order is, first.
- **The fix.** Each call lists YES first and the choice that changes nothing on this or a future boot last:
  - YES, MERGE DRIVE / NO, IGNORE FOREVER / NO, IGNORE THIS TIME;
  - YES, FORMAT & MERGE / NO, IGNORE FOREVER / NO, IGNORE THIS TIME;
  - YES, FORMAT & MERGE / NO, IGNORE.
  - Each lambda moves with its label, and no word changes. The fall-through (`GuiMsgBox.cpp:132-133`), `:257` and ARE YOU SURE?'s NO / YES are untouched (ruling 5).
  - **The lane's count.** The `GuiMsgBox` calls in the 96 with three buttons and none named `OK` or `NO` (expected: the two with-id calls). Any in es-app is named for the coordinator.
- **Positives after:**
  - The drive dialogs' case PASS: back binds NO, IGNORE THIS TIME (with an id) and NO, IGNORE (without one), and NO under GAME DRIVE DETECTED without an id.
  - 3.18 recorded; `Window.cpp` through the stand-in.
  - `t35-surfaces.py` and `t35-leads.py` are untouched (they read the pin).
  - **The guest half,** `fix-walk-pending-image` (#1342's third checkbox). `POST /storage/event` on the guest's 127.0.0.1:1234 with a `REQUEST_MERGE` line naming a disposable mount and an id (`es-app/src/services/HttpServerThread.cpp:577-597`, #1342's VM line) raises GAME DRIVE DETECTED. After `z`, a frame shows the dialog closed with no `Merge requested` toast, and the journal shows no merge request. The frames are labelled by side, at 640x480 and 1280x800, in English and French (`OUI, FUSIONNER LES DISQUES` / `NON, IGNORER À JAMAIS` / `NON, IGNORER CETTE FOIS`, `02` § The words).
- **`Already written:`** #1342's: *"a merge already applied by a back press is persisted by `mergeDrive` for future boots and is indistinguishable from one chosen on purpose -- nothing migrated: the fix changes the dialog, not what an earlier press wrote, and a merged drive stays merged until the player changes it."*
- **Time to play:** off the launch path (a drive event's dialog).
- **Commit:** `es-core: the drive dialogs list YES first and the choice that changes nothing last, so back never lands on a merge or a format (Refs #682, #1342)`. A #585 line if `git log -S` shows the order upstream's (ruling 19).

## S2 -- PL-02 (#1338), PL-07 (#1341), PL-25, PL-26: the window's queue, posts and help bar (Medium)

- **Rulings 1, 2 and 15.** D-UI-093's decided order, rule 6 for upstream's pop and lock, and D-UI-034 for the help bar. Applied over S1 in `Window.cpp`, a separate region.
- **Files** (`Window.cpp`):
  - `processNotificationMessages` (`:324-351`: the hold `:336-337`, **the pop `:339-340`**, the comment `:334-335`).
  - `createAsyncNotificationComponent`'s re-queue (`:1159-1166`: the comment `:1159-1160`, the loop `:1163-1164`, the duration `:1164`).
  - `unregisterPostedFunctions` (`:1262-1274`) against `postToUiThread` (`:1276-1290`, the lock `:1278`, the wake `:1284-1289`) and `processPostedFunctions` (`:1292-1307`, the lock `:1296`).
  - The idle reads (`:540`, `:778`, `:1111`).
  - `setHelpPrompts`' dpad merge (`:1031-1041`; the compares `:1032-1033`).
- **Positives before:**
  - **3.14** FAIL at the pin: `tools/t35-window-input-tests.cpp:65: ERROR: CHECK( w.next().first == "A first" ) is NOT correct!` / `values: CHECK( B second == A first )` (`stage-c/build-tests.out:66-70`).
  - **3.17**: `SAN tsan-posts (-fsanitize=thread): rc 66; WARNING: ThreadSanitizer: data race` (`:94`).
  - **Written first:**
    - **The interruption case** (#1338's second checkbox; the seat's counterexample in `05` PL-02): A on screen, B queued, a card created. Once the card leaves, A shows before B. It FAILs at the pin, where `:1163-1164` appends A behind B.
    - **3.16** (PL-25) over a new `SPECS` lift of `:1005-1078`, with both of the lane's cases: two complementary halves merge into `up/down/left/right`, and an unrelated prompt sharing the action text is kept, not replaced. It FAILs at the pin (`05` PL-25).
    - **PL-26's** `tsan-posts` extended: `postToUiThread`'s writes of `mSleeping` and `mTimeSinceLastInput` against `update`'s reads. It reports the race at the pin, or the record says it could not be constructed.
  - **The intent read first.** `git log -S'pop_back' -- es-core/src/Window.cpp`: the base `bccd715707` pops from the back at its `:322-323` (`02` § The surfaces; the brief § 4 Q1).
- **The fix:**
  - **PL-02:** `:339-340` take the front (`front()` and `erase(begin())`). The re-queue (`:1163-1164`) inserts the popups' words at the front of the queue in their on-screen order, so a toast a card took off the screen shows before anything queued after it. The comment `:1159-1160` is rewritten to say so, and `:1164`'s duration stays (ruling 2).
  - **PL-07:** `unregisterPostedFunctions` takes `mNotificationMessagesLock`. The lane first lists its callers and confirms none holds that lock at the call; that list is not in the record (§ Figures not found, item 8).
  - **PL-25:** `:1032-1033` compare `==` for the complementary half.
  - **PL-26:** `postToUiThread` sets a wake flag under the lock, and `processPostedFunctions` (the interface thread) applies `mSleeping = false`, `mTimeSinceLastInput = 0` and `PowerSaver::pushRefreshEvent()` when it is set.
- **Positives after:**
  - 3.14 both halves PASS; the interruption case PASS; 3.16 PASS.
  - `SAN tsan-posts (-fsanitize=thread): rc 0; no sanitizer report`, the PL-26 extension included (#1341's checkbox).
  - The `queue_pop` and `queue_requeue` specs updated, named (D-WORKFLOW-210); `Window.cpp` through the stand-in.
  - **The guest half,** `fix-walk-pending-image` (#1338's third checkbox). `POST /notify` twice on the guest's 127.0.0.1:1234 while a card is up (G-03's shape), then a frame after the card leaves shows the two toasts in the order they were posted. Plus a list's help bar at 640x480 in French with the dpad prompt merged (PL-25).
- **`Already written:`** #1338's and #1341's: nothing inherited. The queue and the posted functions live in memory for the session. PL-25's and PL-26's are the same, a prompt and an idle counter.
- **Time to play:** the toast queue's front pop is an erase over a few entries per toast, and the unregister takes one lock per page close. The wake moves to the drain on the next update, so the launch path's length does not change.
- **Commit:** `es-core: the toast queue drains in the order things happened and a returned toast keeps its place, the posted functions' unregister takes their lock, a worker's wake is applied on the interface thread, and the help bar merges only the dpad's two halves (Refs #682, #1338, #1341, #<PL-25>, #<PL-26>)`. #585 lines for the four if `git log -S` shows them upstream's (`02` lists PL-02 and PL-07).

## S3 -- PL-05 (#1305's window half): the screensaver held by a page that owns the screen (Medium)

- **Ruling 12.** Applied over S1 and S2 in `Window.cpp`.
- **Files:**
  - `Window.cpp`: the start in `render()` (`:777-779`); `startScreenSaver` (`:1091-1105`: the guards `:1093`, the pages told `:1099-1100`); `cancelScreenSaver` (`:1107-1138`, `resetCounts` `:1117`, read only).
  - `GuiComponent.h` (and `GuiComponent.cpp` if the default lives there): the new virtual beside `onScreenSaverActivate`'s declaration. The lane names the line, because the record does not carry it (§ Figures not found, item 9).
  - **Read, not changed:** T33's `SystemScreenSaver.cpp:342-358` and T2's `SystemData.cpp:459-473` (#1305's other halves).
- **Positives before:**
  - **3.27**, T33's harness unchanged: `SUMMARY: AddressSanitizer: heap-use-after-free a.cpp:14 in FileData::getImagePath` (`stage-c/pl25-screensaver.out`, #1305's trace).
  - **Written first: the window's case.** A new `SPECS` lift of `:777-779` and `:1091-1105` into a window double with a screensaver double and a top page that claims the hold. At the pin, with idle time past the setting, the screensaver starts: FAIL. A second page that does not claim it lets it start, which PASSes at the pin and after, as the guard that upstream pages keep their behaviour.
- **The fix.**
  - `GuiComponent` gains a virtual that allows the screensaver by default.
  - `startScreenSaver` (or `:778` before the call) asks the top page and returns without starting while it holds. `mTimeSinceLastInput` keeps running, so the screensaver starts at the next frame after the page lets go.
  - **The fourth-tier pages' overrides** (`GuiCloudTransfer`, T18's #665; the others the lane names by `git grep` and the slices' globs) are `stage-e/s3-pages.patch`. Each is proven on a scratch copy read by `git show` at its owner's ES tip and named under merge debt.
- **Positives after:** the window's case PASS, and the guard PASS. 3.27 still FAILs, as it should until T33's or T2's half lands, and the record says so (ruling 20). `Window.cpp` and `GuiComponent.cpp` go through the stand-in; `GuiComponent.h`'s includers in the 96 are named.
- **The guest half,** `fix-walk-pending-image`, G-09's sequence on the integration image with the page patch applied: SCREENSAVER AFTER at its minimum, BACK UP TO THE CLOUD's page left running, and a frame after the timeout showing the page, not the screensaver. Then a frame after the job ends and the timeout passes showing the screensaver.
- **`Already written:`** #1305's trace: nothing inherited. The screensaver's state and its list live in memory, and the window writes no file for them.
- **Time to play:** one virtual call per frame while idle past the setting. It is off the launch path.
- **Commit:** `es-core: a page that owns the screen for a job can hold the screensaver off; every other page keeps upstream's start (Refs #682, #1305)`. No #585 line (ruling 19).

## S4 -- PL-01 (#1283's es-core half): the watchers' lock (Medium)

- **Ruling 13.** Rule 6, in T33's named shape (#1283).
- **Files:** `watchers/WatchersManager.cpp`: `run()` `:159-203` (the lock `:181`, `check()` `:196`, the notify `:197` -> `:128`); `RegisterComponent` `:66`, `UnregisterComponent` `:78` (the delete `:85-86`), `ResetComponent` `:92-104`, the destructor `:143`, `mRunning` written at `:151` and read at `:161`, `:172`, `:187`. Also `watchers/WatchersManager.h` (`GetComponent` `:35`, `mRunning`/`mPaused` `:85-86`, the locks `:77`, `:80`, `:83-84`).
- **Positives before:**
  - **3.1** FAIL at the pin: `MESSAGE: ResetComponent returned after 1496 ms` and `ERROR: CHECK( ms < 300 ) is NOT correct!` / `values: CHECK( 1496 <  300 )` (`stage-c/build-tests.out:91-93`). The record's prose says 1,491 ms (§ Figures not found, item 1).
  - **3.3:** `SAN tsan-watchers (-fsanitize=thread): rc 66; WARNING: ThreadSanitizer: data race` (`:95`).
  - **3.2:** clean at the pin (`stage-c/asan-watchers.out`), the guard.
  - **Written first:** 3.2 extended. Unregister a watcher while its probe runs, then delete the `IWatcher` the moment `UnregisterComponent` returns. This is clean at the pin, where the lock spans the probe, and it is the keep-alive's guard. Plus a case that a second watcher's `ResetComponent` returns at once while the first's probe runs, which FAILs at the pin as 3.1 does.
- **The fix.**
  - The due records are snapshotted under `mWatchersLock`, and each `check()` runs outside it.
  - A probe's record carries an in-flight mark. `UnregisterComponent` of that watcher waits on a condition variable for its own probe only, and every other entry point returns at once.
  - The next check time is written back under the lock. The notification stays under `mNotificationLock`, and the order `mWatchersLock` -> `mNotificationLock` is never reversed.
  - `mRunning` becomes `std::atomic<bool>`.
- **Positives after:**
  - 3.1 PASS, its figure quoted from the run.
  - `SAN tsan-watchers (-fsanitize=thread): rc 0; no sanitizer report`; `SAN asan-watchers (-fsanitize=address): rc 0; no sanitizer report`, the extension included; the second-watcher case PASS.
  - Both files through the stand-in.
  - **#1283's checkbox for this slice's record** ticks from `stage-e/s4-checks.txt` with the fixed file's lines cited (the brief § 4 Q3). The guest half: none (#1283's trace: *"host-only"*).
- **`Already written:`** #1283's trace: nothing inherited. The watcher list and its timers live in memory.
- **Time to play:** the interface thread's wait for a probe goes; 3.1 measured it at the bound of the probe in flight. `WatchersManager::pause` (`:29-53`, on the launch path, L-19) is untouched.
- **Commit:** `es-core: the watchers probe outside the list lock with each record kept alive through its probe, and the running flag is atomic (Refs #682, #1283)`. The #585 line is T33's candidate and this slice's (`02` § The #585 lines owed, first line).

## S5 -- PL-03 (#1339): the script runner's quoting (Medium)

- Rule 6. PL-17 and PL-18 are recorded (rulings 8 and 9).
- **Files:** `Scripting.cpp` `executeScript`, the non-WIN32 branch `:88-113`, `:137-148`: the script path quoted on a space `:92-93`, the event name bare `:95-96`, `:104`'s second `startsWith`, the strip `:107`, the double quotes `:109-112`. Read, not changed: `utils/Platform.cpp:162-181` (T36's).
- **Positives before:**
  - **3.4** FAIL at the pin: `:149: ERROR: CHECK( c.find("'/storage/roms/nes/a$(id)b.zip'") != std::string::npos )` and `:151: ERROR: CHECK( t.find("'x`id`y.zip'") != std::string::npos )` (`stage-c/build-tests.out:76-80`).
  - **Written first:** `:104`'s case (#1339's second checkbox): an argument that starts with a double quote keeps its last character. It FAILs at the pin.
  - **3.4's recorded shapes** (`tools/t35-window-input-tests.cpp:154-158`: a space in double quotes, a `"` stripped) change with the fix. Under D-WORKFLOW-211 the record names the new expected strings (each argument single-quoted, `"` kept) in the same commit.
- **The fix.**
  - **Quoting.** The script path, the event name and every argument are single-quoted, an embedded `'` written `'\''`. The strip at `:107` goes, so a `"` reaches the hook intact, and `:104`'s second test is `endsWith`.
  - **A helper.** The lane checks `git grep -n -E 'shellQuote|quoteArg' 16dbac5211 -- es-core/src` first and uses an existing es-core helper if there is one. Otherwise it writes a local one in `Scripting.cpp` (es-app's `FileData.cpp:1148-1151` form, which es-core cannot include).
  - **Out of scope.** An argv executor is #1192's second half (`ProcessStartInfo`, T36's), not this stream.
  - **WIN32** (`:115-136`) gets the same quoting only if its `ProcessStartInfo` reads it the same way; the record says which.
- **Positives after:** 3.4 PASS, `:104`'s case PASS, the `exec_cmd` spec updated, `Scripting.cpp` through the stand-in.
  - **The guest half,** `fix-walk-pending-image` (#1339's third checkbox): a hook in `/storage/.config/emulationstation/scripts/game-start/` that writes its argv to a file records each argument byte for byte, for a game whose name holds shell metacharacters. The file's contents are quoted in the issue. The hook comes out after, and none is shipped.
- **`Already written:`** #1339's: *"nothing inherited -- the command line is built per event and kept nowhere; the hooks' own logs (`es_script_stdout.log`, `es_script_stderr.log`) are rewritten by the next run, and the fix reads nothing an earlier build wrote."*
- **Time to play:** `fireEvent` runs on the launch events. The quoting is a string pass per argument, and the six directory scans are unchanged (L-19).
- **Commit:** `es-core: an event script's path, name and arguments reach the shell single-quoted, so a file name stays text (Refs #682, #1339)`. A #585 line (`02` § The #585 lines owed, second line).

## S6 -- PL-04 (#1340), PL-08, PL-09, PL-10: the input manager (Low)

- **Rulings 7 and 15.** Rule 6 for upstream's lines, D-CLOUD-078 for the write.
- **Files:** `InputManager.cpp`:
  - the cached reads `:893`, `:1187`, `:1250`; the writes `:1225`, `:1232` (`writeDeviceConfig` `:1179-1240`; the hot-plug write `:605`);
  - the approximate-match logs `:946`, `:960`;
  - F4 `:792-800` (`:795`).
  - **The fifth cached read** (`02` § The input) is `guis/GuiDetectDevice.cpp:127`, the first-run skip. `05` PL-04's fix names three lines; the lane either passes `false` there too or records why not.
  - **Read, not changed:** `utils/FileSystemUtil.cpp:296`, `:323`, `:161-162`, `:1122-1147` (T36's) and `utils/AtomicFileUtil.h:42` (T21's).
- **Positives before:**
  - **3.11** FAIL at the pin: `:209: ERROR: CHECK( Utils::FileSystem::exists(p) ) is NOT correct!` / `values: CHECK( false )` (`stage-c/build-tests.out:87-89`). As written it asserts the cache's own answer (`tools/t35-window-input-tests.cpp:205-211`), which S6 does not change. **It is reshaped first to read through `writeDeviceConfig`'s lifted `:1187`** (#1340's first checkbox: *"the read `writeDeviceConfig` makes at `:1187` sees the file"*), with the cache extract kept as the double, and seen to FAIL at the pin.
  - **3.10** FAIL at the pin: `:112` and `:117` `ERROR: CHECK( im::logged[0].find(...) != std::string::npos )` (`:71-75`).
  - **Written first:**
    - **PL-08's case.** The lifted `:1220-1232` with `AtomicFileUtil.cpp` linked. Its bytes equal `save_file`'s for one document. A reader that polls during repeated writes of a large document sees only whole documents. At the pin, where the write truncates in place, the reader sees a short file: FAIL. If no bound makes that FAIL at the pin, the record says so and the proof falls to a seam double counting `writeText` calls.
    - **PL-10's case.** The lifted `:792-800` with `SDL_Event`/`SDL_PushEvent` doubles under `-fsanitize=address`. LeakSanitizer reports the event at the pin.
- **The fix.**
  - **PL-04:** `exists(path, false)` at `:893`, `:1187` and `:1250`, and at `GuiDetectDevice.cpp:127` if the lane rules it.
  - **PL-08:** `:1225` and `:1232` become pugixml's `save` to a string, with `save_file`'s default indent and flags, then `AtomicFile::writeText(path, text)`. A `false` return is logged. The favourites file is recorded (ruling 7).
  - **PL-09:** `:946` and `:960` log `item`'s attributes.
  - **PL-10:** a stack `SDL_Event` at `:795`.
- **Positives after:**
  - 3.11 (reshaped) PASS and 3.10 PASS.
  - PL-08's case PASS: the bytes equal and whole files only.
  - PL-10's sanitizer program `rc 0; no sanitizer report`.
  - The `approx` spec updated if its first or last line moved; `InputManager.cpp` (and `GuiDetectDevice.cpp`) through the stand-in.
  - **The guest half,** `fix-walk-pending-image` (#1340's second checkbox). `rm /storage/.config/emulationstation/es_input.cfg`, restart the interface, and configure through CONTROLLER MAPPING with the monitor hold (G-08: `sendkey x 1000`). The file the next `exists` reads and `loadInputConfig` loads is quoted with its `<inputConfig` count and the journal line. G-10 stays `CANNOT` for a pad and a hot-plug.
- **`Already written:`**
  - **`es_input.cfg`:** #1340's: *"a device whose user file was absent at startup and had two inputs configured in one session may hold an `es_input.cfg` with only the last one -- read both: the file's format is unchanged, so the fixed reads load what is there; the dropped entry is not on the device to recover, and the player configures that input again."* PL-08 adds: *a cut `es_input.cfg` already on a device reads as a parse error at load and is rewritten at the next save with what pugixml salvaged plus this device* (`02` § The input, `:223`; `05` PL-08). The fix writes the same bytes whole and does not repair it, so the answer is read both.
  - **`es_last_input.cfg`:** *"nothing in es-core or es-app reads it back"* (`02` § The input, `:224`), so nothing is inherited to read.
  - **The favourites file:** not changed by S6.
  - **The log:** S7's.
- **Time to play:** `exists(..., false)` is one `stat` at each of three configuration-time reads, none on the launch path. `writeText` adds two fsyncs per save on the interface thread, at a configuration's OK and on an SDL-mapped device's hot-plug write. Both are priced on the integration image.
- **Commit:** `es-core: the input file is read uncached after the interface writes it, written whole through AtomicFile, the approximate match names its device, and F4's quit event lives on the stack (Refs #682, #1340, #<PL-08>, #<PL-09>, #<PL-10>)`. #585 lines for PL-09 and PL-10 (`02` § The #585 lines owed), and for PL-04 if `git log -S` shows its lines upstream's.

## S7 -- PL-27 (#1343), PL-28: the logger (Medium)

- **Ruling 10.** The fork's logger (#178).
- **Files:** `Log.cpp`: `close()` `:63-82` (the drain `:79`); `emergencyFlush` `:84-99` (the handler's own flush `:98`); `enqueue` `:101-108`; `workerLoop` `:117-154` (the swap `:130`, the per-batch flush `:147`, the break `:152`); `drainBuffer` `:156-162`; `mShutdown` `:189`; `crashHandler` `:237-242`; the registrations `:282-285` *(pin read for `:84-99`, `:237-242`, `:282-285`)*.
- **Positives before** (all owed; #1343: *"No case has run it yet"*):
  - **3.23's binary** (*"the natural first binary"*, the brief's floor table), a `Log.cpp` build with the `SDL_timer.h` fake and test-defined `Settings`/`Paths` as `SystemConfTests.cpp` does. Its PL-27 case enqueues lines while `close()` runs and finds every one in the file afterwards; it FAILs at the pin if the lines enqueued after the worker's last swap are lost. The stub against the pin first: if timing cannot make it FAIL within a bound, the record says so.
  - **A ThreadSanitizer program** over `close()` and the worker: the race on `mShutdown` at the pin.
  - **PL-28's ThreadSanitizer program** over `emergencyFlush` against the worker: the race on `mFile` at the pin, or ruling 10 falls to (c).
  - A new binary changes the script's binary count. The `TOTAL:` line says so; it is never summed in the head.
- **The fix.**
  - **PL-27:** `close()` drains the write buffer after the join, swapping first as the worker does. `mShutdown` is read under the mutex inside the worker's wait (`:123-128`) and copied out before the drain, or made atomic.
  - **PL-28:** `:98` goes. The handler's limits (`notify_one` and `sleep_for` are not async-signal-safe; the wait is bounded at 200 x 50 us) are written beside `crashHandler`.
- **Positives after:**
  - The PL-27 case PASS; `SAN ... rc 0; no sanitizer report` for both programs; 3.23 recorded.
  - `Log.cpp` through the stand-in.
  - The guest half: none (#1343's VM line: *"host-only"*).
- **`Already written:`** #1343's: *"the log (`es_log.txt`) is rewritten at each start and nothing reads it back; what earlier exits lost was never written -- nothing inherited to read or migrate."* `Log::init` also rotates up to four archives (`:268-279` *(pin read)*), and nothing reads them back either.
- **Time to play:** `close()` runs at exit and drains at most one more buffer; the handler runs at a crash. Neither is on the launch path.
- **Commit:** `es-core: the logger drains its last batch after the join and reads its stop flag under the lock, and the crash handler leaves the stream to the worker (Refs #682, #1343, #<PL-28>)`. A #585 line only if `git log -S` shows the lines upstream's.

## S8 -- PL-11, PL-12, PL-16: the keyboard, the text popup and the configuration page (Low)

- **Rulings 3, 4 and 14.** D-UI-051 for PL-16's French.
- **Files:**
  - `guis/GuiTextEditPopupKeyboard.cpp`: the define `:14` and its use `:220`; `x` `:392-397`; the CLEAR key `:491-496`.
  - `guis/GuiTextEditPopup.cpp`: the CLEAR button `:34`.
  - `guis/GuiInputConfig.cpp`: the subtitle `:128-136` (`:134`).
  - The French catalog: `GAMEPAD` / `MANETTE` only.
  - **Read, not changed:** T34's `components/MenuComponent.cpp:14` and its comment `:9-10` at `52f0ff512` (merge debt, ruling 3).
- **Positives before:**
  - **3.19** FAIL at the pin: `ERROR: CHECK( kbPad() == doctest::Approx(menuPad()) ) is NOT correct!` / `values: CHECK( 3.33333 == Approx( 14.08 ) )` (`stage-c/build-tests.out:84-86`). Under ruling 3 it is re-written first to assert one name in one file, and seen to FAIL at the pin.
  - **Written first:**
    - **PL-12's case.** The lifted `:34`, `:392-397` and `:491-496` in a popup double. CLEAR and `x` empty the text and leave the popup open with `okCallback` not called. It FAILs at the pin, where `okCallback("")` is called.
    - **3.21** (the subtitle, lifted as text). It asserts the subtitle's argument is the device's name, and FAILs at the pin (`getDeviceId() + 1`).
- **The fix.**
  - **PL-11:** `:14` and `:220` use the keyboard's own name, with the value kept.
  - **PL-12:** CLEAR and `x` empty the field (the text component's value set to `""`) and keep the popup open. OK commits and CANCEL or back discards. The help bar's labels stay.
  - **PL-16:** `:134` takes `target->getDeviceName()`, falling back to `_("GAMEPAD")` when the name is empty, with `MANETTE` in the catalog in the same commit.
- **Positives after:**
  - 3.19 (re-written), PL-12's case and 3.21 PASS.
  - `tools/es-untranslated`'s two lines with `0 without`.
  - `tools/es-menu-map-check --es-src <W> --ref <tip>` printing `0 missing` (no row added; the slice's six dialogs contribute 0 titles, `02` § The structure).
  - The three `.cpp` through the stand-in; the `kb_pad` spec updated.
  - **The guest half,** `fix-walk-pending-image`:
    - G-06's walk to the cloud folder editor: the keyboard's CLEAR key pressed, then a frame shows the field empty and the keyboard still open; OK then commits. At 640x480 and 1280x800, in English and French (`EFFACER`).
    - The key gap measured from the frame.
    - The detect page's hold (G-08) to CONFIGURING with a frame of the subtitle in English and French.
- **`Already written:`** PL-11's and PL-16's: nothing inherited (a padding and a subtitle are drawn, not stored). PL-12's: a value an earlier CLEAR committed (an emptied folder path, hostname or Wi-Fi key) is in the settings as the player left it. The fix changes what the next CLEAR does, not what one wrote, so an empty value reads as it does today: read both.
- **Time to play:** none on the launch path.
- **Commit:** `es-core: the keyboard's key padding has its own name, CLEAR empties the field without committing it, and the configuration page names the pad it configures (Refs #682, #<PL-11>, #<PL-12>, #<PL-16>)`. A #585 line for PL-16 if `:134` is upstream's.

## Recorded, no stream

These are ruled above and listed here so the Phase 7 gate has every row:

- **PL-06:** deferred to #1310 at the integration (ruling 6).
- **PL-13:** whole, by design (ruling 2); its case stays as the contract.
- **PL-14:** stands (ruling 1).
- **PL-17:** recorded, with a #585 line (ruling 8).
- **PL-18:** recorded, with 3.5 `may_fail` (rulings 9 and 20).
- **PL-19, PL-21, PL-22, PL-24, PL-29, PL-31, PL-32, PL-33:** recorded under D-UI-079 (ruling 16). PL-22's lifetime half goes to a Backlog the coordinator files.
- **PL-20, PL-30:** for T3 (#650), a Backlog (ruling 17).
- **PL-23:** the coordinator's sweep (ruling 18).
- **PL-34:** the card tier's design; the 100 s startup card is named for the cloud lane (ruling 11).
- **The favourites file's rewrite** (`FavoriteMusicManager.cpp:115`): recorded (ruling 7).
- **ARE YOU SURE? NO / YES** (`Window.cpp:1622-1626`): recorded (ruling 5).
- **The take-up rows the pause leaves as read** (`04` § The take-up table, rows 706 to 737) stay as the lane disposed them. Row 711, the masking mode, is #1192's.
- **Withdrawn:** none.

## The order

- **S0:** the distribution branch only, the floor.
- **S1:** `Window.cpp:1566-1650`, the drive dialogs; High first.
- **S2:** `Window.cpp:324-351`, `:1031-1041`, `:1159-1166`, `:1262-1307`.
- **S3:** `Window.cpp:777-779`, `:1091-1105`; `GuiComponent.h`/`.cpp`; `stage-e/s3-pages.patch`.
- **S4:** `watchers/WatchersManager.cpp`/`.h`.
- **S5:** `Scripting.cpp`.
- **S6:** `InputManager.cpp`, `guis/GuiDetectDevice.cpp:127`.
- **S7:** `Log.cpp`.
- **S8:** `guis/GuiTextEditPopupKeyboard.cpp`, `guis/GuiTextEditPopup.cpp`, `guis/GuiInputConfig.cpp`, the catalog.

`Window.cpp` is the one file touched by more than one stream: S1, S2 and S3, in that order and in separate regions, as serial commits with no rebase across streams. Every stream's unit cases are written and seen to FAIL at the pin before its fix (S0's are run at the pin and recorded either way). The checkpoint lines on #682 keep the stream numbers.

## The record

As T34's (`t34-streams.md` § The record):

- **`02` § The streams:** one row per stream. Each row has the positive before, the ES commit, the positive after, the `Already written:` answer, `proved: fix-unit-test`, the guest half `fix-walk-pending-image`, and the patches and the collisions named.
- **`02` § Positives:** filled from the `sN-before`/`sN-after` lines. Every count is a tool's line.
- **`05`'s gate table and `punch_index`:** moved together at Phase 7 by `tools/t35-05.py`, which assigns the items as follows.
  - **Fixed, by stream:** PL-15 by S1; PL-02, PL-07, PL-25, PL-26 by S2; PL-05's window half by S3; PL-01 by S4; PL-03 by S5; PL-04, PL-08, PL-09, PL-10 by S6; PL-27, PL-28 by S7; PL-11, PL-12, PL-16 by S8.
  - **Deferred:** PL-06 to #1310.
  - **Recorded:** the rest, as above, with their reasons and #585 lines.
- **The tools.** The extractor's specs, before and after, under D-WORKFLOW-210. The #585 lines in `02` § The #585 lines owed, with each one's `git log -S` provenance.
- **`00`.** Its stage-E entries name the build script's command and each sanitizer program's, and the host-file START/END lines for each compile.
- **The checks.**
  - `tools/lint-audit-artifacts docs/audits/2026_10_31-epic-m6-es-core-window-input/` PASS on its default `resolution` phase, and with `--issue 1337`.
  - `tools/box-check --issue 1337` 0 fail, and the same on each bug filed under ruling 15.
  - `tools/register-check` before each record commit.

## The hand-back

After stage E's record, as the brief's § 10 and T34's:

- **One hand-back comment on #682** names **both tips**: the distribution's, and the ES tip of `feature/m6-es-core-window-input-682` on `origin`. The lane writes `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` into #682's body.
- **The `fixed-at-es` header** goes in `05` and in the body of each bug the streams fixed: #1338, #1339, #1340, #1341, #1342, #1343 and the bugs ruling 15 files. A comment carrying it goes on #1283 and #1305, which are T33's bugs. The bugs stay open until the pin moves on `next`.
- **The lines, quoted from the script's own output:**
  - The `TOTAL:` line, with 0 failed in every binary's test-case summary and `window-input-tests` among the binaries.
  - The `may_fail` count beside it (`1 may_fail: PL-18, recorded` under rulings 9 and 20), with the note that doctest's assertion summary counts those assertions as failed (T34's acceptance errata 9).
  - Every `SAN` line at `rc 0; no sanitizer report`: `tsan-posts`, `tsan-watchers`, `asan-watchers` and the lane's new ones (S6's leak program, S7's two).
  - The seven candidates' FAIL lines at the pin beside their PASS lines: 3.1, 3.4, 3.5, 3.10, 3.11, 3.14, 3.19. 3.5's is `may_fail`; 3.11 and 3.19 are reshaped, and each record says so.
  - 3.27's FAIL-at-pin line and its state at the tip (FAIL until T33's or T2's half lands, ruling 12).
- **The stand-in:** one line per edited `.cpp`, and `t35-syntax-check: 44 file(s) checked, 44 rc 0, 0 not` re-run at the tip. Each source's `es-syntax-check` is `CANNOT` with the host's line.
- **The checkers:**
  - `tools/es-untranslated`'s two lines with `0 without`.
  - `tools/es-menu-map-check --es-src <W> --ref <tip>` with its full line (`0 missing`; no row added).
  - **The five on the distribution branch**, each with its own `rc=` line: `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test`.
  - **The ES fork's `.githooks/pre-push-test`** at the tip.
- **The collisions:**
  - **The three `tests/app-unit/fakes/` doubles** (§ 1 (i)): a `git diff 16dbac5211 <tip> -- es-core/src/Window.h es-core/src/Log.h es-core/src/LocaleES.h` showing neither signature nor `LogLevel` nor a macro changed. S3 changes `GuiComponent.h`, which no double stands in for; its includers are named.
  - **T21's `es-core/CMakeLists.txt` hunk** (`3ae9610b0`, five added lines): no stream touches the file, so the hunk is the integration's.
  - **T34's ES tip**, read a third time (`02` § The merge debt: *"the hand-back reads it a third time"*): its delta inside the 96, which is empty at both earlier reads. Then `patch --dry-run` of `s2-window.patch` and of `s3-msgbox.patch` over T35's ES tip, each hunk's result quoted. `s2-window.patch`'s hunks at `@@ -1149`, `@@ -1165` and `@@ -1245` sit beside S2's re-queue edit (ruling 6). T34's `MenuComponent.cpp:9-10` sentence about the keyboard's second copy is named under ruling 3.
- **The merge debt, by file:**
  - `Window.h`/`Window.cpp`: T34's `s2-window.patch` (#1310, the card handle; ruling 6).
  - `guis/GuiMsgBox.cpp`: T34's `s3-msgbox.patch`, ordered after #1315. T35 does not touch `GuiMsgBox.cpp` under ruling 5, so the patch should apply clean; the dry-run says.
  - `stage-e/s3-pages.patch`: the fourth-tier pages' hold, for T18 and the other owners S3 names.
  - `s2-holders.patch`'s hunk 3 against T2's `ProxyCards.cpp`, T34's, named again.
  - T34's `components/MenuComponent.cpp:9-10` comment (ruling 3).
  - `.claude/rules/es-native-ui.md:30`: the coordinator's sweep (ruling 18).
  - `es-code-traps.md` § Three things a font is not: a sentence that the input file and an uncached `exists(p, false)` rewriting the entry belong there (`04` § Instruction File Recommendations). This is the coordinator's commit at the integration.
- **The guest halves owed at the integration window, by stream, every one `fix-walk-pending-image`:**
  - **S1:** the drive dialog after `z`.
  - **S2:** two toasts after a card, and the French list bar.
  - **S3:** the screensaver held over the transfer page, then started after.
  - **S5:** the hook's argv file.
  - **S6:** the removed `es_input.cfg` reconfigured.
  - **S8:** CLEAR on the keyboard, the key gap, and the configuring subtitle, in English and French at both sizes.
  - With the flow references each changed screen updates (`es-ui-style-guide.md`).
- **The retro.** `docs/retros/<date>-m6-es-core-window-input.md`, posted on #682, says what the slice did to the two time-to-play numbers: priced from the guest, or `CANNOT` with the harness's reason, citing `docs/vm-qa-log.md`, with each stream's clause carried. It also says what T36 and T37 inherit.
- **The shared host file's RETURN line.**

## What T36 and T37 inherit

The lane wrote the list at `02` § What T36 and T37 inherit (`02:803-817`, the brief's § 5 item 3's eleven items with their lines):

1. The provenance table.
2. The surfaces table.
3. The input table.
4. The locks table.
5. The lifetimes table.
6. The scripts table.
7. The `window-input-tests` build recipe.
8. The stand-in's rc per file over the 44.
9. The branches the host did not parse.
10. The `exists` cache's answer for T36's `FileSystemUtil`.
11. `Window.cpp:29`'s disposition.

Stage E adds to it in the retro, not here: the extractor's `SPECS` at the tip; the uncached reads S6 makes (for T36's cache: a writer outside `Utils::FileSystem` is invisible to it); `InputManager` as `AtomicFile::writeText`'s first caller in the 96 (for T21's API, T36's neighbour); and S3's screensaver hold on `GuiComponent`.

## What never runs here

- **Tools beyond the host's:** a build, a compiler beyond the host's `g++` for the unit targets, the sanitizer programs and the stand-in, a guest, a fetch, a keyed council call, anything on a unit.
- **A change outside the 96 and the audit folder.** The exceptions are the French catalog's `GAMEPAD` entry in S8 and the `stage-e/` patches named above.
- **These paths:** `es-core/src/components/**`, `resources/`, `utils/`, `HttpReq.*`, `Settings.*`, `SystemConf.*`, `AtomicFileUtil.*`, `CloudText.*`, `es-core/CMakeLists.txt`, `tests/app-unit/fakes/` and any es-app file beyond the `stage-e/` patches.
- **The window's signatures:** a change to `Window.h`'s `postToUiThread` or `createAsyncNotificationComponent`. T34's `s2-window.patch` is the integration's, not adopted here.
- **The pin and the catalog's history:** a move of the pin; a hand edit of the catalog's orphaned `GAMEPAD %i` or `up/down`.
- **Outside the rulings:** a fix to an upstream line beyond the contained fixes named; a per-event extension filter (ruling 9); a wait added to the quit path (ruling 8).
- **Hooks and input files on a guest:** a `scripts/<event>/` hook written anywhere but a guest at the integration window, or an `es_input.cfg` written on a guest by hand.
- **The held folder:** anything under `/workspace/tmp/m6-t34/held/`, opened or quoted.
- **A refused build:** a `t35-build-tests.sh` run whose extracts were refused. The script says so and does not build `window-input-tests`.

## Figures and lines not found in the record (ask the lane; do not guess)

1. **3.1's figure.** `stage-c/build-tests.out:91` prints `ResetComponent returned after 1496 ms` and `:93` `values: CHECK( 1496 <  300 )`. `00` (stage C and D), `02`, `04`, `05` PL-01 and #1283's trace say **1,491 ms**. The out file at `5d7650c1dc` is the later of at least two runs (the 3.17/3.3 rebuild re-wrote it). Which run the record quotes, and where the 1,491 ms run's output is kept, is not in the tree.
2. **3.2's `SAN` line.** `tools/t35-build-tests.sh:166` now runs `san asan-watchers address ...`, but `stage-c/build-tests.out` (written before that line was added) carries no `SAN asan-watchers` line. 3.2's only record is `stage-c/asan-watchers.out` (`rc=0`, `asan-watchers: done, 1 notification(s)`, compiled at `-O1 -fsanitize=address`). The script's own line at the pin is owed before S4's before/after pair can quote one form.
3. **`PUGIXML_INCLUDE_DIR` for the unit build.** `stage-c/build-tests.out` prints the rapidjson root (`:2`) and no pugixml line: the script prints `pugixml:` only for `es-settings-tests`, at `t35-build-tests.sh:78`. `00` says the stand-in took pugixml *"from the source cache's ES checkout at the pin"*. The value the build script used is not recorded, so the stage-E command line cannot be copied whole.
4. **The keyboard's key gap measured from a frame.** The brief § 7 asks for *"G-06's three keyboard frames with the key gap measured by a reader"*. `02` § The guest cycle's G-06 row carries the full-screen keyboard, the ESC frame, the `s` frame and PL-34, but no measured gap. The 3.33 px and 14.08 px (`05` PL-11; `stage-c/build-tests.out:86`) are computed, not measured. The *"4.2x"* ruling 3 cites is the brief's R4 item 6, not the lane's.
5. **Whose line each fixed item is, by `git log -S`.** The record has it for L-01's pop (the base `bccd715707` at its `:322-323`, `02` § The surfaces). The `stage-b/archaeology-*.out` files are register and log searches, not `git log -S`. It is not in the record for PL-03's quoting, PL-09's logs, PL-10's event, PL-15's order, PL-16's subtitle, PL-17's wait, PL-25's merge, PL-26's wake, or PL-27/PL-28's `emergencyFlush` and close. Ruling 19's #585 lines depend on it.
6. **The time-to-play prices.** `04` Q7: *"`fireEvent`'s three directory listings and three scans per event, `configureEmulators` built on every launch -- is priced from the guest when the window runs (L-19)"*. `02` § The guest cycle's time-to-play row gives only the startup card's ~100 s on the unreachable cloud. The price of L-19 and of `WatchersManager::pause` is not in the record.
7. **The 1280x800 keyboard and quit-box sizes** (G-11: *"about 0.78 W x 0.6 H"*, *"about 0.6 W"*). These are approximations without the reader's command. They are not needed by a ruling, but are named in case a frame row quotes them.
8. **`unregisterPostedFunctions`'s callers**, and whether any holds `mNotificationMessagesLock` at the call. This is S2's PL-07 precondition, and it is not listed in `02` § The lifetimes or § The surfaces.
9. **The line of `onScreenSaverActivate`'s declaration in `GuiComponent.h`.** S3's virtual goes beside it, and `02` cites `GuiComponent.cpp:30` only.
10. **The count of `GuiMsgBox` calls with three buttons and none named `OK` or `NO`,** in the 96 and in es-app (ruling 5's grep). The record names the drive dialogs only (`05` PL-15, `Window.cpp:1568-1578`).
11. **The source greps the brief's Q2 and Q5 asked for.** These are `inputAction` in the distribution's `projects/` and `packages/`, and `scripts/game-start` there. The record carries G-01's image reads instead: *"The shipped file has 0 `inputAction` lines"*, *"No `/usr/bin/scripts` and no user scripts folder"*. Rulings 8, 9 and 16 rest on G-01's lines.
12. **PL-06's two counts are two greps, not a disagreement, named so the hand-back does not mix them.** One is the 10 `createAsyncNotificationComponent` call sites in es-app (`02:204`). The other is T34's thirteen `AsyncNotificationComponent*` holder lines in six files (`t34-streams.md:25`, *"by the drafter's count over the grep's output"*).
