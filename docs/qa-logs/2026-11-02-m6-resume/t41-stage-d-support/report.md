# T41 Stage-D bounded reconciliation

2026-11-02 UTC. Reader: Codex / OpenAI, actual harness session `01a19d11-dda5-72e3-86f9-416f36341c24`, lane `m6-p1-survey`, `wN:p3`. Return to `m6-coordinator`, `wN:p2`. This is record reconciliation under the existing #346 continuation, not acceptance, an audit replay, or a routing decision.

**PASS for the Stage-D packet/filing reconciliation; one stale milestone statement.** No concrete discrepancy found between the immutable D packet, complete checkpoint 6585618201, live #688/#1408/#1409 and the current brief's D obligations. The milestone's current-state paragraph still says B acceptance is next and C has not started. That paragraph is dated 17:58; the checkpoint is 18:56. Suggested factual correction, for the coordinator only: B accepted at `7e5d154671`, AC17 correction `721d6e7049`, C published at `94b5b1c0b9`, D returned at `c9fe606e8d`, awaiting coordinator disposition. This is not a claim that D has been accepted.

Packet: `c9fe606e8d7e7e0f6c70cc686764d1503029d278` (parent `94b5b1c0b983313325dba101217761c6e5c9bca0`, committed 18:54:45Z). Audit root: `docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/`. Current brief read at pinned coordinator `07d01c898fba867e042342017fd8d5257508a28c`, `docs/reviews/briefs/patches-shipped-kernel.md`, blob `a5191945cddb5d2fc282a0d89eeaeac569b4ab4b`. Its only difference from the packet's brief is the appended D222 Stage-B method erratum; D obligations at lines 1169–1184 and 1517–1520 are unchanged. Live #688's actual-reader criterion governs the historical brief's reader label.

The unpublished D-WORKFLOW-226 draft was not available at that immutable coordinator commit. Its immutable/private-scratch location was requested; it has not been used as authority or inferred to expand this assignment.

## Filing and record facts

- Read 06, 07 and 05 in full, the complete checkpoint, live issue bodies, both question comments, parent responses and the current milestone paragraph. Live #1408 and #1409 bodies equal their exact submitted bodies and retained final readbacks, byte for byte. Both question bodies also equal their submissions and retained readbacks.
- #1409 is open, labels `audit`/`punch-list`, milestone 6 `M6: Codebase renovation`, parent #688. It has one unchecked High PL-001, no checked item. #1408 is open, only `bug`, no milestone; its parent endpoint returns HTTP 404 `No parent issue found`. It has two unchecked criteria. Live #688 retains all 28 unchecked criteria.
- 05 has one PL-001 with question, severity/category, two exact source locations, evidence/refutation, integration owner #563/#559, acceptance, enforcement ladder, Already written, VM rationale, and matching Open gate/YAML index. Filing is neither resolution nor deferral. F-02 through F-05 have explicit dispositions; no new finding is invented from a dry-run disagreement.
- 07 quotes the two posted questions: 6585346506 (three duplicate pairs; T11 owns any later recipe-tree change), 6585347732 (ramoops under settled D-SYS-004; coordinator queue disposition, no implicit policy reversal or submission). The source/integration/T11 boundaries and the D stop remain explicit. No E dispatch or another owner's change is hidden in the packet.
- All 28 scorecard rows match exactly across 02, 04 and live #1409: 20 PASS, 8 PARTIAL (AC 2, 4, 5, 24–28). Twelve `proved:` cells match twelve running-log proof entries; leads L-01–L-31 and rulings a–p each occur once in their tables. Accepted provenance/coverage tables and hygiene output are quoted exactly. The formal Local plan retains the actual T3 Codex identity, empty reviewers and historical identities.
- Parent-response note accurately distinguishes the successful one-time POST from the later local assertion failures. Read-only parent responses agree with the final relationships. Missing original POST timing is explicitly unrecorded, not fabricated or treated as a failed relationship mutation.

## Preservation and recorded checks

The D commit changes 46 paths: its 37 new stage-d files plus nine permitted audit/pointer/work-log paths. No path is outside that scope. All 775 pre-D files in stage-a, stage-b, stage-c, tools and second-opinions have identical mode/type/blob at C and D, with no additions to those protected directories. All 329 original blocker-generation files at `3cd9ca140a0da9af447a3ee2fb9cdbbbf222a95b` remain identical too. The 107 canonical source paths are unique, all mode 100644, and have identical blobs at P1 `2174265e9c`, accepted source `02aab33bd9`, C and D. The whole protected-source diff from dispatch `d7dd76665983cb87dba62397691500fcf409fafe` is empty; rules/register/briefs also have no C-to-D delta. These comparisons establish preservation of accepted evidence; they do not rerun its 120 applications or other behavioral claims.

Inspected `stage-d/verify-records.py` as text only. Its SHA matches validation.json; all ten named output SHA256 values also match immutable bytes. Retained validation interval: 18:53:26.653095–18:53:40.680589Z. Audit API, audit box-check, pre-issue lint, rules, register, work-log index, ceremony, whitespace and forbidden check record rc 0; secret grep records expected rc 1 and `0` matching lines. Audit box-check says 1 open / 0 fail; bug box-check says 2 open / 0 fail. Lint explicitly says it does not certify resolution. Initial box-checks and API calls retain actual argv/start/duration/return code. The final receipt append is dated 18:54:45, after validation; this report makes no claim of a later rerun. The checkpoint's push/hooks/clean-other-worktree claims are producer statements, not independently re-executed here.

Key immutable artifact SHA256 values:

| Artifact relative to audit root | SHA256 |
| --- | --- |
| 05-punch-list.md | fd9cb76231e374edb6a76e11e0057c7e142caf5e3b3cc3f8983785be2aba111f |
| 06-audit-summary.md | da69d85a840e68270bb577cf811fa377467c6b4b320a4d0536766d5950d273f1 |
| 07-questions-for-the-maintainer.md | 729d297141fb004349860084ffa8e7de27763436e511602879ee2e30cab34e71 |
| stage-d/validation.json | 6ac3d135c8ce65ae7841e8bf3876b193ce92439e89991f636850e6b8d80e8088 |
| stage-d/verify-records.py | 9cb1dce6c3cdc8ce76b93bb7a81863a2c1f89850686da07a9586b9ce1510b33b |

## Evidence commands and retained return

All Git commands ran from the historical P1 launch worktree against explicit immutable refs. Representative exact commands (full argument arrays are in commands.json):

```sh
git show c9fe606e8d7e7e0f6c70cc686764d1503029d278:docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/06-audit-summary.md
git show c9fe606e8d7e7e0f6c70cc686764d1503029d278:docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/07-questions-for-the-maintainer.md
git show c9fe606e8d7e7e0f6c70cc686764d1503029d278:docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/05-punch-list.md
git show c9fe606e8d7e7e0f6c70cc686764d1503029d278:docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/stage-d/verify-records.py
git diff --name-only d7dd76665983cb87dba62397691500fcf409fafe c9fe606e8d7e7e0f6c70cc686764d1503029d278 -- '*.patch' '*.conf' packages projects tools scripts
git diff --name-only 94b5b1c0b983313325dba101217761c6e5c9bca0 c9fe606e8d7e7e0f6c70cc686764d1503029d278 -- docs/decision-register.md AGENTS.md CLAUDE.md .claude docs/reviews
git diff c9fe606e8d7e7e0f6c70cc686764d1503029d278 07d01c898fba867e042342017fd8d5257508a28c -- docs/reviews/briefs/patches-shipped-kernel.md
python3 /tmp/m6-t41-stage-d-readback.MVMFlk/reconcile.py
```

`reconcile.py` is a small independent byte/metadata comparator. It invokes only immutable `git show`, `git ls-tree`, `git diff --name-only`/brief diff and pinned `git rev-parse`; it reads saved tracker JSON and writes this private scratch's results, hashes and command list. It does not invoke the producer verifier, any generator, test, application, project guard, config, archive or source helper. It keeps source/tree objects in memory; no source-tree export is created.

Read-only GitHub connector calls: `github_fetch_issue` for 1408 and 1409 (`repository_full_name=pixelelated/distribution`); `github_fetch` GET endpoints under `https://api.github.com/repos/pixelelated/distribution/`: `issues/1409/parent` (complete #688 payload and its embedded milestone), `issues/1408/parent`, and `issues/comments/6585618201`, `issues/comments/6585346506`, `issues/comments/6585347732`. Link identity: `link_6ac2961edf2081918a8d75b020eff02b`. A direct `milestones/6` fetch was rejected as an unsupported connector endpoint; the full current milestone object was already supplied by the live #688 parent response. No tracker mutation occurred.

Small retained packet: report.md, reconcile.py, results.json, artifact-hashes.json (all 37 D files plus 05/06/07), commands.json, and the named live tracker snapshots. Full body hashes and all ten receipt-output hashes are in results.json. Historical P1 HEAD remains `2174265e9cc1b248c0fbe27fa101875984d46d6b`, worktree clean. No repository/kit/tracker edit, generator/test replay, extraction, fetch, runtime allocation, provider call, host/device/cloud action or permission answer. Acceptance/routing remains wN:p2; stop at this bounded return.
