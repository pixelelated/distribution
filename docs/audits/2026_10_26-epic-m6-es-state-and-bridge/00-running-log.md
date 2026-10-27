# Running log — M6.P2 T21, EmulationStation's state primitives and its bridge to the OS (#668)

- **Executor:** Opus 5.5 at high effort, the session `m6-t5-build-engine` (the dispatch comment on #668, 20:49 UTC, patched in place at 20:50 UTC).
- **Depth:** Extended -- two seats, GPT-6 Astra at `max`, then Gemini 4 Argon at `high`.
- **The brief:** `docs/reviews/briefs/es-state-and-bridge.md` at `2f1d006461` (version 2), byte-equal to the tree's copy (`git diff --quiet 2f1d006461 HEAD -- <brief>`).
- **reviewed-at:** `4844a773ca`, the distribution worktree's HEAD at dispatch, which is the lane tip the dispatch names.
- **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`. The ES worktree `feature/m6-es-state-and-bridge-668` is at the pin and clean.
- **Can this be done on the VM?** Yes. The host goes first: every read, count and table, and the unit tests built by the generated `g++` commands. Then comes one guest window, asked for on #668 after stage B and granted in the shared host file's queue. It uses one boot of the M6 copy at 640x480, and the QA ScreenScraper account only, never the owner's (D-QA-015/016). Nothing runs on a handheld.
- **The rules followed:**
  - The session loaded them from the T5 worktree (`m6-build-engine-652`). This worktree's `.claude`, `CLAUDE.md` and `AGENTS.md` differ from local `next`; they carry the coordinator's branch, merged here, including T20's two rule edits at `a3f28a19fb`.
  - Four rule files differ from the loaded copies: `device-builds.md`, `engineering-practices.md`, `es-code-traps.md` and `generic-x64-vm-testing.md`. The lane's copies of the first three are read at stage A:
    - a bubblewrap sandbox starts with `--clearenv`;
    - a figure is produced by a command at the hash it is about;
    - a granted window names what stops the guest at its bound;
    - `rc=$?` goes on its own line;
    - a stream's non-ASCII grep judges the lines it added.

    `generic-x64-vm-testing.md` is read at stage B, for the window.
- **The coordinator's correction (20:50 UTC), read:** the highest decided rows are D-WORKFLOW-211, D-RA-051 and D-RA-052, and the compiler census reads 0. The register agrees: those three are Decided rows; D-NET-013, D-UI-120 and D-WORKFLOW-080 are in the open table.

## [Stage A] 20:49 to 21:00 UTC — the first commands, the block, the runs, the build, the errata

- **The host at dispatch:** `/tmp/m7-m6-host-coordination-20261023.txt` (620 lines) ends with M7's RETURN at 18:49:07 UTC (UI04 PASS; UI02 and UI03 retained as failed) and the coordinator's acknowledgement. There is no later M7 line. The census at 20:54:42 UTC: qemu live 0, compilers 0, load 0.42. Swap is full (7 of 7 GiB) with 40 GiB of RAM available; the window request names it.
- **The first commands (§ 1),** all as the brief expects:
  - the worktree clean (0), stacked on `8ebaf8daad`, no change under `packages` or `projects` since it, and `651150fc88` present locally;
  - the ES worktree at the pin, 0 changes, merge base `bccd715707`;
  - T18's punch list reachable (23 items), and `register-check` passing.
- **The membership block (§ 2),** every figure as the brief states (`stage-a/membership.txt`):
  - `selects 1 paths 14 lines 9249`, all shipped and all fork-own;
  - `c++` 7, `c-header` 7;
  - `wc -l` 9,249, and 12 paths in the merge base;
  - no difference between the worktree and the pin on the 14.
- **The runs (§ 5),** the brief's block extracted verbatim into `stage-a/runs.sh` with the dispatch tip `4844a773ca` for its placeholder, run under `bash -x` (`stage-a/runs.txt`, `runs.trace`; rc 0, under one second of wall time; every `git grep` reads the pin's objects). Two deltas from the brief's comments, neither a disagreement between commands:
  - **The shipped `wifictl`:** the pattern `nmcli|password|set_settings` prints `10 18 113 177 270 302 372 383 388 437 460 461`. The brief expects 195 and 209 among them. Those two lines do carry the key, as `802-11-wireless-security.psk "${PSK}"`, but the case-sensitive pattern cannot match them (the binary is `"${NMCLI}"`, and the lines say `psk`). The four lines that put the key on a command line or into the store are 177, 195, 209 and 460 (`stage-a/runs-followup.txt`).
  - **`writeAllText(`:** 27 lines, of which two are the function's definition and declaration (`FileSystemUtil.cpp:1429`, `.h:71`). The call sites are **25**, sixteen of them `ApiSystem.cpp`'s sysfs writes. The writers' generator will carry 25 rows and name the two it leaves out.
  - **Everything else holds:**
    - the 14's delta, 2,510 insertions and 181 deletions;
    - the exit reads (20 lines, 15 `WEXITSTATUS` with the shims at 45-46, 11 without `WIFEXITED`), and `shellQuote` 13;
    - the `batocera-` lines 105 with 36 names, the eight scripts' presence, and the p7zip recipe's `all3` and `bin/7z*`;
    - `maskSecrets` at 2235, 2265, 2297 and 2325;
    - the client's options and defaults, the scraper's lines, the Wi-Fi popups at 295/297/365/367, and the `wifictl` calls without a bound at 642, 767, 771 and 775;
    - the writers' 41 `AtomicFile::` lines, the shell writers' lines, and `chksysconfig`'s 0 lock lines;
    - the readers' lines, the eight test files' 80 cases with no `SettingsTests.cpp`, and the host tools' `--help`;
    - `es-syntax-check` rc 2, and an empty removal check.
- **The host `g++ -fsyntax-only`:** `AtomicFileUtil.cpp` **PASS** (rc 0). The rest are CANNOT, with the missing header named:

  | File | Missing header | Through |
  | --- | --- | --- |
  | `SystemConf.cpp` | `SDL_timer.h` | `:17` |
  | `ApiSystem.cpp`, `GuiWifi.cpp` | `SDL_joystick.h` | `InputConfig.h:6` |
  | `Settings.cpp` | `pugixml/src/pugixml.hpp` | `:7` |
  | `HttpReq.cpp`, `ScreenScraper.cpp` | `curl/curl.h` | `HttpReq.h:5` |
- **The unit tests, built by the generated commands:**
  - **The script:** `tools/t21-build-tests.sh` is T20's `t20-build-tests.sh` at `ffb6b686cb` (itself T18's) with its name and header renamed, 10 changed lines.
  - **rapidjson** (the erratum's provenance): the distribution's own `rapidjson-1.1.0.tar.gz` from the download cache. Its sha256 `bf7ced29…` equals the recipe's `PKG_SHA256`; the recipe's four patches apply in order (each rc 0), into `/workspace/tmp/m6-t21/rj/`. The patched `document.h` is `a8c29c92…`, the bytes T20 recorded and T18's copy had (`stage-a/rapidjson.txt`). No M7 prep directory was read.
  - **At the pin:** `es-unit-tests` 185 of 185, `es-file-tests` 24, `es-conf-tests` 10, `es-file-tests-win32` 2, all passing with g++ 15.2.0 in 41 s, 221 cases in all.
  - **The eight files as run** (doctest's `--count -sf`): `AtomicFileTests` 24 and `AtomicFileWin32Tests` 2 (in the file binaries), `SystemConfTests` 10 (in `es-conf-tests`), `MaskSecretsTests` 12, `WifiTextTests` 19, `CommandLineTests` 2, `LaunchCommandTests` 8, `LogPolicyTests` 3: **80** (`stage-a/unit-pin.txt`).
- **The errata's harness:** the ES repository's `tests/wifi-profile-lifetime.py` extracts `GuiWifi::chooseProfile` and builds it under AddressSanitizer in a temporary directory. At the pin it prints `PASS profile-choice callback survives page deletion`, rc 0, and leaves the ES tree clean (`stage-a/wifi-profile-lifetime.txt`).
- **The errata's inheritance from T20, read by `git show` and never merged:**
  - PL-08's fixture `stage-b/positives/reader.cpp` and its `reader.out` at distribution `ffb6b686cb`. A child killed under `popen` reads as rc 0, a 1,500-byte line comes back as two, and a last line without a newline is dropped. It is Q6's positive to reuse.
  - S2's `HttpReqOptions::httpsRedirectsOnly` at ES `5c0ddaaee`: one `bool`, false by default, choosing `"https"` over `"http,https"` for the redirect protocols at `HttpReq.cpp:227-249`. It is the one change the pin's bytes will show in this slice's files after T20 lands.
- **Read at stage A:**
  - the brief whole, and the dispatch comment with its errata and the 20:50 correction;
  - the 16 issues the brief names, by title, state and closing date only (`01` § The issues); their bodies are read at stage B, where a question needs them;
  - the register rows D-SYS-001 to 014, D-NET-001 to 016, D-CLOUD-078/079 and D-WORKFLOW-166;
  - each file's history since the merge base, and the callers' counts (`01`);
  - the lane's three changed rules.
- **Nothing of the never-run list ran:** no build of an image, no fetch, no guest, no keyed call, no M7 root, worktree or prep directory. The ES worktree is at the pin, its diff empty, and the distribution's `packages`, `projects` and `tools` are unchanged since `4844a773ca`.

## [Stage B] 21:00 to 21:17 UTC — the 14 read whole, 02, the host positives

- **Read whole at the pin,** in the ES worktree (byte-equal to the pin on the 14):
  - `AtomicFileUtil.{h,cpp}`, `SystemConf.{h,cpp}`, `GuiWifi.{h,cpp}`, `HttpReq.{h,cpp}`, `Settings.{h,cpp}`, `ScreenScraper.{h,cpp}`, `ApiSystem.h`;
  - `ApiSystem.cpp` in five reads, 1-3519.
- **The neighbours read where a contract crosses:**
  - `StringUtil.cpp:505-520`, `:715-803` (the mask);
  - `Scraper.cpp:425-460`, `:520-700`, `:779-812` (the media path);
  - `FileSystemUtil.cpp:642-668`, `:1059-1085`, `:1429-1465`;
  - `TextEditComponent.cpp:68-94`, `:170-185`, `:375-378`;
  - `GuiBluetoothDevices.cpp:131-151`, `GuiMenu.cpp:3130-3151`, `:5052-5075`, `:2989`, `:3209`, `:9909`;
  - `HttpServerThread.cpp`'s routes; `main.cpp:1034-1042`.
- **At `8ebaf8daad` (T1's, T17's and T22's files, read only):** `001-functions:1-40`, `:340-610`, `:622-623`; `chksysconfig:280-340`; `backuptool:270-300`; `rocknix-evidence:59-75`.
- **`02-forward-audit.md`:**
  - § Coverage, 14 rows, by the acceptance's own `awk`;
  - the 20 leads, L-01 to L-20, each with its family and `proved:`;
  - § The credentials' paths, 21 rows;
  - § The commands, generated by `tools/t21-commands.py`: 143 rows, cross-checked as 152 - 5 - 4, with `--expect 142` seen to exit 1;
  - § The writers, generated by `tools/t21-writers.py`: 41, 25 and 10 rows, with a wrong expectation seen to exit 1;
  - § The readers, § The client, § The runs (R1 to R24), § Positives, § What T26 and the OS slices inherit;
  - three corrections to the brief by command.
- **The host positives** (`stage-b/positives/`, each built single-threaded with the host's `g++` in seconds):
  - `kill-writer`: 99 kill points, every one leaving the old or the new state whole; 42 leave a temporary nothing sweeps (L-09).
  - `shell-writers`: `8ebaf8daad`'s `001-functions` in bubblewrap with `--clearenv`, the donor's busybox as `/usr/bin`, no path rewritten. The kills keep the file whole. **S1:** the seed copied before the lock and the record, then recorded over the player's record by the pin's `SystemConf` (L-10).
  - `state-units`: an empty value reads as the default; a line end becomes a second key; the default check is dead.
  - `lifted` (ASan, UBSan): `header_callback`'s heap-buffer-overflow; `led.colour` throwing; two executors reading a failure as success.
- **Read and closed:** `file://` from a media URL (the status-0 path); the server's `format` as a path (no `..` resolution, no directory to pass through); the Bluetooth and storage arguments (safe by shape); `maskSecrets`' `--key` (deliberate, #177).
- **Nothing of the never-run list ran:** no guest yet, no image build, no fetch, no keyed call, no M7 root, worktree or prep directory. The ES worktree is at the pin, its diff empty, and nothing under the distribution's `packages`, `projects` or `tools` changed.

## [Window] 22:41 to 22:50 UTC — the guest window under the 22:41 grant

- **Before the clock:**
  - the read-only preflight said `SWAP EXHAUSTED: 3MB of 8191MB free` (rc 1);
  - the grant's one `tools/build-preflight --reclaim-swap` ran at 22:42:21 UTC: rc 0, `READY`, swap 8,188 to 0 MB used, with qemu 0, compilers 0 and M7 holding nothing;
  - the image's `.sha256` checked OK; the disk was built by the rule's recipe (`gunzip`, `qemu-img convert`, `resize 16G`) and the raw intermediate removed.
- **START 22:43:36 UTC:** `generic-x64-vm run --headless --daemonize --res 640x480`. A pidfile from an earlier run existed before the boot; its new PID 4155351 was confirmed as this guest by its command line (`t21.qcow2`) before START was posted.
- **G1 to G5 ran in order** (`02` § The guest cycle). New from the image: L-21 (`system.cfg` and its seed at 0645) and L-22 (a connect with no Wi-Fi device exits 0). Confirmed on the image: L-08's argv, L-15, and both recovery ladders.
- **A misread, caught and redone:** the first image-versus-tree comparison read all six files as different because the serial lines end in CR. Both runs are kept.
- **A key name, wrong and corrected:** the first menu key was not one `vm-visual-qa` knows (the walks' guide: `ret` is START), and the frame showed the carousel.
- **G6 and G7 were not run.** Just after G5's frame, my response was cut off by an automated safety check, and I closed the window rather than run those steps without reviewing them again. The coordinator's 22:51 ruling queues G6(a) and G6(b) for a second 20-minute window behind M7's RETURN; G6(c) and G7 stay `CANNOT` for the slice.
- **RETURN 22:49:29 UTC:**
  - `vm-stop` rc 0 by the pidfile;
  - the disk retired with its path, size and sha, and removed;
  - the guest's stores restored and verified by `cmp`, and no account key ever set on it;
  - the leftover check at 0.
- **No other host action:** nothing in the window touched an M7 root, a handheld or the owner's accounts, and no QA account was used.

## [Stage C] 22:51 to 23:56 UTC — the second opinions, the grades, the leads from the seats

- **The four keyed calls, and no others** (`stage-c/keyed-calls.txt`): Astra's probe and refutation, then Argon's probe and refutation, each PASS on its provenance (`stage-c/provenance-read.py`); `04` § Second opinion has the windows and the verdicts.
- **The grades:** Astra 58 items (`stage-c/astra-grades.md`), Argon 45 (`stage-c/argon-grades.md`); `02` § Corrections and new leads from the seats holds the corrections and L-23 to L-36.
- **The host positive taken further:** `stage-c/positives/hostname-empty.py` (L-23). Its step 3 was run by hand at stage C and appended to the `.out`; it is part of the script since S1, so the script reproduces its own output.
- **`05` was not written by this session:** two of its responses were stopped by an automated safety check (23:38 and 00:20 UTC), and the coordinator wrote `05` from the lane's inputs at `14cd564486` (D-WORKFLOW-212, merged at `69a2006ed4`). Friction: Backlog #1183.

## [Stage D] 00:20 to 00:35 UTC — the lint, the audit issue, the pause

- `04` § Second opinion written; PL-23's `punch_index` question changed from Q8 to `none` with its reason (the lint's second FAIL); `tools/lint-audit-artifacts --phase pre-issue` PASS.
- The audit issue #1184, a sub-issue of #668, 26 items; `tools/box-check` 0 fail. The pause posted on #668; the ruling at 00:29 UTC with the stream brief `docs/reviews/briefs/t21-streams.md` at `e3c07a9c30`.
- **The bugs:** 19 under #668 (#1185, #1187, #1189, #1191, #1193 to #1207) and the OS scripts' four halves under #695 (#1208 to #1211), each body its `05` section copied by a script (`tools/t21-file-bugs.py`, kept from scratch at the close-out), cross-linked in pairs.

## [Stage E] 00:36 UTC onward — the streams

- **The build command:** `RAPIDJSON_INCLUDE_DIR=/workspace/tmp/m6-t21/rj/rapidjson-1.1.0/include bash tools/t21-build-tests.sh <es tree> <build dir>`, with `TMPDIR=/workspace/tmp/m6-t21/tmp`.
- **S1** (#1185, #1198, #1199), ES `ba0e82c1f`. The question on `updateVal`'s refusal was ruled at 00:36 UTC: (b), refined. Before: es-conf-tests 8 of 18 failed, es-unit-tests and es-file-tests 1 each. After: 230 cases passing in the four binaries. The host positives: `bash stage-e/s1-positives.sh <es tree> <scratch> <chksysconfig> <001-functions> <seed> <busybox> <os-release>`, the inputs those of stage C (the scripts at `8ebaf8daad` under `/workspace/tmp/m6-t21/shell/in/`, the donor's busybox and os-release under `/workspace/artifacts/m6-donor/1a0266484423/image/system/`). `stage-e/s1-before.txt`, `s1-after.txt`, `s1-checks.txt`.
- **S2** (#1197, #1189), ES `8cf52e263`. Before (at S1's tree): two SystemConfTests cases FAIL, and the reversed G-E1-04 check FAILs against S1's `AtomicFileUtil.cpp`. After: 232 cases; `kill-writer.py` PASS, 115 points; `shell-writers.py` S1 unchanged, its fix being #1208's (the OS half). `stage-e/s2-before.txt`, `s2-after.txt`, `s2-checks.txt`.
- **S3** stopped at its read by an automated safety check; posted on #668 and taken by the coordinator. Nothing was written for it.
- **S2's next load** (the coordinator's 00:51 UTC note): a written-not-recorded live file *is* published at the next load (`stage-e/s2-nextload-probe.txt`); put to the coordinator on #668 with two options.
- **S4** (#1191), ES `f7c16144d`. A new host target, es-fs-tests: `FileSystemUtil.cpp` with four doubles, built by `tools/t21-build-tests.sh` when the tree names it (the script learned it in this stream). Before: six of eight FAIL. After: 240 cases in five binaries. `HttpReq.cpp` is CANNOT on this host (no curl) and was read twice. `stage-e/s4-before.txt`, `s4-after.txt`, `s4-checks.txt`.
- **S5** (#1193), ES `94791c4ed`. Before (at S4's tree): three cases FAIL. After: 244 cases; `tools/settings-modes-test` PASS. `Settings.cpp` is compiled by no test until S8 and was read twice. `stage-e/s5-before.txt`, `s5-after.txt`, `s5-checks.txt`.
- **S3 merged** from the coordinator's `origin/coordinator/t21-s3` at `13a688804` (merge `f2561bbe4`): five binaries, 0 failed, es-unit-tests 190 (`stage-e/s3-merge.txt`). S3's records and its `02` row are the coordinator's at the hand-back.
- **S6** (#1194), ES `00669ccd9`. Before: four of seven `connectOutcome` cases FAIL. After: 249 cases; the profile-lifetime check PASS; the new sentence and its French in neither untranslated list. `GuiWifi.cpp` read twice (CANNOT here). `stage-e/s6-before.txt`, `s6-after.txt`, `s6-checks.txt`.
- **S7** (#1195, #1196, #1207), ES `8629d5d08`. New: `HttpText` (pure), `stage-e/s7-asan.cpp` and `s7-asan.sh`, and stand-in curl and SDL headers (`stage-e/fakes/`) with which `HttpReq.cpp` takes `g++ -fsyntax-only`; proven to fire on a misspelt copy. Before: two unit cases FAIL, three sanitizer reports. After: 252 cases, three clean runs. `stage-e/s7-before.txt`, `s7-after.txt`, `s7-checks.txt`.
- **S2's follow-up, the marker** (#1189, #1197), ES `eeeaa462c`, as ruled at 01:09 UTC. Before: the probe's case FAILs at S7's tree. After: 253 cases; the kill sweep PASS. The limit is stated in `02` § The streams. `stage-e/s2m-before.txt`, `s2m-after.txt`.
- **S8** (#1200), ES `80c8cbcaa`. A sixth host target, es-settings-tests, with pugixml from the recipe's source cache at the pin (the submodule's commit `61c944895e`; `PUGIXML_INCLUDE_DIR`), and `stage-e/s8-tsan.sh` for the race case. Before: three of four FAIL, seven ThreadSanitizer reports. After: 257 cases, 0 reports. The marker question was ruled (b) at 01:20 UTC; `02` says why. `stage-e/s8-before.txt`, `s8-after.txt`, `s8-checks.txt`.
- **S9** (#1201), ES `c4341c335`. `kill-writer.py` gained `--after-start`. Before: four cases FAIL; 42 of 116 kill points leave a temporary after the next start. After: 261 cases; 0 of 116. `stage-e/s9-before.txt`, `s9-after.txt`, `s9-kill-after.out`, `s9-checks.txt`.
- **S10** (#1202), ES `31b49999e`. New: `ScriptOutput` (pure), `stage-e/s10-reader.cpp` (T20's cases through it), and `stage-e/syntax-check.sh` with stand-in SDL and FreeType headers, so `ApiSystem.cpp` and the two pages take `g++ -fsyntax-only` with the build's `-DHAVE_INTL`; proven to fire on a misspelt copy. Before: four cases FAIL. After: 265 cases; every file named passes the syntax check, S1's and S6's pages included. `stage-e/s10-before.txt`, `s10-after.txt`, `s10-checks.txt`.
- **S11** (#1203), ES `eeee95265`. Before: nine checks FAIL; the first before run's stub had left out the pin's spaced base-colour branch, was completed, and the before was rerun. After: 267 cases. `stage-e/s11-before.txt`, `s11-after.txt`, `s11-checks.txt`.
- **S12** (#1206), ES `e38dcdefd`. Before: seven cases FAIL. After: 274 cases; the syntax set grew a FreeImage stand-in and SDL's events for `Scraper.cpp` and `main.cpp`, and all eight files named pass. Four sentences as proposed, with their French. `Scraper.cpp` skips the two new statuses as it skipped REQ_IO_ERROR. `stage-e/s12-before.txt`, `s12-after.txt`, `s12-checks.txt`.
- **S10's follow-up** (#1202), ES `a73ed9efc`, as ruled at 01:47 UTC: the BIOS CHECK page shows COULDN'T CHECK THE BIOS FILES RIGHT NOW. in place of its list, and the launch check with `ran` false launches without a warning and logs. `stage-e/s10b-before.txt`, `s10b-after.txt`.
- **S13** (#1205), ES `44d3c7e25`. A seventh host target, es-scraper-tests; `t21-build-tests.sh` now builds any further named test. Both Retry-After sites fixed (the brief named one). Before: nine checks FAIL. After: 277 cases. `stage-e/s13-before.txt`, `s13-after.txt`, `s13-checks.txt`.
- **A correction, 2026-10-27:** the case totals written for S2 to S13 in `02` § The streams, in this log and in the checkpoints on #668 were written without being added up, and were 2 to 53 cases high. They are recomputed from each stream's own after-log and corrected here and in `02`: S2 232, S4 240, S5 244, S6 249, S7 252, S2's marker 253, S8 257, S9 261, S10 265, S11 267, S12 274, S10's follow-up 275, S13 277 (S1's 230 was right). The per-binary lines in `stage-e/` were always the binaries' own. `tools/t21-build-tests.sh` now prints `TOTAL: N test cases in B binaries` from the binaries' summary lines, and a record quotes that line.
- **S14** (#1154, D-NET-017), ES `3ae9610b0`. Before: six checks FAIL. After: `TOTAL: 278 test cases in 7 binaries`. The listener positive is CANNOT on this host -- libcurl's runtime without its headers -- and goes to the integration window's guest walk. `stage-e/s14-before.txt`, `s14-after.txt`, `s14-checks.txt`.

## [Stage F] 2026-10-27 — Phase 7: every item at its outcome

- `05`'s gate and its `punch_index` rewritten together: 19 Resolved, 5 Deferred (PL-16 to #1204 and #1210, PL-20 #1186, PL-22 #1188, PL-23 #1190, PL-26 routed), 2 Withdrawn (PL-21 on the #1184 reading, ruled 02:12 UTC; PL-24 recorded as written). Each Resolved row names its ES commit and bug.
- `tools/lint-audit-artifacts` at the resolution phase PASS, and against #1184 PASS (`stage-f/`). #1184's 26 checkboxes ticked at their outcomes; `tools/box-check` 0 fail.
- The bugs carry `fixed-at-es` in their bodies (18 under #668, and #1154); they stay open until the pin moves on `next`.

## [Stages G and H] 2026-10-27 — the retro and the hand-back's checkers

- The retro: `docs/retros/2026-10-27-m6-es-state-and-bridge.md`, its state table computed from the logs in commit order.
- The checkers: `stage-h-checkers.txt` -- register-check, work-log-index, ceremony-check --gate, the lint twice, box-check, the unit build, the syntax check, the ES pre-push test and es-untranslated, every one rc 0.

## [Close-out] 2026-10-27 02:33 UTC — the audit complete

- Accepted by the coordinator on #668 at 02:31 UTC (the merged distribution tip `06c5c4e685`, the ES tip `3ae9610b0`); #1184 closed as completed.
- `audit-completion.json`, `tracker-completion.json` and `tracker-final-readback.json` written by `tools/write-completion.py` (T20's, its path and issue changed) from #1184's closed readback: 26 ticked, 0 open, completed 02:32:32 UTC. The readback carries no credential-shaped line (`.githooks/secret-patterns`: 0).
- `tools/lint-audit-artifacts --issue 1184` PASS; the default phase PASS; `tools/ceremony-check` accepts the marker.
- The scratch `/workspace/tmp/m6-t21/` (375M) retired after a check that no process of this session had its working directory or an open file there; `stageD/bugs.py`, which the records cite, kept first as `tools/t21-file-bugs.py`. The rapidjson copy and the build directories are reproducible from the recipe's cache and `tools/t21-build-tests.sh`.
- The pointer set idle, with the checkpoints from the window onward it had missed.
