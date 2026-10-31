This is a static review of the supplied source. I have not rerun the reported fixtures. References below are relative to `es-core/src/` unless otherwise qualified; references to omitted files are treated as citations, not inspected source.

## 1. PL-01 — Watcher locking

**Read:** `watchers/WatchersManager.cpp:29-53,64-203`; `watchers/WatchersManager.h:31-45,77-88`.

**Yes.** The lock acquired at `:181` remains held through every `check()` at `:196`, notification at `:197`, and rescheduling at `:199`. `RegisterComponent`, `UnregisterComponent`, `ResetComponent`, `GetComponent<T>()`, and the destructor acquire that same mutex (`:66,78,94,143`; `.h:35`) and therefore wait for an in-progress probe. Their actual UI-thread callers are outside this packet.

The nesting is **watcher list → observers**: `:197` calls `NotifyComponentChanged`, which takes `mNotificationLock` at `:128` and invokes callbacks at `:131` without releasing either mutex.

**Callback re-entry can deadlock.** A callback calling `ResetComponent`, `GetComponent`, or another list-locking entry point attempts to reacquire its own non-recursive mutex. Calling `RegisterNotify` or `UnregisterNotify` similarly reacquires the observer mutex. The packet establishes this hazard, but contains no concrete observer body proving it currently happens.

Two corrections to the proposed verification/fix:

- At the pin, concurrent `UnregisterComponent` cannot free the current **`WatcherInfo`** during `check()` through the described path: both operations hold the same mutex. The proposed 3.2 FAIL-at-pin expectation is not supported by these lines.
- Probing a raw-pointer snapshot unlocked and merely revalidating afterward is insufficient. Both the record **and its `IWatcher` object** must remain alive throughout the probe.
- The cited unsynchronized flag is `mRunning` (`:151` versus `:161,172,187`). The shown accesses to `mPaused` are protected by `mThreadLock`; it should not be bundled into that race claim.

## 2. PL-02 — Toast ordering and the proposed fix

**Read:** `Window.cpp:298-351,1152-1175`; `Window.h:153-154`.

**Yes, queued notifications drain newest first:** enqueue uses `push_back` at `:320`; dequeue uses `back()/pop_back()` at `:339-340`.

**No, changing dequeue to the front and reversing the existing re-queue loop is not sufficient.** The loop still appends at `:1164`.

Counterexample:

1. Older toast **A** is already visible.
2. Newer toast **B** is queued.
3. A card appears and appends A to the queue: **[B, A]**.
4. FIFO dequeue now shows B before A. Reversing a one-element re-queue loop changes nothing.

Returned visible toasts must be **prepended ahead of pending newer notifications**, preserving their order. For this vector, that could be a range insertion at `begin()`, or reverse traversal combined with insertion at `begin()`—not reverse traversal with `push_back()`.

The covering test needs this interruption case, not just two notifications accumulated beneath an existing card.

## 3. PL-03 — Shell quoting

**Read:** `Scripting.cpp:88-149,153-207`.

The distinction is **literal ASCII space**, not shell-special characters:

- Without a space, all surviving argument bytes are appended bare (`:109-112`). This includes `$`, backticks, `;`, `&`, `|`, `<`, `>`, parentheses, single quotes, backslashes, tabs/newlines, and glob characters.
- With a space, the argument gets **double quotes**, not safe literal quoting. `$()`/backticks, parameter expansion and arithmetic expansion remain active; backslash retains shell significance. Semicolons and single quotes inside those double quotes are ordinarily literal.
- Every original `"` is removed (`:107`). Additionally, the duplicated `startsWith` test at `:104` removes the final character whenever the argument starts with `"`, whether or not it ends with one.
- The script path has the same space-only quoting weakness (`:92-93`), and the event argument is appended bare (`:95-96`).

**For one POSIX-shell parsing layer, yes:** single-quoting each complete original argument, replacing an embedded `'` with the close/escape/reopen sequence `'\''`, suffices for both `system(command)` and `/bin/sh -c command`. Apply it to the script path and event argument as well; do not first strip the original quotes.

That is not a Windows quoting solution, does not protect against a hook subsequently using `eval`, and cannot represent embedded NUL bytes. The actual `ProcessStartInfo` shell wrapper is an **unverified external citation** here. Also, shell substitutions happen before execution: a selected file need not successfully execute for argument substitution to be dangerous.

## 4. PL-04 — Cached absence after saving

**Read:** `InputManager.cpp:889-905,1113-1141,1179-1284`.

**Taking the cache citations as accurate, the second-pad overwrite is reachable.**

Each write creates a fresh document (`:1185`). If `exists(path)` remains false at `:1187`, the merge is skipped, the new device alone is appended (`:1224`), and `save_file` writes that document (`:1225`). Repeating this for a second device replaces the first device’s file. The reload and finish-command paths also consult `exists` (`:893,1239,1250`).

However, the packet does **not** contain the cache implementation or its invalidation paths. Thus I can confirm the input-side consequence **conditional on a persistent cached miss**, but cannot independently confirm that precondition, its default enablement, or persistence through the intervening calls. The reported 3.11 result is not a substitute for the missing source.

## 5. PL-05 and PL-06 — Screensaver and teardown

**Read:** `Window.cpp:49-63,82-105,115-207,777-813,1091-1138,1152-1260`; `Window.h:123-154`.

### Screensaver

**The window-side claim is correct.** Idle time triggers `startScreenSaver()` at `:777-779`. Its additional guards are only a screensaver object and `!mRenderScreenSaver` (`:1093`). Pages receive activation notifications, not a checked veto (`:1095-1103`). `mAllowSleep` controls the later sleep transition (`:803-805`), not screensaver activation.

`cancelScreenSaver()` calls `resetCounts()` at `:1117`; `removeGui()` does not. This does **not** prove that the external screensaver clears its list nowhere else, or independently prove the reported `FileData` use-after-free. Those require the cited es-app code.

### Teardown

**A surviving card can be drawn again after reinitialization.** Neither `deinit()` nor `init()` clears the notification vectors. Subsequent rendering traverses the card vector (`:1186,1226`) when the screensaver gate permits it (`:782-787`).

“Can” is important: the first subsequent update may retire an expired/closed card at `:1244-1252`. Reappearance is not guaranteed for every card.

The destructor has no ownership cleanup for these raw-pointer notification containers either. But distinguish:

- retained state across a reversible `deinit()`—not inherently a use-after-free;
- leaked survivors at destruction;
- a borrower accessing a card after deletion at `:1248`—a separate, conditional use-after-free.

The last requires the omitted holder paths. Simply deleting cards in `deinit()` does not make those borrowers safe; a method on an already freed card cannot reliably “refuse” a late call.

## Punch-item grades

Severities are unchanged unless explicitly noted.

- **PL-01 — confirmed:** the list mutex spans probes and callbacks, and all five named entry points acquire it (`WatchersManager.cpp:66,78,94,143,181-199`; `.h:35`).
- **PL-02 — confirmed with narrowing:** LIFO is proven, but the proposed FIFO/reversed-loop fix must also prepend returned toasts (`Window.cpp:320,339-340,1163-1164`).
- **PL-03 — confirmed with narrowing:** unsafe command construction is visible; the actual shell sink is an omitted citation, and double-quoted arguments remain substitution-vulnerable too (`Scripting.cpp:92-112,140-147`).
- **PL-04 — cannot tell from the packet:** the overwrite follows from a persistent false result, but negative caching/invalidation is not supplied (`InputManager.cpp:1185-1225`; cited `utils/FileSystemUtil.cpp:296,323`).
- **PL-05 — confirmed with narrowing:** idle-only initiation without a page veto is shown; the slideshow-list lifetime and reported UAF are external (`Window.cpp:777-779,1091-1138`).
- **PL-06 — confirmed with narrowing:** notification retention and missing container cleanup are shown; redraw is conditional, and an actual late-holder UAF is not demonstrated (`Window.cpp:49-63,115-207,1244-1252`).
- **PL-07 — confirmed:** unlocked vector traversal/erase races posting despite the producer’s lock (`Window.cpp:1262-1283`); **Medium rather than Low**, because this is container corruption/undefined behavior.
- **PL-08 — confirmed with narrowing:** the shown persistent writes are in-place; a failed XML parse can retain a partial tree, so the next save does not invariably contain only one device (`InputManager.cpp:1185-1225,1232`; `FavoriteMusicManager.cpp:71,115-123`).
- **PL-09 — confirmed:** both logs read the still-null `configNode` immediately before assigning `item` (`InputManager.cpp:940-961`).
- **PL-10 — confirmed:** the non-Windows F4 branch allocates an event and never frees it after the copying `SDL_PushEvent` call (`InputManager.cpp:792-799`).
- **PL-11 — confirmed with narrowing:** accepting the menu citation, these are independent translation-unit macros, not a collision or necessarily a shared sizing rule; keyboard padding actually divides its factor by four (`GuiTextEditPopupKeyboard.cpp:14,220`); **Informational naming debt**.
- **PL-12 — confirmed:** CLEAR and `x` call the acceptance callback with `""` and delete the popup immediately; consequential effects depend on the caller (`GuiTextEditPopup.cpp:34`; `GuiTextEditPopupKeyboard.cpp:392-397,491-496`).
- **PL-13 — confirmed:** re-queue uses a fresh default, not the original duration or remainder (`Window.cpp:298-309,1164`); **Informational if retained as the stated design**.
- **PL-14 — confirmed with narrowing:** there is no timeout or exception while any card remains; the hasher’s particular duration is external (`Window.cpp:336-337`).
- **PL-15 — confirmed:** the fallback selects the last button, and the unconfigured-pad branch also accepts button releases; the supplied merge dialog makes Back invoke merge (`GuiMsgBox.cpp:125-133,257`; `Window.cpp:1568-1577`); **Medium rather than Low**.
- **PL-16 — confirmed:** the displayed number is the device/SDL instance ID plus one, not the computed seat (`GuiInputConfig.cpp:134`; `InputManager.cpp:525,581`).
- **PL-17 — confirmed with narrowing:** on non-Windows, the per-event pass necessarily sets `waitForExit=false`, including for quit; this proves the requested flag, with execution semantics in the omitted executor (`Scripting.cpp:142,177,205`).
- **PL-18 — confirmed with narrowing:** every returned per-event entry is submitted for execution, but a non-executable `notes.txt` need not actually run; an extension filter is also not an execution-security boundary (`Scripting.cpp:169-178,198-205`).
- **PL-19 — confirmed with narrowing:** the joystick lock encloses the finish-command invocation; synchronous waiting and UI-thread dispatch rely on omitted executor/caller code (`InputManager.cpp:485,605,623,1238,1272`).
- **PL-20 — confirmed:** the two stored names differ after lowercasing; launcher impact is not established here (`InputManager.cpp:1105-1107`; `GuiInputConfig.cpp:273,279`; `InputConfig.cpp:186-189`).
- **PL-21 — confirmed:** all four keyboard chords bypass the commented-out Debug gate (`Window.cpp:262-281`).
- **PL-22 — confirmed:** the cross-layer include and four detached, raw-`this` workers are visible, with no joining teardown (`Window.cpp:29,49-63,1554-1637`); **Medium for the lifetime hazard**, separate from informational layering debt.
- **PL-23 — cannot tell from the packet:** centering is shown, but the allegedly stale rule text is only cited (`Window.cpp:1192`; omitted `.claude/rules/es-native-ui.md:30`).
- **PL-24 — confirmed with narrowing:** text is submitted twice, not necessarily spoken completely twice; non-expanding speech replaces/cancels prior work (`GuiMsgBox.cpp:44,234,240`; `TextToSpeech.h:30`; `.cpp:45,258-259,270-271`).

## Additional defects

These **G-n** identifiers denote independent code findings, not the packet’s guest-case identifiers.

### G-1 — Help-prompt merging uses the opposite comparisons — Low

`Window.cpp:1032-1036` uses `!=` where complementary d-pad halves require equality.

- `("up/down","MOVE")` followed by `("left/right","MOVE")` **does not merge**.
- `("a","MOVE")` followed by `("up/down","MOVE")` instead replaces the **A-button prompt** with `"up/down/left/right"`.

This contradicts both the claimed 3.16 behavior and the assurance that only repeated icons are dropped (`:1023-1045`). Test both complementary halves and an unrelated icon sharing the action text.

### G-2 — Posting from workers races the window’s sleep/idle state — Medium

`postToUiThread()` reads/writes `mSleeping` and writes `mTimeSinceLastInput` under the notification mutex (`Window.cpp:1284-1288`). UI update, render and cancellation access those fields without that mutex (`:540,778,803-810,1111,1129-1132`).

The supplied storage workers call this method from background threads (`:1554-1556`, among others). Protecting the queue does not protect these separate state accesses. Queue the wake request and apply the window-state changes on the UI thread.

### G-3 — Logger shutdown can lose an already-enqueued final batch, and races its stop flag — Medium

An admissible sequence is:

1. Worker swaps buffers and starts draining A (`Log.cpp:130-133`).
2. A producer enqueues into B (`:104-105`).
3. `close()` sets `mShutdown` (`:70-71`).
4. Worker finishes A and exits at `:152`, without swapping B.
5. `close()` drains the already-cleared **drain** buffer again (`:79,156-161`), leaving B unwritten.

This can lose entries enqueued **before** shutdown. Also, `mShutdown` is a plain bool (`:189`), written under the mutex but read outside it at `:152`. Shutdown must synchronize the predicate and drain pending work before exiting.

### G-4 — Emergency log flushing is neither stream-safe nor signal-safe — Medium

`emergencyFlush()` eventually calls `mFile.flush()` on its caller’s thread (`Log.cpp:84-99`), including after its bounded wait expires, while the worker may still write/flush the same stream (`:133-147,164-166`). There is no exclusive stream ownership across these operations.

The same routine runs from SIGABRT/SIGTERM handlers (`:237-242,282-285`). Condition-variable operations and C++ stream I/O are not async-signal-safe. A normal flush needs a proper worker completion protocol; the signal handler needs a separate async-signal-safe path.

### G-5 — Axis reversal without an intervening neutral sample is lost — Medium

`InputManager.cpp:727` compares only whether old and new magnitudes exceed the deadzone. A transition from a positive extreme directly to a negative extreme makes both predicates true, so no input is emitted; the stored previous value nevertheless changes at `:742`.

The direction therefore remains stale until another boundary crossing. Compare signed normalized states, with the necessary old-direction release and new-direction press (`:727-742`; `InputConfig.cpp:224-225`).

### G-6 — SDL-generated analog names do not match core directional matching — Medium

The SDL conversion writes `"joystick1left"`, `"joystick1up"`, `"joystick2left"` and `"joystick2up"` (`InputManager.cpp:993-996,1096`). `InputConfig::isMappedLike()` recognizes `"leftanalogleft"`, `"rightanalogleft"`, and the corresponding up/down/right names—not those generated names (`InputConfig.cpp:233-247`).

`mapInput()` performs only lowercasing (`:186-189`), so there is no alias conversion here. An automatically mapped stick can consequently fail the core directional-matching API despite being recorded as configured.

### G-7 — Windows scripting shutdown does not join its worker — Medium

The first reader’s lifetime tables say `exitScriptingEngine()` joins the script thread. It does not: it only sets the exit flag and notifies (`Scripting.cpp:75-82`). The thread allocated at `:67-68` is never joined or deleted anywhere in the supplied file.

Shutdown therefore supplies no barrier against the worker still accessing the static queue, mutex and condition variable (`:18-53`). Release the mutex before joining; separately decide whether pending commands should drain or be discarded.

### G-8 — Windows hot-plug rebuilds accumulate SDL subsystem references — Medium

Every Windows device-added event calls `rebuildAllJoysticks(false)` (`InputManager.cpp:849-850`). That skips `SDL_QuitSubSystem` (`:381-382`) but still calls `SDL_InitSubSystem(SDL_INIT_JOYSTICK)` unconditionally (`:402`).

Successful repeated SDL initialization increments the subsystem reference count. `InputManager::deinit()` performs only one quit (`:188-189`), so repeated hot-plugs can leave the joystick subsystem initialized after the purported teardown.

### G-9 — Mouse-only supported Windows guns fail the discovery gate — Medium

The physical-gun detection pass requires **`dwType != RIM_TYPEMOUSE`** and a recognized gun path (`GunManager.cpp:637-644`), but the subsequent creation pass accepts **only** `RIM_TYPEMOUSE` entries (`:648-653`).

A recognized gun exposing only a mouse collection, without WiimoteGun, therefore never enables discovery/capture. Its mouse entry is explicitly excluded from the predicate that would admit it.

### G-10 — Windows gun motion drops single-axis movement and zero-edge coordinates — Medium

`GunManager.cpp:425` requires both `lLastX != 0` **and** `lLastY != 0` before handling either relative or absolute movement.

Thus `(dx,0)` and `(0,dy)` relative reports are discarded, and valid absolute reports with either coordinate zero are discarded too (`:425-455`). Motion validity must be handled according to the report’s absolute/relative mode, not this conjunction.

### G-11 — Successful udev gun removal leaks the received event reference — Low

A successful removal marks the incoming device event handled (`GunManager.cpp:547-548`), suppressing the caller’s `udev_device_unref(dev)` (`:552-553`).

But removal only closes/unrefs the device retained by the existing gun (`:1033`; `udev_closeGun` at `:1011-1014`). It neither retains nor releases the incoming remove-event reference. Unlike successful addition (`:998`), successful removal has not transferred ownership of that reference.

### G-12 — Replacing Windows speech leaks queued speech objects — Low

`TextToSpeech::say()` clears `mSpeechQueue` when `expand` is false (`TextToSpeech.cpp:258-259`), but entries are allocated `SpeakItem*` objects (`:261-264`). Clearing the pointer container does not delete them.

The worker deletes only items it has popped (`:33-46`), and teardown deletes only items still in the queue (`:133-136`). Delete discarded entries or use owning smart pointers.

### G-13 — Windows speech shutdown races its condition-variable predicate — Medium

`mShouldTerminate` is a plain bool (`TextToSpeech.h:50`). The worker reads it under `mMutex` in its wait predicate (`TextToSpeech.cpp:27-30`), while teardown writes it without that mutex and then notifies/joins (`:124-128`).

Besides the data race, notification can occur between predicate evaluation and waiting, leaving teardown blocked in `join()`. Set the predicate under the same mutex before notifying.

### G-14 — File-based theme loading ignores XML parse failure — Low

The file-loading branch discards `doc.load_buffer()`’s result (`ThemeData.cpp:807-810`), whereas the string-loading branch checks its result and throws (`:814-816`).

A malformed file with a retained `<theme>`/`<formatVersion>` prefix can pass the subsequent structural checks and be partially applied without reporting the XML parse error (`:819-833`). Check and report the parse result in both branches.

## Sections I need

- **Cache behavior and defaults:** `es-core/src/utils/FileSystemUtil.cpp:130-225,270-335,1115-1145`; `es-core/src/utils/FileSystemUtil.h:1-180`; `es-core/src/Settings.cpp:145-165`.
- **Actual executor and waiting defaults:** `es-core/src/utils/Platform.cpp:35-65,135-190`.
- **Full #1305 lifetime chain:** `es-app/src/SystemScreenSaver.cpp:330-385,525-555`; `es-app/src/SystemData.cpp:450-480`.
- **Notification retirement/render behavior and shutdown ordering:** `es-core/src/components/AsyncNotificationComponent.cpp:1-300`; `es-core/src/components/AsyncNotificationComponent.h:1-160`; `es-core/src/guis/GuiInfoPopup.cpp:1-90`; `es-app/src/main.cpp:330-360,1310-1370`.
- **Cited watcher callers/observer behavior:** `es-app/src/NetworkThread.cpp:45-100,140-220`; `es-app/src/guis/GuiRetroAchievementsSettings.cpp:790-825`.
- **Padding comparison:** `es-core/src/components/MenuComponent.cpp:1-20,535-560`.
- **Allegedly stale instruction text:** `.claude/rules/es-native-ui.md:24-34,185-210`.