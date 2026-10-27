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

**Stages A and B done; the window run and recorded (16:08:36 to 16:22:34 UTC, the disk retired); stage C in progress (16:24 UTC).** The coordinator's instruction (16:24 UTC): run stage C whole -- the host proofs under `stage-c/` (the six FAIL-at-pin leads first, each seen to FAIL against the unfixed extract before a fix shape is trusted), the include graph, `03` and `04`, the packet trimmed and scanned with every hit dispositioned, the two keyed seat calls, the pre-issue lint -- then `05` and the audit issue, and **end the turn only on the stage-D pause post with the punch list and the questions** (or an earlier question that needs the coordinator).

**Stage C, in order, and where each stands** (tick here as each lands):
1. **DONE** (`stage-c/build-pin.txt`: `TOTAL: 221 test cases in 4 binaries`). `tools/t32-build-tests.sh`: T21's `t21-build-tests.sh` (`git show origin/feature/m6-es-state-and-bridge-668:docs/audits/2026_10_26-epic-m6-es-state-and-bridge/tools/t21-build-tests.sh`) or T31's `t31-build-tests.sh` renamed; rapidjson is at `/workspace/tmp/m6-t32/rj/rapidjson-1.1.0/include` (the recipe's tarball, sha matching, four patches). Its `TOTAL:` line is quoted, never summed.
2. **DONE 16:38 UTC** (`stage-c/runs.txt`; `l310`, `l313`, `l316`, `l327`, `l331`, `l332`, `l02` each FAIL at the pin, control rc 0; 3.10's string boxart, L-22's numeric token and L-02 are memory errors: a SEGV, a SEGV and a use-after-free; L-22 and L-23 new; DetailedContainer:1049 does not wrap; G-06 corrected on #679 at 16:28). The six FAIL-at-pin cases, as stage-C harnesses over the pin's extracts (T31's `stage-c/` shape: `t31extract.function`, doubles, compiled under ASan) or as doctest files, each with its FAIL recorded at the pin: **3.10** (`GamesDBJSONScraper.cpp:605-607`, `"boxart": []`), **3.13** (`Scraper.cpp:289` update, `:337`, `:372-376` over a doubled `HttpReq` and `SDL_GetTicks`), **3.16's remainder** (`IGDBScraper.cpp:314-331` returns false; `:143-144`; also read `isSupportedPlatform` `:221-230` for G-06's empty systems list), **3.27** (`SystemView.cpp:272` `_moveCursorInRange(2,-10,5)` -> -3), **3.31** (`GridGameListView.cpp:131-153` IMAGE returns empty), **3.32** (`GameNameFormatter.cpp:84-85` the two ASCENDING tests; `:171-185` the 25-hour wrap; and `DetailedContainer.cpp:1049`). Also L-02 (`progress()` cancelled over finished, `ThreadedScraper.cpp:331`).
2b. **DONE** (`stage-c/floor.md`, 27 ids: 11 holds, 1 design, 15 findings; 3.15 and 3.19 re-read). The other floor items marked "at C" (3.1-3.9, 3.11, 3.12, 3.14, 3.15, 3.17-3.25, 3.28-3.30, 3.34): a verdict each in `stage-c/floor.md` (read; a harness only where a read cannot settle it).
3. **DONE** except G-03 (left open: 3.29 does not explain it) and the French bar (3.34, consistent, not proved). Read at C, from the window (G-06 done): G-03 (the letter jump through T31's `GuiGamelistOptions` and `ISimpleGameListView::moveToLetter` `:486-603` -- why the cursor stayed on Alpha), the French bar's missing SAVE STATES (`ISimpleGameListView::getHelpPrompts` `:681-741`), L-18's caller `components/ScraperSearchComponent.cpp:261` (which thread), L-16's holders (`CollectionSystemManager::reloadCollection`).
4. **DONE** (`stage-c/includes.out`). `tools/t32-includes.py` (the include graph: expect 47 include lines from 23 files outside, es-core edges 143 of 410).
5. **DONE before the seat** (04's § Second opinion after it). `03-retrospective.md`, `04-analysis.md` (Q1 to Q7 at their lines) -- T31's shape.
6. **DONE** (the packet 433,943 bytes, 0 for review; the probe and the refutation PASS; 40 items, all accepted, `stage-c/astra-grades.md`). Was: `stage-c/packet.py` and `stage-c/ask.md` are written (T31's builder adapted; DISPOSITIONS empty until the first build's STOP list). Build: `SECRET_PATTERNS="$(grep -v '^#' .githooks/secret-patterns | paste -sd'|')" python3 -I -B $A/stage-c/packet.py $PWD $W $A/second-opinions/packet.md $A/second-opinions/packet-manifest.json` (check T31's 00 for the exact SECRET_PATTERNS line). The packet: `second-opinions/` (`review-plan.json` depth independent, one reviewer gpt `openai/gpt-6-astra` max; `packet-manifest.json` with every scan hit dispositioned by file:line, `httplib.h` by ranges only); the two keyed `tools/council/run invoke` calls (probe, refutation), every other call `COUNCIL_ENV_FILE=/nonexistent`; T31's `second-opinions/` and `00` are the model.
7. **DONE through the issue:** the lint PASS; `05` 20 items; the audit issue #1257, a sub-issue of #679; box-check 0 fail. **Then the stage-D pause post, and wait for the coordinator's ruling: file the ten bugs with their traces (T31's `t31-file-bugs.py` shape), write the stream briefs, stage E.** Was: `tools/lint-audit-artifacts --phase pre-issue <A>`; then `05-punch-list.md`, the audit issue (a sub-issue of #679), the bugs; the stage-D pause post on #679.

**Facts the record already holds:** 02 is composed by `python3 -I tools/t32-02.py <A> <W> 16dbac5211 .qa-scratch/t32/paths.txt` from `stage-b/02-template.md` (edit the template, never 02); the window's verdicts are in 02 § The guest cycle; L-01 to L-21 in 02 § The leads; corrections to the brief in 02 § The runs.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-app-views-scrapers-679; cd "$D"
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-views-scrapers-679; PIN=16dbac5211
A=docs/audits/2026_10_27-epic-m6-es-app-views-scrapers
git -C "$W" status --short | wc -l                      # 0: the ES worktree stays at the pin until stage E
tail -n 40 "$A/00-running-log.md"; ls "$A/stage-c" "$A/second-opinions" 2>&1
python3 -I "$A/tools/t32-02.py" "$A" "$W" "$PIN" .qa-scratch/t32/paths.txt   # recompose 02 after a template edit
gh issue view 679 --repo pixelelated/distribution --comments | tail -40
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
