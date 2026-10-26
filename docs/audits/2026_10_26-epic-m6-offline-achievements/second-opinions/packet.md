# Second opinion (Phase 4.6), M6 T19: the offline achievements proxy, in pixelelated's distribution

You are one of two independent reviewers for a read-only renovation audit of 27 paths under a **security and new-functionality lens**. They total 5,369 lines at the distribution commit `8ebaf8daad`.

- **Nine fork-own files:**
  - `raofflineproxy-ctl`, the OS's and the interface's one door to the proxy (bash, 2,455 lines);
  - three python helpers the ctl runs under `timeout`: `raofflineproxy-refresh`, `-cache-images` and `-cache-indexed`;
  - the recipe, the systemd unit, the boot-time daemon file, and two sibling recipes.
- **Eighteen patches** the fork carries against upstream RAOfflineProxy at its pin `c7ebd1b6e7`.

**What it is.** RAOfflineProxy is a Python service between an emulator's rcheevos client and retroachievements.org, on `127.0.0.1:8080`. It answers from a local SQLite store when the link is down, queues awards earned offline and sends them when the link returns, and caches game data and badges.

**What ships.** The product is an immutable handheld OS; a person updates it in place and keeps `/storage`. One player uses one console at a time. Every process on the device, the service and the interface included, runs as root.

**What you get.**

- The first reader is another lab's model. You get its `02-forward-audit.md` (whole: coverage, the listener, the credential's paths, the generated writers table, the patches, the bounds, the runs, the guest cycle, what the next slice inherits, 25 findings, the positives), `03-retrospective.md` and `04-analysis.md`.
- Then context: the order's entry and the brief's questions.
- Then the fork's files whole and line-numbered: the ctl, the three helpers, the unit, the daemon file and the recipe.
- Then the patches the findings turn on, whole: 001, 007, 008, 010, 011, 012, 013 and 015.
- Then **line-numbered excerpts** of the patched upstream modules the analyses cite: `proxy_service.py`, `auth.py`, `network.py`, `storage.py`, `utils.py`, `log_uploader.py` and `usage_report.py`, each cited range with eight lines of context.
- Then the interface's `CloudText.cpp` lines the protocol table cites.
- **When a claim needs lines outside the packet, say `outside the packet` and do not guess.**

**Masking.** Every section was passed through a mask that replaces a value after `key=`, `key:`, `token=`, `user=`, `pass...=` or `psk=` with `***`; a `***` is the mask, not the code. The packet was scanned for credential shapes before it left, and no hit was a value.

**Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. The ctl's and the helpers' line numbers are `8ebaf8daad`'s. The upstream modules' are the patched pin's.

**What was run.** Nothing can be run for you.

- **On the host:** the patched pin unpacked (18 of 18 at fuzz 0); its integration test, 12 OK; the scripts suite, 1,379 PASS (it runs the real ctl in a sandbox); one fixture reproducing F-17.
- **On a guest:** an image whose ctl and client are a later branch's. So the tree's four scripts ran from `/storage/t19/bin/` against that image's service. `02` § The guest cycle says which side each verdict belongs to.

Answer these first, in this order:

1. **Where a credential travels (Q2; F-01, F-02, F-05, F-25).**
   - Does `handle_offline_login` (`proxy_service.py`, the excerpt around 491-505) really serve the cached sign-in body, `Token` included, to a request that names the account and proves nothing? Under exactly which conditions?
   - Is anything in the request path a check the first reader missed: a header, the peer address, the `Host`?
   - Is the redaction of `t=` and `p=` in the request log and in the upload bundle complete for every credential the service holds?
   - Do the helpers' printed exception texts (`FAIL ... {error}`) ever carry a URL with a credential?
2. **What runs as root on an unauthenticated port (Q1; F-03, F-04).**
   - Is the readiness check's acceptance of a foreign `0.0.0.0:8080` listener right, and is its disagreement with `setsettings.sh:536` (quoted in `03`) what the first reader says?
   - What does the unit's lack of hardening actually expose, given that the device is single-user and root everywhere?
3. **A check whose failure reads as success (Q3, Q6; F-06, F-07, F-08, F-15, F-16, F-17, F-18, F-24).**
   - For each: is the branch the first reader names really reachable, and is its consequence what it says?
   - Is there a `cannot_tell` site that is not reached on a failure it should catch?
   - Is there a pipeline whose first stage's failure is discarded?
4. **A bound that is not enforced (Q4; F-11 to F-15).**
   - Check every row of `02` § The bounds against the code.
   - Is the scan's missing deadline a defect, or the foreground page's design the analyses say it is?
   - Is F-14 right that `http_post` marks no 429 pause where `http_get` does?

Then:

5. **Refute or confirm each finding F-01 to F-25** in `02` § Findings index: *confirmed*, *narrowed* (say how), or *refuted* (with the line). For the six proposed bugs (F-01, F-03, F-06, F-07, F-16, F-17), also judge the severity and the fix a stream would make, and what the code before a fix has already left on devices.
6. **What the first reader missed:**
   - a defect in the whole files, the patches or the excerpts: a credential where it should not be, a write judged by nothing, a lock that fails open, a stamp that can say the wrong thing, a protocol line the interface misreads, or a bound with no enforcement;
   - a patch whose `+` side introduces a defect;
   - a disposition that should be different.

**Output:**

- Numbered items `{PREFIX}-1`, `{PREFIX}-2`, ..., grouped under the six headings above.
- Each item gets one line saying *confirmed / narrowed / refuted / new*, then the `file:line` evidence, then two to five sentences.
- Do not restate the packet, and do not reproduce long code.
- Keep the whole reply under about 8,000 words.


## The first reader's 02-forward-audit.md (whole)

# Forward audit: M6.P2 T19, the offline achievements proxy (#666)

Read at `8ebaf8daad` (`reviewed-at` `7de4ece06d`, the read equal to it on the 27); the upstream proxy at its pin `c7ebd1b6e7` from the cache's tarball, patched 18 of 18 at fuzz 0 (`stage-a/unpack.txt`). Every row carries `proved:`: `tree` (read at its lines), `history`, `tool-run` (a command's output under `stage-a/` or `stage-b/`), `fixture`, `guest` (the window, owed) or `design`.

## Coverage

| Path | Lines | Read | Feeds | proved |
| --- | ---: | --- | --- | --- |
| `projects/ROCKNIX/packages/network/raofflineproxy-libchdr/package.mk` | 24 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (the sibling pins), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy-rcheevos/package.mk` | 23 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (the sibling pins), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/daemons/006-raofflineproxy` | 10 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The listener (the marker's second writer), Q1 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/package.mk` | 157 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (the pin, the comment, the install), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/001-dorequest-4xx-passthrough.patch` | 64 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/002-no-synthetic-casual-only-achievement.patch` | 61 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/003-flush-stamp.patch` | 80 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/004-no-cap-on-cached-games.patch` | 79 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/005-keep-the-refresh-thread-alive.patch` | 156 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/007-cached-sign-in-of-the-configured-account.patch` | 82 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/008-log-upload-opt-in.patch` | 144 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/009-unique-image-temp-names.patch` | 36 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/010-store-only-header.patch` | 39 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/011-offline-login-header.patch` | 125 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/012-offline-image-miss.patch` | 144 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/013-validate-a-cached-image-before-publishing-it.patch` | 151 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/015-bounded-name-lookup.patch` | 285 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/016-say-what-became-of-a-download.patch` | 66 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/018-pixelelated-platform-identity.patch` | 58 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/019-consent-cache-initial-observation.patch` | 81 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/020-rvz-padding-preserve-partial-word.patch` | 22 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/patches/021-flush-reconnect-during-startup.patch` | 30 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The patches (its row), Q5 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images` | 497 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The writers, § The bounds, § What T20 inherits, Q3, Q4 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed` | 222 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The credential's paths, § The bounds, Q2, Q4 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl` | 2455 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The listener, § The credential's paths, § The writers, § The bounds, § What T20 inherits, Q1 to Q8 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-refresh` | 232 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The credential's paths, § The bounds, § What T20 inherits, Q2, Q4, Q7 | tree |
| `projects/ROCKNIX/packages/network/raofflineproxy/system.d/raofflineproxy.service` | 46 | whole, at `8ebaf8daad` (stage B, `stage-b/reading-notes.md`) | § The listener (the unit, directive by directive), Q1 | tree |

## The listener

- **The bind:** `proxy_host` from the client's `config.json`, default `127.0.0.1` (`config.py:376-377` in the patched pin); the port 8080 (`config.py:368`). AF_INET only: `ThreadingTCPServer` keeps `TCPServer`'s address family (`proxy_service.py:268`), `allow_reuse_address = True` (`:269`). proved: tree.
- **Who can reach it:** any process on the device; nothing off it (a loopback bind). On ROCKNIX the interface, the emulators and every service run as root, so the port adds no reach for a local process, which could read `system.cfg` directly. Two non-local reaches remain: a web page shown on the device (the cloud sign-in window's WebKit, T17's) by DNS rebinding, since the service checks neither `Host` nor `Origin` (none in `proxy_service.py`) and sends no CORS header; and an emulator core running untrusted content. proved: tree.
- **What it answers without identity:**
  - `dorequest.php?r=patch|achievementsets|unlocks&u=<user>` from the store, and `/Badge/`, `/Images/`, `/UserPic/` from the image cache, to any client;
  - **a `login`/`login2` request naming the user, while upstream cannot be reached, is answered with the cached sign-in body** (`handle_offline_login`, `proxy_service.py:491-505`): no password or token is compared, and the body is the row `auth.load_cached_login_for` reads `Token` from (`auth.py`, patch 007). So the account's session token is served to any local client that names the (public) account while the device is offline (Q1, Q2; `04`);
  - `X-RA-Store-Only: 1` (patches 010, 012) selects the store whoever sends it: behaviour, not identity.
  proved: tree; the guest reads the login answer's keys, never its values.
- **The unit, directive by directive** (`system.d/raofflineproxy.service`; T22's table of the other units is `docs/audits/2026_10_25-epic-m6-os-system-services/02-forward-audit.md` on `feature/m6-os-system-services-669`, compared at stage C): `ConditionPathExists` :7 (the marker); `After=network.target network-base.service rocknix-sysconfig.service` :11; `Before=emustation.service essway.service` :16; `StartLimitIntervalSec=300` :23, `StartLimitBurst=5` :24; `Type=simple` :27; `Environment=` RAOFFLINEPROXY_CONFIG_DIR, HOME, XDG_CONFIG_HOME, MALLOC_ARENA_MAX=2 :28-32; `ExecStart` :33; `ExecStartPost=... listening --wait 30` :40; `Restart=on-failure` :41, `RestartSec=5` :42, `TimeoutStopSec=15` :43. **No `User=*** `Group=`, `DynamicUser=*** `Protect*`, `Private*`, `NoNewPrivileges`, `CapabilityBoundingSet`, `RestrictAddressFamilies`, `IPAddress*`, `SystemCallFilter`, `ReadWritePaths`, `Memory*`, `CPU*`, `Tasks*` or `UMask=`** (R3: 0). The service runs as root with the unit's defaults. proved: tree, tool-run; the user read from `ps` on the guest is owed.
- **The readiness check:** `port_listening` (ctl, `do_listening` above it) accepts any LISTEN at `0100007F:1F90`, `00000000:1F90` or the v4-mapped `...FFFF00000100007F:1F90` in `/proc/net/tcp{,6}`, whoever owns it. `ExecStartPost` and `enable` both rest on it, so a foreign listener on `0.0.0.0:8080` satisfies the start and the enable (Q1; the guest's first constructed positive). proved: tree.
- **The port shared:** `cloud_oauth`'s serve takes 8080 too (`:2553`'s comment, T17's), and the suite's case at output line 647 holds that the serve still comes up on the LAN address with the proxy on 127.0.0.1. proved: tree, tool-run.
- **The marker's two writers:** `enable`/`disable` (ctl :450, :436, :453, :527) and `099-networkservices` at boot from `daemons/006`'s `STATE`. proved: tree.

## The credential's paths

| Credential | Sink | Mask at that sink | Line | proved |
| --- | --- | --- | --- | --- |
| the username | argv, `/proc/<pid>/cmdline` | none | ctl :616 (`pending-ids`), :647 (`summary`), :764 (`account`), :1029 (`ready_games_into`); the file's own rule at :1244-1246 and :1265 (the environment) | tree |
| the username | the environment (`RA_SCAN_USER`) | none (`/proc/<pid>/environ`, root-readable) | ctl :1265, :1280 | tree |
| the username | the upload bundle | none: *"the bundle ... carries the account name"* (patch 008's description) | `log_uploader.py` | tree |
| the username | the usage report | salted SHA-256 (`client_id`) | `usage_report.py:47-50`; sent only with consent `is True` (`:180`) | tree |
| the username | the port's query strings (`u=`) | none (a public name) | the emulators; EmulationStation `RetroAchievements.cpp:301`, `:315`, `:338` (T20's) | tree |
| the password | `system.cfg` | none (plain text, T17's and #102's) | the client reads it itself: `load_rocknix_system_password_credentials` (`auth.py`, `config.py`) | tree |
| the password | argv, logs | not read into a variable by the ctl (presence only, ctl :1120-1121); the service's request log redacts `p=` (`redact_query_tokens`, `utils.py:110-116`; `redact_form_tokens` :119-124) | tree |
| the session token | `system.cfg` | none (plain text) | read for presence only by the ctl (:1121) | tree |
| the session token | the store's `login2::<user>` row | none (the store is plain SQLite) | read by `do_account` (ctl :767-787), which prints `score= softcore=` only (:787, checked :795-798) | tree |
| the session token | **the port** | **none: the offline login answers with the cached body** | `proxy_service.py:491-505` | tree |
| the session token | the service's log | `t=` redacted in request lines (`utils.py:110`); a body is logged through `redact_form_tokens` (`proxy_service.py` request handler) | tree |
| the session token | the upload bundle | `t=`, `p=` by `redact_query_tokens`; the quarantined store by `_SENSITIVE_CACHE_ENTRY` (`log_uploader.py:83-95`) | tree |
| the session token, the password | `scan.log` (the helpers' `FAIL ... {error}` lines, ctl `slog`) | none, and none needed so far: the client's exceptions read name no credential; the one URL-bearing message is `image_cache.py:276`, a media-host URL | `cache-indexed:187`, `:204`; `refresh:126`, `:132`, `:219` (stdout) | tree; the guest's scan.log read by count is owed |
| the web API key | none here | the proxy and the ctl use none (`REDACTED_QUERY_KEYS` has no `y`, `network.py:22`); `ra-candidate-games`' `RA_QA_WEBKEY` is T12's | tree |
| the per-emulator token files | not this slice's | T30's PL-009, PL-010, PL-020, PL-021; `backuptool` RATOKENFILES (T17's) | tree |
| all of the above | the packet | the stage-C scan, every hit dispositioned (`second-opinions/`) | design |
| all of the above | the screen | the ctl prints tokens and counts only; the pages are T20's | tree |

## The writers

Generated by `tools/t19-writers.py` at `8ebaf8daad` (rc 0, 77 rows; its drift control at `87d9969bbb` exits 1 with 49: `stage-b/writers-runs.txt`). The mode column says what the tree says; the guest reads each mode back.

| Line | Function | File | Writes by | Mode | Lock held | Reader | proved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `raofflineproxy-ctl:422` | `put_back` | `system.cfg` (`global.retroachievements.offlineproxy`, `.hardcore`, `.offlineproxy.hardcore_was`) | `set_setting` from `/etc/profile`, each value read back before the next | the writer's umask (none set) | none | `setsettings.sh`, `cheevos_ppsspp.sh`, `daemons/006` at boot, EmulationStation's SystemConf | tree |
| `raofflineproxy-ctl:434` | `enable_undo` | `system.cfg` (`global.retroachievements.offlineproxy`, `.hardcore`, `.offlineproxy.hardcore_was`) | `set_setting` from `/etc/profile`, each value read back before the next | the writer's umask (none set) | none | `setsettings.sh`, `cheevos_ppsspp.sh`, `daemons/006` at boot, EmulationStation's SystemConf | tree |
| `raofflineproxy-ctl:436` | `enable_undo` | `/storage/.cache/services/raofflineproxy.conf` (the marker) | direct (`touch`, `rm -f`) | the writer's umask (none set) | none | the unit's `ConditionPathExists`; `099-networkservices` rewrites it at boot | tree |
| `raofflineproxy-ctl:449` | `do_enable` | `/storage/.cache/services/` | `mkdir -p` | the writer's umask (none set) | none | the unit's `ConditionPathExists` | tree |
| `raofflineproxy-ctl:450` | `do_enable` | `/storage/.cache/services/raofflineproxy.conf` (the marker) | direct (`touch`, `rm -f`) | the writer's umask (none set) | none | the unit's `ConditionPathExists`; `099-networkservices` rewrites it at boot | tree |
| `raofflineproxy-ctl:453` | `do_enable` | `/storage/.cache/services/raofflineproxy.conf` (the marker) | direct (`touch`, `rm -f`) | the writer's umask (none set) | none | the unit's `ConditionPathExists`; `099-networkservices` rewrites it at boot | tree |
| `raofflineproxy-ctl:469` | `do_enable` | `system.cfg` (`global.retroachievements.offlineproxy`, `.hardcore`, `.offlineproxy.hardcore_was`) | `set_setting` from `/etc/profile`, each value read back before the next | the writer's umask (none set) | none | `setsettings.sh`, `cheevos_ppsspp.sh`, `daemons/006` at boot, EmulationStation's SystemConf | tree |
| `raofflineproxy-ctl:473` | `do_enable` | `system.cfg` (`global.retroachievements.offlineproxy`, `.hardcore`, `.offlineproxy.hardcore_was`) | `set_setting` from `/etc/profile`, each value read back before the next | the writer's umask (none set) | none | `setsettings.sh`, `cheevos_ppsspp.sh`, `daemons/006` at boot, EmulationStation's SystemConf | tree |
| `raofflineproxy-ctl:476` | `do_enable` | `system.cfg` (`global.retroachievements.offlineproxy`, `.hardcore`, `.offlineproxy.hardcore_was`) | `set_setting` from `/etc/profile`, each value read back before the next | the writer's umask (none set) | none | `setsettings.sh`, `cheevos_ppsspp.sh`, `daemons/006` at boot, EmulationStation's SystemConf | tree |
| `raofflineproxy-ctl:492` | `stop_running_run` | `/var/run/raofflineproxy-scan.lock` | opened read-write without truncating (created if absent); the holder's pid written at offset 0 | the writer's umask (none set) | none | `stop_running_run`, `RunLock::holder` in EmulationStation | tree |
| `raofflineproxy-ctl:523` | `do_disable` | `system.cfg` (`global.retroachievements.offlineproxy`, `.hardcore`, `.offlineproxy.hardcore_was`) | `set_setting` from `/etc/profile`, each value read back before the next | the writer's umask (none set) | none | `setsettings.sh`, `cheevos_ppsspp.sh`, `daemons/006` at boot, EmulationStation's SystemConf | tree |
| `raofflineproxy-ctl:527` | `do_disable` | `/storage/.cache/services/raofflineproxy.conf` (the marker) | direct (`touch`, `rm -f`) | the writer's umask (none set) | none | the unit's `ConditionPathExists`; `099-networkservices` rewrites it at boot | tree |
| `raofflineproxy-ctl:537` | `do_disable` | `system.cfg` (`global.retroachievements.offlineproxy`, `.hardcore`, `.offlineproxy.hardcore_was`) | `set_setting` from `/etc/profile`, each value read back before the next | the writer's umask (none set) | none | `setsettings.sh`, `cheevos_ppsspp.sh`, `daemons/006` at boot, EmulationStation's SystemConf | tree |
| `raofflineproxy-ctl:539` | `do_disable` | `system.cfg` (`global.retroachievements.offlineproxy`, `.hardcore`, `.offlineproxy.hardcore_was`) | `set_setting` from `/etc/profile`, each value read back before the next | the writer's umask (none set) | none | `setsettings.sh`, `cheevos_ppsspp.sh`, `daemons/006` at boot, EmulationStation's SystemConf | tree |
| `raofflineproxy-ctl:812` | `do_flushed` | `last-flush` (the service's, patch 003) | taken by rename to `.$$`, read, removed | the writer's umask (none set) | none | the ctl's `flushed`, for `OfflineAchievements.cpp:119` | tree |
| `raofflineproxy-ctl:814` | `do_flushed` | `last-flush` (the service's, patch 003) | taken by rename to `.$$`, read, removed | the writer's umask (none set) | none | the ctl's `flushed`, for `OfflineAchievements.cpp:119` | tree |
| `raofflineproxy-ctl:828` | `mark_running` | `running` | temp + rename (`mark_running`); removed at the end and by `take_lock` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | EmulationStation (a run it did not start, bound 900 s) | tree |
| `raofflineproxy-ctl:829` | `mark_running` | `running` | temp + rename (`mark_running`); removed at the end and by `take_lock` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | EmulationStation (a run it did not start, bound 900 s) | tree |
| `raofflineproxy-ctl:831` | `unmark_running` | `running` | temp + rename (`mark_running`); removed at the end and by `take_lock` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | EmulationStation (a run it did not start, bound 900 s) | tree |
| `raofflineproxy-ctl:842` | `slog` | `/storage/.config/raofflineproxy/` | `mkdir -p` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the service, the helpers, the ctl | tree |
| `raofflineproxy-ctl:844` | `slog` | `scan.log` (and `scan.log.1`) | append; rotated once past 1,048,576 B in `slog` only -- the helpers' stderr appends bypass the check | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | a person, over a shell | tree |
| `raofflineproxy-ctl:846` | `slog` | `scan.log` (and `scan.log.1`) | append; rotated once past 1,048,576 B in `slog` only -- the helpers' stderr appends bypass the check | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | a person, over a shell | tree |
| `raofflineproxy-ctl:977` | `ready_games_into` | the ready-set file `$1` (`/tmp/raofflineproxy-ready.*`) | direct (truncate, then the python's stdout) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `games_made_ready` | tree |
| `raofflineproxy-ctl:1029` | `ready_games_into` | the ready-set file `$1` (`/tmp/raofflineproxy-ready.*`) | direct (truncate, then the python's stdout) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `games_made_ready` | tree |
| `raofflineproxy-ctl:1093` | `write_stamp` | `/storage/.config/raofflineproxy/` | `mkdir -p` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the service, the helpers, the ctl | tree |
| `raofflineproxy-ctl:1094` | `write_stamp` | `last-scan` | temp + rename (`write_stamp`); its status ignored by every caller | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `CloudText::parseScanStamp` | tree |
| `raofflineproxy-ctl:1107` | `commit_cursor` | `scan-cursor` (and `.next`, `.next.tmp`) | temp + `os.replace` (python), then `mv -f` with a read-back (`commit_cursor`) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the next listing | tree |
| `raofflineproxy-ctl:1108` | `commit_cursor` | `scan-cursor` (and `.next`, `.next.tmp`) | temp + `os.replace` (python), then `mv -f` with a read-back (`commit_cursor`) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the next listing | tree |
| `raofflineproxy-ctl:1112` | `commit_cursor` | `scan-cursor` (and `.next`, `.next.tmp`) | temp + `os.replace` (python), then `mv -f` with a read-back (`commit_cursor`) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the next listing | tree |
| `raofflineproxy-ctl:1137` | `is_online` | `/tmp/raofflineproxy-probe.*` (the probe's own `online_state.json`) | `mktemp -d`, removed by `rm -rf` | the writer's umask (none set) | none | `is_online` | tree |
| `raofflineproxy-ctl:1141` | `is_online` | `/tmp/raofflineproxy-probe.*` (the probe's own `online_state.json`) | `mktemp -d`, removed by `rm -rf` | the writer's umask (none set) | none | `is_online` | tree |
| `raofflineproxy-ctl:1190` | `take_lock` | `/var/run/raofflineproxy-scan.lock` | opened read-write without truncating (created if absent); the holder's pid written at offset 0 | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `stop_running_run`, `RunLock::holder` in EmulationStation | tree |
| `raofflineproxy-ctl:1198` | `take_lock` | `/var/run/raofflineproxy-scan.lock` | opened read-write without truncating (created if absent); the holder's pid written at offset 0 | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `stop_running_run`, `RunLock::holder` in EmulationStation | tree |
| `raofflineproxy-ctl:1204` | `take_lock` | `running` | temp + rename (`mark_running`); removed at the end and by `take_lock` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | EmulationStation (a run it did not start, bound 900 s) | tree |
| `raofflineproxy-ctl:1587` | `list_jobs` | `scan-cursor` (and `.next`, `.next.tmp`) | temp + `os.replace` (python), then `mv -f` with a read-back (`commit_cursor`) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the next listing | tree |
| `raofflineproxy-ctl:1588` | `list_jobs` | `scan-cursor` (and `.next`, `.next.tmp`) | temp + `os.replace` (python), then `mv -f` with a read-back (`commit_cursor`) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the next listing | tree |
| `raofflineproxy-ctl:1592` | `list_jobs` | `scan-cursor` (and `.next`, `.next.tmp`) | temp + `os.replace` (python), then `mv -f` with a read-back (`commit_cursor`) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the next listing | tree |
| `raofflineproxy-ctl:1674` | `list_jobs` | the job list (`$1` of `list_jobs`, `/tmp/raofflineproxy-{scan,topup}.*`) | direct, strict UTF-8 | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `raofflineproxy-cache-indexed` | tree |
| `raofflineproxy-ctl:1708` | `run_jobs` | `/tmp/raofflineproxy-scan-out.*` (a fifo) | `mktemp -u` then `mkfifo` (a name, then the object) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `run_jobs`, fd 8 | tree |
| `raofflineproxy-ctl:1709` | `run_jobs` | `/tmp/raofflineproxy-scan-out.*` (a fifo) | `mktemp -u` then `mkfifo` (a name, then the object) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `run_jobs`, fd 8 | tree |
| `raofflineproxy-ctl:1711` | `run_jobs` | `scan.log` (and `scan.log.1`) | append; rotated once past 1,048,576 B in `slog` only -- the helpers' stderr appends bypass the check | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | a person, over a shell | tree |
| `raofflineproxy-ctl:1713` | `run_jobs` | `scan.log` (and `scan.log.1`) | append; rotated once past 1,048,576 B in `slog` only -- the helpers' stderr appends bypass the check | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | a person, over a shell | tree |
| `raofflineproxy-ctl:1785` | `run_jobs` | `/tmp/raofflineproxy-scan-out.*` (a fifo) | `mktemp -u` then `mkfifo` (a name, then the object) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `run_jobs`, fd 8 | tree |
| `raofflineproxy-ctl:1814` | `cancelled` | `/tmp/raofflineproxy-ready.*` | `mktemp`; removed at the end and by the EXIT trap | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `games_made_ready` | tree |
| `raofflineproxy-ctl:1876` | `run_image_pass` | `scan.log` (and `scan.log.1`) | append; rotated once past 1,048,576 B in `slog` only -- the helpers' stderr appends bypass the check | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | a person, over a shell | tree |
| `raofflineproxy-ctl:1971` | `do_scan` | `/storage/.config/raofflineproxy/` | `mkdir -p` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the service, the helpers, the ctl | tree |
| `raofflineproxy-ctl:1979` | `do_scan` | `/tmp/raofflineproxy-{scan,topup}.*` (the job list) | `mktemp`; removed by the EXIT trap | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `raofflineproxy-cache-indexed` | tree |
| `raofflineproxy-ctl:1981` | `do_scan` | the run's temporaries (the job list, the fifo, the ready sets, `scan-cursor.next`, `running`) | the EXIT trap's `rm -f` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | (cleanup: nothing reads them after) | tree |
| `raofflineproxy-ctl:2036` | `do_scan` | `/tmp/raofflineproxy-ready.*` | `mktemp`; removed at the end and by the EXIT trap | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `games_made_ready` | tree |
| `raofflineproxy-ctl:2041` | `do_scan` | `/tmp/raofflineproxy-ready.*` | `mktemp`; removed at the end and by the EXIT trap | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `games_made_ready` | tree |
| `raofflineproxy-ctl:2042` | `do_scan` | `/tmp/raofflineproxy-ready.*` | `mktemp`; removed at the end and by the EXIT trap | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `games_made_ready` | tree |
| `raofflineproxy-ctl:2095` | `do_scan` | `scan-cursor` (and `.next`, `.next.tmp`) | temp + `os.replace` (python), then `mv -f` with a read-back (`commit_cursor`) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the next listing | tree |
| `raofflineproxy-ctl:2139` | `pending_lock` | `/var/run/raofflineproxy-index-pending.lock` | opened read-write (created if absent) | the writer's umask (none set) | the index-pending lock (fd 6), best effort | `pending_lock` | tree |
| `raofflineproxy-ctl:2154` | `write_index_pending` | `index-pending` (and `.tmp`, `.ack.$$`) | temp + rename; acknowledged by rename aside | the writer's umask (none set) | the index-pending lock (fd 6), best effort | `do_topup` | tree |
| `raofflineproxy-ctl:2155` | `write_index_pending` | `index-pending` (and `.tmp`, `.ack.$$`) | temp + rename; acknowledged by rename aside | the writer's umask (none set) | the index-pending lock (fd 6), best effort | `do_topup` | tree |
| `raofflineproxy-ctl:2172` | `ack_index_pending` | `index-pending` (and `.tmp`, `.ack.$$`) | temp + rename; acknowledged by rename aside | the writer's umask (none set) | the index-pending lock (fd 6), best effort | `do_topup` | tree |
| `raofflineproxy-ctl:2174` | `ack_index_pending` | `index-pending` (and `.tmp`, `.ack.$$`) | temp + rename; acknowledged by rename aside | the writer's umask (none set) | the index-pending lock (fd 6), best effort | `do_topup` | tree |
| `raofflineproxy-ctl:2176` | `ack_index_pending` | `index-pending` (and `.tmp`, `.ack.$$`) | temp + rename; acknowledged by rename aside | the writer's umask (none set) | the index-pending lock (fd 6), best effort | `do_topup` | tree |
| `raofflineproxy-ctl:2177` | `ack_index_pending` | `index-pending` (and `.tmp`, `.ack.$$`) | temp + rename; acknowledged by rename aside | the writer's umask (none set) | the index-pending lock (fd 6), best effort | `do_topup` | tree |
| `raofflineproxy-ctl:2185` | `do_index_offline` | `/storage/.config/raofflineproxy/` | `mkdir -p` | the writer's umask (none set) | none | the service, the helpers, the ctl | tree |
| `raofflineproxy-ctl:2208` | `do_topup` | `/storage/.config/raofflineproxy/` | `mkdir -p` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | the service, the helpers, the ctl | tree |
| `raofflineproxy-ctl:2264` | `do_topup` | `last-topup-attempt` | direct (`touch`, unguarded) | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `do_topup`'s half-hour gate and its `-nt` played check | tree |
| `raofflineproxy-ctl:2267` | `do_topup` | `/tmp/raofflineproxy-{scan,topup}.*` (the job list) | `mktemp`; removed by the EXIT trap | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `raofflineproxy-cache-indexed` | tree |
| `raofflineproxy-ctl:2268` | `do_topup` | the run's temporaries (the job list, the fifo, the ready sets, `scan-cursor.next`, `running`) | the EXIT trap's `rm -f` | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | (cleanup: nothing reads them after) | tree |
| `raofflineproxy-ctl:2271` | `do_topup` | `/tmp/raofflineproxy-ready.*` | `mktemp`; removed at the end and by the EXIT trap | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `games_made_ready` | tree |
| `raofflineproxy-ctl:2364` | `do_topup` | `/tmp/raofflineproxy-topup-sc.*` | `mktemp`, stdout of `run-smart-cache`; removed | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `do_topup` (its last `"type":"result"` line) | tree |
| `raofflineproxy-ctl:2366` | `do_topup` | `scan.log` (and `scan.log.1`) | append; rotated once past 1,048,576 B in `slog` only -- the helpers' stderr appends bypass the check | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | a person, over a shell | tree |
| `raofflineproxy-ctl:2373` | `do_topup` | `/tmp/raofflineproxy-topup-sc.*` | `mktemp`, stdout of `run-smart-cache`; removed | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `do_topup` (its last `"type":"result"` line) | tree |
| `raofflineproxy-ctl:2401` | `do_topup` | `/tmp/raofflineproxy-ready.*` | `mktemp`; removed at the end and by the EXIT trap | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `games_made_ready` | tree |
| `raofflineproxy-ctl:2402` | `do_topup` | `/tmp/raofflineproxy-ready.*` | `mktemp`; removed at the end and by the EXIT trap | the writer's umask (none set) | the scan lock (fd 9, `take_lock`) | `games_made_ready` | tree |
| `raofflineproxy-cache-images:171` | `write_cursor` | `image_cache/verify-cursor` | direct `write_text` -- the one stamp here without temp and rename | the writer's umask (none set) | the caller's: the scan lock when the ctl runs it; none by hand | the next `--verify` pass | tree |
| `raofflineproxy-cache-images:173` | `write_cursor` | `image_cache/verify-cursor` | direct `write_text` -- the one stamp here without temp and rename | the writer's umask (none set) | the caller's: the scan lock when the ctl runs it; none by hand | the next `--verify` pass | tree |
| `raofflineproxy-cache-images:175` | `write_cursor` | `image_cache/verify-cursor` | direct `write_text` -- the one stamp here without temp and rename | the writer's umask (none set) | the caller's: the scan lock when the ctl runs it; none by hand | the next `--verify` pass | tree |
| `raofflineproxy-cache-images:198` | `write_absent` | `image_cache/absent` (and `.tmp`) | temp + `os.replace` | the writer's umask (none set) | the caller's: the scan lock when the ctl runs it; none by hand | the next image pass | tree |
| `raofflineproxy-cache-images:200` | `write_absent` | `image_cache/absent` (and `.tmp`) | temp + `os.replace` | the writer's umask (none set) | the caller's: the scan lock when the ctl runs it; none by hand | the next image pass | tree |
| `raofflineproxy-cache-images:201` | `write_absent` | `image_cache/absent` (and `.tmp`) | temp + `os.replace` | the writer's umask (none set) | the caller's: the scan lock when the ctl runs it; none by hand | the next image pass | tree |
| `raofflineproxy-cache-images:341` | `main` | a damaged cached image under `image_cache/static/` | unlink | the writer's umask (none set) | the caller's: the scan lock when the ctl runs it; none by hand | the fetch that follows in the same pass | tree |

rows=77 expected=77 targets=24 rev=8ebaf8daad

Beyond the four scripts: the service writes the store (`Storage`), the image cache (patches 009, 013), `last-flush` (patch 003), `cached_game_ids.txt` (`es_export.py:58-69`, a fixed `.tmp` and `os.replace`), `online_state.json` and its own log; and **`list_jobs` opens the store through the client's `Storage()` (ctl's listing), whose `_initialize_sqlite` sets `journal_mode=WAL` and runs `CREATE ... IF NOT EXISTS` (`storage.py:106-151`)**: the ctl's own `sqlite3.connect`s are `mode=ro`, but its listing can write the store's schema and its WAL files (Q3, Info). proved: tree.

## The patches

The tarball at the pin: sha256 `88eef31acfa4104b20258bd5cea514ade30e6cdf35767ffc958009851d61898b` = `PKG_SHA256` (R12). The recipe's comment at `package.mk:6` says *"The16 patches apply at fuzz0"*; 18 ship. The count was 16 at `7afa9efcfc`, the previous pin's recipe, before 020 and 021 (`f9b7ce3dfb`, 2026-10-14) (R10, `stage-a/unpack.txt`). The ctl's header note names the pin: `rc-preflight --only proxy-schema` `PASS` (R11), a comment check, *"runtime schema proof remains separate"*. The siblings name older proxy commits (`5866cd9b`, `3036478f`) as the source of their submodule pins; a tarball carries no gitlinks, so whether `c7ebd1b6e7` still names those commits is not checkable from the cache (Q5; the record's `docs/qa-logs/2026-10-03-proxy-refresh/coupled-pins.tsv` is cited at stage C). Every draft's base is older than the pin.

| Patch | Upstream file and function | Kind | At the pin | Added, last change | Draft under `docs/upstream/raofflineproxy/` | The #585 line owed | proved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `001-dorequest-4xx-passthrough` | `proxy_service.py` `is_passthrough_client_error`, the online path | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `43b4a62909` 2026-09-13; `a0f60255ab` 2026-10-11 | `client-errors/` (base `879b158995`) | the draft rebased onto `c7ebd1b6e7`; and a separate line for upstream's `network.http_post`, which marks no pause on a 429 (`network.py:549-563` against `http_get`'s `:408-409`): with 001 the 429 now reaches the emulator, and nothing in the proxy paces the next POST | tree, tool-run |
| `002-no-synthetic-casual-only-achievement` | `rom_cache.py` `filter_warning_achievement_definitions` | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `51e2acece6` 2026-09-14; `409250ebce` 2026-10-03 | `warning-sets/` (`879b158995`) | rebase onto the pin; the Android `filterWarningAchievementDefinitions` gap named beside it | tree, tool-run |
| `003-flush-stamp` | `flusher.py` `write_flush_stamp` | `feature` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `67a89cb623` 2026-09-14; `a2586374b7` 2026-10-05 | none | an interface to agree first (the contribution map: *agree interface with upstream*) | tree, tool-run |
| `004-no-cap-on-cached-games` | `rom_browser.py` `add_rom_to_cache(budgeted=False)`, `_drain` | `feature` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `451a8b1021` 2026-09-14; `9f170ee741` 2026-10-11 | none | an API and policy discussion first (the contribution map) | tree, tool-run |
| `005-keep-the-refresh-thread-alive` | `proxy_service.py` `PeriodicRefresh.run`/`run_pass`/`refresh_games` | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `ce1dbcc986` 2026-09-25; `a0f60255ab` 2026-10-11 | `refresh-resilience/` (`879b158995`) | rebase onto the pin | tree, tool-run |
| `007-cached-sign-in-of-the-configured-account` | `auth.py` `resolve_credentials`, `load_cached_login_for` | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `be3db49acb` 2026-09-14; `409250ebce` 2026-10-03 | `configured-login/` (`879b158995`) | rebase onto the pin; and the offline login's answer (`proxy_service.py:491-505`, below) | tree, tool-run |
| `008-log-upload-opt-in` | `config.py` `log_upload_enabled`; `proxy_service.py` `retry_storage_corruption_report` | `feature` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `12484e492c` 2026-09-14; `a2586374b7` 2026-10-05 | `log-consent/` (`879b158995`) | rebase onto the pin; the default is the project's to decide | tree, tool-run |
| `009-unique-image-temp-names` | `image_cache.py` `download_static_image` | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `109ad8706f` 2026-09-14; `409250ebce` 2026-10-03 | `image-publication/` (`bdcd229b45`) | rebase onto the pin | tree, tool-run |
| `010-store-only-header` | `proxy_service.py` `process_proxy_request` | `feature` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `9d4f496c7a` 2026-09-15; `409250ebce` 2026-10-03 | none | a store-only contract to coordinate | tree, tool-run |
| `011-offline-login-header` | `proxy_service.py` `response_head`, `handle_offline_login` | `feature` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `fb0a42268d` 2026-09-15; `a0f60255ab` 2026-10-11 | none | a provenance header to coordinate | tree, tool-run |
| `012-offline-image-miss` | `proxy_service.py` static assets, `store_only_requested` | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `e29827cccc` 2026-09-15; `a0f60255ab` 2026-10-11 | none | depends on 010's contract | tree, tool-run |
| `013-validate-a-cached-image-before-publishing-it` | `image_cache.py` `png_problem`, `_checked_image_body` | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `2e1df9d4dc` 2026-09-18; `409250ebce` 2026-10-03 | `image-completeness/` (`879b158995`) | rebase onto the pin; with a bound on the inflate (`zlib.decompress(idat)` has none) | tree, tool-run |
| `015-bounded-name-lookup` | `network.py` `resolve_host_bounded`, `getaddrinfo` memory; `proxy_service.py` forwarder | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `f2f23da875` 2026-09-22; `409250ebce` 2026-10-03 | `bounded-dns/` (`879b158995`) | rebase onto the pin; the uncapped lookup threads named | tree, tool-run |
| `016-say-what-became-of-a-download` | `image_cache.py` `download_static_image` return value | `feature` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `fa9af93285` 2026-09-28; `409250ebce` 2026-10-03 | none | an outcome API to coordinate with callers | tree, tool-run |
| `018-pixelelated-platform-identity` | `config.py` `running_on_rocknix` | `identity` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `cf511ce79b` 2026-10-05; `cf511ce79b` 2026-10-05 | `pixelelated-identity/` (`7252fc7813`) | rebase onto the pin | tree, tool-run |
| `019-consent-cache-initial-observation` | `usage_stats.py` `_consented` | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `e4276a6743` 2026-10-06; `e4276a6743` 2026-10-06 | `early-consent/` (`b09d604eca`) | rebase onto the pin | tree, tool-run |
| `020-rvz-padding-preserve-partial-word` | `rvz_datasource.py` lagged-Fibonacci padding | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `f9b7ce3dfb` 2026-10-14; `f9b7ce3dfb` 2026-10-14 | none | a draft owed (no header; `f9b7ce3dfb` cites #583, #584, #588) | tree, tool-run |
| `021-flush-reconnect-during-startup` | `proxy_service.py` `ConnectivityMonitor.run`, `run_proxy_service` | `fix` | absent: applies at fuzz 0, rc 0 (`stage-a/unpack.txt`) | `f9b7ce3dfb` 2026-10-14; `f9b7ce3dfb` 2026-10-14 | none | a draft owed (no header; `f9b7ce3dfb`) | tree, tool-run |

## The bounds

| Bound | Value | Enforced by | proved |
| --- | --- | --- | --- |
| `PROBE_TRIES`, `PROBE_INTERVAL` | 9 × 10 s | the top-up's probe loop, inside its deadline (ctl, `do_topup`) | tree |
| `STOP_WAIT` | 10 s | `stop_running_run`'s wait for the lock | tree |
| `ERRORS_IN_A_ROW` | 3 | `run_jobs`' `IN_A_ROW` | tree |
| `TOPUP_INTERVAL` | 1,800 s | the mark's age, `stat %Y` against `date +%s`; a negative age is not a skip | tree |
| `TOPUP_TIMEOUT` | 900 s | `time_left` from `START`: the lock wait, the probes, the listing (`timeout`), the jobs (`timeout`), the recently played pass (`timeout`), the image pass | tree |
| the top-up's played check | `-nt` | `history_path`'s newest of three files against `last-topup-attempt`: mtime against mtime, no clock read; **a mark touched while the clock ran ahead holds every later history file "not newer" until wall time passes it** (Q4) | tree; a guest positive (the mark dated ahead with `touch -d`) owed |
| the top-up mark | -- | **written unguarded** (`touch`, ctl :2264): a failed touch is not seen, and the half hour is not counted | tree |
| the scan | **none** | the scan's listing and jobs run with budget 0 (no `timeout`); its comment says so (*"The scan has no deadline of its own"*); only the image pass is bounded | tree |
| `IMAGE_PASS_SECONDS` | 300 s | `timeout` on the helper and `--seconds` inside it; verify at most half (`cache-images:309`); `as_completed(timeout=)` (`:417`); `os._exit` past it (`:468-476`) | tree |
| the refresh | 900 s + 60 | `timeout` in `do_refresh`; the helper's `--seconds` between games (`refresh:166`); 3 in a row (`:220`) | tree |
| `RAOFFLINEPROXY_IMAGE_WAIT` | 120 s | `wait_for_badges`' join (`cache-indexed:82-95`, `:217`) | tree |
| the batch cooldown | 30 s per 50 | `apply_scan_batch_cooldown` (`cache-indexed:71-79`) | tree |
| the 429 pause | the client's | `rate_limit` on GET (`network.py:408-409`); **not on POST** (`network.py:549-563`); a persisted pause stops patch 004's drain | tree |
| `scan.log` | 1,048,576 B, once | `slog`'s check only; the helpers' stderr appends (`2>>`) bypass it | tree |
| the IDAT inflate | **none** | `png_problem`'s `zlib.decompress(idat)` (patch 013) with no `max_length`; `_fetch_image` reads the body unbounded | tree |
| the lookup threads | 3 s each, **uncapped in number** | `resolve_host_bounded` (patch 015): one daemon thread per attempt, abandoned at 3 s, alive until glibc gives up (about 20 s) | tree |
| the unit's start | 30 s + 5, 5 in 300 s | `ExecStartPost`'s `--wait 30`, `RestartSec`, `StartLimit*` | tree |
| `TimeoutStopSec` | 15 s | systemd | tree |
| `count_ready` on failure | **0** | the export unreadable, or the client's count failing behind `tail -n 1` with no `pipefail`, reads 0 (Q6) | tree |

**A kill told from a result:** the recently played pass's exit decides its why (124 `TOOK_TOO_LONG`, any other non-zero `RETROACHIEVEMENTS_STOPPED_ANSWERING`); a result line that is missing or unparseable with exit 0 reads `0 0 0`, nothing cached (ctl, the `read -r SC SS SL` with `|| echo "0 0 0"`). So a kill is told apart; an unreadable result is not (Q4).

## The runs

| Run | Command | Exit | Wall | Figure | A FAIL would mean | proved |
| --- | --- | ---: | ---: | --- | --- | --- |
| R0 | `df -i /workspace` | 0 | 0.01 s | 25 % inodes used | no room for the scratch | tool-run |
| R1 | the 27's bytes at `8ebaf8daad` | 0 | 0.06 s | 27 paths, 5,369 lines | the branch differs from the read commit | tool-run |
| R2 | the ctl's shape | 0 | 0.01 s | 0 `set -`, 0 `pipefail`, 55 functions, `EX_` 316-320, the exits listed (and eleven `exit` words in comments) | the brief's line numbers are not the tree's | tool-run |
| R3 | the unit | 1 (the final `grep -c` counting 0) | 0.01 s | the six directives at their lines; hardening 0 | a directive moved or one was added | tool-run |
| R4 | the port outside the package | 0 | 0.13 s | 5 sites with the address, `cloud_oauth` 4 | a new route to the port | tool-run |
| R5 | the credential's keys and sites | 1 (`umask` count 0) | 0.01 s | keys 311-313; argv 616, 647/645, 764/759, 1029; env 1265 | a site moved or was added | tool-run |
| R6 | the stamps' writers | 0 | 0.01 s | the writers at their lines | a writer moved | tool-run |
| R7 | the helpers' writes | 0 | 0.01 s | verify-cursor direct :173; absent :200-201; refresh's `note()` :51 | as R6 | tool-run |
| R8 | the protocol tokens | 0 | 0.01 s | ctl 9, refresh 5, cache-images 8, **cache-indexed 0** (its protocol is `OK`/`FAIL`/`DONE`) | a producer gained or lost its protocol | tool-run |
| R9 | the deletions | 0 | 0.01 s | ctl :977, :1141; recipe :120, :123, :124 | a new deletion | tool-run |
| R10 | the patches and pins | 0 | 0.01 s | 18; *"The16 patches"*; pins; header :242 | the recipe moved | tool-run |
| R11 | `tools/rc-preflight --only proxy-schema` | 0 | 0.04 s | `PASS` | the header note no longer names the pin | tool-run |
| R12 | the tarball by the pin | 0 | 0.01 s | 14 tarballs; sha prefix equal | the cache lacks the pin, or its bytes changed | tool-run |
| R13 | the neighbours | 0 | 0.12 s | 5 OS files, 11 ES files | a new consumer | tool-run |
| R14 | `have_account` | 1 (dispatch count 0) | 0.02 s | the comment :154; the function :1119, :1170; 0 in 2434-2450 | a verb was added, or the comment moved | tool-run |
| R15 | the tools' readiness | 0 | 0.15 s | `--help` 0 ×3; 187 mentions; `qa-accounts` refuses without a port | a tool cannot run | tool-run |
| R16 | the syntax | 0 | 0.10 s | `bash -n` 0 (5.3.9); `py_compile` 0 ×3 (3.14.4) | a script does not parse | tool-run |
| R17 | the removal check from `7de4ece06d` | 0 | 0.01 s | empty | the lane changed a product path | tool-run |
| unpack | the pin's tarball, 18 patches, `-p1 --fuzz=0` | 0 | -- | 18 of 18, 75 hunks, 0 rejects | a patch does not apply to its pin | tool-run |
| integration | `tools/raofflineproxy-integration-test --source <pin> --predecessor-source <879b158995 + its 16>` | 0 | 8 s | 12 OK | the preparation helper or the upgrade reopen regressed | tool-run |
| suite | `QA_SYSTEM_ROOT=<donor> tools/last-good-scripts-test` | 0 | 523 s | 1,379 PASS, 0 FAIL; the proxy cases in `stage-a/last-good-scripts-test.txt`; **it runs the ctl itself, in `bwrap`** | a case regressed | tool-run |
| writers | `tools/t19-writers.py` | 0 | -- | 77 rows; control 49 and exit 1 at `87d9969bbb` | the writers' set changed | tool-run |

**The ctl never ran on the host outside the suite's sandbox; the proxy never ran on the host.** `00` records both.

## What T20 inherits

Written, not tested here.

**The protocol** (`>>> ` lines; the producers at `8ebaf8daad`, the readers at `16dbac5211`):

| Producer | Tokens (line) | Reader |
| --- | --- | --- |
| ctl `scan` | `doing listing` :1986; `total` :2018; `game i\|n\|name` :1723, :1778; `cached c\|s` :1776; `note NO_GAMES` :2012, `NOTHING_NEW` :2020, `LIMIT_REACHED` :2096, `TRUNCATED` :2100; `errors n` :2101; `why <TOKEN>` :1167, :1172, :1817, :1989, :2029, :2102; `done c\|s\|ready\|limit` :2015, :2106 | `OfflineScanJob` (the scan page), `CloudText::classifyProtocolLine` |
| ctl `topup` | none on stdout (`refuse_unless_ready topup >/dev/null`); the stamp only | `CloudText::parseScanStamp` (`CloudText.cpp:1186`) |
| ctl `images`, `refresh` | `why NO_NETWORK` :1897 and the helpers' own | **no reader at the pin** (no interface caller of either verb) |
| `raofflineproxy-refresh` | `doing refresh` :122; `total` :157; `refresh i\|n` :215; `note NOTHING_DUE` :152, `LEFT n` :169; `why STORE_UNREADABLE` :127, `NO_ACCOUNT` :133, `REPEATED_FAILURES` :222; `done a\|b` :153, :170, :223, :227 -- **b is `failed` at :227 and `left` at :170 and :223**; `note()` lines on the same stdout :50-51 | none at the pin (#224's row would be) |
| `raofflineproxy-cache-images` | `doing images` :284; `total` :379; `image i\|n` :433; `verified c\|n` :347, :356; `note VERIFY_COMPLETE` :358, `VERIFY_LEFT n` :362, `ABSENT n` :376, `NOTHING_MISSING` :381; `why STORE_UNREADABLE` :289, `NO_ACCOUNT` :296, `SOME_IMAGES_NOT_SAVED` :460, `CANCELLED` :495; `done f\|left` :382, :461 | the ctl sends it to `scan.log` under `run_image_pass`; none on screen |
| `raofflineproxy-cache-indexed` | none: `OK i/n`, `FAIL i/n label: why`, `DONE cached= failed= indexed=` (:162-216) | the ctl's `run_jobs` |

**The ctl's why tokens against `CloudText::scanWhy`** (`CloudText.cpp:1022-1055`) and `topUpWhy` (`:1057-1064`): the ctl emits TOGGLE_OFF, NO_ACCOUNT, SIGN_IN_REFUSED, RETROACHIEVEMENTS_STOPPED_ANSWERING, LIBRARY_UNREADABLE, TOOK_TOO_LONG, SOME_GAMES_NOT_SAVED, SOME_IMAGES_NOT_SAVED, CANCELLED, SOMETHING_WENT_WRONG, NO_NETWORK. `scanWhy` has a row for each but SOMETHING_WENT_WRONG and NO_NETWORK, which fall to its last line, `SOMETHING WENT WRONG` (the same words for the first; NO_NETWORK reaches no page). **`scanWhy` has a row for `NO_GAMES_FOUND`, which no producer emits** (the ctl says `note NO_GAMES`, fork #329): a reader row for a token gone.

**The stamps' shapes:** `last-scan` -- `<epoch> <rc> <scan|topup> cached= skipped= ready= limit= indexed= errors= added=[ truncated=1][ why=][ note=]` (ctl `write_stamp`; read by `parseScanStamp`, `CloudText.cpp:1186-1270`, which passes over unknown keys and a non-numeric `added`); `last-flush` -- `<epoch> <flushed>` (patch 003; taken by the ctl's `flushed`, `OfflineAchievements.cpp:119`); `running` -- `route=<scan|topup|images|refresh> at=<epoch>[ index= total= name=]` (ctl `mark_running`; read at `CloudText.cpp:1312-1330`); `index-pending` -- `<epoch> <pid> <random>` (the ctl's alone). The exit codes the pages act on: 0, 1, 2 (usage at `:2453` and every `cannot_tell`; `listening` and `refresh` use 64 for usage), 69, 75, 77, 78, 130, 143.

**The page comment's wording:** `GuiRetroAchievementsSettings.cpp:154` names `raofflineproxy-ctl have_account` as if a verb; it is the ctl's function (:1119, called :1170), not in the dispatch (:2434-2450).

**The consent setting's name:** `usage_stats_consent` (with `usage_stats_consent_version`) in the client's `config.json` (patch 019; `usage_report.py:180`); `upload_logs` (JSON `true` only) for the automatic log upload (patch 008).

## Findings index

Each is graded in `04` (severity, class, the brief's question, the `proved:` a fix would need); the ctl's lines are `raofflineproxy-ctl` at `8ebaf8daad`, the service's the patched pin's.

| ID | Q | One line | Where |
| --- | --- | --- | --- |
| F-01 | Q1, Q2 | the offline login answers any `login`/`login2` naming the account with the cached sign-in body, `Token` in it, comparing no password or token, while upstream cannot be reached (upstream code) | `proxy_service.py:491-505`; `auth.py` `load_cached_login_for` (patch 007) |
| F-02 | Q1 | the service validates neither `Host` nor `Origin`: a page shown on the device can reach the port by DNS rebinding, where F-01's answer is readable | `proxy_service.py` (no check); the sign-in window (T17's) |
| F-03 | Q1 | the readiness check accepts any LISTEN on `0.0.0.0:8080`, whoever owns it; `ExecStartPost` and `enable` rest on it, while `setsettings.sh`'s own check takes `127.0.0.1:8080` only, so a foreign `0.0.0.0` listener turns the toggle on and every launch goes direct | ctl `port_listening` :925-937, `do_listening` :939-957; unit :40; `setsettings.sh:536` |
| F-04 | Q1 | the service runs as root with no hardening directive (no `User=*** `Protect*`, `Private*`, `NoNewPrivileges`, `CapabilityBoundingSet`, `RestrictAddressFamilies`, `UMask=`) | `raofflineproxy.service` (R3: 0); against T22's per-unit table at stage C |
| F-05 | Q2 | the username on `python3`'s argv at four sites, against the file's own rule (*through the environment, never a command line*) | ctl :616, :647, :764, :1029 against :1244-1246, :1265 |
| F-06 | Q3 | the scan lock that cannot be opened reads as nothing running: `disable` then stops the service under a live run | ctl :492 |
| F-07 | Q3 | `write_stamp`'s status is ignored by every caller: a stamp that could not be written leaves the row on the last run | ctl :1073-1094 against :2103, :2411, :2423, :2427 (and the cancel, no-games, nothing-new and unreadable paths) |
| F-08 | Q3 | `list_jobs` opens the store through the client's `Storage()`, whose initialisation sets WAL and creates the schema: the ctl's "read-only" holds for its own connects only | ctl :1417; `storage.py:106-151` |
| F-09 | Q3 | `verify-cursor` is written directly (no temp and rename), and the helpers' stderr appends to `scan.log` past `slog`'s rotation | `cache-images:169-177`; ctl :1711, :1713, :1876, :1987, :2301, :2366 against :843-846 |
| F-10 | Q3 | the jobs' fifo is named by `mktemp -u` and made by `mkfifo` (a name, then the object) | ctl :1708-1709 |
| F-11 | Q4 | the scan has no deadline: its listing and its jobs run with budget 0; only the image pass is bounded | ctl :1987, :2037; the comment at :2062 |
| F-12 | Q4 | the top-up mark is touched unguarded, and the played check compares the history's mtime with the mark's: a mark dated ahead of the clock holds every later play "not newer" | ctl :2264; :2221, :2235 |
| F-13 | Q4 | two inputs without a bound: the IDAT inflate (`zlib.decompress` with no `max_length`, the body read whole) and the lookup threads (one per attempt, abandoned at 3 s, uncapped in number) | patch 013 (`image_cache.py` `png_problem`, `_fetch_image`); patch 015 (`network.py` `resolve_host_bounded`) |
| F-14 | Q4 | `http_post` marks no 429 pause where `http_get` does; with patch 001 the 429 reaches the emulator and nothing paces its next POST (upstream code) | `network.py:549-563` against `:408-409`; patch 001 |
| F-15 | Q4, Q6 | the recently played pass's result line unreadable with exit 0 reads `0 0 0`, nothing cached; a kill is told apart by its exit | ctl :2372-2380 |
| F-16 | Q6 | `count_ready` prints `0` when the export cannot be read and the client's count fails behind `tail -n 1` with no `pipefail`; its comment says a number not known is never invented | ctl :888-897 |
| F-17 | Q6 | one ROM name with a byte invalid in UTF-8 fails the whole listing (`out.write_text(..., encoding="utf-8")` over surrogate-escaped paths): the scan reads `why LIBRARY_UNREADABLE` | ctl :1674, :1987-1989; reproduced: `stage-b/listing-fixture.txt` |
| F-18 | Q6 | two usage exits: the dispatch's 2, `listening` and `refresh`'s `EX_USAGE` 64 | ctl :2453 against :316, :944, :1935, :1938 |
| F-19 | Q6, Q7 | the refresh helper prints `note()` lines on the protocol's stdout, and its `done a\|b` means *failed* at the end and *left* at the deadline and on repeated failures; no reader at the pin | `refresh:50-51`, `:170`, `:223`, `:227` |
| F-20 | Q7 | `CloudText::scanWhy` keeps a row for `NO_GAMES_FOUND`, which no producer emits; the page's comment names `have_account` as if a verb (T20's to tidy) | `CloudText.cpp:1032-1033`; `GuiRetroAchievementsSettings.cpp:154` |
| F-21 | Q5 | the recipe says *"The16 patches apply at fuzz0"* over eighteen; the siblings name older proxy commits as their pins' source; 020 and 021 carry no header | `package.mk:6`; the siblings' :5-9; patches 020, 021 |
| F-22 | Q5 | eight patches have no upstream draft (003, 004, 010, 011, 012, 016, 020, 021) and every draft's base is older than the pin: the #585 lines owed | § The patches; `docs/upstream/raofflineproxy/contribution-map.md` |
| F-23 | Q8 | the proxy-schema check is a comment check (*"runtime schema proof remains separate"*), and `last-good-scripts-test` runs the real ctl in `bwrap` -- the harness's reach and limit stated | R11; `stage-a/last-good-scripts-test.txt` |
| F-24 | Q3 | the jobs' classifier matches its stop words over the whole line, file name included: a `FAIL` for a ROM named with `login required` or `HTTP Error 401` stops the scan as a refused sign-in | ctl :1750 |
| F-25 | Q2, Q3 | every file the proxy and the ctl write takes `644 root` under the service's umask `0022` (none set), the store with the session token's row included: world-readable, on a device where every process is root | `guest-cycle/b1-03-scan.txt`; § The writers' mode column |


**A lead outside the slice** (M7's, not graded here): the image's installed client (`build/m7-signin-20261022-07`, 57 modules) fails 4 of the 18 native hashing cases that the record's run passed with the same tests file and the same library (`guest-cycle/b1-08-*`); the coordinator routes it.

## Positives

The constructed positives, each recorded as it falls (the guest's are owed to the window):

| Lead | Positive | Where | Expect on `8ebaf8daad` | proved |
| --- | --- | --- | --- | --- |
| a foreign listener satisfies readiness | a listener on `0.0.0.0:8080` with the service stopped; `raofflineproxy-ctl listening` | guest | exit 0 | guest: **falls** (`b1-04`) |
| the scan lock that cannot be opened reads as nothing running | the lock path made a directory (root bypasses a mode), a run started, `disable` | guest | `disable` proceeds and stops the service | guest: **falls** (`b1-06`) |
| an unreadable export reads 0 | the export made a directory; `ready` | guest | `0` | guest: **falls** (`b1-05`) |
| one undecodable ROM name fails the listing | a ROM named with a byte invalid in UTF-8 | host (`tools/t19-listing-fixture.py`: the listing's python from the ctl at `8ebaf8daad`, unchanged, against the patched pin with a scratch store) and guest | the listing exits non-zero; the scan's why `LIBRARY_UNREADABLE` | fixture: **reproduced** (`stage-b/listing-fixture.txt`: the decodable library rc 0, `found=1`; one name with 0xff, rc 1, `UnicodeEncodeError ... surrogates not allowed` at the job file's strict write); guest: **falls** (`b1-05`) |
| the offline login serves the token | `curl` `dorequest.php?r=login2&u=<the QA user>` with the link down | guest | a 200 whose body has a `Token` key (counted, never printed) | guest: **falls**, the image's service (`b1-07`) |
| a mark ahead of the clock silences the top-up | `last-topup-attempt` dated ahead (`touch -d`), a game played, `topup` | guest | skipped, `scan.log` *"no game played since the last attempt"* | guest: **falls** (`b1-09`) |

## The guest cycle

**The grant:** the coordinator's comment on #666 at 12:41 UTC, as planned. **START 12:43:49 UTC, RETURN 12:53:37 UTC**, both posted on #666 with census 0 (qemu, `:8080`, compilers), inside the 13:43:49 bound. The record is `guest-cycle/`.

- **The image:** `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, `.sha256` OK. Two fresh 16 GB disks of the lane's own; T2's `t2.qcow2` untouched. Read from the guest: `OS_NAME="pixelelated"`, `VERSION="0.0.1-dev+20261022T235948Z.g069fc2704421"`, `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, **`BUILD_BRANCH="build/m7-signin-20261022-07"`**. proved: guest.
- **Installed against the tree** (`b1-01-identity.txt`):
  - the unit and the daemon file are **equal** to `8ebaf8daad`;
  - **the four scripts differ.** The ctl by 233 diff lines (M7's owner-based `enable`/`disable` and new `toggle`, `operation`, `queue-status` verbs, D-RA-050); each helper by 7;
  - the installed client has 57 modules to the pin tarball's 45.
  - **So the positives ran `8ebaf8daad`'s four scripts, copied to `/storage/t19/bin/` (each sha256 equal to the tree's), against the image's installed client and service.** The service-side results (F-01, the native and consent tests) are the image's service and M7's client, said so on each row; the question is put to the coordinator. proved: guest.
- **The listener as it runs** (`b1-02-enable.txt`): the service runs as `root` (MainPID's user), its umask `0022`, listening on `127.0.0.1:8080`. `systemctl show`: `User=*** empty, `NoNewPrivileges=no`, `ProtectSystem=no`, `ProtectHome=no`, `PrivateTmp=no`, the full `CapabilityBoundingSet`, `UMask=0022`. The QA account was carried in by `tools/qa-accounts` (never printed), and the tree's `enable` printed `hardcore=0`, rc 0. proved: guest.
- **The modes as written** (`b1-03-scan.txt`): a scan with the tree's ctl over one seeded ROM. `>>> doing listing`, `total 1`, `game 1|1|...`, `cached 1|0`, `done 1|0|1|0`, rc 0; `last-scan` `... 0 scan cached=1 skipped=0 ready=1 limit=0 indexed=0 errors=0 added=1`. Every file under `/storage/.config/raofflineproxy/` is **`644 root`**: `proxy.sqlite3` (with the session token's row), its `-wal` and `-shm`, `last-scan`, `scan.log`, `cached_game_ids.txt`, `online_state.json`, `service.log`, the queue locks. The folder and `image_cache/` are `755`; the marker and `/var/run/raofflineproxy-scan.lock` are `644`. `scan.log`: 13 lines, 0 naming `t=`, `p=`, a token or a password. proved: guest.
- **The constructed positives**, each as it fell (proved: guest):
  - **F-03** (`b1-04-positive-f03.txt`): control, the service stopped and nothing listening: `listening` rc 1. A stand-in on `0.0.0.0:8080`: **`listening` rc 0**, while `setsettings.sh:536`'s check launches direct. **Falls.**
  - **F-16** (`b1-05-positives-f16-f17.txt`): `ready` 1; **the export a directory: `ready` 0, rc 0**; restored, 1. **Falls.**
  - **F-17** (the same file): one name with 0xff: **`why LIBRARY_UNREADABLE`**, the stamp's rc 1, `UnicodeEncodeError` in `scan.log`. **Falls.**
  - **F-06** (`b1-06-positive-f06.txt`): a stand-in holder (`scripts/holder.sh`) takes the lock as `take_lock` does, and the path is made a directory. `disable` rc 0 in 1 s (`line 492: ... Is a directory`), the service stopped, the marker gone, **the holder still alive, 0 journal lines asking it to stop**. Control, the lock openable: `disable` signals the holder (gone after), 1 such line, 10 s. **Falls.**
  - **F-01** (`b1-07-positive-f01.txt`; `scripts/login-probe.py`, key names only): one cached `login2` row. Control, the link up: a `login2` naming the account with no password or token, 403 from upstream, a 17-byte non-JSON body, no `Token`. **The link cut on the monitor (`set_link net0 off`): 200, `X-RA-Offline: 1`, body keys `AccountType, AvatarUpdatedAt, AvatarUrl, Messages, Permissions, Score, SoftcoreScore, Success, Token, User`, `Token` present and non-empty.** **Falls** (the image's service).
  - **F-12** (`b1-09-positive-f12.txt`): the history touched now and the mark a day ahead: the top-up rc 0, **1 `scan.log` line "no game played since the last attempt"**. Control, the mark two hours back: 0 such lines, the link-return and recently played passes run. **Falls.**
- **`tools/raofflineproxy-installed-native-test`** (`b1-08-installed-native.txt`, `b1-08-native.json`): the pin's `test_linux_rom_hashing.py` (sha256 `500373b9...`, the record's), the record's `legacy-chd.py`, the library sha256 `6c484a29...` (installed equal). **18 run, 4 failures, 0 errors, 0 skips**, against the record's 18 of 18 with the same tests and library. The difference is the installed client (M7's). The four's names were not determined in the window: `python3 -m unittest -v` fails at import, and the tool's report keeps counts only. proved: guest.
- **`tools/ra-offline-test`** (`b1-10-ra-offline-test.txt`): rc 1 at its step 2, 12:50:38 to 12:51:15 UTC: *"the QA account has already earned every achievement this fixture can reach: 100359 Potato-tan Secret (game 15738, earned 2026-10-06 06:07:32)"*. **CANNOT in this window** (D-RA-006 open). Nothing launched, nothing spent. The award proof stands on `docs/qa-logs/2026-10-06-ra-award/` (33 PASS). proved: guest.
- **The close of boot 1** (`b1-11-close.txt`): `qa-accounts clear` cleared the account's keys but left `/storage/.config/raofflineproxy` (rc 1: *"offline achievements are on; raofflineproxy-ctl disable first"*). It lived only on `boot1.qcow2`, retired below. `vm-stop` rc 0 (pid 564592).
- **Boot 2, no NIC** (`b2-*.txt`; `scripts/boot2-cmd.sh`: `qemu-args` without `-netdev`/`virtio-net`, with `-nic none`): 0 default routes, links `lo` only. `raofflineproxy-consent-test --expected-build 069fc270...`, uploaded by `vm-serial script`. Its first run refused the output path (*a fresh directory under `/storage/.cache`*); the second: **30 checks, rc 0**. `summary.json` `build_id` equal. Unanswered, declined, malformed or stale consent sends 0; `logs-only` sends 2 and `both-enabled` 3 on the first call, 0 on restart. `vm-stop` rc 0 (pid 617916). proved: guest.
- **The leftover check at RETURN:** qemu 0, `:8080` 0, compilers 0, sockets 0.
- **Retired (D-INFRA-022)** (`guest-cycle/retired.txt`):
  - `/workspace/tmp/m6-t19/guest/boot1.qcow2`, 2,312,372,224 bytes, sha256 `ddb5a7f6f7f367570f0c662577e59214205cf5fbf592145c5e9109d13f913025`;
  - `/workspace/tmp/m6-t19/guest/boot2.qcow2`, 2,310,471,680 bytes, sha256 `e4731d563bc1c07851fe2d682540ac11bdb920027b9473030a5e7bbcb993cf75`;
  - both removed with their firmware vars and the run's QA key.
**The labels, as ruled** (the coordinator on #666, 12:55 UTC):
- **The tree's scripts against the image's service.** The script-side positives: F-03, F-06, F-12, F-16, F-17; F-25's modes; the listener as root with no hardening. Graded with the seats as found.
- **The image's client** (`build/m7-signin-20261022-07`, hashes in `b1-01-identity.txt`): F-01's offline login, the consent test's 30, the native test's 18 run and 4 failed.
  - **For the pin, re-derived as a read** (`design`): F-01 at the patched pin's `proxy_service.py:491-505` (`handle_offline_login`: the cached `login` row's body for any request naming `u=`, no credential compared) and `auth.py`'s `load_cached_login_for` (the row carries `Token`). The consent path is patch 019's `_consented` (`usage_stats.py`), with `usage_report.py:180` sending only on `load_consent(...) is True`, and patch 008 gating the one automatic upload (`proxy_service.py:1477`).
  - **The native tests on the host** (`stage-c/native-host.out`, `tool-run`): upstream's `linux/tests/test_linux_rom_hashing.py` from the patched pin's root, the host's python 3.14.4. **18 run: 3 OK and 15 skipped** (*"libraproxy_rchash not available"*: the library is a build's product, and no build runs here). So the 15 native cases are **CANNOT** on the host.
- **The installed-native run against the tree's own service** is the integration build's: **`pending-image`**, with this cycle's record as the before (18 run, 4 failed, on M7's client). The 4 are M7's to name (the coordinator posted them on #1111). One aid for naming them: the tests import as the package `linux.tests...`, so `python3 -m unittest` runs them from the tree's root. That is why the window's verbose run failed at import.
- **Three slips in the run, recorded in their files:** a `pkill` by pattern in the guest that did not match (the stand-in then stopped by its pid, 2977); the probe's NameError on a non-JSON body (fixed before its result); the clear without `disable`.



## The first reader's 03-retrospective.md (whole)

# Retrospective audit — M6.P2 T19, the offline achievements proxy (#666)

The proxy against its own record: the epic audit `docs/audits/2026_09_14-epic-offline-retroachievements/` (#186), the fix rounds #307 and #308 its comments and patches cite, and the decisions D-RA-001 to D-RA-048. Read at `8ebaf8daad`; the upstream at its pin, patched (`02`).

## 3.1 Architectural coherence

- **One door.** The ctl is the OS's and the interface's one way to the proxy (enable, disable, the answers, the scan, the top-up), and every answer the interface reads is a last line or a stamp it parses in `CloudText` (`02` § What T20 inherits). The shape held across nineteen rounds of change: 99 commits, 2026-09-13 to 2026-10-14.
- **What runs where.** The service is upstream's, patched; the four scripts are the fork's. The seam between them is the store: the ctl reads it read-only through its own `sqlite3` calls -- except `list_jobs`, which opens it through the client's `Storage()` (F-08). One rule, held almost everywhere.
- **The fork's lanes.** Every patch is in a lane the fork works (D-UI-079): the cards, the scan, the images, the sign-in, the consent. None changes how awards are signed or queued.

## 3.2 Project conformance

- **Guards fail closed** (`engineering-practices.md`): `cannot_tell` (exit 2, nothing on stdout) for every store read the interface acts on; `added=unknown` rather than a count (PL-031); `as_flag` for every setting. Two exceptions read in the tree: `count_ready`'s 0 (F-16) and the scan lock's `|| return 0` (F-06).
- **The last known good state** (D-CLOUD-078): `last-scan`, `running`, `index-pending`, `scan-cursor`, `absent` and the service's `last-flush` and `cached_game_ids.txt` are written whole by temp and rename. `verify-cursor` is not (F-09), and `write_stamp`'s status is ignored (F-07).
- **A credential never on a command line**: the file states it (`:1244-1246`) and follows it once (`:1265`); four python calls pass the username on argv (F-05). The token and the password are never read into a variable by the ctl.
- **Every fix answers what was already written** (`upgrade-and-install.md`): the integration test's upgrade case reopens the predecessor's store with current `Storage` and keeps its bytes (`stage-a/unpack.txt`).

## 3.3 Spec fidelity

- **D-RA-001, D-RA-002** (one system-wide toggle, casual only, hardcore switched with the sentence on screen): `do_enable` records hardcore once, turns it off, sets the toggle last, and undoes every step on a failure; `do_disable` puts it back from the record (`02`). Held.
- **D-RA-004, D-UI-095, D-UI-101** (the cards at the link's return): the `flushed` stamp taken by rename, once per flush (patch 003, ctl `do_flushed`). Held.
- **D-RA-010, D-RA-013** (the scan and the index): the I and H job shapes, the index rule per system, the cursor (#307 PL-059). Held; F-17 is the walk's one input that fails the whole listing.
- **D-RA-016, D-WORKFLOW-164, -165** (whatever the fork changes in the proxy goes back; not sent until the build): ten drafts, none sent; eight patches without one (F-22).
- **#186 PL-12** (the storage-corruption upload opt-in): patch 008 gates the one automatic caller (`proxy_service.py:1477`); the manual upload is in `menu_sdl.py`, which the image never draws. Held.

## 3.4 Platform conformance

- **The unit** carries the fork's start-up contract (`ExecStartPost` waits for the listener; five starts in 300 s) and no hardening directive (F-04): every other directive is the defaults'. T22's table of the other units is compared at stage C.
- **The busybox shell** is not the ctl's: it is `#!/bin/bash` and the recipe depends on `bash`, `coreutils` (`timeout`) and GNU `grep` (#308 F-RA-23, F-RA-24); `last-good-scripts-test` runs it under the donor's busybox applets in `bwrap` (1,379 PASS).

## 3.5 Cross-system interaction audit

### Interaction: the ctl x EmulationStation (T20's, T2's)
The interface calls `pending`, `flushed`, `account`, `summary`, `pending-ids`, `topup`, `index-offline`, `scan` and `enable`/`disable` at the pin; never `refresh` or `images` (F-19). Every reader parses the producer's shape in `CloudText`; one reader row has no producer (F-20). `stopRun` signals the flock's holder found by `/proc/<pid>/fd` (`OfflineAchievements.cpp:339-358`); the ctl writes its pid into the lock for that (`take_lock`).

### Interaction: the port x the launch scripts (T1's)
`setsettings.sh:532-545` routes RetroArch to 8080 only when the toggle is 1, hardcore 0 and `netstat -ltn` shows a listener on `127.0.0.1:8080 ` (:536). That is a different check from the ctl's: it takes any owner on `127.0.0.1:8080` but not `0.0.0.0:8080`, which the ctl's `port_listening` takes. So a foreign `0.0.0.0` listener satisfies `enable` and the unit's start, and every launch then goes direct (F-03).

### Interaction: the port x `cloud_oauth`'s serve (T17's)
Both take 8080; the suite's case holds that the serve comes up on the LAN address with the proxy on loopback. F-01's answer is readable to a web page only by DNS rebinding (F-02), and the sign-in window opens a provider's page only.

### Interaction: the store x `backuptool` (T17's)
`/storage/.config/raofflineproxy/` is a DEVICEONLYDIRS entry: the store, the token row and the queue never travel in a settings backup; the toggle in `system.cfg` does, and `daemons/006` re-derives the marker at boot.

### Interaction: the service x RetroArch's command patch (T3's #825)
With the toggle on, an achievement's title and description reach RetroArch from this store; T3's PL-032 is that patch's half. Nothing here changes it.

### Interaction: M7's open work on these files
None read: M7's worktrees are not this lane's (the brief's § 1).



## The first reader's 04-analysis.md (whole)

# Analysis — M6.P2 T19, the offline achievements proxy (#666)

## Executive summary

The proxy is in good order where the fork has worked it hardest: every answer the interface acts on fails closed (`cannot_tell`, `added=unknown`), the stamps are written whole, the enable and disable undo themselves, and the integration test (12 OK) and the scripts suite (1,379 PASS) hold the preparation and the ctl's verbs. The eighteen patches apply to their pin at fuzz 0.

What the read found, in the brief's four families:

- **Where a credential travels.** The port answers a login naming the account, while upstream cannot be reached, with the cached sign-in body and its session token, comparing no password or token (F-01, upstream code). On this device every local process is root and could read `system.cfg`'s token anyway; the reach the port adds is a web page shown on the device, by DNS rebinding, since the service checks neither `Host` nor `Origin` (F-02). The username rides `python3`'s argv at four sites against the file's own rule (F-05).
- **What runs as root on an unauthenticated port.** The unit carries no hardening directive (F-04), and the ctl's readiness check takes any listener on `0.0.0.0:8080`, so a foreign one turns the toggle on while every launch goes direct (F-03).
- **A check whose failure reads as success.** The scan lock that cannot be opened reads as nothing running (F-06); a stamp that could not be written is not seen (F-07); an unreadable ready count prints 0 (F-16); one undecodable ROM name fails the whole listing, reproduced on the host (F-17).
- **A bound that is not enforced.** The scan has none, by design (F-11); the top-up's played check trusts the mark's mtime (F-12); the IDAT inflate and the lookup threads are unbounded (F-13); `http_post` marks no 429 pause (F-14, upstream).

Six are proposed as Low `bug`s (F-01, F-03, F-06, F-07, F-16, F-17); nineteen are Info. Five of the six fell on the guest as read (F-01, F-03, F-06, F-16, F-17), and F-17 on the host too; F-12 fell as well. Nothing is Medium or above: the port is loopback, the device is single-user and root, and no finding loses an award or a save.

## Acceptance-criteria scorecard

The brief's § 7 against this folder at stage C's start:

| Criterion | State |
| --- | --- |
| `00` to `05` | `00` to `04` written; `05` at stage C's end |
| the lint | pre-issue at stage C's end |
| `review-plan.json`, the four provenance files, the manifest | stage C |
| the punch-list issue | stage D |
| `reviewed-at`, `fixed-at`; nothing under `packages/`, `projects/`, `tools/` | R17 empty at stages A and B |
| `01` § Scope | written (`01`) |
| § Coverage 27 | 27 |
| § The listener | written; the user (`root`) and the bind (`127.0.0.1:8080`) read from the guest |
| § The credential's paths | written |
| § The writers, generated | 77 rows, `tools/t19-writers.py`, its drift control |
| § The patches, 18 | 18 |
| § The bounds | written |
| § The runs | written (R0 to R17, the unpack, the integration test, the suite, the generator) |
| § The guest cycle | written: START 12:43:49, RETURN 12:53:37 UTC; the image's scripts are M7's, so the tree's ran from `/storage/t19/bin/` |
| `00`'s closing census | at hand-back |
| `04` Q1 to Q8 | below |
| `proved:`, `question:`, § What T20 inherits | written in `02`; `question:` in `05` |
| the retro | stage G |
| the five checkers | before each push |

## Risk assessment

| Severity | Count | Findings |
| --- | ---: | --- |
| High | 0 | |
| Medium | 0 | |
| Low | 6 | F-01, F-03, F-06, F-07, F-16, F-17 |
| Info | 19 | F-02, F-04, F-05, F-08 to F-15, F-18 to F-25 |
| **Total** | **25** | |

The Low six share one shape: a state the device can be in -- a link down, a second listener, a full card, a lock or export that cannot be opened, a file name from an archive -- where the code's answer is wrong and nothing says so.

## Coverage boundary

- **Read:** the 27 whole at `8ebaf8daad`; the patched pin's request path, offline login, `auth`, `log_uploader`, `usage_report`, `storage` initialisation, `es_export`, `network` GET and POST; the interface's parsers at `16dbac5211`; the context files in `01`.
- **Not read, and why:** the rest of the upstream client (the menu, the queue internals, `rvz_datasource.py` beyond patch 020's hunk) -- upstream's, outside the four families; the rcheevos and libchdr sources -- T3's and the siblings' pins only; the per-emulator token files -- T30's.
- **Not run on the host:** the ctl outside `last-good-scripts-test`'s `bwrap`, the service, any network call. The guest's facts are in `02` § The guest cycle: the image's scripts are M7's, so `8ebaf8daad`'s four ran from `/storage/t19/bin/` against the image's client and service; the award proof could not run (the QA account's reachable achievements are spent, D-RA-006).

## Q1 The listener

Bound to `127.0.0.1:8080` by the client's default (`config.py:376-377`), AF_INET only; no `Host` or `Origin` check and no CORS header (`02` § The listener). Without identity it answers the store's game data, unlocks and badges, and -- while upstream cannot be reached -- a login naming the account with the cached sign-in and its token (F-01, F-02). The unit runs the service as root with the defaults (F-04). The readiness check takes a foreign `0.0.0.0` listener (F-03); `setsettings.sh` does not, so the two disagree. `cloud_oauth`'s serve shares the port on the LAN address (T17's).

## Q2 The credential's paths

The password and the token stay in `system.cfg` and the store; the ctl reads them for presence only. The username reaches argv at four sites (F-05) and the environment at one. The service's request log and the upload bundle redact `t=` and `p=` (`utils.py:110-124`); the bundle carries the account name and goes only on `upload_logs` being JSON `true` at the one automatic caller (patch 008); the usage report sends a salted hash of the name, only on consent (`usage_report.py:47-50`, `:180`). The port serves the token (F-01). `scan.log` takes the helpers' exception text; no credential-bearing message was found in the client's errors (`02` § The credential's paths).

## Q3 The writers

77 writing statements (`02` § The writers, generated). No script sets a mode; each file takes its writer's umask, read on the guest. Temp and rename everywhere a reader may race, except `verify-cursor` (F-09); `write_stamp`'s status ignored (F-07); the scan lock fails open (F-06); the fifo by name then object (F-10); the store written through `Storage()` by the listing (F-08); `es_export` writes `cached_game_ids.txt` by temp and `os.replace` (`es_export.py:58-69`).

## Q4 The bounds

`02` § The bounds, one row each. Enforced: the probe schedule, the stop wait, three in a row, the half hour, the top-up's 900 s, the image pass's 300 s, the refresh's 960 s, the badge wait, the batch cooldown. Not enforced: the scan's (F-11, by design: a foreground page with CANCEL, D-UI-078), the mark's write and its clock (F-12), the IDAT inflate and the lookup threads (F-13), the POST 429 pause (F-14). A kill is told from a result by its exit; an unreadable result is not (F-15).

## Q5 The patches

Eighteen, all absent from the pin and applying at fuzz 0: eleven fixes, six features, one identity (`02` § The patches). Ten have drafts, all on bases older than the pin; eight have none (F-22). The recipe's *"16 patches"* is the previous pin's count (F-21). A pin refresh (D-WORKFLOW-162): the cache holds fourteen revisions, the newest by date the pin's; what upstream did after `c7ebd1b6e7` is not readable without a fetch, so T19's answer is the procedure -- the integration test with the old pin as predecessor, `rc-preflight --only proxy-schema`, the suite -- and `NOT READ` for the upstream's later commits.

## Q6 What a failure reads as

`count_ready` prints 0 (F-16); one name fails the listing (F-17, reproduced); two usage exits (F-18); the refresh's `note()` on stdout and its `done` field (F-19, no reader); the recently played pass's `0 0 0` (F-15); the page's `have_account` comment (F-20).

## Q7 The protocol the interface reads

`02` § What T20 inherits: four producers, three on the `>>> ` protocol and `cache-indexed` on `OK`/`FAIL`/`DONE`; the stamps' shapes on both sides; the exit codes; the why tokens against `scanWhy`, which keeps a row for a token gone (F-20). T20 inherits the table, not an edit.

## Q8 The harness

`02` § The runs and the Positives table. `rc-preflight --only proxy-schema` is a comment check (F-23). `last-good-scripts-test` runs the real ctl in `bwrap` with shims; `raofflineproxy-integration-test` runs the shipped helper against the patched pin with a predecessor from the cache; the installed-native, consent and award tests are the guest's. The constructed positives: F-17's on the host (`tools/t19-listing-fixture.py`) and the guest; F-01, F-03, F-06, F-12 and F-16's on the guest. All six fell as read (`02` § Positives). The native test ran 18 with 4 failures on the image's M7 client (a lead outside the slice); the consent test passed 30 checks with no NIC; `ra-offline-test` could not run (D-RA-006).

## Second opinion

Phase 4.6 at Extended depth, two seats over one trimmed, scanned packet: GPT-6 Astra at `max`, then Gemini 4 Argon at `high` with the lane's grades of Astra. Not run yet; this section takes the plan, the provenance and every item's grade at stage C.

## Finding Verification

Each finding was read at its lines (`stage-b/reading-notes.md`); F-17 is reproduced by a fixture. The seats' refutations are graded against these at stage C.

## Renovation face

### Q1 Modernize
The two readers' parser is one (`CloudText`); the ctl's embedded python blocks (seven by word) are the shape a helper file would hold with a test of its own. F-08 is where the seam leaks.

### Q2 Standards
The temp-and-rename rule (D-CLOUD-078) holds but for F-09 and F-07; the credential rule holds but for F-05; guards fail closed but for F-06 and F-16.

### Q3 Bugs
F-01, F-03, F-06, F-07, F-16, F-17 (proposed Low).

### Q4 Package currency
The pin `c7ebd1b6e7` is upstream main at 2026-10-11 (the recipe's own comment); the siblings follow its submodules (F-21); later upstream commits are not read here (no fetch).

### Q5 Efficiency
F-13's unbounded inflate and threads; F-14's unpaced POSTs after a 429. The scan's listing parses each set row's head (`head_game_id`), not its body.

### Q6 Dead ends
`scanWhy`'s `NO_GAMES_FOUND` (F-20); the `refresh` and `images` verbs with no interface caller (F-19); the menu module shipped and never drawn (`package.mk:121-124` removes its fonts and images, not the module).

### Q7 Clarity and structure
The recipe's comment (F-21); `count_ready`'s comment against its code (F-16); the refresh's two meanings of `done` (F-19).

## Instruction File Recommendations

### Coverage gaps (would have prevented)
- A scan of a loopback service's request path for an answer that carries a credential to a caller that proved none (F-01) belongs beside the read filter in `engineering-practices.md`.

### Codification gaps (proposals for the coordinator)
- `last-good-scripts-test`'s bubblewrap shape for the ctl is the way to run a fork script on the host; the brief's "never on the host" could name it.

## Quality self-check

- Every finding cites lines at `8ebaf8daad` or the patched pin; one claim corrected before it was committed (`03`'s routing sentence: `setsettings.sh` checks `127.0.0.1:8080` only).
- No credential value was read: the store, `system.cfg` and the QA account file are unread; the scan of the reading notes for a credential-shaped value found 0.
- The severities are proposals for the stage-D ruling.



## Context 1: docs/reviews/order.md § T19

```text
### T19. offline-achievements: the offline achievements proxy

- **id**: `offline-achievements`; **kind**: read; **lens**: security, new functionality
- **why here**: a network listener holding the player's account token, all fork-own (+3,666), and the cheapest product area to finish; its 18 fork-written patches to the upstream proxy are read here, not in the patch tables (pass 6)
- **paths** (27 paths, 5,369 lines, 3,656 read, of which 3,656 fork-own; 1,703 patch and config lines; reach shipped 27): areas `offline-achievements`; globs `(all)` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/packages/network/raofflineproxy*/**`
- **read before**: none
- **depth**: Extended -- a network listener and an account credential (plan § 6c)
- **interacting subsystems** (read-only context): `ProxyCards` and the RetroAchievements pages (ES); RetroArch's `rcheevos` path; #585's upstream queue
- **closing evidence**: audit folder, lint PASS, `tools/ra-offline-test` and the proxy's suites on the VM, punch list through Phase 7, `reviewed-at` and `fixed-at` set

```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-refresh @ 8ebaf8daad (whole, 232 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # raofflineproxy-refresh -- re-read a game's RetroAchievements state now.
    6  #
    7  # The service already re-reads, each online hour while the proxy is idle,
    8  # the patch, unlocks and session of every cached game played in the last
    9  # seven days (upstream 59b167c; D-RA-029). That covers the ordinary case and
   10  # needs nobody's attention. It does not cover the case a player is standing
   11  # in front of: they have just reset an achievement on retroachievements.org,
   12  # or earned one on another device, and they want to play this game offline in
   13  # five minutes -- possibly a game they have not played this week.
   14  #
   15  #   raofflineproxy-refresh --game <id>     one game
   16  #   raofflineproxy-refresh --all           every cached game
   17  #   raofflineproxy-refresh                 what the service's pass would take now
   18  #
   19  # It is the same work the service's own pass does -- refresh_game_patch for
   20  # the set and its images, then cache_unlocks for what the player has earned --
   21  # run when asked instead of when due. Both, because the names mislead: the
   22  # "patch" refresh does not touch unlocks. Nothing here
   23  # changes what a pass is allowed to do: the client's own throttle, batch
   24  # cooldown and 429 backoff still pace every request, and the run is bounded
   25  # by --seconds so a player who asks for 500 games does not wait forever.
   26  #
   27  # Refuses while offline: a refresh is a conversation with the server, and
   28  # there is nothing useful to do without one. Speaks the ctl's `>>> ` protocol
   29  # so the interface can show progress (fork maxengel/rocknix#223).
   30  
   31  from __future__ import annotations
   32  
   33  import argparse
   34  import json
   35  import sys
   36  import time
   37  
   38  from raofflineproxy import cache_keys
   39  from raofflineproxy.auth import resolve_credentials
   40  from raofflineproxy.config import configure_logging, load_config
   41  from raofflineproxy.storage import Storage
   42  from raofflineproxy.utils import proxy_user_agent, self_user_agent
   43  import raofflineproxy.proxy_service as proxy_service
   44  
   45  
   46  def tell(text: str) -> None:
   47      print(f">>> {text}", flush=True)
   48  
   49  
   50  def note(text: str) -> None:
   51      print(text, flush=True)
   52  
   53  
   54  def cached_games(storage: Storage) -> list[str]:
   55      """Patch keys only, matching upstream's refresh scope without loading bodies."""
   56      return storage.cache_keys_by_prefix(cache_keys.PREFIX_PATCH)
   57  
   58  
   59  def game_ids(keys: list[str]) -> list[int]:
   60      return sorted({gid for key in keys
   61                     if (gid := cache_keys.parse_game_id_from_patch_key(key)) is not None})
   62  
   63  
   64  def drop_startsession(storage: Storage, game_id: int) -> int:
   65      """Remove the cached session response for a game. Returns rows removed.
   66  
   67      Raises when a row could not be removed: the session response carries the
   68      player's unlocks, so a refresh that leaves a stale one has not done its
   69      job, and the game is counted failed rather than re-read (#307 PL-058 --
   70      the same shape as 2026-09-19, when this helper reported half its work as
   71      all of it)."""
   72      removed = 0
   73      prefix = f"{cache_keys.PREFIX_STARTSESSION}{game_id}:"
   74      try:
   75          for key in storage.cache_keys_by_prefix(prefix):
   76              if key.startswith(prefix):
   77                  storage.delete_cache(key)
   78                  removed += 1
   79      except Exception as exc:
   80          raise RuntimeError(f"the startsession row could not be dropped ({exc})") from exc
   81      return removed
   82  
   83  
   84  def row_ages(storage: Storage, game_id: int) -> str:
   85      """The four per-game rows and their ages, so staleness is visible."""
   86      now_ms = int(time.time() * 1000)
   87      ages = []
   88      # achievementsets is keyed by the ROM's hash, not by the game id, so it
   89      # cannot be looked up from here; saying "none" for it would be a false
   90      # statement about a row that exists. It is named and left unchecked.
   91      for prefix in (cache_keys.PREFIX_PATCH,
   92                     cache_keys.PREFIX_UNLOCKS, cache_keys.PREFIX_STARTSESSION):
   93          try:
   94              rows = [r for r in storage.cache_summaries_by_prefix(prefix)
   95                      if f":{game_id}:" in f":{str(r.get('cacheKey') or '')}:"
   96                      or str(r.get("cacheKey") or "").startswith(f"{prefix}{game_id}:")]
   97          except Exception:
   98              rows = []
   99          if not rows:
  100              ages.append(f"{prefix.rstrip(':')}=none")
  101              continue
  102          try:
  103              stamp = max(int(row.get("cachedAt") or 0) for row in rows)
  104              stamp = stamp // 1000 if stamp > 1e11 else stamp
  105              ages.append(f"{prefix.rstrip(':')}={max(0, now_ms // 1000 - stamp)}s")
  106          except Exception:
  107              ages.append(f"{prefix.rstrip(':')}=?")
  108      ages.append("achievementsets=hash-keyed, not checked here")
  109      return " ".join(ages)
  110  
  111  
  112  def main() -> int:
  113      parser = argparse.ArgumentParser(add_help=True)
  114      parser.add_argument("--game", type=int, help="one game id")
  115      parser.add_argument("--all", action="store_true", help="every cached game")
  116      parser.add_argument("--seconds", type=float, default=300.0)
  117      args = parser.parse_args()
  118  
  119      configure_logging()
  120      config_data = load_config()
  121  
  122      tell("doing refresh")
  123      try:
  124          storage = Storage()
  125      except Exception as exc:
  126          note(f"the store could not be opened: {exc}")
  127          tell("why STORE_UNREADABLE")
  128          return 2
  129      try:
  130          credentials = resolve_credentials(storage, config_data, self_user_agent())
  131      except Exception as exc:
  132          note(f"no account to refresh as: {exc}")
  133          tell("why NO_ACCOUNT")
  134          return 2
  135      user_agent = proxy_user_agent(self_user_agent())
  136  
  137      rows = cached_games(storage)
  138      if args.game:
  139          wanted = [args.game]
  140      elif args.all:
  141          wanted = game_ids(rows)
  142      else:
  143          # Exactly what the service's pass would take, so this is also a way
  144          # to make the next pass's work happen now.
  145          played = proxy_service.load_recently_played_game_ids(
  146              storage, int(time.time() * 1000) - proxy_service.REFRESH_PLAYED_WINDOW_MS
  147          )
  148          wanted = proxy_service.due_refresh_game_ids(rows, played)
  149      if not wanted:
  150          note(f"nothing is due; no cached game was played in the last "
  151               f"{proxy_service.REFRESH_PLAYED_WINDOW_DAYS} days")
  152          tell("note NOTHING_DUE")
  153          tell("done 0|0")
  154          return 0
  155  
  156      note(f"{len(wanted)} game(s) to re-read, from {len(rows)} cached")
  157      tell(f"total {len(wanted)}")
  158      deadline = time.monotonic() + max(1.0, args.seconds)
  159      done = 0
  160      failed = 0
  161      # Failures in a row, reset by a game that goes through: three unrelated
  162      # failures across a long --all are not the server refusing, and the
  163      # message says "in a row" (#308 F-RA-12, F-RA-19). failed stays the total.
  164      in_a_row = 0
  165      for index, gid in enumerate(wanted, 1):
  166          if time.monotonic() > deadline:
  167              left = len(wanted) - done - failed
  168              note(f"stopped at the {args.seconds:.0f}s ceiling; {left} game(s) left")
  169              tell(f"note LEFT {left}")
  170              tell(f"done {done}|{left}")
  171              return 1
  172          try:
  173              answer = proxy_service.refresh_game_patch(
  174                  gid, credentials, user_agent, storage, config_data
  175              )
  176              # The patch is only half of it. refresh_game_patch re-reads the
  177              # set; the player's unlocks are a separate call, and a refresh
  178              # that skips it reports success while leaving the device
  179              # believing in achievements the site no longer holds -- which is
  180              # exactly what it did on the RG SP on 2026-09-19, after two
  181              # achievements were reset on the site: patch 28 s old, unlocks
  182              # 87,168 s old, and the two still reading as earned.
  183              proxy_service.cache_unlocks(
  184                  gid, credentials, user_agent, config_data, storage
  185              )
  186              # And the third row. A game has four cached rows -- patch,
  187              # achievementsets, unlocks and startsession -- and startsession
  188              # carries the player's unlocks *inside the session response*, so
  189              # a stale one tells RetroArch at launch that achievements are
  190              # already earned however fresh `unlocks` is. That is exactly what
  191              # happened on the RG SP on 2026-09-19: two achievements reset on
  192              # the site, patch and unlocks refreshed, and the game still
  193              # announced both as unlocked from a startsession row two days old.
  194              #
  195              # It is deleted rather than re-fetched because there is nothing to
  196              # fetch outside a real session, and deleting is safe: proved on
  197              # guest d, an offline launch with no cached startsession loads the
  198              # game and reports the right count, because the proxy rebuilds the
  199              # session from the unlocks row (build_unlocks_array).
  200              dropped = drop_startsession(storage, gid)
  201              done += 1
  202              in_a_row = 0
  203              # It is documented as returning the title and returns the patch
  204              # body, so take the title out of it rather than printing a page
  205              # of JSON into the ctl's output.
  206              title = ""
  207              if answer:
  208                  try:
  209                      title = (json.loads(answer).get("PatchData") or {}).get("Title") or ""
  210                  except Exception:
  211                      title = str(answer)[:40]
  212              note(f"re-read {index}/{len(wanted)}: game {gid}" + (f" '{title}'" if title else "")
  213                   + (f"; dropped {dropped} startsession row(s)" if dropped else "")
  214                   + f"; {row_ages(storage, gid)}")
  215              tell(f"refresh {index}|{len(wanted)}")
  216          except Exception as exc:
  217              failed += 1
  218              in_a_row += 1
  219              note(f"game {gid}: {exc}")
  220              if in_a_row >= 3:
  221                  note("three failures in a row; stopping rather than hammering")
  222                  tell("why REPEATED_FAILURES")
  223                  tell(f"done {done}|{len(wanted) - done}")
  224                  return 1
  225  
  226      note(f"re-read {done} game(s), {failed} failed")
  227      tell(f"done {done}|{failed}")
  228      return 1 if failed else 0
  229  
  230  
  231  if __name__ == "__main__":
  232      sys.exit(main())
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed @ 8ebaf8daad (whole, 222 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # raofflineproxy-cache-indexed - cache games for offline achievements from a
    6  # job list raofflineproxy-ctl writes, one game per line (fork #184 note 5b,
    7  # D-RA-013):
    8  #
    9  #   I<TAB><gameId><TAB><hash><TAB><path>   a game the interface's own index
   10  #                                          already identified: cached from
   11  #                                          the id and the hash, the ROM is
   12  #                                          never read
   13  #   H<TAB><TAB><TAB><path>                 a game with no index entry: the
   14  #                                          client's own add_rom_to_cache
   15  #                                          (hash the ROM, ask RetroAchievements
   16  #                                          which game it is, cache it)
   17  #
   18  # It speaks cache-roms' lines on stdout so the ctl's reader is unchanged --
   19  # "OK <i>/<n> <file>", "FAIL <i>/<n> <file>: <reason>", "DONE cached=<c>
   20  # failed=<f> indexed=<i>" (the last field is how many of the cached came
   21  # from the index) -- and says on stderr, per game, which RetroAchievements
   22  # actions it asked, so the scan log shows an indexed game costing patch,
   23  # unlocks and achievementsets and never gameid. The client's own courtesies
   24  # stay: its throttle between requests, its cooldown per batch, its backoff
   25  # on 429 (network.py), and its redaction of the token in what it logs.
   26  #
   27  # An indexed game is cached the way add_rom_to_cache would have cached it
   28  # after the lookup: cache_game (the patch by id, the player's unlocks, the
   29  # achievement sets by hash, a session), the gameid alias for the hash (a
   30  # RetroArch that asks gameid before patch is answered offline), and the ROM's
   31  # path on the patch row (the client's browser and the ctl's own walk read it
   32  # as "already cached"). Nothing here prints a value from system.cfg; the
   33  # credentials pass through the client's resolve_credentials and no further.
   34  from __future__ import annotations
   35  
   36  import json
   37  import os
   38  import sys
   39  import threading
   40  import time
   41  from pathlib import Path
   42  
   43  from raofflineproxy import cache_budget, cache_keys, image_cache, network, rate_limit, rom_browser, rom_cache
   44  from raofflineproxy.auth import resolve_credentials
   45  from raofflineproxy.config import configure_logging, image_caching_enabled, load_config
   46  from raofflineproxy.rom_browser import add_rom_to_cache, normalize_cached_rom_path
   47  from raofflineproxy.rom_cache import cache_game
   48  from raofflineproxy.storage import Storage, current_millis
   49  from raofflineproxy.utils import proxy_user_agent, self_user_agent
   50  
   51  # Every RetroAchievements action a game cost, in order. http_get is bound by
   52  # name in the two modules that call it, so both names are wrapped.
   53  ASKED: list[str] = []
   54  _real_http_get = network.http_get
   55  
   56  
   57  def _counting_http_get(url: str, user_agent: str) -> str:
   58      ASKED.append(network.api_action_from_url(url) or "?")
   59      return _real_http_get(url, user_agent)
   60  
   61  
   62  network.http_get = _counting_http_get
   63  rom_browser.http_get = _counting_http_get
   64  rom_cache.http_get = _counting_http_get
   65  
   66  
   67  def note(text: str) -> None:
   68      print(text, file=sys.stderr, flush=True)
   69  
   70  
   71  def apply_scan_batch_cooldown(scanned: int) -> bool:
   72      # Upstream removed this helper when its background queue adopted pacing.
   73      # Keep the deliberate OS preparation command's existing 50-game/30-second
   74      # cadence; upstream request throttling and persisted 429 pauses still apply.
   75      if scanned > 0 and scanned % 50 == 0:
   76          note(f"Scan batch cooldown after {scanned} scanned, sleeping 30s")
   77          time.sleep(30.0)
   78          return True
   79      return False
   80  
   81  
   82  def wait_for_badges(seconds: float) -> None:
   83      """The badge images the games queued are still coming down in image_cache's
   84      pool, whose workers are not daemon threads: left alone, the process would
   85      live until the last one landed -- on the RG SP 83 s past its DONE, until
   86      the ctl's bound killed it and read the kill as the verdict (fork #188).
   87      Give them `seconds`, then drop what has not started (the games are cached
   88      either way; a badge that did not come is fetched when a page asks for it
   89      online, and offline the page shows the blank it already tolerates)."""
   90      waiter = threading.Thread(target=lambda: image_cache._image_download_executor.shutdown(wait=True), daemon=True)
   91      waiter.start()
   92      waiter.join(timeout=max(0.0, seconds))
   93      if waiter.is_alive():
   94          note(f"badge downloads still running after {int(seconds)} s; the rest are dropped (fetched when a page asks for them online)")
   95          image_cache.shutdown_image_downloads()
   96  
   97  
   98  def cache_indexed(game_id: int, hash_value: str, path: Path, credentials: dict,
   99                    storage: Storage, config_data: dict) -> str:
  100      """Cache one game from its id and hash. Returns the title cached."""
  101      hash_value = cache_keys.normalize_hash(hash_value)
  102      user_agent = proxy_user_agent(self_user_agent())
  103      paused = max(rate_limit.paused_until() or 0, cache_budget.load(storage).paused_until)
  104      if paused > current_millis():
  105          raise rate_limit.RateLimitedError("RetroAchievements asked to slow down; try again later")
  106      try:
  107          with rate_limit.background():
  108              cache_game(
  109                  game_id,
  110                  hash_value,
  111                  credentials,
  112                  user_agent,
  113                  storage,
  114                  config_data,
  115                  cache_images=image_caching_enabled(config_data),
  116              )
  117      finally:
  118          paused = rate_limit.paused_until()
  119          if paused is not None:
  120              cache_budget.pause_until(storage, paused)
  121      storage.upsert_cache(
  122          cache_keys.game_id(hash_value),
  123          json.dumps({"GameID": game_id}, separators=(",", ":")),
  124      )
  125      patch_key = cache_keys.patch(game_id, credentials["user"])
  126      patch_entry = storage.get_cache(patch_key)
  127      if patch_entry is None:
  128          raise rom_cache.CacheGameError("patch data was not stored")
  129      storage.upsert_cache(
  130          patch_key,
  131          patch_entry["responseBody"],
  132          source_rom_path=normalize_cached_rom_path(path),
  133      )
  134      try:
  135          title = (json.loads(patch_entry["responseBody"]).get("PatchData") or {}).get("Title")
  136      except Exception:
  137          title = None
  138      return title or f"Game {game_id}"
  139  
  140  
  141  def main() -> int:
  142      if len(sys.argv) != 2:
  143          print("usage: raofflineproxy-cache-indexed <jobs-file>", file=sys.stderr)
  144          return 2
  145      configure_logging()
  146      config_data = load_config()
  147  
  148      jobs: list[tuple[str, int, str, Path]] = []
  149      for raw in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
  150          if not raw.strip():
  151              continue
  152          fields = raw.split("\t", 3)
  153          if len(fields) != 4 or fields[0] not in ("I", "H"):
  154              note(f"job line not understood, skipped: {raw[:80]}")
  155              continue
  156          kind, game_id, hash_value, path = fields
  157          try:
  158              jobs.append((kind, int(game_id) if game_id else 0, hash_value.strip(), Path(path)))
  159          except ValueError:
  160              note(f"job line not understood, skipped: {raw[:80]}")
  161      if not jobs:
  162          print("DONE cached=0 failed=0 indexed=0", flush=True)
  163          return 0
  164  
  165      cached = failed = indexed = 0
  166      total = len(jobs)
  167      storage = Storage()
  168      try:
  169          # Once, before the first game: the same source the client itself
  170          # reads (a token from system.cfg, else the proxy's cached sign-in,
  171          # else a sign-in from the password). None is the client's own
  172          # "login required", said on every line as cache-roms says it.
  173          credentials = resolve_credentials(storage, config_data, self_user_agent())
  174          for index, (kind, game_id, hash_value, path) in enumerate(jobs, start=1):
  175              apply_scan_batch_cooldown(index - 1)
  176              label = path.name
  177              ASKED.clear()
  178              if credentials is None:
  179                  failed += 1
  180                  print(f"FAIL {index}/{total} {label}: RetroAchievements login required", flush=True)
  181                  continue
  182              if kind == "I" and game_id > 0 and hash_value:
  183                  try:
  184                      title = cache_indexed(game_id, hash_value, path, credentials, storage, config_data)
  185                  except Exception as error:
  186                      failed += 1
  187                      print(f"FAIL {index}/{total} {label}: {error}", flush=True)
  188                      note(f"indexed {index}/{total} {label}: game {game_id} could not be cached; asked {','.join(ASKED) or 'nothing'}")
  189                      continue
  190                  cached += 1
  191                  indexed += 1
  192                  print(f"OK {index}/{total} {label}", flush=True)
  193                  note(f"indexed {index}/{total} {label}: game {game_id} '{title}' cached from the index, hash reused, not hashed; asked {','.join(ASKED) or 'nothing'}")
  194                  continue
  195  
  196              if not path.is_file():
  197                  failed += 1
  198                  print(f"FAIL {index}/{total} {label}: not found", flush=True)
  199                  continue
  200              try:
  201                  result = add_rom_to_cache(path, storage, config_data, budgeted=False)
  202              except Exception as error:
  203                  failed += 1
  204                  print(f"FAIL {index}/{total} {label}: {error}", flush=True)
  205                  continue
  206              if result.success and not result.queued:
  207                  cached += 1
  208                  print(f"OK {index}/{total} {label}", flush=True)
  209              else:
  210                  failed += 1
  211                  print(f"FAIL {index}/{total} {label}: {result.message}", flush=True)
  212              note(f"hashed {index}/{total} {label}: no index entry, the ROM was hashed and looked up; asked {','.join(ASKED) or 'nothing'}")
  213      finally:
  214          storage.close()
  215  
  216      print(f"DONE cached={cached} failed={failed} indexed={indexed}", flush=True)
  217      wait_for_badges(float(os.environ.get("RAOFFLINEPROXY_IMAGE_WAIT", "120")))
  218      return 0
  219  
  220  
  221  if __name__ == "__main__":
  222      sys.exit(main())
```


## projects/ROCKNIX/packages/network/raofflineproxy/system.d/raofflineproxy.service @ 8ebaf8daad (whole, 46 lines)

```text
    1  [Unit]
    2  Description=RAOfflineProxy (offline RetroAchievements)
    3  # The marker is the off-switch, the way avahi's and sshd's are:
    4  # raofflineproxy-ctl enable writes it, disable removes it, and the boot-time
    5  # daemons pass re-derives it from global.retroachievements.offlineproxy in
    6  # system.cfg (fork #165).
    7  ConditionPathExists=/storage/.cache/services/raofflineproxy.conf
    8  # The proxy tolerates no network (that is its purpose); it only needs the
    9  # interface list and system.cfg to be in place. network-base.service by name,
   10  # as avahi does: network.target does not order after the units wanted by it.
   11  After=network.target network-base.service rocknix-sysconfig.service
   12  # Up -- listening, through ExecStartPost below -- before a game can be
   13  # launched, so an emulator's first RetroAchievements call finds the port
   14  # listening rather than refused: a refused connection makes rcheevos disable
   15  # achievements for the whole session.
   16  Before=emustation.service essway.service
   17  # Five starts, then no more: in [Unit], where systemd has read the start
   18  # limit since 230 (#308 F-RA-20). A failed start lasts the readiness wait
   19  # (ExecStartPost, 30 s) and RestartSec (5 s), so the interval has to hold
   20  # five of them -- at sixty seconds no more than two fit, the limit never
   21  # tripped, and a proxy that could never listen restarted for ever (audit of
   22  # the fixes, claude G-D-05). 5 x 35 = 175; three hundred leaves room.
   23  StartLimitIntervalSec=300
   24  StartLimitBurst=5
   25  
   26  [Service]
   27  Type=simple
   28  Environment=RAOFFLINEPROXY_CONFIG_DIR=/storage/.config/raofflineproxy
   29  Environment=HOME=/storage
   30  Environment=XDG_CONFIG_HOME=/storage/.config
   31  # Measured upstream on a 103 MB device: 32 -> 19 MB RSS.
   32  Environment=MALLOC_ARENA_MAX=2
   33  ExecStart=/usr/bin/python3 -m raofflineproxy.main run-service
   34  # Started means listening: Type=simple counts the service up the moment its
   35  # process forks, seconds before Python has bound the port on a handheld, and
   36  # enable routes the emulators to it as soon as `systemctl start` returns; a
   37  # launch meeting a refused connection loses achievements for its session.
   38  # Bounded at thirty looks a second apart; a proxy that never listens fails
   39  # the start, and enable puts the device back as it was (#308 F-RA-26).
   40  ExecStartPost=/usr/bin/raofflineproxy-ctl listening --wait 30
   41  Restart=on-failure
   42  RestartSec=5
   43  TimeoutStopSec=15
   44  
   45  [Install]
   46  WantedBy=multi-user.target
```


## projects/ROCKNIX/packages/network/raofflineproxy/daemons/006-raofflineproxy @ 8ebaf8daad (whole, 10 lines)

```text
    1  # Boot-time reconcile of the OFFLINE RETROACHIEVEMENTS toggle (fork #165):
    2  # 099-networkservices reads STATE, rewrites the marker the unit conditions
    3  # on and starts or stops the daemon. system.cfg is the record that travels
    4  # in a settings backup; the marker under /storage/.cache does not, so a
    5  # restored device with the toggle on gets its marker and its service back at
    6  # the next boot without being asked anything.
    7  STATE=$(get_setting global.retroachievements.offlineproxy)
    8  SVC="raofflineproxy"
    9  CONF="raofflineproxy.conf"
   10  DAEMONS=("raofflineproxy")
```


## projects/ROCKNIX/packages/network/raofflineproxy/patches/001-dorequest-4xx-passthrough.patch @ 8ebaf8daad (whole)

```text
proxy_service: pass a 4xx from dorequest.php through instead of answering 503

RetroAchievements answers a dorequest.php call it understood but cannot
satisfy with a 4xx whose body names the reason -- 404 with
{"Success":false,"Error":"Unknown game",...} for a hash that has no
achievement set, 400 for a malformed parameter. handle_online_request turned
every non-2xx into 503 {"Success":false,"Error":"upstream unavailable"}, so
an emulator behind the proxy reports "Load failed (-27): upstream
unavailable" for a ROM the server had in fact answered about, where the same
launch without the proxy reads "Load failed (-29): Unknown game". The player
is sent looking for a connection problem that does not exist, and the
message is false: upstream answered.

Pass a 4xx from dorequest.php through as it came, status and body, except
401 and 403. An auth failure keeps today's 503, so this change touches
nothing about how the proxy handles credentials (the login actions' cached
responses, the token the flusher carries). 5xx and network errors keep the
503 and the offline path as before; forward_to_upstream and the login and
award paths already passed an http_error through unchanged, so this brings
the general online path in line with them.

Seen on ROCKNIX (fork issue maxengel/rocknix#166) with the proxy at
64d03d30633ca6e7719c26d732cef3c97dedcc27: RetroArch through the proxy logged
"Load failed (-27): upstream unavailable" for a fixture ROM RA answered 404
for, and "Load failed (-29): Unknown game" without it. Offered upstream
as-is (ROCKNIX D-RA-002: whatever the fork changes in the proxy goes back).

diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
--- a/linux/raofflineproxy/proxy_service.py
+++ b/linux/raofflineproxy/proxy_service.py
@@ -84,6 +84,20 @@
 CACHE_QUEUE_POLL_SECONDS = 60
 WORKER_STOP_TIMEOUT_SECONDS = 5.0
 ALWAYS_TRY_UPSTREAM_ACTIONS = {"login", "login2"}
+# A 4xx RetroAchievements sends for a dorequest.php call it understood but
+# cannot satisfy -- 404 "Unknown game" for a hash with no set, 400 for a bad
+# parameter -- carries the reason the emulator shows the player, and passes
+# through as it came. 401 and 403 do not: an auth failure keeps the 503, so
+# nothing about how credentials are handled changes here.
+AUTH_FAILURE_STATUSES = {401, 403}
+
+
+def is_passthrough_client_error(path: str, status: int) -> bool:
+    return (
+        path.startswith("/dorequest.php")
+        and 400 <= status < 500
+        and status not in AUTH_FAILURE_STATUSES
+    )
 
 
 def is_static_asset_request(path: str) -> bool:
@@ -528,6 +542,12 @@
             return self.handle_offline_request(path, raw_body, action)
 
         if upstream[0] != "success":
+            if upstream[0] == "http_error" and is_passthrough_client_error(
+                path, upstream[1]
+            ):
+                return raw_response_bytes(
+                    upstream[1], upstream[3], upstream[4], upstream[2]
+                )
             return error_json(503, "upstream unavailable")
 
         status_code = upstream[1]
```


## projects/ROCKNIX/packages/network/raofflineproxy/patches/007-cached-sign-in-of-the-configured-account.patch @ 8ebaf8daad (whole)

```text
auth: take a cached sign-in only when it is the configured account's

resolve_credentials tried a token, then the first login row in the store
(Storage.load_login_credentials: the first row with the login2:: prefix,
whoever's), then a password. A device that had signed in as one account
and now holds another's password with no token yet -- an OS that signs in
through its own interface and writes the token later, or a QA guest that
carries a test account and the developer's in turn -- kept caching,
refreshing and flushing as the first account for as long as its row was
not marked invalid (ROCKNIX audit #186 PL-23, the credential half).

When the configured password names an account, the cached row consulted
is that account's own (cache_keys.login(user)), and a row of any other
account is not a sign-in for this one; with no password configured the
first cached row is taken as before. The order of sources is otherwise
unchanged: a token wins, then the cache, then a fresh login2.

Written for ROCKNIX (fork issue maxengel/rocknix#186, PL-23). Offered
upstream as-is (ROCKNIX D-RA-016).

diff --git a/linux/raofflineproxy/auth.py b/linux/raofflineproxy/auth.py
index 2f1de88..aaa78d7 100644
--- a/linux/raofflineproxy/auth.py
+++ b/linux/raofflineproxy/auth.py
@@ -47,10 +47,6 @@ def resolve_credentials(
     if token_credentials is not None:
         return cache_token_credentials(storage, token_credentials)
 
-    cached = storage.load_login_credentials()
-    if cached is not None and not storage.is_token_invalid(cached["token"]):
-        return cached
-
     # spruce keeps its credentials in its own settings file and only copies them into
     # the RetroArch config when a game launches, so before the first launch that file is
     # the only source.
@@ -60,6 +56,23 @@ def resolve_credentials(
         or load_rocknix_system_password_credentials(rocknix_system_cfg)
         or load_spruce_credentials()
     )
+
+    # A cached sign-in is taken only when it is the configured account's.
+    # When a password names the account, the cached row looked up is that
+    # user's; the first login row in the store, whoever's it is, was what
+    # this returned before -- so a device that had signed in as one account
+    # and now holds another's password (and no token yet) kept caching,
+    # refreshing and flushing as the first.
+    expected_user = ""
+    if password_credentials is not None:
+        expected_user = cache_keys.normalize_user(str(password_credentials.get("user") or ""))
+    if expected_user:***
+        cached = load_cached_login_for(storage, expected_user)
+    else:
+        cached = storage.load_login_credentials()
+    if cached is not None and not storage.is_token_invalid(cached["token"]):
+        return cached
+
     if password_credentials is not None:
         refreshed = login_and_cache_token(
             storage, config_data, password_credentials, user_agent
@@ -70,6 +83,22 @@ def resolve_credentials(
     return cached
 
 
+def load_cached_login_for(storage: Storage, user:*** str) -> dict | None:
+    """The cached sign-in of one account, by its login row, or None."""
+    entry = storage.get_cache(cache_keys.login(user))
+    if entry is None:
+        return None
+    try:
+        payload = json.loads(entry["responseBody"])
+    except Exception:
+        return None
+    cached_user = payload.get("User")
+    token = payload.get("Token")
+    if not cached_user or not token:***
+        return None
+    return {"user": cached_user, "token": token}
+
+
 def cache_token_credentials(storage: Storage, credentials: dict) -> dict | None:
     user = credentials.get("user")
     token = credentials.get("token")
```


## projects/ROCKNIX/packages/network/raofflineproxy/patches/008-log-upload-opt-in.patch @ 8ebaf8daad (whole)

```text
proxy_service: send a storage-corruption report only where config opts in

After a data file is found corrupt and quarantined, retry_storage_
corruption_report uploads a log bundle to the project's endpoint at every
online start until one gets through -- from the service, with no one's
yes, at the one moment nobody is watching. On a handheld a power cut
mid-write is an ordinary evening, so the trigger is not rare; the bundle
is redacted (t=, p=) and carries the account name; and an OS that ships
the service under its own privacy terms cannot today keep the upload off
short of patching it out (ROCKNIX audit #186 PL-12; on the sqlite backend
the incident is recorded only by the JSON store today, so the path is
unreachable on ROCKNIX's image -- this is the guard for a client that
starts recording incidents for sqlite too).

config.py gains log_upload_enabled: true only when config.json carries
"upload_logs": true -- the JSON true and nothing else, since a consent
boundary is not Python's truthiness ("false", 1 and "yes" are not an
opt-in; ROCKNIX audit #308 F-RA-27) -- and the automatic retry returns
after one log line when it is off. The menu's own manual upload is a choice made on screen
and is not gated. Default off, so an OS integrating the service opts in
knowingly; the project's own bundle can set the key in the config it
ships.

Written for ROCKNIX (fork issue maxengel/rocknix#186, PL-12). Offered
upstream as-is (ROCKNIX D-RA-016), the default being the project's to
decide.

diff --git a/linux/raofflineproxy/config.py b/linux/raofflineproxy/config.py
index 12d2dfb..5cba299 100644
--- a/linux/raofflineproxy/config.py
+++ b/linux/raofflineproxy/config.py
@@ -332,6 +332,11 @@ def load_config() -> dict:
     return data
 
 
+def log_upload_enabled(config_data: dict | None = None) -> bool:
+    """Automatic log upload requires an explicit JSON true, never truthiness."""
+    return (config_data or {}).get("upload_logs") is True
+
+
 def image_caching_enabled(config_data: dict | None = None) -> bool:
     config_data = config_data or {}
     configured = config_data.get("cache_images")
diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
index a0199ad..9c0908d 100644
--- a/linux/raofflineproxy/proxy_service.py
+++ b/linux/raofflineproxy/proxy_service.py
@@ -22,6 +22,7 @@ from .config import (
     FALLBACK_USER_AGENT,
     RA_MEDIA_HOST,
     image_caching_enabled,
+    log_upload_enabled,
     proxy_host,
     proxy_port,
     upstream_host,
@@ -1271,7 +1272,7 @@ def due_refresh_game_ids(patch_entries: list[dict], recently_played: set[int]) -
     return due
 
 
-def retry_storage_corruption_report() -> None:
+def retry_storage_corruption_report(config_data: dict | None = None) -> None:
     # The menu only ever attempts this once (on first open after the incident) and shows
     # the user the outcome regardless of success, so it doesn't nag them again — if that
     # one attempt happened while offline, the report would otherwise never reach us. The
@@ -1279,6 +1280,9 @@ def retry_storage_corruption_report() -> None:
     incident = storage_corruption.load_incident()
     if incident is None or incident.get("reported"):
         return
+    if not log_upload_enabled(config_data):
+        LOGGER.info("Storage corruption report not sent: upload_logs is off")
+        return
     try:
         upload_id = log_uploader.report_storage_corruption(incident)
     except Exception as exc:
@@ -1321,7 +1325,7 @@ def run_proxy_service(
         save_online_state(initial_online)
         if initial_online:
             server.flush_pending_awards()
-            retry_storage_corruption_report()
+            retry_storage_corruption_report(config_data)
         connectivity_monitor.start()
         periodic_refresh.start()
         cache_queue_worker.start()

diff --git a/linux/tests/test_linux_storage_corruption_retry.py b/linux/tests/test_linux_storage_corruption_retry.py
--- a/linux/tests/test_linux_storage_corruption_retry.py
+++ b/linux/tests/test_linux_storage_corruption_retry.py
@@ -5,12 +5,28 @@
 
 
 class RetryStorageCorruptionReportTests(unittest.TestCase):
+    def test_automatic_upload_requires_explicit_true(self) -> None:
+        incident = {"reported": False, "upload_id": None}
+        for config in ({}, {"upload_logs": None}, {"upload_logs": False},
+                       {"upload_logs": 0}, {"upload_logs": 1},
+                       {"upload_logs": "false"}, {"upload_logs": "true"},
+                       {"upload_logs": "yes"}, None):
+            with (
+                self.subTest(config=config),
+                mock.patch.object(proxy_service.storage_corruption, "load_incident", return_value=incident),
+                mock.patch.object(proxy_service.log_uploader, "report_storage_corruption") as report,
+                mock.patch.object(proxy_service.storage_corruption, "mark_reported") as mark,
+            ):
+                proxy_service.retry_storage_corruption_report(config)
+                report.assert_not_called()
+                mark.assert_not_called()
+
     def test_noop_when_no_incident(self) -> None:
         with (
             mock.patch.object(proxy_service.storage_corruption, "load_incident", return_value=None),
             mock.patch.object(proxy_service.log_uploader, "report_storage_corruption") as report,
         ):
-            proxy_service.retry_storage_corruption_report()
+            proxy_service.retry_storage_corruption_report({"upload_logs": True})
 
         report.assert_not_called()
 
@@ -20,7 +36,7 @@
             mock.patch.object(proxy_service.storage_corruption, "load_incident", return_value=incident),
             mock.patch.object(proxy_service.log_uploader, "report_storage_corruption") as report,
         ):
-            proxy_service.retry_storage_corruption_report()
+            proxy_service.retry_storage_corruption_report({"upload_logs": True})
 
         report.assert_not_called()
 
@@ -33,7 +49,7 @@
             ),
             mock.patch.object(proxy_service.storage_corruption, "mark_reported") as mark_reported,
         ):
-            proxy_service.retry_storage_corruption_report()
+            proxy_service.retry_storage_corruption_report({"upload_logs": True})
 
         mark_reported.assert_called_once_with("abc123")
 
@@ -48,7 +64,7 @@
             ),
             mock.patch.object(proxy_service.storage_corruption, "mark_reported") as mark_reported,
         ):
-            proxy_service.retry_storage_corruption_report()
+            proxy_service.retry_storage_corruption_report({"upload_logs": True})
 
         mark_reported.assert_not_called()
 
```


## projects/ROCKNIX/packages/network/raofflineproxy/patches/011-offline-login-header.patch @ 8ebaf8daad (whole)

```text
proxy_service: say in the headers where an answer came from

An emulator behind this process cannot tell an answer from the store from
one that came from RetroAchievements: both arrive as 200 OK with the same
body, by design. So when the store answers a login because the link is
down, RetroArch's own toast reads "RetroAchievements: Logged in as
"<name>"." -- true, and misleading to a player who knows the Wi-Fi is off
and expects to be told something has changed (ROCKNIX fork #194, the RG SP,
2026-09-15). The login body cannot carry the fact: rcheevos takes the
account name straight from it and reads no other field the proxy could
mark.

Two response headers say it instead. `X-RA-Proxy: 1` is on every response
this process writes, online or offline -- a client can tell the proxy is
in the path. `X-RA-Offline: 1` is on the answer handle_offline_login gives,
a login served from the store because upstream could not be reached.
Nothing else changes: the status lines, the bodies and Content-Length are
as before, the login path is otherwise untouched, and a client that does
not look at the headers sees what it saw. RetroArch on ROCKNIX reads the
second header and says "(offline)" in its toast (patch
0013-cheevos-offline-proxy-toast in the fork's retroarch package).

Written for ROCKNIX (fork issue maxengel/rocknix#194). Offered upstream
as-is (ROCKNIX D-RA-002, D-RA-016: whatever the fork changes in the proxy
goes back); the headers are additive and cost a client nothing.

diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
--- a/linux/raofflineproxy/proxy_service.py
+++ b/linux/raofflineproxy/proxy_service.py
@@ -93,6 +93,14 @@
 # through as it came. 401 and 403 do not: an auth failure keeps the 503, so
 # nothing about how credentials are handled changes here.
 AUTH_FAILURE_STATUSES = {401, 403}
+# ROCKNIX (fork #194): two response headers say where an answer came from,
+# for an emulator that wants to tell the player. X-RA-Proxy: 1 is on every
+# response this process writes; X-RA-Offline: 1 is on a login the store
+# answered because upstream could not be reached. RetroArch's sign-in toast
+# can then read "(offline)" -- rcheevos takes the account name straight from
+# the login body, so there is no field in it the proxy could say this in.
+PROXY_HEADER = ("X-RA-Proxy", "1")
+OFFLINE_LOGIN_HEADER = ("X-RA-Offline", "1")
 
 
 def is_passthrough_client_error(path: str, status: int) -> bool:
@@ -161,16 +169,33 @@
     )
 
 
-def response_bytes(code: int, body: str, reason: str | None = None) -> bytes:
+def response_head(
+    code: int,
+    reason: str | None,
+    content_type: str,
+    content_length: int,
+    extra_headers: Sequence[tuple[str, str]] = (),
+) -> bytes:
+    reason_phrase = reason or canonical_reason_phrase(code)
+    lines = [
+        f"HTTP/1.1 {code} {reason_phrase}",
+        f"Content-Type: {content_type}",
+        f"Content-Length: {content_length}",
+        f"{PROXY_HEADER[0]}: {PROXY_HEADER[1]}",
+    ]
+    lines.extend(f"{name}: {value}" for name, value in extra_headers)
+    lines.append("Connection: close")
+    return ("\r\n".join(lines) + "\r\n\r\n").encode("utf-8")
+
+
+def response_bytes(
+    code: int,
+    body: str,
+    reason: str | None = None,
+    extra_headers: Sequence[tuple[str, str]] = (),
+) -> bytes:
     text = body.encode("utf-8")
-    reason_phrase = reason or canonical_reason_phrase(code)
-    head = (
-        f"HTTP/1.1 {code} {reason_phrase}\r\n"
-        f"Content-Type: application/json\r\n"
-        f"Content-Length: {len(text)}\r\n"
-        f"Connection: close\r\n\r\n"
-    ).encode("utf-8")
-    return head + text
+    return response_head(code, reason, "application/json", len(text), extra_headers) + text
 
 
 def raw_response_bytes(
@@ -178,20 +203,14 @@
     body: bytes,
     content_type: str | None,
     reason: str | None = None,
+    extra_headers: Sequence[tuple[str, str]] = (),
 ) -> bytes:
-    reason_phrase = reason or canonical_reason_phrase(code)
     mime_type = content_type or "application/octet-stream"
-    head = (
-        f"HTTP/1.1 {code} {reason_phrase}\r\n"
-        f"Content-Type: {mime_type}\r\n"
-        f"Content-Length: {len(body)}\r\n"
-        f"Connection: close\r\n\r\n"
-    ).encode("utf-8")
-    return head + body
-
-
-def ok_json(body: str) -> bytes:
-    return response_bytes(200, body, "OK")
+    return response_head(code, reason, mime_type, len(body), extra_headers) + body
+
+
+def ok_json(body: str, extra_headers: Sequence[tuple[str, str]] = ()) -> bytes:
+    return response_bytes(200, body, "OK", extra_headers)
 
 
 def error_json(code: int, message: str) -> bytes:
@@ -443,7 +462,9 @@
         if cached is None:
             return None
 
-        return ok_json(cached["responseBody"])
+        # The store's answer, given because upstream could not be reached:
+        # X-RA-Offline: 1 says so to a client that wants to tell the player.
+        return ok_json(cached["responseBody"], extra_headers=(OFFLINE_LOGIN_HEADER,))
 
     def handle_award_request(
         self, path: str, raw_body: str, headers: dict[str, str]
```


## projects/ROCKNIX/packages/network/raofflineproxy/patches/013-validate-a-cached-image-before-publishing-it.patch @ 8ebaf8daad (whole)

```text
image_cache: an image is published only when it is whole and is an image

download_static_image wrote response.read() to a temp file and renamed it
into place. The rename is atomic, so a killed process cannot publish half a
file -- but a short read can: nothing compared the bytes against the length
the server declared, so a connection that dropped mid-body was published
under the asset's real name, and from then on every existence check called
it cached. target.exists() here, resolve_cached_static_asset in the proxy,
and ROCKNIX's own image pass all test presence, never content, so a
truncated badge or icon stays in the cache until something deletes it by
hand -- and offline it is served, whole or not.

Two tests before the rename that makes the file the cache's answer: the
Content-Length the server declared, when it declared one, and for a .png
path png_problem -- the signature, every chunk's length and CRC up to and
including IEND, and IDAT data that inflates. The chunk walk ends at IEND
wherever it is, so a whole PNG an encoder followed with a few bytes is
whole (a trailer test in the last twelve bytes refused it at every fetch;
ROCKNIX audit #308 F-RA-13), and png_problem is a function of its own so
the same test can be put to a file already cached (ROCKNIX's image pass,
--verify; audit #308 F-RA-12). A body that fails either test is dropped
and the asset stays missing, which the callers already handle -- a miss is
re-requested while online and answered 404 at once while offline (ROCKNIX
patch 012). Nothing is retried here:
best-effort is this function's contract, and a missing asset is a state the
cache is allowed to be in, while a damaged one that claims to be cached is
not.

Checked on a ROCKNIX guest: a fixture that closes the connection after half
the body leaves no file where it used to leave a truncated PNG, and a
second pass fetches the asset whole.

Written for ROCKNIX (fork issue maxengel/rocknix#213). Offered upstream
as-is.

diff --git a/linux/raofflineproxy/image_cache.py b/linux/raofflineproxy/image_cache.py
index 64384c9..6378a23 100644
--- a/linux/raofflineproxy/image_cache.py
+++ b/linux/raofflineproxy/image_cache.py
@@ -208,7 +208,12 @@ def download_static_image(
             target.parent.mkdir(parents=True, exist_ok=True)
             tmp = target.with_name(f"{target.name}.{os.getpid()}.{threading.get_ident()}.tmp")
             try:
-                tmp.write_bytes(_fetch_image(url, user_agent))
+                payload = _fetch_image(url, user_agent)
+                if clean_path.lower().endswith(".png"):
+                    problem = png_problem(payload)
+                    if problem is not None:
+                        raise ValueError(problem)
+                tmp.write_bytes(payload)
                 os.replace(tmp, target)
                 tmp = None
             finally:
@@ -252,7 +257,11 @@ def _fetch_image(url: str, user_agent: str) -> bytes:
             _drop_thread_connection(parts.netloc)
         if response.status != _HTTP_OK:
             return _fetch_with_urllib(url, user_agent)
-        return body
+        try:
+            return _checked_image_body(response, body)
+        except ValueError:
+            _drop_thread_connection(parts.netloc)
+            raise
     raise OSError(f"could not fetch {url}")
 
 
@@ -263,7 +272,14 @@ def _fetch_with_urllib(url: str, user_agent: str) -> bytes:
         method="GET",
     )
     with urllib.request.urlopen(request, timeout=10, context=configured_ssl_context()) as response:
-        return response.read()
+        return _checked_image_body(response, response.read())
+
+
+def _checked_image_body(response, payload: bytes) -> bytes:
+    declared = response.getheader("Content-Length")
+    if declared is not None and declared.isdigit() and len(payload) != int(declared):
+        raise ValueError(f"short read: {len(payload)} of {declared} bytes")
+    return payload
 
 
 def _thread_connection(host: str) -> http.client.HTTPSConnection:
@@ -380,3 +396,43 @@ def delete_cached_images_for_game(game_id: int) -> None:
 def clear_all_cached_images() -> None:
     if IMAGE_CACHE_DIR.exists():
         shutil.rmtree(IMAGE_CACHE_DIR, ignore_errors=True)
+
+
+def png_problem(payload: bytes) -> str | None:
+    """Why payload is not a whole PNG, or None when it is.
+
+    The signature; every chunk's length and CRC, up to and including IEND;
+    and IDAT data that inflates. The frame alone -- signature and an IEND in
+    the last twelve bytes -- admitted a body whose image data was garbage
+    (ROCKNIX audit #258, the seat's G-01) and refused a whole PNG an encoder
+    had followed with a few bytes after its IEND, which readers ignore (audit
+    #308 F-RA-13): such a badge was dropped at every fetch and never cached.
+    So the chunk walk is the test, and it ends at IEND wherever IEND is. A
+    few microseconds per badge. One test for a download and for a file
+    already cached (ROCKNIX's raofflineproxy-cache-images --verify, #308
+    F-RA-12). Written for ROCKNIX (fork maxengel/rocknix#213).
+    """
+    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
+        return "not a PNG"
+    pos, idat, ended = 8, b"", False
+    while pos + 12 <= len(payload):
+        length = int.from_bytes(payload[pos:pos + 4], "big")
+        ctype = payload[pos + 4:pos + 8]
+        data = payload[pos + 8:pos + 8 + length]
+        crc = payload[pos + 8 + length:pos + 12 + length]
+        if len(data) != length or len(crc) != 4 or (zlib.crc32(ctype + data) & 0xFFFFFFFF) != int.from_bytes(crc, "big"):
+            return f"PNG chunk {ctype!r} fails its CRC"
+        if ctype == b"IDAT":
+            idat += data
+        pos += 12 + length
+        if ctype == b"IEND":
+            ended = True
+            break
+    if not ended:
+        return "no IEND: the PNG is cut short"
+    try:
+        zlib.decompress(idat)
+    except zlib.error as exc:
+        return f"PNG image data does not inflate: {exc}"
+    return None
+
diff --git a/linux/tests/test_linux_image_cache_shutdown.py b/linux/tests/test_linux_image_cache_shutdown.py
index ecd5dfe..91171e4 100644
--- a/linux/tests/test_linux_image_cache_shutdown.py
+++ b/linux/tests/test_linux_image_cache_shutdown.py
@@ -64,6 +64,9 @@ class ImageConnectionReuseTests(unittest.TestCase):
                 self.status = status
                 self.will_close = False
 
+            def getheader(self, _name):
+                return "3"
+
             def read(self) -> bytes:
                 return b"png"
 
@@ -173,7 +176,9 @@ class ShardedStaticImagesTests(unittest.TestCase):
     def test_a_download_lands_in_its_shard_folder(self) -> None:
         from unittest import mock
 
-        with mock.patch.object(self.image_cache, "_fetch_image", return_value=b"png"):
+        # This test isolates sharded placement; publication validity has its own controls.
+        with mock.patch.object(self.image_cache, "png_problem", return_value=None), \
+                mock.patch.object(self.image_cache, "_fetch_image", return_value=b"png"):
             self.image_cache.download_static_image("https://media/Badge/123456.png", "/Badge/123456.png", "ua")
 
         expected = self.image_cache.sharded_static_path("Badge/123456.png")
```


## linux/raofflineproxy/proxy_service.py @ c7ebd1b6e7+18: lines 260-348 (excerpt of 1506)

```text
  260      user_agent: str | None,
  261      game_id: int | None,
  262  ) -> None:
  263      ua = user_agent or FALLBACK_USER_AGENT
  264      for orig_url, img_path in downloads:
  265          schedule_image_download(orig_url, img_path, ua, game_id)
  266  
  267  
  268  class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
  269      allow_reuse_address = True
  270      daemon_threads = True
  271  
  272  
  273  class ProxyRequestHandler(BaseHTTPRequestHandler):
  274      server: "ProxyRuntimeServer"
  275  
  276      def setup(self) -> None:
  277          super().setup()
  278          self.request.settimeout(SOCKET_TIMEOUT_SECONDS)
  279  
  280      def do_GET(self) -> None:
  281          self._handle_request()
  282  
  283      def do_POST(self) -> None:
  284          self._handle_request()
  285  
  286      def log_message(self, format: str, *args) -> None:
  287          LOGGER.debug(format, *args)
  288  
  289      def _handle_request(self) -> None:
  290          if self.client_address[0] not in {"127.0.0.1", "::1"}:
  291              self.wfile.write(error_json(403, "loopback_only"))
  292              return
  293  
  294          if self.command not in {"GET", "POST"}:
  295              self.wfile.write(error_json(405, "method not allowed"))
  296              return
  297  
  298          content_length = int(self.headers.get("Content-Length", "0") or "0")
  299          if content_length > MAX_REQUEST_BODY_BYTES:
  300              self.wfile.write(error_json(413, "request body too large"))
  301              return
  302  
  303          body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
  304          headers = {key:*** value for key, value in self.headers.items()}
  305  
  306          # ROCKNIX (fork #199, #242): is_online() probes on every call while
  307          # the tracker says unreachable, and the log line is not worth a
  308          # probe for any request: it reads the state as last probed. The
  309          # request's own path asks is_online() below where the answer decides
  310          # something. Before #242 every dorequest.php call paid a probe here
  311          # -- twenty seconds of name lookup on a link with no DNS -- before it
  312          # was even logged, which is how the interface's fifteen-second wait
  313          # for a store-only answer ran out on the RG35XX SP.
  314          online = is_retroachievements_reachable()
  315          LOGGER.info(
  316              "Request: %s %s body=%s online=%s",
  317              self.command,
  318              redact_query_tokens(self.path),
  319              redact_form_tokens(body),
  320              online,
  321          )
  322  
  323          response = self.server.process_proxy_request(
  324              self.command, self.path, body, headers
  325          )
  326          self.wfile.write(response)
  327          self.wfile.flush()
  328          # Close gracefully (FIN, not RST): shut down the write side and let
  329          # the client finish reading before the socket is torn down, rather
  330          # than an abrupt close that can reset the connection out from under
  331          # a client still draining its receive buffer.
  332          try:
  333              self.connection.shutdown(socket.SHUT_WR)
  334          except OSError:
  335              pass
  336  
  337  
  338  class ProxyRuntimeServer(ThreadingTCPServer):
  339      def __init__(self, config_data: dict, storage: Storage):
  340          self.config_data = dict(config_data)
  341          self.storage = storage
  342          self.running = True
  343          self.has_internet = False
  344          self.activity = GameActivityTracker()
  345          self.flush_lock = threading.Lock()
  346          self.pending_award_lock = threading.Lock()
  347          host = proxy_host(self.config_data)
  348          port = proxy_port(self.config_data)
```


## linux/raofflineproxy/proxy_service.py @ c7ebd1b6e7+18: lines 432-518 (excerpt of 1506)

```text
  432          if action in AWARD_ACTIONS:
  433              return self.handle_award_request(path, raw_body, headers)
  434  
  435          if action == "unlocks" and not self.is_online():
  436              game_id = extract_request_param(path, raw_body, "g")
  437              user = extract_request_param(path, raw_body, "u")
  438              if game_id and user:***
  439                  return ok_json(self.build_offline_unlocks_response(int(game_id), user))
  440  
  441          if action == "startsession" and not self.is_online():
  442              return self.handle_start_session(path, raw_body)
  443  
  444          if is_hardcore_request(path, raw_body):
  445              if not self.is_online():
  446                  return error_json(503, "upstream unavailable")
  447              return self.forward_to_upstream(method, path, raw_body, headers)
  448  
  449          if action in FAKE_OFFLINE_SUCCESS_ACTIONS and not self.is_online():
  450              return ok_json('{"Success":true}')
  451  
  452          if action in ALWAYS_TRY_UPSTREAM_ACTIONS:
  453              upstream = self.forward_to_upstream_result(method, path, raw_body, headers)
  454              if upstream[0] in {"success", "http_error"}:
  455                  status_code = upstream[1]
  456                  reason = upstream[2]
  457                  response_body_bytes = upstream[3]
  458                  content_type = upstream[4]
  459                  response_body = upstream[5]
  460                  if response_body is not None and should_cache_response(response_body):
  461                      proxy_base_url = self._proxy_base_url()
  462                      rewritten_body, downloads = rewrite_image_urls(action, response_body, proxy_base_url)
  463                      if image_caching_enabled(self.config_data):
  464                          _start_image_downloads(downloads, user_agent, None)
  465                      key = cache_key_for_request(path, raw_body)
  466                      # Store the original body — the DB stays port-agnostic.
  467                      self.storage.upsert_cache(key, response_body)
  468                      response_body_bytes = rewritten_body.encode("utf-8")
  469                  return raw_response_bytes(
  470                      status_code, response_body_bytes, content_type, reason
  471                  )
  472              cached_login_response = self.handle_offline_login(path, raw_body, action)
  473              if cached_login_response is not None:
  474                  return cached_login_response
  475  
  476          # ROCKNIX (fork #190): a client that wants the store and nothing else
  477          # -- the interface's pages, which show the device's copy -- says so
  478          # with X-RA-Store-Only: 1 and is answered from the store whatever this
  479          # process believes about the link. While it still believes it is
  480          # online (the monitor probes every fifteen seconds), every request
  481          # first tries upstream with a fifteen-second timeout, and a summary
  482          # over a few hundred games on a link that has just gone is hours.
  483          if store_only_requested(headers):
  484              return self.handle_offline_request(path, raw_body, action)
  485  
  486          if self.is_online():
  487              return self.handle_online_request(method, path, raw_body, action, headers)
  488  
  489          return self.handle_offline_request(path, raw_body, action)
  490  
  491      def handle_offline_login(
  492          self, path: str, raw_body: str, action: str | None
  493      ) -> bytes | None:
  494          if action not in ALWAYS_TRY_UPSTREAM_ACTIONS:
  495              return None
  496  
  497          user = extract_request_param(path, raw_body, "u")
  498          if not user:***
  499              return None
  500  
  501          cached = self.storage.get_cache(cache_keys.login(user))
  502          if cached is None:
  503              return None
  504  
  505          # The store's answer, given because upstream could not be reached:
  506          # X-RA-Offline: 1 says so to a client that wants to tell the player.
  507          return ok_json(cached["responseBody"], extra_headers=(OFFLINE_LOGIN_HEADER,))
  508  
  509      def handle_award_request(
  510          self, path: str, raw_body: str, headers: dict[str, str]
  511      ) -> bytes:
  512          if is_hardcore_request(path, raw_body):
  513              return error_json(403, "hardcore_not_supported")
  514  
  515          if self.is_online():
  516              upstream = self.forward_to_upstream_result("POST", path, raw_body, headers)
  517              if upstream[0] == "success":
  518                  self.schedule_post_award_refresh(path, raw_body, headers)
```


## linux/raofflineproxy/proxy_service.py @ c7ebd1b6e7+18: lines 1397-1448 (excerpt of 1506)

```text
 1397                  scan.new,
 1398                  scan.queued,
 1399              )
 1400              scans.append(scan)
 1401          return scans
 1402  
 1403  
 1404  def due_refresh_game_ids(patch_keys: list[str], recently_played: set[int]) -> list[int]:
 1405      due: list[int] = []
 1406      for patch_key in patch_keys:
 1407          game_id = cache_keys.parse_game_id_from_patch_key(patch_key)
 1408          if game_id is not None and game_id in recently_played and game_id not in due:
 1409              due.append(game_id)
 1410      return due
 1411  
 1412  
 1413  def retry_storage_corruption_report(config_data: dict | None = None) -> None:
 1414      # The menu only ever attempts this once (on first open after the incident) and shows
 1415      # the user the outcome regardless of success, so it doesn't nag them again — if that
 1416      # one attempt happened while offline, the report would otherwise never reach us. The
 1417      # service retries silently on every startup until it actually gets through.
 1418      incident = storage_corruption.load_incident()
 1419      if incident is None or incident.get("reported"):
 1420          return
 1421      if not log_upload_enabled(config_data):
 1422          LOGGER.info("Storage corruption report not sent: upload_logs is off")
 1423          return
 1424      try:
 1425          upload_id = log_uploader.report_storage_corruption(incident)
 1426      except Exception as exc:
 1427          LOGGER.warning("Storage corruption report retry failed: %s", exc)
 1428          return
 1429      storage_corruption.mark_reported(upload_id)
 1430  
 1431  
 1432  def stop_workers(workers: list, timeout: float = WORKER_STOP_TIMEOUT_SECONDS) -> None:
 1433      """Stops every worker, then waits for each so none still uses the storage once it is
 1434      closed."""
 1435      for worker in workers:
 1436          worker.stop()
 1437      for worker in workers:
 1438          if worker.is_alive():
 1439              worker.join(timeout)
 1440  
 1441  
 1442  def run_proxy_service(
 1443      config_data: dict, stop_event: threading.Event | None = None
 1444  ) -> None:
 1445      storage = Storage()
 1446      # Bind the listening port before any other startup work: on boot-to-game
 1447      # devices the emulator can reach its RetroAchievements login before the
 1448      # service is fully up, and a refused connection disables achievements for
```


## linux/raofflineproxy/proxy_service.py @ c7ebd1b6e7+18: lines 1452-1506 (excerpt of 1506)

```text
 1452          "Proxy listening host=%s port=%s",
 1453          proxy_host(config_data),
 1454          proxy_port(config_data),
 1455      )
 1456      LOGGER.info("Storage backend: %s", storage.backend)
 1457      ensure_ra_proxy_chained(config_data)
 1458      connectivity_monitor = ConnectivityMonitor(server)
 1459      periodic_refresh = PeriodicRefresh(server)
 1460      cache_queue_worker = CacheQueueWorker(server)
 1461      folder_watcher = FolderWatcher(server)
 1462      usage_reporter = UsageReporter(server)
 1463  
 1464      try:
 1465          serving_thread = threading.Thread(
 1466              target=server.serve_forever,
 1467              kwargs={"poll_interval": 0.5},
 1468              daemon=True,
 1469          )
 1470          serving_thread.start()
 1471  
 1472          migrate_user_case_in_cache_keys(storage)
 1473          initial_online = server.refresh_reachability(force_probe=True)
 1474          save_online_state(initial_online)
 1475          if initial_online:
 1476              server.flush_pending_awards()
 1477              retry_storage_corruption_report(config_data)
 1478          connectivity_monitor.initial_online = initial_online
 1479          connectivity_monitor.start()
 1480          periodic_refresh.start()
 1481          cache_queue_worker.start()
 1482          folder_watcher.start()
 1483          usage_reporter.start()
 1484  
 1485          if stop_event is None:
 1486              serving_thread.join()
 1487          else:
 1488              while not stop_event.wait(0.5):
 1489                  continue
 1490  
 1491          server.shutdown()
 1492          serving_thread.join(timeout=5)
 1493      finally:
 1494          stop_workers(
 1495              [
 1496                  connectivity_monitor,
 1497                  periodic_refresh,
 1498                  cache_queue_worker,
 1499                  folder_watcher,
 1500                  usage_reporter,
 1501              ]
 1502          )
 1503          usage_stats.flush()
 1504          stop_ra_proxy_chain()
 1505          server.server_close()
 1506          storage.close()
```


## linux/raofflineproxy/auth.py @ c7ebd1b6e7+18: lines 1-143 (excerpt of 143)

```text
    1  from __future__ import annotations
    2  
    3  import json
    4  import logging
    5  
    6  from . import cache_keys
    7  from .config import (
    8      FALLBACK_USER_AGENT,
    9      detect_retroarch_cfg,
   10      detect_rocknix_system_cfg,
   11      upstream_host,
   12  )
   13  from .network import build_api_url, http_get
   14  from .retroarch_cfg import (
   15      cheevos_append_cfg_path,
   16      load_retroarch_password_credentials,
   17      load_retroarch_token_credentials,
   18      load_rocknix_system_password_credentials,
   19      load_rocknix_system_token_credentials,
   20      load_spruce_credentials,
   21  )
   22  from .storage import Storage
   23  from .utils import proxy_user_agent
   24  
   25  LOGGER = logging.getLogger("raofflineproxy")
   26  
   27  
   28  def resolve_credentials(
   29      storage: Storage,
   30      config_data: dict | None = None,
   31      user_agent: str = FALLBACK_USER_AGENT,
   32  ) -> dict | None:
   33      config_data = config_data or {}
   34      cfg_path = str(config_data.get("retroarch_cfg") or detect_retroarch_cfg())
   35      # Also check the cheevos appendconfig — muOS stores credentials there
   36      cheevos_cfg = str(cheevos_append_cfg_path(cfg_path)) if cfg_path else None
   37      # ROCKNIX goes further: setsettings.sh deletes cheevos_username/cheevos_password
   38      # from retroarch.cfg on every game launch, so EmulationStation's own settings are
   39      # the only place its credentials live.
   40      rocknix_system_cfg = detect_rocknix_system_cfg(config_data)
   41  
   42      token_credentials = (
   43          load_retroarch_token_credentials(cfg_path)
   44          or load_retroarch_token_credentials(cheevos_cfg)
   45          or load_rocknix_system_token_credentials(rocknix_system_cfg)
   46      )
   47      if token_credentials is not None:
   48          return cache_token_credentials(storage, token_credentials)
   49  
   50      # spruce keeps its credentials in its own settings file and only copies them into
   51      # the RetroArch config when a game launches, so before the first launch that file is
   52      # the only source.
   53      password_credentials = (
   54          load_retroarch_password_credentials(cfg_path)
   55          or load_retroarch_password_credentials(cheevos_cfg)
   56          or load_rocknix_system_password_credentials(rocknix_system_cfg)
   57          or load_spruce_credentials()
   58      )
   59  
   60      # A cached sign-in is taken only when it is the configured account's.
   61      # When a password names the account, the cached row looked up is that
   62      # user's; the first login row in the store, whoever's it is, was what
   63      # this returned before -- so a device that had signed in as one account
   64      # and now holds another's password (and no token yet) kept caching,
   65      # refreshing and flushing as the first.
   66      expected_user = ""
   67      if password_credentials is not None:
   68          expected_user = cache_keys.normalize_user(str(password_credentials.get("user") or ""))
   69      if expected_user:***
   70          cached = load_cached_login_for(storage, expected_user)
   71      else:
   72          cached = storage.load_login_credentials()
   73      if cached is not None and not storage.is_token_invalid(cached["token"]):
   74          return cached
   75  
   76      if password_credentials is not None:
   77          refreshed = login_and_cache_token(
   78              storage, config_data, password_credentials, user_agent
   79          )
   80          if refreshed is not None:
   81              return refreshed
   82  
   83      return cached
   84  
   85  
   86  def load_cached_login_for(storage: Storage, user:*** str) -> dict | None:
   87      """The cached sign-in of one account, by its login row, or None."""
   88      entry = storage.get_cache(cache_keys.login(user))
   89      if entry is None:
   90          return None
   91      try:
   92          payload = json.loads(entry["responseBody"])
   93      except Exception:
   94          return None
   95      cached_user = payload.get("User")
   96      token = payload.get("Token")
   97      if not cached_user or not token:***
   98          return None
   99      return {"user": cached_user, "token": token}
  100  
  101  
  102  def cache_token_credentials(storage: Storage, credentials: dict) -> dict | None:
  103      user = credentials.get("user")
  104      token = credentials.get("token")
  105      if not user or not token:***
  106          return None
  107  
  108      body = json.dumps({"Success": True, "User": user, "Token": token})
  109      storage.upsert_cache(cache_keys.login(user), body)
  110      return {"user": user, "token": token}
  111  
  112  
  113  def login_and_cache_token(
  114      storage: Storage,
  115      config_data: dict,
  116      credentials: dict,
  117      user_agent: str,
  118  ) -> dict | None:
  119      url = build_api_url(
  120          upstream_host(config_data),
  121          "login2",
  122          {
  123              "u": credentials["user"],
  124              "p": credentials["password"],
  125          },
  126      )
  127      try:
  128          response_body = http_get(
  129              url, proxy_user_agent(user_agent or FALLBACK_USER_AGENT)
  130          )
  131          payload = json.loads(response_body)
  132      except Exception as exc:
  133          LOGGER.warning("login2 request failed: %s", exc)
  134          return None
  135  
  136      user = payload.get("User") or credentials["user"]
  137      token = payload.get("Token")
  138      if not payload.get("Success") or not user or not token:***
  139          LOGGER.warning("login2 rejected credentials for user=*** credentials["user"])
  140          return None
  141  
  142      storage.upsert_cache(cache_keys.login(user), response_body)
  143      return {"user": user, "token": token}
```


## linux/raofflineproxy/network.py @ c7ebd1b6e7+18: lines 12-48 (excerpt of 610)

```text
   12  import urllib.request
   13  from pathlib import Path
   14  from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
   15  
   16  from . import rate_limit, usage_stats
   17  from .config import FALLBACK_USER_AGENT, upstream_host
   18  from .utils import proxy_user_agent
   19  
   20  LOGGER = logging.getLogger("raofflineproxy")
   21  REDACTED_QUERY_KEYS = {"p", "t", "token", "password"}
   22  REACHABILITY_INTERVAL_SECONDS = 30.0
   23  PROBE_ATTEMPTS = 3
   24  PROBE_RETRY_DELAY_SECONDS = 1.0
   25  # ROCKNIX (fork #242): how long a name lookup may take before the host is
   26  # called unreachable. urlopen's timeout bounds the connection and the read,
   27  # never the resolver: with a route but no working DNS -- a handheld still
   28  # associated to a hotspot whose uplink is gone, or one whose Wi-Fi switch
   29  # leaves the interface up -- glibc's resolver gives up after about twenty
   30  # seconds, and every request-path probe and every upstream attempt paid
   31  # them. The interface's pages wait fifteen seconds for this process and
   32  # then fell through to the web, which timed out again; RetroArch's sign-in
   33  # at launch paid it twice.
   34  LOOKUP_SECONDS = 3.0
   35  HTTP_TOO_MANY_REQUESTS = 429
   36  HTTP_GET_MAX_429_RETRIES = 4
   37  HTTP_GET_INITIAL_429_BACKOFF_SECONDS = 2.0
   38  HTTP_GET_MAX_429_BACKOFF_SECONDS = 15.0
   39  RA_MIN_REQUEST_INTERVAL_SECONDS = 0.3
   40  
   41  
   42  class RequestThrottle:
   43      def __init__(self) -> None:
   44          self._lock = threading.Lock()
   45          self._last_request_at = 0.0
   46  
   47      def wait(self, action: str | None = None) -> None:
   48          with self._lock:
```


## linux/raofflineproxy/network.py @ c7ebd1b6e7+18: lines 247-428 (excerpt of 610)

```text
  247      _log_probe_failure(reason)
  248      mark_retroachievements_unreachable(current_time)
  249      return False
  250  
  251  
  252  # ROCKNIX (audit #308 F-RA-20): the answer the bounded lookup got, kept for
  253  # the connection that follows. The lookup is bounded, and then the request
  254  # opens its connection by name -- a second lookup, which nothing bounded and
  255  # nothing caches on a handheld (no nscd): a resolver that answered once and
  256  # stopped would hold the request for the twenty seconds the first lookup is
  257  # bounded against. So socket.getaddrinfo answers a host the bounded lookup
  258  # resolved in the last REMEMBER_SECONDS from that answer (the port and the
  259  # socket type the caller asks for put in); every other lookup, and the
  260  # bounded lookup itself -- which asks the resolver every time, so it stays
  261  # the probe it was -- goes to the resolver as before.
  262  REMEMBER_SECONDS = 30.0
  263  _remembered: dict[str, tuple[float, list]] = {}
  264  _remembered_lock = threading.Lock()
  265  _asking_resolver = threading.local()
  266  # The resolver's own function, even when this module is loaded a second time.
  267  _resolver_getaddrinfo = getattr(socket.getaddrinfo, "__wrapped__", socket.getaddrinfo)
  268  
  269  
  270  def _getaddrinfo_remembering(host, port, family=0, type=0, proto=0, flags=0):
  271      if isinstance(host, str) and not getattr(_asking_resolver, "active", False):
  272          with _remembered_lock:
  273              entry = _remembered.get(host.lower())
  274          if entry is not None and time.monotonic() - entry[0] < REMEMBER_SECONDS:
  275              try:
  276                  number = 0 if port is None else int(port)
  277              except (TypeError, ValueError):
  278                  number = None
  279              answer = []
  280              for fam, kind, prot, canon, address in entry[1] if number is not None else ():
  281                  if family and fam != family:
  282                      continue
  283                  if type and kind and kind != type:
  284                      continue
  285                  if proto and prot and prot != proto:
  286                      continue
  287                  item = (fam, kind or type, prot or proto, canon, (address[0], number, *address[2:]))
  288                  if item not in answer:
  289                      answer.append(item)
  290              if answer:
  291                  return answer
  292      return _resolver_getaddrinfo(host, port, family, type, proto, flags)
  293  
  294  
  295  _getaddrinfo_remembering.__wrapped__ = _resolver_getaddrinfo
  296  socket.getaddrinfo = _getaddrinfo_remembering
  297  
  298  
  299  def resolve_host_bounded(host: str, seconds: float = LOOKUP_SECONDS) -> tuple[bool, str]:
  300      """Look the host up in a thread of its own and give it `seconds`.
  301  
  302      ROCKNIX (fork #242). (True, "") when the name resolved in time; (False,
  303      why) when it did not or could not. A lookup still running when the time
  304      is up is left to finish on its own daemon thread; the answer it was going
  305      to give is "unreachable" either way, and the caller must not wait for it.
  306      The resolver is asked every time, and a lookup that succeeded is kept for
  307      REMEMBER_SECONDS, so the connection that follows is answered from it
  308      rather than by a second lookup nothing bounds (audit #308 F-RA-20).
  309      """
  310      if not host:
  311          return False, "no host to look up"
  312      result: dict[str, str | bool] = {}
  313  
  314      def work() -> None:
  315          _asking_resolver.active = True
  316          try:
  317              answer = socket.getaddrinfo(host, None)
  318              with _remembered_lock:
  319                  _remembered[host.lower()] = (time.monotonic(), list(answer))
  320              result["ok"] = True
  321          except Exception as error:  # noqa: BLE001 - every resolver error is the same answer
  322              result["error"] = str(error)
  323  
  324      thread = threading.Thread(target=work, name="ra-name-lookup", daemon=True)
  325      thread.start()
  326      thread.join(seconds)
  327      if thread.is_alive():
  328          return False, f"name lookup of {host} took longer than {seconds:g} s"
  329      if result.get("ok"):
  330          return True, ""
  331      return False, f"name lookup of {host} failed: {result.get('error', 'unknown')}"
  332  
  333  
  334  def _head_upstream(url: str, user_agent: str | None) -> tuple[bool, str]:
  335      # ROCKNIX (fork #242): the lookup first, bounded; the HEAD's own timeout
  336      # starts only once there is an address to connect to.
  337      resolved, reason = resolve_host_bounded(urlsplit(url).hostname or "")
  338      if not resolved:
  339          return False, reason
  340      request = urllib.request.Request(
  341          url,
  342          headers={
  343              "User-Agent": proxy_user_agent(user_agent or FALLBACK_USER_AGENT),
  344              "Accept-Encoding": "identity",
  345          },
  346          method="HEAD",
  347      )
  348      try:
  349          with urllib.request.urlopen(
  350              request, timeout=5, context=configured_ssl_context()
  351          ) as response:
  352              if 200 <= response.status < 500:
  353                  return True, ""
  354              return False, f"HTTP {response.status}"
  355      except Exception as error:
  356          return False, str(error)
  357  
  358  
  359  def _log_probe_failure(reason: str) -> None:
  360      # Only on the way from reachable to unreachable: a device that stays offline
  361      # probes every 15s and would otherwise fill the log with the same line.
  362      reachable, checked_at = _reachability_tracker.current()
  363      if checked_at == 0.0 or reachable:
  364          LOGGER.info("RetroAchievements probe failed: %s", reason)
  365  
  366  
  367  def http_get(url: str, user_agent: str) -> str:
  368      action = api_action_from_url(url)
  369      max_retries = 0 if rate_limit.in_background() else HTTP_GET_MAX_429_RETRIES
  370  
  371      for attempt in range(max_retries + 1):
  372          if rate_limit.in_background() and rate_limit.paused_until() is not None:
  373              raise rate_limit.RateLimitedError(
  374                  "RetroAchievements asked to slow down; background caching is paused"
  375              )
  376          if action is not None:
  377              _request_throttle.wait(f"GET {action}")
  378  
  379          request = urllib.request.Request(
  380              url,
  381              headers={
  382                  "User-Agent": user_agent,
  383                  "Accept-Encoding": "identity",
  384              },
  385              method="GET",
  386          )
  387          usage_source = (
  388              usage_stats.SOURCE_BACKGROUND if rate_limit.in_background() else usage_stats.SOURCE_APP
  389          )
  390  
  391          try:
  392              with urllib.request.urlopen(
  393                  request, timeout=10, context=configured_ssl_context()
  394              ) as response:
  395                  if action is not None:
  396                      usage_stats.record_request(usage_source, getattr(response, "status", 200))
  397                  body = read_response_bytes(response)
  398                  mark_retroachievements_reachable()
  399                  return decode_response_body(body, response_content_type(response))
  400          except urllib.error.HTTPError as error:
  401              if action is not None:
  402                  usage_stats.record_request(usage_source, error.code)
  403              if error.code >= 500:
  404                  mark_retroachievements_unreachable()
  405              else:
  406                  mark_retroachievements_reachable()
  407  
  408              if error.code == HTTP_TOO_MANY_REQUESTS:
  409                  rate_limit.on_rate_limited(retry_after_header_millis(error))
  410                  if attempt < max_retries:
  411                      retry_after = retry_after_seconds(error, attempt)
  412                      LOGGER.warning(
  413                          "GET hit 429 for %s; retrying in %.3fs (attempt %s/%s)",
  414                          action or redacted_url(url),
  415                          retry_after,
  416                          attempt + 1,
  417                          max_retries,
  418                      )
  419                      time.sleep(retry_after)
  420                      continue
  421  
  422              api_error = describe_api_error(error)
  423              if api_error:
  424                  # HTTPError.reason is a read-only view of .msg, and .msg is what
  425                  # str(error) renders, so this is the only way to make the
  426                  # message callers surface carry RA's actual reason.
  427                  error.msg = api_error
  428              LOGGER.warning(
```


## linux/raofflineproxy/network.py @ c7ebd1b6e7+18: lines 508-588 (excerpt of 610)

```text
  508          return min(header_seconds, HTTP_GET_MAX_429_BACKOFF_SECONDS)
  509  
  510      return min(
  511          HTTP_GET_INITIAL_429_BACKOFF_SECONDS * (2**attempt),
  512          HTTP_GET_MAX_429_BACKOFF_SECONDS,
  513      )
  514  
  515  
  516  def http_post(
  517      url: str,
  518      body: str,
  519      headers: dict[str, str] | None = None,
  520      usage_source: str | None = None,
  521  ) -> tuple[int, str, str]:
  522      request_headers = {
  523          "Content-Type": "application/x-www-form-urlencoded",
  524          "Accept-Encoding": "identity",
  525      }
  526      if headers:
  527          request_headers.update(headers)
  528  
  529      request = urllib.request.Request(
  530          url,
  531          data=body.encode("utf-8"),
  532          headers=request_headers,
  533          method="POST",
  534      )
  535  
  536      try:
  537          with urllib.request.urlopen(
  538              request, timeout=15, context=configured_ssl_context()
  539          ) as response:
  540              if usage_source is not None:
  541                  usage_stats.record_request(usage_source, getattr(response, "status", 200))
  542              response_body = read_response_bytes(response)
  543              mark_retroachievements_reachable()
  544              return (
  545                  response.status,
  546                  response.reason,
  547                  decode_response_body(response_body, response_content_type(response)),
  548              )
  549      except urllib.error.HTTPError as error:
  550          if usage_source is not None:
  551              usage_stats.record_request(usage_source, error.code)
  552          response_body = error.read()
  553          if error.code >= 500:
  554              mark_retroachievements_unreachable()
  555          else:
  556              mark_retroachievements_reachable()
  557          LOGGER.warning(
  558              "POST failed status=%s reason=%s url=%s",
  559              error.code,
  560              error.reason,
  561              redacted_url(url),
  562          )
  563          return (
  564              error.code,
  565              error.reason,
  566              decode_response_body(response_body, error.headers.get("Content-Type")),
  567          )
  568      except urllib.error.URLError as error:
  569          if usage_source is not None:
  570              usage_stats.record_request(usage_source, None)
  571          mark_retroachievements_unreachable()
  572          LOGGER.warning(
  573              "POST connection failed reason=%s url=%s",
  574              error.reason,
  575              redacted_url(url),
  576          )
  577          raise
  578      except Exception:
  579          mark_retroachievements_unreachable()
  580          LOGGER.exception("POST failed url=%s", redacted_url(url))
  581          raise
  582  
  583  
  584  def online_check(config_data: dict) -> bool:
  585      return probe_retroachievements(config_data, user_agent=FALLBACK_USER_AGENT)
  586  
  587  
  588  def build_forward_headers(headers: dict[str, str]) -> dict[str, str]:
```


## linux/raofflineproxy/storage.py @ c7ebd1b6e7+18: lines 62-168 (excerpt of 1161)

```text
   62  _EVICTION_EXEMPT_PREFIXES = (
   63      cache_keys.PREFIX_LOGIN,
   64      cache_keys.PREFIX_PATCH,
   65      cache_keys.PREFIX_ACHIEVEMENTSETS,
   66      cache_keys.PREFIX_UNLOCKS,
   67      cache_keys.PREFIX_STARTSESSION,
   68      cache_keys.PREFIX_GAMEID,
   69      cache_keys.PREFIX_CACHE_QUEUE,
   70      cache_keys.PREFIX_WATCH_SEEN,
   71  )
   72  
   73  class Storage:
   74      def __init__(self, database_path: Path = DATABASE_FILE):
   75          ensure_config_dir()
   76          self._database_path = database_path
   77          self._lock = threading.RLock()
   78          self._use_sqlite = sqlite3 is not None
   79          self._json_path = database_path.with_suffix(".json")
   80          self._json_lock_path = self._json_path.with_suffix(
   81              f"{self._json_path.suffix}.lock"
   82          )
   83          self._json_state: dict[str, Any] | None = None
   84          self._connection = None
   85  
   86          if self._use_sqlite:
   87              self._connection = sqlite3.connect(
   88                  self._database_path, check_same_thread=False, timeout=5.0
   89              )
   90              self._connection.row_factory = sqlite3.Row
   91              self._initialize_sqlite()
   92              self._index_missing_game_meta()
   93              self._import_legacy_json()
   94          else:
   95              self._initialize_json()
   96  
   97      @property
   98      def backend(self) -> str:
   99          return "sqlite" if self._use_sqlite else "json"
  100  
  101      def close(self) -> None:
  102          with self._lock:
  103              if self._connection is not None:
  104                  self._connection.close()
  105  
  106      def _initialize_sqlite(self) -> None:
  107          assert self._connection is not None
  108          with self._lock:
  109              try:
  110                  self._connection.execute("PRAGMA journal_mode=WAL;").fetchone()
  111              except sqlite3.OperationalError:
  112                  # WAL requires shared-memory/locking semantics that FAT32
  113                  # (e.g. Miyoo Mini / Onion SD cards) doesn't provide.
  114                  self._connection.execute("PRAGMA journal_mode=DELETE;")
  115              self._connection.executescript(
  116                  """
  117                  CREATE TABLE IF NOT EXISTS api_cache (
  118                      id INTEGER PRIMARY KEY AUTOINCREMENT,
  119                      cacheKey TEXT NOT NULL UNIQUE,
  120                      responseBody TEXT NOT NULL,
  121                      sourceRomPath TEXT,
  122                      cachedAt INTEGER NOT NULL,
  123                      firstCachedAt INTEGER NOT NULL
  124                  );
  125                  CREATE TABLE IF NOT EXISTS pending_awards (
  126                      id INTEGER PRIMARY KEY AUTOINCREMENT,
  127                      achievementId INTEGER NOT NULL UNIQUE,
  128                      queryString TEXT NOT NULL,
  129                      requestBody TEXT NOT NULL,
  130                      userAgent TEXT NOT NULL,
  131                      queuedAt INTEGER NOT NULL,
  132                      retryCount INTEGER NOT NULL DEFAULT 0,
  133                      lastError TEXT,
  134                      status TEXT NOT NULL DEFAULT 'pending',
  135                      payloadHash TEXT NOT NULL DEFAULT '',
  136                      prevHash TEXT NOT NULL DEFAULT '',
  137                      signature TEXT NOT NULL DEFAULT '',
  138                      signedAt INTEGER NOT NULL DEFAULT 0
  139                  );
  140                  CREATE TABLE IF NOT EXISTS cached_game_meta (
  141                      cacheKey TEXT PRIMARY KEY,
  142                      gameId INTEGER,
  143                      title TEXT,
  144                      imagePath TEXT
  145                  );
  146                  CREATE INDEX IF NOT EXISTS cached_game_meta_game_id ON cached_game_meta(gameId);
  147                  CREATE TRIGGER IF NOT EXISTS cached_game_meta_delete AFTER DELETE ON api_cache
  148                  BEGIN
  149                      DELETE FROM cached_game_meta WHERE cacheKey = old.cacheKey;
  150                  END;
  151                  CREATE TRIGGER IF NOT EXISTS cached_game_meta_rename AFTER UPDATE OF cacheKey ON api_cache
  152                  BEGIN
  153                      UPDATE cached_game_meta SET cacheKey = new.cacheKey WHERE cacheKey = old.cacheKey;
  154                  END;
  155                  """
  156              )
  157              cache_columns = {
  158                  row["name"]
  159                  for row in self._connection.execute(
  160                      "PRAGMA table_info(api_cache)"
  161                  ).fetchall()
  162              }
  163              if "sourceRomPath" not in cache_columns:
  164                  self._connection.execute(
  165                      "ALTER TABLE api_cache ADD COLUMN sourceRomPath TEXT"
  166                  )
  167  
  168              columns = {
```


## linux/raofflineproxy/utils.py @ c7ebd1b6e7+18: lines 92-132 (excerpt of 132)

```text
   92          404: "Not Found",
   93          405: "Method Not Allowed",
   94          413: "Payload Too Large",
   95          500: "Internal Server Error",
   96          501: "Not Implemented",
   97          503: "Service Unavailable",
   98      }
   99      return phrases.get(code, "Response")
  100  
  101  
  102  # Only a t=/p= that actually starts a query parameter, hence the leading delimiter: a bare
  103  # substring match also fires on the "t=" inside host=, port= and checked_at=, and with no
  104  # "&" left on the line to stop at it swallows everything after it. That silently shredded
  105  # whole support logs, which are redacted line by line before upload.
  106  #
  107  # The delimiter class is deliberately wider than "?&": these run over free-text log lines,
  108  # where a secret can also follow a quote or a comma. Letters are what must not qualify, so
  109  # host=/port=/checked_at= stay readable.
  110  _QUERY_SECRET_PATTERN = re.compile(r"""(^|[?&,;\s"'\[({])([tp])=([^&\s"'\])}]*)""")
  111  
  112  
  113  def redact_query_tokens(value: str) -> str:
  114      return _QUERY_SECRET_PATTERN.sub(
  115          lambda match: f"{match.group(1)}{match.group(2)}=<token>", value
  116      )
  117  
  118  
  119  def redact_form_tokens(value: str) -> str:
  120      params = parse_qsl(value, keep_blank_values=True)
  121      redacted = [
  122          (key, "<token>" if key in {"t", "p"} else current) for key, current in params
  123      ]
  124      return urlencode(redacted)
  125  
  126  
  127  def query_params_from_path(path: str) -> dict[str, str]:
  128      return dict(parse_qsl(urlsplit(path).query, keep_blank_values=True))
  129  
  130  
  131  def decode_value(value: str) -> str:
  132      return unquote_plus(value)
```


## linux/raofflineproxy/log_uploader.py @ c7ebd1b6e7+18: lines 1-38 (excerpt of 380)

```text
    1  from __future__ import annotations
    2  
    3  import io
    4  import json
    5  import logging
    6  import re
    7  import urllib.error
    8  import urllib.request
    9  import zipfile
   10  from pathlib import Path
   11  
   12  from . import config, ppsspp_cfg, retroarch_cfg
   13  from .network import configured_ssl_context
   14  from .utils import redact_query_tokens
   15  
   16  LOGGER = logging.getLogger(__name__)
   17  
   18  REQUEST_UPLOAD_URL = "https://ud63psmdb5.execute-api.eu-central-1.amazonaws.com/logs/request-upload"
   19  REQUEST_TIMEOUT_SECONDS = 15
   20  # Not config.running_on_muos() (doesn't exist) or menu_sdl.running_on_muos() (would create a
   21  # circular import, since menu_sdl imports upload_logs from this module) — duplicated here.
   22  MUOS_MARKER_PATH = Path("/opt/muos/script/archive")
   23  # Both confirmed from OnionUI/Onion's own diagnostics script
   24  # (static/build/.tmp_update/script/diagnostics/util_snapshot.sh), which reads the exact same
   25  # two files for its "System log snapshot" support tool.
   26  ONION_VERSION_FILE = config.ONION_VERSION_FILE
   27  ONION_DEVICE_MODEL_FILE = Path("/tmp/deviceModel")
   28  # Allium's own version marker, the same file its updater migrations check against.
   29  ALLIUM_VERSION_FILE = Path("/mnt/SDCARD/.allium/version.txt")
   30  # /etc/os-release's OS_VERSION is deliberately truncated to just the leading number by Knulli's
   31  # own build script (board/scripts/post-build-script.sh in knulli-cfw/knulli-linux); this
   32  # untruncated file (version + build date + time) is what Knulli's own knulli-report-stats tool
   33  # reads instead.
   34  KNULLI_VERSION_FILE = Path("/usr/share/knulli/knulli.version")
   35  # muOS's own board/name config value (confirmed on real hardware — see MustardOS/internal's
   36  # script/var/func.sh GET_VAR "device" "board/name"). Its devicetree model property only holds
   37  # the bare SoC codename (e.g. "sun50iw9"), not a useful device label.
   38  MUOS_BOARD_NAME_FILE = Path("/opt/muos/device/config/board/name")
```


## linux/raofflineproxy/log_uploader.py @ c7ebd1b6e7+18: lines 52-138 (excerpt of 380)

```text
   52      r'("cacheKey":\s*"(?:login2::|auth::invalid_token)[^"]*".*?"responseBody":\s*")'
   53      r'((?:\\.|[^"\\])*)(")',
   54      re.DOTALL,
   55  )
   56  
   57  
   58  def _log_file_paths() -> list[Path]:
   59      # RotatingFileHandler renames the active file to "<name>.1" on rollover, so the
   60      # backup can hold the most relevant history if a rollover just happened. Oldest first.
   61      backup = config.LOG_FILE.with_name(config.LOG_FILE.name + ".1")
   62      # menu-sdl.log is a separate log written by the pygame menu process itself
   63      # (key logger output, controller calibration, crashes) — not covered by service.log.
   64      menu_sdl_log = config.CONFIG_DIR / "menu-sdl.log"
   65      # launch.log (muOS only) timestamps every launcher invocation, including the
   66      # boot hook — the only way to see how late the service starts at boot.
   67      launch_log = config.CONFIG_DIR / "launch.log"
   68      # menu-stdout.log (ROCKNIX only) holds the raw stdout/stderr of each launcher
   69      # attempt. A native SDL crash kills the process before any Python handler runs,
   70      # so this is the only record of which driver/preload combination died and how.
   71      menu_stdout_log = config.CONFIG_DIR / "menu-stdout.log"
   72      return [
   73          backup,
   74          config.LOG_FILE,
   75          menu_sdl_log,
   76          launch_log,
   77          menu_stdout_log,
   78          config.UPDATE_STATUS_FILE,
   79          config.STATUS_FILE,
   80      ]
   81  
   82  
   83  def _redact_storage_json(text: str) -> str:
   84      text = _SENSITIVE_CACHE_ENTRY.sub(r"\1<redacted>\3", text)
   85      return "\n".join(redact_query_tokens(line) for line in text.splitlines())
   86  
   87  
   88  def _quarantined_storage_files() -> dict[str, str]:
   89      files: dict[str, str] = {}
   90      for path in sorted(config.CONFIG_DIR.glob(QUARANTINED_STORAGE_GLOB)):
   91          try:
   92              content = path.read_text(encoding="utf-8", errors="replace")
   93          except OSError:
   94              continue
   95          files[path.name] = _redact_storage_json(content)
   96      return files
   97  
   98  
   99  def _read_redacted_log_files() -> dict[str, str]:
  100      # redact_query_tokens does an in-place substring replacement, safe on arbitrary
  101      # free-text log lines. redact_form_tokens fully reparses/re-encodes its input as
  102      # a query string, which would mangle a formatted log line (timestamp, message
  103      # text, etc.) around the secret rather than just blanking it out.
  104      files: dict[str, str] = {}
  105      for path in _log_file_paths():
  106          try:
  107              content = path.read_text(encoding="utf-8", errors="replace")
  108          except OSError:
  109              continue
  110          redacted_lines = (redact_query_tokens(line) for line in content.splitlines())
  111          files[path.name] = "\n".join(redacted_lines)
  112      files.update(_quarantined_storage_files())
  113      return files
  114  
  115  
  116  def _zip_logs(files: dict[str, str]) -> bytes:
  117      buffer = io.BytesIO()
  118      with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
  119          for name, content in files.items():
  120              archive.writestr(name, content.encode("utf-8"))
  121      return buffer.getvalue()
  122  
  123  
  124  def _request_upload_target() -> tuple[str, str]:
  125      request = urllib.request.Request(
  126          REQUEST_UPLOAD_URL,
  127          data=json.dumps(device_metadata()).encode("utf-8"),
  128          headers={"Content-Type": "application/json"},
  129          method="POST",
  130      )
  131      try:
  132          with urllib.request.urlopen(
  133              request, timeout=REQUEST_TIMEOUT_SECONDS, context=configured_ssl_context()
  134          ) as response:
  135              body = response.read().decode("utf-8", errors="replace")
  136      except urllib.error.HTTPError as error:
  137          body = error.read().decode("utf-8", errors="replace")
  138          LOGGER.error(
```


## linux/raofflineproxy/log_uploader.py @ c7ebd1b6e7+18: lines 346-380 (excerpt of 380)

```text
  346          body = error.read().decode("utf-8", errors="replace")
  347          LOGGER.error("Log upload PUT failed status=%s body=%s", error.code, body[:512])
  348          raise RuntimeError(f"Upload failed (HTTP {error.code})") from error
  349      except urllib.error.URLError as error:
  350          LOGGER.error("Log upload PUT failed reason=%s", error.reason)
  351          raise RuntimeError(f"Upload failed: {error.reason}") from error
  352  
  353  
  354  def upload_logs(extra_files: dict[str, str] | None = None) -> str:
  355      files = _read_redacted_log_files()
  356      if extra_files:
  357          files.update(extra_files)
  358      zip_bytes = _zip_logs(files)
  359      try:
  360          upload_id, upload_url = _request_upload_target()
  361          _put_log_archive(upload_url, zip_bytes)
  362      except RuntimeError:
  363          raise
  364      except Exception as error:
  365          LOGGER.exception("Log upload failed unexpectedly")
  366          raise RuntimeError(f"Log upload failed: {error}") from error
  367      return upload_id
  368  
  369  
  370  def report_storage_corruption(incident: dict) -> str:
  371      lost_pending_awards = incident.get("lost_pending_awards")
  372      note = (
  373          "A corrupted local data file was detected and automatically reset.\n"
  374          f"Detected at (ms since epoch): {incident.get('detected_at')}\n"
  375          f"Quarantined file: {incident.get('quarantined_path')}\n"
  376          f"Corrupted file size (bytes): {incident.get('size_bytes')}\n"
  377          f"Parse error: {incident.get('reason')}\n"
  378          f"Salvaged pending_awards count: {lost_pending_awards if lost_pending_awards is not None else 'unknown (unrecoverable)'}\n"
  379      )
  380      return upload_logs({"storage_corruption.txt": note})
```


## linux/raofflineproxy/usage_report.py @ c7ebd1b6e7+18: lines 12-68 (excerpt of 201)

```text
   12  try:
   13      import fcntl
   14  except ImportError:  # pragma: no cover - non-POSIX dev machines
   15      fcntl = None
   16  
   17  from . import cache_keys, cache_queue, log_uploader, usage_stats
   18  from .config import CONFIG_DIR, ensure_config_dir, load_config
   19  from .network import configured_ssl_context
   20  from .storage import PENDING_AWARD_STATUS_PENDING, Storage
   21  
   22  LOGGER = logging.getLogger("raofflineproxy")
   23  
   24  DEFAULT_REPORT_URL = "https://ud63psmdb5.execute-api.eu-central-1.amazonaws.com/usage/ping"
   25  REPORT_URL_ENV = "RAOFFLINEPROXY_USAGE_URL"
   26  # Mirrors config.json's upstream_host override, so test setups can point the report elsewhere
   27  # without having to get an environment variable into the proxy service.
   28  CONFIG_KEY_REPORT_URL = "usage_report_url"
   29  BUILD_ENV = "RAOFFLINEPROXY_BUILD"
   30  REPORT_LOCK_FILE = CONFIG_DIR / "usage_report.lock"
   31  REQUEST_TIMEOUT_SECONDS = 10
   32  DAY_MS = 24 * 60 * 60 * 1000
   33  CLIENT_ID_SALT = "raofflineproxy-usage:"
   34  # Bump when an existing field changes meaning, so the backend can tell old reports from new ones.
   35  USAGE_SCHEMA_VERSION = 1
   36  
   37  
   38  def report_url(config_data: Optional[dict] = None) -> str:
   39      from_env = os.environ.get(REPORT_URL_ENV)
   40      if from_env is not None:
   41          return from_env
   42      data = load_config() if config_data is None else config_data
   43      configured = data.get(CONFIG_KEY_REPORT_URL)
   44      return configured if isinstance(configured, str) else DEFAULT_REPORT_URL
   45  
   46  
   47  def client_id(username: str) -> str:
   48      """Same ID as the Android app, so one person on both platforms is counted once. The backend
   49      re-keys it with a secret that rotates every month."""
   50      return hashlib.sha256((CLIENT_ID_SALT + username.strip().lower()).encode("utf-8")).hexdigest()
   51  
   52  
   53  def is_report_due(last_reported_at: int, now_ms: int) -> bool:
   54      """One report per UTC calendar day, matching the backend's day rows. A clock that jumped to
   55      another day also counts as a new day."""
   56      return last_reported_at <= 0 or last_reported_at // DAY_MS != now_ms // DAY_MS
   57  
   58  
   59  def count_bucket(count: int) -> str:
   60      for limit, label in (
   61          (1, "0"),
   62          (10, "1-9"),
   63          (50, "10-49"),
   64          (100, "50-99"),
   65          (250, "100-249"),
   66          (500, "250-499"),
   67          (1000, "500-999"),
   68          (2500, "1000-2499"),
```


## linux/raofflineproxy/usage_report.py @ c7ebd1b6e7+18: lines 142-201 (excerpt of 201)

```text
  142          try:
  143              fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
  144          except OSError:
  145              yield False
  146              return
  147          try:
  148              yield True
  149          finally:
  150              fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
  151  
  152  
  153  def _send(payload: dict, url: str) -> bool:
  154      request = urllib.request.Request(
  155          url,
  156          data=json.dumps(payload).encode("utf-8"),
  157          headers={"Content-Type": "application/json"},
  158          method="POST",
  159      )
  160      with urllib.request.urlopen(
  161          request, timeout=REQUEST_TIMEOUT_SECONDS, context=configured_ssl_context()
  162      ) as response:
  163          return 200 <= response.status < 300
  164  
  165  
  166  def report_if_due(storage: Storage, now_ms: Optional[int] = None) -> bool:
  167      """Sends at most one report per UTC day, only with consent. Counters are only cleared once the
  168      backend accepted them. Never raises: callers run this from the service's threads and the
  169      menu."""
  170      try:
  171          return _report(storage, int(time.time() * 1000) if now_ms is None else now_ms)
  172      except Exception as exc:
  173          LOGGER.warning("Usage report skipped: %s", exc)
  174          return False
  175  
  176  
  177  def _report(storage: Storage, now_ms: int) -> bool:
  178      config_data = load_config()
  179      url = report_url(config_data)
  180      if not url or usage_stats.load_consent(config_data) is not True:
  181          return False
  182      with _report_lock() as acquired:
  183          if not acquired or not is_report_due(usage_stats.last_reported_at(), now_ms):
  184              return False
  185          credentials = storage.load_login_credentials()
  186          if credentials is None:
  187              return False
  188          counters = usage_stats.reportable(usage_stats.snapshot())
  189          payload = build_payload(
  190              credentials["user"],
  191              log_uploader.device_metadata(),
  192              os.environ.get(BUILD_ENV, "release"),
  193              load_gauges(storage, now_ms),
  194              counters,
  195          )
  196          if not _send(payload, url):
  197              LOGGER.warning("Usage report rejected by the backend")
  198              return False
  199          usage_stats.commit_report(counters, now_ms)
  200          LOGGER.info("Usage report sent")
  201          return True
```


## linux/raofflineproxy/config.py @ c7ebd1b6e7+18: lines 360-385 (excerpt of 539)

```text
  360          json.dump(data, handle, indent=2, sort_keys=True)
  361          handle.write("\n")
  362  
  363  
  364  def default_proxy_port() -> int:
  365      return SPRUCE_DEFAULT_PROXY_PORT if running_on_spruce() else DEFAULT_PROXY_PORT
  366  
  367  
  368  def proxy_port(config_data: dict) -> int:
  369      raw_port = config_data.get("proxy_port", default_proxy_port())
  370      port = int(raw_port)
  371      if not (MIN_PROXY_PORT <= port <= MAX_PROXY_PORT):
  372          raise ValueError(f"Invalid proxy port: {port}")
  373      return port
  374  
  375  
  376  def proxy_host(config_data: dict) -> str:
  377      return str(config_data.get("proxy_host") or "127.0.0.1")
  378  
  379  
  380  def proxy_value(config_data: dict) -> str:
  381      return f"{proxy_host(config_data)}:{proxy_port(config_data)}"
  382  
  383  
  384  def proxy_base(config_data: dict) -> str:
  385      return f"http://{proxy_value(config_data)}"
```


## linux/raofflineproxy/es_export.py @ c7ebd1b6e7+18: lines 50-69 (excerpt of 69)

```text
   50  
   51  
   52  def _game_id_for_entry(cache_key:*** str, response_body: str) -> int | None:
   53      if cache_key.startswith(cache_keys.PREFIX_PATCH):
   54          return cache_keys.parse_game_id_from_patch_key(cache_key)
   55      return achievementsets_game_id(response_body)
   56  
   57  
   58  def _write_ids(ids: set[int]) -> None:
   59      content = "".join(f"{game_id}\n" for game_id in sorted(ids))
   60      try:
   61          if CACHED_IDS_FILE.read_text() == content:
   62              return
   63      except OSError:
   64          pass
   65  
   66      CONFIG_DIR.mkdir(parents=True, exist_ok=True)
   67      tmp_path = CACHED_IDS_FILE.with_name(CACHED_IDS_FILE.name + ".tmp")
   68      tmp_path.write_text(content)
   69      os.replace(tmp_path, CACHED_IDS_FILE)
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 1014-1072 (excerpt of 1409)

```text
 1014  	stamp.ok = true;
 1015  	stamp.when = (time_t) when;
 1016  	stamp.flushed = flushed;
 1017  	return stamp;
 1018  }
 1019  
 1020  // Moved from OfflineAchievements::scanWhy and ProxyCards' topUpWhy, so the
 1021  // table has a case (#308 follow-up): those two now ask here.
 1022  std::string CloudText::scanWhy(const std::string& token)
 1023  {
 1024  	if (token == "TOGGLE_OFF")
 1025  		return _("TURN ON OFFLINE ACHIEVEMENTS FIRST.");
 1026  	if (token == "NO_ACCOUNT")
 1027  		return _("SIGN IN TO RETROACHIEVEMENTS FIRST.");
 1028  	if (token == "SIGN_IN_REFUSED")
 1029  		return _("RETROACHIEVEMENTS DIDN'T ACCEPT YOUR SIGN-IN");
 1030  	if (token == "RETROACHIEVEMENTS_STOPPED_ANSWERING")
 1031  		return _("RETROACHIEVEMENTS STOPPED ANSWERING");
 1032  	if (token == "NO_GAMES_FOUND")
 1033  		return _("NO GAMES WERE FOUND ON THIS CONSOLE");
 1034  	if (token == "LIBRARY_UNREADABLE")
 1035  		return _("YOUR GAMES COULDN'T BE READ");
 1036  	if (token == "TOOK_TOO_LONG")
 1037  		return _("IT TOOK TOO LONG");
 1038  	// A fetch failed for some game, even among many that went through
 1039  	// (audit #186 PL-24): the run could not finish, and the next scan tries
 1040  	// those games again, since nothing marks them cached.
 1041  	if (token == "SOME_GAMES_NOT_SAVED")
 1042  		return _("SOME GAMES COULDN'T BE SAVED. TRY THE SCAN AGAIN.");
 1043  	// The image pass left achievement images behind (#307 PL-060; the ctl
 1044  	// stamps it only for a failure that may pass, so a scan can fetch them):
 1045  	// the games are cached, and the next scan tries the images again.
 1046  	// Proposed words, for the maintainer to approve.
 1047  	if (token == "SOME_IMAGES_NOT_SAVED")
 1048  		return _("SOME ACHIEVEMENT IMAGES COULDN'T BE SAVED. TRY THE SCAN AGAIN.");
 1049  	// The player's CANCEL on the scan page (D-UI-078): the ctl's INT trap
 1050  	// stamps it so the row says so; not a failure, and the next scan
 1051  	// carries on from what was saved.
 1052  	if (token == "CANCELLED")
 1053  		return _("YOU CANCELLED IT");
 1054  	return _("SOMETHING WENT WRONG");
 1055  }
 1056  
 1057  std::string CloudText::topUpWhy(const std::string& token)
 1058  {
 1059  	if (token == "SOME_GAMES_NOT_SAVED")
 1060  		return _("SOME GAMES COULDN'T BE SAVED");
 1061  	if (token == "SOME_IMAGES_NOT_SAVED")
 1062  		return _("SOME ACHIEVEMENT IMAGES COULDN'T BE SAVED");
 1063  	return scanWhy(token);
 1064  }
 1065  
 1066  // What a match that did not complete removed. The count is the one
 1067  // cloud_content_restore's ">>> removed" reports from rclone's own Deleted
 1068  // lines (stream A's 258b5eca38), no longer its plan. Nothing about the
 1069  // cloud: a match removes only what the cloud does not have (D-CLOUD-023),
 1070  // and the clause that followed -- YOUR CLOUD STILL HAS THEM -- said the
 1071  // opposite of what had happened.
 1072  std::string CloudText::matchRemovedNote(int removedFiles)
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 1178-1283 (excerpt of 1409)

```text
 1178  bool CloudText::isKnownUnitLabel(const std::string& label)
 1179  {
 1180  	for (auto& l : unitLabels())
 1181  		if (l.first == label)
 1182  			return true;
 1183  	return false;
 1184  }
 1185  
 1186  CloudText::ScanStamp CloudText::parseScanStamp(const std::string& text)
 1187  {
 1188  	ScanStamp stamp;
 1189  
 1190  	// One line: the time, the exit code and the route, then key=***
 1191  	// fields in any order. A whole number is at most twelve digits, as the
 1192  	// flush stamp's are.
 1193  	std::string line = text;
 1194  	const size_t newline = line.find('\n');
 1195  	if (newline != std::string::npos)
 1196  		line = line.substr(0, newline);
 1197  	const std::vector<std::string> fields = Utils::String::split(Utils::String::trim(line), ' ', true);
 1198  	if (fields.size() < 3)
 1199  		return stamp;
 1200  
 1201  	auto number = [](const std::string& f, long long& out) -> bool
 1202  	{
 1203  		if (f.empty() || f.size() > 12)
 1204  			return false;
 1205  		for (char c : f)
 1206  			if (c < '0' || c > '9')
 1207  				return false;
 1208  		out = std::stoll(f);
 1209  		return true;
 1210  	};
 1211  
 1212  	long long when = 0, code = 0;
 1213  	if (!number(fields[0], when) || when <= 0 || !number(fields[1], code))
 1214  		return stamp;
 1215  	if (fields[2] == "scan")
 1216  		stamp.topup = false;
 1217  	else if (fields[2] == "topup")
 1218  		stamp.topup = true;
 1219  	else
 1220  		return stamp;
 1221  
 1222  	for (size_t i = 3; i < fields.size(); i++)
 1223  	{
 1224  		const size_t eq = fields[i].find('=');
 1225  		if (eq == std::string::npos)
 1226  			continue;
 1227  		const std::string key = fields[i].substr(0, eq);
 1228  		const std::string value = fields[i].substr(eq + 1);
 1229  		if (key == "why")
 1230  		{
 1231  			// A token and nothing else: the caller maps it to a sentence,
 1232  			// and anything it does not know reads as SOMETHING WENT WRONG.
 1233  			bool token = !value.empty();
 1234  			for (char c : value)
 1235  				if (!((c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_'))
 1236  					token = false;
 1237  			if (token)
 1238  				stamp.why = value;
 1239  			continue;
 1240  		}
 1241  		if (key == "note")
 1242  		{
 1243  			// The ctl's token for a run that completed with nothing to do
 1244  			// (NO_GAMES, fork #329): a token, as why= is, or nothing.
 1245  			bool token = !value.empty();
 1246  			for (char c : value)
 1247  				if (!((c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_'))
 1248  					token = false;
 1249  			if (token)
 1250  				stamp.note = value;
 1251  			continue;
 1252  		}
 1253  		// The ctl's word for a count it could not measure (PL-031): an
 1254  		// answer of its own, where any other non-number says nothing.
 1255  		if (key == "added" && value == "unknown")
 1256  		{
 1257  			stamp.added = ScanStamp::AddedUnknown;
 1258  			continue;
 1259  		}
 1260  		long long n = 0;
 1261  		if (!number(value, n) || n > 1000000)
 1262  			continue;
 1263  		if (key == "cached")       stamp.cached = (int) n;
 1264  		else if (key == "added")   stamp.added = (int) n;
 1265  		else if (key == "skipped") stamp.skipped = (int) n;
 1266  		else if (key == "ready")   stamp.ready = (int) n;
 1267  		else if (key == "limit")   stamp.limit = n != 0;
 1268  		else if (key == "indexed") stamp.indexed = (int) n;
 1269  		else if (key == "errors")  stamp.errors = (int) n;
 1270  		else if (key == "truncated") stamp.truncated = n != 0;
 1271  	}
 1272  
 1273  	stamp.ran = true;
 1274  	stamp.when = (time_t) when;
 1275  	stamp.code = (int) code;
 1276  	return stamp;
 1277  }
 1278  
 1279  CloudText::RunningProgress CloudText::parseRunningProgress(const std::string& text, long long nowEpoch)
 1280  {
 1281  	RunningProgress run;
 1282  
 1283  	// One line of key=*** fields, in any order. A whole number is at most
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 1297-1343 (excerpt of 1409)

```text
 1297  			if (c < '0' || c > '9')
 1298  				return false;
 1299  		out = std::stoll(f);
 1300  		return true;
 1301  	};
 1302  
 1303  	bool hasAt = false;
 1304  	for (const std::string& field : fields)
 1305  	{
 1306  		// The name may carry '=' of its own: the first one splits.
 1307  		const size_t eq = field.find('=');
 1308  		if (eq == std::string::npos)
 1309  			continue;
 1310  		const std::string key = field.substr(0, eq);
 1311  		const std::string value = field.substr(eq + 1);
 1312  		if (key == "route")
 1313  			run.route = value;
 1314  		else if (key == "at")
 1315  		{
 1316  			long long at = 0;
 1317  			if (number(value, at) && at > 0)
 1318  			{
 1319  				run.at = at;
 1320  				hasAt = true;
 1321  			}
 1322  		}
 1323  		else if (key == "index" || key == "total")
 1324  		{
 1325  			long long n = 0;
 1326  			if (!number(value, n) || n > 1000000)
 1327  				continue;
 1328  			if (key == "index")
 1329  				run.index = (int) n;
 1330  			else
 1331  				run.total = (int) n;
 1332  		}
 1333  	}
 1334  
 1335  	// A file is never a run on its own: it says when the ctl last wrote it,
 1336  	// and the ctl bounds its runs, so a line older than that bound was left
 1337  	// by a run that died. A line from the future by more than a day is a
 1338  	// clock that jumped, not a run.
 1339  	if (!hasAt)
 1340  		return run;
 1341  	if (nowEpoch - run.at > RUNNING_STALE_AFTER_S || run.at - nowEpoch > RUNNING_AHEAD_LIMIT_S)
 1342  		return run;
 1343  	run.running = true;
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images @ 8ebaf8daad: lines 1-38 (excerpt of 497)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # raofflineproxy-cache-images - the images of the achievements this device has
    6  # already cached, fetched until none is missing (fork #212, D-RA-027: images
    7  # are not a separate choice; the toggle that caches a game caches its badges).
    8  #
    9  #   raofflineproxy-cache-images [--seconds N] [--verify]
   10  #
   11  # Caching a game's achievements and caching its images are one action to a
   12  # player -- "whenever we cache the achievements, we cache the images for the
   13  # achievements" (maintainer, 2026-09-18) -- and two pieces of work to this
   14  # process. The set is stored synchronously; its images go to a four-worker
   15  # pool that the scan gives one global grace of RAOFFLINEPROXY_IMAGE_WAIT
   16  # seconds (120 by default) before dropping what has not started, because the
   17  # pool's non-daemon threads once held the helper 83 s past its DONE (#188).
   18  # A library's scan queues tens of thousands of images, so the pool loses most
   19  # of them, and a miss is answered 404 at once while offline (patch 012, for
   20  # #199's stall). Measured on the maintainer's RG SP before this existed: 494
   21  # cached set rows referencing 56,111 image paths, 956 of them missing, 123 of
   22  # 494 games incomplete -- with nothing saying which.
   23  #
   24  # This walks the store instead of the library: every cached patch,
   25  # achievementsets and login2 row, every image path in it, and the ones whose
   26  # file is not in image_cache/static get fetched. Two properties make that
   27  # safe to run at the end of every scan and top-up:
   28  #
   29  #   * it is idempotent -- download_static_image no-ops on an existing file,
   30  #     and the check here is the file's existence, so a second run fetches
   31  #     nothing and costs no request;
   32  #   * it is resumable -- nothing marks a game done but its own files, so a
   33  #     run that stops at its ceiling leaves the rest for the next one.
   34  #
   35  # With --verify the files that are there are read as well as counted, and a
   36  # PNG is put to the test a download passes (image_cache.png_problem, patch
   37  # 013: every chunk's CRC up to IEND, image data that inflates) behind a
   38  # plausible size (#308 F-RA-12). Presence is what every
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images @ 8ebaf8daad: lines 126-220 (excerpt of 497)

```text
  126  IMAGE_ABSENT = getattr(image_cache, "IMAGE_ABSENT", "absent")
  127  
  128  # Smaller than any real badge: a PNG needs a signature, an IHDR and an IEND,
  129  # and the smallest one RetroAchievements serves is a few hundred bytes (of a
  130  # 4,000-badge sample on the maintainer's device the smallest was 266).
  131  PNG_FLOOR = 68
  132  
  133  
  134  def damaged(path: str) -> str | None:
  135      """Why the cached file for path is not a whole image, or None if it is.
  136  
  137      A .png is put to the test a download passes before it is published
  138      (image_cache.png_problem, patch 013): every chunk's CRC up to IEND and
  139      image data that inflates, so a file damaged inside -- written before
  140      patch 013 checked anything, or by a card since -- is found and fetched
  141      again, not only one cut short; and a whole PNG with bytes after its
  142      IEND is whole, where a trailer test called it damaged and deleted it at
  143      every pass (#308 F-RA-12, F-RA-13).
  144      """
  145      target = image_cache.resolve_cached_static_asset(path)
  146      if target is None:
  147          return "absent"
  148      try:
  149          size = target.stat().st_size
  150          if not path.lower().endswith(".png"):
  151              return None if size > 0 else "empty"
  152          if size < PNG_FLOOR:
  153              return f"tiny({size})"
  154          return image_cache.png_problem(target.read_bytes())
  155      except OSError as exc:
  156          return f"unreadable ({exc})"
  157  
  158  
  159  # The cursor holds a path in the same shape as the rest of this script --
  160  # with its leading slash, as extract_image_path gives it -- so the string
  161  # comparison that resumes the sweep compares like with like.
  162  def read_cursor() -> str:
  163      try:
  164          return CURSOR.read_text(encoding="utf-8").strip()
  165      except OSError:
  166          return ""
  167  
  168  
  169  def write_cursor(value: str) -> None:
  170      try:
  171          CURSOR.parent.mkdir(parents=True, exist_ok=True)
  172          if value:
  173              CURSOR.write_text(value + "\n", encoding="utf-8")
  174          else:
  175              CURSOR.unlink(missing_ok=True)
  176      except OSError as exc:
  177          note(f"the verify cursor could not be written: {exc}")
  178  
  179  
  180  def read_absent() -> dict[str, int]:
  181      """{path: when it was found absent}, the entries not yet due a recheck."""
  182      found: dict[str, int] = {}
  183      try:
  184          text = ABSENT_FILE.read_text(encoding="utf-8")
  185      except OSError:
  186          return found
  187      now = int(time.time())
  188      for line in text.splitlines():
  189          stamp, _, path = line.partition(" ")
  190          if stamp.isdigit() and path.startswith("/") and now - int(stamp) < ABSENT_RECHECK_SECONDS:
  191              found[path] = int(stamp)
  192      return found
  193  
  194  
  195  def write_absent(entries: dict[str, int]) -> None:
  196      """The absent record, whole or not at all."""
  197      try:
  198          ABSENT_FILE.parent.mkdir(parents=True, exist_ok=True)
  199          tmp = ABSENT_FILE.with_name(ABSENT_FILE.name + ".tmp")
  200          tmp.write_text("".join(f"{stamp} {path}\n" for path, stamp in sorted(entries.items())), encoding="utf-8")
  201          os.replace(tmp, ABSENT_FILE)
  202      except OSError as exc:
  203          note(f"the absent record could not be written: {exc}")
  204  
  205  
  206  def tell(text: str) -> None:
  207      print(">>> " + text, flush=True)
  208  
  209  
  210  def note(text: str) -> None:
  211      print(text, file=sys.stderr, flush=True)
  212  
  213  
  214  def image_paths(body: str) -> set[str]:
  215      """Every /Badge/, /Images/ or /UserPic/ path a stored body refers to.
  216  
  217      The stored body has been rewritten to point at this proxy, so the strings
  218      read http://127.0.0.1:8080/Badge/1.png rather than the media host's URL;
  219      extract_image_path takes the path out of either shape. A body is walked
  220      rather than pattern-matched so a field this does not know about still
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images @ 8ebaf8daad: lines 263-328 (excerpt of 497)

```text
  263              if not body:
  264                  continue
  265              rows += 1
  266              seen |= image_paths(body)
  267      missing = [p for p in sorted(seen) if image_cache.resolve_cached_static_asset(p) is None]
  268      return missing, len(seen), rows
  269  
  270  
  271  def main() -> int:
  272      parser = argparse.ArgumentParser(add_help=False)
  273      parser.add_argument("--seconds", type=float, default=300.0)
  274      parser.add_argument("--verify", action="store_true")
  275      parser.add_argument("-h", "--help", action="store_true")
  276      args = parser.parse_args()
  277      if args.help:
  278          print(__doc__ or "usage: raofflineproxy-cache-images [--seconds N]")
  279          return 0
  280  
  281      configure_logging()
  282      config_data = load_config()
  283  
  284      tell("doing images")
  285      try:
  286          storage = Storage()
  287      except Exception as exc:
  288          note(f"the store could not be opened: {exc}")
  289          tell("why STORE_UNREADABLE")
  290          return 2
  291  
  292      try:
  293          credentials = resolve_credentials(storage, config_data, self_user_agent())
  294      except Exception as exc:
  295          note(f"no account to fetch as: {exc}")
  296          tell("why NO_ACCOUNT")
  297          return 2
  298      if not credentials or not credentials.get("user"):
  299          tell("why NO_ACCOUNT")
  300          return 2
  301  
  302      user_agent = proxy_user_agent(self_user_agent())
  303  
  304      # One budget for the run, not one per phase: the top-up hands us the
  305      # seconds it has left, so a verify that took all of them and a fetch
  306      # that then took all of them again would overrun the caller twice over.
  307      # Verify gets at most half, so the fetch always gets a turn.
  308      budget_end = time.monotonic() + max(1.0, args.seconds)
  309      verify_deadline = min(budget_end, time.monotonic() + max(1.0, args.seconds) / 2)
  310      damaged_found: list[str] = []
  311      verify_left = 0
  312      if args.verify:
  313          try:
  314              paths = sorted(all_paths(storage))
  315          except Exception as exc:
  316              note(f"the store could not be read: {exc}")
  317              tell("why STORE_UNREADABLE")
  318              return 2
  319          cursor = read_cursor()
  320          start = 0
  321          if cursor:
  322              for index, path in enumerate(paths):
  323                  if path > cursor:
  324                      start = index
  325                      break
  326              else:
  327                  start = len(paths)
  328          checked = 0
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images @ 8ebaf8daad: lines 333-349 (excerpt of 497)

```text
  333              if why is not None and why != "absent":
  334                  note(f"{path}: {why}")
  335                  damaged_found.append(path)
  336                  # Drop it, so the fetch below treats it as missing and the
  337                  # cache never keeps a file it has just called damaged.
  338                  target = image_cache.resolve_cached_static_asset(path)
  339                  if target is not None:
  340                      try:
  341                          target.unlink()
  342                      except OSError as exc:
  343                          note(f"{path}: could not be removed ({exc})")
  344              checked += 1
  345              index += 1
  346              if checked % 500 == 0:
  347                  tell(f"verified {checked}|{len(paths) - start}")
  348              if time.monotonic() > verify_deadline:
  349                  break
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images @ 8ebaf8daad: lines 387-488 (excerpt of 497)

```text
  387      done = 0
  388      stopped = False
  389  
  390      # The pool the proxy uses for its own images, four workers, so this asks
  391      # RetroAchievements' media host no harder than a launch does. Not a
  392      # with-block: its exit is shutdown(wait=True), which runs every queued
  393      # download to completion, so the page's CANCEL -- a KeyboardInterrupt
  394      # here, from the SIGINT the interface sends the run's process group --
  395      # waited for all of them, tens of thousands on a first scan, before the
  396      # run could stop (#307 PL-013). A cancel drops what has not started and
  397      # leaves at once (leave(), below).
  398      pool = ThreadPoolExecutor(max_workers=4)
  399      futures = {}
  400      try:
  401          for path in missing:
  402              # extract_image_path hands back the path with its leading slash
  403              # ("/Badge/109361.png"), which is the shape the client's own
  404              # cache uses, so the URL is the media host and that path with
  405              # nothing between them.
  406              futures[pool.submit(
  407                  image_cache.download_static_image,
  408                  f"{RA_MEDIA_HOST}{path}",
  409                  path,
  410                  user_agent,
  411              )] = path
  412          # The deadline bounds the wait itself (#308 F-RA-10): as_completed
  413          # with no timeout waited for the next download to finish before the
  414          # deadline could be looked at, and a download that hangs holds that
  415          # wait for as long as its own timeouts allow.
  416          try:
  417              for future in as_completed(futures, timeout=max(0.0, deadline - time.monotonic())):
  418                  path = futures[future]
  419                  done += 1
  420                  outcome = None
  421                  try:
  422                      outcome = future.result()
  423                  except Exception as exc:  # download_static_image swallows its own
  424                      note(f"{path}: {exc}")
  425                  if image_cache.resolve_cached_static_asset(path) is not None:
  426                      fetched += 1
  427                  elif outcome == IMAGE_ABSENT:
  428                      absent[path] = int(time.time())
  429                      note(f"{path}: the image server does not have it (404 or 410); recorded absent, not asked for again")
  430                  elif outcome is not None:
  431                      note(f"{path}: not cached ({outcome}); asked for again next pass")
  432                  if done % 25 == 0 or done == len(missing):
  433                      tell(f"image {done}|{len(missing)}")
  434                  if time.monotonic() > deadline:
  435                      stopped = True
  436                      break
  437          except FuturesTimeout:
  438              stopped = True
  439      except KeyboardInterrupt:
  440          pool.shutdown(wait=False, cancel_futures=True)
  441          raise
  442      # Drop what has not started. What is in flight carries its own timeout
  443      # and is not waited for either (leave(), below): the next run picks up
  444      # whatever did not land.
  445      pool.shutdown(wait=False, cancel_futures=True)
  446      running = any(not future.done() for future in futures)
  447  
  448      if absent != absent_before:
  449          write_absent(absent)
  450      # Left behind: not there and not absent -- what the next pass asks for,
  451      # and what makes this one a failure.
  452      left = [p for p in missing if image_cache.resolve_cached_static_asset(p) is None and p not in absent]
  453      newly_absent = len(absent) - len(absent_before)
  454      note(
  455          f"fetched {fetched}, {newly_absent} absent, still missing {len(left)}"
  456          f"{' (stopped at the ceiling)' if stopped else ''}"
  457          f"{f'; {len(damaged_found)} were damaged and re-fetched' if damaged_found else ''}"
  458      )
  459      if left:
  460          tell("why SOME_IMAGES_NOT_SAVED")
  461      tell(f"done {fetched}|{len(left)}")
  462      code = 1 if left else (3 if verify_left else 0)
  463      if running:
  464          leave(code)
  465      return code
  466  
  467  
  468  def leave(code: int) -> None:
  469      """End the process now, without waiting for downloads still running on
  470      the pool's threads. Each carries its own timeout, fetches into memory and
  471      writes a temp name of its own only once the whole image has arrived and
  472      passed patch 013's test, then renames it (patches 009, 013), so one cut
  473      short leaves nothing the next pass does not fetch."""
  474      sys.stdout.flush()
  475      sys.stderr.flush()
  476      os._exit(code)
  477  
  478  
  479  if __name__ == "__main__":
  480      # Under the ctl this runs beneath timeout, which puts it in a process
  481      # group of its own: the scan page's CANCEL -- a SIGINT to the run's group
  482      # -- reaches the ctl and not this process, and the ctl's EXIT trap ends
  483      # it by SIGTERM through timeout (the default action, at once). The
  484      # SIGINT handling here is for the helper started any other way: by hand,
  485      # or by a caller that does signal its group. A shell starts a background
  486      # job with SIGINT ignored, which Python keeps, so it is taken back; a
  487      # KeyboardInterrupt then drops the queued downloads and leaves without
  488      # the ones in flight (#307 PL-013; the shipped path is the harness's
```


## projects/ROCKNIX/packages/network/raofflineproxy/package.mk @ 8ebaf8daad: lines 1-41 (excerpt of 157)

```text
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="raofflineproxy"
    5  # Current upstream main at2026-10-11 (#541); retain the fork's preparation,
    6  # recovery and explicit-consent behavior. The16 patches apply at fuzz0 after
    7  # rebasing context against the new folder watcher and paced background queue.
    8  # The OS's deliberate whole-library helper retains its own existing cooldown
    9  # after upstream removed that utility; it never labels queued work ready.
   10  # Coupled rcheevos/libchdr pins are unchanged in this parent (D-RA-029/037).
   11  # Source tests and installed-image proof remain separately recorded.
   12  PKG_VERSION="c7ebd1b6e777f3751ff0ecdf8aba54045844e00d"
   13  PKG_SHA256="88eef31acfa4104b20258bd5cea514ade30e6cdf35767ffc958009851d61898b"
   14  # GPLv3 text with no "or any later version" grant in the sources.
   15  PKG_LICENSE="GPL-3.0-only"
   16  PKG_SITE="https://github.com/misantronic/RAOfflineProxy"
   17  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
   18  # Python3 is the interpreter, and its host build carries the compileall that
   19  # python_compile runs; the service itself is stdlib-only (argparse, sqlite3,
   20  # ssl, hmac, http, socketserver, ...), all of it in the image's lib-dynload.
   21  # raofflineproxy-rcheevos and raofflineproxy-libchdr are the two submodules
   22  # the proxy's tarball leaves empty, pinned to the commits it names; make_target
   23  # below compiles them with the glue into libraproxy_rchash.so (fork #179).
   24  # And the packages whose tools the shipped scripts call (packaging-and-patches:
   25  # a shipped script's tools are dependencies too; #308 F-RA-23, F-RA-24): bash,
   26  # raofflineproxy-ctl's interpreter; busybox for flock, mkfifo, mktemp, stat,
   27  # logger, sed, awk, head, tail, date and sleep; coreutils for timeout (the
   28  # image's is coreutils', not a busybox link); grep, GNU's (the image's busybox
   29  # has no grep applet); systemd for systemctl.
   30  PKG_DEPENDS_TARGET="toolchain Python3 bash busybox coreutils grep systemd raofflineproxy-rcheevos raofflineproxy-libchdr"
   31  PKG_LONGDESC="RAOfflineProxy: a loopback proxy between the emulators and retroachievements.org that caches game data and queues casual awards earned without a connection, and sends them when one returns. Approved by RetroAchievements.org; casual (softcore) achievements only."
   32  PKG_TOOLCHAIN="manual"
   33  PKG_BUILD_FLAGS="+pic"
   34  
   35  # OFFLINE RETROACHIEVEMENTS (fork #163/#165, D-RA-001, D-RA-002).
   36  #
   37  # What ships is the service and nothing around it: linux/raofflineproxy as a
   38  # Python module in the image's site-packages, byte-compiled like the stdlib
   39  # (the image carries .pyc only and the root filesystem is read-only, so
   40  # uncompiled sources would recompile at every start), a systemd unit gated on
   41  # the same kind of marker avahi and sshd use, and raofflineproxy-ctl, the
```


## projects/ROCKNIX/packages/network/raofflineproxy/package.mk @ 8ebaf8daad: lines 108-157 (excerpt of 157)

```text
  108      "${CHDR}/src/libchdr_flac.c" \
  109      "${CHDR}/src/libchdr_huffman.c" \
  110      "${CHDR}/deps/miniz-3.1.2/miniz.c" \
  111      "${CHDR}/deps/lzma-26.02/src/LzmaDec.c" \
  112      "${CHDR}/deps/zstd-1.5.7/zstddeclib.c" \
  113      "${LZMA_SDK}"/*.c
  114  }
  115  
  116  makeinstall_target() {
  117    local SITE="${INSTALL}/usr/lib/${PKG_PYTHON_VERSION}/site-packages"
  118    mkdir -p "${SITE}"
  119    cp -r "${PKG_BUILD}/linux/raofflineproxy" "${SITE}/raofflineproxy"
  120    rm -rf "${SITE}/raofflineproxy/__pycache__"
  121    # The SDL menu's fonts and donation QR images. menu_sdl.py only names the
  122    # paths at import; nothing on this image draws that menu.
  123    rm -rf "${SITE}/raofflineproxy/assets"
  124    rm -f "${SITE}"/raofflineproxy/font-mono*.ttf
  125    python_compile "${SITE}/raofflineproxy"
  126  
  127    mkdir -p "${INSTALL}/usr/bin"
  128    cp "${PKG_DIR}/sources/raofflineproxy-ctl" "${INSTALL}/usr/bin/raofflineproxy-ctl"
  129    chmod 0755 "${INSTALL}/usr/bin/raofflineproxy-ctl"
  130    # The scan's worker (fork #184, D-RA-013): caches a game the interface's
  131    # index already identified from its id and hash, and hands the rest to the
  132    # client's own hashing path. The ctl looks for it beside itself.
  133    cp "${PKG_DIR}/sources/raofflineproxy-cache-indexed" "${INSTALL}/usr/bin/raofflineproxy-cache-indexed"
  134    chmod 0755 "${INSTALL}/usr/bin/raofflineproxy-cache-indexed"
  135  
  136    # The images of what is cached, fetched until none is missing (#212): the
  137    # same action as caching the achievements, run at the end of a scan and a
  138    # top-up and available on its own as `raofflineproxy-ctl images`.
  139    cp "${PKG_DIR}/sources/raofflineproxy-cache-images" "${INSTALL}/usr/bin/raofflineproxy-cache-images"
  140    chmod 0755 "${INSTALL}/usr/bin/raofflineproxy-cache-images"
  141    cp "${PKG_DIR}/sources/raofflineproxy-refresh" "${INSTALL}/usr/bin/raofflineproxy-refresh"
  142    chmod 0755 "${INSTALL}/usr/bin/raofflineproxy-refresh"
  143  
  144    # /usr/lib is the first system path rom_hashing.py's loader tries after the
  145    # module's own directory.
  146    mkdir -p "${INSTALL}/usr/lib"
  147    cp "${PKG_BUILD}/.${TARGET_NAME}/libraproxy_rchash.so" "${INSTALL}/usr/lib/libraproxy_rchash.so"
  148    chmod 0644 "${INSTALL}/usr/lib/libraproxy_rchash.so"
  149  }
  150  
  151  post_install() {
  152    # Enabled in the image; the unit's ConditionPathExists on
  153    # /storage/.cache/services/raofflineproxy.conf is the off-switch, and
  154    # raofflineproxy-ctl (and, at boot, /usr/lib/autostart/daemons) owns that
  155    # marker.
  156    enable_service raofflineproxy.service
  157  }
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 1-48 (excerpt of 2455)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # raofflineproxy-ctl - the backend of the OFFLINE RETROACHIEVEMENTS toggle
    6  # (fork #165; D-RA-001, D-RA-002). One system-wide switch, off by default:
    7  #
    8  #   enable   write the on-marker the unit conditions on, start the service,
    9  #            then in system.cfg record the hardcore setting as it was
   10  #            (once -- a second enable keeps the first record), turn hardcore
   11  #            off and set the toggle -- the toggle last, each write read back
   12  #            before the next, and a step that does not hold undoes every
   13  #            step this run made before it (audit #186 PL-16): a failed
   14  #            enable leaves the device exactly as it was, the toggle off. The
   15  #            proxy is casual-only and refuses hardcore awards, so the switch
   16  #            is made here, on purpose, with the sentence on screen in
   17  #            EmulationStation -- never silently.
   18  #   disable  clear the toggle, stop a scan or top-up still running (it is
   19  #            signalled through the pid in its lock file and given STOP_WAIT
   20  #            seconds; #186 PL-30), stop the service, remove the marker, and
   21  #            put hardcore back the way the record says it was; the record
   22  #            goes. Each step is read back before the next uses it up: a
   23  #            toggle that will not clear stops nothing, and a hardcore that
   24  #            will not go back keeps the record for the next disable (#308
   25  #            F-RA-18).
   26  #   start    systemctl start; the marker must already be there.
   27  #   stop     systemctl stop.
   28  #   status   enabled=, marker=, service=, hardcore= on stdout; exit 0 when the
   29  #            toggle is on, 1 when off.
   30  #   pending  how many casual awards the proxy is holding for the next
   31  #            connection: the count of pending rows in its store, on one
   32  #            line; exit 0 when there is at least one, 1 when none. With the
   33  #            toggle off the answer is 0: the service is stopped, so a row
   34  #            left in the store is not on its way anywhere, and the sentence
   35  #            the count feeds ("... WILL BE SENT NEXT TIME YOU'RE CONNECTED")
   36  #            would be a promise nobody keeps. Exit 2, nothing on stdout,
   37  #            when the store could not be read -- an unknown count is never
   38  #            reported as one, so nothing is promised on its strength.
   39  #   flushed  the stamp the service leaves after a flush that sent awards
   40  #            (patches/003: "<epoch> <flushed>", once per such flush),
   41  #            printed as written and removed, exit 0; exit 1 when there is
   42  #            none, or none worth the name. Whoever asks is told once: the
   43  #            stamp is taken (renamed) before it is read, so one the service
   44  #            writes a moment later is the next caller's, and two callers
   45  #            cannot both report the same one (#186 PL-32).
   46  #
   47  #   EmulationStation asks pending as the exit sync card ends and flushed as
   48  #   the next sync card that reached the network does (fork #173, D-RA-004);
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 247-388 (excerpt of 2455)

```text
  247  # Storage twice, preserving cache/login/base/subset award bytes: pending_awards(id,
  248  # achievementId, queryString, requestBody, queuedAt, status) for pending,
  249  # pending-ids and summary; api_cache(cacheKey, responseBody, sourceRomPath,
  250  # cachedAt) for account, summary, the ready set behind added= and the
  251  # scan's "already cached" test, the keys as cache_keys.py spells them
  252  # (login2::<user>, patch:<id>:<user>, unlocks:<id>:<user>:0,
  253  # achievementsets:<hash>:<user>). The client carries no schema version row
  254  # (an upstream item, #186 PL-22); a schema it changes shows here as
  255  # cannot_tell (exit 2), never as a number -- and first in the scripts
  256  # suite, which runs these reads against a store the pinned client's own
  257  # Storage wrote and checks that this paragraph names the pin package.mk
  258  # pins, so a pin that moves makes somebody read the schema again.
  259  
  260  # Machine-facing. The last line of stdout after enable or disable is
  261  # hardcore=<0|1>, the setting as it stands afterwards; EmulationStation
  262  # reads it to keep its HARDCORE MODE row truthful. Everything else goes to
  263  # the log. Exit 0 when done, 1 when a step could not be made to hold, 2 on
  264  # usage or when an answer could not be read; scan and topup add the four
  265  # sysexits codes above, which CloudExit.h in EmulationStation spells the
  266  # same way.
  267  
  268  # No set -u: get_setting and set_setting come from /etc/profile and read
  269  # positional parameters they were not given; every value this script relies
  270  # on is read back and tested below instead.
  271  . /etc/profile
  272  
  273  MARKER_DIR="/storage/.cache/services"
  274  MARKER="${MARKER_DIR}/raofflineproxy.conf"
  275  UNIT="raofflineproxy.service"
  276  KEY=***
  277  HARDCORE_KEY=***
  278  HARDCORE_WAS_KEY=***
  279  # Where the service keeps everything it writes: RAOFFLINEPROXY_CONFIG_DIR in
  280  # the unit, and the default the proxy resolves on a ROCKNIX image without it.
  281  PROXY_DIR="/storage/.config/raofflineproxy"
  282  QUEUE="${PROXY_DIR}/proxy.sqlite3"
  283  FLUSH_STAMP="${PROXY_DIR}/last-flush"
  284  
  285  # The scan's files, all beside the proxy's own so backuptool holds them back
  286  # with the rest (D-INFRA-010) and `disable` leaves them where the cache is.
  287  SCAN_STAMP="${PROXY_DIR}/last-scan"
  288  # Where the walk over unindexed folders stopped at the cap, so the next scan
  289  # walks on from there (#307 PL-059): the path of the last file it took.
  290  SCAN_CURSOR="${PROXY_DIR}/scan-cursor"
  291  SCAN_LOG="${PROXY_DIR}/scan.log"
  292  RUNNING="${PROXY_DIR}/running"
  293  TOPUP_MARK="${PROXY_DIR}/last-topup-attempt"
  294  # An index run that could not reach RetroAchievements (a game list updated
  295  # offline) leaves this, and the next link-return run lists the library
  296  # once for it, so the games an index identified while the device was
  297  # offline are cached when it is next online (fork #299; the games an index
  298  # could not identify are the interface's next index's, #308 F-RA-22). It is
  299  # removed only by a run whose listing and indexed pass both went through, so
  300  # a run that fails or is stopped part-way leaves it for the next (#307
  301  # PL-055).
  302  INDEX_PENDING="${PROXY_DIR}/index-pending"
  303  READY_FILE="${PROXY_DIR}/cached_game_ids.txt"
  304  SCAN_LOCK="/var/run/raofflineproxy-scan.lock"
  305  ROMS_ROOT="/storage/roms"
  306  # The interface's own folder: es_systems.cfg, and the two places its game
  307  # index is kept on disk (gamelists/<system>/ and recovery/<system>/).
  308  ES_DIR="/storage/.config/emulationstation"
  309  # The account keys EmulationStation writes (the token after a sign-in). Read
  310  # for presence only, never printed.
  311  USER_KEY=***
  312  TOKEN_KEY=***
  313  PASSWORD_KEY=***
  314  
  315  # sysexits.h, as CloudExit.h names them: a run that did nothing, and why.
  316  EX_USAGE=64         # a bad argument; the usage line was printed (refresh, audit #258 PL-012)
  317  EX_UNAVAILABLE=69   # offline by the proxy's probe
  318  EX_TEMPFAIL=75      # another scan or top-up holds the lock
  319  EX_NOPERM=77        # no RetroAchievements account signed in
  320  EX_CONFIG=78        # the toggle is off
  321  
  322  # The top-up's probe schedule: the token check's (#175, CheevosRetry.h --
  323  # nine tries ten seconds apart), for the same reason: the hook fires when
  324  # the address arrives, and a hotspot's resolver answers 20-45 s later.
  325  PROBE_TRIES=9
  326  PROBE_INTERVAL=10
  327  # How long disable waits for a scan or top-up it has asked to stop.
  328  STOP_WAIT=10
  329  # Lookups RetroAchievements did not answer, in a row, before the scan stops
  330  # asking: every one is a request spent on a link or a sign-in that is not
  331  # working, and the page can say so sooner.
  332  ERRORS_IN_A_ROW=3
  333  # One automatic top-up attempt per this many seconds, and no single run
  334  # longer than TOPUP_TIMEOUT: a link that flaps must not turn into a request
  335  # storm, and a hook that never returns is a hook nobody can reason about.
  336  TOPUP_INTERVAL=1800
  337  TOPUP_TIMEOUT=900
  338  
  339  # The client resolves its folder the way the unit sets it, and RetroArch's
  340  # `~` in content_history_path and playlist_directory is /storage on ROCKNIX
  341  # (the proxy expands it with HOME, and EmulationStation's may differ).
  342  export RAOFFLINEPROXY_CONFIG_DIR="${PROXY_DIR}"
  343  export HOME=/storage
  344  export XDG_CONFIG_HOME=/storage/.config
  345  PROXY_PY="python3 -m raofflineproxy.main"
  346  
  347  # The ROCKNIX ROM folders of the systems RetroAchievements has sets for, by
  348  # RetroAchievements' console list (2026-09) mapped onto the folder names
  349  # es_systems.cfg uses on this image, both spellings where two images differ
  350  # (coleco/colecovision, odyssey/odyssey2, pc88/pc-8800, fbneo/fbn,
  351  # sgfx/supergrafx). A folder that is not here is never walked: the proxy
  352  # would only hash it and be told no, one request per file, and a computer
  353  # or Windows library can be tens of gigabytes. Arcade folders hash by file
  354  # name (rc_hash's arcade rule), so they cost no reading. The hack folders
  355  # (nesh, snesh, ...) stay: RetroAchievements has sets for many hacks, and
  356  # the ones it does not know are skipped like any other ROM.
  357  SCAN_SYSTEMS="
  358    nes famicom fds nesh snes sfc snesh snesmsu1 satellaview sufami
  359    gb gbh gbc gbch gba gbah n64 n64dd nds ndsiware gamecube wii
  360    pokemini virtualboy megaduck supervision arduboy wasm4 uzebox
  361    channelf odyssey odyssey2 videopac intellivision coleco colecovision vectrex
  362    mastersystem megadrive genesis megadrive-japan megadriveh genh sega32x
  363    segacd megacd saturn dreamcast gamegear gamegearh ggh sg-1000
  364    psx ps2 psp pspminis
  365    atari2600 atari7800 atarijaguar atarijaguarcd atarilynx
  366    pcengine tg16 pcenginecd tg16cd sgfx supergrafx pcfx pc88 pc-8800
  367    ngp ngpc neocd wonderswan wonderswancolor msx msx2 amstradcpc apple2 3do
  368    arcade mame fbneo fbn neogeo cps1 cps2 cps3
  369  "
  370  
  371  say() {
  372      logger -t raofflineproxy-ctl "$*"
  373  }
  374  
  375  fail() {
  376      say "$*"
  377      echo "raofflineproxy-ctl: $*" >&2
  378      exit 1
  379  }
  380  
  381  # A setting as system.cfg holds it; empty when absent.
  382  setting() {
  383      get_setting "${1}"
  384  }
  385  
  386  # 0 or 1, from a value that may be empty or anything else.
  387  as_flag() {
  388      if [ "${1:-}" = "1" ]; then echo 1; else echo 0; fi
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 397-578 (excerpt of 2455)

```text
  397          systemctl is-active "${UNIT}" 2>/dev/null || true
  398      else
  399          echo unknown
  400      fi
  401  }
  402  
  403  do_start() {
  404      have_systemctl || fail "no systemctl to start ${UNIT} with"
  405      systemctl start "${UNIT}" || fail "${UNIT} did not start"
  406  }
  407  
  408  do_stop() {
  409      have_systemctl || return 0
  410      systemctl stop "${UNIT}" || say "${UNIT} did not stop cleanly; carrying on"
  411  }
  412  
  413  # What this run of enable changed, for enable_undo to put back: the marker
  414  # and the service only when this run made or started them (a second enable
  415  # finds both in place and leaves them), the record only when this run wrote
  416  # it, and each setting's value from before the run.
  417  E_MARKER_WAS=0; E_SERVICE_WAS=0; E_STARTED=0; E_RECORD_WROTE=0
  418  E_HARDCORE_BEFORE=""; E_HARDCORE_CHANGED=0; E_KEY_BEFORE=""; E_KEY_CHANGED=0
  419  
  420  # A setting back to what it was: its old value, or gone when it had none.
  421  put_back() {
  422      if [ -n "${2}" ]; then set_setting "${1}" "${2}"; else set_setting "${1}" default; fi
  423  }
  424  
  425  # A step of enable did not hold: undo every step this run made, in the
  426  # order that keeps the device consistent at each point -- the toggle first
  427  # (the launchers and the boot pass read it and nothing else), the settings,
  428  # then the service and the marker -- and fail. A device on which enable
  429  # failed is a device on which enable never ran (#186 PL-16).
  430  enable_undo() {
  431      say "enable: $*; putting the device back as it was"
  432      [ "${E_KEY_CHANGED}" -eq 1 ] && put_back "${KEY}" "${E_KEY_BEFORE}"
  433      [ "${E_HARDCORE_CHANGED}" -eq 1 ] && put_back "${HARDCORE_KEY}" "${E_HARDCORE_BEFORE}"
  434      [ "${E_RECORD_WROTE}" -eq 1 ] && set_setting "${HARDCORE_WAS_KEY}" default
  435      [ "${E_STARTED}" -eq 1 ] && [ "${E_SERVICE_WAS}" -eq 0 ] && do_stop
  436      [ "${E_MARKER_WAS}" -eq 0 ] && rm -f "${MARKER}"
  437      fail "$*"
  438  }
  439  
  440  do_enable() {
  441      E_KEY_BEFORE="$(setting "${KEY}")"
  442      E_HARDCORE_BEFORE="$(setting "${HARDCORE_KEY}")"
  443      [ -e "${MARKER}" ] && E_MARKER_WAS=1
  444      [ "$(service_state)" = "active" ] && E_SERVICE_WAS=1
  445  
  446      # The marker first, the service second: if the service cannot start,
  447      # nothing about the player's settings has changed yet, and the marker
  448      # goes again so the next boot does not start what could not run now.
  449      mkdir -p "${MARKER_DIR}" || fail "cannot create ${MARKER_DIR}"
  450      touch "${MARKER}" || fail "cannot write ${MARKER}"
  451      if have_systemctl; then
  452          if ! systemctl start "${UNIT}"; then
  453              [ "${E_MARKER_WAS}" -eq 0 ] && rm -f "${MARKER}"
  454              fail "${UNIT} did not start; the toggle stays off"
  455          fi
  456          E_STARTED=1
  457      fi
  458  
  459      # Then the settings, each read back before the next is written, the
  460      # toggle last of all: until it reads 1 nothing routes through the proxy,
  461      # so a failure anywhere before it leaves the device as it was once
  462      # enable_undo has run, and a failure after it cannot happen -- it is
  463      # the last write.
  464      #
  465      # Record hardcore as it was, once. A second enable finds the record and
  466      # keeps it, so the value disable puts back is the player's and not the 0
  467      # the first enable wrote.
  468      if [ -z "$(setting "${HARDCORE_WAS_KEY}")" ]; then
  469          set_setting "${HARDCORE_WAS_KEY}" "$(as_flag "${E_HARDCORE_BEFORE}")"
  470          E_RECORD_WROTE=1
  471          [ -n "$(setting "${HARDCORE_WAS_KEY}")" ] || enable_undo "${HARDCORE_WAS_KEY} did not take"
  472      fi
  473      set_setting "${HARDCORE_KEY}" 0
  474      E_HARDCORE_CHANGED=1
  475      [ "$(setting "${HARDCORE_KEY}")" = "0" ] || enable_undo "${HARDCORE_KEY} did not take"
  476      set_setting "${KEY}" 1
  477      E_KEY_CHANGED=1
  478      [ "$(setting "${KEY}")" = "1" ] || enable_undo "${KEY} did not take"
  479      [ -e "${MARKER}" ] || enable_undo "${MARKER} is gone"
  480  
  481      say "offline RetroAchievements on: hardcore was $(setting "${HARDCORE_WAS_KEY}"), now 0; ${UNIT} $(service_state)"
  482      echo "hardcore=0"
  483  }
  484  
  485  # A scan or top-up the interface started is no child of this process; its
  486  # lock file carries its pid (take_lock writes it), so it is asked to stop
  487  # (SIGTERM: its trap ends the helper and cleans up) and given STOP_WAIT
  488  # seconds to let go of the lock. Nothing else is matched by name or pattern.
  489  # Exit 0 when nothing was running or it stopped, 1 when it did not.
  490  stop_running_run() {
  491      [ -e "${SCAN_LOCK}" ] || return 0
  492      exec 7<>"${SCAN_LOCK}" || return 0
  493      if flock -n 7; then exec 7>&-; return 0; fi
  494      local PID WAITED=0
  495      PID="$(head -n 1 "${SCAN_LOCK}" 2>/dev/null)"
  496      case "${PID}" in ''|*[!0-9]*) PID="" ;; esac
  497      if [ -n "${PID}" ]; then
  498          say "disable: a scan or top-up is running (pid ${PID}); asking it to stop"
  499          kill -TERM "${PID}" 2>/dev/null
  500      else
  501          say "disable: a scan or top-up holds the lock and left no pid; waiting for it"
  502      fi
  503      until flock -n 7; do
  504          if [ "${WAITED}" -ge "${STOP_WAIT}" ]; then
  505              say "disable: the running scan or top-up did not stop within ${STOP_WAIT}s; carrying on"
  506              exec 7>&-
  507              return 1
  508          fi
  509          sleep 1
  510          WAITED=$((WAITED + 1))
  511      done
  512      exec 7>&-
  513      say "disable: the running scan or top-up stopped"
  514      return 0
  515  }
  516  
  517  do_disable() {
  518      # The toggle first: a scan or top-up starting from now on is refused by
  519      # its own check, and the launchers route direct from the next launch.
  520      # Each step is read back before the next one uses it up (#308 F-RA-18):
  521      # a toggle that did not clear stops nothing, so the device stays on --
  522      # service, marker and record together -- rather than half off.
  523      set_setting "${KEY}" 0
  524      [ "$(setting "${KEY}")" = "0" ] || fail "${KEY} did not clear; the service, the marker and the hardcore record are left as they were"
  525      stop_running_run
  526      do_stop
  527      rm -f "${MARKER}"
  528  
  529      # Put hardcore back as the record says, and remove the record only once
  530      # hardcore reads back as it says: a write that did not hold keeps the
  531      # record, so the next disable can still put the player's setting back
  532      # (#308 F-RA-18). No record -- a device that never had the toggle on, or
  533      # a second disable -- leaves it alone.
  534      local WAS
  535      WAS="$(setting "${HARDCORE_WAS_KEY}")"
  536      if [ -n "${WAS}" ]; then
  537          set_setting "${HARDCORE_KEY}" "$(as_flag "${WAS}")"
  538          [ "$(setting "${HARDCORE_KEY}")" = "$(as_flag "${WAS}")" ] || fail "${HARDCORE_KEY} was not put back; the record is kept for the next disable"
  539          set_setting "${HARDCORE_WAS_KEY}" default
  540          [ -z "$(setting "${HARDCORE_WAS_KEY}")" ] || fail "${HARDCORE_WAS_KEY} was not cleared"
  541      fi
  542  
  543      [ ! -e "${MARKER}" ] || fail "${MARKER} could not be removed"
  544  
  545      say "offline RetroAchievements off: hardcore ${WAS:+put back to }${WAS:-left as it was}; ${UNIT} $(service_state)"
  546      echo "hardcore=$(as_flag "$(setting "${HARDCORE_KEY}")")"
  547  }
  548  
  549  do_status() {
  550      local ON
  551      ON="$(as_flag "$(setting "${KEY}")")"
  552      echo "enabled=${ON}"
  553      if [ -e "${MARKER}" ]; then echo "marker=1"; else echo "marker=0"; fi
  554      echo "service=$(service_state)"
  555      echo "hardcore=$(as_flag "$(setting "${HARDCORE_KEY}")")"
  556      [ "${ON}" = "1" ]
  557  }
  558  
  559  # The count could not be read: nothing on stdout, the reason on stderr and in
  560  # the log, exit 2. A guard that cannot run has not passed -- and a number
  561  # that is not known is not printed as one.
  562  cannot_tell() {
  563      say "$*"
  564      echo "raofflineproxy-ctl: $*" >&2
  565      exit 2
  566  }
  567  
  568  do_pending() {
  569      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ] || [ ! -e "${QUEUE}" ]; then
  570          echo 0
  571          return 1
  572      fi
  573      # The same interpreter and sqlite3 module the service writes the store
  574      # with (the package depends on Python3 for the service itself), opened
  575      # read-only, with a second's patience for a write in flight. The image
  576      # also carries a sqlite3 binary, but not by this package's asking.
  577      local N
  578      N="$(python3 -c '
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 582-668 (excerpt of 2455)

```text
  582  ' "${QUEUE}" 2>/dev/null)" || cannot_tell "the award queue at ${QUEUE} could not be read"
  583      case "${N}" in
  584          ''|*[!0-9]*) cannot_tell "the award queue answered '${N}', not a count" ;;
  585      esac
  586      echo "${N}"
  587      [ "${N}" -gt 0 ]
  588  }
  589  
  590  # The pending awards by id, oldest first, each with the second it was earned
  591  # (the store keeps milliseconds). Read the way pending reads: read-only, the
  592  # service's own sqlite3 module, a second's patience.
  593  do_pending_ids() {
  594      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ] || [ ! -e "${QUEUE}" ]; then
  595          return 1
  596      fi
  597      # The signed-in account's awards, and those that name no account: the
  598      # page marks these as this player's, so another account's award on this
  599      # device is not among them (#308 gpt F-RA-09). No account set: all, as
  600      # before.
  601      local ROWS
  602      ROWS="$(python3 -c '
  603  import sqlite3, sys
  604  from urllib.parse import parse_qs
  605  user = sys.argv[2].strip().lower()
  606  def owner(query, body):
  607      for text in ((query or "").split("?", 1)[-1], body or ""):
  608          values = parse_qs(text, keep_blank_values=True).get("u")
  609          if values and values[0].strip():
  610              return values[0].strip().lower()
  611      return ""
  612  db = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True, timeout=1.0)
  613  for aid, queued, query, body in db.execute("SELECT achievementId, queuedAt, queryString, requestBody FROM pending_awards WHERE status = ? ORDER BY queuedAt ASC, id ASC", ("pending",)):
  614      if not user or owner(query, body) in ("", user):
  615          print(int(aid), int(queued) // 1000)
  616  ' "${QUEUE}" "$(setting "${USER_KEY}")" 2>/dev/null)" || cannot_tell "the award queue at ${QUEUE} could not be read"
  617      [ -n "${ROWS}" ] || return 1
  618      printf '%s\n' "${ROWS}"
  619      return 0
  620  }
  621  
  622  # summary: the page's whole offline summary in one read of the store (fork
  623  # #190: 247 saved games were 494 requests to the service, each tried
  624  # upstream first while the service still believed it was online -- hours on
  625  # a link that had just gone). One JSON object a line, sorted by id:
  626  #   {"id":4902,"title":"Bobl","icon":"http://127.0.0.1:8080/Images/x.png",
  627  #    "achievements":12,"points":110,"unlocked":1,"unlockedPoints":5,"pending":1}
  628  # A game is the account's patch row, or -- for a game a launch cached and
  629  # nothing else did -- its achievementsets row (RetroArch asks achievementsets,
  630  # not patch; #307 PL-057), read as the interface's game page reads one: the
  631  # set of Type core, else the first. The core set (Flags 3, positive ids) as
  632  # the interface reads a patch; a game whose set is empty is not a cached game
  633  # (audit #186 PL-26); unlocked counts the store's unlocks and the casual
  634  # awards still waiting, as the service's own offline unlocks answer does --
  635  # and when the store's unlock row for the game is missing or cannot be read,
  636  # unlocked and unlockedPoints are null: unknown, never 0 (#307 PL-057). The
  637  # icon carries the service's address as the service would rewrite it. Exit
  638  # 1 with the toggle off, no account set or no store; the store that cannot
  639  # be read is a cannot_tell (exit 2).
  640  do_summary() {
  641      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ] || [ ! -e "${QUEUE}" ]; then
  642          return 1
  643      fi
  644      local USER
  645      USER=*** "${USER_KEY}")"
  646      [ -n "${USER}" ] || return 1
  647      python3 - "${QUEUE}" "${USER}" <<'PY_SUMMARY'
  648  import json, sqlite3, sys
  649  from urllib.parse import parse_qs, urlsplit
  650  store, user = sys.argv[1], sys.argv[2].strip().lower()
  651  base = "http://127.0.0.1:8080"
  652  def icon_url(text):
  653      text = (text or "").strip()
  654      if not text:
  655          return ""
  656      if text.startswith("/"):
  657          return base + text
  658      if "://" in text:
  659          path = urlsplit(text).path
  660          return base + path if path else ""
  661      return base + "/" + text
  662  def core_of(achievements):
  663      return [a for a in (achievements or []) if isinstance(a, dict) and int(a.get("Flags") or 3) == 3 and int(a.get("ID") or 0) > 0]
  664  def set_achievements(data):
  665      # OfflineAchievementsText::parseAchievementSets: the set of Type core, else the first.
  666      if isinstance(data.get("Achievements"), list):
  667          return data["Achievements"]
  668      chosen = None
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 746-1043 (excerpt of 2455)

```text
  746      local RC=$?
  747      [ "${RC}" -eq 0 ] || cannot_tell "the proxy's store at ${QUEUE} could not be read"
  748  }
  749  
  750  # The account's points from the proxy's cached sign-in (the login2 row of the
  751  # signed-in user, keyed by the user name in lower case as cache_keys.py
  752  # normalises it). The row carries the session token; the two numbers are
  753  # all that leaves this function.
  754  do_account() {
  755      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ] || [ ! -e "${QUEUE}" ]; then
  756          return 1
  757      fi
  758      local USER LINE
  759      USER=*** "${USER_KEY}")"
  760      [ -n "${USER}" ] || return 1
  761      # Exit 1 is "no such row", said apart from a store that cannot be read
  762      # (exit 3): an account nobody signed in is not the same as a store the
  763      # page should not trust, and only the second is a cannot_tell.
  764      LINE="$(python3 -c '
  765  import json, sqlite3, sys
  766  try:
  767      db = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True, timeout=1.0)
  768      row = db.execute("SELECT responseBody FROM api_cache WHERE cacheKey = ?", ("login2::" + sys.argv[2].strip().lower(),)).fetchone()
  769  except Exception:
  770      sys.exit(3)
  771  if row is None:
  772      sys.exit(1)
  773  try:
  774      body = json.loads(row[0])
  775  except Exception:
  776      sys.exit(3)
  777  # The row the proxy writes from a token (auth.cache_token_credentials) has no
  778  # Score: nothing is cached about the points, and an absent number is never
  779  # printed as 0.
  780  if not isinstance(body, dict) or body.get("Score") is None or body.get("SoftcoreScore") is None:
  781      sys.exit(1)
  782  try:
  783      score = int(body["Score"])
  784      softcore = int(body["SoftcoreScore"])
  785  except Exception:
  786      sys.exit(3)
  787  print("score=%d softcore=%d" % (score, softcore))
  788  ' "${QUEUE}" "${USER}" 2>/dev/null)"
  789      local RC=$?
  790      if [ "${RC}" -eq 1 ]; then
  791          return 1
  792      elif [ "${RC}" -ne 0 ]; then
  793          cannot_tell "the proxy's store at ${QUEUE} could not be read"
  794      fi
  795      case "${LINE}" in
  796          score=*\ softcore=*) ;;
  797          *) cannot_tell "the proxy's store answered '${LINE}', not the account's points" ;;
  798      esac
  799      echo "${LINE}"
  800      return 0
  801  }
  802  
  803  do_flushed() {
  804      [ -e "${FLUSH_STAMP}" ] || return 1
  805      # Taken before it is read: the rename is one step, so a stamp the
  806      # service replaces after this moment is a new file this call never
  807      # touches (it is the next caller's), and of two callers only the one
  808      # whose rename succeeded has anything to report. Whatever was taken is
  809      # removed before it is judged, so a stamp that says nothing went, or
  810      # nothing readable, is gone too and never read twice.
  811      local MINE="${FLUSH_STAMP}.$$" LINE
  812      mv -f "${FLUSH_STAMP}" "${MINE}" 2>/dev/null || return 1
  813      LINE="$(head -n 1 "${MINE}" 2>/dev/null)"
  814      rm -f "${MINE}"
  815      if [[ "${LINE}" =~ ^[0-9]+\ [1-9][0-9]*$ ]]; then
  816          echo "${LINE}"
  817          return 0
  818      fi
  819      return 1
  820  }
  821  
  822  # ---- the scan -------------------------------------------------------------
  823  
  824  # The progress file (fork #189): whole or not at all (temp + rename), so a
  825  # reader never sees half a line; RUN_ROUTE is set by the route before its
  826  # first mark. $1 is the rest of the line (" index=<i> total=<n> name=<g>").
  827  mark_running() {
  828      printf 'route=%s at=%s%s\n' "${RUN_ROUTE:-run}" "$(date +%s)" "${1:-}" > "${RUNNING}.tmp" 2>/dev/null \
  829          && mv -f "${RUNNING}.tmp" "${RUNNING}" 2>/dev/null
  830  }
  831  unmark_running() { rm -f "${RUNNING}" "${RUNNING}.tmp"; }
  832  
  833  # A line for the page: ">>> <word> <fields>". Everything else on stdout is
  834  # the client's own output, which the page shows nothing of.
  835  tell() {
  836      printf '>>> %s\n' "$*"
  837  }
  838  
  839  # The scan's own log, rotated once past a megabyte. The client's lines are
  840  # file names and reasons; nothing from system.cfg is ever written here.
  841  slog() {
  842      mkdir -p "${PROXY_DIR}" 2>/dev/null
  843      if [ -e "${SCAN_LOG}" ] && [ "$(stat -c %s "${SCAN_LOG}" 2>/dev/null || echo 0)" -gt 1048576 ]; then
  844          mv -f "${SCAN_LOG}" "${SCAN_LOG}.1"
  845      fi
  846      printf '%s %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" "$*" >> "${SCAN_LOG}"
  847  }
  848  
  849  # How many games are cached, from the client's export. One id per line, so
  850  # the count is the line count; absent means none yet. Falls back to asking
  851  # the client when the export is missing but a store exists, and to 0 when
  852  # even that cannot be read -- a number that is not known is never invented.
  853  # RetroArch's play history (fork #299): the link's return looks for games
  854  # played since the last attempt and nothing else, so a wake with no game
  855  # played costs nothing and shows nothing. RetroArch 1.22 with
  856  # content_history_directory = "default" writes it under playlist_directory
  857  # as builtin/content_history.lpl, beside the video, music and image
  858  # histories -- not at content_history_path, which the config still names
  859  # and which the RG35XX SP never had (fork #306: the check read "no game
  860  # played" at every link for a day). Both are read from retroarch.cfg (~ is
  861  # /storage) and the newest file wins; a missing file loses to one that
  862  # exists. PPSSPP's ppsspp.ini is read beside them: it is the toggle's other
  863  # emulator (D-RA-002), the recently played pass reads its [Recent] list as
  864  # well as RetroArch's history (the client's load_content_history_paths), and
  865  # the file is written at every PPSSPP launch (cheevos_ppsspp.sh) and exit, so
  866  # a game played in PPSSPP alone is a game played (#308 F-RA-13).
  867  # RAOFFLINEPROXY_HISTORY overrides them all (the scripts suite's fixture).
  868  PPSSPP_INI=/storage/.config/ppsspp/PSP/SYSTEM/ppsspp.ini
  869  history_path() {
  870      local CFG=/storage/.config/retroarch/retroarch.cfg P D BUILTIN NEWEST=""
  871      if [ -n "${RAOFFLINEPROXY_HISTORY:-}" ]; then
  872          printf '%s\n' "${RAOFFLINEPROXY_HISTORY}"
  873          return 0
  874      fi
  875      P="$(sed -n 's/^content_history_path = "\(.*\)"$/\1/p' "${CFG}" 2>/dev/null | head -n 1)"
  876      case "${P}" in "~/"*) P="/storage/${P#\~/}" ;; esac
  877      P="${P:-/storage/.config/retroarch/content_history.lpl}"
  878      D="$(sed -n 's/^playlist_directory = "\(.*\)"$/\1/p' "${CFG}" 2>/dev/null | head -n 1)"
  879      case "${D}" in "~/"*) D="/storage/${D#\~/}" ;; esac
  880      BUILTIN="${D:-/storage/playlists}/builtin/content_history.lpl"
  881      for F in "${BUILTIN}" "${P}" "${PPSSPP_INI}"; do
  882          [ -e "${F}" ] || continue
  883          if [ -z "${NEWEST}" ] || [ "${F}" -nt "${NEWEST}" ]; then NEWEST="${F}"; fi
  884      done
  885      printf '%s\n' "${NEWEST:-${BUILTIN}}"
  886  }
  887  
  888  count_ready() {
  889      local N=""
  890      if [ -s "${READY_FILE}" ]; then
  891          N="$(grep -c -E '^[0-9]+$' "${READY_FILE}" 2>/dev/null)"
  892      elif [ -e "${QUEUE}" ]; then
  893          N="$(${PROXY_PY} cached-games-count 2>/dev/null | tail -n 1)"
  894      fi
  895      case "${N}" in ''|*[!0-9]*) N=0 ;; esac
  896      echo "${N}"
  897  }
  898  
  899  do_ready() {
  900      count_ready
  901  }
  902  
  903  # listening [--wait N] (#308 F-RA-26): the unit was Type=simple, so
  904  # `systemctl start` -- and with it enable, which routes the emulators to
  905  # the proxy once it returns, and the Before= that holds the interface --
  906  # returned the moment Python began importing, seconds before the port was
  907  # bound on a handheld; a launch in that window met a refused connection,
  908  # which makes rcheevos give up achievements for the session. The unit's
  909  # ExecStartPost runs this, bounded, so "started" means "listening". The
  910  # socket table is read, not a tool's output (netstat is not a dependency
  911  # of anything here); 127.0.0.1, 0.0.0.0 and ::ffff:127.0.0.1 on port 8080
  912  # (1F90) in state LISTEN (0A) count -- the listeners that take the IPv4
  913  # connection to 127.0.0.1:8080 the emulators are given. ::1 does not take
  914  # it, and :: may be IPv6-only, which the table does not say, so neither
  915  # counts (audit of the fixes, gpt G-D-02). Leaving :: out turns the proxy
  916  # away never: its sockets are IPv4 -- proxy_service.py's ThreadingTCPServer
  917  # keeps socketserver.TCPServer's AF_INET (patched client, line 267), boot.py
  918  # makes and adopts AF_INET sockets (lines 32 and 58), and nothing here sets
  919  # proxy_host, whose default is 127.0.0.1 (config.py:367) -- and the scripts
  920  # suite runs the pinned client's run-service in a network namespace of its
  921  # own and holds this check to its socket, so a pin that moves to `::` fails
  922  # there first (audit of the fix round, claude G2-D-01, the blind pass's
  923  # S-26, PL-033). RAOFFLINEPROXY_PROC_NET stands in for /proc/net (the
  924  # scripts suite's fixture).
  925  port_listening() {
  926      local F SL LOCAL REM ST REST
  927      for F in "${RAOFFLINEPROXY_PROC_NET:-/proc/net}/tcp" "${RAOFFLINEPROXY_PROC_NET:-/proc/net}/tcp6"; do
  928          [ -r "${F}" ] || continue
  929          while read -r SL LOCAL REM ST REST; do
  930              [ "${ST}" = "0A" ] || continue
  931              case "${LOCAL}" in
  932                  0100007F:1F90|00000000:1F90|0000000000000000FFFF00000100007F:1F90) return 0 ;;
  933              esac
  934          done < "${F}"
  935      done
  936      return 1
  937  }
  938  
  939  do_listening() {
  940      local TRIES=1 T=0
  941      if [ -n "${1:-}" ]; then
  942          if [ "${1}" != "--wait" ] || [ -z "${2:-}" ] || [ -n "${2//[0-9]/}" ]; then
  943              echo "usage: raofflineproxy-ctl listening [--wait <seconds>]" >&2
  944              exit ${EX_USAGE}
  945          fi
  946          TRIES="${2}"
  947      fi
  948      while :; do
  949          T=$((T + 1))
  950          port_listening && return 0
  951          [ "${T}" -lt "${TRIES}" ] || break
  952          sleep 1
  953      done
  954      say "listening: nothing is listening on 127.0.0.1:8080 after ${T} look(s)"
  955      return 1
  956  }
  957  
  958  # The games ready for the signed-in account, one id a line into $1: those
  959  # with the account's unlocks row and an achievementsets row of the game --
  960  # the rows a launch reads (RetroArch asks achievementsets, not patch), so a
  961  # game a launch cached is ready before any patch row exists. The walk's
  962  # "already cached" (list_jobs whole_games) is the same rule (audit of the
  963  # fixes, claude G-D-08, gpt G-D-04). A sets row's GameId is read from the
  964  # first 512 characters, where the service writes it, and from the whole body
  965  # only when they do not hold it, so the store's bodies are not parsed whole
  966  # at every run. The head answers only with the body's own key -- not a
  967  # nested set's (Sets[].GameId) -- and a number that ends inside it -- not
  968  # one the cut ends in ("GameId":15 of 153); anything less is the whole
  969  # body's parse, so the two ways of reading a row cannot disagree (audit of
  970  # the fix round, gpt G2-D-01, claude G2-D-08). head_game_id is the same text
  971  # in list_jobs' whole_games. added= is how many ids a run adds to this set
  972  # -- the games that became ready for this player (fork #298's "games new to
  973  # the store"), counted from the store rather than from the run's cache
  974  # operations (#308 F-RA-10, F-RA-15). Exit non-zero when the store cannot
  975  # be read.
  976  ready_games_into() {
  977      : > "$1" || return 1
  978      [ -e "${QUEUE}" ] || return 0
  979      python3 -c '
  980  import json, re, sqlite3, sys
  981  store, user = sys.argv[1], sys.argv[2].strip().lower()
  982  db = sqlite3.connect("file:%s?mode=ro" % store, uri=True, timeout=1.0)
  983  HEAD_VALUE = re.compile(r"\s*:\s*(\d+)\s*[,}]")
  984  HEAD_COLON = re.compile(r"\s*:")
  985  def head_game_id(head):
  986      depth, i, n = 0, 0, len(head)
  987      while i < n:
  988          c = head[i]
  989          if c == "\"":
  990              j = i + 1
  991              while j < n and head[j] != "\"":
  992                  j += 2 if head[j] == "\\" else 1
  993              if j >= n:
  994                  return None
  995              if depth == 1 and head[i + 1:j] == "GameId":
  996                  whole = HEAD_VALUE.match(head, j + 1)
  997                  if whole:
  998                      return int(whole.group(1))
  999                  if HEAD_COLON.match(head, j + 1):
 1000                      return None
 1001              i = j + 1
 1002              continue
 1003          if c in "{[":
 1004              depth += 1
 1005          elif c in "}]":
 1006              depth -= 1
 1007          i += 1
 1008      return None
 1009  unlocks, sets = set(), set()
 1010  for key, head in db.execute("SELECT cacheKey, substr(responseBody, 1, 512) FROM api_cache WHERE cacheKey LIKE ? OR cacheKey LIKE ?", ("unlocks:%", "achievementsets:%")).fetchall():
 1011      parts = key.split(":")
 1012      if parts[0] == "unlocks":
 1013          if len(parts) == 4 and parts[2] == user and parts[3] == "0" and parts[1].isdigit():
 1014              unlocks.add(int(parts[1]))
 1015          continue
 1016      if len(parts) != 3 or parts[2] != user:***
 1017          continue
 1018      gid = head_game_id(head or "")
 1019      if gid is None:
 1020          try:
 1021              body = db.execute("SELECT responseBody FROM api_cache WHERE cacheKey = ?", (key,)).fetchone()[0]
 1022              gid = int((json.loads(body) or {}).get("GameId") or 0)
 1023          except Exception:
 1024              gid = 0
 1025      if gid > 0:
 1026          sets.add(gid)
 1027  for g in sorted(unlocks & sets):
 1028      print(g)
 1029  ' "${QUEUE}" "$(setting "${USER_KEY}")" > "$1" 2>/dev/null
 1030  }
 1031  
 1032  # How many games a run made ready: the ids in the after file ($2) that the
 1033  # before file ($1) does not hold. Prints nothing and fails when either could
 1034  # not be read; the caller says so through added_count, and never puts a
 1035  # count of its own in this one's place.
 1036  games_made_ready() {
 1037      [ -n "${1}" ] && [ -n "${2}" ] && [ -e "${1}" ] && [ -e "${2}" ] || return 1
 1038      local NEWIDS RC N=0
 1039      # grep says 0 when it selected lines, 1 when none, 2 when it could not
 1040      # read: only the first two are an answer. A count taken after the pipe
 1041      # read a failed comparison as 0 new games (audit of the fixes, gpt
 1042      # G-D-05).
 1043      NEWIDS="$(grep -vxF -f "$1" "$2" 2>/dev/null)"
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 1052-1308 (excerpt of 2455)

```text
 1052  # nothing made nothing ready; otherwise the word unknown. Never the run's
 1053  # cache operations: they count a second dump of a game already ready, and
 1054  # the top-up card says MORE GAMES ARE READY from this number (audit of the
 1055  # fix round, gpt G2-D-02, the blind pass's S-24, PL-031). The interface's
 1056  # reader (CloudText::parseScanStamp) passes over a value that is not a
 1057  # number, as for a stamp that does not say.
 1058  added_count() { # <measured count, or empty> <cached>
 1059      if [ -n "${1}" ]; then
 1060          echo "${1}"
 1061      elif [ "${2:-0}" -gt 0 ] 2>/dev/null; then
 1062          echo unknown
 1063      else
 1064          echo 0
 1065      fi
 1066  }
 1067  
 1068  # "<epoch> <rc> <route> cached=<n> skipped=<m> ready=<total> limit=<0|1>
 1069  # indexed=<i> errors=<e> added=<k> [why=<TOKEN>] [note=<TOKEN>]", written whole or not at all (a
 1070  # rename), so the page never reads half a line. The page reads the keys it
 1071  # knows and passes over the rest (CloudText::parseScanStamp), so indexed=
 1072  # and errors= are for the log and for whoever reads the file.
 1073  write_stamp() {
 1074      local RC="$1" ROUTE="$2" CACHED="$3" SKIPPED="$4" READY="$5" LIMIT="$6" INDEXED="${7:-0}" ERRORS="${8:-0}" WHY="${9:-}"
 1075      # added (fork #298): the games this run made ready for the account, as
 1076      # measured -- the tenth argument; a run that gives none, or whose
 1077      # measurement failed, is said by added_count, never counted as every
 1078      # game it cached (PL-031).
 1079      local ADDED
 1080      ADDED="$(added_count "${10:-}" "${CACHED}")"
 1081      # truncated=1 (#307 PL-059): the walk over unindexed folders stopped at
 1082      # the cap, and the games past it are the next scan's. Written only when
 1083      # it is 1; CloudText::parseScanStamp reads it.
 1084      local TRUNCATED="${11:-0}"
 1085      # note=NO_GAMES (fork #329): the run completed with nothing to look at;
 1086      # the twelfth argument, written only when given. The page reads it
 1087      # (CloudText::parseScanStamp) for the line under the row.
 1088      local NOTE="${12:-}"
 1089      local LINE="$(date +%s) ${RC} ${ROUTE} cached=${CACHED} skipped=${SKIPPED} ready=${READY} limit=${LIMIT} indexed=${INDEXED} errors=${ERRORS} added=${ADDED}"
 1090      [ "${TRUNCATED}" = "1" ] && LINE="${LINE} truncated=1"
 1091      [ -n "${WHY}" ] && LINE="${LINE} why=${WHY}"
 1092      [ -n "${NOTE}" ] && LINE="${LINE} note=${NOTE}"
 1093      mkdir -p "${PROXY_DIR}" || return 1
 1094      printf '%s\n' "${LINE}" > "${SCAN_STAMP}.tmp" && mv -f "${SCAN_STAMP}.tmp" "${SCAN_STAMP}"
 1095  }
 1096  
 1097  # The walk's proposed cursor (scan-cursor.next, from list_jobs) becomes the
 1098  # cursor: a path to walk on from, or none when the walk came round. Kept
 1099  # only after a run that worked through its jobs (audit of the fixes, claude
 1100  # G-D-06), and read back once written, since the continuation the page
 1101  # promises rests on it (gpt G-D-06). Exit 1 when it could not be kept.
 1102  commit_cursor() {
 1103      local WANT
 1104      [ -f "${SCAN_CURSOR}.next" ] || return 1
 1105      WANT="$(cat "${SCAN_CURSOR}.next" 2>/dev/null)" || return 1
 1106      if [ -z "${WANT}" ]; then
 1107          rm -f "${SCAN_CURSOR}.next"
 1108          rm -f "${SCAN_CURSOR}" 2>/dev/null
 1109          [ ! -e "${SCAN_CURSOR}" ]
 1110          return
 1111      fi
 1112      [ ! -d "${SCAN_CURSOR}" ] && mv -f "${SCAN_CURSOR}.next" "${SCAN_CURSOR}" 2>/dev/null \
 1113          && [ "$(cat "${SCAN_CURSOR}" 2>/dev/null)" = "${WANT}" ]
 1114  }
 1115  
 1116  # The account EmulationStation signed in with: a user name and either the
 1117  # token it wrote after the sign-in or the password it will sign in with.
 1118  # Presence only; the values stay in system.cfg.
 1119  have_account() {
 1120      [ -n "$(setting "${USER_KEY}")" ] || return 1
 1121      [ -n "$(setting "${TOKEN_KEY}")" ] || [ -n "$(setting "${PASSWORD_KEY}")" ]
 1122  }
 1123  
 1124  # The proxy's own answer to "is RetroAchievements reachable": probe-online
 1125  # sends one HEAD to retroachievements.org (a fresh process asks every time;
 1126  # its thirty-second memory is per process) and writes the answer to
 1127  # online_state.json in its config folder, printing nothing. It is pointed
 1128  # at a folder of its own for the call: the service's online_state.json is
 1129  # the service's (its monitor writes it at start and on a change, and the
 1130  # interface reads it as the proxy's own view, D-RA-011), and a probe from
 1131  # here that lands in a resolver lag would otherwise write "false" over it
 1132  # with nothing to correct it until the service's next transition (#186
 1133  # PL-03). Anything but a readable "online": true reads as offline -- a
 1134  # check that cannot run has not passed.
 1135  is_online() {
 1136      local SCRATCH ANSWER=1
 1137      SCRATCH="$(mktemp -d /tmp/raofflineproxy-probe.XXXXXX)" || return 1
 1138      if RAOFFLINEPROXY_CONFIG_DIR="${SCRATCH}" ${PROXY_PY} probe-online >/dev/null 2>&1; then
 1139          grep -q -E '"online": *true' "${SCRATCH}/online_state.json" 2>/dev/null && ANSWER=0
 1140      fi
 1141      rm -rf "${SCRATCH}"
 1142      return ${ANSWER}
 1143  }
 1144  
 1145  # Seconds left of a run's deadline, from its START; never negative.
 1146  time_left() {
 1147      local L=$(( TOPUP_TIMEOUT - ($(date +%s) - ${1}) ))
 1148      [ "${L}" -gt 0 ] || L=0
 1149      echo "${L}"
 1150  }
 1151  
 1152  # A sleep that a SIGTERM interrupts: the shell waits on a background sleep,
 1153  # and wait returns the moment a trapped signal arrives, so disable is not
 1154  # kept waiting for a probe interval to run out.
 1155  pause() {
 1156      sleep "${1}" &
 1157      wait $! 2>/dev/null
 1158  }
 1159  
 1160  # What both verbs refuse before they touch anything, in the order a player
 1161  # would fix them: the toggle, then the account. Exit codes only; the page
 1162  # says them.
 1163  refuse_unless_ready() {
 1164      local VERB="$1"
 1165      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ]; then
 1166          say "${VERB}: refused, offline RetroAchievements is off"
 1167          tell "why TOGGLE_OFF"
 1168          exit ${EX_CONFIG}
 1169      fi
 1170      if ! have_account; then
 1171          say "${VERB}: refused, no RetroAchievements account is signed in"
 1172          tell "why NO_ACCOUNT"
 1173          exit ${EX_NOPERM}
 1174      fi
 1175  }
 1176  
 1177  # One scan or top-up at a time (the lock is held for the rest of the run;
 1178  # the fd closes with the process). Exit 75 when another holds it -- except
 1179  # for the top-up that follows the interface's index (topup --after-index),
 1180  # which waits its turn for what is left of its deadline ($3, the run's
 1181  # START; the wait spends from the same fifteen minutes as the rest, #186
 1182  # PL-28): it is the one run that knows the index has just grown, and the
 1183  # top-up ahead of it read the index before that. Busybox flock has no -w,
 1184  # so the wait is a loop. The file is opened without truncating it, and the
 1185  # holder writes its pid on the first line once it has the lock, which is
 1186  # how disable finds a run to stop (#186 PL-30) -- a run that finds the lock
 1187  # taken has not wiped the holder's pid by opening the file.
 1188  take_lock() {
 1189      local VERB="$1" WAIT="${2:-0}" START="${3:-0}"
 1190      exec 9<>"${SCAN_LOCK}" || fail "cannot open ${SCAN_LOCK}"
 1191      until flock -n 9; do
 1192          if [ "${WAIT}" -eq 0 ] || [ "$(time_left "${START}")" -le 10 ]; then
 1193              say "${VERB}: another scan or top-up is running"
 1194              exit ${EX_TEMPFAIL}
 1195          fi
 1196          pause 10
 1197      done
 1198      printf '%s\n' "$$" >&9
 1199      # The lock is held, so no run is live: a progress file still here was a
 1200      # run that died without its EXIT trap (a kill -9, a power cut), and the
 1201      # interface has been ignoring it since its 900 s bound. Removed here, at
 1202      # the one point every verb passes (#189 box 3's "and removed"; the
 1203      # seat's G-08 under audit #258).
 1204      rm -f "${RUNNING}" "${RUNNING}.tmp"
 1205  }
 1206  
 1207  # The games to cache, one job per line into $1, in the client's own terms
 1208  # where it has any, and in the interface's where it has the better ones
 1209  # (D-RA-013):
 1210  #
 1211  #   I<TAB><gameId><TAB><hash><TAB><path>   from the interface's index
 1212  #   H<TAB><TAB><TAB><path>                 to be hashed and looked up
 1213  #
 1214  # The interface's index is what the hasher wrote (INDEX NEW GAMES AT
 1215  # STARTUP, INDEX GAMES): per system, the games' <cheevosHash> and
 1216  # <cheevosId> in gamelist.xml -- beside the ROMs, else under the interface's
 1217  # gamelists/<system>/ -- overlaid with the per-game files under its
 1218  # recovery/<system>/, which is where a change lives until the interface
 1219  # writes the gamelist at its next clean exit (a recovery file whose
 1220  # parentHash is not the current gamelist's size is stale, and skipped as
 1221  # the interface skips it). A system has an index when any
 1222  # of its games carries a cheevosHash: the hasher writes the hash for every
 1223  # game it looked at and the id only for the ones RetroAchievements knows, so
 1224  # a system whose games all came back without a set is indexed too, and
 1225  # nothing in it is hashed again. In an indexed system the jobs are the games
 1226  # with a cheevosId whose file is still there and whose id the client has not
 1227  # cached (its own export of cached ids, the count `ready` reads); the rest
 1228  # of the system -- games with no set, and games added since the index ran --
 1229  # is left to the index. A system with no index at all keeps today's walk
 1230  # (mode all): every ROM under its folder, in the client's own terms -- its
 1231  # extension list decides what is a ROM (is_supported_browser_file, archives
 1232  # included), its cached-path record what is already done, its history reader
 1233  # what was played (most recent first, then newest file first) -- less hidden
 1234  # files and folders, the scraper's folders, empty files, and a .bin beside a
 1235  # .cue, .gdi or .m3u. Mode indexed writes the I jobs alone: the top-up on
 1236  # connect never hashes a library nobody asked it to.
 1237  #
 1238  # "Already cached" is asked of the signed-in account's rows and this hash's
 1239  # (#186 PL-23): the proxy serves a launch from patch:<id>:<user>,
 1240  # unlocks:<id>:<user>:0 and achievementsets:<hash>:<user>, so a game is
 1241  # cached when all three are there for this account and this dump, and a
 1242  # job again when any is missing -- a fetch that failed after the first row
 1243  # was written, a set the client's eviction took at sixty days (#186 PL-02),
 1244  # a second account on the device, a second dump of a game. The account
 1245  # name reaches the listing through the environment (RA_SCAN_USER), never a
 1246  # command line. The walk's "already done" stays the client's own record
 1247  # (the ROM's path on this account's patch rows).
 1248  #
 1249  # The systems and their folders come from the interface's own files, read
 1250  # as it reads them: the base es_systems.cfg (custom, user or image copy) and
 1251  # the es_systems_*.cfg merged into it (#308 F-RA-06); the walk's
 1252  # folders from SCAN_SYSTEMS as before, less any folder an indexed system
 1253  # owns. The walk stops at the client's cap of files (MAX_SCAN_ENTRIES),
 1254  # counted over the files not yet cached and begun from the cursor the last
 1255  # cut walk left (scan-cursor, $6), so the cap bounds one run's work and never
 1256  # the library: a second run walks past what the first cached (#186 PL-17)
 1257  # and past what the first could not cache (#307 PL-059). $3 bounds the
 1258  # listing in seconds (0: no bound). Prints
 1259  # "found=<seen> new=<jobs> cached=<seen-jobs> indexed=<I> hashing=<H>
 1260  # truncated=<0|1>" on stdout.
 1261  list_jobs() {
 1262      local BUDGET="${3:-0}"
 1263      local -a BOUND=()
 1264      [ "${BUDGET}" -gt 0 ] && BOUND=(timeout "${BUDGET}")
 1265      RA_SCAN_USER=*** "${USER_KEY}")" "${BOUND[@]}" python3 - "$1" "${2:-all}" "${ROMS_ROOT}" "${ES_DIR}" "${SCAN_SYSTEMS}" "${SCAN_CURSOR}" <<'PY'
 1266  import json, os, re, sqlite3, sys
 1267  import xml.etree.ElementTree as ET
 1268  from pathlib import Path
 1269  from raofflineproxy import cache_keys
 1270  from raofflineproxy.config import DATABASE_FILE, load_config
 1271  from raofflineproxy.rom_browser import (
 1272      MAX_SCAN_ENTRIES, is_supported_browser_file, normalize_cached_rom_path,
 1273  )
 1274  from raofflineproxy.smart_cache import load_content_history_paths
 1275  from raofflineproxy.storage import Storage
 1276  
 1277  out, mode, roms_root, es_dir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
 1278  walk_systems = sys.argv[5].split()
 1279  cursor_file = Path(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] else None
 1280  user = cache_keys.normalize_user(os.environ.get("RA_SCAN_USER", ""))
 1281  SKIP_DIRS = {
 1282      "images", "videos", "manuals", "media", "downloaded_images", "downloaded_videos",
 1283      "downloaded_manuals", "imgs", "savestates", "screenshots", "saves", "savefiles",
 1284  }
 1285  DISC_SHEETS = (".cue", ".gdi", ".m3u")
 1286  
 1287  
 1288  def es_systems():
 1289      """(name, folder) per <system>, read as the interface reads them (#308
 1290      F-RA-06): SystemData::getConfigPath takes the first of the user's
 1291      es_systems_custom.cfg, the user's es_systems.cfg, the one beside the
 1292      binary and the image's as the base -- a custom file is the whole base
 1293      there too -- and loadAdditionnalConfig then merges every es_systems_*.cfg
 1294      in the user's folder and beside the binary into it by name: a known
 1295      system's tags replaced (a tag with no text dropped, <emulators> kept), a
 1296      new one appended, and a file that does not parse ends the merging, as it
 1297      does there."""
 1298      root = None
 1299      for cfg in (es_dir / "es_systems_custom.cfg", es_dir / "es_systems.cfg",
 1300                  Path("/usr/bin/es_systems.cfg"), Path("/etc/emulationstation/es_systems.cfg"),
 1301                  Path("/usr/config/emulationstation/es_systems.cfg")):
 1302          if not cfg.is_file():
 1303              continue
 1304          try:
 1305              root = ET.parse(cfg).getroot()
 1306          except Exception:
 1307              continue
 1308          break
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 1402-1448 (excerpt of 2455)

```text
 1402              size = gamelist.stat().st_size
 1403          except OSError:
 1404              size = 0
 1405          take(gamelist)
 1406      recovery = es_dir / "recovery" / name
 1407      if recovery.is_dir():
 1408          for dirpath, dirnames, filenames in os.walk(recovery):
 1409              dirnames.sort()
 1410              for fn in sorted(filenames):
 1411                  if fn.lower().endswith(".xml"):
 1412                      take(Path(dirpath) / fn, parent=size)
 1413      return entries
 1414  
 1415  
 1416  config = load_config()
 1417  storage = Storage()
 1418  
 1419  
 1420  def is_cached(game_id, hash_value):
 1421      """Everything a launch reads, for this account and this dump."""
 1422      return (
 1423          storage.get_cache(cache_keys.patch(game_id, user)) is not None
 1424          and storage.get_cache(cache_keys.unlocks(game_id, user)) is not None
 1425          and storage.get_cache(cache_keys.achievementsets(hash_value, user)) is not None
 1426      )
 1427  
 1428  
 1429  # The ROMs this account's patch rows name (rom_browser.load_cached_rom_paths,
 1430  # narrowed to the account), in the client's own two-component form -- where
 1431  # the game is ready for this account (whole_games: its unlocks row and an
 1432  # achievementsets row of the game), as is_cached asks of an indexed game. A patch row alone (a fetch that failed after the first write, or
 1433  # rows an older client's eviction thinned) used to pass the ROM over for
 1434  # ever; now it is a job again (#308 F-RA-14). The dump's own sets row cannot
 1435  # be asked here -- an unindexed ROM's hash is what the job finds out.
 1436  HEAD_VALUE = re.compile(r"\s*:\s*(\d+)\s*[,}]")
 1437  HEAD_COLON = re.compile(r"\s*:")
 1438  def head_game_id(head):
 1439      depth, i, n = 0, 0, len(head)
 1440      while i < n:
 1441          c = head[i]
 1442          if c == "\"":
 1443              j = i + 1
 1444              while j < n and head[j] != "\"":
 1445                  j += 2 if head[j] == "\\" else 1
 1446              if j >= n:
 1447                  return None
 1448              if depth == 1 and head[i + 1:j] == "GameId":
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 1579-1600 (excerpt of 2455)

```text
 1579      (audit of the fixes, claude G-D-06). False when it could not be written
 1580      -- and the ctl says so rather than promising a continuation it cannot
 1581      keep (gpt G-D-06)."""
 1582      if cursor_file is None:
 1583          return True
 1584      proposal = cursor_file.with_name(cursor_file.name + ".next")
 1585      tmp = proposal.with_name(proposal.name + ".tmp")
 1586      try:
 1587          tmp.write_text(value + "\n" if value else "", encoding="utf-8", errors="surrogateescape")
 1588          os.replace(tmp, proposal)
 1589          return True
 1590      except OSError:
 1591          try:
 1592              tmp.unlink()
 1593          except OSError:
 1594              pass
 1595          return False
 1596  
 1597  
 1598  # The walk is a circle from a cursor (#307 PL-059). Cached files are passed
 1599  # over before the cap counts (#186 PL-17), but a file that never caches -- a
 1600  # ROM RetroAchievements does not know is skipped, and stays uncached --
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 1652-2128 (excerpt of 2455)

```text
 1652                  if take and normalize_cached_rom_path(path) in cached_paths:
 1653                      walked_cached += 1
 1654                      take = False
 1655                  if take:
 1656                      (after if passed else before).append(path)
 1657                  passed = passed or at_cursor
 1658                  if len(after) > MAX_SCAN_ENTRIES:
 1659                      full = True
 1660                      break
 1661              if full:
 1662                  break
 1663          if full:
 1664              break
 1665      candidates = after + before
 1666      walked = candidates[:MAX_SCAN_ENTRIES]
 1667      truncated = 1 if len(candidates) > MAX_SCAN_ENTRIES else 0
 1668      cursor_saved = 1 if propose_cursor(str(walked[-1]) if truncated and walked else "") else 0
 1669  
 1670  hash_jobs = walked
 1671  
 1672  lines = [f"I\t{indexed_jobs[p][0]}\t{indexed_jobs[p][1]}\t{p}\n" for p in by_history(list(indexed_jobs))]
 1673  lines += [f"H\t\t\t{p}\n" for p in by_history(hash_jobs)]
 1674  out.write_text("".join(lines), encoding="utf-8")
 1675  found = indexed_seen + len(walked) + walked_cached
 1676  new = len(lines)
 1677  print(f"found={found} new={new} cached={found - new} indexed={len(indexed_jobs)} hashing={len(hash_jobs)} truncated={truncated} cursor_saved={cursor_saved}")
 1678  PY
 1679  }
 1680  
 1681  # One field of list_jobs' summary line, or 0.
 1682  count_of() {
 1683      local V="${1#*${2}=}"
 1684      V="${V%% *}"
 1685      case "${V}" in ''|*[!0-9]*) echo 0 ;; *) echo "${V}" ;; esac
 1686  }
 1687  
 1688  # The helper that works the job list: beside this script, so a copy of the
 1689  # two files runs from anywhere they are put together.
 1690  case "$0" in
 1691      */*) HELPER="${0%/*}/raofflineproxy-cache-indexed"; IMAGE_HELPER="${0%/*}/raofflineproxy-cache-images"; REFRESH_HELPER="${0%/*}/raofflineproxy-refresh" ;;
 1692      *)   HELPER="/usr/bin/raofflineproxy-cache-indexed"; IMAGE_HELPER="/usr/bin/raofflineproxy-cache-images"; REFRESH_HELPER="/usr/bin/raofflineproxy-refresh" ;;
 1693  esac
 1694  
 1695  # Run the job list $2 of $3 games through the helper and read its lines as
 1696  # they come -- "OK i/n <file>", "FAIL i/n <file>: <reason>", "DONE cached=
 1697  # failed= indexed=" -- stopping it after three lookups in a row that
 1698  # RetroAchievements did not answer, or on a refused sign-in, or when the
 1699  # client reports its cap. $1 is page (the >>> lines for GuiOfflineScan) or
 1700  # quiet (nothing on stdout, for the top-up); $4 a bound in seconds, 0 for
 1701  # none. Leaves R_CACHED R_SKIPPED R_ERRORS R_LIMIT R_WHY R_STOPPED R_INDEXED
 1702  # R_CLIENT_RC for the caller, and the helper's stderr in the scan log. The
 1703  # helper's stdout goes through a fifo so it can be stopped between two lines.
 1704  run_jobs() {
 1705      local MODE="$1" LIST="$2" TOTAL="$3" BUDGET="${4:-0}"
 1706      local -a PATHS
 1707      mapfile -t PATHS < "${LIST}"
 1708      JOBS_FIFO="$(mktemp -u /tmp/raofflineproxy-scan-out.XXXXXX)"
 1709      mkfifo "${JOBS_FIFO}" || fail "cannot create ${JOBS_FIFO}"
 1710      if [ "${BUDGET}" -gt 0 ]; then
 1711          timeout "${BUDGET}" python3 "${HELPER}" "${LIST}" > "${JOBS_FIFO}" 2>>"${SCAN_LOG}" &
 1712      else
 1713          python3 "${HELPER}" "${LIST}" > "${JOBS_FIFO}" 2>>"${SCAN_LOG}" &
 1714      fi
 1715      CLIENT=$!
 1716      exec 8< "${JOBS_FIFO}"
 1717  
 1718      R_CACHED=0; R_SKIPPED=0; R_ERRORS=0; R_LIMIT=0; R_WHY=""; R_STOPPED=0; R_INDEXED=0; R_DONE=0
 1719      local IN_A_ROW=0 line index name
 1720      if [ "${TOTAL}" -gt 0 ]; then
 1721          name="${PATHS[0]##*/}"
 1722          mark_running " index=1 total=${TOTAL} name=${name//[[:space:]]/_}"
 1723          [ "${MODE}" = page ] && tell "game 1|${TOTAL}|${name%.*}"
 1724      fi
 1725      while IFS= read -r line <&8; do
 1726          slog "client: ${line}"
 1727          case "${line}" in
 1728              OK\ *)
 1729                  R_CACHED=$((R_CACHED + 1)); IN_A_ROW=0 ;;
 1730              DONE\ *)
 1731                  # The helper's verdict on the games: whatever the process does
 1732                  # afterwards (badge downloads outliving the bound, fork #188) is
 1733                  # not the run's outcome.
 1734                  R_INDEXED="$(count_of "${line}" indexed)"; R_DONE=1
 1735                  continue ;;
 1736              *"Cache limit reached"*)
 1737                  # The client says it will cache no more (no ROCKNIX client
 1738                  # does since patch 004; kept for one that says so): every
 1739                  # further ROM would be hashed and looked up only to be
 1740                  # refused.
 1741                  R_LIMIT=1; R_STOPPED=1
 1742                  slog "run: the client reports its cache limit; stopping"
 1743                  kill "${CLIENT}" 2>/dev/null
 1744                  break ;;
 1745              *"No RetroAchievements match"*|*"Hash failed"*|*": not found")
 1746                  # Not a game RetroAchievements knows, or not a file it can
 1747                  # read: the proxy's docs skip these silently, and so does
 1748                  # the page -- counted here for the log and the stamp.
 1749                  R_SKIPPED=$((R_SKIPPED + 1)); IN_A_ROW=0 ;;
 1750              *"login required"*|*"HTTP Error 401"*|*"HTTP Error 403"*)
 1751                  # The account, not the link: no retry changes it.
 1752                  R_WHY=SIGN_IN_REFUSED; R_STOPPED=1
 1753                  kill "${CLIENT}" 2>/dev/null
 1754                  break ;;
 1755              FAIL\ *)
 1756                  # A lookup or a fetch that did not come back: the link, the
 1757                  # server, a 429. A run of them is the scan asking a question
 1758                  # nobody is answering.
 1759                  R_ERRORS=$((R_ERRORS + 1)); IN_A_ROW=$((IN_A_ROW + 1))
 1760                  if [ "${IN_A_ROW}" -ge "${ERRORS_IN_A_ROW}" ]; then
 1761                      R_WHY=RETROACHIEVEMENTS_STOPPED_ANSWERING; R_STOPPED=1
 1762                      kill "${CLIENT}" 2>/dev/null
 1763                      break
 1764                  fi ;;
 1765              *)
 1766                  continue ;;
 1767          esac
 1768          # The helper finished game i (1-based); what it is on now is i+1.
 1769          index="${line#* }"; index="${index%%/*}"
 1770          case "${index}" in ''|*[!0-9]*) index=0 ;; esac
 1771          if [ "${index}" -gt 0 ] && [ "${index}" -lt "${TOTAL}" ]; then
 1772              name="${PATHS[${index}]##*/}"
 1773              mark_running " index=$((index + 1)) total=${TOTAL} name=${name//[[:space:]]/_}"
 1774          fi
 1775          [ "${MODE}" = page ] || continue
 1776          tell "cached ${R_CACHED}|${R_SKIPPED}"
 1777          if [ "${index}" -gt 0 ] && [ "${index}" -lt "${TOTAL}" ]; then
 1778              tell "game $((index + 1))|${TOTAL}|${name%.*}"
 1779          fi
 1780      done
 1781      exec 8<&-
 1782      wait "${CLIENT}" 2>/dev/null
 1783      R_CLIENT_RC=$?
 1784      unset CLIENT
 1785      rm -f "${JOBS_FIFO}"; JOBS_FIFO=""
 1786      unmark_running
 1787      if [ "${R_DONE}" -eq 1 ] && [ "${R_CLIENT_RC}" -ne 0 ]; then
 1788          slog "run: the helper had reported DONE and ended with rc ${R_CLIENT_RC} afterwards (badge downloads cut short) -- not the run's verdict (#188)"
 1789      fi
 1790  }
 1791  
 1792  # A run asked to stop (disable's SIGTERM, #186 PL-30) exits through its
 1793  # EXIT trap: the helper is ended, the run's files go, no stamp is written --
 1794  # the line under the row keeps the last run that finished.
 1795  stopped() {
 1796      say "${1}: stopped; offline RetroAchievements was turned off"
 1797      exit 143
 1798  }
 1799  
 1800  # A scan the player cancelled from its page (SIGINT from the interface,
 1801  # fork #241, D-UI-078). Not a failure: what the run saved stays saved, and
 1802  # the next scan passes over those games. So the stamp is written with the
 1803  # counts the run had reached -- the line under the row says SKIPPED and the
 1804  # ready count is right -- the page is told why, and the run exits 130
 1805  # through its EXIT trap (the helper ended, the run's files gone). R_CACHED
 1806  # and the rest are the run's so far; before run_jobs they are unset, and
 1807  # read as 0. added= is measured as the run's own end measures it -- the
 1808  # ready set the run took before its jobs against the store now -- and is
 1809  # unknown when either cannot be read, never the games cached so far
 1810  # (PL-031).
 1811  cancelled() {
 1812      local READY MADE=""
 1813      READY="$(count_ready)"
 1814      if [ -n "${READY_BEFORE:-}" ] && READY_AFTER="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && ready_games_into "${READY_AFTER}"; then
 1815          MADE="$(games_made_ready "${READY_BEFORE}" "${READY_AFTER}")"
 1816      fi
 1817      tell "why CANCELLED"
 1818      write_stamp 130 "${1}" "${R_CACHED:-0}" "${R_SKIPPED:-0}" "${READY}" 0 "${R_INDEXED:-0}" "${R_ERRORS:-0}" CANCELLED "${MADE}"
 1819      slog "${1} cancelled by the player: cached=${R_CACHED:-0} skipped=${R_SKIPPED:-0} errors=${R_ERRORS:-0} ready=${READY}"
 1820      say "${1}: cancelled"
 1821      exit 130
 1822  }
 1823  
 1824  # The images of what is cached, fetched until none is missing (#212). A
 1825  # game's achievements and its images are one action to a player -- the
 1826  # maintainer, 2026-09-18: "whenever we cache the achievements, we cache the
 1827  # images for the achievements" -- so this runs at the end of a scan and of a
 1828  # top-up that cached anything, and on its own as the `images` verb.
 1829  #
 1830  # The helper walks the store, not the library: every cached set row, every
 1831  # image path in it, and the ones with no file get fetched. Idempotent (the
 1832  # check is the file's existence and the client's own download no-ops on one)
 1833  # and resumable (nothing marks a game done but its files), so a run that
 1834  # stops at its ceiling costs the next one nothing. Bounded by what is left of
 1835  # the caller's deadline, or IMAGE_PASS_SECONDS on its own.
 1836  #
 1837  # Its verdict is part of the run's (#307 PL-060). A game whose badges are
 1838  # missing offline reads as half working (D-RA-027), and a run whose parts
 1839  # disagree is COULDN'T FINISH (D-UI-030), so a pass that left images behind
 1840  # -- the helper's `why` line, or an exit it gives no reason for -- leaves
 1841  # R_IMAGES_WHY=SOME_IMAGES_NOT_SAVED for the caller to stamp, the games
 1842  # still counted as cached. A verify slice that did not come round the store
 1843  # (the helper's exit 3) is the sweep doing its work a slice a run, by design
 1844  # (D-RA-024), and is no failure; every other exit is, a crash included. An
 1845  # image the image server does not have (404, 410) is recorded absent by the
 1846  # helper and is no failure either: SOME_IMAGES_NOT_SAVED means images that
 1847  # did not come this time -- a timeout, a 5xx, a short read -- and are asked
 1848  # for again (PL-060's follow-up).
 1849  IMAGE_PASS_SECONDS="${RAOFFLINEPROXY_IMAGE_PASS_SECONDS:-300}"
 1850  
 1851  run_image_pass() {
 1852      local VERB="$1" SECONDS_LEFT="${2:-${IMAGE_PASS_SECONDS}}" MODE="${3:-}" RC=0
 1853      R_IMAGES_WHY=""
 1854      [ -x "${IMAGE_HELPER}" ] || { slog "${VERB}: no image helper at ${IMAGE_HELPER}"; return 0; }
 1855      # No time left is no pass: the images were not looked at, and the run
 1856      # does not say it finished (audit of the fixes, gpt G-D-01).
 1857      [ "${SECONDS_LEFT}" -gt 10 ] 2>/dev/null || { slog "${VERB}: no time left for the image pass (${SECONDS_LEFT}s); not run"; R_IMAGES_WHY=TOOK_TOO_LONG; return 0; }
 1858      slog "${VERB}: image pass, up to ${SECONDS_LEFT}s${MODE:+ (${MODE})}"
 1859      # In the background and waited for, as the jobs and the recently played
 1860      # pass are: bash runs a trap only once the foreground command has
 1861      # returned, so with the helper in the foreground the page's CANCEL (INT)
 1862      # and a stop from disable or STOP IT AND PLAY (TERM) waited for the whole
 1863      # pass before the run could answer either (#307 PL-013, #308 F-RA-11).
 1864      # wait returns the moment a trapped signal arrives, and CLIENT is what
 1865      # the EXIT trap ends. CLIENT is timeout, which puts itself and the
 1866      # helper in a process group of their own: the interface's SIGINT to the
 1867      # run's group reaches this script, not the helper, and the EXIT trap's
 1868      # kill of timeout is forwarded to the helper as SIGTERM -- the path the
 1869      # harness's D23 runs under GNU timeout (audit of the fixes, claude
 1870      # G-D-03).
 1871      # Bounded at the process as well (#308 F-RA-10): the helper checks its
 1872      # --seconds between one blocking call and the next, so it is given ten
 1873      # seconds less than the pass has and timeout ends it at the pass's
 1874      # bound whatever it is blocked on (a timeout is images not saved).
 1875      # shellcheck disable=SC2086 -- MODE is one flag or empty, on purpose
 1876      timeout "${SECONDS_LEFT}" "${IMAGE_HELPER}" --seconds "$(( SECONDS_LEFT - 10 ))" ${MODE} >>"${SCAN_LOG}" 2>&1 &
 1877      CLIENT=$!
 1878      wait "${CLIENT}" || RC=$?
 1879      unset CLIENT
 1880      # 0: every image there. 3: every image there, a verify slice left for
 1881      # the next pass. Anything else -- images left behind (1), no store or
 1882      # account (2), a helper that died -- is the pass not done.
 1883      case "${RC}" in
 1884          0|3) ;;
 1885          *) R_IMAGES_WHY=SOME_IMAGES_NOT_SAVED ;;
 1886      esac
 1887      slog "${VERB}: image pass rc=${RC}${R_IMAGES_WHY:+ why=${R_IMAGES_WHY}}"
 1888      return "${RC}"
 1889  }
 1890  
 1891  do_images() {
 1892      local MODE=""
 1893      [ "${1:-}" = "--verify" ] && MODE=--verify
 1894      refuse_unless_ready images
 1895      if ! is_online; then
 1896          say "images: refused, this device is offline"
 1897          tell "why NO_NETWORK"
 1898          exit ${EX_UNAVAILABLE}
 1899      fi
 1900      # The lock carries this pid, so `disable` can ask the run to stop
 1901      # (stop_running_run, #186 PL-30); the TERM trap ends the helper and
 1902      # the EXIT trap clears the progress file, as scan's do. The progress
 1903      # line is route=images at=<epoch>: RUN_ROUTE names the verb, and
 1904      # mark_running's argument is the rest of the line, not the verb --
 1905      # `mark_running images` wrote at=<epoch>images (audit #258 PL-013).
 1906      trap 'stopped images' TERM
 1907      RUN_ROUTE=images
 1908      take_lock images
 1909      mark_running
 1910      trap 'unmark_running; [ -n "${CLIENT:-}" ] && kill "${CLIENT}" 2>/dev/null' EXIT
 1911      local RC=0
 1912      # Bounded at the process too, a grace past the helper's own --seconds
 1913      # (#308 F-RA-10).
 1914      # shellcheck disable=SC2086 -- MODE is one flag or empty, on purpose
 1915      timeout "$(( IMAGE_PASS_SECONDS + 10 ))" "${IMAGE_HELPER}" --seconds "${IMAGE_PASS_SECONDS}" ${MODE} &
 1916      CLIENT=$!
 1917      wait "${CLIENT}" || RC=$?
 1918      CLIENT=""
 1919      slog "images: rc=${RC}${MODE:+ (${MODE})}"
 1920      exit "${RC}"
 1921  }
 1922  
 1923  # refresh [--game <id>|--all]. The service's own pass re-reads, each online
 1924  # hour while the proxy is idle, the cached games played in the last seven
 1925  # days (upstream 59b167c, D-RA-029; patch 005 keeps only its exception
 1926  # boundary), which covers the ordinary case -- not every cached game, and not
 1927  # daily, as this said until #308 F-RA-28. This is for the player standing in
 1928  # front of the device who has just changed
 1929  # something on the site -- reset an achievement, earned one elsewhere -- and
 1930  # wants it true here before going offline (#223).
 1931  do_refresh() {
 1932      local WHICH=()
 1933      case "${1:-}" in
 1934          --all)  WHICH=(--all) ;;
 1935          --game) [ -n "${2:-}" ] || { echo "usage: raofflineproxy-ctl refresh [--all|--game <id>]" >&2; exit ${EX_USAGE}; }
 1936                  WHICH=(--game "${2}") ;;
 1937          "")     ;;
 1938          *)      echo "usage: raofflineproxy-ctl refresh [--all|--game <id>]" >&2; exit ${EX_USAGE} ;;
 1939      esac
 1940      refuse_unless_ready refresh
 1941      if ! is_online; then
 1942          say "refresh: refused, this device is offline"
 1943          tell "why NO_NETWORK"
 1944          exit ${EX_UNAVAILABLE}
 1945      fi
 1946      # As images: the pid in the lock, a TERM trap over the helper, the
 1947      # verb in RUN_ROUTE (audit #258 PL-013).
 1948      trap 'stopped refresh' TERM
 1949      RUN_ROUTE=refresh
 1950      take_lock refresh
 1951      mark_running
 1952      trap 'unmark_running; [ -n "${CLIENT:-}" ] && kill "${CLIENT}" 2>/dev/null' EXIT
 1953      local RC=0
 1954      # The helper looks at its --seconds between games; a game's requests
 1955      # can block past it, so the process is bounded too, a minute's grace
 1956      # past the helper's own ceiling (#308 F-RA-10).
 1957      timeout "$(( TOPUP_TIMEOUT + 60 ))" "${REFRESH_HELPER}" --seconds "${TOPUP_TIMEOUT}" "${WHICH[@]}" &
 1958      CLIENT=$!
 1959      wait "${CLIENT}" || RC=$?
 1960      CLIENT=""
 1961      slog "refresh: rc=${RC} ${WHICH[*]}"
 1962      exit "${RC}"
 1963  }
 1964  
 1965  do_scan() {
 1966      trap 'stopped scan' TERM
 1967      trap 'cancelled scan' INT
 1968      RUN_ROUTE=scan
 1969      take_lock scan
 1970      refuse_unless_ready scan
 1971      mkdir -p "${PROXY_DIR}" || fail "cannot create ${PROXY_DIR}"
 1972      if ! is_online; then
 1973          say "scan: refused, RetroAchievements is not reachable"
 1974          slog "scan refused: offline by the proxy's probe"
 1975          exit ${EX_UNAVAILABLE}
 1976      fi
 1977  
 1978      local LIST
 1979      LIST="$(mktemp /tmp/raofflineproxy-scan.XXXXXX)" || fail "cannot create the list"
 1980      # Everything of the run's goes when the run does, however it ends.
 1981      trap 'rm -f "${LIST}" "${JOBS_FIFO:-}" "${READY_BEFORE:-}" "${READY_AFTER:-}" "${SCAN_CURSOR}.next" "${RUNNING}" "${RUNNING}.tmp"; [ -n "${CLIENT:-}" ] && kill "${CLIENT}" 2>/dev/null' EXIT
 1982  
 1983      local COUNTS
 1984      R_IMAGES_WHY=""
 1985      mark_running
 1986      tell "doing listing"
 1987      if ! COUNTS="$(list_jobs "${LIST}" all 0 2>>"${SCAN_LOG}")"; then
 1988          slog "scan: the library could not be listed"
 1989          tell "why LIBRARY_UNREADABLE"
 1990          write_stamp 1 scan 0 0 "$(count_ready)" 0 0 0 LIBRARY_UNREADABLE
 1991          exit 1
 1992      fi
 1993      local FOUND NEW TRUNC
 1994      FOUND="$(count_of "${COUNTS}" found)"
 1995      NEW="$(count_of "${COUNTS}" new)"
 1996      TRUNC="$(count_of "${COUNTS}" truncated)"
 1997      slog "scan start: ${COUNTS}"
 1998      if [ "${TRUNC}" -eq 1 ]; then
 1999          slog "scan: the walk stopped at the client's cap of files per run; the next scan walks on from ${SCAN_CURSOR}"
 2000      fi
 2001  
 2002      local READY
 2003      if [ "${FOUND}" -eq 0 ]; then
 2004          # Nothing under the ROM folders to look at is a run that completed
 2005          # with nothing to do, not one that could not finish (fork #329: the
 2006          # page read COULDN'T FINISH on a device with no game yet, and the
 2007          # maintainer's reading was that "there was just nothing to scan").
 2008          # rc 0 and no why; the note tells the page and the stamp what there
 2009          # was to say, and the row reads NO GAMES TO SCAN YET.
 2010          READY="$(count_ready)"
 2011          slog "scan done: no games found under ${ROMS_ROOT}, ready=${READY}"
 2012          tell "note NO_GAMES"
 2013          commit_cursor || slog "scan: an old cursor could not be removed; the next walk starts from the top all the same"
 2014          write_stamp 0 scan 0 0 "${READY}" 0 0 0 "" "" 0 NO_GAMES
 2015          tell "done 0|0|${READY}|0"
 2016          exit 0
 2017      fi
 2018      tell "total ${NEW}"
 2019      if [ "${NEW}" -eq 0 ]; then
 2020          tell "note NOTHING_NEW"
 2021          commit_cursor || slog "scan: an old cursor could not be removed; the next walk starts from the top all the same"
 2022          # No game to cache, but the images of what is cached may still be
 2023          # missing -- a pass the last run cut, a badge that did not come --
 2024          # and pressing SCAN again is how a player asks for them (#307
 2025          # PL-060). The same pass, the same verdict.
 2026          run_image_pass scan "${IMAGE_PASS_SECONDS}"
 2027          READY="$(count_ready)"
 2028          local RC0=0 WHY0="${R_IMAGES_WHY}"
 2029          [ -n "${WHY0}" ] && { RC0=1; tell "why ${WHY0}"; }
 2030          slog "scan done: nothing new, ready=${READY}${WHY0:+ why=${WHY0}}"
 2031          write_stamp "${RC0}" scan 0 0 "${READY}" 0 0 0 "${WHY0}"
 2032          tell "done 0|0|${READY}|0"
 2033          exit "${RC0}"
 2034      fi
 2035  
 2036      READY_BEFORE="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && { ready_games_into "${READY_BEFORE}" || { rm -f "${READY_BEFORE}"; READY_BEFORE=""; }; }
 2037      run_jobs page "${LIST}" "${NEW}" 0
 2038  
 2039      READY="$(count_ready)"
 2040      local ADDED=""
 2041      READY_AFTER="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && ready_games_into "${READY_AFTER}" && ADDED="$(games_made_ready "${READY_BEFORE}" "${READY_AFTER}")"
 2042      rm -f "${READY_BEFORE}" "${READY_AFTER}"; READY_BEFORE=""; READY_AFTER=""
 2043      # A measurement that failed is said as one (added_count, PL-031).
 2044      ADDED="$(added_count "${ADDED}" "${R_CACHED}")"
 2045      [ "${ADDED}" = "unknown" ] && slog "scan: the store could not be read before or after the jobs; how many games they made ready is not known (added=unknown)"
 2046      local RC=0 WHY="${R_WHY}"
 2047      if [ -n "${WHY}" ]; then
 2048          RC=1
 2049      elif [ "${R_STOPPED}" -eq 0 ] && [ "${R_CLIENT_RC}" -ne 0 ] && [ "${R_DONE}" -eq 0 ]; then
 2050          # The helper died on its own, before its DONE, without a reason the
 2051          # lines above named: the log has its traceback. (After DONE the games
 2052          # are cached and the exit is the badge downloads', fork #188.)
 2053          RC=1; WHY=SOMETHING_WENT_WRONG
 2054      elif [ "${R_ERRORS}" -gt 0 ]; then
 2055          # A fetch that failed for any game, even between games that went
 2056          # through, is a run that did not finish (D-UI-030: a run whose
 2057          # parts disagree is COULDN'T FINISH); the next run tries them again.
 2058          RC=1; WHY=SOME_GAMES_NOT_SAVED
 2059      fi
 2060      # The images of what this run cached, and of anything cached before it
 2061      # that is still missing one (#212): the same action, finished.
 2062      # The scan has no deadline of its own (the top-up's TOPUP_TIMEOUT is the
 2063      # one clock here), so the pass gets its own ceiling.
 2064      # Whenever the run worked through its jobs -- cached one or not: a
 2065      # library with a ROM RetroAchievements does not know lists a job at
 2066      # every scan, and gating the pass on a cached game left such a scan
 2067      # COMPLETED over badges it never looked at (audit of the fixes, claude
 2068      # G-D-02 = gpt G-D-01). Not after a stop on a refused sign-in or a
 2069      # server that stopped answering.
 2070      [ "${R_STOPPED}" -eq 0 ] && run_image_pass scan "${IMAGE_PASS_SECONDS}"
 2071      # The games' own why comes first; a pass that left images behind is the
 2072      # run's why when the games went through (#307 PL-060).
 2073      if [ -z "${WHY}" ] && [ -n "${R_IMAGES_WHY}" ]; then
 2074          RC=1; WHY="${R_IMAGES_WHY}"
 2075      fi
 2076  
 2077      # The walk's cursor is kept once the run has worked through its jobs; a
 2078      # run stopped short leaves it where it was (claude G-D-06). A cut walk
 2079      # whose cursor could not be kept promises no continuation: the run could
 2080      # not finish, and neither the page nor the stamp says TRUNCATED (gpt
 2081      # G-D-06).
 2082      if [ "${R_DONE}" -eq 1 ] && [ "${R_STOPPED}" -eq 0 ]; then
 2083          if [ "${TRUNC}" -eq 1 ]; then
 2084              if [ "$(count_of "${COUNTS}" cursor_saved)" -ne 1 ] || ! commit_cursor; then
 2085                  slog "scan: the walk's cursor could not be saved; the next scan would take the same slice"
 2086                  TRUNC=0
 2087                  [ -z "${WHY}" ] && { RC=1; WHY=SOMETHING_WENT_WRONG; }
 2088              fi
 2089          else
 2090              commit_cursor || slog "scan: an old cursor could not be removed; the next walk starts from the top all the same"
 2091          fi
 2092      elif [ "${TRUNC}" -eq 1 ]; then
 2093          slog "scan: the run stopped short of its jobs; the cursor stays where it was"
 2094      fi
 2095      rm -f "${SCAN_CURSOR}.next"
 2096      [ "${R_LIMIT}" -eq 1 ] && tell "note LIMIT_REACHED"
 2097      # Not every folder was walked: the page says so (GuiOfflineScan's
 2098      # NOT EVERY FOLDER WAS LOOKED AT. SCAN AGAIN TO CONTINUE.) and the stamp
 2099      # carries it -- the log alone said it before (#307 PL-059).
 2100      [ "${TRUNC}" -eq 1 ] && tell "note TRUNCATED"
 2101      [ "${R_ERRORS}" -gt 0 ] && tell "errors ${R_ERRORS}"
 2102      [ -n "${WHY}" ] && tell "why ${WHY}"
 2103      write_stamp "${RC}" scan "${R_CACHED}" "${R_SKIPPED}" "${READY}" "${R_LIMIT}" "${R_INDEXED}" "${R_ERRORS}" "${WHY}" "${ADDED}" "${TRUNC}"
 2104      slog "scan done: rc=${RC} cached=${R_CACHED} indexed=${R_INDEXED} skipped=${R_SKIPPED} errors=${R_ERRORS} ready=${READY} limit=${R_LIMIT}${WHY:+ why=${WHY}}"
 2105      say "scan: cached ${R_CACHED} (${R_INDEXED} from the index), skipped ${R_SKIPPED}, ${READY} ready${WHY:+; ${WHY}}"
 2106      tell "done ${R_CACHED}|${R_SKIPPED}|${READY}|${R_LIMIT}"
 2107      exit "${RC}"
 2108  }
 2109  
 2110  # index-offline: the interface's index had games to identify and
 2111  # RetroAchievements' hash library did not come -- offline, nearly always
 2112  # (fork #299, D-UI-104). The marker the after-index run leaves when its
 2113  # probe fails is written here without a probe, since the interface already
 2114  # knows the library did not come: the next link-return topup lists the
 2115  # library once, inside the half hour or not, and clears it once that
 2116  # listing's games are handled. The games this index could not identify are
 2117  # not among them -- they have no cheevosId until an index with the library
 2118  # gives them one; the interface runs that index when the link comes up, and
 2119  # its topup --after-index caches them (#308 F-RA-22). Nothing else is
 2120  # touched; exit 0.
 2121  # index-pending holds a token -- when it was written and by which process --
 2122  # so a top-up can tell the marker its listing was made for from a newer one
 2123  # an index writes while it runs (audit of the fixes, gpt G-D-03). Whole or
 2124  # not at all. A marker an earlier build left is an empty file, and reads as
 2125  # one token like any other.
 2126  #
 2127  # The marker has a lock of its own (audit of the fix round, gpt G2-D-03):
 2128  # the top-up's token check and its removal are one step under it
```


## projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl @ 8ebaf8daad: lines 2131-2455 (excerpt of 2455)

```text
 2131  # one. It is held for a read, a rename or an unlink, never across anything
 2132  # that waits. Busybox flock has no -w: five tries a second apart. A lock
 2133  # that cannot be had leaves the safe side -- the write goes ahead, since a
 2134  # notification lost leaves the player's games uncached, and the removal
 2135  # does not, since a marker kept costs one more listing.
 2136  PENDING_LOCK="/var/run/raofflineproxy-index-pending.lock"
 2137  pending_lock() {
 2138      local TRY=0
 2139      exec 6<>"${PENDING_LOCK}" 2>/dev/null || return 1
 2140      until flock -n 6; do
 2141          TRY=$((TRY + 1))
 2142          if [ "${TRY}" -ge 5 ]; then exec 6>&-; return 1; fi
 2143          sleep 1
 2144      done
 2145  }
 2146  
 2147  pending_unlock() {
 2148      exec 6>&-
 2149  }
 2150  
 2151  write_index_pending() {
 2152      local LOCKED=0 RC=0
 2153      if pending_lock; then LOCKED=1; else say "index-pending: its lock could not be had; written without it"; fi
 2154      printf '%s %s %s\n' "$(date +%s)" "$$" "${RANDOM}" > "${INDEX_PENDING}.tmp" 2>/dev/null \
 2155          && mv -f "${INDEX_PENDING}.tmp" "${INDEX_PENDING}" || RC=1
 2156      [ "${LOCKED}" -eq 1 ] && pending_unlock
 2157      return "${RC}"
 2158  }
 2159  
 2160  # ack_index_pending <token>: remove index-pending if it is still the marker
 2161  # the caller's listing was made for. 0 removed, 1 kept (a newer marker), 2
 2162  # kept because the lock could not be had.
 2163  ack_index_pending() {
 2164      # Taken aside by rename before it is read: a writer that could not have
 2165      # the lock renames a newer marker into place (write_index_pending's
 2166      # fallback), and a compare-then-rm on the shared path removed that newer
 2167      # one (the audit of the fixes, gpt G3-D-03). Whatever lands on the path
 2168      # after the rename is somebody else's and stays; a moved marker that is
 2169      # not the caller's token goes back.
 2170      local RC=1 mine="${INDEX_PENDING}.ack.$$"
 2171      pending_lock || return 2
 2172      if mv -f "${INDEX_PENDING}" "${mine}" 2>/dev/null; then
 2173          if [ "$(cat "${mine}" 2>/dev/null)" = "${1}" ]; then
 2174              rm -f "${mine}" && [ ! -e "${mine}" ] && RC=0
 2175          else
 2176              [ -e "${INDEX_PENDING}" ] || mv -f "${mine}" "${INDEX_PENDING}" 2>/dev/null
 2177              rm -f "${mine}" 2>/dev/null
 2178          fi
 2179      fi
 2180      pending_unlock
 2181      return "${RC}"
 2182  }
 2183  
 2184  do_index_offline() {
 2185      mkdir -p "${PROXY_DIR}" || fail "cannot create ${PROXY_DIR}"
 2186      write_index_pending || fail "cannot write ${INDEX_PENDING}"
 2187      slog "index ran offline: the hash library did not come (index-pending); the library is listed once at the link's return"
 2188  }
 2189  
 2190  # topup [--after-index]. --after-index is the run the interface starts as
 2191  # its hasher finishes (ThreadedHasher, with the toggle on): it waits for a
 2192  # top-up already running instead of giving way to it, and it does not count
 2193  # the half-hour since the last attempt against itself -- the index has just
 2194  # grown, and that is the one moment a top-up is sure to have something to
 2195  # do. It marks the attempt like any other, once its probe has answered.
 2196  do_topup() {
 2197      local AFTER_INDEX=0 AI_NOTE=""
 2198      RUN_ROUTE=topup
 2199      if [ "${1:-}" = "--after-index" ]; then AFTER_INDEX=1; AI_NOTE=" (after the index)"; fi
 2200      trap 'stopped topup' TERM
 2201      # One deadline, taken before anything can wait: the lock, the probes,
 2202      # the listing and both passes all spend from it, so the run ends within
 2203      # TOPUP_TIMEOUT of this moment whatever each part costs (#186 PL-28).
 2204      local START
 2205      START="$(date +%s)"
 2206      take_lock topup "${AFTER_INDEX}" "${START}"
 2207      refuse_unless_ready topup >/dev/null
 2208      mkdir -p "${PROXY_DIR}" || fail "cannot create ${PROXY_DIR}"
 2209  
 2210      # Bounded: one attempt per interval, whatever the link does. The mark
 2211      # is read here and set only below, once a probe has reached the server.
 2212      # An index that ran offline (index-pending, below) is the one reason to
 2213      # run inside the interval: the player added games and the toast said
 2214      # they are looked up next time the device is connected (fork #299,
 2215      # D-UI-104), and "next time" is this link, not the one after the half
 2216      # hour. Only a marker written since the last attempt: one a failed
 2217      # attempt left behind (#307 PL-055, below) waits out the half hour like
 2218      # any other run, so a link that flaps does not turn it into a request
 2219      # storm.
 2220      local PENDING_DUE=0
 2221      if [ -e "${INDEX_PENDING}" ] && { [ ! -e "${TOPUP_MARK}" ] || [ "${INDEX_PENDING}" -nt "${TOPUP_MARK}" ]; }; then
 2222          PENDING_DUE=1
 2223      fi
 2224      if [ "${AFTER_INDEX}" -eq 0 ] && [ -e "${TOPUP_MARK}" ] && [ "${PENDING_DUE}" -eq 0 ]; then
 2225          local AGE=$(( $(date +%s) - $(stat -c %Y "${TOPUP_MARK}" 2>/dev/null || echo 0) ))
 2226          if [ "${AGE}" -ge 0 ] && [ "${AGE}" -lt "${TOPUP_INTERVAL}" ]; then
 2227              exit 0
 2228          fi
 2229          # The link's return has one question -- was a game played since the
 2230          # last attempt? -- and no game means nothing to look for: out before
 2231          # the probe, the mark untouched (fork #299, D-RA-035: the maintainer,
 2232          # a nine-second check at wake with nothing to add).
 2233          local HIST
 2234          HIST="$(history_path)"
 2235          if [ ! -e "${INDEX_PENDING}" ] && { [ ! -e "${HIST}" ] || [ ! "${HIST}" -nt "${TOPUP_MARK}" ]; }; then
 2236              slog "topup: no game played since the last attempt (${HIST} is not newer than the mark); nothing to look for, skipped"
 2237              exit 0
 2238          fi
 2239      fi
 2240  
 2241      # The hook fires when the address arrives, which can be well before the
 2242      # resolver answers (fork #175: 20-45 s behind on that boot shape), so
 2243      # the probe gets the token check's patience -- PROBE_TRIES tries,
 2244      # PROBE_INTERVAL apart, inside the deadline. A probe that never reached
 2245      # RetroAchievements is not an attempt: no mark, so the next link event
 2246      # (or the after-index run) tries again rather than waiting out the half
 2247      # hour on a connect that was never tested (#186 PL-04).
 2248      local TRY=0 ONLINE=0
 2249      while [ "${TRY}" -lt "${PROBE_TRIES}" ]; do
 2250          TRY=$((TRY + 1))
 2251          if is_online; then ONLINE=1; break; fi
 2252          [ "${TRY}" -lt "${PROBE_TRIES}" ] || break
 2253          [ "$(time_left "${START}")" -gt "${PROBE_INTERVAL}" ] || break
 2254          pause "${PROBE_INTERVAL}"
 2255      done
 2256      if [ "${ONLINE}" -eq 0 ]; then
 2257          slog "topup refused: offline by the proxy's probe (${TRY} probes); not counted as an attempt"
 2258          if [ "${AFTER_INDEX}" -eq 1 ]; then
 2259              write_index_pending
 2260              slog "topup: the index's games wait for the link (index-pending)"
 2261          fi
 2262          exit ${EX_UNAVAILABLE}
 2263      fi
 2264      touch "${TOPUP_MARK}"
 2265  
 2266      local LIST
 2267      LIST="$(mktemp /tmp/raofflineproxy-topup.XXXXXX)" || fail "cannot create the list"
 2268      trap 'rm -f "${LIST}" "${JOBS_FIFO:-}" "${SC_OUT:-}" "${READY_BEFORE:-}" "${READY_AFTER:-}" "${RUNNING}" "${RUNNING}.tmp"; [ -n "${CLIENT:-}" ] && kill "${CLIENT}" 2>/dev/null' EXIT
 2269      mark_running
 2270      # The games ready for this account before either pass, for added=.
 2271      READY_BEFORE="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && { ready_games_into "${READY_BEFORE}" || { rm -f "${READY_BEFORE}"; READY_BEFORE=""; }; }
 2272  
 2273      # First, every game the interface's index knows and the client has not
 2274      # cached -- the games added and indexed since the last run, and with a
 2275      # library nobody scanned, as many as the deadline allows (the rest next
 2276      # time). Nothing is hashed here.
 2277      local COUNTS LRC NEW=0 CACHED=0 SKIPPED=0 INDEXED=0 LIMIT=0 ERRORS=0 WHY="" LEFT ADDED="" LISTED=0 LIST_WHY=""
 2278      local PENDING_SEEN=0 PENDING_TOKEN=***
 2279      LEFT="$(time_left "${START}")"
 2280      if [ "${LEFT}" -le 0 ]; then
 2281          WHY=TOOK_TOO_LONG
 2282          slog "topup${AI_NOTE}: the deadline passed while waiting for the lock and the probe"
 2283      elif [ "${AFTER_INDEX}" -eq 0 ] && [ ! -e "${INDEX_PENDING}" ]; then
 2284          # New games are the index's to find -- at startup and with UPDATE
 2285          # GAMELISTS, both of which end in this run with --after-index -- so
 2286          # the link's return does not list the library (fork #299, D-RA-035),
 2287          # unless an index ran offline and left its marker: then once, below.
 2288          slog "topup at the link's return: the recently played pass alone (new games are the index's)"
 2289      else
 2290          # The marker stays until the listing it stands for, and the games
 2291          # that listing found, have been handled -- removed below, never
 2292          # here: a listing that failed, a run cut by the deadline or stopped
 2293          # part-way (STOP IT AND PLAY, disable), a game whose fetch failed,
 2294          # each left no marker and so no retry (#307 PL-055).
 2295          if [ "${AFTER_INDEX}" -eq 0 ]; then
 2296              slog "topup at the link's return: an index ran offline (index-pending); the library listed once for it -- again after the half hour if this run does not finish"
 2297          fi
 2298          # The marker this listing answers, as it reads now: one written
 2299          # after this moment is a newer promise, and stays (gpt G-D-03).
 2300          if [ -e "${INDEX_PENDING}" ]; then PENDING_SEEN=1; PENDING_TOKEN=*** "${INDEX_PENDING}" 2>/dev/null)"; fi
 2301          COUNTS="$(list_jobs "${LIST}" indexed "${LEFT}" 2>>"${SCAN_LOG}")"
 2302          LRC=$?
 2303          if [ "${LRC}" -eq 0 ]; then
 2304              LISTED=1
 2305              NEW="$(count_of "${COUNTS}" new)"
 2306              slog "topup start${AI_NOTE}: ${COUNTS}"
 2307          elif [ "${LRC}" -eq 124 ]; then
 2308              WHY=TOOK_TOO_LONG
 2309              slog "topup${AI_NOTE}: the listing did not finish inside the deadline"
 2310          else
 2311              # The recently played pass still runs -- it needs no index -- but
 2312              # a run a part of which failed is one that could not finish
 2313              # (D-UI-030): the why is kept for the stamp below (audit of the
 2314              # fixes, claude G-D-13; it read COMPLETED before).
 2315              slog "topup${AI_NOTE}: the interface's index could not be read; the recently played pass runs alone"
 2316              LIST_WHY=LIBRARY_UNREADABLE
 2317          fi
 2318      fi
 2319      if [ -z "${WHY}" ] && [ "${NEW}" -gt 0 ]; then
 2320          LEFT="$(time_left "${START}")"
 2321          if [ "${LEFT}" -le 0 ]; then
 2322              WHY=TOOK_TOO_LONG
 2323          else
 2324              run_jobs quiet "${LIST}" "${NEW}" "${LEFT}"
 2325              CACHED="${R_CACHED}"; SKIPPED="${R_SKIPPED}"; INDEXED="${R_INDEXED}"; LIMIT="${R_LIMIT}"; ERRORS="${R_ERRORS}"; WHY="${R_WHY}"
 2326              # A helper killed by the bound after its DONE finished its games
 2327              # (fork #188: badge downloads kept it alive); only one cut before
 2328              # DONE makes the run one that did not finish.
 2329              if [ -z "${WHY}" ] && [ "${R_STOPPED}" -eq 0 ] && [ "${R_CLIENT_RC}" -ne 0 ] && [ "${R_DONE}" -eq 0 ]; then
 2330                  WHY=RETROACHIEVEMENTS_STOPPED_ANSWERING
 2331                  [ "${R_CLIENT_RC}" -eq 124 ] && WHY=TOOK_TOO_LONG
 2332              fi
 2333              # As in scan: a game whose fetch failed is a run that did not
 2334              # finish, and the next top-up tries it again (#186 PL-24).
 2335              [ -z "${WHY}" ] && [ "${ERRORS}" -gt 0 ] && WHY=SOME_GAMES_NOT_SAVED
 2336              slog "topup indexed pass: cached=${CACHED} indexed=${INDEXED} skipped=${SKIPPED} errors=${ERRORS} rc=${R_CLIENT_RC}${WHY:+ why=${WHY}}"
 2337          fi
 2338      fi
 2339  
 2340      # The index's games are handled -- listed, and each cached or passed
 2341      # over -- so whatever index-pending stood for is done; after-index runs
 2342      # included, since their listing is the same (#307 PL-055).
 2343      # The check and the removal are one step under the marker's lock
 2344      # (ack_index_pending, gpt G2-D-03).
 2345      if [ "${LISTED}" -eq 1 ] && [ -z "${WHY}" ] && [ -e "${INDEX_PENDING}" ]; then
 2346          local ACK=1
 2347          [ "${PENDING_SEEN}" -eq 1 ] && { ack_index_pending "${PENDING_TOKEN}"; ACK=$?; }
 2348          case "${ACK}" in
 2349              0) slog "topup: the pending index's listing and its games are handled; index-pending removed" ;;
 2350              1) slog "topup: an index left index-pending while this run was at its jobs; kept for the next run" ;;
 2351              *) slog "topup: index-pending's lock could not be had; the marker is kept and the next run lists for it again" ;;
 2352          esac
 2353      fi
 2354  
 2355      # Then the client's own recently-played pass for what the index missed
 2356      # -- RetroArch's history, PPSSPP's recent list -- each not yet cached,
 2357      # with the client's own pause between requests, in what is left of the
 2358      # deadline. Its progress lines are JSON; the last line is the result.
 2359      # Run in the background and waited for, so a stop request (disable)
 2360      # reaches this process at once and its EXIT trap ends the client.
 2361      LEFT="$(time_left "${START}")"
 2362      if [ -z "${WHY}" ] && [ "${LEFT}" -ge 60 ]; then
 2363          local SRC RESULT
 2364          SC_OUT="$(mktemp /tmp/raofflineproxy-topup-sc.XXXXXX)" || fail "cannot create the result file"
 2365          mark_running
 2366          timeout "${LEFT}" ${PROXY_PY} run-smart-cache > "${SC_OUT}" 2>>"${SCAN_LOG}" &
 2367          CLIENT=$!
 2368          wait "${CLIENT}" 2>/dev/null
 2369          SRC=$?
 2370          unset CLIENT
 2371          unmark_running
 2372          RESULT="$(grep '"type":"result"' "${SC_OUT}" 2>/dev/null | tail -n 1)"
 2373          rm -f "${SC_OUT}"; SC_OUT=""
 2374          local SC=0 SS=0 SL=0
 2375          if [ -n "${RESULT}" ]; then
 2376              read -r SC SS SL < <(python3 -c '
 2377  import json, sys
 2378  r = json.loads(sys.argv[1])
 2379  print(int(r.get("cached", 0)), int(r.get("skipped", 0)), 1 if r.get("limit_reached") else 0)
 2380  ' "${RESULT}" 2>/dev/null || echo "0 0 0")
 2381          fi
 2382          CACHED=$((CACHED + SC)); SKIPPED=$((SKIPPED + SS)); [ "${SL}" -eq 1 ] && LIMIT=1
 2383          slog "topup recently played: rc=${SRC} cached=${SC} skipped=${SS} limit=${SL}"
 2384          if [ "${SRC}" -ne 0 ]; then
 2385              WHY=RETROACHIEVEMENTS_STOPPED_ANSWERING
 2386              [ "${SRC}" -eq 124 ] && WHY=TOOK_TOO_LONG
 2387          fi
 2388      elif [ -z "${WHY}" ]; then
 2389          slog "topup: no time left for the recently played pass (${LEFT}s)"
 2390      fi
 2391  
 2392      # A listing that could not be read is the run's why when nothing later
 2393      # had one of its own.
 2394      [ -z "${WHY}" ] && [ -n "${LIST_WHY}" ] && WHY="${LIST_WHY}"
 2395      local READY MADE
 2396      READY="$(count_ready)"
 2397      # added=: the games the two passes made ready for this account, from the
 2398      # store before and after (#308 F-RA-10, F-RA-15); unknown when the store
 2399      # could not be read, never the passes' cache operations in its place
 2400      # (added_count, PL-031).
 2401      READY_AFTER="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && ready_games_into "${READY_AFTER}" && MADE="$(games_made_ready "${READY_BEFORE}" "${READY_AFTER}")" && ADDED="${MADE}"
 2402      rm -f "${READY_BEFORE}" "${READY_AFTER}"; READY_BEFORE=""; READY_AFTER=""
 2403      ADDED="$(added_count "${ADDED}" "${CACHED}")"
 2404      [ "${ADDED}" = "unknown" ] && slog "topup${AI_NOTE}: the store could not be read before or after the passes; how many games they made ready is not known (added=unknown)"
 2405      slog "topup done: cached=${CACHED} added=${ADDED} indexed=${INDEXED} skipped=${SKIPPED} errors=${ERRORS} ready=${READY} limit=${LIMIT} took=$(( $(date +%s) - START ))s${WHY:+ why=${WHY}}"
 2406  
 2407      # The line under the row changes only when the top-up has something to
 2408      # say: games it added, or a run that could not finish. Nothing new
 2409      # leaves the last scan's line as it was.
 2410      if [ -n "${WHY}" ]; then
 2411          write_stamp 1 topup "${CACHED}" "${SKIPPED}" "${READY}" "${LIMIT}" "${INDEXED}" "${ERRORS}" "${WHY}" "${ADDED}"
 2412          say "topup could not finish (${WHY}); cached ${CACHED}, ${READY} ready"
 2413          exit 1
 2414      fi
 2415      if [ "${CACHED}" -gt 0 ]; then
 2416          # The top-up is the background run, so it is where the store is
 2417          # verified as well as filled: a slice per run from the cursor, so
 2418          # the whole store comes round without any one run being long (#213).
 2419          run_image_pass topup "$(time_left "${START}")" --verify
 2420          if [ -n "${R_IMAGES_WHY}" ]; then
 2421              # The games are cached; their images are not all there (#307
 2422              # PL-060): a run whose parts disagree could not finish.
 2423              write_stamp 1 topup "${CACHED}" "${SKIPPED}" "${READY}" "${LIMIT}" "${INDEXED}" "${ERRORS}" "${R_IMAGES_WHY}" "${ADDED}"
 2424              say "topup could not finish (${R_IMAGES_WHY}); cached ${CACHED}, ${READY} ready"
 2425              exit 1
 2426          fi
 2427          write_stamp 0 topup "${CACHED}" "${SKIPPED}" "${READY}" "${LIMIT}" "${INDEXED}" "${ERRORS}" "" "${ADDED}"
 2428          say "topup: cached ${CACHED} game(s), ${INDEXED} from the index; ${READY} ready"
 2429      fi
 2430      exit 0
 2431  }
 2432  
 2433  case "${1:-}" in
 2434      enable)  do_enable ;;
 2435      disable) do_disable ;;
 2436      start)   do_start ;;
 2437      stop)    do_stop ;;
 2438      status)  do_status ;;
 2439      pending) do_pending ;;
 2440      pending-ids) do_pending_ids ;;
 2441      account) do_account ;;
 2442      summary) do_summary ;;
 2443      flushed) do_flushed ;;
 2444      scan)    do_scan ;;
 2445      topup)   do_topup "${2:-}" ;;
 2446      index-offline) do_index_offline ;;
 2447      ready)   do_ready ;;
 2448      listening) do_listening "${2:-}" "${3:-}" ;;
 2449      images)  do_images "${2:-}" ;;
 2450      refresh) do_refresh "${2:-}" "${3:-}" ;;
 2451      *)
 2452          echo "Usage: raofflineproxy-ctl {enable|disable|start|stop|status|pending|pending-ids|account|summary|flushed|scan|topup [--after-index]|index-offline|images [--verify]|refresh [--all|--game <id>]|listening [--wait <seconds>]|ready}" >&2
 2453          exit 2
 2454      ;;
 2455  esac
```
