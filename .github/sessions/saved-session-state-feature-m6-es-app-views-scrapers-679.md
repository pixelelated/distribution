# Session pointer: M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

> **Seeded:** 2026-10-27 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-app-views-scrapers-679`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`42cb00860c` at `121d0180f0`, one merge, carrying the brief's versions 1 and 2, the register rows the brief cites, the day's logs)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-app-views-scrapers-679` -- the audit artifacts, the work log, this pointer and every ceremony live here
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-app-views-scrapers-679`, branch `feature/m6-es-app-views-scrapers-679`, cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`** (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `8ebaf8daad`); the sources are read and the fixes are made here, on this branch only; **the pin bump in the distribution is the coordinator's**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read**; the other ES checkouts under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's, `qa-integration` another lane's) are read with `git -C ... show` only, never checked out or written; M7's October work on this file is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #679 names (`m6-t5-build-engine`)
> **Epic:** #700 (the interface: T2 and T18 accepted and closed out; T20 #667 and T21 #668 briefed; this slice; T32 to T37, T44 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed, scanned packet (D-WORKFLOW-195: the six fork-modified files whole, 4,005 lines, and of the 36 upstream-carried files only the ranges the questions cite; `services/httplib.h` is vendored, 5,713 lines, cited ranges only, never whole; every scan hit dispositioned by name in `packet-manifest.json`, the scrapers' developer-credential macro gates named, never valued), a probe then one refutation; **exactly two keyed `tools/council/run invoke` calls**, every other council call with `COUNCIL_ENV_FILE=/nonexistent`.
> **The lens:** cost against value over 42 paths at the pin (17,311 lines; the fork modified six, +168/-46, and 36 are byte-identical to ROCKNIX's master; no upstream commit on the slice since the merge base `cada856d86`, so the merge debt is a one-line record): the game list views and their containers, the scrapers less `ScreenScraper.*`, the local HTTP service; seven questions in the brief's § 4 (lifetime and threads; bounded calls; reads that read as success; uncached reads; the words, the French and the help bars; the views and their cost; the structure, the map and the merge debt), with the floor's thirty-five pure leads in the brief.
> **The rule:** **the lane changes nothing under the distribution's `packages/`, `projects/` or `tools/` at any stage, and nothing in the ES worktree outside the 42 paths at stages A to D**; `views/ViewController.*` is T2's, `scrapers/ScreenScraper.*` T21's, and every page under `guis/` (`GuiScraperStart`, `GuiScraperRun`, `GuiGameScraper` included) T31's -- the globs decide; T21's ES tip `3ae9610b0` is read for its `Scraper.cpp` and `ScraperReplies` deltas and each is recorded as inherited, every collision named in the hand-back; a defect is a `bug` with its trace, its `Already written:` line and its VM line (D-WORKFLOW-050, `bugs-are-agent-first.md`); a lead outside the 42 is a Backlog the coordinator files.
> **The host:** M6's and M7's by the shared log `/tmp/m7-m6-host-coordination-20261023.txt` (M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window**, asked for on #679 with its plan and bound after stage B and granted in the host file's queue: one GENERIC_X64 guest from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/`, started at 640x480 (`generic-x64-vm run --res`; `vm-pair` has no option, #1141), the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census, the stop by pidfile at bound plus grace, the disk retired after with path, size and sha; the fork pages' walks with their strings read back, the wizard's transitions, the confirmations' back-button landing, the rows' stores read from both files after a page close; **the QA accounts only** (`tools/qa-accounts`, never printed; D-QA-016), never the owner's (D-QA-015)
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-WORKFLOW-212, D-NET-017 and D-CLOUD-186 the last three decided rows (D-WORKFLOW-188 on the P1 branch only); a row this slice forces (none expected) takes an ID the coordinator assigns on #679
> **The brief:** `docs/reviews/briefs/es-app-views-scrapers.md` at `85307da3b3` (version 2, after a stranger's proof of version 1 -- its corrections listed at its end); #679's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Idle. T32 (#679) is closed out** -- accepted by the coordinator at 18:35 UTC (#679 comment 6450480649) at distribution `6b372e1ab7` / ES `b52245036`; #1257 closed with its 22 checkboxes ticked; `audit-completion.json` written from #1257's closed readback; `tools/lint-audit-artifacts --issue 1257` and the default phase PASS; the 23 #585 lines posted on #585 (comment 6450506376, none sent); `/workspace/tmp/m6-t32/` retired after a check that nothing ran there. The twelve bugs #1258 to #1269 stay open until the pin moves on `next`; the guest halves are owed at the integration window (the hand-back post on #679, comment 6450217632). Nothing runs for this lane.

**The session's next slice is T33 (#680), in its own worktree, by the coordinator's dispatch comment there** -- not on this branch.

## Next commands

```bash
# nothing for T32; the record is the audit folder and #679
gh issue view 680 --repo pixelelated/distribution --comments | tail -40
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

- (none yet; the executor appends one line per stage: the stage, both tips, the time)
