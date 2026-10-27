# Session pointer: M6.P2 T31, EmulationStation's other pages (#678)

> **Seeded:** 2026-10-27 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-pages-678`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`266a14163e` at `3d591f7e30`, one merge, carrying the brief's versions 1 and 2, the register rows the brief cites, the day's logs)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-pages-678` -- the audit artifacts, the work log, this pointer and every ceremony live here
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-pages-678`, branch `feature/m6-es-pages-678`, cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`** (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `8ebaf8daad`); the sources are read and the fixes are made here, on this branch only; **the pin bump in the distribution is the coordinator's**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read**; the other ES checkouts under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's, `qa-integration` another lane's) are read with `git -C ... show` only, never checked out or written; M7's October work on this file is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #678 names (`m6-t5-build-engine`)
> **Epic:** #700 (the interface: T2 and T18 accepted and closed out; T20 #667 and T21 #668 briefed; this slice; T31 to T37, T44 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed, scanned packet (D-WORKFLOW-195: the twelve fork-touched files whole, 4,230 lines, and of the 64 upstream-carried files only the ranges the questions cite; the manifest names every trimmed file and range), a probe then one refutation; `review-plan.json` records depth `independent`, one reviewer; **exactly two keyed invokes**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`; every scan hit dispositioned by shape, a value stops the packet; a test fixture's secret-shaped literal is itself a finding (#1061)
> **The lens:** new functionality and brittleness over EmulationStation's other pages at the pin: 76 paths under `es-app/src/guis/` (GuiMenu, the cloud, RetroAchievements, offline-scan and Wi-Fi pages excluded), 15,537 lines by `grep -c`; the twelve the fork touched (3 added, 9 modified, 1,207 added and 129 removed against `cada856d86`) read line by line, the 64 byte-identical to `rocknix/master` checked against it and read for brittleness and left as upstream has them (D-UI-079); Q1 to Q7 as brief § 4 sets them. *(Corrected at stage A: the seeded line was T26's, "two files, 11,883 lines".)*
> **The rule:** **the lane changes nothing under the distribution's `packages/`, `projects/` or `tools/` at any stage, and nothing in the ES worktree at stages A to D**; a defect is a `bug` with its trace and `Already written:` line, fixed only under a stream brief the coordinator writes, on the ES branch, proven twice (`fix-unit-test` or `fix-walk-pending-image`), `tools/es-syntax-check` PASS where a toolchain exists, else the host `g++ -fsyntax-only` pass or its `CANNOT` with the missing header named (#1137), a clean non-ASCII comment grep over a stream's added lines before its commit, and **`docs/es-menu-map.md` updated in the same commit as any row added, moved or renamed, `tools/es-menu-map-check` passing (D-UI-039)**; a sentence carries its French in the same commit (D-UI-051); the walks' steps under the audit folder's `stage-e/walks/`; the pin is not moved by the lane. *(Corrected at stage A: the seeded line said "outside the two files", T26's.)*
> **The host:** M6's and M7's by the shared log `/tmp/m7-m6-host-coordination-20261023.txt` (M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window**, asked for on #678 with its plan and bound after stage B and granted in the host file's queue: one GENERIC_X64 guest from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/`, started at 640x480 (`generic-x64-vm run --res`; `vm-pair` has no option, #1141), the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census, the stop by pidfile at bound plus grace, the disk retired after with path, size and sha; the fork pages' walks with their strings read back, the wizard's transitions, the confirmations' back-button landing, the rows' stores read from both files after a page close; **the QA accounts only** (`tools/qa-accounts`, never printed; D-QA-016), never the owner's (D-QA-015)
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-WORKFLOW-212, D-NET-017 and D-CLOUD-186 the last three decided rows (D-WORKFLOW-188 on the P1 branch only); a row this slice forces (none expected) takes an ID the coordinator assigns on #678
> **The brief:** `docs/reviews/briefs/es-pages.md` at `34e130d2ce` (version 2, after a stranger's proof of version 1 -- its corrections listed at its end); #678's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage A done** (12:00 to 12:07 UTC; committed 12:07:06, posted 12:07:50). **Stage B done** (12:23 UTC): `02` with its sections and 25 leads, six generators, the window plan; the window asked for on #678.
`docs/audits/2026_10_27-epic-m6-es-pages/`: `00-running-log.md` (the header and § Stage A),
`01-research-notes.md` (§ Scope, § History, § Callers, § Context), `stage-a/` (the first
commands, the membership block, the § 5 runs and their output, the reruns, the callers, the
history) and `tools/` (`t31-callers.py`, `t31-run-runs.py`). Every § 5 figure as the brief
expects; the brief's non-ASCII adjacency grep is a basic-regex error (`'_\("'`), rerun with
`-F`: 0. `GuiAutoScrape` has no caller at the pin (a Q7 lead).

**Next:** the window when granted on #678 (`stage-b/window-plan.md`), and stage C beside it: the host proofs under `stage-c/` (the plan's list), `03`, `04`, the packet trimmed and scanned, the seat (GPT-6 Astra at max, two keyed invokes), the pre-issue lint.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-pages-678; cd "$D"
W=/home/max/Development/emulationstation-next.worktrees/m6-es-pages-678; PIN=16dbac5211
A=docs/audits/2026_10_27-epic-m6-es-pages
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l            # the pin; 0
cat "$A/00-running-log.md"; sed -n '584,800p' docs/reviews/briefs/es-pages.md   # § 4 the questions, § 5 the floor
tools/archaeology 'save state manager' | head -60; tools/archaeology 'scrape' | head -60
python3 -I "$A/tools/t31-callers.py" "$W" "$PIN" .qa-scratch/t31/paths.txt | tail -1   # classes 39; 1 without a caller
tail -n 6 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200        # the host, before the window request
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, T17, T18, T19, T20, T21, **then this
branch, with the pin moved to the ES branch's tip in the same integration
commit**, then T4's last. When `next` moves, the **coordinator** merges
`next` into this branch, and never between stage A and stage D; the
coordinator merges its own branch into this one at hand-back, before the
last criterion's checkers run. Never merge another lane's feature branch
here, in either repository. Every lane and the M7 lane append to
`docs/decision-register.md`, the day's work log and `docs/work-logs/INDEX.md`:
keep every append, regenerate the index, never edit another lane's rows; a
merge with conflicts is checked for leftover markers before it is committed
(#696), and a union of two ledgers is made by whole entries. Nothing here
builds an image, touches a device, a cloud account, a provider, a key file,
the host's swap, another lane's worktree, or a guest outside the one
granted window.

## Checkpoints

- Stage B: distribution `<this commit>`, ES at the pin, window requested
- Stage A: distribution `c252de767f` (pointer `87f679e0ce`), ES at the pin `16dbac5211`, posted 12:07:50 UTC (accepted 12:09 UTC)
