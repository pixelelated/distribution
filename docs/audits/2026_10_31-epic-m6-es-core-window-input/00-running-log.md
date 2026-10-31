# Running log — M6.P2 T35, EmulationStation's window, input, settings and the rest of es-core (#682)

- **Model:** Opus 5.5 (`claude-opus-5-5`), **effort high**. The session is the T5 session (`m6-t5-build-engine`), free since T33's close-out.
- **reviewed-at:** `b1f2908a55`, the distribution worktree's HEAD at stage A: the coordinator's `be119338ff` merged at `b51dd8a805`, then the pointer seeded. **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`. The ES worktree `feature/m6-es-core-window-input-682` is at the pin and clean.
- **The dispatch:** #682 comment 6539807425, 05:56:41 UTC 2026-10-31. It names the brief `docs/reviews/briefs/es-core-window-input.md` at `8b5d9b9b62` (version 2), the lane tip `b1f2908a55`, and a census at 05:56 of qemu 0 and compilers 0.
- **The host,** read at 06:00:08Z (`stage-a/host.out`):
  - M7 holds a native window grant (the coordinator's 05:42 line) and its no-NIC guest next.
  - T34's lane wrote `stage E S2 compiles START` at 05:55:03Z, with no END line at the read.
  - The census at 06:00:08Z: qemu 0, compilers 0 (cc1plus), g++ 0.
- **Can this be done on the VM?** Yes. The host goes first, then one guest window granted on #682 (brief § 5 item 1).
- **The pointer's eleven keys,** read against the brief's § 10 table before the first command after `cat`: none names T34 (`es-core-components`, the 80 paths or the T3 session). Each reads the value § 10 asks for. One note, not a predecessor error: the `Branch (distribution):` line says the lane's own tip is `b51dd8a805`, while HEAD is `b1f2908a55`, the pointer's own seeding commit, which the dispatch names.
- **The rules followed:**
  - This worktree's `.claude`, `CLAUDE.md` and `AGENTS.md` differ from local `next` (`8ebaf8daad`) by 11 files (+211/-11). They carry the coordinator's branch, which is newer than `next`.
  - The session's rules were loaded at start from the T5 worktree (`m6-build-engine-652`). Six of this worktree's rule files are newer than those: `device-builds`, `engineering-practices`, `es-code-traps`, `es-player-text`, `es-ui-style-guide` and `generic-x64-vm-testing` (`git diff --stat feature/m6-build-engine-652 HEAD -- .claude CLAUDE.md AGENTS.md`: 8 files, +174/-9, two of them skill files). Their hunks were read from this worktree before this log was written, so where a rule matters here, this worktree's copy is the one read.

## [Stage A] 05:57 to 06:03 UTC 2026-10-31 — the brief, the first commands, the block, the runs

- **Read:** the dispatch comment whole; the pointer (`cat`); the brief at `8b5d9b9b62`, 2,120 lines (the worktree copy equals that commit's), § 10 first and then § 1 to § 9; the six newer rule hunks above (`git diff feature/m6-build-engine-652 HEAD -- .claude/rules`).
- **The first commands** (brief § 1; `stage-a/first-commands.out`, 05:58:44Z): every line prints as § 1 expects -- `stacked`, `upstream-next-is-here`, the ES worktree at the pin with 0 status lines, `cada856d86`, `f6c542872e`, `b2ceb55a7e`, `1750dded8c`, `register-ok`, `stacked-on-P1`, `coordinator-tip-merged`, the diffs against `8ebaf8daad` and `b51dd8a805` empty, `inventory`, and § 9's placeholder grep on the pointer `0`.
  - **One delta:** T34's `origin/feature/m6-es-core-components-681` now resolves, to `dbe4c2db0f`, where the brief expected a `fatal:` line. Its delta inside the 96 is empty (the § 5 run below). Recorded, not a stop.
- **The membership block** (brief § 2, run verbatim from the brief's text; `stage-a/membership.sh`, `.out`; 05:58:56Z to 05:58:57Z, rc 0):
  - `96 .qa-scratch/t35/paths.txt`;
  - `mine: 96 paths.txt: 96 equal: True`;
  - `lines: 22575 reach: {'shipped': 96} tier: {'fork-own': 13, 'upstream-carried': 83} lang: {'cmake': 1, 'c-header': 51, 'c++': 44}`;
  - `fork-own lines: 6759`; `read lines: 22575`; `wc -l 22567`; `grep -c 22575`; `95` and `95`;
  - `13 files changed, 247 insertions(+), 71 deletions(-)` twice.

  Every line is § 2's, byte for byte. **One record-only delta:** the brief's prose lists two `GuiLoading.h` rows under `CLAIMS` that the script's own `named` list does not carry, so the block prints 30 claims, not 32. The four `ES-CORE BY SLICE` rows are § 1's.
- **The § 5 runs** (`stage-a/runs.sh`, `.out`; 05:59:32Z to 05:59:35Z): 22 runs, each wrapped in its own `rc=$?` line and a `date +%s` pair around the brief's lines, unchanged inside. Every figure prints as expected, with these deltas recorded beside the expectations:
  - T34's ref prints an empty stat inside the 96, not `fatal:`.
  - The lock grep prints `66 78 94 143 181 196`. The brief's comment expects `181` and `196`; the other four are the acquisitions in `RegisterComponent`, `UnregisterComponent`, `ResetComponent` and the destructor, as § 2's table names them.
  - The `say(` grep prints `44 234 240`, three lines, as correction 7 and L-16 state, though the comment names two.
  - The gates run prints one line of 128 items (counted, `run rc=0`). The `ROCKNIX` grep its expectation names is added as a run of its own: 3 lines, `InputManager.cpp:585 Paths.cpp:76 Splash.h:10`.
  - The three STAGE C commands are `CANNOT` at stage A: their scripts are the lane's stage-C inputs.
  - The removal check, with the lane's own tip `b51dd8a805` filling the brief's placeholder, prints empty for both diffs. The run of the literal placeholder word was dropped from the record so § 9's placeholder grep reads 0 on every artifact.
- **The issue states** (brief § 3 item 9; `stage-a/issues.out`, read at 06:00:08Z):
  - **OPEN `bug`:** #1283, #1276, #1212, #1178, #1305, #1195, #1245.
  - **OPEN, no label:** #682 (1 comment, the dispatch), #1192, #54, #1137, #1138, #1141, #585, #63, #65, #680, #681.
  - **OPEN, labelled:** #1307 (`audit`, `punch-list`) and #700 (`epic`).
  - **CLOSED:** #1270, #115, #149, #177, #178, #246, #283, #299, #48.
- **Nothing was written in the ES worktree.** Its HEAD is the pin, with 0 status lines (the first commands, and the removal check's second diff). No guest, no image build, no fetch and no keyed call. The scratch is `/workspace/tmp/m6-t35/tmp`, made after `df -i` (26% of the inodes used).

## [Stage B] 06:08 to 06:38 UTC 2026-10-31 — `02` in § 6's order, nine generators and their drifts, the window plan

- **Read first:** the coordinator's acceptance of stage A and its answer on #682 (comment 6539898291, 06:07 UTC), whole. T34's held `stage-e/s2-window.patch` was read on T34's distribution branch (`3bb0924c87`, 06:08:25Z) as Q1's input. T34's ES tip was read twice by `git -C ... rev-parse`/`diff`: local `db12b1598a`, `origin` `2cbb62d7bd` at 06:08:37Z, then local `568ef099d`, `origin` `a9017ff50` at 06:29:09Z for `02` § The merge debt. Both reads are empty inside the 96. The hand-back reads it a third time.
- **The generators** (`tools/`, each `python3 -I <gen> <W> 16dbac5211 .qa-scratch/t35/paths.txt key=value...`, reading the pin by `git show`): `t35-coverage.py`, `t35-leads.py`, `t35-surfaces.py`, `t35-input.py`, `t35-locks.py`, `t35-lifetimes.py`, `t35-scripts.py`, `t35-words.py` and `t35-includes.py` over the shared `t35lib.py`, plus `t35-runs.py` over stage A's record. Each asserts its counts and every cited line's text, and ends `generated, asserted: ...`.
- **Each generator was seen to exit 1 before it was trusted** (`stage-b/drift.sh` -> `stage-b/generators.txt`; re-run after the last generator edit, which was a display label): rc 0 clean, then rc 1 on each of three constructed drifts -- (a) a wrong expectation, (b) the paths list with a cited file dropped, (c) the pin's paths read at the base `bccd715707`, where the cited lines have moved. 0 tracebacks; every FAIL is an assertion. `t35-runs.py` exits 1 on `runs=24`.
- **The composition:** `tools/t35-02.py` writes `02-forward-audit.md` from `stage-b/02-template.md`. It refuses on any generator's non-zero exit (`stage-b/compose-drift.out`: a template with `rows=95` -> `t35-02: t35-coverage.py exited 1; nothing written`), on a coverage section that is not 96 rows, and on a placeholder. `stage-b/compose.out`: *10 generated sections, coverage rows 96, placeholders 0*. `02` is 787 lines, its 16 sections in § 6's order. The acceptance's own awk prints `96`.
- **What the tree said at stage B** (the leads' dispositions, `02` § The leads): 24 of 29 leads confirmed at the tree, 1 contradicted, the rest read or supported. **L-20 is contradicted:** `configureEmulators` writes index and GUID only, no device name (`InputManager.cpp:1481-1482`). **L-07 is supported:** the `exists` cache stores misses, and `save_file` bypasses it (T36's `FileSystemUtil.cpp:296`, `:323`). The brief's `:420` (the SDL mapping files) is **WIN32-only** (`:404-483`). The writes grep's seven sites hold **five writes and two read-mode `fopen`s**. Every `ProcessStartInfo` reaches `/bin/sh -c` or `system()` (`Platform.cpp:162-181`). The per-event script pass runs `quit`'s scripts without waiting (`Scripting.cpp:142`, `:177`). The queue's LIFO pop is upstream's (the base's `:322-323`) against the fork's D-UI-093 comment. **T34's `s2-window.patch` is named a collision for the pause** (10 es-app callers in five lanes and 3 doubles change with its `weak_ptr` return, § 1 i).
- **Brief errata found** (record only, for the coordinator's errata list): § 6 says *L-01 to L-27*, while version 2's tables carry L-28 and L-29. The register's later rows sit one line below the brief's, after D-WORKFLOW-214. The highest D-WORKFLOW is 214, not 213. § 9's placeholder pattern `__[A-Z]+__` also matches the compiler's predefined Apple macro (`APPLE` wrapped in double underscores), so `02` shows it as `APPLE` with a note, and the § 9 check prints 0.
- **The window plan:** `stage-b/window-plan.md`: 30 + 5 minutes, the plan's 1,560 s re-summed by the brief's own command, G-01 to G-12, two boots, the detached timer named at START. The image is present (2,122,289,964 bytes, 06:30 UTC). The host file was read at 06:30:43Z: M7's two granted windows stand (05:42), no M6 runtime is held, and T34's S5 compiles ended 06:30:10Z.
- **No guest, no image build, no fetch, no keyed call.** Nothing was written in the ES worktree (`git -C <W> status --short` empty, HEAD the pin). Host compiles at stage B: none (the generators run python and git only).
- **The `toast` read settled part of L-01** (`stage-b/archaeology-toast.out`): D-UI-093's decided row (`decision-register.md:404`) already says *Nothing is dropped; the order is the order things happened.* So newest-first is a defect against a decided row. `02` cites the row and does not re-argue it, and the order is no longer one of brief § 9's four register questions: three remain (F-ES-24's toast behind a long card, the re-queued duration, the second padding define), plus the CLEAR question. The drifts and the composition were re-run after the edit: 9 clean rc 0, 27 drifts rc 1, *coverage rows 96, placeholders 0*.

## [Stage C, partial] 06:46 to 06:55 UTC 2026-10-31 — the stand-in, window-input-tests, 3.27; T34's s3-msgbox.patch row

- **Read:** the coordinator's acceptance of stage B and the grant (#682 comment 6540234733, 06:45 UTC), whole. The window is queued behind M7 until 07:30 UTC. The seat's two keyed invokes are granted, and **neither was made** this turn.
- **T34's `stage-e/s3-msgbox.patch`** (T34's distribution branch `3e285d86b3`, written 06:12:14Z) has its row beside `s2-window.patch`'s in `02` § The surfaces. It removes `GuiMsgBox`'s #48 height workaround (`guis/GuiMsgBox.cpp:198-202` at the pin) and depends on T34's `TextComponent` fix (#1315), so it is an ordering collision for the pause, not adopted. `t35-surfaces.py` now asserts 22 rows. The drifts were re-run (9 clean at rc 0, 27 drifts at rc 1) and `02` recomposed.
- **The stand-in** (`stage-a/syntax-check.sh`, T34's copied and adapted; T34's 14 fakes under `stage-a/fakes/`; pugixml from the source cache's ES checkout at the pin; rapidjson `/workspace/tmp/m6-t34/rj/...`): **37 of the 44 at rc 0** on the first run, in 11 s (`stage-a/syntax-check.out`). The 7 at rc 1 (`AudioManager`, `ImageIO`, `InputManager`, `PowerSaver`, `Sound`, `Splash`, `VolumeControl`) stop at APIs the fakes lack: SDL joystick/events/audio, SDL_mixer, GL swap, FreeImage, the ALSA mixer, and `SDL_VERSION_ATLEAST`. The fakes are not extended yet. The udev, pulse, TTS, CEC and WIN32 branches are not parsed.
- **`tools/t35-build-tests.sh`** (T34's, copied and adapted; extracts by `tools/t35-extract.py`, cases in `tools/t35-window-input-tests.cpp`, the pin's `WatchersManager.cpp` linked behind `tests/app-unit/fakes/Log.h`): `stage-c/build-tests.out`, 41 s, **`TOTAL: 249 test cases in 6 binaries`**. The tree's five binaries pass 239 of 239. `window-input-tests` has **7 of its 10 cases FAIL at the pin, the seven candidates as designed**:
  - 3.14: toasts drain B before A.
  - 3.10: the approximate-match log names no device.
  - 3.4: `a$(id)b.zip` reaches the command unquoted.
  - 3.5: `notes.txt` in a per-event folder is run.
  - 3.19: the two padding values are 3.33 and 14.08 px at 640.
  - 3.11: the cached `exists` stays false after `save_file`.
  - 3.1: `ResetComponent` waited 1,491 ms behind a running probe.

  The three recorded contracts pass: the re-queued duration, `notificationDuration`'s branches, and the quoting shapes at the pin. 3.11's first ordering passed, because an uncached `exists(p, false)` rewrites the cache entry (`FileSystemUtil.cpp:161-162`). The case now makes the cached read first, as `writeDeviceConfig` does.
- **3.27** (T33's `stage-c/pl25-screensaver.py` and `t33extract.py`, byte-identical to `947ace1966`; T33's retired scratch was re-made empty for the run and removed with `rmdir` after): **rc 1, `SUMMARY: AddressSanitizer: heap-use-after-free a.cpp:14 in FileData::getImagePath`** (`stage-c/pl25-screensaver.out`). The script takes the `SystemScreenSaver.cpp` path, not the worktree the brief's § 5 line passes (a record delta).
- **Host-file lines:** START/END at each compile (three pairs). No guest, no image build, no fetch, no keyed call. The ES worktree is at the pin and clean.
- **Still owed:** the seven files' fakes; § 3 items 5 to 8; the packet, the plan and the seat's two calls; `03` to `05` and the pre-issue lint; the guest window, which stays queued (not started this turn, because the session cannot supervise it past the turn).

## [Stage C, continued] 10:41 to 10:54 UTC 2026-10-31 — the fakes, 03 to 05, the packet, the probe; the refutation running; the window queued in slot 3

- **The order on the host** (the host file, read at 10:41:36Z and 10:44:22Z): the coordinator resumed at 10:42 and **fixed the runtimes' order: slot 1 M7 native, slot 2 M7's RA guest (1800 s, START by 11:04 UTC or the slot passes to T35), slot 3 T35's guest, slot 4 M7's cloud-native guest.** M7's slot 1 ran 10:42:43 to 10:43:44 (+00:00 stamps). T35's 07:30 rule lapsed while both lanes were cut, so the guest waits for slot 3. A background watcher on the host file reports slot 2's START or RETURN, a move of the order, or 11:05. The first watcher matched T35's own compile line, a self-matching pattern, and was re-armed to skip the lane's lines.
- **The guest disk is prepared before the slot** (`guest-cycle/helpers/prepare.txt`): the image's sha256 `6b4c3079...e08fb` matches its `.sha256`; gunzip, convert and resize rc 0; 16 GiB virtual. The helpers (`qemu-wrap`: `restrict=on` plus one `guestfwd` to the host's WebDAV at 10.0.2.100:9010; `stop-timer.sh`: 2,100 s then `tools/vm-stop`; `census.sh`, T34's) are under `guest-cycle/helpers/`. Census at 10:43: qemu 0, compilers 0, listeners 0. G-05 is named: **REMOVE CONNECTION / CANCEL** (`GuiMenu.cpp:8057-8058`) on the seeded WebDAV connection. G-08: **CONTROLLER MAPPING** (`GuiControllersSettings.cpp:74`).
- **The fakes:** the seven files' gaps were closed by `stage-a/fakes/t35-sdl-more.h` (the event members, keys and macros) and T35 sections in `SDL_joystick.h` (the calls), `SDL_mixer.h` (now `#pragma once`), `FreeImage.h` (two defaults as FreeImage declares them, and the memory and multi-page calls) and `alsa/asoundlib.h` (the mixer). **The stand-in passes 44 of 44 at rc 0 in 11 s** (`stage-a/syntax-check.out`; the first run, 37/44, is `syntax-check-first.out`). Host-file START/END at 10:45:35Z and 10:46:57Z.
- **`05`** (`tools/t35-05.py`): 24 items (0 Critical, 0 High, 6 Medium, 18 Low), all Open before stage D. **`04`** carries the lint's sections, Q1 to Q7 at their lines, and the take-up table's 32 rows each disposed (one carried: the tile text's theme contract, T34's file, not re-read). **`03`** is the audit's retrospective. § 3 item 5 (the tests), item 6 (the walks' README, the steps G-06 and G-09 use, the keys) and item 7 (the French: the lane's own parse in `t35-words.py` agrees with the brief's 61 msgids, 25 `pgettext` and 2 `ngettext` pairs, the fork's `CLEAR` -> `EFFACER`) were read. Item 8: T34's `02` was not re-read for a § What T35 inherits beyond the two held patches.
- **`02` § The runs** now reads stage C's records (`t35-runs.py` asserts 44/44/0, `TOTAL: 249 in 6`, the seven failing cases by name, the tree's five binaries at 0 failed, 3.27's ASan line). `02` was recomposed (*coverage rows 96, placeholders 0*), and `runs=24` still exits 1.
- **The council runtime, keyless** (`stage-c/keyless-calls.txt`): `npm install --offline --prefix tools/council` rc 0 (install scripts not run); `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`; `... invoke --help`.
- **The packet** (`tools/t35-packet.py` -> `second-opinions/t35-packet.md`, `packet-manifest.json`): 511,237 bytes, 83 sources (13 files whole, the 83's cited ranges, `02` to `05`, the brief's § 4). Scan: forbidden-terms 0, secret patterns 0, 121 credential-shaped words each classed by file:line (`tools/t35-packet-disp.json`, 34 code lines: `key` a keyboard key or input type, `user` the player or SDL's user event, comments), 0 a value. Withholding one class (`T35_PACKET_DROP=src/Window.cpp:1159`) refuses the packet, rc 1. `gpt-brief.md` (the ask plus the packet): 514,074 bytes, sha256 `df7e8f3a978f1d711b6fe405e1863a58ab964288552d08f073d4304e4e9be62a`, rescanned 0 and 0.
- **Keyed invoke 1 of 2, the probe:** 10:53:10 to 10:53:26Z, rc 0, `READY unknown`. Served `openai/gpt-6-astra` by OpenAI at `max`; semantic verification PASS; `council-facilitator@1.14.1-pixelelated.2`; 28 prompt, 463 completion tokens.
- **Keyed invoke 2 of 2, the refutation,** started 10:53:40Z with `--per-attempt-timeout-ms 3600000 --total-timeout-ms 10800000`, logging to `/workspace/tmp/m6-t35/tmp/refutation.log`. **What watches it:** the harness background task, which delivers its end; **its silent mode:** a hung seat ends only at those timeouts. No other keyed call.
- **3.17 and 3.3 under ThreadSanitizer** (`stage-c/tsan-posts.cpp` over two new extracts `posts_unreg` `Window.cpp:1262-1274` and `posts_post` `:1276-1290`; `stage-c/tsan-watchers.cpp` over the pin's `WatchersManager.cpp` behind `tests/app-unit/fakes/Log.h`; both built by `tools/t35-build-tests.sh`, 41 s, host-file START/END): **both report a data race at the pin**, rc 66. Posts: the erase loop's read (T2) against the post's reallocation under the mutex (T1). Watchers: `WatchersManager.cpp:151` (the destructor's write of `mRunning`) against `:161` (`run()`'s read). `TOTAL: 249 test cases in 6 binaries` again. `05` (PL-01, PL-07), `04` and `02` § The runs now carry them; `t35-runs.py` asserts the two lines. **The packet the seat is reading was built at 10:52**, before these edits: its `04` and `05` are the earlier ones, by `packet-manifest.json`'s hashes.
- **3.2 under AddressSanitizer** (`stage-c/asan-watchers.cpp`, the pin's `WatchersManager.cpp`; host-file START/END): **rc 0, no report, one notification** (`stage-c/asan-watchers.out`). At the pin the list lock spans the probe, so `UnregisterComponent` waits and the `WatcherInfo` is freed between iterations. **PASS at the pin, recorded as the guard PL-01's fix must keep passing** (EP-13: a probe outside the lock must re-validate). It is now in `tools/t35-build-tests.sh` beside the two TSan programs.

## [Stage C] 11:05 to 11:34 UTC 2026-10-31 — the refutation verified; the guest window START 11:07:40 to RETURN 11:31:00; 05 at 34 items; the pre-issue lint PASS

- **The refutation returned** at 11:05:36Z, rc 0: served `openai/gpt-6-astra` by OpenAI at `max`, verification PASS, attempt 1 of 4, 166,040 prompt and 33,790 completion tokens (`second-opinions/gpt-audit.md`, 21,166 bytes; its provenance beside it). It holds no credential or held material. **Exactly two keyed invokes; its `## Sections I need` were not sent.** Every grade and every G finding was checked at the pin before it changed `04` or `05` (`04` § Second opinion):
  - grades: 11 confirmed, 11 with narrowing, 2 cannot tell, 0 refuted;
  - PL-07, PL-15 and PL-22 raised to Medium (PL-15: back on GAME DRIVE DETECTED takes YES, MERGE DRIVE, `Window.cpp:1568-1578`);
  - G-1 to G-14 verified: PL-25 to PL-33, the six WIN32-only ones as one item.
- **Corrections this forced, in the generators:** L-28's "merges the dpad halves" was wrong (G-1); the script queue's thread is not joined (G-7, the lifetimes and locks tables); `mPaused` is protected and only `mRunning` races; 3.2's expectation is PASS at the pin. The drifts were re-run (9 clean at rc 0, 27 at rc 1) and `02` recomposed.
- **The guest window** (slot 3): **START 11:07:40 UTC** (#682 comment 6542598902), **RETURN 11:31:00 UTC** (#682 comment 6542812230), inside the 11:42:40 bound. Two boots of one disk: 640x480, QEMU pid 3085638; 1280x800, pid 3342138. Both stopped by `tools/vm-stop` on the pidfile. Host-file lines at both, with censuses `qemu 0, compilers 0, listeners 0`. `02` § The guest cycle holds every row with its frames (`guest-cycle/`).
  - **G-02/G-03 showed L-01's order on the image:** toast B above toast A after the card.
  - **G-09 showed #1305's window half:** the screensaver over VÉRIFICATION DE VOTRE CLOUD while its job ran.
  - **G-08 closed the hold gap:** a monitor `sendkey x 1000` advanced the detect page.
  - **G-11 reproduced T34 PL-05** and placed it before the window.
  - **G-01 lowered PL-04:** the user `es_input.cfg` exists on first boot.
  - **G-05 is `CANNOT`** (the refusal box precedes the two-button dialog). G-06's clear-and-commit was not shown by the keyboard route. G-10 is `CANNOT`.
- **One mistake in the window, caught inside it:** the stop timer carried `--timeout 90`, which `tools/vm-stop` refuses. It was found when my own stop failed at 11:24:57 and replaced by its PID (3085742 -> 3339644) with the same 11:42:41 deadline at `--timeout 60`. Had it fired unreplaced, it would have failed and left the guest running past the bound. A friction line is owed (the helper copied T34's value without checking `tools/vm-stop`'s limit).
- **The guest's network:** a `tcp:` guestfwd is one connection opened at QEMU's start, so the WebDAV answered once. G-02 and G-09 ran on the unreachable cloud's bounded outcomes.
- **The disk retired:** 2,312,372,224 bytes, sha256 `c98ec34b491ff866f9d2e135af5374e7bb6cb7f34e695c42b3a77a6c4d1385e7`, absent after (`guest-cycle/retired.txt`). The WebDAV is down by its pidfile. The stop timer was stopped by its PID, unfired.
- **`05`: 34 items (0 Critical, 0 High, 9 Medium, 25 Low), all Open before stage D.** `tools/lint-audit-artifacts --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)`.

## [Stage D] 11:37 to 11:42 UTC 2026-10-31 — the audit issue #1337, six bugs, two traces, the punch list posted; the pause

- **Read first:** the coordinator's acceptance of stage C and its rulings (#682 comment 6542863818, 11:37 UTC), whole. PL-03 and PL-15 are filed publicly with neutral titles, PL-03 naming no example file in its body. PL-15 is re-graded **High as data safety**. PL-02 is filed as a defect against D-UI-093's decided row.
- **`05` re-graded:** 34 items, **0 Critical, 1 High, 8 Medium, 25 Low**, all Open. `04`'s counts follow.
- **The audit issue #1337:** `Audit: M6 T35 EmulationStation's window, input, settings and the rest of es-core -- 34 findings (0 critical, 1 high)`, labels `audit` and `punch-list`, milestone M6. Linked as a **sub-issue of #682 by REST id** (6134366034); `sub_issues` of #682 reads `1337`. Its body carries the punch list with every item's `question:` in the index, the bug table, and a Phase 7 checklist of 34 checkboxes. `tools/box-check --issue 1337`: 0 fail.
- **The bugs** (`tools/t35-file-bugs.py` -> `stage-d/bugs/`, `stage-d/filed.txt`): PL-02 **#1338**, PL-03 **#1339**, PL-04 **#1340**, PL-07 **#1341**, PL-15 **#1342**, PL-27 **#1343**. Each carries its code trace, the positive before the fix, what reading cannot prove, its VM line and its `Already written:` line. Each was checked by `tools/box-check --issue N`: 0 fail. The forbidden-terms check read 0 on each body, and PL-03's body names no example file (`grep` 0).
- **The traces on the existing bugs:** #1283 (PL-01's es-core half: 3.1 at 1,491 ms, 3.3's race, 3.2 clean as the guard, the fix shape; comment 6542901479) and #1305 (PL-05's window half: 3.27's ASan line and G-09's frames; comment 6542901694). Both bodies were read to their last comment first (0 comments).
- **The lint:** `tools/lint-audit-artifacts ... --phase pre-issue --issue 1337`: `PASS pre-issue artifacts (does not certify resolution)`. A first run failed on 0 checkboxes in #1337, fixed by the Phase 7 checklist.
- **The pause:** the punch list is posted on #682 as its input. `t35-streams.md` is the coordinator's. Nothing is written in the ES worktree before a stream brief.

## [Stage E, S0] 16:02 to 16:11 UTC 2026-10-31 — the floor cases no stream holds, each run at the pin (ruling 21)

- **Read first:** the coordinator's stage-E dispatch (#682 comment 6545778560, 16:01 UTC), whole, and the stream brief `docs/reviews/briefs/t35-streams.md` at `0f9f8f69fe` on the coordinator's branch, whole (612 lines, by `git -C .../m6-renovation-plan-346 show`). It carries twenty-one rulings, the register rows D-UI-134 to D-UI-137, and the Backlogs #1344 to #1347. The merge of the coordinator's branch is at the hand-back.
- **The cases** (`tools/t35-floor-tests.cpp`, the sibling binary `floor-tests` in `tools/t35-build-tests.sh`): 3.6, 3.7 (two cases), 3.8, 3.9, 3.12, 3.13, 3.20, 3.22, 3.24 and 3.25, over thirteen new lifts in `tools/t35-extract.py`: `ic_utils`, `ic_ctor`, `ic_map`, `ic_buttons`, `im_hotkey`, `im_onfinish`, `sc_single`, `mb_ctor`, `ip_fade`, `fm_app`, `fm_trunc`, `mame_ops` and `mame_roms`; 25 extracts at the pin.
  - **InputConfig's functions** are lifted whole and compiled against the pin's own `InputConfig.h`, with SDL from `stage-a/fakes` and the log from `tests/app-unit/fakes/Log.h`.
  - **3.20 and 3.24 read their lifts as text.**
  - **3.26 has no host case** (parse-only) and is recorded.
  - Two first-compile errors were the doubles', not the pin's: the fade's lift `return`s from a void function, and `ArcadeRomType`'s `operator |=` lives in `MameNames.cpp:38-44`, now lifted as `mame_ops`.
- **At the pin: `RUN floor-tests: rc 0; [doctest] test cases: 11 | 11 passed | 0 failed`**, every case as the floor table expects (PASS for 3.6 to 3.9, 3.12, 3.13 and 3.22; recorded, and passing as written, for 3.20, 3.24 and 3.25). **`TOTAL: 260 test cases in 7 binaries`** (`stage-e/s0-floor.txt`, 49 s): the tree's five binaries at 0 failed, `window-input-tests` with its seven candidates failing as at stage C, `SAN tsan-posts` and `SAN tsan-watchers` at rc 66. Host-file START/END at every compile.
- **Each floor case was seen to fail before it was trusted** (`stage-e/s0-mutations.txt`). The constructed mutations of the lifts were: `toLower` made a no-op (3.7 fails), the first `say(` call's text removed (3.20 fails), `FADE_DURATION` 250 -> 500 (3.22 fails). A first try at the `say(` mutation only commented the call out, the text stayed, and 3.20 still passed: my mutation's fault, redone.
- **The brief's § Figures not found, items 1 to 3, settled:**
  1. **3.1's figure** is 1,496 ms in `stage-c/build-tests.out` and 1,495 ms in this run. The 1,491 ms the stage-C and stage-D record quoted was the first direct run's console line (06:52 UTC), never kept. `04`, `05` PL-01 and #1283's trace (comment 6542901479, edited 16:10:54Z) now quote the kept lines.
  2. **3.2's own line:** `SAN asan-watchers (-fsanitize=address): rc 0; no sanitizer report` at the pin.
  3. **The pugixml root** is `/workspace/cache/rocknix-sources/emulationstation/emulationstation-16dbac5211.../external`, the same as stage C's commands. The script now prints it.
- **The rapidjson root was re-made.** T34's `/workspace/tmp/m6-t34/rj` is retired, and the first S0 run stopped at once (rc 2, *nothing built*). I extracted the source cache's `rapidjson-1.1.0.tar.gz` (sha256 `bf7ced29...`, matching its `.sha256`) into `/workspace/tmp/m6-t35/rj/` and applied the package's two header patches (`projects/ROCKNIX/packages/devel/rapidjson/patches/rapidjson-0002`, `-0003`). Its `document.h` hashes `a8c29c92d1e89279`, the same as stage C's root.
- **`02`:** § The leads' floor rows show each run's result and `tool-run`; 3.16, 3.18, 3.21 and 3.23 stay `design` for S2, S1, S8 and S7. § The runs gains stage E's asserted rows. The drifts were re-run (9 clean at rc 0, 27 at rc 1), and the pre-issue lint with `--issue 1337` passes.
- **Nothing in the ES worktree** (HEAD the pin, 0 status lines). No guest, no fetch, no keyed call.

## [Stage E, before S1] 16:14 to 16:17 UTC 2026-10-31 — ruling 15's bugs

- **Filed** with `tools/t35-file-bugs.py <out> --file --only ...` (the tool gained `--only`, so the six bugs filed at stage D are never filed again): PL-08 #1348, PL-09 #1349, PL-10 #1350, PL-11 #1351, PL-12 #1352, PL-16 #1353, PL-25 #1354, PL-26 #1355 (`stage-e/filed.txt`; bodies `stage-e/bugs/`). Each in #1338's shape: the code trace at the pin, the positive before, what reading cannot prove, the VM line, agent-verifiable criteria and `Already written:`.
- **Checked:** `box-check --issue N` prints `0 fail` for each, and `forbidden-terms-check --stdin` over the eight bodies prints `0 hits`. All fourteen of T35's bugs are now sub-issues of #1337 (stage D's six had not been attached).
- **Posted** in one line on #682 (comment 6545952298). PL-28's bug waits on ruling 10's ThreadSanitizer program, before S7.

## [Stage E, S1] 16:17 to 16:26 UTC 2026-10-31 — PL-15 (#1342): back on the drive dialogs (ruling 5)

- **The intent read first** (ruling 19): `git log -S'NO, IGNORE THIS TIME' -- es-core/src/Window.cpp` names `a8513aec1` and `eeaa8616a` (Daniel Martin, 2026-03-24 and 2025-12-08), both ancestors of `cada856d86`. The order is upstream ROCKNIX's, so a #585 line is owed (written in `02` § The #585 lines owed).
- **The cases** (`tools/t35-window-input-tests.cpp`, `namespace mb`):
  - The pin's accelerator `guis/GuiMsgBox.cpp:116-134` is lifted verbatim (`mb_accel`) into a box double whose buttons are built from each drive dialog's call. Each call is lifted as text (`dlg_game_id`, `dlg_game`, `dlg_sure`, `dlg_new_id`, `dlg_new`), and a label is a line that opens with `_("...")` and a comma.
  - **3.18** runs the accelerator's three branches.
  - `window-input-tests` is now built with `-DT35_X`, so it can read a lift as text.
- **Before, at the pin** (`stage-e/s1-before.txt`, 49 s): `RUN window-input-tests: rc 1; [doctest] test cases: 16 | 6 passed | 10 failed`. The seven candidates fail, and so do the three drive cases: `values: CHECK( YES, MERGE DRIVE == NO, IGNORE THIS TIME )`, `values: CHECK( YES, FORMAT & MERGE == NO, IGNORE THIS TIME )`, and NEW DRIVE DETECTED without an id with NO, IGNORE first. 3.18, GAME DRIVE DETECTED without an id (NO by name) and ARE YOU SURE? (NO by name) pass. `TOTAL: 266 test cases in 7 binaries`.
- **The fix,** ES `56aa398b8` (`Window.cpp`, 9 insertions, 6 deletions; on origin): each of the three calls lists YES first and the choice that changes nothing on this or a future boot last. Each lambda moves with its label, no word changes, and a one-line comment cites #1342. The fall-through, `:257` and ARE YOU SURE?'s NO / YES are untouched. The stand-in: `t35-syntax-check: 44 file(s) checked, 44 rc 0, 0 not`. `es-syntax-check` exits 2 on this host.
- **After, at the tip** (`stage-e/s1-after.txt`, 42 s): `RUN window-input-tests: rc 1; [doctest] test cases: 16 | 9 passed | 7 failed`, and the failing cases are the seven candidates alone. `TOTAL: 266 test cases in 7 binaries`. The S1 cases run alone: `6 | 6 passed | 0 failed`.
- **D-WORKFLOW-210:** the five dialog specs moved from the pin's 1568-1578, 1583-1586, 1623-1625, 1630-1640 and 1645-1648 to the tip's 1569-1579, 1584-1587, 1624-1626, 1632-1642 and 1648-1651. They hold the same calls, now reordered.
- **The lane's count** (ruling 5; the brief's figure 10), by `tools/t35-msgbox-count.py`:
  - In the 96: 2 three-button calls with none named OK or NO (the two with-id drive dialogs), and 2 two-button calls with neither (NEW DRIVE DETECTED without an id; `GuiInputConfig.cpp:268`'s hotkey question, whose back lands on DO NOT ASSIGN HOTKEY, which changes nothing).
  - At the tip all three drive dialogs end on the safe choice.
  - es-app at the pin: 4 three-button calls, 3 with none named OK or NO (`CloudOffer.cpp:51` back NOT NOW, `ScraperSearchComponent.cpp:468` back CANCEL, `GuiWifi.cpp:251` back CANCEL), named for #1344 and never edited here. The tool splits each call's arguments, skips comments, and counts buttons by argument count so a trailing icon is never read as a name.
- **The checks** (`stage-e/s1-checks.txt`): one file changed, inside the 96; 0 non-ASCII added lines; `es-untranslated` 706 and 703 with French, 0 without; the three doubles' headers 0 lines changed; the ES `.githooks/pre-push-test` `PASS` before the push. Host-file START/END at both compiles.
- **Time to play:** off the launch path (a drive event's dialog).
- **The build script** now also prints every failing case by name, untruncated (`failing:`), because its 40-line excerpt can cut one. `tools/t35-runs.py` asserts each stream's before and after lines from `stage-e/sN-*.txt`.
- **A slip, recorded:** the stand-in (`stage-a/syntax-check.sh`, `g++ -fsyntax-only` over the 44, about 11 s, between the two builds) ran without its own host-file START/END lines; only the two unit builds carry them. From S2 the stand-in runs through a wrapper that writes both.

## [Stage E, S2] 16:25 to 16:40 UTC 2026-10-31 — PL-02 (#1338), PL-07 (#1341), PL-25 (#1354), PL-26 (#1355): the window's queue, posts and help bar

- **The intent reads** (ruling 19; `stage-e/s2-checks.txt`), by `git blame` at the pin and `git log -S'pop_back'`:
  - The pop is `49efd94495`, which came from `ac0fbeac8`. The unregister is `c5ceca49a8`, the wake `d1106f674a` and `8c25e2b086`, the dpad compare `8d7fb7b3e8`. All are ancestors of `cada856d86`, upstream's, so #585 lines are written in `02`.
  - The re-queue is the fork's `c1c0d6ddcf`, so that half gets no line.
- **Figure 8:** `unregisterPostedFunctions` has one caller, `DetailedContainerHost::~DetailedContainerHost` (`es-app/src/views/gamelist/DetailedContainer.cpp:1351`), on the interface thread. The lock is `Window.cpp`'s file-static (`:293`), held only inside `Window`'s own functions (`:313`, `:326`, `:427`, `:1148`, `:1154`, `:1179`, `:1238`, `:1278`, `:1296-1303`), none of which deletes a `DetailedContainerHost`. So taking the lock in the unregister cannot deadlock.
- **The cases, written first:**
  - The interruption case: A on screen, B and C queued, a card. Three toasts, so a fix of the pop alone fails it too.
  - 3.16's two cases, over the whole of `setHelpPrompts` lifted (`help_prompts`).
  - `stage-c/tsan-posts.cpp` extended with the interface thread: the drain (`posts_drain`), update's `:540` (`upd_idle`) and `isSleeping` (`Window.h:69`), with the members taken from `Window.h`'s own lines (`win_idle`) so the double's types follow the tree.
  - The program runs in two phases, the wake first, because a first try with all three threads at once crashed at the pin (rc 134, `bad_function_call`): 3.17's corruption hid PL-26's report.
- **Before, at S1's tip** (`stage-e/s2-before.txt`, 43 s): `window-input-tests` 19 cases, 10 failed (the seven candidates' 3.14 and the three new). `SAN tsan-posts (-fsanitize=thread): rc 66`. Its first report is the post's write of `mTimeSinceLastInput` (`x_posts_post.inc:13`) against update's (`x_upd_idle.inc:2`), and 3.17's race is warning 2 (the erase loop's read against the post's `push_back`). `TOTAL: 269 test cases in 7 binaries`.
- **The fix,** ES `453dffd0a` (`Window.cpp`, `Window.h`; on origin):
  - The pop takes the front, and the re-queue inserts the returned words at the front in their on-screen order. The comments say so, and the duration is unchanged (D-UI-134).
  - The unregister takes the lock.
  - The post marks `mWakePosted` under the lock and the drain applies the two writes.
  - The dpad compare is `==`.
- **The one departure from the brief's words:** the refresh event stays with the post, because only an event ends the main loop's `SDL_WaitEventTimeout` (`main.cpp:1183-1188`). `mSleeping` becomes `std::atomic<bool>` for the post's read. The reasoning is in `s2-checks.txt`, and es-app's `main.cpp` parses against it (`isSleeping()`, rc 0).
- **The extractor's refusal, and a guard that did not fail closed:**
  - The first after-run (`stage-e/s2-after-refused.txt`) refused the S1 dialog specs, which S2 had moved by 22 lines.
  - The script then built `window-input-tests` and `floor-tests` from the previous run's `x/` anyway, while printing *window-input-tests not built*.
  - `tools/t35-build-tests.sh` now clears `x/` before extracting. It was seen to fire: with one spec made wrong in a scratch copy, the run printed the refusal, built neither binary and left no `x/` (`TOTAL: 239 test cases in 5 binaries`, `stage-e/s2-guard-proof.txt`).
- **After, at the tip** (`stage-e/s2-after.txt`, 43 s): 19 cases, 6 failed (3.1, 3.4, 3.5, 3.10, 3.11, 3.19). `SAN tsan-posts (-fsanitize=thread): rc 0; no sanitizer report`. `TOTAL: 269 test cases in 7 binaries`.
- **D-WORKFLOW-210:**
  - `queue_pop` (the same lines, `front()`/`erase(begin())`), `queue_requeue` (1163-1164 -> 1166-1169), `posts_unreg` (-> 1267-1282), `posts_post` (-> 1284-1302), `help_prompts` (-> 1005-1079), `posts_drain` (-> 1304-1329), `win_issleeping` (-> `Window.h:70`), `win_idle` (-> `Window.h:175-177`).
  - The S1 dialog specs moved +22.
- **The checks:**
  - Two files changed, inside the 96; 0 non-ASCII added lines; the stand-in 44 of 44.
  - `es-untranslated` 706 and 703 with French, 0 without.
  - The four signatures the doubles rely on are unchanged. `Window.h` gains `<atomic>`, the atomic flag and `mWakePosted` only.
  - The ES `pre-push-test` `PASS`. Host-file START/END at every compile, the stand-in, the lone TSan try, es-app's syntax check and the guard proof included.
- **A lead, not fixed, read not run:** `PowerSaver::pushRefreshEvent` (`PowerSaver.cpp:19-31`, one of the 96) reads and writes the static `mHasPushedEvent` from the posting worker, while `resetRefreshEvent` writes it on the interface thread. Neither is locked or atomic, and the punch list does not carry it. Put to the coordinator in the checkpoint.
- **Time to play:** the front pop is an erase over a few entries per toast, and the unregister takes one lock per page close. The wake is applied at the next update's drain, and the refresh event still ends the wait at once, so the launch path's length does not change.

## [Stage E, S3, in progress] 16:39 to 16:45 UTC 2026-10-31 — PL-05 (#1305's window half): the fix and its cases; the pages' patch not yet written

- **Figure 9:** `onScreenSaverActivate` is declared at `GuiComponent.h:209` (pin read; `GuiComponent.cpp:959` defines it).
- **The cases** (`namespace ss`, the lifted `ss_render` `:777-779` and `ss_start`): at S2's tip (`stage-e/s3-before.txt`) 21 cases, 7 failed. The S3 hold case gives `CHECK_FALSE( w.saver.started )` -> true, and the guard (a page that does not hold) passes.
- **The fix,** ES `5d7707790` (on origin; pre-push-test `PASS`): `GuiComponent::allowScreenSaver()` defaults to true, and `startScreenSaver` returns while the top page holds. No class in the tree already had that name (`git grep` rc 1). The stand-in gives 44 of 44.
- **After** (`stage-e/s3-after.txt`): 21 cases, 6 failed (3.1, 3.4, 3.5, 3.10, 3.11, 3.19), and `TOTAL: 271 test cases in 7 binaries`. Every `Window.cpp` spec below `startScreenSaver` moved +7 (D-WORKFLOW-210, named in the extractor).
- **3.27 at the tip** (`stage-e/s3-pl25.txt`): still `heap-use-after-free a.cpp:14 in FileData::getImagePath`, rc 1, as ruling 12 expects until T33's or T2's half lands.
- **Not yet done:** `stage-e/s3-pages.patch` for the owners. `GuiCloudTransfer` and `GuiOfflineScan` are T18's (`origin/feature/m6-es-cloud-pages-665` at `d55235d4b`), and `GuiScraperRun` is T31's (`origin/feature/m6-es-pages-678` at `95852f873`). Each page's override is `bool allowScreenSaver() override { return mShownFinished; }` (`mShownFinished` is false while its job runs). It is to be proven by `git apply --check` on copies read by `git show` at those tips. Also still owed: `s3-checks.txt`, `02`'s S3 row, `t35-runs`' S3 entry and S3's checkpoint on #682.

## [Stage E, S3, done] 20:40 to 20:46 UTC 2026-10-31 — PL-05: the pages' patch, the checks, the row

- **`stage-e/s3-pages.patch`** (36 lines, three headers): each fourth-tier page gets `bool allowScreenSaver() override { return mShownFinished; }`, false from the page's construction and from TRY AGAIN until its job's finish is shown.
  - The pages are `GuiCloudTransfer.h` and `GuiOfflineScan.h` (T18's, #665) and `GuiScraperRun.h` (T31's, #678), the owners taken from `docs/reviews/briefs/es-pages.md:408` and `:238` on the coordinator's branch.
  - The patch was written from copies read by `git show` at the owners' tips, `origin/feature/m6-es-cloud-pages-665` `d55235d4b` and `origin/feature/m6-es-pages-678` `95852f873`. `git apply --check` gives rc 0 there and at the pin's copies.
  - The three patched pages, compiled syntax-only (the pin's es-app, T35's es-core, the stand-in's fakes), give rc 0 each.
  - The failing control is `GuiScraperRun.cpp` against the pin's `GuiComponent.h`: rc 1, *marked 'override', but does not override*. Host-file START/END for both compiles.
- **`stage-e/s3-checks.txt`:**
  - Figure 9: `GuiComponent.h:209`.
  - `git grep allowScreenSaver` at the pin gives rc 1. `GuiComponent.h`'s direct includers in the 96 are named there.
  - `startScreenSaver`'s lines are upstream's (`8d7fb7b3e8`, `e83addd461`, `e915ef84e1`), but ruling 19 gives PL-05 no #585 line (the hold needs the fork's fourth-tier pages).
  - Two files changed, inside the 96; 0 non-ASCII added lines; the stand-in 44 of 44.
  - `es-untranslated` 706 and 703 with French, 0 without. The four signatures the doubles rely on are unchanged. The ES `pre-push-test` gives `PASS`.
- **`02`:** S3's row, and § The merge debt names the patch for T18 and T31 (it needs S3's `GuiComponent.h` first). `tools/t35-runs.py` asserts S3's before and after lines and 3.27's FAIL at the tip. The pre-issue lint with `--issue 1337` passes.
- **Time to play:** one virtual call per frame while idle past the setting, off the launch path.
- **A command refused by the harness's safety check** (it contained no removal; the parser could not read its quoting) was rewritten as a script file, `/workspace/tmp/m6-t35/tmp/s3-checks.sh`, which writes the same record.

## [Stage E, S4] 20:47 to 20:55 UTC 2026-10-31 — PL-01 (#1283's es-core half): the watchers probe outside the list lock (ruling 13)

- **The cases, written first:**
  - In `window-input-tests`, against the tree's `WatchersManager.cpp`:
    - A second watcher's `ResetComponent` while the first probes.
    - A reset during a probe is not lost (the guard for the semantics the fix keeps).
  - `stage-c/asan-watchers.cpp` (3.2) extended: a due watcher, not yet probed, unregistered and freed while the first probes, then the probing one.
- **Before, at S3's tip** (`stage-e/s4-before.txt`, 54 s):
  - `window-input-tests` 23 cases, 7 failed. 3.1 gives `ResetComponent returned after 1492 ms` and the second watcher `... 1491 ms`; the reset guard passes.
  - `SAN tsan-watchers ... rc 66`; `SAN asan-watchers ... rc 0; no sanitizer report` with the extension (2 notifications).
- **The fix,** ES `1d5d3e0db` (`WatchersManager.cpp`, `.h`; on origin; pre-push-test `PASS`):
  - `run()` snapshots the due records under `mWatchersLock` and marks each `probing`. Each `check()` and its notification run outside the lock, and the next check time is written back under it.
  - `UnregisterComponent` waits on `mProbeDone` for its own record's probe alone and searches again after the wait.
  - A reset during a probe sets `resetPending` and is applied when the probe ends.
  - The notification never runs under the list lock.
  - `mRunning` is atomic and set under `mThreadLock`. The destructor now joins the thread before it frees the records.
  - The stand-in: 44 of 44.
- **After** (`stage-e/s4-after.txt`, 54 s): 23 cases, 5 failed (3.4, 3.5, 3.10, 3.11, 3.19). 3.1 and the second watcher give `0 ms`. `SAN tsan-watchers (-fsanitize=thread): rc 0; no sanitizer report`, `SAN asan-watchers (-fsanitize=address): rc 0; no sanitizer report`. `TOTAL: 273 test cases in 7 binaries`.
- **The wait left** (ruling 13: recorded beside 3.1's figure). `stage-e/s4-unregister-wait.cpp` was built against `WatchersManager.cpp`/`.h` read by `git show` at both tips (`stage-e/s4-unregister-wait.txt`).
  - Another watcher's unregister went from 1494 ms to 0 ms.
  - The probing watcher's own unregister went from 0 ms to 1493 ms, bounded by its own probe (1500 ms). At S3's tip it was 0 only because the first call had already waited out the whole pass.
- **A script fault found and fixed:** the build script's untruncated failing-case list read doctest's `TEST CASE:` headers, which doctest also prints for a passing case's `MESSAGE`. So the first after-run listed 3.1 and the S4 case as failing while the summary said 5 failed (that run is kept at `/workspace/tmp/m6-t35/tmp/s4-after-first.txt`, outside the record).
  - The list is now `failed case:`, one name per case with an `ERROR` line under its header, and `t35-runs.py` reads it. S1 to S3's `failing:` lines named 3.1 for its message too, but 3.1 was failing there anyway, so their assertions stand.
- **#1283:** its checkbox for this slice (*`check()` called with `mWatchersLock` released, a line-cited read*) ticks from `stage-e/s4-checks.txt`, where the fixed `run()` shows the lock block at `:205-219` and `check()` at `:223`. Whose: `1da12fc7b6` and `5974280a95`, both upstream, so the #585 line (T33's candidate and this slice's) stands in `02`.
- **Time to play:** the interface thread no longer waits for another watcher's probe (3.1's 1,492 ms, gone). `WatchersManager::pause` (on the launch path, L-19) is byte-identical to the pin's.

## [Stage E, S5] 20:58 to 21:04 UTC 2026-10-31 — PL-03 (#1339): the script runner's quoting; PL-17 and PL-18 recorded

- **The helper first:** `git grep -E 'shellQuote|quoteArg'` at the pin finds es-core's own `Utils::String::shellQuote` (`utils/StringUtil.cpp:426-444`, T36's file, used and never changed). It is lifted verbatim for the case (`str_shellquote`). No caller passes a pre-quoted argument (25 `fireEvent` lines, 0 with an escaped double quote).
- **The cases, written first:** `:104`'s case (`"abc` keeps its `c`), and the script path and event name single-quoted. Before, at S4's tip (`stage-e/s5-before.txt`): 3.4 and both fail; the case recording the pin's shapes passes. `window-input-tests` 25 cases, 7 failed.
- **The fix,** ES `c0ab63bf2` (`Scripting.cpp`; on origin; pre-push-test `PASS`):
  - On the shell branch the path, the event name and every argument go through `shellQuote`. A caller's surrounding double quotes are taken off and every other byte is kept: the strip at `:107` and the unwrap's own inner strip both go, so a `"` reaches the hook intact.
  - `:104`'s second test is `endsWith`.
  - The WIN32 branch keeps its double-quote form, because its `ProcessStartInfo` does not read single quotes. It takes the `endsWith` fix only.
  - The stand-in: 44 of 44.
- **After** (`stage-e/s5-after.txt`): 25 cases, 3 failed (3.10, 3.11, 3.19) with `may_fail: 1`. 3.5 is marked `doctest::may_fail` with PL-18 named (rulings 9 and 20): doctest prints *Allowed to fail so marking it as not failed*, and its assertions still count (erratum 9). 3.4 and both S5 cases pass. `floor-tests` 11 of 11. `TOTAL: 275 test cases in 7 binaries`.
- **D-WORKFLOW-210/211:**
  - `exec_cmd` lifted the pin's 90-113 and now lifts 90-136 (both forms; the double compiles the shell one).
  - `event_pass` and `sc_single` moved +23.
  - The recorded-shapes case now holds the fixed shapes, with the pin's quoted in its comment and in `s5-before.txt`.
- **The build script** lists a case doctest allows to fail as `may_fail case:` with a `may_fail: N` line (the hand-back's quote). `tools/t35-runs.py` asserts 3.5 as the one.
- **PL-17's intent, read before its line** (ruling 8): `git log -S'waitForExit = (eventName'` names `d85f6a98f` (2023-10-29, *Make "quit" event waitable*) and `4da07ecfc`, both upstream. The recorded-only #585 line is in `02`.
- **Whose:** the quoting is upstream's (`76a413bba5`, `097b811e4f`, `1c1432ff7d`), so PL-03's #585 line stands.
- **Time to play:** `fireEvent` runs on the launch events. The quoting is one string pass per word, and the directory scans are unchanged (L-19).

## [Stage E, S6] 21:05 to 21:13 UTC 2026-10-31 — PL-04 (#1340), PL-08 (#1348), PL-09 (#1349), PL-10 (#1350): the input manager (rulings 7 and 15)

- **The cases, written first:**
  - 3.11, reshaped (D-WORKFLOW-211; its old shape is quoted in the test file's comment). It now runs through `writeDeviceConfig` lifted whole (`im_writecfg`) into an `InputManager` double over 3.11's cache lift: two pads configured after a startup miss must both reach the file.
  - PL-08's bytes case: the written file equals `save_file`'s for one document. This is the format's guard and passes at the pin.
  - PL-08's polling reader: a 3,000-input document rewritten 60 times while a thread reads the file whole.
  - PL-10's `stage-e/lsan-f4.cpp` over the lifted `:792-800` (`im_f4`), run by `san` as `lsan-f4`.
  - `window-input-tests` now links `utils/AtomicFileUtil.cpp` (T21's, self-contained).
- **Before, at S5's tip** (`stage-e/s6-before.txt`): 27 cases, 4 failed. 3.10 fails; 3.11 gives `values: CHECK( 1 == 2 )`; the reader saw `13321 reads, 3838 of a short file`. `SAN lsan-f4 (-fsanitize=address): rc 1; SUMMARY: AddressSanitizer: 24 byte(s) leaked in 3 allocation(s).`
- **The fix,** ES `f5a698915` (`InputManager.cpp`, `guis/GuiDetectDevice.cpp`; on origin; pre-push-test `PASS`):
  - `exists(path, false)` at `:893`, `:1187` and `:1250`, and at the detect page's first-run skip `:127` (it reads the same file through the same cache, only while a button is held).
  - Both input files are written as pugixml's `save` to a stream (`save_file`'s defaults) through `Utils::AtomicFile::writeText`, a failure logged. `AtomicFileUtil.*` are byte-identical to the pin's (used, never changed).
  - The approximate-match logs read `item`.
  - F4's event is a stack `SDL_Event`.
  - The stand-in: 44 of 44.
- **After** (`stage-e/s6-after.txt`): 27 cases, 1 failed (3.19), `may_fail: 1`. The reader saw `110283 reads, 0 of a short file`, and the bytes still equal. `SAN lsan-f4 ... rc 0; no sanitizer report`. `floor-tests` 11 of 11. `TOTAL: 277 test cases in 7 binaries`.
- **D-WORKFLOW-211:** the first after-run left `floor-tests` unbuilt, because 3.13's `exists` double took one argument and the lifted `doOnFinish` now passes two. The script said `RUN floor-tests: not built` and `TOTAL: 266 test cases in 6 binaries`, so the miss was loud. The double now takes the flag. That run is kept outside the record.
- **D-WORKFLOW-210:** `im_writecfg` 1179-1240 -> 1182-1254, `im_f4` 792-800 -> 794-802, `approx` 939-965 -> 942-968; the floor's `im_hotkey` 1101-1108 -> 1104-1111 and `im_onfinish` 1244-1283 -> 1258-1298.
- **Whose:** every changed line is upstream's (`stage-e/s6-checks.txt`). The #585 lines for PL-04, PL-09 and PL-10 are in `02`, with none for PL-08 (the fork's `AtomicFile`).
- **Time to play:** `exists(..., false)` is one `stat` at each configuration-time read, none on the launch path. `writeText` adds two fsyncs per save on the interface thread, at a configuration's OK and on an SDL-mapped device's hot-plug write. They are priced on the integration image (G-10 `CANNOT` for the hot-plug).

## [Stage E, S7] 21:14 to 21:24 UTC 2026-10-31 — PL-27 (#1343), PL-28 (#1356): the logger (ruling 10)

- **The method:** `Log.cpp`'s `AsyncLogger` is file-local, so a new binary, `log-tests` (`tools/t35-log-tests.cpp`), and two ThreadSanitizer programs (`stage-e/tsan-log-close.cpp`, `stage-e/tsan-log-flush.cpp`) lift the class whole (`log_async`, `Log.cpp:29-196`) beside the tree's `Log.h` and `LogPolicy.h`. `Log::init`'s `Settings` and `Paths` are not on either item's path. The TOTAL line counts 8 binaries from here.
- **Two first shapes did not fail at the pin, and were reshaped before any fix** (kept outside the record):
  - PL-27's case with 200,000 short lines and then the last lost 0 of 5: the worker kept pace and was asleep when the last line came. One 64 MiB line keeps it draining while the last line is enqueued and `close()` runs.
  - `tsan-log-close` with the worker idle before `close()` reported nothing, because the wait's own lock orders the two. A 16 MiB line has `close()` write the flag mid-drain.
  - Their first build failed because `san` puts the app-unit fakes first, so `Log.h` arrived twice. The programs now include `LogPolicy.h` alone.
- **Before, at S6's tip** (`stage-e/s7-before.txt`):
  - `log-tests` 2 cases, 1 failed. 3.23 passes; PL-27 gives `5 of 5 rounds lost their last line`.
  - `SAN tsan-log-close ... rc 66`: the worker's read at `:152` against `close()`'s write at `:71`.
  - `SAN tsan-log-flush ... rc 66`: the handler thread's `write` of the file buffer (`std::__basic_file<char>::xsputn`) against the worker's `memcpy` into it, the buffer `basic_filebuf::_M_allocate_internal_buffer`'s.
- **Ruling 10's (b) runs:** PL-28 was filed as #1356 (`t35-file-bugs.py --only PL-28`; `box-check` 0 fail; a sub-issue of #1337) and posted on #682 before the commit.
- **The fix,** ES `425fbd4af` (`Log.cpp`; on origin; pre-push-test `PASS`):
  - `close()` swaps and drains after the join.
  - The worker copies `mShutdown` under the lock after its swap.
  - `emergencyFlush`'s own `mFile.flush()` is gone, and the handler's limits are written beside `crashHandler`.
  - The stand-in: 44 of 44.
- **After** (`stage-e/s7-after.txt`): `log-tests` 2 cases, 0 failed (`0 of 5`). `SAN tsan-log-close (-fsanitize=thread): rc 0; no sanitizer report`, `SAN tsan-log-flush (-fsanitize=thread): rc 0; no sanitizer report`. `TOTAL: 279 test cases in 8 binaries`.
- **A correction:** the logger is upstream's (`e478a1eda4`, *[Logger] Threaded logging*, an ancestor of `cada856d86`), and only the per-batch flush is the fork's (`469441d4d6`, #178). `05`, #1343 and the brief called it the fork's logger. Under ruling 19 the #585 lines for PL-27 and PL-28 are therefore owed, and they are in `02`.
- **Time to play:** `close()` runs at exit and drains at most one more buffer, and the handler runs at a crash. Neither is on the launch path.

## [Stage E, S8] 21:25 to 21:31 UTC 2026-10-31 — PL-11 (#1351), PL-12 (#1352), PL-16 (#1353): the keyboard, the text popup, the configuration page (rulings 3, 4, 14)

- **The cases, written first:**
  - 3.19, re-shaped under ruling 3 (D-WORKFLOW-211; the old assertion is quoted in the test file): `BUTTON_GRID_HORIZ_PADDING` defined only in `MenuComponent.cpp`, the keyboard's value kept. It is read from the lifts' text: `kb_pad` and the new `kb_pad_use`, the value parsed from the line so the case holds whatever the macro is called.
  - PL-12's three cases: the text popup's CLEAR button (`pp_clear`), the keyboard's `x` (`kb_x`) and its CLEAR key (`kb_clear`), each lifted into a popup double that counts its deletions and its OK callback's calls.
  - 3.21: the subtitle lifted as text (`cfg_subtitle`).
- **Before, at S7's tip** (`stage-e/s8-before.txt`): `window-input-tests` 31 cases, 5 failed, all five of these.
- **The fix,** ES `d0e5b3432` (three `.cpp` and the French catalog; on origin; pre-push-test `PASS`):
  - The keyboard's inset is `OSK_KEY_PADDING`, its value kept.
  - CLEAR (both popups) and `x` set the text to `""` and the cursor to 0, and keep the popup open. No word changes.
  - The subtitle is `getDeviceName()`, falling back to `_("GAMEPAD")`, with `msgid "GAMEPAD"` / `msgstr "MANETTE"` in the same commit (D-UI-051). The orphaned `GAMEPAD %i` is left to `msgmerge`.
  - The stand-in: 44 of 44.
- **After** (`stage-e/s8-after.txt`): 31 cases, 0 failed, `may_fail: 1` (3.5). **The whole unit build exits rc 0:** every binary at 0 failed, every `SAN` line `rc 0; no sanitizer report`, `TOTAL: 283 test cases in 8 binaries`.
  - `es-untranslated`: 707 and 704 with French, 0 without.
  - `es-menu-map-check --ref d0e5b3432`: `55 screen(s) at d0e5b3432, 31 in the map, 24 declared unmapped, 0 missing`.
  - One `#define BUTTON_GRID_HORIZ_PADDING` in es-core, the menu bar's.
- **D-WORKFLOW-210:**
  - `kb_pad` asserted `#define BUTTON_GRID_HORIZ_PADDING` at the pin's `:14` and asserts `#define OSK_KEY_PADDING` at `:16`.
  - The new specs moved: `kb_pad_use` 220 -> 222, `pp_clear` 34 -> 35, `kb_x` 392-397 -> 395-400, `kb_clear` 491-496 -> 494-500, `cfg_subtitle` 128-136 -> 128-139.
  - A first after-run was refused by the extractor (`kb_x` given to 401, a blank line): the S2 guard built nothing and printed the refusal. That run is kept outside the record.
- **Whose:** PL-16's `:134` is upstream's (`c3d400a3af`), so its #585 line is in `02`. There are no lines for PL-11 (a rename) or PL-12 (a design choice; the popup's CLEAR is the fork's `c8dc72cf9e`).
- **Merge debt:** T34's `MenuComponent.cpp:9-10` sentence about the keyboard's second copy is now false (ruling 3, the integration's).
- **Time to play:** none on the launch path.

## [Stage F] 21:33 to 21:33 UTC 2026-10-31 — Phase 7: every punch item at an outcome

- **`tools/t35-05.py` writes the outcomes from one table** (`OUT`), so the gate table and `punch_index` agree. Both come from `t35-streams.md`'s rulings and the streams' commits. **17 Resolved:** PL-01, PL-02, PL-03, PL-04, PL-05's window half, PL-07, PL-08, PL-09, PL-10, PL-11, PL-12, PL-15, PL-16, PL-25, PL-26, PL-27 and PL-28, each with its ES commit and bug. **17 Deferred:**
  - PL-06 to #1310.
  - PL-13 and PL-14 recorded as written (D-UI-134).
  - PL-17, PL-29, PL-31 and PL-32 to #585.
  - PL-18 recorded, 3.5 `may_fail`.
  - PL-19, PL-21, PL-24 and PL-33 recorded under D-UI-079.
  - PL-20 and PL-30 to #1347.
  - PL-22 to #1346.
  - PL-23 the coordinator's sweep.
  - PL-34 recorded as the card tier's design (#1345).
  - 0 Withdrawn.
- **`05`** carries `fixed-at-es: d0e5b3432...`, and PL-27 and PL-28's owner cells carry S7's correction (the logger is upstream's).
- **`tools/lint-audit-artifacts <folder>`** passes on its default `resolution` phase, and with `--issue 1337`.
- **`02` § Positives** gains stage E's: the build at S8's tip exits 0 (`TOTAL: 283 test cases in 8 binaries`, `may_fail: 1`, every `SAN` line rc 0), the seven candidates' FAIL-then-PASS, and the script's two guards.
- **#1337's checkboxes** are ticked against the committed `05` rows (next).

## [Stage G] 21:35 to 21:37 UTC 2026-10-31 — the retro, with time to play

- **`docs/retros/2026-10-31-m6-es-core-window-input.md`**, posted whole on #682 (comment 6549449227), its heading's time from `date -u` in the posting command. It carries the four questions, time to play, what T36 and T37 inherit, the scoped audit and the practice adjustments.
- **Time to play:** stream by stream, nothing lengthens the launch path. The two numbers are `CANNOT` here (no guest after stage C's window, the fixes in no image yet) and are for `tools/time-to-play` on the integration image. The last figure on record is `docs/vm-qa-log.md:171`, and the window's one reading is the startup card's ~100 s (#1345).
- **The cornerstone read:** `git diff --name-only b51dd8a805 HEAD -- packages projects tools` prints nothing (`b51dd8a805`, the dispatch merge).
- **Two friction lines, written late** (`docs/friction-log.md`): S2's stale extracts and S4's message headers, each with its guard. They should have been written when each slowed the work, and were not.
