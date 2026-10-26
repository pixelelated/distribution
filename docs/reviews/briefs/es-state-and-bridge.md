# Review brief: M6.P2 T21, EmulationStation's state primitives and its bridge to the OS (#668)

**Version 2, 2026-10-26, the coordinator's** (D-WORKFLOW-189; version 1 `601bd5d10f`; the stranger's proof's 21 corrections are listed at the end). Written from
four read-only research digests (the coordinator's scratch files, not in any
tree; every figure they gave is reproduced by a command below), the order's
§ T21, the slice record, T18's and T20's briefs and what their lanes and
research found on these files; the figures were produced at the hashes they
name with `/usr/bin/grep`, never the shell's function (#1138). A stranger's
proof runs before dispatch; version 2 records what it found
(`docs/reviews/plan-for-the-plan.md` § 6b).

## 1. Identity

- **Issue:** #668 `M6.P2 E700/T21: interface: EmulationStation's state
  primitives and its bridge to the OS`, slice `es-state-and-bridge`
  (`k: 21`) in `docs/reviews/slices.json`, twenty-first in
  `docs/reviews/order.md` (its § T21 paths line: *"14 paths, 9,249 lines,
  9,249 read, of which 9,249 fork-own; 0 patch and config lines; reach
  shipped 14"*; its `why`: *"`Settings`, `SystemConf` and `AtomicFileUtil`
  write `es_settings.cfg`, `system.cfg` and the last-good copies; `HttpReq`
  is the network client; `ApiSystem` assembles the shell commands every
  page runs, from player-entered strings (Wi-Fi, accounts); `GuiWifi` and
  `ScreenScraper` carry credentials. All are on the order's security or
  state lists, so they are cut out of their Independent slices into one
  Extended read"*; kind read; lens security, state preservation; depth
  Extended, *"security and state preservation (plan § 6c)"*). **Epic:**
  #700 (the interface: T2 #649 and T18 #665 accepted and closed out; T20
  #667 briefed; this slice; T26, T31 to T37 and T44 after), whose futro
  `docs/futros/2026-10-23-m6-interface.md` takes a T21 kickoff addendum
  written with this version. **Milestone:** M6. **Predecessors:** #346,
  #641, **T18 #665** (the host has no toolchain, #1137; the unit tests by a
  generated `g++` command; its S2 moved `writeStamp` onto
  `Utils::AtomicFile::writeText`, this slice's primitive; its Backlog #1143
  names one reader for both surfaces), **T20 #667** (its research filed
  **#1154** -- `HttpReq.cpp:192` never verifies the TLS peer -- and found
  `ask()`'s `WEXITSTATUS` without `WIFEXITED` at `ApiSystem.cpp:2278-2291`,
  `executeScriptLegacy`'s echo of every stdout line at `:2284`,
  `maskSecrets` at `:2235`, `:2265`, `:2297`, and `Settings.cpp:420`'s
  `.hardcore` default: all this slice's lines, cited not re-found), **T1
  #648** (`setsettings.sh` and `add_setting`, the other end of `system.cfg`:
  PL-004 the backgrounded first test), **T17 #664** (`backuptool`'s
  SECRETLIST and RATOKENSETTINGS on `system.cfg`'s keys), **T15 #662**
  (`tools/last-good-scripts-test`'s `system.cfg` cases under busybox,
  blindspot 34), **T14 #661** (`tools/settings-modes-test`, #421), **T12
  #659** (`tools/cloud-input-test`, the Wi-Fi selection under delayed HTTP,
  #535/#536), **T22 #669** (the services that read `system.cfg` at boot).
  **Beside it:** T19 or T20 in the running session; the host shared by
  `/tmp/m7-m6-host-coordination-20261023.txt`; a window for this slice is
  asked for on #668 and granted there in the queue.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of scope:
  those are the coordinator's, reached through #668, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already written:`
  line (D-WORKFLOW-187). A fix lands only under a stream brief the
  coordinator writes at the stage-D pause, **on the EmulationStation
  branch**. All fourteen are the fork's own by the inventory's commit share; twelve exist in ROCKNIX's master `bccd715707` and are rewritten (`git diff --numstat`, the pair's insertions/deletions: `ApiSystem.*` 251/34, `HttpReq.*` 25/0 (the whole delta is `stallTimeout`), `GuiWifi.*` 628/76, `ScreenScraper.*` 126/8, `Settings.*` 104/9, `SystemConf.*` 332/54), and `AtomicFileUtil.*` is new (829/0 and 215/0); 14 files, 2,510 insertions, 181 deletions. A defect in a line the fork wrote is the fork's to fix; a
  defect in an upstream line is a contained fix under
  `bugs-are-agent-first.md` rule 6 and a #585 line (D-WORKFLOW-164, never
  sent, D-WORKFLOW-165) -- #1154 is that shape and already filed. D-UI-079's
  lanes: `HttpReq`, `ApiSystem`, the two stores and the Wi-Fi page are the
  lanes the fork has worked in; the scraper is read for its credentials
  and changed only where a credential is at risk. The read is the pin
  `16dbac5211`'s bytes; M7's worktrees are never read.
- **Two worktrees, one session.** The distribution's
  `feature/m6-es-state-and-bridge-668` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-state-and-bridge-668`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the two hashes in the dispatch comment on #668); and the
  EmulationStation fork's `feature/m6-es-state-and-bridge-668` at
  `/home/max/Development/emulationstation-next.worktrees/m6-es-state-and-bridge-668`,
  cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`**:
  the sources are read and the fixes are made there, and the pin is not
  moved by the lane. The other ES checkouts under
  `~/Development/emulationstation-next.worktrees/` are other lanes' and
  M7's: read with `git -C <checkout> show <hash>:<path>` only. Until the
  dispatch comment exists the pointer is not seeded and nothing starts.
- **Depth: Extended** -- two seats, as T18's and T20's stage C: GPT-6 Astra
  at `max` over a trimmed, scanned packet (D-WORKFLOW-195), a probe then one
  refutation; then Gemini 4 Argon at `high` over the same packet plus the
  lane's grades of Astra, a probe then one refutation (one in-call retry
  allowed); `review-plan.json` records depth `extended` and both reviewers
  with their served models; **exactly four keyed `tools/council/run invoke`
  calls**, every other `tools/council/run` call with
  `COUNCIL_ENV_FILE=/nonexistent`; the runtime from `npm install --offline`,
  no fetch. **The packet is scanned before it leaves:** these files name
  the Wi-Fi key, the scraper's developer pair and account, and the
  RetroAchievements keys by setting name (the Wi-Fi key (`wifi.key`), the scraper's `ScreenScraperPass`/`DevPass`/`User`, the RetroAchievements keys and `IGDBSecret` appear as setting names and query-parameter names -- read as counts only; the dropping filter `grep -v -i -E 'key|pass|token|user|psk'` lets `IGDBSecret` and `ScreenScraperDevId` through, so the packet scan reads those by name too), so the manifest records every
  scan hit and its disposition, and a hit that is a value stops the packet.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the distribution worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-state-and-bridge-668
cat .github/sessions/saved-session-state-feature-m6-es-state-and-bridge-668.md  # the pointer: the dispatch's two hashes
git status --short | wc -l                                                        # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                    # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-state-and-bridge-668; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                     # the pin; 0
git -C "$W" merge-base bccd715707 HEAD | cut -c1-10                                # bccd715707: the merge base with ROCKNIX's master
git show feature/m6-es-cloud-pages-665:docs/audits/2026_10_26-epic-m6-es-cloud-pages/05-punch-list.md | /usr/bin/grep -c '^## PL-'   # T18's punch list is reachable (23)
tools/register-check >/dev/null && echo register-ok
tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200                # who holds the host: no guest before a grant on #668
```

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, stacked on the P1 branch, which holds
`docs/reviews/{inventory.json,slices.json}`; the slice's `select` is one
object with five globs; `W` is the ES worktree):

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k = [s for s in sl["slices"] if s["k"] == 21][0]; sels = k["select"] if isinstance(k["select"], list) else [k["select"]]
def expand(g):
    mm = re.search(r'\{([^{}]*)\}', g)
    if not mm: return [g]
    return [x for alt in mm.group(1).split(",") for x in expand(g[:mm.start()] + alt + g[mm.end():])]
def m(p, g): return fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2]))
def pick(sel):
    globs = sel.get("globs") or []; tiers = sel.get("tier"); areas = sel.get("areas") or [k["area"]]
    es = [x[3:] for g in globs if g.startswith("es:") for x in expand(g)]
    return [r for r in rows if r["tree"] == "es" and r["area"] in areas and any(m(r["path"], g) for g in es) and (not tiers or r["tier"] in tiers)]
t21 = []
for sel in sels:
    for r in pick(sel):
        if r not in t21: t21.append(r)
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("selects", len(sels), "paths", len(t21), "lines", L(t21), dict(collections.Counter(r["reach"] for r in t21)), dict(collections.Counter(r["tier"] for r in t21)))
print(dict(collections.Counter(r["language"] for r in t21)))
os.makedirs(".qa-scratch/t21", exist_ok=True)
open(".qa-scratch/t21/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t21, key=lambda r: r["path"])))
for r in sorted(t21, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
PY
wc -l .qa-scratch/t21/paths.txt     # 14
W=/home/max/Development/emulationstation-next.worktrees/m6-es-state-and-bridge-668; PIN=16dbac5211eea7e70db7394372033be2be7df829
while IFS= read -r p; do printf '%6d %s\n' "$(git -C "$W" show "$PIN:$p" | wc -l)" "$p"; done < .qa-scratch/t21/paths.txt | awk '{s+=$1} END {print "wc -l lines", s}'   # 9249
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t21/paths.txt | wc -l   # the files that exist in ROCKNIX's master: read as diffs
```

Expected, at `2174265e9c` (the coordinator ran it on a clone at that commit
with `W` the `qa-integration` checkout at the pin): `selects 1 paths 14 lines
9249 {'shipped': 14} {'fork-own': 14}`; languages `c++ 7, c-header 7`. The merge-base line's count is **12** (`AtomicFileUtil.cpp` and `.h` are new); the block prints it.

**The files, read whole, in this order** (lines at the pin):

| File | Lines | What it is |
| --- | ---: | --- |
| `es-app/src/ApiSystem.cpp` / `.h` | 3,519 / 490 | the bridge, upstream's file (`bccd715707` an ancestor; +251/-34 over 19 fork commits: `timeout N` on the `wifictl` calls but four (`:642` `enable <ssid> <key>`, the key on argv with no bound; `:767`, `:771`, `:775`), `launchCloudSignIn`'s three `system("/usr/bin/cloud_oauth ...")` literals, `maskSecrets` on the eight command-line log lines, the zeroed output buffer at `:2310`); four executors -- `executeEnumerationScript` `:2233-2252` (`popen`, every line, **the exit discarded at `:2251`**: a failed script equals an empty list, so `getBiosInformations` reports no BIOS problem when `rocknix-systems` fails, at launch when CHECK BIOS AT LAUNCH is on -- `CheckBiosesAtLaunch`, default false, `Settings.cpp:207`; `ViewController:507-509`), `executeScriptLegacy` `:2263-2292` (every stdout line echoed to `std::cout` at `:2284`, unmasked -- and ES's stdout is the journal: `emustation.service:12` has no `StandardOutput`), `executeScript(func)` `:2295-2320` (the **last line** as `pair.first`), `executeScript(bool)` `:2323-2333` (`system()`, the child's output inheriting ES's stdout); **`WEXITSTATUS` without `WIFEXITED` at eleven sites** (`:234`, `:270`, `:293`, `:329`, `:354`, `:397`, `:415`, `:440`, `:469`, `:2291`, `:2319`; only `:528`, `:585`, `:607` check it): a signal-killed child reads as exit 0; `shellQuote` at 13 sites, all `wifictl` (the SSID, key, country and profile paths safe); **double-quoted external strings at 16 functions** (the file's own comment `:631-634`: double quotes are not enough), live on this image for `7z` over a ROM path (`:1527`, `:1578`, `:1659`) and poppler over a manual's path (`:2509`, `:2593`), the rest calling scripts absent from the distribution; bare external strings from script output (`:800-815`, `:884`, `:984`) and from a network-fetched bezel list (`:1484`, `:1489`); `FILE*` and the child leaked when a command prints nothing (`:942-953`, `:1109-1122`, `:1160-1173`); `getRootPassword` `:1029-1037` returns `root.password` or the literal default; 105 lines name a `batocera-` script (36 distinct names), and `keyboardToPads`, `rocknix-sync`, `rocknix-resolution`, `pm-*` and `set-audio` are absent at `8ebaf8daad`; the p7zip recipe builds `all3` and installs `bin/7z*` (`:37`, `:43`), so whether the `7zr` that `getSevenZipCommand()` returns and the NETPLAY gate wants is on the image is the window's `ls /usr/bin/7z*`, not a finding; `GuiLoading` wraps the Wi-Fi apply, bluetooth, BIOS, PDF and nfc calls, while the timezone, audio, storage, service, hotkey and LED setters, `getVideoModes` at page build and `getBiosInformations` at launch with that setting on block the interface thread with no bound; 293 lines in 41 files call `ApiSystem::getInstance()->` (`git grep -c`) |
| `es-core/src/HttpReq.cpp` / `.h` | 644 / 180 | the network client: one process-wide `curl_multi` (`:21`) with **no network thread** -- `curl_multi_perform` runs inside `status()` on whichever thread calls it under the static `mMutex` (`:19`, `:397`), and one caller's `status()` completes other objects' requests (`:412-523`); `HttpReqOptions` defaults (`.h:45-88`): connect 10 s, `timeout` 0 (unbounded), `stallTimeout` 0, a cookie jar at `<ES dir>/tmp/cookies.txt` (`:96-103`, `:287-288`), a spoofed Firefox user agent (`.h:30`); `FOLLOWLOCATION` 1 with `MAXREDIRS` 2 over `http,https` (`:183`, `:222`, `:240`); **`VERIFYPEER` 0 at `:192` (#1154, cited) and `VERIFYHOST` 0 on the client-certificate path (`:200`)**; `TIMEOUT_MS` only when > 0 (`:206`), `LOW_SPEED_*` only when `stallTimeout` > 0 (`:211-213`); **no response-size bound**; `onError` (`:559-563`) logs the status and message and never the URL, but for 400 to 503 the message is **the server's body verbatim** (`:443-459`) into `es_log.txt`; the fork's whole delta against the base is `stallTimeout` (`9202ebed5`, #299) -- the verify lines are upstream's |
| `es-core/src/SystemConf.cpp` / `.h` | 494 / 94 | `system.cfg`, the launch scripts' store (332 insertions, 54 deletions against the base; 11 of its 15 commits in the range on 2026-09-28): `saveSystemConf` `:304` through `saveUnderLock` (the `PidLock` at `/tmp/.system.cfg.lock`, 5 s; `LockBusy`, `Unreadable` and `WriteFailed` keep the change in memory), then `recordLastGood` `:86-112` reacquires the lock and re-reads the disk before writing `.backup` (#320); the live mode kept (`:107`; the comment at `:100` on the build that made 0644); `:210` sweeps `system.cfg.backup.tmp`, the name `chksysconfig backup` writes at boot; it forwards to `Settings` when `mSystemConfFile` is empty (`:288`, `:426`, `:442`, `:469`, `:480`; the path from `Paths::getSystemConfFilePath()`, `:58`; `:19-25` is `mapSettingsName()`), the case `Settings.cpp:420`'s `.hardcore` default serves (`#if WIN32`, `:417-433`); its own defaults table carries `global.retroachievements.hardcore` `"0"` (`:46`) -- the lane reads `Paths` for whether that path can be empty on ROCKNIX before calling it not a second live store (T20's lead, Q4); the one key with a live default on both sides otherwise is `audio.bgmusic` (`Settings.cpp:402` / `:42`) |
| `es-core/src/Settings.cpp` / `.h` | 723 / 165 | `es_settings.cfg`, EmulationStation's own store (209 commits, upstream's file): `saveFile` `:524` (live) and `:533` (`.backup`, the live file's mode) through `AtomicFile::writeText`, **with no lock on either side** and no mutex on the maps for a save from a worker thread; the live file **0644 by default** (`AtomicFileUtil.cpp:115`'s default; `modeOf(path, 0644)` at `:533`, `:629`) with the scraper's and RetroAchievements' credentials inside; `loadFile` `:549-634`: a pugixml parse (empty = failure) → `.backup` → defaults with nothing written, the record copied back and refreshed only when it differs, the player told once (`main.cpp:1041-1042`); **no `SettingsTests.cpp` exists** -- the XML record path has no unit case; every page close writes both stores (`GuiSettings.cpp:94-95`); `addSwitch`'s `storeInSettings` bool at `GuiSettings.cpp:391-395`, 48 rows `true` |
| `es-core/src/utils/AtomicFileUtil.cpp` / `.h` | 829 / 215 | the fork's atomic writer, new since the base (+829/+215): `createTemporary` `:50-64` (the temp name), `writeText` `:115-183` -- its own temp `path.tmp.<pid>.<n>` with `O_EXCL`, write, `fsync(fd)`, rename, `fsync` of the directory; a missing live file refuses the save (`:506-521`); `chooseConfig` `:291-396` -- Live (usable, not a cut prefix) → a whole `.tmp` the live file is a prefix of (PL-064) → a whole `.backup` (the mtime-bounded cut-of-record case) → a whole `.tmp` → Damaged (read, never recorded) → Missing, the recovery written back under the lock after re-choosing (`:404-432`); `parseKeyValues` (`:453-469`) silently drops a line without `=`, with an empty key **or an empty value**, keeps the last duplicate and strips no BOM; the three-byte `readAllText` trap does not reach it (own `fd` reads); callers: `Settings`, `SystemConf`, `GuiMenu:5066` (the journey record), two `isFlockHeld` users; the writers that do **not** use it, through a void in-place `writeAllText` (27 sites at the pin): `CaptureRotation.cpp:175`, `FileData.cpp:2213`, `KeyboardMapping.cpp:426/:429`, `GuiMenu.cpp:11587`, `GuiKeyboardLayout.cpp:164`, `HttpApi.cpp:258`, `ThreadedCloudSync.cpp:944` (T18's `writeStamp`, fixed on its branch), `Win32ApiSystem.cpp:979`, and `ApiSystem.cpp`'s sixteen sysfs writes; tests `AtomicFileTests.cpp` 24 cases, `AtomicFileWin32Tests.cpp` 2, `SystemConfTests.cpp` 10 against real files |
| `es-app/src/guis/GuiWifi.cpp` / `.h` | 607 / 93 | the Wi-Fi page: the key is typed in a WI-FI KEY popup at `:365`/`:367` (the manual name's at `:295`/`:297`), and **neither `GuiTextEditPopup` nor `GuiTextEditPopupKeyboard` takes a password parameter** (`.h:15-16`, `.h:13-14`): masking is a mode to add to the popup, not a flag to pass; the only masked `wifi.key` row is the relink page's, `GuiMenu.cpp:8297`; connect is `ApiSystem::enableWifi` → `executeScript("timeout 150 wifictl connect " + shellQuote(ssid) + key + country)` → `system()` (`ApiSystem.cpp:635-637`, `:2328`): **the key is argv** of `sh`, `timeout`, `wifictl` and then `nmcli ... password` (`wifictl:177`, `:195`, `:209`; `set_settings ... wifi.key` on `join`, `:460`) for up to 150 s (and `enable` at `:642` with no bound), readable in `/proc`; `shellQuote` (`StringUtil.cpp:426-444`) closes injection; the scan uses `posix_spawnp` argv on a worker (`WifiScanProcess.h:125`, `:535-567`); `maskSecrets` keeps the SSID and redacts the key in the log line (`StringUtil.cpp:764-784`); the NetworkManager keyfile path is `NetworkManager.conf:19`'s, and the directory's and the keyfile's modes are the window's to read; 628/76 by `numstat` against the base |
| `es-app/src/scrapers/ScreenScraper.cpp` / `.h` | 1,092 / 104 | the scraper: the compiled developer pair returned verbatim as the `devid=..&devpassword=..` fragment (`:36-37`, D-WORKFLOW-166's allowed case), the runtime pair from the `Settings` keys `ScreenScraperDevId`/`ScreenScraperDevPass` url-encoded (`:39-43`, #64/#566), the player's `ScreenScraperUser`/`ScreenScraperPass` appended as `&ssid=&sspassword=` only when both are set (`:874-878`, `:890-894`; the API's names, not Wi-Fi's); the rows at `GuiScraperStart.cpp:413-420` and `GuiMenu.cpp:8371/:8374`, the password rows masked, `storeInSettings=true` -- **so the account lives in `es_settings.cfg`, written at mode 0644** (`AtomicFileUtil.cpp:115`'s default; `modeOf(path, 0644)` at `Settings.cpp:533`, `:629`); no `LOG(` prints a credential; `Scraper.cpp:524` logs the URL through `maskSecrets`, whose word list (`StringUtil.cpp:513`: password, pass, token, key, secret, psk, pin) masks `sspassword=` and `devpassword=` and leaves `ssid=<username>` and `devid=`; `getThreadCount` (`:1067-1068`) and the probe (`:1030-1032`) use default options with a blocking `wait()` -- unbounded (#299's shape); the rejected-pair message differs (`:1047-1050`) |

**The shell bridge** (the bridge digest). Four executors, one of them
`system()`; eleven exit reads without `WIFEXITED` and one executor that
discards the exit altogether; `shellQuote` where the fork wrote the call
(`wifictl`, 13 sites) and double quotes where upstream did (16 functions,
two of them live on this image: `7z` over a ROM's path, poppler over a
manual's path -- a path is a player's file name, and a name with a `"`, a
`$` or a backtick reaches `system()`); bare strings from script output and
from a network-fetched bezel list; children and `FILE*`s leaked when a
command prints nothing; most of upstream's command sites calling scripts the distribution does not ship (105 lines naming a `batocera-` script, 36 distinct names; `set-audio`, `keyboardToPads`, `pm-*`); whether the `7zr` the NETPLAY gate wants is on the image is the window's `ls /usr/bin/7z*` (the p7zip recipe builds `all3` and installs `bin/7z*`). **Every stdout line of a legacy-executed script is echoed to
`std::cout`**, which on the image is the journal (`emustation.service:12`,
no `StandardOutput` directive): the proxy's control script, the cloud
scripts and `wifictl` speak there unmasked, and `maskSecrets` is applied to
the command line only, never to the output.

**The network client** (the credentials digest). One process-wide
`curl_multi` with no thread of its own: whichever thread calls `status()`
drives every request under one static mutex, which is the shape of #299's
quarter-hour silence (the hasher's fetch on the interface thread, T20's)
and of every page's wait. `timeout` and `stallTimeout` default to 0; the
cookie jar is a file; redirects follow twice; the server's body for 400 to
503 is logged verbatim; **the peer is never verified (#1154, filed from
T20's research, this file's lines `:192` and `:200`)**, and the credentials
the pages put on their queries -- the RetroAchievements password and web
API key (T20's), the scraper's developer pair and the player's account
(this slice's) -- travel through it.

**The two stores and the OS side** (the state digest). `SystemConf` writes
`system.cfg` through the fork's `AtomicFile::writeText` under a `PidLock`
and records the last-good copy only after re-reading the disk; `Settings`
writes `es_settings.cfg` through the same writer **with no lock and no
mutex on its maps**, at mode 0644, with the scraper's and RetroAchievements'
credentials inside, and has **no unit test**. The shell writers of
`system.cfg` at `8ebaf8daad` (`001-functions:429-607`) rename a temp under
the same lock path with **no `fsync`**; `chksysconfig` renames with **no
lock**; `post-update` edits in place with `sed -i` (T1's PL-014);
**`set_setting` seeds a missing `system.cfg` from `/usr/config` before the
lock and without consulting the record**, after which EmulationStation's
next save makes those defaults the record -- D-CLOUD-078's three steps in
the wrong order; a new file is 0644 from EmulationStation and 0600 from the
shell, the shipped seed is 0644, and a replaced file keeps its bits (T1's
PL-023), so nothing on an upgraded device ever tightens a 0644 `system.cfg`
that holds a Wi-Fi key. The reader's ladder (`chooseConfig`) is the fork's
and tested; `parseKeyValues` drops a line with an empty value silently.
`tools/vm-upgrade-rehearsal` seeds neither `.backup` record, so an update
has never been proved to keep them.

**The credentials these files carry:** the Wi-Fi key (typed at `GuiWifi.cpp:365-367` in a popup whose class has no masking mode; argv of four processes for up to 150 s, and of `enable` at `:642` with no bound; masked in
the log line; the NetworkManager keyfile's mode not yet read; `wifi.key` in
`system.cfg` at whatever mode the file has), the scraper's developer pair
(compiled in under D-WORKFLOW-166, or the runtime rows) and the player's
account (`es_settings.cfg`, 0644; `ssid=<username>` unmasked at LogDebug),
and -- through `HttpReq` -- every query T20's pages send. The dropping
filter `grep -v -i -E 'key|pass|token|user|psk'` lets `IGDBSecret` and
`ScreenScraperDevId` through; `redact_credentials` guards `exec.log`
(blindspot 43), which none of these files writes.

**The neighbours, and whose they are:** `setsettings.sh`, `get_setting`,
`set_setting`, `chksysconfig`, `post-update` and `wifictl` are **T1's**
(#648, accepted; its PL-004, PL-014, PL-023 cited, not re-found);
`backuptool`'s SECRETLIST and RATOKENSETTINGS on these keys are **T17's**;
the proxy's control script spoken to through `executeScriptLegacy` is
**T19's**; the RetroAchievements pages and the hasher that call `HttpReq`
and `ask()` are **T20's** (#667: `ask()`'s missing `WIFEXITED` is this
slice's line, T20's caller); `GuiMenu.cpp`'s rows (the timezone written at
`:1890`, the relink rows at `:8297`, `:8371`, `:8374`, the journey record at
`:5066`) are **T26's**; `GuiScraperStart.cpp:413-420` is T32's; the
services that read `system.cfg` at boot are **T22's**; the empty-path forward (`SystemConf` to `Settings` when `mSystemConfFile` is empty, `:288` and its siblings; `Settings.cpp:420`'s default under `#if WIN32`) is Q4's to read in `Paths`.

**Already found; do not re-find** (cited at its lines): T1's PL-004
(`add_setting`'s backgrounded first test), PL-014 (`post-update`'s `sed
-i`), PL-023 (the replaced file's mode) and its siblings on the settings
scripts (`docs/audits/2026_10_23-epic-m6-os-launch-control-state/` on
`feature/m6-os-launch-control-state-648`); T18's F-06 (`writeStamp`'s
unchecked write, fixed onto `AtomicFile::writeText` on its branch) and
#1143 (one reader for both surfaces); T20's research: **#1154**, `ask()`'s
`WEXITSTATUS` without `WIFEXITED` (`:2278-2291`), the echo at `:2284`,
`maskSecrets` at `:2235`, `:2265`, `:2297`, and `Settings.cpp:420`'s `.hardcore` default, **which sits inside `#if WIN32` (`:417-433`) and serves `SystemConf`'s empty-path forward** -- whether that path can be empty on ROCKNIX is Q4's to read in `Paths` (T20's lane is told at dispatch); T17's SECRETLIST; T15's `system.cfg` cases (blindspot 34);
T14's `settings-modes-test` (#421); #102 (the truncated stores of
2026-09-09, closed as delivered 2026-09-17); #320 (the record re-read under
the lock). T2's (#649) own T21 lead at its `04-analysis.md:142` (the seam-leads line): the ROM paths in double quotes at `ApiSystem.cpp:1527`, `:1659`, `:2591-2593`, `:3502` and `SystemConf` read on worker threads (its PC-2) -- this slice's Q1 and Q4, cited; T12's PL-13 (`device-act` logs credentials); T17's punch list carries **no** SECRETLIST or RATOKENSETTINGS line, so `backuptool`'s treatment of these keys is read here as a sink, not re-audited. The four `maskSecrets` sites are `:2235`, `:2265`, `:2297` and `:2325` (T20's brief named three); the echo is observed at `:2266` and `:2284` is read again here.

## 3. Read first

In this order, each read in this session, and `01-research-notes.md` says
which were read (`working-principles.md` § Pre-flight):

1. **The rules.** `es-native-ui.md` § Code conventions (`addSwitch`'s bool is
   `storeInSettings`: `false` → `system.cfg`, the only store the launch
   scripts read), § Core patterns (`addInputTextConfigRow` for `wifi.key`
   and `ScreenScraperPass`; `runSystemCommand`; `isScriptingSupported`; no
   raw `popen` in UI code), the bullet *A file another process writes is read uncached* in § Core patterns; `es-code-traps.md` § A pooled connection with the link gone
   (#299, `stallTimeout`, #300) and § Three things a font is not (the
   `exists` cache); `es-player-text.md` § Outcome words (the player's one
   sentence when a store is recovered); `engineering-practices.md`'s bullet *A read is free, and still goes through the filter* under § Nothing runs on a person's device without their yes (D-QA-021, the two forms), § Fail gracefully and **its paragraph *The last known good state is a record, kept on purpose* (D-CLOUD-078: know you succeeded, replace only after, remove the superseded copy once; #102 the two stores)**, § Guards must fail closed
   (`rc=$?` on its own line; a fixture for a secret scanner built at run
   time, #307), § Verify the artifact; `upgrade-and-install.md` whole (the
   `Already written:` line; read both, write the new one; the shell's
   settings keys row); `device-builds.md` § Build credentials
   (`SCREENSCRAPER_DEV_LOGIN`, the #64 runtime pair, #566 and
   D-WORKFLOW-166's shared identity hiding the developer rows, #586 later,
   D-INFRA-006/007); `generic-x64-vm-testing.md` (`exec.log` carries
   `cheevos_password` from `setsettings.sh`, blindspot 43; the interface
   loads `system.cfg` once); `rclone-cloud-sync.md` (the cloud scripts are
   run through `executeScriptLegacy`, not `runSystemCommand`);
   `handheld-evidence.md`; `bugs-are-agent-first.md` rule 6;
   `adversarial-council.md`; `issue-tracking.md`; `decision-register.md` §
   A reversal sweeps its old words (D-UI-071's stale comments name
   `wifi.ssid`).
2. **The register.** Forty-one rows touch the scope; the binding ones:
   D-CLOUD-078/079 (the last-good record; 079's sentence on the writers
   describes the code before #320), D-CLOUD-145, D-CLOUD-181 (integrity
   inputs and the credential filter are separate), D-QA-003 to 006,
   D-QA-014, **D-QA-021** (the read filter), D-INFRA-006/007/010/011/012
   (credentials in builds; the historical binary guard), D-UI-048, D-UI-063,
   D-UI-071, D-UI-118, D-RA-025/036, **D-SYS-001 to 013** (the settings
   stores' contract -- read each; the digest's lookup was by the wrong
   column and the lane reads the rows themselves: `/usr/bin/grep -n
   'D-SYS-0' docs/decision-register.md | cut -c1-160`), **D-NET-001 to 016 less 011** (no row carries that ID; the Wi-Fi page and `wifictl`), D-LAUNCH-004, D-WORKFLOW-017/021/064/071,
   D-WORKFLOW-166, D-WORKFLOW-192. Open and this slice's to leave open:
   D-SYS-006, D-SYS-014, D-NET-012, D-NET-013, D-WORKFLOW-080 (`ApiSystem.cpp`
   carries every PR bucket's rows; the 200-file PR closed).
3. **The menu map** (`docs/es-menu-map.md`), the rows these files draw:
   `:139` (the SCRAPER row), `:442-461` and `:473-489` (the Wi-Fi and relink pages), `:571`, `:642-644` (the scraper's account rows), `:701`,
   `:911-935` -- D-UI-039: a fix that moves or renames a row updates the map
   in the same change.
4. **The blindspots**: 3 (`GetShOutput` → `executeEnumerationScript`), 34
   (busybox `tr` against `system.cfg`; guard `tools/last-good-scripts-test`),
   42 (a device's state is read from the device; no guard path named --
   `device-act` by the rule), 43 (#176's `exec.log` password; guard case r),
   50 and 55 (`exec.log`'s log; `time-to-play`'s surface check), 64 (#299,
   no tool), 67 (the credential fixture; the pre-commit hook).
5. **The tests at the pin**, 80 `TEST_CASE`s in the eight files that touch this slice (the unit directory holds 19 files and 221 cases; the run counts the eight): `SystemConfTests` 10 (names `SystemConf::get` 18 times,
   `saveSystemConf` 13, `set` 10, `loadSystemConf` 6, `recordLastGood` 1,
   the lock statics; `Settings::setString`/`setBool` as fixture),
   `AtomicFileTests` 24 (lines naming `chooseConfig` 22, `saveUnderLock` 10, `readText` 9, `writeText` 5, `isFlockHeld` 4, `modeOf` 3, `copy` 1),
   `AtomicFileWin32Tests` 2, `MaskSecretsTests` 12 (`StringUtil.cpp:715`,
   **not one of the fourteen**, this slice's subject), `WifiTextTests` 19
   (`WifiText.cpp`, not one of the fourteen; `GuiWifi.cpp` uses 16 `WifiText::` names), `CommandLineTests` 2, `LaunchCommandTests` 8,
   `LogPolicyTests` 3. **Zero tests** name `ApiSystem.cpp`'s 173 member
   functions (the Wi-Fi command builders, `executeScript*`,
   `getRootPassword`), `HttpReq.cpp`'s 13 (`urlEncode`, `isUrl`, the option
   mapping `:183-316`), `ScreenScraper.cpp`'s (`screenScraperDevLogin :34`,
   `getGameSearchUrl :857`, `getUserInfoUrl`, `ensureUrl`), `Settings.cpp`'s
   (`saveFile :469`, `loadFile`, `setDefaults :131`) or `GuiWifi.cpp`'s 18;
   `SystemConf`'s `parseSystemConf`, `applyChanges`, `getBool`, `setBool` and `AtomicFile`'s `isUsableKeyValues`, `loadUnderLock` have no direct case; `SystemConfTests.cpp` names `Settings::saveFile` once as a fixture, `OfflineAchievementsTextTests.cpp` names `HttpReq` once and `MaskSecretsTests.cpp` names `ScreenScraper` twice, and none exercises them.
6. **The walks and the harness** (`tools/vm-walks/`, 22 `.steps` walks): **no Wi-Fi or scraper walk, suite row or `claims.txt` baseline exists**; only
   `tick-settings` and `ui-settings-toggle` touch `es_settings.cfg`. The
   frames that exist live in qa-logs: `2026-10-15-wifi-remaining-result`
   (24 png, `frame-review.json`), `wifi-normal-exit-result` (4),
   `2026-10-13-library-wifi-baseline` (12), `2026-10-14-screenscraper-ui-runtime`
   (35 png; its map says 20 primary); six named directories hold 0 png (`2026-10-13-wifi-backend-source`, `2026-10-13-wifi-picker-source`, `2026-10-14-screenscraper-provisioning`, `2026-10-14-screenscraper-rejection-runtime`, `2026-10-14-wifi-remaining-lifecycle`, `2026-10-15-wifi-log-observation`).
   `tools/cloud-input-test` (9 `def test_` against `wifictl` and the phone
   page's JS; fixture `wifi.key → OLD_FIXTURE_KEY`; not EmulationStation),
   `tools/settings-modes-test` (24 + 5 checks on the shell writers of
   `system.cfg` and `.backup`; not `SystemConf`),
   `tools/last-good-scripts-test`'s `system.cfg` cases (`:429-492`,
   `:527-548` which strips `wifi.key=SECRET`, `:611-647`, `:1253-1307`),
   `tools/vm-upgrade-rehearsal` (seeds no Wi-Fi key, scraper credential or
   `es_settings.cfg`), `tools/vm-qa`'s SUITES line (`:63`).
7. **The French** at the pin by 40-character prefix against `fr.po` (6,964
   lines, 2,207 msgids): `GuiWifi.cpp` 44 calls, 28 unique literals, 28
   found with a non-empty msgstr; `ScreenScraper.cpp` 14 / 13 / 13;
   `ApiSystem.cpp` 1 / 1 / 1 -- a single-line match, no `_U(`, the
   translations' content unread; a changed string is `es-untranslated
   --upstream bccd715707`'s.
8. **The audits**: T2's `04-analysis.md:142` (above); T1's punch list
   (PL-004, PL-014, PL-023 and the `:25-30` netplay host item); T12's
   PL-13; T14's PL-13 and T15's `:27` and PL-13 (the busybox contract);
   T17's (PL-08 the staged `.rclone.conf-*`; `mv` unchecked); T18's PL-01
   (`writeAllText` → `AtomicFile::writeText`, `f63ad4de4`), PL-11/12/16/23
   → #1143; T20's research and its stage-D ruling on #1154 (T20 or T21:
   **this slice's**, by its lines).
9. **The issues**, dated: #102 (the two stores truncated, 2026-09-09; closed as delivered 2026-09-17 by that day's work log -- the line the digest cited is another entry), #320 (the
   record re-read under the lock), #421 (modes; `2026_10_04:565-631`,
   friction-log `:153`), #535/#536 (`cloud-input-test`; the rules index
   credits it to both while the 2026_10_11 work log names #536 as the
   Dropbox pointer report -- read the issue, not the index), #64 (the
   runtime scraper pair), #566 (the shared developer identity), #586 (its
   replacement, later), #299/#300 (the pooled connection; the hasher's
   fetch), #1154, #1143, #176 (`exec.log`'s password), #1137, #1138,
   #1141.

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of four families: **a command built from
a player's string** (a path, a name, a key), **a credential's sink** (argv,
a file's mode, a log, an unverified peer), **a state write that can lose
the record** (no lock, no `fsync`, in place, the seed before the record),
**a check whose failure reads as success** (a discarded exit, a signal read
as 0, a dropped line). The leads below are the digests' by shape; each is
read at its lines before it is called anything.

- **Q1 The commands.** Every command-running call with its quoting: the
  two live double-quoted paths (`7z`, poppler) against a file name carrying
  a shell metacharacter -- the constructed positive is a ROM named with a
  `$(...)` in a scratch library on the guest, never on a device; the bare
  strings from script output and the bezel list; the leaked children; the
  absent scripts' sites (a table: which gate hides each, which page could
  still reach one; recorded, since D-UI-079 keeps upstream's surfaces as
  upstream has them until a lane opens them); the blocking calls on the
  interface thread and their bounds (none for the timezone, audio,
  storage, service, hotkey and LED setters; `getBiosInformations` at launch when CHECK BIOS AT LAUNCH is on, default off -- the time-to-play line).
- **Q2 The client.** The one `curl_multi` driven by whichever thread
  calls `status()`: which callers hold the interface thread and for how
  long with `timeout` 0; the server's body logged verbatim for 400 to 503
  (peer-controlled text into `es_log.txt`); the cookie jar's file and mode;
  the redirect policy against a credential on the first query; #1154 cited
  -- and the fix's design question for the stage-D pause: verify the peer
  by default with the image's CA bundle and keep the 2021 exception as an
  explicit option the scrapers' media downloads set (the bundle's presence
  on the image and the scrapers' behaviour with verification on are the
  window's to read).
- **Q3 The credentials' paths.** The Wi-Fi key on argv of four processes for up to 150 s (and of `enable` at `:642` with no bound) and in a popup whose class has no masking mode at all (`GuiTextEditPopup` `.h:15-16`, `GuiTextEditPopupKeyboard` `.h:13-14`: a fix adds a mode, not a flag); `wifi.key` at rest
  in `system.cfg` at the file's mode; the NetworkManager keyfile's mode
  (read on the guest); `es_settings.cfg` at 0644 with the scraper's
  account and the RetroAchievements key; the developer pair compiled in
  (D-WORKFLOW-166's allowed case: which identity, and that no personal
  value is embedded -- read by name, never printed) against the runtime
  rows; the filter's two blind words; the LogDebug lines with the username
  and `devid`; `getRootPassword`'s literal default and where it is shown.
- **Q4 The writers.** The lock asymmetry (`SystemConf` locked, `Settings`
  not, the maps unguarded under a worker's save); the shell writers with no
  `fsync`; `chksysconfig` with no lock; `post-update`'s `sed -i`; **the
  seed before the record** (`set_setting:540-543`); the modes (0644 from
  EmulationStation, 0600 from the shell, the seed 0644, a replaced file's
  bits kept: what an upgraded device holds -- `upgrade-and-install.md`'s
  question, with `Already written:` the answer); the `.backup.tmp` sweep
  against `chksysconfig backup`'s temp name; the in-place `writeAllText`
  state writers outside `AtomicFile`.
- **Q5 The readers.** `parseKeyValues`' silent drops (no `=`, an empty
  key, **an empty value**, a BOM kept, the last duplicate winning) against
  what the shell writers can produce; the recovery ladder's cases and
  their tests (`SystemConfTests` 10 against real files; `AtomicFileTests`
  24); `Settings::loadFile`'s ladder with **no test at all**; the player
  told once at `main.cpp:1041-1042` (the words, `es-player-text.md`).
- **Q6 What a failure reads as.** The enumeration executor's discarded exit and `getBiosInformations` at launch with CHECK BIOS AT LAUNCH on; the `#if WIN32` shims at `:45-46` that make the Windows build read every status as an exit code (not built here; recorded); the eleven
  `WEXITSTATUS` reads without `WIFEXITED` and which pages act on them
  (T20's `ask()` among them); the last line as the result where a script
  prints two; `cloud_oauth close`'s ignored result (`:593`); the
  `LockBusy` path that keeps a change in memory and what the player sees.
- **Q7 The dead paths.** The 105 `batocera-` lines (36 names), `set-audio`, `keyboardToPads`, `rocknix-sync`, `rocknix-resolution`, `pm-*`, and the `7zr` question (the recipe's `all3` and `bin/7z*`; the image's listing in the window): a table of each site, its gate, whether a page on this
  image can reach it, and what it would do if reached -- recorded as
  written (D-WORKFLOW-209's shape: a table removes nothing; the removal is
  the renovation's later pass, #1143's family).
- **Q8 The harness.** What `tools/settings-modes-test` (#421),
  `tools/last-good-scripts-test`'s sections a and c, `AtomicFileTests`'
  24 cases, `tools/vm-upgrade-rehearsal` (no `--help`; seeds no `.backup`),
  `tools/cloud-input-test` (#535/#536) and `MaskSecretsTests` prove and do
  not; the kill-the-writer test D-CLOUD-078 names (every step, for both
  stores, on the host through the unit tests' fakes where the writer is
  pure and on the guest where it is not); for each lead this slice
  confirms, the constructed positive that fails on the pin's bytes.

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #668.** Every read, count and table runs on the host
   at the pin's bytes. **The host has no toolchain** (#1137): the state
   tests (`AtomicFileTests` 24, `AtomicFileWin32Tests` 2, `SystemConfTests`
   10, `MaskSecretsTests`, `WifiTextTests`, `CommandLineTests`,
   `LaunchCommandTests`, `LogPolicyTests` -- T18's files, this slice's
   subjects) are built with the host's `g++` by the command generated from
   `es-app/tests/unit/CMakeLists.txt` (T18's `tools/t18-build-tests.sh`
   copied into this audit folder's `tools/`; rapidjson by a named copy with
   provenance, or the dependent cases named as not run); `tools/es-syntax-check`
   records its exit-2 line with `ES_BUILD_ROOT` set, never empty;
   `ApiSystem.cpp`, `GuiWifi.cpp` and `ScreenScraper.cpp` include SDL or
   curl and are `CANNOT` for the host's `g++ -fsyntax-only`, their compile
   proof the integration build's; `Settings.cpp`, `SystemConf.cpp` and
   `AtomicFileUtil.cpp` are tried the same way and recorded as they fall.
   `tools/settings-modes-test` and `tools/last-good-scripts-test` run on the
   host with the retained donor's busybox
   (`/workspace/artifacts/m6-donor/1a0266484423/image/system`), their
   `system.cfg` cases named; **the kill-the-writer test** (D-CLOUD-078:
   the writer killed at every step, the previous state what remains) runs
   on the host against `AtomicFile::writeText` through a fixture in the
   unit tests' shape, and against the shell writers under the donor's
   busybox in a bubblewrap sandbox started with `--clearenv` (the real
   `001-functions`, no path rewritten); **the seed-before-the-record
   case** (`set_setting:540-543`) the same way: a `.backup` present, the
   live file absent, `set_setting` run, the result compared with the
   record. A new unit case is the proof of choice for every pure lead (the
   parser's drops, the exit reads, the mask's `--key` gap).
2. **The guest window** -- one, asked for on #668 at stage B's end with its
   plan and bound (45 minutes proposed), granted explicitly in the shared
   log's queue, one boot of the M6 copy of the image
   (`/workspace/artifacts/m6-t2-20261023/`, `069fc2704421`) **started at
   640x480** (`generic-x64-vm run --res`, #1141), the post contract
   `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line
   with the census, the stop by pidfile at bound plus grace, the disk
   retired after with path, size and sha (D-INFRA-022): the identity
   (`BUILD_ID`; the image's EmulationStation is M7's build, as T19 found of
   its scripts -- the installed `emulationstation` hashed against nothing
   and every verdict labelled the image's); **the modes as written** --
   `es_settings.cfg`, `system.cfg`, their `.backup`s, the cookie jar, the
   NetworkManager keyfile after a Wi-Fi join through the page's own
   command (`tools/cloud-input-test`'s open and protected selections,
   #535/#536, drive the page with its fake networks; the lane reads the
   tool first and records what it drives); **the recovery ladder on the
   image** -- `system.cfg` truncated by hand with a good `.backup`, then
   EmulationStation started: the record chosen and written back, the
   player told once (a frame at 640x480); `es_settings.cfg` the same, which
   has no unit test; **the key on argv** -- during the join, `/proc/<pid>/cmdline`
   of `timeout`, `wifictl` and `nmcli` read for the presence of the key's
   *name*, never its value (a count of processes whose cmdline carries
   the QA network's key, the value masked); **the #1154 positive** for the
   scraper -- `screenscraper.fr` pointed by the guest's hosts file at a
   host-run TLS endpoint with a self-signed certificate, a scrape from the
   page reaching it on the pin's binary (the endpoint's log; no value
   printed); **one live sign-in with the QA ScreenScraper account**
   (`SS_QA_*` in `~/.ROCKNIX/qa-accounts`, carried by `tools/qa-accounts`,
   never printed; D-QA-016; never the owner's, D-QA-015) against the real
   server, last, if the bound allows, recorded `CANNOT in this window`
   otherwise; and **the `7z` positive** -- a ROM named with `$(...)` in a
   scratch library, the page's 7z action run on it, and what the shell did
   (a marker file the command substitution would have written). Every
   proof's frames are `pin-binary` evidence; a fix's frame is
   `fix-walk-pending-image`.
3. **What T26 and the OS slices inherit** is written, not tested here: the command builders' quoting rule (`shellQuote` or an argv executor, never double quotes), the stores' keys and which store each row should use, the writers' contract (`AtomicFile` for state, the lock, the record after the re-read), and the `7zr` question's answer from the window.
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   ES branch, proven twice (`fix-unit-test` or `fix-walk-pending-image`),
   the unit tests built before every commit; a change to the shell writers
   is **T1's file** and lands only by the coordinator's ruling.

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its
reason). From the distribution worktree after the membership block; `W` the
ES worktree, `PIN` the pin, `D` the distribution; counts by `/usr/bin/grep`
(#1138); `rc=$?` on its own line, never after a pipe:

```bash
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-state-and-bridge-668; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep; C=8ebaf8daad
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t21/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
# the ES worktree at the pin, clean; the merge base; the delta (expect the pin; 0; bccd715707; 14 files changed, AtomicFileUtil.* new)
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l; git -C "$W" merge-base bccd715707 HEAD | cut -c1-10; git -C "$W" diff --stat bccd715707 "$PIN" -- $(cat .qa-scratch/t21/paths.txt) | tail -n 1
# the executors and the exit reads (expect popen/pclose in 2233-2252, 2263-2292, 2295-2320; system( at 2328; 20 lines, 15 of them WEXITSTATUS with the #define shims at 45-46 among them, of which 11 are reads without WIFEXITED on the same line: 234 270 293 329 354 397 415 440 469 2291 2319; WIFEXITED at 528 585 607)
git -C "$W" grep -n -E 'WEXITSTATUS|WIFEXITED' "$PIN" -- es-app/src/ApiSystem.cpp | sed "s/^$PIN://" | cut -c1-110; git -C "$W" grep -n -E '\bsystem\(|popen\(|pclose\(' "$PIN" -- es-app/src/ApiSystem.cpp | sed "s/^$PIN://" | cut -c1-100
# the quoting (expect shellQuote at 13 sites, all wifictl; getSevenZipCommand() over a double-quoted path at 1527 1578 1659 and the poppler calls at 2509 2593; the comment at 631-634)
git -C "$W" grep -c 'shellQuote' "$PIN" -- es-app/src/ApiSystem.cpp | sed "s/^$PIN://"; git -C "$W" grep -n -E 'shellQuote|getSevenZipCommand|7z|pdftoppm|pdfinfo' "$PIN" -- es-app/src/ApiSystem.cpp | sed "s/^$PIN://" | cut -c1-110; git -C "$W" show "$PIN:es-app/src/ApiSystem.cpp" | sed -n '631,634p'
# the absent scripts (expect 105 lines naming a batocera- script and 36 distinct names; under projects/ROCKNIX/packages at 8ebaf8daad wifictl, rocknix-bluetooth, rocknix-config and cloud_oauth each 1, set-audio, keyboardToPads, rocknix-sync and rocknix-resolution each 0; the p7zip recipe's all3 and bin/7z* lines -- whether 7zr is on the image is the window's ls /usr/bin/7z*)
git -C "$W" grep -c -E 'batocera-[a-z-]+' "$PIN" -- es-app/src/ApiSystem.cpp | sed "s/^$PIN://"; git -C "$W" grep -o -h -E 'batocera-[a-z-]+' "$PIN" -- es-app/src/ApiSystem.cpp | sort -u | wc -l; for s in wifictl rocknix-bluetooth rocknix-config cloud_oauth set-audio keyboardToPads rocknix-sync rocknix-resolution; do printf '%s: ' "$s"; git ls-tree -r --name-only "$C" -- projects/ROCKNIX/packages | $G -c -E "(^|/)$s$"; done; git show "$C:projects/ROCKNIX/packages/compress/p7zip/package.mk" | $G -n -E 'make_target|all3|7z' | cut -c1-100
# the mask (expect maskSecrets at ApiSystem.cpp 2235 2265 2297; its rules at StringUtil.cpp 715-803 with the name list at 513 and the wifictl rule at 764-784; --key absent from the flag rule)
git -C "$W" grep -n 'maskSecrets' "$PIN" -- es-app/src/ApiSystem.cpp es-core/src/utils/StringUtil.cpp | sed "s/^$PIN://" | cut -c1-100; git -C "$W" show "$PIN:es-core/src/utils/StringUtil.cpp" | sed -n '513p;764,784p' | $G -n -E 'password|wifictl|--' | cut -c1-110
# the client's options (expect curl_multi at HttpReq.cpp:21, the mutex 19/397; setopt FOLLOWLOCATION 183, VERIFYPEER 192, VERIFYHOST 200, TIMEOUT_MS 206, LOW_SPEED 211-213, MAXREDIRS 222, REDIR_PROTOCOLS 240; the body logged 443-459; onError 559-563; the defaults HttpReq.h:45-88, the user agent :30)
git -C "$W" grep -n -E 'curl_multi_init|curl_easy_setopt' "$PIN" -- es-core/src/HttpReq.cpp | sed "s/^$PIN://" | cut -c1-110; git -C "$W" grep -n -E 'timeout|stallTimeout|connectTimeout' "$PIN" -- es-core/src/HttpReq.h | sed "s/^$PIN://" | cut -c1-100
# the scraper's credentials (expect the compiled pair at 36-37, the runtime pair 39-43, the account 874-878 and 890-894; the rows at GuiScraperStart.cpp:413-420 and GuiMenu.cpp:8371,8374; the LogDebug mask at Scraper.cpp:524) -- names and lines only
git -C "$W" grep -n -E 'devid|devpassword|ssid=|sspassword|ScreenScraperDevId|ScreenScraperDevPass|ScreenScraperUser|ScreenScraperPass|maskSecrets' "$PIN" -- es-app/src/scrapers/ScreenScraper.cpp es-app/src/scrapers/Scraper.cpp es-app/src/guis/GuiScraperStart.cpp es-app/src/guis/GuiMenu.cpp | sed "s/^$PIN://" | cut -d: -f1,2 | sort | uniq -c | sort -k2 | head -n 30
# the Wi-Fi key's path (expect the popups at GuiWifi.cpp 295/297 (the name) and 365/367 (the key), neither class with a password parameter; the wifictl calls without a timeout at ApiSystem.cpp 642 767 771 775 among the lines printed; the shipped wifictl 557 lines, its nmcli/password/set_settings hits including 177 195 209 460; the relink row GuiMenu.cpp:8297)
git -C "$W" grep -n 'GuiTextEditPopup' "$PIN" -- es-app/src/guis/GuiWifi.cpp | sed "s/^$PIN://" | cut -c1-110; git -C "$W" grep -n 'wifictl' "$PIN" -- es-app/src/ApiSystem.cpp | sed "s/^$PIN://" | $G -v 'timeout' | cut -c1-110; WF=projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl; git show "$C:$WF" | wc -l; git show "$C:$WF" | $G -n -E 'nmcli|password|set_settings' | cut -d: -f1 | tr '\n' ' '; echo
# the writers (expect 41 AtomicFile:: lines and 27 writeAllText( lines: Settings.cpp 524 and 533 and SystemConf.cpp 304 and 86-112 among the first; the modes modeOf(path, 0644) at Settings.cpp 533 and 629 with AtomicFileUtil.cpp:115's default, SystemConf.cpp:107; among the second CaptureRotation.cpp:175 FileData.cpp:2213 KeyboardMapping.cpp:426,429 GuiMenu.cpp:11587 GuiKeyboardLayout.cpp:164 HttpApi.cpp:258 ThreadedCloudSync.cpp:944 and ApiSystem.cpp's sixteen sysfs writes; the shell's at 001-functions 429-607 with no fsync; chksysconfig with no lock; post-update's sed -i at 101, 160, 202; set_setting's seed at 540-543 before the lock at 555)
git -C "$W" grep -n -E 'AtomicFile::|writeAllText\(' "$PIN" -- es-core/src/Settings.cpp es-core/src/SystemConf.cpp es-app/src es-core/src | sed "s/^$PIN://" | cut -c1-100
FN=$(git ls-tree -r --name-only "$C" | $G -E '(^|/)001-functions$' | head -n 1); echo "001-functions: $FN"; git show "$C:$FN" | $G -n -E 'fsync|flock|wait_lock|mv -f|/usr/config' | cut -c1-100 | head -n 20; git show "$C:$FN" | sed -n '540,543p' | cut -c1-110
git show "$C:projects/ROCKNIX/packages/rocknix/sources/post-update" | $G -n -E 'sed -i' | cut -c1-100; CS=$(git ls-tree -r --name-only "$C" -- projects/ROCKNIX/packages/rocknix | $G -E '(^|/)chksysconfig$' | head -n 1); echo "chksysconfig: $CS"; git show "$C:$CS" | $G -c -E 'flock|wait_lock'; rc=$?; echo "chksysconfig lock lines: rc=$rc (1 = none)"
# the readers (expect parseKeyValues in AtomicFileUtil.cpp dropping an empty value; chooseConfig 291-396; Settings::loadFile 549-634; the player told at main.cpp:1041-1042)
git -C "$W" grep -n -E 'parseKeyValues|chooseConfig|loadFile|wasRecovered' "$PIN" -- es-core/src/utils/AtomicFileUtil.cpp es-core/src/Settings.cpp es-core/src/SystemConf.cpp es-app/src/main.cpp | sed "s/^$PIN://" | cut -c1-100
# the tests at the pin (expect AtomicFileTests 24, AtomicFileWin32Tests 2, SystemConfTests 10, MaskSecretsTests 12, WifiTextTests 19, CommandLineTests 2, LaunchCommandTests 8, LogPolicyTests 3: 80; no SettingsTests.cpp: 0)
for f in AtomicFileTests AtomicFileWin32Tests SystemConfTests MaskSecretsTests WifiTextTests CommandLineTests LaunchCommandTests LogPolicyTests; do printf '%s: ' "$f"; git -C "$W" show "$PIN:es-app/tests/unit/$f.cpp" 2>/dev/null | $G -c 'TEST_CASE' || echo absent; done; git -C "$W" ls-tree --name-only "$PIN" -- es-app/tests/unit/SettingsTests.cpp | wc -l
echo "the lane's tools/t21-build-tests.sh (from T18's) generates the g++ lines, names every -I, and records each binary's summary line"
# the host tools (expect settings-modes-test and last-good-scripts-test --help rc 0; vm-upgrade-rehearsal has no --help; cloud-input-test --help rc 0)
for t in settings-modes-test last-good-scripts-test cloud-input-test; do out=$(tools/$t --help 2>&1); rc=$?; echo "$t --help rc=$rc"; done; out=$(tools/vm-upgrade-rehearsal --help 2>&1); rc=$?; echo "vm-upgrade-rehearsal --help rc=$rc ($(printf '%s' "$out" | head -n 1 | cut -c1-60))"
# the syntax check (expect exit 2 on this host with ES_BUILD_ROOT set; rc on its own line) and the host g++ on three files (expect the first error line: curl/curl.h or SDL for ApiSystem.cpp; the stores as they fall)
out=$(ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" es-core/src/utils/AtomicFileUtil.cpp 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 1; echo "es-syntax-check rc=$rc"
for f in es-core/src/utils/AtomicFileUtil.cpp es-core/src/SystemConf.cpp es-app/src/ApiSystem.cpp; do out=$(g++ -std=c++17 -fsyntax-only -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$f" 2>&1); rc=$?; printf '%s: %s rc=%s\n' "$f" "$(printf '%s\n' "$out" | $G -m1 -E 'fatal error|error:' | cut -c1-90)" "$rc"; done
# the removal check from the dispatch tip -- <dispatch tip> is the lane tip the dispatch comment on #668 names (expect empty) and the ES diff against the pin (expect empty before stage E)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1
```

## 6. Outputs

As T20's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-es-state-and-bridge/`:
`00` to `05`, `second-opinions/`, `guest-cycle/`, the lint before D, the audit
issue (`Audit: M6 T21 EmulationStation's state primitives and its bridge to
the OS -- N findings (...)`, a sub-issue of #668), the bugs, and the retro at
`docs/retros/<date>-m6-es-state-and-bridge.md` (**what the slice did to the
two time-to-play numbers**: `getBiosInformations` runs at launch when `CheckBiosesAtLaunch` is on (default false, `Settings.cpp:207`) through `executeEnumerationScript` (`ViewController:507-509`), and `SystemConf::saveSystemConf` runs when a page closes before a launch, both unbounded, so the answer names those two with what they cost on the guest (`tools/time-to-play --vm` with the backend up) and cites `docs/vm-qa-log.md` and T18's window's three numbers; never "nothing" by default; **what T26 and
the OS slices inherit**: the command builders' quoting, the stores' keys,
the writers' contract). **`02` carries § Coverage (14), § The commands (one
row per command-running call: the literal, the player-supplied arguments,
the quoting, how the output and exit are read), § The credentials' paths
(one row per credential kind per sink), § The writers (one generated row per
write of `es_settings.cfg`, `system.cfg`, their copies and every
`AtomicFile`/`writeAllText` call under `es-app/src` and `es-core/src`:
temp-and-rename or in place, `fsync`, the mode, the positive check, the
failure's remainder), § The readers (each parse's edge cases), § The client
(every `curl_easy_setopt` with its value and every `HttpReqOptions` field),
§ The runs, § The guest cycle, § Positives, and every proof with `proved:`.**
The stage-D pause as T20's: the punch list posted on #668, the lane waits for
the coordinator's dispositions and any stream brief.

## 7. Acceptance

The checklist on #668 becomes this section at dispatch, written there by
the coordinator in place of P1's generated ones. Every checkbox names the
artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-state-and-bridge/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-state-and-bridge/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`).
- [ ] `second-opinions/review-plan.json` records `depth: extended` and two reviewers (`gpt`, `openai/gpt-6-astra`, `max`; `gemini-argon`, `google/gemini-4-argon`, `high`); each seat's probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the three-way scan with every hit dispositioned by name; the running log shows exactly four keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #1154, #1143, #585, #648, #673, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail.
- [ ] `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in the checklist's header carry the lane's commits; the ES read is on the pin's bytes for the 14 (`git -C <W> diff --stat 16dbac5211 <reviewed-at-es> -- $(cat .qa-scratch/t21/paths.txt)` empty before stage E) and nothing under the distribution's `packages/`, `projects/` or `tools/` changed at any stage.
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (14 paths, 9,249 lines; fork-own 14; 12 in the merge base -- or the deltas beside them) and the per-file line table at the pin.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `14`.
- [ ] `02-forward-audit.md` § The commands has one row per command-running call in `ApiSystem.cpp` (the literal, the player-supplied arguments and their quoting, how the output and the exit are read, the thread, the script's presence at `8ebaf8daad`), generated by a script under the audit folder's `tools/` that asserts its row count.
- [ ] `02-forward-audit.md` § The credentials' paths has one row per credential kind (the Wi-Fi key, the scraper's developer pair and account, the RetroAchievements keys through `HttpReq`, the root password's default) per sink it can reach (argv, a file and its mode, a log, a query, the unverified peer, the screen, the packet), each at its line, with the mask at that sink or `none`.
- [ ] `02-forward-audit.md` § The writers is generated by a script under the audit folder's `tools/` (the generator asserts its row count and exits 1 on drift), one row per write of `es_settings.cfg`, `system.cfg` and their copies, per `AtomicFile::` call and per `writeAllText(` call under `es-app/src` and `es-core/src` (27 `writeAllText` sites at the pin, sixteen of them `ApiSystem.cpp`'s sysfs writes, carried as `sysfs` rows), and per shell writer at `8ebaf8daad`: temp-and-rename or in place, `fsync`, the lock, the mode, the positive check, the failure's remainder.
- [ ] `02-forward-audit.md` § The readers states each parse's edge cases (no `=`, an empty key, an empty value, a BOM, a duplicate, a file under three bytes, a missing file) with the line that handles or drops each, and the recovery ladder's cases against their tests.
- [ ] `02-forward-audit.md` § The client has one row per `curl_easy_setopt` and per `HttpReqOptions` field with its value and default, the thread model stated, and #1154 cited.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason; the generated test build's summary lines, the kill-the-writer fixture's result for both stores and the shell writers, and the seed-before-the-record case are among them.
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #668 (the comment's time; the START and RETURN posts with their first-line contract and censuses), the image by file name and `BUILD_ID` read from the guest at 640x480, the modes of both stores, their copies, the cookie jar and the keyfile as written, the recovery ladder on the image for both stores with the player's frame, the key-on-argv count with the value masked, the `7z` positive, the #1154 positive's endpoint log, the live scraper sign-in's outcome or its `CANNOT in this window`, the disk retired with path, size and sha, the leftover check.
- [ ] `00-running-log.md` shows no image build, no fetch (the council runtime from `npm install --offline`), no handheld, the owner's accounts never named or used, no hosted account but the QA ones, no M7 root, worktree or prep directory, the guest only inside the granted window, four keyed invokes and every other council call keyless (`00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q8 are answered at their lines; every `bug` states its trace, its `Already written:` line and its VM line in the four families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` in the shape the lane writes.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; `02` § What T26 and the OS slices inherit lists the quoting rule, the stores' keys, the writers' contract and the `7zr` question's answer with their lines.
- [ ] The retro exists at `docs/retros/<date>-m6-es-state-and-bridge.md`, is posted on #668, says what the slice did to the two time-to-play numbers (the BIOS enumeration at launch when its setting is on, and the save at a page's close, named with what they cost on the guest; cited from `docs/vm-qa-log.md` and T18's window), and what T26 and the OS slices inherit.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch and the ES fork's `.githooks/pre-push-test` on the ES branch before the hand-back merge; every fix on the ES branch has, recorded beside its commit, `tools/es-syntax-check` PASS where a toolchain exists or else the host `g++ -fsyntax-only` pass or its `CANNOT` with the missing header named, the unit tests' summary lines, and a clean non-ASCII comment grep.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back); the stage-D pause; an explicit maintainer
pause on #668; a blocker named on #668 (a seat that fails its provenance
gate twice, a packet scan hit that is a value, two commands that disagree, a
block whose output differs from § 2's beyond the deltas it records; **not**
the host's missing toolchain, which § 5 names and the generated `g++` build
and the `CANNOT` forms absorb); an ES worktree that differs from the pin on
one of the 14 at stage A; or an execution limit, stated as such with the
running log current. A checkpoint is not a stop. An idle session says it is
idle on #668, **and does not end a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#668`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #668` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window granted on #668; the QA ScreenScraper and
  RetroAchievements accounts only, never the owner's, D-QA-015/016; nothing
  on a handheld).
- The mini-retro at stage G, posted on #668, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (none
  expected); D-WORKFLOW-209 is the highest Decided row on the coordinator's
  branch and D-CLOUD-185 the highest cloud row (D-WORKFLOW-188 on the P1
  branch only; the merge unites them); a row this slice forces takes an ID
  the coordinator assigns on #668.
- `tools/ceremony-check --gate` before every push of the distribution
  branch and the ES fork's `.githooks/pre-push-test` after an ES change;
  never `--no-verify`; a merge with conflicts is checked for markers; the
  ledgers united by whole entries; **a commit names its paths**; anything
  temporary under `/workspace/tmp/m6-t21/` after `df -i`, never `/tmp`; the
  window's record kept on the branch, the guest disk retired after it with
  the retirement recorded in `00` (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never inside
  a `bash -c` script**; **the unit tests built by the generated `g++`
  command before every commit on the ES branch**; a fixture that rewrites
  no path, in a bubblewrap sandbox started with `--clearenv`; the walks'
  steps under the audit folder's `stage-e/walks/`, never under `tools/`.
- Commit messages `docs: ...` on the distribution branch, with `Refs #668`;
  on the ES branch the package's convention, `Refs #668, #<bug>`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#668's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the four provenance files (read directly) and the
manifest's scans; the audit issue's checkboxes all at an outcome; the
coverage table's row count (14), § The commands' rows, § The writers'
generated count, § The client's rows; every Q bug with its three lines;
**re-running on clones of both branches at their tips under
`/workspace/tmp/m6-coordinator/`: the membership block and every § 5 run in
full** (no guest: the window's record is read, not repeated);
`register-check` on a simulated merge with the coordinator's tip; the
retro's answers; the five checkers' exit codes. The lane posts one hand-back
comment naming **both tips** and each artifact by path, writes
`reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` into
#668's body, then says it is idle. After acceptance the coordinator closes
the audit issue, prompts the lane for `audit-completion.json` and the lint
against **the audit issue**, merges the distribution branch in its turn
after the M7 candidate with the pin moved to the ES branch's tip in the same
integration commit (the ES package built before it lands), regenerates the
ledgers, posts any #585 lines in the shape the lane wrote, and closes #668
when every row is proven; the interface epic #700 closes when its slices
have.

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro takes a T21 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.

**What never runs in this slice:** an image build, a compiler beyond the
host's `g++ -fsyntax-only` and the generated test build, a fetch (the
council runtime from `npm install --offline`), a handheld, the owner's
accounts or any hosted account but the QA ones the window names, a guest
before a grant on #668, M7's roots, worktrees or prep directories, a change
outside the 14 files and the audit folder except under a stream brief, a
move of the pin.

## Version 2: what the stranger's proof of version 1 corrected (2026-10-26)

A reader with no context ran version 1 (`601bd5d10f`) from the P1 clone and the pin by hash, seven commands; § 2's block, every per-file count and delta, the executors, the exit sites, the client's options, the stores' lines, the tests' counts and the French all held. What did not, corrected above:

1. **The runs block disagreed with its own comments on the correct tree** -- a § 8 stop condition as written: the `wifictl` line picked an audit copy under `docs/audits/` (now pinned to the shipped script); the `post-update` path carried a spurious `scripts/` and `git grep -c` is silent on zero matches (now `git show` and `grep -c` with `rc` on its own line); the `7zr` grep hit a `.ttf` and `|| echo` bound to `sed` (now the recipe's `all3`/`bin/7z*` lines); the tests loop omitted `LogPolicyTests` (77 against 80); the `7z` grep could not print `:1527`/`:1578`/`:1659` (`getSevenZipCommand`); `Scraper.cpp:524` and `main.cpp:1041-1042` were unreachable by their patterns (`maskSecrets`, `wasRecovered` added); the popup grep's `head -n 20` never reached `GuiWifi.cpp`; the syntax-check path lacked `utils/`; the `WEXITSTATUS` count is 15 lines with the `#define` shims.
2. **`GuiWifi.cpp:460`/`:462` is `update()`**; the key's popup is `:365`/`:367`, the name's `:295`/`:297`, and neither popup class takes a password parameter at all (`.h:15-16`, `.h:13-14`): masking is a mode to add.
3. **`timeout N` is not on every `wifictl` call**: `:642` (`enable <ssid> <key>`), `:767`, `:771`, `:775` have no bound.
4. **The `7zr` claim was not what the recipe says**: p7zip builds `all3` and installs `bin/7z*`; whether `7zr` is on the image is the window's listing, not a finding.
5. **`getBiosInformations` is gated by `CheckBiosesAtLaunch`** (default false, `Settings.cpp:207`), not run at every launch.
6. **`SystemConf`'s forward to `Settings` is the empty-path case** (`:288`, `:426`, `:442`, `:469`, `:480`), not `#if WIN32` and not `:19-25` (`mapSettingsName`); its own defaults table carries `global.retroachievements.hardcore` `"0"` (`:46`); whether the path can be empty on ROCKNIX is Q4's to read in `Paths`.
7. **D-NET-011 has no row**; the range reads 001 to 016 less 011.
8. **Counts restated with their methods**: 105 `batocera-` lines, 36 names (not "62 sites"); 293 `getInstance()->` lines in 41 files (not 289/40); 16 `WifiText::` names (not 17); `SystemConf.cpp` 15 commits in the range, 11 on 2026-09-28 (not 29/21); `AtomicFileTests` lines naming `chooseConfig` 22, `saveUnderLock` 10, `readText` 9; `GuiWifi.cpp` 628/76 by `numstat`; `SystemConf.cpp` 332/54.
9. **`Settings.cpp:478` is the path line**; the 0644 is `AtomicFileUtil.cpp:115`'s default with `modeOf(path, 0644)` at `:533`/`:629`. **`AtomicFileUtil.cpp:50-64` is `createTemporary`**; `parseKeyValues` is `:453-469`.
10. The menu map's `:139` is the SCRAPER row; T2's lead is `04-analysis.md:142`; `2026_09_17-work_log.md:100` is not #102's closure; 22 `.steps` walks (25 entries); six wifi/scraper qa-log directories hold 0 png, not three; `NetworkManager.conf:19` carries no mode; the unit directory holds 19 files and 221 cases, the eight named are 80; `SystemConfTests` names `Settings::saveFile` once as a fixture; the writers generator finds 27 `writeAllText` sites, sixteen of them sysfs; three rule citations were bullets or paragraphs, not sections; `Scraper.cpp:524`'s mask is `maskSecrets`' word list (`StringUtil.cpp:513`); `:45-46`'s shims are cited under Q6.

What a stranger could not do from this file alone, unchanged: run stage A before the dispatch (the worktrees and the pointer are cut then); run § 2 from the coordinator's branch (`docs/reviews/*.json` are the P1 branch's -- the lane's worktree is stacked on it); see the four digests; find `tools/t18-build-tests.sh` (T18's audit folder, on its branch); settle `7zr` or the keyfile's mode without the window.
