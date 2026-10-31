# Research notes: M6.P2 T36, EmulationStation's utilities, resources and renderers (#683)

## Scope

The membership is the brief's § 2 block (`stage-a/membership-block.sh`, the brief's lines 406-495 extracted: 90 lines, sha256 prefix `ebe18e98a244a77d`, R1's `block.sh`), run from this worktree at `3740ce4a0d` against `docs/reviews/{inventory.json,slices.json}` of the P1 branch at `2174265e9c`, with the ES worktree at the pin `16dbac5211`. Its output, as it printed (rc 0, 2 s; `stage-a/membership-block.out`):

```
58 .qa-scratch/t36/paths.txt
mine: 58 paths.txt: 58 equal: True
only-mine: []
only-paths.txt: []
lines: 50840 reach: {'shipped': 58} tier: {'upstream-carried': 43, 'fork-own': 15} lang: {'c++': 25, 'c-header': 32, 'c++-header': 1}
fork-own lines: 6212
read lines: 50840
ls-tree at the pin = paths.txt
wc -l 50827
grep -c 50840
52
52
 15 files changed, 1032 insertions(+), 60 deletions(-)
 15 files changed, 1032 insertions(+), 60 deletions(-)
```

Under `CLAIMS` (`stage-a/membership-claims.out`): the twelve named paths of this slice `in-T36 non-rest [('es-core-utils-resources', 36)]`; `utils/AtomicFileUtil.cpp` (829) and `.h` (215), `Settings.cpp`, `SystemConf.cpp`, `HttpReq.cpp` and `es-app/src/ApiSystem.cpp` `not-in-T36 non-rest [('es-state-and-bridge', 21)]`; `utils/DownloadFile.cpp` `NOT IN INVENTORY`; `components/TextComponent.cpp` and `MenuComponent.cpp` `[('es-core-components', 34)]`; `ImageIO.cpp`, `Log.cpp`, `Window.cpp` and `es-core/CMakeLists.txt` `not-in-T36 rest [('es-core-window-input', 35)]`; `CloudText.cpp` and `es-app/tests/unit/CMakeLists.txt` `[('es-cloud-pages', 18)]`; `GuiMenu.cpp` `[('es-guimenu', 26)]`. ES-CORE BY SLICE:

```
96 paths 22575 lines (('es-core-window-input',), 'rest')
80 paths 21984 lines (('es-core-components',), 'non-rest')
58 paths 50840 lines (('es-core-utils-resources',), 'non-rest')
8 paths 3344 lines (('es-state-and-bridge',), 'non-rest')
```

**The 58** (`stage-a/paths.txt`): 25 `.cpp`, 32 `.h`, one `.hpp`; 14 under `renderers/`, 11 under `resources/`, 33 under `utils/` (r01). Tiers by the read: fork-added 6, fork-modified 9 (`6 A`, `9 M` against the merge base `cada856d86`, r04), upstream-carried 43, all 43 blob-identical to `rocknix/master` (r05).

## The § 5 runs at stage A

`stage-a/runs.sh` is the brief's run block (lines 1574-1624) verbatim, each command in its own subshell with an `rc=` line and a `date +%s` pair; `stage-a/runs.out` holds every line (run at 16:40:14Z, 2 s, 23 runs, every rc 0 as the subshell returns). Each figure below is the run's own line; every one equals the brief's expectation unless the last column says otherwise.

| Run | What | The run's line(s) | Against the brief |
| --- | --- | --- | --- |
| r01 | the scope | `58`; `25`; `32`; `1`; `14 renderers`, `11 resources`, `33 utils` | as expected |
| r02 | the worktree and the bases | `16dbac5211`; `0`; `cada856d86`; `f6c542872e`; `b2ceb55a7e`; `1750dded8c`; `bccd715707`; `14`; `0` | as expected |
| r03 | the lines two ways | `wc -l 50827`; `grep -c 50840`; `no trailing newline: 13` (the thirteen named in `runs.out`); `han.h + zip_file.hpp grep -c 30934` | as expected |
| r04 | the fork's delta | `15 files changed, 1032 insertions(+), 60 deletions(-)` twice; `15 files changed, 60 insertions(+), 1032 deletions(-)`; `6 A`, `9 M`; the 15 numstat rows; `19`; `2`; `19` | as expected |
| r05 | upstream's delta | `0`, `upstream commits rc=1`; `identical to rocknix/master: 43`; batocera `13`, `9 files changed, 668 insertions(+), 386 deletions(-)`; both: `Font.cpp`, `Font.h`, `TextureData.cpp`, `Platform.cpp` | as expected |
| r06 | the other lanes' deltas in the 58 | T20 `1 file changed, 4 insertions(+)`; T21 `FileSystemUtil.cpp \| 17`, `1 file changed, 11 insertions(+), 6 deletions(-)`; T26 `1 file changed, 15 insertions(+), 5 deletions(-)`; every other tip empty, T35's `453dffd0a2` included; T21 with `DownloadFile.*` `3 files changed, 101 insertions(+), 6 deletions(-)` | as expected; T35's ref resolved (the research had none) |
| r07 | the collisions' commits | `d9afa5c7c` `FileSystemUtil.cpp \| 4`; `f7c16144d` `FileSystemUtil.cpp \| 17`; T26's S8 is `a5d2d3756` | as expected; S8's hash read here |
| r08 | the strings | `_(" lines TOTAL 11 in 2 files`; `12` | as expected |
| r09 | the French; `es-untranslated` | the seven msgids at `:143 :1673 :3554 :4007 :4011 :4015 :4019`, each with its msgstr; `es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without`, rc 0 | as expected; the tree-wide line is the lane's |
| r10 | the log lines | `LOG(Log lines TOTAL 99 in 16 files` | as expected |
| r11 | threads and lifetimes | the ten thread lines; `10`; `1` (`.detach(`); the weak_ptr lines; `0`, `delete this rc=1` | as expected |
| r12 | the locks | the ten per-file counts; `63` | as expected |
| r13 | the process spawns | the sixteen `Platform.cpp` lines; `16` | as expected |
| r14 | the writes | `FileSystemUtil.cpp:1432 :1434 :1490 :1492`; `6` (`zip_file.hpp`) | as expected |
| r15 | the helpers' reach | `runSystemCommand\( 80`, `ProcessStartInfo 13`, `GetShOutput\( 27`, `GetShOutputLines\( 9`, `writeAllText\( 27`, `renameFile\( 17`, `copyFile\( 12`, `readAllText\( 38`, `readAllLines\( 5`, `AtomicFile:: 41` | as expected |
| r16 | includes and gates | `241`; `Font.h:11:#include FT_FREETYPE_H`; `0`, `ROCKNIX gates rc=1`; the `USE_OPENGLES_30` positions from `GlExtensions.h:5`; `3`, `GLES3 macro rc=0` | as expected; under the lane's own standard list `NON-STD ANGLE INCLUDES (lane's list): 33` (`stage-a/angle-includes.sh`, `.out`) |
| r17 | non-ASCII bytes | `FileSystemUtil.cpp:3`, `StringUtil.cpp:2`, `StringUtil.h:7`; `files with a non-ascii byte: 3`; the lines `225 287 718`, `1406 1407`, `62-68` | as expected |
| r18 | the candidate lines | `359 400`; `162`, `164`; `115`; `1773`; `331 339 410`; `runSystemCommand` at the read's `1:` and its `return 0;` at the read's `27:` (`:879`) | as expected |
| r19 | the pipe, 3.5's two forms | `seq 400 rc=0`; `seq 200000 rc=141`; `1492`; `/usr/bin/dash` | as expected (the shell's default; the errata: the launch ignores SIGPIPE) |
| r20 | the menu map | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing`, rc 0; `SOURCE_DIRS = ["es-app/src/guis", "es-core/src/guis"]` | the checker's line is the lane's |
| r21 | the compile | `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)`, rc 2 | as expected |
| r22 | STAGE C | not run: `stage-a/syntax-check.sh` and `tools/t36-build-tests.sh` are stage C's | stage C |
| r23 | the removal check | empty; empty | as expected |

## The collisions, read at stage A

`stage-a/collisions.sh` and `.out` (each fix by `git show` and the tip's whole diff to the file against the pin):

| Lane | Commit | Tip | File | What it changes | Issue |
| --- | --- | --- | --- | --- | --- |
| T20 | `d9afa5c7c` | `5c0ddaaeef` | `utils/FileSystemUtil.cpp` (+4) | `readAllText`: `file.clear()` after the failed three-byte BOM read, so a file under three bytes is read | #1177 |
| T21 | `f7c16144d` | `3ae9610b0f` | `utils/FileSystemUtil.cpp` (11+/6-) | `renameFile`: an absent source returns false; off WIN32 the destination is no longer removed before `rename(2)` | #1191 |
| T26 S8 | `a5d2d3756` | `757f5370ea` | `utils/Platform.cpp` (15+/5-) | `GetShOutput`: only a trailing newline dropped per chunk; a failed `popen` returns `""` | #1225 |

Each commit is an ancestor of its tip and the only one on it touching the file since the pin. This slice's own case over the same lines (3.4, 3.2's `renameFile` half, 3.9) is the FAIL-at-pin control each merged fix turns green; `copyFile`'s same shape is named by no lane and is this slice's.
