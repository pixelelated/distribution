# T13 running log: the cloud test harness (#660)

The flight recorder for M6.P2 T13 (`cloud-harness`), brief
`docs/reviews/briefs/cloud-harness.md` at `6aa2fbaadb` (version 2), dispatched
on #660 at 2026-10-25 04:58 UTC. Newest last. Every time is from `date -u`.

## Header

| Field | Value |
| --- | --- |
| Executor | the T1 session (`m6-t1-os-launch`), **Opus 5.5** (`claude-opus-5-5`), **high** effort |
| Depth | Independent: one reviewer, `gpt` (`openai/gpt-6-astra`, `max`) at Phase 4.6, through the local Facilitator |
| `reviewed-at` | the nine tools read at **`8ebaf8daad`**'s bytes; the lane tip at dispatch is `e1d51b3a04`, where `git diff --stat 8ebaf8daad HEAD -- <the nine>` is empty |
| Worktree / branch | `/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-harness-660`, `feature/m6-cloud-harness-660`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` |
| Rules | `next`'s, except the eight paths the dispatch lists (`git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`: 8 files, 135+ 11-, exactly those); `rclone-cloud-sync.md` here is the stale one under #909 (OPEN) |
| Scratch | `TMPDIR=/workspace/tmp/m6-t13/tmp`; backend state `/workspace/tmp/m6-t13/state`; `.qa-scratch/t13/` (gitignored) |
| VM question | **Can this be done on the VM? Yes -- most of it on the host** (the four bare tests, the backends' up/ls/cat/down, `--list`); the one guest cycle (the single-device suite over WebDAV and SFTP plus CAP1-14) only in a window the coordinator grants on #660. No handheld, no person's cloud, no hosted account; `cloud-census` read, never run; `--real-roms` never. |

## 2026-10-25 04:58 UTC -- dispatch read, first commands

- #660's body (16 criteria) and its dispatch comment read; the brief read whole at `6aa2fbaadb` (`git diff --quiet 6aa2fbaadb HEAD -- docs/reviews/briefs/cloud-harness.md`: equal); the seeded pointer read. **Delta, recorded:** the pointer's lens line says "46 steps and 42 cells"; the body and the brief's version 2 say 32 + 2 steps and 44 cells. The body wins; the generator decides at stage B.
- `git fetch origin`, `git fetch upstream --no-tags`: rc 0. Branch `feature/m6-cloud-harness-660`; `merge-base --is-ancestor 2174265e9c HEAD`: stacked-on-P1; `docs/reviews/inventory.json` present.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`: the dispatch's eight paths, nothing else.
- Host file, last line: `== M7 root correction: input06 also retained stop rc5 because the successful transient fixture unit auto-unloaded. [...] Input07 adds fixture-only RemainAfterExit=yes [...]`. Census: `pgrep -x qemu-system-x86`: **0**; compilers (`cc1|cc1plus|rustc|ninja`): **0**. `df -i /tmp`: 41% (nothing is exported under `/tmp`).
- `git diff --stat 8ebaf8daad HEAD -- <the nine>`: **empty**.
- #909: `OPEN Bug: rclone-cloud-sync.md states five rclone facts the package has moved past (PKG_SHA256, the version, tar.gz, exit 69, the content tier)`.
- `tools/rules-check --quiet`: rc 0; `tools/register-check`: `681 IDs, each once; every citation in the live documents names a row`.
- Branch already on origin at `e1d51b3a04` (the coordinator pushed it).

## 2026-10-25 04:59 UTC -- before the backends: isolation from the M7 lane

`tools/cloud-test-backend` keeps its state at `${CLOUD_QA_STATE:-~/.cache/rocknix-cloud-qa}` on fixed ports (9010 WebDAV, 9012 S3, 9013 SFTP), names its MinIO container `rocknix-cloud-qa`, and its `down` kills **any** process listening on the backend's port (lines 565-591). The M7 lane runs guests on this host under its own grant. Read first: `ss -ltnp` shows nothing on 9010-9099; `docker ps` shows no QA container; `~/.cache/rocknix-cloud-qa` holds old state (last pid file 2026-09-09). So stage A runs every backend with the tool's own overrides, **`CLOUD_QA_STATE=/workspace/tmp/m6-t13/state`, ports 9080 (WebDAV), 9082 (S3, upstream 9092), 9083 (SFTP), container `rocknix-cloud-qa-m6t13`**, so that a `down` here can reach nothing of another lane's. The subcommands and their code paths are the defaults' (the port, the state root and the name are parameters).

- **No fetch:** `up` for S3 is `docker run` with no `--pull` (lines 432, 447); `quay.io/minio/minio:latest` is already local (`14cea493d9a3`, created 13 months ago); `dperson/samba:latest` local too (`66088b78a198`). WebDAV and SFTP are host binaries (`rclone v1.60.1-DEV`, `/usr/sbin/sshd`).
- **A finding to carry to stage B:** the tool's option loop (lines 57-63) stops at the first non-option, so `--backend` must come **before** the subcommand. The brief's § 5 line `tools/cloud-test-backend up --backend "$b"` would run `up` on the default WebDAV with `--backend` as a stray argument. Stage A uses `--backend "$b" up`; the brief's order is checked by a run below.

## 2026-10-25 05:00-05:01 UTC -- stage A runs (host only)

Census before: qemu 0, compilers 0 (04:58). `TMPDIR=/workspace/tmp/m6-t13/tmp`. Every line below is in `02-forward-audit.md` § The runs with its *a FAIL would mean*; raw outputs in `.qa-scratch/t13/`.

| Time | Command | Exit | Wall |
| --- | --- | ---: | ---: |
| 05:00:06 | `tools/cloud-connections-test` (26 tests, `OK`) | 0 | 1.9 s |
| 05:00:08 | `tools/cloud-input-test` (9 tests, `OK`) | 0 | 1.0 s |
| 05:00:08 | `tools/cloud-capture-stamp-test` (14 PASS, `PASSED`) | 0 | 0.1 s |
| 05:00:08 | `tools/cloud-save-integrity-test --rclone /usr/bin/rclone` (`PASS total=24`) | 0 | 0.1 s |
| 05:00:08 | the stamp test's positive over `f451252587`'s `cloud_capture` (`8 CHECK(S) FAILED`) | 1 | 0.1 s |
| 05:00:09 | `tools/cloud-pair-migration /nonexistent/a.img.gz /nonexistent/b.img.gz /nonexistent/c.tar` (the retirement sentence) | 2 | 0.00 s |
| 05:00:35 | `tools/cloud-test-backend port --backend sftp` vs `--backend sftp port`: 9010 vs 9013, both rc 0 (and `caps`, the same) | 0 | -- |
| 05:00:41 | WebDAV `:9080`: `up` 0, `put` 0, `ls` 0, `cat` present 0, `cat no/such/object` **1**, `reset` 0, `down` 0, `status` 1 (`not running`) | -- | 0.0-0.1 s each |
| 05:00:45 | SFTP `:9083`: the same sequence, the same exits | -- | 0.1 s each |
| 05:00:45 | S3 `:9082` (container `rocknix-cloud-qa-m6t13`, `quay.io/minio/minio:latest` already local, not pulled): the same sequence, the same exits; `up` 1.6 s | -- | -- |
| 05:01 | nothing left: `ss -ltn` 0 listeners on 9010-9099; `docker ps -a` 0 `rocknix-cloud-qa*`; `pgrep -a sshd \| grep -c m6-t13` 0; no `rclone serve webdav`, no `minio server` | -- | -- |
| 05:01 | `tools/cloud-round-trip --list`: 55 lines, 45 cells | 0 | 0.1 s |

Nothing ran against a handheld, a person's cloud or a hosted account. `cloud-census` was not run. No guest, no `--real-roms`, no `tools/council/run` call. Nothing was written under `/workspace/repos/rocknix*` or `/tmp`; `/tmp` was only read (the host coordination file's last lines). No credential-shaped line reached a log: every backend output was passed through the masking `sed` before display, and the SFTP/S3 `up` lines carry no secret.

The image for the guest-cycle request, read only: `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` (2,122,289,964 bytes; three copies under `/workspace/artifacts/m6-t{1,2,3}-*`). T12's vm-qa report of 2026-10-24 22:57 (`/workspace/artifacts/rocknix-images/qa-069fc27044-webdav-a-20261024-225716/report.md`) names `BUILD_ID 069fc270442134fe771258418adf4e666e0473fb` and a 52 s bring-up. This tree's `docs/vm-qa-log.md` has no row for it; T12's branch has one (`git show feature/m6-tooling-vm-harness-659:docs/vm-qa-log.md | grep -c 069fc27044` prints 1).

**Stage A done at 05:0x UTC**; the checkpoint and the window request go on #660.

## 2026-10-25 05:07 UTC -- stage B begun while the window waits: the shapes generator

- The checkpoint and window request were posted at 05:0x: https://github.com/pixelelated/distribution/issues/660#issuecomment-6393734808.
- **Isolation carries into the window:** `vm-qa` calls `cloud-test-backend` with no arguments and exports only `CLOUD_QA_BACKEND` (lines 70, 117-118, 313, 325-326, 397-400), so `CLOUD_QA_STATE`, `CLOUD_QA_PORT` and `CLOUD_QA_NAME` reach it through the environment.
- `tools/t13-shapes.py` (in this folder, not the repo's `tools/`) is written. It is run as `python3 -I -B tools/t13-shapes.py /workspace/tmp/m6-t13/cloud-round-trip.8ebaf8daad --json .qa-scratch/t13/shapes.json`, against `git show 8ebaf8daad:tools/cloud-round-trip` (`cmp` equal to the worktree's). Result: rc 0, `{"steps": 34, "cells": 44, "rows": 78, "by_oracle_rule": {"both ends": 28, "device report": 19, "synthetic": 31}, "deltas": []}`. Its oracle column is a rule-based first cut, to be reviewed row by row.
- **Q2 lead:** `caps()` is read at three call sites. Two are in A14's helper (`hash`, lines 2369-2373) and one is in KILL1 (`commit`, line 6786). No step of the single-device suite reads it.
- **Q7 lead:** the suite's 34 step spans hold 114 `check()` calls; the cells' spans hold 352 (one helper level). The ledger's 106 and the work log's 108 are runtime counts, which loops and branches make differ from the static count.

## 2026-10-25 05:07-05:20 UTC -- stage B (reading; no guest)

- 05:07: the coordinator's answer on #660 (stage A stands; the window asked of M7; go on to stage B). 05:1x: the pass-through check posted (https://github.com/pixelelated/distribution/issues/660#issuecomment-6393759361). `vm-qa` passes `CLOUD_QA_STATE`, `CLOUD_QA_PORT` and `CLOUD_QA_NAME` through, never downs the backend, and defaults `VM_PAIR_DIR`/`VM_QEMU_RUNTIME_DIR` to `/tmp`, both to be set under `/workspace/tmp/m6-t13/` in the window. `vm-stop` refuses a process not on its own qcow2. Guest a's SSH port 10022 is fixed.
- The generator `tools/t13-shapes.py` was refined (host runs of the tool, `Pair.cloud_sha`, `Link.exercise`'s receiving side, the device's own rclone reads, the planted conditions) and still asserts 34 + 44 with no delta. `tools/t13-render.py` renders 02 § Assertion shapes: 79 rows (78 + `CONTRACT`), by oracle **24 both ends, 44 synthetic input, 10 the device's report**, with eight rows overridden by hand, each with its reason. An early cut read PASS or FAIL off the ledger rows' free text; it was withdrawn for citing the rows by date and line.
- 05:2x: positives on the host, all in scratch trees under `/workspace/tmp/m6-t13/pos/` (the worktree untouched):
  - `cloud-round-trip` on refused SSH port 1: rc 2, `FAIL  no shell over ssh`.
  - `cloud-connections-test` with the line-147 guard defeated: rc 1, 1 FAIL of 26.
  - `cloud-input-test` with a no-op `wifictl`: rc 1, 6 FAIL. The negative control ERRORed on `git show` in a non-checkout (exit 128), the environment's.
  - `cloud-save-integrity-test` with the provider-hash compare defeated: rc 1, `FAIL changed payload rejected`.
  - The backend's `ls` on a state directory that does not exist: rc 0, 0 bytes (F-12).
- Read for Q4 only, never brought up: pyftpdlib 2.2.0 in the default state's venv; the image's rclone `PKG_VERSION="1.75.2"`.
- `tools/archaeology mixed-installation` (read only): the D-CLOUD-158 gate was met on 2026-10-05, before D-CLOUD-175 retired the migration.
- Written: 02 § Coverage (9), § Assertion shapes (79), § Positives (9), § Proofs; 03 whole; 04 to its renovation face, with § Second opinion pending stage C. The pre-issue lint was run once to learn its contract: 14 failures, all owed by stage C (05, `review-plan.json`, and the 04 sections now written).
- No guest, no handheld, no hosted account, no `cloud-census` run, no `tools/council/run` call, no write under `/tmp` or `/workspace/repos/rocknix*`.
