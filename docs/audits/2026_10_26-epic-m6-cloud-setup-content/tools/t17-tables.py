#!/usr/bin/env python3
"""T17 (#664): 02-forward-audit.md's generated tables.

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-tables.py write|check <02-forward-audit.md>

Sections (each between <!-- begin t17:<name> --> and <!-- end t17:<name> -->):
  coverage   one row per path of the 14 (asserts 14 and 11,180 lines)
  runs       stage A's 40 runs from stage-a/out/runs.tsv (asserts 40, all rc 0)
  tools      stage B's five tools from stage-b/tools-out/tools.tsv
  writers    one row per writing statement, each anchored by a pattern that
             must match exactly the asserted number of lines at 8ebaf8daad
  secrets    one row per credential kind per sink, each anchored the same way
             where a line exists (a sink no line reaches says so)
  deletions  every rm -rf, rclone delete, sync, move and purge in the 14, by
             grep at 8ebaf8daad, with its bound and condition; asserts the
             counts (12 rm -rf; 1 delete; 3 sync statements; 0 move, 0 purge;
             --delete-excluded only in a comment)

Every anchor is read with `git show 8ebaf8daad:<path>`; a pattern that matches
a different number of lines than asserted exits 1 naming it (drift).
`check` exits 1 when the file differs from a fresh generation.
"""
import collections, re, subprocess, sys
from pathlib import Path

R = "8ebaf8daad"
A = Path("docs/audits/2026_10_26-epic-m6-cloud-setup-content")
P = "projects/ROCKNIX/packages/network/rclone/sources/"
F = {
    "connections": P + "cloud_connections.py", "oauth": P + "cloud_oauth", "remote": P + "cloud_remote",
    "setup": P + "cloud_setup", "restore": P + "cloud_content_restore", "backup": P + "cloud_content_backup",
    "transfer": P + "cloud_content_transfer", "scan": P + "cloud_scan", "validate": P + "cloud_folder_validate",
    "device_id": P + "cloud_device_id", "scrub": P + "cloud_log_scrub",
    "window": "projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c",
    "recipe": "projects/ROCKNIX/packages/network/cloud-signin-window/package.mk",
    "backuptool": "projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool",
}
_cache = {}


def lines(key):
    if key not in _cache:
        _cache[key] = subprocess.run(["git", "show", f"{R}:{F[key]}"], capture_output=True, text=True,
                                     check=True).stdout.splitlines()
    return _cache[key]


def anchor(key, pattern, count=1):
    hits = [i + 1 for i, l in enumerate(lines(key)) if re.search(pattern, l)]
    if len(hits) != count:
        sys.exit(f"t17-tables: drift: {F[key]} /{pattern}/ matched {len(hits)} line(s) {hits}, expected {count}")
    return hits


def short(key):
    return Path(F[key]).name


def cite(key, pattern, count=1):
    return ", ".join(f"`{short(key)}:{n}`" for n in anchor(key, pattern, count))


# --- coverage -----------------------------------------------------------------
def coverage():
    paths = (A / "stage-a/paths.txt").read_text().split("\n")[:-1]
    assert len(paths) == 14, len(paths)
    what = {
        "cloud_connections.py": "the one writer of `rclone.conf` and `active-connection`; read whole",
        "cloud_oauth": "sign-in broker, phone page, state; read whole",
        "cloud-signin-window.c": "the WebKit window and its navigation policy; read whole",
        "package.mk": "the window's recipe; read whole",
        "cloud_setup": "folders, markers, validation context, console flow; read whole",
        "cloud_remote": "providers, fields, create/update, active; read whole",
        "cloud_log_scrub": "the one-time log scrub; read whole",
        "cloud_device_id": "this device's cloud name; read whole",
        "backuptool": "the settings archive; read whole",
        "cloud_content_restore": "content restore and the only deleting path (`--match --apply`); read whole",
        "cloud_content_backup": "content backup, copy only; read whole",
        "cloud_content_transfer": "the bounded rclone wrapper (sourced); read whole",
        "cloud_scan": "the read-only opening scan; read whole",
        "cloud_folder_validate": "the bounded category validator; read whole",
    }
    finding = {"cloud_oauth": "F-01, F-05, F-09", "cloud_content_restore": "F-02, F-08, F-10",
               "cloud_content_backup": "F-03", "backuptool": "F-04, F-10, F-16",
               "cloud_connections.py": "F-05, F-06, F-15", "cloud_setup": "F-07, F-10, F-14",
               "cloud_device_id": "F-11", "cloud-signin-window.c": "F-12", "cloud_log_scrub": "-- (§ The secrets' paths)",
               "cloud_remote": "F-05, F-07", "cloud_scan": "--", "cloud_folder_validate": "F-13",
               "cloud_content_transfer": "F-02", "package.mk": "F-19"}
    out = ["| Path | Lines | Read | What it is | Findings |", "| --- | ---: | --- | --- | --- |"]
    total = 0
    for p in paths:
        n = len(subprocess.run(["git", "show", f"{R}:{p}"], capture_output=True, text=True, check=True).stdout.splitlines())
        total += n
        name = Path(p).name
        out.append(f"| `{p}` | {n:,} | whole | {what[name]} | {finding[name]} |")
    assert total == 11180, total
    return "\n".join(out)


# --- runs ------------------------------------------------------------------------
FAIL = {
    "r01_block": "a membership other than 14 paths and 11,180 lines, or a tier or reach other than fork-own and shipped",
    "r02_modes": "a mode other than 10 x 100755 and 4 x 100644",
    "r03_lines": "a line total other than 11,180",
    "r04_shell_functions": "a function count other than 112 strict / 147 loose",
    "r05_python_defs": "a def or class count other than 124 / 9",
    "r06_set_discipline": "a global set -e or -u, or pipefail somewhere new, or an eval in code",
    "r07_exit_constants": "an exit constant other than 75 and 69 in the 14",
    "r08_writer_rclone_conf": "an rclone.conf writer other than cloud_connections.py",
    "r09_setup_remote_config": "an `rclone config` write in cloud_setup, or cloud_remote writing other than through connections.save",
    "r10_deleting_statements": "a deleting statement other than restore :750 (dry run), :1015 and :1046",
    "r11_delete_excluded": "--delete-excluded anywhere but the comment at restore :528",
    "r12_rm_rf": "an rm -rf count other than 12, or one on something other than a script's own temporary",
    "r13_match_refusals": "a refusal line missing before the deleting sync",
    "r14_pattern_kills": "a pattern kill other than setup :775-776 and oauth :357, :2819",
    "r15_unquoted": "an unquoted expansion other than the five constants",
    "r16_dollar_dollar": "a `.$$` name other than the 15 listed",
    "r17_oauth_bounds": "a changed OAuth constant or bound",
    "r18_backuptool_lists": "a held-back list other than DEVICEONLYDIRS and DEVICEONLY as read",
    "r19_backuptool_shape": "ARCHIVE_KEEP, the 5) arm or the .partial writes moved",
    "r20_backuptool_logger": "a logger -t backuptool count other than 37",
    "r21_device_id": "a changed id derivation or write",
    "r22_validate_bounds": "a changed validator bound or stderr handling",
    "r23_scan_routing": "a changed stop_on",
    "r24_scrub_hook": "the scrubber not run at boot, or its record or pipefail moved",
    "r25_history": "a history other than 284 commits (265 / 12 / 7)",
    "r26_history_span": "a span other than 2026-07-25 to 2026-10-13",
    "r27_history_june": "a June count other than 284",
    "r28_history_backuptool": "a backuptool count other than 79",
    "r29_upstream_presence": "a slice file other than backuptool present upstream or in the base",
    "r30_upstream_backuptool": "upstream's backuptool not 68 lines, or base and upstream differing",
    "r31_upstream_diffstat": "a diffstat other than 14 files, +26 / -11,138",
    "r32_callers": "a caller count other than 19",
    "r33_install_lines": "the eleven scripts or the window not installed by rclone/package.mk",
    "r34_tools": "a tool that stopped naming the 14",
    "r35_t13_rows": "a count of T13's rows other than 5",
    "r36_back_up_words": "a count other than BACK UP 7, BACKUP 38",
    "r37_vocabulary_check": "a refusal without its CANNOT line (the run itself is stage-b/vocabulary-check.txt)",
    "r38_sourced": "a sourced file other than /etc/profile, 001-functions, cloud_content_transfer and the archive helper",
    "r39_removal_rule": "a change under packages/, projects/ or tools/ since the dispatch tip",
    "r40_branch_vs_read": "the branch differing from 8ebaf8daad on one of the 14",
}


def first_line(p):
    t = p.read_text().strip("\n").splitlines()
    head = (t[0] if t else "").replace("|", "\\|")[:90]
    more = f" (+{len(t) - 1} lines)" if len(t) > 1 else ""
    return f"`{head}`{more}" if head else "(empty)"


def runs():
    rows = [l.split("\t") for l in (A / "stage-a/out/runs.tsv").read_text().splitlines()[1:]]
    assert len(rows) == 40 and all(r[1] == "0" for r in rows), (len(rows), [r for r in rows if r[1] != "0"])
    out = ["| Run (`stage-a/runs.sh`) | Exit | Seconds | Started (UTC) | Figure (first line of `stage-a/out/<run>.out`) | A FAIL would mean |",
           "| --- | ---: | ---: | --- | --- | --- |"]
    for rid, rc, sec, start in rows:
        out.append(f"| `{rid}` | {rc} | {sec} | {start} | {first_line(A / f'stage-a/out/{rid}.out')} | {FAIL[rid]} |")
    return "\n".join(out)


def tools():
    rows = [l.split("\t") for l in (A / "stage-b/tools-out/tools.tsv").read_text().splitlines()[1:]]
    assert len(rows) == 5, len(rows)
    verdict = {
        "t1_cloud_connections_test": ("`Ran 26 tests` `OK`", "a connection transaction that installs credentials it did not verify, or leaves staging"),
        "t2_cloud_input_test": ("`Ran 9 tests` `OK`", "the phone page's ordering or the Wi-Fi selection broken"),
        "t3_validator_test": ("`CANNOT`: the test hard-codes `rclone v1.75.1`; the tree pins 1.75.2 (`rclone/package.mk:7`, `a0f60255ab`)", "-- (the run is refused by the test's own stale pin, not by the product)"),
        "t4_content_scope_test": ("19 PASS, 2 FAIL: `system-traversal-refused`, `content-pointer-traversal-refused` -- each test's refusal assertion passed (`:221`), then it read `ctl/argv`, which a refusal before any rclone call never creates", "a selected-library boundary crossed"),
        "t5_save_layout_test": ("`save-layout: 39 PASS, 0 FAIL`", "a save path carried by a content transfer"),
    }
    out = ["| Tool (`stage-b/tools.sh`) | Exit | Seconds | Started (UTC) | rclone it ran | Verdict | A FAIL would mean |",
           "| --- | ---: | ---: | --- | --- | --- | --- |"]
    for rid, rc, sec, start, rcl in rows:
        v, f = verdict[rid]
        out.append(f"| `{rid}` | {rc} | {sec} | {start} | {rcl} | {v} | {f} |")
    return "\n".join(out)


# --- writers ---------------------------------------------------------------------------
W = [
    # target, file, pattern, count, mode, lock, how, reached by
    ("`rclone.conf`", "connections", r"^def atomic\(path, data\):", 1, "0600 observed (`stage-b/fixture-mode.txt`: new, and over a 0644 file)", "the caller's", "temp (`mkstemp` beside it) + fsync + `os.replace` + directory fsync", "the one writer: every row below"),
    ("`rclone.conf`", "connections", r"atomic\(CONFIG, updated\)", 2, "0600 observed", "`/var/run/cloud_sync.lock` (flock)", "`atomic()`", "`save()` commit (`cloud_remote create`/`update` -> `connections.save`; `cloud_oauth` -> `connections.save`), `remove()`"),
    ("`rclone.conf`", "connections", r"atomic\(CONFIG, original\)", 2, "0600 observed", "flock", "`atomic()` (rollback)", "a failed publish or commit"),
    ("`rclone.conf`", "connections", r"CONFIG\.unlink\(\)", 1, "--", "flock", "unlink (rollback of a first connection)", "a failed first save"),
    ("staged `rclone.conf`", "connections", r"staged\.write_bytes\(original\)", 2, "0700 directory, 0600 file observed", "flock", "in a `TemporaryDirectory`; rclone writes it", "`save()`, `remove()`"),
    ("`active-connection`", "connections", r"atomic\(ACTIVE, ", 4, "0600 observed", "flock", "`atomic()`", "`save()` pin, `restore_selection()`, `select()`, `remove()` tombstone"),
    ("`active-connection`", "connections", r"ACTIVE\.unlink\(\)", 1, "--", "flock", "unlink + directory fsync", "`restore_selection()` with no previous selection"),
    ("`cloud_sync-device-id`", "device_id", r'> "\$\{ID_FILE\}\.tmp\.\$\$"', 1, "0644 observed", "none", "temp `.tmp.$$` + `mv -f`", "first run with an adapter; healing"),
    ("`cloud_sync-device-id.previous`", "device_id", r'>> "\$\{PREVIOUS_FILE\}"', 1, "0644 observed", "none", "append, then a positive `grep -qxF`", "`heal_poisoned()`"),
    ("`content-match-plan`", "restore", r"printf 'plan2 %s %s %s", 1, "by construction (umask: 0644)", "none for the preview; the apply holds the flock", "temp `.tmp.$$` + `mv -f`, context re-checked first", "`--match` (preview)"),
    ("`content-match-plan`", "restore", r'rm -f "\$\{MATCH_PLAN\}" 2>/dev/null', 2, "--", "the apply's flock (`:890`); none (`:911`)", "spent: removed, then checked absent (`:891`)", "`--match --apply` before any read; `--match` before a new preview"),
    ("`content-systems`", "restore", r'> "\$\{SELECTION\}\.tmp\.\$\$"', 1, "by construction (umask: 0644)", "none", "temp + `mv -f`; **the write is not checked** (F-10)", "`--set-systems`"),
    ("`last-content-*` stamps", "restore", r'tmp="\$\{file\}\.tmp\.\$\$"', 1, "by construction (umask: 0644)", "the run's flock", "temp + `mv -f`", "`record_outcome`, `stop_no_network`"),
    ("`last-content-backup` stamp", "backup", r'tmp="\$\{file\}\.tmp\.\$\$"', 1, "by construction (umask: 0644)", "the run's flock", "temp + `mv -f`", "`record_outcome`, `stop_no_network`"),
    ("OAuth `session.json`", "oauth", r"os\.replace\(tmp, path\)", 1, "0644 observed (holds the PIN, the URL with it, the provider link)", "`threading.Lock` + flock on `session.lock`", "temp `<path>.<pid>.tmp` + `os.replace`", "`write_state`, `write_owned`, `reset_state`, `_fail_owned`"),
    ("OAuth `session.lock`", "oauth", r'os\.open\(state_path\("session\.lock"\)', 1, "0600 observed", "--", "`O_CREAT` 0600", "`_state_locked()`"),
    ("OAuth markers", "oauth", r'open\(state_path\("(signed-in|open-browser|close-browser)"\), "w"\)', 3, "0644 observed", "none", "empty file", "`signed_in()`, `open`, `close`"),
    ("OAuth marker `phone-keyboard` (stage C, A-20)", "oauth", r'^\s+open\(marker, "w"\)\.close\(\)', 1, "0644 by construction (the same `open`)", "none", "empty file", "`open --phone`"),
    ("OAuth `window.log`", "oauth", r'self\.log_file = open\(self\.log_path, "w"\)', 1, "by construction (umask: 0644)", "none", "truncate; the window's stdout and stderr", "`BrowserSession.start()`"),
    ("OAuth page and field records", "window", r"g_file_set_contents\(", 2, "by construction (0666 & ~umask)", "none", "GLib's temp + rename", "the window's load (never a 127.0.0.1/localhost address, `:660-671`) and its field probe"),
    ("scan results", "scan", r'> "\$\{OUT\}/(scan|systems|state|started|archives|content-location)"', 6, "0644 by construction: the fixture observed a scan-style `>` write, not these statements (stage C, A-21)", "`/var/run/cloud_scan.lock` (flock)", "in place, after `rm -f` of the old set", "`cloud_scan`, `--content`, `--folder`"),
    ("scan results", "scan", r'\} > "\$\{OUT\}/settings"', 1, "0644 by construction (as above)", "flock", "in place", "`cloud_scan`"),
    ("scan completion", "scan", r'mv -f "\$\{tmp\}" "\$\{OUT\}/\$\{stamp\}"', 1, "by construction (umask: 0644)", "flock", "temp + `mv -f`, after the context re-check", "`write_completion`"),
    ("scrubber record `log-scrubbed`", "scrub", r'mv -f "\$\{STAMP\}\.tmp" "\$\{STAMP\}"', 1, "by construction (umask: 0644)", "none (once per boot, before the writers)", "temp + `mv -f`, other lines kept", "`record()`"),
    ("rewritten logs", "scrub", r'elif ! mv -f "\$\{tmp\}" "\$\{f\}"', 1, "the new file's (umask), not the old one's", "none", "temp `.scrub.$$` + `mv -f`, line-count parity first", "`scrub()`"),
    ("settings archive", "backuptool", r'to_log tar -czf "\$\{TARGET\}\.partial"', 1, "by construction (umask: 0644)", "flock on the backups folder", "`.partial`, listed back and counted, then `mv -f`", "`write_archive` (backup)"),
    ("settings archive", "backuptool", r'if ! mv -f "\$\{TARGET\}\.partial" "\$\{TARGET\}"', 1, "--", "flock", "the rename", "`write_archive`"),
    ("pre-restore copy", "backuptool", r'if ! tar -czf "\$\{TARGET\}\.partial" -C / -T "\$\{KEEP\}"', 1, "by construction", "flock", "`.partial`, counted, then `mv -f`", "`snapshot_members` (restore)"),
    ("restore mark", "backuptool", r'mv -fT "\$\{RESTORE_MARK\}\.tmp"', 1, "by construction", "flock", "temp + `mv -fT`, then read back (first line, last line, count)", "restore"),
    ("an upstream-era archive", "backuptool", r'mv -n "\$\{OLD\}" "\$\{DEST\}"', 1, "--", "flock", "`mv -n`, then a positive check", "backup"),
    ("the previous archive", "backuptool", r'mv "\$\{PREVIOUS\}" "\$\{ARCHIVEFOLDER\}/\$\{PREVIOUS_NAME\}"', 1, "--", "flock", "`mv`, **unchecked**", "backup's rotation"),
    ("`cloud_sync.conf`", "setup", r'> "\$\{tmp\}" && mv -f "\$\{tmp\}" "\$\{SYNC_CONF\}"', 1, "by construction (umask: 0644)", "**none**", "temp + `mv -f`, then every line checked", "`--set-saves-remote`, `--set-content-remote`, `--set-settings-remote`, `--use-content-root`"),
]


def writers():
    out = ["| Target | Statement | Mode it ends with | Lock held | How | Reached by |", "| --- | --- | --- | --- | --- | --- |"]
    for target, key, pat, n, mode, lock, how, reach in W:
        out.append(f"| {target} | {cite(key, pat, n)} | {mode} | {lock} | {how} | {reach} |")
    # cloud_setup writes no rclone.conf: its 'rclone config' lines are reads, a kill and echoes.
    cfg = [i + 1 for i, l in enumerate(lines("setup")) if "rclone config" in l and not l.lstrip().startswith("#")]
    assert cfg == [553, 651, 775, 938, 958, 972], cfg
    out.append("")
    out.append(f"**`cloud_setup` writes no `rclone.conf`.** Its six non-comment `rclone config` lines are two reads "
               f"(`cloud_setup:553` `config file`, `:651` `config show`, the `type` line only), the kill at `:775`, and three "
               f"echoed console instructions (`:938`, `:958`, `:972`). `cloud_remote`'s two `rclone(` calls are reads "
               f"({cite('remote', r'^def rclone\(', 1)} the helper, {cite('remote', r'rclone\(\"config\", \"providers\"\)', 1)}); "
               f"its write is {cite('remote', r'connections\.save\(name', 1)}. "
               f"The interface's connection pages reach `connections.save` by running `cloud_remote create`/`update` (ES, read by name only).")
    rows = len(W)
    # 31 at stage B; 32 since stage C added `cloud_oauth:2708`'s `phone-keyboard` marker (Astra's A-20).
    assert rows == 32, rows
    return "\n".join(out)


# --- secrets' paths -----------------------------------------------------------------------
S = [
    # kind, sink, (file, pattern, count) or None, mask, note
    ("provider token", "file: `rclone.conf`", ("connections", r"atomic\(CONFIG, updated\)", 2), "0600 (observed); not obscured by rclone (OAuth JSON)", "held back from every archive (`backuptool` DEVICEONLY, `:746-751`)"),
    ("provider token", "process argv (`/proc/<pid>/cmdline`)", ("oauth", r'\("token", self\.token\)', 1), "**none**", "on `rclone config create`'s argv for up to the 40 s `run()` bound and the `lsd` check (F-05)"),
    ("provider token", "`/var/log/cloud_sync.log`", ("oauth", r'log\("could not finish the sign-in: %s" % detail\)', 1), "fixed sentences only", "today's `detail` is a `Refused` sentence or `CLOSED_EARLY`; scrubber family F2 covers earlier builds"),
    ("provider token", "stderr", ("connections", r"Never forward provider diagnostics", 1), "discarded", "`run()` raises a fixed sentence; `read_config`'s dump never echoed (`:37-38`)"),
    ("provider token", "`/var/run/cloud_oauth/session.json`", None, "not written", "the state's fields are status, attempt, session, url, address, provider, pin, name, backend, error, remote"),
    ("provider token", "the per-session log (`window.log`)", None, "not written", "the window never sees the token"),
    ("provider token", "a settings archive", ("backuptool", r"rclone\.conf held back from the archive", 1), "held back; the credential scan refuses a staged token (exit 5)", "`credential_lines` `:431-459`"),
    ("provider token", "a packet", None, "never collected", "D-CLOUD-181; this audit's packet is scanned three ways at stage C"),
    ("provider token", "a screen", None, "not shown", "--"),
    ("OAuth code", "the sign-in window's page record", ("window", r"^static int page_worth_recording\(const char \*uri\)", 1), "excluded: a 127.0.0.1/localhost address is never recorded", "#308 claude F-RS-20"),
    ("OAuth code", "a loopback GET to rclone", ("oauth", r'urllib\.request\.urlopen\("%s/\?%s" % \(LOCAL_AUTH, query\)', 1), "loopback only", "the paste flow (`submit`)"),
    ("OAuth code", "the LAN (the paste flow's POST)", ("oauth", r'session\.submit\(fields\.get\("code"', 1), "**none**: plain HTTP on the LAN, behind the PIN", "only where the device has no browser stack"),
    ("OAuth code", "`/var/log/cloud_sync.log`, `session.json`, stderr", None, "not written", "--"),
    ("pin", "`session.json`", ("oauth", r"provider=holder\.session\.provider, pin=holder\.pin,", 1), "**none**; 0644 observed in a 0755 folder", "cleared by `cancel` (`reset_state`)"),
    ("pin", "stdout to the interface", ("oauth", r'print\("PIN=%s" % holder\.pin\)', 1), "none (by design: the handheld shows it)", "and `URL=` with it"),
    ("pin", "a screen (the handheld), the QR, the URL path", ("oauth", r'url = "%s/%s" % \(bare, holder\.pin\)', 1), "by design", "the URL travels plain HTTP on the LAN"),
    ("pin", "the phone page", ("oauth", r'var pin = "%\(pin\)s";', 1), "served only after the gate", "posted back on every request (`:1181`)"),
    ("pin", "`/var/log/cloud_sync.log`", None, "not written", "--"),
    ("typed WebDAV/SFTP secret", "process argv (`cloud_remote`, then `rclone`)", ("connections", r"args\.extend\('%s=%s' % pair for pair in settings\)", 1), "**none**", "two processes' argv for the create's duration (F-05)"),
    ("typed WebDAV/SFTP secret", "file: `rclone.conf`", ("connections", r"args \+= \['--non-interactive', '--obscure'\]", 1), "obscured by rclone (reversible), 0600", "--"),
    ("typed WebDAV/SFTP secret", "`/var/log/cloud_sync.log`", ("remote", r'log\("rclone %s failed \(%d\)" % \(verb, proc\.returncode\)\)', 1), "verb and code only", "scrubber family F1 covers earlier builds"),
    ("typed WebDAV/SFTP secret", "stderr", ("remote", r'expected key=value, got: %s', 1), "**none** for a malformed pair", "Info: a pair with no `=`"),
    ("sign-in page password", "the phone keyboard (LAN; stage C, R-2: the page the window shows, not a WebDAV/SFTP form)", ("oauth", r'log\("typed %d characters%s%s"', 1), "the log counts characters only; the LAN carries them plain (the page says so)", "masked box on the phone (`type=password`)"),
    ("sign-in page password", "the per-session log (`window.log`)", ("window", r'g_message\("key %s \(%u\)"', 1), "only under `CLOUD_SIGNIN_DEBUG`, which nothing sets; any value turns it on (A-37, R-32)", "Info (F-12)"),
    ("typed WebDAV/SFTP secret", "a screen (`cloud_setup`'s rclone stderr)", ("setup", r'probe=\$\(rclone lsd "\$\{remote\}\$\{path\}"', 1), "**none**: two lines of rclone's ERROR text shown", "F-07; nothing masks rclone's ERROR text, so a URL holding a secret would show (stage C, A-4)"),
    ("device id", "file: `cloud_sync-device-id`", ("device_id", r'> "\$\{ID_FILE\}\.tmp\.\$\$"', 1), "0644 observed", "held back from every archive"),
    ("device id", "cloud folder names, logs, stdout", ("device_id", r'printf .%s\|%s. "\$\{1\}" "\$\{DEVICE:-unknown\}" \| md5sum \| cut -c1-10', 1), "an unsalted md5 of the MAC, cut to 40 bits", "**recoverable by brute force** within an OUI (F-11)"),
    ("the root password", "a screen (the console setup flow)", ("setup", r'ROOTPASS=\$\(get_setting root\.password\)', 1), "**none**: shown in the clear", "the legacy SSH flow; `--info` prints `PASSWORD_SET` only (`:618`)"),
]


def secrets():
    out = ["| Credential | Sink | Where | Mask at that sink | Note |", "| --- | --- | --- | --- | --- |"]
    kinds = collections.Counter()
    for kind, sink, anc, mask, note in S:
        where = cite(*anc) if anc else "no line reaches it"
        out.append(f"| {kind} | {sink} | {where} | {mask} | {note} |")
        kinds[kind] += 1
    # "sign-in page password" since stage C (Argon's R-2): the phone keyboard types into the sign-in window.
    assert set(kinds) == {"provider token", "OAuth code", "pin", "typed WebDAV/SFTP secret", "sign-in page password", "device id", "the root password"}, kinds
    assert len(S) == 28, len(S)
    out += ["", "**The scrubber's three families** (`cloud_log_scrub:78-121`), the shapes earlier builds wrote, and whether a writer in the 14 writes each today:", "",
            "| Family | Shape | Rule | Writes it today |", "| --- | --- | --- | --- |",
            f"| F1 | `cloud_remote` failure lines with their arguments (`rclone config create <name> <type> k=v ... failed (<n>): <rclone's words>`) | {cite('scrub', r'^s/\^\(\.\*\\\[cloud_remote\\\] rclone config \[a-z\]\+\)', 1)} and the key masks | **no**: {cite('remote', r'log\(\"rclone %s failed \(%d\)\"', 1)} logs the verb and code |",
            f"| F2 | `cloud_oauth`'s `could not finish the sign-in: <rclone's words>` | {cite('scrub', r'could not finish the sign-in: \)\.\*', 1)} | **the shape yes, the words no**: {cite('oauth', r'log\(\"could not finish the sign-in: %s\" % detail\)', 1)} writes a fixed `Refused` sentence (`cloud_oauth:592-594`) |",
            f"| F3 | the interface's `cloud_remote create: <output>` record and its continuation lines in `es_log*.txt` | {cite('scrub', r'i = index\(\$0, \"cloud_remote create: \"\)', 1)} | **the shape yes, masked**: at the ES pin `16dbac5211`, `GuiMenu.cpp:7414` logs `cloud_remote create: ` + `Utils::String::maskSecrets(out)` (`stage-b/es-cloud-remote-log.txt`; masked since ES `731252c61`, the scrubber's comment); what the mask catches is the ES slice's |"]
    return "\n".join(out)


# --- deletions -------------------------------------------------------------------------------
def deletions():
    out = ["| Statement | Verb | Bound | Reached when |", "| --- | --- | --- | --- |"]
    rm = []
    for key in F:
        for i, l in enumerate(lines(key)):
            if "rm -rf" in l and not l.lstrip().startswith("#"):
                rm.append((key, i + 1, l))
    assert len(rm) == 12, len(rm)
    bound = {
        ("backuptool", 224): ("`/storage/.cache/backuptool-staging.`* (`:762`)", "every backup and restore, under the folder's flock (`sweep_leftovers`)"),
        ("backuptool", 227): ("this run's `${STAGING}`, when set", "the EXIT trap"),
    }
    for key, n, l in rm:
        b, w = bound.get((key, n), ("this run's `${STAGING}` (`mktemp -d` under the prefix, `:1161`)" if key == "backuptool" else
                                    "this call's `mktemp -d` fifo directory" if key == "transfer" else "the scan's `mktemp -d`",
                                    "a failed step of `write_archive` or its end" if key == "backuptool" else
                                    "`bounded_content_rclone`'s cleanup trap" if key == "transfer" else "`--scan`'s EXIT trap"))
        out.append(f"| `{short(key)}:{n}` | `rm -rf` | {b} | {w} |")
    deleting = [("restore", r"rclone delete \"\$\{DEST\}/\$\{sys\}\"", "`rclone delete`", "`--max-delete` the preview's count; the save, conflict, metadata (and n64 state) excludes; local only", "`--match --apply`, verb `remove`, only after the spent plan, the context and mode check, a populated root, and the per-system verb and count check (`:885-980`)"),
                ("restore", r"bounded_content_rclone sync \"\$\{src\}\" \"\$\{local_dir\}\"", "`sync --dry-run`", "deletes nothing (`--dry-run`)", "every preview and apply (`match_plan_one`)"),
                ("restore", r"bounded_content_rclone sync \"\$\(remote_for", "`sync`", "`--max-delete` the preview's count; the excludes; the inactivity bound; **and whatever `RCLONE_NET_OPTS` adds** (F-02)", "`--match --apply`, verb `sync`, under the same refusals")]
    for key, pat, verb, b, w in deleting:
        out.append(f"| {cite(key, pat, 1)} | {verb} | {b} | {w} |")
    for key in F:
        for i, l in enumerate(lines(key)):
            if re.search(r"rclone (move|purge|rmdir)|bounded_content_rclone (move|purge|delete)", l) and not l.lstrip().startswith("#"):
                sys.exit(f"t17-tables: an unlisted deleting statement at {short(key)}:{i + 1}")
    de = [(key, i + 1) for key in F for i, l in enumerate(lines(key)) if "--delete-excluded" in l]
    assert de == [("restore", 528)], de
    assert lines("restore")[527].lstrip().startswith("#"), lines("restore")[527]
    out += ["", "**`rclone move`, `purge` and `rmdir`: 0 in the 14.** **`--delete-excluded`: 0 in code**; its one occurrence is the comment at `cloud_content_restore:528`. But no statement strips it from `RCLONE_NET_OPTS`, which reaches the deleting `sync` (F-02).",
            "",
            "**The refusals before the two deleting statements** (`cloud_content_restore`, quoted):", ""]
    for pat, what in ((r"if \[ -s \"\$\{MATCH_PLAN\}\" \] && head -1", "a `plan2` header with a 64-hex context and a mode"),
                      (r'rm -f "\$\{MATCH_PLAN\}" 2>/dev/null', "the plan spent before anything is read"),
                      (r'echo "Nothing was removed: something went wrong on this device', "refused if it could not be spent"),
                      (r'echo "Nothing was removed: your cloud settings changed', "the context or mode drifted: `SOMETHING CHANGED SINCE YOU CHECKED`"),
                      (r'echo "Nothing was removed: check what would change first', "no plan: `CHECK WHAT WOULD CHANGE FIRST`"),
                      (r'echo "Refusing to change anything: your cloud', "an empty or unreadable cloud root"),
                      (r'echo "Nothing was removed from \$\{sys\}: it changed since you checked', "a verb changed, or more to remove than the preview counted")):
        hits = [i + 1 for i, l in enumerate(lines("restore")) if re.search(pat, l)]
        n = hits[0] if pat != r'rm -f "\$\{MATCH_PLAN\}" 2>/dev/null' else hits[0]
        assert hits, pat
        out.append(f"- `cloud_content_restore:{n}` -- {what}.")
    return "\n".join(out)


SECTIONS = {"coverage": coverage, "runs": runs, "tools": tools, "writers": writers, "secrets": secrets, "deletions": deletions}


def render(text):
    for name, fn in SECTIONS.items():
        b, e = f"<!-- begin t17:{name} -->", f"<!-- end t17:{name} -->"
        if b not in text:
            sys.exit(f"t17-tables: no {b} in the file")
        pre, rest = text.split(b, 1); _, post = rest.split(e, 1)
        text = pre + b + "\n" + fn() + "\n" + e + post
    return text


if __name__ == "__main__":
    mode, path = sys.argv[1], Path(sys.argv[2])
    old = path.read_text(); new = render(old)
    if mode == "write":
        path.write_text(new); print(f"t17-tables: wrote {path}")
    elif mode == "check":
        print(f"t17-tables: check {'same' if new == old else 'DIFFERS'} {path}"); sys.exit(0 if new == old else 1)
