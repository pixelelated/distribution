### 1. Where a credential travels (Q2; F-01, F-02, F-05, F-25)

#### R-1: Unauthenticated offline login token disclosure (F-01, A-1)
- **Status:** confirmed
- **Evidence:** `proxy_service.py:452-474`, `proxy_service.py:491-507`; `007-cached-sign-in-of-the-configured-account.patch` (`auth.py:86-110`, `auth.py:142`)
- **Analysis:** When `action` is `"login"` or `"login2"` (`ALWAYS_TRY_UPSTREAM_ACTIONS`, `proxy_service.py:86` in patch 001), `process_proxy_request` first calls `self.forward_to_upstream_result(method, path, raw_body, headers)` (`:453`), even if `X-RA-Store-Only: 1` was sent (`:483`). If the upstream call returns `success` or `http_error` (such as `401` or `403`), that upstream response is returned directly (`:454-471`); only when upstream fails to answer (connection, DNS, or timeout error) does `:472` call `handle_offline_login`. `handle_offline_login` (`:491-507`) checks only that `action in ALWAYS_TRY_UPSTREAM_ACTIONS`, `u=` is non-empty (`:497-499`), and `self.storage.get_cache(cache_keys.login(user))` exists (`:501-503`), serving `cached["responseBody"]` (which contains `"Token"`) without inspecting `p=`, `t=`, token invalidity, or whether `user` is the currently configured account.

#### R-2: Loopback peer check vs. missing `Host`/`Origin` validation (F-02, A-2)
- **Status:** narrowed
- **Evidence:** `proxy_service.py:290-292`, `proxy_service.py:304`, `011-offline-login-header.patch` (`proxy_service.py:172-188`)
- **Analysis:** The first reader missed the explicit peer-address check in `ProxyRequestHandler._handle_request` (`proxy_service.py:290-292`), which rejects any connection where `self.client_address[0] not in {"127.0.0.1", "::1"}` with `403 {"Error":"loopback_only"}` (as Astra's `A-2` caught). However, neither `_handle_request` nor `response_head` (`proxy_service.py:172-188`) checks `Host` or `Origin` or emits CORS headers. A cross-origin page running in a browser/WebKit view on the device cannot read the response directly without CORS, and DNS rebinding (which makes `127.0.0.1:8080` same-origin while connecting from `127.0.0.1`) would require external DNS resolution to succeed for the rebind while upstream `retroachievements.org` simultaneously fails in `forward_to_upstream_result` (`:453-474`).

#### R-3: Completeness of `t=` and `p=` redaction in logs and upload bundles (A-3)
- **Status:** narrowed
- **Evidence:** `utils.py:110-124`, `network.py:21`, `proxy_service.py:315-321`, `log_uploader.py:52-55`, `log_uploader.py:83-113`, `log_uploader.py:354-380`
- **Analysis:** In `utils.py:110-124`, `redact_query_tokens` and `redact_form_tokens` redact only lowercase literal `t` and `p` keys, even though `network.py:21` defines `REDACTED_QUERY_KEYS = {"p", "t", "token", "password"}` (the `redacted_url` implementation in `network.py` is `outside the packet`). In `utils.py:110`, `_QUERY_SECRET_PATTERN` misses uppercase (`T=`, `P=`) and percent-encoded parameter names (`%74=`, `%70=`), and in `proxy_service.py:319`, `redact_form_tokens(body)` reparses the POST body with `parse_qsl`/`urlencode` (`utils.py:120-124`), which only matches standard form-encoded `t`/`p` fields. In `log_uploader.py:52-55`, `_SENSITIVE_CACHE_ENTRY` redacts quarantined JSON store files only when `"cacheKey": "login2::..."` precedes `"responseBody"` and matches well-formed JSON quotes, which is fragile on a file quarantined specifically because its JSON was corrupted (`log_uploader.py:370-379`).

#### R-4: Exception texts printed to `scan.log` and stdout by the helpers (A-4)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-cache-indexed:185-188`, `raofflineproxy-cache-indexed:202-204`, `raofflineproxy-refresh:125-134`, `raofflineproxy-refresh:216-219`, `raofflineproxy-cache-images:422-424`, `network.py:400-428`, `auth.py:127-134`
- **Analysis:** The helpers print raw exception strings (`{error}` / `{exc}`) to stdout or stderr (`scan.log`) when `resolve_credentials`, `cache_indexed`, `add_rom_to_cache`, `refresh_game_patch`, or `cache_unlocks` raises. In the excerpts provided, `auth.login_and_cache_token` (`auth.py:127-134`) catches exceptions and returns `None` rather than raising, and `urllib.error.HTTPError.__str__` in `network.py:400-428` formats only `code` and `msg` (not `error.url`, even though `error.url` contains `t=` or `p=`). However, the `URLError` and generic exception handlers in `http_get` (`network.py:429-507`), as well as `rom_cache.py` and `rom_browser.py`, are `outside the packet`, so `02`'s claim must be narrowed to *no credential-bearing exception text found in the lines read* (confirming `A-4`).

#### R-5: Username on `python3` argv and file creation modes (F-05, F-25, A-5)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:616`, `raofflineproxy-ctl:647`, `raofflineproxy-ctl:764`, `raofflineproxy-ctl:1029`, `raofflineproxy-ctl:1244-1246`, `raofflineproxy-ctl:1265`; `raofflineproxy.service:26-44`
- **Analysis:** The comment at `raofflineproxy-ctl:1244-1246` (*"The account name reaches the listing through the environment (RA_SCAN_USER), never a command line"*) is written inside `list_jobs`'s block comment and `list_jobs` obeys it at `:1265`, while four other `python3` invocations (`:616`, `:647`, `:764`, `:1029`) pass the public username on argv (confirming `A-5`). Neither `raofflineproxy.service` nor the four scripts set `UMask=` or `umask`, so files created by them inherit the process umask (`0022` on the guest, yielding `0644 root:root` on observed files including `proxy.sqlite3`, which holds the session token in `login2::<user>`). Because `storage.py` beyond line 168 is `outside the packet`, F-25 is narrowed to the writers in the packet and the files observed on the guest.

---

### 2. What runs as root on an unauthenticated port (Q1; F-03, F-04)

#### R-6: Foreign `0.0.0.0:8080` listener in `port_listening` and `do_enable` race (F-03, A-6)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:451-482`, `raofflineproxy-ctl:925-956`, `raofflineproxy.service:27-40`, `proxy_service.py:268-270`, `config.py:368-377`
- **Analysis:** `port_listening` (`raofflineproxy-ctl:925-937`) accepts any TCP `LISTEN` (`0A`) entry at `0100007F:1F90`, `00000000:1F90`, or `0000000000000000FFFF00000100007F:1F90` in `/proc/net/tcp{,6}` without checking socket ownership or PID. Contrary to Astra's `A-6` assumption that `do_enable` cannot complete because Python's `bind()` to `127.0.0.1:8080` fails against `0.0.0.0:8080`, `raofflineproxy.service` uses `Type=simple` (`:27`) with `ExecStartPost=/usr/bin/raofflineproxy-ctl listening --wait 30` (`:40`): systemd starts `ExecStartPost` immediately after forking Python (which takes seconds to import modules, per `raofflineproxy.service:34-36`), so `ExecStartPost` sees the pre-existing foreign `0.0.0.0:8080` listener on its first poll and exits `0`, allowing `systemctl start` and `do_enable` (`:452-482`) to complete and turn the toggle on before Python reaches `bind()` and dies with `EADDRINUSE`! However, `setsettings.sh:536` is `outside the packet` (quoted only in `02` and `03`), so the launcher-routing half of F-03 cannot be verified from the packet alone.

#### R-7: Exposure from running `raofflineproxy.service` as root with no systemd hardening (F-04, A-7)
- **Status:** confirmed
- **Evidence:** `raofflineproxy.service:1-46`, `package.mk:108-114`, `package.mk:146-149`, `proxy_service.py:1458-1483`
- **Analysis:** `raofflineproxy.service` sets no `User=`, `NoNewPrivileges=`, `ProtectSystem=`, `ProtectHome=`, `PrivateTmp=`, `ReadWritePaths=`, `CapabilityBoundingSet=`, `RestrictAddressFamilies=`, `SystemCallFilter=`, or `UMask=`. Even on a single-user handheld where local processes already run as root, this service processes untrusted external inputs: HTTP/HTTPS responses and PNGs from the network, and ROM/archive/disc images on `/storage/roms` parsed in-process by the native C library `libraproxy_rchash.so` (`rcheevos`, `libchdr`, `miniz`, `lzma`, `zstd`, `package.mk:108-114`) via `FolderWatcher` and `CacheQueueWorker` (`proxy_service.py:1460-1482`). Without hardening, a parser or network vulnerability in the service has unrestricted root access to the entire OS, `/dev`, network namespaces, and all credentials under `/storage`.

---

### 3. A check whose failure reads as success (Q3, Q6; F-06, F-07, F-08, F-15, F-16, F-17, F-18, F-24)

#### R-8: `stop_running_run` open failure and ignored return status in `do_disable` (F-06, A-8)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:490-515`, `raofflineproxy-ctl:525`
- **Analysis:** In `stop_running_run` (`raofflineproxy-ctl:491-492`), both `[ -e "${SCAN_LOCK}" ] || return 0` and `exec 7<>"${SCAN_LOCK}" || return 0` return `0` when the lock file cannot be opened (for instance, if `/var/run/raofflineproxy-scan.lock` was replaced with a directory, as reproduced on the guest). Worse, as Astra's `A-8` identified, `do_disable` (`:525`) calls `stop_running_run` without checking its return code, so even when `stop_running_run` detects a running scan/top-up, sends `SIGTERM`, waits `STOP_WAIT` (10 s), and returns `1` (`:504-507`), `do_disable` still stops the service (`:526`), removes the marker (`:527`), and exits `0` while the scan or top-up is still running.

#### R-9: Unchecked `write_stamp` status and directory target hazard (F-07, A-9)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:1073-1095`, `raofflineproxy-ctl:1818`, `raofflineproxy-ctl:1990`, `raofflineproxy-ctl:2014`, `raofflineproxy-ctl:2031`, `raofflineproxy-ctl:2103`, `raofflineproxy-ctl:2411`, `raofflineproxy-ctl:2423`, `raofflineproxy-ctl:2427`
- **Analysis:** `write_stamp` (`:1093-1094`) returns non-zero when `mkdir -p "${PROXY_DIR}"`, `printf ... > "${SCAN_STAMP}.tmp"`, or `mv -f "${SCAN_STAMP}.tmp" "${SCAN_STAMP}"` fails, but all eight callers ignore its return value. Consequently, if `last-scan` cannot be written (e.g., disk full on `/storage`), `do_scan` and `do_topup` still exit `0` on success paths (`:2016`, `:2033`, `:2107`, `:2430`) and leave the previous run's `last-scan` stamp in place. In addition, unlike `commit_cursor` (`:1112`), `write_stamp` does not check `[ ! -d "${SCAN_STAMP}" ]` before `mv -f` (so if `last-scan` is a directory, `mv -f` moves `last-scan.tmp` inside it and returns `0`), and does not remove `${SCAN_STAMP}.tmp` if `printf` fails mid-write.

#### R-10: `list_jobs` opening the store read-write via `Storage()` (F-08, A-10)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:1417`, `storage.py:73-167`
- **Analysis:** `list_jobs` instantiates `storage = Storage()` (`raofflineproxy-ctl:1417`), which opens `proxy.sqlite3` read-write (`storage.py:87`), enables `WAL` mode (`:110`), creates tables, indexes, and triggers (`:115-156`), runs schema migrations (`:163-166`), and runs `_index_missing_game_meta()` and `_import_legacy_json()` (`:92-93`), without even calling `storage.close()` at the end of `list_jobs`. This is a real violation of the ctl's read-only store boundary, though it is a write-side effect rather than "a check whose failure reads as success" (if `Storage()` raises, `list_jobs` exits non-zero and triggers `LIBRARY_UNREADABLE` at `:1987-1991`).

#### R-11: Unreadable or missing `run-smart-cache` result line in `do_topup` (F-15, A-11)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:2366-2387`
- **Analysis:** In `do_topup` (`:2366-2387`), `RESULT` is extracted by `grep '"type":"result"' "${SC_OUT}" 2>/dev/null | tail -n 1` (`:2372`). If `run-smart-cache` exits `0` (`SRC=0`) without emitting a line matching the exact substring `"type":"result"` (e.g., different JSON spacing or truncated stdout), `RESULT` is empty and `SC=0 SS=0 SL=0` (`:2374-2375`); if `RESULT` is matched but malformed JSON, the `python3 -c ... || echo "0 0 0"` fallback (`:2376-2380`) likewise sets `SC=0 SS=0 SL=0`. Because `:2384` only checks `if [ "${SRC}" -ne 0 ]`, both failures read as a clean pass that cached 0 games.

#### R-12: `count_ready` pipeline and fallback turning read errors into `0` (F-16, A-12)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:849-852`, `raofflineproxy-ctl:888-901`
- **Analysis:** `count_ready` (`:888-897`) violates its own comment at `:851-852` (*"a number that is not known is never invented"*) in three ways: (1) if `${READY_FILE}` is a directory, `[ -s "${READY_FILE}" ]` (`:890`) is true on a non-empty directory inode, `grep` fails with empty output, and `:895` sets `N=0` without even trying `${QUEUE}`; (2) if `${READY_FILE}` is absent/empty and `${QUEUE}` exists (`:892-893`), `N="$(${PROXY_PY} cached-games-count 2>/dev/null | tail -n 1)"` discards `${PROXY_PY}`'s exit code because `pipefail` is off, turning a failed command's empty (or non-numeric) output into `N=0` at `:895`; and (3) as Astra's `A-12` noted, if a failing `cached-games-count` prints any number on its last stdout line before exiting non-zero, `count_ready` trusts and prints that number.

#### R-13: `cannot_tell` sites and `do_account`'s non-dict JSON handling (A-13)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:568-588`, `raofflineproxy-ctl:593-620`, `raofflineproxy-ctl:640-668`, `raofflineproxy-ctl:746-801`, `raofflineproxy-ctl:888-901`
- **Analysis:** Aside from `do_ready` (`:899-901`, which never calls `cannot_tell` at all, F-16), `do_account` (`:764-794`) has a reachable branch that bypasses `cannot_tell`: if the `login2::<user>` row's `responseBody` is valid JSON but not a JSON object (e.g., `[]`, `null`, or a number), `if not isinstance(body, dict) ...: sys.exit(1)` (`:780-781`) exits `1` instead of `3`, which `do_account` (`:790-791`) treats as "no points" rather than calling `cannot_tell` (confirming `A-13`). Furthermore, in `do_account` (`:783-784`), `int(body["Score"])` accepts JSON booleans (`True`/`False`) because `bool` is a subclass of `int` in Python, printing `score=1` or `score=0` instead of exiting `3`. (Note that `do_summary` lines `669-745` and `do_pending` lines `579-581` are `outside the packet`.)

#### R-14: Non-UTF-8 ROM filename aborting `list_jobs` (F-17, A-14)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:1587`, `raofflineproxy-ctl:1672-1674`, `raofflineproxy-ctl:1987-1991`, `raofflineproxy-ctl:2301-2317`, `raofflineproxy-cache-indexed:149`
- **Analysis:** When Python walks a filesystem containing a non-UTF-8 byte in a filename, `Path` stores the byte as a lone surrogate (`U+DC80`..`U+DCFF`) via PEP 383 `surrogateescape`. If that path is selected into `indexed_jobs` or `hash_jobs`, `out.write_text("".join(lines), encoding="utf-8")` (`raofflineproxy-ctl:1674`) raises `UnicodeEncodeError` (unlike `propose_cursor` at `:1587`, which passes `errors="surrogateescape"`), and `raofflineproxy-cache-indexed:149` has the matching strict `read_text(encoding="utf-8")`. This is a confirmed bug, but it is narrow in two ways: (1) it is a loud failure (`why LIBRARY_UNREADABLE`, exit 1), not a failure that reads as success; and (2) as `A-14` noted, an undecodable filename in a skipped directory, unsupported extension, already-cached path, or beyond `MAX_SCAN_ENTRIES` does not reach `lines` at `:1672-1673`.

#### R-15: Usage exit code split (F-18) and whole-line glob classification in `run_jobs` (F-24, A-15)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:316`, `raofflineproxy-ctl:944`, `raofflineproxy-ctl:1727-1767`, `raofflineproxy-ctl:1935-1938`, `raofflineproxy-ctl:2453`
- **Analysis:** F-18 is confirmed (though it is an exit-code inconsistency between `2` at `:2453` and `EX_USAGE=64` at `:944, :1935, :1938`, not a failure reading as success). F-24 (`:1736-1755`) is confirmed and, as Astra's `A-15` pointed out, actually has a "failure reads as skip" branch: because `*"No RetroAchievements match"*|*"Hash failed"*|*": not found"` (`:1745`) is tested across the entire `FAIL i/n <label>: <reason>` line **before** `*"login required"*|*"HTTP Error 401"*|*"HTTP Error 403"*` (`:1750`) and `FAIL\ *)` (`:1755`), any ROM whose filename contains `"Hash failed"` or `"No RetroAchievements match"` will have its real auth or network failures counted as `R_SKIPPED` and will reset `IN_A_ROW=0` (`:1749`). Conversely, a failing ROM whose filename contains `"Cache limit reached"` hits `:1736` (`R_LIMIT=1; R_STOPPED=1`), and one containing `"login required"` or `"HTTP Error 401"`/`"403"` (without matching `:1745`) hits `:1750` (`R_WHY=SIGN_IN_REFUSED`).

---

### 4. A bound that is not enforced (Q4; F-11 to F-15)

#### R-16: Verification of `02` § The bounds — enforced vs. soft/unenforced rows (F-09, F-12, F-13, A-16 to A-20)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:325-337`, `raofflineproxy-ctl:490-515`, `raofflineproxy-ctl:843-846`, `raofflineproxy-ctl:1135-1150`, `raofflineproxy-ctl:1849-1962`, `raofflineproxy-ctl:2220-2390`, `raofflineproxy-cache-indexed:71-95`, `raofflineproxy-cache-images:169-177`, `raofflineproxy-cache-images:308-309`, `013-validate-a-cached-image-before-publishing-it.patch` (`image_cache.py:252-280`, `:415-436`), `015-bounded-name-lookup.patch` (`network.py:270-332`), `raofflineproxy.service:23-24`, `:40-43`
- **Analysis:** Checking all 19 rows of `02` § The bounds against the code:
  1. **Enforced as stated:** `ERRORS_IN_A_ROW` (3, ctl `:332, :1760`, modulo F-24), `IMAGE_PASS_SECONDS` (300 s, ctl `:1849, :1876, :1915`, `cache-images:308-309, :417, :468-476`), batch cooldown (30 s per 50 jobs, `cache-indexed:71-79, :175`), unit start limit (`StartLimitIntervalSec=300`, `StartLimitBurst=5`, `--wait 30`, `RestartSec=5`, `raofflineproxy.service:23-24, :40-42`), and `TimeoutStopSec=15` (`:43`).
  2. **Overstated as hard bounds in `02` (confirming `A-16`, `A-18`, `A-19`):** `PROBE_TRIES`/`PROBE_INTERVAL` (ctl `:2248-2255`) does up to 9 probes and 8 sleeps of 10 s, but `is_online` (`:1135-1143`) has no `timeout` wrapper around `probe-online` (`network.py:23-24, :334-357`, up to 3 attempts × ~8 s each); `STOP_WAIT` (10 s, `:503-511`) bounds only the `flock` poll loop and neither `SIGKILL`s the job nor stops `do_disable`; `TOPUP_TIMEOUT` (900 s, `:1146-1150`) is a soft wall-clock calculation (`date +%s`, sensitive to NTP steps) and does not wrap `is_online`; `RAOFFLINEPROXY_IMAGE_WAIT` (120 s, `cache-indexed:82-95, :217`) bounds `waiter.join()`, but unlike `cache-images:476` (`os._exit`), `cache-indexed:218` exits normally and still waits for active non-daemon `ThreadPoolExecutor` threads; and `do_refresh` (`ctl:1957`, `refresh:158-228`) never shuts down `image_cache._image_download_executor` at all, so badge downloads queued by `refresh_game_patch` can hold `raofflineproxy-refresh` until the outer `timeout 960` kills it with rc `124` after `>>> done` was already printed.
  3. **Confirmed unenforced / flawed bounds:** `TOPUP_INTERVAL` and `-nt` played check with unguarded `touch "${TOPUP_MARK}"` (F-12, ctl `:2221-2238, :2264`), `scan.log` 1 MiB rotation bypassed by `2>>` appends (F-09, ctl `:843-846` vs. `:1711, :1713, :1876, :1987, :2301, :2366`), unbounded `response.read()` and `zlib.decompress(idat)` in patch 013 (F-13, `image_cache.py:252-276, :431`), and uncapped daemon threads in `resolve_host_bounded` plus unremembered synchronous `getaddrinfo` calls after `REMEMBER_SECONDS` or to `RA_MEDIA_HOST` in patch 015 (F-13, `network.py:270-332`, confirming `A-20`).

#### R-17: The scan's missing deadline — foreground design vs. `CloudText` staleness bound (F-11, A-19, A-54)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:1786`, `raofflineproxy-ctl:1985-1987`, `raofflineproxy-ctl:2026`, `raofflineproxy-ctl:2037`, `raofflineproxy-ctl:2062-2070`, `CloudText.cpp:1335-1343`
- **Analysis:** In `do_scan`, running `list_jobs` (`:1987`) and `run_jobs` (`:2037`) with `BUDGET=0` while bounding `run_image_pass` to `IMAGE_PASS_SECONDS` (`:2026, :2070`) is intentional design for a foreground page with an interactive `CANCEL` (`SIGINT`) trap (`:1967`, `:2062-2063`). However, as Astra's `A-54` identified, `CloudText::parseRunningProgress` (`CloudText.cpp:1335-1342`) assumes *"the ctl bounds its runs, so a line older than that bound was left by a run that died"* (`nowEpoch - run.at > RUNNING_STALE_AFTER_S`). Because `do_scan` has no bound on `list_jobs` (which writes `running` only once at `:1985`) and `run_jobs` deletes `running` at `:1786` (`unmark_running`) **before** `run_image_pass` (`:2070`, up to 300 s) even starts, the `running` file contract disagrees with `CloudText::parseRunningProgress` during long listings and during the scan's image pass.

#### R-18: `http_post` missing 429 rate-limit pause and request throttling (F-14, A-21)
- **Status:** narrowed
- **Evidence:** `network.py:367-421`, `network.py:516-567`, `001-dorequest-4xx-passthrough.patch` (`proxy_service.py:92-100`, `:542-550`)
- **Analysis:** In `network.py`, `http_get` (`:376-377`, `:408-420`) waits on `_request_throttle.wait(f"GET {action}")` and, on `HTTP_TOO_MANY_REQUESTS` (`429`), calls `rate_limit.on_rate_limited(retry_after_header_millis(error))` and retries with backoff. By contrast, `http_post` (`:516-567`) neither calls `_request_throttle.wait(...)` nor checks `error.code == HTTP_TOO_MANY_REQUESTS` in its `HTTPError` handler (`:549-567`), returning `(429, reason, body)` without recording a rate-limit pause. With patch 001 (`proxy_service.py:92-100, :542-550`), `is_passthrough_client_error` passes any `400 <= status < 500` except `{401, 403}` (including `429`) straight through to the client on `handle_online_request`; because `forward_to_upstream_result` and the flusher (`flusher.py`) are `outside the packet`, F-14 is narrowed to the functions shown in `network.py` and `patch 001` (confirming `A-21`).

---

### 5. Refute or confirm each finding F-01 to F-25 (and the six proposed bugs)

#### R-19: F-01 (Proposed Low bug — offline login serves cached token without credential verification)
- **Status:** confirmed
- **Evidence:** `proxy_service.py:452-474`, `proxy_service.py:491-507`, `auth.py:86-110`, `auth.py:142`
- **Analysis:** **Confirmed; Low severity is appropriate** given the loopback peer check (`proxy_service.py:290-292`) and single-user root OS model. A stream fix should require `handle_offline_login` to verify that `u` matches the currently configured account and that the request presents either a matching cached `t` (token) or a password `p` matching the configured password before returning `cached["responseBody"]`. On existing devices, `proxy.sqlite3` already holds `login2::<user>` rows (including rows for any previously signed-in accounts, which persist across account switches), and any token already returned over loopback cannot be recalled locally; the fix should also purge or refuse `login2::` rows for non-current accounts.

#### R-20: F-02 (Info — no `Host` or `Origin` validation on the proxy port)
- **Status:** narrowed
- **Evidence:** `proxy_service.py:290-292`, `011-offline-login-header.patch` (`proxy_service.py:172-188`)
- **Analysis:** Narrowed as in R-2 (and `A-2`/`A-23`): `_handle_request` enforces a loopback peer check (`127.0.0.1` / `::1`), and no CORS headers are sent, so a cross-origin page on the device could only read responses via DNS rebinding during a window where DNS rebinding works while upstream `retroachievements.org` is unreachable. Rejecting requests whose `Host` header is not `127.0.0.1:8080` / `localhost:8080` (or `proxy_value(config_data)`) and rejecting requests carrying an `Origin` header closes this cleanly.

#### R-21: F-03 (Proposed Low bug — `port_listening` accepts foreign `0.0.0.0:8080` listener)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:451-482`, `raofflineproxy-ctl:925-956`, `raofflineproxy.service:27-40`
- **Analysis:** **Narrowed (`setsettings.sh:536` is `outside the packet`); Low severity is appropriate.** As shown in R-6, because `raofflineproxy.service` is `Type=simple`, `ExecStartPost` (`raofflineproxy-ctl listening --wait 30`) runs immediately upon fork before Python imports finish and reaches `bind()`, so a pre-existing foreign `0.0.0.0:8080` listener satisfies `ExecStartPost` and lets `do_enable` complete and set `offlineproxy=1` and `hardcore=0` right before the service crashes with `EADDRINUSE`. A stream fix should drop `00000000:1F90` from `port_listening` (`:932`) and verify that the listening socket inode belongs to `raofflineproxy.service`'s `MainPID` (or check an HTTP response with `X-RA-Proxy: 1`). On existing devices where this race occurred, `system.cfg` could have been left with `offlineproxy=1`, `hardcore=0`, and the marker present while the service failed; `daemons/006-raofflineproxy` will retry starting the service on the next boot.

#### R-22: F-04 (Info — systemd unit runs as root with no hardening directives)
- **Status:** confirmed
- **Evidence:** `raofflineproxy.service:1-46`
- **Analysis:** Confirmed as Info (defense in depth), as detailed in R-7 and `A-25` (the T22 comparison table cited in `02` is `outside the packet`). Adding `UMask=0077`, `NoNewPrivileges=yes`, `PrivateTmp=yes`, `ProtectSystem=strict`, `ReadWritePaths=/storage/.config/raofflineproxy /storage/.config/retroarch /storage`, and `RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6` hardens the network- and ROM-parsing daemon without requiring a non-root user migration.

#### R-23: F-05 (Info — username passed on `python3` argv at four sites)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:616`, `raofflineproxy-ctl:647`, `raofflineproxy-ctl:764`, `raofflineproxy-ctl:1029`, `raofflineproxy-ctl:1244-1246`, `raofflineproxy-ctl:1265`
- **Analysis:** Narrowed as in R-5 and `A-5`/`A-26`: the comment at `:1244-1246` specifically describes `list_jobs`, which passes `RA_SCAN_USER` via the environment (`:1265`), while the four other sites pass the public username on `python3`'s argv. Passing `RA_USER` via environment at `:616`, `:647`, `:764`, and `:1029` makes all five sites uniform.

#### R-24: F-06 (Proposed Low bug — unopenable scan lock and ignored timeout in `do_disable`)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:490-515`, `raofflineproxy-ctl:525`
- **Analysis:** **Confirmed (and wider per R-8 / `A-8`); Low severity is appropriate.** Both `exec 7<>"${SCAN_LOCK}" || return 0` (`:492`) and `do_disable`'s unchecked call to `stop_running_run` (`:525`) allow `do_disable` to stop `raofflineproxy.service` underneath a running scan or top-up. A stream fix should check `stop_running_run` in `do_disable`, remove/recreate `${SCAN_LOCK}` if it is a directory, and `kill -KILL` the lock holder if `SIGTERM` does not stop it within `STOP_WAIT`. On existing devices, `/var/run/raofflineproxy-scan.lock` is on tmpfs (cleared on reboot), and any stale `running` file left behind is removed on the next `take_lock` (`:1204`).

#### R-25: F-07 (Proposed Low bug — `write_stamp` return status ignored by callers)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:1073-1095`, `raofflineproxy-ctl:1818`, `raofflineproxy-ctl:1990`, `raofflineproxy-ctl:2014`, `raofflineproxy-ctl:2031`, `raofflineproxy-ctl:2103`, `raofflineproxy-ctl:2411`, `raofflineproxy-ctl:2423`, `raofflineproxy-ctl:2427`
- **Analysis:** **Confirmed; Low severity is appropriate.** As detailed in R-9 and `A-9`/`A-28`, `write_stamp`'s exit code is ignored at all eight call sites, and `write_stamp` neither guards against `${SCAN_STAMP}` being a directory nor cleans up `${SCAN_STAMP}.tmp` on write failure. A stream fix should guard `[ ! -d "${SCAN_STAMP}" ]`, remove `${SCAN_STAMP}.tmp` on failure (and in the `EXIT` traps at `:1981, :2268`), and check `write_stamp` in `do_scan`/`do_topup` so a failed stamp write exits non-zero and logs the error. On existing devices where a write failed, `last-scan` holds an older run's stamp and `last-scan.tmp` may remain in `/storage/.config/raofflineproxy/` until cleaned up or overwritten.

#### R-26: F-08, F-09, F-10 (Info — writer hygiene in `list_jobs`, `verify-cursor`/`scan.log`, and `mkfifo`)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:1417`, `storage.py:73-167` (F-08); `raofflineproxy-cache-images:169-177`, `raofflineproxy-ctl:843-846`, `:1711-1713`, `:1876`, `:1987`, `:2301`, `:2366` (F-09); `raofflineproxy-ctl:1708-1709` (F-10)
- **Analysis:** All three are confirmed as Info (confirming `A-29`, `A-30`, `A-31`). For F-08, `list_jobs` opens `Storage()` read-write (`raofflineproxy-ctl:1417`), which sets `WAL` mode and runs DDL/migrations (`storage.py:86-167`) without closing the connection; `list_jobs` should query `DATABASE_FILE` via `sqlite3.connect("file:...?mode=ro", uri=True)` as `do_summary` and `ready_games_into` do. For F-09, `write_cursor` (`raofflineproxy-cache-images:173`) writes `verify-cursor` directly without temp+rename, and helper stderr (`2>>"${SCAN_LOG}"`) appends past 1 MiB until the next `slog` call rotates `scan.log`. For F-10, `mktemp -u` followed by `mkfifo` (`raofflineproxy-ctl:1708-1709`) fails closed via `|| fail` if the name collides, though creating the fifo inside a `mktemp -d` directory avoids any name race.

#### R-27: F-11, F-12, F-13, F-14, F-15 (Bounds and rate-limit findings; severity upgrades on F-12 and F-15)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:1987`, `:2037`, `:2062` (F-11); `raofflineproxy-ctl:2221-2238`, `:2264` (F-12); `013-validate-a-cached-image-before-publishing-it.patch` (`image_cache.py:252-276`, `:431`), `015-bounded-name-lookup.patch` (`network.py:270-332`) (F-13); `network.py:408-409`, `:549-563`, `001-dorequest-4xx-passthrough.patch` (F-14); `raofflineproxy-ctl:2372-2387` (F-15)
- **Analysis:**
  - **F-11 (confirmed Info, design, with R-17/`A-54` interaction):** Foreground `scan` intentionally has no overall timeout, though `CloudText::parseRunningProgress` (`CloudText.cpp:1335-1342`) assumes all runs are bounded.
  - **F-12 (confirmed; upgrade from Info to Low `bug`, confirming `A-33`):** `touch "${TOPUP_MARK}"` (`:2264`) is unguarded, and if `TOPUP_MARK` receives a future mtime (before NTP corrects a handheld's clock), `[ ! "${HIST}" -nt "${TOPUP_MARK}" ]` (`:2235`) and `[ "${INDEX_PENDING}" -nt "${TOPUP_MARK}" ]` (`:2221`) treat later play sessions and later `index-pending` files as older than the mark, silencing link-return top-ups until wall time passes the mark's future mtime. A fix should clamp/reset a future-dated `TOPUP_MARK` (`AGE < 0` at `:2225`) before the `-nt` comparisons so future-dated marks already left on devices heal automatically.
  - **F-13 (confirmed; availability defect in patches 013 and 015, confirming `A-34`):** `_fetch_image`/`_fetch_with_urllib` (`image_cache.py:252-276`) and `zlib.decompress(idat)` (`:431`) have no byte cap, and `resolve_host_bounded` (`network.py:299-332`) spawns uncapped daemon threads while leaving expired/unprobed hosts (`RA_MEDIA_HOST`) to block synchronously in `_resolver_getaddrinfo`.
  - **F-14 (narrowed Info, confirming `A-21`/`A-35`):** `http_post` (`network.py:549-567`) records no 429 pause and does not throttle requests; callers outside the excerpts (`flusher.py`, `forward_to_upstream_result`) are `outside the packet`.
  - **F-15 (confirmed; upgrade from Info to Low `bug`, confirming `A-36`):** An unreadable or missing `run-smart-cache` result line with exit `0` (`raofflineproxy-ctl:2372-2380`) silently reports `0 0 0` cached/skipped/limit instead of flagging an error.

#### R-28: F-16 (Proposed Low bug — `count_ready` prints `0` on failure) and F-17 (Proposed Low bug — non-UTF-8 ROM name fails listing)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:888-901` (F-16); `raofflineproxy-ctl:1672-1674`, `:1987-1991`, `:2301-2317`, `raofflineproxy-cache-indexed:149` (F-17)
- **Analysis:**
  - **F-16 (confirmed Low `bug`, wider per R-12/`A-12`/`A-37`):** `count_ready` prints `0` when `${READY_FILE}` is a directory or corrupt, or when `cached-games-count` fails behind `| tail -n 1`, and trusts any trailing digits printed before a failure. A stream fix should require `[ -f "${READY_FILE}" ]`, check `cached-games-count`'s exit status without a pipeline, and call `cannot_tell` in `do_ready` when the count cannot be read; on existing devices, any `last-scan` stamp that recorded `ready=0` during a read failure will be overwritten on the next scan or top-up.
  - **F-17 (confirmed Low `bug`, narrowed to selected paths per R-14/`A-14`/`A-38`):** One surrogate-escaped non-UTF-8 path in `lines` causes `out.write_text(..., encoding="utf-8")` (`raofflineproxy-ctl:1674`) to raise `UnicodeEncodeError` and abort the listing with `LIBRARY_UNREADABLE`. Using `errors="surrogateescape"` at `raofflineproxy-ctl:1674` and `raofflineproxy-cache-indexed:149` (and handling surrogates when formatting output lines) or skipping undecodable paths per-entry fixes the failure; on existing devices, `last-scan` with `why=LIBRARY_UNREADABLE` will clear on the next scan/top-up.

#### R-29: F-18 to F-25 (Protocol, packaging, harness, classifier, and file-mode findings)
- **Status:** narrowed
- **Evidence:** `raofflineproxy-ctl:316, :944, :1935, :1938, :2453` (F-18); `raofflineproxy-refresh:50-51, :153, :170, :223, :227` (F-19); `CloudText.cpp:1032-1033` (F-20); `package.mk:6` (F-21); `02` § The patches (F-22); `raofflineproxy-ctl:247-258` (F-23); `raofflineproxy-ctl:1736-1764` (F-24); `raofflineproxy.service:26-44` (F-25)
- **Analysis:**
  - **F-18 (confirmed Info):** Usage exits are split between `2` (`:2453`, `cache-indexed:144`) and `EX_USAGE=64` (`:944, :1935, :1938`); furthermore, `raofflineproxy-cache-images:278-279` exits `0` on `-h`/`--help` and `2` on bad flags via `argparse`.
  - **F-19 (narrowed Info, confirming `A-40`):** `raofflineproxy-refresh` writes unprefixed `note()` lines to stdout (`:50-51`) alongside `>>> ` protocol lines, and in `done {done}|{b}`, `b` is `left` (`len(wanted) - done - failed`) at `:170`, `len(wanted) - done` (which includes `failed`!) at `:223`, and `failed` at `:227` — three different meanings across the three exits. Whether any interface caller reads `refresh` is `outside the packet`.
  - **F-20 (narrowed Info, confirming `A-41`):** `CloudText::scanWhy` (`CloudText.cpp:1032-1033`) has a dead branch for `NO_GAMES_FOUND` while `raofflineproxy-ctl:2012, :2014` emits `note NO_GAMES`; `GuiRetroAchievementsSettings.cpp:154` is `outside the packet`.
  - **F-21, F-22, F-23 (narrowed Info, confirming `A-42` to `A-44`):** `package.mk:6` says `"The16 patches"` when 18 patches ship (`02`); the two sibling `package.mk` files, patches 020/021, `docs/upstream/raofflineproxy/`, and the `rc-preflight` / `last-good-scripts-test` scripts themselves are `outside the packet`.
  - **F-24 (confirmed Info/Low, wider per R-15/`A-15`/`A-45`):** Whole-line globbing in `run_jobs` (`:1736-1755`) lets ROM filenames trigger false `R_LIMIT`, false `SIGN_IN_REFUSED`, or false `R_SKIPPED` (masking real auth/network failures).
  - **F-25 (narrowed Info, per R-5/`A-46`):** Confirmed for the unit (`raofflineproxy.service`), the four scripts, and the files observed on the guest (`0644 root:root` under default `0022` umask).

---

### 6. What the first reader missed (including verification of Astra's new items and further defects)

#### R-30: `enable_undo` and `put_back` ignore failed rollback writes (A-47 / F-27)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:421-438`, `raofflineproxy-ctl:468-480`
- **Analysis:** Confirming Astra's `A-47`: in `enable_undo` (`raofflineproxy-ctl:430-438`), `put_back` (`:421-423`), `set_setting "${HARDCORE_WAS_KEY}" default` (`:434`), `do_stop` (`:435`), and `rm -f "${MARKER}"` (`:436`) are never read back or checked for success. That contradicts `03` § 3.3's claim that `do_enable` *"undoes every step on a failure"* and the comment at `:428-429` (*"A device on which enable failed is a device on which enable never ran"*).

#### R-31: `index-pending` lock-fallback `.tmp` race and unconditional deletion on failed restore in `ack_index_pending` (A-48 / F-28)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:2151-2182`
- **Analysis:** Confirming Astra's `A-48`: `write_index_pending` (`:2151-2158`) proceeds without the lock when `pending_lock` fails (`:2153`) and writes to a fixed shared path `${INDEX_PENDING}.tmp` (`:2154-2155`), so two concurrent writers can clobber or unlink each other's `.tmp`. Worse, in `ack_index_pending` (`:2172-2178`), when `${mine}` does not match `${1}` (a newer marker arrived), line 2176 attempts `[ -e "${INDEX_PENDING}" ] || mv -f "${mine}" "${INDEX_PENDING}" 2>/dev/null` and line 2177 **unconditionally** runs `rm -f "${mine}" 2>/dev/null` — so if `mv -f` at `:2176` fails, the only copy of the newer `index-pending` marker is permanently deleted!

#### R-32: Unescaped newlines or tabs in ROM paths break `list_jobs` / `raofflineproxy-cache-indexed` framing (A-49 / F-29)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:1672-1674`, `raofflineproxy-ctl:1707`, `raofflineproxy-cache-indexed:149-160`
- **Analysis:** Confirming Astra's `A-49` directly from the code: `list_jobs` (`raofflineproxy-ctl:1672-1673`) formats each job as `f"I\t{game_id}\t{hash}\t{p}\n"` or `f"H\t\t\t{p}\n"`, `run_jobs` (`:1707`) reads `${LIST}` with `mapfile -t PATHS < "${LIST}"`, and `raofflineproxy-cache-indexed:149` splits on `.splitlines()`. If a ROM filename on `/storage/roms` contains a newline character, `PATHS` in `run_jobs` desynchronizes from `TOTAL` and `raofflineproxy-cache-indexed` splits one path into two lines.

#### R-33: Patch 013 (`png_problem`) accepts IHDR-less PNGs and `_fetch_image` aborts retry loop on short read (A-50 / F-30, plus new)
- **Status:** confirmed
- **Evidence:** `013-validate-a-cached-image-before-publishing-it.patch` (`image_cache.py:209-215`, `:257-264`, `:415-436`)
- **Analysis:** Confirming Astra's `A-50`: `png_problem` (`image_cache.py:415-436`) checks only the 8-byte PNG signature, chunk CRCs up to `IEND`, and `zlib.decompress(idat)` (with no `max_length`), without verifying that an `IHDR` chunk is first (or present at all: a signature + `IDAT` containing `zlib.compress(b"")` + `IEND` passes `png_problem`). In addition, on the `+` side of patch 013 in `_fetch_image` (`image_cache.py:257-261`), when `_checked_image_body(response, body)` raises `ValueError` on a short read over a reused keep-alive connection, `_fetch_image` drops the connection and immediately `raise`s `ValueError` out of the retry loop instead of retrying on a fresh connection or falling back to `_fetch_with_urllib` as non-200 responses do at `:256`.

#### R-34: `ProxyRequestHandler._handle_request` negative/invalid `Content-Length`, non-UTF-8 body, and invalid `g=` param crashes (A-51 / F-31, plus new)
- **Status:** confirmed
- **Evidence:** `proxy_service.py:298-303`, `proxy_service.py:435-439`
- **Analysis:** Confirming Astra's `A-51` and extending it: in `_handle_request` (`proxy_service.py:298-303`), a negative `Content-Length` (e.g. `-1`) passes `content_length > MAX_REQUEST_BODY_BYTES` (`:299`), is truthy in `if content_length` (`:303`), and calls `self.rfile.read(-1)` (an unbounded read until EOF). In the same block, a non-numeric `Content-Length` header raises an uncaught `ValueError` at `int(...)` (`:298`), a non-UTF-8 request body raises an uncaught `UnicodeDecodeError` at `.decode("utf-8")` (`:303`), and in `process_proxy_request` (`:435-439`), an offline `unlocks` request with a non-integer `g=` parameter raises an uncaught `ValueError` at `int(game_id)` (`:439`).

#### R-35: Missing image helper returns `0`, `<60s` skips recently-played pass with no `why`, and un-unlinked damaged images count as cached (A-52 / F-32, A-53 / F-33)
- **Status:** confirmed
- **Evidence:** `raofflineproxy-ctl:1854`, `raofflineproxy-ctl:2362`, `raofflineproxy-ctl:2388-2390`, `raofflineproxy-cache-images:333-343`, `raofflineproxy-cache-images:452`
- **Analysis:** Confirming Astra's `A-52` and `A-53`: in `run_image_pass` (`raofflineproxy-ctl:1854`), if `${IMAGE_HELPER}` is not executable (`[ -x "${IMAGE_HELPER}" ]`), it logs to `scan.log` and returns `0` with `R_IMAGES_WHY=""` (reading as all images saved). In `do_topup` (`:2362, :2388-2390`), if `0 < LEFT < 60` seconds remain after the indexed pass, the recently-played pass (`run-smart-cache`) is skipped with no `WHY=TOOK_TOO_LONG` (unlike `:2280` and `:2321` when `LEFT <= 0` and `:1857` when `SECONDS_LEFT <= 10`). And in `raofflineproxy-cache-images:338-343`, if `--verify` detects a damaged image on disk (`why != "absent"`) and `target.unlink()` fails with `OSError`, the damaged file stays on disk so `resolve_cached_static_asset(p) is None` at `:452` is `False`, leaving `left` empty and exiting `0`.

#### R-36: `usage_report.py` still calls `storage.load_login_credentials()`, bypassing Patch 007's configured-account fix
- **Status:** new
- **Evidence:** `usage_report.py:185-195`, `007-cached-sign-in-of-the-configured-account.patch` (`auth.py:60-74`)
- **Analysis:** Patch 007 fixed `auth.resolve_credentials` so that when a device switches accounts, the proxy no longer takes `storage.load_login_credentials()` (the first `login2::` row in `api_cache`, regardless of which user is currently configured in `system.cfg`). However, `usage_report._report` (`usage_report.py:185`) was not updated by Patch 007 and still calls `credentials = storage.load_login_credentials()` directly, hashing `credentials["user"]` into `client_id` (`usage_report.py:47-50`, `:190`). On a device that previously signed in as another account, daily usage reports attribute activity to the old `login2::` row's user rather than the configured account.

#### R-37: Child processes inherit open `SCAN_LOCK` fd 9, and `cancelled`/`stopped` kill `${CLIENT}` without waiting
- **Status:** new
- **Evidence:** `raofflineproxy-ctl:1190`, `raofflineproxy-ctl:1711-1715`, `raofflineproxy-ctl:1781-1782`, `raofflineproxy-ctl:1795-1798`, `raofflineproxy-ctl:1811-1822`, `raofflineproxy-ctl:1876-1878`, `raofflineproxy-ctl:1910`, `raofflineproxy-ctl:1952`, `raofflineproxy-ctl:1981`, `raofflineproxy-ctl:2268`
- **Analysis:** `take_lock` (`raofflineproxy-ctl:1190`) opens `/var/run/raofflineproxy-scan.lock` on file descriptor `9` (`exec 9<>"${SCAN_LOCK}"`) without close-on-exec, so every background helper spawned afterwards (`python3 "${HELPER}"` at `:1711-1713`, `timeout ... "${IMAGE_HELPER}"` at `:1876, :1915`, `timeout ... "${REFRESH_HELPER}"` at `:1957`, `run-smart-cache` at `:2366`) inherits an open file descriptor to the `flock`-locked file description. When `cancelled` (`:1811-1822`) runs on `SIGINT`, `${CLIENT}` is still running and writing to `proxy.sqlite3` while `cancelled` computes `count_ready`, `ready_games_into`, and `write_stamp` (`:1813-1818`), because `kill "${CLIENT}"` only runs later in the `EXIT` trap (`:1981`). Furthermore, the `EXIT` traps (`:1910, :1952, :1981, :2268`) run `kill "${CLIENT}" 2>/dev/null` without `wait "${CLIENT}"`, so `raofflineproxy-ctl` exits while `${CLIENT}` (or its child processes) still holds inherited fd `9`, keeping `SCAN_LOCK` locked under a dead PID in `/var/run/raofflineproxy-scan.lock`.

#### R-38: `raofflineproxy-refresh` is $O(N^2)$ over the store in `row_ages` and never shuts down the badge download pool
- **Status:** new
- **Evidence:** `raofflineproxy-refresh:91-109`, `raofflineproxy-refresh:173-215`, `raofflineproxy-refresh:226-228`, `raofflineproxy-ctl:1957-1962`, `raofflineproxy-cache-indexed:82-95`
- **Analysis:** Inside the per-game refresh loop (`raofflineproxy-refresh:165-215`), line 214 calls `row_ages(storage, gid)`, which calls `storage.cache_summaries_by_prefix(prefix)` (`:94`) for the whole `"patch:"`, `"unlocks:"`, and `"startsession:"` tables and filters them in Python instead of querying `f"{prefix}{game_id}:"` as `drop_startsession` (`:73-75`) does, making `raofflineproxy-refresh --all` quadratic in the number of cached games. In addition, `refresh_game_patch` (`:173`) schedules background badge downloads on `image_cache._image_download_executor` (whose workers are non-daemon threads, per `raofflineproxy-cache-indexed:83-86`), but `raofflineproxy-refresh` never calls `wait_for_badges` or `shutdown_image_downloads()`. As a result, after `raofflineproxy-refresh` prints `>>> done {done}|{failed}` (`:227`) and returns `0` (`:228`), Python can block in interpreter exit waiting for badge downloads until `do_refresh`'s outer `timeout "$(( TOPUP_TIMEOUT + 60 ))"` (`raofflineproxy-ctl:1957`) kills it with exit code `124`.

#### R-39: `raofflineproxy-cache-indexed` falls through from malformed `I` jobs into `H` (ROM hashing)
- **Status:** new
- **Evidence:** `raofflineproxy-cache-indexed:152-160`, `raofflineproxy-cache-indexed:182-201`
- **Analysis:** In `raofflineproxy-cache-indexed:152-160`, any job line with `kind` in `("I", "H")` is appended to `jobs`, converting an empty `game_id` to `0` (`int(game_id) if game_id else 0`). At line 182, the indexed branch checks `if kind == "I" and game_id > 0 and hash_value:`; if an `I` job line has `game_id <= 0` or an empty `hash_value`, instead of failing or skipping that `I` job, execution falls through to lines `196-201` (`add_rom_to_cache`), hashing the ROM on disk even when `list_jobs` ran in `indexed` mode (`do_topup`, which is never supposed to hash ROMs, `raofflineproxy-ctl:1235-1236, :2276`).