# Research notes: M6.P2 T19, the offline achievements proxy (#666)

## Scope

The brief's § 2 block, run from the lane's worktree (stacked on the P1 branch at `2174265e9c`) at 12:10 UTC on 2026-10-26:

```
selects 2 paths 27 lines 5369 {'shipped': 27} {'fork-own': 9, 'vendor-carried': 18}
{'recipe': 3, 'none': 1, 'python': 3, 'shell': 1, 'systemd': 1, 'patch': 18} {'offline-achievements': 9, 'patches-and-configs': 18}
patch-and-config rows 18 1703
```

**Against the brief:** every figure equal: 27 paths, 5,369 lines, fork-own 9, vendor-carried 18, shipped 27, the languages and areas as stated, patch-and-config rows 18 / 1,703. The nine fork-own files hold 3,666 lines.

### The 27 at `8ebaf8daad` (R1: `git show 8ebaf8daad:<path> | wc -l`; total 27 paths, 5,369 lines, equal to the inventory's per row)

| Lines | Path |
| ---: | --- |
| 24 | `projects/ROCKNIX/packages/network/raofflineproxy-libchdr/package.mk` |
| 23 | `projects/ROCKNIX/packages/network/raofflineproxy-rcheevos/package.mk` |
| 10 | `projects/ROCKNIX/packages/network/raofflineproxy/daemons/006-raofflineproxy` |
| 157 | `projects/ROCKNIX/packages/network/raofflineproxy/package.mk` |
| 64 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/001-dorequest-4xx-passthrough.patch` |
| 61 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/002-no-synthetic-casual-only-achievement.patch` |
| 80 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/003-flush-stamp.patch` |
| 79 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/004-no-cap-on-cached-games.patch` |
| 156 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/005-keep-the-refresh-thread-alive.patch` |
| 82 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/007-cached-sign-in-of-the-configured-account.patch` |
| 144 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/008-log-upload-opt-in.patch` |
| 36 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/009-unique-image-temp-names.patch` |
| 39 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/010-store-only-header.patch` |
| 125 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/011-offline-login-header.patch` |
| 144 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/012-offline-image-miss.patch` |
| 151 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/013-validate-a-cached-image-before-publishing-it.patch` |
| 285 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/015-bounded-name-lookup.patch` |
| 66 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/016-say-what-became-of-a-download.patch` |
| 58 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/018-pixelelated-platform-identity.patch` |
| 81 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/019-consent-cache-initial-observation.patch` |
| 22 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/020-rvz-padding-preserve-partial-word.patch` |
| 30 | `projects/ROCKNIX/packages/network/raofflineproxy/patches/021-flush-reconnect-during-startup.patch` |
| 497 | `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images` |
| 222 | `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed` |
| 2455 | `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl` |
| 232 | `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-refresh` |
| 46 | `projects/ROCKNIX/packages/network/raofflineproxy/system.d/raofflineproxy.service` |

## The runs at stage A, against the brief

The § 5 block is run by `tools/t19-runs.sh 7de4ece06d`, and its output is in `stage-a/runs.txt`.

**Equal to the brief:**
- **R1:** 27 paths, 5,369 lines.
- **R2, the ctl's shape:**
  - no `set -` line, no `pipefail`, 55 functions;
  - the five `EX_` constants at 316-320;
  - the code exits as the brief lists them (1 at 378, 1991, 2413, 2425; 2 at 560, 565, 639, 2453; 3 at 762, 1843; 130 at 1821; 143 at 1797; 0 at 2016, 2227, 2237, 2430).
- **R3, the unit:** `ConditionPathExists` :7, `ExecStart` :33, `ExecStartPost` :40, `Restart` :41, `RestartSec` :42, `TimeoutStopSec` :43; no `User=`/`Group=`; hardening directives 0.
- **R4, the port:**
  - the address at `setsettings.sh:538` (and its log line :540), `cheevos_ppsspp.sh:97` (and its comment :66), `cheevos_dolphin.sh:142`, and RetroArch's `0013-cheevos-offline-proxy-toast.patch:6`;
  - `cloud_oauth` names 8080 at 857, 2333, 2553, 2681, and :2553 carries the address in a comment.
- **R5, the credential:**
  - the three keys at 311-313;
  - the username's argv sites: 616 and 1029 by `$(setting "${USER_KEY}")` on the argv directly; 647 and 764 by `"${USER}"` after its assignment at 645 and 759;
  - the environment site at 1265 (and its reader at 1280);
  - `umask|chmod|chown` 0.
- **R6, the stamps:**
  - the marker `touch` :450, the flush stamp's rename :812, `mark_running` :828-829, the log's rotation :844, `write_stamp` :1094, the cursor :1112, `index-pending` :2154-2155 and its acknowledgement :2172/:2176;
  - the topup `touch` :2264.
- **R7, the helpers' writes:** `verify-cursor` a direct `write_text` at cache-images :173; `absent` by `.tmp` + `os.replace` :200-201; the refresh's `note()` to stdout :51.
- **R9, the deletions:** `: > "$1"` at ctl :977; `rm -rf "${SCRATCH}"` at :1141; the recipe's `rm -rf` at :120, :123 and `rm -f` at :124.
- **R10, the patches:** 18 files; the comment at `package.mk:6` reads *"The16 patches apply at fuzz0 after"* (no spaces, in the tree's own bytes); the pins and sha as stated; the ctl's header note at :242.
- **R11:** `PASS proxy schema note review note matches c7ebd1b6e7...`.
- **R12, the tarball:** sha256 prefix `88eef31acfa4104b` equal to `PKG_SHA256`'s. The directory's 42 entries are 14 tarballs, 14 `.sha256` and 14 `.url` files: fourteen, as stated.
- **R13, the neighbours:**
  - 5 OS files by word (`cheevos_ppsspp.sh` 3, `001-functions` 1, `backuptool` 1, `setsettings.sh` 2, `packages/virtual/network/package.mk` 1);
  - 11 ES files, `OfflineAchievements.cpp` 9 and `GuiRetroAchievementsSettings.cpp` 8, with `OfflineAchievements.h` the most at 10.
- **R14:** the comment at `GuiRetroAchievementsSettings.cpp:154`; the function at ctl :1119, called at :1170; 0 in 2434-2450.
- **R15:**
  - the three python tools' `--help` rc 0;
  - `tools/last-good-scripts-test` names `raofflineproxy` 187 times;
  - `qa-accounts` refuses without a guest port (*"<ssh-port> must be a QA guest's (10022-10029)"*).
- **R16:** bash 5.3.9, `bash -n` rc 0; python 3.14.4, `py_compile` rc 0 for all three helpers.
- **R17:** `git diff --stat 7de4ece06d HEAD -- packages projects tools` empty.

**The deltas:**
1. **R8: `raofflineproxy-cache-indexed` emits no protocol token** (0), where the brief expects non-zero for all four producers. The others: ctl 9, refresh 5, cache-images 8. Its whole protocol is `OK <i>/<n> <label>`, `FAIL <i>/<n> <label>: <why>` and `DONE cached= failed= indexed=` lines on stdout (`:162-216`), read by the ctl, not by EmulationStation; § Q7's table names it as a producer the ctl consumes.
2. **R2's grep also lists eleven `exit` words in comments** (lines 28 to 255 in the header's verb descriptions, and :2120). They are documentation, not exits; the brief's list of code exits holds.
3. **§ 1's stage-A read, answered:** `tools/last-good-scripts-test` does run the ctl itself. Its groups p and t execute the real script inside `bwrap` (`:1612-1621`, `:2239-2246`; background runs at `:2485`, `:2524`, `:2565`, `:6661`), with `/storage` and `/run` as fixtures, `systemctl` and `logger` shimmed, and the client's network verbs answered by a `python3` shim. So "the ctl never runs on the host" holds for the host's own state, but not literally: the floor's own suite runs it in a sandbox.

## The upstream source (the floor's step 1)

The full record is `stage-a/unpack.txt`.
- **The pin:** the cache's `raofflineproxy-c7ebd1b6e777f3751ff0ecdf8aba54045844e00d.tar.gz` (sha256 `88eef31acfa4104b20258bd5cea514ade30e6cdf35767ffc958009851d61898b`, equal to `PKG_SHA256`; 745 entries) is unpacked to `/workspace/tmp/m6-t19/src/`. The 18 patches apply with GNU patch 2.8, `-p1 --fuzz=0`, in name order: all rc 0, 75 hunks, no rejects; offsets in 002, 008, 010 and 015.
- **The predecessor**, for `tools/raofflineproxy-integration-test`, is the previous shipped pin `879b158995` (the recipe at `7afa9efcfc`, 2026-10-06), from the same cache, sha256 equal to that commit's `PKG_SHA256`, with that commit's 16 patches, all rc 0. That is the recipe's *"16 patches"* comment's own moment: 020 and 021 arrived on 2026-10-14 (`f9b7ce3dfb`).
- **The integration test** passes: 12 tests, `OK`, 8 s.

## The context read

These are read at stage B for the producer side of each contract. **Line counts at their revisions:**

| Lines | File | Why |
| ---: | --- | --- |
| 148 | `es-app/src/OfflineAchievements.h` @ `16dbac5211` | the ctl's verbs as the interface calls them (10 mentions) |
| 353 | `es-app/src/OfflineAchievements.cpp` @ `16dbac5211` | `ask(verb)` :51-57, the last stdout line and the exit; `pending` :108, `flushed` :119, `summary` :250, `pending-ids` :275, `account` :286, `topup` :318, `index-offline` :325, `stopRun` :339-358; the store-only fetches :200-235 |
| 808 | `es-app/src/guis/GuiRetroAchievementsSettings.cpp` @ `16dbac5211` | `scan` :322, `enable|disable` :479, the `have_account` comment :154 |
| 589 | `es-app/src/CloudText.h` @ `16dbac5211` | the parsers :441-451, :473, :508, :560, :581 |
| 161 | `es-app/src/OfflineAchievementsText.h` @ `16dbac5211` | :105, :115, :149 |
| 1,072 | `es-app/src/RetroAchievements.cpp` @ `16dbac5211` | `u=<username>` on the proxy's query strings :301, :315, :338 (T20's) |
| 373 | `es-app/src/OfflineScanJob.{h,cpp}` @ `16dbac5211` (100 + 273) | the scan page's `>>> ` reader |
| 93 | `es-app/src/guis/GuiOfflineScan.h` @ `16dbac5211` | the scan page |
| 415 | `es-app/src/ThreadedHasher.cpp` @ `16dbac5211` | `index-offline` after a game list update |
| 74 | `es-app/src/RunLock.h` @ `16dbac5211` | the flock's holder `stopRun` signals |
| 596 | `es-app/src/ProxyCards.cpp` @ `16dbac5211` | the cards at the link's return; 143 and 130 read as stopped :291-294 (T2's PL-013, PL-022) |
| 264 | `es-core/src/components/WebImageComponent.cpp` @ `16dbac5211` | the badge fetch with `X-RA-Store-Only: 1` :240-241 (es-core, not es-app) |
| 1,479 | `projects/ROCKNIX/packages/rocknix/sources/scripts/setsettings.sh` @ `8ebaf8daad` | the routing per launch :532-545 |
| 131 | `.../ppsspp-sa/scripts/cheevos_ppsspp.sh` @ `8ebaf8daad` | :94-98, :125-129 |
| 148 | `.../dolphin-sa/scripts/cheevos_dolphin.sh` @ `8ebaf8daad` | :19, :139-144 (the port only) |
| 1,899 | `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool` @ `8ebaf8daad` | RATOKENFILES :698-703, RATOKENSETTINGS :705-709, DEVICEONLYDIRS :723-726 |
| 707 | `projects/ROCKNIX/packages/rocknix/profile.d/001-functions` @ `8ebaf8daad` | :113 |
| 44 | `projects/ROCKNIX/packages/virtual/network/package.mk` @ `8ebaf8daad` | :13, which ships it |
| 2,830 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth` @ `8ebaf8daad` | the serve that takes 8080 too, :2549-2560 (T17's) |

**The upstream's own modules** are read in `/workspace/tmp/m6-t19/src/` (the patched pin): `proxy_service.py`, `state.py`, `es_export.py`, `log_uploader.py` and `config.py` under `linux/raofflineproxy/`.

## The history

- **At `8ebaf8daad`, over the 27:** 99 non-merge commits and 0 merges, 2026-09-13 to 2026-10-14 (the last `f9b7ce3dfb`); 80 by Max Engel, 18 by blitterbot, 1 by rasterabot.
- **The recipe's pins, newest first:**

| Recipe commit | Date | Pin |
| --- | --- | --- |
| `a0f60255ab` | 2026-10-11 | `c7ebd1b6e7` |
| `7afa9efcfc` | 2026-10-06 | `879b158995` |
| `e4276a6743` | 2026-10-06 | `b09d604eca` |
| `9bb2b42e5a` | 2026-10-05 | `3036478f2b` |
| `a2586374b7` | 2026-10-05 | `7252fc7813` |
| `57cbc9b981` | 2026-10-04 | `865e218660` |

The siblings' comments cite `3036478f` and `5866cd9b`, both older than the pin.

### The patches' provenance

Each patch's first add, its last change, its commit count, and the issues its header cites:

| Patch | Added | Last change | Commits | Header cites |
| --- | --- | --- | ---: | --- |
| 001-dorequest-4xx-passthrough | `43b4a62909` 2026-09-13 | `a0f60255ab` 2026-10-11 | 4 | #166  |
| 002-no-synthetic-casual-only-achievement | `51e2acece6` 2026-09-14 | `409250ebce` 2026-10-03 | 3 | #166  |
| 003-flush-stamp | `67a89cb623` 2026-09-14 | `a2586374b7` 2026-10-05 | 4 | #173  |
| 004-no-cap-on-cached-games | `451a8b1021` 2026-09-14 | `9f170ee741` 2026-10-11 | 6 | #361  |
| 005-keep-the-refresh-thread-alive | `ce1dbcc986` 2026-09-25 | `a0f60255ab` 2026-10-11 | 4 | #186 #259  |
| 007-cached-sign-in-of-the-configured-account | `be3db49acb` 2026-09-14 | `409250ebce` 2026-10-03 | 3 | #186  |
| 008-log-upload-opt-in | `12484e492c` 2026-09-14 | `a2586374b7` 2026-10-05 | 6 | #186 #308  |
| 009-unique-image-temp-names | `109ad8706f` 2026-09-14 | `409250ebce` 2026-10-03 | 3 | #186  |
| 010-store-only-header | `9d4f496c7a` 2026-09-15 | `409250ebce` 2026-10-03 | 3 | #180 #190  |
| 011-offline-login-header | `fb0a42268d` 2026-09-15 | `a0f60255ab` 2026-10-11 | 4 | #194  |
| 012-offline-image-miss | `e29827cccc` 2026-09-15 | `a0f60255ab` 2026-10-11 | 5 | #180 #199  |
| 013-validate-a-cached-image-before-publishing-it | `2e1df9d4dc` 2026-09-18 | `409250ebce` 2026-10-03 | 5 | #213 #308  |
| 015-bounded-name-lookup | `f2f23da875` 2026-09-22 | `409250ebce` 2026-10-03 | 4 | #242 #308  |
| 016-say-what-became-of-a-download | `fa9af93285` 2026-09-28 | `409250ebce` 2026-10-03 | 2 | #307  |
| 018-pixelelated-platform-identity | `cf511ce79b` 2026-10-05 | `cf511ce79b` 2026-10-05 | 1 | #168 #408  |
| 019-consent-cache-initial-observation | `e4276a6743` 2026-10-06 | `e4276a6743` 2026-10-06 | 1 | #168 #457  |
| 020-rvz-padding-preserve-partial-word | `f9b7ce3dfb` 2026-10-14 | `f9b7ce3dfb` 2026-10-14 | 1 | none in its header (f9b7ce3dfb's message cites #583, #584, #588) |
| 021-flush-reconnect-during-startup | `f9b7ce3dfb` 2026-10-14 | `f9b7ce3dfb` 2026-10-14 | 1 | none in its header (f9b7ce3dfb's message cites #583, #584, #588) |

The absent numbers are as the brief gives them:
- **006:** retired by `ce1dbcc986`;
- **014 and 017:** retired by `409250ebce` and `e2761d15f9`, upstreamed on 2026-10-03.

## The issues (read on GitHub at 12:12 UTC; the latest dated mention in the tree)

| Issue | State, date and title | Latest work-log mention |
| --- | --- | --- |
| #452 | closed/completed 2026-10-05 | M7.P3: Reconcile proxy schema review note before refreshed build | 2026-10-05 |
| #414 | closed/completed 2026-10-04 | M7.P3: Keep the proxy schema note aligned with its upstream pin | 2026-10-04 |
| #329 | closed/completed 2026-09-29 | es: SCAN GAMES FOR OFFLINE ACHIEVEMENTS with no games on the device ends COULDN'T FINISH;  | 2026-09-29 |
| #306 | closed/completed 2026-09-28 | The wake check reads a history file RetroArch 1.22 does not write; the top-up at the link' | 2026-09-29 |
| #305 | closed/completed 2026-09-28 | At a reconnection: saves first, then one RetroAchievements batch, and the send card report | 2026-09-29 |
| #300 | closed/completed 2026-09-27 | An offline game list update holds the interface on a stalled hash-library fetch until the  | 2026-09-25 |
| #282 | closed/completed 2026-09-26 | After hours offline, the first game-exit sync ran out of its 20 s automatic budget on the  | 2026-09-25 |
| #246 | closed/completed 2026-09-24 | EmulationStation SIGSEGV 2.4 s after a Dr. Mario exit, offline with awards queued (RG35XX  | 2026-09-24 |
| #242 | closed/completed 2026-09-22 | Offline with the toggle on, VIEW THIS GAME'S ACHIEVEMENTS asked the web and timed out (RG3 | 2026-09-23 |
| #211 | closed/completed 2026-09-25 | RetroArch segfaults 8 ms after the badge image of a second offline award (Bubble Bobble, f | 2026-09-25 |
| #587 | open 2026-10-23 | M7.P5: Evaluate temporary service shutdown for browser headroom | 2026-10-16 |
| #585 | open 2026-10-26 | Standing: Queue upstream contributions after the initial build | 2026-10-26 |
| #568 | open 2026-10-14 | Backlog: Explain the final phase of offline achievement preparation | 2026-10-14 |
| #369 | open 2026-10-02 | Parked: offer the fork's generic fixes to their own projects (RetroArch, RAOfflineProxy, t | none in the work logs |
| #323 | open 2026-09-29 | Release notes, the wiki pages in the site's own voice, screenshots from the VM, and a tech | 2026-09-29 |
| #293 | open 2026-09-26 | Every automatic process in the saves and achievements lanes is shown while it runs, and a  | 2026-09-25 |
| #292 | open 2026-09-26 | Show the send when it happens: a card on the link's return for the offline awards the prox | 2026-09-25 |
| #266 | open 2026-09-25 | Bucket B re-derived: which of the 35 'device' boxes need a person with a handheld, and whi | 2026-09-25 |
| #236 | open 2026-09-29 | RC round on the RG35XX SP, now at 664ad9ac64: the soak, then the candidate is called; the  | 2026-09-29 |
| #224 | open 2026-09-19 | Offline RA: REFRESH ACHIEVEMENT STATUS -- a row that re-reads RetroAchievements state on d | none in the work logs |
| #214 | open 2026-09-18 | Offline RA: a per-game manifest, so "is this game ready?" is a number rather than a direct | 2026-09-18 |
| #212 | open 2026-09-25 | Cache a game's images with its achievements: 956 images missing across 123 cached games | 2026-09-25 |
| #173 | open 2026-09-15 | RA offline, phase 2b: tell the player at exit and at reconnect what happened to an offline | 2026-09-17 |
| #168 | open 2026-10-14 | RA offline, phase 5: docs and contributing back | 2026-10-14 |
| #163 | open 2026-09-14 | Epic: offline RetroAchievements through RAOfflineProxy, system-wide or per emulator | 2026-09-18 |
| #79 | open 2026-09-25 | Emulator crashes seen on the handhelds -- the running list | 2026-09-25 |

The two without a work-log mention are cited in audits instead:
- **#224:** latest in `docs/audits/2026_09_24-milestone-rc-round-since-186/`;
- **#369:** latest in `docs/audits/2026_10_06-milestone-m7-p4-fixes-383/` and in `docs/reviews/assessment.md`.
