# Session pointer: M6.P2 T16, cloud sync: the sync, backup, restore and capture core (#663)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-cloud-sync-core-663`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`2cc743efd6` at `7cf9826140`, one merge, carrying the brief's versions 1 and 2, D-WORKFLOW-209, the device briefs and T27's errata); the lane's commits on top
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663`; the earlier worktrees of its session beside it, read with `git show`, never checked out again
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read** (`m7-signin-sm8550-build-20261025-01` is a name, never a path opened)
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #663 names (`m6-t1-os-launch`)
> **Epic:** #1047 (the cloud area: T13 accepted and closed out, this slice, then T17); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Extended -- **two seats, GPT-6 Astra at `max` then Gemini 4 Argon at `high`** over a trimmed, scanned packet (D-WORKFLOW-195), a probe then one refutation each, as T22's stage C; `review-plan.json` records depth `extended`, two reviewers; **exactly four keyed invokes**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`
> **The lens:** security, brittleness and new functionality over the fork's own 14 files (8,316 lines; two copy-twins and the capture are 6,538 of the 7,827 read lines) -- Q3 leads; T13's 79-row assertion table is the oracle (24 both ends, 46 synthetic, 8 device report); the three stamp families, the one `flock`, exits 69 and 75, the 90 s bound; D-CLOUD-076 superseded by 109/130; #909's drift in the rule
> **The rule:** **the lane changes nothing under `packages/`, `projects/` or `tools/` at stages A to D**; every file is the fork's own, so a defect is a `bug` with its trace and `Already written:` line, fixed only under a stream brief the coordinator writes; **nothing on a person's device or cloud** (D-QA-015, blindspot 38); no hosted account (D-QA-058)
> **The host:** M6's; this slice runs **one guest window** (granted on #663 on request after stages A and B: one GENERIC_X64 guest, the QA WebDAV on the lane's own isolation under `/workspace/tmp/m6-t16/`, about 20 minutes, a 30-minute bound, START/RETURN posted, stop by pidfile, the leftover check, every output kept; the installed scripts diffed against the read tree before any verdict), no build, no compiler, no fetch, nothing on a handheld, no M7 build root read
> **Register:** D-WORKFLOW-209 is the highest Decided row on the coordinator's branch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); other lanes may take the next IDs; a row this slice forces (none expected) takes an ID the coordinator assigns on #663
> **The brief:** `docs/reviews/briefs/cloud-sync-core.md` at `2cc743efd6` (version 2, after a stranger's proof of version 1); #663's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage D done (2026-10-30). Waiting for the coordinator's stream brief (`t16-streams.md`) and the stage-E dispatch.**

- **The ruling is applied:** the 25 outcomes are in `05` and on #1295 (25 ticked).
- **The seven bugs:** #1298 (PL-01), #1299 (PL-02), #1300 (PL-03), #1301 (PL-04), #1302 (PL-05), #1303 (PL-06), #1304 (PL-07).
- **Elsewhere:** #909 (PL-11), #1057 (PL-13), #1297 (PL-15) and #1296 (F-15). PL-24 is a design.
- **ES read at `16dbac5211`** in `02` § The ES stop and the why texts. The rule's rc 3/4 and 7/8 sentences are the coordinator's to correct; name that in the hand-back.
- **Next:** stage E under the stream brief.
  - **Window-pending, at the integration window (`fix-walk-pending-image`):** lead (c)'s timings, and F-03's image half.
  - **Stage-E host fixtures:** the capture's TERM, and the clock step.
- **Scratch to retire at close-out** (literal paths): `/workspace/tmp/m6-t16/hl/`, `/workspace/tmp/m6-t16/packet*`, `/workspace/tmp/m6-t16/bugs/` and `/workspace/tmp/m6-t16/g01.pids`.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-WORKFLOW-209' docs/decision-register.md                                 # 1 or more: the coordinator's tip is merged
tail -3 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l   # the host file since the 2026-10-28 reboot
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
sed -n '1,140p' docs/reviews/briefs/cloud-sync-core.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905; #1012 after T12's), T5, T6, T7,
T8, T23, T40, T11, T27, T25, **then this branch**, then T9, T10, T12, T13,
T22, T14, T15, T45, then T4's last. When `next` moves, the **coordinator**
merges `next` into this branch, and never between stage A and stage D; the
coordinator merges its own branch into this one at hand-back, before the
last criterion's checkers run. Never merge another lane's feature branch
here. Every lane and the M7 lane append to `docs/decision-register.md`, the
day's work log and `docs/work-logs/INDEX.md`: keep every append, regenerate
the index, never edit another lane's rows; a merge with conflicts is checked
for leftover markers before it is committed (#696), and a union of two
ledgers is made by whole entries. T11's F-09 note (a merge of `next` keeps
GENERIC_X64 in the kernel override's version case), T27's PL-02 (upstream's
atf URL with both checksums) and #1099 (upstream's Qualcomm boot change:
both ABL slots' `Already written:`, the loader entry's identity) are the
coordinator's merge notes, inherited here for the record. Nothing here
builds, touches a device, a cloud account, a provider, a key file, the
host's swap, another lane's worktree, or a guest.

## Checkpoints

- stage A: 00, 01 § Scope, the friction line, the work-log entry; `5d0a65d334`; 11:39 UTC (accepted by the coordinator 11:4x)
- stage B: 02 and its two generators; `6ce90c7c57`; 11:5x UTC; window asked for
- stage C first reader: 03, 04, two fixtures; `ab32ce5745`; 2026-10-25 11:55 UTC; window START 11:56:21Z, cut at ~12:08 by the usage limit
- resumed 2026-10-29 18:0x UTC: state reconciled from the record; waiting on the re-granted window
- 2026-10-29: merge `1bb8ad08e7`; window START 18:10:18Z, RETURN 22:31:21 (overrun 3 h 46 min, session cut); disks retired; record committed
- 2026-10-30: the leads ruled (05:15); the host leads (05:24-05:35); KILL2 graded F-14, KILL15 F-15, F-02 re-graded, F-03 proved; three corrections; next, the packet and the seats
- 2026-10-30: packet `552a6b525c`; Astra graded `4ee3eaba1f`; Argon graded and 05 `4853bdbd5c`; #1295 `9cdcc98bec`; stage-D pause posted
- 2026-10-30: the stage-D ruling applied; bugs #1298-#1304; #1295 ticked
