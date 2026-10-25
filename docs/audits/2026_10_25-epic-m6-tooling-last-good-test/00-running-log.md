# Running log: M6.P2 T15, the last-good scripts test (#662)

- **Executor:** Opus 5.5 at high effort (`claude-opus-5-5`), the T3 session (`m6-t3-emulators`), under the coordinator's dispatch on #662 (2026-10-25 00:21 UTC).
- **Brief:** `docs/reviews/briefs/tooling-last-good-test.md` version 2 (`269a552a0b`).
- **Depth:** Independent: one GPT-6 Astra seat at `max` through the Facilitator.
- **Branch:** `feature/m6-tooling-last-good-test-662` at `60d7f6a5b2`, stacked on P1's `2174265e9c`, with the coordinator's tips merged in. Pushed, with upstream `origin/feature/m6-tooling-last-good-test-662`.
- **`reviewed-at`:** `60d7f6a5b2`, the branch `HEAD` at stage A, beside the read hash `8ebaf8daad`. `git diff --stat 8ebaf8daad 60d7f6a5b2 -- tools/last-good-scripts-test` is empty.
- **Temp roots:** `TMPDIR=/workspace/tmp/m6-t15/tmp`; outputs under `.qa-scratch/t15/` (gitignored) and `/workspace/tmp/m6-t15/`.

## [Stage A] 00:22 UTC — the first commands, the host, and the runs started

### The brief's first commands
- `git fetch origin` and `git fetch upstream --no-tags`: rc 0.
- **The branch:** `feature/m6-tooling-last-good-test-662`, stacked on P1, with `docs/reviews/inventory.json` present.
- **The rules:** `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` lists exactly the dispatch's eight paths (8 files, +127/-11), nothing else.
- **The host file's last line,** `/tmp/m7-m6-host-coordination-20261023.txt`: *M6 coordinator, 2026-10-25 00:09 UTC: GRANT to M7: one 2 GiB / 4 CPU / no-NIC VM window for the focused lifecycle regression ...*. That is M7's window, which this lane does not touch. **The live census** (`pgrep -x qemu-system-x86 -r R,S,D,T | wc -l`): **0**.
- **`/tmp`'s inodes:** 41 % used. Nothing is exported under `/tmp`.
- **The file at the hash:** `git show 8ebaf8daad:tools/last-good-scripts-test | wc -l -c` gives **14238 1167697**, and `git diff --stat 8ebaf8daad HEAD -- tools/last-good-scripts-test` is empty.
- **The two M7 roots carrying a GENERIC_X64 image busybox:** `m7-pixelelated-replacement20` and `m7-signin-build-20261022-07` (both `build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/busybox`).
- `tools/rules-check --quiet`: rc 0. `tools/register-check`: `679 IDs, each once; every citation in the live documents names a row`.
- `git push -u origin feature/m6-tooling-last-good-test-662`: done.

### The runs, started 00:23:16 UTC
- **The runner:** `tools/t15-stage-a.sh` in this folder runs the brief's § 5 block in its order: the image's busybox, the host's, then the twelve `--old` recipes under the image's. Every run starts through `vm-qa:158`'s `python3 -c` launcher (SIGINT and SIGPIPE to default, then exec). It is one background job, its exit delivered to the session by the harness.
- **The root:** `QA_SYSTEM_ROOT=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system`, read only: `BusyBox v1.36.1 (2026-10-05 03:37:19 UTC)`, BUILD_ID `"069fc270442134fe771258418adf4e666e0473fb"` (its `etc/os-release`).
- **The image run's first output line:** `signals: SigIgn=0000000001000004 SIGINT ignored=0 SIGPIPE ignored=0`. Its banner: `sed/mv/cp/tr/head/wc/cut/awk: BusyBox v1.36.1 (2026-10-05 03:37:19 UTC) multi-call binary. -- a copy of /workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/...`.

### [Stage A] 00:35 UTC — run 1 back: the image's busybox passes; the coordinator's ten sorted

- **The coordinator's rulings on #662:** 00:27, keep 34 section rows for Coverage and Q6, plus a sub-group table under Q6; 00:33, that table covers every group carrying verdicts: `x`'s `F1.`/`C.`/`D.`, `y`'s `y1`-`y4`, `A.`, `F1r.` and `CF.`, and `z`'s `S315.` and `S3F.`. `y1` to `y4` are comment headings (`:7799`, `:8397`, `:8607`, `:8684`), never echoed, so a run's output cannot name them; their verdicts are mapped by line range.
- **Run 1, the image's busybox** (`QA_SYSTEM_ROOT` on `m7-signin-build-20261022-07`): **rc 0, 517 s, 1,313 PASS, 0 FAIL, 0 SKIP**, last line `PASSED`.
  - First line: `signals: SigIgn=0000000001000004 SIGINT ignored=0 SIGPIPE ignored=0`.
  - Banner: `... BusyBox v1.36.1 (2026-10-05 03:37:19 UTC) multi-call binary. -- a copy of /workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/...`.
  - Before `PASSED`: `1 HISTORICAL FEATURE GROUP(S) NOT APPLICABLE -- no checks counted as PASS`, the fourth verdict word, exiting 0.
- **The coordinator's ten image-run FAILs are the fixture's, not the tree's.**
  - The coordinator ran the same bytes from `/workspace/tmp/m6-coordinator/t15-hash/tree`, an export with **no `.git`** (read only: its `run-image.out` lines 428-431, 524-525 and 1150-1156). This lane's run is from the worktree, `.git` present, and all ten pass.
  - **The mechanism:** the `F1.` and `F1r.` fixtures read earlier builds' quirks from git (`F1_PREV=417dcd8610` `:3200`, `73b20caf86`) through `f1_tree_at` (`:3274`): `git -C "${ROOT}" ls-tree ... 2>/dev/null | while ...; do git show ... || { ...; exit 2; }; done`. Without `.git` the `ls-tree` fails silently: stderr is dropped, and a pipeline's first stage has no `pipefail`. The loop never runs, and its `exit 2` is in the pipeline's subshell, so it could not end the run anyway.
  - The `C.` group's repair fixture reads `git show 417dcd8610:.../mupen64plus.cfg > spliced.cfg 2>/dev/null` (`:4271`) the same way.
  - **What caught them:** each fixture came up empty, and the file's own vacuity detectors fired (*the fixture proves nothing*, *the downgrade wrote 0 file(s)*, *the repair changed: 'nothing'*). The guard held downstream, while the read itself fails open: a Q2 item.

### [Stage A] 01:10 UTC — run 2 and the twelve `--old` recipes back (the runner ended 01:06:41, `runner rc 0`)

- **The coordinator's 00:36 ruling (#662):** the fail-open history read (`f1_tree_at`'s pipeline `exit 2`; `:4271`'s `2>/dev/null`) is a bug for stage D. The worktree run's 1,313/0/0 is the tree's baseline.
- **Run 2, the host's busybox** (`QA_SYSTEM_ROOT` unset): **rc 1, 677 s, 994 PASS, 319 FAIL, 0 SKIP**, last line `319 CHECK(S) FAILED, 0 SKIPPED`.
  - First line: `signals: SigIgn=0000000001000004 SIGINT ignored=0 SIGPIPE ignored=0`.
  - Banner: `sed/mv/cp/tr/head/wc/cut/awk: BusyBox v1.37.0 (Ubuntu 1:1.37.0-7ubuntu1) multi-call binary. -- a copy of /usr/bin/busybox`. Stream A's `rclone:` line names the host's `/usr/bin/rclone`, **v1.60.1-DEV** (`rclone version`), against the recipe's 1.75.2.
- **The busybox diff:** both runs count 1,313 checks in the same order, so the pairs align by position, and every PASS/PASS pair's text matches.
  - **319 checks flip, all PASS under the image's and FAIL under the host's** (one more pair differs only because its text carries a literal tab), #1015's count exactly.
  - By section and group: `y/A` 95, `y` (`y1`-`y4`) 59, `t` 42, `x/D` 33, `y/CF` 26, `z` 24, `z/S315` 12, `k` 11, `n` 7, `af` 6, `ad` 4.
  - **`flock` is the only missing applet the run names:** 150 `flock: applet not found` lines; the suite's `flock` shims (`n` `:1484`, `t` `:2097`, `y` `:7811`, stream A `:8983`) exec a busybox without it. 61 of the flips print it, and 127 more show its consequence (rc 75, *another sync is already running*, a lock). The other 131 are not yet attributable by text. Stream A also ran on rclone 1.60.1, so two attribution runs follow (below).
- **The twelve `--old` recipes, under the image's busybox: every one exits 2, and none reaches the verdict.**

| `BASE_REF` | rc | wall | PASS | FAIL | where it stopped |
| --- | ---: | ---: | ---: | ---: | --- |
| `1d1503180d` (default) | 2 | 211 s | 73 | 118 | `s`: `rocknix-evidence` is not at the ref |
| `53f390b1e9` | 2 | 156 s | 123 | 116 | `x`: `rocknix-corekeep` is not at the ref |
| `c15050c897` | 2 | 213 s | 88 | 103 | `s`: `rocknix-evidence` |
| `8707919349` | 2 | 156 s | 161 | 78 | `x`: `rocknix-corekeep` |
| `34aca64afd` | 2 | 70 s | 179 | 60 | `x`: `rocknix-corekeep` |
| `0f7785e6ed` | 2 | 0 s | 0 | 0 | at once: `fatal: invalid object name '0f7785e6ed'` |
| `d79281066c` | 2 | 0 s | 0 | 0 | at once: `fatal: invalid object name 'd79281066c'` |
| `cee1656c33` | 2 | 133 s | 256 | 90 | `x`: `rocknix-corekeep` |
| `28a80357ed` | 2 | 114 s | 218 | 122 | `x`: `rocknix-corekeep` |
| `3387cf5da0` | 2 | 118 s | 264 | 85 | `x`: `rocknix-corekeep` |
| `655f103cc5` | 2 | 121 s | 267 | 82 | `x`: `rocknix-corekeep` |
| `70b6c70ca7` | 2 | 119 s | 296 | 71 | `x`: `rocknix-corekeep` |

- **Why every recipe stops:** `src_of` (`:320-325`) exits 2 for the whole run when a script is absent at `BASE_REF`. So every section from the first script a ref predates onward never runs as a control: `s` to `ah`, or `x` to `ah`.
- **The two dead refs** exist nowhere in the repository (`git cat-file -t`: *Not a valid object name*; no branch contains them). They were written into the header by `1a5c066623` (#166) and `67a89cb623` (#173), so they most likely named commits a later history rewrite replaced. **q's and p's pending/flushed controls cannot run.**
- **The promises against what fired before each stop (FAILs per section):**
  - **Fired:** `1d1503180d` (`a` 9, `b` 7, `c` 4, `d` 9, `e` 1, `f` 5, `j` 4, `k` 19, `l` 14, `m` 17), `53f390b1e9` (`k` 17, `l` 14, `m` 17), `c15050c897` (`a` 10), `8707919349` (`h` 3, `n` 7, `o` 5), `28a80357ed` (`r` 6, `s` 7), `655f103cc5` (`u` 19 of its 19, `v` 2).
  - **`34aca64afd`:** `k` 8, four naming the proxy; `p` 1, *raofflineproxy-ctl is absent at 34aca64afd*.
  - **`cee1656c33`:** `p` 5, `r` 2 (the promise says *three* PL-29 canaries; two FAIL lines carry the planted values), `t` 44.
  - **`3387cf5da0`:** `t` 46, three FAIL texts naming the helper's verdict and stamp.
  - **`70b6c70ca7`: the promised control does not fire as promised.** `t`'s client-predicate block cannot build the client at that ref: the tree's patches `003` to `006` *do not apply to the pinned client* ("1 out of 4 hunks FAILED"). So `t`'s 43 FAILs are patch-application failures, and **none of the five `012` checks runs** (0 lines name `012`, against 5 PASS in the baseline).
- **A slip of mine:** one command wrote `t-img.txt` into the session's scratchpad, which is under `/tmp`, and the brief forbids any write there. It was listed and removed at once. Every T15 scratch file now goes under `/workspace/tmp/m6-t15/`.
- **Attribution runs, started 01:2x UTC:** two constructed roots under `/workspace/tmp/m6-t15/roots/`, each swapping one dependency of the host run: `bbhost` (the host's busybox with the image's rclone) and `rchost` (the image's busybox with the host's rclone), each with the M7 image's avahi unit and os-release beside it. Then a timed image run for Q5. The runner is `tools/t15-attribution.sh`.

### [Stage A] 01:39 UTC — the attribution runs and the timed run back (`tools/t15-attribution.sh`, 01:09:56 to 01:38:21, `runner rc 0`)

- **`bbhost`** (the host's BusyBox 1.37.0 with the image's rclone v1.75.2, `QA_SYSTEM_ROOT=/workspace/tmp/m6-t15/roots/bbhost/image/system`): **rc 1, 678 s, 994 PASS / 319 FAIL / 0 SKIP**, `SIGINT ignored=0`. Its 1,313 verdicts equal the host run's, check for check (`diff`, 0 lines).
- **`rchost`** (the image's BusyBox 1.36.1 with the host's rclone v1.60.1-DEV): **rc 0, 512 s, 1,313 / 0 / 0**, `PASSED`. Its verdicts equal the image run's (0 lines).
- **So every one of the 319 flips is the busybox's, and the rclone's version changes no verdict.** Stream A's cases, written as *the cloud scripts against the image's rclone* (`:8906`), pass unchanged under an rclone of 1.60.1 against the pin's 1.75.2. That is a Q4 finding and a Q3 lead: nothing in them distinguishes the version they claim to need.
- **Which applet:** `flock` is the only refusal any output names. 61 FAIL lines carry `flock: applet not found`, some several times (150 occurrences in all), and the image run has none. No `unrecognized`, `invalid` or `unknown option`, `not supported` or `Usage:` appears in either run. The other 131 flips show no applet error of their own. **That `flock` causes all 319 is not proven:** a 1.37 applet that behaves differently without erroring would read the same.
- **The timed image run** (each line stamped with the seconds since its start): rc 0, 515 s, `PASSED`. Wall time by section: `y` 248.3 s, `x` 82.1 s, `n` 41.6 s, `af` 33.7 s, `t` 33.6 s, `ae` 19.8 s, `z` 17.4 s, `i` 14.3 s, `h` 6.3 s, `b` 2.9 s, `ad` 2.7 s, `q` 2.2 s, `p` 1.6 s, `ab` 1.4 s, `s` 1.3 s, `k` 1.0 s, `m` 0.6 s, `f` 0.6 s, `u` 0.5 s, `j` 0.5 s, `d` 0.4 s, `ag` 0.4 s, `a` 0.4 s, `v` 0.3 s, `w` 0.2 s, `l` 0.2 s, `c` 0.2 s, `r` 0.1 s, `o` 0.1 s, `e` 0.1 s, `ah` 0.1 s, `ac` 0.1 s, `g` 0.0 s. By group: `x/F1` 4.9 s, `x/C` 45.3 s, `x/D` 31.7 s, `y/A` 137.2 s, `y/F1r` 8.8 s, `y/CF` 65.9 s, `z/S315` 9.1 s, `z/S3F` 0.3 s. `y`'s `y1`-`y4` take 248.3 - 137.2 - 8.8 - 65.9 = 36.4 s.
- **The wrong busybox's cost:** 677 s (the host run) and 678 s (`bbhost`), against 515 s, to a verdict about the host's applets: 162 s more, and 319 FAILs that say nothing about the tree.

### [Stage B] 01:50 UTC — a line-number correction; the section reads under way

- **Correction of mine:** `f1_tree_at` is at **`:3205-3215`**: the `ls-tree ... 2>/dev/null` at `:3208`, the `exit 2` inside the pipeline at `:3209`. `:3274` is inside `f1_pass` (`:3273`). The 00:3x entry above and the 00:35 post on #662 said `:3274`. The line was wrong; the finding (the fail-open history read, ruled a bug at 00:36) is unchanged. Found by the section-`x` read agent and re-derived by `grep -n '^f1_tree_at()'`.
- **The section reads:** three read-only agents, `a`-`w` with `aa`-`ah`, `x`, and `y`-`z`, read their spans for Q6's columns and Q3. Each lead is re-derived from the lines before it enters `04`. Two have reported.

## [Stage B] 01:59 UTC — 03 and 04 written (`c4a7e98509`)

- **The three read-only agents reported:** `a`-`w` with `aa`-`ah`, `x`, and `y`-`z`. Their leads are kept in scratch notes. Those marked *re-derived* in `04` were read from their lines by the lane: `:3051`, `:13826`, `:1842`, `:548`, `:845-851`, `:6488-6492`, `:6762-6765`, `:4279-4283`, `:8581-8584` and `:13421-13424`, plus `f1_tree_at`'s place.
- **`04`:** findings F-01 to F-21 (2 High, 10 Medium, 9 Low), each with its line; § 4.5 by artifact; the renovation face Q1 to Q7.
  - **Q6:** the 34-row brittleness table, and **15** sub-group rows. The coordinator's 00:33 list named twelve, and the `y`-`z` read found three more comment-headed groups that carry verdicts: D-fix `:12094`, F2-20..24 `:12344` and A-fix `:12605`, included under the same ruling.
  - **The split proposal**, as a lead.
- **`03`:** § 3.1 to § 3.5, the seams. One claim was corrected before the commit: #1015 had already suspected host tools (its title), so it did not read the FAILs as the tree's.
- **Two counts of mine corrected before the commit:** sections `x` to `ah` hold **933** checks, not 948 (`02` and `04`); stream A makes 143 `sa_run` calls, and 145 is all of `y`'s.
- **The S3F canaries** write to the host's `/tmp/s3f-*` only if their guard fails. No `/tmp/s3f-*` exists after this lane's runs (`ls`).

## [Stage C] 02:03 UTC — the seat: the Facilitator, the packet, its scan, the probe, the refutation started

- `npm install --prefix tools/council`: rc 0 (it warned that install scripts were not run). `tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.` `tools/council/run test`: rc 0, with 39/39, 127/127 and 19/19 passing and 0 failing. `run` sources `~/.config/council/env` itself; the file was not read here.
- **The packet** (`tools/t15-packet.py`, the manifest `second-opinions/packet-manifest.json`), built from excerpts because the file is 1,167,697 bytes (its sha256 is in the manifest):
  - the section index and the groups;
  - **13 excerpts, 1,484 lines**, each line-numbered at `8ebaf8daad` and hashed: the harness `:1-430`, `a`, `b`, `q`, `t`'s patch block and verdict reading, `v`, the `F1.` history helpers `:3198-3330`, the `:4255-4290` repair, `y4`, stream A's setup and sandbox helpers `:8895-9032`, `aa`'s two-argument check, and the call sites and verdict `:14177-14239`;
  - `02`, `03` and `04` whole;
  - `engineering-practices.md` § Guards must fail closed and `upgrade-and-install.md` § Verify on a device, from `next`.
  - **Sizes:** the body is 255,869 bytes. `gpt-brief.md`, the ask plus the body, is 258790 bytes, sha256 `e0940e387dd33cfc05841543f97d1567fd4335389ddfe192b3a1433f2e058c7c`. The ask puts the brief's five questions first and offers a second packet: the seat names the sections it needs under `## Sections I need`.
- **The packet's scan, before it was sent:**
  - `tools/forbidden-terms-check --stdin`: `0 hits on stdin`.
  - **A slip of mine:** my first credential scan used `grep -E -f .githooks/secret-patterns`, which errors (`Unmatched (`, line 6), because that file is a shell assignment, not a pattern list. Its "0" proved nothing, and was discarded. The rescan sources each file as `guard_load` does, checks that the pattern compiles, and greps with it. Result: **0 lines under three pattern sets** (this branch's, the primary checkout's, and T10's at `feature/m6-tooling-guards-657`). **Each was seen to fire** on a credential-shaped line built at run time on stdin (1, 1, 1).
  - **The `:8004` fixture literal (#962)** is not carried: it lies outside every excerpt, so no redaction was needed.
- **The probe**, 02:02:31 to 02:02:39Z, `--member gpt --provider openrouter`: served `openai/gpt-6-astra` by `OpenAI`, effort `max` (297 reasoning tokens). Verification PASS, effort PASS (`reasoning_tokens`), provider PASS (`response_provider_field`). The reply was `READY unknown`.
- **The refutation** started at 02:02:52Z with `--per-attempt-timeout-ms 3600000 --total-timeout-ms 10800000`, logging to `/workspace/tmp/m6-t15/audit.log`.
  - **What watches it:** the harness background task running it, which delivers its end.
  - **Its silent mode:** a hung seat is ended only by those timeouts. The failed-seat rule holds: hold, diagnose, one same-slug retry on a transient cause.

## [Stage C] 02:17 UTC — the seat's first reply; the second packet it asked for

- **The refutation returned** (`/workspace/tmp/m6-t15/audit.log`): 02:02:52Z to 02:15:31Z, attempt 1 of 4, `finish=stop`, 16,359 bytes of content (the file is 16,578), 759,660 ms, 0 retries.
  - **Served:** `openai/gpt-6-astra` by OpenAI at `max` (33,590 reasoning tokens); verification, effort and provider PASS (`gpt-audit.md.provenance.json`).
  - **Scanned before it was read:** `forbidden-terms-check --stdin` 0 hits, and 0 credential-pattern lines under the three sets.
- **What it said, in outline:**
  - its five answers;
  - F-01 to F-21 graded: 5 confirmed, 10 confirmed with narrowing, 1 refuted (F-08), and 5 *cannot tell from the packet* (F-07, F-09, F-17, F-19, F-21);
  - four new findings, G-01 to G-04;
  - two corrections to the first reader's Q3: `:3329` does not pass on an empty `F1_WROTE` (the here-string makes one empty line, so `F1_LEFT` is non-empty and the check FAILs), and `:3053`'s `sa` statuses are all in the `&&` chain, so only `:3061-3062` drops one.
  - Under `## Sections I need`, it asked for 14 ranges and the two callee tools.
- **Re-derived by the lane at their lines** (`sed -n`): the two corrections (`:3326-3329`, `:3053`, `:3061-3062`), both right, and G-01 (`:522`, `:536-541`), G-02 (`:14224` `${ROOT}` against `:14231` `${HARNESS_ROOT}`), G-03 (`:1781-1789`, `find` in `${ROOT}`) and G-04 (`:8854-8860`, ordering by `sleep 1`), all four confirmed.
- **The second packet** (`tools/t15-packet2.py`, `second-opinions/packet2-manifest.json`):
  - **What it carries:** the 14 ranges the seat named (1,839 lines) at `8ebaf8daad`; `settings-modes-test` and `melonds-upgrade-test` whole at `8ebaf8daad` and at T14's `7c1d729b57`; the seat's first reply; and the first packet whole.
  - **Size:** `gpt-brief2.md` is 479,112 bytes.
  - **Scanned before it was sent:** 0 hits; 0 credential lines under the three sets; `:8004` not carried.
  - **Sent** at 02:16:37Z, with the same timeouts. The harness background task delivers its end.

## [Stage C] 02:26 UTC — the second reply; the grading; the coordinator's 02:24 ruling

- **The coordinator's answer (02:24 UTC; its session had been down from 00:45 to 02:20):** all three `--old` items are bugs of this file.
  - The two dead refs are fixed to `717bc04449` and `51e2acece6`, proven by running.
  - `src_of`'s whole-run exit 2 under `--old` becomes NOT APPLICABLE per section, and the run goes on.
  - `70b6c70ca7`'s `t`: pin the client build, or retire the recipe with the reason.
  - They are filed at stage D.
- **The second reply** (`/workspace/tmp/m6-t15/audit2.log`): 02:16:37Z to 02:24:14Z, attempt 1 of 4, `finish=stop`, 6,815 bytes of content (the file is 6,961), 457,661 ms. Served `openai/gpt-6-astra` by OpenAI at `max` (21,576 reasoning tokens); verification, effort and provider PASS. Scanned before it was read: 0 hits and 0 credential lines.
- **The grading** (`04` § Second opinion):
  - **The 21 findings:** 7 confirmed, 13 confirmed with narrowing, and 1 refuted. F-08 is **withdrawn**: `NOT APPLICABLE` marks a retirement and is not counted as a pass (`:14235`); the fragile gate behind it is G-05.
  - **G-01 to G-10** were added by the seat. Each was re-derived by the lane at its lines (`:522`/`:536-541`, `:14224`/`:14231`, `:1781-1789`, `:8852-8860`, `:4553-4559`, `:7320-7357`, `:10326-10333`, `:7771-7776`, `:14224-14233`/`:310`), and all were accepted.
  - **Two Q3 errors of the first reader are corrected:** `:3329` (agent 2's lead) and `:3053`.
- **One tension, recorded and not resolved here:** the seat argues against a blanket per-section NOT APPLICABLE for F-05. Its distinctions: an invalid ref → CANNOT; an absent historical feature → a presence-contract FAIL; an unrelated newer section → not applicable; a selected check that cannot run → incomplete, never PASS. The coordinator's 02:24 ruling sets the fix as NOT APPLICABLE per section. The ruling governs; the seat's distinctions go into that bug's acceptance as a lead.
- **`review-plan.json`** is set complete, recording both calls and the second packet.

## [Stage D] 02:30 UTC — the punch list, the bugs, the audit issue; the stage-D pause

- **`05`,** generated by `tools/t15-punch.py` from one list: **24 items, 0 Critical, 2 High, 13 Medium and 9 Low.**
  - **22 bugs.** Defects of one shape were grouped: F-01 with F-20 (PL-01); F-07 with G-10 (PL-02); G-04 with G-08 (PL-14); F-13, F-14, G-03, G-05 and G-09 (PL-19); F-19 with G-07 (PL-20).
  - **Two leads for the coordinator:** PL-23 (the rules' and index's descriptions) and PL-24 (the split).
  - **F-08** was withdrawn after the seat's refutation.
- **The lint:** `tools/lint-audit-artifacts <folder> --phase pre-issue` gives `PASS pre-issue artifacts`, with *review plan: independent, 2 model perspectives, 1 verified external calls*. Its first run failed one check: my `review-plan.json` listed the second-packet call as a second `refutation` call, which the schema refuses (one refutation pass). It is now recorded as `continuations` of that pass, with its output and provenance named.
- **The bugs: #1018 to #1039,** filed with the label `bug` and milestone M6. Every body was scanned before filing: 0 listed words, and 0 credential lines under two pattern sets. Each passes `tools/box-check --issue N` with 0 fail.
- **The audit issue: #1040,** `Audit: M6 T15 the last-good scripts test -- 24 findings (0 critical, 2 high)`, labels `audit` and `punch-list`, milestone M6, **a sub-issue of #662** (read back). 24 checkboxes; `box-check --issue 1040` 0 fail.
- **No file under `tools/` was changed by this lane:** `git diff --stat 60d7f6a5b2 HEAD -- tools/` (since the dispatch tip) is empty. **A correction of mine:** I first wrote that `git diff --stat 8ebaf8daad HEAD -- tools/` is empty without running it. It prints 15 files, all inherited from the branch's base: P1's `renovation-inventory`, `renovation-drift` and `renovation-status`; the coordinator's `lint-audit-artifacts`, `register-check` and the lint fixtures (the dispatch lists `tools/lint-audit-artifacts` among its paths). Criterion 16's command reads that inherited diff; the lane's own is the one since `60d7f6a5b2`.
- **The stage-D pause** is posted on #662: the stream briefs are the coordinator's.

## [Stage E] 02:40 UTC — the stage-E dispatch; S1 begun

- **The coordinator's stage-E dispatch (02:36 UTC on #662):** the stream briefs are `docs/reviews/briefs/t15-streams.md` at `d717bac312`, read with `git show`, not merged; a copy is at `/workspace/tmp/m6-t15/t15-streams.md`.
  - **The two questions:** PL-06 takes the seat's three distinctions, and Q6 keeps 15 rows.
  - **The streams:** six, serial, with S1 first.
  - **The positives** come from a clone or a detached worktree, never `git archive`.
- **#1023's acceptance** was rewritten to the three distinctions under that ruling. `box-check --issue 1023`: 4 open checkboxes, 0 fail.
- **The stage-D export:** `git clone --shared --no-checkout` of the repository, checked out detached at `2eface0727`, at `/workspace/tmp/m6-t15/stageD`. It is not shallow, `417dcd8610` resolves, the file is at the hash, and no build root is beside it.
- **S1's first positive is running there:** the unfixed file with `QA_SYSTEM_ROOT` unset on purpose, its output in `/workspace/tmp/m6-t15/s1/unfixed-fallback.out`. The harness delivers its end.
- **#1018's fix, in the working tree:** `--host-diagnostic`; `BB_KIND` (root, build or host); refusal with exit 2 without a candidate; `HOST: ` on every result line under the flag; the G-B-15 probes judging the banner against the copy's and the source; the verdict's `tools:` line; `NOT DEVICE EVIDENCE` with exit 3.
  - **Its first refusal check:** the fixed file from the worktree with `QA_SYSTEM_ROOT` unset gives **rc 2 in 39 ms**, `CANNOT -- no candidate image's busybox ... (found: /usr/bin/busybox). Set QA_SYSTEM_ROOT=<a build root>/image/system, or run with --host-diagnostic ...`.
  - **Two slips of mine before it parsed:** a pattern that missed (nothing was written), and an apostrophe inside a `${...:-...}` word, which bash reads as a quote even within double quotes (`bash -n` caught it).
- **`/workspace/tmp/m6-t15/tmp/tsx-1000`** was left there at 02:24 by the Facilitator's `tsx`, run with that `TMPDIR` exported. It is not the suite's.

## [Stage E] 03:09 UTC — S1: #1018 fixed, with its positives

- **D-QA-063 (the coordinator, 02:42 UTC on #662, `d54b754da3`):** under `--host-diagnostic` the run exits 1 when any case failed and 3 only when none did, never 0. Every line is marked, and the verdict says NOT DEVICE EVIDENCE either way. The fix, `--help`, the refusal message and the header comment all say this. My first cut ended with exit 3 regardless, per the brief's sentence that D-QA-063 corrects.
- **The runs, one at a time** (the table is `02` § The streams' positives):
  - unfixed, from the export, no root: rc 1, 994 / 319, nothing naming the host;
  - fixed refusal: rc 2 in 26 ms;
  - fixed `--host-diagnostic`: rc 1, 994 / 319, all 1,313 lines `HOST:`;
  - the two cut-copy positives: rc 3 with no failing case, rc 1 with one injected;
  - fixed under the M7 root: **rc 0, 1,313 / 0 / 0**, with the verdict naming `source: root, BUILD_ID 069fc2704421...`.
- **The suite under the root after #1018: 1,313 / 0 / 0**, equal to the baseline. Neither the fix nor the G-B-15 probes' new source condition changed any verdict under a root.
- **The brief's "329" is 319** for a clone with history. The ten are #1021's export case.

## [Stage E] 03:22 UTC — S1: #1020 fixed, with its positive

- **The coordinator's 03:11 ruling (a)** on #662: a root whose rclone is missing, or not the recipe's `PKG_VERSION` read through `src_of`, is CANNOT before section `a`, exit 2, naming both versions and the two ways out. Under `--host-diagnostic` the host's rclone runs marked, with its version in the verdict.
- **The fix:**
  - the rclone is the busybox's own root's (`${BB_SRC%/usr/bin/busybox}/usr/bin/rclone`), resolved and checked once, right after the busybox;
  - stream A uses it rather than a second `image_tool_source` search;
  - the verdict's second `tools:` line names it, its version and the recipe's;
  - the header, `--help` and stream A's comment say so.
- **The runs, one at a time** (the table is `02` § S1, #1020):
  - unfixed (`3037ce6b8c`, a clone) under `rchost`: **rc 0, PASSED, 1,313 / 0**, with the verdict claiming the M7 BUILD_ID over the host's rclone 1.60.1-DEV;
  - fixed under `rchost`: rc 2 in 47 ms;
  - fixed `--old` at `417dcd8610` under the M7 root: rc 2 (the ref's recipe says 1.75.1);
  - cut copies: rc 3 under `--host-diagnostic`, rc 0 under the M7 root;
  - **fixed full suite under the M7 root: rc 0 in 522 s, 1,313 / 0 / 0**, both provenance lines.
- **The `--old` consequence:** every positive ref pins rclone 1.75.1 and every GENERIC_X64 root here carries 1.75.2, so no `--old` run reaches a verdict on this host. Put to the coordinator with the checkpoint, since S2 proves #1022/#1023 with `--old` runs.
- **Coordinator, 03:16:** D-WORKFLOW-206/207 are reserved for the M7 lane; a row from this slice takes D-WORKFLOW-208+, D-QA-064 or D-INFRA-032. None is planned.

## [Stage E] 03:55 UTC — S1: #1029 and #1038 fixed; the 03:34 `--old` ruling

- **The coordinator's 03:34 ruling on `--old` (#662): option (2), made precise per tool.**
  - Under `--old` only, each tool borrowed from the root (rclone, busybox) is read against the ref's recipe. A match is evidence.
  - A mismatch is named on the banner and the `tools:` line, and the sections that tool judges count as unverified: stream A for rclone, every section for busybox.
  - The exit follows D-QA-063.
  - Outside `--old`, the 03:11 CANNOT stands.
  - Option (3), a root of a 1.75.1 ref, goes into `04` as what would turn those 3s into 0s.
  - This lands in S2, with #1022/#1023.
- **#1029:** section `b` binds the busybox and 28 applet wrappers, and a probe in the sandbox checks each one. **#1038:** PL-022 runs only on a root's or build's busybox; otherwise it is a counted SKIP. Table: `02` § S1, #1029 and #1038.
- **The runs:**
  - the probe with `b`'s old sandbox: rc 1, 0 of 28 (the positive);
  - with the binding: rc 0, 28 of 28;
  - unfixed host run's PL-022: PASS "the image's" on the host's 1.37.0 (the positive);
  - fixed `--host-diagnostic`: rc 1, 985 / 325 / 1 SKIP;
  - **fixed under the M7 root: rc 0, 1,314 / 0 / 0.**
- **My count slip:** I first estimated that PL-022's block was 5 checks. It is 4, and the line-by-line diff of the two host runs reconciles exactly (`02`).
- **The host run's new FAILs in `b`** are backuptool's lock with no `flock` applet: section `b` now judges the busybox it is given, as the other flock-using sections already did. Not a script bug; the host's busybox lacks the applet.
- **Coordinator, 03:43:** D-WORKFLOW-206 to 208 are the M7 lane's; a row from this slice takes D-WORKFLOW-209+, D-QA-064 or D-INFRA-032.

## [Stage E] 04:07 UTC — S1: #1019 fixed; S1 complete

- **The coordinator's 03:58 ruling:**
  - (a): a child's CANNOT/UNVERIFIED gives 3 with no FAIL, counted and named;
  - the `ag` move to `HARNESS_ROOT` is approved, with the `--old` sentence beside it.
- **The runs** (the table is `02` § S1, #1019):
  - the unfixed cut copy with T14's tools: both children refuse the run's copy and read FAIL, rc 1 (the positive);
  - the doubles: both flattened to FAIL (the positive);
  - fixed with T14's tools: **rc 0**, both PASS, `declared from 069fc2704421...`;
  - fixed with the doubles: rc 3, CANNOT and UNVERIFIED named;
  - `--host-diagnostic`: rc 3, both unverified.
- **S1's end, the full suite under the M7 root at this branch: rc 3, 1,312 / 0 / 0 / 2 CANNOT.** This branch's copies of the two writer tests predate T14's `--busybox-from` (`unrecognized arguments`). With T14 merged, they are the cut copy's two PASSes and the run is 1,314 / 0 / 0. That merge is the coordinator's (T14 merges before this branch).
- **S1's five bugs** (#1018, #1020, #1029, #1038, #1019) are fixed in four commits. Next is S2: #1021-#1024, #1035, #1039, with the 03:34 `--old` per-tool ruling.
- **One edit after the end-of-S1 run:** the comment beside the `ag` move gained the coordinator's `--old` sentence. It is comment only; `bash -n` passes, and no line that runs changed.

## [Stage E] 04:08 UTC — #1030's positive, its fix already in #1019's commit

- **`3da816ce24` (#1019) already moved `ag`'s tool to `HARNESS_ROOT`, which is #1030's whole fix** (S6). The coordinator approved the move at 03:58. I made it as part of #1019 before noticing #1030 is its own bug.
- **Its positive** (the table is `02` § S6, #1030): with `LAST_GOOD_SOURCE_ROOT` naming a checkout without the tool, the unfixed `ag` gives `No such file or directory` and FAIL (rc 1); the fixed one PASSes (rc 0).
- **S6 therefore has no code commit left.** Put to the coordinator with the S1 checkpoint.

## [Stage E] 04:33 UTC — S2: #1023 fixed (the --old verdict); the coordinator's 04:12 answers

- **The coordinator, 04:12:**
  - S6 (#1030) is closed by `3da816ce24` with its positive, and a Phase 7 row will cite it;
  - #1021's positive comes from a `git clone --depth 1` of the tip: a constructed input, which the rule against `git archive` (about figures) does not cover.
- **#1023:**
  - an invalid ref is CANNOT at once;
  - a script absent at the ref is a promised FAIL, or NOT APPLICABLE by name from that point in its section, or CANNOT before any section;
  - the recipes are data (`old_promises`), and the verdict lists the promises that fired;
  - each borrowed tool is checked against the ref's recipe, and a mismatch is unverified (the 03:34 ruling);
  - the 34 banners go through `section()`, with identical output.
- **Runs:**
  - the invalid refs: CANNOT in about 10 ms;
  - **`--old 1d1503180d`: exit 1 in 1,219 s, a verdict where the unfixed file exited 2 at `s`**: all ten promises fired; `s x y z ab` N/A by name (654 checks); rclone v1.75.2 against the ref's v1.75.0 unverified; busybox v1.36.1 matched.
- **Busybox and rclone at the refs:** the busybox override says 1.36.1 at every ref the suite names, so under `--old` busybox is evidence. Rclone says 1.75.0 (the twelve) or 1.75.1 (the in-section positives), so stream A is unverified at each.

## [Stage E] 05:32 UTC — S2's code complete; the run queue stopped for M7's build window

- **S2's code commits:**
  - #1023 `5a155ed7fc`;
  - #1022 `bea0374f3b`;
  - #1021 `70af8e3771`;
  - #1035 `1dbb668bb2`;
  - #1024 `4bc40d7733`: the client's pin through `subj`, so `70b6c70ca7`'s `t` builds its own client (`64d03d3063...`, in the sources cache);
  - #1039 `a286e5b49f`: the header's 34 claims and positives, `--help`'s `--old` line, and the SIGINT advice.
  - #1022, #1021, #1035 and #1024 were committed with their runs in flight, each message saying so.
- **#1039's positive:** under a parent ignoring SIGINT, the unfixed refusal advises `setsid -f`, and `setsid -w` under such a parent still refuses (rc 2). The fixed refusal names a launcher that resets SIGINT.
- **#1024's record, corrected:** stage A's `t` at `70b6c70ca7` had 43 FAIL and 21 PASS. Five of the FAILs are patches 003, 004, 005, 006 and 009 not applying; the rest follow from the unbuilt client; and no line in `t` names `012`. The commit message's *"43 FAILs were patch failures"* overstated that; the issue's own wording was the source.
- **#1023's second case (`--old 34aca64afd`, from a clone at `5a155ed7fc`): exit 1 in 1,189 s**, 233 PASS / 265 FAIL / 637 N/A / 26 SKIP / 2 CANNOT. `p`: `FAIL  raofflineproxy-ctl is absent at 34aca64afd: the toggle had no backend`. Both promises fired (`k p`); `x y z ab` were N/A by name; rclone v1.75.2 against v1.75.0 was unverified. The unfixed file stopped at `x`, exit 2 (stage A).
- **The M7 lane, about 05:25:** its donor-cache move was blocked by T15 shells naming the `m7-signin-build-20261022-07` root, and M6 had granted M7 the build window at 05:22.
  - The five PIDs it named were all mine (host PID namespace `4026531836`): one running suite (`--old 717bc04449`, process group 3674113) and four waiters that would each have started a suite on that root.
  - Stopped by PID at 05:30 (SIGTERM): the waiters and their `sleep`s, the outer shell 2555091, and group 3674113.
  - Readback at 05:31: no process with that root in `QA_SYSTEM_ROOT`, as its working directory, or open; no suite, `bwrap` or `cloud_capture` left; the killed run's scratch removed by its EXIT trap.
  - Reported to M6 on #662. The `/tmp` handoff file was not written: this lane writes nothing under `/tmp`.
- **To re-run after the window, serial, about five hours:**
  - #1022's `717bc04449` and `51e2acece6`;
  - #1021's two `--depth` clones;
  - #1035's `g`/`h`/`i` cuts;
  - #1024's `t` cut;
  - the twelve recipes and the root run at `a286e5b49f`.
  - Which root to resume on was put to M6.
- **The register:** D-WORKFLOW-206 to 209 and D-INFRA-032 are reserved for the M7 lane (the coordinator, 03:16, 03:43 and 04:46). A row from this slice takes D-WORKFLOW-210+, D-QA-064 or D-INFRA-033+.
- **05:42, the M7 lane:** the `069fc2704421` cache moves permanently (to `m7-signin-generic-build-20261025-01`, becoming `bcc`), so option (a) is gone. Its pipeline does not move or build `m7-pixelelated-replacement20`, whose root reads `BUILD_ID 1a026648442321609b2288c2c9c06803817f9df2`, busybox v1.36.1 with the same 2026-10-05 03:37:19 build stamp, and rclone v1.75.2 (read, nothing run). Put to M6 on #662: (b) `replacement20`, or (c) M7's new root when released. T15 holds to source edits until M6 assigns one.

## [Stage E] 05:39 UTC — the root changes to M6's donor; the serial runs resume

- **The coordinator's 05:38 ruling (#662):** every remaining and re-run T15 run uses `QA_SYSTEM_ROOT=/workspace/artifacts/m6-donor/1a0266484423/image/system`, M6's own retained donor, copied byte-equal from `m7-pixelelated-replacement20`'s root. No M6 run sets `QA_SYSTEM_ROOT` under `/workspace/repos/rocknix.worktrees/` again. The root change is in `02` § The runs, *The root changes*.
- **Verified at the lane's start:** `sha256sum -c ../../SHA256SUMS` from `image/system`: busybox, rclone and os-release OK; 146 applet links; busybox `79e7b20ddbe5...`, 574456 bytes, v1.36.1 built 2026-10-05 03:37:19 UTC; rclone v1.75.2; BUILD_ID `1a026648442321609b2288c2c9c06803817f9df2`.
- **The host file** (`/tmp/m7-m6-host-coordination-20261023.txt`, read only) has no `PAUSE T15` line. Census: `cc1plus` 4, qemu 0, load 5.69. The M7 lane's `bcc866f1` GENERIC build runs beside these runs (granted 05:22), so each run's wall time is read beside its census.
- **The order, one at a time:**
  1. the full root run at S2's tip (`a286e5b49f`), the baseline on the donor;
  2. #1021's `shallow-unfixed` (`bea0374f3b`, `--depth 2`) and `shallow-fixed` (`70af8e3771`, `--depth 1`);
  3. the twelve recipes at the tip.
- **The twelve at the tip carry the fixed sides of #1022** (`717bc04449`, `51e2acece6`), **#1035** (`g` and `i` under `1d1503180d`) **and #1024** (`t` under `70b6c70ca7`). So the separate cut runs at earlier commits are dropped as duplicates. The unfixed sides are the records already made: stage A's `--old` outputs, and #1023's `1d1503180d` run at `5a155ed7fc` (`g` 6 PASS, `i` 6 PASS, on the `069fc` root).
- **Each step checks the host file for `PAUSE T15` at its boundary,** and writes the census (`pgrep -c -x cc1plus`, `pgrep -c -x qemu-system-x86`, the load) before and after each run to `/workspace/tmp/m6-t15/s2/queue.log`. The queue's PIDs follow in this log once it is started.
- **The queue:** `/workspace/tmp/m6-t15/s2/queue.sh` on one background shell (the harness task `bwk8barpr`), queue PID **215160**. It started 05:40:35, and its first run, root-tip, is PID **215185**. Each run's PID, start, end, census and verdict go to `queue.log`; if the session is gone, that file and `pgrep -af last-good-scripts-test` are where to look.
- **A slip of mine, caught at the first boundary:** the first start (queue PID 209913, 05:39:59) paused at once. Its pause test matched any line naming `PAUSE T15`, and the coordinator's 05:38 entry names the convention (*"write PAUSE T15 on this file"*). I stopped it by PID before any run began and tightened the match to a directive: `PAUSE T15` or `RESUME T15` at the start of a line or straight after an entry's header. The new match finds 0 such lines in the host file, and fires on a constructed `== M7 root -- ...: PAUSE T15 ...` line and on a bare `PAUSE T15`. Then I restarted the queue.

## [Stage E] 05:51 UTC — the first run on the donor: root-tip at S2's tip; S3's code so far

- **root-tip** (`a286e5b49f`, a clone, PID 215185): **rc 3 in 517 s, 1,312 PASS / 0 FAIL / 0 SKIP / 2 CANNOT**, census `cc1plus=0 qemu=0 load 1.28` at its end (`4.29` at its start). The banner reads `sed/mv/cp/tr/head/wc/cut/awk: BusyBox v1.36.1 (2026-10-05 03:37:19 UTC) multi-call binary. -- a copy of /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox`. The verdict's lines:
  - `tools: busybox .../m6-donor/1a0266484423/... ; source: root, BUILD_ID 1a026648442321609b2288c2c9c06803817f9df2`;
  - `tools: rclone .../m6-donor/... -- v1.75.2; the recipe says v1.75.2`;
  - `2 CHILD SUITE(S) COULD NOT RUN` (this branch's writer tests; T14 merges first);
  - `PASSED, 0 SKIPPED, 2 CHILD SUITE(S) NOT EVIDENCE, 0 NOT APPLICABLE`.
  The counts are S1's end on the `069fc` root, so S2's six commits change no verdict on the tree.
- **S3's code so far, each committed with its positive or with its run queued:**
  - #1033 `5429e27e72` (positive in the commit: the static count, 3 then 0; the `set -u` abort);
  - #1037 `60066e21f8`;
  - #1027 `65bdd1a717`;
  - #1036 `32ba775765`;
  - #1034 `e155cd4309`;
  - #1032 `11952dfcf3` (positive in the commit: a driver that raises after its first verdict passes the unfixed check, the fixed one FAILs it).
  - #1037, #1027, #1036 and #1034's constructed cases run after the current queue.
  - #1026 and #1031 are next. #1026's representative set is the five runners that carry 63 of the file's `rc ≠ 0` checks: `p7bt` 27, `sa_run` 18, `c1` 10, `cf1` 6 and `b`'s `bt` (the founding kill and restore).

## [Stage E] 06:02 UTC — S3 to S6's code complete; #1021's positives; the twelve move to the final tip

- **All 22 bugs now have code.** S3:
  - #1033 `5429e27e72`, #1037 `60066e21f8`, #1027 `65bdd1a717`, #1036 `32ba775765`, #1034 `e155cd4309`, #1032 `11952dfcf3`;
  - #1026 `812d09e3af` (a witness that the script started, in the six runners that carry 63 of the 71 `rc ≠ 0` checks, and the guarded steps in `b`);
  - #1031 `b729628ad6` (barriers: a `flock` shim marking the second handler at the lock; a `hold` verb in the helper double).
  - S5: #1028 `5d1b47deb7` (`--clearenv --unshare-net` in `sa_run` and `sa2_run`).
  - S4: #1025 `db08ed0953` (`skip_dependents`: 40 missing-dependency branches, 164 dependent check sites named, a reader over the file's own structure).
  - #1032 `5d1f67ca0b`: `d13a` as well, found while S4's reader listed D's checks.
  - S6 (#1030) was closed by `3da816ce24` (the coordinator, 04:12).
- **#1021's positives on the donor** (`02` § S2, #1021): unfixed shallow clone, rc 1 with ten vacuity FAILs; fixed, rc 2 in 127 s at the read, naming `417dcd8610` and the path.
- **The twelve recipes move to the final tip, `5d1f67ca0b`.** #1023's acceptance asks for them at `fixed-at`, and S3's commits changed `--old` behaviour too (`q`'s fragments read at the ref, #1036). The first queue (215160) was stopped by its process group at 06:00, after `shallow-fixed` and 22 s into `old-1d1503180d` at `a286e5b49f`; nothing of it remained (`pgrep -g` 0, no suite or `bwrap` left).
- **The second queue** (`/workspace/tmp/m6-t15/s3/queue2.sh`, PID **1008748**, harness task `btiiafr4w`, the same `queue.log`), one run at a time:
  1. root-final, the full suite at `5d1f67ca0b` (PID 1008765, from 06:01:29);
  2. #1026's positive: a fake `bwrap` that exits 1 first on PATH, a sandbox that cannot start, on the unfixed file (`11952dfcf3`) and the fixed one;
  3. #1028's probe: a cut copy of stream A's setup with a script through `sa_run`, the caller exporting `RCLONE_CONFIG`, `RCLONE_CONFIG_QA_TYPE`, `BASH_ENV` and a function; unfixed `b729628ad6`, fixed `5d1f67ca0b`;
  4. the twelve `--old` recipes at `5d1f67ca0b`.
- **Still to construct, waiting on the coordinator's answer (#662, 05:52):** the positives that need a proven script altered in a throwaway clone (#1037, #1027, #1036, #1034), and #1031's broken lock and acknowledgement.

## [Stage E] 06:13 UTC — root-final; the coordinator's 06:05 answers; the stage-e alteration recipes

- **The coordinator, 06:05 (#662):**
  - (1) yes to altered throwaway copies for S3's positives, under `/workspace/tmp/m6-t15/s3/<bug>/`, never committed, removed after the run, each a recipe the branch carries (`stage-e/alter-<bug>.sh`) so the acceptance re-run reproduces it;
  - (2) the twelve at the final tip only. The 06:00 stop of the first queue is recorded at 06:05 above.
- **root-final at `5d1f67ca0b`** (the second queue's first run, PID 1008765): **rc 3 in 516 s, 1,315 PASS / 0 FAIL / 0 SKIP / 2 CANNOT**, census `cc1plus=0 qemu=0`. That is 1,312, plus #1033's self-check, plus the two checks #1027's split adds. Every strengthened check passes on the real scripts:
  - #1026's witnesses and `b`'s guarded steps;
  - #1036's rewritten markers, the pass's own status, `each compiled`, the four `100755` modes;
  - #1031's two barriers;
  - #1032's three drivers;
  - #1033's count (1,259 calls, 0 short).
- **`stage-e/` in the audit folder:**
  - `alter-lib.sh` (`change` and `drop_fn`, each failing closed when a change does not apply);
  - one recipe per positive: `alter-1037.sh`, `alter-1027.sh`, `alter-1034.sh`, `alter-1036.sh` (`q`'s status and markers, `t`'s compile, D21's mode), `alter-1036-gate.sh` (its own clone: CANNOT stops the fixed run), `alter-1036-frag.sh` (`q` cut under `--old 717bc04449`), `alter-1031.sh`;
  - `run-positives.sh`: per bug, clones at the tip and at the unfixed harness commit, the recipe, both runs on the donor, the target lines into `queue.log`, the clones removed.
  - Each recipe was dry-run on a fresh clone and its diff read. The first dry run caught two faults of mine in `alter-lib.sh`: `awk -v` ate the pattern's backslashes, so `drop_fn` removed nothing (its own post-check refused it); and the post-check did not fit insertions. Both fixed.
- **A slip of mine:** the first set of dry clones was removed with `rm -rf -- "${S:?}/dry-$b"` in a loop inside a longer command. That breaks the removal shape: `rm -rf` in its own short command. The paths were guarded and only those clones went. Every later removal is one short command, and the runner's three are one line each.
- **The positives run after the second queue ends** (a waiter on `QUEUE2 END`, then `run-positives.sh`, serial).
