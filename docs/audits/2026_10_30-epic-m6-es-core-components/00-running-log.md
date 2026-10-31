# T34 (#681) running log: EmulationStation's core components

- **Model:** Opus 5.5 (`claude-opus-5-5`), high effort, the T3 session (`m6-t3-emulators`).
- **reviewed-at:** distribution `dff4fbd61d` (the lane tip; the dispatch's merge `00d490e654`, the coordinator's `200a9a032d` merged), with the ES pin `16dbac5211eea7e70db7394372033be2be7df829` beside it.
- **Host file** `/workspace/tmp/m7-m6-host-coordination.txt`, read at 2026-10-30T09:54:55Z (49 lines). Its last entry (09:26) queues M7's TLS proof windows and says T34's window waits behind all of M7's. **Census** at 09:55:01 UTC: qemu 0, compilers 0.

## [Stage A] 09:56 UTC 2026-10-30 — the pointer's keys, the first commands, the membership block, the § 5 runs; stopped at the usage limit

- **The pointer's eleven keys** were read against the brief's § 10 table before any command. All are present, and none names T33 or carries a seeding-error phrase. Two slips, neither a predecessor naming:
  - The brief's § 9 placeholder grep prints **1** on the pointer, not the dispatch's 0. The one match is the pointer's own line 43, the check line itself, which carries the tip placeholder's literal word; its three other placeholders were filled at seeding, so that line's own grep prints 5.
  - The Register key's D-SYS-014 is a row in `## Open decisions`. The decided table's highest SYS row is D-SYS-013. The other eight areas match my reading of the table.
- **§ 1 first commands:** every line printed as expected (`stage-a/first-commands.txt`). T33's ES tip is now `f802c55c62c1` (the brief read `dd86d7ce20a5`).
- **§ 2 membership block:** extracted from the brief byte for byte and run twice. Every expected line printed: `mine: 80 paths.txt: 80 equal: True`, the five summary lines, the 25 claims, the four ES-CORE rows, `wc -l 21971`, `grep -c 21984`, 80 and 80, and the shortstat twice. The outputs are in `.qa-scratch/t34/` (gitignored), to be carried into `01`.
- **§ 5 runs block** (`stage-a/runs.txt`, every line with its rc and wall time; block rc 0 in 3 s). Every expectation matched, with one brief erratum: the in-source gates command prints **13** lines. That is exactly § 4 Q7's list, where `VideoPlayerComponent.{cpp,h}:1` is two lines; the comment's "twelve" is the miscount. All eight lane tips are empty inside the 80.
- **#681's body:** its 21 checkboxes equal the brief's § 7 byte for byte. Issue states are in `stage-a/issue-states.txt`.
- **The ES worktree** is at the pin, clean, with an empty diff against it. Nothing was written there.
- **The rules:** six rule files in T34's worktree differ from the copy this session loaded (the T3 worktree's): `device-builds`, `engineering-practices`, `es-code-traps`, `es-player-text`, `es-ui-style-guide`, `generic-x64-vm-testing`. T34's are the ones the brief cites, and they are read from this worktree.
- **Stopped** here at the session's usage limit.
  - **Stage A still owes:** `01-research-notes.md` § Scope, the pointer's checkpoint (and its line-43 check rewritten), and the day's work-log entry headed #681.

## [Stage A] 14:24 UTC 2026-10-30 — resumed after the usage-limit stop; the stage-A close

- **The stop:** from just after `22c0d5a2c2` (about 09:57) to 14:22 UTC, the session's usage limit. Nothing of T34 ran in the gap: no process, and the ES worktree at the pin, clean.
- **The host file, read at 2026-10-30T14:24:16Z (59 lines):** M7's TLS native window ran 13:25:28 to 13:26:11, and its TLS VM window 13:33:45 to 13:35:50 (the guest's certificate generation failed; nothing remains). At 14:21 the coordinator granted M7 a follow-up TLS guest, with T34's window asked for after stage B and after every M7 window. **Census** at 14:24:16: qemu 0, compilers 0.
- **The placeholder check, corrected:** the commit `22c0d5a2c2` carried this file with two of the brief's placeholder words spelled out, so the brief's § 9 grep printed 1 on it; I had committed without gating on that line. Both are reworded. `stage-a/runs.txt` and `01` quote the brief's removal-check comment, so the four words are written hyphenated there (said in `runs.txt`'s first line). The grep now prints 0 on `00`, `01`, every `stage-a/` file and the pointer.
- **Written:**
  - `01-research-notes.md` (§ Scope, generated from `stage-a/membership-block.txt`; § The § 5 runs at stage A, from `stage-a/runs.txt`; § Read this session);
  - `stage-a/membership-block.txt` and `stage-a/paths.txt`;
  - the pointer (the stage-A focus, its line 43 rewritten, the first checkpoint line);
  - the day's work-log entry headed #681.

## [Stage B] 14:46 UTC 2026-10-30 — 02 composed; the window plan; the request

- **`02-forward-audit.md`** is composed by `tools/t34-02.py` from `tools/t34-02.template.md` and nine generators (coverage, leads, layouts, constants, input, lifetimes, reads, words, includes). Each was seen to exit 1 on a constructed drift (`stage-b/generator-drifts.txt`). It has 510 lines, its 16 sections in the brief's § 6 order, and 80 coverage rows by § 7's own command; the placeholder grep reads 0.
- **New leads:**
  - L-22: the card's `close()` writes its closing state unlocked from the holders' threads while `update()` reads it;
  - L-23: `"add star"` is outside `_()`;
  - L-24: a video component's BACK prompt is labelled SELECT.
- **Readings:** L-09 is sound at the pin, by the writer's erase. § 1 (g)'s `setOpacity` is unreachable on the fork's images. `UntintedImageComponent` is at `GuiMenu.cpp:6401`.
- **The window plan** is `stage-b/window-plan.md`: 1,410 s by the brief's command re-run; 30 + 5 minutes; two boots.
- **The push route:** HTTPS with `gh`'s credential (the friction lines).

## [Stage C] 19:39 UTC 2026-10-30 — the guest window (granted 19:24), START 19:28:13 to RETURN 19:39:23

- **The order:** the host file was read at 19:27:40, the minute before START. My scripted open-START check matched no M7 line, because M7 stamps its lines `+00:00`, not `Z`. Read by hand at 19:27:53: the last M7 runtime line was the 13:35:50 RETURN, so no M7 START was open. The scripted check was wrong, and I said so in the START post.
- **The guest:** `generic-x64-vm run --headless --daemonize` through a wrapper (`guest-cycle/helpers/qemu-wrap`) adding `restrict=on` to the user netdev (read back from `/proc/<pid>/cmdline`), sockets under `/workspace/tmp/m6-t34/guest/`. Two boots: 640x480 (pid 743737, 19:27:41 to 19:35:30), then 1280x800 (pid 797892, 19:35:30 to 19:38:58). The detached stop timer was PID 743756, set to fire at 20:02:42; it was stopped with its child by recorded PIDs, unfired.
- **The records:** the RETURN post on #681 (comment 6531938082) carries the readings; the frames and reads are in `guest-cycle/`. Every frame is `image`. Gap 14 px at 640 and 28 px at 1280; the dim's ratio 0.314; the strip's four frames and L-02's pair identical. L-01 not reproduced on the image (0 log lines; the catalog carries `haut/bas`); new lead L-25 (the tabbed page's bar carries no component prompt at 1280); G-02, G-06, G-07, G-08 and G-10 CANNOT with their reasons.
- **The disk:** retired after the RETURN, as `guest-cycle/retired.txt` records; the census `qemu 0, compilers 0, listeners 0`.

## [Stage C] 20:00 UTC 2026-10-30 — 03, 04, 05; the packet; the seat's probe; the refutation started

- **`05`** is written by `tools/t34-05.py` from one item table: 26 items (0 Critical, 0 High, 5 Medium, 21 Low), each Open at the Phase 7 gate before stage D. `question:` uses the brief's numbering. **`04`** has the brief's seven questions, the take-up table disposed, and the plan's seven under Renovation face; it names the owed proofs (the unit build, the sanitizer cases, the syntax check). **`03`** is the audit's retrospective.
- **The council runtime:** `npm install --offline --prefix tools/council` rc 0 (install scripts not run). `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`. `... test`: 39/39, 127/127 and 19/19 pass, 0 fail.
- **The packet** (`tools/t34-packet.py` -> `second-opinions/t34-packet.md` and `packet-manifest.json`): 544,752 bytes and 95 sources (21 files whole, the 59's cited ranges, `02` to `05`, the brief's § 4). Its scan: 0 forbidden, 0 secret-shaped lines, 108 credential-shaped words each classed by file:line, 0 a value. `gpt-brief.md` (the ask plus the packet): 547,488 bytes, sha256 `126879915217b088c0d8f08925ee95413e9a504955b66c4ada6ec4b4c4e91b27`, rescanned 0 and 0.
- **Keyed invoke 1 of 2, the probe:** 19:59:53 to 20:00:06Z, `READY unknown`. Served `openai/gpt-6-astra` by OpenAI, effort `max`; verification, effort and provider PASS; `council-facilitator@1.14.1-pixelelated.2`.
- **Keyed invoke 2 of 2, the refutation,** started at 20:00Z with `--per-attempt-timeout-ms 3600000 --total-timeout-ms 10800000`, logging to `/workspace/tmp/m6-t34/audit.log`.
  - **What watches it:** the harness background task `b28z2x9mz`, which delivers its end.
  - **Its silent mode:** a hung seat ends only at those timeouts.

## [Stage C] 20:23 UTC 2026-10-30 — the refutation returned; the findings verified; one held

- **Keyed invoke 2 of 2:** 20:00:16 to 20:17:16Z, attempt 1 of 4, `finish=stop`, 24,250 bytes of content, 35,726 reasoning tokens. Served `openai/gpt-6-astra` by OpenAI at `max`; verification, effort and provider PASS. The reply was scanned before it was read: 0 forbidden, 0 secret-shaped.
- **No more keyed invokes:** exactly two were allowed, and both ran. The seat's "Sections I need" list got no second packet.
- **The grades** are recorded in `04` § Second opinion: PL-05 and PL-24 refuted (proposed withdrawn); PL-04 lowered to Low; PL-07 and PL-18 raised to Medium; the rest confirmed, confirmed with narrowing, or cannot tell.
- **G-1 to G-16:** each read at its cited lines at the pin before it was carried (11 confirmed, 5 with narrowing). They are PL-27 to PL-42.
  - **G-7 corrects this audit:** the stage-B statement of the grid's `clear()` contract was wrong, and `02` is recomposed with the correction.
  - **The seat's `:205` correction** (`addWithLabel`) is applied. Checking it found a seventh formatter, `:358` `setSubTitle` through `getFileName`: L-26, PL-43.
- **G-3 (PL-27) is security-sensitive,** and this repository and tracker are public. Its details are kept out of every committed file and post. The reply is held at `/workspace/tmp/m6-t34/held/gpt-audit.md` (mode 600; sha256 `609c488c...`, which the committed receipt binds). The maintainer's decision on the channel is asked for at the pause.
- **`05` now holds 43 items** (0 Critical, 1 High, 15 Medium, 27 Low), each Open until stage D disposes it.
- **The pre-issue lint** (`stage-c/lint-pre-issue.txt`):
  - on the committed tree: rc 1, one failure, the missing reply (the lint hashes it against the receipt, `tools/lint-audit-artifacts:105-110`);
  - with the held reply copied in for the run and removed straight after: `PASS pre-issue artifacts (does not certify resolution)`, rc 0. The reply was not left in the tree (`git status` after).

## [Stage D] 20:25 UTC 2026-10-30 — the audit issue; the pause

- **The audit issue:** #1307, `Audit: M6 T34 EmulationStation's core components -- 43 findings (0 critical, 1 high)`. Labels `audit` and `punch-list`, milestone M6, a sub-issue of #681. Its 43 checkboxes are generated from `05`. `tools/box-check --issue 1307`: `43 open checkbox(es), 0 fail`, rc 0. PL-27's line names no mechanism.
- **The pause** is posted on #681. The lane waits for the coordinator's dispositions, the four register rows, the channel for PL-27, the bug list and the unit build's timing.

## [Stage D] 20:39 UTC 2026-10-30 — the owed proofs, under the 20:30 ruling (host-only; the host file's lines 20:32:17 START, 20:39:10 END)

- **The stand-in syntax check over the 37** (`tools/t34-syntax-check.sh`, `stage-d/syntax-check.txt`):
  - the first run: 35 of 37 rc 0. `BusyComponent.cpp` and `TextEditComponent.cpp` stopped on SDL symbols T31's fakes do not declare: the mutex calls, the keyboard calls and nine `SDLK_*`;
  - the lane's copies were extended, plus the tenth fake `SDL_power.h`;
  - the second run: **37 of 37 rc 0**. `VideoVlcComponent.cpp` is CANNOT, its two VLC headers named.
- **The unit build** (`tools/t34-build-tests.sh`, T33's with `components-tests` and three sanitizer programs; `stage-d/build-tests.txt`): rc 1 (`components-tests` FAILs at the pin, as it should). The script exited 0 on its first run despite that, because its run loop never set `FAIL` for the new binary; that is fixed. `TOTAL: 246 test cases in 6 binaries`.
  - The tree's five binaries pass: 185, 24, 10, 2 and 18 cases.
  - `components-tests`: 7 cases, 2 passed, 5 failed. Each is the pin's lines lifted verbatim by `tools/t34-extract.py`, each range refused unless it holds its code.
  - **FAIL at the pin, as the brief expects:**
    - 3.4: `0.986957` and `1.01304 == Approx(1)`;
    - 3.6: `80 == 60`;
    - 3.7: `Auto == AUTO`;
    - 3.16: `0 == 1` for `haut/bas`;
    - 3.26: five 128 px buttons `710.4 <= 576` (four fit).
  - **PASS at the pin:** 3.8, every loop type landing in range (the seat's refutation of PL-24, shown), and 3.7's precision case.
  - **The sanitizer cases:**
    - PL-01: `WARNING: ThreadSanitizer: data race`, rc 66;
    - PL-03 / 3.20: `ERROR: AddressSanitizer: heap-use-after-free`, rc 1;
    - 3.19 (a double of the popup's shape, not its lines): clean, rc 0.
- **Not yet written:** 3.21, the other 26 seam cases, and the new items' own cases. They follow the bugs.
- **20:44 UTC, the bugs filed:** 25, #1309 to #1333 (`stage-d/bugs-filed.txt`, `tools/t34-file-bugs.py`). Each has its trace, its family, its VM line, `Already written:` and criteria an agent can tick; `tools/box-check` reports 0 fail on each. PL-27 (#1323) carries only its fix's shape and the held trace's path and sha256 (`46d9494e...`); the trace is at `/workspace/tmp/m6-t34/held/pl27-trace.md`, mode 600, beside the coordinator's `pl27-stream.md`.

## [Stage D] 00:48 UTC 2026-10-31 — the stand-in and the sanitizer sources moved to the paths the acceptance reads

- **The coordinator, 00:47 (comment 6536721649), asked for these files to be committed;** they were already in the tree at `be881e95bc` (committed in `f6d5d2ffa9`), at other paths: `tools/t34-syntax-check.sh`, `tools/t34-build-tests.sh`, `stage-a/fakes/` (14 files: T31's 13 and `SDL_power.h`), and `tools/t34-{tsan-card,asan-textedit,asan-popup}.cpp`. `git ls-tree -r --name-only be881e95bc` lists each.
- **Moved with `git mv`, one copy each:** `tools/t34-syntax-check.sh` to `stage-a/syntax-check.sh`, and the three sources to `stage-d/tsan-card.cpp`, `stage-d/asan-textedit.cpp` and `stage-d/asan-popup.cpp`. `tools/t34-build-tests.sh` names the new paths, and the stand-in's usage line its own.
- **Checked without running anything:** both scripts pass `bash -n`; the build script's three source paths resolve from `tools/`; the stand-in resolves its 14 fakes from `stage-a/`.
- **Not run since the move:** no compile ran, because the ruling says nothing runs before the stream brief. Both scripts' last runs were from the old paths, recorded at `stage-d/syntax-check.txt` and `stage-d/build-tests.txt`. The `tools/t34-syntax-check.sh` named in the 20:3x entry above is now `stage-a/syntax-check.sh`.

## [Stage E] 01:08 UTC 2026-10-31 — S0: the four floor cases no stream's file holds, run at the pin (the 01:01 dispatch, comment 6536878915; the brief's ruling 10)

- **The brief** is the coordinator's `65bd4d446d:docs/reviews/briefs/t34-streams.md`. It still names the stand-in and the sanitizer sources at their pre-move paths, `tools/t34-syntax-check.sh` and `tools/`; they are `stage-a/syntax-check.sh` and `stage-d/*.cpp` since `d446c4c6c3`.
- **Four cases in `components-tests`**, over the pin's lines lifted by `tools/t34-extract.py`. Five specs were added (D-WORKFLOW-210): before, none for these files; after, `textlist_range`, `textlist_camera`, `scroll_defines`, `scroll_update` and `scroll_reset`. 3.15 reuses `ilist_scroll`.
- **Results at the pin** (`stage-e/s0-before.txt`):
  - PASS: 3.11, 3.29, 3.15 and 3.14.
  - FAIL: 3.14's PL-40 half, on PL-40's lines (`-10 >= 0` and `0 > 1`).
  - `TOTAL: 251 test cases in 6 binaries` (246 at stage D).
- **3.14's first run FAILed on my own arithmetic**, not the pin. The first step lands at the delay itself, because `reset()` starts the accumulator at `-delay + speed`. The case was corrected before the record.
- **PL-40 keeps its ruled disposition** (a #585 line). The case shows a consequence its entry does not name: content narrower than its container never scrolls down. Reach at the pin: the detailed list's description container, whose child takes the container's width. This is put to the coordinator in the S0 checkpoint, not filed: the line is PL-40's.
- **The host file:** START 01:02:54, END 01:08:37.

## [Stage E] 05:48 UTC 2026-10-31 — S1 (#1323, held): the ES branch's first commit, `dbe4c2db0`

- **The held stream section** was read after its sha256 was checked against the brief (`766afe21...`, three matches in the brief). Its case, outputs and notes stay in the held directory. `stage-e/s1-checks.txt` carries their sha256s and counts, nothing else.
- **The case first.** Five held cases over the pin's cache-key lines, lifted verbatim, were run through `tools/t34-build-tests.sh`'s new held hook into a build directory beside them: **2 of 5 FAIL at the pin**. The fix followed. After it: **5 of 5 PASS**, plus the two after-only cases (7 of 7), one of them the containment guard seen to refuse.
- **The commit:** `es-core: WebImageComponent names its cache files by a safe key and keeps every file operation inside the cache directory`, body `Refs #681, #1323`, one file. The stand-in over the 37: 37 rc 0, `WebImageComponent.cpp` among them. The public build: `TOTAL: 251 test cases in 6 binaries`, unchanged.
- **The push.** ES `pre-push-test` PASS. The guard refused a bare-URL push (a URL names no remote, so it read 8192 commits). The push by remote name over HTTPS passed with 1 commit read. Friction-log line written.
- **Two departures from the held stream**, both explained in the held notes:
  - the digest is es-core's md5, because es-core carries no sha256;
  - the count is 2 of 5, not the predicted 3 of 4: the stream's four cases plus one more.
- **The #585 line:** a private report owed upstream; the held notes carry it.
- **The host file:** S1's START and END lines written.

## [Stage E] 06:01 UTC 2026-10-31 — S2 (#1309, #1310, #1311): the card's close, its handle and the field's posts, `2cbb62d7b`

- **The cases came first, run at `dbe4c2db0`** (the card's and field's files are the pin's there; `stage-e/s2-before.txt`):
  - PL-01's interleaving case in `components-tests`: `update()` runs between the pin's two writes. FAIL: a closing frame was drawn before the fade's opacity was captured.
  - `asan-card-handle`, the new program (`stage-e/asan-card-handle.cpp`): heap-use-after-free, rc 1.
  - tsan-card rc 66 and asan-textedit rc 1, as at stage D.
  - 3.18 and 3.33 PASS.
  - `TOTAL: 254 test cases in 6 binaries`.
- **The fix**, one ES commit on four files:
  - `close()` is one release store to `mCloseRequested`, and `update()` turns it;
  - the card derives `enable_shared_from_this` and offers `Handle handle()`;
  - the text field's posts check a weak token made before the constructor's first `onFocusLost()`.
- **After, at `2cbb62d7b`** (`stage-e/s2-after.txt`):
  - PL-01's case PASS;
  - tsan-card rc 0 and asan-textedit rc 0;
  - asan-card-handle rc 0, with 2 of 2 late calls refused and 1 off-thread release handed back;
  - `TOTAL: 254 test cases in 6 binaries`.
- **Window's half is `stage-e/s2-window.patch`** (T35's), written on scratch copies of the pin's two files and proven there:
  - it applies cleanly to both;
  - the patched `Window.cpp` passes the stand-in's compile;
  - the lane's keyboard fake gained the seven SDL names `Window.cpp` reads.

  The card's destructor chain frees GL textures, so ruling 1's retired list is kept.
- **The 13 holder lines** (`git grep -c` agrees with the brief) are merge debt by owner, listed in `stage-e/s2-checks.txt`. #1310's second checkbox ticks at the integration.
- **Specs moved (D-WORKFLOW-210):** `card_close`, `card_update` and `textedit_focuslost`, each named with its before and after in `s2-checks.txt`. New: `card_update_full`, `card_choose`, `textedit_move`, `str_cursor` and `card_handle`. The extractor now takes tree paths and clears stale extracts.
- **`t34-lifetimes.py`:** the four rows carry S2's outcome.
- **One correction to the brief:** it expected no #585 line. `git log -S` puts both the card's close writes and the field's post shape in batocera's 2020 commits (`ad9802f44`, `2f5ec7d33`), so PL-01 and PL-03 get #585 lines.

## [Stage E] 06:12 UTC 2026-10-31 — S3 (#1314, #1315, #1313, #1320, #1326): the layout, `db12b1598`

- **The cases came first, run at `2cbb62d7b`** (`stage-e/s3-before.txt`):
  - PL-07 FAIL;
  - 3.5 FAIL, measured one line short at both sites;
  - PL-15 FAIL (10 at 1280);
  - PL-30 FAIL (the grid sizes the image again from its own notice, depth 5);
  - 3.4 and 3.6 FAIL as at stage D;
  - 3.25 and 3.28 PASS.
- **The fix**, one ES commit on five files (D-UI-130/131/132):
  - the shares are `th / h` and `sh / h`;
  - TextComponent measures at its drawn width, at both sites;
  - the marquee's limit takes `mPadding.w()`;
  - `ROW_INSET_FRACTION 0.015625` is read through `rowInset()` everywhere;
  - MenuComponent's comment names the second copy;
  - `ImageComponent::setSize` returns on an unchanged target size.
- **After, at `db12b1598`** (`stage-e/s3-after.txt`): all eight cases PASS. `TOTAL: 260 test cases in 6 binaries`. The stand-in passes all 37.
- **`GuiMsgBox`'s workaround** is `stage-e/s3-msgbox.patch` (T35's), proven on a scratch copy of the pin's file; the lane's keyboard fake gained `SDLK_SPACE`.
- **The build script's gap, fixed:** a refused extraction left the previous binary to run and report. The first after-run's counts matched the before-run exactly, which is how it showed. Friction-log line written.
- **Specs moved and added:** each named with its before and after in `stage-e/s3-checks.txt`. The layouts and constants generators carry S3's outcome.

## [Stage E] 06:21 UTC 2026-10-31 — S4 (#1312, #1316, #1317, #1318, #1321, #1322, #1325): the words and the prompts, `a9017ff50`

- **The cases came first, run at `db12b1598`** (`stage-e/s4-before.txt`):
  - FAIL: 3.7, 3.16, PL-10, PL-11, PL-19, 3.13 (PL-25) and PL-29;
  - PASS: the floor's 3.1-3.3, 3.12, 3.17, 3.31, 3.32 and 3.34;
  - `TOTAL: 271 test cases in 6 binaries`.
- **The fix**, one ES commit on eight sources and the French catalog. The subject follows ruling 4 rather than the drafted subject. Changes:
  - the icon key leaves `_()` (D-UI-133);
  - AUTO, ADD STAR and <NOT SET> go through it, and ADD STAR gains its French;
  - the video component offers no prompt (ruling 7);
  - one entry offers no direction;
  - the help bar keeps and clips its first prompt, builds no grid only when nothing fits, and takes batocera's `setOpacity` guard (ruling 4).
- **After:** every S4 case PASS; `TOTAL: 271 test cases in 6 binaries`.
  - `es-untranslated`: 704 fork strings, 0 without French.
  - `t34-words.py --at`: 24 lines in 13 files, 28 occurrences at the tip (22, 12 and 27 at the pin).
  - The input counts are unchanged (14 and 12).
  - The stand-in passes all 37.
- **3.16's setup** now reads the list's own line through a catalog double; its assertion is unchanged (D-WORKFLOW-211). Seventeen specs added, eight of them moved by the fix, each named in `s4-checks.txt`.

## [Stage E] 06:30 UTC 2026-10-31 — S5 (#1319, #1327, #1328): the web image, `568ef099d`

- **The cases came first, run at `a9017ff50`** (`stage-e/s5-before.txt`):
  - 3.21's first half PASS (L-09).
  - PL-13's stub: the pin already re-asks on the next bind. Its one FAIL was the cache path kept. Under ruling 5 the fix is the uncached state alone, and #1319's first checkbox says so.
  - PL-31 FAIL: a stale queued URL's picture replaced a local one.
  - PL-32 FAIL for both overloads.
  - 3.22-3.24 PASS.
- **The fix**, one ES commit on three files:
  - `setImage` clears the queue on every bind;
  - a 0-byte answer keeps no cache path;
  - the memory and shared-texture overloads cancel a pending load through the new `cancelPendingLoad()`.

  The subject follows ruling 5 rather than the drafted "bounded retry".
- **After:** every S5 case PASS; `TOTAL: 276 test cases in 6 binaries`; the stand-in passes all 37.
- **Specs moved:** each named in `s5-checks.txt`. S3's double gained the helper the fixed lines call (D-WORKFLOW-211). The reads and leads generators re-disposition L-08.
- **#585 lines:** PL-31 and PL-32 (upstream's lines, per `git log -S`); none for PL-13 (the fork's).

## [Stage E] 06:36 UTC 2026-10-31 — S6 (#1329, #1330, #1331): the image grid, `6050b8419`

- **PL-35's intent read was posted before the commit** (issuecomment-6540110468, ruling 12). The sentinel is the drag's, written at `:1606` and compared at `:1200` and `:1213` in the same 2022 commit, so `:1151` becomes `==`.
- **The cases came first, run at `568ef099d`** (`stage-e/s6-before.txt`), over a double of the grid template:
  - PL-33 FAIL (loop-copy tiles survive `clear()`);
  - PL-34 FAIL (4 visible tiles after three image changes);
  - PL-35 FAIL (no cursor callback, and a video started on a plain move);
  - 3.9 and 3.10 PASS.
- **The fix** is one ES commit on `ImageGridComponent.h`: `resetGrid()` clears the loop-copy tiles, `setImage` retires the old tile, and `:1151` compares.
- **After:** all five PASS; `TOTAL: 280 test cases in 6 binaries`. The stand-in passes all 37, and the template compiles through three es-app includers.
- **#585 lines:** all three, upstream's lines per `git log -S`.

## [Stage E] 06:44 UTC 2026-10-31 — S7 (#1332, #1333, #1324): the switch and the menu, `5908888b5`

- **The cases came first, run at `6050b8419`** (`stage-e/s7-before.txt`):
  - PL-36 FAIL;
  - PL-37 FAIL (2, then 3 header cells);
  - PL-28 FAIL, with each double built over 0xAB bytes: the update type read `0xABABABAB`, two flags read `0xAB`, and the constructor's `setSelected(false)` returned early;
  - 3.30 PASS.

  3.27's FAIL there was my expectation, not the pin: its values line shows the pin computing 277, which the corrected case expects.
- **The fix**, one ES commit on six files:
  - the switch's image follows its state through `updateImage()`, and auto stays in force (ruling 13);
  - `setTitleImage` removes the entry it holds before setting it again;
  - `mUpdateType` starts at `UPDATE_ALWAYS`, chosen after reading every caller (ruling 11);
  - `mSelected` starts false, with the constructor's call forced;
  - `autoScroll` starts false.
- **After:** all PASS; `TOTAL: 285 test cases in 6 binaries`. The stand-in passes all 37.
- **`button_width`** moved with MenuComponent's five lines; the extractor refused it and the run read "not built". The build script now also drops each binary's old run log before compiling.

## [Stage E] 10:46 UTC 2026-10-31 — the hand-back

- **The S2 addendum** `52f0ff512`: the handle is a forwarding class, and the holders' patch is the 13 lines plus one include. `stage-e/s2-holders.patch` and `s2-window.patch` together compile the eight touched sources on a full scratch tree (`stage-e/s2-holders-check.txt`).
- **The build at the ES tip** (`stage-e/handback-build.txt`, the command `tools/t34-build-tests.sh <W> /workspace/tmp/m6-t34/build`):
  - rc 0, `TOTAL: 285 test cases in 6 binaries`;
  - 0 failed test cases in every binary; 3.26 and PL-40's half `may_fail`;
  - the four sanitizer programs, each `g++ -std=c++17 -O1 -g -fno-omit-frame-pointer -fsanitize=<thread|address>` over its `stage-d/` or `stage-e/` source, all rc 0.

  The held case passes 7 of 7 at the tip.
- **`05` at Phase 7:** 26 Resolved, 14 Deferred, 3 Withdrawn. PL-43 is withdrawn by its read.
  - The lint `--phase resolution --issue 1307` PASS, with the held reply copied in for the run and removed.
  - `box-check --issue 1307` 0 fail.
- **The issues:** #681's four header fields are filled. The 25 bugs carry `fixed-at-es`, and #1319's, #1325's and #1332's first checkboxes were re-derived to rulings 5, 4 and 13.
- **The retro** is `stage-e/retro.md`, posted whole on #681.
- **The checks:** `stage-e/handback-checks.txt`. Next: the merge of the coordinator's tip and the hand-back post.
