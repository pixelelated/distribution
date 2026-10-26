### 1. Where a secret can travel (`02` § The secrets' paths; F-05, F-07, F-09, F-11, F-12)

#### R-1: Provider token and WebDAV/SFTP secret on process argv (`02` § The secrets' paths; F-05)
- **Verdict:** narrowed
- **Evidence:** `cloud_connections.py:131`, `cloud_connections.py:161-168`, `cloud_connections.py:180`, `cloud_oauth:588-591`, `cloud_remote:325-335`
- `02` § The secrets' paths and F-05 state that the provider token in `cloud_oauth:589` stays on `rclone config create`'s argv for both the 40 s `run()` bound and the subsequent `lsd` check (`cloud_connections.py:180`). In fact, `run(args)` at `cloud_connections.py:168` finishes and exits before `run(['--config', str(staged), 'lsd', ...])` at `:180` starts, and `lsd`'s argv contains only the staged config path and remote name, not `settings`. Conversely, for a WebDAV or SFTP secret passed via `cloud_remote create`/`update` (`cloud_remote:325-335`), `cloud_remote`'s own `/proc/<pid>/cmdline` holds the `key=value` arguments across the entire `connections.save()` transaction, including both `rclone config` and `rclone lsd`.

#### R-2: Conflation of WebDAV/SFTP secrets with phone-page keystrokes (`02` § The secrets' paths)
- **Verdict:** narrowed
- **Evidence:** `cloud_remote:36`, `cloud_remote:113-120`, `cloud_remote:325-335`, `cloud_oauth:2437-2458`, `cloud-signin-window.c:530-534`
- `02` § The secrets' paths groups the phone keyboard (`cloud_oauth:2455`) and `window.log` (`cloud-signin-window.c:533`) under "typed WebDAV/SFTP secret", but WebDAV and SFTP are `"keys"`-tier backends (`cloud_remote:118-119`) configured through `cloud_remote create`/`update`, never through `cloud_oauth`'s phone page. What the phone page (`cloud_oauth:2437-2458`) actually carries is the user's OAuth provider username, password, or 2FA code typed into `cloud-signin-window` during an `"oauth"`-tier sign-in. Those two credential kinds have distinct paths: WebDAV/SFTP secrets travel on `cloud_remote` and `rclone` argv into `rclone.conf` (obscured, `0600`), while OAuth passwords typed on the phone travel over plain HTTP on the LAN (`cloud_oauth:2406, 2446`) into `uinput` and `cloud-signin-window` (reaching `window.log` if `CLOUD_SIGNIN_DEBUG` is set in the environment at `cloud-signin-window.c:532`).

#### R-3: Unmasked `rclone` `ERROR` diagnostics on screen in `cloud_setup` (`02` § The secrets' paths; F-07)
- **Verdict:** refuted
- **Evidence:** `cloud_setup:495`, `cloud_setup:537`, `cloud_setup:543`, `cloud_connections.py:135`, `cloud_folder_validate:44`
- `02` § The secrets' paths (`cloud_setup:495` row) and F-07 claim that `rclone`'s `ERROR` output shown on the setup screen "carries the remote's URL, not its secret". In fact, `cloud_setup:495` captures the first two lines of `rclone lsd "${remote}${path}" ... --log-level ERROR 2>&1 >/dev/null` and `cloud_setup:537, 543` echoes `${probe}` raw with no scrubbing or `redact_credentials` filter. As `cloud_connections.py:135` and `cloud_folder_validate:44` explicitly warn, provider error diagnostics from `rclone` can contain credentials, SAS/query tokens, or userinfo embedded in endpoint URLs, so `cloud_setup:537, 543` is an unmasked diagnostic sink as well as a player-language violation.

#### R-4: OAuth code and PIN sinks (`02` § The secrets' paths)
- **Verdict:** narrowed
- **Evidence:** `cloud_oauth:187-193`, `cloud_oauth:516-520`, `cloud_oauth:1133`, `cloud_oauth:2490`, `cloud_oauth:2587-2598`, `cloud_oauth:2639-2641`, `cloud-signin-window.c:660-668`
- For the OAuth redirect code, `cloud-signin-window.c:660-668` excludes `127.0.0.1` and `localhost` redirects from the `page` file (lines 669-671 are `outside the packet`), and in the paste flow the code crosses the LAN via plain HTTP POST (`cloud_oauth:2490`) and loopback GET to `127.0.0.1:53682` (`cloud_oauth:516`). However, if `urlopen` at `cloud_oauth:516` raises an `OSError` whose message includes the URL, `:520` returns `"could not hand the code back to rclone: %s" % exc` to `:2490`, and if the user pastes the code into the phone's keyboard box (`:2446`) instead of the code box, it travels the keystroke path. For the PIN, all sinks in `02` (`session.json` `0644` at `:193, 2597`, stdout at `:2639-2641`, QR/URL at `:2587`, and the phone page JS `var pin = "%(pin)s";` at `:1133`) are confirmed; whether `BaseHTTPRequestHandler.log_message` is overridden to suppress request-path logging to stderr is in lines 2215-2321 (`outside the packet`).

#### R-5: Device ID sinks and `machine-id` fallback (`02` § The secrets' paths; F-11)
- **Verdict:** narrowed
- **Evidence:** `cloud_device_id:29-36`, `cloud_device_id:133-168`, `cloud_device_id:290`, `cloud_device_id:301`, `cloud_scan:332-344`, `backuptool:1891`
- Beyond `/storage/.config/cloud_sync-device-id` (`0644`, `cloud_device_id:290`) and `.previous` (`0644`, `:301`), the device ID also lands in `/storage/.cache/cloud_sync/scan/settings` and `scan/archives` (`0644`, `cloud_scan:332-344`) and in settings archive filenames (`backuptool:1891`). In `cloud_device_id:143-145`, `hash_of()` truncates `md5(<seed>|unknown)` to 10 hex characters (40 bits), so a 48-bit MAC seed (`:165-166`) is searchable within a 24-bit vendor OUI (~$2^{24}$ candidates) and has ~$2^8$ collisions across the full 48-bit MAC space. However, when no adapter has a valid permanent MAC (`:167-168`, comment at `:33-36`, body `outside the packet`), the seed falls back to `/etc/machine-id` (128 bits), which is not recoverable by brute force.

#### R-6: Scrubber pattern families and `cloud_oauth` / `cloud_log_scrub` drift (`02` § The secrets' paths)
- **Verdict:** narrowed
- **Evidence:** `cloud_log_scrub:78-121`, `cloud_log_scrub:190-196`, `cloud_remote:95-96`, `cloud_oauth:448`, `cloud_oauth:594`, `cloud_connections.py:50-192`
- No writer in the 14 files today writes credentials in the three shapes `cloud_log_scrub` was built to remove: `cloud_remote:95-96` logs only the verb and exit code (F1), `cloud_oauth:448` logs only `Refused` sentences or fixed strings from `_write_config()` (`:594`) / `CLOSED_EARLY` (`:601`) (F2), and ES masks `cloud_remote create:` output at `GuiMenu.cpp:7414` (F3). However, `cloud_log_scrub:94`'s F2 allowlist only lists six older sentences (`a remote called .* already exists`, `signed in, but the remote did not respond`, `rclone rejected the token`, etc.) and does not include the new `connections.Refused` sentences (`cloud_connections.py:50-192`) or `"Your cloud settings could not be saved."` (`cloud_oauth:594`). Consequently, `cloud_oauth:448` still writes lines that match `cloud_log_scrub:93-95`'s redaction rule: if `cloud_log_scrub` runs after such a failure, it redacts the benign `Refused` sentence to `<redacted>` and falsely reports in boot output (`cloud_log_scrub:193`) that a credential leak was found and masked.

---

### 2. What the deleting path can delete (`02` § The deletions; F-02)

#### R-7: Reachability and order of operations before the two deleting statements (`02` § The deletions)
- **Verdict:** narrowed
- **Evidence:** `cloud_content_restore:873-981`, `cloud_content_restore:1012-1020`, `cloud_content_restore:1033-1052`
- Both deleting statements (`rclone delete` at `:1015` and `bounded_content_rclone sync` at `:1046`) are inside `match_run()` under `if [ "${apply}" = "1" ]; then` (`:1012`, `:1033`) and are reachable only after acquiring the transfer lock (`:874`), spending `MATCH_PLAN` (`:890-896`), verifying `content_context_current`, `plan_context`, `plan_mode`, and non-empty `MATCH_PLAN_TEXT` (`:898-909`), confirming `cloud_root_populated` (`:914`), and verifying for each system that its current dry-run verb matches `pverb` and `files <= pfiles` (`:970-980`). However, `02`'s statement that "The apply spends the plan before it reads anything (`:885-897`)" is slightly inaccurate: `:886-889` reads `plan_context`, `plan_mode`, and `MATCH_PLAN_TEXT` into memory first and then unlinks `MATCH_PLAN` at `:890` before checking context or contacting the cloud. In addition, the verb and count check at `:970-980` is evaluated per system inside the loop (`:947`), so if a later system fails the drift check and `continue`s (`:978`), earlier systems in the same `--match --apply` run have already been deleted or synced.

#### R-8: `RCLONE_NET_OPTS` injection into `--match` dry-run and deleting `sync` (F-02)
- **Verdict:** confirmed
- **Evidence:** `cloud_content_restore:235-238`, `cloud_content_restore:276-279`, `cloud_content_restore:750-752`, `cloud_content_restore:1046-1050`, `stage-b/fixture-content.txt`
- F-02 is confirmed by the code and `stage-b/fixture-content.txt`: `RCLONE_NET_OPTS` is read by `conf_get` (`:235`), split into `RCLONE_NET_OPTS_ARRAY` without filtering (`:277-279`), and expanded into both the preview's dry-run `sync` (`:750`) and the apply's deleting `sync` (`:1046`). Crucially, because `:750` also receives `RCLONE_NET_OPTS_ARRAY`, `--delete-excluded` causes the preview dry-run itself to count the excluded save files into `pfiles` (`snes|sync|2|48`), so the apply hands that inflated count to `--max-delete "${files}"` (`:1048`) along with `--delete-excluded`, defeating `--max-delete` and deleting the local saves.

#### R-9: Other dangerous flags `RCLONE_NET_OPTS` can carry to `rclone`
- **Verdict:** new
- **Evidence:** `cloud_content_restore:276-279`, `cloud_content_restore:750-752`, `cloud_content_restore:1046-1050`, `cloud_content_backup:230-232`
- Beyond `--delete-excluded`, `RCLONE_NET_OPTS_ARRAY` is expanded at `cloud_content_restore:750, 1046` **before** `"${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}"`. Because `rclone` evaluates filter flags in command-line order (first match wins), a flag such as `--include *` or `--filter "+ *"` in `RCLONE_NET_OPTS` precedes and overrides all subsequent `--exclude` arguments in `SAVE_EXCLUDES`, causing save files to be treated as ordinary sync targets and deleted on `--match --apply` even without `--delete-excluded`. `RCLONE_NET_OPTS` can likewise carry `--config <path>`, `--backup-dir <path>`, `--log-file <path>`, or `--files-from` into every networked `rclone` call in both `cloud_content_restore` and `cloud_content_backup:230-232`.

#### R-10: `bounded_content_rclone` verb and flag handling (`cloud_content_transfer:85-158`)
- **Verdict:** narrowed
- **Evidence:** `cloud_content_transfer:85-96`, `cloud_content_transfer:124`, `cloud_content_restore:750`, `cloud_content_restore:1046`
- `bounded_content_rclone` (`cloud_content_transfer:85-158`) copies `"$@"` into `args=("$@")` (`:88`), appends `--progress` if absent (`:90-93`), and executes `command rclone "${args[@]}" > "${dir}/fifo" &` (`:124`) with no validation of the verb or flags. At the call sites visible in the packet (`cloud_content_restore:750, 1046`; other call sites in `cloud_content_restore` and `cloud_content_backup` are `outside the packet`), the first argument is a literal verb (`sync` or `copy`), so a caller cannot inject a different verb, but any flags in `RCLONE_NET_OPTS_ARRAY` are passed straight through to `rclone`.

#### R-11: `rm -rf` sites and `pkill -f` pattern reach (`02` § The deletions)
- **Verdict:** refuted
- **Evidence:** `cloud_content_restore:1271`, `cloud_setup:775-776`, `cloud_oauth:357`, `cloud_oauth:861-863`, `cloud_oauth:2819`, `cloud_connections.py:41`, `cloud_connections.py:161`, `cloud_connections.py:242`, `cloud_remote:102`, `cloud_setup:553`, `cloud_setup:651`
- While 11 of the 12 `rm -rf` sites are properly bounded to non-empty staging/temp paths (`backuptool:224` sweeps `${STAGING_PREFIX}*` under the lock, `:227` checks `[ -n "${STAGING:-}" ]`, and `cloud_content_transfer:110` checks `[ -z "${dir}" ]`), `cloud_content_restore:1271` runs `TMP=$(mktemp -d /tmp/cloud-scan.XXXXXX); trap 'rm -rf "${TMP}"' EXIT` without checking if `mktemp -d` succeeded. More importantly, `cloud_setup:775` runs `pkill -f "rclone config"` without a lock or anchor: that substring matches `cloud_remote`'s `rclone config providers` (`cloud_remote:102`), `cloud_setup`'s own `rclone config file` (`:553`) and `rclone config show` (`:651`), and any test harness or process whose argv contains `"rclone config"` (the exact self/harness-kill hazard `cloud_oauth:861-863` notes for `pkill -f`). Similarly, `pkill -f "rclone authorize"` (`cloud_setup:776`, `cloud_oauth:357`, `:2819`) is unanchored and matches any command line containing that substring.

---

### 3. The phone page (F-01, F-09)

#### R-12: Browser icon requests exhausting the 10 PIN attempts (F-01)
- **Verdict:** confirmed
- **Evidence:** `cloud_oauth:2196-2206`, `cloud_oauth:2322-2348`, `stage-b/fixture-pin.txt`
- F-01 is confirmed by `cloud_oauth:2322-2348` and `stage-b/fixture-pin.txt`: `_supplied()` (`:2330-2344`) returns `?pin=` if present, and otherwise returns `parsed.path.strip("/").split("/")[0]`. An unauthenticated browser request for `/favicon.ico` or `/apple-touch-icon.png` therefore supplies `"favicon.ico"` or `"apple-touch-icon.png"` as a candidate PIN, causing `_gate()` (`:2322`) to call `holder.pin_failed()` (`:2200-2203`), which increments `self.pin_attempts` (returning HTTP 200 with the PIN error page on attempts 1–9 and HTTP 403 on attempt 10+) and locks out the legitimate PIN once `self.pin_attempts >= 10`.

#### R-13: Bounds on guessing the four-digit PIN (`02` § The phone flow)
- **Verdict:** confirmed
- **Evidence:** `cloud_oauth:2062`, `cloud_oauth:2065-2066`, `cloud_oauth:2196-2206`, `cloud_oauth:2405-2409`, `cloud_oauth:2648-2649`
- The PIN is a 4-digit string drawn uniformly via `secrets.randbelow(10000)` (`cloud_oauth:2062`) and checked with `secrets.compare_digest(str(pin), self.pin)` (`:2206`). Guessing is bounded by `self.pin_attempts >= 10` under `self.lock` (`:2065-2066, 2196-2203`), giving a random guess at most a 10 in 10,000 (0.1%) chance per `serve` before all requests return 403 (`:2322-2324`), alongside the 600 s serve timer (`:2648-2649`; `lan_address()`, `MAX_CONNECTIONS = 16`, `REQUEST_TIMEOUT = 15`, and `MAX_BODY = 64 KiB` at `:268-281`, `:2220-2244`, `:2395-2404`, and `:2549-2561` are `outside the packet`). Note that because `secrets.compare_digest` raises `TypeError` on non-ASCII strings before `pin_failed()` is reached (`:2206, 2322`), non-ASCII guesses crash the handler thread without incrementing `pin_attempts` (`stage-b/fixture-pin.txt`).

#### R-14: What the phone listener serves to unauthenticated requests (`02` § The phone flow)
- **Verdict:** narrowed
- **Evidence:** `cloud_oauth:2322-2348`, `cloud_oauth:2405-2410`, `stage-b/fixture-pin.txt`
- An unauthenticated `GET /` (empty `_supplied()`) serves the HTML PIN prompt page (HTTP 200) without incrementing `pin_attempts` (lines 2308-2321 are `outside the packet`), while an unauthenticated `GET /<anything>` or `POST` with a wrong non-empty PIN on attempts 1–9 increments `pin_attempts` and serves HTTP 200 with `<div class=err>That PIN did not match.</div>` (`:2326-2327`), and on attempt 10+ serves HTTP 403 (`:2323-2324`). On `do_POST` (`:2405-2408`), up to 64 KiB of request body is read and URL-decoded with `urllib.parse.parse_qs` **before** `_gate()` is called at `:2408`, because the PIN may be supplied in the POST form body.

#### R-15: Reachability of the paste flow's raw-HTML render with attacker-chosen text (F-09)
- **Verdict:** narrowed
- **Evidence:** `cloud_oauth:508-524`, `cloud_oauth:2408`, `cloud_oauth:2482`, `cloud_oauth:2490`
- In `do_POST`, `self._render('<div class=err>%s</div>%s' % (error, again))` (`:2482`) and `session.submit(fields.get("code", [""])[0])` (`:2490`) sit behind `_gate()` (`:2408`), so an external party without the 4-digit PIN cannot reach them directly. However, contrary to `02` F-09's claim that this path is "only reachable where the device has no browser stack", `do_POST` at `:2490` accepts a `code` POST on **any** active `serve` once authenticated with the PIN, even when the device has a browser stack. When `session.submit()` (`:516`) forwards the pasted query string to `http://127.0.0.1:53682/?<query>`, if a crafted redirect URL (e.g., an `error_description` parameter) or `OSError` (`:520`) causes `detail` / `failure_reason()` (lines 480-488 and 2271-2290 are `outside the packet`) to contain unescaped HTML, `_render` inserts it raw into the HTML response.

---

### 4. What the content backup takes (F-03)

#### R-16: Path traversal in `cloud_content_backup` positional arguments and unchecked `RCLONE_NET_OPTS` (F-03)
- **Verdict:** narrowed
- **Evidence:** `cloud_content_backup:230-232`, `cloud_content_backup:583-585`, `cloud_content_restore:1482-1487`, `stage-b/fixture-content.txt`
- `cloud_content_backup:583-585` sets `DIRS=("$@")` without running the `^[A-Za-z0-9_][A-Za-z0-9._-]*$` validation that `cloud_content_restore:1482-1487` enforces. As shown by `stage-b/fixture-content.txt` (lines 710 and 753 of `cloud_content_backup` are `outside the packet`), passing `'../.config'` copies from `/storage/roms/../.config` (i.e., `/storage/.config`, which contains `rclone/rclone.conf` and `system/configs/system.cfg`) to `<REMOTE><CONTENT_REMOTE>/ROMs/../.config`, which normalizes on the remote to `<REMOTE><CONTENT_REMOTE>/.config`. In addition, `02` § 4 / F-03 missed that `cloud_content_backup:230-232` also splits `RCLONE_NET_OPTS` from `cloud_sync.conf` into `RCLONE_NET_OPTS_ARRAY` without filtering, allowing arbitrary `rclone` flags (such as `--include *` to override save/metadata exclusions, or `--config`) to be injected into backup runs.

---

### 5. The writers (`02` § The writers, 31 rows; F-06, F-08, F-10)

#### R-17: Audit of the 31 writer rows — modes, locks, atomicity, and missing rows (`02` § The writers)
- **Verdict:** narrowed
- **Evidence:** `cloud_connections.py:159-160`, `cloud_connections.py:212`, `cloud_oauth:2134`, `cloud_oauth:2708`, `cloud_oauth:2715`, `cloud_oauth:2754`, `cloud_scan:276-350`, `cloud_log_scrub:182-186`
- Several rows in `02` § The writers need correction:
  1. `cloud_oauth:2708` (`open(marker, "w").close()` for the `--phone` marker) is missing from the OAuth markers row (`:2134, :2715, :2754`), and `cloud_scan:276` also writes `2> "${OUT}/scan.err"`.
  2. The scan results rows (`cloud_scan:276-350`) are labeled `0644 observed`, but `stage-b/fixture-mode.txt` only ran a synthetic `> file` redirection in bash rather than `cloud_scan`, so those modes are *by construction*.
  3. `cloud_connections.py:212` (`CONFIG.unlink()` on rollback of a first save) does not `fsync` `CONFIG.parent` afterwards (unlike `restore_selection` at `:98-103`), and `staged.write_bytes(original)` (`:159, :240`) writes with the process umask before `staged.chmod(0o600)` (`:160, :241`) inside the `0700` `TemporaryDirectory`.
  4. In `cloud_log_scrub:182-186`, `{ grep -v "^$1=" "${STAMP}" 2>/dev/null; printf ...; } > "${STAMP}.tmp"` judges the compound block only by `printf`'s exit status and uses a fixed `.tmp` suffix rather than `.$$`.

#### R-18: Whether `cloud_connections.atomic()` is the only writer of `rclone.conf` (`03` § 3.1; F-15)
- **Verdict:** refuted
- **Evidence:** `cloud_connections.py:72-89`, `cloud_connections.py:161-168`, `cloud_connections.py:198`, `cloud_connections.py:210`, `cloud_connections.py:218-225`, `cloud_connections.py:253`, `cloud_connections.py:256`, `cloud_remote:329-335`
- In normal operation, `cloud_connections.atomic()` (`:72-89`, called at `:198, :210, :253, :256`) is the only writer of `/storage/.config/rclone/rclone.conf` (after `rclone` writes to the private `staged` copy at `:168, :242`). However, because `cloud_connections.save()` (`:161-165`) appends `'%s=%s' % pair for pair in settings` to `rclone`'s argv without validating that `key` does not start with `-` (and without `--`), passing `--config=/storage/.config/rclone/rclone.conf` (or any `<path>`) in `settings` causes `rclone` at `:168` to override `--config <staged>` and write directly to `<path>`, bypassing `staged`, `lsd` verification, and `atomic()`. Separately, `03` § 3.1 states that every path to `cloud_connections.py` goes through `save` or `remove`, overlooking `select(name)` (`:218-225`), which is a third locked entry point writing `active-connection`.

#### R-19: What a kill at each step leaves (F-06, F-10)
- **Verdict:** narrowed
- **Evidence:** `cloud_connections.py:74`, `cloud_connections.py:157`, `cloud_connections.py:195-214`, `cloud_connections.py:238`, `cloud_connections.py:251-258`, `cloud_oauth:580-583`, `cloud_content_restore:1405-1406`
- Beyond leaving `.connection-*` (`0700`) and `.rclone.conf-*` / `.active-connection-*` (`0600`) in `/storage/.config/rclone/` on a `SIGKILL` (F-06), there are two intermediate kill states in `cloud_connections.py`:
  1. In `remove()` (`:252-253`), `atomic(ACTIVE, written_selection)` writes the empty tombstone `b'\n'` before `atomic(CONFIG, updated)` deletes the section; a `SIGKILL` between `:252` and `:253` leaves `active-connection` tombstoned while the removed remote's credentials remain in `rclone.conf`.
  2. In `save()` with `cloud_oauth`'s `publish` callback (`cloud_oauth:580-583`, `cloud_connections.py:201-214`), `commit()` installs `rclone.conf` at `:581` before `_write_whole(state)` updates `session.json` at `:583`; a `SIGKILL` between `:581` and `:583` bypasses the Python `except Exception:` rollback at `:205-214`, leaving `rclone.conf` updated while `session.json` still reads `waiting`.
  3. In `cloud_content_restore:1405-1406` (`--set-systems`), because line 1405 (`{ ... || printf ...; } > "${SELECTION}.tmp.$$"`) and line 1406 (`mv -f "${SELECTION}.tmp.$$" "${SELECTION}"`) are not joined with `&&`, a write that fails partway on line 1405 (e.g., `ENOSPC`) is still renamed over `${SELECTION}` on line 1406, installing a truncated system selection.

#### R-20: Soundness of `backuptool`'s archive write and restore mark-and-revert (`03` § 3.1; F-10)
- **Verdict:** narrowed
- **Evidence:** `backuptool:649-661`, `backuptool:1175-1186`, `backuptool:1271-1347`, `backuptool:1608-1620`, `backuptool:1821-1823`, `backuptool:1885`
- The archive creation in `backuptool:1175-1347` and pre-restore snapshot in `:649-661` verify pipeline status (`set -o pipefail` at `:1177`), staged file counts (`:1287`), credential scan (`:1301-1310`), and `.partial` member counts via `listed_files` (`:654, :1334`) before renaming, and `:1608-1620` atomically writes `RESTORE_MARK` with `mv -fT` and verifies its first line, last line, and line count. Three qualifications apply: first, `:655` and `:1342` use `mv -f "${TARGET}.partial" "${TARGET}"` without `-T` or a post-move `[ -f "${TARGET}" ]` check (unlike `:1611` and `:1822-1823`); second, `:1287` uses `if [ "${STAGED}" -ne $((SENT + SANITISED)) ]` without `2>/dev/null`, which in bash fails open if `STAGED` is empty/non-numeric (`[` exits 2, skipping the `then` refusal branch); third, the extraction and revert execution itself (lines 1629-1813) is `outside the packet`.

---

### 6. Findings F-01 to F-19 (`02` § Findings)

#### R-21: F-01 — Phone icon requests spend the 10 PIN attempts
- **Verdict:** confirmed
- **Evidence:** `cloud_oauth:2196-2206`, `cloud_oauth:2322-2348`, `cloud_oauth:2408`, `stage-b/fixture-pin.txt`
- **Confirmation & Severity:** Confirmed by `cloud_oauth:2322-2348` and `stage-b/fixture-pin.txt`; **Low** severity is appropriate because the lockout affects only the optional phone helper for the current `serve` session and leaves the handheld's own sign-in intact.
- **Proposed fix & `Already written:`:** The proposed fix (returning 404 for icon/non-PIN paths before `_gate` and only counting 4-digit ASCII PIN candidates on both GET and POST) is sound and, if checked before `secrets.compare_digest` (`:2206`), also fixes F-09's non-ASCII `TypeError`. The `Already written:` assessment is exact: `self.pin_attempts` (`:2065`) is in-memory only and leaves nothing on disk or in the cloud.

#### R-22: F-02 — `RCLONE_NET_OPTS` reaches `--match --apply`'s deleting `sync` unfiltered
- **Verdict:** confirmed
- **Evidence:** `cloud_content_restore:235-238`, `cloud_content_restore:276-279`, `cloud_content_restore:750`, `cloud_content_restore:1046`, `cloud_content_backup:230-232`, `stage-b/fixture-content.txt`
- **Confirmation & Severity:** Confirmed by code and real-`rclone` fixture (`stage-b/fixture-content.txt`); however, severity should be **Medium** rather than Low, because `--match --apply` is the only destructive content path (with no `--backup-dir`, D-CLOUD-023) and a fail-open flag injection (`--delete-excluded`, or `--include *` / `--filter "+ *"` before `"${SAVE_EXCLUDES[@]}"`) causes unrecoverable local save deletion while bypassing `--max-delete` via `:750`.
- **Proposed fix & `Already written:`:** Allowlisting only the four timeout/retry options (`--contimeout`, `--timeout`, `--low-level-retries`, `--retries`) with validated values across `cloud_content_restore:276-279` and `cloud_content_backup:230-232` (and routing the same to T16) is the right fix. For `Already written:`, any saves deleted by a past apply with `--delete-excluded` are already gone locally, and if a device holds an unspent `content-match-plan` (`:812`) generated while a bad `RCLONE_NET_OPTS` was set, stripping/refusing the bad option before `:1046` prevents save deletion on apply, though invalidating `plan2` or including the effective net-opts in `CONTENT_CONFIG_ID` is even cleaner.

#### R-23: F-03 — `cloud_content_backup` accepts unchecked system names (`../.config`)
- **Verdict:** confirmed
- **Evidence:** `cloud_content_backup:583-585`, `cloud_content_restore:1482-1487`, `stage-b/fixture-content.txt`
- **Confirmation & Severity:** Confirmed by `cloud_content_backup:583-585` and `stage-b/fixture-content.txt`; severity should be **Medium** rather than Low under a security lens, because path traversal (`cloud_content_backup '../.config'`) uploads `/storage/.config` (including `rclone/rclone.conf` with plaintext OAuth tokens) to `<REMOTE><CONTENT_REMOTE>/.config` in the cloud.
- **Proposed fix & `Already written:`:** Enforcing `cloud_content_restore:1482-1487`'s `^[A-Za-z0-9_][A-Za-z0-9._-]*$` check on `DIRS` in `cloud_content_backup` before acquiring the lock is sound. The `Already written:` note is accurate: nothing is modified on the device, and any prior traversal upload would reside in the user's cloud at `<CONTENT_REMOTE>/.config`.

#### R-24: F-04 — Symlink member in a settings archive accepted by `foreign_member()` and stopped by busybox `tar`
- **Verdict:** narrowed
- **Evidence:** `backuptool:551-558`, `backuptool:1324`, `backuptool:1608-1620`, `stage-b/fixture-archive.txt`
- `foreign_member()` (`backuptool:551-558`) inspects only member names from `tar -tzf`, not member types (`l` or `h`), and `stage-b/fixture-archive.txt` proves that busybox `tar` refuses a symlink followed by a child file through that symlink (`storage/.config/escape` then `storage/.config/escape/note.txt`). However, the fixture only tests a symlink followed by a child file (which turns `storage/.config/escape` into a directory before deferred symlink creation runs), not a standalone symlink member with no child path in the archive or a hardlink member; and the full `backuptool restore` extraction/revert path (lines 1629-1813) is `outside the packet`.

#### R-25: F-05 — Secrets on process argv and `session.json` mode `0644`
- **Verdict:** narrowed
- **Evidence:** `cloud_connections.py:131`, `cloud_connections.py:161-168`, `cloud_connections.py:180`, `cloud_oauth:187-193`, `cloud_remote:325-335`, `stage-b/fixture-mode.txt`
- `session.json` being `0644` in `0755` `/var/run/cloud_oauth` (`cloud_oauth:187-193`, `stage-b/fixture-mode.txt`) and secrets appearing on process argv are confirmed. As noted in R-1, `rclone`'s argv holds the secret only during `rclone config create`/`update` (`cloud_connections.py:168`, up to 40 s), not during `rclone lsd` (`:180`), whereas `cloud_remote`'s argv (`cloud_remote:325-335`) holds typed WebDAV/SFTP secrets across both steps.

#### R-26: F-06 — Kill mid-save leaves staged credentials in `/storage/.config/rclone/`
- **Verdict:** confirmed
- **Evidence:** `cloud_connections.py:74`, `cloud_connections.py:157`, `cloud_connections.py:238`, `backuptool:1036-1046`
- `save()` (`:157`) and `remove()` (`:238`) create `.connection-*` directories (`0700`) with `rclone.conf` (`0600`), and `atomic()` (`:74`) creates `.rclone.conf-*` / `.active-connection-*` (`0600`) in `/storage/.config/rclone/`. A `SIGKILL` or power loss leaves those files behind until swept, though `backuptool` excludes `/storage/.config/rclone` from settings archives.

#### R-27: F-07 — Diagnostic words and root password reaching a screen or stderr
- **Verdict:** narrowed
- **Evidence:** `cloud_setup:224`, `cloud_setup:495`, `cloud_setup:537`, `cloud_setup:543`, `cloud_setup:926-937`, `cloud_remote:331`
- All four items in F-07 (`cloud_setup:495, 537, 543` echoing `rclone` `ERROR` lines; `cloud_setup:926, 937` printing `root.password` in the legacy SSH flow; `cloud_remote:331` echoing a malformed `pair` without `=` to stderr; and `cloud_setup:224, 928` logging `SSH_CMD` from `/storage/.config/cloud_setup_ssh`) are confirmed at their cited lines. As detailed in R-3, F-07 is narrowed because `cloud_setup:495, 537, 543` does not strip credentials or secret-bearing URLs from `rclone`'s `ERROR` text before printing it.

#### R-28: F-08 — Match plan age, `/tmp` `.$$` fallbacks, and `exists_remote` regex
- **Verdict:** narrowed
- **Evidence:** `cloud_content_restore:837-838`, `cloud_content_restore:886-980`, `cloud_content_restore:1418`
- The lack of a TTL on `plan2`'s timestamp (`:886-903`, bounded by context hash, mode, verbs, and counts at `:970-980`) and the predictable `/tmp/cloud-match-log.$$` and `/tmp/cloud-match-before.$$` fallbacks when `mktemp` fails (`:837-838`) are confirmed. The body of `exists_remote` at `:441` is `outside the packet`; its visible caller at `:1418` passes `"${ROOT}BIOS"`, which contains no regex metacharacters.

#### R-29: F-09 — Non-ASCII PIN `TypeError` and raw-HTML paste error rendering
- **Verdict:** narrowed
- **Evidence:** `cloud_oauth:508-524`, `cloud_oauth:2206`, `cloud_oauth:2406-2408`, `cloud_oauth:2482`, `cloud_oauth:2490`, `stage-b/fixture-pin.txt`
- The `TypeError` in `secrets.compare_digest(str(pin), self.pin)` (`:2206`) on a URL-decoded non-ASCII PIN is confirmed by code and `stage-b/fixture-pin.txt`. For the raw HTML interpolation in `_render` (`:2482, :2490`), the definitions of `failure_reason()` (`:480-488`) and `_render()` (`:2271-2290`) are `outside the packet`, and as noted in R-15, `do_POST` at `:2490` accepts `code` submissions even when the browser stack is present.

#### R-30: F-10 — Unchecked or unlocked writes in `cloud_content_restore`, `backuptool`, and `cloud_setup`
- **Verdict:** narrowed
- **Evidence:** `cloud_content_restore:1405-1407`, `backuptool:1885`, `cloud_setup:69-112`
- All three sites in F-10 are confirmed, and `cloud_content_restore:1405-1406` is more severe than F-10 states: because `:1405` (`> "${SELECTION}.tmp.$$"`) and `:1406` (`mv -f "${SELECTION}.tmp.$$" "${SELECTION}"`) are separate statements not chained with `&&`, a partial write that fails mid-stream on `:1405` is still renamed over `${SELECTION}` by `:1406`, corrupting the stored system selection rather than leaving the old count intact.

#### R-31: F-11 — Device ID MD5 prefix brute-forceability
- **Verdict:** narrowed
- **Evidence:** `cloud_device_id:29-36`, `cloud_device_id:133-145`, `cloud_device_id:162-168`
- Confirmed for the hardware MAC path (`:143-145, :165-166`), where `md5(<MAC>|unknown)` truncated to 10 hex digits (40 bits) is brute-forceable within a known 24-bit vendor OUI (~$2^{24}$ candidates). Narrowed as in R-5 because the `/etc/machine-id` fallback (`:33-36, :167-168`) hashes a 128-bit random ID, and across all 48-bit MACs a 40-bit prefix has ~$2^8$ preimages rather than a unique inverse.

#### R-32: F-12 — `cloud-signin-window` navigation policy and `CLOUD_SIGNIN_DEBUG`
- **Verdict:** narrowed
- **Evidence:** `cloud-signin-window.c:532-534`, `cloud-signin-window.c:660-668`, `cloud-signin-window.c:851-859`, `cloud_oauth:915-917`, `cloud_oauth:990-1000`
- Confirmed that user-gesture navigations are checked against `host_permitted` (`cloud-signin-window.c:851-859`), `registrable_domain` keeps the last two domain labels (`cloud_oauth:990-1000`), and `page_worth_recording` excludes `127.0.0.1`/`localhost` (`cloud-signin-window.c:660-668`; lines 892-916 and 963-966 are `outside the packet`). Narrowed on `CLOUD_SIGNIN_DEBUG` (`cloud-signin-window.c:532`): `if (g_getenv("CLOUD_SIGNIN_DEBUG"))` checks only for a non-NULL pointer, so even `CLOUD_SIGNIN_DEBUG=""` or `CLOUD_SIGNIN_DEBUG=0` in the inherited environment (`cloud_oauth:917`) logs every keystroke string to `window.log` (`0644`, `cloud_oauth:915`).

#### R-33: F-13 — `cloud_folder_validate` `PATH` lookup and host test tool issues
- **Verdict:** confirmed
- **Evidence:** `cloud_folder_validate:90`, `02` § The host tools
- `cloud_folder_validate:90` calls `'rclone'` via `PATH` rather than `/usr/bin/rclone` (line 252 is `outside the packet`). The stale `rclone v1.75.1` pin in `pixelelated-cloud-validator-test` and the missing `ctl/argv` check on refused runs in `pixelelated-content-scope-test` are confirmed from `02` § The host tools.

#### R-34: F-14 — Two `>>> why` sentences missing from `CloudText.cpp`
- **Verdict:** confirmed
- **Evidence:** `cloud_setup:797`, `backuptool:1495`, Context 4 (`CloudText.cpp` why table)
- `ANOTHER CLOUD SYNC IS RUNNING` (`cloud_setup:797`) and `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` (`backuptool:1495`) are both confirmed present in the scripts and absent from the 38 sentences in Context 4.

#### R-35: F-15 — Connection model asymmetries and `cloud_oauth` structure
- **Verdict:** confirmed
- **Evidence:** `cloud_connections.py:54-62`, `cloud_connections.py:140-258`
- Confirmed that `require_manual()` is enforced on `replace=True` (`:150`), `select()` (`:220`), and `remove()` (`:229`) but not on `save(..., replace=False)`, and that `commit()` (`:195-197`) does not write `active-connection` on a first remote (`not config.sections()`), leaving `active()` (`:62`) on the legacy first-section fallback.

#### R-36: F-16 — Reachable legacy paths (`backuptool` zip path and `cloud_setup` console flow)
- **Verdict:** confirmed
- **Evidence:** `backuptool:480-520`, `cloud_setup:918-945`, `cloud_oauth:295`, `cloud_oauth:2346`
- Confirmed from the excerpts that `backuptool`'s read-only legacy zip verification (`:480-520`) and `cloud_setup`'s no-argument SSH console flow (`:918-945`) remain reachable, and `redirect_request` (`:295`) and `do_GET` (`:2346`) are framework callbacks (the full-file function recount across the 10 excerpted files is `outside the packet`).

#### R-37: F-17 — Directory clarity and generated writer/secret tables
- **Verdict:** confirmed
- **Evidence:** `cloud_connections.py:1-258`, `cloud_remote:1-345`, `cloud_content_transfer:1-158`
- Confirmed that the script filenames alone do not distinguish the single `rclone.conf` writer (`cloud_connections.py`), the single deleting script (`cloud_content_restore`), and the boot scrubber (`cloud_log_scrub`), and that the generated tables in `02` provide that map (subject to the corrections in R-1 through R-20; `rclone-cloud-sync.md` itself is `outside the packet`).

#### R-38: F-18 — Timeout bounds and launch-path claim
- **Verdict:** narrowed
- **Evidence:** `cloud_folder_validate:22-24`, `cloud_folder_validate:43`, `cloud_content_transfer:65-96`, `cloud_oauth:300`, `cloud_oauth:516`, `cloud_oauth:2648`, `cloud_connections.py:131`, `cloud_connections.py:168`, `cloud_connections.py:180`, `02` § The runs (`r24_scrub_hook`)
- F-18 states that connection verification is bounded at 40 s and that none of the 14 scripts run on the boot/launch path. However, `cloud_connections.save()` runs two sequential `run()` calls with `timeout=40` (`rclone config create/update` at `:168` and `rclone lsd` at `:180`), and `cloud_log_scrub` runs at boot from `autostart/102-cloud-saves:29` (`r24_scrub_hook`) until both stamp lines are recorded in `/storage/.cache/cloud_sync/log-scrubbed` (`cloud_log_scrub:62`).

#### R-39: F-19 — `cloud-signin-window` `webkitgtk` recipe and `WEBKIT_DISABLE_DMABUF_RENDERER`
- **Verdict:** confirmed
- **Evidence:** `cloud-signin-window/package.mk:9`, `cloud-signin-window/package.mk:17-22`, `cloud-signin-window.c:949`
- Confirmed: `cloud-signin-window/package.mk:9, 20` links against `gtk+-3.0` and `webkit2gtk-4.1` with `-latomic`, and `cloud-signin-window.c:949` sets `WEBKIT_DISABLE_DMABUF_RENDERER=1` with `overwrite=FALSE`.

---

### 7. What the first reader missed

#### R-40: Option injection into `rclone config` via unvalidated `settings` keys in `cloud_connections.save()`
- **Verdict:** new
- **Evidence:** `cloud_connections.py:141`, `cloud_connections.py:161-168`, `cloud_remote:329-335`
- `cloud_remote:329-335` splits any `argv[4:]` argument containing `=` into `(key, value)` without validating `key`, and `cloud_connections.save()` (`:161-165`) appends `'%s=%s' % pair for pair in settings` directly to `rclone`'s argv without checking `key` (unlike `name` at `:141`) and without a `--` end-of-options separator. Because `rclone` parses flags anywhere in argv unless `--` precedes positional arguments, an option-shaped key such as `--config=/path/to/file` or `--log-file=/path/to/file` is honoured by `rclone` as a CLI flag, overriding `--config <staged>` (`:161`) and writing the unverified remote directly to `<path>` before `read_config(staged)` (`:183-185`) raises `Refused('The connection was not saved.')`.

#### R-41: Pre-validation logging of `name` in `cloud_remote:263`
- **Verdict:** new
- **Evidence:** `cloud_remote:263-264`, `cloud_connections.py:141-142`
- In `cloud_remote:263-264`, `cmd_create()` writes `log("updating remote " + name if replace else "creating remote " + name)` to `/var/log/cloud_sync.log` **before** calling `connections.save(name, ...)` (`:264`), which is where `name` is validated against `:[]\r\n\t` and leading `-` (`cloud_connections.py:141-142`). A caller that passes a newline-bearing string or accidentally places a `key=secret` argument in the `<name>` position (`argv[2]`) therefore writes it in cleartext into `/var/log/cloud_sync.log` before `connections.save()` rejects the call.

#### R-42: Unchecked `mktemp -d` and redirection failure fallthrough in `cloud_content_restore:1271-1278`
- **Verdict:** new
- **Evidence:** `cloud_content_restore:1271-1278`
- At `cloud_content_restore:1271`, `TMP=$(mktemp -d /tmp/cloud-scan.XXXXXX); trap 'rm -rf "${TMP}"' EXIT` does not check whether `mktemp -d` succeeded (unlike `cloud_content_transfer:117` and `backuptool:239`). If `mktemp -d` fails, `TMP` is `""`, `:1272` attempts to redirect `rclone lsf` output to `"/cloud.raw"` (setting `scan_rc=1` with an empty/nonexistent `"/cloud.raw"`), and because `:1274` only aborts when `[ "${scan_rc}" -ne 0 ] && [ -s "${TMP}/cloud.raw" ]`, execution falls straight through `:1278` with an empty cloud listing instead of failing closed.

#### R-43: Fail-open pipeline and path-substring match in `cloud_setup:495-499`
- **Verdict:** new
- **Evidence:** `cloud_setup:495-499`
- In `cloud_setup:495`, `probe=$(rclone lsd "${remote}${path}" "${RCLONE_LIST_OPTS[@]}" --log-level ERROR 2>&1 >/dev/null | head -2)` runs without `pipefail` and ignores `rclone`'s exit code. If `rclone` fails without writing to its first two stderr lines (or is killed by a signal), `probe` is `""`, which matches `""` at `:498` and returns `0` (success); likewise, if the user's `${path}` itself contains the substring `"not found"` or `"NoSuchBucket"`, any `rclone` error that echoes the path (such as an auth failure or network error) matches `*"not found"*` at `:498` and falsely reports the folder as valid.

#### R-44: Unescaped regex interpolation and unlocked `CONFIG_ID` capture in `cloud_scan`
- **Verdict:** new
- **Evidence:** `cloud_scan:260`, `cloud_scan:301-308`, `cloud_scan:333-336`, `cloud_scan:360-362`, `cloud_device_id:273`
- In `cloud_scan:260`, `CONFIG_ID=$(context_id) || exit 1` is captured before the `/var/run/cloud_scan.lock` flock is acquired at `:360-362`, and `cloud_scan --folder` (`:301-308`) removes `${OUT}/done` and overwrites `${OUT}/state` in place without re-checking `context_id` or writing a completion stamp. In addition, `cloud_scan:335` interpolates `${label}` (and `${osn}`) unescaped into `grep -E "^[0-9]{4}_...-${label}-..."`, where a `.` in the device ID (permitted by `cloud_device_id:273`) acts as a regex wildcard matching any character.

---

### 8. The lane's grades

#### R-45: Reversal in part of the lane's rejection of A-49 (`backuptool:1284-1292`)
- **Verdict:** narrowed
- **Evidence:** `backuptool:654-655`, `backuptool:1284-1292`, `backuptool:1324`, `backuptool:1334`
- The lane rejected A-49 on the ground that if `find "${STAGING}" -type f` at `backuptool:1285` fails partway, `STAGED` is smaller than `SENT + SANITISED` and `[ "${STAGED}" -ne $((SENT + SANITISED)) ]` at `:1287` fails closed. That holds when `wc -l` outputs a valid integer and `SENT + SANITISED > 0`, **but** `:1287` is written as `if [ "${STAGED}" -ne $((SENT + SANITISED)) ]` rather than `if ! [ "${STAGED}" -eq $((SENT + SANITISED)) ] 2>/dev/null` (compare `:655` and `:1334`): in bash, if `wc -l` fails so `STAGED` is empty, `[ "" -ne ... ]` returns exit status 2 (`integer expression expected`), which `if` treats as false and skips the refusal branch (failing open), and if all files in `FILELIST` were held back so `SENT + SANITISED == 0`, an immediate `find` failure (`STAGED=0`) satisfies `0 -ne 0` as false. A-49 should therefore be narrowed and kept as an Info hardening under F-10 (`! [ "${STAGED}" -eq $((SENT + SANITISED)) ] 2>/dev/null`) rather than rejected outright.

#### R-46: Reversal of the lane's "No finding" dismissal on A-23 (`backuptool:655, 1342`)
- **Verdict:** narrowed
- **Evidence:** `backuptool:655`, `backuptool:1342`, `backuptool:1611`, `backuptool:1822-1823`, `cloud_setup:72-76`, `cloud_setup:104`
- The lane accepted A-23 as theoretical and recorded "No finding" because `TARGET` is a timestamped archive name where a directory is unlikely to exist. However, `02` F-10 explicitly holds `backuptool:1323-1347` up as the model for `engineering-practices.md` § Verify the artifact, not the report, while `cloud_setup:72-76` (citing G-C-04) and `backuptool:1611` (`mv -fT`) and `:1823` (`[ -f "${DEST}" ]`) specifically guard against `mv -f` moving a file inside an existing directory. Adding `-T` and `[ -f "${TARGET}" ]` at `backuptool:655` and `:1342` belongs in F-10 (Info) alongside the other writer-verification items rather than being dropped.

#### R-47: Endorsement of A-27 and A-28 — upgrading F-02 and F-03 from Low to Medium
- **Verdict:** confirmed
- **Evidence:** `cloud_content_restore:235-279`, `cloud_content_restore:750`, `cloud_content_restore:1046`, `cloud_content_backup:583-585`, `stage-b/fixture-content.txt`
- Under T17's security and state-preservation lens (`order.md` Context 1), the lane should adopt Astra's Medium severity for both F-02 (A-27) and F-03 (A-28) rather than leaving them at Low. F-02 is a fail-open guard on the only destructive path (`--match --apply`, D-CLOUD-023) that permanently deletes local saves while bypassing both `SAVE_EXCLUDES` and `--max-delete` (via `:750`), and F-03 is an unvalidated path traversal in `cloud_content_backup` that copies `/storage/.config` (including `rclone.conf` tokens) to the cloud.

#### R-48: Confirmation of F-20 (A-45) — option-shaped key in `cloud_connections.save()`
- **Verdict:** confirmed
- **Evidence:** `cloud_connections.py:141`, `cloud_connections.py:161-168`, `cloud_remote:329-335`
- The lane's grade accepting A-45 as candidate bug **F-20** (confirmed by fixture `c13_option_key.out`) is sound. Because `cloud_connections.save()` (`:161-165`) formats `settings` pairs as `'%s=%s'` into `rclone`'s argv without validating `key` or inserting `--`, an option-shaped key like `--config=<path>` overrides `--config <staged>` (`:161`), causing `rclone config create`/`update` to write the unverified remote directly to `<path>` while `save()` then fails on `read_config(staged)` (`:183-185`). Validating every key in `settings` against `^[A-Za-z0-9_]+$` in `cloud_connections.save()` (and rejecting any key starting with `-`) closes the bug cleanly.

#### R-49: Adjustment to the lane's grade on A-5 (`cloud_log_scrub:94` vs `cloud_oauth:448, 594`)
- **Verdict:** narrowed
- **Evidence:** `cloud_log_scrub:93-95`, `cloud_log_scrub:190-196`, `cloud_oauth:448`, `cloud_oauth:594`, `cloud_connections.py:50-192`
- The lane graded A-5 as "accepted, no leak: the F2 prefix is still written, with fixed sentences only", without recording a finding. As shown in R-6, because `cloud_log_scrub:94`'s allowlist was never updated when `cloud_connections.py` replaced the old error strings with new `Refused` sentences, `cloud_log_scrub` treats today's safe `cloud_oauth:448` failure lines as credential leaks, overwrites the diagnostic reason with `<redacted>`, and prints a false-positive credential-leak warning at boot (`cloud_log_scrub:193`). This drift should be recorded as an Info item (or added to F-14/F-17) so `cloud_log_scrub:94`'s allowlist stays in sync with `cloud_oauth:594` and `cloud_connections.py`.