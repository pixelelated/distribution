# Second opinion (Phase 4.6), M6 T17: cloud setup, sign-in, connections, content and settings backups in pixelelated/distribution

You are one of two independent reviewers for a read-only renovation audit of 14 files at commit `8ebaf8daad`, read under a **security lens**. The audit is deep because these files preserve a person's state. The 14 files are 11,180 lines, all of them shipped:
- the rclone package's cloud scripts: `cloud_connections.py`, `cloud_remote`, `cloud_oauth`, `cloud_setup`, `cloud_scan`, `cloud_folder_validate`, `cloud_device_id`, `cloud_log_scrub`, `cloud_content_backup`, `cloud_content_restore` and `cloud_content_transfer`;
- the sign-in window (`cloud-signin-window.c` and its `package.mk`);
- the settings archive tool `backuptool`.

The fork wrote thirteen of them. `backuptool` is upstream's, rewritten.

- **What ships.** The product is an immutable handheld OS. A person updates it in place and keeps `/storage`.
  - These scripts link a cloud provider, pair a phone over the LAN to type a secret, back up and restore ROMs, BIOS and game content, and archive settings.
  - The scripts run under busybox `ash`/`bash` and python 3, with rclone 1.75.2.
  - One player uses one console at a time.
- **What you get.**
  - The first reader is another lab's model. You get its `02-forward-audit.md` (whole, with its generated tables), `03-retrospective.md` and `04-analysis.md`.
  - Then four context sections: the order's entry, the brief's questions, the register rows, and the interface's why table.
  - Then four of the 14 whole and line-numbered: `package.mk`, `cloud_connections.py` (the one writer of `rclone.conf`), `cloud_remote` and `cloud_content_transfer`.
  - Then **line-numbered excerpts** of the other ten (`cloud_oauth`, `cloud_content_restore`, `backuptool`, `cloud_setup`, `cloud_content_backup`, `cloud-signin-window.c`, `cloud_device_id`, `cloud_folder_validate`, `cloud_log_scrub`, `cloud_scan`). Each excerpt covers every line the analyses or the brief cite, with eight lines of context.
  - Then the four host fixtures the first reader wrote, as their docstrings, with their outputs.
  - **When a claim needs lines outside an excerpt, say `outside the packet` and do not guess.**
- **Masking.**
  - Every section was passed through a mask that replaces a value after `key=`, `key:`, `token=`, `user=`, `pass...=` or `psk=` with `***`. A `***` is the mask, not the code.
  - The packet was scanned for credential shapes before it left. No hit was a value.
- **Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. Its line numbers are `8ebaf8daad`'s.
- **Nothing can be run for you.** A fixture's output is what was observed on the host, with the substitutes it names. A guest repeat of the fixtures is planned.

Answer these first, in this order:

1. **Where a secret can travel (`02` § The secrets' paths; F-05, F-07, F-09, F-11, F-12).**
   - The credential kinds are a provider's token in `rclone.conf`, the OAuth code in the redirect, the pin, a WebDAV or SFTP secret typed on the phone page, and the device id.
   - Is every sink each one reaches named, with what masks it there? The sinks are the file and its mode, `/var/log/cloud_sync.log`, stderr, `/var/run/cloud_oauth/session.json`, a process's argv, the sign-in window's log, and a screen.
   - Is any row wrong?
   - Does any writer in these 14 still write one of the shapes `cloud_log_scrub` removes?
2. **What the deleting path can delete (`02` § The deletions; F-02).**
   - Are the two deleting statements in `cloud_content_restore` (`:1015`, `:1046`) reachable only under `--match --apply` with a spent plan and the preview's counts?
   - Is F-02 right? `RCLONE_NET_OPTS` is read at `:235-279` with no filter and reaches the `sync` at `:1046`, so a `--delete-excluded` there deletes what the plan excluded.
   - What else can that variable carry to that statement?
   - Can `bounded_content_rclone` (`cloud_content_transfer:85-158`) be handed a verb or a flag from input?
   - Do the `rm -rf` sites and the `pkill -f` patterns reach outside their own work?
3. **The phone page (F-01, F-09).**
   - Is F-01 right? `cloud_oauth:2330-2344`'s `_supplied()` takes a request's first path segment as the pin. The serve counts each wrong pin, so a browser's unasked `/favicon.ico` or touch-icon requests can lock the right pin out with a 403 for the rest of the serve.
   - What bounds guessing the four-digit pin?
   - What does the page serve to an unauthenticated request?
   - Is the paste flow's raw-HTML render of rclone's words (F-09) reachable with attacker-chosen text?
4. **What the content backup takes (F-03).** `cloud_content_backup:583-585` accepts a system name the restore would refuse (`cloud_content_restore:1482-1487`). What can a name like `../.config` copy, from where and to where? Is anything else in the backup path taken from input unchecked?
5. **The writers (`02` § The writers, 31 rows; F-06, F-08, F-10).**
   - Is each row's mode, lock and atomicity right?
   - Is `cloud_connections.atomic()` the only writer of `rclone.conf`, and does every path reach it?
   - What does a kill at each step leave?
   - Are `backuptool`'s archive write and its restore's mark-and-revert as sound as `03` § 3.1 says?

Then:

6. **Refute or confirm each finding F-01 to F-19** in `02` § Findings: *confirmed*, *narrowed* (say how), or *refuted* (with the line). For F-01, F-02 and F-03, also judge the severity, the fix the first reader proposes, and its `Already written:` line: what the code before a fix has already left on devices and in their clouds.
7. **What the first reader missed:**
   - a defect in the excerpts or the whole files: an unchecked write, a pipeline judged by its last stage, an unquoted expansion feeding a command, a fail-open temp, a probe that cannot report absence, or success recorded from an exit status rather than the artifact;
   - a secret's path it did not name;
   - a disposition that should be different.

**Output:**
- Numbered items `A-1`, `A-2`, ..., grouped under the seven headings above.
- Each item gets one line saying *confirmed / narrowed / refuted / new*, then the `file:line` evidence, then two to five sentences.
- Do not restate the packet, and do not reproduce long code.
- Keep the whole reply under about 8,000 words.


## The first reader's 02-forward-audit.md (whole)

# Forward audit — M6.P2 T17, cloud setup, sign-in, connections, content and settings backups (#664)

## Running notes

- **What this is.** A read slice at Extended depth over the 14 files the cloud's setup, sign-in, connections, content and settings archives run on. 11,180 lines, all fork-own, all shipped. Thirteen exist nowhere upstream; `backuptool` is the fork's 1,899-line rewrite of an identical 68-line upstream script. **The lens is security; the depth reason is state preservation.**
- **The read.** The bytes are `8ebaf8daad`'s, and the branch differs from them on none of the 14 (r40, `xargs -0`). Every line of the 14 was read; `stage-b/read-notes.md` is the reading record, one section per file. Upstream `651150fc88` is read locally by name. No fetch. Nothing under `packages/`, `projects/` or `tools/` changes at stages A to D (r39).
- **The bench.** *Can this be done on the VM? Yes -- the host first, then one guest after two other windows.*
  - The host ran the five fork tools (two with its own rclone 1.60.1-DEV, as `tools/cloud-connections-test` hard-codes; three given M6's donor rclone 1.75.2) and four of the lane's fixtures, with no network beyond loopback.
  - The fixtures run the product's own code: the real `cloud_oauth` handler over loopback; the real content scripts under the donor's busybox applets with their absolute paths rewritten into a scratch root; `backuptool`'s own `foreign_member()` and the image's busybox `tar`; the real writers for their modes.
  - The guest window is asked for after this stage (§ The guest cycle). **No guest ran; nothing ran on a person's device or cloud.**
- **The read filter.** Counts of the credential words are taken unfiltered; every line printed into a run's output passes the filter or the mask. No credential-shaped value is quoted here; a finding names file:line and the shape.
- **The tables** in § Coverage, § The runs, § The writers, § The secrets' paths and § The deletions are generated by `tools/t17-tables.py`. Every row is anchored by a pattern that must match the asserted number of lines at `8ebaf8daad`, and `check` exits 1 when a table differs from a fresh run.

## Deltas from the brief

1. **15 `.$$` lines in the 14, not 14** (r16): `cloud_content_restore:819` opens the plan's temp write on its own line.
2. **`backuptool:224` sweeps `"${STAGING_PREFIX}"*`**, the script's own `/storage/.cache/backuptool-staging.` prefix (`:762`), not `${STAGING}`.
3. **The exit-constant run reads the whole directory** and prints T16's four constants too; within the 14 they are as written.
4. **`tools/vocabulary-check` ran** against the ES checkout at the pin, after the coordinator's word (exit 0, 163 judged, 0 wrong; `stage-b/vocabulary-check.txt`). The brief expected `CANNOT`.
5. **Two of the five tools could not give a clean verdict, for reasons of their own** (§ The host tools): `pixelelated-cloud-validator-test` hard-codes `rclone v1.75.1` while the tree pins 1.75.2, and `pixelelated-content-scope-test` fails two cases whose refusal it had just confirmed.
6. **The "symlink never extracted" proof** the brief puts on the guest is answered on the host by the image's own busybox `tar` (F-04): it defers an absolute-target link and fails the extraction. The guest repeats it through a full `backuptool restore`.

## § The runs

The brief's § 5 commands, from `stage-a/runs.sh`, with each exit, wall time, figure and what a FAIL would mean. **All 40 exit 0.**

<!-- begin t17:runs -->
| Run (`stage-a/runs.sh`) | Exit | Seconds | Started (UTC) | Figure (first line of `stage-a/out/<run>.out`) | A FAIL would mean |
| --- | ---: | ---: | --- | --- | --- |
| `r01_block` | 0 | 0.70 | 06:13:48 | `paths 14 lines 11180 {'shipped': 14} {'fork-own': 14}` (+17 lines) | a membership other than 14 paths and 11,180 lines, or a tier or reach other than fork-own and shipped |
| `r02_modes` | 0 | 0.01 | 06:13:48 | `      4 100644` (+1 lines) | a mode other than 10 x 100755 and 4 x 100644 |
| `r03_lines` | 0 | 0.03 | 06:13:48 | `    27 projects/ROCKNIX/packages/network/cloud-signin-window/package.mk` (+14 lines) | a line total other than 11,180 |
| `r04_shell_functions` | 0 | 0.03 | 06:13:48 | `cloud_content_backup strict 17 loose 22` (+7 lines) | a function count other than 112 strict / 147 loose |
| `r05_python_defs` | 0 | 0.02 | 06:13:48 | `cloud_oauth 89 defs 7 classes` (+3 lines) | a def or class count other than 124 / 9 |
| `r06_set_discipline` | 0 | 0.01 | 06:13:48 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_log_scrub:63:set -o pipefail` (+5 lines) | a global set -e or -u, or pipefail somewhere new, or an eval in code |
| `r07_exit_constants` | 0 | 0.01 | 06:13:48 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_backup:20:readonly EXIT_LOCK_HELD=7` (+6 lines) | an exit constant other than 75 and 69 in the 14 |
| `r08_writer_rclone_conf` | 0 | 0.01 | 06:13:48 | `projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c:657: *` (+13 lines) | an rclone.conf writer other than cloud_connections.py |
| `r09_setup_remote_config` | 0 | 0.01 | 06:13:48 | `553:    config_file=$(timeout 3 rclone config file 2>/dev/null \| tail -1)` (+16 lines) | an `rclone config` write in cloud_setup, or cloud_remote writing other than through connections.save |
| `r10_deleting_statements` | 0 | 0.01 | 06:13:48 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore:750:        out=$(b` (+2 lines) | a deleting statement other than restore :750 (dry run), :1015 and :1046 |
| `r11_delete_excluded` | 0 | 0.01 | 06:13:48 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore:528:#  1. --delete-` | --delete-excluded anywhere but the comment at restore :528 |
| `r12_rm_rf` | 0 | 0.01 | 06:13:48 | `12` (+12 lines) | an rm -rf count other than 12, or one on something other than a script's own temporary |
| `r13_match_refusals` | 0 | 0.00 | 06:13:48 | `        if [ -s "${MATCH_PLAN}" ] && head -1 "${MATCH_PLAN}" \| grep -qE '^plan2 [0-9]+ [0` (+14 lines) | a refusal line missing before the deleting sync |
| `r14_pattern_kills` | 0 | 0.01 | 06:13:48 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth:357:        subprocess.run(["` (+4 lines) | a pattern kill other than setup :775-776 and oauth :357, :2819 |
| `r15_unquoted` | 0 | 0.01 | 06:13:48 | `projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup:40:    echo "[$(date` (+4 lines) | an unquoted expansion other than the five constants |
| `r16_dollar_dollar` | 0 | 0.01 | 06:13:48 | `15` (+15 lines) | a `.$$` name other than the 15 listed |
| `r17_oauth_bounds` | 0 | 0.00 | 06:13:48 | `72:STATE_DIR = "/var/run/cloud_oauth"` (+19 lines) | a changed OAuth constant or bound |
| `r18_backuptool_lists` | 0 | 0.00 | 06:13:48 | `    /storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat  # cheevos_ppsspp.sh` (+17 lines) | a held-back list other than DEVICEONLYDIRS and DEVICEONLY as read |
| `r19_backuptool_shape` | 0 | 0.00 | 06:13:48 | `93:stamp_at() {` (+42 lines) | ARCHIVE_KEEP, the 5) arm or the .partial writes moved |
| `r20_backuptool_logger` | 0 | 0.00 | 06:13:48 | `37` | a logger -t backuptool count other than 37 |
| `r21_device_id` | 0 | 0.00 | 06:13:48 | `ID_FILE="/storage/.config/cloud_sync-device-id"` (+8 lines) | a changed id derivation or write |
| `r22_validate_bounds` | 0 | 0.00 | 06:13:49 | `22:MAX_BYTES = 2 * 1024 * 1024` (+10 lines) | a changed validator bound or stderr handling |
| `r23_scan_routing` | 0 | 0.00 | 06:13:49 | `readonly EXIT_NO_NETWORK=69` (+17 lines) | a changed stop_on |
| `r24_scrub_hook` | 0 | 0.01 | 06:13:49 | `projects/ROCKNIX/packages/network/rclone/autostart/102-cloud-saves:29:[ -x /usr/bin/cloud_` (+4 lines) | the scrubber not run at boot, or its record or pipefail moved |
| `r25_history` | 0 | 0.04 | 06:13:49 | `284` (+3 lines) | a history other than 284 commits (265 / 12 / 7) |
| `r26_history_span` | 0 | 0.03 | 06:13:49 | `2026-07-25` (+1 lines) | a span other than 2026-07-25 to 2026-10-13 |
| `r27_history_june` | 0 | 0.03 | 06:13:49 | `284` | a June count other than 284 |
| `r28_history_backuptool` | 0 | 0.02 | 06:13:49 | `79` | a backuptool count other than 79 |
| `r29_upstream_presence` | 0 | 0.01 | 06:13:49 | `      2 projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool` | a slice file other than backuptool present upstream or in the base |
| `r30_upstream_backuptool` | 0 | 0.01 | 06:13:49 | `68` (+1 lines) | upstream's backuptool not 68 lines, or base and upstream differing |
| `r31_upstream_diffstat` | 0 | 0.01 | 06:13:49 | ` 14 files changed, 26 insertions(+), 11138 deletions(-)` | a diffstat other than 14 files, +26 / -11,138 |
| `r32_callers` | 0 | 1.44 | 06:13:49 | `19` (+19 lines) | a caller count other than 19 |
| `r33_install_lines` | 0 | 0.01 | 06:13:50 | `projects/ROCKNIX/packages/network/rclone/package.mk:22:                    webkitgtk cloud` (+22 lines) | the eleven scripts or the window not installed by rclone/package.mk |
| `r34_tools` | 0 | 0.03 | 06:13:50 | `cloud-connections-test 3` (+10 lines) | a tool that stopped naming the 14 |
| `r35_t13_rows` | 0 | 0.01 | 06:13:50 | `5` | a count of T13's rows other than 5 |
| `r36_back_up_words` | 0 | 0.01 | 06:13:50 | `      7 BACK UP` (+1 lines) | a count other than BACK UP 7, BACKUP 38 |
| `r37_vocabulary_check` | 0 | 0.00 | 06:13:50 | `6:  ./tools/vocabulary-check [--es <emulationstation checkout>] [--scripts <dir>] [--show]` (+8 lines) | a refusal without its CANNOT line (the run itself is stage-b/vocabulary-check.txt) |
| `r38_sourced` | 0 | 0.02 | 06:13:50 | `cloud_content_backup: 21:. /etc/profile 234:. "$(dirname "${BASH_SOURCE[0]}")/cloud_conten` (+7 lines) | a sourced file other than /etc/profile, 001-functions, cloud_content_transfer and the archive helper |
| `r39_removal_rule` | 0 | 0.00 | 06:13:50 | `[]` | a change under packages/, projects/ or tools/ since the dispatch tip |
| `r40_branch_vs_read` | 0 | 0.01 | 06:13:50 | `[]` | the branch differing from 8ebaf8daad on one of the 14 |
<!-- end t17:runs -->

### § The host tools

The five fork tools that exercise the 14, from `stage-b/tools.sh`, each with the rclone it ran. The outputs, masked, are in `stage-b/tools-out/`.

<!-- begin t17:tools -->
| Tool (`stage-b/tools.sh`) | Exit | Seconds | Started (UTC) | rclone it ran | Verdict | A FAIL would mean |
| --- | ---: | ---: | --- | --- | --- | --- |
| `t1_cloud_connections_test` | 0 | 2.0 | 06:25:41 | host /usr/bin/rclone rclone v1.60.1-DEV | `Ran 26 tests` `OK` | a connection transaction that installs credentials it did not verify, or leaves staging |
| `t2_cloud_input_test` | 0 | 1.0 | 06:25:43 | host /usr/bin/rclone rclone v1.60.1-DEV (not used: wifictl/phone JS) | `Ran 9 tests` `OK` | the phone page's ordering or the Wi-Fi selection broken |
| `t3_validator_test` | 1 | 0.1 | 06:25:44 | donor /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone rclone v1.75.2 | `CANNOT`: the test hard-codes `rclone v1.75.1`; the tree pins 1.75.2 (`rclone/package.mk:7`, `a0f60255ab`) | -- (the run is refused by the test's own stale pin, not by the product) |
| `t4_content_scope_test` | 1 | 3.5 | 06:25:44 | donor /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone rclone v1.75.2 | 19 PASS, 2 FAIL: `system-traversal-refused`, `content-pointer-traversal-refused` -- each test's refusal assertion passed (`:221`), then it read `ctl/argv`, which a refusal before any rclone call never creates | a selected-library boundary crossed |
| `t5_save_layout_test` | 0 | 29.6 | 06:25:47 | donor /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone rclone v1.75.2 | `save-layout: 39 PASS, 0 FAIL` | a save path carried by a content transfer |
<!-- end t17:tools -->

- **`tools/cloud-connections-test`'s 26 are host verdicts** (rclone 1.60.1-DEV against the image's 1.75.2; T13's Q2 note) until the guest repeats them.
- **The two content-scope FAILs are the test's.** Each case asserts the refusal first (`pixelelated-content-scope-test:221`, which passed) and then reads the stub's argv file, which a run refused before its first rclone call never writes. The product refused as it should; the test is a lead for its owner (F-13).
- **The validator test refuses the tree's own rclone.** It requires `rclone v1.75.1` (`:58`); `rclone/package.mk:7` pins 1.75.2 since `a0f60255ab`. Its verdict is `CANNOT` until the test follows the pin (F-13).

### § The fixtures

The lane's four, under `tools/`, each run with `--expect` where it can fail; outputs in `stage-b/fixture-*.txt`.

| Fixture | What it runs | Verdict at `8ebaf8daad` |
| --- | --- | --- |
| `t17-pin-fixture.py` | the real `cloud_oauth` `SessionHolder` and `make_server()` on 127.0.0.1, real HTTP | `--expect unfixed` met: ten icon requests spend the ten PIN attempts and the right PIN then gets 403; nine leave it working; a decoded non-ASCII PIN raises `TypeError` in the handler (F-01, F-09) |
| `t17-archive-fixture.py` | `backuptool`'s own `foreign_member()` and the image's busybox `tar` | a symlink member with an absolute target is **accepted** by `foreign_member` and **refused** by busybox `tar` (rc 1, nothing outside the root); a `storage/../` member is refused by `foreign_member` (F-04) |
| `t17-content-fixture.py` | the real content scripts under the donor's busybox, a stub rclone recording argv, and the donor's real rclone over a local-backend cloud | `--expect unfixed` met: `cloud_content_backup '../.config'` copies from `/storage/roms/../.config` (F-03); `--delete-excluded` in `RCLONE_NET_OPTS` reaches the deleting `sync`, and with the real rclone the apply **deletes the save `a.srm`** (F-02) |
| `t17-mode-fixture.py` | the real writers under umask 022 | `rclone.conf` and `active-connection` 0600 (also over a 0644 file); staging 0700/0600, nothing left after a refusal; `session.json` 0644 in a 0755 folder; `session.lock` 0600; the device id 0644 |

## Coverage

One row per path of the 14, every one read whole.

<!-- begin t17:coverage -->
| Path | Lines | Read | What it is | Findings |
| --- | ---: | --- | --- | --- |
| `projects/ROCKNIX/packages/network/cloud-signin-window/package.mk` | 27 | whole | the window's recipe; read whole | F-19 |
| `projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c` | 1,052 | whole | the WebKit window and its navigation policy; read whole | F-12 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_connections.py` | 258 | whole | the one writer of `rclone.conf` and `active-connection`; read whole | F-05, F-06, F-15 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup` | 799 | whole | content backup, copy only; read whole | F-03 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore` | 1,589 | whole | content restore and the only deleting path (`--match --apply`); read whole | F-02, F-08, F-10 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_content_transfer` | 158 | whole | the bounded rclone wrapper (sourced); read whole | F-02 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_device_id` | 401 | whole | this device's cloud name; read whole | F-11 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_folder_validate` | 278 | whole | the bounded category validator; read whole | F-13 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_log_scrub` | 206 | whole | the one-time log scrub; read whole | -- (§ The secrets' paths) |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth` | 2,830 | whole | sign-in broker, phone page, state; read whole | F-01, F-05, F-09 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_remote` | 345 | whole | providers, fields, create/update, active; read whole | F-05, F-07 |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_scan` | 362 | whole | the read-only opening scan; read whole | -- |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_setup` | 976 | whole | folders, markers, validation context, console flow; read whole | F-07, F-10, F-14 |
| `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool` | 1,899 | whole | the settings archive; read whole | F-04, F-10, F-16 |
<!-- end t17:coverage -->

## § The writers

One row per writing statement of `rclone.conf`, `active-connection`, `cloud_sync-device-id`, the match plan, the OAuth state, the scan results, the scrubber's record and an archive, with the stamps and `cloud_sync.conf` beside them. "Observed" is `stage-b/fixture-mode.txt` (host python and the donor's busybox, umask 022); the guest repeats it under the image's python.

<!-- begin t17:writers -->
| Target | Statement | Mode it ends with | Lock held | How | Reached by |
| --- | --- | --- | --- | --- | --- |
| `rclone.conf` | `cloud_connections.py:72` | 0600 observed (`stage-b/fixture-mode.txt`: new, and over a 0644 file) | the caller's | temp (`mkstemp` beside it) + fsync + `os.replace` + directory fsync | the one writer: every row below |
| `rclone.conf` | `cloud_connections.py:198`, `cloud_connections.py:253` | 0600 observed | `/var/run/cloud_sync.lock` (flock) | `atomic()` | `save()` commit (`cloud_remote create`/`update` -> `connections.save`; `cloud_oauth` -> `connections.save`), `remove()` |
| `rclone.conf` | `cloud_connections.py:210`, `cloud_connections.py:256` | 0600 observed | flock | `atomic()` (rollback) | a failed publish or commit |
| `rclone.conf` | `cloud_connections.py:212` | -- | flock | unlink (rollback of a first connection) | a failed first save |
| staged `rclone.conf` | `cloud_connections.py:159`, `cloud_connections.py:240` | 0700 directory, 0600 file observed | flock | in a `TemporaryDirectory`; rclone writes it | `save()`, `remove()` |
| `active-connection` | `cloud_connections.py:96`, `cloud_connections.py:197`, `cloud_connections.py:224`, `cloud_connections.py:252` | 0600 observed | flock | `atomic()` | `save()` pin, `restore_selection()`, `select()`, `remove()` tombstone |
| `active-connection` | `cloud_connections.py:98` | -- | flock | unlink + directory fsync | `restore_selection()` with no previous selection |
| `cloud_sync-device-id` | `cloud_device_id:290` | 0644 observed | none | temp `.tmp.$$` + `mv -f` | first run with an adapter; healing |
| `cloud_sync-device-id.previous` | `cloud_device_id:301` | 0644 observed | none | append, then a positive `grep -qxF` | `heal_poisoned()` |
| `content-match-plan` | `cloud_content_restore:819` | by construction (umask: 0644) | none for the preview; the apply holds the flock | temp `.tmp.$$` + `mv -f`, context re-checked first | `--match` (preview) |
| `content-match-plan` | `cloud_content_restore:890`, `cloud_content_restore:911` | -- | the apply's flock (`:890`); none (`:911`) | spent: removed, then checked absent (`:891`) | `--match --apply` before any read; `--match` before a new preview |
| `content-systems` | `cloud_content_restore:1405` | by construction (umask: 0644) | none | temp + `mv -f`; **the write is not checked** (F-10) | `--set-systems` |
| `last-content-*` stamps | `cloud_content_restore:299` | by construction (umask: 0644) | the run's flock | temp + `mv -f` | `record_outcome`, `stop_no_network` |
| `last-content-backup` stamp | `cloud_content_backup:252` | by construction (umask: 0644) | the run's flock | temp + `mv -f` | `record_outcome`, `stop_no_network` |
| OAuth `session.json` | `cloud_oauth:193` | 0644 observed (holds the PIN, the URL with it, the provider link) | `threading.Lock` + flock on `session.lock` | temp `<path>.<pid>.tmp` + `os.replace` | `write_state`, `write_owned`, `reset_state`, `_fail_owned` |
| OAuth `session.lock` | `cloud_oauth:179` | 0600 observed | -- | `O_CREAT` 0600 | `_state_locked()` |
| OAuth markers | `cloud_oauth:2134`, `cloud_oauth:2715`, `cloud_oauth:2754` | 0644 observed | none | empty file | `signed_in()`, `open`, `close` |
| OAuth `window.log` | `cloud_oauth:915` | by construction (umask: 0644) | none | truncate; the window's stdout and stderr | `BrowserSession.start()` |
| OAuth page and field records | `cloud-signin-window.c:408`, `cloud-signin-window.c:726` | by construction (0666 & ~umask) | none | GLib's temp + rename | the window's load (never a 127.0.0.1/localhost address, `:660-671`) and its field probe |
| scan results | `cloud_scan:276`, `cloud_scan:279`, `cloud_scan:294`, `cloud_scan:315`, `cloud_scan:332`, `cloud_scan:350` | 0644 observed (a `>` write) | `/var/run/cloud_scan.lock` (flock) | in place, after `rm -f` of the old set | `cloud_scan`, `--content`, `--folder` |
| scan results | `cloud_scan:344` | 0644 observed | flock | in place | `cloud_scan` |
| scan completion | `cloud_scan:229` | by construction (umask: 0644) | flock | temp + `mv -f`, after the context re-check | `write_completion` |
| scrubber record `log-scrubbed` | `cloud_log_scrub:185` | by construction (umask: 0644) | none (once per boot, before the writers) | temp + `mv -f`, other lines kept | `record()` |
| rewritten logs | `cloud_log_scrub:155` | the new file's (umask), not the old one's | none | temp `.scrub.$$` + `mv -f`, line-count parity first | `scrub()` |
| settings archive | `backuptool:1325` | by construction (umask: 0644) | flock on the backups folder | `.partial`, listed back and counted, then `mv -f` | `write_archive` (backup) |
| settings archive | `backuptool:1342` | -- | flock | the rename | `write_archive` |
| pre-restore copy | `backuptool:649` | by construction | flock | `.partial`, counted, then `mv -f` | `snapshot_members` (restore) |
| restore mark | `backuptool:1611` | by construction | flock | temp + `mv -fT`, then read back (first line, last line, count) | restore |
| an upstream-era archive | `backuptool:1822` | -- | flock | `mv -n`, then a positive check | backup |
| the previous archive | `backuptool:1885` | -- | flock | `mv`, **unchecked** | backup's rotation |
| `cloud_sync.conf` | `cloud_setup:101` | by construction (umask: 0644) | **none** | temp + `mv -f`, then every line checked | `--set-saves-remote`, `--set-content-remote`, `--set-settings-remote`, `--use-content-root` |

**`cloud_setup` writes no `rclone.conf`.** Its six non-comment `rclone config` lines are two reads (`cloud_setup:553` `config file`, `:651` `config show`, the `type` line only), the kill at `:775`, and three echoed console instructions (`:938`, `:958`, `:972`). `cloud_remote`'s two `rclone(` calls are reads (`cloud_remote:83` the helper, `cloud_remote:102`); its write is `cloud_remote:264`. The interface's connection pages reach `connections.save` by running `cloud_remote create`/`update` (ES, read by name only).
<!-- end t17:writers -->

## § The secrets' paths

One row per credential kind per sink it can reach. A sink no line reaches says so. Every "where" is a line at `8ebaf8daad`.

<!-- begin t17:secrets -->
| Credential | Sink | Where | Mask at that sink | Note |
| --- | --- | --- | --- | --- |
| provider token | file: `rclone.conf` | `cloud_connections.py:198`, `cloud_connections.py:253` | 0600 (observed); not obscured by rclone (OAuth JSON) | held back from every archive (`backuptool` DEVICEONLY, `:746-751`) |
| provider token | process argv (`/proc/<pid>/cmdline`) | `cloud_oauth:589` | **none** | on `rclone config create`'s argv for up to the 40 s `run()` bound and the `lsd` check (F-05) |
| provider token | `/var/log/cloud_sync.log` | `cloud_oauth:448` | fixed sentences only | today's `detail` is a `Refused` sentence or `CLOSED_EARLY`; scrubber family F2 covers earlier builds |
| provider token | stderr | `cloud_connections.py:135` | discarded | `run()` raises a fixed sentence; `read_config`'s dump never echoed (`:37-38`) |
| provider token | `/var/run/cloud_oauth/session.json` | no line reaches it | not written | the state's fields are status, attempt, session, url, address, provider, pin, name, backend, error, remote |
| provider token | the per-session log (`window.log`) | no line reaches it | not written | the window never sees the token |
| provider token | a settings archive | `backuptool:1038` | held back; the credential scan refuses a staged token (exit 5) | `credential_lines` `:431-459` |
| provider token | a packet | no line reaches it | never collected | D-CLOUD-181; this audit's packet is scanned three ways at stage C |
| provider token | a screen | no line reaches it | not shown | -- |
| OAuth code | the sign-in window's page record | `cloud-signin-window.c:660` | excluded: a 127.0.0.1/localhost address is never recorded | #308 claude F-RS-20 |
| OAuth code | a loopback GET to rclone | `cloud_oauth:516` | loopback only | the paste flow (`submit`) |
| OAuth code | the LAN (the paste flow's POST) | `cloud_oauth:2490` | **none**: plain HTTP on the LAN, behind the PIN | only where the device has no browser stack |
| OAuth code | `/var/log/cloud_sync.log`, `session.json`, stderr | no line reaches it | not written | -- |
| pin | `session.json` | `cloud_oauth:2597` | **none**; 0644 observed in a 0755 folder | cleared by `cancel` (`reset_state`) |
| pin | stdout to the interface | `cloud_oauth:2641` | none (by design: the handheld shows it) | and `URL=` with it |
| pin | a screen (the handheld), the QR, the URL path | `cloud_oauth:2587` | by design | the URL travels plain HTTP on the LAN |
| pin | the phone page | `cloud_oauth:1133` | served only after the gate | posted back on every request (`:1181`) |
| pin | `/var/log/cloud_sync.log` | no line reaches it | not written | -- |
| typed WebDAV/SFTP secret | process argv (`cloud_remote`, then `rclone`) | `cloud_connections.py:164` | **none** | two processes' argv for the create's duration (F-05) |
| typed WebDAV/SFTP secret | file: `rclone.conf` | `cloud_connections.py:165` | obscured by rclone (reversible), 0600 | -- |
| typed WebDAV/SFTP secret | `/var/log/cloud_sync.log` | `cloud_remote:96` | verb and code only | scrubber family F1 covers earlier builds |
| typed WebDAV/SFTP secret | stderr | `cloud_remote:331` | **none** for a malformed pair | Info: a pair with no `=` |
| typed WebDAV/SFTP secret | the phone keyboard (LAN) | `cloud_oauth:2455` | the log counts characters only; the LAN carries them plain (the page says so) | masked box on the phone (`type=password`) |
| typed WebDAV/SFTP secret | the per-session log (`window.log`) | `cloud-signin-window.c:533` | only under `CLOUD_SIGNIN_DEBUG`, which nothing sets | Info (F-12) |
| typed WebDAV/SFTP secret | a screen (`cloud_setup`'s rclone stderr) | `cloud_setup:495` | **none**: two lines of rclone's ERROR text shown | F-07; rclone's error carries the remote's URL, not its secret |
| device id | file: `cloud_sync-device-id` | `cloud_device_id:290` | 0644 observed | held back from every archive |
| device id | cloud folder names, logs, stdout | `cloud_device_id:144` | an unsalted md5 of the MAC, cut to 40 bits | **recoverable by brute force** within an OUI (F-11) |
| the root password | a screen (the console setup flow) | `cloud_setup:926` | **none**: shown in the clear | the legacy SSH flow; `--info` prints `PASSWORD_SET` only (`:618`) |

**The scrubber's three families** (`cloud_log_scrub:78-121`), the shapes earlier builds wrote, and whether a writer in the 14 writes each today:

| Family | Shape | Rule | Writes it today |
| --- | --- | --- | --- |
| F1 | `cloud_remote` failure lines with their arguments (`rclone config create <name> <type> k=v ... failed (<n>): <rclone's words>`) | `cloud_log_scrub:80` and the key masks | **no**: `cloud_remote:96` logs the verb and code |
| F2 | `cloud_oauth`'s `could not finish the sign-in: <rclone's words>` | `cloud_log_scrub:94` | **the shape yes, the words no**: `cloud_oauth:448` writes a fixed `Refused` sentence (`cloud_oauth:592-594`) |
| F3 | the interface's `cloud_remote create: <output>` record and its continuation lines in `es_log*.txt` | `cloud_log_scrub:112` | **the shape yes, masked**: at the ES pin `16dbac5211`, `GuiMenu.cpp:7414` logs `cloud_remote create: ` + `Utils::String::maskSecrets(out)` (`stage-b/es-cloud-remote-log.txt`; masked since ES `731252c61`, the scrubber's comment); what the mask catches is the ES slice's |
<!-- end t17:secrets -->

## § The deletions

Every `rm -rf`, `rclone delete`, `sync`, `move` and `purge` in the 14, with its bound and the condition that reaches it.

<!-- begin t17:deletions -->
| Statement | Verb | Bound | Reached when |
| --- | --- | --- | --- |
| `cloud_content_restore:1271` | `rm -rf` | the scan's `mktemp -d` | `--scan`'s EXIT trap |
| `cloud_content_transfer:110` | `rm -rf` | this call's `mktemp -d` fifo directory | `bounded_content_rclone`'s cleanup trap |
| `backuptool:224` | `rm -rf` | `/storage/.cache/backuptool-staging.`* (`:762`) | every backup and restore, under the folder's flock (`sweep_leftovers`) |
| `backuptool:227` | `rm -rf` | this run's `${STAGING}`, when set | the EXIT trap |
| `backuptool:1183` | `rm -rf` | this run's `${STAGING}` (`mktemp -d` under the prefix, `:1161`) | a failed step of `write_archive` or its end |
| `backuptool:1274` | `rm -rf` | this run's `${STAGING}` (`mktemp -d` under the prefix, `:1161`) | a failed step of `write_archive` or its end |
| `backuptool:1290` | `rm -rf` | this run's `${STAGING}` (`mktemp -d` under the prefix, `:1161`) | a failed step of `write_archive` or its end |
| `backuptool:1303` | `rm -rf` | this run's `${STAGING}` (`mktemp -d` under the prefix, `:1161`) | a failed step of `write_archive` or its end |
| `backuptool:1308` | `rm -rf` | this run's `${STAGING}` (`mktemp -d` under the prefix, `:1161`) | a failed step of `write_archive` or its end |
| `backuptool:1327` | `rm -rf` | this run's `${STAGING}` (`mktemp -d` under the prefix, `:1161`) | a failed step of `write_archive` or its end |
| `backuptool:1337` | `rm -rf` | this run's `${STAGING}` (`mktemp -d` under the prefix, `:1161`) | a failed step of `write_archive` or its end |
| `backuptool:1341` | `rm -rf` | this run's `${STAGING}` (`mktemp -d` under the prefix, `:1161`) | a failed step of `write_archive` or its end |
| `cloud_content_restore:1015` | `rclone delete` | `--max-delete` the preview's count; the save, conflict, metadata (and n64 state) excludes; local only | `--match --apply`, verb `remove`, only after the spent plan, the context and mode check, a populated root, and the per-system verb and count check (`:885-980`) |
| `cloud_content_restore:750` | `sync --dry-run` | deletes nothing (`--dry-run`) | every preview and apply (`match_plan_one`) |
| `cloud_content_restore:1046` | `sync` | `--max-delete` the preview's count; the excludes; the inactivity bound; **and whatever `RCLONE_NET_OPTS` adds** (F-02) | `--match --apply`, verb `sync`, under the same refusals |

**`rclone move`, `purge` and `rmdir`: 0 in the 14.** **`--delete-excluded`: 0 in code**; its one occurrence is the comment at `cloud_content_restore:528`. But no statement strips it from `RCLONE_NET_OPTS`, which reaches the deleting `sync` (F-02).

**The refusals before the two deleting statements** (`cloud_content_restore`, quoted):

- `cloud_content_restore:886` -- a `plan2` header with a 64-hex context and a mode.
- `cloud_content_restore:890` -- the plan spent before anything is read.
- `cloud_content_restore:892` -- refused if it could not be spent.
- `cloud_content_restore:899` -- the context or mode drifted: `SOMETHING CHANGED SINCE YOU CHECKED`.
- `cloud_content_restore:905` -- no plan: `CHECK WHAT WOULD CHANGE FIRST`.
- `cloud_content_restore:915` -- an empty or unreadable cloud root.
- `cloud_content_restore:974` -- a verb changed, or more to remove than the preview counted.
<!-- end t17:deletions -->

- **The two deleting statements of `--match --apply` are reachable only with a spent `plan2` plan whose context and mode match and whose per-system count the device's listing does not exceed.**
  - The apply spends the plan before it reads anything (`:885-897`).
  - It refuses a drifted context or mode (`:898-903`), an empty plan (`:904-909`) and an empty or unreadable cloud root (`:914-928`).
  - Per system it refuses a changed verb or a higher count (`:970-980`), and gives `--max-delete` the preview's count.
  - **`--max-delete` is a cap, not a transaction** (`:1036-1044`): the refusals are the guard.
- **What the refusals do not cover:** the flags `RCLONE_NET_OPTS` adds to the deleting `sync` (F-02).

## § The archive

`backuptool`, read whole; the figures are the code's.

- **Held back at backup** (`write_archive`, `:1016-1112`), each line counted:
  - `rclone.conf`, `active-connection`, the device id and its `.previous` (DEVICEONLY, `:746-751`);
  - the whole of `rclone/` and `raofflineproxy/` (DEVICEONLYDIRS, `:723-726`);
  - five token-only emulator files (RATOKENFILES, `:698-704`);
  - the `.backup`, `.bak`, `.tmp` and `.old` beside every stripped or held file.
- **Sanitised copies** (`:1193-1261`):
  - `system.cfg` drops every line with `.key=*** `.password=*** or `.token=***
  - `es_settings.cfg` drops `ScreenScraperPass`, `ScreenScraperDevPass` and `IGDBSecret`, which at the ES pin are exactly the interface's credential settings (the lane's grep of the pin, read under the coordinator's word);
  - `retroarch.cfg` and four emulator settings files blank their token and password values;
  - each copy keeps its original's mode and time (`keep_meta`, `:367-372`, four call sites, each checked).
- **The SECRETLIST and SENDLIST arithmetic** (`:1128-1142`): the send list must equal the file list less the unique held-back lines, or nothing is written.
- **The staged tree is counted** against what was sent plus the sanitised copies (`:1283-1292`), then **scanned for credential-shaped lines** (`credential_lines`, `:431-459`). Any hit is exit 5, `A SIGN-IN WAS FOUND IN THE BACKUP`, before the archive has a name.
- **The archive is named only after it lists back whole** (`:1323-1347`): `.partial`, then `tar -tzf` counted against the staged files, then `mv`. This is the model the brief holds the other writers to.
- **Restore** (`:1413-1765`):
  - the newest archive by name, any device's; `archive_ok` (a zip's stored members CRC-checked with busybox `crc32`);
  - `foreign_member` refuses a member outside `storage/` or with a `.` or `..` part;
  - the seed list read whole; a copy of everything the archive would replace, and a list of what it would create, both counted, under a mark read back before the first write;
  - extraction with an exclusion file written whole and counted; live symlinks skipped by exact name; a revert on any failure.
- **The legacy zip path** (`zip_stored_ok` `:480-514`, `archive_ok`, `archive_members`) is reachable while any device holds a `*_BACKUP.zip` or `ROCKNIX_BACKUP.zip` (`newest_backup`, `:159-171`). It is a row, with removals none (F-16).
- **What `foreign_member` does not judge:** a member's type. F-04 is the case, and the image's `tar` is what stops it.

## § The phone flow

`cloud_oauth`'s LAN listener, read whole.

- **The bind:** `lan_address()` (`:268-281`), the source address of the default route, else 127.0.0.1; never the wildcard (`:2549-2561`). Port 8080 by default, shared with the offline achievements proxy's 127.0.0.1:8080.
- **The bounds:**
  - 16 connections at once, the 17th closed on arrival (`BoundedHTTPServer`, `:2220-2244`);
  - 15 s per socket (`REQUEST_TIMEOUT`);
  - a body over 64 KiB refused before a byte is read (`:2395-2405`);
  - the whole listener ends with the serve's timer (600 s by default, `:2648-2650`).
- **The PIN:** four digits from `secrets.randbelow` (`:2062`), compared with `secrets.compare_digest` (`:2206`). Ten wrong answers end the PIN for the rest of the serve (`pin_exhausted`, `:2196-2203`), so a guess has 10 in 10,000.
  - **The defect** (F-01): `_supplied()` (`:2330-2344`) takes a request's first path segment as its PIN. A browser's own `/favicon.ico` or touch-icon request is therefore a wrong PIN, and ten of them lock the right one out (`stage-b/fixture-pin.txt`).
- **The routes:**
  - an unauthenticated GET is answered with the PIN page and spends nothing; a wrong PIN gets the same page with *"That PIN did not match."*, then 403 at the tenth;
  - after the gate: the probe (`waiting`, `loading <hash>`, `open <hash>`, where the hash is the first 8 hex of the window's page address, never the address itself, `:2355-2389`); the keyboard's `type` and `key`, and the pointer's `move`, `click` and `wheel`, each 409 without a window (`:2411-2458`); `restart`; and the paste flow's `code`.
  - The log records keystroke counts only (`:2455-2457`).
- **What the page says:** what is typed crosses the network unencrypted, so use it on a network you trust (`:1052-1055`, and in French). The box is masked, and dropped characters are counted while masked (`:1241-1262`).

## § The guest cycle

**Not yet run.** The window is asked for on #664 after this stage, with its plan, and runs only after M7's guest RETURN on the host file and T16's re-granted window. The proofs it owes are listed in that request and in `00`'s stage-B entry. If no window is granted before the hand-back, this section records `CANNOT` with the host file's state and names each proof that moved to a host fixture or stays open.

## Findings

### F-01 (Q3a; Low; a candidate bug, fork-own): a phone's own icon requests spend the sign-in PIN's ten attempts and lock the right PIN out

- **The trace.**
  - `cloud_oauth:2330-2344` `_supplied()` returns `?pin=` from the query, else the request path's first segment.
  - `_gate()` (`:2308-2328`) counts any non-empty, non-matching value as a wrong PIN (`pin_failed`, `:2200-2203`).
  - At ten, `pin_exhausted()` (`:2196-2198`) refuses every request with 403, the right PIN included, for the rest of the serve.
- **The cause.** `GET /favicon.ico`, and Safari's `apple-touch-icon.png` and `-precomposed.png`, carry no PIN in the path or the query, so each is a wrong PIN named `favicon.ico`. A phone's browser makes these requests on its own, without the page asking for them.
- **The fixture** (`tools/t17-pin-fixture.py --expect unfixed`, the real holder and server over loopback):
  - ten `/favicon.ico`, then `GET /<pin>` -> **403**;
  - ten touch-icon requests -> **403**;
  - nine -> 200;
  - ten real wrong PINs -> 403 (the designed lockout, the control).
- **What the player meets:** the phone keyboard page answering *"Too many wrong PINs. Start again on the handheld."* after a handful of reloads. The sign-in on the handheld itself is unaffected.
- **Already written:** nothing persisted. The counter lives in the serve's memory, and a new serve starts at 0.
- **The fix is contained:** count only a request that offers a PIN-shaped value (four digits), and answer `/favicon.ico` and friends with 404 before the gate.

### F-02 (Q3b; Low, a fail-open guard on the only deleting path; fork-own): a flag in `RCLONE_NET_OPTS` reaches the match's deleting `sync`, and `--delete-excluded` there deletes saves

- **The trace.**
  - `cloud_content_restore:235-238` reads `RCLONE_NET_OPTS` from `cloud_sync.conf` as text (a double-quoted value may hold spaces).
  - `:276-279` splits it into `RCLONE_NET_OPTS_ARRAY`.
  - Every networked rclone call takes the array, the preview's dry run (`:750`) and **the apply's deleting `sync` (`:1046`)** among them.
  - No statement allowlists its flags or strips `--delete-excluded`. The rule (`rclone-cloud-sync.md:207-218`) calls that flag catastrophic on a restore-side `sync` and asks for it to be stripped unconditionally; T16's scripts strip it from `RCLONEOPTS` (`cloud_restore:1383`, `cloud_backup:1342`) but split `RCLONE_NET_OPTS` the same unfiltered way (`cloud_restore:1406-1411`) -- the seam, named from this side.
- **The fixture** (`tools/t17-content-fixture.py --expect unfixed --real-rclone <the donor's 1.75.2>`):
  - with `RCLONE_NET_OPTS="... --delete-excluded"`, the deleting `sync` carries the flag (stub);
  - with the real rclone over a local-backend cloud holding `snes/a.zip` and a device holding `a.zip`, `b.zip` and the save `a.srm`: the preview plans **`snes|sync|2|48`**, and the apply **leaves only `a.zip`. The save is gone.**
  - The shipped bound plans `snes|sync|1|28` and keeps the save.
  - The confirmation would say "2 files" with nothing to say one is a save.
- **The reach:** no shipped build writes the flag into `RCLONE_NET_OPTS` (`cloud_sync.conf.defaults:94`). The value is a player's, an editor's or a future default's. The guard that would catch it is missing; the loss it allows is a save, not recoverable locally.
- **Already written:** a device whose `cloud_sync.conf` already holds such a value has lost nothing until it runs `--match --apply`. The fix acts on the next run, and no migration is owed.
- **The fix is contained:** take only the bound's flags from `RCLONE_NET_OPTS` (an allowlist: `--contimeout`, `--timeout`, `--low-level-retries`, `--retries`), or refuse a run whose bound holds anything else. T16's two scripts are the coordinator's to route.

### F-03 (Q3b, Q3a; Low; a candidate bug, fork-own): `cloud_content_backup` uploads any path it is named, `/storage/.config` among them

- **The trace.**
  - `cloud_content_backup:583-585` `*) DIRS=("$@")` takes the explicit names as given.
  - `:710` makes `SRC="${DEST}/${DIR}"`, and `:753` copies it to `remote_for "${DIR}"`.
  - No name is checked against `^[A-Za-z0-9_][A-Za-z0-9._-]*$`. `cloud_content_restore` checks every name before its first transfer (`:1482-1487`), and both scripts' `--selected` read through the same pattern (`selected_systems`). Audit #307 PL-030's rule, *"only a system folder's name is ever acted on"*, holds for the restore and not for the backup's explicit form.
- **The fixture:** `cloud_content_backup '../.config'` hands rclone a `copy` from `<root>/storage/roms/../.config` and exits 0; the control `snes` copies only its folder.
  - On a device that is `/storage/.config`, `rclone/rclone.conf` with its tokens among it, sent to the player's cloud under `ROMs/../.config`.
- **The reach:** the interface passes names it listed itself (`--list`), so a player's menu never sends one. A shell, a script or a future caller does. A path traversal into the cloud on the one tier with no name check, with credentials in its path.
- **Already written:** nothing on the device. A cloud that ever received such an upload keeps it; the fix cannot see it, and the coordinator decides whether that is worth a note.
- **The fix is contained:** the restore's loop (`:1482-1487`), before the lock.

### F-04 (Q3b; Info; a candidate refuted by fixture): a symlink member in a hand-made settings archive is accepted by `backuptool`'s check and stopped by the image's `tar`

- **The trace.** `foreign_member()` (`backuptool:551-558`) judges member **names**: under `storage/`, with no `.` or `..` part. A tar member that is a symlink, `storage/.config/escape -> /elsewhere`, followed by `storage/.config/escape/note.txt`, passes it. The restore's `LINKS` skip (`:1633-1638`) covers only paths that are symlinks on the device.
- **The fixture** (`tools/t17-archive-fixture.py`, the product's own function and the image's busybox):
  - `foreign_member` -> rc 1, *accepted*;
  - busybox `tar -xzf -C <root>` -> **rc 1, `can't create symlink`**: busybox defers a link with an absolute or `..` target to the end of extraction, by which time the later member has made a directory of the name. Nothing landed outside the root.
  - The tree ships no GNU tar (no `PKG_NAME="tar"` under `packages/` or `projects/`), so the image's `tar` is busybox's.
  - On a device the extraction fails, and `backuptool` reverts the restore.
- **Disposition:** a design note. The guard that holds is the extractor's, not the check's. `backuptool`'s own archives hold regular files only (`find storage -type f`, `:1324`), so only a foreign or tampered archive carries such a member. D-UI-117's promise is about names. The guest repeats it through a full `backuptool restore`.

### F-05 (Q3a; Info): secrets on process argv, and the sign-in state readable by any user

- **On argv.** `connections.save()` builds `rclone --config <staged> config create <name> <type> key=*** ...` (`cloud_connections:161-165`) and holds it for the `run()` bound of 40 s and the `lsd` check (`:131`, `:180`). The values are a WebDAV or SFTP secret from `cloud_remote`'s own argv (`cloud_remote:325-335`), or the provider token from `cloud_oauth` (`:588-591`). `/proc/<pid>/cmdline` shows them to any process for that time.
- **At rest:** `session.json` (the PIN, the URL with it, the provider link) is 0644 in a 0755 folder (`stage-b/fixture-mode.txt`), while `session.lock` is 0600.
- **The reach:** every process on a handheld runs as root, so no second user exists to read either. Recorded for a future multi-user or service account.
- **Disposition:** a design note. rclone reads a config value from `RCLONE_CONFIG_<REMOTE>_<KEY>` in the environment, which is not world-readable, so a fix exists if the coordinator wants one.

### F-06 (Q3a; Info): a kill mid-save leaves the new credentials staged beside `rclone.conf`, and nothing sweeps them

- **The trace.** `save()` and `remove()` stage a copy in `tempfile.TemporaryDirectory(prefix='.connection-', dir=/storage/.config/rclone)` (`cloud_connections:157`, `:238`), and `atomic()` stages `.rclone.conf-*` beside the file (`:74`). A SIGKILL or power cut before their cleanup leaves the staged `rclone.conf` with the new token:*** 0600, in a 0700 directory. No script in the tree removes `.connection-*` or `.rclone.conf-*` (the lane's grep).
- **What holds:** `backuptool` holds the whole of `rclone/` back (`:723-726`; `last-good-scripts-test:779-781` checks it), so the leftover never reaches an archive or the cloud.
- **Already written:** any device that was cut mid-sign-in holds such a directory today, and a sweep would remove it.
- **Disposition:** a hardening, for the coordinator: a sweep of `.connection-*` and `.rclone.conf-*` under the transfer lock, at the start of `save()`.

### F-07 (Q3a, Q2; Info): what reaches a screen

- `cloud_setup:495`'s probe shows the first two lines of rclone's ERROR text on the setup page (`:537`, `:543`). They carry the remote's URL, not its secret, but they are rclone's words on a player's screen (`player-language.md`: a tool's words never reach a player).
- The legacy console flow shows the root password in the clear (`cloud_setup:926`, `:937`) beside the SSH command. `--info` prints `PASSWORD_SET` only (`:618`, #116).
- `cloud_remote:331` echoes a malformed `key=*** pair to stderr.
- `resolve_connection` logs the override file's first line (`cloud_setup:224`, `:928`).
- **Disposition:** recorded; the first is a Q2 item for the setup page's ES slice.

### F-08 (Q3b; Info): the match's smaller edges

- **The plan has a timestamp and no age.** An apply weeks after its preview runs if the context, mode, verbs and counts still agree (`cloud_content_restore:886`, `:898`, `:970-980`). The counts bound it. A design note under D-CLOUD-141.
- **The `/tmp` fallbacks** with a predictable `.$$` name when `mktemp` fails (`:837-838`): fail-open on a single-user device.
- **`exists_remote` matches a folder name as a regex** (`:441`, `grep -qx "${name}/"`): a name with `.` matches more than itself. Its callers ask whether BIOS exists.

### F-09 (Q3a; Info): the listener's two smaller edges

- **A non-ASCII PIN raises `TypeError`.** `secrets.compare_digest` refuses a non-ASCII `str`. `parse_qs` decodes a POSTed `pin=%C3%A9` to `é`, and the handler thread dies with a traceback on stderr (`stage-b/fixture-pin.txt`). It is not counted and grants nothing.
- **The paste flow renders rclone's words as HTML.** `_render`'s message is inserted raw into `PAGE` (`:2271-2290`), and a failed submit's message is `failure_reason()`, which embeds up to 160 characters of rclone's last error line (`:480-488`), the provider's error text. It is only reachable where the device has no browser stack, and only behind the PIN.

### F-10 (Q3; Info): writes judged by their exit status, or not at all

- **`--set-systems`** (`cloud_content_restore:1405-1407`) does not check its temp write. A failed write prints `OK <n> selected` with the old count and exits 0.
- **`backuptool`'s rotation** `mv "${PREVIOUS}" ...` (`:1885`) is unchecked. A failed move leaves two archives at the root, and the settings upload sends both.
- **`cloud_sync.conf`'s writes take no lock** (`cloud_setup:69-112`, `--set-*-remote`, `--use-content-root`). They are atomic and checked line by line, but an interface write and a `cloud_sync_helper` append can interleave.
- **The model** is `backuptool`'s archive (`:1323-1347`): `.partial`, listed back and counted, then the rename.

### F-11 (Q3a; Info): the device id's hash hides the MAC from a glance, not from a search

- **The trace.** `cloud_device_id:143-145`: the id's suffix is `md5(<permanent MAC>|unknown)[:10]`, unsalted (`DEVICE` is never set on a device, `:136-142`). A MAC is 48 bits, of which the first 24 name the adapter's vendor, so about 2^24 candidates per vendor recover it from a cloud folder name.
- **The comment's claim** (`:29-31`, *"the address is hashed rather than stored ... has no business sitting in somebody's cloud storage in the clear"*) holds against reading and not against trying.
- **Disposition:** a design note. A salted or keyed hash is a second identity change, with a legacy variant of its own (`:139-142`); the coordinator's call.

### F-12 (Q3a; Info): the sign-in window

- **Navigation policy:** only user-gesture navigations are filtered (`cloud-signin-window.c:851`), by design (captchas, IdPs).
  - The allowed host is the last two labels of the provider's (`cloud_oauth:990-1000`), so a Google Drive sign-in allows every `*.google.com`.
  - Popups are held to the same host rule (`:892-916`).
- **The context is ephemeral** (`:963-966`).
- **`CLOUD_SIGNIN_DEBUG` logs every key's string** to `window.log` (`:532-534`). Nothing in the tree sets it, but `cloud_oauth` passes its own environment to the window (`:917`), so an exported variable would.
- **The page record excludes the code-bearing redirect** (`:660-671`); the probe exposes only an 8-hex hash.

### F-13 (Q4; Info): the tools that exercise these files, and the rclone each runs

- `cloud_folder_validate` runs `rclone` from `PATH`, not `/usr/bin/rclone` (`:90`, `:252`). This is M7's #1117 (*the validator bound to the package's rclone*), cited and not read from M7.
- `tools/pixelelated-cloud-validator-test:58` hard-codes `rclone v1.75.1`; the tree pins 1.75.2. A lead for the tool's owner.
- `tools/pixelelated-content-scope-test:222` reads an argv file a refused run never writes. A lead.
- `tools/cloud-connections-test` runs the host's rclone (T13's Q2).

### F-14 (Q2; Low): two `>>> why` sentences the interface's table at the pin does not know

- **The check:** every `>>> why` sentence the 14 print, against `CloudText.cpp:414-466`'s 38 at the ES pin `16dbac5211` (`stage-b/why-lines.txt`, `stage-b/es-why-sentences.txt`). Every literal and helper sentence is in it but two:
  - `ANOTHER CLOUD SYNC IS RUNNING` (`cloud_setup:797`, `--seed-folders` refused by the lock). It is also the *"Not this"* form of `es-player-text.md:227` (D-UI-031); the rule's word is `A SYNC IS ALREADY RUNNING`.
  - `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK` (`backuptool:1495`, D-UI-117's proposed words).
- **Either one, if shown, reads in English on a French screen** (`localizedWhy` falls back to the sentence itself). Whether the interface shows them (`CloudText.cpp:663` treats `--seed-folders` on its own) is the ES slice's read.
- **`tools/vocabulary-check`'s verdict** over the four it reads: 0 wrong of 163 (`stage-b/vocabulary-check.txt`). The other ten files' strings were read by hand against `es-player-text.md`, and F-07's rclone text is their one departure.

### F-15 (Q1; Design): the connection model

- **One writer, one lock, one set of refusals:** every path to `rclone.conf` goes through `connections.save` or `remove` under the flock (§ The writers). That covers `cloud_remote create`, `cloud_remote update`, `cloud_oauth`'s sign-in and the interface's connection pages through `cloud_remote`.
- **Two asymmetries, recorded:**
  - `require_manual()` refuses while an automatic sync option is on for `update`, `select` and `remove` (`cloud_connections:150`, `:220`, `:229`), but not for a new `create`.
  - A first connection writes no `active-connection` (`:193-197`), so the legacy first-remote fallback (`active()`, `:54-62`) is a shape the new writer itself leaves. The comment says so, and it is harmless with one remote.
- **`cloud_oauth` at 2,830 lines and seven classes**, its seams as a proposal: the broker (`Session`, `SessionHolder`), the phone page (`make_handler` and the three templates), the device input (`RemoteKeyboard`, `RemoteMouse`, `GamepadBridge`), and the state (`session.json` and its markers).

### F-16 (Q6; Renovation): dead ends

- **The zip path** in `backuptool` (`:480-518`, `:1436-1445`, `:1686-1708`) is reachable while a device holds a legacy zip. A row; removals none.
- **Uncalled functions:** the lane's recount at `8ebaf8daad` (every defined name, whole-word, over the 14): no shell function is named only once; three python methods are, `cloud_oauth`'s `do_GET`, `do_POST` and `redirect_request`, which `http.server` and `urllib` call. Nothing dead.
- **The legacy console flow** in `cloud_setup` (`:913-976`) is the SSH setup the wizard replaced. It is still reachable as `cloud_setup` with no argument. A row.

### F-17 (Q7; Info)

- Can a reader tell, from the directory and the rule, which script writes `rclone.conf`, which deletes, which runs at boot, and where each secret may appear? From the directory, no. From the two generated tables, yes: § The writers and § The secrets' paths.
- **The rule does not say who writes `rclone.conf`.** `rclone-cloud-sync.md` names `cloud_remote active` and the legacy first-remote fallback (`:268`), and never names `cloud_connections.py` (0 hits). The rule's drift is #909's: cited, not edited here.

### F-18 (Q5; Info)

- **Bounds, and what the player waits for:**
  - the validator: 6 s a call, 25 s in all, 2 MiB and 4,096 entries (`cloud_folder_validate:22-24`);
  - the content transfer: an inactivity ceiling of the bound's `--timeout` plus 6 s, with no total (`cloud_content_transfer:85-158`, D-CLOUD-127);
  - the sign-in: 10 s on the opener (`cloud_oauth:300`), 15 s on the paste replay (`:516`), 15 s a socket, 600 s a serve;
  - the connection's verification: 40 s.
- **These scripts run from menus, not on the launch path.** Time to play is not touched; the retro cites `docs/vm-qa-log.md`.

### F-19 (Q4; Info)

- The window's recipe builds against `webkitgtk` (`cloud-signin-window/package.mk:9`). The DMABuf renderer is off unless set (`cloud-signin-window.c:949`), blindspot 48's family: a WebKit constraint written beside the thing it constrains.
- rclone 1.75.2 on the image (`rclone/package.mk:7`) against the host's 1.60.1-DEV (§ The host tools).

## Proofs

| Proof | What | Artifact | Cell |
| --- | --- | --- | --- |
| P1 | The membership: 14 / 11,180 / fork-own 14 / shipped 14 | r01 | proved: tool-run |
| P2 | The lines, modes and functions | r02 to r05 | proved: tree |
| P3 | The history with the three identities | r25 to r28 | proved: history |
| P4 | The upstream relation | r29 to r31 | proved: history |
| P5 | The callers and the tools' counts | r32 to r35 | proved: tree |
| P6 | The branch and the removal rule | r39, r40 | proved: tree |
| P7 | § The writers, generated and anchored | `tools/t17-tables.py writers` | proved: tool-run |
| P8 | § The secrets' paths, generated and anchored | `tools/t17-tables.py secrets` | proved: tree |
| P9 | § The deletions and the refusals | `tools/t17-tables.py deletions`, r10 to r13 | proved: tree |
| P10 | The five fork tools on the host | `stage-b/tools-out/` | proved: tool-run |
| P11 | The PIN attempts spent by icon requests; the non-ASCII PIN | `stage-b/fixture-pin.txt` | proved: fixture |
| P12 | A symlink member: the check accepts, the image's tar refuses | `stage-b/fixture-archive.txt` | proved: fixture |
| P13 | The backup's unchecked names; the flag into the deleting sync, a save deleted | `stage-b/fixture-content.txt` | proved: fixture |
| P14 | The writers' modes, observed | `stage-b/fixture-mode.txt` | proved: fixture |
| P15 | `tools/vocabulary-check` at the ES pin | `stage-b/vocabulary-check.txt` | proved: tool-run |
| P16 | The `>>> why` sentences against the interface's table | `stage-b/why-lines.txt`, `stage-b/es-why-sentences.txt` | proved: tree |
| P17 | The tables regenerated | `tools/t17-tables.py check` | proved: tool-run |

## Positives

| What | Where | Why it matters |
| --- | --- | --- |
| One writer of `rclone.conf`, atomic, locked, verified before install, rolled back on a failed publish | `cloud_connections.py:72-215` | a sign-in that fails leaves the old bytes |
| Provider diagnostics never forwarded; the dump never echoed | `cloud_connections.py:37-38`, `:135-136`; `cloud_remote:90-96` | rclone's words, which can carry credentials, stay out of the logs |
| The match's refusals, in order, before any deletion | `cloud_content_restore:885-980` | a stale, foreign or empty preview deletes nothing |
| The archive named only after it lists back whole, and scanned for credentials first | `backuptool:1283-1347` | the model the other writers are held to |
| A probe that reports absence honestly | `cloud_scan:149-169`, `cloud_folder_validate:89-113` | blindspot 22's shape avoided: an unreadable cloud is never an empty one |
| The scrubber records each family only when every file was rewritten whole, line counts equal | `cloud_log_scrub:136-187` | a partial scrub is retried, never recorded as done |
| The phone page masks the box and counts dropped characters while masked | `cloud_oauth:1241-1288` | the keyboard does not undo its own masking |



## The first reader's 03-retrospective.md (whole)

# Retrospective audit — M6.P2 T17, cloud setup, sign-in, connections, content and settings backups (#664)

*The fourteen as a system: what they are built on, what they keep to, where they meet the rest. Findings are `02`'s, by number.*

## 3.1 Architectural coherence

- **One writer, one lock, one set of refusals.** `cloud_connections.py` is the only file that writes `rclone.conf` or `active-connection`. It does so atomically, under the transfer lock, and verifies a new connection in a private copy before installing it. Every path to it goes through `save` or `remove`: `cloud_remote create` and `update`, `cloud_oauth`'s sign-in, and the interface's pages through `cloud_remote`. This is the newest and cleanest shape in the slice (F-15).
- **Three scripts read `cloud_sync.conf` with one reader.** `cloud_setup`, the two content scripts and `cloud_scan` carry the same `conf_get` awk, so the tiers read one value the same way (D-CLOUD-149). It is copied four times rather than shared: a fix to one copy is a fix to four.
- **The only deleting path is guarded by its order of refusals** (§ The deletions). The plan is spent first, then context and mode, an empty plan, an empty root, and the per-system verb and count are checked, with `--max-delete` as the cap. What the order does not cover is the flags another file contributes (F-02).
- **`backuptool` is a transaction with a model archive write** (§ The archive): staged, counted, scanned, listed back, renamed. Its restore takes a copy and a mark before the first write and reverts on failure.
- **`cloud_oauth` is the largest file the fork wrote** (2,830 lines, seven classes), and its seams are visible: broker, phone page, device input, state. A split is a proposal, not a defect (F-15).

## 3.2 Project conformance

- **`engineering-practices.md` § Guards must fail closed.**
  - Mostly kept: `cloud_scan`'s `stop_on`, `cloud_folder_validate`'s `Unreadable`, `backuptool`'s counts, and the refusal that the match's exclusion arrays are loaded (`cloud_content_restore:866-870`).
  - Two guards fail open: the match takes whatever flags `RCLONE_NET_OPTS` holds (F-02), and `cloud_content_backup` takes any name (F-03).
- **`engineering-practices.md` § Verify the artifact, not the report.** `backuptool`'s archive is the model. `--set-systems` and `backuptool`'s rotation report success from an exit status, or from nothing (F-10).
- **`upgrade-and-install.md`.** Each candidate bug's `Already written:` is in `02`. None leaves state to migrate: the PIN counter is in memory; a conf value acts only on the next run; an upload already made is the cloud's. F-06's leftover staging directories are the one already-written state a fix would want to sweep.
- **`player-language.md` and `es-player-text.md`.**
  - Two `>>> why` sentences are not in the interface's table, and one of them is the rule's *"Not this"* wording (F-14).
  - rclone's own ERROR text reaches the setup page (F-07): *a tool's words never reach a player*.
  - `tools/vocabulary-check`: 0 wrong of 163.
- **`rclone-cloud-sync.md`:** `--delete-excluded` *"stripped unconditionally"* is kept for `RCLONEOPTS` and not for `RCLONE_NET_OPTS` (F-02). The rule does not say which script writes `rclone.conf` (F-17, #909).
- **D-CLOUD-142** (no command in `cloud_sync.conf` ever runs) is kept: every reader is text. `backuptool.conf` is sourced, by design: it is the player's own list, and a restore can already write any file under `/storage` (F-04's design note).
- **D-QA-021:** every config-shaped read in this audit went through the filter; the packet goes through the mask and the three-way scan.

## 3.3 Spec fidelity

The brief's figures were re-derived at stage A, and every one held but four, recorded as deltas in `01` and `02`:
- 15 `.$$` lines;
- the staging prefix sweep;
- the directory-wide exit-constant run;
- the vocabulary check, which ran.

At stage B two of the five tools could not give a clean verdict, and the symlink proof was answered on the host by the image's own `tar`. The brief's *"Q6: three python defs referenced once"* held, and so did *"0 shell functions defined and never named"*.

## 3.4 Platform conformance

- **On the host:** the product's own code, with the image's busybox applets where the scripts run under busybox, and M6's donor rclone 1.75.2 where a real rclone was needed.
- **Substitutes, named:** a recording stub rclone, path rewrites into a scratch root, the host's GNU `grep`, `sort`, `gzip` and `timeout` (absent from the donor's busybox), and the host's python 3.
- **The guest** repeats each proof on the installed files under the image's python and rclone, in the window asked for on #664.
- **What only a device shows:** nothing here. The phone page from the host is `CANNOT` under user-mode networking, a harness gap rather than a device fact.

## 3.5 Cross-system interaction audit

### Interaction: T16's sync core x this slice's content scripts (`RCLONE_NET_OPTS`)

- **The shared state:** one config line, read by both slices' scripts and split the same way (`cloud_restore:1406-1411`, `cloud_backup:1367-1371`, `cloud_content_restore:276-279`, `cloud_content_backup:230-232`).
- **The interaction.** T16's scripts strip `--delete-excluded` from `RCLONEOPTS` and not from `RCLONE_NET_OPTS`; this slice's strip neither. On the content side it reaches the only deleting statement (F-02). On T16's side it reaches `cloud_restore`'s `sync` restores, the rule's catastrophic case. This is named here and is T16's to read.

### Interaction: the interface x the `>>> why` lines

- **The shared state:** `CloudText::whySentences()` at the ES pin, 38 sentences, and `localizedWhy`'s fall-through to the sentence itself.
- **The interaction:** two sentences the scripts print have no pair (F-14). A French screen shows them in English if it shows them at all, and that is the ES slice's read.

### Interaction: the interface's connection pages x `cloud_remote`

- **The shared state:** `cloud_remote`'s argv, carrying every `key=*** the player typed, and its exit and stderr sentences.
- **The interaction:** the pages reach the one writer through `cloud_remote create` and `update`, so the secrets ride on two processes' argv (F-05). The interface logs `cloud_remote create: ` through `maskSecrets` at the pin (`GuiMenu.cpp:7414`); what that mask catches is the ES slice's.

### Interaction: `backuptool` x `chksysconfig` and `post-update` (T1)

- **The shared state:** the restore mark `/storage/.config/.restore-in-progress`, read by `chksysconfig verify` at the next boot to put the copy back and remove what the restore created, and the `.restore-finish-pending` and `.cloud-journey-pending` markers the interface reads.
- **The interaction:** the mark is written whole and read back before the first write (`backuptool:1608-1620`), and removed only once the tree is whole or reverted. The reader is T1's.

### Interaction: `cloud_scan` x `rasteratops-settings-archive` (T16)

- **The shared state:** `select_settings_archives` and `SETTINGS_ARCHIVE_LISTING`, sourced at `cloud_scan:326-329`.
- **The interaction:** the scan's settings row is the archive helper's answer. The call site is read here; the helper is T16's.

### Interaction: M7's open work on these files

- **#1111** connection folders and active selection; **#1113** the phone disconnect notice; **#1115** accessibility against the validator's limits; **#1117** the validator bound to the package's rclone (F-13).
- They are cited by number and never read from M7's worktrees. Every finding here stands against `8ebaf8daad`'s bytes.



## The first reader's 04-analysis.md (whole)

# Analysis — M6.P2 T17, cloud setup, sign-in, connections, content and settings backups (#664)

## Executive summary

- **What it read.** The 14 files the cloud's setup, sign-in, connections, content and settings archives run on: 11,180 lines, every one read, all shipped. Thirteen are the fork's own; `backuptool` is the fork's rewrite of an identical 68-line upstream script. **Lens: security. Depth reason: state preservation.**
- **What holds.**
  - One writer of `rclone.conf` (`cloud_connections.atomic()`, 0600 observed), locked, verified before install, rolled back on failure.
  - Provider diagnostics never forwarded.
  - The only deleting path behind an ordered set of refusals, with the preview's count as `--max-delete`.
  - A settings archive named only after it lists back whole and is scanned for credentials.
  - Probes that report absence honestly.
  - A log scrub recorded only when every file was rewritten whole.
- **Three candidate bugs, each shown by a host fixture running the product's own code:**
  - **F-01** (Low): the phone listener counts a browser's own icon requests as wrong PINs, and ten lock the right PIN out for the serve.
  - **F-02** (Low; the only deleting path): `RCLONE_NET_OPTS` reaches `--match --apply`'s deleting `sync` unfiltered. With the donor's real rclone, `--delete-excluded` there deletes a save. T16's `cloud_restore` takes the same value the same way.
  - **F-03** (Low): `cloud_content_backup`'s explicit names are not checked as the restore's are, and `'../.config'` uploads `/storage/.config`.
- **One candidate refuted by fixture:** F-04. A symlink member passes `backuptool`'s name check, and the image's busybox `tar` refuses it.
- **Info and design notes:** secrets on argv and a 0644 state file holding the PIN (F-05); staged credentials a kill leaves behind (F-06); rclone's words and the root password on a screen (F-07); the match's and the listener's smaller edges (F-08, F-09); unchecked or unlocked writes (F-10); a reversible device-id hash (F-11); the window (F-12); the tools' drift (F-13); two why sentences the interface cannot translate (F-14).
- **Nineteen findings:** 4 Low (F-01, F-02, F-03, F-14), 15 Info, Design or Renovation. **Removals: none.** **No guest yet; nothing on a person's device or cloud.**

## Acceptance-criteria scorecard

#664's seventeen, at stage C before the punch-list issue. *Met* names its artifact; *waits* names the stage that ticks it.

| # | Criterion | State |
| --- | --- | --- |
| 1 | `00` and `01` to `05` | met at stage C |
| 2 | the lint `PASS` | pre-issue at stage C; resolution at the close |
| 3 | the plan, two reviewers, provenance, the manifest's scans | stage C |
| 4 | every punch item at a Phase 7 outcome | waits: stage D onward |
| 5 | `reviewed-at:` and `fixed-at:`; the 14 at `8ebaf8daad`'s bytes; nothing changed at A to D | the diffs are empty (r39, r40); the header lines wait for the hand-back |
| 6 | `01` § Scope | met (`64ff2f519f`), with four deltas |
| 7 | coverage, 14 rows | met |
| 8 | § The writers, generated with asserts | met (`tools/t17-tables.py writers`, 31 rows) |
| 9 | § The secrets' paths, the scrubber's families with *writes it today* | met (28 rows, three families) |
| 10 | § The deletions, the two deleting statements and the refusals | met |
| 11 | § The runs | met (40 generated rows, and the host tools) |
| 12 | § The guest cycle | waits: the window asked for on #664 after stage B |
| 13 | `00`'s never-run list, four keyed invokes | met through stage B; the four at stage C |
| 14 | `04` § Q3, Q2, Q4, Q6, Q7 | met |
| 15 | every proof's cell; every punch item's `question:`; every `bug` `box-check` | 17 proofs at stage B; `05` at stage C; bugs at stage D |
| 16 | the retro | waits: stage G |
| 17 | the five checkers | waits: the hand-back |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| A player is locked out of the phone keyboard mid sign-in | Medium (every page load may request icons) | Low (the handheld's own sign-in still works; a new serve resets it) | F-01 |
| A match deletes the saves beside the ROMs | Low (needs a non-shipped value in `RCLONE_NET_OPTS`) | High (saves, not recoverable locally) | F-02; the guard is missing, not the loss |
| `/storage/.config`, `rclone.conf` among it, uploaded to the cloud | Low (needs a direct command line) | High (credentials in the player's cloud) | F-03 |
| A kill mid sign-in leaves new credentials staged | Low | Low (0600, never archived) | F-06 |
| A French player reads an English refusal | Low | Low | F-14 |

## Coverage boundary

- **Read in full:** all 14 (`stage-b/read-notes.md`). `001-functions`'s `redact_credentials` (outside the 14) was read for what the scrubber relies on. The rule `rclone-cloud-sync.md` was read for its `--delete-excluded` lines and its naming of the setup scripts.
- **Read at the ES pin, under the coordinator's word:** `CloudText.cpp`'s why table, the `cloud_remote create` logging line and the `es_settings` credential keys. `tools/vocabulary-check` ran against it.
- **Read by name only:** the interface's setup, connection, transfer and scan pages; T16's scripts, beyond the `RCLONE_NET_OPTS` lines quoted; T1's `chksysconfig`.
- **Not run:** a guest (the window is asked for); a provider's sign-in page with an account (D-QA-058); the phone page from the host (`CANNOT` under user-mode networking).

## Second opinion

*Written at stage C (the two seats' probes and refutations).*

## Finding Verification

| Finding | Re-derivation | Verdict |
| --- | --- | --- |
| F-01 | `cloud_oauth:2196-2206`, `:2308-2344`; `stage-b/fixture-pin.txt` | confirmed by fixture |
| F-02 | `cloud_content_restore:235-279`, `:750`, `:1046`; `cloud_restore:1383`, `:1406-1411`; `stage-b/fixture-content.txt` with the real rclone | confirmed by fixture |
| F-03 | `cloud_content_backup:583-585`, `:710`, `:753`; `cloud_content_restore:1482-1487`; `stage-b/fixture-content.txt` | confirmed by fixture |
| F-04 | `backuptool:551-558`, `:1633-1638`, `:1679`; `stage-b/fixture-archive.txt`; no GNU tar in the tree | refuted by fixture as a bug; kept as a design note |
| F-05 | `cloud_connections.py:161-165`; `cloud_remote:325-335`; `stage-b/fixture-mode.txt` | confirmed |
| F-06 | `cloud_connections.py:74`, `:157`, `:238`; the lane's grep for a sweep (none) | confirmed |
| F-07 | `cloud_setup:495`, `:537`, `:543`, `:926`, `:937`; `cloud_remote:331` | confirmed |
| F-08 | `cloud_content_restore:837-838`, `:441`, `:886-980` | confirmed |
| F-09 | `cloud_oauth:2206`, `:2271-2290`, `:480-488`; `stage-b/fixture-pin.txt` | confirmed by fixture (the `TypeError`) |
| F-10 | `cloud_content_restore:1405-1407`; `backuptool:1885`; `cloud_setup:69-112` | confirmed |
| F-11 | `cloud_device_id:143-145`, `:29-31` | confirmed |
| F-12 | `cloud-signin-window.c:532-534`, `:851`; `cloud_oauth:917`, `:990-1000` | confirmed |
| F-13 | `cloud_folder_validate:90`, `:252`; the tools' outputs | confirmed |
| F-14 | `stage-b/why-lines.txt`, `stage-b/es-why-sentences.txt` | confirmed |
| F-15 to F-19 | the reads named in each | confirmed |

**Narrowings made while writing:**
- F-17 first said the rule names `cloud_setup` as a writer; it names no writer of `rclone.conf` at all.
- F-16 first claimed a recount not yet run; it was run.
- F-04 was a candidate bug until the image's `tar` was run against it.

## Renovation face

### Q1 Modernize

The connection model is the newest shape (F-15). Two asymmetries are proposals for the coordinator:
- `require_manual()` for a new `create` as well as `update`;
- a first connection writing `active-connection`, so the legacy fallback stops being a shape the writer itself leaves.

`cloud_oauth`'s four seams are a split proposal. The four copies of `conf_get` are one helper waiting to be shared.

### Q2 Standards

- **Player text:**
  - `tools/vocabulary-check` against the ES pin: 0 wrong of 163, over `cloud_content_backup`, `cloud_content_restore`, `cloud_setup` and `backuptool`.
  - The other ten files were read by hand against `es-player-text.md`. The departures are rclone's ERROR text on the setup page (F-07) and two why sentences without an interface pair, one of them the *"Not this"* wording (F-14).
  - `cloud_oauth`'s phone page reads in English and French, its warning about the unencrypted LAN in both.
- **Discipline without `set -e`:** the `rc=$?` and `|| return` shapes were read, not assumed. The departures are F-10's three writes.
- **Modes and owners:** § The writers, observed for every Python and busybox writer (`stage-b/fixture-mode.txt`). Everything runs as root; the 0644 files hold no credential but the PIN (F-05).
- **The temp conventions:**
  - `mktemp` checked in `backuptool` (`tmp_file`, `:237-246`);
  - checked with `|| return 5` in `cloud_setup:394`;
  - the `$$` fallbacks in the restore (F-08).

### Q3 Bugs

**(a) Where a secret can travel** (§ The secrets' paths, 28 rows):

- **F-01, a candidate bug.**
  - **The trace:** `cloud_oauth:2330-2344` takes a request's first path segment as its PIN. `_gate` (`:2308-2328`) counts a non-empty mismatch, and `pin_exhausted` (`:2196-2198`) refuses everything at ten.
  - **`Already written:`** nothing; the counter lives in memory.
  - **The VM line:** `tools/t17-pin-fixture.py --expect unfixed|fixed`, on the host now, the guest's serve next.
- **F-05, F-06, F-07, F-09, F-11, F-12:** Info and design notes, each with its line in `02`.

**(b) What the deleting path can delete** (§ The deletions):

- **F-02, a candidate bug.**
  - **The trace:** `cloud_content_restore:235-279` splits `RCLONE_NET_OPTS` into the arguments of the deleting `sync` (`:1046`) without an allowlist or a strip.
  - **`Already written:`** nothing deleted until the next apply; no migration.
  - **The VM line:** `tools/t17-content-fixture.py --expect unfixed|fixed --real-rclone <rclone>`: a save deleted unfixed, kept fixed.
  - T16's `cloud_restore` is the same seam, the coordinator's to route.
- **F-03, a candidate bug.**
  - **The trace:** `cloud_content_backup:583-585` and `:710` take any name.
  - **`Already written:`** nothing on the device; an upload already made is the cloud's.
  - **The VM line:** the same fixture, `backup-traversal`.
- **F-04,** refuted as a bug by the image's `tar`; a design note.
- **F-08, F-10:** Info.

### Q4 Package currency

- **rclone:** 1.75.2 on the image (`rclone/package.mk:7`) against the host's 1.60.1-DEV. `tools/cloud-connections-test`'s 26 and `tools/cloud-input-test`'s 9 are host verdicts until the guest repeats them.
- **webkitgtk:** the window's recipe builds against it with the DMABuf renderer off by default (blindspot 48's family, F-19).
- **M7's open issues met:** #1117 (the validator's `rclone` from `PATH`, F-13). #1111, #1113 and #1115 are cited in `03` § 3.5 and met by no finding here.
- **Upstream:** thirteen files absent and `backuptool` rewritten. Nothing upstream-carried to disposition (D-WORKFLOW-209 reaches nothing).

### Q5 Efficiency

The bounds and what the player waits for are F-18's. These scripts run from menus, not on the launch path, so time to play is not touched; the retro cites `docs/vm-qa-log.md`.

### Q6 Dead ends

**Removals: none.**
- `backuptool`'s legacy zip path is reachable while any device holds a zip: a row.
- `cloud_setup`'s console flow is reachable with no argument: a row.
- The lane's recount found no shell function named only once, and three framework-called python methods (F-16).

### Q7 Clarity and structure

**From the directory, no; from the two generated tables, yes.**
- § The writers says which statement writes each file, with its mode, lock and shape.
- § The secrets' paths says where each credential may and may not appear.
- `rclone-cloud-sync.md` names no writer of `rclone.conf` (F-17, #909).

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **F-02:** `rclone-cloud-sync.md`'s *"treat any restore-side `--delete-excluded` as a bug"* is written about `RCLONEOPTS`. A rule naming every config value that reaches a deleting statement would have put `RCLONE_NET_OPTS` beside it. A proposal for the coordinator.

### Codification gaps (proposals for the coordinator)

1. **A deleting statement takes its flags from an allowlist, never from a config value whole.** F-02's shape is in two slices' scripts.
2. **Every entry point that names a path under `/storage` checks the name the same way.** F-03 is the one that does not; the restore's regex is the model.
3. **A tool test that asserts a refusal reads its artifacts as "absent means none"** (F-13's content-scope case), so a guard that works is not reported as a failure.

## Quality self-check

- **Blindspot 13:** each scorecard row names its artifact.
- **Blindspot 22:** every fixture has a control that comes out the other way (nine icon requests; the shipped bound; a system name; a `..` member).
- **Blindspot 31:** the selection of writers came from `grep -n` at `8ebaf8daad`, not from the brief's list; two typed claims were corrected before commit (§ Finding Verification).
- **Blindspot 38:** nothing ran on a person's device or cloud. The real rclone ran against a local-backend cloud in scratch.
- **Blindspot 75:** every figure is a command at `8ebaf8daad`, counted unfiltered over 14 paths with `xargs -0`.
- **Rules read this session:** `engineering-practices.md`, `upgrade-and-install.md`, `rclone-cloud-sync.md` (the cited lines), `es-player-text.md`, `player-language.md`, `bugs-are-agent-first.md`, `vm-first.md`, `adversarial-council.md`, `issue-tracking.md`, `decision-register.md`. Decisions: D-CLOUD-023, -141, -142, -149, -175, -178, -179, -181; D-QA-021, -058, -015; D-WORKFLOW-061, -195, -209; D-UI-031, -117.



## Context 1: docs/reviews/order.md § T17

```text
### T17. cloud-sync-and-saves: cloud sync: setup, sign-in, connections, content and settings backups

- **id**: `cloud-setup-content`; **kind**: read; **lens**: security
- **why here**: handles credentials (`rclone.conf`, OAuth tokens, the sign-in window) and the only content action that deletes (`--match`, D-CLOUD-023)
- **paths** (14 paths, 11,180 lines, 11,180 read, of which 11,180 fork-own; 0 patch and config lines; reach shipped 14): areas `cloud-sync-and-saves`; globs `projects/ROCKNIX/packages/network/rclone/sources/cloud_{oauth,setup,remote,connections.py,content_backup,content_restore,content_transfer,scan,folder_validate,device_id,log_scrub}`, `projects/ROCKNIX/packages/network/cloud-signin-window/**`, `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool`
- **read before**: none
- **depth**: Extended -- security and state preservation (plan § 6c)
- **interacting subsystems** (read-only context): the sync core (`cloud-sync-core`); `post-update` and `chksysconfig`, whose state `backuptool` archives (`os-launch-control-state`); `ApiSystem` and `Settings` (`es-state-and-bridge`); the ES setup wizard and transfer page; webkitgtk (#576)
- **closing evidence**: audit folder, lint PASS, VM proofs, punch list through Phase 7, `reviewed-at` and `fixed-at` set

```


## Context 2: the brief's § 4 (its § 2, the scope, is 01's and 02's)

```text
## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`guest`, `design`); the lens is security and the depth reason state
preservation, so Q3 leads with two families of question and Q6 is small:

- **Q3 Bugs -- the lead question, in two families.**
  **(a) Where a secret can travel.** For every credential the product
  touches -- a provider's token in `rclone.conf`, the OAuth code in the
  redirect, the pin, a WebDAV or SFTP secret typed on the phone page, the
  device id -- name every sink it can reach and what masks it there: the
  file it rests in and that file's mode (`rclone.conf` 0600 by
  `mkstemp`'s default carried through `os.replace` -- **by construction,
  not yet observed**: a § 5 fixture reads the mode after `atomic()`;
  `/var/run/cloud_oauth/session.json` written under the default umask
  (`:187-193`) while its lock is 0600 (`:179`) -- what `read_state`
  exposes and whether any field can carry rclone's words; the per-session
  log `open(self.log_path, "w")` at `:915`), the logs (`log()` at `:80`
  appends to `/var/log/cloud_sync.log`, 31 call sites; `logger -t` in
  `backuptool` 38 lines, `cloud_device_id`, `cloud_scan`; the `>>> why`
  lines ES shows), stderr dropped or kept (`cloud_folder_validate:49` drops it on purpose; `cloud_connections.read_config` never echoes the dump;
  where else rclone's stderr is captured and where it goes), a packet
  (D-CLOUD-181), a screen. `cloud_log_scrub` is the measure of what has
  already leaked: its three pattern families are the shapes earlier builds
  wrote, and the question is whether any writer in these 14 still writes
  one of them. **(b) What the deleting path can delete.** `--match --apply`
  is the only content action that deletes (D-CLOUD-023), by two statements:
  `rclone delete "${DEST}/${sys}"` at `:1015` and `bounded_content_rclone
  sync ... --max-delete "${files}"` at `:1046`, both under the preview's
  count. `--max-delete` is a cap, not a transaction (the comment at
  `:1036-1044`: on rclone 1.75.0, three deletions and `--max-delete 2`
  exits 7 having removed two), so the refusals before it are the guard: the
  plan spent (`:890-893`), the context drift (`:898-900`, `SOMETHING
  CHANGED SINCE YOU CHECKED`), the empty plan (`:904-906`, `CHECK WHAT
  WOULD CHANGE FIRST`), a count above the preview's. Are both deleting
  statements reachable only under apply with a spent plan? Can
  `bounded_content_rclone` (`cloud_content_transfer:85`) be handed a verb
  from input? Is `--delete-excluded` absent from every statement (one hit
  in the 14, a comment at `cloud_content_restore:528`; 0 in code)? Does any
  `rm -rf` reach outside the scripts' own temporaries (12 sites: `backuptool`'s
  ten on `${STAGING}`, `cloud_content_transfer:110` on its ceiling dir,
  `cloud_content_restore:1271` on its scan temp)? What do the `pkill -f`
  by pattern at `cloud_setup:775-776`, `cloud_oauth:357` and `:2819` reach
  on a device, and on a host running the harness (blindspot: a pattern that
  matches a harness whose argv carries the words -- `cloud_oauth:861` says
  the serve walks `/proc` for its own kind for this reason)? The LAN phone
  page: what bounds guessing the four-digit pin (`secrets.randbelow(10000)`
  `:2062`, `compare_digest` `:2206`, `MAX_CONNECTIONS 16`,
  `REQUEST_TIMEOUT 15`, the 409s at `:2413` and `:2442`, the serve's
  timeout), and what the page serves to an unauthenticated GET? Then the
  ordinary shapes: a write unchecked (`cmd; rc=$?` on its own line), a
  pipeline judged by its last stage in a file with no `set -o pipefail`
  (every shell file but the scrubber), an unquoted expansion feeding a
  command (five known: `>> ${LOG_FILE}` at `cloud_content_backup:40`,
  `cloud_content_restore:77`, `cloud_setup:53`; `[ -f ${SYNC_CONF} ]` at
  `cloud_scan:54`, `cloud_setup:137`; constants today, each a disposition),
  the predictable `/tmp` fallbacks at `cloud_content_restore:837-838`
  (`$$` when `mktemp` fails: fail-open on a single-user device), a probe
  that cannot report absence (blindspot 22: `cloud_scan`'s `stop_on`,
  `cloud_folder_validate`'s `Unreadable`, `cloud_connections.active`'s
  legacy first remote), a success recorded from an exit status rather than
  the artifact (`backuptool`'s `.partial` then `listed_files` count then
  `mv`, `:649-655`, is the model to hold the others to). **Each bug carries
  its trace, its `Already written:` line and its VM line**; the
  `Already written:` is where state preservation lives: an archive already
  on a device or in a cloud (legacy zip, tar, `ARCHIVE_KEEP=3`, the
  `.backuptool-seeds` list), a `rclone.conf` with no `active-connection`
  beside it (the legacy first remote), a `cloud_sync-device-id` from a
  sit-tunnel kernel (#86's healing), a `content-match-plan` in an older
  shape, a `log-scrubbed` record from a build that covered one family.
- **Q2 Standards.** The player text (`es-player-text.md`): the 13 unique
  `>>> why` sentences the shell files print and `backuptool`'s own list
  (`THERE'S NOTHING TO BACK UP YET`, `A SIGN-IN WAS FOUND IN THE BACKUP`,
  `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK`, ...) against the
  outcome vocabulary and the two verbs (`BACK UP` 7, `BACKUP` 38 across the 14 by whole-word count; the digest's heuristics found no violation; `tools/vocabulary-check` reads only four of the 14 -- `cloud_content_backup`, `cloud_content_restore`, `cloud_setup`, `backuptool` -- and needs an EmulationStation checkout (`--es`, else exit 1), so the other ten's strings are the lane's own read against the rule, § 5); `cloud_oauth`'s phone page strings in both languages (the
  French phone keyboard, `31012f0ca1`). The scripts' discipline without
  `set -e`: the `|| return` and `rc=$?` shapes, read rather than assumed.
  The modes and owners of what these scripts write under `/storage/.config`,
  `/storage/.cache/cloud_sync` and `/var/run`. The three temp conventions
  (`mktemp` checked in `backuptool:239`, unchecked at `cloud_setup:394`
  with `|| return 5`, the `$$` fallback in the restore).
- **Q1 Modernize.** `cloud_connections.py` is the one writer of `rclone.conf` and the newest shape (atomic, locked, refusing): `cloud_remote create` reaches it through `connections.save`, and `cloud_setup` writes no `rclone.conf` (version 1 said otherwise; the proof corrected it). So the question is whether every path to `connections.save` -- `cloud_remote create`, the interface's connection pages by name, the harness -- takes the same lock and meets the same refusals, and whether `active()`'s legacy first-remote fallback (a `rclone.conf` with no `active-connection` beside it) is still a shape a device can hold once the new writer has written. `cloud_oauth` at 2,830 lines
  and seven classes is the largest single file the fork wrote: name its
  seams (the serve, the browser session, the phone page, the state) as a
  proposal, not a change.
- **Q4 Currency.** `rclone` 1.75.2 on the image against the host's
  1.60.1-DEV that `tools/cloud-connections-test` runs (T13's Q2 note):
  every verdict from that test is a host verdict until the guest repeats
  it. `webkitgtk`'s version and blindspot 48's constraint (video on; the
  recipe says why). M7's open issues on these scripts (#1111 connection
  folders and active selection, #1113 the phone disconnect notice, #1115
  accessibility against the validator's limits, #1117 the validator bound
  to the package's rclone): a finding that meets one is recorded with the
  number and stands against `8ebaf8daad`'s bytes. Upstream: thirteen files
  absent, `backuptool` rewritten (§ 2); the ROCKNIX tracker is not
  consulted from the lane (no network beyond the seats; D-WORKFLOW-162's
  check is the coordinator's at the PR bucket).
- **Q5 Efficiency.** The scan's bounded listings (`cloud_folder_validate`'s
  6 s / 25 s, 2 MiB, 4,096 entries), the content transfer's inactivity
  bound, the sign-in's timeouts (10 s on the opener at `:300`, 15 s on the
  redirect post at `:516`, `REQUEST_TIMEOUT 15`): each stated with what the
  player waits for, and whether `time-to-play` is touched (these scripts
  run from menus, not on the launch path; say so and cite `docs/vm-qa-log.md`).
- **Q6 Dead ends.** The digest found **0 shell functions defined and never
  named elsewhere in the 14** and three python defs referenced once that
  the framework calls (`redirect_request`, `do_GET`, `do_POST`): the lane
  re-counts and reads any `--` option parsed and never used, and the zip
  path in `backuptool` (`:487-518`: read-only for legacy archives --
  reachable while any device holds one; D-WORKFLOW-209: a disposition, a
  row). Removals none.
- **Q7 Clarity and structure.** Can a reader tell, from the directory and
  the rule, which script writes `rclone.conf`, which reads it, which
  deletes anything, which runs at boot, and where each secret may and may
  not appear? One generated table answers it (§ 6, *The writers* and *The
  secrets' paths*); the rule's drift is cited where it misleads (#909).

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. The seats (Phase 4.6) grade the
findings and the dispositions; each seat's probe comes first.

```


## Context 3: the register rows

```text
| D-CLOUD-023 | 2026-09-04 | **A third content action makes the device match the cloud, and its deletions are not recoverable locally.** Backup and restore are both copy-only, so a system removed from the cloud stayed on the device forever — found when `genesis` and `megadrive` turned out to hold byte-identical libraries. Preview, confirm, delete outright: no local `--backup-dir`, because the space reclaimed is the entire point of syncing ROMs selectively and the cloud is the backup by definition, this operation only ever removing what the cloud does not have. Contrast D-CLOUD-014, where a `--backup-dir` is kept precisely because the deleted thing exists nowhere else. Cloud → device only. | maintainer, 2026-09-04; #61 |

| D-QA-021 | 2026-09-12 | **Every read of a device's or a QA guest's config goes through a secrets filter wider than the word *password*: `grep -v -i -E 'key\|pass\|token\|user\|psk'`.** A read needs no permission (D-QA-015) but lands in a transcript, and `system.cfg`, `rclone.conf`, `get_setting` output and anything piped back over SSH can carry a sign-in; rclone writes `pass =`, `user =`, `token =`, `key =`, and the network writes `psk`. The QA guests are in scope: their credentials are throwaway, their files are the same shape, and the transcript is the same transcript. A filter written as `password` let a `pass =` line through on a guest on 2026-09-12. Practice text moved into `engineering-practices.md` by the #147 sweep; long form in `docs/device-testing-policy.md` § Reading a device's output. (source: work log 2026-09-12 05:57 UTC, `6075c64f2e`; no maintainer quote on record) | #147, `6075c64f2e` |

| D-CLOUD-141 | 2026-09-28 | **A content match is held to the plan the player approved: the preview writes its per-system plan to `/storage/.cache/cloud_sync/content-match-plan`, `--match --apply` reads it and uses it up, refuses a system missing from it or whose verb changed or whose count grew, and passes the preview's count to `--max-delete`; a listing whose exit status is not 0 (or 3/4, absent) plans nothing for that system.** A fork resolved in the audit's fixes (#307 PL-001, both seats' Critical): the alternative -- a fresh plan at apply bounded by its own count -- was the guard the code's comment promised and could never trip. An apply with no plan is refused; MATCH again reruns the preview. | #307 PL-001, D-CLOUD-023 |

| D-CLOUD-142 | 2026-09-28 | **`cloud_sync.conf` is never sourced with a command in it: `conf_valid` (the helper, the backup and the restore) refuses `$(` or a backtick on any line and `$`, backticks, backslashes or control characters in the five folder values, ending the run `YOUR CLOUD SYNC SETTINGS COULDN'T BE READ`; `cloud_setup` writes the conf as text and never sources it; the content scripts read the values as text.** Streams A and C on #307 PL-051 (both halves). A folder name with those characters is refused where it is typed. `Already written`: a conf an earlier build wrote with a command in it is exactly the case the readers now refuse. | #307 PL-051, PL-030 |

| D-CLOUD-149 | 2026-09-28 | **A key written twice in `cloud_sync.conf` means its first assignment, for every reader.** `conf_get` (the hub's line, `--content-location`, `--info`) now reads the first assignment as `cloud_sync_cleanup_duplicates.sh` keeps it and as the content scripts' reader does; the first round had settled the opposite for `conf_get` alone (G-C-03 gpt, G-C-06 claude: last wins), which left two readers of one file naming two folders (BS-2, blindspots 12 and 46; audit of the fix round PL-021, stream C `9c9951798b`). A value the reader cannot parse as text exits 2 and its callers refuse (G2-C-01 gpt, `98a2f9e244`). | #313 PL-021; BS-2 |

| D-CLOUD-175 | 2026-10-07 | **0.0.1 uses ordinary cloud linking, folder creation and explicit folder selection; retire the cloud-folder migration engine, automatic legacy joining/following, startup migration prompts and optional tidier. Fresh configurations default to `/pixelelated`; existing credentials and selected paths remain until explicitly changed. Users populate or rearrange their cloud folders themselves.** The maintainer says only their own installation has used the fork, raises multi-gigabyte ROMs and partially installed libraries, and says "I'm fine doing a rename on my end, and then we can abandon the migration entirely". This supersedes the move/follow/setup-step portions of D-CLOUD-158 through D-CLOUD-174 and D-UI-122 through D-UI-124; normal sync, selective transfer, defaults, stored-format guards and OS upgrade preservation remain. Historical correction: optional `/GAMES` to `/ROCKNIX` tidying was already included in the unmerged September 29 upstream PRs; automation came later. The owner's partially migrated Dropbox needs separately authorized host reconciliation, never an inferred rename/delete. | #508; supersedes #505's integration plan; ROCKNIX/distribution#3404 and ROCKNIX/emulationstation-next#40; source, UI, docs and focused VM sweep tracked by #508 |

| D-CLOUD-178 | 2026-10-07 | **Use a category validator for cloud setup, reusing existing backup/restore readers and interface building blocks. Validation itself is read-only; fixes are separate, explicit actions for game saves, save states and screenshots, with their exact plan, collision handling and verification defined before implementation. ROMs and BIOS get expected paths and manual setup instructions, never automatic library relocation.** Distinguish missing, empty, recognized misplaced and unreadable content within selected roots; folder readiness does not prove complete transfer integrity or BIOS compatibility. Preserve configured choices and do not infer cloud-wide absence. Once relevant wiki guides are published, `See instructions` opens a QR modal for the ROM or BIOS guide; no clickable-link or handheld-browser expectation. Until then, local guidance remains useful and no dead QR destination ships. Refines D-CLOUD-175/176/177; #510's direction is chosen, while #508 still needs contract reconciliation, implementation and qualification. | #510; #508; #511; maintainer's validator, reuse and QR guidance on 2026-10-07; `docs/pixelelated/cloud-folder-flow-review.md` |

| D-CLOUD-179 | 2026-10-08 | **The post-rclone setup solution is settled: place category verification, separately confirmed directory creation and explicit user actions after remote connection; use manual guidance for data-intensive ROM/BIOS organization. Make the remaining targeted game-save/save-state/screenshot repairs concrete through source-derived cases and bounded plans, not another generic design-choice question.** #515 owns that investigation and supported implementation/qualification before #508 final integration and #507's frozen delta audit; unsupported cases retain instructions with an evidence-backed disposition. The owner will manually align their experimental cloud, so no product compatibility branch or agent-led Dropbox reconciliation is required for it. Their reported experimental reset is context, not verified cloud integrity or a reset of device pointers. Refines D-CLOUD-175/177/178. | #510; #515; #508; maintainer's 2026-10-08 documentation/implementation request and Dropbox reset report; sweep: M7, #507/#508/#510, canonical session, cloud flow/menu/changelog and cloud/upgrade rules |

| D-WORKFLOW-195 | 2026-10-24 | **An Extended seat whose answer the model's output ceiling cuts on the packet is run again on a trimmed packet for that seat -- the same model, effort and provider; the analyses and tables whole, the cited files as line-numbered excerpts with context, the ask bounded -- never a model or effort substitution and never the same packet again.** `04` § Second opinion says the seats saw different evidence; an item one seat saw only in excerpt carries `excerpt`, and a disagreement that could be the excerpt's doing is resolved from the artifact, not from either seat. A fork resolved during execution on T30 (#677): Argon at `high` spent about 57k of its 65.5k output tokens reasoning on a 438 KB packet three times (`finish=length`), where T3's 308 KB packet took 30k. The maintainer may reverse it by a new row. | #677, #798; `adversarial-council.md` § Council model floor; the T30 hold post of 10:04 UTC and the coordinator's answer the same hour |
```


## Context 4: the interface's why table and its log of cloud_remote (ES pin 16dbac5211, read only)

```text
AN OLD FOLDER SETTING IS IN THE WAY
ANOTHER CLOUD CHECK IS RUNNING
A SETTINGS BACKUP OR RESTORE IS ALREADY RUNNING
A SIGN-IN WAS FOUND IN THE BACKUP
CHECK WHAT WOULD CHANGE FIRST
CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.
COULDN'T FIND YOUR CLOUD FOLDER
COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS
COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN
COULDN'T RECORD WHICH CARD YOUR SAVES ARE ON
COULDN'T TELL WHICH CARD YOUR SAVES ARE ON
IT WAS STOPPED
SOME FILES DIDN'T FINISH
SOMETHING CHANGED SINCE YOU CHECKED
SOMETHING WENT WRONG
THE BACKUP COULDN'T FINISH
THE BACKUP COULDN'T FINISH WHILE GATHERING YOUR SETTINGS
THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME
THE COPY IN YOUR CLOUD ISN'T COMPLETE
THERE'S NO SETTINGS BACKUP ON THIS DEVICE YET
THERE'S NOTHING TO BACK UP YET
THE RESTORE COULDN'T FINISH
THIS DEVICE CAN'T MAKE A SETTINGS BACKUP
THIS DEVICE CAN'T RESTORE SETTINGS
THIS DEVICE'S SETTINGS BACKUP IS DAMAGED
YOUR CLOUD FOLDER COULDN'T BE READ
YOUR CLOUD FOLDERS COULDN'T BE CREATED
YOUR CLOUD SETTINGS CHANGED. CHECK AGAIN
YOUR CLOUD STOPPED ANSWERING
YOUR CLOUD STORAGE ISN'T SET UP YET
YOUR CLOUD SYNC SETTINGS COULDN'T BE READ
YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED
YOUR CLOUD WOULDN'T TAKE THE FILES
YOUR OWN BACKUP LIST NAMES A FOLDER A BACKUP CAN'T CARRY
YOUR SAVES ARE ON A DIFFERENT CARD
YOUR SAVES CHANGED CARDS PART-WAY THROUGH
YOUR SAVES FOLDER ISN'T ON THIS DEVICE
YOU WENT OFFLINE PART-WAY THROUGH

$ grep -rn 'cloud_remote create' es-app/src (the ES checkout at HEAD 16dbac5211, the pin; a read)
es-app/src/guis/GuiMenu.cpp:7414:						LOG(LogInfo) << "cloud_remote create: " << Utils::String::maskSecrets(out);
exit 0
```


## projects/ROCKNIX/packages/network/cloud-signin-window/package.mk @ 8ebaf8daad (whole, 27 lines)

```text
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    3  
    4  PKG_NAME="cloud-signin-window"
    5  PKG_VERSION=""
    6  PKG_LICENSE="GPL-2.0"
    7  PKG_SITE="https://rocknix.org"
    8  PKG_URL=""
    9  PKG_DEPENDS_TARGET="toolchain gtk3 webkitgtk"
   10  PKG_LONGDESC="A single fullscreen web view for cloud provider sign-in. Not a browser: no address bar, no tabs, and navigation refused outside the provider's host."
   11  PKG_TOOLCHAIN="manual"
   12  
   13  # -latomic: WebKit uses 128-bit atomics, which gcc leaves to libatomic rather
   14  # than emitting inline. Linking against libwebkit2gtk without it fails on
   15  # __atomic_load_16 and friends, naming WebKit's library as if it were broken.
   16  make_target() {
   17    ${CC} ${CFLAGS} ${LDFLAGS} \
   18      ${PKG_DIR}/sources/cloud-signin-window.c \
   19      -o cloud-signin-window \
   20      $(${PKG_CONFIG} --cflags --libs gtk+-3.0 webkit2gtk-4.1) \
   21      -latomic
   22  }
   23  
   24  makeinstall_target() {
   25    mkdir -p ${INSTALL}/usr/bin
   26    cp cloud-signin-window ${INSTALL}/usr/bin
   27  }
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_connections.py @ 8ebaf8daad (whole, 258 lines)

```text
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2026 pixelelated
    3  """Local connection transactions. No cloud mutations; only bounded listings.
    4  
    5  One active connection is persisted separately from credentials. Missing selection
    6  preserves the legacy first remote; an explicit empty selection never falls back.
    7  All writers share the transfer lock. New credentials are verified in a private
    8  config and only then installed; failed/cancelled attempts leave old bytes intact.
    9  """
   10  import configparser
   11  import contextlib
   12  import fcntl
   13  import os
   14  from pathlib import Path
   15  import re
   16  import subprocess
   17  import tempfile
   18  
   19  RCLONE = '/usr/bin/rclone'
   20  CONFIG = Path('/storage/.config/rclone/rclone.conf')
   21  ACTIVE = CONFIG.with_name('active-connection')
   22  LOCK = Path('/var/run/cloud_sync.lock')
   23  SYSTEM = Path('/storage/.config/system/configs/system.cfg')
   24  
   25  class Refused(Exception):
   26      pass
   27  
   28  
   29  def read_config(path= None):
   30      path = CONFIG if path is None else path
   31      raw = path.read_bytes() if path.exists() else b''
   32      parser = configparser.RawConfigParser(strict=True)
   33      parser.optionxform = str
   34      try:
   35          parser.read_string(raw.decode('utf-8'))
   36      except (UnicodeError, configparser.Error):
   37          # rclone can read encrypted configurations using its normal password
   38          # mechanism. Keep that existing capability; never echo the dump.
   39          import json
   40          try:
   41              result = subprocess.run([RCLONE, '--config', str(path), 'config', 'dump'],
   42                                      capture_output=True, text=True, timeout=8)
   43              if result.returncode:
   44                  raise ValueError()
   45              data = json.loads(result.stdout)
   46              parser = configparser.RawConfigParser(interpolation=None)
   47              parser.optionxform = str
   48              parser.read_dict(data)
   49          except (ValueError, configparser.Error, subprocess.TimeoutExpired):
   50              raise Refused('Cloud connection settings could not be read.')
   51      return raw, parser
   52  
   53  
   54  def active(config=None):
   55      if config is None:
   56          _, config = read_config()
   57      if ACTIVE.exists():
   58          value = ACTIVE.read_text().removesuffix('\n')
   59          if value and not config.has_section(value):
   60              raise Refused('The selected connection is missing. Choose a connection first.')
   61          return value
   62      return next(iter(sorted(config.sections())), '')
   63  
   64  
   65  def selection_reason():
   66      """Safe player-facing reason when no usable selected account was resolved."""
   67      _, config = read_config()
   68      return ("CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS." if config.sections()
   69              else "YOUR CLOUD STORAGE ISN'T SET UP YET")
   70  
   71  
   72  def atomic(path, data):
   73      path.parent.mkdir(parents=True, exist_ok=True)
   74      fd, name = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
   75      try:
   76          with os.fdopen(fd, 'wb') as handle:
   77              handle.write(data)
   78              handle.flush()
   79              os.fsync(handle.fileno())
   80          os.replace(name, path)
   81          directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
   82          try:
   83              os.fsync(directory)
   84          finally:
   85              os.close(directory)
   86      finally:
   87          if os.path.exists(name):
   88              os.unlink(name)
   89  
   90  
   91  def restore_selection(previous, written):
   92      # Only undo our write; never clobber an outside settings writer.
   93      if written is None or not ACTIVE.exists() or ACTIVE.read_bytes() != written:
   94          return
   95      if previous is not None:
   96          atomic(ACTIVE, previous)
   97      else:
   98          ACTIVE.unlink()
   99          directory = os.open(ACTIVE.parent, os.O_RDONLY | os.O_DIRECTORY)
  100          try:
  101              os.fsync(directory)
  102          finally:
  103              os.close(directory)
  104  
  105  
  106  @contextlib.contextmanager
  107  def locked():
  108      LOCK.parent.mkdir(parents=True, exist_ok=True)
  109      with LOCK.open('a') as handle:
  110          try:
  111              fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
  112          except BlockingIOError:
  113              raise Refused('A cloud operation is running. Wait for it to finish, then try again.')
  114          yield
  115  
  116  
  117  def require_manual():
  118      # Same literal keys as ES. Read text, never execute system.cfg.
  119      values = {}
  120      if SYSTEM.exists():
  121          for line in SYSTEM.read_text().splitlines():
  122              key, sep, value = line.partition('=')
  123              if sep:
  124                  values[key.strip()] = value.strip()
  125      if any(values.get(k) == '1' for k in ('cloudsaves.startup', 'cloudsaves.gameexit')):
  126          raise Refused('Turn off both automatic save sync options before changing this connection.')
  127  
  128  
  129  def run(args):
  130      try:
  131          result = subprocess.run([RCLONE] + args, capture_output=True, text=True, timeout=40)
  132      except subprocess.TimeoutExpired:
  133          raise Refused('The connection stopped answering. Your settings were not changed.')
  134      if result.returncode:
  135          # Never forward provider diagnostics: they may contain credentials.
  136          raise Refused('The connection could not be verified. Your settings were not changed.')
  137      return result.stdout
  138  
  139  
  140  def save(name, backend, settings, replace=False, publish=None, check_current=None):
  141      if not name or name != name.strip() or any(c in name for c in ':[]\r\n\t') or name.startswith('-'):
  142          raise Refused('Give the connection a name without colons or brackets.')
  143      with locked():
  144          existed = CONFIG.exists()
  145          original, config = read_config()
  146          exists = config.has_section(name)
  147          if replace != exists:
  148              raise Refused('Choose a different connection name.' if exists else 'This connection no longer exists.')
  149          if replace:
  150              require_manual()
  151              if config.get(name, 'type', fallback='') != backend:
  152                  raise Refused('The connection provider changed. Open its settings again.')
  153          selected = active(config)
  154          previous_selection = ACTIVE.read_bytes() if ACTIVE.exists() else None
  155          written_selection = None
  156          CONFIG.parent.mkdir(parents=True, exist_ok=True)
  157          with tempfile.TemporaryDirectory(prefix='.connection-', dir=CONFIG.parent) as directory:
  158              staged = Path(directory) / 'rclone.conf'
  159              staged.write_bytes(original)
  160              staged.chmod(0o600)
  161              args = ['--config', str(staged), 'config', 'update' if replace else 'create', name]
  162              if not replace:
  163                  args.append(backend)
  164              args.extend('%s=%s' % pair for pair in settings)
  165              args += ['--non-interactive', '--obscure']
  166              if check_current:
  167                  check_current()
  168              out = run(args)
  169              import json
  170              try:
  171                  answer = json.loads(out or '{}')
  172              except ValueError:
  173                  answer = {}
  174              if isinstance(answer, dict) and answer.get('State'):
  175                  raise Refused('This provider needs additional setup. Use a computer to finish connecting it.')
  176              # Each subprocess is bounded. Cancellation between stages avoids
  177              # starting another full wait and lets private staging be cleaned.
  178              if check_current:
  179                  check_current()
  180              run(['--config', str(staged), 'lsd', name + ':', '--contimeout', '10s', '--timeout', '20s', '--low-level-retries', '1', '--retries', '1'])
  181              if check_current:
  182                  check_current()
  183              updated, result = read_config(staged)
  184              if not result.has_section(name):
  185                  raise Refused('The connection was not saved.')
  186  
  187              def commit():
  188                  nonlocal written_selection
  189                  # Refuse an outside writer instead of overwriting its update.
  190                  current = CONFIG.read_bytes() if CONFIG.exists() else b''
  191                  if current != original:
  192                      raise Refused('Cloud settings changed during sign-in. Try again.')
  193                  # Pin the old selection BEFORE making another name visible.
  194                  # On a first connection the legacy fallback selects only it.
  195                  if not ACTIVE.exists() and config.sections():
  196                      written_selection = (selected + '\n').encode()
  197                      atomic(ACTIVE, written_selection)
  198                  atomic(CONFIG, updated)
  199  
  200              try:
  201                  if publish:
  202                      publish(commit)
  203                  else:
  204                      commit()
  205              except Exception:
  206                  # A failed success-record write must not install credentials
  207                  # that the interface reports as unsaved.
  208                  if CONFIG.exists() and CONFIG.read_bytes() == updated:
  209                      if existed:
  210                          atomic(CONFIG, original)
  211                      else:
  212                          CONFIG.unlink()
  213                  restore_selection(previous_selection, written_selection)
  214                  raise
  215      return name
  216  
  217  
  218  def select(name):
  219      with locked():
  220          require_manual()
  221          _, config = read_config()
  222          if not config.has_section(name):
  223              raise Refused('This connection no longer exists.')
  224          atomic(ACTIVE, (name + '\n').encode())
  225  
  226  
  227  def remove(name):
  228      with locked():
  229          require_manual()
  230          original, config = read_config()
  231          if not config.has_section(name):
  232              raise Refused('This connection no longer exists.')
  233          # Removing a wrapper's underlying connection would break the wrapper.
  234          for other in config.sections():
  235              if other != name and any(re.search(r'(?<![\w.-])' + re.escape(name) + ':', v) for _, v in config.items(other)):
  236                  raise Refused('Another connection uses this one. Change that connection first.')
  237          selected = active(config)
  238          with tempfile.TemporaryDirectory(prefix='.connection-', dir=CONFIG.parent) as directory:
  239              staged = Path(directory) / 'rclone.conf'
  240              staged.write_bytes(original)
  241              staged.chmod(0o600)
  242              run(['--config', str(staged), 'config', 'delete', name])
  243              updated, result = read_config(staged)
  244              if result.has_section(name):
  245                  raise Refused('The connection settings could not be changed safely.')
  246          if CONFIG.read_bytes() != original:
  247              raise Refused('Cloud settings changed. Open this page again.')
  248          # Empty selection is a tombstone: never silently use another account.
  249          previous_selection = ACTIVE.read_bytes() if ACTIVE.exists() else None
  250          written_selection = (('' if selected == name else selected) + '\n').encode()
  251          try:
  252              atomic(ACTIVE, written_selection)
  253              atomic(CONFIG, updated)
  254          except Exception:
  255              if CONFIG.exists() and CONFIG.read_bytes() == updated:
  256                  atomic(CONFIG, original)
  257              restore_selection(previous_selection, written_selection)
  258              raise
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_remote @ 8ebaf8daad (whole, 345 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # cloud_remote - configure rclone remotes without rclone's interactive TUI.
    6  #
    7  # `rclone config` asks its questions in a terminal, which on a handheld means
    8  # an SSH session from another computer. That flow fails in ways the player
    9  # cannot act on: rclone's own prompt tells them to answer N at "Use auto
   10  # config?" (correct advice for a headless machine, fatal here), the auth link
   11  # only exists in terminal scrollback, and the whole thing needs a machine that
   12  # can reach the handheld over the LAN. See fork issue #51.
   13  #
   14  # rclone supports being configured programmatically -- `rclone config create`
   15  # writes a remote non-interactively, and every OAuth backend accepts a finished
   16  # token as a plain config value. So we ask the questions ourselves, in a UI the
   17  # player already has in their hands, and hand rclone the answers.
   18  #
   19  # Commands (all output is machine-readable, for the ES front end):
   20  #   providers            TSV: tier, name, label
   21  #   subproviders <type>  TSV: value, label -- the sub-provider choice a few
   22  #                        backends make before their other options mean anything
   23  #   fields <type> [prov] TSV: name, required, password, sensitive, type,
   24  #                        default, help, choices -- filtered to the options
   25  #                        that apply to sub-provider `prov`. `choices` is how
   26  #                        many suggested values the option has, so the caller
   27  #                        can pick an input widget without fetching them.
   28  #   choices <type> <field> [prov]  TSV: value, label
   29  #   create <name> <type> [key=*** ...]    create, verify, roll back on failure
   30  #   update <name> <type> [key=*** ...]  verify and replace saved settings
   31  #   active               selected name with trailing colon; empty is failure
   32  #   select/remove <name> change local selection or remove local credentials
   33  #   list                 STATE line, then TSV: name, type, active/saved, provider
   34  #
   35  # Tiers:
   36  #   keys      no OAuth at all - a form is enough
   37  #   oauth     needs a provider sign-in, which cloud_oauth handles on-device
   38  #   plumbing  not a storage provider at all - see NOT_PROVIDERS
   39  #
   40  # Exit codes: 0 ok, 1 usage/arguments, 2 rclone failed, 3 verification failed.
   41  
   42  import json
   43  import os
   44  import subprocess
   45  import sys
   46  import cloud_connections as connections
   47  
   48  RCLONE = "/usr/bin/rclone"
   49  LOG_FILE = "/var/log/cloud_sync.log"
   50  
   51  # Every OAuth backend goes through cloud_oauth, which wraps rclone's own
   52  # `authorize` rather than reimplementing any provider's flow, so nothing here
   53  # is per-provider: the "oauth" tier is whatever rclone can authorize. (A
   54  # DRIVABLE_OAUTH constant and a table of device-flow and PKCE-paste backends
   55  # described a design that was not built; nothing read them, and they went in
   56  # #308, claude F-RS-14.) That a provider's authorize link resolves to the
   57  # provider was probed for dropbox, drive, onedrive, box, pcloud and yandex;
   58  # that its sign-in completes on the device is proved per provider.
   59  
   60  # rclone's backend list is not a list of cloud services. These wrap or
   61  # transform another remote, or are not remote at all, and offering them as
   62  # "where your saves go" ranges from meaningless to harmful: `local` would
   63  # have someone back their saves up onto the same storage the saves are on,
   64  # which is not a backup and only looks like one.
   65  NOT_PROVIDERS = {
   66      "alias", "cache", "chunker", "combine", "compress", "crypt", "hasher",
   67      "local", "memory", "union",
   68  }
   69  
   70  
   71  def log(message):
   72      """Append to the shared cloud-sync log, matching the other tools' format."""
   73      import datetime
   74      stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   75      try:
   76          with open(LOG_FILE, "a") as handle:
   77              handle.write("[%s] [INFO] [cloud_remote] %s\n" % (stamp, message))
   78      except OSError:
   79          # A full or read-only /var/log must not take the setup flow down.
   80          pass
   81  
   82  
   83  def rclone(*args, check=True):
   84      """Run rclone and return (exit code, stdout, stderr)."""
   85      proc = subprocess.run(
   86          [RCLONE] + list(args),
   87          capture_output=True, text=True,
   88      )
   89      if check and proc.returncode != 0:
   90          # The verb and the exit code -- never the arguments, never rclone's
   91          # words. `config create` carries every key=*** the player typed,
   92          # passwords among them, and this line put them in cloud_sync.log in
   93          # the clear whenever a create failed (audit #307, gpt F-RS-04: the
   94          # finding the audit refuted for cloud_oauth holds here).
   95          verb = " ".join(args[:2]) if args[:1] == ("config",) else (args[0] if args else "")
   96          log("rclone %s failed (%d)" % (verb, proc.returncode))
   97      return proc.returncode, proc.stdout, proc.stderr
   98  
   99  
  100  def load_providers():
  101      """rclone's own backend catalogue, as a list of dicts."""
  102      code, out, err = rclone("config", "providers")
  103      if code != 0:
  104          sys.stderr.write("could not read rclone's provider list\n")
  105          sys.exit(2)
  106      try:
  107          return json.loads(out)
  108      except json.JSONDecodeError as exc:
  109          sys.stderr.write("rclone's provider list was not valid JSON: %s\n" % exc)
  110          sys.exit(2)
  111  
  112  
  113  def tier_of(provider):
  114      """Which setup path this backend can use."""
  115      if provider.get("Name") in NOT_PROVIDERS:
  116          return "plumbing"
  117      names = {opt.get("Name") for opt in provider.get("Options") or []}
  118      if "token" not in names:
  119          return "keys"
  120      return "oauth"
  121  
  122  
  123  def option_applies(opt, subprovider):
  124      """Is this option relevant once `subprovider` has been chosen?
  125  
  126      Several backends gate their options on a sub-provider: koofr carries
  127      three separate options all named `password`, one each for Koofr,
  128      Digi Storage and "other", and only one of them is ever real. S3 goes
  129      further, with 51 sub-providers and options like ibm_api_key that mean
  130      nothing unless you picked IBMCOS. Rendering them all gives duplicate
  131      fields and questions about vendors the player is not using.
  132      """
  133      constraint = (opt.get("Provider") or "").strip()
  134      if not constraint:
  135          return True
  136      if constraint.startswith("!"):
  137          excluded = {p.strip() for p in constraint[1:].split(",") if p.strip()}
  138          return subprovider not in excluded
  139      allowed = {p.strip() for p in constraint.split(",") if p.strip()}
  140      return subprovider in allowed
  141  
  142  
  143  def cmd_subproviders(backend_type):
  144      """The sub-provider choice, where a backend has one."""
  145      for provider in load_providers():
  146          if provider.get("Name") != backend_type:
  147              continue
  148          for opt in provider.get("Options") or []:
  149              if opt.get("Name") != "provider":
  150                  continue
  151              for example in opt.get("Examples") or []:
  152                  help_text = (example.get("Help") or "").splitlines()
  153                  print("%s\t%s" % (
  154                      example.get("Value") or "",
  155                      help_text[0] if help_text else (example.get("Value") or ""),
  156                  ))
  157              return 0
  158          return 0
  159      sys.stderr.write("unknown backend type: %s\n" % backend_type)
  160      return 1
  161  
  162  
  163  def cmd_providers():
  164      """Every backend with the setup path it can use. Sorted for a stable UI."""
  165      rows = []
  166      for provider in load_providers():
  167          name = provider.get("Name") or ""
  168          label = (provider.get("Description") or name).splitlines()[0]
  169          rows.append((tier_of(provider), name, label))
  170      for tier, name, label in sorted(rows, key=*** r: (r[0], r[1])):
  171          print("%s\t%s\t%s" % (tier, name, label))
  172      return 0
  173  
  174  
  175  def cmd_fields(backend_type, subprovider=""):
  176      """The options a player actually has to answer for one backend.
  177  
  178      rclone exposes every knob a backend has, most of which are advanced
  179      tuning nobody should meet during setup. Show the non-advanced ones, and
  180      let the caller decide how to render required vs optional.
  181      """
  182      for provider in load_providers():
  183          if provider.get("Name") != backend_type:
  184              continue
  185          for opt in provider.get("Options") or []:
  186              if opt.get("Advanced") or opt.get("Hide"):
  187                  continue
  188              # The sub-provider choice itself is made on its own screen.
  189              if opt.get("Name") == "provider":
  190                  continue
  191              if not option_applies(opt, subprovider):
  192                  continue
  193              # These are two different things and must not be collapsed.
  194              # IsPassword means the value is a credential: mask the input and
  195              # let rclone obscure it on the way in. Sensitive only means "do
  196              # not echo this into logs" -- rclone marks sftp's host and user
  197              # that way, and password-masking a hostname would leave the
  198              # player unable to see what they typed.
  199              help_text = (opt.get("Help") or "").splitlines()
  200              print("%s\t%d\t%d\t%d\t%s\t%s\t%s\t%d" % (
  201                  opt.get("Name") or "",
  202                  1 if opt.get("Required") else 0,
  203                  1 if opt.get("IsPassword") else 0,
  204                  1 if opt.get("Sensitive") else 0,
  205                  opt.get("Type") or "string",
  206                  opt.get("DefaultStr") or "",
  207                  help_text[0] if help_text else "",
  208                  len(opt.get("Examples") or []),
  209              ))
  210          return 0
  211      sys.stderr.write("unknown backend type: %s\n" % backend_type)
  212      return 1
  213  
  214  
  215  def cmd_choices(backend_type, field, subprovider=""):
  216      """The suggested values for one option.
  217  
  218      rclone marks none of these Exclusive, so they are suggestions rather than
  219      a closed set -- but for something like webdav's `vendor` the player has
  220      no way to guess "other", so offering the list is the difference between
  221      a form they can fill in and one they cannot.
  222      """
  223      for provider in load_providers():
  224          if provider.get("Name") != backend_type:
  225              continue
  226          for opt in provider.get("Options") or []:
  227              if opt.get("Name") != field:
  228                  continue
  229              if not option_applies(opt, subprovider):
  230                  continue
  231              for example in opt.get("Examples") or []:
  232                  help_text = (example.get("Help") or "").splitlines()
  233                  value = example.get("Value")
  234                  if value is None:
  235                      continue
  236                  label = help_text[0] if help_text else str(value)
  237                  print("%s\t%s" % (value, label))
  238              return 0
  239          return 0
  240      sys.stderr.write("unknown backend type: %s\n" % backend_type)
  241      return 1
  242  
  243  
  244  def cmd_list():
  245      _, config = connections.read_config()
  246      try:
  247          selected = connections.active(config)
  248      except connections.Refused:
  249          selected = ""
  250      print("STATE=" + ("active" if selected else "unselected"))
  251      for name in sorted(config.sections()):
  252          print("%s\t%s\t%s\t%s" % (name, config.get(name, "type", fallback=""),
  253                                      "active" if name == selected else "saved", config.get(name, "provider", fallback="")))
  254      return 0
  255  
  256  
  257  def cmd_create(name, backend_type, settings, replace=False):
  258      providers = load_providers()
  259      if backend_type not in {p.get("Name") for p in providers}:
  260          raise connections.Refused("Unknown provider.")
  261      if not replace and backend_type in ("s3", "gcs", "azureblob") and not any(k == "directory_markers" for k, _ in settings):
  262          settings.append(("directory_markers", "true"))
  263      log("updating remote " + name if replace else "creating remote " + name)
  264      connections.save(name, backend_type, settings, replace=replace)
  265      print("OK=%s" % name)
  266      return 0
  267  
  268  
  269  def usage():
  270      sys.stderr.write(
  271          "usage: cloud_remote providers\n"
  272          "       cloud_remote subproviders <type>\n"
  273          "       cloud_remote fields <type> [subprovider]\n"
  274          "       cloud_remote choices <type> <field> [subprovider]\n"
  275          "       cloud_remote create <name> <type> [key=*** ...]\n"
  276          "       cloud_remote update <name> <type> [key=*** ...]\n"
  277          "       cloud_remote active\n"
  278          "       cloud_remote select|remove <name>\n"
  279          "       cloud_remote list\n")
  280      return 1
  281  
  282  
  283  def main(argv):
  284      if len(argv) < 2:
  285          return usage()
  286      command = argv[1]
  287  
  288      if command == "providers":
  289          return cmd_providers()
  290  
  291      if command == "subproviders":
  292          if len(argv) != 3:
  293              return usage()
  294          return cmd_subproviders(argv[2])
  295  
  296      if command == "choices":
  297          if len(argv) not in (4, 5):
  298              return usage()
  299          return cmd_choices(argv[2], argv[3], argv[4] if len(argv) == 5 else "")
  300  
  301      if command == "fields":
  302          if len(argv) not in (3, 4):
  303              return usage()
  304          return cmd_fields(argv[2], argv[3] if len(argv) == 4 else "")
  305  
  306      if command == "list":
  307          return cmd_list()
  308  
  309      if command == "selection-reason" and len(argv) == 2:
  310          print(connections.selection_reason())
  311          return 0
  312  
  313      if command == "active":
  314          name = connections.active()
  315          if name:
  316              print(name + ":")
  317              return 0
  318          return 1
  319  
  320      if command in ("select", "remove") and len(argv) == 3:
  321          (connections.select if command == "select" else connections.remove)(argv[2])
  322          print("OK=" + argv[2])
  323          return 0
  324  
  325      if command in ("create", "update"):
  326          if len(argv) < 4:
  327              return usage()
  328          settings = []
  329          for pair in argv[4:]:
  330              if "=" not in pair:
  331                  sys.stderr.write("expected key=*** got: %s\n" % pair)
  332                  return 1
  333              key, value = pair.split("=", 1)
  334              settings.append((key, value))
  335          return cmd_create(argv[2], argv[3], settings, replace=(command == "update"))
  336  
  337      return usage()
  338  
  339  
  340  if __name__ == "__main__":
  341      try:
  342          sys.exit(main(sys.argv))
  343      except (connections.Refused, OSError) as exc:
  344          sys.stderr.write(str(exc) + "\n" if isinstance(exc, connections.Refused) else "Cloud settings could not be read or saved.\n")
  345          sys.exit(2)
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_transfer @ 8ebaf8daad (whole, 158 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # Shared by the two content scripts. D-CLOUD-127 applies to content too:
    6  # SDK retries must not outlive inactivity, but a progressing ROM library
    7  # has no total-duration limit (#401). Keep the five-counter interpretation
    8  # aligned with cloud_backup/cloud_restore; a retry's rising total is not
    9  # progress. These helpers are sourced, never run as a separate command.
   10  
   11  child_running() {
   12      local _pid _comm state
   13      { read -r _pid _comm state _ < "/proc/$1/stat"; } 2>/dev/null || return 1
   14      [ "${state}" != "Z" ]
   15  }
   16  
   17  # The furthest rclone's stats block in the tail of a trace has got: bytes
   18  # transferred, checks done, files transferred, files deleted, entries
   19  # listed -- five integers on one line. The listed count is the Checks line's
   20  # "Listed N" (#308, the seats' claude F-CS-13): a first backup against a
   21  # folder of tens of thousands of files lists for longer than the ceiling
   22  # before its first check completes, and a count that only read checks
   23  # ended that run as a stall. The bytes line is the Transferred: with a unit in
   24  # it; the one without is the file count. A block's last line is glued to
   25  # the next block's Transferred: (the rule's "Progress output" section),
   26  # which the sed unglues. Rates, ETAs, percentages and the elapsed time are
   27  # not progress and are not read.
   28  progress_mark() {
   29      tail -c 8192 "$1" 2>/dev/null | tr '\r' '\n' | sed 's/Transferred:/\nTransferred:/g' | awk '
   30          function unit(u) {
   31              if (u ~ /^K/) return 1024
   32              if (u ~ /^M/) return 1048576
   33              if (u ~ /^G/) return 1073741824
   34              if (u ~ /^T/) return 1099511627776
   35              return 1
   36          }
   37          /^Transferred:/ {
   38              s = $0; sub(/^Transferred:[ \t]*/, "", s); sub(/ \/.*$/, "", s)
   39              n = split(s, w, " ")
   40              if (n >= 2) { b = w[1] * unit(w[2]); if (b > bytes) bytes = b }
   41              else if (n == 1 && w[1] ~ /^[0-9]+$/ && w[1] + 0 > files) files = w[1] + 0
   42          }
   43          /^Checks:/  { s = $0; sub(/^Checks:[ \t]*/, "", s);  sub(/[^0-9].*$/, "", s); if (s + 0 > checks)  checks  = s + 0
   44                        if ($0 ~ /Listed [0-9]/) { l = $0; sub(/^.*Listed /, "", l); sub(/[^0-9].*$/, "", l); if (l + 0 > listed) listed = l + 0 } }
   45          /^Deleted:/ { s = $0; sub(/^Deleted:[ \t]*/, "", s); sub(/[^0-9].*$/, "", s); if (s + 0 > deleted) deleted = s + 0 }
   46          END { printf "%.0f %.0f %.0f %.0f %.0f\n", bytes, checks, files, deleted, listed }'
   47  }
   48  
   49  # Did any count in <mark> exceed <high water>? Prints the new high water --
   50  # each field the larger of the two, so a count that falls back (a phase
   51  # that starts over) never lets an old level read as new progress -- and
   52  # returns 0 when something grew.
   53  advance_mark() {
   54      local a=($1) b=(${2:-0 0 0 0 0}) i grew=1
   55      for i in 0 1 2 3 4; do
   56          if [ "${a[$i]:-0}" -gt "${b[$i]:-0}" ] 2>/dev/null; then
   57              b[$i]="${a[$i]}"
   58              grew=0
   59          fi
   60      done
   61      echo "${b[*]}"
   62      return "${grew}"
   63  }
   64  
   65  idle_timeout_seconds() {
   66      local v="" prev="" a
   67      for a in "$@"; do
   68          case "${a}" in
   69              --timeout=*) v="${a#--timeout=}" ;;
   70              *) [ "${prev}" = "--timeout" ] && v="${a}" ;;
   71          esac
   72          prev="${a}"
   73      done
   74      case "${v}" in
   75          *h) [[ "${v%h}" =~ ^[0-9]+$ ]] && echo $(( ${v%h} * 3600 )) ;;
   76          *m) [[ "${v%m}" =~ ^[0-9]+$ ]] && echo $(( ${v%m} * 60 )) ;;
   77          *s) [[ "${v%s}" =~ ^[0-9]+$ ]] && echo "${v%s}" ;;
   78          *)  [[ "${v}" =~ ^[0-9]+$ ]] && echo "${v}" ;;
   79      esac
   80  }
   81  
   82  # A subshell keeps cleanup traps local: cloud_content_restore also owns
   83  # the scan's temporary directory. stdout remains the original stats stream;
   84  # stderr still reaches the caller, including dry-run deletion notices.
   85  bounded_content_rclone() (
   86      local dir="" pid="" tee_pid="" rc=1 ended=0
   87      local high="0 0 0 0 0" mark new since now idle ceiling=36 n
   88      local -a args=("$@")
   89      local has_progress=0 a
   90      for a in "$@"; do
   91          case "${a}" in --progress|-P) has_progress=1 ;; esac
   92      done
   93      [ "${has_progress}" -eq 1 ] || args+=(--progress)
   94      idle=$(idle_timeout_seconds "$@")
   95      [[ "${idle}" =~ ^[0-9]+$ ]] && [ "${idle}" -gt 0 ] && ceiling=$((idle + 6))
   96  
   97      stop_child() {
   98          [ -n "$1" ] || return 0
   99          if child_running "$1"; then
  100              kill -TERM "$1" 2>/dev/null
  101              local n=0
  102              while [ "${n}" -lt 30 ] && child_running "$1"; do sleep 0.1; n=$((n + 1)); done
  103              child_running "$1" && kill -KILL "$1" 2>/dev/null
  104          fi
  105          wait "$1" 2>/dev/null || true
  106      }
  107      cleanup() {
  108          stop_child "${pid}"
  109          stop_child "${tee_pid}"
  110          [ -z "${dir}" ] || rm -rf -- "${dir}"
  111      }
  112      trap cleanup EXIT
  113      trap 'exit 130' INT
  114      trap 'exit 143' TERM
  115      # Failure to create the guard is a failure of this call, never an
  116      # unbounded transfer silently accepted as guarded.
  117      if ! dir=$(mktemp -d "${CEILING_DIR_ROOT:-/var/run}/cloud-content.XXXXXX")         || ! mkfifo "${dir}/fifo"; then
  118          log_message "cannot create content transfer inactivity guard"
  119          exit 1
  120      fi
  121      : > "${dir}/trace" || exit 1
  122      tee "${dir}/trace" < "${dir}/fifo" &
  123      tee_pid=$!
  124      command rclone "${args[@]}" > "${dir}/fifo" &
  125      pid=$!
  126      since=${SECONDS}
  127      while child_running "${pid}"; do
  128          sleep 0.25
  129          now=${SECONDS}
  130          [ "${now}" -gt "${since}" ] || continue
  131          mark=$(progress_mark "${dir}/trace")
  132          if new=$(advance_mark "${mark}" "${high}"); then
  133              high="${new}"
  134              since=${SECONDS}
  135          elif [ $((now - since)) -ge "${ceiling}" ]; then
  136              ended=1
  137              stop_child "${pid}"
  138              break
  139          fi
  140      done
  141      if [ "${ended}" -eq 1 ]; then
  142          rc=124
  143          log_message "rclone $1 made no progress for ${ceiling}s; reporting 124"
  144      else
  145          wait "${pid}"; rc=$?
  146      fi
  147      pid=""
  148      # Drain the final stats before the caller prints the outcome. A
  149      # terminated test shim can leave a writer behind; do not wait forever.
  150      n=0
  151      while [ "${n}" -lt 30 ] && child_running "${tee_pid}"; do sleep 0.1; n=$((n + 1)); done
  152      stop_child "${tee_pid}"
  153      tee_pid=""
  154      if [ -s "${dir}/trace" ] && [ -n "$(tail -c1 "${dir}/trace")" ]; then
  155          printf '\n'
  156      fi
  157      exit "${rc}"
  158  )
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 72-88 (excerpt of 2830)

```text
   72  STATE_DIR = "/var/run/cloud_oauth"
   73  RCLONE = "/usr/bin/rclone"
   74  LOCAL_AUTH = "http://127.0.0.1:53682"
   75  # How long `rclone authorize` has to print its local link.
   76  AUTHORIZE_WAIT = 20
   77  LOG_FILE = "/var/log/cloud_sync.log"
   78  
   79  
   80  def log(message):
   81      import datetime
   82      stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   83      try:
   84          with open(LOG_FILE, "a") as handle:
   85              handle.write("[%s] [INFO] [cloud_oauth] %s\n" % (stamp, message))
   86      except OSError:
   87          pass
   88  
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 171-201 (excerpt of 2830)

```text
  171  _STATE_LOCK = threading.Lock()
  172  _flock, _LOCK_EX = fcntl.flock, fcntl.LOCK_EX
  173  
  174  
  175  @contextlib.contextmanager
  176  def _state_locked():
  177      with _STATE_LOCK:
  178          os.makedirs(STATE_DIR, exist_ok=True)
  179          fd = os.open(state_path("session.lock"), os.O_RDWR | os.O_CREAT, 0o600)
  180          try:
  181              _flock(fd, _LOCK_EX)
  182              yield
  183          finally:
  184              os.close(fd)
  185  
  186  
  187  def _write_whole(data):
  188      os.makedirs(STATE_DIR, exist_ok=True)
  189      path = state_path("session.json")
  190      tmp = "%s.%d.tmp" % (path, os.getpid())
  191      with open(tmp, "w") as handle:
  192          json.dump(data, handle)
  193      os.replace(tmp, path)
  194  
  195  
  196  def write_state(**fields):
  197      with _state_locked():
  198          existing = read_state()
  199          existing.update(fields)
  200          _write_whole(existing)
  201  
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 292-308 (excerpt of 2830)

```text
  292      request = urllib.request.Request(local_url)
  293  
  294      class NoRedirect(urllib.request.HTTPRedirectHandler):
  295          def redirect_request(self, *args, **kwargs):
  296              return None
  297  
  298      opener = urllib.request.build_opener(NoRedirect)
  299      try:
  300          opener.open(request, timeout=10)
  301      except urllib.error.HTTPError as exc:
  302          location = exc.headers.get("Location")
  303          if location:
  304              return location
  305      except OSError:
  306          pass
  307      return None
  308  
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 349-365 (excerpt of 2830)

```text
  349          self.rclone_says = ""
  350  
  351      def finished(self):
  352          return self.proc is not None and self.proc.poll() is not None
  353  
  354      def start(self):
  355          # A previous attempt still holding 53682 would make this one fail with
  356          # "address already in use", which reads as a provider problem.
  357          subprocess.run(["pkill", "-f", "rclone authorize"],
  358                         capture_output=True)
  359          time.sleep(1)
  360  
  361          self.proc = subprocess.Popen(
  362              [RCLONE, "authorize", self.backend, "--auth-no-open-browser"],
  363              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
  364  
  365          # The wait for the link is bounded by the clock, not by rclone. It
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 440-456 (excerpt of 2830)

```text
  440              if ok:
  441                  log("sign-in completed on the device")
  442                  if self.on_signed_in:
  443                      try:
  444                          self.on_signed_in()
  445                      except Exception as exc:      # never take the thread down
  446                          log("post-sign-in step failed: %s" % exc)
  447              else:
  448                  log("could not finish the sign-in: %s" % detail)
  449                  # Only while this attempt still speaks for the state: a
  450                  # restart may have replaced it while its remote was being
  451                  # created (G-C-02 gpt).
  452                  if not self.superseded:
  453                      self._fail_owned(detail, ("starting", "waiting", "failed"))
  454          elif not self.token and not self.superseded:
  455              # rclone ended without a token:*** the provider refused, the
  456              # exchange failed, or it was killed. Nothing else is going to
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 508-524 (excerpt of 2830)

```text
  508              # Nothing was replayed, so the attempt is still alive and they can
  509              # simply paste again -- worth distinguishing from the dead-session
  510              # case below.
  511              return False, ("Nothing was pasted. Go to the page that failed "
  512                             "to load, copy its whole address from the browser "
  513                             "bar, and paste it here.")
  514  
  515          try:
  516              urllib.request.urlopen("%s/?%s" % (LOCAL_AUTH, query), timeout=15).read()
  517          except urllib.error.HTTPError:
  518              pass  # rclone answers the redirect with its own page; not an error
  519          except OSError as exc:
  520              return False, "could not hand the code back to rclone: %s" % exc
  521  
  522          for _ in range(40):
  523              if self.token:***
  524                  return self._write_config()
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 581-602 (excerpt of 2830)

```text
  581                  commit()
  582                  state.update(status="signed-in", remote=name)
  583                  _write_whole(state)
  584          try:
  585              # authorize already obtained this token. rclone otherwise asks whether
  586              # to refresh it, leaving noninteractive configuration unfinished.
  587              # Other provider questions remain errors in connections.save.
  588              connections.save(name, self.backend,
  589                               [("token", self.token), ("config_refresh_token", "false")],
  590                               replace=getattr(self, "replace", False), publish=publish,
  591                               check_current=current_state)
  592          except (connections.Refused, OSError) as exc:
  593              log("the sign-in could not be saved; previous settings retained")
  594              return False, str(exc) if isinstance(exc, connections.Refused) else "Your cloud settings could not be saved."
  595          log("remote %s verified and saved for %s" % (name, self.backend))
  596          return True, name
  597  
  598  
  599  # What a closed or replaced attempt's own late ending says, on the phone and
  600  # in the log, when it has one to say.
  601  CLOSED_EARLY = "That sign-in was closed before it finished."
  602  
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 853-869 (excerpt of 2830)

```text
  853  
  854  def stop_other_serves():
  855      """End any other `cloud_oauth serve`, so this one can have the port.
  856  
  857      cancel only ever killed rclone; a serve left running kept port 8080 and
  858      the next attempt died on EADDRINUSE before writing any state -- so the
  859      handheld showed a blank address and nothing said why.
  860  
  861      Walks /proc rather than calling pkill: `pkill -f "cloud_oauth serve"`
  862      matches its own command line, and has killed the calling shell repeatedly
  863      in this project's history.
  864      """
  865      me = os.getpid()
  866      for entry in os.listdir("/proc"):
  867          if not entry.isdigit() or int(entry) == me:
  868              continue
  869          try:
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 907-925 (excerpt of 2830)

```text
  907          if not runtime:
  908              self.error = "no display session to show the sign-in page on"
  909              return False
  910  
  911          os.makedirs(STATE_DIR, exist_ok=True)
  912          self.log_path = state_path("window.log")
  913          # Kept rather than discarded: a window that fails to start otherwise
  914          # looks exactly like one that started and was never asked for.
  915          self.log_file = open(self.log_path, "w")
  916  
  917          env = dict(os.environ)
  918          # Where the window records the address it is showing, so the phone can
  919          # tell when the provider has moved on.
  920          env["CLOUD_SIGNIN_PAGE_FILE"] = state_path("page")
  921          env["CLOUD_SIGNIN_DONE_FILE"] = state_path("signed-in")
  922          env["CLOUD_SIGNIN_LANGUAGE"] = signin_language()
  923          # And where it records that a field on that page has had the caret,
  924          # which is when the phone's text can go across (the probe below). A
  925          # record a previous window left says nothing about this one.
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 982-1008 (excerpt of 2830)

```text
  982          if self.log_file:
  983              try:
  984                  self.log_file.close()
  985              except OSError:
  986                  pass
  987              self.log_file = None
  988  
  989  
  990  def registrable_domain(host):
  991      """dropbox.com from www.dropbox.com.
  992  
  993      Providers bounce a sign-in through their own subdomains -- Dropbox goes
  994      via marketing.dropbox.com -- so pinning navigation to the exact host the
  995      authorize URL used refuses legitimate steps of the flow. Two labels is a
  996      blunt rule that is wrong for co.uk and right for every provider rclone
  997      talks to; the window treats it as a suffix, not an exact match.
  998      """
  999      parts = [p for p in (host or "").split(".") if p]
 1000      return ".".join(parts[-2:]) if len(parts) > 2 else (host or "")
 1001  
 1002  
 1003  # Shown when the sign-in page is open on the handheld itself. That is the good
 1004  # path: the redirect completes on its own and nothing has to be copied.
 1005  #
 1006  # The keyboard below is an option, not a requirement. On a 6" handheld with a
 1007  # touchscreen, typing on the device is perfectly reasonable and this page is
 1008  # unnecessary; on a 3.5" screen driven by a d-pad it is the difference between
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 1125-1141 (excerpt of 2830)

```text
 1125  // A script that dies before it starts leaves the page saying Checking... for
 1126  // as long as it is open, its taps dead (fork #330). Said on the page, with
 1127  // the browser's words for the ROCKNIX team, instead of nothing.
 1128  window.onerror = function (message) {
 1129    phoneScriptFailed = true;
 1130    phoneStatus("warning", "broken", phoneMessages.broken + message, true);
 1131  };
 1132  (function () {
 1133    var pin = "%(pin)s";
 1134    var box = document.getElementById("kb");
 1135    var warn = document.getElementById("warn");
 1136    var state = document.getElementById("state");
 1137    var pad = document.getElementById("pad");
 1138    var statusPanel = document.getElementById("status-panel");
 1139    state.addEventListener("click", function () {
 1140      statusPanel.hidden = !statusPanel.hidden;
 1141      state.setAttribute("aria-expanded", String(!statusPanel.hidden));
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 1233-1296 (excerpt of 2830)

```text
 1233    }
 1234  
 1235    // Only what the handheld can type goes in the box: printable ASCII,
 1236    // [ -~], the US layout cloud_oauth types with. Anything else used to be
 1237    // sent, dropped at the other end without a word, and left showing here
 1238    // -- a credential altered in silence (#308 claude F-RS-16, gpt F-RS-13).
 1239    // It is taken out of the box instead, and the page says which.
 1240    //
 1241    // The line names the characters only while Show is on. With the box
 1242    // masked it counts them: a password's characters written out under a
 1243    // box that hides them is the box's masking undone (G-C-05, the audit of
 1244    // stream C).
 1245    var dropped = [];
 1246    function warnSay() {
 1247      if (!dropped.length) { warn.hidden = true; return; }
 1248      var many = dropped.length > 1;
 1249      warn.textContent = box.type === "password"
 1250        ? (many ? phoneMessages.droppedMaskedMany.replace("{count}", dropped.length)
 1251            : phoneMessages.droppedMaskedOne)
 1252        : (many ? phoneMessages.droppedVisibleMany : phoneMessages.droppedVisibleOne)
 1253            .replace("{characters}", dropped.join(" "));
 1254      warn.hidden = false;
 1255    }
 1256    function typable() {
 1257      var v = box.value, kept = v.replace(/[^ -~]/g, "");
 1258      if (kept === v) return;
 1259      dropped = v.replace(/[ -~]/g, "").split("");
 1260      box.value = kept;
 1261      warnSay();
 1262    }
 1263  
 1264    // What you typed stays visible. Clearing the box after every keystroke made
 1265    // a keyboard that looked broken -- you type and nothing appears anywhere
 1266    // you can see.
 1267    box.addEventListener("input", function () {
 1268      typable();
 1269      if (ready) deliver(box.value);
 1270    });
 1271    box.addEventListener("keydown", function (e) {
 1272      var named = {Enter: "enter", Backspace: "backspace", Tab: "tab"}[e.key];
 1273      if (!named) return;
 1274      e.preventDefault();
 1275      act(named);
 1276    });
 1277  
 1278    // Masked, because what goes through this box is mostly a password, and
 1279    // it stayed readable on the phone's screen after it was sent (#308 gpt
 1280    // F-RS-14). Show reveals it for checking; it hides again on a second
 1281    // press.
 1282    var show = document.getElementById("show");
 1283    show.addEventListener("click", function () {
 1284      var hidden = box.type === "password";
 1285      box.type = hidden ? "text" : "password";
 1286      show.textContent = hidden ? phoneMessages.hide : phoneMessages.show;
 1287      warnSay();
 1288    });
 1289  
 1290    // Local only: the handheld has moved to another field and this box still
 1291    // holds what went into the last one.
 1292    document.getElementById("clear").addEventListener("click", function () {
 1293      box.value = ""; sent = ""; dropped = []; warnSay(); box.focus();
 1294    });
 1295  
 1296    // Close page asks once, in place, in the words approved for it (D-CLOUD-164
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2054-2070 (excerpt of 2830)

```text
 2054      """
 2055  
 2056      def __init__(self, backend, remote_name, label, timeout, replace=False):
 2057          self.backend = backend
 2058          self.remote_name = remote_name
 2059          self.replace = replace
 2060          self.name = display_name(backend, label)
 2061          self.timeout = timeout
 2062          self.pin = "%04d" % secrets.randbelow(10000)
 2063          # Which serve the shared state belongs to (write_owned).
 2064          self.attempt = secrets.token_hex(6)
 2065          self.pin_attempts = 0
 2066          self.lock = threading.Lock()
 2067          self.session = None
 2068          self.browser = None
 2069          self.keyboard = RemoteKeyboard()
 2070          self.mouse = RemoteMouse()
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2126-2142 (excerpt of 2830)

```text
 2126          let go only when the window died, which is after that re-open (audit
 2127          #307 PL-018).
 2128          """
 2129          gamepad, self.gamepad = self.gamepad, None
 2130          if gamepad:
 2131              gamepad.stop()
 2132          os.makedirs(STATE_DIR, exist_ok=True)
 2133          try:
 2134              open(state_path("signed-in"), "w").close()
 2135          except OSError:
 2136              self.stop_browser()
 2137  
 2138      def start_browser(self):
 2139          """Open the provider's page here, for the handheld or a phone to drive."""
 2140          if not browser_stack_available() or not self.session:
 2141              return False
 2142          self.stop_browser()
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2188-2214 (excerpt of 2830)

```text
 2188          if gamepad:
 2189              gamepad.stop()
 2190          browser, self.browser = self.browser, None
 2191          if browser:
 2192              browser.stop()
 2193          self.keyboard.close()
 2194          self.mouse.close()
 2195  
 2196      def pin_exhausted(self):
 2197          with self.lock:
 2198              return self.pin_attempts >= 10
 2199  
 2200      def pin_failed(self):
 2201          with self.lock:
 2202              self.pin_attempts += 1
 2203              return self.pin_attempts >= 10
 2204  
 2205      def authorised(self, pin):
 2206          return secrets.compare_digest(str(pin), self.pin)
 2207  
 2208  
 2209  # What an unauthenticated client on the LAN can make this spend before the
 2210  # PIN is checked. The body was read whole, whatever Content-Length said, on
 2211  # a thread per connection with no read deadline and no limit on threads --
 2212  # memory and threads that WebKit, on a 1 GB handheld, needs more (#308 gpt
 2213  # F-RS-18). The keyboard's largest request is a paste of a few hundred
 2214  # bytes.
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2322-2352 (excerpt of 2830)

```text
 2322              elif holder.pin_failed():
 2323                  self.send_error(403, "Too many wrong PINs. Start again on "
 2324                                       "the handheld.")
 2325              else:
 2326                  self._render_pin('<div class=err>That PIN did not match.</div>',
 2327                                   supplied="")
 2328              return False
 2329  
 2330          def _supplied(self):
 2331              """The PIN, from wherever this request carries it.
 2332  
 2333              The address shown on the handheld is http://<device>:8080/7677 --
 2334              the PIN is the tail of the one thing on screen, rather than a
 2335              second number displayed beside it that only the minority who type
 2336              the address rather than scanning it will ever need. ?pin= is still
 2337              accepted: it is what the prompt below submits, and what an older
 2338              QR still in somebody's camera roll would carry.
 2339              """
 2340              parsed = urllib.parse.urlparse(self.path)
 2341              from_query = urllib.parse.parse_qs(parsed.query).get("pin", [""])[0]
 2342              if from_query:
 2343                  return from_query
 2344              return parsed.path.strip("/").split("/")[0]
 2345  
 2346          def do_GET(self):
 2347              if not self._gate(self._supplied()):
 2348                  return
 2349  
 2350              # Is the page actually up on the handheld yet? The keyboard page
 2351              # asks every couple of seconds, because it is scanned before the
 2352              # window exists and has to start working by itself when it does.
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2405-2421 (excerpt of 2830)

```text
 2405                  return
 2406              fields = urllib.parse.parse_qs(
 2407                  self.rfile.read(length).decode("utf-8", "replace"))
 2408              if not self._gate(fields.get("pin", [""])[0] or self._supplied()):
 2409                  return
 2410  
 2411              if fields.get("move") or fields.get("click") or fields.get("wheel"):
 2412                  if not holder.browser:
 2413                      self.send_response(409)
 2414                      self.send_header("Content-Length", "0")
 2415                      self.end_headers()
 2416                      return
 2417                  moved = fields.get("move", [""])[0]
 2418                  if moved:
 2419                      try:
 2420                          dx, dy = (int(float(v)) for v in moved.split(",", 1))
 2421                      except ValueError:
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2434-2463 (excerpt of 2830)

```text
 2434                  self.end_headers()
 2435                  return
 2436  
 2437              if fields.get("type") or fields.get("key"):
 2438                  if not holder.browser:
 2439                      # 409 rather than a rendered page: the keyboard posts by
 2440                      # fetch and throwing HTML at it would replace nothing and
 2441                      # tell nobody. Its own poll is what reports this state.
 2442                      self.send_response(409)
 2443                      self.send_header("Content-Length", "0")
 2444                      self.end_headers()
 2445                      return
 2446                  text = fields.get("type", [""])[0]
 2447                  named = fields.get("key", [""])[0]
 2448                  sent = holder.keyboard.type_text(text) if text else 0
 2449                  if named:
 2450                      holder.keyboard.press(named)
 2451                  self.send_response(204)
 2452                  self.send_header("Content-Length", "0")
 2453                  self.end_headers()
 2454                  # Counts only: what was typed may be a password.
 2455                  log("typed %d characters%s%s" % (
 2456                      sent, " + " + named if named else "",
 2457                      ", %d not on the keyboard" % (len(text) - sent) if len(text) > sent else ""))
 2458                  return
 2459  
 2460              if fields.get("restart"):
 2461                  ok, error = holder.start()
 2462                  # Waiting only from the starting the new attempt began with:
 2463                  # its rclone may already have died, and its collector said
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2482-2498 (excerpt of 2830)

```text
 2482                  self._render('<div class=err>%s</div>%s' % (error, again))
 2483                  return
 2484  
 2485              session = holder.session
 2486              if session is None:
 2487                  self._render('<div class=err>No sign-in is running.</div>')
 2488                  return
 2489  
 2490              ok, detail = session.submit(fields.get("code", [""])[0])
 2491              if ok:
 2492                  self._render_done(detail)
 2493                  threading.Timer(2.0, shutdown).start()
 2494                  return
 2495  
 2496              # A dead attempt gets a way forward on this page rather than an
 2497              # instruction to walk back to the handheld and redo the flow.
 2498              restart = ""
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2579-2605 (excerpt of 2830)

```text
 2579          # The port and the errno stay in the log; the state carries words
 2580          # (G-C-03, the audit of stream C).
 2581          write_owned(holder.attempt, status="failed",
 2582                      error="Something else on this handheld is using the "
 2583                            "sign-in's connection. Restart it and try again.")
 2584          return 2
 2585  
 2586      bare = "http://%s:%d" % (address, port)
 2587      url = "%s/%s" % (bare, holder.pin)
 2588      # Waiting only from starting, and only while this session is the one
 2589      # the state names. Authorize can print its link and die at once; its
 2590      # collector records failed while this was still binding, and this write
 2591      # used to put waiting over it -- a dead attempt republished, the
 2592      # handheld reading STILL WAITING until the serve's timeout (PL-032, gpt
 2593      # G2-C-02). What the state says then stands, and the serve ends.
 2594      if not write_owned(holder.attempt, owner=holder.session.gen,
 2595                         from_status=("starting",), status="waiting",
 2596                         backend=backend, url=url, address=bare,
 2597                         provider=holder.session.provider, pin=holder.pin,
 2598                         name=holder.name):
 2599          log("the sign-in ended before it could be offered")
 2600          server.server_close()
 2601          return 2
 2602  
 2603      # The window is not opened here. It covers the screen the moment it
 2604      # appears, and the address and QR the handheld is showing are how
 2605      # somebody gets a phone keyboard onto it -- opening it immediately means
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2633-2649 (excerpt of 2830)

```text
 2633              time.sleep(0.4)
 2634  
 2635      if browser_stack_available():
 2636          threading.Thread(target=open_when_asked, daemon=True).start()
 2637  
 2638      # stdout is the contract for the caller (the ES page reads these).
 2639      print("URL=%s" % url)
 2640      print("ADDRESS=%s" % bare)
 2641      print("PIN=%s" % holder.pin)
 2642      print("NAME=%s" % holder.name)
 2643      print("PROVIDER=%s" % holder.session.provider)
 2644      print("EXIT_HINT=%s" % exit_hint())
 2645      sys.stdout.flush()
 2646  
 2647      # The listener is only open while someone is actually signing in.
 2648      timer = threading.Timer(timeout, shutdown)
 2649      timer.daemon = True
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2707-2723 (excerpt of 2830)

```text
 2707          if "--phone" in argv:
 2708              open(marker, "w").close()
 2709          elif os.path.exists(marker):
 2710              try:
 2711                  os.unlink(marker)
 2712              except OSError:
 2713                  pass
 2714  
 2715          open(state_path("open-browser"), "w").close()
 2716  
 2717          # Return once the window is actually up, not once the request is
 2718          # filed. The caller's next act is to tear down its own renderer, and
 2719          # doing that before there is anything to look at leaves the player
 2720          # staring at the wallpaper for the seconds WebKit takes to start.
 2721          deadline = time.time() + 20
 2722          while time.time() < deadline:
 2723              if signin_window_running():
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2746-2762 (excerpt of 2830)

```text
 2746          while time.time() < settle and not pad_is_free():
 2747              time.sleep(0.1)
 2748          return 0
 2749  
 2750      if command == "close":
 2751          # Asked for once the caller is drawing again, so there is something
 2752          # behind the window when it goes.
 2753          os.makedirs(STATE_DIR, exist_ok=True)
 2754          open(state_path("close-browser"), "w").close()
 2755          deadline = time.time() + 10
 2756          while time.time() < deadline and signin_window_running():
 2757              time.sleep(0.2)
 2758  
 2759          # The serve process is what normally takes the window away, and it may
 2760          # not be there to do it -- it times out on its own, and a sign-in that
 2761          # finished near that deadline leaves the window with nobody to close
 2762          # it. That is a fullscreen page reading "Finishing up" sitting on top
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth @ 8ebaf8daad: lines 2811-2827 (excerpt of 2830)

```text
 2811          return 0
 2812  
 2813      if command == "status":
 2814          print(read_state().get("status", "idle"))
 2815          return 0
 2816  
 2817      if command == "cancel":
 2818          stop_other_serves()
 2819          subprocess.run(["pkill", "-f", "rclone authorize"], capture_output=True)
 2820          # Clears the address, PIN and provider link as well as the status --
 2821          # a dead session's details are not something to leave lying in
 2822          # /var/run for the next page to pick up and display.
 2823          reset_state(status="idle")
 2824          return 0
 2825  
 2826      return main([argv[0]])
 2827  
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_setup @ 8ebaf8daad: lines 45-120 (excerpt of 976)

```text
   45  
   46  SCRIPT_NAME=$(basename "$0")
   47  LOG_FILE="/var/log/cloud_sync.log"
   48  SYNC_CONF="/storage/.config/cloud_sync.conf"
   49  
   50  log_message() {
   51      local message="$1"
   52      local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
   53      echo "[${timestamp}] [INFO] [${SCRIPT_NAME}] ${message}" >> ${LOG_FILE}
   54  }
   55  
   56  # The config is shell: every cloud script sources it. So a value is written
   57  # as text between double quotes, never through a sed replacement -- where &
   58  # is the matched line and | ends the expression, so "/R&D/Saves" became
   59  # garbage and "/a|b" failed the write while OK was printed (audit #307
   60  # PL-051) -- and a value that would mean something to a shell between double
   61  # quotes (" $ ` \) is refused where it is typed (syncpath_problem).
   62  #
   63  # conf_set KEY VALUE [KEY VALUE ...] writes every pair in one pass, each
   64  # KEY=*** line replaced (every one, as the sed was) or appended, to a file
   65  # beside the config that is renamed over it: all the keys or none, and the
   66  # previous config intact when the write fails. The values reach awk through
   67  # the environment, so nothing in them is interpreted. Returns non-zero when
   68  # the config could not be written.
   69  conf_set() {
   70      local tmp="${SYNC_CONF}.tmp.$$" src="${SYNC_CONF}" n=0 i
   71      local -a pairs=() want=()
   72      # Something at the config's path that is not a file is not a config this
   73      # can write: read as "absent", `mv -f` then put the new file INSIDE a
   74      # directory there and succeeded (audit of stream C, G-C-04).
   75      if [ -e "${SYNC_CONF}" ] && [ ! -f "${SYNC_CONF}" ]; then
   76          return 1
   77      fi
   78      [ -f "${src}" ] || src=/dev/null
   79      while [ $# -ge 2 ]; do
   80          n=$((n + 1)); pairs+=("CONF_K${n}=$1" "CONF_V${n}=$2")
   81          want+=("$1=\"$2\""); shift 2
   82      done
   83      # Braced, and silenced as a whole: a redirection that fails opening the
   84      # temp file happens before a `2>/dev/null` written after it, and the
   85      # shell printed its own diagnostic -- a line number and the temp file's
   86      # path -- ahead of the caller's sentence (G-C-07).
   87      if { env "${pairs[@]}" CONF_N="${n}" awk '
   88          BEGIN {
   89              n = ENVIRON["CONF_N"] + 0
   90              for (i = 1; i <= n; i++) {
   91                  k[i] = ENVIRON["CONF_K" i]
   92                  line[i] = k[i] "=\"" ENVIRON["CONF_V" i] "\""
   93              }
   94          }
   95          {
   96              for (i = 1; i <= n; i++)
   97                  if (index($0, k[i] "=") == 1) { print line[i]; seen[i] = 1; next }
   98              print
   99          }
  100          END { for (i = 1; i <= n; i++) if (!seen[i]) print line[i] }
  101      ' "${src}" > "${tmp}" && mv -f "${tmp}" "${SYNC_CONF}"; } 2>/dev/null; then
  102          # Written is what the file says, not what mv returned: a regular
  103          # file at the path, holding every line asked for.
  104          [ -f "${SYNC_CONF}" ] || return 1
  105          for i in "${want[@]}"; do
  106              grep -qFx -- "${i}" "${SYNC_CONF}" 2>/dev/null || return 1
  107          done
  108          return 0
  109      fi
  110      rm -f "${tmp}" 2>/dev/null
  111      return 1
  112  }
  113  
  114  # One value from the config, read as text -- never by sourcing or eval, since
  115  # a value an earlier build wrote with $( ) in it would run (PL-051) -- and as
  116  # the scripts that run with it read it, so this and they never disagree
  117  # about a player's folder:
  118  #   - Of two assignments of a key, the FIRST: every saves run the interface
  119  #     starts is --yes, which runs cloud_sync_cleanup_duplicates.sh, which
  120  #     keeps the first and is what the file becomes; the content scripts'
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_setup @ 8ebaf8daad: lines 129-145 (excerpt of 976)

```text
  129  #     text after a closing quote, a double-quoted value with $, ` or \ in it
  130  #     (what a shell would expand there) -- as the content scripts' conf_get
  131  #     answers it and as conf_valid refuses the whole file. The first cut
  132  #     read /Mine/'My as the folder, one no script would ever use (the audit
  133  #     of the fix round, gpt G2-C-01).
  134  # Nothing when the key is absent. The same awk as cloud_content_backup's and
  135  # cloud_content_restore's conf_get, on the file SYNC_CONF names.
  136  conf_get() { # <KEY> (the content scripts' reader, mirrored so every reader agrees, D-CLOUD-149): its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
  137      [ -f ${SYNC_CONF} ] || return 0
  138      awk -v k="$1" '
  139          { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
  140          index($0, k "=") != 1 && !other \
  141              && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
  142          index($0, k "=") == 1 {
  143              s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
  144              c = substr(s, 1, 1)
  145              if (c == "\"") {
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_setup @ 8ebaf8daad: lines 216-232 (excerpt of 976)

```text
  216      # Optional connection override: when the device is reached through a
  217      # gateway that remaps its address (development setups, tunnels,
  218      # proxies), the command in this file is shown instead of the direct one.
  219      OVERRIDE_FILE="/storage/.config/cloud_setup_ssh"
  220      if [ -s "${OVERRIDE_FILE}" ]; then
  221          SSH_CMD=$(head -n1 "${OVERRIDE_FILE}")
  222          SHOW_QR=0
  223          OVERRIDE_ACTIVE=1
  224          log_message "Using connection override: ${SSH_CMD}"
  225      fi
  226  }
  227  
  228  # True when at least one inbound SSH session is established (a peer is
  229  # connected to local port 22). Reads /proc/net/tcp* directly so it works
  230  # without ss/netstat; port 22 is 0016 hex, state 01 is ESTABLISHED.
  231  ssh_session_established() {
  232      local f
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_setup @ 8ebaf8daad: lines 386-402 (excerpt of 976)

```text
  386      esac
  387  }
  388  folder_marker_read() {
  389      FOLDER_VERSION=0
  390      # Custom/legacy paths are independent choices, not a renamed layout.
  391      folder_current_namespace; local scope=$?
  392      case "${scope}" in 0) ;; 1) return 0 ;; *) return "${scope}" ;; esac
  393      local tmp rc version
  394      tmp=$(mktemp /tmp/cloud_folder_marker.XXXXXX) || return 5
  395      rclone cat "${REMOTE}${SAVES%/*}/.layout" "${RCLONE_LIST_OPTS[@]}" > "${tmp}" 2>/dev/null; rc=$?
  396      if [ "${rc}" -ne 0 ]; then
  397          rm -f "${tmp}"
  398          folder_listing "${REMOTE}${SAVES%/*}/" --files-only || return $?
  399          if printf '%s\n' "${FOLDER_LISTING}" | grep -qxF '.layout'; then
  400              echo ">>> why YOUR CLOUD STOPPED ANSWERING"
  401              return "${rc}"
  402          fi
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_setup @ 8ebaf8daad: lines 487-503 (excerpt of 976)

```text
  487      # So: ask the provider now, and attach the answer to the setting.
  488      #
  489      # Only what rclone says went wrong, never its listing. This used to read
  490      # stdout as well, so a folder that already existed and held anything --
  491      # a saves folder with savestates/ in it, which is every folder somebody
  492      # would type on a second device -- was refused as "your provider would
  493      # not accept this folder", with the folder's own contents quoted as the
  494      # reason (found by the A3 fixture on the VM pair, 2026-09-06).
  495      probe=$(rclone lsd "${remote}${path}" "${RCLONE_LIST_OPTS[@]}" --log-level ERROR 2>&1 >/dev/null | head -2)
  496      case "${probe}" in
  497          # A folder that does not exist yet is fine - it gets created on use.
  498          *"not found"*|*NoSuchBucket*|"") return 0 ;;
  499      esac
  500      # The same folder, on a server whose "missing" rclone relays as a plain
  501      # error rather than "not found" (#142). On a path-based cloud a folder
  502      # its parent lacks is a folder not created yet, whatever the words. On
  503      # a bucket the first component is a bucket name the provider judges,
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_setup @ 8ebaf8daad: lines 529-561 (excerpt of 976)

```text
  529          bucket="${path#/}"; bucket="${bucket%%/*}"
  530          echo "Your provider wouldn't accept \"${bucket}\"."
  531          echo
  532          echo "This provider keeps things in buckets, so the first part of the"
  533          echo "folder is a bucket name, not a folder - and bucket names have"
  534          echo "rules that folders do not. They are also shared with everyone"
  535          echo "else using the provider, not private to your account."
  536          echo
  537          echo "  ${probe}"
  538          echo
  539          echo "Try something like /pixelelated-saves-yourname/Saves instead."
  540      else
  541          echo "Your provider wouldn't accept this folder:"
  542          echo
  543          echo "  ${probe}"
  544      fi
  545      return 1
  546  }
  547  
  548  validation_context() {
  549      folder_values >/dev/null || return 2
  550      local remotes config_file config_id
  551      REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null) || return 2
  552      [ -n "${REMOTE}" ] || return 2
  553      config_file=$(timeout 3 rclone config file 2>/dev/null | tail -1)
  554      [ -f "${config_file}" ] && [ -r "${config_file}" ] || return 2
  555      # Only a digest leaves this scope; never print credential/config bytes.
  556      config_id=$( set -o pipefail; { printf '%s\0' "${REMOTE}" "${SAVES}" "${BACKUPS}" "${CONTENT}";
  557          sha256sum "${config_file}" || exit 1
  558          if [ -f "${SYNC_CONF}" ]; then sha256sum "${SYNC_CONF}" || exit 1; fi
  559          if [ -f /storage/.config/rclone/active-connection ]; then
  560              sha256sum /storage/.config/rclone/active-connection || exit 1
  561          fi
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_setup @ 8ebaf8daad: lines 767-784 (excerpt of 976)

```text
  767          fi
  768          log_message "Sync path changed to ${NEWPATH}"
  769          echo "OK ${NEWPATH}"
  770          exit 0
  771      ;;
  772      --free-auth-port)
  773          # Clear a stale sign-in webserver left by an interrupted
  774          # `rclone config`, so the next auto-config attempt can bind.
  775          pkill -f "rclone config" 2>/dev/null
  776          pkill -f "rclone authorize" 2>/dev/null
  777          log_message "Cleared stale processes holding the OAuth port"
  778          echo "OK"
  779          exit 0
  780      ;;
  781      --connected)
  782          # The native UI gates its connect step on this, so the player
  783          # cannot advance without an SSH session actually being open.
  784          if ssh_session_established; then
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_setup @ 8ebaf8daad: lines 789-805 (excerpt of 976)

```text
  789          exit 1
  790      ;;
  791      --seed-folders)
  792          [ "$#" -eq 2 ] && seed_categories "$2" || { echo "Choose which cloud folders to create."; exit 2; }
  793          # Resolve the account only after excluding credential/selection writers.
  794          # The brace body closes fd9 in children, as the transfer scripts do.
  795          exec 9>/var/run/cloud_sync.lock || exit 1
  796          if ! flock -n 9; then
  797              echo ">>> why ANOTHER CLOUD SYNC IS RUNNING"
  798              exit 75
  799          fi
  800          {
  801          REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
  802          [ -n "${REMOTE}" ] || { echo "ERROR no remote"; exit 2; }
  803          folder_values || exit $?
  804          seed_failed=0
  805          # Only the saves action reads/writes its historical layout guard.
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_setup @ 8ebaf8daad: lines 918-945 (excerpt of 976)

```text
  918      echo -e "\e[31mNo network connection detected.\e[0m"
  919      echo "Connect to a network first, then try again."
  920      echo
  921      echo "Press any button to exit."
  922      wait_for_button
  923      exit 1
  924  fi
  925  
  926  ROOTPASS=$(get_setting root.password)
  927  
  928  log_message "Cloud setup instructions shown (${SSH_CMD})"
  929  
  930  echo -e "\e[32m=> ${OS_NAME:-ROCKNIX} CLOUD SETUP\e[0m"
  931  echo
  932  echo "Connect from a computer on your network and follow rclone's"
  933  echo "step-by-step setup. It signs in to your cloud provider and picks"
  934  echo "the account/folder to use."
  935  echo
  936  echo -e "  1. On your computer, connect:  \e[1;36m${SSH_CMD}\e[0m"
  937  echo -e "     Password:***                   \e[1;36m${ROOTPASS:-<not set>}\e[0m"
  938  echo -e "  2. Run:                        \e[1;36mrclone config\e[0m"
  939  echo "     Choose 'n' for a new remote, pick your provider, and follow"
  940  echo "     the prompts. Defaults are fine if you are unsure."
  941  echo "     When asked 'Use auto config?', answer Y, then open the"
  942  echo "     sign-in link it prints in your computer's browser."
  943  echo "  3. Quit with 'q' when the remote is listed, then come back here."
  944  echo
  945  if [ "${SHOW_QR}" = "1" ]; then
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 69-85 (excerpt of 1589)

```text
   69  # rclone returns (0-9) and below the 128+signal range, so nothing this script
   70  # forwards can produce it. The same two numbers (75, and 69 for no network --
   71  # raised here when the link goes away under a running unit, see
   72  # stop_no_network) are what EmulationStation reads; scripts and ES ship
   73  # together.
   74  readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69
   75  
   76  log_message() {
   77      echo "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO] [${SCRIPT_NAME}] ${1}" >> ${LOG_FILE}
   78  }
   79  
   80  # One cloud transfer at a time, whoever asked for it.
   81  #
   82  # Three callers can start one: EmulationStation at boot (the startup sync,
   83  # which ran headless from autostart/102-cloud-saves until #94), EmulationStation
   84  # after a game exits, and a person in the menu. Until
   85  # 2026-09-04 the game-exit path was an OS hook with a pgrep guard; moving it
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 227-287 (excerpt of 1589)

```text
  227      # never the value (PL-015).
  228      log_message "cloud_sync.conf was not read: ${CONTENT_REMOTE}"
  229      echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
  230      echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
  231      exit 1
  232  fi
  233  # The bound falls back to the shipped value below when this is empty; a
  234  # line it cannot read is that too, and the log says so.
  235  if ! RCLONE_NET_OPTS=$(conf_get RCLONE_NET_OPTS); then
  236      log_message "RCLONE_NET_OPTS was not read (${RCLONE_NET_OPTS}); the shipped bound stands in"
  237      RCLONE_NET_OPTS=""
  238  fi
  239  case "${CONTENT_REMOTE}" in
  240      *[\$\`\\]*|*[[:cntrl:]]*)
  241          echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
  242          echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
  243          exit 1 ;;
  244  esac
  245  
  246  REMOTENAME=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active)
  247  if [ -z "${REMOTENAME}" ]; then
  248      reason=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" selection-reason 2>/dev/null) || reason="YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
  249      echo ">>> why ${reason}"
  250      echo "Choose or add a connection under GAME SETTINGS > MANAGE CLOUD STORAGE > CLOUD CONNECTIONS, then try again."
  251      exit 1
  252  fi
  253  
  254  CHECK_CONTENT="${CONTENT_REMOTE%/}"
  255  if [ -n "${CHECK_CONTENT}" ]; then
  256      case "/${CHECK_CONTENT#/}/" in
  257          *//*|*/./*|*/../*)
  258              echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
  259              exit 1 ;;
  260      esac
  261  fi
  262  ROOT="${REMOTENAME}${CONTENT_REMOTE:+${CONTENT_REMOTE%/}/}"
  263  
  264  # The bound on every rclone command below that opens a socket: RCLONE_NET_OPTS
  265  # from cloud_sync.conf, or the same shipped values when the config has no
  266  # such line yet -- this script reads the config without running
  267  # cloud_sync_helper, so on the first run after an update it may not, and the
  268  # bound is a guard that a missing line must not switch off. The reasoning
  269  # for the numbers is beside the option in cloud_sync.conf.defaults; the
  270  # short version is that rclone's own defaults (60 s connect, 5 min idle, 10
  271  # low-level retries, 3 whole-run retries) hold a run for over ten minutes
  272  # on a link that drops mid-run (#101, #102, #103). Keep the fallback in step
  273  # with the default. The two rclone calls that touch only this device --
  274  # `rclone size` and `rclone delete` on a local folder in the match flow --
  275  # open no socket and carry none of this.
  276  RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
  277  _net_opts=$(echo "${RCLONE_NET_OPTS:-}" | tr '\n\\' '  ' | tr -s ' ' | sed 's/^ //; s/ $//')
  278  [ -n "${_net_opts}" ] || _net_opts="${RCLONE_NET_OPTS_FALLBACK}"
  279  read -r -a RCLONE_NET_OPTS_ARRAY <<< "${_net_opts}"
  280  # Installed beside this script, also when the host fixtures copy it.
  281  . "$(dirname "${BASH_SOURCE[0]}")/cloud_content_transfer" || exit 1
  282  # A probe is a single listing that exists to answer quickly: one attempt,
  283  # tighter than the transfers (the same values the saves scripts probe with).
  284  readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
  285  # A listing's bound (#143): three low-level retries, not a transfer's ten --
  286  # rclone's S3 backend hands the count to the AWS SDK as attempts with
  287  # exponential backoff (see cloud_backup for the measurement).
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 291-307 (excerpt of 1589)

```text
  291  # over it, as ThreadedCloudSync::recordOutcome does. A kill mid-write leaves
  292  # the previous stamp; it used to leave an empty file (D-CLOUD-078, #105).
  293  # LAST_WHY, when a `>>> why` line was printed, becomes the stamp's third
  294  # field as a token (spaces to underscores) for the row to read (D-UI-028).
  295  LAST_WHY=""
  296  write_stamp() {
  297      local file="$1" line="$2" tmp
  298      mkdir -p "$(dirname "${file}")" 2>/dev/null
  299      tmp="${file}.tmp.$$"
  300      { printf '%s\n' "${line}" > "${tmp}"; } 2>/dev/null \
  301          && mv -f "${tmp}" "${file}" 2>/dev/null \
  302          || rm -f "${tmp}" 2>/dev/null
  303  }
  304  record_outcome() { # <stamp-name> <rc>
  305      local why=""
  306      case "$2" in
  307          0|9|"${EXIT_NO_NETWORK}"|"${EXIT_LOCK_HELD}") ;;
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 520-536 (excerpt of 1589)

```text
  520  #
  521  # Backup and restore are both copy-only, deliberately, so a system removed
  522  # from the cloud stays on the device forever and a card can never be made to
  523  # match the library. This is the third action, and the only one here that
  524  # deletes.
  525  #
  526  # Five rules, each of which has already cost something in this subsystem:
  527  #
  528  #  1. --delete-excluded NEVER appears. Save files live inside system
  529  #     directories; with the excludes in place rclone leaves excluded
  530  #     destination files alone, and that one flag inverts it into a save wipe.
  531  #  2. Only ROMs/<selected system> and BIOS. /storage/roms also holds
  532  #     savefiles, savestates, screenshots, backup, bezels, themes and music --
  533  #     other tiers' or nobody's.
  534  #  3. An empty or failed listing must never mean "delete everything". A wifi
  535  #     drop, a lapsed token and a renamed cloud folder all look exactly like an
  536  #     empty cloud, so the content root is positively confirmed to hold
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 742-758 (excerpt of 1589)

```text
  742                  log_message "match: ${sys} could not be listed (rclone exit ${lrc}); not planned"
  743                  printf '%s|fail|%s|0\n' "${sys}" "${lrc}"
  744                  return 0
  745              fi ;;
  746      esac
  747  
  748      if [ "${lrc}" -eq 0 ] && [ -n "${listing}" ]; then
  749          # Present in the cloud: sync reconciles both directions of difference.
  750          out=$(bounded_content_rclone sync "${src}" "${local_dir}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
  751                  "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
  752                  --dry-run --stats 0 2>&1)
  753          lrc=$?
  754          if [ "${lrc}" -ne 0 ]; then
  755              log_message "match: ${sys} dry run failed (rclone exit ${lrc}); not planned"
  756              printf '%s|fail|%s|0\n' "${sys}" "${lrc}"
  757              return 0
  758          fi
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 811-827 (excerpt of 1589)

```text
  811  # another card.
  812  MATCH_PLAN="/storage/.cache/cloud_sync/content-match-plan"
  813  match_plan_write() { # <plan lines>
  814      mkdir -p "$(dirname "${MATCH_PLAN}")" 2>/dev/null
  815      content_context_current || {
  816          say_why "SOMETHING CHANGED SINCE YOU CHECKED"
  817          return 1
  818      }
  819      { printf 'plan2 %s %s %s\n' "$(date +%s)" "${CONTENT_CONFIG_ID}" "${MEDIA_MODE}"; printf '%s\n' "$1" | grep '|'; } > "${MATCH_PLAN}.tmp.$$" 2>/dev/null \
  820          && mv -f "${MATCH_PLAN}.tmp.$$" "${MATCH_PLAN}" 2>/dev/null \
  821          || { rm -f "${MATCH_PLAN}.tmp.$$" 2>/dev/null; return 1; }
  822  }
  823  match_plan_of() { # <sys>: its line from the plan, or nothing
  824      [ -n "${MATCH_PLAN_TEXT}" ] || return 1
  825      printf '%s\n' "${MATCH_PLAN_TEXT}" | awk -F'|' -v s="$1" '$1 == s { print; exit }'
  826  }
  827  
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 829-846 (excerpt of 1589)

```text
  829  # system runs, its content files are listed with their sizes by the same
  830  # excludes the run uses; its rclone writes a log of its own, whose
  831  # "<path>: Deleted" lines name what went; the count and the bytes are
  832  # those names looked up in the list, added to the run's totals. The log is
  833  # then appended to the script's own.
  834  MATCH_LOG=""
  835  MATCH_BEFORE=""
  836  match_before() { # <sys>
  837      MATCH_LOG=$(mktemp /tmp/cloud-match-log.XXXXXX 2>/dev/null) || MATCH_LOG="/tmp/cloud-match-log.$$"
  838      MATCH_BEFORE=$(mktemp /tmp/cloud-match-before.XXXXXX 2>/dev/null) || MATCH_BEFORE="/tmp/cloud-match-before.$$"
  839      : > "${MATCH_LOG}"
  840      rclone lsf -R --files-only --format "sp" --separator "|" "${DEST}/$1" \
  841          "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" > "${MATCH_BEFORE}" 2>/dev/null
  842  }
  843  match_count() { # <sys>: adds what the log says went to the totals
  844      local counted cfiles cbytes
  845      counted=$(awk -F'|' -v L="${MATCH_BEFORE}" '
  846          BEGIN { while ((getline x < L) > 0) { i = index(x, "|"); sz[substr(x, i + 1)] = substr(x, 1, i - 1) } }
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 858-1068 (excerpt of 1589)

```text
  858  }
  859  
  860  match_run() {
  861      local apply="$1" sys line verb files bytes rc=0 sync_rc=0 del_rc=0 total_removed=0
  862  
  863      # The exclusions are the only thing standing between this and somebody's
  864      # saves, so assert they exist rather than trusting the file's layout. An
  865      # unset array expands to nothing and rclone would happily proceed.
  866      if [ ${#SAVE_EXCLUDES[@]} -eq 0 ] || [ ${#METADATA_EXCLUDES[@]} -eq 0 ]; then
  867          echo "Refusing: the rules that keep your saves safe aren't loaded."
  868          log_message "match: refused, exclusion arrays empty"
  869          return 1
  870      fi
  871  
  872      # The preview is read-only and may run beside a transfer; applying is one.
  873      if [ "${apply}" = "1" ]; then
  874          take_cloud_lock
  875      fi
  876      # As at the foot of the script: the rest of the run cannot leak the
  877      # lock into rclone. Closing a descriptor that was never opened (the
  878      # preview, which takes no lock) is a no-op.
  879      {
  880  
  881      # Spend the preview before checking its binding or reading the cloud.
  882      # An old-format or stale plan must never survive a refused apply.
  883      MATCH_PLAN_TEXT=""
  884      local plan_lines="" pverb pfiles pbytes plan_context="" plan_mode=""
  885      if [ "${apply}" = "1" ]; then
  886          if [ -s "${MATCH_PLAN}" ] && head -1 "${MATCH_PLAN}" | grep -qE '^plan2 [0-9]+ [0-9a-f]{64} (roms|with|only)$'; then
  887              read -r _ _ plan_context plan_mode < "${MATCH_PLAN}"
  888              MATCH_PLAN_TEXT=$(tail -n +2 "${MATCH_PLAN}")
  889          fi
  890          rm -f "${MATCH_PLAN}" 2>/dev/null
  891          if [ -e "${MATCH_PLAN}" ]; then
  892              echo "Nothing was removed: something went wrong on this device. Try again."
  893              log_message "match: refused, the preview plan could not be spent"
  894              say_why "SOMETHING WENT WRONG"
  895              record_outcome content-match 1
  896              return 1
  897          fi
  898          if ! content_context_current || { [ -n "${plan_context}" ] && { [ "${plan_context}" != "${CONTENT_CONFIG_ID}" ] || [ "${plan_mode}" != "${MEDIA_MODE}" ]; }; }; then
  899              echo "Nothing was removed: your cloud settings changed. Check what would change again."
  900              say_why "SOMETHING CHANGED SINCE YOU CHECKED"
  901              record_outcome content-match 1
  902              return 1
  903          fi
  904          if [ -z "${MATCH_PLAN_TEXT}" ]; then
  905              echo "Nothing was removed: check what would change first, then try again."
  906              say_why "CHECK WHAT WOULD CHANGE FIRST"
  907              record_outcome content-match 1
  908              return 1
  909          fi
  910      else
  911          rm -f "${MATCH_PLAN}" 2>/dev/null
  912      fi
  913  
  914      if ! cloud_root_populated; then
  915          echo "Refusing to change anything: your cloud's ROMs and BIOS folder looks empty."
  916          echo "That looks the same whether it really is empty, you're offline, or the"
  917          echo "folder was renamed - so nothing is removed."
  918          log_message "match: refused, content root lists nothing"
  919          # One of the three it can tell apart: with the network gone the
  920          # refusal is the no-network skip, and says so with the code
  921          # EmulationStation names. Nothing ran, so no stamp.
  922          if network_gone; then
  923              echo "Skipped: there's no network connection. Try again when you're online."
  924              log_message "match: skipped, no network"
  925              exit "${EXIT_NO_NETWORK}"
  926          fi
  927          return 1
  928      fi
  929  
  930      mapfile -t SYS < <(selected_systems)
  931      if [ ${#SYS[@]} -eq 0 ]; then
  932          echo "You haven't picked any systems for this device yet."
  933          return 1
  934      fi
  935  
  936      # It writes into the saves restore's tree only after its bound plan
  937      # and the current cloud/selection have passed all preflight checks.
  938      [ "${apply}" != "1" ] || tree_record_take
  939  
  940      # What the page that runs this shows when it is done. A match is mostly
  941      # deletion, and rclone's own totals for a deletion read "0 B / 0 B" --
  942      # true and useless (maintainer, 2026-09-07). So each system is announced
  943      # as a unit while it runs, and the summary at the end names what went:
  944      # the numbers the confirmation showed, per system, so the last screen
  945      # answers the first one.
  946      local total_bytes=0 removed_detail="" unit_i=0 unit_n=${#SYS[@]} planned
  947      for sys in "${SYS[@]}"; do
  948          set_system_save_excludes "${sys}"
  949          unit_i=$((unit_i + 1))
  950          # Every chosen system is an item on the page, announced before its
  951          # own dry run -- so the page names what is being checked while the
  952          # check runs -- and announced whether or not it turns out to need
  953          # anything. The page shows ITEM i OF n with this script's n, so n has
  954          # to be the number of announcements the run makes and i their running
  955          # count; until 2026-09-09 a system with nothing to do was skipped
  956          # without one, and a run over three systems ended on ITEM 2 OF 3
  957          # (#95). "Already matches the cloud" is that item's outcome, not a
  958          # reason to hide it, and counting the work first would have held the
  959          # page on WORKING with no item through one dry run per system. The
  960          # preview (apply=0) prints plan lines for the confirmation and no
  961          # markers, as before.
  962          [ "${apply}" = "1" ] && echo ">>> unit ${sys}|${unit_i}|${unit_n}"
  963          planned=$(match_plan_one "${sys}")
  964          IFS='|' read -r _ verb files bytes <<< "${planned}"
  965          if [ "${apply}" = "1" ] && [ "${verb}" != "fail" ] && [ "${verb}" != "none" ]; then
  966              # Held to the preview: the same verb, and no more to remove than
  967              # it counted -- a ROM added since, or a system gone from the
  968              # cloud since, is not what the player agreed to. The preview's
  969              # count, not this one, is what --max-delete is given.
  970              pverb=""; pfiles=""; pbytes=""
  971              IFS='|' read -r _ pverb pfiles pbytes <<< "$(match_plan_of "${sys}")"
  972              if [ -z "${pverb}" ] || [ "${verb}" != "${pverb}" ] \
  973                 || ! [ "${files}" -le "${pfiles:-0}" ] 2>/dev/null; then
  974                  echo "Nothing was removed from ${sys}: it changed since you checked. Check again to see what would change."
  975                  log_message "match: ${sys} refused: previewed ${pverb:-nothing}|${pfiles:--}, now ${verb}|${files}"
  976                  say_why "SOMETHING CHANGED SINCE YOU CHECKED"
  977                  rc=1
  978                  continue
  979              fi
  980              files="${pfiles}"; bytes="${pbytes}"
  981          fi
  982          [ "${apply}" = "1" ] || plan_lines="${plan_lines}${planned}"$'\n'
  983          case "${verb}" in
  984              fail)
  985                  # A system that could not be told is neither planned nor
  986                  # touched (PL-001). With the network gone the run is the
  987                  # no-network skip, as everywhere else here; otherwise the
  988                  # preview says so and plans nothing, and an apply says why.
  989                  if [ "${apply}" = "1" ]; then
  990                      echo "Couldn't check ${sys} against your cloud, so nothing was removed from it."
  991                  else
  992                      echo "Couldn't check ${sys} against your cloud. Try again."
  993                  fi
  994                  if network_gone; then
  995                      if [ "${apply}" = "1" ]; then
  996                          echo ">>> removed ${total_removed}|${total_bytes}|${removed_detail}"
  997                          stop_no_network match "${files}" "checking ${sys} against the cloud"
  998                      fi
  999                      echo "Skipped: there's no network connection. Try again when you're online."
 1000                      exit "${EXIT_NO_NETWORK}"
 1001                  fi
 1002                  [ "${apply}" = "1" ] && say_why "$(why_for "${files}")"
 1003                  rc=${files}
 1004                  [ "${rc}" -ne 0 ] 2>/dev/null || rc=1
 1005                  continue
 1006              ;;
 1007              none)
 1008                  [ "${apply}" = "1" ] && echo "Nothing to remove from ${sys}: it already matches the cloud."
 1009                  continue
 1010              ;;
 1011              remove)
 1012                  if [ "${apply}" = "1" ]; then
 1013                      echo "Removing ${files} files from ${sys} that aren't in your cloud..."
 1014                      match_before "${sys}"
 1015                      rclone delete "${DEST}/${sys}" \
 1016                          "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
 1017                          --max-delete "${files}" \
 1018                          --log-file "${MATCH_LOG}" --log-level INFO
 1019                      del_rc=$?
 1020                      match_count "${sys}"
 1021                      if [ ${del_rc} -ne 0 ]; then
 1022                          rc=${del_rc}
 1023                          log_message "match: removing ${sys}: rclone exit ${del_rc}"
 1024                          echo "Couldn't finish removing files from ${sys}: $(why_for "${del_rc}" | tr 'A-Z' 'a-z')."
 1025                          say_why "$(why_for "${del_rc}")"
 1026                      fi
 1027                      rmdir "${DEST}/${sys}" 2>/dev/null
 1028                  else
 1029                      echo "${sys}|remove|${files}|${bytes}"
 1030                  fi
 1031              ;;
 1032              sync)
 1033                  if [ "${apply}" = "1" ]; then
 1034                      echo "Matching ${sys} to the cloud..."
 1035                      # --max-delete is the fail-closed half: if reality has
 1036                      # drifted from the preview the player agreed to, this
 1037                      # aborts rather than deleting more than they saw.
 1038                      #
 1039                      # It is a cap, not a transaction. Measured on rclone
 1040                      # 1.75.0: given three deletions and --max-delete 2, it
 1041                      # exits 7 having already removed two. So it bounds the
 1042                      # damage to what was previewed and does not undo it --
 1043                      # the removals are final (D-CLOUD-023), which is why a
 1044                      # count above the preview's is refused before this runs.
 1045                      match_before "${sys}"
 1046                      bounded_content_rclone sync "$(remote_for "${sys}")" "${DEST}/${sys}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
 1047                          "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
 1048                          --max-delete "${files}" \
 1049                          --progress --stats 1s \
 1050                          --log-file "${MATCH_LOG}" --log-level INFO
 1051                      sync_rc=$?
 1052                      match_count "${sys}"
 1053                      if [ ${sync_rc} -ne 0 ]; then
 1054                          rc=${sync_rc}
 1055                          sweep_partials "${DEST}/${sys}"
 1056                          # A failed unit says why: the network gone ends the
 1057                          # run as 69 here, anything else carries rclone's own
 1058                          # code up as before. Before the 69 exit, the running
 1059                          # totals go out on the same `>>> removed` line the
 1060                          # completed run prints, so the page can report the
 1061                          # deletions that did happen -- a match is mostly
 1062                          # deletion, and it had already run for every system
 1063                          # before this one (D-UI-028; #105). The totals are
 1064                          # what rclone reports removed (match_count), within
 1065                          # what the player agreed to; what was removed is what
 1066                          # the cloud does not have, so it is gone (D-CLOUD-023).
 1067                          if network_gone; then
 1068                              echo ">>> removed ${total_removed}|${total_bytes}|${removed_detail}"
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 1263-1279 (excerpt of 1589)

```text
 1263          # Both sides listed by the same rule (D-CLOUD-048) as "size|relpath"
 1264          # and compared by name and size (delta_of), because totals cannot say
 1265          # whether one side has what the other has. Fields 7 and 8 are what a
 1266          # copy in that direction would send; fields 5 and 6 count the same
 1267          # set. The game list is in the totals and never in the comparison
 1268          # (below). They arrived 2026-09-08; the first six keep their position
 1269          # and type, so a page built against six still reads this line.
 1270          SUP=$(supported_systems)
 1271          TMP=$(mktemp -d /tmp/cloud-scan.XXXXXX); trap 'rm -rf "${TMP}"' EXIT
 1272          rclone lsf -R --files-only --format "sp" --separator "|" "${ROOT}ROMs/" "${RCLONE_LIST_OPTS[@]}" > "${TMP}/cloud.raw" 2>/dev/null
 1273          scan_rc=$?
 1274          if [ "${scan_rc}" -ne 0 ] && [ -s "${TMP}/cloud.raw" ]; then
 1275              echo "Couldn't finish reading your cloud. Try again." >&2
 1276              exit 5
 1277          fi
 1278          cloud_content_filter < "${TMP}/cloud.raw" > "${TMP}/cloud"
 1279          # A code other than 3 from a folder that is simply not there yet
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 1397-1419 (excerpt of 1589)

```text
 1397              fi
 1398          done
 1399          mkdir -p "$(dirname "${SELECTION}")" 2>/dev/null
 1400          # An empty selection is a real answer ("none"), distinct from never
 1401          # having chosen; the file exists either way. Which is exactly why it
 1402          # is written whole or not at all: a kill mid-write left an empty
 1403          # file, and an empty file is a different valid choice -- every later
 1404          # --selected then said no systems were selected (D-CLOUD-078, #105).
 1405          { [ ${#local_names[@]} -eq 0 ] || printf '%s\n' "${local_names[@]}"; } > "${SELECTION}.tmp.$$" 2>/dev/null
 1406          mv -f "${SELECTION}.tmp.$$" "${SELECTION}" 2>/dev/null || rm -f "${SELECTION}.tmp.$$"
 1407          echo "OK $(selected_systems | wc -l) selected"
 1408          exit 0
 1409      ;;
 1410      --selected)
 1411          mapfile -t DIRS < <(selected_systems)
 1412          # BIOS is not a system and is no longer a pick (maintainer, 2026-09-06):
 1413          # it comes with the tier whenever the cloud has it. The tier's own
 1414          # switch already says ROMS AND BIOS; nothing runs without them. A
 1415          # "bios" line in the selection -- the placeholder the interface wrote
 1416          # so that BIOS alone was not refused -- is the same thing: remote_for
 1417          # sends it to BIOS/, one unit, never to a system folder under ROMs/.
 1418          if [ "${MEDIA_MODE}" != only ] && exists_remote "${ROOT}BIOS" && ! printf '%s\n' "${DIRS[@]}" | grep -qx bios; then
 1419              DIRS+=("bios")
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore @ 8ebaf8daad: lines 1474-1495 (excerpt of 1589)

```text
 1474      ;;
 1475      *)
 1476          DIRS=("$@")
 1477      ;;
 1478  esac
 1479  
 1480  
 1481  
 1482  for DIR in "${DIRS[@]}"; do
 1483      if ! [[ "${DIR}" =~ ^[A-Za-z0-9_][A-Za-z0-9._-]*$ ]]; then
 1484          echo "That system folder name can't be used. Nothing was restored."
 1485          exit 1
 1486      fi
 1487  done
 1488  
 1489  STATUS=0
 1490  take_cloud_lock
 1491  # Everything from here to the end of the script runs with the lock
 1492  # descriptor closed, so no child of this run can hold the lock once this
 1493  # shell is gone -- see take_cloud_lock. The brace group is the whole of
 1494  # the change: it adds no subshell, so exits, traps and variables behave
 1495  # exactly as they did.
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 216-247 (excerpt of 1899)

```text
  216  # lock -- where it cannot be another run's file in flight: the backup's
  217  # .partial at the root, a pre-restore copy's .partial in archive/ (which
  218  # neither the old sweep nor the trim ever matched, so repeated cut restores
  219  # grew archive/ without bound), and a staging folder. A run that is only
  220  # interrupted (INT, TERM) removes its own staging folder on the way out
  221  # (#308, the gpt seat's F-BR-17).
  222  sweep_leftovers() {
  223      rm -f "${SETTINGS_BACKUPS}"/*.tar.gz.partial "${ARCHIVEFOLDER}"/*.tar.gz.partial 2>/dev/null
  224      rm -rf "${STAGING_PREFIX}"* 2>/dev/null
  225      return 0
  226  }
  227  trap '[ -n "${STAGING:-}" ] && rm -rf "${STAGING}"' EXIT
  228  
  229  # Every temporary file this script writes a list into comes from here, and
  230  # every caller checks the answer (#307, the audit of the fix round, PL-006).
  231  # The copy a restore takes was built from a list in a temporary whose mktemp
  232  # was never checked: a mktemp that failed gave an empty name, every write to
  233  # it went nowhere, and the empty list read as "nothing here to protect" -- so
  234  # the restore extracted over the settings with no copy taken, and a cut one
  235  # then said they were unchanged. Prints the path of a new, empty, regular
  236  # file, or nothing and returns 1; mktemp's own words go to the log.
  237  tmp_file() {
  238      local T
  239      if T=$(mktemp 2>/dev/null) && [ -n "${T}" ] && [ -f "${T}" ] && [ ! -L "${T}" ] && [ ! -s "${T}" ]
  240      then
  241          printf '%s\n' "${T}"
  242          return 0
  243      fi
  244      logger -t backuptool "a temporary file could not be made (mktemp failed or gave no file)"
  245      return 1
  246  }
  247  
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 479-526 (excerpt of 1899)

```text
  479  # time costs a few milliseconds each on a handheld's core.
  480  zip_stored_ok() { # <zip>: 0 when every stored member's bytes match its listed CRC
  481      local L CRC NAME GOT RC=0
  482      L=$(tmp_file) || return 1
  483      # The listing must carry the CRC column at all: a busybox built without
  484      # CONFIG_DESKTOP accepts -v and lists in the -l shape, and every member
  485      # would then pass unchecked (the audit of the fixes, claude G3-D-01; the
  486      # image's busybox prints it, measured 2026-09-29).
  487      if ! unzip -lv "${1}" 2>/dev/null | head -n 3 | grep -q 'CRC-32'; then
  488          logger -t backuptool "$(basename "${1}"): unzip -lv lists no CRC column; the archive's stored members cannot be checked"
  489          rm -f "${L}"
  490          return 1
  491      fi
  492      if ! ( set -o pipefail
  493             unzip -lv "${1}" 2>/dev/null | awk '
  494                 $2 == "Stored" && match($0, /[0-9][0-9]:[0-9][0-9] [0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]  /) {
  495                     print substr($0, RSTART + 6, 8) "\t" substr($0, RSTART + RLENGTH)
  496                 }' ) 2>/dev/null > "${L}"
  497      then
  498          rm -f "${L}"
  499          return 1
  500      fi
  501      while IFS=$'\t' read -r CRC NAME
  502      do
  503          case "${NAME}" in ''|*/) continue ;; esac
  504          if ! GOT=$( set -o pipefail; unzip -p "${1}" "$(glob_literal "${NAME}")" 2>/dev/null | crc32 2>/dev/null ) \
  505             || [ "${GOT%% *}" != "${CRC,,}" ]
  506          then
  507              logger -t backuptool "${NAME} in $(basename "${1}") does not match its CRC (${CRC} listed, ${GOT%% *} read)"
  508              RC=1
  509              break
  510          fi
  511      done < "${L}"
  512      rm -f "${L}"
  513      return ${RC}
  514  }
  515  archive_ok() {
  516      case "${1}" in
  517          *.tar.gz) tar -tzf "${1}" >/dev/null 2>&1 ;;
  518          *)        unzip -l "${1}" >/dev/null 2>&1 && unzip -p "${1}" >/dev/null 2>&1 && zip_stored_ok "${1}" ;;
  519      esac
  520  }
  521  
  522  # An archive's members, one per line and each whole, for either kind. Its
  523  # status is the lister's (pipefail for the zip's pipe): a listing that stops
  524  # part-way is a failure, never a shorter list -- the copy before a restore is
  525  # built from it, and a short list left files unprotected, an empty one read
  526  # as "nothing to protect" (#307, the audit of the fixes, gpt G-B-01).
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 543-566 (excerpt of 1899)

```text
  543  # one; 1 when there is none; anything else when the list cannot be read.
  544  # Every member of an archive this tool writes is a file under storage/,
  545  # named with no "." or ".." part. Extraction runs the whole archive into /
  546  # less a list of exclusions, while the copy taken before it covers only
  547  # storage/ -- so a member elsewhere (a foreign or hand-made archive's
  548  # tmp/..., or storage/../x) was written and never put back when a restore
  549  # failed, and a failed restore still said the settings were unchanged
  550  # (#307, the audit of the fix round, PL-028, from gpt G2-B-05).
  551  foreign_member() { # <members file>
  552      # busybox awk ends a file it cannot open in END, as "none found".
  553      [ -r "${1}" ] || return 2
  554      awk '{ m = $0; sub(/^\.\//, "", m) }
  555           m == "" || m == "." || m == "storage" || m == "storage/" { next }
  556           m !~ /^storage\// || ("/" m "/") ~ /\/\.\.?\// { print; found = 1; exit }
  557           END { exit !found }' "${1}" 2>/dev/null
  558  }
  559  
  560  # How many file members an archive lists, or nothing and 1 when it does not
  561  # list back whole: the count supplements tar's status, never replaces it (a
  562  # listing can print every name and then fail on a damaged tail; #307, the
  563  # audit of the fixes, gpt G-B-02).
  564  listed_files() {
  565      local L N
  566      L=$(tmp_file) || return 1
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 641-663 (excerpt of 1899)

```text
  641          rm -f "${KEEP}" "${KEEP}.unique"
  642          return 3
  643      fi
  644      if [ ! -s "${KEEP}" ]
  645      then
  646          rm -f "${KEEP}"
  647          return 4
  648      fi
  649      if ! tar -czf "${TARGET}.partial" -C / -T "${KEEP}" 2>/dev/null
  650      then
  651          rm -f "${KEEP}" "${TARGET}.partial"
  652          return 2
  653      fi
  654      if ! { LISTED=$(listed_files "${TARGET}.partial") && NKEEP_FILE=$(wc -l 2>/dev/null < "${KEEP}") \
  655             && [ "${LISTED}" -eq "${NKEEP_FILE}" ] 2>/dev/null && mv -f "${TARGET}.partial" "${TARGET}"; }
  656      then
  657          rm -f "${KEEP}" "${TARGET}.partial"
  658          return 3
  659      fi
  660      rm -f "${KEEP}"
  661      return 0
  662  }
  663  
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 1030-1046 (excerpt of 1899)

```text
 1030          # player's cloud account. There is no sanitized copy worth keeping
 1031          # -- a remote without its token is a name -- so it is held back
 1032          # outright, and a restored device connects its cloud storage again
 1033          # (thirty seconds on a phone with the wizard). Not in the default
 1034          # LOCATIONS, but a custom LOCATIONS such as /storage/.config sweeps
 1035          # it in, and the archive is synced to the cloud by design (#52).
 1036          if grep -qxF "${RCLONECFG}" "${FILELIST}"
 1037          then
 1038              logger -t backuptool "rclone.conf held back from the archive: cloud tokens never travel in a backup (#52)"
 1039          fi
 1040          for CANDIDATE in "${DEVICEONLY[@]}"
 1041          do
 1042              [ "${CANDIDATE}" = "${RCLONECFG}" ] && continue
 1043              if grep -qxF "${CANDIDATE}" "${FILELIST}"
 1044              then
 1045                  hold_back_line "${CANDIDATE}"
 1046                  logger -t backuptool "${CANDIDATE##*/} held back from the archive: a device's cloud name never travels (#307 PL-010)"
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 1175-1191 (excerpt of 1899)

```text
 1175      if [ -s "${SENDLIST}" ]
 1176      then
 1177          ( set -o pipefail
 1178            tar -cf - -T "${SENDLIST}" 2>/dev/null | tar -xf - -C "${STAGING}" 2>/dev/null )
 1179          COLLECT_RC=$?
 1180      fi
 1181      if [ "${COLLECT_RC}" -ne 0 ]
 1182      then
 1183          rm -rf "${STAGING}"
 1184          rm -f "${FILELIST}" "${SECRETLIST}" "${SENDLIST}"
 1185          return 2
 1186      fi
 1187  
 1188      # How many sanitised copies were staged in place of a file held back,
 1189      # for the member count below; and whether every one of them was written
 1190      # whole. A sanitiser that dies part-way (a read error, a full card)
 1191      # leaves a copy that exists and is short, which the count cannot see, so
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 1266-1355 (excerpt of 1899)

```text
 1266          mkdir -p "${STAGING}${SEEDLIST%/*}"
 1267          cp "${SEEDED}" "${STAGING}${SEEDLIST}" || SANITISE_RC=1
 1268          SANITISED=$((SANITISED + 1))
 1269      fi
 1270      rm -f "${SEEDED}"
 1271      if [ "${SANITISE_RC}" -ne 0 ]
 1272      then
 1273          logger -t backuptool "a sanitised copy could not be written whole; nothing written"
 1274          rm -rf "${STAGING}"
 1275          rm -f "${FILELIST}" "${SECRETLIST}" "${SENDLIST}"
 1276          return 2
 1277      fi
 1278  
 1279      # The staged tree is counted against what it was handed: every file
 1280      # the collector was given, plus each sanitised copy. A collector that
 1281      # leaves a file out and exits 0 is caught here rather than trusted
 1282      # (#307 PL-004); the archive is then counted against the tree.
 1283      local SENT STAGED LISTED
 1284      SENT=$(wc -l < "${SENDLIST}")
 1285      STAGED=$(find "${STAGING}" -type f | wc -l)
 1286      rm -f "${FILELIST}" "${SECRETLIST}" "${SENDLIST}"
 1287      if [ "${STAGED}" -ne $((SENT + SANITISED)) ]
 1288      then
 1289          logger -t backuptool "the staged copy holds ${STAGED} file(s) where $((SENT + SANITISED)) were collected; nothing written"
 1290          rm -rf "${STAGING}"
 1291          return 2
 1292      fi
 1293  
 1294      # A backup that may leave the device carries no sign-in (return 5), and
 1295      # the check reads the staged tree -- exactly what the archive is made
 1296      # from -- before the archive exists, so nothing credential-bearing is
 1297      # ever written under a name an uploader matches (#307 PL-005).
 1298      if [ "${STRIP}" = "1" ]
 1299      then
 1300          local LEAKS
 1301          if ! LEAKS=$(credential_lines "${STAGING}")
 1302          then
 1303              rm -rf "${STAGING}"
 1304              return 3
 1305          fi
 1306          if [ "${LEAKS}" -gt 0 ]
 1307          then
 1308              rm -rf "${STAGING}"
 1309              return 5
 1310          fi
 1311      fi
 1312  
 1313      # Member names come out as storage/... exactly as the zip's did, so
 1314      # anything reading the archive sees the same shape. To .partial first;
 1315      # the name every reader looks for is given only to an archive that has
 1316      # listed back whole -- every staged file, counted, not only a listing
 1317      # that ends without an error.
 1318      #
 1319      # Files only, named from a list: the folders in the staging tree were
 1320      # made by the collecting tar and by mkdir, not copied, and archiving
 1321      # them put their modes into the archive for a restore to impose on the
 1322      # device's own folders (#308, the gpt seat's F-BR-16).
 1323      local MEMBERLIST=""
 1324      if ! { MEMBERLIST=$(tmp_file) && ( cd "${STAGING}" && find storage -type f ) 2>/dev/null > "${MEMBERLIST}" \
 1325             && to_log tar -czf "${TARGET}.partial" -C "${STAGING}" -T "${MEMBERLIST}"; }
 1326      then
 1327          rm -rf "${STAGING}"
 1328          rm -f "${TARGET}.partial"
 1329          [ -n "${MEMBERLIST}" ] && rm -f "${MEMBERLIST}"
 1330          return 3
 1331      fi
 1332      rm -f "${MEMBERLIST}"
 1333      # One chain only success gets through (a count that errors is not one).
 1334      if ! { LISTED=$(listed_files "${TARGET}.partial") && [ "${LISTED}" -eq "${STAGED}" ] 2>/dev/null; }
 1335      then
 1336          logger -t backuptool "the archive does not list back whole (${LISTED:-no listing} of the ${STAGED} staged); nothing written"
 1337          rm -rf "${STAGING}"
 1338          rm -f "${TARGET}.partial"
 1339          return 3
 1340      fi
 1341      rm -rf "${STAGING}"
 1342      if ! mv -f "${TARGET}.partial" "${TARGET}"
 1343      then
 1344          rm -f "${TARGET}.partial"
 1345          return 3
 1346      fi
 1347      return 0
 1348  }
 1349  
 1350  # Keep only the newest ARCHIVE_KEEP archives under archive/. Both shapes: an
 1351  # upgraded device still has archives written under the old name, and
 1352  # rotation must not skip them and keep them for ever while trimming only the
 1353  # new ones. The pre-restore snapshots restore writes (<stamp>-PRE_RESTORE-...)
 1354  # are candidates too, so a run of restores cannot grow the folder past the
 1355  # same bound; they end in _SETTINGS.tar.gz and the first glob takes them, and
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 1487-1503 (excerpt of 1899)

```text
 1487              fail "THIS DEVICE'S SETTINGS BACKUP IS DAMAGED. NOTHING WAS CHANGED. RESTORE SETTINGS FROM THE CLOUD AGAIN, OR BACK UP SETTINGS TO REPLACE IT." "${BACKUPFILE} did not list its members whole"
 1488          fi
 1489          # Nothing is written from an archive that holds a member a settings
 1490          # restore cannot put back (foreign_member; #307, the audit of the fix
 1491          # round, PL-028). The words are proposed (D-UI-112's register).
 1492          FOREIGN=$(foreign_member "${MEMBERS}")
 1493          case $? in
 1494              0) rm -f "${MEMBERS}" "${NEWLIST}" "${SEEDS}"
 1495                 why "THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK"
 1496                 fail "THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK, SO NOTHING WAS CHANGED. RESTORE SETTINGS FROM THE CLOUD AGAIN, OR BACK UP SETTINGS TO REPLACE IT." "${BACKUPFILE} holds '${FOREIGN}', which a settings restore does not write (not a file under storage/)" ;;
 1497              1) ;;
 1498              *) rm -f "${MEMBERS}" "${NEWLIST}" "${SEEDS}"
 1499                 why "COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS"
 1500                 fail "COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS, SO NOTHING WAS CHANGED. TRY AGAIN." "the member list of ${BACKUPFILE} could not be read back" ;;
 1501          esac
 1502          # The files the backup left out as the image's own (SEEDLIST), to
 1503          # be put back to this image's copy after the extraction: a path under
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 1600-1628 (excerpt of 1899)

```text
 1600          if [ -r /proc/mounts ]
 1601          then
 1602              awk '$2 == "/storage/roms" { f = 1 } END { exit !f }' /proc/mounts 2>/dev/null
 1603              case $? in
 1604                  0) ROMS_MOUNTED=yes ;;
 1605                  1) ROMS_MOUNTED=no ;;
 1606              esac
 1607          fi
 1608          if [ -n "${SNAPSHOT}" ] || [ -s "${NEWLIST}" ]
 1609          then
 1610              if ! { { printf '%s\n' "${SNAPSHOT}"; sed 's/^/+/' "${NEWLIST}"; printf 'roms-mounted=%s\n' "${ROMS_MOUNTED}"; } > "${RESTORE_MARK}.tmp" 2>/dev/null \
 1611                     && mv -fT "${RESTORE_MARK}.tmp" "${RESTORE_MARK}" 2>/dev/null \
 1612                     && [ "$(head -n 1 "${RESTORE_MARK}" 2>/dev/null)" = "${SNAPSHOT}" ] \
 1613                     && [ "$(tail -n 1 "${RESTORE_MARK}" 2>/dev/null)" = "roms-mounted=${ROMS_MOUNTED}" ] \
 1614                     && [ "$(wc -l < "${RESTORE_MARK}")" -eq $(( 2 + $(wc -l < "${NEWLIST}") )) ] 2>/dev/null; }
 1615              then
 1616                  rm -f "${RESTORE_MARK}.tmp" "${MEMBERS}" "${NEWLIST}" 2>/dev/null
 1617                  why "COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS"
 1618                  fail "COULDN'T KEEP A COPY OF YOUR CURRENT SETTINGS, SO NOTHING WAS CHANGED. TRY AGAIN." "the restore mark ${RESTORE_MARK} could not be written"
 1619              fi
 1620          fi
 1621  
 1622          note "RESTORING SETTINGS..." "from ${BACKUPFILE}"
 1623          # A member whose path is a symlink here is the OS's to provide
 1624          # (es_systems.cfg and es_features.cfg point into /usr/config), in
 1625          # either kind of archive. Backups hold regular files only, so an
 1626          # archive member at such a path is a flattened copy -- from a zip
 1627          # written before backups skipped symlinks, or a tar from a device
 1628          # where the link had been flattened -- and extracting it would freeze
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 1814-1830 (excerpt of 1899)

```text
 1814              DEST="${ERA}/$(basename "${OLD}")"
 1815              N=1
 1816              while [ -e "${DEST}" ] || [ -L "${DEST}" ]
 1817              do
 1818                  DEST="${ERA}/$(basename "${OLD}" .zip)-kept-${BACKUP_STAMP}$([ "${N}" -gt 1 ] && echo "-${N}").zip"
 1819                  N=$((N + 1))
 1820              done
 1821              if ! { mkdir -p "${ERA}" 2>/dev/null \
 1822                     && mv -n "${OLD}" "${DEST}" 2>/dev/null \
 1823                     && [ ! -e "${OLD}" ] && [ -f "${DEST}" ]; }
 1824              then
 1825                  why "THE BACKUP COULDN'T FINISH"
 1826                  fail "THE BACKUP COULDN'T FINISH. NOTHING WAS WRITTEN, AND YOUR LAST BACKUP IS UNCHANGED. TRY AGAIN." "$(basename "${OLD}") could not be moved off the backups folder's root, where the settings upload would send it"
 1827              fi
 1828              logger -t backuptool "moved $(basename "${OLD}") from the backups folder's root to archive/upstream-era/$(basename "${DEST}"): nothing uploads it there"
 1829          done
 1830  
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool @ 8ebaf8daad: lines 1877-1893 (excerpt of 1899)

```text
 1877              # not what somebody hunting for "the one from before Tuesday"
 1878              # needs. An archive written before names carried dates has none to
 1879              # keep, so it gets one now.
 1880              PREVIOUS_NAME="$(basename "${PREVIOUS}")"
 1881              case "${PREVIOUS_NAME}" in
 1882                  [0-9][0-9][0-9][0-9]_*) ;;
 1883                  *) PREVIOUS_NAME="$(date -r "${PREVIOUS}" +%Y_%m_%d-%H%M%S 2>/dev/null || date +%Y_%m_%d-%H%M%S)-${PREVIOUS_NAME}" ;;
 1884              esac
 1885              mv "${PREVIOUS}" "${ARCHIVEFOLDER}/${PREVIOUS_NAME}"
 1886              trim_archive
 1887          fi
 1888  
 1889  
 1890          sync
 1891          note "SETTINGS BACKED UP TO THIS DEVICE." "${BACKUPFILE}"
 1892          note "COPY IT SOMEWHERE SAFE, OR BACK UP SETTINGS TO THE CLOUD UNDER GAME SETTINGS > MANAGE CLOUD STORAGE."
 1893          if [ -t 1 ]; then sleep 3; fi
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup @ 8ebaf8daad: lines 32-48 (excerpt of 799)

```text
   32  # rclone returns (0-9) and below the 128+signal range, so nothing this script
   33  # forwards can produce it. The same two numbers (75, and 69 for no network --
   34  # raised here when the link goes away under a running unit, see
   35  # stop_no_network) are what EmulationStation reads; scripts and ES ship
   36  # together.
   37  readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69
   38  
   39  log_message() {
   40      echo "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO] [${SCRIPT_NAME}] ${1}" >> ${LOG_FILE}
   41  }
   42  
   43  # One cloud transfer at a time, whoever asked for it.
   44  #
   45  # Three callers can start one: EmulationStation at boot (the startup sync,
   46  # which ran headless from autostart/102-cloud-saves until #94), EmulationStation
   47  # after a game exits, and a person in the menu. Until
   48  # 2026-09-04 the game-exit path was an OS hook with a pgrep guard; moving it
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup @ 8ebaf8daad: lines 222-240 (excerpt of 799)

```text
  222  # cloud_sync_helper, so on the first run after an update it may not, and the
  223  # bound is a guard that a missing line must not switch off. The reasoning
  224  # for the numbers is beside the option in cloud_sync.conf.defaults; the
  225  # short version is that rclone's own defaults (60 s connect, 5 min idle, 10
  226  # low-level retries, 3 whole-run retries) hold a run for over ten minutes
  227  # on a link that drops mid-run (#101, #102, #103). Keep the fallback in step
  228  # with the default.
  229  RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
  230  _net_opts=$(echo "${RCLONE_NET_OPTS:-}" | tr '\n\\' '  ' | tr -s ' ' | sed 's/^ //; s/ $//')
  231  [ -n "${_net_opts}" ] || _net_opts="${RCLONE_NET_OPTS_FALLBACK}"
  232  read -r -a RCLONE_NET_OPTS_ARRAY <<< "${_net_opts}"
  233  # Installed beside this script, also when the host fixtures copy it.
  234  . "$(dirname "${BASH_SOURCE[0]}")/cloud_content_transfer" || exit 1
  235  # A probe is a single listing that exists to answer quickly: one attempt,
  236  # tighter than the transfers (the same values the saves scripts probe with).
  237  readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
  238  # A listing's bound (#143): three low-level retries, not a transfer's ten --
  239  # rclone's S3 backend hands the count to the AWS SDK as attempts with
  240  # exponential backoff (see cloud_backup for the measurement).
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup @ 8ebaf8daad: lines 244-260 (excerpt of 799)

```text
  244  # over it, as ThreadedCloudSync::recordOutcome does. A kill mid-write leaves
  245  # the previous stamp; it used to leave an empty file (D-CLOUD-078, #105).
  246  # LAST_WHY, when a `>>> why` line was printed, becomes the stamp's third
  247  # field as a token (spaces to underscores) for the row to read (D-UI-028).
  248  LAST_WHY=""
  249  write_stamp() {
  250      local file="$1" line="$2" tmp
  251      mkdir -p "$(dirname "${file}")" 2>/dev/null
  252      tmp="${file}.tmp.$$"
  253      { printf '%s\n' "${line}" > "${tmp}"; } 2>/dev/null \
  254          && mv -f "${tmp}" "${file}" 2>/dev/null \
  255          || rm -f "${tmp}" 2>/dev/null
  256  }
  257  record_outcome() { # <stamp-name> <rc>
  258      local why=""
  259      case "$2" in
  260          0|9|"${EXIT_NO_NETWORK}"|"${EXIT_LOCK_HELD}") ;;
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup @ 8ebaf8daad: lines 575-593 (excerpt of 799)

```text
  575              record_outcome content-backup 0
  576              exit 0
  577          fi
  578      ;;
  579      "")
  580          echo "Usage: ${SCRIPT_NAME} --list | --list-sizes | --all | <dir> [<dir>...]" >&2
  581          exit 1
  582      ;;
  583      *)
  584          DIRS=("$@")
  585      ;;
  586  esac
  587  
  588  # Another sync client's unresolved dispute is not our content.
  589  #
  590  # Dropbox and Nextcloud rename the losing side of a concurrent write to
  591  # "X (Someone's conflicted copy 2026-09-03)"; Syncthing appends
  592  # ".sync-conflict-<date>". Carrying those onto a handheld doubles the storage
  593  # for no benefit -- the player cannot resolve a conflict from a games menu --
```


## projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c @ 8ebaf8daad: lines 400-416 (excerpt of 1052)

```text
  400          const char *field = text + 5;
  401          /* A field on this page has the caret: say so, once per page, for
  402           * the phone. Its text goes across from here -- not from the moment
  403           * this window's process started, while the page was still loading
  404           * and nothing could take a keystroke (the audit of the fix round,
  405           * claude G2-C-01). The load of the next page takes the record away. */
  406          if (!osk->field_recorded) {
  407              const char *field_file = g_getenv("CLOUD_SIGNIN_FIELD_FILE");
  408              if (field_file && g_file_set_contents(field_file, field, -1, NULL))
  409                  osk->field_recorded = TRUE;
  410          }
  411          /* Only on a change of field. Re-raising a keyboard the player just
  412           * dismissed, every half second (probe_tick), would be worse than
  413           * never raising it. */
  414          if (g_strcmp0(field, osk->last_field) != 0) {
  415              g_strlcpy(osk->last_field, field, sizeof(osk->last_field));
  416              /* Not for somebody who chose to type on their phone: they asked
```


## projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c @ 8ebaf8daad: lines 524-542 (excerpt of 1052)

```text
  524  
  525  /* Instrumentation, kept deliberately. Keystrokes arriving from the phone go
  526   * uinput -> kernel -> libinput -> sway -> here, and when they stopped landing
  527   * every hop but the last could be proven individually. Without this line
  528   * there is no way to tell "sway never delivered it" from "the page had
  529   * nothing focused". */
  530  static gboolean on_key(GtkWidget *widget, GdkEventKey *event, gpointer data)
  531  {
  532      if (g_getenv("CLOUD_SIGNIN_DEBUG"))
  533          g_message("key %s (%u)", event->string && *event->string ? event->string : "?",
  534                    event->keyval);
  535  
  536      /* A way out, always. The handheld's buttons are not a keyboard -- sway
  537       * reports the gamepad as a tablet_pad -- so without something mapping
  538       * them, this window covers the screen, cannot be driven from the device
  539       * and cannot be closed. Escape is what the phone's "Close page" sends,
  540       * and a keyboard plugged in; the pad's Select + Start ends the window
  541       * from cloud_oauth's side (GAMEPAD_QUIT -> stop_browser) and never
  542       * arrives here. (This said cloud_oauth mapped Start to Escape; #308
```


## projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c @ 8ebaf8daad: lines 649-668 (excerpt of 1052)

```text
  649          }
  650      }
  651      return FALSE;
  652  }
  653  
  654  /* Whether an address goes in the page file. Not rclone's loopback redirect:
  655   * http://127.0.0.1:53682/?state=...&code=... carries the OAuth code, a
  656   * credential even once redeemed, and the file is read by another process
  657   * and lives in /var/run with whatever mode the umask gives it (#308 claude
  658   * F-RS-20). The phone loses nothing -- the window turns to "Finishing up"
  659   * there. Plain C, host by host, so it can be tested without GTK. */
  660  static int page_worth_recording(const char *uri)
  661  {
  662      const char *host = uri ? strstr(uri, "://") : NULL;
  663      if (!host)
  664          return 1;
  665      host += 3;
  666      size_t n = strcspn(host, ":/?#");
  667      if (n == 9 && (strncmp(host, "127.0.0.1", 9) == 0
  668                     || strncasecmp(host, "localhost", 9) == 0))
```


## projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c @ 8ebaf8daad: lines 718-734 (excerpt of 1052)

```text
  718           * beside that page's caret (claude G2-C-01); the probe writes a new
  719           * one when a field here has it. */
  720          const char *field_file = g_getenv("CLOUD_SIGNIN_FIELD_FILE");
  721          if (field_file)
  722              g_remove(field_file);
  723          if (data)
  724              ((Osk *) data)->field_recorded = FALSE;
  725          GError *werr = NULL;
  726          if (!g_file_set_contents(page_file, uri, -1, &werr)) {
  727              if (werr) {
  728                  g_message("could not record the page: %s", werr->message);
  729                  g_error_free(werr);
  730              }
  731          }
  732      }
  733  
  734      gtk_widget_grab_focus(GTK_WIDGET(view));
```


## projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c @ 8ebaf8daad: lines 843-859 (excerpt of 1052)

```text
  843       * dropboxcaptcha.com for the form's captcha, accounts.google.com for the
  844       * "Continue with Google" button, analytics nobody asked for -- arrives
  845       * without one.
  846       *
  847       * Not frame_name: an iframe with no name attribute reports NULL exactly
  848       * as the main frame does, so that test refused the captcha anyway and
  849       * the form stayed unusable.
  850       */
  851      if (!webkit_navigation_action_is_user_gesture(action))
  852          return FALSE;
  853  
  854      const char *host = g_uri_get_host(parsed);
  855      if (!host_permitted(host)) {
  856          g_message("refused navigation to host %s", host ? host : "(none)");
  857          webkit_policy_decision_ignore(decision);
  858          return TRUE;
  859      }
```


## projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c @ 8ebaf8daad: lines 941-957 (excerpt of 1052)

```text
  941       * that path never finished loading even example.org and left the guest
  942       * unanswering, while 2.52.6 loaded it. With the DMABuf renderer off,
  943       * 2.54 takes the shared-memory path 2.52.6 took: example.org loaded on
  944       * the 1 GB guest with the window at 87 MB and the web process at 35 MB,
  945       * and on 8 GB the three processes came to 285 MB against 666 MB with it
  946       * on (2026-09-25). A sign-in page gains nothing from GPU buffers; the
  947       * memory it keeps is the game's. An environment that sets the variable
  948       * keeps its own value, so the other path stays one export away. */
  949      g_setenv("WEBKIT_DISABLE_DMABUF_RENDERER", "1", FALSE);
  950  
  951      gtk_init(&argc, &argv);
  952  
  953      static Osk osk;
  954  
  955      GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
  956      gtk_window_set_title(GTK_WINDOW(window), "Sign in");
  957      gtk_window_fullscreen(GTK_WINDOW(window));
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_device_id @ 8ebaf8daad: lines 1-38 (excerpt of 401)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # cloud_device_id - this device's stable name in cloud storage.
    6  #
    7  # Every device used to write the settings backup to one shared filename, so the
    8  # second device to run replaced the first device's archive (fork #49). Each now
    9  # gets its own folder, which needs a name that is stable for as long as the
   10  # player would call it the same device.
   11  #
   12  # The identity is generated once and kept in /storage/.config. Whatever it is
   13  # derived from, the stored value wins afterwards -- so replacing a wifi module
   14  # does not strand the backups, and the file can be edited to adopt another
   15  # device's folder deliberately. One exception, below: a stored id whose hash is
   16  # the constant every sit-tunnel kernel produced (#86) is healed on the first
   17  # run that can see a real hardware address.
   18  #
   19  # It is seeded from the permanent hardware address, because a player's idea of
   20  # "my device" is the handheld in their hands, not the installation on the card.
   21  # Seeding this way means a reflash regenerates the same identity and the device
   22  # finds its own backups again -- which is exactly the fresh-handheld journey.
   23  #
   24  #   ethtool -P reports the address burned into the adapter, not the one
   25  #   currently assigned. NetworkManager and iwd can both randomise the live
   26  #   address; the permanent one is immune, so this needs no assumption about
   27  #   their configuration.
   28  #
   29  # The address is hashed rather than stored. A MAC is a network identifier and
   30  # has no business sitting in somebody's cloud storage in the clear, where a
   31  # folder listing may be shared or synced onwards.
   32  #
   33  # Where there is no usable adapter, it falls back to /etc/machine-id, which
   34  # symlinks into /storage and is generated on first boot. That identity does not
   35  # survive a reflash -- worse, but better than none, and it only applies to a
   36  # device with no network hardware at all.
   37  #
   38  # The id file is not in backuptool's include list, so a settings archive never
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_device_id @ 8ebaf8daad: lines 112-168 (excerpt of 401)

```text
  112  valid_mac() {
  113      local lower
  114      lower=$(printf '%s' "${1}" | tr 'A-F' 'a-f')
  115      case "${lower}" in
  116          00:00:00:00:00:00|ff:ff:ff:ff:ff:ff) return 1 ;;
  117      esac
  118      [[ "${1}" =~ ^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$ ]]
  119  }
  120  
  121  permanent_address() {
  122      local name perm
  123      while IFS= read -r name; do
  124          [ -n "${name}" ] || continue
  125          perm=$(ethtool -P "${name}" 2>/dev/null | sed 's/.*: //' | tr -d ' \r\n')
  126          valid_mac "${perm}" || continue
  127          echo "${perm}"
  128          return 0
  129      done < <(usable_interfaces)
  130      return 1
  131  }
  132  
  133  # The hash of a seed, exactly as it has been computed since the first hardware
  134  # seed (aa58235112): the seed, a bar, and ${DEVICE:-unknown}, md5, ten hex.
  135  #
  136  # DEVICE is a build-system variable. On a device it is never set -- /etc/profile
  137  # exports HW_DEVICE, and nothing exports DEVICE -- so the second term is the
  138  # literal "unknown" on every handheld and the family does not join the hash.
  139  # An earlier comment here claimed it did. The recipe stays as it is anyway:
  140  # every correctly seeded device keeps its id and its pre-label folder name
  141  # under --legacy, and switching the term to HW_DEVICE would be a second
  142  # identity change that needs its own legacy variant.
  143  hash_of() {
  144      printf '%s|%s' "${1}" "${DEVICE:-unknown}" | md5sum | cut -c1-10
  145  }
  146  
  147  # What every device with a built-in sit tunnel hashed until 2026-09-08: the
  148  # string "notset", which is ee5013fc56 -- the suffix both handhelds carried.
  149  # Computed rather than written down so the derivation is in the code.
  150  poisoned_hash() {
  151      hash_of "notset"
  152  }
  153  
  154  # Does a stored id end in the poisoned hash?
  155  is_poisoned() {
  156      case "${1}" in
  157          *-"$(poisoned_hash)") return 0 ;;
  158      esac
  159      return 1
  160  }
  161  
  162  generate_id() {
  163      local seed prefix
  164  
  165      if seed=$(permanent_address); then
  166          prefix=$(hash_of "${seed}")
  167      else
  168          # No adapter to key on. machine-id is per-installation rather than
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_device_id @ 8ebaf8daad: lines 272-318 (excerpt of 401)

```text
  272      {
  273          [ -r "${PREVIOUS_FILE}" ] && tr -cd 'A-Za-z0-9_.\n-' < "${PREVIOUS_FILE}"
  274          echo
  275          if [ -e /sys/class/net/sit0 ]; then
  276              echo "$(device_label)-${poisoned}"
  277              echo "$(host_label)-${poisoned}"
  278          fi
  279      } | grep -v '^$' | awk '!seen[$0]++'
  280  }
  281  
  282  # The id file, whole or not at all: written beside itself and renamed over,
  283  # so a kill mid-write leaves the previous id and never an empty file
  284  # (D-CLOUD-078, #105). Braced, so a file that will not open is reported by
  285  # the caller's WARN line alone (redirections apply left to right, and
  286  # `> file 2>/dev/null` lets the shell print "Operation not permitted" before
  287  # stderr is closed).
  288  write_id() {
  289      mkdir -p "$(dirname "${ID_FILE}")" 2>/dev/null
  290      { printf '%s\n' "$1" > "${ID_FILE}.tmp.$$"; } 2>/dev/null \
  291          && mv -f "${ID_FILE}.tmp.$$" "${ID_FILE}" 2>/dev/null \
  292          || { rm -f "${ID_FILE}.tmp.$$" 2>/dev/null; return 1; }
  293  }
  294  
  295  # Append an id to the .previous file unless it is already there. Succeeds
  296  # only when the line is there afterwards: healing rests on it. Braced for the
  297  # reason write_id is.
  298  remember_previous() {
  299      mkdir -p "$(dirname "${PREVIOUS_FILE}")" 2>/dev/null
  300      grep -qxF -- "${1}" "${PREVIOUS_FILE}" 2>/dev/null && return 0
  301      { printf '%s\n' "${1}" >> "${PREVIOUS_FILE}"; } 2>/dev/null || return 1
  302      grep -qxF -- "${1}" "${PREVIOUS_FILE}" 2>/dev/null
  303  }
  304  
  305  # A stored id ending in the poisoned hash was not derived from this hardware,
  306  # so the rule that the stored value wins does not protect anything here: it
  307  # is the same string on every affected device, which is the one thing an
  308  # identity must not be. It is healed when -- and only when -- a validated
  309  # hardware address is available: the old id is recorded in .previous, the new
  310  # one written, and the change logged. With no address there is nothing to
  311  # regenerate from and the stored id is returned as it is, never invented.
  312  #
  313  # Only the poisoned hash is healed. A stored id that merely differs from what
  314  # this hardware would hash to is the wifi-module-swap case the stored value
  315  # exists for, and the maintainer's "edit the file to adopt another device's
  316  # folder"; neither is touched.
  317  heal_poisoned() {
  318      local stored="$1" seed healed
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_folder_validate @ 8ebaf8daad: lines 1-68 (excerpt of 278)

```text
    1  #!/usr/bin/python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """Bounded folder readiness metadata, never a transfer or integrity check.
    5  
    6  Private stdout contract for cloud_setup/ES. Missing means the selected endpoint
    7  returned not-found, or the selected content root listed without the child.
    8  Empty means a successful bounded listing found no recognized content; it is not
    9  an account-wide absence claim. No ancestor outside the selected root is read.
   10  """
   11  import json
   12  import os
   13  from pathlib import Path
   14  import re
   15  import selectors
   16  import signal
   17  import subprocess
   18  import sys
   19  import time
   20  
   21  CATEGORIES = ('saves', 'settings', 'roms', 'bios', 'media')
   22  MAX_BYTES = 2 * 1024 * 1024
   23  MAX_ENTRIES = 4096
   24  TOTAL_SECONDS = 25
   25  # Only observed standard save subtrees get deeper reads; never widen the
   26  # whole selected root or infer progress from an uninspected directory.
   27  SAVE_SUBTREES = {'psp/PSP/SAVEDATA': 2, 'psx/duckstation/memcards': 1}
   28  MEDIA = {'images', 'videos', 'manuals', 'screenshots', 'fanart', 'boxart', 'wheel', 'mix', 'maps', 'media'}
   29  # Match the shipped progress allowlist and content transfer exclusions. These
   30  # are case-sensitive like rclone's filters; test controls compare actual bytes.
   31  PROGRESS = re.compile(r'\.(srm|sav|fs|state[^/]*|auto|dsv[^/]*|eep|mpk|sra|fla)$')
   32  N64_STATE = re.compile(r'\.(st[0-9]|pj[0-9](\.zip)?)$')
   33  CONTENT_SAVE = re.compile(r'\.(srm|sav|fs|state[^/]*|auto|dsv[^/]*|eep|mpk|sra|fla|mcd|mcr)$')
   34  DATABASE = re.compile(r'\.(db|db-wal|db-shm|db-journal|sqlite|sqlite3)$')
   35  PARTIAL = re.compile(r'\.[^/]{8}\.partial$')
   36  HERE = Path(__file__).resolve().parent
   37  
   38  
   39  class Unreadable(Exception):
   40      pass
   41  
   42  
   43  def command(args, deadline, seconds=6, limit=MAX_BYTES):
   44      """Drain only bounded stdout; diagnostics can contain provider credentials."""
   45      remaining = min(seconds, deadline - time.monotonic())
   46      if remaining <= 0:
   47          raise Unreadable('time-limit')
   48      end = time.monotonic() + remaining
   49      proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
   50                              start_new_session=True)
   51      output = bytearray()
   52      try:
   53          with selectors.DefaultSelector() as ready:
   54              ready.register(proc.stdout, selectors.EVENT_READ)
   55              while ready.get_map():
   56                  wait = end - time.monotonic()
   57                  if wait <= 0:
   58                      raise Unreadable('time-limit')
   59                  if not ready.select(wait):
   60                      raise Unreadable('time-limit')
   61                  chunk = os.read(proc.stdout.fileno(), 65536)
   62                  if not chunk:
   63                      ready.unregister(proc.stdout)
   64                      break
   65                  output.extend(chunk)
   66                  if len(output) > limit:
   67                      raise Unreadable('listing-limit')
   68          rc = proc.wait(timeout=max(0.01, end - time.monotonic()))
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_folder_validate @ 8ebaf8daad: lines 77-128 (excerpt of 278)

```text
   77  
   78  
   79  def context(deadline):
   80      rc, raw = command([str(HERE / 'cloud_setup'), '--validation-context'], deadline)
   81      if rc:
   82          raise Unreadable('unreadable-config')
   83      value = json.loads(raw)
   84      if not re.fullmatch('[0-9a-f]{64}', value.get('config_id', '')):
   85          raise Unreadable('unreadable-config')
   86      return value
   87  
   88  
   89  def listing(remote, path, depth, deadline):
   90      rc, raw = command(['rclone', 'lsjson', remote + path, '--recursive',
   91                         '--max-depth', str(depth), '--no-mimetype', '--no-modtime',
   92                         '--retries', '1', '--low-level-retries', '1',
   93                         '--contimeout', '3s', '--timeout', '5s', '--max-duration', '6s'], deadline)
   94      if rc:
   95          # Entries on ANY error are not a valid observation. rclone lsjson
   96          # emits its opening bracket before a directory-not-found response.
   97          if rc in (3, 4) and (raw.strip() in (b'', b'[') or json.loads(raw) == []):
   98              return None
   99          raise Unreadable('listing-failed')
  100      entries = json.loads(raw)
  101      if not isinstance(entries, list) or len(entries) > MAX_ENTRIES:
  102          raise Unreadable('listing-limit')
  103      seen = set()
  104      for entry in entries:
  105          if not isinstance(entry, dict) or not isinstance(entry.get('Path'), str) or type(entry.get('IsDir')) is not bool:
  106              raise Unreadable('invalid-listing')
  107          p = entry['Path']
  108          if not p or len(p.split('/')) > depth or p.startswith('/') or any(x in ('', '.', '..') for x in p.split('/')) or any(ord(c) < 32 for c in p):
  109              raise Unreadable('invalid-listing')
  110          if p in seen:
  111              raise Unreadable('invalid-listing')
  112          seen.add(p)
  113      return entries
  114  
  115  
  116  def save_entries(remote, path, entries, deadline):
  117      """Inspect named save writers beyond the root's ordinary depth-three cut."""
  118      combined = list(entries)
  119      unchecked = {e['Path'] for e in entries if e['IsDir'] and len(e['Path'].split('/')) == 3}
  120      for subtree, depth in SAVE_SUBTREES.items():
  121          if subtree not in unchecked:
  122              continue
  123          child = path + ('' if not path or path.endswith('/') else '/') + subtree
  124          extra = listing(remote, child, depth, deadline)
  125          if extra is None:
  126              raise Unreadable('folder-changed-during-check')
  127          unchecked.remove(subtree)
  128          for entry in extra:
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_log_scrub @ 8ebaf8daad: lines 1-38 (excerpt of 206)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # cloud_log_scrub - take out of the logs the credentials earlier builds wrote
    6  # into them. Once per device, at boot, before anything writes those logs.
    7  #
    8  # Until e2d45ec7ec, cloud_remote logged every failed rclone call whole:
    9  # "rclone config create <name> <type> url=... user=*** pass=<the password>
   10  # ... failed (1): <rclone's words>", every value the player had typed,
   11  # passwords and keys among them; and cloud_oauth logged rclone's words when
   12  # a sign-in could not be saved -- words that could carry the token. The
   13  # fix stopped new lines (audit #307 PL-074). The old ones stayed: /var/log is
   14  # /storage/.cache/log on every device since D-SYS-001 (2026-09-10), and
   15  # cloud_sync.log is only trimmed past 1 MiB, which is months of ordinary
   16  # runs (the audit of the fix round, PL-014).
   17  #
   18  # The interface's own logs sit in the same folder. EmulationStation logged
   19  # cloud_remote's whole output at the Info level -- "cloud_remote create:
   20  # <output>", rclone's error among it, the output's later lines raw after
   21  # that record -- from ES cf09fc2f8 (2026-08-29) until ES 731252c61
   22  # (2026-09-28) masked it, and es_log*.txt keeps five interface starts, which
   23  # on a handheld is days.
   24  #
   25  # So, once, two families of file under /storage/.cache/log, each file
   26  # rewritten through a temp and a rename:
   27  #   cloud_sync.log* -- the log, a copy a trim left behind when it was cut
   28  #     off, any rotation:
   29  #     - an old cloud_remote failure line put in the shape this build writes,
   30  #       "rclone <verb> failed (<code>)", its arguments and rclone's words
   31  #       gone (a line cut off before its "failed" has every key=***
   32  #       masked);
   33  #     - cloud_oauth's "could not finish the sign-in: <rclone's words>" with
   34  #       the words <redacted>, unless they are one of the fixed sentences the
   35  #       scripts themselves wrote;
   36  #   es_log*.txt -- the interface's log and its rotations:
   37  #     - a "cloud_remote create: <output>" record keeps its timestamp and its
   38  #       words and has the output <redacted>, unless the output is the
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_log_scrub @ 8ebaf8daad: lines 47-198 (excerpt of 206)

```text
   47  #
   48  # Done is recorded in /storage/.cache/cloud_sync/log-scrubbed, one line per
   49  # family, each written only once every file of its family was rewritten or
   50  # needed nothing: "scrubbed=<epoch> files=<n> lines=<n>" for the cloud log --
   51  # the line this script wrote before it covered the interface's logs, so a
   52  # device that ran it then does not read its cloud log again -- and
   53  # "es_log_scrubbed=<epoch> files=<n> lines=<n>" for the interface's. A
   54  # family not recorded is tried again at the next boot. A device with no log
   55  # folder -- a clean install -- is recorded as done: no earlier build wrote
   56  # anything there.
   57  
   58  LOG_DIR=/storage/.cache/log
   59  STAMP=/storage/.cache/cloud_sync/log-scrubbed
   60  
   61  recorded() { grep -q "^$1=" "${STAMP}" 2>/dev/null; }
   62  recorded scrubbed && recorded es_log_scrubbed && exit 0
   63  set -o pipefail
   64  
   65  # The filter or nothing: without it a password in a line this script has no
   66  # rule for would be kept and the log recorded as clean.
   67  . /etc/profile.d/001-functions 2>/dev/null
   68  if ! type redact_credentials >/dev/null 2>&1; then
   69      echo "cloud_log_scrub: redact_credentials is not in /etc/profile.d/001-functions; nothing was scrubbed, and the next boot tries again"
   70      exit 1
   71  fi
   72  
   73  # The shapes earlier builds wrote to the cloud log, by the script that wrote
   74  # them. The cloud_remote rule for "config" verbs and the one for the others
   75  # are kept apart so neither reads this build's own "rclone config create
   76  # failed (1)" as an old line: that has no argument between the verb and
   77  # "failed".
   78  SCRUB_SED='
   79  /\[cloud_remote\] rclone config /{
   80  s/^(.*\[cloud_remote\] rclone config [a-z]+) [^ ]+( .*)? failed \(([0-9-]+)\)(: .*)?$/\1 failed (\3)/
   81  # A record cut before its "failed (...)" suffix (the log truncated mid-line) is
   82  # masked key by key:*** a quoted value is masked whole, spaces and all, and one cut
   83  # inside its quotes is masked to the end of the line -- the unquoted rule alone
   84  # stopped at the first space and left a quoted value'"'"'s tail readable (the audit
   85  # of the fixes, gpt G3-D-09).
   86  s/ ([A-Za-z0-9_.-]+)="[^"]*"/ \1=<redacted>/g
   87  s/ ([A-Za-z0-9_.-]+)='"'"'[^'"'"']*'"'"'/ \1=<redacted>/g
   88  s/ ([A-Za-z0-9_.-]+)="[^"]*$/ \1=<redacted>/
   89  s/ ([A-Za-z0-9_.-]+)='"'"'[^'"'"']*$/ \1=<redacted>/
   90  s/ ([A-Za-z0-9_.-]+)=[^ ]*/ \1=<redacted>/g
   91  }
   92  /\[cloud_remote\] rclone config /!s/^(.*\[cloud_remote\] rclone [a-z]+) [^ ]+( .*)? failed \(([0-9-]+)\)(: .*)?$/\1 failed (\3)/
   93  /\[cloud_oauth\] could not finish the sign-in: /{
   94  /sign-in: (a remote called .* already exists|signed in, but the remote did not respond|rclone rejected the token|The sign-in worked, but it couldn.t be saved on your handheld\.|The sign-in worked, but your handheld.s cloud settings couldn.t be read\.|That sign-in was closed before it finished\.)$/!s/(could not finish the sign-in: ).*$/\1<redacted>/
   95  }
   96  '
   97  
   98  # The interface's record starts "%F %T<TAB>" (Log::stream, since ES
   99  # e478a1eda); a line that does not is the rest of the record before it.
  100  # Each line goes out with the newline that ended the one before it, and the
  101  # last one's only when the file had it (nl): a log cut off mid-line -- the
  102  # interface killed as it wrote -- keeps its shape, as sed keeps it for the
  103  # cloud log.
  104  ES_AWK='
  105  function out(s) { if (NR > 1) printf "\n"; printf "%s", s }
  106  /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\t/ { inrec = 0 }
  107  inrec {
  108      if ($0 != "" && $0 !~ /^OK=[A-Za-z0-9_.-]*$/) $0 = "<redacted>"
  109      out($0); next
  110  }
  111  {
  112      i = index($0, "cloud_remote create: ")
  113      if (i) {
  114          inrec = 1
  115          rest = substr($0, i + 21)
  116          if (rest != "" && rest !~ /^OK=[A-Za-z0-9_.-]*$/) $0 = substr($0, 1, i + 20) "<redacted>"
  117      }
  118      out($0)
  119  }
  120  END { if (NR > 0 && nl) printf "\n" }
  121  '
  122  
  123  lines_in() { awk 'END { print NR }' "$1"; }
  124  
  125  first_pass() { # <file> <cloud|es>
  126      if [ "$2" = es ]; then
  127          awk -v nl="$([ -z "$(tail -c 1 "$1")" ] && echo 1 || echo 0)" "${ES_AWK}" "$1"
  128      else
  129          sed -E -e "${SCRUB_SED}" "$1"
  130      fi
  131  }
  132  
  133  # scrub <file> <cloud|es>: rewrite it in place, through a temp and a rename;
  134  # prints the number of lines it changed. Non-zero when the file could not be
  135  # rewritten whole, which leaves it as it was.
  136  scrub() {
  137      local f="$1" tmp="$1.scrub.$$" before after tries=0 changed
  138      while :; do
  139          before=$(wc -c < "${f}") || return 1
  140          if ! first_pass "${f}" "$2" | redact_credentials > "${tmp}"; then
  141              rm -f "${tmp}"; return 1
  142          fi
  143          after=$(wc -c < "${f}") || { rm -f "${tmp}"; return 1; }
  144          [ "${before}" = "${after}" ] && break
  145          tries=$((tries + 1))
  146          [ "${tries}" -lt 3 ] || { rm -f "${tmp}"; return 1; }
  147      done
  148      if [ "$(lines_in "${tmp}")" != "$(lines_in "${f}")" ]; then
  149          rm -f "${tmp}"; return 1
  150      fi
  151      changed=$(awk 'NR == FNR { a[FNR] = $0; next } a[FNR] != $0 { n++ } END { print n + 0 }' "${f}" "${tmp}") \
  152          || { rm -f "${tmp}"; return 1; }
  153      if [ "${changed}" -eq 0 ]; then
  154          rm -f "${tmp}"
  155      elif ! mv -f "${tmp}" "${f}"; then
  156          rm -f "${tmp}"; return 1
  157      fi
  158      echo "${changed}"
  159  }
  160  
  161  # family <cloud|es> <file...>: scrub every regular file named; sets FILES and
  162  # LINES, and returns non-zero if any could not be rewritten.
  163  family() {
  164      local kind="$1" f n bad=0; shift
  165      FILES=0 LINES=0
  166      for f in "$@"; do
  167          [ -f "${f}" ] && [ ! -L "${f}" ] || continue
  168          case "${f}" in *.scrub.*) continue ;; esac
  169          if n=$(scrub "${f}" "${kind}"); then
  170              FILES=$((FILES + 1)); LINES=$((LINES + n))
  171          else
  172              bad=1
  173              echo "cloud_log_scrub: ${f##*/} could not be rewritten; it is as it was, and the next boot tries again"
  174          fi
  175      done
  176      return "${bad}"
  177  }
  178  
  179  # record <key> <files> <lines>: the family's line in the stamp, the lines
  180  # already there kept, through a temp and a rename.
  181  record() {
  182      mkdir -p "${STAMP%/*}" \
  183          && { grep -v "^$1=" "${STAMP}" 2>/dev/null
  184               printf '%s=%s files=%s lines=%s\n' "$1" "$(date +%s)" "$2" "$3"; } > "${STAMP}.tmp" \
  185          && mv -f "${STAMP}.tmp" "${STAMP}" \
  186          || { rm -f "${STAMP}.tmp"; echo "cloud_log_scrub: the record of the scrub could not be written; the next boot runs it again"; return 1; }
  187  }
  188  
  189  failed=0
  190  if ! recorded scrubbed; then
  191      if family cloud "${LOG_DIR}"/cloud_sync.log "${LOG_DIR}"/cloud_sync.log.*; then
  192          record scrubbed "${FILES}" "${LINES}" || failed=1
  193          [ "${LINES}" -eq 0 ] || echo "cloud_log_scrub: ${LINES} line(s) in ${FILES} cloud log file(s) had credentials an earlier build wrote; masked"
  194      else
  195          failed=1
  196      fi
  197  fi
  198  if ! recorded es_log_scrubbed; then
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_scan @ 8ebaf8daad: lines 1-68 (excerpt of 362)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present rasteratops (https://github.com/rasteratops)
    4  
    5  # cloud_scan - what the cloud holds for this device, before anything is offered.
    6  #
    7  # The transfer pages scan first and offer only what the scan found
    8  # (D-CLOUD-156, fork #350): the folder's state, the settings archives by
    9  # device label, where the content is, and -- once the player has ticked
   10  # what to move -- the content listing in those classes. This runs those
   11  # reads and talks to the scan page in the protocol every cloud page reads
   12  # (">>> unit", ">>> doing", ">>> why"), writing each result to a file the
   13  # options page builds from.
   14  #
   15  #   cloud_scan                   the opening scan: the folder, the settings
   16  #                                archives, where the content is (three items)
   17  #   cloud_scan --content [--with-media|--media-only]
   18  #                                the content listing for the systems page,
   19  #                                in the classes ticked (one item)
   20  #   cloud_scan --folder          configured folder availability (one item)
   21  #
   22  # Read-only: scans never adopt another device's folders, rewrite settings,
   23  # move files, or offer migration. Folder changes use explicit setup choices.
   24  #
   25  # Results, under /storage/.cache/cloud_sync/scan/:
   26  #   state             cloud_setup --folder-state, one fact per line
   27  #   archives          every settings archive in the Backups folder, one per line
   28  #   settings          LABEL= (this device's), MINE= (its newest), NEWEST= (overall), COUNT=
   29  #   content-location  cloud_setup --content-location, key=***
   30  #   done              JSON binding the opening result to its run/configuration
   31  #   scan              cloud_content_restore --scan's rows        (--content)
   32  #   systems           the systems this device syncs (--systems)  (--content)
   33  #   content-done      equivalent binding for the selected content mode
   34  #
   35  # Exit: 0 all read; 69 no network (the page says SKIPPED - YOU'RE NOT
   36  # ONLINE); 1 no cloud storage set up; otherwise the failing read's code,
   37  # with a ">>> why" in the player's words before it (D-UI-028).
   38  
   39  . /etc/profile 2>/dev/null
   40  
   41  OUT=/storage/.cache/cloud_sync/scan
   42  SYNC_CONF=/storage/.config/cloud_sync.conf
   43  readonly EXIT_NO_NETWORK=69
   44  # Every listing here is bounded as the other readers' are (#308 claude F-RS-13).
   45  readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
   46  
   47  say() { echo "$@"; }
   48  log() { logger -t cloud_scan "$*" 2>/dev/null; }
   49  why() { echo ">>> why $*"; }
   50  
   51  # The shared reader (cloud_setup's, the content scripts', D-CLOUD-149): a
   52  # value in a form the sync does not read is nothing here, never a folder.
   53  conf_get() { # <KEY> (the content scripts' reader, mirrored so every reader agrees, D-CLOUD-149): its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
   54      [ -f ${SYNC_CONF} ] || return 0
   55      awk -v k="$1" '
   56          { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
   57          index($0, k "=") != 1 && !other \
   58              && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
   59          index($0, k "=") == 1 {
   60              s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
   61              c = substr(s, 1, 1)
   62              if (c == "\"") {
   63                  # Inside double quotes bash reads \" \\ \$ and \` as the one
   64                  # character each (PL-015), and so does this; an unescaped $
   65                  # or backtick is an expansion this reader does not make, and
   66                  # any other backslash is refused as conf_valid refuses it.
   67                  n = length(s); i = 2; closed = 0
   68                  while (i <= n) {
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_scan @ 8ebaf8daad: lines 132-183 (excerpt of 362)

```text
  132      mkdir -p "${OUT}" || { log "scan: cannot make ${OUT}"; why "SOMETHING WENT WRONG"; exit 1; }
  133      # No route, nothing tried: the page says SKIPPED - YOU'RE NOT ONLINE from
  134      # the code alone (D-CLOUD-072, D-CLOUD-112).
  135      if ! ip route show default 2>/dev/null | grep -q .; then
  136          log "scan: no default route; skipped"
  137          exit "${EXIT_NO_NETWORK}"
  138      fi
  139      REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
  140      if [ -z "${REMOTE}" ]; then
  141          local reason
  142          reason=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" selection-reason 2>/dev/null) || reason="YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
  143          why "${reason}"
  144          exit 1
  145      fi
  146  }
  147  
  148  # A read that failed ends the run with its why; 69 is the page's own sentinel.
  149  stop_on() { # <rc> <what> [application output file]
  150      [ "$1" -eq 0 ] && return 0
  151      log "scan: $2 exited $1"
  152      [ "$1" -eq "${EXIT_NO_NETWORK}" ] && exit "$1"
  153      if [ -n "${3:-}" ]; then
  154          local reason
  155          reason=$(sed -n 's/^>>> why //p' "$3" 2>/dev/null | tail -1)
  156          if [ -n "${reason}" ]; then
  157              why "${reason}"
  158          elif [ "$1" -eq 124 ]; then
  159              why "YOUR CLOUD STOPPED ANSWERING"
  160          else
  161              # Application codes are not rclone's codes. A refused layout
  162              # or invalid record does not mean that a folder is missing.
  163              why "YOUR CLOUD FOLDER COULDN'T BE READ"
  164          fi
  165      else
  166          why_for_rc "$1"
  167      fi
  168      exit "$1"
  169  }
  170  
  171  # Local-only identity: no rclone invocation and no configuration merge. A
  172  # changed endpoint, folder, rule or selection invalidates every old result.
  173  context_id() {
  174      local file fingerprint="" value
  175      for file in /storage/.config/cloud_sync.conf \
  176                  /storage/.config/rclone/rclone.conf \
  177                  /storage/.config/rclone/active-connection \
  178                  /storage/.config/cloud_sync-rules.txt \
  179                  /storage/.cache/cloud_sync/content-systems \
  180                  /storage/.config/emulationstation/es_systems.cfg \
  181                  /usr/config/emulationstation/es_systems.cfg; do
  182          if [ -f "${file}" ]; then
  183              value=$(sha256sum "${file}") || return 1
```


## projects/ROCKNIX/packages/network/rclone/sources/cloud_scan @ 8ebaf8daad: lines 212-362 (excerpt of 362)

```text
  212      case " $* " in
  213          *" --with-media "*" --media-only "*|*" --media-only "*" --with-media "*) return 1 ;;
  214          *" --with-media "*) echo content:all ;;
  215          *" --media-only "*) echo content:media ;;
  216          *) echo content:roms ;;
  217      esac
  218  }
  219  write_completion() {
  220      local stamp="$1" mode="$2" current digest tmp
  221      current=$(context_id) && [ "${current}" = "${CONFIG_ID}" ] || {
  222          why "YOUR CLOUD SETTINGS CHANGED. CHECK AGAIN"; return 1;
  223      }
  224      digest=$(result_id "${stamp}") || return 1
  225      tmp="${OUT}/${stamp}.tmp.$$"
  226      jq -n --arg run "${RUN_ID}" --arg config "${CONFIG_ID}" \
  227          --arg mode "${mode}" --arg result "${digest}" \
  228          '{schema_version:1,run_id:$run,config_id:$config,mode:$mode,result_id:$result}' > "${tmp}" \
  229          && mv -f "${tmp}" "${OUT}/${stamp}"
  230  }
  231  if [ "$1" = --context ]; then
  232      [ $# -eq 1 ] || exit 2
  233      context_id; exit $?
  234  elif [ "$1" = --stamp-valid ]; then
  235      STAMP="$2"; EXPECTED_RUN="$3"; shift 3 || exit 2
  236      [[ "${EXPECTED_RUN}" =~ ^[A-Za-z0-9_.-]{1,96}$ ]] || exit 2
  237      case "${STAMP}" in
  238          done) [ $# -eq 0 ] || exit 2; MODE=opening ;;
  239          content-done) MODE=$(content_mode "$@") || exit 2 ;;
  240          *) exit 2 ;;
  241      esac
  242      CURRENT=$(context_id) && DIGEST=$(result_id "${STAMP}") || exit 1
  243      jq -e --arg run "${EXPECTED_RUN}" --arg config "${CURRENT}" \
  244          --arg mode "${MODE}" --arg result "${DIGEST}" \
  245          '.schema_version == 1 and .run_id == $run and .config_id == $config and .mode == $mode and .result_id == $result' \
  246          "${OUT}/${STAMP}" >/dev/null 2>&1
  247      exit $?
  248  fi
  249  RUN_ID=""; ARGS=()
  250  while [ $# -gt 0 ]; do
  251      case "$1" in
  252          --run-id) [ -z "${RUN_ID}" ] && [ $# -ge 2 ] || exit 2; RUN_ID="$2"; shift 2 ;;
  253          --content|--folder|--with-media|--media-only) ARGS+=("$1"); shift ;;
  254          *) echo "Unknown scan option" >&2; exit 2 ;;
  255      esac
  256  done
  257  RUN_ID="${RUN_ID:-$(date +%s)-$$}"
  258  [[ "${RUN_ID}" =~ ^[A-Za-z0-9_.-]{1,96}$ ]] || exit 2
  259  set -- "${ARGS[@]}"
  260  CONFIG_ID=$(context_id) || exit 1
  261  
  262  # --content: the listing the systems page is built from, in the classes
  263  # the player ticked (cloud_content_restore --scan's own flags), and the
  264  # systems this device syncs. One item; the page's row 3 says it is
  265  # comparing.
  266  scan_content() {
  267      local label="ROMS AND BIOS" rc
  268      case " $* " in
  269          *" --with-media "*) label="ROMS, BIOS, AND GAME CONTENT" ;;
  270          *" --media-only "*) label="GAME CONTENT" ;;
  271      esac
  272      prepare
  273      rm -f "${OUT}"/scan "${OUT}"/scan.err "${OUT}"/systems "${OUT}"/content-done
  274      echo ">>> unit ${label}||"
  275      echo ">>> doing compare"
  276      "$(sibling cloud_content_restore)" --scan "$@" > "${OUT}/scan" 2> "${OUT}/scan.err"; rc=$?
  277      [ "${rc}" -eq 0 ] || log "scan: --scan $* exited ${rc}: $(head -1 "${OUT}/scan.err" 2>/dev/null)"
  278      stop_on "${rc}" "--scan"
  279      "$(sibling cloud_content_restore)" --systems > "${OUT}/systems" 2>/dev/null; rc=$?
  280      stop_on "${rc}" "--systems"
  281      mode=$(content_mode "$@") || exit 2
  282      write_completion content-done "${mode}" || exit 1
  283      log "scan: content done ($(grep -c . "${OUT}/scan") rows, ${label})"
  284      exit 0
  285  }
  286  
  287  # 1. Availability of the configured saves folder. It is not a reason to
  288  # reselect paths: other selected tiers may still hold their own files.
  289  read_folder() {
  290      local setup
  291      echo ">>> unit CLOUD FOLDER||"
  292      echo ">>> doing scan"
  293      setup=$(sibling cloud_setup)
  294      "${setup}" --folder-state > "${OUT}/state" 2>/dev/null
  295      stop_on $? "--folder-state" "${OUT}/state"
  296  }
  297  
  298  scan_main() {
  299  case "$1" in
  300      --content) shift; scan_content "$@" ;;
  301      --folder)
  302          # The step reads state alone; the opening scan's other files are
  303          # left as they were, and are rewritten by the next opening scan.
  304          prepare
  305          rm -f "${OUT}"/state "${OUT}"/done
  306          read_folder
  307          log "scan: folder done ($(sed -n 's/^STATE=//p' "${OUT}/state"))"
  308          exit 0 ;;
  309      "") ;;
  310      *) echo "usage: cloud_scan [--content [--with-media|--media-only] | --folder]" >&2; exit 2 ;;
  311  esac
  312  
  313  prepare
  314  rm -f "${OUT}"/state "${OUT}"/archives "${OUT}"/settings "${OUT}"/content-location "${OUT}"/root-dirs "${OUT}"/done
  315  date +%s > "${OUT}/started"
  316  read_folder
  317  
  318  # 2. The settings archives, by the device that wrote each (the label in the
  319  #    name, cloud_restore's rule): this device's newest first, else the newest
  320  #    overall, else none -- the row is offered or dimmed from this (D-CLOUD-162).
  321  echo ">>> unit SETTINGS BACKUPS||"
  322  echo ">>> doing scan"
  323  settings_remote=$(conf_get SETTINGS_REMOTE) || { why "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"; exit 1; }
  324  settings_remote="${settings_remote%/}"
  325  # Use the restore reader's directory priority, including inherited device IDs.
  326  archive_tool=$(sibling rasteratops-settings-archive)
  327  [ -r "${archive_tool}" ] || { why "SOMETHING WENT WRONG"; exit 1; }
  328  . "${archive_tool}"
  329  select_settings_archives "${REMOTE}${settings_remote}" "$(sibling cloud_device_id)"; rc=$?
  330  stop_on "${rc}" "archives listing"
  331  listing="${SETTINGS_ARCHIVE_LISTING}"
  332  printf '%s\n' "${listing}" | sed '/^$/d' > "${OUT}/archives"
  333  label=$(device_label); osn=$(os_name); mine=""; newest=""
  334  if [ -n "${label}" ]; then
  335      mine=$(grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-(${osn}|ROCKNIX|RASTERATOPS)_SETTINGS\.tar\.gz$" "${OUT}/archives" | sort | tail -1)
  336  fi
  337  newest=$(grep -E '^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-' "${OUT}/archives" | sort | tail -1)
  338  {
  339      echo "SOURCE=${SETTINGS_ARCHIVE_SOURCE}"
  340      echo "LABEL=${label}"
  341      echo "MINE=${mine}"
  342      echo "NEWEST=${newest}"
  343      echo "COUNT=$(grep -c . "${OUT}/archives")"
  344  } > "${OUT}/settings"
  345  
  346  # 3. Availability at the explicitly selected library. Account-root browsing
  347  # and discovery of another library are not part of a transfer preview.
  348  echo ">>> unit GAME CONTENT||"
  349  echo ">>> doing scan"
  350  "$(sibling cloud_setup)" --content-location > "${OUT}/content-location" 2>/dev/null; rc=$?
  351  stop_on "${rc}" "--content-location" "${OUT}/content-location"
  352  
  353  write_completion done opening || exit 1
  354  log "scan: done ($(grep -c . "${OUT}/archives") archives, $(sed -n 's/^STATE=//p' "${OUT}/state"), content $(sed -n 's/^STATE=//p' "${OUT}/content-location"))"
  355  exit 0
  356  
  357  }
  358  # The lock protects shared cache files. The function runs with the descriptor
  359  # closed; children cannot retain a stale lock after this owner exits.
  360  exec 8>/var/run/cloud_scan.lock || exit 1
  361  flock -n 8 || { why "ANOTHER CLOUD CHECK IS RUNNING"; exit 75; }
  362  scan_main "$@" 8>&-
```


## Fixture: tools/t17-pin-fixture.py (its docstring; the code runs the product's own functions)

```text
#!/usr/bin/env python3
"""T17 (#664): what spends the phone listener's ten PIN attempts.

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-pin-fixture.py \
        [--file <cloud_oauth>] [--expect unfixed|fixed]

Loads the real cloud_oauth (default: the worktree's, which is 8ebaf8daad's
bytes) by SourceFileLoader, makes a real SessionHolder and the real
make_server() on 127.0.0.1 at an ephemeral port, and sends real HTTP requests
over loopback. No sign-in runs: the holder's session is never started, so no
rclone runs; log() is pointed at a scratch file. Nothing leaves the host.

Cases (each on a fresh holder and server):
  favicon      ten GET /favicon.ico, then GET /<pin>: the browser's own icon
               requests carry no PIN; does the right PIN still open the page?
  touch-icons  five GET /apple-touch-icon.png and five
               /apple-touch-icon-precomposed.png, then GET /<pin>
  control      nine GET /favicon.ico, then GET /<pin>: under the limit
  wrong-pins   ten GET /0000-style wrong PINs, then GET /<pin>: the designed
               lockout, the control that the limit exists
  non-ascii    POST pin=%C3%A9 (a decoded non-ASCII PIN): a refusal page, or
               an unhandled exception in the handler?

--expect unfixed asserts what the file at 8ebaf8daad does; --expect fixed what
a fix must do (icons spend nothing; a non-ASCII PIN is refused like any wrong
one). Writes only under a temporary directory.
"""
```


## Fixture output: stage-b/fixture-pin.txt

```text
$ t17-pin-fixture.py --expect unfixed (06:33:03Z)
file: projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth
favicon: 10 requests before, statuses ['200', '403'], attempts spent 10; then GET /<the right pin> -> 403
touch-icons: 10 requests before, statuses ['200', '403'], attempts spent 10; then GET /<the right pin> -> 403
control: 9 requests before, statuses ['200'], attempts spent 9; then GET /<the right pin> -> 200
wrong-pins: 10 requests before, statuses ['200', '403'], attempts spent 10; then GET /<the right pin> -> 403
non-ascii: POST pin=%C3%A9 -> dropped:RemoteDisconnected; handler raised: yes: TypeError: comparing strings with non-ASCII characters is not supported; attempts spent 0
t17-pin-fixture: unfixed-expectation-met
exit 0
```


## Fixture: tools/t17-content-fixture.py (its docstring; the code runs the product's own functions)

```text
#!/usr/bin/env python3
"""T17 (#664): what the content scripts hand rclone from their arguments and
from cloud_sync.conf.

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-content-fixture.py \
        [--sources <dir holding the scripts>] [--busybox <busybox>] [--expect unfixed|fixed]

The real cloud_content_backup, cloud_content_restore and cloud_content_transfer
run under bash with the M6 donor's busybox applets first on PATH. Their
absolute paths are rewritten into a scratch root (/storage, /var/log, /var/run,
/tmp, and `. /etc/profile` dropped); nothing else in them changes. Their
siblings cloud_scan and cloud_remote are stubs (a fixed context digest; an
active remote `qa:`), and `rclone` is a stub that records every argv and
answers the listings a match needs. No network, no real cloud; the stub's
answers are named in each case.

Cases:
  backup-traversal  cloud_content_backup '../.config': does a copy reach
                    rclone with a source outside /storage/roms?
  backup-control    cloud_content_backup snes: the harness copies a system
  match-netopts     cloud_sync.conf RCLONE_NET_OPTS="... --delete-excluded";
                    cloud_content_restore --match, then --match --apply: does
                    the flag reach the deleting sync?
  match-control     the same with the shipped bound: it does not
  match-netopts-real, match-control-real (with --real-rclone): the same two
                    with a real rclone and a local-backend "cloud" under the
                    scratch root -- the cloud holds snes/a.zip; the device
                    holds a.zip, b.zip (not in the cloud) and a.srm (a save
                    beside the ROM). Which files does the apply delete?

--expect unfixed asserts what the files at 8ebaf8daad do; --expect fixed what
a fix must do (the traversal refused before any rclone call; the deleting
sync never carries --delete-excluded). Writes only under a temporary directory.
"""
```


## Fixture output: stage-b/fixture-content.txt

```text
$ t17-content-fixture.py --expect unfixed --real-rclone /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone (06:33:06Z)
sources: projects/ROCKNIX/packages/network/rclone/sources; applets: /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox
backup-traversal: rc 0; rclone copy calls 1; sources ['<root>/storage/roms/../.config']; a source outside /storage/roms: yes
backup-control: rc 0; rclone copy calls 1; sources ['<root>/storage/roms/snes']; a source outside /storage/roms: no
match-netopts: preview rc 0, plan ['snes|sync|1|5']; apply rc 0; deleting syncs 1, --max-delete ['1']; --delete-excluded on the deleting sync: yes
match-control: preview rc 0, plan ['snes|sync|1|5']; apply rc 0; deleting syncs 1, --max-delete ['1']; --delete-excluded on the deleting sync: no
real rclone: /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone rclone v1.75.2
match-netopts-real: preview rc 0, plan ['snes|sync|2|48']; apply rc 0; left on the device in roms/snes: ['a.zip']; the save a.srm kept: NO
match-control-real: preview rc 0, plan ['snes|sync|1|28']; apply rc 0; left on the device in roms/snes: ['a.srm', 'a.zip']; the save a.srm kept: yes
t17-content-fixture: unfixed-expectation-met
exit 0
```


## Fixture: tools/t17-archive-fixture.py (its docstring; the code runs the product's own functions)

```text
#!/usr/bin/env python3
"""T17 (#664): does backuptool's member check stop a settings archive that
writes outside /storage through a symlink member?

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-archive-fixture.py \
        [--file <backuptool>] [--busybox <busybox>]

Two halves, each with the product's own code or the image's tools:
  1. backuptool's foreign_member(), cut out of the script by name and run in
     bash with the M6 donor's busybox applets first on PATH, over the member
     list the donor busybox `tar -tzf` prints for the archive;
  2. the donor busybox `tar -xzf <archive> -C <root>`, the extraction the
     restore runs with -C / (backuptool :1679), into a scratch root holding storage/.config, as every device's /storage does.

Archives, built here with Python's tarfile (synthetic, no credential):
  escape    storage/.config/escape -> <scratch>/outside (an absolute symlink
            member), then storage/.config/escape/note.txt
  control   a member named storage/../outside-control.txt, which
            foreign_member exists to refuse

This is a named substitute for a full `backuptool restore` (which extracts
with -C / and is a stage-E or guest proof): it shows what the check judges
and what the extractor does with the same bytes. Writes only under a
temporary directory.
"""
```


## Fixture output: stage-b/fixture-archive.txt

```text
$ t17-archive-fixture.py  (06:33:06Z)
file: projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool; foreign_member() lines 551-558
tar and awk: /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox (busybox applets first on PATH)
escape: members ['storage/.config/escape', 'storage/.config/escape/note.txt']; foreign_member -> rc 1, accepted (no foreign member); busybox tar -xzf -C root -> rc 1 (tar: can't create symlink 'storage/.config/escape' to '<scratch> a file landed outside the root: no
control: members ['outside-control.txt']; foreign_member -> rc 0, refused (a member a restore can't put back) first: outside-control.txt; busybox tar -xzf -C root -> rc 0 (tar: removing leading 'storage/../' from member names); a file landed outside the root: no
escape: storage/.config/escape in the root is not a symlink
exit 0
```


## Fixture: tools/t17-mode-fixture.py (its docstring; the code runs the product's own functions)

```text
#!/usr/bin/env python3
"""T17 (#664): the mode each writer leaves its file with, observed.

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-mode-fixture.py [--umask 022]

Real functions, scratch paths, under the given umask (default 022, the
device's): cloud_connections.atomic() over rclone.conf and active-connection
(and over an existing 0644 rclone.conf, to see whether the old mode survives);
cloud_connections.save()'s staging directory and staged copy (stopped at the
first rclone call, which raises); cloud_oauth's _write_whole() (session.json),
_state_locked() (session.lock) and the marker writes; cloud_device_id's
write_id and remember_previous, and a cloud_scan-style `> file` write, run
through bash with the M6 donor's busybox. No rclone runs (the one call reached
is answered by a stub that fails). Writes only under a temporary directory.
"""
```


## Fixture output: stage-b/fixture-mode.txt

```text
$ t17-mode-fixture.py  (06:33:10Z)
umask 022; scratch under TMPDIR
atomic() new rclone.conf: 0o600
atomic() over an existing 0644 rclone.conf: 0o600
atomic() active-connection: 0o600
locked(): cloud_sync.lock 0o644 (opened 'a')
save(): staging directory 0o700, staged rclone.conf 0o600; left behind after a refusal: []
cloud_oauth STATE_DIR: 0o755; session.json: 0o644; session.lock: 0o600; cloud_sync.log (log()): 0o644
cloud_oauth marker signed-in: 0o644
cloud_device_id write_id: 0o644; .previous: 0o644; a cloud_scan-style '> file': 0o644 (bash rc 0)
exit 0
```
