# Running log — M6.P2 T31, EmulationStation's other pages (#678)

- **Executor:** Opus 5.5 at high effort, the session `m6-t5-build-engine` (the dispatch comment on #678, 11:59 UTC on 2026-10-27, comment 6441337287).
- **Depth:** Independent -- one seat, GPT-6 Astra at `max`: a probe and one refutation, exactly two keyed invokes.
- **The brief:** `docs/reviews/briefs/es-pages.md` at `34e130d2ce` (version 2), byte-equal to the tree's copy (`git diff --quiet 34e130d2ce HEAD -- <brief>`).
- **reviewed-at:** `da7922a7bd`, the distribution worktree's HEAD at dispatch (the pointer's seeding; the dispatch merge `3d591f7e30` of the coordinator's `266a14163e`).
- **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`. The ES worktree `feature/m6-es-pages-678` is at the pin and clean.
- **Can this be done on the VM?** Yes. The host goes first: every read, count and table, and the harnesses that extract a page's functions and compile them with the host's `g++`. Then one guest window, asked for on #678 at stage B's end with its plan and bound, and granted in the shared log's queue. The QA accounts only; nothing runs on a handheld or against the owner's accounts.
- **The rules followed:** this worktree's `.claude`, `CLAUDE.md` and `AGENTS.md` differ from local `next` (`8ebaf8daad`) because they carry the coordinator's branch, which is newer than `next` (`git diff --stat next -- .claude CLAUDE.md AGENTS.md`: 9 files, 194 insertions, 5 deletions). They are the same nine files T26 read at its stage A, under the same rules this session has followed since (a total is the tool's line; `rc=$?` on its own line; a stub checked against the unfixed code before its FAIL is recorded; a stream's non-ASCII grep judges the lines it added).

## [Stage A] 12:00 to 12:07 UTC — the first commands, the block, the runs, the context

- **The host at dispatch** (12:03:16 UTC): qemu 0, compilers 0 (`pgrep -c -x qemu-system-x86`; `pgrep -c -f '[c]c1plus|[n]inja'`), `/workspace` inodes 26% used. `/tmp/m7-m6-host-coordination-20261023.txt` ends with the coordinator's `T26 RETURN ACKNOWLEDGED` (08:31 UTC): the host is free. No guest runs from this lane before a grant on #678.
- **The first commands (§ 1)** (`stage-a/first-commands.txt`, 12:00:41Z), all as the brief expects: the worktree clean (0); stacked on `8ebaf8daad`; no change under `packages` or `projects` since it; `651150fc88` present locally; the ES worktree at the pin, 0 changes; the merge base with `rocknix/master` `cada856d86`; `rocknix/master` `f6c542872e`; T2's punch list reachable (36 items); `register-check` passing.
- **The membership block (§ 2)** (`stage-a/membership.sh`, its output `stage-a/membership.txt`, 12:01:06Z, rc 0): `selects 1 paths 76 lines 15537 {'shipped': 76} {'upstream-carried': 64, 'fork-own': 12}`; 37 `c++` and 39 `c-header`; 4,230 lines on the inventory's fork-own tier; `wc -l` 15526 and `grep -c` 15537; 73 of the 76 in the merge base; `12 files 1207 added 129 removed`.
- **The runs (§ 5)** (`stage-a/runs.sh`, run by `tools/t31-run-runs.py`, its output `stage-a/runs.txt`, each with its wall time and exit): every figure as the brief expects, among them:
  - the scope 90/14/76, no subdirectory under `guis/`;
  - the bases: `cada856d86` (with `rocknix/master`) and `bccd715707` (its parent: `rev-list --count bccd715707..cada856d86` is 1); `rocknix/master` 14 commits past the base, 8 of them touching `guis/` and none a slice file (0 slice rows; GuiMenu's 152/2 and 1/0 are T26's); the pin 724 commits past the base; the fork's 12 rows (9 M, 3 A), 1207/129;
  - 891 `_("` lines in 37 files; 50 `GuiMsgBox` sites in 18 files; 26 `addSwitch` lines in 6 files (3 with the literal in the 4th slot, 20 in the 3rd); 12 cached `exists(` reads in 5 files, 0 with `, false)`;
  - `runSystemCommand` 6 in 3 files, `executeScript` 5 in `GuiMoonlight.cpp`, `system(` and `popen(` 0;
  - `clearButtons(` 3 in 2 files; `std::thread` 18 in 13 files; `GuiLoading<` 18 in 12; `postToUiThread(` 9 in 5; `AsyncNotificationComponent` 3 in 2;
  - 79 `getHelpPrompts` lines and 8 `.cpp` without a definition; `atoi(` 9 in 3 files; `multiLine` 8 in 3, `addWithDescription(` 14 in 7; the reboot flags 0 and 0;
  - the harness sweep: `GuiSaveState` → `TimeTextTests.cpp`, `GuiSettings` → four `tests/*.py`, `GuiLoading` → `launch-capture-gate.py`, 15 `.py` under `tests/`;
  - `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (rc 0);
  - `es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without` against `bccd715707`, and **703 / 703 / 0 against `cada856d86`** (the line the brief left to the lane);
  - `es-syntax-check` exit 2 with no build root; `g++`'s first error `InputConfig.h:6:10: fatal error: SDL_joystick.h` (rc 1);
  - the removal check empty against `3d591f7e30` and against the pin.
- **The brief's non-ASCII adjacency grep is malformed.** `$G -B1 '_\("'` is a basic-regex error (`\(` opens a group), and the run printed `Unmatched ( or \(` once per file, 76 times. The count itself (0 files with a non-ASCII comment) is a separate grep and stands. Rerun with `-F '_("'` over the same `-A1` windows: 0 adjacent lines (`stage-a/reruns.txt`). Reported to the coordinator in the checkpoint; the brief is theirs to correct.
- **Not run at stage A:** the title shapes (§ 5 line 838). Its script, `tools/t31-titles.py`, is written at stage B.
- **The callers** (`tools/t31-callers.py`, its output `stage-a/callers.txt`): 39 classes named by the 76 paths' basenames; who constructs each or calls a static of it, outside its own two files. A short paths file is a constructed negative, and it exits 1 (`FAIL t31-callers: 5 classes, expected 39`). **One class has no caller: `GuiAutoScrape`**, which nothing includes or constructs at the pin. It is a Q7 lead for stage B.
- **The history** (`stage-a/history.txt`): the fork's 58 commit lines over the twelve files, `cada856d86..16dbac5211`, no merges.
- **Read at stage A** (`01` § Context): the dispatch comment whole; the brief whole with its two version notes; #678's body (21 checkboxes); T2's punch list at the lines the brief routes (`:109`, `:295`, `:614-615`, PL-016's and PL-031's resolution rows); T26's `02` § What T31 to T37 inherit and its retro.
- **Nothing else ran:** no image build, no fetch, no guest, no handheld, no council call.
- **A correction (stage B):** the stage-A heading above first read 12:00 to 12:20 UTC, the pointer 12:25, and the checkpoint on #678 was headed 12:28 UTC. All three were times written by hand, not read from a clock. The commit is at 12:07:06Z (`git log --format=%cI`) and the post at 12:07:50 UTC (the coordinator's note, 12:09 UTC). Corrected here, in the pointer, and in the comment's heading. From now on a time in a record comes from `date -u` in the same command that makes the record.

## [Stage B] 12:10 to 12:23 UTC — the generators, the reading, 02, the window plan

- **Six generators under `tools/`**, sharing `t31lib.py` (the call parser). Each asserts its counts and exits 1 on drift, and each was seen to exit 1 on a constructed drift:
  - `t31-dialogs.py`: 50 sites; back lands on OK 30, NO 18, CANCEL 1, CLOSE 1. GuiMsgBox's rule is read from `GuiMsgBox.cpp:116-134`.
  - `t31-titles.py`: the checker's own patterns and `names_screen`, 12 / 27 / 10 / 12, the brief's hand counts.
  - `t31-rows.py`: 50 calls.
  - `t31-reads.py`: 26 sites.
  - `t31-pages.py`: 37 pages and 2 header-only units, every census total as the brief's runs except `popen` (1).
  - `t31-callers.py`, from stage A.
- **The generators were corrected as they were read:**
  - a receiver match that crossed a comment's end hid the DEVELOPER ID row, found by its absence;
  - `std::atoi` was missed by a pattern that excluded `::`;
  - header-only files were missed by a per-`.cpp` loop;
  - the no-title count first excluded computed titles. The brief's 10 counts no `_()` title, with `GuiMoonlight`'s raw literal among them.
- **The reading:** the twelve fork-touched files (the three fork-own and four modified whole, the rest at the fork's diff and the leads' lines), `GuiLoading.h` whole, and the upstream pages at every lead's lines (`stage-b/`, `02` § Leads).
- **`02`:** 25 leads. New against the brief:
  - L-01: START drops every open settings page's choices; upstream in both trees, reaching the fork's pages;
  - L-02: the LED colour is never saved to `system.cfg`;
  - L-03: a relay change drops ENABLE NETPLAY;
  - L-04: PLAYER PASSWORD is shown in clear;
  - L-05 and L-06: Moonlight's unquoted SERVER IP, and an unpair that removes nothing and says it cleared;
  - L-07: Moonlight's raw English title, unmapped and invisible to the checker;
  - L-19 to L-21: three back landings that act;
  - L-22: `GuiLoading`'s unsynchronised `mRunning`;
  - L-23: `GuiAutoScrape` is not compiled.

  Corrections to the brief: seven, in `02`.
- **The window plan** (`stage-b/window-plan.md`): thirteen steps, 45 minutes plus 5 of grace, stopped by pidfile at the bound; the identity by two literals first.
- **Nothing else ran:** no image build, no fetch, no guest, no handheld, no council call.

## [Window] 12:25 to 12:45 UTC — the guest, granted on #678

- **Granted** at 12:25 UTC (comment 6441815522). The guarded swap reclaim ran once before the guest (`READY`, 7,331 MiB of swap used to 0). **START** 12:26:47 UTC (comment 6441849481); **RETURN** posted after the stop at 12:45:00 (comment 6442212756), each with its census (qemu, compilers) and a line in the shared host file. The guest was stopped by `tools/vm-stop` on its pidfile (rc 0), 18 minutes into the 45.
- **Proved on the image** (M7's composition over the pin, by its two literals): L-01, L-03, L-06, L-07 (FR), L-11 (FR), L-12, L-13 (with a new fact: a copy that worked leaves the same frame as one that failed), L-15 and L-16; and two back landings on NO. **New:** BIOS CHECK draws no help bar under full-screen menus; offline SCRAPE NOW ends on the main menu with a box, not on SCRAPING GAMES. **CANNOT:** L-09 offline, G10, G11, L-19 by design.
- **The disk retired:** `t31.qcow2`, 2,510,749,696 bytes, sha256 `8aee68ee…b2a596`, removed; the leftover check is clean (`guest-cycle/retired.txt`).
- **Mine:**
  - a START pressed before the carousel settled did not land, so G03's first pass entered PICO-8 instead of the menu;
  - two up presses put the focus on BACK rather than the tab strip;
  - right presses sent while the manager slid in did not move its cursor.

  Each void pass is recorded and redone with a frame per press.
- **Correction:** `02`'s correction 5 ("writes only on a change") is wrong in effect. A save function stores a value the player never chose, and `Settings` counts a default as a change. This is corrected in `04`.
- **Nothing else ran:** no image build, no fetch, no handheld, no account, no council call.

## [Stage C] 12:24 UTC onward — the host proofs

- `stage-c/t31extract.py` holds the shared extractor and runner.
- **L-01** (`l01-start-drops.py`): FAIL at the pin (START drops the switch, writes 0 times, skips `onFinalize`). The control replaces START's loop with `close()` per page and passes.
- **L-02** (`l02-led-not-saved.py`): FAIL at the pin (`system.cfg` written 0 times). The control adds one save function and the colour is saved.
- Their outputs are in `stage-c/runs.txt`.
- **Keyed call 2 of 2,** the refutation: 12:59:34 to 13:14:26 UTC, rc 0, served `openai/gpt-6-astra` by OpenAI at `max`, with identity, effort and provider verification PASS. **Exactly two keyed invokes, and no others.**
- **The grades** (`stage-c/astra-grades.md`): 43 items, 41 accepted, 1 in part (EP-33), 1 not kept (EP-26), counted by `awk`. Sixteen new leads, L-28 to L-43, Moonlight's six among them. The narrowings are written into `02`'s leads in place, citing their EP items.
- **The seat found a bug in this lane's own census:** two `addSwitch` calls inside a `/* */` block were counted.
  - `tools/t31lib.py` now scans comments and strings; four constructed cases pass.
  - The first fix attempt dropped real sites, because a `/*` inside `"rm .../*"` read as a comment. The dialog count fell from 50 to 46 and was caught by its own assertion.
  - Every generator was rerun: 48 rows, 21 switches.
- **Corrected by the seat** (EP-4): stage B's and the window's explanation of L-16, "a default counts as a change", was wrong. The setters change only on an absent key or a different value; the two mtimes stand as observations.
- **05:** 27 items (7 medium, 20 low, counted from the index). `tools/lint-audit-artifacts --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)`.

## [Stage D] 13:3x to 13:23 UTC — the audit issue, the pause

- **The audit issue:** #1234, `Audit: M6 T31 EmulationStation's other pages -- 27 findings (0 critical, 0 high, 7 medium, 20 low, 0 info)`. Labels `audit` and `punch-list`, milestone M6, body generated by `tools/t31-issue-body.py` from `05` at `a7b0899e12`. It is a sub-issue of #678, read back from #678's sub-issues.
- **Checks:** `tools/box-check --issue 1234`: 27 open checkboxes, 0 fail. `tools/lint-audit-artifacts --phase pre-issue --issue 1234`: `PASS pre-issue artifacts (does not certify resolution)`.
- **The pause:** the punch list is posted on #678 with the questions for the coordinator. No `bug` is filed and no fix is made before the ruling.
- **The ruling** (13:27 UTC, comment 6443081619):
  - PL-01 is fixed under D-UI-128;
  - the Moonlight cluster (PL-03 to PL-06, PL-15, PL-16) is one stream under rule 6;
  - PL-14's title goes through `_()` with the page mapped;
  - PL-13 is D-UI-129, and the completed-run misreport is T32's L-02, recorded in `02`;
  - PL-24 is recorded with #585 lines, one per landing, in `02`;
  - PL-25 is Backlog #1235.

  The rows are on the coordinator's branch (`acb7ead172`), not this one.
- **The bugs** (filed by 13:32 UTC): 21, #1236 to #1256, one per bug item (`tools/t31-file-bugs.py`). Each carries its `05` section with the ruling, a four-part code trace, its `Already written:` line and its VM line. Each passes `tools/box-check --issue N` (0 fail). They are cross-linked from `05` (a `Bug:` line per item) and from #1234's item lines, both read back with 21 links. `box-check --issue 1234` 0 fail; the pre-issue lint PASS.

## [Stage E] 13:51 UTC onward — the streams

- **The brief:** `docs/reviews/briefs/t31-streams.md` at `17be18bde5` (the coordinator's; comment 6443605741). Fourteen streams in its order: S1, S2, S13, S5, S11, S3 with S8, S4, S14, S9, S10, S12, S7, then S6 after cherry-picking `a73ed9efc`.
- **The floor:**
  - `tools/t31-build-tests.sh`: T26's `t26-build-tests.sh`, copied by `git show` from `feature/m6-es-guimenu-673` and renamed.
  - rapidjson 1.1.0 from the source cache, its sha matching the recipe's `PKG_SHA256`, with the recipe's four patches, under `/workspace/tmp/m6-t31/rapidjson`.
  - `stage-e/syntax-check.sh` and `stage-e/fakes/`: T21's, by `git show` from `feature/m6-es-state-and-bridge-668`.
  - `stage-e/checks.sh`: T26's, adapted.
- **The baseline at the pin** (`stage-e/s0-pin-checks.txt`): `TOTAL: 221 test cases in 4 binaries`; the 15 `tests/` harnesses rc 0; the five stage-C positives FAIL; the map check `0 missing`; French 706 and 703 with 0 without. The build script refuses without rapidjson (rc 2).
- **S1** (#1236): ES `9cb0e5c9a`, pushed after `.githooks/pre-push-test` PASS. `l01-start-drops.py` went from 4 of 5 FAIL to `5 cases`; the checks are clean (`stage-e/s1-*.txt`).
- **S2** (#1237): ES `1ca322f75`, pushed after pre-push-test PASS. `l02-led-not-saved.py`, extended, went from 2 of 3 FAIL to `3 cases` (the no-change page writing 0 times both before and after); the checks are clean (`stage-e/s2-*.txt`).
- **S13** (#1255): ES `03a929e02`, pushed after pre-push-test PASS. A new harness, `stage-c/s13-text-row.py`: 2 FAIL at S2's tip, then `3 cases`; the checks are clean (`stage-e/s13-*.txt`).
- **S5** (#1243): ES `82f80693d`, pushed after pre-push-test PASS. A new harness, `stage-c/s05-replace-saves.py`: 2 FAIL, then `2 cases`. Mine: the harness's first after-run stopped on the apostrophe in the fix's own comment, because its lambda reader skipped no comments. It was fixed, and the before was rerun on the unfixed files: still 2 FAIL (`stage-e/s5-*.txt`).
- **S11** (#1253): ES `a8dcc23ea`, pushed after pre-push-test PASS. The rows tool's line for `GuiGameOptions.cpp:204` read `plain` before and `password` after (`stage-e/s11-*.txt`).
- **S3** (#1238, #1239, #1240, #1241, #1248, #1249, #1250): ES `70db6535b`, pushed after pre-push-test PASS. `python3 -I stage-c/s03-moonlight.py <W> [<GuiMoonlight.cpp>]` (new; the page compiled whole against stand-ins, each case in bubblewrap with a 5 s watchdog) read 15 of 16 FAIL on `a8dcc23ea`'s page (`update-keeps` the control) and `s03: PASS, 16 cases` after; `credential-quoting` 9 to 11 sites, and its constructed bare site caught; the map check 1 missing without the map entry, 0 with it (`stage-e/s3-*.txt`). The map entry is its own commit on this branch.
- **S8** (#1234, PL-17): **stopped at the checker**, as the brief's § S8 directs. The draft map (`stage-e/s8-map-draft.patch`: BIOS CHECK and SCRAPING GAMES mapped, ten upstream pages declared) leaves `t31-titles.py` with 0 pages in neither place (12 before), and `es-menu-map-check` at `70db6535b` still reads `0 missing`, but it exits 1 on ten `STALE ... declared unmapped but no longer exists` lines, one per declaration of a title its three shapes cannot see (#951, #965). No declaration was deleted to make it green and the map is unchanged on this branch (`stage-e/s8-before.txt`, `s8-stopped.txt`). The stream is the coordinator's; the lane goes on with S4.
- **S8** (#1234, PL-17), ruled at 14:27 UTC: BIOS CHECK and SCRAPING GAMES mapped; the ten upstream declarations as HTML comment lines in `## Not mapped`, waiting on #951/#965. `es-menu-map-check --ref 70db6535b` `0 missing`, rc 0; `t31-titles.py --expect=13,28,9` 10 in neither place, those ten (`stage-e/s8-after.txt`).
- Mine: the S8 map commit `50f5d08ccd` cited D-UI-129, a row this branch's register does not carry yet (it is on the plan branch at `acb7ead172`); `tools/register-check` failed after the push, and the next commit cites the stage-D ruling on #678 instead. The ID returns to the map at integration, when the row is on the branch.
- **S4** (#1242, #782's caller half): ES `f9b97b3ea`, pushed after pre-push-test PASS. `python3 -I stage-c/s04-copy-press.py <GuiSaveState.cpp>` (new): 4 of 5 FAIL on S3's tip, `s04: PASS, 5 cases` after. `bash tools/t31-bookkeeper-tests.sh <es tree> <build>` (new; tests/app-unit's bookkeeper-tests built by host g++ from its CMake block): the new cases do not build against the old bookkeeper (no such job), its own 5 PASS; after, `8 | 8 passed` (`stage-e/s4-*.txt`). `checks.sh` runs both from S4 on.
- **S14** (#1256): ES `bc3959c69`, pushed after pre-push-test PASS. `SaveStateOrderTests.cpp` (new, in es-unit-tests) 3 of 4 FAIL over the lifted `>=`, then PASS; `python3 -I stage-c/s14-sort-debug.py <W>` (new) rc 1 then `s14: PASS`; `TOTAL: 225 test cases in 4 binaries` (`stage-e/s14-*.txt`).
