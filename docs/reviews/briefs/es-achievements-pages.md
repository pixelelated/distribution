# Review brief: M6.P2 T20, EmulationStation's RetroAchievements and offline pages (#667)

**Version 1, 2026-10-26, the coordinator's** (D-WORKFLOW-189). Written from
four read-only research digests (the coordinator's scratch files, not in any
tree; every figure they gave is reproduced by a command below), the order's
§ T20, the slice record, T18's and T19's briefs and what their lanes found
on these files; the figures were produced at the hashes they name with
`/usr/bin/grep`, never the shell's function (#1138). A stranger's proof runs
before dispatch; version 2 records what it found
(`docs/reviews/plan-for-the-plan.md` § 6b).

## 1. Identity

- **Issue:** #667 `M6.P2 E700/T20: interface: EmulationStation's
  RetroAchievements and offline pages`, slice `es-achievements-pages`
  (`k: 20`) in `docs/reviews/slices.json`, twentieth in
  `docs/reviews/order.md` (its § T20 paths line: *"25 paths, 7,485 lines,
  7,427 read, of which 7,416 fork-own; 0 patch and config lines; reach
  shipped 25"*; its `why`: *"the account pages and the offline scan, which
  drive the proxy (16 interface files name it); with the fork-touched files
  of ES's vendored libcheevos (rcheevos and libretro-common), read as a
  diff against their imported version, since a local delta in the protocol
  library is invisible to a version row"*; kind read; lens security, new
  functionality; depth Extended, *"`RetroAchievements.*` is on the security
  list: the account's credentials (plan § 6c)"*). **Epic:** #700 (the
  interface: T2 #649 and T18 #665 accepted and closed out; this slice; T21,
  T26, T31 to T37 and T44 after), whose futro
  `docs/futros/2026-10-23-m6-interface.md` takes a T20 kickoff addendum
  written with this version; the area's other half is the proxy, T19 #666
  under #1139. **Milestone:** M6. **Predecessors:** #346, #641, **T2 #649**
  (`ProxyCards` and the launch's question: `docs/audits/2026_10_23-epic-m6-es-launch-path/`
  on `feature/m6-es-launch-path-649`, PL-013 the running game's pointer read
  at `ProxyCards.cpp:269`, PL-022 the top-up card after the screen stopped
  being free), **T18 #665** (the cloud pages, the ES sibling:
  `docs/reviews/briefs/es-cloud-pages.md` -- the host has no toolchain
  (#1137), the unit tests are built by a generated `g++` command, three
  GUI files are `CANNOT` for the syntax check; its findings on these files
  are in `02` § Findings index on `feature/m6-es-cloud-pages-665`; its
  Backlogs #1142 (the launch's stop wait), #1143 (one reader for both
  surfaces), #1144 (the suites)), **T19 #666** (the proxy, running in the
  T5 session: the protocol's producer side and the table T20 inherits --
  every `>>> ` token, every stamp's shape, the page comment's
  `have_account` wording; read its `02` § What T20 inherits on
  `feature/m6-offline-achievements-666` when it lands, and its brief
  `docs/reviews/briefs/offline-achievements-proxy.md` now), **T12 #659**
  (`tools/ra-ui-test` and its `assert` refusals PL-10; #1141 the harness at
  640x480), **T3 #650** (#825, PL-032: RetroArch's `cheevos_cmd` hook runs
  the achievement's title through `system()`), **T30 #677** (the standalone
  emulators' `cheevos_*.sh` token files, PL-009/010/020/021), **T1 #648**
  (`setsettings.sh`'s routing of RetroArch to the proxy per launch).
  **Beside it:** T19 in the T5 session until its close-out; the host is
  shared by `/tmp/m7-m6-host-coordination-20261023.txt` and a window for
  this slice is asked for on #667 and granted there in the queue.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #909, or decide a question of scope:
  those are the coordinator's, reached through #667, one question at a
  time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves, with its trace and `Already written:`
  line (D-WORKFLOW-187). A fix lands only under a stream brief the
  coordinator writes at the stage-D pause, **on the EmulationStation
  branch**. Twenty-four of the 25 are the fork's own; one header is
  upstream-carried (`GuiRetroAchievementsSettings.h`, 11 lines) and nine are
  the fork's edits inside a vendored library, read as diffs: a defect in
  the library's fork-touched lines is the fork's to fix; a defect in the
  library's imported lines is a contained fix here under
  `bugs-are-agent-first.md` rule 6 and a #585 line (D-WORKFLOW-164, never
  sent, D-WORKFLOW-165). D-UI-079 (change stays inside the lanes) is
  satisfied: these pages are the offline achievements lane. The read is
  the pin `16dbac5211`'s bytes; M7's worktrees are never read.
- **Two worktrees, one session.** The distribution's
  `feature/m6-es-achievements-pages-667` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-es-achievements-pages-667`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's
  pointer seeded (the two hashes in the dispatch comment on #667); and the
  EmulationStation fork's `feature/m6-es-achievements-pages-667` at
  `/home/max/Development/emulationstation-next.worktrees/m6-es-achievements-pages-667`,
  cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`**
  (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s
  `PKG_VERSION` names at `8ebaf8daad`): the sources are read and the fixes
  are made there, on that branch, and the pin is not moved by the lane. The
  other ES checkouts under `~/Development/emulationstation-next.worktrees/`
  are other lanes' and M7's: read with `git -C <checkout> show <hash>:<path>`
  only. Until the dispatch comment exists the pointer is not seeded, the
  first command's `cat` fails, and nothing starts.
- **Depth: Extended** -- two seats, as T18's stage C: GPT-6 Astra at `max`
  over a trimmed, scanned packet (D-WORKFLOW-195; T18's went out at 348 KB
  after a trim from 364 KB), a probe then one refutation; then Gemini 4
  Argon at `high` over the same packet plus the lane's grades of Astra, a
  probe then one refutation (one in-call retry is allowed, as T18's call 4
  needed); `review-plan.json` records depth `extended` and both reviewers
  with their served models; **exactly four keyed `tools/council/run invoke`
  calls**, every other `tools/council/run` call with
  `COUNCIL_ENV_FILE=/nonexistent`; the runtime from `npm install --offline`,
  no fetch. **The packet is scanned before it leaves:** these files handle
  the account's password, token and web API key by name
  (the four keys `global.retroachievements.{username,password,token,key}` are read at `GuiRetroAchievementsSettings.cpp:610-616` and sent at `RetroAchievements.cpp:149`, `:195`, `:1037`; the words appear as setting names and query parameters, never values -- read here as counts only),
  so the manifest records every scan hit and its disposition, and a hit
  that is a value stops the packet. Every seat item is re-read at its
  lines before it is graded.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the distribution worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-achievements-pages-667
cat .github/sessions/saved-session-state-feature-m6-es-achievements-pages-667.md  # the pointer: the dispatch's two hashes
git status --short | wc -l                                                          # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                      # empty: the read is of next's bytes
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here     # read locally, never fetched
W=/home/max/Development/emulationstation-next.worktrees/m6-es-achievements-pages-667; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                       # the pin; 0
git -C "$W" merge-base bccd715707 HEAD | cut -c1-10                                  # bccd715707: the merge base with ROCKNIX's master
git show feature/m6-es-cloud-pages-665:docs/audits/2026_10_26-epic-m6-es-cloud-pages/05-punch-list.md | /usr/bin/grep -c '^## PL-'   # T18's punch list is reachable (23)
tools/register-check >/dev/null && echo register-ok
tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200                  # who holds the host: no guest before a grant on #667
```

## 2. Scope

**The membership, by the block that defines it** (run from the lane's
distribution worktree, which is stacked on the P1 branch and so holds
`docs/reviews/{inventory.json,slices.json}`; the slice's `select` has two
entries, the pages' globs and the fork-own rows under `external/libcheevos/**`;
`W` is the ES worktree):

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k20 = [s for s in sl["slices"] if s["k"] == 20][0]; sels = k20["select"]
def expand(g):
    mm = re.search(r'\{([^{}]*)\}', g)
    if not mm: return [g]
    return [x for alt in mm.group(1).split(",") for x in expand(g[:mm.start()] + alt + g[mm.end():])]
def m(p, g): return fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2]))
def pick(sel):
    globs = sel.get("globs") or []; tiers = sel.get("tier"); areas = sel.get("areas") or [k20["area"]]
    es = [x[3:] for g in globs if g.startswith("es:") for x in expand(g)]
    return [r for r in rows if r["tree"] == "es" and r["area"] in areas and any(m(r["path"], g) for g in es) and (not tiers or r["tier"] in tiers)]
t20 = []
for sel in sels:
    for r in pick(sel):
        if r not in t20: t20.append(r)
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("selects", len(sels), "paths", len(t20), "lines", L(t20), dict(collections.Counter(r["reach"] for r in t20)), dict(collections.Counter(r["tier"] for r in t20)))
print(dict(collections.Counter(r["language"] for r in t20)))
CODE = {"c++", "c-header", "c", "cmake", "python", "shell"}
rd = [r for r in t20 if r["language"] in CODE]; print("read", len(rd), L(rd), "unread", [r["path"] for r in t20 if r not in rd])
fo = [r for r in t20 if r["tier"] == "fork-own"]; print("fork-own", len(fo), L(fo))
lib = [r for r in t20 if r["path"].startswith("external/libcheevos/")]; print("libcheevos rows", len(lib), L(lib))
os.makedirs(".qa-scratch/t20", exist_ok=True)
open(".qa-scratch/t20/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t20, key=lambda r: r["path"])))
for r in sorted(t20, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["path"])
PY
wc -l .qa-scratch/t20/paths.txt     # 25
W=/home/max/Development/emulationstation-next.worktrees/m6-es-achievements-pages-667; PIN=16dbac5211eea7e70db7394372033be2be7df829
while IFS= read -r p; do printf '%6d %s\n' "$(git -C "$W" show "$PIN:$p" | wc -l)" "$p"; done < .qa-scratch/t20/paths.txt | awk '{s+=$1} END {print "wc -l lines", s}'   # 7485
while IFS= read -r p; do git -C "$W" cat-file -e "bccd715707:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t20/paths.txt | wc -l   # the files that exist in ROCKNIX's master: read as diffs
```

Expected, at `2174265e9c` (the coordinator ran it on a clone at that commit
with `W` the `qa-integration` checkout at the pin): `selects 2 paths 25
lines 7485 {'shipped': 25} {'fork-own': 24, 'upstream-carried': 1}`;
languages `c++ 10, c-header 10, c 2, cmake 1, markdown 1, other 1`; `read 23
7427` (unread: `LICENSE.rvz-padding`, `RVZ-NOTICES.md`); `fork-own 24 7474`
(the order's 7,416 counts the 23 read rows); `libcheevos rows 9 2556`. The merge-base line's count is **17**: the eight account files and `ThreadedHasher.cpp/.h` are ROCKNIX's files rewritten by the fork (`GuiRetroAchievementsSettings.cpp` +704/-11, `RetroAchievements.cpp` +404/-28, the hasher 259 → 415 lines), the seven libcheevos files that exist at the base are the fork's edits inside the vendored library (526 insertions, 15 deletions over the nine, the whole directory's delta), and `OfflineAchievements.*`, `OfflineScanJob.*`, `GuiOfflineScan.*` and `rvz_hash.*` with the two notices are new; the inventory's `fork-own` is by the fork's share of the commits, and the read of a rewritten file is its diff against the base plus the lines the diff does not reach.

**The files, read whole, in this order** (lines at the pin):

| File | Lines | What it is |
| --- | ---: | --- |
| `es-app/src/RetroAchievements.cpp` / `.h` | 1,072 / 286 | the account client: every web-API URL carries `z=<username>` and `y=<web API key>` as GET queries (`:149`, `:195`, `:521`, `:634`, `:757`), the sign-in `p=<password>` (`:1037`, timeout 0, stall 0, on the interface thread inside `addSaveFunc`), the username also as the `User-Agent` (`:181-183`); the proxy's `u=<username>` with `X-RA-Store-Only` (`:301`, `:315`, `:338`); page requests 15 s total / 10 s connect on `GuiLoading` workers; the hash library's two requests with `stallTimeout` 30 s (#299); `CheevosRetry` 10 s x 9 then 120 min; curl's `getErrorMsg()` reaches a player (`:165` → `GuiRetroAchievements.cpp:44`, `GuiGameAchievements.cpp:42`); `throw e;` at `:923-926` slices the exception |
| `es-app/src/guis/GuiRetroAchievementsSettings.cpp` / `.h` | 808 / 11 (upstream-carried) | RETROACHIEVEMENTS SETTINGS (`:596-808`, 21 rows: the username unmasked `:610`, the password masked `:611`, the web API key masked `:616` under `#ifndef CHEEVOS_DEV_LOGIN`; two switches on `es_settings.cfg`, `RetroachievementsMenuitem` `:695` and `CheevosCheckIndexesAtStart` `:712`, the rest SystemConf; PROGRESS TRACKER hand-built; LED NOTIFICATIONS written at once) and OFFLINE ACHIEVEMENTS (BETA) (`:408-593`: the switch → `raofflineproxy-ctl enable|disable 2>/dev/null` on a detached thread, ok iff exit 0 and the last line starts `hardcore=` `:479-501`; the scan row's seven line variants and `raofflineproxy-ctl scan` at `:322` after `saveSystemConf()` `:321`; the comment naming `have_account` `:154`); the server's JSON `Error` shown verbatim `:784`; a runtime msgid `:671`; one `exists(` `:633` on the ctl's path, cached |
| `es-app/src/guis/GuiRetroAchievements.cpp` / `.h` | 471 / 54 | the account summary page (the player's games and progress from the web API; the offline summary from the ctl's `summary`); curl's error text at `:44` |
| `es-app/src/guis/GuiGameAchievements.cpp` / `.h` | 352 / 35 | one game's achievements page; curl's error text at `:42` |
| `es-app/src/OfflineAchievements.cpp` / `.h` | 353 / 148 | the ctl's one door from ES: `ask(verb)` `:51-57` keeps the last non-empty stdout line and `WEXITSTATUS(pclose())` **without `WIFEXITED`** (`ApiSystem.cpp:2278-2291`), so a ctl killed by an untrapped signal reads as exit 0; the verbs `pending` `:108`, `flushed` `:119`, `summary` `:250` (every line; a line over 1,023 bytes is split by `fgets` and its game dropped), `pending-ids` `:275`, `account` `:286`, `topup [--after-index]` `:318`, `index-offline` `:325`; the runtime paths `:26-41`, every ctl- or service-written file read uncached (`:127`, `:136`, `:147`, `:156`, `:192`), `online_state.json` missing or unparseable read as online by design (`:192-196`); `stopRun` `:339-358` proves the lock's holder by flock, cmdline and `/proc/<pid>/fd` dev/ino, then SIGTERM, 10 x 50 ms |
| `es-app/src/OfflineScanJob.cpp` / `.h` | 273 / 100 | the scan page's reader: a 1,024-byte cap (`:145`), `\r` and `\n` split, `cleanLine` shared with the card; `>>> pid` accepted from any line, any count, any n ≥ 1, and CANCEL signals the group `-n` as root (`>>> pid 1` would be `kill(-1, SIGINT)`; T18's reader has the same shape at `CloudTransferJob.cpp:272-278`, recorded latent there); unknown markers dropped without `changed()`; `run` checks `WIFEXITED` (`:156-157`) where `ask()` does not; the outcome per exit (0, 130, 69, 75 read as A SCAN IS ALREADY RUNNING when a top-up holds the lock, 77, 78, 1, -1, 143 from `disable` read as COULDN'T FINISH / SOMETHING WENT WRONG with no note); a detached thread holds the job, `sCurrent` keeps the last run for the session |
| `es-app/src/guis/GuiOfflineScan.cpp` / `.h` | 382 / 93 | the scan page, a fourth-tier page (D-UI-078) honoured: full screen, dimmed under, BACK → the cancel dialog only while running (YES then NO, NO null), the help bar drawn early; after a run that did not complete any button but OK closes it, a direction included; seven `TextComponent`s refreshed every frame and, with no `done` line, `cached_game_ids.txt` read every frame (`:299`) |
| `es-app/src/ThreadedHasher.cpp` / `.h` | 415 / 76 | upstream's hasher (259/59 lines at the base) rewritten: the constructor fetches the hash library **on the interface thread in all four callers** (`SystemData.cpp:1134`, `NetworkThread.cpp:251` via `postToUiThread`, `GuiMenu.cpp:1214`, `GuiRetroAchievementsSettings.cpp:800`), `stallTimeout` 30 s on the two requests; the after-index top-up (`--after-index`, `:152`) runs from the destructor on a worker thread only when `mCheevosIndexed` -- offline the queue is emptied and the path never reaches it (blindspot 64 in code); a race between `start()` `:375-392` and `run()` `:257-263` for a short lookup-only queue; `throw e;` at `:117` loses the library's message; `GuiMsgBox(window, e.what())` at `:399` outside `_( )`; `pause()`/`resume()` with no caller |
| `external/libcheevos/CMakeLists.txt` | 245 | `add_library(libcheevos STATIC ...)` with `-DRC_DISABLE_LUA`, the CHD/7zip/FLAC set, `-DHAVE_LROUND`; `ENABLE_RVZ_HASH` defaults to `${ROCKNIX}` (on for every device build), zstd or Boost missing is a `FATAL_ERROR`; it also compiles a stale rcheevos 10.7.0 generation (`src/rcheevos/rc_version.h`, `compat.c`, `rc_libretro.c`) beside the vendored 12.2.1 -- upstream-carried, outside this slice, **T44's**; `es-unit-tests` does not link it |
| `external/libcheevos/cheevos.cpp` / `.h` | 193 / 8 | the `.rvz` + GameCube dispatch and `gameCubeRvzHashEnabled()` (`1a4a2f12c`, `5a86caea9`); the hash path `ThreadedHasher` → `FileData::checkCheevosHash` → `RetroAchievements::getCheevosHashFromFile` (a zero sentinel on failure) → `generateHashFromFile` → `generateGameCubeRvzHash` (its own iterator and file reader, `rc_hash_generate(..., RC_CONSOLE_GAMECUBE, ...)`) |
| `external/libcheevos/rvz_hash.cpp` / `.h`, `LICENSE.rvz-padding`, `RVZ-NOTICES.md` | 389 / 7, 29, 29 | the bounded GameCube RVZ reader (`1a4a2f12c`, 2026-10-13): a byte-indexed lagged-Fibonacci padding generator (`:66-98`; 521 words, the `<<23 ^ >>9 ^ [i-1]` seeding, four initial advances, the 32-tap advance, byte shifts 24/18/8/0) attributed to bodgit/rvz at `bc439051cbed` under BSD-3, the notices installed by the ES recipe to `/usr/share/licenses/emulationstation/`; **this copy never had the defect** the proxy's Python twin (`rvz_datasource.py:655-671`) received patch 020 for a day later; RetroArch's GPL `cheevos_rvz.c` is a third, byte-granular copy kept as a reference under `docs/qa-logs/` and copied from nowhere by the README's word |
| `external/libcheevos/rcheevos/src/rhash/hash_disc.c` | 1,352 | the fork's +26/-14 inside rcheevos 12.2.1's disc hashing: every `rc_file_read` in `rc_hash_nintendo_disc_partition` and `rc_hash_gamecube` checked, the header-size sum widened to `uint64_t`, two `rc_file_close` calls that double-closed on `malloc` failure removed; **absent from upstream's 12.5.0** (the proxy's cached rcheevos; 140 changed lines there, none in the GameCube region) -- a #585 candidate for rcheevos; `dol_offsets`/`dol_sizes` still trusted as seek and length (now a failure, not a stale buffer) |
| `external/libcheevos/libretro-common/src/utils/md5.c` | 304 | the fork's +10/-1 (`314da58d6`): the cast-pointer word load replaced by a `memcpy` helper in the x86-only branch (no change on aarch64 handhelds); RetroArch's newer `md5.c` still dereferences the cast pointer; libretro-common carries no version marker; `tests/md5-alignment.c` is a standalone file no suite runs |

**The credential's paths** (the account digest § 1). Four keys. The
username: an unmasked row (`:610`), `z=` and `u=` on every web-API URL, `u=`
to the proxy, and the `User-Agent` header. The password: a masked row
(`:611`, through `GuiSettings.cpp:192/:229`), sent once as `p=` in a GET
query at `RetroAchievements.cpp:1037`. The token: set at `:777` and
`NetworkThread.cpp:268`, cleared at `:767`, `:780`, `:796`. The web API
key: a masked row (`:616`), `y=` on every page request. All four at rest in
clear text in `system.cfg` (T21's `SystemConf`; `backuptool` strips the
`.key=`, `.password=` and `.token=` lines from the archive, T17's). No
credential reaches a `LOG(` (nine in the client, two in the page,
enumerated) or a command line; `Utils::String::maskSecrets` exists and is
used only by `ApiSystem.cpp`. **Every request goes through `HttpReq`, whose
`es-core/src/HttpReq.cpp:192` sets `CURLOPT_SSL_VERIFYPEER` to 0** (upstream
batocera's 2021 line for the scrapers, carried by ROCKNIX): the password
and the key travel to an unverified peer. That is **#1154** (bug, Medium,
filed 2026-10-26 by the coordinator under #700 from this research, with
its trace and its VM proof): this slice does not re-find it; it cites it
in § The credentials' paths, and whether its stream is this lane's or
T21's (`HttpReq` is `es-state-and-bridge`'s file) is ruled at the stage-D
pause.

**The contract with the ctl** (the offline digest § 1; the other end is
T19's, read at `8ebaf8daad`). The ctl's `>>> ` protocol is `tell()`
(`raofflineproxy-ctl:835-837`, 20 call sites); its `say()` (`:371-373`) is
`logger`, syslog only -- T19's brief says `say()` where it means `tell()`,
an erratum for T19 at acceptance, not this slice's. The four `ask()` verbs'
shapes match their parsers (`CloudText::parsePendingCount`,
`parseFlushStamp` of `<epoch> <flushed>`, `OfflineAchievementsText::parseStoreGame`,
`parseAccountTotals`); the mismatches are the readers': `ask()`'s missing
`WIFEXITED` (a ctl killed by a signal → exit 0 → for `topup`, `COMPLETED` on
the card, `ProxyCards.cpp:338`, `:353`); `topup`'s 75, 77 and 78 unmapped
(*any other* → SOMETHING WENT WRONG, said only with `sawWork`); `summary`'s
1,023-byte split; the refresh verb EmulationStation never runs. The page
comment naming `have_account` (`:154`) is a comment: the ctl's function at
`:1119` is internal and the page implements the test from SystemConf.

**The stamps and the two takers** (the offline digest § 5). Nine paths; every
ctl- or service-written file read with `exists(path, false)`; the ctl's own
path cached (static, right). `last-flush` is polled for presence by the
page (`:127`) and taken by rename by `ctl flushed`: two takers cannot both
report, and `tools/ra-offline-test:239` is a second taker on guests.
`cached_game_ids.txt` can be two bytes (`es-code-traps.md` § A file under
three bytes reads as empty; `readAllText` at the pin not yet verified).

**The seam with T2's cards** (the offline digest § 6). T2's PL-013
(`ProxyCards.cpp:269`, the running game's pointer) and PL-022 (`:244-270`,
the top-up card after the screen stopped being free) are marked Resolved
by ES `05c8e4b5e` and `dce0b9b6b` on T2's branch, **neither an ancestor of
the pin**: the pin carries the seam as T2 found it, and the integration
moves the pin to a tip that carries both. `offlineIndexCard` (`:211-224`)
posts a card with no screen-free check at all (D-UI-093; T2's file, this
slice's card).

**The three hashers** (the libcheevos digest § 4). EmulationStation hashes
the index with rcheevos 12.2.1 plus its own RVZ reader; the proxy's
`libraproxy_rchash.so` is rcheevos 12.5.0 plus libchdr with the Python RVZ
reader (patch 020); RetroArch carries rcheevos 12.2.1 with its own
`cheevos_rvz.c` behind `HAVE_CHEEVOS_RVZ`, which the distribution's recipe
neither names nor disables -- whether the image's RetroArch has the reader
is unverified (T3's). The three agree on paper; **nothing at the pin proves
they agree on a padded region at a non-aligned offset**, which is exactly
where the proxy's was wrong for a day: `tools/ra-candidate-games --check`
hashes with NES/SNES rules only, `raofflineproxy-installed-native-test`'s
`test_linux_rom_hashing.py` at `c7ebd1b6` has no RVZ case, and the RVZ QA
log's README says no fixture was generated or run.

**The neighbours, and whose they are:** `HttpReq`, `ApiSystem` (the
`executeScriptLegacy` that echoes every ctl stdout line to the journal,
`:2284`) and `SystemConf` are **T21's** (#668); `ProxyCards` and
`FileData::launchGame` are **T2's** (accepted, its fixes on its branch);
the ctl and the proxy are **T19's** (#666, running: its `02` § What T20
inherits is this slice's input the moment it lands); `setsettings.sh`'s
routing and `runemu.sh` are **T1's**; RetroArch's `0012-cheevos-cmd.patch`
(#825, the title through `system()`) and its rcheevos are **T3's**; the
standalone emulators' `cheevos_*.sh` token files are **T30's**; the stale
10.7.0 rcheevos generation and the rest of `external/libcheevos/` are
**T44's**; `GuiMenu.cpp:188-191`'s gates on these pages are **T26's**.

**Already found; do not re-find** (cited at its lines): T2's PL-013 and
PL-022 (`docs/audits/2026_10_23-epic-m6-es-launch-path/` on
`feature/m6-es-launch-path-649`); T18's `02` § Findings index notes at
`:317` and `:321` (`ProxyCards::afterSync` over a launched game during the
linger -- S5's guard routed to this slice's issue #667) and its Backlogs
#1142, #1143, #1144 (`feature/m6-es-cloud-pages-665`); T12's PL-10 (the
`assert` refusals, `ra-ui-test` among them), PL-18, PL-19 (#986); T3's
PL-032 (#825); T30's PL-009/010/020/021; the proxy's own epic audit
`docs/audits/2026_09_14-epic-offline-retroachievements/05-punch-list.md`
(#186) PL-05, 06, 07, 08, 09, 10, 15, 17, 24, 26, 27, 28, 30, which name
the pages, the index and the hasher -- read before the questions; and
**#1154**. (The branches are named once here: T2
`feature/m6-es-launch-path-649`, T18 `feature/m6-es-cloud-pages-665`, T12
`feature/m6-tooling-vm-harness-659`, T3 `feature/m6-emulators-libretro-650`,
T30 `feature/m6-emulators-standalone-677`, T19
`feature/m6-offline-achievements-666`; the audit folders are
`docs/audits/<date>-epic-m6-<slice>/` on each, read with `git show
origin/<branch>:<path>` after no fetch.)

## 3. Read first

In this order, the working tree's copies (the coordinator's branch, merged
in): `.claude/rules/es-native-ui.md` § Core patterns (the credential row
`:89-90`; the card for fast work only `:94-98`; `exists(path, false)`
`:107-113`), § The cards at the link's return (`:144-173`, D-UI-101/109), §
the four surface tiers (`:205-212`: the scan page is the fourth tier,
D-UI-078), § One floating surface at a time (`:214-222`, D-UI-093), § A
fourth-tier page is sat in, with CANCEL (`:225-250`), § Anything automatic
that moves data is shown while it runs (`:254-272`, D-UI-095/096), § A
layout must not be computed from what it last produced (`:323-340`, the
SCAN GAMES row, blindspot 44); `es-player-text.md` § Conventions (`:79-137`:
the RETROACHIEVEMENTS card's words, D-UI-096/101-109; the index-offline
card D-UI-106) and § Outcome vocabulary (`:253-292`); `es-ui-style-guide.md`
§ Dim, don't hide (`:91-96`) and § Gating (`:273`); `es-code-traps.md` §
Three things a font is not (`:121-125`, the cache), § A pooled connection
(`:218-244`, the hasher's fetch on the interface thread, #299/#300), § A
file under three bytes; `generic-x64-vm-testing.md` (`:326-334` the hasher
and `/isIdle`; `:495-500` the RETROACHIEVEMENTS row's conditions; `:754-760`
the filter and `Invalid user/password combination`; `:890-895`
`--ra-offline` opt-in; `:1044-1090` the games with sets and `ra-offline-test`;
`:1150-1161` a settings change from the shell; `:1169-1186` `ra-ui-test`;
`:1246-1300` `frame-diff`); `least-surprise.md` and `time-to-play.md` (which
name none of these pages, and bind them anyway); `bugs-are-agent-first.md`
rule 6; `engineering-practices.md` § Consider contributing (D-WORKFLOW-164/165).

`docs/es-menu-map.md:578-657`, the map's rows for these pages -- **its line
`:595` still describes "a scan left running with B, PL-07", the design
D-UI-078 reversed (a D-UI-039 drift this slice corrects in the same change
as any row it touches), and the scan page's title and its CANCEL dialog are
absent from the map** (`tools/es-menu-map-check` passed because the check
reads titles, not copy; the lane records which).

`docs/decision-register.md`: the 22 `D-UI` rows for these pages (D-UI-053 to
-056, -067, -077, -078/-079, -092, -095/-096, -101 to -107, -109, -112, -113,
-119) and the 15 `D-RA` rows whose subject is the interface (the index, the
hasher, the top-up's two passes D-RA-035, the summary); **open: D-RA-006,
D-RA-026, D-UI-120, D-NET-013**. `docs/blindspot-register.md` 44 (the top-up
proven at fixture size), 46 (names read as behaviour in this subsystem),
64 (a wait lengthened for an event `ProxyCards::indexRanOffline`'s path
never reaches -- confirmed in the hasher's code), 65 (a shimmed ctl in a
proof), and 22, 39, 75 as always.

**The tests at the pin** (the record digest § 3): `OfflineAchievementsTextTests.cpp`
15 cases, `CheevosIndexTests.cpp` 6, `CheevosRetryTests.cpp` 7,
`OfflineProxyUrlTests.cpp` 4, `CloudTextTests.cpp`'s 9 RetroAchievements
cases of 70, `ProxyCardsTests.cpp` 11, `JobsTests.cpp`'s one scan-job case,
`tests/hasher-offline-index.py`. Every function of `OfflineAchievementsText.h`,
`CheevosIndex.h`, `CheevosRetry.h` and `CloudText.h`'s RetroAchievements
block is named by a test. **No test:** `RetroAchievements.cpp` (1,072 lines:
`getApiUrl`, `getCheevosHash*`, `toRetroAchivementInfo`,
`getGameInfoFromDevice`, `testAccount`), `OfflineAchievements.cpp` (its 18
functions appear in `ProxyCardsTests` only as fakes), `OfflineScanJob::cleanLine`,
`ThreadedHasher::formatGameName`, the three pages, `GameCubeRvzHashRetry.h`;
`es-unit-tests` does not link libcheevos, so the RVZ hash has no host test.

**The walks and frames** (the record digest § 4): one RetroAchievements walk,
`tools/vm-walks/m7-retro-achievements.steps` (36 lines, the #422 fixture:
frames `retroachievements-settings` and `offline-achievements`), **absent
from `suite.txt`, `claims.txt` and `masks.txt`, so `frame-diff` never
compares these pages and no accepted baseline exists for them**;
`tools/ra-ui-test`'s frames `baseline/{accept,refuse}-{sending,outcome,dismissed}`
and `empty-repeat` at EN and FR, 640x480 and 1280x960 (`docs/qa-logs/2026-10-06-ra-ui/`,
69 frames, 109 PASS, 23 reviewed, `docs/vm-qa-log.md:179`); the installed
top-up packets of 2026-10-14 with no frames. `to-manage-cloud-storage.steps:7-8`
assumes no sign-in (signed in, the main menu opens on its RETROACHIEVEMENTS
row first).

**The French:** 222 `_("` occurrences, 177 unique literals across the pages
and `ProxyCards.cpp`, 177 of 177 present and translated in the catalog at
the pin (2,189 msgids, 0 empty, 0 fuzzy); run-time-composed strings not
counted (`tools/es-untranslated` is the check).

**The record of the proxy's and the pages' proofs:** the proxy's epic audit
(#186); `docs/qa-logs/2026-10-06-ra-award/` and `2026-10-06-ra-ui/`;
`docs/qa-logs/2026-10-1{3,4}-*proxy*`; the RVZ QA log with its README's *no
fixture was generated or run*; `docs/cloud-sync-changelog.md`'s achievements
entries. The issues the tree names: #186, #241, #292, #293, #298, #299,
#300, #305, #306, #465, #986, and now #1154, #1141, #1142, #1143, #1144 --
read on GitHub at stage A.

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of four families: **where a credential
travels** (a query string, a header, an unverified peer, a log, a command
line, the screen), **a contract read one-sidedly** (an exit or a line one
end prints and the other does not expect), **a check whose failure reads as
success**, **a library edit without its upstream**. The leads below are
the digests' by shape; each is read at its lines before it is called
anything.

- **Q1 The credential's paths.** Every sink of the four keys at its line;
  #1154 cited, not re-found (the peer); the username in the `User-Agent`
  and in every query; the clear text at rest in `system.cfg` against what
  `backuptool` strips; the sign-in with timeout 0 and stall 0 **on the
  interface thread** inside `addSaveFunc` (`CheevosRetry::saveSignIn`'s
  `Now`) -- the screen frozen for as long as the server takes on a bad
  link (`es-code-traps.md` § A pooled connection); curl's `getErrorMsg()`
  and the server's JSON `Error` shown to a player verbatim
  (`player-language.md`: a tool's words never reach a player); the
  runtime msgid at `:671`; `maskSecrets` unused here.
- **Q2 The contract, both ends.** `ask()`'s `WEXITSTATUS` without
  `WIFEXITED` and what each caller then shows (a top-up killed by a
  signal → COMPLETED); the unmapped 75/77/78 for `topup`; the 1,023-byte
  `summary` line; the last-line rule against a ctl that prints two; the
  `>>> pid` accepted from any line and `kill(-n)` as root (`>>> pid 1`);
  the outcome per exit for the scan (75 as A SCAN IS ALREADY RUNNING, 143
  from `disable` as COULDN'T FINISH with no note); T19's inheritance table
  consumed when it lands, and this slice's half written as § The contract.
- **Q3 The stamps and the files.** The two takers of `last-flush`;
  `online_state.json` absent read as online; `cached_game_ids.txt` read
  every frame by the scan page and possibly two bytes; the runtime paths'
  modes as the ctl writes them (T19's finding: no `umask` anywhere -- read
  from the guest); `exists(` second arguments (all `false` for the ctl's
  files; the one cached read right).
- **Q4 The pages.** Every row's builder, store and save mechanism against
  `es-ui-style-guide.md` (two switches on `es_settings.cfg` where the
  launch scripts read SystemConf -- which scripts read
  `RetroachievementsMenuitem` and `CheevosCheckIndexesAtStart`?); HARDCORE
  MODE with two writers (the page and the ctl's `enable` line) and nothing
  holding it while the proxy is on; `Settings.cpp:420`'s same-named
  `.hardcore` default and who reads it; the dialogs' button order (all
  safe by the digest's read: NOT NOW / LATER / NO last -- verified at their
  lines); the scan page's fourth-tier contract and its every-frame reads;
  the settings page's 1 s refresher against the `layoutRows` trap (closed
  at the pin, ES `7c7ffab43`); the menu map's `:595` drift and the two
  missing entries.
- **Q5 The hasher.** The library fetch on the interface thread in four
  callers with its 10 s connect + 30 s stall bound (the freeze is the
  bound; moving it off the thread is #300's follow-up, not this slice's
  change unless ruled); the after-index top-up that offline never runs
  (blindspot 64); the `start()`/`run()` race for a short queue; `throw e;`
  slicing at `:117`; `e.what()` outside `_( )` at `:399`; `pause()`/`resume()`
  with no caller; the zero sentinel re-hashing permanently unsupported
  RVZs (a design fact, named).
- **Q6 The library.** Each of the nine as a diff: what the fork changed,
  the upstream it came from, whether upstream has it (the `hash_disc.c`
  read checks, the `uint64_t` sum and the double close absent from 12.5.0:
  three #585 lines for rcheevos; `md5.c`'s x86-only `memcpy`), the licence
  notices present and shipped (bodgit/rvz BSD-3; Boost and zstd declared,
  not copied); the stale 10.7.0 generation compiled beside 12.2.1 named for
  T44, not changed here.
- **Q7 One hash, three hashers.** The paper agreement of the three RVZ
  readers on the padding generator and on the partial-word case; what
  would prove it (one synthetic RVZ with a packed region at `offset % 4 !=
  0`, hashed by EmulationStation's index, by the proxy's `.so` on the
  guest, by RetroArch where it has the reader, against the raw ISO's MD5)
  -- `CANNOT` with the fixture named if no RVZ can be made without a
  fetch, and the coordinator's harness Backlog follows at the stage-D
  pause (`bugs-are-agent-first.md` rule 3).
- **Q8 The harness.** `tools/ra-ui-test` (what it proves: the reconnect
  cards with a synthetic award; what it cannot: the pages themselves),
  the one walk with no baseline and no claim (a `frame-diff` gap: every
  change to these pages is uncaught -- a harness finding for #1144's
  family), `tools/es-untranslated`, `tools/es-menu-map-check`'s blindness
  to copy; for each lead this slice confirms, the constructed positive
  that fails on the pin's bytes (the self-signed endpoint for #1154's
  unfixed half; a ctl stub killed by a signal under `ask()`; a `summary`
  line over 1,023 bytes; a two-byte `cached_game_ids.txt`), on the host
  where the pure parts allow (the generated `g++` build) and on the guest
  where they do not.

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #667.** Every read, count and table runs on the host
   at the pin's bytes. **The host has no toolchain** (#1137): the pure
   parts' tests (`es-unit-tests` with `OfflineAchievementsTextTests`,
   `CheevosIndexTests`, `CheevosRetryTests`, `OfflineProxyUrlTests`, the
   RetroAchievements cases of `CloudTextTests`; `proxycards-tests`,
   `jobs-tests`) are built with the host's `g++` by the command T18's
   `tools/t18-build-tests.sh` generates from the two `CMakeLists.txt`
   (copied into this audit folder's `tools/`, its source list recorded;
   rapidjson by a named copy with provenance, or the dependent cases named
   as not run); `tools/es-syntax-check` records its exit-2 line with
   `ES_BUILD_ROOT` set, never empty; the pages and the hasher include SDL
   and are `CANNOT` for the host's `g++ -fsyntax-only` (as T18's three
   were), their compile proof the integration build's; `RetroAchievements.cpp`
   and `OfflineAchievements.cpp` are tried the same way and recorded as they
   fall. `tools/es-menu-map-check --es-src <W>` and `tools/es-untranslated
   --es-src <W>` run on the host. **A new unit case is the proof of choice
   for every pure lead** (the exit mapping, the line cap, the two-byte
   file, the parsers). The libcheevos diffs are read against the base and,
   where the cache holds a tarball, against the proxy's rcheevos 12.5.0
   (`/workspace/cache/rocknix-sources/raofflineproxy-rcheevos/` if present;
   the exact 12.2.1 import is `CANNOT` without a fetch).
2. **The guest window** -- one, asked for on #667 at stage B's end with its
   plan and bound (45 minutes proposed), granted explicitly in the shared
   log's queue, one boot of the M6 copy of the image
   (`/workspace/artifacts/m6-t2-20261023/`, `069fc2704421`) **started at
   640x480** (`generic-x64-vm run --res`; `vm-pair` has no option, #1141),
   the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each
   post's first line with the census, the stop by pidfile at bound plus
   grace, the disk retired after with path, size and sha (D-INFRA-022):
   the identity (`BUILD_ID`, a `_( )` literal of these files absent from
   the base found by `strings`); the QA RetroAchievements account carried
   in by `tools/qa-accounts` (D-QA-016; never the owner's, D-QA-015);
   `tools/ra-ui-test` at 640x480, EN and FR, with `--failure-control`; the
   walk `m7-retro-achievements.steps` and the scan page over a seeded small
   library (running, the cancel dialog, done) with every frame's strings
   read back; the runtime files' modes after a scan; **the #1154 positive**
   -- `retroachievements.org` pointed by the guest's hosts file at a
   host-run TLS endpoint with a self-signed certificate, the sign-in from
   the page reaching it on the pin's binary (the endpoint's log; no value
   printed); and **one live sign-in with the QA account** against the real
   server, last, if the bound allows (over the unverified peer the pin has;
   the QA account's password is throwaway and D-QA-016's), recorded
   `CANNOT in this window` otherwise. Every proof's frames are
   `pin-binary` evidence; a fix's frame is `fix-walk-pending-image`.
3. **What T21 and T26 inherit** is written, not tested here: `ask()`'s
   reader in `ApiSystem.cpp:2278-2291` (T21's file, this slice's caller),
   `HttpReq`'s options (#1154), `SystemConf`'s clear text; `GuiMenu.cpp`'s
   gates and the `cheevos_cmd` title's source (T26's and T3's).
4. **A fix lands only under a stream brief** at the stage-D pause, on the
   ES branch, proven twice (`fix-unit-test` or `fix-walk-pending-image`),
   the unit tests built before every commit, the walks' steps under
   `stage-e/walks/`.

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its
reason). From the distribution worktree after the membership block; `W` the
ES worktree, `PIN` the pin; counts by `/usr/bin/grep` (#1138):

```bash
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-achievements-pages-667; PIN=16dbac5211eea7e70db7394372033be2be7df829; G=/usr/bin/grep
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t20/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
# the ES worktree at the pin, clean; the merge base (expect the pin; 0; bccd715707)
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l; git -C "$W" merge-base bccd715707 HEAD | cut -c1-10
# the credentials' sinks (expect the four keys at GuiRetroAchievementsSettings.cpp 610, 611, 616; z= and y= at RetroAchievements.cpp 149, 195, 521, 634, 757; p= at 1037; User-Agent 181-183; u= to the proxy at 301, 315, 338; VERIFYPEER 0 at HttpReq.cpp:192 and VERIFYHOST 0 at :200, #1154)
git -C "$W" grep -n -E 'global\.retroachievements\.(username|password|token|key)' "$PIN" -- es-app/src/guis/GuiRetroAchievementsSettings.cpp | sed "s/^$PIN://" | cut -c1-110
git -C "$W" grep -n -E '[?&](z|y|p|u)=' "$PIN" -- es-app/src/RetroAchievements.cpp | sed "s/^$PIN://" | cut -c1-120; git -C "$W" grep -n -E 'User-Agent' "$PIN" -- es-app/src/RetroAchievements.cpp | sed "s/^$PIN://" | cut -c1-100
git -C "$W" grep -n -E 'SSL_VERIFY(PEER|HOST)' "$PIN" -- es-core/src/HttpReq.cpp | sed "s/^$PIN://"
# no credential in a LOG( line (expect 0 LOG( lines naming a password, token or key value in the two files; maskSecrets used in ApiSystem.cpp only)
git -C "$W" grep -n -E 'LOG\(' "$PIN" -- es-app/src/RetroAchievements.cpp es-app/src/guis/GuiRetroAchievementsSettings.cpp | sed "s/^$PIN://" | $G -i -E 'passw|token|key' | wc -l; git -C "$W" grep -c 'maskSecrets' "$PIN" -- es-app/src es-core/src | sed "s/^$PIN://"
# the ctl calls and the reader (expect scan :322 after saveSystemConf :321; enable|disable :479; the have_account comment :154; ask() :51-57; WEXITSTATUS without WIFEXITED at ApiSystem.cpp:2278-2291; OfflineScanJob::run with WIFEXITED :156-157; the 1024 cap :145)
git -C "$W" grep -n -E 'raofflineproxy-ctl|have_account' "$PIN" -- es-app/src/guis/GuiRetroAchievementsSettings.cpp es-app/src/OfflineAchievements.cpp | sed "s/^$PIN://" | cut -c1-120
git -C "$W" show "$PIN:es-app/src/ApiSystem.cpp" | sed -n '2278,2291p' | $G -n -E 'WEXITSTATUS|WIFEXITED|pclose'; git -C "$W" show "$PIN:es-app/src/OfflineScanJob.cpp" | $G -n -E 'WIFEXITED|WEXITSTATUS|1024|>>> pid' | cut -c1-110
# the exists( cache (expect one cached read at GuiRetroAchievementsSettings.cpp:633 on the ctl's path; every ctl file read with false in OfflineAchievements.cpp)
git -C "$W" grep -n -E 'FileSystem::exists\(' "$PIN" -- es-app/src/OfflineAchievements.cpp es-app/src/guis/GuiRetroAchievementsSettings.cpp es-app/src/OfflineScanJob.cpp es-app/src/ThreadedHasher.cpp es-app/src/RetroAchievements.cpp | sed "s/^$PIN://" | cut -c1-120
# the network client's bounds (expect the login request with no timeout; page requests 15 s / 10 s; the hash library stallTimeout 30 s; the hasher constructed in four callers)
git -C "$W" grep -n -E 'stallTimeout|\.timeout|connectTimeout' "$PIN" -- es-app/src/RetroAchievements.cpp es-app/src/ThreadedHasher.cpp | sed "s/^$PIN://" | cut -c1-110; git -C "$W" grep -n -E 'new ThreadedHasher|ThreadedHasher\(' "$PIN" -- es-app/src | sed "s/^$PIN://" | cut -c1-110
# the strings (expect 222 _( ) occurrences in the eight sources and ProxyCards.cpp; es-untranslated 0; the texts outside _( ): e.what() at ThreadedHasher.cpp:399, curl's error text at RetroAchievements.cpp:165)
git -C "$W" grep -c '_("' "$PIN" -- es-app/src/RetroAchievements.cpp es-app/src/OfflineAchievements.cpp es-app/src/OfflineScanJob.cpp es-app/src/ThreadedHasher.cpp es-app/src/guis/GuiRetroAchievements.cpp es-app/src/guis/GuiRetroAchievementsSettings.cpp es-app/src/guis/GuiGameAchievements.cpp es-app/src/guis/GuiOfflineScan.cpp es-app/src/ProxyCards.cpp | sed "s/^$PIN://"; tools/es-untranslated --es-src "$W" 2>&1 | tail -n 2
# the menu map (expect es-menu-map-check 0 missing; the :595 line naming PL-07; the scan page's title absent from the map)
tools/es-menu-map-check --es-src "$W" 2>&1 | tail -n 1; $G -n -E 'PL-07|left running' docs/es-menu-map.md | cut -c1-120; $G -c -i -E 'SCANNING|OFFLINE SCAN' docs/es-menu-map.md
# the walks and the baseline (expect one RA walk, 36 lines; 0 lines naming it in suite.txt, claims.txt, masks.txt; ra-ui-test --help exit 0)
wc -l tools/vm-walks/m7-retro-achievements.steps; $G -c -i -E 'retro|achiev|offline' tools/vm-walks/suite.txt tools/vm-walks/claims.txt tools/vm-walks/masks.txt; tools/ra-ui-test --help >/dev/null 2>&1; echo "ra-ui-test --help rc=$?"
# the library's delta (expect the whole directory's diff base..pin equal to the nine rows, 526 insertions 15 deletions; rcheevos 12.2.1 in rc_version.h and a stale 10.7.0 beside it)
git -C "$W" diff --stat bccd715707 "$PIN" -- external/libcheevos | tail -n 1; git -C "$W" grep -n -E 'RCHEEVOS_VERSION_(MAJOR|MINOR|PATCH)' "$PIN" -- external/libcheevos | sed "s/^$PIN://" | cut -c1-100
# the tests at the pin (expect 15, 6, 7, 4 cases; CloudTextTests' RA cases; the unit tests built by the generated command: the summary lines or CANNOT with the sources left out)
for f in OfflineAchievementsTextTests CheevosIndexTests CheevosRetryTests OfflineProxyUrlTests; do printf '%s: ' "$f"; git -C "$W" show "$PIN:es-app/tests/unit/$f.cpp" | $G -c 'TEST_CASE'; done; git -C "$W" show "$PIN:es-app/tests/unit/CloudTextTests.cpp" | $G -c -i -E 'retroachievements|offline'
echo "the lane's tools/t20-build-tests.sh (from T18's) generates the g++ lines from both CMakeLists, names every -I, and records each binary's summary line"
# the syntax check (expect exit 2 on this host with ES_BUILD_ROOT set, never empty) and the host g++ on three files (expect CANNOT naming SDL for the pages and the hasher; the pure files as they fall)
ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" es-app/src/OfflineAchievements.cpp 2>&1 | tail -n 1; echo "rc=$?"
for f in es-app/src/OfflineAchievements.cpp es-app/src/RetroAchievements.cpp es-app/src/guis/GuiOfflineScan.cpp; do printf '%s: ' "$f"; g++ -std=c++17 -fsyntax-only -I "$W/es-app/src" -I "$W/es-core/src" -I "$W/external" "$W/$f" 2>&1 | tail -n 1 | cut -c1-100; echo "rc=${PIPESTATUS[0]}"; done
# the removal check from the dispatch tip -- <dispatch tip> is the lane tip the dispatch comment on #667 names (expect empty: nothing under packages/ projects/ tools/ changed at stages A to D) and the ES diff against the pin (expect empty before stage E)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -n 1; git -C "$W" diff --stat "$PIN" HEAD | tail -n 1
```

## 6. Outputs

As T18's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-es-achievements-pages/`:
`00` to `05`, `second-opinions/` (both seats' plans, the manifest with its
three-way scan and every scan hit's disposition, each probe and refutation
with provenance), `guest-cycle/` (the window's record: the image's identity
against the pin, the frames at 640x480 with their strings read back,
`ra-ui-test`'s outputs, the leftover check), the lint before D, the audit
issue (`Audit: M6 T20 EmulationStation's RetroAchievements and offline pages
-- N findings (...)`, a sub-issue of #667), the bugs, and the retro at
`docs/retros/<date>-m6-es-achievements-pages.md` (**what the slice did to
the two time-to-play numbers**: the hasher runs at the game list update and the top-up after the index, not on the launch path, and the cards at the link's return are T2's, so the answer cites `docs/vm-qa-log.md` and T18's window's three numbers (0.56 s to a first frame, the exit sync's stamp 1.58 s, game to game 1.01 s) and names the one place these files sit on a launch: nowhere, unless the lane finds one; **what T21 and T26 inherit**: `ApiSystem`'s command assembly,
`HttpReq`'s options, the main menu's rows). **`02` carries § Coverage (25),
§ The credentials' paths (one row per credential kind -- the password, the
token, the web API key, the username -- per sink it can reach: a setting
store, a request's query, a log, a shell command, the screen, the packet --
with the mask at that sink or `none`), § The pages (one row per page and
dialog: title, rows, builders, gates, stores, save mechanism, the strings'
count), § The contract (both ends of every ctl verb: what the ctl prints at
`8ebaf8daad`, what the page keeps and parses, each mismatch; T19's
inheritance table consumed when it lands), § The reader (the `>>> ` reader's
markers, caps, lifetimes, the stop path), § The hasher (what it hashes,
where it runs, the stall timeout, the top-up, the index-offline path), § The
library (one row per fork-own libcheevos file: the diff against the imported
version, the upstream it came from, the licence notice; the three hashers'
versions and the seam), § The runs (every § 5 command), § The guest cycle,
§ Positives, and every proof with `proved:`.** The stage-D pause as T18's:
the punch list posted on #667, the lane waits for the coordinator's
dispositions and any stream brief.

## 7. Acceptance

The checklist on #667 becomes this section at dispatch, written there by
the coordinator in place of P1's generated ones. Every checkbox names the
artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-es-achievements-pages/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-achievements-pages/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`).
- [ ] `second-opinions/review-plan.json` records `depth: extended` and two reviewers (`gpt`, `openai/gpt-6-astra`, `max`; `gemini-argon`, `google/gemini-4-argon`, `high`); each seat's probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly); `packet-manifest.json` carries the three-way scan with every hit dispositioned by name; the running log shows exactly four keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #1154, #585, #668, #673, #691, an M7 issue by number), withdrawn or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail.
- [ ] `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in the checklist's header carry the lane's commits; the ES read is on the pin's bytes for the 25 (`git -C <W> diff --stat 16dbac5211 <reviewed-at-es> -- $(cat .qa-scratch/t20/paths.txt)` empty before stage E) and nothing under the distribution's `packages/`, `projects/` or `tools/` changed at any stage.
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (25 paths, 7,485 lines; read 23 / 7,427; fork-own 24; libcheevos 9 / 2,556; 17 in the merge base -- or the deltas beside them) and the per-file line table at the pin.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `25`.
- [ ] `02-forward-audit.md` § The credentials' paths has one row per credential kind (the username, the password, the token, the web API key) per sink it can reach (a setting store at rest, a query string, a header, the unverified peer #1154, a log, a shell command, the screen, the packet), each at its line, with the mask at that sink or `none`.
- [ ] `02-forward-audit.md` § The pages has one row per page and dialog (title, rows, builders, gates, stores, save mechanism, the strings' count, the dialog's button order), and states the two `es_settings.cfg` switches with what reads them.
- [ ] `02-forward-audit.md` § The contract has one row per ctl verb EmulationStation runs, both ends: what the ctl prints at `8ebaf8daad` (its `tell()` literals and exits), what the page keeps and parses at its line, each mismatch named (`WIFEXITED`, the unmapped 75/77/78, the 1,023-byte split, the two takers of `last-flush`); T19's `02` § What T20 inherits consumed if it has landed, or named as pending.
- [ ] `02-forward-audit.md` § The reader and § The hasher state the `>>> ` reader's markers, caps and lifetimes with the stop path, and the hasher's fetch thread, bounds, the after-index top-up's offline path (blindspot 64) and the `start()`/`run()` race, each at its line.
- [ ] `02-forward-audit.md` § The library has nine rows (the diff against the base, the upstream it came from, whether upstream's 12.5.0 has it, the licence notice, the #585 line owed) and states the three RVZ hashers' paper agreement with what would prove it (`CANNOT` with the fixture named if no synthetic RVZ can be made).
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason; the generated test build's summary lines (or the cases not run) and the syntax check's `CANNOT` lines are among them.
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #667 (the comment's time; the START and RETURN posts with their first-line contract and censuses), the image by file name and `BUILD_ID` read from the guest at 640x480, the identity literal, `ra-ui-test`'s outputs at EN and FR, the walk's and the scan page's frames with their strings read back, the runtime files' modes, the #1154 positive's endpoint log, the live sign-in's outcome or its `CANNOT in this window`, the disk retired with path, size and sha, the leftover check.
- [ ] `00-running-log.md` shows no image build, no fetch (the council runtime from `npm install --offline`; the rcheevos import `CANNOT` without a tarball), no handheld, the owner's RetroAchievements account never named or used, no hosted account but the QA one, no M7 root, worktree or prep directory, the guest only inside the granted window, four keyed invokes and every other council call keyless (`00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q8 are answered at their lines; every `bug` states its trace, its `Already written:` line and its VM line in the four families and passes `tools/box-check --issue N`; every #585 line owed is written in `02` § The library in the shape the lane writes.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; every punch item carries `question:`; `02` § What T21 and T26 inherit lists `ask()`'s reader, `HttpReq`'s options, the gates and the title's source with their lines on both sides.
- [ ] The retro exists at `docs/retros/<date>-m6-es-achievements-pages.md`, is posted on #667, says what the slice did to the two time-to-play numbers (cited from `docs/vm-qa-log.md` and T18's window; these files are off the launch path, and it says where it checked), and what T21 and T26 inherit; `docs/es-menu-map.md`'s `:595` line and the scan page's entries are corrected in the same change as any row the slice touches (D-UI-039), or the correction is a punch item with its owner.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch and the ES fork's `.githooks/pre-push-test` on the ES branch before the hand-back merge; every fix on the ES branch has, recorded beside its commit, `tools/es-syntax-check` PASS where a toolchain exists or else the host `g++ -fsyntax-only` pass or its `CANNOT` with the missing header named, the unit tests' summary lines, and a clean non-ASCII comment grep.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back); the stage-D pause; an explicit maintainer
pause on #667; a blocker named on #667 (a seat that fails its provenance
gate twice, a packet scan hit that is a value, two commands that disagree, a
block whose output differs from § 2's beyond the deltas it records; **not**
the host's missing toolchain, which § 5 names and the generated `g++` build
and the `CANNOT` forms absorb); an ES worktree that differs from the pin on
one of the 25 at stage A; or an execution limit, stated as such with the
running log current. A checkpoint is not a stop. An idle session says it is
idle on #667, **and does not end a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#667`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #667` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window granted on #667; the QA RetroAchievements account only,
  never the owner's, D-QA-015/016; nothing on a handheld).
- The mini-retro at stage G, posted on #667, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (none
  expected); D-WORKFLOW-209 is the highest Decided row on the coordinator's
  branch and D-CLOUD-185 the highest cloud row (D-WORKFLOW-188 on the P1
  branch only; the merge unites them); a row this slice forces takes an ID
  the coordinator assigns on #667.
- `tools/ceremony-check --gate` before every push of the distribution
  branch and the ES fork's `.githooks/pre-push-test` after an ES change;
  never `--no-verify`; a merge with conflicts is checked for markers; the
  ledgers united by whole entries; **a commit names its paths**; anything
  temporary under `/workspace/tmp/m6-t20/` after `df -i`, never `/tmp`; the
  window's record kept on the branch, the guest disk retired after it with
  the retirement recorded in `00` (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never inside
  a `bash -c` script**; **the unit tests (`es-unit-tests`, `jobs-tests`,
  `proxycards-tests`) built by the generated `g++` command before every
  commit on the ES branch** (plan § 6b's stream practice); the walks' steps
  under the audit folder's `stage-e/walks/`, never under `tools/`.
- Commit messages `docs: ...` on the distribution branch, with `Refs #667`;
  on the ES branch the package's convention, `Refs #667, #<bug>`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#667's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the four provenance files (read directly) and the
manifest's scans; the audit issue's checkboxes all at an outcome; the
coverage table's row count (25), § The credentials' paths' rows, § The
contract's both-ends rows, § The library's nine rows; every Q bug with its
three lines; **re-running on clones of both branches at their tips under
`/workspace/tmp/m6-coordinator/`: the membership block and every § 5 run in
full** (no guest: the window's record is read, not repeated);
`register-check` on a simulated merge with the coordinator's tip; the
retro's answers; the five checkers' exit codes. The lane posts one hand-back
comment naming **both tips** and each artifact by path, writes
`reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` into
#667's body, then says it is idle. After acceptance the coordinator closes
the audit issue, prompts the lane for `audit-completion.json` and the lint
against **the audit issue** (`--issue <audit issue>`, never the slice's),
merges the distribution branch in its turn after the M7 candidate with the
pin moved to the ES branch's tip in the same integration commit (the ES
package built before it lands), regenerates the ledgers, posts any #585
lines in the shape the lane wrote, and closes #667 when every row is proven;
the interface epic #700 closes when its slices have.

**The readings before dispatch** (plan § 3, principle 3): the interface
epic's futro takes a T20 kickoff addendum written with this version, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.

**What never runs in this slice:** an image build, a compiler beyond the
host's `g++ -fsyntax-only` and the generated test build, a fetch (the
council runtime from `npm install --offline`; rcheevos's imported version
read from the download cache if present, never cloned), a handheld, the
owner's RetroAchievements account or any hosted account but the QA one
(reached by the one sign-in the window names, if at all), a guest before a
grant on #667, M7's roots, worktrees or prep directories, a change outside
the 25 files and the audit folder except under a stream brief, a move of
the pin.
