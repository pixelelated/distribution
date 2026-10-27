# Session pointer: M6.P2 T33, EmulationStation's system layer: game lists, collections, metadata, and the fork's helper units (#680)

> **Seeded:** 2026-10-27 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-app-system-680`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`ab3678cc09` at `cbe03cdaed`, one merge, carrying the brief's versions 1 and 2, the register rows the brief cites, the day's logs)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-app-system-680` -- the audit artifacts, the work log, this pointer and every ceremony live here
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-app-system-680`, branch `feature/m6-es-app-system-680`, cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`** (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `8ebaf8daad`); the sources are read and the fixes are made here, on this branch only; **the pin bump in the distribution is the coordinator's**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read**; the other ES checkouts under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's, `qa-integration` another lane's) are read with `git -C ... show` only, never checked out or written; M7's October work on this file is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #680 names (`m6-t5-build-engine`)
> **Epic:** #700 (the interface: T2, T18, T20, T21, T26, T31 and T32 accepted -- their issues open until the integration moves the pin; this slice; T34 to T37 and T44 after; corrected at stage A, 2026-10-27); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed, scanned packet (D-WORKFLOW-195: the 27 fork-added files whole less the Windows residue, the fork's hunks of the 4 modified files, and of the 46 upstream-carried files only the ranges the questions cite; `Win32ApiSystem.cpp` and `EmulationStation.aps` never whole; the credential macros are the top-level `CMakeLists.txt`'s, outside the 77, and no value goes anywhere), a probe then one refutation; **exactly two keyed `tools/council/run invoke` calls**, every other council call with `COUNCIL_ENV_FILE=/nonexistent`.
> **The lens:** cost against value over the 77 paths the `rest` selector leaves at the pin (16,276 lines; 27 fork-added and 4 fork-modified, +2,689/-7; 46 byte-identical to ROCKNIX's master; 0 upstream commits on the 77 since the merge base `cada856d86`, so the merge debt is a one-line record): the game lists, collections, metadata and filter library, the fork's 29 helper units whose pages live in other slices, and the Windows residue no image compiles; seven questions in the brief's § 4 (lifetime and threads; bounded calls; reads that read as success; uncached reads and in-place writes; the words and the French; the library's cost; the structure, the map and the merge debt), with the floor's pure leads in the brief.
> **The rule:** **the lane changes nothing under the distribution's `packages/`, `projects/` or `tools/` at any stage, and nothing in the ES worktree outside the 77 paths at stages A to D**; `ApiSystem.*` and `main.cpp` are T21's, `FileData.*`/`SystemData.*`/`ViewController.*` T2's, `CloudText.*` T18's, `guis/` T31's, `views/`/`scrapers/`/`services/` T32's, `es-core/` the es-core slices' -- the globs decide; T21's and T20's ES tips are read for their deltas in `es-app/CMakeLists.txt`, `WifiText.*` and `OfflineAchievementsText.*` and each is recorded as inherited, every collision named in the hand-back; a defect is a `bug` with its trace, its `Already written:` line and its VM line (D-WORKFLOW-050, `bugs-are-agent-first.md`); a lead outside the 77 is a Backlog the coordinator files.
> **The host:** M6's and M7's by the shared log `/tmp/m7-m6-host-coordination-20261023.txt` (M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window**, asked for on #680 with its plan and bound after stage B and granted in the host file's queue: one GENERIC_X64 guest from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/`, started at 640x480 (`generic-x64-vm run --res`; `vm-pair` has no option, #1141), the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census, the stop by pidfile at bound plus grace, the disk retired after with path, size and sha; the fork pages' walks with their strings read back, the wizard's transitions, the confirmations' back-button landing, the rows' stores read from both files after a page close; **the QA accounts only** (`tools/qa-accounts`, never printed; D-QA-016), never the owner's (D-QA-015)
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-WORKFLOW-212, D-NET-017 and D-CLOUD-186 the last three decided rows (D-WORKFLOW-188 on the P1 branch only); a row this slice forces (none expected) takes an ID the coordinator assigns on #680
> **The brief:** `docs/reviews/briefs/es-app-system.md` at `c48f8b387e` (version 2, after a stranger's proof of version 1 -- its corrections listed at its end); #680's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage A done and accepted (18:43 UTC, #680; the two errata are the coordinator's). Stage B in progress (18:44 UTC).** The coordinator's instruction: stage B -- `02-forward-audit.md` with its sections, every table generated by a tool under the audit folder's `tools/` that asserts its counts and was seen to exit 1 on a constructed drift -- then the window request on #680 with its plan and bound (the host is free); a turn ends on a post or a commit.

**Stage B, in order** (all four landed by 18:58 UTC; the request is posted on #680 and waits for the coordinator's grant):
1. Read the brief's § 2's leads, § 4's floor, § 5 and § 6 at their lines. Done.
2. The generators under `docs/audits/2026_10_27-epic-m6-es-app-system/tools/` are `t33-reads.py` (83/86/4), `t33-writes.py` (11), `t33-bounds.py` (4 http, 6 process, 4 waits, 2 bounded), `t33-library.py` (11 units), `t33-helpers.py` (17 units, 12 cases, 7 built) and `t33-words.py` (176/223/196). Each was seen to exit 1 on a wrong count and on a paths list with its file dropped (`stage-b/generators.txt`). Done.
3. `stage-b/02-template.md` has the sixteen sections and is composed by `tools/t33-02.py` into `02`: coverage 77, 27/4/46, inventory 31/46. Done.
4. The window plan is `stage-b/window-plan.md` (25 + 5 minutes; the plan sums to 1,260 s; G-05, G-07 and G-09 are `CANNOT`). The request is on #680. Done.

**The window ran and returned.** Granted at 19:00 UTC; START 19:01:31; stopped by pidfile at 19:14:06; RETURN posted (comment 6451273341) and in the host file; the disk retired. The results are in `02` § The guest cycle:
- L-05 and L-28 were reproduced on the image.
- L-06 did not fault once.
- G-03's index toast and `exec.log` were not shown.

**Next: stage C's host work**, in this order:
1. `t33-includes.py`'s expectations.
2. `t33-build-tests.sh` extended to `tests/app-unit`'s `app-unit-tests` (its fakes before `es-app/src`).
3. The six FAIL-at-pin cases (3.9, 3.13, 3.21, 3.29, 3.31, 3.35).
4. The harnesses for L-06 (ASan extract), L-07 and L-12.
5. `03` and `04`.
6. The packet and the two keyed council calls.
7. The pre-issue lint.

After that comes stage D: `05`, the audit issue under #680, and the pause.

**Scratch:** `/workspace/tmp/m6-t33/` (`tmp/`, `rj/` the recipe's rapidjson). `stage-a/env.sh` holds the paths.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-app-system-680
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-RA-050' docs/decision-register.md                                       # 1 or more: the coordinator's tip is merged
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-system-680
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                      # the pin; 0
tail -n 6 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
sed -n '1,150p' docs/reviews/briefs/es-app-system.md
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

- window, 2026-10-27 19:01-19:14 UTC: G-01..G-10 run (G-05/07/09 CANNOT); L-05 and L-28 reproduced on the image; RETURN posted; distribution `d680658464`
- stage B, 2026-10-27 18:58 UTC: `02` composed (16 sections; the five generated tables and the words, each asserted and drift-tested); the window plan; the request posted on #680
- stage A, 2026-10-27 18:4x UTC: distribution `27bd8499f1` + stage A's record, ES `16dbac5211` (the pin, clean); every § 1, § 2 and § 5 figure as the brief expects; the stand-in 29/29 rc 0; next: stage B (`02`), then the window request
