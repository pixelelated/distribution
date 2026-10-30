# Mini Retro: T33, EmulationStation's system layer (#680)

**Completed:** 2026-10-30.

**Scope:** the 77 paths of `es-app/src`'s system layer that the slice brief `docs/reviews/briefs/es-app-system.md` (version 2) names: the game lists, metadata, collections and filters, the parsers and tables, the fork's helpers, the network thread, the screensaver, and upstream's workers. Read at the ES pin `16dbac5211`, at Independent depth (one seat, GPT-6 Astra at `max`). The artifacts are:
- the audit, `docs/audits/2026_10_27-epic-m6-es-app-system/`;
- the audit issue #1270: 26 items, 23 resolved and 3 deferred;
- the twenty-two bugs #1271 to #1292;
- the coordinator's stream brief `docs/reviews/briefs/t33-streams.md` at `31561429a2`, with its ten rulings.

**Branches:**
- **The ES branch** `feature/m6-es-app-system-680` (pixelelated/emulationstation): 8 commits, `d0d92dda6` to `f802c55c6`, one per stream from S1a to S6. S7 changes only the distribution's map.
- **The distribution branch** `feature/m6-es-app-system-680`: the records, one commit per stream, then stage F `e3cb92c7d6`.

**Delta** (each figure is a tool's own line):
- `git diff --shortstat 16dbac5211 f802c55c6`: `26 files changed, 890 insertions(+), 172 deletions(-)`. The sources are 22 files (+728/-172), the tests 3 files (+141), and the rest is the catalog.
- `tools/t33-build-tests.sh`: `TOTAL: 239 test cases in 5 binaries` at the pin, `TOTAL: 245 test cases in 5 binaries` at the tip, 0 failed in every binary.
- The generators (D-WORKFLOW-210): uncached reads 4 to 18; write lines 11 to 2; msgids 196 to 202; `es-untranslated` 706 of 706 to 709 of 709.
- `stage-e/handback-run.sh`: 30 harness runs at the tip, 0 unexpected.

## What worked well

- **Test first, by extraction.** Every positive compiled the pin's own function bodies (`stage-c/t33extract.py`) over doubles, under ASan, UBSan or TSan. Each was seen to FAIL at the pin before the fix and PASS after. No stream's proof rests on a hand-written model of the code.
- **The checkpoint per stream.** One line on #680 as each landed (eight, plus S7's) made two usage-limit pauses cheap to resume from. The pause posts at 05:41 and 09:56 UTC named the next step exactly.
- **Guarding each `--control` as `CANNOT`** once its targets were gone (D-WORKFLOW-211). A control that would have silently passed or crashed on fixed code now says what it is, and `handback-run.sh` expects its rc 2.
- **Scheduling a race on purpose.** The Bluetooth fixture's `T33Thread` sleeps 50 ms after starting its worker. That made the pin's publication race (the worker deletes the object before the constructor stores its handle) a heap-use-after-free every run, with no chance in it.

## What was harder than expected

- **Three places where the brief's fix was wrong or not enough**, each found by the fixture or by reading the shipped artifact:
  - **S4a:** a worker calling `ResetComponent` takes `mWatchersLock`, while `check()` joins that worker under the same lock: a deadlock. The worker now polls instead; posted at 05:41 before any code.
  - **S4b:** argv[0]'s basename never names `raofflineproxy-ctl`, a `#!/bin/bash` script whose first cmdline field is `/bin/bash`. The interpreter's script field is matched too, with a test of that shape.
  - **S5:** stage C's control (join plus atomic flag) still read destroyed params, because `ScraperSearch` declares `params` after `searchHandle`. The builder copies its params.
- **Later streams broke earlier harnesses' doubles.** New includes in S4b's `KeyboardMapping.cpp` and S1's `overlayXML` meant completing the l321 fakes and the l313 doubles (D-WORKFLOW-211). Each completion was a setup line; no assertion changed.
- **The session's environment changed under the stage.** After a usage-limit reset the ssh agent was gone: `git ls-remote` over the ES remote's host was refused, and the ES tip was read back through the API instead. A `gh issue comment` on #771 reported a GraphQL error although the comment had landed; it was read back by its text before any retry.
- **A record line that would have been wrong.** The first `handback-checks.txt` carried the refused `ls-remote`'s error in place of the tip. It was caught on reading the file back, not by a check.

## What did we discover

- **PL-25 is a reachable use-after-free, not only a lead.** The screensaver's slideshow list is cleared only when it stops (`Window.cpp:1107-1117`). A long transfer lets it start, and the transfer's posted rescan deletes games that list holds. `stage-c/pl25-screensaver.py` FAILs at the pin and the tip. It is the rescan owner's (T2's `SystemData.cpp`) and es-core's to fix; severity is the coordinator's word.
- **CloudText's why table lacks the lock's sentence** `ANOTHER CLOUD SYNC IS RUNNING` (`cloud_setup --seed-folders`, rc 75). The box translates it locally, and the table row is named for the cloud slice.
- **The update check does no network on pixelelated.** `ApiSystem::canUpdate` returns at `:455-456` for `OS_NAME=pixelelated`, so ruling 7's shape question answered itself.
- **The rotation cache needs the inode.** A restore through rclone renames a temporary over the record with the source's modtime, and a one-digit turn is the same size. Mtime and size alone would not see it.
- **`RetroAchievements.cpp:350-363` narrows the now 64-bit ids into `std::set<int>`**, on both sides the same way. Named for its slice.

## What adjustments are needed

- **For the coordinator:** PL-25's severity, and whether the rescan-to-screensaver fix goes into T2's integration or a new bug.
- **For the remaining slices:** the es-core lock's shape (`WatchersManager::run` calling `check()` under `mWatchersLock`, EP-13) is #585 line 20 and the es-core slice's. CloudText's missing why is the cloud slice's.
- **For the integration window:** the guest halves, listed by step in the hand-back, every one `fix-walk-pending-image`.

## Instruction recommendations

- **`es-code-traps.md`** could carry, as a proposal for the coordinator: a worker must never take a lock that its joiner holds while joining it. Poll instead, or join only a worker that has left its answer (S4a).
- **The same file or `engineering-practices.md`:** a process's identity in `/proc/<pid>/cmdline` is its interpreter's for a script (S4b). A name test reads the first field, then the script field after `sh` or `bash`, never a substring of the whole line.
- Both are proposals only: the lane changes no rule (the brief's § What never runs here).

## Time to play

- **S1a alone touches the launch path:** `saveToXml` writes the launch's `%GAMEINFOXML%` with one `rename(2)` where there was a remove and a save.
- **The exit save's cost** (S1b item 4, D-CLOUD-119's 3 s), for one dirty game:

  | Entries | Pin | S1a | S1b |
  | ---: | --- | --- | --- |
  | 1,000 | 0.7 ms | 0.8-0.9 ms | 0.8-0.9 ms |
  | 10,000 | 6.5-7.0 ms | 8.0-8.3 ms | 8.4-8.5 ms |

  The device's factor and the real fsync are not priced on the host.
- **No other stream is on the launch path.** S4a takes the sign-in off the watcher lock, so a page's close no longer waits on it.

## What T34 to T37 inherit

1. **PL-25's fixture and read** (`stage-c/pl25-screensaver.py`, `stage-e/pl25-read.txt`).
2. **The es-core lock shape** (#585 line 20), with S4a's worker as the fork-side model.
3. **CloudText's missing why row**, and `RetroAchievements.cpp`'s `std::set<int>`.
4. **Three patches for other lanes' files** under `stage-e/patches/`, each proven on a scratch copy.
5. **`stage-e/handback-run.sh`:** one command for every harness at a tip, with expected rcs.

## Scoped audit (Step 2.5)

- **AC conformance:** PASS. Each of the 22 bugs' fix is in its stream's commit, with its before and after under `stage-e/`. #1270's 26 checkboxes are ticked from the Phase 7 table. `box-check --issue 1270` reads 0 open and 0 fail, and the 22 bugs read 0 fail. The bugs stay open until the pin moves on `next`.
- **Cornerstone spot-check:** PASS.
  - Temp-and-rename and checked writes everywhere this stage wrote (D-CLOUD-078).
  - The French in the same commit as the English (D-UI-051).
  - Comments ASCII: 0 non-ASCII added lines outside the catalog.
  - No change in another lane's file; patches only.
- **Interaction-defect scan:** PARTIAL. PL-25, the rescan against the screensaver, is an interaction defect between two slices, found and recorded, not fixed here.
- **Futro prediction verification:** SKIP. No futro was run for this stage; the brief's own rulings served as its plan.
- **Housekeeping (full-suite scan):** PASS. `TOTAL: 245 test cases in 5 binaries`, 0 failed; 30 harness runs, 0 unexpected; the stand-in rc 0 on all 14 edited `.cpp`.
- **Harness self-coverage:** PASS. Each new harness FAILed at the pin before it PASSed (`stage-e/s4a-before.txt`, `s4b-before.txt`, `s5-before.txt`, `pl25-read.txt`).
- **Documentation and glossary freshness:** PASS. `docs/es-menu-map.md` was updated in S7, and `es-menu-map-check` reads 0 missing.
- **UI review:** SKIP. No guest in stage E; every frame is owed at the integration window.
- **Build-vs-adopt:** SKIP (fixes only).

## Code-verifiable state

| Stream | Bugs | ES commit | Positive |
| --- | --- | --- | --- |
| S1a | #1271, #1285 | `d0d92dda6` | `l313-update-gamelist`, `l313-gamelist-save` |
| S1b | #1271 | `dd86d7ce2` | `l313-gamelist-merge` |
| S2 | #1272, #1275, #1287 | `4e9a7d166` | `l06-*`, `s2-collection-files` |
| S3 | #1274, #1279, #1291, #1292, #1282, #1278 | `0b369b44b` | `l309`, `l321-*`, `l331`, `l335`, `s3-tables`, `TextFitTests` |
| S4a | #1276, #1288, #1283 | `b902cc8ba` | `l12`, `s4a-token-check` (ASan and TSan) |
| S4b | #1286, #1281, #1280, #1284, #1285, #1289 | `a5273390e` | five doctest cases, `s4b-cloudoffer`, `s4b-writes` |
| S5 | #1273, #1290 | `d370ac62e` | `l07` (drop, engine, l08), `s5-bluetooth` |
| S6 | #1277 | `f802c55c6` | `l329` |
| S7 | #1270 checkbox 17 | distribution `75f696b22d` | `es-menu-map-check`, the grep |
