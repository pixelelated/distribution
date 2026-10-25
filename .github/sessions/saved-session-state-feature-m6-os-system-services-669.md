# Session pointer: M6.P2 T22, the OS's system services and platform quirks (#669)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-os-system-services-669`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tips merged in (`cc8b6cf2a3` at `311c1f7972` (two merges, `3d56c56380` then `311c1f7972`, carrying versions 1 to 3)); the pointer seeded after the second merge
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-os-system-services-669`; the T5, T6, T7, T8, T9, T12, T45, T23 and T40 worktrees beside it (`m6-packages-dead-ends-670` read with `git show`, never checked out) (`m6-build-engine-652`, `m6-build-engine-upstream-tools-653`, `m6-generic-packages-reached-654`, `m6-image-packages-655`, `m6-tooling-build-supervision-656`, `m6-tooling-vm-harness-659`, `m6-tooling-council-692`, `m6-packages-dead-ends-670`), idle until their merges; nothing is written there
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T1 session, `m6-t1-os-launch`, after T13's close-out), unless #669 says otherwise
> **Epic:** #695 (the OS scripts: T1 done, this slice, then T29); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Extended -- **two seats, GPT-6 Astra at `max` and Gemini 4 Argon at `high`**, each a probe then one refutation over a trimmed packet (D-WORKFLOW-195), as T1's audit ran them; `review-plan.json` records depth `extended` and both reviewers; a seat that cannot run is a named blocker at Phase 4.6, never a substitute; **every other `tools/council/run` call carries `COUNCIL_ENV_FILE=/nonexistent`, `--help` included**
> **The lens:** security first, then brittleness -- the 29 units that all run as root and the paths they read or run (brief § 4 Q3), the two selection mechanisms (install-time in `system-utils`, run-time in the quirks) and a reachability table of 422 with a *runs on* column, busybox's flagged applets, the three-and-a-half-week upstream drift beside every finding (44 M, 20 D, 42 A), a coverage table of 422
> **The rule:** **the lane changes none of the 422 and nothing under `packages/`, `projects/` or `tools/` at stages A to D** (D-WORKFLOW-209); a fix is a stage-E stream the coordinator writes; the class decision for anything upstream carries is the maintainer's on #346; nothing runs on a handheld
> **The host:** M6's; **one guest cycle at most**, under 30 minutes, planned on #669 at stage A and granted by the coordinator after the M7 lane's FINAL RETURN and T13's cycle; nothing boots before the grant; no build, no compiler, no fetch, no plan generation; `TMPDIR` under `/workspace/tmp/m6-t22/`
> **Register:** the three workflow IDs before 209 are the M7 lane's; D-WORKFLOW-209 is the removal rule (the coordinator's); a row this slice forces takes D-WORKFLOW-210 or higher, D-QA-064, D-INFRA-033 or higher (032 is the M7 lane's); a row is never edited
> **The brief:** `docs/reviews/briefs/os-system-services.md` at `cc8b6cf2a3` (version 3, after a stranger's proof); #669's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**T22 is closed out; the lane is idle.**
- **Accepted** at `8a4d5eb5b2` (10:50 UTC). #1103 is closed at 28 of 28, and #669 reads 17 of 18.
- **Written:** `docs/audits/2026_10_25-epic-m6-os-system-services/audit-completion.json` and its receipts under `checks/phase7-closure/`. The lint with `--issue 1103` passes, and `ceremony-check`'s validator accepts the marker.
- **Posted:** the close-out tip, on #669.
- **Open:** #1106's two fix-pending-image criteria, which wait for an image built after the merge.
- **Scratch:** `/workspace/tmp/m6-t22/` removed.

Nothing is running. **Next:** whatever the coordinator dispatches.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-os-system-services-669
cd "$D"   # no fetch of any kind: 651150fc88 is already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the dispatch's paths
test -f docs/reviews/inventory.json && echo inventory
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
sed -n '1,160p' docs/reviews/briefs/os-system-services.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905; #1012 after T12's), T5, T6, T7,
T8, T23, T40, T11, T9, T10, T12, T13, **then this branch**, then T14, T15, T45, then T4's last.
When `next` moves, the **coordinator** merges `next` into this branch, and
never between stage A and stage D; the coordinator merges its own branch
into this one at hand-back, before the last criterion's checkers run. Never
merge another lane's feature branch here. Every lane and the M7 lane append
to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made by
whole entries. Nothing here builds, touches a device, a cloud account, a
provider, a key file, the host's swap, another lane's worktree, or a guest.
