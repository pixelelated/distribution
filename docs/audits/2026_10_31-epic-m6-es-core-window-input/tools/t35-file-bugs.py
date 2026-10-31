"""File T35's `bug` issues (#682, stage D) from one table, T34's t34-file-bugs.py's shape:
each body carries its code trace, the positive before the fix, what reading cannot prove,
the VM line, the acceptance criteria (agent-verifiable, D-QA-044) and its `Already
written:` line (D-WORKFLOW-050). Writes the body files under <out dir> and, with --file,
files each with gh and prints `PL-nn #N`.
    t35-file-bugs.py <out dir> [--file]"""
import os
import subprocess
import sys

OUT = sys.argv[1]
FILE = "--file" in sys.argv
AUD = "docs/audits/2026_10_31-epic-m6-es-core-window-input"
TAIL = "Refs #682, #1337"
B = [
    ("PL-02", "Bug: EmulationStation: the toast queue drains newest first, against D-UI-093's decided order (T35 PL-02)",
     "`Window.cpp:339-340` against `:334-335` and `:1163-1164`",
     "`processNotificationMessages` takes the queue's `back()` and `pop_back()`, so toasts queued while a card is up show newest first. **D-UI-093's decided row says the opposite** (`docs/decision-register.md:404`: *Nothing is dropped; the order is the order things happened.*), and so does the fork's comment at `c1c0d6ddc` (`:334-335`). The pop is upstream's (the base `bccd715707` pops from the back at its `:322-323`); the fork's rule was written over it. The re-queue at `:1163-1164` appends a toast a new card takes off the screen behind any newer one already queued (the seat's counterexample, verified: A visible, B queued, a card returns A behind B).",
     "T35's audit of `es-core/**` as `rest` (#682): L-01 (the first reader), confirmed with narrowing by the independent seat; PL-02 in `" + AUD + "/05-punch-list.md` and #1337. This is a defect against a decided row, not a new question.",
     "`window-input-tests` (3.14, the pin's `:339-340` lifted verbatim): `CHECK( B second == A first )` -- B shown before A (`stage-c/build-tests.out`). **On the image** (the guest window, G-03): two toasts posted A then B under the startup card appeared stacked **B above A** after the card left (`guest-cycle/g02b-001.png`).",
     "the order of toasts queued under a card is not the order in which anything was shown, so neither data nor a file is involved.",
     "Yes -- host-only for the case (`tools/t35-build-tests.sh`), and the guest for the frame: `POST /notify` twice on the guest's own 127.0.0.1:1234 while a card is up, then a frame after the card leaves (G-03's shape).",
     ["`tools/t35-build-tests.sh`'s `window-input-tests` reports the 3.14 order case passing: no `ERROR: CHECK` under `3.14 the toast queue drains in the order things happened` in its run log",
      "a `window-input-tests` case for the interruption (A on screen, B queued, a card created) shows A before B once the card leaves",
      "a guest frame after a card leaves shows two toasts posted under it in the order they were posted (G-03's shape, `POST /notify` on 127.0.0.1:1234), labelled by side"],
     "nothing inherited -- the queue lives in memory for the session; the code writes no file and reads nothing an earlier build left."),
    ("PL-03", "Bug: EmulationStation: Scripting: a game's file name reaches /bin/sh unquoted when an event hook exists (T35 PL-03)",
     "`Scripting.cpp:88-149` (`:92-93`, `:95-96`, `:98-113`); `utils/Platform.cpp:162-181`",
     "`executeScript` builds one shell command line: the script path is quoted only when it contains a space (`:92-93`), the event name is appended bare (`:95-96`), and each argument has every double quote stripped (`:107`) and is quoted only when it contains a space -- then in double quotes, where `$( )`, backticks and parameter expansion stay live (`:109-112`). `ProcessStartInfo::run` hands that line to `system()` when it waits and to `/bin/sh -c` otherwise (`Platform.cpp:162-181`, T36's). So shell metacharacters in an argument a caller passes -- a game's path or name -- are interpreted by the shell whenever any script sits in an event folder. `:104` also tests `startsWith` twice where the second should be `endsWith`, so an argument that starts with a double quote loses its last character.",
     "T35's audit (#682): L-18 (the first reader) with T2's FD-9/FD-19, confirmed with narrowing by the seat; PL-03 in `" + AUD + "/05-punch-list.md` and #1337. Filed publicly with a neutral title at the coordinator's ruling (#682 comment 6542863818).",
     "`window-input-tests` (3.4, `Scripting.cpp:90-113` lifted verbatim): an argument carrying `$( )` and one carrying a backtick each arrive in the command unquoted (`stage-c/build-tests.out`). **The image ships no hook** (G-01: no `/usr/bin/scripts`, no user `scripts/` folder), so the shell sees an argument only once a hook is added.",
     "which callers pass which arguments for each event (es-app's, outside the slice), and what a hook then does with them (`eval` in a hook is the hook's).",
     "Yes -- host-only (the 3.4 case over the lifted lines); on a guest, a hook script that prints its arguments, placed in a user `scripts/<event>/` folder, shows what the shell received.",
     ["`window-input-tests`' 3.4 case passes: every argument, the script path and the event name reach the command single-quoted, with an embedded single quote escaped",
      "a `window-input-tests` case shows an argument that starts with a double quote keeps its last character (`:104`)",
      "on a guest, a hook in `/storage/.config/emulationstation/scripts/game-start/` that writes its argv to a file records each argument byte for byte for a game whose name holds shell metacharacters (the file's contents quoted in the issue)"],
     "nothing inherited -- the command line is built per event and kept nowhere; the hooks' own logs (`es_script_stdout.log`, `es_script_stderr.log`) are rewritten by the next run, and the fix reads nothing an earlier build wrote."),
    ("PL-04", "Bug: EmulationStation: es_input.cfg written by pugixml after a cached miss reads as absent for the rest of the session (T35 PL-04)",
     "`InputManager.cpp:893`, `:1187`, `:1225`, `:1239`, `:1250`; `utils/FileSystemUtil.cpp:296`, `:306`, `:323`, `:1122-1147`",
     "`exists(path)` with the file cache on (`Settings.cpp:155`) stores what `stat64` found, absence included (`FileSystemUtil.cpp:296`, `:323`); `pugi::xml_document::save_file` writes through `fopen`, never through `Utils::FileSystem`, so the cache never hears of the new file. On a device whose user `es_input.cfg` was absent at the first check (`:893`), the merge at `:1187` reads false and the save at `:1225` keeps only the device being configured; `loadInputConfig` after the write (`:1239`) and `doOnFinish` (`:1250`) read the same miss. An uncached `exists(p, false)` rewrites the entry (`:161-162`).",
     "T35's audit (#682): L-07, 3.11; the seat could not tell from the packet (the cache was outside it); 3.11 runs over the cache's own lines. PL-04 in `" + AUD + "/05-punch-list.md` and #1337. **Low:** the image's first boot copies the shipped `es_input.cfg` into place (G-01, 117,859 bytes), so the startup miss needs a user file that was removed.",
     "`window-input-tests` (3.11, `FileSystemUtil.cpp:48-341` and `:1122-1147` lifted verbatim): after a cached miss and a `save_file`, the cached read stays `false` (`stage-c/build-tests.out`).",
     "how often a user file is absent at startup on devices in the field (a removal, a reset of `/storage/.config`).",
     "Yes -- host-only for the case; on a guest, `rm /storage/.config/emulationstation/es_input.cfg`, restart the interface, configure the keyboard through CONTROLLER MAPPING (G-08's hold), then read the file.",
     ["`window-input-tests`' 3.11 case passes: after a cached miss and a `save_file`, the read `writeDeviceConfig` makes at `:1187` sees the file",
      "on a guest whose user `es_input.cfg` was removed before the interface started, a configuration through CONTROLLER MAPPING (the monitor hold of G-08) leaves an `es_input.cfg` the next `exists` reads as present and `loadInputConfig` loads (the file's `<inputConfig` count and the journal line quoted)"],
     "a device whose user file was absent at startup and had two inputs configured in one session may hold an `es_input.cfg` with only the last one -- read both: the file's format is unchanged, so the fixed reads load what is there; the dropped entry is not on the device to recover, and the player configures that input again."),
    ("PL-07", "Bug: EmulationStation: unregisterPostedFunctions erases the posted functions without the lock their producers take (T35 PL-07)",
     "`Window.cpp:1262-1274` against `:1276-1290`, `:1292-1307`",
     "`postToUiThread` appends under `mNotificationMessagesLock` and `processPostedFunctions` copies and clears under it; `unregisterPostedFunctions` iterates and erases `mFunctions` with no lock. A worker posting while a page unregisters reallocates the vector under the erase loop: container corruption, undefined behaviour.",
     "T35's audit (#682): L-03 (the first reader), confirmed by the seat at Medium; PL-07 in `" + AUD + "/05-punch-list.md` and #1337.",
     "`SAN tsan-posts (-fsanitize=thread): rc 66; WARNING: ThreadSanitizer: data race` -- the erase loop's read on one thread against the post's reallocation under the mutex on the other (`stage-c/tsan-posts.cpp` over `Window.cpp:1262-1274` and `:1276-1290` lifted verbatim; `stage-c/build-tests.out`).",
     "which pages unregister while a worker posts (the callers are es-app's).",
     "Yes -- host-only (the ThreadSanitizer program in `tools/t35-build-tests.sh`).",
     ["`tools/t35-build-tests.sh` prints `SAN tsan-posts (-fsanitize=thread): rc 0; no sanitizer report` (rc 66 and the race at the pin)"],
     "nothing inherited -- the posted functions live in memory for the session; no file is written or read."),
    ("PL-15", "Bug: EmulationStation: back on the GAME DRIVE DETECTED dialog lands on MERGE DRIVE (T35 PL-15)",
     "`guis/GuiMsgBox.cpp:116-134` (`:132-133`), `:257`; `Window.cpp:1568-1578` (the dialog), `:1550-1563` (the merge), `:1622-1640`",
     "`GuiMsgBox` binds back to the only button, else the first named exactly `OK` or `NO`, **else the last** (`:132-133`); `:257` also fires it for any button of an unconfigured pad. GAME DRIVE DETECTED with a drive id offers NO, IGNORE THIS TIME / NO, IGNORE FOREVER / YES, MERGE DRIVE (`Window.cpp:1568-1578`): none is named exactly `NO`, so **back takes YES, MERGE DRIVE**, whose lambda merges the drive's games, a choice that *also applies on future boots* (`:1547-1548`, `:1550-1563`). The format path asks again with NO first (`:1622-1625`), so back there binds NO. `es-ui-style-guide.md` § Confirmations: back must never land on the destructive choice.",
     "T35's audit (#682): L-12 (the first reader); the seat traced it to the drive dialog at Medium; **re-graded High as data safety** at the coordinator's stage-D ruling (#682 comment 6542863818). PL-15 in `" + AUD + "/05-punch-list.md` and #1337. Upstream ROCKNIX's dialog (outside the lanes, D-UI-079) carries a destructive default, which rule 6's contained fix removes.",
     "Read at the pin: the three labels at `:1569`, `:1570`, `:1577`, and `:125`'s comparison against `_(\"OK\")` and `_(\"NO\")`. **On the image** the accelerator lands on NO/NON where a NO exists (G-04, G-07); the drive dialog itself was not raised in the window.",
     "how often a player meets the dialog (a second card or a USB drive with games), and what `ApiSystem::mergeDrive` writes (es-app's).",
     "Yes -- `POST /storage/event` on the guest's 127.0.0.1:1234 (`es-app/src/services/HttpServerThread.cpp:577-597`) with a `REQUEST_MERGE` line naming a disposable mount and an id raises GAME DRIVE DETECTED; `z` (back) then shows what back chose.",
     ["a `window-input-tests` case over the drive dialogs' button labels shows the accelerator binds a non-destructive button for GAME DRIVE DETECTED (with and without an id) and NEW DRIVE DETECTED",
      "the fix gives the dialog a button named exactly `NO` (or binds the accelerator to the non-destructive choice) and orders the buttons with the safe one last; the diff and the case's PASS line quoted",
      "on a guest, `POST /storage/event` with a `REQUEST_MERGE` line raises GAME DRIVE DETECTED, and after `z` a frame shows the dialog closed with no `Merge requested` toast and the guest's journal shows no merge request (frames labelled by side)"],
     "a merge already applied by a back press is persisted by `mergeDrive` for future boots and is indistinguishable from one chosen on purpose -- nothing migrated: the fix changes the dialog, not what an earlier press wrote, and a merged drive stays merged until the player changes it."),
    ("PL-27", "Bug: EmulationStation: the logger can lose its final batch at close, and reads its stop flag outside the lock (T35 PL-27)",
     "`Log.cpp:63-82`, `:101-108`, `:117-162`, `:189`",
     "`close()` sets `mShutdown` under the mutex, notifies and joins; the worker swaps the buffers (`:130`), drains, flushes, and breaks when it reads `mShutdown` (`:152`) -- outside the mutex. Entries enqueued after the worker's last swap stay in the write buffer: the worker exits without another swap, and `close()` then drains the already-cleared drain buffer (`:79`, `:156-161`). #178's promise (*every batch reaches the file*, `:135-146`) does not hold at close. `mShutdown` is a plain `bool` (`:189`).",
     "T35's audit (#682): the seat's G-3, verified at the pin; PL-27 in `" + AUD + "/05-punch-list.md` and #1337. The fork's logger (fork #178).",
     "Read at the pin: the sequence swap (`:130`) / enqueue into the new write buffer (`:104-105`) / `close()` (`:70-71`) / break (`:152`) / `close()` drains the drain buffer (`:79`). No case has run it yet.",
     "how many lines a real exit loses (it depends on the timing of the last `LOG` against `Log::close`).",
     "Yes -- host-only: a `Log.cpp` binary (3.23's, with the `SDL_timer.h` fake and test-defined `Settings`/`Paths` as `SystemConfTests.cpp` does) that enqueues during shutdown and reads the file.",
     ["a `Log.cpp` case built by `tools/t35-build-tests.sh` enqueues lines while `close()` runs and finds every one of them in the file afterwards",
      "a ThreadSanitizer program over `close()` and the worker reports no race on `mShutdown` (`SAN ... rc 0; no sanitizer report`)"],
     "the log (`es_log.txt`) is rewritten at each start and nothing reads it back; what earlier exits lost was never written -- nothing inherited to read or migrate."),
]


def body(t):
    pl, title, where, defect, found, positive, cannot, vm, crit, already = t
    return "\n".join([
        "## Code trace", "",
        "**Where (at `16dbac5211`):** " + where, "",
        "**The defect:** " + defect, "",
        "**How it was found:** " + found, "",
        "**The positive before the fix:** " + positive, "",
        "**What reading cannot prove:** " + cannot, "",
        "**Can this be done on the VM?** " + vm, "",
        "## Acceptance criteria", "",
        *["- [ ] " + c for c in crit], "",
        "**Already written:** " + already, "",
        TAIL, ""])


os.makedirs(OUT, exist_ok=True)
for t in B:
    open(os.path.join(OUT, t[0] + ".md"), "w").write(body(t))
    if FILE:
        r = subprocess.run(["gh", "issue", "create", "--repo", "pixelelated/distribution", "--title", t[1], "--label", "bug",
                            "--milestone", "M6: Codebase renovation", "--body-file", os.path.join(OUT, t[0] + ".md")], capture_output=True, text=True)
        url = (r.stdout.strip().split("\n") or [""])[-1]
        print(t[0], ("#" + url.rsplit("/", 1)[-1]) if r.returncode == 0 else ("FAILED " + r.stderr.strip()[:200]))
print("t35-file-bugs: %d bodies written%s" % (len(B), ", filed" if FILE else ""))
