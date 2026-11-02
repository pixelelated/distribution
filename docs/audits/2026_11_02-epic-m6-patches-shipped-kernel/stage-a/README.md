# Stage A scripts and outputs — T41 (`patches-shipped-kernel`, #688)

Stage-A verification outputs produced by the brief's § 5 `# STAGE A` commands at `f03b64419f` (`2026-11-02T05:27:50Z–05:30:28Z`).

- `block.sh` — § 2 membership block extracted by markers from `9313492990:docs/reviews/briefs/patches-shipped-kernel.md` (sha256 prefix `4d300124a6bf116f`, 148 lines).
- `block-expected.txt` — § 2's 99 expected output lines extracted from `9313492990`.
- `block.out` — 99-line output at P1 (`2174265e9c`, via `/workspace/tmp/m6-coordinator/t11-research/tree`); identical to `block-expected.txt` (`diff` empty).
- `block-tip.out` — 99-line output at the tip (`f03b64419f`); identical to `block.out` (`diff` empty).
- `paths.txt` — the 107 sorted paths of `patches-shipped-kernel`.
- `patches.txt` — the 106 `.patch` paths.
- `confs.txt` — the 1 `kernel-config` path (`projects/Qualcomm/devices/SM8550/linux/linux.aarch64.conf`).
- `lines-grep.tsv` — per-file line counts by `/usr/bin/grep -c ''` (total `40474`).
- `lines-wc.tsv` — per-file line counts by `wc -l` (total `40473`; `0004-drm-msm-a6xx-Enable-IFPC-on-Adreno-740.patch` is `32` vs `33`, no trailing newline).
- `headers.tsv` — per-patch header census (`From:`, `Subject:`, `Date:`, `Signed-off-by:`, `Link:`/`Upstream-Status:`, diffstat `---`) across the 106 `.patch` files (`87` with `From:`, `89` with `Subject:`, `4` with `Link:`/`Upstream-Status:`).
- `vs-mergebase.tsv` — per-file byte comparison against `c445081a59` (`106 SAME`, `1 ABSENT`: `0950` ramoops).
- `vs-upstream-next.tsv` — per-file byte comparison against `651150fc88` (`101 SAME`, `4 CHANGED`, `2 ABSENT`).
- `order-GENERIC_X64.txt`, `order-H700.txt`, `order-SM8550.txt` — exact `scripts/unpack` patch-application orders (`8`, `42`, and `65` patches).
- `sm8550-vs-h700-conf.diff`, `sm8550-vs-defconfig.diff`, `sm8550-vs-upstream-next.diff`, `linux-pkg-forced-configs.txt` — the four `SM8550/linux/linux.aarch64.conf` diff and forced-symbol outputs (`2609`, `3827`, `7/7`, and `17` symbols).
- `lint-proof/` — Local depth `tools/lint-audit-artifacts` proof on T4's finished Local folder (`lint-pass.out` `rc=0`, `lint-fail.out` `rc=1` when `tier_exception` is removed).
- `run/driver.sh`, `run/run-stage-a-extra.sh`, `run/stage-a.out`, `run/stage-a-extra.out` — Stage-A runner scripts and combined non-trace outputs (the full `set -x` trace remains in `/workspace/tmp/m6-t41/run/stage-a.trace`).

> **Note on `.githooks/secret-patterns`:** H700 patch #32 (`0158-mmc-sunxi-mmc-mask\u002ddata0-when-updating-the-clock-on-h616-emmc.patch`) has a filename substring starting at the last two letters of `mask` that matches the unanchored `sk-[A-Za-z0-9_-]{24,}` regex in `.githooks/secret-patterns` (the same reason `docs/reviews/inventory.json` records it in `escaped_rows` with `\u002d`, `tools/renovation-inventory:633-642`). In the 11 committed files under `stage-a/` that list this path, the hyphen immediately after `mask` is escaped as `\u002d`; the unescaped copies remain in `/workspace/tmp/m6-t41/` and gitignored `.qa-scratch/t41/` for byte-exact script comparisons.
