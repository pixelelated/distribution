# T39 final hand-back — bounded acceptance support

2026-11-02 UTC. Codex / OpenAI, session `01a19d11-dda5-72e3-86f9-416f36341c24`, `m6-p1-survey` wN:p3; return only to `m6-coordinator` wN:p2. This is artifact reconciliation, not a slice acceptance or new audit.

Read complete live #686 body/checkpoint 6586260088, #1406, six bug bodies and their named correction comments; proved stream brief v2 at `7f25f9f78b3da3a6b2c893397b58a3ce5a04be75`; final artifacts at `4eb5dfab8e745914a55e7de3e5a43c5b91ebc608` (T). Reviewed baseline B=`86ebb6dffce7bec2dda6296bd84dd225a28b1347`; authorized coordinator K=`329011b9eae20922b4d0727e13bf1626b2e1c04f`; merge M=`24a5e0e294607bc6fc99025873cb063d26c9a4da` has exactly parents `ad5516f6603509954d241e62585b22d32402b03c` and K.

**Three literal-predicate discrepancies remain for coordinator disposition. No source-scope discrepancy or missing final-tip receipt was found within the bounded reconciliation.**

1. **Criterion 5 does not pass as written.** Its unfiltered B..T history contains 46 non-merge commits: 16 lane commits and 30 reachable from K. Its exact protected-path removal command is nonempty: six coordinator brief files, **3,056 insertions** (`doctrine-reference.md`, `doctrine-skills.md`, `patches-shipped-kernel.md`, `patches-shipped.md`, `t38-streams.md`, `t39-streams.md`, all under `docs/reviews/briefs/`). Removed register lines are zero. The scoped evidence below does not make the original predicate true.
2. **Criterion 12 has the same ancestry problem.** Its literal ledger-history command returns **10 coordinator commits**, starting with `329011b9ea`, `07d01c898f`, `7f25f9f78b`. Excluding K's reachable history gives zero. Criterion 13's unfiltered read-only history is already empty. The coordinator has acknowledged 5/12 and owns any prospective reconciliation; no replacement wording is selected here.
3. **Criterion 24's quoted count also needs reconciliation.** Committed `stage-h/host-census.json` records baseline 712/current 1061 lines and two post-baseline T39 mentions at lines **802 and 1003**, both classified as coordinator-authored, while reporting zero T39-authored lines. That supports a different claim from the criterion's unqualified `grep -c -E 'T39|#686'` expectation of zero matches. This observation uses the retained census only: no host-file read, host action or allegation of a T39 write.

## What the artifacts establish

- Exactly **48** of the 254 source paths changed, all in the manifest; before/after SHA256 values match immutable blobs. Those 48 modes/blobs are identical at final source `de11515859...`, M and T. S1–S5 change 3/4/5/12/29 source rows respectively, with overlap. Each of the five recorded candidate tree IDs equals its committed tree ID. All 719 K-to-T changed paths are confined to these source paths and the allowed audit/pointer/retro/work-log records. Protected paths equal K. Both complete log append sequences and their recorded merge hashes reconcile and survive in T.
- **31 binaries + 18 art files** retain their baseline mode/blob identities. All **124 A–D receipt files** remain unchanged. The sole review-plan change appends E–H identity context; historical primary.model/lab, Local depth and empty reviewers remain intact. No completion marker is present.
- All **46** outcomes agree between `stage-f/outcomes.json`, 05's gate and live #1406: **15 Resolved / 22 Deferred / 9 Withdrawn**, with 24 checked and 22 unchecked audit items. The six bugs remain open; their correction comments name the appropriate immutable S1/S2 commit and final tip. Q5 retains **33 files / 2,770 lines**: 29 notices, three reused S2 statuses, one unchanged plan. The final records have **28 matching proof pairs** in the five allowed classes. D223/D224 and #1407 ownership remain explicit.
- Inspected the provenance implementation as text: `tools/t39-checks.sh:56–60` recognizes only K and requires K ancestry; `tools/t39-checks.py:317–345` excludes K history, independently compares every non-owned final path to K, and retains append-only register checks. It retains 13 steps and the default mode. The three implementation hashes in `stage-h/checker-changes.json` match T's actual blobs.
- Immutable H controls record wrong-tip/unmerged-tip refusals **rc 2**, post-merge and merge-resolution edits to `docs/reviews/order.md` **rc 1 / 12 of 13**, then genuine M with findings withheld **rc 0 / 13 of 13**. The failure messages identify the introduced path; the merge-resolution control is caught by the independent final-byte comparison. No control was executed here. All **34 exact raw JSON companions** match their embedded hashes and normalized text views.

## Final retained producer receipts, distinct from M's committed packet

Per the coordinator's explicit follow-up, read only allowed ordinary receipt files under `/workspace/tmp/m6-t39/final-4eb5dfab8e74/`: **64 files / 598,697 bytes**. Their complete actual size/SHA256 manifest is `final-receipts.json`; raw files were not copied or regenerated. The coordinator is retaining them.

Both commands name actual T, original `--since 86ebb6dffc`, and exact K. Normal started **19:17:22Z**, withheld **19:17:25Z**; both have **rc 0, 13/13**, including 1,503 ownership assertions and 64 allowlist assertions (59 legitimate, five inherited, zero findings). The final record check reports 28 pairs and rejects all five record controls. Resolution lint, rules/register/index/ceremony/hooks/menu-map, forbidden scan and the eight issue checks record rc 0; final #686/#1406 readback checks also record zero failures. Producer cleanup/clean-state statements are retained claims, not independently repeated operations.

| Retained receipt | Actual SHA256 |
| --- | --- |
| results.json | cb50da659a5bc5c63e521bd4b49cd80d8b64121d1484c23b2a75c14b5b25053a |
| normal/harness.out | 319aebfa109b3971048ea7f8e3d5cf43971c5d7682e4a9f443b4f0a6d97e7a31 |
| withheld-findings/harness.out | 833ab89575663dc7dbd9cddee3f4298ef4ef3e545f0931a0b274c3a87a0b3810 |
| record-check.out | b801ab972ea8b28c8cd411c76f3f7ed4263a0ef30c9477912ad9e9c4682c01f8 |

## Reproducer and commands

`reconcile.py` reads immutable Git objects and saved tracker snapshots, compares metadata/hashes/record fields, and writes only this scratch's results. `read-final-receipts.py` hashes only the explicitly permitted receipt files. Neither executes producer code, project checks, generators, fixtures, exports or source behavior. `commands.json` contains exact Git argument arrays; `results.json`, `additional-facts.json`, `artifact-hashes.json` and `final-receipts.json` contain results and hashes.

Key commands, with B/K/M/T as defined above:

```sh
git show --no-patch --format=%P "$M"
git log --no-merges --format=%H "$B..$T"
git log --no-merges --format=%H "$B..$T" --not "$K"
git diff --stat "$B" "$T" -- docs/reviews docs/releases/catalog.md docs/pr-series/map.txt docs/releases/rc-accept.txt docs/vm-qa-log.md docs/cloud-sync-changelog.md docs/rasteratops/p0-sweep-hits.txt plans licenses documentation LICENSE.md docs/upstream .claude CLAUDE.md AGENTS.md NAMING.md tools scripts packages projects
git log --no-merges --format=%H "$B..$T" -- docs/reviews docs/releases/catalog.md docs/pr-series/map.txt docs/releases/rc-accept.txt docs/vm-qa-log.md docs/cloud-sync-changelog.md docs/rasteratops/p0-sweep-hits.txt plans
git show "$T:docs/audits/2026_11_01-epic-m6-doctrine-reference/stage-h/host-census.json"
python3 /tmp/m6-t39-final-support.cmlvWk/reconcile.py
python3 /tmp/m6-t39-final-support.cmlvWk/read-final-receipts.py
```

Tracker reads used GitHub connector `github_fetch_issue` for 686/1406/1400–1405 and GET `repos/pixelelated/distribution/issues/comments/{6586260088,6586196594,6586197813,6586199573,6586200742,6586202112,6586203346}`. Complete fetched snapshots are retained here.

Historical P1 remains clean at `2174265e9cc1b248c0fbe27fa101875984d46d6b`. No repository/kit/tracker edit, private held read, execution replay, source export, runtime/provider/device/cloud/host action or permission answer. Stop at this return; final acceptance, criterion changes and routing remain wN:p2's.
