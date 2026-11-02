# Stage A scripts and outputs — T41 (#688)

Corrected on 2026-11-02 16:44:30 UTC by Codex / GPT-6-Astra / xhigh, session `01a19d12-29e3-7fe0-9f41-038dac0a5deb` (observed live footer, not provider-attested). Acceptance: #688 comment 6582546759. The original command receipts are unchanged.

Stage-A execution was `2026-11-02T05:27:50Z–05:30:28Z` under Claude Opus 5.5 (High), at seed `f03b64419fa656fb3af61cbc8d174284020d439c`. Gemini 4 Argon (High) wrote/stashed the records from 15:08 UTC. The accepted artifact is `cffe3f869c5ced124e26befa36505350b4964f77`.

## Committed layout

`git ls-tree -r --name-only cffe3f869c -- docs/audits/2026_11_02-epic-m6-patches-shipped-kernel` contains 37 files: `00-running-log.md`, `01-research-notes.md`, and these **35** relative to `stage-a/`:

```text
README.md
block-tip.out
block.out
box-check.out
ceremony-check.out
forced.txt
hooks-test.out
index.out
lint-local-fail.out
lint-local-pass.out
order-GENERIC_X64.txt
order-H700.txt
order-SM8550.txt
order.out
p1-qa-scratch/block-1.txt
p1-qa-scratch/block-2.txt
p1-qa-scratch/block-expected.txt
p1-qa-scratch/block.sh
p1-qa-scratch/mb-compare.txt
p1-qa-scratch/membership.py
p1-qa-scratch/paths.txt
p1-qa-scratch/text.txt
p1-qa-scratch/tree-listings.sha256
register-check.out
rules-check.out
run/driver.sh
run/runs.sh
run/stage-a-extra.out
run/stage-a.out
tip-qa-scratch/block-1.txt
tip-qa-scratch/block-2.txt
tip-qa-scratch/block-tip.sh
tip-qa-scratch/mb-compare.txt
tip-qa-scratch/paths.txt
tip-qa-scratch/text.txt
```

`p1-qa-scratch/block.sh` is the marker-extracted v2 membership block (148 lines, SHA256 `4d300124a6bf116f9c0177712e8f0a824b35db45cc5a042acbd4cc58445192a3`). `p1-qa-scratch/block-expected.txt`, `block.out`, and `block-tip.out` are the identical 99-line expected/P1/seed outputs. `p1-qa-scratch/paths.txt` and `tip-qa-scratch/paths.txt` carry 107 paths. The only configuration is `projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf`.

`run/driver.sh`, `run/runs.sh`, `run/stage-a.out`, and `run/stage-a-extra.out` hold the retained scripts and combined command outputs. Census, byte comparisons and configuration counts are in those combined outputs, not separate `headers.tsv`, line-count TSVs, comparison TSVs or `sm8550-*.diff` files. The retained Local proof outputs are `lint-local-pass.out` and `lint-local-fail.out`.

The directory groups in brief order are 7.0:4, 7.2:6, mainline:4, H700 patches:32, SM8550 patches:55, SM8550 config:1, DDR3:2, DDR4:2, firmware:1 (107 total). The three kernel orders contain 8 / 42 / 65 paths.

## Scratch retained outside this packet

`/workspace/tmp/m6-t41/stage-a-p1/` holds the unescaped membership inputs/output, including `tree-ih.txt` and `tree-p1.txt`; only their SHA256s were retained in the packet. `/workspace/tmp/m6-t41/run/` contains `stage-a.trace`, `stage-a.sh`, `brief-v2.md`, `driver.sh`, `runs.sh`, and `stage-a-extra.out`. `/workspace/tmp/m6-t41/tmp/` holds the block/checker outputs, `brief.md`, `order.out`, and `forced.txt`; the Local fixture is in `lint-proof/`. The three order files and the extracted `src/linux-7.2/arch/arm64/configs/defconfig` also remain outside git.

The gitignored `.qa-scratch/t41/` contains block scripts/outputs, membership.py, paths.txt, text.txt, mb-compare.txt, and the two full tree listings. The old README named nonexistent per-check files; they are not evidence and are not reclassified as scratch.

The H700 0158 filename uses the literal `\u002d` escape in committed text, as inventory and acceptance criterion 9 require. Decode it only for comparisons or actual source access. Keep the patch filename and secret scanner unchanged.
