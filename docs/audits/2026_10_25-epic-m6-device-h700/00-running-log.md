# Running log — M6.P2 T27, the H700 device (RG35XX SP, RG SP) (#674)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, the T5 session (`m6-t5-build-engine`), after T11's close-out.
- **Brief:** `docs/reviews/briefs/device-h700.md`, version 3 (`cc8b6cf2a3`, the same bytes at the branch's `HEAD`).
- **Dispatch:** the coordinator's comment on #674, 08:09 UTC on 2026-10-25.
- **Depth:** Independent. One seat, GPT-6 Astra at `max`, a probe first, at stage C. It is the only `tools/council/run invoke`; every other `tools/council/run` call carries `COUNCIL_ENV_FILE=/nonexistent`.
- **`reviewed-at`:** `ed7fd0ea50`, the dispatch tip and the branch `HEAD` at stage A. The read is of `8ebaf8daad`'s bytes: `git diff --stat 8ebaf8daad HEAD -- packages projects` is empty (r16). Upstream is `651150fc88`, read locally with `git rev-parse`; no `git fetch` was run.
- **The rule (D-WORKFLOW-209):** at stages A to D the lane changes none of the 28 and nothing under `packages/`, `projects/` or `tools/`.
- **No guest, no build, no compiler, no plan generation, no fetch. Nothing against a handheld:** no `ssh`, `scp` or `device-act` to the RG35XX SP or the RG SP (D-QA-015, D-QA-027). A device fact is a `docs/releases/device-facts.md` row, read.
- **One recipe line matches the credential read filter** (`h700-suspend-stub/package.mk:43`, a build flag). Every recipe read here passes the masking `sed` (`s/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig`), and the line is never quoted raw.
- **Scratch:** `TMPDIR=/workspace/tmp/m6-t27/tmp`. Outputs are under `.qa-scratch/t27/` and `/workspace/tmp/m6-t27/runner/`, with copies in `stage-a/`.
- **Prose** goes in through a quoted heredoc or the Write tool; **times** come from `date -u`.

## [Stage A] 08:09:41 to 08:11 UTC — scope, the configuration, the pins, the loader and the trees, the history, the upstream delta

- **The first commands** (brief § 1), 08:09:41:
  - the branch is `feature/m6-device-h700-674`, stacked on P1 (`2174265e9c`); `inventory.json` is present;
  - `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` gives 8 files, the dispatch's eight;
  - `651150fc88` is in the repository;
  - `rules-check --quiet` rc 0; `register-check`: 681 IDs;
  - `df -i /tmp`: 41 %. Nothing was written there.
- **The host before anything ran:** the host file's last line is the coordinator's 07:53 UTC T13 guest-cycle start. Census: qemu 0 (T13's guest had stopped), compilers 0.
- **The runs:** `stage-a/runs.sh`, 16 read-only steps from 08:10:10 UTC, each with its exit and wall time (`stage-a/runs.tsv`). **All exit 0.**
  - r01, the membership: paths 28, lines 12,901; read 8 / 327 / fork-own 0; tier `upstream-carried` 27, `vendor-carried` 1; reach shipped 28; languages as the brief; written 28.
  - r02 and r03, the configuration: `# Linux/arm64 7.2.0 Kernel Configuration`, 8,129 lines; against `651150fc88`'s own copy **removed 12, added 13**.
  - r04: the fork's edits since the merge base `c445081a59` are `cbf75c0b06` (2026-09-10) alone. r05: upstream's four since: `c0980b2b71` (10-02), `5f56cd5150` (10-04), `6fbefc45c6` (10-18) and `dcafa74090` (10-22).
  - r06: the kernel is `7.2` for `H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750`.
  - r07, the pins, read through the masking `sed`, the same at both hashes: u-boot-DDR3 and -DDR4 `v2026.01`, sha256 `03bb43c58d23...`; the suspend stub `712653d11230...`, sha256 `3698da9aad40...`; the wrapper `1.0`.
  - r08: the two defconfigs differ in 20 lines.
  - r09: `update.sh` writes `dtb.img` (`:30-31`), finds `vdd-dram` (`:36`), reads `microvolts` (`:40`) and `dd`s the loader `bs=1K seek=8` (`:55`).
  - r10: the project `mkimage` writes the H700 SUBDEVICE's loader (`:18-21`) and copies `device_trees` (`:26`). No line names `dtb.img`.
  - r11: `SUBDEVICES` comes from `config.xml` through `xmlstarlet` (`functions:224`).
  - r12 and r13: 15 trees; 13 include a mainline board file and 2 a fork sibling; each carries its own `rocknix-dt-id`.
  - r15, the upstream delta: **1 D** (`80-clock.rules`) and **2 M** (`linux.aarch64.conf`, `options`).
  - r16: the removal rule; both diffs empty.
- **A delta, explained:** r14's history printed **28 / 1 / 27**, not the brief's 29 / 1 / 28. `git log --since=2026-06-01` reads a bare date at the current time of day: run at 08:10, it excluded `efae8a5653` ("Update kernel configs", committed 2026-06-01T08:07:03Z). With `--since='2026-06-01T00:00:00Z'` the count is **29; fork 1; upstream 28**, the brief's figure, at any hour. A friction line is written.
- **Nothing written** under `/tmp`, `/workspace/repos/rocknix*`, another lane's worktree, `packages/`, `projects/` or `tools/`. No guest, build, compiler, plan generation, fetch, handheld command or `tools/council/run` call.
