# Review brief: M6.P2 T33, EmulationStation's system layer: game lists, collections, metadata, and the fork's helper units (#680)

**Version 1, drafted 2026-10-27 from the five research files; not yet proved.**
(D-WORKFLOW-189; `docs/reviews/plan-for-the-plan.md` § 6b `:301`, § 6c `:374`,
§ 7 `:397`.) The five read-only digests this version was drafted from
(membership, fork changes, upstream delta, inherit, floor) are the
coordinator's scratch files, not in any tree, so every figure they gave is
either reproduced by a command below at the hash it names, with
`/usr/bin/grep` and never the shell's function (#1138), or marked
`[unverified: run <command>]`. The drafter ran ten `git -C` reads against
the `qa-integration` checkout at the pin and quotes each beside its figure
in § 2 and § 5; the stranger's proof of this version runs the membership
block, the § 1 commands and the § 5 runs, and version 2 applies what it
corrects. The structure is T32's brief (`es-app-views-scrapers.md`, version
2 at `85307da3b3`); every T32-specific paragraph is replaced.

## 1. Identity

- **Issue:** #680 `M6.P2 E339/T33: interface: EmulationStation's system
  layer: ApiSystem, game lists, collections, metadata` (the live title,
  read 2026-10-27, OPEN, milestone `M6: Codebase renovation`, no labels),
  **retitled at dispatch to `M6.P2 E700/T33: interface: EmulationStation's
  system layer: game lists, collections, metadata, and the fork's helper
  units`** (`milestone-phase-naming.md`; the body says *"under epic #339
  until this area's epic is filed"*, and #700 is filed; #678 and #679 were
  retitled the same way). Slice `es-app-system` (`k: 33`) in
  `docs/reviews/slices.json`, thirty-third in `docs/reviews/order.md`
  (`order.md`, `slices.json` and `inventory.json` are the P1 branch's, which
  the lane's worktree is stacked on; the drafter read them in the P1
  research clone `/workspace/tmp/m6-coordinator/t11-research/tree` at
  `2174265e9c`; its § T33 at `order.md:613-621`: *"77 paths, 16,276 lines,
  16,210 read, of which 4,522 fork-own; 0 patch and config lines; reach
  shipped 77"*; its `why`: *"the rest of `es-app`: `ApiSystem.cpp` (3,519
  fork-own lines) is the bridge to the OS scripts; game lists, collections
  and metadata hold the player's library"*; **kind currency; lens cost
  against value**; read before none; depth Independent, *"an ordinary code
  slice"*; interacting subsystems *"the OS scripts `ApiSystem` calls
  (`os-launch-control-state`, os-system-services); `gamelist.xml` (game
  content, D-CLOUD-049)"*; closing evidence *"audit folder, lint PASS,
  punch list through Phase 7"*). The selector is one object:
  `globs: ["es:es-app/**"]`, `rest: true`, area `interface` by default.
  **Epic:** #700 `M6.P2 E339: Area epic: the interface, EmulationStation
  (T2, T18, T20, T21, T26, T31 to T37, T44)`: T2 #649, T18 #665, T20 #667,
  T21 #668 and T26 #673 are **accepted, and their issues stay open** until
  the integration moves the pin on `next` (§ 10); T31 #678 was accepted
  2026-10-27 (its errata are the futro's `:932`); T32 #679 is in flight
  (dispatched 16:0x UTC; its guest window started 16:08:36 UTC, § 1's last
  command shows it); this slice; T34 to T37 and T44 after. The futro
  `docs/futros/2026-10-23-m6-interface.md` (934 lines) takes a T33 kickoff
  addendum written by the coordinator with this version, after its T32
  addendum at `:914` and the T31 acceptance errata at `:932`.
  **Milestone:** M6. **Predecessors:** T2 #649, T18 #665, T20 #667, T21
  #668, T26 #673, T31 #678 and T32 #679 (in flight) each routed items here
  by name, and the menu map `docs/es-menu-map.md` (D-UI-039 at `:668`)
  declares three of the slice's surfaces unmapped; every one is listed with
  its lines and its disposition in § 2 under *Already found; do not
  re-find; take up*, which is the one place they live. **Beside it:** T32's
  lane, which holds the running session and today's guest window; the host
  shared through `/tmp/m7-m6-host-coordination-20261023.txt`; a window for
  this slice is asked for on #680 and granted there and in that file's
  queue (§ 5 item 2 says how).
- **The order's title and why are half true of the membership, and this
  brief says so rather than the lane re-deriving it.** `ApiSystem.{cpp,h}`
  (the *"bridge to the OS scripts"*, 3,519 + 490 inventory lines) is
  **T21's** by a non-rest glob (`es:es-app/src/ApiSystem.*`, read at
  Extended depth under #668); `FileData.*` and `SystemData.*` (*"the
  player's library"*) are **T2's** (#649); `CloudText.*` is **T18's**
  (#665, by the glob `es:es-app/src/{CloudText,ThreadedCloudSync,CloudTransferJob}.*`).
  A `rest` selector takes, within its areas, only the rows no non-rest
  selector of any slice claims (`tools/renovation-inventory:1237-1246` at
  `2174265e9c`), and that is exactly what those globs are. **So T33 is
  three things** (the membership digest's § 8, reproduced by the block in
  § 2): (1) **the upstream library layer the title promises** --
  `Gamelist`, `CollectionSystemManager`, `MetaData`, `FileFilterIndex`,
  `FileSorts`, `FileTag`, `Genres`, `LangParser`, `PlatformId`,
  `CustomFeatures`, `SystemScreenSaver`, `SystemRandomPlaylist`,
  `KeyboardMapping`, `ContentInstaller`, `ThreadedBluetooth`,
  `ZaparooSupport`, `LibretroRatio`, the two animations,
  `components/ScraperSearchComponent`, `EmulationStation.h`: 40 files,
  every one byte-identical to `rocknix/master` today and untouched by
  upstream since the merge base, plus `ScraperCmdLine.{cpp,h}`,
  upstream-carried and **in no CMake list** (290 + 7 lines, last upstream
  commit `8d7fb7b3e8` 2019-04-25; the `GuiAutoScrape` shape of Backlog
  #1235, where the coordinator has added them); (2) **29 small fork helper
  units whose pages live in other slices** -- `CaptureRotation{,Text}.*`
  (T2's `FileData.cpp` reads them), `DisplayAspect{,Text}.*` (T32's
  views), `CheevosIndex.*`, `CheevosRetry.*`, `OfflineAchievementsText.*`,
  `RunLock.h`, `GameCubeRvzHashRetry.h` (T20's pages and hasher),
  `CloudExit.h`, `CloudOffer.*`, `CloudFolderValidation.*`,
  `JourneyTiers.h`, `TextFit.h` (T18's cards and T26's menu), `WifiText.*`
  (T21's `ApiSystem.h` and T31's `GuiWifi`), `AppWindow.h`,
  `FolderMerge.h`, `NetworkThread.*`, and the `es-app/CMakeLists.txt` that
  lists them: 2,689 fork insertions in all; (3) **Windows residue** no
  ROCKNIX image compiles -- `Win32ApiSystem.{cpp,h}` (`:1` is `#if WIN32`,
  `:1267` `#endif`, so an empty translation unit on every image),
  `EmulationStation.rc` (MSVC only, `es-app/CMakeLists.txt:292-296`),
  `es_icon.ico` (34,494 bytes, reached only through the `.rc`),
  `EmulationStation.aps` (356,792 bytes, a resource-editor cache no build
  file names), `EmulationStation.h.in` (the `INJECT_VERSION` template
  under `if(WIN32)`, `:3-29`). The order's sentence is corrected on the P1
  branch at the inventory's regeneration (#1235), not by the lane; the
  retitle at dispatch is the coordinator's.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of scope:
  those are the coordinator's, reached through #680, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already written:`
  line (D-WORKFLOW-187). A fix lands only under a stream brief the
  coordinator writes at the stage-D pause, **on the EmulationStation
  branch**. **Forty-six of the 77 paths are byte-identical to ROCKNIX's
  master today, 27 were added by the fork and 4 are the fork's by
  modification** (`es-app/CMakeLists.txt` +44/-0, `NetworkThread.cpp`
  +105/-3, `NetworkThread.h` +29/-1, `Win32ApiSystem.cpp` +3/-3): `git
  diff --shortstat bccd715707 PIN` over the 77 prints `31 files changed,
  2689 insertions(+), 7 deletions(-)`, and the same line against
  `cada856d86` and against `rocknix/master`. So the inventory's `fork-own`
  tier (31 files, 4,522 lines) is the read's **fork-added 27 /
  fork-modified 4 / upstream-carried 46**, and 1,269 of the 4,522 are
  `Win32ApiSystem.cpp`, whose fork change is three logging lines inside
  the `#if WIN32` (§ 2). A defect in a line the fork wrote is the fork's to
  fix; a defect in an upstream line is a contained fix under
  `bugs-are-agent-first.md` rule 6 (`:76`) and a #585 line (D-WORKFLOW-164,
  never sent, D-WORKFLOW-165). D-UI-079's lanes
  (`engineering-practices.md:12`): the cloud offer and the tiers record, the
  captures' aspect and turn, the offline achievements' text, the Wi-Fi
  rows' text, the token check's retry at link-up, the rescan's merge, the
  game list the cloud's content restore brings (D-CLOUD-049) are the lanes
  the fork works in; an upstream surface's *behaviour* -- the content
  installer's card, the Bluetooth scan, the screensaver, Zaparoo, the
  key-to-pad editor, the collections flow -- is read for brittleness and
  cost (the lens) and left as upstream has it, and a defect in one is still
  ours to close when the fix is contained (rule 6). The read is the pin
  `16dbac5211`'s bytes; M7's worktrees are never read.
- **Ownership rulings, stated once.** (a) `es-core/src/Scripting.cpp`
  (T2's FD-9/FD-19 quoting lead, routed *"T33/T21 `Scripting`"* at T2
  `05:610`) is es-core's, in no es-app list, outside the 77: **recorded as
  inherited in `02` and routed to the es-core slice the order gives that
  file** (the inherit digest's reading of `es-pages.md:415-418` is T35);
  the lane writes no line in it. (b) `CloudText.{h,cpp}` are **T18's**
  (above); the lane reads them as a neighbour only. (c)
  `DisplayAspect.cpp`'s interface-thread walk (T31 PL-26, T32 L-14) and
  `CollectionSystemManager.cpp`'s `reloadCollection`-then-`reloadGameListView`
  (T32 L-16, the #246 shape) are **T33's**: both files are in the 77, and
  T32's brief (`:429-431`) and T31's `04:80` left the owner to the
  coordinator, who confirms it here. (d) `AppWindow.h` (T2's PC-1) is
  **T33's**, with T2's finding inherited. (e) The three `writeAllText`
  sites under Backlog #1186 (`CaptureRotation.cpp:175`,
  `KeyboardMapping.cpp:426`, `:429`) are **T33's to fix or to record under
  #1186**, the ruling at stage D. (f) `GameCubeRvzHashRetry.h:35-48`,
  *"by design"* at T20 `02:167` against open #609: read, recorded, the
  ruling at stage D. (g) `NetworkThread.cpp:248`/`:251`/`:237` are the
  callers' side of T20's #1170 and #301 and of `ProxyCards::linkReturned`;
  T33 owes the callers' read, not the hasher's.
- **Two worktrees, one session, and four placeholders.** The distribution's
  `feature/m6-es-app-system-680` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-app-system-680`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (or the P1 tip the dispatch comment names, should #1235's
  regeneration have moved it) with the coordinator's tip merged in and the
  lane's pointer seeded; and the EmulationStation fork's
  `feature/m6-es-app-system-680` at
  `W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-system-680`,
  cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`**
  and clean until stage E: the sources are read and the fixes are made
  there, and the pin is not moved by the lane. **`W` is that one path in
  every block of this brief; until it exists -- neither worktree does
  before dispatch, and `git -C <qa-integration> rev-parse --verify
  origin/feature/m6-es-app-system-680` prints `fatal: Needed a single
  revision` today -- the `qa-integration` checkout at the same pin, clean,
  stands in, read by `git -C` only, and gives the same lines (the drafter
  ran every quoted command there).** **Four placeholders stand in this
  brief for hashes that do not exist until dispatch:** `COHASH` (the
  coordinator's tip merged into the lane's branch), `MERGE_HASH` (that
  merge commit, the lane's dispatch tip), `TIPHASH` (the lane's own tip as
  it moves; at stage A it is `MERGE_HASH`) and `V2HASH` (this brief's
  commit on the coordinator's branch). The dispatch comment on #680 and the
  seeded pointer carry their values; the lane reads them there, never
  guesses them, and § 9's placeholder check names all four. **Two other
  lanes' ES branches have already changed files inside the 77** (§ 2):
  T21's `feature/m6-es-state-and-bridge-668` at `3ae9610b0`
  (`es-app/CMakeLists.txt` +10/-0 over six commits; `WifiText.cpp` +11/-0
  and `WifiText.h` +13/-0 at `00669ccd9`, #1194) and T20's
  `feature/m6-es-achievements-pages-667` at `5c0ddaaee`
  (`OfflineAchievementsText.cpp` +99/-0 and `.h` +52/-0 at `274a71add`
  and `f85061f14`, #1174 and #1173); T2's, T18's, T26's and T31's touch
  none of the 77 (`git diff --numstat PIN <tip> -- <77>` empty for each).
  The lane reads the pin for the audit and reads those tips for the deltas,
  recording each as inherited in `02`; a T33 fix that touches the same
  lines is written against the pin and the integration's merge (the
  coordinator's) reconciles; the lane names each such collision in the
  hand-back. The other ES checkouts under
  `~/Development/emulationstation-next.worktrees/` are other lanes' and
  M7's: read with `git -C <checkout> show <hash>:<path>` only;
  `rocknix/master` is read from the shared refs, never fetched
  (`upstream/master` in that repository is a stale copy 15 commits behind,
  § 2). Until the dispatch comment exists the pointer is not seeded and
  nothing starts.
- **Depth: Independent** -- one seat from another lab (plan § 6c `:374`,
  D-WORKFLOW-137; `adversarial-council.md`: an Anthropic-led audit's
  reviewer is pinned GPT-6 Astra; no Gemini seat): Astra at `max` over a
  trimmed, scanned packet (D-WORKFLOW-195 -- **the 27 fork-added files
  whole** (2,508 lines by subtraction from the numstat, a derived figure
  the lane replaces with the packet's own `wc -l`), **the fork's hunks of
  the 4 modified** (`es-app/CMakeLists.txt`'s five additive hunks,
  `NetworkThread.cpp`'s ten, `NetworkThread.h`'s seven, and
  `Win32ApiSystem.cpp`'s three one-line hunks at `:316`, `:341`, `:368` --
  never that file whole), and **of the 46 upstream-carried files only the
  ranges the questions cite**; `EmulationStation.aps` and `es_icon.ico`
  are binaries and never go in; the manifest names every trimmed file and
  range), a probe then one refutation (one in-call retry allowed);
  `review-plan.json` records depth `independent` and the one reviewer with
  its served model; **exactly two keyed `tools/council/run invoke` calls**,
  every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`
  (the runner reads that variable at `tools/council/run:21`, default
  `~/.config/council/env`; the recipe is `.claude/skills/council/SKILL.md`
  and its `references/`; the runtime under `tools/council/` from `npm
  install --offline`, no fetch). The packet is scanned before it leaves.
  **The credential macros are not in this slice:** `es-app/CMakeLists.txt`
  carries only source lists (the macro-name grep over it hits only the
  substrings of `IGDBScraper`, `GamesDBJSONScraper`, `HfsDBScraper`,
  `ScreenScraper`, `CheevosRetry` and `CheevosIndex` file names); the
  macros by name live in the **top-level** `CMakeLists.txt:303-329`
  (`SCREENSCRAPER_DEV_LOGIN` `:307-308`, `:314`;
  `SCREENSCRAPER_RUNTIME_DEV_LOGIN` `:313`, `:316-317`; `GAMESDB_APIKEY`
  `:320-321`; `CHEEVOS_DEV_LOGIN` `:324-325`; `HFS_DEV_LOGIN` `:328-329`),
  outside the 77, read from the environment and never from the tree. What
  the scan will hit inside the 77: `Win32ApiSystem.cpp:98` names
  `CHEEVOS_DEV_LOGIN` (macro name, inside the dead block);
  `NetworkThread.cpp:130-131` reads the account's sign-in pair from
  `SystemConf` by key name and `:268-269` writes the token key (setting
  names); `KeyboardMapping.cpp`'s JSON field `"key"` and `KeyName` tables
  (identifiers); `RunLock.h`'s `holder` (identifier);
  `OfflineAchievementsText.h:99`'s `HttpReq` comment -- so
  `packet-manifest.json` records **every scan hit dispositioned by
  file:line** (library plumbing / macro name / identifier / setting name /
  value), and a hit that is a value stops the packet; no value ever reaches
  the packet or an artifact.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the distribution worktree; `8ebaf8daad`
  is `next`'s commit the P1 branch stacks on and `651150fc88` is
  `upstream/next`'s, both copied from T32's brief and proved there:
  `651150fc88` is *Merge pull request #3547 from spycat88/qcom-bls*,
  `8ebaf8daad` is *browser: record provider pages and GTK4 compilation
  (#616)*; the coordinator worktree at `ce8608e38f` has `8ebaf8daad` as an
  ancestor today):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-app-system-680
cat .github/sessions/saved-session-state-feature-m6-es-app-system-680.md    # the pointer: the dispatch's two hashes; § 10 names the lines to check
git status --short | wc -l                                                   # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1               # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-system-680; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                # the pin; 0
git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10                     # cada856d86: the merge base with ROCKNIX's master (not bccd715707, § 2)
git -C "$W" rev-parse --verify rocknix/master | cut -c1-10                    # f6c542872e, read from the shared refs
git -C "$W" rev-parse --verify origin/feature/m6-es-state-and-bridge-668 | cut -c1-9     # 3ae9610b0: T21's ES tip, whose CMakeLists and WifiText deltas § 2 names
git -C "$W" rev-parse --verify origin/feature/m6-es-achievements-pages-667 | cut -c1-9   # 5c0ddaaee: T20's ES tip, whose OfflineAchievementsText deltas § 2 names
git show origin/feature/m6-es-state-and-bridge-668:docs/audits/2026_10_26-epic-m6-es-state-and-bridge/05-punch-list.md | /usr/bin/grep -c '^## PL-'   # 26: PL-20 is routed here (#1186)
tools/register-check >/dev/null && echo register-ok
tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200           # who holds the host: no guest before a grant on #680
```

Every line above except the first `cat` and the two `rev-parse` of the
lane's own worktree ran today in the coordinator worktree and
`qa-integration` (the ES lines) and printed what its comment says; the
`cat` cannot run before the pointer is seeded, and `W` does not exist
before dispatch.

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{inventory.json,slices.json}`; the script is the membership
digest's, verbatim, a rewrite of `tools/renovation-inventory`'s `glob_body`
grammar (`**/`, `**`, `*`, `?`, `{a,b}`) and of its rest semantics
(`:1237-1246`); two `sort`/`sorted` keyword arguments are spaced `key =
lambda` so this file carries no `key=` token, and the script as run wrote
them unspaced; nothing else differs. It takes a paths file as its one
argument and prints; run it twice -- first against `/dev/null` to make the
paths file from its own TSV, then against that file to prove equality):

```bash
mkdir -p .qa-scratch/t33
python3 -I - /dev/null > .qa-scratch/t33/block-1.txt <<'PYEOF'
import json, re, sys, collections
CODE = {"shell","python","recipe","c","c++","c-header","c++-header","javascript","typescript","make","cmake","systemd","udev","script","perl","lua","rust","go","assembly","shader","docker","kconfig","html","css"}
def gre(g):
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i]=="?": out+="[^/]"; i+=1
        elif g[i]=="{":
            j=g.index("}",i); out+="(?:"+"|".join(gre(x) for x in g[i+1:j].split(","))+")"; i=j+1
        else: out+=re.escape(g[i]); i+=1
    return out
def compile_globs(globs):
    inc=collections.defaultdict(list); exc=collections.defaultdict(list)
    for g in globs:
        neg=g.startswith("!"); g=g[1:] if neg else g
        tree="es" if g.startswith("es:") else "distribution"
        g=g[3:] if tree=="es" else g
        (exc if neg else inc)[tree].append(re.compile(gre(g)+r"\Z"))
    return inc,exc
doc=json.load(open("docs/reviews/slices.json"))
sl=[]
for s in doc["slices"]:
    sels=s.get("select",{}); sels=sels if isinstance(sels,list) else [sels]
    comp=[]
    for sel in sels:
        comp.append((set(sel.get("areas",[s["area"]])), compile_globs(sel["globs"]) if sel.get("globs") else None,
                     set(sel["reach"]) if sel.get("reach") else None, bool(sel.get("rest")), set(sel["tier"]) if sel.get("tier") else None))
    sl.append((s,comp))
inv=json.load(open("docs/reviews/inventory.json"))
cols=inv["columns"]; print("columns:",cols)
rows=[dict(zip(cols,r)) for r in inv["rows"]]
def match(row,areas,comp,reach,tier):
    if row["area"] not in areas: return False
    if reach and row["reach"] not in reach: return False
    if tier and row["tier"] not in tier: return False
    if comp is None: return True
    inc,exc=comp; t=row["tree"]; p=row["path"]
    return any(r.match(p) for r in inc.get(t,())) and not any(r.match(p) for r in exc.get(t,()))
def hits(row):
    non=[s["id"] for s,c in sl if any(not rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)]
    if non: return non,"non-rest"
    return [s["id"] for s,c in sl if any(rest and match(row,a,cm,r,t) for a,cm,r,rest,t in c)],"rest"
kof={s["id"]:s["k"] for s,_ in sl}
mine=[]
for r in rows:
    if r["tree"]!="es": continue
    h,kind=hits(r)
    if h==["es-app-system"]: mine.append(r)
mine.sort(key = lambda r:r["path"])
want=[l.strip() for l in open(sys.argv[1]) if l.strip()]
got=[r["path"] for r in mine]
print("mine:",len(got),"paths.txt:",len(want),"equal:",got==want)
print("only-mine:",sorted(set(got)-set(want))); print("only-paths.txt:",sorted(set(want)-set(got)))
c=collections.Counter
print("lines:",sum(r["lines"] or 0 for r in mine), "reach:",dict(c(r["reach"] for r in mine)),"tier:",dict(c(r["tier"] for r in mine)),"lang:",dict(c(r["language"] for r in mine)))
print("fork-own lines:",sum((r["lines"] or 0) for r in mine if r["tier"]=="fork-own"))
print("read lines:",sum((r["lines"] or 0) for r in mine if r["language"] in CODE and r["tier"]!="vendor-carried" and r["reach"]!="unreached"))
print("TSV"); print("\t".join(cols))
for r in mine: print("\t".join(str(r.get(k)) for k in cols))
print("CLAIMS")
named=["es-app/src/ApiSystem.cpp","es-app/src/ApiSystem.h","es-app/src/FileData.cpp","es-app/src/FileData.h","es-app/src/SystemData.cpp","es-app/src/SystemData.h","es-app/src/CollectionSystemManager.cpp","es-app/src/CollectionSystemManager.h","es-app/src/Gamelist.cpp","es-app/src/Gamelist.h","es-app/src/MetaData.cpp","es-app/src/MetaData.h","es-app/src/FileFilterIndex.cpp","es-app/src/FileFilterIndex.h","es-app/src/Win32ApiSystem.cpp","es-app/src/CloudText.cpp","es-app/src/CloudText.h","es-app/src/OfflineAchievementsText.cpp","es-app/src/OfflineAchievementsText.h","es-app/src/NetworkThread.cpp","es-app/src/NetworkThread.h","es-app/CMakeLists.txt"]
byp={r["path"]:r for r in rows if r["tree"]=="es"}
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY"); continue
    h,kind=hits(r); print(p, "in-T33" if p in got else "not-in-T33", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"area",r["area"])
print("ES-APP BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="es" and r["path"].startswith("es-app/"):
        h,kind=hits(r); cnt[(tuple(h),kind)]+=1; ln[(tuple(h),kind)]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)
PYEOF
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="es" {print $2}' .qa-scratch/t33/block-1.txt > .qa-scratch/t33/paths.txt
wc -l .qa-scratch/t33/paths.txt                                             # 77
# the second pass, the same script with the paths file as its argument (the heredoc repeated, not shown twice here):
# python3 -I - .qa-scratch/t33/paths.txt > .qa-scratch/t33/block-2.txt <<'PYEOF' ... PYEOF
/usr/bin/grep -E '^(mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t33/block-2.txt
W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-system-680; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
T=$(/usr/bin/grep -v -E '\.(aps|ico)$' .qa-scratch/t33/paths.txt); printf '%s\n' $T | wc -l           # 75 text paths
for p in $T; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l text", s}'            # 16272
for p in $T; do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c text", s}'   # 16276
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t33/paths.txt | wc -l   # 50: the upstream-carried 46 and the 4 modified
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN BASE: $p"; done < .qa-scratch/t33/paths.txt | wc -l   # 50
git -C "$W" diff --shortstat "$MB" "$PIN" -- $(cat .qa-scratch/t33/paths.txt)           # 31 files changed, 2689 insertions(+), 7 deletions(-)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $(cat .qa-scratch/t33/paths.txt)     # the same line
```

Expected, at `2174265e9c` (the membership digest ran the script in the P1
research clone on 2026-10-27 against the coordinator's own 77-line list and
printed `mine: 77 paths.txt: 77 equal: True`, `only-mine: []`,
`only-paths.txt: []`; the first pass above, against `/dev/null`, prints
`mine: 77 paths.txt: 0 equal: False` with every path under `only-mine`, and
the second pass prints the digest's three lines), the block's exact output
lines:

```
mine: 77 paths.txt: 77 equal: True
only-mine: []
only-paths.txt: []
lines: 16276 reach: {'shipped': 77} tier: {'fork-own': 31, 'upstream-carried': 46} lang: {'cmake': 1, 'other': 4, 'c-header': 41, 'c++': 31}
fork-own lines: 4522
read lines: 16210
```

then, under `CLAIMS`, the 22 named paths with their claimant: `ApiSystem.cpp`
and `.h` `not-in-T33 non-rest [('es-state-and-bridge', 21)]` (tiers
fork-own, 3519 and 490 lines); `FileData.*` and `SystemData.*` `not-in-T33
non-rest [('es-launch-path', 2)]`; `CloudText.*` `not-in-T33 non-rest
[('es-cloud-pages', 18)]`; `CollectionSystemManager.*`, `Gamelist.*`,
`MetaData.*`, `FileFilterIndex.*`, `Win32ApiSystem.cpp`,
`OfflineAchievementsText.*`, `NetworkThread.*` and `es-app/CMakeLists.txt`
`in-T33 rest [('es-app-system', 33)]`; and under `ES-APP BY SLICE` the
eight rows that sum to 269 paths: `77 paths 16276 lines (('es-app-system',),
'rest')`, then `es-pages` 76 / 15,537, `es-app-views-scrapers` 42 / 17,311,
`es-cloud-pages` 30 / 11,193, `es-launch-path` 20 / 11,287,
`es-achievements-pages` 16 / 4,929, `es-state-and-bridge` 6 / 5,905,
`es-guimenu` 2 / 11,883 -- no `es-app/**` row unassigned or ambiguous. Then
the ES lines: 75 text paths, `wc -l text 16272`, `grep -c text 16276`, 50 at
the merge base and 50 at the base, and the shortstat line twice (the
drafter's reads of 2026-10-27, with `W` the `qa-integration` checkout).

**Three things the figures hide, settled here so the lane does not
re-derive them.** (1) **The inventory counts lines as `grep -c ''` does**
over the 75 text files, the unterminated last line included and the two
binaries counted as none: four slice files end without a newline
(`EmulationStation.h.in` 26/27, `KeyboardMapping.cpp` 816/817,
`LangParser.cpp` 241/242, `NetworkThread.cpp` 273/274), so `wc -l` sums to
16,272 and `grep -c ''` to 16,276 -- the same bytes, two counting rules; a
figure in `02` says which. The order's *"16,210 read"* is the inventory's
rule (`language in CODE`, tier not vendor-carried, reach not unreached): the
16,276 less `EmulationStation.h.in` (27) and `EmulationStation.rc` (39),
both `other`. The same two rules reach every count in this brief: `git
grep -c` counts **lines** and `git grep -o | wc -l` counts **occurrences**,
and § 5 states both for `_("` (176 lines, 223 occurrences) and
`Utils::FileSystem::exists(` (83 lines, 86 occurrences). (2) **"4,522
fork-own" is the lines of the 31 files the fork touched, not the lines the
fork wrote.** The inventory's `tier` is per file
(`tools/renovation-inventory:568-569`, `fork_own = path in forkset`), so
`Win32ApiSystem.cpp` counts whole (1,269 of the 4,522) for a +3/-3 change
inside `#if WIN32`; the fork's own insertions over the 77 are **2,689** and
its deletions 7, the tool's line. So the read's tiers are **fork-added 27,
fork-modified 4, upstream-carried 46**, and `02` § Coverage carries both
tiers. (3) **The merge base with ROCKNIX's master is `cada856d86`, not
`bccd715707`.** `rocknix/master` is
`f6c542872e3850c5f432929ead219547a897cd4a` (2026-10-23, *Merge pull request
#54 from porschemad911/s922x-suspend*); the pin's merge base with it is
`cada856d86e3115fbbf0bce09dd761b0ee8fa9fd`, one commit after `bccd715707`
(`rev-list --count bccd715707..cada856d86` = 1; `bccd715707..PIN` = 725;
`cada856d86..rocknix/master` = 14), and `bccd715707` is the base every
earlier ES brief named because the repository's `upstream/master` ref was
never fetched and still points there. For this slice the difference is
nothing: `cada856d86` touched `ApiSystem.{cpp,h}`, `GuiMenu.{cpp,h}` and
`GuiWifi.{cpp,h}`, none of them here, and `git diff --stat bccd715707
cada856d86 -- <77>` prints nothing. The lane names `cada856d86` in every
merge-debt figure and records that `bccd715707` is an ancestor of both the
pin and the base.

**Merge debt: none** -- 0 of the 14 upstream commits since `cada856d86`
touch a slice path (`git log --format=%h cada856d86..rocknix/master --
<77> | grep -c .` prints 0, rc 1) and the numstat prints nothing (rc 1); all
14 are `GuiMenu.{cpp,h}` (`git diff --name-only cada856d86 rocknix/master`
prints exactly those two files). The record in `02` § The merge debt is one
line (§ 6), not a table. **Batocera's six commits since the pin's merge
base with `batocera/master`** (`1750dded8c`; `a79c12052` +12 on
`SystemScreenSaver.cpp`, `5f106acce` and `308221458` on
`animations/LaunchAnimation.h`, `52710803c` on
`components/ScraperSearchComponent.cpp`, `7988b09d9` on `CustomFeatures.*`,
`b69fb143c` +10/-1 on `Gamelist.cpp`, none in ROCKNIX's master yet) are
**context only**, named in `02` § The merge debt's one line as *not
ROCKNIX's*, never a debt figure and never fetched (the `batocera` remote's
refs are read as they stand).

**The files, read whole** (lines at the pin by `grep -c ''`, the
inventory's rule; the fork's `--numstat` against the base, which equals the
merge base's and master's for every row; the fork's commits
`bccd715707..PIN` on the file, merges included; `S`/`H` the line of
`es-app/CMakeLists.txt` at the pin that lists it, `--` not listed):

| File | Lines | +/- | Commits | CMake | What it is |
| --- | ---: | ---: | ---: | --- | --- |
| `es-app/CMakeLists.txt` | 363 | 44/0 | 22 | -- | the `ES_HEADERS`/`ES_SOURCES` lists and `add_executable` (`:316`); the fork's 44 lines are its units in those lists (`:34`, `:50-64`, `:98-104`, `:184-197`, `:228-234`); three conditionals only (`if(WIN32)` `:3-29`, `if(MSVC)` `:292-296` and `:299-311`, `if(MSVC)` `:320-329`); no `BATOCERA`/`ROCKNIX` condition, no `add_definitions`, no test target, no credential macro; 319 lines at the base and at `rocknix/master` |
| `AppWindow.h` | 56 | 56/0 | 1 | -- | `AppWindow::gate()` `:24`, `open()` `:30`, `post(W*, task)` `:38-45`, `closing()` `:49-53` (`5443b5301`, #308 F-ES-26); templated so a test needs no SDL (`:18`); callers `FileData.cpp:1283`, `GuiMenu.cpp:9785`/`:9800`/`:9835`, `OfflineScanJob.cpp:104`, `ProxyCards.cpp:213`/`:253`/`:482`/`:507`, `CloudOffer.cpp:81`; `closing()` at `main.cpp:1322` only; **`tests/app-unit/AppWindowTests.cpp` exists at the pin (1 case) and no lane has built it** |
| `CaptureRotation.cpp` / `.h` | 188 / 39 | 188/0, 39/0 | 7 / 5 | S230 / H100 | a game's quarter turns beside its save states (`<first save-state dir>/<stem>.rotation`, `recordPath` `:64-79`); `read()` `:98-131` (`sKnownAt` under `sLock` `:21` by mtime `:103-109`, else `exists(path, false)` `:113` and `readAllText` `:114`, trusted only with `from=checked-launch` `:124`); `fromTable()` `:34-59` (`/usr/config/emulationstation/rotation/<core>.txt`, **cached `exists` `:51` on purpose**, `:23-30`); `recordAfterSession()` `:139-187` from `FileData.cpp:1167` after exit 0: `exists(LAUNCH_LOG, false)` `:146`, the age check `:151-156`, **the whole `/var/log/exec.log` read `:158`** and `retroarch.cfg` `:161-162`, `shouldRecord` `:170-172`, **`Utils::FileSystem::writeAllText` `:175`** (in place), the cache `:179-182`, `DisplayAspect::forgetScreenshots()` `:186`; `forgetAll()` `:133-137` has no caller; the four uncached `exists` of the slice (`:113`, `:146`, `:161`, `:170`) |
| `CaptureRotationText.cpp` / `.h` | 164 / 68 | 164/0, 68/0 | 7 / 7 | S231 / H101 | pure: `OWN_LAUNCH_LINE = "from=checked-launch"` `:14`, `configValue` `:17-45`, `logHasLaunch` `:49`, `shouldRecord` `:54-61`, `turnsFromLog` `:63-85`, `fold` `:87-97`, `turnsFromTable` `:99-119`, `recordText` `:121-125` (`turns=N\nfrom=checked-launch\n`, over three bytes by design, `.h:31-36`), `recordFromOwnLaunch` `:127-150`, `parseRecord` `:152-163`; 8 cases in `CaptureRotationTextTests.cpp` |
| `CheevosIndex.cpp` / `.h` | 30 / 47 | 30/0, 47/0 | 2 / 2 | S191 / H58 | pure: `hasId` `:5-14`, `take` `:16-23`, `lookupDue` `:25-30` (`LookupIntervalSeconds` 86,400, `.h:43`); callers `ThreadedHasher.cpp:325`, `:355`, `:366`; 6 cases |
| `CheevosRetry.cpp` / `.h` | 31 / 47 | 31/0, 47/0 | 2 / 2 | S190 / H57 | pure: `IntervalMs` 10 s, `Attempts` 9, `ScheduledMs` 120 min (`.h:16-18`); `nextDelayMs` `:5-15`, `saveSignIn` `:23-31`; callers `NetworkThread.cpp:125`, `:168`, `.h:69`, `GuiRetroAchievementsSettings.cpp:757-758`; 7 cases |
| `CloudExit.h` | 30 | 30/0 | 2 | H53 | `LockHeld = 75` `:22`, `NoNetwork = 69` `:23`, `NoFolder = 78` `:29` (D-CLOUD-166), `Stopped = 130` `:30`; readers in `ThreadedCloudSync.cpp`, `CloudText.cpp`, `CloudTransferJob.cpp`, `GuiCloudTransfer.cpp`, `GuiMenu.cpp:4306`/`:5306`, `GuiOfflineScan.cpp`, `main.cpp:593`/`:621`/`:664`, `FileData.cpp:1248`; no includer inside the 77 |
| `CloudFolderValidation.cpp` / `.h` | 96 / 33 | 96/0, 33/0 | 2 / 2 | S189 / H56 | pure, fail-closed: `document()` `:27-33` refuses empty, over 65,536 bytes `:29`, a NUL, `schema_version != 1` `:31-32`; `parseResult` `:63-96` binds `run_id`, `config_id`, the contexts `:68-69`, the selected set `:70-72`, every row to the started path `:85`, `seen == expected` `:89`, **`unreadable` never complete `:92-93`**; callers `GuiMenu.cpp:6910-6986`; 4 cases |
| `CloudOffer.cpp` / `.h` | 84 / 33 | 84/0, 33/0 | 5 / 1 | S187 / H54 | the `>>> offer create-saves-folder\|<folder>\|<near>` question: `present()` `:67-82` posts through `AppWindow::post` `:81`; `createSavesFolder()` `:25-65` pushes `GuiLoading<int>` `:34` whose worker runs **`timeout 90 /usr/bin/cloud_setup --seed-folders saves`** `:37` (the slice's one process start) and whose outcome box `:42-45` reads **rc only**; the three-button box `:51-56` (CHANGE FOLDER / CREATE ANYWAY / NOT NOW, back on the last, NOT NOW) and the two-button `:59-64`; 12 `_("` lines, 11 distinct, all with French; callers `GuiCloudTransfer.cpp:341`, `ThreadedCloudSync.cpp:741` |
| `DisplayAspect.cpp` / `.h` | 153 / 42 | 153/0, 42/0 | 8 / 4 | S232 / H102 | `forSystem` `:17-22`, `forGame` `:24-35` (`CaptureRotation::read` `:33`), `sShots` `:57` and `sStems` `:63` under `sShotLock` `:56`; `forgetScreenshots()` `:66-72` (callers `CaptureRotation.cpp:186`, `SystemData.cpp:504`, `ViewController.cpp:1470`); **`buildStems()` `:74-87` walks every non-collection system's `getFilesRecursive(GAME)` `:83`**, built at the first miss `:116-118`; `findGame` `:89-97` re-resolves by `FolderData::FindByPath` `:96` on every look (`:48-52`, no `FileData*` cached, #246's lesson); `forScreenshotPath` `:99-130`; `applyToBoundImages` `:140-152`; callers `GuiImageViewer.cpp:283`/`:679`, `DetailedContainer.cpp:1064`/`:1067`, `GridGameListView.cpp:44`, `ISimpleGameListView.cpp:761`/`:764`, `GuiSaveState.cpp`, `SystemData.cpp`, `ViewController.cpp` |
| `DisplayAspectText.cpp` / `.h` | 76 / 26 | 76/0, 26/0 | 3 / 1 | S233 / H103 | pure: `forSystem` `:8-31` (the 4:3 theme folders `:18-29`), `screenshotContent` `:33-75` (an image extension only `:45-54`, `-cheevo-<id>` `:55-64`, `-YYMMDD-HHMMSS` `:65-74`); 3 cases |
| `FolderMerge.h` | 74 | 74/0 | 1 | -- | pure template: `merge(live, fresh, tree)` `:38-71` (by path `:41-43`, `vanished` for gone or type-changed `:49-55`, new entries moved whole `:62-66`, folders merged recursively `:68-69`); `tree.detach(fresh, f)` `:64` is a tree operation, not a thread; caller `SystemData.cpp:486` with the `Tree` at `:470-484` (`vanished` -> `delete n` `:473`); **`tests/app-unit/FolderMergeTests.cpp` exists (3 cases), never built by a lane** |
| `GameCubeRvzHashRetry.h` | 45 | 45/0 | 1 | -- | pure: `needed()` `:16-44` (only `.rvz` `:19-23`, only an empty or `"0"` id `:27-29`, only a hash that is not 32 hex chars or all zeros `:31-43`); caller `ThreadedHasher.cpp:44`; no case anywhere; #609 OPEN against T20's *"by design"* |
| `JourneyTiers.h` | 159 | 159/0 | 2 | -- | `PATH = /storage/.cache/cloud_sync/journey-tiers` `:24`; `record()` `:38-44`, `parse()` `:51-97` (known only with the header and all three tiers `:63`, `:85-86`), `replaceRecord()` `:105-118` (injected write/remove/exists; `OldRecordStands`), `command()` `:133-154` from fixed literals only (`cloud_content_restore --all` `:142`, `cloud_restore --yes` `:143`, `--saves-only` `:148`, `--selected [--with-media\|--media-only]` `:151-152`, `>>> tier <label>\|<rc>` `:136-139`); writer `GuiMenu.cpp:5053-5075` (`AtomicFile::writeText` `:5066`, uncached `exists` `:5068`); reader `main.cpp:958-975` (uncached `:960`); **`tests/app-unit/JourneyTiersTests.cpp` exists (8 cases), never built by a lane** |
| `NetworkThread.cpp` / `.h` | 274 / 108 | 105/3, 29/1 | 7 / 3 | S179 / H45 | not a thread: a registrar of four `IWatcher` components on es-core's `WatchersManager` thread (1 s tick, `WatchersManager.cpp:170`; every `check()` under `mWatchersLock` `:181-196`); the fork added `sCheevosToken` `:19`, `checkCheevosTokenSoon()` `:21-25` (`ResetComponent`; caller `GuiRetroAchievementsSettings.cpp:806` on the page's save), the schedule reset `:125`, `testAccount(..., &refused)` `:138`, the retry bookkeeping `:159-172` (`CheevosRetry::nextDelayMs` `:168`), `setOnline()` `:178-186`, the link-up branch `:210-260` (`ProxyCards::linkReturned` posted `:237`, `SystemData::startIndexesAtStart(window, true)` posted `:251` under `Settings::CheevosCheckIndexesAtStart()` `:248`, the re-check `:257`); unchanged: pads battery (15 s, `.h:23`), updates (24 h, `.h:41`; toast `:198` `UPDATE AVAILABLE`), the token write `:262-273` (`SystemConf::set` + `saveSystemConf()` `:268-269` on the interface thread); **five `postToUiThread` (`:206`, `:237`, `:251`, `:257`, `:266`), none through `AppWindow`**; `new NetworkThread` at `main.cpp:898`, never deleted; `WatchersManager::stop()` at `main.cpp:1330` joins after `AppWindow::closing()` `:1322`; `<SDL.h>` direct, curl through `RetroAchievements.h`; no case |
| `OfflineAchievementsText.cpp` / `.h` | 283 / 161 | 283/0, 161/0 | 5 / 5 | S194 / H61 | pure, fail-closed: `jsonInt` `:10-22` (**`(int)v.GetInt64()` `:18`**), `readAchievements` `:41-63`, `requestUrl` `:83`, `badgeUrl` `:88`, `parsePatch` `:95-114`, `parseAchievementSets` `:116-150` (an empty set is not a cached game `:109`, `:145`), `parseStoreGame` `:152-177` (`unlocked: null` -> `unlockedKnown = false` `:167-168`), `parseUnlocks` `:179-201`, `parseError`/`isNotCached` `:203-216`, `parsePendingIds` `:218-237` (`strtoll` `:231`), `parseOnlineState` `:239-246`, `parseReadyIds` `:248-261`, `parseAccountTotals` `:263-283`; 15 cases; **changed on T20's ES branch (+99/+52)** |
| `RunLock.h` | 74 | 74/0 | 2 | -- | `held(path)` `:29-42` (`flock(LOCK_SH\|LOCK_NB)` `:34`, released at once), `holder(path, program)` `:44-70` (the pid by `pread` `:58`, `strtol` `:63`, `pid <= 1 -> 0` `:64`, **`/proc/<pid>/cmdline` `find(program)` `:66-68`, a substring**); callers `OfflineAchievements.cpp:60`, `:341`, `:344`, `SaveStateBookkeeper.cpp:67`; **`tests/app-unit/RunLockTests.cpp` exists (3 cases), never built by a lane** |
| `TextFit.h` | 40 | 40/0 | 1 | -- | `popCharacter` `:12-20` (a whole UTF-8 character), `fitOneLine` `:30-37` with **`while (text.size() > 4 && measure(text + "...") > width)` `:34`** -- a byte floor; callers `GuiCloudTransfer.cpp:585`, `GuiOfflineScan.cpp:238`, `GuiScraperRun.cpp:185`; **`tests/app-unit/TextFitTests.cpp` exists (3 cases), never built by a lane** |
| `WifiText.cpp` / `.h` | 265 / 164 | 265/0, 164/0 | 9 / 10 | S192 / H59 | pure: `parseSavedLine` `:11-31`, `savedField` `:34-42`, `parseSavedDetailsLine` `:44-55`, `profilesForSsid` `:58-65`, `preferredProfile` `:67-81`, `parseSaved` `:83-93`, `parseCurrent` `:95-104`, `pickerRows` `:106-193` (the connected row first `:175-180`; its profile by the three-step rule `:151-171`: named-and-up, else the one up, else the namesake with none up; two up and none named -> no guess, `.h:137-146`), `parseJoin` `:195-200`, `joinFailure` `:203-206`, `parseForget` `:208-220`, `pressAction` `:222-231`, `manualAction` `:233-243`, `joinName` `:248-251`, `joinedNotice` `:262-265`; `JoinAnswer` `.h:145-149` cannot read as a bool; 19 cases; **changed on T21's ES branch (+11/+13, `00669ccd9`, #1194)** |
| `Win32ApiSystem.cpp` (`.h` upstream, 70) | 1,269 | 3/3 | 2 | S287 | `#if WIN32` `:1` to `#endif` `:1267`: the Windows `ApiSystem` subclass, listed unconditionally (`:287`, `# batocera`) and empty on every image; the fork's three lines `:316`, `:341`, `:368` wrap `LOG(...) << command` in `Utils::String::maskSecrets` (`80f52e500`, #177); `CHEEVOS_DEV_LOGIN` named at `:98`; 31 cached `exists`, `writeAllText` `:979`, `executeScript` `:314`/`:340`/`:1264`, 3 `HttpReq` lines, all dead here; D-WORKFLOW-209: *recorded, not dead on Windows* (T21 `05:473`) |
| the game list and its metadata: `Gamelist.cpp` / `.h`, `MetaData.cpp` / `.h`, `Genres.cpp` / `.h`, `PlatformId.cpp` / `.h`, `LangParser.cpp` / `.h`, `FileTag.cpp` / `.h` | 848 / 31, 604 / 201, 372 / 69, 301 / 196, 242 / 27, 46 / 20 | 0/0 | 0 | S174 / H40, S171 / H37, S175 / H41, S172 / H38, S199 / H66, S168 / H35 | `Gamelist.cpp`: `loadGamelistFile` `:112-117` (gated on `isRegularFile(xmlpath)`, the cached family), `addFileDataNode` `:255`, `saveToXml` `:288-318` (**remove `:307` then `save_file` `:308`**: no file between), `saveToGamelistRecovery` `:320-336` (after every game, `FileData.cpp:1208`; the hasher `ThreadedHasher.cpp:245`; the scraper `ThreadedScraper.cpp:284`; `GuiMetaDataEd.cpp:497`; `HttpApi.cpp:205`/`:260`; `CollectionSystemManager.cpp:697`; `FileData.cpp:2139`/`:2162`/`:2184`), `updateGamelist` `:374-481` (**cached `exists(xmlReadPath)` `:413`**, the existing file parsed `:416`, then **in-place `doc.save_file(xmlWritePath)` `:474`** when `numUpdated > 0` `:466`, `clearTemporaryGamelistRecovery` `:477`; callers `SystemData.cpp:1570`, `HttpServerThread.cpp:688`), `packGamelist` `:518-630` and `cleanupGamelist` `:631-848` (copy aside `:619-620`, `:838-839`, then `save_file` `:622`, `:841`; cached `exists` on media `:601`, `:705`, `:732-748`); 15 `exists` lines, 4 `save_file`, 3 `gamelist.xml` log lines (`:475`, `:623`, `:842`). `MetaData.cpp`: the decl table `:28-100` (45 `_("` lines), `loadFromXML` `:151-223` (cached `exists` `:223` under `PreloadMedias`), `migrate` `:270`, `appendToXML` `:280`, `set` `:357`, `get` `:407`, `exists(key)` `:435`, `getInt` `:451` (`atoi`), `getFloat` `:456`, `importScrappedMetadata` `:469-507`; `CheevosId` `MD_INT` default `""` `:96`. `Genres.cpp`: `init` `:19-39` from `:/genres.xml`; `genreExists` `:185`, `getGenreFiltersNames` `:234`, `genreStringFromIds` `:257`, `fromGenreName` `:293`, `convertGenreToGenreIds` `:323`. `PlatformId.cpp`: the table `:11-212`, `getPlatformId` `:215-224` (lowercases `:220`), `getPlatformName` `:227`, `ArcadeSystems` `:237`. `LangParser.cpp`: `extractLang` `:33` with the token tables `:37-65` (**`:65` `{ { "in", "ìndia" }, "in", "in" }`, a non-ASCII token in a string literal**), `parse` `:144`, `getFlag` `:203`. `FileTag.cpp`: **`:6-11` wrap six of the nine names in `_()` (FINISHED, SLOW, NOT WORKING, BUGGY, LIKED, DISLIKED); `IN PROGRESS`, `DROPPED`, `ON HOLD` at `:16-18` are not wrapped and have no `msgid` in the French catalog at the pin**; `getDisplayIcons` `:30` |
| the collections and filters: `CollectionSystemManager.cpp` / `.h`, `FileFilterIndex.cpp` / `.h`, `FileSorts.cpp` / `.h`, `CustomFeatures.cpp` / `.h`, `LibretroRatio.cpp` / `.h` | 1,631 / 149, 1,412 / 197, 226 / 87, 537 / 157, 53 / 22 | 0/0 | 0 | S178 / H44, S176 / H42, S169 / H36, S207 / H75, S286 / H162 | `CollectionSystemManager.cpp`: `getSystemDecls` `:34` (`recent` sorts `LASTPLAYED_ASCENDING` `:40`), the six `systemBy*Sort` `:172-294`, `saveCustomCollection` `:333-357` (**`std::ofstream` `:345`, in place**, one path per line `:354`), `updateCollectionSystem` `:472-530` (after every game, `FileData.cpp:1207`; removes through the view `:495-498`), **`:540` `.at()` on a set value** (T2 FD-15, #771 OPEN), `trimCollectionCount` `:548-561`, `getValidNewCollectionName` `:598`, `toggleGameInCollection` `:671`, `displayNotificationMessage` `:762`, `populateCustomCollection` `:1103-1117` (**`rootFolder->clear()` `:1117`**), `getCollectionsFromConfigFolder` `:1434`, `themeFolderExists` `:1492`, the paths `:1508-1532`, **`reloadCollection` `:1558-1600` (`populateCustomCollection` `:1576` then `ViewController::get()->reloadGameListView(bundle)` `:1589`**; callers `GuiGamelistOptions.cpp:425`, `ISimpleGameListView.cpp:462`, `GuiCollectionSystemsOptions.cpp:443`/`:490`/`:501`), `deleteCustomCollection` `:1605-1629`; 10 cached `exists`, 21 `_("` lines. `FileFilterIndex.cpp`: `getIndexableKey` `:247` (**`RATINGS_FILTER` `:322-341`: `rating <= 0` -> UNKNOWN `:333`, clamped at 1 `:336-337`, `(int)Math::round(rating * 5)` `:339` + `" STARS"` `:340`, so `"0.05"` reads `0 STARS`; `YEAR_FILTER` `:364-369`: `:367` keeps the first four characters only when `key[0]` is `'1'` or `'2'`, so `"3000"` and `"999"` read `""`**; `PLAYED_FILTER` `:362`), `setTextFilter` `:551`, `jw_distance` `:557`, `CollectionFilter::load` `:1142-1152` (cached `exists` `:1144`), `save()` `:1237-1315` (**in-place `save_file(mPath)` `:1313`** on `<collections>/<name>.xcc`); 3 `exists`, 21 `_("`. `FileSorts.cpp`: `getSortType` `:32`, the 28-row table `:43-71`, `compareName` `:75`, `stripLeadingArticle` `:93` (`_("A,AN,THE")` `:83`); `FileSorts.h:22-23` `RELEASEDATE_ASCENDING = 10`, `RELEASEDATE_DESCENDING = 11` (T32's 3.32 reads them). `CustomFeatures.cpp`: `parseFeatures` `:23`, `loadEsFeaturesFile` `:155-183` (cached `exists` `:164`, `:167`), `loadCustomFeatures` `:406`, `hasFeature` `:529`; the `save_file` at `:151` sits inside `/* ... */` `:148-152`, dead text. `LibretroRatio.cpp`: `getRatio()` `:51` over `:12-43`; included by `GuiMenu.cpp:60` in angle brackets |
| the surfaces outside the lanes: `SystemScreenSaver.cpp` / `.h`, `SystemRandomPlaylist.cpp` / `.h`, `ContentInstaller.cpp` / `.h`, `ThreadedBluetooth.cpp` / `.h`, `ZaparooSupport.cpp` / `.h`, `KeyboardMapping.cpp` / `.h`, `components/ScraperSearchComponent.cpp` / `.h`, `animations/LaunchAnimation.h`, `animations/MoveCameraAnimation.h` | 1,125 / 134, 109 / 38, 277 / 65, 123 / 47, 64 / 21, 817 / 80, 755 / 112, 67, 28 | 0/0 | 0 | S177 / H43, S198 / H65, S180 / H46, S183 / H49, S285 / H161, S200 / H67, S210 / H78, H157, H158 | `SystemScreenSaver.cpp`: the state machine (`update` `:484-523`, `getNextUpdateTimeout` `:74-94`, 100 ms polls `:31-32`), `startScreenSaver` `:97`, **`pickRandomGameMedia` `:154` retried ten times over a cached `exists` `:156-161`**, `:164` the same cached read, `:350` `getFilesRecursive(GAME, true)` at first start on the interface thread, `pickRandomCustomImage` `:436`, `launchGame()` `:536` (**`:546` calls `FileData::launchGame` past `ViewController::launch`'s checks**, T2's brief `:293-294`), `postToUiThread` `:1022` from the video component's end callback, `VideoVlcComponent` `:996-1000`; 35 `Settings::` reads, 10 cached `exists`. `SystemRandomPlaylist.cpp`: `getNextItem()` `:24`, cached `exists` `:87`, `:97`, `:104`. `ContentInstaller.cpp`: the third-tier card `:60`, **`new std::thread` `:61`**, `threadUpdate` `:106-249` under `static std::mutex mLock` `:11`, **`delete this` `:247` on its own thread**, `mInstance = nullptr` `:248`, `~ContentInstaller` `:64-70` nulls `mHandle` without join or delete and closes the card from the worker `:68`; 12 toasts from the worker (`:140-237`), six of them `_("AN ERROR OCCURRED") + ": " + updateStatus.first` (`:144`, `:163`, `:182`, `:201`, `:218`, `:236`); the downloads are `ApiSystem::installBatocera{Theme,Bezel,StorePackage}` (`:132`, `:170`, `:206`); 13 `_("`. `ThreadedBluetooth.cpp`: the same shape twice (`new std::thread` `:19`/`:76`, **`delete this` `:46`/`:110`**, the card closed in the destructor `:24-25`/`:81-82`, `mHandle` never joined), `formatDisk` exit 69 -> `A REBOOT IS REQUIRED` `:107-108`; 7 `_("`, 2 `GuiMsgBox`. `ZaparooSupport.cpp`: `checkZaparooEnabledAsync` `:20-28` (**`std::thread(...)` `:22`, `.detach()` `:27`**, from `main.cpp:839`), `isZaparooEnabled` `:30-50` (**`mZaparooLock` `:13` held across `HttpReq ... wait()` with `connectTimeout` only `:37-39`, the slice's one bound line `:38`**), `writeZaparooCard` `:52-63` (**no bound `:58-62`**); callers `GuiGameOptions.cpp:59`, `:281`. `KeyboardMapping.cpp`: `checkTriggerExists` `:178`, `checkTargetExists` `:190`, `KeyMappingFile::load` `:217-232` (cached `exists` `:222`, `readAllText` `:225`, `doc.Parse` `:228`; **a trigger `checkTriggerExists` refuses is silently not inserted `:265`, `:271`**; a target of type `key` likewise `:282`, `:288`), `save` `:328-431` (**`writeAllText` in place `:426`, `:429`**), `fromP2k` `:432-437`; backs T31's `GuiKeyMappingEditor` and `GuiKeyboardtopads` (the tab-strip pages of #63). `components/ScraperSearchComponent.cpp`: `ScraperAsyncRequestsBuilder` `:197-258` (**`new std::thread` `:206`, joined only in `update()` `:230-234`, `mFinished` a plain `bool` `:256` written `:220` on the worker and read `:225` on the interface thread, no destructor**; dropped at `:358-361` and `:96-100`), **`:645-658` the second search run synchronously on the interface thread (`:652`, `:658`)**; 19 `_("`, 3 `GuiMsgBox`, 1 `GuiTextEditPopupKeyboard`, 1 `GuiTextEditPopup`. The two animations: `LaunchAnimation.h` `:67` lines, `MoveCameraAnimation.h` 28 (batocera's `5f106acce`/`308221458` touch the first, context only) |
| the unbuilt and the residue: `ScraperCmdLine.cpp` / `.h`; `EmulationStation.h`; `EmulationStation.h.in`, `EmulationStation.rc`, `EmulationStation.aps`, `es_icon.ico`; `Win32ApiSystem.h` | 290 / 7; 31; 27, 39, binary, binary; 70 | 0/0 | 0 | --; H32; --, S294 (`if(MSVC)`), --, --; H163 | `ScraperCmdLine.cpp`: `run_scraper_cmdline()` `:27`, `std::cin` `:50-215`, `handle_interrupt_signal` `:16-24` (`sleep(50); exit(1)`), `downloadImage` `:268`, the TODO `:287` (the slice's one); **`git grep -n ScraperCmdLine PIN` prints one line, `es-app/src/ScraperCmdLine.cpp:1:#include "ScraperCmdLine.h"`**, and `:4 #include "platform.h"` names a header the tree does not hold: dead, uncompiled, uncompilable. `EmulationStation.h`: `PROGRAM_VERSION_MAJOR` and `SCREENSCRAPER_SOFTNAME` with a `#elif ROCKNIX` branch the `.h.in` template lacks, so the `WIN32` `configure_file` would overwrite it (`es-app/CMakeLists.txt:23-27`); a trap for the reader, not an image concern. The `.rc` (`VS_VERSION_INFO`, `IDI_ES_LOGO ICON "es_icon.ico"`), the `.aps` (last upstream commit `90bd22df14` 2015-03-05; a `C:\EmulationStation\es-a` path at offset 69) and the `.ico` (header `00 00 01 00 05 00`, five images): read by nothing on an image |

**The 72 fork commits on the 77** (`git log --format=%h bccd715707..PIN --
<77> | grep -c .` = 72; `--no-merges` = 68; the four merges `da702d8b6`,
`370ebe416` (*Merge remote-tracking branch 'rocknix/master'*), `137309b7d`,
`6c7a36d04`), from `76f502979` *Cloud Saves: run syncs in the background
with a native progress card* to `5a86caea9` *ThreadedHasher: retry failed
GameCube RVZ hashes without an id*; the first commit of each fork-added
unit: `aacde6e20` `CloudExit.h`, `1b3d94d0d` `CloudOffer`, `d9d6083de`
`CheevosRetry`, `c13119bfb` `OfflineAchievementsText`, `f80083a19`
`CheevosIndex`, `6915d80f7` `WifiText`, `3b7265f33` `DisplayAspect{,Text}`,
`12de21757` `CaptureRotation{,Text}`, `8fb12b185` `JourneyTiers.h`,
`9b7b1d3a2` `FolderMerge.h`, `7b7f2f9ee` `RunLock.h`, `53a444e91`
`TextFit.h`, `5443b5301` `AppWindow.h`, `1272b3405`
`CloudFolderValidation`, `5a86caea9` `GameCubeRvzHashRetry.h`; 21 of the 68
touched `es-app/CMakeLists.txt`, one per unit that added a file. The lane's
`02` § Coverage quotes the 72 subjects from its own `git log`, never from
here.

**What the digests checked and found sound, so the lane confirms rather
than hunts:** no `system(`, `popen(`, `runSystemCommand(` or `getShOutput`
in any of the 77 (the one process start is `CloudOffer.cpp:37`'s
`executeScriptLegacy`, bounded by `timeout 90`; `Win32ApiSystem`'s
`executeScript` lines `:314`, `:340`, `:1264`, `.h:55-56` are dead); no
`std::thread` in any fork-own file (the five constructions are upstream's:
`ContentInstaller.cpp:61`, `ThreadedBluetooth.cpp:19`, `:76`,
`ZaparooSupport.cpp:22`, `components/ScraperSearchComponent.cpp:206`); the
two `.detach(` lines are `FolderMerge.h:64` (a tree operation) and
`ZaparooSupport.cpp:27` (the one detached thread); **0 non-ASCII `//`
comments across the 75 text files** (the drafter's grep); 0 `TODO`/`FIXME`
in fork-own files (the slice's one is `ScraperCmdLine.cpp:287`); no
`HttpReq` in fork-own code (`OfflineAchievementsText.h:99` is a comment;
the live constructions are `ZaparooSupport.cpp:37-39` and `:58-62`);
`CloudFolderValidation` and `OfflineAchievementsText` fail closed
throughout (every parser carries an `ok` apart from emptiness, PL-26 and
PL-057); `CheevosRetry`'s window (9 x 10 s inside the 1 s tick) is
honoured; `AppWindow::post`'s two nested locks (the gate, then
`Window::mNotificationMessagesLock` at `Window.cpp:1278`) are taken in one
order everywhere; `JourneyTiers::command()` is built from fixed literals
(no player text reaches the shell) and its reader at `main.cpp:960` and
writer at `GuiMenu.cpp:5068` read uncached (T26 `02:568-569`, a positive);
`CustomFeatures.cpp:151`'s `save_file` is dead text; the `69` shared by
`CloudExit::NoNetwork` and `ThreadedBluetooth.cpp:107`'s *reboot required*
is two scripts' contracts with no shared reader; the **196 distinct msgids
across the 77's 176 `_("` lines every one have a `msgid` line in
`locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the pin with a
non-empty `msgstr`** (the fork-changes digest's lookup; positives `NOT NOW`
-> po 4313 `PAS MAINTENANT`, `CREATE ANYWAY` -> 4641, `SETTING UP YOUR
CLOUD FOLDERS` -> 4626, the two-line `YOUR CLOUD HAS NO SAVES FOLDER YET.`
-> 4644; the catalog holds 2,207 msgids and 42 empty `msgstr` lines
overall, none of them this slice's) -- **and the three `FileTag` names
that are not msgids are the exception that check cannot see** (L-25).

**What they found instead -- the leads, one line each.** § 4 carries each
at its lines with what proves it and its disposition, and tables the
floor's pure leads beside them; the lines here are the pin's, nine of them
read again by the drafter today (`FileTag.cpp:6-18`, `LangParser.cpp:65`,
`TextFit.h:34`, `KeyboardMapping.cpp:265`/`:271`,
`SystemScreenSaver.cpp:156-164`, `Gamelist.cpp:307-308`/`:413`/`:474`,
`CollectionSystemManager.cpp:1117`/`:1589`, `FileFilterIndex.cpp:333-340`/`:367`,
the ten write sites).

| Lead | Lines at the pin | Shape | Q |
| --- | --- | --- | --- |
| L-01 | `es-core/src/watchers/WatchersManager.cpp:181-196` (every `check()` under `mWatchersLock`), `:92-100` (`ResetComponent` takes the same lock); the interface-thread callers `NetworkThread.cpp:21-25` <- `GuiRetroAchievementsSettings.cpp:806`, `:257`, `:191` | a page close that asks for the token check blocks the interface thread until the check in flight ends: `testAccount`'s HTTPS login (`RetroAchievements.cpp:1035-1038`, bounded by `getHttpOptions()`), `canUpdate`'s or `getPadsInfo`'s script; #308 F-RA-19 moved the sign-in off the thread and left this path back onto it | Q2, Q1 |
| L-02 | `CaptureRotation.cpp:146-163` <- `FileData.cpp:1166-1167` | after every RetroArch exit, on the interface thread, the whole `/var/log/exec.log` (`:158`) and `retroarch.cfg` (`:162`) read and scanned; the only size bound is the launcher's truncation (#280) | Q6, Q2 |
| L-03 | `CaptureRotation.cpp:175` against `GuiMenu.cpp:5066` | the rotation record, a saves-tier file the cloud syncs, written in place by `writeAllText` where the journey record beside it is atomic; a truncated record reads as untrusted (benign), D-CLOUD-078 asks for temp-and-rename anyway; Backlog #1186's site | Q4 |
| L-04 | `DisplayAspect.cpp:74-87`, `:116-118`, `:96` + `FileData.cpp:1914-1926`; rebuilt after `SystemData.cpp:503-504` and `ViewController.cpp:1470` | the first screenshot look after each library change walks the whole library under `sShotLock` on the interface thread, and every hit walks the tree for the game (T31 PL-26, T32 L-14) | Q6 |
| L-05 | `Gamelist.cpp:413` (cached `exists`), `:466-477` (in-place `save_file` `:474`), `:112-117` (the `isRegularFile` gate); writers `SystemData.cpp:1570`, `HttpServerThread.cpp:688`; the cache's only reset `FileSystemUtil.cpp:345` | a `gamelist.xml` that arrives after startup (the cloud's game-content restore, D-CLOUD-049) reads as absent through the session cache: the restore's reload may not parse it, and the exit's `updateGamelist` writes the in-memory nodes alone over it; `saveToXml`'s remove-then-save `:307-308` is the same writer's no-last-good shape for the recovery files (D-CLOUD-078) | Q4 |
| L-06 | `CollectionSystemManager.cpp:1117` (`rootFolder->clear()` via `:1576`) then `:1589` (`reloadGameListView(bundle)`); callers `GuiGamelistOptions.cpp:425`, `ISimpleGameListView.cpp:462` | the #246 shape (`es-code-traps.md:191`): the custom collection's entries deleted, then the bundle view's cursor read; the fork's `dropGameListView`/`remakeGameListView` pair (`SystemData.cpp:508`) is the contained fix (T32 L-16, handed here) | Q1 |
| L-07 | `components/ScraperSearchComponent.cpp:197-258` (`:206`, `:230-234`, `:256`, no destructor); dropped at `:358-361` and `:96-100` | a builder destroyed mid-search leaks its running thread, which then writes `:213`, `:217`, `:220` into freed memory; `mFinished` read unsynchronised | Q1 |
| L-08 | `components/ScraperSearchComponent.cpp:645-658` (`:652`, `:658`) | on `ASYNC_DONE` with no results the second search runs synchronously on the interface thread, the call the builder exists to take off it (`:196`) | Q2, Q6 |
| L-09 | `ZaparooSupport.cpp:32-39`, `:58-63`; `GuiGameOptions.cpp:59`, `:281`; `main.cpp:839` | a service on `127.0.0.1:7497` that accepts and never answers holds the detached probe forever and, through `mZaparooLock`, the game-options page; `writeZaparooCard` unbounded; outside the lanes, recorded | Q2 |
| L-10 | `ContentInstaller.cpp:61`, `:64-70`, `:247-248`; `ThreadedBluetooth.cpp:19`, `:22-26`, `:46`, `:76`, `:110`; the `AN ERROR OCCURRED: <status>` toasts `:144`, `:163`, `:182`, `:201`, `:218`, `:236` | `delete this` on the worker, the thread never joined or deleted, the card closed from the worker; a tool's status text on the screen; outside the lanes (D-UI-079), recorded | Q1, Q5 |
| L-11 | `SystemScreenSaver.cpp:156-164`, `:350`, `:1022` | ten retries over a cached miss never see a file appear; a media file deleted since the cache remembered it is handed to the player; the first start walks the library on the interface thread; a post outside `AppWindow` (its target is process-lifetime); outside the lanes, recorded | Q4, Q6 |
| L-12 | `NetworkThread.cpp:206`, `:237`, `:251`, `:257`, `:266` vs `AppWindow.h:38-45`; `main.cpp:1322`, `:1330` | five posts straight to `Window::postToUiThread`, not through the gate the fork wrote for exactly this (F-ES-26); sound by order, but a post between `:1322` and `:1330` lands in `mFunctions` and never runs; `:237`, `:251`, `:257` are the fork's | Q1 |
| L-13 | `NetworkThread.cpp:266-270` | the token written with `SystemConf::set` + `saveSystemConf()` on the interface thread, a `system.cfg` rewrite covered by `es-conf-tests` (D-CLOUD-078's writer is es-core's); nothing new to prove | Q4 |
| L-14 | `RunLock.h:44-70` (`:58`, `:66-68`) | `holder()` names a pid whose `/proc/<pid>/cmdline` merely contains `program`; the window is a pid reused between a holder's death and the file's next writer; `OfflineAchievements::stopRun` signals what it returns | Q3, Q7 |
| L-15 | `FolderMerge.h:38-71` <- `SystemData.cpp:486` (`vanished` -> `delete n` `:473`) | every holder of a vanished node (the collections' entries, a group folder, a hasher's queue, the header's own list `:9-13`) must be dropped at the `Tree` `:470-484`; the template's case file exists and has never been built (`tests/app-unit/FolderMergeTests.cpp`) | Q1 |
| L-16 | `JourneyTiers.h:133-154`; `main.cpp:958-975` | the continuation from fixed literals (sound); a marker with no record runs everything (`--all` + `--yes`, `:142-143`) by design (D-WORKFLOW-050); recorded, not a defect; the case file exists, never built | Q7 |
| L-17 | `OfflineAchievementsText.cpp:18`, `:231` | a 64-bit id or epoch truncated to `int`; harmless today | Q3 |
| L-18 | `CloudOffer.cpp:37`, `:42-45` | bounded at 90 s on `GuiLoading`'s worker; a `timeout` kill (124) reads COULDN'T CREATE IT; a script exiting 0 having created nothing reads DONE (the no-op-success shape; the script's half is the rclone slice's) | Q3, Q5 |
| L-19 | `WifiText.cpp:151-173`, `:67-81`, `:248-252`; `.h:137-146` | with two profiles up on one SSID and neither named, the connected row joins by its name, which `wifictl join` reads as a profile name: a renamed profile fails with `MayBeKey` and the player is asked for a key they have; documented as deliberate | Q5 |
| L-20 | `TextFit.h:34` | the floor is 4 bytes, not 4 characters: a 4-byte name wider than the box never gets its ellipsis; a two-character CJK name stops at one character | Q5 |
| L-21 | `Win32ApiSystem.cpp:1`, `:1267`, `:316`, `:341`, `:368`; `es-app/CMakeLists.txt:287` | listed unconditionally, guarded in the file: the fork-own tier is provenance | Q7 |
| L-22 | `ScraperCmdLine.cpp:27`, `:24`, `:287`; `es-app/CMakeLists.txt` (absent) | 290 lines of console code in no list; Backlog #1235's shape | Q7 |
| L-23 | `FileFilterIndex.cpp:1313`; `CollectionSystemManager.cpp:345-357` | settings-tier files (`.xcc`, `custom-<name>.cfg`, which backuptool's archive carries) written in place; the atomic writer exists (`AtomicFileUtil`) | Q4 |
| L-24 | `NetworkThread.cpp:19-25`, `main.cpp:898` | `sCheevosToken` points into a `NetworkThread` newed once and never deleted: sound for the process's life, recorded so nobody "fixes" the leak and dangles the static | Q1 |
| L-25 | `FileTag.cpp:6-11` against `:16-18`; the catalog | six of nine tag names reach xgettext through `fake_gettext_*`; `IN PROGRESS`, `DROPPED`, `ON HOLD` do not and have no `msgid` at the pin (the drafter's grep: six `msgid` lines at po 717, 3576-3588, none for the three) | Q5 |
| L-26 | `LangParser.cpp:65` | `{ { "in", "ìndia" }, "in", "in" }`: a non-ASCII token matched lowercase against ASCII ROM names, unreachable; a string literal, so xgettext is unaffected | Q5 |
| L-27 | `FileFilterIndex.cpp:333-340`, `:367` | `"0.05"` rounds to `0 STARS` where `"0"` and `""` read UNKNOWN; a year starting `3`, or three digits, reads `""` | Q3 |
| L-28 | `KeyboardMapping.cpp:265`, `:271`, `:282`, `:288` | a trigger or key target `checkTriggerExists`/`checkTargetExists` refuses is dropped silently: a mapping loads as an action with no trigger | Q3 |
| L-29 | § 5's two delta commands | merge debt none | Q7 |

**The harness that exists.** At the pin, `es-app/tests/unit/CMakeLists.txt`
(159 lines) defines four targets: **`es-unit-tests`** (`:36-65`; 16 test
files linking 9 es-app sources and 3 es-core; fails configure without
rapidjson `:72-75`), **`es-file-tests`** (`:96-112`, `AtomicFileUtil`),
**`es-conf-tests`** (`:120-135`, `SystemConf.cpp` + `AtomicFileUtil.cpp`
with `fakes/SDL_timer.h`), **`es-file-tests-win32`** (`:142-158`). Of this
slice's 31 `.cpp`, **seven are linked by `es-unit-tests`** --
`CloudFolderValidation.cpp` (4 cases), `CheevosRetry.cpp` (7),
`OfflineAchievementsText.cpp` (15), `CheevosIndex.cpp` (6), `WifiText.cpp`
(19), `CaptureRotationText.cpp` (8), `DisplayAspectText.cpp` (3) -- the
one floored family; the model is `CloudTextTests.cpp` (70 cases, every one
of `CloudText.h`'s 45 functions named). 19 `*Tests.cpp` under
`es-app/tests/unit/`, 15 `.py` under `tests/`. **And a second tree the
earlier digests under-read: `tests/app-unit/CMakeLists.txt` at the pin
defines `app-unit-tests` (`:35-41`) from `main.cpp`, `JourneyTiersTests.cpp`
(8 cases), `FolderMergeTests.cpp` (3), `RunLockTests.cpp` (3),
`TextFitTests.cpp` (3) and `AppWindowTests.cpp` (1) -- five of the fork's
header-only units have a case file that no lane has ever built** (T18
`02:50-58` ran only `jobs-tests`, on the coordinator's yes; T31's build
script parses `es-app/tests/unit/CMakeLists.txt` alone, its `:23`), beside
`proxycards-tests` (`:51`), `jobs-tests` (`:71`) and `bookkeeper-tests`
(`:92`) and nine doubles under `fakes/` (`ApiSystem.h`, `FileData.h`,
`LocaleES.h`, `Log.h`, `SystemConf.h`, `ThreadedCloudSync.h`, `Window.h`,
`components/AsyncNotificationComponent.h`, `utils/FileSystemUtil.h`). So
the digests' *"eight fork-own units have no case"* is three:
`GameCubeRvzHashRetry.h`, `CloudExit.h` and `NetworkThread.*` have none
anywhere; `AppWindow.h`, `FolderMerge.h`, `JourneyTiers.h`, `RunLock.h`
and `TextFit.h` have cases nobody has run, which § 5 makes the lane's
first build. In the coordinator worktree nothing exercises the slice:
`tools/vm-qa:63`'s suites name no collection, UPDATE GAMELISTS, screensaver
or content installer; the 18 `tools/vm-walks/*.steps` enter none of them
(`wake.steps` *avoids* the screensaver: one `shift` to spend the eaten
press, `generic-x64-vm-testing.md:365`); `docs/es-menu-map.md` declares
SCREENSAVER SETTINGS (`:699`), ADD TO CUSTOM COLLECTION... (`:704`),
GLOBAL HOTKEYS (`:705`), KEYBOARDTOPADS (`:707`) and PAIR A BLUETOOTH
DEVICE (`:709`) upstream-unchanged under `## Not mapped` (`:677`), maps
GAME COLLECTION SETTINGS (`:109`, `:136`), the SELECT row (`:90`),
GAMELIST OPTIONS (`:135`) and `cheevosHash` in `gamelist.xml` (`:625`),
and names **neither FILTER GAMELIST BY nor EDIT DYNAMIC COLLECTION
FILTERS** (0 grep hits; T31 PL-17's twelve undescribed titles). **Compiled
syntax-only on the host before: 0 of 31** (the three lanes' `stage-e`
records name `ApiSystem.cpp`, `GuiSettings.cpp`, `GuiWifi.cpp`,
`HttpReq.cpp`, `Settings.cpp`, `ViewController.cpp`, `GuiBios.cpp`,
`main.cpp`, `ScreenScraper.cpp`, `Scraper.cpp`, `GuiMenu.cpp` and T31's
twelve pages, none of the 77). The prior guest evidence that touches the
slice is nine `docs/vm-qa-log.md` rows (`:41`, `:61` -- #145's empty-cloud
offer, **the one slice function with a frame on record**, `:86`, `:87`,
`:111`, `:145`, `:151-155`, `:265`): the index and its triggers, never a
custom collection, a `gamelist.xml` read back, the screensaver, the
installer or the key-to-pad editor.

**The neighbours, and whose they are:** `ApiSystem.*`, `HttpReq`,
`FileSystemUtil.cpp`'s cache (its only reset at `:345`), `AtomicFileUtil`,
`Settings`/`SystemConf`, `WatchersManager` and `Scripting.cpp` are
**T21's and es-core's** (#668; the es-core slice the order names);
`FileData`, `SystemData` (`rescanIfFolderChanged` `:431-486`, the `Tree`
`:470-484`, `:508`'s drop/remake pair, `:1570`'s `updateGamelist` call),
`main.cpp` and `SaveStateBookkeeper` are **T2's** (#649); the views and
`HttpServerThread.cpp:688` are **T32's** (#679); every page under `guis/`
(`GuiCollectionSystemsOptions`, `GuiGamelistOptions`, `GuiGamelistFilter`,
`GuiMetaDataEd`, `GuiKeyMappingEditor`, `GuiKeyboardtopads`,
`GuiBatoceraStore`, `GuiThemeInstaller`, `GuiGameOptions`,
`GuiImageViewer`, `GuiSaveState`, `GuiWifi`, `GuiRetroAchievementsSettings`)
is **T31's** (#678); `GuiMenu.*` **T26's** (#673); `ThreadedHasher`,
`OfflineAchievements`, `RetroAchievements` and `ProxyCards` **T20's**
(#667); `CloudText`, `ThreadedCloudSync`, `CloudTransferJob` and the cloud
pages **T18's** (#665); the es-core components **T35's** by the earlier
briefs' reading. Twenty of the 77 include T21's `ApiSystem.h` (7 edges),
T2's `FileData.h` (13) or `SystemData.h` (11), or T32's `views/` (6):
one direction of a cycle taken as given, not as a finding. Six of the
fork's header-only units (`CloudExit.h`, `FolderMerge.h`,
`GameCubeRvzHashRetry.h`, `JourneyTiers.h`, `RunLock.h`, `TextFit.h`)
have **no includer inside the 77**: every reader is in T2, T18, T20, T26
or T31, which is the reader's warning that these files are read here out
of context.

**Already found; do not re-find; take up** (each cited at its lines in
`02`, with a disposition; states as the inherit digest read them on
2026-10-27, re-read at stage A): **T2 FD-9/FD-19** (`Scripting.cpp:88-148`,
routed *"T33/T21"* at T2 `05:610`): recorded as inherited and routed to
the es-core slice (§ 1 ruling a). **T2 FD-15 / #771 (OPEN)**:
`CollectionSystemManager.cpp:540`'s `.at()` on a set value, the sibling of
the sort-id off-by-one T2 fixed in `FileData`/`SystemData` (28 sort types,
`FileSorts.cpp:43-71`): *to be confirmed at `setSortId`* -- confirm or
clamp (Q3). **T2 SD-1 / #781 (OPEN)**: the rescan's merge misses
sub-folder changes and lists a multi-disc game's tracks; T2's file, T33's
template (L-15). **T2 PC-1**: detached card workers call their card after
`window.deinit` (`main.cpp:1358`); `AppWindow::post` stops posting once
`main()` lets go but those calls are not posts; a T35/T18 lead on a T33
header, inherited. **T2 `02:84`, `04:190`**: `recordAfterSession`,
`refreshCollectionSystems` and `saveToGamelistRecovery` on exit 0
(`FileData.cpp:1207-1208`) inside T2's measured 1.01 s exit-to-next-frame:
the callees are T33's (L-02; the retro's line). **T2's brief
`:293-294`**: `SystemScreenSaver.cpp:546` calls `FileData::launchGame`
past `ViewController::launch`'s checks, ungraded by T2 -- graded here
(Q6), with D-UI-081's *"screensaver slideshow"* as a rotation surface
(does it draw the turn? unread). **T31 PL-26** (ruled 13:27 UTC on #678,
*recorded as written, for the slices that own `DisplayAspect.cpp`*) and
**T32 L-14**: L-04 (Q6). **T32 L-16** (`:716-724`): L-06 (Q1), the
disposition at T33's pause now that the owner is confirmed. **T21 PL-20 /
Backlog #1186 (OPEN)**: `writeAllText` is `fopen "wb"`, `fwrite`, `fclose`
unchecked (`FileSystemUtil.cpp:1429-1443`); three of the eight sites are
T33's (`CaptureRotation.cpp:175`, `KeyboardMapping.cpp:426`, `:429`); T26
moved its own at `2dd46a3e3` (#1231); the fix shape `Utils::AtomicFile::writeText`
(T18's S2); the kill sweep `kill-writer.py` the proof shape; **the ruling
(this slice's stream or the Backlog) at the pause**. **T31 PL-25 /
Backlog #1235 (OPEN)**: `es-app/CMakeLists.txt:315-316`'s lists decide
reach; `GuiAutoScrape.*` and now `ScraperCmdLine.*` (L-22) are the shape;
the inventory tool's side is the Backlog's. **T32 errata 23**:
`CPPHTTPLIB_OPENSSL_SUPPORT` defined nowhere -- recorded, not re-grepped.
**T20 PL-01 / #1170 (OPEN, fixed on T20's branch in `ThreadedHasher` only,
`698040b5c`) and PL-07 / #301 (OPEN)**: `NetworkThread.cpp:248`, `:251`
start the hasher on the interface thread through `postToUiThread`; the
callers' side is T33's, the hasher's is T20's (Q2). **T20 PL-06 / #1175
(OPEN, resolved `2d8a0a135`)**: the sign-in at the page's close;
`CheevosRetry.*` unchanged, its 7 cases the rule. **T20 PL-04 / #1173
(OPEN, `f85061f14`) and PL-05 / #1174 (OPEN, `274a71add`)**:
`OfflineAchievementsText.{cpp,h}` +99/+52 on T20's branch (`toggleOutcome`
lifted; `unknown` is not zero) -- read at both refs, inherited, no second
fix. **T20 `02:167`**: `GameCubeRvzHashRetry.h:35-48` *by design* against
**#609 (OPEN)** -- the ruling at the pause (§ 1 f). **T20 S9**:
`TextFit::fitOneLine` cuts on characters; a non-UTF-8 name reaches the
page as bytes -- L-20 adds the 4-byte floor. **T21 PL-16 / #1204 and
#1194 (OPEN)**: `WifiText.{cpp,h}` +11/+13 at `00669ccd9` on T21's branch
(CONNECTED only on a current network) -- read at both refs, inherited.
**T21 `02:329`, `04:192`, `05:473`**: `Win32ApiSystem.cpp` *recorded, not
dead on Windows* (D-WORKFLOW-209) -- L-21 restates, with the CMake line.
**T21 PL-15 / #1203**: `LedText.{h,cpp}` added to `es-app/CMakeLists.txt`
on T21's branch (two of its +10 lines; the others `TextRowEdit`,
`ScriptOutput`, `StatusText`, `scrapers/ScraperReplies`) -- the list
collision named in the hand-back. **T18 `02:24-27`, `:30`, `:34`, `:41`,
`:291-306`**: the seven `es-app/tests/unit` files of T33's subjects were
graded only on what a test file owes, *"their subjects belong to other
slices"* (`02:44`) -- the subjects are T33's, audited here. **T18
`02:50-58`**: `app-unit-tests` never built -- § 5's first build. **T18
`02:83-84`**: `CloudOffer::present` after a completed run, a positive;
**#1150**'s linger (resolved `29d500db9` on T18's branch) runs
`CloudOffer::present` over a started game -- the caller's fix is T18's,
cited. **T26 `02:568-569`, `:596`**: `JourneyTiers::PATH` read uncached, a
positive. **T31 `02:643`, retro `:83`**: `GuiKeyMappingEditor` and
`GuiKeyboardtopads` still route left/right to their strips (#63);
`KeyboardMapping.*` backs both -- the pages are T31's, the file's load and
save are Q3's. **T32 3.32**: `FileSorts.h:22-23` is the enum behind
`GameNameFormatter.cpp:84-85`'s missing descending year; the enum is
T33's, the bug T32's. **Backlog #560 (OPEN)**: FAST SHUTDOWN skips
`updateGamelist` under `IgnoreGamelist` (`main.cpp:1322`); a
source-backed matrix of which dirty fields each shutdown path persists is
owed -- `Gamelist.cpp:374-481` is the writer's half (Q4, recorded).
**#69 (OPEN, milestone-less)**: Tools entries lose their icons
(`/usr/config/modules/gamelist.xml`, `ThemeData.cpp`, `SystemData.cpp`)
-- cited, outside the 77. **#585 (OPEN)**: its body and comments name
none of the 77; the lines T33 owes start empty and end with § 5's
candidates. **#1140, #1143, #1144** (T18's Backlogs on `CloudText`):
cited, T18's. **The menu map's three declarations** (`:699`, `:704`,
`:707`): adding a ROCKNIX row to any of those pages means mapping it and
deleting the line (`:683-684`); the two filter rows are Q7's.

## 3. Read first

In this order, each read in this session, and `01-research-notes.md` says
which were read (`working-principles.md` § Pre-flight):

1. **The rules**, each at the section named, with the question it serves;
   the section's own sentence is not repeated here -- open it (the line
   numbers are the coordinator worktree's at `ce8608e38f`, by `grep -n
   '^## '`):

   | Rule | Line | Section | Serves |
   | --- | ---: | --- | --- |
   | `es-code-traps.md` | `:22` | Never rebuild a button bar from inside one of its buttons | Q1 (`CloudOffer`'s boxes, `ScraperSearchComponent`'s) |
   | | `:60` | Comments near a translatable string must be ASCII | Q5, § 9 |
   | | `:104` | Three things a font is not, third bullet: `exists` caches for the session; pass `false` for what changes while ES runs | Q4 (the 83 cached reads) |
   | | `:139` | Pure text has a home, and a test | § 5 (every unit case's shape; the eleven pure units) |
   | | `:164` | The picture beside a game list is the theme's own extra, not md_image | Q6 (`DisplayAspect::applyToBoundImages`) |
   | | `:191` | A rescan that deletes FileData drops the view first | Q1 (L-06, L-15: list who holds a pointer) |
   | | `:212` | A file under three bytes reads as empty | Q4 (`CaptureRotation`'s record, `JourneyTiers`' record) |
   | | `:238` | A pooled connection with the link gone is silent for a quarter of an hour | Q2 (L-01's `testAccount`, L-09) |
   | `es-native-ui.md` | `:32` | The other files that carry the interface law (D-UI-039) | Q7 |
   | | `:81` | Core patterns: the progress card for fast work only (D-UI-078); a file another process writes is read uncached; the gates | Q1, Q4 |
   | | `:144` | The cards at the link's return: saves first, then one batch (D-UI-101/109); the top-up is two things (D-RA-035) | Q1 (`NetworkThread.cpp:237`, `:251`) |
   | | `:175` | Spacing: the four surface tiers; D-UI-079 (the content installer and the Bluetooth scan keep their cards) | Q1, Q5 (L-10) |
   | | `:324` | A layout must not be computed from what it last produced | Q6 |
   | | `:377` | Anti-patterns: two surfaces for one event; a transient-only report | Q5 (the installer's toasts) |
   | | `:405` | Before the pin moves, the compiler has seen the edit (`tools/es-syntax-check`, exit 2 here) | § 5, § 9 |
   | `es-player-text.md` | `:29` | Conventions: the four tiers (`gamelist.xml` is game content, D-CLOUD-049, `:62`); back up / backup; the one-line toast | Q4, Q5 |
   | | `:141` | Every fork string ships in English and French (D-UI-051); script text `:164` | Q5, § 9 |
   | | `:211`, `:236` | Outcome words and the register; the outcome vocabulary (COMPLETED / COULDN'T FINISH / SKIPPED; D-UI-129's fourth SKIPPED) | Q3, Q5 (`CloudOffer`'s outcome box; `CloudExit.h`) |
   | `es-ui-style-guide.md` | `:32` | Keep the flow and its visual evidence together | § 5, § 7 |
   | | `:169` | Confirmations: YES first; back lands on NO or OK, else on the last button | Q5 (`CloudOffer.cpp:51-56`, `:59-64`) |
   | | `:268` | Gating: kid and kiosk behind `isFullUI`; network round-trips behind an action | Q2 (`ZaparooSupport` at page build) |
   | `engineering-practices.md` | `:12` | Change stays inside the fork's lanes (D-UI-079) | every Q |
   | | `:28` | Check upstream early (the 46 are `rocknix/master`'s bytes: the check is of batocera's tree, § 2) | Q7 |
   | | `:83` | Verify design intent (`git log -S` before each FAIL-at-pin lead) | § 4, § 5 |
   | | `:111` | Verify the artifact, not the report | Q3 |
   | | `:194`, `:250` | A name is not a behaviour; **a total is the tool's line, never a sum made in the head** | § 5 (every count; the `TOTAL:` line) |
   | | `:419`, `:464`, `:478`, `:548` | **Guards must fail closed; prove the guard fires and check the stub against the unfixed code first**; `rc=$?` on its own line; the first PASS of anything new is the one to distrust | Q3, § 5 |
   | | `:576` | Before deleting a duplicate, diff its behaviours (blindspot 23) | § 4 (L-22's dead code is not deleted here) |
   | | `:799`, `:829` | Fail gracefully; **the last known good state is a record, kept on purpose (D-CLOUD-078): temp-and-rename `:836`** | Q4 (every writer) |
   | `bugs-are-agent-first.md` | `:41`, `:53`, `:76` | The three classes; The rules; rule 6 | every bug |
   | `issue-tracking.md` | `:129`, `:180` | A criterion is agent-first (D-QA-044); Ticking an acceptance criterion | § 7 |
   | `upgrade-and-install.md` | `:40`, `:58` | Fixing forward is not enough; every fix answers what was already written (D-WORKFLOW-050, the `Already written:` line) | every bug (a `gamelist.xml`, an `.xcc`, a `.rotation` record already on devices) |
   | `rclone-cloud-sync.md` | `:705`, `:711` | The content tier's flags: `MEDIA_DIRS` and `gamelist.xml` excluded from the ROMs-and-BIOS transfer and every count (D-CLOUD-048/049); `--media-only` carries the game list | Q4 (L-05's restore) |
   | `generic-x64-vm-testing.md` | `:100`, `:108`, `:215`, `:224-225` | Headless: `run --headless --daemonize`, `tools/vm-serial`, the pidfile; `--res 640x480` (#1141); cutting the link with `ip link set eth0 down` | § 5 |
   | | `:325` | A launch, a START or a walk waits for the interface to be idle (D-QA-057: `/isIdle` false while the hasher, scraper, **content installer**, updater or a game runs) | § 5 (G-03 waits on the index) |
   | | `:365`, `:382` | After five idle minutes the first key only wakes the screensaver (`wake.steps`); a restarted ES comes back on the last game list, not the carousel | § 5 (G-02, G-06) |
   | | `:486` | `dismiss-dialogs` ends on the carousel where it was | § 5 |
   | | `:1145`, `:1155` | A settings change made from the shell is invisible to the running interface; restart the interface after `set_setting` | § 5 (G-06's `ScreenSaverTime`) |
   | | `:959`, `:1432` | `tools/vm-visual-qa`; the guest is the candidate image, not the read tree -- compare the file before trusting the verdict | § 5 (every frame's side) |
   | `device-builds.md` | § Build credentials | the four macros, by name; their home is the top-level `CMakeLists.txt`, not this slice's (§ 1) | Q7 |
   | `player-language.md`, `least-surprise.md`, `time-to-play.md` | whole | | Q5, Q6, § 6 |

2. **The register.** The rows that name a file or behaviour here (all on
   the coordinator's branch; D-WORKFLOW-188 is the P1 branch's; the line
   is the table's): **D-CLOUD-049** (`:107`: `gamelist.xml` belongs to game
   content; favourites and play counts live in it), D-CLOUD-048 (`:106`),
   **D-CLOUD-074** (`:140`: the sentinels 75 and 69), **D-CLOUD-166**
   (`:574`: `CloudExit::NoFolder`, 78), **D-UI-079** (`:345`: the content
   installer and the Bluetooth scan keep their cards), **D-UI-080**
   (`:346`) and **D-UI-081** (`:348`: the rotation learned from the launch
   log, applied wherever drawn, *"the screensaver slideshow"* among the
   surfaces), D-UI-082 (`:349`: the core's table stands in), **D-UI-094**
   (`:407`) and **D-UI-114** (`:455`: `from=checked-launch`; older lines
   read as no line), D-RA-013 (`:299`), **D-RA-035** (`:423`), D-UI-104
   (`:425`), D-RA-036 (`:428`), **D-UI-113** (`:451`: the rescan merges
   rather than clears; the restore's ticks travel in `journey-tiers`),
   D-UI-061 (`:309`), D-UI-101/109 (`:421`, `:434`), **D-QA-057**
   (`:492`), D-RA-052 (`:752`), D-CLOUD-186 (`:755`), D-UI-128 (`:756`),
   **D-UI-129** (`:757`: a completed run reported as cancelled is a
   defect), **D-WORKFLOW-209** (`:746`: a dead-end table removes nothing),
   D-WORKFLOW-212 (`:753`), D-WORKFLOW-188/189, D-UI-039, D-UI-042/045,
   D-UI-051, D-WORKFLOW-144, D-WORKFLOW-155/156, D-WORKFLOW-164/165,
   D-WORKFLOW-187/195; **D-UI-120** (`:775`) is open (sentence case on the
   fork's pages). The highest decided IDs at this version are § 9's; the
   lane reads the collection, gamelist and screensaver rows by
   `tools/archaeology 'gamelist'`, `'collection'` and `'screensaver'`
   before calling anything pending.
3. **The menu map** (`docs/es-menu-map.md`, 989 lines): `## Two ways in`
   `:83` (the SELECT row `:90`), `## Main menu` `:95` (`:109` GAME
   COLLECTION SETTINGS), `## What lives where` `:126` (`:135` USER
   INTERFACE with GAMELIST OPTIONS; `:136` GAME COLLECTION: COLLECTIONS TO
   DISPLAY, CREATE CUSTOM COLLECTION, OPTIONS), `## RetroAchievements`
   `:578` (`:625` `cheevosHash` in `gamelist.xml` or in `recovery/<system>/`
   until the next clean exit writes it), **D-UI-039 at `:668`**, **`## Not
   mapped` `:677`** (the rule `:683-684`; `:699`, `:704`, `:705`, `:707`,
   `:709`), and the visual-evidence section `:26-82` (the baseline
   `d72084ccad`; the `evidence-index.json` schema). **No section names
   FILTER GAMELIST BY, EDIT DYNAMIC COLLECTION FILTERS or UPDATE GAMELISTS
   as a row** (Q7).
4. **The blindspots** naming this slice's shapes: 4 (`close()` inside a
   page's own handler; #246's cursor is the same shape), 8 (an assertion
   that holds because nothing had happened yet), 13 (assumed done), 22 (a
   probe that cannot report absence), **33** (`:134`: a sentinel exit code
   borrowed from the wrapped tool's space -- `CloudExit.h`'s 69/75/78 and
   `formatDisk`'s 69), **44** (`:445`: proven at a fixture's size), 49
   (`:590`: an edit made blind to the compiler), **62** (`:913`: a fix
   corrected the writer and left what it had written -- `Already written:`
   on every bug), **64** (`:971`: a wait lengthened for an event the code
   had no path to produce: the re-index *"started by the network thread
   when the link came back"* is `NetworkThread.cpp:251`), **75** (`:1206`:
   a corpus read on the wrong tree -- every count at the hash); and the
   register's `:155-162` (the sentinels 75 and 69 in the scripts and in
   `CloudExit.h`: check every reader that names a code when one is added).
5. **The tests at the pin.** § 2's harness paragraph; read whole before a
   case is written: `es-app/tests/unit/README.md` and `CMakeLists.txt`
   (`:36-65`), the seven slice test files (`CloudFolderValidationTests.cpp`
   84 lines, `CheevosRetryTests.cpp` 112, `OfflineAchievementsTextTests.cpp`
   350, `CheevosIndexTests.cpp` 62, `WifiTextTests.cpp` 352,
   `CaptureRotationTextTests.cpp` 164, `DisplayAspectTextTests.cpp` 54),
   `CloudTextTests.cpp` (1,784 lines, the model), `tests/app-unit/CMakeLists.txt`
   whole (its `:1-23` say why `app-unit` is a tree of its own) and the
   five case files it links for T33's units, with `fakes/`; on T21's ES
   branch `3ae9610b0` `es-app/tests/unit/ScraperRepliesTests.cpp` (the
   model for validity beside the value); the ES tree also has a top-level
   `tests/`, so the full path matters.
6. **The walks and the frames.** `tools/vm-walks/README.md:23-32` (the
   step vocabulary), `wake.steps` (one step), `manager.steps` (the one walk
   that enters a game list; its `0-carousel` and `1-list` shots),
   `claims.txt:79` and `:476-492` (the `recent` collection as a backdrop in
   the accepted `tick-game-content` frames, #578), `reset.steps:6-8`' note
   on the GO TO dialog a walk must not be left holding (#85).
7. **The French**: 176 `_("` lines in 11 of the 77 files; 196 distinct
   msgids, every one in the catalog at the pin with French; the three
   `FileTag` names outside `_()` (L-25); `tools/es-untranslated` is the
   count over the whole tree, both lines known from T32's proof at the same
   pin (`706 fork string(s) in the source, 706 with French, 0 without`
   against `bccd715707`, `703 ... 703 with French, 0 without` against
   `cada856d86`, § 5) and silent on an upstream string, which is why L-25
   is a grep of the catalog, not the tool's line.
8. **The audits**: T21's `02-forward-audit.md:393-398` (§ The writers,
   group 2), `:329`, `04:192`, `05:393-410` (PL-20), `:473`,
   `stage-e/syntax-check.sh` and `tools/t21-build-tests.sh` (on
   `origin/feature/m6-es-state-and-bridge-668`); T2's `02:71` (FD-9),
   `:84`, `:92` (FD-15), `:112` (FD-21), `:130` (SD-1), `:178`, `:210-211`
   (PC-1), `04:142`, `:190`, `:670-720`, `05:102-118` (PL-005),
   `:269-287` (PL-015), `:607-618` (on `origin/feature/m6-es-launch-path-649`);
   T18's `02:24-58`, `:83-84`, `:291-306`, `:355-359` (on
   `origin/feature/m6-es-cloud-pages-665`); T20's `02:84`, `:105`,
   `:118`, `:129`, `:152`, `:167`, `:206`, `05:12`, `:69-100`, `:115` (on
   `origin/feature/m6-es-achievements-pages-667`); T26's `02:568-569`,
   `:596`, `:824-833` (on `origin/feature/m6-es-guimenu-673`); T31's
   `02:426`, `:643-648`, `04:80`, `:239`, `05:437`, `:450-462`,
   `tools/t31-build-tests.sh`, `stage-e/fakes/` (13 headers),
   `stage-e/handback-checks.txt:15-19` (on `origin/feature/m6-es-pages-678`);
   T32's `02` § What T33 to T37 inherit when it lands (its brief's `:1060-1065`
   says what it carries: the views' provenance, the cached-read table with
   its writers, the thread table, the bounds table, the outcome routing,
   the `httplib.h` note, the map section for the views) -- read at dispatch
   if it has landed, else mid-run when it does.
9. **The issues**: #771, #781, #1186, #1235, #1170, #301, #1175, #1173,
   #1174, #609, #1194, #1203, #1204, #1150, #1140, #1143, #1144, #560, #69,
   #585, #1137, #1138, #1141, #246, #243, #245, #248, #280, #288, #175,
   #183, #145, #127, #99, #308, #307, #186, #574, #566, #64, #63, #700,
   #679, #678; #680's own body. States the inherit digest read
   2026-10-27: #771, #781, #1186, #1235, #1170, #301, #1175, #1173, #1174,
   #609, #1194, #1203, #560, #69, #585, #1143, #1144, #1140, #1137, #1138,
   #1141 OPEN; #300, #246, #243, #245, #578 CLOSED; #649, #665, #667,
   #668, #673, #678 OPEN until the integration merge (§ 1); #679 OPEN, in
   flight. The lane re-reads each with `gh issue view` at stage A and
   records the states it saw.
10. **Time to play**: `docs/vm-qa-log.md:9-18` (the three headline
    columns; *"no budget row exists yet"*); `time-to-play.md`'s one budget
    (the exit sync's 3 s, D-CLOUD-119). This slice sits on the two paths at
    three points: **the exit path** -- `CaptureRotation::recordAfterSession`
    (`FileData.cpp:1166-1167`), `CollectionSystemManager::updateCollectionSystem`
    (`:1207`) and `saveToGamelistRecovery` (`:1208`) run after every game
    on the interface thread, inside T2's measured 1.01 s from
    `execute_kill` to the next frame (T2 `02:84`, `04:190`); **the first
    screenshot look after a rescan** -- `DisplayAspect::buildStems` (L-04)
    between a press on SCREENSHOTS and its first frame; and **UPDATE
    GAMELISTS** -- `updateGamelist`'s parse-and-save per dirty system and
    `reloadCollection`'s repopulate. The retro's line names them with what
    they cost on the guest, never "nothing".

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of the families the earlier ES briefs
used -- **a lifetime or a thread**, **a call with no bound**, **a check
whose failure reads as success**, **a read of a file another process
writes, or a write with no last good state**, **a player sentence outside
the vocabulary or without its French**, **work on the interface thread the
lens prices**, **a page the map does not describe and the checker cannot
see** -- with the lens, cost against value, asked of every upstream
surface: what it costs the player (a wait, a read, a thread) against what
it gives. The leads are § 2's L-01 to L-29 and the floor's pure leads
tabled at the end of this section; each is read at its lines before it is
called anything, and the six that FAIL at the pin (§ 5) get their `git log
-S` first (`engineering-practices.md:83`). Upstream-carried surfaces
outside the lanes -- the content installer's card, the Bluetooth scan, the
screensaver, Zaparoo, the key-to-pad editor, the collections flow -- are
read and recorded, fixed only where rule 6's containment holds (D-UI-079).

- **Q1 Lifetimes and threads** (`es-code-traps.md:22`, `:191`;
  `es-native-ui.md:81`, `:175`; `engineering-practices.md:419`; the threads
  run). **L-07**: `ScraperAsyncRequestsBuilder`'s thread joined only in
  `update()` `:230-234` and never in a destructor (none exists); the owner
  drops it at `:358-361` (`searchHandle.reset()` in `stop()`) and
  `:96-100` -- proved by reading; the guest cannot make the window
  reliably (T32's G-05 shape, B during the search, is the attempt, labelled
  `image`); the disposition is a read trace and a contained fix under rule
  6 (a destructor that joins; `std::atomic<bool>` for `mFinished`); T32's
  L-01 is the same family in `ThreadedScraper`, cited. **L-10**:
  `ContentInstaller` and `ThreadedBluetooth` `delete this` on the worker
  (`:247`, `:46`, `:110`) with the thread never joined and the card closed
  from the worker; outside the lanes, recorded with the lens's price (a
  leaked `std::thread` object per run; no `std::terminate` because it is
  never destroyed), fixed only if the coordinator opens the lane at the
  pause. **L-06**: `reloadCollection` `:1558-1600` repopulates the custom
  collection (`populateCustomCollection` `:1576` -> `rootFolder->clear()`
  `:1117`) and then `reloadGameListView(bundle)` `:1589`, which
  `es-code-traps.md:191` says reads the old view's cursor first; the
  holders listed (the bundle view's cursor, `mCurrentView`,
  `FileData::mRunningGame`, the collection's own `mChildren`); the fork's
  `dropGameListView`/`remakeGameListView` halves (`SystemData.cpp:508`)
  the contained fix; the guest's G-02 removes a game from inside the
  collection and reads `journalctl -u essway` for `start_es.sh`'s
  backtrace (`device-builds.md` § Reading a crash); ASan where the harness
  has it; no unit case (views). **L-15**: the `Tree` at
  `SystemData.cpp:470-484` is the one place that drops holders before
  `vanished` deletes; `FolderMergeTests.cpp`'s three cases built and run
  (§ 5), and the guest's G-03 variant (a ROM in a custom collection
  deleted over serial, then UPDATE GAMELISTS, then the collection opened).
  **L-12**: the five `postToUiThread` in `NetworkThread.cpp` against
  `AppWindow::post`; `AppWindowTests.cpp`'s one case built and run, and a
  second case written (closing-then-post returns false; post-then-closing
  waits) if the file lacks it -- the fork's three posts (`:237`, `:251`,
  `:257`) the stream's. **L-24**: sound, recorded. **L-01**'s lock half is
  Q2's. The `.7z` hash and the scrape thread are T32's. A table: every
  `std::thread` construction (5, in 4 upstream files; 0 in fork-own code),
  every `delete this` (3), every `.detach(` of a thread (1), every
  `postToUiThread(` (7 lines in 3 files: `NetworkThread.cpp` 5,
  `AppWindow.h` 1, `SystemScreenSaver.cpp` 1), who joins it, what it
  touches on the interface thread.
- **Q2 Bounded calls** (`es-code-traps.md:238`; `time-to-play.md`;
  D-CLOUD-075; `engineering-practices.md:799`; the bounds run). **L-01**:
  `WatchersManager.cpp:181-196` runs every `check()` under
  `mWatchersLock` and `ResetComponent` (`:92-100`) takes the same lock, so
  `checkCheevosTokenSoon()` (`NetworkThread.cpp:21-25`, from the page's
  save at `GuiRetroAchievementsSettings.cpp:806`) blocks the interface
  thread for the length of the check in flight -- `testAccount`'s HTTPS
  login (`RetroAchievements.cpp:1035-1038`, `getHttpOptions()`'s bound),
  `canUpdate`'s or `getPadsInfo`'s script. The lock is es-core's
  (upstream-carried, T21's file); the three interface-thread callers are
  the fork's (#175, F-RA-19); a contained fix (set `nextCheckTime` under a
  lock of its own, or run `check()` outside `mWatchersLock`) is rule 6,
  put to the pause with T21 named. No unit case (SDL, es-core); the guest
  is G-09's `CANNOT` (no account), so the proof is the read trace and the
  bound's arithmetic. **L-09**: `ZaparooSupport.cpp:37-39` sets
  `connectTimeout` only and `:58-62` nothing -- the slice's own code sets
  no `timeout`/`stallTimeout` anywhere (§ 5's bounds grep prints one line,
  `:38`); outside the lanes, recorded; a `nc -l 7497` on the guest would
  show it and is not asked for. **L-08**: the synchronous second search on
  the interface thread; recorded with the lens's price against `HttpReq`'s
  10 s connect and no total bound (T32's L-06, cited). **L-18**:
  `CloudOffer.cpp:37`'s `timeout 90` is the bound; sound. **L-02**: the
  whole `exec.log` read after every exit, bounded by the launcher's
  truncation (#280) -- the retro's time-to-play line prices it (G-03's
  `stat` of the log). **The callers' side of the hasher**
  (`NetworkThread.cpp:248`, `:251`): T20's #1170 and #301 are the
  hasher's; what T33 records is that the link-up re-index is posted to the
  interface thread by this file (blindspot 64 named it) and what bounds it
  there. A table of every network or script wait reachable from the 77
  with its bound.
- **Q3 Reads that read as success** (`engineering-practices.md:111`,
  `:419`; blindspot 22; `es-player-text.md:236`; the success-reads run).
  **L-18**: `CloudOffer.cpp:42-45` reads rc alone: a script exiting 0
  having created nothing says DONE (the script's half is the rclone
  slice's; the dialog's half is this slice's: what the sentence promises
  against what rc 0 proves). **L-28**: `KeyboardMapping.cpp:265`, `:271`
  drop a trigger `checkTriggerExists` refuses, `:282`, `:288` a key target,
  silently: a unit case on a `parse(json)` seam (`load` `:217-232` reads
  the file then `doc.Parse` `:228`), seen to FAIL at the pin, the fix a
  logged line or a refused load (upstream-carried, outside the lanes:
  recorded with the case, the fix at the pause). **L-27**:
  `FileFilterIndex.cpp:333-340`'s rating arithmetic and `:367`'s year
  test, lifted into string-in/string-out helpers (the T32 shape) with
  cases `ratingKey("0.05")` and `yearKey("3000")` asserting the rule the
  lane proposes, seen to FAIL at the pin, the `git log -S` first. **L-14**:
  `RunLock::holder`'s substring match; a stricter match (argv[0] basename
  equality) is contained; `RunLockTests.cpp`'s three cases built. **L-17**:
  the `int` truncation, a case with an id above 2^31. **T2 FD-15**:
  `CollectionSystemManager.cpp:540`'s `.at()` -- confirm the index range
  against the 28 sort types or clamp. **`MetaData::getInt` `:451`**: `atoi`
  on a player-edited field reads 0 unchecked -- recorded. A table of every
  read and parse with its writer, what a failure reads as, and the unit
  case or guest step that proves it.
- **Q4 Uncached reads and in-place writes** (`es-code-traps.md:104`,
  `:212`; `es-native-ui.md:81`; `engineering-practices.md:829`
  (D-CLOUD-078); `upgrade-and-install.md:40`; T26's readers' rule
  `02:829`; the reads and writes runs). **The reads**: 83 lines (86
  occurrences) of `Utils::FileSystem::exists(`, **4 with `, false)`, all in
  `CaptureRotation.cpp`** (`:113`, `:146`, `:161`, `:170`), one deliberate
  cached read beside them (`:51`, the read-only table), and **0 uncached
  in the 46 upstream files**: each with its file, its writer while ES runs,
  and whether a remembered miss changes the screen. **L-05** is the one
  that reaches a player's data: `Gamelist.cpp:413`'s cached `exists` before
  `updateGamelist` parses the existing file and `:474` writes over it in
  place, and `:112-117`'s cached gate on parse -- a `gamelist.xml` the
  cloud's content restore brings after startup (D-CLOUD-049;
  `rclone-cloud-sync.md:711`) can read as absent for the session and be
  overwritten at the exit by the in-memory nodes alone. The guest's G-04
  variant: a system with no `gamelist.xml`, one written over serial while
  ES runs (the restore's shape without the cloud), a favourite changed,
  QUIT > RESTART, the file diffed against the written bytes --
  the positive, `image` side. **L-11** (`SystemScreenSaver.cpp:156-164`),
  `SystemRandomPlaylist.cpp:87`/`:97`/`:104` and `Gamelist.cpp`'s media
  checks (`:601`, `:705`, `:732-748`) are the same family, recorded with
  the writer that could change them mid-session (the scraper, the API,
  a player over SSH). Whether `FileSystemUtil`'s writers update their own
  cache is T21's file, answered at its lines (`:1051`, `:1067`, `:1097`,
  `:1445`, `:1457-1458`, `:1506-1507`, T32's Q4) and cited, not re-read.
  **The writes**: every file the 77 write, in place or temp-and-rename --
  `Gamelist.cpp:308` (after `removeFile` `:307`: no file between),
  `:474`, `:622`, `:841` (the last two after a copy aside `:619-620`,
  `:838-839`: a last good copy exists, an interrupted save leaves the new
  file cut), `FileFilterIndex.cpp:1313`, `CollectionSystemManager.cpp:345`
  (`std::ofstream`), `KeyboardMapping.cpp:426`, `:429`,
  `CaptureRotation.cpp:175`; against `JourneyTiers`' writer
  (`GuiMenu.cpp:5066`, `AtomicFile::writeText`) and es-core's
  `AtomicFileUtil` (`es-file-tests`). D-CLOUD-078 asks every writer for
  temp-and-rename; `upgrade-and-install.md:58` asks every fix what the old
  writer left (`Already written:` a cut `gamelist.xml` is read by the
  parser as a parse error and the system shows no metadata until the next
  save; a cut `.rotation` reads as untrusted; a cut `.xcc` as no filter):
  the disposition per site is a stream (this slice's, or Backlog #1186's
  for the three it names -- the ruling at the pause), or left with the
  reason. **L-13**: `es-conf-tests`, cited. **L-23**: the `.xcc` and
  `custom-<name>.cfg` writes.
- **Q5 The words, the French and the help bars** (`es-player-text.md:29`,
  `:141`, `:211`, `:236`; `es-code-traps.md:60`;
  `es-ui-style-guide.md:169`; the strings, French and non-ASCII runs).
  **L-25**: `FileTag.cpp:6-11` against `:16-18`: `IN PROGRESS`, `DROPPED`
  and `ON HOLD` reach the screen (`GuiGamelistFilter`, `GuiMetaDataEd`,
  T31's) in English under French; a unit case on `getDisplayIcons` `:30`
  plus the catalog grep is the proof; the fix is three `fake_gettext_`
  lines and three `msgid` entries in the same commit (D-UI-051, § 9) --
  upstream-carried, contained (rule 6), a #585 line. **L-26**:
  `LangParser.cpp:65`'s `"ìndia"` -- a unit case on `extractLang` `:33`
  with `"(India)"`, the design-intent read (`git log -S ìndia`), and the
  disposition (the ASCII token, or recorded). **L-20**: `TextFit.h:34`'s
  byte floor -- `TextFitTests.cpp`'s three cases built, a fourth on a
  4-byte name over the width and a two-character CJK name, FAIL at the pin
  if the rule is characters. **L-19**: `WifiTextTests.cpp` holds the
  two-profiles rule; the words the row shows (`MayBeKey`'s sentence) are
  T31's `GuiWifi`; recorded with the register row that chose it
  (D-UI-118). **L-10**: six `_("AN ERROR OCCURRED") + ": " + updateStatus.first`
  toasts put a tool's status text on the screen
  (`player-language.md`: a tool's words never reach a player) -- outside
  the lanes, recorded. **`CloudOffer`'s three boxes**: YES-first and the
  back landing (`:51-56` on NOT NOW, the last; `:59-64` on NOT NOW;
  `:42-45` on OK) read against `es-ui-style-guide.md:169`; the French
  three-button box at 640x480 (the length of `NOTHING TO RESTORE: YOUR
  CLOUD HAS %s, NOT %s.`) framed on the guest only if G-02's bound allows
  -- the offer needs a cloud, so it is a frame of the dialog raised by
  hand through `cloud_setup`'s protocol line if the harness has it, else
  `CANNOT` with the reason. **The 196 msgids** against the catalog (the
  fork-changes digest's lookup, re-run); `tools/es-untranslated`'s two
  lines; the 0 non-ASCII comments; `MetaData.cpp`'s 45 labels and
  `FileSorts.cpp`'s 29 sort names against `tools/es-untranslated`. **The
  help bars**: none in the 77 (no `getHelpPrompts` here); the pages are
  T31's.
- **Q6 The library's cost** (the lens; `time-to-play.md`;
  `es-code-traps.md:164`, `:191`; `es-native-ui.md:324`; D-UI-080/081;
  the cost run). **L-04**: `DisplayAspect::buildStems` `:74-87` walks
  every non-collection system's `getFilesRecursive(GAME)` `:83` under
  `sShotLock` on the interface thread at the first miss after
  `forgetScreenshots()` (after every rescan that changed anything,
  `SystemData.cpp:503-504`, and every `reloadAll`,
  `ViewController.cpp:1470`), and every hit walks the tree by
  `FolderData::FindByPath` `:96` (`FileData.cpp:1914-1926`) -- the
  guest's G-03 then a press on SCREENSHOTS, `tools/time-to-play`'s shape
  with N seeded captures (N the lane's judgement at stage B inside the
  window's bound), a `LogInfo` on `buildStems` for the count (none at the
  pin; a diagnostic the stream may add). **L-02**: the exit path's read of
  `exec.log` and `retroarch.cfg`, priced in the retro. **L-08**: the
  synchronous search. **L-11**: `SystemScreenSaver.cpp:350`'s first-start
  walk, and `:546`'s `launchGame` past `ViewController::launch`'s checks
  (T2's brief `:293-294`): what the checks guard (the image viewer, the
  netplay downgrade, input locked, the splash) and whether the saver's
  launch needs them -- read, recorded, the lane named for the coordinator.
  **`FileFilterIndex`**: the index built per system at load and the text
  filter's `jw_distance` `:557` per game -- priced. **`reloadCollection`**:
  per repopulate. The two numbers in the retro.
- **Q7 The structure, the map and the merge debt** (`es-native-ui.md:32`,
  D-UI-039; `es-ui-style-guide.md:268`; `device-builds.md` § Build
  credentials; `engineering-practices.md:576`; the membership, scope and
  delta runs). **L-22**: `ScraperCmdLine.{cpp,h}` in no list, with no
  caller and a header the tree lacks -- recorded as Backlog #1235's shape
  (the coordinator has added them there), never deleted by the lane
  (`:576`: a deletion lists what the doomed copy does; here nothing, and
  the deletion is still the coordinator's call). **L-21**: the Windows
  residue, one row each, D-WORKFLOW-209's disposition. **L-14**: structure
  half, Q3's. **The map**: FILTER GAMELIST BY and EDIT DYNAMIC COLLECTION
  FILTERS (T31's pages over `FileFilterIndex`) are in neither the map nor
  `## Not mapped`, beside the declared SCREENSAVER SETTINGS (`:699`) and
  ADD TO CUSTOM COLLECTION... (`:704`); the two rows are mapped in the
  same commit as any row a stream touches, else a punch item saying
  which; UPDATE GAMELISTS as a row of GAME COLLECTION SETTINGS
  (`GuiCollectionSystemsOptions.cpp:368`) is recorded as unmapped and
  named for the coordinator. **The credential macros**: not here (§ 1);
  `02` § The structure says so in one sentence and points at the top-level
  file's lines by name. **`es-app/CMakeLists.txt`**: the three
  conditionals, the 30 `ES_SOURCES` entries of the slice (unconditional)
  and the one absent; the 34 of 41 headers in `ES_HEADERS` and the seven
  not (a listing omission, not a build one); the ten lines T21's branch
  adds, named as a collision. **The merge debt**: the two § 5 commands
  (`log --format=%h cada856d86..rocknix/master -- $FILES` 0, `diff
  --numstat` empty), both bases named, the four modified files with their
  numstat pairs, batocera's six as context, and what the slice carries
  that upstream lacks as the #585 candidates the coordinator weighs: three
  patches to shared files (`maskSecrets` on the logged command line,
  `80f52e500`, needs `StringUtil`'s `maskSecrets`, 0 files at
  `rocknix/master`; the bounded token-check retry at link-up,
  `d9d6083de`/`461e14305`/`42f9e8851`, needs `testAccount(..., bool*
  refused)` at `RetroAchievements.h:282`; the startup index re-run at
  link-up, `cce9ab12a`, needs `ThreadedHasher::cheevosLibraryCameThisSession`
  and `SystemData::startIndexesAtStart`) and three helper-file fixes
  whose consumers sit in earlier slices (`FolderMerge.h`,
  `CheevosIndex.*`, `GameCubeRvzHashRetry.h`), plus L-25's three lines.

### The floor's pure leads, carried

The floor digest is in no tree, so its § 3 is here in the shape `file:line
at the pin | the function | the defect a unit case would catch`; rows with
no case shape are dropped; **(fork-own)** marks the fork's units; the six
that FAIL at the pin are in bold. Each is a case in `CloudText`'s or
`ScraperReplies`'s shape (§ 5 item 1) unless marked file or guest.

| # | At the pin | Function | What a case would catch |
| --- | --- | --- | --- |
| 3.1 | `PlatformId.cpp:215` (`:220`), `:227` (`:233`), `:237` | `getPlatformId`, `getPlatformName`, the `ArcadeSystems` map | `getPlatformId(nullptr)`; a duplicated table string shadowing an id; an enum value with no row reading `"unknown"`; short names not lowercase |
| 3.2 | `MetaData.cpp:28` (`:30-66`), `:42-43`/`:46-47` | `initMetadata`'s `gameDecls` | a key typed twice with two types; `Emulator`/`Core` twice by design, the case pins which wins |
| 3.3 | `MetaData.cpp:280` (`+153`, `+158-161`, `+167-169`, `+199-201`) | `appendToXML` | a player-set value equal to its default dropped under `ignoreDefaults`; an `MD_PATH` written absolute when relative was asked |
| 3.4 | `MetaData.cpp:357`, `:407`, `:435`, `:451`, `:454`, `:459` | `set`, `get`, `exists`, `getInt`, `getFloat`, `wasChanged` | `getInt` on `""`; a non-numeric `playcount`; `set` of the same value flipping `wasChanged` |
| 3.5 | `MetaData.cpp:469` | `importScrappedMetadata` | a scrape wiping a player's favourite flag; an empty scraped field blanking a filled one |
| 3.6 | `MetaData.cpp:270` (`+124`) | `migrate` (`FileData*` on the signature: the lane finds the seam) | an old `<hash>` lost on first load (`upgrade-and-install.md:95`: read both) |
| 3.7 | `MetaData.cpp:151` (`+20-28`, `+66-70`) | `loadFromXML`'s default-and-lowercase rule and the `<scrap>` reading, lifted | a `"TRUE"` another tool wrote not read as true |
| 3.8 | `Genres.cpp:185`, `:234`, `:257`, `:293`, `:323` (`init` `:19`) | the genre lookups, over a seam that takes a document | a game counted twice in the genre filter (parent and child); a trailing comma |
| **3.9** | `FileFilterIndex.cpp:247` (**`:322-341`, `:364-369`**), `:362` | the rating, year and played predicates, lifted into string-in/string-out helpers | **`ratingKey("0.05")` reads `0 STARS` where `""` and `"0"` read UNKNOWN (`:333`, `:339`); `yearKey("3000")` and `yearKey("999")` read `""` (`:367`)** (L-27) |
| 3.10 | `FileFilterIndex.cpp:557` | `jw_distance` (file-static Jaro-Winkler) | identical -> 1.0; empty vs non-empty -> 0; symmetric; a distance above 1 or NaN on an empty string |
| 3.11 | `FileFilterIndex.cpp:1107-1321` (`+11`, `+37-39`, `+99-161`) | `CollectionFilter::load`/`save` on a temp `.xcc` (file) | a tag `save` writes that `load` ignores: a filter forgetting one of its rows on restart |
| 3.12 | `Gamelist.cpp:255`, `:288` (`:261`, `+274`, `+283`) | `addFileDataNode`, `saveToXml` (needs `FileData*`/`SystemData*` doubles, `tests/app-unit/fakes/FileData.h`) | a `<path>` written absolute into a per-system gamelist |
| **3.13** | `Gamelist.cpp:374` (**`:413`, `:466-477`**; `:308`, `:622`, `:841`) | `updateGamelist`'s shape | **the in-place `doc.save_file` with no temp-and-rename (D-CLOUD-078) and the cached `exists` before it** (L-05); the shape in a file case, the atomicity `CANNOT` without a fault seam (G-05) |
| 3.14 | `Gamelist.cpp:112` (`+35-38`, `+47`, `+61-63`, `+66`, `+79-83`) | `loadGamelistFile` through its `!fromFile` branch (a string) | a `<path>` with a trailing newline or `\` never matched; the size-mismatch warning |
| 3.15 | `Gamelist.cpp:518`, `:631`, `:483` (`+601`, `+705`, `+732-748`) | `packGamelist`, `cleanupGamelist` (file or guest) | `cleanupGamelist` dropping a media reference that exists on disk through the cache |
| 3.16 | `CollectionSystemManager.cpp:1508`, `:1513`, `:1518`, `:1523`, `:1532` | the collection paths | a name containing `/` or `..` writing outside the collections folder |
| 3.17 | `CollectionSystemManager.cpp:598` (`:627`, `:646`, `:651`; `themeFolderExists` `:1492`) | `getValidNewCollectionName` over a seam for `sSystemVector` | an auto-collection name (`"all"`) or a theme folder accepted |
| 3.18 | `CollectionSystemManager.cpp:1434` (`+1450`) | `getCollectionsFromConfigFolder` over a handed listing | `custom-.cfg` or `custom-a.cfg.bak` read as a collection |
| 3.19 | `CollectionSystemManager.cpp:34` (`:40`) | `getSystemDecls` | names or theme folders not unique; `recent`'s sort |
| 3.20 | `CollectionSystemManager.cpp:540` | the `.at()` on a set value (T2 FD-15, #771) | an index outside the 28 sort types |
| **3.21** | `KeyboardMapping.cpp:217` (**`:265`, `:271`, `:282`, `:288`**; `checkTriggerExists` `:178`) | `KeyMappingFile::load`'s parse, split out as `parse(json)` | **a trigger naming an unknown key dropped silently: a mapping loads as an action with no trigger** (L-28); a parse error -> what `isValid` `:499` says |
| 3.22 | `KeyboardMapping.cpp:328`, `:432`, `:512`, `:535`, `:586`, `:726`, `:776`, `:793` | `save`, `fromP2k`, `triggerEquals`, `toTargetString`, `updateMapping`, `removeMapping`, the descriptions | a description with a quote breaking a JSON written by hand (read `:328-431` first); `save -> load` round trip |
| 3.23 | `KeyboardMapping.cpp:178`, `:190`, `:199`, `:208` (the tables `:163-176`) | `checkTriggerExists`, `checkTargetExists`, `getTriggerFromP2k`, `getTargetFromP2k` | a key whose name has two `_` taking the wrong tail |
| 3.24 | `CustomFeatures.cpp:23` (`:13-21`) | `parseFeatures` | a feature name with a trailing space never enabling its row |
| 3.25 | `CustomFeatures.cpp:406`, `:61`, `:93`, `:155` (`:202-207`, `:224-227`, `:242-251`, `:256`, `:292-298`) | `loadCustomFeatures` over an XML string | a feature declared on the core not reaching the menu when the emulator declares none |
| 3.26 | `CustomFeatures.cpp:529`, `:534`, `:523` | `hasFeature`, `hasGlobalFeature`, `sort` | a case mismatch between `es_features.cfg` and the launcher |
| 3.27 | `FileSorts.cpp:93` (`:96`, `:99`, `:106`; `:83`) | `stripLeadingArticle` | an article matched by prefix; a title that is only an article emptied; `_("A,AN,THE")` translated |
| 3.28 | `FileSorts.cpp:32` (`:43-71`) | `getSortType` and the 28-row table | an id twice; a pair not sharing its comparator; `getSortType(-1)` falling to the first row |
| **3.29** | `FileTag.cpp:30` (**`:6-11` against `:16-18`**) | `getDisplayIcons` | **three of nine names outside `_()` and absent from the catalog** (L-25); `"finished"` -> 0 (exact case) |
| 3.30 | `LibretroRatio.cpp:51` (`:12-43`) | `getRatio()` | keys not unique; a value RetroArch does not accept |
| **3.31** | `LangParser.cpp:33` (**`:65`**; `:37-64`) | `extractLang` | **`"ìndia"` unreachable: only `"in"` matches** (L-26); `"(USA, Europe)"` -> en + us,eu |
| 3.32 | `LangParser.cpp:144`, `:203`, `:18` | `parse`, `getFlag`, `getLanguageString` | a region with no flag asset drawing a broken image |
| 3.33 | `CaptureRotation.cpp:51` against `:113`, `:146`, `:161`, `:170` **(fork-own)** | the one cached read beside four uncached | a rotation table written after ES started reading as absent (by design: the lane records the comment `:23-30`) |
| 3.34 | `SystemRandomPlaylist.cpp:24` (`:12`, `:87`, `:97`, `:104`) | `getNextItem` over a seam for the RNG | a path that starts existing mid-session never seen |
| **3.35** | `TextFit.h:30` (**`:34`**), `:12` **(fork-own)** | `fitOneLine` with a fake measure (1 px per char), `popCharacter` | **a 4-byte name over the width never gets its ellipsis; a two-character CJK name stops at one** (L-20); a label cut inside a UTF-8 sequence |
| 3.36 | `JourneyTiers.h:38`, `:51`, `:105` (`:117`), `:133` **(fork-own)** | `record`, `parse`, `replaceRecord`, `command` (`JourneyTiersTests.cpp`'s 8 cases first) | a two-byte record read as empty; a `Write` that fails -> `OldRecordStands`; the literals' exact shape |
| 3.37 | `FolderMerge.h:38` **(fork-own)** | `merge(live, fresh, tree)` (`FolderMergeTests.cpp`'s 3 cases first) | a live node dropped when the fresh tree holds it under a different case; a renamed folder |
| 3.38 | `RunLock.h:29`, `:44` **(fork-own)** | `held`, `holder` (`RunLockTests.cpp`'s 3 cases first; file) | a stale lock file read as held; the substring match (L-14) |
| 3.39 | `GameCubeRvzHashRetry.h:8`, `:16` **(fork-own)** | `trim`, `needed` | a valid unknown hash retried; whitespace only |
| 3.40 | `AppWindow.h:24`, `:30`, `:38`, `:49` **(fork-own)** | `gate`, `open`, `post`, `closing` (`AppWindowTests.cpp`'s 1 case first) | a task posted after `closing()` running; a task posted before running twice |
| 3.41 | `OfflineAchievementsText.cpp:18`, `:231` **(fork-own)** | `jsonInt`, `parsePendingIds` | the `int` truncation (L-17) |

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #680.** Every read, count and table runs on the host
   at the pin's bytes. **The host has no toolchain** (#1137):
   `tools/es-syntax-check` exits 2 on this host (`no build root at ...`,
   its `:69`) and records that line with `ES_BUILD_ROOT` set, never
   empty; **0 of the 31 `.cpp` were ever syntax-checked on the host** and
   7 of them link into `es-unit-tests` (§ 2). The include graph, read not
   compiled (the floor's § 2.1): the `FileData.h`/`SystemData.h` chain
   reaches no SDL, curl or vlc header (`FileData.h` ->
   `utils/FileSystemUtil.h MetaData.h KeyboardMapping.h SystemData.h
   SaveState.h BindingManager.h`; `SystemData.h` -> `PlatformId.h
   <pugixml> FileFilterIndex.h KeyboardMapping.h math/Vector2f.h
   CustomFeatures.h utils/VectorEx.h BindingManager.h`; vlc is in
   `VideoVlcComponent.cpp:8-9`, not its header), so the 31 fall in six
   classes: **(a) pure, 12** (`CaptureRotationText`, `CheevosIndex`,
   `CheevosRetry`, `CloudFolderValidation`, `CustomFeatures`,
   `DisplayAspectText`, `FileTag`, `KeyboardMapping`, `LibretroRatio`,
   `OfflineAchievementsText`, `PlatformId`, `WifiText`; five of them never
   compiled on the host); **(b) the FileData chain with no SDL on the
   graph, 6** (`MetaData`, `Gamelist`, `Genres`, `CaptureRotation`,
   `FileSorts`, `FileFilterIndex`) -- **the first candidates for the
   stand-in check**; **(c) SDL through `GuiComponent.h`/`Window.h`/`ApiSystem.h`,
   10** (`CloudOffer`, `CollectionSystemManager`, `ContentInstaller`,
   `DisplayAspect`, `LangParser`, `NetworkThread`, `SystemRandomPlaylist`,
   `SystemScreenSaver`, `ThreadedBluetooth`, `components/ScraperSearchComponent`);
   **(d) curl, 1** (`ZaparooSupport`); **(e) WIN32-only, 1**
   (`Win32ApiSystem`: a check proves it preprocesses to nothing); **(f)
   unbuilt, 1** (`ScraperCmdLine`: its `platform.h` does not exist; a
   case cannot link it). T21's `stage-e/syntax-check.sh` (`:14` `g++
   -std=c++17 -fsyntax-only -DHAVE_INTL -I "$F" -I es-app/src -I
   es-core/src -I external`) with T31's **13 fakes** (`FreeImage.h`,
   `SDL.h`, `SDL_audio.h`, `SDL_events.h`, `SDL_joystick.h`,
   `SDL_keyboard.h`, `SDL_main.h`, `SDL_mixer.h`, `SDL_mutex.h`,
   `SDL_timer.h`, `alsa/asoundlib.h`, `curl/curl.h`, `ft2build.h`, under
   `docs/audits/2026_10_27-epic-m6-es-pages/stage-e/fakes/` on
   `origin/feature/m6-es-pages-678`) runs over classes (a) to (d), 29
   files, `rc` per file recorded; it checks the file's own C++ and proves
   nothing about SDL or curl. **The host floor is the lane's own: unit
   cases for the pure leads** in `CloudText`'s shape (`es-code-traps.md:139`)
   -- **first the five case files that exist and have never been built**
   (`tests/app-unit/{JourneyTiers,FolderMerge,RunLock,TextFit,AppWindow}Tests.cpp`,
   18 cases by `grep -c TEST_CASE`, the `app-unit-tests` target at
   `tests/app-unit/CMakeLists.txt:35-41`), **then the six that FAIL at the
   pin** (3.9, 3.13, 3.21, 3.29, 3.31, 3.35, in bold in § 4's table), each
   seen to FAIL against the unfixed extract before it is trusted, the stub
   that constructs the failure checked against the unfixed code first
   (`engineering-practices.md:464`); then the rest. The cases are **built
   by the lane's generated script in T31's shape**
   (`docs/audits/2026_10_27-epic-m6-es-pages/tools/t31-build-tests.sh`:
   the targets parsed out of `es-app/tests/unit/CMakeLists.txt` by a
   `python3 -I` pass (`:30`), `g++ -std=c++17 -O0 -g0 -pthread` (`:44`),
   include roots `es-app/src`, `es-core/src`, `external` and
   `RAPIDJSON_INCLUDE_DIR` (`:57`), pugixml from `PUGIXML_INCLUDE_DIR`
   (`:69-78`), the `TOTAL:` echo (`:112`); **rapidjson from the recipe's
   tarball plus its four patches** (`projects/ROCKNIX/packages/devel/rapidjson`,
   1.1.0, unpacked under `/workspace/tmp/m6-t33/rj/` as T21 and T32 did);
   **pugixml from the pin's extracted source** under
   `/workspace/cache/rocknix-sources/emulationstation/emulationstation-<PIN>/external`),
   **extended to parse `tests/app-unit/CMakeLists.txt`'s `app-unit-tests`
   too** (its sources are the five test files and `main.cpp`, its include
   root `tests/app-unit/fakes` before `es-app/src`), saved as
   `docs/audits/<audit>/tools/t33-build-tests.sh`, **the total quoted as
   the script's `TOTAL: N test cases in B binaries` line** and never
   summed by hand (`engineering-practices.md:250`; T31's close read `TOTAL:
   228 test cases in 4 binaries` with `es-unit-tests ... 192 | 0 failed`,
   its `handback-checks.txt:15-19`); `Settings.cpp`, `AtomicFileUtil.cpp`,
   `FileSystemUtil.cpp`, `StringUtil.cpp` and `md5.cpp` are host-buildable
   dependencies a case may link. `tools/es-menu-map-check`,
   `tools/es-untranslated --upstream bccd715707` (and the same with
   `cada856d86`, both lines recorded), the non-ASCII comment grep, the
   counts and the generated tables run on the host.
2. **The guest window** -- one, asked for on #680 at stage B's end with its
   plan and bound (**25 minutes proposed, plus 5 of grace**: the plan below
   sums to 1,260 s, 21 minutes, by the floor's awk over `60 240 180 180
   300 180 120`; T32's window was 35 + 5 for a 22-minute plan with a stub
   row), granted explicitly by the coordinator on #680 and in the shared
   log's queue. **The queue is the shared file's own lines**,
   `/tmp/m7-m6-host-coordination-20261023.txt`: a request is a line that
   names the slice, its plan and its bound; the grant is the coordinator's
   line answering it; the lane's START and RETURN each add a line with the
   census; the file is read before any guest starts (§ 1's last command
   reads its tail; today it shows T32's START at 16:08:36 UTC). One boot
   of the M6 copy of the image (`/workspace/artifacts/m6-t2-20261023/`,
   `069fc2704421`) **started at 640x480**
   (`projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless
   --daemonize --res 640x480`, `generic-x64-vm-testing.md:108`, `:215`,
   #1141), **under T13's conditions -- T13 is #660, the first M6 lane to
   hold a guest window, and its shape is every later window's (T26's,
   T31's and T32's included); spelled out here so the lane needs no other
   file:** one guest, from that M6 copy, at 640x480; **the image
   identified by two literals first** (`BUILD_ID` from `/etc/os-release`
   and the file name); **every verdict labelled by side** because the
   image's EmulationStation is M7's composition -- a frame is `pin-binary`
   evidence only where the digest found the pin's lines unchanged against
   the image's binary, else `image` (`generic-x64-vm-testing.md:1432`);
   the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as the
   first line of each post on #680 and a line in the shared host file,
   each with the census (`qemu N, compilers N`); the stop by pidfile at
   bound plus grace (`tools/vm-stop`, never a pattern); the disk retired
   after with path, size and sha (D-INFRA-022); and the guarded
   `tools/build-preflight --reclaim-swap` allowed once, before the guest,
   never beside it. **The floor's limit, said plainly: a no-NIC guest
   cannot show the content installer's download (every branch is
   `ApiSystem::installBatocera{Theme,Bezel,StorePackage}` over the
   network, `:132`, `:170`, `:206`), NetworkThread's three checks (UPDATE
   AVAILABLE needs `updates.enabled` and `canUpdate` over the network
   `:87-95`; the token check `:120-178` needs an account, D-QA-016, which
   no row grows; the pads battery `:58` needs a pad), the screensaver's
   video and slideshow modes (no media in the fixture), or the atomicity
   of the gamelist write (no fault seam).** None of these needs a device;
   each is a unit lead or a harness gap to name (`bugs-are-agent-first.md`
   rule 3). What the guest does show: a custom collection created, shown
   and toggled; UPDATE GAMELISTS over seeded stubs and the index's toast;
   a `gamelist.xml` written and read back; the screensaver's dim and
   black; the key-to-pad editor and its file; the French strings. The QA
   accounts are needed by no row (`tools/qa-accounts`, never printed;
   never the owner's, D-QA-015). Every proof's frames are labelled by
   side; a fix's frame is `fix-walk-pending-image`.

   | G | Behaviour only the running image shows | Walk or serial command | Expected frame or line | Bound (s) |
   | --- | --- | --- | --- | ---: |
   | G-01 | identity and side | `vm-serial sh 'cat /etc/os-release; fbset'`; the ES binary's digest against the pin's lines (T26's `g01-identity.txt` shape) | `BUILD_ID=...`, `640x480`; every frame labelled `image` or `pin-binary` | 60 |
   | G-02 | a custom collection created, enabled, shown and toggled (L-06, L-15) | the on-screen keyboard has no walk (T32 § 5.1), so seed it: `vm-serial sh 'printf "%s\n" /storage/roms/<sys>/<rom> > <collections folder>/custom-t33.cfg'` (the folder from `getCollectionsFolder` `:1518` read on the guest; the file shape from `saveCustomCollection` `:333-357` read first), ES restarted (`generic-x64-vm-testing.md:382`: back on the last list -- one `z`, a frame, then drive), MAIN MENU > GAME COLLECTION SETTINGS > COLLECTIONS TO DISPLAY, tick `t33`, back; `shot` the carousel and the list; then SELECT on the game inside the collection > ADD TO CUSTOM COLLECTION (menu map `:704`) to remove it, `shot`, and `journalctl -u essway` read for `start_es.sh`'s backtrace | the collection in `SystemView` and its one game in the list (`populateCustomCollection` `:1103`); the file read back over serial lacking the path after the toggle (`toggleGameInCollection` `:671`); a clean list after the removal, or the backtrace (L-06's positive) -- `image` side | 240 |
   | G-03 | UPDATE GAMELISTS over a seeded library, the index card, and the stem walk (L-04, L-02) | three zero-byte ROM stubs with valid extensions seeded under `/storage/roms/<sys>/` over serial (`loadGamelistFile` `+79-83` refuses a path that does not exist); N capture stubs under the SCREENSHOTS source (N the lane's, inside the bound); GAME SETTINGS > UPDATE GAMELISTS (`GuiCollectionSystemsOptions.cpp:368`); `/isIdle` waited for (D-QA-057: the installer, the hasher); `shot` the carousel and `1-list`; then a press on SCREENSHOTS timed to its first frame (`tools/time-to-play`'s shape); `stat` of `/var/log/exec.log` | the three stubs in the list; with INDEX NEW GAMES on (menu map `:625`) the `INDEXING COMPLETED. UPDATE ...` toast (`ThreadedHasher.cpp:146`) against the one-line rule; the SCREENSHOTS press-to-frame number for the retro -- `image` side | 180 |
   | G-04 | a `gamelist.xml` written and its shape; the stale read (L-05) | one stub marked FAVORITE through SELECT; a `gamelist.xml` for a second system written over serial while ES runs (the restore's shape without the cloud); QUIT > RESTART EMULATIONSTATION (the clean exit writes dirty files, `updateGamelist` `:374`); `vm-serial sh 'cat /storage/roms/<sys>/gamelist.xml; ls <recovery>/<sys>'` (`getGamelistRecoveryPath` `:22`); the second system's file diffed against the written bytes | `<gameList><game><path>./<stub></path>...<favorite>true</favorite>` -- relative path (`+283`), only non-default fields (`ignoreDefaults` true at `:261`), the recovery directory empty after the clean exit (menu map `:626`); the second file unchanged or overwritten (L-05's positive, read both ways) -- `image` side | 180 |
   | G-05 | the in-place write's window (`doc.save_file` `:474`) | -- | `CANNOT` on the guest without a fault seam; the lead stays a unit case for the shape (3.13) and a review note for the atomicity | 0 |
   | G-06 | the screensaver starting and stopping | with ES stopped (`generic-x64-vm-testing.md:1145`, `:1155`): `ScreenSaverTime` one minute and `ScreenSaverBehavior` `dim` in `es_settings.cfg` over serial, ES started, 70 s waited, `shot`; `wake` (`wake.steps`: `shift`), `shot`; once more with `black` | a dimmed frame then the same screen awake; a black frame; `journalctl -u essway` quiet (`Scripting::fireEvent("screensaver-start")` runs nothing unless a script exists); `random video` and `slideshow` not in this window -- `image` side | 300 |
   | G-07 | the content installer's card | -- | `CANNOT` on a no-NIC guest; the card's title `DOWNLOADING <n>` (`:78`) and the toasts (`:140`, `:159`, `:178`, `:214`, `:232`) read as strings | 0 |
   | G-08 | the key-to-pad editor and its file (L-28) | on a stub game, SELECT > KEYBOARDTOPADS (menu map `:707`, upstream, tab strip under #63); one mapping set, saved; `shot` the editor; `vm-serial sh 'cat <the .keys file>'` (its path from `save` `:328` read first); then one unknown trigger name written into the file over serial, ES restarted, the editor reopened | the editor frame at 640x480; a JSON with one player array holding `type`, `trigger`, `target` (`:250-288`); the unknown trigger absent from the reopened editor with no word said (L-28's positive) -- `image` side | 180 |
   | G-09 | NetworkThread's checks | -- | `CANNOT` on this guest (above); the retry schedule is `CheevosRetry`'s 7 cases | 0 |
   | G-10 | close | `tools/vm-stop` on the pidfile; the disk's size and sha; `qemu 0, compilers 0` | `retired.txt`; the leftover check | 120 |

   Sum of the bounds as written: 1,260 s (21 min), the floor's figure by
   its author's command. Every frame is read back for its strings.
3. **What T34 to T37 inherit** is written, not tested here: the slice's
   provenance table (27 / 4 / 46 with both bases named), the cached-read
   table with its writers (83 rows), the write table (the ten sites, in
   place or atomic), the thread-and-lifetime table, the bounds table, the
   `app-unit-tests` build recipe (the five case files and their fakes),
   the map's two filter rows, and the Windows residue's dispositions.
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   ES branch, proven twice (`fix-unit-test` through a case the build
   script links, or `fix-walk-pending-image`), the covering case run before
   every commit, under § 9's same-commit rules for the map and the French;
   a fix on `es-app/CMakeLists.txt`, `WifiText.*` or
   `OfflineAchievementsText.*` that meets T21's `3ae9610b0` or T20's
   `5c0ddaaee` lines is written against the pin and named as a collision
   in the hand-back (§ 1).

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its
reason). From the distribution worktree after the membership block; `W`
the ES worktree (§ 1), `PIN` the pin, `MB` the merge base, `FILES` the 77
from the block's paths file; counts by `/usr/bin/grep` (#1138); **every
grep for `_("` is `-F`** -- the basic-regex form with `\(` was T31's
stage-A erratum and is not written here; `rc=$?` on its own line, never
after a pipe. Every expectation below is a line the drafter printed from
the pin on 2026-10-27 in `qa-integration`, except the ones marked by stage,
which cannot run before the lane writes their inputs, and the three marked
`[unverified]`, which the proof runs:

```bash
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-system-680; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; C=8ebaf8daad; MB=cada856d86
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t33/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
FILES=$(cat .qa-scratch/t33/paths.txt); T=$(printf '%s\n' $FILES | $G -v -E '\.(aps|ico)$')
# the scope (expect 77; cpp 31; h 41; other 5; text 75)
printf '%s\n' $FILES | $G -c .; printf '%s\n' $FILES | $G -c '\.cpp$'; printf '%s\n' $FILES | $G -c '\.h$'; printf '%s\n' $FILES | $G -c -v -E '\.(cpp|h)$'; printf '%s\n' $T | $G -c .
# the ES worktree at the pin, clean; the bases; the counts (expect the pin; 0; cada856d86; f6c542872e; 725; 14; 1; 3ae9610b0; 5c0ddaaee)
git -C "$W" rev-parse HEAD | cut -c1-10; git -C "$W" status --short | wc -l; git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10; git -C "$W" rev-parse rocknix/master | cut -c1-10; git -C "$W" rev-list --count bccd715707.."$PIN"; git -C "$W" rev-list --count "$MB"..rocknix/master; git -C "$W" rev-list --count bccd715707.."$MB"; git -C "$W" rev-parse origin/feature/m6-es-state-and-bridge-668 | cut -c1-9; git -C "$W" rev-parse origin/feature/m6-es-achievements-pages-667 | cut -c1-9
# the lines two ways (expect wc -l text 16272; grep -c text 16276; no trailing newline: 4 -- EmulationStation.h.in 26/27, KeyboardMapping.cpp 816/817, LangParser.cpp 241/242, NetworkThread.cpp 273/274)
for p in $T; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l text", s}'; for p in $T; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c text", s}'; n=0; for p in $T; do a=$(git -C "$W" show "$PIN:$p" | wc -l); b=$(git -C "$W" show "$PIN:$p" | $G -c ''); [ "$a" != "$b" ] && { n=$((n+1)); echo "no newline: $p $a/$b"; }; done; echo "no trailing newline: $n"
# the fork's delta (expect `31 files changed, 2689 insertions(+), 7 deletions(-)` three times; 27 added; the four M rows `44 0 es-app/CMakeLists.txt`, `105 3 es-app/src/NetworkThread.cpp`, `29 1 es-app/src/NetworkThread.h`, `3 3 es-app/src/Win32ApiSystem.cpp`; 72 commits, 68 non-merge, the merges `da702d8b6 370ebe416 137309b7d 6c7a36d04`)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $FILES; git -C "$W" diff --shortstat "$MB" "$PIN" -- $FILES; git -C "$W" diff --shortstat rocknix/master "$PIN" -- $FILES; git -C "$W" diff --diff-filter=A --name-only bccd715707 "$PIN" -- $FILES | $G -c .; git -C "$W" diff --diff-filter=M --numstat bccd715707 "$PIN" -- $FILES; git -C "$W" log --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; git -C "$W" log --no-merges --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; git -C "$W" log --merges --format=%h bccd715707.."$PIN" -- $FILES | tr '\n' ' '; echo
# upstream's delta: the merge-debt record (expect 0 rc=1; 0 rc=1; identical to rocknix/master: 46; identical to cada856d86: 46; the two GuiMenu files as upstream's whole delta)
git -C "$W" log --format=%h "$MB"..rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream commits rc=$rc"; git -C "$W" diff --numstat "$MB" rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream numstat rc=$rc"; n=0; for p in $FILES; do git -C "$W" cat-file -e "rocknix/master:$p" 2>/dev/null && git -C "$W" diff --quiet rocknix/master "$PIN" -- "$p" && n=$((n+1)); done; echo "identical to rocknix/master: $n"; n=0; for p in $FILES; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && git -C "$W" diff --quiet "$MB" "$PIN" -- "$p" && n=$((n+1)); done; echo "identical to cada856d86: $n"; git -C "$W" diff --name-only "$MB" rocknix/master | tr '\n' ' '; echo
# the other lanes' deltas inside the 77, inherited (expect T21: `10 0 es-app/CMakeLists.txt`, `11 0 es-app/src/WifiText.cpp`, `13 0 es-app/src/WifiText.h`, commits `44d3c7e25 e38dcdefd eeee95265 31b49999e 00669ccd9 ba0e82c1f`; T20: `99 0 .../OfflineAchievementsText.cpp`, `52 0 .../OfflineAchievementsText.h`, commits `274a71add f85061f14`; T26, T31, T2, T18 empty)
for b in origin/feature/m6-es-state-and-bridge-668 origin/feature/m6-es-achievements-pages-667 origin/feature/m6-es-guimenu-673 origin/feature/m6-es-pages-678 origin/feature/m6-es-launch-path-649 origin/feature/m6-es-cloud-pages-665; do echo "== $b"; git -C "$W" diff --numstat "$PIN" "$b" -- $FILES; git -C "$W" log --format=%h "$PIN".."$b" -- $FILES | tr '\n' ' '; echo; done
# the strings, two ways (expect `_(" lines TOTAL 176 in 11 files`; occurrences 223; MetaData.cpp 45 and FileSorts.cpp 29 the two largest)
git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "_(\" lines TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F '_("' "$PIN" -- $FILES | wc -l
# the dialogs and pages built (expect `new Gui TOTAL 10 in 3 files`; `7 GuiMsgBox; 1 GuiTextEditPopupKeyboard; 1 GuiTextEditPopup; 1 GuiLoading`; the sites read whole for the buttons in order)
git -C "$W" grep -c -E 'new Gui[A-Za-z]+' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "new Gui TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -E 'new Gui[A-Za-z]+' "$PIN" -- $FILES | sed -E 's/.*new //' | sort | uniq -c | sort -rn | tr '\n' ';'; echo; git -C "$W" grep -n -A3 -F 'GuiMsgBox(' "$PIN" -- $FILES | sed "s/^$PIN://" > "$TMPDIR/dialogs.txt"; $G -c 'GuiMsgBox(' "$TMPDIR/dialogs.txt"
# the threads and the lifetimes (expect `std::thread lines TOTAL 9 in 6 files`; the sites `ContentInstaller.cpp:61 :247 ThreadedBluetooth.cpp:19 :46 :76 :110 ZaparooSupport.cpp:22 components/ScraperSearchComponent.cpp:206` -- 5 constructions, 3 `delete this`; detach `FolderMerge.h:64 ZaparooSupport.cpp:27`; postToUiThread `AppWindow.h:1 NetworkThread.cpp:5 SystemScreenSaver.cpp:1`)
git -C "$W" grep -c -F 'std::thread' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "std::thread lines TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -n -E 'new std::thread|std::thread\(|delete this' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -F '.detach(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -c -F 'postToUiThread(' "$PIN" -- $FILES | sed "s/^$PIN://" | tr '\n' ' '; echo
# the bounds (expect HttpReq lines `OfflineAchievementsText.h:1 ScraperCmdLine.cpp:1 Win32ApiSystem.cpp:3 ZaparooSupport.cpp:5`; the one option line `ZaparooSupport.cpp:38`)
git -C "$W" grep -c -F 'HttpReq' "$PIN" -- $FILES | sed "s/^$PIN://" | tr '\n' ' '; echo; git -C "$W" grep -n -E 'stallTimeout|\.timeout\s*=|connectTimeout' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the reads (expect `exists( lines TOTAL 83 in 11 files`; occurrences 86; uncached `CaptureRotation.cpp:113 :146 :161 :170`)
git -C "$W" grep -c -F 'Utils::FileSystem::exists(' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "exists( lines TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F 'Utils::FileSystem::exists(' "$PIN" -- $FILES | wc -l; git -C "$W" grep -n -E 'exists\([^)]*, *false\)' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the writes (expect exactly the ten lines: CaptureRotation.cpp:175 writeAllText; CollectionSystemManager.cpp:345 std::ofstream; CustomFeatures.cpp:151 save_file (dead text); FileFilterIndex.cpp:1313; Gamelist.cpp:308 :474 :622 :841; KeyboardMapping.cpp:426 :429; and Gamelist's removeFile :307 :353 :619 :827 :838, copyFile :620 :839)
git -C "$W" grep -n -E 'save_file\(|writeAllText\(|std::ofstream' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -E 'removeFile\(|copyFile\(' "$PIN" -- es-app/src/Gamelist.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo
# the process starts and the parses (expect `CloudOffer.cpp:37 Win32ApiSystem.cpp:314 :340 :1264 Win32ApiSystem.h:55 :56`; `gamelist.xml lines TOTAL 6 in 3 files`; the parse counts [unverified: the loop's own lines])
git -C "$W" grep -n -E '(^|[^A-Za-z_])(system|popen)\(|runSystemCommand\(|executeScript' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -c -F 'gamelist.xml' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "gamelist.xml lines TOTAL", s, "in", NR, "files"}'; for k in 'std::stoi(' 'std::stoul(' 'atoi(' 'toInteger(' 'atol(' 'strtol' 'strtoll'; do printf '%s ' "$k"; git -C "$W" grep -c -F "$k" "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "TOTAL", s+0, "in", NR, "files"}'; done
# the success-reads and the three FAIL-at-pin lines (expect `rootFolder->clear()` at CollectionSystemManager.cpp:1117, reloadGameListView( at :1589, reloadCollection at :1558; KeyboardMapping checkTriggerExists at :178 :265 :271; the screensaver retry `:157`; FileTag `_("` at 6 7 8 9 10 11; LangParser:65 the `ìndia` line; TextFit.h:34 the `> 4`)
git -C "$W" grep -n -E 'rootFolder->clear\(\)|reloadGameListView\(|::reloadCollection' "$PIN" -- es-app/src/CollectionSystemManager.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'checkTriggerExists' "$PIN" -- es-app/src/KeyboardMapping.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'while (retry > 0' "$PIN" -- es-app/src/SystemScreenSaver.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -F '_("' "$PIN" -- es-app/src/FileTag.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -P '[^\x00-\x7F]' "$PIN" -- es-app/src/LangParser.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -F 'text.size() > 4' "$PIN" -- es-app/src/TextFit.h | sed "s/^$PIN://" | cut -d: -f2
# the French (expect six msgid lines for the tag names at po 717 3576 3579 3582 3585 3588 and none for IN PROGRESS, DROPPED, ON HOLD; the catalog 2207 msgids, 42 empty msgstr; es-untranslated `706 fork string(s) in the source, 706 with French, 0 without` rc 0 against bccd715707 and `703 ... 703 with French, 0 without` rc 0 against cada856d86 -- T32's proved lines at the same pin)
git -C "$W" grep -n -E '^msgid "(IN PROGRESS|DROPPED|ON HOLD|FINISHED|SLOW|NOT WORKING|BUGGY|LIKED|DISLIKED)"$' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://" | cut -d: -f2,3 | tr '\n' ' '; echo; git -C "$W" grep -c -E '^msgid ' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://"; git -C "$W" grep -c -E '^msgstr ""$' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://"
out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated rc=$rc"
out=$(tools/es-untranslated --es-src "$W" --upstream "$MB" 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated(cada) rc=$rc"
# the non-ASCII comments (expect files with non-ascii comments: 0; adjacent 0 rc=1 -- the adjacency grep is -F, never a basic-regex `\(`)
n=0; for f in $T; do c=$(git -C "$W" show "$PIN:$f" | $G -c -P '^\s*//.*[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "$f:$c"; n=$((n+1)); }; done; echo "files with non-ascii comments: $n"; for f in $T; do git -C "$W" show "$PIN:$f" | $G -n -P -A1 '^\s*//.*[^\x00-\x7F]' | $G -F -B1 '_("'; done | $G -c .; rc=$?; echo "adjacent rc=$rc"
# the harness (expect 19 Tests.cpp under es-app/tests/unit; 15 .py under tests/; app-unit `AppWindow: 1 FolderMerge: 3 JourneyTiers: 8 RunLock: 3 TextFit: 3`; ScraperCmdLine one line, its own include)
git -C "$W" ls-tree -r --name-only "$PIN" -- es-app/tests/unit/ | $G -c 'Tests\.cpp$'; git -C "$W" ls-tree -r --name-only "$PIN" -- tests/ | $G -c '\.py$'; for t in AppWindow FolderMerge JourneyTiers RunLock TextFit; do printf '%s: ' "$t"; git -C "$W" show "$PIN:tests/app-unit/${t}Tests.cpp" | $G -c -E '^\s*TEST_CASE\('; done | tr '\n' ' '; echo; git -C "$W" grep -n ScraperCmdLine "$PIN" | sed "s/^$PIN://"
# the menu map (expect T32's line at the same pin and map, `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0 [unverified on this map's tip]; 0 hits for the two filter rows; the map at 989 lines)
out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"; $G -c -E 'FILTER GAMELIST BY|EDIT DYNAMIC COLLECTION FILTERS' docs/es-menu-map.md; rc=$?; echo "filter rows rc=$rc"; wc -l docs/es-menu-map.md
# the compile (expect `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2; plain g++ on MetaData.cpp: its first missing header [unverified: run it]; the stand-in check over classes (a)-(d) with T31's fakes copied under stage-a/fakes/ and RAPIDJSON_INCLUDE_DIR set, rc per file)
F=es-app/src/MetaData.cpp; out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc"
out=$(g++ -std=c++17 -fsyntax-only -DHAVE_INTL -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$F" 2>&1); rc=$?; printf '%s rc=%s\n' "$(printf '%s\n' "$out" | $G -m1 -E 'fatal error|error:' | cut -c1-90)" "$rc"
# STAGE C -- the include graph and the unit build: the lane's scripts, which do not exist at stage A (expect the include script's last lines: 272 include lines; es-core 119 edges over 40 headers; earlier slices 10 edges over 7 headers; and the build script's own `TOTAL: N test cases in B binaries` with 0 failed, the five app-unit files among the binaries, and before any fix the six FAIL-at-pin cases reported FAIL by name)
python3 -I docs/audits/*-epic-m6-es-app-system/tools/t33-includes.py "$W" "$PIN" .qa-scratch/t33/paths.txt | tail -n 4
bash docs/audits/*-epic-m6-es-app-system/tools/t33-build-tests.sh "$W" 2>&1 | tail -n 10
# STAGE A, after the pointer is read -- the removal check: TIPHASH is the lane's own tip the pointer and the dispatch comment name (MERGE_HASH at stage A); the literal word fails with `fatal: bad revision` (expect empty) and the ES diff against the pin (expect empty before stage E)
git diff --stat TIPHASH HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1
```

## 6. Outputs

As T26's, T31's and T32's briefs § 6; § 7 is this section as checkboxes,
so only the layout and `02`'s section order are given here. The folder
`docs/audits/<yyyy_mm_dd>-epic-m6-es-app-system/`: `00-running-log.md` to
`05-punch-list.md`; `second-opinions/` (`review-plan.json`, the probe's and
the refutation's `.provenance.json`, `packet-manifest.json`); `stage-a/`
to `stage-e/` (the first commands and the § 5 runs under `stage-a/`, with
T31's 13 fakes copied under `stage-a/fakes/`; the window plan under
`stage-b/`; the host proofs under `stage-c/`; the walks' steps under
`stage-e/walks/`); `tools/` (the generators -- `t33-includes.py`,
`t33-build-tests.sh`, the tables' generators -- each asserting its counts
and each seen to exit 1 on a constructed drift before it is trusted);
`guest-cycle/`; the lint before D; the audit issue (`Audit: M6 T33
EmulationStation's system layer -- N findings (...)`, a sub-issue of #680;
the audit issue and the bugs are the lane's, D-WORKFLOW-189; **a Backlog
for a lead outside the 77 is the coordinator's**, named in the hand-back);
and the retro at `docs/retros/<date>-m6-es-app-system.md` (**what the slice
did to the two time-to-play numbers**: the exit path's three callees
(`recordAfterSession`, `updateCollectionSystem`, `saveToGamelistRecovery`)
inside T2's 1.01 s, the SCREENSHOTS press after a rescan over
`buildStems`, and UPDATE GAMELISTS' parse-and-save, named with what they
cost on the guest and cited from `docs/vm-qa-log.md`; never "nothing" by
default; **what T34 to T37 inherit**: § 5 item 3).
**`02-forward-audit.md` carries these sections, in this order, each
generated section's row count stated as "generated, asserted" by the
script that made it:** § Coverage (77, one row per path, the path in
backticks as the first cell, both tiers: fork-added 27 / fork-modified 4 /
upstream-carried 46 and inventory 31 / 46), § The leads (L-01 to L-29 and
3.1 to 3.41 from § 4's table, each with its lines, its family, who owns
it, its disposition), § The library (one row per unit of the game lists,
collections, metadata and filters: what reads it, what writes it, on
which thread, what the first frame waits for), § The helpers (one row per
fork unit: its page or caller in the other slice, its case file and
whether it was built, its French), § The writes (every file the 77 write,
the ten sites, in place or temp-and-rename, with `Already written:` per
site), § The reads (one row per `Utils::FileSystem::exists(` line, 83:
the file, its writer while ES runs, cached or not, what a miss reads as),
§ The bounds (every network or script wait reachable from the 77, with
its bound), § The words (the 176 lines, the 196 msgids, L-25's three,
L-26, the dialog words, L-10's toasts), § The structure (the three CMake
conditionals, the 30 in `ES_SOURCES` and the one absent, the seven headers
unlisted, the Windows residue, the macros' real home in one sentence),
§ The merge debt (one line, both bases, batocera's six as context), § The
runs, § The guest cycle, § The streams (stage E: **written by the
coordinator after stage D, as for T21, T26 and T32**; the lane leaves the
heading and the pause's dispositions), § Positives, § The #585 lines owed
(one per upstream-carried defect closed under rule 6, in the shape the
lane writes, never sent; the three shared-file patches and the three
helper-file fixes of § 4's Q7 named as candidates for the coordinator),
§ What T34 to T37 inherit; every proof with `proved:`. The stage-D pause
as T21's: the punch list posted on #680, the lane waits for the
coordinator's dispositions and any stream brief.

## 7. Acceptance

The checklist on #680 becomes this section at dispatch, written there by
the coordinator in place of P1's generated ones. Every checkbox names the
artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-app-system/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `second-opinions/`, `stage-a/` to `stage-e/`, `tools/` and `guest-cycle/` (`ls` of the folder in the hand-back).
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-app-system/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), and the same with `--issue <audit issue>` prints `PASS`; Q1 to Q7 are answered in `04-analysis.md` and every punch item carries `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); its probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the scan block with every hit dispositioned by file:line (library plumbing / macro name / identifier / setting name) and no value, every trimmed file and range named, `Win32ApiSystem.cpp` by its three hunks only, `EmulationStation.aps` and `es_icon.ico` absent; `00` shows exactly two keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #585, #649, #665, #667, #668, #673, #678, #679, #771, #781, #1186, #1235, #1170, #301, #609, #1194, #560, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail; the issue is closed by the coordinator at acceptance.
- [ ] `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in #680's header carry the lane's commits; the ES read is on the pin's bytes for the 77 files (`git -C <W> diff --stat 16dbac5211 <reviewed-at-es> -- $(cat .qa-scratch/t33/paths.txt)` empty before stage E) and nothing under the distribution's `packages/`, `projects/` or `tools/` changed at any stage against the lane's own dispatch tip (the pointer's merge hash, never `2174265e9c`).
- [ ] `01-research-notes.md` § Scope records § 2's block with its exact output lines (`mine: 77 paths.txt: 77 equal: True`; `lines: 16276 reach: {'shipped': 77} tier: {'fork-own': 31, 'upstream-carried': 46} lang: {'cmake': 1, 'other': 4, 'c-header': 41, 'c++': 31}`; `fork-own lines: 4522`; `read lines: 16210`; `wc -l text 16272` and `grep -c text 16276` with the four files without a trailing newline; 50 at the merge base and 50 at the base; `31 files changed, 2689 insertions(+), 7 deletions(-)` three times -- or the deltas beside them) and names `cada856d86` as the merge base against `rocknix/master` with `bccd715707` as its parent.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `77`; its tier columns read fork-added 27 / fork-modified 4 / upstream-carried 46 and inventory 31 / 46.
- [ ] `02` § The runs records the counts with both rules where they differ -- `_("` 176 lines in 11 files and 223 occurrences; `Utils::FileSystem::exists(` 83 lines in 11 files, 86 occurrences, 4 uncached all in `CaptureRotation.cpp`; `new Gui` 10 in 3 files with 7 `GuiMsgBox`; `std::thread` 9 lines in 6 files, 5 constructions in 4 `.cpp`, 3 `delete this`; `postToUiThread(` 7 lines in 3 files; `gamelist.xml` 6 lines in 3 files; the ten write sites; the one process start; include edges 272 with es-core 119 over 40 headers and the earlier slices 10 over 7 -- each as a command's own output line, or the lane's figure with the command that differs named.
- [ ] `02` § The library, § The helpers, § The writes, § The reads and § The bounds are each generated or asserted by a script under the audit folder's `tools/` that names its row count ("generated, asserted"), and `02` § The runs records each script seen to exit 1 on a constructed drift before it was trusted.
- [ ] `02` § The reads has one row per `Utils::FileSystem::exists(` line (83): the file or line read, its writer while ES runs, cached or not, and what a remembered miss reads as; `Gamelist.cpp:413`, `SystemScreenSaver.cpp:157` and `:164`, and `CaptureRotation.cpp:51` among them with a disposition each.
- [ ] `02` § The writes has one row per write site (the ten: `Gamelist.cpp:308`, `:474`, `:622`, `:841`, `FileFilterIndex.cpp:1313`, `CollectionSystemManager.cpp:345`, `KeyboardMapping.cpp:426`, `:429`, `CaptureRotation.cpp:175`, `CustomFeatures.cpp:151` as dead text), each with in place or temp-and-rename, its last-good copy if any, its `Already written:` line, and its disposition (a stream, Backlog #1186, or left with the reason).
- [ ] `02` § The merge debt is one line naming `cada856d86` as the merge base with `rocknix/master` (`f6c542872e`), `bccd715707` as its parent and the stale `upstream/master`, the 0 upstream commits on the 77 of 14 since the base, the fork's four modified files with their numstat pairs, and batocera's six commits since `1750dded8c` as context only; the T21 deltas (`es-app/CMakeLists.txt` +10/-0, `WifiText.cpp` +11/-0, `WifiText.h` +13/-0) and T20's (`OfflineAchievementsText.cpp` +99/-0, `.h` +52/-0) recorded as inherited with their commits.
- [ ] `02` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason; the menu-map check's line, both `es-untranslated` lines, the catalog grep for the nine tag names, the non-ASCII grep's 0 (adjacency by `-F`), the stand-in syntax check's rc per file over classes (a) to (d) and the unit build's `TOTAL: N test cases in B binaries` line with 0 failed are among them; every unit case the lane wrote has its FAIL-then-PASS pair recorded against the unfixed extract first, the six FAIL-at-pin leads by name; the five `app-unit` case files are built and their cases counted in the `TOTAL:` line.
- [ ] `02` § The guest cycle records the window the coordinator granted on #680 (the comment's time; the START and RETURN posts with their first-line contract and censuses, and the host file's lines beside them), the image by file name and `BUILD_ID` read from the guest at 640x480, G-01 to G-10 with their frames read back at EN and FR and each frame labelled by side (`image` or `pin-binary`), G-02's collection and its toggle with the file read back and the journal read for a backtrace, G-03's three stubs and the index toast and the SCREENSHOTS press-to-frame number, G-04's `gamelist.xml` shape and the stale-read result read both ways, G-06's dimmed and black frames, G-08's editor frame and file and the dropped trigger, G-05, G-07 and G-09 as `CANNOT` with the reason, the disk retired with path, size and sha, the leftover check (`qemu 0, compilers 0`), and the window closed inside its bound plus grace.
- [ ] `00-running-log.md` shows no image build, no fetch (the council runtime from `npm install --offline`; `rocknix/master`, `batocera/master` and the lanes' ES tips read from the shared refs), no handheld, the owner's accounts never named or used, no hosted account, no M7 root, worktree or prep directory, the guest only inside the granted window, two keyed invokes and every other council call keyless, and nothing written under the ES worktree before stage E (`00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q7 are answered at their lines; every `bug` states its trace, its `Already written:` line and its VM line in one of the named families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` in the shape the lane writes; the items § 2 lists under *do not re-find; take up* (T2 FD-9/FD-19 routed out, FD-15, SD-1, PC-1, the exit path, `SystemScreenSaver.cpp:546`; T31 PL-26 and T32 L-14/L-16; T21 PL-20/#1186, PL-15, PL-16/#1194; T31 PL-25/#1235; T20 #1170/#301, #1175, #1173/#1174, `GameCubeRvzHashRetry` vs #609, S9; T18's seven test files and the unbuilt `app-unit`; T26's `JourneyTiers` positive; #560; the map's three declarations) each have a disposition at their lines, and every collision with T21's and T20's lines is named.
- [ ] Every proof in `02` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; `02` § What T34 to T37 inherit lists § 5 item 3's eight items with their lines.
- [ ] The retro exists at `docs/retros/<date>-m6-es-app-system.md`, is posted on #680 with its heading's time from `date -u` in the posting command, says what the slice did to the two time-to-play numbers (the exit path's three callees, the SCREENSHOTS press over `buildStems` and UPDATE GAMELISTS named with what they cost on the guest; cited from `docs/vm-qa-log.md`), and what T34 to T37 inherit.
- [ ] `tools/es-menu-map-check --es-src <W> --ref <reviewed-at-es>` prints `0 missing` on the branch as handed back **after `docs/es-menu-map.md` takes rows for FILTER GAMELIST BY and EDIT DYNAMIC COLLECTION FILTERS** (in the same commit as any row a stream touched, D-UI-039; the checker printed `0 missing` on T32's run at the same pin, which says it does not see them -- the lane records which titles the check reads and why these two passed it), and UPDATE GAMELISTS has its disposition in the map, in `## Not mapped` with a reason, or in a punch item saying which.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch and the ES fork's `.githooks/pre-push-test` on the ES branch before the hand-back merge, and again on the coordinator's simulated merge; every fix on the ES branch has, recorded beside its commit, the covering unit case's PASS line (and its earlier FAIL), its French in the same commit where a sentence changed (L-25's three `msgid` entries included), `tools/es-syntax-check` PASS where a toolchain exists or else the stand-in `g++ -fsyntax-only` rc (or `CANNOT` with the missing header named), and a clean non-ASCII grep over its added lines.
- [ ] The unit build's `TOTAL: N test cases in B binaries` line is quoted in `02` § The runs and in the hand-back from the script's own output, with 0 failed in every binary's summary after the fixes, `app-unit-tests` among the binaries, and the six FAIL-at-pin leads' earlier FAIL lines beside it.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back); the stage-D pause; an explicit maintainer
pause on #680; a blocker named on #680 (the seat failing its provenance
gate twice, a packet scan hit that is a value, two commands that disagree,
a block whose output differs from § 2's beyond the deltas it records, an
upstream-carried file that is not byte-identical to `rocknix/master`, a
pointer line that names the predecessor slice (§ 10); **not** the host's
missing toolchain, which § 5 names and the `CANNOT` forms absorb, **not**
the five `app-unit` case files failing to build on the first try, which §
5 says the lane's script is extended to, and **not** the no-NIC guest's
inability to show the installer, the network thread's checks or the
write's atomicity, which § 5 names as the floor's limit); an ES worktree
that differs from the pin on any of the 77 files at stage A; or an
execution limit, stated as such with the running log current. A
checkpoint is not a stop. An idle session says it is idle on #680, **and
does not end a turn on a post that asks nothing**: a turn ends on a post
or a commit, never on "next is ..." (the T26 lane sat 28 minutes on
exactly that, friction 2026-10-27 10:48 UTC).

## 9. Ceremonies owed

- A work-log entry per session headed `#680`, **its time from `date -u` in
  the same command** (a heading's time typed by hand was this week's
  erratum), prose through a quoted heredoc; `tools/work-log-index --write`
  after it.
- A friction line the moment something slows, with `issue: #680` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window granted on #680; no account needed; nothing on a
  handheld; D-QA-015/016).
- The mini-retro at stage G, posted on #680, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (three
  expected, all put to the coordinator at the pause, never decided by the
  lane: whether the three `writeAllText` sites move onto the atomic writer
  in this slice's stream or under Backlog #1186; whether
  `GameCubeRvzHashRetry`'s every-run retry stands *by design* against
  #609's bound; and whether a `gamelist.xml` the cloud brings after
  startup is read uncached at `Gamelist.cpp:413` and `:116`, Q4's L-05).
  **The highest IDs the register on the coordinator's branch names at this
  version are D-CLOUD-186 (`:755`), D-UI-128 (`:756`) and D-UI-129
  (`:757`), after D-WORKFLOW-212 (`:753`) and D-NET-017 (`:754`)** (the
  last five decided rows; `tools/register-check` is the proof;
  D-WORKFLOW-188 is on the P1 branch only and the merge unites them); a
  row this slice forces takes an ID the coordinator assigns on #680.
- `tools/ceremony-check --gate` before every push of the distribution
  branch and the ES fork's `.githooks/pre-push-test` after an ES change;
  never `--no-verify`; a merge with conflicts is checked for markers; the
  ledgers united by whole entries; **a commit names its paths**; anything
  temporary under `/workspace/tmp/m6-t33/` after `df -i`, never `/tmp`;
  the window's record kept on the branch, the guest disk retired after it
  with the retirement recorded in `00` (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never
  inside a `bash -c` script**.
- **The same-commit rules, stated once:** a row added, moved or renamed
  updates `docs/es-menu-map.md` in the same commit and
  `tools/es-menu-map-check` passes before it (D-UI-039); a sentence added
  or changed carries its French in the same commit (D-UI-051).
- **Every count is a tool's line** (`engineering-practices.md:250`): a
  figure in `02`, a post or the hand-back is the command's own output,
  quoted; a sum, a difference or a rate is computed by the command that
  prints it (T21's twelve stream totals were composed by hand and every
  one was wrong, #668).
- A fixture that rewrites no path, in a bubblewrap sandbox started with
  `--clearenv`; the walks' steps under the audit folder's `stage-e/walks/`,
  never under `tools/`; the non-ASCII grep over a stream's added lines
  (`git diff -U0 HEAD -- <file>`, its `+` lines), an upstream hit recorded
  and not fixed; a generator seen to exit 1 on a constructed drift before
  its table is trusted; **every grep for `_("` by `-F`**, never the
  basic-regex `\(` (T31's stage-A erratum).
- **Every edited file checked for an unfilled placeholder before its
  commit**: `/usr/bin/grep -c -E '__[A-Z]+__|\b(COHASH|MERGE_HASH|TIPHASH|V2HASH)\b'`
  is 0 on the pointer, the running log and every artifact (the T31
  dispatch entry shipped with its `__TS__`/`__URL__` placeholders
  unfilled, friction 2026-10-27 12:02 UTC; this brief's own four names,
  § 1, would pass the first alternation unseen, so the pattern names
  them).
- Commit messages `docs: ...` on the distribution branch, with `Refs #680`;
  on the ES branch the package's convention, `Refs #680, #<bug>`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#680's checkboxes against their artifacts; the lint's `PASS` line on the
default phase and with `--issue`; `review-plan.json` and the two
provenance files (read directly) and the manifest's scan block; the audit
issue's checkboxes all at an outcome; the coverage table's row count (77),
the generated sections' asserted counts, § The reads' 83 rows, § The
writes' ten, § The merge debt's one line; every Q bug with its three
lines; **re-running on clones of both branches at their tips under
`/workspace/tmp/m6-coordinator/`: the membership block, every § 5 run in
full and the unit build script** (no guest: the window's record is read,
not repeated); `register-check` on a simulated merge with the
coordinator's tip; the retro's answers; the five checkers' exit codes; the
collisions named against T21's `es-app/CMakeLists.txt` and `WifiText`
lines and T20's `OfflineAchievementsText` lines. The lane posts one
hand-back comment naming **both tips** and each artifact by path, writes
`reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` into
#680's body, then says it is idle. After acceptance the coordinator closes
the audit issue, prompts the lane for `audit-completion.json` and the lint
against **the audit issue**, merges the distribution branch in its turn
after the M7 candidate with the pin moved to the ES branch's tip in the
same integration commit (the ES package built before it lands; T21's and
T20's deltas reconciled there), regenerates the ledgers, posts any #585
lines in the shape the lane wrote, files any Backlog the hand-back names,
and closes #680 when every row is proven -- which is also when #649,
#665, #667, #668, #673 and #678 close (§ 1); the interface epic #700
closes when its slices have.

**The pointer the lane checks at stage A, line by line.** The seeded
pointer `.github/sessions/saved-session-state-feature-m6-es-app-system-680.md`
is written by the coordinator from T32's, and T32's was seeded from T31's,
which carried a sentence of T26's. So before the first command after `cat`
the lane reads these eleven keys, each against the one value that would be
the seeding error, and reports any that name the predecessor on #680
before going on:

| Key | Must read | The seeding error reads |
| --- | --- | --- |
| `Branch (distribution):` | `feature/m6-es-app-system-680` stacked on `feature/m6-p1-survey-641` at the P1 tip the dispatch comment names | `...-es-app-views-scrapers-679` |
| `Worktree (distribution):` | the § 1 path ending `m6-es-app-system-680` | `m6-es-app-views-scrapers-679` |
| `Worktree (EmulationStation):` | `W` of § 1, at the pin `16dbac5211` | another lane's checkout |
| `Executor:` | Opus 5.5 at high effort, the session the dispatch comment on #680 names | T32's session |
| `Epic:` | #700; T2, T18, T20, T21, T26, T31 accepted and open until the integration merge; T32 in flight; T34 to T37 and T44 after | "T32 accepted" or "closed" |
| `Depth:` | one seat, GPT-6 Astra at `max`; the 27 fork-added files whole, the 4 modified by their hunks, the 46 upstream-carried by cited ranges; the two binaries never | six fork-modified files, 42 paths, `httplib.h` |
| `The lens:` | cost against value over 77 paths, the rest of `es-app/**` | the views, the scrapers, the services |
| `The rule:` | nothing under the distribution's `packages/`, `projects/` or `tools/`; nothing in the ES worktree at stages A to D | -- |
| `The host:` | the shared log and one guest window of 25 + 5 minutes | a 35-minute window |
| `Register:` | D-CLOUD-186, D-UI-128, D-UI-129 (after D-WORKFLOW-212, D-NET-017) | D-WORKFLOW-212, D-NET-017, D-CLOUD-186 alone, or an older triple |
| `The brief:` | `docs/reviews/briefs/es-app-system.md` at `V2HASH` (§ 1: filled by the dispatch comment) | `es-app-views-scrapers.md`, or the literal word `V2HASH` |

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro takes a T33 kickoff addendum written by the coordinator with
version 2, and the stranger's proof of this version has run; its findings
become the last section of version 2. This brief's hash at dispatch is
`V2HASH`.

**What never runs in this slice:** an image build, a compiler beyond the
host's `g++ -fsyntax-only` (plain or with T31's stand-ins) and the
generated test build, a fetch (the council runtime from `npm install
--offline`; `rocknix/master`, `batocera/master` and the lanes' ES tips
from the shared refs), a handheld, the owner's accounts or any hosted
account, a host listener on a privileged port, a guest before a grant on
#680, M7's roots, worktrees or prep directories, a change outside the 77
files, `docs/es-menu-map.md`, the French catalog and the audit folder
except under a stream brief, a move of the pin, a deletion of
`ScraperCmdLine.*` or the Windows residue, a line in `ApiSystem.*`,
`FileData.*`, `SystemData.*`, `CloudText.*`, `Scripting.cpp`, `guis/`,
`views/` or `WatchersManager.*` without the pause's ruling on its owner.

## Version 1: what the drafting read did not settle

Written from the five digests and ten `git -C` reads of the pin on
2026-10-27; a stranger's proof runs the membership block, the § 1 commands
and the § 5 runs, and version 2 applies what it corrects. What this
version leaves for the proof, each marked where it stands:

1. **The three `[unverified]` items in § 5's runs**: the parse-count loop's
   own lines (`std::stoi(`, `std::stoul(`, `atoi(`, `toInteger(`, `atol(`,
   `strtol`, `strtoll` over the 77); `tools/es-menu-map-check`'s line on
   the coordinator's map today (T32's `55 screen(s) ... 0 missing` was
   proved on the same pin and map on 2026-10-27, so it is expected to
   hold); and plain `g++ -fsyntax-only`'s first error on `MetaData.cpp`
   (class (b): the floor says no SDL, curl or vlc header on its graph, so
   the expectation is a pugixml or es-core include, not `curl/curl.h` as
   T32 measured on `ThreadedScraper.cpp`).
2. **The membership block's two-pass recipe** (`/dev/null` first, then the
   paths file the TSV yields) was composed here, not run: the digest ran
   the script once against its own list. The proof runs both passes and
   records the first pass's `only-mine` line.
3. **`tools/es-untranslated`'s two lines** are T32's proved lines at the
   same pin and catalog, not this slice's run; and whether the tool reports
   an upstream string without French (L-25's three) is unknown -- the
   catalog grep is the check this brief relies on.
4. **The include-graph figures** (272 include lines; es-core 119 edges over
   40 headers; earlier slices 10 edges over 7 headers; the per-header
   outside-includer counts of the membership digest's § 7) are the
   digests' Python passes over `git grep` output, quoted-form includes
   only (`GuiMenu.cpp:60` includes `<LibretroRatio.h>` in angle brackets
   and was missed); the lane's `t33-includes.py` is the first tool line.
5. **The floor's "33 pure leads"** is the floor's author's count; § 4's
   table carries 41 rows after dropping the rows with no case shape, and
   the brief does not claim the 33.
6. **Line offsets written `+N`** in § 4's table (`MetaData.cpp:280`'s
   `+153`, `Gamelist.cpp:112`'s `+79-83`, `FileFilterIndex.cpp:1107`'s
   `+99-161`, and the like) are the floor's relative lines from the
   function's first line; the lane reads them to absolute lines before
   citing them in `02`.
7. **`CollectionSystemManager.cpp:540`'s `.at()`** (T2 FD-15) was not
   re-read by the drafter; the line is T2's citation.
8. **T32's `02` § What T33 to T37 inherit** had not landed at drafting
   (T32's guest window started 16:08:36 UTC); its items are named from
   T32's brief, not from the audit.
9. **The P1 tip**: `origin/feature/m6-p1-survey-641` is not a ref in the
   coordinator worktree (`git rev-parse` fails there); `2174265e9c` is the
   P1 research clone's HEAD and T32's stacking base. If #1235's
   regeneration moves the P1 branch before dispatch, the dispatch comment
   names the new tip and the block's expected lines are re-run against it.
10. **The guest plan's G-02 removal step** (removing a game from inside the
    collection to provoke L-06) assumes the bundle view is what the
    collection opens in at the image's settings; the lane reads
    `reloadCollection`'s callers on the image's binary (G-01's digest) and
    labels the frame `image`.
11. **Whether `app-unit-tests` builds with T31's script's flags** (its
    `fakes/` include root first, `main.cpp` providing doctest's main) is
    the lane's first stage-C result, not a figure here; a failure there is
    not a stop (§ 8).
