#!/usr/bin/env python3
"""T31 (#678): the titles and bodies of the 21 bugs the stage-D ruling names, from 05-punch-list.md
(T26's t26-file-bugs.py, adapted: these are filed before the stream brief, so each carries its own code trace).

    python3 -I t31-file-bugs.py <05-punch-list.md> <out dir>

Writes <out dir>/PL-NN.title and PL-NN.md. A body is: an introduction, the
item's section of 05 copied (its family, owner area, fix shape, VM line,
Already written line, acceptance and the ruling), then a code trace in four
parts -- how it was found, the defect at its source at the pin, the siblings
hunted, and what reading cannot prove -- then the acceptance every T31 bug
shares. Asserts 21 bugs, each with a trace.
"""
import os, re, sys

PLS = ["PL-01", "PL-02", "PL-03", "PL-04", "PL-05", "PL-06", "PL-07", "PL-08", "PL-09", "PL-10", "PL-11", "PL-12",
       "PL-14", "PL-15", "PL-16", "PL-18", "PL-19", "PL-20", "PL-21", "PL-22", "PL-23"]
TRACE = {
 "PL-01": ("Reading `GuiSettings::input` for L-01 at stage B; G02 on the guest (START left `es_settings.cfg` untouched, B wrote `ShowCheevosIcon=false`); `stage-c/l01-start-drops.py` FAILs at the pin; the seat's EP-1 and EP-34 narrowed and extended it.",
           "`GuiSettings.cpp:106-112` (START), `:133-139` (the bar's CLOSE) and `:456-464` (an outside click) delete pages without `close()` (`:73-81`), the only caller of `save()` and `mOnFinalizeFunc`; `~GuiSettings` (`:68-71`) is empty.",
           "`GuiScraperStart.cpp:542-548` and `GuiMetaDataEd.cpp:620-624` carry the same loop. `GuiGameOptions` saves in its destructor (`:494-501`), so it is not affected. FAVORITE SONGS' close key is SELECT (`GuiFavoriteMusicSelector.cpp:15`). The loop meets mixed stacks: BIOS DETAILS is a `GuiSettings` over the plain `GuiBios`.",
           "Which `onFinalize` functions across the app push a page (GuiMenu's are T26's); the stream reads them."),
 "PL-02": ("L-02 at stage B (the LED page's lambda); `stage-c/l02-led-not-saved.py` FAILs at the pin; the seat's EP-2 narrowed it and EP-36 extended it to text-only pages; T26's PL-17 is the same return.",
           "`GuiSettings.cpp:83-96`: `save()` returns when `mSaveFuncs` is empty, before `saveFile`/`saveSystemConf`. `GuiAnalogSticksLedControls.cpp:62-87` writes `SystemConf::set` at each slider step and registers no save function.",
           "Text rows write memory only (`GuiSettings.cpp:218-238`), so Moonlight's page (`GuiMoonlight.cpp:278-343`) and NETPLAY with ad hoc on (`GuiGameOptions.cpp:203-216`) flush nothing on their own close. Four GuiMenu sub-pages work around it (T26's PL-17). Nothing calls `saveSystemConf` at exit (`main.cpp`, `es-core`).",
           "Whether a device's boot `ledcontrol` would read a pending value written later in the same session; the fix makes the question moot."),
 "PL-03": ("L-05 at stage B (Moonlight's commands); `stage-c/l05-l06-moonlight.py` makes the canary through all three; the seat's EP-28 found the generated launchers.",
           "`GuiMoonlight.cpp:282`, `:304`, `:306`: `snprintf(..., \"%s\", server_ip)` into `executeScriptLegacy`, which is `popen` (`ApiSystem.cpp:2269`). `:223-239`: each launcher written with `\"<title>\"` (double quotes: `$()` and backticks stay live) and the host bare.",
           "The pairing reader writes a host parsed from moonlight's output back to `moonlight.host` (`:310-311`). The PIN is four digits (`:270-271`). `WifiScanProcess.h` is the argv model (#1192).",
           "The launchers' run on a device (they are run by the emulator launch, T1's path); the fixture runs a generated one under bubblewrap."),
 "PL-04": ("The seat's EP-29 and EP-30, read at their lines.",
           "`GuiMoonlight.cpp:174-184`: `rm .../images/*` and `rm .../*` before `GetAppListXml()`; a failure returns `false` after the deletion. `:230-257`: streams unchecked, `gamelist_doc.save_file` ignored, `return true`. `WriteBoxArtFile` returns `true` regardless (`:167-171`).",
           "On `true` the page quits ES to reload (`:289-293`); on `false` it says \"Unable to connect to server\" (`:295`).",
           "A real server's applist; the fixture doubles the fetch."),
 "PL-05": ("L-06 at stage B; G09 on the guest (the box said cleared, both seeded directories intact); the fixture's two `rm` exit 1; the seat's EP-17 extended it to the embedded branch.",
           "`GuiMoonlight.cpp:330-333`: `rm -r \"~/.cache/...\"` -- a tilde inside double quotes is literal. `:335`'s `rm -r ~/.cache/moonlight` expands, and neither branch reads a result.",
           "`fileExists` tests the real path (`:329`), so the branch is taken; the success box is unconditional.",
           "No server-side revocation is claimed or tested; the cleanup is local."),
 "PL-06": ("The seat's EP-32, read at its lines.",
           "`GuiMoonlight.cpp:54-61` and `:83-87`: `do { getline } while (line.find(marker) == npos)` with no EOF test. `:69-74` and `:95-99`: `replace(find(\"\\\\n\"), 2, ...)` throws `out_of_range` when the first `find` is `npos`.",
           "Both run inside `executeScriptLegacy`'s line callback (`:308-325`), synchronously on the interface thread (`ApiSystem.cpp:2278-2287`).",
           "The conf's shape from every Moonlight version; the fixture feeds an empty and a malformed one."),
 "PL-07": ("L-13 at stage B; G06 on the guest (no message, no tile over a read-only directory; a 64 MB copy leaves the same frame); the seat's EP-11 narrowed it and EP-38 found the lock window; T2's PL-016 (#782) routed the message here.",
           "`GuiSaveState.cpp:513-529`: `getNextFreeSlot < 0` silent; `copyToSlot` false silent; true rebuilds the grid (`loadGrid` puts the cursor on START NEW GAME). `:499-505` probes the lock via `isFlockHeld`, which releases it (`AtomicFileUtil.cpp:440-449`), before the copy.",
           "DELETE goes through `SaveStateBookkeeper::deleteLater` on a worker under the lock (D-UI-073); COPY is the sibling that did not move. At the pin `SaveState::copyToSlot` ignores `copyFile` (`SaveState.cpp:231-238`), T2's SS-4, fixed on T2's branch.",
           "A card's copy time (the guest's disk wrote 64 MB within the second)."),
 "PL-08": ("L-03 at stage B; G08 on the guest (`global.netplay=0` after ENABLE NETPLAY was switched on); the seat's EP-3 extended it and EP-35 found the sibling.",
           "`GuiNetPlaySettings.cpp:155-187`: the relay option's callback runs `delete this` and pushes a new page with no `save()`. `GuiControllersSettings.cpp:200-211`: SHOW CONTROLLER ACTIVITY does the same.",
           "`OptionListComponent.h:310-311`, `:323-324` return straight after the callback; nothing of the deleted page is touched after it on those paths. Text rows on both pages are immediate in memory.",
           "The popup path of the option list (outside the read)."),
 "PL-09": ("L-12 at stage B; G05 on the guest (`rocknix-systems` shadowed by an exit-1 script: THE BIOS CHECK RETURNED NOTHING); the seat's EP-39 found the partial-output case.",
           "`ApiSystem.cpp:2233-2252`: `executeEnumerationScript` returns lines and drops `pclose`'s status; `:872-924` parses what came. `GuiBios.cpp:183-203` shows the empty case; `:158-162`, `:220-223` turn a header with no rows into ALL PRESENT (0).",
           "The launch-time check calls the same reader without `--all` (T1's script, T21's executor).",
           "`rocknix-systems`' own failure modes (T1's)."),
 "PL-10": ("L-26 from G05's frames (no bar at 640x480); confirmed at G12; the seat's EP-14 narrowed it.",
           "`GuiBios` (a `GuiComponent`, `GuiBios.h:15`) defines `getHelpPrompts` (`GuiBios.cpp:313-324`) and has no `render` calling `renderHelpPromptsEarly`; with full-screen menus `Window` draws no help while a second page is open (`es-code-traps.md`).",
           "The manager (`GuiSaveState.cpp:397-398`) and the scrape page (`GuiScraperRun.cpp:173-174`) draw their own. DETAILS is offered whenever `mBios` is non-empty (`:319-320`).",
           "Window's suppression code (es-core, outside the read); the frames show its effect."),
 "PL-11": ("L-11 from G12's French frame (`7 SUR 7 MANQUANT`); L-27 from G05's frame (Nds, Psx, Gb); the seat's EP-25 and EP-15 narrowed both.",
           "`GuiBios.cpp:220-230`: `to_string(n) + \" \" + _(\"OF\") + ...` assembled from fragments. `:143-156`: `e.name = proper(shortName)`, replaced only for a system in `sSystemVector`.",
           "`:263`'s PRESENT, BUT NOT A KNOWN VERSION is a whole msgid.",
           "Other locales' plural rules (French and English are the shipped two)."),
 "PL-12": ("L-09 and L-10 at stage B; `stage-c/l09-l10-scrape-page.py` FAILs at the pin; the seat's EP-8 narrowed L-09 and EP-9 found the input before the frame.",
           "`GuiScraperRun.cpp:225` writes line 4 only when `p.failed`; `:231` line 5 only when `done - errors > 0`. `:90-103`: `if (!input.value) return true; ... delete this` for any input once `p.finished`, `mShownFinished` untested.",
           "The comment at `:87-89` says SCRAPER is behind; `GuiScraperStart.cpp:489-492` closes it at the run's start. A completed run reported as cancelled is T32's L-02 (the ruling).",
           "`ThreadedScraper::progress()`'s synchronisation (T32's file)."),
 "PL-14": ("L-07 from G12's French frame (the rows French, the title English); `t31-titles.py` (no `_()` title).",
           "`GuiMoonlight.cpp:268`: `GuiSettings(window, \"MOONLIGHT GAME STREAMING\")`, a raw literal that xgettext never extracts and `es-menu-map-check`'s patterns never see; the map names no MOONLIGHT.",
           "The menu's row is translated (`GuiMenu.cpp:5758`). The four sentence-case boxes (`:295`, `:315`, `:333`, `:336`) stay as ROCKNIX wrote them (the ruling).",
           "None: the title and the map are read in full."),
 "PL-15": ("The seat's EP-31, read at its lines.",
           "`GuiMoonlight.cpp:40-50`: `ss << mlver` inserts the `FILE*`; `output.find(\"Embedded\")` searches its address; no `pclose`.",
           "`:301-306` uses it to choose between the two pair commands, so the embedded form is unreachable through it.",
           "What `moonlight -v` prints on each build (the fixture stubs it)."),
 "PL-16": ("The seat's EP-33, accepted in part.",
           "`GuiMoonlight.cpp:79-100`: `std::ofstream keyFile(\".../key.pem\")`, no mode; `:145-147` hands it to TLS as the client key.",
           "`extractClient` writes `client.pem` the same way (`:54-75`); a certificate is not a secret, the key is.",
           "The mode on the image (the umask and the directory): the stream's VM line reads it, labelled by side."),
 "PL-18": ("L-22 from reading `GuiLoading.h` whole; `stage-c/l22-guiloading-race.py` reports 2 ThreadSanitizer races; the seat's EP-21 extended it.",
           "`GuiLoading.h`: `threadLoading` writes `result` then `mRunning = false`; `update` reads `mRunning` and copies `result` with no ordering, before `~GuiLoading`'s join; `mHandle = new std::thread` is never deleted.",
           "18 `GuiLoading<` in the slice and 41 lines across the tree use it; `GuiBios.cpp:43-45`'s completion captures only `window`, others raw `this` (#1212).",
           "Whether the race has misbehaved on a device (undefined behaviour need not show)."),
 "PL-19": ("The seat's EP-40 and EP-41, read at their lines.",
           "`GuiImageViewer.cpp:272-277`: `static bool g_isGuiImageViewerRunning`, set and cleared per viewer and read in pool jobs (`:365-377`, `:501-512`). `:390-399`, `:536-545`: an empty first extraction returns without pushing or deleting the viewer `showPdf`/`showCbz` allocated (`:692-712`).",
           "`GuiSettings::lifeToken` (`GuiSettings.h:104-115`) is the fork's instance guard to follow.",
           "ThreadPool shutdown and the window's queue invalidation (es-core)."),
 "PL-20": ("L-04 from the rows table (`t31-rows.py`).",
           "`GuiGameOptions.cpp:204`: `addInputTextConfigRow(_(\"PLAYER PASSWORD\"), \"global.netplay.password\", false)`; `GuiSettings.cpp:190-193` shows the value when `password` is false.",
           "batocera's master has the same at `:198`. The scraper's secrets pass `true`.",
           "The editors' own confidentiality (es-core)."),
 "PL-21": ("L-15 and L-16 from G03 on the guest (`ScraperSystems=\"pico-8\"` at the first tab switch; a second write); the seat's EP-13 narrowed L-15, EP-4 withdrew L-16's cause, EP-42 found the stale filters.",
           "`GuiScraperStart.cpp:166-210`: \"\" reads as nothing remembered; the default set is saved when `currentSystem` is empty. `:83`, `:97-133`, `:173-175` bind the filters and systems to the scraper at build; `:215`'s change callback only sets `Scraper`.",
           "`save()` on each tab switch (`:34-37`); `Settings` marks a change only for an absent key or a different value (`Settings.cpp:646-654`).",
           "Which save function set `mWasChanged` on G03's second write (the stream's fixture records it)."),
 "PL-22": ("The seat's EP-37, read at its lines.",
           "`GuiSettings.cpp:321-334`: the accept handler captures `value` and opens the editor with it; `updateVal` (`:301-317`) changes the display and calls `onsave`, not the captured value.",
           "`GuiKeyboardtopads.cpp:168` edits a joystick's name with it; `addInputTextConfigRow` reads its store each time (`:243`) and is not affected.",
           "Other callers outside the slice (es-app-wide grep at the stream)."),
 "PL-23": ("The seat's EP-43, read at its line.",
           "`GuiSaveState.cpp:274-275`: `return file1->creationDate >= file2->creationDate;` inside `std::sort`'s comparator.",
           "The other branches compare with `<` (`:277`) and config equality (`:271-272`).",
           "Whether equal creation dates occur on a device (incremental states saved within one clock tick)."),
}
assert sorted(TRACE) == sorted(PLS), set(PLS) ^ set(TRACE)
text = open(sys.argv[1], encoding="utf-8").read()
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
INTRO = ("Found by T31 (#678), the audit of EmulationStation's other pages (`docs/audits/2026_10_27-epic-m6-es-pages/` on "
         "`feature/m6-es-pages-678`; the audit issue #1234), read at the ES pin `16dbac5211`. The section below is the item's "
         "in `05-punch-list.md`, copied with the stage-D ruling (#678, comment 6443081619); its leads and proofs are in "
         "`02-forward-audit.md`, the guest's records under `guest-cycle/`, the host harnesses under `stage-c/`.")
for pl in PLS:
    m = re.search(r"^## (%s): (.*?)\n(.*?)(?=^## PL-|^## Phase 7)" % pl, text, re.S | re.M)
    assert m, pl
    title = re.sub(r"\s*\((a `bug` proposed|recorded|keep an eye on)[^)]*\)\s*$", "", m.group(2)).strip()
    found, source, siblings, cannot = TRACE[pl]
    sect = m.group(3).rstrip()
    sect = sect.replace("- [ ] ", "- ")   # the item's own lines become the proof's description; the criteria are below
    body = "\n".join([INTRO, "", "## " + pl, sect, "",
                      "## Code trace", "",
                      "- **How it was found:** " + found,
                      "- **The defect at its source (the pin):** " + source,
                      "- **Siblings hunted:** " + siblings,
                      "- **What reading cannot prove:** " + cannot, "",
                      "## Acceptance criteria", "",
                      "- [ ] The item's positive FAILs on the pin and PASSes on the stream's commit: `stage-e/<stream>-before.txt` and `-after.txt` in the audit folder, as the item's **Acceptance** lines above describe.",
                      "- [ ] `02` § The streams carries the stream's row with this bug's `Already written:` answer, and `05`'s Phase 7 row names the commit.", ""])
    full = "Bug: EmulationStation: %s (T31 %s)" % (title, pl)
    open(os.path.join(out, pl + ".title"), "w").write(full + "\n")
    open(os.path.join(out, pl + ".md"), "w").write(body)
    print(pl, len(full), len(body))
