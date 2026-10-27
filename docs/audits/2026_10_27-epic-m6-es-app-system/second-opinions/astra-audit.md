I treated the harness results as proofs of their constructed cases, not of every caller’s reachability. The guest results remain **image** evidence, not an end-to-end execution of the pin. Upstream and neighbour conclusions below are **excerpt-based**; missing decisive code is identified as **outside the packet**.

## 1. Game-list reads and writes

### EP-1 — L-05 / 3.13 — **confirmed**

The destructive cached-miss branch is real, **conditional on a remembered miss and a dirty entry that produces an update**. `updateGamelist` collects dirty files, skips the write when none exist, and otherwise uses cached `exists` to choose between loading the existing document and constructing an empty root (`Gamelist.cpp:394-428`). It then writes that document over the selected destination (`Gamelist.cpp:466-477`).

The earlier lookup is **not “none”**: `SystemData::getGamelistPath` probes both the ROM-side path and the fallback path through cached `exists` (`SystemData.cpp:1652-1658`). `updateGamelist` calls it at **`:411`**, before `:413`. A visible startup route is `SystemData.cpp:125-126` → `packGamelist` → `getGamelistPath` (`Gamelist.cpp:530`). The ordinary `parseGamelist` implementation connecting startup’s `SystemData.cpp:128` to that resolver is **outside the packet**. Thus the packet identifies the cache-priming operation, but does not independently establish that startup route for every configuration.

**Change:** Keep L-05, but state its prerequisites. Cite `SystemData.cpp:1653`, not `loadGamelistFile`’s regular-file gate, as the earlier cached existence lookup. G-04 supports the occurrence on the later image; its control and the fixture do not justify “every restore is overwritten.”

Also correct the parse-error description: a failed load merely logs and continues with whatever root the document exposes, creating one if necessary (`Gamelist.cpp:416-424`). The safe response to an existing but unreadable/malformed document is not to overwrite it. Uncached reads and atomic writes cannot reconstruct entries an earlier version already lost.

### EP-2 — 3.15 and L-05’s proposed repair — **narrowed**

**`exists(path, false)` at `:413` plus temp-and-rename is not sufficient.**

* The resolver must also stop choosing paths from stale answers. Both candidates are probed in `getGamelistPath`, which is used for the read and again for the write (`SystemData.cpp:1652-1663`; `Gamelist.cpp:411,469`).
* `packGamelist` can remove an existing, restored media reference on a cached miss: the failed existence test directly removes the XML child (`Gamelist.cpp:595-605`).
* `cleanupGamelist` likewise enters its missing-media/repair branch using cached answers and searches replacement paths through more cached probes (`Gamelist.cpp:702-705,730-752`). Its precise old-reference removal at the reported `:762-768` is **outside the packet**.
* Both routines replace the XML in place after removing the previous `.old` and attempting an unchecked copy (`Gamelist.cpp:618-625,837-844`). That is not a verified recovery protocol.

There is another ordering worth resolving: startup calls packing before parsing (`SystemData.cpp:125-128`), packing calls `clearTemporaryGamelistRecovery` (`Gamelist.cpp:625-628`), and parsing later reads recovery files (`Gamelist.cpp:247-249`). The clearing implementation and the omitted middle of packing are **outside the packet**; verify that recovery is incorporated before it can be discarded.

**Change:** Expand the repair and its tests to path selection, destructive media probes, malformed input, backup/recovery handling, and the same-entry merge defect in EP-36. Atomic replacement prevents torn publication; it does not make an incorrect document correct.

### EP-3 — 3.12 — **narrowed**

The excerpt shows metadata serialization receiving `relativeTo` and `fullPaths`, and the resulting game path being emitted (`Gamelist.cpp:255-261,280-283`). The decisive game-path calculation, including the reported `:279`, is **outside the packet**. I cannot independently certify the floor’s complete relative-path verdict.

The separate writer defect is visible: `saveToXml` removes the destination before attempting `save_file` (`Gamelist.cpp:303-311`). A failed save can therefore destroy a previous recovery record.

**Change:** Retain the relative-path case as a test obligation, not independent proof from this excerpt. Include the recovery writer in last-good-state work; fixing only `updateGamelist` leaves this remove-before-save operation intact.

### EP-4 — 3.14 — **narrowed**

The first reader should not attribute every skipped entry to cached `exists`. For a file load, the initial gate is extension plus `isRegularFile` (`Gamelist.cpp:112-117`). Later, creating a file missing from `fileMap` is permitted only on the **`!fromFile`** branch (`Gamelist.cpp:185-195`).

The path-reading/normalization code containing the reported `:177` is **outside the packet**, so the newline and backslash verdicts cannot be independently closed here. The supplied cache implementation does contain a cached regular-file query (`FileSystemUtil.cpp:238-240`), but the public `isRegularFile` dispatch is also **outside the packet**.

**Change:** Do not describe `:116` as an `exists` call or propose a blind textual substitution there. Test path normalization and uncached file recognition separately, retaining regular-file validation.

## 2. Lifetimes

### EP-5 — L-06 — **narrowed**

The dangerous ordering is present: dynamic population calls `rootFolder->clear()` before `reloadCollection` reloads the bundle view (`CollectionSystemManager.cpp:1112-1117,1573-1589`). The bundle holds the collection’s actual root, not a copy (`CollectionSystemManager.cpp:1301-1302`). Reloading a view reads its cursor and dereferences it (`ViewController.cpp:1140-1143`).

But **the claimed bundled-filter-edit route is not established**:

* When `mSystem` is the bundle, the shown options-page condition explicitly **does not call** `reloadCollection`; it takes `reloadGameListView(mSystem)` instead (`GuiGamelistOptions.cpp:424-427`).
* The cited `ISimpleGameListView.cpp:462` caller is **outside the packet**.
* The implementation of `FolderData::clear` is also outside this excerpt. The fixture demonstrates the free/read mechanism under its ownership doubles, not the missing GUI route.

The first reader’s explanation of G-02 as “the heap’s choice” is wrong. A plain collection does not enter the `filteredIndex != nullptr` repopulation branch (`CollectionSystemManager.cpp:1573`); that guest action did not exercise this alleged failure.

**Change:** Keep a conditional lifetime finding, but withdraw “proved bundled filter-edit crash” until the actual caller path is established. Drop/remake must occur before deletion for every affected view, including non-bundled views. Also address the separate stale-view use in EP-37.

### EP-6 — L-07 — **confirmed**

Cancellation destroys the builder through `searchHandle.reset()` while its worker can still write `mSearchHandle`, `mError`, and `mFinished` (`ScraperSearchComponent.cpp:209-220,358-361`). The non-atomic completion flag is another defect (`ScraperSearchComponent.cpp:225,256`).

The proposed repair needs more than “add a joining destructor”:

* **The first reader is wrong that the thread is never joined.** `update()` already joins it (`ScraperSearchComponent.cpp:230-232`).
* `update()` then loses the allocated thread object by assigning `nullptr` without deleting it (`ScraperSearchComponent.cpp:233`). A destructor cannot recover that pointer.
* A new destructor must not unconditionally join a thread already joined by `update()`. Use one ownership scheme and `joinable()` appropriately, rather than two independent cleanup paths.
* Joining during `stop()` can move the blocking search back onto the interface thread. The code explicitly says request construction can hash a ROM or obtain a token (`ScraperSearchComponent.cpp:195-196`).

**Change:** Own the thread, synchronize completion, and keep the scraper/search inputs alive until completion. Test both cancellation and normal completion. The base and enclosing search-object destruction details are **outside the packet** and must be checked before declaring the ownership repair complete.

### EP-7 — L-12 — **narrowed**

There are five direct posts, at `NetworkThread.cpp:206,237,251,257,266`. Routing them through `AppWindow::post` enforces the closing gate (`AppWindow.h:38-44`).

It does **not** guarantee that a token save runs. `closing()` only prevents subsequent enqueueing; it neither executes nor drains tasks already queued (`AppWindow.h:49-53`). The main loop has already ended when closing is called, and watcher shutdown follows it (`main.cpp:1317-1330`).

Nor does the supplied count fixture prove a use-after-free. The shown ordering puts watcher shutdown before later teardown; the implementation of `WatchersManager::stop` is **outside the packet**.

**Change:** Describe this as a closing-protocol violation, not a demonstrated dangling-window write. If preserving a completed token update at shutdown is required, specify a drain/commit policy: replacing the posting API alone deliberately drops that update instead of saving it.

### EP-8 — L-15 — **narrowed**

The merge helper deliberately preserves identity by full path and hands vanished nodes to the caller for retirement (`FolderMerge.h:15-18,22,48-69`). Its unit tests do not establish that all external holders are retired.

The shown retirement code removes collection entries and a group-folder reference, then deletes the node (`SystemData.cpp:459-473`). It does not show a complete holder audit. In particular, the slice also stores raw game pointers in the screensaver (`SystemScreenSaver.cpp:350-358,378-380`); see EP-38.

**Change:** Keep the helper’s positive verdict, but do not equate three passing merge tests with lifetime closure. Explicitly include screensaver-held pointers in the retirement checklist. The rest of the rescan’s invalidation sequence is **outside the packet**.

### EP-9 — L-24 — **confirmed**, within the stated process-lifetime model

The static points to a member of the allocated `NetworkThread` (`NetworkThread.cpp:19,31-32`; `main.cpp:898`). The object also registers itself for watcher and joystick notifications (`NetworkThread.cpp:43-46`).

**Change:** Retain the warning against simply deleting the allocation. A future ownership repair must unregister callbacks/components, clear the static, and stop relevant work before destruction. “Never free it” is not the architectural rule; “retire every observer before freeing it” is.

The absence of a later deletion cannot be independently proved from the trimmed end of `main.cpp`; that part of the first reader’s process-lifetime account remains supplied evidence.

## 3. Parses

### EP-10 — L-28 / 3.21 — **confirmed**

The first reader’s retrospective correction is right: a mapping with no surviving trigger is not retained (`KeyboardMapping.cpp:293-294`). The forward table’s “action with no trigger” is wrong.

The release-build type hazards are broader than the unknown-name fixture:

* Unchecked string reads: **`:251`, `:254`, `:257`** for type, mode, description.
* Trigger values: **`:265-266`, `:271-272`**.
* Target values: **`:282-283`, `:288-289`**. For non-`key` types, short-circuiting the whitelist check still reaches the unchecked insertion getter.
* An array element is used as an object without an `action.IsObject()` check before `HasMember` (`KeyboardMapping.cpp:246-250`).

Under the supplied `NDEBUG` build condition, those wrong-type accesses are undefined behaviour, not controlled parse failures. A fault is input-dependent; “every malformed value necessarily crashes” would also overstate it.

**The `GetArray` calls themselves are guarded:** `:246` by `:244`, `:263` by `:261`, and `:280` by `:278`. Do not classify all of them as unguarded wild reads. Whether there is a top-level object guard in `:231-238` is **outside the packet**.

There is also partial acceptance: a chord with one known and one unknown trigger can survive with the unknown member removed (`KeyboardMapping.cpp:263-266,293-294`). That changes its meaning, rather than merely dropping a mapping.

**Change:** Separate unknown-name handling from memory safety. Validate objects, field types, array elements and whole actions before accepting them. Add malformed-shape tests compiled with `NDEBUG`; the supplied fixture proves only silent unknown-trigger handling. “Low because outside the lanes” is not an adequate ranking for a player-file memory-safety defect.

### EP-11 — L-27 / 3.9 — **narrowed**

The arithmetic is accurately reported: a positive rating can round to zero stars, while non-positive values become UNKNOWN (`FileFilterIndex.cpp:328-340`). The year predicate accepts only strings of at least four characters beginning with `1` or `2` (`FileFilterIndex.cpp:364-369`).

But the control’s rule—every positive rating must produce at least one star, and years 0999/3000 must be accepted—is a **proposed policy**, not a correctness requirement established by this code. Rounding a known small rating to zero is not inherently the same as treating absent metadata as unknown.

Also, `""` is the intermediate year key at `:367`; the function’s eventual normalization/return path is **outside the packet**. Likewise, `"1 STARS"` is visibly an index key, not independently proved to be the final player-facing wording.

**Change:** Distinguish arithmetic facts from chosen normalization policy. Test malformed values, finite/range handling and complete year validation, not merely a control that encodes the desired new buckets.

### EP-12 — L-17 / 3.41 — **narrowed**

The ID narrowing is real: `jsonInt` casts `GetInt64()` to `int`, and the exposed ID fields remain `int` (`OfflineAchievementsText.cpp:10-20`; `OfflineAchievementsText.h:51,63,110`).

**The epoch claim is wrong as written.** `parsePendingIds` parses the epoch with `strtoll` and casts to **`time_t`**, not `int` (`OfflineAchievementsText.cpp:229-231`). Its remaining risks are conversion overflow and the width/range of the shipped `time_t`, not a demonstrated unconditional 32-bit truncation.

The string-to-integer implementation used for IDs is **outside the packet**. It should not be credited with range validation merely because the input contains digits (`OfflineAchievementsText.cpp:227-232,254-258`).

**Change:** Remove “harmless today.” Out-of-range external input needs a defined rejection/unknown outcome today. Either validate against the actual model’s integer ranges or widen the complete producer/consumer chain; widening only this helper is insufficient.

## 4. Bounds and the interface thread

### EP-13 — L-01 — **confirmed**

The lock chain is real:

1. `checkCheevosTokenSoon` calls `ResetComponent` (`NetworkThread.cpp:21-24`).
2. `ResetComponent` takes `mWatchersLock` (`WatchersManager.cpp:92-100`).
3. The watcher holds that same lock across the entire due-check loop, including `check()` and notification (`WatchersManager.cpp:181-199`).
4. Those checks call account authentication, pad information and update detection (`NetworkThread.cpp:62,95,138`).
5. A visible settings-page callback invokes the reset (`GuiRetroAchievementsSettings.cpp:805-806`); another UI-posted callback does so at `NetworkThread.cpp:257`.

Two cited settings-page callers are wrong at this pin: `GuiRetroAchievementsSettings.cpp:191` is a comment, and `:257` is a weak-pointer test, not a token-reset call.

**Change:** Keep the interface-blocking finding and correct the trace. The actual network/script bounds are **outside the packet**, so distinguish “no bound on this lock acquisition” from a proved infinite HTTPS wait.

Moving `check()` outside the lock also needs lifetime protection: unregistering deletes the `WatcherInfo` (`WatchersManager.cpp:80-86`). A bare unlock around raw registry pointers is not a sufficient repair.

### EP-14 — L-02 — **narrowed**

The full-file reads are visible (`CaptureRotation.cpp:158-163`), but they do not run after **every** RetroArch exit. The caller requires exit code zero, and the helper also requires RetroArch, a record path, an existing log and an acceptable log timestamp (`FileData.cpp:1166-1169`; `CaptureRotation.cpp:139-156`).

Truncating the log at launch prevents accumulation across launches; it does **not** impose a maximum byte count or elapsed read time on a long-running session. There is no size limit at these reads (`CaptureRotation.cpp:158,162`).

**Change:** Describe both reads as size-dependent interface work. Do not mark the log read strictly bounded solely because it is launch-truncated. The guest supplied no launch timing for this path.

### EP-15 — L-04 — **confirmed**, as a cost finding

The first unresolved screenshot builds the stem index under `sShotLock`, walking the eligible systems’ games (`DisplayAspect.cpp:74-87,116-118`). Cached screenshot hits still resolve the game again and obtain its transform under the lock (`DisplayAspect.cpp:102-109`).

The actual complexity of `FindByPath` is **outside the packet**; the visible evidence is its call at `DisplayAspect.cpp:96`, not an independently verified tree-walk implementation.

**Change:** Keep the finding, but retain “not priced.” A four-game library does not validate scalability. Also note that invalidation occurs after recording rotation, not only after library changes (`CaptureRotation.cpp:182-186`).

### EP-16 — L-09 — **narrowed**

The coupling is confirmed: the detached health probe enters `isZaparooEnabled`, which holds `mZaparooLock` while constructing and waiting for the request (`ZaparooSupport.cpp:20-41`). The call site sets only `connectTimeout`; the card-writing call sets no explicit duration bound (`ZaparooSupport.cpp:37-39,58-63`).

The `HttpReqOptions` defaults, `wait()` implementation, and cited game-options callers are **outside the packet**. Consequently, the exact total/stall guarantee cannot be independently established here.

**Change:** Preserve the lock/bound lead, but distinguish explicit options from inherited defaults. Once the defaults are checked, a contained timeout and lock-scope repair should not be dismissed merely because the surface is outside the fork’s feature lanes.

### EP-17 — L-11 — **narrowed**

Cached media existence checks are real (`SystemScreenSaver.cpp:157,164,208,375`). The forward read table is **wrong at `:375`**: this is the selected game’s video/image path, not the title directory (`SystemScreenSaver.cpp:372-376`).

The retry loop picks another candidate on each iteration (`SystemScreenSaver.cpp:157-160`). It is not necessarily ten checks of one path; nevertheless, candidates with cached misses cannot become newly visible through those probes.

The library walk and pointer collection are also visible (`SystemScreenSaver.cpp:342-358`). Their lifetime consequences need the additional review in EP-38.

**Change:** Correct the `:375` row and avoid treating the retries as a freshness mechanism. Do not call all of this harmless outside-lane behaviour: media freshness and retained object lifetime are separate concerns.

### EP-18 — `02`’s bounds table / `03`’s platform summary — **refuted** as an exhaustive account

The table is not “every network or script wait reachable from the 77.” Visible transitive calls include the synchronous fallback scraper searches, installers and Bluetooth/formatting operations (`ScraperSearchComponent.cpp:652,658`; `ContentInstaller.cpp:132-135,206-209`; `ThreadedBluetooth.cpp:41-44,102-105`).

Their implementations and exact bounds are **outside the packet**, but that does not make the call sites disappear. Likewise, “nothing shells out except CloudOffer and Windows residue” is too broad when describing reachable behaviour rather than literal process constructions.

**Change:** Label the generated table as direct constructions plus selected transitive waits, or complete the call graph. Include L-08 in the bounded-work repair for L-07.

## 5. Writes and the cache’s third shape

### EP-19 — L-23 / third cache shape — **confirmed**, conditionally

The raw writers bypass the supplied filesystem-wrapper invalidation contract: custom lists use `std::ofstream`, and filters use `pugi::save_file` (`CollectionSystemManager.cpp:345-357`; `FileFilterIndex.cpp:1313`). An earlier `.xcc` probe exists at `CollectionSystemManager.cpp:962-963`; a custom-list probe exists at `:1145-1147`.

Deletion first probes `.xcc`, falls back to `custom-…cfg` on a miss, and returns false only if the selected path also reads absent (`CollectionSystemManager.cpp:1609-1614`). Therefore:

* a remembered miss followed by a raw write can leave deletion stale;
* a stale `.xcc` miss does **not always mean `return false`**—it may select an existing `.cfg` instead.

Two other corrections are required:

* `.xcc` is written by **pugixml**, not `std::ofstream`.
* A malformed dynamic filter does **not populate every game** on the shown path. Population clears the collection, then enters the all-games traversal only if `load()` succeeds (`CollectionSystemManager.cpp:1114-1124`; `FileFilterIndex.cpp:1152-1158`).

**Change:** Retain the third-cache-shape finding and correct those consequences. Atomic replacement does not inherently invalidate this cache: `AtomicFileUtil`’s implementation is **outside the packet**. Require explicit invalidation, such as the available path reset (`FileSystemUtil.cpp:348-350`), or uncached reads at these mutable-file boundaries.

### EP-20 — L-03 — **confirmed**

The rotation record is written directly and its write outcome is not checked before logging/publishing the new cached value (`CaptureRotation.cpp:174-180`).

The on-disk fallback is useful: records lacking the checked-launch marker fall back to the table (`CaptureRotation.cpp:124-127`). But that is not a complete “benign failure” argument for the running process; EP-40 identifies the missing success check.

**Change:** Use checked atomic publication and update the cache only after success. Preserve the read-old/write-new marker compatibility behaviour rather than describing atomic writing alone as the complete fix.

### EP-21 — `02` read table, `.keys` deletion — **refuted**

The claim that ES’s own `.keys` writes bypass `Utils::FileSystem` is plainly wrong: both writer branches call `Utils::FileSystem::writeAllText` (`KeyboardMapping.cpp:423-429`).

Under the supplied cache contract, those writes invalidate their destination. Thus the specific story “save this mapping through ES, then deletion misses it because that save bypassed invalidation” is not supported (`KeyboardMapping.cpp:324-325`).

**Change:** Remove that example from the third-cache-shape table. External replacement can still make the cached reader stale, and the writes remain non-atomic; those are different findings.

## 6. Words and map

### EP-22 — L-25 / 3.29 — **confirmed**

Six extraction macros exist, while the three additional stable tag names have no corresponding macros (`FileTag.cpp:6-18`). The supplied catalog fixture supports the missing French entries.

**Change:** Add extraction anchors and translations, **not translated values in `defaultTags`**. These names are identifiers used in exact comparisons (`FileTag.cpp:34-38`) and serialized filter values (`FileFilterIndex.cpp:1224-1225,1310-1311`). Localizing the stored keys would break compatibility with existing metadata.

The “196 of 196 msgids have French” result remains valid within its stated scope. It is not a completeness proof for bare or dynamically produced player text; the untranslated scraper sentence and button are visible counterexamples (`ScraperSearchComponent.cpp:386-387`).

### EP-23 — L-26 / 3.31 — **narrowed**

`"ìndia"` is a typo for the intended ASCII token (`LangParser.cpp:65`), and the fixture demonstrates that `"india"` fails.

It is not literally unreachable: a token matching the accented literal is different from ASCII `"india"`. This is a recognition-table defect, not an xgettext defect.

**Change:** Replace the intended token and describe the failure precisely. Keep the retrospective’s correction of the mixed-region fixture; the forward floor text should not continue promising `us,eu` when the supplied run produced `us`.

### EP-24 — L-20 / 3.35 — **narrowed**

The byte-floor defect is real: the loop tests `text.size() > 4` while popping complete UTF-8 characters (`TextFit.h:19-26,34-35`).

But **“a four-byte name never gets its ellipsis” is false**. Once the initial width check fails, the function always returns `text + "..."`, even if the loop never executes (`TextFit.h:32-36`).

**Change:** Describe the defect as script-dependent retained length, not missing ellipsis or UTF-8 splitting. A character-count floor also does not guarantee fitting inside arbitrarily narrow widths; the control proves the proposed floor rule, not a universal width guarantee.

### EP-25 — proposed UPDATE GAMELISTS map text — **refuted**

The shipped Linux interface does **not** have the two asserted homes. The collection-settings entry is inside:

```cpp
#if defined(WIN32) && !defined(_DEBUG)
```

and additionally conditional on scripting support (`GuiCollectionSystemsOptions.cpp:366-369`). The visible shipped home is GAME SETTINGS > TOOLS (`GuiMenu.cpp:5751-5756`).

The blocking-operation description also needs precision: the action offers to stop the scraper or hasher and returns; answering YES stops that operation, rather than continuing the update in the shown callback (`GuiMenu.cpp:8501-8517`).

**Change:** Remove the collection-settings home from the handheld map, or explicitly mark it Windows-only residue. Do not promise the index toast unconditionally: its implementation is **outside the packet**, and the guest did not exercise that setting.

### EP-26 — filter-page map text and fourth check pattern — **narrowed**

The two titles really are member initializers (`GuiGamelistFilter.cpp:11,17`). The proposed regex matches those two literal spellings. That part of the proposal is sound.

The checker’s implementation and complete scan population are **outside the packet**. Adding this pattern may discover other pages too; “exactly two new matches” needs a fresh census rather than assumption.

The page behaviour is also clearer than the draft:

* ordinary filters are applied to the in-memory index;
* only a `CollectionFilter` is saved by this page (`GuiGamelistFilter.cpp:226-263`);
* dynamic-filter creation has an explicit finalize callback that reloads the collection (`GuiCollectionSystemsOptions.cpp:495-504`).

**Change:** Keep both page descriptions and the pattern proposal. Finish the ordinary-filter persistence sentence using the full lifecycle; this excerpt proves that the page itself does not save ordinary filters, not that no other component ever persists them. Add positive and negative checker fixtures and rerun the full inventory.

## 7. The floor

### EP-27 — floor 3.3 — **narrowed**

The floor bundles intended serialization choices with a potentially real path-helper bug. Omitting defaults under an `ignoreDefaults` contract, and retaining an absolute path outside the requested base, do not themselves demonstrate lost information; the serializer explicitly exposes those controls (`MetaData.cpp:280`; `Gamelist.cpp:261`).

The alleged sibling-prefix conversion in `FileSystemUtil.cpp:986-991` is **outside the packet**.

**Change:** Split the verdict. Keep the prefix-boundary case open for verification; stop counting default omission or a genuinely external absolute path as defects without a violated persistence requirement.

### EP-28 — floor 3.16 — **narrowed**

The path helper does concatenate an unchecked name (`CollectionSystemManager.cpp:1508-1515`). `"../evil"` therefore demonstrates a helper precondition, not by itself a reachable player-controlled traversal.

The subagent simultaneously says all current callers sanitize names. That universal caller claim cannot be verified from the excerpts.

**Change:** Do not count a reachable traversal as PRESENT yet. Prove an unsanitized caller or define and enforce the helper’s validation contract. The complete naming/caller path is **outside the packet**.

### EP-29 — floor 3.17 — **narrowed**

Accepting an otherwise unused theme folder name is not established as a defect. The function checks configured systems and used collection theme folders, then reserved collection names (`CollectionSystemManager.cpp:627-651`). An existing configured name is rejected by that comparison.

**Change:** Supply the actual configuration and the rule forbidding unused theme names before calling `"zxspectrum"` a concrete failure. The absence of a call to `themeFolderExists` is not a correctness proof.

### EP-30 — floor 3.26 — **refuted** as a demonstrated defect

The lookups are exact and explicitly support the `global.` variant (`CustomFeatures.cpp:529-536`). No supplied contract says feature identifiers are case-insensitive.

**Change:** Reclassify `"Ratio"` versus `"ratio"` as a schema/producer compatibility test, not an established lookup bug. Evidence that the shipped producer emits the former while the consumer requires the latter is **outside the packet**.

### EP-31 — floor 3.28 — **refuted**

`getSortType(-1)` returning the first sort is an explicit fallback, not an out-of-bounds operation (`FileSorts.cpp:32-38`). The table is populated immediately below (`FileSorts.cpp:43-71`).

**Change:** Keep a regression test for the safe fallback, but remove this from the defect count. It is different from the separately reported index-bound error in `FileData.cpp`, whose decisive lines are **outside the packet**.

### EP-32 — floor 3.37 — **refuted**

A case-only rename is a different full-path identity under this helper’s explicit contract (`FolderMerge.h:15-18,22`). The implementation consequently retires one node and attaches another (`FolderMerge.h:48-66`).

**Change:** Do not “fix” this by case-folding path identity: that could conflate distinct files on a case-sensitive filesystem. If rename tracking is desired, specify it as additional functionality rather than counting its absence as this merge algorithm’s defect.

### EP-33 — floor 3.10 — **narrowed**

The blanket property verdict is too strong. The visible function returns zero when **either** string is empty, including two identical empty strings (`FileFilterIndex.cpp:562-565`). That contradicts an unqualified “identical → 1” test rule unless empty/empty is deliberately exempted.

The claimed fixed-array overflow at `:579-580` and the symmetry calculation are **outside the packet**.

**Change:** Define the empty-string convention explicitly. Keep the oversized-string case pending the actual array/index code; sampled symmetry is not proof of the property for all inputs.

### EP-34 — floor 3.38 / L-14 — **narrowed**

The substring issue is real (`RunLock.h:66-70`), but a stale PID file alone is not enough: a successfully acquired probe lock returns zero (`RunLock.h:49-55`). The counterexample also requires the lock to remain held or to have been reacquired while the recorded PID is stale.

The proposed argv[0]-basename equality repair is not automatically sufficient for a **script**. An interpreter may occupy argv[0]; the actual script invocation is **outside the packet**. Matching a command name also does not prove that the recorded PID owns the tested lock.

**Change:** Test the real NUL-separated invocation shape, stale-record/new-holder window and misleading argument case. Describe stricter command matching as mitigation, not proof of lock ownership or elimination of the later PID-reuse race.

### EP-35 — remaining floor evidence — **narrowed**

Several verdicts cannot be independently confirmed or reversed from this packet:

* duplicate BBC rows: reported `PlatformId.cpp:28,171`;
* scrape-field clearing: reported `MetaData.cpp:532,560-568`;
* duplicate parent genres and the end-iterator dereference: reported `Genres.cpp:244-248,302-304`;
* the sibling sort-bound error: reported `FileData.cpp:1659`;
* flag selection/assets: reported `LangParser.cpp:225-226` and `DetailedContainer.cpp:892`.

Those decisive lines are **outside the packet**. The visible `Genres.cpp:299` comparison is indeed always true for an unsigned `find()` result, but it does not expose the reported dereference itself.

Likewise, the ratio table exposes its strings, not proof that the shipped launcher accepts every value (`LibretroRatio.cpp:15-40`); that consumer contract is outside the packet.

**Change:** Do not turn these into ABSENT findings. Preserve them as supplied subagent findings requiring artifact verification. Recompute the floor’s defect count after removing the intentional behaviours above; “PRESENT 16” is not a reliable count of demonstrated runtime defects.

## New findings

### EP-36 — **new: restored metadata can still be lost after the proposed L-05 fix**

**Verdict: new. Family: a read of a file another process writes.**

Even with a fresh read, a dirty game’s entire restored node is removed and replaced from the in-memory game (`Gamelist.cpp:449-459`). The comment assumes memory contains complete information for that game (`Gamelist.cpp:376-379`); a restore performed while ES runs invalidates that assumption.

Example: memory has Alpha’s name and a newly changed favourite; the restored XML has Alpha’s description and artwork. Freshly loading that XML preserves Bravo, but replacing Alpha’s whole node can still discard Alpha’s restored fields.

There is also a read/replace interval in which an external writer can publish a newer document (`Gamelist.cpp:416,474`). Temp-and-rename alone does not prevent that lost update.

**What would prove it:** Extend the fixture to restore metadata for the *same dirty game*, then save; separately pause ES after reading while another writer replaces the XML.

**Change:** Add a merge/restore coordination policy—field-level reconciliation or coordinated reload/replay—not just an existence and atomicity patch.

### EP-37 — **new: collection reload moves the old view, not the replacement**

**Verdict: new. Family: a lifetime or a thread.**

`reloadCollection` retains `view`, calls `reloadGameListView(bundle)`, then casts and moves **that retained old view** (`CollectionSystemManager.cpp:1586-1593`). The reload erases the registered view and obtains a replacement (`ViewController.cpp:1145-1153`).

The local shared owner can keep the old object alive, so this is not necessarily another UAF. It is nevertheless the wrong instance on which to restore navigation.

**What would prove it:** A view-double test that records old/new identities and asserts `moveToFolder` affects the registered replacement. UI reachability still needs the L-06 caller proof.

**Change:** Reacquire/use the remade view. Include navigation restoration in the L-06 control, not only absence of an ASan fault.

### EP-38 — **new: screensaver-held `FileData` pointers are missing from the retirement audit**

**Verdict: new. Family: a lifetime or a thread.**

The screensaver stores game pointers in its media collection and in `mCurrentGame` (`SystemScreenSaver.cpp:350-358,378-380`). It subsequently dereferences a supplied game for media and the current game for navigation/launch (`SystemScreenSaver.cpp:372-379,538-548`).

The shown rescan retirement removes collection/group holders and deletes the node without showing screensaver retirement (`SystemData.cpp:459-473`).

**What would prove it:** Prime the screensaver, remove a represented ROM, perform the relevant rescan, then select/launch screensaver media under ASan. First inspect the omitted reset/invalidation paths: those are **outside the packet**, so this is an unclosed lifetime lead, not a claimed reproduced UAF.

**Change:** Add these holders to L-15. Do not infer their safety from `DisplayAspect`, which deliberately caches paths rather than pointers (`DisplayAspect.cpp:44-55`).

### EP-39 — **new: an obsolete token check can overwrite newer account state**

**Verdict: new. Family: a lifetime or a thread.**

The worker snapshots credentials before authentication (`NetworkThread.cpp:130-138`), but posts only the returned token; the UI callback writes it without checking the account or settings generation (`NetworkThread.cpp:264-270`).

Meanwhile, disabling achievements explicitly clears the token (`GuiRetroAchievementsSettings.cpp:795-798`). An already-running successful check can subsequently write it back. The closing gate does not address this ordinary-session stale-result problem.

**What would prove it:** Block authentication, disable achievements or change the account, release the old success, and drain the UI queue.

**Change:** Carry account identity/generation with the result and reject obsolete completion before committing it.

### EP-40 — **new: failed rotation persistence is published as successful state**

**Verdict: new. Family: a check whose failure reads as success.**

After the unchecked write, the helper logs the new rotation and caches it with the destination’s current timestamp (`CaptureRotation.cpp:175-180`). `read()` then returns that cached value solely on timestamp equality (`CaptureRotation.cpp:103-108`).

A failed write can therefore leave old bytes—or no file—while the running interface reports the intended new rotation.

**What would prove it:** Inject a write failure with an old record or a missing destination, then call `read()` and compare the returned rotation with the verified artifact/fallback.

**Change:** Publish the cached value only after checked persistence. Atomic writing without checking its result leaves this defect.

### EP-41 — **new: the rotation cache can miss an atomic external replacement**

**Verdict: new. Family: a read of a file another process writes.**

The cache identity is only `time_t st_mtime` (`CaptureRotation.cpp:89-95,103-108`). A changed record with the same timestamp returns the previous rotation **before** the uncached existence check is reached (`CaptureRotation.cpp:113`).

**What would prove it:** Read one rotation, atomically replace the record with another while preserving its timestamp, then read again. A same-second replacement is another relevant case.

**Change:** Stop describing the four uncached probes as complete freshness coverage. Reread the small record or use a replacement-sensitive identity/generation with an explicit writer contract.

### EP-42 — **new: malformed achievement replies can become known empty progress**

**Verdict: new. Family: a check whose failure reads as success.**

`parseUnlocks` rejects only an explicitly boolean-false `Success`; missing or wrong-typed `Success` passes. Invalid list elements can all be discarded, after which `ok` is set true (`OfflineAchievementsText.cpp:183-200`).

For example, `{"Success":"false","UserUnlocks":[{}]}` yields an accepted empty result, contrary to the documented requirement for `Success: true` (`OfflineAchievementsText.h:84-90`).

The patch/set readers also set `ok` without validating the response’s `Success` field (`OfflineAchievementsText.cpp:99-112,120-148`).

**What would prove it:** Pure parser cases for missing/wrong-typed success, explicit failed responses carrying lists, and lists containing only malformed entries.

**Change:** Narrow the first reader’s blanket “fail closed” positive. Keep unknown/unreadable progress distinct from zero, while preserving the explicitly documented allowance for a valid all-unofficial set (`OfflineAchievementsText.h:75-76`).

### EP-43 — **new: dynamic-filter save failure is ignored by the page**

**Verdict: new. Family: a check whose failure reads as success.**

`CollectionFilter::save` reports failure (`FileFilterIndex.cpp:1313-1316`), but the page discards that result, deletes itself, and invokes finalization (`GuiGamelistFilter.cpp:262-270`).

Thus an atomic writer could correctly retain the old file while the UI still closes as though the new selection had been saved.

**What would prove it:** Force `save()` to fail and verify that the page retains the unsaved choices, reports failure, and does not execute success finalization.

**Change:** Include the caller in L-23’s repair. Preserve both the last-good file and a truthful UI outcome.

### EP-44 — **new: `clearIndex` clears a copy**

**Verdict: new. Family: a check whose failure reads as success — silent no-op reset.**

`FileFilterIndex::clearIndex` receives its map **by value** and clears only that copy (`FileFilterIndex.cpp:1102-1105`).

**What would prove it:** Call the helper with a populated map and assert that the original becomes empty. Then trace its actual callers; they are **outside the packet**, so no particular player-visible stale-index scenario is established here.

**Change:** Verify whether this is live. If so, pass the map by reference and test the owning reset path. Do not claim that the caller’s index has been cleared by the current helper.

### EP-45 — **new: Zaparoo treats transport completion as card-write success**

**Verdict: new. Family: a check whose failure reads as success.**

`writeZaparooCard` returns `req.wait()` without inspecting any JSON-RPC result or error (`ZaparooSupport.cpp:58-63`). It also inserts `name` directly into a JSON string (`ZaparooSupport.cpp:60`), so a quote or backslash can change or invalidate the request representation.

**What would prove it:** Capture a request containing a quoted name, and return a successful HTTP response carrying a JSON-RPC error. Establish the real `HttpReq::wait` contract, whose implementation is **outside the packet**.

**Change:** Serialize JSON properly and validate the protocol outcome, including response identity where applicable. A successful HTTP exchange is not proof that a card was written.

### EP-46 — **new: a valid mouse-only key map is classified invalid**

**Verdict: new. Family: a read of a file another process writes.**

Mouse mappings can use a joystick trigger and need no targets: that is accepted by the trigger check, loader and writer (`KeyboardMapping.cpp:178-181,293-294,351-352`). But `isValid()` requires nonempty targets for every mapping (`KeyboardMapping.cpp:499-509`).

A file consisting only of such a mouse mapping can therefore load and save, yet be declared invalid. A visible menu gate uses `isValid()` for system mappings (`GuiGamelistOptions.cpp:262-267`).

**What would prove it:** Load/save a mouse-only mapping with `joystick1` and no targets, then assert validity and the applicable information row.

**Change:** Align the validity predicate with the accepted mapping schema. The floor’s quote-escaping check does not cover this round-trip validity disagreement.

### EP-47 — **new: self-deleting workers can finish before their singleton is published**

**Verdict: new. Family: a lifetime or a thread.**

`ThreadedBluetooth` starts its worker inside its constructor (`ThreadedBluetooth.cpp:19`). The worker can return from the API call and delete the object (`ThreadedBluetooth.cpp:39-47`) before `start()` finishes assigning the `new` expression to `mInstance` (`ThreadedBluetooth.cpp:58`).

That permits publishing a freed pointer; the constructor’s own `mHandle` assignment can also race the deletion. The singleton reads/writes shown have no synchronization (`ThreadedBluetooth.cpp:10,27,47,52,58`). Formatting repeats the construction/self-deletion/publication pattern (`ThreadedBluetooth.cpp:76,110-122`).

**What would prove it:** Make the service call complete immediately, force completion before publication, and run under ASan/TSan; test repeated starts as well as the slow-success case.

**Change:** Expand L-10 beyond the leaked thread object. Publish ownership before starting work and let an owner retire/join the worker. This safety repair does not require redesigning the background-card interface.

## Highest priorities

1. **EP-1, EP-2 and EP-36 — game-content preservation.** The supplied fixture and image show real loss, while the proposed repair still permits destructive cleanup and same-game metadata loss.
2. **EP-6 and EP-10 — memory safety.** Cancellation has a demonstrated free/write failure; malformed `.keys` values reach unchecked release-build accesses. Neither should be downgraded merely for being upstream-carried or outside a feature lane.
3. **EP-13 — interface responsiveness.** The network-to-interface lock coupling is directly established and affects ordinary settings/input paths.
4. **EP-19 and EP-43 — persistence plus truthful completion.** Atomic files, cache invalidation and handling the save result are three separate obligations.
5. **EP-5 and EP-38 — urgent reachability/retirement verification.** The lifetime mechanisms warrant attention, but I would not rank them as demonstrated end-to-end crashes until the omitted caller and invalidation paths are resolved.