# T22 running log: the OS's system services and platform quirks (#669)

The flight recorder for M6.P2 T22 (`os-system-services`), brief
`docs/reviews/briefs/os-system-services.md` at `cc8b6cf2a3` (version 3),
dispatched on #669 at 2026-10-25 09:05 UTC. Newest entries are last. Every
time comes from `date -u`.

## Header

| Field | Value |
| --- | --- |
| Executor | the T1 session (`m6-t1-os-launch`), **Opus 5.5** (`claude-opus-5-5`), **high** effort |
| Depth | **Extended**: two reviewers at Phase 4.6, through the local Facilitator: `gpt` (`openai/gpt-6-astra`, `max`) and `gemini-argon` (`google/gemini-4-argon`, `high`); each runs a probe, then one refutation over a trimmed packet (D-WORKFLOW-195). If a seat cannot run, that is a named blocker on #669, never `--member gemini` |
| `reviewed-at` | the 422 read at **`8ebaf8daad`**'s bytes; at the dispatch tip `4a48d388c4` nothing under `packages/` or `projects/` differs from it (the coordinator's check) |
| Upstream compared | **`651150fc88`** (upstream `next`, already in the repository; never fetched); merge base `c445081a59` |
| Worktree / branch | `/workspace/repos/pixelelated/distribution.worktrees/m6-os-system-services-669`, `feature/m6-os-system-services-669`, stacked on `feature/m6-p1-survey-641` at `2174265e9c`; dispatch tip `4a48d388c4` |
| Rules | `next`'s, except the eight paths the dispatch lists; `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` gives 9 files (those eight plus `tools/lint-audit-artifacts`, which the command names), 142+ 11- |
| Scratch | `TMPDIR=/workspace/tmp/m6-t22/tmp`; `.qa-scratch/t22/` (gitignored) |
| VM question | **Can this be done on the VM? Yes, for the units and the GENERIC_X64 quirks.** One GENERIC_X64 guest, under 30 minutes, only in the window the coordinator grants on #669. **No, for the rest:** the H700 and SM8550 platform quirks, `QUIRK_DEVICE`'s device-tree branch, `sleep.d/` and `volume-fixup.service` are read line by line and point at `docs/releases/device-facts.md` or become an open item to test. Nothing runs on a handheld. |

## 2026-10-25 09:05 UTC -- dispatch read, first commands

- #669's body (18 criteria), its dispatch comment, the brief (read whole at `cc8b6cf2a3`) and the seeded pointer were read.
- First commands (brief § 1), in the worktree only, **no fetch**:
  - branch `feature/m6-os-system-services-669`; stacked on P1 (`merge-base --is-ancestor 2174265e9c HEAD`); `docs/reviews/inventory.json` present;
  - `651150fc88` resolves locally;
  - `grep -c gemini-argon`: `scripts/council-invoke.ts:7`, `tools/lint-audit-artifacts:4` (two non-zero counts, so both seats' routes are in the tree);
  - `tools/rules-check --quiet`: rc 0; `tools/register-check`: `681 IDs, each once; every citation in the live documents names a row`;
  - `git status --short`: clean; the branch tracks `origin/feature/m6-os-system-services-669` (pushed by the coordinator).
- **Host file, last line:** `== M6 coordinator — 08:42 UTC: T13 THIRD WINDOW RETURN (the lane's post on #660); census qemu 0, listeners on 9010-9099 and 10022: 0. M6 runs no guest now. No device operation.`
- **Census:** `pgrep -x qemu-system-x86 -r R,S,D,T`: **0**; compilers: **0**; `df -i /tmp`: 41% (nothing is exported under `/tmp`).

## 2026-10-25 09:06-09:20 UTC -- stage A: the § 5 runs

Each run's output is in `.qa-scratch/t22/runs/NN-*.out`, with its exit and wall time. The figures and their *a FAIL would mean* go into `02` § The runs at stage B. The summary:

- **Membership** (`01-membership`): `paths 422 lines 16604`; `read 10898 fork-own read 3002 fork-own paths 24`; tier 398 / 24; reach 422; written 422. All as the brief says.
- **Selection:**
  - `system-utils/package.mk:27-36` installs `sources/devices/${DEVICE}/*` and `sources/autostart/${DEVICE}`; `:14-15` installs `autostart/common` on every build.
  - `quirks/package.mk:15` copies every `devices/*`; `:16-18` copies every `platforms/*` when `platforms/${DEVICE}` exists.
  - The 264 platform files split H700 22 + SM8550 24 + GENERIC_X64 5 = 51 shipped and 213 that run nowhere shipped.
  - The `system-utils` device rows not installed by any shipped image: AMD64 3, RK3399 3, RK3566 1, S922X 1 = 8. `video_sense` exists for GENERIC_X64 and RK3399 only.
  - `/usr/bin/autostart` (97 lines) selects at `:16-28` (`HW_DEVICE`) and `:31-43` (`QUIRK_DEVICE`, set at `002-autostart:8-12`), and runs `/storage/.config/autostart/*` from `:71`.
- **Units** (`09`, `10`, `10b`): 29.
  - **Delta in the brief's own command:** its masking `sed` (`user[=:]`, case-insensitive) also matches `User=`, so `10` printed `User=***` for all 29 and hid the count. A run that masks its own figure cannot pass.
  - Rerun with the mask applied to the `ExecStart` text only (`10b`): **0 of 29** carry `User=`, `Group=` or `DynamicUser=`, so all run as root.
- **Enablement** (`20`):
  - Who enables what: `shell.service` (`busybox/package.mk:187`, override), `cron`/`cron-defaults` (`:196`, `:200`), `userconfig.service` (`systemd/package.mk:326`), `udevil-mount@.service` (generic `udevil/package.mk:40`), `rocknix-autostart.service` (`rocknix/package.mk:85`), `powerstate.service` (`powerstate/package.mk:20`).
  - No `enable_service` names `video`, `headphones`, `input`, `fancontrol` or `batteryledstatus`; what enables them is stage B's question.
- **busybox** (`11`, `12`): `PKG_VERSION="1.36.1"` (`:7`); `PKG_URL="http://busybox.net/..."` (`:11`, plain http); `CONFIG_FEATURE_SUID=y` `:30`, `LOGIN` `:549`, `PASSWD` `:554`, `SU` `:556`, `HTTPD` `:888`, `FEATURE_HTTPD_CGI` `:894`, `NC` `:950`, `UDHCPD` `:1010`. All at the brief's lines.
- **History** (`13`, with the explicit midnight cutoff `--since='2026-06-01T00:00:00Z'`): **87** non-merge commits; **33** the fork's; **54** upstream's.
- **Upstream delta** (`14`, `15`, `19`):
  - **44 M, 20 D**; under the globs **42 A and 2 R** (the R are `busybox-10-...MS_BIND` R056 and `util-linux-02-enable-blkdiscard` R073).
  - The 20 D split **9 / 2 / 9**: 9 absent at the merge base (the five GENERIC_X64 quirks, `hang-policy.conf`, `GENERIC_X64/video_sense`, `20-watchdog.conf`, the pstore drop-in); 2 upstream removed (`99-coredump.conf` by `8bce25b3b7`, `sysctl.d/rocknix.conf` by `54acd9556f`); 9 deleted (RK3576 `99-idle-only` `a98a3066f5`, the four SM6115 sleep hooks `6ac52e0c04`, `file` and `i2c-tools` `6103571f67`, `99-rocknix-networking.conf` `54acd9556f`, `80-clock.rules` `899193e5af`).
- **Routes** (`17`): 7 and 4. **The removal rule** (`18`): `git diff --stat 4a48d388c4 HEAD -- packages projects tools` is empty.
- **The fork-own 24** and the **30 config files** (4,487 lines; the three busybox configurations 1,224 + 1,224 + 1,200 = 3,648) are listed in `01` § Scope (`21`).
- **The pre-commit scan refused the first commit** of `01`: one upstream file name under `gptfdisk/patches/` (patch 0001) contains a key-shaped substring. The line in `01` was reworded to a placeholder with the command that shows the name, not exempted (`fork-workflow.md`). The raw run output under `.qa-scratch/` keeps the name and is gitignored.

## 2026-10-25 09:12-09:17 UTC -- the guest window (granted 09:12 on #669)

- Granted at 09:12 (one guest, 30 minutes from START, the seven steps; T13's conditions). Census before the boot: qemu 0, 10022 free; the host file's last line is the grant.
- **START 09:13:41** (posted on #669). Guest a was booted with `tools/vm-pair reimage a` from M6's image (`...g069fc2704421...img.gz`, BUILD_ID `069fc270442134fe771258418adf4e666e0473fb`), under `/workspace/tmp/m6-t22/`.
- Every read went through the masking `sed`. Identities print as `runs-as=` and as uids from `/proc`, so the mask cannot hide a figure. One masked token, `passwd:***` in step 4's applet line, is the mask matching an applet name; its value (`applet=1`, the link) is in the same line.
- **The only write was step 5,** on the disposable disk: five plants in `/storage/.config/autostart/` (an executable marker, a copy named `40`, one named `40 split`, a mode-644 file, a directory) and one reboot over SSH. The boot id moved from `6d0c5b10-...` to `ed740e10-...`.
- **Stopped 09:16:25** by `tools/vm-pair down` (`owned QEMU exited (pid 3339623)`). The leftover check reads 0 on every line. The record is every output, in `guest-cycle/` (`s1` to `s6b`, `boot.out`, `down.out`, `leftover.txt`). What it shows goes to `02` § The guest cycle.

## 2026-10-25 09:17 UTC -- the guest disk retired (D-INFRA-022)

- **Retired:** `/workspace/tmp/m6-t22/vm-pair/` (the QA key pair, `vm-a.ovmf-vars.fd`, `vm-a.qcow2` 2,309,881,856 B sha256 `11bf750d38df9bf8764e24eb9ed0ea86dc9d52554a2501ce696b127e37d2ba68`), 2,310,423,016 bytes. Nothing had it open. It was released by RETURN with the record on the branch (`c102a91281`). The hash is provenance only; it makes no claim that the file still exists.
- **df on /workspace:** 1,643,651,694,592 bytes available before, 1,645,962,080,256 after, a measured recovery of 2,310,385,664 bytes. The isolation directories that remain (`run/`, `tmp/`, `artifacts/`, `cycle/`, `cycle.env`) are kilobytes and go at the hand-back.

## 2026-10-25 09:17-09:45 UTC -- stage B: 02 written

- More host reads (`.qa-scratch/t22/runs/19` to `24`): the 20 D's split, `enable_service`, the applets' callers and the setuid lines, the 44 M with their commits, every unit's Exec lines. Plus targeted reads: `scripts/install`'s copy blocks (`:86-155`), `quirks/package.mk` whole, `098-deviceutils`, `/etc/profile` (`busybox/config/profile:13-23` sources `/storage/.config/profile.d/*`), `scripts/init:1215-1216` and `:1363-1364`, `rocknix/package.mk:36-40` (`LOCAL_SSH_KEYS_FILE`) and `post-update:54-57` (#740's sibling), and the `DEVICE_HAS_HDMI` devices.
- `tools/t22-reach.py` generates the reachability and coverage tables, and asserts 422 rows, 8 and 213 (no deltas).
- **My slip:** the generator's first cut cited `scripts/install` lines one to two off (`:85-88` and so on, which are `fi` lines). Corrected against `grep -n` before `02` was written. The cited lines of `system-utils`, busybox, systemd, the quirks, `autostart`, `sleep.sh` and `098-deviceutils` were re-checked against reads made in this session.
- `02`: § The runs (25 rows), § The reachability table (422), § The units (29), § busybox, § The upstream delta (44 M with each finding's state; 20 D; 42 A and 2 R; C-1 and C-2), § The guest cycle, § Proofs (L-01 to L-15), § Coverage (422).
- `git diff --stat 4a48d388c4 HEAD -- packages projects tools`: empty.

## 2026-10-25 09:20-09:34 UTC -- stage C: 03, 04, the packet, the seats

- `03` and `04` written. `04` holds sixteen findings, all Low, eight of them designs. The pre-issue lint fails only on `05` (stage D) and, until it was written, `review-plan.json`.
- **The council runtime:** `tools/council/node_modules` was absent in this worktree. T1 and T13 each ran `npm install --prefix tools/council`, which can reach the registry. This slice forbids a fetch, so instead: `npm install --offline --prefix tools/council --no-audit --no-fund` (cache only; it refuses rather than touch the network): rc 0, 1 s, `esbuild`'s install script declined as before. `package-lock.json` sha256 `ad7b535894875b35...`, the same as T13's. `COUNCIL_ENV_FILE=/nonexistent tools/council/run invoke --help` runs.
- **The packet** (`tools/t22-packet.py`): 56 files whole (the 29 units, the 24 fork-own, the brief's named files, and three additions: `busybox/config/profile`, `098-deviceutils`, `udevil.conf`'s lines 200-245 as an excerpt), busybox-target.conf's flagged lines as an excerpt, four context sections, and all 30 register rows the brief names. Body 379,978 bytes.
  - **Scanned before any brief was written:** `tools/forbidden-terms-check --stdin` 0 hits; `.githooks/secret-patterns` 0 lines; T10's widened set (`git show feature/m6-tooling-guards-657:.githooks/secret-patterns`) 0 lines. No redaction.
  - `second-opinions/packet-manifest.json` records every source's sha256 and the scan.
- `review-plan.json` (depth `extended`, the two reviewers, four calls planned) was committed before the first call (`5321bea183`).
- **The `invoke` calls:** four in all, a probe and a refutation per seat. That is the brief's "a probe then one refutation" for each of the two seats; the acceptance criterion's "two invoke calls (the seats)" counts seats.
  1. **Astra probe** (`tools/council/run invoke --member gpt --provider openrouter --prompt-file .../gpt-probe-prompt.md --output .../gpt-probe.md`, 09:32:20-09:32:31): rc 0, `council-facilitator@1.14.1-pixelelated.2`, outcome success, 0 retries. Verification PASS: observed `openai/gpt-6-astra` (`provider_response`), provider OpenAI (`response_provider_field`), effort `max` (340 reasoning tokens). The reply was `READY unknown`; identity is taken from the provider's fields, not the reply.
  2. **Astra refutation**, in flight since 09:33:02: `tools/watch-build --record-only -- tools/council/run invoke --member gpt --provider openrouter --prompt-file .../gpt-brief.md --output .../gpt-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`. **What watches it:** the record `.build-runs/20261025T093302Z-f3543809/` (status, `build.rc`), and the harness's background task, which delivers the exit to this session. If the process is killed outright, the record says `died` and the background task still returns.
  3. **Argon probe** (`--member gemini-argon`, 09:33:15-09:33:21): rc 0, the same facilitator, success, 0 retries. Verification PASS: observed `google/gemini-4-argon` (`provider_response`), provider Google, effort PASS (192 reasoning tokens). Reply `READY Gemini 4 Argon`.
- **Every other `tools/council/run` call carried `COUNCIL_ENV_FILE=/nonexistent`** (the `--help`s).

## 2026-10-25 09:54-10:12 UTC -- Astra graded; Argon's refutation in flight

- **Astra refutation** finished 09:53:54: watch-build rc 0, `build.rc` 0, state finished. The facilitator printed `attempt=1/4 ... model=openai/gpt-6-astra providers=["OpenAI"] effort=max reasoning=48690 content=25905b finish=stop outcome=success duration=1248877ms`. Provenance: verification PASS (`provider_response`), provider PASS, effort PASS. Output `gpt-audit.md`, sha256 `107d6168aebfbe40d6552e2532e36cc8b103411c918b702776a0e06e9d4d4987`.
- **Graded** in `04` § Second opinion. Every confirmed item was re-read at its lines: `scripts/init` (`:86-99,143-174,298-331,340-376,394-437,610-666,825-906,1031-1145,1290-1320`), `input_sense` (`:90-106,176-226,280-372`), `userconfig-setup:66-90`, `autostart:78-97`, `systemd/package.mk:215-226,328-334`, `powerstate.sh:50-62`, `095-cloud-ssh:30-46`, and the autostart and udevil units. Upstream's `init` diff was read: the update code is unchanged; the reset and restore markers are removed by `a98a3066f5`.
- Grades: 26 confirmed (G-02, G-04, G-13 and G-23 at Medium), 6 narrowed, 2 not re-read (G-26, G-27).
- **Corrected from Astra's reading:**
  - `03` § 3.5's claim that `EnvironmentFile=/etc/profile` sources the profile (G-21);
  - F-07's "only on a `textmode` boot" (G-12, G-13);
  - F-04 to Medium.
- **Argon refutation**, in flight since 09:58: `tools/watch-build --record-only -- tools/council/run invoke --member gemini-argon --provider openrouter --prompt-file .../gemini-argon-brief.md --output .../gemini-argon-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`. The brief is 393,701 bytes: Argon's third-reader preamble, the Astra brief unchanged, and `04` § Second opinion appended. It was scanned three ways: 0, 0, 0. **What watches it:** the record `.build-runs/20261025T095741Z-4e1cd8de`, and the harness's background task.
