I treated the source as evidence about the pin, and the guest records as evidence about the later image. I ran nothing. Items marked **excerpt** depend on trimmed source; where the missing implementation matters, I say so.

## 1. The base

### EP-1 — L-01: **narrowed**

The core defect is real. The destructor is empty; only `close()` calls `save()` and `onFinalize`. Both close-all handlers directly delete the stack (`GuiSettings.cpp:68-95,106-112,133-139`). The header’s “just calls save()” destructor comment is wrong (`GuiSettings.h:24`).

But “no save function runs on any page” is too broad:

- A non-`GuiSettings` page can save in its destructor: `GuiGameOptions` does (`GuiGameOptions.cpp:494-501`).
- Immediate setters retain their changes in memory despite deletion (`GuiSettings.cpp:234-237`).
- The accelerator is not invariably START: FAVORITE SONGS changes it to SELECT (**excerpt**, `GuiFavoriteMusicSelector.cpp:15-16`).
- The metadata editor’s close-all loop is behind its dirty-state question, including a YES path that calls `save()` (**excerpt**, `GuiMetaDataEd.cpp:613-635`).

**A blanket replacement with `close()` is not established safe.** There is a concrete heterogeneous stack: BIOS DETAILS is a `GuiSettings` over a `GuiBios`, which derives directly from `GuiComponent` (`GuiBios.cpp:251-280`; `GuiBios.h:15`). `GuiSettings::close()` is not a common virtual closing protocol (`GuiSettings.h:26-27`).

The claimed finalizer that pushes a reboot page is **outside the packet**. The supplied scraper finalizer only saves Settings (`GuiScraperStart.cpp:26`). Nevertheless, a close-all implementation must specify what happens to pages pushed by finalization, rather than immediately processing those new pages too.

**Change:** Retain the defect, qualify its scope, and replace “close each page” with a type- and lifetime-aware close-all design and mixed-stack/finalizer regression tests. The isolated harness does not establish that design’s safety.

### EP-2 — L-02: **narrowed**

The LED page does not persist its own changes. Its callback runs the command and calls only `SystemConf::set`; no save function is registered (`GuiAnalogSticksLedControls.cpp:62-88`). Therefore its normal `GuiSettings::save()` returns before either store is flushed (`GuiSettings.cpp:83-95`).

However, **“never reaches `system.cfg`” and “reset at every restart” are wrong as unconditional claims**. `SystemConf::set` records a pending global change, and a later `saveSystemConf()` can write it (**excerpt**, `SystemConf.cpp:439-460,285-305`). Another settings page with save functions performs that flush (`GuiSettings.cpp:91-95`). The supplied parent-menu excerpt even contains such a save function, although its complete gating is not shown (`GuiMenu.cpp:2192-2194`).

**Change:** Say “the LED page does not save; persistence depends on a subsequent flush.” The fixture proves that isolated page defect, not every complete exit/restart route. Whole-application shutdown persistence is **outside the packet**.

The synchronous command per slider movement is independently confirmed (`GuiAnalogSticksLedControls.cpp:77,81-87`).

### EP-3 — L-03: **narrowed** — excerpt

Replacing the relay page without saving is confirmed (`GuiNetPlaySettings.cpp:156-187`; `GuiSettings.cpp:68-95`). It affects more than ENABLE NETPLAY: the three lobby/display switches and INDEX NEW GAMES AT STARTUP also use deferred save functions (`GuiNetPlaySettings.cpp:38-45`; `GuiSettings.cpp:408-413`).

Conversely, HOST, PORT, NICKNAME and CUSTOM RELAY SERVER use immediate in-memory setters, so their edited values are not necessarily discarded by replacement (`GuiNetPlaySettings.cpp:26,33-34,191`; `GuiSettings.cpp:234-243`).

The ENABLE NETPLAY saver begins at `GuiNetPlaySettings.cpp:52-53`; its body is **outside the packet**. G08 supplies the image-level loss observation.

The shown `OptionListComponent` paths do return immediately after the callback, and the callback is the last operation in `onSelectedChanged()` (`OptionListComponent.h:310-311,323-324,632-634`). That supports the narrow statement about those functions—not a complete lifetime proof for the omitted popup and parent dispatch paths.

**Change:** Include the four additional deferred switches; distinguish them from immediate text edits.

### EP-4 — L-16: **refuted as stated** — excerpt

A value is **not counted as changed merely because it equals a default**.

The setters compare against the current map: an existing equal value returns false (`Settings.cpp:645-654,670-686`). Default-value omission during serialization is a separate operation; it does not erase the current value or itself dirty Settings (`Settings.cpp:495-502`). `saveFile()` merely tests the dirty flag (`Settings.cpp:469-474`).

An absent numeric entry—or an absent, nonempty string—can be inserted and marked changed even if that value happens to equal a declared default. But the initial map population is **outside the packet**. That conditional possibility does not establish the first reader’s explanation of G03.

The scraper does call `save()` on tab transitions (`GuiScraperStart.cpp:34-37`), but that does not imply a file write on every transition (`GuiSettings.cpp:85-95`; `Settings.cpp:471-472`).

**Change:** Retain the two image mtimes as observations. Remove the asserted causal explanation at the pin until a test records the actual keys and old/new in-memory values that set `mWasChanged`.

### EP-5 — L-25: **confirmed** — excerpt

The port is genuinely seeded when its current value is empty (`GuiNetPlaySettings.cpp:17-19`). This is an immediate in-memory write, not an unconditional write at page construction; persistence still requires a flush (`SystemConf.cpp:439-460,285-305`).

**Change:** None beyond retaining that distinction. This is a record of behavior, not by itself a defect.

### EP-6 — L-04: **confirmed**

PLAYER PASSWORD passes `password=false`, and the default store is SystemConf (`GuiGameOptions.cpp:204`; `GuiSettings.h:84`). The builder consequently displays the value rather than its row mask (`GuiSettings.cpp:190-193`).

Also, the positive “the scraper’s secrets are masked” should mean **masked on their rows**. The builder conditionally clears the editor’s initial data under the security setting, then opens an ordinary text editor (`GuiSettings.cpp:243-254`). Those editor implementations are **outside the packet**; the flag alone does not prove editor confidentiality.

**Change:** Keep L-04; avoid extending the scraper-row masking positive to every credential sink.

## 2. The fork’s pages

### EP-7 — L-08: **confirmed**

The additional outcome is explicit: `SKIPPED - YOU CANCELLED IT` (`GuiScraperRun.cpp:138-144`). The preceding comment argues for it but does not constitute a register decision (`GuiScraperRun.cpp:132-137`).

Against the supplied D-UI-028/D-UI-030 vocabulary, the first reader correctly identifies a decision requiring disposition.

**Change:** Keep it as a vocabulary decision, not an execution failure.

### EP-8 — L-09: **narrowed**

For `finished=true`, `failed=false`, and `done==errors>0`, the outcome is COULDN’T FINISH, the counts show zero scraped, and both the explanation and next-step rows are empty (`GuiScraperRun.cpp:142-143,194-197,225-233`).

That is an incomplete failure outcome—not a failure presented as success. The missing explanation also affects partially successful runs with per-game errors but no run-level failure (`GuiScraperRun.cpp:225`).

The harness control is not necessarily suitable product wording: “NO MATCH” invents a cause not established by these fields, and asking to apply changes when zero games succeeded is not useful recovery.

**Change:** Retain the missing why/recovery finding, narrow its family description, and require truthful retry guidance rather than merely nonempty rows.

### EP-9 — L-10: **confirmed**

Every nonzero event dismisses a finished run, without checking its input type or mapping (`GuiScraperRun.cpp:90-102`). An axis event therefore qualifies.

There is another facet of the same defect: dismissal does not require `mShownFinished`. Input can observe `p.finished` and delete the page while that member is still false—before `update()` has prepared the terminal display (`GuiScraperRun.cpp:94-101,205-210,217-235`). Restricting dismissal to buttons alone would not address that case.

The comment saying SCRAPER remains immediately behind is also wrong: the caller closes it after starting the run (`GuiScraperRun.cpp:87-89`; `GuiScraperStart.cpp:486-493`).

**Change:** Extend the acceptance test to a completion arriving before the first terminal frame. `ThreadedScraper::progress()` synchronization and whether `stop()` blocks are **outside the packet**; no claim about either is justified here.

### EP-10 — L-12: **narrowed** — excerpt

The loss of command status is confirmed: `executeEnumerationScript()` ignores `pclose()`’s result, and `getBiosInformations()` returns only parsed systems (`ApiSystem.cpp:2233-2252,886-924`).

An empty result gets THE BIOS CHECK RETURNED NOTHING (`GuiBios.cpp:183-202`). That does not explicitly claim a clean check; it conflates failed, unavailable and genuinely empty results and supplies no failure-specific recovery.

**Change:** Keep the status-loss finding, but stop describing this particular empty screen as success. There is a stronger, actual false-success variant in EP-39 below.

### EP-11 — L-13: **narrowed**

The silence is real on all relevant branches:

- A negative free-slot result has no outcome.
- A `false` copy result has no outcome.
- A `true` result queues recording and rebuilds the grid without a success indication (`GuiSaveState.cpp:513-529`).

At the pin, disk-copy failure generally follows the **true** branch: `copyToSlot()` ignores both `copyFile()` results and returns true (**excerpt**, `SaveState.cpp:231-238`). The early false path is different, including a missing source (`SaveState.cpp:215-219`).

The interface-thread copy is explicit (`GuiSaveState.cpp:494-516`). The rebuild clears the grid and adds START NEW GAME first (`GuiSaveState.cpp:245-248,281`). But “the new tile is off-screen” is a property of G06’s layout/state count, not every successful copy.

One further correction: “PLAY starts no process or file work” cannot be concluded from this page. It invokes a callback (`GuiSaveState.cpp:418-426`), and the supplied caller invokes `ViewController::launch()` (`GuiGameOptions.cpp:152-157`). The downstream launch work is **outside the packet**.

**Change:** Preserve the silent-result and synchronous-work defects; distinguish return paths, and qualify the identical-frame and launch-cost claims.

### EP-12 — L-14: **confirmed** — excerpt

An open failure other than ENOENT is reported as held; any unsuccessful non-interrupted `flock` is also reported as held (`AtomicFileUtil.cpp:440-449`). The manager turns that uncertainty into a categorical running-sync sentence (`GuiSaveState.cpp:33-34`).

**Change:** Keep “fails closed, wrong explanation.” Do not reduce the issue solely to EACCES: the helper also conflates other open and lock failures with contention.

### EP-13 — L-15: **narrowed**

The representation cannot distinguish a remembered empty selection from no remembered selection (`GuiScraperStart.cpp:166-193,202-209`). An untouched default selection is also saved, and subsequently excludes newly listed systems while an old remembered system still matches (`GuiScraperStart.cpp:172-193,202-209`).

Two qualifications matter:

- The condition is `currentSystem.empty()`, not literally “opened from the main menu”; `currentSystem` depends on the underlying ViewController state (`GuiScraperStart.cpp:145-158,181,202`).
- The fallback selects eligible listed systems with platform IDs, not every system (`GuiScraperStart.cpp:173-195`).

**Change:** Keep both persistence defects with those conditions stated precisely.

### EP-14 — L-26: **narrowed**

BIOS CHECK has no render override or explicit early-help rendering, despite defining help prompts (`GuiBios.h:15-43`; `GuiBios.cpp:313-324`). This contrasts with the explicit full-screen rendering in the manager and scrape page (`GuiSaveState.cpp:397-398`; `GuiScraperRun.cpp:173-174`). G05/G12 corroborate the missing bar on the image.

But **REFRESH is not wholly undiscoverable**: there are visible REFRESH and BACK buttons (`GuiBios.cpp:79-85`). It is the START shortcut, and the DETAILS help, that the missing bar fails to advertise.

The Window suppression implementation is **outside the packet**; the source shape plus image evidence supports the finding, not an independently reconstructed Window rendering trace.

**Change:** Keep the missing-bar fix, correct the discoverability wording, and make the new prompts follow focus: the current DETAILS test only checks whether `mBios` is nonempty, even though focus can be on the buttons (`GuiBios.cpp:77,85,319-322`).

### EP-15 — L-27: **narrowed**

The naming inconsistency is confirmed: the fallback is `proper(shortName)`, replaced with a full name only when a matching loaded system is found (`GuiBios.cpp:143-155`).

The code does **not** test whether that system has games; it tests membership in `sSystemVector`. The same distinction affects its `hasGames` sorting flag (`GuiBios.cpp:149-155,177`).

**Change:** Describe this as “loaded-system lookup versus short-name fallback,” not an exact games/no-games distinction.

## 3. The commands

### EP-16 — L-05: **confirmed**

The host enters through an unrestricted text row and is inserted bare into the quit and pairing command templates (`GuiMoonlight.cpp:283-284,304-308,341`; `GuiSettings.cpp:234-254`). `executeScriptLegacy()` passes the resulting string to `popen()` (**excerpt**, `ApiSystem.cpp:2263-2269`). The PIN, unlike the host, is generated as four digits (`GuiMoonlight.cpp:270-271`).

**Another command construction was missed:** network-supplied application titles and the host are written into executable shell text at `GuiMoonlight.cpp:223-239`. EP-28 details it. Counting immediate process-start calls does not cover generated scripts.

The “Bluetooth/storage arguments are safe by shape” conclusion is not independently supported here. The Bluetooth excerpt extracts an arbitrary `id` string and forwards it to a backend (`GuiBluetoothDevices.cpp:52-61`; `GuiBluetoothDeviceOptions.cpp:59-64`). The storage excerpt checks nonempty selections (`GuiInstallStart.cpp:74-78`). Their complete validation and command-building implementations are **outside the packet**; do not claim either injection or safety without them.

**Executor assessment:** `WifiScanProcess.h` is a sound shell-free model for the shown API: argv construction, low-fd relocation, process-group creation, cancellation, output cap, deadline and checked cleanup are present (`WifiScanProcess.h:79-125,135-183`). Two positive claims need precision:

- Nonzero child exit codes are preserved; **not every failure returns −1** (`WifiScanProcess.h:184-185`).
- The two-second reap is a bounded attempt, not a guarantee that every child has been reaped when cleanup reports failure (`WifiScanProcess.h:50-60`).

It also inherits `environ` and searches PATH; trusted executable selection remains the caller’s responsibility (`WifiScanProcess.h:125`).

**Change:** Expand the command audit to generated launchers and qualify the unseen backend claims.

### EP-17 — L-06: **confirmed**

The quoted tilde is literal shell text, so the two Qt-directory commands do not target the user’s home directories (`GuiMoonlight.cpp:330-333`). Their results are ignored before the success message.

The embedded branch expands its unquoted tilde, but it too reports success without checking the removal (`GuiMoonlight.cpp:335-336`).

**Change:** Keep the finding. Correct paths alone are insufficient: the outcome must depend on cleanup succeeding. The code shown performs local cleanup, not a verified server-side revocation.

## 4. The dialogs

### EP-18 — L-19: **confirmed** — excerpt

The landing rule is read correctly: the sole button; otherwise the first button whose uppercased displayed text matches translated OK or NO; otherwise the last button (`GuiMsgBox.cpp:116-134`). There is no preference for CANCEL.

Thus back invokes controller mapping’s OK callback, which opens `GuiDetectDevice` (`GuiControllersSettings.cpp:76-83`).

**Change:** Keep the finding. Merely reordering OK/CANCEL, or adding CANCEL after a NO, does not generally fix this label-based accelerator rule.

### EP-19 — L-20: **confirmed** — excerpt

The three-button metadata dialog lands on NO. That callback performs the save without copying external files and deletes the editor; CANCEL has no callback (`GuiMetaDataEd.cpp:524-528`; `GuiMsgBox.cpp:123-133`).

**Change:** None to the finding. Back must explicitly select the non-saving cancellation behavior, not rely on button order.

### EP-20 — L-21: **confirmed** — excerpt

Both SAVE CHANGES dialogs discard on back:

- Metadata: NO invokes the closing function without saving (`GuiMetaDataEd.cpp:613-632`).
- Key mapping: NO deletes the dirty editor (`GuiKeyMappingEditor.cpp:489-501`).

There are **four risky call sites across three leads**, not literally three landings.

The table also already records another acting NO: cancelling DELETE COLLECTION deletes the game-options page (`GuiGameOptions.cpp:630-654`). That is an additional navigation effect, not collection deletion, so it should not be classified as a destructive-file landing. The single-button wizard acknowledgements likewise run closing callbacks; their existence does not make every acting callback unsafe (`GuiBackup.cpp:61-64`; `GuiInstall.cpp:62-65`).

**Change:** Correct the count/terminology and distinguish destructive, saving and navigation-only callbacks. No further destructive landing is established by the supplied excerpts.

## 5. The threads

### EP-21 — L-22: **confirmed**

This is a real data race, not merely a questionable coding style. The worker writes `result` and the plain `mRunning`; the interface reads both without synchronization (`GuiLoading.h:92-98,110-114,132,140`).

The destructor’s join does not rescue it: `result` is copied **before** deletion invokes that join (`GuiLoading.h:98-100,48-52`). The text mutex protects text, not these publications (`GuiLoading.h:54-65,116-128`).

The allocated `std::thread` object is also never deleted (`GuiLoading.h:39,48-52`).

**Change:** Keep the finding; repair publication and thread ownership together. The supplied atomic control addresses publication, not the heap-object leak. “Benign so far” is not a technical mitigation for undefined behavior.

### EP-22 — L-17: **narrowed**

The worker accesses the option components, invokes filters capturing the page, and changes `mOverwriteMedias` (`GuiScraperStart.cpp:97-100,475-478,513-518`).

But those facts alone do **not** prove a second race independent of L-22: the overwrite write and subsequent read occur on that worker, and the supplied path does not show simultaneous user mutation of those components. The claimed modal input-routing guarantee is **outside the packet**.

**Change:** Keep this as thread-affinity/lifetime brittleness. Snapshot selections on the interface thread and make the worker’s filter/overwrite state independent of page objects; do not label every component read a proven race.

Also correct “all 18 completions hold raw `this`”: BIOS’s initial loader captures only `window` (`GuiBios.cpp:43-45`). Ownership must be graded per call site.

The lifecycle and join/detach implementations for the other upstream workers are largely **outside the packet**. The shown fragments do not establish that they are sound. There are additional concrete viewer problems in EP-40 and EP-41.

### EP-23 — L-18: **narrowed** — excerpt

The library walk is confirmed (`DisplayAspect.cpp:74-87`), reached through the tile decorator (`GuiImageViewer.cpp:281-286`).

It is not confined to “the viewer’s first tile”:

- The single-image zoom path also calls it (`GuiImageViewer.cpp:675-681`).
- The index is rebuilt after `forgetScreenshots()` (`DisplayAspect.cpp:66-71`).
- `buildStems()` runs before testing whether the parsed screenshot content is empty, so a first uncached non-screenshot path can trigger it (`DisplayAspect.cpp:113-119`).

**Change:** Describe “first uncached lookup after invalidation,” keep timing unmeasured, and do not simply move the global `SystemData` traversal to a worker without a safe snapshot or synchronization plan.

## 6. The words and the map

### EP-24 — L-07: **confirmed**

The title is a raw literal, while the menu entry is translated (`GuiMoonlight.cpp:268`; **excerpt**, `GuiMenu.cpp:5758`). The four sentence-case messages, including “Succesfully,” are present (`GuiMoonlight.cpp:295,315,333,336`).

A PIN is generated anew at construction; uniqueness between openings is not guaranteed (`GuiMoonlight.cpp:270-271`).

**Change:** Keep the localization and spelling findings. Say “regenerated,” not “necessarily different.” Map membership is addressed separately below.

### EP-25 — L-11: **narrowed**

The summary is assembled from individually translated fragments and fixed ordering (`GuiBios.cpp:220-230`). That prevents sentence-level reordering and correct count-dependent agreement. G12’s singular MANQUANT is image evidence of the resulting problem.

“English word order” is imprecise: “7 sur 7 manquants” is not inherently an English construction. The demonstrated defect is fragmented translation and missing plural agreement.

**Change:** Use a translatable count-bearing sentence/plural form; describe the linguistic defect accurately.

### EP-26 — L-23: **narrowed** — excerpt

The supplied `GuiAutoScrape` fragment shows executable implementation, not whether it belongs to a build target (`GuiAutoScrape.cpp:60-86`). `es-app/CMakeLists.txt`, other build lists and complete caller information are **outside the packet**.

A zero textual grep in one CMake file does not by itself exclude globbing or another source list.

**Change:** Preserve the reported inventory correction as first-reader/tool evidence, but support “not built” with the actual target source enumeration or build graph. I cannot independently confirm that conclusion from this packet.

### EP-27 — L-24: **narrowed**

The two fork titles and Moonlight’s raw title are directly established (`GuiBios.cpp:65`; `GuiScraperRun.cpp:28`; `GuiMoonlight.cpp:268`). The map, declarations and checker patterns are **outside the packet**. Their membership verdicts therefore remain supplied generator results, not independently verified source findings.

Several surrounding architectural/census statements need correction:

- Three added **files** are not three added pages: `GuiScraperRun` is one page, while `WifiScanProcess` is an executor (`GuiScraperRun.h:24`; `WifiScanProcess.h:22-28,74`).
- “One page/class per file” is not literal: the viewer file also defines a zoomable image page and video viewer (`GuiImageViewer.cpp:19,274,729`).
- Two of the 23 tabulated switch sites are commented out. The table therefore has 21 active switch sites, not 23 (`GuiScraperStart.cpp:370-376`).
- The two `atof` calls at `GuiGamelistOptions.cpp:389` parse grid dimensions, not ratings (**excerpt**, `GuiGamelistOptions.cpp:381-389`).

Nor does “opened from a settings page” establish help-bar rendering. BIOS itself demonstrates the distinction between defining prompts and drawing them (`GuiBios.cpp:313-324`; `GuiSaveState.cpp:386-398`).

**Change:** Retain the proposed map work, but correct those semantic claims. Count assertions and constructed drift tests do not validate whether counted code is active or what it does.

## New items

### EP-28 — new: **new — shell injection in generated Moonlight launchers**

**Family:** a command built from a player’s string.

Application titles come from the server’s XML. Only `/` is replaced in the filename; both filename and title are then embedded inside shell double quotes, and the host is embedded bare (`GuiMoonlight.cpp:223-239`). Double quotes do not neutralize command substitution, backticks or embedded quotes.

This is a network-supplied command-construction path, beyond L-05’s directly typed host.

**What would prove it:** Generate a launcher from a synthetic title such as `$(touch t31-canary)`, execute it in an isolated temporary directory with doubled executables, and observe the canary. The distribution’s complete `.sh` launch configuration is **outside the packet**; that is needed for an end-to-end device exploit claim.

**Change:** Add this finding and cover every generated argument, not just the three immediate command templates.

### EP-29 — new: **new — Moonlight deletes the working library before fetching its replacement**

**Family:** a state write that can lose the record.

`UpdateMoonlightGames()` removes existing images and top-level Moonlight files before fetching or validating the new application list (`GuiMoonlight.cpp:174-184`). A network or XML failure then returns false, after the old launchers/gamelist have already been removed. The UI reports only inability to connect (`GuiMoonlight.cpp:287-295`).

**What would prove it:** Seed a working launcher, gamelist and image; make the fetch return empty or malformed XML; verify the old files were removed.

**Change:** Add a transactional replacement requirement: obtain and validate the new list, build a replacement, and preserve the previous working set on failure.

### EP-30 — new: **new — Moonlight reports import success despite failed writes**

**Family:** a check whose failure reads as success.

Launcher streams are not checked, `gamelist_doc.save_file()` is ignored, and the function returns true (`GuiMoonlight.cpp:230-240,256-257`). Box-art writing likewise returns true regardless of the request’s result (`GuiMoonlight.cpp:167-171`). The GUI interprets true as grounds to quit/restart (`GuiMoonlight.cpp:291-293`).

**What would prove it:** Supply valid application XML while making output writes fail on a read-only/full target. Assert that the function currently returns true and the UI takes its success route.

**Change:** Add checked output/commit results and an honest failure outcome, separately from the pre-deletion defect.

### EP-31 — new: **new — Moonlight’s version probe reads a pointer, not command output**

**Family:** a check whose failure reads as success.

`ss << mlver` inserts the `FILE*` value, not the subprocess’s bytes. Searching that representation for “Embedded” does not identify the client (`GuiMoonlight.cpp:40-50`). The opened stream is also never passed to `pclose()`.

Consequently, the normal pairing route chooses the non-embedded command; the host harness’s two pairing templates do not prove both branches are reachable through this helper (`GuiMoonlight.cpp:303-306`).

**What would prove it:** Return an “Embedded” version line from a controlled `moonlight -v`; assert that `isEmbedded()` still returns false. Repeated calls can separately measure leaked stream descriptors.

**Change:** Add this functional check failure and resource leak; use a checked, bounded output reader.

### EP-32 — new: **new — Moonlight credential parsing can hang or throw on the interface thread**

**Family:** work on the interface thread.

`extractClient()` loops until it finds a certificate marker without checking whether `getline()` reached EOF or failed (`GuiMoonlight.cpp:54-61`). An existing empty/truncated configuration therefore makes the loop nonterminating. Its escape-decoding loop also calls `replace()` without guarding against `find()` returning `npos` (`GuiMoonlight.cpp:69-74`).

This parsing runs in the pairing output callback (`GuiMoonlight.cpp:308-325`), which `executeScriptLegacy()` invokes synchronously while reading the child (**excerpt**, `ApiSystem.cpp:2278-2287`).

**What would prove it:** Use an empty configuration and a watchdog around the callback; separately supply a malformed certificate line without an escaped newline and test that it does not throw.

**Change:** Add explicit EOF/format/error handling. I do not infer the masked key-search predicate at `GuiMoonlight.cpp:86-87`.

### EP-33 — new: **new — the extracted Moonlight private key lacks an explicit privacy policy**

**Family:** a credential’s sink.

The private-key output is created with an ordinary `ofstream`, then populated from the configuration (`GuiMoonlight.cpp:79-100`). It is subsequently supplied as the TLS client key (`GuiMoonlight.cpp:145-147`). No restrictive mode enforcement appears in that writer.

Actual exposure depends on the process umask, existing file mode and parent-directory permissions; those are **outside the packet**. This is not proof that the image’s key is publicly readable.

**What would prove it:** With a synthetic key, test creation under umask 022 and replacement of an existing permissive file; inspect file and directory modes and test access from the relevant unprivileged identity.

**Change:** Add this sink to the credential audit and enforce an explicit private mode rather than relying on ambient permissions.

### EP-34 — new: **new — outside-click dismissal also bypasses settings saving**

**Family:** a state write that can lose the record.

A left click outside the menu directly deletes the page (`GuiSettings.cpp:456-461`), bypassing exactly the save/finalize contract identified in L-01 (`GuiSettings.cpp:73-95`).

**What would prove it:** Change a deferred switch, deliver an outside-menu click, and compare store/finalizer calls with the BACK control.

**Change:** Include this exit in the base fix. Repairing START alone leaves another divergent close path.

### EP-35 — new: **new — SHOW CONTROLLER ACTIVITY drops other pending controller settings** — excerpt

**Family:** a state write that can lose the record.

The activity callback writes its own setting, deletes the page and rebuilds it without saving (`GuiControllersSettings.cpp:200-211`). Other controls are deferred, including AUTOCONFIGURE RETROARCH HOTKEYS and SHOW CONTROLLER NOTIFICATIONS (`GuiControllersSettings.cpp:66-71,198`; `GuiSettings.cpp:408-413`).

**What would prove it:** Change one of those deferred controls, toggle activity, and inspect the rebuilt control and persisted value.

**Change:** Add this sibling of L-03; the relay page is not the only replacement callback that drops pending edits.

### EP-36 — new: **new — text-only settings pages do not flush their own edits**

**Family:** a state write that can lose the record.

The text-row builder writes immediately to memory but registers no save function (`GuiSettings.cpp:218-258`). Moonlight’s constructor installs text/actions but no save hook (`GuiMoonlight.cpp:278-343`), so the shown base save path has nothing to run.

There is another visible instance: the game-options NETPLAY page has its only explicit save function inside `!adhocEnabled`; with ad-hoc enabled, its nickname/password edits have no such hook (`GuiGameOptions.cpp:203-216`).

**What would prove it:** Test each page in isolation: edit text, close with BACK, and assert a store flush. Then restart the test process and check the value. Parent or later global flushes must be excluded from that proof.

**Change:** Extend L-02’s architectural lesson beyond LEDs. Say “does not persist on its own close,” not “can never be persisted.”

### EP-37 — new: **new — reopening a non-config text editor starts from stale text** — excerpt

**Family:** a state write that can lose the record.

`addInputTextRow()` captures the original `value` and reuses it each time the editor opens (`GuiSettings.cpp:321-334`). Its successful update changes the displayed row and calls `onsave`, but does not update that captured value (`GuiSettings.cpp:301-317`).

The keyboard-to-pads caller uses this builder to edit the joystick’s actual name (`GuiKeyboardtopads.cpp:168`).

**What would prove it:** Change name A to B, reopen the editor, and press OK without editing. It starts from A and can write A back over B.

**Change:** Keep a current unmasked value or use a getter. Do not repair this by rereading the masked display text.

### EP-38 — new: **new — COPY’s transfer-lock check does not hold exclusion across the write** — excerpt

**Family:** a state write that can lose the record.

The manager probes the transfer lock and later performs the copy (`GuiSaveState.cpp:499-516`). The probe explicitly closes its descriptor and releases any acquired lock (`AtomicFileUtil.cpp:440-449`). The shown `copyToSlot()` contains no enclosing lock (`SaveState.cpp:213-238`).

Thus the shown gate is a check-then-write window, not proof of D-CLOUD-053 exclusion. A lower-level filesystem operation independently taking the transfer lock would change that conclusion; its implementation is **outside the packet**.

**What would prove it:** Pause after the probe, acquire the transfer lock from another process, then resume the copy and detect whether it writes while that lock is held.

**Change:** Require a retained lock around the actual copy/record operation, or demonstrate the lower-layer guard. Checking twice does not remove this race.

### EP-39 — new: **new — a partially failed BIOS command can produce ALL PRESENT** — excerpt

**Family:** a check whose failure reads as success.

The enumeration helper retains stdout while discarding exit status (`ApiSystem.cpp:2239-2252`). The BIOS parser accepts and returns systems from that output (`ApiSystem.cpp:889-924`). A header with no parsed file rows yields zero missing/untested files and therefore ALL PRESENT (0); partial PRESENT-only output likewise produces an apparently clean system (`GuiBios.cpp:158-162,210,220-223`).

**What would prove it:** Shadow the command with one that prints a system header—or a header and one PRESENT record—then exits nonzero. Assert that the UI must not report a completed clean check.

**Change:** Add this stronger variant to L-12. Checking only whether the returned vector is empty is insufficient.

### EP-40 — new: **new — the image viewer’s global “running” flag is neither synchronization nor a lifetime token**

**Family:** work on the interface thread, including worker/UI lifetime.

A plain global bool is written by construction/destruction and read in thread-pool jobs (`GuiImageViewer.cpp:272-277,365-374,501-510,550-552`). That is an unsynchronized worker/UI flag.

It also guards the wrong identity: queued callbacks retain an old viewer’s `this`, but opening a different viewer sets the same global flag true again. The old callback can then pass its test and address the old grid (`GuiImageViewer.cpp:371-377,507-512`).

**What would prove it:** Use ThreadSanitizer for the flag; then delay a posted callback, destroy viewer A, construct B, and deliver A’s callback under AddressSanitizer. ThreadPool shutdown and Window queue invalidation details are **outside the packet** and must be included in the production reproduction.

**Change:** Add an instance-specific lifetime/generation guard. Making the global bool atomic fixes only the race, not the identity error.

### EP-41 — new: **new — failed first-page extraction abandons the viewer**

**Family:** work on the interface thread, specifically completion ownership.

The PDF/CBZ viewer is allocated before being pushed (`GuiImageViewer.cpp:692-712`). It is pushed only by successful first-extraction completions. Both completions simply return on an empty result without deleting the viewer or presenting an error (`GuiImageViewer.cpp:390-399,536-545`).

For multi-page inputs, the thread pool has already been allocated and started (`GuiImageViewer.cpp:359-382,494-517`).

**What would prove it:** Report a positive page count/list but fail the initial extraction. Count viewer/pool destruction and inspect the resulting GUI stack.

**Change:** Add explicit ownership and cleanup for the not-yet-pushed viewer on failure. This is distinct from #1212’s callback-to-destroyed-page shape.

### EP-42 — new: **new — changing SCRAPE FROM leaves checks bound to the old provider**

**Family:** a check whose failure reads as success/no work.

The page builds media filters using the current scraper object, date filters using its name, and the supported-system list using that scraper (`GuiScraperStart.cpp:83,97-100,126-133,173-175`). Changing SCRAPE FROM only updates Settings; it does not rebuild those dependencies (`GuiScraperStart.cpp:215`).

The subsequent search therefore still uses the old filters and system list (`GuiScraperStart.cpp:475-478,510-518`), potentially treating work needed by the new source as already satisfied or reporting NO GAMES FIT THAT CRITERIA (`GuiScraperStart.cpp:482-483`).

**What would prove it:** Use two scraper doubles with different supported systems, scrape dates and missing-media answers. Switch sources without a tab round trip and inspect the resulting queue.

**Change:** Add this functional selection bug; snapshotting worker inputs alone will not fix stale provider dependencies.

### EP-43 — new: **new — incremental save-state sorting violates `std::sort`’s comparator contract**

**Family:** work on the interface thread.

The grid rebuild passes a comparator using `creationDate >=` to `std::sort` (`GuiSaveState.cpp:268-278`). Equal dates make that branch true in both directions, violating strict weak ordering. This can make an ordinary synchronous grid rebuild undefined behavior.

**What would prove it:** Exercise incremental states with equal timestamps and assert comparator irreflexivity and asymmetry; then run the real sort under a checked/debug standard library.

**Change:** Add the defect and use a strict comparison, with a stable tie-break if required. This is not a request merely to move the unsafe sort onto a worker.

## Highest priorities

1. **EP-28 and EP-16 — command construction.** The generated-script path expands the concern from a self-entered host to network-provided shell text (`GuiMoonlight.cpp:223-239`).
2. **EP-29, EP-38 and EP-11 — preservation of working data.** These concern deleting the working Moonlight library before replacement, incomplete copy exclusion, and untruthful copy results—not cosmetic outcomes.
3. **EP-1, EP-34 and EP-35 — closing/rebuilding pages loses choices.** Fix the shared contract, but do not introduce a generic close-all loop that mishandles heterogeneous pages or finalizer-created UI.
4. **EP-21 and EP-40 — concurrency/lifetime correctness.** The demonstrated publication race and the viewer’s non-instance lifetime guard deserve more weight than “benign so far.”
5. **EP-32 — unbounded parsing on the interface thread.** A persistent truncated configuration can turn pairing into an unrecoverable interface hang until the process is stopped.