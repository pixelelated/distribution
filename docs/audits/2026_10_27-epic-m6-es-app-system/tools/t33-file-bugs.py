#!/usr/bin/env python3
"""T33 (#680): the titles and bodies of the twenty bugs the stage-D ruling names
(#680 comment 6452429909, 20:10 UTC), from 05-punch-list.md (T32's t32-file-bugs.py,
#679, adapted).

    python3 -I t33-file-bugs.py <05-punch-list.md> <out dir>

Writes <out dir>/<ID>.title and <ID>.md. A body is: an introduction, the
item's section of 05 copied (its family, owner area, fix shape, VM line,
Already written line and acceptance), the ruling for it, then a code trace in
four parts -- how it was found, the defect at its source at the pin, the
siblings hunted, and what reading cannot prove -- then the acceptance every
T33 bug shares. EP-47 is PL-19's one ruled part and carries its own section.
Asserts twenty bugs, each with a trace, an Already written line and a VM line.
"""
import os, re, sys

RULE = "#680 comment 6452429909, 20:10 UTC"
RULING = {
 "PL-01": "one stream with the field merge, under **D-CLOUD-187** (a game list the cloud restored while ES runs is merged at the next save, never overwritten): the uncached reads, temp-and-rename for the three writes (D-CLOUD-078), no overwrite of a file that did not parse, and the field-level merge (EP-36) with `MetaDataList` tracking which fields changed; the merge the stream's last commit with its own FAIL-first case; the exit save's cost measured against D-CLOUD-119's budget; a #585 line to ROCKNIX.",
 "PL-02": "a bug now; the stream's first step reads the caller route (the bundle is excluded at `GuiGamelistOptions.cpp:424`; a non-bundled dynamic collection's own view is where to look) and records it here; the fix is the drop/remake pair around `reloadCollection` either way (D-QA-051 rule 6); the route decides the severity's word.",
 "PL-03": "a bug under rule 6: the builder owns and joins its thread.",
 "PL-04": "a bug, as proposed (rule 6).",
 "PL-05": "a bug, as proposed (rule 6).",
 "PL-06": "a bug, as proposed (the fork's own rule).",
 "PL-07": "a bug; the three French words as proposed (EN COURS, ABANDONNÉ, EN PAUSE; D-UI-112, put to the maintainer in the build); the tag keys stay English.",
 "PL-08": "a bug, as proposed.",
 "PL-09": "a bug, as proposed (rule 6).",
 "PL-10": "a bug, as proposed.",
 "PL-11": "a bug here, written against the pin in `OfflineAchievementsText.*`, T20's `274a71add` and `f85061f14` named in the hand-back as the collision the integration reconciles.",
 "PL-12": "a bug under rule 6: a shape check before every read, the refused trigger named to the player in one line; the loader's behaviour otherwise as upstream has it (D-UI-079).",
 "PL-14": "a bug here, the fork's half: `NetworkThread` runs the token check off the watcher lock and applies its result under it; if `WatchersManager.cpp`'s structure must change, that half is named for the es-core slice with its shape in `02`, and this bug keeps that checkbox open.",
 "PL-15": "a bug here: the dialog reads the script's `>>> why` line and its outcome, not rc alone; if `cloud_setup --seed-folders` prints no why on a failure, that half is a line for the rclone slice, named.",
 "PL-16": "a bug here, for the writers in T33's files (`CaptureRotation.cpp`, `KeyboardMapping.cpp`, `Gamelist.cpp`'s remove-then-save), through `AtomicFile::writeText`; Backlog #1186 updated by the coordinator.",
 "PL-21": "a bug here, with T20's collision named (as PL-11).",
 "PL-22": "a bug, as proposed (rule 6).",
 "PL-23": "a bug, as proposed (the fork's lane).",
 "PL-24": "a bug here, through `AtomicFile::writeText` (as PL-16).",
 "EP-47": "a bug under rule 6: the publication under its lock.",
}
TRACE = {
 "PL-01": ("L-05 at stage B (`t33-reads.py`'s `Gamelist.cpp:413` row); `stage-c/l313-update-gamelist.py` FAILs at the pin (the outside entry lost; the inode unchanged); G-04 on the guest with its control (gb's file lost Bravo, gbc's byte-identical); the cache trace to `SystemData.cpp:1653`; the seat's EP-1, EP-2 and EP-36.",
           "`SystemData::getGamelistPath` (`SystemData.cpp:1652-1663`) answers through the session cache at load and again at `Gamelist.cpp:411`; `:413` reads the remembered miss; `:427` starts an empty `<gameList>`; `:449-459` removes a dirty game's node and rebuilds it from memory; `:474` writes in place. `packGamelist` (`:595-605`) removes a media child on a cached miss; `cleanupGamelist` (`:702-752`) probes the same way; both copy aside to `.old` unchecked and write in place (`:618-625`, `:837-844`).",
           "`saveToXml`'s remove-then-save (`:307-308`, PL-16); `MetaData.cpp:223`'s PreloadMedias probe at load; `FileFilterIndex.cpp:867`, `:889` (has-media filters); the startup order pack -> parse with the recovery clear between (`SystemData.cpp:125-128`, `Gamelist.cpp:625-628`, `:247-249`; EP-2, to read).",
           "The cloud restore's timing against a running ES on a device; the exit save's cost on a large library (measured in the stream's harness); whether `isRegularFile` shares the cache entry `exists` writes (`FileSystemUtil.cpp:238-240`, T21's file)."),
 "PL-02": ("L-06 (brief, T32 L-16) at stage B; `stage-c/l06-reload-collection.py` at stage C (a heap-use-after-free under ASan, the control clean); G-02 on the guest drove a plain collection and could not reach it; the seat's EP-5 (the route), EP-37 (the old view moved), EP-38.",
           "`CollectionSystemManager.cpp:1573-1600`: for a dynamic collection, `populateCustomCollection` clears its root (`:1115-1117`), which is the bundle's child by identity (`:1302`); `reloadGameListView(bundle)` then reads the old view's cursor (`ViewController.cpp:1140-1142`); `moveToFolder` is called on the retained old view (`:1586-1593`).",
           "`GuiGamelistOptions.cpp:424-427` (excludes the bundle); `ISimpleGameListView.cpp:455-464` (reloads by its root's system); a non-bundled dynamic collection's own view; `SystemScreenSaver.cpp:350-358`'s held pointers (PL-25); `SystemData.cpp:459-473`'s retirement.",
           "The GUI route that reaches the free with a cursor on a freed game (the stream's first step); whether `FolderData::clear` deletes children in every build (read in `FileData.cpp`, outside the slice)."),
 "PL-03": ("L-07 at stage B (handed by T32's ruling 4); `stage-c/l07-search-builder.py` at stage C (a heap-use-after-free under ASan when the builder is dropped mid-search); the seat's EP-6.",
           "`components/ScraperSearchComponent.cpp:196-258`: `new std::thread` at `:206`; the worker writes `mSearchHandle`, `mError`, `mFinished` (`:213-220`); `update()` joins only after `mFinished` and then drops the pointer without deleting it (`:225-233`); there is no destructor; `stop()` and `~ScraperSearchComponent` drop the builder (`:358-361`, `:96-100`).",
           "L-08's synchronous second search (`:645-658`); the manual paths on the interface thread (`:303`, `:321`); `mFinished` read across threads unsynchronised.",
           "The device timing of a back press during a token or hash request; whether `Scraper` and `ScraperSearch` outlive the worker in every caller (EP-6, outside the packet)."),
 "PL-04": ("The floor's 3.8, a subagent's read, re-read by the first reader at `Genres.cpp:293-306`; the seat's EP-35 could not see it (outside the packet).",
           "`Genres.cpp:295` looks the whole name up; on a miss, `:299`'s `name.find(\"/\") >= 0` is always true; the loop finds a subgenre as `sg` and returns `mGenres[g->second]` (`:304`), dereferencing `g`, the whole name's end iterator.",
           "`FileFilterIndex.cpp:1251-1253`, `:1184` (a dynamic collection's genre filter round trip); the scrapers' genre conversion; 3.8's double count of a parent genre (`Genres.cpp:244-248`, `FileFilterIndex.cpp:1015-1016`).",
           "Which genre names reach the branch on a device (a scraper's or a filter's); the observed effect of the undefined read (a wrong genre or a crash)."),
 "PL-05": ("L-23 at stage B (`t33-writes.py`); the third cache shape read at stage B; the seat's EP-19 (the `.xcc` is pugixml's; a cut one empties the collection) and EP-43 (the page ignores `save()`).",
           "`CollectionSystemManager.cpp:345` writes `custom-<name>.cfg` through `std::ofstream` with no check; `FileFilterIndex.cpp:1313` writes the `.xcc` through `pugi::save_file`; neither drops the cache entry; `:963` reads the `.xcc` at startup; `deleteCustomCollection` (`:1609-1614`) reads both through the cache; `populateCustomCollection` (`:1114-1124`) clears, then adds only if `load()` succeeds; `GuiGamelistFilter.cpp:262-270` discards `save()`'s result.",
           "`:1147` (the custom list's probe), `FileFilterIndex.cpp:1144` (`CollectionFilter::load`); backuptool's archive carries both files (settings tier).",
           "A power loss mid-write on a device; whether `AtomicFileUtil` drops the cache entry (outside the packet, EP-19: the stream drops it explicitly)."),
 "PL-06": ("L-12 at stage B; `stage-c/l12-network-posts.py` at stage C (five direct posts; the gate refuses a gated post after `closing()`); the seat's EP-7.",
           "`NetworkThread.cpp:206`, `:237`, `:251`, `:257`, `:266` call `mWindow->postToUiThread`; `AppWindow::post` (`AppWindow.h:38-45`) is the gate; `main.cpp:1322` closes it and `:1330` stops the watchers after it.",
           "T20's hasher start at `:248`, `:251` (#1170's callers); `ProxyCards::linkReturned` posted at `:237`; PL-23's stale token write at `:266`.",
           "The ordering on a device at shutdown; whether a lost token write matters given the next start re-checks (EP-7: the stream states the drain policy)."),
 "PL-07": ("L-25 at stage B; `stage-c/l329-filetag-words.py` at stage C (three names not extracted, no French); the seat's EP-22.",
           "`FileTag.cpp:6-11` defines six `fake_gettext_*` anchors; `defaultTags` (`:13-26`) holds nine names; IN PROGRESS, DROPPED and ON HOLD have no anchor and no msgid in `locale/lang/fr/LC_MESSAGES/emulationstation2.po`.",
           "The pages that show tags (T31's `GuiGamelistFilter`, `GuiMetaDataEd`); `FileFilterIndex.cpp:1224-1225`, `:1310-1311` store the English names (they stay English: EP-22).",
           "The French on a frame (an open item for the integration window)."),
 "PL-08": ("L-20 at stage B; T20 S9; `stage-c/l335-textfit-floor.py` at stage C (4 ASCII characters kept against 1 Japanese); the seat's EP-24.",
           "`TextFit.h:34`: `while (text.size() > 4 && measure(text + \"...\") > width)` counts bytes, while `popCharacter` (`:19-26`) pops whole characters.",
           "The callers `guis/GuiCloudTransfer.cpp:585`, `GuiOfflineScan`, `GuiScraperRun`; `TextFitTests.cpp`'s three cases (pass at the pin).",
           "How often a CJK name meets a width that small on a device."),
 "PL-09": ("L-26 at stage B; `stage-c/l331-lang-india.py` at stage C (`india` reads nothing); the seat's EP-23.",
           "`LangParser.cpp:65`: `{ { \"in\", \"ìndia\" }, \"in\", \"in\" }`; tags are lowercased at `:148` before `extractLang`, so `india` never equals the accented token.",
           "The other rows of `langDatas` (`:37-64`, all ASCII); `getFlag` (`:203`, the floor's 3.32).",
           "Nothing beyond the fixture."),
 "PL-10": ("L-14 at stage B; the floor's 3.38 (a subagent's read); the seat's EP-34.",
           "`RunLock.h:66-68`: `holder()` accepts a pid whose `/proc/<pid>/cmdline` merely contains `program` (`line.find(program)`).",
           "`OfflineAchievements::stopRun`, which signals the pid `holder()` returns; `held()` (`:29-42`, sound).",
           "The pid-reuse window on a device; that the recorded pid owns the lock (EP-34: command matching is a mitigation)."),
 "PL-11": ("L-17 at stage B; the floor's 3.41 (a subagent's read); the seat's EP-12 (the epoch is `time_t`).",
           "`OfflineAchievementsText.cpp:17-20`: `jsonInt` returns `(int)v.GetInt64()`; the id fields are `int` (`OfflineAchievementsText.h:51`, `:63`, `:110`); `parsePendingIds` parses ids with `toInteger` (`:229`).",
           "T20's `274a71add` and `f85061f14` on the same file (the collision); the consumers in `RetroAchievements.cpp` (outside the slice).",
           "Whether any id above 2^31 exists today; `toInteger`'s range behaviour (es-core, outside the slice)."),
 "PL-12": ("L-28 at stage B; `stage-c/l321-keys-parse.py` at stage C (the unknown trigger dropped, nothing logged); G-08 on the guest (the editor shows the known mapping alone); the seat's EP-10.",
           "`KeyboardMapping.cpp:262-272` skips a trigger `checkTriggerExists` refuses; `:292-294` keeps a mapping only with a trigger; `GetString` with no `IsString` at `:251`, `:254`, `:257`, `:265-266`, `:271-272`, `:282-283`, `:288-289`, and no `IsObject` at `:246-250`; the build defines NDEBUG.",
           "`fromP2k` (`:432`); `isValid` (`:499-509`, PL-26); the editors (T31's `GuiKeyMappingEditor`, `GuiKeyboardtopads`).",
           "Which malformed values crash and which misread on a device (input-dependent, EP-10)."),
 "PL-14": ("L-01 at stage B; the read trace; G-09 `CANNOT` (no account); the seat's EP-13 (the callers corrected).",
           "`NetworkThread.cpp:21-25` calls `ResetComponent`, which takes `mWatchersLock` (`WatchersManager.cpp:92-100`); the watcher thread holds it across every `check()` (`:181-199`), including the token check's sign-in (`NetworkThread.cpp:120-178`); the callers are `GuiRetroAchievementsSettings.cpp:805-806` and `NetworkThread.cpp:257`.",
           "The update check (`:87-95`) and pads (`:58`) under the same lock; unregistering deletes the `WatcherInfo` (`WatchersManager.cpp:80-86`).",
           "The wait's length on a device (the sign-in's own bound, outside the packet)."),
 "PL-15": ("L-18 at stage B; the bounds row (`timeout 90`, sound).",
           "`CloudOffer.cpp:37` runs `timeout 90 /usr/bin/cloud_setup --seed-folders saves`; `:42-45` choose DONE or COULDN'T CREATE IT from rc alone.",
           "`ThreadedCloudSync.cpp` and `GuiCloudTransfer.cpp` (the offer's callers); the script's `>>> why` lines (the rclone slice).",
           "Whether `cloud_setup --seed-folders` exits 0 without creating the folder on some provider (the script's half)."),
 "PL-16": ("L-03 and the writes table at stage B (`t33-writes.py`); T21 PL-20 / #1186; the seat's EP-3 and EP-20.",
           "`CaptureRotation.cpp:175` and `KeyboardMapping.cpp:426`, `:429` call `writeAllText` in place, the result unread; `Gamelist.cpp:307-308` removes the file, then saves.",
           "PL-24 (the rotation cache after the write); PL-01's three gamelist writes; PL-05's collections writes.",
           "A power loss mid-write on a device."),
 "PL-21": ("The seat's EP-42, read by the first reader at `OfflineAchievementsText.cpp:183-200`.",
           "`parseUnlocks` (`:183-200`) rejects only a boolean-false `Success` (`:187`); a missing or non-bool `Success` passes; entries that are neither int nor string are skipped; `ok = true` at `:199`. The patch and set readers (`:99-112`, `:120-148`) set `ok` without the check.",
           "T20's delta on the same file (the collision); the consumers in `RetroAchievements.cpp` and `OfflineAchievements` (outside the slice).",
           "What the proxy sends on an error today (its own code, outside the slice)."),
 "PL-22": ("The seat's EP-44, read by the first reader at `FileFilterIndex.cpp:146-160` and `:1102-1105`.",
           "`clearIndex(std::map<std::string, int> indexMap)` (`:1102-1105`) takes the map by value; `resetIndex` (`:154-160`) calls it for every facet.",
           "`populateCustomCollection` (`CollectionSystemManager.cpp:1114`) calls `resetIndex` before repopulating; the filter pages read the facet maps.",
           "The stale values on a frame (an integration-window check)."),
 "PL-23": ("The seat's EP-39, read by the first reader at `NetworkThread.cpp:260-272` and `GuiRetroAchievementsSettings.cpp:793-799`.",
           "The check snapshots the credentials (`NetworkThread.cpp:130-138`) and posts only the token; `:266-270` writes it to SystemConf with no account or generation check; turning achievements off clears it (`GuiRetroAchievementsSettings.cpp:795-796`).",
           "PL-06's direct post at `:266`; PL-14's lock.",
           "The race's timing on a device."),
 "PL-24": ("The seat's EP-40 and EP-41, read by the first reader at `CaptureRotation.cpp:100-110` and `:174-181`.",
           "`write()` calls `writeAllText` (`:175`) without reading its result, then caches the turns with the destination's mtime (`:179-180`); `read()` answers from `sKnownAt` when the mtime matches (`:103-108`), before the uncached probe at `:113`.",
           "PL-16's write at `:175`; the cloud's saves tier, which replaces `.rotation` files.",
           "The frequency of a same-mtime replacement on a device."),
 "EP-47": ("The seat's EP-47, read by the first reader at `ThreadedBluetooth.cpp:36-60`; L-10 at stage B.",
           "`ThreadedBluetooth`'s constructor starts the worker (`:19`); `run()` deletes the object and clears `mInstance` (`:39-47`); `start()` assigns `mInstance = new ThreadedBluetooth(window)` (`:58`) after the constructor returns, so a fast scan publishes a freed pointer; nothing synchronises `mInstance` (`:10`, `:27`, `:47`, `:52`, `:58`). The format path repeats it (`:76`, `:110-122`).",
           "`ContentInstaller.cpp:61`, `:247` (L-10's other self-deleting worker); `ZaparooSupport.cpp:22-27`'s detached thread.",
           "How fast the scan returns on a device with no adapter."),
}
EP47 = """## EP-47 (part of PL-19)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** EP-47, L-10 -- proved: tree (`ThreadedBluetooth.cpp:36-60`, the first reader's read)
- **Owner area:** `es-app/src/ThreadedBluetooth.cpp:10-60`, `:76`, `:110-122`
- **What:**
  - The worker starts in the constructor (`:19`) and can finish, `delete this` and clear `mInstance` (`:39-47`) before `start()` publishes the new object (`:58`). A fast scan therefore publishes a freed pointer, and the next `start()` sees a scan "already running" or touches freed memory. `mInstance` is read and written with no lock. The format path repeats the pattern.
- **Fix shape:**
  - publish before the worker starts, under a lock; the worker clears it under the same lock; the format path the same.
- **Can this be done on the VM?** Yes. A fixture over the class with a scan double that returns at once, under ASan (`fix-unit-test`); the guest has no Bluetooth adapter, so no frame.
- **Already written:** nothing inherited. The object lives in memory only.
- **Acceptance:**
  - [ ] A fixture whose scan returns before `start()` publishes FAILs at the pin under ASan and passes on the fix (`stage-e/`).
"""
PLS = ["PL-01", "PL-02", "PL-03", "PL-04", "PL-05", "PL-06", "PL-07", "PL-08", "PL-09", "PL-10", "PL-11", "PL-12", "PL-14", "PL-15", "PL-16", "PL-21", "PL-22", "PL-23", "PL-24", "EP-47"]
text = open(sys.argv[1], encoding="utf-8").read()
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
n = 0
for pl in PLS:
    if pl == "EP-47":
        sec, title = EP47, "Bluetooth's scan can publish its own freed object: the worker deletes itself before `start()` assigns it"
    else:
        m = re.search(r"^## %s: (.*)$" % pl, text, re.M)
        title = re.sub(r"\s*\([^()]*\)\s*$", "", m.group(1))
        end = text.find("\n## ", m.end())
        sec = text[m.start():end].rstrip()
        sec = re.sub(r"^## (PL-\d+): .*$", r"## \1", sec, count=1, flags=re.M)
    assert "**Already written:**" in sec and "**Can this be done on the VM?**" in sec, pl
    how, src, sib, cannot = TRACE[pl]
    body = ("Found by T33 (#680), the audit of EmulationStation's system layer (`docs/audits/2026_10_27-epic-m6-es-app-system/` on `feature/m6-es-app-system-680`; the audit issue #1270), read at the ES pin `16dbac5211`. The section below is `05-punch-list.md`'s, copied; the ruling is the coordinator's (%s).\n\n" % RULE
            + sec + "\n- **Ruled (%s):** %s\n\n" % (RULE, RULING[pl])
            + "## Code trace\n\n- **How it was found:** %s\n- **The defect at its source (the pin):** %s\n- **Siblings hunted:** %s\n- **What reading cannot prove:** %s\n\n" % (how, src, sib, cannot)
            + "## Acceptance criteria\n\n- [ ] The item's positive FAILs on the pin and PASSes on the stream's commit: `stage-e/<stream>-before.txt` and `-after.txt` in the audit folder, as the item's **Acceptance** lines above describe.\n- [ ] `02` § The streams carries the stream's row with this bug's `Already written:` answer, and `05`'s Phase 7 row names the commit.\n")
    open(os.path.join(out, pl + ".title"), "w").write("Bug: EmulationStation: %s (T33 %s)" % (title, pl if pl != "EP-47" else "PL-19 EP-47"))
    open(os.path.join(out, pl + ".md"), "w").write(body)
    n += 1
assert n == 20, n
print("t33-file-bugs: %d bodies written to %s" % (n, out))
