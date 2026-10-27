# Retrospective audit — M6.P2 T33, EmulationStation's system layer (#680)

Read at the ES pin `16dbac5211` over the 77 paths of brief § 2: the game lists, the collections, the metadata and the filters; the fork's 17 helper units; the surfaces outside the lanes; and the Windows and console residue. The tables are `02`'s. The proofs are `stage-c/runs.txt` (nine harnesses, each FAIL at the pin and PASS under its control) and `02` § The guest cycle (the window, labelled `image`).

## 3.1 Architectural coherence

- **The fork's helpers are where the fork's rule is kept.** The pure `*Text` units, `CloudFolderValidation`, `CheevosIndex`, `CheevosRetry` and `WifiText` are string-in/string-out and fail closed, and seven of them have cases that every lane builds. The five header-only units (`AppWindow.h`, `FolderMerge.h`, `JourneyTiers.h`, `RunLock.h`, `TextFit.h`) had case files that no lane had built. Built at stage C, they pass, 18 of 18 (`stage-c/build-pin.txt`).
- **The fork wrote a rule and did not apply it everywhere.** `AppWindow::post` exists to drop a worker's post once the loop ends (F-ES-26). NetworkThread's five posts call `Window::postToUiThread` directly (L-12, `stage-c/l12-network-posts.py`). The rule holds in the files written after it, and not in the one written before it.
- **The library has two kinds of writer, and the cache knows only one.**
  - Through `Utils::FileSystem`, whose writes drop their path from the session cache (T21's file, cited).
  - Through `std::ofstream` and `pugi::save_file`, whose writes do not: `Gamelist.cpp:308`, `:474`, `:622`, `:841`; `FileFilterIndex.cpp:1313`; `CollectionSystemManager.cpp:345`.

  None of the nine compiled writes is temp-and-rename (`02` § The writes). The fork's own atomic writer (`AtomicFileUtil`, JourneyTiers' `AtomicFile::writeText`) is used by none of them.
- **A dynamic collection is the bundle's child, by identity.** `CollectionSystemManager.cpp:1302` adds the collection system's own root folder to the custom collections bundle. Any clear of that root deletes what the bundle's view points at, which is L-06's mechanism (3.5 below).

## 3.2 Project conformance

- **D-CLOUD-078 (temp-and-rename):** not met by any of the nine compiled writers. Two of them carry a player's data: `gamelist.xml` (game content, synced) and the collections' `.xcc` and `custom-<name>.cfg` (settings tier). 3.13 proves the gamelist write is in place (the same inode after the save).
- **D-CLOUD-049 (`gamelist.xml` is game content and is restored):** broken end to end by L-05. A `gamelist.xml` that arrives after the session's first look is read as absent and overwritten with the dirty entries alone (3.13 on the host; G-04 on the image, with its control).
- **D-UI-051 (every string ships in English and French):** met for the 196 msgids the 77 pass through `_()`. Three player words never pass through it: FileTag's IN PROGRESS, DROPPED and ON HOLD (L-25, 3.29).
- **`es-ui-style-guide.md` § Confirmations:** CloudOffer's two dialogs put NOT NOW last, where back lands. The scraper search's two upstream boxes do not use the fork's dialect: one is an English sentence through `toUpper` with a bare `"FINISH"`, and one carries a tool's error text (`02` § The words; outside the lanes).
- **D-UI-039 (the map):** two pages and one row are absent from `docs/es-menu-map.md`. `tools/es-menu-map-check` cannot see the pages, because their titles are passed in a member initializer (`02` § The structure). The coordinator recorded this as #951/#965's class.

## 3.3 Spec fidelity

The brief's figures, read at the pin, all hold (stage A; `02` § The runs). Where a reading sharpens or corrects the brief:
- **L-05:** the loss is total for the restored entries, not a stale read alone. `updateGamelist` starts from an empty `<gameList>` (`:427`).
- **L-06:** only a **dynamic** collection takes the repopulate path (`:1573`). G-02's plain custom collection could not show it.
- **L-28:** the mapping is dropped whole (`KeyboardMapping.cpp:292` keeps a mapping only with a trigger), not "an action with no trigger".
- **3.31:** the region is one string, so `usa, europe` reads region `us` alone.
- **`app-unit-tests`:** its CMakeLists puts no `fakes/` before `es-app/src` for this target (the brief said it did).
- **The bounds' "HttpReq lines":** these count every mention. The constructions are four, two of them live.

## 3.4 Platform conformance

- **Shipped build flags:** the recipe builds with NDEBUG (T32's finding), so the rapidjson reads in `KeyboardMapping.cpp`'s `load` (`:240-290`, `GetString` on any `type`, `mode`, `description` and `trigger` without `IsString`) are wild reads on a malformed `.keys` file in the shipped build, not assertions. This is recorded with L-28 for the stream; the harness proves only the dropped mapping.
- **Busybox and paths:** nothing in the slice shells out except `CloudOffer.cpp:37` (`timeout 90`, bounded) and the Windows residue.
- **The image:** the guest confirmed the paths the reads table assumes: `gamelist.xml` beside the ROMs, `recovery/<system>/` under the user's ES folder and emptied by a clean exit, `<rom>.keys` beside the game, and `/storage/.emulationstation` as a symlink to `.config/emulationstation`.

## 3.5 Cross-system interaction audit

### Interaction: the cloud's game-content restore x `Gamelist.cpp:413`'s cached read x the exit's `updateGamelist`
A restore writes `gamelist.xml` outside ES. The cache answers `:413` with the miss it remembered. The next save of any dirty game (a favourite, a play count) writes a `<gameList>` holding the dirty entries alone over the restored file. The player loses every scraped description and picture reference the restore brought. proved: 3.13 (host, FAIL then control PASS); G-04 (image, with a control system byte-identical).

### Interaction: EDIT DYNAMIC COLLECTION FILTERS x `reloadCollection(name, true)` x `ViewController::reloadGameListView`
From the bundle's view, with the cursor on a game in a dynamic collection, a filter change reloads the collection. `populateCustomCollection` clears the collection's root, which is the bundle's child (`:1302`). The reload then reads the freed cursor (`ViewController.cpp:1140-1142`), the #246 shape. proved: `stage-c/l06-reload-collection.py` (a heap-use-after-free under ASan at the pin; the control, reading the cursor before the clear, is clean). Not reproduced on the guest: G-02 drove a plain collection.

### Interaction: the scrape page's stop x `ScraperAsyncRequestsBuilder`'s thread x a slow token or hash
`stop()` and the destructor drop the builder while its thread runs `Scraper::search`. The class has no destructor and never joins or deletes its thread, so the thread writes into freed memory when the search returns. proved: `stage-c/l07-search-builder.py` (a heap-use-after-free at the pin; the control's destructor is clean).

### Interaction: `main()`'s end x `AppWindow::closing()` x NetworkThread's watchers
Between `closing()` (`main.cpp:1322`) and `WatchersManager::stop()` (`:1330`), a watcher's check can still post directly. Its task lands in a queue no loop will run, and `:266`'s token write is such a task. Sound by order, unsound by the fork's own rule. proved: `stage-c/l12-network-posts.py`.

### Interaction: a deleted custom collection x the session cache x the writers that bypass it
`deleteCustomCollection` (`:1610`, `:1613`) asks the cache for a file `std::ofstream` wrote this session. If an earlier read remembered the miss (`:963` reads the same `.xcc` path), the delete returns false and the file stays. Read, not run (`02` § The reads).

## 3.6 Time to play

- **Interface to a game's first frame:** nothing in the slice sits on the launch path, except `DisplayAspect`'s screenshot walk (L-04) on the first SCREENSHOTS look after a library change. On the guest, SCREENSHOTS changed 0.1 s after the press, over 100 captures and a four-game library. That does not price L-04 on a real library, which is the integration image's `time-to-play` cell.
- **A game's exit to the next first frame:** `CaptureRotation`'s read of `/var/log/exec.log` and `retroarch.cfg` after every RetroArch exit, on the interface thread (L-02). The log is bounded by the launcher's truncation; `retroarch.cfg` is bounded by nothing. Not measured here: the window launched no game.
- **The first frame:** waits for every system's `gamelist.xml` parse, the filter index and the collections (`02` § The library). The fixes proposed add one uncached `exists` per system at save time, not at startup.
