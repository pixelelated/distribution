# Mini Retro: M6.P2 T4, the binding doctrine (#651)

**Completed:** 2026-10-24

**Scope of this retro:** the T4 lane, from the dispatch (#651, issuecomment-6385443829, 14:32 UTC) to stage G:
- the audit in `docs/audits/2026_10_24-epic-m6-doctrine-rules/`;
- the eight `bug` issues #904 to #911 and the punch-list issue #912;
- the eight stage-E streams of `docs/reviews/briefs/t4-streams.md` (`ee029004c6`).

Not retro'd here, because they are not this lane's:
- #905's tool packet (the T1 session's, reviewed at `9e12014623`);
- the deferred items' owners (#685, #657, #808, #811, #640, #645);
- the merge.

**Branch:** `feature/m6-doctrine-rules-651`. `reviewed-at: 00e75ab135` (the read on `8ebaf8daad`'s bytes); `fixed-at: b3c1d0d7c3` (S8, the last stream).

**Delta:**
- **Doctrine:** 13 files of the 36 changed by eight stream commits, +139/-107, each limited to the paragraphs its item names:
  - `CLAUDE.md` and `AGENTS.md`;
  - `time-to-play.md` and `least-surprise.md`;
  - `generic-x64-vm-testing.md` and `es-code-traps.md`;
  - `rclone-cloud-sync.md`;
  - `fork-workflow.md` and `device-builds.md`;
  - the build-root lines in four rules (`worktrees.md` and `packaging-and-patches.md` among them);
  - `instruction-files.md`;
  - `ceremonies.md`.

  The registers are untouched but for one friction append.
- **Records:** `00` to `05`; a Local `review-plan.json`; five tools (`t4-q4.py`, `t4-q6.py`, `t4-blocks.py`, `t4-coverage.py`, and `tick-checkboxes.py` copied from T24); 35 proofs.
- **The punch list:** 25 items: 16 Resolved, 8 Deferred, 1 Withdrawn.
- **Bugs:** 8 filed (#904 to #911). Six are fixed here with every criterion ticked; #905's rule half is fixed, with its tool half in the packet; #911 is deferred to T38.
- **Network:** tracker reads and writes only. No guest, no build, no model call.

## What the slice did to the two time-to-play numbers

**The slice did nothing to the two time-to-play numbers.** It changed rule text only. No file a device runs or a build reads changed: `git diff --stat 8ebaf8daad b3c1d0d7c3 -- packages projects` is empty. What changed is that `time-to-play.md` now describes the launch over a running sync the way the shipped code does it (D-CLOUD-130). That changes what a designer reads, not either number.

## What worked well

- **The at-hash read tree** (the futro's A1): every figure the brief named re-derived with no delta, and the branch's own deltas were listed hunk by hunk with their owners before a rule was read.
- **Read-only readers with no context for the unread files.** Four of them read 11 files, about 5,900 lines, in under eight minutes. Their reports found the largest items: the friction check failing open (F-02), the `/var/log` contradiction (F-11) and the stale rclone recipe facts (F-21). Every lead that became a finding was re-read here first. One of their counts was wrong (the open table's cells), which is why the rule calls them leads.
- **Lifting a tool's own regex to count what it skips.** `ceremony-check`'s friction matcher, applied to the log, gave the 125 entries it never reads. It was the tool's code, not a reading of it, and the packet's diff fixes exactly that.
- **Generated tables that assert their rows.** Each of the four scripts refuses a missing row or an empty cell. The stage-F check for PL-19 is one of them (`t4-q6.py pointers`: 31 at the hash, 0 at the tip), so the coordinator re-runs a command rather than reading a table.
- **One stream per file, each with a check that fails before and passes after** (the futro's pre-mortem rule). Eight commits, eight checkpoints, `rules-check` after each. No stream touched a paragraph its item did not name.

## What was harder than expected

- **My own counts went wrong six times before commit**, each caught by recounting from the artifact:
  - a list on cut lines (27 against 2);
  - a guessed "120-entry line" (100);
  - a separator row counted (33 against 32);
  - a rule's reach (7 against 11 areas);
  - an absent-path split (9/4 against 8/5);
  - the superseded count (2 against 3).

  A seventh, *eleven* Q3 findings, reached a commit message (`ef09e6f54e`; there are 13). This is blindspot 75's shape at a small scale, and the scripts are what caught it.
- **Tool slips around the work:**
  - eight bug bodies through unquoted heredocs (friction line 15:09; nothing expanded);
  - an audit-issue body whose title pattern ran across newlines, so #912 first had one checkbox;
  - a `sed` whose `#` delimiter met `#651`;
  - a punch-index regex that expected an indent;
  - a cell rewrite that dropped `docs/reviews/README.md`.

  Each was caught before it stood, but each cost a re-run.
- **Reflowing prose by string replacement** made long lines and stray spaces three times (S1, S2, S4).
- **Where to stop a sentence's claim.** S3's first wording said *ES rotates the log*, a mechanism read from the rule's own text rather than ES's code (another repository). It was softened to what the rule says. A doctrine edit is held to the evidence floor as much as a finding is.

## What we discovered

- **Doctrine tools claim more than they check:**
  - `rules-check` against *kept equal* (F-01; the coordinator withdrew the tool half as a design the files were not given);
  - `ceremony-check` against its friction promise (F-02; fixed by the packet).

  A rule that names its guard has to name what the guard holds.
- **Facts copied into both entry files go stale in both.** Five of S1's seven changes were the same sentence wrong in `CLAUDE.md` and `AGENTS.md` alike: the mirror, `mkimage`, the vocabulary line, the documents and the targets.
- **Superseded rows live on in every-session rules** (F-10), and a reversal row's sweep (`decision-register.md`) was not run for D-CLOUD-130.
- **The index's tool-to-rule direction was unchecked.** 31 of 85 pairs pointed at a rule that never names the tool (F-22). The other direction was checked and clean.
- **Every stale fact on the other briefs' lists was real.** The lists were findings already paid for.

## Adjustments (proposals for the coordinator, each with its ladder rung; none applied here)

1. **The index's tool-to-rule direction to `rules-check`** (routed to audited): `t4-q6.py pointers` is the check, ready to be lifted into the tool's `tools` line, and seen to fail on the hash (31).
2. **A superseded-citation check** (written to audited): `t4-q4.py`'s narrowed review found 3 of 45 citations stale. A tool that flags a rule citing an ID a later row reverses would hold F-10's class. It is #657's (T10) to weigh beside the register checks.
3. **A brief's stream block names its own probe precisely.** S4's first probe matched the line before the corrected one; a probe written as the exact old phrase avoids that. This is a line for the stream-brief template.
4. **Prose rewrites by tool, not by string replacement**, for a rule edit: the Edit tool, or a reflow that is checked (`awk 'length > 100'` over the added lines) before the commit. It was needed three times here.
5. **An executor's own artifact tables are scripts**, as T4's are. The stranger's proof checks a brief's counts; only a regenerating script checks an executor's. This is for the slice-brief template.

## Scoped audit (Step 2.5)

- **AC conformance:** PASS. #651's sixteen criteria have their artifacts, except the merge and `renovation-status` clause, which is the coordinator's.
- **Cornerstone spot-check:** PASS.
  - No decided register row edited.
  - No rule edited outside a stream's named paragraphs (each stream's diff read before its commit).
  - No legacy-path line changed (#640).
  - `council-substrate-integrity.md` untouched (T38).
  - Nothing outward.
- **Interaction-defect scan:** PASS. `03` § 3.5's five seams. S8's sentence describes the packet's tool, which merges before this branch.
- **Futro prediction verification:**
  - **The unknowns:** U-1 to U-3 and U-5 are answered, U-6 is moot, and U-4 (the merge) is the coordinator's.
  - **The adjustments:** A1 to A9 were each done.
  - **The pre-mortem:** its sizing rule held (25 items, eight streams, not 140 items).
  - **Missed:** F-02, F-11, F-20, F-22.
- **Housekeeping:** the six checkers are in the hand-back.
- **Harness self-coverage:** PASS. `t4-q6.py pointers` fails at the hash and passes at the tip. `tick-checkboxes.py` refused nothing it should have, and read every body back equal.
- **UI review:** SKIP (no UI surface).
- **Documentation and glossary freshness:** the slice *is* the documentation freshness pass. No new proper noun.
- **Build-vs-adopt:** SKIP.

## Practice adjustments

- This retro reused the four-answer draft written during the stage-D pause (A6), and stage E added only its own lessons. The futro's suggestion to draft during the pause saved the retro's first hour.

## Code-verifiable state

| Artifact | Path | Check |
| --- | --- | --- |
| the coverage table | `02-forward-audit.md` | 36 rows (`t4-coverage.py`) |
| the proofs | `02`, `00` | 35 = 35 |
| the streams | 8 commits, `0faea874de` to `b3c1d0d7c3` | each check fails at the hash and passes at the tip (`02` § Stage F) |
| the index pointers | `tools/t4-q6.py <tree> <list> pointers` | 31 at the hash, 0 at the tip |
| the punch list | `05-punch-list.md`, #912 | 16 / 8 / 1; 25 checkboxes ticked |
| the lint | `tools/lint-audit-artifacts <folder> --issue 912` | `PASS` |

---

**T4 is complete to stage G. Next is the hand-back on #651 (stage H). The coordinator accepts by brief § 10 on the branch at `fixed-at`, with the simulated merge beside it.**
