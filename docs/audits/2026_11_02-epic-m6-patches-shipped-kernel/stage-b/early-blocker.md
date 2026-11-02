# Stage-B early blocker: dry-run and actual application disagree

Observed 2026-11-02 16:54:50 UTC; Codex / GPT-6-Astra / xhigh, session `01a19d12-29e3-7fe0-9f41-038dac0a5deb` (live Herdr footer, not provider-attested). Source/ref: `02aab33bd9842610b0d466c9c186454dc14373ee`. Stage B is **incomplete**; this is an early-blocker packet, not a Stage-B checkpoint or product-bug claim.

## The conflicting commands

H700 order 011 is `projects/ROCKNIX/devices/H700/patches/linux/0002-rg35xx-enable-HDMI-LCD.patch`. In isolated touched-file scratch, after the same ten predecessor patches:

- `patch -p1 -N --batch --directory /workspace/tmp/m6-t41/src/refute-H700-same-input --dry-run` returned **1**. `logs/same-input-H700-011.dry.out` reports `Hunk #1 FAILED at 1154.` followed by `1 out of 1 hunk FAILED`.
- The identical command without `--dry-run`, on the **same unchanged input tree and identical patch bytes**, returned **0**. `logs/same-input-H700-011.apply.out` reports that hunk succeeding at **1246 (offset 92 lines)**.
- Tree SHA256 before and after the dry-run and before the actual apply: `2c8679d35a8d5a9ec5e55b72c87869104581c76fd2a2a650ad7105589420abc1`. Patch SHA256: `3c368ef17a3632532da37c8a126fb82cdd6b21b83333abf2094914cce37a83db`. All three equalities are asserted by `refute-dry-run.py`; `same-input-refutation.json` retains commands, timestamps, elapsed time, rc and both tree hashes.

The patch is a concatenated series. `sun50i-h616.dtsi` is modified at patch lines **1081, 2051, 2101**; the failing dry-run hunk is at **2105** and needs the `tcon_lcd0_out` context introduced by earlier diffs in the same input. A real scratch application preserves those earlier edits; the dry-run fails on this dependent later diff. This refutes treating the initial rc=1 as proof the complete patch cannot apply.

## Why the v2 sequence cannot yet be certified

Brief § 5 (1410 onward) says to dry-run each patch, apply only after rc=0, and use the dry-run rc for the applies-at-pin cell. Its supplied loop therefore skips all of H700 011 after this false failure. Later H700 results no longer see the source that a successful real application would produce. Six initial H700 `fails` are retained as **method-contaminated leads**, not six established product bugs. The initial nonzero dry-runs are H700 **011, 013, 015, 018, 035, 036**; none has been filed as a bug.

Brief § 10 explicitly names **“two commands that disagree”** as a blocker; a lone failed dry-run is expressly not a stop. This packet demonstrates the former, using identical inputs. The user requested a Stage-B checkpoint **or early blocker**, and the coordinator owns this method ruling. No additional Stage-A acceptance is requested.

**Ruling requested on #688:** may Stage B retain the literal v2 dry-run results but use a complete normal application in a fresh disposable touched-file copy as the authoritative applicability check, advancing the ordered scratch only when that complete application succeeds? This would resolve concatenated-series semantics while preserving every failure receipt and the source-only boundary. An alternative is to specify a corrected sequence-aware dry-run method. No method change has been substituted silently.

## Work completed and retained

The initial runner was observed running at 16:49:05 UTC and exited rc=1 after its firmware empty-root assertion. This observation is separate from the per-command producer receipts. The five preceding plan loops completed; `applies-*.txt` and `logs/` retain their own output. The runner's final `application-results.json` was never written and is not claimed.

| Plan | Rows | applies | applies with offset | fuzz | fails | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| GENERIC_X64 | 8 | 2 | 4 | 2 | 0 | Literal initial dry-run results |
| H700 | 42 | 14 | 12 | 10 | 6 | Incomplete sequence after false failure 011; not acceptance evidence |
| SM8550 | 65 | 18 | 30 | 17 | 0 | Literal initial dry-run results |
| UBOOT-DDR3 | 2 | 2 | 0 | 0 | 0 | Dry-run and actual scratch apply both rc=0 |
| UBOOT-DDR4 | 2 | 2 | 0 | 0 | 0 | Dry-run and actual scratch apply both rc=0 |
| FIRMWARE | 1 | 1 | 0 | 0 | 0 | Completed separately after empty-root correction; both rc=0 |

All five distinct cached archives match their `.sha256` sidecars and recipe text (`archive-sha256.json`, reverified after the initial runner exited). Six `tar-*.json` receipts retain rc=2 and missing-member counts **2 / 7 / 30 / 1 / 1 / 2** in table order. Missing targets created by patches are expected. Firmware's patch creates both target files from `/dev/null`; tar extracted no members and therefore no root directory. The initial runner asserted the root existed and exited. Creating just the empty scratch root resolved this runner assumption; `firmware-refutation.json` and its two logs show dry-run/apply rc=0. This is not a source or cache defect and does not need a separate permission relay.

The input source archives and all 107 repository paths remain unchanged. Only touched files were extracted under `/workspace/tmp/m6-t41/src/`. Scratch remains for Stage H retirement; no live job remains. No compiler, guest, fetch, provider, device/cloud action, host-ledger line, root-tool edit, product edit, or historical launch-tree edit occurred.

## Next owner and action

`m6-coordinator` in `wN:p2`: resolve the v2 method disagreement. T3 then resumes the cached-source sequence using the specified method and completes 02/03/04 plus the full Stage-B packet. `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md` are intentionally **not presented as complete** in this early-blocker packet. The Stage-C generator/identity plan and later issue/punch-list stages have not started.
