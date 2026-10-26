# Review brief: M6.P2 T26, EmulationStation's main menu, GuiMenu (#673)

**Version 1, 2026-10-26, the coordinator's** (D-WORKFLOW-189). Written from
four read-only research digests (the coordinator's scratch files, not in any
tree; every figure they gave is reproduced by a command below), the order's
§ T26, the slice record, and what T2, T18, T20 and T21 found or cited in
this file; the figures were produced at the hashes they name with
`/usr/bin/grep`, never the shell's function (#1138). A stranger's proof
runs before dispatch; version 2 records what it found
(`docs/reviews/plan-for-the-plan.md` § 6b).

## 1. Identity

- **Issue:** #673 `M6.P2 E700/T26: interface: EmulationStation's main
  menu (GuiMenu)`, slice `es-guimenu` (`k: 26`) in
  `docs/reviews/slices.json`, twenty-sixth in `docs/reviews/order.md` (its
  § T26 paths line: *"2 paths, 11,883 lines, 11,883 read, of which 11,883
  fork-own; 0 patch and config lines; reach shipped 2"*; its `why`: *"one
  file, 11,883 lines, the largest fork-own unit, where every fork page is
  reached from"*; kind read; lens new functionality, brittleness; depth
  Independent, *"an ordinary code slice"*; closing evidence *"audit folder,
  lint PASS, `tools/es-menu-map-check`, punch list through Phase 7"*).
  **Epic:** #700 (the interface: T2 #649 and T18 #665 accepted and closed
  out; T20 #667 and T21 #668 briefed; this slice; T31 to T37 and T44
  after), whose futro `docs/futros/2026-10-23-m6-interface.md` takes a T26
  kickoff addendum written with this version. **Milestone:** M6.
  **Predecessors:** #346, #641, **T2 #649** (the launch path: its PL-006 at `:11325`, the boot game's frozen command; its leads for this slice at `:11714-11738` and `:1842`), **T18 #665** (the cloud pages this menu opens; `GuiMenu.cpp` was not among its 30 covered paths, and its PL-17 and PL-21 halves were routed to #673 on 2026-10-26 at 11:13, its PL-01 and PL-03 cite `:5066` and `:5043-5045`, its forward audit assigned eight Python harnesses to this slice), **T20 #667** (the RetroAchievements gates at `:188-191` and the hasher started at `:1214` are read there for the account and the index, here for the menu; the relink page's RETROACHIEVEMENTS step is inside `:8261-8497`),
  **T21 #668** (the stores and the bridge: the relink rows `:8297`,
  `:8342`, `:8367`, `:8371`, `:8374`, the timezone at `:1890`, the journey
  record at `:5066`, the in-place write at `:11587`, the detached threads
  at `:9769`, `:9797`, `:9830` -- cited, not re-found), **T1 #648**
  (`setsettings.sh` reads what this menu writes to `system.cfg`), **T12
  #659** (`tools/cloud-input-test` drives the Wi-Fi page), and the menu
  map `docs/es-menu-map.md` (D-UI-039: a row added, moved or renamed
  updates it in the same change; `tools/es-menu-map-check` is the closing
  evidence). **Beside it:** whichever interface slice holds the running
  session; the host shared by `/tmp/m7-m6-host-coordination-20261023.txt`;
  a window for this slice is asked for on #673 and granted there in the
  queue.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of
  scope: those are the coordinator's, reached through #673, one question
  at a time. What it does file: its own audit punch-list issue (stage D)
  and a `bug` issue for a defect it proves, with its trace and `Already
  written:` line (D-WORKFLOW-187). A fix lands only under a stream brief
  the coordinator writes at the stage-D pause, **on the EmulationStation
  branch**. Both files exist in ROCKNIX's master `bccd715707` and are
  rewritten by the fork (`GuiMenu.cpp` 7,059 lines at the base, 11,747 at
  the pin: 5,124 insertions, 436 deletions over 225 fork commits; `.h`
  114 to 136, 23/1). A defect in a line the fork wrote is the fork's to
  fix; a defect in an upstream line is a contained fix under
  `bugs-are-agent-first.md` rule 6 and a #585 line (D-WORKFLOW-164, never
  sent, D-WORKFLOW-165). D-UI-079's lanes: the fork's pages in this file
  -- the cloud setup wizard, the cloud hub, the network and Wi-Fi pages,
  the relink page, the save rows, the RetroAchievements rows -- are the
  lanes the fork works in; an upstream page in the same file outside them
  is read for brittleness and left as upstream has it. The read is the
  pin `16dbac5211`'s bytes; M7's worktrees are never read.
- **Two worktrees, one session.** The distribution's
  `feature/m6-es-guimenu-673` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-guimenu-673`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the two hashes in the dispatch comment on #673); and the
  EmulationStation fork's `feature/m6-es-guimenu-673` at
  `/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673`,
  cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`**:
  the sources are read and the fixes are made there, and the pin is not
  moved by the lane. The other ES checkouts under
  `~/Development/emulationstation-next.worktrees/` are other lanes' and
  M7's: read with `git -C <checkout> show <hash>:<path>` only. Until the
  dispatch comment exists the pointer is not seeded and nothing starts.
- **Depth: Independent** -- one seat from another lab (plan § 6c,
  D-WORKFLOW-137; `adversarial-council.md`: an Anthropic-led audit's
  reviewer is pinned GPT-6 Astra): Astra at `max` over a trimmed, scanned
  packet (D-WORKFLOW-195 -- one file of 11,747 lines is most of the packet;
  trim the upstream regions the lens does not reach and say so in the
  manifest), a probe then one refutation (one in-call retry allowed);
  `review-plan.json` records depth `independent` and the one reviewer with
  its served model; **exactly two keyed `tools/council/run invoke` calls**,
  every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`;
  the runtime from `npm install --offline`, no fetch. The packet is scanned
  before it leaves: this file names `wifi.key`, the scraper's and
  RetroAchievements' settings and the cloud's keys by setting name, so the
  manifest records every scan hit and its disposition, and a hit that is a
  value stops the packet.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the distribution worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-guimenu-673
cat .github/sessions/saved-session-state-feature-m6-es-guimenu-673.md         # the pointer: the dispatch's two hashes
git status --short | wc -l                                                     # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                 # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                  # the pin; 0
git -C "$W" merge-base bccd715707 HEAD | cut -c1-10                             # bccd715707: the merge base with ROCKNIX's master
git show feature/m6-es-cloud-pages-665:docs/audits/2026_10_26-epic-m6-es-cloud-pages/05-punch-list.md | /usr/bin/grep -c '^## PL-'   # T18's punch list is reachable (23)
tools/register-check >/dev/null && echo register-ok
tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200             # who holds the host: no guest before a grant on #673
```

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{inventory.json,slices.json}`; the slice's `select` is one
object with one glob; `W` is the ES worktree):

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k = [s for s in sl["slices"] if s["k"] == 26][0]; sels = k["select"] if isinstance(k["select"], list) else [k["select"]]
def expand(g):
    mm = re.search(r'\{([^{}]*)\}', g)
    if not mm: return [g]
    return [x for alt in mm.group(1).split(",") for x in expand(g[:mm.start()] + alt + g[mm.end():])]
def m(p, g): return fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2]))
def pick(sel):
    globs = sel.get("globs") or []; tiers = sel.get("tier"); areas = sel.get("areas") or [k["area"]]
    es = [x[3:] for g in globs if g.startswith("es:") for x in expand(g)]
    return [r for r in rows if r["tree"] == "es" and r["area"] in areas and any(m(r["path"], g) for g in es) and (not tiers or r["tier"] in tiers)]
t26 = []
for sel in sels:
    for r in pick(sel):
        if r not in t26: t26.append(r)
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("selects", len(sels), "paths", len(t26), "lines", L(t26), dict(collections.Counter(r["reach"] for r in t26)), dict(collections.Counter(r["tier"] for r in t26)))
print(dict(collections.Counter(r["language"] for r in t26)))
os.makedirs(".qa-scratch/t26", exist_ok=True)
open(".qa-scratch/t26/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t26, key=lambda r: r["path"])))
for r in sorted(t26, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
PY
wc -l .qa-scratch/t26/paths.txt     # 2
W=/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673; PIN=16dbac5211eea7e70db7394372033be2be7df829
while IFS= read -r p; do printf '%6d %s\n' "$(git -C "$W" show "$PIN:$p" | wc -l)" "$p"; done < .qa-scratch/t26/paths.txt | awk '{s+=$1} END {print "wc -l lines", s}'   # 11883
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t26/paths.txt | wc -l   # 2: both are read as diffs against the base
git -C "$W" diff --numstat bccd715707 "$PIN" -- $(cat .qa-scratch/t26/paths.txt)    # 5124 436 GuiMenu.cpp; 23 1 GuiMenu.h
```

Expected, at `2174265e9c` (the coordinator ran it on a clone at that commit
with `W` the `qa-integration` checkout at the pin): `selects 1 paths 2 lines
11883 {'shipped': 2} {'fork-own': 2}`; languages `c++ 1, c-header 1`; `wc -l
lines 11883`; the merge-base count **2**; the numstat pairs 5124/436 and 23/1.

**The files, read whole** (lines at the pin):

| File | Lines | What it is |
| --- | ---: | --- |
| `es-app/src/guis/GuiMenu.cpp` | 11,747 | the main menu and every fork page, built in place: **156 function definitions at the pin against 60 at the base -- 97 added, 15 changed (`openNetworkSettings` +236/-95, `openGamesSettings` +78/-13, `openResetOptions` +69/-26 the largest), 1 removed (`openWifiSettings`), 44 unchanged** (the pages digest's parser over the two dumps; 38 hunks; 225 commits from 2026-07-24 to 2026-10-13, 142 of them in September); the added functions build twenty page titles -- the SYSTEM MANAGEMENT AND RESET helpers (`:296-392`), the content picker and its helpers (`:4086-4609`; `cloudContentSystemPicker` 317 lines), the LAST-row readers (`:4634-4827`), BACK UP TO / RESTORE FROM THE CLOUD (`cloudOpenTransferOptions` `:4836-5210`, 375 lines), the scan pages and the match (`:5219-5388`), the CLOUD hub (`:5437-5745`; `openCloud` 144 lines), the SSH wizard and its helpers (`:6222-6879`; `cloudSetupPresent` `:6484`, sixteen calls, every one the last statement of its caller and every callback handing the new page on), the folder pages (`:6883-7070`), the native provider form (`cloudRemoteShowForm` `:7220-7440`, 221 lines) and backend picker, the OAuth sign-in (`:7507-7922`; `cloudOAuthShowSignIn` 152 lines), the connections pages (`:7925-8160`), CLOUD STORAGE SETUP (`:8162-8242`), FINISH RESTORE PROCESS (`openRestoreRelink` `:8261-8497`, 237 lines), NETWORK SETTINGS and MANAGE SAVED NETWORKS (`:9744-10512`); **264 value-binding rows from 568 builder calls** (the settings digest's generator: 35 `addSwitch`, 30 of them to `Settings` and 5 to `SystemConf`; 6 `addOptionList`, all `Settings`; 15 `addInputTextConfigRow`; 5 `addFileBrowser`; 169 `addWithLabel`; 72 and 27 `addWithDescription`; 129 `addEntry`; 90 `addGroup`; 16 `addRow`), 260 store writes (152 `SystemConf`, 108 `Settings`; 68 dynamic keys), the store decided mechanically for 261 rows and by hand for 41; 96 literal `system.cfg` keys written here, 24 of them named by the OS scripts and the rclone package at `8ebaf8daad`, 4 written on both sides, **33 written by a row and read by nothing under `projects/ROCKNIX/packages`**, 15 read by a script with no row; **the ten longest functions**: `openSystemSettings` `:1697-3300` (1,604 lines, 148 row builders, 87 lambdas, 24 `#if`), `openThemeConfiguration` 674, `popSpecificConfigurationGui` 537, `openNetworkSettings` 494 (+101 by the fork over 30 hunks), `openDeveloperSettings` 483, `openGamesSettings` 446 (+65), `cloudOpenTransferOptions` 375 (fork-own, nesting depth 6), `addFeatureItem` 357, `cloudContentSystemPicker` 317 (fork-own), `openRestoreRelink` 237 (fork-own); **86 `#if` regions** (78 at the base) and, under the build's `-DROCKNIX=1 -DDISABLE_KODI=1` with BATOCERA off, about 930 lines (8%) compiled into no ROCKNIX image (753 BATOCERA, 124 `!ROCKNIX` first arms, 37 WIN32, 19 `_RPI_`, 19 KODI); 98 includes (71 at the base), 11 fork-own headers, the top include block repeated at `:99-102` and `GuiLoading.h` included under two spellings; **166 `_("")` literals used in two or more functions**; 109 `GuiMsgBox` constructions; 9 upstream commits to this file since the base (+155/-12, 14 hunks) against the fork's 148 hunks |
| `es-app/src/guis/GuiMenu.h` | 136 | the class (114 lines at the base; 23 insertions, 1 deletion): the fork's member declarations for the pages above (`openCloud`, `openCloudConnections`, `openCloudAddRemote`, `openCloudSetup`, `openRestoreRelink`, `openCloudFolderEditor`, ...); 63 `GuiMenu::` members are defined in the `.cpp` (91 file-statics and 2 free functions beside them); the lane matches the header's declarations against the definitions and names any declared member without one, or vice versa |

**The pages** (the pages digest). Every fork page is a function in this
file building a `GuiSettings` in place: the wizard's three steps and its
gate, the folder pages, the provider form, the sign-in with its QR page,
the connections pages, the hub, the transfer options and their picker, the
match, the relink page, the network pages, the maintenance rows. What the
digest checked and found sound, so the lane confirms rather than hunts:
**every wizard transition hands the new page on** (`:6683-6686`,
`:6737-6740`, `:6847`, `:6872`, `:7658-7670`, `:7919`, `:8217`, `:8223`,
`:8234-8235` -- the 2026-09-05 shape is gone); every button-bar rebuild
happens at build or is posted (`:4534-4545`, `:5165-5190` from switch
callbacks, `:7741`, `:7054`, `:8484`, `:6512-6519`); every fork YES/NO
confirmation is YES first and NO last (`:401-534`, `:4971`, `:5050`,
`:5249`, `:5381`, `:6137-6151`, `:6322`, `:7036`, `:10411`) and the
verb-first dialogs end in CANCEL (`:8025`, `:8039`, `:8058`) or NO
(`:7397-7435`); twelve uncached `exists` reads cover `rclone.conf`, the
stamps, the journey record and the restore marker (`:4645`, `:4843`,
`:5068`, `:5079`, `:5247`, `:5604`, `:5730`, `:6126`, `:6315`, `:8436`,
`:8475`, `:10261`); the `run` lambda copies `window` before `s->close()`
(`:4959-4967`); the picker's rebuild is weakly held (`:4529-4530`,
`:4584`); `CloudConnectionsPage` guards its posted refresh with `mAlive`
(`:5580`, `:5588`); `setrootpass` is quoted at all three sites (`:3272`,
`:6537`, `:8421`); no non-ASCII comment sits near a `_()`; every script
flag this file passes exists in the product scripts at `8ebaf8daad`.

What it found instead, the leads of § 4: **`exists(qrPath)` at `:7792` is
cached** on `/tmp/cloud-oauth-qr.png`, a file `rm -f`ed and rewritten by
`qrencode` on every sign-in attempt (`:7767-7793`; `runSystemCommand`
waits and returns 0 always, `Platform.cpp:868/876`) -- a first attempt
with no QR caches the miss for the session, a first attempt with one
caches the hit over a later failure; **`cloudSelectionRead` (`:4133-4137`)
reads the scan files through `isRegularFile`, which is cache-backed and
remembers a miss** (`FileSystemUtil.cpp:1164-1167`, `:138-148`) while its
own comment at `:4154-4156` says "uncached" (exposure narrow: every read
follows a `--stamp-valid` gate and `cloud_scan` writes all three files);
**synchronous process starts on the interface thread with no bound**,
several per page build -- `cloud_remote list` in `CloudConnectionsPage`'s
constructor and `topWindow` (`:5579`, `:5589`), `cloud_remote active`
(`:7060`), `fields`, `choices` per field, `subproviders`, `providers`
(`:7233`, `:7321`, `:7450`, `:7930`, `:8027`, `:8091`; `providers` runs
`rclone config providers`), `cloud_setup --connected` (`:6749`),
`--set-systems` on CONTINUE and BACK (`:4207`, whose start runs `rclone
listremotes`), `cloud_oauth status` (`:7813`, `:7848`) -- against the
wizard's own comment at `:6627-6630` that the `--check` is "the only slow
call"; **`GetShOutput` drops the last byte of every 256-byte chunk and
every newline** (`Platform.cpp:897-900`), and the fork reads `cloud_remote
create|update ... 2>&1` and `select|remove` through it, matching error
sentences by substring (`:7407-7414`, `:7419-7422`, `:7995`, `:7998-8001`,
`:7141-7155`; `OK=<name>` is the last stdout line, `cloud_remote:265`,
`:322`, so the name parse is safe; the `\r\n` search at `:7422` is dead);
the TRY AGAIN / CANCEL SIGN-IN dialogs (`:7702-7717`, `:7824-7827`) carry
no NO or OK, so back lands on CANCEL SIGN-IN, which closes the page and
cancels the session through `onFinalize` (`:6468-6478`) -- the one place
in the wizard where back leaves; the MANUAL UPDATES dialog (`:1511-1521`)
is sentence-case prose with a URL in a `GuiMsgBox`; `_(want.second.c_str())`
at `:8116` translates a runtime string xgettext cannot extract; two
shell-quoting functions with one algorithm (`cloudShellQuote` `:7183-7194`
and `Utils::String::shellQuote`); the three detached threads post through
the gated `AppWindow::post` (safe) while `queryInterfaceAddresses` has no
bound and can outlive `main` (`:9737-9738`, `:9769-9847`); and `#ifndef
CHEEVOS_DEV_LOGIN` at `:8354-8357` removes the WEB API KEY re-entry row on
a build with a compiled pair.

**The rows** (the settings digest). The generated table's counts are in
the file table above; what they hide is the shape of the leads. **A page
with only `addInputTextConfigRow` rows never writes a file by itself**:
`GuiSettings::save()` returns at `if(!mSaveFuncs.size())`
(`GuiSettings.cpp:88-89`) before it saves either store, and
`SystemConf::set` is memory-only (`SystemConf.cpp:439-464`), so the six
such pages (`:7223`, `:7890`, `:8296`, `:8352`, `:8370`, `:8391`) persist
only because the fork added `onFinalize` saves (`:8309`, `:8360`, `:8376`,
`:8393`) -- the next one will not, silently. **An empty OK clears a
credential**: `buildInputTextConfigRow`'s `updateVal` writes whatever the
editor returns with no non-empty or changed guard (`GuiSettings.cpp:218-238`),
the editor opens blank when `system.security.enabled=1` (`:245-248`), and
an empty `SystemConf` value deletes the line (`SystemConf.cpp:387-396`):
the rows at `:8297` (`wifi.key`), `:8353`/`:8356` (the RetroAchievements
password and key), `:8371`/`:8374` (the scraper account) and `:8392`
(netplay) have no guard; only DEVICE PASSWORD at `:8413-8423` guards, as
`es-ui-style-guide.md` § Saving says every credential row must. **ROOT
PASSWORD** (`:3261-3275`, SYSTEM SETTINGS > SECURITY, an upstream page the
fork's #198 touched) draws its value unmasked and runs `setrootpass
<value>` on every page close, changed or not, empty or not, against its
guarded twin on the relink page. **The VIDEO FILTER global row writes
`global.videofilters`** (`:5947`) while `setsettings.sh` reads
`videofilter` and the per-system row writes `.videofilter` (`:10990`), so
the global default never reaches RetroArch. **Writes at page open, before
any player action**: `system.battery.warning_threshold=25` when SOUND
SETTINGS opens (`:9655`, persisted at close), `audio.useFavoriteMusic=false`
plus `saveFile()` at open (`:9612-9613`), `system.timezone` seeded from
`timeinfo` and written at close (`:1857-1870`). The 33 unread keys include
the bezel and tattoo rows (`:5971-6019`), AUTOCONFIGURE CONTROLLERS
(`:6111`/`:6112`, `:11299`), PAUSE ON TRANSLATED SCREEN (`:6085`/`:6095`),
WIREGUARD (`:10316`), the splash rows (`:2799-2814`), the boot game
(`:1081`/`:11319`) and **`led.colour` (`:3038-3062`) against the scripts'
`led.color`** -- several gated and possibly never built, which a frame
decides. The four keys both sides write (`rocknix.bottomscreen.type`,
`system.automount`, `system.merged.device`, `system.suspendmode`) meet
`saveSystemConf`'s rewrite of only its changed keys under the shell's lock
(T21's). `cloudSetupPresent` (`:6484-6503`) sizes the 0.75-height wizard
pages without positioning them and they fit only because 0.15 + 0.75 =
0.90 (#540's shape, one constant away). `exitreboot` is set at `:1100` on
a page whose `onFinalize` (`:1457-1466`) reads only `reboot`; two labels
are not upper-cased in the source (`:10349` `ZeroTier One`, `:10860`
`Emulator`); 25 descriptions run past 60 characters, nine on fork lines
(`:1358`/`:9461` at 88 the longest); `ScrollLoadMedias` (`:9485`) is the one
`addSwitch(..., false)` that sends an ES-only key to `system.cfg`. The menu
map: `tools/es-menu-map-check` at the pin prints `55 screen(s) at
16dbac521, 31 in the map, 24 declared unmapped, 0 missing`; this file
builds 37 literal `GuiSettings` titles (plus 8 computed), all 37 in the
map, with one stale node name (FINISH RESTORE SETUP, D-UI-046's drift) and
86 row labels the map names that no `_("")` literal carries -- the lane
reads which are the map's prose and which are drift.

**The structure and the merge debt** (the structure digest). The counts
are in the file table; the shape: a page is one function, and the
largest build a page in one go -- `openSystemSettings` at 1,604 lines
with 24 `#if` arms inside it, and the two fork-own builders over 300
lines (`cloudOpenTransferOptions`, `cloudContentSystemPicker`) where
T18's PL-21 and PL-03 sites live. **Duplication in four families**:
upstream's global/per-system twins (`openGamesSettings` against
`popSpecificConfigurationGui`, 17 literal pairs), the theme-page and
UI-page twins, the system-page twins, and the fork's own repeats --
CONNECT CLOUD STORAGE as five titles, CHECKING... five times, CONNECTING
TO WI-FI four, **the FINISH RESTORE PROCESS row built in two menus
(`:5739-5741`, `:10269-10271`)**, the TURN OFF BOTH AUTOMATIC... sentence
on both sides of the process boundary, five `GuiMsgBox` texts built in two
or more places and **the NO CLOUD STORAGE IS SET UP gate three times
behind three different predicates (`:4969`, `:5247`, `:6315`)**; seven
identical code runs of six lines or more, all upstream's, the 13-line one
dead (`:1344-1362` under `!ROCKNIX` against `:9447-9465`); fork helpers
that overlap (`cloudSetupAddInfoRow`/`cloudAddCentredLine`,
`cloudAddDimmedRow`/`cloudSetupAddProse`: the prose-row inset decided two
ways); `cloudSelectionNotSaved` exists and `:5075` spells its sentence
again. **The Wi-Fi connect verdict is composed in two places with
different success behaviour** (`:10084-10090` against `:8320-8332`); three
copies of a `#if !WIN32`/`#else` lambda pair sit in `openNetworkSettings`
(six edits per change, the WIN32 arm dead); braces are opened under one
`#if !defined(ROCKNIX)` and closed under another in `openGamesSettings`
and `popSpecificConfigurationGui` (the digest's own parser tripped on
exactly this). **Compile and translation**: `g++ -fsyntax-only` fails at
`InputConfig.h:6` on `SDL_joystick.h` (`CANNOT`); 0 of 1,606 comment
lines carry a non-ASCII byte (40 string lines do), and the build runs
`xgettext --add-comments=TRANSLATION` with no `--from-code`
(`locale/CMakeLists.txt:9`), so the trap stands empty at this pin; 1,447
lines carry `_("`, 1,689 occurrences, 980 unique one-line literals (408
new at the pin), **French 978 of 980**, 0 fuzzy, the two absent being
upstream's RESET BATTERY FUEL GAUGE rows at `openResetOptions:517-518`,
live on every image. **The merge debt**: 9 upstream commits to this file
since the base; both sides changed `openNetworkSettings`,
`openResetOptions`, `openSystemSettings`, `popSpecificConfigurationGui`
and the `getCountryCodes`/`openWifiSettings` file scope; **a certain
conflict: upstream's `cada856d8` (*Refactor wifi menu, saving multiple
profiles*) deletes `openWifiSettings` and the SSID/KEY rows and drops
`baseSSID` from the apply conditions, inside lines the fork rewrote
thirty times, with a competing saved-networks design (`GuiManageNetworks`,
D-UI-118)**; the rest probably auto-merges; five new upstream rows will
need the map and the French. D-WORKFLOW-080's option (a) -- each
bucket's code out of `GuiMenu.cpp` into its own file -- is the shape this
slice records from these tables and does not do (#1143's family).

**The neighbours, and whose they are:** the pages this menu opens --
`GuiCloudTransfer`, `GuiCloudConflict`, `GuiCloudFolderEditor`, the
scan page -- are **T18's** (#665, accepted); `GuiWifi` and the stores
`Settings`/`SystemConf`, `ApiSystem`'s executors and `HttpReq` are
**T21's** (#668); the RetroAchievements pages and the hasher are
**T20's** (#667); `setsettings.sh`, `get_setting`/`set_setting` and
`wifictl` are **T1's** (#648, accepted); the cloud scripts this file runs
(`cloud_remote`, `cloud_setup`, `cloud_oauth`, `cloud_scan`,
`cloud_connections.py`) are **T17's** (#664, accepted) and T13's; the
scraper page `GuiScraperStart` is T32's; `Platform.cpp`'s `GetShOutput`
and `runSystemCommand` are `es-core`'s and read here only as the reader
this file's commands go through.

**Already found; do not re-find** (cited at its lines): T2's PL-006 (`:11325` stores the boot game's command, frozen; the getter saves `system.cfg`) and its two leads (`:11714-11738`, `:1842`); T18's PL-17 (the hub's BRING DATA BACK ONTO THIS DEVICE. and the match confirmation's DOWNLOADED, paraphrases where the verbs are *restore* and *back up*; the settings backup's chain discards `backuptool backup`'s output at `:5125`, its whys included, unlike the restore's at `:5043-5045`), PL-21's composers' half (`:5006` sets `rc` from any nonzero part, a 9 included, so a failed part followed by rclone's 9 ends 9 and reads COMPLETED; `:6140` skips the backup on a restore's 9; latent while no script passes `--error-on-no-transfer`), PL-01 (`:5066` already used `AtomicFile::writeText`), PL-03 (`backuptool`'s sentence reaches the restore page's line 4 through `:5043-5045`), its forward audit's P13 (`:5083-5096` dead `setFailedNote`/`setDismissedAction`), r11 (35 cached `exists()` reads in the callers, named as this slice's) and r17 (50 lines naming `/usr/bin/cloud_`); T20's `:188-191` (the RetroAchievements gates read `Settings`) and `:1214` (the hasher started on the interface thread); T21's `:1890`, `:5066`, `:8297`, `:8342-8374`, `:9769/:9797/:9830`, `:9857-9861`, `:11587`; blindspot 57's three `setrootpass` callers (#198; `tests/credential-quoting.py`); D-UI-046 against the map's `:405` heading. T19 found nothing in this file.

## 3. Read first

In this order, each read in this session, and `01-research-notes.md` says
which were read (`working-principles.md` § Pre-flight):

1. **The rules.** `es-native-ui.md`: § Spacing's `:189` (`CLOUD_SETUP_ROW_PADDING`
   lives in this file and nowhere else), the surface-tier table `:209` (the
   pages this menu's rows open), § Code conventions `:350-357` (`addSwitch`'s
   bool is `storeInSettings`; the PROGRESS TRACKER row) and **`:359-366`, the
   wizard page replacement rule** (`cloudSetupPresent(window, current,
   prev)` closes `prev`, `GuiSettings::close()` ends in `delete this`, a
   callback hands the new page on; the OAuth keyboard crash of 2026-09-05;
   `tests/cloud-oauth-lifetime.py` under ASan), § Core patterns' bullet *A
   file another process writes is read uncached* (the cloud rows read NOT
   DONE ON THIS DEVICE YET after a run had stamped, 2026-09-10), § The other
   files `:57-58` (six fork wizard pages found unmapped on 2026-09-18);
   `es-ui-style-guide.md`: `:110` (`cloudSetupAddInfoRow`, one non-selectable
   small row per line), § Size by weight (the wizard's SSH line a size too
   small), § Buttons (`clearButtons()`, EXIT SETUP left, CONTINUE by
   existence), § Confirmations (YES first; back lands on NO or OK, else the
   last button), § Wizards (push the new page, then close the old), and
   `:157`'s three stale line citations (`GuiMenu.cpp:4450`, `:4804`, `:5433`,
   from 2026-09-12 -- re-measured here); `es-player-text.md`: `:183` (a row
   that opens a page with more than one action is a submenu), `:207`
   (D-UI-023, two lines per row), `:238` (the three outcome words), `:331`
   (the card's action line names the row), `:168` (a `>>> why` sentence
   updates `CloudText::whySentences` and the French with its emitter, #512);
   `es-code-traps.md`: `:31` (a button bar rebuilt from a switch row's
   callback is fine, from a button never), **`:246-253` (#540: `getMenu().setSize()`
   resizes and does not move; verify the last line and both buttons in
   640x480 and 1280x800 frames, each locale)**, § Three things a font is not
   (the `exists` cache: the rclone.conf gate passed `false`, the
   restore-marker gates did not, ES `613f6152b`), the non-ASCII comment
   grep; `engineering-practices.md` `:570-573` (blindspot 23: the GAME
   SETTINGS save rows and the NETWORK SETTINGS cloud group deleted as
   duplicates), § Change stays inside the fork's lanes (D-UI-079);
   `player-language.md` and `least-surprise.md` whole.
2. **The register.** 44 rows name a page this file builds; the binding ones:
   D-UI-005 and D-UI-015 (one cloud entry, `GAME SETTINGS > CLOUD`; the
   NETWORK SETTINGS cloud group gone), D-UI-017/018/020 (the save rows and
   the hub's ticks stay; ticks remembered per direction), **D-UI-023** (a
   row is a label and at most one line), D-UI-028/030 (three outcome words),
   D-UI-033 (a transfer page that replaced the configuration owns the
   restart), D-UI-040, **D-UI-046** (the relink page and both rows that open
   it are called FINISH RESTORE PROCESS -- **the menu map's heading at `:405`
   reads FINISH RESTORE SETUP: a drift to settle at its lines**), D-UI-047,
   D-UI-051 (English and French), D-UI-053, D-UI-061/063/071/118/125 (the
   Wi-Fi rows: WI-FI NETWORK, the value is the network the device is on,
   the saved-Wi-Fi surface), D-UI-078/085/093/095, D-CLOUD-002 (native
   provider setup is the front door, the SSH wizard the fallback),
   D-CLOUD-048/050, D-CLOUD-074/077, D-CLOUD-084/085, D-CLOUD-113/129,
   D-CLOUD-160/161/166/167/169, **D-CLOUD-170/171 (the folder step at the
   wizard's end) against D-CLOUD-175/178/179 (#508/#510: the automatic
   migration retired, linking alone creates nothing)** -- which rows the
   wizard at the pin still builds is Q2's; D-NET-001/002/008; D-WORKFLOW-064.
   Open and this slice's to leave open: **D-WORKFLOW-080** (how the
   interface work goes upstream in pieces; its option (a) is to move each
   bucket's code out of `GuiMenu.cpp` -- the refactor this slice records
   the shape of and does not do, #1143's family), D-CLOUD-051, D-UI-120.
3. **The menu map** (`docs/es-menu-map.md`, 989 lines): `## Main menu`
   `:95`, `## What lives where` `:126` (`:145` read-only facts before
   editable settings; `:147` destructive work behind ADVANCED), `## Cloud
   (our subtree)` `:231`, the relink page `:405`, the 24 `## Not mapped`
   entries `:686-709` (upstream pages under D-UI-079, SECURITY among them
   with its note), **D-UI-039 at `:666-668`**, and the visual-evidence
   section `:26-82` (the baseline `d72084ccad` of 78 walk frames; the
   `evidence-index.json` schema: `flow_id`, `branch_id`, `document`,
   `anchor`, `trigger`, `expected_state`, `source`, `locale`, `width`,
   `height`, `frame`, `sha256`, `status`, `review`, `carried_forward_from`).
   `docs/conflict-wizard-ia.md` is `GuiCloudConflict`'s, not this file's.
4. **The blindspots** naming this file or its pages: 4 (`close()` inside a
   page's own handler; the wizard's CONTINUE crash of 2026-08-15; the guard
   is `cloudSetupPresent`'s order), 23 (deduplicating by deleting the
   frequent path), 29 (a feature that ships with no route), 33 (a sentinel
   borrowed from the wrapped tool's exit codes), 35 (a remedy built on an
   audit's claim about a default), 49 (an edit made blind to the compiler),
   50 (a log check that never asked whose log), **57 (a fix that covered
   fewer sites than its issue named: #198's three `setrootpass` callers in
   this file; guard `tests/credential-quoting.py`, the `quoting` suite)**,
   67 (a credential-shaped fixture reaching history).
5. **The tests at the pin.** No unit test compiles `GuiMenu.cpp`
   (`es-app/tests/unit/` 19 files, 221 cases, GuiMenu named only in
   `CloudTextTests.cpp` and `MaskSecretsTests.cpp`; `tests/app-unit/` 7
   files, 40 cases, none). **Nine Python harnesses under the ES repository's
   `tests/` extract this file's own functions by brace-matching and compile
   them with the host's `g++`** -- T18's forward audit assigned eight of
   them to this slice: `cloud-oauth-lifetime.py` (184 lines; the sign-in
   callbacks under `-fsanitize=address`, the phone, keyboard, no-browser and
   failed-start routes), `cloud-sync-last-run.py` (`cloudLastRunWhy` over
   stamps), `maintenance-why.py` (`maintenanceWhy`), `cloud-set-systems-quoting.py`
   (`cloudSetSystemsCommand` through `/bin/sh`), `cloud-gated-row.py`
   (`cloudAddGatedEntry`), `cloud-folder-reopen.py` (reads the source for
   the reopened row; no compiler), `cloud-content-selection.py` (the content
   picker), `cloud-oauth-await.py` (`cloudOAuthAwaitSession`) -- and
   `credential-quoting.py` (blindspot 57's guard) is the ninth; `wifi-profile-lifetime.py`
   is read for whether its subject is this file's. They are the host
   evidence floor (§ 5). `.githooks/pre-push-test` is the ES fork's guard
   test.
6. **The walks and the frames.** `tools/vm-walks/`: 18 `.steps` files;
   those naming this file's pages: `to-manage-cloud-storage.steps` (five
   lines: START opens MAIN MENU on GAME SETTINGS, MANAGE CLOUD STORAGE the
   last row of the CLOUD SETTINGS group, the RETROACHIEVEMENTS row above
   it), `ui-settings-toggle.steps`, `reset.steps`, `m7-cloud-sync.steps`,
   `m7-retro-achievements.steps`; `suite.txt` resets `cloudsync.pick.*` and
   the hub's two sync rows before each composition; `claims.txt` (564
   lines) entries on this file's pages at `:10-11` (CHANGE CLOUD FOLDER's
   line), `:25-27` (the editor holds `/pixelelated/Saves`), `:32` (the
   restore page's SETTINGS dimmed), `:57-68`, `:72-75`, `:89`; `masks.txt`
   masks the folder editor's caret (`confirm-cloud-folder/*`,
   `to-change-cloud-folder/*` at 416 222 432 272). The frames that exist:
   `docs/qa-logs/2026-10-11-network-cloud-management` (153 png, with
   `evidence-index.json`), `2026-10-08-cloud-folder-walks` (110),
   `2026-10-07-cloud-validator` (103), `2026-10-13-setup-qualification`
   (83), `2026-10-07-manual-cloud-setup` (76), `2026-10-15-wifi-remaining-result`
   (24), `2026-10-06-ra-ui` (69).
7. **The French**: 980 unique one-line `_("...")` literals in this file at the pin (1,689 occurrences on 1,447 lines; 408 new at the pin), 978 with a non-empty French `msgstr`, 0 fuzzy; the two without are upstream's RESET BATTERY FUEL GAUGE rows (`openResetOptions:517-518`), live on every image -- the structure digest's python pass, one-line msgids only; a changed
   string is `tools/es-untranslated --upstream bccd715707`'s.
8. **The audits**: T2's PL-006 (`:11325`, the boot game's frozen command;
   its MN-3 and FD-4) and its leads for this slice (`:11714-11738` the
   eject-drive boxes outside `_()`; `:1842` a keyboard layout in raw double
   quotes); T18's PL-17 and PL-21 (the two halves routed to #673 on
   2026-10-26 at 11:13 -- read that comment), PL-01 and PL-03 (`:5066`,
   `:5043-5045`), its forward audit's P13 (`:5083-5096`, dead `setFailedNote`
   and `setDismissedAction`), r11 (35 cached `exists()` reads), r17 (50
   lines naming `/usr/bin/cloud_`), the `>>> doing`/`tier`/`unit` emitters at
   `:5044`, `:5125`, `:5006`, `:6140`, `:6141`, `:5043`; T19's: none in this
   file; T20's brief (`:188-191`'s gates are this slice's; `:1214` the hasher
   on the interface thread); T21's brief (the relink and scraper rows, the
   timezone, the journey record, the in-place write, the detached threads).
9. **The issues**: #15, #27, #48, #63, #65, #102, #108, #115, #120, #147,
   #148, #149, #186, #187, #198, #241, #258, #303, #307, #512, #535/#536/#537,
   #540, #1143, #1145, #1147; #673's own comment of 11:13 (T18's notes).
10. **Time to play**: `docs/vm-qa-log.md:9-18` (the three headline columns);
    the measured rows of September (UI to game 0.6 to 1.11 s, exit sync
    1.06 to 1.56 s, game to game 1.0 to 2.04 s), `Not measured` on
    2026-10-14 and 2026-10-16; `time-to-play.md`'s one budget (the exit
    sync's 3 s, D-CLOUD-119) against `vm-qa-log.md:16`'s "no budget row"
    (D-CLOUD-116) -- a drift to name in the retro, not to settle here.

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of four families: **a page's lifetime or
thread** (a callback outliving its page, an unbounded call on the
interface thread), **a read that can be stale** (a cached `exists` or
`isRegularFile` on a file another process writes), **a row that writes or
reads the wrong place** (the store, the key, the script that reads it,
the reader of a command's output), **a word or a dialog that breaks the
house rules** (the verbs, the two lines, the case, the back landing, the
map). The leads below are the digests' by shape; each is read at its lines
before it is called anything.

- **Q1 The pages' lifetimes.** The sixteen `cloudSetupPresent` calls and
  what each callback captures (sound by the digest: confirmed, with the
  nine harnesses as the proof); the posted rebuilds; the three detached
  threads (`:9769-9847`: safe through the gated post, unbounded in
  `queryInterfaceAddresses`); `CloudHubRefresher` and `CloudConnectionsPage`'s
  `mAlive`; what `tests/cloud-oauth-lifetime.py` and `wifi-profile-lifetime.py`
  cover and what they do not (the folder pages' and the relink page's
  transitions have no harness).
- **Q2 The rows and their stores.** The generated table re-made by the
  lane's own generator (the digest's figures above are the expectation);
  the six `addInputTextConfigRow`-only pages and their `onFinalize` saves
  (the systemic fix belongs to `GuiSettings.cpp`, another interface
  slice's file -- a punch item for the pause); **the five unguarded
  credential rows** (a defect of the state kind: an untouched editor under
  `system.security.enabled=1` erases the key; the constructed positive on
  the guest, the guard in this file's row callbacks or in `GuiSettings`,
  ruled at the pause); ROOT PASSWORD's unmasked value and unconditional
  `setrootpass` (what `setrootpass` does with an empty argument is T1's
  file to read, cited); `global.videofilters` against `videofilter`;
  `led.colour` against `led.color`; the writes at page open; the 33 unread
  keys with a frame each or `gated: never built`; `ScrollLoadMedias`'
  store; `exitreboot` with no consumer; the wizard's folder step at its
  end (D-CLOUD-170/171) against the retired migration (D-CLOUD-175/178/179):
  which rows the pin still builds, and whether any still offers a join,
  follow or move.
- **Q3 The interface thread's bounds.** The synchronous starts in § 2
  (`cloud_remote list` in a constructor, `providers`, `fields` and
  `choices` per field, `--connected`, `--set-systems`, `cloud_oauth status`)
  -- each with what the player sees while it runs (nothing: no spinner, no
  card) and what bounds it (nothing); the hasher at `:1214`; the time-to-
  play line (§ 6): which of these sit between a press and a frame.
- **Q4 The reads that can be stale.** `exists(qrPath)` at `:7792` and
  `cloudSelectionRead`'s `isRegularFile` at `:4133-4137` against the
  twelve uncached reads; T18's r11 (35 cached `exists()` reads in the
  callers): a table of every `exists(`/`isRegularFile(` in this file
  with the file it reads, who writes it, and whether the read is cached;
  the constructed positive for the QR path (remount `/tmp` read-only, sign
  in, remount, sign in again in the same session).
- **Q5 The words and the dialogs.** PL-17's paraphrases (BRING DATA BACK
  ONTO THIS DEVICE., DOWNLOADED) against the two verbs; D-UI-046's name
  against the map's `:405`; the TRY AGAIN / CANCEL SIGN-IN back landing
  (a style call for the pause, not a defect); the MANUAL UPDATES dialog's
  case and URL (upstream's lane, recorded); the runtime msgid at `:8116`;
  `#540`'s taller pages (every `getMenu().setSize(` with or without a
  position, and the frames at 640x480); the French at 978 of 980 one-line literals with the two upstream rows named, and the non-ASCII comment grep at 0 of 1,606 (the 40 string lines with non-ASCII bytes read for which glyphs they are); the twenty page titles against `tools/es-menu-map-check`.
- **Q6 The commands and their readers.** `GetShOutput`'s dropped bytes
  against the substring matches on `cloud_remote`'s errors; the two
  shell-quoting functions (one algorithm; a refactor for the pause, not a
  hole); PL-21's composers (`:5006` sets `rc` from any nonzero part, a 9
  included; `:6140` skips the backup on a restore's 9; latent); PL-17's
  discarded `backuptool backup` output at `:5125` against the restore's
  kept output at `:5043-5045`; `credential-quoting.py`'s nine sites;
  every script flag against the product scripts (sound by the digest).
- **Q7 The structure and the merge debt.** The ten longest functions and
  what a page built in one 375-line function costs the next change (the
  two fork-own builders over 300 lines, with T18's sites inside them); the
  duplicates table (the 166 literals, the FINISH RESTORE PROCESS row in
  two menus, the one gate behind three predicates, the two helper pairs,
  `:5075`'s re-spelled sentence) with, per family, whether the copies
  differ; the `#if` map and the ~930 dead lines (recorded, D-UI-079: not
  removed here); the braces opened and closed under different `#if`s; the
  three `#if !WIN32` lambda copies; the Wi-Fi verdict composed twice; the
  nine upstream commits and the hunks the fork's edits overlap, `cada856d8`
  first -- the next merge's conflicts named with the fork's design that
  competes (D-UI-118); D-WORKFLOW-080's option (a) recorded as the shape,
  not done here (#1143's family; a Backlog the coordinator files from the
  lane's table).

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #673.** Every read, count and table runs on the host
   at the pin's bytes. **The host has no toolchain** (#1137): `GuiMenu.cpp`
   is `CANNOT` for the host's `g++ -fsyntax-only` (SDL through
   `Window.h`) and its compile proof is the integration build's;
   `tools/es-syntax-check` records its exit-2 line with `ES_BUILD_ROOT`
   set, never empty. **But nine Python harnesses under the ES repository's
   `tests/` extract this file's own functions by brace-matching and compile
   them with the host's `g++`** -- the coordinator ran all nine on an
   extract of the pin on 2026-10-26 and each passed (the lines in the runs
   block are their output); they are the host evidence floor, each run
   from the ES worktree at stage A with its exit and summary line recorded
   in `02` § The runs, and **a new case in one of them is the proof of
   choice for every pure lead** (a transition, a reader, a composer, a
   quoting). `tools/es-menu-map-check` (the closing evidence the order
   names), `tools/es-untranslated --upstream bccd715707`, the non-ASCII
   comment grep, the definitions parser and the generated rows table run
   on the host. `tests/wifi-profile-lifetime.py` is `GuiWifi.cpp`'s
   (T21's), not this slice's.
2. **The guest window** -- one, asked for on #673 at stage B's end with its
   plan and bound (45 minutes proposed), granted explicitly in the shared
   log's queue, one boot of the M6 copy of the image
   (`/workspace/artifacts/m6-t2-20261023/`, `069fc2704421`) **started at
   640x480** (`generic-x64-vm run --res`, #1141), the post contract
   `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line
   with the census, the stop by pidfile at bound plus grace, the disk
   retired after with path, size and sha (D-INFRA-022): the identity
   (`BUILD_ID`; the image's EmulationStation is M7's build, so every
   verdict labels the image's side, and a frame is `pin-binary` evidence
   only where the digest found the pin's lines unchanged against the
   image's -- else `image`); **the walks of the fork's pages** -- the hub,
   the wizard's three steps and gate, the folder pages, the provider form,
   the sign-in's QR page (with `qrencode` present and, for the Q4
   positive, `/tmp` remounted read-only for one attempt), the connections
   pages, the transfer options and the picker, the relink page, NETWORK
   SETTINGS and MANAGE SAVED NETWORKS -- at EN and FR with every frame's
   strings read back; **each confirmation's back-button landing** (the
   frame after B on each YES/NO and verb-first dialog, the TRY AGAIN /
   CANCEL SIGN-IN pair included); **the two stores read** from
   `system.cfg` and `es_settings.cfg` after a page close for every row Q2
   names; **the taller pages' last row and both buttons on screen** at
   640x480 for every page that calls `getMenu().setSize(` (1280x800 is
   `fix-walk-pending-image` until `vm-pair` has `--res`); the QA accounts
   only where a sign-in is needed (`tools/qa-accounts`, never printed;
   D-QA-016; never the owner's, D-QA-015). Every proof's frames are
   labelled by side; a fix's frame is `fix-walk-pending-image`.
3. **What T31 to T37 inherit** is written, not tested here: the page
   builders' pattern (one function per page, the transition rule, the
   posted rebuild), the rows' store rule, the readers' uncached-read rule,
   the commands' quoting through one function, and the table of upstream
   hunks the next merge will meet.
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   ES branch, proven twice (`fix-unit-test` through one of the nine
   harnesses or `fix-walk-pending-image`), the harness that covers the
   function run before every commit; **a row added, moved or renamed
   updates `docs/es-menu-map.md` in the same commit and
   `tools/es-menu-map-check` passes before it (D-UI-039)**.

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its
reason). From the distribution worktree after the membership block; `W` the
ES worktree, `PIN` the pin, `D` the distribution; counts by `/usr/bin/grep`
(#1138); `rc=$?` on its own line, never after a pipe:

```bash
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; C=8ebaf8daad; F=es-app/src/guis/GuiMenu.cpp
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t26/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
# the ES worktree at the pin, clean; the merge base; the delta (expect the pin; 0; bccd715707; 5124 436 GuiMenu.cpp and 23 1 GuiMenu.h)
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l; git -C "$W" merge-base bccd715707 HEAD | cut -c1-10; git -C "$W" diff --numstat bccd715707 "$PIN" -- es-app/src/guis/GuiMenu.cpp es-app/src/guis/GuiMenu.h
# the definitions (expect pin 156, base 60: added 97, changed 15, removed 1 -- openWifiSettings -- unchanged 44; the parser is the lane's, under the audit folder's tools/, a brace-matching pass over the two dumps; 225 commits in the range)
git -C "$W" show "$PIN:$F" > "$TMPDIR/pin.cpp"; git -C "$W" show "bccd715707:$F" > "$TMPDIR/base.cpp"; python3 -I docs/audits/*-epic-m6-es-guimenu/tools/t26-defs.py "$TMPDIR/pin.cpp" "$TMPDIR/base.cpp"; git -C "$W" log --oneline bccd715707.."$PIN" -- "$F" | wc -l
# the transitions and the rebuilds (expect cloudSetupPresent( on 17 lines, the definition at 6484 among them; the posted rebuild at 4534-4545; the sixteen calls each the last statement of its caller -- read, not counted)
git -C "$W" grep -n 'cloudSetupPresent(' "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" grep -c 'cloudSetupPresent(' "$PIN" -- "$F" | sed "s/^$PIN://"
# the reads of files other processes write (expect 12 lines with `, false)`; exists(qrPath) at 7792 without it; isRegularFile at 4133-4137; the comment "uncached" at 4154-4156)
git -C "$W" grep -n -E 'exists\(|isRegularFile\(' "$PIN" -- "$F" | sed "s/^$PIN://" | $G -c ', false)'; git -C "$W" grep -n -E 'qrPath|isRegularFile\(' "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo; git -C "$W" show "$PIN:$F" | sed -n '4154,4156p' | cut -c1-120
# the synchronous starts and the output reader (expect cloud_remote/cloud_setup/cloud_oauth lines including 5579 5589 7060 7233 7321 7450 6749 4207 7813 7848 7930 8027 8091; GetShOutput at 7133 and its callers)
git -C "$W" grep -n -E 'cloud_remote|cloud_setup|cloud_oauth' "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' ' | cut -c1-400; echo; git -C "$W" grep -n 'GetShOutput' "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the dialogs, the composers, the chain, the quoting (expect CANCEL SIGN-IN at 7702-7717 and 7824-7827; MANUAL UPDATES at 1511-1521; backuptool at 5043-5045 and 5125; the composers' rc at 5006 and 6140; setrootpass at 3272 6537 8421; cloudShellQuote at 7183; the runtime msgid at 8116; the two #ifndef at 8354 and 8372)
git -C "$W" grep -n -E 'CANCEL SIGN-IN|MANUAL UPDATES|backuptool|setrootpass|cloudShellQuote\(|want\.second\.c_str|#ifndef (CHEEVOS|SCREENSCRAPER)_DEV_LOGIN' "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' ' | cut -c1-400; echo
# the nine harnesses on the host (expect: maintenance-why: PASS; cloud-sync-last-run: PASS; cloud-oauth-lifetime PASS phone/keyboard/no-browser/failed-start; cloud-set-systems-quoting: 5 of 5 passed; cloud-gated-row: PASS; cloud-folder-reopen: PASS; cloud-content-selection: 14 of 14 passed; cloud-oauth-await: PASS; credential-quoting: 9 credential call site(s), 9 quoted, 0 bare; every rc 0 -- the coordinator's run of 2026-10-26 on the pin extract)
( cd "$W" && for t in maintenance-why cloud-sync-last-run cloud-oauth-lifetime cloud-set-systems-quoting cloud-gated-row cloud-folder-reopen cloud-content-selection cloud-oauth-await credential-quoting; do out=$(timeout 600 python3 -I "tests/$t.py" 2>&1); rc=$?; printf '%s rc=%s: %s\n' "$t" "$rc" "$(printf '%s\n' "$out" | tail -n 1 | cut -c1-120)"; done )
# the menu map and the French (expect `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` -- or the counts the lane finds, named; the es-untranslated summary line `N fork string(s) in the source, N with French, 0 without`)
out=$(tools/es-menu-map-check --es-src "$W" --ref "$PIN" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-menu-map-check rc=$rc"
out=$(tools/es-untranslated --es-src "$W" --upstream bccd715707 2>&1); rc=$?; printf '%s\n' "$out" | $G -m1 'fork string'; echo "es-untranslated rc=$rc"
# the non-ASCII comments and the compile (expect 0 with rc 1; es-syntax-check exit 2 on this host; g++'s first error names SDL)
git -C "$W" show "$PIN:$F" | $G -c -P '^\s*//.*[^\x00-\x7F]'; rc=$?; echo "non-ascii grep rc=$rc"
out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" "$F" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc"
out=$(g++ -std=c++17 -fsyntax-only -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$F" 2>&1); rc=$?; printf '%s rc=%s\n' "$(printf '%s\n' "$out" | $G -m1 -E 'fatal error|error:' | cut -c1-90)" "$rc"
# the rows (expect the lane's generator under the audit folder's tools/ to print its asserted counts: 264 value-binding rows from 568 builder calls -- addSwitch 35 (30 Settings, 5 SystemConf), addOptionList 6, addInputTextConfigRow 15, addFileBrowser 5, addWithLabel 169, addWithDescription 72+27, addEntry 129, addGroup 90, addRow 16; 260 store writes, 152 SystemConf and 108 Settings -- or its own figures with the method named; the raw builder counts by grep beside them)
python3 -I docs/audits/*-epic-m6-es-guimenu/tools/t26-rows.py "$TMPDIR/pin.cpp" | tail -n 3; for b in addSwitch addOptionList addInputTextConfigRow addFileBrowser addWithLabel addWithDescription addEntry addGroup addRow; do printf '%s %s\n' "$b" "$(git -C "$W" show "$PIN:$F" | $G -c -E "\b$b\(")"; done
# the credential rows, the stores' writers and the page-open writes (expect addInputTextConfigRow at 8297 8353 8356 8371 8374 8392 among the 15; onFinalize at 8309 8360 8376 8393; the guard at 8413-8423; setrootpass at 3272; global.videofilters at 5947 and .videofilter at 10990; led.colour between 3038 and 3062; warning_threshold at 9655; useFavoriteMusic at 9612-9613; timezone at 1857-1870)
git -C "$W" grep -n -E 'addInputTextConfigRow\(|onFinalize|global\.videofilters|\.videofilter|led\.colour|warning_threshold|useFavoriteMusic|system\.timezone' "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' ' | cut -c1-500; echo
# the keys both sides touch (expect 4 keys written by a row and by a set_setting: rocknix.bottomscreen.type, system.automount, system.merged.device, system.suspendmode; the scripts' videofilter and led.color names)
git grep -n -E 'set_setting (rocknix\.bottomscreen\.type|system\.automount|system\.merged\.device|system\.suspendmode)\b' "$C" -- projects/ROCKNIX/packages/rocknix/sources/scripts | sed "s/^$C://" | cut -d: -f1,2 | tr '\n' ' '; echo; git grep -n -E 'videofilter|led\.colou?r' "$C" -- projects/ROCKNIX/packages/rocknix/sources/scripts | sed "s/^$C://" | cut -d: -f1,2 | tr '\n' ' ' | cut -c1-300; echo
# the reboot flags and the sized pages (expect every setVariable/getVariable of reboot|exitreboot in GuiMenu.cpp; exitreboot set at 1100 and read nowhere but reboot at 1457-1466; setSize only in cloudSetupPresent 6484-6503, the 0.75 pages unpositioned)
git -C "$W" grep -n -E 'setVariable\("(reboot|exitreboot)"|getVariable\("(reboot|exitreboot)"' "$PIN" -- es-app/src | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' ' | cut -c1-400; echo; git -C "$W" grep -n -E 'getMenu\(\)\.(setSize|setPosition)|mMenu\.(setSize|setPosition)' "$PIN" -- es-app/src/guis | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the structure (expect the lane's analyser under the audit folder's tools/ to print: 156 definitions (63 members, 91 statics, 2 free); the ten longest with openSystemSettings 1697-3300 at 1604 lines first; 86 #if regions; about 930 lines in no ROCKNIX image; 166 literals in two or more functions; 109 GuiMsgBox; the FINISH RESTORE PROCESS row at 5739-5741 and 10269-10271; the NO CLOUD STORAGE gate at 4969 5247 6315)
python3 -I docs/audits/*-epic-m6-es-guimenu/tools/t26-structure.py "$TMPDIR/pin.cpp" | tail -n 12; git -C "$W" show "$PIN:$F" | $G -c -E '^\s*#\s*if'; git -C "$W" show "$PIN:$F" | $G -c 'new GuiMsgBox'; git -C "$W" grep -n -E 'FINISH RESTORE PROCESS|NO CLOUD STORAGE IS SET UP' "$PIN" -- "$F" | sed "s/^$PIN://" | cut -d: -f1,2 | tr '\n' ' '; echo
# the strings (expect 1447 lines with _(" ; 980 unique one-line literals; French 978 of 980 with RESET BATTERY FUEL GAUGE the two absent -- the lane's pass, one-line msgids)
git -C "$W" show "$PIN:$F" | $G -c '_("'; git -C "$W" show "$PIN:$F" | $G -o -E '_\("[^"]*"\)' | sort -u | wc -l; python3 -I docs/audits/*-epic-m6-es-guimenu/tools/t26-french.py "$TMPDIR/pin.cpp" <(git -C "$W" show "$PIN:locale/lang/fr/LC_MESSAGES/emulationstation2.po") | tail -n 3
# the merge debt (expect 9 upstream commits and +155/-12 since the base; the fork's 225 on the two files; cada856d8 among upstream's, touching openWifiSettings)
git -C "$W" log --oneline bccd715707..rocknix/master -- "$F" | wc -l; git -C "$W" diff --numstat bccd715707 rocknix/master -- "$F"; git -C "$W" log --oneline bccd715707..rocknix/master -- "$F" | $G -c cada856d8; git -C "$W" show --stat cada856d8 -- "$F" | tail -n 1
# the removal check from the dispatch tip -- <dispatch tip> is the lane tip the dispatch comment on #673 names (expect empty) and the ES diff against the pin (expect empty before stage E)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1
```

## 6. Outputs

As T21's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-es-guimenu/`:
`00` to `05`, `second-opinions/`, `guest-cycle/`, the lint before D, the audit
issue (`Audit: M6 T26 EmulationStation's main menu (GuiMenu) -- N findings
(...)`, a sub-issue of #673), the bugs, and the retro at
`docs/retros/<date>-m6-es-guimenu.md` (**what the slice did to the two
time-to-play numbers**: the main menu's build at START (`GuiMenu::GuiMenu`), a page close's save of both stores (`GuiSettings.cpp:94-95`) before a launch, and -- when a page is opened -- the synchronous script starts of Q3; cited from `docs/vm-qa-log.md` (the September rows: UI to game 0.6 to 1.11 s; `Not measured` on 2026-10-14/16) and named with their bounds; never "nothing" by default; **what T31 to T37 inherit**: the page builders' pattern, the
rows' store rule, the wizard's transition rule). **`02` carries § Coverage
(2), § The pages (one row per page this file builds: the title, the
function, the line range, what it opens, what it runs, its threads, its
confirmations' button order), § The rows (one generated row per settings
row: the builder, the label, the key, the store, the save mechanism, the
line), § The transitions (every `cloudSetupPresent` and page replacement:
what closes, what the callbacks capture), § The duplicates (every label
built in two functions), § The merge debt (what upstream changed in this
file since the base, against the fork's hunks), § The runs, § The guest
cycle, § Positives, and every proof with `proved:`.** The stage-D pause as
T21's: the punch list posted on #673, the lane waits for the coordinator's
dispositions and any stream brief.

## 7. Acceptance

The checklist on #673 becomes this section at dispatch, written there by
the coordinator in place of P1's generated ones. Every checkbox names the
artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-guimenu/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-guimenu/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`).
- [ ] `second-opinions/review-plan.json` records `depth: independent` and one reviewer (`gpt`, `openai/gpt-6-astra`, `max`); its probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the three-way scan with every hit dispositioned by name and the trimmed regions named; the running log shows exactly two keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #1143, #585, #648, #665, #668, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail.
- [ ] `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in the checklist's header carry the lane's commits; the ES read is on the pin's bytes for the two files (`git -C <W> diff --stat 16dbac5211 <reviewed-at-es> -- es-app/src/guis/GuiMenu.cpp es-app/src/guis/GuiMenu.h` empty before stage E) and nothing under the distribution's `packages/`, `projects/` or `tools/` changed at any stage.
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (2 paths, 11,883 lines; fork-own 2; both in the merge base; 5124/436 and 23/1 -- or the deltas beside them) and the definitions parser's line (156 / 60 / 97 / 15 / 1 / 44, or the lane's figures with the parser committed under `tools/`).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `2`.
- [ ] `02-forward-audit.md` § The pages has one row per page title this file builds (the title, the function, the line range, what it opens, what it runs and on which thread with what bound, its threads, its confirmations with the button back lands on), generated or asserted by a script under the audit folder's `tools/` that names its count (twenty by the pages digest, or the lane's count with its method).
- [ ] `02-forward-audit.md` § The rows is generated by a script under the audit folder's `tools/` (the generator asserts its row count and exits 1 on drift), one row per settings row: the builder, the label, the key, the store, the save mechanism, the line; with the keys both this file and an OS script at `8ebaf8daad` touch marked.
- [ ] `02-forward-audit.md` § The transitions has one row per `cloudSetupPresent` call and per page replacement outside the wizard (sixteen and the rest): what closes, what the callbacks capture, which harness covers it or `none`.
- [ ] `02-forward-audit.md` § The reads has one row per `exists(`/`isRegularFile(` in this file: the file, its writer, cached or not, and the line -- the twelve uncached and the two cached leads among them.
- [ ] `02-forward-audit.md` § The duplicates and § The merge debt are present: every label built in two functions with both lines; upstream's commits to this file since `bccd715707` and the hunks the fork's edits overlap, named; D-WORKFLOW-080's option (a) recorded as the shape.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason; the nine harnesses' lines, the menu-map check's line and the French summary line are among them.
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #673 (the comment's time; the START and RETURN posts with their first-line contract and censuses), the image by file name and `BUILD_ID` read from the guest at 640x480, the walks of the fork's pages with their strings read back at EN and FR and each frame labelled by side, each confirmation's back landing, the two stores after a page close for Q2's rows, the taller pages' last row and buttons on screen, the QR-path positive, the disk retired with path, size and sha, the leftover check.
- [ ] `00-running-log.md` shows no image build, no fetch (the council runtime from `npm install --offline`), no handheld, the owner's accounts never named or used, no hosted account but the QA ones, no M7 root, worktree or prep directory, the guest only inside the granted window, two keyed invokes and every other council call keyless (`00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q7 are answered at their lines; every `bug` states its trace, its `Already written:` line and its VM line in the four families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` in the shape the lane writes.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; `02` § What T31 to T37 inherit lists the builders' pattern, the rows' store rule, the readers' rule, the quoting function and the upstream hunks table with their lines.
- [ ] The retro exists at `docs/retros/<date>-m6-es-guimenu.md`, is posted on #673, says what the slice did to the two time-to-play numbers (the main menu's build, the page close's save of both stores and Q3's synchronous starts named with what they cost on the guest; cited from `docs/vm-qa-log.md`), and what T31 to T37 inherit.
- [ ] `tools/es-menu-map-check --es-src <W> --ref <reviewed-at-es>` prints `0 missing` on the branch as handed back, `docs/es-menu-map.md` changed in the same commit as any row a stream added, moved or renamed, and D-UI-046's name against the map's `:405` heading is settled at its lines (the map, the code, or a punch item saying which).
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch and the ES fork's `.githooks/pre-push-test` on the ES branch before the hand-back merge; every fix on the ES branch has, recorded beside its commit, the covering harness's PASS line, `tools/es-syntax-check` PASS where a toolchain exists or else the host `g++ -fsyntax-only` `CANNOT` with the missing header named, and a clean non-ASCII comment grep.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back); the stage-D pause; an explicit maintainer
pause on #673; a blocker named on #673 (the seat failing its provenance
gate twice, a packet scan hit that is a value, two commands that disagree, a
block whose output differs from § 2's beyond the deltas it records; **not**
the host's missing toolchain, which § 5 names and the `CANNOT` forms
absorb); an ES worktree that differs from the pin on either file at stage
A; or an execution limit, stated as such with the running log current. A
checkpoint is not a stop. An idle session says it is idle on #673, **and
does not end a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#673`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #673` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window granted on #673; the QA accounts only, never the
  owner's, D-QA-015/016; nothing on a handheld).
- The mini-retro at stage G, posted on #673, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (none
  expected); D-WORKFLOW-209 is the highest workflow row and D-RA-050 the
  highest row on the coordinator's branch (D-WORKFLOW-188 on the P1 branch
  only; the merge unites them); a row this slice forces takes an ID the
  coordinator assigns on #673.
- `tools/ceremony-check --gate` before every push of the distribution
  branch and the ES fork's `.githooks/pre-push-test` after an ES change;
  never `--no-verify`; a merge with conflicts is checked for markers; the
  ledgers united by whole entries; **a commit names its paths**; anything
  temporary under `/workspace/tmp/m6-t26/` after `df -i`, never `/tmp`; the
  window's record kept on the branch, the guest disk retired after it with
  the retirement recorded in `00` (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never inside
  a `bash -c` script**; **a row added, moved or renamed updates
  `docs/es-menu-map.md` in the same commit (D-UI-039) and
  `tools/es-menu-map-check` passes before it**; a fixture that rewrites no
  path, in a bubblewrap sandbox started with `--clearenv`; the walks' steps
  under the audit folder's `stage-e/walks/`, never under `tools/`.
- Commit messages `docs: ...` on the distribution branch, with `Refs #673`;
  on the ES branch the package's convention, `Refs #673, #<bug>`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#673's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the two provenance files (read directly) and the
manifest's scans; the audit issue's checkboxes all at an outcome; the
coverage table's row count (2), § The pages' rows, § The rows' generated
count, § The transitions' rows; every Q bug with its three lines;
**re-running on clones of both branches at their tips under
`/workspace/tmp/m6-coordinator/`: the membership block and every § 5 run in
full** (no guest: the window's record is read, not repeated);
`register-check` on a simulated merge with the coordinator's tip; the
retro's answers; the five checkers' exit codes. The lane posts one hand-back
comment naming **both tips** and each artifact by path, writes
`reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` into
#673's body, then says it is idle. After acceptance the coordinator closes
the audit issue, prompts the lane for `audit-completion.json` and the lint
against **the audit issue**, merges the distribution branch in its turn
after the M7 candidate with the pin moved to the ES branch's tip in the same
integration commit (the ES package built before it lands), regenerates the
ledgers, posts any #585 lines in the shape the lane wrote, and closes #673
when every row is proven; the interface epic #700 closes when its slices
have.

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro takes a T26 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.

**What never runs in this slice:** an image build, a compiler beyond the
host's `g++ -fsyntax-only` and a generated test build, a fetch (the council
runtime from `npm install --offline`), a handheld, the owner's accounts or
any hosted account but the QA ones the window names, a guest before a grant
on #673, M7's roots, worktrees or prep directories, a change outside the two
files, `docs/es-menu-map.md` and the audit folder except under a stream
brief, a move of the pin.
