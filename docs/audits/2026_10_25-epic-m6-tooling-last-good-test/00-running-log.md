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
