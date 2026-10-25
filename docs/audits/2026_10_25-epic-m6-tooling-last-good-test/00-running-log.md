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
