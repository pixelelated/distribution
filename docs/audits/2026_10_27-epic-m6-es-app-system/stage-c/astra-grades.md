# T33 (#680): the seat's 47 items, graded by the first reader

The seat is GPT-6 Astra at `max`, the refutation 19:41:52 to 20:01:31 UTC (`second-opinions/astra-audit.md`; provenance PASS). Each item was read against the pin at its lines before it was graded. **Verified** names the lines the first reader read. **Outside the packet** is where the seat could not decide; the first reader's own re-read settles some of those (`stage-c/floor.md`'s [re-read] rows).

| EP | Lead | Seat | Grade | What changes | Verified |
| --- | --- | --- | --- | --- | --- |
| 1 | L-05, 3.13 | confirmed | accepted | L-05 states its prerequisites (a remembered miss, a dirty entry); the parse-error sentence corrected (`:416-424` logs and continues: an unreadable file must not be overwritten) | `Gamelist.cpp:394-428`, `SystemData.cpp:1648-1663` |
| 2 | 3.15, L-05's fix | narrowed | accepted | PL-01's fix covers `getGamelistPath`'s path choice, `packGamelist`'s removal on a miss (`:595-605`), `cleanupGamelist`'s probes, the unverified `.old` copy, and the recovery order at startup (pack clears recovery before parse reads it; to verify) | `Gamelist.cpp:595-605`, `:618-625` |
| 3 | 3.12 | narrowed | accepted | `saveToXml`'s remove-before-save (`:303-311`) joins PL-16 | `Gamelist.cpp:307-308` |
| 4 | 3.14 | narrowed | accepted | no blind `exists` substitution at `:116` (it is `isRegularFile`); path normalization tested apart | `Gamelist.cpp:112-117` |
| 5 | L-06 | narrowed | **accepted** | the mechanism stands (fixture); **the bundle route is not established**: `GuiGamelistOptions.cpp:424` excludes the bundle, and `ISimpleGameListView.cpp:461-462` reloads by the root's system. A non-bundled dynamic collection's own view is cleared by `:1117` with no reload by `reloadCollection` at all: a further lead. PL-02 narrows to "conditional", severity Medium. G-02's "heap's choice" sentence withdrawn | `GuiGamelistOptions.cpp:424-427`, `ISimpleGameListView.cpp:455-464` |
| 6 | L-07 | confirmed | accepted | **the thread is joined in `update()`** (`:230-232`); the first reader's "never joined" is wrong. The fix is one ownership scheme (`joinable()`), the leak at `:233`, and no join on the interface thread in `stop()` | `ScraperSearchComponent.cpp:225-233` |
| 7 | L-12 | narrowed | accepted | a closing-protocol violation, not a dangling write; routing the posts drops the token write rather than saving it: the stream states the drain policy | `AppWindow.h:38-53`, `main.cpp:1316-1330` |
| 8 | L-15 | narrowed | accepted | three passing tests are not lifetime closure; the screensaver's holders join the checklist (EP-38) | `SystemData.cpp:459-473` (cited) |
| 9 | L-24 | confirmed | accepted | the rule written as "retire every observer before freeing it" | -- |
| 10 | L-28, 3.21 | confirmed | **accepted** | the wild reads named line by line (`:251`, `:254`, `:257`, `:265-266`, `:271-272`, `:282-283`, `:288-289`; no `IsObject` at `:246-250`); `GetArray` calls are guarded; a chord can lose one trigger and change meaning. **PL-12 raised to Medium**: a memory-safety defect on a player file | `KeyboardMapping.cpp:236-294` |
| 11 | L-27, 3.9 | narrowed | accepted | the control's rule is a proposed policy, said so; `1 STARS` is an index key whose display is to verify | `FileFilterIndex.cpp:321-369` |
| 12 | L-17, 3.41 | narrowed | accepted | the epoch is `time_t` via `strtoll` (`:229-231`), not `int`; "harmless today" removed | `OfflineAchievementsText.cpp:17-20`, `:229-231` |
| 13 | L-01 | confirmed | accepted | the brief's callers corrected: `GuiRetroAchievementsSettings.cpp:191` is a comment and `:257` a weak-pointer test; the callers are `:805-806` and `NetworkThread.cpp:257`; moving `check()` out of the lock needs the registry's lifetime | `WatchersManager.cpp:80-100`, `:181-199` |
| 14 | L-02 | narrowed | accepted | not every exit (exit 0, RetroArch, a record path, a fresh log); the log's truncation is no size bound: `t33-bounds.py`'s exec.log row is **not bounded** | `CaptureRotation.cpp:139-163`, `FileData.cpp:1166-1169` |
| 15 | L-04 | confirmed | accepted | invalidation also after a rotation record (`CaptureRotation.cpp:182-186`) | -- |
| 16 | L-09 | narrowed | accepted | explicit options against inherited defaults (T32's bounds cite `HttpReq.h:45-90`: no total, no stall) | cited |
| 17 | L-11 | narrowed | accepted | **`SystemScreenSaver.cpp:375` is the game's media, not the title folder**: `t33-reads.py`'s group corrected; the retries pick a new candidate each time | `SystemScreenSaver.cpp:372-376` |
| 18 | `02` § The bounds | refuted as exhaustive | accepted | the table is labelled direct constructions, process starts and named waits; the transitive installer, Bluetooth and fallback-search calls listed as not bounded here | `ContentInstaller.cpp:132-135`, `ThreadedBluetooth.cpp:41-44` (cited) |
| 19 | L-23 | confirmed, conditionally | accepted | the `.xcc` is pugixml's, not `std::ofstream`; a stale `.xcc` miss may select the `.cfg` rather than return false; **a cut `.xcc` gives an empty collection, not every game**; atomic write needs explicit invalidation | `CollectionSystemManager.cpp:1114-1124`, `:1609-1614` |
| 20 | L-03 | confirmed | accepted | the cache updated only after a checked write (with EP-40) | `CaptureRotation.cpp:174-181` |
| 21 | `02` § The reads, `.keys` | refuted | **accepted** | **`KeyboardMapping.cpp:426`, `:429` write through `Utils::FileSystem::writeAllText`**: the `:324` row's claim is withdrawn | `KeyboardMapping.cpp:423-429` |
| 22 | L-25 | confirmed | accepted | anchors and French only; `defaultTags`' names are stored keys and stay English | `FileTag.cpp:34-38` |
| 23 | L-26 | narrowed | accepted | "a recognition-table typo", not "unreachable" | -- |
| 24 | L-20 | narrowed | accepted | script-dependent retained length; "never gets its ellipsis" (the brief's) is false | `TextFit.h:32-36` |
| 25 | the map's UPDATE GAMELISTS | refuted | **accepted** | **the collection-settings entry is `#if defined(WIN32) && !defined(_DEBUG)`** (`GuiCollectionSystemsOptions.cpp:366-369`): the handheld's one home is GAME SETTINGS > TOOLS; YES on the scraper/hasher question stops it and returns | `GuiCollectionSystemsOptions.cpp:366-369`, `GuiMenu.cpp:8501-8517` |
| 26 | the filter pages' text, the pattern | narrowed | accepted | only a `CollectionFilter` is saved by the page; the pattern's census is rerun on the stream's tree | `GuiGamelistFilter.cpp:226-270` |
| 27 | 3.3 | narrowed | accepted | default omission and an outside absolute path are contracts, not defects; the prefix case stays open | -- |
| 28 | 3.16 | narrowed | accepted | a helper precondition, not a reachable traversal | -- |
| 29 | 3.17 | narrowed | accepted | not a defect without a rule against unused theme names | -- |
| 30 | 3.26 | refuted | accepted | a schema test, not a bug | -- |
| 31 | 3.28 | refuted | accepted | an explicit fallback; removed from the defect count | `FileSorts.cpp:32-38` |
| 32 | 3.37 | refuted | accepted | a case-only rename is a new identity by contract | `FolderMerge.h:15-22` |
| 33 | 3.10 | narrowed | accepted | empty/empty returns 0 (`:562-565`); the arrays are confirmed by the first reader's re-read (`:579-580`), the overflow index to verify | `FileFilterIndex.cpp:562-580` |
| 34 | L-14, 3.38 | narrowed | accepted | needs the lock held with a stale pid; basename equality is a mitigation, not ownership proof | `RunLock.h:49-70` |
| 35 | the floor's rest | narrowed | accepted in part | the five the seat could not see were re-read by the first reader (`Genres.cpp:304`, `PlatformId.cpp:28`/`:171`, `MetaData.cpp:568`, `FileData.cpp:1659`; `LangParser.cpp:225-226` remains the subagent's); the defect count recomputed without 3.26, 3.28, 3.37 | `stage-c/floor.md` |
| 36 | new: same-game restored fields | new | **accepted** | a dirty game's whole node is replaced from memory (`Gamelist.cpp:449-459`): its restored description and art are lost even with a fresh read; PL-01's fix needs a field merge, and its fixture a same-game case | `Gamelist.cpp:445-459` |
| 37 | new: the old view moved | new | accepted | `reloadCollection` moves the retained old view (`:1586-1593`); joins PL-02 | `CollectionSystemManager.cpp:1584-1594` |
| 38 | new: screensaver holders | new | accepted as a lead | the screensaver's `FileData*` (`SystemScreenSaver.cpp:350-358`) not retired by the rescan shown; a lead for PL-02's checklist, not a reproduced fault | cited |
| 39 | new: a stale token write | new | **accepted** | the posted token is written with no account or generation check (`NetworkThread.cpp:264-270`), and disabling achievements clears it (`GuiRetroAchievementsSettings.cpp:795-796`): a check in flight writes it back. The fork's file, the fork's lanes | `NetworkThread.cpp:260-272`, `GuiRetroAchievementsSettings.cpp:793-799` |
| 40 | new: rotation published unchecked | new | accepted | `writeAllText`'s result unread, then cached with the destination's mtime (`CaptureRotation.cpp:175-180`) | `CaptureRotation.cpp:174-181` |
| 41 | new: rotation cache by mtime | new | accepted | `sKnownAt` keyed by mtime alone (`:103-108`) answers before the uncached probe: the four uncached reads are not full freshness | `CaptureRotation.cpp:100-110` |
| 42 | new: malformed unlocks read as known | new | **accepted** | a missing or non-bool `Success` passes, and a list of invalid entries ends `ok = true` with no ids (`OfflineAchievementsText.cpp:183-200`); the first reader's "fails closed" positive narrowed. The fork's helper | `OfflineAchievementsText.cpp:183-200` |
| 43 | new: the filter save unchecked | new | accepted | `collectionFilter->save()`'s result discarded, the page closes as saved (`GuiGamelistFilter.cpp:262-270`); joins PL-05 | `GuiGamelistFilter.cpp:258-270` |
| 44 | new: `clearIndex` clears a copy | new | **accepted, live** | `clearIndex` takes the map by value (`FileFilterIndex.cpp:1102-1105`) and `resetIndex` calls it for every index (`:154-160`); a reset keeps every old key | `FileFilterIndex.cpp:146-160`, `:1102-1105` |
| 45 | new: Zaparoo's card | new | accepted (recorded) | `req.wait()` is the success, and the name goes raw into JSON (`ZaparooSupport.cpp:58-63`); outside the lanes | `ZaparooSupport.cpp:55-64` |
| 46 | new: mouse-only map invalid | new | accepted (recorded) | `isValid` requires targets (`KeyboardMapping.cpp:499-509`), which a mouse mapping has none of; outside the lanes | `KeyboardMapping.cpp:499-509` |
| 47 | new: Bluetooth publication race | new | accepted (recorded) | the worker starts in the constructor and deletes itself (`ThreadedBluetooth.cpp:39-47`) before `start()` publishes (`:58`); joins L-10 | `ThreadedBluetooth.cpp:36-60` |

**Counts:** 47 items, 47 accepted (three of them "recorded", one "in part", one "as a lead"). Each sentence of the first reader's the seat corrected is fixed in place and cited by EP: EP-1, EP-5, EP-6, EP-12, EP-14, EP-17, EP-19, EP-21 and EP-25.
