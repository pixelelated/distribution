# T33 (#680) stage C: the floor's 35 non-harness rows, read at the pin

**Read by a read-only subagent** (an Explore agent of this session, 19:18 to 19:32 UTC), given the 41-row table carried in `02` § The leads and the pin's sources under `/workspace/tmp/m6-t33/pin/`. It was told to call a defect PRESENT only for a concrete input. The six FAIL-at-pin rows (3.9, 3.13, 3.21, 3.29, 3.31, 3.35) are the fixtures in `stage-c/runs.txt`, not this read.

**Re-read by the first reader at their lines** before anything is carried to `05`. Each is marked **[re-read]** below:
- **3.8:** `Genres.cpp:304` returns `mGenres[g->second]` with `g` the end iterator from `:295` (the loop's `sg` was meant). `:299`'s `name.find("/") >= 0` is always true (`size_t`). This is undefined behaviour for any genre name not found whole that has a known subgenre after `/`.
- **3.1:** `PlatformId.cpp:28` `{ "bbc", BBC_MICRO }` and `:171` `{ "bbc", ACORN_BBC_MICRO }`.
- **3.5:** `MetaData.cpp:568` `set(mdd.id, source.get(mdd.id))` after the skips at `:560-566`, which skip an empty cartridge and a negative rating only.
- **3.10's aside:** `FileFilterIndex.cpp:579-580`, two `int[65000]` arrays on the stack, about 520 KB.
- **3.20's sibling:** `FileData.cpp:1659` `if (currentSortId > FileSorts::getSortTypes().size())` lets `.at(28)` throw (outside the slice; T2 FD-15 / #771's file).

The remaining verdicts are the subagent's, carried as it gave them. **Counts (its line):** PRESENT 16, ABSENT 18, NO-DEFECT-CLAIM 1, UNCLEAR 0.

**Its line corrections:**
- `MetaData.cpp`'s `+N` (3.3, 3.6, 3.7) count from `:150`.
- 3.14's from `:111`.
- `ArcadeSystems` starts at `:236`.
- `gameDecls` runs `:30-101`.
- `getInt` starts at `:449`.
- CaptureRotation's comment is `:26-30`.

| # | Verdict | Lines | The concrete input -> what happens |
| --- | --- | --- | --- |
| 3.1 | PRESENT [re-read] | `PlatformId.cpp:28`, `:171` | `getPlatformId("bbc")` is BBC_MICRO; the second `bbc` row (ACORN) is never stored; ACORN is reachable only as `bbcmicro`. Nullptr handled `:217-218`; every enum has a row; keys lowercase |
| 3.2 | ABSENT | `MetaData.cpp:30-101` | no key twice; `Emulator`/`Core` are in the two halves of `#if WIN32 && !_DEBUG` (`:42-43` / `:46-47`) |
| 3.3 | PRESENT | `MetaData.cpp:303`, `:313` | a player's explicit default is dropped under `ignoreDefaults` (reloads as the same value); a path outside the start path stays absolute; `/storage/roms/snes2/a.png` against `/storage/roms/snes` becomes `.//a.png` (`FileSystemUtil.cpp:986-991`'s prefix match) |
| 3.4 | PRESENT | `MetaData.cpp:392-404` | `set(Genre, "")` with no genre stores nothing but sets `mWasChanged` (`:404`); `getInt("3x")` is 3 (atoi) |
| 3.5 | PRESENT [re-read] | `MetaData.cpp:568` | a game with developer "Capcom", a scrape with none: the field becomes `""`; the release date "not-a-date-time"; the favourite flag is safe (`:532`) |
| 3.6 | ABSENT | `MetaData.cpp:272-276` | a node with only `<hash>` keeps it as crc32; only `<crc32>A</crc32><hash>B</hash>` loses B (`:191-192`) |
| 3.7 | ABSENT | `MetaData.cpp:216-220` | `TRUE` is lowercased; aside: `"true "` with one trailing space is kept and reads false (`:397`) |
| 3.8 | PRESENT [re-read] | `Genres.cpp:244-248`, `:295-305`; `FileFilterIndex.cpp:1015-1016` | ids "11,12", both children of 10: the parent is counted twice for one game; **`fromGenreName` `:304` reads the end iterator** (e.g. "Foo / Shooter"); a trailing comma is ABSENT |
| 3.10 | ABSENT (aside PRESENT [re-read]) | `FileFilterIndex.cpp:563-575`, `:632-641`; `:579-580` | the distance stays in 0..1, symmetric over the strings tried; **aside:** two `int[65000]` on the stack, and a string of 65,001 characters writes past them |
| 3.11 | ABSENT | `FileFilterIndex.cpp:1178-1225` vs `:1243-1311` | every tag `save` writes has a `load` branch; the genre goes through a name, so 3.8's `:304` is reached on a failed lookup |
| 3.12 | ABSENT | `Gamelist.cpp:279` | a game under the start path is written `./name`; absolute only for a file outside it |
| 3.14 | PRESENT | `Gamelist.cpp:177`, `:185-195` | `<path>./Game.sfc\n</path>`: the newline is kept and the lookup misses (`:194`); a trailing `\` is ABSENT |
| 3.15 | PRESENT | `Gamelist.cpp:705`, `:762-768` | a cached miss for `images/x-image.png`, the file copied in, then CLEAN GAMELISTS with no launch: the reference is removed (L-05's family) |
| 3.16 | PRESENT | `CollectionSystemManager.cpp:1510` | `getFilteredCollectionPath("../evil")` leaves the folder; every caller found sanitises first (`getValidNewCollectionName`), so no current path reaches it |
| 3.17 | PRESENT | `CollectionSystemManager.cpp:627-651` | `themeFolderExists` is never called; a theme folder's name (`zxspectrum`) is accepted as a new collection's name; `all` is ABSENT (`:650`) |
| 3.18 | ABSENT | `CollectionSystemManager.cpp:1450` | `custom-.cfg` excluded; `custom-a.cfg.bak` only logged |
| 3.19 | ABSENT | `CollectionSystemManager.cpp:39-104` | names and theme folders unique; `recent` is declared ascending (`:40`) and forced descending (`:538`) |
| 3.20 | ABSENT (sibling PRESENT [re-read], outside the slice) | `CollectionSystemManager.cpp:538-540`; `FileData.cpp:1659` | the id is set just before the `.at()`; the off-by-one is `FileData.cpp:1659` (`>` for `>=`): `<sys>.sort=28` throws |
| 3.22 | ABSENT | `KeyboardMapping.cpp:403-406` | rapidjson's writer escapes a quote; save then load keeps the sets |
| 3.23 | ABSENT | `KeyboardMapping.cpp:171-172` | no key has two `_`; aside: BTN_LEFT/RIGHT's p2k names are shadowed by KEY_LEFT/RIGHT |
| 3.24 | ABSENT | `CustomFeatures.cpp:29` | a trailing space is trimmed |
| 3.25 | ABSENT | `CustomFeatures.cpp:211-216`, `:242-290` | core features are stored; aside: `:222` then `:227` overwrite `autosave` |
| 3.26 | PRESENT | `CustomFeatures.cpp:531`, `:536` | exact case: `value="Ratio"` against `hasFeature("ratio")` is false |
| 3.27 | ABSENT | `FileSorts.cpp:96-106` | only a whole first word is stripped; `_("A,AN,THE")` is translated once into a function static (`:83`) |
| 3.28 | PRESENT | `FileSorts.cpp:38` | `getSortType(-1)` returns row 0 |
| 3.30 | ABSENT | `LibretroRatio.cpp:15-40` | 26 keys unique; every value but `auto` is a RetroArch ratio |
| 3.32 | PRESENT | `LangParser.cpp:225-226` | `<lang>ja</lang>` with no region asks for `:/flags/ja.png`, which does not exist (`DetailedContainer.cpp:892`) |
| 3.33 | NO-DEFECT-CLAIM | `CaptureRotation.cpp:45-53` | a table read once and kept, a miss included; by design (the image's read-only tree) |
| 3.34 | PRESENT | `SystemRandomPlaylist.cpp:28-30`, `:75`, `:87` | art copied in after the playlist is built is never returned until `resetCache`; L-11's family |
| 3.36 | ABSENT | `JourneyTiers.h:63-64`, `:85-86` | a two-byte record reads unknown (offer everything); a failed write with nothing left is NoRecord |
| 3.37 | PRESENT | `FolderMerge.h:50-52` | `Game.sfc` renamed `game.sfc` on disk: the live node vanishes (collections drop it) and the fresh one arrives; by design per path identity |
| 3.38 | PRESENT | `RunLock.h:68` | L-14: the lock held, its pid reused by `tail -f /var/log/raofflineproxy-ctl.log`: that pid is returned; a stale lock is ABSENT |
| 3.39 | ABSENT | `GameCubeRvzHashRetry.h:32-43` | a valid unknown hash is not retried |
| 3.40 | ABSENT | `AppWindow.h:40-44` | after `closing()` nothing posts; `open()` is process-wide |
| 3.41 | PRESENT | `OfflineAchievementsText.cpp:229`, `:17-20` | L-17: `"4294967297 1700000000"` reads id 1, accepted; `jsonInt` truncates the same way |
