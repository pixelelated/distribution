# Session pointer: M6.P2 T17, cloud sync: setup, sign-in, connections, content and settings backups (#664)

> **Seeded:** 2026-10-26 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-cloud-setup-content-664`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`608315f65f` at `3c8a28918f`, one merge, carrying the brief's versions 1 and 2, the register rows the brief cites, the day's logs)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-setup-content-664`; the earlier worktrees of this session beside it, read with `git show`, never checked out again
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root or worktree read**; M7's work on these same scripts (#1111, #1113, #1115, #1117) is cited by number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #664 names (`m6-t5-build-engine`)
> **Epic:** #1047 (the cloud area: T13 accepted and closed out, T16 at stage C with its window to re-grant, this slice last); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Extended -- **two seats, GPT-6 Astra at `max` then Gemini 4 Argon at `high`** over a trimmed, scanned packet (D-WORKFLOW-195), a probe then one refutation each, as T22's and T16's stage C; `review-plan.json` records depth `extended`, two reviewers; **exactly four keyed invokes**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`; **the packet's three-way scan hits every one of these files' comments and names -- each hit gets a disposition, a value stops the packet**
> **The lens:** security, with state preservation as the depth reason, over 14 files (11,180 lines, every one read; 13 fork-own and `backuptool` the fork's rewrite of upstream's 68-line script). **One writer of `rclone.conf`** (`cloud_connections.atomic()`; `cloud_remote create` reaches it through `connections.save`; `cloud_setup` writes none); **one deleting path** (`--match --apply`, two statements under the preview's count, `--max-delete` a cap not a transaction); Q3 in two families (where a secret can travel; what the deleting path can delete); two generated tables (§ The writers, § The secrets' paths)
> **The rule:** **the lane changes nothing under `packages/`, `projects/` or `tools/` at stages A to D**; a defect is a `bug` with its trace and `Already written:` line, fixed only under a stream brief the coordinator writes; **a credential-shaped line is never quoted and never written to a file at rest** (D-QA-021, D-WORKFLOW-061; #1061 is the case); every config-shaped read through `grep -v -i -E 'key|pass|token|user|psk'`; **nothing on a person's device or cloud** (D-QA-015, blindspot 38); **`rm -rf` only as `"${VAR:?}"/...` or a literal path, in its own short command, never inside a `bash -c` script**
> **The host:** M7's under the coordinator's handoff of 2026-10-26 04:47 on `/tmp/m7-m6-host-coordination-20261023.txt` (M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window**, asked for on #664 with its plan after stage B and granted **only after M7's guest RETURN there and after T16's re-granted window has returned**: one GENERIC_X64 guest from M6's `069fc2704421` copy, the QA backends on the lane's own isolation under `/workspace/tmp/m6-t17/`, 30 minutes from START, START/RETURN posted, stop by pidfile, the leftover check, every output kept; the fourteen installed files hashed against `git show 8ebaf8daad:<path>` before any verdict; the phone page from the host is `CANNOT` with the gap named unless the harness can reach it
> **Register:** the rows this brief cites (D-WORKFLOW-190, 195, 209; D-QA-063) are on the coordinator's branch, merged here; D-WORKFLOW-209 is the highest Decided row (D-WORKFLOW-188 on the P1 branch only); a row this slice forces (none expected) takes an ID the coordinator assigns on #664
> **The brief:** `docs/reviews/briefs/cloud-setup-content.md` at `71ded3ac40` (version 2, after a stranger's proof of version 1 -- eleven corrections, listed at its end); #664's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stages F to H done; the third hand-back is posted on #664; the lane is idle** (09:17 UTC).
- `05`: 21 Resolved and 2 Deferred. The default-phase lint `PASS`.
- The retro is posted. The five checkers are green on the branch after the coordinator's merge `8592f91054`.
- `reviewed-at: f3803436b8`, `fixed-at: 479cd96c24`.
- `/workspace/tmp/m6-t17/` is kept until acceptance.

**Next:** the coordinator's acceptance (`AUDIT_ISSUE=1134`); then `audit-completion.json` and the full lint, as prompted.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-setup-content-664
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-WORKFLOW-209' docs/decision-register.md                                 # 1 or more: the coordinator's tip is merged
tail -n 6 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
sed -n '1,160p' docs/reviews/briefs/cloud-setup-content.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, **then this branch**, then T4's last.
When `next` moves, the **coordinator** merges `next` into this branch, and
never between stage A and stage D; the coordinator merges its own branch
into this one at hand-back, before the last criterion's checkers run. Never
merge another lane's feature branch here. Every lane and the M7 lane append
to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made
by whole entries. Nothing here builds, touches a device, a cloud account, a
provider, a key file, the host's swap, another lane's worktree, or a guest
outside the one granted window.

## Checkpoints

- Stage A: `64ff2f519f`, 2026-10-26 06:15 UTC.
- Stage B: `ee45aa9262`, 2026-10-26 06:41 UTC.
