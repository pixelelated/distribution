# Running log — M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`), after T25's close-out.
- **Brief:** `docs/reviews/briefs/device-sm8550.md`, version 2 (`5f4430f676`). **Dispatch:** the coordinator's comment on #675, 10:31 UTC on 2026-10-25 (issuecomment-6396531859).
- **Depth:** Independent, with one seat (GPT-6 Astra at `max`) over a trimmed, scanned packet (D-WORKFLOW-195).
  - **Exactly one keyed `tools/council/run invoke` pair:** the probe and the refutation, at stage C.
  - Every other `tools/council/run` call runs with `COUNCIL_ENV_FILE=/nonexistent`, `--help` included.
- **`reviewed-at`:** `458e2bfda1`, the dispatch tip. The read is of `8ebaf8daad`'s bytes: the branch-vs-hash diff over the 29 is empty (r03), and so is `git diff --stat 8ebaf8daad HEAD -- packages projects`. Upstream is read at `651150fc88` and the base at `c445081a59`, both from the repository's own store. No fetch.
- **Can this be done on the VM? Yes, on the host, with no network.** Every read, diff, log and script read runs on the build host at `8ebaf8daad`, with `651150fc88` read locally.
  - The GENERIC_X64 guest cannot be an SM8550, so **no guest is asked for**.
  - A fact only the Nova can show is a `device-facts.md` row (L17 to L20, L27, L28, L31), read and cited, **never produced here**. The Nova is a person's device (D-QA-015, D-QA-027).
- **What never runs here:** a build, a compiler, a plan generation, a guest, a fetch, a network read of any upstream or author, a command against the Nova or any handheld, an M7 build root read, a keyed `tools/council/run` call beyond the seat's two, or a change under `packages/`, `projects/` or `tools/` at stages A to D.
- **The host:** the host file's last line at 10:31 is the coordinator's 10:24 UTC *T22 SECOND GUEST WINDOW RETURN ... M6 runs no guest now*. Census: qemu live 0; `/tmp` inodes 41 %.
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t28/tmp`, `.qa-scratch/t28/`; copies in `stage-a/`.
- **Proofs:** each proof in `02`'s § Proofs has one numbered proof line here, in its stage.

## [Stage A] 10:31:53 to 10:33 UTC — the first commands, the block, the runs

- **The first commands** (brief § 1), 10:31:53:
  - the status is clean (0);
  - the tip is `458e2bfda1`, on `4beb95adf6` and `5f4430f676`;
  - stacked on `8ebaf8daad` and on P1's `2174265e9c`;
  - `[]` against `8ebaf8daad` under `packages` and `projects`;
  - `651150fc88` is present;
  - `register-check` ok; D-WORKFLOW-209 present (1); the inventory present.
- **The runs:** `stage-a/runs.sh`, 31 steps from 10:32:32 UTC, each with its exit and wall time (`stage-a/runs.tsv`). **All exit 0.** The `grep -c` steps that could print 0 are wrapped (`|| true`, or a `wc -l` count), so none exits 1.
  - r01, the block: `paths 29 lines 28053 {'shipped': 29} {'upstream-carried': 29}`; `{'shell': 2, 'other': 3, 'yaml': 8, 'devicetree': 16}`; `read 2 118 fork-own 0`; `whole directory in the inventory 85 57561 {'devices': 29, 'patches-and-configs': 56}`; `paths.txt` 29.
  - r04: 28,053 lines by `wc -l` at the hash. r05: the `.disabled` patch has 20,593 lines.
  - r06, r07: the configuration's header is `# Linux/arm64 7.2.0 Kernel Configuration`, 8,608 lines. Against `651150fc88`'s copy: **removed 7, added 7**, the compiler stamps (gcc 16.2.0 / 15.2.0), RUSTC and LLVM ×3, `CC_HAS_COUNTED_BY_PTR=y` / `# INPUT_POLLDEV is not set`, and `RAID6_PQ_BENCHMARK`.
  - r08: `SM8650 41/36 SM8750 81/105 SM6115 228/133 SM4450 229/189 SM8250 371/204`. **Delta:** the brief's command prints each pair reversed from the brief's text (36/41, 105/81, ...). Each count is the same; only the order differs.
  - r09: 0 fork non-merge commits on the conf since the base. r10: upstream's four (`dcafa74090`, `6fbefc45c6`, `5f56cd5150`, `c0980b2b71`).
  - r11: the kernel's `7.2` at the hash. At `651150fc88` SM8550's case is `:35`, `7.2` with the same sha. The `7.2.11` at `:30` is RK3566/RK3576/S922X's (`c803640655`), not SM8550's.
  - r12: the pins.
    - `qcom-abl` `1.0` at both hashes.
    - `rocknix-abl` `1.2`, then **absent**.
    - `mkbootimg` `d2bb0af5...`, then **absent**.
    - `extra-firmware` `88b363e6...` / `925dfb5e...` (**differs**).
    - `kernel-firmware` `20260309` at both.
    - `inputplumber` `v0.79.0` / `0.82.0` (**differs**).
    - `gamepadcalibration` identical.
    - The masking `sed` masked nothing on these lines.
  - r13: `9aa7affee9` (blitterbot, 2026-10-15, #600) and `b354bfe6d6`. r14: openabl `1.2` at `651150fc88`; `71d8932b33`, `a5d0dd4d57`, `73ffb8ee37`.
  - The boot path:
    - r15, `update.sh`: `:10-12` `BOOT_DISK`; `:19-22` `rocknix_abl`; `:25` `updateabl`; `:29-30` the two `rm -rf`; `:37` `.boot.hint`.
    - r16, `scripts/mkimage`: `:257`, `:259` and `:265` name `qcom-abl`.
    - r17, `bootloader/mkimage`: `:22-25` the `rocknix-u-boot.img` branch (*"SM8750, SM8650 & SM8550"*); `:81` the `SM8550|...)` case; `:110` `rocknix_abl`.
    - r18, the kernel recipe: the dtb loop appends to `kernel.gz`, then `mkbootimg.py`.
    - r19: the embed condition at `:83` names SM8250, H700, SM8650 and SM8750, **no SM8550**.
    - r20: 14 `<file>` entries. r21: `updateabl`'s compare and its two `dd`s.
  - The trees: r22, 16 sources. r23, the Nova's include (`qcs8550-retroidpocket-rp6.dts`), `model = "Retroid Pocket Nova"`, its compatible, and its panel `il97680a,rpnova`. r24: `16 0`, no `rocknix-dt-id`.
  - History:
    - r25: 24 non-merge, fork 0, 27 with merges; directory 54 / 63; bare date 52, T27's erratum reproduced.
    - r26: `--no-merges` 0; without it the fork's two upstream merges, `7bd7f31312` and `7650de7dd6`.
  - The upstream delta:
    - r27, over the 29: **2 M** (`update.sh`, `options`), +20 / -14.
    - r28, over the directory: **4 M 2 A**, +451 / -22.
    - r29: 18 commits, 10-01 to 10-24.
  - r30: `Makefile:39,42,98-101`; `config/options:31` `export DEVICE="SM8550"`. r31: `[]` against the dispatch tip under `packages projects tools`.
- **Nothing of the never-run list ran.**
- PROOF: P1, the membership: r01, r02, r04.
- PROOF: P2, the history and the delta: r25 to r29.

## [Stage B] 10:34 to 10:43 UTC — the sections, the generator, the corrections

- **The reads:** `stage-b/reads.sh`, 21 steps from `stage-b/runs.tsv`'s first start, all rc 0. b01 to b20 are the sources behind `02`'s sections; `g_check` is the generator's `check` and `counts`.
- **The generator:** `tools/t28-tables.py` writes § The runs (31 rows, each with *a FAIL would mean*), § The pins (8), § The device trees (16 + the `.disabled` row) and § Coverage (29). Each section asserts its count, and `check` exits 1 on drift. `counts`: carried by placement 20, disabled 1, shipped 3, shipped unit 5, total 29.
- **Corrections to the brief, recorded in `02` § Deltas:**
  - two InputPlumber files serve the Nova (`02-ayn-controller.yaml:44` `value: Retroid Pocket Nova`);
  - the Nova's include chain is part of the shipped unit;
  - r08's pair order;
  - `gamepadcalibration`'s file differs upstream in SM6115's branch only (`48b98a02d7`).
- **Citations corrected before commit:**
  - the brief's `install:50-60` is `projects/ROCKNIX/bootloader/install:50-61`, not `scripts/install`;
  - `kernel-firmware`'s die line is `:57` within `:39-70`.
- **Upstream's loader entry:** `virtual/arm-efi/package.mk:13-23` at `651150fc88` writes `${DISTRONAME,,}.conf`. On the fork that is `pixelelated.conf`, with `boot=LABEL=ROCKNIX`: #1099's seam, cited.
- **Findings:** eight, 2 Low (F-04, F-05) and 6 Info. No `bug`.
- **Nothing of the never-run list ran.** No council call yet: the seat is stage C's.
- PROOF: P3, the branch and the removal rule: r03, r31.
- PROOF: P4, the configuration: r06 to r10.
- PROOF: P5, the pins: r11 to r14, `g_check`.
- PROOF: P6, the build side of the boot path: r16 to r18, r20, b07, b08, b09, b10.
- PROOF: P7, the update side: r15, r21, b04, b05.
- PROOF: P8, the embed reading: r19, b01, b02, b03.
- PROOF: P9, the trees: r22 to r24.
- PROOF: P10, the Nova's input files: b13.
- PROOF: P11, the two branches that never run: b09, b07.
- PROOF: P12, upstream's replacement and the entry's name: r29, b11, b12.
- PROOF: P13, the device facts: b19.
- PROOF: P14, the tables regenerated: `g_check`.

## [Stage C] 10:45 UTC onward — the packet, its scan, the seat

- **The packet** (`stage-c/packet.py`, from `stage-c/ask.md`), `second-opinions/gpt-brief.md`: 72 sources, 377,172 bytes, sha256 `90fdaca720aa5fa8...`. Built 10:45:39 UTC.
  - **Contents:** the ask; `02`, `03` and `04` whole; five context sections (the order's § T28, the brief's § 2 and § 4, 10 register rows, device-facts L17 to L20, L27, L28 and L31 at `2174265e9c`, `device-builds.md:16-26`).
  - **Line-numbered:** the 28 slice files that are not the `.disabled` patch; that patch's first 12 lines; the configuration's header and its diff against upstream's copy (asserted 7 / 7); the four Qualcomm confs' `DRM_MSM` and `EXTRA_FIRMWARE` lines; and 31 excerpts at `8ebaf8daad` and `651150fc88`.
  - **Masking:** every source passed the masking `sed`'s rule; **2 lines were masked**, both `key=lambda` in the brief's own § 2 block.
- **The scan, before sending** (10:45:58):
  - `forbidden-terms-check --stdin`: 0 hits.
  - `SECRET_PATTERNS`: 0 lines under this branch's, the primary checkout's and T10's widened sets. Each set matched a `devpassword=` line assembled at run time. No redaction.
  - Recorded in `packet-manifest.json`'s `scan`.
- **The plan:** `second-opinions/review-plan.json`: `depth: independent`, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`, pinned to OpenAI, `allow_fallbacks: false`), written before the first call.
- **The runner's dependencies:** `tools/council/node_modules` was copied from the T27 worktree (gitignored; the tracked `tools/council` is identical to T27's), since a fetch is forbidden. `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`. Earlier, `COUNCIL_ENV_FILE=/nonexistent tools/council/run --help`, also keyless.
- **The probe**, 10:46:28 to 10:46:38 (keyed; **the first of the seat's two calls**):
  - `attempt=1/4 http=200 model=openai/gpt-6-astra providers=["OpenAI"] effort=max finish=stop outcome=success`.
  - Provenance: verification `PASS`, `observed: openai/gpt-6-astra`, `model_identity_source: provider_response`; `council-facilitator@1.14.1-pixelelated.2`.
  - The reply text is `READY unknown`: the model's own claim, which the provider's identity overrides.
- **The refutation**, started 10:46:53 UTC (keyed; **the second and last call**), runs as a harness background task. It writes `second-opinions/gpt-audit.md` and `/workspace/tmp/m6-t28/refutation.rc`; the task notifies this session when it ends.
