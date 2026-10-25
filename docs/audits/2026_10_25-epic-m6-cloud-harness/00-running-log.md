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
- 05:12-05:13 (the outputs' mtimes): positives on the host, all in scratch trees under `/workspace/tmp/m6-t13/pos/` (the worktree untouched):
  - `cloud-round-trip` on refused SSH port 1: rc 2, `FAIL  no shell over ssh`.
  - `cloud-connections-test` with the line-147 guard defeated: rc 1, 1 FAIL of 26.
  - `cloud-input-test` with a no-op `wifictl`: rc 1, 6 FAIL. The negative control ERRORed on `git show` in a non-checkout (exit 128), the environment's.
  - `cloud-save-integrity-test` with the provider-hash compare defeated: rc 1, `FAIL changed payload rejected`.
  - The backend's `ls` on a state directory that does not exist: rc 0, 0 bytes (F-12).
- Read for Q4 only, never brought up: pyftpdlib 2.2.0 in the default state's venv; the image's rclone `PKG_VERSION="1.75.2"`.
- `tools/archaeology mixed-installation` (read only): the D-CLOUD-158 gate was met on 2026-10-05, before D-CLOUD-175 retired the migration.
- Written: 02 § Coverage (9), § Assertion shapes (79), § Positives (9), § Proofs; 03 whole; 04 to its renovation face, with § Second opinion pending stage C. The pre-issue lint was run once to learn its contract: 14 failures, all owed by stage C (05, `review-plan.json`, and the 04 sections now written).
- No guest, no handheld, no hosted account, no `cloud-census` run, no `tools/council/run` call, no write under `/tmp` or `/workspace/repos/rocknix*`.

## 2026-10-25 05:21 UTC -- stage C begun; a rule broken, recorded

- **A breach of the slice's rule:** `tools/council/run --help` was run **without** `COUNCIL_ENV_FILE=/nonexistent`, at about 05:2x UTC, to read its subcommands.
  - **What that call did, read from the script** (`tools/council/run` lines 21-28, 47-49), not from the key file: it sourced `~/.config/council/env` into its own process (the file is readable and mode 600). `--help` matched no subcommand, so it printed its header lines 3-18 to stderr and exited 2.
  - **What it did not do:** make a provider call. No key value appeared in the output, which was the header comments alone, and nothing was written.
  - **What it breaks:** the brief's "every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`", and so #660's criterion 12, which 00 has to show unbroken. This entry is that record. It goes on #660 with the stage-C checkpoint, and a friction line is written (`issue: #660`).
  - **From here,** every `tools/council/run` call but the one Phase 4.6 invoke carries `COUNCIL_ENV_FILE=/nonexistent`.
- 05:22: the coordinator's answers on #660. The mixed-installation proof under D-CLOUD-175 is owed as Backlog #1055 (the coordinator's); `cloud-pair-migration` stays retired, its removal deferred to #1055, recorded as F-13. The guest window is held behind M7's full build (05:12 clause) and comes at its FINAL RETURN.
- **The Facilitator, keyless:**
  - `npm install --prefix tools/council`: rc 0, 2 s. It warned that `esbuild`'s install script was not run, as in earlier slices.
  - `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.`
  - `COUNCIL_ENV_FILE=/nonexistent tools/council/run test`: rc 0, 28 s, 39/39, 127/127 and 19/19, 0 failing.
  - `COUNCIL_ENV_FILE=/nonexistent tools/council/run invoke --help`: usage only.
- **The packet** (`tools/t13-packet.py`, manifest `second-opinions/packet-manifest.json`) has 15 sources:
  - the nine at `8ebaf8daad`, **594,115 bytes** as the brief says;
  - the three context sections from this tree;
  - `02`, `03` and `04` whole.

  The body is 743,735 bytes. `gpt-brief.md` is the ask plus the body, **746,882 bytes, sha256 `e4cda5bc459519faa0d0f93b82014a6014f701f1025088541bf71630c61d2af2`**.
- **The packet's scan, before it was sent:**
  - `tools/forbidden-terms-check --stdin`: `0 hits on stdin`.
  - `SECRET_PATTERNS` (sourced, `/usr/bin/grep -a -c -E`): 0 lines under this branch's and the primary checkout's sets. **T10's widened set (`feature/m6-tooling-guards-657`, #935) matched 1 line:** `tools/cloud-connections-test:37`, a synthetic fixture value, not a credential.
  - **Redacted in the body** (the manifest's `redactions`); the source's sha256 is the original file's. The builder assembles the target value at run time, so it is not at rest. Rescanned: 0 lines under all three sets.
  - The line itself is a finding (F-14): a credential-shaped fixture literal at rest that T10's widened pre-commit will refuse on its next edit.
- **The probe**, 05:25:06-05:25:15 UTC, `tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-probe-prompt.md --output second-opinions/gpt-probe.md` (sources the key: the first of the two Phase 4.6 calls):
  - Served `openai/gpt-6-astra` by `OpenAI`, effort `max`, 291 reasoning tokens, outcome success, 9,348 ms, 0 retries.
  - Verification PASS (semantic, identity source `provider_response`); effort PASS; provider PASS (`response_provider_field`).
  - `facilitator_version` `council-facilitator@1.14.1-pixelelated.2`. The reply: `READY unknown`.
- **The refutation** (the second Phase 4.6 call) began at 05:25 UTC with `--per-attempt-timeout-ms 3600000 --total-timeout-ms 10800000`, logging to `/workspace/tmp/m6-t13/audit.log`.
  - **What watches it:** the harness background task that runs it (`bkeysfam7`), which notifies this session when it ends.
  - **Its silent mode:** a hung seat is ended only by those timeouts.
  - **A failed seat is a hold.** A seat cut by its output ceiling re-runs on a trimmed packet (D-WORKFLOW-195).

## 2026-10-25 05:38-05:47 UTC -- stage C's seat graded; stage D: the bugs, the audit issue, the pause

- **The refutation returned** at 05:38:50 UTC (background task `bkeysfam7`, rc 0): attempt 1 of 4, `finish=stop`, 34,948 bytes; 220,427 prompt and 36,583 completion tokens (28,431 reasoning); 803,757 ms, 0 retries. Served `openai/gpt-6-astra` by OpenAI at `max`; verification (semantic, `provider_response`), effort and provider PASS; Facilitator `council-facilitator@1.14.1-pixelelated.2`.
- **Scanned before it was read:** `forbidden-terms-check --stdin` 0 hits; `SECRET_PATTERNS` 0 lines under all three sets.
- **Graded in 04 § Second opinion:** 53 items. Re-read at their lines in this session: G-1, G-3, G-6 to G-8, G-11, G-19, G-26, G-30 to G-35, G-38 (step 29), G-40, G-42 to G-44, G-46 to G-48 and G-52; the rest accepted on the seat's citations and marked so.
  - **13 new defects verified** (F-15 to F-25), among them KILL1's `NameError` (6846), CONTRACT's always-true guard (4739, 4844), step 8's refusal deleting the refused `/storage/roms/vectrex` (915-916, 7784-7785), and the SFTP endpoint's guest key reaching the host user's files (396-397).
  - **The first reader's errors accepted:** six overrides shown where eight were claimed; A3, `prepare_device.2`, step 30, KILL1 and step 32 reclassified; "skips nothing"; line 5294; 17 rejection checks, not 19.
  - **The table re-rendered:** 24 both ends, 46 synthetic, 8 the device's report.
- **Stage D:**
  - 14 `bug` issues filed, **#1057 to #1070** (milestone M6), each `tools/box-check --issue N` 0 fail (28 open checkboxes in all).
  - 05 written with 24 PL items, `punch_index` and the Phase 7 gate (every item Open); `tools/lint-audit-artifacts ... --phase pre-issue`: `PASS pre-issue artifacts`.
  - **The audit issue #1073**, `Audit: M6 T13 the cloud test harness -- 24 findings (0 critical, 2 high)`, labels `audit` and `punch-list`, milestone M6, a sub-issue of #660 (`POST .../issues/660/sub_issues`).
  - **Two slips on the way, both corrected in place:**
    - #1073 was first filed with one checkbox (a greedy parse that swallowed the items), then edited to 24.
    - Its PL-22 named a handheld and failed `box-check`; it was reworded to the code fact (`tools/cloud-census:76`). `box-check --issue 1073` now reports 24 open and 0 fail.
- No guest, no handheld, no hosted account, no `cloud-census` run. The `tools/council/run` calls were the probe and the refutation, plus the keyless ones and the 05:2x breach recorded above. Nothing was written under `/tmp` or `/workspace/repos/rocknix*`.

## 2026-10-25 05:53-05:54 UTC -- the coordinator's stage-D rulings applied

- **05:52, the coordinator on #660:**
  - the rule break stays recorded (criterion 12 is ticked against 00's 05:21 entry), and its guard is on #1044;
  - PL-22 is **drop the call**: `cloud-census` reads the stored id file and never runs `cloud_device_id`;
  - the six Backlogs are filed (PL-17 #1075, PL-19 #1076, PL-20 #1077, PL-21 #1078, PL-23 #1079, PL-24 #1080);
  - stage E is three streams by tool, #1066 and #1067 first, with the brief to follow; nothing under `tools/` changes before it lands.
- **The census bug, filed: #1081.** The defect and the fix were re-read first: `tools/cloud-census:76` runs `cloud_device_id`, which writes `ID_FILE=/storage/.config/cloud_sync-device-id` (its line 54, `write_id` at 288), against the tool's own header lines 16-18. `box-check --issue 1081`: 2 open, 0 fail.
- 05's Tracked fields, its `punch_index` and its Phase 7 gate now name #1075-#1080 and #1081, and PL-22 is a Correctness bug. #1073's body was edited to match; `box-check --issue 1073`: 24 open, 0 fail. The pre-issue lint: `PASS pre-issue artifacts`. 04 § Q6's census row records the ruling.
- `git status --short -- tools` is empty: nothing under `tools/` has changed.
