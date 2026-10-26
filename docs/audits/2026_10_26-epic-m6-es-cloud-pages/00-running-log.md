# Running log — M6.P2 T18, EmulationStation's cloud pages, cards and text, with their unit tests (#665)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`), after T17's close-out.
- **Brief:** `docs/reviews/briefs/es-cloud-pages.md`, version 2 (`99515f83ad`). **Dispatch:** the coordinator's comment on #665, 09:29 UTC on 2026-10-26.
- **Depth:** Extended. Two seats over a trimmed, scanned packet (D-WORKFLOW-195): GPT-6 Astra at `max`, then Gemini 4 Argon at `high`, each a probe then one refutation.
  - **Exactly four keyed `tools/council/run invoke` calls**, at stage C.
  - Every other `tools/council/run` call runs with `COUNCIL_ENV_FILE=/nonexistent`; the runtime comes from `npm install --offline`, with no fetch.
- **`reviewed-at`:** the distribution's dispatch tip `cbf6d7ef83`, with **the pin `16dbac5211eea7e70db7394372033be2be7df829`** beside it: the ES worktree's HEAD, clean, on `feature/m6-es-cloud-pages-665` (r25).
- **Can this be done on the VM? Yes -- the host first, then one guest window.**
  - Every read runs on the host. So do the unit tests, built with the host's `g++` by `tools/t18-build-tests.sh`, generated from `es-app/tests/unit/CMakeLists.txt` (the host has no `cmake`).
  - `tools/es-syntax-check` cannot run here (exit 2, no build root). A fix to a GUI file has the host `g++ -fsyntax-only` pass, or its `CANNOT` with the missing header named, and its compile proof is the integration build's.
  - The GENERIC_X64 guest runs the pin's binary at 640x480, with `tools/cloud-test-backend`'s WebDAV, the eight cloud walks, `tools/vm-visual-qa` and `tools/time-to-play --vm`. The window is asked for on #665 after stage B and granted in the host file's queue, with the post contract.
  - Nothing runs on a person's device or cloud (D-QA-015).
- **What never runs here:**
  - a build, or a compiler beyond the host's for `es-app/tests/unit` and the syntax-only replay;
  - a plan generation, a fetch, or a network read beyond the four seat calls;
  - a hosted or offsite account, or a command against a handheld or a person's cloud;
  - a read of an M7 build root or an `m7-*` ES worktree, or a write in any ES worktree but the lane's;
  - a guest outside the granted window, or a keyed council call beyond the four;
  - a credential-shaped literal at rest;
  - a change under the distribution's `packages/`, `projects/` or `tools/`, or to an ES file outside the 30 at stages A to D.
- **The read filter.** Counts are taken unfiltered. A line that could carry a credential word is read through `grep -v -i -E 'key|pass|token|user|psk'` (D-QA-021) or the mask.
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t18/tmp`, `.qa-scratch/t18/` (gitignored). `/workspace` inodes were 25 % used at 09:31.
- **Proofs:** each proof in `02`'s § Proofs has one numbered proof line here, in its stage.

## [Stage A] 09:31 to 09:42 UTC — the first commands, the block, the runs, the unit tests

- **The host** at 09:31:00 UTC: the host file's last lines are M7's `GUEST RETURN` at 09:12:20 and the coordinator's acknowledgement (*"M7 GUEST RETURN ACKNOWLEDGED (09:12 ...) The host is free"*). Census: qemu 0, compilers (`cc1plus`) 0.
- **The first commands** (brief § 1):
  - the status is clean (0); the tip is `cbf6d7ef83`, on `4db784d1c0` (the coordinator's `7769e792a4` merged);
  - stacked on `8ebaf8daad` and on P1's `2174265e9c`;
  - `packages/` and `projects/` against `8ebaf8daad`: empty;
  - `tools/` against `8ebaf8daad`: `15 files changed, 2130 insertions(+), 8 deletions(-)`, P1's own files;
  - `PKG_VERSION="16dbac5211eea7e70db7394372033be2be7df829"`;
  - the ES worktree: HEAD the pin, status 0, on `feature/m6-es-cloud-pages-665`; the merge base with `upstream/master` is `bccd715707`, 725 ahead;
  - `register-check` ok.
- **The rules.** `git diff --quiet next -- .claude CLAUDE.md AGENTS.md` reports a difference, but `git log HEAD..next` over those paths is empty: the branch is 19 commits ahead of `next`, not behind.
- **The runs:** `stage-a/runs.sh`, 26 steps, each with its exit and wall time (`stage-a/out/runs.tsv`). **All exit 0.** The brief's § 2 block is copied verbatim as `stage-a/scope.py`.
- **What held** (brief § 2 and § 5):
  - 30 paths, 11,193 lines; read 29 / 11,116 (`README.md` the unread file); fork-own 30; shipped 30; c++ 23, c-header 5, cmake 1, markdown 1; 1,114 ES rows in the inventory;
  - sources 8 / 5,429 and tests 22 / 5,764; none in the merge base;
  - 221 `TEST_CASE` in 19 files, 1,665 `CHECK*` lines; `CloudTextTests.cpp` 70;
  - the seven markers at `CloudText.cpp:561-616`, 75 at `:1386`, `whyForCode` at `ThreadedCloudSync.cpp:80-98`, 0 and 9 at `CloudTransferJob.cpp:302` and `GuiCloudTransfer.cpp:289` / `:440`;
  - the job's wrapper `:636-638` with `trap '' PIPE`, the card's `:206-208` without;
  - the stamps (`STAMP_DIR :892`, `readStamps :894`, tmp + `std::rename :944-947`, the map `CloudText.cpp:186-189`);
  - `FileSystem::exists(` 0 in the eight;
  - the lifetimes at the brief's lines;
  - the why table: 38 ES rows, 38 unique; 34 script literals; 32 shared; 2 script-only (`ANOTHER CLOUD SYNC IS RUNNING`, `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK`); 6 ES-only; 17 variable emitter lines (`cloud_backup` 5, `cloud_content_restore` 5, `cloud_restore` 4, `cloud_scan` 2, `cloud_content_backup` 1);
  - the strings: 220 `_( )` occurrences; the card 58 / 50 unique, the page 80 / 67; `WIFI` 0; *back up* only as a verb, *backup* only as a noun;
  - 0 non-ASCII `//` comment lines in the 30. The 11 non-ASCII lines are `·` in string literals, except `CloudTransferJob.h:151`, a trailing comment on a member with no `_( )` near it;
  - the history: 181 non-merge commits, Max Engel 170, blitterbot 9, rasterabot 2; 2026-07-25 to 2026-10-11 (2 / 166 / 13 by month); the newest ten as the brief lists;
  - the callers outside the eight at the brief's lines; `GuiMenu.cpp` names `/usr/bin/cloud_` on 50 lines;
  - none of the five M6 build roots holds an ES build, a rapidjson copy or `ninja`; no `cmake` or `ninja` on the host;
  - `tools/es-menu-map-check --es-src <W>`: 55 screens at `16dbac521`, 31 mapped, 24 declared, **0 missing**;
  - eight cloud walks; `docs/es-menu-map.md` § Visual evidence at `:26` and § Cloud at `:231`.
- **Two deltas, one a tool difference:**
  - **The declarations:** the brief's regex prints **44 under GNU `grep -E`** (the scripts' grep) and **47 under `grep -P`**. GNU `-E` reads `\s` inside `[...]` as a backslash and an `s`, so it misses the three declarations whose return type holds a space (`CloudText.h:187`, `:529`, `:546`). The brief's 47 came from a shell whose `grep` is a function routing to an ugrep that reads `\s` in a class as whitespace: this session's interactive shell is such a shell, and gave 47 too. **47 is the count**, and r07 records both.
  - **The `exists(` control's top three** are `GuiMenu.cpp` 35, `Win32ApiSystem.cpp` 31 and `Scraper.cpp` 25 (the brief named `ApiSystem.cpp` 23 second). The figure for the eight, 0, holds.
- **Flags the brief's lines did not take:** `tools/es-untranslated` and `tools/es-menu-map-check` take `--es-src`, not a positional tree.
  - `es-untranslated` exits 0 and names only two upstream strings in `GuiMenu.cpp`, none in the eight. **Every fork string of the eight has French.**
- **The unit tests, built and run** (`tools/t18-build-tests.sh`, r20):
  - The four binaries, their sources read from `CMakeLists.txt`'s own lists, built with g++ 15.2.0 at `-std=c++17`, with the file's `-I` roots.
  - Results, 221 cases and 0 failed: `es-unit-tests` 185 cases / 4,795 assertions; `es-file-tests` 24 / 3,389; `es-conf-tests` 10 / 119; `es-file-tests-win32` 2 / 14.
  - **rapidjson** is a copy of 35 headers at `/workspace/tmp/m6-t18/rapidjson`. They were taken from `/tmp/pix642-host-controls-prep-20261022-01/inputs/include`, M7's prep, read only. Every header matches that prep's recorded sha256 in its `inputs.json` (35 of 35; `document.h` `a8c29c92…`). Its `provenance.json` names the source as the sign-in build root's toolchain sysroot `usr/include/rapidjson`, which this lane did not read.
  - The binaries are in `/workspace/tmp/m6-t18/build-stage-a`.
  - **The copy's record** (the coordinator's 09:44 read on #665: the brief's "named copy with provenance, as a read" form):
    - source directory `/tmp/pix642-host-controls-prep-20261022-01/inputs/include/rapidjson`;
    - `inputs.json` sha256 `a5ecb96872d773427397204e663bbbdd60dcf67d957f4f365d9e8216e98fe473` (read 09:44:58 UTC);
    - **no build root was read**, M6's or M7's: the sysroot the prep names is cited from its `provenance.json`, never opened.
- **The syntax check:** `ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree <W> es-app/src/CloudText.cpp` exits 2, *"no build root at /nonexistent"*. The host's `g++ -std=c++17 -fsyntax-only` over `CloudText.cpp` exits 0.
- **The window's identity literal**, chosen now (r26 and a `git log -S`): **`FOLDERS ALREADY CREATED WILL STAY. YOU CAN TRY AGAIN LATER.`**, a `_( )` literal of `GuiCloudTransfer.cpp`. It is absent from the merge base's `es-app` and `es-core`, and was added by `1272b3405` on 2026-10-08, the latest of the candidates.
- **The context read, named** (§ 2; read at stage B): `tests/app-unit/`, 19 files (10 at the top, 9 fakes, `fakes/ThreadedCloudSync.h` among them), and the eight Python harnesses under `tests/`, 986 lines.
- **Nothing of the never-run list ran.** The one compiler run was the host's `g++` for `es-app/tests/unit` and the syntax-only replay. `git diff --stat cbf6d7ef83 HEAD -- packages projects tools` is empty; the ES worktree is at the pin, clean.
- PROOF: P1, the membership: r01, r02, r03, r05.
- PROOF: P2, the pin and its base: r04.
- PROOF: P3, the history: r16.
- PROOF: P4, the callers outside the eight: r17.
- PROOF: P5, the unit tests built and run: r20.
- PROOF: P6, the branch and the removal rule: r25.

## [Stage B] 09:44 to 09:59 UTC — the eight read, the two tables generated, `02`

- **The coordinator's stage-A read** (09:44 UTC, #665): 47 is the count, with r07 recording both; the three corrections go to the brief's errata at acceptance; the rapidjson copy's record went into § Stage A above.
- **Read:**
  - the eight sources whole, in the brief's order;
  - `CloudTextTests.cpp` against the functions it calls, and the other 21 test files for subject, fixtures and the eight's functions;
  - the context: `tests/app-unit/`, 19 files, which is at the **top of the ES repository**, not `es-app/tests/` as `01` first said (corrected in this commit), and the eight harnesses;
  - the callers' lines where they decide what reaches the eight: `FileData.cpp:960-1030`, `GuiMenu.cpp:5038-5100` and `:7036-7046`, `main.cpp`'s producers;
  - `es-core/src/utils/FileSystemUtil.cpp:1429-1446` and `AtomicFileUtil.h`, for the stamp writer.
- **Two generators** under `tools/`, run at 09:55:28 and 09:55:29 UTC, both exit 0; outputs in `stage-b/`:
  - `t18-protocol-table.py`: 18 rows;
  - `t18-why-table.py`: eight counts, the fallback map and the eight wordings for 75.
  - Each was run against upstream's `651150fc88` and **exits 1**, naming its counts: the guard fires.
- **A check that could not fail, caught by its control:** the first fixture scan read `.githooks/secret-patterns` with `grep -f`. The file is a shell assignment, and the control line gave 0. Re-run with the hook's own form (`. .githooks/secret-patterns; grep -E -e "$SECRET_PATTERNS"`): the control 1, and the 22 test files 0.
- **`02-forward-audit.md`:**
  - § Coverage, 30 rows (the brief's `awk` prints 30);
  - § Context read, 21 rows covering the 19 files and the eight harnesses;
  - § The protocol and § The why table, generated and inserted between markers;
  - § The surfaces, § The lifetimes (13 rows), § The strings (219 strings: r14's 220th is a comment at `CloudText.h:527`), § The tests (22 rows), § The runs (26);
  - § The guest cycle: `CANNOT` until the window;
  - § Findings index (F-01 to F-19, and one lead outside the slice), § Positives, § Proofs (P1 to P16).
- **Not run, by the brief's compiler scope:** `tests/app-unit`'s `jobs-tests`, the only test of the job's stop races (F-19), is asked about on #665. The harnesses' subjects are `GuiMenu.cpp`'s, T26's.
- **Nothing of the never-run list ran.** No compiler ran at this stage. The ES worktree is at the pin, clean. No guest was started.
- PROOF: P7, the protocol table generated, 18 rows asserted.
- PROOF: P8, the protocol generator exits 1 against `651150fc88`.
- PROOF: P9, the why generator exits 1 against `651150fc88`.
- PROOF: P10, the why table generated, eight counts and the fallback map asserted.
- PROOF: P11, no secret-shaped literal in the 22 test files (0; control 1).
- PROOF: P12, `nextTime`, `isKnownWhy` and `isKnownUnitLabel` have no caller outside `CloudText.cpp`.
- PROOF: P13, `setFailedNote` and `setDismissedAction` have no caller; `cancellable` is never passed.
- PROOF: P14, `doing copy`/`verify`/`remove` and `DISCARDED SAVES` have no producer.
- PROOF: P15, `cancelForLaunch` runs on the interface thread.
- PROOF: P16, `writeStamp` renames an unchecked write.

## [Stage C, the window] 10:00 to 10:24 UTC — the window, `jobs-tests`, the packet's first build

- **The coordinator's reads on #665:** the window granted at 10:02 UTC; `jobs-tests` allowed (F-19); the `cloud_content_transfer` lead taken as Backlog #1140 under #1047.
- **`jobs-tests`** (`tools/t18-build-jobs-tests.sh`, 10:07:52 to 10:08:01 UTC): the host `g++` by commands generated from `tests/app-unit/CMakeLists.txt`, with ASan and UBSan, the test's own copies of the shipped sources under `/workspace/tmp/m6-t18/build-jobs-tests/under-test/`. 6 cases PASS.
- **The window** (`guest-cycle/`, START 10:06:23 and RETURN 10:23:21 UTC, both posted on #665 with census 0):
  - The image's `.sha256` OK; the backend up; guest a reimaged.
  - The identity read first (P17).
  - The first walks ran at 1280x800, `vm-pair`'s default, which my plan did not name. I stopped them by PID (3001365, 3030647 and their `vm-visual-qa` children) and stopped the guest by its pidfile (`vm-pair down`). I relaunched it on the same disk with `generic-x64-vm run --res 640x480` and `vm-pair`'s own arguments (`relaunch-640.out`); this is #1141.
  - At 640x480 five walks passed. `run-transfer-frames` exited 3 (#1141), and I stopped the run by PID (3036593, 3086676 and their children) before `run-transfer`.
  - F-08's before-frame was `CANNOT`.
  - `time-to-play` exited 0 (P20, P21).
  - `vm-pair down` and `backend down`; the leftover check all 0.
- **Retired, D-INFRA-022:** `/workspace/tmp/m6-t18/vm-pair/vm-a.qcow2`, 2,334,785,536 bytes, sha256 `c24599965c6331f9d4d1bf88636a4d225ed6861fee503ab24c130957880514a9`, removed with its directory (the run's QA key and firmware vars with it). What is kept:
  - the cited frames, in `guest-cycle/frames/`;
  - the walks' and `time-to-play`'s other frames under `/workspace/tmp/m6-t18/`, until the hand-back;
  - `time-to-play`'s saved copy of the guest's `rclone.conf` (the QA endpoint's synthetic config, mode 600, never read). It is retired with the scratch.
- **The packet's first build** (`stage-c/packet.py`, before the window's results): 31 sections and 364 KB at first, trimmed to 38 sections and 337 KB by moving the headers to excerpts and narrowing the register rows. Six `review` hits were read by shape (an outcome token compared with a word; a `bool` initialised `false`; D-QA-021's prose row) and dispositioned by name in `packet.py`. **No keyed call yet.**
- **Filed:** #1141 (`vm-pair` has no resolution, and the transfer walks fail at 640x480).
- PROOF: P17, the binary carries the pin's strings.
- PROOF: P18, `jobs-tests` 6 PASS.
- PROOF: P19, `SNES 0 FILES` at 640x480.
- PROOF: P20, the exit sync 1.58 s, completed 3 of 3.
- PROOF: P21, the card at 640x480.

## [Stage C, the seats] 10:24 to 11:09 UTC — four keyed calls, 87 items graded, the pre-issue lint

- **The runtime:** `npm install --offline` in `tools/council/` (`node_modules` is gitignored). `esbuild`'s install script was left unapproved, and the runner worked without it. `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`.
- **The packet:** `second-opinions/packet.md`, 347,592 bytes, sha256 `e92cc4dc…`; the scan and the trims are in `04` § Second opinion. `review-plan.json` was written at 10:26Z, before the first call.
- **The four keyed calls, and no others** (`/workspace/tmp/m6-t18/keyed-calls.txt`; options `--max-retries 1 --per-attempt-timeout-ms 1800000 --total-timeout-ms 2400000` on the refutations):
  1. Astra's probe, 10:26:38 to 10:26:57 UTC: PASS, `openai/gpt-6-astra` by OpenAI.
  2. Astra's refutation, 10:27:06 to 10:47:10 UTC: one attempt, `finish=stop`, 42 items.
  3. Argon's probe, 10:49:58 to 10:50:05 UTC: PASS, `google/gemini-4-argon` by Google.
  4. Argon's refutation, 10:50:15 to 11:06:02 UTC. Its first attempt returned empty content (`finish=error`, 396 s); the one allowed retry, within the same call, returned 45 items with `finish=stop`.
- **The provenance, read directly** (`stage-c/provenance-read.py` into `provenance-read.txt`): all four `verification=PASS`, served model and provider the seat's, each output's sha256 matching `output_file_sha256`, `facilitator_version council-facilitator@1.14.1-pixelelated.2`. `tools/council/run summary`, with `COUNCIL_ENV_FILE=/nonexistent`, refuses without a council run directory (`--run-dir is required`), as for T17.
- **The grades** (`04` § Second opinion; `stage-c/astra-grades.md` and `argon-grades.md`; the re-reads in `stage-c/rereads/`):
  - Astra: 40 accepted, 1 in part, 1 plausible, 0 rejected.
  - Argon: 45 accepted, 0 rejected.
  - New and confirmed: A-33/A-34 with R-11/R-39/R-41 (stops and cancels against an ending run), A-36 (the full-stop row), A-37 (a part's early why misplaced), A-38/R-40 (a 9 after a failed part, latent), A-39 (`backuptool backup`'s output discarded, T26's), R-42 (a content transfer cut by the network reads COULDN'T FINISH with no why), and R-43 (the job's dead `mWhy`).
  - The lane's claims the seats refuted, corrected in `02` and `04` in place, each saying so:
    - the fallback map omitted codes 6 and 10 (A-15; the generator now lists seven groups and asserts 2 differences);
    - "every row is fitted" (A-40);
    - the 2 s budget compared with D-CLOUD-119's 3 s (A-11);
    - "the second half is not a protocol line" (A-4).
- **`05`:** 23 items; seven `bug`s proposed, all Low (PL-01 to PL-04, PL-18, PL-20, PL-22), and two more proposed Low by the seats (PL-05, PL-15).
- **The lint:** `tools/lint-audit-artifacts docs/audits/2026_10_26-epic-m6-es-cloud-pages --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)`.
- **Nothing of the never-run list ran.** No keyed call beyond the four. No guest outside the window. The ES worktree is at the pin, clean.
