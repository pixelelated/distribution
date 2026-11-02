# M6 workspace recovery, 2026-11-02T16:43:25Z

Refs #346, #686, #688, #689. The coordinator resumed all six existing Herdr tabs in workspace `wN` under Codex / GPT-6-Astra / xhigh (observed in its own live footer; no provider attestation). The actual new session identities and next actions are in the [current handoff](../../../.github/sessions/saved-session-state-feature-m6-renovation-plan-346.md).

The retained Python script reads immutable Git blobs in the two existing worktrees and records their membership and stage artifacts. It does not execute the historical tests. Its output is `stage-records.json`; the source is the exact successful reader, with its original `/tmp/m6-resume-20261102` output location retained. It is a recovery receipt, not the full T39/T41 acceptance runner. The first reader attempt rejected headings carrying parenthetical detail; the reader was corrected to accept those existing headings before its successful run. No lane evidence was changed to satisfy the reader.

- T39 Stage C accepted at `c61bcdcb5f2de47dfa35ac25776965e77f962914`: [issue comment 6582545265](https://github.com/pixelelated/distribution/issues/686#issuecomment-6582545265).
- T41 Stage-A evidence accepted at `cffe3f869c5ced124e26befa36505350b4964f77`, with records corrected before Stage B: [issue comment 6582546759](https://github.com/pixelelated/distribution/issues/688#issuecomment-6582546759). The lane's checkpoint summaries had stale groups, filenames and pins; the retained membership output and original source bytes agree. Criteria 3/9 were updated and read back for the actual primary identity and escaped-path comparison.
- [Resume request and ownership](https://github.com/pixelelated/distribution/issues/346#issuecomment-6582593029); [T42 read-only preparation](https://github.com/pixelelated/distribution/issues/689#issuecomment-6582593675).

All five worker sessions acknowledged recovery. A subsequent live Herdr read observed P1, T1, T2 and T3 working, and T5 ready after acknowledgement. No new runtime slot was allocated. In the host namespace, PID 1230737 was verified as the existing `compile-ack.sh`, PID 1230738 as its ledger tail, both start ticks 42356911. The last ledger RETURN observed was 2026-11-02T01:22:14.426038Z. That monitor acknowledges ledger lines; it is not an off-session result-delivery service.

The recorded source checks run on the host because they read committed files and historical receipts. No device, cloud, VM or compiler action occurred in this recovery. The source/behaviour distinction and Local depth remain unchanged.

## Follow-up and retained T42 planning inputs

The records-only T41 correction at `02aab33bd9842610b0d466c9c186454dc14373ee` changes six record files; all 34 original Stage-A receipts and all product paths remain unchanged. Stage B then started under the existing acceptance. See `follow-up-readbacks.json`.

P1's [membership report](t42-membership/report.md) and T2's [inherited-lead report](t42-inherited/report.txt) are completed bounded research, not new audit verdicts or an execution brief. Both reproductions were inspected and run by the coordinator using immutable Git objects. P1's main output matches all but its separately appended `LINE_SEMANTICS` row; the coordinator's [supplement reproducer](t42-membership/verify-supplement.py) derives that row from the four referents and verifies the combined output byte-for-byte. T2's generated tables and counts match byte-for-byte. `t42-research-manifest.json` gives the original research artifact hashes. The reports retain their original scratch locations and author identities as provenance; the copies here survive scratch loss. These scripts require the named immutable commits to be present locally. The inherited-lead script writes beside itself: copy it to a small scratch directory before reproducing it. Neither script invokes the inventory generator, sources configuration, extracts archives, runs a build or starts a guest.

Native T42 membership is **384 paths / 71,387 logical Git-blob lines**, separate from **50 inherited questions / 26 override recipes**. The former includes 380 regular patch files, four symlinks and 12 fork-written paths. A T42 MangoHud symlink reaches a T43-owned referent; that is context, not shared edit ownership. The inherited H700 SWIG question remains T42, adjacent to T41's four applied U-Boot patches and T27's recipe ownership. Current milestone text was updated with these populations and read back byte-for-byte.

## T39 Stage-D handoff accepted

Stage D at `96ef183aae39da587e5dc51d19d7c1fc9e850704` is accepted in [#686 comment 6583071671](https://github.com/pixelelated/distribution/issues/686#issuecomment-6583071671), retained in `t39-stage-d-acceptance.md`. The live seven issue bodies match the committed hashes; #1406 is a child of #686 with 46 open items, and each of #1400–#1405 has one open criterion. The readback is `t39-stage-d-readback.json`. The 14 retained validation receipts are green; this is a record review, with no A–C behavior checks replayed. Primary model/lab are unchanged and prior harness/identity text remains as a prefix to the appended Codex observation.

T1 is paused for the coordinator's stream brief. The menu-map journal and low-inbound-document preferences have been routed to the owner. No restructure or retirement is inferred from a missing answer. T41 remains active in Stage B; the two T42 research lanes and T5 are available.

Coordinator publication checks: `git diff --check`, `tools/rules-check` (30 rules), `tools/register-check` (717 IDs), `tools/work-log-index --check`, and the network-capable `tools/ceremony-check --gate` all returned 0. No package or product code changed in this recovery packet.

The original `t42-inherited/leads.tsv` uses Python CSV writer CRLF endings.
The adjacent `.gitattributes` preserves those exact bytes and recognizes its
carriage returns as line endings. The staged whitespace check then includes
all new evidence files; the original research hash remains unchanged.
