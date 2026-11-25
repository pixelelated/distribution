# #1451 criterion 2: the shared worktree's rule text against `next`

Reviewed 2026-11-25 by the OS coordinator. The shared `conflict-resolution` worktree is uncommitted. Its `AGENTS.md`, rules, skills and register were compared with `next` at `cc89bb4453`. `unique.py` (here) lists every line the worktree carries that `next` does not, whitespace-normalised.

- **Before integration:** 302 worktree-only lines in 21 files.
- **After integration:** 163 lines remain. They are in `residual.txt`, compared against the integrated tree.

Each remaining run is listed below with its reason. Where a later commit replaced the text, the commit is named.

## Integrated onto `next` in this change

| Worktree text | Where on `next` now | Edited for |
| --- | --- | --- |
| `engineering-practices.md` § Parallel work must close the progress loop (D-WORKFLOW-183, 189, 195) | same heading, after § Max speaks in one place | "Human updates follow D-WORKFLOW-194" now reads "go to the steward's inbox (D-WORKFLOW-194, D-WORKFLOW-205)" |
| § Approval is for a decision, readiness is the coordinator's work (D-WORKFLOW-184) | same heading | unchanged |
| § Understandable decisions and effective escalation (D-WORKFLOW-190) | same heading, moved up beside the other coordination sections, so `residual.txt` still lists it at its old position | a stopped outcome is reported "as a `STOPPED WORK` file in the steward's inbox (D-WORKFLOW-205)" |
| § Stopped work must reach the maintainer (D-WORKFLOW-187) | rewritten as § Stopped work reaches the steward's inbox unasked | the one-on-one-lane delivery and the "pinned human-lane identity" are replaced by the inbox file and its issue. The content fields, the "quiet is not stopped" line and the ACK separation are kept |
| `ceremonies.md` § Execution discipline: the focused mini-retro and futro paragraphs (D-WORKFLOW-184) | before the existing serial-stages paragraph | unchanged |
| `milestone-phase-naming.md`: current cross-milestone priorities (D-WORKFLOW-185) | first bullet of § Sources of truth | unchanged |
| `learning-capture.md` § Close the learning loop, including the process itself (#1434) | before § Notes | unchanged |
| `futro` and `mini-retro` skills: the continuation sentences (D-WORKFLOW-184), and mini-retro's recurring-coordination-stall paragraph | same places | unchanged |
| `AGENTS.md`: Before scheduling work (D-WORKFLOW-185), and the first binding bullet, "The coordinator closes each progress loop" (D-WORKFLOW-183/184) | after Communication lanes; first bullet of the binding rules | unchanged. `AGENTS.md` is 30,463 bytes, under the 32,768 budget |
| Register rows D-WORKFLOW-191, 192, 193, 195 and D-LAUNCH-008 | appended after D-WORKFLOW-205 | refs note added: integrated 2026-11-25; the cited files are untracked in the worktree. D-LAUNCH-008 names its implementation, `ee74f157ef`, which `0a3e979e50` carries |

The evidence the four D-WORKFLOW rows cite stays untracked in the worktree and is not on `next`:
- `docs/qa-logs/2026-11-17-proactive-continuation/` (93 MB, 1,444 files, including pane and session records);
- `docs/qa-logs/2026-11-17-retention-continuation-retro/`;
- `docs/retros/2026-11-17-retention-continuation.md`.

Their size and their transcripts of Max's words make each a separate decision. That decision is not taken here.

## Intentional differences that remain

| File and worktree text | Why `next` differs |
| --- | --- |
| `engineering-practices.md` § Separate direct conversation from worker traffic (D-WORKFLOW-186), the D-WORKFLOW-194 pane paragraph, and § Stopped work must reach the maintainer (D-WORKFLOW-187) as written | Reversed in their transport by D-WORKFLOW-201 and D-WORKFLOW-205 (`3aab3ee850`, `cc89bb4453` and the change before it). Nothing goes into the one-on-one pane. What still holds is on `next` in § Max speaks in one place, § Stopped work reaches the steward's inbox unasked, `docs/coordination-continuity.md` (ACKs out of the human conversation), and the November 18 clarification at the top of the file |
| `engineering-practices.md`, line 382 (`watch-build-submit` wording) | reworded on `next` by `d7e2d6be41` (#493) |
| `AGENTS.md`: Communication lanes and Lane models as written | superseded by D-WORKFLOW-201/205 and D-WORKFLOW-200 (`AGENTS.md` on `next`) |
| `AGENTS.md`: the authority, watch-build and rclone lines | reworded on `next` by `db1c00df3d` (#1437), `d7e2d6be41` (#493) and `bc2dceb406` |
| `device-builds.md`: worktree command, warm cache, credentials, publishing, time budget | reworded or replaced on `next` by `6ee8c7610e`, `f10eec1306`, `60a5d7f9c7`, `4f6e0a4c95` and `f3d6ef6501` |
| `rclone-cloud-sync.md`: single remote, asserted remote name | replaced on `next` by `bc2dceb406` (saved connections bound to account state) |
| `release-candidates.md`: preflight acceptance line, step 2, step 4 | `f7f7755e8b` (D-WORKFLOW-202), D-INFRA-043's whole-set step 2, and step 4 now citing D-WORKFLOW-198 |
| `worktrees.md`: two cleanup sentences | replaced by `67faae8bb5` (#493, build-cleanup) |
| `build-cleanup/SKILL.md`: refusal line, warm base | `3aab3ee850` (#1447), then D-WORKFLOW-205 (the refusal goes to the inbox) and `0fa33fbd57` |
| `instruction-files.md`: five table rows | `next`'s newer rows: escalation (this change), `vm-upgrade-rehearsal`, `fork-publish-release`, the VM tools and `rc-preflight` (D-INFRA-043) |
| `fork-workflow.md`, `generic-x64-vm-testing.md`, `packaging-and-patches.md`, `ceremonies.md`: one line each | the tool list grew on `next` (#1451's tools); image names by `f10eec1306`; the ceremonies row's wording on `next` |
| `docs/decision-register.md`: 13 runs | the five rows above sit at a different place on `next`, and `next` carries 48 rows the worktree lacks |

The worktree's council, code-auditor and agent files that `git status` lists as modified have no worktree-only lines against `next`. `next` already carries them.

## Not reviewed here

- `docs/coordinator-one-on-one.md` is held by the steward (#1451 criterion 3).
- `scripts/`, `council-seat-efforts.json`, `verifier-pins.json`, the package recipes and `tools/` files the worktree also modifies are product or council code, not rule text, and are outside this criterion.
