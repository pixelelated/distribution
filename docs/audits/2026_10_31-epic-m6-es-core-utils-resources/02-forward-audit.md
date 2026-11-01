# Forward audit: M6.P2 T36, EmulationStation's utilities, resources and renderers (#683)

- **At:** the pin `16dbac5211eea7e70db7394372033be2be7df829` (ES) and `a5fbd75d61` (distribution, stage A's tip). Stage B, the T1 session (Opus 5.5, high).
- **The 58 paths:** `es-core/src/{utils,resources,renderers}/**` less `utils/AtomicFileUtil.*` (`stage-a/paths.txt`).
- **Generated sections:** each generated table sits between `<!-- gen:NAME -->` markers. It is written by `tools/t36-tables.py --write 02-forward-audit.md`, read back by `--check`, and ends with its own "generated, asserted" line. The script exits 1 before writing when a count drifts. Its constructed drifts are `stage-b/tables-drift.out`.
- **What stage B did not do:** no case ran (stage C), no guest started (the window is asked for on #683), and no fix was made (stage E, under a stream brief).
- **`proved:` values:**
  - `tree`: read at the pin.
  - `tool-run`: a stage-A run in `stage-a/runs.out`.
  - `pending stage C` / `pending window`: owed.

## Coverage

All 58 paths. Each row gives its provenance against the merge base, its inventory tier, whether its blob is ROCKNIX master's, batocera's commits on it since `1750dded8c`, and the section that reads it.

<!-- gen:coverage -->
| Path | Lines (`grep -c ''`) | Against the merge base `cada856d86` | Inventory tier | Blob = ROCKNIX `f6c542872e` | Batocera commits since `1750dded8c` | Read under (`02` §) |
| --- | --- | --- | --- | --- | --- | --- |
| `es-core/src/renderers/GlExtensions.cpp` | 140 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/GlExtensions.h` | 88 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Renderer.cpp` | 1170 | upstream-carried | upstream-carried | yes | 2 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Renderer.h` | 263 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Renderer_GL21.cpp` | 459 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GL21.h` | 53 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES10.cpp` | 422 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES10.h` | 53 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES20.cpp` | 1420 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES20.h` | 67 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES30.cpp` | 2291 | upstream-carried | upstream-carried | yes | 1 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Renderer_GLES30.h` | 69 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Shader.cpp` | 642 | upstream-carried | upstream-carried | yes | 1 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Shader.h` | 146 | upstream-carried | upstream-carried | yes | 1 | the device reads, the renderers and the words; the structure |
| `es-core/src/resources/Font.cpp` | 1311 | fork-modified | fork-own | no | 4 | the texture and font caches (the font) |
| `es-core/src/resources/Font.h` | 217 | fork-modified | fork-own | no | 1 | the texture and font caches (the font) |
| `es-core/src/resources/ResourceManager.cpp` | 258 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/ResourceManager.h` | 64 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TabStops.h` | 49 | fork-added | fork-own | no | 0 | the texture and font caches (the font) |
| `es-core/src/resources/TextureData.cpp` | 739 | fork-modified | fork-own | no | 2 | the texture and font caches |
| `es-core/src/resources/TextureData.h` | 126 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TextureDataManager.cpp` | 381 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TextureDataManager.h` | 108 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TextureResource.cpp` | 348 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TextureResource.h` | 74 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/utils/CommandLineUtil.h` | 104 | fork-added | fork-own | no | 0 | the structure (fork files whole) |
| `es-core/src/utils/ConcurrentVector.h` | 92 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/Delegate.h` | 27 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/FileSystemUtil.cpp` | 1805 | upstream-carried | upstream-carried | yes | 1 | the file cache; the paths; the writes and reads |
| `es-core/src/utils/FileSystemUtil.h` | 103 | upstream-carried | upstream-carried | yes | 0 | the file cache; the paths; the writes and reads |
| `es-core/src/utils/HtmlColor.cpp` | 248 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/HtmlColor.h` | 18 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/MathExpr.cpp` | 1016 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words (the `_(` line) |
| `es-core/src/utils/MathExpr.h` | 75 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words (the `_(` line) |
| `es-core/src/utils/OfflineProxyUrl.cpp` | 21 | fork-added | fork-own | no | 0 | the structure (fork files whole) |
| `es-core/src/utils/OfflineProxyUrl.h` | 40 | fork-added | fork-own | no | 0 | the structure (fork files whole) |
| `es-core/src/utils/Platform.cpp` | 956 | fork-modified | fork-own | no | 1 | the processes; the device reads |
| `es-core/src/utils/Platform.h` | 100 | fork-modified | fork-own | no | 0 | the processes; the device reads |
| `es-core/src/utils/Randomizer.cpp` | 53 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/Randomizer.h` | 19 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/StringListLock.cpp` | 61 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/StringListLock.h` | 30 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/StringUtil.cpp` | 1706 | fork-modified | fork-own | no | 0 | the device reads, the renderers and the words (case helpers); the processes (`shellQuote`, `maskSecrets`) |
| `es-core/src/utils/StringUtil.h` | 96 | fork-modified | fork-own | no | 0 | the device reads, the renderers and the words (case helpers); the processes (`shellQuote`, `maskSecrets`) |
| `es-core/src/utils/ThreadPool.cpp` | 230 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/ThreadPool.h` | 77 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/TimeText.cpp` | 83 | fork-added | fork-own | no | 0 | the device reads, the renderers and the words |
| `es-core/src/utils/TimeText.h` | 57 | fork-added | fork-own | no | 0 | the device reads, the renderers and the words |
| `es-core/src/utils/TimeUtil.cpp` | 634 | fork-modified | fork-own | no | 0 | the device reads, the renderers and the words |
| `es-core/src/utils/TimeUtil.h` | 99 | fork-modified | fork-own | no | 0 | the device reads, the renderers and the words |
| `es-core/src/utils/Uri.h` | 144 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/VectorEx.h` | 170 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/ZipFile.cpp` | 369 | upstream-carried | upstream-carried | yes | 0 | the writes and reads; the structure (reading scope) |
| `es-core/src/utils/ZipFile.h` | 51 | upstream-carried | upstream-carried | yes | 0 | the writes and reads; the structure (reading scope) |
| `es-core/src/utils/han.h` | 20923 | upstream-carried | upstream-carried | yes | 0 | the structure (reading scope) |
| `es-core/src/utils/md5.cpp` | 369 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/md5.h` | 95 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/zip_file.hpp` | 10011 | upstream-carried | upstream-carried | yes | 0 | the writes and reads; the structure (reading scope) |

generated, asserted: 58 rows (`tools/t36-tables.py --print coverage`)

Totals: fork-added 6, fork-modified 9, upstream-carried 43; inventory fork-own 15, upstream-carried 43; 43 of 58 blobs identical to ROCKNIX's master; batocera 13 commits on 9 files since `1750dded8c`.
<!-- /gen:coverage -->

## The leads

- **The table:** L-01 to L-18 are the brief's (R2 and R3). L-19 is stage B's own (§ The file cache).
- **The floor:** 3.1 to 3.25 are the brief's floor; 3.26 is stage B's case for L-19. Every case runs at stage C.
- **Family:** a lead's family is the brief's natural home for it (§ 4's opening paragraph).

<!-- gen:leads -->
| Lead | Lines at the pin | Family | Owner | Disposition at stage B | proved: |
| --- | --- | --- | --- | --- | --- |
| L-01 | `utils/StringUtil.cpp:357-362`, `:398-403` against `:352-356`, `:393-397`; tables `:76`, `:93`, `:153`, `:170`; lookup `:184-200` | a player sentence | T36 | case 3.1 at stage C (FAIL at the pin expected); a fix only under a stream brief | tree |
| L-02 | `utils/FileSystemUtil.cpp:1369-1379`, `:1400-1427` | a write's claim | T20 (#1177, `d9afa5c7c`) -- collision | control 3.4 at stage C, never re-fixed here; § The merge debt | tree |
| L-03 | `utils/FileSystemUtil.cpp:1451-1452`, `:1454-1455`, `:1463`; `:1472-1474`, `:1492`, `:1500-1504` | a write's claim | `renameFile`: T21 (#1191, `f7c16144d`) -- collision; `copyFile`: T36 | case 3.2 at stage C; `copyFile`'s half this slice's (rule 6) | tree |
| L-04 | `utils/FileSystemUtil.cpp:1429-1446`; `es-app/src/ThreadedCloudSync.cpp:943-948` (T18's) | a write's claim | the pause (#1186, T21 PL-20); call sites their owners' | text case 3.3; the return or the supersession put to the stage-D pause | tree |
| L-05 | `utils/Platform.cpp:40`, `:52`, `:162-168` | a process's contract | T36 (ruling (j): T35's PL-03 fix is `Scripting`'s) | 3.5's two host rcs at stage A; G-07 reads `SigIgn` first (errata), then the image's shell and wrapper | tree |
| L-06 | `utils/Platform.cpp:891-905` | a process's contract | T26 (#1225, `a5d2d3756`) -- collision | control 3.9 at stage C, never re-fixed here; § The merge debt | tree |
| L-07 | `resources/Font.cpp:1238`, `:1255`, `:165-166`, `:99-101` | a layout computed from a moving number | T36 | case 3.16 at stage C; G-02 and G-06 frames | tree |
| L-08 | `resources/Font.cpp:107`, `:115-117`, `:420-421`; `es-code-traps.md:118`; T34 L-02 (`es-core-components.md:597`) | a layout computed from a moving number | the coordinator's rule sweep (erratum against `es-code-traps.md:118`); T34 PL-17 beside it | positive 3.8 at stage C; recorded as a rule erratum | tree |
| L-09 | `resources/Font.cpp:728-731`, `:734-745`; the fork's `getTabStops`/`sizeTabbedText` `:833-941`; `:1044-1078` | a layout computed from a moving number | T36 | case 3.17 at stage C | tree |
| L-10 | `resources/TextureData.cpp:615-645`, `:670-725` against `:92-195` (`:95` the lock) | a lifetime or a thread | T36 | TSan case 3.11 at stage C | tree |
| L-11 | `resources/TextureDataManager.cpp:231-235`, `:252-253`, `:284`; `es-app/src/views/SystemView.cpp:198`, `:226` (T32's) | a lifetime or a thread | T36 | teardown case 3.12 at stage C | tree |
| L-12 | `utils/FileSystemUtil.cpp:277-282`, `:161-162`, `:183-198` | a read of a file another process writes | T36 (ruling (h): the cache's fix is T36's, T35's 3.11 the case) | positive 3.13 at stage C; T35's 3.11 re-run at T35's tips (ruling (h) as (a)) | tree |
| L-13 | `utils/Platform.cpp:853-880` | a process's contract | the coordinator's rule sweep (erratum against `es-native-ui.md:103`); #1220 the callers' | text case 3.7 at stage C; recorded as a rule erratum | tree |
| L-14 | `utils/StringUtil.cpp:446-804` (the `=` test inside `maskSecrets`) | a player's secret in a log | T36 | case 3.10 at stage C, its value built at run time | tree |
| L-15 | `utils/FileSystemUtil.cpp:1766-1797` | a lifetime or a thread | T36 | ASan case 3.6 at stage C | tree |
| L-16 | `utils/FileSystemUtil.cpp:1089-1120` | a write's claim | T36 | case 3.15 at stage C | tree |
| L-17 | `resources/Font.cpp:30-31`, `:177`, `:417`; `resources/TextureResource.cpp:12`, `:146`; `renderers/` | a lifetime or a thread | T36 | TSan programs 3.25 at stage C; the threads named in § The texture and font caches | tree |
| L-18 | `utils/Platform.cpp:235-237` | a lifetime or a thread | T36 | text case 3.24 at stage C (recorded) | tree |
| L-19 | `utils/FileSystemUtil.cpp:1067`, `:1080`, `:1084` (stage B's read) | a read of a file another process writes | T36 (new at stage B) | case 3.26 at stage C (FAIL at the pin expected); reaches #1263's `TextureData.cpp:336-339` | tree |

generated, asserted: 19 rows (`tools/t36-tables.py --print leads`)

| Case | At the pin | Function | Status | proved: |
| --- | --- | --- | --- | --- |
| 3.1 | `utils/StringUtil.cpp:357-362`, `:398-403`; tables `:76`, `:93`, `:153`, `:170` | `toUpper`, `toLower` in `es-unit-tests` | stage C | pending stage C |
| 3.2 | `utils/FileSystemUtil.cpp:1451-1455`, `:1463`; `:1472-1474`, `:1492`, `:1500-1504` | `renameFile`, `copyFile`, `FileSystemUtil.cpp` linked whole (T21's `es-fs-tests` shape) | stage C | pending stage C |
| 3.3 | `utils/FileSystemUtil.cpp:1429-1446` | `writeAllText` | stage C | pending stage C |
| 3.4 | `utils/FileSystemUtil.cpp:1369-1379`, `:1400-1427` | `readAllText`, `readAllLines` | stage C | pending stage C |
| 3.5 | `utils/Platform.cpp:162-164` | the wrap's literal, run by the host's shell | run at stage A: `seq 400 rc=0`, `seq 200000 rc=141` on `/usr/bin/dash` (`stage-a/runs.out`); G-07 the image's | tool-run |
| 3.6 | `utils/FileSystemUtil.cpp:1758-1798` (`:1773`, `:1775`, `:1788`, `:1797`) | `preloadFileSystemCache` under ASan | stage C | pending stage C |
| 3.7 | `utils/Platform.cpp:853-880` (`:879`) | `runSystemCommand`, lifted as text | stage C | pending stage C |
| 3.8 | `resources/Font.cpp:107`, `:115-117`, `:420-421`, `:754-757` | `getHeight` (FreeType and renderer stand-ins) | stage C | pending stage C |
| 3.9 | `utils/Platform.cpp:891-905` | `GetShOutput`, extracted | stage C | pending stage C |
| 3.10 | `utils/StringUtil.cpp:446-804` | `maskSecrets` in `es-unit-tests` (`MaskSecretsTests.cpp` exists) | stage C | pending stage C |
| 3.11 | `resources/TextureData.cpp:615-645`, `:670-725` against `:92-195` | a `san tsan-...` stand-in | stage C | pending stage C |
| 3.12 | `resources/TextureDataManager.cpp:215-235`, `:252-253`, `:284` | `TextureLoader`'s teardown, with a timeout | stage C | pending stage C |
| 3.13 | `utils/FileSystemUtil.cpp:48-341`, `:1122-1147`, `:161-162` | the cache, extracted in T35's `fs_cache`/`fs_exists` shape | stage C | pending stage C |
| 3.14 | T35's `window-input-tests` case 3.11 at T35's tip (`InputManager.cpp:1187` with `FileSystemUtil.cpp`) | re-run unchanged, never edited (ruling (h)) | re-run at stage C from T35's tips of that minute, named with the time and T35's stage (ruling (h) as (a)); again at the hand-back | pending stage C |
| 3.15 | `utils/FileSystemUtil.cpp:1089-1120` | `createDirectory` | stage C | pending stage C |
| 3.16 | `resources/Font.cpp:99`, `:161-165`, `:1238`, `:1255`; `Renderer.cpp:1149` doubled | the scaling, extracted | stage C | pending stage C |
| 3.17 | `resources/Font.cpp:714-752`, `:1044-1078` | `sizeText` against the cache's last vertex (stand-ins) | stage C | pending stage C |
| 3.18 | `utils/StringUtil.cpp:426-444` | `shellQuote` in `es-unit-tests` | stage C | pending stage C |
| 3.19 | `getEscapedPath` (`FileSystemUtil.cpp`) | linked whole | run at stage C; its output is held (D-WORKFLOW-215), only a neutral line in public | pending stage C |
| 3.20 | `getCanonicalPath` (`:726`, T2's line) | linked whole, ASan | run at stage C; its output is held (D-WORKFLOW-215), only a neutral line in public | pending stage C |
| 3.21 | the relative path (`:986`) | linked whole | stage C | pending stage C |
| 3.22 | `utils/TimeUtil.cpp:514-588` | `LocaleES` and `Settings` doubles | stage C | pending stage C |
| 3.23 | `resources/TextureDataManager.cpp:135-170` | `cleanupVRAM`, extracted | stage C | pending stage C |
| 3.24 | `utils/Platform.cpp:235-237` | `quitES`, lifted as text | stage C | pending stage C |
| 3.25 | `FileSystemUtil.cpp:331-332` (`shared_mutex`); `ThreadPool.cpp:26`, `:84`, `:91`; `StringListLock.cpp`; `ConcurrentVector.h` | `san()` TSan programs (R3 § 6 item 2) | stage C | pending stage C |
| 3.26 | `utils/FileSystemUtil.cpp:1059-1087` | `removeFile`, linked whole | new at stage B (L-19): `writeAllText(p)`; `exists(p)`; `removeFile(p)`; `CHECK_FALSE(exists(p))` -- FAIL at the pin expected | pending stage C |

generated, asserted: 26 rows (`tools/t36-tables.py --print leads`)
<!-- /gen:leads -->

**The three holds.** Stage B's two named reads were the archive extraction path with its caller read whole, and the scoped lead of ruling (k) on `getCanonicalPath`'s callers. Both were weighed under D-WORKFLOW-215. The Q3 read of `getEscapedPath`'s list, made while writing § The paths, was weighed the same way. **All three met the test.**
- Their records are off the tree at `/workspace/tmp/m6-t36/held/` (directory mode 700, files mode 600), with their sha256 values in `SHA256SUMS` there and in `00`.
- Nothing more about them is written on the tree or in public. Cases 3.19 and 3.20 run at stage C with their output written to the held directory, not here.

## The file cache

The cache is an `unordered_map<size_t, FileCache>` keyed by `std::hash` of the generic path, under one `shared_mutex` (`FileSystemUtil.cpp:331-337`).
- **Reads:** reads go through it only while `Settings::UseFileCache()` (`:203`). A miss is stat'ed with no lock held and stored (`:213-215`). A directory a listing has walked answers `absent` for every name it did not list, without a stat (`:277-282`, L-12).
- **Refresh:** `exists(p, false)` and the uncached `is*` fallbacks rewrite an entry through `fromStat64` (`:161-162`); **`FileCache::add` also overwrites an existing entry** (`:168-180`, a listing's write), and the WIN32 `fromStat64` uses `try_emplace` (no overwrite). So `fromStat64` is not the *only* writer (04 correction 2, the seat).
- **The key:** the key is the hash, not the path. Two paths whose hashes collide share one answer. That needs a 64-bit collision; it is recorded as the contract, not as a lead.

<!-- gen:filecache -->
| Entry point | At the pin | Lock | What it does | Its answer to a file another process wrote |
| --- | --- | --- | --- | --- |
| `FileCache::queryCacheEntry` | `:201` | shared, then unique for the insert | a hit answered under the shared lock; a miss stat'ed with no lock (`statKey`) and stored by `insertEntry` | the entry stands until an erase or the reset: a file created, removed or rewritten outside is not seen |
| `FileCache::insertEntry` | `:313` | unique (the caller's) | re-checks the key, then the parent's wildcard, then stores the stat | a listed parent stores `absent` without the stat it made (L-12) |
| `FileCache::getCacheEntry` | `:268` | shared (the caller's) | the key, else the parent's `/*` wildcard as a static `absent` | a listed directory answers `absent` for every name not listed |
| `FileCache::fromStat64` | `:138` | unique, after an unlocked `stat64` | overwrites the entry with the stat it made (`mFileCache[...] = cache`), with no `UseFileCache` gate | a refresh path (`exists(p, false)`, the uncached `is*`); `add` (`:168-180`) also overwrites, so not the only writer (04) |
| `FileCache::add` | `:168` | unique | a listing's entries and its `/*` wildcard (`getDirContent`, `getDirectoryFiles`) | a listing's snapshot; `_symlink` set only here, from `d_type` |
| `FileCache::remove` | `:183` | unique | erases the key and every ancestor's `/*` wildcard | the writers below call it; nothing outside ES does |
| `FileCache::resetCache / FileSystemCache::reset()` | `:258` | unique | clears the whole map | the only way a remembered answer about an outside write goes |
| `FileSystemCache::reset(file)` | `:348` | unique (through `remove`) | erases one key and its ancestors' wildcards | a caller that knows the path can drop it |
| `FileCache::isCached` | `:226` | shared | the key or the parent's wildcard present; never stats | says only that an answer is remembered |

generated, asserted: 9 rows (`tools/t36-tables.py --print filecache`)

| Writer | Erase lines | Lock | Order, read from the source |
| --- | --- | --- | --- |
| `removeDirectory` | `:1051` | unique (inside `remove`) | erase, then `rmdir`; nothing re-reads between |
| `removeFile` | `:1067` | unique (inside `remove`) | **erase, then `isDirectory(_path)` re-stats and stores `exists` (`:1080`), then `unlink` (`:1084`): the deleted path is left cached as present (L-19)** |
| `createDirectory` | `:1097` | unique (inside `remove`) | `exists(path, false)` rewrites, erase, then `mkdir`; the recursion's parents the same |
| `writeAllText` | `:1445` | unique (inside `remove`) | erase after `fclose`; skipped when `fopen` fails (nothing written) |
| `renameFile` | `:1457`, `:1458` | unique (inside `remove`) | erase both after `exists(dst, false)` and `removeFile(dst)`; the rename after the erase |
| `copyFile` | `:1506`, `:1507` | unique (inside `remove`) | erase both after the copy; skipped on an open failure |

generated, asserted: 6 rows (`tools/t36-tables.py --print filecache`)

| Function | Line | Lock | Kind | Erases |
| --- | --- | --- | --- | --- |
| `getDirContent` | `:364` | unique | a listing's write | -- |
| `getDirContent` | `:433` | unique | a listing's write | -- |
| `getDirectoryFiles` | `:479` | unique | a listing's write | -- |
| `getDirectoryFiles` | `:575` | unique | a listing's write | -- |
| `exists` | `:1145` | unique | a stat's write | -- |
| `isRegularFile` | `:1173` | unique | a stat's write | -- |
| `isDirectory` | `:1196` | unique | a stat's write | -- |
| `isDirectory` | `:1201` | unique | a stat's write | -- |
| `isSymlink` | `:1230` | unique | a stat's write | -- |

generated, asserted: 9 rows (`tools/t36-tables.py --print filecache`)

| Cited by | Line | The pin's function at that line | Image | The pin's text at that line |
| --- | --- | --- | --- | --- |
| T34's brief | `:144` | `fromStat64` | WIN32 only | `mFileCache.try_emplace(hashPath(key), ret == 0, ret == 0 && S_ISDIR(in` |
| T34's brief | `:185` | `remove` | built | `if (!Settings::UseFileCache())` |
| T34's brief | `:195` | `remove` | built | `mFileCache.erase(hashPath(parent + "/*"));` |
| T34's brief | `:203` | `queryCacheEntry` | built | `if (!Settings::UseFileCache())` |
| T34's brief | `:220` | `exists` | built | `return queryCacheEntry(key, [](const FileCache* e) { return std::optio` |
| T35 | `:296` | `statKey` | built | `bool exists = ret == 0;` |
| T35 | `:323` | `insertEntry` | built | `return mFileCache.try_emplace(hash, std::move(fetched)).first->second;` |
| T35 | `:1127` | `exists` | built | `if (enableCache)` |
| T35 | `:1131` | `exists` | built | `return *val;` |
| T35 | `:161` | `fromStat64` | built | `std::unique_lock<std::shared_mutex> guard(mFileCacheMutex);` |
| T35 | `:162` | `fromStat64` | built | `mFileCache[hashPath(key)] = cache;` |
| T33 | `:345` | `FileSystemCache::reset` | built | `FileCache::resetCache();` |
| T33 | `:348` | `FileSystemCache::reset` | built | `void FileSystemCache::reset(const std::string& file)` |
| T33 | `:350` | `FileSystemCache::reset` | built | `FileCache::remove(file);` |
| T33 | `:238` | `isRegularFile` | built | `static std::optional<bool> isRegularFile(const std::string& key)` |
| T26 | `:138` | `fromStat64` | built | `static int fromStat64(const std::string& key, struct stat64* info)` |
| T26 | `:1164` | `isRegularFile` | built | `bool isRegularFile(const std::string& _path)` |

generated, asserted: 17 rows (`tools/t36-tables.py --print filecache`)
<!-- /gen:filecache -->

- **L-19, stage B's lead (`proved: tree`; case 3.26 at stage C).**
  - **Ordering:** `removeFile` erases the path's entry (`:1067`), then asks `isDirectory(_path)` (`:1080`). That stats the still-present file through `queryCacheEntry` and stores `exists = true` (`insertEntry`). Then it unlinks (`:1084`).
  - **Result:** after a successful `removeFile`, `exists(p)` answers `true` from the cache until a refresh (`exists(p, false)`), an invalidation by another writer, or a reset -- ordinary cached reads do not repair it (04 correction 3, the seat: narrow the persistence wording, keep the functional priority). ES's own deleting writer leaves its path stale, so the brief's premise and #1263's (*"ES's own writers drop their entry, so only an outside writer is stale"*) do not hold for `removeFile`. `deleteDirectoryFiles` (`:1512-1531`) inherits it for every file it removes.
  - **Upstream:** ROCKNIX `f6c542872e` and batocera `b2ceb55a7e` have the same order: `FileCache::remove`, then `isDirectory(_path)` twice, then `unlink`, read by `grep -n` over each copy's `removeFile`.
  - **Fix shape (a stream's, not made here):** unlink or `rmdir` first, then erase.
- **#1271's question** (does `isRegularFile` share `exists`'s entry and remember a miss), answered from the source (`proved: tree`; #1271 read at 20:47 UTC with no comments; its body `:38` is the question).
  - **Shared entry: yes.** `FileCache::exists` (`:218-221`) and `FileCache::isRegularFile` (`:238-241`) are two lambdas over one entry found by one hash, and a miss stored by either answers both. The uncached `isRegularFile` (`:1164-1179`) rewrites that shared entry through `fromStat64`.
  - **Symlinks:** a symlinked regular file answers `false` from an entry a listing wrote, because `_symlink` comes from `d_type` there (`:433`, `:575`). It answers `true` from an entry a stat wrote: `stat64` follows the link, so `S_ISLNK` is never true at `:298` or `:152`.
- **T34 L-09** (`HttpReq.cpp:344`, `:479`, through `copyFile`'s erase `:1506-1507`): T34's answer *"sound at the pin"* stands for those two writes. The erase follows the copy, and `copyFile` does not re-read in between.
- **L-12 and the outside writer.** pugixml's `save_file`, `std::ofstream`, `std::rename` outside `renameFile`, libvlc's snapshot, and every other process write without erasing. The stored answer stands until a reset.
  - **The resets** (T33 L-05):
    - `ViewController.cpp:1208` and `:1434`;
    - `FileData.cpp:1113`, after a game exits;
    - `ApiSystem.cpp:496`;
    - `HttpServerThread.cpp:662`;
    - the cache switch `GuiMenu.cpp:1455`.
  - `FileSystemCache::reset(file)` (`:348-351`) has no caller in es-app or es-core at the pin (the grep over both, 6 lines all calling the whole reset).
- **T35's 3.11 and ruling (h) as (a)** (the coordinator's acceptance, comment 6546249036):
  - **At stage C:** T35's case is re-run unchanged from T35's ES and distribution tips of that minute. Both are named with the time of the read and T35's stage (before or after its S6). The record says what the case proves at that tip: the cache's side before S6, the caller's side after.
  - **At the hand-back:** it is re-run once more and named again.
  - **The cache's side, at stage B:** a contained fix for L-19 is certain and goes to the pause. For a write the cache cannot see, the contract stands. `exists(p, false)` at the reads whose writer is outside ES is the guard (`es-code-traps.md:127`, `es-native-ui.md:107`). A stored miss that expires is priced at stage C from 3.13's case, not proposed here.
- **L-15, `preloadFileSystemCache`** (`:1758-1797`):
  - The `[&]` lambda (`:1773`) reads the parameter `trySaveStates` from a detached thread (`:1797`) after the function may have returned (3.6, ASan at stage C).
  - `preloaded` is a function-static `std::set` (`:1766`) read and written with no lock.
  - Its callers are counted at stage C with the case.
- **The five earlier line sets** are the last generated table above: each cited line, the pin's function at it, and whether the image builds that line. T34's brief's `:144` is the WIN32 branch of `fromStat64`, not a line the image runs.

## The texture and font caches

- **#1263's three reads** (`TextureData.cpp:331`, `:339`, `:410`; #1263 read at 20:47 UTC, no comments; `proved: tree`; the cases are 3.13 and 3.26's shapes at stage C, G-03 the frame):
  - **The flow:** `loadFromVideo` (`:322-417`) asks `exists(localFile)` at `:331` with the session cache. When the thumbnail is older than two months it calls `removeFile` (`:336`) and asks again at `:339`.
  - **After the expiry:** with L-19 the second answer is `true`, so the thumbnail is not re-extracted. `:410` answers `true` and `getFileData` reads a file that no longer exists. The texture loads nothing.
  - **On a first extraction:** `:331`'s miss is stored. `createDirectory` at `:341` erases only the parent's entry. libvlc writes the snapshot at `:402` outside `FileSystemUtil`, so `:410` reads the stored miss and returns `false` (`:417`). The thumbnail just made is not used until a reset.
  - **Disposition:** the read is recorded here. The fix is rule 6 at the pause, with an uncached read at `:339` and `:410`, or L-19's order fix, which serves `:339`. #1263 keeps its picture checkbox open for this record (ruling (i)).
- **The texture key's contract** (`TextureResource.cpp:84-165`, T34's inherit item 9):
  - **The key** is `(canonicalPath, tile, linear, shareId)` (`:100`) in a static map of `weak_ptr` with no lock (`:12`, `:146`).
  - **When a key is dropped:** only when its texture has expired and the caller does not ask for a reloadable (`:133-134`), or by the map's own sweep at `:76-81`.
  - **A rewrite on disk** under a living key is never seen. The key carries no file time, and the only reload is `OptimizeVRAM`'s re-size, which reloads the same path synchronously on the caller's thread (`:110-127`, #1221 and T32 PL-07).
  - The caller's half is T34's `02`; #1221's fix is the caller's (`exists(qrPath, false)` and a session-named path).
- **The rest, with their cases (all `pending stage C`):**
  - **L-07:** the font's scale through `getFromTheme`, 3.16.
  - **L-09:** the glyph width, 3.17.
  - **L-10:** `TextureData`'s size fields without `mMutex`, 3.11's TSan line.
  - **L-11:** the loader's `notify_all` and `paused`, 3.12's teardown line.
  - **L-17:** the static caches with no lock. These are the texture map (`TextureResource.cpp:12`), `preloaded` (`FileSystemUtil.cpp:1766`), the battery paths (`Platform.cpp:445-449`) and the font map. 3.25 names the threads that reach each.
- **L-08, a rule erratum against `es-code-traps.md:118`.** The research read `Font::getHeight` as fixed after the constructor (`Font.cpp:107`, `:115-117`, `:420-421`, `:754-757`). The rule says it grows as glyphs rasterise. 3.8 is the positive that decides it at stage C. **T34 PL-17** (*"the moving font height"*, an open item to test) is named beside it for the coordinator's sweep.

## The paths

<!-- gen:paths -->
| Transform | At the pin | Input class | Output | Case |
| --- | --- | --- | --- | --- |
| `getCWDPath` | `:618` | none | the generic cwd, `""` when `getcwd` fails past 2,048 bytes | -- |
| `getPreferredPath` | `:625` | any path | unchanged off WIN32 | -- |
| `getGenericPath` | `:642` | any path | `\` to `/`, `//` folded, trailing `/` dropped | 3.21's inputs |
| `getEscapedPath` | `:670` | a ROM path (the launch's `%ROM%`) | a backslash before each character of the list at `:679` | 3.19 (held at stage B) |
| `getCanonicalPath` | `:707` | any path | the `.`/`..` fold | 3.20 (held at stage B) |
| `getAbsolutePath` | `:787` | a relative path and a base | `getCanonicalPath(base + "/" + path)` unless absolute | -- |
| `getParent` | `:795` | any path | the text before the last `/` | -- |
| `getFileName` | `:804` | any path | the text after the last `/` | -- |
| `getStem` | `:813` | any path | the file name less its last extension | -- |
| `getExtension` | `:842` | any path | from the last `.` of the file name | -- |
| `changeExtension` | `:859` | a path and an extension | the extension replaced | -- |
| `resolveRelativePath` | `:890` | a path and a root | `./` and `~/` resolved against the root | -- |
| `createRelativePath` | `:917` | a path and a root | `./`-relative by string prefix | 3.21 (`.//a.png`) |
| `removeCommonPath` | `:980` | a path and a prefix | the rest by string prefix, not by component | 3.21 |
| `resolveSymlink` | `:999` | a path | `readlink`'s target, made absolute | -- |
| `combine` | `:1261` | a base and a name | joined; a leading `/..` climbs the base | -- |
| `megaBytesToString` | `:1533` | a size | a display string | -- |
| `kiloBytesToString` | `:1554` | a size | a display string | -- |
| `getTempPath` | `:1575` | none | the temp folder, created | -- |
| `getPdfTempPath` | `:1599` | none | the PDF temp folder, emptied | -- |
| `getFileCrc32` | `:1623` | a file | hex CRC32 | -- |
| `getFileMd5` | `:1664` | a file | hex MD5 | -- |

generated, asserted: 22 rows (`tools/t36-tables.py --print paths`)
<!-- /gen:paths -->

- **`getEscapedPath`'s list** (`:679`, 19 characters, the launch's `%ROM%`): read whole. What it leaves, and what that reaches, is held under D-WORKFLOW-215 (§ The leads). 3.19 runs at stage C into the held directory.
- **`getCanonicalPath`:** the brief's 3.20 (R4 item 16, T2's lead). Its callers were read whole at stage B under ruling (k), and the result is held.
- **`createRelativePath` and `removeCommonPath`** (`:917-997`) compare by string prefix: `/storage/roms/snes2/a.png` against `/storage/roms/snes` gives `.//a.png` (R4 item 17, 3.21, `pending stage C`).
- **`isAbsolute`** is `path[0] == '/'` off WIN32 (`:1149-1162`, T2 FD-14, cited).
- **`CommandLineUtil.h`'s `wordEnd`:** T1's F-07 (#730), cited.

## The processes

<!-- gen:processes -->
| Line | Function | Match | Image | Shell | Waits | Returns | Callers' thread |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Platform.cpp:167` | `run` | spawn | built | `system()` (`/bin/sh -c`) when waiting; `execl("/bin/sh")` in a grandchild when not | when `waitForExit` (the launch, `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`); not at `Scripting.cpp:45` | `WEXITSTATUS` of the wrap's `exit $xs` (L-05); `0` when not waiting, or when the first `fork` fails | the launch on the interface thread (`FileData.cpp:1100-1103`) |
| `Platform.cpp:172` | `run` | spawn | built | `system()` (`/bin/sh -c`) when waiting; `execl("/bin/sh")` in a grandchild when not | when `waitForExit` (the launch, `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`); not at `Scripting.cpp:45` | `WEXITSTATUS` of the wrap's `exit $xs` (L-05); `0` when not waiting, or when the first `fork` fails | the launch on the interface thread (`FileData.cpp:1100-1103`) |
| `Platform.cpp:175` | `run` | spawn | built | `system()` (`/bin/sh -c`) when waiting; `execl("/bin/sh")` in a grandchild when not | when `waitForExit` (the launch, `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`); not at `Scripting.cpp:45` | `WEXITSTATUS` of the wrap's `exit $xs` (L-05); `0` when not waiting, or when the first `fork` fails | the launch on the interface thread (`FileData.cpp:1100-1103`) |
| `Platform.cpp:178` | `run` | spawn | built | `system()` (`/bin/sh -c`) when waiting; `execl("/bin/sh")` in a grandchild when not | when `waitForExit` (the launch, `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`); not at `Scripting.cpp:45` | `WEXITSTATUS` of the wrap's `exit $xs` (L-05); `0` when not waiting, or when the first `fork` fails | the launch on the interface thread (`FileData.cpp:1100-1103`) |
| `Platform.cpp:179` | `run` | comment | built | -- | -- | -- | -- |
| `Platform.cpp:199` | `runShutdownCommand` | spawn | WIN32 only | `system()` | yes | `system()`'s raw status, not `WEXITSTATUS` | the quit path |
| `Platform.cpp:201` | `runShutdownCommand` | spawn | built | `system()` | yes | `system()`'s raw status, not `WEXITSTATUS` | the quit path |
| `Platform.cpp:208` | `runRestartCommand` | spawn | WIN32 only | `system()` | yes | `system()`'s raw status, not `WEXITSTATUS` | the quit path |
| `Platform.cpp:210` | `runRestartCommand` | spawn | built | `system()` | yes | `system()`'s raw status, not `WEXITSTATUS` | the quit path |
| `Platform.cpp:248` | `touch` | comment | built | -- | -- | -- | -- |
| `Platform.cpp:858` | `runSystemCommand` | spawn | built | `execl("/usr/bin/sh")` in a grandchild | **yes**: the child waits for the grandchild and the caller waits for the child (L-13) | `0` always (`:879`) | the interface thread for most of its 80 call lines (#1220) |
| `Platform.cpp:861` | `runSystemCommand` | spawn | built | `execl("/usr/bin/sh")` in a grandchild | **yes**: the child waits for the grandchild and the caller waits for the child (L-13) | `0` always (`:879`) | the interface thread for most of its 80 call lines (#1220) |
| `Platform.cpp:864` | `runSystemCommand` | spawn | built | `execl("/usr/bin/sh")` in a grandchild | **yes**: the child waits for the grandchild and the caller waits for the child (L-13) | `0` always (`:879`) | the interface thread for most of its 80 call lines (#1220) |
| `Platform.cpp:865` | `runSystemCommand` | comment | built | -- | -- | -- | -- |
| `Platform.cpp:894` | `GetShOutput` | spawn | built | `popen()` (`/bin/sh -c`) | yes (to EOF, `pclose`) | each `fgets` chunk loses its last byte: the newline of a short line, a real character past 255 bytes or at an unterminated end (L-06); `popen` failure unchecked | its 27 call lines' (T26's collision) |
| `Platform.cpp:911` | `GetShOutputLines` | spawn | built | `popen()` | yes | the lines; `popen` failure returns none | its 9 call lines' |

generated, asserted: 16 rows (`tools/t36-tables.py --print processes`)
<!-- /gen:processes -->

The 16 lines are 13 spawns and 3 comment matches (`:179` and `:865` are `// execl failed`; `:248` is the commented `system("touch ...")` in `touch`, built). 11 of the 13 are built into the image; `:199` and `:208` are WIN32 only.

- **L-05, `run()`'s wrap** (`Platform.cpp:162-168`):
  - **The host's rcs:** the literal printed `seq 400 rc=0` and `seq 200000 rc=141` under the host's `/usr/bin/dash` at stage A (`stage-a/runs.out`, `proved: tool-run`).
  - **The launch's disposition (the errata's):** the launch does not run with SIGPIPE's default. `httplib::Server` ignores it and every child inherits that, so past the pipe's buffer the launch gets EPIPE and lost output, not a signal.
  - **G-07 at the window:** it first reads `SigIgn` (bit `0x1000`) of the running EmulationStation, then the image's shell rcs and the image's `runemu.sh`.
  - **The wrapper's redirects** from the distribution at `a5fbd75d61` (`runemu.sh` last changed `6f2eb9c212`, 2026-10-14):
    - `:40` `LOG_FILE="exec.log"`;
    - `:46` `OUTPUT_LOG="${LOG_DIRECTORY}/${LOG_FILE}"`;
    - `:84` `... 2>&1 | tee -a ${LOG_DIRECTORY}/${LOG_FILE}`;
    - `:491` `"${ROMNAME}" &>>${OUTPUT_LOG}`;
    - `:500` `eval ${RUNTHIS} &>>${OUTPUT_LOG}`.
  - **What reaches the pipe:** the emulator's output is appended to the log and does not reach `run()`'s pipe; the wrapper's `tee`'d lines do. That ES's launch command is this script stays `[unverified]` until the guest.
- **L-13, a rule erratum against `es-native-ui.md:103`.** The rule calls `runSystemCommand` the way to run an OS command without blocking.
  - At the pin it returns `0` at `:879`, reads neither `name` nor `window`, and blocks: the child waits for the grandchild (`:867-868`) and the caller waits for the child (`:876`). It is a double fork that does not detach.
  - 3.7's text case records it (`pending stage C`). #1220 (process starts on the interface thread) is its callers'.
- **L-06, `GetShOutput`** (`:891-905`): T26's collision (#1225, `a5d2d3756` on `757f5370ea`). 3.9 is the FAIL-at-pin control at stage C, never re-fixed here.
- **`shellQuote`** (`StringUtil.cpp:426-444`) is the contract four lanes' fixes rest on: single quotes, `'` as `'\''`, the empty string as `''`. 3.18's positive is at stage C.
- **L-14, `maskSecrets`' reach** (`StringUtil.cpp:446-804`). 18 call lines over es-app and es-core (`grep -c 'maskSecrets('`), in 10 files, the definition among them. `runSystemCommand` logs every command through it (`Platform.cpp:855`), and the launch logs its command through it (`FileData.cpp:1090`). 3.10's JSON, `name: value` and `Authorization: Bearer` shapes, each built at run time, run at stage C.

## The writes and reads

<!-- gen:writes -->
| Site | Function | Image | Mechanism | Atomic | What an interrupted write leaves | What its return claims |
| --- | --- | --- | --- | --- | --- | --- |
| `FileSystemUtil.cpp:1053` | `removeDirectory` | WIN32 only | `rmdir` | atomic | nothing (the directory stays) | true when `rmdir` returned 0; true when absent |
| `FileSystemUtil.cpp:1055` | `removeDirectory` | built | `rmdir` | atomic | nothing (the directory stays) | true when `rmdir` returned 0; true when absent |
| `FileSystemUtil.cpp:1070` | `removeFile` | WIN32 only | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1072` | `removeFile` | WIN32 only | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1075` | `removeFile` | WIN32 only | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1081` | `removeFile` | built | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1084` | `removeFile` | built | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1100` | `createDirectory` | WIN32 only | `mkdir 0755`, parents by recursion | per directory | the parents made so far | false on a race with another creator (L-16) |
| `FileSystemUtil.cpp:1105` | `createDirectory` | built | `mkdir 0755`, parents by recursion | per directory | the parents made so far | false on a race with another creator (L-16) |
| `FileSystemUtil.cpp:1116` | `createDirectory` | built | `mkdir 0755`, parents by recursion | per directory | the parents made so far | false on a race with another creator (L-16) |
| `FileSystemUtil.cpp:1432` | `writeAllText` | WIN32 only | `fopen "wb"` in place, `fwrite`, `fclose` | **no**: truncate then write | a truncated or short file | nothing: `void` (L-04, #1186) |
| `FileSystemUtil.cpp:1434` | `writeAllText` | built | `fopen "wb"` in place, `fwrite`, `fclose` | **no**: truncate then write | a truncated or short file | nothing: `void` (L-04, #1186) |
| `FileSystemUtil.cpp:1461` | `renameFile` | WIN32 only | `std::rename` | atomic on one filesystem | src or dst | true over an absent source (L-03; T21's fix) |
| `FileSystemUtil.cpp:1463` | `renameFile` | built | `std::rename` | atomic on one filesystem | src or dst | true over an absent source (L-03; T21's fix) |
| `FileSystemUtil.cpp:1490` | `copyFile` | WIN32 only | `fopen "wb"` in place, 512-byte `fread`/`fwrite` | **no** | a short destination | true over an absent source and over a short write (L-03) |
| `FileSystemUtil.cpp:1492` | `copyFile` | built | `fopen "wb"` in place, 512-byte `fread`/`fwrite` | **no** | a short destination | true over an absent source and over a short write (L-03) |
| `Platform.cpp:244` | `touch` | built | `open` with `O_CREAT` and `O_WRONLY`, mode `0644`, no truncation | yes (creates or leaves) | an empty file or the old one | nothing: `void` |
| `ZipFile.cpp:259` | `ZipFile::extract` | built | miniz `MZ_FOPEN(..., "wb")` (`zip_file.hpp:6634`) | **no** | a partial member | miniz's status |

generated, asserted: 18 rows (`tools/t36-tables.py --print writes`)
<!-- /gen:writes -->

- **L-04 and #1186:** `writeAllText` (`:1429-1446`) truncates in place, ignores `fwrite` and `fclose`, and returns `void`. #1186's last comment as read is 6440869119 (2026-10-27 11:33 UTC). Whether the function returns its result or is marked as superseded by `AtomicFile::writeText` is put to the pause; the call sites stay their owners' under #1186.
- **L-03** (`proved: tree`, case 3.2 at stage C):
  - `renameFile` returns `true` over an absent source (`:1451-1452`), and with `overWrite` removes the destination before renaming (`:1454-1455`). Both are T21's fix (#1191, `f7c16144d`), a collision.
  - `copyFile` returns `true` over an absent source (`:1472-1474`) and over a short write: `fwrite`'s count is unread (`:1500-1501`) and so is `fclose`'s (`:1503`). That half is this slice's (rule 6).
- **L-02:** `skipUtf8Bom` (`:1369-1379`) leaves the stream failed for a file under three bytes, so `readAllText` (`:1418-1427`) and `readAllLines` (`:1400-1416`) read nothing. T20's collision (#1177, `d9afa5c7c`); 3.4 is the control.
- **L-16:** `createDirectory` (`:1089-1120`) returns `false` when another creator made the directory between its `exists` and its `mkdir` (3.15).
- **`readAllBytes`** (`:1381-1398`) returns empty on a short read and for a file whose size `tellg` cannot give; no lead.

## The device reads, the renderers and the words

- **The case helpers:** `toUpper` and `toLower` (`StringUtil.cpp:357-362`, `:398-403`), L-01, 3.1.
- **The battery read, for #840** (`Platform.cpp:440-560`, `proved: tree`):
  - The paths are found once, by a listing of `/sys/class/power_supply` through the cached `getDirContent` (`:458`), and kept in five function-static strings with no lock (`:445-449`).
  - The capacity is read uncached each call: a fresh `std::ifstream` (`:546-557`), the status through `readAllText` (`:524`).
  - The fuel-gauge branch's `std::stof` (`:539-540`) throws on an empty read.
  - So #840's question has no cache in the read itself. A supply added after the first call is never found.
- **`TimeText`:** the fork's file, read whole (`TimeText.cpp`, 83 lines); its cases are T18's in `es-unit-tests`.
- **The 11 `_("` lines** (stage A's count: 11 lines, 12 occurrences), with the French from the pin's catalog (`locale/lang/fr/LC_MESSAGES/emulationstation2.po`, parsed at stage B):

  | Line | msgid | French |
  | --- | --- | --- |
  | `MathExpr.cpp:95` | `Unknown`, `None` | `Inconnu`, `Aucun` |
  | `TimeUtil.cpp:517`, `:588` | `never` | `jamais` |
  | `TimeUtil.cpp:544` | `%d d` | `%d j` |
  | `TimeUtil.cpp:548`, `:569` | `%d h` | `%d h` |
  | `TimeUtil.cpp:552`, `:560`, `:573`, `:578` | `%d mn` | `%d mn` |
  | `TimeUtil.cpp:580` | `%d sec` | `%d sec` |

  `es-untranslated` printed 706 of 706 fork strings with French (stage A). G-04 draws the durations at 640x480 in both languages (`pending window`).
- **The renderers:**
  - The image builds `Renderer_GLES30.cpp` (`-DGLES3=1` on every device, R3 § 2.2). The guest runs it through Mesa virgl; H700 runs panfrost and SM8550 Adreno, which the guest cannot show (G-09 `CANNOT`).
  - The GL thread question is 3.25's and G-05's.

## The structure

- **Three renderers no image compiles:** `Renderer_GL21`, `Renderer_GLES10` and `Renderer_GLES20` (G-08 `CANNOT`, a structure fact).
- **Includes:** the angle includes outside the lane's standard list are 33 of 241 (`stage-a/angle-includes.out`); R3's 41 was against an unstated list. The branches the host did not parse, and the stand-in's renderer positives, are stage C's (`stage-a/syntax-check.out` owed).
- **`ROCKNIX` gates in the 58: 0.** The one mention is a comment (`CommandLineUtil.h:51`).
- **`han.h` (20,923 lines) and `zip_file.hpp` (10,011 lines):** read only where a lead reaches them. `zip_file.hpp`'s provenance and licence notice belong to #256's vendored-header PR bucket.
- **T21's `utils/DownloadFile.{h,cpp}`** fall under the glob and are not at the pin (ruling (b)).
- **The fakes' double:** stage C's.
- **The two rule errata, for the coordinator's sweep:**
  - **L-08** against `es-code-traps.md:118`, with 3.8's PASS line;
  - **L-13** against `es-native-ui.md:103`, with 3.7's text case.
- **The menu map's checker:** `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (stage A).

## The merge debt

- **The bases:** `cada856d86` is the base against ROCKNIX's master `f6c542872e`, and `bccd715707` is its parent.
- **Upstream:** upstream commits on the 58: 0 (14 on any path). 43 of 58 blobs are identical pin to master. Batocera has 13 commits since `1750dded8c` on nine files, four of them fork-modified; that is the reconciliation list only.
- **The pending collisions:**
  - T20's `d9afa5c7c` (`FileSystemUtil.cpp`, `readAllText`, #1177) on `5c0ddaaeef`;
  - T21's `f7c16144d` (`FileSystemUtil.cpp`, `renameFile`, #1191) on `3ae9610b0f`;
  - T26's `a5d2d3756` (`Platform.cpp`, `GetShOutput`, #1225) on `757f5370ea`;
  - T21's two new files, `utils/DownloadFile.{cpp,h}`, under the glob.
  - Each is read and recorded in `stage-a/collisions.out`, and never re-made here.

## The runs

- **Stage A:** 23 runs, each as the brief expected (`stage-a/runs.out`, `00`).
- **Stage C (host):**
  - **`utils-resources-tests`** (`stage-c/build-tests.out`): 15 cases, 11 passed, 4 failed; the 4 FAILs are the FAIL-at-pin candidates, each proving its defect at the pin (`proved: fix-unit-test`): **3.1 (L-01)**, **3.2 (L-03)**, **3.4 (L-02)** and **3.26 (L-19)** -- 3.26 FAILs `CHECK(exists(p)==false)` with `true == false`, confirming the stale cache. The 11 that pass are the controls, the positives and the text-read seams.
  - **T35's 3.11 re-run** (ruling (h) as (a), `stage-c/t35-311-rerun.out`): `window-input-tests` at distribution `4f7d98b2ed` / ES `b7fdb3a24` (T35 stage H, read 23:44:37Z) -- rc 0, 31/31 passed. 3.11 PASSES at the amended tip (T35's caller fix landed), where it FAILs at the pin; T36 owns the cache's half.
  - **the stand-in** (`stage-c/syntax-check-probe.out`): T35's fakes over the 25 `.cpp`, 20 rc 0; the 5 that need the T36 fakes (Font/FreeType, TextureData/vlc, the 3 renderers/GL) and the renderers positive under `-DUSE_OPENGLES_30` are the remaining stage-C compile item.
  - **`es-unit-tests` (the slice's StringUtil/TimeText/OfflineProxyUrl):** retried at stage E (S0, ruling 13) with rapidjson 1.1.0 from the sources cache (`/workspace/tmp/m6-t36/rj`). `-Wno-error` does not build it (the `-Wtemplate-body` on `rapidjson/document.h:319` is a g++ 15 default-error, not `-Werror`-promoted); **`-Wno-template-body` builds it: `RUN es-unit-tests: rc 0; [doctest] test cases: 185 | 185 passed | 0 failed`.** So the slice's three linked files pass, and `es-unit-tests` joins the `TOTAL:` line (the build script carries `-Wno-template-body`).
  - **the packet and the seat's probe** (`second-opinions/`): packet 352,038 bytes / 36 sources / sha256 `c3b14889`, scan clean (138 words classed, 0 a value); probe PASS (served `openai/gpt-6-astra`, OpenAI, max); refutation in `04`.

## The guest cycle

Slot 3, START 23:09:19 to RETURN 23:22:05 UTC, inside the bound; the detached timer (pid 2238851) stopped unfired; disk retired (sha256 `65d4dc4e...`), census `qemu 0, compilers 0`. Full record in `00` and `guest-cycle/`.
- **G-01:** `BUILD_ID=069fc27044...`, 640x480, art-book-next; **`libfribidi` not linked** (freetype and vlc are) -- Q7's `HAVE_FRIBIDI` answered: the image did not take it.
- **G-02/G-06:** carousel + menu at 640x480 and 1280x800; cap heights 13 px and 17 px (`guest-cycle/g02-g06-measure.txt`); at 1280 the menu floats, at 640 it is full-screen (#540's threshold).
- **G-03:** the guest ships no game with a manual; the frame was not stageable, the proof is unit cases 3.13/3.26 (`es-native-ui.md`).
- **G-04:** `secondsToString` panel needs scraped media the guest lacks; the thresholds are host-read and the French catalog renders cleanly on the chrome (accents, the typographic apostrophe). An open item for a media-scraped guest.
- **G-05:** driver `virtio-pci` (virgl, not softpipe); art clean, RSS stable; VRAM counters `CANNOT`.
- **G-07:** `SigIgn=0x1000` (SIGPIPE ignored) -- the launch gets EPIPE past the pipe buffer, not a signal; `sh`->bash; `seq 400`->0, `seq 200000`->255; the image's `runemu.sh` keeps the emulator's output out of `run()`'s pipe.
- **G-08, G-09:** `CANNOT` as planned.

## The streams

One row per stream: the positive before, the ES commit, the positive after, `Already written:`, `proved:`, the guest half, and the patches/collisions/#585.

| Stream | Before (pin) | ES commit | After | Already written | proved | Guest | #585 / notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 (PL-06 #1359, G-1) | `S1 pin: rc 1; ERROR: AddressSanitizer: attempting double-free` (`stage-e/s1-before.txt`; `getTextureForNewGlyph` pushed then deleted the atlas) | `4fc77caaa` | `S1 tip: rc 0; no sanitizer report` (`stage-e/s1-after.txt`; push only after `findEmpty` succeeds) | nothing on disk; a live-session memory error in the font cache (#1359) | fix-unit-test (ASan, the method lifted at pin vs tip) | none (#1359 VM line: a host ASan case) | #585 owed: `mTextures.push_back(tex)` is in ROCKNIX `f6c542872e` and batocera `b2ceb55a7e` |

## Positives

- **The cache's lock discipline:** `queryCacheEntry` stats outside the lock and `insertEntry` re-checks under the unique lock, so two threads that miss together store one answer (`:200-216`, `:313-324`; `proved: tree`, 3.25's TSan program at stage C).
- **`GetShOutputLines`** (`Platform.cpp:907-935`) accumulates a line longer than its buffer and checks `popen`, which `GetShOutput` does not.
- **`writeAllText` erases after it writes; `renameFile` and `copyFile` erase *before* the rename/copy, not after** (`:1457-1463`, `:1506-1507`; the "erase after they write" claim is withdrawn, 04 correction 1, the seat). What is unique to `removeFile` is that it **re-reads the cache between its erase and its unlink** (`isDirectory` at `:1080`), which is L-19; the other writers do not re-read in between.
- **The battery's capacity read** is uncached.

## The #585 lines owed

- **The three never posted (D-WORKFLOW-165), for the coordinator:**
  - T20 `02:337`, `skipUtf8Bom` (batocera);
  - #1191 `:21`, `renameFile`;
  - T26 `02:819`, `GetShOutput` (ROCKNIX's alone).
- **This slice's, so far:**
  - L-19, `removeFile`'s order (ROCKNIX and batocera both). It is written in the shape the lane writes at stage D and never sent.
  - The three holds' lines are held with their records.

## What T37 inherits

Written at the hand-back. Its tables are the five above, the provenance table and the lines-set reconciliation. The `utils-resources-tests` recipe, the stand-in's rc per file, the rule errata as dispositioned and the collision list follow at stages C to E.
