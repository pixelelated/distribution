# T17 stage-B read notes (lane scratch; never quotes a credential-shaped line)

## cloud_connections.py (258, read whole)
- WRITES: atomic(path,data) :72-88 mkstemp(dir=parent, prefix='.<name>-') -> write, fsync, os.replace, dir fsync; temp unlinked in finally if still there. Mode by construction 0600 (mkstemp), carried through os.replace. Callers: save->commit :197 ACTIVE, :198 CONFIG; save rollback :210 CONFIG; restore_selection :96 ACTIVE (unlink :98); select :224 ACTIVE; remove :252 ACTIVE, :253 CONFIG, rollback :256 CONFIG.
- LOCK: locked() :106-114 flock LOCK_EX|LOCK_NB on /var/run/cloud_sync.lock opened 'a' (default umask mode); every writer (save/select/remove) holds it. Refused 'A cloud operation is running'.
- require_manual :117-126: reads system.cfg as text; refuses if cloudsaves.startup or cloudsaves.gameexit == '1'. Called by save only when replace=True (:150), select :220, remove :229. A NEW create does not require manual mode (design?).
- save :140-215: name check :141 (no : [ ] CR LF TAB, no leading -, no surrounding space). TemporaryDirectory(prefix='.connection-', dir=/storage/.config/rclone) (mkdtemp 0700) -> staged rclone.conf write_bytes(original) then chmod 0600 :159-160 (window inside 0700 dir). argv: ['--config',staged,'config','create'|'update',name,(backend),'k=v'..., '--non-interactive','--obscure'] :161-165 -> SECRET ON ARGV (/proc/<pid>/cmdline, ps) for up to 40 s (run timeout :131); then lsd verify :180 (contimeout 10s timeout 20s, retries 1) under the same 40 s run() timeout. stderr never forwarded (:135-136). JSON 'State' answer -> Refused (needs a computer) :174-175.
  commit :187-198: refuses if CONFIG changed since read (:190-192); pins old selection to ACTIVE only if ACTIVE missing AND config had sections (:195-197); then atomic(CONFIG, updated).
  rollback :205-214 on any exception from publish/commit: restores CONFIG (or unlinks if !existed) only if CONFIG == updated; restore_selection.
- LEGACY FALLBACK (Q1): active() :54-62: ACTIVE present -> its value ('' = tombstone, never falls back; missing section -> Refused); ACTIVE absent -> sorted(sections)[0]. save() does NOT write ACTIVE on a first connection (no sections before) -> after the new writer's first write the device holds rclone.conf with one section and no active-connection: the legacy shape persists by design (:193-194 comment). A second create pins the first.
- read_config :29-51: ini parse; on parse failure runs `rclone --config <path> config dump` (timeout 8) and parses its JSON -- secrets in memory only, never echoed; failure -> Refused (no stderr). Called on CONFIG and on staged.
- remove :227-258: wrapper check regex :235; staged delete; refuses if CONFIG changed :246; writes ACTIVE '' when removing the selected one (tombstone) :250.
- LEFTOVER (candidate): a SIGKILL/power loss between TemporaryDirectory creation and its cleanup leaves /storage/.config/rclone/.connection-XXXX/rclone.conf holding the NEW credentials (0600 in a 0700 dir). Need: does anything sweep '.connection-*'? (grep). backuptool DEVICEONLYDIRS holds rclone/ back, so it never reaches an archive.
- mkstemp temp '.rclone.conf-XXXX' in /storage/.config/rclone: removed in finally; a kill between mkstemp and replace leaves it (0600). Same sweep question.

## cloud_oauth (2830) -- read 1-1368 so far
- consts :72-77. log() :80-87 appends to /var/log/cloud_sync.log (D-SYS-001 persistent), message only; open "a" (umask mode).
- state: _state_locked :175-184 threading lock + flock on session.lock (O_CREAT 0o600). _write_whole :187-193: tmp "<path>.<pid>.tmp" open("w") (DEFAULT UMASK -> 0644 on tmpfs), json.dump, os.replace. STATE_DIR os.makedirs default (0755 under umask 022). reset_state :237-257 unlinks markers open-browser close-browser signed-in page phone-keyboard field.
- write_owned/_fail_owned: attempt/session/from_status guards.
- lan_address :268-281 UDP connect to 192.0.2.1:9, getsockname; else 127.0.0.1.
- provider_url :284-307 follows rclone's /auth on 127.0.0.1:53682 without redirect, 10 s; returns Location (carries client_id, state).
- Session.start :354-411: pkill -f "rclone authorize" :357 (pattern kill; on a host it reaches any process whose argv carries the words), sleep 1, Popen rclone authorize <backend> --auth-no-open-browser (stdout+stderr merged); AUTHORIZE_WAIT 20 s select loop; regex local link; terminate/kill on failure.
- _collect :413-462: token = JSON blob after 'Paste the following' :425-429 (in memory). rclone_says from 'Error:'/'Fatal error:' line -> failure_reason :480-488 'The provider refused it: %s' % said[:160] -> session.json error (screens), NOT log(). log lines here carry fixed words only.
- submit :490-534: pasted code/URL; builds query; urlopen LOCAL_AUTH/?<query> timeout 15 (code in a loopback GET, not logged); 40 x 0.5 s wait.
- _create_remote_locked :560-596: connections.save(name, backend, [("token", token), ("config_refresh_token","false")], replace, publish, check_current) -> TOKEN ON rclone argv (config create k=v) for <=40 s; publish holds _state_locked while commit+status signed-in. Refused/OSError -> log fixed sentence; return str(exc) (Refused messages are fixed sentences).
- BrowserSession.start :905-947: window.log = /var/run/cloud_oauth/window.log open("w") (umask mode), window stdout+stderr -> it. env CLOUD_SIGNIN_PAGE_FILE=state/page (the address the window shows!), _DONE_FILE, _FIELD_FILE. argv: window <url> <registrable_domain> --exit-hint .. [--no-auto-keyboard]. log("sign-in window opened on %s for %s" % (display, host)).
- registrable_domain :990-1000 last two labels (suffix match in the window).
- running_session :820-851 reads /proc/*/environ of sway. stop_other_serves :854-879 walks /proc, kills argv containing 'cloud_oauth' and exact 'serve' (SIGTERM) -- a harness whose argv holds both words would be killed too (e.g. a python running a test named ... with arg 'serve').
- PAGES: PAGE (paste) carries PIN in hidden inputs; PIN_PAGE asks 4 digits; REMOTE_PAGE: phone keyboard; JS posts to "/" + pin (PIN IN URL PATH) with pin in body; typed text crosses LAN HTTP unencrypted (page says so, en+fr). type=password box masked; dropped chars counted when masked.
- (1369-2831 read)
- uinput keyboard/mouse :1498-1709 (US keymap; type_text skips unmapped silently; counts returned). GamepadBridge :1910-2042 EVIOCGRAB while window up; Select/Mode+Start quits; watchdog 0.5 s.
- SessionHolder :2044-2206: pin "%04d" % secrets.randbelow(10000) :2062; attempt token_hex(6); pin_attempts; pin_exhausted >=10 :2196-2198; pin_failed :2200-2203; authorised compare_digest(str(pin), self.pin) :2205-2206.
- BoundedHTTPServer :2220-2244 semaphore 16, over-cap closed on arrival. MAX_BODY 64 KiB checked before body read (:2395-2405 -> 413/400). REQUEST_TIMEOUT 15 socket timeout. log_message silenced :2260.
- _gate :2308-2328: exhausted -> 403; authorised -> proceed; empty pin -> PIN page (no count); wrong -> pin_failed (+1), 403 at 10, else PIN page "did not match".
- _supplied :2330-2344: ?pin= query else FIRST PATH SEGMENT. => GET /favicon.ico counts as a wrong PIN (candidate BUG: browser icon requests -- favicon.ico, apple-touch-icon*.png -- burn the 10 attempts; at 10 even the right PIN gets 403 for the rest of the serve; the phone keyboard is locked out). Fixture: host python, make_handler with a stub holder over loopback.
- compare_digest(str, str) raises TypeError on non-ASCII str (Python doc). POST body pin is percent-DECODED by parse_qs -> pin=%C3%A9 -> TypeError in the handler thread -> socketserver.handle_error prints a traceback to stderr, connection dropped; not counted as a failure (Info; fixture). Path pin stays percent-encoded ASCII; request line latin-1 can carry non-ASCII.
- do_GET probe :2355-2389: answers 'waiting' | 'loading <8hex>' | 'open <8hex>' (sha256[:8] of the window's page file, never the URL).
- do_POST: move/click/wheel 409 without browser; type/key 409 without browser; log counts only :2455-2457 ('typed %d characters'); restart -> holder.start; code -> session.submit -> DONE page + shutdown in 2 s.
- HTML injection (Info): _render's message inserted raw into PAGE: restart error (session.error / state error) and submit detail = failure_reason() which embeds rclone_says[:160] (rclone's output, i.e. the provider's error text) -- only on the paste flow (browser stack absent). PAGE %(name)s and DONE_PAGE %(name)s/%(remote)s not html-escaped (phone_page escapes name) -- names are local.
- cmd_serve :2510-2540 stop_other_serves, reset_state, SIGTERM handler -> SystemExit, finally holder.end(). serve_with :2542-2663: bind lan_address (127.0.0.1 when no route) port 8080 default; on EADDRINUSE log port+errno, state words. write_owned waiting with url (contains PIN), address, provider (rclone state), pin, name -> session.json (0644 by umask). stdout contract URL= ADDRESS= PIN= NAME= PROVIDER= EXIT_HINT= (ES reads). Timer(timeout=600 default) shutdown.
- main: open/close/wait/info/status/cancel. info prints URL, ADDRESS, PIN, NAME, PROVIDER, STATUS... to stdout. cancel :2817-2824 stop_other_serves, pkill -f "rclone authorize" :2819, reset_state idle (clears pin/url/provider). close kills window by argv[0] exact match.
- SECRETS in cloud_oauth: token -> memory -> rclone argv (via connections.save) -> rclone.conf (0600). OAuth code: in the provider redirect (browser address bar on device; window's page file?; loopback GET to rclone :516). PIN: session.json (0644 tmpfs), stdout to ES, URL path, phone page JS, QR. Typed text: phone page -> LAN HTTP plaintext (disclosed) -> uinput; log counts only.

## cloud-signin-window.c (1052, read whole) + package.mk (27, read whole)
- host_permitted :36-59: localhost/127.0.0.1 always; allowed_host NULL -> TRUE (unreachable from cloud_oauth, which always passes one; "" refuses nearly all); dropbox.com adds 4 IdP hosts; exact or dot-suffix match. registrable_domain (cloud_oauth :990) = last two labels -> for drive, accounts.google.com -> google.com (any *.google.com).
- on_decide_policy :794-861: only NAVIGATION_ACTION; non-http(s) allowed; NON-GESTURE navigations allowed (by design, captcha/IdP iframes); gesture to non-permitted host refused + g_message host to window.log.
- on_auth_create :892-916: popup only if network+permitted host or about:blank by gesture; one popup at a time.
- page_worth_recording :660-671 excludes host 127.0.0.1 / localhost (exact 9 chars) -> the code-bearing redirect never reaches CLOUD_SIGNIN_PAGE_FILE (#308 F-RS-20). page file written by g_file_set_contents (0666 & ~umask -> 0644) :726; other providers' URLs recorded (client_id/state in query). cloud_oauth probe exposes only sha256[:8].
- field file :406-409 writes 'TAG/type/id-or-name' (no value).
- on_key :530-535 g_message("key %s (%u)", event->string, keyval) under CLOUD_SIGNIN_DEBUG -> TYPED CHARACTERS to window.log (stderr -> /var/run/cloud_oauth/window.log via cloud_oauth :941). CLOUD_SIGNIN_DEBUG set nowhere in projects/packages/tools; cloud_oauth passes env=dict(os.environ) :917 -> an exported var reaches it. Info.
- Escape quits; F1-F4 mapped; OSK printable ASCII 3 layouts.
- ephemeral web context :963-966; WEBKIT_DISABLE_DMABUF_RENDERER=1 default (no overwrite) :949 (blindspot 48 family: memory on 1 GB).
- package.mk: PKG_VERSION="" (in-tree), deps gtk3 webkitgtk, -latomic; installs /usr/bin/cloud-signin-window.

## cloud_setup (976, read whole)
- writes NO rclone.conf. Its rclone calls: lsf/lsd/cat/rcat/mkdir/copyto(--ignore-existing)/backend features/config file/config show(type line only)/listremotes. rclone stderr dropped everywhere EXCEPT syncpath_problem :495 probe=$(rclone lsd ... --log-level ERROR 2>&1 >/dev/null | head -2) -> echoed to stdout :537/:543 -> ES shows it ('Your provider wouldn't accept this folder:'). Sink: rclone's ERROR text on the screen (e.g. a URL); mask none. Info/Low.
- conf_set :69-112: awk via env, tmp "${SYNC_CONF}.tmp.$$" (umask mode), mv -f, then a positive check every KEY="value" line present (grep -qFx). Refuses non-file at the path. NO LOCK on cloud_sync.conf writes (--set-*-remote, --use-content-root). cloud_sync.conf holds folder names, not secrets.
- conf_get :136-183 first assignment, refuses $ ` \ in "", controls, other forms -> exit 2 with why on stdout.
- resolve_connection :207-226: override file /storage/.config/cloud_setup_ssh first line -> SSH_CMD, LOGGED :224 'Using connection override: ${SSH_CMD}' and :928 (a file the owner writes; could hold anything). Info.
- CONSOLE FLOW :913-976 (legacy, via run): ROOTPASS=$(get_setting root.password) :926 SHOWN ON SCREEN :937. --info prints PASSWORD_SET only :618 (#116, D-INFRA-008). Sink: screen (console flow) -- the root password, by design of the legacy SSH flow.
- validation_context :548-568 config_id = sha256 over REMOTE/SAVES/BACKUPS/CONTENT + sha256 of rclone.conf, cloud_sync.conf, active-connection, pipefail subshell :556; only the digest leaves.
- folder_values defaults /pixelelated/{Saves,Backups,Content}; CONTENT explicit empty = root.
- folder_marker_read/write: mktemp /tmp checked (|| return 5) :394; rcat .layout.
- --seed-folders :791-884 flock -n fd9 on /var/run/cloud_sync.lock (exit 75 'ANOTHER CLOUD SYNC IS RUNNING' -- note the why sentence differs from es-player-text's 'A SYNC IS ALREADY RUNNING'?? check: es-player-text table maps rc 75 SKIPPED - A SYNC IS ALREADY RUNNING; the >>> why line here says ANOTHER CLOUD SYNC IS RUNNING, which the rule's register table lists as the OLD formal wording ('Not this: ANOTHER CLOUD SYNC IS RUNNING'). CANDIDATE Q2 FINDING.) mkdir --s3-directory-markers; seed_note never clobbers (listing then copyto --ignore-existing); positive check by listing.
- --free-auth-port :772-780 pkill -f "rclone config" + "rclone authorize" (pattern kills; reach: any argv with those words; cloud_connections' staged argv '/usr/bin/rclone --config <...rclone.conf> config create' does not contain the substring 'rclone config').
- --check :886-910 lsd bounded.
- unquoted [ -f ${SYNC_CONF} ] :137, >> ${LOG_FILE} :53 (constants).

## WHY SENTENCES vs ES whySentences() at the pin 16dbac5211 (CloudText.cpp:414-466, 38 entries; ES read allowed by the coordinator 06:2x)
- literal '>>> why <S>' lines in the 14 (29 lines, 7 sentences) + helper args (say_why/why/reason=, 23 sentences): all in the table EXCEPT
  - 'ANOTHER CLOUD SYNC IS RUNNING' cloud_setup:797 (--seed-folders, exit 75) -- also es-player-text.md:227's "Not this" (D-UI-031) form of 'A SYNC IS ALREADY RUNNING'. ES at the pin special-cases --seed-folders (CloudText.cpp:663); whether the screen shows this line is the ES slice's read. Q2 Low.
  - "THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK" (backuptool; es-player-text lists it 'proposed, D-UI-117'). Not in the table -> English on a French screen if shown. Q2 Low. (whySentences' own comment: CloudTextTests' emitter table should fail on a why not here -- that test is ES's, not run here.)
- method: stage-b/why-check (to write as a generated table).

## cloud_remote (345, read whole)
- secrets path: ES passes key=value pairs on cloud_remote's ARGV (main :325-335) -> connections.save -> rclone argv. Two process argvs carry the typed secret for the create's duration (<=40 s + lsd). rclone() :83-97 logs 'rclone <verb> failed (<code>)' only (since e2d45ec7ec, audit #307 PL-074). 'expected key=value, got: %s' :331 echoes a malformed pair to stderr (Info). cmd_create logs 'creating remote <name>' :263; adds directory_markers=true for s3/gcs/azureblob. Exceptions -> fixed sentences to stderr, exit 2 :341-345. cmd_list prints name/type/selection/provider only. 'active' prints name: or exits 1 (Refused -> exit 2 'The selected connection is missing...').
- tiers: NOT_PROVIDERS plumbing; 'token' option -> oauth; else keys.
- rclone() has NO timeout (providers/fields/choices calls: `rclone config providers` local, no network).

## cloud_log_scrub (206, read whole)
- once per device per family at boot (102-cloud-saves:29); STAMP /storage/.cache/cloud_sync/log-scrubbed lines scrubbed= and es_log_scrubbed=; pipefail :63; refuses (exit 1, retried next boot) without redact_credentials :67-71.
- FAMILIES (the shapes earlier builds wrote):
  F1 cloud_remote failure lines with arguments (pre e2d45ec7ec): SCRUB_SED :79-92 -> 'rclone <verb> failed (<code>)'; truncated lines masked key by key. WRITES TODAY: no (cloud_remote:95-96 verb+code).
  F2 cloud_oauth 'could not finish the sign-in: <rclone words>' :93-95 -> <redacted> unless one of 6 fixed sentences. WRITES TODAY: the SHAPE yes (cloud_oauth:448 'could not finish the sign-in: %s' % detail) but detail is now a fixed Refused sentence / CLOSED_EARLY / 'Your cloud settings could not be saved.' (cloud_oauth:592-594) -- no rclone words. The scrub's allowlist names older sentences, so it would redact today's harmless ones (no loss: one-time).
  F3 ES 'cloud_remote create: <output>' records + continuation lines in es_log*.txt :104-121 (ES cf09fc2f8..731252c61). WRITES TODAY: not this slice's (ES), per the comment no since ES 731252c61.
  + every line through redact_credentials (001-functions:69, outside the 14: words passw|passphrase|token|api_?key|access[_-]?key|secret|psk|wifi.key|retroachievements.key, marks, URL user:pw@).
- scrub(): tmp "$f.scrub.$$", re-read if grew (<=3), LINE-COUNT PARITY :148, changed count, mv; family skips symlinks and *.scrub.*; record() tmp+mv keeping other lines.
- Already-written note: a device whose cloud log trimmed past 1 MiB, or a log the scrubber could not rewrite, keeps trying next boot; record written only on success.

## cloud_device_id (401, read whole)
- ID_FILE /storage/.config/cloud_sync-device-id :54; .previous :58. write_id :288-293 tmp.$$ + mv (umask mode); remember_previous :298-303 append >> then positive grep.
- id = device_label (dt model / HW_DEVICE / os-release / hostname, hyphenated, <=32) + '-' + md5(MAC|${DEVICE:-unknown})[:10] :143-145 (DEVICE never set on a device -> 'unknown'); machine-id fallback :170; 'unknown'.
- PRIVACY (Info): comment :29-31 'hashed rather than stored ... no business sitting in somebody's cloud in the clear'. Unsalted md5 of a 48-bit MAC whose 24-bit OUI is the adapter vendor's -> ~2^24 candidates per vendor -> the MAC is recoverable from the folder name in seconds. The hash hides it from a glance, not from anyone who tries. Changing the recipe = another identity change (needs a legacy variant, :136-142). Secret path: device id -> cloud folder names (Backups/<id>), logs (heal lines), stdout to cloud_backup/restore/capture.
- usable_interfaces :91-104 type==1 and /device exists (sit0 #86). valid_mac :112-119 positive shape.
- heal_poisoned :317-339: records old id in .previous first; heals only the poisoned hash.
- --if-present :363-376 never seeds from machine-id. empty id file + no adapter -> refuse (exit 1, nothing on stdout).
- id file held back from archives (backuptool DEVICEONLY lists it).

## backuptool (1899, read whole)
- conf_text_value :43-57 reads SETTINGS_BACKUPS/BACKUPFOLDER as text; /storage/* only.
- newest_backup :159-171 any device's archive (by name sort); legacy names.
- fail/note/why :189-271; to_log :255-262 keeps tool stderr in logger (cut 500).
- take_lock :209-213 flock on fd9 opened on the SETTINGS_BACKUPS dir. sweep_leftovers :222-226 .partial at root and archive/, rm -rf STAGING_PREFIX* (/storage/.cache/backuptool-staging., :762). EXIT trap rm -rf STAGING :227.
- tmp_file :237-246 mktemp checked (regular, empty, not link).
- DEFAULT list :283-318 (+ player's themes). backuptool.conf IS SOURCED as root :335 and is itself in DEFAULT :285 (travels). DESIGN NOTE: a restore already writes any file under /storage (foreign_member refuses only outside storage/ or ./.. parts), so a sourced backuptool.conf from an archive adds no new boundary beyond what a restore writes (profile.d scripts, es scripts/*). Record as design, cite D-CLOUD-142's different ruling for cloud_sync.conf.
- keep_meta :367-372 mode+time onto sanitised copies, status checked (4 call sites :1203 :1221 :1236 :1255).
- credential_lines :431-459: CREDENTIAL_KEYS (text configs) + CREDENTIAL_TOKENS (any text file, -I skips binary); walk status and each grep's status read; lang/locale/translations exempt for KEYS; returns count; names files in logger (names only).
- zip path: zip_stored_ok :480-514 (CRC column required; stored members CRC'd with busybox crc32), archive_ok :515-520, archive_members :534-540 (pipefail), foreign_member :551-558 (members not under storage/ or with ./.. refused -> 'THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK' :1495). Restore needs crc32 for zips :1441-1445. LEGACY ZIP disposition (Q6): reachable while a device holds *_BACKUP.zip or ROCKNIX_BACKUP.zip (newest_backup, :1434-1437) -- a row, removals none.
- SYMLINK MEMBERS (candidate, to fixture): foreign_member judges NAMES only; a tar member that is a SYMLINK under storage/ (e.g. storage/.config/x -> /outside) followed by storage/.config/x/f would be extracted by `tar -xzf -C / -X SKIP` :1679 through the link. LINKS skip :1633-1638 covers only paths that are symlinks on the DEVICE. snapshot_members/NEWLIST cover storage/ paths only, so a revert would not remove the outside file. backuptool's own archives hold regular files only (find storage -type f :1324) -> only a hand-made/foreign/tampered archive. D-UI-117's promise is about member names. Fixture: donor busybox tar over a scratch root.
- write_archive :805-1348: canonical walk (readlink -f), outside /storage -> 6; find status -> 2; filter own backups/staging/cores/evidence/RESTORE_CONTROL :907-921; prune /usr/config-identical seeds -> SEEDED list :940-994; hold-back SECRETLIST :1016-1112 (system.cfg, es_settings.cfg, retroarch.cfg, rclone.conf; DEVICEONLY 4; RATOKENFILES 5; RATOKENSETTINGS 4; DEVICEONLYDIRS rclone/ raofflineproxy/; .backup .bak .tmp .old beside them), counted; SENDLIST arithmetic :1128-1142 (NSEND == NFILES - unique(SECRETLIST)); staging on /storage/.cache via mktemp -d :1161; collect tar|tar pipefail :1177-1179; sanitised copies :1193-1261 (system.cfg drops lines with .key=/.password=/.token=; es_settings drops ScreenScraperPass/ScreenScraperDevPass/IGDBSecret -- at the ES pin these are exactly the Settings secrets; retroarch blanks *password/token/stream_key; RA settings blank Token/Password); SEEDLIST; count STAGED == SENT + SANITISED :1287; credential scan -> 5 :1298-1311; tar to .partial from member list :1324-1325; listed back == STAGED :1334; mv.
- trim_archive :1372-1384 by name date, ARCHIVE_KEEP=3, never the pre-restore copy just taken.
- restore :1413-1765: flock+crc32 tool checks, lock, sweep, newest_backup, archive_ok, snapshot path unique, MEMBERS/NEWLIST/SEEDS, foreign_member, SEEDLIST read whole, snapshot_members (4 = nothing to copy), RESTORE_MARK written and read back (first line, last line, count) :1608-1620, LINKS skip, SKIPS (assets, cache, RATOKENFILES, DEVICEONLYDIR patterns, DEVICEONLY, SEEDLIST, LINKS, RESTORE_CONTROL, backups folder, snapshot), tar -X written whole and counted :1676-1684 / unzip -x :1706, seeds cp back, revert on failure, mark removed, markers, reboot unless --no-restart.
- backup :1766-1894: tool checks, lock, sweep, move upstream ARCHIVED_*.zip to archive/upstream-era (mv -n + positive check) :1810-1829, unique name, PREVIOUS, write_archive codes 4/2/5/6/*, rotate PREVIOUS (mv UNCHECKED :1885 -- a failed mv leaves two archives at the root, both uploaded; Info), trim.
- 'backup' message 'COPY IT SOMEWHERE SAFE, OR BACK UP SETTINGS TO THE CLOUD UNDER GAME SETTINGS > MANAGE CLOUD STORAGE.' -- menu path in player text (upgrade-and-install: a string naming a menu path; check es-menu-map at stage C? note).

## cloud_content_restore (1589) -- read 1-450 so far
- --known-directories :59-62 (no credentials).
- EXIT 75/69 :74; take_cloud_lock :116-129 exec 9> + flock -n, 4 tries x 0.25 s, 'Skipped: another cloud sync is already running.' exit 75; body runs with 9>&- (comment).
- CONTENT_CONFIG_ID = cloud_scan --context :133-137, compared again under the lock (content_context_current :138-141).
- rclone.conf existence gate :143-147 (why YOUR CLOUD STORAGE ISN'T SET UP YET).
- conf_get :177-224 (same reader as cloud_setup). CONTENT_REMOTE refusals :225-244; RCLONE_NET_OPTS read :235-238.
- REMOTENAME = cloud_remote active :246-252 (selection-reason why).
- path checks :254-262; ROOT = remote:CONTENT/.
- **RCLONE_NET_OPTS FLAG INJECTION (candidate):** :276-279 the conf value (double-quoted may hold spaces) split into RCLONE_NET_OPTS_ARRAY and passed to every networked rclone call INCLUDING the match apply's deleting `sync` :1046 and the dry run :750. No allowlist of flags, no strip of --delete-excluded (T16's cloud_restore:1383 strips --delete-excluded from RCLONEOPTS only; cloud_restore:1406-1411 and cloud_backup:1367-1371 split RCLONE_NET_OPTS the same unfiltered way -- the seam, T16's side named). A conf line RCLONE_NET_OPTS="... --delete-excluded" makes --match --apply delete the SAVE_EXCLUDES/SYSTEM_SAVE_EXCLUDES/CONFLICT_EXCLUDES/METADATA_EXCLUDES files under /storage/roms/<sys> (the saves the excludes exist to protect, comment :528). No shipped build writes such a value (defaults :94). Fail-open guard; rule rclone-cloud-sync.md:207-218 'treat any restore-side --delete-excluded as a bug'. Fixture: stub rclone recording argv.
- write_stamp :296-303 tmp.$$ + mv; record_outcome :304-311 'epoch rc [WHY_TOKEN]'.
- say_why/why_for :317-331; network_gone :346-352 (lsd probe + ping 1.1.1.1 / 8.8.8.8 -- the device's network, not this lane's); stop_no_network :388-398 (gaps token when PROGRESS_MADE).
- moved_since :381-386 reads LOG_FILE tail for Copied/Moved/Deleted.
- remote_for :412-417 bios->ROOT/BIOS, else ROOT/ROMs/<sys>.
- exists_remote :436-442: grep -qx "${name}/" is a REGEX (a name with . or other metachars matches more) -- Info.
- (450-1589 read)
- absent_not_broken :456-480 bounded to ROOT; list_content_dirs :484-491 partial output never empty.
- SELECTION /storage/.cache/cloud_sync/content-systems :508; selected_systems regex :514-517.
- match rules comment :519-547; SAVE_EXCLUDES :577-585; SYSTEM_SAVE_EXCLUDES n64 :589-595; CONFLICT_EXCLUDES :612-616; GAMELIST_ONLY :654-659; METADATA_EXCLUDES :675-683.
- cloud_root_populated :698-704 (rule 3; failure -> 0 -> refuse).
- match_plan_one :726-783: listing 0/3/4 or absent_not_broken else fail; present -> sync --dry-run with ALL excludes + RCLONE_NET_OPTS_ARRAY :750-752, count 'Skipped delete'; absent -> rclone size local with excludes :769-781 (remove verb).
- TREE_CLEAN record :794-798.
- MATCH_PLAN /storage/.cache/cloud_sync/content-match-plan :812; match_plan_write :813-822 checks context, header 'plan2 <epoch> <config_id> <mode>' + lines, tmp.$$ + mv (umask).
- match_before :836-842 mktemp /tmp with predictable $$ FALLBACK :837-838 (single-user device; Info as brief).
- match_count :843-858 counts Deleted lines vs before-list; appends MATCH_LOG to LOG_FILE.
- match_run :860-1119: excludes asserted non-empty :866-870; apply takes the lock :873-875; SPEND FIRST :885-897 (rm -f, refuse if still there); context/mode drift :898-903 'SOMETHING CHANGED SINCE YOU CHECKED'; empty plan :904-909 'CHECK WHAT WOULD CHANGE FIRST'; cloud_root_populated :914-928; per system :970-980 verb equal and files <= pfiles else refuse that system; files := pfiles -> --max-delete. DELETING: remove -> `rclone delete DEST/sys excludes --max-delete files` :1015-1018 (local only, no net opts); sync -> `bounded_content_rclone sync remote DEST/sys NET_OPTS excludes --max-delete files` :1046-1050. Both only under apply=1 after the spent plan. rmdir empty dir :1027. Preview writes the plan only when rc==0 :1095-1101.
  - plan has a timestamp; NO AGE CHECK (Info/design: D-CLOUD-141 spends it; the per-system count bounds a stale plan).
- content_files :1121-1158 find with the same save/conflict/partial excludes + media modes + n64 states.
- --scan :1260-1372 read-only; mktemp -d /tmp + trap rm -rf (the 12th rm -rf) :1271; partial output -> exit 5; network_gone -> 69; else rc.
- --set-systems :1378-1409 regex per name, set -f :1389; WRITE UNCHECKED: `{...} > SELECTION.tmp.$$ 2>/dev/null; mv -f ... || rm -f` then `echo "OK $(selected_systems | wc -l) selected"; exit 0` -> a failed write prints OK with the OLD count and exits 0 (Info/Low: success over a failed write; the count is the artifact's, but not compared with the request).
- --selected/--list/--all :1410-1470; dir name regex before any transfer :1482-1487; lock :1490; context re-check under the lock :1499-1503; copy loop (copy only, excludes, README.txt, gamelist --update pass) :1506-1577; record_outcome :1584.

## cloud_content_backup (799, read whole)
- copy only (bounded_content_rclone copy :753, gamelist --update pass :766), mkdir unchecked by design :747; lock :691; context re-check under lock :700-704; conf_get (same reader); RCLONE_NET_OPTS split the same way :230-232 (copy: --delete-excluded no-op for copy -> no deletion risk here).
- list_local_dirs :447-476 allowlist = ES-declared systems + bios, minus savefiles/savestates/screenshots/backup, has_content.
- **EXPLICIT NAMES NOT VALIDATED (candidate bug):** `*) DIRS=("$@")` :583-585 then SRC="${DEST}/${DIR}" :710, TARGET=remote_for :711 -- no ^[A-Za-z0-9_][A-Za-z0-9._-]*$ check (cloud_content_restore has it at :1482-1487; selected_systems filters --selected; --all comes from list_local_dirs). A name '../.config' uploads /storage/.config (rclone.conf among it) to <root>ROMs/../.config. Caller: ES picker passes names it listed; a direct command line reaches it. Audit #307 PL-030's rule ('only a system folder's name is ever acted on') holds for restore and --set-systems, not backup's argv form. Fixture: stub rclone recording SRC.
- network_gone/stop_no_network/record_outcome as restore. Stamp last-content-backup.

## cloud_content_transfer (158, read whole)
- sourced. bounded_content_rclone :85-158 subshell: verb is the caller's first arg -- every call site passes a literal copy/sync (backup :753 :766; restore :750 :1046 :1538 :1551) -> no verb from input. Adds --progress if absent. ceiling = idle(--timeout)+6 else 36 s. mktemp -d ${CEILING_DIR_ROOT:-/var/run}/cloud-content.XXXXXX + mkfifo, failure -> exit 1 (fail closed) :117-120; trace tee; progress_mark 5 counters :28-47 (bytes, checks, files, deleted, listed); advance_mark high water; no progress for ceiling -> stop_child TERM then KILL -> 124 :141-143. cleanup rm -rf -- dir :110 (the 2nd of the 12).
- idle_timeout_seconds :65-80 reads --timeout from the args (incl. RCLONE_NET_OPTS).

## cloud_scan (362, read whole)
- read-only; results under /storage/.cache/cloud_sync/scan; lock /var/run/cloud_scan.lock fd8 flock -n -> why ANOTHER CLOUD CHECK IS RUNNING exit 75 :360-362.
- context_id :173-192 sha256 over 7 files (cloud_sync.conf, rclone.conf, active-connection, rules, content-systems, es_systems x2), unreadable/non-file -> fail. result_id/write_completion :193-230 JSON binding run/config/mode/result, tmp.$$ + mv. --stamp-valid :234-248.
- prepare :131-146 default route only (69), cloud_remote active / selection-reason why.
- stop_on :149-169 (exit 69 passes; app output's >>> why taken; 124 -> STOPPED ANSWERING; else FOLDER COULDN'T BE READ; rclone codes why_for_rc). Probe that can report absence: yes (every non-zero routed).
- sources rasteratops-settings-archive :326-328 (T16's).
- RUN_ID regex :258. unknown option -> exit 2.

## cloud_folder_validate (278, read whole)
- bounded read-only: command() :43-76 stderr DEVNULL (credentials), start_new_session, killpg on timeout, 2 MiB, 6 s per call, 25 s total; listing() :89-113 lsjson --recursive --max-depth N --contimeout 3s --timeout 5s --max-duration 6s, rc 3/4 + '['/[] -> None (missing), else Unreadable; validates entries (path shape, depth, dupes, controls) :105-112; MAX_ENTRIES 4096.
- 'rclone' from PATH (args[0] 'rclone', :90, :252) -- not /usr/bin/rclone: M7 #1117 (the validator bound to the package's rclone). Cite.
- context via cloud_setup --validation-context before and after (config drift -> configuration-changed) :216/:267-269.
- classify :174-202; result JSON; exit 0 complete else 5. Unreadable is the honest answer (blindspot 22 shape satisfied).
