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

## 2026-10-25 06:02-06:15 UTC -- stage E, S1 (`cloud-test-backend`) done

- 06:02: the stage-E brief (`t13-streams.md` at `44fdec1e16`, read whole) and the dispatch on #660. S1 is `cloud-test-backend`, S2 `cloud-round-trip`, S3 the small tools; the four guest criteria fold into the held cycle.
- **The unfixed copy:** `git clone --no-checkout --shared` of this worktree into `/workspace/tmp/m6-t13/unfixed`, with `git checkout 8a2518fa44 -- tools` (no worktree registered, so nothing for `fork-worktree` to remove).
- **The commits, one per bug, each with its positive in 02 § The streams' positives:**
  - `0cceb65207` #1058: `--backend` after the subcommand refused, exit 2.
  - `94c050ed5a` #1067: the SFTP endpoint is `rclone serve sftp` rooted at the data directory under the QA key. `/etc` is not found, the stanza user is `rocknix-qa`, and the endpoint prefix is now empty. Stated in the code: rclone does not check the user name under key auth.
  - `91267b0dda` #1068: no stanza from a failed `obscure`; the S3 config created under umask 077.
  - `7345a65e9d` #1060's backend half: `ls` and `reset` fail closed.
- **Post-S1 run** (06:14 UTC): WebDAV :9080, SFTP :9083 and S3 :9082, each `up`/`put`/`ls`/`ls` of a missing prefix/`cat` present and missing/`reset`/`ls`/`caps`/`down`, all as expected (02).
- **Leftover check after every case and every commit:** `ss` 0 on 9010-9099, 0 `rocknix-cloud-qa*` containers, 0 `rclone serve`, 0 `minio server`, 0 sshd on `m6-t13`.
- **A lead for S2:** `cloud-round-trip`'s `epath()` and `rpath()` docstrings describe SFTP's old absolute-path prefix; they are S2's file.
- Nothing under `tools/` but `cloud-test-backend`; no guest; nothing under `/tmp` or `/workspace/repos/rocknix*`.

## 2026-10-25 06:17-06:32 UTC -- #1067's ruling applied; stage E, S2 (`cloud-round-trip`) done

- **06:17, the coordinator's ruling on #1067's second criterion.** I edited the checkbox to the ruled text and ticked it from the S1 runs plus two refusals, run at 06:2x with the endpoint up under isolation:
  - the host's own keys, by ssh's defaults and by `~/.ssh/id_ed25519_devboxes` alone: `Permission denied (password,publickey)`, rc 255;
  - exec requests (`id`, `sh -c true`): `"…" not implemented`, rc 1;
  - stated, not hidden: rclone's built-in `md5sum`/`df` answer, with `df` giving disk figures.

  The evidence is on #1067 (issuecomment-6394310968); `box-check --issue 1067` reports 0 fail. The rewrite is noted in 05 PL-11 and in 02.
- **S2, one commit per bug in the brief's order, each with its host positive first** (against the shared clone at `8a2518fa44` or an extracted function; the lines are in 02 § The streams' positives):
  - `7f0e527800` #1066: ownership. Every removal under `/storage/roms` goes through `rm_owned`; an occupied `vectrex` is a refusal left as found.
  - `1e28ba8f94` #1060's harness half: `backend_listing` and a `Fail`-raising `backend()`; the `epath`/`rpath` docstrings follow #1067.
  - `332bda1515` #1062: KILL1 assigns `webdav`; `kill1_bad()` fails a file that is gone.
  - `539622b9d7` #1063: `contract_guard()` reads the structured list.
  - `09ca086062` #1057: A5 and RETENTION are one SKIP each without `cloud_reconcile`; RETENTION's two checks are gated on the kill point; `skip()` and `SKIPPED` are one definition.
  - `e71d077882` #1059: `verdict_line()` with backend, capabilities and counts; `NOTHING CHECKED` exits 2; an unknown or unsatisfiable `--only` exits 2; the equipment check stops the setup; the 14 ad-hoc SKIP prints go through `skip()`.
  - `bde357126c` #1064: `es_path_orphans()` and a floor of one path read.
  - `f7482f9684` #1065: CAP13 reads its own log part; the `grep -c ... || echo 0` sweep is listed in 02.
  - `0c538b1f74` #1069: A15's upload is a real archive.
  - `77e7b16193` #1070: `kill5_names()`; KILL5's literal 5 became `len(own) + 2`.
- **Slips of my own, caught and corrected before any commit** (each is named in 02 where it touched a positive):
  - the #1066 stub mapped `/tmp/` twice;
  - the #1062 AST driver counted function-local names as module scope;
  - #1059's first conversion rewrote `skip()`'s own print into a recursion;
  - #1059's driver stubbed `backend()` for its verdict part;
  - a dead-device rc of 0 was read from `PIPESTATUS` after a command substitution;
  - the #1064 control's stub rewrote the `case` pattern;
  - `py_compile` twice left a `tools/__pycache__` (gitignored, removed; syntax checks then went through `ast.parse`).
- **Post-S2:** `--list` 45 cells; the dead-device case rc 2; no listener on 9010-9099; no QA container.
- No guest; nothing under `tools/` but `cloud-test-backend` and `cloud-round-trip`; nothing under `/tmp` or `/workspace/repos/rocknix*`.

## 2026-10-25 06:5x-06:35 UTC -- stage E, S3 done; nothing-checked exits 3; 05's outcomes; reviewed-at and fixed-at

- **S3:**
  - `1911fee4df` #1061: the fixture value is assembled at run time. T10's patterns (`git show`, never merged) match 1 line unfixed and 0 fixed, and the test still runs 26 OK.
  - `bf2832ce5b` #1081: the census reads the stored id file. `grep -c cloud_device_id` gives 1 unfixed and 0 fixed; an AST read of the string constants finds `['cloud_device_id']` unfixed and none fixed. The census was not run.
- **06:33, the coordinator's ruling** (#660, D-QA-063): nothing checked exits 3, and 2 stays the usage error. `cee4bf481d` is #1059's follow-up: `main()`'s return, evaluated from the AST, gives 3 for nothing checked, 0 for a pass and 1 for a failure, and the unknown `--only` is still rc 2.
- 05's Phase 7 gate and `punch_index` are at their outcomes:
  - Resolved, with commits: PL-02, 03, 04, 05, 07, 10, 11, 12, 15 and 22;
  - Open, fixed with the guest criterion pending: PL-01, 06, 08, 09, 13 and 14;
  - Deferred: PL-16 (#1055), PL-17 (#1075), PL-18 (#909), PL-19 to 21 (#1076-#1078), PL-23 (#1079) and PL-24 (#1080).

  `tools/lint-audit-artifacts ... --phase pre-issue`: `PASS pre-issue artifacts`.
- **Criterion 5:**
  - `reviewed-at` is `8a2518fa44` (the stage-D tip, rulings applied); `git diff --stat 8ebaf8daad 8a2518fa44 -- <the nine>` is empty.
  - `fixed-at` is `cee4bf481d`; `git diff --stat e1d51b3a04 cee4bf481d -- tools | grep -v tools/cloud-` gives no file line. Four of the nine changed: `cloud-census`, `cloud-connections-test`, `cloud-round-trip` and `cloud-test-backend`.
- No guest; nothing under `/tmp` or `/workspace/repos/rocknix*`.

## 2026-10-25 06:45-06:51 UTC -- the positives' drivers kept on the branch (the coordinator's 06:45 ask)

- `stage-e/` has nine drivers (#1066, #1060's harness half, #1062, #1063, #1057, #1059, #1064, #1069, #1070), `common.py`, `shim1068/build.sh` and `README.md`.
- Each driver was rewritten from its scratch version to the ask: the tool's path and `unfixed|fixed` as arguments, writes only under `$TMPDIR`, one verdict line last, exit 0 on the expectation met.
- **Run both ways:** all nine meet the unfixed expectation on the clone at `8a2518fa44` and the fixed one on this tree. A wrong expectation prints `UNEXPECTED` (pos1066 run `fixed`-tree/`unfixed`).
- **The README's shell rows were run as written,** with each backend down after. Each printed what its row says (#1058 rc 0/2; #1068 rc 0 with the clear value and 664 / rc 1 and 600; #1060 rc 0 empty / rc 1; #1061 1/0; #1065 `0 0`; #1081 1/0).
- `lint-audit-artifacts --phase pre-issue`: PASS. No change under `tools/`.

## 2026-10-25 07:50-08:11 UTC -- the guest cycle (granted 07:50 on #660)

- START 07:52:28 UTC (qemu 1), guest a booted alone with `tools/vm-pair reimage a` from M6's copy of the image, BUILD_ID `069fc270442134fe771258418adf4e666e0473fb`; the controls from the clone, the fixed cells, 5b, the suite over WebDAV and SFTP, and an unfixed SFTP suite as the comparison; the guest stopped by its pidfile at 08:09:21; the backends down; the leftover check clean (`stage-e/cycle/leftover.txt`); RETURN on #660 at 08:10. Nothing written on the host file.
- In-window: `a70b4889a3` (#1065, CAP13's needle to the image's words). My slip: the clone was `tools/` only, the first KILL1 control stopped at planting; the rclone sources checked out into the clone and the control re-run.
- Lines and findings: 02 § The guest cycle. 05 updated (PL-06/08/09/13/14 Resolved; PL-01, PL-11 Open). Retention held pending the #1067 answer (said on RETURN).

## 2026-10-25 08:12-08:20 UTC -- #1067's SFTP regression, fixed forward on the host (the 08:12 ruling)

- Host only, no guest. The diag endpoint was under `/workspace/tmp/m6-t13/diag-state` on 9083; servers on 9086/9087 for the version comparison; every listener down after each run (`ss`: 0 on 9083/9086/9087).
- The cause is `rclone serve sftp`'s five-minute directory cache, on 1.60.1 and 1.75.2 alike (02 § #1067, follow-up). Fixed in `7a71af7671` (`--dir-cache-time 1s`; `settle_cache` covers sftp). Positive: `stage-e/pos1067cache/run.sh`, both ways and crossed.
- My slip: the first proof wrote fixtures and listed within the 1 s window, so it read rc 3 on the fixed tool too. Rerun with the tool's own settle; the driver goes through `put`.
- No revert of `94c050ed5a`. Its confinement stands, and the 09:15 bound was met at 08:16.

## 2026-10-25 08:19-08:23 UTC -- the second window (granted 08:12 on #660)

- START 08:20 on #660. The pair came up at 08:19 (`vm-pair up`, M6's image). The SFTP suite on the fixed endpoint gave 108/0/0. A5/RETENTION across two guests gave both cells SKIP on the fixed tree and RETENTION's two vacuous PASS lines on the unfixed tree. The guests were stopped by owned pid at 08:22:43, every backend down, the leftover check clean. Record: `stage-e/cycle2/`, 02 § The second window.
- Then the host reruns at `7a71af7671`: pos1057 `fixed-expectation-met`, and the SFTP confinement probes (`/etc` and `get /etc/hostname` not found, no file written). #1057's two checkboxes and #1067's first were ticked from these. 05: PL-01 and PL-11 Resolved (16 resolved, 8 deferred, 0 open).

## 2026-10-25 08:25 UTC -- retention (the 06:52 ruling, held to the second RETURN by the 08:12 ruling), D-INFRA-022

- **Retired:** all of `/workspace/tmp/m6-t13/`, 4,637,791,555 bytes. Its top level was: 1067-body.md 1067-evidence.md 660-body.md artifacts audit-issue.md audit.log body-1057.md body-1067.md bugs c1057.md c1067.md cloud-round-trip.8ebaf8daad conf-state council-test.out cycle cycle.env cycle2 dead.out diag diag-state handback-streams.md idle.md idle2.md npm-install.out packet passthrough.md patch1066.py pos pos1057 pos1059 pos1060 pos1062 pos1063 pos1064 pos1065.log pos1066 pos1069 pos1070 post-1067host.md probe.log return2.md rulings-applied.md run s1-checkpoint.md s1-post.txt s2-checkpoint.md s2-dead.out scripts secret-patterns.t10 shapes-section.md shim1068 stageA-checkpoint.md stageB-checkpoint.md stageD-pause.md state streams-positives.md tmp u1067.log unfixed verify-pins.out vm-pair. The large payload was `vm-pair/`, two disposable guest disks rebuilt from the image on every `up`:
  - `vm-a.qcow2`, 2,310,209,536 B, sha256 `97fd5f897f28948f158298fd9dba3669a5033f58851a7908aed3ab4b76a811b5`
  - `vm-b.qcow2`, 2,309,160,960 B, sha256 `9d64fc5ab1ec6e4e91bd7f7060a8640800f7aff7fd5bb28415ff6e4028cc90e7`

  Those hashes are provenance. They make no claim that the files still exist.
- **Checked before removal:** nothing in the tree was open by a process or was any process's cwd; every file was owned by this user; no qemu, backend or container of the slice was running (the second window's leftover check, 08:22:43).
- **Released by:** both RETURNs on #660, with both cycles' compact records on the branch (`stage-e/cycle/` and `stage-e/cycle2/`). Nothing there needed a full disk: a later run regenerates a guest from the image.
- **df on /workspace:** 1,655,478,046,720 bytes available before, 1,660,111,147,008 after, a measured recovery of 4,633,100,288 bytes (4,418 MiB).
- **Kept (inputs, not this slice's):** the M6 image under `/workspace/artifacts/m6-t3-20261024/` (2,122,289,964 B) and the donor rclone under `/workspace/artifacts/m6-donor/1a0266484423/`.
- **Stage F's scratch:** a new `/workspace/tmp/m6-t13/` holding only host drivers' `$TMPDIR` output, removed at the hand-back.

## 2026-10-25 08:27-08:45 UTC -- stage F: G-2 and G-3 fixed on the host

- Filed #1092 (G-2, KILL1's drained re-run) and #1093 (G-3, A15's needles) before the fixes, as `bug` under M6 with code traces.
- `07c37ec2ed` (#1093) and `3a653eaec4` (#1092); positives `stage-e/pos1093`, `stage-e/pos1092`, both ways and crossed; LINK's judgement checked unchanged over 72 combinations; all twelve positives rerun at `3a653eaec4`.
- 04 § Q3 carries G-1..G-4; 05 adds PL-25 and PL-26, Open until a guest runs KILL1 and A15. The resolution lint FAILs on exactly those two, which is the true state; pre-issue PASS.
- Stage F's scratch is a new `/workspace/tmp/m6-t13/` (`tmp/`, the `c66b325ece` copy of the tool, the issue bodies).

## 2026-10-25 08:34-08:42 UTC -- the third window (granted 08:34 on #660)

- The isolation environment was recreated under `/workspace/tmp/m6-t13/` (retired at 08:25). One guest was booted; START was posted at 08:35. KILL1 at 200k gave 22/0/0; it did not meet the drained face, and 1a did not recur. A15 gave 38/0/0. The guest was stopped by owned pid at 08:40:44, the backend brought down, and the leftover check came back clean. Record: `stage-e/cycle3/`, 02 § The third window.
- #1092's and #1093's guest checkboxes are ticked, and their issues have no open checkboxes left. 05 has PL-25 and PL-26 Resolved: 18 resolved, 8 deferred, 0 open.

## 2026-10-25 08:44 UTC -- stage F's scratch retired (D-INFRA-022)

- **Retired:** all of `/workspace/tmp/m6-t13/` as recreated for stage F and the third window, 2,319,731,839 bytes. Its top level was: artifacts b1092.md b1093.md b660.md c1092.md c1093.md ckF.md cycle.env cycle3 g1092.md g1093.md g2.md g3.md return3.md run state tmp u1093 vm-pair.
- **The guest disk:** `vm-pair/vm-a.qcow2`, 2,318,598,144 B, sha256 `dd5a1c190bc4719fe19e244dbbd9d8b39d14a26af71f8f3ef4e232c8bbae6836`. The hash is provenance; it makes no claim that the file still exists.
- **Checked before removal:** nothing was open or used as a cwd; every file was this user's; qemu 0; the third window's leftover check was clean. The issue-comment drafts in the tree had all been posted.
- **Released by:** the third RETURN on #660, with the compact record on the branch (`stage-e/cycle3/`).
- **df on /workspace:** 1,657,831,952,384 bytes available before, 1,660,151,803,904 after, a measured recovery of 2,319,851,520 bytes (2,212 MiB). Before and after were read about a minute apart on a shared volume.
- **Kept:** the M6 image and the donor rclone under `/workspace/artifacts/`. Nothing of this slice remains under `/workspace/tmp/`.

