# Running log — M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the boot files (#658)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`).
- **Brief:** `docs/reviews/briefs/device-generic-x64-and-kernel.md`, version 2 (`5bb8828b71`, the same bytes at the branch's `HEAD`).
- **Dispatch:** the coordinator's comment on #658, 06:43 UTC on 2026-10-25.
- **Depth:** Independent. One seat, GPT-6 Astra at `max`, a probe first, at stage C. It is the only `tools/council/run invoke`; every other `tools/council/run` call carries `COUNCIL_ENV_FILE=/nonexistent`.
- **`reviewed-at`:** `2103f0271d`, the dispatch tip and the branch `HEAD` at stage A. The read is of `8ebaf8daad`'s bytes: `git diff --stat 8ebaf8daad 2103f0271d -- <the 58>` is empty. Upstream is `651150fc88`, read locally with `git rev-parse`; no `git fetch` was run.
- **The rule (D-WORKFLOW-209):** at stages A to D the lane changes none of the 58 and nothing under `packages/`, `projects/` or `tools/`.
- **No guest, no build, no compiler, no plan generation, no fetch, no handheld.**
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t11/tmp`. Outputs are under `.qa-scratch/t11/`, and copies are in `stage-a/`.
- **Prose** goes in through a quoted heredoc or the Write tool; **times** come from `date -u`.

## [Stage A] 06:44:34 to 06:46 UTC — scope, the configuration, the history, the upstream delta, the boot files, the launcher

- **The first commands** (brief § 1):
  - the branch is `feature/m6-device-generic-x64-658`, stacked on P1 (`2174265e9c`); `inventory.json` is present;
  - `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` gives 8 files, the dispatch's eight;
  - `git rev-parse --verify 651150fc88^{commit}` succeeds: the commit is in the repository;
  - `git diff --stat 2103f0271d HEAD -- packages projects tools` is empty, and so is `git diff --stat 8ebaf8daad HEAD -- packages projects`;
  - `rules-check --quiet` rc 0; `register-check`: 681 IDs;
  - `df -i /tmp`: 41 %. Nothing was written there.
- **The host before anything ran:**
  - The host file's last line is the coordinator's 06:40 UTC release of the H700 caches to the M7 lane. That is not this lane's.
  - Census: qemu 0, compilers 0.
- **Membership** (§ 2's block at `2174265e9c`; `stage-a/scope.out`):
  - paths 58, lines 10,418;
  - read 14, 1,820 lines, 1,421 of them fork-own;
  - tier: fork-own 11, upstream-carried 46, vendor-carried 1;
  - reach: shipped 49, test 9;
  - **GENERIC_X64 fork-own lines 1,217** (the order's 989 is an erratum).

  `paths.txt` has 58 lines, and the 58 are byte-equal to `8ebaf8daad` (`git diff --stat` empty).
- **The configuration** (`stage-a/config.out`):
  - `projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf` is 7,754 lines, and its header (line 3) reads `# Linux/x86 6.15.6 Kernel Configuration`.
  - Against `projects/Generic/linux/linux.x86_64.conf` (8,062 lines, `7.1.2`): **removed 659, added 351**.
  - Against `projects/ROCKNIX/devices/AMD64/linux/linux.x86_64.conf` (12,445 lines, `7.1.2`): **removed 7,671, added 2,980**.
  - The override recipe sets `PKG_VERSION="7.1.2"` for `RK3326|AMD64|GENERIC_X64` (`package.mk:36-38`); the default is `7.2`.
  - `listnewconfig` is at `:306`; `oldconfig` at `:309` and `:315` (`yes "" | kernel_make oldconfig`).
  - The fork's edits since the adding commit `73b20caf86` (2026-06-30): `1cd0093d67` (2026-07-26) and `cbf75c0b06` (2026-09-10).
- **The history since 2026-06-01** (`stage-a/hist.txt`): **110** non-merge commits on the 58. **40 fork** (Max Engel 36, blitterbot 3, rasterabot 1) and **70 upstream**.
- **The upstream delta at `651150fc88`** (`stage-a/upstream-delta.txt`):
  - **7 M:** `bootloader/mkimage`, `config.xml`, `rocknix-joypad`, `extra-firmware`, `linux/package.mk`, `qdisc.conf`, `10-bfq-sched.rules`;
  - **11 D:** the fork-only files (the GENERIC_X64 device's nine, `bootloader/install`, `machine-info`).
- **The boot files** (`stage-a/runs.out`):
  - `scripts/image:280` runs `bootloader/install`; `:285` runs `bootloader/release`; `scripts/mkimage:225-263` sources `bootloader/mkimage` (three blocks).
  - `install` is **fork-only** (`git cat-file -e 651150fc88:...` fails), yet line 2 reads `# Copyright (C) 2024-present ROCKNIX`.
  - Its branches: `syslinux` (14), `grub` (25), `systemd-boot` (35), `u-boot` (45, echo), `qcom-abl|arm-efi` (50, echo with the image-time note at 59), empty (`:64`) and `*)` (68).
  - **`BOOTLOADER=`** per device: H700 `u-boot`; SM8550 `qcom-abl`; GENERIC_X64 and AMD64 `syslinux`; every Rockchip `u-boot`; every other Qualcomm `qcom-abl`. No device sets `grub` or `systemd-boot`.
  - **`rkhelper`** is read by seven Rockchip u-boot recipes (RK3566 ×2, RK3588, RK3326 ×2, RK3576, RK3399) and by no shipped device.
- **The generic recipe's mark:** `packages/linux/package.mk` reads fork-own because of one fork commit, `3d7c075f63` (2026-10-02, blitterbot, *identity: prepare Rasteratops 0.0.1 source inputs*). The next four commits are upstream's (Matthias Reichl, RPi kernel bumps).
- **The launcher** (`stage-a/launcher.out`):
  - `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm` is 817 lines, 19 functions, git mode `100755`, with the header `# Copyright (C) 2026 ROCKNIX`. There is no `tools/generic-x64-vm`.
  - **The callers reach it by path, not by basename.** `tools/vm-pair:36` sets `VM_TOOL="$ROOT/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm"` and `:74` runs `"$VM_TOOL" run --headless --daemonize ...`. The rule's `VM_TOOL=` lines (`generic-x64-vm-testing.md:83`, `:107`) do the same. `tools/last-good-scripts-test:3406-3571` uses the full path in its fixture.
  - The basename appears only in comments and help text: `tools/vm-serial:8`, `tools/cloud-test-backend:8`, and `tools/cloud-round-trip:504/513/607` (help strings). This is a delta from the brief's *call it by basename*.
- **Nothing written** under `/tmp`, `/workspace/repos/rocknix*`, another lane's worktree, `packages/`, `projects/` or `tools/`. No guest, build, compiler, plan generation, fetch or `tools/council/run` call.

## [Stage B] 06:48 to 07:04 UTC — Phase 1 and 2, the runs, `02`, `03`, `04`, the review plan

- **The coordinator's answer** (06:47 UTC, #658): § The launcher records the resolution as found, `tools/vm-pair` by full path through `VM_TOOL`; the brief's *by basename* is an erratum for acceptance.
- **The runs:** `/workspace/tmp/m6-t11/runner/runs.sh`, 28 read-only steps started at 06:56:11 UTC, each with its exit and wall time. All exit 0 but r28, whose exit 1 is `grep -c` printing the expected 0. Copied to `stage-b/runs/`, with the runner, `cfgclass.py` and `coverage.py`.
- **Read beyond the 58:** `scripts/image`, `scripts/mkimage`, `config/functions`, `packages/virtual/image`, the `syslinux`, `installer`, `grub`, `rocknix-abl` and `rocknix` recipes, every device's options and firmware list, `tools/vm-pair`, the inventory's tier rule, the 2026-10-11 usb-revision proof. Cross-slice records read with `git show`: T5's F-16/F-17 and E6, T40's x86_64 five, T12's harness rows.
- **Read from the M7 lane's build root, read-only** (`/workspace/repos/rocknix.worktrees/m7-signin-generic-build-20261025-01`):
  - the built kernel `.config` (sha256 `e769f2e5fe2ebe9d...`, equal to `m7-pixelelated-replacement20`'s; the M7 head `bcc866f1f3` carries the committed conf unchanged);
  - the installed firmware tree (6,158 files, 2,876,913,748 bytes);
  - the bzImage's size and the embedded firmware's source.

  Copies went to `/workspace/tmp/m6-t11/cfg/`. Nothing was written in that tree, and no process there was touched.
- **Corrections before commit:**
  - three line ranges in `02` (`:197-207`, `scripts/image:272-289`, the shipped `init:432`);
  - Q5's claim that ours adds the GPU drivers (the Generic conf has them; the Generic file's 7.1.2 header makes part of the 659 / 351 drift);
  - `03`'s *five* overlay sources, which are six.
- **Findings:** F-01 (Medium) to F-10; no `bug` proven. The one proof that read the committed configuration (`usb-revision/guest02/run.py:15`) holds in the built file.
- **Nothing written** under `/tmp`, `/workspace/repos/rocknix*`, another lane's worktree, `packages/`, `projects/` or `tools/`. No guest, build, compiler, plan generation, fetch or `tools/council/run` call.

## [Stage C] 07:05 UTC onward — the packet, its scan, the seat

- **The packet** (`stage-c/packet.py`, from `stage-c/ask.md`), `second-opinions/gpt-brief.md`: 46 sources, 247,469 bytes, sha256 `a61ed1b792dbae62...`. It holds the ask, `02`, `03` and `04` whole, and three context sections (the order's § T11, the brief's § 2 and § 4, the rows D-WORKFLOW-185/186/187 and D-QA-053). Then, line-numbered: the 14 read paths, the four bootloader scripts, the conf's header and its diff against the Generic conf (asserted 659 / 351), and 19 excerpts of the code `02` cites. Every source is in `packet-manifest.json` with its sha256.
- **The scan, before it was sent** (07:06-07:07):
  - `tools/forbidden-terms-check --stdin`: `0 hits on stdin`, rc 0;
  - `SECRET_PATTERNS`: 0 lines under this branch's set and the primary checkout's (`57fd72093984`), and 0 under T10's widened set (`7295e68fd978`, read with `git show feature/m6-tooling-guards-657`);
  - the positive control: each set matched a `devpassword=` line assembled at run time. No redaction.
- **The runner's dependencies** (07:08:02): the worktree had no `tools/council/node_modules`, and the brief forbids every fetch, so `npm install` was not run. The install was copied locally from the T5 worktree (`cp -a ../m6-build-engine-652/tools/council/node_modules`): tracked `tools/council` is identical at `5f1b343d25`, and the installed lockfiles are equal (`ad7b5358...`). The directory is gitignored (`git check-ignore`), and `git status` showed nothing under `tools/`. A friction line is written (`issue: #658`).
- **Keyless calls:** `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`, rc 0. `COUNCIL_ENV_FILE=/nonexistent tools/council/run invoke --help`: usage, rc 0. One earlier keyless call, at 07:07:28, failed rc 127 before the copy (`tsx` missing).
- **The probe**, 07:08:17-07:08:27, `tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-probe-prompt.md --output second-opinions/gpt-probe.md` (keyed; the first of the seat's two calls): `http=200 model=openai/gpt-6-astra providers=["OpenAI"] effort=max reasoning=279 finish=stop outcome=success`. Provenance: verification `PASS` (semantic, from the provider's response), effort `PASS`, provider `PASS`, `facilitator_version` `council-facilitator@1.14.1-pixelelated.2`. Its reply was `READY unknown`: the identity is the provider's field, not the model's own.
- **The refutation**, started 07:08:52 UTC, `tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-brief.md --output second-opinions/gpt-audit.md` (keyed; the second and last call). It runs as the harness background task `bc29oco8c`, which notifies the session when it exits, and writes `/workspace/tmp/m6-t11/refutation.rc`.
