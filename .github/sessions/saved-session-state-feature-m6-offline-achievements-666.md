# Session pointer: M6.P2 T19, the offline achievements proxy (#666)

> **Seeded:** 2026-10-26 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-offline-achievements-666`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`42623ac083` at `30654cd701`, one merge, carrying the brief's versions 1 and 2, the area futro, the register rows the brief cites, the day's logs)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-offline-achievements-666` -- the audit artifacts, the work log, this pointer and every ceremony live here; anything temporary under `/workspace/tmp/m6-t19/`
> **EmulationStation:** read-only context, by `git -C /home/max/Development/emulationstation-next.worktrees/qa-integration show 16dbac5211:<path>` (the pin at `8ebaf8daad`); no ES worktree for this slice; never that checkout's working tree
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root or prep directory read**; the upstream proxy's source is the download cache's tarball (`/workspace/cache/rocknix-sources/raofflineproxy/`), never fetched
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #666 names (`m6-t5-build-engine`)
> **Epic:** #1139 (offline achievements: this slice; T20 #667 under the interface epic #700 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Extended -- **two seats, GPT-6 Astra at `max` then Gemini 4 Argon at `high`** over a trimmed, scanned packet (D-WORKFLOW-195: trim before any seat sees it; Argon fails near 437 KB), a probe then one refutation each; `review-plan.json` records depth `extended`, two reviewers; **exactly four keyed invokes**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`; the runtime from `npm install --offline`
> **The lens:** security and new functionality over 27 paths at `8ebaf8daad` (5,369 lines): nine fork-own files (the ctl, three python helpers, the recipe, the unit, the daemon file, two sibling recipes) and eighteen patches read as diffs against the pinned upstream tarball. Q1 to Q8 in four families: where a credential travels; what runs as root on an unauthenticated port; a check whose failure reads as success; a bound not enforced
> **The rule:** **the lane changes nothing under `packages/`, `projects/` or `tools/` at any stage**; a defect is a `bug` with its trace and `Already written:` line (D-WORKFLOW-187), fixed only under a stream brief the coordinator writes at the stage-D pause, in a fork-own file or on a patch's `+` side; a stream that changes a script `tools/last-good-scripts-test` covers runs the suite before its commit; a fixture rewrites no path (the real script in a bubblewrap sandbox with `--clearenv`); **the ctl never runs on the host**, and the proxy runs only on the guest
> **The host:** M6's and M7's by the shared log `/tmp/m7-m6-host-coordination-20261023.txt` (M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window** of two boots, asked for on #666 with its plan and bound after stage B and granted there in the host file's queue: a GENERIC_X64 guest from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/`, the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census, the stop by pidfile at bound plus grace, the disk retired after with path, size and sha; **the QA RetroAchievements account only** (`~/.ROCKNIX/qa-accounts`, carried by `tools/qa-accounts` over ssh stdin, never printed; D-QA-016), never the owner's (D-QA-015); the award proof last, once, and `CANNOT in this window` if the bound is reached
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-CLOUD-185 the highest cloud row and D-WORKFLOW-209 the highest workflow row (D-WORKFLOW-188 on the P1 branch only); a row this slice forces (none expected) takes an ID the coordinator assigns on #666
> **The brief:** `docs/reviews/briefs/offline-achievements-proxy.md` at `110943c58c` (version 2, after a stranger's proof of version 1 -- its corrections listed at its end); #666's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Closed out.** T19 was accepted on #666 at `c0af666edf`, and #1156 is closed. `audit-completion.json` is written, and both lints PASS (`--issue 1156` and the default phase). `/workspace/tmp/m6-t19/` and its three scratch worktrees are retired.

- **Nothing in flight here.** The session moves to T20 (#667).
- **The integration owes:**
  - every `fix-walk-pending-image` in `02` § The streams;
  - the installed-native run against the tree's service.
- **The coordinator owes:** posting the #585 lines in `02` § The patches.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-offline-achievements-666
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-CLOUD-185' docs/decision-register.md                                    # 1 or more: the coordinator's tip is merged
ls /workspace/cache/rocknix-sources/raofflineproxy/ 2>/dev/null                    # the pinned tarball, read, never fetched
tail -n 6 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
sed -n '1,140p' docs/reviews/briefs/offline-achievements-proxy.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, T17, T18, **then this branch**, then
T4's last. When `next` moves, the **coordinator** merges `next` into this
branch, and never between stage A and stage D; the coordinator merges its
own branch into this one at hand-back, before the last criterion's checkers
run. Never merge another lane's feature branch here. Every lane and the M7
lane append to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made
by whole entries. Nothing here builds an image, touches a device, the
owner's account, a cloud account, a provider, a key file, the host's swap,
another lane's worktree, or a guest outside the one granted window.

## Checkpoints

- Stage A, 2026-10-26 12:25 UTC: tip (this commit) on `7de4ece06d`; figures equal to the brief's but R8 (cache-indexed has no `>>> ` token).
- Stage B and the window, 2026-10-26 13:05 UTC: tip `3f51094560`; 25 findings; six positives fall; the image's scripts M7's (ruled 12:55).
- Stage C, 2026-10-26 13:45 UTC: four keyed calls PASS; 94 items graded; 41 findings; `05` 23 items; pre-issue lint PASS.
