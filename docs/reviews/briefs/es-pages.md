# Review brief: M6.P2 T31, EmulationStation's other pages (#678)

**Version 1, 2026-10-27, the coordinator's draft** (D-WORKFLOW-189; the
stranger's proof runs before dispatch and version 2 records what it finds,
`docs/reviews/plan-for-the-plan.md` § 6b). Written from five read-only
research digests (the coordinator's scratch files, not in any tree; every
figure they gave is reproduced by a command below), the order's § T31, #678's
body, and what T2, T20 and T21 routed to this slice by name; the figures were
produced at the hashes they name with `/usr/bin/grep`, never the shell's
function (#1138). The last section lists every figure this version could not
copy from a recorded output and every judgement it made.

## 1. Identity

- **Issue:** #678 `M6.P2 E339/T31: interface: EmulationStation's other
  pages`, retitled `M6.P2 E700/T31: interface: EmulationStation's other
  pages` at dispatch (`milestone-phase-naming.md`; the body says *"under
  epic #339 until this area's epic is filed"*, and #700 is filed), slice
  `es-pages` (`k: 31`) in `docs/reviews/slices.json`, thirty-first in
  `docs/reviews/order.md` (`order.md`, `slices.json` and `inventory.json`
  are the P1 branch's, which the lane's worktree is stacked on -- a reader of
  the coordinator's branch alone cannot open them; its § T31 paths line: *"76
  paths, 15,537 lines, 15,537 read, of which 4,230 fork-own; 0 patch and
  config lines; reach shipped 76"*; its `why`: *"the remaining pages under
  `guis/`: the fork-touched ones read line by line, the upstream ones checked
  against `rocknix/master`"*; kind currency; lens new functionality; depth
  Independent, *"an ordinary code slice"*; closing evidence *"audit folder,
  lint PASS, punch list through Phase 7"*). **Epic:** #700 (the interface:
  T2 #649 and T18 #665 accepted and closed out; T20 #667 and T21 #668
  accepted, their errata in the futro dated 2026-10-26 and 2026-10-27; T26
  #673 in flight, its branch holding `00` and `01` of its audit folder; this
  slice; T32 to T37 and T44 after), whose futro
  `docs/futros/2026-10-23-m6-interface.md` takes a T31 kickoff addendum
  written with this version. **Milestone:** M6. **Predecessors:** #346,
  #641, **T2 #649** (the launch path: four leads routed here by name -- the
  relay session and the spectator mode in `GuiNetPlay.cpp:1021` and `:1058`
  (#776, its PL-010); `GuiSaveState`'s callers of the now-truthful
  `copyToSlot`/`remove` (PL-016, ES `f11e7528a`; #782 open; walk W-5 named
  and not run); the netplay nickname default moving into
  `GuiNetPlaySettings.cpp:26` and `GuiGameOptions.cpp:203` (PL-031,
  `deferred:#678`); the off-by-one at `GuiGamelistOptions.cpp:148` (PL-005's
  sibling) -- plus FD-14's dialog words at `GuiGameOptions.cpp:253` and
  FD-21's call to grade, `GuiCollectionSystemsOptions` →
  `FileData::resetSettings`), **T20 #667** (the hasher constructed from
  `GuiHashStart.cpp:85` and `GuiNetPlaySettings.cpp:59` on the interface
  thread: #1170 the lifetime, #301 the constructor's fetch; cited, not
  re-found), **T21 #668** (the base this slice's pages are built on: the
  stores' keys and `addSwitch`'s bool at its `02:546`; `GuiSettings.cpp`'s
  `addInputTextConfigRow` and #1185; `GuiBluetoothDevices.cpp:127/:150` and
  #1212; `GuiBluetoothDevices.cpp:117-121` L-33; `GuiScraperStart.cpp:413-420`
  and #1193; `GuiScraperStart.cpp:99` and #1191; `GuiKeyboardLayout.cpp:164`'s `writeAllText` call (the in-place `fopen "wb"` is `FileSystemUtil.cpp:1434`, T21's file; the site is Backlog #1186's); `GuiSaveState.cpp:33`'s `isFlockHeld`; its ES branch's
  `a73ed9efc` touching `GuiBios.cpp` for PL-14/#1202), **T26 #673** (GuiMenu,
  the file every page here is reached from; its `02` § What T31 to T37 inherit
  is owed and not written at this version -- read at dispatch if it has
  landed, else mid-run when it does), **T18 #665** (the cloud pages: nothing
  routed here, verified by its headings), **T1 #648** (`rocknix-systems`,
  which the BIOS check runs), and the menu map `docs/es-menu-map.md`
  (D-UI-039: a row added, moved or renamed updates it in the same change;
  `tools/es-menu-map-check` is the closing evidence the order names for the
  interface slices). **Beside it:** whichever interface slice holds the
  running session; the host shared by `/tmp/m7-m6-host-coordination-20261023.txt`;
  a window for this slice is asked for on #678 and granted there in the queue.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of
  scope: those are the coordinator's, reached through #678, one question
  at a time. What it does file: its own audit punch-list issue (stage D)
  and a `bug` issue for a defect it proves, with its trace and `Already
  written:` line (D-WORKFLOW-187). A fix lands only under a stream brief
  the coordinator writes at the stage-D pause, **on the EmulationStation
  branch**. **Sixty-four of the 76 paths are byte-identical to ROCKNIX's
  master** and twelve are the fork's (three files it added, nine it
  modified: 1,207 lines added and 129 removed against the merge base). A
  defect in a line the fork wrote is the fork's to fix; a defect in an
  upstream line is a contained fix under `bugs-are-agent-first.md` rule 6 (`:76`) and a #585 line (D-WORKFLOW-164, never sent, D-WORKFLOW-165).
  D-UI-079's lanes (`engineering-practices.md:12`): the save state manager,
  the scrape page and the scraper's fork rows, the BIOS check, the image
  viewer's aspect, the Wi-Fi executor are the lanes the fork works in; an
  upstream page's *behaviour* -- the content downloader, the theme
  installer, the Bluetooth pages, netplay, the metadata editor, the key
  mapping editor -- is read for brittleness and left as upstream has it,
  and a defect in one is still ours to close when the fix is contained
  (rule 6). The read is the pin `16dbac5211`'s bytes; M7's worktrees are
  never read.
- **Two worktrees, one session.** The distribution's
  `feature/m6-es-pages-678` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-pages-678`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip `COHASH` merged in as
  `MERGE_HASH` and the lane's pointer seeded (the two hashes in the dispatch
  comment on #678; the lane's own tip is `TIPHASH`); and the EmulationStation
  fork's `feature/m6-es-pages-678` at
  `/home/max/Development/emulationstation-next.worktrees/m6-es-pages-678`,
  cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`**
  and clean until stage E: the sources are read and the fixes are made
  there, and the pin is not moved by the lane. The other ES checkouts under
  `~/Development/emulationstation-next.worktrees/` are other lanes' and
  M7's: read with `git -C <checkout> show <hash>:<path>` only; `rocknix/master`
  is read from the shared refs, never fetched (`upstream/master` in that
  repository is a stale copy 15 commits behind -- § 2). Until the dispatch
  comment exists the pointer is not seeded and nothing starts.
- **Depth: Independent** -- one seat from another lab (plan § 6c,
  D-WORKFLOW-137; `adversarial-council.md`: an Anthropic-led audit's
  reviewer is pinned GPT-6 Astra; no Gemini seat): Astra at `max` over a
  trimmed, scanned packet (D-WORKFLOW-195 -- the twelve fork-touched files
  whole, 4,230 lines, and of the 64 upstream-carried files only the ranges
  the questions cite; the manifest names every trimmed file and range), a
  probe then one refutation (one in-call retry allowed); `review-plan.json`
  records depth `independent` and the one reviewer with its served model;
  **exactly two keyed `tools/council/run invoke` calls**, every other
  `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`; the runtime
  from `npm install --offline`, no fetch. The packet is scanned before it
  leaves: this slice names `ScreenScraperUser`, `ScreenScraperPass`,
  `ScreenScraperDevId`, `ScreenScraperDevPass`, PLAYER PASSWORD, CLIENT
  SECRET and the netplay password by setting name and label, so the manifest
  records every scan hit and its disposition, and a hit that is a value stops
  the packet.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the distribution worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-pages-678
cat .github/sessions/saved-session-state-feature-m6-es-pages-678.md           # the pointer: the dispatch's two hashes
git status --short | wc -l                                                     # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                 # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-pages-678; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                  # the pin; 0
git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10                       # cada856d86: the merge base with ROCKNIX's master (not bccd715707, § 2)
git -C "$W" rev-parse --verify rocknix/master | cut -c1-10                      # f6c542872e, read from the shared refs
git show origin/feature/m6-es-launch-path-649:docs/audits/2026_10_23-epic-m6-es-launch-path/05-punch-list.md | /usr/bin/grep -c '^## PL-'   # T2's punch list is reachable (36): the leads routed here are at its :109, :295, :614-615, :645, :660
tools/register-check >/dev/null && echo register-ok
tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200             # who holds the host: no guest before a grant on #678
```

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{inventory.json,slices.json}`; the slice's `select` is one
object with one positive glob and four negative ones; `W` is the ES
worktree):

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k = [s for s in sl["slices"] if s["k"] == 31][0]; sels = k["select"] if isinstance(k["select"], list) else [k["select"]]
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
t31 = []
for sel in sels:
    for r in pick(sel):
        if r not in t31: t31.append(r)
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("selects", len(sels), "paths", len(t31), "lines", L(t31), dict(collections.Counter(r["reach"] for r in t31)), dict(collections.Counter(r["tier"] for r in t31)))
print(dict(collections.Counter(r["language"] for r in t31)))
print("fork-own lines by inventory tier:", L([r for r in t31 if r["tier"] == "fork-own"]))
os.makedirs(".qa-scratch/t31", exist_ok=True)
open(".qa-scratch/t31/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t31, key=lambda r: r["path"])))
for r in sorted(t31, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
PY
wc -l .qa-scratch/t31/paths.txt     # 76
W=/home/max/Development/emulationstation-next.worktrees/m6-es-pages-678; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
while IFS= read -r p; do git -C "$W" show "$PIN:$p" | wc -l; done < .qa-scratch/t31/paths.txt | awk '{s+=$1} END {print "wc -l lines", s}'           # 15526
while IFS= read -r p; do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done < .qa-scratch/t31/paths.txt | awk '{s+=$1} END {print "grep -c lines", s}'   # 15537
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t31/paths.txt | wc -l   # 73: the three fork-added files are not
git -C "$W" diff --numstat "$MB" "$PIN" -- $(cat .qa-scratch/t31/paths.txt) | awk '{a+=$1; r+=$2; n+=1} END {print n, "files", a, "added", r, "removed"}'   # 12 files 1207 added 129 removed
```

Expected, at `2174265e9c` (the coordinator ran it on this tree's copy of
that commit on 2026-10-27, `W` the `qa-integration` checkout at the pin):
`selects 1 paths 76 lines 15537 {'shipped': 76} {'upstream-carried': 64,
'fork-own': 12}`; languages `c++ 37, c-header 39`; `fork-own lines by
inventory tier: 4230`; `wc -l lines 15526`; `grep -c lines 15537`; the
merge-base count **73**; **12 files 1207 added 129 removed**.

**Three things the figures hide, settled here so the lane does not
re-derive them.** (1) **The inventory counts lines as `grep -c ''` does**,
the unterminated last line included: 11 slice files end without a newline
(`GuiBatoceraStore.cpp`, `GuiBezelInstaller.cpp`, `GuiFileBrowser.cpp`,
`GuiGamelistFilter.cpp`, `GuiGamelistOptions.cpp`, `GuiHashStart.cpp`,
`GuiImageViewer.h`, `GuiMetaDataEd.cpp`, `GuiNetPlay.cpp`, `GuiSaveState.h`,
`GuiThemeInstaller.cpp`), so `wc -l` sums to 15,526 and `grep -c ''` to
15,537 -- the same bytes, two counting rules; a figure in `02` says which.
(2) **"4,230 fork-own" is the lines of the twelve files the fork touched,
not the lines the fork wrote.** The inventory's `tier` is `fork-own` for
any path the fork added or changed: three files are the fork's own
(`GuiScraperRun.cpp` 258, `GuiScraperRun.h` 67, `WifiScanProcess.h` 202 --
527 lines) and nine are upstream pages carrying fork edits (3,702 lines at
the pin); the fork authored about 1,207 lines in this slice, 129 removed,
by `--numstat` against the merge base; the twelve files hold 4,229 lines by
`wc -l` and 4,230 by `grep -c ''` (`GuiSaveState.h` is one of the eleven).
`02` § Coverage carries both tiers: the inventory's two and the read's
three (fork-own 3, fork-modified 9, upstream-carried 64). (3) **The merge
base with ROCKNIX's master is `cada856d86`, not `bccd715707`.**
`rocknix/master` is `f6c542872e3850c5f432929ead219547a897cd4a` (2026-10-23,
*Merge pull request #54 from porschemad911/s922x-suspend*); the pin's merge
base with it is `cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` (2026-09-28,
spycat88, *Refactor wifi menu and add support for saving multiple
profiles*), one commit after `bccd715707` (`rev-list --count bccd..cada` =
1), which is the base the earlier ES briefs named because the repository's
`upstream/master` ref was never fetched and still points at `bccd715707`,
15 commits behind `rocknix/master`. For this slice the difference is
nothing: `cada856d86` touched `GuiMenu.cpp` (3/10), `GuiMenu.h` (0/2),
`GuiWifi.cpp` (116/27) and `GuiWifi.h` (3/5), all excluded. The lane names
`cada856d86` in every merge-debt figure and records that `bccd715707` is an
ancestor of both the pin and the base.

**`WifiScanProcess.h` is in scope.** The exclusion is `GuiWifi.*` -- GuiWifi
followed by a dot -- so the Wi-Fi picker's argv executor (#577, fork-own,
202 lines) falls to this slice by the glob while its only callers
(`GuiWifi.cpp:540`, `:548`, `:567`) are T21's and T26's reading. It is read
here as the model T21's quoting rule names (`02:545`: a string from outside
the program goes to `Utils::String::shellQuote` or to an argv executor,
never double quotes) and as #1192's named precedent.

**The files, read whole** (lines at the pin by `wc -l`; the fork's
`--numstat` against the merge base; the fork's non-merge commits
`bccd715707..PIN` on the file):

| File | Lines | +/- | Commits | What it is |
| --- | ---: | ---: | ---: | --- |
| `GuiSaveState.cpp` / `.h` | 612 / 75 | 330/23 / 23/0 | 25 | the SAVE STATE MANAGER: upstream's sheet turned into a page that fits two-line labels at 640x480, draws tiles at the system's aspect and the capture's turn (`DisplayAspect::forGame`, `:76-83`), says TODAY / YESTERDAY / date "at" time (`:303-307`), refuses DELETE and COPY while the saves tree is being synced (`savesTreeBusy`, `:18-35`: `ThreadedCloudSync::isRunning()` at `:28`, then `isFlockHeld("/var/run/cloud_sync.lock") && !holdsTransferLock()` at `:33`), deletes on a worker (`SaveStateBookkeeper::deleteLater`, `:480`) and rebuilds only when the disk disagrees with the page (`update`, `:538-575`, comparing `filesOnDisk()` with `mShown` when `completed()` moves), draws its own help bar on full-screen-menu panels (`render`, `:386-399`); WINDOW_HEIGHT 0.40 → 0.55 (`:43`); 19 `_("` in added lines, 10 distinct, all with French; dialogs `:442`/`:503` single-OK, `:457` re-asked inside the YES lambda, `:449-488` YES/NO |
| `GuiScraperRun.cpp` / `.h` | 258 / 67 | 258/0 / 67/0 | 4 | **fork-own**, the SCRAPING GAMES page (D-UI-078, #241): a fourth-tier page in `GuiCloudTransfer`'s geometry -- one column 0.78 W, seven rows, a spinner (never a bar), elapsed time, CANCEL the one way out while `ThreadedScraper` runs (`input`, `:90-103`: releases swallowed, only BACK does anything, every other press refused; once finished `delete this` on any press, `:101`), the outcome in D-UI-028's words (`outcomeWord`, `:138-145`: `SKIPPED - YOU CANCELLED IT` / `COULDN'T FINISH` / `COMPLETED`); `BusyComponent(window, "")` at `:14`; `progress()` a mutex-guarded copy of a static (`ThreadedScraper.cpp:15-22`); 23 `_("`, 21 distinct, all with French; one dialog `:112-116` YES/NO |
| `WifiScanProcess.h` | 202 | 202/0 | 2 | **fork-own**, header-only (#577): `Answer{code=-1, lines}` (`:24-28`, every failure `-1`, "never empty success"); `Child` RAII over pid and pipe with `kill(-pid, SIGKILL)` of the child's own group and a 2 s `waitpid` deadline (`:31-71`); `read(command, timeout, cancelled)` (`:74-201`): refuses an empty command, a non-positive timeout or an already-cancelled flag, `pipe2(O_CLOEXEC)`, relocates a pipe end that landed on fd 0-2, `posix_spawnp` with `POSIX_SPAWN_SETPGROUP`, a non-blocking read bounded by the deadline and a 256 KiB cap, `WIFEXITED` required before `code`; 0 player strings |
| `GuiBios.cpp` / `.h` | 324 / 43 | 172/88 / 6/7 | 4 | BIOS CHECK (#308 F-ES-06/F-ES-28): the two-tab "Installed / All" page became one list of every system the check knows, sorted problems first (`loadList`, `:121-249`); a press opens a per-system `GuiSettings` of file rows (`openSystem`, `:251-281`); the empty state reads THE BIOS CHECK RETURNED NOTHING (`:187`); DETAILS offered only with a row to open (`:319-320`); `GuiLoading` over `getBiosInformations("", true)` (`:43-44`, `:116-117`) → `rocknix-systems --all` (`ApiSystem.cpp:880-886`); the row summary built word by word (`:223-229`); 10 `_("`, 9 distinct, all with French; no dialog left in the file; **T21's ES branch edited this file after the pin (`a73ed9efc`, PL-14/#1202)** -- the read is the pin's bytes, the stream's a fix on top |
| `GuiScraperStart.cpp` (`.h` upstream) | 559 / 48 | 105/7 | 5 | the SCRAPER page: GAMES TO SCRAPE FOR, IGNORE RECENTLY SCRAPED GAMES and SYSTEMS INCLUDED remembered in `Settings` (`ScraperFilter` `:93-107`, `RecentlyScrappedFilter` `:122-140` bounded to 0..6 else 3, `ScraperSystems` `:166-210`, the set saved only when opened from the main menu); DEVELOPER ID / DEVELOPER PASSWORD rows under `#if defined(SCREENSCRAPER_RUNTIME_DEV_LOGIN) && !defined(SCREENSCRAPER_DEV_LOGIN)` (`:415-421`, `storeInSettings=true`) and the refusal at SCRAPE NOW when empty (`:436-441`); SCRAPE NOW pushes `GuiScraperRun` when `ThreadedScraper::isRunning()` then closes (`:489-492`); `loadActivePage()` (`:34-50`, upstream) runs `save()` then `clearSaveFuncs()` on every tab switch; 13 `addSwitch(` with a literal `true`; 7 `_("` added, all with French; dialogs `:438-439` single-OK (fork), `:449` WARNING YES, `:467-470` YES/NO, `:483` single (upstream) |
| `GuiSettings.cpp` / `.h` | 465 / 164 | 8/1 / 18/0 | 3 / 4 | the base every settings page is built on: `lifeToken()` (`.h:104-115`, a `shared_ptr<void>` a worker holds weak and locks inside `postToUiThread`, held as `mLifeToken` at `:157` rather than in a save function "so that adding one does not turn a page with nothing to save into one that writes the settings files on close"); `addInputTextConfigRow` (`.h:84`) forwarding to `buildInputTextConfigRow` (`.h:151`, `.cpp:167-175`), the arrow sized from `font->getLetterHeight()` (`:208`); the two `addSwitch` signatures with `bool storeInSettings` (`.h:88-89`); the two `addWithDescription` overloads (`.h:49-56`: the three-argument form passes `multiLine = true`, the func form defaults `false`); `save()` and the close path T21's #1188 names (`:94-95`); `updateVal` with no non-empty-and-changed guard (#1185, T21 PL-01); one dialog `:449` single-OK |
| `GuiImageViewer.cpp` (`.h` upstream) | 778 / 51 | 16/1 | 1 | the viewer's grid tiles and the zoom take `DisplayAspect::forScreenshotPath(path)` (`:281-286`, `:678-682`; #243/#245, D-UI-080/081); the first call of a session walks every system's games on the interface thread under `sShotLock` (`DisplayAspect.cpp:74-87`, `:99-131`); upstream's four cached `exists` (`:415`, `:629`, `:660`, `:723`) and four `postToUiThread` (`:371`, `:432`, `:507`, `:752`); 0 strings added |
| `GuiGameOptions.cpp` (`.h` upstream) | 682 / 52 | 2/2 | 1 | both VIEW THIS GAME'S ACHIEVEMENTS rows pass the game's `CheevosHash` to `GuiGameAchievements::show` (`:128`, `:136`; #180, D-RA-009/011); otherwise upstream's context menu: 59 `_("`, 8 `GuiMsgBox(` (the most of any slice file), 5 cached `exists` at `:41`, `:53-56`; the DELETE confirmation at `:253` (FD-14) and `:630`; the NETPLAY NICKNAME row at `:203` (PL-031) |
| the 64 upstream-carried | 11,297 | 0/0 | 0 | byte-identical to the merge base **and to `rocknix/master` today**: upstream changed none of them since the base (its 14 commits touch `guis/` only in `GuiMenu.*`, `152/2` and `1/0`); the largest `GuiNetPlay.cpp` 1,109, `GuiControllersSettings.cpp` 853 (183 `_("`, the most), `GuiGamelistOptions.cpp` 691, `GuiMetaDataEd.cpp` 678, `GuiKeyMappingEditor.cpp` 632, `GuiCollectionSystemsOptions.cpp` 611, `GuiBatoceraStore.cpp` 547, `GuiThemeInstaller.cpp` 461, `GuiGeneralScreensaverOptions.cpp` 424, `GuiKeyboardtopads.cpp` 380, `GuiMoonlight.cpp` 365; `GuiLoading.h` 143 is the busy page every `GuiLoading<T>` in the tree is; read for brittleness, left as upstream has them (D-UI-079), a contained defect still closed (rule 6) |

**The pages, what the digest checked and found sound, so the lane confirms
rather than hunts:** every fork YES/NO confirmation is YES first and NO last
(`GuiSaveState.cpp:449-488`, `GuiScraperRun.cpp:112-116`); the three
`clearButtons(` sites sit in page methods that rebuild the whole menu, none
in a lambda handed to `addButton(` (`GuiKeyboardtopads.cpp:78`,
`GuiScraperStart.cpp:40`, `:212`; the only button lambdas in those files are
the two BACK closers at `GuiKeyboardtopads.cpp:93`, `GuiScraperStart.cpp:55`
and `std::bind(&GuiScraperStart::pressedStart)` at `:213`); `delete this`
at `GuiScraperRun.cpp:101` is safe (`GuiComponent::~GuiComponent` removes
the page from the window, `GuiComponent.cpp:28-30`); the scrape page owns no
thread and reads a copy; no `system(` or `popen(` in any of the 76 files; no
`std::stoi`/`std::stoul`; no `setVariable("reboot"` or `"exitreboot"` and no
mention of either name; 0 non-ASCII bytes in `//` comments across the 76,
and 0 adjacent to a `_(`; every `_("")` string the fork added in the four
pages that add any (59 occurrences, 50 distinct) has a `msgid` in the French
catalog at the pin with a non-empty `msgstr`; a 40-of-168 stride sample of
the twelve fork-touched files' one-line literals is 40 TRANSLATED, 0 empty,
0 fuzzy, 0 not in the catalog.

**What it found instead, the leads of § 4** (each read at its lines before
it is called anything): **the scrape page's finished state is dismissed by
any input** (`GuiScraperRun.cpp:101`: `input.value != 0`, an axis crossing
its deadzone or a held D-pad repeat included -- the outcome a player walked
away from can be dismissed by stick drift before it is read);
**`SKIPPED - YOU CANCELLED IT` is a fourth SKIPPED reason** (`:141`) where
`es-player-text.md:236` and D-UI-028 reserve the word for rclone 69, 75 and
the launch cancel; the comment argues it and no register row is cited; **a
run in which every game errored but the scraper did not `fail`** shows
`COULDN'T FINISH` with counts and neither a why (line 4 needs `p.failed`,
`:225`) nor a next step (line 5 needs `done - errors > 0`, `:231`); **the
BIOS row summary is assembled word by word** (`GuiBios.cpp:227-229`: `N` +
OF + `M` + MISSING, `, K` + NOT A KNOWN VERSION), so the French reads `2 SUR
5 MANQUANT` in English word order with no agreement; **an absent or failing
`rocknix-systems` yields an empty vector the page shows as THE BIOS CHECK
RETURNED NOTHING** (`:183-187` with `ApiSystem.cpp:880-886`) with no
recovery line -- the page cannot tell a failed script from a check that
knows no systems; **`isFlockHeld` returns `errno != ENOENT` when the lock
file cannot be opened** (`AtomicFileUtil.cpp:440-442`), so an unreadable
`/var/run/cloud_sync.lock` refuses DELETE and COPY indefinitely with A SYNC
IS ALREADY RUNNING. -- fails closed, with the wrong words; **COPY TO FREE
SLOT still runs upstream's `copyToSlot(slot)` synchronously on the
interface thread** (`GuiSaveState.cpp:516`); only the record (`:524`) moved
to the worker, so a large state on a slow card holds the screen in the
shape #205 fixed for DELETE -- and since T2's `f11e7528a` the call returns
what the file operations did, which this page does not yet say to the
player (PL-016, #782); **`loadActivePage()` calls `save()` on every tab
switch** (`GuiScraperStart.cpp:36-37`) and `GuiSettings::save()` writes
`es_settings.cfg`, so with the fork's three save functions a visit that
steps SCRAPE → OPTIONS → ACCOUNTS rewrites the settings file twice before
SCRAPE NOW (upstream's path, now exercised on every visit); **a set of zero
systems chosen from the main menu saves `ScraperSystems=""`** and the next
open reads `anyRemembered == false` and falls back to every platform-id
system (`:181`, `:202-210`) -- "none" cannot be remembered; **the first
`forScreenshotPath` of a session walks `getFilesRecursive(GAME)` of every
system on the interface thread under `sShotLock`** (`GuiImageViewer.cpp:281-286`
with `DisplayAspect.cpp:74-87`): on a large library the screenshot grid's
first open pays that walk before its first frame.

**The dialogs, the rows, the reads and the bars** (the floor's runs, § 5):
**50 `GuiMsgBox(` in 18 files** -- by the three-line heuristic YES first at
17, OK at 10, another word at 6, none in the window at 17; read whole,
three of the six are the one-word message FINISHED with OK beside it
(`GuiAutoScrape.cpp:68`, `GuiBackup.cpp:61`, `GuiInstall.cpp:62`), one is
FAILED with no button (`GuiNetPlay.cpp:336`, a word D-UI-028 bans from
every screen; upstream's), and **two are real first buttons that are
neither YES nor OK: WRITE at `GuiGameOptions.cpp:274` and CLOSE at `:289`**;
13 of the 17 are single-OK boxes by `GuiMsgBox`'s default (the four
sentence-case `GuiMoonlight.cpp` boxes at `:295`, `:315`, `:333`, `:336`
among them), and the three with buttons past the window are printed whole
in the floor (`GuiControllersSettings.cpp:76-84` OK / CANCEL; the scrape
page's YES / NO; the scraper's single). **26 `addSwitch(` in 6 files, 23
with a literal in the `storeInSettings` slot, all `true`**
(`GuiScraperStart.cpp` 13, `GuiControllersSettings.cpp` 4,
`GuiNetPlaySettings.cpp` 4, `GuiCollectionSystemsOptions.cpp` 2; the other
three are `GuiSettings`' own two signatures and one definition): ES-own
keys to `es_settings.cfg`, not the PROGRESS TRACKER shape. **12
`Utils::FileSystem::exists(` in 5 files, 0 with `, false)`**
(`GuiGameOptions.cpp:41`, `:53-56`; `GuiImageViewer.cpp:415`, `:629`,
`:660`, `:723`; `GuiFavoriteMusicSelector.cpp:19`; `GuiNetPlay.cpp:679`;
`GuiNetPlaySettings.cpp:70`), each asking about a file the scraper, the
player or another process writes while ES runs. **8 `.cpp` files define no
`getHelpPrompts()`** (`GuiAnalogSticksLedControls`,
`GuiCollectionSystemsOptions`, `GuiControllersSettings`,
`GuiFavoriteMusicSelector`, `GuiGeneralScreensaverOptions`, `GuiMoonlight`,
`GuiNetPlaySettings`, `GuiSystemInformation`; 79 lines name the symbol
elsewhere). **6 `runSystemCommand(` in 3 files** (`GuiAnalogSticksLedControls.cpp`
1, `GuiControllersSettings.cpp` 2, `GuiMoonlight.cpp` 3) **and 5
`executeScript` in `GuiMoonlight.cpp`**; 18 `std::thread` in 13 files, 18
`GuiLoading<` in 12, 9 `postToUiThread(` in 5, 3 `AsyncNotificationComponent`
in `GuiUpdate.*` (the OS update card, D-UI-079's named upstream surface);
**9 `atoi(` in 3 files** (`GuiAnalogSticksLedControls.cpp:20-26`,
`GuiKeyMappingEditor.cpp:156`, `GuiUpdate.cpp:213`), 0 throwing parses; 14
`addWithDescription(` in 7 files, 8 `multiLine` in 3; **891 `_("` sites in
37 files.**

**The map and the checker.** `docs/es-menu-map.md` (989 lines) describes or
declares the titles of 15 of this slice's pages: six mapped (GAME COLLECTION
SETTINGS; VIEW OPTIONS once, the SELECT row at `:90` under `## Two ways in` at `:83`; INDEX
GAMES as the RetroAchievements row, not the page; SAVE STATE MANAGER in its
own section `:150`; SCRAPER in the main menu, the tabbed page and the #566
flow at `:911`; INFORMATION at `:718` and `:793`) and nine declared under
`## Not mapped` (`:677`; eleven of its 24 titles sit behind a T31 page:
FAVORITE SONGS, SCREENSAVER SETTINGS, SCREENSCRAPER, NETPLAY SETTINGS,
CONNECT TO NETPLAY, ADD TO CUSTOM COLLECTION..., GLOBAL HOTKEYS, JOYSTICKS
HOTKEYS, KEYBOARDTOPADS, ANALOG STICKS LEDS, PAIR A BLUETOOTH DEVICE). **Twelve pages
have a title in neither place**: `GuiBios` (BIOS CHECK, fork-modified),
**`GuiScraperRun` (SCRAPING GAMES, fork-own)**, and ten upstream pages
(BACKUP USER DATA, hidden on ROCKNIX; CONTENT DOWNLOADER; THE BEZEL PROJECT
-- the map declares DECORATIONS, not the installer; DEVICE OPTIONS;
BLUETOOTH DEVICE LIST; FILTER GAMELIST BY / EDIT DYNAMIC COLLECTION FILTERS /
FIND GAMES; INSTALL ON A NEW DISK; PAD TO KEYBOARD CONFIGURATION and its two
sub-titles; EDIT METADATA; THEMES DOWNLOADER). Ten `.cpp` and two headers
yield no title by any of the shapes read (the viewer, the file browser,
`GuiMoonlight`, `GuiUpdate` among them). **And the checker cannot see most
of them**: `tools/es-menu-map-check`'s three regexes match `new
GuiSettings(window, _("..."))`, `GuiSettings(m?[Ww]indow, _("..."))` and
`MenuComponent(window, _("..."))`; a page built on `GuiComponent` with its
own `mMenu(window, _("..."))`, a `setTitle(_(...))` or a computed title is
invisible to it, which is #951's shape (22 of 75 `new GuiSettings(` calls at
the pin never checked) seen from the pages' side -- so a T31 page can be
neither mapped nor declared and the check still prints `0 missing`. No
slice **class name** appears in the map but `GuiScraperStart` (once). The
same check passes at the pin for the tree (T26's recorded line, § 5).

**The harness that exists.** None of the 15 Python harnesses under the ES
repository's `tests/` reads a file in this slice (8 read `GuiMenu.cpp`, 2
`FileData.cpp`, 1 `GuiWifi.cpp`, 1 `ThreadedHasher.cpp`, 1
`OfflineAchievements.cpp`, 1 the tree, 1 `GuiMenu.cpp` with
`OptionListComponent.h`); of the slice's classes, `GuiSaveState` is named
by `es-app/tests/unit/TimeTextTests.cpp`, `GuiSettings` by four harnesses as
the base their pages double, `GuiLoading` by `tests/launch-capture-gate.py`,
and **every other class by nothing** -- the fork-own `GuiScraperRun` and
`WifiScanProcess` included (`WifiTextTests.cpp` does not name the class).
The doctest binaries need the toolchain's rapidjson (#1137: M6 has no build
root). So the host floor for this slice is the four patterns T31 copies:
`tests/wifi-profile-lifetime.py` (a page callback with real deletion under
ASan -- T21 PL-21's named shape for deleting a `guis/` page under a
`GuiLoading`), `tests/cloud-oauth-lifetime.py` (page transitions),
`tests/gpu-governor-save.py` (a row's save callback with the stores
doubled), `tests/cloud-gated-row.py` / `tests/cloud-set-systems-quoting.py`
(a builder; a command through `/bin/sh`). The walks: `tools/vm-walks/` holds
18 `.steps` files and one frames two of this slice's pages --
`manager.steps` (33 lines: carousel, list, X for GAME OPTIONS, A for the
manager, right to the capture tile, back out; shots `0-carousel`, `1-list`,
`2-game-options`, `3-manager`, `4-manager-next-tile`), with the accepted
baseline `d72084ccad`'s `manager-gb/nes/fbn` claims at `claims.txt:38-44`,
`:49-50`, `:160-230` (564 lines; `suite.txt` 100); `ui-settings-toggle.steps`
(41 lines) is the one walk that exercises `GuiSettings.cpp`'s close path
(#1188's lines) on a T26 page. **No walk opens** the Bluetooth pages,
SCRAPER, the BIOS check, the theme installer or content downloader, the
mapping pages, netplay, the metadata editor, collection settings, game-list
options and filter, the image viewer, INFORMATION, UPDATES, MOONLIGHT, the
screensaver page, the file browser, KEYBOARD LAYOUT or the backup pages;
#1190 names the scraper walk baseline as missing; the frames that exist are
`docs/qa-logs/2026-10-14-screenscraper-ui-runtime` (35 png) and the
`manager-*` frames of the baseline.

**The neighbours, and whose they are:** `GuiMenu.*` -- the rows that open
every page here -- is **T26's** (#673); `GuiWifi.*`, the stores
`Settings`/`SystemConf`, `ApiSystem`'s executors, `AtomicFileUtil.cpp`'s
`isFlockHeld`, `FileSystemUtil.cpp`'s cache, `HttpReq` are **T21's**
(#668); `GuiCloud*` and `GuiOfflineScan*` are **T18's** (#665);
`GuiRetroAchievements*`, `GuiGameAchievements*` and `ThreadedHasher` are
**T20's** (#667); `SaveState.cpp`'s `copyToSlot`/`remove`, `FileData.cpp`'s
launch options and the nickname seeding, `SystemData` are **T2's** (#649);
`SaveStateBookkeeper`, `ThreadedScraper`, `DisplayAspect.cpp`, `CloudText`
and `TextFit` are other interface slices' (T32 to T37) and read here only as
what this slice's pages call; `rocknix-systems` and the launch scripts are
**T1's** (#648); the es-core components (`GuiMsgBox`, `GuiTextEditPopup*`,
`ComponentTab`, `MenuComponent`, `BusyComponent`, `TextComponent`) are
**T35's** by the inherit digest's reading -- the coordinator confirms the
owner at the pause before any es-core line is touched.

**Already found; do not re-find** (cited at its lines): T2's PL-010/#776
(`GuiNetPlay.cpp:1021` fills `session` and nothing reads it; `:1058` sets
SPECTATOR and the image joins as a player), PL-016/#782 (`copyToSlot` and
`remove` return what the file operations did since ES `f11e7528a`; the
message to the player is this slice's), PL-031 (`FileData.cpp:653-657`
seeds `global.netplay.nickname`; the two rows at `GuiNetPlaySettings.cpp:26`
and `GuiGameOptions.cpp:203` rely on it), PL-005's sibling
(`GuiGamelistOptions.cpp:148`: `>` before `.at()` where `>=` is meant), FD-14
(`GuiGameOptions.cpp:253` names no path), FD-21 (`FileData::resetSettings`
static and empty, called from `GuiCollectionSystemsOptions`), SS-4
(upstream's `copyToSlot` returned `true` unchecked -- fixed by S2); T20's
`:85`/`:59` hasher constructions (#1170, #301); T21's L-23/#1185
(`updateVal` saves an empty value unchecked), L-33 (`GuiBluetoothDevices.cpp:117-121`
ignores the bulk delete's result), L-35/#1212 (`:127`, `:150` -- a data
race by reading; the ASan case in `wifi-profile-lifetime.py`'s shape is the
VM line), #1193 (`ScreenScraperUser`/`ScreenScraperPass` in
`es_settings.cfg`, 0644 when new, `GuiScraperStart.cpp:413-420`),
L-03/#1191 (the default filter clears the overwrite, `:99`), `:66` (the
Bluetooth and storage arguments joined bare -- "safe by shape, not by
quoting"), `:335` (`GuiSaveState.cpp:33` asks the transfer's flock), `:399`
(`GuiKeyboardLayout.cpp:164` writes a file on the card through `writeAllText`, whose `fopen "wb"`, `fwrite` and `fclose` are unchecked at `FileSystemUtil.cpp:1434` -- an empty or cut file where the old one was; Backlog #1186), PL-14/#1202 (`a73ed9efc` on T21's ES branch); blindspot
4 (`close()` inside a page's own handler), 45 (the manager's DELETE ran two
synchronous `cloud_capture`s, proven at a fixture's speed), 62 (the
maintainer's first look at the SAVE STATE MANAGER after the upgrade found
what a fix had left written). T18 found nothing in these files.

## 3. Read first

In this order, each read in this session, and `01-research-notes.md` says
which were read (`working-principles.md` § Pre-flight):

1. **The rules.** `es-ui-style-guide.md`: § Confirmations `:169` (**YES
   first; the back-button accelerator binds to a button named exactly NO or
   OK and otherwise falls through to the last button**), § Rows `:68` and
   § The `multiLine` trap `:90` (which overload a row hits decides whether
   its description wraps), § Saving `:210` (apply a credential only when
   non-empty and changed), § Reboot-required `:221`, § Buttons `:232`, §
   Gating `:268` (network round-trips behind an explicit action, never at
   page build), § Interaction rules `:296` (`getHelpPrompts()` kept
   accurate), § Known inconsistencies `:306` (`MenuComponent::addEntry` and
   `GuiSettings::addEntry` swap parameters 5 and 6), § Keep the flow and its
   visual evidence together `:32`; `es-code-traps.md`: § Never rebuild a
   button bar from inside one of its buttons `:22`, § What rclone's piped
   progress looks like `:38` (only its `BusyComponent(window, "")` line), §
   Comments near a translatable string must be ASCII `:60`, § The help bar
   offers a direction only where it moves something `:79`, § Three things a
   font is not `:104` (**the `exists` cache; and with full-screen menus a
   non-`MenuComponent` page draws its own bar with `renderHelpPromptsEarly()`
   -- the save state manager, ES `d8e95118c`, #149**), § A rescan that
   deletes FileData drops the view first `:191` (`GuiCollectionSystemsOptions`
   and `GuiMetaDataEd` sit on this edge), § A pooled connection with the
   link gone `:238` (the hasher's constructor, called from two of this
   slice's pages), **§ A taller GuiSettings menu keeps its old top offset
   `:266` (#540)**; `es-native-ui.md`: § Core patterns `:81` (**a file
   another process writes is read uncached**), **§ Tabbed pages `:121`
   (four screens still route left/right to their strips themselves --
   `GuiThemeInstaller`, `GuiBatoceraStore`, `GuiKeyMappingEditor`,
   `GuiKeyboardtopads` -- all four this slice's; they move with #63)**, §
   Spacing `:175` (the four surface tiers; D-UI-078 the fourth-tier page
   with CANCEL; **D-UI-079: the upstream cards -- the game index, the content
   installer, the OS update, the Bluetooth scan -- stay as they are**), § A
   layout must not be computed from what it last produced `:324`, § Code
   conventions `:342` (**`addSwitch`'s bool is `storeInSettings`**), §
   Reusable precedents `:367` (`GuiBackupStart`/`GuiBackup`,
   `GuiFileBrowser`, `GuiMoonlight`, `GuiBatoceraStore`/`GuiThemeDownloader`
   -- all this slice's files), § Anti-patterns `:377`, § Before the pin
   moves `:405`; `es-player-text.md`: § Conventions `:29` (the three outcome
   words; a question over a running job; the card rule), § Every fork string
   ships in English and French `:141`, § A row that leads somewhere `:170`
   (D-UI-023), § Outcome words `:211` and **§ Outcome vocabulary `:236`
   (`SKIPPED - <reason>` for 69, 75 and the launch cancel only; no FAILED on
   any screen)**; `engineering-practices.md` `:12` (D-UI-079), `:28` (check
   upstream early -- the 64 upstream-carried files are at `rocknix/master`'s
   bytes, so the check is of batocera's tree for a page's later fix), `:111`
   (verify the artifact), `:419` (guards fail closed), `:576` (blindspot
   23); `bugs-are-agent-first.md` `:41`, `:53` (§ The rules), `:76` (rule 6); `player-language.md`
   and `least-surprise.md` whole.
2. **The register.** The rows that name a page here (all present on the
   coordinator's branch; D-WORKFLOW-188 is the P1 branch's): **D-UI-021**
   (the tab strip is a focus stop; the four screens that still route
   left/right themselves), **D-UI-022** (save state, two words; the manager
   renamed), D-UI-023, **D-UI-028/030** (the three outcome words -- the
   scrape page's fourth SKIPPED is Q5's), D-UI-034 (the help bar), D-UI-035
   (the longer candidate first; the scrape page's two notes), D-UI-039,
   D-UI-042/045, D-UI-051, **D-UI-069/073/074/080/081/087/089 and
   D-CLOUD-053** (the manager's twenty-five commits: the label fit, the
   aspect and the turn, the dates, the gate on the saves tree, the worker
   deletion), **D-UI-078** (the scrape page), **D-UI-079** (the lanes),
   D-UI-093/095, D-UI-107, D-UI-118, D-RA-009/011 (the hash to the
   achievements page), D-NET-009 (an empty value on purpose), D-WORKFLOW-144
   (pixelelated lowercase), D-WORKFLOW-155/156 (flow and evidence together),
   D-WORKFLOW-164/165 (#585, never sent), **D-WORKFLOW-166** (#566: the shared
   ScreenScraper developer identity; the DEVELOPER rows hidden when a pair
   is compiled in), D-WORKFLOW-187/189/195. Open and this slice's to leave
   open: D-WORKFLOW-080 (how the interface work goes upstream in pieces).
   The register names the save state manager in 7 rows and the scrape in
   16; the lane reads them by `tools/archaeology 'save state manager'` and
   `'scrape'` before calling anything pending.
3. **The menu map** (`docs/es-menu-map.md`, 989 lines): `## Two ways in`
   `:83` (VIEW OPTIONS), `## Main menu` `:95`, `## What lives where` `:126`,
   **`## Save state manager` `:150`** (`### Save-state capability guidance
   (#575)` `:179`), **`## Not mapped` `:677`** (the rule at `:683`: *adding
   a row to any of these means mapping it above and deleting its line
   here*), **D-UI-039 at `:668`**, `## ScreenScraper developer provisioning
   (#566)` `:911`, `## Build identity in INFORMATION (#530)` `:718`, `##
   Unavailable hardware readings (#548)` `:793`, and the visual-evidence
   section `:26-82` (the baseline `d72084ccad`; the `evidence-index.json`
   schema). `docs/conflict-wizard-ia.md` is T18's.
4. **The blindspots** naming this slice's pages or shapes: 4 (`close()`
   inside a page's own handler), 8 (an assertion that holds because
   nothing had happened yet -- the manager's gate on a lock nobody holds),
   13 (assumed done), 44 (`MultiLineMenuEntry` measured from the cells it
   set last time; the SCAN GAMES row -- `es-native-ui.md:324`), **45 (the
   manager's DELETE ran two synchronous `cloud_capture`s, proven at a
   fixture's speed, not the device's -- COPY at `:516` is the sibling)**,
   49 (an edit made blind to the compiler), **62 (a fix corrected the
   writer and left what it had already written to heal by play: the
   maintainer's first look at the manager after the upgrade)**, 75 (a
   corpus read on the wrong tree -- the two merge bases of § 2).
5. **The tests at the pin.** The sweep in § 5 (`git -C "$W" grep -l -w
   <class> "$PIN" -- es-app/tests tests` for every slice basename): three
   hits, named in § 2. The four pattern harnesses, read whole before a case
   is written in their shape: `tests/wifi-profile-lifetime.py`,
   `tests/cloud-oauth-lifetime.py` (184 lines), `tests/gpu-governor-save.py`,
   `tests/cloud-gated-row.py` and `tests/cloud-set-systems-quoting.py`.
   `SaveStateJobQueueTests.cpp` and `TabStopsTests.cpp` are the two unit
   files nearest this slice's pages (the manager's job queue; the strip's
   focus stops, #65). `.githooks/pre-push-test` is the ES fork's guard
   test.
6. **The walks and the frames.** `tools/vm-walks/manager.steps` (33 lines)
   and its `README.md:184-189`; `ui-settings-toggle.steps` (41);
   `claims.txt:38-44`, `:49-50`, `:160-230` (the `manager-*` frames at
   `d72084ccad`); `suite.txt` (100 lines; the `default-pre` every leg
   starts from); `reset.steps`'s note on the GO TO dialog a walk must not be
   left holding (#85); `docs/qa-logs/2026-10-14-screenscraper-ui-runtime`
   (35 png). T2's W-5 (`02-forward-audit.md:268` on
   `origin/feature/m6-es-launch-path-649`) is the walk this slice writes
   next on the manager.
7. **The French**: 891 `_("` sites in 37 of the 76 files; the 59
   occurrences (50 distinct) the fork added, every one with a non-empty
   `msgstr`; the 40-of-168 sample at 40 TRANSLATED (an estimate, not the
   count: `tools/es-untranslated` is the count, § 5); the BIOS summary's
   word-by-word French (Q5).
8. **The audits**: T2's `02-forward-audit.md:54-55`, `:112`, `:146`, `:268`,
   `04-analysis.md:99`, `:612-613`, `05-punch-list.md:109`, `:295`, `:614-615`,
   `:645`, `:660` (on `origin/feature/m6-es-launch-path-649`); T21's `02:74-129`
   § Corrections and new leads and `:543-553` § What T26 and the OS slices
   inherit (on `origin/feature/m6-es-state-and-bridge-668`), its `05:130`,
   `:400`, `:418-421`, `:509`; T20's `02:78-79`, `:152`, `:158`; T26's `02`
   § What T31 to T37 inherit when it lands (its brief's `:575-579` and
   `:678` say what it carries). T18's has no inherit section.
9. **The issues**: #776, #782, #768, #1212, #1185, #1188, #1170, #301, #63
   (and #65, the `MenuComponent` half done), #196, #37, #951, #965, #1192,
   #1193, #1191, #1202, #577, #241, #243, #245, #250, #205, #307, #308, #566,
   #540, #149, #1137, #1182, #1190, #1141, #791, #222, #36, #18; #678's own
   body.
10. **Time to play**: `docs/vm-qa-log.md:9-18` (the three headline columns;
    T26's brief cites the September rows: UI to game 0.6 to 1.11 s, exit sync
    1.06 to 1.56 s, game to game 1.0 to 2.04 s; `Not measured` on 2026-10-14
    and 2026-10-16); `time-to-play.md`'s one budget (the exit sync's 3 s,
    D-CLOUD-119). This slice's pages sit on the launch path at two points:
    the manager's PLAY from a slot (#196's `launch` with a state) and the game
    options menu (X on a game) -- the retro's line names them.

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of the four families the earlier ES briefs
used -- **a command built from a player's string**, **a credential's sink**,
**a state write that can lose the record**, **a check whose failure reads
as success** -- or one of the page families this slice adds: **a dialog
whose back lands on the destructive choice**, **a row whose store is
wrong**, **a read of a file another process writes**, **a page with no help
bar**, **work on the interface thread**, **a player sentence outside the
vocabulary**, **a page the map does not describe and the checker cannot
see**. The leads are § 2's by shape; each is read at its lines before it is
called anything; each question names its rule and the § 5 run that
measures it.

- **Q1 The dialogs and where back lands** (`es-ui-style-guide.md:169`,
  `es-code-traps.md:79`; the dialogs run). All 50 sites read whole for the
  buttons in order and the one the back accelerator reaches: the 17
  YES-first and 10 OK-first confirmed; **WRITE / CANCEL at
  `GuiGameOptions.cpp:274` and CLOSE at `:289`** (what back does on the NFC
  writer); the three multi-line boxes; the `busyNow` box re-asked inside
  the manager's YES lambda (`:457`); THIS WILL DELETE THE ACTUAL GAME
  FILE(S)! at `GuiGameOptions.cpp:253` and `GuiMetaDataEd.cpp:365` (neither
  names a path, FD-14; #768 is the deletion's bug); SAVE CHANGES? at
  `GuiKeyMappingEditor.cpp:497` and `GuiMetaDataEd.cpp:629` (where back
  lands on an edited page). A table: site, first words, buttons in order,
  the landing, destructive or not.
- **Q2 The rows, their stores, and the writes that can lose the record**
  (`es-native-ui.md:342`, `es-ui-style-guide.md:210`, T21's `02:546-552`;
  the switches and two-line-rows runs). The 23 `addSwitch` literals
  confirmed as ES-own keys; every `addInputTextConfigRow` here (DEVELOPER
  ID / PASSWORD `GuiScraperStart.cpp:415-421`, the ScreenScraper account
  `:413-420`, NICKNAME `GuiNetPlaySettings.cpp:26`, NETPLAY NICKNAME
  `GuiGameOptions.cpp:203`, the netplay password) as **a credential's
  sink** -- the store, the mode (#1193's 0644), whether an untouched editor
  clears it (#1185's `updateVal`: recorded per row, nothing changed in
  `GuiSettings.cpp` without the pause's ruling); **a state write that can
  lose the record**: `save()` on every SCRAPER tab switch (`:36-37`, two
  rewrites of `es_settings.cfg` before SCRAPE NOW; atomicity is T21's
  `:547`, cited), `ScraperSystems=""` read as every system (`:181`,
  `:202-210`), `GuiKeyboardLayout.cpp:164`'s `writeAllText` call (the in-place `fopen "wb"` is `FileSystemUtil.cpp:1434`, T21's file; the site is Backlog #1186's); PL-031's
  nickname default; the overload each of the 14 `addWithDescription(` hits
  and the metadata editor's multi-line popups (`GuiMetaDataEd.cpp:333-341`);
  no reboot flag set by any page here (a setting that needs one is a
  finding).
- **Q3 The interface thread** (`es-native-ui.md:175`, D-UI-078;
  `es-code-traps.md:238`; #1188; the process-starts and async runs).
  **`copyToSlot(slot)` synchronous at `GuiSaveState.cpp:516`** (blindspot
  45's sibling: what the player sees, nothing; what bounds it, nothing);
  **`buildStems` at the viewer's first open** (`GuiImageViewer.cpp:281-286`,
  `DisplayAspect.cpp:74-87`); **`save()` per tab switch** with
  `GuiSettings.cpp:94-95`'s two writes under #1188's lock; the 6
  `runSystemCommand(` and 5 `executeScript` -- each with what it runs,
  whether the window is passed, what bounds it; the 18 `GuiLoading<`
  completions (which hold raw `this`; `GuiBluetoothDevices.cpp:127`/`:150`
  is #1212's, the rest graded the same way) and the 18 `std::thread`
  mentions (who joins each, what it touches on the UI thread; `GuiUpdate`'s
  four and `GuiNetPlay`'s one first); the hasher at `GuiHashStart.cpp:85`
  and `GuiNetPlaySettings.cpp:59` (#1170, #301: cited); the time-to-play
  line (§ 6): which of these sit between a press and a frame on the
  manager's PLAY or the game options menu.
- **Q4 The reads, and the checks whose failure reads as success**
  (`es-native-ui.md:81`, `es-code-traps.md:104`,
  `engineering-practices.md:111`, `:419`; the reads and parses runs). The
  12 cached `exists` sites, each with its file, its writer while ES runs
  (the scraper writes what `GuiGameOptions.cpp:41`, `:53-56` and
  `GuiNetPlay.cpp:679` ask about) and whether a remembered miss changes the
  screen (a row hidden after a scrape until restart; the positive on the
  guest: options menu, scrape, options menu again, one session); **the
  empty vector read as THE BIOS CHECK RETURNED NOTHING** (`GuiBios.cpp:183-187`,
  `ApiSystem.cpp:880-886`: a failed script and an empty check are one
  screen; the harness a double for `getBiosInformations`);
  **`isFlockHeld`'s EACCES read as a running sync** (`GuiSaveState.cpp:33`,
  `AtomicFileUtil.cpp:440-442`: T21's file, this slice's sentence); the
  manager's silence when `copyToSlot`/`remove` return `false` (PL-016,
  #782; the sentence under `es-player-text.md:236`); the Bluetooth bulk
  delete's ignored result (L-33, `:117-121`; `:120` says DELETED whatever
  happened); the 9 `atoi(` sites (`GuiAnalogSticksLedControls.cpp:20-26`
  over seven tokens of a script's line -- a short line and `tokens[6]`;
  `GuiKeyMappingEditor.cpp:156`; `GuiUpdate.cpp:213`); the scrape page's
  all-errored run (`:225`, `:231`) and its finished state dismissed by
  `input.value != 0` (`:101`). A table of every read and parse with its
  writer, cached or not, and what a failure reads as.
- **Q5 The words, the French and the help bars** (`es-player-text.md:29`,
  `:141`, `:211`, `:236`; `es-code-traps.md:60`, `:79`; the strings,
  help-bars, non-ASCII and French runs). **The fourth SKIPPED**
  (`GuiScraperRun.cpp:141`: a cancel the player made under D-UI-028's
  launch-cancel reading, or a new reason that wants a row -- for the pause,
  with the sentence and the comment's argument quoted); **the word-by-word
  BIOS summary** (`GuiBios.cpp:223-229`: `2 SUR 5 MANQUANT`); the scrape
  page's two notes (`:232`, D-UI-035) at 640x480 in both locales; FAILED at
  `GuiNetPlay.cpp:336` and `GuiMoonlight.cpp`'s sentence case (upstream's;
  recorded under D-UI-079, a #585 line if the fix is one word); the 891
  sites against `tools/es-untranslated` and the 59 fork additions against
  the catalog; the 0 non-ASCII comments; **the 8 bar-less `.cpp` files** --
  which subclass `GuiSettings` and inherit the menu's bar (read, not
  assumed), which show none, and whether what a bar offers moves something
  (`GuiKeyMappingEditor.cpp:476`'s commented-out prompts); the manager's own
  bar under full-screen menus (`:386-399`, #149) in a 640x480 frame; #540's
  shape on any page that calls `getMenu().setSize(` here (the lane's run,
  no expectation).
- **Q6 The commands and their readers** (T21's `02:545`;
  `es-native-ui.md:377`; `engineering-practices.md:419`; the
  process-starts run). **A command built from a player's string**: what
  reaches the 6 `runSystemCommand(` and 5 `executeScript` sites (a
  Moonlight host or PIN the player typed? a controller's name? the LED
  values?) and through which quoting; the Bluetooth and storage arguments
  joined bare (T21's `:66`: safe by shape, the shape named per site --
  `GuiBluetoothDevices.cpp:131-137`, `GuiBluetoothDeviceOptions.cpp:56-106`,
  `GuiInstallStart`, `GuiBackupStart`); **`WifiScanProcess.h` as the argv
  model**, read whole for its own bounds (the 256 KiB cap, the 2 s reap,
  the fd relocation, `environ` passed) and recorded as the executor #1192
  names; `GuiNetPlay`'s `session` and SPECTATOR (#776: cited; what the
  launcher can express is T1's); `GuiUpdate.cpp:213`'s percent reader. No
  `system(`, no `popen(`.
- **Q7 The map, the structure and the merge debt** (`es-native-ui.md:121`,
  `:32`; D-UI-039; D-UI-079; the membership block, the scope and delta
  runs, the title shapes run). **The twelve undescribed titles**, one line
  each -- map it, declare it with a reason, or record it as not built on
  ROCKNIX -- BIOS CHECK and SCRAPING GAMES first (D-UI-039 applies to every
  row the fork added); **the checker's blind spot** (the 76 files' title
  shapes against its three regexes: the table is #951/#965's evidence, the
  fix a Backlog the coordinator files); **the four tab-strip pages** (#63:
  recorded with lines, not moved); the duplicates across pages (ARE YOU
  SURE YOU WANT TO DELETE THIS ITEM? at four sites, THIS WILL DELETE at
  two, FINISHED / OK in three wizard pages, YOU ARE NOT CONNECTED TO A
  NETWORK at three) -- per family, whether the copies differ; **the merge
  debt**: zero upstream changes to any slice file since `cada856d86`, the
  table saying so with both bases named; the provenance 3 / 9 / 64 as what
  T32 to T37 read; D-WORKFLOW-080's shape (the fork's pages are already one
  file each here -- recorded for GuiMenu's option (a)).

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #678.** Every read, count and table runs on the host at
   the pin's bytes. **The host has no toolchain** (#1137): every `.cpp` here
   is `CANNOT` for the host's `g++ -fsyntax-only` until proven otherwise
   (SDL through `Window.h`), and its compile proof is the integration
   build's; `tools/es-syntax-check` records its exit-2 line with
   `ES_BUILD_ROOT` set, never empty. **No harness reads a file in this slice
   at the pin**, so the host floor is what the lane builds in the four
   patterns' shape under the ES worktree's `tests/` -- **a case per pure
   lead** (the BIOS page's empty vector against a doubled
   `getBiosInformations`; the scrape page's `outcomeWord` and its finished
   rows over a `progress()` double; the manager's `savesTreeBusy` against a
   lock file it cannot open; `GuiScraperStart`'s save functions against
   doubled stores; a page deleted under a `GuiLoading` under ASan for #1212's
   shape) -- each run from the ES worktree with its exit and summary line
   recorded in `02` § The runs, and seen to FAIL once against the unfixed
   extract before it is trusted (`engineering-practices.md:419`; T21's
   retro). `tools/es-menu-map-check`, `tools/es-untranslated --upstream
   bccd715707` (and the same with `cada856d86`, both lines recorded), the
   non-ASCII comment grep, the title-shape table and the dialog table run on
   the host.
2. **The guest window** -- one, asked for on #678 at stage B's end with its
   plan and bound (45 minutes proposed), granted explicitly in the shared
   log's queue, one boot of the M6 copy of the image
   (`/workspace/artifacts/m6-t2-20261023/`, `069fc2704421`) **started at
   640x480** (`projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run
   --res`, #1141), the post contract `START HH:MM:SS UTC` / `RETURN
   HH:MM:SS UTC` as each post's first line with the census, the stop by
   pidfile at bound plus grace, the disk retired after with path, size and
   sha (D-INFRA-022): the identity (`BUILD_ID`; the image's EmulationStation
   is M7's build, so every verdict labels the image's side, and a frame is
   `pin-binary` evidence only where the digest found the pin's lines
   unchanged against the image's -- else `image`); **the walks of the fork's
   pages** -- the SAVE STATE MANAGER (`manager.steps` and W-5's shape: COPY
   TO FREE SLOT over a read-only save-state directory, the frame after),
   GAME OPTIONS, SCRAPER's three tabs and SCRAPE NOW into SCRAPING GAMES
   (with a stand-in scraper or an empty selection: NO GAMES FIT THAT
   CRITERIA. and the WARNING box), BIOS CHECK and one system's DETAILS, the
   screenshot viewer -- at EN and FR with every frame's strings read back;
   **each confirmation's back-button landing** (the frame after B on each
   YES/NO, on WRITE / CANCEL, on SAVE CHANGES?); **the two stores read** from
   `es_settings.cfg` and `system.cfg` after a tab switch and a page close on
   SCRAPER (Q2's two rewrites, with mtimes); **the manager's help bar and
   last tile on screen** at 640x480 (1280x800 is `fix-walk-pending-image`
   until `vm-pair` has `--res`); the stale-read positive (options menu
   before and after a scrape writes a game's image); the QA accounts only
   where a sign-in is needed (`tools/qa-accounts`, never printed; D-QA-016;
   never the owner's, D-QA-015). Every proof's frames are labelled by side;
   a fix's frame is `fix-walk-pending-image`.
3. **What T32 to T37 inherit** is written, not tested here: the pages'
   provenance table (3 / 9 / 64 with the merge base named), the dialog
   table's method (the first button read whole, never by a three-line
   window), the title-shape table the checker cannot see, the cached-read
   table's writers, the four tab-strip pages, and the one-file-per-page
   shape GuiMenu's option (a) would reach.
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   ES branch, proven twice (`fix-unit-test` through a harness in the four
   patterns' shape or `fix-walk-pending-image`), the harness that covers the
   function run before every commit; **a row added, moved or renamed updates
   `docs/es-menu-map.md` in the same commit and `tools/es-menu-map-check`
   passes before it (D-UI-039)**; a sentence changed updates the French in
   the same commit (D-UI-051).

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its
reason). From the distribution worktree after the membership block; `W` the
ES worktree, `PIN` the pin, `MB` the merge base, `X` the exclusion regex,
`FILES` the 76; counts by `/usr/bin/grep` (#1138); `rc=$?` on its own line,
never after a pipe:

```bash
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-pages-678; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; C=8ebaf8daad; MB=cada856d86
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t31/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
X='/(GuiMenu\.|GuiCloud|GuiRetroAchievements|GuiOfflineScan|GuiGameAchievements|GuiWifi\.)[^/]*$'
FILES=$(git -C "$W" ls-tree -r --name-only "$PIN" -- es-app/src/guis/ | $G -v -E "$X")
# the scope (expect 90 all; 14 excluded; 76 in scope; no subdirectory under guis/)
git -C "$W" ls-tree -r --name-only "$PIN" -- es-app/src/guis/ | $G -c .; git -C "$W" ls-tree -r --name-only "$PIN" -- es-app/src/guis/ | $G -c -E "$X"; printf '%s\n' $FILES | $G -c .; git -C "$W" ls-tree -r --name-only "$PIN" -- es-app/src/guis/ | sed -E 's#^es-app/src/guis/##' | $G -c '/'
# the ES worktree at the pin, clean; the two merge bases; the counts (expect the pin; 0; cada856d86; bccd715707; 14; 724; 1; f6c542872e)
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l; git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10; git -C "$W" merge-base bccd715707 "$PIN" | cut -c1-10; git -C "$W" rev-list --count "$MB"..rocknix/master; git -C "$W" rev-list --count "$MB".."$PIN"; git -C "$W" rev-list --count bccd715707.."$MB"; git -C "$W" rev-parse rocknix/master | cut -c1-10
# the lines two ways (expect wc -l 15526; grep -c 15537; 11 files without a trailing newline)
for p in $FILES; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'; for p in $FILES; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c", s}'; n=0; for p in $FILES; do a=$(git -C "$W" show "$PIN:$p" | wc -l); b=$(git -C "$W" show "$PIN:$p" | $G -c ''); [ "$a" != "$b" ] && n=$((n+1)); done; echo "no trailing newline: $n"
# the fork's delta over the slice (expect 12 rows: 9 M and 3 A -- GuiScraperRun.cpp, GuiScraperRun.h, WifiScanProcess.h; no D; the sums 1207 129; the pairs 172 88, 6 7, 2 2, 16 1, 330 23, 23 0, 258 0, 67 0, 105 7, 8 1, 18 0, 202 0)
git -C "$W" diff --name-status "$MB" "$PIN" -- es-app/src/guis/ | $G -v -E "$X"; git -C "$W" diff --numstat "$MB" "$PIN" -- es-app/src/guis/ | $G -v -E "$X" | awk '{a+=$1; r+=$2} END {print a, r}'
# upstream's delta over the slice (expect 0 slice rows, rc 1 from grep -c on no match; the excluded 152 2 GuiMenu.cpp and 1 0 GuiMenu.h; 8 upstream commits touching guis/, none a slice file; 73 slice files at the base and at master)
git -C "$W" diff --numstat "$MB" rocknix/master -- es-app/src/guis/ | $G -v -E "$X" | $G -c .; rc=$?; echo "slice rows rc=$rc"; git -C "$W" diff --numstat "$MB" rocknix/master -- es-app/src/guis/ | $G -E "$X"; git -C "$W" log --format=%h "$MB"..rocknix/master -- es-app/src/guis/ | $G -c .; git -C "$W" ls-tree -r --name-only "$MB" -- es-app/src/guis/ | $G -v -E "$X" | $G -c .; git -C "$W" ls-tree -r --name-only rocknix/master -- es-app/src/guis/ | $G -v -E "$X" | $G -c .
# the fork's commits per touched file, no merges, from bccd715707 (expect GuiSaveState.cpp 25, GuiScraperRun.cpp 4, WifiScanProcess.h 2, GuiBios.cpp 4, GuiScraperStart.cpp 5, GuiSettings.h 4, GuiSettings.cpp 3, GuiImageViewer.cpp 1, GuiGameOptions.cpp 1)
for f in GuiSaveState.cpp GuiScraperRun.cpp WifiScanProcess.h GuiBios.cpp GuiScraperStart.cpp GuiSettings.h GuiSettings.cpp GuiImageViewer.cpp GuiGameOptions.cpp; do printf '%s %s\n' "$f" "$(git -C "$W" log --no-merges --format=%h bccd715707.."$PIN" -- "es-app/src/guis/$f" | $G -c .)"; done
# the strings (expect TOTAL 891 in 37 files; GuiControllersSettings.cpp 183, GuiScraperStart.cpp 92, GuiGameOptions.cpp 59 the three largest)
git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'
# the dialogs (expect TOTAL 50 in 18 files; GuiGameOptions.cpp 8; then every site with two lines after it, read whole -- the first button is never counted from a window: WRITE at GuiGameOptions.cpp:274 and CLOSE at :289 are the two first buttons that are neither YES nor OK)
git -C "$W" grep -c -F 'GuiMsgBox(' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -n -A2 -F 'GuiMsgBox(' "$PIN" -- $FILES | sed "s/^$PIN://" > "$TMPDIR/dialogs.txt"; $G -c 'GuiMsgBox(' "$TMPDIR/dialogs.txt"
# the switches and their store (expect TOTAL 26 in 6 files; 3 lines with the literal in the 4th slot, all at GuiNetPlaySettings.cpp:38-40; 20 lines with it in the 3rd slot; every literal true; the two signatures at GuiSettings.h:88-89)
git -C "$W" grep -c -F 'addSwitch(' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -n -F 'addSwitch(' "$PIN" -- $FILES | $G -c -E 'addSwitch\(([^,]*,){3}[[:space:]]*(true|false)'; git -C "$W" grep -n -F 'addSwitch(' "$PIN" -- $FILES | $G -c -E 'addSwitch\(([^,]*,){2}[[:space:]]*(true|false)[[:space:]]*[,)]'; git -C "$W" grep -n -F 'addSwitch(' "$PIN" -- $FILES | $G -c -E 'addSwitch\(([^,]*,){2,3}[[:space:]]*false'; git -C "$W" grep -n -F 'addSwitch' "$PIN" -- es-app/src/guis/GuiSettings.h | sed "s/^$PIN://" | cut -d: -f1,2
# the reads (expect TOTAL 12 in 5 files; 0 with `, false)`; 12 FileSystem::exists; the lines at GuiFavoriteMusicSelector.cpp:19, GuiGameOptions.cpp:41 53 54 55 56, GuiImageViewer.cpp:415 629 660 723, GuiNetPlay.cpp:679, GuiNetPlaySettings.cpp:70)
git -C "$W" grep -c -F 'exists(' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -n -E 'exists\([^)]*, *false\)' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -c -F 'FileSystem::exists(' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print s}'; git -C "$W" grep -n -F 'exists(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the process starts (expect system( 0; popen( 0; runSystemCommand( TOTAL 6 in 3 files -- GuiAnalogSticksLedControls.cpp 1, GuiControllersSettings.cpp 2, GuiMoonlight.cpp 3; executeScript 5 in 1 -- GuiMoonlight.cpp; executeEnumerationScript 0)
for k in 'system(' 'popen(' 'runSystemCommand(' 'executeScript' 'executeEnumerationScript'; do printf '%s ' "$k"; git -C "$W" grep -c -F "$k" "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s+0, "in", NR, "files"}'; done; git -C "$W" grep -n -E '(^|[^A-Za-z_])(system|popen)\(' "$PIN" -- $FILES | $G -c .
# the button bars (expect clearButtons( TOTAL 3 in 2 files at GuiKeyboardtopads.cpp:78, GuiScraperStart.cpp:40 and :212; addButton( at GuiKeyboardtopads.cpp:93, GuiScraperStart.cpp:55 and :213 -- none of the three sites inside a button's lambda, read)
git -C "$W" grep -n -F 'clearButtons(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'addButton(' "$PIN" -- es-app/src/guis/GuiKeyboardtopads.cpp es-app/src/guis/GuiScraperStart.cpp | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the async surfaces (expect std::thread TOTAL 18 in 13 files; GuiLoading< 18 in 12; postToUiThread( 9 in 5; AsyncNotificationComponent 3 in 2 -- GuiUpdate.cpp 1, GuiUpdate.h 2)
for k in 'std::thread' 'GuiLoading<' 'postToUiThread(' 'AsyncNotificationComponent'; do printf '%s ' "$k"; git -C "$W" grep -c -F "$k" "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s+0, "in", NR, "files"}'; done
# the help bars (expect 79 lines naming getHelpPrompts; 8 .cpp files with no ::getHelpPrompts( definition: GuiAnalogSticksLedControls GuiCollectionSystemsOptions GuiControllersSettings GuiFavoriteMusicSelector GuiGeneralScreensaverOptions GuiMoonlight GuiNetPlaySettings GuiSystemInformation)
git -C "$W" grep -n -F 'getHelpPrompts' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -L -F '::getHelpPrompts(' "$PIN" -- $FILES | $G '\.cpp$' | sed -E 's#.*/##' | tr '\n' ' '; echo
# the parses (expect std::stoi( 0; std::stoul( 0; atoi( TOTAL 9 in 3 files; the 9 lines at GuiAnalogSticksLedControls.cpp:20-26, GuiKeyMappingEditor.cpp:156, GuiUpdate.cpp:213)
for k in 'std::stoi(' 'std::stoul(' 'atoi('; do printf '%s ' "$k"; git -C "$W" grep -c -F "$k" "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s+0, "in", NR, "files"}'; done; git -C "$W" grep -n -E 'std::sto(i|ul|l|ll|ull|f|d)\(|atoi\(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the two-line rows (expect multiLine TOTAL 8 in 3 files; addWithDescription( TOTAL 14 in 7 files; the overloads at GuiSettings.h:49 51 54 56)
for k in 'multiLine' 'addWithDescription('; do printf '%s ' "$k"; git -C "$W" grep -c -F "$k" "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s+0, "in", NR, "files"}'; done; git -C "$W" grep -n -F 'addWithDescription' "$PIN" -- es-app/src/guis/GuiSettings.h | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the reboot flags (expect 0 and 0: no page here sets or names reboot or exitreboot)
git -C "$W" grep -n -E 'setVariable\("(reboot|exitreboot)"' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E '"(reboot|exitreboot)"' "$PIN" -- $FILES | $G -c .
# the sized pages (the floor did not run this: the lane's figure, every setSize/setPosition on a GuiSettings menu in the slice, read against #540)
git -C "$W" grep -n -E 'getMenu\(\)\.(setSize|setPosition)|mMenu\.(setSize|setPosition)' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the non-ASCII comments (expect 0 files with a hit across the 76, and 0 hits adjacent to a _( ; each grep -c exits 1 on 0)
n=0; for f in $FILES; do c=$(git -C "$W" show "$PIN:$f" | $G -c -P '^\s*//.*[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "$f:$c"; n=$((n+1)); }; done; echo "files with non-ascii comments: $n"; for f in $FILES; do git -C "$W" show "$PIN:$f" | $G -n -P -A1 '^\s*//.*[^\x00-\x7F]' | $G -B1 '_\("'; done | $G -c .
# the harness sweep (expect GuiSaveState -> es-app/tests/unit/TimeTextTests.cpp; GuiSettings -> tests/cloud-content-selection.py cloud-gated-row.py cloud-oauth-lifetime.py wifi-profile-lifetime.py; GuiLoading -> tests/launch-capture-gate.py; every other class 0; 15 .py under tests/)
for c in $(printf '%s\n' $FILES | sed -E 's#.*/##; s#\.(cpp|h)$##' | sort -u); do h=$(git -C "$W" grep -l -w -- "$c" "$PIN" -- es-app/tests tests | sed "s/^$PIN://" | tr '\n' ' '); [ -n "$h" ] && echo "$c: $h"; done; git -C "$W" ls-tree -r --name-only "$PIN" -- tests/ | $G -c '\.py$'
# the menu map and the French (expect `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` -- T26's recorded line at this pin, or the counts the lane finds, named; `706 fork string(s) in the source, 706 with French, 0 without` against bccd715707 -- the line against cada856d86 is the lane's to record, unrecorded here; rc 0 for both)
out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"
out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated rc=$rc"
out=$(tools/es-untranslated --es-src "$W" --upstream "$MB" 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated(cada) rc=$rc"
# the title shapes (the lane's script under the audit folder's tools/: for each .cpp, the titles by the checker's three regexes and by the wider shapes -- expect 12 .cpp with a title by the checker's shapes, 27 .cpp with a title by the wider sweep, 12 pages whose title is in neither the map's body nor `## Not mapped`, 10 .cpp with no title by any shape -- the 12 and 27 are hand counts over the membership digest's lists, the lane's script asserts them; the map at 989 lines, `## Not mapped` at :677 with 24 lines)
python3 -I docs/audits/*-epic-m6-es-pages/tools/t31-titles.py "$W" "$PIN" docs/es-menu-map.md | tail -n 6; wc -l docs/es-menu-map.md; sed -n '/^## Not mapped/,/^## /p' docs/es-menu-map.md | $G -c -E '^- '
# the compile (expect es-syntax-check exit 2 on this host for every .cpp tried; g++'s first error named, SDL expected)
F=es-app/src/guis/GuiSaveState.cpp; out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc"
out=$(g++ -std=c++17 -fsyntax-only -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$F" 2>&1); rc=$?; printf '%s rc=%s\n' "$(printf '%s\n' "$out" | $G -m1 -E 'fatal error|error:' | cut -c1-90)" "$rc"
# the removal check -- TIPHASH is the lane's own tip the pointer and the dispatch comment name (the merge of 2174265e9c and COHASH; never 2174265e9c itself, whose tools/ differ from the coordinator's) (expect empty) and the ES diff against the pin (expect empty before stage E)
git diff --stat TIPHASH HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1
```

## 6. Outputs

As T26's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-es-pages/`:
`00` to `05`, `second-opinions/`, `guest-cycle/`, the lint before D, the
audit issue (`Audit: M6 T31 EmulationStation's other pages -- N findings
(...)`, a sub-issue of #678), the bugs, and the retro at
`docs/retros/<date>-m6-es-pages.md` (**what the slice did to the two
time-to-play numbers**: the manager's PLAY from a slot and the game options
menu are on the launch path; `copyToSlot` at `:516` and the options menu's
five cached reads at open are named with their bounds; cited from
`docs/vm-qa-log.md`; never "nothing" by default; **what T32 to T37
inherit**: § 5 item 3). **`02` carries § Coverage (76), § The pages (one row
per `.cpp` page: the title and its shape, the class and its base, what
opens it, what it runs and on which thread with what bound, its threads,
its dialogs with the button back lands on, mapped / declared / neither), §
The dialogs (one row per `GuiMsgBox(` site: the message's first words, the
buttons in order, the landing, destructive or not), § The rows (one row per
`addSwitch`/`addInputTextConfigRow`/`addWithDescription` in the slice: the
builder, the label, the key, the store, the overload, the line), § The
reads (one row per `exists(`/`isFlockHeld`/parse: the file, its writer,
cached or not, what a failure reads as), § The titles (one row per `.cpp`:
the shape, the checker's view, the map's), § The merge debt (the two merge
bases; upstream's 14 commits and the 0 slice files among them; the fork's
12 against the base), § The runs, § The guest cycle, § Positives, and every
proof with `proved:`.** The stage-D pause as T21's: the punch list posted on
#678, the lane waits for the coordinator's dispositions and any stream
brief.

## 7. Acceptance

The checklist on #678 becomes this section at dispatch, written there by
the coordinator in place of P1's generated ones. Every checkbox names the
artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-pages/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-pages/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`); Q1 to Q7 are answered in `04-analysis.md` and every punch item carries `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); its probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the three-way scan with every hit dispositioned by name and every trimmed file and range named; the running log shows exactly two keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #585, #648, #649, #665, #667, #668, #673, #776, #782, #951, #965, #63, #1192, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail.
- [ ] `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in the checklist's header carry the lane's commits; the ES read is on the pin's bytes for the 76 files (`git -C <W> diff --stat 16dbac5211 <reviewed-at-es> -- $(cat .qa-scratch/t31/paths.txt)` empty before stage E) and nothing under the distribution's `packages/`, `projects/` or `tools/` changed at any stage against the lane's own dispatch tip (the pointer's merge hash, never `2174265e9c`).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (76 paths; 15,537 by the inventory and `grep -c ''`, 15,526 by `wc -l`, 11 files without a trailing newline; inventory tiers 64 / 12 and read tiers 3 / 9 / 64; 73 in the merge base; 12 files 1207 added 129 removed -- or the deltas beside them) and the two merge bases with `cada856d86` named as the one against `rocknix/master`.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `76`.
- [ ] `02-forward-audit.md` § The pages has one row per `.cpp` in the slice (37), generated or asserted by a script under the audit folder's `tools/` that names its count, with the title's shape, the class's base, what it runs and on which thread, its dialogs' landing, and mapped / declared / neither.
- [ ] `02-forward-audit.md` § The dialogs has one row per `GuiMsgBox(` site (50, or the lane's count with its method), each read whole: the buttons in order and the button back lands on; the WRITE / CANCEL and CLOSE boxes at `GuiGameOptions.cpp:274` and `:289`, the SAVE CHANGES? boxes and the two THIS WILL DELETE boxes among them, each with its landing named.
- [ ] `02-forward-audit.md` § The rows is generated by a script under the audit folder's `tools/` (the generator asserts its row count and exits 1 on drift): the 23 `addSwitch` literals with their store, every `addInputTextConfigRow` with its store and mode, every `addWithDescription` with the overload it hits.
- [ ] `02-forward-audit.md` § The reads has one row per `exists(`/`isFlockHeld`/`atoi(` site in the slice (12 + 1 + 9): the file or line read, its writer, cached or not, and what a failure reads as; the BIOS page's empty vector and the manager's EACCES among them.
- [ ] `02-forward-audit.md` § The titles has one row per `.cpp` (37): the title by shape, whether `tools/es-menu-map-check`'s regexes see it, whether the map describes or declares it; the twelve in neither place listed with a disposition each (map, declare with reason, or not built on ROCKNIX) -- BIOS CHECK and SCRAPING GAMES first.
- [ ] `02-forward-audit.md` § The merge debt names `cada856d86` as the merge base with `rocknix/master` (`f6c542872e`), `bccd715707` as its parent and the stale `upstream/master`, upstream's 14 commits since the base and the 0 slice files among them, and the fork's 12 files with their numstat pairs.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason; the harness sweep's three lines, the menu-map check's line, both `es-untranslated` lines and the non-ASCII grep's 0 are among them; every harness the lane wrote has its FAIL-then-PASS pair recorded against the unfixed extract first.
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #678 (the comment's time; the START and RETURN posts with their first-line contract and censuses), the image by file name and `BUILD_ID` read from the guest at 640x480, the walks of the manager, GAME OPTIONS, SCRAPER's tabs and SCRAPE NOW, BIOS CHECK and the viewer with their strings read back at EN and FR and each frame labelled by side, each confirmation's back landing, the two stores' mtimes after a SCRAPER tab switch and close, the manager's help bar and last tile on screen, the stale-read positive, the disk retired with path, size and sha, the leftover check.
- [ ] `00-running-log.md` shows no image build, no fetch (the council runtime from `npm install --offline`; `rocknix/master` read from the shared refs), no handheld, the owner's accounts never named or used, no hosted account but the QA ones, no M7 root, worktree or prep directory, the guest only inside the granted window, two keyed invokes and every other council call keyless (`00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q7 are answered at their lines; every `bug` states its trace, its `Already written:` line and its VM line in one of the named families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` in the shape the lane writes; T2's four routed leads and T21's rows in this slice's files each have a disposition at their lines.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; `02` § What T32 to T37 inherit lists the provenance table, the dialog method, the title-shape table, the cached-read table and the four tab-strip pages with their lines.
- [ ] The retro exists at `docs/retros/<date>-m6-es-pages.md`, is posted on #678, says what the slice did to the two time-to-play numbers (the manager's PLAY and the game options menu named with what they cost on the guest; cited from `docs/vm-qa-log.md`), and what T32 to T37 inherit.
- [ ] `tools/es-menu-map-check --es-src <W> --ref <reviewed-at-es>` prints `0 missing` on the branch as handed back, `docs/es-menu-map.md` changed in the same commit as any row a stream added, moved or renamed, and each of the twelve undescribed titles has its disposition in the map, in `## Not mapped` with a reason, or in a punch item saying which (BIOS CHECK and SCRAPING GAMES not deferred).
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch and the ES fork's `.githooks/pre-push-test` on the ES branch before the hand-back merge; every fix on the ES branch has, recorded beside its commit, the covering harness's PASS line, its French in the same commit where a sentence changed, `tools/es-syntax-check` PASS where a toolchain exists or else the host `g++ -fsyntax-only` `CANNOT` with the missing header named, and a clean non-ASCII grep over its added lines.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back); the stage-D pause; an explicit maintainer
pause on #678; a blocker named on #678 (the seat failing its provenance
gate twice, a packet scan hit that is a value, two commands that disagree,
a block whose output differs from § 2's beyond the deltas it records, an
upstream-carried file that is not byte-identical to `rocknix/master`;
**not** the host's missing toolchain, which § 5 names and the `CANNOT`
forms absorb, and **not** the empty harness floor, which § 5 says the lane
builds); an ES worktree that differs from the pin on any of the 76 files at
stage A; or an execution limit, stated as such with the running log
current. A checkpoint is not a stop. An idle session says it is idle on
#678, **and does not end a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#678`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #678` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window granted on #678; the QA accounts only, never the
  owner's, D-QA-015/016; nothing on a handheld).
- The mini-retro at stage G, posted on #678, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (one
  expected: the fourth SKIPPED reason, Q5 -- put to the coordinator at the
  pause, never decided by the lane); the highest IDs the register on the
  coordinator's branch names at this version are D-WORKFLOW-212, D-NET-017
   and D-CLOUD-186 (the last three decided rows; `tools/register-check` is the proof; D-WORKFLOW-188
  is on the P1 branch only and the merge unites them); a row this slice
  forces takes an ID the coordinator assigns on #678.
- `tools/ceremony-check --gate` before every push of the distribution
  branch and the ES fork's `.githooks/pre-push-test` after an ES change;
  never `--no-verify`; a merge with conflicts is checked for markers; the
  ledgers united by whole entries; **a commit names its paths**; anything
  temporary under `/workspace/tmp/m6-t31/` after `df -i`, never `/tmp`; the
  window's record kept on the branch, the guest disk retired after it with
  the retirement recorded in `00` (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never inside
  a `bash -c` script**; **a row added, moved or renamed updates
  `docs/es-menu-map.md` in the same commit (D-UI-039) and
  `tools/es-menu-map-check` passes before it**; a sentence added or changed
  carries its French in the same commit (D-UI-051); a fixture that rewrites
  no path, in a bubblewrap sandbox started with `--clearenv`; the walks'
  steps under the audit folder's `stage-e/walks/`, never under `tools/`; the
  non-ASCII grep over a stream's added lines (`git diff -U0 HEAD -- <file>`,
  its `+` lines), an upstream hit recorded and not fixed.
- Commit messages `docs: ...` on the distribution branch, with `Refs #678`;
  on the ES branch the package's convention, `Refs #678, #<bug>`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#678's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the two provenance files (read directly) and the
manifest's scans; the audit issue's checkboxes all at an outcome; the
coverage table's row count (76), § The pages' and § The titles' 37 rows, §
The dialogs' 50, § The rows' generated count, § The reads' rows; every Q
bug with its three lines; **re-running on clones of both branches at their
tips under `/workspace/tmp/m6-coordinator/`: the membership block and every
§ 5 run in full** (no guest: the window's record is read, not repeated);
`register-check` on a simulated merge with the coordinator's tip; the
retro's answers; the five checkers' exit codes. The lane posts one hand-back
comment naming **both tips** and each artifact by path, writes
`reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` into
#678's body, then says it is idle. After acceptance the coordinator closes
the audit issue, prompts the lane for `audit-completion.json` and the lint
against **the audit issue**, merges the distribution branch in its turn
after the M7 candidate with the pin moved to the ES branch's tip in the same
integration commit (the ES package built before it lands), regenerates the
ledgers, posts any #585 lines in the shape the lane wrote, and closes #678
when every row is proven; the interface epic #700 closes when its slices
have.

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro takes a T31 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found. This brief's hash at dispatch
is `V2HASH`.

**What never runs in this slice:** an image build, a compiler beyond the
host's `g++ -fsyntax-only` and a generated test build, a fetch (the council
runtime from `npm install --offline`; `rocknix/master` from the shared
refs), a handheld, the owner's accounts or any hosted account but the QA
ones the window names, a guest before a grant on #678, M7's roots,
worktrees or prep directories, a change outside the 76 files,
`docs/es-menu-map.md`, the French catalog and the audit folder except under
a stream brief, a move of the pin, an es-core line without the pause's
ruling on its owner.

## Version 1: what the drafting read did not settle

Every figure above is copied from a recorded output -- the five research
digests (membership, fork pages, upstream delta, inherit, floor) and six
commands the drafter ran on 2026-10-27 (the membership block at
`2174265e9c`; the rules' and the map's heading lines; the register's rows
and highest IDs; the blindspot headings; T2's and T21's punch-list counts
and the T26 branch's audit files; #678's body and the order's § T31) --
except these, which the stranger's proof should run first:

1. **Copied from T26's brief, not re-derived**: `8ebaf8daad`, `651150fc88`,
   `/tmp/m7-m6-host-coordination-20261023.txt`, the M6 image at
   `/workspace/artifacts/m6-t2-20261023/` (`069fc2704421`), the 45-minute
   window, the menu-map check's line `55 screen(s) at 16dbac521, 31 in the
   map, 24 declared unmapped, 0 missing`, `tools/es-untranslated`'s `706
   fork string(s) in the source, 706 with French, 0 without` against
   `bccd715707`, the baseline `d72084ccad` "of 78 walk frames", the
   September time-to-play rows, `cloud-oauth-lifetime.py` at 184 lines, the
   `g++ -fsyntax-only` failure naming SDL (measured on `GuiMenu.cpp`, not on
   any file here), and the tool flags `--es-src`, `--ref`, `--upstream`,
   `--tree`, `--phase pre-issue` (the grep for them found only `box-check`'s
   and `rules-check`'s; T26's proof ran them).
2. **Not recorded anywhere**: `tools/es-untranslated --upstream cada856d86`'s
   line; every `getMenu().setSize(`/`setPosition(` site in the slice (the
   floor did not grep it; § 5 adds the run with no expectation); the counts
   of `.cpp` files with a title by the checker's shapes (12) and by the
   wider sweep (27), and of `## Not mapped` titles behind this slice's
   pages (11) -- hand counts over the membership digest's lists, not a
   tool's line; the `73` of the cat-file loop (76 less the three
   fork-added, consistent with the delta digest's "73 files at base and
   master", not run as that loop); the second button at
   `GuiGameOptions.cpp:274` and `:289`; which of the 8 bar-less `.cpp`
   files subclass `GuiSettings`; whether the `GuiMoonlight` boxes are
   reachable on a ROCKNIX image; T21's `02-forward-audit.md` path on this
   branch (its `05` at `docs/audits/2026_10_26-epic-m6-es-state-and-bridge/`
   counted 26 `## PL-`; the `02` was not at that path -- the inherit
   digest's line numbers are from `origin/feature/m6-es-state-and-bridge-668`);
   the titles and states of #776, #782, #768, #63, #196, #37, #301, #791,
   #222, #700 (the `gh` list of the 400 most recent did not reach them;
   quoted from the inherit digest).
3. **Two digests disagreed** ("21 doctest files under `es-app/tests/unit/`" against 19 names): the proof counted 19 `.cpp` under `es-app/tests/unit/` at the pin, every one a `*Tests.cpp`; settled.
4. **Lines counted from hunk headers** in the fork-pages digest (its `≈`
   marks): `GuiSaveState.cpp:48-245`, `:95-189`, `:246-321`, `:323-334`,
   `:336-363`, `:365-384`, `:386-399`, `:575`; `GuiBios.cpp:33-38`,
   `:48-100`, `:65`, `:300-311`; the lane's `git grep -n` settles each.
5. **Judgements the drafter made**: the seven questions' grouping (eleven
   families folded into Q1 to Q7 because the lint and #678's body expect
   seven); the packet's trimming shape; the guest plan; the es-core owner
   "T35's by the inherit digest's reading"; which pages are the fork's
   lanes under D-UI-079; § 5 item 3's inheritance list; the acceptance
   thresholds (37 page rows, 50 dialog rows, 12 + 1 + 9 read rows); T20 and
   T21 "accepted" (read from the futro's errata headings, not the issues);
   `0 missing` expected on the branch as handed back; the fourth SKIPPED as
   the one register row expected; the `grep -c` exit-1-on-zero notes in the
   runs block (the shell's behaviour, not a recorded output).
6. **Not run by the drafter**: any command in the ES repository (the
   digests ran theirs through `git -C .../qa-integration`);
   `tools/archaeology` over the register's 7 "save state manager" and 16
   "scrape" mentions (`grep -c -i -F`, mentions not rows); the walk files
   beyond `wc -l` and the `claims.txt` lines named.

## Version 2: what the stranger's proof of version 1 corrected (2026-10-27)

A reader with no context ran the membership block and the first eight runs of
§ 5 from the P1 clone and the pin, resolved `rocknix/master` and the merge
base, checked the four tool flags, the 36 rule-file citations and the menu
map's figures (82 checks; the coordinator's `t31-proof.md`). Everything held
except these seven, corrected above in place:

1. `GuiSaveState.cpp`'s WINDOW_HEIGHT is at `:43` (`:42` is a comment).
2. `claims.txt`'s `manager-*` claims run `:160-230`, not `:160-168`.
3. `GuiKeyboardLayout.cpp:164` calls `Utils::FileSystem::writeAllText`; the
   unchecked `fopen "wb"` is `FileSystemUtil.cpp:1434`, T21's file (the site
   is Backlog #1186's).
4. `GuiSettings.h:84` declares `addInputTextConfigRow`; `:151` is
   `buildInputTextConfigRow`.
5. VIEW OPTIONS in the menu map is the SELECT row at `:90`, under `## Two
   ways in` at `:83`.
6. The unit test files under `es-app/tests/unit/` are 19 `.cpp`, not 21.
7. `bugs-are-agent-first.md:53` is `## The rules`; rule 6 is at `:76`.

Settled without correction: the NFC box at `GuiGameOptions.cpp:274` is
WRITE / CANCEL (`:298`) and the `:289` box is a single CLOSE; `cada856d86`
was committed 2026-09-28 (authored 09-23); `ThreadedScraper.cpp` lives under
`es-app/src/scrapers/`.

## Errata at acceptance (2026-10-27)

Found by the lane in stages A to E and by its seat, each recorded on #678; the brief's text above is left as dispatched (the errata practice: appended, never edited in).

1. **§ 5, the non-ASCII run (`:830`):** the adjacency grep `$G -B1 '_\("'` is a basic-regex error (`\(` opens a group) and printed `Unmatched ( or \(` once per file. The run is `-F '_("'` over the same `-A1` windows: 0 adjacent non-ASCII comments at the pin (stage A, `stage-a/reruns.txt`).
2. **The seeded pointer** carried T26's "The lens" and "The rule" sentences (two files, 11,883 lines); the lane rewrote both at stage A. A kit derived from a predecessor's is read line by line before seeding (T32's was).
3. **`popen` is 1, not 0:** `GuiMoonlight.cpp:42` writes `popen (` with a space, which the brief's census pattern missed.
4. **`GuiKeyboardLayout.cpp:164`** writes `/tmp/kblayout-N.svg`, not a file on the card.
5. **The LED parse** (`GuiAnalogSticksLedControls.cpp`) is guarded by `tokens.size() == 7`; the brief's lead assumed it unguarded.
6. **The tab-switch `save()`:** the brief's "writes `es_settings.cfg` on every tab switch" and the lane's stage-B correction ("only when a value changed") are both partial: a save function stores a value the player never chose on a first visit (the default scraper set, PL-21, #1254) and that counts as a change; the mtimes stand as observations (the seat's correction at stage C).
7. **`GuiAutoScrape.{cpp,h}`** are in no build list (`es-app/CMakeLists.txt:315`): never compiled, while the inventory records both as `shipped` (PL-25, Backlog #1235).
8. **The dialog table:** 50 `GuiMsgBox` sites at the pin; back lands on OK at 30, NO at 18, CANCEL at 1, CLOSE at 1, by `GuiMsgBox.cpp:116-134`'s rule read from the source; the brief's hand counts are replaced by the lane's generated table (`tools/t31-dialogs.py`).
9. **The rows census:** 21 active switches, not 23; two `addSwitch` calls sit inside a `/* */` block (the seat's correction; the parser fixed with constructed cases).
10. **The stream brief's S6 (`t31-streams.md`, § The order and the rulings' item 2):** `git cherry-pick -x a73ed9efc` does not apply alone -- it rests on `e38dcdefd` (creates `StatusText`) and `31b49999e` (changes `ApiSystem.*`), both T21's; superseded by the 15:12 UTC ruling: S6a at the pin, S6b a proven patch for the integration after T21's merge (`stage-e/s6b.patch`, `s6b-merge.diff`). The coordinator's error: a cherry-pick ruled without reading the commit's parent chain.
11. **Three runs the brief wrote as expectations could not run before dispatch** (the generators' final signatures, the build script, the pointer's hashes); the acceptance reads the lane's recorded runs in `02` § The runs for those.
