# Research notes — M6.P2 T18 (#665)

## Scope

**The membership block** (brief § 2, copied verbatim as `stage-a/scope.py`; run as r01 at 09:37 UTC on 2026-10-26; output `stage-a/out/r01_block.out`):

```
paths 30 lines 11193 {'shipped': 30} {'fork-own': 30}
{'c++': 23, 'c-header': 5, 'cmake': 1, 'markdown': 1}
read 29 11116 unread ['es-app/tests/unit/README.md']
sources 8 5429 tests 22 5764
```

**30 paths, 11,193 lines; read 29 / 11,116; tier fork-own 30; reach shipped 30.** The inventory holds 1,114 ES rows. The unread file is the tests' `README.md` (77 lines), read as context, not graded.

| Part | Paths | Lines | Files |
| --- | ---: | ---: | --- |
| The sources | 8 | 5,429 | `CloudText.{h,cpp}` 589 / 1,409, `ThreadedCloudSync.{h,cpp}` 201 / 949, `CloudTransferJob.{h,cpp}` 217 / 751, `guis/GuiCloudTransfer.{h,cpp}` 236 / 1,077 |
| The tests | 22 | 5,764 | 19 test sources (`CloudTextTests.cpp` 1,784, `AtomicFileTests.cpp` 1,090, `SystemConfTests.cpp` 506 the largest), `CMakeLists.txt` 159, `README.md` 77, `fakes/SDL_timer.h` 8 |

- **None of the 30 is in the merge base** `bccd715707` (r03): every line is the fork's.
- **The pin and its base** (r04): `16dbac5211eea7e70db7394372033be2be7df829`, the ES worktree's HEAD; merge base with `upstream/master` `bccd715707`, which is `upstream/master` itself; 725 ahead, 0 behind.
- **The tests:** 221 `TEST_CASE` in 19 files, 1,665 `CHECK*` lines; `CloudTextTests.cpp` holds 70 (r06).
- **`CloudText.h` declares 47 functions** (r07, by `grep -P`; GNU `grep -E` with the brief's regex gives 44, missing `:187`, `:529` and `:546`, whose return types hold a space; `00` § Stage A).

### The history

`git log --no-merges bccd715707..16dbac5211 -- <the 30>` (r16):

- **181 commits:** Max Engel 170, blitterbot 9, rasterabot 2;
- **from 2026-07-25 to 2026-10-11**: July 2, September 166, October 13;
- per file, the most changed: `ThreadedCloudSync.cpp` 56, `GuiCloudTransfer.cpp` 47, `CloudText.cpp` 39, `CloudTextTests.cpp` 37, `CloudText.h` 35, `GuiCloudTransfer.h` 24.

The newest ten:

```
c8dc72cf9 2026-10-11 emulationstation: manage cloud connections and network recovery
1d76b3da7 2026-10-08 cloud setup: explain refused folder paths (#524)
1d5397fda 2026-10-08 cloud: translate folder check failures and name scan contention
baeea2a8c 2026-10-08 cloud setup: preserve bounded JSON across pipe reads
1272b3405 2026-10-08 cloud setup: check selected folders without moving libraries
300f97d28 2026-10-07 cloud: replace migration with manual folder setup
8beab9090 2026-10-06 cloud: fit recovery reasons and French edit guidance
bab4df649 2026-10-06 cloud: handle root content and preserve migration failure reasons
39f888354 2026-10-03 settings: revalidate last-good records under the lock (#320)
e108699ea 2026-10-01 cloud: the cloud folder step at the end of cloud setup and at boot (fork #363)
```

The last commit to the 30 is 15 days before this review. October's thirteen are the retirement of the folder migration (D-CLOUD-175, #508) and the connections work that followed it. They are where a sentence describing the retired flow is likeliest to survive (§ The strings, at stage B).

### The callers outside the eight

The sources are entered from four files outside the slice (r17):

| Caller | Lines | Enters |
| --- | --- | --- |
| `main.cpp` | `:691`, `:1027` | the startup sync card; the restore page at boot |
| `FileData.cpp` | `:1010-1018`, `:1310` | the launch over a running transfer (`stopForLaunch`, `launchWhenGone`); the exit sync |
| `ProxyCards.cpp` | `:118` | the exit sync owed at the link's return |
| `guis/GuiMenu.cpp` | `:5082`, `:5157`, `:5229`, `:5260`, `:5383`, `:5487-5546`, `:6139-6152`, `:7041` | the transfer page (restore, back up, the two scans, the folder seeding), the reopen of a running job, the manual sync rows |

`GuiMenu.cpp` names `/usr/bin/cloud_` on 50 lines. Those callers are context: they are read where they decide what reaches the eight (a command string, a title, a lifetime), and graded only there.

### The context read

Named at stage A, read at stage B (brief § 2):

- **`es-app/tests/app-unit/`**, 19 files at the pin: `AppWindowTests.cpp`, `BookkeeperTests.cpp`, `CMakeLists.txt`, `FolderMergeTests.cpp`, `JobsTests.cpp`, `JourneyTiersTests.cpp`, `ProxyCardsTests.cpp`, `RunLockTests.cpp`, `TextFitTests.cpp`, `main.cpp`, and nine fakes (`ApiSystem.h`, `FileData.h`, `LocaleES.h`, `Log.h`, `SystemConf.h`, `ThreadedCloudSync.h`, `Window.h`, `components/AsyncNotificationComponent.h`, `utils/FileSystemUtil.h`). Not in the inventory's T18 rows; the fake `ThreadedCloudSync.h` is where a test of a caller stands in for the eight.
- **The eight Python harnesses** under `tests/`, 986 lines: `cloud-oauth-lifetime.py` 184, `cloud-sync-last-run.py` 82, `maintenance-why.py` 72, `cloud-set-systems-quoting.py` 99, `cloud-gated-row.py` 125, `cloud-folder-reopen.py` 51, `cloud-content-selection.py` 272, `cloud-oauth-await.py` 101.

### The unit tests' build

The host has no `cmake` or `ninja`, and no M6 build root holds an ES build or rapidjson (r18). `tools/t18-build-tests.sh` reads `es-app/tests/unit/CMakeLists.txt`'s own `add_executable` / `add_library` lists, expands `${CMAKE_CURRENT_SOURCE_DIR}` and `${ES_ROOT}`, and builds with the file's include roots and flags (r19 lists the lines it reads):

| Binary | Sources | Flags beyond `-std=c++17 -pthread` | Cases | Assertions |
| --- | ---: | --- | ---: | ---: |
| `es-unit-tests` | 28 | rapidjson on the include path | 185 | 4,795 |
| `es-file-tests` | 2 | `-DES_ROOT_DIR` | 24 | 3,389 |
| `es-conf-tests` | 3 | `fakes/` before `es-core/src` | 10 | 119 |
| `es-file-tests-win32` | 2 + 1 object | the object built with `-D_WIN32` | 2 | 14 |

**221 cases, 0 failed** (r20), the same 221 as r06's `TEST_CASE` count. rapidjson is the 35-header copy recorded in `00` § Stage A (35 of 35 sha256 matching M7's prep's `inputs.json`).
