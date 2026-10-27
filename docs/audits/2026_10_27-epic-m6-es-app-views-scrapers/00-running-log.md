# Running log — M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

- **Executor:** Opus 5.5 at high effort, the session `m6-t5-build-engine` (the dispatch comment on #679, 15:46 UTC on 2026-10-27, comment 6446520036).
- **Depth:** Independent -- one seat, GPT-6 Astra at `max`: a probe and one refutation, exactly two keyed invokes, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`.
- **The brief:** `docs/reviews/briefs/es-app-views-scrapers.md` at `85307da3b3` (version 2), byte-equal to the tree's copy (`git diff --quiet 85307da3b3 HEAD -- <brief>`). #679's body carries its § 7 checkboxes; where the two differ the body wins.
- **reviewed-at:** `603b358a14`, the distribution worktree's HEAD at dispatch (the pointer's seeding; the dispatch merge `121d0180f0` of the coordinator's `42cb00860c`).
- **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`. The ES worktree `feature/m6-es-app-views-scrapers-679` is at the pin and clean.
- **Can this be done on the VM?** Yes. The host goes first: every read, count and table, and the unit cases for the pure leads built by the lane's script. Then one guest window, asked for on #679 at stage B's end with its plan and bound (§ 5 item 2: 35 minutes proposed plus 5 of grace), granted on #679 and in the shared host file's queue. A no-NIC guest cannot show any scraper's success path; G-07 (ArcadeDB against a host stub) is `CANNOT` without host port 80.
- **The rules followed:** this worktree's `.claude`, `CLAUDE.md` and `AGENTS.md` differ from local `next` (`8ebaf8daad`) because they carry the coordinator's branch, which is newer than `next` (`git diff --stat next -- .claude CLAUDE.md AGENTS.md`: 10 files, 195 insertions, 6 deletions). The session's own rules were loaded from `m6-build-engine-652`'s worktree; where a rule matters here, its copy in this worktree is the one read.

## [Stage A] 15:47 to 15:52 UTC — the first commands, the block, the runs, the context

- **The host at dispatch** (15:48:49 UTC): qemu 0, compilers 0 (`pgrep -c -f '^[^ ]*qemu-system'`, `pgrep -c -f '^[^ ]*(cc1plus|cc1)( |$)'`; the pattern seen to fire on a `sleep`), `/workspace` inodes 26% used. `/tmp/m7-m6-host-coordination-20261023.txt` ends with the coordinator's `T31 RETURN 12:45:31 ACKNOWLEDGED` (the disk retired; census qemu 0, compilers 0); nobody holds the host, and no guest starts before a grant on #679.
- **Mine, corrected before use:** the first census line used `pgrep -c -x qemu-system-x86_64`, whose name is longer than the 15 characters `-x` can match, so its 0 could not have been anything else; it was retaken with `-f` and a pattern seen to fire.
- **The first commands (§ 1)** (`stage-a/first-commands.sh`, its output `.out`, 15:47:18Z), all as the brief expects: stacked on `8ebaf8daad`; no change under `packages` or `projects` since it; `651150fc88` present locally; the ES worktree at the pin, 0 changes; `cada856d86` the merge base with `rocknix/master` (`f6c542872e`); T21's ES tip `3ae9610b0`; T21's punch list reachable, 26 items; `register-ok`; the host file's tail. The worktree's status read 1 only because this run's own audit folder was untracked at that moment.
- **The membership block (§ 2)** (`stage-a/membership.sh`, `.out`, rc 0): `selects 1 paths 42 lines 17311 {'shipped': 42} {'upstream-carried': 36, 'fork-own': 6}`; 20 `c++`, 22 `c-header`; 4,005 lines on the inventory's `fork-own` tier; `.qa-scratch/t32/paths.txt` 42 lines; `wc -l` 17,306 and `grep -c` 17,311; every path at both bases (42, 42); 6 files, 168 added, 46 removed, against each base.
- **The runs (§ 5)** (`stage-a/runs.sh`, `.out`, rc 0, 2 s wall; the three stage-C runs left out, as the brief marks them): every figure as the brief expects but one, among them:
  - the scope 46 / 4 / 42; scrapers 14, services 5, views 23 (gamelist 18); 20 `.cpp`, 22 `.h`;
  - the bases, `rocknix/master` 14 commits past `cada856d86`, 725 commits from `bccd715707` to the pin, 1 from `bccd715707` to `cada856d86`;
  - the fork's six `M` rows, 168 / 46 against both bases, 0 fork-added; upstream's 0 commits and 0 numstat rows on the slice; the tree hashes `cd0f559cb1 2f14b69046 2ffe2cc4cf` at `bccd715707`, `cada856d86` and `rocknix/master`, `31078e99df 1e39292413 2ffe2cc4cf` at the pin;
  - T21's six deltas (`Scraper.cpp` 28/8, `Scraper.h` 5/0, `ScraperReplies.cpp` 51/0, `ScraperReplies.h` 22/0; outside the 42, `ScreenScraper.cpp` 17/16 and `ViewController.cpp` 8/2) and its three commits on `Scraper.cpp`, `3ae9610b0 44d3c7e25 e38dcdefd`;
  - the fork's commits per file 2 / 1 / 1 / 5 / 1 / 4, 10 non-merge, 11 with `370ebe416`;
  - `_("` 58 lines in 9 files, 70 occurrences; `new Gui` 19 in 5 files, `GuiMsgBox` 8; `std::thread` 13 in 5; `new std::thread` at `ThreadedScraper.cpp:53` and `HttpServerThread.cpp:74`, `delete this` at `ThreadedScraper.cpp:241`; `mInstance` 9 lines; `.detach(` 0; `postToUiThread(` 13 in 3;
  - `HttpReq` 83 lines in 14 files, 95 occurrences; `new HttpReq(` at `GamesDBJSONScraperResources.cpp:153` and `Scraper.cpp:267 302 332 564 567 596`; 0 lines setting a timeout or `stallTimeout`;
  - the success-reads `214 ... 688`, `IsObject` at `448 607`, IGDB's `return false;` at `144 164 230 324 331`;
  - `exists(` 49 lines in 6 files, 50 occurrences, 0 uncached; DetailedContainer's 19 lines as listed;
  - process starts 0; `std::stoi(` 3 in 1, `std::stoul(` 0, `atoi(` 0, `toInteger(` 6 in 5;
  - `::getHelpPrompts(` defined in `SystemView.cpp` and `ISimpleGameListView.cpp` only; the five `getName()` defaults; `_moveCursorInRange` at the ten lines;
  - the T21-class uses 51 lines in 14 files; the macro names at the lines § 1 gives, cut to file, line and name;
  - 0 files with a non-ASCII comment, 0 adjacent; the harness sweep prints no basename; 15 `.py`, 19 `*Tests.cpp`;
  - the French: L218/219 and L233/234 as expected, L115's msgid with L116's empty `msgstr`; `es-untranslated` 706 / 706 / 0 against `bccd715707` and 703 / 703 / 0 against `cada856d86`, rc 0 each;
  - `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (rc 0); `:135` the one view-style line; the map 989 lines;
  - `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2; plain `g++` on `ThreadedScraper.cpp`: `es-core/src/HttpReq.h:5:10: fatal error: curl/curl.h: No such file or directory` rc 1.
- **The one difference, a count in the brief:** `atol(` reads `TOTAL 2 in 2 files` where § 5 expects 1 in 1. The second site is `DetailedContainer.cpp:1049`, `secondsToString(atol(file->getMetadata(MetaDataId::GameTime)...))` -- the detailed view's play-time display, the same parse 3.32 cites at `GameNameFormatter.cpp:171`. Both are 3.32's.
- **The stand-in syntax check** (`stage-a/syntax-check.sh` and its 13 fakes, T21's, read by `git show` from `origin/feature/m6-es-state-and-bridge-668`; `stage-a/syntax-check.out`): rc 0 on `Scraper.cpp` as T21 recorded, and on the other six scrapers' `.cpp` files and `GameNameFormatter.cpp`. pugixml from the pin's extracted `external` (its `pugixml/src` by `CPATH`); rapidjson 1.1.0 from `/workspace/cache/rocknix-sources/rapidjson/rapidjson-1.1.0.tar.gz`, its sha matching the recipe's `PKG_SHA256`, with the recipe's four patches, under `/workspace/tmp/m6-t32/rj/`. It checks each file's own C++; it proves nothing about curl or SDL.
- **The removal check** (`stage-a/removal-check.out`): empty against `603b358a14` and against `121d0180f0`; the literal `TIPHASH` fails with `fatal: bad revision`; the ES diff against the pin empty.
- **The callers** (`stage-a/callers.out`): 47 include lines of the slice's 22 headers from 23 files outside the 42 -- the figure § 5's stage-C include script expects; `UIModeController.h` 10, `IGameListView.h` 9, `ThreadedScraper.h` 9, `Scraper.h` 8.
- **The history** (`stage-a/history.out`): the fork's ten commits on the slice and the merge `370ebe416`.
- **Not run at stage A:** the include graph and the unit build (§ 5's two stage-C runs; their scripts are written at stage C).

## [Stage B] 15:53 to 16:06 UTC — 02 with its sections, the generators, the window plan

- **`02-forward-audit.md`**, composed by `python3 -I tools/t32-02.py <A> <W> 16dbac5211 .qa-scratch/t32/paths.txt` from `stage-b/02-template.md`: § Coverage 42 rows (fork-modified 6, upstream-carried 36, fork-added 0; inventory 6 / 36), § The leads (L-01 to L-21 and the floor's 35), the six generated tables, § The words, § The structure, § The merge debt, § The runs, and the stage-C/D/E headings.
- **The generators** under `tools/` (`t32lib.py`, T31's reader, renamed): `t32-views.py` 6 views, 2 help bars; `t32-scrapers.py` 5 scrapers, 3 under a build macro by name; `t32-services.py` 27 registrations over 25 patterns; `t32-reads.py` 49 lines, 50 calls, 0 uncached; `t32-bounds.py` 9 constructions, 0 bounded; `t32-words.py` 57 lines, 69 calls, 50 msgids, 0 without French. Each was seen to exit 1 on a constructed drift (`stage-b/generators.txt`: 8 drifts rc 1, 7 runs rc 0).
- **Mine, caught by first runs:** `t32-views.py` flagged `SystemView` through an operator-precedence slip and counted `ViewController`'s help bar (T2's file); both fixed before use. `t32-words.py`'s first count, one line short of the brief's, was the generator right: the brief's 58 / 70 / 51 count a comment, `ISimpleGameListView.cpp:905`'s `// _("Parent folder")`.
- **New leads from the read:** L-18 (HfsDB's and IGDB's token requests on the stack, ended by `request.wait()` with only the connect bound), L-19 (`POST /launch` walks the library on the pool thread and posts a raw `FileData*` once per match), L-20 (`/isIdle` asks neither a cloud sync nor the proxy; `/reloadgames` waits for nothing), L-21 (`quitES` on the pool thread). Inherited, not a lead: the media retry's lost `Referer` at `Scraper.cpp:596`, fixed on T21's tip (`mOptions` at its `:611`).
- **Corrections to the brief, counts only:** `atol(` 2 in 2 files; the services 25 patterns over 27 registrations (16 plain strings); 9 `HttpReq` constructions (7 `new`, 2 on the stack); 57 code lines, 69 calls and 50 msgids of `_(`; po L116's `msgstr ""` continues at L117, so L-11's empty-French half is withdrawn and its dialog half stands.
- **The window plan** (`stage-b/window-plan.md`): 35 minutes plus 5 of grace, G-01 to G-11 as § 5 names them; G-07 `CANNOT` (host port 80 is privileged: `ip_unprivileged_port_start` 1024) and G-10 `CANNOT`; L-14's N set at 100 seeded screenshots against a list of 10.
- **§ 3's reads still owed before stage D, said so:** the blindspots (item 4), the other audits' cited lines (item 8), the issues' states (item 9) and `docs/vm-qa-log.md:9-18` (item 10). Read for this stage: the slice's code behind each table, `FileSystemUtil.cpp`'s cache (T21's, read), `HttpReq.{h,cpp}`'s options and `wait()`, `DisplayAspect.cpp:99-131`, `tools/vm-walks/manager.steps`.

## [Window] 16:07 to 16:22 UTC — the guest, granted on #679

- **Granted** at 16:07 UTC (comment 6447015977), the host free (swap 1,402 of 8,191 MiB: no reclaim). **START 16:08:36 UTC** (comment 6447041699); **RETURN 16:22:34 UTC** (comment 6447364690), each with its census and a line in the shared host file. The guest was stopped by `tools/vm-stop` on its pidfile at 16:22:12 (rc 0), 14 minutes into the 35.
- **Proved on the image** (M7's composition: every frame `image`): 3.13 and L-07 (offline ArcadeDB reads COMPLETED, 9 scraped, nothing fetched); L-08 with its control (a picture written from outside ES is not drawn until a restart); 3.16's remainder as the player meets it (IGDB with no client id: NO GAMES FIT THAT CRITERIA., EN and FR); G-08's four answers; G-04's clean wrap. **Not reached:** L-14 (the shipped theme has no grid view). **Read at C before called anything:** G-03's cursor that stayed on Alpha, and the French bar's missing SAVE STATES. **CANNOT:** G-07, G-10, the 403, the l2/r2 keys.
- **The disk retired:** `t32.qcow2`, 2,312,372,224 bytes, sha256 `a3a152ce…0627d`, removed (`guest-cycle/retired.txt`); qemu 0, compilers 0.
- **Mine:** three void passes, each redone with a frame (a `StartupSystem` named `screenshots` where the system is `imageviewer`; a `ret` that reached the list; a `set_setting` without `/etc/profile`).
- **Nothing else ran:** no image build, no fetch, no handheld, no account, no council call.

## [Stage C] 16:24 UTC onward — the host proofs, the analysis, the seat

- The coordinator's instruction (16:24 UTC): stage C whole, then 05 and the audit issue, ending on the stage-D pause post. The order and its state are in the pointer's § Current focus.
- **Correction to the RETURN post (16:22 UTC), mine:** G-06's NO GAMES FIT THAT CRITERIA. is not 3.16's remainder. `IGDBScraper::isSupportedPlatform` (`:221-230`) reads only the platform map, and it has `GAME_BOY` (`:65`). SCRAPER had opened with ArcadeDB (left set by G-05's run), which takes no gb, so the systems list was empty, and moving SCRAPE FROM to IGDB did not rebuild it: T31's PL-21 (#1254) on the image. The INVALID CREDENTIALS box was not reached. 02 § The guest cycle and the post on #679 are corrected.
- **16:36 UTC, the six FAIL-at-pin proofs** (`stage-c/runs.txt`; each FAIL at the pin, then its control rc 0):
  - 3.27 `l327-cursor-range.py`: 25 of 312 cases out of range. All 25 are congruent mod the size, so a wrapping carousel hides them (G-04). The other non-congruent 37 are the forward fast move on 3 to 9 systems, a no-op by `count >= sz`.
  - 3.31 `l331-grid-image.py`: IMAGE with no image returns "", not the thumbnail. History: the early return from 8f30c244c (2019), kept as context by 4371e3b7d (2021), which added IMAGE to the fallback below it. Intent is ambiguous: a stream question.
  - 3.32 `l332-year-and-time.py`: no year under RELEASEDATE_DESCENDING; 90000 s reads [01:00:00]. **Correction:** DetailedContainer.cpp:1049 does not wrap (secondsToString folds the day: "25 h"). 02's "both atol sites" is now one.
  - 3.10 `l310-boxart-shape.py`: the shipped build has NDEBUG (config/functions' ndebug flag; ES's PKG_BUILD_FLAGS "-gold"), so the rapidjson assertion is compiled out. `"boxart": "x"` is a **SEGV**, under ASan and without it (rc -11). [], [1,2], data [] and root [] violate preconditions without a crash. Reach: GAMESDB_APIKEY only.
  - 3.13 `l313-request-outcome.py`: IO error, 429 with retries spent, and 429 with a long Retry-After where retryOn249 is false all end ASYNC_DONE with code 200. 404 DONE and 403 ERROR are right. The reader (ThreadedScraper.cpp:157-173) counts a non-fatal error and goes on, so the 2020 "Secure requests" intent survives the fix.
  - 3.16 `l316-igdb-contract.py`: process() returns false for [], {} and a parse error, against the contract written above it. Today the return is dropped (3.13), so it is a trap for 3.13's fix.
  - **L-22 (new):** IGDB's and HfsDB's ensureToken read HasMember before IsObject and GetString before IsString. A body of `{"access_token": 5}` is a **SEGV** (rc -11 plain). IGDB is compiled in every build.
- **16:38 UTC, L-02** (`l02-stop-after-finish.py`). The window is widened synthetically: the finishing block's LOG starts stop() and waits 50 ms; named in the docstring. At the pin it is a **heap-use-after-free** in stop() (`:333` writing through mInstance after `delete this` at `:238`). Under `--plain`, finished 1, cancelled 1: SKIPPED - YOU CANCELLED IT over a completed run. The control (stop() under the mutex, returning when finished) gives rc 0.
  - **L-23 (new, minor):** run() erases each ScraperThread without a delete (`:218`, 717e7d8c3), and mHandle is never joined or freed, so every run leaks them.
- **16:52 UTC, the rest of stage C before the seat:**
  - **L-16 and L-18 read.** L-16's free-then-read is inside `reloadCollection` (T33's). L-18's token fetch runs on the interface thread at a batch's start and in three manual paths.
  - **The include graph:** 47 lines from 23 files; es-core edges 143 of 410; seen to exit 1 on a drift.
  - **`httplib.h`** is the 2020 v0.7 series. L-24 is its unbounded body (CVE-2025-46728's class). CVE-2026-45372's mechanism is absent. One web search, dated in 02.
  - **§ 3 items 4, 8, 9 and 10** are read; the issue states are as the brief gives them.
  - **The floor's 27**, read by a read-only subagent and checked per `stage-c/floor.md` § Verification. The two that matter most are 3.15 (a null dereference on SCRAPE NOW for an unregistered saved scraper) and 3.19 (G-05's ten games read 9). ScreenScraper's rate-limit `false` is dropped at `:337`.
  - **03 and 04** are written before the seat.
  - **The packet builder and the ask** are in `stage-c/`.
  - **Next:** build the packet (scan and dispositions); the two keyed calls; the pre-issue lint; then 05, the issue, the bugs and the stage-D post.
- **The packet** (`stage-c/packet.py`, T31's adapted): 101 sections, 433,943 bytes. The forbidden-terms check found 0 sections with hits and was proven to run on a clean line. SECRET_PATTERNS found 0 lines and was proven to fire on a run-time fake. The first build stopped on 8 credential-word hits for review; each was read through the mask and dispositioned by `(file, line)` as code: the `apikey=` query prefix joined to a call (GamesDB `:201`, `:570`), `mTokenDate` (HfsDB `:222`, IGDB `:177`) and ``mPassKeyCounter` (UIModeController `:72`, `:75`). The second build had 0 for review. Sent: 6,240 of 17,311 slice lines, the six fork-modified files whole, and `httplib.h` by its cited ranges. `astra-brief.md` is byte-identical to `packet.md`.
- **The runtime:** `npm install --offline` in `tools/council/`. A keyless check (`COUNCIL_ENV_FILE=/nonexistent tools/council/run efforts`) printed OK.
- **Keyed call 1 of 2,** the probe: 16:53:56 to 16:54:10 UTC, rc 0. Served `openai/gpt-6-astra` by OpenAI at `max`, with identity, effort and provider verification PASS. The reply was `READY unknown` (13 bytes).
- **Keyed call 2 of 2,** the refutation, started 16:54 UTC in the background. Its exit writes `/workspace/tmp/m6-t32/refutation.rc`, and a harness waiter on that file delivers the result.
- **Keyed call 2 of 2,** the refutation: 16:54:20 to 17:15:50 UTC, rc 0. Served `openai/gpt-6-astra` by OpenAI at `max`, with identity, effort and provider verification PASS. 137,102 prompt tokens and 44,178 completion tokens, 34,731 of them reasoning. **Exactly two keyed invokes, and no others.** The harness waiter delivered its end at 17:15:55 UTC.
- **The grades** (`stage-c/astra-grades.md`): 40 items, 40 accepted, counted by `awk`. EP-33 and EP-35 were re-read before grading; EP-34 is unproved; EP-40 is #1154.
  - The seat corrected five sentences of mine, each fixed in place: G-05 is not L-07's positive (EP-4); L-02 needs no hook (EP-6); L-22's lines and prerequisites (EP-10); two rescan callers do delete first (EP-28); G-09 is a picture, not a manual (EP-29).
  - New leads L-25 to L-29 in 02 § Corrections and new leads from the seat.
- **05:** 20 items (3 High, 5 Medium, 12 Low); ten `bug`s proposed, to be filed after the ruling as on #678. `tools/lint-audit-artifacts --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)` at 17:19 UTC.
- **Stage D, 17:20 UTC:** the audit issue #1257 was filed from `05` by `tools/t32-issue-body.py` and attached as a sub-issue of #679. `tools/box-check --issue 1257`: 20 open checkboxes, 0 fail. The ten bugs wait for the ruling. Next: the stage-D pause post on #679.
- **The stage-D pause post** on #679 (comment 6448662059, 17:20 UTC): the 20 items, and four questions (the ten bugs; PL-06, PL-09 and PL-11's `/isIdle`; the streams with two design calls; G-03 and the French bar). Waiting for the ruling.
- **The stage-D ruling, 17:26 UTC** (#679 comment 6448695986, 17:22 UTC), carried out:
  - **Twelve bugs filed with their code traces** by `tools/t32-file-bugs.py`: #1258 PL-01, #1259 PL-02, #1260 PL-03, #1261 PL-04, #1262 PL-05, #1263 PL-07, #1264 PL-08, #1265 PL-10, #1266 PL-17, #1267 PL-18, #1268 PL-21, #1269 PL-22. Each passes `tools/box-check --issue N` with 0 fail. PL-02's heading was shortened for GitHub's 256-character title.
  - **PL-11 split** into PL-21 (`/isIdle`) and PL-22 (`/launch`); 05 now holds 22 items.
  - **Recorded:** PL-06 and PL-09, with #585 lines.
  - **Carried as observations:** G-03 (PL-13) and the French bar (PL-10).
  - The streams S1 to S6 are recorded in each item's disposition. The stream brief is the coordinator's.

## Stage E (17:43 UTC onward) -- the streams, under `docs/reviews/briefs/t32-streams.md` at `1010359737`

- **Commands:** `stage-e/env.sh` holds the paths. Each stream's command is in its `sN-before.txt` and `sN-after.txt`.
- **At the start:** `TOTAL: 221 test cases in 4 binaries` (`s0-build-pin.txt`). The stand-in passes 12 of 13 sources, with `SystemView.cpp` `CANNOT` on `SDLK_r` (`s0-syntax-pin.txt`).
- **S1, 17:51 UTC:** ES `e85735b0b`, pushed to pixelelated/emulationstation.
  - `l02` was rewritten to four cases over the extracted `Process`, `run`, `stop`, `start` and destructor. The fake was completed for the fixed shape (`mWorker`, atomic `mExitCode`, and a `pushGui` that deletes, since the window owns what is pushed). EP-34's hook is named in the harness.
  - Before: every case FAILs.
  - After: every case rc 0, also under `--plain`, and cancel five times. `--control` is `CANNOT` against the fix.
  - Checks: the stand-in rc 0 on four sources; non-ASCII 0; `TOTAL: 221 test cases in 4 binaries`.
  - `main.cpp` was read: `stop()` at `:1332` follows `AppWindow::closing()` and precedes the window's teardown, so a joining `stop()` needs no added call and nothing is named under merge debt.
  - Time to play: off the launch path.
  - The ES pre-push-test PASS.
- **S2, 18:03 UTC:** ES `bf3e8e2bd`, pushed.
  - **Before** (S1's tip): `l313` 10 FAIL; `l316`'s 3.16 half returns 0; `s2-scrapers.py` 6 FAIL; `t32-bounds.py` `bounded=0`.
  - **After:** every positive passes, `bounded=9`, and `l02` is still rc 0.
  - **Fixtures completed** (D-WORKFLOW-211): `l316`'s fakes take S2's `status()`, the bounds and `mTokenUnreachable`; `l02`'s fake takes the two class counters, and its startup case waits for `finished`. `l313` was rewritten to a request sequence with the dependency, the retry and five media cases; `--control` is `CANNOT` against the fix.
  - **The generator** `t32-bounds.py` is keyed by order and reads `bounded` from the options passed (D-WORKFLOW-210; `generators.txt`).
  - **PL-04's second half:** `stage-e/s2-guiscraperstart.patch` applies to T31's `2fa6b5f73`, and the stand-in shows the same T31 error with it and without it.
  - **Words:** `YOU'RE NOT ONLINE.` reuses the catalog's L4386; `THE SCRAPER IS BUSY RIGHT NOW.` is added with `LE SCRAPEUR EST OCCUPÉ POUR L’INSTANT.`; `es-untranslated`: 0 without French.
  - **Checks:** the stand-in passes 12 of 13 (`SystemView.cpp` `CANNOT` as at the pin); non-ASCII 0; `TOTAL: 221 test cases in 4 binaries`.
  - **Choices, put to the coordinator in the #679 line:**
    - a dependency's 404 keeps the primary's data and is logged, not counted (the ruling listed it as a request failure; counting it would discard the game's text, which EP-1 forbids);
    - media, rename and resize errors are counted in `errors` (COULDN'T FINISH) with no class why on line 4, since only offline and busy have a sentence;
    - the manual scrape's token failure (EP-36's manual half) is unchanged, because the synchronous paths that would have to catch it are `ScraperSearchComponent.cpp`'s (T33's).
  - **Collisions named:** `Scraper.cpp` against T21's `3ae9610b0` (the `:596` retry, now `:644`; T21 keeps `mRequestUrl`/`mOptions` there), `44d3c7e25` (both `Retry-After` reads) and `e38dcdefd`; `GuiScraperRun.cpp` against T31's `2fa6b5f73` (unchanged here: the contract kept).
  - **Time to play:** off the launch path.
- **S3, 18:09 UTC:** ES `0404e76cc`, pushed.
  - **The doctest came first:** `ScraperJsonTests.cpp` was listed in `es-unit-tests` before `ScraperJson.h` existed, and the build failed.
  - **Harnesses:** `l310` takes a root string; `stage-c/s3-images.py` (new) extracts `processGame` and its two helpers for the images JSON and `:415`; `l316` takes `--hfs-only` to measure HfsDB apart (EP-10), so `t32extract.run` takes `args`.
  - **Before:** every case FAILs, the malformed shapes as SEGVs.
  - **After:** every case rc 0 with 0 violations, also under `--plain`.
  - **Fixture completions** (D-WORKFLOW-211): the three harnesses include `scrapers/ScraperJson.h` from the tree they read, when the extract uses it.
  - **`:415` re-read, as the brief asked:** `getStringOrThrow(boxart["base_url"], "thumb")` carries neither `HasMember` nor `GetString` itself. The helper now checks the container, and `process` checks `base_url` is an object.
  - **Checks:** the stand-in passes 12 of 13 (`SystemView.cpp` `CANNOT`); non-ASCII 0; `TOTAL: 225 test cases in 4 binaries`.
  - **#1154 (PL-20):** these parsers are a consumer of peer verification. The note is in this record, and the comment on #1154 is the coordinator's.
  - **Time to play:** off the launch path.
- **S4, 18:15 UTC:** ES `1655e2f4c`, pushed.
  - **Harness:** `stage-c/s4-views.py` (new) covers the placeholder and the scraper's reads. Its fake view was given the real destructor's delete (`ISimpleGameListView.cpp:63-69`) after the first after-run reported the fake's own leak, and S3's tip was rerun with it: both cases still FAIL.
  - **Before:** FAIL throughout.
  - **After:** rc 0 throughout; `t32-reads.py` `34 uncached`, its revision recorded in `generators.txt`.
  - **Scope:** `Scraper.cpp`'s `getSaveAsPath` directory check (the pin's `:808`) was changed by the sweep and put back: ES writes that directory, and the brief's 24 do not name it.
  - **The picture is es-core's** (ruling 7): `TextureData.cpp:331`, `:339`, `:410`; #1263's picture checkbox stays open.
  - **Checks:** the stand-in passes 12 of 13. `SystemView.cpp` is `CANNOT` at the same `SDLK_r`, now `:471`; the edited `:231-238` come before it and were read twice. Non-ASCII 0; `es-untranslated` 705/705; `TOTAL: 225 test cases in 4 binaries`.
  - `t32-words.py` now reads 59 lines, 75 calls and 53 msgids, every one with French: S2's two sentences, and S4's dialog and its `OK`.
  - **Time to play:** off the launch path.
- **S5, 18:16 UTC:** `docs/es-menu-map.md` § Game list views, paired with S4's `1655e2f4c`. Before and after, the checker reads `0 missing`; the views carry no title, which is its blind spot. The grep moved from 0 lines to the section's.
  - **One correction to the brief:** the carousel's fast move is a shoulder-button input in `SystemView` (`:282-334`, `:406-413`), not a VIEW OPTIONS row. The map says so, and the letter jump is the row.
  - Time to play: a document.
- **S6, 18:19 UTC:** ES `e594e46e3`, pushed.
  - **Harness:** `stage-c/s6-api.py` (new) extracts `/isIdle`'s predicate and `/launch`'s body as written.
  - **Before** (S4's tip): `[ true ]` under each of the four, and two posts holding raw pointers, a use-after-free after the rebuild.
  - **After:** rc 0.
  - **The brief's premise was wrong:** `ProxyCards::sendRunning()` and `topUpRunning()` are free functions of a namespace, not instance methods. So no accessor was added and `ProxyCards.*` is unchanged; the reads are an atomic and an uncached file read, safe off the interface thread.
  - **Time to play:** the lookup by path moves from the pool thread to the interface thread, before the launch: one walk of the library's games. The integration's `time-to-play` cell says what it costs against the accepted baseline.
  - **Checks:** the stand-in passes 12 of 13 (`HttpServerThread.cpp` rc 0); non-ASCII 0; `TOTAL: 225 test cases in 4 binaries`.
