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
