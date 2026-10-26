# Review brief: M6.P2 T19, the offline achievements proxy (#666)

**Version 2, 2026-10-26, the coordinator's** (D-WORKFLOW-189; version 1 the same hour, corrected by a stranger's proof -- thirteen corrections, listed at the end). Written from four read-only research digests (the coordinator's scratch files, not in any tree; every figure they gave is reproduced by a command below), the order's § T19, the slice record, and the eighteen patches' commit history; the figures were produced at the hashes they name with `/usr/bin/grep`, never the shell's function (#1138). The stranger's proof of version 1 ran before dispatch from the scratch clone at `2174265e9c` (ten commands); this version records what it found (`docs/reviews/plan-for-the-plan.md` § 6b).

## 1. Identity

- **Issue:** #666 `M6.P2 E1139/T19: offline-achievements: the offline achievements proxy`, slice `offline-achievements` (`k: 19`) in
  `docs/reviews/slices.json`, nineteenth in `docs/reviews/order.md` (its
  § T19 paths line: *"27 paths, 5,369 lines, 3,656 read, of which 3,656
  fork-own; 1,703 patch and config lines; reach shipped 27"*; its `why`:
  *"a network listener holding the player's account token, all fork-own
  (+3,666), and the cheapest product area to finish; its 18 fork-written
  patches to the upstream proxy are read here, not in the patch tables
  (pass 6)"*; kind read; lens security, new functionality; depth Extended,
  *"a network listener and an account credential (plan § 6c)"*).
  **Epic:** #1139 (offline achievements: this slice, then T20 #667, the RetroAchievements pages in EmulationStation, under the interface epic #700), filed 2026-10-26 with its futro `docs/futros/2026-10-26-m6-offline-achievements.md` posted on it; #666 re-parented and retitled.
  **Milestone:** M6. **Predecessors:** #346, #641, **T2 #649**
  (`ProxyCards`, `JourneyTiers`: the cards at the link's return and the
  launch's question over the proxy's send -- the ES end of this slice's
  stamps; its audit `docs/audits/2026_10_23-epic-m6-es-launch-path/` on `feature/m6-es-launch-path-649`: PL-013 (the running game's pointer read at `ProxyCards.cpp:269`, `:410`, `:416`, `:479`) and PL-022 (`ProxyCards.cpp:244-270`, the top-up card after the screen stopped being free)),
  **T1 #648** (the launch scripts that route RetroArch to the port at game start: `setsettings.sh:532-545`; `runemu.sh:335` at `8ebaf8daad` writes `cheevos_custom_host = "http://127.0.0.1:4874"` -- the lowerdeck proxy on dual-screen devices, not this proxy's port; the `ra_lifecycle_*` admission and `exec 199>&-` seam are T1's stream insertions on `feature/m6-os-launch-control-state-648`, absent from `8ebaf8daad`; PL-004 of its audit, `docs/audits/2026_10_23-epic-m6-os-launch-control-state/` on that branch, is the `retroachievements.hardcore` override), **T22 #669** (the systemd units read under the Extended recipe, `docs/audits/2026_10_25-epic-m6-os-system-services/02-forward-audit.md` on `feature/m6-os-system-services-669`: the proxy's unit is read here, its directives against the per-unit rows that audit gives -- the lane names the section it finds them in), **T17 #664** (`docs/reviews/briefs/cloud-setup-content.md`, the closest sibling: a listener with a credential; `backuptool` holds `/storage/.config/raofflineproxy/` back as DEVICEONLYDIRS `:723-726` and the token files and settings as RATOKENFILES `:698-703` and RATOKENSETTINGS `:705-709`: what this slice's state looks like in a settings backup is settled there), **T15 #662** (`tools/last-good-scripts-test`: blindspot 43's cases r and s plant a `cheevos_password` value in `exec.log`; its proxy cases name the marker, the lock and the stamps around its lines 1006-1065, 1599-1668 and 2147-2315 and setsettings' `cheevos_custom_host` at 1893-1898; whether any case runs the ctl itself is a stage-A read, recorded whatever it says), **T10 #657** (the pre-commit pattern a fixture must
  not trip, #1061), **T45 #692** (the council runner the seats go through).
  **Beside it:** T18 in the T5 session (the cloud pages in ES; no shared
  path); the host is free since M7's RETURN of 09:12 UTC on
  `/tmp/m7-m6-host-coordination-20261023.txt`, and a window for this slice
  is asked for on #666 and granted there in the shared log's queue.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6
  body, edit `slices.json`, `areas.json`, `order.md` or the plan, file a
  Backlog issue, post on #346, #585 or #168, or decide a question of
  scope: those are the coordinator's, reached through #666, one question
  at a time. What it does file: its own audit punch-list issue (stage D)
  and a `bug` issue for a defect it proves, with its trace and `Already
  written:` line (D-WORKFLOW-187). A fix lands only under a stream brief
  the coordinator writes at the stage-D pause. **Nine of the 27 are the
  fork's own files and eighteen are the fork's patches to upstream's
  proxy** (§ 2): a defect in a fork file or on a patch's `+` side is the
  fork's to fix; a defect in upstream's unpatched code is a contained fix
  here under `bugs-are-agent-first.md` rule 6 and a line for #585 in the
  shape the lane writes (D-WORKFLOW-164: the target, the current-source
  comparison, the minimal patch), never a submission (D-WORKFLOW-165).
  D-WORKFLOW-209's class decision reaches nothing here. The read is
  `8ebaf8daad`'s bytes; M7's worktrees are never read.
- **One worktree, one session.** Branch `feature/m6-offline-achievements-666`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-offline-achievements-666`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's
  pointer seeded; the two hashes are in the dispatch comment on #666.
  Until that comment exists the pointer is not seeded, the first command's
  `cat` fails, and nothing starts. The session is the one the dispatch
  comment names. The EmulationStation fork is read-only context here
  (`git -C /home/max/Development/emulationstation-next.worktrees/qa-integration show 16dbac5211:<path>`,
  never its working tree); no ES worktree is cut for this slice.
- **Depth: Extended** -- two seats, as T17's stage C: GPT-6 Astra at `max`
  over a trimmed, scanned packet (D-WORKFLOW-195), a probe then one
  refutation; then Gemini 4 Argon at `high` over the same packet plus the
  lane's grades of Astra, a probe then one refutation; `review-plan.json`
  records depth `extended` and both reviewers with their served models;
  **exactly four keyed `tools/council/run invoke` calls**, every other
  `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`, `--help`
  included; the runtime from `npm install --offline`, no fetch. **The
  packet is scanned before it leaves**: the ctl handles the account's
  token and password by name (the ctl defines `USER_KEY`, `TOKEN_KEY` and `PASSWORD_KEY` at `:311-313` and reads the token and password for presence only (`:1120-1121`); patch 008's description names the redaction of `t=` and `p=` in the upload bundle; the scanner's words appear as names, never values -- read here as counts only), so the manifest records every scan
  hit and its disposition, and a hit that is a value stops the packet.
  Every seat item is re-read at its lines before it is graded.
- **Model and effort:** Opus 5.5 at high effort, written into `00` at
  stage A.
- **The first commands** (stage A, in the worktree):

```bash
cd /workspace/repos/pixelelated/distribution.worktrees/m6-offline-achievements-666
cat .github/sessions/saved-session-state-feature-m6-offline-achievements-666.md  # the pointer: the dispatch's two hashes
git status --short | wc -l                                                        # 0
git log --oneline -3; git merge-base --is-ancestor 8ebaf8daad HEAD && echo stacked
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                    # empty: the read is of next's bytes
git diff --stat 8ebaf8daad HEAD -- tools | tail -1                                # P1's own files under tools/, nothing else
git rev-parse --verify 651150fc88^{commit} >/dev/null && echo upstream-next-is-here   # read locally, never fetched
git show feature/m6-es-launch-path-649:docs/audits/2026_10_23-epic-m6-es-launch-path/05-punch-list.md | /usr/bin/grep -c '^## PL-'   # T2's punch list is reachable (its PL-013 and PL-022 are the cards' side of this slice's stamps)
tools/register-check >/dev/null && echo register-ok
tail -n 3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200                # who holds the host: no guest before a grant on #666
```

## 2. Scope

**The membership, by the block that defines it** (run from the lane's worktree, which is stacked on the P1 branch `feature/m6-p1-survey-641` at `2174265e9c` and so holds `docs/reviews/{inventory.json,slices.json,order.md,areas.json}` -- the coordinator's branch alone does not; the coordinator ran it on a clone at that commit; the slice's `select` has two entries, the area's own files and the patches-and-configs rows under the proxy's package globs):

```bash
python3 -I - <<'PY'
import json, collections, os, fnmatch, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
sl = json.load(open("docs/reviews/slices.json"))
k19 = [s for s in sl["slices"] if s["k"] == 19][0]; sels = k19["select"]
def expand(g):
    mm = re.search(r'\{([^{}]*)\}', g)
    if not mm: return [g]
    return [x for alt in mm.group(1).split(",") for x in expand(g[:mm.start()] + alt + g[mm.end():])]
def m(p, g): return fnmatch.fnmatchcase(p, g) or (g.endswith("/**") and p.startswith(g[:-2]))
def pick(sel):
    areas = sel.get("areas") or [k19["area"]]; globs = sel.get("globs") or []
    inc = [x for g in globs if not g.startswith("!") for x in expand(g)]; exc = [x for g in globs if g.startswith("!") for x in expand(g[1:])]
    return [r for r in rows if r["tree"] == "distribution" and r["area"] in areas and (not inc or any(m(r["path"], g) for g in inc)) and not any(m(r["path"], g) for g in exc)]
t19 = []
for sel in sels:
    for r in pick(sel):
        if r not in t19: t19.append(r)
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("selects", len(sels), "paths", len(t19), "lines", L(t19), dict(collections.Counter(r["reach"] for r in t19)), dict(collections.Counter(r["tier"] for r in t19)))
print(dict(collections.Counter(r["language"] for r in t19)), dict(collections.Counter(r["area"] for r in t19)))
pa = [r for r in t19 if r["area"] == "patches-and-configs"]; print("patch-and-config rows", len(pa), L(pa))
os.makedirs(".qa-scratch/t19", exist_ok=True)
open(".qa-scratch/t19/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t19, key=lambda r: r["path"])))
for r in sorted(t19, key=lambda r: r["path"]): print(r["lines"], r["language"], r["tier"], r["reach"], r["path"])
PY
wc -l .qa-scratch/t19/paths.txt     # 27
```

Expected, at `2174265e9c` (the coordinator ran it on a clone at that
commit): `selects 2 paths 27 lines 5369 {'shipped': 27} {'fork-own': 9,
'vendor-carried': 18}`; languages `recipe 3, none 1, python 3, shell 1,
systemd 1, patch 18`; areas `offline-achievements 9, patches-and-configs
18`; `patch-and-config rows 18 1703`. The nine fork-own files hold 3,666
lines (the order's "3,656 read" leaves out the ten-line daemon file, whose
language the inventory records as `none`).

**The files, read whole, in this order** (lines at `8ebaf8daad`, equal to
the inventory's at `2174265e9c`):

| File | Lines | Language | What it is |
| --- | ---: | --- | --- |
| `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl` | 2,455 | shell | the control script: `#!/bin/bash`, no `set -` by design (`:268-270`), no `pipefail`, 55 functions (`:371-2196`), exit constants `EX_USAGE=64`, `EX_UNAVAILABLE=69`, `EX_TEMPFAIL=75`, `EX_NOPERM=77`, `EX_CONFIG=78` (`:316-320`), the bounds `PROBE_TRIES=9`, `PROBE_INTERVAL=10`, `STOP_WAIT=10`, `ERRORS_IN_A_ROW=3`, `TOPUP_INTERVAL=1800`, `TOPUP_TIMEOUT=900` (`:325-337`), `IMAGE_PASS_SECONDS=300` (`:1849`); drives the unit (`systemctl` on 6 non-comment code lines, 9 by word), the three python helpers under `timeout`, the scan (`:1969-2110`), the top-up (`:2200-2300`), the stamps the cards read, the toggle and hardcore keys in `system.cfg` (`set_setting` on 8 code lines); the embedded `python3 -c`/heredoc blocks (six by the digest's count of block starts, seven by word) read the store read-only (`mode=ro` at every `sqlite3.connect`); its exits are 1 at `:378`, `:1991`, `:2413`, `:2425`, 2 at `:560`, `:565`, `:639`, `:2453`, 3 at `:762`, `:1843`, 130 at `:1821`, 143 at `:1797`, 0 at `:2016`, `:2227`, `:2237`, `:2430` |
| `.../sources/raofflineproxy-cache-images` | 497 | python | the badge cache pass: `--seconds 300`, the verify pass at most half, 4 workers, `as_completed` with a timeout, 404/410 recorded `absent` with a 24 h recheck (`write_absent` temp + `os.replace`), `PNG_FLOOR 68`, patch 013's `png_problem` (every chunk's CRC to IEND, the IDAT inflated) before the rename and under `--verify`; `verify-cursor` written directly (`:169-177`), the one stamp here without temp-and-rename |
| `.../sources/raofflineproxy-refresh` | 232 | python | the hourly refresh pass the ctl runs under `timeout 960` with `--seconds 900`: `cached_games`, `row_ages`, `drop_startsession`; three failures in a row stop it (`why REPEATED_FAILURES`); its `note()` prints to **stdout** (`:50-51`), on the same stream as the `>>> ` protocol |
| `.../sources/raofflineproxy-cache-indexed` | 222 | python | the index-fed preparation: `_counting_http_get`, a 30 s sleep per 50 jobs, `RAOFFLINEPROXY_IMAGE_WAIT` 120 s, the client's rate-limit pause honoured; the username reaches it by `RA_SCAN_USER` in the environment (`ctl:1265`) |
| `.../package.mk` | 157 | recipe | the upstream pin `c7ebd1b6e777f3751ff0ecdf8aba54045844e00d` (`misantronic/RAOfflineProxy`), `PKG_SHA256 88eef31a...` (the cached tarball `raofflineproxy-c7ebd1b6e777f3751ff0ecdf8aba54045844e00d.tar.gz`, one of fourteen in the cache directory), depends `Python3 bash busybox coreutils grep systemd raofflineproxy-rcheevos raofflineproxy-libchdr`; installs the module to site-packages as `.pyc` only, the four scripts 0755 to `/usr/bin`, `libraproxy_rchash.so` 0644 to `/usr/lib`, enables the unit; its header comment (line 6) says *"The 16 patches apply at fuzz 0"* while 18 patch files ship; GPL-3.0-only |
| `.../system.d/raofflineproxy.service` | 46 | systemd | the unit: `ExecStart=/usr/bin/python3 -m raofflineproxy.main run-service` (`:33`), `ExecStartPost=/usr/bin/raofflineproxy-ctl listening --wait 30` (`:40`), `ConditionPathExists=/storage/.cache/services/raofflineproxy.conf` (`:7`), `After=network.target network-base.service rocknix-sysconfig.service`, `Before=emustation.service essway.service`, `Restart=on-failure`, `RestartSec=5`, `TimeoutStopSec=15`, a start limit of 5 in 300 s; **no `User=`, no `Protect*`, `Private*`, `NoNewPrivileges`, `CapabilityBoundingSet`, `Memory*`, `CPU*` or `UMask=`** -- the proxy runs as root with the unit's defaults |
| `.../daemons/006-raofflineproxy` | 10 | none | sets `STATE`, `SVC`, `CONF` and `DAEMONS` for the shared `099-networkservices` pass, which rewrites the marker and starts or stops the unit from `system.cfg`'s `global.retroachievements.offlineproxy` at boot (the marker is not in a settings backup; the toggle is) |
| `.../raofflineproxy-libchdr/package.mk` | 24 | recipe | pins libchdr `607694ca0812edfc9cc2030c64634fc2393668de` (BSD-3); its comment cites a proxy commit (`3036478f`) older than the parent's pin |
| `.../raofflineproxy-rcheevos/package.mk` | 23 | recipe | pins rcheevos `1433173220a7eaede6a9ed7a18e94117be1821e0` (MIT); its comment cites `5866cd9b`, older than the parent's pin; RetroArch's own rcheevos is T3's |
| `.../patches/001-dorequest-4xx-passthrough.patch` … `021-flush-reconnect-during-startup.patch` | 1,703 | patch (18) | the fork's changes to upstream's proxy, read as diffs against the pin: fixes 001, 002, 005, 007, 009, 012, 013, 015, 019, 020, 021; features 003 (the flush stamp), 004 (`budgeted=False` for the deliberate whole-library drain), 008 (the storage-corruption report gated on `upload_logs` being JSON `true`), 010 (`X-RA-Store-Only`), 011 (`X-RA-Proxy` and the offline-login header), 016 (`cached`/`absent`/`transient`); identity 018. The absent numbers: 006 retired by `ce1dbcc986` (upstream exempts every game row from eviction), 014 and 017 by `409250ebce`/`e2761d15f9` (upstreamed connection reuse and subset mapping, 2026-10-03). The series is chained: 001→011→012→015, 009→013→016, 008→021. 020 and 021 carry no header and cite issues only through `f9b7ce3dfb` (Refs #583, #584, #588). The cached tarball's sha256 equals `PKG_SHA256`; every patch's distinctive `+` line is absent from it and every probed context line present |

**What the proxy is.** Upstream RAOfflineProxy is a Python service between
an emulator's rcheevos client and retroachievements.org on `127.0.0.1:8080`:
it answers `dorequest.php` from a local SQLite store when the link is down,
queues awards earned offline and flushes them when the link returns, and
caches game data and badges. The fork ships it as a package with eighteen
patches, a systemd unit, and four fork-own scripts: the ctl, which is the
OS's and the interface's one door to it, and three python helpers the ctl
runs under `timeout`. The service's own code (`proxy_service.py`, `state.py`, `es_export.py`, `log_uploader.py`, `config.py`) is **not in the tree**: it is read from the download cache's tarball **named by the pin** -- `/workspace/cache/rocknix-sources/raofflineproxy/raofflineproxy-c7ebd1b6e777f3751ff0ecdf8aba54045844e00d.tar.gz`, sha256 equal to `PKG_SHA256`; the directory holds fourteen tarballs of other revisions, and the first by name is a 2026-09-25 tree, not the pin -- as the pin's bytes with the patches applied by hand (§ 5), never fetched.

**The listener** (the sources digest § 2). The bind is the client's
`proxy_host` default, `127.0.0.1` (`config.py:367` in the tarball), AF_INET
only; the port is hardcoded in the ctl's `listening` check (`:932`, which
accepts a LISTEN at `0100007F:1F90`, at `00000000:1F90` and at the
v4-mapped form), in its badge base (`:651`), in `setsettings.sh:538`,
`cheevos_ppsspp.sh:97` and `cheevos_dolphin.sh:142`, and it is the port
`cloud_oauth`'s serve also takes (`cloud_oauth:2549-2560`, T17's): a sign-in
in progress and the proxy contend for one port. **No authentication on the
port**: the store answers `dorequest.php?r=patch|achievementsets|unlocks&u=<username>`
and `/Badge/` to any local client (EmulationStation itself at
`OfflineAchievements.cpp:200-235` and `WebImageComponent.cpp:240-241`, with
`X-RA-Store-Only: 1`; the header selects behaviour, not identity). **The
unit runs the service as root with no hardening directive** (no `User=`,
`Protect*`, `Private*`, `NoNewPrivileges`, `CapabilityBoundingSet`,
`Memory*`, `CPU*`, `UMask=`); `ExecStartPost` runs `ctl listening --wait
30`, so a foreign process on `0.0.0.0:8080` satisfies the start. The marker
`/storage/.cache/services/raofflineproxy.conf` gates the unit and has two
writers: `enable`/`disable` and `099-networkservices` at boot from
`daemons/006`.

**The credential** (the sources digest § 3). The keys are defined at
`ctl:311-313`; the token and password are read for presence only
(`:1120-1121`) and never into a variable; the **username travels on
`python3`'s argv at `:616`, `:647`, `:764` and `:1029`** -- readable in
`/proc/<pid>/cmdline` -- while `:1244-1246` states the file's own rule
(*through the environment, never a command line*) and `:1265` follows it;
`do_account` reads the `login2::<user>` row that holds the session token
and prints only `score= softcore=` (`:787`, checked by `case` at `:795-798`).
The helpers take credentials only from the client's `resolve_credentials`
(refresh `:130`, cache-indexed `:173`, cache-images `:293`). The client's own
log redaction (`t=`, `p=`) lives in the tarball; patch 008's description
says the storage-corruption bundle is redacted and carries the account
name. **No script sets a file mode** (no `umask`, `chmod` or `chown`
anywhere in the four; no `UMask=` in the unit), so everything the proxy
writes takes root's umask under systemd or EmulationStation's when the ctl
runs from a page. The per-emulator token files are T30's (PL-009, PL-010,
PL-020, PL-021 on `feature/m6-emulators-standalone-677`); `exec.log`'s
`cheevos_password` is blindspot 43, T1's guard.

**The writers** (the sources digest § 3b; one generated row each in `02`):
the marker (`touch`); `last-scan` (`write_stamp :1094`, temp + `mv -f`,
read by `CloudText::parseScanStamp`); `running` (temp + rename; removed by
the EXIT traps `:1981`, `:2268`); `scan-cursor` (`os.replace` then `mv -f`
with a read-back, `:1112-1113`); `scan.log` (append; rotated once past
1,048,576 B inside `slog` only, `:843-846`, while the helpers' stderr
appends at `:1711`, `:1713`, `:1876`, `:1987`, `:2301`, `:2366` bypass the
check); `last-topup-attempt` (an unguarded `touch`, `:2264`);
`index-pending` (temp + rename under the `pending_lock` fd 6, `:2154-2155`;
acknowledged by rename to `.ack.$$`, `:2170-2179`); `last-flush` (the
**service's**, patch 003's `flusher.py`, `tmp.write_text` + `os.replace`;
the ctl renames it to `.$$`, reads one line and removes it, `:812-814`);
`proxy.sqlite3` (never written by the ctl: `mode=ro` at every
`sqlite3.connect`, `:580`, `:612`, `:679`, `:767`, `:982`, `:1477`);
`cached_game_ids.txt` (the client's export, `es_export.py`, atomicity not
yet read); `online_state.json` (the service's monitor; the ctl's probe
writes its own copy in a `mktemp -d` scratch and deletes it, `:1137-1141`);
`verify-cursor` (cache-images `:169-177`, a direct `write_text`, the one
stamp here without temp-and-rename); `absent` (temp + `os.replace`); the
badge files (a per-pid, per-thread temp and `os.replace`, patches 009 and
013); the `system.cfg` keys through `set_setting` at eight sites;
`/tmp/raofflineproxy-*` from ten `mktemp` sites, all under the EXIT traps.
**`write_stamp`'s status is ignored by every caller** (`:1094` against
`:2103`, `:2411`, `:2423`, `:2427`).

**The bounds** (the sources digest § 6): the refresh under `timeout 960`
with `--seconds 900`, three failures in a row stop it; cache-indexed sleeps
30 s per 50 jobs, waits 120 s for badges, honours the client's rate-limit
pause; cache-images `--seconds 300`, the verify pass at most half, four
workers, 404/410 recorded absent with a 24 h recheck; **the scan has no
deadline of its own** (`:2062`); the top-up has one 900 s deadline, one
attempt per 1,800 s, nine 10 s probes, and a recently-played gate on the
history file's mtime (`:2229-2238`, an `-nt` comparison on devices without
a clock); the badge-cache's `png_problem` inflates every IDAT with no
`max_length` (patch 013, lines 121-124); patch 015's name lookups spawn one
daemon thread per attempt and abandon it after 3 s with no cap on how many
are alive.

**The neighbours, and whose they are** (the neighbours digest). On the
EmulationStation side at `16dbac5211`, eleven files name the ctl; every call
goes through `OfflineAchievements.cpp:51-57 ask(verb)`, which keeps the
**last stdout line** and the exit: `pending` (`:108`), `flushed` (`:119`,
`CloudText::parseFlushStamp` of `<epoch> <flushed>`), `summary` (`:250`,
every line as JSON), `pending-ids` (`:275`), `account` (`:286`, `score=
softcore=`), `topup [--after-index]` (`:318`, the exit only; 143 and 130
read as stopped at `ProxyCards.cpp:291-294`), `index-offline` (`:325`), and
`stopRun` (`:339-358`: SIGTERM to the flock's holder proved by
`/proc/<pid>/fd` inode); `GuiRetroAchievementsSettings.cpp:322` runs the literal `raofflineproxy-ctl scan` on the scan page (its `>>> ` lines read by `OfflineScanJob`), `:479` `enable|disable` requiring a `hardcore=` last line; a comment at `:154` names `have_account`, which is the ctl's **internal function** (`:1119`, called at `:1170`) and not a verb in the dispatch (`:2434-2450`) -- the page implements the test itself from SystemConf, so the drift is a comment's wording, T20's to tidy. **Those files are T20's (#667) and T2's;** this
slice reads the producer side of that contract -- every `>>> ` token, every
stamp's shape, every last line -- and records what T20 inherits. On the OS side at `8ebaf8daad`, five files outside the three packages name the proxy by word (`git grep -w raofflineproxy`): `setsettings.sh:532-545` (routing per launch, fail-closed: `cheevos_custom_host = 127.0.0.1:8080` only when the toggle is 1, hardcore reads 0 and the port answers), `cheevos_ppsspp.sh:94-98, 125-129`, `backuptool` (RATOKENFILES `:698-703`, RATOKENSETTINGS `:705-709`, DEVICEONLYDIRS `:723-726`: the proxy's folder is never in a settings backup), `001-functions:113` and `packages/virtual/network/package.mk:13` (which ships it); `cheevos_dolphin.sh:19, 139-144` names only the port; `runemu.sh:335` writes `cheevos_custom_host` for the lowerdeck proxy on 4874 on dual-screen devices (T1's), a second writer of the key, not of this port; RetroArch's `0013-cheevos-offline-proxy-toast.patch:6` names the address too (T3's). RetroArch's
`0012-cheevos-cmd.patch` hands an achievement's title and description to
`system()` as root (T3's #825, PL-032); **with the toggle on those strings
come from this proxy's store**, which is this slice's side of that finding.
The rcheevos copies: RetroArch's in-tree (T3's), the proxy's own
`libraproxy_rchash.so` from `raofflineproxy-rcheevos`, Kodi's
`packages/emulation/rcheevos`, EmulationStation's `external/libcheevos`,
melonDS's and Dolphin's bundled copies -- a table in `02`, no change.

**Already found; do not re-find** (cited, each read at its lines): T2's
PL-013 and PL-022 (`feature/m6-es-launch-path-649`,
`docs/audits/2026_10_23-epic-m6-es-launch-path/`); T3's PL-032, #825
(`feature/m6-emulators-libretro-650`, `docs/audits/2026_10_24-epic-m6-emulators-libretro/`);
T30's PL-009, PL-010, PL-020, PL-021, PL-034, PL-037, PL-039
(`feature/m6-emulators-standalone-677`); T12's PL-10 (`assert` refusals in
`ra-ui-test`, `raofflineproxy-consent-test`,
`raofflineproxy-installed-native-test`; #983), PL-18, PL-19 (#986,
`ra-candidate-games`), its S4 (#971) and S9 (#977, #983) on
`ra-offline-test` and `qa-accounts` (`feature/m6-tooling-vm-harness-659`);
T1's PL-004 and `runemu.sh`'s seam; T17's DEVICEONLYDIRS row; and the
proxy's own epic audit `docs/audits/2026_09_14-epic-offline-retroachievements/`
(#186): PL-13, PL-18, PL-25. **Not found before, and this slice's:** the listener's binding and the unit's hardening, the consent and upload path's endpoint and default, the ctl's embedded SQL, the writers' modes, the username on argv, the bounds that are not enforced. (The branches above are named once here for every citation below: T2 `feature/m6-es-launch-path-649`, T1 `feature/m6-os-launch-control-state-648`, T3 `feature/m6-emulators-libretro-650`, T30 `feature/m6-emulators-standalone-677`, T12 `feature/m6-tooling-vm-harness-659`, T22 `feature/m6-os-system-services-669`, T17 `feature/m6-cloud-setup-content-664`; each audit folder is `docs/audits/<date>-epic-m6-<slice>/` on its branch, read with `git show origin/<branch>:<path>` after no fetch -- the clone the lane is cut from already holds them.)

## 3. Read first

In this order, the working tree's copies (the coordinator's branch, merged
in): `.claude/rules/generic-x64-vm-testing.md` (the consent test at its
§ around line 795, `--ra-offline` around 890, the RA games around 1044,
`ra-ui-test` around 1169, the installed-native test around 1361),
`es-native-ui.md` § The cards at the link's return (the flush stamp taken
within ten seconds), `es-player-text.md` (the RetroAchievements strings and
their whys, around lines 81 and 253), `release-candidates.md` (around 64 and
99: `ra-offline-test` is the proxy's proof; `--only proxy-schema` after a
refresh), `vm-first.md` (line 52: the award proof is separate from the
cloud baseline, D-QA-058), `device-builds.md` (around 533,
`CHEEVOS_DEV_LOGIN`), `bugs-are-agent-first.md` rule 6,
`engineering-practices.md` § Consider contributing every applicable fix
upstream (D-WORKFLOW-164, -165), `upgrade-and-install.md` § Every fix
answers what was already written, `issue-tracking.md` § Ticking.

`docs/decision-register.md`: the 48 `D-RA-*` rows (001 to 048, 015 present as a *never issued* row; **open: D-RA-006**, the spent achievement and a second QA account,
and **D-RA-026**, the sets export in the backup, #219) and the rows that
name the proxy from other areas: D-WORKFLOW-018, -020, -029, -138, -165;
D-INFRA-011; D-UI-053, -054, -056, -077, -079, -092, -095, -096, -101 to
-107, -109, -112, -113, -119; D-QA-015, -016, -035, -036, -037, -048, -049,
-058; D-CLOUD-137; D-LAUNCH-006. `docs/blindspot-register.md` entries 43,
44, 46, 64 and 65 (and 22, 39, 75 as always).

The record of the proxy's own proofs, by folder: the epic audit
`docs/audits/2026_09_14-epic-offline-retroachievements/` (#186);
`docs/qa-logs/2026-10-06-ra-award/` (the last real `ra-offline-test`, 33
PASS); `docs/qa-logs/*ra-ui*`, `*proxy-consent*` (with its retained failed
positive control), `*installed-proxy*` (18 of 18), `*proxy-test-discovery*`
(12 of 12), `*browser-headroom-587*` (26.27 MiB gained; a 15 s SIGKILL on a
busy stop), `2026-10-04-proxy-schema-note/`, and the three UNRUN fixture
folders of 2026-10-13/14 (`library-index-fixture`, `dolphin-proxy-routing-source`,
`proxy-cgroup-source`); `docs/cloud-sync-changelog.md`'s proxy entries;
`docs/upstream/README.md` and the ten drafts under
`docs/upstream/raofflineproxy/` (for 001, 002, 005, 007, 008, 009, 013, 015,
018, 019; every base older than the pin; nothing has been sent).

The issues, read on GitHub at stage A (`gh issue view` is a read): closed
#452, #414, #329, #306, #305, #300, #282, #246, #242, #211; open #587 (the
browser's headroom), #585 (the contribution queue; its proxy rows are the
#585 lines this slice owes), #568, #369, #323, #293, #292, #266, #236,
#224, #214, #212, #173, #168 (the earlier contribution map), #163, #79 --
one line each in `01` with the latest dated mention in the tree.

**The tools, and what each proves** (read whole; none run on the host
except as § 5 says):

| Tool | Proves | Needs | Host without a guest |
| --- | --- | --- | --- |
| `tools/ra-offline-test` (524) | the end-to-end award earned offline reaching the server: launch, link cut on the monitor, the award, `pending=1`, link back, `Flush complete ... flushed=1` and the stamp, the API showing it earned; `--control` proves #162's loss | a QA guest with serial and monitor, **the QA RetroAchievements account** (`~/.ROCKNIX/qa-accounts`, 0600, carried over ssh stdin, D-QA-016), the live API; **spends one cheap achievement per PASS** (D-RA-006) | no |
| `tools/raofflineproxy-integration-test` (247) | the shipped preparation helper against an unpacked patched proxy: the 125-game whole-library pass, retries, rate-limit pacing (#361) | `--source` (a patched tree with `linux/`) and `--predecessor-source`; a temp config dir; synthetic HTTP, no account | **yes** |
| `tools/raofflineproxy-installed-native-test` (70) | upstream's unchanged hashing and format tests against the image's installed modules and the accepted library sha256 (#547) | the image's runtime (`/usr/lib/python*/site-packages/raofflineproxy/`, `libraproxy_rchash.so`) | no: on the guest |
| `tools/raofflineproxy-consent-test` (230) | an unanswered, declined, malformed or stale consent sends nothing; explicit `true` sends once; a restart does not duplicate (#457) | a fresh guest **with no default route**, `--expected-build`, loopback HTTP | no: on a no-NIC boot |
| `tools/ra-ui-test` (225) | the installed reconnect cards against a synthetic award and loopback HTTP, frames EN and FR | a disposable guest | no; **T20's** |
| `tools/ra-candidate-games` (223) | which homebrew sets have cheap achievements; `--check` hashes a ROM RA's way | the live API, `RA_QA_WEBKEY` | yes; retirement proposed (#986) |
| `tools/qa-accounts` (159) | carries the QA account into a guest and clears what the proxy wrote | the account file, a guest port | no |
| `tools/rc-preflight --only proxy-schema` | the ctl's header note names the recipe's pin (`check_proxy_schema`, `:138-164`): a comment check, *"not a schema test"* (#414) | the tree | yes |
| `tools/last-good-scripts-test` | its proxy cases (lines around 1006-1065, 1599-1668, 2147-2315: the marker, the lock, the stamps; `:1893-1898` setsettings' `cheevos_custom_host`) under the image's busybox | the build root's busybox, or the retained donor's | yes, with the donor |

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of four families: **where a credential
travels** (argv, a log, the bundle, the port), **what runs as root on an
unauthenticated port**, **a check whose failure reads as success**, **a
bound that is not enforced**. The leads below are the digests' by shape;
each is read at its lines before it is called anything.

- **Q1 The listener.** Who can reach `127.0.0.1:8080`, and what the port
  answers without identity (the account's game data, unlocks and badges to
  any local process; `X-RA-Store-Only` from whoever sends it, patches 010
  and 012); the service as root with no hardening directive against T22's
  table of the other units; the readiness check and `enable` (`:451-456`)
  accepting a foreign `0.0.0.0:8080` listener (lead: `:932`); the port
  shared with `cloud_oauth`'s serve. What the service's own request
  validation does (`proxy_service.py` in the tarball, not read yet).
- **Q2 The credential's paths.** The username on argv at four sites
  against the file's rule at `:1244-1246`; the `login2` row with the token
  read by `do_account`; the token and password presence-only; the client's
  own logging and its `t=`/`p=` redaction (the tarball); patch 008's bundle
  -- what it carries, to which endpoint (`log_uploader.py`), under
  `upload_logs` being JSON `true` exactly, default off, and the claim that
  the path is unreachable on the sqlite backend today; patch 019's consent
  sentinel; the proxy's query strings carrying `u=<username>` from
  EmulationStation (`RetroAchievements.cpp:301/315/338`, T20's) and from
  the emulators.
- **Q3 The writers.** Every write's mode under the writer's umask, since
  none is set; the three direct writes (`verify-cursor`, `scan.log`, the
  topup mark) against the temp-and-rename rule (D-CLOUD-078); `write_stamp`'s
  ignored status; the lock that fails open at `:492` (`exec 7<>"${SCAN_LOCK}"
  || return 0`: a lock that cannot be opened reads as *nothing running*, and
  `disable` stops the service under a live scan); the fifo named by `mktemp
  -u` (`:1708`); `es_export.py`'s write of `cached_game_ids.txt`, which
  EmulationStation reads uncached.
- **Q4 The bounds.** Which of the constants at `:325-337` and in the
  helpers are enforced and by what: the scan with no deadline of its own
  (`:2062`); the unguarded topup mark (`:2264`) and the `-nt` comparisons
  without a clock (`:2221`, `:2235`); the IDAT inflate without `max_length`
  (patch 013); the lookup threads without a cap (patch 015); the 429
  passed through with no rate-limit marking on the pinned POST path (patch
  001); the 15-minute kill once read as the verdict (blindspot 44) -- does
  the ctl still tell a kill from a result (`:2372-2380`'s `0 0 0` fallback)?
- **Q5 The patches.** Each of the eighteen at the pin: present or absent in
  the tarball, `fix`/`feature`/`identity`, its draft under `docs/upstream/`
  or none, the #585 line it owes in the shape the lane writes (the target,
  the current-source comparison, the minimal patch; D-WORKFLOW-164, never
  sent, D-WORKFLOW-165); the recipe's *"16 patches"* comment against
  eighteen files; 020 and 021 without headers; the sibling recipes' comments
  citing proxy commits older than the pin; the ctl's header note equal to
  the pin (`rc-preflight --only proxy-schema`); what T19 would say to a pin
  refresh (D-WORKFLOW-162: the upstream's commits since `c7ebd1b6e7`, read
  only from the record -- no fetch).
- **Q6 What a failure reads as.** `count_ready` printing `0` for an
  unreadable export (`:888-897`, against `cannot_tell` elsewhere); the
  `tail -n 1` without `pipefail` at `:893`; one non-UTF-8 ROM name failing the whole listing (the strict `write_text` at `:1672-1674`, read as `why LIBRARY_UNREADABLE` at `:1989` and `:2316`); two usage exit codes (`:2452-2453` against `EX_USAGE`); the refresh's `note()` on stdout (`:50-51`) on the protocol's stream; the listing's `:2372-2380` fallback; the page's comment naming `have_account` as if a verb (a function at `:1119`).
- **Q7 The protocol the interface reads.** Every `>>> ` token the three
  producers emit (the sources digest § 4's table) against what
  `CloudText.h:441-451`, `:473`, `:508`, `:560`, `:581` and
  `OfflineAchievementsText.h:105`, `:115`, `:149` parse and what the cards
  say (`es-player-text.md`); every stamp's shape (`last-scan`, `last-flush
  <epoch> <flushed>`, `running`, `index-pending`) on both sides; the exit
  codes the pages act on (0, 1, 2, 130, 143); the player-facing lines the
  ctl's `fail`/`cannot_tell` print; what changes here is T20's to show, so
  the answer is a table T20 inherits, not an edit.
- **Q8 The harness.** For each tool in § 3's table: what it proves, what it
  cannot (the schema note is a comment check; `ra-offline-test`'s loose
  `flushed=` match and its key-to-`--host` are T12's #977/#983), and the
  positive it has been seen to catch; for each lead this slice confirms,
  the constructed positive that fails on `8ebaf8daad`'s bytes (a foreign
  listener on 8080; a lock file made unopenable; an unreadable export; a
  ROM name with undecodable bytes), on the host where the script's shape
  allows and on the guest where it does not.

## 5. The evidence floor

1. **Can this be done on the VM? Yes -- the host first, then one guest
   window granted on #666.** Every read, count and table runs on the host
   at `8ebaf8daad`'s bytes. The proxy's upstream source is read from the download cache's tarball **named by the pin**, `/workspace/cache/rocknix-sources/raofflineproxy/raofflineproxy-c7ebd1b6e777f3751ff0ecdf8aba54045844e00d.tar.gz` (sha256 equal to `PKG_SHA256`; thirteen other revisions sit beside it), unpacked under `/workspace/tmp/m6-t19/`
   with the eighteen patches applied by GNU `patch -p1 --fuzz=0` in the
   recipe's order -- an unpack and a patch, not a build; the result and
   every hunk's exit recorded. `tools/raofflineproxy-integration-test
   --source <that tree>` runs on the host with synthetic HTTP (its
   `--predecessor-source` is `CANNOT` unless a predecessor tree exists
   without a fetch; say which). `bash -n` on the ctl under the host's bash
   5.3 (the image pins 5.3; the donor holds busybox and rclone only, no
   bash) and `python3 -I -m py_compile` on the three helpers under the
   host's python (3.14; the image's is 3.10 -- the guest runs them). **The
   ctl itself never runs on the host**: it reads and writes `system.cfg`
   and `systemctl`. `tools/last-good-scripts-test` runs on the host with
   the retained donor's busybox (`/workspace/artifacts/m6-donor/1a0266484423/image/system`),
   its proxy cases named in the record. The service runs only on the
   guest. **The RetroAchievements server is reached by one tool only,
   `ra-offline-test`, with the QA account** (`~/.ROCKNIX/qa-accounts`,
   never printed, carried over ssh stdin; D-QA-016; never the owner's,
   D-QA-015); it spends one cheap achievement (D-RA-006 is the open
   decision on a second account), which the window's plan says in advance.
   Nothing on a handheld.
2. **The guest window** -- one, asked for on #666 at stage B's end with its
   plan and bound (60 minutes proposed), granted explicitly in the shared
   log's queue, two boots of the M6 copy of the image
   (`/workspace/artifacts/m6-t2-20261023/`, `069fc2704421`), the post
   contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's
   first line with the census, the stop by pidfile at bound plus grace, the
   disk retired after with path, size and sha (D-INFRA-022):
   - *boot 1, with a NIC on user-mode networking:* the identity (`BUILD_ID`,
     the distribution commit, the installed `package.mk`'s pin); the four
     scripts, the unit and the daemon file hashed against the tree; the
     module's installed `.pyc` set listed against the tarball's modules;
     `systemctl show raofflineproxy -p User -p ProtectSystem -p
     NoNewPrivileges -p CapabilityBoundingSet -p UMask`, the listener's user
     from `ps`, `ss -ltnp` for 8080; a scan over a seeded small library
     (the QA account carried in, the toggle on) with every stamp's mode read
     back as written; **four constructed positives** -- a foreign listener
     on `0.0.0.0:8080` with the service stopped and `ctl listening`'s
     answer; the scan lock made unopenable and `disable`'s behaviour under
     a running scan; the ready export made unreadable and `ready`'s
     printed count; a ROM name with undecodable bytes and the listing's
     `why` -- each recorded as it falls, never as a conclusion typed;
     `tools/raofflineproxy-installed-native-test` with the accepted library
     sha256 from the record (expect 18 of 18); then, **if the bound still
     allows after those**, `tools/ra-offline-test` with the QA account
     (the award proof; its 2026-10-06 run, 33 PASS, is cited otherwise and
     the step recorded `CANNOT in this window`);
   - *boot 2, no NIC:* `tools/raofflineproxy-consent-test --expected-build
     <BUILD_ID>`, its output kept.
   The window's record is `02` § The guest cycle; the host file carries the
   mirrors; the lane never names an M7 root.
3. **What T20 inherits** is written, not tested here: the protocol table (Q7), the page comment's `have_account` wording, the stamps' shapes, the strings. (`069fc2704421` names the image file's build, not a git object in this repository; the guest reads its `BUILD_ID` and the M6 copy's `.sha256` is checked first.)
4. **A fix lands only under a stream brief** at the stage-D pause, in the
   fork's files or on a patch's `+` side; a stream that changes the ctl
   runs `tools/last-good-scripts-test` before its commit; a fixture
   rewrites no path.

**The runs** (every one in `02` § The runs with exit, wall time, the figure
and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its
reason). From the worktree, after the membership block; `P` is the proxy's
package directory at `8ebaf8daad`; counts by `/usr/bin/grep` (never the
shell's function, #1138):

```bash
export LC_ALL=C; C=8ebaf8daad; P=projects/ROCKNIX/packages/network/raofflineproxy; G=/usr/bin/grep
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t19/tmp; mkdir -p "$TMPDIR"; df -i /workspace | tail -n 1
# the membership's bytes at the read commit (expect 27 paths, 5369 lines; the per-file lines equal to the block's)
tr '\n' '\0' < .qa-scratch/t19/paths.txt | xargs -0 -I{} sh -c 'printf "%6d %s\n" "$(git show '"$C"':{} | wc -l)" "{}"' | awk '{s+=$1} END{print NR" paths "s" lines"}'
# the ctl's shape (expect: no set lines; no pipefail; 55 functions; the five EX_ constants at 316-320; exit 1 at 378,1991,2413,2425; exit 2 at 560,565,639,2453; exit 3 at 762,1843; 130 at 1821; 143 at 1797; 0 at 2016,2227,2237,2430)
git show $C:$P/sources/raofflineproxy-ctl | $G -n -E '^\s*set -' | wc -l; git show $C:$P/sources/raofflineproxy-ctl | $G -c pipefail; git show $C:$P/sources/raofflineproxy-ctl | $G -c -E '^[a-z_]+\(\)'; git show $C:$P/sources/raofflineproxy-ctl | $G -n -E '^EX_[A-Z]+=' ; git show $C:$P/sources/raofflineproxy-ctl | $G -n -o -E '\bexit [0-9]+'
# the unit (expect ExecStart :33, ExecStartPost :40, ConditionPathExists :7; hardening directives 0)
git show $C:$P/system.d/raofflineproxy.service | $G -n -E '^(ExecStart|ExecStartPost|ConditionPathExists|Restart|RestartSec|TimeoutStopSec|User|Group)='; git show $C:$P/system.d/raofflineproxy.service | $G -c -E '^(Protect|Private|NoNewPrivileges|CapabilityBoundingSet|Memory|CPU|Tasks|DynamicUser|IPAddress|RestrictAddressFamilies|SystemCallFilter|ReadWritePaths|ReadOnlyPaths|UMask)'
# the port, everywhere outside the package (expect setsettings.sh:538, cheevos_ppsspp.sh:97, cheevos_dolphin.sh:142 and RetroArch's 0013-cheevos-offline-proxy-toast.patch:6 for the address; cloud_oauth names 8080 at 857, 2333, 2553, 2681)
git grep -n -E '127\.0\.0\.1:8080' $C -- packages projects ":!$P" | sed "s/^$C://" | cut -c1-120; git grep -n -E '\b8080\b' $C -- projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth | sed "s/^$C://" | cut -c1-100
# the credential's keys and sites (expect the three keys at 311-313; argv sites 616, 647, 764, 1029; the env site 1265; no umask/chmod/chown)
git show $C:$P/sources/raofflineproxy-ctl | $G -n -E 'USER_KEY|TOKEN_KEY|PASSWORD_KEY|RA_SCAN_USER' | $G -v -E '^[0-9]+:\s*#' | cut -c1-110; git show $C:$P/sources/raofflineproxy-ctl | $G -c -E 'umask|chmod|chown'
# the stamps' writers (expect write_stamp :1094 with mv -f; mark_running :828-829; index-pending :2154-2155; the topup touch :2264; the flush stamp's rename :812-814)
git show $C:$P/sources/raofflineproxy-ctl | $G -n -E 'mv -f|touch |> *"\$\{?(SCAN_STAMP|RUNNING|INDEX_PENDING|TOPUP_MARK|FLUSH_STAMP)' | cut -c1-120
# the helpers' writes (expect verify-cursor a direct write_text :169-177; absent via .tmp + os.replace :195-203; refresh's note to stdout :50-51)
for f in raofflineproxy-cache-images raofflineproxy-refresh raofflineproxy-cache-indexed; do echo "== $f"; git show $C:$P/sources/$f | $G -n -E 'write_text|os\.replace|rename\(|sys\.stdout|print\(' | cut -c1-110 | head -n 12; done
# the protocol tokens per producer: the ctl emits through say() with literals such as say "why TOGGLE_OFF" (:836), the helpers through tell()/f">>> {text}", so the token is counted without its >>> prefix (expect non-zero for all four, the ctl's the largest; the list, not the count, is the table in 02: TOGGLE_OFF, NO_ACCOUNT, CANCELLED, NO_NETWORK, LIBRARY_UNREADABLE, NO_GAMES, NOTHING_NEW, LIMIT_REACHED, TRUNCATED in the ctl; STORE_UNREADABLE, NO_ACCOUNT, NOTHING_DUE, LEFT, REPEATED_FAILURES in the refresh; STORE_UNREADABLE, NO_ACCOUNT, VERIFY_COMPLETE... in cache-images)
for f in raofflineproxy-ctl raofflineproxy-refresh raofflineproxy-cache-images raofflineproxy-cache-indexed; do printf '%s: ' "$f"; git show $C:$P/sources/$f | $G -o -E '"(why|note|doing|done|total|game|cached|refresh|verified|errors) [A-Z_]{2,}' | sort -u | wc -l; done
# the deletions (expect one rm -rf in the ctl at 1141 and two in package.mk at 120,123; no find -delete)
git show $C:$P/sources/raofflineproxy-ctl | $G -n -E 'rm -rf|find .*-delete|(^|[^a-z])(: *>)' | cut -c1-100; git show $C:$P/package.mk | $G -n -E 'rm -rf|rm -f' | cut -c1-100
# the patches (expect 18 files; the recipe's comment "16 patches" at line 6; the two sibling pins; the ctl's header note equal to the recipe's pin)
git ls-tree -r --name-only $C -- $P/patches | wc -l; git show $C:$P/package.mk | $G -n -i 'patches' | head -n 3 | cut -c1-120; git show $C:$P/package.mk | $G -n -E '^PKG_(VERSION|SHA256)='; for s in rcheevos libchdr; do git show $C:projects/ROCKNIX/packages/network/raofflineproxy-$s/package.mk | $G -n -E '^PKG_VERSION='; done; git show $C:$P/sources/raofflineproxy-ctl | $G -n -E '^# package\.mk pins' | cut -c1-100
tools/rc-preflight --only proxy-schema --tree "$D" 2>&1 | tail -n 2
# the tarball, NAMED BY THE PIN (the directory holds fourteen; the first by name is a 2026-09-25 tree) (expect the file; its sha256 equal to PKG_SHA256's first 16 hex; every patch's first + line absent from the unpacked pin)
PIN=$(git show $C:$P/package.mk | sed -n -E 's/^PKG_VERSION="([0-9a-f]{40})".*/\1/p'); T=/workspace/cache/rocknix-sources/raofflineproxy/raofflineproxy-$PIN.tar.gz; ls /workspace/cache/rocknix-sources/raofflineproxy/ | wc -l; [ -f "$T" ] && sha256sum "$T" | cut -c1-16 || echo "CANNOT: $T absent"; git show $C:$P/package.mk | sed -n -E 's/^PKG_SHA256="([0-9a-f]{16}).*/\1/p'
# the neighbours (expect 5 OS files by word outside the three packages: cheevos_ppsspp.sh, 001-functions, backuptool, setsettings.sh, packages/virtual/network/package.mk; ES 11 files at the pin, OfflineAchievements.cpp 9, GuiRetroAchievementsSettings.cpp 8)
git grep -c -w raofflineproxy $C -- packages projects ":!$P" ":!projects/ROCKNIX/packages/network/raofflineproxy-rcheevos" ":!projects/ROCKNIX/packages/network/raofflineproxy-libchdr" | sed "s/^$C://"; git -C /home/max/Development/emulationstation-next.worktrees/qa-integration grep -c -w raofflineproxy 16dbac5211 -- es-app/src es-core/src | sed 's/^16dbac5211://' | sort -t: -k2 -n -r | head -n 11
# the page comment's have_account (expect the comment at GuiRetroAchievementsSettings.cpp:154; the ctl's function at :1119 called at :1170; 0 in the dispatch's case list 2434-2450)
git -C /home/max/Development/emulationstation-next.worktrees/qa-integration grep -n have_account 16dbac5211 -- es-app/src | sed 's/^16dbac5211://' | cut -c1-100; git show $C:$P/sources/raofflineproxy-ctl | $G -n 'have_account' | cut -c1-80; git show $C:$P/sources/raofflineproxy-ctl | sed -n '2434,2450p' | $G -c 'have_account'
# the tools' readiness on the host (expect --help exit 0 for the two python tools; the suite's proxy cases counted; qa-accounts refusing without a port)
for t in raofflineproxy-integration-test raofflineproxy-installed-native-test raofflineproxy-consent-test; do printf '%s: ' "$t"; tools/$t --help >/dev/null 2>&1; echo "rc=$?"; done; $G -c -w raofflineproxy tools/last-good-scripts-test; tools/qa-accounts 2>&1 | head -n 2 | cut -c1-100
# the syntax under the host's interpreters (expect bash -n 0; py_compile 0 x3; the versions recorded)
bash --version | head -n 1; git show $C:$P/sources/raofflineproxy-ctl > "$TMPDIR/ctl"; bash -n "$TMPDIR/ctl"; echo "bash -n rc=$?"; python3 --version; for f in raofflineproxy-refresh raofflineproxy-cache-images raofflineproxy-cache-indexed; do git show $C:$P/sources/$f > "$TMPDIR/$f"; python3 -I -m py_compile "$TMPDIR/$f"; echo "$f py_compile rc=$?"; done
# the removal check from the dispatch tip -- <dispatch tip> is the lane tip the dispatch comment on #666 names; the lane substitutes it (expect empty: nothing under packages/ projects/ tools/ changed at stages A to D)
git diff --stat <dispatch tip> HEAD -- packages projects tools | tail -n 1
```

## 6. Outputs

As T17's brief § 6, with the folder `docs/audits/<yyyy_mm_dd>-epic-m6-offline-achievements/`:
`00` to `05`, `second-opinions/` (both seats' plans, the manifest with its
three-way scan and every scan hit's disposition, each probe and refutation
with provenance), `guest-cycle/` (the window's record: the image's
identity, the installed-versus-tree hashes of the nine fork-own files and
the applied upstream sources, each proof's dump, the leftover check), the
lint before D, the audit issue (`Audit: M6 T19 the offline achievements
proxy -- N findings (...)`, a sub-issue of #666), the bugs, and the retro at
`docs/retros/<date>-m6-offline-achievements.md` (**what the slice did to
the two time-to-play numbers**: the proxy sits on the launch path twice -- `setsettings.sh:540`'s port probe before RetroArch starts, and the cards at exit over the flush and the top-up (`ProxyCards`, T2's) -- so the answer names those two with their bounds and cites `docs/vm-qa-log.md`'s last numbers, never "nothing" by default; **what T20 inherits**: the stamps and strings the pages read,
the ctl subcommands they run, the consent setting's name). **`02` carries
§ Coverage (27), § The listener (bind, port, authentication, the unit's
hardening line by line, who can reach the port), § The credential's paths
(one row per credential kind -- the account's password, its web API key,
the session token, the per-emulator token files -- per sink it can reach:
file, log, stderr, state, packet, screen, the upload -- with the mask at
that sink or `none`), § The writers (one generated row per statement that
writes under `/storage/.config/raofflineproxy/`, `/storage/.cache/`,
`/var/run/` or `/tmp/`: file:line, the file, the mode, temp-and-rename or
in place), § The patches (one row per patch: what it changes, the
upstream state, `fix`/`feature`/`identity`, the #585 line it owes), § The
bounds (every timeout, size, count and pacing in the refresh and cache
scripts, with the line that enforces it or `none`), § The runs (every § 5
command), § The guest cycle, § Positives, and every proof with
`proved:`.** The stage-D pause as T17's: the punch list posted on #666,
the lane waits for the coordinator's dispositions and any stream brief.

## 7. Acceptance

The checklist on #666 becomes this section at dispatch, written there by
the coordinator in place of P1's generated ones. Every checkbox names the
artifact that ticks it (D-QA-044); the coordinator ticks at acceptance,
from the artifacts, never from the hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-offline-achievements/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-offline-achievements/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts (does not certify resolution)`).
- [ ] `second-opinions/review-plan.json` records `depth: extended` and two reviewers (`gpt`, `openai/gpt-6-astra`, `max`; `gemini-argon`, `google/gemini-4-argon`, `high`); each seat's probe and refutation have a `.provenance.json` beside them whose served model is the seat's, whose verification is PASS and whose `facilitator_version` is named (read directly, as T17's); `packet-manifest.json` carries the three-way scan with every hit dispositioned by name; the running log shows exactly four keyed invokes.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a `bug`, a Backlog the coordinator files, #585, #168, T20's #667 by number, an M7 issue by number), or recorded as written with its reason; `tools/box-check --issue <audit issue>` prints 0 fail.
- [ ] `reviewed-at:` and `fixed-at:` in the checklist's header carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the 27 (``tr '\n' '\0' < .qa-scratch/t19/paths.txt | xargs -0 git diff --stat 8ebaf8daad <reviewed-at> --`` empty) and nothing under `packages/`, `projects/` or `tools/` changed at stages A to D (`git diff --stat <dispatch tip> <stage-D tip> -- packages projects tools` empty).
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (27 paths, 5,369 lines; fork-own 9, vendor-carried 18; shipped 27; patch-and-config rows 18, 1,703 lines -- or the deltas beside them) and the per-file line table at `8ebaf8daad`.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | /usr/bin/grep -c -E '^\| `'`` prints `27`.
- [ ] `02-forward-audit.md` § The listener states the bind and port with their lines, who can reach the port and what it answers without identity, the unit's hardening directive by directive against T22's table of the other units, the readiness check's accepted forms, and the user the service runs as read from the guest (`systemctl show`, `ps`).
- [ ] `02-forward-audit.md` § The credential's paths has one row per credential kind (the account's password, its web API key, the session token in the `login2` row, the username, the per-emulator token files) per sink it can reach (argv and `/proc/<pid>/cmdline`, the journal, `scan.log`, stderr, the upload bundle, the port's query strings, the packet, the screen), with the mask at that sink or `none`, each at its line.
- [ ] `02-forward-audit.md` § The writers is generated by a script under the audit folder's `tools/` from `grep -n` over the four scripts and the unit at `8ebaf8daad` (the generator asserts its row count and exits 1 on drift), one row per writing statement: the file, the mode it ends with (none set: the writer's umask, read on the guest), temp-and-rename or direct, the lock held, the reader.
- [ ] `02-forward-audit.md` § The patches has eighteen rows (number, title, upstream file and function, `fix`/`feature`/`identity`, present or absent in the tarball at the pin, the draft under `docs/upstream/` or none, the #585 line owed) and states the tarball's sha256 against `PKG_SHA256`, the recipe's *"16 patches"* comment against the count, and the ctl's header note against the pin (`rc-preflight --only proxy-schema`'s line).
- [ ] `02-forward-audit.md` § The bounds has one row per constant and timeout in the four scripts and the unit, with the line that enforces it or `none`, and names the scan's missing deadline, the unguarded topup mark, the `-nt` comparisons, the IDAT inflate and the lookup threads as enforced or not.
- [ ] `02-forward-audit.md` § The runs records every § 5 command with exit, wall time, the figure and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass; the patched-source unpack records every hunk's exit at fuzz 0; `tools/raofflineproxy-integration-test`'s result or its `CANNOT` is one of them; the ctl is shown never to have run on the host.
- [ ] `02-forward-audit.md` § The guest cycle records the window the coordinator granted on #666 (the comment's time; the START and RETURN posts with their first-line contract and censuses), the image by file name and BUILD_ID read from the guest, the installed-versus-tree hashes of the four scripts, the unit and the daemon file, the module's installed set against the tarball's, the listener's user and bind as read, every stamp's mode as written, the four constructed positives each with what fell, `raofflineproxy-installed-native-test`'s count, `raofflineproxy-consent-test`'s output from the no-NIC boot, and `ra-offline-test`'s result with the QA account or its `CANNOT in this window` with the record's 2026-10-06 run cited; the disk retired with path, size and sha; the leftover check.
- [ ] `00-running-log.md` shows no build, no compiler, no plan generation, no fetch (the council runtime from `npm install --offline`; the upstream source from the cache's tarball), no handheld, the owner's RetroAchievements account never named or used, no hosted account but the QA one, no M7 root or worktree, guests only inside the granted window, the proxy never started on the host, four keyed invokes and every other council call keyless (`grep -c` lines for each in `00`'s own closing census).
- [ ] `04-analysis.md` § Q1 to Q8 are answered at their lines; § Q3/Q6-class bugs state each decision with its trace, its `Already written:` line and its VM line, in the four families; every `bug` passes `tools/box-check --issue N`; every #585 line owed is written in `02` § The patches in the shape the lane writes.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fixture`, `guest` or `design`; every punch item carries `question:`; `02` § What T20 inherits lists the protocol table, the page comment's `have_account` wording, the stamps' shapes and the strings with their lines on both sides.
- [ ] The retro exists at `docs/retros/<date>-m6-offline-achievements.md`, is posted on #666, says what the slice did to the two time-to-play numbers (the port probe at launch and the cards at exit named with their bounds; cited from `docs/vm-qa-log.md`), and what T20 inherits.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); the stage-D pause; an explicit maintainer pause on
#666; a blocker named on #666 (a seat that fails its provenance gate
twice, a packet scan hit that is a value, two commands that disagree, a
block whose output differs from § 2's beyond the deltas it records); a
branch that differs from `8ebaf8daad` on one of the 27 at stage A; or an
execution limit, stated as such with the running log current. A checkpoint
is not a stop. An idle session says it is idle on #666, **and does not end
a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#666`, its time from `date -u` in
  the same command, prose through a quoted heredoc; `tools/work-log-index
  --write` after it.
- A friction line the moment something slows, with `issue: #666` or the
  guard.
- The VM question written before any proof (§ 5: yes, the host first, then
  one guest window granted on #666; nothing on a person's device or
  account, and never the owner's RetroAchievements account).
- The mini-retro at stage G, posted on #666, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator; its scoped
  audit runs check 7's step 5 where a fix landed.
- A register row the same session for any decision the slice forces (none expected); D-WORKFLOW-209 is the highest Decided row on the coordinator's branch and D-CLOUD-185 the highest cloud row (D-WORKFLOW-188 on the P1 branch only; the merge unites them); a row this slice forces takes an ID the coordinator assigns on #666.
- `tools/ceremony-check --gate` before every push; never `--no-verify`; a
  merge with conflicts is checked for markers; the ledgers united by whole
  entries; **a commit names its paths**; anything temporary under
  `/workspace/tmp/m6-t19/` after `df -i`, never `/tmp`; the window's
  record kept on the branch, the guest disk retired after it with the
  retirement recorded in `00` (D-INFRA-022); **`rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command, never
  inside a `bash -c` script**; **a stream that changes a script
  `tools/last-good-scripts-test` covers runs the suite before its commit**,
  and a fixture rewrites no path -- the real script in a bubblewrap sandbox
  started with `--clearenv` (plan § 6b's stream practice).
- Commit messages `docs: ...`, with `Refs #666`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#666's checkboxes against their artifacts; the lint's `PASS` line;
`review-plan.json` and the four provenance files (read directly) and the
manifest's scans; the audit issue's checkboxes all at an outcome; the
coverage table's row count (27), § The listener's and § The credential's
paths' rows, § The patches' 18 rows, § The writers' generated count;
every Q bug with its three lines; **re-running on a clone of the branch
at the tip under `/workspace/tmp/m6-coordinator/`: the membership block
and every § 5 run in full** (no guest: the window's record is read, not
repeated); `register-check` on a simulated merge with the coordinator's
tip; the retro's answers; the five checkers' exit codes. The lane posts
one hand-back comment naming the tip and each artifact by path, writes
`reviewed-at:` and `fixed-at:` into #666's body, then says it is idle.
After acceptance the coordinator closes the audit issue, prompts the lane
for `audit-completion.json` and the lint against **the audit issue**
(`--issue <audit issue>`, never the slice's), merges the branch in its
turn after the M7 candidate, regenerates the ledgers, posts the #585 lines
in the shape the lane wrote, and closes #666 when every row is proven; the
area epic closes when T19 and T20 have.

**The readings before dispatch** (plan § 3, principle 3): the area epic's
futro, written with this version, carries a T19 kickoff addendum, and a
stranger's proof of this brief is run by a reader with no context before
dispatch; version 2 records what each found.

**What never runs in this slice:** a build, a compiler, a plan generation,
a fetch (the council runtime from `npm install --offline`; the upstream
proxy read from the download cache's tarball if present, never cloned), a
handheld, the owner's RetroAchievements account or any hosted account
(the RetroAchievements server is reached only by the harness the record
names with a QA account, if one exists -- § 5 says), the proxy started on
the host (it runs only on the guest), a guest before a grant on #666, M7's
roots or worktrees, a change outside the 27 files and the audit folder
except under a stream brief.

## Version 2: what the stranger's proof found (2026-10-26)

Ten commands from the scratch clone at `2174265e9c`. The membership block
reproduced exactly; every per-file line count, every ctl line number the
brief states, the unit's lines and its zero hardening directives, the
recipe's pin, sha and comments, the patches' provenance, the
EmulationStation counts and lines, the tools' behaviour, every decision
ID, blindspot, branch, audit folder and punch item held. The corrections:

1. **The runs block's tarball line picked the wrong file.** `ls | head -n 1`
   over fourteen cached tarballs returns a 2026-09-25 revision; the pin's
   is `raofflineproxy-c7ebd1b6e777f3751ff0ecdf8aba54045844e00d.tar.gz` (sha
   `88eef31a...` = `PKG_SHA256`). R12 and § 5's unpack now name it by
   `PKG_VERSION`; a lane following version 1 would have patched the wrong
   tree.
2. The five OS files that name the proxy by word are `cheevos_ppsspp.sh`,
   `001-functions`, `backuptool`, `setsettings.sh` and
   `packages/virtual/network/package.mk:13`; `cheevos_dolphin.sh` names
   only the port.
3. `have_account` is the ctl's internal function (`:1119`, called `:1170`);
   the page's `:154` is a comment naming it. No verb is missing; the drift
   is a comment's wording, T20's.
4. R8's `>>> (why|...)` regex matched nothing in three of four producers:
   the ctl emits through `say()` with `"why TOGGLE_OFF"` literals and the
   refresh prints `f">>> {text}"`; the token is now counted without its
   prefix.
5. D-WORKFLOW-209 is the highest Decided row on the coordinator's branch;
   D-CLOUD-185 the highest cloud row.
6. 48 `D-RA` rows (001 to 048), 015 present as *never issued*, not fifty.
7. `runemu.sh`'s `ra_lifecycle_*` and `exec 199>&-` are T1's stream
   insertions on its branch, absent from `8ebaf8daad`, whose line 335
   writes `cheevos_custom_host` for the lowerdeck proxy on 4874.
8. RetroArch's `0013-cheevos-offline-proxy-toast.patch:6` names the
   address; `cloud_oauth` names 8080 at 857, 2333, 2553 and 2681.
9. The ctl's exits: 2 also at `:560` and `:639`; 3 at `:762` and `:1843`.
10. `systemctl` 6, `set_setting` 8 and *six* python blocks are counts of
    non-comment code lines (9, 9 and 7 by word); the rule is stated.
11. The membership block's inputs are on the P1 branch only; the brief says
    so and names the stacked worktree.
12. `<dispatch tip>` is named as the hash the dispatch comment gives; two
    bare `grep`s are `/usr/bin/grep`.
13. Minor: RATOKENSETTINGS starts at `:705`; `:1672-1674` is the listing's
    `write_text` and the why is at `:1989`/`:2316`; the audit folders are
    cited with their branches once in § 2.

What a stranger could not do from version 1 alone, now said: the digests
are the coordinator's scratch files (every figure is reproduced by a
command here); the membership block needs the stacked worktree; "T17's
brief" and "T22's table" are named files; `069fc2704421` is the image
file's build name, not a git object; the GitHub issue list is read at
stage A, not from the tree; the draft-to-patch mapping is the lane's
table, not a grep.

## Errata at acceptance (2026-10-26)

Gathered from the lane's posts on #666 from stage A to the hand-back, each at the stage it was found; the sections above are unchanged.

- Stage A (lane, 12:25): R8 expects non-zero tokens for all four producers; `raofflineproxy-cache-indexed` prints `OK`/`FAIL`/`DONE` lines to the ctl (`:162-216`), not `>>> ` lines -- 0 is right; the ctl 9, the refresh 5, cache-images 8.
- Stage A: R2's `exit` grep also catches eleven `exit` words in the ctl's header comments (28 to 255, and 2120).
- Stage A: the tarball directory's 42 entries are 14 tarballs with their `.sha256` and `.url` files.
- Stage A: the ctl's protocol function is `tell()` (`:835-837`, 20 sites); `say()` (`:371-373`) is `logger`, syslog only -- the brief's § 5 comment names `say()` where it means `tell()` (found by T20's research).
- Stage A: `raofflineproxy-integration-test`'s `--predecessor-source` is the previous shipped pin `879b158995` (the recipe at `7afa9efcfc`), also in the cache; 12 tests OK on the host.
- Stage A: § 7's "the ctl is shown never to have run on the host" reads "never outside `tools/last-good-scripts-test`'s bubblewrap sandbox" -- the suite's groups p and t run the real ctl with `systemctl` and `logger` shimmed and the client's network verbs answered from `/run` (the coordinator's wording, 12:3x).
- Stage B (lane, 12:38): `list_jobs` writes the store through the client's `Storage()` (WAL and `CREATE IF NOT EXISTS`), so the brief's "never written by the ctl" holds only for the ctl's own `mode=ro` connects.
- Stage B: `scanWhy` (`CloudText`, T20's table) carries a `NO_GAMES_FOUND` row no producer emits -- routed to #667 at its dispatch.
- Stage B: § The writers generated by `tools/t19-writers.py` at 77 rows (the brief's own count of writing statements was lower); its drift control at `87d9969bbb` exits 1 with 49 rows, a proven positive.
- Stage B: the refresh's `done a|b` means *failed* at `:227` and *left* at `:170` and `:223` (two meanings for one token shape).
- The window granted 12:4x: 60 min + 10 grace, two boots, the award proof last with the QA account (D-RA-006's spend accepted for this proof).
- The suite ruling (14:33): `tools/last-good-scripts-test` changes in S1's and S3's commits (D-WORKFLOW-210); the acceptance expects it as the only `tools/` path; the brief's § 5 named the suite as a before/after oracle for the ctl without saying it asserted the defects.
- Stage E (lane, 15:14): F-42 / #1166 -- `pending_lock`'s `exec 6<>"${PENDING_LOCK}" 2>/dev/null` redirected the ctl's stderr to `/dev/null` for the rest of a run (a bare `exec` with a redirect is a redirect of the shell); folded into S5. The brief's four families did not anticipate a shell-redirect class.
- Stage E (lane, 15:49 and 16:08): the suite's fixtures also leaned on the defects (an absent image helper read as clean, S7; the old job protocol in its stand-in, S9) -- completed in the streams' commits (D-WORKFLOW-211); the #188 check belongs to that completion, not to the reversed checks.
- Stage G (lane, 16:41): with 022 as first landed, a device that updates and plays offline before an online launch has no recorded hash and its offline login is refused -- RetroArch holds the token only in memory and signs in with the password each start; S1b under D-RA-051 keeps the old answer until the first online login records a hash. The brief's § 4 Q3 and D-RA-050 assumed the token suffices.
- Stage G: the image's busybox has no `grep` or `sort`; the host cannot hash a ROM (no native module), so a network-failure fixture uses an index job.
- After acceptance (M7, relayed by the owner at 18:4x): the window's `raofflineproxy-installed-native-test` result -- 18 run, 4 failed against the image's client -- was the absence of four upstream fixtures in M6's run, not a client defect: M7 reproduced the four failures exactly by omitting them and, with all four exact-pin `.7z` fixtures installed, the client passes 18 of 18 plus CHD. The lane's `02` § The guest cycle row stands as what was observed; its reading as a client failure does not. The stale-lock observation (`disable` exit 75 on the image's ctl) remains separate.
