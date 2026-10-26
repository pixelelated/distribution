# Running log — M6.P2 T20, EmulationStation's RetroAchievements and offline pages (#667)

- **Executor:** Opus 5.5 at high effort, the session `m6-t5-build-engine` (the dispatch comment on #667, 17:09 UTC).
- **Depth:** Extended -- two seats, GPT-6 Astra at `max`, then Gemini 4 Argon at `high`.
- **The brief:** `docs/reviews/briefs/es-achievements-pages.md` at `14852bd6ed` (version 2), byte-equal to the tree's copy.
- **reviewed-at:** `ae3c013cac`, the distribution worktree's HEAD at dispatch, which is the lane tip the dispatch names.
- **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`. The ES worktree `feature/m6-es-achievements-pages-667` is at the pin and clean.
- **Can this be done on the VM?** Yes. The host goes first: every read, count and table, and the unit tests built by the generated `g++` commands. Then comes one guest window, asked for on #667 after stage B and granted in the shared host file's queue. It uses the QA RetroAchievements account only, never the owner's (D-QA-015/016). Nothing runs on a handheld.
- **The rules followed:** the session loaded them from the T5 worktree (`m6-build-engine-652`). This worktree's `.claude`, `CLAUDE.md` and `AGENTS.md` differ from local `next` (`git diff --quiet next` is non-zero). The coordinator's branch, merged here, carries the brief's rule ranges (§ 3), and those are the copies read for the ranges the brief cites.

## [Stage A] 17:09 to 17:30 UTC — the first commands, the block, the runs, the build

- **The host at dispatch:** `/tmp/m7-m6-host-coordination-20261023.txt`'s last entries are the coordinator's mirror of T19's window, closed at 12:55 UTC ("qemu 0, listeners 0, compilers 0"). There is no M7 line after it. The census at 17:17:23 UTC: qemu live 0, compilers 0.
- **The first commands (§ 1):** the worktree clean (0); stacked on `8ebaf8daad`; no change under `packages` or `projects` since it; `651150fc88` present locally; the ES worktree at the pin, 0 changes, merge base `bccd715707`; T18's punch list reachable (23 items); `register-check` OK.
- **The membership block (§ 2):** `selects 2 paths 25 lines 7485`; shipped 25; fork-own 24, upstream-carried 1; read 23 (7,427), unread the two notices; fork-own 7,474; libcheevos 9 rows (2,556); `wc -l` 7,485; 15 paths in the merge base. Every figure is as the brief states. `.qa-scratch/t20/paths.txt` holds the 25; `.qa-scratch/` is gitignored.
- **The runs (§ 5),** each with its exit and wall time, in `01` § The runs at stage A and `02` § The runs at stage B. The deltas from the brief:
  - **R5:** `maskSecrets` appears in 11 files, ten `.cpp` (the definition `StringUtil.cpp` among them) and its header. The brief counts ten.
  - **R14:** the RetroAchievements cases of `CloudTextTests.cpp` by the brief's word regex: **0**. The test names say `raofflineproxy-ctl` and `proxy`, never *achievement*. By subject there are six (`:1191`, `:1228`, `:1314`, `:1334`, `:1359`, `:1577`).
  - **R17:** the host `g++ -fsyntax-only` falls, as the brief expects, on `SDL_joystick.h` (through `es-core/src/InputConfig.h:6`) for `OfflineAchievements.cpp` and `GuiOfflineScan.cpp`, and on `curl/curl.h` (`es-core/src/HttpReq.h:5`) for `RetroAchievements.cpp`.
  - **R16:** `tools/es-syntax-check` exits 2 with `ES_BUILD_ROOT=/nonexistent` ("no build root"). That is its CANNOT, never a pass.
- **The unit tests, built by the generated commands:**
  - **The scripts:** `tools/t20-build-tests.sh` is T18's renamed; `tools/t20-build-app-tests.sh` is T18's jobs build with the target an argument.
  - **rapidjson:** the distribution's own `rapidjson-1.1.0.tar.gz` from the download cache. Its sha256 `bf7ced29…` equals the recipe's `PKG_SHA256` (`projects/ROCKNIX/packages/devel/rapidjson/package.mk`). The recipe's four patches are applied in order, as the build does, into `/workspace/tmp/m6-t20/rj/`; patches 0002 and 0003 remove the assignment operator GCC 15 rejects. The patched `document.h` is `a8c29c92…`, the same bytes T18's copy had. No M7 prep directory was read: this brief forbids it, where T18's run took its copy from one.
  - **At the pin:** `es-unit-tests` 185 of 185, `es-file-tests` 24, `es-conf-tests` 10, `es-file-tests-win32` 2, `jobs-tests` 6, `proxycards-tests` 11. All pass, with g++ 15.2.0.
- **Read at stage A:**
  - the brief whole, and the dispatch comment;
  - the issues the tree names (#186 to #1144, listed in `01`);
  - the callers of the 25's entry points;
  - each file's history since the merge base;
  - T19's `02` § What T20 inherits at `d8c02be1c9` (landed: lines 257-307, 10 KB). It is consumed at stage B.
- **The kickoff notes (the dispatch, as errata at stage A):** `scanWhy`'s `NO_GAMES_FOUND` row, which the brief's why table omits; and `Settings.cpp:420`'s `.hardcore` default, inside `#if WIN32` (`:417-433`), which matters only if `Paths::getSystemConfFilePath()` can be empty on ROCKNIX (T21's Q4). Both are carried into `01` and read at their lines at stage B.
- **Nothing of the never-run list ran:** no build of an image, no fetch, no guest, no keyed call, no M7 root, worktree or prep directory. The ES worktree is at the pin, its diff empty (R18), and the distribution's `packages`, `projects` and `tools` are unchanged since `ae3c013cac`.

## [Stage B] 17:30 to 17:32 UTC — 02, the host positives, the window request

- **Read whole at the pin:** the 16 interface files and `rvz_hash.*`. The five modified libcheevos files are read as diffs against `bccd715707`, and the two notices as present and shipped (`package.mk:58-64`). The neighbours read where a contract crosses: `ApiSystem.cpp:2262-2293`, `HttpReq.{h,cpp}`, `ProxyCards.cpp:196-385`, `CloudText.cpp:1018-1066` and `:1186-1270`, `FileSystemUtil.cpp:1369-1427`.
- **The ctl** is read at `8ebaf8daad` (`projects/.../raofflineproxy-ctl`, the same bytes at `ae3c013cac`), and T19's § What T20 inherits is consumed in `02` § The contract. One correction to T19's table: `TOOK_TOO_LONG` reaches `topUpWhy` through its fall-through to `scanWhy`.
- **Both kickoff notes are read at their lines.** `NO_GAMES_FOUND` is a row no producer emits (L-08). `Settings.cpp:417-433` is `#if WIN32`, and `Paths.cpp:94` sets the ROCKNIX path, so no second `.hardcore` store is live (T21's Q4 owns `Paths`).
- **The rule ranges** the brief's § 3 cites in `generic-x64-vm-testing.md` are read (`:326-334`, `:495-500`, `:754-760`, `:890-895`, `:1150-1161`, `:1169-1186`).
- **Six host positives,** each built with the host `g++` from the pin's own lines and kept under `stage-b/positives/` with its output. No ES file changed, and none was built in the ES worktree.
  - **L-06:** a `popen` child killed by `SIGKILL` reads rc 0.
  - **L-05:** a 1,500-byte line loses its head, and a last line with no newline is dropped.
  - **L-20:** `throw e;` shows `std::exception`.
  - **L-07:** T19 S8's `unknown` reads as 0, at both the scan page's `done` and the stamp's `ready`.
  - **L-13:** a two-byte `cached_game_ids.txt` reads as empty.
  - **L-25:** ES's RVZ padding equals Dolphin's on 4,000 cases, 3,032 of them unaligned. The control fails all 4,000.
- **A lead withdrawn before it was written:** `rvz_hash.cpp:87`'s shift `18` is Dolphin's documented oddity ("NB: 18, not 16"), not a slip. The fixture above is the proof.
- **`02`:** Coverage holds 25 rows, by the brief's own command. It also carries the credentials' paths, the pages, the contract, the reader, the hasher, the library, the runs, the positives and what T21 and T26 inherit. The guest cycle is pending the window.
- **Nothing of the never-run list ran.** No guest, no fetch, no keyed call. The ES worktree is unchanged (R18).

## [Window] 17:34 to 17:57 UTC — the guest cycle

- **Granted** on #667 at 17:34 UTC. START 17:36:17 and RETURN 17:57:04 were posted with their censuses and mirrored in the host file; the bound was 18:36:17. The guest ran from M6's copy on a fresh disk at 640x480, ssh by a key of the lane's own.
- **What ran:** the eight steps of the request, recorded in `02` § The guest cycle. The one live sign-in used the QA account through `tools/qa-accounts`, never printed and never the owner's. The #1154 probe used dummy credentials only. `tools/ra-ui-test` is CANNOT in this window: four EN attempts, three failing closed on the tool's own preconditions, two of them states I had made.
- **The image's ES is M7's composition over the pin.** It carries the pin's literal and pages the pin does not have, so the page frames are M7's. This was found at step 4's first frame, not at step 1. Checking one identity literal answered "contains the pin", not "is the pin".
- **Two errors of mine.**
  - A kill by pattern: `pgrep -x sleep | head -1` hit `video_sense`'s `sleep 3600` (`g02b`), against the PID-only rule. It was voided in the record.
  - A first `openssl req` under `set -e` with its output silenced stopped without a word. The image has no `openssl.cnf`; nothing had changed.
- **Closed:** `vm-stop` rc 0; the disk retired with path, size and sha; the account's four keys emptied on the guest before the stop. No image build, no fetch, no handheld, no M7 root or worktree.

## [Stage C] 17:58 to 18:37 UTC — 04, the packet, four keyed calls, 80 items graded, the pre-issue lint

- **`03` and `04`** were written as the first reader's before the packet was built.
- **The runtime:** `npm install --offline --ignore-scripts` in `tools/council/`; `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`. No fetch.
- **The packet:** `second-opinions/packet.md`, 354,904 bytes, built by `stage-c/packet.py`. The scan's figures and its 48 shape dispositions are in `04` § Second opinion; a first build stopped on 43 review lines, each read through the mask and dispositioned before the rebuild. `review-plan.json` was written before the first call.
- **The keyed calls: exactly 4, and no others** (`stage-c/keyed-calls.txt`; every other `tools/council/run` call ran with `COUNCIL_ENV_FILE=/nonexistent`; the key file was never read by me):
  1. Astra's probe, 18:05:10 to 18:05:23 UTC: PASS, `openai/gpt-6-astra` by OpenAI, effort `max`.
  2. Astra's refutation, 18:05:34 to 18:22:23 UTC: one attempt, `finish=stop`, 55 items.
  3. Argon's probe, 18:23:49 to 18:23:56 UTC: PASS, `google/gemini-4-argon` by Google, effort `high`.
  4. Argon's refutation, 18:24:18 to 18:33:50 UTC: one attempt, `finish=stop`, 25 items.
- **The provenance, read directly** (`stage-c/provenance-read.py`): all four `verification=PASS`, served model and provider the seat's, each output's sha256 matching, `facilitator_version council-facilitator@1.14.1-pixelelated.2`.
- **The grades:** Astra 48 accepted, 6 in part, 1 plausible, 0 rejected; Argon 24 accepted, 1 in part, 0 rejected. Each item was re-read at its lines. The corrections and the new leads L-26 to L-32 are in `02` § Corrections and new leads from the seats.
- **`05`:** 25 items, PL-01 High; PL-02 to PL-07 Medium. Ten are proposed as `bug`s.
- **`tools/lint-audit-artifacts --phase pre-issue`:** `PASS pre-issue artifacts (does not certify resolution)`.
- **The host:** M7 has held it since 18:19 UTC (the coordinator's comment); nothing here needed it.

## [Stage D] 18:38 UTC — the audit issue and the pause

- **#1167**, `Audit: M6 T20 EmulationStation's RetroAchievements and offline pages -- 25 findings (0 critical, 1 high, 6 medium, 15 low, 3 info)`, labels `audit` and `punch-list`, milestone M6, is a sub-issue of #667 (read back: #667's sub-issues are `1167`).
- **Checks:** `tools/box-check --issue 1167`: 25 open checkboxes, 0 fail. `tools/lint-audit-artifacts … --phase pre-issue --issue 1167`: `PASS pre-issue artifacts (does not certify resolution)`.
- **The pause:** the punch list is posted on #667 for the coordinator's dispositions and any stream brief. Nothing in the ES worktree or under `packages/`, `projects/` or `tools/` has changed (R18).
