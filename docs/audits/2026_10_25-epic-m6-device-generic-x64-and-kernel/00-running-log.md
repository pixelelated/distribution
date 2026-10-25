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
- **07:11:53 UTC: the coordinator's answer** (07:10 UTC, #658): the M7-root reads are accepted as evidence with their provenance written, the recipe-only statement primary and the measurement its corroboration, and any further M7-root read gets a line here. `02` § The configuration now carries the primary statement, the corroboration, a provenance table and the transfer argument. `04` Q1 and the quality self-check say the same.
- **Every M7-root read so far** (A = `m7-signin-generic-build-20261025-01` at `bcc866f1f3`, B = `m7-pixelelated-replacement20` at `1a02664844`; read-only, nothing written or started there):
  - between 06:48 and 06:56:11 (not timed one by one): `ls -d` of both roots' `build/linux-*`; `stat` and line 3 of both `.config`s; the copies `built-a.config` and `built-b.config` (mtime 06:52:01, both sha256 `e769f2e5fe2ebe9d...`); `git -C` `log -1` and `diff --quiet` on both worktrees; `grep` of A's `.config` for `PREEMPT`, `IKCONFIG` and `USB_GADGET`; `du` and `find` on A's `install_pkg/kernel-firmware-20260309` and `image/system/.../firmware`; `ls -la` of A's `target/`; `stat` of A's bzImage; `du` and `find` on A's `external-firmware`; existence tests of three firmware files in A's install tree;
  - 06:56:12: r24, r25 and r26 (`runs.tsv`), over A;
  - 07:10: `git -C` `branch --show-current`, `rev-parse HEAD`, `diff --stat` / `--quiet` and `log -1` on the conf for both A and B (the transfer argument);
  - 07:10:54: `stat` of A's firmware tree, bzImage, `.config` and `external-firmware`, and B's `.config` sha256 re-read.
- **The packet and the edited `02`:** the seat received `02` as it stood at 07:05 (manifest sha256 `4071b371a7280110...`). The 07:11 edits change the framing and add the provenance table and transfer argument, not a figure or a finding. The seat's items are graded against the code, and any that turns on the framing says so.
- **The refutation** returned at 07:22:52 UTC, rc 0 (`/workspace/tmp/m6-t11/refutation.rc`): `attempt=1/4 http=200 model=openai/gpt-6-astra providers=["OpenAI"] effort=max reasoning=31521 content=23630b finish=stop outcome=success duration=839998ms`. Provenance: verification `PASS` (semantic, from the provider's response), effort `PASS`, provider `PASS`, `council-facilitator@1.14.1-pixelelated.2`. 36 items (the seat's labels: 13 confirmed, 14 narrowed, 9 new). **That was the last `tools/council/run invoke`.**
- **The lane's re-reads** (`02` § Stage C re-reads): G-8 refuted by `CONFIG_CFG80211=m`; G-24 and G-25 confirmed from the override's `:1-20`, `73b20caf86`'s message and `872b13a3b3`; G-31, G-33 and G-34 re-read at their lines; no `scripts/cleanup.sh` in the tree (G-28).
- **A further M7-root read** (the coordinator's 07:10 condition), 07:25:12 UTC: `cp` of `/workspace/repos/rocknix.worktrees/m7-gtk4-build-20261017-01/build.pixelelated-GENERIC_X64.x86_64/toolchain/bin/mtools` (mtools 4.0.49, sha256 `2050c806846eedb3...`, libc only) to `/workspace/tmp/m6-t11/mcopy-test/bin/`. It ran there, not in that tree, as T5's P15 had done. **G-26 is refuted:** `mcopy -i part.fat src/rocknix_abl ::` without `-s` copied the directory and both files, rc 0, the same listing as with `-s` (P19).
- **The corrections from the seat:** `02`, `03` and `04` corrected per `04` § Second opinion. Among them: the recipe's edits (G-1), `any.dat` (G-4), the launcher's extra devices (G-5), F-01's scope (G-6), F-02's mixed payload (G-7), the `grub` branch's consequence (G-12), F-09 to a broken build (G-24), and the ancestry claim withdrawn (G-25). Four findings added, F-11 to F-14, and P19 and P20. The coverage generator was resynced: still 58 rows.
- **`05`:** PL-01 to PL-14, all Open, with the `punch_index`. `tools/lint-audit-artifacts <folder> --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)`, at 07:30:11.
- **Stage C ends 07:30 UTC.** No guest, build, compiler, plan generation, fetch or handheld. The `tools/council/run` calls were two keyed (the probe and the refutation) and three keyless (`COUNCIL_ENV_FILE=/nonexistent`: `invoke --help` rc 127 before the copy, `verify-pins`, `invoke --help`). Nothing was written under `/tmp`, `/workspace/repos/rocknix*`, another lane's worktree, `packages/` or `projects/`. Under `tools/`, only the gitignored `tools/council/node_modules` was written, and nothing tracked changed.

## [Stage D] 07:35 to 07:38 UTC — the bugs, the audit issue, the outcomes; the pause

- **The coordinator's dispositions** (07:34 UTC, #658): five bugs for the lane; PL-06 removed in stage-E stream S1 (the coordinator's decision on fork-own dead code); PL-07 to #1085, PL-01 to #1083, PL-04 to #1084 (Backlogs the coordinator filed); PL-02, PL-05 and PL-09 recorded; PL-03 and PL-10 resolved in the stream.
- **The bugs**, bodies in `/workspace/tmp/m6-t11/posts/`, scanned before filing (`forbidden-terms-check --stdin` 0 hits; `SECRET_PATTERNS` 0 lines), each with a code trace, an `Already written:` line and a host fixture as its VM line. Label `bug`, milestone M6. `tools/box-check --issue N`: 0 fail on each.
  - #1086 (PL-08, the inventory, `2174265e9c:tools/renovation-inventory:465-468`, `:474-476`): 2 checkboxes;
  - #1087 (PL-11, the modeswitch rule's line 7): 2 checkboxes;
  - #1088 (PL-12, `dtb_overlay`): 3 checkboxes;
  - #1089 (PL-13, the launcher): 2 checkboxes;
  - #1090 (PL-14, `install` and `release`, a sibling of #827): 3 checkboxes.
- **`05`:** every item at its Phase 7 outcome: 11 Deferred (to #1083, #1084, #1085, the five bugs, and #658's stream for PL-03, PL-06 and PL-10) and 3 Resolved as recorded at `b501bdad67` (PL-02, PL-05, PL-09). `tracked:` and `outcome:` are in the `punch_index`; the five bug items carry `Bug issue:`. `tools/lint-audit-artifacts <folder>` (resolution phase): `PASS`.
- **The audit issue:** #1091, labels `audit` and `punch-list`, milestone M6, a sub-issue of #658 (`gh api .../658/sub_issues` lists `[1091]`): 14 checkboxes, `box-check` 0 fail. `tools/lint-audit-artifacts <folder> --issue 1091`: `PASS`.
- **The removal rule at the stage-D tip:** `git diff --stat 2103f0271d HEAD -- packages projects tools` is empty.
- **The pause:** the stage-E stream brief is the coordinator's (S1 `install` and `release`; S2 the launcher; S3 the udev rule and `options`; S4 `dtb_overlay`). No guest, build, compiler, plan generation, fetch, handheld or `tools/council/run` call at stage D.
