# GPT-6 Astra's 43 items, graded by the first reader (#678)

The seat's answer is `second-opinions/astra-audit.md` (keyed call 2 of 2, 12:59:34 to 13:14:26 UTC). Each item was read against the pin's lines it cites, at the lines, before a grade was given. `accepted` means the item stands as the seat wrote it; `in part` means part of it stands, with the part named; `not kept` means the reading did not hold it. New items become leads L-28 to L-43, in the seat's order.

| Item | Lead | Seat's verdict | Grade | The reader's check |
| --- | --- | --- | --- | --- |
| EP-1 | L-01 | narrowed | accepted | `GuiGameOptions::~GuiGameOptions` runs its save functions (`GuiGameOptions.cpp:494-501`); FAVORITE SONGS sets the close button to SELECT (`GuiFavoriteMusicSelector.cpp:15`); BIOS DETAILS is a `GuiSettings` over the `GuiComponent` `GuiBios`; `close()` is not virtual. The fix shape becomes a type- and lifetime-aware close-all, put to the pause |
| EP-2 | L-02 | narrowed | accepted | `SystemConf::set` keeps the change pending and a later `saveSystemConf` from any page writes it: "the LED page does not save its own change; it persists only when a later page flushes `system.cfg`" |
| EP-3 | L-03 | narrowed | accepted | the three lobby switches and INDEX NEW GAMES AT STARTUP (`:38-45`) are dropped too; HOST, PORT, NICKNAME and CUSTOM RELAY SERVER are immediate in memory |
| EP-4 | L-16 | refuted as stated | accepted | `Settings::setString`/`setX` mark a change only when the key is absent or the value differs (`Settings.cpp:646-654`, `:670-686`); "a default counts as a change" is not shown for a key the defaults populate. The two G03 mtimes stand as observations; the cause is unknown until a test records the keys that set `mWasChanged` |
| EP-5 | L-25 | confirmed | accepted | -- |
| EP-6 | L-04 | confirmed | accepted | and the scraper's secrets are masked **on their rows**; the editor's confidentiality is outside this read |
| EP-7 | L-08 | confirmed | accepted | -- |
| EP-8 | L-09 | narrowed | accepted | an incomplete failure outcome, not a failure shown as success; it also covers partly successful runs with per-game errors; the harness control's words ("NO MATCH", "UPDATE GAMELISTS" after zero) are not a product sentence |
| EP-9 | L-10 | confirmed, extended | accepted | `input` deletes on `p.finished` before `update` has set `mShownFinished` and drawn the outcome (`:94-101`, `:205-210`); and the comment at `:87-89` is wrong: SCRAPER was closed at the run's start (`GuiScraperStart.cpp:489-492`) |
| EP-10 | L-12 | narrowed | accepted | the empty screen conflates failed, unavailable and empty; the stronger case is EP-39 |
| EP-11 | L-13 | narrowed | accepted | at the pin a failed `copyFile` takes the `true` branch (`SaveState.cpp:231-238`); "the new tile off-screen" is G06's layout, not every copy; PLAY's downstream launch work is outside this read (`03` § 3.6 corrected) |
| EP-12 | L-14 | confirmed, extended | accepted | any failed `flock` other than EINTR also reads as held (`AtomicFileUtil.cpp:444-447`) |
| EP-13 | L-15 | narrowed | accepted | the condition is `currentSystem.empty()`; the fallback is eligible listed systems with platform ids |
| EP-14 | L-26 | narrowed | accepted | REFRESH is a visible button (`GuiBios.cpp:81`); the bar's loss is DETAILS and START; the DETAILS prompt should follow focus (`:319-320` tests only `mBios`) |
| EP-15 | L-27 | narrowed | accepted | the test is membership in `sSystemVector` (a loaded system), not games |
| EP-16 | L-05 | confirmed; narrowed elsewhere | accepted | the generated launchers are L-28; "safe by shape" for Bluetooth and storage is withdrawn as unsupported by this read; `WifiScanProcess.h` preserves non-zero exit codes (`:184-185`) and its reap is a bounded attempt |
| EP-17 | L-06 | confirmed, extended | accepted | the embedded branch (`:335`) expands its tilde but also reports success unchecked |
| EP-18 | L-19 | confirmed | accepted | reordering does not fix a label-based accelerator |
| EP-19 | L-20 | confirmed | accepted | -- |
| EP-20 | L-21 | confirmed; terms | accepted | four call sites across three leads; DELETE COLLECTION's NO deletes the options page (navigation only, `GuiGameOptions.cpp:630-654`) |
| EP-21 | L-22 | confirmed, extended | accepted | the copy of `result` precedes the join; the thread object leaks; "benign so far" withdrawn |
| EP-22 | L-17 | narrowed | accepted | thread-affinity brittleness, not a proven second race; BIOS's first loader captures only `window` (`GuiBios.cpp:43-45`): ownership graded per site |
| EP-23 | L-18 | narrowed | accepted | the zoom path (`GuiImageViewer.cpp:675-681`), a rebuild after `forgetScreenshots`, and a first uncached non-screenshot path all trigger the walk |
| EP-24 | L-07 | confirmed | accepted | "regenerated", not "necessarily different" |
| EP-25 | L-11 | narrowed | accepted | the defect is fragmented translation and missing plural agreement, not "English word order" |
| EP-26 | L-23 | narrowed (cannot confirm) | **not kept** | the target is `add_executable(emulationstation ${ES_SOURCES} ${ES_HEADERS})` (`es-app/CMakeLists.txt:315`); the only GLOB (`:301`) is MSVC's source grouping; `GuiAutoScrape` is in no list. L-23 stands |
| EP-27 | L-24 and the census | narrowed | accepted | **the rows tool counted two `addSwitch` calls inside a `/* */` block** (`GuiScraperStart.cpp:370-376`): fixed in `t31lib.py` (a scan that skips strings; four constructed cases pass), 21 switches; `GuiGamelistOptions.cpp:389` parses grid dimensions; "three added files" are one page, an executor and its header; the viewer file defines three classes; "inherits the menu's bar" is not shown by "opened from a settings page" |
| EP-28 | **L-28** | new | accepted | `GuiMoonlight.cpp:223-239`: the server's `AppTitle` inside double quotes in a generated `.sh`, the host bare |
| EP-29 | **L-29** | new | accepted | `:174-184`: `rm` before the fetch |
| EP-30 | **L-30** | new | accepted | `:230-257`: unchecked streams, `save_file` ignored, `true` returned; `WriteBoxArtFile` returns `true` (`:167-171`) |
| EP-31 | **L-31** | new | accepted | `:40-50`: `ss << mlver` streams the `FILE*`; no `pclose` |
| EP-32 | **L-32** | new | accepted | `:54-74` (and `:79-100`): `getline` loops without EOF; `replace(npos, ...)` throws; run inside the pairing callback |
| EP-33 | **L-33** | new | accepted in part | the key is written by a plain `ofstream` (`:79-100`); its mode depends on the umask and the directory, outside this read: plausible, a VM read of the mode settles it |
| EP-34 | **L-34** | new | accepted | `GuiSettings.cpp:456-461`: an outside click deletes the page without `close()` |
| EP-35 | **L-35** | new | accepted | `GuiControllersSettings.cpp:200-211`: the activity switch deletes and reopens without `save()` |
| EP-36 | **L-36** | new | accepted | text rows write memory only; a page of only text rows (Moonlight; NETPLAY with ad hoc on, `GuiGameOptions.cpp:203-216`) flushes nothing on its close; T26's PL-17 is the same shape |
| EP-37 | **L-37** | new | accepted | `GuiSettings.cpp:321-334`: the editor reopens from the captured `value` |
| EP-38 | **L-38** | new | accepted | the probe releases the lock before the copy (`AtomicFileUtil.cpp:440-449`; `GuiSaveState.cpp:499-516`) |
| EP-39 | **L-39** | new | accepted | `GuiBios.cpp:158-162`, `:220-223`: a header with no file rows is ALL PRESENT (0); a script dying after PRESENT rows reads clean |
| EP-40 | **L-40** | new | accepted | `g_isGuiImageViewerRunning` (`GuiImageViewer.cpp:272-277`, `:365-374`): a plain global, not an instance guard |
| EP-41 | **L-41** | new | accepted | `:390-399`, `:536-545`: an empty first extraction returns without deleting the unpushed viewer |
| EP-42 | **L-42** | new | accepted | `GuiScraperStart.cpp:83`, `:97-133`, `:173-175`, `:215`: SCRAPE FROM updates only the setting; the filters and systems keep the old scraper until the tab is rebuilt |
| EP-43 | **L-43** | new | accepted | `GuiSaveState.cpp:275`: `>=` in a `std::sort` comparator |

**Totals** (counted from the grade column above by `awk`, recorded in `00`): 41 accepted, 1 accepted in part (EP-33), 1 not kept (EP-26). Sixteen new leads (L-28 to L-43).

**What the seat changed in the first reader's work**, beyond the narrowings:
- **The census bug.** The rows count was 23 switches by a parser blind to `/* */`; it is 21.
- **L-16's cause** is withdrawn (EP-4).
- **Moonlight is the slice's largest cluster:** L-05, L-06, L-07 and L-28 to L-33.
- **`GuiSettings`' exits** are three, not two: START, an outside click and the replacing callbacks (L-01, L-34, L-03, L-35).
