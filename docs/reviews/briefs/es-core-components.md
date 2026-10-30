# Review brief: M6.P2 T34, EmulationStation's core components: the rows, grids, menus, lists, cards, images, videos and text every page is built from (#681)

**Version 2, 2026-10-30, after a stranger's proof of version 1 (`a728d04c95`); the
corrections are the last section.** (D-WORKFLOW-189;
`docs/reviews/plan-for-the-plan.md` § 6b, § 6c, § 7.) Version 1 was drafted
from five read-only digests (membership, fork changes, upstream delta,
inherit, floor) that are in no tree, so every figure here is reproduced by a
command at the hash it names, with `/usr/bin/grep` and never the shell's
function (#1138: on this host `grep` is a function and prints nothing for
the one slice file holding a non-UTF-8 byte); the proof ran every block
below at the pin by `git -C` and at `2174265e9c` by `git show`, and carries
no `[unverified]` bracket. The structure is T33's brief (`es-app-system.md`,
version 2 at `c48f8b387e`; the same blob through `b0c7e3f059` and
`a8fe371b0a`); every T33-specific paragraph is replaced. The rule, register,
menu-map and blindspot line numbers are the coordinator worktree's at
`a8fe371b0a`, unchanged through `a728d04c95`: the one change since T33's
`ce8608e38f` is `es-ui-style-guide.md:202`, the Waiting table's card row
(`git diff --stat ce8608e38f a8fe371b0a -- .claude/rules
docs/decision-register.md docs/es-menu-map.md docs/blindspot-register.md`
prints that one file, `1 insertion(+), 1 deletion(-)`).

## 1. Identity

- **Issue:** #681 `M6.P2 E339/T34: interface: EmulationStation's core
  components` (the live title, read 2026-10-27 after 19:04 UTC, OPEN,
  milestone `M6: Codebase renovation`, no labels, 0 comments), **retitled at
  dispatch to `M6.P2 E700/T34: interface: EmulationStation's core
  components`** (`milestone-phase-naming.md`; the body says *"under epic
  #339 until this area's epic is filed"*, and #700 is filed; #678, #679 and
  #680 were retitled the same way). Slice `es-core-components` (`k: 34`) in
  `docs/reviews/slices.json`, thirty-fourth in `docs/reviews/order.md`
  (`order.md`, `slices.json` and `inventory.json` are the P1 branch's, which
  the lane's worktree is stacked on; they are not on `next` and not in the
  coordinator worktree; the drafter read them in the P1 research clone
  `/workspace/tmp/m6-coordinator/t11-research/tree` at
  `2174265e9cc1b248c0fbe27fa101875984d46d6b`, `git status --porcelain`
  empty; its § T34 at `order.md:623-631`: 80 paths, 21,984 lines, 21,984 read,
  9,541 fork-own, 0 patch and config lines, reach shipped 80; its `why`
  *"`es-core/src/components` (21,984 lines, 9,541 fork-own): the rows,
  grids, menus and cards every page is built from"*; **kind currency; lens
  cost against value**; read before none; depth Independent, *"an ordinary
  code slice"*; interacting subsystems *"every page; `es-code-traps.md`"*;
  closing evidence *"audit folder, lint PASS, punch list through Phase
  7"*). The selector is one object with one positive glob and no negative
  one, `{"globs": ["es:es-core/src/components/**"]}` (not a list; the
  block wraps it), area `interface`, no `rest`. (The
  `| T34 | T13 | cloud-harness |` row at `order.md:179` is the old-to-new
  numbering table, not this slice.) **Epic:** #700 `M6.P2 E339: Area epic:
  the interface, EmulationStation (T2, T18, T20, T21, T26, T31 to T37,
  T44)`: T2 #649, T18 #665, T20 #667, T21 #668, T26 #673, T31 #678 and T32
  #679 are **accepted, and their issues stay open** until the integration
  moves the pin on `next` (§ 10); T32 was accepted 2026-10-27 (its errata are
  the futro's `:954` and `es-app-views-scrapers.md` § Errata at
  acceptance); T33 #680 is in flight (dispatched 2026-10-27; its distribution branch at
  `0ee735862d6a` and its ES branch at `dd86d7ce20a5` on 2026-10-30, the
  proof's read); this slice; T35 #682, T36 #683, T37 #684 and T44 after. The futro
  `docs/futros/2026-10-23-m6-interface.md` (956 lines) takes a T34 kickoff
  addendum written by the coordinator with this version, after the T33
  kickoff addendum at `:936`, the T33 proof errata at `:950` and the T32
  acceptance errata at `:954`. **Milestone:** M6. **Predecessors:** T2, T18,
  T20, T21, T26, T31, T32 and T33 each routed items here by name or named a
  component file as context; every one is listed with its lines and its
  disposition in § 2 under *Already found; do not re-find; take up*, which
  points back at the rulings below. **Beside it:** T33's
  lane; the host shared through `/workspace/tmp/m7-m6-host-coordination.txt`
  (the durable successor of `/tmp/m7-m6-host-coordination-20261023.txt`,
  which the reboot of 2026-10-28 removed); a window for this slice is asked
  for on #681 and granted there and in that file's queue (§ 5 item 2).
- **The order's sentence is true of the membership, and this brief says
  what the title does not.** The glob and the title agree: the 80 are
  exactly `es-core/src/components/**`, 38 `.cpp` and 42 `.h`, every one
  byte-identical to `rocknix/master` or changed by the fork, none added by
  the fork. What the title leaves open is the rest of es-core, which four
  earlier briefs assigned by a reading rather than by the order
  (`es-pages.md:415-418` *"the es-core components (`GuiMsgBox`,
  `GuiTextEditPopup*`, `ComponentTab`, `MenuComponent`, `BusyComponent`,
  `TextComponent`) are **T35's** by the inherit digest's reading"*;
  `es-app-views-scrapers.md:432-434`; `es-app-system.md:627` *"the es-core
  components **T35's** by the earlier briefs' reading"*;
  `es-launch-path.md:382-383` and `:799`), and the futro's known unknown at
  `:846-848` left for the coordinator (*"which es-core owner rules on a
  popup or `GuiMsgBox` change (the inherit digest reads T35; the coordinator
  confirms)"*). **The ruling, by the selectors in `slices.json` at
  `2174265e9c`, is in the next bullet.** The "9,541 fork-own" of the order
  is the size of the 21 upstream files the fork modified, not the lines the
  fork wrote: the fork's own authorship over the 80 is **+591/-114 over 33
  commits by one author**, 20 of which the fork-changes digest reads as
  fixes (its count, not a tool's line); fork-added 0. § 2 carries the
  figures.
- **Ownership rulings, stated once; § 2's take-up list points here.**
  **T34 owns `es-core/src/components/**`, the 80 paths, and nothing else.**
  The selectors (`slices.json`, read at `2174265e9c`; the block in § 2
  prints the claimants under `CLAIMS`): T35 #682 `es-core-window-input` is
  `es:es-core/**` with `rest: true`, so **`es-core/src/guis/` (`GuiMsgBox`,
  `GuiTextEditPopup`, `GuiTextEditPopupKeyboard`, `GuiInfoPopup`),
  `Window.cpp`, `ThemeData.cpp`, `GuiComponent.cpp`, `InputConfig.cpp`,
  `InputManager`, `watchers/WatchersManager.cpp`, `Scripting.cpp` and
  `es-core/CMakeLists.txt` are T35's**; T36 #683 `es-core-utils-resources`
  is `es:es-core/src/{utils,resources,renderers}/**` less
  `utils/AtomicFileUtil.*`, so **`resources/TextureData.cpp`,
  `resources/TextureResource.cpp`, `resources/Font.cpp`,
  `utils/FileSystemUtil.cpp` and `utils/OfflineProxyUrl.cpp` are T36's**;
  T21 #668 holds `es:es-core/src/{Settings,SystemConf,HttpReq}.*` and
  `utils/AtomicFileUtil.*` by non-rest globs (`HttpReq.cpp`, `Settings.cpp`,
  `AtomicFileUtil.cpp` print `('es-state-and-bridge', 21)`); `CloudText.*`
  is T18's (#665) and `es-app/src/components/ScraperSearchComponent.cpp` is
  T33's (#680, `rest`). So the earlier briefs' "T35's" was right for the
  popups and the window and wrong for the texture cache and the font, and
  the lane writes no line outside the 80 (a fix in a neighbour is named for
  its owner at the pause). The routed items, ruled: (a) **T32 PL-07 /
  #1263's picture miss**: `resources/TextureData.cpp:331`, `:339`, `:410`
  are T36's by the glob; **the caller's half is T34's**: `ImageComponent.cpp:408`
  asks `TextureResource::get` by path, and what the component asks, what it
  does with a texture that is live under that key (T26 #1221's shape) and
  whether it ever re-asks is this slice's Q5. (b) **T2 PC-1**: detached
  workers hold a raw `AsyncNotificationComponent*` and call `close()` after
  `window.deinit()`; **the component's half is T34's Q4** (what a card
  promises a holder after the window lets go, and whether the component
  can refuse a late call); `Window`'s teardown is T35's; `delete this` at
  `ThreadedCloudSync.cpp:757` is T18's. (c) **T26 PL-27**: self-capturing
  `SwitchComponent`/`OptionListComponent` callbacks (withdrawn on T26 under
  D-WORKFLOW-209, *"the leak's shape noted for the es-core slice"*); **the
  component's callback type (weak by design or not) is T34's Q4**; the
  pages' `onFinalize` clearing is T26's and T31's. (d) **T31 L-03 / #1243's
  invariant** at `OptionListComponent.h:310-311` and `:323-324` (a `delete
  this` inside the option list's own callback is safe only because the
  component touches nothing after the callback returns): **T34's to state
  in `02` and to keep**; the pages' save-first fix is T31's `82f80693d`.
  (e) **#1266's grid-after-`clear()` contract** (`ImageGridComponent.h`;
  #207's `clear()`/`resetGrid()`; the view's fix is T32's `1655e2f4c`):
  **T34's Q4**, with T32's `s4-views.py` as the harness shape. (f) **#48's
  `TextComponent` padded-height root** (`TextComponent.cpp:338` measures at
  `getSize().x()`, `:350` draws at `mSize.x() - padding`; unchanged at the
  pin; M7 patched the page side only; an investigation candidate on #585):
  **T34's Q1 to read, reproduce and record with frames**; whether the root
  is fixed in the component, which re-heights every padded auto-height text
  in the app, is a stage-D ruling, never the lane's. (g) **batocera's
  `HelpComponent::setOpacity` null guard** (`9dbd4b9bf`, absent at the pin
  and at `rocknix/master`): its reachability on the fork's images is T34's
  Q7 under D-WORKFLOW-162. (h) **`UntintedImageComponent`**
  (`es-native-ui.md:318`) is not under `components/` at the pin (the
  inherit digest's grep was empty; it lives in es-app): whether the untinted
  mode is lifted into `ImageComponent` is a Q7 question for the pause, not a
  change the lane makes. (i) **`ComponentList.cpp:568`'s `_("up/down")`**
  is inside the 80, upstream's, and the one icon key in the tree that goes
  through `_()`: a contained fix under rule 6 (Q3, Q6). (j) **The two
  lanes' unit-test doubles of `AsyncNotificationComponent.h`**
  (`tests/app-unit/fakes/components/AsyncNotificationComponent.h`, T18's,
  24 lines; T33's build names the same fake): a header change in T34 is
  named as a collision in the hand-back; the fakes are not the lane's to
  edit.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of scope:
  those are the coordinator's, reached through #681, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already written:`
  line (D-WORKFLOW-187). A fix lands only under a stream brief the
  coordinator writes at the stage-D pause, **on the EmulationStation
  branch**. The read's tiers are **fork-added 0 / fork-modified 21 /
  upstream-carried 59** (§ 2 § Three things the figures hide, (2), which
  reconciles them with the inventory's `fork-own` 21 / 9,541 lines). A
  defect in a line the fork wrote is the fork's to fix; a defect in an
  upstream line is a contained fix under `bugs-are-agent-first.md` rule 6
  (`:76`) and a #585 line (D-WORKFLOW-164, never sent, D-WORKFLOW-165).
  D-UI-079's lanes (`engineering-practices.md:12`): the progress card, the
  menu and its button bar, the tab strip, the rows (`ComponentList`,
  `MultiLineMenuEntry`, `SwitchComponent`), the help bar, the grid and its
  tile, the image's aspect and turn and the web image are the surfaces the
  fork's 33 commits work in and are the lanes; **the video components, the
  carousel, the rating, the date editor, the text list, the scrollable
  container, the stack panel, the post-process shader, the battery,
  network, clock and volume glyphs and the controller strip are upstream
  surfaces** read for brittleness and cost (the lens) and left as upstream
  has them, and a defect in one is still ours to close when the fix is
  contained (rule 6). The read is the pin `16dbac5211`'s bytes; M7's
  worktrees are never read.
- **Two worktrees, one session, and four placeholders.** The distribution's
  `feature/m6-es-core-components-681` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-components-681`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** (`origin/feature/m6-p1-survey-641` resolves to
  `2174265e9cc1b248c0fbe27fa101875984d46d6b` in the coordinator worktree,
  read 2026-10-27 after 19:04 UTC; or the P1 tip the dispatch comment
  names) with the coordinator's tip merged in and the lane's pointer seeded;
  and the EmulationStation fork's `feature/m6-es-core-components-681` at
  `W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-components-681`,
  cut by the coordinator from **the pin
  `16dbac5211eea7e70db7394372033be2be7df829`** and clean until stage E: the
  sources are read and the fixes are made there, and the pin is not moved
  by the lane. **`W` is that one path in every block of this brief, § 5's
  runs included; until it exists -- neither worktree does before dispatch,
  and `git -C <qa-integration> rev-parse --verify
  origin/feature/m6-es-core-components-681` prints `fatal: Needed a single
  revision` today -- the `qa-integration` checkout at the same pin, clean,
  stands in, read by `git -C` only, and gives the same lines (the drafter
  ran every quoted ES command there).** **Four placeholders stand in this
  brief for hashes that do not exist until dispatch:** `COHASH` (the
  coordinator's tip merged into the lane's branch), `MERGE_HASH` (that merge
  commit, the lane's dispatch tip), `TIPHASH` (the lane's own tip as it
  moves; at stage A it is `MERGE_HASH`) and `V2HASH` (this brief's commit on
  the coordinator's branch). The dispatch comment on #681 and the seeded
  pointer carry their values; the lane reads them there, never guesses them,
  and § 9's placeholder check names all four. **No earlier lane's ES branch
  touches any of the 80** (§ 2): for each of the seven accepted lanes' ES
  tips (T2 `55158d2a64`, T18 `d55235d4b3`, T20 `5c0ddaaeef`, T21
  `3ae9610b0f`, T26 `757f5370ea`, T31 `95852f8736`, T32 `b52245036f`) `git
  diff --stat PIN <tip> -- es-core/src/components` is empty, so the
  integration has no lane-on-lane collision inside the slice. **T33's ES
  branch** `origin/feature/m6-es-app-system-680` resolves to `dd86d7ce20a5`
  in the checkout at the proof's read (2026-10-30; `fatal: Needed a single
  revision` on 2026-10-27), and `git diff --stat PIN dd86d7ce20a5 --
  es-core/src/components` is empty: the lane runs the same diff at stage A
  and again at the hand-back, recording the result either way. The other ES checkouts under
  `~/Development/emulationstation-next.worktrees/` are read with `git -C
  <checkout> show <hash>:<path>` only, and nothing is fetched (§ 10; the
  stale `upstream/master` is § 2's). Until the dispatch comment exists the
  pointer is not seeded and nothing starts.
- **Depth: Independent** -- one seat from another lab (plan § 6c,
  D-WORKFLOW-137; `adversarial-council.md`: an Anthropic-led audit's
  reviewer is pinned GPT-6 Astra; no Gemini seat): Astra at `max` over a
  trimmed, scanned packet (D-WORKFLOW-195 -- **the 21 fork-modified files
  whole** (9,541 lines by `grep -c ''`, the inventory's rule, which the lane
  replaces with the packet's own `wc -l`) **and of the 59 upstream-carried
  files only the ranges the questions cite**; the manifest names every
  trimmed file and range; nothing in the 80 is a binary), a probe then one
  refutation (one in-call retry allowed); `review-plan.json` records depth
  `independent` and the one reviewer with its served model; **exactly two
  keyed `tools/council/run invoke` calls**, every other `tools/council/run`
  call with `COUNCIL_ENV_FILE=/nonexistent` (the runner reads that variable
  at `tools/council/run:21`, default `~/.config/council/env`; the recipe is
  `.claude/skills/council/SKILL.md` and its `references/`; the runtime under
  `tools/council/` from `npm install --offline`, no fetch). The packet is
  scanned before it leaves. **What the scan will hit inside the 80, so the
  lane dispositions rather than stops:** the fork-changes digest quoted no
  credential-shaped line in any of the 80 and the drafter read none; the
  expected hits are identifiers and header names only -- `WebImageComponent.cpp:239-243`'s
  `X-RA-Store-Only` request header (`StoreOnlyHeader` at
  `es-core/src/utils/OfflineProxyUrl.h:29`, a header name, not a value),
  `TextEditComponent.cpp`'s `SDLK_*` key constants and any `isPassword`-shaped
  member of the text field, `ComponentGrid`'s and `IList`'s `key` words in
  comments (the lane's scan at stage A is the list; the proof read none) --
  so `packet-manifest.json` records **every scan hit dispositioned by
  file:line** (library plumbing / macro name / identifier / setting name /
  value), and a hit that is a value stops the packet; no value ever reaches
  the packet or an artifact.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the distribution worktree;
  `8ebaf8daad` is `next`'s commit the P1 branch stacks on and `651150fc88`
  is `upstream/next`'s, both copied from T33's brief and read again by the
  drafter in the coordinator worktree: `651150fc88` is *Merge pull request
  #3547 from spycat88/qcom-bls*, `8ebaf8daad` is *browser: record provider
  pages and GTK4 compilation (#616)*; `a8fe371b0a`, the coordinator's tip at
  this draft, has `8ebaf8daad` as an ancestor):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-core-components-681
cat .github/sessions/saved-session-state-feature-m6-es-core-components-681.md   # the pointer: the dispatch's two hashes; § 10 names the lines to check
git status --short | wc -l                                                   # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1               # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-components-681; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                # the pin; 0
git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10                     # cada856d86: the merge base with ROCKNIX's master (bccd715707 is its parent, § 2)
git -C "$W" rev-parse --verify rocknix/master | cut -c1-10                    # f6c542872e, read from the shared refs
git -C "$W" rev-parse --verify batocera/master | cut -c1-10                   # b2ceb55a7e, read from the shared refs; context only
git -C "$W" merge-base "$PIN" batocera/master | cut -c1-10                    # 1750dded8c: ROCKNIX has merged nothing from batocera since 2026-09-13
for b in m6-es-launch-path-649 m6-es-cloud-pages-665 m6-es-achievements-pages-667 m6-es-state-and-bridge-668 m6-es-guimenu-673 m6-es-pages-678 m6-es-app-views-scrapers-679 m6-es-app-system-680; do printf '%s ' "$b"; git -C "$W" rev-parse --verify "origin/feature/$b" 2>&1 | cut -c1-10; done   # eight tips (T33's `dd86d7ce20a5` since 2026-10-30)
tools/register-check >/dev/null && echo register-ok
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200   # who holds the host, with the time of the read (M7 writes timestamped lines: read the whole tail); no guest before a grant on #681
```

Every line above except the first `cat` and the two `rev-parse` of the
lane's own worktree printed what its comment says on 2026-10-27 (the
drafter, the digests) and again at the proof of 2026-10-30 (the ES lines by
`git -C` against `qa-integration`); the `cat` cannot run before the pointer
is seeded, and `W` does not exist before dispatch. The host file's tail is
whatever the host is doing at the moment of the read, so the lane records
the time beside the lines; a sentence about what the tail "shows today" is
never written into an artifact without one.

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{inventory.json,slices.json}`; the script is T33's
`membership.py` with three lines changed -- the slice id in `hits`, the
`named` list and the `ES-CORE BY SLICE` prefix -- a rewrite of
`tools/renovation-inventory`'s `glob_body` grammar and rest semantics; two
keyword arguments are spaced `key = lambda` so this file carries no
key-equals token. **The heredoc is saved once and run twice** -- first
against `/dev/null` to make the paths file from its own TSV, then against
that file to prove equality; the proof of 2026-10-30 ran both passes with
the two JSONs read by `git show 2174265e9c:`, and the lines below are that
run's, byte for byte. The awk reads columns 1 and 2, `tree` and `path`, the
inventory's first two by its own `columns:` line):

```bash
mkdir -p .qa-scratch/t34
cat > .qa-scratch/t34/membership.py <<'PYEOF'
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
    if h==["es-core-components"]: mine.append(r)
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
named=["es-core/src/components/MenuComponent.cpp","es-core/src/components/AsyncNotificationComponent.cpp","es-core/src/components/VideoVlcComponent.cpp","es-core/src/components/OptionListComponent.h","es-core/src/guis/GuiMsgBox.cpp","es-core/src/guis/GuiTextEditPopup.cpp","es-core/src/guis/GuiTextEditPopupKeyboard.cpp","es-core/src/guis/GuiInfoPopup.cpp","es-core/src/Window.cpp","es-core/src/ThemeData.cpp","es-core/src/GuiComponent.cpp","es-core/src/InputConfig.cpp","es-core/src/HttpReq.cpp","es-core/src/Settings.cpp","es-core/src/resources/TextureData.cpp","es-core/src/resources/TextureResource.cpp","es-core/src/resources/Font.cpp","es-core/src/utils/FileSystemUtil.cpp","es-core/src/utils/AtomicFileUtil.cpp","es-core/src/utils/OfflineProxyUrl.cpp","es-core/src/watchers/WatchersManager.cpp","es-core/src/Scripting.cpp","es-app/src/CloudText.cpp","es-app/src/components/ScraperSearchComponent.cpp","es-core/CMakeLists.txt"]
byp={r["path"]:r for r in rows if r["tree"]=="es"}
for p in named:
    r=byp.get(p)
    if not r: print(p,"NOT IN INVENTORY"); continue
    h,kind=hits(r); print(p, "in-T34" if p in got else "not-in-T34", kind, [(x,kof[x]) for x in h], "tier",r["tier"],"lines",r["lines"],"area",r["area"])
print("ES-CORE BY SLICE")
cnt=collections.Counter(); ln=collections.Counter()
for r in rows:
    if r["tree"]=="es" and r["path"].startswith("es-core/"):
        h,kind=hits(r); cnt[(tuple(h),kind)]+=1; ln[(tuple(h),kind)]+=(r["lines"] or 0)
for k,v in sorted(cnt.items(), key = lambda kv:-kv[1]): print(v,"paths",ln[k],"lines",k)
PYEOF
python3 -I .qa-scratch/t34/membership.py /dev/null > .qa-scratch/t34/block-1.txt
awk -F'\t' '/^TSV$/{p=1;next} /^CLAIMS$/{p=0} p && $1=="es" {print $2}' .qa-scratch/t34/block-1.txt > .qa-scratch/t34/paths.txt
wc -l .qa-scratch/t34/paths.txt                                             # 80
python3 -I .qa-scratch/t34/membership.py .qa-scratch/t34/paths.txt > .qa-scratch/t34/block-2.txt
/usr/bin/grep -E '^(mine:|only-|lines:|fork-own lines:|read lines:)' .qa-scratch/t34/block-2.txt
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-components-681; PIN=16dbac5211eea7e70db7394372033be2be7df829; MB=cada856d86
for p in $(cat .qa-scratch/t34/paths.txt); do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'                  # wc -l 21971
for p in $(cat .qa-scratch/t34/paths.txt); do git -C "$W" show "$PIN:$p" | /usr/bin/grep -c ''; done | awk '{s+=$1} END {print "grep -c", s}'   # grep -c 21984
while IFS= read -r p; do git -C "$W" cat-file -e "$MB:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t34/paths.txt | wc -l   # 80
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN BASE: $p"; done < .qa-scratch/t34/paths.txt | wc -l   # 80
git -C "$W" diff --shortstat "$MB" "$PIN" -- $(cat .qa-scratch/t34/paths.txt)           # 21 files changed, 591 insertions(+), 114 deletions(-)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $(cat .qa-scratch/t34/paths.txt)     # the same line
```

Expected, at `2174265e9c` (the first pass, against `/dev/null`, prints
`mine: 80 paths.txt: 0 equal: False` with every path under `only-mine`; the
second prints these five lines byte for byte -- the proof's run):

```
mine: 80 paths.txt: 80 equal: True
only-mine: []
only-paths.txt: []
lines: 21984 reach: {'shipped': 80} tier: {'upstream-carried': 59, 'fork-own': 21} lang: {'c++': 38, 'c-header': 42}
fork-own lines: 9541
read lines: 21984
```

then, under `CLAIMS`, the 25 named paths with their claimant (the proof's
run): the four components `in-T34 non-rest [('es-core-components', 34)]`
(`MenuComponent.cpp` and `AsyncNotificationComponent.cpp` tier fork-own, 574
and 306 lines; `VideoVlcComponent.cpp` and `OptionListComponent.h`
upstream-carried, 1113 and 661); `guis/GuiMsgBox.cpp`,
`guis/GuiTextEditPopup.cpp`, `guis/GuiTextEditPopupKeyboard.cpp`,
`guis/GuiInfoPopup.cpp`, `Window.cpp`, `ThemeData.cpp`, `GuiComponent.cpp`,
`InputConfig.cpp`, `watchers/WatchersManager.cpp`, `Scripting.cpp` and
`es-core/CMakeLists.txt` `not-in-T34 rest [('es-core-window-input', 35)]`;
`HttpReq.cpp`, `Settings.cpp` and `utils/AtomicFileUtil.cpp` `not-in-T34
non-rest [('es-state-and-bridge', 21)]`; `resources/TextureData.cpp`,
`resources/TextureResource.cpp`, `resources/Font.cpp`,
`utils/FileSystemUtil.cpp` and `utils/OfflineProxyUrl.cpp` `not-in-T34
non-rest [('es-core-utils-resources', 36)]`; `es-app/src/CloudText.cpp`
`not-in-T34 non-rest [('es-cloud-pages', 18)]`;
`es-app/src/components/ScraperSearchComponent.cpp` `not-in-T34 rest
[('es-app-system', 33)]`; and under `ES-CORE BY SLICE` the four rows that
sum to 242 paths: `96 paths 22575 lines (('es-core-window-input',), 'rest')`,
`80 paths 21984 lines (('es-core-components',), 'non-rest')`, `58 paths
50840 lines (('es-core-utils-resources',), 'non-rest')`, `8 paths 3344 lines
(('es-state-and-bridge',), 'non-rest')` -- no `es-core/**` row unassigned
or ambiguous. Then the ES lines: `wc -l 21971`, `grep -c 21984`, 80 at the
merge base and 80 at the base, and the shortstat line twice (the membership
and upstream-delta digests' reads of 2026-10-27, with `W` the
`qa-integration` checkout).

**Three things the figures hide, settled here so the lane does not
re-derive them.** (1) **The inventory counts lines as `grep -c ''` does**
over the 80 files, the unterminated last line included: thirteen slice
files end without a newline (`AsyncNotificationComponent.h` 78/77,
`ComponentTab.cpp` 437/436, `GridTileComponent.cpp` 1596/1595,
`HelpComponent.cpp` 331/330, `ImageComponent.cpp` 1400/1399,
`NinePatchComponent.cpp` 495/494, `RatingComponent.cpp` 295/294,
`ScrollbarComponent.cpp` 215/214, `StackPanelComponent.cpp` 226/225,
`TextComponent.cpp` 857/856, `VolumeInfoComponent.h` 30/29,
`WebImageComponent.cpp` 265/264, `WebImageComponent.h` 40/39), so `wc -l`
sums to 21,971 and `grep -c ''` to 21,984 -- the same bytes, two counting
rules; a figure in `02` says which. The order's *"21,984 read"* is every
line: all 80 are `c++` or `c-header`, shipped, and none vendor-carried. The
same two rules reach every count in this brief: `git grep -c` counts
**lines** and `git grep -o | wc -l` counts **occurrences**, and § 5 states
both for `_("` (22 lines, 27 occurrences) and `exists(` (10 and 10). (2)
**"9,541 fork-own" is the lines of the 21 files the fork touched, not the
lines the fork wrote.** The inventory's `tier` is per file, so
`MenuComponent.cpp` counts whole (574) for an 86/49 change; the fork's own
insertions over the 80 are **591** and its deletions 114, the tool's line
(`21 files changed, 591 insertions(+), 114 deletions(-)` against
`bccd715707` and against `cada856d86`; `--diff-filter=A` 0, `M` 21, `D` 0).
The 21, by numstat: the eleven `.cpp` -- `AsyncNotificationComponent.cpp`
128/17, `MenuComponent.cpp` 86/49, `ImageComponent.cpp` 58/4,
`MultiLineMenuEntry.cpp` 58/26, `ComponentGrid.cpp` 38/2,
`HelpComponent.cpp` 25/7, `WebImageComponent.cpp` 25/1,
`GridTileComponent.cpp` 22/0, `SwitchComponent.cpp` 13/3,
`ComponentList.cpp` 5/0, `ComponentTab.cpp` 3/2 -- and the ten `.h` --
`AsyncNotificationComponent.h` 23/2, `ImageGridComponent.h` 19/0,
`MultiLineMenuEntry.h` 19/0, `GridTileComponent.h` 16/0, `ImageComponent.h`
16/0, `ComponentList.h` 14/0, `MenuComponent.h` 9/0, `SwitchComponent.h`
9/1, `ComponentGrid.h` 3/0, `TextComponent.h` 2/0. Eight pairs have both
halves modified, two headers are modified with their `.cpp` untouched
(`TextComponent.h`; `ImageGridComponent.h` is header-only), three `.cpp`
are modified with their `.h` untouched (`ComponentTab`, `HelpComponent`,
`WebImageComponent`). So the read's tiers are **fork-added 0, fork-modified
21, upstream-carried 59**, and `02` § Coverage carries both tiers. (3)
**The bases.** `rocknix/master` is
`f6c542872e3850c5f432929ead219547a897cd4a` (2026-10-23, *Merge pull request
#54 from porschemad911/s922x-suspend*); the pin's merge base with it is
`cada856d86e3115fbbf0bce09dd761b0ee8fa9fd` (2026-09-23), one commit after
`bccd715707` (`rev-list --count bccd715707..cada856d86` = 1;
`bccd715707..PIN` = 725, 531 without merges; `cada856d86..rocknix/master` =
14), and `bccd715707` is the base every earlier ES brief named because the
repository's `upstream/master` ref was never fetched and still points there
(`rev-list --count upstream/master..rocknix/master` = 15). For this slice the
difference is nothing: `git log --oneline bccd715707..cada856d86 -- <80>`
prints 0 lines and `git diff --stat bccd715707 cada856d86 -- <80>` prints
nothing. `batocera/master` is `b2ceb55a7e3d205a11f055b7d93c8be50cd6f9c9`
(2026-10-21, *update po*) and its merge base with the pin **and** with `rocknix/master` is
`1750dded8c0fdff70630026f756a69fcad0bb995` (2026-09-13, *update po*), so
ROCKNIX has merged nothing from batocera since then. This paragraph is the
one statement of the bases; § 1's comments, § 5's expectations and § 7's
checkbox cite it.

**Merge debt: none** -- 0 of the 14 upstream commits since `cada856d86`
touch a slice path (`git log --format=%h cada856d86..rocknix/master -- <80>
| grep -c .` prints 0, rc 1), the numstat prints nothing (rc 1), and **80 of
80 blobs are identical between `cada856d86` and `rocknix/master`**, 59 of 80
between the pin and `rocknix/master` (the 21 that differ are exactly the
fork's 21). The 14 are the same fourteen T26, T32 and T33 found (S922X
suspend, batteryplus, the sway cursor, four `GuiMenu` entries, ZRAM). The
record in `02` § The merge debt is one line (§ 6), not a table. **Batocera's
eight commits on `es-core/src/components` since `1750dded8c`** (139 on any
path; the directory and the slice are the same set) are **a reconciliation
list for the integration, not this slice's debt**, named in `02` § The merge
debt's one line as *not ROCKNIX's*, never a debt figure and never fetched:
`0806a0c5c` 2026-10-20 (launch zoom; `GridTileComponent.cpp` 53/4, `.h`
2/0, `VideoComponent.h` 7/0), `9dbd4b9bf` 2026-10-17 (*fix null pointer RB
was seeing*; `HelpComponent.cpp` 7/3), `308221458` 2026-10-16
(`GridTileComponent.cpp` 8/0, `.h` 1/0), `ac4baceaf` 2026-10-14 (*fix: rtl
auto switch*; `SwitchComponent.cpp` 12/3, `.h` 1/0), `09f5f708f` 2026-10-14
(*fix rtl help menu*; `HelpComponent.cpp` 23/9), `b728ac99d` 2026-10-02
(*fix: rtl alignments (others)*; `MenuComponent.cpp` 6/2,
`TextComponent.cpp` 9/3), `ab218fba1` 2026-10-02 (*load slow menu option
lists in the background and fix asan errors*; `OptionListComponent.h`
100/1), `ad104860f` 2026-09-30 (*Fix rtl aligments*; `MultiLineMenuEntry.cpp`
7/0): `10 files changed, 233 insertions(+), 22 deletions(-)`, seven of the
ten also fork-modified (`7 files changed, 117 insertions(+), 18
deletions(-)` restricted to those). **One real overlap by hunk range:**
`HelpComponent.cpp`, where batocera's `09f5f708f` (hunks `-8,6`, `-119,7`,
`-139,16`, `-310,4`) and the fork's `7dc8bf373` (`-121,10`, `-135,17`) both
rewrite `updateGrid()`, overlapping at base lines 121-125 and 139-151; the
other six pairs share no base line (the digest's reading, not re-derived). **One item runs the other
way:** `9dbd4b9bf` guards `HelpComponent::setOpacity` against a null `mGrid`
(*"null when ShowHelpPrompts is disabled or there are no prompts"*); at the
pin `HelpComponent.cpp:208-213` and `:251` dereference `mGrid` with no guard
(`git grep -n -E 'setOpacity|mGrid->getChildCount|mGrid == nullptr' PIN --
es-core/src/components/HelpComponent.cpp` prints `208`, `210`, `212`, `213`,
`251`), and `Window.cpp` at the pin never calls `mHelp->setOpacity` (its
eight `mHelp->` lines are `:745`, `:1001`, `:1009`, `:1011`, `:1012`,
`:1077`, `:1397`, `:1398`: render, the grid, the prompts, the style, the hit
test) -- so who calls `HelpComponent::setOpacity` on the fork's images, and
whether `mGrid` can be null there, is Q7's question under D-WORKFLOW-162.

**The files, read whole** (lines at the pin by `grep -c ''`, the
inventory's rule; the fork's `--numstat` against the base, which equals the
merge base's for every row; the fork's commits `bccd715707..PIN` on the
file, newest first; every `.cpp` is in `es-core/CMakeLists.txt`'s
`CORE_SOURCES` at `:186-223` and every `.h` in `CORE_HEADERS` at `:49-90`,
each named exactly once and unconditionally, so no per-file CMake column; a
neighbour outside `es-core/src/components/` is written with its directory
the first time it appears; the 21 fork-modified files one row each, the 59
upstream-carried grouped by what they are):

| File | Lines | +/- | Fork commits (newest first) | What it is at the pin |
| --- | ---: | ---: | --- | --- |
| `AsyncNotificationComponent.cpp` / `.h` | 306 / 78 | 128/17, 23/2 | `38e08cdc6 460102b91 22b15531c 0c06ad548 81231b377 016385b52 f7d12ffb5 fa26307e1 dca520faa`; `.h` `460102b91 22b15531c` | the top-centred progress card (the third surface tier): **`:12 #include "../../es-app/src/CloudText.h"`** (the one es-core to es-app include, `38e08cdc6`; the comment `:9-11` says why; used once at `:144 CloudText::chooseThatFits`); `#define NOTIFICATION_OPACITY 255` `:31` (the 200 it replaced in `:18-30`; used `:114`, `:276`); the width `max(sizeText("TEXT FOR SIZE CALCULATION TEST"), 0.9 * W)` `:63-65` (reasoning `:46-62`); the edge colour from the theme and the comment refusing a drawn rim `:79-89`; centred at the top `:112-113`; `static chooseThatFits(row, candidates)` `:136-144`; three `updateText` overloads `:147`, `:157`, `:168` under `mMutex` (h `:67`; cpp `:149`, `:159`, `:170`, `:182`, `:189`, `:196`), each leaving at least one candidate (`push_back("")` `:165`, `:174`, `:177`); `render` `:194` re-chooses a row only when its joined candidates change `:200-224` (keys h `:55-58`); `mFrame = new NinePatchComponent` `:78`, `mGrid = new ComponentGrid` `:97`, both deleted `:125-126`; callers of `updateText(` outside the slice: 24 lines in 7 files (`ThreadedCloudSync.cpp:48,167,184,425,700`, `ProxyCards.cpp:131,180,217,259,286,382,516`, `ThreadedBluetooth.cpp:17,36,74,93`, `GuiUpdate.cpp:200,219,224,234`, `ContentInstaller.cpp:97,102`, `ThreadedHasher.cpp:177`, `guis/GuiMenu.cpp:11718`); the vector overloads used by `ThreadedCloudSync.cpp:184,425,700` and `ProxyCards.cpp:180,382`; unit cases `es-app/tests/unit/CloudTextTests.cpp:832-854` (8 `CHECK`s on `chooseThatFits`) and `:1597-1598` |
| `ComponentGrid.cpp` / `.h` | 553 / 150 | 38/2, 3/0 | `aa8c5da4c` | the cell grid every dialog and page is laid on: `bool canMoveCursor(const Vector2i&) const` `:396-412` (h `:63`; the comment `:380-395` naming #115 and `OK CHOOSE CHOOSE`), the same linear scan as `moveCursor` `:329-379` (`:347-357`; the reverse scan commented out `:358-372`) with nothing moved; `getHelpPrompts` `:519-553` offers up/down and left/right only when the scan finds a focusable cell other than the current one `:527-528` (was `mGridSize.y() > 1` / `.x() > 1`); three upstream prompt lines `:546`, `:548`, `:550` (`CHOOSE`, icon keys untranslated); `canMoveCursor` called from nowhere else in `es-app` or `es-core` |
| `ComponentList.cpp` / `.h` | 728 / 169 | 5/0, 14/0 | `551c5a762`; `.h` `551c5a762 d9fa93bf2` | the row list under every settings page: `static float rowInset()` `:491-494` (h `:109-113`) returning `TOTAL_HORIZONTAL_PADDING_PX / 2`, where **`#define TOTAL_HORIZONTAL_PADDING_PX 20` `:11`** is upstream's pixel constant used by `updateElementPosition` `:508` and `updateElementSize` `:521`; `ComponentListFlags::DIMMED_ALPHA = 0x50` and `inline dimmed(color)` h `:25-26` (comment h `:19-24`: `render` recolours every element every frame, so a dim must live inside the element's `setColor`, #182); `render` `:321`, `setColor` at `:391`, `:394`, `:398`, `:400` every frame; upstream `_()` at `:276` (`ENABLED`/`DISABLED`) and **`:568` (`_("up/down")`, `_("CHOOSE")`, L-01)**; `updateCameraOffset` `:295-319`; callers of `rowInset()` `guis/GuiMenu.cpp:4091,4097`, `guis/GuiWifi.cpp:103`; of `dimmed()` `MultiLineMenuEntry.cpp:84`, `SwitchComponent.cpp:30` |
| `ComponentTab.cpp` (`.h` upstream, 82) | 437 | 3/2 | `8927b1760` | the tab strip over a tabbed menu (D-UI-021): `getHelpPrompts` `:320-345` de-duplicates on `left/right` `:332` and pushes `HelpPrompt("left/right", _("SWITCH TAB"))` `:341` (was `HelpPrompt(_("up/down"), _("CHOOSE"))`; the slice's one changed `_("` line; msgid `SWITCH TAB` at `locale/lang/fr/LC_MESSAGES/emulationstation2.po:4929-4930`, `CHANGER D’ONGLET`); `input` returns on `size() == 0` `:79-80`; `getHelpPrompts` empty on `!size()` `:322-323`; `setColor` `:193`; `addTab` uppercases at display time (#63) |
| `GridTileComponent.cpp` / `.h` | 1,596 / 332 | 22/0, 16/0 | `12de21757 3b7265f33 2088eadb9` (both) | one tile of the image grid: `GridTextProperties::multiLine` read from the theme `:700-701` (h `:135`; declared `ThemeData.cpp:267` as `STRING // auto, true, false`) and applied as MULTILINE / SINGLELINE / AUTO h `:107-116` (the comment on the 1.8-line moving threshold; #27, D-UI-050); `setDisplayAspect(float)` `:1048-1053` and `setDisplayRotation(int)` normalising `((q % 4) + 4) % 4` `:1055-1063`, re-applied by `setImage` `:1042-1043` (`:1043` indented one level deeper than `:1042`, L-14), stored h `:305-306` (API h `:233-236`); `:11 #ifdef _RPI_`; `Padding = Vector4f(16.0f, 16.0f, 16.0f, 16.0f)` `:56`, `cornerSize = Vector2f(16, 16)` h `:148`; raw `new`/`delete` of the sub-images upstream's (`:39`, `:85-100`, `:490-540`, `:777-934`); callers through a tile decorator `guis/GuiSaveState.cpp:80-81`, `views/gamelist/GridGameListView.cpp:45-46`, `guis/GuiImageViewer.cpp:284-285`; batocera's launch zoom touches `:1529-1532` and h `:254`, `:261` (context) |
| `HelpComponent.cpp` (`.h` upstream, 44) | 331 | 25/7 | `7dc8bf373` | the bottom help bar (#210): an entry's width is measured first and kept only if `width + entryWidth < maxWidth` `:121-138` (the old code added before testing); the grid's box `rowWidth = width - ENTRY_SPACING` floored at 1 `:143-152`; the last entry's trailing spacer 0 (`isLast` `:160`, `:166`); unchanged around it: `width = 0` `:95`, `maxWidth = W - ENTRY_SPACING` `:79` or `W - size.x()` of the right-hand component `:90`, the label split for 4:3 screens `:110-120`, `getIconTexture` `:176-200` (the theme's icon map, then `ICON_PATH_MAP` with keys `up/down left/right up/down/left/right a b x y l r lr start select F1`, else `LogError "Unknown help icon"` and `nullptr` `:190-194`); **`setOpacity` `:208-213` and `:251` dereference `mGrid` unguarded** (batocera `9dbd4b9bf`); `ICON_TEXT_SPACING W*0.0042f` `:13`, `ENTRY_SPACING` x2 `:16`; `mPrompts.empty()` returns `:67-70` |
| `ImageComponent.cpp` / `.h` | 1,400 / 220 | 58/4, 16/0 | `b49d85448 1ce55ceef 12de21757 4e4ab0647 c437fe77f 3b7265f33`; `.h` `12de21757 3b7265f33` | the image drawer: `resize` fits the quad at `(physical.y * mDisplayAspect, physical.y)` when an aspect is set `:91-97` and swaps the fitted width and height when `mDisplayRotation % 2` `:98-101`; the crop branches follow the turn `:156-159`, `:167-170`; `updateVertices` permutes the four texture corners for turns 1, 2, 3 `:273-291`; `setDisplayAspect` clamps negatives to 0 and resizes on change `:481-489`; `setDisplayRotation` normalises `:491-499`; getters and members h `:133-140`, `:194-195`; **h `:76` `virtual void setColor(unsigned int color) { setColorShift(color); }`** (`es-native-ui.md:302`); **`:408` asks `TextureResource::get` by path** (T26 #1221, T32 #1263: the caller's half, § 1 a); `_()` at `:1060` (`SELECT`); cached `exists(value.s)` `:1232` (a theme path); `getHelpPrompts` `:1057`; the two diagnostic `LOG` commits (`c437fe77f` +2, `1ce55ceef` +1) are removed by `4e4ab0647` and `b49d85448`: **0 added `LOG(` lines net**; callers of the aspect and turn `DisplayAspect.cpp:147-148`, `guis/GuiImageViewer.cpp:680-681`, `views/gamelist/DetailedContainer.cpp:1070-1071` |
| `ImageGridComponent.h` | 1,705 | 19/0 | `217872e32 bb79e4fc4 12de21757 3b7265f33` | header-only template, the tile grid behind the grid view and the save-state manager: `#include <functional>` `:2` above the include guard `:3` (L-14); `setTileDecorator(std::function<void(GridTileComponent*, const T&)>)` `:100` (comment `:94-99`), `mTileDecorator` `:181`, called at the three tile-creation sites `:309` (`preloadTiles`), `:381` (`ensureVisibleTileExist`, indented two levels short of its block) and `:422` (the scroll-loop copy, audit #258 PL-017, comment `:418-421`); `calcGridDimension()` `:1437-1468` (`LOG(LogError)` guards `<1` `:1449-1452`); `onCursorChanged` (from `:1065`), its `mStartPosition` `:1162-1186`; `clear()` / `resetGrid()` (#207, #1266's contract, § 1 e); callers of the decorator `guis/GuiImageViewer.cpp:281`, `guis/GuiSaveState.cpp:77`, `views/gamelist/GridGameListView.cpp:42`, each before its first add |
| `MenuComponent.cpp` / `.h` | 574 / 122 | 86/49, 9/0 | `f1ae6bc25 b6eb26980 a846b4c69 8927b1760 082edc223`; `.h` `7b18c4489 a846b4c69` | the title, tab strip, rows and button bar every settings page is: **`#define BUTTON_GRID_HORIZ_PADDING (Renderer::getScreenWidth()*0.022)` `:14`** (the 0.0052 it replaced in the comment `:7-13`, *"the one place it is defined"*; used by `makeButtonGrid` `:547`, `:555`; D-UI-012), `BUTTON_GRID_VERT_PADDING (H*0.0296296)` `:6`; the wrap callback `:80-101` (down past the buttons to the strip when it has tabs, else the first row; up past the top to the buttons with the last row armed); the strip entered non-focusable at construction `:115`/`:117-118` and re-entered focusable on the first `addTab` (`removeEntry` `:143`, `setEntry(..., true, ...)` `:144`; comment `:109-115` citing #325); the page opens on its first row `setCursorTo(mList)` `:123`; `input` is `GuiComponent::input` alone `:126-131` (#65); `updateSize` `:396-447` keeps the row-fit loop and lets the title-image alignment block run in both modes (`pad = W*0.012`, `setPadding` `:438`, `:443`; #160); `setCursorToButton(int)` `:506-515` (h `:53-56`: the inner `ComponentGrid` cursor first, then the outer focus, then `updateHelpPrompts`; **`static_pointer_cast<ComponentGrid>(mButtonGrid)` while `setButtonGrid` `:492-503` accepts any `GuiComponent`**, L-15); `getSubTitle()` h `:85-89`; `clearButtons` `:478-483` and `updateGrid` `:517-529` (`removeEntry` then `makeButtonGrid` `:543-562`); the up-casing formatters `:205` (`addGroup`), `:233`, `:236` (`addWithDescription`/`addEntry`), `:283` (`setTitle`), `:487` (`addButton`); `spacer->setSize(10, 0)` `:167`, `:192`; `fitTo(..., Vector2f(-32, -32))` `:453`; `getHelpPrompts` `:531-533` returns `mGrid.getHelpPrompts()`; `_()`: none; callers `setCursorToButton` `guis/GuiMenu.cpp:4542`, `guis/GuiWifi.cpp:153`; `getSubTitle` `guis/GuiGameAchievements.cpp:234,278`; `setButtonGrid` with a non-grid `guis/GuiMenu.cpp:591` (`mVersion`) |
| `MultiLineMenuEntry.cpp` / `.h` | 153 / 46 | 58/26, 19/0 | `7c7ffab43 daafb69f1 d9fa93bf2 48d43c0fb`; `.h` `217872e32 daafb69f1 d9fa93bf2 48d43c0fb` | the label + description row: `static naturalHeight(text)` = `font->getHeight() + padding.y + padding.w` `:50-56` (the comment `:38-49` on #241 and the 0.9/1.1 cells); `layoutRows()` `:58-77` from the constructor `:36`, from `setDescription` in single-line mode `:118` and from `onSizeChanged` in multi-line mode `:132`; **the row percentages `(th*0.9)/h` and `(sh*1.1)/h` `:74-75`, upstream's formula carried whole (L-03)**; `mDimmed`/`mColor` `:18`, `:21` (h `:40-43`), `setColor` applying `dimmed()` `:79-86` (`:84`), `setDimmed` `:89-93`, `setPadding` reaching both texts `:100-105`; `setDescription` re-lays `:112-119`; `onSizeChanged` under the `mSizeChanging` guard `:121-136`; the list re-laid only on `GuiSettings::updateSize` (h `:26-28`); callers of `setDimmed` `guis/GuiMenu.cpp:4094,5478,6302,6318`, `guis/GuiRetroAchievementsSettings.cpp:262,375`; of `setPadding` `guis/GuiMenu.cpp:6341`; `Font::getHeight(lineSpacing)` is `mMaxGlyphHeight * lineSpacing` (`es-core/src/resources/Font.cpp:754-756`, grown in `getGlyph` for ASCII 32..127 only `:420-421`, from 0 `:107`; T36's file, cited) |
| `SwitchComponent.cpp` / `.h` | 175 / 60 | 13/3, 9/1 | `d9fa93bf2` (both) | the on/off row: `mDimmed(false), mColor(0)` `:8-9` (h `:55-57`), `mColor = menuTheme->Text.color` `:16`, `setColor` storing and applying the dim `:27-31` (`:30`; `override` h `:33`), `setDimmed` `:33-37`, `isDimmed` h `:37`; **the constructor reads `menuTheme->Text.font->getHeight(1.1f)` for the image height `:14`** (L-16); the tri-state cycle `:50-80`, `getValue`/`setValue` `:118-138`; `_()` `:168` (`CHANGE`); `getHelpPrompts` `:165`; callers of `setDimmed` `guis/GuiRetroAchievementsSettings.cpp:472,488`; batocera's `ac4baceaf` touches the constructor at `-17,3` beside the fork's `-15` (context) |
| `TextComponent.h` (`.cpp` upstream, 857) | 141 | 2/0 | `b6eb26980 7b18c4489` | two getters, `getLineSpacing()` `:48` and `getHorizontalAlignment()` `:49`, read by `guis/GuiGameAchievements.cpp:238,240,291,299,302` (#160); **`TextComponent.cpp` is unchanged by the fork: `:338` `sizeWrappedText(..., getSize().x(), ...)` against `:350` `sx = mSize.x() - mPadding.x() - mPadding.z()` (#48's root, L-17); `:486` `int limit = mSize.y() - mPadding.y() - mPadding.y();` where `:428` and `:351` subtract `.w()` (3.6)**; `onTextChanged` `:315-340` (SINGLELINE with `"a\nb"` measures `"a"` `:325-327`); batocera's `b728ac99d` changes `TextComponent.cpp` 9/3 for RTL (context) |
| `WebImageComponent.cpp` (`.h` upstream, 40) | 265 | 25/1 | `0ec3f43ae c13119bfb` | an image fetched over HTTP and cached: `#include "utils/OfflineProxyUrl.h"` `:7`; after `REQ_SUCCESS` and `exists(mLocalFile)` `:190` (upstream, cached), **a file of size 0 (`getFileSize` `:197`, an uncached `stat64`) is removed and the update returns `:197-200`** (comment `:191-196`, #180; `mUrlToLoad` was cleared when the request went out `:244`, so the component never asks again, L-08); the request carries `X-RA-Store-Only` when the URL is the offline proxy's `:239-243` (`Utils::OfflineProxy::isProxyUrl`, `StoreOnlyHeader`; #199); `HttpReqOptions options(mLocalFile)` on the stack `:239`, handed by pointer `:243` (consumed in `HttpReq::HttpReq` before it returns, `es-core/src/HttpReq.cpp:119-123`, `:131-132`, `:172-176`; L-21); cached `exists` at `:81` (destructor), `:134` (`setImage`'s cache check), `:190`, `:228` (the directory); `removeFile` erases the cache key (`FileSystemUtil.cpp:185-195`); 7 `HttpReq` lines (`:3`, `:178`, `:190`, `:239`, `:243`; h `:6`, `:27`) |
| the lists: `IList.h`; `TextListComponent.h`; `CarouselComponent.cpp` / `.h`; `ComponentTab.h`; `ScrollbarComponent.cpp` / `.h` | 431; 981; 1,128 / 183; 82; 215 / 64 | 0/0 | -- | `IList.h`: `template <typename EntryData, typename UserData> class IList : public GuiComponent` `:60-61`, the scrolling-list base of `ComponentList`, `ComponentTab`, `CarouselComponent`, `ImageGridComponent`, `TextListComponent`; `listInput` `:267-290`, `listUpdate`'s tier maths `:292-329` (`:313`, `:320`), `setCursorIndex` `:138-147`, `scroll` `:376-400` (`LIST_NEVER_LOOP` clamps and zeroes velocity and tier `:388-399`). `TextListComponent.h`: the game list's text list, `:34-35`; the visible range in `render` `:262-269`; `updateCameraOffset` `:591-608`; `Font::getHeight` reads `:613`, `:725` (L-16). `CarouselComponent.cpp`: the themed carousel (the `gamecarousel` view's, not `SystemView`'s); **`moveCursorFast` `:74-90` with `:113`, `:119` (3.8)**; the shortest-path target `:183-200`; `getHelpPrompts` `:354-361` offers `up/down` or `left/right CHOOSE` by carousel type alone (L-13); cached `exists` `:765` (`marqueePath`); `CAROUSEL_MOUSE_SPEED 100.0f` `:898`; 12 `isMappedLike`; 2 `_("`. `ComponentTab.h`: `:31`, structs `:8`, `:18`. `ScrollbarComponent`: the list scrollbar, no outside includer |
| the rows and editors: `OptionListComponent.h`; `SliderComponent.cpp` / `.h`; `ButtonComponent.cpp` / `.h`; `DateTimeEditComponent.cpp` / `.h`; `RatingComponent.cpp` / `.h`; `TextEditComponent.cpp` / `.h`; `ScrollableContainer.cpp` / `.h`; `StackPanelComponent.cpp` / `.h` | 661; 408 / 67; 225 / 73; 363 / 77; 295 / 63; 400 / 72; 132 / 32; 226 / 37 | 0/0 | -- | `OptionListComponent.h`: the choose-one / multi-select row and its popup, header-only; **four `delete this` `:96`, `:145`, `:158`, `:195`** (each the lambda's last statement `:97`, `:146` or followed by `return true` `:196`; L-11); **`:310-311`, `:323-324` return straight after the callback (T31's invariant, § 1 d)**; `getHelpPrompts` `:202` (the popup) and `:636-643` (`left/right CHANGE` whenever `!mMultiSelect`, L-13); `Font::getHeight` reads `:255`, `:276`; 6 `_("`; `tests/gpu-governor-save.py:14` lifts four of its methods as text (`:26-29`); batocera's `ab218fba1` adds a 100-line background loader (context). `SliderComponent.cpp`: `calculatePrecision(step)` `:44-58`; `setValue`'s clamp and the AUTO sentinel `:234-257`; the value text in `onValueChanged()` `:271-319` (**`"Auto"` at `:282`, outside `_()` and not the placeholder `AUTO`, 3.7**; the suffix glued `:295-296`, `:312-313`); `getHelpPrompts` `:337`; 1 `_("`. `ButtonComponent.cpp`: a button owning its callback; `TEXT_PADDING Math::max(12, W*0.014)` `:10` (12 px wins below 857 px); the `toUpper` `:73`; `:80`; `getHelpPrompts` `:186`. `DateTimeEditComponent.cpp`: the month/day/year steps inside `input()` `:116-164` (`:131-132`, `:144-145`, `:152-153`, `:156-158`); `getDisplayString()` `:251-260` (`getTime() == 0` -> `""` `:256-257`). `RatingComponent.cpp`: the OK-press accumulation `+= 1/5` `:192-204`; `getHelpPrompts` `:262`. `TextEditComponent.cpp`: the field under the on-screen keyboard; **two `postToUiThread([this] ...)` `:39`, `:47`** (`startEditing`/`stopEditing` on focus; L-12); `TEXT_PADDING_HORIZ 10`, `TEXT_PADDING_VERT 2` `:8-9`; `setSize(4096, ...)` `:31` (a `Font::getHeight` read, L-16); `fitTo(..., -34, -32 - TEXT_PADDING_VERT)` `:53`; `moveCursor` `:267-271` through `Utils::String::moveCursor`; `input()`'s keyboard-RETURN branch `:176-189` (`textInput("\n")` `:180` when multiline, else `stopEditing()` `:184`; no `applyChanges` symbol exists in the file at the pin -- T21 #1199's writer is `SystemConf`'s, where it was fixed); `getHelpPrompts` `:390`; 2 `_("`; `SDLK_*` and `SDL_StartTextInput` symbols. `ScrollableContainer.cpp`: `update` `:62-107` (**`:69 const float widthMod = (680.0f / getSize().x());` computed and never used**), `getContentSize` `:110-124`, `reset` `:126-131`, `AUTO_SCROLL_RESET_DELAY` `:6`. `StackPanelComponent`: a horizontal/vertical stack |
| the images and the video: `AnimatedImageComponent.cpp` / `.h`; `NinePatchComponent.cpp` / `.h`; `RectangleComponent.cpp` / `.h`; `PostProcessShaderComponent.cpp` / `.h`; `VideoComponent.cpp` / `.h`; `VideoPlayerComponent.cpp` / `.h`; `VideoVlcComponent.cpp` / `.h`; `WebImageComponent.h` | 86 / 47; 495 / 88; 166 / 37; 105 / 28; 657 / 228; 274 / 42; 1,113 / 170; 40 | 0/0 | -- | `AnimatedImageComponent`: the busy spinner's frames (no outside includer; `BusyComponent.cpp` and itself). `NinePatchComponent.cpp`: the stretched frame behind menus, cards and dialogs; `int margin = 50` `:177`; `:415 #if defined(USE_OPENGLES_30)`. `VideoComponent.cpp`: the video base (`setScreensaverMode`, play/stop, delay); `:22 #if WIN32`; cached `exists` `:327` (the theme's video path), `:591` (a property) (L-20); `getHelpPrompts` `:347`; `255.0f` `:223`, `1000.0f` `:282`; batocera's `0806a0c5c` adds 7 lines to `VideoComponent.h` (context). `VideoPlayerComponent`: the whole unit under `:1 #ifdef _RPI_` (omxplayer; `<fcntl.h> <unistd.h> <wait.h>` `:9-11`), the slice's one `TODO`. `VideoVlcComponent.cpp`: the libvlc player; **the slice's only `std::thread` `:91` and `.detach()` `:95` inside `mediaplayer_release_async` `:84-96`, which sets `ctx->component = nullptr` on the interface thread without the lock `:89` while VLC's thread reads it in `display` `:53-61` and locks `c->mutexes[frame]` in `lock`/`unlock` `:28-49`; `render` locks the same mutex `:491-494`; `stopVideo` `:897-930` calls it at `:911`, else `delete mContext` `:915`; the destructor is `stopVideo()` `:98-100`** (L-10); gates `:17`, `:485`, `:592`, `:668`, `:779`, `:836`, `:874` (`LIBVLC_VERSION_MAJOR >= 3`), `:875`; `maxSize = Vector2f(400, 300)` `:782`; cached `exists` `:605`, `:639` (the Windows plugin check); **the slice's one non-ASCII byte, 0x96 at `:859`** in the comment `// use: vlc<0x96>long-help` (a Windows-1252 en dash, not UTF-8; `file -` reads the file as `Non-ISO extended-ASCII text`); `std::mutex mutexes[2]` in `VideoContext` h `:40`, `:14`; h `:1-3` `#pragma once` over an `#ifndef` guard. `WebImageComponent.h`: `class HttpReq;` `:6`, `HttpReq* mRequest = nullptr;` `:27` |
| the status glyphs and the rest: `BatteryIconComponent.cpp` / `.h`; `BatteryIndicatorComponent.cpp` / `.h`; `BatteryTextComponent.cpp` / `.h`; `BusyComponent.cpp` / `.h`; `ClockComponent.cpp` / `.h`; `ControllerActivityComponent.cpp` / `.h`; `DateTimeComponent.cpp` / `.h`; `HelpComponent.h`; `IExternalActivity.cpp` / `.h`; `NetworkIconComponent.cpp` / `.h`; `VolumeInfoComponent.cpp` / `.h` | 101 / 38; 56 / 19; 64 / 30; 134 / 41; 52 / 24; 603 / 135; 110 / 41; 44; 3 / 14; 79 / 34; 143 / 30 | 0/0 | -- | the battery glyph, percentage and indicator (`BatteryIndicatorComponent.cpp:7 <SDL_power.h>`, the one SDL header T31's fakes lack), the clock (`ClockComponent`; D-UI-058; `tools/vm-walks/masks.txt` masks its minute), the network glyph, the pad/battery/network strip (`ControllerActivityComponent`; `getScreenHeight() / 200.0f`, `/ 100.0f`, `/ 280.0f` `:62-67`), the date text (`DateTimeComponent`; 1 `_("`), the volume overlay (`VolumeInfoComponent`; `fitTo(-32, -32)` `:45`; `255.0f` `:127`), `IExternalActivity` (an interface, three lines of `.cpp`), the spinner `BusyComponent` (`BusyComponent(window, text)`: `setText("")` is a no-op against the empty initial state, `es-code-traps.md:56`; `SDL_CreateMutex`/`SDL_DestroyMutex`, `SDL_GetTicks`; #1112 asks it for a contrast edge, M7's, read-only), `HelpComponent.h` |

**The 33 fork commits on the 80** (`git log --oneline bccd715707..PIN --
<80> | wc -l` = 33; `--no-merges` = 33; one author by `%an`, two addresses
by `%ae`; `--diff-filter=A` 0),
from `48d43c0fb` 2026-08-28 *Cloud setup: align prose rows and let the
details group breathe* to `551c5a762` 2026-10-01 *cloud: the dimmed SETTINGS
row keeps the rows' inset (fork #349)*; the fork-changes digest reads 20 of
the 33 subjects as fixes, 2 as diagnostics (both removed again by the pin,
net 0 `LOG(` lines), 1 as a refactor (`38e08cdc6`, the es-app include), 7 as
features and 3 as styling or text -- its reading of the subjects, not a
tool's line. The 21 distinct issue numbers the subjects and bodies cite, counted by
occurrence (`git log --format='%s%n%b' bccd715707..PIN -- <80> | grep -o -E
'#[0-9]+' | sort | uniq -c`): #245 (3), #243 (3), #65, #258, #210, #199, #191, #160, #115 (2 each), and
once each #63, #53, #349, #325, #27, #250, #241, #198, #182, #180, #120,
#105. The lane's `02` § Coverage quotes the 33 subjects from its own `git
log`, never from here.

**What the digests checked and found sound, beyond what the table and
§ 5 carry, so the lane confirms rather than hunts:** the strip's re-entry
on the first tab moves its cell to the end of `mCells` with no cursor
change (`ComponentGrid.cpp:150-163`); **the 17 distinct msgids across the
80's 22 `_("` lines every one have a `msgid` line in
`locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the pin with a
non-empty translation** (`WORKING...`, `CHOOSE`, `Unknown`, `accept`,
`BACK`, `CHANGE`, `SELECT`, `select all`, `SELECT ALL`, `select none`,
`SELECT NONE`, `EDIT`, `MOVE CURSOR`, `DISABLED`, `ENABLED`, `up/down`,
`SWITCH TAB`; the proof's parser, 2026-10-30), and the catalog's own
figures at the pin are T33's (`grep -c '^msgid '` 2,207; 2,188 distinct
msgids with 0 empty translations once continuation lines are joined). The
one translation that is itself the defect is `up/down` -> `haut/bas` at
po `:3708-3709` (L-01): a correct French line for a string that should
never have been a msgid.

**What they found instead -- the leads, one line each.** § 4 carries each
lead's disposition and the question it serves, citing this table rather
than restating its lines; the lines are the pin's, every one read again by
the stranger's proof of 2026-10-30 (its corrections are the last section).

| Lead | Lines at the pin | Shape | Q |
| --- | --- | --- | --- |
| L-01 | `ComponentList.cpp:568`; `HelpComponent.cpp:102-104`, `:190-194`; `es-core/src/InputConfig.cpp:353-366`; fr po `:3708-3709` | the one icon key in the tree that goes through `_()`: the catalog translates `up/down` to `haut/bas`, `InputConfig::buttonLabel` returns the key unchanged, `ICON_PATH_MAP` has no such key, so under French every settings list's CHOISIR prompt draws with a null icon and logs `Unknown help icon "haut/bas"`; the fork's own strip line `ComponentTab.cpp:341` and `ComponentGrid.cpp:546-550` write the key untranslated | Q3, Q6 |
| L-02 | `MultiLineMenuEntry.cpp:52-56`; `resources/Font.cpp:754-756`, `:420-421`, `:107` | the entry's row height is `mMaxGlyphHeight * 1.5` + padding: the tallest ASCII glyph rasterised so far, 0 at construction; a row built before the font has drawn its tallest glyph is laid out a few px shorter than one refreshed after; the list is re-laid only on `GuiSettings::updateSize` | Q1 |
| L-03 | `MultiLineMenuEntry.cpp:74-75` | `setRowHeightPerc(0, th*0.9/h)` and `(1, sh*1.1/h)` sum to 1 only when `th == sh`; a taller Text font underfills (a gap under the line), a taller TextSmall overflows by `0.1*(sh-th)/h`; upstream's formula moved whole into `layoutRows` | Q1 |
| L-04 | `MenuComponent.cpp:14`, `:547-558`, `:527`; `ComponentGrid.cpp:174-175`, `:194`; `ButtonComponent.cpp:10`, `:80` | the bar is `sum(text + max(12, 0.014W)) + N * 0.022W` wide and its cell does not resize it (`resize = false`), so a wider bar is centred on the cell and overhangs both edges of the menu; the gap grew 4.2x (3 px to 14 px at 640); candidates `guis/GuiMenu.cpp` (14 `addButton` sites), `GuiBluetoothDeviceOptions.cpp` (4), `GuiWifi.cpp` (3), `GuiInstallStart.cpp` (3) | Q2 |
| L-05 | `MenuComponent.cpp:7-13` against `es-core/src/guis/GuiTextEditPopupKeyboard.cpp:14`, `:220` | the comment says the gap is defined in "the one place"; the keyboard popup keeps its own `BUTTON_GRID_HORIZ_PADDING (W*0.0052083333)` for its key buttons; two definitions, one claim (the popup is T35's file; the claim is this slice's comment) | Q2, Q7 |
| L-06 | `ComponentList.cpp:11`, `:491-494`; `guis/GuiMenu.cpp:4091`, `:4097`; `guis/GuiWifi.cpp:103` | `rowInset()` exports upstream's `TOTAL_HORIZONTAL_PADDING_PX 20` (10 px a side at every panel) to two fork pages: 1.6 % of a 640 panel, 0.5 % of 1920 | Q2 |
| L-07 | `AsyncNotificationComponent.cpp:12`; `es-core/src/Window.cpp:29` | es-core includes `../../es-app/src/CloudText.h`; the only other such include is upstream's `ApiSystem.h` in `Window.cpp`; a build of es-core alone, or a reorder of the include paths, fails here; the unit build links `CloudText.cpp` | Q7 |
| L-08 | `WebImageComponent.cpp:197-200`, `:244` | a 0-byte answer (the proxy's 204 for a badge it lacks) removes the file and returns, but `mUrlToLoad` was cleared when the request went out, so the component never asks again: the badge stays blank for the page's life with no word on the row; by design per the comment | Q5 |
| L-09 | `WebImageComponent.cpp:190` (and `:81`, `:134`, `:228`); `utils/FileSystemUtil.cpp:144`, `:203-220` | `exists(mLocalFile)` cached right after `HttpReq` wrote the file; a remembered miss from `:134` before the download would make a successful download read as absent unless the writer erases the key; `getFileSize` `:197` is an uncached `stat64`; whether `HttpReq`'s write goes through the cache's erase is T21's and T36's answer | Q5 |
| L-10 | `VideoVlcComponent.cpp:84-95`, `:53-61`, `:28-49`, `:491-494`, `:911` | a detached `std::thread` releases the media player and deletes the `VideoContext` whose two mutexes VLC's thread locks and whose `component` the `display` callback reads; `ctx->component = nullptr` written on the interface thread with no lock against that read; the slice's only thread and only detach; outside the lanes | Q4 |
| L-11 | `OptionListComponent.h:96`, `:145`, `:158`, `:195`; `:310-311`, `:323-324` | `delete this` from inside the popup's own row handlers, its BACK button and its `input`: the button-bar trap's shape; sound at the pin because each is the lambda's last statement and the component touches nothing after the callback returns (T31's invariant, § 1 d), and every option row in the fork's pages goes through it | Q4 |
| L-12 | `TextEditComponent.cpp:39`, `:47` | the slice's two `postToUiThread` capture raw `this` (`startEditing`/`stopEditing` on focus); a text edit destroyed before the post runs is a use after free; what `Window::postToUiThread` promises is T35's, `AppWindow`'s gate T33's | Q4 |
| L-13 | `CarouselComponent.cpp:354-361`; `OptionListComponent.h:639-640` | a carousel with one entry offers `CHOOSE` for a direction that moves nothing (type decides, not `size()`); an option list with one value offers `CHANGE`; `ComponentList:555` and `ComponentTab:327` check `size() > 1`; the grid asks the cursor (D-UI-034); upstream surfaces | Q3 |
| L-14 | `GridTileComponent.cpp:1043`; `ImageGridComponent.h:2`, `:380-381` | indentation one level off (`:1043` deeper, `:380-381` shallower than their blocks); `#include <functional>` above the include guard; reads as a block it is not in | Q7 |
| L-15 | `MenuComponent.cpp:506-515`, `:492-503`; `guis/GuiMenu.cpp:591` | `setCursorToButton` casts `mButtonGrid` to `ComponentGrid` while `setButtonGrid` accepts any `GuiComponent` and the MAIN MENU hands it a text; the cast never runs there only because `mButtons` is empty and the index guard `:508` returns first -- an invariant nothing states | Q3 |
| L-16 | `SwitchComponent.cpp:14`; `OptionListComponent.h:255`, `:276`; `TextEditComponent.cpp:31`; `MenuComponent.cpp:393`; `TextListComponent.h:613`, `:725` | seven more constructor or layout reads of `Font::getHeight` (L-02's moving number) in upstream components the fork's pages are built from | Q1 |
| L-17 | `TextComponent.cpp:338` against `:350` | the auto height is measured at `getSize().x()` and the text drawn at `mSize.x() - padding`; a wrap in that band paints a line the height never budgeted (#48; `es-code-traps.md:91`); unchanged at the pin; `GuiMsgBox` works around it, nothing else does | Q1 |
| L-18 | `MenuComponent.cpp:205`, `:233`, `:236`, `:283`, `:487`; `ButtonComponent.cpp:73` | every group label, entry label, title and button name is `toUpper`ed by the component (D-WORKFLOW-144: the brand is never uppercased through a formatter); at the pin no fork label carries `pixelelated` through these (the digest's grep: 7 lines in `es-app/src`, the two on-screen ones `guis/GuiMenu.cpp:1999` and `main.cpp:929` go round them), so the guard is a reading, not a check | Q6 |
| L-19 | `AsyncNotificationComponent.cpp:63-65` | `max(sizeText(30 chars), 0.9W)`: the measured floor never binds on a panel 640 or wider, so the card is 0.9 W everywhere and the comment's "floor" is dead text; harmless | Q2 |
| L-20 | `VideoComponent.cpp:327`, `:591`; `ImageComponent.cpp:1232` | cached `exists` on media the scraper writes while ES runs: a video or image scraped mid-session reads as absent until a game launch clears the cache (`es-native-ui.md:107`); upstream surfaces | Q5 |
| L-21 | `WebImageComponent.cpp:239-243`; `es-core/src/HttpReq.cpp:119-123`, `:131-132`, `:172-176` | a stack `HttpReqOptions` handed by pointer to a heap `HttpReq`: sound, the constructor consumes `outputFilename` and `customHeaders` before returning; recorded so the next reader does not re-derive it | Q4 |

**The neighbours, and whose they are:** `es-core/src/guis/` (`GuiMsgBox`,
`GuiTextEditPopup`, `GuiTextEditPopupKeyboard`, `GuiInfoPopup`,
`GuiInputConfig`, `GuiDetectDevice`; `GuiLoading.h` is
`es-app/src/guis/`'s, T31's by the block), `Window.cpp` (`renderAsyncNotifications` positions the card
every frame; `postToUiThread`; `renderHelpPromptsEarly`; the one floating
surface at a time, D-UI-093), `ThemeData.cpp` (`GridTextProperties::multiLine`
declared `:267`; 13 include lines of slice headers, the top including
file), `GuiComponent`, `InputConfig.cpp` (`buttonLabel` `:353-366`),
`InputManager`, `watchers/WatchersManager.cpp`, `Scripting.cpp` and
`es-core/CMakeLists.txt` are **T35's** (#682); `resources/Font.cpp`
(`getHeight` `:754-756`, `getGlyph` `:420-421`, `mMaxGlyphHeight` `:107`),
`resources/TextureResource.cpp` (`:100-131`, a path is a cache key for the
texture's lifetime), `resources/TextureData.cpp` (`:331`, `:339`, `:410`,
#1263's es-core half), `utils/FileSystemUtil.cpp` (the `exists` cache
`:144`, `:203-220`, its erase `:185-195`, `getFileSize` `:1319-1335`) and
`utils/OfflineProxyUrl.{h,cpp}` are **T36's** (#683); `HttpReq.{cpp,h}`,
`Settings`, `SystemConf` and `utils/AtomicFileUtil` are **T21's** (#668);
`es-app/src/CloudText.{h,cpp}` (`chooseThatFits` `:672-685`) and the cloud
threads are **T18's** (#665); `ProxyCards`, `ThreadedHasher` and
`OfflineAchievements` **T20's** (#667); `guis/GuiMenu.*` **T26's** (#673);
every other page under `es-app/src/guis/` **T31's** (#678); the views and
`ScraperSearchComponent`'s pages **T32's** (#679); `AppWindow.h`,
`ScraperSearchComponent.cpp` and the game list **T33's** (#680). **274
include lines in 112 files outside the slice name a slice header** (215
`es-app`, 58 `es-core`, 1 `tests`: `tests/app-unit/ProxyCardsTests.cpp`),
`MenuComponent.h` 32, `TextComponent.h` 24, `OptionListComponent.h` 22,
`ComponentGrid.h` 21, `BusyComponent.h` 17, `NinePatchComponent.h` 16,
`ImageComponent.h` 16, `SwitchComponent.h` 15, `MultiLineMenuEntry.h` 12,
`ButtonComponent.h` 12, `AsyncNotificationComponent.h` 11; three headers
have no outside includer (`ScrollbarComponent.h`, `GridTileComponent.h`,
`AnimatedImageComponent.h`, reached from inside the slice). Within the 80:
389 include lines, 352 quoted over 91 distinct headers (`GuiComponent.h` 28,
`Settings.h` 20, `ThemeData.h` 19, `LocaleES.h` 18, `utils/StringUtil.h` 17,
`renderers/Renderer.h` 13, `components/TextComponent.h` 13, `Window.h` 13,
`resources/TextureResource.h` 12, `components/ImageComponent.h` 12, `Log.h`
12, `resources/Font.h` 11), 37 angle-bracket (`<SDL_timer.h>` 3,
`<SDL_mutex.h>` 2, `<SDL_power.h>` 1, `<vlc/vlc.h>` 1,
`<vlc/libvlc_version.h>` 1, `<Windows.h>` 1, `<wait.h>` 1, the rest
standard library), **1 to es-app** -- one direction of a dependency taken
as given, not as a finding, except the one line L-07 names.

**Already found; do not re-find; take up.** Each is cited at its lines in
`02` with a disposition; the states are as the inherit digest read them on
2026-10-27, re-read at stage A; a ruling the table names by letter is
§ 1's. The audit folders are § 3 item 8's.

| Found by | Lines at the pin | Take up as |
| --- | --- | --- |
| T32 PL-07 / #1263 (OPEN, `bug`; `02:362`, `05:474`, retro `:59`, `:82` *"For the es-core slice"*) | `resources/TextureData.cpp:331`, `:339`, `:410` (T36's); the caller `ImageComponent.cpp:408` | the caller's half, Q5 (§ 1 a); the cache's half named for T36 |
| T2 PC-1 (`02:178`, `:211`, `04:142`, `05:612` *"T35/T18"*); T33's brief `:649` | `AsyncNotificationComponent` held raw by `ProxyCards.cpp:125-190`, `:381-389`, `:218-222` and `ThreadedCloudSync`; `main.cpp:1358` `window.deinit()`; `delete this` at `ThreadedCloudSync.cpp:757` | the component's half, Q4 (§ 1 b); no issue exists, the lane files one if the read proves the window |
| T26 L-02 / #1221 (OPEN, fixed on T26's branch `aca4076c5`; `02:31`, `:810`) | `ImageComponent.cpp:408` with `resources/TextureResource.cpp:100-131` | the component contract (a path is a cache key for the texture's lifetime) stated in `02`; Q5 |
| T26 PL-27 (withdrawn, D-WORKFLOW-209; `05:401-411`, `:479`) | `SwitchComponent` / `OptionListComponent` `setOnChangedCallback` sites `guis/GuiMenu.cpp:5651`, `:5658`, `:7301`, `:10097`, `:10133`, `:10182`, `:10201`, `:10220` | the callback type's design, Q4 (§ 1 c); LeakSanitizer over an extracted builder is the named proof |
| T31 L-03 / #1243 (OPEN, fixed on T31's branch `82f80693d`; `02:406`, `04:80`) | `OptionListComponent.h:310-311`, `:323-324` | the invariant stated in `02` and kept, Q4 (§ 1 d) |
| T31 `02:643`; #63 (OPEN), #65 (OPEN); `es-native-ui.md:138-141`; menu map `:707` | `ComponentTab.cpp`, `MenuComponent.cpp:115`, `:144`; the four self-routing pages `GuiThemeInstaller`, `GuiBatoceraStore`, `GuiKeyMappingEditor`, `GuiKeyboardtopads` | the component half of #65 proved with G-05's frames; the pages are T31's and upstream's (D-UI-079); the ruling on closing #65's half is the pause's |
| T31 L-26 / #1245 (OPEN, fixed `95852f873`; `02:429`, `04:205`) | `HelpComponent` draws the bar; `renderHelpPromptsEarly()` is `Window`'s | read; the checker proposal is the coordinator's, not T34's |
| T31 retro `:81`, T26 `02:828`; `es-code-traps.md:22` | `MenuComponent::clearButtons()` `:478-483` destroys the running callback | the rule restated in `02` beside the lines; no component-side guard exists, said so |
| T32 S4 / #1266 (OPEN, `bug`, fixed `1655e2f4c`; `02:436`, `05:474`); #207 (CLOSED) | `ImageGridComponent.h` `clear()` / `resetGrid()` | the grid's contract after `clear()`, Q4 (§ 1 e); T32's `s4-views.py` the harness shape |
| T32 PL-16 (`05:331`), T31 PL-26 (`02:645`, `05:507`) | `GridTileComponent` under a tile decorator computing `DisplayAspect::forScreenshot` per tile (`GridGameListView.cpp:42-46`, `forScreenshot` `:44`; `:131-153` is `getImagePath`) | recorded; not reached on the shipped theme (T32 G-02); G-08 asks the image |
| T32 PL-10 / #1265 (OPEN, fixed `1655e2f4c`) | `HelpComponent` (what the bar shows); `updateHelpPrompts()` on a cursor change | read; the fix is the views' |
| #585's comment from #1116 / UI-02; #48 (CLOSED); `es-code-traps.md:91` | `TextComponent.cpp:338`, `:350` | Q1 (§ 1 f): the reproducer and frames; the root fix a stage-D ruling |
| #182 (CLOSED, `bug`; ES `d9fa93bf2`) | `ComponentList.h:23-26`, `SwitchComponent.cpp:30`, `:33`, `MultiLineMenuEntry.cpp:84`, `:89` | the dim mechanism the cloud rows and T20's SCAN GAMES row depend on; G-04's frame |
| #325 (CLOSED, `bug`; ES `f1ae6bc25`) | `MenuComponent.cpp:115`, `:144` | G-05's wrap |
| #210 (CLOSED, `bug`; ES `7dc8bf373`) | `HelpComponent.cpp:98-110`, `:118-127` | 3.16's case; G-03's and G-11's bars |
| #27 (CLOSED; D-UI-050; ES `2088eadb9`) | `GridTileComponent` `GridTextProperties::updateTextComponent` | read; G-08 if a grid theme exists |
| #243 (CLOSED; `es-code-traps.md:164`) | `ImageComponent::setMaxSize`, `resize` | 3.22, 3.23's cases |
| #157 (CLOSED, D-UI-108; T18 `02:209`) | `AsyncNotificationComponent` has no animation; the two-half bar is `ThreadedCloudSync.cpp:186-196` | read; G-02's frames |
| #1112 (OPEN, `enhancement`, M7.P5) | `BusyComponent` asks for a contrast edge where D-UI-016 forbids a drawn border | read-only context; T34 does not re-decide D-UI-016 |
| T21 L-11 / #1199 (OPEN, fixed `ba0e82c1f`) | `TextEditComponent.cpp:176-189`, `input()`'s RETURN branch ending in `stopEditing()` `:184` (no `applyChanges` at the pin) | read; the guard is `SystemConf`'s |
| T21 PL-26 / Backlog #1192 (OPEN) | the popups' masking mode (es-core `guis/`, T35's); the field is `TextEditComponent` | read; a masking mode on the field is named for T35's pause if T34's read finds the field is where it belongs |
| T18 `02:61`; T33's brief `:1194` | `tests/app-unit/fakes/components/AsyncNotificationComponent.h` (24 lines) doubled by two lanes' builds | a header change named as a collision (§ 1 j) |
| T20 `02:74` | SCAN GAMES FOR OFFLINE ACHIEVEMENTS, a `MultiLineMenuEntry` dimmed by gates with a hidden 1 s refresher (`GuiRetroAchievementsSettings.cpp:282-305`) | blindspot 44's shape; 3.4's case is the proof (G-07 `CANNOT`) |
| T31 `02:214`, `:231`, `:232` | `addWithDescription`'s func form (`multiLine = false`) at `GuiBluetoothDevices.cpp:60`, `GuiGamelistOptions.cpp:77`, `:174` | Q2's per-frame cost (`es-ui-style-guide.md:96`) |
| the inherit digest's § 6 item 9; `a8fe371b0a` | `es-ui-style-guide.md:202` read *"minutes"* for the card against D-UI-078 | fixed today by the coordinator; the lane reads the row as it stands |
| #585 (OPEN) | its body and comments name `TextComponent.cpp` once (#1116's comment); none of the fork's six candidates | the lines T34 owes start with the upstream-delta digest's six candidates (Q7) |

## 3. Read first

In this order, each read in this session, and `01-research-notes.md` says
which were read (`working-principles.md` § Pre-flight):

1. **The rules**, each at the section named, with the question it serves;
   the section's own sentence is not repeated here -- open it (the line
   numbers are the coordinator worktree's at `a8fe371b0a`, by `grep -n
   '^## '`):

   | Rule | Line | Section | Serves |
   | --- | ---: | --- | --- |
   | `es-code-traps.md` | `:22` | Never rebuild a button bar from inside one of its buttons | Q4 (`clearButtons` `:478-483`; `OptionListComponent.h`'s four `delete this`) |
   | | `:56` | `BusyComponent::setText("")` is a no-op (the rclone section's last bullet) | Q6 |
   | | `:60` | Comments near a translatable string must be ASCII | Q7 (`VideoVlcComponent.cpp:859`), § 9 |
   | | `:79` | The help bar offers a direction only where it moves something (D-UI-034) | Q3 |
   | | `:91` | TextComponent measures at its full width and draws at its padded one | Q1 (L-17, 3.5) |
   | | `:104`, `:118`, `:127` | Three things a font is not: `Font::get` scales; `getHeight()` is the tallest glyph so far; `exists` caches | Q1 (L-02, L-16), Q5 |
   | | `:136` | the window paragraph: `renderHelpPromptsEarly()` | Q3 |
   | | `:139` | Pure text has a home, and a test | § 5 (every unit case's shape) |
   | | `:164` | The picture beside a game list is the theme's own extra | Q5 (`ImageComponent::resize`, `applyToBoundImages`) |
   | | `:191` | A rescan that deletes FileData drops the view first | Q4 (#1266's grid) |
   | | `:238` | A pooled connection with the link gone | Q5 (`WebImageComponent`'s `HttpReq`) |
   | | `:266` | A taller GuiSettings menu keeps its old top offset: verify in 640x480 and 1280x800 frames | § 5 (G-03, G-11) |
   | `es-native-ui.md` | `:32` | The other files that carry the interface law (D-UI-039) | Q7 |
   | | `:76` | Dim, don't hide (alpha `0x50`); a button is gated by existence | Q2 (G-04) |
   | | `:81`, `:94`, `:107` | Core patterns: the card for fast work only (D-UI-078); a file another process writes is read uncached | Q4, Q5 |
   | | `:121` | Tabbed pages: the strip is a focus stop (D-UI-021); do not route a direction key from everywhere | Q3 (G-05) |
   | | `:175`, `:179`, `:191`, `:199-210`, `:289`, `:299` | Spacing: the bar's gap; the card's width and position; the four surface tiers; the card's opacity; fractions never pixel constants | Q2 |
   | | `:302`, `:318` | Images in a menu row are themed as text; `UntintedImageComponent` | Q5, Q7 |
   | | `:324` | A layout must not be computed from what it last produced (blindspot 44) | Q1 |
   | | `:377` | Anti-patterns: two surfaces for one event; a transient-only report | Q6 |
   | | `:405` | Before the pin moves, the compiler has seen the edit (`tools/es-syntax-check`, exit 2 here) | § 5, § 9 |
   | `es-ui-style-guide.md` | `:32` | Keep the flow and its visual evidence together | § 5, § 7 |
   | | `:68`, `:70`, `:88` | Rows: the seven builders; sliders render `value+suffix` with no space | Q3, Q6 (3.7, G-09) |
   | | `:95-109` | The `multiLine` trap: which overload decides; `false` forces per-frame updates | Q2 |
   | | `:118-120` | Size by weight: the three type sizes | Q6 |
   | | `:136` | Dim, don't hide: `(color & 0xFFFFFF00) \| 0x50` | Q2 |
   | | `:144`, `:164` | Text: the component upper-cases four of eleven cases; placeholders `AUTO`, `NONE`, `<NOT SET>` | Q6 (L-18, 3.7, 3.13) |
   | | `:171`, `:178` | Confirmations: YES first; back lands on `NO` or `OK`, else on the last button | Q3 (G-03) |
   | | `:197-204` | Waiting: the card row as fixed at `a8fe371b0a` (seconds, fast work only) | Q2 |
   | | `:232` | Buttons: BACK last; gate by existence | Q3 |
   | | `:306`, `:312` | Known inconsistencies: `MenuComponent::addEntry` and `GuiSettings::addEntry` swap parameters 5 and 6 | Q7 |
   | `es-player-text.md` | `:25` | the brand stays lowercase (D-WORKFLOW-144) | Q6 (L-18) |
   | | `:29`, `:31`, `:135` | Conventions: every label through `_()`; a toast is one line at 0.9 of the screen | Q6 |
   | | `:141` | Every fork string ships in English and French (D-UI-051) | Q6, § 9 |
   | | `:211`, `:236` | Outcome words; the outcome vocabulary (D-UI-028, D-UI-035's candidates) | Q6 (the card's rows) |
   | `engineering-practices.md` | `:12` | Change stays inside the fork's lanes (D-UI-079) | every Q |
   | | `:28` | Check upstream early (D-WORKFLOW-162): batocera's eight, the `setOpacity` guard | Q7 |
   | | `:83` | Verify design intent (`git log -S` before each FAIL-at-pin lead) | § 4, § 5 |
   | | `:111` | Verify the artifact, not the report | Q5 |
   | | `:194`, `:250` | A name is not a behaviour; a total is the tool's line | § 5 (the `TOTAL:` line) |
   | | `:419`, `:478`, `:548` | Guards must fail closed; `rc=$?` on its own line; the first PASS is the one to distrust | § 5 |
   | | `:576` | Before deleting a duplicate, diff its behaviours | Q7 (L-05's second copy is not deleted here) |
   | `bugs-are-agent-first.md` | `:41`, `:53`, `:76` | The three classes; The rules; rule 6 | every bug |
   | `issue-tracking.md` | `:129`, `:180` | A criterion is agent-first (D-QA-044); Ticking an acceptance criterion | § 7 |
   | `upgrade-and-install.md` | `:40`, `:58`, `:74` | Fixing forward is not enough; the `Already written:` line (D-WORKFLOW-050) | every bug (a component writes no file: `Already written:` is argued as *nothing inherited* unless `WebImageComponent`'s cache is the subject) |
   | `generic-x64-vm-testing.md` | `:100`, `:108-114`, `:215`, `:221-222` | Headless: `run --headless --daemonize`, `tools/vm-serial`, the pidfile; `--res 640x480` is a flag (#1141), a second size is a second boot | § 5 |
   | | `:325` | A launch, a START or a walk waits for `/isIdle` (D-QA-057) | § 5 |
   | | `:365`, `:382`, `:393` | The first key after five idle minutes only wakes; a restarted ES comes back on the last game list; `screendump` can serve the previous ES's last frame | § 5 (G-05, G-08) |
   | | `:448-458` | Frame at the handheld's size: a UI change is framed at 640x480 before it is called done | § 5 (every frame) |
   | | `:486` | `dismiss-dialogs` ends on the carousel where it was | § 5 |
   | | `:959` | Automated visual QA (`tools/vm-visual-qa`) | § 5 |
   | | `:1145` | A settings change from the shell is invisible to the running interface (`essway.service` stopped first) | § 5 (G-08) |
   | | `:1432` | The guest is the candidate image, not the read tree | § 5 (every frame's side) |
   | `player-language.md`, `least-surprise.md`, `time-to-play.md` | whole | | Q2, Q6, § 6 |

2. **The register.** The rows that name a file or behaviour here (the
   coordinator's branch at `a8fe371b0a`; the line is the table's): D-UI-007
   `:38` (a placeholder never looks like a value), **D-UI-012** `:44`
   (`BUTTON_GRID_HORIZ_PADDING` 0.022, defined once; labels one word),
   **D-UI-016** `:56` (no drawn border; `NOTIFICATION_OPACITY` 255),
   **D-UI-021** `:78` (the strip is a focus stop), D-UI-023 `:96` (two lines
   per row), D-UI-024 `:102` (the transfer page's seven fitted lines),
   **D-UI-034** `:167`, **D-UI-035** `:168` (candidates, longest first),
   D-CLOUD-098 `:189` (time to play), D-UI-039 `:190`, **D-UI-050** `:246`
   (the tile label wraps outright), D-UI-051 `:251`, D-UI-058 `:301` (the
   clock's 12-hour rule), **D-UI-078** `:344`, **D-UI-079** `:345`,
   **D-UI-093** `:404` (one floating surface at a time), D-UI-107 `:432`,
   D-UI-108 `:433`, D-WORKFLOW-137 `:589`, **D-WORKFLOW-144** `:604`,
   **D-WORKFLOW-162** `:690`, D-WORKFLOW-187 `:722`, D-WORKFLOW-189 `:723`,
   D-WORKFLOW-195 `:728`, **D-WORKFLOW-209** `:746`, D-UI-128 `:756`,
   D-UI-129 `:757`; by ID only D-WORKFLOW-188 (the P1 branch's), D-UI-042,
   D-UI-045, D-WORKFLOW-155/156, 164/165. **The highest IDs the register on
   the coordinator's branch names at this version are D-CLOUD-186 (`:755`),
   D-UI-128 (`:756`) and D-UI-129 (`:757`), after D-WORKFLOW-212 (`:753`)
   and D-NET-017 (`:754`)**; `## Open decisions` opens at `:759`;
   `tools/register-check` is the proof. The lane reads the card, bar, strip
   and dim rows by `tools/archaeology 'button bar'`, `'progress card'`,
   `'tab strip'` and `'dimmed'` before calling anything pending.
3. **The menu map** (`docs/es-menu-map.md`, 989 lines): `:128` (the
   `addGroup` headers are the real IA), `:139` (SCRAPER: tabbed, SCRAPE ·
   OPTIONS · ACCOUNTS, G-05's strip), `:253` (the line under a launching
   row), `:378` (a transfer runs on a page since D-UI-078), `:567-568` (A
   confirms, YES first; a help bar that lies), `:596-597` (the SCAN row's
   two dimmed states), `:660-664` (the surface tiers against the data
   tiers), **D-UI-039 at `:668`**, **`## Not mapped` `:677`** (`:699`
   SCREENSAVER SETTINGS, `:707` KEYBOARDTOPADS and #63), the visual-evidence
   section `:26-82`. **The components have no page of their own, so the map
   has no row for this slice to add**; `tools/es-menu-map-check:54-55`
   reads `MenuComponent(window, _("TITLE"))` constructor calls in es-app as
   screen titles, the one fork tool that names a component, and it misses a
   title set in a member initializer (#951, #965) -- so the checkbox in § 7
   is worded on the rows a stream adds, with the checker's line quoted, red
   if the checker cannot see them.
4. **The blindspots** (`docs/blindspot-register.md`, 1,250 lines; the
   inherit digest's lines at `045dfe80df`, unchanged since -- the diff in
   the header): 4 (`:13`: `close()` inside a page's own handler), 5
   (`:14`: `MenuComponent` upper-cases row titles), 35 (`:208`: the card
   composed a third row it had no row to draw on), 41 (`:378`: verified at
   a size no handheld has; `Font::get` scales under 720 px), **44**
   (`:445`: `layoutRows` measured from the cells it had set; hundreds of
   refreshes), 49 (`:590`: an edit made blind to the compiler), 54 (`:720`:
   a measurement on a guest whose renderer was not the device's), **75**
   (`:1206`: a corpus read on the wrong tree -- every count at the hash).
5. **The tests at the pin.** § 5 item 1 describes what exists; read whole
   before a case is written: `es-app/tests/unit/README.md` (`:12-13`,
   `:44-46`: *"functions that read nothing, ask nothing and draw nothing"*),
   `es-app/tests/unit/CMakeLists.txt` (`:36-65`, `:62-64` the three es-core
   sources it links: `utils/StringUtil.cpp`, `utils/TimeText.cpp`,
   `utils/OfflineProxyUrl.cpp`), `CloudTextTests.cpp:832-854` and
   `:1597-1598` (`chooseThatFits`, the model), `tests/app-unit/CMakeLists.txt`
   (`:31` the sanitizer flags, `:35-42`), its nine doubles under
   `tests/app-unit/fakes/` (`Window.h` carries `postToUiThread`;
   `components/AsyncNotificationComponent.h` is the double of this slice's
   header), `tests/gpu-governor-save.py:14`, `:26-29` (four
   `OptionListComponent.h` methods lifted as text; T31's `s0-pin-checks.txt:20`
   `gpu-governor-save rc=0: PASS fallback`), `tests/cloud-oauth-lifetime.py`
   (the ASan lifetime shape, 3.19), T32's `stage-e/s0-syntax-pin.txt` (the
   stand-in check's whole record at this pin: twelve es-app files `rc 0`,
   `SystemView.cpp:469:92: error: 'SDLK_r' was not declared` -- the fake
   `SDL_keyboard.h` is partial).
6. **The walks and the frames.** `tools/vm-walks/README.md:13-37` (the
   step vocabulary: `settle`, `wait-for-change`, `wake`, `dismiss-dialogs`),
   `:144` (*"`up` from a page's first row lands on its BACK button before it
   wraps to the last row"*, the grid wrap this slice owns), the 18
   top-level `*.steps` (22 with `docs/`; `to-manage-cloud-storage.steps` for G-04,
   `ui-settings-toggle.steps` for the vocabulary, `wake.steps` whose one
   step is `wake`), `suite.txt:77` (`default-pre`, which stops `essway` and
   seeds the settings before every walk's reboot), `claims.txt:30`
   (`d72084ccad run-transfer-frames/08-t05.png 584 740 696 768 #308`, the
   help bar's one accepted claim), `masks.txt` (the clock's minute at
   `1110 36 1215 64`; the transfer page's three rectangles).
7. **The French**: 22 `_("` lines in 12 of the 80 files, 27 occurrences, 17
   distinct msgids, every one with a non-empty French `msgstr` at the pin
   (§ 2); the fork's one msgid `SWITCH TAB` at po `:4929-4930`; `up/down`
   at po `:3708-3709` (L-01); `"Auto"` at `SliderComponent.cpp:282` outside
   `_()` (3.7); `tools/es-untranslated` is the count over the whole tree,
   and its two lines at this pin are T33's brief's (`706 fork string(s) in
   the source, 706 with French, 0 without` against `bccd715707`, `703 ...
   703 with French, 0 without` against `cada856d86`), unchanged by this
   slice since it adds no msgid T33's run did not count; the tool sees only
   `_("...")` literals, so `"Auto"` is invisible to it.
8. **The audits**, each on its lane's branch and in its folder, named here
   once and cited by section elsewhere: **T2** `origin/feature/m6-es-launch-path-649`
   (`7041b0d71036`; ES `55158d2a64`), `docs/audits/2026_10_23-epic-m6-es-launch-path/`
   (`02:178`, `:211`, `04:142`, `05:612`); **T18** `origin/feature/m6-es-cloud-pages-665`
   (`6a560b9fbd12`; ES `d55235d4b3`), `docs/audits/2026_10_26-epic-m6-es-cloud-pages/`
   (`02:61`, `:209`); **T20** `origin/feature/m6-es-achievements-pages-667`
   (`ffb6b686cbd4`; ES `5c0ddaaeef`), `docs/audits/2026_10_26-epic-m6-es-achievements-pages/`
   (`02:74`); **T21** `origin/feature/m6-es-state-and-bridge-668`
   (`82c67e99c572`; ES `3ae9610b0f`), `docs/audits/2026_10_26-epic-m6-es-state-and-bridge/`
   (`02:50`, `05:220`, `:509`, `stage-e/syntax-check.sh:12-16`); **T26**
   `origin/feature/m6-es-guimenu-673` (`bcfad2144bc8`; ES `757f5370ea`),
   `docs/audits/2026_10_27-epic-m6-es-guimenu/` (`02:22`, `:31`, `:810`,
   `:828`, `05:401-411`, `:479`); **T31** `origin/feature/m6-es-pages-678`
   (`6ec4dda2035d`; ES `95852f8736`), `docs/audits/2026_10_27-epic-m6-es-pages/`
   (`02:214`, `:231-232`, `:406`, `:429`, `:643`, `:645`, `04:19`, `:80`,
   `:147`, `:205`, `05:507`, retro `:81`, `tools/t31-build-tests.sh`,
   `stage-e/fakes/` (13 headers: `FreeImage.h`, `SDL.h`, `SDL_audio.h`,
   `SDL_events.h`, `SDL_joystick.h`, `SDL_keyboard.h`, `SDL_main.h`,
   `SDL_mixer.h`, `SDL_mutex.h`, `SDL_timer.h`, `alsa/asoundlib.h`,
   `curl/curl.h`, `ft2build.h`)); **T32** `origin/feature/m6-es-app-views-scrapers-679`
   (`1dd3093853d4`; ES `b52245036f`), `docs/audits/2026_10_27-epic-m6-es-app-views-scrapers/`
   (`02:362`, `:436`, `:437`, `05:222-234`, `:331`, `:474`, retro `:59`,
   `:82`, `tools/t32-build-tests.sh`, `stage-e/s0-syntax-pin.txt`,
   `stage-e/handback-checks.txt:45` `TOTAL: 225 test cases in 4 binaries`,
   `02` § What T33 to T37 inherit at `:479`); **T33**
   `origin/feature/m6-es-app-system-680` (`0ee735862d6a`, ES `dd86d7ce20a5`
   at the proof's read, 2026-10-30), in flight -- its `02` § What T34 to T37 inherit (its
   brief's § 5 item 3: the provenance table, the cached-read table, the
   write table, the thread table, the bounds table, the `app-unit-tests`
   recipe) read at dispatch if it has landed, else mid-run when it does.
   Read with `git show <branch>:<path>`, never a checkout.
9. **The issues**: #681's own body; #63, #65, #27, #48, #115, #157, #180,
   #181, #182, #199, #207, #210, #241, #243, #245, #250, #325, #349, #436,
   #585, #951, #965, #1112, #1116, #1137, #1138, #1141, #1192, #1199,
   #1221, #1243, #1245, #1263, #1265, #1266; #700, #679, #680. States as
   read on 2026-10-27 after 19:04 UTC: #681 OPEN with 0 comments; #63, #65,
   #585, #1112, #1116, #1192, #1199, #1221, #1243, #1245, #1263, #1265,
   #1266 OPEN; #27, #48, #157, #181, #182, #207, #210, #325 CLOSED; #649,
   #665, #667, #668, #673, #678, #679 OPEN until the integration merge
   (§ 1); #680 OPEN, in flight. The lane re-reads each with `gh issue view`
   at stage A and records the states it saw.
10. **Time to play**: `docs/vm-qa-log.md:9-18` (the three headline columns;
    *"no budget row exists yet"*); `time-to-play.md`'s one budget (the exit
    sync's 3 s, D-CLOUD-119). This slice is on both paths at every frame
    rather than at a point: `ComponentList::render` re-tints every element
    every frame (`:321`, `:391-400`); a `multiLine = false` description
    forces the whole list into per-frame updates
    (`es-ui-style-guide.md:96`; T31's three func-form rows); the card's
    `render` measures under `mMutex` only when candidates change; the first
    grid view walks `calcGridDimension` per resize. The retro's line names
    what the slice costs between a press and its frame on the guest, never
    "nothing".

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of the families the earlier ES briefs
used -- **a layout computed from what it last produced or from a moving
number**, **a house constant a surface does not keep**, **a prompt offered
where the key moves nothing**, **a lifetime or a thread**, **a read of a
file another process writes**, **a player sentence outside the vocabulary
or without its French**, **a structure or merge-debt fact** -- with the
lens, cost against value, asked of every upstream surface: what it costs
the player (a frame's work, a wait, a thread) against what it gives. The
leads are § 2's L-01 to L-21, cited here by number (their lines are the
table's and are not restated), and the floor's pure leads tabled at the end
of this section; each is read at its lines before it is called anything,
and the seven that FAIL at the pin (§ 5) get their `git log -S` first
(`engineering-practices.md:83`); the upstream surfaces outside the lanes are
§ 1's list, read and recorded, fixed only under rule 6 (D-UI-079).

- **Q1 Layout: computed from what it last produced, or from a moving
  number** (`es-native-ui.md:324`; `es-code-traps.md:91`, `:118`;
  blindspot 44; D-UI-050; the layouts run). **L-03**: 3.4's case,
  `rowPercs(26, 20)` and `(20, 26)` seen to FAIL at the pin (the sum is not
  1), the `git log -S` of the 0.9/1.1 first, the contained fix a pair of
  percentages that sum to 1 (or the second row the remainder); G-07 is
  `CANNOT`, 3.4's 300 `setDescription` calls are the hundreds the rule
  asks for. **L-02** and **L-16**: the eight constructor reads of
  `Font::getHeight` tabled with what each sizes and whether a page reopened
  after its tallest glyph has drawn differs from its first paint; the proof
  is a read trace and a 640x480 frame pair (G-05's page opened twice); the
  disposition a rasterise-first (`font->sizeText(<ASCII 32..126>)`,
  `es-code-traps.md:118`) in the component or a record, ruled at the pause.
  **L-17**: 3.5's case on `onTextChanged` with a `Font` double (padding 32
  px on a 640 px box, a word at the wrap point: the measured height one
  line short), a 640x480 frame of a padded auto-height text that is not a
  `GuiMsgBox`, and the reproducer written into `02` for #585's line; the
  root fix is the pause's (§ 1 f). **3.6** (`TextComponent.cpp:486`'s
  `mPadding.y()` twice): the case seen to FAIL, the lines `:480-500` read
  whole first (the stub checked against the unfixed code,
  `engineering-practices.md:464`), a contained one-token fix under rule 6
  and a #585 line. A table: every size in the 80 computed from a size the
  pass wrote (the rule's shape) and every layout read of `Font::getHeight`,
  with the surface that shows it.
- **Q2 The house constants, and the surfaces that keep them**
  (`es-native-ui.md:175-299`; `es-ui-style-guide.md:136`, `:197-204`;
  D-UI-012, D-UI-016, D-UI-078; `time-to-play.md`; the constants run).
  **`BUTTON_GRID_HORIZ_PADDING` 0.022** (`MenuComponent.cpp:14`): G-03's
  14 px at 640 and G-11's 28 px at 1280 measured in the frames' columns;
  **L-04**: 3.26's case (`makeButtonGrid`'s widths: four 128 px buttons at
  640 fit, five do not) and the arithmetic per candidate page at 640 (the
  14 + 4 + 3 + 3 `addButton` sites named), the widest bars framed on the
  guest, the disposition (a bar that fits its cell, or the pages' labels)
  ruled at the pause; **L-05**: the second copy at
  `GuiTextEditPopupKeyboard.cpp:14` recorded against the comment's "one
  place" (the popup is T35's; the comment is this slice's to correct or the
  claim to keep); **L-19**: the dead floor, recorded. **`NOTIFICATION_OPACITY`
  255, 0.9 W, centred** (`AsyncNotificationComponent.cpp:31`, `:64`,
  `:112`): G-02's pixel reads (edges at x 32 and x 608; a panel-colour
  pixel over box art, not a blend); the agreement with `Window.cpp:1183`,
  `:1192` cited from T35's file, not re-read. **`DIMMED_ALPHA` 0x50**
  (`ComponentList.h:25-26`): G-04's luminance ratio over the same panel;
  **L-06**: the 20 px inset at both sizes framed, recorded as upstream's
  constant the fork exposed, the fraction a pause ruling. **The pixel
  constants in nine upstream sites** (`ComponentList.cpp:11`,
  `TextEditComponent.cpp:8-9`, `:31`, `ButtonComponent.cpp:10`,
  `GridTileComponent.cpp:56`, `.h:148`, `MenuComponent.cpp:167`, `:192`,
  `VideoVlcComponent.cpp:782`, `NinePatchComponent.cpp:177`, the `-32`
  nine-patch corner in four files): tabled against `es-native-ui.md:299`,
  each with the panel it is right on; outside the lanes unless a fork page
  reads it (L-06). **The per-frame cost** (`es-ui-style-guide.md:96`): the
  three func-form rows T31 listed, `ComponentList::render`'s re-tint, and
  the card's `render`, each priced in the retro from the guest (a frame
  time read from `tools/vm-visual-qa`'s `settle` is the only number the
  harness gives; a `CANNOT` with that reason is allowed). A table: every
  house constant, its one definition, every site that reads it, and the
  frame that shows it.
- **Q3 Input and the help bar** (`es-code-traps.md:79`, `:136`; D-UI-034,
  D-UI-021; `es-ui-style-guide.md:171`, `:178`, `:232`; menu map
  `:567-568`; the input run). **`canMoveCursor`**: 3.1 to 3.3's cases (the
  `GuiMsgBox` shape false in all four; the Nx2 button row left/right only;
  `(0,0)` false), G-06's OK-only dialog reading `OK` and no `CHOOSE`, and
  G-03's YES/NO box reading exactly one. **The strip's focus stop**:
  G-05's four frames (the selector bar over SCRAPE, SWITCH TAB in the bar,
  OPTIONS after right, the first row after down, the wrap strip -> rows ->
  buttons -> strip); 3.17's de-duplication case; #65's component half
  proved there and put to the pause (§ 2's row). **`getHelpPrompts` per
  component** (12 `.cpp` definitions, 2 inline): a table of each with the
  condition under which it offers a direction, and **L-13**'s two that
  offer by type or by mode alone (the carousel, the option list) framed
  on the guest if a one-system carousel or a one-value option row is
  reachable, else recorded; **L-01**: the icon key through `_()` --
  3.16's case over `getIconTexture`'s key table with `haut/bas`, the
  `es_log.txt` line `Unknown help icon "haut/bas"` and a French settings
  page's help bar at 640x480 (G-04 or G-05 run under French) are the
  positives; the contained fix drops the `_()` on `ComponentList.cpp:568`
  (the catalog's `msgid "up/down"` then an orphan the stream leaves or
  removes, D-UI-051's same-commit rule either way). **L-15**:
  `setCursorToButton`'s unstated invariant, a `dynamic_pointer_cast` plus a
  null check as the contained fix, the invariant written into `02` beside
  `MenuComponent.h:53-56`. **The back-button accelerator** is `GuiMsgBox`'s
  (T35's) and is cited, not read; what this slice owns is the bar's order
  (`MenuComponent::addButton` `:487`, BACK last) and the grid's cursor.
- **Q4 Lifetime** (`es-code-traps.md:22`, `:191`; `es-native-ui.md:94`;
  D-UI-078, D-UI-093; the lifetimes run). **L-11** and § 1 (d): the four
  `delete this` and the two return-straight-after lines read, the
  invariant stated, 3.19's ASan harness in `cloud-oauth-lifetime.py`'s
  shape run on the host over an extracted popup if a `Window` double
  suffices, else `CANNOT` with the reason. **L-12**: 3.20's case (post,
  delete, drain) with the fakes' `Window.h`; a contained fix is a weak
  token the posts check, put to the pause with T33's `AppWindow` named.
  **L-10**: the detached release thread, the unlocked `component = nullptr`
  write, the destructor's `stopVideo()`: a read trace with the two threads
  and the two reads named; TSan on a guest with a video theme is G-10's
  `CANNOT` (no media); outside the lanes, recorded. **§ 1 (b)**, T2's
  PC-1: what the card promises a holder after `window.deinit()` -- the
  destructor `:125-126`, the mutex, `Window`'s teardown order (cited from
  T35's file) -- and whether the component can refuse a late `close()`;
  the lane files the `bug` if the read proves the window, naming the
  callers' half for T18 and T20. **§ 1 (c)**, T26 PL-27: the callback
  types of `SwitchComponent::setOnChangedCallback` and
  `OptionListComponent`'s, whether a weak-by-design type is the
  component's answer or the pages' `onFinalize` clearing stays the fix;
  LeakSanitizer over an extracted builder; a design ruling at the pause.
  **§ 1 (e)**, #1266: `ImageGridComponent::clear()` / `resetGrid()` read
  for what the grid may still point at after `clear()`, the contract
  written, T32's `s4-views.py` shape named as the harness. **L-21**:
  recorded, sound. A table: every `delete this` (4), every `std::thread`
  (1), every `.detach(` (1), every `postToUiThread` (2), every raw pointer
  a component hands out or holds across a rebuild, who joins or drains it,
  what it touches on the interface thread.
- **Q5 Reads and the network** (`es-native-ui.md:107`;
  `es-code-traps.md:127`, `:164`, `:238`; `engineering-practices.md:111`;
  D-RA-009; the reads run). **The reads**: 10 `exists(` lines, 10
  occurrences, **0 uncached**: each with its file, its writer while ES
  runs (the scraper for the media paths, `HttpReq` for the badge, a theme
  install for the theme paths), and whether a remembered miss changes the
  screen. **L-08**: `tools/ra-ui-test`'s fixture shape (a 204 then a 200
  on the same badge URL) and a frame of the row; by design per the comment,
  and the player sees nothing, so the disposition (a re-ask on the next
  page build, or a word on the row) is the pause's; **L-09**: 3.21's case
  with the real `FileSystemUtil` (the miss cached at `:134`, the file
  written, `:190` read), seen to FAIL or PASS at the pin, the answer about
  the writer's erase cited from T21's and T36's rows; **L-20**: recorded
  with the scraper named as the writer, a frame if a scrape then a game
  open before any launch fits the window, else `CANNOT`. **§ 1 (a)**,
  #1263's caller half: `ImageComponent.cpp:408` read with
  `TextureResource.cpp:100-131` (T36's, cited): what the component asks
  by path, when it re-asks, what a live texture under the key gives it
  (T26 #1221's shape); the contract stated in `02`; the cache's half named
  for T36. A table: every `exists`, `getFileSize`, `HttpReq` and texture
  lookup reachable from the 80 with its writer and what a stale answer
  reads as.
- **Q6 The words** (`es-player-text.md:25`, `:29-31`, `:135`, `:141`,
  `:236`; `es-ui-style-guide.md:88`, `:144`, `:164`; D-UI-051,
  D-WORKFLOW-144; the strings and French runs). **The 17 msgids** against
  the catalog (the proof's parser shape, re-run); `SWITCH TAB` and its
  French read in G-05's frames under EN and FR; **`"Auto"`**
  (`SliderComponent.cpp:282`): 3.7's case, G-09's frame, the contained fix
  `_("AUTO")` with its French in the same commit (the placeholder word the
  style guide names) -- upstream's line, rule 6, a #585 line; **the slider's
  suffix** glued (`:295-296`, `:312-313`) read against `es-ui-style-guide.md:88`
  and framed; **3.13**: a row with no date reads blank, not `<NOT SET>`
  (`DateTimeEditComponent.cpp:256-257`), recorded against `:164`, a style
  question for the pause; **L-18**: the five up-casing formatters tabled
  with the one word they must never see, and a `tools/vocabulary-check`
  rule proposed in `02` (a grep for the brand inside `addEntry|addButton|
  setTitle|addWithDescription|addGroup` arguments) for the coordinator;
  **L-01**'s French half is Q3's; the 0 non-ASCII comment lines in the 21
  fork-modified files and the one upstream byte at
  `VideoVlcComponent.cpp:859` (Q7). The card's candidate rows
  (D-UI-035, D-UI-107) are read for the shape the component imposes (at
  least one candidate per row; the width it hands the chooser, 3.18), the
  words themselves being T18's and T20's.
- **Q7 The structure and the merge debt** (`es-native-ui.md:32`;
  `es-code-traps.md:60`; `engineering-practices.md:28`, `:576`;
  D-WORKFLOW-162, D-WORKFLOW-209; the membership, scope, delta and
  non-ASCII runs). **L-07**: the es-core to es-app include recorded with
  how it resolves (`-I es-core/src` plus `../../`), the unit build's
  `CloudText.cpp` link, and the question for the pause (a `CloudText`
  that moves to es-core is T18's and T35's call, not the lane's). **The
  in-source platform gates** (`GridTileComponent.cpp:11`,
  `NinePatchComponent.cpp:415`, `VideoComponent.cpp:22`,
  `VideoPlayerComponent.{cpp,h}:1`, `VideoVlcComponent.cpp:17`, `:485`,
  `:592`, `:668`, `:779`, `:836`, `:874`, `:875`) tabled against
  `es-core/CMakeLists.txt`'s unconditional lists (`:49-90`, `:186-223`;
  `if(` only at `:278` and `:287`): which units compile to nothing on an
  image (`VideoPlayerComponent` whole), D-WORKFLOW-209's disposition (a
  dead-end table removes nothing). **The non-ASCII byte**
  (`VideoVlcComponent.cpp:859`): recorded, not fixed (`es-code-traps.md:60`,
  an upstream hit), with the fact that `git grep -P` does not see it and a
  C-locale grep does, and `:860` read for what sits next to it. **L-14**:
  the two indentations and the include above the guard, a stream's
  one-commit tidy if the pause opens it. **L-05**'s second copy: recorded,
  not deleted (`engineering-practices.md:576`). **Merge debt: none**, the
  one line; **batocera's eight** as the reconciliation list with the one
  `updateGrid()` overlap and the six fork candidates for #585 named in
  `02` § The #585 lines owed (`aa8c5da4c` the strongest; `7c7ffab43`;
  `b6eb26980`; `8927b1760` with `f1ae6bc25` as a pair; `7dc8bf373` only
  after the RTL reconciliation; `2088eadb9`); **the `setOpacity` null
  guard**: `git grep -n 'setOpacity' PIN -- es-core/src es-app/src` for
  every caller, whether `mGrid` can be null at `HelpComponent.cpp:212` or
  `:251` on the fork's images (`ShowHelpPrompts` off, or a page with no
  prompts, while something fades the bar), a contained guard under rule 6
  if reachable, recorded with the read if not; **`UntintedImageComponent`**'s
  home found by `git grep` and the lift question put to the pause (§ 1 h).
  **The map**: no row; the checker's line quoted (§ 3 item 3).

### The floor's pure leads, carried

The floor and fork-changes digests are in no tree, so their seams are here
in the shape `file:line at the pin | the function | what a case would
catch`; rows 3.1 to 3.21 are the floor's, 3.22 to 3.34 the fork-changes
digest's § 5 seams that the floor does not carry; the seven that FAIL at
the pin, or are the candidates the drafter marks as such, are in bold.
Each is a case in `CloudText`'s shape (§ 5 item 1) with a `Window` or
`Font` double where the lines consult one (the fakes' `Window.h` exists; a
`Font` double is the lane's), unless marked ASan or guest.

| # | At the pin | Function | What a case would catch |
| --- | --- | --- | --- |
| 3.1 | `ComponentGrid.cpp:396-414` | `canMoveCursor(dir)` | a 2x2 whose only focusable cell is one row answers false in all four directions; an Nx2 button row with a 2 px spacer row answers left/right true, up/down false; `(0,0)` false (`:398-399`) |
| 3.2 | `ComponentGrid.cpp:519-553` | `getHelpPrompts()` | a child prompt named `up/down` suppresses the grid's vertical CHOOSE (`:536-538`); `up/down/left/right` both (`:532-535`); otherwise exactly one of the three (`:546-551`) |
| 3.3 | `ComponentGrid.cpp:329-379` | `moveCursor(dir)` | from the only focusable cell every direction returns false and `mCursor` is unchanged (`:377-378`); in a 1x3 with (0,2) the only other focusable, down from (0,0) lands on (0,2); the reverse scan (`:359-373`) stays off |
| **3.4** | `MultiLineMenuEntry.cpp:50-80` (**`:74-75`**) | `naturalHeight`, `layoutRows()` | font height 20, padding 0: label only -> rows 20 and 0; with a substring -> `0.9*20/40`, `1.1*20/40`; **`rowPercs(26, 20)` -> 0.987 and `(20, 26)` -> 1.013, a sum other than 1 (L-03)**; 300 `setDescription` calls leave `size.y` at 40 (#241) |
| 3.5 | `TextComponent.cpp:315-340` | `onTextChanged()` | SINGLELINE with `"a\nb"` measures `"a"` (`:325-327`); with padding 32 px on a 640 px box and a word at the wrap point the measured height is one line short (`:338` against `:350`, L-17) |
| **3.6** | `TextComponent.cpp:486` | `update()`'s vertical marquee limit | **`int limit = mSize.y() - mPadding.y() - mPadding.y();` where `:428` and `:351` subtract `.w()`: with padding (0,10,0,30) the limit is 20 px too large** -- the lines `:480-500` read whole before the stub |
| **3.7** | `SliderComponent.cpp:44-58`, `:271-319` (**`:282`**) | `calculatePrecision(step)`, the value text | step 0.1 -> `1.5%`; step 1 -> `15%` (suffix glued); step 0.25 -> 2; **AUTO prints `"Auto"`, neither `_()` nor the placeholder `AUTO`**; `std::to_string(step)` prints six decimals so a step under 1e-6 yields 0 |
| **3.8** | `CarouselComponent.cpp:74-90` with `:113`, `:119`; `IList.h:376-400` | `moveCursorFast(forward)` | **size 3, cursor 0, `pageup`: `count=-10`, `value = -10 + 3 = -7` after one `+= sz` (`:84-85`), `listInput(-7)`**; the case asserts the landing index is in `[0, sz)` for every loop type (3.15) |
| 3.9 | `ImageGridComponent.h:1437-1468` | `calcGridDimension()` | 640x480, tile 100x100, margin 10 -> x 5, y `ceil(4.45)` = 5, `mLastRowPartial`; a tile size of 0 when `mTileSize + mMargin` is 0 (only `LOG(LogError)` guards `<1`, `:1449-1452`) |
| 3.10 | `ImageGridComponent.h` from `:1065` (`:1162-1186`) | `onCursorChanged`'s `mStartPosition` | first, middle and last row -> 0, `(col - centralCol) * dimOpposite`, `lastScroll * dimOpposite`; an off-by-one on the partial last row |
| 3.11 | `TextListComponent.h:262-269` | the visible range in `render` | offset 0, row 20, height 480 -> `screenCount` 24, `lastEntry min(n, 25)`, `listCutoff` 24; the extra row past the cutoff (the arithmetic extracted first) |
| 3.12 | `DateTimeEditComponent.cpp:124-160` | the month/day/year step inside `input()` | 31 Jan +1 month -> 28/29 Feb (`:156-158`); Dec +1 -> Jan (`:131-132`); day 1 -1 -> days in month (`:144-145`); `tm_year` 0 -1 -> 0 (`:152-153`); a fake `InputConfig` or an extraction |
| 3.13 | `DateTimeEditComponent.cpp:251-260` | `getDisplayString()` | `getTime() == 0` -> `""` (`:256-257`): a row with no date reads blank, not `<NOT SET>` (Q6) |
| 3.14 | `ScrollableContainer.cpp:62-107`, `:110-124`, `:126-131` | `update`, `getContentSize`, `reset` | content 1000 px in a 480 px box, speed 150, delay 6000: the first step at 6000 ms (`reset` seeds `-delay + speed`, `:130`); `mAtEnd` then `reset()` after `AUTO_SCROLL_RESET_DELAY` (`:6`); `:69`'s unused `680.0f` is lint |
| 3.15 | `IList.h:267-330`, `:376-400` | `listInput`, `scroll` | `LIST_NEVER_LOOP` clamps and zeroes velocity and tier (`:388-399`); `LIST_PAUSE_AT_END` clamps only at tier > 0 or `\|amt\| > 1`; else wraps -- the landing index for 3.8 |
| **3.16** | `HelpComponent.cpp:73-130`, `:121-169`, `:176-200` | the prompt row's layout; `getIconTexture` | `maxWidth = width - ENTRY_SPACING` (`:79`), the clock's width subtracted (`:89-90`), height `round(letterHeight * 1.25)` (`:96`); `[100, 100, 100]` at max 250 -> 2 kept; `[300]` -> 0 kept, `rowWidth = 1`; **a key `haut/bas` -> `nullptr` and the `Unknown help icon` line (L-01)** |
| 3.17 | `ComponentTab.cpp:77-96`, `:320-345` | `input` left/right, `getHelpPrompts` | a child prompt already naming `left/right` or `up/down/left/right` gets no second SWITCH TAB (`:332-341`); a one-tab strip offers none |
| 3.18 | `AsyncNotificationComponent.cpp:136-145`, `:63-65` | the width handed to `chooseThatFits` | the row's own `getSize().x()` (`:138`; 0 for a null row), measured with the row's font (`:142`): a row the grid has not sized yet gets the first candidate, the full form (`:133-135`); the case asserts the width is the row's cell, never the screen's 0.9 W (`:64`) (the chooser itself is `CloudTextTests.cpp:832-854`) |
| 3.19 | `OptionListComponent.h:88-100`, `:140-160`, `:188-200` (ASan) | the popup's four `delete this` | select a row (`:96`), press BACK (`:158`), the back button (`:195`): the popup is gone and nothing touches it after; the `cloud-oauth-lifetime.py` shape |
| 3.20 | `TextEditComponent.cpp:39`, `:47` | the two posted raw `this` | post, delete the component, drain the queue: `startEditing()` on freed memory (the fakes' `Window.h` queues posts) |
| **3.21** | `WebImageComponent.cpp:134`, `:190`, `:197-200`; `utils/FileSystemUtil.cpp:144` | the cached `exists` around a download; the 0-byte answer | **the miss cached at `:134`, the file written, `:190` asserted true**; **a 204 then a 200 on the same URL: the second never asked (L-08)** -- `queryCacheEntry :203-220` and `Settings::UseFileCache()`'s default read first |
| 3.22 | `ImageComponent.cpp:85-180` | `resize`'s fit (aspect, turn, min/max modes) | `256x240` at `4/3` -> `320x240`; turned -> `240x320`; a crop applied to the wrong axis after a turn (`:156-159`, `:167-170`); an aspect of 0 changing anything |
| 3.23 | `ImageComponent.cpp:273-291` | the texture-corner permutation | turn 1 applied four times is identity; turn 2 is turn 1 twice; turn 3 its inverse |
| 3.24 | `ImageComponent.cpp:491-499`, `GridTileComponent.cpp:1055-1063` | the quarter-turn normaliser | `-1 -> 3`, `5 -> 1`, `-4 -> 0`; a negative record left negative |
| 3.25 | `ComponentList.h:26` | `ComponentListFlags::dimmed` | `dimmed(0xAABBCCFF) == 0xAABBCC50`; idempotent |
| **3.26** | `MenuComponent.cpp:543-562`; `ButtonComponent.cpp:10` | `makeButtonGrid`'s widths | **four 128 px buttons at 640 -> 568 <= 576; five -> 710 > 576 (L-04)**; a column percentage sum other than 1 |
| 3.27 | `MenuComponent.cpp:396-424` | `updateSize`'s row-fit loop | a first row taller than the budget -> zero rows; rows exactly filling; the `height + rowHeight < maxHeight` test excluding the row that fits exactly |
| 3.28 | `ComponentList.cpp:295-319` | `updateCameraOffset` | a cursor on the last row -> `total - view`; rows shorter than the view -> 0; the `mCursor < mEntries.size()` signed/unsigned compare |
| 3.29 | `TextListComponent.h:591-608` | `updateCameraOffset` | the same three, for the game list |
| 3.30 | `SwitchComponent.cpp:50-80`, `:118-138` | the tri-state cycle, `getValue`/`setValue` | auto -> on -> off -> auto; `setValue("auto")` without `hasAuto` -> off; `"AUTO"` (case) read as off |
| 3.31 | `SliderComponent.cpp:234-257` | `setValue`'s clamp and the AUTO sentinel | `setValue(max + 1) == max`; the sentinel (`mMin - mSingleIncrement`) accepted without auto mode |
| 3.32 | `RatingComponent.cpp:192-204` | the OK-press accumulation `+= 1/5` | five presses from 0.0 reach 1.0 exactly, the sixth wraps; from a parsed `0.35` the steps drift |
| 3.33 | `TextEditComponent.cpp:267-271` | `moveCursor` through `Utils::String::moveCursor` (T21's) | a 4-byte glyph and a two-character CJK name: a cursor inside a UTF-8 sequence |
| 3.34 | `CarouselComponent.cpp:183-200` | the shortest-path target | from 0 to N-1 -> `-1`; from N-1 to 0 -> `N`; a count of 1; a divide by 0 |

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #681.** Every read, count and table runs on the host
   at the pin's bytes. **The host has no toolchain** (#1137):
   `tools/es-syntax-check` exits 2 on this host (`es-syntax-check: no build
   root at ... (ES_BUILD_ROOT, --root)`, its `:69`) and records that line
   with `ES_BUILD_ROOT` set, never empty; **0 of the 38 `.cpp` were ever
   syntax-checked on the host** (every `stage-a`/`stage-e` record of the
   three lanes with a stand-in check names none of the 80; T32's
   `s0-syntax-pin.txt` is the whole record at this pin, and three of its
   rc-0 translation units include `ImageGridComponent.h`,
   `TextListComponent.h`, `CarouselComponent.h` and `GridTileComponent.h`
   through `views/gamelist/*.h`, so **the headers have parsed under the
   fakes transitively; no `.cpp` body of the 38 has**). The include graph,
   read not compiled (the floor's § 2): every one of the 42 headers reaches
   `GuiComponent.h` directly or through another component header (28 direct
   lines), and `GuiComponent.h` reaches `InputConfig.h` (`<SDL_joystick.h>`,
   `<SDL_keyboard.h>`, `<CECInput.h>`) and `ThemeData.h`
   (`<pugixml/src/pugixml.hpp>`); `resources/Font.h` (`<ft2build.h>`)
   reaches most; `InputManager.h` adds pugixml and `GunManager.h`
   (`<libudev.h>`, `<SDL.h>`, `<Windows.h>`, guarded as T32's rc-0 TUs
   show). So the 38 fall in four classes: **(a) pure, 0**; **(c) SDL and
   pugixml through `GuiComponent.h`, 35**; **(c+) an SDL header not among
   the nine fakes, 1** (`BatteryIndicatorComponent.cpp:7 <SDL_power.h>`: a
   tenth fake the lane writes under `stage-a/fakes/`); **(d) VLC, 1**
   (`VideoVlcComponent.cpp:8-9 <vlc/vlc.h> <vlc/libvlc_version.h>`, also
   `:10 <SDL_mutex.h>`, `:14 <SDL_timer.h>`, `:593 <Windows.h>`: two VLC
   fakes, or `CANNOT` with the headers named); **(e) curl, 1**
   (`WebImageComponent.cpp:3 "HttpReq.h"` -> `<curl/curl.h>`, the existing
   fake). **The SDL symbols the fakes must declare**, which the partial
   `SDL_keyboard.h` cost T32 its one rc 1: `SDL_GetTicks` (x3),
   `SDL_LockMutex`/`SDL_UnlockMutex`, `SDL_CreateMutex`/`SDL_DestroyMutex`,
   `SDL_StartTextInput`/`SDL_StopTextInput`, `SDL_GetKeyboardState`,
   `SDLK_RETURN`, `SDLK_UP DOWN LEFT RIGHT HOME END ESCAPE DELETE`
   (`TextEditComponent.cpp` is the first to fail if the fake lacks a
   `SDLK_` constant); seven files use an SDL symbol. **The stand-in check**
   is T21's `stage-e/syntax-check.sh:12-16` (`g++ -std=c++17 -fsyntax-only
   -DHAVE_INTL -I "$F" -I "$ES/es-app/src" -I "$ES/es-core/src" -I
   "$ES/external" -I "${PUGIXML_INCLUDE_DIR:?}" -I "${RAPIDJSON_INCLUDE_DIR:?}"`,
   `rc=$?` on its own line) with T31's 13 fakes (§ 3 item 8) copied under
   `stage-a/fakes/`, the tenth fake added, **and the pugixml root**, over
   classes (c), (c+) and (e), 37 files, `rc` per file recorded; it checks
   the file's own C++ and proves nothing about SDL, VLC or curl. **The
   pugixml root, said beside the check that needs it:** `external/pugixml`
   is a gitlink at the pin (`git ls-tree PIN external/` prints `160000
   commit 61c944895e071872370219cadade8423dc6e04dc external/pugixml`), so
   an archive, a `git show` or a fresh clone carries no pugixml, and plain
   `g++` on any component `.cpp` with `-I es-app/src -I es-core/src -I
   external` dies at `es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No
   such file or directory` (rc 1, g++ 15.2.0, run by the proof over a `git
   archive` of the pin: the SDL header through `GuiComponent.h` ->
   `InputConfig.h`, before any pugixml line). The one root that works is the pin's extracted source,
   `/workspace/cache/rocknix-sources/emulationstation/emulationstation-16dbac5211eea7e70db7394372033be2be7df829/external`
   (the directory exists on this host; T31's and T32's scripts took
   `PUGIXML_INCLUDE_DIR` from it). **The one cross-tree include resolves
   only through an include root**: `AsyncNotificationComponent.cpp:12`'s
   `../../es-app/src/CloudText.h` relative to the file is
   `es-core/es-app/src/CloudText.h`, which does not exist; `-I es-core/src`
   plus `../../` is the tree root, which the stand-in check supplies; a
   unit build of the file links `CloudText.cpp` for `:144`.
   **The harness that exists, described once: nothing links a component.**
   `es-app/tests/unit/CMakeLists.txt` (159 lines) defines `es-unit-tests`
   (`:36-65`; 16 test files, 9 es-app and 3 es-core sources, none under
   `components/`), `es-file-tests` (`:96-112`), `es-conf-tests`
   (`:120-135`), `es-file-tests-win32` (`:146-158`);
   `tests/app-unit/CMakeLists.txt` (106 lines) defines `app-unit-tests`
   (`:35-42`, under `-fsanitize=address,undefined` `:31`),
   `proxycards-tests` (`:51-56`), `jobs-tests` (`:71-78`),
   `bookkeeper-tests` (`:92-98`), none naming a component source; the one
   component name in a test tree is the double
   `tests/app-unit/fakes/components/AsyncNotificationComponent.h`; of the
   15 `tests/*.py`, seven name `fsanitize` and none names a
   `components/*.cpp`; `tests/gpu-governor-save.py:14` lifts four
   `OptionListComponent.h` methods as text. **In the coordinator worktree
   nothing exercises a component by name:** `tools/vm-qa:63`'s sixteen
   suites name none; the 18 walks drive menus by key and every page they
   open is built on this slice; `tools/es-menu-map-check:54-55` reads
   `MenuComponent(` constructor calls in es-app; `tools/ra-ui-test:199`
   greps a guest's `es_log.txt` for `ProxyCards:|AsyncNotification`;
   `claims.txt:30` is the help bar's one accepted claim at 1280x800; the
   prior guest evidence is twelve `docs/vm-qa-log.md` rows (`:36`, `:41`,
   `:46`, `:52`, `:68`, `:70`, `:78` -- the card's 21 frames at 640x480 and
   three at 1280x800, the fullest record of `AsyncNotificationComponent` on
   a frame -- `:104`, `:107` -- the help bar centred, `70 / 71` px at
   640x480 and `118 / 118` at 1280x800, five of six French prompts drawn at
   640 -- `:145`, `:152`, `:188-190`) and, under `docs/qa-logs/`, four
   lines (`2026-10-13-wifi-picker-source/README.md:91`,
   `2026-10-14-screenscraper-ui-runtime/README.md:5`,
   `2026-10-11-frame-claims/README.md:6`,
   `2026-10-11-network-cloud-management/frame-index.md:42`); **not on
   record anywhere**: a frame of the tabbed strip with its selector bar, a
   grid view, a slider's suffix, a dimmed row measured, a
   `MultiLineMenuEntry` refreshed more than once, a `canMoveCursor`,
   `BUTTON_GRID` or `NOTIFICATION_OPACITY` line (the lane takes the per-name
   count over `docs/qa-logs/` with `grep -rl -F <name> ... | wc -l` before
   claiming a zero).
   **The host floor is the lane's own: unit cases for the 34 pure seams** in
   `CloudText`'s shape (`es-code-traps.md:139`) -- **first the seven that
   FAIL at the pin or are marked as candidates** (3.4's `rowPercs`, 3.6's
   `:486`, 3.7's `"Auto"`, 3.8's `moveCursorFast`, 3.16's `haut/bas` icon
   key, 3.21's cached `exists` and 0-byte answer, 3.26's bar width), each
   seen to FAIL against the unfixed extract before it is trusted, the stub
   checked against the unfixed code first (`engineering-practices.md:464`),
   then the rest. The cases are **built by the lane's generated script in
   T32's shape** (`t32-build-tests.sh:30` the `python3 -I` parse of
   `es-app/tests/unit/CMakeLists.txt`, `:44` `g++ -std=c++17 -O0 -g0
   -pthread`, `:57` the include roots, `:70-75` the pugixml guard, `:112`
   the `TOTAL:` echo; T32's close read `TOTAL: 225 test cases in 4
   binaries`, `handback-checks.txt:45`), **extended to add a
   `components-tests` binary** that links the component sources a case
   needs with `Window`/`Font` doubles (the `tests/app-unit/fakes/` set, a
   `Font` double of the lane's) and `CloudText.cpp`, saved as
   `docs/audits/<audit>/tools/t34-build-tests.sh`, **the total quoted as
   the script's `TOTAL: N test cases in B binaries` line** and never summed
   by hand (`engineering-practices.md:250`); rapidjson from the recipe's
   tarball plus its four patches (`projects/ROCKNIX/packages/devel/rapidjson`,
   unpacked under `/workspace/tmp/m6-t34/rj/` as T21, T32 and T33 did);
   pugixml from the cache source above. **`tools/font-stems`** (227 lines;
   usage `:9`; libfreetype through ctypes `:88-100`; `FT_Set_Pixel_Sizes`
   with default hinting `:104-106`) prices a string's width at a pixel size
   for a face on the host -- the inputs `Font::sizeText`/`getHeight`
   consume -- so a slider's `max + suffix` or a help prompt's label at
   640x480 is a number the host produces, given the image's face path (read
   off the guest in G-01); it cannot run ES's `Font` or `TextComponent`.
   The counts and the generated tables run on the host.
2. **The guest window** -- one, asked for on #681 at stage B's end with its
   plan and bound (**30 minutes proposed, plus 5 of grace**: the plan below
   sums to 1,410 s, 23.5 minutes, by the floor's `printf '%s\n' 60 240 120
   120 180 120 0 180 90 0 180 120 | awk '{s+=$1} END {print s}'`, and the
   second boot is inside it; T33's window was 25 + 5 for a 21-minute plan),
   granted explicitly by the coordinator on #681 and in the shared log's
   queue. **The queue is the shared file's own lines**,
   `/workspace/tmp/m7-m6-host-coordination.txt` (the durable successor of
   `/tmp/m7-m6-host-coordination-20261023.txt`, gone with the reboot of
   2026-10-28; M7 writes timestamped lines, so the whole tail is read): a
   request is a line that names the slice, its plan and its bound; the
   grant is the coordinator's line answering it; the lane's START and
   RETURN each add a line with the census; the file is read before any
   guest starts (§ 1's last command, with the time of the read), and who
   holds the host is read there, with the time.
   **The conditions, stated here once -- T13's (#660, the first M6 lane to
   hold a guest window, whose shape every later window kept), beyond the
   rule file's own (§ 3's `generic-x64-vm-testing.md` rows):** one boot of
   the M6 copy of the image (`/workspace/artifacts/m6-t2-20261023/`,
   `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`,
   present on this host at this draft) **started at 640x480**
   (`generic-x64-vm run --headless --daemonize --res 640x480`, #1141);
   **the image identified by two literals first** (`BUILD_ID` from
   `/etc/os-release` and the file name); **every verdict labelled by
   side** because the image's EmulationStation is M7's composition --
   `pin-binary` only where the digest found the pin's lines unchanged
   against the image's binary, else `image`; the post contract `START
   HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as the first line of each post on
   #681 and a line in the shared host file, each with the census (`qemu N,
   compilers N`); the stop by pidfile at bound plus grace (`tools/vm-stop`,
   never a pattern); the disk retired after with path, size and sha
   (D-INFRA-022); the guarded `tools/build-preflight --reclaim-swap` allowed
   once, before the guest, never beside it. **The second boot at 1280x800
   is this slice's own need**: the bar and the card are screen fractions
   (`es-native-ui.md:299`) and `es-code-traps.md:266` asks for both sizes;
   a guest's size is QEMU's flag, so the second size is a second boot of
   the same disk. **The floor's limit, said plainly: a `MultiLineMenuEntry`
   refreshed hundreds of times needs the offline scan over dozens of games
   (#241's shape), which is not inside one window -- 3.4 is its proof; a
   video component needs media the fixture has not (T33's finding); the
   grid view needs a theme that draws `ImageGridComponent` -- G-01 asks the
   image, and G-08 is `CANNOT` with its grep line if none does.** None of
   these needs a device; each is a unit lead or a harness gap to name
   (`bugs-are-agent-first.md` rule 3). The QA accounts are needed by no
   row (`tools/qa-accounts`, never printed; never the owner's, D-QA-015).
   Every proof's frames are labelled by side; a fix's frame is
   `fix-walk-pending-image`.

   | G | Behaviour only the running image shows | Walk or serial command | Expected frame or line | Bound (s) |
   | --- | --- | --- | --- | ---: |
   | G-01 | identity and side; the theme and the face | `vm-serial sh 'cat /etc/os-release; fbset; ls /usr/share/themes; grep -rl -E "imagegrid\|<grid" /usr/share/themes/*/ \| head; find /usr/share -name "*.ttf" \| head'`; the ES binary's digest against the pin's lines (T26's `g01-identity.txt` shape) | `BUILD_ID=...`, `640x480`; the theme name; whether any theme file names a grid; the face path for `tools/font-stems`; every frame labelled `image` or `pin-binary` | 60 |
   | G-02 | the card at 0.9 of the width, centred, opaque over box art (`AsyncNotificationComponent.cpp:31`, `:64`, `:112`) | `default-pre` (`suite.txt:77`) with the WebDAV stanza seeded; reboot; the startup sync card over the carousel (`vm-qa-log:78`'s 21 frames are the precedent); `shot` at 0.4 s intervals for 6 s | the card's left edge at x 32 and right at x 608 (0.9 x 640 = 576, centred); a pixel inside the card over the game art equal to the nine-patch's panel colour, not a blend (a stdlib `zlib` PNG reader, never by eye) -- `image` side | 240 |
   | G-03 | the button bar's gap at 640x480 (`MenuComponent.cpp:14`, `:13` "14px there") and a YES/NO box's one CHOOSE | MAIN MENU > QUIT > RESTART EMULATIONSTATION: a YES/NO `GuiMsgBox`; `shot`; press B (`z`) to decline | the gap between YES's and NO's nine-patch edges 14 px (`0.022 x 640 = 14.08`), measured in the frame's columns; the help bar carrying one CHOOSE and the buttons' own prompts (3.2) -- `image` side | 120 |
   | G-04 | a dimmed row at alpha `0x50` (`ComponentList.h:25-26`, `MultiLineMenuEntry.cpp:84`, `SwitchComponent.cpp:30`); under French, L-01's bar | on the unseeded guest (before G-02's reboot, or `default-pre` without the stanza): `to-manage-cloud-storage.steps`; `shot` the CLOUD page; then `system.language` set to `fr_FR` over serial with ES stopped (`generic-x64-vm-testing.md:1145`), ES started, the same page, `shot`; `vm-serial sh 'grep -c "Unknown help icon" /var/log/es_log.txt'` | the unconfigured rows' text at `0x50/0xFF` of the selectable rows' luminance over the same panel (two pixel reads), their descriptions still present; under French the CHOISIR prompt with no icon and the log count above 0 (L-01's positive) -- `image` side | 120 |
   | G-05 | the tabbed strip as a focus stop (`MenuComponent.cpp:80-101`, `:144`; `ComponentTab.cpp:77-96`, `:341`) | MAIN MENU > SCRAPER (menu map `:139`); `key up` from the first row; `shot strip-focused`; `key right`; `shot options-tab`; `key down`; `shot rows-again`; `key up`, `key up` (the wrap strip -> rows -> buttons -> strip); the page closed and reopened once for L-02's pair | the selector bar over SCRAPE and SWITCH TAB in the help bar; after right, the bar over OPTIONS and the rows OPTIONS'; after down, the first row focused and no SWITCH TAB; the reopened page's row heights against the first paint's -- `image` side | 180 |
   | G-06 | `canMoveCursor` on a one-button dialog (`ComponentGrid.cpp:396-414`; #115) | the lane picks one OK-only `GuiMsgBox` reachable on an unseeded guest and names it in its START post (a cloud row's refusal before setup, `tests/cloud-gated-row.py`'s surface; the ACCOUNTS tab's SIGN IN with empty fields); `shot` | the help bar reading `OK` and no `CHOOSE` (`:527-528` both false) -- `image` side | 120 |
   | G-07 | a `MultiLineMenuEntry` refreshed hundreds of times keeping its height | -- | `CANNOT` in this window (above); the proof is 3.4, seen to FAIL on the pre-#241 shape first | 0 |
   | G-08 | the grid view (`ImageGridComponent`, `GridTileComponent`) at 640x480 | if G-01 found a grid in the theme: `systemctl stop essway`; `GamelistViewStyle` = `grid` in `es_settings.cfg` over serial (the key read from the file first); ES started; a game list opened; `shot`; `vm-serial sh 'grep -c "grid X dimension\|grid Y dimension" /var/log/es_log.txt'` | tiles at the theme's size and margin, the selected tile scaled, no `LOG(LogError)` from `calcGridDimension` (`:1449-1452`); else `CANNOT: no theme on the image draws a grid` with G-01's grep line -- `image` side | 180 |
   | G-09 | a slider's suffix glued to its value; `"Auto"` (`SliderComponent.cpp:282`, `:295-296`) | MAIN MENU > SOUND SETTINGS (SYSTEM VOLUME, `%`) or UI SETTINGS > SCREENSAVER SETTINGS > SCREENSAVER AFTER (`m`): `shot`; `key right`; `shot`; a slider with auto mode if one is reachable, `key left` past its minimum, `shot` | `NN%` / `Nm` with no space, the knob moved by one increment; `Auto` in mixed case if the auto slider is reached (3.7's positive) -- `image` side | 90 |
   | G-10 | a video component's lifetime on a game list (`VideoVlcComponent.cpp:84-96`) | -- | `CANNOT`: no media in the fixture; the detached thread is Q4's read trace | 0 |
   | G-11 | the second size: the bar's gap, the help bar and the card at 1280x800 | `tools/vm-stop`; `generic-x64-vm run --headless --daemonize --res 1280x800` on the same disk; `vm-serial wait`; G-03's dialog and G-05's strip again; `shot` each | the gap 28 px (`0.022 x 1280 = 28.16`); the help bar's six prompts all drawn (vm-qa-log `:107`: `118 / 118` at 1280x800); the card not re-framed (`:78`'s three frames stand) -- `image` side | 180 |
   | G-12 | close | `tools/vm-stop` on the pidfile; the disk's size and sha; `qemu 0, compilers 0` | `retired.txt`; the leftover check | 120 |

   Sum of the bounds as written: 1,410 s (23.5 min), the floor's figure by
   its author's command. Every frame is read back for its strings; a
   measurement in pixels is made by a reader, not by eye.
3. **What T35 to T37 inherit** is written, not tested here: the slice's
   provenance table (0 / 21 / 59 with both bases named), the layouts table
   (every size computed from a size the pass wrote; the eight
   `Font::getHeight` reads), the constants table (each house value, its
   one definition, every reader, the frame), the input table (the 14
   `input()` and the 14 `getHelpPrompts` with their conditions), the
   lifetimes table, the reads table (10 rows), the `components-tests` build
   recipe (the doubles, the tenth fake, the pugixml root), the
   `setOpacity` callers' read for T35, the texture-cache contract stated
   for T36, and the es-core to es-app include's disposition.
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   ES branch, proven twice (`fix-unit-test` through a case the build script
   links, or `fix-walk-pending-image`), the covering case run before every
   commit, under § 9's same-commit rules for the French; a fix that changes
   `AsyncNotificationComponent.h` names the two lanes' doubles as a
   collision in the hand-back (§ 1 j).

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...* -- **the block below captures neither exit nor
time except where it says `rc=$?`; the lane wraps each run in its own
`rc=$?` line and a `date +%s` pair, or records that it did not**; a run
that cannot be made is `CANNOT` with its reason). From the distribution
worktree after the membership block; `W` the ES worktree (§ 1) -- **before
dispatch, `W` is the `qa-integration` checkout at the pin, read by `git
-C` only, and every expectation below printed at the pin on 2026-10-30 by the
stranger's proof, by `git -C` against `qa-integration`, except the tool
lines marked by stage** --
`PIN` the pin, `MB` the merge base, `FILES` the 80 from the block's paths
file; counts by `/usr/bin/grep` (#1138); **every grep for `_("` is `-F`**
(the basic-regex form with `\(` was T31's stage-A erratum and is not
written here); `rc=$?` on its own line, never after a pipe; **no `cut`
truncates an expected error line** (T33's `cut -c1-90` cut the text the
expectation was about). Every expectation is a printed line, except the
ones marked by stage, which cannot run before the lane writes their
inputs:

```bash
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-components-681; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; C=8ebaf8daad; MB=cada856d86
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t34/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
FILES=$(cat .qa-scratch/t34/paths.txt)
# the scope (expect 80; cpp 38; h 42; other 0)
printf '%s\n' $FILES | $G -c .; printf '%s\n' $FILES | $G -c '\.cpp$'; printf '%s\n' $FILES | $G -c '\.h$'; printf '%s\n' $FILES | $G -c -v -E '\.(cpp|h)$'
# the ES worktree at the pin, clean; the bases; the counts (expect the pin; 0; cada856d86; f6c542872e; b2ceb55a7e; 1750dded8c; 725; 14; 1; 15)
git -C "$W" rev-parse HEAD | cut -c1-10; git -C "$W" status --short | wc -l; git -C "$W" merge-base "$PIN" rocknix/master | cut -c1-10; git -C "$W" rev-parse rocknix/master | cut -c1-10; git -C "$W" rev-parse batocera/master | cut -c1-10; git -C "$W" merge-base "$PIN" batocera/master | cut -c1-10; git -C "$W" rev-list --count bccd715707.."$PIN"; git -C "$W" rev-list --count "$MB"..rocknix/master; git -C "$W" rev-list --count bccd715707.."$MB"; git -C "$W" rev-list --count upstream/master..rocknix/master
# the lines two ways (expect wc -l 21971; grep -c 21984; no trailing newline: 13, the files § 2 names)
for p in $FILES; do git -C "$W" show "$PIN:$p" | wc -l; done | awk '{s+=$1} END {print "wc -l", s}'; for p in $FILES; do git -C "$W" show "$PIN:$p" | $G -c ''; done | awk '{s+=$1} END {print "grep -c", s}'; n=0; for p in $FILES; do a=$(git -C "$W" show "$PIN:$p" | wc -l); b=$(git -C "$W" show "$PIN:$p" | $G -c ''); [ "$a" != "$b" ] && { n=$((n+1)); echo "no newline: $p $a/$b"; }; done; echo "no trailing newline: $n"
# the fork's delta (expect `21 files changed, 591 insertions(+), 114 deletions(-)` three times; A 0; M 21; the 21 numstat rows of § 2; 33 commits, 33 non-merge, no merges)
git -C "$W" diff --shortstat bccd715707 "$PIN" -- $FILES; git -C "$W" diff --shortstat "$MB" "$PIN" -- $FILES; git -C "$W" diff --shortstat rocknix/master "$PIN" -- $FILES; git -C "$W" diff --diff-filter=A --name-only bccd715707 "$PIN" -- $FILES | $G -c .; rc=$?; echo "added rc=$rc"; git -C "$W" diff --diff-filter=M --numstat bccd715707 "$PIN" -- $FILES; git -C "$W" log --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; git -C "$W" log --no-merges --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; git -C "$W" log --merges --format=%h bccd715707.."$PIN" -- $FILES | $G -c .; rc=$?; echo "merges rc=$rc"
# upstream's delta: the merge-debt record (expect 0 rc=1; 0 rc=1; identical to rocknix/master: 59; identical to cada856d86: 59; MB-vs-master identical: 80; batocera commits on the 80: 8; batocera files: 10; both-changed: 7)
git -C "$W" log --format=%h "$MB"..rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream commits rc=$rc"; git -C "$W" diff --numstat "$MB" rocknix/master -- $FILES | $G -c .; rc=$?; echo "upstream numstat rc=$rc"; n=0; for p in $FILES; do git -C "$W" diff --quiet rocknix/master "$PIN" -- "$p" && n=$((n+1)); done; echo "identical to rocknix/master: $n"; n=0; for p in $FILES; do git -C "$W" diff --quiet "$MB" "$PIN" -- "$p" && n=$((n+1)); done; echo "identical to cada856d86: $n"; n=0; for p in $FILES; do git -C "$W" diff --quiet "$MB" rocknix/master -- "$p" && n=$((n+1)); done; echo "MB-vs-master identical: $n"; git -C "$W" log --format=%h 1750dded8c..batocera/master -- $FILES | $G -c .; git -C "$W" diff --name-only 1750dded8c batocera/master -- $FILES | $G -c .; comm -12 <(git -C "$W" diff --name-only 1750dded8c batocera/master -- $FILES | sort) <(git -C "$W" diff --name-only "$MB" "$PIN" -- $FILES | sort) | $G -c .
# the other lanes' deltas inside the 80 (expect every stat line empty for the eight -- T33's `dd86d7ce20a5`, read 2026-10-30 -- or the rows named as a collision)
for b in m6-es-launch-path-649 m6-es-cloud-pages-665 m6-es-achievements-pages-667 m6-es-state-and-bridge-668 m6-es-guimenu-673 m6-es-pages-678 m6-es-app-views-scrapers-679 m6-es-app-system-680; do echo "== $b"; git -C "$W" diff --stat "$PIN" "origin/feature/$b" -- $FILES 2>&1 | tail -n 1; done
# the strings, two ways (expect `_(" lines TOTAL 22 in 12 files`; occurrences 27; per file BusyComponent 1, CarouselComponent 2, ComponentGrid 3, ComponentList 2, ComponentTab 1, DateTimeComponent 1, ImageComponent 1, OptionListComponent.h 6, SliderComponent 1, SwitchComponent 1, TextEditComponent 2, VideoComponent 1)
git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "_(\" lines TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F '_("' "$PIN" -- $FILES | wc -l; git -C "$W" grep -c -F '_("' "$PIN" -- $FILES | sed "s/^$PIN:es-core\/src\/components\///" | tr '\n' ' '; echo
# the threads and the lifetimes (expect `std::thread` 1 at VideoVlcComponent.cpp:91; `.detach(` 1 at :95; `delete this` 4 at OptionListComponent.h:96 :145 :158 :195; `postToUiThread` 2 at TextEditComponent.cpp:39 :47)
git -C "$W" grep -n -F 'std::thread' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -F '.detach(' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'delete this' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'postToUiThread' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the reads and the network (expect `exists( lines TOTAL 10 in 5 files`; occurrences 10; uncached: 0 rc=1; HttpReq lines `WebImageComponent.cpp:5 WebImageComponent.h:2`)
git -C "$W" grep -c -F 'exists(' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "exists( lines TOTAL", s, "in", NR, "files"}'; git -C "$W" grep -o -F 'exists(' "$PIN" -- $FILES | wc -l; git -C "$W" grep -n -E 'exists\([^)]*, *false\)' "$PIN" -- $FILES | $G -c .; rc=$?; echo "uncached rc=$rc"; git -C "$W" grep -c -F 'HttpReq' "$PIN" -- $FILES | sed "s/^$PIN:es-core\/src\/components\///" | tr '\n' ' '; echo
# the input and the help bar (expect getHelpPrompts definitions in .cpp: 12; inline in OptionListComponent.h: 2 at :202 :636; `input(` definitions 14; `canMoveCursor` callers outside ComponentGrid.cpp: 0 rc=1)
git -C "$W" grep -n -E '::getHelpPrompts\(\)' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E 'getHelpPrompts\(\) *(override)? *$|getHelpPrompts\(\)\s*(override)?\s*\{' "$PIN" -- es-core/src/components/OptionListComponent.h | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -E '::input\(InputConfig' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -F 'canMoveCursor' "$PIN" -- es-core/src es-app/src | $G -v 'components/ComponentGrid\.' | $G -c .; rc=$?; echo "canMoveCursor outside rc=$rc"
# the constants (expect nine lines: MenuComponent.cpp:6 :14; AsyncNotificationComponent.cpp:31; ComponentList.cpp:11; ComponentList.h:25; HelpComponent.cpp:13 :16 and :130 (`const float entryWidth`, a use); GuiTextEditPopupKeyboard.cpp:14 the second copy at 0.0052083333 -- the uses at AsyncNotificationComponent.cpp:64 :112 :276 and ComponentList.h:26 are dropped by the `#define|const ` filter)
git -C "$W" grep -n -E 'BUTTON_GRID_(HORIZ|VERT)_PADDING|NOTIFICATION_OPACITY|DIMMED_ALPHA|TOTAL_HORIZONTAL_PADDING_PX|ICON_TEXT_SPACING|ENTRY_SPACING' "$PIN" -- $FILES es-core/src/guis/GuiTextEditPopupKeyboard.cpp | sed "s/^$PIN://" | $G -E '#define|const ' | cut -c1-160
# the pixel constants (expect 2 lines, both comments, MenuComponent.cpp:11 and :13; screen-relative lines 86; fontScale 0 rc=1)
git -C "$W" grep -n -E '[0-9]+px|\b(640|480|1280|800|1920|1080)\b' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -c -E 'getScreen(Width|Height|Proportion)' "$PIN" -- $FILES | sed "s/^$PIN://" | awk -F: '{s+=$NF} END {print "screen-relative", s}'; git -C "$W" grep -c -F 'fontScale' "$PIN" -- $FILES | $G -c .; rc=$?; echo "fontScale rc=$rc"
# the includes (expect quoted include lines 352; angle 37; es-app 1 at AsyncNotificationComponent.cpp:12; outside includers 274 lines in 112 files; CMake: 42 headers named at :49-90, 38 sources at :186-223, named-0-times 0, `if(` at 278 287)
git -C "$W" grep -h -E '^\s*#\s*include\s*"' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -h -E '^\s*#\s*include\s*<' "$PIN" -- $FILES | $G -c .; git -C "$W" grep -n -E '^\s*#\s*include\s*"\.\./' "$PIN" -- $FILES | sed "s/^$PIN://"; B=$(printf '%s\n' $FILES | sed 's|.*/||; s|\.h$||' | $G -v '\.cpp$' | paste -sd'|'); git -C "$W" grep -n -E "^\s*#\s*include\s*[<\"]([a-z/]*/)?($B)\.h[>\"]" "$PIN" -- . ':!es-core/src/components' | sed "s/^$PIN://" > "$TMPDIR/includers.txt"; wc -l < "$TMPDIR/includers.txt"; cut -d: -f1 "$TMPDIR/includers.txt" | sort -u | wc -l; n=0; for p in $FILES; do b=${p#es-core/src/}; git -C "$W" grep -c -F "$b" "$PIN" -- es-core/CMakeLists.txt | sed "s/^$PIN://" | $G -q ':1$' || { echo "not once: $p"; n=$((n+1)); }; done; echo "named-0-times (or more than once): $n"; git -C "$W" grep -n -E '^\s*if\s*\(' "$PIN" -- es-core/CMakeLists.txt | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo
# the in-source gates (expect the twelve lines § 4 Q7 names)
git -C "$W" grep -n -E '^\s*#\s*(if|ifdef|ifndef|elif)\b.*(_RPI_|WIN32|USE_OPENGLES_30|LIBVLC_VERSION_MAJOR|BATOCERA)' "$PIN" -- $FILES | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the non-ASCII byte (expect `git grep -P` 1 rc=0 under the block's LC_ALL=C; in a UTF-8 locale (`LC_ALL=C.UTF-8`) it prints nothing, rc=1 -- the UTF-mode miss; the C-locale loop `VideoVlcComponent.cpp:1`, `files with a non-ascii byte: 1`, and the comment-line form the same 1; the 21 fork-modified files 0)
git -C "$W" grep -n -P '[^\x00-\x7F]' "$PIN" -- $FILES | $G -c .; rc=$?; echo "git grep -P rc=$rc"; n=0; for f in $FILES; do c=$(git -C "$W" show "$PIN:$f" | LC_ALL=C $G -c -P '[^\x00-\x7F]'); [ "$c" != 0 ] && { echo "${f#es-core/src/components/}:$c"; n=$((n+1)); }; done; echo "files with a non-ascii byte: $n"; git -C "$W" show "$PIN:es-core/src/components/VideoVlcComponent.cpp" | LC_ALL=C $G -c -P '^\s*//.*[^\x00-\x7F]'; git -C "$W" show "$PIN:es-core/src/components/VideoVlcComponent.cpp" | sed -n '859,860p' | LC_ALL=C od -c | head -n 4
# the French (expect `4929:msgid "SWITCH TAB"` with `msgstr "CHANGER D’ONGLET"` after it; `3708:msgid "up/down"` with `msgstr "haut/bas"`; `^msgid ` lines 2207; the slider's "Auto" at SliderComponent.cpp:282 outside _(); es-untranslated the two tree-wide lines T33 printed, rc 0 each)
git -C "$W" grep -n -E '^msgid "(SWITCH TAB|up/down|CHOOSE|CHANGE|SELECT|WORKING\.\.\.)"$' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://" | cut -d: -f2,3 | tr '\n' ' '; echo; git -C "$W" show "$PIN:locale/lang/fr/LC_MESSAGES/emulationstation2.po" | sed -n '3708,3709p;4929,4930p'; git -C "$W" grep -c -E '^msgid ' "$PIN" -- locale/lang/fr/LC_MESSAGES/emulationstation2.po | sed "s/^$PIN://"; git -C "$W" grep -n -F '"Auto"' "$PIN" -- $FILES | sed "s/^$PIN://"
out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated rc=$rc"
out=$(tools/es-untranslated --es-src "$W" --upstream "$MB" 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated(cada) rc=$rc"
# the FAIL-at-pin lines (expect MultiLineMenuEntry `74 75` for the two setRowHeightPerc; TextComponent `486` for the doubled .y(); ComponentList `568` for the _("up/down"); HelpComponent setOpacity and mGrid `208 210 212 213 251`; Carousel moveCursorFast `74`; WebImage `81 190 197` -- `:134` tests a local `localFile`, not `mLocalFile`)
git -C "$W" grep -n -F 'setRowHeightPerc' "$PIN" -- es-core/src/components/MultiLineMenuEntry.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'mPadding.y() - mPadding.y()' "$PIN" -- es-core/src/components/TextComponent.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -F '_("up/down")' "$PIN" -- es-core/src/components/ComponentList.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -E 'setOpacity|mGrid->getChildCount' "$PIN" -- es-core/src/components/HelpComponent.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F '::moveCursorFast' "$PIN" -- es-core/src/components/CarouselComponent.cpp | sed "s/^$PIN://" | cut -d: -f2; git -C "$W" grep -n -E 'exists\(mLocalFile\)|getFileSize\(mLocalFile\)' "$PIN" -- es-core/src/components/WebImageComponent.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo
# the setOpacity callers (expect: no `mHelp->setOpacity` in Window.cpp -- its mHelp-> lines 745 1001 1009 1011 1012 1077 1397 1398; the tree-wide `setOpacity` lines 107 in es-core/src and es-app/src, the caller list the lane's, § 4 Q7)
git -C "$W" grep -n -F 'mHelp->' "$PIN" -- es-core/src/Window.cpp | sed "s/^$PIN://" | cut -d: -f2 | tr '\n' ' '; echo; git -C "$W" grep -n -F 'setOpacity' "$PIN" -- es-core/src es-app/src | sed "s/^$PIN://" | $G -c .
# the menu map (expect `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0 -- T33's proof's line at the same pin on the map at ce8608e38f, 989 lines; the map unchanged since)
out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"; wc -l docs/es-menu-map.md
# the compile (expect `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2; plain g++ on MenuComponent.cpp: rc 1 and `es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory`; with the fakes and the pugixml root the stand-in check over the 37, rc per file)
F=es-core/src/components/MenuComponent.cpp; out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc"
out=$(g++ -std=c++17 -fsyntax-only -DHAVE_INTL -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$F" 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 -E 'fatal error|error:'; echo "plain g++ rc=$rc"
PUGI=/workspace/cache/rocknix-sources/emulationstation/emulationstation-$PIN/external; test -d "$PUGI/pugixml/src" && echo "pugixml root present"
# STAGE C -- the lane's scripts, which do not exist at stage A (expect the include script's last lines: 352 quoted, 37 angle, es-app 1, 274 outside lines in 112 files; and the build script's own `TOTAL: N test cases in B binaries` with 0 failed, `components-tests` among the binaries, and before any fix the seven FAIL-at-pin cases reported FAIL by name)
python3 -I docs/audits/*-epic-m6-es-core-components/tools/t34-includes.py "$W" "$PIN" .qa-scratch/t34/paths.txt | tail -n 4
bash docs/audits/*-epic-m6-es-core-components/tools/t34-build-tests.sh "$W" 2>&1 | tail -n 10
# STAGE A, after the pointer is read -- the removal check: TIPHASH is the lane's own tip the pointer and the dispatch comment name (MERGE_HASH at stage A); the literal word fails with `fatal: bad revision 'TIPHASH'` (expect empty) and the ES diff against the pin (expect empty before stage E)
git diff --stat TIPHASH HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1
```

Settled by the proof of 2026-10-30 from the block's own lines:
`getHelpPrompts` 12 and inline `202 636`, `input(` 14, `named-0-times` 0,
the tree-wide `setOpacity` count 107, and the plain `g++` first error
quoted in its comment. The include-graph figures in the STAGE C comment are
the floor's and the membership digest's Python passes over `git grep`
output, reproduced by the includes run; the lane's `t34-includes.py` is the
first tool line.

## 6. Outputs

As T26's, T31's, T32's and T33's briefs § 6; § 7 is this section as
checkboxes. The folder `docs/audits/<yyyy_mm_dd>-epic-m6-es-core-components/`:
`00-running-log.md` to `05-punch-list.md`; `second-opinions/`
(`review-plan.json`, the probe's and the refutation's `.provenance.json`,
`packet-manifest.json`); `stage-a/` to `stage-e/` (the first commands and
the § 5 runs under `stage-a/`, with T31's 13 fakes and the lane's tenth
`SDL_power.h` under `stage-a/fakes/`; the window plan under `stage-b/`;
the host proofs under `stage-c/`; the walks' steps under
`stage-e/walks/`); `tools/` (the generators -- `t34-includes.py`,
`t34-build-tests.sh`, the tables' generators -- each asserting its counts
and each seen to exit 1 on a constructed drift before it is trusted);
`guest-cycle/`; the lint before D; the audit issue (`Audit: M6 T34
EmulationStation's core components -- N findings (...)`, a sub-issue of
#681; the audit issue and the bugs are the lane's, D-WORKFLOW-189; a
Backlog for a lead outside the 80 is the coordinator's, named in the
hand-back); and the retro at `docs/retros/<date>-m6-es-core-components.md`
(**what the slice did to the two time-to-play numbers**, § 3 item 10's
per-frame work priced from the guest and cited from `docs/vm-qa-log.md`,
never "nothing" by default; **what T35 to T37 inherit**, § 5 item 3).

**`02-forward-audit.md` carries these sections, in this order, each
generated section's row count stated as "generated, asserted" by the
script that made it:** § Coverage (80 rows, the path in backticks as the
first cell, both tiers: fork-added 0 / fork-modified 21 / upstream-carried
59 and inventory 21 / 59), § The leads (L-01 to L-21 and 3.1 to 3.34, each
with its lines, its family, who owns it, its disposition), § The layouts
(every size in the 80 computed from a size the pass wrote, and every
layout read of `Font::getHeight`, with the surface that shows it), § The
constants (the house values and every site that reads them; the pixel
constants with the panel each is right on), § The input (the 14 `input()`
and the 14 `getHelpPrompts` per component, each with the condition under
which it offers a direction), § The lifetimes (every `delete this`,
thread, detach, post and raw pointer held across a rebuild), § The reads
(10 rows plus the texture lookup and the `HttpReq`, with the writer and
what a stale answer reads as), § The words (the 22 lines, the 17 msgids,
L-01, 3.7, 3.13, L-18's formatters, the card's candidate shape), § The
structure (the one es-core to es-app include, the in-source gates against
the unconditional CMake lists, the non-ASCII byte, L-14, L-05's second
copy, `UntintedImageComponent`'s home, the map's checker line), § The
merge debt (one line: `cada856d86` the base against `rocknix/master`
`f6c542872e`, `bccd715707` its parent and the stale `upstream/master`, 0
upstream commits on the 80 of 14, 80 of 80 blobs identical MB to master,
batocera's eight since `1750dded8c` as the reconciliation list with the
`updateGrid()` overlap and the `setOpacity` guard), § The runs, § The
guest cycle, § The streams (stage E: **written by the coordinator after
stage D, as for T21, T26, T32 and T33**; the lane leaves the heading and
the pause's dispositions), § Positives, § The #585 lines owed (one per
upstream-carried defect closed under rule 6, in the shape the lane writes,
never sent; the six fork candidates named for the coordinator), § What T35
to T37 inherit; every proof with `proved:`. The stage-D pause as T21's:
the punch list posted on #681, the lane waits for the coordinator's
dispositions and any stream brief.

## 7. Acceptance

The checklist on #681 becomes this section at dispatch, written there by
the coordinator in place of P1's generated ones (its fifth, naming
`tools/renovation-status`, is replaced by checkbox 5 below as T33's was).
Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-core-components/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`, `second-opinions/`, `stage-a/` to `stage-e/`, `tools/` and `guest-cycle/` (`ls` of the folder in the hand-back).
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-core-components/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`), and the same with `--issue <audit issue>` prints `PASS`; Q1 to Q7 are answered in `04-analysis.md` and every punch item carries `question:` in the index.
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); its probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the scan block with every hit dispositioned by file:line (library plumbing / macro name / identifier / setting name) and no value, the 21 fork-modified files whole and every cited range of the 59 named; `00` shows exactly two keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #585, #649, #665, #667, #668, #673, #678, #679, #680, #682, #683, #63, #65, #1112, #1116, #1192, #1221, #1243, #1263, #1266, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail; the issue is closed by the coordinator at acceptance.
- [ ] `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in #681's header carry the lane's commits; the ES read is on the pin's bytes for the 80 files (`git -C <W> diff --stat 16dbac5211 <reviewed-at-es> -- $(cat .qa-scratch/t34/paths.txt)` empty before stage E) and nothing under the distribution's `packages/`, `projects/` or `tools/` changed at any stage against the lane's own dispatch tip (the pointer's merge hash, never `2174265e9c`).
- [ ] `01-research-notes.md` § Scope records § 2's block with its exact output lines (`mine: 80 paths.txt: 80 equal: True`; `lines: 21984 reach: {'shipped': 80} tier: {'upstream-carried': 59, 'fork-own': 21} lang: {'c++': 38, 'c-header': 42}`; `fork-own lines: 9541`; `read lines: 21984`; `wc -l 21971` and `grep -c 21984` with the thirteen files without a trailing newline; 80 at the merge base and 80 at the base; `21 files changed, 591 insertions(+), 114 deletions(-)` three times -- or the deltas beside them) and names `cada856d86` as the merge base against `rocknix/master` with `bccd715707` as its parent and `1750dded8c` as the base against `batocera/master`.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `80`; its tier columns read fork-added 0 / fork-modified 21 / upstream-carried 59 and inventory 21 / 59.
- [ ] `02` § The runs records the counts with both rules where they differ -- `_("` 22 lines in 12 files and 27 occurrences, 17 distinct msgids; `exists(` 10 lines in 5 files, 10 occurrences, 0 uncached; `std::thread` 1 and `.detach(` 1 (`VideoVlcComponent.cpp:91`, `:95`); `delete this` 4 (`OptionListComponent.h`); `postToUiThread` 2 (`TextEditComponent.cpp`); `HttpReq` 7 lines in 2 files; `getHelpPrompts` 12 `.cpp` definitions plus 2 inline; quoted includes 352 over 91 headers, angle 37, es-core to es-app 1; 274 outside include lines in 112 files; the 42 headers and 38 sources each named once in `es-core/CMakeLists.txt` -- each as a command's own output line, or the lane's figure with the command that differs named.
- [ ] `02` § The layouts, § The constants, § The input, § The lifetimes and § The reads are each generated or asserted by a script under the audit folder's `tools/` that names its row count ("generated, asserted"), and `02` § The runs records each script seen to exit 1 on a constructed drift before it was trusted.
- [ ] `02` § The layouts has one row per size computed from a size the pass wrote and per layout read of `Font::getHeight` (the eight: `MultiLineMenuEntry.cpp:52-56`, `SwitchComponent.cpp:14`, `OptionListComponent.h:255`, `:276`, `TextEditComponent.cpp:31`, `MenuComponent.cpp:393`, `TextListComponent.h:613`, `:725`), each with the surface that shows it and a disposition; `MultiLineMenuEntry.cpp:74-75`'s percentages and `TextComponent.cpp:338`/`:350` among them with the reproducer for #585.
- [ ] `02` § The constants has one row per house value (`BUTTON_GRID_HORIZ_PADDING` 0.022, `NOTIFICATION_OPACITY` 255, the card's 0.9 W centred, `DIMMED_ALPHA` 0x50) with its one definition, every reader and the frame that shows it at 640x480 and, for the bar and the card, at 1280x800; and one row per pixel constant in the 80 with the panel it is right on; `GuiTextEditPopupKeyboard.cpp:14`'s second copy recorded against `MenuComponent.cpp:7-13`'s claim.
- [ ] `02` § The merge debt is one line naming `cada856d86`, `rocknix/master` (`f6c542872e`), `bccd715707` as its parent and the stale `upstream/master`, the 0 upstream commits on the 80 of 14 since the base, 80 of 80 blobs identical between the base and master, 59 of 80 between the pin and master, and batocera's eight commits since `1750dded8c` on ten files (seven of them fork-modified, the one `updateGrid()` overlap, the `setOpacity` guard) as the reconciliation list only; T33's ES tip's delta inside the 80 recorded (empty, or named).
- [ ] `02` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason; the menu-map check's line, both `es-untranslated` lines, the catalog lines for `SWITCH TAB` and `up/down`, the C-locale non-ASCII count (1, `VideoVlcComponent.cpp:859`) beside `git grep -P`'s 0, the plain-`g++` first error quoted whole, the stand-in syntax check's rc per file over the 37 with the tenth fake and the pugixml root (VLC's two headers `CANNOT` or faked), and the unit build's `TOTAL: N test cases in B binaries` line with 0 failed are among them; every unit case the lane wrote has its FAIL-then-PASS pair recorded against the unfixed extract first, the seven FAIL-at-pin leads by name (3.4, 3.6, 3.7, 3.8, 3.16, 3.21, 3.26), and a candidate that PASSes at the pin is recorded as such, not as a defect.
- [ ] `02` § The guest cycle records the window the coordinator granted on #681 (the comment's time; the START and RETURN posts with their first-line contract and censuses, and the host file's lines beside them), the image by file name and `BUILD_ID` read from the guest at 640x480, G-01 to G-12 with their frames read back at EN and FR and each frame labelled by side (`image` or `pin-binary`), G-02's two pixel reads, G-03's 14 px and G-11's 28 px measured by a reader in the frames' columns, G-04's luminance ratio and the French bar's log count, G-05's four frames and the reopened page's pair, G-06's `OK` with no `CHOOSE`, G-09's glued suffix, G-07, G-08 (if no grid theme) and G-10 as `CANNOT` with the reason, the second boot at 1280x800, the disk retired with path, size and sha, the leftover check (`qemu 0, compilers 0`), and the window closed inside its bound plus grace.
- [ ] `00-running-log.md` shows no image build, no fetch (the council runtime from `npm install --offline`; `rocknix/master`, `batocera/master` and the lanes' ES tips read from the shared refs), no handheld, the owner's accounts never named or used, no hosted account, no M7 root, worktree or prep directory, the guest only inside the granted window, two keyed invokes and every other council call keyless, and nothing written under the ES worktree before stage E (`00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q7 are answered at their lines; every `bug` states its trace, its `Already written:` line (argued as *nothing inherited* where the component writes no file) and its VM line in one of the named families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` in the shape the lane writes; every row of § 2's take-up table has a disposition at its lines; the § 1 rulings (a) to (j) each have their `02` row.
- [ ] Every proof in `02` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; `02` § What T35 to T37 inherit lists § 5 item 3's ten items with their lines.
- [ ] The retro exists at `docs/retros/<date>-m6-es-core-components.md`, is posted on #681 with its heading's time from `date -u` in the posting command, says what the slice did to the two time-to-play numbers (the per-frame work of `ComponentList::render`, the func-form rows and the card priced from the guest, or `CANNOT` with the harness's reason; cited from `docs/vm-qa-log.md`), and what T35 to T37 inherit.
- [ ] The map: **the rows a stream added, the checker's line quoted, red if it cannot see them** -- this slice has no page of its own and proposes no row; if a stage-E stream adds, moves or renames a row on a page it touches, `docs/es-menu-map.md` changes in the same commit (D-UI-039) and `tools/es-menu-map-check --es-src <W> --ref <reviewed-at-es>` prints `0 missing` on the branch as handed back, with its full output line quoted in `02` § The structure; a title the checker reads from a member initializer and misses (#951, #965) is named there as unseen, and that is red, not `0 missing`.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch and the ES fork's `.githooks/pre-push-test` on the ES branch before the hand-back merge, and again on the coordinator's simulated merge; every fix on the ES branch has, recorded beside its commit, the covering unit case's PASS line (and its earlier FAIL), its French in the same commit where a sentence changed (3.7's `AUTO` included), `tools/es-syntax-check` PASS where a toolchain exists or else the stand-in `g++ -fsyntax-only` rc with the fakes and the pugixml root (or `CANNOT` with the missing header named), and a clean non-ASCII grep over its added lines.
- [ ] The unit build's `TOTAL: N test cases in B binaries` line is quoted in `02` § The runs and in the hand-back from the script's own output, with 0 failed in every binary's summary after the fixes, `components-tests` among the binaries, and the seven FAIL-at-pin leads' earlier FAIL lines (or their PASS-at-pin record) beside it.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back); the stage-D pause; an explicit maintainer
pause on #681; a blocker named on #681 (the seat failing its provenance
gate twice, a packet scan hit that is a value, two commands that disagree,
a block whose output differs from § 2's beyond the deltas it records, an
upstream-carried file that is not byte-identical to `rocknix/master`, a
pointer line that names the predecessor slice (§ 10); **not** the host's
missing toolchain, which § 5 names and the `CANNOT` forms absorb, **not**
the VLC headers the fakes lack, **not** a `components-tests` binary that
fails to build on the first try (the doubles are the lane's to extend),
and **not** the no-media guest's inability to show a video component or
a grid the theme does not draw, which § 5 names as the floor's limit); an
ES worktree that differs from the pin on any of the 80 files at stage A;
or an execution limit, stated as such with the running log current. A
checkpoint is not a stop. An idle session says it is idle on #681, **and
does not end a turn on a post that asks nothing**: a turn ends on a post or
a commit, never on "next is ..." (the T26 lane sat 28 minutes on exactly
that, friction 2026-10-27 10:48 UTC).

## 9. Ceremonies owed

The ceremonies every lane owes are the rules that load every session --
`learning-capture.md` (the work-log entry per session headed `#681`, its
time from `date -u` in the same command, `tools/work-log-index --write`
after it), `ceremonies.md` (a friction line the moment something slows,
`issue: #681` or the guard; `tools/ceremony-check --gate` before every
push, never `--no-verify`), `decision-register.md` (a row the same
session for any decision), `vm-first.md` (the VM question before any
proof: § 5 answers it), the mini-retro at stage G posted on #681 in
Instruction-Recommendations mode with its *adjustments* as proposals for
the coordinator -- and are not restated here. What is this slice's:

- **Four register rows expected, all put to the coordinator at the pause,
  never decided by the lane** (the ownership ruling of § 1 is the
  coordinator's own row, written at dispatch): whether the
  `TextComponent` padded-height root is fixed in the component or recorded
  with its reproducer (§ 1 f); whether `MultiLineMenuEntry.cpp:74-75`'s
  percentages are made to sum to 1 in the component or the gap is
  recorded (L-03); whether `ComponentList.cpp:11`'s 20 px becomes a screen
  fraction under D-UI-012's family or stays upstream's constant (L-06);
  and whether the `_("up/down")` fix leaves or removes the catalog's
  orphan `msgid "up/down"` (L-01). The highest IDs are § 3 item 2's (D-CLOUD-186, D-UI-128,
  D-UI-129 after D-WORKFLOW-212 and D-NET-017); `tools/register-check` is
  the proof; D-WORKFLOW-188 is on the P1 branch only and the merge unites
  them; a row this slice forces takes an ID the coordinator assigns on
  #681.
- **The same-commit rules, stated once:** a row added, moved or renamed
  updates `docs/es-menu-map.md` in the same commit and
  `tools/es-menu-map-check` passes before it (D-UI-039; this slice expects
  none); a sentence added or changed carries its French in the same commit
  (D-UI-051).
- **Every count is a tool's line** (`engineering-practices.md:250`): a
  figure in `02`, a post or the hand-back is the command's own output,
  quoted; a sum, a difference or a rate is computed by the command that
  prints it. **Every grep for `_("` by `-F`**; **no `cut` on an expected
  error line**; **a heading's time from `date -u`, never typed**.
- The ES fork's `.githooks/pre-push-test` after an ES change; a merge with
  conflicts is checked for markers; the ledgers united by whole entries;
  **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t34/` after `df -i`, never `/tmp`; the window's record
  kept on the branch, the guest disk retired after it with the retirement
  recorded in `00` (D-INFRA-022); **`rm -rf` only as `"${VAR:?}"/...` or a
  literal path, in its own short command, never inside a `bash -c`
  script**.
- A fixture that rewrites no path, in a bubblewrap sandbox started with
  `--clearenv`; the walks' steps under the audit folder's `stage-e/walks/`,
  never under `tools/`; the non-ASCII grep over a stream's added lines
  (`git diff -U0 HEAD -- <file>`, its `+` lines), an upstream hit recorded
  and not fixed; a generator seen to exit 1 on a constructed drift before
  its table is trusted.
- **Every edited file checked for an unfilled placeholder before its
  commit**: `/usr/bin/grep -c -E '__[A-Z]+__|\b(COHASH|MERGE_HASH|TIPHASH|V2HASH)\b'`
  is 0 on the pointer, the running log and every artifact (the T31
  dispatch entry shipped with its `__TS__`/`__URL__` placeholders unfilled,
  friction 2026-10-27 12:02 UTC).
- Commit messages `docs: ...` on the distribution branch, with `Refs #681`;
  on the ES branch the package's convention, `Refs #681, #<bug>`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#681's checkboxes against their artifacts; the lint's `PASS` line on the
default phase and with `--issue`; `review-plan.json` and the two
provenance files (read directly) and the manifest's scan block; the audit
issue's checkboxes all at an outcome; the coverage table's row count (80),
the generated sections' asserted counts, § The reads' 10 rows, § The
layouts' eight `getHeight` reads, § The merge debt's one line; every Q bug
with its three lines; **re-running on clones of both branches at their
tips under `/workspace/tmp/m6-coordinator/`: the membership block, every
§ 5 run in full and the unit build script** (no guest: the window's record
is read, not repeated); `register-check` on a simulated merge with the
coordinator's tip; the retro's answers; the five checkers' exit codes; the
collisions named against the two lanes' `AsyncNotificationComponent.h`
doubles and against T33's ES tip; **the § 1 rulings' rows in `02`**. The
lane posts one hand-back comment naming **both tips** and each artifact by
path, writes `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and
`fixed-at-es:` into #681's body, then says it is idle. After acceptance
the coordinator closes the audit issue, prompts the lane for
`audit-completion.json` and the lint against **the audit issue**, merges
the distribution branch in its turn after the M7 candidate with the pin
moved to the ES branch's tip in the same integration commit (the ES
package built before it lands), regenerates the ledgers, posts any #585
lines in the shape the lane wrote, files any Backlog the hand-back names,
and closes #681 when every row is proven -- which is also when #649, #665,
#667, #668, #673, #678, #679 and #680 close (§ 1); the interface epic #700
closes when its slices have.

**The pointer the lane checks at stage A, line by line.** The seeded
pointer `.github/sessions/saved-session-state-feature-m6-es-core-components-681.md`
is written by the coordinator from T33's, and T33's was seeded from T32's,
which carried a sentence of T26's. So before the first command after `cat`
the lane reads these eleven keys, each against the one value that would be
the seeding error, and reports any that name the predecessor on #681
before going on:

| Key | Must read | The seeding error reads |
| --- | --- | --- |
| `Branch (distribution):` | `feature/m6-es-core-components-681` stacked on `feature/m6-p1-survey-641` at the P1 tip the dispatch comment names (`2174265e9c` today) | `...-es-app-system-680` |
| `Worktree (distribution):` | the § 1 path ending `m6-es-core-components-681` | `m6-es-app-system-680` |
| `Worktree (EmulationStation):` | `W` of § 1, at the pin `16dbac5211` | another lane's checkout |
| `Executor:` | Opus 5.5 at high effort, the session the dispatch comment on #681 names | T33's session |
| `Epic:` | #700; T2, T18, T20, T21, T26, T31, T32 accepted and open until the integration merge; T33 in flight or accepted as the comment says; T35 to T37 and T44 after | "T33 accepted" before it is, or "T32 in flight" |
| `Depth:` | one seat, GPT-6 Astra at `max`; the 21 fork-modified files whole, the 59 upstream-carried by cited ranges; no binary in the 80 | 27 fork-added files, 4 modified by hunks, two binaries |
| `The lens:` | cost against value over 80 paths, `es-core/src/components/**` | the game lists, the collections, the helper units |
| `The rule:` | nothing under the distribution's `packages/`, `projects/` or `tools/`; nothing in the ES worktree at stages A to D; nothing outside the 80 at stage E | -- |
| `The host:` | the shared log and one guest window of 30 + 5 minutes with two boots | a 25-minute window, one boot |
| `Register:` | D-CLOUD-186, D-UI-128, D-UI-129 (after D-WORKFLOW-212, D-NET-017), plus the ownership row the coordinator writes at dispatch | the triple alone if the row was written, or an older triple |
| `The brief:` | `docs/reviews/briefs/es-core-components.md` at `V2HASH` (§ 1: filled by the dispatch comment) | `es-app-system.md`, or the literal word `V2HASH` |

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro takes a T34 kickoff addendum written by the coordinator with
this version; the stranger's proof of version 1 ran on 2026-10-30 and its findings
are the last section. This brief's hash at dispatch is `V2HASH`.

**What never runs in this slice:** an image build, a compiler beyond the
host's `g++ -fsyntax-only` (plain or with the fakes and the pugixml root)
and the generated test build, a fetch (the council runtime from `npm
install --offline`; `rocknix/master`, `batocera/master` and the lanes' ES
tips from the shared refs), a handheld, the owner's accounts or any hosted
account, a host listener on a privileged port, a guest before a grant on
#681, M7's roots, worktrees or prep directories, a change outside the 80
files, a change to `docs/es-menu-map.md`, the French catalog or the audit
folder except under a stream brief, a move of the pin, a line in
`es-core/src/guis/`, `Window.cpp`, `ThemeData.cpp`, `resources/`,
`utils/`, `HttpReq.*`, `CloudText.*`, `es-core/CMakeLists.txt` or
`tests/app-unit/fakes/` without the pause's ruling on its owner, a
deletion of `GuiTextEditPopupKeyboard.cpp:14`'s second constant, and a
fix to `VideoVlcComponent.cpp:859`'s byte.

## Corrections in version 2

A stranger's proof of version 1 (`a728d04c95`) on 2026-10-30 -- eleven commands,
every figure read at the pin by `git -C ... show|grep|diff|log|ls-tree|archive`
against the `qa-integration` checkout, at `2174265e9c` by `git show`, and at
`a8fe371b0a` for the rules, registers and map; 817 line checks, nothing
written to either tree, nothing posted; its record is the coordinator's
`t34-proof.md` -- found these, each corrected above in place (the line is
version 1's):

1. `:17`: T33's brief "version 2 at `b0c7e3f059`" -> version 2's commit is `c48f8b387e`; the blob is the same through `b0c7e3f059` and `a8fe371b0a`.
2. `:49-50`: the selector written as a list `[{...}]` -> one object, `{"globs": ["es:es-core/src/components/**"]}`.
3. `:649`, Version 1 item 8 (`:1746-1749`): `GuiLoading` under `es-core/src/guis/` as T35's -> `es-app/src/guis/GuiLoading.h`, in the inventory (upstream-carried, 143 lines), T31's by the block; `es-core/src/guis/` holds twelve files and no `GuiLoading`.
4. `:564`, `:617`, `:627`, `:1152`, `:1446`, `:1545`, `:1596`: `MultiLineMenuEntry.cpp:72-73` for the two `setRowHeightPerc` -> `:74-75` (`:72` is `float h = th + sh;`).
5. `:564`: "`mColor`/`mDimmed` `:18`, `:21`" -> `mDimmed` `:18`, `mColor` `:21`.
6. `:555`: the card's `push_back("")` at `:151`, `:161`, `:163` -> `:165`, `:174`, `:177`.
7. `:555`: `render` re-chooses "`:204-223`" -> `render` `:194`, the two blocks `:200-224`.
8. `:1166` (3.18): the width handed to `chooseThatFits` "`getScreenWidth() * 0.9f` less the grid's padding" at `:130-145` -> the row's own `getSize().x()` (`:138`), measured with its font (`:142`), `:136-145`; `0.9` is only `:55` and `:64`.
9. `:560`: the help bar's trailing spacer "`:159-165`" -> `isLast` `:160`, the spacer `:166`.
10. `:569`, `:1089`: the slider's second glued suffix "`:316-318`" -> `:312-313`.
11. `:569`, `:713`: `TextEditComponent.cpp`'s `applyChanges` `:176-185` -> no such symbol at the pin; `:176-189` is `input()`'s keyboard-RETURN branch ending in `stopEditing()` `:184`.
12. `:567`: `HttpReqOptions` "on the stack handed by pointer `:243`" -> built `:239`, handed `:243`.
13. `:1446`: the WebImage expectation `134 190 197` -> the grep prints `81 190 197` (`:134` tests a local `localFile`).
14. `:1446`: the HelpComponent expectation `208 212 251` -> `208 210 212 213 251`, § 2's own list.
15. `:1432`: "the six lines quoted" -> the command prints nine, `HelpComponent.cpp:130` among them; the uses at ANC `:64 :112 :276` and `ComponentList.h:26` are filtered out.
16. `:1440`: "`git grep -P` 0 rc=1 -- the UTF-mode miss" -> `1` rc 0 under the block's own `LC_ALL=C`; the miss is a UTF-8 locale's.
17. `:530`: the `updateGrid()` overlap "at base lines 142-150 (`-142` and `-145,4` in both)" -> hunks `-121,10` and `-135,17` (fork) against `-8,6`, `-119,7`, `-139,16`, `-310,4` (batocera): base lines 121-125 and 139-151.
18. `:555`: `CloudTextTests.cpp:832-854` "9 `CHECK`s" -> 8.
19. `:570`: `VideoVlcComponent.cpp` "`:2` the include guard" -> the `.h`'s `:1-3`; the `.cpp`'s `:2` is blank.
20. `:562`, `:1158`: `onCursorChanged` "`:1096-1200`" -> from `:1065`; `:1096` is a brace; `mStartPosition` `:1162-1186` stands.
21. `:703`: the decorator's `forScreenshot` "`GridGameListView.cpp:131-153`" -> `:42-46` (`:44`); `:131-153` is `getImagePath`.
22. `:217-223`, `:899`, `:1422`: T33's ES branch "not yet in the checkout's refs", its distribution branch `373e99281dce` -> on 2026-10-30 ES `dd86d7ce20a5`, distribution `0ee735862d6a`; empty inside the 80.
23. `:72`, `:283`, `:291-294`, `:1317`: the host file `/tmp/m7-m6-host-coordination-20261023.txt` -> absent since the reboot of 2026-10-28; `/workspace/tmp/m7-m6-host-coordination.txt` is the durable successor.
24. `:1234`, `:1452`: the plain `g++` first error `[unverified]` -> `es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory`, rc 1 (g++ 15.2.0), from a `git archive` of the pin: SDL before pugixml.
25. `:1256`: "eight invoke `g++ -fsanitize`" -> seven of the 15 name `fsanitize`.
26. `:559`: "`Vector4f(16, 16, 16, 16)`" -> `Vector4f(16.0f, 16.0f, 16.0f, 16.0f)`.
27. `:1170` (3.22): `resize` "`:87-180`" -> defined `:85`, body from `:87`.
28. `:856`: "the 18 `*.steps`" -> 18 at the top level, 22 with `tools/vm-walks/docs/`.
29. `:1463-1470`, `:253`, Version 1 item 2: the four unprinted expectations and the scan's bracket -> settled: `getHelpPrompts` 12 and `202 636`, `input(` 14, `named-0-times` 0, `setOpacity` 107 tree-wide.
30. `:581-585`: the 21 issue numbers' counts, with no rule -> by occurrence over subjects and bodies (the rule is now written; per commit #258, #210, #199, #191 are one each).
31. `:93`, `:574`: "one author" -> one by `%an`, two addresses by `%ae`.
32. `:497`: `batocera/master`'s hash with no date -> 2026-10-21, *update po*.

Everything else held -- the membership block's lines, the bases, the
80 lengths and the two line rules, the fork's and upstream's and
batocera's deltas, the lanes' tips, every other § 5 expectation, the 17
msgids, every rule, register, map, blindspot, futro, vm-qa-log, walk,
caller, test-tree and lane-audit line cited, the menu-map check's line at
the pin (the proof's held list is the record). Not checked: the tracker's
states, the host file's tail, the packet scan, the digests' reading of
the 33 subjects, `tools/es-untranslated` (T33's lines; a working tree),
the window plan's sum, "the other six pairs share no base line". Cut on
the proof's advice: the header's provenance story, the T33
guest-window status, § 2's "found sound" list (now the two facts the table
and § 5 do not carry), the nine-line re-citation before the L-table, § 4's
restated lanes, the block preamble's second description of the heredoc,
and the "Version 1" section, replaced by this one; the § 2 table, the
L-table, the floor's table and the runs block are kept whole, each being
the one copy the lane reads from.
