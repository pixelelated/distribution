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

## 2026-10-25 09:54-09:58 UTC -- Astra graded; Argon's refutation in flight

- **Astra refutation** finished 09:53:54: watch-build rc 0, `build.rc` 0, state finished. The facilitator printed `attempt=1/4 ... model=openai/gpt-6-astra providers=["OpenAI"] effort=max reasoning=48690 content=25905b finish=stop outcome=success duration=1248877ms`. Provenance: verification PASS (`provider_response`), provider PASS, effort PASS. Output `gpt-audit.md`, sha256 `107d6168aebfbe40d6552e2532e36cc8b103411c918b702776a0e06e9d4d4987`.
- **Graded** in `04` § Second opinion. Every confirmed item was re-read at its lines: `scripts/init` (`:86-99,143-174,298-331,340-376,394-437,610-666,825-906,1031-1145,1290-1320`), `input_sense` (`:90-106,176-226,280-372`), `userconfig-setup:66-90`, `autostart:78-97`, `systemd/package.mk:215-226,328-334`, `powerstate.sh:50-62`, `095-cloud-ssh:30-46`, and the autostart and udevil units. Upstream's `init` diff was read: the update code is unchanged; the reset and restore markers are removed by `a98a3066f5`.
- Grades: 26 confirmed (G-02, G-04, G-13 and G-23 at Medium), 6 narrowed, 2 not re-read (G-26, G-27).
- **Corrected from Astra's reading:**
  - `03` § 3.5's claim that `EnvironmentFile=/etc/profile` sources the profile (G-21);
  - F-07's "only on a `textmode` boot" (G-12, G-13);
  - F-04 to Medium.
- **Argon refutation**, in flight since 09:58: `tools/watch-build --record-only -- tools/council/run invoke --member gemini-argon --provider openrouter --prompt-file .../gemini-argon-brief.md --output .../gemini-argon-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`. The brief is 393,701 bytes: Argon's third-reader preamble, the Astra brief unchanged, and `04` § Second opinion appended. It was scanned three ways: 0, 0, 0. **What watches it:** the record `.build-runs/20261025T095741Z-4e1cd8de`, and the harness's background task.
- **My slip, corrected:** this entry's heading and `04`'s grading time were first written as 09:54-10:12 and 09:54-10:10, before the clock reached them. The real times are from `date -u` and the watcher: Astra ended 09:53:54 and Argon started 09:57:41.
- **Who carries what** (09:59, `grep -c -F` of each confirmed line at `8ebaf8daad`, `651150fc88` and `c445081a59`): the lines of G-23 (with its comment, upstream's `dc5f51ad72`), G-25, G-29, G-22, G-14 and G-15 are in all three, so they are upstream-carried and their class decision is #346. G-33's `tr -cd '0-9'` is in the read tree only: the fork's own. `04`'s G-23 row said "the fork's comment", which is corrected.

## 2026-10-25 10:05-10:08 UTC -- Argon graded; 04 complete; stage D's 05

- **Argon refutation** finished 10:05:08: watch-build rc 0, `build.rc` 0. The facilitator printed `attempt=1/4 ... model=google/gemini-4-argon providers=["Google"] effort=high reasoning=30565 content=19302b finish=stop outcome=success duration=444340ms`. Provenance: verification PASS (`provider_response`), provider PASS, effort PASS. Output sha256 `f075e46df8b5945249d1a4d9520977f351ff0909bf86482a1aa9b0740e8fe61a`.
- **Graded** in `04` § Second opinion. Every item was re-read at its lines: `init:60-64,287-292,537-592,712-717,760-765,1015-1028,1222-1227,1378-1383`; `input_sense:141-176,512-536`; `powerstate.sh:11-80`; `systemd/package.mk:256-323`; `busybox/package.mk:182-185`; `network-base-setup:76-116`; `udevil.conf:236-248` plus a `grep` for `allowed_options_btrfs` (none); the two units' `Before=`; `001-functions`; SM8550's `030-led-control`; `git ls-tree` for the two targets and for device `config/` directories (none).
- Grades: 12 items confirmed, of which 5 were narrowed (G-35 to dead code, G-36 to first boot) and 4 recorded as designs. G-26 and G-27 confirmed from the packet. The extensions to G-04, G-06, G-19, G-23 and G-32 confirmed. F-08's reset and restore markers re-graded to a Low defect, settled by the next base merge.
- **My slip, again:** the Argon section's grading time was first written as 10:05-10:20, ahead of the clock (10:07:05). Corrected. From here a time is written only after `date -u` has printed it.
- `04`'s risk table, opening and Q3 now carry both seats: F-04 Medium with G-44, F-07 as four paths, F-08 as above, and the seats' four Mediums (G-02, G-04, G-13, G-23).
- `review-plan.json`'s two statuses are complete, with each output's sha256.
- **Stage D:** `05` holds 28 items (5 Medium, 23 Low). Each item proposes its owner: #346 for upstream-carried lines, #740, a design sentence, *settled by the next base merge*, or a fork `bug` for G-33 (the fork's own). `lint-audit-artifacts --phase pre-issue`: `PASS pre-issue artifacts`.
- Four Mediums owe a VM proof (PL-01 btrfs, PL-03 the rejected update, PL-04 `debug-shell`, PL-05 the reader count), and so does G-33 (on the host first).
- **The audit issue** is #1103 (`Audit: M6 T22 the OS's system services and platform quirks -- 28 findings (0 critical, 0 high)`, labels `audit`, `punch-list`, M6), attached as a sub-issue of #669, with 28 checkboxes: `box-check --issue 1103` reads 0 fail.

## 2026-10-25 10:13-10:24 UTC -- the second window (granted 10:13 on #669)

- **Ruling read:**
  - bugs for PL-02, PL-03 and PL-05;
  - PL-01 decided by the window; PL-04 settled by the merge;
  - PL-28 a fork bug;
  - eleven Lows to #585 as lines in `05`;
  - PL-08 to #346, PL-10 to #740, PL-16 and PL-17 to #1104;
  - PL-20 the coordinator's rule edit; the rest recorded.
- Census: qemu 0, 10022 free. **START 10:14:56** (posted). The guest was stopped at 10:23:46 by owned pid; the leftover check reads 0; the record is `guest-cycle-2/`. `02` § The second window has the four cases.
- Writes on the disposable disk: two loop images, a staged `.tar`, and three reboots (the second, a backgrounded `reboot` over serial, did not happen; the boot id was unchanged; `systemctl reboot` in the foreground did).
- **PL-01:** udevil refuses btrfs (`denied 90: option 'compress=zstd:3' is not an allowed option`); the vfat control mounts with `nosuid,nodev,noexec`.
- **PL-04:** `debug-shell.service` active, a root `sh` on tty9.
- **PL-05: not reproduced.** The image's `input_sense` carries the fix (`6101242e14`, on the M7 line; read by diffing the installed file against the tree and by running the installed `get_devices` alone: `entries=3 after 5s`).
- **PL-03 proven:** no `/storage` after the rejection; the next boot whole.
- **The guest disk was retired** (D-INFRA-022): `/workspace/tmp/m6-t22/vm-pair/` (`vm-a.qcow2` 2,477,391,872 B, sha256 `83cfd747cb1baa95d37f844bd83838ed3da16c7e68380fc89a517af4be2eb29f`), 2,477,933,032 bytes in all. df: 1,635,229,728,768 bytes available before, 1637699203072 after, a measured 2469474304 bytes. The hash is provenance only.

## 2026-10-25 10:24-10:27 UTC -- stage D's outcomes; the bugs; the stage-E pause

- The bugs were filed with code traces, `Already written:` lines and VM lines: **#1105** (PL-02), **#1106** (PL-03, proven on the guest) and **#1107** (PL-28, the fork's own); `box-check` reads 0 fail on each. PL-10's comment is on #740 (issuecomment-6396488186).
- The coordinator's 10:25 ruling: PL-01 recorded as a Low on #585 (S4 struck); PL-05 deferred to #344 with `6101242e14` (S2 struck). The stream brief is `docs/reviews/briefs/t22-streams.md` at `a6e7a12ad6` (S1 `scripts/init`, S3 `095-cloud-ssh`), read with `git show`.
- `05`: every item has its outcome: 12 `deferred:#585`, 2 `deferred:#346`, `#344`, `#740`, 2 `#1104`, `#669` (the rule edit), the three bugs `deferred:#110x` until their streams' commits, and six `resolved # #669` (recorded designs). Also written: the #585 block (twelve lines, ready to paste) and the #346 root-surfaces sentence.
- #1103: all 28 checkboxes ticked (outcomes recorded); `box-check` reads 0 fail.
- `lint-audit-artifacts`: `PASS pre-issue artifacts` and `PASS` (resolution).

## 2026-10-25 10:30-10:38 UTC -- stage E: S3 and S1

- **S3** (`095-cloud-ssh`, #1107): the case `stage-e/s3/drive.sh` was written first, and the tree before the fix read `UNEXPECTED` as `fixed`. The fix is `9145b90fac`: the whole value judged, one journal line per refusal. The case then gained two boots of the whole quirk, for the bug's second criterion.
- **S1** (`scripts/init`, #1105 and #1106): the case `stage-e/s1/drive.sh` was written first.
  - **Fixture slips, each found by reading the fixture's own output before trusting a verdict:**
    - the driver's `set -u` reached `init`'s functions;
    - a returning `reboot` stub;
    - the host's `md5sum` (uutils) rejects `-s`, so the case now runs under **the initramfs busybox**, copied from the M7 build root into scratch (a read: nothing runs there), sha256 `4ce43643...`;
    - this busybox has no `--install` and its ash no `command` builtin, so a `command dd` stub exited 127 and the unfixed file printed `Update complete` over it;
    - the path rewrite missed `/storage;`;
    - a case with no calls had no `calls` file.
  - **The fix,** in two commits as the brief asks, PL-03 first because PL-02 uses its keep mode: `ffd1e34dbd` (`do_cleanup keep <why>`; the six normal-start rejections keep `/storage` and the update as `.rejected`) and `6cfe1fdba1` (checked writes; a staged pair committed only when whole, when `/flash` has room; `update_failed`; boot files' failure named; `dd` operands quoted). Both pass `busybox sh -n` and `bash -n`. The committed file is byte-identical to the tested one.
  - #1106's criterion asks for all six rejection paths, so cases f to j were added after the first passing run (netboot, missing target, missing source, incompatible, no room). An `exit 9` in the verdict, which would have ended a crossed run silently, became a helper returning a status.
- `run-all.sh` against the stage-D export (`git archive 0f7ece71e8`) and the fixed tree: **`run-all: PASS (8 of 8)`**.
- `05`: PL-02 `resolved # 6cfe1fdba1`, PL-03 `resolved # ffd1e34dbd` (the guest's after a fix-pending-image row), PL-28 `resolved # 9145b90fac`. Both lints PASS.

## 2026-10-25 10:41 UTC -- the initramfs busybox's provenance (the coordinator's 10:41 line)

S1's case runs under a copy of the image's initramfs busybox. Where it came from, all read by plain file reads; no process was started in that worktree:
- **The build root, at the copy:** `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64`. The file is `build/busybox-1.36.1/.x86_64-rocknix-linux-gnu-init/busybox`: 335,568 bytes, mtime 2026-10-05 03:37:22 UTC, reporting `BusyBox v1.36.1 (2026-10-05 03:37:08 UTC) multi-call binary`.
- **The root's head:** the worktree's `.git` points at `/workspace/repos/rocknix/.git/worktrees/m7-pixelelated-replacement20`, whose `HEAD` is `ref: refs/heads/build/m7-pixelelated-replacement20` at **`1a026648442321609b2288c2c9c06803817f9df2`**.
- **The copy:** `cp` to `/workspace/tmp/m6-t22/tmp/bb/busybox` at **2026-10-25T10:32:33Z** (the copy's mtime), sha256 **`4ce43643f300b585233e4723aaa3380d79d3b2bbe7a4ffaa540888041dbc13a6`**.
- **Its state:** it is in M6's scratch only. `lsof` shows no descriptor held on it, and none on the source. It is run only by `stage-e/s1/drive.sh` through `T22_BUSYBOX`. It goes with the scratch at the hand-back; M6 keeps its own copy for the acceptance re-run.

## 2026-10-25 10:45 UTC -- stage H: the scratch retired; #669's header; the hand-back

- **The scratch was retired** (D-INFRA-022): all of `/workspace/tmp/m6-t22/` (`artifacts`, `cycle`, `cycle.env`, `cycle2`, `run`, `tmp`, with the busybox copy, the stage-D export and the case scratch), 134,881,395 bytes. Nothing in it was open; every file was this user's; qemu 0. Both guest disks had already gone (00, 09:17 and 10:24). df: 1634983305216 bytes available before, 1634975244288 after.
- **#669's header:** `reviewed-at: 0f7ece71e8` (`git diff --stat 8ebaf8daad 0f7ece71e8 -- <the 422>` empty; `git diff --stat 4a48d388c4 0f7ece71e8 -- packages projects tools` empty) and `fixed-at: 6cfe1fdba1`. Since the stage-D tip only the two stream files changed under `packages/`, `projects/` and `tools/`.
- **The checkers on the branch:** `register-check` rc 0 (681 IDs), `work-log-index --check` current, `rules-check --quiet` rc 0, `forbidden-terms-check` 0 hits, `.githooks/hooks-test` PASS. `lint-audit-artifacts` passes in both phases.

## 2026-10-25 10:50-10:52 UTC -- close-out (the coordinator's 10:50 acceptance at `8a4d5eb5b2`)

- #1103 read back closed as completed at 10:50:32Z, 28 ticked and 0 open (`checks/phase7-closure/1103-readback.json`). `tools/lint-audit-artifacts <this folder> --issue 1103 --repo pixelelated/distribution` printed `PASS` (`resolution-lint.*`).
- `tracker-states.json` holds the state, close reason, body sha256 and checkbox counts of #1103 and every issue `05` tracks:
  - #344, #346, #585, #669, #740 and #1104;
  - #1105, #1106 and #1107, the three bugs, open with their fixes on this branch: #1106 with its two fix-pending-image criteria, the other two with 0 open checkboxes.
- `tracker-completion.json` is PASS, verified 10:51:05.789295Z.
- `audit-completion.json` (schema 1, issue 1103, `completed_at` equal to the receipt) binds `02`, `04`, `05` and the four receipts by sha256. `ceremony-check`'s own validator accepts it, and the full report is in `ceremony.stdout`.
- `/workspace/tmp/m6-t22/` was already gone (removed at stage H, 00); `ls` confirms.
