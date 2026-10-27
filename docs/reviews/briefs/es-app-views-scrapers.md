# Review brief: M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

**Version 2, 2026-10-27, after a stranger's proof of version 1 (`2ed286145d`); the corrections are listed at the end.**
(D-WORKFLOW-189; `docs/reviews/plan-for-the-plan.md` § 6b `:301`.) The
five read-only digests version 1 was drafted from (membership, fork
changes, upstream delta, inherit, floor) are the coordinator's scratch
files, not in any tree, so every figure they gave is reproduced by a
command below, at the hash it names, with `/usr/bin/grep` and never the
shell's function (#1138), and the floor's 35 leads are carried in § 4 so a
session with only this file has them. The proof ran the membership block,
the § 1 commands and the § 5 runs against the P1 research clone and the
`qa-integration` checkout at the pin, settled version 1's four
unverified items, and made 48 spot checks; what it corrected is applied
in place and listed in the last section. Nothing in this brief is left
unverified.

## 1. Identity

- **Issue:** #679 `M6.P2 E339/T32: interface: EmulationStation's game list
  views, scrapers and services`, retitled `M6.P2 E700/T32: ...` at dispatch
  (`milestone-phase-naming.md`; the body says *"under epic #339 until this
  area's epic is filed"*, and #700 is filed; #678 was retitled the same way
  today), slice `es-app-views-scrapers` (`k: 32`) in
  `docs/reviews/slices.json`, thirty-second in `docs/reviews/order.md`
  (`order.md`, `slices.json` and `inventory.json` are the P1 branch's, which
  the lane's worktree is stacked on -- a reader of the coordinator's branch
  alone cannot open them; the drafter read them in the P1 research clone
  `/workspace/tmp/m6-coordinator/t11-research/tree` at `2174265e9c`; its
  § T32 at `order.md:603-611`: *"42 paths, 17,311 lines, 17,311 read, of
  which 4,005 fork-own; 0 patch and config lines; reach shipped 42"*; its
  `why`: *"`views/` (8,155 lines, ViewController and the game list
  containers the fork changed) and the scrapers (ScreenScraper's credential
  wiring is read in `es-state-and-bridge`)"*; **kind currency; lens cost
  against value**; read before none; depth Independent, *"an ordinary code
  slice"*; interacting subsystems *"the scrapers' developer credentials
  (`device-builds.md` § Build credentials); the launch path (game list to
  launch)"*; closing evidence *"audit folder, lint PASS, punch list through
  Phase 7"*). **The two membership sources disagree on a glob, and
  `slices.json` decides:** `order.md:607` prints one negative glob,
  `!es:es-app/src/views/ViewController.*`; the slice's `select` in
  `slices.json` carries two, the second
  `!es:es-app/src/scrapers/ScreenScraper.*`, and § 2's block follows
  `slices.json` (46 - 4 = 42). The `order.md` line is the coordinator's to
  fix on the P1 branch, not a finding for the lane. **Epic:** #700 `M6.P2
  E339: Area epic: the interface, EmulationStation (T2, T18, T20, T21, T26,
  T31 to T37, T44)`: T2 #649, T18 #665, T20 #667, T21 #668 and T26 #673 are
  **accepted, and their issues stay open** until the integration moves the
  pin on `next` (§ 10) -- `gh issue view` on each prints OPEN today; their
  errata are in the futro `docs/futros/2026-10-23-m6-interface.md` dated
  2026-10-26 and 2026-10-27; T31 #678 was dispatched today at 12:01 UTC and
  is in flight; this slice; T33 to T37 and T44 after. The futro takes a T32
  kickoff addendum written by the coordinator with this version.
  **Milestone:** M6. **Predecessors:** T21 #668, T2 #649, T20 #667, T18
  #665, T26 #673, T31 #678 (in flight), T10 S9 #965 and the menu map
  `docs/es-menu-map.md` (D-UI-039 at `:668`) each routed items here by name;
  every one is listed with its lines and its disposition in § 2 under
  *Already found; do not re-find; take up*, which is the one place they
  live. **Beside it:** T31's lane, which holds the running session; the host
  shared through `/tmp/m7-m6-host-coordination-20261023.txt`; a window for
  this slice is asked for on #679 and granted there and in that file's
  queue (§ 5 item 2 says how).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of scope:
  those are the coordinator's, reached through #679, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already written:`
  line (D-WORKFLOW-187). A fix lands only under a stream brief the
  coordinator writes at the stage-D pause, **on the EmulationStation
  branch**. **Thirty-six of the 42 paths are byte-identical to ROCKNIX's
  master today** and six are the fork's by modification: no file in this
  slice was added by the fork (168 lines added and 46 removed against the
  merge base, `git diff --shortstat`), so the inventory's `fork-own` tier
  is the read's `fork-modified` for all six (§ 2). A defect in a line the
  fork wrote is the fork's to fix; a defect in an upstream line is a
  contained fix under `bugs-are-agent-first.md` rule 6 (`:76`) and a #585
  line (D-WORKFLOW-164, never sent, D-WORKFLOW-165). D-UI-079's lanes
  (`engineering-practices.md:12`): the scrape run's `Progress` contract and
  the scrape page it feeds, the SCREENSHOTS list's aspect and turn, the
  #210 help bar, the achievements hash the list passes are the lanes the
  fork works in; an upstream surface's *behaviour* -- the carousel, the
  four view styles, the kid and kiosk unlock, the local HTTP API, the four
  upstream scrapers -- is read for brittleness and cost (the lens) and left
  as upstream has it, and a defect in one is still ours to close when the
  fix is contained (rule 6). The read is the pin `16dbac5211`'s bytes; M7's
  worktrees are never read.
- **One sentence on ownership, because two earlier briefs disagree.**
  `es-state-and-bridge.md:233` and `es-guimenu.md:313` call
  `GuiScraperStart.cpp` "T32's"; #678's globs (`es:es-app/src/guis/**`
  minus named exclusions) and `es-pages.md:241` give it to T31, and #679's
  globs do not reach `guis/`: **the globs decide, so `GuiScraperStart`,
  `GuiScraperRun`, `GuiGameScraper` and every page under `guis/` are
  T31's; `views/ViewController.*` is T2's (read at Extended depth, #649)
  and `scrapers/ScreenScraper.*` is T21's (#668); T32 reads its callers
  for context only** and takes `Scraper.cpp:400` (the overwrite flag the
  page sets), `ThreadedScraper` whole, and the scrapers' side of #1191 and
  #1193.
- **Two worktrees, one session, and four placeholders.** The distribution's
  `feature/m6-es-app-views-scrapers-679` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-app-views-scrapers-679`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded; and the EmulationStation fork's
  `feature/m6-es-app-views-scrapers-679` at
  `W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-views-scrapers-679`,
  cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`**
  and clean until stage E: the sources are read and the fixes are made
  there, and the pin is not moved by the lane. **`W` is that one path in
  every block of this brief; until it exists -- neither worktree does
  before dispatch -- the `qa-integration` checkout at the same pin, clean,
  stands in, read by `git -C` only, and gives the same lines (the proof ran
  every command there).** **Four placeholders stand in this brief for
  hashes that do not exist until dispatch:** `COHASH` (the coordinator's
  tip merged into the lane's branch), `MERGE_HASH` (that merge commit, the
  lane's dispatch tip), `TIPHASH` (the lane's own tip as it moves; at stage
  A it is `MERGE_HASH`) and `V2HASH` (this brief's commit on the
  coordinator's branch). The dispatch comment on #679 and the seeded
  pointer carry their values; the lane reads them there, never guesses
  them, and § 9's placeholder check names all four. **T21's ES branch
  `feature/m6-es-state-and-bridge-668` at `3ae9610b0` has already changed
  `Scraper.cpp` and `Scraper.h` and added `scrapers/ScraperReplies.{h,cpp}`
  (§ 2): the lane reads the pin for the audit and reads that tip for those
  deltas, recording each as inherited in `02`; a T32 fix that touches the
  same lines is written against the pin and the integration's merge (the
  coordinator's) reconciles; the lane names each such collision in the
  hand-back.** The other ES checkouts under
  `~/Development/emulationstation-next.worktrees/` are other lanes' and
  M7's: read with `git -C <checkout> show <hash>:<path>` only;
  `rocknix/master` is read from the shared refs, never fetched
  (`upstream/master` in that repository is a stale copy 15 commits behind,
  § 2). Until the dispatch comment exists the pointer is not seeded and
  nothing starts.
- **Depth: Independent** -- one seat from another lab (plan § 6c `:374`,
  D-WORKFLOW-137; `adversarial-council.md`: an Anthropic-led audit's
  reviewer is pinned GPT-6 Astra; no Gemini seat): Astra at `max` over a
  trimmed, scanned packet (D-WORKFLOW-195 -- the six fork-modified files
  whole, 4,005 lines, and of the 36 upstream-carried files only the ranges
  the questions cite; **`services/httplib.h` is vendored cpp-httplib, 5,713
  lines and 174,945 bytes, a third of the slice's lines: cited ranges only,
  never whole**; the manifest names every trimmed file and range), a probe
  then one refutation (one in-call retry allowed); `review-plan.json`
  records depth `independent` and the one reviewer with its served model;
  **exactly two keyed `tools/council/run invoke` calls**, every other
  `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent` (the runner
  reads that variable at `tools/council/run:21`, default
  `~/.config/council/env`; the recipe is `.claude/skills/council/SKILL.md`
  and its `references/`; the runtime under `tools/council/` from `npm
  install --offline`, no fetch). The packet is scanned before it leaves:
  **the scrapers carry developer-credential macro gates by name**
  (`GAMESDB_APIKEY` at `GamesDBJSONScraper.cpp:7`, `GamesDBJSONScraper.h:7`,
  `GamesDBJSONScraperResources.cpp:12`, `:49`,
  `GamesDBJSONScraperResources.h:7`, `Scraper.cpp:29`; `HFS_DEV_LOGIN` at
  `HfsDBScraper.cpp:1`, `:181`, `:190`, `HfsDBScraper.h:6`, `Scraper.cpp:33`;
  `SCREENSCRAPER_DEV_LOGIN` and `SCREENSCRAPER_RUNTIME_DEV_LOGIN` at
  `Scraper.cpp:25`), the IGDB client identity lives in `ensureToken`
  (`IGDBScraper.cpp:136-165`), `httplib.h` carries 42 credential-shaped
  lines of its own HTTP-auth plumbing and `UIModeController.*` 17 lines
  naming the unlock sequence -- so `packet-manifest.json` records **every
  scan hit dispositioned by file:line** (library plumbing / macro name /
  identifier / setting name / value), and a hit that is a value stops the
  packet; no value ever reaches the packet or an artifact.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the distribution worktree; `8ebaf8daad`
  is `next`'s commit the P1 branch stacks on and `651150fc88` is
  `upstream/next`'s, both copied from T31's brief and both proved today:
  `651150fc88` is *Merge pull request #3547 from spycat88/qcom-bls*,
  `8ebaf8daad` is *browser: record provider pages and GTK4 compilation
  (#616)*):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-app-views-scrapers-679
cat .github/sessions/saved-session-state-feature-m6-es-app-views-scrapers-679.md   # the pointer: the dispatch's two hashes; § 10 names the lines to check
git status --short | wc -l                                                     # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                 # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-views-scrapers-679; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                  # the pin; 0
git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10                       # cada856d86: the merge base with ROCKNIX's master (not bccd715707, § 2)
git -C "$W" rev-parse --verify rocknix/master | cut -c1-10                      # f6c542872e, read from the shared refs
git -C "$W" rev-parse --verify origin/feature/m6-es-state-and-bridge-668 | cut -c1-9   # 3ae9610b0: T21's ES tip, whose Scraper.cpp deltas § 2 names
git show origin/feature/m6-es-state-and-bridge-668:docs/audits/2026_10_26-epic-m6-es-state-and-bridge/05-punch-list.md | /usr/bin/grep -c '^## PL-'   # T21's punch list is reachable (26): PL-04, PL-17, PL-20, PL-25 are routed here
tools/register-check >/dev/null && echo register-ok
tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200             # who holds the host: no guest before a grant on #679
```

Every line above except the first `cat` ran today in the P1 clone and
`qa-integration` and printed what its comment says; the `cat` cannot run
before the pointer is seeded.

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{inventory.json,slices.json}`; the slice's `select` is one
object with one positive glob and two negative ones; `W` is the ES
worktree):

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k = [s for s in sl["slices"] if s["k"] == 32][0]; sels = k["select"] if isinstance(k["select"], list) else [k["select"]]
def expand(g):
    mm = re.search(r'\{([^{}]*)\}', g)
    if not mm: return [g]
    return [x for alt in mm.group(1).split(",") for x in expand(g[:mm.start()] + alt + g[mm.end():])]
def m(p, g): return fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2]))
def pick(sel):
    globs = sel.get("globs") or []; tiers = sel.get("tier"); areas = sel.get("areas") or [k["area"]]
    inc = [x[3:] for g in globs if g.startswith("es:") for x in expand(g)]
    exc = [x[4:] for g in globs if g.startswith("!es:") for x in expand(g)]
    return [r for r in rows if r["tree"] == "es" and r["area"] in areas and any(m(r["path"], g) for g in inc) and not any(m(r["path"], g) for g in exc) and (not tiers or r["tier"] in tiers)]
t32 = []
for sel in sels:
    for r in pick(sel):
        if r not in t32: t32.append(r)
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("selects", len(sels), "paths", len(t32), "lines", L(t32), dict(collections.Counter(r["reach"] for r in t32)), dict(collections.Counter(r["tier"] for r in t32)))
print(dict(collections.Counter(r["language"] for r in t32)))
print("fork-own lines by inventory tier:", L([r for r in t32 if r["tier"] == "fork-own"]))
os.makedirs(".qa-scratch/t32", exist_ok=True)
open(".qa-scratch/t32/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t32, key=lambda r: r["path"])))
for r in sorted(t32, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
PY
wc -l .qa-scratch/t32/paths.txt     # 42
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-views-scrapers-679; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
while IFS= read -r p; do git -C "$W" show "$PIN:$p" | wc -l; done < .qa-scratch/t32/paths.txt | awk '{s+=$1} END {print "wc -l lines", s}'           # 17306
while IFS= read -r p; do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done < .qa-scratch/t32/paths.txt | awk '{s+=$1} END {print "grep -c lines", s}'   # 17311
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t32/paths.txt | wc -l   # 42: every path exists at the merge base
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN BASE: $p"; done < .qa-scratch/t32/paths.txt | wc -l   # 42
git -C "$W" diff --numstat "$MB" "$PIN" -- $(cat .qa-scratch/t32/paths.txt) | awk '{a+=$1; r+=$2; n+=1} END {print n, "files", a, "added", r, "removed"}'   # 6 files 168 added 46 removed
git -C "$W" diff --numstat bccd715707 "$PIN" -- $(cat .qa-scratch/t32/paths.txt) | awk '{a+=$1; r+=$2; n+=1} END {print n, "files", a, "added", r, "removed"}'   # 6 files 168 added 46 removed: the same
```

Expected, at `2174265e9c` (the membership digest ran it in the P1 research
clone on 2026-10-27, and the proof ran it again there the same day with
`W` the `qa-integration` checkout at the pin: every line identical), the
block's exact output lines:

```
selects 1 paths 42 lines 17311 {'shipped': 42} {'upstream-carried': 36, 'fork-own': 6}
{'c++': 20, 'c-header': 22}
fork-own lines by inventory tier: 4005
```

then `wc -l` of the paths file **42**; `wc -l lines 17306`; `grep -c lines
17311`; the merge-base count **42** and the base count **42**; **6 files 168
added 46 removed**, twice. The 42 per-file `lines language tier` rows match
the table below in every row.

**Three things the figures hide, settled here so the lane does not
re-derive them.** (1) **The inventory counts lines as `grep -c ''` does**,
the unterminated last line included: five slice files end without a newline
(`GamesDBJSONScraperResources.cpp` 200/201, `UIModeController.cpp` 196/197,
`BasicGameListView.cpp` 226/227, `IGameListView.cpp` 48/49,
`VideoGameListView.cpp` 64/65), so `wc -l` sums to 17,306 and `grep -c ''`
to 17,311 -- the same bytes, two counting rules; a figure in `02` says
which. The same two rules reach every count in this brief: `git grep -c`
counts **lines** and `git grep -o | wc -l` counts **occurrences**, and
where the digests' totals were occurrences the lane's `grep -c` prints the
smaller number -- § 5 states both for `_("` (58 lines, 70 occurrences),
`HttpReq` (83, 95) and `exists(` (49, 50). (2) **"4,005 fork-own" is the
lines of the six files the fork touched, not the lines the fork wrote.**
The inventory's `tier` is `fork-own` for any path the fork added or
changed, and the fork added nothing here (`git diff --diff-filter=A
--name-only bccd715707 PIN -- <paths> | wc -l` = 0): every one of the 42
exists at `bccd715707`, at `cada856d86` and in `rocknix/master`. So the
read's tiers are **fork-modified 6, upstream-carried 36, fork-added 0**,
and the fork authored 168 lines and removed 46 in this slice. `02` §
Coverage carries both tiers. (3) **The merge base with ROCKNIX's master is
`cada856d86`, not `bccd715707`.** `rocknix/master` is
`f6c542872e3850c5f432929ead219547a897cd4a` (2026-10-23, *Merge pull request
#54 from porschemad911/s922x-suspend*); the pin's merge base with it is
`cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` (*Refactor wifi menu and add
support for saving multiple profiles*, authored 2026-09-23, committed
2026-09-28), one commit after `bccd715707` (`rev-list --count
bccd715707..cada856d86` = 1); `bccd715707` is the base every earlier ES
brief named because the repository's `upstream/master` ref was never
fetched and still points there, 15 commits behind `rocknix/master`
(`rev-list --count cada856d86..rocknix/master` = 14). For this slice the
difference is nothing: `cada856d86` touched `ApiSystem.{cpp,h}`,
`GuiMenu.{cpp,h}` and `GuiWifi.{cpp,h}`, none of them here (`git show
--stat cada856d86 -- <paths>` prints no file). The lane names `cada856d86`
in every merge-debt figure and records that `bccd715707` is an ancestor of
both the pin and the base.

**Merge debt: none** -- 0 of the 14 upstream commits since `cada856d86`
touch a slice path and the numstat prints nothing; the two commands and
their zeros are in § 5's runs block, and the record in `02` § The merge
debt is one line (§ 6), not a table.

**The files, read whole** (lines at the pin by `grep -c ''`, the
inventory's rule; the fork's `--numstat` against the merge base; the fork's
non-merge commits `bccd715707..PIN` on the file):

| File | Lines | +/- | Commits | What it is |
| --- | ---: | ---: | ---: | --- |
| `scrapers/Scraper.cpp` (`.h` upstream, 289) | 813 | 2/2 | 2 | the scraper registry `Scraper::scrapers` (`:24-33`; ScreenScraper's entry under `defined(SCREENSCRAPER_DEV_LOGIN) \|\| defined(SCREENSCRAPER_RUNTIME_DEV_LOGIN)` at `:25`, `c0f6fb58f`, #64), `getScraper`/`getScraperList`, `ScraperSearchHandle::update` (`:212`), `ScraperHttpRequest::update` (`:289`: the 429 retry `:343-361` with the `Retry-After` read at `:351`, the dependency chain `:317-333`, `process()`'s return discarded at `:337`, 404 and IO error ending `ASYNC_DONE` at `:372-376`), `MDResolveHandle` and `ImageDownloadHandle` (`:539` options, `:564`/`:567`, **`:596` `new HttpReq(url, mSavePath)` with no options**, `:607-614` the exhausted 429, `:618-623` the `Retry-After` read, `:631-635` 404 and IO error read as done), `downloadImageAsync`'s URL logged through `Utils::String::maskSecrets` (`:524`, `80f52e500`, #177), `resizeImage` (`:683`), the content-type table (`:646-677`), `getSaveAsPath` (`:779-809`); 25 cached `exists(` at `:88-177`, `:407`, `:440`, `:808`; the only slice file that names ScreenScraper (`:6`, `:26`); **T21's ES tip changes it (+28/-8) and `Scraper.h` (+5)**, below |
| `scrapers/ThreadedScraper.cpp` / `.h` | 339 / 119 | 56/22 / 30/4 | 1 / 1 | **the scrape run on its own threads** (`acd7a6fee`, #241, D-UI-078): the fork removed upstream's corner card, SCRAPE FAILED dialog and SCRAPING FINISHED toast and publishes a mutex-guarded static `Progress` (`h:61-73`: running, done, total, game, errors, finished, cancelled, failed, failure, elapsedMs; `progress()` at `cpp:15-22` copies it under `sProgressMutex`) that `GuiScraperRun` (T31) reads at its `:94`, `:122`, `:205`; `Process()` `:32` resets it (`:38` `running = true`); `ScraperThread::updateState` `:103-153`; `processError` `:155-175` (the seven whole-run statuses at `:157` set `failed` at `:166`, any other counts `errors`); `run()` `:177-243` polls `mExitCode` (`:179`), freezes `finished` at `:235`, logs at `:237`, then **`delete this` at `:241` and `mInstance = nullptr` at `:242` on its own thread**; `updateUI` `:248-258` (`done = total - queued - threads`, clamped at `:251`); `acceptResult` `:260-289` posts to the interface thread with a raw `FileData*`; `start` `:290-321` (the probe's `threadCount < 0` / `== 0` branches at `:297`/`:303` raise the two `_("AN ERROR OCCURRED")` boxes at `:299` and `:314`, one button each); `stop()` `:323-337` reads `mInstance` at `:325`, marks `cancelled` at `:331`, writes `thread->mExitCode` at `:335`; `isRunning()` at `h:77` reads the same pointer; `mHandle = new std::thread(...)` at `:53` and nowhere else (`h:100`); `mExitCode` a plain `int` (`h:111`), `mPaused` a plain static `bool` (`h:113`) |
| `views/gamelist/DetailedContainer.cpp` (`.h` upstream, 187) | 1450 | 21/0 | 5 | the metadata panel the detailed, video and grid views share (`getMetaComponents`, `createImageComponent`, `createVideo`, `initMDLabels`/`initMDValues`, `loadIfThemed` with `md_image` at `:464`, `loadThemedExtras`, `updateControls`, `createFolderGrid`); the fork's +21 (the #243/#245 chain, D-UI-080/081): `DisplayAspect.h`/`PlatformId.h` includes (`:2`, `:8`) and, after `BindingManager::updateBindings` in `updateControls`, `DisplayAspect::forScreenshot(file)` for a file under `PlatformIds::IMAGEVIEWER` applied by `applyToBoundImages` over `mThemeExtras` and to `mImage` (`:1057-1072`); 20 cached `exists(` occurrences on 19 lines (`:667-681` the folder's first image, `:756-771` per-game theme xml, `:817-831` the image source, `:863`, `:873` marquee, **`:903` manual or magazine, `:916` map**); 12 `_("` lines (the 12 label strings at `:112-140`, `:1010`, `:1043`), all with French |
| `views/gamelist/GridGameListView.cpp` (`.h` upstream, 65) | 347 | 14/0 | 1 | the tile grid over `ImageGridComponent` (`populateList`, `getImagePath` `:131-153`, `input`, `updateInfoPanel`, `moveToRandomGame`); the fork's +14 (`12de21757`, #243/#245): on the IMAGEVIEWER system `mGrid.setTileDecorator(...)` computes `DisplayAspect::forScreenshot(file)` per tile and sets the tile's aspect and turn (`:37-48`) plus two includes (`:2-3`); theme element `"gamegrid"` (`:229`); `reloadGameListView(this)` at `:279`, `:287`; one cached `exists` at `:208`; 0 `_("` |
| `views/gamelist/ISimpleGameListView.cpp` (`.h` upstream, 102) | 937 | 45/18 | 4 | the shared list behaviour (`input` `:256-335`, `goBack`, `moveToFolder`, `toggleFavoritesFilter`, the options and manager openers, `launchSelectedGame`, `moveToLetter`/`moveToLetterByOffset`/`getEntriesLetters` `:486-603`, `getHelpPrompts` `:681-741`, `updateThemeExtrasBindings` `:744-765`, `onAction`); the fork's +45/-18: **the help bar names SAVE STATES (HOLD) and GAME OPTIONS only where the button does it** (`7dc8bf373`, #210, `:693-739`), `DisplayAspect` on the theme's `{game:image}` extra for SCREENSHOTS (`4e4ab0647`/`12de21757`, `:755-765`), `GuiGameAchievements::show` given the `CheevosHash` (`986f1749c`, #180, `:873`); 10 lines name `ViewController` (`:4` the include, `:163` and **`:464`** `reloadGameListView` after `reloadCollection` at `:462`, `:238`, `:252`, `:308`, `:318`, `:386`, `:395`, `:427`); 2 cached `exists` (`:619`, `:910`, theme logos); 18 `_("` lines, all with French |
| the 36 upstream-carried | 13,306 | 0/0 | 0 | byte-identical to the merge base **and to `rocknix/master` today**; the four upstream scrapers `ArcadeDBJSONScraper.{cpp,h}` 243/46 (plain `http://adb.arcadeitalia.net`, `:29`), `GamesDBJSONScraper.{cpp,h}` 633/51 and `GamesDBJSONScraperResources.{cpp,h}` 201/45 (the whole of each under `GAMESDB_APIKEY`), `HfsDBScraper.{cpp,h}` 633/66 (under `HFS_DEV_LOGIN`), `IGDBScraper.{cpp,h}` 349/62 (no build macro; the player's own client id and secret from `Settings`, D-QA-003, #274), `Scraper.h` 289; the services `HttpApi.{cpp,h}` 344/35 (JSON for the embedded server; `ImportFromJson` `:170`, `ImportMedia` `:210-260` writing media and metadata on the pool thread, `:258` the in-place `writeAllText`), `HttpServerThread.{cpp,h}` 834/30 (`mThread = new std::thread` `:74`; `isAllowed` `:127-138`; `getMimeType` `:114`; **16 distinct paths over 27 `Get`/`Post`/`Delete` registrations at `:149-803`** (the registration lines `149 157 167 219 244 252 260 268 276 284 299 323 353 370 407 456 491 514 533 545 562 577 599 632 711 786 803`), `listen` on `127.0.0.1` or `0.0.0.0` under `PublicWebAccess` at `:821-828`, port 1234, plain HTTP; **`:574` `mWindow->displayNotificationMessage(req.body)` on the pool thread**; the delete route `:738-755`; 10 `ViewController` lines), `httplib.h` 5,713 (vendored; `Server` `:590`, `Client` `:716`, `ThreadPool` `:447`; 9 `std::thread`; the slice's four TODOs; no version line, Q7); the views `SystemView.{cpp,h}` 1638/142 (the carousel: `populate` `:196`, `_moveCursorInRange` `:272` a static pure function, `moveCursorFast` `:282-331`, `input` `:376-515`, **`:233-234` the untranslated sentence-case dialog with a bare `"OK"`**, `:348` `reloadGameListView` after a text filter, `:552` the computed-title `GuiSettings` page (#965), `:1616` `RetroachievementsMenuitem`; 18 `_("` lines, one with an empty French `msgstr`, po L115/L116), `SystemViewControlWrapper.h` 184, `UIModeController.{cpp,h}` 197/63 (full/basic/kid/kiosk; the unlock sequence `listen()` `:55-97`, a wrong press resetting it at `:72`; `UIMode = Full` and `saveFile()` at `:102-103`), `BasicGameListView.{cpp,h}` 227/49 (`recurseFind` `:101-124`; `reloadGameListView(this)` `:54`, `:182`), `CarouselGameListView.{cpp,h}` 207/52 (`:61`, `:171`), `DetailedGameListView.{cpp,h}` 66/38, `VideoGameListView.{cpp,h}` 65/39, `GameNameFormatter.{cpp,h}` 269/36 (`getDisplayName` `:121`; the sort-id test at `:84-85`; the play-time format `:171-185`, `atol` at `:171`), `IGameListView.{cpp,h}` 49/57 (included by 9 files outside the slice) -- read for brittleness and cost, left as upstream has them (D-UI-079), a contained defect still closed (rule 6) |

**The views this slice draws** (the digest's table; `getName()` returns
`mCustomThemeName` first when set): `BasicGameListView` (`"basic"`,
`h:31`; element `"gamelist"`, `cpp:44`), `DetailedGameListView`
(`"detailed"`, `h:24`; the container's `md_*`), `VideoGameListView`
(`"video"`, `h:26`), `GridGameListView` (`"grid"`, `h:36`; `"gamegrid"`),
`CarouselGameListView` (`"gamecarousel"`, `h:32`), and `SystemView` (the
system carousel). The choice is `ViewController.cpp:704-806` (T2's file:
`Settings "GamelistViewStyle"`, read at `:712`, or the system's own mode,
gated by `theme->hasView("video"|"grid")`); **the row that writes the
global key is GAMELIST VIEW STYLE on the THEME CONFIGURATION page**
(`GuiMenu.cpp:8668` the page, `:8691` the `OptionListComponent`, `:8729`
the `addWithLabel`; its values at `:8685-8735` are `automatic`, `basic`,
`detailed`, `video`, `grid`, `gamecarousel`; T26's file), **and per list it
is SELECT > VIEW OPTIONS > GAMELIST VIEW STYLE** (`GuiGamelistOptions.cpp:194`/`:232`,
T31's; that file writes the system's own mode and has 0 hits for
`GamelistViewStyle`). The hop from USER INTERFACE SETTINGS to THEME
CONFIGURATION the lane reads on the guest (the map's `:135` names
APPEARANCE, not THEME CONFIGURATION; L-15). Every `.cpp` under `views/`
and `services/` includes `views/ViewController.h`, and T21's
`ViewController.cpp` includes seven slice headers back: one include cycle,
taken as given, not as a finding.

**What the digests checked and found sound, so the lane confirms rather
than hunts:** no `system(`, `popen(` or `runSystemCommand` in any of the 42
files (`git grep -n -E '\b(system|popen)\s*\('` prints nothing); no
`.detach(`; 0 non-ASCII `//` comments across the 42 (and 0 in T31's
`GuiScraperRun.cpp`); the four TODO/FIXME/XXX lines are the vendor's
(`httplib.h:2863`, `:3170`, `:3885`, `:4312`); no store is written from
`scrapers/` or `services/` (the `Settings::...->set|SystemConf::...->set|saveFile`
grep hits nothing there); `UIModeController.cpp:102-103` writes `UIMode` to
the ES store with `saveFile()`, the right store for an ES-only mode; the
scrape page's cancel dialog (T31's `GuiScraperRun.cpp:112-116`) is YES
then NO, back lands on NO; `HttpServerThread.cpp:754`'s cached `exists`
sits before a `removeFile`, so a remembered miss skips a delete (the safe
direction); `isAllowed` refuses every remote but `127.0.0.1` unless
`PublicWebAccess` and the routes call it; the 51 distinct msgids across the
42 files every one have a `msgid` line in
`locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the pin, one with an
empty `msgstr` (the msgid at po L115, `SystemView.cpp`'s ERROR: EVERY
SYSTEM IS HIDDEN ..., and the empty `msgstr ""` at L116); the fork added no
new `_("` msgid in this slice (the help-bar change re-arranges existing
strings; `ThreadedScraper.cpp` *removes* four, the last reused at
`GuiScraperRun.cpp:232`).

**What they found instead -- the leads, one line each.** § 4 carries each
at its lines with what proves it and its disposition, and tables the
floor's 3.1 to 3.35 beside them; the lines here are the pin's, three of
them corrected against the digests by the drafter's reads (`delete this`
at `:241`, not `:253-254`; `HasMember` at `GamesDBJSONScraper.cpp:607`,
not `:606`; `IGDBScraper.cpp:143` an `if`, not an unconditional return)
and four more by the proof (`h:77`, `:299`/`:314`, `:640`, `:167-172`):

| Lead | Lines at the pin | Shape | Q |
| --- | --- | --- | --- |
| L-01 | `ThreadedScraper.cpp:325`/`:335` against `:241-242`; `isRunning()` `h:77` | `stop()` reads and writes through `mInstance` under no lock while `run()` may be at `delete this` | Q1 |
| L-02 | `ThreadedScraper.cpp:331` with `GuiScraperRun.cpp:140-141` | a `stop()` between `:235` and `:242`, or `main.cpp:1332`'s at exit, marks a finished run cancelled: SKIPPED - YOU CANCELLED IT over a completed run | Q1 |
| L-03 | `ThreadedScraper.cpp:53`, `h:100`, `h:111`, `h:113` | the scrape thread never joined, detached or deleted; `mExitCode` and `mPaused` cross threads as plain variables | Q1 |
| L-04 | `ThreadedScraper.cpp:299`, `:314` | the two `_("AN ERROR OCCURRED") + " :\r\n" +` one-button boxes on the fork's start path | Q5 |
| L-05 | `GuiScraperRun.cpp:225` <- `ThreadedScraper.cpp:166` <- `Scraper.cpp:640` | the page's line 4 carries `removeHtmlTags(getErrorMsg())`, curl's or the server's words, for every scraper but ScreenScraper | Q5 |
| L-06 | `Scraper.cpp:596`, `GamesDBJSONScraperResources.cpp:153` (no options); `HfsDBScraper.cpp:179`, `:287`, `IGDBScraper.cpp:146`, `:189`, `:205`, `:215`, `Scraper.cpp:539` (headers only) | no `timeout` or `stallTimeout` anywhere in the slice: `HttpReq.cpp:204`'s 10 s connect and no total or stall bound, #299's quarter of an hour under a page whose only exit is CANCEL | Q2 |
| L-07 | `Scraper.cpp:607-614`, `:631-635` | a 429 whose retries are spent, a 404 and an IO error on a media download read as done: no file, the result accepted and stamped, the page COMPLETED (#1191's caller half) | Q3 |
| L-08 | `DetailedContainer.cpp:903`, `:916` (and `:817-831`, `:863`, `:873`) | a row decided from a file the scraper (`Scraper.cpp:683`) and the API (`HttpApi.cpp:258`) write while the list is open; a remembered miss hides it until a launch | Q4 |
| L-09 | `Scraper.cpp:88-177`, `:407`, `:440` | what to fetch and what to overwrite decided from the same cache | Q4 |
| L-10 | po L218 against L233 | the French of `SAVE STATES (HOLD)` is `SAUVEGARDES (MAINTENU)`, a game save; L233's `SAVE STATES` is `SAUVEGARDES D’ÉTAT` | Q5 |
| L-11 | `SystemView.cpp:233-234` | an untranslated sentence-case dialog with a bare `"OK"`, after `:233` writes `UIMode` without `saveFile()` | Q5 |
| L-12 | `HttpServerThread.cpp:574` | the request body as a toast from the pool thread, unbounded, where every other route posts to the interface thread (`:229`, `:443`, `:479`, `:539`, `:559`, `:592`, `:623`, `:698`, `:702`, `:776`) | Q5, Q1 |
| L-13 | `HttpServerThread.cpp:738`, `:751-755`; `HttpApi.cpp:258-260` | files removed and media written on the pool thread while the interface thread reads the same `FileData` | Q1 |
| L-14 | `GridGameListView.cpp:38-48` with `DisplayAspect.cpp:99-131` | one capture record read per tile on the interface thread at populate: N reads before the SCREENSHOTS list's first frame | Q6 |
| L-15 | `docs/es-menu-map.md:135`, the one grep hit | no row for the view styles, the row that picks them or the SCREENSHOTS list; the views carry no screen title, so the checker cannot see them; `SystemView.cpp:552`'s computed title is #965's | Q7 |
| L-16 | `ISimpleGameListView.cpp:462-464` | `reloadCollection` then `reloadGameListView`, #246's shape if the collection reload frees the view's cursor first | Q1 |
| L-17 | § 5's two delta commands | merge debt none | Q7 |

**The harness that exists: none.** `git grep -l -E '\b<basename>\b' PIN --
es-app/tests tests CMakeLists.txt es-app/CMakeLists.txt es-core/CMakeLists.txt
es-app/tests/unit/CMakeLists.txt` for every slice basename hits only
`es-app/CMakeLists.txt` (the product binary's source list); no test file,
no test CMakeLists and none of the 15 Python harnesses under `tests/` names
a slice file at the pin; `es-app/tests/unit/CMakeLists.txt` links
`es-unit-tests` from 16 test files and 12 shipped sources, none in the
slice; `tests/app-unit/` compiles `ProxyCards`, `CloudTransferJob`,
`OfflineScanJob`, `SaveStateBookkeeper` against its `fakes/` (a `FileData`
double at `fakes/FileData.h:4`; no `SystemData` double). In the
coordinator worktree `GameListView`, `HfsDB`, `TheGamesDB`, `ArcadeDB` and
`views/` hit nothing under `tools/`, `docs/es-menu-map.md` or
`tools/vm-walks/`; the `scraper` hits (`qa-accounts`,
`pixelelated-state-check`, `last-good-scripts-test`) are the ScreenScraper
account state, excluded here. **`manager.steps` is the only walk that
enters a game list** (its `0-carousel` and `1-list` shots are `SystemView`
and a game list; `claims.txt:38-39` carries `manager-gb/01-0-carousel.png`
and `02-1-list.png` at `d72084ccad` **at 1280x800** -- the rows read `0 0
1280 800` -- so no 640x480 list baseline exists, which is #1141's point,
and the one 640x480 frame of a list on record is #210's bar,
`vm-qa-log:107`); no step file scrolls a list, opens SCRAPER or runs a
scrape; `tools/vm-qa:63`'s suites touch the slice only through
`walks`/`frame-diff`. The one host compile precedent is
`scrapers/Scraper.cpp` syntax-only, rc 0 three times on T21's edited tree
under its stand-in headers
(`docs/audits/2026_10_26-epic-m6-es-state-and-bridge/stage-e/syntax-check.sh`
on `origin/feature/m6-es-state-and-bridge-668`; `s12-after.txt:16-17`,
`s13-after.txt:12-13`, `s14-after.txt:14-15`); 13 of the other 19 `.cpp`
include `Window.h` or `views/ViewController.h` (SDL through
`InputConfig.h` by the includes), two bring vlc with no stand-in, and
`GameNameFormatter.cpp` brings neither; **the one error measured in this
slice is curl**: plain `g++ -fsyntax-only` on `ThreadedScraper.cpp` at the
pin stops at `es-core/src/HttpReq.h:5:10: fatal error: curl/curl.h: No
such file or directory`, rc 1 (§ 5). The prior guest evidence that touches
the slice is six `docs/vm-qa-log.md` rows (`:72-74`, `:106`, `:107`,
`:111`, `:114`, `:116`: the ScreenScraper refusal dialog raised through
`ThreadedScraper::start`, #67's remembered systems, #210's bar measured at
640x480, #241's CANCEL outcome, #243's `game-artwork` extra, #246's crash
under the soak with `POST /launch`).

**The neighbours, and whose they are:** `ViewController.*` is **T2's**
(#649); `ScreenScraper.*`, `HttpReq`, `FileSystemUtil.cpp`'s cache,
`AtomicFileUtil`, `ApiSystem`'s executors and `Settings`/`SystemConf` are
**T21's** (#668); every page under `guis/` -- `GuiScraperStart`,
`GuiScraperRun`, `GuiGameScraper`, `GuiGamelistOptions`, `GuiGameOptions`
-- is **T31's** (#678, dispatched today); `GuiMenu.*` is **T26's** (#673);
`ThreadedHasher` and the achievements pages are **T20's** (#667); the cloud
pages **T18's** (#665); `FileData`, `SystemData`, `CollectionSystemManager`,
`main.cpp`, `DisplayAspect.cpp` are **T33's by the earlier briefs' reading**
(the coordinator confirms the owner at the pause before any line outside
the 42 is touched); the es-core components (`ImageGridComponent`,
`GridTileComponent`, `TextListComponent`, `CarouselComponent`,
`GuiMsgBox`) are **T35's** by the same reading.

**Already found; do not re-find; take up** (each cited at its lines in
`02`, with a disposition): **#1191** (T21 PL-04, open): the es-core half --
`HttpReq.cpp:344`/`:328`'s removal of the file it will replace and
`renameFile` -- is fixed on T21's ES branch at `f7c16144d`, which touches
no file under `scrapers/` (its stat: `es-core/src/HttpReq.cpp` 9/19,
`FileSystemTests.cpp` 177/0, a CMakeLists 22/0); **the caller half at
`Scraper.cpp:400` and `:631-635` is this slice's**: whether a failed
download still reads as a scraped game after S4, and the stream to close
it. **#1205** (PL-17, open): fixed on T21's ES branch at `44d3c7e25`
(`Scraper.cpp` +7/-2, the new `scrapers/ScraperReplies.{h,cpp}` and
`es-app/tests/unit/ScraperRepliesTests.cpp`: `threadCount(body)` and
`retryAfterSeconds(value, now, fallback)`, so both `Retry-After` reads go
through one function with `OVERQUOTA_RETRY_DELAY` as the fallback), "stays
open until the pin moves on `next`". **At the pin those reads are `:351`
(the search request's) and `:618` (the media download's); `:356` and
`:628`, which T21's `s13-checks.txt:98` names, are its branch's lines after
the +28/-8** -- T32 reads the pin's `:618-623` and `:351-355`, records the
fix as inherited, and writes no second one. **#1154 / D-NET-017** (PL-25,
open): fixed on T21's branch at `3ae9610b0` (`Scraper.cpp` +13/-4,
`Scraper.h` +5: the media downloads' verify opt-out as an explicit
`HttpReqOptions` field that survives the 429 retry at `:596`); the guest
half "scrapers with verification on" is `CANNOT` on a no-NIC guest and
#156's shim, recorded. The three commits on `Scraper.cpp` sum to the
+28/-8 (`44d3c7e25` 7/2, `e38dcdefd` 8/2, `3ae9610b0` 13/4). **S12** (ES
`e38dcdefd`, #1206): `Scraper.cpp:372` and `:631` skip the two new status
classes exactly as they skipped `REQ_IO_ERROR`, a contained edit in this
slice's file, accepted by T21's erratum -- inherited, read at both refs.
**Backlog #1186**: `services/HttpApi.cpp:258`'s in-place `writeAllText`
(the `fopen "wb"` is `FileSystemUtil.cpp:1434`, T21's) is one of the seven
writers the Backlog owns; T32 records the site and its reader, and the
stream question (this slice's fix or the Backlog's) goes to the pause.
**#965**: `SystemView.cpp:552`'s computed-title page, to map or to declare
with the reason. **T20's routed read**: `SystemView.cpp:1616` reads
`RetroachievementsMenuitem` beside `GuiMenu.cpp:190`/`:5760` -- read here,
since T26's `02` has no line on it. **#1187/#1192** (T21 L-01, PL-02):
the `.7z` hash through `sh` is `ScreenScraper.cpp:306-308` ->
`ApiSystem::getMD5` (fixed `13a688804`, outside T32); `ThreadedScraper`
is the thread it runs on, as root -- a Q1 row citing it, not re-found.
**T2's #774, #780, #789, #791** on `ViewController` are context: #774's
fix `3fee0df8a` carries the launch's game by name; the API side (does
`/reloadgames` wait for idle?) is not in its stat and is Q2's; #791 (one
ES upstream sync per cycle) carries batocera's `308221458`, which changes
`launch`'s signature for the six view callers (`es-launch-path.md:295-297`)
-- read against the pin's signature only. **T20's L-19/#300** (the
hasher's fetch on the interface thread, up to ~40 s with the link gone)
and **L-21** (fixed `698040b5c`): the callers' side only (`reloadAll`, the
API's `/reloadgames`). **#246 / D-UI-113** (`es-code-traps.md:191`): the
halves `dropGameListView` / `remakeGameListView` are `ViewController`'s
and T2 read them as implemented; the holders -- the views' cursor,
`mCurrentView`, the collections -- are this slice's to list (T18's
`02:223`). **#243 / D-UI-080/081** (`es-code-traps.md:164`): shipped; the
views carry the hook. **T18's control count** (`02:329`): `Scraper.cpp`'s
25 cached `exists()` calls, unexamined there, examined here (Q4). **T26's
inheritance** (`02:824-833`): the readers' rule, a file another process
writes is read uncached, `isRegularFile` included; one quoting function;
`GetShOutputLines` not `GetShOutput`. **T31's `02` § What T32 to T37
inherit** is owed and not written at this version: read at dispatch if it
has landed, else mid-run when it does (its brief's `:768-773` says what it
carries: the provenance table, the dialog method, the title-shape table,
the cached-read table's writers, the four tab-strip pages); the scrape
page `GuiScraperRun` whose line 4 this slice's words reach is T31's.
**#66** (closed): the probe order and the English status sentences
(`ScreenScraper.cpp`, T21's); `ThreadedScraper.cpp:290-321` is where the
refusal dialog is raised. **#67** (closed, T31 re-reads it). **Backlog
#1190**: no scraper walk, suite row or `claims.txt` baseline exists -- the
window plan's G-05 is the first scrape walk, kept under the audit folder,
not `tools/`. **#1141**: `vm-pair` cannot start a 640x480 guest; a walk
that lands in a game list view at 640x480 is this slice's surface and the
single guest's.

## 3. Read first

In this order, each read in this session, and `01-research-notes.md` says
which were read (`working-principles.md` § Pre-flight):

1. **The rules**, each at the section named, with the question it serves;
   the section's own sentence is not repeated here -- open it (the proof
   read every line below as the heading or sentence it names):

   | Rule | Line | Section | Serves |
   | --- | ---: | --- | --- |
   | `es-code-traps.md` | `:22` | Never rebuild a button bar from inside one of its buttons | Q1 |
   | | `:60` | Comments near a translatable string must be ASCII | Q5, § 9 |
   | | `:79` | The help bar offers a direction only where it moves something | Q5 (the two `getHelpPrompts()`) |
   | | `:104` | Three things a font is not, third bullet: `exists` caches for the session; pass `false` for what changes while ES runs | Q4 (the 50 cached reads) |
   | | `:139` | Pure text has a home, and a test | § 5 (every unit case's shape) |
   | | `:164` | The picture beside a game list is the theme's own extra, not md_image | Q6 (#243: the extras after `updateBindings`; check the theme first) |
   | | `:191` | A rescan that deletes FileData drops the view first | Q1, Q6 (#246: list who holds a pointer) |
   | | `:212` | A file under three bytes reads as empty | Q6 (`DisplayAspect`'s records) |
   | | `:224` | curl hands a header callback a length, not a string | Q2 (`HttpReq`, T21's; every scraper consumes it) |
   | | `:238` | A pooled connection with the link gone is silent for a quarter of an hour | Q2 (#299; the shape of L-06) |
   | | `:266` | A taller GuiSettings menu keeps its old top offset | Q7 (`SystemView.cpp:552`'s page) |
   | `es-native-ui.md` | `:32` | The other files that carry the interface law (D-UI-039) | Q7 |
   | | `:81` | Core patterns: a file another process writes is read uncached; the gates; `isFullUI` | Q4, Q7 |
   | | `:121` | Tabbed pages | Q7 |
   | | `:144` | The cards at the link's return: the hasher after UPDATE GAMELISTS | Q2 (`/reloadgames` starts it) |
   | | `:175` | Spacing: the four surface tiers; D-UI-078 (the scraper included); D-UI-079 | Q1, Q5 (the scrape page; the toast) |
   | | `:324` | A layout must not be computed from what it last produced | Q6 |
   | | `:342` | Code conventions: `getHelpPrompts()` kept accurate; theme-aware colours | Q5 |
   | | `:377` | Anti-patterns: two surfaces for one event; a transient-only report | Q1, Q5 |
   | | `:405` | Before the pin moves, the compiler has seen the edit (`tools/es-syntax-check`, exit 2 here) | § 5, § 9 |
   | `es-player-text.md` | `:29` | Conventions: game save vs save state; a card's title and line; the one-line toast | Q5 (L-10, L-12) |
   | | `:141` | Every fork string ships in English and French | Q5, § 9 |
   | | `:170` | A row that leads somewhere is a label, not a paragraph | Q5 |
   | | `:211` | Outcome words, and the register they are written in | Q5 |
   | | `:236` | Outcome vocabulary: COMPLETED / COULDN'T FINISH / SKIPPED | Q3, Q5 (the scrape page's line 4) |
   | `es-ui-style-guide.md` | `:32` | Keep the flow and its visual evidence together | § 5, § 7 |
   | | `:68` | Rows | Q7 |
   | | `:169` | Confirmations: YES first; back lands on NO or OK, else on the last button | Q5 (L-04, L-11) |
   | | `:268` | Gating: kid and kiosk behind `isFullUI`; network round-trips behind an action | Q7 |
   | | `:296` | Interaction rules: SELECT opens the context menu; buttons by position | Q5, Q6 |
   | `engineering-practices.md` | `:12` | Change stays inside the fork's lanes (D-UI-079) | every Q |
   | | `:28` | Check upstream early (the 36 are `rocknix/master`'s bytes: the check is of batocera's tree) | Q7, § 2 |
   | | `:83` | Verify design intent (`git log -S` before each FAIL-at-pin lead) | § 4, § 5 |
   | | `:111` | Verify the artifact, not the report | Q3 |
   | | `:194`, `:250` | A name is not a behaviour; a total is the tool's line, never a sum made in the head | § 5 (every count) |
   | | `:419`, `:464`, `:478`, `:548` | Guards must fail closed; prove the guard fires and check the stub against the unfixed code first; `rc=$?` on its own line; the first PASS of anything new is the one to distrust | Q3, § 5 |
   | | `:576` | Before deleting a duplicate, diff its behaviours (blindspot 23) | § 4 |
   | | `:799` | Fail gracefully: do what you can, keep the last good state, say how to recover (D-CLOUD-077) | Q2 |
   | `bugs-are-agent-first.md` | `:41`, `:53`, `:76` | The three classes; The rules; rule 6 | every bug |
   | `issue-tracking.md` | `:129`, `:180` | A criterion is agent-first (D-QA-044); Ticking an acceptance criterion | § 7 |
   | `generic-x64-vm-testing.md` | `:100`, `:108`, `:215`, `:224` | Headless: `run --headless --daemonize`, `tools/vm-serial`, the pidfile; `--res 640x480` (#1141); cutting the link with `ip link set eth0 down` | § 5 |
   | | `:325` | A launch, a START or a walk waits for the interface to be idle (D-QA-057: `GET /isIdle`) | Q2 (this slice's `HttpApi`) |
   | | `:383-388`, `:486-488` | a restarted ES comes back on the last list, not the carousel; `dismiss-dialogs` ends on the carousel where it was | § 5 (G-06, G-09) |
   | | `:556` | the cloud tier's fixtures: a host process on a fixed port, reached at `10.0.2.2` | § 5 (the shape a scraper stub would copy) |
   | | `:959`, `:1432` | `tools/vm-visual-qa`; the guest is the candidate image, not the read tree -- compare the file before trusting the verdict | § 5 (every frame's side) |
   | `device-builds.md` | § Build credentials | the four macros; "without them the matching scraper is not built -- except ScreenScraper on fork builds" (#64); D-WORKFLOW-166; never a personal credential as the developer default | Q7 |
   | `player-language.md`, `least-surprise.md`, `time-to-play.md` | whole | | Q5, Q6, § 6 |

2. **The register.** The rows that name a file or behaviour here (all on
   the coordinator's branch; D-WORKFLOW-188 is the P1 branch's): **D-QA-003**
   (fork builds without ScreenScraper and TheGamesDB; a scraper compiles
   only with its credential in the build environment; IGDB and ArcadeDB
   remain), D-QA-004, **D-QA-005** (the ScreenScraper pair at runtime,
   #64), D-QA-006, **D-WORKFLOW-166** (#566: the shared JELOS identity;
   #586 replacement credentials), D-UI-021, **D-CLOUD-038** (a sync gates
   launch "similar to how when the scraper is running you can't update
   gamelists"), D-CLOUD-048/049 (`gamelist.xml` is game content, what the
   scraper writes), **D-UI-034** (the help bar), **D-UI-078** (long work on
   a foreground page with CANCEL; the scraper included) and **D-UI-079**
   (the lanes; the game index keeps its card), **D-UI-080/081** (the
   aspect and the turn, wherever the interface draws them), D-UI-092,
   **D-UI-113** (#246's companion: the rescan merges), D-RA-013/035/036,
   **D-QA-057** (`/isIdle`), D-WORKFLOW-017 (#156's halves hold no build),
   D-WORKFLOW-192 (the netplay seam on the launch line the views start),
   **D-NET-017** (the peer verified by default; the scrapers' media
   downloads the one opt-out), D-QA-050 (#274: the IGDB client secret
   stripped from settings backups), D-UI-028/030 (the outcome words),
   D-UI-039, D-UI-042/045, D-UI-051, D-WORKFLOW-144, D-WORKFLOW-155/156,
   D-WORKFLOW-164/165, D-WORKFLOW-187/189/195. The highest decided IDs are
   § 9's; the lane reads the scrape and view rows by `tools/archaeology
   'scraper'`, `'game list'` and `'carousel'` before calling anything
   pending.
3. **The menu map** (`docs/es-menu-map.md`, 989 lines): `## Two ways in`
   `:83` (the SELECT row at `:90`: QUICK ACCESS on the system view, VIEW
   OPTIONS on a game list -- the only row the map gives the views' own
   surface), `## Main menu` `:95` (`:112` FULL --> SCRAPER; `:116`, `:121-124`
   the kid and kiosk collapse, `UIModeController`'s modes), `:135` USER
   INTERFACE with GAMELIST OPTIONS (and APPEARANCE, not THEME
   CONFIGURATION), `:139` SCRAPER tabbed, `:642-644` the ACCOUNTS tab's
   DEVELOPER rows, **D-UI-039 at `:668`**, **`## Not mapped` `:677`** (the
   rule at `:683-685`; `:701` SCREENSCRAPER; `:704` ADD TO CUSTOM
   COLLECTION...), `## ScreenScraper developer provisioning (#566)` `:911`
   (its frame index at
   `docs/qa-logs/2026-10-14-screenscraper-ui-runtime/frame-index.json`),
   and the visual-evidence section `:26-82` (the baseline `d72084ccad`;
   the `evidence-index.json` schema). **No section names the five view
   styles, the row that picks them, or the SCREENSHOTS list** (Q7).
4. **The blindspots** naming this slice's shapes: 3 (`GetShOutput`'s
   line-join), 4 (`close()` inside a page's own handler -- #246's cursor is
   the same shape), 8 (an assertion that holds because nothing had
   happened yet), 13 (assumed done), 22 (a probe that cannot report
   absence -- `Scraper.cpp:372` reads an unreachable scraper as "nothing
   found"), **44** (`MultiLineMenuEntry` measured from the cells it set
   last time; a row refreshed per game of a scan), 49 (an edit made blind
   to the compiler), **62** (a fix corrected the writer and left what it
   had written: `Already written:` on every bug), **64** (a wait lengthened
   for an event the code had no path to produce: the hasher's offline path
   -- the scrapers' unbounded requests are the sibling), **75** (a corpus
   read on the wrong tree: every count at the hash).
5. **The tests at the pin.** The sweep in § 5 (`git -C "$W" grep -l -w
   <class> "$PIN" -- es-app/tests tests` for every slice basename): zero
   hits. The shapes a case is written in, read whole before one is
   written: `es-app/tests/unit/README.md` and `CMakeLists.txt` (`:37-64`:
   the 16 test files and 12 shipped sources `es-unit-tests` links),
   `es-app/tests/unit/fakes/SDL_timer.h` (the clock fake
   `ScraperHttpRequest::update`'s cases need), `tests/app-unit/CMakeLists.txt`
   `:50-101` and its `fakes/` (`FileData.h:4`, `Window.h`, `utils/FileSystemUtil.h`:
   the doubles the views' and the API's cases reuse); on T21's ES branch
   `3ae9610b0`, `scrapers/ScraperReplies.{h,cpp}` and
   `es-app/tests/unit/ScraperRepliesTests.cpp` (target `es-scraper-tests`,
   its `CMakeLists.txt:184`: the model -- validity beside the value, so an
   answer that is not one is a failure, never a number; the ES tree also
   has a top-level `tests/`, so the full path matters); `CloudTextTests.cpp`
   and `DisplayAspectTextTests.cpp` as the nearest doctest files.
6. **The walks and the frames.** `tools/vm-walks/manager.steps` (33 lines:
   carousel, X to the list, shots `0-carousel` and `1-list` at its steps
   10-14) and `README.md:23-32` (the step vocabulary); `suite.txt:98-100`
   (the three `manager-*` compositions setting `StartupSystem`);
   `claims.txt:38-39` (the two baseline frames at `d72084ccad`, 1280x800);
   `reset.steps:6-8`' note on the GO TO dialog a walk must not be left
   holding (#85); `docs/qa-logs/2026-10-14-screenscraper-ui-runtime` (35
   png under its subfolders and the index, the scrape page's frames).
7. **The French**: 58 `_("` lines in 9 of the 42 files; 51 distinct
   msgids, every one in the catalog at the pin; L115's msgid with L116's
   empty `msgstr`; L218 against L233 (Q5); `tools/es-untranslated` is the
   count, both lines known (`706 ... 706 with French, 0 without` against
   `bccd715707`, `703 ... 703 with French, 0 without` against
   `cada856d86`, § 5).
8. **The audits**: T21's `02-forward-audit.md` `:23` (§ Coverage, the probe
   without bounds), `:40` (L-01), `:145-154` (the credentials' paths),
   `:401` (§ The commands), `:543-553` (§ What T26 and the OS slices
   inherit), its `04:173`, its `05` PL-04 `:81-100`, PL-17 `:332-351`,
   PL-20 `:393`, PL-25 `:479-496`, and `stage-e/s13-checks.txt:96-98` (all
   on `origin/feature/m6-es-state-and-bridge-668`; `:98`'s `:356`/`:628`
   are that branch's lines); T2's `02-forward-audit.md:114-124` (group 1,
   `ViewController`: VC-5 `reloadAll`'s race `:1248-1267` and
   `reloadAllGames`' unchecked `getSelectedSystem()` `:1437`, recorded
   only; the view-type selection's cost `:700-846`), `:352` (§ Coverage
   Boundary, `HttpServerThread.cpp:615-630`), `04:661`, `05` PL-008
   `:157-172`, PL-023 `:400-415`, PL-033 `:549-562`, `:607-619` (on
   `origin/feature/m6-es-launch-path-649`); T18's `02:223` and `:329` (on
   `origin/feature/m6-es-cloud-pages-665`); T20's `02:147-168` and `:321`
   (on `origin/feature/m6-es-achievements-pages-667`); T26's `02:824-833`
   (on `origin/feature/m6-es-guimenu-673`); T31's `02` § What T32 to T37
   inherit when it lands.
9. **The issues**: #1191, #1205, #1154, #1206, #1186, #1187, #1192, #1193,
   #965, #1190, #156, #774, #780, #789, #791, #300, #299, #246, #243, #245,
   #241, #210, #180, #177, #66, #67, #64, #566, #585, #951, #1137, #1141,
   #1183, #700, #678; #679's own body. States read 2026-10-27: #1191,
   #1205, #1154, #1206 (`Bug: EmulationStation: two sentences that are not
   true (T21 PL-18)`), #1186, #1187, #1192, #1193, #965, #1190, #1141,
   #1137, #1138, #64, #180, #156, #791, #774, #780, #789, #951, #1183,
   #1135 and #585 (`Standing: Queue upstream contributions after the
   initial build`) OPEN; #246, #243, #245, #241, #210, #177, #66, #67,
   #566, #274, #300 and #299 CLOSED; #649, #665, #667, #668, #673 OPEN
   until the integration merge (§ 1).
10. **Time to play**: `docs/vm-qa-log.md:9-18` (the three headline columns:
    the press on a game to its first frame; `execute_kill` to the exit
    sync's stamp; `execute_kill` to the next game's first frame; "no budget
    row exists yet"); `time-to-play.md`'s one budget (the exit sync's 3 s,
    D-CLOUD-119). This slice sits on the launch path at three points: the
    list's `launchSelectedGame` (every view's press to `ViewController::launch`),
    the game list's populate (the per-tile record reads on SCREENSHOTS in
    grid style, `GridGameListView.cpp:38-48`), and the carousel's
    `SystemView::populate` after UPDATE GAMELISTS -- the retro's line names
    them with what they cost on the guest, never "nothing".

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of the families the earlier ES briefs
used -- **a lifetime or a thread**, **a call with no bound**, **a check
whose failure reads as success**, **a read of a file another process
writes**, **a player sentence outside the vocabulary**, **work on the
interface thread the lens prices**, **a page the map does not describe
and the checker cannot see** -- with the lens, cost against value, asked
of every upstream surface: what it costs the player (a wait, a read, a
thread) against what it gives. The leads are § 2's L-01 to L-17 and the
floor's 3.1 to 3.35, tabled at the end of this section; each is read at
its lines before it is called anything, and the six that FAIL at the pin
(§ 5) get their `git log -S` first (`engineering-practices.md:83`).

- **Q1 Lifetimes and threads** (`es-code-traps.md:22`, `:191`;
  `es-native-ui.md:175`; `engineering-practices.md:419`; the threads and
  lifetime runs). **L-01**: `stop()` and `isRunning()` (`h:77`) read
  `mInstance` and write `thread->mExitCode` under no lock while `run()` may
  be deleting `this` on its thread -- proved by reading (`mInstance` on 9
  lines of the `.cpp`: `:9`, `:76`, `:242`, `:292`, `:306`, `:310`,
  `:315-316`, `:325`); a unit case cannot reach it and the guest cannot
  make the window reliably, so the disposition is a read trace and a
  contained fix (detach at `:53`; atomics for `mExitCode` and `mPaused`;
  the null-check under the mutex) under rule 6. **L-03**: the same
  pointer's owner. **L-02**: a unit case on `progress()`'s shape with
  `cancelled && finished && done == total`, seen to FAIL at the pin, the
  fix `if (!sProgress.finished)` around `:331` (fork's own). **L-13**:
  bounded to the system's own `fileMap`, `:443` then posts
  `onFileChanged` -- the guest's G-08 `POST` with a path outside the system
  (expect `204 No game removed`); and L-12's toast raised from the pool
  thread. **L-16**: `git grep -n -A20 reloadCollection
  CollectionSystemManager.cpp` for a `clear()` or `delete` before return,
  and the holders listed -- the `getCursor()` lines (**20 in
  `ISimpleGameListView.cpp`; 30 across 9 of the 42 files**:
  `BasicGameListView.cpp` 2, `.h` 1, `CarouselGameListView.cpp` 2, `.h` 1,
  `GridGameListView.cpp` 1, `.h` 1, `IGameListView.h` 1,
  `ISimpleGameListView.h` 1 -- the list covers all 30), `mCurrentView`,
  `FileData::mRunningGame`; T33's file named, the disposition at the
  pause. **The `.7z` hash** `ThreadedScraper` runs as root (#1187, fixed
  `13a688804`; #1192): cited. `acceptResult` `:260-289` posting a raw
  `FileData*` to the interface thread, with `SystemData.cpp:393`'s
  `isRunning()` gate as what keeps the library alive under it: read and
  recorded. A table: every `std::thread` (13 lines in 5 files), every
  `postToUiThread(` (13 lines in 3 files: `HttpServerThread.cpp` 10,
  `DetailedContainer.cpp` 2, `ThreadedScraper.cpp` 1), every `delete` of a
  thread-owning object, who joins it, what it touches on the interface
  thread.
- **Q2 Bounded calls** (`es-code-traps.md:238`; `time-to-play.md`;
  D-CLOUD-075; `engineering-practices.md:799`; the bounds run). **L-06**:
  the seven `HttpReq` constructions in the slice's own code with their
  options; `HttpReq.cpp:204-213` the defaults (T21's file, cited). What
  bounds a scrape with the link cut after connect: nothing but CANCEL,
  whose own bound then depends on the handle's destructor -- the guest's
  G-05 (the link down before SCRAPE NOW, the page's ELAPSED line and
  outcome) and the unit case on `ScraperHttpRequest::update` with a doubled
  `HttpReq` (3.13); the fix a `stallTimeout` on the scraper's options as
  #299 did for the hasher (contained, rule 6; T21's `stallTimeout` work in
  es-core cited, not redone). **The probe without bounds**
  `ThreadedScraper::start` calls (`:290-321` ->
  `ScreenScraper::getThreadCount`, T21's `02:23`): cited. **The HTTP API's
  reload and idle** (D-QA-057): `/isIdle` (`HttpServerThread.cpp:306`),
  `/reloadgames` -> `reloadAllGames` with its unchecked
  `getSelectedSystem()` (T2 VC-5, `ViewController.cpp:1437`, recorded
  only) and `/launch` (`:599` the route, `:615-630`, `:625`): does the
  reload wait for idle, what a second `POST /launch` during a launch does,
  and what bounds a route's handler -- read line by line, which no audit
  has done. **The time-to-play line** (§ 6): which of the above sits
  between a press and a frame.
- **Q3 Reads that read as success** (`engineering-practices.md:111`,
  `:419`; blindspot 22; `es-player-text.md:236`; the success-reads run).
  **L-07** (#1191's caller half): a unit case on `ImageDownloadHandle` with
  a doubled `HttpReq` status; the guest's G-05 reads `GAMES SCRAPED: n`
  with no COULDN'T SCRAPE; the fix counts them in `errors` or says what
  did not arrive (stream brief). **3.13** `:372-376`: an unreachable
  scraper reads as "no results" (every request `REQ_IO_ERROR`,
  `processError` never called) -- G-05's positive and the unit case seen
  to FAIL at the pin; **`:337`** discards `process()`'s return, so
  `ArcadeDBJSONScraper.cpp:199`'s contract is dead. **3.10**
  `GamesDBJSONScraper.cpp:607` (`HasMember` before `IsObject`; `:605` the
  `const Value& boxart`): a unit case with `"boxart": []` under a checked
  rapidjson, FAIL at the pin. **3.16's remainder** `IGDBScraper.cpp:143-144`
  (the `if` on the two settings and its `return false`), the throw of
  `_("INVALID CREDENTIALS")` at `:167-172` (the string at `:172`), `:324`,
  `:331` (and `:230`): the `false` the other scrapers never return, and
  IGDB offered with no client id (G-06 frames the dialog). **3.17**
  `Scraper.cpp:681-685`: a non-image body (a provider's HTML error page)
  saved under the image's name and "resized" inside `catch(...) {}`; and
  the Content-Type table written twice (`:646-677`, `HttpApi.cpp:213-231`).
  **3.18** `getSaveAsPath`'s switch (`:784-799`): an id outside it (`Mix`)
  overwrites the image's name. **3.23** `HttpApi.cpp:240-253`:
  `ImportMedia` refuses `image/svg+xml` with `false` and no reason. **3.7**
  `GamesDBJSONScraper.cpp:293-309`: an array whose first element has no
  `filename` throws where an empty one returns `""`. **3.30**
  `BasicGameListView.cpp:123-124`: a cursor set to a file no longer listed
  lands on the root silently. A table of every read and parse with its
  writer, what a failure reads as, and the unit case or guest step that
  proves it.
- **Q4 Uncached reads** (`es-code-traps.md:104`; `es-native-ui.md:81`;
  T26's readers' rule `02:829`; the reads run). The 49 lines (50
  occurrences) of `exists(`, 0 with `, false)`: each with its file, its
  writer while ES runs, and whether a remembered miss changes the screen.
  **L-08**: the one-session positive on the guest (G-09's shape: a
  detailed list with no manual, a media file written over serial or
  through `POST` at `127.0.0.1:1234`, the row absent until a launch); the
  same shape as T31's Q4 at `GuiGameOptions.cpp:41` and
  `es-native-ui.md:81`'s own case. **L-09**: the cache deciding what to
  fetch and what to overwrite against files this run or a player over SSH
  changed since the cache answered. **Whether `FileSystemUtil`'s writers
  update their own cache is T21's file, and the answer is not "nothing":
  the cache is referenced at `FileSystemUtil.cpp:1051`, `:1067` (beside
  `removeFile` `:1059`), `:1097` (`createDirectory` `:1089`), `:1445`
  (`writeAllText` `:1429`), `:1457-1458` (`renameFile` `:1448`) and
  `:1506-1507` (`copyFile` `:1467`) -- the lane reads what each does and
  cites it.** `GamesDBJSONScraperResources.cpp:37` (its own resource
  cache) and `HttpServerThread.cpp:754` (the safe direction): recorded. The
  disposition per site: uncached (`, false`), left cached with the reason,
  or a stream.
- **Q5 The words, the French and the help bars** (`es-player-text.md:29`,
  `:141`, `:211`, `:236`; `es-code-traps.md:60`, `:79`;
  `es-ui-style-guide.md:169`; the strings, French and non-ASCII runs).
  **L-10**: one catalog line closes it (the French in the same commit as
  any string change, § 9); a French 640x480 frame of a list with save
  states and GAME OPTIONS AT NORTH on. **L-11**: the dialog and the
  `UIMode` write; po L116's empty `msgstr` for the same file's L115 msgid,
  ERROR: EVERY SYSTEM IS HIDDEN ... (the guest: hide every system under
  kid or kiosk, read the frame and `es_settings.cfg` after a restart).
  **L-04**: an upstream string on the fork's start path, one button each;
  the sentence at 640x480 in both locales (G-06). **L-05**: `git grep -n
  'setError(' Scraper.cpp` (the call at `:640` under `:638`'s `if (status
  != HttpReq::REQ_SUCCESS)`); G-05 reads line 4 against
  `es-player-text.md:236`. **L-12**: G-08's `POST /notify` with a long
  body against the one-line toast rule. **The help bars**: `getHelpPrompts()`
  is defined twice in the slice, `SystemView::getHelpPrompts` and
  `ISimpleGameListView::getHelpPrompts` (`:681-741`, #210, fork-own: SAVE
  STATES (HOLD) only with `cursorHasSaveStatesEnabled()` at `:361`/`:707`;
  the frames exist, `vm-qa-log:107`), and the five view styles inherit the
  latter's -- so G-02 reads one list bar per style against D-UI-034, not
  five overrides. **3.35** the 12 label strings
  (`DetailedContainer.cpp:112-140`) against `tools/es-untranslated`; the 0
  non-ASCII comments; the 51 msgids against the catalog with both
  `--upstream` lines recorded.
- **Q6 The views and their cost** (the lens; `time-to-play.md`;
  `es-code-traps.md:164`, `:191`; `es-native-ui.md:324`; D-UI-080/081;
  the views run). The four view styles and the carousel, one row each:
  what draws it, what it reads per item on the interface thread, what the
  first frame waits for. **L-14**: the per-tile read is
  `GridGameListView.cpp:42-47` (`setTileDecorator` calling
  `DisplayAspect::forScreenshot(file)`) into `DisplayAspect.cpp:99`
  (`forScreenshotPath`, ending `:131`) -- the guest with N seeded captures,
  press-to-first-frame of SCREENSHOTS in grid style against a list of 10
  (`tools/time-to-play`'s shape); **N is the lane's judgement at stage B,
  with a floor of what the window's bound can afford** (the seeding over
  serial sits inside G-02's bound), not a number this brief sets. **3.27**
  `SystemView.cpp:272-278`, `:331`: the fast move going negative on a
  carousel with fewer than ten systems (a unit case on the static, FAIL at
  the pin; G-04 on the guest: wraps cleanly, a wrong system, or
  `start_es.sh`'s backtrace in `journalctl -u essway`). **3.31**
  `GridGameListView.cpp:135-136`: IMAGE's fallback unreachable (a unit case
  on `getImagePath` with a `FileData` double, FAIL at the pin). **3.32**
  `GameNameFormatter.cpp:84-85`, `:171-185`: the year under a descending
  sort -- **`FileSorts.h:23` has `RELEASEDATE_DESCENDING = 11` beside
  `:22`'s `RELEASEDATE_ASCENDING = 10` (and `:37-40` the `SYSTEM_`
  variants), so the lead stands** -- and the 25-hour wrap at `:175`.
  **3.29** `ISimpleGameListView.cpp:486-603`: the UTF-8 lead byte as a
  letter; the `break` at `:514-515` assuming name order (G-03 frames the
  jump). **The #246 cursor shape** (Q1's L-16) and the 30 `getCursor()`
  lines; `BasicGameListView.cpp:54`, `:182`, `CarouselGameListView.cpp:61`,
  `:171` calling `reloadGameListView(this)` with nothing deleted first
  (recorded sound). **The #243 theme extra**: `DetailedContainer.cpp:1057-1072`
  and `ISimpleGameListView.cpp:755-765` reach both `mImage` and the extras
  (`es-code-traps.md:164`); `md_image` at `:61`, `:464`, `:1060` -- read,
  recorded. **The view-type selection's cost** (`ViewController.cpp:700-846`,
  T2's: `getFilesRecursive` walks the whole system once to choose a view)
  and `SystemView::populate` (`:196`) after UPDATE GAMELISTS (G-09): the
  two numbers in the retro.
- **Q7 The structure, the map and the merge debt** (`es-native-ui.md:32`,
  D-UI-039; `es-ui-style-guide.md:268`; `device-builds.md` § Build
  credentials; the membership, scope and delta runs). **L-15**: a section
  naming the five views, the row that picks them (GAMELIST VIEW STYLE on
  THEME CONFIGURATION, T26's, and SELECT > VIEW OPTIONS, T31's, § 2) and
  the SCREENSHOTS list where D-UI-080/081 and #210's bar are seen --
  mapped in the same commit as any row a stream touches, else a punch item
  saying which; `SystemView.cpp:552`'s computed title (#965): map it,
  declare it with a reason, or record it outside the checker's reach.
  **`UIModeController`'s gating**: the four modes, what the kid and kiosk
  collapse hides (`es-ui-style-guide.md:268`; the map's `:121-124`), the
  unlock sequence's reset on a wrong press (**3.33, settled: `:72` resets
  the counter on an incorrect input**), `LoadEmptySystems`. **The
  build-credential macros deciding which scrapers compile**: the registry
  at `Scraper.cpp:24-39` against `device-builds.md` § Build credentials and
  D-QA-003 -- which scrapers a fork image lists (ScreenScraper under the
  runtime define, ArcadeDB and IGDB always, TheGamesDB and HfsDB only with
  their macro), the macro names only; and IGDB's `Settings` keys against
  #274's backup strip (D-QA-050), by key name. **`httplib.h`**: **the
  vendored copy carries no version line and no `CPPHTTPLIB_VERSION` (0
  hits; its header reads `httplib.h / Copyright (c) 2020 Yuji Hirose`),
  so its currency is judged by content against cpp-httplib's 2020 series,
  not by a grep; `CPPHTTPLIB_OPENSSL_SUPPORT` is defined nowhere -- 0 hits
  in `es-app/CMakeLists.txt`, `CMakeLists.txt` and `HttpServerThread.cpp`
  at the pin and in `projects/ROCKNIX/packages/ui/emulationstation/package.mk`
  -- so the embedded server is plain HTTP on `127.0.0.1:1234`
  (`HttpServerThread.cpp:823-828`)**; a #585 line if a known fix is
  behind it -- a library checked for currency, not read line by line.
  **The merge debt**: the two § 5 commands (`log --format=%h
  cada856d86..rocknix/master -- $FILES` 0, `diff --numstat` empty), both
  bases named, the fork's six files with their numstat pairs, and what the
  slice carries that upstream lacks (the `maskSecrets` line, #210, the
  `Progress` contract, the aspect and turn, the `CheevosHash` argument) as
  the #585 candidates the coordinator weighs; D-WORKFLOW-080's shape (how
  the views' work would go upstream in pieces) recorded, not decided.

### The floor's 35 leads, carried

The floor digest is in no tree, so its § 3 is here, one line each, in the
shape `file:line at the pin | the function | the defect a unit case would
catch`, with the brief's corrections applied (3.10 at `:607`, 3.16's first
half withdrawn, 3.26's range); **(fork-own)** marks lines the fork wrote.
Each is a unit case in `ScraperReplies`'s shape (§ 5 item 1) unless marked
guest-only; the six that FAIL at the pin are in bold.

| # | At the pin | Function | What a case would catch |
| --- | --- | --- | --- |
| 3.1 | `ArcadeDBJSONScraper.cpp:26` (`:34-37`) | `generateRequests`'s URL | a change to the name cleaning ("Mr. Do!" -> `MrDo!`); needs a `FileData` double for the stem |
| 3.2 | `:76`, `:85`, `:94` | `getStringOrThrow` / `getIntOrThrow` | a silently defaulted field (missing key -> `runtime_error`) |
| 3.3 | `:103` | `getMediaTagNames(imageSource)` | a renamed `ScrapperImageSrc` value yielding no media with no error |
| 3.4 | `:121` | `findMedia(Value, source)` | tag precedence; a non-string skipped; none -> `""` |
| 3.5 | `:200` (`:213-218`, `:232-239`) | `ArcadeDBJSONRequest::process` | the `:199` contract ("return false only when ... maximum scrap by minute") -- see 3.13 |
| 3.6 | `GamesDBJSONScraper.cpp:195` (`:203-212`, `:225-256`) | `generateRequests` | the platform map (`:27`) drifting; the key segment at `:206`/`:218` stubbed in a unit |
| 3.7 | `:293` (`:309`) | `getBoxartImage(Value)` | an array whose first element has no `filename` throws where an empty one returns `""` |
| 3.8 | `:402` (`:313`, `:338`, `:363`; `loadResource` `:157`) | `findMedia(map, source)` and the three string joins | the resource JSON's shape (a fixture file in a temp dir) |
| 3.9 | `:553` (`:566-567`) | `TheGamesDBJSONRequest::preProcess` | the dependency queue's shape feeding 3.13; a string id skipped |
| **3.10** | `:575`; **`:605`, `:607`** | `TheGamesDBJSONRequest::process` | **`boxart.HasMember(...)` before `boxart.IsObject()`: `"boxart": []` is a rapidjson assertion, not the warning the line means to log** |
| 3.11 | `HfsDBScraper.cpp:308`, `:343` (`:385`, `:393`) | `getMediaTagNames`, `findMedia(Value, source)` | the `name == tagName + "type"` convention: a server rename falls through to a different picture |
| 3.12 | `:407` (`:410-420`), `:584` (`:597`, `:621-622`) | `processGame(..., arcadeGame)`, `HfsDBRequest::process` | the arcade filter dropping a valid system; the first-result rule |
| **3.13** | `Scraper.cpp:289` (`:317-333`, `:343-361` with `:351`, **`:337`**, **`:372-376`**) | `ScraperHttpRequest::update` over an `HttpReq` double and the `SDL_timer.h` fake | **404 and IO error end `ASYNC_DONE` with no error, so an unreachable scraper reads as "no results"; `:337` discards `process()`'s return**; the 429 arithmetic (T21's, inherited) |
| 3.14 | `:212` (`:224-255`) | `ScraperSearchHandle::update` over `ScraperRequest` doubles | the multi-URL fallback (HfsDB pushes several, `:288-289`) stopping at the first result |
| 3.15 | `:41-78` | `getScraperName` / `getScraperIndex` / `getScraperNameFromIndex` / `getScraper` | extracted over an injected vector: linking `Scraper.cpp` constructs every scraper at load (`:23-39`) |
| **3.16** | `IGDBScraper.cpp:143-144`, `:167-172`, `:314` (`:324`, `:331`; also `:230`) | `ensureToken`, `IGDBRequest::process` | **(remainder) `process` returns `false` where the three others return `true`; IGDB listed with no client id, `_("INVALID CREDENTIALS")` thrown at `:172`**; the `:143` unconditional-return half is withdrawn (it is an `if`); the design-intent read of `e14538b5c` and `71ff744d8` first |
| 3.17 | `Scraper.cpp:583` (`:646-677`, `:681-685`) and `HttpApi.cpp:210` (`:213-231`) | the Content-Type -> extension rule, written twice | the two copies diverging; a non-image body kept as `<game>-image.png` inside `catch(...) {}` |
| 3.18 | `:779` (`:784-799`, `:808-809`) | `getSaveAsPath` | an id outside the switch (`Mix`) overwriting the image's name |
| 3.19 | `ThreadedScraper.cpp:15`, `:155`, `:248` **(fork-own)** | `progress()`, `processError`, `updateUI` with a clock injection | a status added upstream landing in the wrong column of the outcome `GuiScraperRun` reads |
| 3.20 | `:103` (`:118-132`; `:79-82`) | `ScraperThread::updateState` over two `AsyncHandle` doubles | the state machine; `formatGameName` beside it |
| 3.21 | `HttpApi.cpp:102`, `:110` | `getFileDataId`, `findFileData` | the id scheme a web client caches (MD5 of the path; es-core `md5.cpp` host-built on 668) |
| 3.22 | `:170` (`:186`, `:192-193`, `:205`) | `ImportFromJson` | the string-only rule: an int silently ignored; `id` read as `scraperId` |
| 3.23 | `:210` (`:240`, `:245`, `:250`, `:253`) | `ImportMedia`'s rule half | `image/svg+xml` refused with `false` and no reason |
| 3.24 | `HttpServerThread.cpp:93`, `:114` (`:99-100`) | `mimeTypes`, `getMimeType` | the table (`.jpg` -> `image/jpg`, not the IANA type; no extension -> `text/plain`) |
| 3.25 | `:127` (`:129`) | `isAllowed` | `::1` refused unless public (`Settings.cpp` is host-buildable) |
| 3.26 | `:149-803` | the 16 distinct paths over 27 registrations; `listen(ip, 1234)` `:828` | not pure; G-08 reads them on the guest |
| **3.27** | `SystemView.cpp:272` (`:274`, `:277-278`; `:331`) | `_moveCursorInRange(value, count, sz)`, static and pure | **`(2, -10, 5)` leaves `-3`: the guard is `count >= sz` only and `value += sz` runs once; the fast move goes negative under ten systems** |
| 3.28 | `:282` (`:298-306`) | `moveCursorFast(forward)` | the manufacturer grouping and its rewind, over an injected vector |
| 3.29 | `ISimpleGameListView.cpp:486`, `:529`, `:580` (`:511`, `:554`, `:603`; `:514-515`) **(fork-own file)** | `moveToLetter`, `moveToLetterByOffset`, `getEntriesLetters` | `std::string(1, toupper(name[0]))` on a UTF-8 lead byte; the `break` assuming name order |
| 3.30 | `BasicGameListView.cpp:101` (`:123-124`) | `recurseFind(toFind, folder, stack)` | not found with an empty stack -> the root's items, silently |
| **3.31** | `GridGameListView.cpp:131` (`:135-136`, `:144`, `:153`) **(fork-own file)** | `getImagePath(file)` | **`src == IMAGE` returns `getImagePath()` even when empty: the fallback and the thumbnail unreachable for IMAGE** |
| **3.32** | `GameNameFormatter.cpp:56`, `:113`, `:121` (`:84-85`, `:162-166`, `:171-185`) | `getLangFlag`, `valueOrDefault`, `getDisplayName` | **`:84-85` test `RELEASEDATE_ASCENDING` twice and never `FileSorts.h:23`'s `RELEASEDATE_DESCENDING`: no year under a descending sort**; `h = (seconds / 3600) % 24` wraps a 25-hour game |
| 3.33 | `UIModeController.cpp:55-97` (`:72` the reset), `:185` | the unlock sequence (`listen`, `inputIsMatch`, `isValidInput`) | blocked by `InputConfig.h` until extracted; a wrong press resets the counter at `:72` (settled) |
| 3.34 | `ISimpleGameListView.cpp:681` (`:714`, `:717`, `:725`, `:732`, `:739`) **(fork-own, #210)** | `getHelpPrompts`'s choice half | the #210 rule regressing; the frames exist (`vm-qa-log:107`) |
| 3.35 | `DetailedContainer.cpp:112-140`, `:1010`, `:1043` **(fork-own file)** | the 12 label strings, `valueOrUnknown`, YES/NO | a label added without French (`es-untranslated`'s line); `:1446-1450` is a commented-out `ngettext`, dead text |

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #679.** Every read, count and table runs on the host
   at the pin's bytes. **The host has no toolchain** (#1137):
   `tools/es-syntax-check` exits 2 on this host (`no build root at ...`,
   its `:69`) and records that line with `ES_BUILD_ROOT` set, never
   empty; every `.cpp` here is `CANNOT` for the host's plain `g++
   -fsyntax-only` until proven otherwise (the measured first error on
   `ThreadedScraper.cpp` is `es-core/src/HttpReq.h:5:10: fatal error:
   curl/curl.h`, rc 1 -- curl before SDL; SDL through `Window.h` and
   `views/ViewController.h` is what the includes of 13 of them promise
   next; vlc for `SystemView.cpp` and `DetailedContainer.cpp`), and its
   compile proof is the integration build's. The one precedent, T21's
   stand-in-header check on `Scraper.cpp` (§ 2), is worth repeating on the
   five scrapers and `GameNameFormatter.cpp` with the thirteen fakes of
   `docs/audits/2026_10_26-epic-m6-es-state-and-bridge/stage-e/syntax-check.sh`
   (read from `origin/feature/m6-es-state-and-bridge-668`); it checks the
   file's own C++ and proves nothing about curl or SDL. **Nothing reads the
   slice today** (§ 2), so **the host floor is the lane's own: unit cases
   in the ES worktree's `es-app/tests/unit/` for the pure leads** in
   `ScraperReplies`'s and `CloudText`'s shape (`es-code-traps.md:139`: the
   pure rule moves to a function with nothing from the window, the fonts
   or the filesystem behind it; the thin shell stays) -- **the six that
   FAIL at the pin first** (3.10, 3.13, 3.16's remainder, 3.27, 3.31,
   3.32, in bold in § 4's table), each seen to FAIL against the unfixed
   extract before it is trusted, and the stub that constructs the failure
   checked against the unfixed code first (`engineering-practices.md:464`);
   then the rest of the 35. The cases are **built by the lane's generated
   script in T21's and T26's shape**
   (`docs/audits/2026_10_26-epic-m6-es-state-and-bridge/tools/t21-build-tests.sh`,
   `docs/audits/2026_10_27-epic-m6-es-guimenu/tools/t26-build-tests.sh`,
   each on its lane's branch: the targets parsed out of
   `es-app/tests/unit/CMakeLists.txt` by a `python3 -I` pass, `g++
   -std=c++17 -O0 -g0 -pthread`, include roots `es-app/src`, `es-core/src`,
   `external`; **rapidjson from the recipe's tarball plus its four patches**
   -- `projects/ROCKNIX/packages/devel/rapidjson` is 1.1.0 with
   `rapidjson-0001-remove_custom_cxx_flags.patch`,
   `0002-Removed-non-compiling-assignment-operator.-Fixed-718`,
   `0003-Explicitly-disable-copy-assignment-operator`,
   `0004-build-with-cmake-4.0.0` -- unpacked under `/workspace/tmp/m6-t32/rj/`
   as T21 did; **pugixml from the pin's extracted source** at
   `/workspace/cache/rocknix-sources/emulationstation/emulationstation-<PIN>/external`),
   saved as `docs/audits/<audit>/tools/t32-build-tests.sh`, **the total
   quoted as the script's `TOTAL: N test cases in B binaries` line** and
   never summed by hand (`engineering-practices.md:250`); `Settings.cpp`,
   `AtomicFileUtil.cpp`, `FileSystemUtil.cpp`, `StringUtil.cpp` and
   `md5.cpp` are host-buildable dependencies a case may link (T21's
   `es-settings-tests`). `tools/es-menu-map-check`, `tools/es-untranslated
   --upstream bccd715707` (and the same with `cada856d86`, both lines
   recorded), the non-ASCII comment grep, the counts and the generated
   tables run on the host.
2. **The guest window** -- one, asked for on #679 at stage B's end with its
   plan and bound (**35 minutes proposed, plus 5 of grace**: the plan
   below sums to 22 without a stub, T26's window ran 23), granted
   explicitly by the coordinator on #679 and in the shared log's queue.
   **The queue is the shared file's own lines**,
   `/tmp/m7-m6-host-coordination-20261023.txt`: a request is a line that
   names the slice, its plan and its bound; the grant is the coordinator's
   line answering it; the lane's START and RETURN each add a line with the
   census; the file is read before any guest starts (§ 1's last command
   reads its tail). One boot of the M6 copy of the image
   (`/workspace/artifacts/m6-t2-20261023/`, `069fc2704421`) **started at
   640x480** (`projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run
   --headless --daemonize --res 640x480`, `generic-x64-vm-testing.md:108`,
   `:215`, #1141), **under T13's conditions -- T13 is #660, the first M6
   lane to hold a guest window, and its shape is every later window's
   (T26's and T31's included); spelled out here so the lane needs no
   other file:** one guest, from that M6 copy, at 640x480; **the image
   identified by two literals first** (`BUILD_ID` from `/etc/os-release`
   and the file name); **every verdict labelled by side** because the
   image's EmulationStation is M7's composition -- a frame is `pin-binary`
   evidence only where the digest found the pin's lines unchanged against
   the image's binary, else `image` (`generic-x64-vm-testing.md:1432`);
   the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as the
   first line of each post on #679 and a line in the shared host file,
   each with the census (`qemu N, compilers N`); the stop by pidfile at
   bound plus grace (`tools/vm-stop`, never a pattern); the disk retired
   after with path, size and sha (D-INFRA-022); and the guarded
   `tools/build-preflight --reclaim-swap` allowed once, before the guest,
   never beside it. **The floor's limit, said plainly: a no-NIC guest
   cannot show any scraper's success path.** The scrapers' hosts are
   literals (`http://adb.arcadeitalia.net`, `ArcadeDBJSONScraper.cpp:29`;
   `https://api.thegamesdb.net/v1`, `GamesDBJSONScraper.cpp:199` (and
   `:571`); `db.hfsplay.fr`, `HfsDBScraper.cpp:195` and `:224`;
   `api.igdb.com`, `IGDBScraper.cpp:187`); only ArcadeDB is plain http
   and stub-able, and that needs the guest's resolver pointed at the host
   over serial **and a host listener on port 80**, privileged on this host
   -- `CANNOT` unless it is available; the three https scrapers are unit
   cases only (the 429 and stall paths too), and #156's TLS shim is the
   harness item. What the guest does show: every view's rendering, the
   cursor and letter logic, the offline scrape's outcome words, the IGDB
   dialog in both locales, the local HTTP API, the French strings. The QA
   accounts are needed by no row (`tools/qa-accounts`, never printed, only
   if a row grows one; D-QA-016; never the owner's, D-QA-015). Every
   proof's frames are labelled by side; a fix's frame is
   `fix-walk-pending-image`.

   | G | Behaviour only the running image shows | Walk or serial command | Expected frame or line | Bound (s) |
   | --- | --- | --- | --- | ---: |
   | G-01 | identity and side | `vm-serial sh 'cat /etc/os-release; fbset'`; the ES binary's digest against the pin's lines (T26's `g01-identity.txt` shape) | `BUILD_ID=...`, `640x480`; every frame labelled `image` or `pin-binary` | 60 |
   | G-02 | `SystemView` and a game list per view style at 640x480 | `manager-gb`'s first two steps (`settle / shot 0-carousel / key x / wait-for-change / settle / shot 1-list`), then GAMELIST VIEW STYLE cycled on THEME CONFIGURATION (`GuiMenu.cpp:8668`, the row `:8691`/`:8729`, values `automatic basic detailed video grid gamecarousel`; the hop from USER INTERFACE SETTINGS read on the guest) or per list through SELECT > VIEW OPTIONS (`GuiGamelistOptions.cpp:194`/`:232`), and `shot` per style: basic, detailed, video, grid, carousel; the captures for L-14 seeded over serial first | the fixture list drawn in each style (no 640x480 baseline exists to diff against, #1141: these frames are the first); the one list help bar (`ISimpleGameListView::getHelpPrompts`, #210) read back from the frame; the `SAVE STATES (HOLD)` French frame for Q5 | 240 |
   | G-03 | the letter jump (3.29) | on a list with three or more first letters: the next/previous-letter keys (`ISimpleGameListView::input` `:256-335`, read first), `shot` after each | the cursor on the first game of the next letter; the wrap from the last letter to the first | 120 |
   | G-04 | the carousel's fast move with fewer than ten systems, backward (3.27) | on `0-carousel`: the fast-move key backward (`SystemView::input` `:376-515`, read first), `shot`; then forward | wraps cleanly -- or a wrong system, a blank, or `start_es.sh`'s backtrace in `journalctl -u essway` (`device-builds.md` § Reading a crash) | 120 |
   | G-05 | SCRAPE NOW with the link down (3.13's `:372`; L-05's line 4; L-07's COMPLETED) | `vm-serial sh 'ip link set eth0 down'`; MAIN MENU > SCRAPER > SCRAPE, ArcadeDB selected (no credentials), SCRAPE NOW; `shot` the SCRAPING GAMES page's outcome; link back | the outcome words for a run whose every request ended `REQ_IO_ERROR` (from the code: COMPLETED-shaped with nothing scraped, not COULDN'T FINISH -- the lead's positive); line 4's words; journal `ThreadedScraper::SearchResponse : <code>` (`:112`); the walk's steps kept under `stage-e/walks/` (Backlog #1190's first scrape walk) | 240 |
   | G-06 | IGDB selected with no client id (3.16's remainder; L-04) | SCRAPER > SCRAPE, source IGDB, SCRAPE NOW; `shot`; then `system.language=fr_FR`, ES restarted (`generic-x64-vm-testing.md:383`: back on the last list -- one `z`, a frame, then drive), the same | `AN ERROR OCCURRED :` + `INVALID CREDENTIALS` (`ThreadedScraper.cpp:314` over `IGDBScraper.cpp:172`) in EN and FR; **B lands on the only button** (the boxes at `:299` and `:314` name none, so the back accelerator falls to the last and only one) | 180 |
   | G-07 | ArcadeDB against a host stub | `vm-serial sh 'echo 10.0.2.2 adb.arcadeitalia.net >> /etc/hosts'`; a host HTTP server on :80 answering `/service_scraper.php` with a fixture JSON | the game's metadata and image landing in the list (`getSaveAsPath` -> `images/<stem>-image.png`); then L-08's stale read: the MANUAL row before and after, one session | 240 -- `CANNOT` without host port 80 |
   | G-08 | the HTTP API (3.21 to 3.26; L-12; L-13), **plain HTTP, reached from inside the guest** | over `vm-serial`/SSH, as `tools/vm-qa:479` does: `wget -qO- http://127.0.0.1:1234/caps; wget -qO- http://127.0.0.1:1234/isIdle`; `POST /notify` with a long body; `POST` the delete route with a path outside the system; `shot` | JSON with `"Version"` (`HttpApi.cpp:332`); `[ true ]`; a toast frame against the one-line rule; `204 No game removed`; **the `403` for a non-loopback address is `CANNOT` from the host: `generic-x64-vm:380-383` forwards SSH and the profile's services, never 1234** | 120 |
   | G-09 | the list after UPDATE GAMELISTS; the stale read without a stub | GAME SETTINGS > UPDATE GAMELISTS; `shot` the carousel and `1-list`; a media file written over serial into a game's `images/` while its detailed list is open, the list re-entered | the same frames as G-02 (`SystemView::populate` `:196`, the view remade); the picture or MANUAL row absent until a launch -- L-08's positive, `image` side | 120 |
   | G-10 | an HTTP stall or 429 inside the scrape | -- | `CANNOT`: the https hosts refuse a stub; 3.13's unit cases and T21's `stallTimeout` work (es-core) | 0 |
   | G-11 | close | `tools/vm-stop` on the pidfile; the disk's size and sha recorded; `qemu 0, compilers 0` | `retired.txt`; the leftover check | 120 |

   Sum of the bounds as written: 1,560 s (26 min) with G-07 counted; 1,320 s
   (22 min) without it (the floor's figures, summed by its author's
   command). Every frame is read back for its strings; each confirmation's
   B landing is framed (G-06).
3. **What T33 to T37 inherit** is written, not tested here: the views'
   provenance table (6 / 36 with both bases named), the cached-read table
   with its writers, the thread-and-lifetime table, the bounds table (every
   `HttpReq` construction with its options), the scrapers' outcome routing
   (status -> `processError` -> `Progress` -> the page's line), the
   `httplib.h` currency note, and the map section for the views.
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   ES branch, proven twice (`fix-unit-test` through a case the build
   script links, or `fix-walk-pending-image`), the covering case run before
   every commit, under § 9's same-commit rules for the map and the French;
   a fix on `Scraper.cpp` that meets T21's `3ae9610b0`, `44d3c7e25` or
   `e38dcdefd` lines is written against the pin and named as a collision
   in the hand-back (§ 1).

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its
reason). From the distribution worktree after the membership block; `W`
the ES worktree (§ 1), `PIN` the pin, `MB` the merge base, `X` the
exclusion regex, `FILES` the 42; counts by `/usr/bin/grep` (#1138);
**every grep for `_("` is `-F`** -- the basic-regex form with `\(` was
T31's stage-A erratum and is not written here; `rc=$?` on its own line,
never after a pipe. Every expectation below is a line the proof printed
from the pin on 2026-10-27, except the three marked by stage, which cannot
run before the lane writes their inputs:

```bash
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-views-scrapers-679; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; C=8ebaf8daad; MB=cada856d86
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t32/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
X='^es-app/src/(views/ViewController\.|scrapers/ScreenScraper\.)'
FILES=$(git -C "$W" ls-tree -r --name-only "$PIN" -- es-app/src/views es-app/src/scrapers es-app/src/services | $G -v -E "$X")
# the scope (expect 46 all; 4 excluded; 42 in scope; by directory scrapers 14, services 5, views 23 of which gamelist 18; cpp 20 h 22)
git -C "$W" ls-tree -r --name-only "$PIN" -- es-app/src/views es-app/src/scrapers es-app/src/services | $G -c .; git -C "$W" ls-tree -r --name-only "$PIN" -- es-app/src/views es-app/src/scrapers es-app/src/services | $G -c -E "$X"; printf '%s\n' $FILES | $G -c .; for d in scrapers services views views/gamelist; do printf '%s %s\n' "$d" "$(printf '%s\n' $FILES | $G -c "^es-app/src/$d/")"; done; printf '%s\n' $FILES | $G -c '\.cpp$'; printf '%s\n' $FILES | $G -c '\.h$'
# the ES worktree at the pin, clean; the two merge bases; the counts (expect the pin; 0; cada856d86; bccd715707; 14; 725; 1; f6c542872e; 3ae9610b0)
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l; git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10; git -C "$W" merge-base bccd715707 "$PIN" | cut -c1-10; git -C "$W" rev-list --count "$MB"..rocknix/master; git -C "$W" rev-list --count bccd715707.."$PIN"; git -C "$W" rev-list --count bccd715707.."$MB"; git -C "$W" rev-parse rocknix/master | cut -c1-10; git -C "$W" rev-parse origin/feature/m6-es-state-and-bridge-668 | cut -c1-9
# the lines two ways (expect wc -l 17306; grep -c 17311; no trailing newline: 5)
for p in $FILES; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'; for p in $FILES; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c", s}'; n=0; for p in $FILES; do a=$(git -C "$W" show "$PIN:$p" | wc -l); b=$(git -C "$W" show "$PIN:$p" | $G -c ''); [ "$a" != "$b" ] && n=$((n+1)); done; echo "no trailing newline: $n"
# the fork's delta over the slice (expect 6 rows, all M, no A, no D; the sums 168 46; the pairs 2 2 Scraper.cpp, 56 22 ThreadedScraper.cpp, 30 4 ThreadedScraper.h, 21 0 DetailedContainer.cpp, 14 0 GridGameListView.cpp, 45 18 ISimpleGameListView.cpp; the same against bccd715707; 0 and fork-added rc=1)
git -C "$W" diff --name-status "$MB" "$PIN" -- $FILES; git -C "$W" diff --numstat "$MB" "$PIN" -- $FILES | awk '{a+=$1; r+=$2} END {print a, r}'; git -C "$W" diff --numstat bccd715707 "$PIN" -- $FILES | awk '{a+=$1; r+=$2} END {print a, r}'; git -C "$W" diff --diff-filter=A --name-only bccd715707 "$PIN" -- $FILES | $G -c .; rc=$?; echo "fork-added rc=$rc"
# upstream's delta over the slice: the merge-debt record (expect 0 rc=1; 0 rc=1; 42; 42; the three tree hashes cd0f559cb1 2f14b69046 2ffe2cc4cf at bccd715707, cada856d86 and rocknix/master, and 31078e99df 1e39292413 2ffe2cc4cf at the pin)
git -C "$W" log --format=%h "$MB"..rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream commits on the slice rc=$rc"; git -C "$W" diff --numstat "$MB" rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream numstat rows rc=$rc"; git -C "$W" ls-tree -r --name-only "$MB" -- es-app/src/views es-app/src/scrapers es-app/src/services | $G -v -E "$X" | $G -c .; git -C "$W" ls-tree -r --name-only rocknix/master -- es-app/src/views es-app/src/scrapers es-app/src/services | $G -v -E "$X" | $G -c .; for r in bccd715707 "$MB" rocknix/master "$PIN"; do printf '%s ' "$r"; for d in views scrapers services; do printf '%s ' "$(git -C "$W" rev-parse "$r:es-app/src/$d" | cut -c1-10)"; done; echo; done
# T21's deltas on this slice, inherited (expect 6 rows, the pathspec being the three directories: Scraper.cpp 28 8, Scraper.h 5 0, ScraperReplies.cpp 51 0, ScraperReplies.h 22 0, and -- outside the 42 -- ScreenScraper.cpp 17 16 and ViewController.cpp 8 2; the three commits 3ae9610b0 44d3c7e25 e38dcdefd on Scraper.cpp)
git -C "$W" diff --numstat "$PIN" origin/feature/m6-es-state-and-bridge-668 -- es-app/src/views es-app/src/scrapers es-app/src/services; git -C "$W" log --format=%h "$PIN"..origin/feature/m6-es-state-and-bridge-668 -- es-app/src/scrapers/Scraper.cpp | tr '\n' ' '; echo
# the fork's commits per touched file, no merges, from bccd715707 (expect Scraper.cpp 2, ThreadedScraper.cpp 1, ThreadedScraper.h 1, DetailedContainer.cpp 5, GridGameListView.cpp 1, ISimpleGameListView.cpp 4; 10 non-merge commits on the slice, 11 with the merge 370ebe416)
for f in scrapers/Scraper.cpp scrapers/ThreadedScraper.cpp scrapers/ThreadedScraper.h views/gamelist/DetailedContainer.cpp views/gamelist/GridGameListView.cpp views/gamelist/ISimpleGameListView.cpp; do printf '%s %s\n' "$f" "$(git -C "$W" log --no-merges --format=%h bccd715707.."$PIN" -- "es-app/src/$f" | $G -c .)"; done; git -C "$W" log --no-merges --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; git -C "$W" log --format=%h bccd715707.."$PIN" -- $FILES | $G -c .
# the strings, two ways (expect lines TOTAL 58 in 9 files; occurrences 70; SystemView.cpp 18 and ISimpleGameListView.cpp 18 the two largest)
git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F '_("' "$PIN" -- $FILES | wc -l
# the dialogs and pages built (expect new Gui TOTAL 19 in 5 files; GuiMsgBox 8; the sites read whole for the buttons in order -- the two AN ERROR OCCURRED boxes at ThreadedScraper.cpp:299 and :314 and SystemView.cpp:234's bare "OK" among them)
git -C "$W" grep -c -E 'new Gui[A-Za-z]+' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -E 'new Gui[A-Za-z]+' "$PIN" -- $FILES | sed -E 's/.*new //' | sort | uniq -c | sort -rn; git -C "$W" grep -n -A2 -F 'GuiMsgBox(' "$PIN" -- $FILES | sed "s/^$PIN://" > "$TMPDIR/dialogs.txt"; $G -c 'GuiMsgBox(' "$TMPDIR/dialogs.txt"
# the threads and the lifetimes (expect std::thread TOTAL 13 in 5 files, 9 in httplib.h; new std::thread at ThreadedScraper.cpp:53 and HttpServerThread.cpp:74; delete this at ThreadedScraper.cpp:241; mInstance on 9 lines of ThreadedScraper.cpp; .detach( 0 rc=1; postToUiThread( TOTAL 13 in 3 files: HttpServerThread.cpp 10, DetailedContainer.cpp 2, ThreadedScraper.cpp 1)
git -C "$W" grep -c -F 'std::thread' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -n -E 'new std::thread|delete this' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -c -F 'mInstance' "$PIN" -- es-app/src/scrapers/ThreadedScraper.cpp | sed "s/^$PIN://"; git -C "$W" grep -n -F '.detach(' "$PIN" -- $FILES | $G -c .; rc=$?; echo "detach rc=$rc"; git -C "$W" grep -c -F 'postToUiThread(' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'
# the bounds (expect HttpReq lines TOTAL 83 in 14 files, Scraper.cpp 27 the most, occurrences 95; new HttpReq( at GamesDBJSONScraperResources.cpp:153 and Scraper.cpp:267 302 332 564 567 596; 0 lines setting timeout or stallTimeout -- the second grep prints nothing, rc 1; the HttpReqOptions declarations are at HfsDBScraper.cpp:179 :287, IGDBScraper.cpp:146 :189 :205 :215, Scraper.cpp:539 and Scraper.h:104)
git -C "$W" grep -c -F 'HttpReq' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F 'HttpReq' "$PIN" -- $FILES | wc -l; git -C "$W" grep -n -E 'new HttpReq\(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'stallTimeout|\.timeout\s*=|setTimeout' "$PIN" -- $FILES | $G -c .; rc=$?; echo "bounds rc=$rc"
# the success-reads (expect the first grep to print `214 237 253 336 346 359 371 374 469 480 486 503 519 612 630 633 688` -- the setStatus and comment lines beside the leads' :337, :372, :607 and :631, which the pattern does not hit; IsObject prints `448 607`, the second the HasMember-before-IsObject line; `return false;` in IGDBScraper.cpp prints `144 164 230 324 331`, :144 the return under :143's if)
git -C "$W" grep -n -E 'ASYNC_DONE|Ignore' "$PIN" -- es-app/src/scrapers/Scraper.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'IsObject' "$PIN" -- es-app/src/scrapers/GamesDBJSONScraper.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -E '^\s*return false;' "$PIN" -- es-app/src/scrapers/IGDBScraper.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo
# the reads (expect exists( lines TOTAL 49 in 6 files, occurrences 50, 0 with `, false)` rc=1; Scraper.cpp 25 lines, DetailedContainer.cpp 19; DetailedContainer's lines 667 669 677 679 681 756 762 765 768 771 817 819 827 829 831 863 873 903 916)
git -C "$W" grep -c -F 'exists(' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F 'exists(' "$PIN" -- $FILES | wc -l; git -C "$W" grep -n -E 'exists\([^)]*, *false\)' "$PIN" -- $FILES | $G -c .; rc=$?; echo "uncached rc=$rc"; git -C "$W" grep -n -F 'exists(' "$PIN" -- es-app/src/views/gamelist/DetailedContainer.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo
# the process starts and the parses (expect system( popen( runSystemCommand( 0 rc=1; std::stoi( TOTAL 3 in 1 files; std::stoul( 0; atoi( 0; toInteger( TOTAL 6 in 5 files; atol( TOTAL 1 in 1 files, GameNameFormatter.cpp:171, the play-time parse 3.32 cites)
git -C "$W" grep -n -E '(^|[^A-Za-z_])(system|popen)\(|runSystemCommand\(' "$PIN" -- $FILES | $G -c .; rc=$?; echo "process starts rc=$rc"; for k in 'std::stoi(' 'std::stoul(' 'atoi(' 'toInteger(' 'atol('; do printf '%s ' "$k"; git -C "$W" grep -c -F "$k" "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s+0, "in", NR, "files"}'; done
# the help bars and the views (expect only SystemView.cpp and ISimpleGameListView.cpp to define ::getHelpPrompts( -- the five styles inherit the latter's; the five getName() defaults at BasicGameListView.h:31 CarouselGameListView.h:32 DetailedGameListView.h:24 GridGameListView.h:36 VideoGameListView.h:26; _moveCursorInRange at SystemView.cpp 272 293 296 303 305 315 318 325 327 331)
git -C "$W" grep -l -F '::getHelpPrompts(' "$PIN" -- $FILES | sed "s/^$PIN://" | sed -E 's#.*/##' | tr '\n' ' '; echo; git -C "$W" grep -n -E 'return "(basic|detailed|video|grid|gamecarousel)"' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -F '_moveCursorInRange' "$PIN" -- es-app/src/views/SystemView.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo
# STAGE C -- the include graph: the lane's script under the audit folder's tools/, which does not exist at stage A (expect its last three lines: 47 include lines from 23 files outside the slice; es-core edges 143 of 410)
python3 -I docs/audits/*-epic-m6-es-app-views-scrapers/tools/t32-includes.py "$W" "$PIN" .qa-scratch/t32/paths.txt | tail -n 3
# the T21-class uses and the credential shapes, file:line only (expect 51 lines in 14 files, 13 of them #include; ScreenScraper only at Scraper.cpp:6 and :26; the macro names at the lines § 1 gives; no value printed -- every line cut to its file and number)
git -C "$W" grep -n -E 'ViewController|ScreenScraper' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1 | sort | uniq -c | sort -rn; git -C "$W" grep -n -E 'ViewController|ScreenScraper' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -o -E 'GAMESDB_APIKEY|HFS_DEV_LOGIN|SCREENSCRAPER_(RUNTIME_)?DEV_LOGIN' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2,3 | tr '\n' ' '; echo
# the non-ASCII comments (expect files with non-ascii comments: 0; adjacent 0 rc=1 -- the adjacency grep is -F, never a basic-regex `\(`)
n=0; for f in $FILES; do c=$(git -C "$W" show "$PIN:$f" | $G -c -P '^\s*//.*[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "$f:$c"; n=$((n+1)); }; done; echo "files with non-ascii comments: $n"; for f in $FILES; do git -C "$W" show "$PIN:$f" | $G -n -P -A1 '^\s*//.*[^\x00-\x7F]' | $G -F -B1 '_("'; done | $G -c .; rc=$?; echo "adjacent rc=$rc"
# the harness sweep (expect no basename printed before `sweep done`; 15 .py under tests/; 19 *Tests.cpp under es-app/tests/unit/)
for c in $(printf '%s\n' $FILES | sed -E 's#.*/##; s#\.(cpp|h)$##' | sort -u); do h=$(git -C "$W" grep -l -w -- "$c" "$PIN" -- es-app/tests tests CMakeLists.txt es-app/CMakeLists.txt es-core/CMakeLists.txt | sed "s/^$PIN://" | $G -v '^es-app/CMakeLists.txt$' | tr '\n' ' '); [ -n "$h" ] && echo "$c: $h"; done; echo "sweep done"; git -C "$W" ls-tree -r --name-only "$PIN" -- tests/ | $G -c '\.py$'; git -C "$W" ls-tree -r --name-only "$PIN" -- es-app/tests/unit/ | $G -c 'Tests\.cpp$'
# the French (expect 218 msgid "SAVE STATES (HOLD)" / 219 msgstr "SAUVEGARDES (MAINTENU)" and 233 msgid "SAVE STATES" / 234 msgstr "SAUVEGARDES D’ÉTAT"; L115 the msgid "ERROR: EVERY SYSTEM IS HIDDEN, RE-DISPLAYING ALL OF THEM NOW" and L116 `msgstr ""`; es-untranslated `706 fork string(s) in the source, 706 with French, 0 without` rc 0 against bccd715707 and `703 fork string(s) in the source, 703 with French, 0 without` rc 0 against cada856d86)
git -C "$W" grep -n -A1 -E '^msgid "SAVE STATES( \(HOLD\))?"$' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://" | cut -c1-80; git -C "$W" show "$PIN:locale/lang/fr/LC_MESSAGES/emulationstation2.po" | sed -n '115,116p'
out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated rc=$rc"
out=$(tools/es-untranslated --es-src "$W" --upstream "$MB" 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated(cada) rc=$rc"
# the menu map (expect `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0; one line matches the view-style grep, :135 the USER INTERFACE row; the map at 989 lines)
out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"; $G -n -E 'VIEW STYLE|GAMELIST|GAME LIST|SCREENSHOTS' docs/es-menu-map.md | cut -c1-60; wc -l docs/es-menu-map.md
# the compile (expect `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2, its :69; plain g++ on ThreadedScraper.cpp: `es-core/src/HttpReq.h:5:10: fatal error: curl/curl.h: No such file or directory` rc=1 -- curl, not SDL, measured on the pin's bytes; the stand-in check on Scraper.cpp rc 0 as T21 recorded, with T21's fakes copied under the audit folder's stage-a/fakes/ and RAPIDJSON_INCLUDE_DIR set)
F=es-app/src/scrapers/ThreadedScraper.cpp; out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc"
out=$(g++ -std=c++17 -fsyntax-only -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$F" 2>&1); rc=$?; printf '%s rc=%s\n' "$(printf '%s\n' "$out" | $G -m1 -E 'fatal error|error:' | cut -c1-90)" "$rc"
# STAGE C -- the unit build: the lane's script, which does not exist at stage A (expect its own `TOTAL: N test cases in B binaries` line with 0 failed in every binary's doctest summary; before any fix, the six FAIL-at-pin cases reported as FAIL by name)
bash docs/audits/*-epic-m6-es-app-views-scrapers/tools/t32-build-tests.sh "$W" 2>&1 | tail -n 8
# STAGE A, after the pointer is read -- the removal check: TIPHASH is the lane's own tip the pointer and the dispatch comment name (MERGE_HASH at stage A; never 2174265e9c itself, whose tools/ differ from the coordinator's); the literal word fails with `fatal: bad revision` (expect empty) and the ES diff against the pin (expect empty before stage E)
git diff --stat TIPHASH HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1
```

## 6. Outputs

As T26's and T31's briefs § 6; § 7 is this section as checkboxes, so only
the layout and `02`'s section order are given here. The folder
`docs/audits/<yyyy_mm_dd>-epic-m6-es-app-views-scrapers/`: `00-running-log.md`
to `05-punch-list.md`; `second-opinions/` (`review-plan.json`, the probe's
and the refutation's `.provenance.json`, `packet-manifest.json`); `stage-a/`
to `stage-e/` (the first commands and the § 5 runs under `stage-a/`; the
window plan under `stage-b/`; the host proofs under `stage-c/`; the walks'
steps under `stage-e/walks/`); `tools/` (the generators -- `t32-includes.py`,
`t32-build-tests.sh`, the tables' generators -- each asserting its counts
and each seen to exit 1 on a constructed drift before it is trusted);
`guest-cycle/`; the lint before D; the audit issue (`Audit: M6 T32
EmulationStation's game list views, scrapers and services -- N findings
(...)`, a sub-issue of #679; the audit issue and the bugs are the lane's,
D-WORKFLOW-189; a Backlog for a lead outside the 42 is the coordinator's,
named in the hand-back); and the retro at
`docs/retros/<date>-m6-es-app-views-scrapers.md` (**what the slice did to
the two time-to-play numbers**: the list's press to `launch`, the
SCREENSHOTS grid's per-tile reads and the carousel's `populate` after
UPDATE GAMELISTS named with what they cost on the guest, cited from
`docs/vm-qa-log.md`; never "nothing" by default; **what T33 to T37
inherit**: § 5 item 3). **`02-forward-audit.md` carries these sections, in
this order, each generated section's row count stated as "generated,
asserted" by the script that made it:** § Coverage (42, one row per path,
the path in backticks as the first cell, both tiers), § The leads (L-01
to L-17 and 3.1 to 3.35 from § 4's table, each with its lines, its family,
who owns it, its disposition), § The views (one row per view class and
the carousel: what draws it, the per-item reads, what the first frame
waits for, which `getHelpPrompts` it shows), § The scrapers (one row per
scraper: the host literal, the macro gate, the options its requests
carry, the status routing to `processError`, the success-reads), § The
services (the 16 distinct paths over their 27 registrations: the thread
each runs on, what it posts, what it writes, what bounds it), § The reads
(one row per `exists(` line, 49: the file, its writer while ES runs,
cached or not, what a miss reads as), § The bounds (one row per `HttpReq`
construction, 7 in the slice's own code: its options, connect, total,
stall), § The words (the 58 lines, the 51 msgids, L115/L116, L218/L233,
the dialog words, the toast), § The structure (the modes, the macro-gated
registry, the include cycle, `httplib.h`'s currency), § The merge debt
(one line, both bases), § The runs, § The guest cycle, § The streams
(stage E: **written by the coordinator after stage D, as for T21 and
T26**; the lane leaves the heading and the pause's dispositions),
§ Positives, § The #585 lines owed (one per upstream-carried defect closed
under rule 6, in the shape the lane writes, never sent), § What T33 to T37
inherit; every proof with `proved:`. The stage-D pause as T21's: the punch
list posted on #679, the lane waits for the coordinator's dispositions and
any stream brief.

## 7. Acceptance

The checklist on #679 becomes this section at dispatch, written there by
the coordinator in place of P1's generated ones. Every checkbox names the
artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-app-views-scrapers/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `second-opinions/`, `stage-a/` to `stage-e/`, `tools/` and `guest-cycle/` (`ls` of the folder in the hand-back).
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-app-views-scrapers/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), and the same with `--issue <audit issue>` prints `PASS`; Q1 to Q7 are answered in `04-analysis.md` and every punch item carries `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); its probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the scan block with every hit dispositioned by file:line (library plumbing / macro name / identifier / setting name) and no value, every trimmed file and range named, `httplib.h` by ranges only; `00` shows exactly two keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #585, #649, #665, #667, #668, #673, #678, #1186, #1191, #1192, #1205, #965, #1190, #156, #791, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail; the issue is closed by the coordinator at acceptance.
- [ ] `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in #679's header carry the lane's commits; the ES read is on the pin's bytes for the 42 files (`git -C <W> diff --stat 16dbac5211 <reviewed-at-es> -- $(cat .qa-scratch/t32/paths.txt)` empty before stage E) and nothing under the distribution's `packages/`, `projects/` or `tools/` changed at any stage against the lane's own dispatch tip (the pointer's merge hash, never `2174265e9c`).
- [ ] `01-research-notes.md` § Scope records § 2's block with its exact output lines (`selects 1 paths 42 lines 17311 {'shipped': 42} {'upstream-carried': 36, 'fork-own': 6}`; `{'c++': 20, 'c-header': 22}`; `fork-own lines by inventory tier: 4005`; `wc -l` 17,306 and `grep -c ''` 17,311 with the five files without a trailing newline; 42 at the merge base and 42 at the base; 6 files 168 added 46 removed, twice -- or the deltas beside them) and names `cada856d86` as the merge base against `rocknix/master` with `bccd715707` as its parent.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `42`; its tier columns read fork-modified 6 / upstream-carried 36 / fork-added 0 and inventory 6 / 36.
- [ ] `02` § The runs records the counts with both rules where they differ -- `_("` 58 lines in 9 files and 70 occurrences; `HttpReq` 83 lines in 14 files and 95 occurrences; `exists(` 49 lines in 6 files, 50 occurrences, 0 uncached; `new Gui` 19 with 8 `GuiMsgBox`; `std::thread` 13 in 5 files; es-core include edges 143 of 410; the T21-class uses 51 lines in 14 files; 47 include lines from 23 outside files -- each as a command's own output line, or the lane's figure with the command that differs named.
- [ ] `02` § The views, § The scrapers, § The services, § The reads and § The bounds are each generated or asserted by a script under the audit folder's `tools/` that names its row count ("generated, asserted"), and `02` § The runs records each script seen to exit 1 on a constructed drift before it was trusted.
- [ ] `02` § The reads has one row per `exists(` line (49): the file or line read, its writer while ES runs, cached or not, and what a remembered miss reads as; `DetailedContainer.cpp:903` and `:916` and `Scraper.cpp`'s 25 among them with a disposition each.
- [ ] `02` § The merge debt is one line naming `cada856d86` as the merge base with `rocknix/master` (`f6c542872e`), `bccd715707` as its parent and the stale `upstream/master`, the 0 upstream commits on the 42 paths of 14 since the base, and the fork's six files with their numstat pairs; the T21 deltas (`Scraper.cpp` 28/8, `Scraper.h` 5/0, `ScraperReplies.{cpp,h}` 51/22 new) recorded as inherited with their commits.
- [ ] `02` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason; the harness sweep's empty result, the menu-map check's line, both `es-untranslated` lines, the non-ASCII grep's 0 (adjacency by `-F`), the stand-in syntax check's rc on `Scraper.cpp` and the unit build's `TOTAL: N test cases in B binaries` line with 0 failed are among them; every unit case the lane wrote has its FAIL-then-PASS pair recorded against the unfixed extract first, the six FAIL-at-pin leads by name.
- [ ] `02` § The guest cycle records the window the coordinator granted on #679 (the comment's time; the START and RETURN posts with their first-line contract and censuses, and the host file's lines beside them), the image by file name and `BUILD_ID` read from the guest at 640x480, G-01 to G-11 with their frames read back at EN and FR and each frame labelled by side (`image` or `pin-binary`), G-05's outcome words and line 4, G-06's B landing on the only button in both locales, G-08's four lines with its 403 line as `CANNOT` (no forward), G-09's stale-read positive, G-07 and G-10 as `CANNOT` with the reason, the disk retired with path, size and sha, the leftover check (`qemu 0, compilers 0`), and the window closed inside its bound plus grace.
- [ ] `00-running-log.md` shows no image build, no fetch (the council runtime from `npm install --offline`; `rocknix/master` and T21's ES tip read from the shared refs), no handheld, the owner's accounts never named or used, no hosted account, no M7 root, worktree or prep directory, the guest only inside the granted window, two keyed invokes and every other council call keyless, and nothing written under the ES worktree before stage E (`00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q7 are answered at their lines; every `bug` states its trace, its `Already written:` line and its VM line in one of the named families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` in the shape the lane writes; the items § 2 lists under *do not re-find; take up* (#1191's caller half, #1205, #1154, S12, #1186, #965, `SystemView.cpp:1616`, #1187/#1192, T2's four, T20's two, #246's holders) each have a disposition at their lines, and every collision with T21's `Scraper.cpp` lines is named.
- [ ] Every proof in `02` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; `02` § What T33 to T37 inherit lists § 5 item 3's seven items with their lines.
- [ ] The retro exists at `docs/retros/<date>-m6-es-app-views-scrapers.md`, is posted on #679, says what the slice did to the two time-to-play numbers (the list's press to `launch`, the SCREENSHOTS grid's populate and the carousel's `populate` named with what they cost on the guest; cited from `docs/vm-qa-log.md`), and what T33 to T37 inherit.
- [ ] `tools/es-menu-map-check --es-src <W> --ref <reviewed-at-es>` prints `0 missing` on the branch as handed back **after `docs/es-menu-map.md` takes a section for the five view styles, the row that picks them and the SCREENSHOTS list** (in the same commit as any row a stream touched, D-UI-039), and `SystemView.cpp:552`'s computed title has its disposition in the map, in `## Not mapped` with a reason, or in a punch item saying which (#965 cited).
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch and the ES fork's `.githooks/pre-push-test` on the ES branch before the hand-back merge, and again on the coordinator's simulated merge; every fix on the ES branch has, recorded beside its commit, the covering unit case's PASS line (and its earlier FAIL), its French in the same commit where a sentence changed, `tools/es-syntax-check` PASS where a toolchain exists or else the stand-in `g++ -fsyntax-only` rc (or `CANNOT` with the missing header named), and a clean non-ASCII grep over its added lines.
- [ ] The unit build's `TOTAL: N test cases in B binaries` line is quoted in `02` § The runs and in the hand-back from the script's own output, with 0 failed in every binary's summary after the fixes and the six FAIL-at-pin leads' earlier FAIL lines beside it.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back); the stage-D pause; an explicit maintainer
pause on #679; a blocker named on #679 (the seat failing its provenance
gate twice, a packet scan hit that is a value, two commands that disagree,
a block whose output differs from § 2's beyond the deltas it records, an
upstream-carried file that is not byte-identical to `rocknix/master`, a
pointer line that names the predecessor slice (§ 10); **not** the host's
missing toolchain, which § 5 names and the `CANNOT` forms absorb, **not**
the empty harness floor, which § 5 says the lane builds, and **not** the
no-NIC guest's inability to show a scraper's success path, which § 5
names as the floor's limit); an ES worktree that differs from the pin on
any of the 42 files at stage A; or an execution limit, stated as such with
the running log current. A checkpoint is not a stop. An idle session says
it is idle on #679, **and does not end a turn on a post that asks nothing**:
a turn ends on a post or a commit, never on "next is ..." (the T26 lane
sat 28 minutes on exactly that, friction 2026-10-27 10:48 UTC).

## 9. Ceremonies owed

- A work-log entry per session headed `#679`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #679` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window granted on #679; no account needed; nothing on a
  handheld; D-QA-015/016).
- The mini-retro at stage G, posted on #679, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (two
  expected, both put to the coordinator at the pause, never decided by the
  lane: whether a media download that did not arrive counts as an error
  or as scraped, Q3's L-07; and whether `SKIPPED - YOU CANCELLED IT` over a
  finished run is a reword or a guard, Q1's L-02 beside T31's Q5). **The
  highest IDs the register on the coordinator's branch names at this
  version are D-WORKFLOW-212, D-NET-017 and D-CLOUD-186** (the last three
  decided rows; `tools/register-check` is the proof; D-WORKFLOW-188 is on
  the P1 branch only and the merge unites them); a row this slice forces
  takes an ID the coordinator assigns on #679.
- `tools/ceremony-check --gate` before every push of the distribution
  branch and the ES fork's `.githooks/pre-push-test` after an ES change;
  never `--no-verify`; a merge with conflicts is checked for markers; the
  ledgers united by whole entries; **a commit names its paths**; anything
  temporary under `/workspace/tmp/m6-t32/` after `df -i`, never `/tmp`;
  the window's record kept on the branch, the guest disk retired after it
  with the retirement recorded in `00` (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never
  inside a `bash -c` script**.
- **The same-commit rules, stated once:** a row added, moved or renamed
  updates `docs/es-menu-map.md` in the same commit and
  `tools/es-menu-map-check` passes before it (D-UI-039); a sentence added
  or changed carries its French in the same commit (D-UI-051).
- A fixture that rewrites no path, in a bubblewrap sandbox started with
  `--clearenv`; the walks' steps under the audit folder's `stage-e/walks/`,
  never under `tools/`; the non-ASCII grep over a stream's added lines
  (`git diff -U0 HEAD -- <file>`, its `+` lines), an upstream hit recorded
  and not fixed; a generator seen to exit 1 on a constructed drift before
  its table is trusted.
- **Every edited file checked for an unfilled placeholder before its
  commit**: `/usr/bin/grep -c -E '__[A-Z]+__|\b(COHASH|MERGE_HASH|TIPHASH|V2HASH)\b'`
  is 0 on the pointer, the running log and every artifact (the T31
  dispatch entry shipped with its `__TS__`/`__URL__` placeholders
  unfilled, friction 2026-10-27 12:02 UTC; this brief's own four names,
  § 1, would pass the first alternation unseen, so the pattern names
  them).
- Commit messages `docs: ...` on the distribution branch, with `Refs #679`;
  on the ES branch the package's convention, `Refs #679, #<bug>`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#679's checkboxes against their artifacts; the lint's `PASS` line on the
default phase and with `--issue`; `review-plan.json` and the two
provenance files (read directly) and the manifest's scan block; the audit
issue's checkboxes all at an outcome; the coverage table's row count (42),
the generated sections' asserted counts, § The reads' 49 rows, § The
bounds' 7, § The merge debt's one line; every Q bug with its three lines;
**re-running on clones of both branches at their tips under
`/workspace/tmp/m6-coordinator/`: the membership block, every § 5 run in
full and the unit build script** (no guest: the window's record is read,
not repeated); `register-check` on a simulated merge with the
coordinator's tip; the retro's answers; the five checkers' exit codes; the
collisions named against T21's `Scraper.cpp` lines. The lane posts one
hand-back comment naming **both tips** and each artifact by path, writes
`reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` into
#679's body, then says it is idle. After acceptance the coordinator closes
the audit issue, prompts the lane for `audit-completion.json` and the lint
against **the audit issue**, merges the distribution branch in its turn
after the M7 candidate with the pin moved to the ES branch's tip in the
same integration commit (the ES package built before it lands; T21's
`Scraper.cpp` deltas reconciled there), regenerates the ledgers, posts any
#585 lines in the shape the lane wrote, files any Backlog the hand-back
names, and closes #679 when every row is proven -- which is also when
#649, #665, #667, #668 and #673 close (§ 1); the interface epic #700
closes when its slices have.

**The pointer the lane checks at stage A, line by line.** The seeded
pointer `.github/sessions/saved-session-state-feature-m6-es-app-views-scrapers-679.md`
is written by the coordinator from T31's, and T31's was seeded with a
sentence of T26's still in it. So before the first command after `cat`
the lane reads these eleven keys, each against the one value that would
be the seeding error, and reports any that name the predecessor on #679
before going on:

| Key | Must read | The seeding error reads |
| --- | --- | --- |
| `Branch (distribution):` | `feature/m6-es-app-views-scrapers-679` stacked on `feature/m6-p1-survey-641` at `2174265e9c` | `...-es-pages-678` |
| `Worktree (distribution):` | the § 1 path ending `m6-es-app-views-scrapers-679` | `m6-es-pages-678` |
| `Worktree (EmulationStation):` | `W` of § 1, at the pin `16dbac5211` | another lane's checkout |
| `Executor:` | Opus 5.5 at high effort, the session the dispatch comment on #679 names | T31's session |
| `Epic:` | #700; T2, T18, T20, T21, T26 accepted and open until the integration merge; T31 in flight; T33 to T37 and T44 after | "T31 accepted" or "closed" |
| `Depth:` | one seat, GPT-6 Astra at `max`; the six fork-modified files whole (4,005 lines), the 36 upstream-carried by cited ranges, `httplib.h` never whole | twelve fork-touched files, 76 paths |
| `The lens:` | cost against value over 42 paths under `views/`, `scrapers/` and `services/` | the manager, the BIOS check |
| `The rule:` | nothing under the distribution's `packages/`, `projects/` or `tools/`; nothing in the ES worktree at stages A to D | -- |
| `The host:` | the shared log and one guest window of 35 + 5 minutes | a 45-minute window |
| `Register:` | D-WORKFLOW-212, D-NET-017, D-CLOUD-186 | an older triple |
| `The brief:` | `docs/reviews/briefs/es-app-views-scrapers.md` at `V2HASH` (§ 1: filled by the dispatch comment) | `es-pages.md`, or the literal word `V2HASH` |

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro takes a T32 kickoff addendum written by the coordinator with
this version, and the stranger's proof of version 1 has run; its findings
are below. This brief's hash at dispatch is `V2HASH`.

**What never runs in this slice:** an image build, a compiler beyond the
host's `g++ -fsyntax-only` (plain or with T21's stand-ins) and the
generated test build, a fetch (the council runtime from `npm install
--offline`; `rocknix/master` and the lanes' ES tips from the shared refs),
a handheld, the owner's accounts or any hosted account, a host listener on
a privileged port, a guest before a grant on #679, M7's roots, worktrees
or prep directories, a change outside the 42 files, `docs/es-menu-map.md`,
the French catalog and the audit folder except under a stream brief, a
move of the pin, a line in `ViewController.*`, `ScreenScraper.*`, `guis/`,
es-core or `CollectionSystemManager` without the pause's ruling on its
owner.

## Version 2: what the stranger's proof of version 1 corrected (2026-10-27)

A reader with no context ran the membership block, the thirteen § 1
commands and the § 5 runs block from the P1 clone and the `qa-integration`
checkout at the pin (14 shell commands, every file written to scratch,
neither tree touched), settled the four unverified items, and made 48
spot checks, 36 of which held. The membership block reproduced exactly;
of the § 5 expectations three differed and three cannot run before
dispatch. Everything else held except these, corrected above in place
(the line is version 1's at `2ed286145d`):

1. `:39-40`, `:1357-1358`: "accepted and closed out" -> accepted, the issues open until the integration merge -- `gh issue view` 649/665/667/668/673 all OPEN.
2. `:118-119`, `:1173-1174`, `:1366`, `:1375`: `COHASH`/`MERGE_HASH`/`TIPHASH`/`V2HASH` undefined -> defined once in § 1 as the dispatch comment's and the pointer's values, and named in § 9's placeholder pattern -- `git diff --stat TIPHASH HEAD` fails `fatal: bad revision`; the `__[A-Z]+__` check printed 0.
3. `:1062-1065`: `IGDBScraper.cpp:185` -> `:187`; `HfsDBScraper.cpp:222` -> `:195` (and `:224`) -- `git grep -n` of the two host names; `:185` is `data += " limit 10;"`, `:222` is the token date.
4. `:353`, `:782`: `isRunning()` at `h:80` -> `h:77` -- `h:77 static bool isRunning()`; `h:80` is `pause()`.
5. `:388-389`, `:851-852`, `:1084`: `_("INVALID CREDENTIALS")` at `:167-171` -> `:167-172`, the string at `:172` -- `git grep -n -F`.
6. `:529`: "both `Retry-After` reads, `:356` and `:628`" -> `:351` and `:618` at the pin; `:356`/`:628` are T21's branch lines after its +28/-8 -- the pin's `:356` is blank, `:628` is `}`; `s13-checks.txt:98` is the branch's.
7. `:526`: `44d3c7e25` "+9/-2" -> +7/-2 -- `git show --numstat 44d3c7e25 -- es-app/src/scrapers`.
8. `:533`: `3ae9610b0` "+17/-4" -> +13/-4 -- `git show --numstat 3ae9610b0`; the three commits sum to 28/8.
9. `:310`, `:1209`: "the 16 routes `:149-599`" -> 16 distinct paths over 27 registrations at `:149-803` -- the registration lines end `... 599 632 711 786 803`; the delete route at `:738-755` was outside the old range.
10. `:939`: `md_image` at `:464`, `:61`, `:534` -> `:61`, `:464`, `:1060` -- `git grep -n -F md_image` on `DetailedContainer.cpp`.
11. `:806`, `:934`: "the views' `getCursor()` at 20 lines" -> 20 in `ISimpleGameListView.cpp`, 30 in 9 of the 42 files -- `git grep -c -F 'getCursor()'` over `$FILES`.
12. `:487`: the `manager-gb` baseline shots "at 640x480" -> 1280x800; no 640x480 list baseline exists (#1141) -- `claims.txt:38-39` read `0 0 1280 800`.
13. `:1086`: "`vm-qa:349` forwards SSH only" -> `generic-x64-vm:380-383` forwards SSH and the profile's services, never 1234; `vm-qa:479` reaches `127.0.0.1:1234` over SSH; G-08's 403 line is `CANNOT` from the host -- `grep -n 1234` on the VM script prints nothing; `vm-qa:349` is the `link` suite's case arm.
14. `:1134`: the T21-delta run "expect 4 rows" -> 6 rows, the pathspec being the three directories: `ScreenScraper.cpp 17 16` and `ViewController.cpp 8 2` beside the four -- the command's own output.
15. `:1146`: "Scraper.cpp 337 372 607 631 among them" -> `336 371 374 612 630 633` among the 17 printed (the pattern hits the `setStatus`/comment lines beside the leads'); `return false;` in `IGDBScraper.cpp` gains `230` -- the real printed lists.
16. `:1168`: plain `g++` "SDL expected for ThreadedScraper.cpp" -> `es-core/src/HttpReq.h:5:10: fatal error: curl/curl.h: No such file or directory`, rc 1 -- measured on the pin's bytes; the SDL figure had been measured on `GuiMenu.cpp` and `GuiSaveState.cpp`.
17. `:1150`: the parse run named no expectation and missed `atol(` -> `std::stoi(` 3 in 1, `std::stoul(` 0, `atoi(` 0, `toInteger(` 6 in 5, `atol(` 1 at `GameNameFormatter.cpp:171` -- the loop's own lines.
18. `:1142-1143`: "`postToUiThread(` the lane's count" -> 13 lines in 3 files (`HttpServerThread.cpp` 10, `DetailedContainer.cpp` 2, `ThreadedScraper.cpp` 1) -- `git grep -c -F`.
19. `:1165`: the `cada856d86` line of `tools/es-untranslated` -> `703 fork string(s) in the source, 703 with French, 0 without`, rc 0 -- the tool's line.
20. `:343`, `:727`, `:1162`: "po L115 empty" -> L115 the msgid, L116 the empty `msgstr` -- `sed -n '115,116p'`.
21. `:909-910`, `:1153`: "each view's override" of `getHelpPrompts()` -> two definitions, `SystemView`'s and `ISimpleGameListView`'s; the five styles inherit -- `git grep -l -F '::getHelpPrompts('`.
22. `:961-962`: the unverified httplib version grep -> no version line and no `CPPHTTPLIB_VERSION` (0 hits; the header's copyright is 2020); currency judged by content -- the named grep returned an OpenSSL comment at `:212`.
23. `:963-964`: the unverified `CPPHTTPLIB_OPENSSL_SUPPORT` item (the ES recipe and `es-app/CMakeLists.txt`) -> `CPPHTTPLIB_OPENSSL_SUPPORT` defined nowhere (0 hits in `es-app/CMakeLists.txt`, `CMakeLists.txt`, `HttpServerThread.cpp` and the recipe); the server is plain HTTP -- the four greps.
24. `:1080`: the unverified view-style row (its path and values) -> THEME CONFIGURATION (`GuiMenu.cpp:8668`), GAMELIST VIEW STYLE at `:8691`/`:8729`, values `automatic basic detailed video grid gamecarousel` (`:8685-8735`); per list SELECT > VIEW OPTIONS (`GuiGamelistOptions.cpp:194`/`:232`, no write of `GamelistViewStyle`) -- the lines read.
25. `:1439-1442`: four open items -> `FileSorts.h:23 RELEASEDATE_DESCENDING = 11` (3.32 stands); `UIModeController.cpp:72` resets the counter on a wrong press (3.33); `FileSystemUtil.cpp`'s writers reference the cache at `1051`, `1067`, `1097`, `1445`, `1457-1458`, `1506-1507` (L-09); #1206 OPEN, #300 CLOSED, #299 CLOSED, #585 OPEN with their titles -- the lines and `gh issue view`.
26. `:527`, `:713`: `tests/unit/ScraperRepliesTests.cpp` -> `es-app/tests/unit/ScraperRepliesTests.cpp` (the ES tree also has a top-level `tests/`) -- T21's branch.
27. `:899-902`: L-05's call at `Scraper.cpp:638` -> `:640`, under `:638`'s `if` -- `removeHtmlTags` at `227 381 387 640`.
28. `:1474`: "the 900 to 1,100 lines asked for" -> dropped; no such figure exists in `plan-for-the-plan.md`.
29. `:1007` and every `3.x` citation: the floor's leads were cited by number from a file in no tree -> the 35 are tabled in § 4 with their lines.
30. `:1051`: "T13's conditions" unresolved -> T13 is #660; the conditions are spelled out in § 5 item 2.
31. `:1084`: "B lands on OK" -> B lands on the only button: the boxes at `ThreadedScraper.cpp:299` and `:314` name none -- the `GuiMsgBox` calls read whole.
32. `:28-30`, `:193`: the two membership sources' globs -> `order.md:607` prints one negative glob, `slices.json` two, and `slices.json` is the membership's source (§ 1) -- both files at `2174265e9c`.
33. `:13` and the last section: "seven unverified" -> four items (`:922`, `:961`, `:963`, `:1080`; the other three lines were the definition and two back-references), all settled here -- the proof's grep of the bracketed form.
34. `:1155`, `:1172`: the two generator calls in the runs block run at stage A as written and fail -> marked STAGE C, with the removal check marked STAGE A after the pointer -- the glob matches nothing until the lane writes the scripts.

Settled without correction: `Scraper.cpp:596`, `:337`, `:372-376`,
`:607-635`; `GamesDBJSONScraper.cpp:605`/`:607`; `IGDBScraper.cpp:143-144`;
`ThreadedScraper.cpp:53`, `:179`, `:235`, `:241-242`, `:325`, `:331`,
`:335` and the two boxes at `:299`/`:314` (the digests' `:300` and
`:313`/`:314`); `SystemView.cpp:233-234`, `:272-278`, `:331`, `:552`,
`:1616`; `HttpServerThread.cpp:74`, `:127-138`, `:574`, `:615-630`,
`:754-755`, `:821-828`; `HttpApi.cpp:102`, `:170`, `:210`, `:258-260`,
`:332`; every rule-file, menu-map, vm-qa-log and lane-audit line cited;
the register's highest IDs; the credential-shaped lines and the macro
lines by file:line; `f7c16144d`'s stat; the rapidjson recipe and patches.
Cut on the proof's advice (about 350 lines): § 1's predecessor routing
(now § 2's take-up list alone), § 2's leads paragraph (now the index) and
counts paragraph (now § 5's comments and § 7's checkbox alone), four of
the five merge-debt restatements, § 3's rule glosses (now the table), § 6
against § 7, the pointer paragraph (now the eleven-key table), and the
"Version 1" section, replaced by this one.
