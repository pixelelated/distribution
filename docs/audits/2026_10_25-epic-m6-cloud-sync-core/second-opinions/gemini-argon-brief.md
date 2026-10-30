# Third reading of a code audit -- M6.P2 T16, the cloud sync core, epic tier

You are the third reader. The first reader (Claude Opus 5.5, Anthropic)
wrote the audit in the packet below; a second reader (GPT-6 Astra, OpenAI)
has read the same packet, and the first reader's grades of the second
reader's items are appended at the end, after the packet. You cannot run
commands or open the repository; cite the packet's `file:line` or command
output for every claim.

The packet's own preamble (directly below) describes the scope, the threat
model, the trimming and the three-part answer. Answer the same three parts,
and add a fourth:

4. **The second reading, read again.** Where the first reader confirmed,
   narrowed, or refuted one of Astra's items, say whether the grade holds
   against the packet's lines, and name any item both earlier readers
   missed.

Do not repeat an item already graded unless you disagree with its grade.

---
# Second opinion on a code audit -- M6.P2 T16, the cloud sync core, epic tier

You are the second reader of a finished code audit. You cannot run
commands or open the repository; everything you may cite is in the packet
below, and every claim you make names the packet's `file:line` or the
command output it rests on. The first reader's verdicts are in the packet;
do not take them as given.

The scope: the 14 files of a handheld Linux distribution's cloud sync core
(`projects/ROCKNIX/packages/network/rclone/`), read at one commit
(`8ebaf8daad`):
- `cloud_backup` and `cloud_restore`, copy-twins that move game saves,
  save states and a settings archive between the device and the player's
  cloud with rclone;
- `cloud_capture`, a local manifest of the saves after each game;
- `cloud_saves_root`, which records the card the saves are on;
- `cloud_net_ready` and `cloud_sync_helper`, the conf's upgrades;
- the duplicate cleanup, the settings-archive wrapper, the boot hook and
  the recipe;
- the conf and the rclone allowlist, with their defaults.

Behaviour was proven in two places:
- **On a QEMU guest** of the distribution's x86_64 test image, against a
  local WebDAV server: the regression suite, and the cells that stop a run
  or cut its link.
- **On the build host**, in a sandbox running the image's busybox and
  rclone with the scripts at the read commit: the "host leads".

The scripts run as root at boot, after every game exits, and from menu
rows. The run after a game is an automatic sync bounded at 90 s; the
interface may stop it when the player launches a game ("STOP IT AND
PLAY"). The device has one player, who owns `/storage`, may edit
`cloud_sync.conf`, and owns the cloud account. Nothing remote but that
account is an input. The image's `/bin/sh` is bash; busybox provides the
small utilities; grep, sort and timeout are GNU.

The first reader is Claude Opus 5.5 (Anthropic); you are a reviewer from
another lab. The lens is security first, then brittleness, then new
functionality, and what loses or misplaces a player's save is the gravest
thing here. The audit is a renovation: besides defects, its findings answer
seven questions (Q1 modernize, Q2 standards, Q3 bugs, Q4 package currency,
Q5 efficiency, Q6 dead ends, Q7 clarity).

**The packet is trimmed** (the project's rule D-WORKFLOW-195):
- the analyses and their tables whole;
- the eleven smaller files whole;
- the three large scripts (`cloud_backup`, `cloud_restore`,
  `cloud_capture`: 6,538 lines) as line-numbered excerpts. Each excerpt
  covers every line the first reader cites, with context either side, plus
  each script's head, its trap and its main. A gap is marked `...`.

An item that rests on lines you saw only in excerpt says `excerpt`. Do not
guess at lines you were not shown.

Answer in three parts, in this order:

1. **Your own findings first.** Read the packet's evidence (the scripts,
   the configuration, the fixtures, the host leads' and the guest's
   records) and list every defect, gap or unsafe seam you find that is not
   already one of the first reader's findings. One line each:
   - an id (G-01, G-02, ...);
   - a severity (Critical / High / Medium / Low);
   - the packet's `file:line`;
   - what fails and when;
   - who can trigger it: the player's own conf, their cloud's contents, a
     card swap, a power cut or a stop, or nobody.
2. **Refute the first reader.** The table in 04 lists 15 findings, F-01 to
   F-15:
   - F-03 is High if the interface signals the script alone;
   - F-01, F-05 and F-14 are Medium;
   - the rest are Low, besides one design (F-11) and one oracle finding
     (F-15).

   For each, agree, disagree, re-grade or narrow, and say what would make
   the finding false and whether the packet shows it. Say plainly whether
   a Low should be Medium or High. Test hardest these three:
   - F-14: the restore's `--backup-dir` removes the saves it will replace
     before any transfer;
   - F-03: the automatic run's foreground `timeout ... rclone`, and the
     orphan a KILL to the script leaves;
   - F-02: the claim that an empty `SAVESPATH` is refused only by rclone's
     own overlap check.
3. **What you could not judge.** Name the claims the packet does not let
   you verify, so the orchestrator knows where its evidence was thin. Name
   each one that the trimming kept from you.

Everyday words, no hedging: a finding either survives your reading or it
does not, and you say which.

---


## The first reader's 02-forward-audit.md (whole)

# T16 forward audit: the cloud sync core (#663)

The forward audit of M6.P2 T16 (`cloud-sync-core`), from the brief at
`2cc743efd6`. Every file is read at `8ebaf8daad`'s bytes (`01` § Scope:
`git diff --stat 8ebaf8daad HEAD` over the 14 is empty). Each table that
can be generated is generated: the oracle by `tools/t16-oracle.py`, the
functions by `tools/t16-functions.py`, both under this folder, from
`git show` copies of the files in `/workspace/tmp/m6-t16/src/`. A guest
verdict, when the window runs, is written in § The guest cycle beside the
image-versus-tree diff it depends on.

## Coverage

One row per path of the slice (14). *Read* says how; `proved: tree` is a
read of the file at `8ebaf8daad`.

| Path | Lines | What it is | Read | proved: |
| --- | ---: | --- | --- | --- |
| `projects/ROCKNIX/packages/network/rclone/autostart/102-cloud-saves` | 57 | the boot hook: `cloud_log_scrub` (T17's) in the foreground, then a detached, niced `cloud_capture --full` when either cloud-saves toggle is on | whole | tree |
| `projects/ROCKNIX/packages/network/rclone/package.mk` | 111 | rclone 1.75.2 as a per-arch binary zip, pinned with its SHA256; installs 19 scripts and the four configuration files | whole | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_backup` | 2510 | the deliberate back up and the automatic exit sync: the saves phase, then the settings phase | whole | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_capture` | 1704 | the save manifest's recorder: exit, rescan, full, retire, adopt | whole: 1-770, 770-1110 and 1585-1704 line by line; 1110-1585 for its writes, removals, jq calls and exits | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_net_ready` | 217 | is the network up and settled (route, NetworkManager, carrier), for the startup sync | whole | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_restore` | 2324 | the deliberate restore and the automatic startup restore; a copy-twin of `cloud_backup` | the 34 shared functions identical to `cloud_backup`'s read once there; the 5 differing ones as diffs; its own 8 functions whole | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_saves_root` | 205 | which card the saves are on: identity, check, record, accept | whole | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync-rules.txt` | 89 | the saves allowlist that ships (54 rule lines, the catch-all `- /**` last) | whole; rule lines compared with the defaults | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync-rules.txt.defaults` | 100 | what the helper merges below a player's own rules | whole; its 54 rule lines equal the shipped file's, the 23 differing lines are comments | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf` | 160 | 16 keys | whole | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults` | 140 | the 16 `DEFAULT_` twins the helper appends from | whole | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync_cleanup_duplicates.sh` | 31 | keep the first of a repeated key, a continued value whole | whole | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_sync_helper` | 625 | run by `post-update` and at the start of every twin run: log trim, rules merge, config merge, four one-shot edits | whole | tree |
| `projects/ROCKNIX/packages/network/rclone/sources/rasteratops-settings-archive` | 43 | `select_settings_archives`, sourced by `cloud_restore` | whole | tree |

## The functions

`python3 -I -B tools/t16-functions.py /workspace/tmp/m6-t16/src .qa-scratch/t16/oracle.json --markdown`
(run from the worktree's root with the audit folder's path), rc 0:
`{"functions": 132, "by_script": {"cloud_backup": 45, "cloud_restore": 47, "cloud_capture": 40}, "shared": 39, "identical_shared": 34, "unrowed": 3, "uncalled": ["cloud_restore:controller_menu", "cloud_restore:device_folder"], "deltas": []}`.

- **The twins under `LC_ALL=C`:**
  - 39 shared names (`comm -12`, run r5) and 1,622 differing lines (`diff`, run r6).
  - **34 of the 39 shared bodies are byte-identical.** The five that differ are `check_network_link` (one log line), `record_last_run` (the stamp's name, and the settings-only skip, which only the backup has), `run_outcome_line` (the backup's two extra sentences), `load_config` (the restore lacks the nested-folder warning; its `--delete-excluded` comment differs; it overrides `BACKUPFILE_RESTORE_OPTION` and `RESTOREMETHOD`) and `main`.
  - So the shared body was read once, in `cloud_backup`, and every divergence whole.
- **A third copy:** `conf_valid` is in `cloud_sync_helper` too, identical to the twins' with comments set aside. Three copies of the one gate that decides whether a file is sourced as root.
- **Reach is static:**
  - A row reaches a function when it invokes the script and the function is in the call closure from the script's top level.
  - The phases its flags skip are removed. Under `--yes`, the console prompts are removed.
  - For `cloud_capture` the closure is the whole script's. Its five modes are not split statically, so a capture row "reaching" a function says a path exists, not that the row ran it. That is this table's limit, stated rather than hidden.
- **Unrowed: 3, all in `cloud_restore`, and none of them called by anything** (Q6):
  - `get_controller_devices` (616-628, called only from `controller_menu`);
  - `controller_menu` (632-693, no caller);
  - `device_folder` (1476-1482, no caller: the restore names its folder through `rasteratops-settings-archive`).

  The three are read whole: 76 lines that run on no path.

| Script | Function | Lines | Copy-twin | Called from | Oracle rows that reach it | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| `cloud_backup` | `child_running` | 187-191 | cloud_restore:174-178 identical | bounded_rclone, clean_exit | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `progress_mark` | 204-223 | cloud_restore:191-210 identical | bounded_rclone | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `advance_mark` | 229-239 | cloud_restore:216-226 identical | bounded_rclone | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `bounded_rclone` | 251-339 | cloud_restore:238-326 identical | rclone | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `logged_moved` | 348-355 | cloud_restore:335-342 identical | execute_rclone_with_error_handling, rclone | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `rclone` | 357-383 | cloud_restore:344-370 identical | (top level), backup_game_saves, backup_system_files, bounded_rclone, bucket_dir_listed, check_internet, check_rclone_config, execute_rclone_with_error_handling, load_config, network_lost_during_run, prune_replaced_remote, remote_compares_by_size, report_rclone_error | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `pause` | 389-391 | cloud_restore:378-380 identical | check_internet, check_rclone_config, load_config, main | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `log_message` | 402-418 | cloud_restore:387-403 identical | (top level), backup_game_saves, backup_system_files, bounded_rclone, check_internet, check_network_link, check_rclone_config, clean_exit, controller_confirm, execute_rclone_with_error_handling, load_config, main, network_lost_during_run, prune_replaced_remote, rclone, read_controller_input, relay_refusal, report_rclone_error, say_why, take_cloud_lock | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `take_cloud_lock` | 457-469 | cloud_restore:442-454 identical | (top level) | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `first_remote` | 474-476 | cloud_restore:931-933 identical | main | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `remote_compares_by_size` | 499-519 | cloud_restore:956-976 identical | backup_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.7`, `run_steps.9`, `run_steps.10`, `run_steps.11` (+23) | tree |
| `cloud_backup` | `_rclone_conf_key` | 522-529 | cloud_restore:979-986 identical | remote_compares_by_size | `run_steps.2`, `run_steps.3`, `run_steps.7`, `run_steps.9`, `run_steps.10`, `run_steps.11` (+23) | tree |
| `cloud_backup` | `has_default_route` | 538-541 | cloud_restore:464-467 identical | check_network_link, network_lost_during_run | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `check_network_link` | 543-549 | cloud_restore:469-475 differs | main | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `read_controller_input` | 559-627 | cloud_restore:485-553 identical | controller_confirm | `run_steps.7`, `run_steps.11`, `prepare_device.1`, `prepare_device.2`, `A8`, `A15` (+3) | tree |
| `cloud_backup` | `controller_confirm` | 631-687 | cloud_restore:557-613 identical | load_config | `run_steps.7`, `run_steps.11`, `prepare_device.1`, `prepare_device.2`, `A8`, `A15` (+3) | tree |
| `cloud_backup` | `write_stamp` | 702-709 | cloud_restore:708-715 identical | (top level), record_last_run | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `record_last_run` | 716-738 | cloud_restore:722-739 differs | clean_exit | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `unzip_can_test` | 753-763 | own | archive_whole | `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.11`, `run_steps.12`, `run_steps.13` (+9) | tree |
| `cloud_backup` | `archive_whole` | 764-774 | own | backup_system_files | `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.11`, `run_steps.12`, `run_steps.13` (+9) | tree |
| `cloud_backup` | `say_why` | 786-792 | cloud_restore:751-757 identical | (top level), backup_game_saves, backup_system_files, check_internet, check_rclone_config, load_config, main, network_lost_during_run, relay_refusal, report_rclone_error | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `bucket_dir_listed` | 802-813 | cloud_restore:821-832 identical | backup_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.7`, `run_steps.9`, `run_steps.10`, `run_steps.11` (+23) | tree |
| `cloud_backup` | `superseded_saves_setting` | 818-820 | own | backup_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.7`, `run_steps.9`, `run_steps.10`, `run_steps.11` (+23) | tree |
| `cloud_backup` | `outcome_word` | 822-827 | cloud_restore:787-792 identical | main | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `why_for` | 828-846 | cloud_restore:834-852 identical | backup_game_saves, check_internet, report_rclone_error | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `idle_timeout_seconds` | 851-866 | cloud_restore:857-872 identical | load_config | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `run_outcome_line` | 878-899 | cloud_restore:880-892 differs | main | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `clean_exit` | 905-933 | cloud_restore:898-926 identical | (top level), check_internet, check_rclone_config, load_config, main, network_lost_during_run | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `check_rclone_config` | 937-944 | cloud_restore:990-997 identical | main | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `check_internet` | 953-994 | cloud_restore:1006-1047 identical | backup_game_saves, main | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `network_lost_during_run` | 1021-1050 | cloud_restore:1070-1099 identical | (top level), backup_game_saves, backup_system_files | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `rules_whole` | 1056-1058 | cloud_restore:1105-1107 identical | backup_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.7`, `run_steps.9`, `run_steps.10`, `run_steps.11` (+23) | tree |
| `cloud_backup` | `conf_valid` | 1107-1190 | cloud_restore:1156-1239 identical | load_config | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `load_config` | 1194-1438 | cloud_restore:1243-1460 differs | main | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `device_id_tool` | 1444-1449 | cloud_restore:1466-1471 identical | device_folder, device_label | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `device_folder` | 1454-1460 | cloud_restore:1476-1482 identical | backup_system_files | `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.11`, `run_steps.12`, `run_steps.13` (+9) | tree |
| `cloud_backup` | `device_label` | 1469-1473 | cloud_restore:1491-1495 identical | (top level) | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `os_name` | 1479-1484 | cloud_restore:1501-1506 identical | (top level) | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `report_rclone_error` | 1493-1509 | cloud_restore:1515-1531 identical | backup_game_saves, backup_system_files | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_backup` | `relay_refusal` | 1513-1518 | cloud_restore:1535-1540 identical | backup_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.7`, `run_steps.9`, `run_steps.10`, `run_steps.11` (+23) | tree |
| `cloud_backup` | `execute_rclone_with_error_handling` | 1521-1552 | cloud_restore:1543-1574 identical | backup_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.7`, `run_steps.9`, `run_steps.10`, `run_steps.11` (+23) | tree |
| `cloud_backup` | `prune_replaced_remote` | 1564-1578 | own | backup_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.7`, `run_steps.9`, `run_steps.10`, `run_steps.11` (+23) | tree |
| `cloud_backup` | `backup_game_saves` | 1582-1960 | own | main | `run_steps.2`, `run_steps.3`, `run_steps.7`, `run_steps.9`, `run_steps.10`, `run_steps.11` (+23) | tree |
| `cloud_backup` | `backup_system_files` | 1965-2256 | own | main | `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.11`, `run_steps.12`, `run_steps.13` (+9) | tree |
| `cloud_backup` | `main` | 2407-2501 | cloud_restore:2207-2315 differs | (top level) | `run_steps.2`, `run_steps.3`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.9` (+28) | tree |
| `cloud_restore` | `child_running` | 174-178 | cloud_backup:187-191 identical | bounded_rclone, clean_exit | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `progress_mark` | 191-210 | cloud_backup:204-223 identical | bounded_rclone | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `advance_mark` | 216-226 | cloud_backup:229-239 identical | bounded_rclone | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `bounded_rclone` | 238-326 | cloud_backup:251-339 identical | rclone | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `logged_moved` | 335-342 | cloud_backup:348-355 identical | execute_rclone_with_error_handling, rclone | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `rclone` | 344-370 | cloud_backup:357-383 identical | (top level), bounded_rclone, bucket_based, bucket_dir_listed, check_internet, check_rclone_config, execute_rclone_with_error_handling, load_config, network_lost_during_run, remote_compares_by_size, report_rclone_error, restore_game_saves, restore_system_files | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `pause` | 378-380 | cloud_backup:389-391 identical | check_internet, check_rclone_config, load_config, main | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `log_message` | 387-403 | cloud_backup:402-418 identical | (top level), bounded_rclone, check_internet, check_network_link, check_rclone_config, clean_exit, controller_confirm, execute_rclone_with_error_handling, load_config, main, network_lost_during_run, rclone, read_controller_input, relay_refusal, report_rclone_error, restore_game_saves, restore_system_files, say_why, take_cloud_lock | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `take_cloud_lock` | 442-454 | cloud_backup:457-469 identical | (top level) | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `has_default_route` | 464-467 | cloud_backup:538-541 identical | check_network_link, network_lost_during_run | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `check_network_link` | 469-475 | cloud_backup:543-549 differs | main | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `read_controller_input` | 485-553 | cloud_backup:559-627 identical | controller_confirm | `run_steps.2`, `run_steps.11`, `prepare_device.1`, `A15`, `CONTRACT` | tree |
| `cloud_restore` | `controller_confirm` | 557-613 | cloud_backup:631-687 identical | load_config | `run_steps.2`, `run_steps.11`, `prepare_device.1`, `A15`, `CONTRACT` | tree |
| `cloud_restore` | `get_controller_devices` | 616-628 | own | controller_menu | unrowed | tree |
| `cloud_restore` | `controller_menu` | 632-693 | own | **nothing** | unrowed | tree |
| `cloud_restore` | `write_stamp` | 708-715 | cloud_backup:702-709 identical | record_last_run | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `record_last_run` | 722-739 | cloud_backup:716-738 differs | clean_exit | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `say_why` | 751-757 | cloud_backup:786-792 identical | check_internet, check_rclone_config, load_config, main, network_lost_during_run, relay_refusal, report_rclone_error, restore_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `near_names` | 766-785 | own | restore_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `outcome_word` | 787-792 | cloud_backup:822-827 identical | main | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `bucket_based` | 798-813 | own | restore_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `bucket_dir_listed` | 821-832 | cloud_backup:802-813 identical | restore_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `why_for` | 834-852 | cloud_backup:828-846 identical | check_internet, report_rclone_error | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `idle_timeout_seconds` | 857-872 | cloud_backup:851-866 identical | load_config | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `run_outcome_line` | 880-892 | cloud_backup:878-899 differs | main | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `clean_exit` | 898-926 | cloud_backup:905-933 identical | (top level), check_internet, check_rclone_config, load_config, main, network_lost_during_run | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `first_remote` | 931-933 | cloud_backup:474-476 identical | main | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `remote_compares_by_size` | 956-976 | cloud_backup:499-519 identical | restore_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `_rclone_conf_key` | 979-986 | cloud_backup:522-529 identical | remote_compares_by_size | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `check_rclone_config` | 990-997 | cloud_backup:937-944 identical | main | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `check_internet` | 1006-1047 | cloud_backup:953-994 identical | main | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `network_lost_during_run` | 1070-1099 | cloud_backup:1021-1050 identical | restore_game_saves, restore_system_files | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `rules_whole` | 1105-1107 | cloud_backup:1056-1058 identical | restore_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `conf_valid` | 1156-1239 | cloud_backup:1107-1190 identical | load_config | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `load_config` | 1243-1460 | cloud_backup:1194-1438 differs | main | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `device_id_tool` | 1466-1471 | cloud_backup:1444-1449 identical | device_folder, device_label, restore_system_files | `run_steps.2`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.11`, `prepare_device.1` (+2) | tree |
| `cloud_restore` | `device_folder` | 1476-1482 | cloud_backup:1454-1460 identical | **nothing** | unrowed | tree |
| `cloud_restore` | `device_label` | 1491-1495 | cloud_backup:1469-1473 identical | restore_system_files | `run_steps.2`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.11`, `prepare_device.1` (+2) | tree |
| `cloud_restore` | `os_name` | 1501-1506 | cloud_backup:1479-1484 identical | restore_system_files | `run_steps.2`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.11`, `prepare_device.1` (+2) | tree |
| `cloud_restore` | `report_rclone_error` | 1515-1531 | cloud_backup:1493-1509 identical | restore_game_saves, restore_system_files | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `relay_refusal` | 1535-1540 | cloud_backup:1513-1518 identical | restore_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `execute_rclone_with_error_handling` | 1543-1574 | cloud_backup:1521-1552 identical | restore_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `sweep_partials` | 1595-1598 | own | restore_game_saves, restore_system_files | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_restore` | `prune_replaced_local` | 1607-1621 | own | restore_game_saves | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `restore_game_saves` | 1625-1950 | own | main | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.10`, `run_steps.11`, `run_steps.14` (+6) | tree |
| `cloud_restore` | `restore_system_files` | 1955-2198 | own | main | `run_steps.2`, `run_steps.5`, `run_steps.6`, `run_steps.7`, `run_steps.11`, `prepare_device.1` (+2) | tree |
| `cloud_restore` | `main` | 2207-2315 | cloud_backup:2407-2501 differs | (top level) | `run_steps.2`, `run_steps.3`, `run_steps.4`, `run_steps.5`, `run_steps.6`, `run_steps.7` (+9) | tree |
| `cloud_capture` | `log_message` | 156-172 | own | capture_lock, finish, usage_error | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `log_info` | 176-176 | own | (top level), finish | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `log_warn` | 177-177 | own | (top level), seal | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `log_error` | 178-178 | own | (top level), seal | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `log_debug` | 179-179 | own | (top level), core_build_of | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `_sib` | 183-188 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `saves_path` | 193-198 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `elapsed_ms` | 200-205 | own | (top level), past_exit_bound | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `past_exit_bound` | 226-228 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `capture_lock` | 252-271 | own | (top level), finish | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `capture_unlock` | 272-276 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `finish` | 278-352 | own | (top level), usage_error | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `usage` | 354-356 | own | (top level), finish, usage_error | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `usage_error` | 358-363 | own | (top level), set_mode | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `set_mode` | 376-381 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `retire_rel` | 510-518 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `add_member` | 547-555 | own | (top level), row_retroarch | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `row_retroarch` | 560-586 | own | locate_unit | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `locate_unit` | 601-627 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `screenshot_of` | 630-636 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `rel_of` | 640-648 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `cleanup` | 764-766 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `core_package` | 870-890 | own | core_build_of | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `core_build_of` | 892-901 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `core_display_version_of` | 903-905 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `emit_op` | 959-961 | own | op_copy, op_meta, op_move, op_put, op_retire, op_unit | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `render_entry` | 965-985 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `op_put` | 987-990 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `op_meta` | 992-996 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `op_move` | 998-1006 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `op_copy` | 1011-1020 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `op_retire` | 1022-1026 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `op_unit` | 1030-1033 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `mtime_iso` | 1035-1037 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `seal` | 1045-1106 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `known_hash` | 1115-1133 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `entry_holds` | 1245-1253 | own | find_move_source | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `find_move_source` | 1259-1272 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `is_thumbnail` | 1430-1436 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |
| `cloud_capture` | `stage_times` | 1666-1672 | own | (top level) | `A9`, `A15`, `CAP1`, `CAP2`, `CAP3`, `CAP4` (+10) | tree |

## The oracle

`python3 -I -B tools/t16-oracle.py <T13's 02 at 0b72904621> /workspace/tmp/m6-t16/src/cloud-round-trip.8ebaf8daad --json .qa-scratch/t16/oracle.json --markdown`, rc 0:
`{"rows": 79, "by_oracle": {"synthetic": 46, "both ends": 25, "device report": 8}, "reviewed": 11, "reading_slice": 56, "via_helper": 8, "t17_only": 15, "deltas": []}`.

- **The input:**
  - 79 rows in, 11 of them `(reviewed)`;
  - the Oracle column 25 both ends (`CONTRACT` among them), 46 synthetic and 8 device report: the brief's figures, no delta;
  - T13's `04` `:228` lists the 24 both-ends rows of the 78, and `CONTRACT` is the 25th.
- **The scripts each row invokes** are read from its own line span of the harness at `8ebaf8daad`.
  - 8 rows name none in their span but call a harness helper outside it that does. The column names the helper (`via both_changed()`, `via capture()`, `via litter_scan()`).
  - 15 rows invoke only T17's content scripts or setup, and say so.
  - 56 of the 79 rows run at least one of this slice's nine scripts.
  - None runs `cloud_net_ready`, `rasteratops-settings-archive` or `cloud_sync_cleanup_duplicates.sh` by name. Those three are read whole here and have no oracle row of their own (run r23).
- **What makes it FAIL** is each `check()`'s `ok` text, false.
  - The text is taken from the AST of the call, three per row, with the rest counted.
  - The LINK rows' spans are their registry entries. Their checks are `Link.exercise`'s shared ones, so their cell reads "no check() in the span".
- **The verdicts this slice may trust at `3a653eaec4` and later** are the both-ends rows (T13's `04` `:228`).
  - A synthetic row proves the path, not the input.
  - A device-report row certifies the code by its own output and is not evidence about it.
  - A5 and RETENTION SKIP today: there is no `cloud_reconcile` (#1057).

| Row | Harness lines | Oracle | Scripts invoked, with flags | What makes it FAIL (each check's ok, false) | proved: |
| --- | --- | --- | --- | --- | --- |
| `run_steps.1` | 625-631 | synthetic | none of the nine | not: fixtures written | tree |
| `run_steps.2` | 632-671 | both ends | `cloud_restore`; `cloud_restore --saves-only --yes`; `cloud_backup --saves-only --yes` | not: a restore with no Saves folder in the cloud is a truthful empty (0 + the offer) or fails with its own code, never a sentinel; not: all {...} fixtures reached the bucket; not: the allowlist kept excluded files out of the cloud | tree |
| `run_steps.3` | 672-707 | device report (reviewed) | `cloud_backup --saves-only --yes`; `cloud_restore --saves-only --yes` | not: the second backup completed (exit {...}); not: all {...} replaced saves came back from the cloud as the new bytes | tree |
| `run_steps.4` | 708-721 | device report (reviewed) | `cloud_restore --saves-only --yes` | not: local copies removed before restore; not: all {...} files restored byte-identical | tree |
| `run_steps.5` | 722-787 | both ends | `cloud_backup --system-only --yes`; `cloud_restore --system-only --yes` | not: the settings backup archive reached the cloud; not: the settings backup exited 0 and ended on Completed.; not: the archive is filed under this device ({...}) (+3 more) | tree |
| `run_steps.6` | 788-814 | device report (reviewed) | `cloud_backup --system-only --yes`; `cloud_restore --system-only --yes` | not: the second archive replaced the first in the cloud | tree |
| `run_steps.7` | 815-910 | synthetic | `cloud_backup`; `cloud_backup --system-only --yes`; `cloud_restore --system-only --yes` | not: ; not: ; not: the upload ran (exit {...}) (+5 more) | tree |
| `run_steps.8` | 911-945 | both ends | none of the nine; T17's `cloud_content_backup` | not: {...} is offered as a content directory; not: all {...} content files reached the cloud | tree |
| `run_steps.9` | 946-967 | synthetic | `cloud_backup --saves-only --yes` | not: the backup with a user rule completed (exit {...}); not: the user rule sits above the catch-all in the merged file (lines {...}); not: the excluded file stayed home while the ordinary save travelled | tree |
| `run_steps.10` | 968-1008 | synthetic | `cloud_backup --saves-only --yes`; `cloud_restore --saves-only --yes` | not: the backup with a bare RCLONEOPTS completed (exit {...}); not: the file outside the allowlist stayed home while the save travelled; not: the log says the allowlist was added (+2 more) | tree |
| `run_steps.11` | 1009-1069 | synthetic | `cloud_backup`; `cloud_restore`; `cloud_backup --saves-only --yes` | not: no command {...} starts under the lock sees its descriptor (0 of {...}); not: the lock is free the moment the run returns ({...}) | tree |
| `run_steps.12` | 1070-1099 | device report | `cloud_backup --system-only --yes` | not: the settings phase says it was skipped and the summary agrees: SKIPPED - NOTHING TO SEND YET; not: and the saves line says the phase was skipped, not COMPLETED; not: the settings stamp still describes the last upload that happened ({...}) | tree |
| `run_steps.13` | 1100-1140 | synthetic | `cloud_backup --system-only --yes` | not: selecting saves preserves the settings and library paths; not: selecting settings preserves saves and the library path; not: a settings backup ran without the nesting warning (exit {...}) (+2 more) | tree |
| `run_steps.14` | 1141-1200 | synthetic | `cloud_restore --saves-only --yes` | not: root present, Saves absent: exit 0, the plain line, and the offer; not: root absent: the restore fails (exit {...}) and offers nothing; not: a root-level saves folder on an empty cloud: exit 0 and the offer names it (+2 more) | tree |
| `run_steps.15` | 1201-1234 | synthetic | none of the nine; T17's `cloud_content_restore` | not: local content removed before restore; not: all {...} content files restored byte-identical | tree |
| `run_steps.16` | 1235-1266 | synthetic | none of the nine; T17's `cloud_content_restore` | not: --all exited 0; not: the BIOS file came down with --all; not: and {...}'s {...} files, byte-identical (+1 more) | tree |
| `run_steps.17` | 1267-1286 | both ends | none of the nine; T17's `cloud_content_backup` | not: the ROM reached the content tier; not: the save file was correctly withheld from content | tree |
| `run_steps.18` | 1287-1317 | both ends | none of the nine; T17's `cloud_content_backup` | not: the ordinary ROM reached the content tier; not: the conflicted copy was withheld from the cloud; not: the Syncthing conflict file was withheld (+1 more) | tree |
| `run_steps.19` | 1318-1362 | both ends | none of the nine; T17's `cloud_content_backup`, `cloud_content_restore` | not: the ROM reached the content tier; not: the gamelist reached the cloud in its own pass; not: --selected announced every unit it moved, numbered across the run ({...}) (+2 more) | tree |
| `run_steps.20` | 1363-1389 | synthetic | `cloud_backup --yes`; `cloud_backup --recent --saves-only --yes` | not: the test could hold the lock itself; not: the second sync exited 75 (EX_TEMPFAIL, the lock sentinel); not: and said another sync was running (+1 more) | tree |
| `run_steps.21` | 1390-1406 | device report | `cloud_backup --saves-only --yes`; `cloud_backup --recent --saves-only --yes` | not: the recent sync exited 0; not: rclone was given a recency window and told not to list the remote; not: and found nothing to move (+1 more) | tree |
| `run_steps.22` | 1407-1419 | both ends | `cloud_backup --recent --saves-only --yes` | not: the new save reached the bucket; not: and it was the only file transferred | tree |
| `run_steps.23` | 1420-1459 | both ends | `cloud_backup --recent --saves-only --yes` | not: ; not: the same-size change reached the bucket as the new bytes | tree |
| `run_steps.24` | 1460-1479 | synthetic | `cloud_backup --recent --saves-only --yes` | not: exit 69 (EX_UNAVAILABLE, the no-network sentinel) with no default route; not: and it answered in under two seconds; not: no last-run stamp was written for work that did not happen | tree |
| `run_steps.25` | 1480-1496 | device report | none of the nine | not: every ES path outside /storage/roms is in the settings backup | tree |
| `run_steps.26` | 1497-1551 | synthetic | none of the nine; T17's `cloud_device_id` | not: newest archive is a tar.gz ({...}); not: the archive passes tar integrity; not: the archive is named for this device, between the date and {...} ({...}) (+2 more) | tree |
| `run_steps.27` | 1552-1596 | both ends | none of the nine; T17's `cloud_content_backup`, `cloud_content_restore` | not: selection persisted as {...}; not: an unselected system was not uploaded; not: --selected announced the selected units and only those, numbered across the run ({...}) (+2 more) | tree |
| `run_steps.28` | 1597-1644 | synthetic | none of the nine; T17's `cloud_content_restore` | not: the unrunnable system is flagged 0 (unsupported); not: the scan says what a copy each way would move, in files and bytes; not: under ROMs alone the game list is neither sized nor counted (+1 more) | tree |
| `run_steps.29` | 1645-1673 | synthetic (reviewed) | none of the nine; T17's `cloud_content_restore` | not: the stanza's endpoint is the dead port {...}; not: the scan exited {...} with no system lines; not: with the stanza restored the scan lists systems again (exit 0) | tree |
| `run_steps.30` | 1674-1693 | synthetic (reviewed) | none of the nine; T17's `cloud_setup` | not: explicit selected-category seeding completed; not: a second seeding run reports the folders present; not: the owner's note survived a second seeding | tree |
| `run_steps.31` | 1694-1713 | synthetic | `cloud_sync_helper` | not: every old key reached its new name with its value | tree |
| `run_steps.32` | 1714-1716 | both ends (reviewed) | `cloud_sync_helper` (via `litter_scan()`) | no check() in the span | tree |
| `prepare_device.1` | 309-317 | device report | `cloud_backup`; `cloud_restore` | not: ssh works; not: rclone and cloud scripts present | tree |
| `prepare_device.2` | 318-383 | synthetic (reviewed) | `cloud_backup` | not: active remote is {...}, which is what the scripts will use | tree |
| `A1` | 1972-1999 | both ends | `cloud_backup --saves-only --yes` (via `both_changed()`) | not: {...}: neither HA nor HB was overwritten; not: {...}: reported one queued conflict (exit 5) | tree |
| `A2` | 2002-2043 | both ends | `cloud_backup --recent --saves-only --yes`; `cloud_backup --saves-only --yes`; `cloud_restore --saves-only --yes` | not: the push failed while the cloud refused the sign-in (exit {...}; the setup); not: the next exit, with nothing changed since, retried and published; not: an equal-size, equal-mtime byte change entered the changed set at the full pass | tree |
| `A3` | 2046-2082 | synthetic (reviewed) | `cloud_backup --saves-only --yes` | not: nothing on this device was replaced by the new folder's saves; not: the identical pair is untouched; not: the differing pair was queued (exit 5) (+1 more) | tree |
| `A8` | 2085-2144 | both ends | `cloud_backup`; `cloud_backup --saves-only --yes` | not: b's publication was interrupted after its first member (the setup); not: a installed no mixed set (its pair is {...}/{...}); not: an unrelated unit still moved while the torn one was held (+1 more) | tree |
| `A9` | 2147-2252 | both ends | `cloud_capture`; `cloud_capture --retire` | not: the manager's deletion left a retired row for state2 with S2's sha (#21; the record #22 propagates); not: after repeated syncs b holds S1 and S3, each exactly once; not: and so does the cloud (+12 more) | tree |
| `A11` | 2255-2277 | both ends | `cloud_backup --saves-only --yes` | not: the clone was refused with duplicate-device-id; not: and transferred nothing | tree |
| `A12` | 2280-2318 | synthetic | `cloud_sync_helper` | not: SAVESPATH was migrated from BACKUPPATH; not: RESTOREPATH was dropped; not: one WARN names the ignored folder (+2 more) | tree |
| `A14` | 2321-2377 | both ends | `cloud_backup --recent --saves-only --yes` | not: the working copy {...}/manifest-{...}.json holds both entries with the planted shas (#21); not: the manifest reached the cloud under savestates/.rocknix/; not: its entry for the state carries the planted bytes' sha256 (#22) (+2 more) | tree |
| `A5` | 2380-2417 | device report (reviewed) | `cloud_backup --saves-only --yes` (via `both_changed()`) | not: b read a decision record from the store; not: the newest record names when, the producing device and the winning side; not: the loser's thumbnail travelled with it | tree |
| `RETENTION` | 2420-2455 | both ends | `cloud_backup --saves-only --yes` (via `both_changed()`) | not: the loser's record appeared in the store (the kill point); not: the loser's bytes are in the store, hash-equal; not: the head is unchanged (+1 more) | tree |
| `A15` | 2530-2990 | synthetic | `cloud_capture`; `cloud_restore`; `cloud_capture --full`; `cloud_restore --system-only --yes`; `cloud_backup`; `cloud_backup --system-only --yes` | not: sit0 is present (modprobe sit); not: the old pipeline turns `ethtool -P sit0` into {...} -- the string both handhelds hashed; not: permanent_address yields nothing for sit0 (exit {...}) (+33 more) | tree |
| `CAP1` | 3243-3333 | synthetic | `cloud_capture --system` | not: the test held the transfer lock itself (the setup); not: capture exited 0 under a held lock, with no route, after exit 1 from the emulator; not: the manifest exists and parses (+16 more) | tree |
| `CAP2` | 3336-3372 | synthetic | `cloud_capture --system` (via `capture()`) | not: core is snes9x2005_plus (not gba's default), emulator retroarch; not: the next version records mgba; not: replaces is the first version's sha (+3 more) | tree |
| `CAP3` | 3375-3449 | synthetic | `cloud_capture --system` (via `capture()`) | not: the seal has one link and its own inode; not: the in-place write to the source landed (the setup); not: stage/<sha> still hashes to its name after the source was rewritten (+5 more) | tree |
| `CAP4` | 3452-3518 | synthetic | `cloud_capture`; `cloud_capture --full`; `cloud_capture --retire` | not: (computed); not: a touch rewrote the manifest (mtime, inode and sha all changed); not: the entry's mtime is the file's new value, ISO-UTC (+4 more) | tree |
| `CAP5` | 3521-3556 | synthetic | `cloud_capture --system` (via `capture()`) | no check() in the span | tree |
| `CAP6` | 3607-3678 | synthetic | `cloud_capture --system` (via `capture()`) | not: exactly four entries: the .srm (keyed under gba/sub/), .state, .state3, .state.auto; not: all with unit {...}; not: slots null/0/3/null (a bare .state is slot 0) (+8 more) | tree |
| `CAP7` | 3681-3877 | synthetic | `cloud_capture --retire`; `cloud_capture --rescan --system` | not: --retire (one absolute, one relative path) exited 0 and removed the state's entry; not: one retired row: the state with its entry's sha, root-relative; none for the thumbnail, which has no version to retire (D-CLOUD-059); not: retires_pub null and `at` ISO-UTC on it (+26 more) | tree |
| `CAP8` | 3880-3966 | synthetic | `cloud_capture --full` | not: a member older than --started with no entry: exit 0 and no manifest was created; not: the log says it was not stamped; not: the fresh .srm is recorded and the old state still is not (the rule is per member, not per run) (+9 more) | tree |
| `CAP9` | 3969-4113 | synthetic | `cloud_capture --system`; `cloud_capture --bogus`; `cloud_capture --retire`; `cloud_capture --full`; `cloud_capture` | not: {...}: exit 2 with a line on stderr; not: usage errors created no manifest; not: --emulator '' (a system with no emulator): exit 0, nothing recorded, no capture-failures row, last-capture rc 0 (+16 more) | tree |
| `CAP10` | 4154-4245 | synthetic | `cloud_saves_root`; `cloud_capture`; `cloud_capture --full` | not: on a wrong-but-stable card the new version IS recorded (the file is real; its claim belongs, I5); not: the log carries cloud_saves_root's 'different card' sentence; not: last-capture carries the !card marker (+9 more) | tree |
| `CAP11` | 4248-4314 | synthetic | `cloud_capture`; `cloud_saves_root` | not: the second writer landed between the run's load and its rename (the setup); not: the exit capture that lost the race exited 0 with its version recorded; not: and the winner's entry stands (the re-run built on the new document, not over it) (+3 more) | tree |
| `CAP12` | 4317-4388 | synthetic | `cloud_capture --full`; `cloud_capture --retire` | not: a one-line stamp from before (an exit) survives a --full pass byte for byte; not: and the file holds exactly two lines, exit and full; not: the full line reads rc 0, unit -, emu-exit=? -/- (+6 more) | tree |
| `CAP13` | 4391-4457 | synthetic | `cloud_capture --retire --unlink`; `cloud_capture --unlink` | not: (a) the retired row carries state2's sha and its entry is gone; not: (a) the state and its thumbnail are gone from disk; not: (b) a slot with no entry: the row carries the live hash and the file goes (+3 more) | tree |
| `CAP14` | 4460-4524 | synthetic | `cloud_capture --adopt`; `cloud_capture --retire --unlink` | not: (a) the copy's entry carries the source's sha; not: (a) and the source's emulator, core and core_build; not: (a) its own slot, kind and thumbnail; replaces and pub null (+4 more) | tree |
| `LINK1` | 5609-5619 | synthetic (reviewed) | `cloud_backup --saves-only --yes`; `cloud_restore --method=copy --saves-only --update --yes` | no check() in the span | tree |
| `LINK2` | 5622-5627 | both ends | `cloud_backup --saves-only --yes` | no check() in the span | tree |
| `LINK3` | 5630-5636 | both ends | none of the nine; T17's `cloud_content_backup` | no check() in the span | tree |
| `LINK4` | 5639-5645 | synthetic | none of the nine; T17's `cloud_content_restore` | no check() in the span | tree |
| `LINK5` | 5648-5679 | both ends | `cloud_backup`; `cloud_backup --system-only --yes` | no check() in the span | tree |
| `LINK6` | 5682-5690 | both ends | `cloud_backup --recent --saves-only --yes` | no check() in the span | tree |
| `LINK7` | 5693-5717 | synthetic | none of the nine; T17's `cloud_content_restore` | no check() in the span | tree |
| `KILL1` | 6771-6855 | both ends (reviewed) | `cloud_backup --saves-only --yes` | not: ; not: {...}: SIG{...} mid-transfer of {...}: the process group was gone in {...}s; not: {...}: no *.partial in the cloud (+6 more) | tree |
| `KILL2` | 6858-6956 | synthetic | `cloud_restore --method=copy --saves-only --update --yes` | not: ; not: {...}: TERM then KILL at 1.5s: the group was empty {...}s after the signal (budget 2s), mid-download of {...}; not: {...}: SIGKILL mid-download of {...}: the group was gone in {...}s (+8 more) | tree |
| `KILL3` | 6975-7019 | synthetic | none of the nine | not: the kill landed mid-rotation (archive/{...} present); not: the new archive is at the root, lists, and is what newest_backup finds ({...}); not: A is in archive/ (+3 more) | tree |
| `KILL4` | 7021-7070 | both ends | `cloud_backup --system-only`; `cloud_backup`; `cloud_backup --system-only --yes` | not: the kill landed while tar was writing the new archive; not: what the readers find passes tar -tzf ({...}); not: no truncated archive under a final name at the root (+2 more) | tree |
| `KILL5` | 7073-7159 | both ends | `cloud_backup --system-only --yes` | not: ; not: SIGKILL mid-copyto of {...}: the group was gone in {...}s; not: settings-backup.uploaded is byte-identical (the upload was never confirmed) (+9 more) | tree |
| `KILL10` | 7162-7202 | synthetic | none of the nine | not: {...} still reads old after the kill mid-write; not: the writer's temporary (system.cfg.tmp) is present after the kill; not: the re-run cleared the stale lock (held by pid {...}) and set {...}=new in {...}s (+2 more) | tree |
| `KILL11` | 7205-7235 | synthetic | none of the nine | not: {...} reads {...} after the kill at the lock release: old or new, never lost; not: system.cfg.backup untouched; not: the re-run set {...}=new | tree |
| `KILL12` | 7251-7352 | synthetic | none of the nine | not: ({...}) after boot system.cfg is {...}; not: ({...}) the planted es_settings.cfg value survived the boot; not: ({...}) system.cfg.backup is still the good copy (+2 more) | tree |
| `KILL13` | 7375-7512 | synthetic | none of the nine | not: ; not: [{...}] {...}; not: [{...}] the toggle was recorded: the walk reaches the switch (+2 more) | tree |
| `KILL15` | 7515-7540 | synthetic | `cloud_saves_root` | not: an empty saves-root record is refused (exit 1) rather than read as none; not: record rewrites the identity ({...}); not: no saves-root temp left | tree |
| `KILL16` | 7543-7577 | synthetic | none of the nine; T17's `cloud_content_restore` | not: killed before the write (mkdir shim): the selection still reads qa-a qa-b; not: after --set-systems a b the file holds exactly those two lines; not: no content-systems temp left | tree |
| `KILL18` | 7580-7659 | synthetic | none of the nine | not: the kill landed mid-extract (a.cfg {...}, {...} of {...} small files, b.cfg {...}); not: the pre-restore state is kept ({...}) while the tree is half restored (a.cfg {...}, b.cfg {...}, {...} of {...} files); not: the restore-in-progress marker names the copy for the next boot (+3 more) | tree |
| `CONTRACT` | 4617-5128 | both ends | `cloud_backup`; `cloud_backup --system-only`; `cloud_restore` | not: the both-changed pair was reported in a parseable form; not: and neither file changed; not: the dry-run guard fired on the constructed conflict (+13 more) | tree |

## The stamps and locks

**Three stamp families** (run r17, read line by line):

| Family | Stamp (under `/storage/.cache/cloud_sync/`) | Writer | Readers | proved: |
| --- | --- | --- | --- | --- |
| the twins' | `last-backup`, `last-settings-backup`, `last-restore`, `last-settings-restore` | `record_last_run` (`cloud_backup:716`, `cloud_restore:722`) writes `last-${name}` through `write_stamp` (temp, then `mv`): name `backup`/`settings-backup` or `restore`/`settings-restore` by `--system-only` | `cloud_backup:1806` (`--recent` reads `last-backup`: rc 0 and its epoch open the window); EmulationStation's rows (named, not read); `tools/cloud-round-trip` (9 hits of `last-restore`) | tree |
| the twins' | `settings-backup.uploaded` | `cloud_backup:2303`, only after the cloud copy's size equals the bytes sent | `cloud_backup:2118` | tree |
| the twins' | `restore-tree-clean` | `cloud_restore:1594` (removed as the saves transfer starts, written after it); **also `cloud_content_restore:794`** (T17's), by design (G-A-07, A49) | `cloud_restore:1898` | tree |
| the twins' | `replaced/<stamp>/` (local), `<SAVES_REMOTE>-replaced/<stamp>/` (cloud) | `--backup-dir` of each saves transfer; pruned to one by `prune_replaced_local` / `prune_replaced_remote` after a run that completed | none in the slice | tree |
| the capture's | `last-capture` (one line per mode), `capture-failures` (the last 20), `manifest-<id>.json`, `stage/<sha256>` | `cloud_capture` `finish` (`:278`), the commit (`:1639`), `seal` (`:1045`) | EmulationStation (by path); `tools/cloud-capture-stamp-test`; `stage/` has **no reader in the tree** (the reconciler is #1057's) | tree |
| the capture's | `saves-root` | `cloud_saves_root` `write_record` (`:94`), on `record` after a transfer that completed, and on `accept` | `cloud_saves_root check` (`:143`); the twins (`:1606`/`:1648`) and the capture (`:776`) through it | tree |
| EmulationStation's | `last-sync-<origin>` | `ThreadedCloudSync` and the cards (by path; 0 hits in the 14) | five tools on 17 lines | tree |

**Deltas to the brief's § 2:**

- **`last-restore` exists.** The brief says "there is no `last-restore`" (version 2's correction 4). The literal string has no hit because the name is built: `name="restore"` at `cloud_restore:724`, then `last-${name}`. A deliberate saves restore and the automatic startup restore write it.
- **`cloud_sync_helper` names three of the stamps only to carry old names across** (`last-system-backup` to `last-settings-backup`, `last-system-restore` to `last-settings-restore`, `system-backup.uploaded` to `settings-backup.uploaded`; `:417-427`), with a plain `mv` per stamp, once. Its `last-run` hit is the comment at `:417`. It writes no stamp of its own.
- **`102-cloud-saves`'s `saves-root` hit is its comment** (`:48-53`). It writes nothing.

**The locks: two.**

- `cloud_sync.lock` (`/var/run`, tmpfs) is the twins' alone.
  - `take_cloud_lock` (`cloud_backup:457`, `cloud_restore:442`) opens fd 9 and tries `flock -n` five times, 0.25 s apart.
  - Then it exits `EXIT_LOCK_HELD` (75) with no stamp.
  - `main 9>&-` (`:2510`, `:2324`) runs the body with fd 9 closed, so no child can hold it.
  - **It is released on every path by the shell's exit**: there is no explicit unlock, and `clean_exit` and the `INT TERM` trap both `exit`.
- `.capture.lock` (`/storage/.cache/cloud_sync`) is the capture's alone.
  - `capture_lock` (`:252`) opens fd 8 for append and waits up to 50 times 0.1 s.
  - It is released by `capture_unlock` before a re-run's `exec`, or by exit.
  - Unlike the twins, **fd 8 is not closed for the children the capture starts while it holds it** (`jq`, `sha256sum`, `mv`). They are synchronous, so this matters only for a capture killed mid-child.
  - The capture never takes `cloud_sync.lock` (run r10: 0 hits). **`102-cloud-saves:44` says "Capture takes no lock"**: stale since PL-067 (blindspot 72's shape; Q7).
- **The exits:** `readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69` (`cloud_backup:20`, `cloud_restore:21`). `cloud_net_ready` has its own `EXIT_NO_NETWORK=69` (`:4`); the capture has none.
  - 75 never writes a stamp. It leaves from `take_cloud_lock` before `main`.
  - 69 leaves two ways:
    - before the run, by `check_network_link` or `check_internet`'s last branch: no stamp;
    - mid-run, by `network_lost_during_run`, through `clean_exit`: a stamp `<epoch> 69`, plus `gaps YOU WENT OFFLINE PART-WAY THROUGH` when a transfer of the run had moved a file.
  - **The header's "Neither writes a last-run stamp -- nothing ran" (`cloud_backup:69-71`) is true only of the first way** (Q7).
- **The bounds:** `SYNC_CEILING_SECONDS_FALLBACK=90` (`:57` in both twins).
  - An automatic run's deadline is `START_TIME + ceiling` (`load_config`, `cloud_backup:1403`). The `rclone()` wrapper (`:357`) starts nothing past it and runs each call under `timeout -k 3 <left>`.
  - A deliberate run has `bounded_rclone`'s stall ceiling: `--timeout`'s idle seconds plus 6, measured from the last progress in rclone's stats block.
  - The capture's exit bound is `EXIT_BOUND_MS=100000` (`:221`), checked before and after it waits for its lock.
- **The `>>> why` sentences each script prints:**

| Sentence | Printed by | In `es-player-text.md`'s table? | proved: |
| --- | --- | --- | --- |
| `COULDN'T FIND YOUR CLOUD FOLDER` (rclone 3/4, `why_for`) | both twins | **no**: the rule's rc list says `YOUR CLOUD FOLDER WASN'T FOUND` | tree |
| `YOUR CLOUD STOPPED ANSWERING` (rclone 5; a deliberate run's ceiling) | both twins | yes | tree |
| `SOME FILES DIDN'T FINISH` (6) | both twins | yes | tree |
| `YOUR CLOUD WOULDN'T TAKE THE FILES` (7/8) | both twins | the D-UI-031 register table, yes; **the rc list still says `YOUR CLOUD REFUSED THE TRANSFER`** | tree |
| `IT WAS STOPPED` (130) | both twins | yes | tree |
| `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` (10/124, automatic) | both twins | **no** | tree |
| `COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN` (`check_internet`) | both twins | **no**: the rule says `COULDN'T REACH YOUR CLOUD. YOU MAY NEED TO SIGN IN AGAIN` | tree |
| `YOUR CLOUD STORAGE ISN'T SET UP YET`, `YOUR SAVES FOLDER ISN'T ON THIS DEVICE`, `THIS DEVICE'S SETTINGS BACKUP IS DAMAGED`, `THE COPY IN YOUR CLOUD ISN'T COMPLETE`, `YOUR CLOUD SYNC SETTINGS COULDN'T BE READ`, `AN OLD FOLDER SETTING IS IN THE WAY` | the twins | yes | tree |
| `COULDN'T TELL WHICH CARD YOUR SAVES ARE ON`, `YOUR SAVES ARE ON A DIFFERENT CARD`, `YOUR SAVES CHANGED CARDS PART-WAY THROUGH`, `COULDN'T RECORD WHICH CARD YOUR SAVES ARE ON` | `cloud_saves_root`, relayed by the twins | yes | tree |

The rule says the six rc-keyed sentences are "duplicated verbatim in
`ThreadedCloudSync`'s own fallback map, so they change on both sides or
on neither". The script side has moved for 3/4 and 7/8 against the rule.
The ES map is named and not read, so whether it moved too is the ES
slice's question. The rule's stale list is #909's (T4's).

## The configuration

- **The keys:** 16 in `cloud_sync.conf`, 16 `DEFAULT_` in the defaults (run r11), and `comm -3` prints nothing under `LC_ALL=C` (run r12). Every key has its twin:
  - `SAVESPATH SETTINGS_BACKUPS SAVES_REMOTE SETTINGS_REMOTE CONTENT_REMOTE LOG_LEVEL`
  - `RCLONEOPTS RCLONE_NET_OPTS RCLONE_SYNC_NET_OPTS SYNC_CEILING_SECONDS`
  - `BACKUPMETHOD CLOUD_BACKUP_KEEP BACKUPFILE_BACKUP_OPTION RESTOREMETHOD BACKUPFILE_RESTORE_OPTION RSYNCRMDIR`
- **The shipped values that matter to the lens:**
  - `BACKUPMETHOD="copy"`, `RESTOREMETHOD="copy"`;
  - `RCLONEOPTS` carries `--progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt` and no `--delete-excluded`. Both twins strip that flag anyway (`sed`, `load_config`).
- **The allowlist:**
  - 54 rule lines, the same in `cloud_sync-rules.txt` and its `.defaults` (`diff` of the non-comment lines: rc 0).
  - The 23 differing lines of run r13 are comments.
  - One `- /**` catch-all in each. Both twins refuse the device's own rules file without it (`rules_whole`); a player's own `--filter-from` is used as written (#71).
- **What each script reads:**

| Script | How it reads the conf | proved: |
| --- | --- | --- |
| `cloud_backup`, `cloud_restore` | `cloud_sync_helper` first. Then `conf_valid` on the file (its `.bak` on failure). Then `source`, so bash takes **the last** of a repeated key. Then `cloud_sync_cleanup_duplicates.sh` under `--yes`, which keeps **the first** (PL-021: every reader is meant to read the first after it), and `source` again | tree |
| `cloud_saves_root`, `cloud_capture` | `sed -n 's/^SAVESPATH="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' | head -1`, then `BACKUPPATH`, then `/storage/roms`. Never sourced | tree |
| `cloud_sync_helper` | `conf_valid`, `grep`/`cut` per key, `sed -i` for four one-shot edits | tree |
| `cloud_net_ready`, `rasteratops-settings-archive`, `102-cloud-saves` | not at all | tree |

**The two readers disagree on a value `conf_valid` passes** (fixture, `/workspace/tmp/m6-t16/fx/`, run 11:46 UTC):

- `conf_valid`, lifted from `cloud_backup` at `8ebaf8daad`, passes all four of:
  - the shipped conf;
  - `SAVESPATH=""`;
  - `SAVESPATH=`;
  - `SAVESPATH="/storage/roms"   # my saves`.
- The `sed` reader prints nothing for the first and last (`[end]` with no value), so `cloud_saves_root` and `cloud_capture` fall back to `/storage/roms`, while the twins' `source` reads `""`, or the commented value.
- **With an empty `SAVESPATH`:**
  - the backup refuses (`[ ! -d "" ]`, `cloud_backup:1613`, `YOUR SAVES FOLDER ISN'T ON THIS DEVICE`);
  - **the restore goes on.** `cloud_restore:1758-1760` runs `mkdir -p ""` and ignores its failure, and `:1902-1906` copies `remote:<SAVES_REMOTE>/` into `"${SAVESPATH}/"`, which is `/`.
  - The card check passes, because it judged `/storage/roms`.
- What the restore then does on a device is the guest's to show (§ The guest cycle). `proved: fixture` for the readers, `tree` for the restore's path.

## The runs

Every § 5 command of the brief, run at stage A as one script file
(`/workspace/tmp/m6-t16/runs.sh`, 11:37 UTC); the outputs are in
`.qa-scratch/t16/runs.txt`.

| Run | What | Figure | rc | Wall | A FAIL would mean | proved: |
| --- | --- | --- | ---: | ---: | --- | --- |
| r1 | the membership's path list | 14 | 0 | 3 ms | the slice is not the 14 the order sizes: re-cut or a stale inventory | tool-run |
| r2 | the 14 against `8ebaf8daad` | [empty-above] | 0 | 5 ms | the read is not of `next`'s bytes for a path; every verdict on it needs its own hash | tool-run |
| r3 | lines at `8ebaf8daad` | 8316 | 0 | 29 ms | the inventory's line count is stale | tool-run |
| r4 | functions in the twins | 45; 47 | 0 | 5 ms | a twin grew or lost a function since the brief; the table's count moves | tool-run |
| r5 | shared function names | 39 | 0 | 5 ms | the twins' shared surface changed | tool-run |
| r6 | differing lines between the twins | 1622 | 0 | 4 ms | the twins drifted further (or converged) | tool-run |
| r7 | functions in the capture | 40 | 0 | 3 ms | the capture changed shape | tool-run |
| r8 | `cloud_backup`'s exits, ceiling, lock, bound and stamp writer | 20:readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69; 57:SYNC_CEILING_SECONDS_FALLBACK=90; 251:bounded_rclone() {; 457:take_cloud_lock() {; 716:record_last_run() { | 0 | 4 ms | a sentinel or a bound moved; ES reads the same two numbers | tool-run |
| r9 | the same in `cloud_restore` | 21:readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69; 57:SYNC_CEILING_SECONDS_FALLBACK=90; 238:bounded_rclone() {; 442:take_cloud_lock() {; 722:record_last_run() { | 0 | 3 ms | the twins disagree on a sentinel or a bound | tool-run |
| r10 | the capture's lock, stage and exit bound; `cloud_sync.lock` hits | 102:# GC, the stamp -- runs under /storage/.cache/cloud_sync/.capture.lock (audi; 118:STAGE="${CACHE}/stage"; 221:EXIT_BOUND_MS=100000; 243:# flock has no -w -- and then 1, and the caller does not commit (G-A-04);; 249:CAPTURE_LOCK="${CACHE}/.capture.lock"; 252:capture_lock() {; 259:    while ! flock -n 8 2>/dev/null; do; 301:    # way capture_lock fails sets LOCK_BUSY -- so a finish() lifted on its; 303:    if capture_lock // [ "${LOCK_BUSY:-0}" != 1 ]; then; 1599:if ! capture_lock; then; cloud_sync.lock hits: 0 | 0 | 5 ms | a hit would mean the capture takes the transfer lock, against its header (`:83`) | tool-run |
| r11 | keys in the conf and its defaults | 16; 16 | 0 | 4 ms | a key without its `DEFAULT_` twin never reaches an upgraded device (`upgrade-and-install.md`'s first row) | tool-run |
| r12 | keys present on one side only | [empty-above] | 0 | 4 ms | any line printed is such a key | tool-run |
| r13 | the rules file against its defaults | 23 | 0 | 3 ms | a change in rule lines (not comments) between what ships and what the helper merges in | tool-run |
| r14 | callers outside the directory | projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml; projects/ROCKNIX/packages/rocknix/sources/post-update; projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool; projects/ROCKNIX/packages/rocknix/sources/scripts/run; projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh | 0 | 124 ms | a new caller of the core this slice has not read | tool-run |
| r15 | `gamelist.xml`'s cloud entries | 64:        <path>./cloud_backup.sh</path>; 76:        <path>./cloud_restore.sh</path> | 0 | 3 ms | the dead tool entries were fixed (or moved) | tool-run |
| r16 | `post-update`'s removal loop | 4:for tool in cloud_backup cloud_restore; do; 7:    rm -f "${link}" | 0 | 3 ms | the legacy symlinks are no longer removed | tool-run |
| r17 | files naming each stamp | last-backup: projects/ROCKNIX/packages/network/rclone/sources/cloud_backup:1 ; last-settings-backup: projects/ROCKNIX/packages/network/rclone/sources/cloud_backup:1 projects/ROCKNIX/packages/network/rclone/sources/cloud_sync_helper:1 ; last-settings-restore: projects/ROCKNIX/packages/network/rclone/sources/cloud_restore:1 projects/ROCKNIX/packages/network/rclone/sources/cloud_sync_helper:1 ; last-run: projects/ROCKNIX/packages/network/rclone/sources/cloud_backup:3 projects/ROCKNIX/packages/network/rclone/sources/cloud_restore:1 projects/ROCKNIX/packages/network/rclone/sources/cloud_sync_helper:1 ; last-capture: projects/ROCKNIX/packages/network/rclone/sources/cloud_capture:7 ; capture-failures: projects/ROCKNIX/packages/network/rclone/sources/cloud_capture:6 ; saves-root: projects/ROCKNIX/packages/network/rclone/autostart/102-cloud-saves:1 projects/ROCKNIX/packages/network/rclone/sources/cloud_capture:1 projects/ROCKNIX/packages/network/rclone/sources/cloud_saves_root:3 ; last-sync: | 0 | 37 ms | a stamp's writer or reader moved | tool-run |
| r18 | non-merge commits since June, and how many are fork identities | 145; 145;     131 Max Engel;      10 blitterbot;       4 rasterabot | 0 | 34 ms | a commit by another identity: an upstream change inside the fork's own files | tool-run |
| r19 | upstream's change to the directory since the base | [empty-above]; 0 | 0 | 6 ms | the next base merge brings changes here | tool-run |
| r20 | the 14 since the base | 14 files changed, 6976 insertions(+), 338 deletions(-) | 0 | 8 ms | the fork's delta moved | tool-run |
| r21 | T13's table lines | 81 | 0 | 3 ms | T13's table is not 79 rows: the oracle is not the accepted one | tool-run |
| r22 | T13's Oracle column | 25 / both ends /;       8 / device report /;      46 / synthetic / | 0 | 4 ms | the oracle classes moved since T13's acceptance | tool-run |
| r23 | the harness's mentions of each script | cloud_backup 70 cloud_capture 66 cloud_restore 33 cloud_saves_root 18 102-cloud-saves 5 cloud_sync_helper 3 cloud_net_ready 0 rasteratops-settings-archive 0 cloud_sync_cleanup_duplicates.sh 0 | 0 | 30 ms | a script the harness never names has no oracle row of its own | tool-run |
| r24 | the removal rule's check from the dispatch tip | [empty-above] | 0 | 3 ms | this lane changed `packages/`, `projects/` or `tools/` at stages A to D | tool-run |
| r25 | all-time commits and the first | 151; 9f1fab30f6 ROCKNIX Team 2025-07-13 | 0 | 214 ms | the history's start is not upstream's import | tool-run |
| r26 | T13's branch tip | 0b72904621 | 0 | 3 ms | the oracle was read from a branch that moved after its acceptance | tool-run |

## The guest cycle

**The windows.**
- **The first**, START 2026-10-25 11:56:21Z, was cut by the lane's usage limit after the boot. No verdict came from it.
- **The second** was granted on #663 at 2026-10-29 18:09: START 18:10:18Z (census 0), the bound 18:40:18, the grace 18:45:18.
  - **It was stopped by pidfile at 22:31:21, 3 h 46 min past the grace**: the lane's session was cut again at about 18:19, and the guest sat idle.
  - RETURN was posted on #663 and on the host file. The record is `guest-cycle/`.

**The image.**
- M6's copy, `/workspace/artifacts/m6-t3-20261024/…g069fc2704421….img.gz` (sha256 `6b4c3079…`), by `tools/vm-pair reimage a` under `VM_PAIR_DIR=/workspace/tmp/m6-t16/vm-pair-2`.
- The guest's `/etc/os-release`: `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"` (`guest-cycle/os-release.txt`).

**The image against the tree, before any verdict.**
- `sha256sum` on the guest of the nine scripts (`102-cloud-saves` at `/usr/lib/autostart/common/`) and the four `/usr/config` files, against `git show 8ebaf8daad:<path>`: **13 of 13 identical** (`guest-cycle/image-vs-tree.txt`, `installed.sha256`).
- No verdict below needs a difference written beside it. The guest ran the read bytes.

**The harness.** `tools/` at `3a653eaec4` (T13's fixes), from the `--shared` clone at `/workspace/tmp/m6-t16/harness`; the worktree's `vm-pair` booted the guest (identical at both hashes).

| Run | Harness | Result | Verdict | proved: |
| --- | --- | --- | --- | --- |
| the suite over WebDAV, first | `3a653eaec4` | 100 passed, 3 failed, rc 1, 73 s | **void**: the clone has `tools/` only, so `cloud-test-backend saves-remote` read no shipped default and the suite ran with `SAVES_REMOTE=""` (`suite-webdav.out`: `SAVES_REMOTE  on the webdav endpoint`); the lane's setup error | guest |
| the suite over WebDAV | `3a653eaec4`, `CLOUD_QA_DEFAULTS` = the `8ebaf8daad` defaults | `PASSED -- backend webdav (hash=none modtime=no commit=partial bucket=no): 108 passed, 0 failed, 0 skipped`, rc 0, 82 s (`suite-webdav-2.out`) | the oracle's both-ends rows that the suite holds (steps 2, 5, 8, 17, 18, 19, 22, 23, 27, 32) pass on the read bytes; T13's 108 reproduced | guest |
| KILL15 | `3a653eaec4` | 6 passed, 1 failed (`cells-1.out`) | the empty saves-root record is refused (exit 1); **FAIL**: `cloud_saves_root`'s last line, `If both cards are in the device, try again.`, is not one of the three outcome sentences (`cloud_saves_root:137-139`; `es-player-text.md` § Outcome vocabulary) | guest |
| LINK1, LINK2, LINK6 (200k) | `3a653eaec4` | each exit 69 with `Couldn't finish: lost the network during the saves restore/backup. Try again ...`; no FAIL (`cells-3.out`, `cells-3/LINK*`) | the link cut ends in the sentinel and an outcome line, on the restore, the backup and the exit sync | guest |
| KILL2 (200k) | `3a653eaec4` | 3 FAIL (`cells-3.out`, `cells-3/KILL2a`, `KILL2b`) | **2a** (TERM then KILL at 1.5 s) and **2b** (SIGKILL): two saves **absent** from `SAVESPATH` after the stop in each arm, while the previous version of each "is kept somewhere" and a re-run restores them; **2b**: three `*.partial` under `SAVESPATH` until the re-run sweeps them (the tree is clean at the cell's end). Read with the code at stage C before it is graded: the shape is `--backup-dir` moving the replaced save aside before the new copy lands | guest |

**Graded at stage C** (§ The host leads, below): KILL15's FAIL is the harness's (F-15); KILL2's absent saves are F-14. The `.partial` FAIL's "nothing removes it" is the cell's word, not the code's: the re-run's `sweep_partials` removes them (`cloud_restore:1898-1913`; the cell's own last check reads the tree clean).

**Not run on the guest:**
- leads (a) to (e) of the plan. (a), (b), (d) and (e) ran on the host at stage C (§ The host leads, below); (c) is `(window)`-pending;
- the brief's extra both-ends cells (LINK3, LINK5, KILL4, A1, A2, A8, A9, A11, A14);
- `tools/time-to-play --vm`: **not run.** The session was cut, and then the bound had passed. **No figure was measured, and none is cited** in this folder. *Corrected 2026-10-30:* this line first said `CANNOT`, with the last `docs/vm-qa-log.md` figure "cited in `04` § Q5"; `04` § Q5 cited none. The RETURN post repeated the error.

**The stop and the leftovers:**
- `tools/vm-pair down`: `down: owned QEMU exited (pid 1792756)`; the WebDAV `down`.
- `guest-cycle/leftover.txt`: qemu 0, compilers 0, listeners 0.

**The disks** (`guest-cycle/retire.txt`, D-INFRA-022):
- the retained `vm-pair/vm-a.qcow2` (2,310,799,360 bytes, sha256 `27d1a5e5…`);
- the window's `vm-pair-2/vm-a.qcow2` (2,331,246,592 bytes, sha256 `bc8e8a19…`);
- both removed with their directories after the stop; +4,643,045,376 bytes.

## The host leads (stage C, 2026-10-30)

The coordinator's ruling on #663 (05:15 UTC): no second window now. (a), (b), (d) and (e) run on the host, with the image's own binaries, as stage-C cells. (c) and whatever a host run cannot show are `(window)`-pending, for stage E and the integration window. Can this be done on the VM? Yes, and four of the five without a guest. The host is the cheaper answer `vm-first.md` asks for first.

**What the host runs.**
- **From the donor root** `/workspace/artifacts/m6-donor/1a0266484423/image/system`:
  - busybox v1.36.1 with its 146 applet links, which stand in front of everything else;
  - rclone v1.75.2;
  - `etc/os-release`.
  - Its `sha256sum -c ../../SHA256SUMS` reads OK for all three; every cell's `out` opens with that line.
  - The donor holds no cloud script (its `RECORD.txt`: busybox, rclone and os-release only).
- **The scripts and `/usr/config`:** `git show 8ebaf8daad`. All 12 are sha256-equal to the guest's installed bytes (`guest-cycle/installed.sha256`).
- **The host stands in where the donor has nothing:**

  | Program | On the host | On the image |
  | --- | --- | --- |
  | bash | 5.3.9 | 5.3 |
  | `timeout` | GNU coreutils 9.7, by `gnu<name>` (the host's default is uutils) | GNU 9.4 |
  | grep | GNU 3.12 | GNU 3.9 |
  | python3 | 3.14.4 | |
  | `ip` | iproute2 | |

- **The sandbox:** `host-leads/sandbox/` (`mkroot.sh`, `sbx.sh`, `lib.sh`).
  - bwrap, after T15's `tools/last-good-scripts-test` model.
  - Its own pid namespace; the host network; `/storage`, `/var/log`, `/var/run`, `/run` and `/tmp` writable.
  - `RO=1` remounts `/` read-only, as the squashfs is.
- **The backend:** `cloud-test-backend` at `3a653eaec4`, WebDAV on 127.0.0.1:9010, state `/workspace/tmp/m6-t16/hl/state`. It was stopped by its pidfile at the end.
- **The `proved:` cells** read `fixture` where a constructed input ran a script, or the donor's rclone, whole in the sandbox; and `tool-run` where the donor's binary was asked directly.
- **The host file** carries the cells' opening line (05:24:09Z) and closing line (05:34:11Z). No guest, compiler or build ran.

| Cell | Command | Result | Verdict | proved: |
| --- | --- | --- | --- | --- |
| `a-awk` (lead a) | the donor's `awk`, and two `gensub` calls under its busybox; then `cloud_sync_cleanup_duplicates.sh`, whole in the sandbox, on the shipped conf with `LOG_LEVEL` and a three-line `RCLONEOPTS` repeated | `awk -> busybox`; `gensub` prints `a` and `a<b>c<b>`, rc 0; the cleanup, rc 0, leaves one `LOG_LEVEL` and one `RCLONEOPTS`, and `bash -n` passes | **busybox 1.36.1 awk has `gensub`**, so the cleanup works on the image. `cloud_restore:764-765`'s "busybox awk: no gensub" is false (F-09). A48 ran busybox awk (its `nbin` carries `awk`, `tools/last-good-scripts-test:8983`) and was right | tool-run |
| `d-terminal-width` (lead d) | the donor rclone: `help \| grep -c progress-terminal-width`; `help flags \| grep -c`; `lsf <dir> --progress-terminal-width=80` | 0; 0; `Error: unknown flag: --progress-terminal-width`, rc 2. The probe costs 22-24 ms here and never matches | **rclone 1.75.2 has no such flag.** The scripts' probe (`cloud_restore:1893`, `:2028`; `cloud_backup:2054`) can never add it, so each probe is an rclone start for nothing (F-05, F-06). The device's figure is lead (c)'s | tool-run |
| `b-empty-savespath` (lead b) | `cloud_restore --yes --saves-only`, whole, in four arms. **ctl:** the shipped `SAVESPATH`. **ro:** `SAVESPATH=""`, `/` read-only. **rw:** `SAVESPATH=""`, `/` writable. **bk:** `cloud_backup --yes --saves-only` with `SAVESPATH=""` | **ctl:** rc 0, `Completed.`, both cloud saves under `/storage/roms`. **ro and rw:** rc 7; `mkdir: can't create directory ''` in the output; rclone `Failed to copy: destination and parameter to --backup-dir mustn't overlap`, a fatal error before any transfer; `>>> why YOUR CLOUD WOULDN'T TAKE THE FILES`; `Couldn't finish: your cloud wouldn't take the files. Try again.`; stamp `7`; **no file restored anywhere**. **bk:** rc 1, `YOUR SAVES FOLDER ISN'T ON THIS DEVICE` (`cloud_backup:1613`) | **F-02 re-graded.** Nothing is copied into `/`, whatever `/`'s mode: rclone's overlap check on `--backup-dir` refuses first. That guard is an accident. The player is told the cloud refused, and a retry cannot succeed. The backup twin refuses correctly; the restore has no such test | fixture |
| `e-term-automatic` (lead e) | `cloud_restore --automatic --yes --saves-only`, whole, against the WebDAV at 100k (`CLOUD_QA_BWLIMIT`), one 6 MiB save to fetch. **term:** TERM to the script's pid at +5 s. **termkill:** TERM at +5 s, KILL at +9 s. **termkill-game:** the same, then at +11 s the "game" writes 10 bytes to the name the orphan is fetching (`out-game`). The 2 MiB first try (`out.2mib`) finished before +9 s | **term:** the trap ran at +41 s, when the foreground `timeout -k 3 90 rclone` returned. The save landed whole; exit 130, stamp `130`. **termkill:** after the KILL, `timeout` and `rclone` run on with ppid 1. A whole save landed 12-32 s after the script was gone, and the next was mid-transfer at +41 s. No stamp. **termkill-game:** at the end the game's file holds 6,291,456 bytes, the cloud's. **No file anywhere holds the game's 10 bytes** (a whole-content `cmp`), and nothing is under `replaced/` | **F-03 proved on the host, and worse than graded.** A TERM waits out the transfer (36 s here), and the run is then stamped "stopped" over a save that landed. A KILL to the script alone leaves the transfer running unlocked to its 90 s deadline, and **its rename replaces a save written after the stop, with no copy kept** | fixture |
| `f14-backup-dir-order` (KILL2) | the donor rclone alone: `copy cloud/ saves/ --backup-dir replaced/run1 --bwlimit 200k --transfers 1`, three local saves to be replaced, SIGKILL at +1.5 s; then `lsf -R --filter-from <shipped rules>` on what is left | At +1.5 s, all three local saves are already in `replaced/run1` (`Moved (server-side)` ×3 logged before 220 KiB of the first copy), and `saves/` holds one `.partial`. After the kill, the same. The allowlist lists `savestates/f1.state.b2048630.partial` | **F-14.** rclone moves every file it will replace aside at check time, before the transfers. So a stopped restore leaves those saves absent (KILL2: two per arm, the third the game's), and the `.partial` a SIGKILL leaves is admitted to the next backup | fixture; guest (KILL2) |
| `k15-at-the-run` (KILL15) | an empty saves-root record; `cloud_saves_root check` alone, then each twin `--yes --saves-only`, in the sandbox | check alone ends `If both cards are in the device, try again.` Both twins end `Couldn't finish: couldn't tell which card your saves are on. Try again.`, rc 1, stamp `1 COULDN'T_TELL_WHICH_CARD_YOUR_SAVES_ARE_ON`; the local save untouched | **KILL15's FAIL is the harness's.** `fx_kill15` (`tools/cloud-round-trip:7747-7772`) asserts a run's outcome line on a helper whose lines reach a player only through the twins, which end on an outcome sentence (F-15) | fixture |

**Still `(window)`-pending (stage E and the integration window, `fix-walk-pending-image`):**
- lead (c), every timing on the image (F-05);
- F-03 under the image's own bash 5.3 and coreutils 9.4. The host ran 5.3.9 and 9.7: the trap's deferral is bash's documented order, and the orphan's bound is `timeout`'s own;
- how EmulationStation stops an automatic run, which is the ES slice's. A group kill gives F-14; a signal to the script alone gives F-03.

**No second window is asked for.** No host lead found a fact that only the guest can settle, beyond the three named here.

## Leads for stage C and the window

Each is a question the lane has read and not yet graded. Each becomes a
finding with its question in `04` and `05`, or is withdrawn with its reason.

1. **Q3, the conf fallback that sources what it refused.**
   - `load_config`, identical in both twins: at `cloud_backup:1209-1222` a refused conf with a valid `.bak` runs `cp -f .bak .tmp.$$ && mv -f .tmp.$$ conf`, and neither status is read.
   - `source "${conf}"` at `:1222` then runs on whatever is there. If the `cp` or the `mv` fails (a full card), that is the file `conf_valid` refused, and the `.tmp.$$` is left behind.
   - The guard is skipped exactly when the disk is the cause.
2. **Q3, an empty or commented `SAVESPATH`** (§ The configuration): the restore copies into `/`, and the card check judges another path.
3. **Q2/Q7, the why sentences against the rule and the ES fallback map** (§ The stamps and locks).
4. **Q5, time to play on the exit path.**
   - Every twin run starts `cloud_sync_helper` (`load_config:1197-1199`): a log trim, a rules merge with one `grep -F` per rule line, two `conf_valid`s, a pass over the defaults, and four `grep`/`sed -i` one-shots.
   - `cloud_restore`'s saves phase starts `rclone help` (`:1893`) for a display flag.
   - `cloud_backup`'s settings phase starts `rclone help` (`:2054`) for a flag its own loop then drops (`:2170`).
   - What these cost against D-CLOUD-119's 3 s is the window's `time-to-play` and journal to answer, with the exit sync's flags read from the harness (`cloud_backup --automatic --recent --saves-only` is the shape the brief names; ES's own flags are not read).
5. **Q6, dead code:**
   - the three uncalled restore functions (76 lines);
   - `cloud_backup:2054-2056` (a flag added only to be removed);
   - `logged_moved` at `cloud_backup:1539` and `cloud_restore`'s twin, which measures `LOG_FILE` from its size *after* the transfer, so with the shipped `--log-file` its log half can never match. The wrapper's own check (`:371-373`) and the stall ceiling's trace cover it.
6. **Q3, `cloud_sync_helper`'s key test is a substring** (`grep -qF "${var_name}=" "${work}"`, `cloud_sync_helper:462`): a missing key that some comment or other line names is never added. No shipped key is another's suffix and no shipped comment names one, so this is a latent shape (Low) unless the window finds a conf that shows it.
7. **Q3, the helper's `-v ` edit** rewrites the conf in place with `sed -i` and no `conf_valid` after (`cloud_sync_helper:536-544`), including `s/  \+/ /g` across every value. It is gated on `--verbose` or `-v ` appearing anywhere; the shipped conf has neither (grep: 0).
8. **Q3, the capture's stage GC on a failed read** (`:1649-1686`): `STAGE_REF` is filled from a `jq` whose status is not read. A failed read leaves it empty, and every seal older than 600 s goes. No consumer of `stage/` exists today (#1057), so the cost is a future reconciler's evidence (blindspot 22's shape).
9. **Q1/Q5, `cloud_net_ready`'s 3 s grace** is counted from its own first look, not the link's age (`cloud_net_ready:199`), so every startup sync waits at least 3 s on a network up for hours.
10. **Q3/Q5, `trap '' TERM` in the capture** (`:136`) with an unbounded `--full`: a boot pass still running at power-off holds the stop until systemd's kill. The guest's journal can time one `--full`.
11. **Q4, the recipe's `unpack`** removes the download from the shared source cache (`rm -f ${SOURCES}/rclone/rclone-${PKG_VERSION}*`, `package.mk:58`, since the ROCKNIX import `9f1fab30f6`), so every rebuild of rclone fetches again; in a container without DNS it cannot rebuild.
12. **Q3, the trap and the automatic run's foreground `timeout rclone`.**
    - Bash runs a trap only after the foreground child returns.
    - So a SIGTERM to an automatic run waits out the call it is in, up to the ceiling's remainder.
    - How EmulationStation stops a run for STOP IT AND PLAY (D-CLOUD-130) is not read here; KILL2 and KILL15 are the window's cells for the stop paths.

## Positives

For each lead that became a defect: the input constructed to make the
code at `8ebaf8daad` FAIL, the command, and the FAIL observed. A finding
with no constructed FAIL says so.

| Finding | The constructed input | The command | The FAIL observed | proved: |
| --- | --- | --- | --- | --- |
| F-01 | a refused conf, a valid `.bak`, and a `cp` that fails (standing for a full card) | `fixtures/load-config-fallback.sh`, against both twins | `sourced_refused=YES`, `load_config` rc 0, the refused conf still in place | fixture |
| F-02 | `SAVESPATH=""` in the shipped conf; two saves in the cloud | `host-leads/b-empty-savespath` (ro and rw arms) | `Couldn't finish: your cloud wouldn't take the files. Try again.` for a fault on the device, stamp `7`, `mkdir: can't create directory ''` in the output. The control arm completes | fixture |
| F-03 | an automatic restore of a 6 MiB save at 100k; TERM, then KILL, to the script alone; a save written at +11 s | `host-leads/e-term-automatic` (`out`, `out-game`) | the trap waits 36 s; after the KILL, `rclone` runs on with ppid 1; the save written after the stop is replaced by the cloud's bytes, and no copy is kept | fixture |
| F-03, the control | the deliberate restore, its process group stopped | KILL2 on the guest | the save the game wrote 1 s after the stop still stands 5 s later | guest |
| F-06 | none needed: the probe's input is rclone's own help | `host-leads/d-terminal-width` | `unknown flag: --progress-terminal-width`, rc 2; the scripts' grep never matches | tool-run |
| F-09 (`:764`) | the comment's claim, put to the image's busybox | `host-leads/a-awk` | `gensub` works, so the comment is false | tool-run |
| F-14 | three local saves to be replaced by newer cloud copies; the transfer stopped part-way | KILL2 (guest, the real script); `host-leads/f14-backup-dir-order` (the bare rclone) | the saves are absent from `SAVESPATH` after the stop: two per arm on the guest, three of three on the host. The allowlist admits the `.partial` | guest, fixture |
| F-15 | an empty saves-root record | `host-leads/k15-at-the-run` | **no FAIL at the run**: the twins end on an outcome sentence. The FAIL is the cell's | fixture |

F-04, F-05, F-07, F-08, F-10 to F-13 have no constructed FAIL: they are
read at their lines (`04`). F-05's cost on the device is lead (c)'s, and
`(window)`-pending.


## The first reader's 03-retrospective.md (whole)

# T16 retrospective: the cloud sync core (#663)

Phase 3 of the code-auditor method: what the record of these 14 files
says about how they came to be, before `04` judges them. It is about the
*area*; the slice's own retro is written at stage G
(`docs/retros/<date>-m6-cloud-sync-core.md`).

## The shape of the history

- **151 commits all-time**, every one after the first a fork identity (run r25). The first, `9f1fab30f6`, is ROCKNIX's import of 2025-07-13.
- **By month:** 2025-07 to 2025-10: 6; 2026-07: 7; 2026-08: 14; **2026-09: 110**; 2026-10: 14. The September burst is the release-candidate rounds and the two audits of them (#307, #308, and "the audit of the fixes").
- **Since the base the 14 are +6,976 / -338** (run r20). Five files are new since then: the capture, `cloud_net_ready`, `cloud_saves_root`, the settings-archive helper and the boot hook.
- **Upstream has not touched the directory since the base** (run r19), so nothing here is a merge risk: the next base merge brings none of it.
- **The issues the commits cite most** (subjects): #21 (the save manifest), #141 (bucket presence), #99 (the sentinel exits), #94 (the startup sync moved into ES), #86 (the device id), #83 (the saves root's card), #192, #153 (the deliberate ceiling), #143 (the listing bound), #127, #103.

## What the code itself records

The scripts carry their history as comments, at a density no other slice
has: most functions open with the incident that made them. The comments
are the authors' claims (blindspot 31). Where `02` checked one against the
code, two were stale:
- `cloud_backup:69-71` says neither sentinel writes a stamp, while a 69 from a run the network cut does;
- `102-cloud-saves:44` says the capture takes no lock, while it takes `.capture.lock` since PL-067.

The pattern is blindspot 72's: a comment held an invariant the code had
stopped keeping.

## The recurring classes, from the blindspot register and the code's own comments

- **Success over a no-op** (blindspots 13, 33): `cloud_restore`'s `backup/*.zip` filter, the sentinel 3 and 4 borrowed from rclone, the size-only remote. Each fix in the code is a positive check: `rules_whole`, the size check before the upload marker, 75 and 69 above rclone's range.
- **A guard that falls open when its machinery breaks** (blindspot 22): `ls A B`'s status, the pipeline's last stage, the unquoted list. The read finds two more of the shape (`02` § Leads 1 and 8).
- **Two copies of one thing** (blindspot 28; the copy-twins):
  - the twins share 39 functions, 34 of them byte for byte;
  - `conf_valid` is a third copy in the helper;
  - the conf has two readers that disagree on a value all three copies of the gate pass (`02` § The configuration).
- **Fixed forward, not backward** (blindspots 10, 62): the helper's one-shot edits are the backward half (BACKUPMETHOD to copy, the retry counts, the stamp renames), each guarded by its own marker file.

## Decisions the read found implemented

- **D-CLOUD-109 / D-CLOUD-130, not D-CLOUD-076.**
  - The scripts have no launch-cancel path.
  - An automatic run is bounded from its start (`SYNC_DEADLINE`, the `rclone()` wrapper's `timeout -k 3 <left>`) and ends with an outcome, not a cancel.
  - The question STOP IT AND PLAY / KEEP WAITING is EmulationStation's (named, not read).
- **D-CLOUD-078, the last known good:** the stamps are temp-and-rename; the upload marker only after the size check; the retention only after it; the `.bak` copies removed by a run that completed.
- **D-CLOUD-175/178/179:** no folder migration remains in these 14. `superseded_saves_setting` recognises `/GAMES` and `/ROCKNIX/Saves` only to refuse creating them.

## Carried to `04`

The twelve leads of `02` § Leads, the three uncalled functions, and the
two stale comments above.


## The first reader's 04-analysis.md (whole)

# T16 analysis: the cloud sync core (#663)

The first reader's analysis (Opus 5.5, high effort). It was written before
the seats and the guest window, then graded at stage C against the window's
record and the host leads (`02` § The guest cycle and § The host leads,
2026-10-29 and 2026-10-30). A finding still marked **(window)** has its
deciding observation pending, for stage E and the integration window
(`fix-walk-pending-image`).

## Executive Summary

The core is the most defended code in the fork. Every outcome is written
temp-and-rename. Every bound is applied in one wrapper. The allowlist is
refused when its catch-all is missing, and the sentinels sit above rclone's
range. **The read tree implements D-CLOUD-109/130, not the superseded
D-CLOUD-076**: no launch-cancel path exists in the scripts, and an
automatic run is bounded from its start.

What the read finds are **guards that fall open when their own machinery
breaks**, two **copies that disagree**, and **cost on the exit path**:

| ID | Question | Severity | The finding | proved: |
| --- | --- | --- | --- | --- |
| F-01 | Q3 | Medium | `load_config` (identical in both twins) sources the conf `conf_valid` refused when the `.bak` put-back's `cp` fails, as on a full card: a torn file is run with, and a refused line executes | fixture |
| F-02 | Q3 | Low | an empty or commented `SAVESPATH` passes `conf_valid`, and the `sed` reader of `cloud_saves_root`/`cloud_capture` reads the default instead. The restore has no test for it (the backup has, `:1613`). It reaches rclone, which refuses on its `--backup-dir` overlap check before any transfer, and the player reads `Couldn't finish: your cloud wouldn't take the files. Try again.`, the wrong reason with a retry that cannot work. **Nothing is copied into `/`, but only by accident**: a fix to F-14 that drops `--backup-dir` would open it | fixture |
| F-03 | Q3 | **High if ES signals the script alone** (window: the image's bash and coreutils; the ES slice: the stop's shape) | an automatic run's TERM waits behind its foreground `timeout ... rclone` (36 s on the host), and the run is then stamped "stopped" over a save that landed. A KILL to the script alone leaves `timeout` and `rclone` running unlocked to the 90 s deadline, and **their rename replaces a save the game wrote after the stop, with no copy kept**. KILL2, the oracle's stop cell, runs the deliberate shape, whose group is stopped | fixture |
| F-04 | Q2 | Low | the `>>> why` sentences for rclone 3/4 and 7/8 differ from `es-player-text.md`'s rc list, and two the scripts print are in no table; the ES fallback map that must change with them is unread | tree |
| F-05 | Q5 | Medium (window) | every twin run, the exit sync's included, starts `cloud_sync_helper` (a rules merge with a `grep` per rule line, two `conf_valid`s, a pass over the defaults); the restore's saves phase and both settings phases start `rclone help` for a flag rclone 1.75.2 does not have (22-24 ms each on the host); `cloud_net_ready` holds 3 s from its own first look on any startup | tree, tool-run |
| F-06 | Q6 | Low | dead code: `controller_menu`, `get_controller_devices` and `device_folder` in `cloud_restore` (76 lines, no caller); the `--progress-terminal-width` probe at `cloud_restore:1893`, `:2028` and `cloud_backup:2054` can never match (`unknown flag` on 1.75.2), and `:2170` would drop it anyway; `logged_moved` at `:1539` reads `LOG_FILE` from its size after the transfer | tree, tool-run |
| F-07 | Q3 | Low | `cloud_sync_helper` adds a missing key only when no line contains `KEY=` anywhere (`:462`, unanchored `grep -F`); its `-v` edit rewrites the conf in place with no `conf_valid` after (`:536-544`) | tree |
| F-08 | Q3 | Low | the capture's stage GC reads its keep-list from a `jq` whose status is not checked (`:1649-1652`): a failed read keeps nothing, and every seal older than 600 s goes | tree |
| F-09 | Q7 | Low | three comments state what is not so: `cloud_backup:69-71` and `102-cloud-saves:44` (invariants the code stopped keeping); `cloud_restore:764-765`, "busybox awk: no gensub", which the image's busybox 1.36.1 has. The brief's "there is no `last-restore`" is the same shape in a document | tree, tool-run |
| F-10 | Q4 | Low | `package.mk`'s `unpack` deletes the download from the shared source cache (`:58`), so every rebuild fetches rclone again and a container without DNS cannot rebuild it | tree |
| F-11 | Q1 | design | the twins share 34 byte-identical functions and the helper carries a third `conf_valid`: one sourced library would make the gate one thing | design |
| F-12 | Q3/Q5 | Low (window) | the capture ignores TERM (`:136`); its exit mode is bounded at 100 s, its boot `--full` is not, so a pass still running at power-off holds the stop until systemd's kill | tree |
| F-13 | Q3 | Low | unquoted expansions: `mkdir -p ${SETTINGS_BACKUPS}` (`cloud_restore:1993`); `for opt in ${RCLONEOPTS}` (both twins), which globs; `cloud_saves_root check --wait` as the last argument loops for ever on bash's failed `shift 2` (`:126`) | tree |
| F-14 | Q3 | Medium | the restore's `--backup-dir` (`cloud_restore:1869-1871`) has rclone move every save it will replace aside at check time, before any transfer. A restore stopped part-way leaves those saves **absent** until a completed restore: the player who stopped it to play opens the game with no save. The `.partial` a SIGKILL leaves is admitted by the allowlist (`+ /savestates/**`), so a backup before the next restore sends it | guest, fixture |
| F-15 | Q2 | Low (oracle) | KILL15's FAIL is the harness's: `fx_kill15` (`tools/cloud-round-trip:7747-7772`) holds `cloud_saves_root check`'s own last line to a run's outcome vocabulary, but a player reads that helper only through the twins, which end on `Couldn't finish: couldn't tell which card your saves are on. Try again.` A proposal for T13's harness, not a code defect | fixture |

## Acceptance-criteria scorecard

The slice's criteria are #663's seventeen (brief § 7). At stage C:

| Criterion | State |
| --- | --- |
| folder `00`-`05` | `00`-`04` written; `05` at stage D |
| lint `PASS` | pre-issue lint at stage C's end |
| review plan and provenance | after the seats |
| punch-list issue at Phase 7 | stage D onward |
| `reviewed-at` / `fixed-at`; the 14 at `8ebaf8daad`; nothing under `packages/`, `projects/`, `tools/` | run r2 empty; run r24 empty |
| `01` § Scope | done |
| `02` § Coverage 14 | done (`awk ... | grep -c` prints 14) |
| `02` § The functions 132 | done, generated |
| `02` § The oracle | done, generated; the counts are under Q2 below |
| `02` § The stamps and locks; § The configuration | done |
| `02` § The runs | done |
| `02` § The guest cycle | done: the window (2026-10-29) and the host leads (2026-10-30) |
| `00` shows no build, fetch, handheld, hosted account | so far |
| `04` § Q3 bugs with three lines; § Q2; § Q6; § Q7; § Second opinion | Q3-Q7 below; the seats after the window |
| `proved:` cells; `question:` cells | `02` every table; `05` at stage D |
| retro | stage G |
| the five checkers | at hand-back |

## Risk Assessment

- **Highest:**
  - **A stop over a restore costs a save in either shape.**
    - Under F-03, a signal to the script alone leaves the transfer running, and its rename replaces what the game wrote after the stop, with no copy kept (host, `out-game`).
    - Under F-14, a group stop leaves the replaced saves absent until a completed restore (KILL2 on the guest).
    - Which one the player meets is how EmulationStation stops STOP IT AND PLAY (D-CLOUD-130). That is the ES slice's to read.
  - **F-02 no longer writes into `/`.** rclone's `--backup-dir` overlap check refuses first. That makes F-14's fix and F-02's one change: a restore without `--backup-dir` must first refuse an empty `SAVESPATH` as the backup does (`cloud_backup:1613`).
- **Data at risk from F-01:** a torn conf run with missing keys. `SAVES_REMOTE` unset sends a backup to the cloud's root folder.
  - The guard was written for exactly this (D-CLOUD-078, #105).
  - It holds unless the card is full, which is when a torn write is most likely.
- **No finding loses a save already in the cloud:**
  - `copy` is the default both ways;
  - `--delete-excluded` is stripped;
  - `--backup-dir` keeps every replaced copy for one cycle.

## Coverage Boundary

- **Read:** the 14 at `8ebaf8daad` (`02` § Coverage); the harness at `8ebaf8daad` for the oracle; `cloud_content_restore:780-795` for the shared `restore-tree-clean` record (T17's file, one paragraph).
- **Named, not read:** EmulationStation's `ThreadedCloudSync`, `FileData::launchGame`, `GuiCloudTransfer`, `CloudText`. These are the ES slices': how ES invokes and stops these scripts, and its why fallback map.
- **T17's callees:** `cloud_remote`, `cloud_device_id`, `cloud_log_scrub`, `cloud_scan` and the content scripts. Their call sites are read; their internals are not.

## Finding Verification (Phase 4.5)

Each finding was re-read at its lines after `02` was written. Each has a
proof:
- **F-01:** the fixture `fixtures/load-config-fallback.sh`, against both twins at `8ebaf8daad`.
  - With `cp` working, the refused conf is replaced by the `.bak`, nothing it holds runs, and the conf is valid after.
  - **With `cp` failing** (the planted input, standing for a full card), its planted line ran (`sourced_refused=YES`), `load_config` returned 0, and the conf was still the refused one.
  - The same in both twins.
- **F-02:** the readers' disagreement is a fixture (`02` § The configuration). The restore whole, on the host with the image's busybox and rclone (`host-leads/b-empty-savespath`), against a control that completes: rc 7, rclone's overlap refusal, no file anywhere. The backup twin refuses at `:1613`.
- **F-03:** `fixtures/trap-defer.sh`. A TERM at +1 s ran the trap at +6 s, when the foreground `timeout -k 3 6` child returned (bash runs a trap only between foreground commands). `cloud_backup:372` and `cloud_restore:359` run the automatic call in the foreground; `bounded_rclone` (deliberate) backgrounds it and `wait`s, which a trap interrupts.
  - Then the restore whole on the host (`host-leads/e-term-automatic`), in three arms: the deferral (36 s), the orphan (ppid 1, still writing 32 s after the KILL), and the game's save replaced (`out-game`: 6,291,456 bytes where the game wrote 10; none kept).
- **F-14:** KILL2 on the guest, the real script, two arms (`guest-cycle/cells-3/KILL2a`, `KILL2b`: `Server Side Moves: 3` before the transfers). The bare donor rclone on the host (`host-leads/f14-backup-dir-order`): all three moved aside within 1.5 s, before 220 KiB of the first copy.
- **F-15:** the refusal through each twin (`host-leads/k15-at-the-run`). Both end on an outcome sentence.
- **F-04 to F-13:** read at their lines; each cell above names them. F-06's probe and F-09's `:764` were also put to the donor's binaries (`host-leads/d-terminal-width`, `a-awk`).

## Renovation face

### Q1 Modernize

- **F-11, the copy-twin as a design.**
  - 34 of the 39 shared functions are byte-identical (`tools/t16-functions.py`); the 5 that differ do so in a handful of lines.
  - `conf_valid`, the gate that decides what root sources, is in three files.
  - One library sourced by the twins and the helper (`/usr/lib/cloud_sync/common.sh`, say) would make each fix one fix. #307's audits fixed the gate three times, each time in each copy.
  - **A proposal for the coordinator, no edit here.**
- **The three stamp families:** a design sentence.
  - The twins own `last-<run>` and the upload marker;
  - the capture and `cloud_saves_root` own the manifest, its stage and the card;
  - EmulationStation owns `last-sync-<origin>`.

  No file says so. Q7 asks for that sentence.
- **`102-cloud-saves`' detached `--full`:** off the boot's critical path by design (D-CLOUD-057, D-CLOUD-064). Its cost is F-12's at power-off, not at boot.

### Q2 Standards and best practices

- **The oracle verdict.**
  - T13's 79 rows: 25 both ends (`CONTRACT` among them; T13's `04` `:228` names the 24 of the 78: steps 2, 5, 8, 17, 18, 19, 22, 23, 27, 32; A1, A2, A8, A9, A11, A14, RETENTION; LINK2, LINK3, LINK5, LINK6; KILL1, KILL4 (conditional), KILL5), 46 synthetic and 8 device report. No delta.
  - **56 rows run one of the nine scripts**, 8 of them through a harness helper; 15 run only T17's.
  - **This slice trusts, at `3a653eaec4`, the both-ends verdicts of the rows that run its scripts:** steps 2 and 5, A2, A8, A11, A14, LINK2, LINK5, LINK6, KILL1, KILL4 (conditional), KILL5 and `CONTRACT`. Steps 22 and 23 also run `cloud_backup` by name, and A1 and A9 run it through a helper.
  - It does not take a synthetic row as evidence about an input, nor a device-report row as evidence about the code.
  - A5 and RETENTION SKIP (#1057).
  - **The gap the read finds is in the stop:** KILL2, the one cell that stops a run as EmulationStation does, runs the deliberate flags. The automatic run, which is what ES stops at a launch, is not in any KILL row (F-03).
  - **Two of the window's FAILs are the harness's words, not the code's:**
    - KILL15 holds a helper to a run's outcome line (F-15).
    - KILL2b's "nothing removes it (litter forever)" is contradicted by the re-run's sweep, and the cell's own last check reads the tree clean.
    - KILL2's absent saves are the code's (F-14).
    - KILL2's header still names D-CLOUD-076, which D-CLOUD-109/130 superseded.
- **The twins' discipline:**
  - `set -o pipefail` appears once in the capture (`seal`'s hash, `:1081`) and nowhere in the twins. Their pipelines that reach a decision are `md5sum | md5sum` (`cloud_backup:2114`, failing toward a send) and `lsf | grep` (`:1566`, failing toward removing nothing). Both fail safe.
  - `set -u` is in none of the nine.
  - The unquoted expansions are F-13's.
- **The conf against its defaults:** 16 and 16, nothing on one side only (run r12).
  - The allowlist's 54 rule lines are the same in the file and its `.defaults`; the 23 differing lines are comments (run r13).
  - The two conf readers disagree on values the gate passes (F-02).
- **F-04, the why sentences:**
  - The scripts and `es-player-text.md`'s rc list disagree on 3/4 (`COULDN'T FIND YOUR CLOUD FOLDER` against `YOUR CLOUD FOLDER WASN'T FOUND`) and 7/8 (`YOUR CLOUD WOULDN'T TAKE THE FILES` against `YOUR CLOUD REFUSED THE TRANSFER`; the D-UI-031 table agrees with the scripts).
  - `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` and `COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN` are in no table.
  - The rule's half is #909's. Whether `ThreadedCloudSync`'s fallback map moved with the scripts is the ES slice's.
- **Busybox:** the scripts run under the image's busybox.
  - `cloud_sync_cleanup_duplicates.sh` calls `gensub`, which `cloud_restore`'s `near_names` comment says busybox awk lacks.
  - **The comment is wrong** (`host-leads/a-awk`). The donor's `/usr/bin/awk` is busybox 1.36.1's, `gensub` works with back-references, and the cleanup runs whole under it and leaves a conf that parses.
  - A48 ran the same awk (`tools/last-good-scripts-test:8983`). F-09 carries the comment.

### Q3 Bugs

**Which design the tree implements:** D-CLOUD-109/130. The scripts have
no path that cancels on a launch. The automatic run carries a deadline
from its start (`load_config`, `cloud_backup:1403`), and the `rclone()`
wrapper starts nothing past it (`:366-369`). The superseded D-CLOUD-076 is
not filed against.

**Bug decisions.** Each bug is filed at stage D with these three lines, a
defect in a twin as one bug naming both files:

- **F-01, a bug.**
  - *Trace:* `load_config` at `cloud_backup:1209-1222` and `cloud_restore:1258-1271`. `conf_valid` refuses; `cp -f .bak .tmp.$$ && mv -f .tmp.$$ conf`, neither status read; then `if ! source "${conf}"`, which runs whatever the file holds. A failed `cp` (no space) leaves the refused file in place and a partial `.tmp.$$` beside it. `bash -n` passed the file or `conf_valid` would have said so first, so `source` succeeds and the run goes on.
  - *Already written:* nothing on a device or in a cloud is written by the defect, which is a read. A fixed reader inherits a refused conf and perhaps a `cloud_sync.conf.tmp.<pid>` left by a failed copy. The fix refuses (`YOUR CLOUD SYNC SETTINGS COULDN'T BE READ`) when the put-back does not leave a file `conf_valid` passes, and removes its own temp.
  - *VM line:* `fixtures/load-config-fallback.sh` against the twins is the host proof. On the VM a full `/storage` is planted with `fallocate` on the disposable guest and the run's sourcing observed; that is stage E's, not this window's.
- **F-02, a bug (Low; re-graded on the host).**
  - *Trace:* `conf_valid` passes `SAVESPATH=""` (fixture). `cloud_restore:1758` tests `[ ! -d "" ]` (true) and runs `mkdir -p ""`, which fails; its message, `mkdir: can't create directory ''`, reaches the output. `:1902-1906` asks rclone to copy into `"${SAVESPATH}/"`, which is `/`. rclone 1.75.2 refuses as a fatal error because `--backup-dir` (under `/storage/.cache`) lies inside `/`. That gives exit 7, which `report_rclone_error` words as the cloud's refusal. `cloud_backup:1613` refuses the same conf with `YOUR SAVES FOLDER ISN'T ON THIS DEVICE`; the restore has no such test. `cloud_saves_root:46-51` and `cloud_capture:193-198` read the default `/storage/roms` for the same file.
  - *Already written:* any conf a device holds with such a value (none ships, and the helper never writes one). The restore wrote nothing anywhere (`host-leads/b-empty-savespath`: no file restored, in either mode of `/`), and the stamp it leaves is `7 YOUR_CLOUD_WOULDN'T_TAKE_THE_FILES`. The next good run replaces it. A fix reads the same conf and refuses with the backup's sentence.
  - *VM line:* `host-leads/b-empty-savespath` is the proof, on the image's busybox and rclone; the guest adds nothing to it. The fix's walk repeats it on the image (stage E).
- **F-03, a bug, High if the ES slice shows ES signals the script alone (window: the image's bash and coreutils).**
  - *Trace:* `cloud_backup:372` and `cloud_restore:359` run the automatic call as `command timeout -k 3 "${left}" rclone ...` in the foreground. The `INT TERM` trap (`cloud_restore:2318`, `cloud_backup:2504`) runs only when it returns (`fixtures/trap-defer.sh`). On the host, a TERM at +5 s ran the trap at +41 s, and the run is stamped `130` over a save that landed. A KILL to the script leaves `timeout` and `rclone` running with ppid 1, unlocked (fd 9 is closed in the body), to the 90 s deadline. Their final rename lands on whatever the name holds by then: a save the game wrote at +11 s was replaced by the cloud's copy (`out-game`).
  - *Already written:* a KILLed run writes no stamp, so `last-*` keeps the previous run's. An orphaned restore may already have replaced a save that a game wrote after a stop on a device; nothing records that, and the copy is gone (it was never under `--backup-dir`: the move aside happens at check time). A fix inherits nothing it can read; it stops the transfer with the script (the deliberate path's backgrounded child and `wait`).
  - *VM line:* `host-leads/e-term-automatic` on the host. The same three arms on the guest, with the image's bash 5.3 and coreutils 9.4, are stage E's (`fix-walk-pending-image`).
- **F-14, a bug (Medium).**
  - *Trace:* `cloud_restore:1869-1871` passes `--backup-dir=/storage/.cache/cloud_sync/replaced/<stamp>`. rclone moves each destination file it will replace into it at check time, and only then queues the copy (`f14-backup-dir-order`: three `Moved (server-side)` before 220 KiB of the first copy). A stop between the two leaves the save absent from `SAVESPATH`. The copy kept under `replaced/` is pruned by the next completed run (`prune_replaced_local`, `:1607-1621`), which has fetched the cloud's copy by then. A SIGKILL also leaves `<name>.<8>.partial`, which the next restore sweeps (`:1898-1913`); `+ /savestates/**` admits it to any backup that runs first.
  - *Already written:* a device whose restore was stopped holds the replaced saves under `replaced/<stamp>/`, and perhaps a `.partial`. A cloud may hold a `.partial` that a later backup sent. A fix reads both: the next restore puts a missing save back from the cloud (it does today), and a fix that sweeps `.partial` from the cloud names its pattern exactly, as `sweep_partials` does.
  - *VM line:* KILL2 on the guest (`guest-cycle/cells-3/KILL2a`, `KILL2b`) and `host-leads/f14-backup-dir-order`. The fix's walk is KILL2 with the absent-save check passing.
- **F-07, F-08, F-12, F-13:** Low. Each a proposal with its trace in `05`; none is filed as a `bug` unless the window shows an effect on a player's data.
- **F-15:** a proposal for T13's harness (`tools/` is not this lane's): `fx_kill15` asserts the refusal's why and its "nothing was transferred", and leaves the outcome line to a twin's run.

### Q4 Package currency

- **rclone 1.75.2**, a binary zip pinned per arch with its SHA256 (`package.mk`, verified against `SHA256SUMS`, #541).
  - Its author's current release: **CANNOT (no network)**.
  - `tools/fork-package-freshness` is the tool, and is not run (it reads the network).
- **Upstream relation:** nil. ROCKNIX has not changed the directory since the base (run r19).
- **T13's fixes this slice's rows depend on**, all in `tools/` at `3a653eaec4`:
  - #1059 (the restore's empty-cloud exit);
  - #1067 (the SFTP endpoint);
  - KILL1's commit-model expectation;
  - A15's backup landing;
  - CAP13's warning.
- **F-10**, the recipe's `unpack`, is a build-path finding: no player sees it.

### Q5 Efficiency

The exit sync's budget is D-CLOUD-119's 3 s.

- **Measured median:** none. The window did not run `tools/time-to-play --vm`, and no figure is cited here (corrected 2026-10-30; `02` § The guest cycle). Lead (c) is `(window)`-pending, for stage E and the integration window.
- **What runs on that path, by the code:**
  1. `cloud_backup`'s top level;
  2. `take_cloud_lock` (at most 1 s when contended);
  3. `check_network_link` (`ip route`);
  4. `check_rclone_config`;
  5. **`cloud_sync_helper`**: a log trim, a rules merge with one `grep -F` per rule line (54), two `conf_valid` runs (`bash -n` and awk), a pass over the defaults with one `grep` per key, and four `grep`/`sed -i` one-shots;
  6. `load_config` (`conf_valid` again, `source`, about 15 `echo | sed | tr` pipelines on `RCLONEOPTS`);
  7. `first_remote` (`cloud_remote`, python3);
  8. the saves phase:
     - `cloud_saves_root check --wait 15`;
     - `find | head -1`;
     - `remote_compares_by_size` (awk over `rclone.conf`);
     - with `--recent`, no `mkdir` and `--no-traverse`;
     - one rclone;
     - `cloud_saves_root record`;
  9. with the settings phase, **`rclone help`** (F-06) and a `rclone size` per archive.
- **Each step's cost** is lead (c)'s to time on the image (`(window)`-pending). F-05 is graded from that, not from this list.
- **One cost is settled without the guest:** the restore's saves phase and both settings phases start `rclone help` for a flag rclone 1.75.2 does not know. That is 22-24 ms per start on the host, and never any effect (`host-leads/d-terminal-width`).
- **`cloud_net_ready`'s 3 s grace** is counted from its own first observation (`cloud_net_ready:199`), so a startup sync on a link up for hours still waits about 3-4 s before it starts. Whether ES runs it on the launch path is the ES slice's.

### Q6 Dead ends

- **Functions with no caller (F-06):** `cloud_restore`'s `controller_menu` (632-693), `get_controller_devices` (616-628, called only by `controller_menu`) and `device_folder` (1476-1482). 76 lines.
  - `cloud_backup` and `cloud_capture` have none (`tools/t16-functions.py`, `uncalled`).
  - **Removals none here**: each is a proposal on the punch list for the coordinator (D-WORKFLOW-209's last clause).
- **Code that runs and does nothing:**
  - `cloud_backup:2054-2056` (`rclone help` for `--progress-terminal-width`, which `:2170` drops); the restore's settings phase has the same pair at `:2028-2030` and `:2173`; the saves phase's probe at `cloud_restore:1893-1895`. **rclone 1.75.2 has no such flag** (`unknown flag`, rc 2), so all three probes are dead whatever follows them;
  - `logged_moved`'s `LOG_FILE` half at `cloud_backup:1539` and `cloud_restore`'s twin, whose offset is taken after the transfer.
- **Options parsed and never used:** none. Every `--` option of the twins, the capture, `cloud_net_ready` and `cloud_saves_root` reaches a branch.
- **`gamelist.xml:64,76`'s** `./cloud_backup.sh` and `./cloud_restore.sh` tool entries point at symlinks `post-update:81-86` removes and `package.mk` no longer installs: a dead end in the modules package's slice (the coordinator's lead).

### Q7 Clarity and structure

Can a reader tell, from the directory and the rule, which script runs
when, under which lock, writing which stamp, and on which card the saves
are?

- **Which script runs when:** partly.
  - The scripts' headers say: boot (`102-cloud-saves`: the scrub, then the capture's `--full`), a game's exit (ES: the capture, then `cloud_backup --automatic`), an update (`post-update`: the helper), a menu row (ES: the twins).
  - No one file lists the four, and `102-cloud-saves`'s comment on the lock is stale (F-09).
- **The locks:** two (`02` § The stamps and locks).
  - The twins' header explains theirs at length.
  - The capture's header explains its own and says it never takes the other; its boot hook's comment says it takes none.
- **The stamps:** three families, never named as families anywhere. The twins' `last-<name>` is built at run time, so a literal search finds no `last-restore`: it misled the brief (F-09).
- **The card:** `cloud_saves_root` is clear, and every caller states what it does with a refusal.
- **The rule:** `rclone-cloud-sync.md` carries #909's drift. Its `:375` still says `tools/cloud-round-trip` asserts "the exit-4 timing"; the scripts and the harness use 69.

## Instruction File Recommendations

- **`rclone-cloud-sync.md`**:
  - a short table of the three stamp families and the two locks, with their owners (Q7);
  - the sentence that a conf value the gate passes may be read by two readers (`source` and the `sed` extraction) that disagree on comments, quotes and empties (F-02).

  These are proposals for #909's owner; this lane edits no rule.
- **`engineering-practices.md` § Guards must fail closed:** F-01 is that rule's shape in a fallback. A fallback whose copy fails must not fall through to the thing it replaced. It is offered as an example, not a new rule.

## Second opinion (Phase 4.6)

Not run yet. Astra then Argon, a probe and a refutation each, after the
guest window's record is in `02`, over the packet `tools/t16-packet.py`
builds from `02`, `03`, this file and the 14 at `8ebaf8daad`.

## Quality Self-Check

- **Every finding names its lines and its proof.** The three marked (window) say what observation decides them.
- **The host leads ran the image's busybox and rclone**, but the host's bash 5.3.9, GNU coreutils 9.7, grep 3.12, python3 and `ip` (`02` § The host leads). A verdict that could turn on those (F-03's timing) stays `(window)`-pending.
- **Not checked:**
  - how EmulationStation invokes and stops the scripts (named, not read);
  - the capture's lines 1110-1585 line by line (read for writes, removals, `jq` calls and exits);
  - rclone's own currency (no network).
- **The first draft of `02`'s leads carried six line numbers from a comment-free listing**, corrected from the file before its commit. The same check ran over this file's numbers.


## Context: docs/reviews/order.md § T16

### T16. cloud-sync-and-saves: cloud sync: the sync, backup, restore and capture core

- **id**: `cloud-sync-core`; **kind**: read; **lens**: security, brittleness, new functionality
- **why here**: the state model players' saves depend on: the highest brittleness of the product areas (19 blindspot entries, 47 closed bugs, 451 commits since June) and +28,279 lines since the base; its closing evidence runs `tools/cloud-round-trip`, so the brief asks the executor to read the assertions it relies on for invariants rather than current behaviour (blindspot 31), ahead of `cloud-harness`
- **paths** (14 paths, 8,316 lines, 7,827 read, of which 7,827 fork-own; 0 patch and config lines; reach shipped 14): areas `cloud-sync-and-saves`; globs `projects/ROCKNIX/packages/network/rclone/**`, `!projects/ROCKNIX/packages/network/rclone/sources/cloud_{oauth,setup,remote,connections.py,content_backup,content_restore,content_transfer,scan,folder_validate,device_id,log_scrub}`
- **read before**: none
- **depth**: Extended -- the cloud sync and state preservation (plan § 6c)
- **interacting subsystems** (read-only context): the ES cloud cards and transfer page (`es-cloud-pages`); `backuptool` and the setup scripts (`cloud-setup-content`); the game-end hook and autostart (`sysutils/autostart` in `os-system-services`, `rclone/autostart` here); the save layout RetroArch and the standalone emulators write (`emulators-libretro`, `emulators-standalone`); `rclone-cloud-sync.md`'s invariants
- **closing evidence**: audit folder, lint PASS with the renovation face, every behaviour claim proven on the VM (`tools/cloud-round-trip`, `tools/vm-qa`), punch list through Phase 7, `reviewed-at` and `fixed-at` set


## Context: the brief § 4 The questions

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`guest`, `design`); the lens is security, brittleness and new
functionality, so Q3 and Q2 lead and Q6 is small:

- **Q3 Bugs -- the lead question.** For each of the nine scripts, the
  defects the lens finds: a write that is not checked (`cmd; rc=$?` on its
  own line), a pipeline whose status is its last stage's, an unquoted
  expansion that becomes rclone's argument, a probe that cannot report
  absence (blindspot 22), a success recorded from the exit status rather
  than the artifact (blindspot 33), a lock taken without a bound or
  released on a path that is not every path, a stamp written before the
  bytes are confirmed (D-CLOUD-078), a `--delete-excluded` or `sync`
  reachable without the allowlist, a credential that can reach a log or a
  stamp (`_rclone_conf_key:522`; the `>>> why` lines; `cloud_log_scrub` is
  T17's, but what these scripts *print* is theirs), the `--automatic`
  path's bound against D-CLOUD-109/130 and the 3 s budget (D-CLOUD-119),
  the no-network exit (69) and the lock-held exit (75) reaching the card
  with the right words (`es-player-text.md`'s table). **Each defect is a
  `bug` only with its trace and its `Already written:` line** (what the
  script left in `/storage/.cache/cloud_sync/`, the stamps, the conf and
  the cloud on devices that ran it) and its VM line (which cell or which
  fixture proves it); a defect in a copy-twin is one bug naming both files.
- **Q2 Standards.** The twins: `cloud_backup` and `cloud_restore` share
  most of their function list by copy (`diff` the two once, with the
  function list; read the shared body once and every divergence whole);
  `set -o pipefail` and `set -u` where pipelines and expansions reach
  rclone; the `>>> why` sentences against `es-player-text.md`'s table and
  `ThreadedCloudSync`'s fallback map (named, not read); the conf's 16 keys
  against their 16 `DEFAULT_` twins (a key in one and not the other is a
  finding: `upgrade-and-install.md`'s first row); the rules file against
  its `.defaults`; the scripts' busybox-safety (they run under the image's
  busybox: `tools/last-good-scripts-test`'s shims are the host's way,
  D-QA-063's lattice says a host-bash verdict is not device evidence).
- **Q4 Currency.** rclone 1.75.2 as a binary zip (`package.mk`): the
  author's release `CANNOT (no network)`, `tools/fork-package-freshness`
  named; the upstream relation is nil (the directory is the fork's); the
  fixes T13 made in `tools/` that these scripts' rows now depend on
  (#1059's exit 3, #1067's cache, KILL1, A15, CAP13) are named by bug.
- **Q1 Modernize.** The copy-twin as a design (one library sourced by both,
  deferred to the coordinator; no edit); the three stamp families and who
  owns which (a design sentence); `102-cloud-saves`' detached `--full`
  capture at boot against the boot's time to play (named, measured by the
  guest's journal if the window allows).
- **Q5 Efficiency.** The scripts' size by function (the twins' 92 functions
  and how many are identical by copy); what the exit path costs
  (D-CLOUD-119's 3 s: the `--automatic` path's steps and their bounds, read
  from the code and cited from `docs/vm-qa-log.md`'s measured medians, not
  re-measured here unless the window allows one `tools/time-to-play`
  run).
- **Q6 Dead ends.** Code no row and no caller reaches: functions in the 14
  with no caller (`grep -c '<name>' <file>` over the function list; a
  function defined and never called is a row), the `gamelist.xml` tool
  entries (above; the modules package's, named), any `--` option parsed
  and never used. Removals none here: a fork-own dead function is a
  proposal on the punch list, left for the coordinator (D-WORKFLOW-209's
  last clause).
- **Q7 Clarity and structure.** Can a reader tell, from the directory and
  the rule, which script runs when (boot, a game's exit, an update, a
  menu row), under which lock, writing which stamp, and which card the
  saves are on? The three stamp families and the two locks are the test;
  the rule's drift (#909) is cited where it misleads.

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. The seats (Phase 4.6) grade the
findings and the dispositions; each seat's probe comes first.

**The oracle, written into `02` § The oracle.** From T13's § Assertion
shapes, one row per assertion that reads this slice's scripts: the row, the
script and function it exercises, the oracle class, and *what makes it
FAIL* (from T13's § Positives); **the rows that read both ends** (T13's `04` `:228`: steps 2, 5, 8, 17, 18, 19, 22, 23, 27, 32; A1, A2, A8, A9, A11, A14, RETENTION; LINK2, LINK3, LINK5, LINK6; KILL1, KILL4 (conditional), KILL5 -- 24 of 78, with `CONTRACT` the 79th row reading both ends) are the verdicts this slice may trust at `3a653eaec4` and later; the **synthetic** rows (46: CAP1-14 and the other planted inputs) prove the path, not the input; the **device-report** rows (8: `run_steps.3/.4/.6/.12/.21/.25`, `prepare_device.1`, `A5`) certify the code by its own output and are not evidence about it; A5 and RETENTION SKIP today (no `cloud_reconcile`, #1057), whatever their class. The table is generated from T13's `02`
by a script under the audit folder's `tools/` (the generator asserts 79 in,
N out), not typed. This is #1047's fifth criterion, met here.


## Context: .claude/rules/es-player-text.md § Outcome vocabulary (D-UI-028)

## Outcome vocabulary (D-UI-028)

Every cloud surface -- the sync card, the transfer page, the rows under the
toggles -- ends a run with one of **three** words, then a why, what is in
place, and how to recover. Nothing else: no `FAILED`, no `SUCCEEDED`, no log
path, no exit code, no `rclone`. D-UI-028 set four; **D-UI-030 removed the
middle one** -- a run passes or fails, and a run whose parts disagree reads
`COULDN'T FINISH - <why>` with the failing part's why while still saying
truthfully what moved. The stamps keep the `gaps` token so a log can tell a
partial run from a total one; no screen ever shows it.

| Word | When | Card (line 2) | Page (line 1) | Row token |
|---|---|---|---|---|
| `COMPLETED` | every part of the run succeeded (rclone 9 counts as success) | `COMPLETED` | `COMPLETED` | `COMPLETED` |
| `COULDN'T FINISH - <why>` | nothing succeeded and it is not a sentinel | `COULDN'T FINISH - YOUR CLOUD STOPPED ANSWERING` | `COULDN'T FINISH` | `COULDN'T FINISH, YOUR CLOUD STOPPED ANSWERING` |
| `SKIPPED - <reason>` | only 69, 75, the launch cancel, and a player's own cancel of a run they started on a fourth-tier page (D-UI-129, 2026-10-27: the scrape page's `SKIPPED - YOU CANCELLED IT`) | `SKIPPED - YOU'RE NOT ONLINE` / `SKIPPED - A SYNC IS ALREADY RUNNING` / `SKIPPED - YOU STARTED A GAME` | same | `SKIPPED, NO NETWORK` / `SKIPPED, ANOTHER SYNC WAS RUNNING` / `SKIPPED, A GAME WAS STARTED` |

The offline achievements' two cards (#292, #293; D-RA-030, D-UI-095) end in
the same three words: the send card `COMPLETED` with OFFLINE ACHIEVEMENTS HAVE
BEEN SENT until D-UI-107 reworded it to WHAT YOU EARNED OFFLINE IS NOW ON
YOUR ACCOUNT. under the title RETROACHIEVEMENTS) or `COULDN'T FINISH - IT
STOPPED ANSWERING` with IT'LL TRY AGAIN WHEN YOU'RE CONNECTED.; the top-up
card `COMPLETED` with N MORE GAMES ARE READY. or EVERYTHING'S UP TO DATE., or
`COULDN'T FINISH - <the ctl's why>` with IT'LL TRY AGAIN NEXT TIME YOU'RE
CONNECTED. Their running lines: RETROACHIEVEMENTS / SENDING N EARNED
OFFLINE..., and RETROACHIEVEMENTS (OFFLINE) / GETTING GAME N OF M READY...
Their stamp is `last-sync-link`, in the
same shape. And a capture that could not record after a game says, once,
as a toast after the sync card (D-UI-093): COULDN'T RECORD THIS SESSION'S
SAVES. THEY'RE STILL ON THIS DEVICE. -- what did not happen and what is in
place, no log path (#293 item 3; the maintainer would rather a proposed
sentence ship in the cut than wait, `player-language.md`).

**Why** comes from a `>>> why <sentence>` line the scripts print at the point
of failure (rclone's own taxonomy stays in the log), else from rc: rclone 3/4
`YOUR CLOUD FOLDER WASN'T FOUND`; 5 `YOUR CLOUD STOPPED ANSWERING`; 7/8 `YOUR
CLOUD REFUSED THE TRANSFER`; the sign-in check `COULDN'T REACH YOUR CLOUD. YOU
MAY NEED TO SIGN IN AGAIN`; the saves-root guard `YOUR SAVES ARE ON A
DIFFERENT CARD`; a 130 that was not a launch cancel `IT WAS STOPPED`; anything
else `SOMETHING WENT WRONG`. The six rc-keyed sentences are duplicated
verbatim in `ThreadedCloudSync`'s own fallback map, so they change on both
sides or on neither -- the plain-language pass (#108) deliberately left them
alone for that reason.

The scripts also print, where the table has no entry: `YOUR CLOUD STORAGE
ISN'T SET UP YET`, `YOUR SAVES FOLDER ISN'T ON THIS DEVICE`, `THIS DEVICE'S
SETTINGS BACKUP IS DAMAGED`, `THE COPY IN YOUR CLOUD ISN'T COMPLETE`, `YOUR
CLOUD SYNC SETTINGS COULDN'T BE READ`, `AN OLD FOLDER SETTING IS IN THE WAY`,
`COULDN'T TELL WHICH CARD YOUR SAVES ARE ON`, `YOUR SAVES CHANGED CARDS
PART-WAY THROUGH`, and `SOME FILES DIDN'T FINISH` for rclone 6 (2026-09-10,
#105 tranche A; reworded into everyday words 2026-09-10, #108); since the
audit's fixes (2026-09-28, #307): `SOMETHING CHANGED SINCE YOU CHECKED` (a match
refused because the cloud no longer matches the preview), `COULDN'T RECORD WHICH
CARD YOUR SAVES ARE ON`, `THE NEW FOLDER ALREADY HAS FILES IN IT` (the layout
migration's refusal), the stamp why `YOU WENT OFFLINE PART-WAY THROUGH` (a run the
network cut after files moved, stamped `69 gaps`), `SOME ACHIEVEMENT IMAGES
COULDN'T BE SAVED` (the scan page adds `TRY THE SCAN AGAIN.`), `CHECK WHAT WOULD
CHANGE FIRST` (`cloud_content_restore`: a match applied without its preview),
`YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED` (historically
`cloud_migrate_layout`: a pointer that could not be written; the migration
flow and its exclusive outcomes are retired by D-CLOUD-175/#508), and `backuptool`'s
`A SIGN-IN WAS FOUND IN THE BACKUP`, `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT
BACK, SO NOTHING WAS CHANGED. RESTORE SETTINGS FROM THE CLOUD AGAIN, OR BACK UP
SETTINGS TO REPLACE IT.` (proposed, D-UI-117), `THERE'S NOTHING TO BACK UP YET`, `A SETTINGS
BACKUP OR RESTORE IS ALREADY RUNNING`, `YOUR OWN BACKUP LIST NAMES A FOLDER A BACKUP
CAN'T CARRY`, `THIS DEVICE CAN'T RESTORE SETTINGS. SOMETHING IT NEEDS IS MISSING FROM
THIS BUILD.` -- proposed by the fix streams, built with the proposed words, and put
to the maintainer (D-UI-112); `backuptool`
prints its own on the console flows (`THERE'S NO SETTINGS BACKUP ON THIS
DEVICE YET`, `THIS DEVICE'S SETTINGS BACKUP IS DAMAGED`, `COULDN'T KEEP A COPY
OF YOUR CURRENT SETTINGS`, `THE RESTORE COULDN'T FINISH`, ...). **The stamp's
third field** is the why
sentence as one token, spaces as underscores
(`1789000000 5 YOUR_CLOUD_STOPPED_ANSWERING`), present only when the run did
not complete and was not a sentinel; a reader turns the underscores back into
spaces.

**In place**, one per verb, true because rclone renames on completion and the
content scripts never delete outside a match: back up `WHAT MADE IT IS IN
YOUR CLOUD. THE REST IS STILL HERE.` / `DON'T WORRY, NOTHING CHANGED.`; restore
`WHAT MADE IT IS ON THIS DEVICE. NOTHING ELSE CHANGED.` / `DON'T WORRY, NOTHING
CHANGED.`; saves sync `THE SAVES THAT MADE IT ARE ON BOTH SIDES. NOTHING ELSE
CHANGED.` / `DON'T WORRY, NOTHING CHANGED.` (the shipped strings,
`ThreadedCloudSync.cpp:135-137`, since the plain-language pass #108; this
paragraph carried the pre-#108 wording until 2026-09-28, when stream E1 found
the drift while reusing the sync clause for a run the network cut part-way); match `N FILES WERE REMOVED FROM THIS DEVICE.` / `NOTHING WAS REMOVED FROM THIS DEVICE.` -- the
count only: a match removes what the cloud does *not* have (D-CLOUD-023), so
the old second sentence, YOUR CLOUD STILL HAS THEM, said the opposite of the
truth (#308, E2's third pass, 2026-09-28)

**Recover**: the page offers `TRY AGAIN` (the confirm button, south) beside `CLOSE` (the back button, east; buttons by position, never by letter -- `es-ui-style-guide.md` § Interaction rules) on the page's help bar when
the run did not complete, re-running the same command -- except a match, whose
apply used up its preview's plan (PL-001, D-CLOUD-141): the same command again
is always refused, so the page offers no TRY AGAIN for a match and line 7 points
at the row that checks again, `TRY AGAIN: MATCH THIS DEVICE TO THE CLOUD`; the card's action line
names the row (`TRY AGAIN: GAME SETTINGS > BACK UP SAVES TO THE CLOUD`), or for
an automatic sync when it runs again (`IT RUNS AGAIN WHEN YOU EXIT A GAME`);
no network `TRY AGAIN WHEN YOU'RE ONLINE.`; lock held `WAIT FOR IT TO FINISH,
THEN TRY AGAIN.`; a game started `YOUR SAVES ARE SENT WHEN YOU EXIT THE GAME.`
Measure every string at 640x480 in frames; if the card's action line clips,
drop the in-place clause first.


## Context: docs/decision-register.md: the rows the brief's §§ 1-4 name (D-CLOUD-075, D-CLOUD-076, D-CLOUD-078, D-CLOUD-109, D-CLOUD-112, D-CLOUD-113, D-CLOUD-118, D-CLOUD-119, D-CLOUD-130, D-CLOUD-158, D-CLOUD-178, D-QA-012, D-QA-015, D-QA-058, D-QA-063, D-UI-095, D-WORKFLOW-183, D-WORKFLOW-187, D-WORKFLOW-189, D-WORKFLOW-190, D-WORKFLOW-195, D-WORKFLOW-209)

| D-QA-012 | 2026-09-08 | **Every out-of-band maintainer request is filed as a fork issue in the same session, quoting their words.** Maintainer: *"we should create issues to cover them ... so we have the right paper trail of what we've been doing."* Small items raised together may share one issue with a section each (#85); a concern that becomes a requirement on existing work is recorded where it lands and also made findable as an issue. Rule in `issue-tracking.md`. | #85, #86 |
| D-CLOUD-075 | 2026-09-09 | **A cloud operation must end within a known bound when the network goes away, and say why it ended; connectivity loss is a designed-for eventuality, tested by fault injection on the VM before anything else ships to the handhelds.** Maintainer, after the RG SP incident (#102): *"We want to make sure we're dealing with connectivity drops as a potential eventuality, so it's good to get that testing underway so we can harden the experience. Given these are portable devices, there's a good chance that users will experience network drops."* Order set by the maintainer: settings restore, then #103 (link-loss matrix, bounded rclone runs, post-failure probe to the 69 sentinel, startup sync on a settled connection, interface-thread audit), then #104 (persistent journal and logs, watchdog, crash store). Every rclone run the scripts make carries explicit connect/idle timeouts and retry limits; a run that fails while the remote is unreachable exits 69 so the card and the page say `SKIPPED - NO NETWORK CONNECTION`; the interface thread never waits on the network. | #103, #104, #101, #102 |
| D-CLOUD-076 | 2026-09-09 | **A game launch cancels an automatic saves sync (origin startup or exit) in any phase; only a sync the player started by hand is refused (refines D-CLOUD-072).** The kill completes before the game starts -- SIGTERM to the process group, wait for the run to end with a two-second budget, SIGKILL at 1.5 s -- because rclone renames a temporary file into place at the end of each copy and a rename landing on a save the game has just written would lose it. The card ends `SKIPPED - A GAME WAS STARTED`, the stamp records the stop. Accepted: a cancelled startup sync leaves the player on the local save, and the exit sync then pushes it, which can overwrite a newer save another device put in the cloud -- the same exposure as any boot without network; the reconciler (#22) is the protection, not this gate. Maintainer: *"90 seconds is a really long time to wait before you can launch a game. The alternative you propose seems more user-friendly."* Recommended and taken the same evening. | #101, #103; ES `feature/link-loss` |
| D-CLOUD-078 | 2026-09-10 | **Always keep a record of the last known good state. A failure reverts to it; a success becomes it, and the previous record is then removed (refines D-CLOUD-077).** Maintainer: *"we should always keep a record of the last known good state, which hopefully is a fairly straightforward but powerful rule. That way, if something fails, it should always revert to the last known good state. This also means we should always know when something is successful, and therefore the successful state becomes the last known good state, and we can remove the previous one."* Three obligations follow for every writer: (1) it must *know* when it succeeded -- a positive check of the artifact, never the absence of an error (engineering-practices § guards fail closed); (2) the new state replaces the old only after that check -- temp-and-rename, a marker written after the bytes are confirmed, a copy kept until the replacement is verified; (3) the superseded record is removed once, after the new one is good, so there is exactly one last-known-good at rest. Where it already holds: rclone's per-file rename, the settings-upload marker, `backuptool`'s rotation, the capture stage (content-addressed copies of every save the manifest claims), the device id's `.previous`, the `last-*` stamps. Where it does not yet: `system.cfg` and `es_settings.cfg` are rewritten in place and `chksysconfig` overwrites its `.backup` every boot with whatever is there -- so the RG SP's truncated file replaced its own good copy and defaults won (#102); a saves restore that overwrites a newer local copy keeps no previous version (`--backup-dir` would). Work: #105 (messages and retries), #104 (config files kept last-good and restored from it at boot instead of defaults), #22 (the reconciler's kept losers are this rule for saves). | #105, #104, #22, #102 |
| D-QA-015 | 2026-09-11 | **Every action that uses a handheld or the owner's cloud -- a game launch, pad input, a screenshot, a write under `/storage/roms`, a sync, an upload, a deletion in the cloud -- is asked for by name before it runs, with what it does on screen, what it writes, what it sends and what it leaves behind; a general offer of device testing is not a standing yes.** Extends D-QA-008/011 (reboot, staging) after the session ran the exit test and a Dropbox replacement proof on the RG35XX SP unannounced and the owner met the uploaded files in Dropbox first. Reads need no question. | maintainer, #130 |
| D-CLOUD-109 | 2026-09-12 | **A sync the player can see is a sync that happens: a launch never cancels an automatic sync, it waits for it. What makes the wait acceptable is that the sync bounds itself -- a total budget of a few seconds set from measurement (#135) -- and past that budget it ends with a connectivity outcome the player can act on ("Couldn't finish: your connection looks slow or down. Check your internet connection and speed."), the publish waits for the next pass, and the game starts. A sync never takes minutes; its network bounds are time-based, not retry-count based (which answers #113), and the checks that decide connectivity run first.** Supersedes D-CLOUD-076's cancel-on-launch for automatic syncs; refines D-CLOUD-038/072. Maintainer: "canceling the sync at launch is not what the user would expect. If they think a sync is happening, they think a sync is happening ... if we're seeing it take longer than X number of seconds, we assume bad connectivity and then say, 'There was a connectivity error. Check your internet connection and speed' ... the sync should never take minutes." | #134, #22, #135, #113 |
| D-CLOUD-112 | 2026-09-12 | **The offline benchmark: with sync-on-exit left on, a console with no connectivity -- no route, a route with a dead uplink, a captive portal -- reaches its connectivity outcome in about the time a successful sync of the same change would have taken; the connect timeout and the reachability probe are sized to that, and #135 measures the offline exit beside the online one.** Refines D-CLOUD-109/111. Maintainer: "a player like me will leave sync on exit on all the time, wanting to sync whenever available. If I hop into a subway or on a plane, I'm not going to turn that setting off every time, so I would expect it to time out in roughly the same amount of time it would have taken to sync, that's our benchmark." | #135, #134, #22 |
| D-CLOUD-113 | 2026-09-12 | **Two transfer contracts. A deliberate back up or restore is a single action the player started and expects to take time: it runs on the transfer page with its bar and outcome, may be long, and refuses a launch while it runs. An automatic sync -- on exit, at startup -- is expected to be quick: it runs on the card, is bounded by D-CLOUD-111/112, and a launch waits for it (D-CLOUD-109).** The two never share a budget or a surface. Maintainer: "it's also important to differentiate between what's happening when you say 'backup and restore' (where you're deliberately doing a single action that you expect to take time) and the sync on exit, which is something you expect to happen relatively quickly. We should check, but I think even Steam doesn't let you launch a new game until the syncs are backed up to the cloud." Steam's behaviour (sync on exit; that game not launchable until the sync ends; a dialog on conflict) is the precedent to confirm, not a source. Extends D-UI-022's tiers and D-CLOUD-076's manual/automatic split. | #134, #22, #135 |
| D-CLOUD-130 | 2026-09-16 | **Every sync or transfer a game launch would interrupt asks the same question -- STOP IT AND PLAY / KEEP WAITING -- the automatic startup and after-a-game syncs included; nothing is cancelled until the player answers.** Maintainer, having met the exit sync's stop: *"The case I ran into hasn't been changed, correct? When I ran into it, it was an auto-save on exit, and it didn't present me with an option. If we want consistent behavior on how user-started syncs or transfers deal with a potential interruption by a game launch, we should have a consistent behavior."* Reverses the silent cancel of #101 / D-CLOUD-109 for launches; refines D-CLOUD-129. | #203, ES `e21841060` |
| D-CLOUD-118 | 2026-09-12 | **The automatic sync's bounds start at: connect 5 s; a stalled transfer given up after 5 s with no bytes moving; an absolute ceiling of 20 s per script run** (D-CLOUD-111's shape, numbers from #135's measurement: online success 0.8-1.4 s, no route 0.5 s, portal 0.9 s, a refused port 12 s and a stalled endpoint 321 s today). Applies to the startup and exit syncs only; the deliberate back up / restore page keeps its own bound (D-CLOUD-113). Maintainer: "your limit sounds good. Let's start there and then we'll tweak it as we get feedback." The low-level retry count stays 10 for the cloud's own transient errors (#107); the ceiling, not the retries, bounds a stall -- measured before this lands. | #135, #134 |
| D-CLOUD-119 | 2026-09-12 | **Starting budgets: the exit sync of one changed battery save on a hashed cloud within 3 s (P-13; measured 0.8 s); an offline outcome within three times the online success, about 5 s (D-CLOUD-112; four of six offline shapes already meet it, the other two by D-CLOUD-118).** Same words from the maintainer as D-CLOUD-118; recorded as starting points to tweak on feedback. A run over budget fails the runner once the cell reports against these rows. | #135 |
| D-UI-095 | 2026-09-26 | **Any automatic activity in the saves or achievements lanes that moves data over the network, or changes what the player will find earned or saved, is shown while it runs, and a launch over it asks the same question a sync gets; bookkeeping that only reads the device stays silent, and its failure is said once.** Maintainer: *"if there's activity happening in the background around RetroAchievements or save management, etc., we want to make sure we're showing the user what's going on. We want to enact the right gates to keep the user from proceeding without knowing what's going on"*; and *"if RetroAchievements were being sent and the user immediately tried to launch a game, we probably would want to show the same modal we show for save."* The inventory (#293): the startup and exit syncs and the transfer pages already have both; the proxy's send and the two top-ups have neither (D-RA-010's "nothing on screen" is superseded); the captures and the proxy's hourly re-read stay silent as bookkeeping, a failed capture to be said. The proxy's send is not ours to stop, so its question is wait or go; a top-up is stoppable, so its question is stop or wait. | #293, #292 |
| D-CLOUD-158 | 2026-09-30 | **The default cloud folder is `/Rasteratops` (`/Rasteratops/Saves`, `/Rasteratops/Backups`, `/Rasteratops/Content`), and every lookup, offer and default reads it. Reverses D-WORKFLOW-101's "unchanged in 0.0.1"; that row's gate stands: the mixed-installation test runs on `tools/vm-pair` before the default ships. A device whose configured folder is the fork's earlier `/ROCKNIX` is read from there and offered the move (copy, verify, then delete; leave-it-alone the default -- `upgrade-and-install.md` § Migrating data that lives in someone's cloud); a device carrying upstream's shipped `/GAMES`, a value no player typed, is re-pointed at the first cloud check without a question. The rules and register rows that name `/ROCKNIX` as the cloud root are swept with the code (#353's checkbox).** Maintainer, 2026-09-30: *"We should definitely make sure everything is mapped to look for the slash Rasteratops directory instead. And I know we've mentioned the guards, so we'll need to make sure those are in place too, so we don't wind up with very confused users."* | #353, #354; reverses D-WORKFLOW-101; D-CLOUD-018, D-CLOUD-050 |
| D-QA-058 | 2026-10-06 | **Routine cloud qualification uses the candidate image's rclone/cloud scripts against local WebDAV, SFTP and MinIO/S3; Dropbox credentials, an offsite endpoint or any hosted-provider account are not RC prerequisites now or going forward.** Maintainer: "The Dropbox credential check isn't something we need to do now" and "That's for now and moving forward." Refines D-QA-017 and reaffirms D-QA-041: broader local SMB/FTP coverage remains separate; optional authenticated provider observations remain explicitly unverified rather than counted as local-matrix passes. The dedicated RetroAchievements award/reconnect proof is separate and unchanged. Sweep: VM/cloud/release rules, release readiness, M7 and #351/#361/#383/#409/#344/#354; the Dropbox observation moves to milestone-less #463. | #462, #463, #133 |
| D-CLOUD-178 | 2026-10-07 | **Use a category validator for cloud setup, reusing existing backup/restore readers and interface building blocks. Validation itself is read-only; fixes are separate, explicit actions for game saves, save states and screenshots, with their exact plan, collision handling and verification defined before implementation. ROMs and BIOS get expected paths and manual setup instructions, never automatic library relocation.** Distinguish missing, empty, recognized misplaced and unreadable content within selected roots; folder readiness does not prove complete transfer integrity or BIOS compatibility. Preserve configured choices and do not infer cloud-wide absence. Once relevant wiki guides are published, `See instructions` opens a QR modal for the ROM or BIOS guide; no clickable-link or handheld-browser expectation. Until then, local guidance remains useful and no dead QR destination ships. Refines D-CLOUD-175/176/177; #510's direction is chosen, while #508 still needs contract reconciliation, implementation and qualification. | #510; #508; #511; maintainer's validator, reuse and QR guidance on 2026-10-07; `docs/pixelelated/cloud-folder-flow-review.md` |
| D-WORKFLOW-183 | 2026-10-22 | **The renovation program runs as one coordinator lane and one session per worktree: `feature/m6-renovation-plan-346` coordinates (plans, writes briefs, accepts at gates, integrates), each executing phase or slice is one worktree with one session, a second session never shares a checkout, fan-out inside a lane is read-only research subagents, and there is no long-lived M6 integration branch, `next` being the roll-up.** Put to the maintainer as the shape M7 already uses, against two alternatives: a second tab inside the P1 worktree (the one-index-per-checkout failure of 2026-09-14, `worktrees.md` § One builder per build worktree) and a general `m6-code-assessment` branch everything rolls up to (stranded finished work, `fork-workflow.md`; remediation must reach `next` to be built and VM-tested; a second integration branch doubles the ledger conflicts). Maintainer, 2026-10-22: *"this works for me."* The coordinator runs on Fable; the work lanes run on Opus 5.5 (D-WORKFLOW-056, D-WORKFLOW-181). | #346; #641; D-WORKFLOW-182; D-WORKFLOW-056; D-WORKFLOW-181; `docs/reviews/plan-for-the-plan.md` § 8 |
| D-WORKFLOW-187 | 2026-10-23 | **The renovation gates no release. M6 is an audit, assessment and renovation of the codebase: it decides what is read, in what order and at what depth, never what ships or when. D-WORKFLOW-102's release clause is retired (`0.1` waiting on Tier 1's findings on the launch, control and state slice and on any known security, state-preservation or launch-path finding from any tier); its placed, progressive review stands. A finding that is a defect is filed as a bug the session it is found (D-WORKFLOW-132) and holds or clears a release the way every bug does (D-QA-051, `tools/rc-preflight`), owned by the release's milestone, never by a slice. The order carries no release-gate column; T1 and T2 keep their place on the order's own lenses, and the one prerequisite that stands is a reading order, not a gate: the launch-path slices are read before #336 Step 1 replaces what they read. The drift re-review runs at the renovation's own cadence (every slice close), not as a release step. D-WORKFLOW-186's "within D-WORKFLOW-102's gates" reads accordingly. P1's pass-7 question 2 (whether `backuptool`, T17, and the system services, T22, also gate `0.1`) is withdrawn as outside the program, not answered.** Maintainer, 2026-10-23, when the coordinator put question 2: *"Our codebase check shouldn't have anything to do with what we're actually shipping. This is meant to be an audit, assessment, and renovation, and not concerned with features proactively shipping. Now, why would your question 2 be part of what we're trying to accomplish here?"* Sweep in the same change: plan § 5 and § 6a, § 8's drift trigger, the M6 body's acceptance and dependencies, #339's gate checkbox; `order.md` § 1, the Gate column and T1's release-gate line are P1's (#641). | #346; #641; #339; D-WORKFLOW-102; D-WORKFLOW-186; D-WORKFLOW-132; D-QA-051; `docs/reviews/plan-for-the-plan.md` § 5, § 6a, § 8 |
| D-WORKFLOW-189 | 2026-10-23 | **Planning stays in the coordinator lane: the division of work, the meta work, the definition of work items (the slice issues and their acceptance criteria, the area epics, the briefs) and every change to the roadmap (the M6 body, the order's sequence, the plan) are the coordinator's, on Fable; every other lane executes its brief and does no planning or strategy. So the 46 slice issues and their criteria are the coordinator's to write and file, not P1's: the third output of the P1 brief leaves P1's scope, P1 hands back the inventory and the order, and the coordinator files the issues from `slices.json` through `tools/renovation-inventory --slice-issues`, adding each slice's specific criteria with its brief before dispatch (plan § 7). A lane's question about scope or order still reaches the coordinator (the pass-7 shape), and the coordinator, not the lane, answers or relays it.** Maintainer, 2026-10-23, answering who authors the slice issues: *"Anything related to the division of work, meta work, definition of work items, changes to the roadmap, etc., should be done in this coordinator lane. Any additional lane should be focused on execution, but not on planning, strategy, etc."* Restores D-WORKFLOW-181's letter (Fable writes "the issues and their agent-first criteria") where the lane split of 2026-10-22 had put the slice-issue filing on the Opus P1 lane; refines D-WORKFLOW-183's "coordinates (plans, writes briefs, accepts at gates, integrates)" by naming what a work lane does not do. Sweep in the same change: the P1 brief § 6, § 7, § 8 and § 10; #641's step 6 and criterion 7; the M6 body; plan § 6 (P1, step 6) names the coordinator as the filer. | #346; #641; #339; D-WORKFLOW-181; D-WORKFLOW-183; D-WORKFLOW-187; D-WORKFLOW-056; `docs/reviews/briefs/p1-survey.md`; `docs/reviews/plan-for-the-plan.md` § 6, § 7 |
| D-WORKFLOW-190 | 2026-10-23 | **Slices run beside each other when the plan's condition holds (different areas, no shared path; plan § 6 "P2 onward" and § 8): T2 (#649, the interface's launch path) runs in its own lane beside T1 (#648), not after it, and the same holds for every later pair the order places in different areas. What parallel costs is the coordinator's to carry: one image build at a time on the host (`worktrees.md` § One builder per build worktree), one guest per lane on its own ports and sockets, the shared QA backend and `vm-pair` off-limits to a slice lane, and a remedy applied once on the coordinator branch so every later lane is cut with it in (the Argon route: M7's `fac2129787`, `1c7d283ad5` and `a7a3bdda4e`, cherry-picked as `033eb7ed23`, `0ceb2994c5` and `6874394d49`).** Maintainer, 2026-10-23, asked whether T2 runs beside T1: *"Is there a reason not to have T2 launch in another lane? If there's an advantage to it being in serial, we can do that. Otherwise, we can do it in parallel."* The coordinator's answer, which the call rests on: no structural reason for serial; T1 is the distribution's shell scripts and T2 the EmulationStation sources, meeting at one seam (the argument line `LaunchCommand.h` builds for `runemu.sh`) that each brief names as the other's read-only context; the one serial advantage, T1's execution lessons reaching T2's brief before dispatch, is small because T1's stage-D pause lands before T2's and a brief is amended at the pause. Refines D-WORKFLOW-183 (one session per worktree; the coordinator integrates) and the order's row (the order is a reading order, not a serial constraint between areas). | #346; #648; #649; D-WORKFLOW-183; D-WORKFLOW-187; D-WORKFLOW-189; `docs/reviews/plan-for-the-plan.md` § 6, § 8 |
| D-WORKFLOW-195 | 2026-10-24 | **An Extended seat whose answer the model's output ceiling cuts on the packet is run again on a trimmed packet for that seat -- the same model, effort and provider; the analyses and tables whole, the cited files as line-numbered excerpts with context, the ask bounded -- never a model or effort substitution and never the same packet again.** `04` § Second opinion says the seats saw different evidence; an item one seat saw only in excerpt carries `excerpt`, and a disagreement that could be the excerpt's doing is resolved from the artifact, not from either seat. A fork resolved during execution on T30 (#677): Argon at `high` spent about 57k of its 65.5k output tokens reasoning on a 438 KB packet three times (`finish=length`), where T3's 308 KB packet took 30k. The maintainer may reverse it by a new row. | #677, #798; `adversarial-council.md` § Council model floor; the T30 hold post of 10:04 UTC and the coordinator's answer the same hour |
| D-QA-063 | 2026-10-25 | **Every fork suite shares one exit lattice: 1 when any case failed; else 3 when any case was skipped or was judged by something that is not device evidence (a host-tool run under `--host-diagnostic` or `--unverified-busybox`, a missing busybox); 2 on a usage error or an unknown selector; 0 only when every case ran as evidence and passed. The precedence is 1 over 3 over 0, so a failure is never hidden behind a skip and a skip is never read as a pass.** Generalizes D-QA-061 (`vm-qa`) to the state tests (T14's `--unverified-busybox`, ruled 1 on a failing case on #661) and `last-good-scripts-test`'s `--host-diagnostic` (T15 S1 asked on #662 whether to match T14; it does). The T15 stream brief's `exits 3` was written short and is corrected in the same change; a defect found under the host's applets is still a defect, and a caller reading 3 must be able to trust that nothing failed. | #662, #1018, #661, #940, D-QA-061; `docs/reviews/briefs/t15-streams.md` S1 |
| D-WORKFLOW-209 | 2026-10-25 | **A renovation dead-end table removes nothing and edits no recipe: T23 (and T40, T43 and T25 after it) record a disposition per unit -- dead upstream-carried, shadowed copy with its override live or dead, unshipped, fork-own dead with a proposed removal and its `Already written:` line, or reached after all -- and the removal of upstream-carried dead code is one class decision for the maintainer, put to them on #346 with the table's counts and the cost against the value; a fork-own dead unit's removal is proposed on the punch list and left for the coordinator.** The 1,604 rows are 1,601 upstream-carried: the fork tracks `upstream/next`, a deletion of upstream's file is a modify/delete at every merge (D-WORKFLOW-198's class), and the area futro already held T7 to *deletes nothing upstream carries*. The order's § T23 said *decides the removals*; this row narrows it to *decides the dispositions*. The three IDs before this one are the M7 lane's reservation; this row is the first M6 row after it. | #670, #848, #346; `docs/reviews/briefs/generic-packages-dead-ends.md` § 1 |

## File: autostart/102-cloud-saves (at 8ebaf8daad, 57 lines, whole)

```text
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # Cloud saves at boot.
    6  #
    7  # The startup saves sync (Cloud Settings > SYNC SAVES DURING STARTUP) is
    8  # EmulationStation's now, not this file's: with the toggle on, ES runs the
    9  # same pair the SYNC SAVES WITH THE CLOUD row runs, through the progress card
   10  # the game-exit sync uses, so a player sees it run and how it ended (fork
   11  # #94). Until 2026-09-09 this autostart ran that pair headless -- a ping loop,
   12  # then cloud_restore and cloud_backup with their output discarded -- which
   13  # left no sign on screen that it had run at all, and sat outside the launch
   14  # gate that keeps a game from starting mid-transfer (D-CLOUD-038). A second,
   15  # headless copy here would only race the visible one for the transfer lock
   16  # and report SKIPPED into /dev/null. So this file no longer syncs anything.
   17  #
   18  # What it still does is the full capture pass, below -- and, once per
   19  # device, the cloud log's scrub before it.
   20  
   21  . /etc/profile.d/001-functions
   22  
   23  # Passwords and keys an earlier build wrote into the cloud log and the
   24  # interface's log, masked once per device (the audit of the fix round,
   25  # PL-014). Here, in the foreground, because nothing else writes those logs
   26  # yet: the capture pass below writes the cloud log, and EmulationStation
   27  # starts only after every autostart script has run. After the first boot it
   28  # reads its record and returns.
   29  [ -x /usr/bin/cloud_log_scrub ] && /usr/bin/cloud_log_scrub
   30  
   31  # The full capture pass (fork #21): re-hash every save the manifest already
   32  # claims, so an edit from a shell, a session EmulationStation itself aborted,
   33  # a power loss, or a rewrite that kept the size and mtime of a game nobody
   34  # has played since is caught -- none of those reach the exit-path capture.
   35  # Boot is the one moment no game can have just exited, so it cannot race one.
   36  #
   37  # Only a device that has turned cloud saves on runs it: a device with both
   38  # toggles off has no consumer for the manifest, and boot time is not ours to
   39  # spend (#84, D-CLOUD-057). Detached and niced, so it never delays boot and
   40  # never holds the autostart runner; it needs no network and takes no lock.
   41  #
   42  # Two residuals of running it detached, both accepted (D-CLOUD-064):
   43  # - It can still be finishing when the first game exits, so the two are
   44  #   concurrent writers of one manifest. Capture takes no lock; the loser sees
   45  #   the file change under it and, for an exit capture, re-runs once against
   46  #   the winner's document, so the first version a game wrote is not lost to
   47  #   the race. --full itself never retries.
   48  # - On a two-card device that has never synced there is no saves-root record,
   49  #   so `cloud_saves_root check --wait` returns at once and this pass may hash
   50  #   the internal card's copies before the automount binds the second card;
   51  #   the next exit then records the real file with `replaces` pointing at that
   52  #   stale hash. A flip DURING the pass is discarded; the pre-first-sync window
   53  #   is not, and a device that has never synced has published nothing yet.
   54  if [ "$(get_setting cloudsaves.startup)" = "1" ] || [ "$(get_setting cloudsaves.gameexit)" = "1" ]
   55  then
   56    setsid nohup nice -n 10 /usr/bin/cloud_capture --full >/dev/null 2>&1 &
   57  fi
```

## File: package.mk (at 8ebaf8daad, 111 lines, whole)

```text
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2021-present Xargon (https://github.com/XargonWan)
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  # Copyright (C) 2025 ROCKNIX Team (https://github.com/ROCKNIX)
    5  
    6  PKG_NAME="rclone"
    7  PKG_VERSION="1.75.2"
    8  # Primary project; embedded dependencies retain their own terms (#528).
    9  PKG_LICENSE="MIT"
   10  # Python3 is the interpreter for cloud_remote. A shipped script's tools are
   11  # real dependencies even though nothing links against them: upstream deleted
   12  # packages/compress/zip in a3d0ad0430, nothing referenced it, and backuptool
   13  # lost its archiver silently for months.
   14  # webkitgtk is here because cloud_oauth needs a browser on the device: a
   15  # provider's OAuth redirect goes to localhost, so it only lands somewhere
   16  # useful if the browser is on the same machine as rclone's authorize listener.
   17  # glib-networking is what gives that browser TLS at all.
   18  # jq is cloud_capture's only JSON reader and writer (the save manifest, #21);
   19  # the same policy as Python3 above -- until now it reached the image only
   20  # through virtual/image's own dependency list.
   21  PKG_DEPENDS_TARGET="toolchain fuse rsync qrencode Python3 \
   22                      webkitgtk cloud-signin-window glib-networking jq"
   23  PKG_LONGDESC="rsync for cloud storage"
   24  PKG_TOOLCHAIN="manual"
   25  
   26  # Pinned per arch, and pinned to OUR version.
   27  #
   28  # Upstream added PKG_SHA256 for 1.71.0 in e0a68c95bd while this fork is on
   29  # 1.75.2, so a rebase would bring in a hash that cannot match what we download.
   30  # Setting the right ones here makes that merge a no-op instead of a build
   31  # failure whose message names a checksum and not the version behind it.
   32  #
   33  # Verified against downloads.rclone.org/v1.75.2/SHA256SUMS and independent
   34  # archive hashing (#541). Image assembly strips the binary; installed version
   35  # and protocol proof are recorded separately.
   36  case ${ARCH} in
   37      aarch64)
   38        RCLONE_ARCH="arm64"
   39        PKG_SHA256="7e1e8d69654941b7b7df84ee74c5f7fb09cce7d5496947fb7bf16b55ff427d10"
   40      ;;
   41      *)
   42        RCLONE_ARCH="amd64"
   43        PKG_SHA256="349ac8fba6ff65d6247043f1750cdcb518ec5d500ef91463a10d37c0ccdf3702"
   44      ;;
   45  esac
   46  
   47  PKG_URL="https://downloads.rclone.org/v${PKG_VERSION}/rclone-v${PKG_VERSION}-linux-${RCLONE_ARCH}.zip"
   48  PKG_RCLONE="rclone-v${PKG_VERSION}-linux-${RCLONE_ARCH}/rclone"
   49  
   50  unpack() {
   51    # Create build directory
   52    mkdir -p ${PKG_BUILD}
   53    # Rename the downloaded zip to include architecture for better tracking
   54    mv ${SOURCES}/rclone/rclone-${PKG_VERSION}.zip ${SOURCES}/rclone/rclone-${PKG_VERSION}-${RCLONE_ARCH}.zip
   55    # Extract the binary package to the build directory
   56    unzip ${SOURCES}/rclone/rclone-${PKG_VERSION}-${RCLONE_ARCH}.zip -d ${PKG_BUILD}/
   57    # Remove downloaded zip files to conserve space
   58    rm -f ${SOURCES}/rclone/rclone-${PKG_VERSION}*
   59  }
   60  
   61  makeinstall_target() {
   62    mkdir -p ${INSTALL}/usr/bin/
   63    mkdir -p ${INSTALL}/usr/config/
   64    cp cloud_backup ${INSTALL}/usr/bin/
   65    cp cloud_restore ${INSTALL}/usr/bin/
   66    cp cloud_sync_helper ${INSTALL}/usr/bin/
   67    cp cloud_setup ${INSTALL}/usr/bin/
   68    cp cloud_folder_validate ${INSTALL}/usr/bin/
   69    cp cloud_remote ${INSTALL}/usr/bin/
   70    cp cloud_connections.py ${INSTALL}/usr/bin/
   71    cp cloud_device_id ${INSTALL}/usr/bin/
   72    cp cloud_oauth ${INSTALL}/usr/bin/
   73    cp cloud_content_restore ${INSTALL}/usr/bin/
   74    cp cloud_content_backup ${INSTALL}/usr/bin/
   75    cp cloud_content_transfer ${INSTALL}/usr/bin/
   76    cp cloud_sync_cleanup_duplicates.sh ${INSTALL}/usr/bin/
   77    cp cloud_saves_root ${INSTALL}/usr/bin/
   78    cp cloud_capture ${INSTALL}/usr/bin/
   79    # cloud_log_scrub: once per device, masks the credentials earlier builds
   80    # wrote into cloud_sync.log and the interface's es_log*.txt (the audit of
   81    # the fix round, PL-014); run at boot by autostart/102-cloud-saves.
   82    cp cloud_log_scrub ${INSTALL}/usr/bin/
   83    # cloud_net_ready: what EmulationStation's startup sync asks before it runs
   84    # the restore/backup pair -- is the network up, and has it stayed up (#103).
   85    cp cloud_net_ready ${INSTALL}/usr/bin/
   86    # cloud_scan: the restore flow's scan page runs it first and offers only
   87    # what it found (D-CLOUD-156, fork #350); reads under a parent-held lock.
   88    cp cloud_scan ${INSTALL}/usr/bin/
   89    cp rasteratops-settings-archive ${INSTALL}/usr/bin/
   90    # No game-end event hook. EmulationStation runs the save sync itself now
   91    # (FileData::launchGame), so it can show the result on the progress card
   92    # instead of backgrounding the work into /dev/null where nobody could tell
   93    # whether it had happened. The hook had no caller but ES, and leaving it
   94    # installed would start a second concurrent cloud_backup on the same remote.
   95    cp ${PKG_BUILD}/${PKG_RCLONE} ${INSTALL}/usr/bin/
   96    chmod 0755 ${INSTALL}/usr/bin/*
   97    cp cloud_sync-rules.txt ${INSTALL}/usr/config/
   98    cp cloud_sync.conf ${INSTALL}/usr/config/
   99    cp cloud_sync.conf.defaults ${INSTALL}/usr/config/
  100    cp cloud_sync-rules.txt.defaults ${INSTALL}/usr/config/
  101    chmod 755 ${INSTALL}/usr/bin/rclone
  102    # No TOOLS entries for cloud backup and restore.
  103    #
  104    # These symlinked the scripts into the tools list, so running one dropped
  105    # the player into a fullscreen console. That was the parity stopgap while
  106    # cloud sync had no native surface; EmulationStation now has the whole flow
  107    # -- direction, the three data classes, progress and the last result -- so
  108    # the console route is a second, worse way to do the same thing, and two
  109    # paths to one operation is how somebody ends up with a backup missing what
  110    # they assumed was in it.
  111  }
```

## File: sources/cloud_net_ready (at 8ebaf8daad, 217 lines, whole)

```text
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # cloud_net_ready - wait for a settled network before a cloud sync starts.
    6  #
    7  # Usage: cloud_net_ready [--wait N]
    8  #
    9  #   exit 0    NetworkManager reports the connection up (STATE connected,
   10  #             in any connected state -- its connectivity word is only logged) and it
   11  #             has stayed up for GRACE seconds with a default route the
   12  #             whole time
   13  #   exit 69   no network: there is no default route and nothing is coming
   14  #             up -- at once, without waiting (D-CLOUD-072: a device booted
   15  #             with its radio off never holds the card); or a link that was
   16  #             coming up (NetworkManager `connecting`, or a carrier with no
   17  #             NetworkManager to ask) had no route by the deadline
   18  #             (D-CLOUD-136, #192); or N seconds (default 60) passed without
   19  #             a settled connection. 69 is EXIT_NO_NETWORK, the code the
   20  #             cloud scripts and EmulationStation share for "skipped, no
   21  #             network".
   22  #
   23  # Prints ">>> doing network" once, the moment it starts waiting -- which
   24  # includes the grace, and the wait for a route while a link comes up -- so
   25  # the sync card names its step: CHECKING THE CONNECTION... when the
   26  # interface sees a link, WAITING FOR A NETWORK, UP TO N SECONDS... when it
   27  # does not (#192), and a game launched meanwhile cancels the sync rather
   28  # than being refused (ThreadedCloudSync::cancelIfWaitingForNetwork), which
   29  # is what keeps this wait off the time to play (D-CLOUD-136; maintainer,
   30  # 2026-09-24: "If we can add the reachable wait without adding a delay to
   31  # the time to play, we should do it."). Nothing else on stdout on success;
   32  # one line saying why on a 69.
   33  #
   34  # Why. The startup sync used to begin on the first ping that came back:
   35  # seconds after Wi-Fi associates, which on an SDIO module is the moment it
   36  # is most likely to drop again (#102, #103). NetworkManager's `connected`
   37  # is the whole stack agreeing the link is up; holding it for a few seconds
   38  # is what "settled" means here. And no ping: a probe to a public host fails
   39  # on a LAN-only remote and on networks that block it, and passes while the
   40  # player's provider is down (rclone-cloud-sync.md, reachability). The
   41  # scripts probe the remote itself once they run.
   42  #
   43  # Busybox-compatible: sh, timeout, sleep, cat, grep, ip and nmcli, all on
   44  # the image (nmcli from the networkmanager package). Where nmcli is
   45  # missing or NetworkManager is not answering, the route test plus a carrier
   46  # on some interface stands in, and the log says so.
   47  #
   48  # The bound is N seconds plus at most GRACE: a connection that settles in
   49  # the last seconds of the wait is given its grace rather than dropped.
   50  
   51  WAIT=60
   52  GRACE=3
   53  POLL=1
   54  EXIT_NO_NETWORK=69
   55  LOG_FILE=/var/log/cloud_sync.log
   56  
   57  usage() {
   58      echo "Usage: cloud_net_ready [--wait N]"
   59      echo "  exit 0 when the network has been up for ${GRACE} s; 69 when there is"
   60      echo "  no default route, or after N s (default ${WAIT}) without a settled one."
   61  }
   62  
   63  while [ $# -gt 0 ]; do
   64      case "$1" in
   65          --wait)   shift; WAIT="$1" ;;
   66          --wait=*) WAIT="${1#--wait=}" ;;
   67          -h|--help) usage; exit 0 ;;
   68          *) echo "cloud_net_ready: unknown option $1" >&2; usage >&2; exit 64 ;;
   69      esac
   70      shift
   71  done
   72  case "${WAIT}" in
   73      ''|*[!0-9]*) echo "cloud_net_ready: --wait takes a number of seconds" >&2; exit 64 ;;
   74  esac
   75  
   76  # Braced, so that a log that cannot be written is silent: redirections apply
   77  # left to right, and `>> file 2>/dev/null` reports the failed `>>` on the
   78  # original stderr -- which reaches the card, where any line that is not a
   79  # marker ends the WAITING state and with it a launch's power to cancel.
   80  log() {
   81      { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${2:-INFO}] [cloud_net_ready] $1" >> "${LOG_FILE}"; } 2>/dev/null
   82  }
   83  
   84  # Hundredths of a second since boot, from the kernel: the wall clock jumps
   85  # when NTP or the RTC corrects it, which at boot -- the one time this runs
   86  # -- it does. Hundredths rather than whole seconds so "held for 3 s" is
   87  # three seconds and not a rounding of two point one.
   88  uptime_cs() {
   89      local up
   90      read -r up _ < /proc/uptime
   91      echo "${up%.*}${up#*.}"
   92  }
   93  
   94  # The same test cloud_backup's check_network_link makes: reads the kernel's
   95  # table, sends nothing.
   96  has_default_route() {
   97      ip -4 route show default 2>/dev/null | grep -q . \
   98          || ip -6 route show default 2>/dev/null | grep -q .
   99  }
  100  
  101  # NetworkManager's word for the whole stack: connected, connecting,
  102  # disconnected, asleep, or "connected (site)" / "connected (local)" for a
  103  # device that is up without a default route. Empty when nmcli is absent or
  104  # NetworkManager does not answer within 5 s -- nmcli talks over D-Bus, and
  105  # an unanswered D-Bus call would otherwise wait forever, which in a tool
  106  # whose job is to bound a wait is the one failure it may not have.
  107  nm_state()        { timeout 5 nmcli -g STATE general 2>/dev/null; }
  108  nm_connectivity() { timeout 5 nmcli -g CONNECTIVITY general 2>/dev/null; }
  109  
  110  # The stand-in when NetworkManager cannot be asked: some interface other
  111  # than loopback has a carrier.
  112  carrier_up() {
  113      local f
  114      for f in /sys/class/net/*/carrier; do
  115          case "${f}" in */lo/carrier) continue ;; esac
  116          [ "$(cat "${f}" 2>/dev/null)" = "1" ] && return 0
  117      done
  118      return 1
  119  }
  120  
  121  START=$(uptime_cs)
  122  DEADLINE=$((START + WAIT * 100))
  123  GRACE_CS=$((GRACE * 100))
  124  SETTLED_SINCE=""
  125  ANNOUNCED=0
  126  FALLBACK_SAID=0
  127  STATE=""
  128  CONN=""
  129  
  130  while :; do
  131      NOW=$(uptime_cs)
  132  
  133      if ! has_default_route; then
  134          # No route yet. A link that is coming up -- NetworkManager says
  135          # `connecting`, or with no NetworkManager to ask some interface has
  136          # a carrier -- is waited for up to the deadline, so the card's
  137          # WAITING FOR A NETWORK line can be reached (#192, D-CLOUD-136; it
  138          # was written in RC-11 and this exit stood in front of it). A
  139          # device that is disconnected, asleep, or has its radio off exits at
  140          # once as before: on the plane the card ends in a successful sync's
  141          # time (D-CLOUD-072, D-CLOUD-112).
  142          STATE=$(nm_state)
  143          case "${STATE}" in
  144              connecting*) COMING_UP=1 ;;
  145              '') if carrier_up; then COMING_UP=1; else COMING_UP=0; fi ;;
  146              *) COMING_UP=0 ;;
  147          esac
  148          if [ "${COMING_UP}" = 0 ]; then
  149              echo "Skipped: there's no network connection. Try again when you're online."
  150              log "no default route after $(((NOW - START) / 100))s (NetworkManager: ${STATE:-not asked}); exit ${EXIT_NO_NETWORK}"
  151              exit "${EXIT_NO_NETWORK}"
  152          fi
  153          if [ "${NOW}" -ge "${DEADLINE}" ]; then
  154              echo "Skipped: your network didn't come up in time. Try again when you're online."
  155              log "no default route after ${WAIT}s while ${STATE:-a carrier} was coming up; exit ${EXIT_NO_NETWORK}"
  156              exit "${EXIT_NO_NETWORK}"
  157          fi
  158          SETTLED_SINCE=""
  159          if [ "${ANNOUNCED}" = 0 ]; then
  160              echo ">>> doing network"
  161              ANNOUNCED=1
  162          fi
  163          sleep "${POLL}"
  164          continue
  165      fi
  166  
  167      STATE=$(nm_state)
  168      if [ -n "${STATE}" ]; then
  169          CONN=$(nm_connectivity)
  170          # Any "connected" state settles -- "connected", "connected (site
  171          # only)", "connected (local only)" -- once the default route above
  172          # has held for GRACE seconds. NetworkManager's connectivity word is
  173          # logged and not judged. It used to be: only "full" (or "unknown",
  174          # or blank) settled, and "limited" or "portal" kept waiting until
  175          # the deadline. The maintainer's RG SP (2026-09-12, 7eb713bbd9) sat
  176          # at "connected (site only), connectivity limited" for its whole
  177          # uptime while dropbox.com and two public connectivity checks
  178          # answered it in under a second: NetworkManager's probe had failed
  179          # once at boot and it re-checks every five minutes, so a 60 s wait
  180          # could never see it change, and the startup sync ended "no
  181          # network" on a device that had one. The judge of the cloud is the
  182          # bounded run that follows (D-CLOUD-118): a portal or a dead link
  183          # ends it within seconds with its own words, which is D-CLOUD-112's
  184          # shape. "connecting" and "disconnected" still wait.
  185          case "${STATE}" in
  186              connected*) SETTLED=1 ;;
  187              *) SETTLED=0 ;;
  188          esac
  189      else
  190          if [ "${FALLBACK_SAID}" = 0 ]; then
  191              log "nmcli unavailable or NetworkManager not answering; judging by the route and a carrier alone" WARN
  192              FALLBACK_SAID=1
  193          fi
  194          if carrier_up; then SETTLED=1; else SETTLED=0; fi
  195      fi
  196  
  197      if [ "${SETTLED}" = 1 ]; then
  198          [ -n "${SETTLED_SINCE}" ] || SETTLED_SINCE=${NOW}
  199          if [ $((NOW - SETTLED_SINCE)) -ge "${GRACE_CS}" ]; then
  200              log "network settled (${STATE:-carrier}${CONN:+, connectivity ${CONN}}), held ${GRACE}s, ready after $(((NOW - START) / 100))s"
  201              exit 0
  202          fi
  203      else
  204          SETTLED_SINCE=""
  205          if [ "${NOW}" -ge "${DEADLINE}" ]; then
  206              echo "Skipped: your network didn't come up in time. Try again when you're online."
  207              log "not settled after ${WAIT}s (NetworkManager: ${STATE:-not asked}${CONN:+, connectivity ${CONN}}); exit ${EXIT_NO_NETWORK}"
  208              exit "${EXIT_NO_NETWORK}"
  209          fi
  210      fi
  211  
  212      if [ "${ANNOUNCED}" = 0 ]; then
  213          echo ">>> doing network"
  214          ANNOUNCED=1
  215      fi
  216      sleep "${POLL}"
  217  done
```

## File: sources/cloud_saves_root (at 8ebaf8daad, 205 lines, whole)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # cloud_saves_root - which card the saves folder is on, and whether that
    6  # changed since saves were last synced.
    7  #
    8  # On a device with two microSD cards the second one is bound over
    9  # /storage/roms by the automount script, which first unmounts whatever is
   10  # there. For a moment at every boot -- and the interface starts in that
   11  # same moment -- /storage/roms is the internal card. A saves transfer that
   12  # begins then writes a whole tree onto the wrong card, and a stale copy on
   13  # whichever card is mounted later reads as this device's newest save.
   14  # Seen on an RG SP on 2026-09-08: 101 files on the internal card written
   15  # by boot restores, with both cards in the device the whole time (fork
   16  # #83, D-CLOUD-054).
   17  #
   18  # So the filesystem under SAVESPATH is remembered when saves are synced,
   19  # a transfer waits a little for the usual card to come back before it
   20  # refuses, and it refuses to record a run during which the card changed.
   21  #
   22  #   cloud_saves_root identity            print the identity of the filesystem under SAVESPATH
   23  #   cloud_saves_root check [--wait N]    exit 0 and print the identity when it matches the
   24  #                                        record (or there is none), waiting up to N seconds
   25  #                                        for a mismatch to clear; exit 1 with the reason on
   26  #                                        stdout when it does not
   27  #   cloud_saves_root record [IDENTITY] [--no-write]
   28  #                                        remember the current identity after a successful
   29  #                                        sync; with IDENTITY (the one check printed before
   30  #                                        the transfer), refuse with exit 1 when the folder
   31  #                                        is on a different card now. --no-write compares
   32  #                                        and records nothing: what a transfer that failed
   33  #                                        asks, so a card change still names itself
   34  #                                        without a failed run becoming the record. A
   35  #                                        record that cannot be written is exit 1 too.
   36  #   cloud_saves_root accept              the owner says the current card is right: remember it
   37  #
   38  # The identity is the filesystem UUID of the mount holding SAVESPATH, from
   39  # blkid; where there is none, the device number. The record lives under
   40  # /storage/.cache, which is always the internal card, so it is the same
   41  # file whichever card /storage/roms is on -- that is the point.
   42  
   43  RECORD="/storage/.cache/cloud_sync/saves-root"
   44  CONF="/storage/.config/cloud_sync.conf"
   45  
   46  saves_path() {
   47      local p
   48      p=$(sed -n 's/^SAVESPATH="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' "${CONF}" 2>/dev/null | head -1)
   49      [ -n "${p}" ] || p=$(sed -n 's/^BACKUPPATH="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' "${CONF}" 2>/dev/null | head -1)
   50      echo "${p:-/storage/roms}"
   51  }
   52  
   53  # The mount that holds a path: the longest mount point that is a prefix of
   54  # it. /proc/mounts lists the most recent mount of a path last, which is the
   55  # one in effect -- the bind of the second card over /storage/roms.
   56  mount_of() {
   57      local target="$1" best="" bestlen=0 dev mp
   58      while read -r dev mp _; do
   59          case "${target}/" in
   60              "${mp%/}/"*)
   61                  if [ ${#mp} -ge ${bestlen} ]; then
   62                      best="${dev}"; bestlen=${#mp}
   63                  fi
   64              ;;
   65          esac
   66      done < /proc/mounts
   67      echo "${best}"
   68  }
   69  
   70  identity() {
   71      local root dev uuid
   72      root=$(saves_path)
   73      dev=$(mount_of "${root}")
   74      uuid=""
   75      case "${dev}" in
   76          /dev/*) uuid=$(blkid -o value -s UUID "${dev}" 2>/dev/null) ;;
   77      esac
   78      if [ -n "${uuid}" ]; then
   79          echo "uuid:${uuid}"
   80      else
   81          # No block device or no UUID (overlay, bind of a directory): the
   82          # device number still tells one filesystem from another this boot.
   83          echo "dev:$(stat -c %d "${root}" 2>/dev/null || echo unknown)"
   84      fi
   85  }
   86  
   87  # The record, whole or not at all: written beside itself and renamed over,
   88  # so a kill mid-write leaves the previous record and never an empty file
   89  # (which check would then have to refuse -- D-CLOUD-078, #105).
   90  #
   91  # And it says whether it landed (#308 gpt F-CS-20): the callers exited 0
   92  # whatever happened here, so a full or read-only /storage/.cache left the
   93  # guard with no record while every run reported it made one.
   94  write_record() {
   95      mkdir -p "$(dirname "${RECORD}")" 2>/dev/null
   96      if { printf '%s\n' "$1" > "${RECORD}.tmp.$$"; } 2>/dev/null \
   97          && mv -f "${RECORD}.tmp.$$" "${RECORD}" 2>/dev/null; then
   98          return 0
   99      fi
  100      rm -f "${RECORD}.tmp.$$" 2>/dev/null
  101      return 1
  102  }
  103  
  104  # Re-read the identity once a second until it equals $1 or $2 seconds pass;
  105  # print what it is at the end.
  106  wait_for() {
  107      local want="$1" deadline now
  108      deadline=$(( $(date +%s) + ${2} ))
  109      now=$(identity)
  110      while [ "${now}" != "${want}" ] && [ "$(date +%s)" -lt "${deadline}" ]; do
  111          sleep 1
  112          now=$(identity)
  113      done
  114      echo "${now}"
  115  }
  116  
  117  case "${1:-}" in
  118      identity)
  119          identity
  120      ;;
  121      check)
  122          shift
  123          WAIT=0
  124          while [ $# -gt 0 ]; do
  125              case "$1" in
  126                  --wait) WAIT="${2:-0}"; shift 2 ;;
  127                  *) shift ;;
  128              esac
  129          done
  130          now=$(identity)
  131          if [ -e "${RECORD}" ] && [ ! -s "${RECORD}" ]; then
  132              # A record that exists and says nothing is not "no record": it is
  133              # a record that was being written when something killed the
  134              # writer, and it must not pass the transfer unchecked (the #83
  135              # guard failing open). Refuse until a good run rewrites it, or
  136              # the owner accepts the card.
  137              echo ">>> why COULDN'T TELL WHICH CARD YOUR SAVES ARE ON"
  138              echo "We can't tell which card your saves were last synced from, so nothing was transferred."
  139              echo "If both cards are in the device, try again."
  140              logger -t cloud_saves_root "refused: the record at ${RECORD} exists and is empty; to accept the current card deliberately run: cloud_setup --accept-saves-root" 2>/dev/null
  141              exit 1
  142          fi
  143          if [ -s "${RECORD}" ]; then
  144              last=$(head -1 "${RECORD}")
  145              if [ "${now}" != "${last}" ] && [ "${WAIT}" -gt 0 ] 2>/dev/null; then
  146                  # At boot the second card is bound over the saves folder a
  147                  # moment after the interface starts; give it that moment.
  148                  echo "The saves folder is not on its usual card yet; waiting up to ${WAIT}s for it." >&2
  149                  now=$(wait_for "${last}" "${WAIT}")
  150              fi
  151              if [ "${now}" != "${last}" ]; then
  152                  # The why line first, for the caller to relay (D-UI-028);
  153                  # then the reason and what to do, in the player's words. How
  154                  # to accept the new card deliberately is a command, so it goes
  155                  # to the log, not the screen -- no menu row offers it yet.
  156                  echo ">>> why YOUR SAVES ARE ON A DIFFERENT CARD"
  157                  echo "Your saves are on a different card than the last time they were synced."
  158                  echo "Nothing was transferred. If your second card is missing, put it back and try again."
  159                  logger -t cloud_saves_root "refused: saves root ${now}, recorded ${last}; to accept the current card deliberately run: cloud_setup --accept-saves-root" 2>/dev/null
  160                  exit 1
  161              fi
  162          fi
  163          echo "${now}"
  164          exit 0
  165      ;;
  166      record)
  167          now=$(identity)
  168          WANT="" NO_WRITE=0
  169          shift
  170          for _a in "$@"; do
  171              case "${_a}" in
  172                  --no-write) NO_WRITE=1 ;;
  173                  *) WANT="${_a}" ;;
  174              esac
  175          done
  176          if [ -n "${WANT}" ] && [ "${now}" != "${WANT}" ]; then
  177              echo ">>> why YOUR SAVES CHANGED CARDS PART-WAY THROUGH"
  178              echo "Your saves changed cards part-way through, so some files may have gone to the other card."
  179              echo "Nothing was recorded. Try the transfer again once both cards are back in place."
  180              logger -t cloud_saves_root "refused to record: saves root $(saves_path) started on ${WANT} and is on ${now} now" 2>/dev/null
  181              exit 1
  182          fi
  183          [ "${NO_WRITE}" -eq 1 ] && exit 0
  184          if ! write_record "${now}"; then
  185              echo ">>> why COULDN'T RECORD WHICH CARD YOUR SAVES ARE ON"
  186              echo "Your saves moved, but this device couldn't note which card they're on."
  187              echo "If its storage is full, free some space and try again."
  188              logger -t cloud_saves_root "could not write ${RECORD}" 2>/dev/null
  189              exit 1
  190          fi
  191          exit 0
  192      ;;
  193      accept)
  194          if ! write_record "$(identity)"; then
  195              echo "Couldn't save which card your saves are on. If this device's storage is full, free some space and try again."
  196              exit 1
  197          fi
  198          echo "Saves folder accepted: $(cat "${RECORD}" 2>/dev/null)"
  199          exit 0
  200      ;;
  201      *)
  202          echo "usage: cloud_saves_root identity|check [--wait N]|record [IDENTITY]|accept" >&2
  203          exit 2
  204      ;;
  205  esac
```

## File: sources/cloud_sync_helper (at 8ebaf8daad, 625 lines, whole)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # Helper script to manage cloud sync rules and configuration
    6  # Called by both cloud_backup and cloud_restore scripts
    7  #
    8  # This script handles:
    9  # 1. Merging default rules with user customizations
   10  # 2. Updating configuration files while preserving user settings
   11  # 3. Ensuring all required parameters exist with sensible defaults
   12  #
   13  # Version: 1.0
   14  # Last updated: 2024
   15  
   16  # Logs messages to the specified log file
   17  log_to_file() {
   18    local log_file="${1}"
   19    local message="${2}"
   20    local level="${3:-INFO}"
   21    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
   22    local script_name="cloud_sync_helper"
   23    
   24    echo "[${timestamp}] [${level}] [${script_name}] ${message}" >> ${log_file}
   25  }
   26  
   27  # Is this rules file whole? The allowlist's last rule is the catch-all
   28  # "- /**", written last, so a file cut anywhere lacks it -- and without it
   29  # the allowlist admits everything under the saves folder, the ROMs
   30  # included. The line itself, whole: "- /**/*.db" starts the same way and
   31  # stands near the top of every rules file (audit #308, claude F-CS-06; the
   32  # test was an unanchored '^- /\*\*', which it matched).
   33  rules_whole() {
   34    [ -s "$1" ] && grep -qx -- '- /\*\*' "$1"
   35  }
   36  
   37  # Merges default rules with user-customized rules
   38  # 
   39  # This function preserves user customizations while adding new default rules.
   40  # It creates a backup of the user's current rules before modifying them,
   41  # then adds any default rules that are not present in the user's file.
   42  # 
   43  # Parameters:
   44  #   $1: Path to log file for operation messages
   45  # Returns:
   46  #   0 on success, 1 if default rules file not found
   47  update_cloud_sync_rules() {
   48    local log_file="${1:-/var/log/cloud_sync.log}"
   49    local rules="/storage/.config/cloud_sync-rules.txt"
   50    
   51    log_to_file "${log_file}" "Checking cloud sync rules file..."
   52    
   53    # Check if user has a custom cloud_sync-rules.txt
   54    if [ -f "${rules}" ]; then
   55      # Check if defaults file exists
   56      if [ ! -f "/usr/config/cloud_sync-rules.txt.defaults" ]; then
   57        log_to_file "${log_file}" "Default rules file not found" "WARN"
   58        return 1
   59      fi
   60      
   61      log_to_file "${log_file}" "Merging custom rules with defaults"
   62  
   63      # Collect the user's own rules - lines that are not in the defaults.
   64      # The -e flag ensures grep treats the entire line as a fixed pattern,
   65      # preventing misinterpretation of spaces and special characters in rules.
   66      #
   67      # Except the rules that never took effect (#308 claude F-CS-11). The
   68      # helper this replaced -- upstream's, and every device's before this
   69      # fork's merge -- appended each non-default rule AFTER the catch-all,
   70      # where rclone never reached it; moving all of them to the top on the
   71      # first merge woke whatever anybody had ever typed, working or not, with
   72      # no word said: a `+ /roms/**` somebody tried once would send the ROM
   73      # library into the saves folder on the next sync. So on the first merge
   74      # this build makes (no marker yet), a rule found below the catch-all is
   75      # kept as it was -- inert -- written after the defaults as a comment,
   76      # "# inert: <rule>", and logged; that line is carried as it stands by
   77      # every later merge. From then on a rule anywhere is the player's and
   78      # goes first, as the merge intends.
   79      local marker=/storage/.config/.cloud_sync-rules-user-first-applied first_merge=0 past_catch_all=0
   80      [ -e "${marker}" ] || first_merge=1
   81      : > /tmp/cloud_sync-rules.user
   82      : > /tmp/cloud_sync-rules.inert
   83      while IFS= read -r line; do
   84        case "${line}" in
   85          "# inert: "*) echo "${line#\# inert: }" >> /tmp/cloud_sync-rules.inert; continue ;;
   86          "- /**") past_catch_all=1 ;;
   87        esac
   88        if [[ "$line" != \#* ]] && [[ -n "$line" ]]; then
   89          if ! grep -Fxq -e "$line" /usr/config/cloud_sync-rules.txt.defaults; then
   90            if [ "${first_merge}" = 1 ] && [ "${past_catch_all}" = 1 ]; then
   91              echo "$line" >> /tmp/cloud_sync-rules.inert
   92              log_to_file "${log_file}" "rule '${line}' sat below the catch-all and never took effect; kept, commented out, as it was" "WARN"
   93            else
   94              echo "$line" >> /tmp/cloud_sync-rules.user
   95            fi
   96          fi
   97        fi
   98      done < "${rules}"
   99  
  100      # User rules go FIRST, then the defaults. rclone filters are
  101      # first-match-wins, so position is the only thing that grants precedence:
  102      # appended after the defaults these were unreachable - every one of them
  103      # sat below the catch-all "- /**", so a customization was silently
  104      # ignored while still being visible in the file. Placing them ahead of
  105      # the defaults is also what lets a user's "+ include" beat a default
  106      # exclusion, which moving them above the catch-all alone would not.
  107      # Assembled beside the file it replaces, then renamed over it. It used
  108      # to be built under /tmp and moved: /tmp is another filesystem, so that
  109      # mv was a copy and an unlink -- a truncate-then-write of the live rules
  110      # file, with the catch-all (written last) the first line to be missing
  111      # from a cut copy (D-CLOUD-078, #105). Same directory, so it is a rename.
  112      #
  113      # And only a whole candidate replaces it (audit #307 PL-020). Every write
  114      # below is checked, and the candidate must carry the catch-all before
  115      # the rename: a card that fills while the defaults are being appended
  116      # used to leave a candidate cut before "- /**", and the unconditional
  117      # rename made that the live allowlist -- one that admits the ROMs.
  118      local built=0
  119      : > "${rules}.new" && built=1
  120      if [ "${built}" = 1 ] && [ -s /tmp/cloud_sync-rules.user ]; then
  121        {
  122          echo "# ----------------------------------------------------------------"
  123          echo "# Your own rules, kept across updates."
  124          echo "# These come first because rclone uses the first matching rule,"
  125          echo "# so anything here takes precedence over the defaults below."
  126          echo "# ----------------------------------------------------------------"
  127          cat /tmp/cloud_sync-rules.user
  128          echo
  129          echo "# ----------------------------- defaults -------------------------"
  130        } >> "${rules}.new" || built=0
  131      fi
  132      [ "${built}" = 1 ] && { cat /usr/config/cloud_sync-rules.txt.defaults >> "${rules}.new" || built=0; }
  133      if [ "${built}" = 1 ] && [ -s /tmp/cloud_sync-rules.inert ]; then
  134        {
  135          echo
  136          echo "# ----------------------------------------------------------------"
  137          echo "# Rules that sat below the catch-all before this update, where they"
  138          echo "# never took effect. Kept as they were: to use one, write it again"
  139          echo "# at the top of this file."
  140          echo "# ----------------------------------------------------------------"
  141          sed 's/^/# inert: /' /tmp/cloud_sync-rules.inert
  142        } >> "${rules}.new" || built=0
  143      fi
  144      rm -f /tmp/cloud_sync-rules.user /tmp/cloud_sync-rules.inert
  145      if [ "${built}" != 1 ] || ! rules_whole "${rules}.new"; then
  146        rm -f "${rules}.new"
  147        log_to_file "${log_file}" "the merged rules file was not whole (a write failed before its catch-all line); it was not installed and the rules file was left as it was" "WARN"
  148        return 1
  149      fi
  150  
  151      # A merge that changes nothing writes nothing (#308 claude F-CS-18): the
  152      # helper runs before every sync, the one after each game included, and
  153      # rewrote the rules file and its .bak every time -- flash writes and an
  154      # mtime that changes for no reason, which the settings backup then
  155      # carries as a change.
  156      if cmp -s "${rules}.new" "${rules}"; then
  157        rm -f "${rules}.new"
  158        touch "${marker}" 2>/dev/null
  159        return 0
  160      fi
  161  
  162      # Keep a copy of the user's rules before replacing them -- but only of a
  163      # file that is plainly whole: the allowlist ends in its catch-all
  164      # "- /**", and a file cut before that line is not a rules file. Copying
  165      # whatever was there put a truncated file over the last good copy on
  166      # the very next run (D-CLOUD-078, #105). Written beside the copy and
  167      # renamed, so the copy itself is never half-written either.
  168      if rules_whole "${rules}"; then
  169        cp -f "${rules}" "${rules}.bak.tmp" && mv -f "${rules}.bak.tmp" "${rules}.bak"
  170      else
  171        rm -f "${rules}.bak.tmp"
  172        log_to_file "${log_file}" "rules file has no catch-all line; not taking a .bak from it" "WARN"
  173      fi
  174  
  175      # Replace the user's file with the merged version -- one rename -- and
  176      # mark the first merge done only once it has landed.
  177      mv -f "${rules}.new" "${rules}" && touch "${marker}" 2>/dev/null
  178      
  179      log_to_file "${log_file}" "Updated cloud_sync-rules.txt with new defaults while preserving custom rules"
  180    else
  181      # No existing rules file, just copy the defaults
  182      log_to_file "${log_file}" "No existing rules file, copying defaults"
  183      if cp -f /usr/config/cloud_sync-rules.txt.defaults "${rules}.new" && rules_whole "${rules}.new"; then
  184        mv -f "${rules}.new" "${rules}"
  185      else
  186        rm -f "${rules}.new"
  187        log_to_file "${log_file}" "the default rules file could not be copied whole; no rules file was installed" "WARN"
  188        return 1
  189      fi
  190    fi
  191    
  192    return 0
  193  }
  194  
  195  # Is this a cloud_sync.conf that can be run with? bash -n, and a grammar
  196  # nothing but assignments of text can pass. Every line is blank, a
  197  # comment, or KEY=value, where the value is
  198  #   - "double quoted": any text but a backtick, a $ that is not a plain
  199  #     $NAME or ${NAME}, and a backslash that is not the line's last
  200  #     character (the continuation RCLONEOPTS is written with) or one of
  201  #     bash's own escapes inside double quotes, \" \\ \$ and \`, each of
  202  #     which is the one character bash makes of it;
  203  #   - 'single quoted' on one line, with no $( or backtick in it;
  204  #   - or a bare word of letters, digits and . / : @ % + , = _ -;
  205  # and after it nothing, or blanks and a # comment. The shape check matters
  206  # because a torn line -- SAVES_REMOTE="/ROCK, cut mid-value -- can have its
  207  # quote closed by whatever is appended after it, and then parses.
  208  #
  209  # The escapes were refused until the audit of the fix round (PL-015): the
  210  # validator before this grammar passed them, so an upgraded device whose
  211  # hand-edited RCLONEOPTS read --exclude \"*.tmp\" was told its settings
  212  # could not be read on every run. A backslash before anything else is
  213  # still refused; bash would keep it, and nothing needs it.
  214  #
  215  # A blank is a space or a tab, and nothing else is: no line may carry a
  216  # control character but a tab (the audit of the fix round, PL-002). Bash
  217  # does not split a word on a carriage return, a vertical tab or a form
  218  # feed, so EXTRA="x"<CR>#$(cmd) is one word whose $(cmd) runs, and so is a
  219  # "comment" line <CR>#$(cmd) -- and this grammar read all three as blanks
  220  # ([ \t\r] after a value, [[:space:]] before a comment) and passed them.
  221  #
  222  # And nothing in it runs when it is sourced (audit #307 PL-051's script
  223  # half). The setup page writes the folder values from what a player typed
  224  # or picked, and an earlier build wrote one that held "$(...)" as it
  225  # stood, which every `source` of this file then ran; a folder value
  226  # (SAVESPATH, SETTINGS_BACKUPS, SAVES_REMOTE, SETTINGS_REMOTE,
  227  # CONTENT_REMOTE) is plain text on one line, with no $, backtick,
  228  # backslash or control character. The first cut of this refused only $(
  229  # and a backtick, and let a continued line through unchecked: a quoted
  230  # value continued onto a line that closed the quote and went on
  231  # (`RCLONEOPTS="--progress \` then `"; touch x; : ""`), a value closed and
  232  # followed by `; command`, and ${W@P}, which runs the command a value
  233  # spells out, all passed and ran (the audit of the fixes, G-A-05). A
  234  # config that fails is not sourced: the caller falls back to the good
  235  # copy or refuses (YOUR CLOUD SYNC SETTINGS COULDN'T BE READ).
  236  #
  237  # CONF_WHY says why a file was refused -- "line N: <its shape>", never the
  238  # value -- for the caller's log (PL-015): a refusal that names nothing
  239  # leaves whoever reads the log to guess which line of a hand edit it was.
  240  conf_valid() {
  241      CONF_WHY=""
  242      if [ ! -s "$1" ]; then CONF_WHY="the file is missing or empty"; return 1; fi
  243      if ! bash -n "$1" 2>/dev/null; then CONF_WHY="bash cannot parse it"; return 1; fi
  244      # A NUL byte ends awk's record on the device's busybox, so the grammar below
  245      # would read "EXTRA=x"<NUL>"#$(cmd)" as EXTRA=x (the audit of the fixes,
  246      # claude G3-D-02); counted before anything reads the file.
  247      if [ "$(tr -d '\000' < "$1" 2>/dev/null | wc -c)" -ne "$(wc -c < "$1")" ]; then CONF_WHY="a NUL byte"; return 1; fi
  248      CONF_WHY=$(awk '
  249          function bad(why) { if (!failed) print "line " NR ": " why; failed = 1; exit 1 }
  250          # A double-quoted value from position i of s: the position after
  251          # its closing quote, or 0 when the line ends in a continuation.
  252          function dq(s, i,    n, c, d) {
  253              n = length(s)
  254              while (i <= n) {
  255                  c = substr(s, i, 1)
  256                  if (c == "\"") return i + 1
  257                  if (c == "`") bad("a backtick inside double quotes")
  258                  if (c == "\\") {
  259                      if (i == n) return 0
  260                      d = substr(s, i + 1, 1)
  261                      if (d == "$" && substr(s, i + 2, 1) ~ /[(\[{]/) bad("a \\$ followed by (, [ or { -- a literal $( that a shell context could still run (audit of the fixes, G3-D-01)")
  262                      if (d == "\"" || d == "\\" || d == "$" || d == "`") { val = val c d; i += 2; continue }
  263                      bad("a backslash inside double quotes that is not one of the escapes bash reads there")
  264                  }
  265                  if (c == "$") {
  266                      d = substr(s, i + 1)
  267                      if (match(d, /^[A-Za-z_][A-Za-z0-9_]*/) || match(d, /^\{[A-Za-z_][A-Za-z0-9_]*\}/)) {
  268                          val = val c substr(d, 1, RLENGTH); i += 1 + RLENGTH; continue
  269                      }
  270                      bad("a $ inside double quotes that is not a plain $NAME or ${NAME}")
  271                  }
  272                  val = val c; i++
  273              }
  274              bad("a double-quoted value that runs on past the line without a backslash")
  275          }
  276          # After a value: nothing, or blanks and a comment.
  277          function rest(s, i) { if (substr(s, i) !~ /^([ \t]+(#.*)?)?$/) bad("something after the value that is not a # comment") }
  278          function whole() {
  279              if (key ~ /^(SAVESPATH|SETTINGS_BACKUPS|SAVES_REMOTE|SETTINGS_REMOTE|CONTENT_REMOTE)$/ \
  280                  && (val ~ /[$`\\]/ || val ~ /[[:cntrl:]]/ || lines > 1)) bad("a folder value that is not plain text on one line")
  281          }
  282          {
  283              s = $0
  284              t = s; gsub(/\t/, "", t)
  285              if (t ~ /[[:cntrl:]]/) bad("a control character other than a tab")
  286              if (indq) {
  287                  lines++
  288                  j = dq(s, 1)
  289                  if (j == 0) next
  290                  indq = 0; rest(s, j); whole(); next
  291              }
  292              if (s ~ /^[ \t]*(#|$)/) next
  293              if (!match(s, /^[A-Za-z_][A-Za-z0-9_]*=/)) bad("a line that is not KEY=value, a comment or blank")
  294              key = substr(s, 1, RLENGTH - 1); i = RLENGTH + 1; val = ""; lines = 1
  295              # A name the shell owns is refused whatever its value: bash evaluates an
  296              # assignment to RANDOM, SECONDS or LINENO as arithmetic, and arithmetic
  297              # runs a $( ) it finds (the audit of the fixes, gpt G3-D-01: a sourced
  298              # RANDOM="BASH_VERSINFO[\\$(cmd)0]" ran cmd on the host); PATH, IFS and
  299              # the rest change what every later command means.
  300              if (key ~ /^(RANDOM|SRANDOM|SECONDS|LINENO|HISTCMD|BASHPID|BASH_[A-Z_]*|EPOCH[A-Z]*|FUNCNAME|GROUPS|DIRSTACK|PIPESTATUS|SHELLOPTS|BASHOPTS|COMP_[A-Z_]*|READLINE_[A-Z_]*|PATH|IFS|ENV|BASH_ENV|CDPATH|HOME|PS[0-4]|PROMPT_COMMAND|TMPDIR|SHELL|LANG|LC_[A-Z_]*|GLOBIGNORE|HISTFILE|TMOUT|OPTIND|OPTARG|PWD|OLDPWD|SHLVL|UID|EUID|PPID|LD_[A-Z_]*)$/) bad("a name the shell owns (" key ")")
  301              c = substr(s, i, 1)
  302              if (c == "\"") {
  303                  j = dq(s, i + 1)
  304                  if (j == 0) { indq = 1; next }
  305                  rest(s, j); whole(); next
  306              }
  307              if (c == "'"'"'") {
  308                  j = index(substr(s, i + 1), "'"'"'")
  309                  if (!j) bad("a single-quoted value that does not close on its line")
  310                  val = substr(s, i + 1, j - 1)
  311                  if (val ~ /\$\(|`/) bad("a $( or a backtick inside single quotes")
  312                  rest(s, i + j + 1); whole(); next
  313              }
  314              match(substr(s, i), /^[A-Za-z0-9_.\/:@%+,=-]*/)
  315              val = substr(s, i, RLENGTH)
  316              rest(s, i + RLENGTH); whole()
  317          }
  318          END {
  319              if (failed) exit 1
  320              if (indq) { print "line " NR ": a double-quoted value that never closes"; exit 1 }
  321          }
  322      ' "$1")
  323  }
  324  
  325  # Updates user configuration file with new defaults while preserving customizations
  326  #
  327  # This function ensures user configs have all required parameters while 
  328  # preserving any customized values. It adds any missing parameters from
  329  # the defaults file but doesn't overwrite existing user settings.
  330  #
  331  # Parameters:
  332  #   $1: Path to log file for operation messages
  333  # Returns:
  334  #   0 on success, 1 if default config file not found
  335  update_cloud_sync_config() {
  336    local log_file="${1:-/var/log/cloud_sync.log}"
  337    local conf="/storage/.config/cloud_sync.conf"
  338    # Every change below lands in this copy, beside the live file; the live
  339    # file is replaced by one rename once the copy parses. Until 2026-09-10
  340    # each new key was appended to the live file, so a kill mid-append left a
  341    # partial trailing line that `source` then tripped over -- and the callers
  342    # went on with the variables it never reached (D-CLOUD-078, #105).
  343    local work="${conf}.new"
  344    
  345    log_to_file "${log_file}" "Checking cloud sync configuration..."
  346    
  347    # Check if user has a config file
  348    if [ -f "${conf}" ]; then
  349      # Nothing is merged onto a config that does not parse: appending to a
  350      # torn file can close its open quote and hand the callers a config that
  351      # parses and means nothing. The callers fall back to the .bak, or refuse.
  352      # The .bak itself is taken below, from this file, only when the merge
  353      # changes it (#308 claude F-CS-18).
  354      if ! conf_valid "${conf}"; then
  355        rm -f "${conf}.bak.tmp"
  356        log_to_file "${log_file}" "config is not whole (${CONF_WHY}); not taking a .bak from it and not updating it" "WARN"
  357        return 1
  358      fi
  359      
  360      # Check if defaults file exists
  361      if [ ! -f "/usr/config/cloud_sync.conf.defaults" ]; then
  362        log_to_file "${log_file}" "Default config file not found" "WARN"
  363        return 1
  364      fi
  365      
  366      log_to_file "${log_file}" "Updating configuration with new defaults"
  367      cp -f "${conf}" "${work}" || { log_to_file "${log_file}" "could not copy the config to work on" "WARN"; return 1; }
  368      
  369      # Carry a customised value across to a renamed key, once.
  370      #
  371      # The 2026-09 vocabulary sweep (D-UI-022) renamed the path keys so each
  372      # says which tier it belongs to and which side it is on. The append loop
  373      # below only adds a key that is missing, with the shipped default -- so
  374      # without this step a device that had customised SYNCPATH would gain a
  375      # SAVES_REMOTE pointing at /ROCKNIX/Saves and silently stop syncing to
  376      # its own folder. That is the "renamed key resets everyone's preference"
  377      # trap upgrade-and-install.md names. The old key is left in place and
  378      # ignored; the .bak beside the file keeps the pre-migration text.
  379      #
  380      # RESTOREPATH is not carried: saves have one local folder now
  381      # (D-CLOUD-040). A value that differs from the saves folder is reported
  382      # here and refused by every saves transfer until it is removed.
  383      migrate_key() {
  384        local old="$1" new="$2" value
  385        if grep -q "^${old}=" "${work}" \
  386           && ! grep -q "^${new}=" "${work}"; then
  387          value=$(grep -m1 "^${old}=" "${work}" | cut -d= -f2-)
  388          echo "${new}=${value}" >> "${work}"
  389          log_to_file "${log_file}" "Carried ${old} across to ${new} (${value})"
  390        fi
  391      }
  392      migrate_key BACKUPPATH      SAVESPATH
  393      migrate_key BACKUPFOLDER    SETTINGS_BACKUPS
  394      migrate_key SYNCPATH        SAVES_REMOTE
  395      migrate_key SYNCPATH_BACKUP SETTINGS_REMOTE
  396      migrate_key CONTENTPATH     CONTENT_REMOTE
  397      # A value that equals a superseded default is the default, not a choice
  398      # (upgrade-and-install.md: a fix that changes what we write does nothing
  399      # for what is already written). The append loop leaves a key that exists
  400      # alone, so a device configured by an earlier image keeps its old number
  401      # for ever unless it is moved here. The automatic sync's ceiling rose from
  402      # 20 s to 90 s on 2026-09-25 (D-CLOUD-137, #282): the old default follows
  403      # the new one; a value somebody changed is left as it is.
  404      migrate_default() {
  405        local key="$1" old="$2" new="$3" value
  406        grep -q "^${key}=" "${work}" || return 0
  407        value=$(grep -m1 "^${key}=" "${work}" | cut -d= -f2-)
  408        if [ "${value}" = "${old}" ]; then
  409          sed -i "s|^${key}=.*|${key}=${new}|" "${work}"
  410          log_to_file "${log_file}" "Moved ${key} from the superseded default ${old} to ${new}"
  411        fi
  412      }
  413      migrate_default SYNC_CEILING_SECONDS 20 90
  414      migrate_default RCLONE_SYNC_NET_OPTS \
  415        '"--contimeout 5s --timeout 5s --retries 1 --max-duration 20s --low-level-retries 5 --transfers 1"' \
  416        '"--contimeout 5s --timeout 5s --retries 1 --max-duration 90s --low-level-retries 5 --transfers 1"'
  417      # The settings-only rows' last-run stamps carried the old name; move them
  418      # so the rows do not read "never" after the update.
  419      for pair in last-system-backup:last-settings-backup \
  420                  last-system-restore:last-settings-restore \
  421                  system-backup.uploaded:settings-backup.uploaded; do
  422        old_stamp="/storage/.cache/cloud_sync/${pair%%:*}"; new_stamp="/storage/.cache/cloud_sync/${pair##*:}"
  423        if [ -f "${old_stamp}" ] && [ ! -f "${new_stamp}" ]; then
  424          mv "${old_stamp}" "${new_stamp}"
  425          log_to_file "${log_file}" "Carried ${pair%%:*} across to ${pair##*:}"
  426        fi
  427      done
  428      if grep -q '^RESTOREPATH=' "${work}"; then
  429        restore_root=$(grep -m1 '^RESTOREPATH=' "${work}" | cut -d'"' -f2)
  430        saves_root=$(grep -m1 '^SAVESPATH=' "${work}" | cut -d'"' -f2)
  431        if [ -n "${restore_root}" ] && [ "${restore_root}" != "${saves_root}" ]; then
  432          log_to_file "${log_file}" "RESTOREPATH (${restore_root}) differs from SAVESPATH (${saves_root}); saves transfers will refuse until it is removed" "WARN"
  433        fi
  434      fi
  435  
  436      # Extract all configuration variables from defaults. A value that runs
  437      # over several lines with backslashes (RCLONEOPTS) is carried whole:
  438      # until 2026-09-10 only its first line was appended, leaving an open
  439      # quote that broke the file for every reader (found by
  440      # tools/last-good-scripts-test).
  441      local line entry pending="" key value
  442      while IFS= read -r line || [ -n "${line}" ]; do
  443        if [ -n "${pending}" ]; then
  444          pending="${pending}"$'\n'"${line}"
  445          case "${line}" in *\\) continue ;; esac
  446          entry="${pending}"; pending=""
  447        else
  448          case "${line}" in
  449            DEFAULT_*=*) ;;
  450            *) continue ;;
  451          esac
  452          case "${line}" in *\\) pending="${line}"; continue ;; esac
  453          entry="${line}"
  454        fi
  455        key="${entry%%=*}"; value="${entry#*=}"
  456        # Only process DEFAULT_ variables
  457        if [[ "$key" == DEFAULT_* ]]; then
  458          # Strip the DEFAULT_ prefix
  459          var_name="${key#DEFAULT_}"
  460          
  461          # Check if this variable exists in the user config - FIX the grep pattern to avoid space issues
  462          if ! grep -qF "${var_name}=" "${work}"; then
  463            # Public ROCKNIX has no content-library selection to inherit.
  464            # A missing key takes the fresh default; never infer a library or
  465            # the account root from SAVES_REMOTE. An existing CONTENT_REMOTE,
  466            # including an explicit empty root, was preserved by the check above.
  467            echo "${var_name}=${value}" >> "${work}"
  468            log_to_file "${log_file}" "Added new configuration option: ${var_name}"
  469          fi
  470        fi
  471      done < /usr/config/cloud_sync.conf.defaults
  472      
  473      # The merged copy replaces the live file only if it parses; otherwise the
  474      # live file -- and the .bak beside it -- stay exactly as they were. And
  475      # only if it differs (#308 claude F-CS-18): a run with nothing to add
  476      # writes neither the conf nor its .bak. When it does replace it, the
  477      # copy of the user's config -- a file that parses, checked above -- is
  478      # taken first, whole or not at all.
  479      if ! conf_valid "${work}"; then
  480        rm -f "${work}"
  481        log_to_file "${log_file}" "merged configuration does not parse (${CONF_WHY}); the config was left as it was" "WARN"
  482      elif cmp -s "${work}" "${conf}"; then
  483        rm -f "${work}"
  484      elif cp -f "${conf}" "${conf}.bak.tmp" && mv -f "${conf}.bak.tmp" "${conf}.bak" \
  485           && mv -f "${work}" "${conf}"; then
  486        log_to_file "${log_file}" "Configuration file updated while preserving customizations"
  487      else
  488        rm -f "${work}" "${conf}.bak.tmp"
  489        log_to_file "${log_file}" "the configuration could not be updated; the config was left as it was" "WARN"
  490      fi
  491    else
  492      # No existing config file, create one with defaults
  493      log_to_file "${log_file}" "No existing config file, creating from template"
  494      
  495      # Strip the DEFAULT_ prefix; sed preserves multi-line backslash-continued values
  496      sed 's/^DEFAULT_//' /usr/config/cloud_sync.conf.defaults > "${work}" && mv -f "${work}" "${conf}"
  497    fi
  498    
  499    return 0
  500  }
  501  
  502  # Main function that handles all updates
  503  # The log lives on /storage since fork #104 (var-log.mount binds /var/log
  504  # there), so it must not grow without bound -- every run appends and nothing
  505  # ever rotated it; a device in the field already carried 80 KiB of it in RAM.
  506  # Over 1 MiB it is cut to its last 512 KiB, on a line boundary, through a
  507  # temporary and a rename, so a writer mid-line loses nothing. Run once per
  508  # script start, from main, under the caller's run lock, so two scripts never
  509  # trim at once. Sized for months of ordinary runs.
  510  trim_cloud_log() {
  511    local log="${1}" size
  512    [ -n "${log}" ] && [ -f "${log}" ] || return 0
  513    size=$(stat -c %s "${log}" 2>/dev/null) || return 0
  514    [ "${size}" -gt 1048576 ] 2>/dev/null || return 0
  515    if tail -c 524288 "${log}" | sed '1d' > "${log}.tmp" 2>/dev/null; then
  516      mv -f "${log}.tmp" "${log}"
  517      log_to_file "${log}" "log trimmed from ${size} bytes to its last 512 KiB"
  518    else
  519      rm -f "${log}.tmp"
  520    fi
  521    return 0
  522  }
  523  
  524  main() {
  525    local log_file="${1:-/var/log/cloud_sync.log}"
  526    trim_cloud_log "${log_file}"
  527  
  528    # Update both rules and config
  529    update_cloud_sync_rules "${log_file}"
  530    update_cloud_sync_config "${log_file}"
  531    
  532    # Remove conflicting --verbose flags from existing user config to prevent parameter conflicts
  533    # This is needed for users upgrading from older versions where --verbose was used
  534    # Only when there is one: sed -i rewrites the file whether or not it
  535    # matched (#308 claude F-CS-18).
  536    if [ -f "/storage/.config/cloud_sync.conf" ] \
  537       && grep -qE -- '--verbose|-v ' /storage/.config/cloud_sync.conf; then
  538      log_to_file "${log_file}" "Removing conflicting --verbose flags from configuration"
  539      sed -i 's/--verbose//g' /storage/.config/cloud_sync.conf
  540      sed -i 's/-v / /g' /storage/.config/cloud_sync.conf
  541      # Clean up any double spaces left by removal
  542      sed -i 's/  \+/ /g' /storage/.config/cloud_sync.conf
  543      log_to_file "${log_file}" "Configuration cleaned of conflicting flags"
  544    fi
  545  
  546    # Turn an existing mirror backup into a copy.
  547    #
  548    # One cloud folder is shared by every handheld, and BACKUPMETHOD="sync"
  549    # makes it match whichever device ran last -- deleting everything the others
  550    # put there. It cost a real user 70 files: another handheld's whole save
  551    # library, from the shipped default, in one run.
  552    #
  553    # The default is "copy" now, but a default only reaches a device that has no
  554    # value yet: update_cloud_sync_config appends keys it cannot find and never
  555    # touches one already written. So every device set up before this stays on
  556    # sync for ever unless the value is rewritten, which is what the --verbose
  557    # strip above is doing for the same reason.
  558    #
  559    # Deliberately not asking. This changes a destructive setting to a
  560    # non-destructive one, the previous file is kept beside it, and anybody who
  561    # actually wants a mirror can set it back -- where somebody who does not
  562    # want one has no way of learning that they had it until their saves are
  563    # gone.
  564    # Once, and only once. Rewriting on every run does not migrate anybody off a
  565    # bad default -- it takes the setting away, so somebody who reads the docs,
  566    # decides they want a mirror and sets it gets silently overruled on their
  567    # next backup. The marker is what makes this a migration rather than a veto.
  568    # Found by testing: a run with sync deliberately set came back as copy.
  569    if [ -f "/storage/.config/cloud_sync.conf" ] \
  570       && [ ! -f "/storage/.config/.cloud_sync-copy-default-applied" ] \
  571       && grep -q '^BACKUPMETHOD="\?sync"\?' /storage/.config/cloud_sync.conf; then
  572      cp /storage/.config/cloud_sync.conf \
  573         /storage/.config/cloud_sync.conf.pre-copy-default.tmp 2>/dev/null \
  574        && mv -f /storage/.config/cloud_sync.conf.pre-copy-default.tmp \
  575                 /storage/.config/cloud_sync.conf.pre-copy-default 2>/dev/null
  576      sed -i 's|^BACKUPMETHOD=.*|BACKUPMETHOD="copy"|' /storage/.config/cloud_sync.conf
  577      touch /storage/.config/.cloud_sync-copy-default-applied 2>/dev/null
  578      log_to_file "${log_file}" "BACKUPMETHOD was 'sync', which deletes other devices' saves from the shared folder; set to 'copy'. Previous config kept as cloud_sync.conf.pre-copy-default until the next run that completes (D-CLOUD-079). This is done once; setting it back to sync will be respected."
  579    fi
  580  
  581    # The shipped rclone retry bounds, for a device that already has the old
  582    # ones. update_cloud_sync_config only appends keys it cannot find, so a
  583    # value written before today stays for ever -- and the value written before
  584    # today (--low-level-retries 2) makes every saves backup fail on Dropbox
  585    # once a save is already in the cloud, because Dropbox answers concurrent
  586    # writes to one folder with a lock error and two retries do not outlast it.
  587    # Rewritten only when it is still exactly what we shipped, so a hand-tuned
  588    # value is left alone, and only once, with a marker -- the same shape as the
  589    # BACKUPMETHOD migration above and for the same reason.
  590    if [ -f "/storage/.config/cloud_sync.conf" ] \
  591       && [ ! -f "/storage/.config/.cloud_sync-net-opts-retries-applied" ] \
  592       && grep -qF 'RCLONE_NET_OPTS="--contimeout 15s --timeout 30s --low-level-retries 2 --retries 1"' \
  593               /storage/.config/cloud_sync.conf; then
  594      sed -i 's|^RCLONE_NET_OPTS=.*|RCLONE_NET_OPTS="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"|' \
  595          /storage/.config/cloud_sync.conf
  596      touch /storage/.config/.cloud_sync-net-opts-retries-applied 2>/dev/null
  597      log_to_file "${log_file}" "RCLONE_NET_OPTS still held the two-low-level-retry bound, which fails a Dropbox backup whenever a save is replaced; set back to rclone's ten. This is done once; a value you have edited yourself is left alone."
  598    fi
  599  
  600    # The automatic sync's bound, for a device that got its first cut
  601    # (2026-09-12, ten low-level retries left to the caller) before the
  602    # maintainer's baseline of five retries and one transfer at a time
  603    # (D-CLOUD-121) shipped the same day. Same shape as above: rewritten only
  604    # while it is still exactly the first-cut value, once, with a marker.
  605    # Straight to today's value (#308 gpt F-CS-29): this runs after
  606    # update_cloud_sync_config's 20 s -> 90 s step (D-CLOUD-137), which matches
  607    # only the suffixed 20 s value, so writing the suffixed 20 s here left the
  608    # first cut on 20 s until the helper's next run.
  609    if [ -f "/storage/.config/cloud_sync.conf" ] \
  610       && [ ! -f "/storage/.config/.cloud_sync-sync-net-opts-five-applied" ] \
  611       && grep -qF 'RCLONE_SYNC_NET_OPTS="--contimeout 5s --timeout 5s --retries 1 --max-duration 20s"' \
  612               /storage/.config/cloud_sync.conf; then
  613      sed -i 's|^RCLONE_SYNC_NET_OPTS=.*|RCLONE_SYNC_NET_OPTS="--contimeout 5s --timeout 5s --retries 1 --max-duration 90s --low-level-retries 5 --transfers 1"|' \
  614          /storage/.config/cloud_sync.conf
  615      touch /storage/.config/.cloud_sync-sync-net-opts-five-applied 2>/dev/null
  616      log_to_file "${log_file}" "RCLONE_SYNC_NET_OPTS held the first-cut automatic bound; set to today's: five low-level retries, one transfer at a time, a 90 s ceiling (D-CLOUD-121, D-CLOUD-137)"
  617    fi
  618  
  619    return 0
  620  }
  621  
  622  # If script is called directly, run the main function
  623  if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  624    main "$@"
  625  fi
```

## File: sources/cloud_sync_cleanup_duplicates.sh (at 8ebaf8daad, 31 lines, whole)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Remove duplicate variable assignments from cloud_sync.conf, keeping only the first occurrence.
    4  # Usage: ./cloud_sync_cleanup_duplicates.sh /path/to/cloud_sync.conf
    5  
    6  CONF_FILE="${1:-/storage/.config/cloud_sync.conf}"
    7  TMP_FILE="${CONF_FILE}.cleaned"
    8  
    9  # A value continued with a trailing backslash (RCLONEOPTS is written that
   10  # way) is one assignment over several lines: a repeated one is removed whole.
   11  # Its first line alone used to go, and the lines that continued it stayed as
   12  # bare lines -- a file that no longer parses, which every run after then
   13  # refused or fell back from (found in the audit of the fixes to #307).
   14  awk '
   15    skip { skip = ($0 ~ /\\$/); next }
   16    /^[[:space:]]*#/ { print; next }
   17    /^[[:space:]]*$/ { print; next }
   18    /^[A-Za-z0-9_]+=.*$/ {
   19      var=gensub(/=.*/, "", 1)
   20      if (!(var in seen)) {
   21        print
   22        seen[var]=1
   23      } else if ($0 ~ /\\$/) {
   24        skip = 1
   25      }
   26      next
   27    }
   28    { print }
   29  ' "$CONF_FILE" > "$TMP_FILE" && mv "$TMP_FILE" "$CONF_FILE" \
   30    && echo "Duplicate variable assignments removed from $CONF_FILE." \
   31    || { rm -f "$TMP_FILE"; echo "Could not clean $CONF_FILE; left as it was." >&2; exit 1; }
```

## File: sources/rasteratops-settings-archive (at 8ebaf8daad, 43 lines, whole)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present rasteratops (https://github.com/rasteratops)
    4  # Shared archive discovery for cloud_scan and cloud_restore. Sourced, no I/O
    5  # until select_settings_archives is called. Directory priority is part of the
    6  # persisted device identity: current, pre-label, healed IDs, then flat legacy.
    7  # Never search other devices recursively. A failed read is not an empty folder.
    8  select_settings_archives() { # <remote Backups path> <device-id helper>
    9      local root="${1%/}" tool="$2" own="" prior="" previous="" name path rc
   10      local -a names=()
   11      SETTINGS_ARCHIVE_SOURCE=""; SETTINGS_ARCHIVE_LISTING=""; SETTINGS_ARCHIVE_KIND=""
   12      if [ -x "${tool}" ]; then
   13          own=$("${tool}" 2>/dev/null | tr -cd 'A-Za-z0-9_.-')
   14          prior=$("${tool}" --legacy 2>/dev/null | tr -cd 'A-Za-z0-9_.-')
   15          previous=$("${tool}" --previous 2>/dev/null | tr -cd 'A-Za-z0-9_.\n-')
   16      fi
   17      [ -n "${own}" ] && names+=("${own}")
   18      [ -n "${prior}" ] && [ "${prior}" != "${own}" ] && names+=("${prior}")
   19      while IFS= read -r name; do
   20          [ -n "${name}" ] && [ "${name}" != "${own}" ] && [ "${name}" != "${prior}" ] && names+=("${name}")
   21      done <<< "${previous}"
   22      names+=("")
   23      for name in "${names[@]}"; do
   24          case "${name}" in .|..) continue ;; esac
   25          path="${root}${name:+/${name}}"
   26          SETTINGS_ARCHIVE_LISTING=$(rclone lsf --files-only --include '/*.{zip,tar.gz}' "${path}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); rc=$?
   27          case "${rc}" in
   28              0) ;;
   29              3|4) SETTINGS_ARCHIVE_LISTING=""; continue ;;
   30              *) SETTINGS_ARCHIVE_LISTING=""; return "${rc}" ;;
   31          esac
   32          [ -n "${SETTINGS_ARCHIVE_LISTING}" ] || continue
   33          SETTINGS_ARCHIVE_SOURCE="${path}"
   34          case "${name}" in
   35              "") SETTINGS_ARCHIVE_KIND=flat ;;
   36              "${own}") SETTINGS_ARCHIVE_KIND=current ;;
   37              "${prior}") SETTINGS_ARCHIVE_KIND=legacy ;;
   38              *) SETTINGS_ARCHIVE_KIND=previous ;;
   39          esac
   40          return 0
   41      done
   42      return 0
   43  }
```

## File: sources/cloud_sync.conf (at 8ebaf8daad, 160 lines, whole)

```text
    1  # Cloud Sync Configuration
    2  # This file defines paths and settings for cloud sync operations
    3  
    4  # Where things live
    5  # ----------------
    6  # Three kinds of thing move through cloud sync, and each key below says which:
    7  #
    8  #   settings  the configuration archive `backuptool` writes: emulator and
    9  #             interface settings, input mapping, themes, collections, bezels.
   10  #             No saves, no ROMs, no operating system.
   11  #   saves     game saves, save states, and screenshots -- files copied in
   12  #             place, matched by cloud_sync-rules.txt
   13  #   content   ROMs and BIOS files
   14  #
   15  # Keys ending in _REMOTE are folders on the cloud remote; the others are on
   16  # this device. Older configs used BACKUPPATH, RESTOREPATH, BACKUPFOLDER,
   17  # SYNCPATH, SYNCPATH_BACKUP and CONTENTPATH; cloud_sync_helper carries a
   18  # customised value across to the new name once, and the old keys are then
   19  # ignored. RESTOREPATH is gone: saves have one local folder, and a config
   20  # that still points it somewhere else makes every saves transfer refuse.
   21  
   22  # Saves on this device. Game saves, save states, and screenshots are found
   23  # under here by the rules file.
   24  SAVESPATH="/storage/roms"
   25  
   26  # Settings backups on this device (written by backuptool)
   27  SETTINGS_BACKUPS="/storage/roms/backup"
   28  
   29  # Saves on the cloud remote
   30  SAVES_REMOTE="/pixelelated/Saves"
   31  
   32  # Settings backups on the cloud remote. Must be a sibling of SAVES_REMOTE,
   33  # never inside it -- a mirror of the saves folder would delete the archives.
   34  SETTINGS_REMOTE="/pixelelated/Backups"
   35  
   36  # ROMs and BIOS files on the cloud remote, one folder per system plus "bios".
   37  # Previously unset, which put them at the remote root and scattered system
   38  # folders among whatever else lived there.
   39  #
   40  # Unlike the saves folder this key is derived for an upgrading config rather
   41  # than defaulted, so a device set up under an older layout keeps its ROMs
   42  # beside its saves -- except a saves folder at the top level (/GAMES), which
   43  # has no parent to put them beside: that config gets "" (the remote root,
   44  # where its ROMs already were) for its owner to set. Clear it back to "" to
   45  # use the remote root.
   46  CONTENT_REMOTE="/pixelelated/Content"
   47  
   48  
   49  # Logging Options
   50  # --------------
   51  # Set the minimum level of messages to log (INFO, WARN, ERROR)
   52  LOG_LEVEL="INFO"
   53  
   54  # Transfer Settings
   55  # ---------------
   56  # rclone sync rules - modify these options to change transfer behavior
   57  # IMPORTANT: Each option must be preceded by a backslash (\) except the first one
   58  RCLONEOPTS="--progress \
   59  --log-file /var/log/cloud_sync.log \
   60  --filter-from /storage/.config/cloud_sync-rules.txt"
   61  
   62  # Network bounds
   63  # --------------
   64  # Timeouts and retry limits for every rclone command the cloud scripts run
   65  # against the cloud -- transfers, listings, probes, the settings archive's
   66  # upload and its size check. Without them rclone's own defaults apply: a
   67  # 60 s connect timeout, a 5 minute idle timeout, 10 low-level retries and
   68  # 3 whole-run retries, so a Wi-Fi link that drops in the middle of a run
   69  # holds the process for well over ten minutes. On the RG SP that left the
   70  # startup sync's card frozen at 113/113 with the launch gate held (#101,
   71  # #102).
   72  #
   73  # --timeout is rclone's IDLE timeout: it fires when no byte has moved for
   74  # that long, so a large transfer that is making progress is unaffected.
   75  # Size it for a stalled link, not a slow one. That is what bounds a dead
   76  # link, and it is the part that matters for #101/#102.
   77  #
   78  # The two retry counts are different things and only one of them may be cut.
   79  # --retries is whole-run: a failed run is repeated by the exit sync, the next
   80  # boot, or the player, so one attempt is right and the run is not repeated
   81  # here. --low-level-retries is per HTTP operation, and it is what every
   82  # rclone user relies on to ride out a provider's transient errors. Cutting it
   83  # to 2 broke Dropbox outright: Dropbox serialises writes per folder and
   84  # answers concurrent ones with a lock error, so a saves backup that replaced
   85  # more than one file failed every time -- the exit sync after a game, for a
   86  # save already in the cloud, which is the ordinary case. Measured on the
   87  # maintainer's RG SP (2026-09-10): replacing 12 files, 6 moves failed at 2
   88  # low-level retries and 0 failed at 10. It is back at rclone's default.
   89  #
   90  # One line, split on spaces by the scripts. An empty value gives these same
   91  # numbers, never rclone's defaults: the scripts fall back to them.
   92  RCLONE_NET_OPTS="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
   93  
   94  # The automatic sync's bound (D-CLOUD-118) -- the sync at startup and the
   95  # one after a game, which a player is waiting through. Applied on top of
   96  # RCLONE_NET_OPTS by the scripts when EmulationStation passes --automatic;
   97  # the back up and restore you press yourself keep the bound above. From the
   98  # measurement in #135 (2026-09-12): a save syncs in about a second, no
   99  # network is known in half a second, and a cloud that accepts and never
  100  # answers held the card for 321 seconds. Connect in 5 s, give up a stalled
  101  # transfer after 5 s, and never run past the ceiling. Five low-level retries
  102  # and one transfer at a time (2026-09-12, the maintainer's baseline): rclone
  103  # spends the transfer's retries on a refused connection too -- 12 s at ten,
  104  # 3.9 s at five -- and Dropbox's per-folder write lock (#107) is tripped by
  105  # CONCURRENT writes, which one transfer at a time never makes. Tweak on
  106  # feedback -- and tweaked once: the ceiling was 20 s until 2026-09-25, when
  107  # the first exit sync after hours offline carried a two-hour backlog and
  108  # Dropbox moved one file a second (a changed file is moved aside server-side
  109  # and then uploaded; an unchanged one whose time differs is re-uploaded, since
  110  # Dropbox cannot set a time), so twelve operations were all the twenty
  111  # seconds allowed and the run read COULDN'T FINISH. Ninety seconds is the
  112  # maintainer's longer budget (D-CLOUD-137, #282): the idle timeout still ends
  113  # a stalled transfer in five, so the ceiling only counts while bytes move,
  114  # and a launch pressed mid-sync waits for it that long at most (D-CLOUD-109).
  115  RCLONE_SYNC_NET_OPTS="--contimeout 5s --timeout 5s --retries 1 --max-duration 90s --low-level-retries 5 --transfers 1"
  116  SYNC_CEILING_SECONDS=90
  117  
  118  # Backup Options
  119  # -------------
  120  ## Backup method
  121  ### The default is "copy", which sends each save that differs and never deletes
  122  ### anything in the cloud; whatever it replaces is kept for one cycle in the
  123  ### folder beside the saves folder named <saves folder>-replaced.
  124  ### "sync" also deletes from the cloud whatever this device does not have --
  125  ### every other device's saves, in a folder they share. It is honoured if set
  126  ### here; no menu offers it.
  127  ### --delete-excluded is removed from RCLONEOPTS before every run, whatever
  128  ### this file says, so a mirror never reaches past the rules file.
  129  BACKUPMETHOD="copy"
  130  
  131  ## How many dated settings backups to keep in the cloud, per device
  132  ### Each is a full archive (~17MB). Older ones beyond this are removed
  133  ### after a successful upload. Set to a larger number to keep more
  134  ### history, at the cost of cloud storage.
  135  ### Only archives carrying this device's name, between the date and
  136  ### ROCKNIX (<date>-<device>-ROCKNIX_SETTINGS.tar.gz), are counted and
  137  ### removed; one carrying another device's name, or none, is left alone.
  138  CLOUD_BACKUP_KEEP="3"
  139  
  140  ## Enable backing-up the settings backup file
  141  ### The default is "yes", which will include the settings backup file in the backup
  142  ### Switching to "no" will exclude the settings backup file from the backup
  143  BACKUPFILE_BACKUP_OPTION="yes"
  144  
  145  # Restore Options
  146  # --------------
  147  ## Restore method
  148  ### The default is "copy", which will preserve any existing files and folders
  149  ### Switching to "sync" will replace all local files in the restore path with what is on the remote
  150  RESTOREMETHOD="copy"
  151  
  152  ## Enable restoring the settings backup file
  153  ### The default is "no", which will exclude the settings backup file from the restore
  154  ### Switching to "yes" will include the settings backup file in the restore
  155  BACKUPFILE_RESTORE_OPTION="no"
  156  
  157  # Maintenance Options
  158  # -----------------
  159  # Option to enable/disable removing orphaned empty directories on the remote that are also empty locally. Enabled by default. Comment out to disable.
  160  RSYNCRMDIR="yes"
```

## File: sources/cloud_sync.conf.defaults (at 8ebaf8daad, 140 lines, whole)

```text
    1  # Cloud Sync Default Configuration
    2  # This file defines the default values used when creating a new configuration
    3  
    4  # Where things live
    5  # ----------------
    6  # Three kinds of thing move through cloud sync, and each key below says which:
    7  #
    8  #   settings  the configuration archive `backuptool` writes: emulator and
    9  #             interface settings, input mapping, themes, collections, bezels.
   10  #             No saves, no ROMs, no operating system.
   11  #   saves     game saves, save states, and screenshots -- files copied in
   12  #             place, matched by cloud_sync-rules.txt
   13  #   content   ROMs and BIOS files
   14  #
   15  # Keys ending in _REMOTE are folders on the cloud remote; the others are on
   16  # this device. Older configs used BACKUPPATH, RESTOREPATH, BACKUPFOLDER,
   17  # SYNCPATH, SYNCPATH_BACKUP and CONTENTPATH; cloud_sync_helper carries a
   18  # customised value across to the new name once, and the old keys are then
   19  # ignored. RESTOREPATH is gone: saves have one local folder, and a config
   20  # that still points it somewhere else makes every saves transfer refuse.
   21  
   22  # Saves on this device. Game saves, save states, and screenshots are found
   23  # under here by the rules file.
   24  DEFAULT_SAVESPATH="/storage/roms"
   25  
   26  # Settings backups on this device (written by backuptool)
   27  DEFAULT_SETTINGS_BACKUPS="/storage/roms/backup"
   28  
   29  # Saves on the cloud remote
   30  DEFAULT_SAVES_REMOTE="/pixelelated/Saves"
   31  
   32  # Settings backups on the cloud remote. Must be a sibling of SAVES_REMOTE,
   33  # never inside it -- a mirror of the saves folder would delete the archives.
   34  DEFAULT_SETTINGS_REMOTE="/pixelelated/Backups"
   35  
   36  # ROMs and BIOS files on the cloud remote, one folder per system plus "bios".
   37  # Previously unset, which put them at the remote root and scattered system
   38  # folders among whatever else lived there.
   39  #
   40  # Unlike the saves folder this key is derived for an upgrading config rather
   41  # than defaulted, so a device set up under an older layout keeps its ROMs
   42  # beside its saves -- except a saves folder at the top level (/GAMES), which
   43  # has no parent to put them beside: that config gets "" (the remote root,
   44  # where its ROMs already were) for its owner to set. Clear it back to "" to
   45  # use the remote root.
   46  DEFAULT_CONTENT_REMOTE="/pixelelated/Content"
   47  
   48  # Logging Options
   49  # --------------
   50  # Set the minimum level of messages to log (INFO, WARN, ERROR)
   51  DEFAULT_LOG_LEVEL="INFO"
   52  
   53  # Transfer Settings
   54  # ---------------
   55  # rclone sync rules - modify these options to change transfer behavior
   56  # IMPORTANT: Each option must be preceded by a backslash (\) except the first one
   57  # The saves allowlist (--filter-from /storage/.config/cloud_sync-rules.txt) is
   58  # applied whether or not it appears here: dropping it from this line does not
   59  # drop it from the transfer (#71). To change what syncs, edit the rules file.
   60  DEFAULT_RCLONEOPTS="--progress \
   61  --log-file /var/log/cloud_sync.log \
   62  --filter-from /storage/.config/cloud_sync-rules.txt"
   63  
   64  # Network bounds
   65  # --------------
   66  # Timeouts and retry limits for every rclone command the cloud scripts run
   67  # against the cloud -- transfers, listings, probes, the settings archive's
   68  # upload and its size check. Without them rclone's own defaults apply: a
   69  # 60 s connect timeout, a 5 minute idle timeout, 10 low-level retries and
   70  # 3 whole-run retries, so a Wi-Fi link that drops in the middle of a run
   71  # holds the process for well over ten minutes. On the RG SP that left the
   72  # startup sync's card frozen at 113/113 with the launch gate held (#101,
   73  # #102).
   74  #
   75  # --timeout is rclone's IDLE timeout: it fires when no byte has moved for
   76  # that long, so a large transfer that is making progress is unaffected.
   77  # Size it for a stalled link, not a slow one. That is what bounds a dead
   78  # link, and it is the part that matters for #101/#102.
   79  #
   80  # The two retry counts are different things and only one of them may be cut.
   81  # --retries is whole-run: a failed run is repeated by the exit sync, the next
   82  # boot, or the player, so one attempt is right and the run is not repeated
   83  # here. --low-level-retries is per HTTP operation, and it is what every
   84  # rclone user relies on to ride out a provider's transient errors. Cutting it
   85  # to 2 broke Dropbox outright: Dropbox serialises writes per folder and
   86  # answers concurrent ones with a lock error, so a saves backup that replaced
   87  # more than one file failed every time -- the exit sync after a game, for a
   88  # save already in the cloud, which is the ordinary case. Measured on the
   89  # maintainer's RG SP (2026-09-10): replacing 12 files, 6 moves failed at 2
   90  # low-level retries and 0 failed at 10. It is back at rclone's default.
   91  #
   92  # One line, split on spaces by the scripts. An empty value gives these same
   93  # numbers, never rclone's defaults: the scripts fall back to them.
   94  DEFAULT_RCLONE_NET_OPTS="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
   95  DEFAULT_RCLONE_SYNC_NET_OPTS="--contimeout 5s --timeout 5s --retries 1 --max-duration 90s --low-level-retries 5 --transfers 1"
   96  DEFAULT_SYNC_CEILING_SECONDS=90
   97  
   98  # Backup Options
   99  # -------------
  100  ## Backup method
  101  ### The default is "copy", which sends each save that differs and never deletes
  102  ### anything in the cloud; whatever it replaces is kept for one cycle in the
  103  ### folder beside the saves folder named <saves folder>-replaced.
  104  ### "sync" also deletes from the cloud whatever this device does not have --
  105  ### every other device's saves, in a folder they share. It is honoured if set
  106  ### here; no menu offers it.
  107  ### --delete-excluded is removed from RCLONEOPTS before every run, whatever
  108  ### this file says, so a mirror never reaches past the rules file.
  109  DEFAULT_BACKUPMETHOD="copy"
  110  
  111  ## How many dated settings backups to keep in the cloud, per device
  112  ### Each is a full archive (~17MB). Older ones beyond this are removed
  113  ### after a successful upload. Set to a larger number to keep more
  114  ### history, at the cost of cloud storage.
  115  ### Only archives carrying this device's name, between the date and
  116  ### ROCKNIX (<date>-<device>-ROCKNIX_SETTINGS.tar.gz), are counted and
  117  ### removed; one carrying another device's name, or none, is left alone.
  118  DEFAULT_CLOUD_BACKUP_KEEP="3"
  119  
  120  ## Enable backing-up the settings backup file
  121  ### The default is "yes", which will include the settings backup file in the backup
  122  ### Switching to "no" will exclude the settings backup file from the backup
  123  DEFAULT_BACKUPFILE_BACKUP_OPTION="yes"
  124  
  125  # Restore Options
  126  # --------------
  127  ## Restore method
  128  ### The default is "copy", which will preserve any existing files and folders
  129  ### Switching to "sync" will replace all local files in the restore path with what is on the remote
  130  DEFAULT_RESTOREMETHOD="copy"
  131  
  132  ## Enable restoring the settings backup file
  133  ### The default is "no", which will exclude the settings backup file from the restore
  134  ### Switching to "yes" will include the settings backup file in the restore
  135  DEFAULT_BACKUPFILE_RESTORE_OPTION="no"
  136  
  137  # Maintenance Options
  138  # -----------------
  139  # Option to enable/disable removing orphaned empty directories on the remote that are also empty locally. Enabled by default. Comment out to disable.
  140  DEFAULT_RSYNCRMDIR="yes"
```

## File: sources/cloud_sync-rules.txt (at 8ebaf8daad, 89 lines, whole)

```text
    1  # Cloud Sync Rules - Default Configuration
    2  # Rules use the same syntax as .gitignore, and THE FIRST MATCH WINS - a later
    3  # rule cannot override an earlier one.
    4  
    5  # Databases and their sidecars, before anything else can include them.
    6  # A synced database is unresolvable by hand and rclone replaces it wholesale,
    7  # so one device's history would overwrite the other's. Ours lives in
    8  # /storage/.cache and never syncs; this guards against one an emulator drops
    9  # into a save directory.
   10  - /**/*.db
   11  - /**/*.db-wal
   12  - /**/*.db-shm
   13  - /**/*.db-journal
   14  - /**/*.sqlite
   15  - /**/*.sqlite3
   16  
   17  # Start by explicitly including directories we want to fully backup
   18  + /savefiles/**
   19  + /savestates/**
   20  + /screenshots/**
   21  
   22  # Include specific save file types across all directories
   23  + /**/*.srm
   24  + /**/*.sav
   25  + /**/*.fs
   26  + /**/*.state*
   27  + /**/*.auto
   28  + /**/*.dsv*
   29  
   30  # Standalone N64 saves sit BESIDE THE ROM, not in a save directory: every
   31  # shipped mupen64plus.cfg sets SaveSRAMPath = "/storage/roms/n64", so the
   32  # emulator writes n64/<Game>.eep, .mpk, .sra and .fla there. The
   33  # /n64/save/*.eep lines below match the libretro layout and have never
   34  # matched these, so a standalone N64 player's saves have never been backed
   35  # up on any device (#89, D-CLOUD-086). Widened here rather than in the
   36  # per-system block because the four extensions belong to no other system
   37  # and the same file can appear at either depth.
   38  + /**/*.eep
   39  + /**/*.mpk
   40  + /**/*.sra
   41  + /**/*.fla
   42  
   43  # Include system-specific save directories
   44  # Mupen64Plus writes slots 0-9 beside N64 ROMs (native or Project64).
   45  + /n64/*.st[0-9]
   46  + /n64/*.pj[0-9]
   47  + /n64/*.pj[0-9].zip
   48  + /n64/save/*.eep
   49  + /n64/save/*.mpk
   50  + /n64/save/*.sra
   51  + /n64/save/*.srm
   52  + /psx/memcards/*.mcd
   53  + /psx/memcards/*.mcr
   54  # DuckStation redirects its native memory-card directory here.
   55  + /psx/duckstation/memcards/*.mcd
   56  + /psx/duckstation/memcards/*.mcr
   57  + /dc/shared/savefiles/**
   58  + /psp/PPSSPP/**
   59  # PPSSPP mounts ms0 at psp; ordinary saves use PSP/SAVEDATA/<id>/.
   60  + /psp/PSP/SAVEDATA/**
   61  
   62  # Backup files
   63  + /backup/*.zip
   64  + /backup/*.tar.gz
   65  
   66  # Specifically exclude directories that should never be backed up
   67  - /roms/**
   68  - /bios/**
   69  - /downloads/**
   70  - /.cache/**
   71  - /images/**
   72  - /manuals/**
   73  - /videos/**
   74  - /themes/**
   75  - /**/*.bin
   76  - /**/*.iso
   77  - /**/*.img
   78  - /**/*.rom
   79  - /**/*.zip
   80  - /**/*.7z
   81  - /**/*.chd
   82  - /**/*.dol
   83  - /**/*.elf
   84  
   85  # Exclude XML files (like gamelist.xml) by default
   86  - /**/*.xml
   87  
   88  # Exclude everything else not explicitly included above
   89  - /**
```

## File: sources/cloud_sync-rules.txt.defaults (at 8ebaf8daad, 100 lines, whole)

```text
    1  # Cloud Sync Rules - Default Configuration
    2  #
    3  # These rules determine which files are included/excluded during cloud sync operations.
    4  # The syntax follows the same pattern as .gitignore, where:
    5  #   + pattern = explicitly include matching files/directories
    6  #   - pattern = explicitly exclude matching files/directories
    7  #
    8  # Rules are processed in order and THE FIRST MATCH WINS - a later rule cannot
    9  # override an earlier one. This is why the catch-all "- /**" sits at the very
   10  # bottom, and why an exclusion must appear ABOVE any include that would
   11  # otherwise match the same file.
   12  # Using /** matches files recursively through all subdirectories.
   13  
   14  # Databases and their sidecars, before anything else can include them.
   15  # A database is the one file a player cannot resolve by hand if two devices
   16  # both write it, and rclone replaces files wholesale rather than merging, so a
   17  # synced database loses one side's history outright. Copying one mid-write also
   18  # yields a torn file, and a .db separated from its -wal can lose recent writes
   19  # or refuse to open. Ours lives in /storage/.cache and is never synced; this
   20  # guards against one an emulator drops into a save directory.
   21  - /**/*.db
   22  - /**/*.db-wal
   23  - /**/*.db-shm
   24  - /**/*.db-journal
   25  - /**/*.sqlite
   26  - /**/*.sqlite3
   27  
   28  # Start by explicitly including directories we want to fully backup
   29  + /savefiles/**
   30  + /savestates/**
   31  + /screenshots/**
   32  
   33  # Include specific save file types across all directories
   34  + /**/*.srm
   35  + /**/*.sav
   36  + /**/*.fs
   37  + /**/*.state*
   38  + /**/*.auto
   39  + /**/*.dsv*
   40  
   41  # Standalone N64 saves sit BESIDE THE ROM, not in a save directory: every
   42  # shipped mupen64plus.cfg sets SaveSRAMPath = "/storage/roms/n64", so the
   43  # emulator writes n64/<Game>.eep, .mpk, .sra and .fla there. The
   44  # /n64/save/*.eep lines below match the libretro layout and have never
   45  # matched these, so a standalone N64 player's saves have never been backed
   46  # up on any device (#89, D-CLOUD-086). Widened here rather than in the
   47  # per-system block because the four extensions belong to no other system
   48  # and the same file can appear at either depth.
   49  + /**/*.eep
   50  + /**/*.mpk
   51  + /**/*.sra
   52  + /**/*.fla
   53  
   54  # Include system-specific save directories
   55  # Mupen64Plus writes slots 0-9 beside N64 ROMs (native or Project64).
   56  + /n64/*.st[0-9]
   57  + /n64/*.pj[0-9]
   58  + /n64/*.pj[0-9].zip
   59  + /n64/save/*.eep
   60  + /n64/save/*.mpk
   61  + /n64/save/*.sra
   62  + /n64/save/*.srm
   63  + /psx/memcards/*.mcd
   64  + /psx/memcards/*.mcr
   65  # DuckStation redirects its native memory-card directory here.
   66  + /psx/duckstation/memcards/*.mcd
   67  + /psx/duckstation/memcards/*.mcr
   68  + /dc/shared/savefiles/**
   69  + /psp/PPSSPP/**
   70  # PPSSPP mounts ms0 at psp; ordinary saves use PSP/SAVEDATA/<id>/.
   71  + /psp/PSP/SAVEDATA/**
   72  
   73  # Backup files
   74  + /backup/*.zip
   75  + /backup/*.tar.gz
   76  
   77  # Specifically exclude directories that should never be backed up
   78  - /roms/**
   79  - /bios/**
   80  - /downloads/**
   81  - /.cache/**
   82  - /images/**
   83  - /manuals/**
   84  - /videos/**
   85  - /themes/**
   86  - /**/*.bin
   87  - /**/*.iso
   88  - /**/*.img
   89  - /**/*.rom
   90  - /**/*.zip
   91  - /**/*.7z
   92  - /**/*.chd
   93  - /**/*.dol
   94  - /**/*.elf
   95  
   96  # Exclude XML files (like gamelist.xml) by default
   97  - /**/*.xml
   98  
   99  # Exclude everything else not explicitly included above
  100  - /**
```

## Excerpt: sources/cloud_backup (at 8ebaf8daad; 423 of 2510 lines: every line 02 and 04 cite, 8 lines either side, the head, the traps and main; a gap is marked ...)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # Script configuration and global variables
    6  SCRIPT_NAME=$(basename "$0")
    7  LOG_FILE="/var/log/cloud_sync.log"
    8  START_TIME=$(date +%s)
    9  
   10  # The two exits that mean "nothing ran", which EmulationStation names
   11  # (SKIPPED - ANOTHER CLOUD SYNC IS RUNNING / SKIPPED - NO NETWORK CONNECTION).
   12  # They were 3 and 4 until 2026-09-09 -- and rclone's own 3 and 4 are
   13  # "directory not found" and "file not found", so a failed phase carrying
   14  # rclone's code up to the final exit read as a sentinel nobody had raised: a
   15  # restore against a cloud with no Saves folder yet said a sync was running
   16  # (#99, blindspot 33). sysexits.h's EX_TEMPFAIL and EX_UNAVAILABLE sit above
   17  # everything rclone returns (0-9) and below the 128+signal range, so nothing
   18  # this script forwards can produce them. EmulationStation reads the same two
   19  # numbers; scripts and ES ship in one image.
   20  readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69
   21  
   22  # The bound on a reachability probe: one attempt, 10 s to connect, 20 s in
   23  # all. Tighter than the transfers' bound below, because a probe is a single
   24  # listing whose whole point is to answer quickly. Used by check_internet,
   25  # by the mkdir that doubles as the pre-run probe, and by
   26  # network_lost_during_run after a failure.
   27  readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
   28  # A listing's bound (#143). rclone's S3 backend hands --low-level-retries to
   29  # the AWS SDK as its number of attempts, with the SDK's exponential backoff
   30  # between them, and --contimeout never enters it: a refused endpoint costs
   31  # 0.03 s at 1 attempt, 2 s at 2, 6 s at 3 and 230 s at 10 (rclone 1.75 on
   32  # the VM, 2026-09-12). Ten is right for a write -- Dropbox answers a
   33  # concurrent write with a lock error a retry clears (#107) -- and wrong for
   34  # a listing, which has nothing to clear. Three covers a rate-limit answer
   35  # and keeps a dead endpoint under ten seconds on every backend.
   36  readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
   37  
   38  # What bounds every other rclone command this script runs against the cloud
   39  # -- the transfers, the listings, the archive upload and its size check.
   40  # The value is RCLONE_NET_OPTS in cloud_sync.conf (the reasoning for the
   41  # numbers is beside it in cloud_sync.conf.defaults), seeded there by
   42  # cloud_sync_helper; load_config turns it into RCLONE_NET_OPTS_ARRAY. This
   43  # is the same value for a config the helper has not reached -- the helper
   44  # binary missing, the line blanked -- so the bound holds on the first run
   45  # after an update too. Until 2026-09-09 only the probes were bounded and
   46  # every transfer ran on rclone's defaults: a 60 s connect timeout, a 5 min
   47  # idle timeout, 10 low-level retries, 3 whole-run retries. A link that
   48  # dropped mid-run held the process for over ten minutes, and on the RG SP
   49  # that froze the startup card at 113/113 with the launch gate held (#101,
   50  # #102, #103). Keep the two values in step.
   51  RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
   52  # The automatic sync's bound (D-CLOUD-118), appended after the caller's flags
   53  # by the rclone() wrapper below; the ceiling is enforced by timeout. The two
   54  # are RCLONE_SYNC_NET_OPTS and SYNC_CEILING_SECONDS in cloud_sync.conf, and
   55  # these are the same values for a config the helper has not reached.
   56  RCLONE_SYNC_NET_OPTS_FALLBACK="--contimeout 5s --timeout 5s --retries 1 --max-duration 90s --low-level-retries 5 --transfers 1"
   57  SYNC_CEILING_SECONDS_FALLBACK=90
   58  RCLONE_NET_OPTS_ARRAY=()
   59  
   60  # Non-interactive support for hooks and the ES menu:
   61  #   --yes / -y      answer prompts automatically (headless mode)
   62  #   --method=X      override the configured transfer method (sync or copy)
   63  #   --update        add rclone --update (skip files newer on the destination)
   64  #   --system-only   only the system-settings archive, not the saves
   65  #   --saves-only    only the saves, not the system-settings archive
   66  #   --recent        only saves changed since the last backup that worked
   67  #                   (the game-exit sync); always copies, never tidies
   68  #
   69  # Exit codes the UI names: EXIT_LOCK_HELD (75) = skipped, another cloud sync
   70  # holds the lock; EXIT_NO_NETWORK (69) = skipped, no network. Neither writes a
   71  # last-run stamp -- nothing ran. Defined below, with why those two numbers.
   72  ASSUME_YES=0
   73  METHOD_OVERRIDE=""
   74  EXTRA_UPDATE=0
   75  SYSTEM_ONLY=0
   76  # The settings phase's own summary word when it is not the exit code's
   77  # (SKIPPED - NOTHING TO SEND YET), and whether a --system-only run did any
   78  # work at all -- when it did not, the settings stamp is not rewritten (#126).
   79  SETTINGS_OUTCOME=""
   80  SETTINGS_NOTHING_RAN=0
   81  # The saves phase's, for the same reason: under --system-only the phase is
   82  # skipped, and its summary line said COMPLETED for work that was never run.
   83  SAVES_OUTCOME=""
   84  SAVES_ONLY=0
   85  # --automatic: this run is the startup sync or the sync after a game, not a
   86  # back up or restore somebody pressed (D-CLOUD-113). A player is waiting to
   87  # play, so the run is bounded the way #135 measured it should be (D-CLOUD-118):
   88  # connect in 5 s, give a stalled transfer up after 5 s with nothing moving,
   89  # and never run past SYNC_CEILING_SECONDS in all -- against a cloud that
   90  # accepts and never answers the unbounded run took 321 s, with the outcome
   91  # landing behind the screensaver. The bound is applied here, on every rclone
   92  # this script runs: RCLONE_SYNC_NET_OPTS goes last on the command line so it
   93  # outranks the caller's bound, and busybox timeout enforces the ceiling on
   94  # what rclone's own flags cannot reach (a stalled listing retried ten times).
   95  # The low-level retry count is left to the caller's: ten for a transfer,
   96  # because Dropbox answers concurrent writes with a lock error that a retry
   97  # clears (#107), and the ceiling -- not the retries -- is what bounds a stall.
   98  # A run the ceiling ends returns 124 (timeout) or 10 (rclone's own
   99  # --max-duration); why_for says what that means to the player.
  100  AUTOMATIC=0
  101  SYNC_DEADLINE=0
  102  RCLONE_SYNC_NET_OPTS_ARRAY=()
  103  RECENT=0
  104  for CLI_ARG in "$@"; do
  105      case "${CLI_ARG}" in
  106          --yes|-y) ASSUME_YES=1 ;;
  107          --method=sync|--method=copy) METHOD_OVERRIDE="${CLI_ARG#--method=}" ;;
  108          --method=*) echo "Ignoring invalid --method value: ${CLI_ARG#--method=}" ;;
  109          --update) EXTRA_UPDATE=1 ;;
  110          --system-only) SYSTEM_ONLY=1 ;;
  111          --saves-only) SAVES_ONLY=1 ;;
  112          --recent) RECENT=1 ;;
  113          --automatic) AUTOMATIC=1 ;;
  114      esac
  115  done
  116  
  117  # Every rclone this script runs goes through the rclone() function below:
  118  # the automatic run's bound on one branch, the deliberate run's on the
  119  # other (D-CLOUD-126, #153). The function and its helpers sit at column 0
  120  # so tools/last-good-scripts-test can lift them by their first lines.
  ...
  349      local now
  350      {
  351          now=$(stat -c %s "${LOG_FILE}" 2>/dev/null) && [ "${now}" -gt "$1" ] 2>/dev/null \
  352              && tail -c +$(( $1 + 1 )) "${LOG_FILE}" 2>/dev/null
  353          [ -n "${2:-}" ] && cat "$2" 2>/dev/null
  354      } | grep -qE ': (Copied|Moved) \(|: Deleted$'
  355  }
  356  
  357  rclone() {
  358      if [ "${AUTOMATIC}" -eq 1 ]; then
  359          if [ "${SYNC_DEADLINE}" -gt 0 ]; then
  360              local left=$(( SYNC_DEADLINE - $(date +%s) ))
  361              # Past the ceiling nothing more is started (#308 gpt F-CS-34): each
  362              # call used to be given a second more and three to die in, so a
  363              # run that met its ceiling went on for as many seconds again as it
  364              # had calls left -- the probe that words the failure, the tidy.
  365              # The call's answer is the ceiling's own, 124.
  366              if [ "${left}" -lt 1 ]; then
  367                  log_message "rclone $1 not started: the automatic ceiling had passed" "false"
  368                  return 124
  369              fi
  370              local log0 rc
  371              log0=$(stat -c %s "${LOG_FILE}" 2>/dev/null || echo 0)
  372              command timeout -k 3 "${left}" rclone "$@" "${RCLONE_SYNC_NET_OPTS_ARRAY[@]}"; rc=$?
  373              logged_moved "${log0}" && RCLONE_MOVED=1
  374              return "${rc}"
  375          else
  376              command rclone "$@"
  377          fi
  378      elif [ -n "${RCLONE_OUTER}" ]; then
  379          "${RCLONE_OUTER}" "$@"
  380      else
  381          bounded_rclone "$@"
  382      fi
  383  }
  384  
  385  # The pauses between sections give somebody reading the console time to see
  ...
  449  # does mark close-on-exec, and nothing this script starts can see it.
  450  #
  451  # The refusal also waits a moment before saying no, as belt and braces for
  452  # a holder this script does not own: a descriptor leaked by an older build,
  453  # or a process in the act of exiting, frees itself in milliseconds, while a
  454  # real concurrent transfer does not. One second of patience turns a raced
  455  # skip into a run that works and costs a genuinely blocked run one second.
  456  CLOUD_SYNC_LOCK=/var/run/cloud_sync.lock
  457  take_cloud_lock() {
  458      local tries=0
  459      exec 9>"${CLOUD_SYNC_LOCK}"
  460      while ! flock -n 9; do
  461          if [ "${tries}" -ge 4 ]; then
  462              echo "Skipped: another cloud sync is already running. Try again when it's done."
  463              log_message "skipped: another cloud sync holds ${CLOUD_SYNC_LOCK}" "false"
  464              exit "${EXIT_LOCK_HELD}"
  465          fi
  ...
  708          || rm -f "${tmp}" 2>/dev/null
  709  }
  710  
  711  # The stamp's third field: why the run did not finish, as the token the
  712  # menu row reads back (D-UI-028) -- the >>> why sentence with its spaces as
  713  # underscores, so a reader that splits on spaces still gets one field.
  714  # Nothing when the run completed, or ended on a sentinel the reader names
  715  # itself.
  716  record_last_run() {
  717      local exit_code="$1"
  718      local name="backup" why=""
  719      [ "${SYSTEM_ONLY}" -eq 1 ] && name="settings-backup"
  720      # A settings-only run that found nothing to send ran nothing; the stamp
  721      # keeps describing the last upload that happened (#126).
  722      if [ "${SYSTEM_ONLY}" -eq 1 ] && [ "${SETTINGS_NOTHING_RAN}" -eq 1 ]; then
  723          return 0
  724      fi
  ...
 1201      log_message "Loading configuration from cloud_sync.conf" "false"
 1202      # A config that does not parse is not run with. `source` used to be
 1203      # unchecked, so a torn file -- a partial trailing line -- was read up to
 1204      # the tear and the run went on with whatever was missing (SAVES_REMOTE
 1205      # unset means remote:/). The helper's copy from before this run's
 1206      # update is the fallback; with no good copy the run refuses and says so
 1207      # (D-CLOUD-078, #105).
 1208      local conf="/storage/.config/cloud_sync.conf"
 1209      if ! conf_valid "${conf}"; then
 1210          # Which line, and what about it -- never the value (PL-015).
 1211          log_message "cloud_sync.conf is not run with: ${CONF_WHY}" "false" "WARN"
 1212          if [ -f "${conf}.bak" ] && conf_valid "${conf}.bak"; then
 1213              log_message "cloud_sync.conf does not parse; putting back the copy taken before this run's update" "false" "WARN"
 1214              cp -f "${conf}.bak" "${conf}.tmp.$$" && mv -f "${conf}.tmp.$$" "${conf}"
 1215          else
 1216              rm -f "${conf}.tmp.$$" 2>/dev/null
 1217              log_message "Your cloud sync settings couldn't be read, and there's no good copy to fall back on.\nNothing was changed. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE." "true" "ERROR"
 1218              say_why "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
 1219              clean_exit 1
 1220          fi
 1221      fi
 1222      if ! source "${conf}"; then
 1223          log_message "Your cloud sync settings couldn't be read. Nothing was changed.\nSet up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE." "true" "ERROR"
 1224          say_why "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
 1225          clean_exit 1
 1226      fi
 1227  
 1228      # Saves have one local folder (D-CLOUD-040). RESTOREPATH used to let a
 1229      # restore land somewhere other than the live saves -- a safety valve from
 1230      # when restore was a mirror. A config still pointing it elsewhere would
  ...
 1395          sync_opts=$(echo "${RCLONE_SYNC_NET_OPTS:-}" | tr '\n\\' '  ' | tr -s ' ' | sed 's/^ //; s/ $//')
 1396          [ -n "${sync_opts}" ] || sync_opts="${RCLONE_SYNC_NET_OPTS_FALLBACK}"
 1397          RCLONE_SYNC_NET_OPTS_ARRAY=()
 1398          for opt in ${sync_opts}; do
 1399              RCLONE_SYNC_NET_OPTS_ARRAY+=("$opt")
 1400          done
 1401          ceiling="${SYNC_CEILING_SECONDS:-}"
 1402          [[ "${ceiling}" =~ ^[0-9]+$ ]] && [ "${ceiling}" -ge 1 ] || ceiling="${SYNC_CEILING_SECONDS_FALLBACK}"
 1403          SYNC_DEADLINE=$(( START_TIME + ceiling ))
 1404          log_message "automatic run: ${sync_opts}; ceiling ${ceiling}s from start" "false"
 1405      fi
 1406  
 1407      # Apply command-line overrides
 1408      if [ "${SYSTEM_ONLY}" -eq 1 ]; then
 1409          BACKUPFILE_BACKUP_OPTION="yes"
 1410          log_message "System-backup phase forced on by --system-only" "false"
 1411      fi
  ...
 1531      local stderr_file="/tmp/rclone_stderr_$$"
 1532      
 1533      # Execute rclone with real-time progress display
 1534      # stdout goes to terminal (shows progress), stderr goes to temp file for logging
 1535      rclone "${method}" "${extra_opts[@]}" "${RCLONE_NET_OPTS_ARRAY[@]}" "${source}" "${dest}" 2>"$stderr_file"
 1536      local rclone_exit_code=$?
 1537      # With no --log-file in the options rclone's own lines, the ones that
 1538      # say what moved, are on stderr (claude G-A-01).
 1539      logged_moved "$(stat -c %s "${LOG_FILE}" 2>/dev/null || echo 0)" "$stderr_file" && RCLONE_MOVED=1
 1540      
 1541      # Log any stderr output for debugging
 1542      if [ -s "$stderr_file" ]; then
 1543          while IFS= read -r line; do
 1544              log_message "rclone stderr: $line" "false"
 1545          done < "$stderr_file"
 1546      fi
 1547      
  ...
 1558  # is not age: a folder from a device whose clock runs ahead, or from this
 1559  # one before its clock was corrected, sorted after this run's, and "keep the
 1560  # newest by name" purged the record this run had just written (audit #307
 1561  # PL-021). When this run replaced nothing it wrote no folder, nothing is
 1562  # superseded, and the newest by name is kept as before. The root not
 1563  # existing, or not listing, removes nothing.
 1564  prune_replaced_remote() {
 1565      local root="$1" pinned="$2" names doomed d
 1566      names=$(rclone lsf --dirs-only "${root}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | tr -d '/' | grep .)
 1567      if [ -n "${pinned}" ] && printf '%s\n' "${names}" | grep -qxF -- "${pinned}"; then
 1568          doomed=$(printf '%s\n' "${names}" | grep -vxF -- "${pinned}")
 1569      else
 1570          doomed=$(printf '%s\n' "${names}" | sort -r | tail -n +2)
 1571      fi
 1572      printf '%s\n' "${doomed}" | while read -r d; do
 1573          [ -n "${d}" ] || continue
 1574          log_message "removing replaced-saves folder ${root}/${d} (superseded)" "false"
  ...
 1605          # confirmed, or the reason it refused.
 1606          if ! saves_root_id=$("${saves_root_tool}" check --wait 15); then
 1607              relay_refusal "${saves_root_id}"
 1608              return 1
 1609          fi
 1610      fi
 1611      
 1612      # Check if local backup path exists and has content
 1613      if [ ! -d "${SAVESPATH}" ]; then
 1614          log_message "the saves folder ${SAVESPATH} is not on this device" "false" "ERROR"
 1615          log_message "Your saves folder isn't on this device." "true" "ERROR"
 1616          say_why "YOUR SAVES FOLDER ISN'T ON THIS DEVICE"
 1617          return 1
 1618      fi
 1619      
 1620      # Check if we have any files to backup (excluding directories we'll skip anyway)
 1621      local files_to_backup=$(find "${SAVESPATH}" -type f ! -path "*/bios/*" ! -path "*/backups/*" ! -name "*.zip" ! -name "*.tar.gz" | head -1)
  ...
 1798      # own layouts -- PPSSPP by game ID, Dreamcast in a shared VMU folder --
 1799      # and a filter on the ROM's name would miss every one of them.
 1800      #
 1801      # Full passes still happen: the boot sync and the menu rows. A file with
 1802      # a wrong mtime -- written before the clock was set, on a device with no
 1803      # RTC -- is caught there. And --recent always copies: a filtered sync
 1804      # would weigh deleting whatever the filter hid.
 1805      if [ "${RECENT}" -eq 1 ]; then
 1806          local stamp_file=/storage/.cache/cloud_sync/last-backup
 1807          local stamp_epoch="" stamp_rc="" now
 1808          now=$(date +%s)
 1809          [ -r "${stamp_file}" ] && read -r stamp_epoch stamp_rc < "${stamp_file}"
 1810          if [ "${stamp_rc}" = "0" ] && [ "${stamp_epoch:-0}" -gt 0 ] 2>/dev/null \
 1811             && [ "${stamp_epoch}" -le "${now}" ]; then
 1812              local age=$(( now - stamp_epoch + 600 ))
 1813              all_opts+=("--max-age" "${age}s" "--no-traverse")
 1814              log_message "recent: only files changed in the last ${age}s, since the last successful backup" "false"
  ...
 2020          log_message "Sending your settings backup to the cloud..." "true"
 2021          log_message "Settings backup file transfer started at $(date)" "false"
 2022          
 2023          # Test remote backup path connectivity
 2024          log_message "Testing remote backup path connectivity: ${device_dest}" "false"
 2025          rclone mkdir "${device_dest}/" "${RCLONE_NET_OPTS_ARRAY[@]}" 2>/dev/null
 2026          local mkdir_status=$?
 2027          if [ $mkdir_status -ne 0 ]; then
 2028              network_lost_during_run "$mkdir_status" "the settings backup"
 2029              log_message "Couldn't reach your settings folder in the cloud." "true" "ERROR"
 2030              report_rclone_error $mkdir_status "Reaching your settings folder"
 2031              return $mkdir_status
 2032          fi
 2033          
 2034          # No --filter-from here on purpose. The saves allowlist is anchored to
 2035          # SAVESPATH, but this transfer's root is SETTINGS_BACKUPS, so its rules
 2036          # describe paths that do not exist in this tree -- and its "- /**/*.zip"
 2037          # matches the archive itself. This phase only ever kept working because
 2038          # rclone applies --include ahead of --filter-from; borrowing the rules
  ...
 2046          local backup_opts=(
 2047              "--progress"
 2048              "--log-file" "/var/log/cloud_sync.log"
 2049              "--include=/*.{zip,tar.gz}"
 2050              "--stats" "1s"
 2051          )
 2052  
 2053          # Check if the rclone version supports the terminal width flag
 2054          if rclone help | grep -q progress-terminal-width; then
 2055              backup_opts+=("--progress-terminal-width=80")
 2056          fi
 2057          
 2058          # rclone decides whether to send a file by comparing it with the one
 2059          # already there. Given neither modification times nor hashes it falls
 2060          # back to size alone, and plenty of remotes offer neither -- a WebDAV
 2061          # server commonly reports `Precision` unsupported and `Hashes: []`.
 2062          #
 2063          # The archive is ~17 MB of OS-shipped assets wrapped around a few KB of
 2064          # configuration, so its size barely moves when settings change:
  ...
 2106          local archives=()
 2107          local a
 2108          for a in "${SETTINGS_BACKUPS}"/*.zip "${SETTINGS_BACKUPS}"/*.tar.gz; do
 2109              [ -f "${a}" ] && archives+=("${a}")
 2110          done
 2111          if [ ${#archives[@]} -gt 0 ]; then
 2112              # Hash of the members' hashes, so more than one archive at the
 2113              # root is still covered by a single comparison.
 2114              local_sum=$(md5sum "${archives[@]}" 2>/dev/null | md5sum | cut -d' ' -f1)
 2115              local_bytes=$(cat "${archives[@]}" 2>/dev/null | wc -c)
 2116          fi
 2117          if [ -f "${uploaded_marker}" ]; then
 2118              last_sum=$(cat "${uploaded_marker}" 2>/dev/null)
 2119          fi
 2120  
 2121          if [ -n "${local_sum}" ] && [ "${local_sum} ${device_dest}" = "${last_sum}" ]; then
 2122              # Say what is true. Reporting a transfer that did not happen is
 2123              # how the stale-copy bug stayed invisible.
 2124              log_message "Settings backup is unchanged since the last upload to ${device_dest}; nothing to send" "false"
 2125              log_message "Your settings backup hasn't changed since the last one, so there's nothing to send." "true"
 2126              BACKUP_SYSTEM_STATUS=0
  ...
 2162                  --include|--exclude|--filter|--filter-from)
 2163                      skip_next=1; continue ;;
 2164                  --include=*|--exclude=*|--filter*) continue ;;
 2165                  # The guard that adds this greps `rclone help`, which mentions
 2166                  # the flag on builds that do not accept it -- so it reaches the
 2167                  # command line and rclone exits with "unknown flag", having
 2168                  # transferred nothing while the run still reported success. It
 2169                  # only shapes the progress display, so nothing is lost here.
 2170                  --progress-terminal-width*) continue ;;
 2171              esac
 2172              copy_opts+=("${opt}")
 2173          done
 2174  
 2175          local stamp
 2176          stamp=$(date +%Y_%m_%d-%H%M%S)
 2177          BACKUP_SYSTEM_STATUS=0
 2178          local sent_any=0
 2179          # What this run actually put there, so the check afterwards measures
 2180          # those and not the whole history beside them.
 2181          local uploaded_names=()
  ...
 2295              done
 2296              [ ${checked} -eq 1 ] || remote_bytes=""
 2297              # Nothing came back at all: the check itself could not reach the
 2298              # cloud, which after a finished upload most likely means the link
 2299              # went in between. The marker stays unwritten either way -- the
 2300              # upload is unconfirmed -- and the run says why it ended.
 2301              [ -n "${remote_bytes}" ] || network_lost_during_run 1 "the settings backup's size check"
 2302              if [ -n "${remote_bytes}" ] && [ "${remote_bytes}" = "${local_bytes}" ]; then
 2303                  write_stamp "${uploaded_marker}" "${local_sum} ${device_dest}"
 2304              else
 2305                  log_message "the cloud copy is ${remote_bytes:-none} bytes against the ${local_bytes} sent; it will be sent again next time" "false" "WARN"
 2306                  log_message "The copy in your cloud isn't complete. Nothing was lost - it'll be sent again next time." "true" "WARN"
 2307                  say_why "THE COPY IN YOUR CLOUD ISN'T COMPLETE"
 2308                  BACKUP_SYSTEM_STATUS=1
 2309              fi
 2310          fi
 2311  
  ...
 2490      
 2491      # Both phases decide the exit. It was the saves phase's alone -- "use the
 2492      # game saves backup status as the overall exit code", from when this was
 2493      # a console tool with one phase that mattered -- so a settings upload
 2494      # that failed exited 0, and under --system-only, where the saves phase
 2495      # is skipped and reports 0, every failure did: the card said COMPLETED
 2496      # SUCCESSFULLY and last-settings-backup recorded 0 for an archive that
 2497      # never arrived (found while bounding the runs, #103). A run is good when
 2498      # every phase it ran is; otherwise it carries the first failing phase's
 2499      # code, the saves phase's when both failed.
 2500      clean_exit ${overall}
 2501  }
 2502  
 2503  # Set up signal trap to handle user interruption gracefully
 2504  trap 'log_message "Script interrupted by user" "false" "WARN"; clean_exit 130' INT TERM
 2505  
 2506  # Start script execution. The body runs with the lock descriptor closed,
 2507  # so nothing it starts can hold the lock after this shell is gone -- see
 2508  # take_cloud_lock.
 2509  take_cloud_lock
 2510  main 9>&-
```

## Excerpt: sources/cloud_restore (at 8ebaf8daad; 658 of 2324 lines: every line 02 and 04 cite, 8 lines either side, the head, the traps and main; a gap is marked ...)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # Script configuration and global variables
    6  SCRIPT_NAME=$(basename "$0")
    7  LOG_FILE="/var/log/cloud_sync.log"
    8  START_TIME=$(date +%s)
    9  
   10  # The exit that means "nothing ran: another cloud sync holds the lock", which
   11  # EmulationStation names (SKIPPED - ANOTHER CLOUD SYNC IS RUNNING). It was 3
   12  # until 2026-09-09 -- and rclone's own 3 is "directory not found", so a
   13  # restore whose saves phase met a cloud with no Saves folder yet carried
   14  # rclone's code to the final exit and the page said a sync was running (#99,
   15  # blindspot 33). sysexits.h's EX_TEMPFAIL sits above everything rclone
   16  # returns (0-9) and below the 128+signal range, so nothing this script
   17  # forwards can produce it. The no-network exit is 69 (EX_UNAVAILABLE) by the
   18  # same rule -- raised by check_network_link before a run and by
   19  # network_lost_during_run after a failed one, as in cloud_backup;
   20  # EmulationStation reads both, and scripts and ES ship in one image.
   21  readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69
   22  
   23  # The bound on a reachability probe: one attempt, 10 s to connect, 20 s in
   24  # all. Tighter than the transfers' bound below, because a probe is a single
   25  # listing whose whole point is to answer quickly. Used by check_internet and
   26  # by network_lost_during_run after a failure.
   27  readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
   28  # A listing's bound (#143). rclone's S3 backend hands --low-level-retries to
   29  # the AWS SDK as its number of attempts, with the SDK's exponential backoff
   30  # between them, and --contimeout never enters it: a refused endpoint costs
   31  # 0.03 s at 1 attempt, 2 s at 2, 6 s at 3 and 230 s at 10 (rclone 1.75 on
   32  # the VM, 2026-09-12). Ten is right for a write -- Dropbox answers a
   33  # concurrent write with a lock error a retry clears (#107) -- and wrong for
   34  # a listing, which has nothing to clear. Three covers a rate-limit answer
   35  # and keeps a dead endpoint under ten seconds on every backend.
   36  readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
   37  
   38  # What bounds every other rclone command this script runs against the cloud
   39  # -- the transfers, the listings, the archive download. The value is
   40  # RCLONE_NET_OPTS in cloud_sync.conf (the reasoning for the numbers is
   41  # beside it in cloud_sync.conf.defaults), seeded there by cloud_sync_helper;
   42  # load_config turns it into RCLONE_NET_OPTS_ARRAY. This is the same value
   43  # for a config the helper has not reached -- the helper binary missing, the
   44  # line blanked -- so the bound holds on the first run after an update too.
   45  # Until 2026-09-09 only the probe was bounded and every transfer ran on
   46  # rclone's defaults: a 60 s connect timeout, a 5 min idle timeout, 10
   47  # low-level retries, 3 whole-run retries. A link that dropped mid-run held
   48  # the process for over ten minutes, and on the RG SP that froze the startup
   49  # card at 113/113 with the launch gate held (#101, #102, #103). Keep the two
   50  # values in step.
   51  RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
   52  # The automatic sync's bound (D-CLOUD-118), appended after the caller's flags
   53  # by the rclone() wrapper below; the ceiling is enforced by timeout. The two
   54  # are RCLONE_SYNC_NET_OPTS and SYNC_CEILING_SECONDS in cloud_sync.conf, and
   55  # these are the same values for a config the helper has not reached.
   56  RCLONE_SYNC_NET_OPTS_FALLBACK="--contimeout 5s --timeout 5s --retries 1 --max-duration 90s --low-level-retries 5 --transfers 1"
   57  SYNC_CEILING_SECONDS_FALLBACK=90
   58  RCLONE_NET_OPTS_ARRAY=()
   59  
   60  # Non-interactive support for hooks and the ES menu:
   61  #   --yes / -y   answer prompts automatically (headless mode)
   62  #   --method=X   override the configured transfer method (sync or copy)
   63  #   --update     add rclone --update (skip files newer on the destination)
   64  ASSUME_YES=0
   65  METHOD_OVERRIDE=""
   66  EXTRA_UPDATE=0
   67  SYSTEM_ONLY=0
   68  # A skipped phase's own summary word, where the exit code's would say
   69  # COMPLETED for work that was never run (#126 in cloud_backup; #308 claude
   70  # F-CS-04 here).
   71  SAVES_OUTCOME=""
   72  SETTINGS_OUTCOME=""
   73  # --automatic: this run is the startup sync or the sync after a game, not a
   74  # back up or restore somebody pressed (D-CLOUD-113). A player is waiting to
   75  # play, so the run is bounded the way #135 measured it should be (D-CLOUD-118):
   76  # connect in 5 s, give a stalled transfer up after 5 s with nothing moving,
   77  # and never run past SYNC_CEILING_SECONDS in all -- against a cloud that
   78  # accepts and never answers the unbounded run took 321 s, with the outcome
   79  # landing behind the screensaver. The bound is applied here, on every rclone
   80  # this script runs: RCLONE_SYNC_NET_OPTS goes last on the command line so it
   81  # outranks the caller's bound, and busybox timeout enforces the ceiling on
   82  # what rclone's own flags cannot reach (a stalled listing retried ten times).
   83  # The low-level retry count is left to the caller's: ten for a transfer,
   84  # because Dropbox answers concurrent writes with a lock error that a retry
   85  # clears (#107), and the ceiling -- not the retries -- is what bounds a stall.
   86  # A run the ceiling ends returns 124 (timeout) or 10 (rclone's own
   87  # --max-duration); why_for says what that means to the player.
   88  AUTOMATIC=0
   89  SYNC_DEADLINE=0
   90  RCLONE_SYNC_NET_OPTS_ARRAY=()
   91  SAVES_ONLY=0
   92  for CLI_ARG in "$@"; do
   93      case "${CLI_ARG}" in
   94          --yes|-y) ASSUME_YES=1 ;;
   95          --method=sync|--method=copy) METHOD_OVERRIDE="${CLI_ARG#--method=}" ;;
   96          --method=*) echo "Ignoring invalid --method value: ${CLI_ARG#--method=}" ;;
   97          --update) EXTRA_UPDATE=1 ;;
   98          --system-only) SYSTEM_ONLY=1 ;;
   99          --saves-only) SAVES_ONLY=1 ;;
  100          --automatic) AUTOMATIC=1 ;;
  101      esac
  102  done
  103  
  104  # Every rclone this script runs goes through the rclone() function below:
  105  # the automatic run's bound on one branch, the deliberate run's on the
  106  # other (D-CLOUD-126, #153). The function and its helpers sit at column 0
  107  # so tools/last-good-scripts-test can lift them by their first lines.
  108  #
  109  # An rclone function the environment exported -- the round-trip harness's
  110  # lock-descriptor probe does exactly that, to count what a child of a run
  111  # can see -- used to reach a deliberate run unwrapped, because no function
  112  # was defined for one. It still runs: it is kept under another name and
  113  # the deliberate branch calls it in place of the binary, in the foreground.
  114  # A shell function cannot be ended the way a process can, and the only
  115  # environments that export one are harnesses.
  116  RCLONE_OUTER=""
  117  if declare -F rclone >/dev/null 2>&1; then
  118      eval "outer_$(declare -f rclone)"
  119      RCLONE_OUTER=outer_rclone
  120  fi
  121  
  122  # The deliberate run's ceiling (D-CLOUD-126, #153). RCLONE_NET_OPTS bounds
  123  # a dead link with --timeout 30s, rclone's idle limit: nothing moved for
  124  # that long, the connection is dropped and the operation retried. On the
  125  # path-based backends a retry against a dead link fails at once and the
  126  # run ends inside the outage, exit 69. rclone's S3 backend hands
  127  # --low-level-retries to the AWS SDK as its attempt count, and the SDK
  128  # backs off exponentially between attempts with no timeout of ours in the
  129  # way (the note beside RCLONE_LIST_OPTS: 230 s at ten). So a deliberate
  130  # `cloud_backup --system-only` whose link dropped sat through the outage,
  131  # re-dialled when the link came back, uploaded the whole archive again and
  132  # exited 0 -- 88.8 s after a 40 s cut, 163.6 s after a 120 s one -- past
  133  # the 90 s tools/cloud-round-trip's LINK cells hold every run to, and
  134  # stamped success for a run the network had left (LINK5 on MinIO,
  135  # 2026-09-13). --low-level-retries itself is not the knob (D-CLOUD-083).
  136  #
  137  # The ceiling is the automatic run's mechanism -- end the process, return
  138  # 124 -- measured differently. The automatic run is bounded from its
  139  # start, because a player is waiting to play and the run is small by
  140  # construction. A deliberate run is the one that moves a first backup of
  141  # every save state, or a settings archive carrying a theme pack, so a
  142  # ceiling from its start would end exactly the transfers it exists for.
  143  # This one is measured from the last moment rclone made progress: the
  144  # byte, check, file or delete count in its own stats block exceeding what
  145  # it had reached before. The block goes to stdout under --progress and is
  146  # copied to a trace on its way through; rclone's transferred count never
  147  # falls on a retry, only its total grows (the LINK5 capture shows
  148  # 8.902 MiB standing for 45 s under a total that went from 12.0 to
  149  # 20.9 MiB), so a count above its previous high is progress and nothing
  150  # else is. A transfer that keeps moving is never ended; one that has moved
  151  # nothing for the idle timeout plus a grace is. The grace gives a healthy
  152  # link's retry after the idle timeout time to show progress -- the SDK's
  153  # first backoffs are a second or two -- and stays short enough that a run
  154  # whose link is down ends before an outage of the LINK cells' shape is
  155  # over, with the link still down, exit 69 like the other backends.
  156  # load_config sizes the ceiling from RCLONE_NET_OPTS; the value here is
  157  # for a config the helper has not reached. Calls that print no stats block
  158  # -- a mkdir, a size, a deletefile, each carrying the transfer's ten
  159  # retries -- are bounded from their start by the same figure, which is
  160  # what they need.
  ...
  238  bounded_rclone() {
  239      local dir="${CEILING_DIR_ROOT}/cloud_sync.${$}.${RANDOM}" fifo trace pid tee_pid rc
  240      local mark high="0 0 0 0 0" new since now ticks=0 ended=0 n progress_verb=0
  241      if ! mkdir -p "${dir}" 2>/dev/null || ! mkfifo "${dir}/fifo" 2>/dev/null; then
  242          # Nowhere to trace through. On a device /var/run is tmpfs and this
  243          # does not happen; when it does, the call runs as it did before the
  244          # ceiling and the log says so -- a backup refused for want of a
  245          # fifo would be the worse failure.
  246          log_message "cannot make ${dir}/fifo; rclone $1 runs without the stall ceiling" "false" "WARN"
  247          rm -rf "${dir}" 2>/dev/null
  248          command rclone "$@"
  249          return
  250      fi
  251      fifo="${dir}/fifo"; trace="${dir}/trace"
  252      : > "${trace}"
  253      local -a args=("$@")
  254      case "$1" in
  255          copy|copyto|sync|move|moveto)
  256              progress_verb=1
  257              local has_progress=0 a
  258              for a in "$@"; do
  259                  case "${a}" in --progress|-P) has_progress=1 ;; esac
  260              done
  261              [ "${has_progress}" -eq 1 ] || args+=(--progress) ;;
  262      esac
  263      tee -a "${trace}" < "${fifo}" &
  264      tee_pid=$!
  265      command rclone "${args[@]}" > "${fifo}" &
  266      pid=$!
  267      RCLONE_CHILD="${pid}"
  268      since=$(date +%s)
  269      while child_running "${pid}"; do
  270          sleep 0.25
  271          ticks=$((ticks + 1))
  272          [ $((ticks % 4)) -eq 0 ] || continue
  273          mark=$(progress_mark "${trace}")
  274          if new=$(advance_mark "${mark}" "${high}"); then
  275              high="${new}"
  276              since=$(date +%s)
  277              continue
  278          fi
  279          now=$(date +%s)
  280          if [ $((now - since)) -ge "${DELIBERATE_CEILING_SECONDS}" ]; then
  281              ended=1
  282              kill -TERM "${pid}" 2>/dev/null
  283              # Three seconds to go, as timeout -k 3 gives the automatic run.
  284              n=0
  285              while [ "${n}" -lt 30 ] && child_running "${pid}"; do sleep 0.1; n=$((n + 1)); done
  286              kill -KILL "${pid}" 2>/dev/null
  287              break
  288          fi
  289      done
  290      wait "${pid}" 2>/dev/null; rc=$?
  291      RCLONE_CHILD=""
  292      # tee ends when the fifo's last writer has gone. rclone starts no
  293      # children; a shim under test might leave one holding the fifo, so tee
  294      # gets the same three seconds and is then ended too.
  295      n=0
  296      while [ "${n}" -lt 30 ] && child_running "${tee_pid}"; do sleep 0.1; n=$((n + 1)); done
  297      kill -KILL "${tee_pid}" 2>/dev/null
  298      wait "${tee_pid}" 2>/dev/null
  299      # rclone ends each redraw of its stats block on a " * file" line with no
  300      # newline (the rule's "Progress output"), so a transfer ended inside a
  301      # redraw -- the ceiling's kill lands there -- leaves that line open on
  302      # the stream, and the sentence the caller prints next is glued to it:
  303      # " * ...SETTINGS.tar.gz:  0% / 12.011 MiB, 0 B/s, -Couldn't finish:
  304      # lost the network during the settings backup." (LINK5 on MinIO,
  305      # 4d7eb1f303, 2026-09-13). Every reader that takes the stream by lines
  306      # -- the card, the page, the round-trip's outcome gate -- then sees
  307      # rclone's line and never the outcome. When the block was left open,
  308      # close it; only on the verbs whose stdout is the block, so a listing
  309      # the caller captures is handed over byte for byte. A block that ended
  310      # on its own newline gets nothing, and neither reader minds a blank
  311      # line (CloudText::liveLine reads one as nothing).
  312      if [ "${progress_verb}" -eq 1 ] && [ -s "${trace}" ] && [ -n "$(tail -c1 "${trace}")" ]; then
  313          printf '\n'
  314      fi
  315      # Whether this call moved anything -- a file transferred or deleted --
  316      # for the stamp of a run the network later ends (#308 claude F-CS-24).
  317      local moved_bytes moved_checks moved_files moved_deleted moved_listed
  318      read -r moved_bytes moved_checks moved_files moved_deleted moved_listed <<< "$(progress_mark "${trace}")"
  319      { [ "${moved_files:-0}" -gt 0 ] || [ "${moved_deleted:-0}" -gt 0 ]; } 2>/dev/null && RCLONE_MOVED=1
  320      rm -rf "${dir}" 2>/dev/null
  321      if [ "${ended}" -eq 1 ]; then
  322          log_message "rclone $1 made no progress for ${DELIBERATE_CEILING_SECONDS}s and was ended (it returned ${rc}); reporting 124" "false" "WARN"
  323          rc=124
  324      fi
  325      return "${rc}"
  326  }
  327  
  328  # Did rclone log moving a file -- "<path>: Copied (...)", "Moved (...)",
  329  # "Deleted" -- since <offset> into LOG_FILE, or in <file> (its stderr, when
  330  # the options carry no --log-file)? An automatic run's rclone runs under
  331  # timeout, not the stall ceiling, so it has no trace for progress_mark to
  332  # read; what it logs is how RCLONE_MOVED is known for it (the audit of the
  333  # fixes, claude G-A-01: the game-exit sync stamped a bare 69, SKIPPED, over
  334  # saves that went up).
  335  logged_moved() { # <offset into LOG_FILE> [file]
  336      local now
  337      {
  338          now=$(stat -c %s "${LOG_FILE}" 2>/dev/null) && [ "${now}" -gt "$1" ] 2>/dev/null \
  339              && tail -c +$(( $1 + 1 )) "${LOG_FILE}" 2>/dev/null
  340          [ -n "${2:-}" ] && cat "$2" 2>/dev/null
  341      } | grep -qE ': (Copied|Moved) \(|: Deleted$'
  342  }
  343  
  344  rclone() {
  345      if [ "${AUTOMATIC}" -eq 1 ]; then
  346          if [ "${SYNC_DEADLINE}" -gt 0 ]; then
  347              local left=$(( SYNC_DEADLINE - $(date +%s) ))
  348              # Past the ceiling nothing more is started (#308 gpt F-CS-34): each
  349              # call used to be given a second more and three to die in, so a
  350              # run that met its ceiling went on for as many seconds again as it
  351              # had calls left -- the probe that words the failure, the tidy.
  352              # The call's answer is the ceiling's own, 124.
  353              if [ "${left}" -lt 1 ]; then
  354                  log_message "rclone $1 not started: the automatic ceiling had passed" "false"
  355                  return 124
  356              fi
  357              local log0 rc
  358              log0=$(stat -c %s "${LOG_FILE}" 2>/dev/null || echo 0)
  359              command timeout -k 3 "${left}" rclone "$@" "${RCLONE_SYNC_NET_OPTS_ARRAY[@]}"; rc=$?
  360              logged_moved "${log0}" && RCLONE_MOVED=1
  361              return "${rc}"
  362          else
  363              command rclone "$@"
  364          fi
  365      elif [ -n "${RCLONE_OUTER}" ]; then
  366          "${RCLONE_OUTER}" "$@"
  367      else
  368          bounded_rclone "$@"
  369      fi
  370  }
  371  
  372  # The pauses between sections give somebody reading the console time to see
  373  # each one before the next scrolls in. Under --yes nobody is reading -- the
  374  # output is a progress card or the transfer page -- and the restore still
  375  # slept seven seconds of them on every headless run, the startup sync's
  376  # restore half included, while cloud_backup had stopped (#308 claude
  377  # F-CS-04). The same function as cloud_backup's.
  378  pause() {
  379      [ "${ASSUME_YES}" -eq 1 ] || sleep "$1"
  380  }
  ...
  434  # does mark close-on-exec, and nothing this script starts can see it.
  435  #
  436  # The refusal also waits a moment before saying no, as belt and braces for
  437  # a holder this script does not own: a descriptor leaked by an older build,
  438  # or a process in the act of exiting, frees itself in milliseconds, while a
  439  # real concurrent transfer does not. One second of patience turns a raced
  440  # skip into a run that works and costs a genuinely blocked run one second.
  441  CLOUD_SYNC_LOCK=/var/run/cloud_sync.lock
  442  take_cloud_lock() {
  443      local tries=0
  444      exec 9>"${CLOUD_SYNC_LOCK}"
  445      while ! flock -n 9; do
  446          if [ "${tries}" -ge 4 ]; then
  447              echo "Skipped: another cloud sync is already running. Try again when it's done."
  448              log_message "skipped: another cloud sync holds ${CLOUD_SYNC_LOCK}" "false"
  449              exit "${EXIT_LOCK_HELD}"
  450          fi
  ...
  714          || rm -f "${tmp}" 2>/dev/null
  715  }
  716  
  717  # The stamp's third field: why the run did not finish, as the token the
  718  # menu row reads back (D-UI-028) -- the >>> why sentence with its spaces as
  719  # underscores, so a reader that splits on spaces still gets one field.
  720  # Nothing when the run completed, or ended on a sentinel the reader names
  721  # itself.
  722  record_last_run() {
  723      local exit_code="$1"
  724      local name="restore" why=""
  725      [ "${SYSTEM_ONLY}" -eq 1 ] && name="settings-restore"
  726      case "${exit_code}" in
  727          0|9|"${EXIT_NO_NETWORK}"|"${EXIT_LOCK_HELD}") ;;
  728          *) [ -n "${LAST_WHY}" ] && why=" $(printf '%s' "${LAST_WHY}" | tr ' ' '_')" ;;
  729      esac
  730      # SKIPPED means nothing was touched (#308 claude F-CS-24): a run the
  731      # network ended after a transfer of this run had moved a file keeps its
  732      # 69 and adds the gaps token and a why, which the rows read as COULDN'T
  ...
  756      log_message "why: $1" "false"
  757  }
  758  # The summary's word for a phase (D-UI-028): COMPLETED, or COULDN'T FINISH.
  759  # rclone's 9 (nothing needed moving) is a completion. SUCCESS and COMPLETED
  760  # WITH ERRORS -- a partial success reported as errors -- retire.
  761  # Names on stdin within a typo of the one wanted -- two edits, one for a
  762  # name under five characters -- compared without case: Savez, saves, Save,
  763  # Saves2 against Saves (#127). The exact name is never among them, since it
  764  # is the folder that was found missing. busybox awk: no gensub, no
  765  # multi-dimensional array syntax beyond SUBSEP, both avoided.
  766  near_names() {
  767      awk -v want="$1" '
  768      function lev(a, b,    i, j, la, lb, cost, ai, bj, best) {
  769          la = length(a); lb = length(b)
  770          for (j = 0; j <= lb; j++) d[0, j] = j
  771          for (i = 1; i <= la; i++) {
  772              d[i, 0] = i; ai = substr(a, i, 1)
  773              for (j = 1; j <= lb; j++) {
  ...
 1250      log_message "Loading configuration from cloud_sync.conf" "false"
 1251      # A config that does not parse is not run with. `source` used to be
 1252      # unchecked, so a torn file -- a partial trailing line -- was read up to
 1253      # the tear and the run went on with whatever was missing (SAVES_REMOTE
 1254      # unset means remote:/). The helper's copy from before this run's
 1255      # update is the fallback; with no good copy the run refuses and says so
 1256      # (D-CLOUD-078, #105).
 1257      local conf="/storage/.config/cloud_sync.conf"
 1258      if ! conf_valid "${conf}"; then
 1259          # Which line, and what about it -- never the value (PL-015).
 1260          log_message "cloud_sync.conf is not run with: ${CONF_WHY}" "false" "WARN"
 1261          if [ -f "${conf}.bak" ] && conf_valid "${conf}.bak"; then
 1262              log_message "cloud_sync.conf does not parse; putting back the copy taken before this run's update" "false" "WARN"
 1263              cp -f "${conf}.bak" "${conf}.tmp.$$" && mv -f "${conf}.tmp.$$" "${conf}"
 1264          else
 1265              rm -f "${conf}.tmp.$$" 2>/dev/null
 1266              log_message "Your cloud sync settings couldn't be read, and there's no good copy to fall back on.\nNothing was changed. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE." "true" "ERROR"
 1267              say_why "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
 1268              clean_exit 1
 1269          fi
 1270      fi
 1271      if ! source "${conf}"; then
 1272          log_message "Your cloud sync settings couldn't be read. Nothing was changed.\nSet up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE." "true" "ERROR"
 1273          say_why "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
 1274          clean_exit 1
 1275      fi
 1276  
 1277      # Saves have one local folder (D-CLOUD-040). RESTOREPATH used to let a
 1278      # restore land somewhere other than the live saves -- a safety valve from
 1279      # when restore was a mirror. A config still pointing it elsewhere would
  ...
 1586  # included, outside every rclone bound, and on a large library on a slow
 1587  # card that is seconds of walking at boot. rclone renames on completion, so
 1588  # a transfer that finished left none; what can have left one is a transfer
 1589  # that failed, or one that never got to say it finished (a kill, a power
 1590  # cut). PARTIALS_CLEAN is that saying: removed as the saves transfer
 1591  # starts, written back once it has ended and been swept if it needed to
 1592  # be. A run that finds it missing -- a cut run before it, or the first run
 1593  # on a build that keeps it -- sweeps. One rm for many files (+, not \;).
 1594  PARTIALS_CLEAN=/storage/.cache/cloud_sync/restore-tree-clean
 1595  sweep_partials() {
 1596      [ -d "$1" ] || return 0
 1597      find "$1" -type f -name '*.????????.partial' -exec rm -f {} + 2>/dev/null
 1598  }
 1599  
 1600  # One record at rest under the local --backup-dir root: the folder this run
 1601  # wrote, kept by the name this run gave it, every other one removed. Names
 1602  # are stamps from this device's clock, which moves backwards when NTP
 1603  # corrects it on a handheld with no RTC, so "the newest by name" could be an
 1604  # older run's and the copies this run had just replaced were the ones removed
 1605  # (audit #307 PL-021, the local half). With no folder of this run's --
 1606  # nothing was replaced -- the newest by name is kept, as before.
 1607  prune_replaced_local() {
 1608      local root="$1" pinned="$2" d
 1609      [ -d "${root}" ] || return 0
 1610      if [ -n "${pinned}" ] && [ -d "${root}/${pinned}" ]; then
 1611          for d in "${root}"/*/; do
 1612              [ -d "${d}" ] || continue
 1613              [ "${d%/}" = "${root}/${pinned}" ] && continue
 1614              rm -rf "${d}"
 1615          done
 1616          return 0
 1617      fi
 1618      ls -1d "${root}"/*/ 2>/dev/null | sort -r | tail -n +2 | while read -r d; do
 1619          rm -rf "${d}"
 1620      done
 1621  }
 1622  
 1623  # PART 1: Game saves restore function
 1624  # Restores game saves from cloud storage
 1625  restore_game_saves() {
 1626      WHY_SAID=0
 1627      log_message "====================================" "true"
 1628      log_message "RESTORING YOUR GAME SAVES" "true"
 1629      echo ">>> unit SAVES||"
  ...
 1750          fi
 1751  
 1752          log_message "Couldn't reach your saves folder in the cloud." "true" "ERROR"
 1753          report_rclone_error $remote_check_status "Reaching your saves folder"
 1754          return $remote_check_status
 1755      fi
 1756      
 1757      # Ensure local restore path exists
 1758      if [ ! -d "${SAVESPATH}" ]; then
 1759          log_message "Creating local restore path: ${SAVESPATH}" "false"
 1760          mkdir -p "${SAVESPATH}"
 1761      fi
 1762      
 1763      # Pass an explicit --log-level INFO when LOG_LEVEL is INFO
 1764      local rclone_debug=""
 1765      local filtered_opts=("${RCLONE_OPTS_ARRAY[@]}")
 1766      
 1767      # Add debug logging if LOG_LEVEL is INFO
 1768      if [ "${LOG_LEVEL}" == "INFO" ]; then
  ...
 1861      # writing the new one. The manual RESTORE SAVES row passes no --update,
 1862      # so a newer local save can be replaced by an older cloud copy, and
 1863      # until 2026-09-10 nothing kept the loser -- D-CLOUD-078's named gap
 1864      # (#22's reconciler is the full answer; this is the cheap form). Under
 1865      # /storage/.cache: the internal card, outside the saves tree, so it never
 1866      # overlaps the destination and never enters a backup. One folder per
 1867      # run; after a run that completed, every folder but the newest goes, so
 1868      # there is one record at rest (D-CLOUD-078 (3)).
 1869      local replaced_root="/storage/.cache/cloud_sync/replaced" replaced_stamp
 1870      replaced_stamp=$(date +%Y_%m_%d-%H%M%S)
 1871      all_opts+=("--backup-dir=${replaced_root}/${replaced_stamp}")
 1872      # #315 (D-CLOUD-153, refined D-CLOUD-154): on a remote that compares by
 1873      # size alone, the cloud's upload time stands in for its modtime under
 1874      # --update: a copy uploaded after this device's was written is fetched,
 1875      # one uploaded before it is not (rclone's own one-second window; no
 1876      # --modify-window needed). Without it a same-size change in the cloud
 1877      # read as "already here" whatever its bytes, so the second device never
 1878      # received the first device's save. Known: a local save written under a
 1879      # wrong clock, never uploaded, can be replaced by the cloud's older copy
  ...
 1885          for opt in "${all_opts[@]}"; do [ "${opt}" = "--update" ] && has_update=1; done
 1886          [ "${has_update}" = 1 ] || all_opts+=("--update")
 1887          log_message "the remote compares by size alone (#315): the cloud's upload time is compared with this device's copy (--update)" "false"
 1888      else
 1889          log_message "the remote keeps modtimes or hashes: rclone's own comparison" "false"
 1890      fi
 1891  
 1892      # Check if the rclone version supports the terminal width flag
 1893      if rclone help | grep -q progress-terminal-width; then
 1894          all_opts+=("--progress-terminal-width=80")
 1895      fi
 1896      
 1897      local tree_was_clean=0
 1898      [ -e "${PARTIALS_CLEAN}" ] && tree_was_clean=1
 1899      rm -f "${PARTIALS_CLEAN}" 2>/dev/null
 1900  
 1901      # Execute rclone with enhanced error handling
 1902      execute_rclone_with_error_handling \
 1903          "${RESTOREMETHOD}" \
 1904          "${REMOTENAME}${SAVES_REMOTE}/" \
 1905          "${SAVESPATH}/" \
 1906          "${all_opts[@]}"
 1907      
 1908      RESTORE_STATUS=$?
 1909      if [ "${tree_was_clean}" -eq 0 ] || { [ $RESTORE_STATUS -ne 0 ] && [ $RESTORE_STATUS -ne 9 ]; }; then
 1910          sweep_partials "${SAVESPATH}"
 1911      fi
 1912      mkdir -p "$(dirname "${PARTIALS_CLEAN}")" 2>/dev/null
 1913      : > "${PARTIALS_CLEAN}" 2>/dev/null
 1914      if [ $RESTORE_STATUS -eq 0 ] || [ $RESTORE_STATUS -eq 9 ]; then
 1915          prune_replaced_local "${replaced_root}" "${replaced_stamp}"
 1916      fi
 1917      # A failed transfer says why. The network gone ends the run as 69 here;
 1918      # anything else falls through to report_rclone_error with rclone's code.
 1919      if [ $RESTORE_STATUS -ne 0 ] && [ $RESTORE_STATUS -ne 9 ]; then
 1920          network_lost_during_run "$RESTORE_STATUS" "the saves restore"
 1921      fi
  ...
 1985              log_message "There's no settings backup in the cloud yet." "true" "WARN"
 1986              return 0
 1987          fi
 1988          
 1989          log_message "Starting restore of settings backup files from ${REMOTENAME}${SETTINGS_REMOTE} to ${SETTINGS_BACKUPS}" "false"
 1990          log_message "Settings backup file restore started at $(date)" "false"
 1991          
 1992          # Ensure local target directory exists before attempting restore
 1993          mkdir -p ${SETTINGS_BACKUPS}
 1994          
 1995          # This transfer's root is SETTINGS_REMOTE, whose contents came from
 1996          # SETTINGS_BACKUPS -- so the archive sits at the root, as "backup-*.zip",
 1997          # not under "backup/". Both includes below named a directory that is not
 1998          # there, and because using --include at all excludes everything it does
 1999          # not match, this restore transferred nothing at all. The saves
 2000          # allowlist was misanchored here for the same reason, and its
 2001          # "- /**/*.zip" would have excluded the archive regardless. Match what
  ...
 2020          # Unlike the backup side, this cannot be settled from a local marker:
 2021          # the authoritative copy is the remote one, and its content is exactly
 2022          # what we cannot see. Restore is an explicit, infrequent action -- it
 2023          # does not run on game exit -- so fetching unconditionally costs one
 2024          # download at the moment someone is already waiting for their data.
 2025          backup_opts+=("--ignore-times")
 2026  
 2027          # Check if the rclone version supports the terminal width flag
 2028          if rclone help | grep -q progress-terminal-width; then
 2029              backup_opts+=("--progress-terminal-width=80")
 2030          fi
 2031          
 2032          # Read both layouts, and write only the new one (cloud_backup does
 2033          # that). Archives made before per-device folders sit at the root of
 2034          # SETTINGS_REMOTE, and they are still someone's only backup -- a device
 2035          # that upgrades must keep finding them. Nothing is moved or deleted:
 2036          # the root copy may belong to another device that has not updated yet.
  ...
 2207  main() {
 2208      check_network_link
 2209      check_rclone_config
 2210      load_config
 2211      # restore_game_saves proves the remote reachable with the listing it
 2212      # needs anyway, and network_lost_during_run words a failure there; only
 2213      # the settings-only path has no such step of its own -- cloud_backup's
 2214      # shape (#308 claude F-CS-04), one remote round trip fewer per run. After
 2215      # load_config, which sets an automatic run's deadline (#308 gpt F-CS-34).
 2216      # An existing config file can contain no remote (#392). Without the
 2217      # prefix, rclone interprets SAVES_REMOTE as a local path. Refuse before
 2218      # any path operation instead of treating local files as cloud storage.
 2219      REMOTENAME=$(first_remote)
 2220      case "${REMOTENAME}" in
 2221          ?*:) ;;
 2222          *) local reason
 2223             reason=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" selection-reason 2>/dev/null) || reason="YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
 2224             log_message "Choose or add a connection under GAME SETTINGS > MANAGE CLOUD STORAGE > CLOUD CONNECTIONS, then try again." "true" "ERROR"
 2225             say_why "${reason}"
 2226             clean_exit 1 ;;
 2227      esac
 2228      [ "${SYSTEM_ONLY}" -eq 1 ] && check_internet
 2229      
 2230      # Begin main script operations with user-friendly header
 2231      log_message "=> ${OS_NAME} CLOUD RESTORE\n"
 2232      
 2233      # Execute Part 1: Game saves restore
 2234      # This performs the primary save file restoration operation using the configured method
 2235      # --system-only was parsed and then ignored here, so it restored game saves
 2236      # anyway -- the opposite of what it says, over the top of local saves.
 2237      if [ "${SYSTEM_ONLY}" -eq 1 ]; then
 2238          log_message "Skipped game saves this time - settings only." "true"
 2239          SAVES_OUTCOME="SKIPPED - SETTINGS ONLY"
 2240          RESTORE_STATUS=0
 2241      else
 2242          restore_game_saves
 2243          RESTORE_STATUS=$?
 2244      fi
 2245      
 2246      # Add a pause for better visual separation between operations
 2247      pause 2
 2248      
 2249      # Execute Part 2: System restore
 2250      # This restores settings backup files (zip files) if enabled in configuration
 2251      if [ "${SAVES_ONLY}" -eq 1 ]; then
 2252          log_message "Skipped settings this time - saves only." "true"
 2253          SETTINGS_OUTCOME="SKIPPED - SAVES ONLY"
 2254          RESTORE_SYSTEM_STATUS=0
 2255      else
 2256          restore_system_files
 2257          RESTORE_SYSTEM_STATUS=$?
 2258      fi
 2259      
 2260      # Create empty missing system directories if removed during restore
 2261      # Only necessary when using sync method which can delete files
 2262      if [ "${RESTOREMETHOD}" == "sync" ]; then
 2263          log_message "Making sure every system folder is there..." "true"
 2264          # Guarded the way automount does it: the file is generated at build
 2265          # time, so a missing one means a broken image, not a reason to print a
 2266          # systemd error at the end of an otherwise good restore.
 2267          if [ -e "/usr/config/system-dirs.conf" ]; then
 2268              systemd-tmpfiles --create /usr/config/system-dirs.conf >/dev/null 2>&1 ||:
 2269          fi
 2270      fi
 2271      
 2272      # Add a pause before summary
 2273      pause 2
 2274      
 2275      # Add a line break for better visual separation
 2276      echo
 2277      
 2278      # The run's exit, decided by both phases (the note below the summary
 2279      # says why); computed here because the outcome line reads it.
 2280      # rclone's 9 -- nothing needed moving -- is a completion wherever a
 2281      # phase is judged (outcome_word, run_outcome_line), so it is here too: a
 2282      # saves phase that returned 9 used to keep a settings phase's failure
 2283      # out of the exit and the stamp, and the run said Completed. over an
 2284      # archive that never moved (audit #307 PL-028).
 2285      local overall=${RESTORE_STATUS}
 2286      case "${overall}" in
 2287          0|9) overall=${RESTORE_SYSTEM_STATUS} ;;
 2288      esac
 2289  
 2290      # Provide final summary of all operations
 2291      log_message "====================================" "true"
 2292      log_message "RESTORE SUMMARY:" "true"
 2293      log_message "Game saves: ${SAVES_OUTCOME:-$(outcome_word $RESTORE_STATUS)}" "true"
 2294      [ "${BACKUPFILE_RESTORE_OPTION}" == "yes" ] && log_message "Settings backup: ${SETTINGS_OUTCOME:-$(outcome_word $RESTORE_SYSTEM_STATUS)}" "true"
 2295      case "${overall}" in
 2296          0|9) log_message "$(run_outcome_line "${overall}")" "true" ;;
 2297          *)   log_message "$(run_outcome_line "${overall}")" "true" "ERROR" ;;
 2298      esac
 2299      log_message "Log file: ${LOG_FILE}" "false"
 2300      log_message "====================================" "true"
 2301      
 2302      # Add a final pause before exiting
 2303      pause 3
 2304      
 2305      # Both phases decide the exit. It was the saves phase's alone -- "use the
 2306      # game saves restore status as the overall exit code" -- so a settings
 2307      # download that failed exited 0, and under --system-only, where the saves
 2308      # phase is skipped and reports 0, every failure did: the page said
 2309      # COMPLETED SUCCESSFULLY and last-settings-restore recorded 0 for an
 2310      # archive that never arrived (found while bounding the runs, #103; the
 2311      # same fix as cloud_backup's). A run is good when every phase it ran is;
 2312      # otherwise it carries the first failing phase's code, the saves phase's
 2313      # when both failed.
 2314      clean_exit ${overall}
 2315  }
 2316  
 2317  # Set up signal trap to handle user interruption gracefully
 2318  trap 'log_message "Script interrupted by user" "false" "WARN"; clean_exit 130' INT TERM
 2319  
 2320  # Start script execution. The body runs with the lock descriptor closed,
 2321  # so nothing it starts can hold the lock after this shell is gone -- see
 2322  # take_cloud_lock.
 2323  take_cloud_lock
 2324  main 9>&-
```

## Excerpt: sources/cloud_capture (at 8ebaf8daad; 270 of 1704 lines: every line 02 and 04 cite, 8 lines either side, the head, the traps and main; a gap is marked ...)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # cloud_capture - record what a game session wrote into the saves tree, in
    6  # this device's save manifest, at the moment it was written.
    7  #
    8  # A save version is identified by the sha256 of its bytes and explained by who
    9  # wrote it: which device, which emulator and core, which build of that core
   10  # (docs/save-manifest-schema.md). Only the exit path knows the last three, so
   11  # EmulationStation calls this after every game, whatever the cloud toggles
   12  # say and whether or not the emulator exited cleanly (fork #21, R5): a file
   13  # written and not recorded is the one thing nothing can explain later.
   14  #
   15  # The hash is taken from an independent copy of the file, kept under
   16  # /storage/.cache/cloud_sync/stage/<sha256>, never from the live file and
   17  # never from a hard link -- a link follows the next in-place flush, and then
   18  # the bytes the transfer pushes are not the bytes the hash describes
   19  # (D-CLOUD-034). The manifest is rev 2 of the schema (D-CLOUD-045): every
   20  # entry names its unit, each unit declares its members, and a deletion made
   21  # through the save-state manager is written as a retired record before the
   22  # file goes (D-CLOUD-053), so the reconciler can tell "deleted on purpose"
   23  # from "never arrived".
   24  #
   25  # Everything diagnostic goes to /var/log, which is tmpfs and gone at the next
   26  # boot (D-CLOUD-027). So every run also leaves a stamp under
   27  # /storage/.cache/cloud_sync -- a line in last-capture, and one in
   28  # capture-failures for the runs that could not record -- which is how "did
   29  # any exit go unrecorded on this device?" gets answered after a reboot.
   30  # last-capture holds ONE LINE PER MODE (exit, rescan, full, retire; usage for
   31  # a bad invocation), each replaced only by a run of the same mode
   32  # (D-CLOUD-070, #94): the boot --full pass used to write over the record of
   33  # the last game exit. A stamp from before that is a single line, and reads as
   34  # that mode's line. Each line is
   35  #
   36  #   <epoch> <rc> <mode>[!card] <unit|-> emu-exit=<N|?> <emulator>/<core>
   37  #
   38  # The unit may contain spaces (a ROM stem); the two trailing fields never do,
   39  # so a reader takes three fields from the front and two from the back, picks
   40  # its line by the third field with any !card marker stripped, and finds the
   41  # most recent run of any mode by the largest first field.
   42  # emu-exit is the launch's exit as EmulationStation saw it -- runemu.sh's
   43  # status, 0 or 1: it collapses the emulator's own code, and reports the exit
   44  # hotkey's kill (137/143) as 0 -- not the emulator's code. That and the frozen
   45  # pair are the two things only the exit path knew, and a run that could not
   46  # record (rc 1) is exactly when the log line naming them is the one that will
   47  # be gone; outside exit mode they read `emu-exit=? -/-`.
   48  #
   49  # Exactly one mode per invocation:
   50  #
   51  #   cloud_capture --system SYS --rom ROM --emulator EMU --core CORE --started EPOCH [--exit N]
   52  #                                        exit mode: record the unit the session wrote.
   53  #                                        --emulator/--core are the tokens of the command
   54  #                                        that ran, never re-resolved; a member with no
   55  #                                        entry is recorded only when its mtime >= EPOCH
   56  #                                        (--started 0 records every member)
   57  #   cloud_capture --rescan --system SYS --rom ROM
   58  #                                        after the save-state manager renumbered: re-key
   59  #                                        moved versions; adopts nothing new
   60  #   cloud_capture --full                 hash every path the manifest already claims;
   61  #                                        adopts no path without an entry (the boot pass)
   62  #   cloud_capture --retire PATH [PATH ...]
   63  #                                        record deliberate deletions, BEFORE the unlink
   64  #                                        (a state's .png: dropped from its unit's members,
   65  #                                        never a retired row -- D-CLOUD-059)
   66  #   cloud_capture --retire --unlink PATH [PATH ...]
   67  #                                        the same, then the files go: the save-state
   68  #                                        manager's deletion as one unit, so a stop cannot
   69  #                                        leave the row without the unlink (D-CLOUD-133)
   70  #   cloud_capture --adopt PATH --from PATH --system SYS --rom ROM
   71  #                                        record a copy the save-state manager made: the
   72  #                                        source's version at the new path, or a version of
   73  #                                        unknown provenance when the source had no entry
   74  #   cloud_capture -h | --help
   75  #
   76  # Exit codes: 0 recorded, or nothing to record; 1 could not record (the
   77  # reason is in the log and in capture-failures); 2 usage; 3 (--adopt only)
   78  # the copy is not a state of this unit, so nothing was recorded -- distinct
   79  # from 0 so the caller does not log a recording that never happened (audit
   80  # #258 PL-016). EmulationStation never branches on the code beyond logging
   81  # it -- it logs a nonzero and carries on.
   82  #
   83  # What this script never does: take the transfer lock or touch /var/run, open
   84  # a socket, run rclone or cloud_sync_helper, source the conf or /etc/profile
   85  # (098-busybox would discard a staged PATH), or write anywhere under the
   86  # saves folder -- --unlink removes exactly the files --retire accepted (plain
   87  # paths under the saves folder; one it refused to record it also refuses to
   88  # remove, audit #258 PL-002) and nothing else. Two environment overrides,
   89  # each for a proof: CLOUD_CAPTURE_PINS, so the core-pins map can be proven
   90  # on an image whose read-only /usr has none, and CLOUD_CAPTURE_EXIT_BOUND,
   91  # so the exit capture's bound (PL-034, below) can be proven in seconds.
   92  #
   93  # Two writers are serialised by detection, and their commits by a lock of
   94  # this script's own. The boot --full runs detached and can overlap the first
   95  # game's exit capture; whichever lands second sees the manifest's inode or
   96  # mtime differ from what it loaded and discards its own document rather than
   97  # clobber the other's. An exit, --rescan or --retire that loses then re-runs
   98  # itself ONCE against the winner's document (CLOUD_CAPTURE_RETRY marks the
   99  # second attempt; seals are content-addressed, so it re-uses them); a second
  100  # loss, or a --full that loses, is recorded as manifest-moved and left to the
  101  # next run. The commit itself -- the final check, the rename, the stage's
  102  # GC, the stamp -- runs under /storage/.cache/cloud_sync/.capture.lock (audit
  103  # #307 PL-067): the check and the rename were two steps another capture
  104  # could land between, and one capture's GC could collect a seal another had
  105  # just placed and not yet published. The lock is waited for, briefly -- a
  106  # commit holds it for the check, the rename, one listing of the stage and
  107  # the stamp (lead G2-A-06 of the audit of the fix round) -- and a run that
  108  # cannot have it does not commit (the audit of the fixes, G-A-04: the first
  109  # cut went on under
  110  # detection alone, which is the race the lock exists to close). It is
  111  # treated as a loss to another writer: an exit, --rescan, --retire or
  112  # --adopt re-runs itself once, and a second failure, or a --full, is
  113  # recorded as lock-busy and left to the next run; its stamp line is not
  114  # written either, since the stamp is a read-modify-rename under the same
  115  # lock. It is not the transfer lock, which this script never takes.
  116  
  117  CACHE="/storage/.cache/cloud_sync"
  118  STAGE="${CACHE}/stage"
  119  CONF="/storage/.config/cloud_sync.conf"
  120  LOG_FILE="/var/log/cloud_sync.log"
  121  PINS="${CLOUD_CAPTURE_PINS:-/usr/share/rocknix/core-pins}"
  122  INFO_DIR="/usr/lib/libretro"
  123  RETIRED_MAX=200
  124  SEAL_RETRIES=3
  125  STAGE_MAX_BYTES=268435456
  126  JQ="/usr/bin/jq"
  127  
  128  SCRIPT_NAME="cloud_capture"
  129  # systemd stops EmulationStation's cgroup with one SIGTERM to every process in
  130  # it (essway.service, KillMode control-group), and a deletion this recorder is
  131  # asked to finish (--retire --unlink) is one unit: the row, then the files.
  132  # Ignored here and, since exec keeps SIG_IGN, in every jq, sha256sum and mv
  133  # this starts; systemd's SIGKILL comes only at the stop timeout, long after a
  134  # run this short has exited (fork #205, D-CLOUD-133). A terminal's Ctrl-C
  135  # (SIGINT) still ends it.
  136  trap '' TERM
  137  ECHO_TO_SCREEN="false"
  138  read -r _UP0 _ < /proc/uptime 2>/dev/null || _UP0="0"
  139  _UP0_MS=$(( 10#${_UP0/./}0 ))
  140  # A re-run (CLOUD_CAPTURE_RETRY, below) counts from the first run's start,
  ...
  185      t="$(dirname "$(readlink -f "$0")")/$1"
  186      [ -x "${t}" ] || t="/usr/bin/$1"
  187      printf '%s' "${t}"
  188  }
  189  
  190  # cloud_saves_root's extraction, verbatim: SAVESPATH, then BACKUPPATH, then
  191  # the default. Read, never sourced -- and never cloud_sync_helper, which
  192  # rewrites /storage/.config on every call.
  193  saves_path() {
  194      local p
  195      p=$(sed -n 's/^SAVESPATH="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' "${CONF}" 2>/dev/null | head -1)
  196      [ -n "${p}" ] || p=$(sed -n 's/^BACKUPPATH="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' "${CONF}" 2>/dev/null | head -1)
  197      echo "${p:-/storage/roms}"
  198  }
  199  
  200  elapsed_ms() {
  201      local up
  202      read -r up _ < /proc/uptime 2>/dev/null || up="0"
  203      up="${up/./}0"
  204      echo $(( 10#${up} - _UP0_MS ))
  205  }
  206  
  ...
  765      rm -f "${OPS}" "${CAND}" "${CANON_A}" "${CANON_B}" "${STAGE}"/.tmp.$$.* 2>/dev/null
  766  }
  767  trap cleanup EXIT
  768  
  769  # ---------------------------------------------------------------------------
  770  # STEP 1 -- card context (informational; the one refusal is a flip mid-run)
  771  # ---------------------------------------------------------------------------
  772  SAVES_ROOT_BIN="$(_sib cloud_saves_root)"
  773  IDENT0=""
  774  if [ -x "${SAVES_ROOT_BIN}" ]; then
  775      if [ "${MODE}" = "full" ]; then
  776          _out="$("${SAVES_ROOT_BIN}" check --wait 10 2>&1)"
  777      else
  778          _out="$("${SAVES_ROOT_BIN}" check 2>&1)"
  779      fi
  780      _rc=$?
  781      if [ "${_rc}" -eq 0 ]; then
  782          IDENT0="$(printf '%s\n' "${_out}" | tail -n 1)"
  783          # Anything before the identity is the wait notice.
  784          printf '%s\n' "${_out}" | sed '$d' | while IFS= read -r _line; do
  785              [ -n "${_line}" ] && log_info "${_line}"
  786          done
  787      else
  788          # The file an emulator wrote is real and its claim belongs in the
  789          # manifest (I5); the card is noted, the run continues.
  790          CARD="!card"
  791          printf '%s\n' "${_out}" | while IFS= read -r _line; do
  792              case "${_line}" in
  793                  ''|"Nothing was transferred"*) ;;
  794                  *) log_warn "${_line}" ;;
  795              esac
  796          done
  797          IDENT0="$("${SAVES_ROOT_BIN}" identity 2>/dev/null)"
  798      fi
  799  else
  800      log_warn "cloud_saves_root is missing beside $0 and in /usr/bin; the card is not checked this run"
  801  fi
  802  
  803  # ---------------------------------------------------------------------------
  804  # STEP 2 -- load the manifest
  805  # ---------------------------------------------------------------------------
  ...
 1075      if [ "$(stat -c '%d %i' "${tmp}" 2>/dev/null)" = "$(stat -c '%d %i' "${src}" 2>/dev/null)" ] \
 1076          || [ "$(stat -c %h "${tmp}" 2>/dev/null)" != "1" ]; then
 1077          rm -f "${tmp}" 2>/dev/null
 1078          log_error "seal of ${src} shares the source inode; not recorded this run"
 1079          return 1
 1080      fi
 1081      sha="$( set -o pipefail; sha256sum "${tmp}" | cut -c1-64 )"
 1082      if [ "${#sha}" -ne 64 ]; then
 1083          rm -f "${tmp}" 2>/dev/null
 1084          log_error "hashing the seal of ${src} produced no hash; not recorded this run"
 1085          return 1
 1086      fi
 1087      case "${sha}" in
 1088          *[!0-9a-f]*)
 1089              rm -f "${tmp}" 2>/dev/null
 1090              log_error "hashing the seal of ${src} produced '${sha}'; not recorded this run"
  ...
 1640      rm -f "${TMP}" 2>/dev/null
 1641      log_error "could not rename ${TMP} onto ${MANIFEST}; the previous manifest is intact"
 1642      finish 1 "rename-failed"
 1643  fi
 1644  [ "${MANIFEST_REV1}" -eq 1 ] && log_warn "${MANIFEST} was a rev 1 manifest; upgraded in place (units, retired added)"
 1645  
 1646  # ---------------------------------------------------------------------------
 1647  # STEP 11 -- stage GC, and the price
 1648  # ---------------------------------------------------------------------------
 1649  declare -A STAGE_REF
 1650  while IFS= read -r _ref; do
 1651      [ -n "${_ref}" ] && STAGE_REF["${_ref}"]=1
 1652  done < <("${JQ}" -r '.entries[] | select(.pub == null) | .sha256 // empty' "${MANIFEST}" 2>/dev/null)
 1653  # A seal placed in the last ten minutes is spared (PL-067): it may be
 1654  # another capture's, sealed and not yet published, and collecting it would
 1655  # leave that capture's entry naming a copy that is gone. By its change time,
 1656  # which the seal's rename sets -- its modification time is the save's own
 1657  # (cp -p). The next capture's GC takes it if nothing claims it.
 1658  #
 1659  # One stat over the whole stage and one rm over what goes (the audit of
 1660  # the fix round, lead G2-A-06): this runs under the commit lock, which an
 1661  # exit capture waits for, and a stat per seal held it for seconds on a
 1662  # stage of thousands on a slow card. The glob is the stage's own names --
 1663  # no dot files, so no .tmp.* seal in the making -- and a seal's name is a
 1664  # sha256, which holds no blank. A stage too big for one command line
 1665  # (bash's 126) is walked in the batches find makes instead.
 1666  stage_times() {
 1667      local out rc
 1668      out=$(stat -c '%Z %n' -- "${STAGE}"/* 2>/dev/null); rc=$?
 1669      [ "${rc}" -eq 126 ] \
 1670          && out=$(find "${STAGE}" -mindepth 1 -maxdepth 1 -type f ! -name '.*' -exec stat -c '%Z %n' {} + 2>/dev/null)
 1671      [ -n "${out}" ] && printf '%s\n' "${out}"
 1672  }
 1673  _now=$(date +%s)
 1674  _gone=()
 1675  while read -r _ct _f; do
 1676      _n="${_f##*/}"
 1677      [ -n "${_n}" ] || continue
 1678      [ -n "${STAGE_REF[${_n}]}" ] && continue
 1679      case "${_ct}" in ''|*[!0-9]*) continue ;; esac
 1680      [ $(( _now - _ct )) -lt 600 ] && continue
 1681      _gone+=("${_f}")
 1682  done < <(stage_times)
 1683  # Removed in bounded batches (the audit of the fixes, gpt G3-D-05): a stage with
 1684  # enough old seals to exceed the argument size failed the one rm the way the
 1685  # stat above already guarded against, and kept them all.
 1686  [ "${#_gone[@]}" -gt 0 ] && printf '%s\0' "${_gone[@]}" | xargs -0 rm -f 2>/dev/null
 1687  _kb="$(du -sk "${STAGE}" 2>/dev/null | cut -f1)"
 1688  case "${_kb}" in ''|*[!0-9]*) _kb=0 ;; esac
 1689  if [ $(( _kb * 1024 )) -gt "${STAGE_MAX_BYTES}" ]; then
 1690      _cnt="$(ls -1 "${STAGE}" 2>/dev/null | wc -l | tr -d ' ')"
```

## Evidence: fixtures/load-config-fallback.sh (F-01's fixture)

```text
#!/bin/bash
# T16 lead 1: load_config sources the conf conf_valid refused when the .bak copy fails.
#   run.sh <cloud_backup or cloud_restore at 8ebaf8daad> unfixed-shape
# Lifts conf_valid, load_config, log_message, say_why and clean_exit's stand-in from the
# script; rewrites /storage/.config to a scratch dir; the one planted input is a cp that
# fails (the full card), named here. The refused conf carries a line that, if sourced,
# leaves a marker file; conf_valid refuses it ("something after the value").
set -u
SRC=${1:?script}; W=$(mktemp -d "${TMPDIR:?}/lc.XXXXXX"); mkdir -p "$W/storage/.config"
python3 -I - "$SRC" "$W/funcs.sh" "$W" <<'PY'
import re, sys
src, out, w = sys.argv[1], sys.argv[2], sys.argv[3]
L = open(src).read().split("\n"); keep = {"conf_valid", "load_config", "say_why"}; buf = []; i = 0
while i < len(L):
    m = re.match(r"^([a-z_]+)\(\)", L[i])
    if m and m.group(1) in keep:
        j = i
        while not L[j].startswith("}"): j += 1
        buf += L[i:j + 1]; i = j + 1; continue
    i += 1
open(out, "w").write("\n".join(buf).replace("/storage/.config", w + "/storage/.config") + "\n")
PY
# a valid .bak (the shipped conf) and a refused live conf whose sourcing leaves a marker
cp "$(dirname "$SRC")/cloud_sync.conf" "$W/storage/.config/cloud_sync.conf.bak"
{ cat "$W/storage/.config/cloud_sync.conf.bak"; printf 'EXTRA=x; : > %s/SOURCED_REFUSED\n' "$W"; } > "$W/storage/.config/cloud_sync.conf"
for mode in cp-works cp-fails; do
  rm -f "$W/SOURCED_REFUSED"; cp "$W/storage/.config/cloud_sync.conf" "$W/live.$mode"
  bash -c '
    W=$1; mode=$2
    log_message() { echo "LOG[$3] $1" >> "$W/log.$mode"; }; clean_exit() { echo "clean_exit $1" >> "$W/log.$mode"; exit "$1"; }
    pause() { :; }; controller_confirm() { return 1; }
    [ "$mode" = cp-fails ] && cp() { return 1; }      # the planted input: the copy fails, as on a full card
    AUTOMATIC=1; ASSUME_YES=1; SYSTEM_ONLY=0; METHOD_OVERRIDE=""; EXTRA_UPDATE=0; START_TIME=$(date +%s); WHY_SAID=0
    RCLONE_NET_OPTS_FALLBACK="x"; RCLONE_SYNC_NET_OPTS_FALLBACK="x"; SYNC_CEILING_SECONDS_FALLBACK=90; LOG_FILE=/dev/null
    . "$W/funcs.sh"; load_config; echo "load_config returned $?" >> "$W/log.$mode"' _ "$W" "$mode" > "$W/out.$mode" 2>&1
  printf '%s: rc=%s sourced_refused=%s conf_now_valid=%s tmp_left=%s\n' "$mode" "$?" \
    "$([ -e "$W/SOURCED_REFUSED" ] && echo YES || echo no)" \
    "$(bash -c '. "$1/funcs.sh"; conf_valid "$1/storage/.config/cloud_sync.conf" && echo yes || echo no' _ "$W")" \
    "$(ls "$W/storage/.config/" | grep -c '\.tmp\.' )"
  cp "$W/live.$mode" "$W/storage/.config/cloud_sync.conf"
  grep -E 'clean_exit|putting back|returned' "$W/log.$mode" | sed 's/^/    /'
done
echo "scratch: $W"
```

## Evidence: fixtures/trap-defer.sh (F-03's fixture)

```text
#!/bin/bash
# T16 lead 12: a TERM to a bash script waits for its foreground child, as cloud_backup's
# automatic run's `command timeout -k 3 <left> rclone ...` is. `sleep` stands in for rclone.
trap 'echo "trap ran at +$(( $(date +%s) - T0 ))s"; exit 130' INT TERM
T0=$(date +%s); timeout -k 3 6 sleep 30; echo "child returned at +$(( $(date +%s) - T0 ))s"
```

## Evidence: guest-cycle/host-leads/a-awk/out (host lead a-awk)

```text
== T16 host lead (a) awk and gensub -- 2026-10-30T05:34:01Z
donor root: /workspace/artifacts/m6-donor/1a0266484423/image/system (BUILD_ID 1a0266484423); sha256sum -c ../../SHA256SUMS:
  usr/bin/busybox: OK
  usr/bin/rclone: OK
  etc/os-release: OK
the scripts and /usr/config: git show 8ebaf8daad, 12 of 12 sha256-equal to the guest's installed bytes (guest-cycle/installed.sha256)
from the donor: busybox v1.36.1 (146 applet links), rclone v1.75.2
host stand-ins (not in the donor): bash 5.3.9(1)-release (image: 5.3), timeout (GNU coreutils) 9.7 (image: 9.4), grep (GNU grep) 3.12 (image: 3.9), python3 3.14.4, ip (iproute2)
sandbox: /workspace/tmp/m6-t16/hl/sbx.sh (copied to host-leads/sandbox/) (bwrap, own pid namespace, host network); backend: cloud-test-backend at 3a653eaec4, WebDAV 127.0.0.1:9010, state /workspace/tmp/m6-t16/hl/state

$ readlink /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/awk
busybox
$ echo 'a=b' | busybox awk '{print gensub(/=.*/, "", 1)}'   (the cleanup's own call)
a
rc=0
$ busybox awk 'BEGIN{print gensub(/(b)/, "<\\1>", "g", "abcb")}'   (back-references, global)
a<b>c<b>
rc=0

the shipped conf with LOG_LEVEL and a three-line RCLONEOPTS repeated after it (A48's shape):
  before: 2 LOG_LEVEL, 2 RCLONEOPTS, bwlimit lines 1
$ (sandbox) command -v awk; cloud_sync_cleanup_duplicates.sh /storage/.config/cloud_sync.conf
/donor/usr/bin/busybox
Duplicate variable assignments removed from /storage/.config/cloud_sync.conf.
rc=0
bash -n rc=0
  after: 1 LOG_LEVEL (LOG_LEVEL="INFO"), 1 RCLONEOPTS, bwlimit lines 0
== end 2026-10-30T05:34:01Z
```

## Evidence: guest-cycle/host-leads/b-empty-savespath/out (host lead b-empty-savespath)

```text
== T16 host lead (b) SAVESPATH="", cloud_restore --yes --saves-only -- 2026-10-30T05:27:00Z
donor root: /workspace/artifacts/m6-donor/1a0266484423/image/system (BUILD_ID 1a0266484423); sha256sum -c ../../SHA256SUMS:
  usr/bin/busybox: OK
  usr/bin/rclone: OK
  etc/os-release: OK
the scripts and /usr/config: git show 8ebaf8daad, 12 of 12 sha256-equal to the guest's installed bytes (guest-cycle/installed.sha256)
from the donor: busybox v1.36.1 (146 applet links), rclone v1.75.2
host stand-ins (not in the donor): bash 5.3.9(1)-release (image: 5.3), timeout (GNU coreutils) 9.7 (image: 9.4), grep (GNU grep) 3.12 (image: 3.9), python3 3.14.4, ip (iproute2)
sandbox: /workspace/tmp/m6-t16/hl/sbx.sh (copied to host-leads/sandbox/) (bwrap, own pid namespace, host network); backend: cloud-test-backend at 3a653eaec4, WebDAV 127.0.0.1:9010, state /workspace/tmp/m6-t16/hl/state

the cloud (the backend's data directory): pixelelated/Saves/gba/b2.srm pixelelated/Saves/savestates/b1.state 

=== arm ctl (2026-10-30T05:27:00Z); cell /workspace/tmp/m6-t16/hl/cells/b-ctl.052700
conf: 24:SAVESPATH="/storage/roms"
/ is writable
cloud_restore rc=0
-- its output, protocol and prose lines (rclone's redraws dropped; masked):
=>  CLOUD RESTORE
====================================
RESTORING YOUR GAME SAVES
>>> unit SAVES||
====================================
Restoring your saves: completed.
Skipped settings this time - saves only.
====================================
RESTORE SUMMARY:
Game saves: COMPLETED
Completed.
====================================
-- the log's lines for this run (masked):
[2026-10-30 05:27:01] [INFO] [cloud_restore] Starting restore from qa-cloud:/pixelelated/Saves to /storage/roms
[2026-10-30 05:27:01] [INFO] [cloud_restore] the remote compares by size alone (#315): the cloud's upload time is compared with this device's copy (--update)
[2026-10-30 05:27:02] [INFO] [cloud_restore] About to execute: rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO --stats 1s --exclude=bios/** --exclude=backup/** --backup-dir=/storage/.cache/cloud_sync/replaced/2026_10_30-052701 --update qa-cloud:/pixelelated/Saves/ /storage/roms/
-- stamp last-restore: 1793338022 0
-- stamp last-backup: none
-- the seeded saves by name, anywhere but /proc: /storage/roms/gba/b2.srm /storage/roms/savestates/b1.state 
-- files newer than the marker, the whole tree but /proc, /dev and the marker:
/storage/.cache/cloud_sync/last-restore
/storage/.cache/cloud_sync/restore-tree-clean
/storage/.cache/cloud_sync/saves-root
/storage/.config/cloud_sync-rules.txt
/t16-probe
/tmp/b.out
/var/log/cloud_sync.log
/var/run/cloud_sync.lock
-- directories at / now: bin dev donor drv etc host lib lib64 proc run sbin storage t16-probe tmp usr var 
sandbox rc=0

=== arm ro (2026-10-30T05:27:05Z); cell /workspace/tmp/m6-t16/hl/cells/b-ro.052705
conf: 24:SAVESPATH=""
/ is read-only
cloud_restore rc=7
-- its output, protocol and prose lines (rclone's redraws dropped; masked):
=>  CLOUD RESTORE
====================================
RESTORING YOUR GAME SAVES
>>> unit SAVES||
====================================
mkdir: can't create directory '': No such file or directory
[31mRestoring your saves: your cloud wouldn't take the files.[0m
>>> why YOUR CLOUD WOULDN'T TAKE THE FILES
Skipped settings this time - saves only.
====================================
RESTORE SUMMARY:
Game saves: COULDN'T FINISH
[31mCouldn't finish: your cloud wouldn't take the files. Try again.[0m
====================================
-- the log's lines for this run (masked):
[2026-10-30 05:27:06] [INFO] [cloud_restore] Starting restore from qa-cloud:/pixelelated/Saves to 
[2026-10-30 05:27:06] [INFO] [cloud_restore] Creating local restore path: 
[2026-10-30 05:27:06] [INFO] [cloud_restore] the remote compares by size alone (#315): the cloud's upload time is compared with this device's copy (--update)
[2026-10-30 05:27:07] [INFO] [cloud_restore] About to execute: rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO --stats 1s --exclude=bios/** --exclude=storage/roms/backup/** --backup-dir=/storage/.cache/cloud_sync/replaced/2026_10_30-052706 --update qa-cloud:/pixelelated/Saves/ /
2026/10/30 05:27:07 ERROR : Fatal error received - not attempting retries
Errors:                 1 (fatal error encountered)
2026/10/30 05:27:07 NOTICE: Failed to copy: destination and parameter to --backup-dir mustn't overlap
[2026-10-30 05:27:07] [ERROR] [cloud_restore] Restoring your saves: rclone exit 7
[2026-10-30 05:27:07] [ERROR] [cloud_restore] Restoring your saves: your cloud wouldn't take the files.
[2026-10-30 05:27:07] [INFO] [cloud_restore] why: YOUR CLOUD WOULDN'T TAKE THE FILES
[2026-10-30 05:27:07] [ERROR] [cloud_restore] Couldn't finish: your cloud wouldn't take the files. Try again.
-- stamp last-restore: 1793338027 7 YOUR_CLOUD_WOULDN'T_TAKE_THE_FILES
-- stamp last-backup: none
-- the seeded saves by name, anywhere but /proc: 
-- files newer than the marker, the whole tree but /proc, /dev and the marker:
/storage/.cache/cloud_sync/last-restore
/storage/.cache/cloud_sync/restore-tree-clean
/storage/.config/cloud_sync-rules.txt
/storage/.config/cloud_sync-rules.txt.bak
/storage/.config/cloud_sync.conf
/tmp/b.out
/var/log/cloud_sync.log
/var/run/cloud_sync.lock
-- directories at / now: bin dev donor drv etc host lib lib64 proc run sbin storage tmp usr var 
sandbox rc=0

=== arm rw (2026-10-30T05:27:08Z); cell /workspace/tmp/m6-t16/hl/cells/b-rw.052708
conf: 24:SAVESPATH=""
/ is writable
cloud_restore rc=7
-- its output, protocol and prose lines (rclone's redraws dropped; masked):
=>  CLOUD RESTORE
====================================
RESTORING YOUR GAME SAVES
>>> unit SAVES||
====================================
mkdir: can't create directory '': No such file or directory
[31mRestoring your saves: your cloud wouldn't take the files.[0m
>>> why YOUR CLOUD WOULDN'T TAKE THE FILES
Skipped settings this time - saves only.
====================================
RESTORE SUMMARY:
Game saves: COULDN'T FINISH
[31mCouldn't finish: your cloud wouldn't take the files. Try again.[0m
====================================
-- the log's lines for this run (masked):
[2026-10-30 05:27:09] [INFO] [cloud_restore] Starting restore from qa-cloud:/pixelelated/Saves to 
[2026-10-30 05:27:09] [INFO] [cloud_restore] Creating local restore path: 
[2026-10-30 05:27:09] [INFO] [cloud_restore] the remote compares by size alone (#315): the cloud's upload time is compared with this device's copy (--update)
[2026-10-30 05:27:10] [INFO] [cloud_restore] About to execute: rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO --stats 1s --exclude=bios/** --exclude=storage/roms/backup/** --backup-dir=/storage/.cache/cloud_sync/replaced/2026_10_30-052709 --update qa-cloud:/pixelelated/Saves/ /
2026/10/30 05:27:10 ERROR : Fatal error received - not attempting retries
Errors:                 1 (fatal error encountered)
2026/10/30 05:27:10 NOTICE: Failed to copy: destination and parameter to --backup-dir mustn't overlap
[2026-10-30 05:27:10] [ERROR] [cloud_restore] Restoring your saves: rclone exit 7
[2026-10-30 05:27:10] [ERROR] [cloud_restore] Restoring your saves: your cloud wouldn't take the files.
[2026-10-30 05:27:10] [INFO] [cloud_restore] why: YOUR CLOUD WOULDN'T TAKE THE FILES
[2026-10-30 05:27:10] [ERROR] [cloud_restore] Couldn't finish: your cloud wouldn't take the files. Try again.
-- stamp last-restore: 1793338030 7 YOUR_CLOUD_WOULDN'T_TAKE_THE_FILES
-- stamp last-backup: none
-- the seeded saves by name, anywhere but /proc: 
-- files newer than the marker, the whole tree but /proc, /dev and the marker:
/storage/.cache/cloud_sync/last-restore
/storage/.cache/cloud_sync/restore-tree-clean
/storage/.config/cloud_sync-rules.txt
/storage/.config/cloud_sync-rules.txt.bak
/storage/.config/cloud_sync.conf
/t16-probe
/tmp/b.out
/var/log/cloud_sync.log
/var/run/cloud_sync.lock
-- directories at / now: bin dev donor drv etc host lib lib64 proc run sbin storage t16-probe tmp usr var 
sandbox rc=0

=== arm bk (2026-10-30T05:27:11Z); cell /workspace/tmp/m6-t16/hl/cells/b-bk.052711
conf: 24:SAVESPATH=""
/ is read-only
cloud_backup rc=1
-- its output, protocol and prose lines (rclone's redraws dropped; masked):
=>  CLOUD BACKUP
====================================
BACKING UP YOUR GAME SAVES
>>> unit SAVES||
====================================
[31mYour saves folder isn't on this device.[0m
>>> why YOUR SAVES FOLDER ISN'T ON THIS DEVICE
Skipped settings this time - saves only.
====================================
BACKUP SUMMARY:
Game saves: COULDN'T FINISH
Settings backup: SKIPPED - SAVES ONLY
[31mCouldn't finish: your saves folder isn't on this device. Try again.[0m
====================================
-- the log's lines for this run (masked):
[2026-10-30 05:27:12] [INFO] [cloud_backup] Starting backup from  to qa-cloud:/pixelelated/Saves
[2026-10-30 05:27:12] [ERROR] [cloud_backup] the saves folder  is not on this device
[2026-10-30 05:27:12] [ERROR] [cloud_backup] Your saves folder isn't on this device.
[2026-10-30 05:27:12] [INFO] [cloud_backup] why: YOUR SAVES FOLDER ISN'T ON THIS DEVICE
[2026-10-30 05:27:12] [ERROR] [cloud_backup] Couldn't finish: your saves folder isn't on this device. Try again.
-- stamp last-restore: none
-- stamp last-backup: 1793338032 1 YOUR_SAVES_FOLDER_ISN'T_ON_THIS_DEVICE
-- the seeded saves by name, anywhere but /proc: /storage/roms/gba/bk.srm 
-- files newer than the marker, the whole tree but /proc, /dev and the marker:
/storage/.cache/cloud_sync/last-backup
/storage/.config/cloud_sync-rules.txt
/storage/.config/cloud_sync-rules.txt.bak
/storage/.config/cloud_sync.conf
/tmp/b.out
/var/log/cloud_sync.log
/var/run/cloud_sync.lock
-- directories at / now: bin dev donor drv etc host lib lib64 proc run sbin storage tmp usr var 
sandbox rc=0
== end 2026-10-30T05:27:13Z
```

## Evidence: guest-cycle/host-leads/d-terminal-width/out (host lead d-terminal-width)

```text
== T16 host lead (d) --progress-terminal-width -- 2026-10-30T05:34:01Z
donor root: /workspace/artifacts/m6-donor/1a0266484423/image/system (BUILD_ID 1a0266484423); sha256sum -c ../../SHA256SUMS:
  usr/bin/busybox: OK
  usr/bin/rclone: OK
  etc/os-release: OK
the scripts and /usr/config: git show 8ebaf8daad, 12 of 12 sha256-equal to the guest's installed bytes (guest-cycle/installed.sha256)
from the donor: busybox v1.36.1 (146 applet links), rclone v1.75.2
host stand-ins (not in the donor): bash 5.3.9(1)-release (image: 5.3), timeout (GNU coreutils) 9.7 (image: 9.4), grep (GNU grep) 3.12 (image: 3.9), python3 3.14.4, ip (iproute2)
sandbox: /workspace/tmp/m6-t16/hl/sbx.sh (copied to host-leads/sandbox/) (bwrap, own pid namespace, host network); backend: cloud-test-backend at 3a653eaec4, WebDAV 127.0.0.1:9010, state /workspace/tmp/m6-t16/hl/state

$ rclone help | grep -c progress-terminal-width   (the scripts' test)
0
$ rclone help flags | grep -c -- --progress-terminal-width
0
$ rclone help flags | grep -c -- '--progress'   (the family is listed there)
2
$ rclone lsf <empty dir> --progress-terminal-width=80
rc=2
Error: unknown flag: --progress-terminal-width
Usage:
$ rclone lsf <empty dir>   (the control)
rc=0
the scripts' probe, timed on this host (not the device's figure; lead (c) is (window)-pending):
  rclone help | grep -q: 24 ms, grep rc=1
  rclone help | grep -q: 24 ms, grep rc=1
  rclone help | grep -q: 23 ms, grep rc=1
== end 2026-10-30T05:34:01Z
```

## Evidence: guest-cycle/host-leads/f14-backup-dir-order/out (host lead f14-backup-dir-order)

```text
== T16 host lead F-14 --backup-dir order -- 2026-10-30T05:24:51Z
donor root: /workspace/artifacts/m6-donor/1a0266484423/image/system (BUILD_ID 1a0266484423); sha256sum -c ../../SHA256SUMS:
  usr/bin/busybox: OK
  usr/bin/rclone: OK
  etc/os-release: OK
the scripts and /usr/config: git show 8ebaf8daad, 12 of 12 sha256-equal to the guest's installed bytes (guest-cycle/installed.sha256)
from the donor: busybox v1.36.1 (146 applet links), rclone v1.75.2
host stand-ins (not in the donor): bash 5.3.9(1)-release (image: 5.3), timeout (GNU coreutils) 9.7 (image: 9.4), grep (GNU grep) 3.12 (image: 3.9), python3 3.14.4, ip (iproute2)
sandbox: /workspace/tmp/m6-t16/hl/sbx.sh (copied to host-leads/sandbox/) (bwrap, own pid namespace, host network); backend: cloud-test-backend at 3a653eaec4, WebDAV 127.0.0.1:9010, state /workspace/tmp/m6-t16/hl/state

before: three local saves (v1, 15 bytes each), three newer cloud copies (1 MiB each)
  saves:    ./savestates/f1.state ./savestates/f2.state ./savestates/f3.state 
  replaced: 
$ rclone copy cloud/ saves/ --backup-dir replaced/run1 --bwlimit 200k --transfers 1 --checkers 8 --stats 1s -v &
+1507 ms, mid-transfer:
  saves:    ./savestates/f1.state.b2048630.partial 
  replaced: ./run1/savestates/f1.state ./run1/savestates/f2.state ./run1/savestates/f3.state 
SIGKILL to rclone (pid 1541559) at +1525 ms
after the kill:
  saves:    ./savestates/f1.state.b2048630.partial 
  replaced: ./run1/savestates/f1.state ./run1/savestates/f2.state ./run1/savestates/f3.state 
rclone's log, its order (masked):
  2026/10/30 05:24:51 INFO  : savestates/f1.state: Moved (server-side)
  2026/10/30 05:24:51 INFO  : savestates/f2.state: Moved (server-side)
  2026/10/30 05:24:51 INFO  : savestates/f3.state: Moved (server-side)
  Transferred:   	      220 KiB / 3 MiB, 7%, 0 B/s, ETA -
  Renamed:                3
  Transferred:            0 / 3, 0%
  Server Side Moves:      3 @ 48 B

$ rclone lsf -R --files-only --filter-from <shipped cloud_sync-rules.txt> saves/   (what a backup's allowlist admits now)
savestates/f1.state.b2048630.partial
rc=0
== end 2026-10-30T05:24:53Z
```

## Evidence: guest-cycle/host-leads/k15-at-the-run/out (host lead k15-at-the-run)

```text
== T16 host lead KILL15 at the run: an empty saves-root record under each twin -- 2026-10-30T05:34:58Z
donor root: /workspace/artifacts/m6-donor/1a0266484423/image/system (BUILD_ID 1a0266484423); sha256sum -c ../../SHA256SUMS:
  usr/bin/busybox: OK
  usr/bin/rclone: OK
  etc/os-release: OK
the scripts and /usr/config: git show 8ebaf8daad, 12 of 12 sha256-equal to the guest's installed bytes (guest-cycle/installed.sha256)
from the donor: busybox v1.36.1 (146 applet links), rclone v1.75.2
host stand-ins (not in the donor): bash 5.3.9(1)-release (image: 5.3), timeout (GNU coreutils) 9.7 (image: 9.4), grep (GNU grep) 3.12 (image: 3.9), python3 3.14.4, ip (iproute2)
sandbox: /workspace/tmp/m6-t16/hl/sbx.sh (copied to host-leads/sandbox/) (bwrap, own pid namespace, host network); backend: cloud-test-backend at 3a653eaec4, WebDAV 127.0.0.1:9010, state /workspace/tmp/m6-t16/hl/state

$ (sandbox) cloud_saves_root check   (the guest cell's own invocation, for comparison)

=== cloud_saves_root check (2026-10-30T05:34:58Z); cell /workspace/tmp/m6-t16/hl/cells/k15-check.053458
rc=1
>>> why COULDN'T TELL WHICH CARD YOUR SAVES ARE ON
We can't tell which card your saves were last synced from, so nothing was transferred.
If both cards are in the device, try again.
stamps: last-restore none; last-backup none; the local save local save

=== cloud_restore --yes --saves-only (2026-10-30T05:34:58Z); cell /workspace/tmp/m6-t16/hl/cells/k15-cloud_restore.053458
rc=1
RESTORING YOUR GAME SAVES
>>> unit SAVES||
====================================
>>> why COULDN'T TELL WHICH CARD YOUR SAVES ARE ON
[31mWe can't tell which card your saves were last synced from, so nothing was transferred.
If both cards are in the device, try again.[0m
Skipped settings this time - saves only.
====================================
RESTORE SUMMARY:
Game saves: COULDN'T FINISH
[31mCouldn't finish: couldn't tell which card your saves are on. Try again.[0m
====================================
stamps: last-restore 1793338498 1 COULDN'T_TELL_WHICH_CARD_YOUR_SAVES_ARE_ON; last-backup none; the local save local save

=== cloud_backup --yes --saves-only (2026-10-30T05:34:58Z); cell /workspace/tmp/m6-t16/hl/cells/k15-cloud_backup.053458
rc=1
>>> unit SAVES||
====================================
>>> why COULDN'T TELL WHICH CARD YOUR SAVES ARE ON
[31mWe can't tell which card your saves were last synced from, so nothing was transferred.
If both cards are in the device, try again.[0m
Skipped settings this time - saves only.
====================================
BACKUP SUMMARY:
Game saves: COULDN'T FINISH
Settings backup: SKIPPED - SAVES ONLY
[31mCouldn't finish: couldn't tell which card your saves are on. Try again.[0m
====================================
stamps: last-restore none; last-backup 1793338498 1 COULDN'T_TELL_WHICH_CARD_YOUR_SAVES_ARE_ON; the local save local save
== end 2026-10-30T05:34:58Z
```

## Evidence: guest-cycle/host-leads/e-term-automatic/out (host lead e, the term and termkill arms)

```text
== T16 host lead (e) TERM to an automatic restore -- 2026-10-30T05:29:36Z
donor root: /workspace/artifacts/m6-donor/1a0266484423/image/system (BUILD_ID 1a0266484423); sha256sum -c ../../SHA256SUMS:
  usr/bin/busybox: OK
  usr/bin/rclone: OK
  etc/os-release: OK
the scripts and /usr/config: git show 8ebaf8daad, 12 of 12 sha256-equal to the guest's installed bytes (guest-cycle/installed.sha256)
from the donor: busybox v1.36.1 (146 applet links), rclone v1.75.2
host stand-ins (not in the donor): bash 5.3.9(1)-release (image: 5.3), timeout (GNU coreutils) 9.7 (image: 9.4), grep (GNU grep) 3.12 (image: 3.9), python3 3.14.4, ip (iproute2)
sandbox: /workspace/tmp/m6-t16/hl/sbx.sh (copied to host-leads/sandbox/) (bwrap, own pid namespace, host network); backend: cloud-test-backend at 3a653eaec4, WebDAV 127.0.0.1:9010, state /workspace/tmp/m6-t16/hl/state


=== arm term (2026-10-30T05:29:36Z); cell /workspace/tmp/m6-t16/hl/cells/e-term.052936
cloud_restore --automatic --yes --saves-only started, pid 5
+5s: script alive; partial: 4190208  landed: b1.state 
            5       2       5 /bin/bash /usr/bin/cloud_restore --automatic --yes --saves-only
          302       5       4 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          303     302       4 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
TERM to 5 at +5s
the script ended by +42s
its status (as its parent saw it): 130
+44s: script gone; partial:  landed: b1.state e-term.state e-termkill.state 
+54s: script gone; partial:  landed: b1.state e-term.state e-termkill.state 
+74s: script gone; partial:  landed: b1.state e-term.state e-termkill.state 
-- the script's last lines (masked):
=>  CLOUD RESTORE
====================================
RESTORING YOUR GAME SAVES
>>> unit SAVES||
====================================
-- the log: deadline, interruption, exit (masked):
[2026-10-30 05:29:36] [INFO] [cloud_restore] automatic run: --contimeout 5s --timeout 5s --retries 1 --max-duration 90s --low-level-retries 5 --transfers 1; ceiling 90s from start
2026/10/30 05:29:36 INFO  : Local file system at /storage/roms: Transfer session HARD deadline: 2026/10/30 05:31:06
[2026-10-30 05:30:17] [WARN] [cloud_restore] Script interrupted by user
[2026-10-30 05:30:17] [INFO] [cloud_restore] Script completed in 41 seconds with exit code 130
-- stamp last-restore: 1793338217 130
-- left in the saves tree: /storage/roms/gba/b2.srm /storage/roms/savestates/b1.state /storage/roms/savestates/e-term.state /storage/roms/savestates/e-termkill.state 
sandbox rc=0 at 2026-10-30T05:30:50Z

=== arm termkill (2026-10-30T05:30:50Z); cell /workspace/tmp/m6-t16/hl/cells/e-termkill.053050
cloud_restore --automatic --yes --saves-only started, pid 5
+5s: script alive; partial: 3141632  landed: b1.state 
            5       2       5 /bin/bash /usr/bin/cloud_restore --automatic --yes --saves-only
          298       5       4 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          299     298       4 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
TERM to 5 at +5s
+7s: script alive; partial: 3141632  landed: b1.state 
            5       2       7 /bin/bash /usr/bin/cloud_restore --automatic --yes --saves-only
          298       5       6 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          299     298       6 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
+9s: script alive; partial: 4190208  landed: b1.state 
            5       2       9 /bin/bash /usr/bin/cloud_restore --automatic --yes --saves-only
          298       5       8 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          299     298       8 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
KILL to 5 at +9s
/drv/e.sh: line 17:     5 Killed                     cloud_restore --automatic --yes --saves-only > /tmp/e.out 2>&1
the script ended by +9s
its status (as its parent saw it): 137
+11s: script gone; partial: 4190208  landed: b1.state 
          298       1      10 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          299     298      10 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
+21s: script gone; partial: 5238784  landed: b1.state 
          298       1      20 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          299     298      20 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
+41s: script gone; partial: 1044480  landed: b1.state e-term.state 
          298       1      40 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          299     298      40 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
-- the script's last lines (masked):
=>  CLOUD RESTORE
====================================
RESTORING YOUR GAME SAVES
>>> unit SAVES||
====================================
-- the log: deadline, interruption, exit (masked):
[2026-10-30 05:30:50] [INFO] [cloud_restore] automatic run: --contimeout 5s --timeout 5s --retries 1 --max-duration 90s --low-level-retries 5 --transfers 1; ceiling 90s from start
2026/10/30 05:30:50 INFO  : Local file system at /storage/roms: Transfer session HARD deadline: 2026/10/30 05:32:20
-- stamp last-restore: none
-- left in the saves tree: /storage/roms/savestates/b1.state /storage/roms/savestates/e-term.state /storage/roms/savestates/e-termkill.state.73cdc66a.partial 
sandbox rc=0 at 2026-10-30T05:31:31Z
== end 2026-10-30T05:31:31Z
```

## Evidence: guest-cycle/host-leads/e-term-automatic/out-game (host lead e, the termkill-game arm)

```text
== T16 host lead (e) TERM to an automatic restore -- 2026-10-30T05:32:15Z
donor root: /workspace/artifacts/m6-donor/1a0266484423/image/system (BUILD_ID 1a0266484423); sha256sum -c ../../SHA256SUMS:
  usr/bin/busybox: OK
  usr/bin/rclone: OK
  etc/os-release: OK
the scripts and /usr/config: git show 8ebaf8daad, 12 of 12 sha256-equal to the guest's installed bytes (guest-cycle/installed.sha256)
from the donor: busybox v1.36.1 (146 applet links), rclone v1.75.2
host stand-ins (not in the donor): bash 5.3.9(1)-release (image: 5.3), timeout (GNU coreutils) 9.7 (image: 9.4), grep (GNU grep) 3.12 (image: 3.9), python3 3.14.4, ip (iproute2)
sandbox: /workspace/tmp/m6-t16/hl/sbx.sh (copied to host-leads/sandbox/) (bwrap, own pid namespace, host network); backend: cloud-test-backend at 3a653eaec4, WebDAV 127.0.0.1:9010, state /workspace/tmp/m6-t16/hl/state


=== arm termkill-game (2026-10-30T05:32:15Z); cell /workspace/tmp/m6-t16/hl/cells/e-termkill-game.053215
cloud_restore --automatic --yes --saves-only started, pid 5
+5s: script alive; partial: 4190208  landed: b1.state 
            5       2       5 /bin/bash /usr/bin/cloud_restore --automatic --yes --saves-only
          301       5       4 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          302     301       4 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
TERM to 5 at +5s
+7s: script alive; partial: 4190208  landed: b1.state 
            5       2       7 /bin/bash /usr/bin/cloud_restore --automatic --yes --saves-only
          301       5       6 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          302     301       6 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
+9s: script alive; partial: 4190208  landed: b1.state 
            5       2       9 /bin/bash /usr/bin/cloud_restore --automatic --yes --saves-only
          301       5       8 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          302     301       8 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
KILL to 5 at +9s
/drv/e.sh: line 17:     5 Killed                     cloud_restore --automatic --yes --saves-only > /tmp/e.out 2>&1
+11s: the game wrote /storage/roms/savestates/e-term.state (10 bytes) while e-term.state.cfedb2b3.partial is open
the script ended by +11s
its status (as its parent saw it): 137
+13s: script gone; partial: 5238784  landed: b1.state e-term.state 
          301       1      12 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          302     301      12 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
+23s: script gone; partial: 126976  landed: b1.state e-term.state 
          301       1      22 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          302     301      22 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
+43s: script gone; partial: 2093056  landed: b1.state e-term.state 
          301       1      42 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          302     301      42 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
+73s: script gone; partial: 5238784  landed: b1.state e-term.state 
          301       1      72 timeout -k 3 90 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt 
          302     301      72 rclone copy --progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt --log-level INFO
-- the game's file at the end: /storage/roms/savestates/e-term.state, 6291456 bytes, NOT the game's bytes: the orphan's rename landed on it
-- the script's last lines (masked):
=>  CLOUD RESTORE
====================================
RESTORING YOUR GAME SAVES
>>> unit SAVES||
====================================
-- the log: deadline, interruption, exit (masked):
[2026-10-30 05:32:15] [INFO] [cloud_restore] automatic run: --contimeout 5s --timeout 5s --retries 1 --max-duration 90s --low-level-retries 5 --transfers 1; ceiling 90s from start
2026/10/30 05:32:15 INFO  : Local file system at /storage/roms: Transfer session HARD deadline: 2026/10/30 05:33:45
-- stamp last-restore: none
-- left in the saves tree: /storage/roms/gba/b2.srm /storage/roms/savestates/b1.state /storage/roms/savestates/e-term.state /storage/roms/savestates/e-termkill-game.state.1c0fbb98.partial 
sandbox rc=0 at 2026-10-30T05:33:28Z
== end 2026-10-30T05:33:28Z
-- after the sandbox (host read, 2026-10-30T05:33:40Z): files under the cell's /storage/.cache: 
-- files anywhere under the cell's /storage whose bytes are exactly the game's 10: 0 (a whole-content cmp; a grep for the words matched a comment in cloud_sync.conf)
```

## Evidence: guest-cycle/cells-1.out (KILL15 on the guest)

```text
=== KILL15 -- an empty saves-root record refuses instead of reading as none
    PASS  an empty saves-root record is refused (exit 1) rather than read as none
    PASS  check: no developer words on the 0 card-visible line(s) or the outcome line ('If both cards are in the device, try again.')
    FAIL  check: the outcome line is not Completed / Couldn't finish / Skipped: 'If both cards are in the device, try again.'
    PASS  check: a failed run says how to recover
    PASS  record rewrites the identity (uuid:4e65d46a-9bfe-4c84-b957-6c8a3a555999)
    PASS  no saves-root temp left
    PASS  KILL15: one record each, no litter: system.cfg 226 keys, record .backup; es_settings.cfg 0 keys; 7 last-* stamps, 0 capture line(s), 0 manifest; 0 archive at root, 0 in archive/; saves tree clean of *.partial/*.tmp; cloud 0 settings file(s)
    (KILL15 took 0s)
```

## Evidence: guest-cycle/cells-3.out (KILL2 on the guest, 200k)

```text
=== KILL2 -- saves restore stopped mid-download by ES's TERM-then-KILL (D-CLOUD-076): the game's save stands, *.partial litter, re-run keeps the previous version
    PASS  2a: TERM then KILL at 1.5s: the group was empty 0.01s after the signal (budget 2s), mid-download of 'savestates/kill2-3.state'
    PASS  2a: the save the game wrote 1s after the stop still stands 5s later (no rename landed on it)
    FAIL  2a: a file is torn or gone: {'savestates/kill2-1.state': 'absent', 'savestates/kill2-2.state': 'absent'}
    PASS  2a: no rclone *.partial left under SAVESPATH
    PASS  2a: last-restore is 1793297958 130: the stop is recorded, never as 0
          outputs kept: /tmp/qa-link-KILL2a/ on the guest, /workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663/docs/audits/2026_10_25-epic-m6-cloud-sync-core/guest-cycle/cells-3/KILL2a/ here
    PASS  2a: a plain re-run exits 0
    PASS  2a: after the re-run: the game's save kept, the rest v2 ({'savestates/kill2-1.state': 'v2', 'savestates/kill2-2.state': 'v2', 'savestates/kill2-3.state': 'v3'})
    PASS  2a: the previous version of every overwritten save is kept somewhere (2 checked)
    PASS  2a re-run: no developer words on the 91 card-visible line(s) or the outcome line ('Completed.')
    PASS  2a re-run: the outcome line is one of the three outcome words ('Completed.')
    PASS  2b: SIGKILL mid-download of 'savestates/kill2-1.state': the group was gone in 0.01s
    PASS  2b: the save the game wrote 1s after the stop still stands 5s later (no rename landed on it)
    FAIL  2b: a file is torn or gone: {'savestates/kill2-2.state': 'absent', 'savestates/kill2-3.state': 'absent'}
    FAIL  2b: rclone's temporary copy left under SAVESPATH, and nothing removes it: ['savestates/kill2-2.state.fc23ea21.partial', 'savestates/kill2-1.state.8042cffa.partial', 'savestates/kill2-3.state.612c0b57.partial'] (D-CLOUD-078: litter forever)
    PASS  2b: last-restore unchanged (1793297989 0) -- nothing ran after SIGKILL
          outputs kept: /tmp/qa-link-KILL2b/ on the guest, /workspace/repos/pixelelated/distribution.worktrees/m6-cloud-sync-core-663/docs/audits/2026_10_25-epic-m6-cloud-sync-core/guest-cycle/cells-3/KILL2b/ here
    PASS  2b: a plain re-run exits 0
    PASS  2b: after the re-run: the game's save kept, the rest v2 ({'savestates/kill2-1.state': 'v3', 'savestates/kill2-2.state': 'v2', 'savestates/kill2-3.state': 'v2'})
    PASS  2b: the previous version of every overwritten save is kept somewhere (2 checked)
    PASS  2b re-run: no developer words on the 91 card-visible line(s) or the outcome line ('Completed.')
    PASS  2b re-run: the outcome line is one of the three outcome words ('Completed.')
    PASS  KILL2: one record each, no litter: system.cfg 226 keys, record .backup; es_settings.cfg 0 keys; 7 last-* stamps, 0 capture line(s), 0 manifest; 0 archive at root, 0 in archive/; saves tree clean of *.partial/*.tmp; cloud 0 settings file(s)
    (KILL2 took 74s)
```

## Excerpt: tools/cloud-round-trip (at 3a653eaec4; fx_kill15, F-15)

```text
 7747  def fx_kill15(L):
 7748      """KILL15: `cloud_saves_root record` writes its one-line record in place
 7749      (`echo >`, a builtin: no external kill lands in it), so the torn state is
 7750      planted -- an empty saves-root. Asserted: `check` REFUSES an empty record
 7751      (with the accept instruction), because `-s` false reads today as "no
 7752      record" and the #83 guard is silently off (FAIL, fails open); the refusal
 7753      text carries no CLI name (assert_message)."""
 7754      f = 0
 7755      rec = L.dev.run(f"cat {CACHE}/saves-root 2>/dev/null || true", check=False)
 7756      if not rec.strip():
 7757          rc0, _ = run_rc(L.dev, "cloud_saves_root record")
 7758          rec = L.dev.run(f"cat {CACHE}/saves-root 2>/dev/null || true", check=False)
 7759          if not rec.strip():
 7760              raise Fail(f"cloud_saves_root record wrote no record (rc {rc0})")
 7761      L.cleanups.append(lambda: L.dev.write(f"{CACHE}/saves-root", rec.encode()))
 7762      L.dev.run(f"mkdir -p {CACHE}; : > {CACHE}/saves-root")
 7763      rc, out = run_rc(L.dev, "cloud_saves_root check")
 7764      f += not check(rc != 0, "an empty saves-root record is refused (exit 1) rather than read as none",
 7765                     f"cloud_saves_root check exited {rc} on an EMPTY record: the #83 guard fails open (cloud_saves_root:109 tests -s)")
 7766      f += assert_message(out, rc, L.args.vocabulary, label="check: ")
 7767      rc2, out2 = run_rc(L.dev, "cloud_saves_root record")
 7768      now = L.dev.run(f"cat {CACHE}/saves-root 2>/dev/null || true", check=False).strip()
 7769      f += not check(rc2 == 0 and now == rec.strip(), f"record rewrites the identity ({now})", f"record (rc {rc2}) left {now!r}, expected {rec.strip()!r}")
 7770      temps = L.dev.run(f"ls {CACHE}/saves-root.* {CACHE}/.saves-root* 2>/dev/null; true", check=False).split()
 7771      f += not check(not temps, "no saves-root temp left", f"temps left: {temps}")
 7772      return f
```

---

# Appended: the first reader's grades of the second reader's items (04 § Second opinion, 2026-10-30, after Astra)

## Second opinion (Phase 4.6)

Depth **extended** (`second-opinions/review-plan.json`): the primary (Anthropic, Opus 5.5) and two reviewers from other labs. Each seat ran its probe first, then its refutation, through the Facilitator.

**Both seats saw the same trimmed packet** (D-WORKFLOW-195): `02` to `04` whole, the eleven smaller files whole, and the three large scripts in excerpt (`second-opinions/packet-manifest.json` lists the spans). Argon's brief also carries Astra's grades below. An item resting on lines a seat saw only in excerpt says so, and is graded from the file, not from either seat.

| Seat | Call | Provenance | Served | Outcome |
| --- | --- | --- | --- | --- |
| GPT-6 Astra, `max` | probe 09:26:11-09:26:20 (`READY unknown`); refutation `tools/council/run invoke --member gpt --provider openrouter`, brief `second-opinions/gpt-brief.md` (381,240 bytes), under `tools/watch-build --record-only` (`.build-runs/20261030T092635Z-597bc6f5/`, `build.rc` 0), 09:26:35-09:43:20 | `gpt-probe.md.provenance.json`, `gpt-audit.md.provenance.json`: `council-facilitator@1.14.1-pixelelated.2`; verification PASS (`provider_response`), provider PASS (`response_provider_field`), effort PASS (41,752 reasoning tokens); 1 attempt, `finish=stop`, 1,002,690 ms | `openai/gpt-6-astra` by OpenAI | `gpt-audit.md`, 26,238 bytes, sha256 `c872717a1a8ea3b88e8ddcbe1ca86e3ea2ed70d6d8c6fced222f96570acb206c`: 19 items of its own, the 15 findings graded |

### Astra's items, graded against the artifacts

Each grade comes from re-reading the cited lines at `8ebaf8daad` (09:43-09:47 UTC), not from the seat's wording. One item was also run: G-01, as a host cell. The grades are:
- **confirmed** (the lines show it);
- **confirmed, re-graded** (they show it, at another severity);
- **narrowed** (part of it holds);
- **design** (the lines show it, and a comment beside them gives the reason);
- **disagree** (with the artifact that refutes it).

| Item | Grade | The lines read, and what they show |
| --- | --- | --- |
| G-01 `timeout`'s own process group | **confirmed, High; widens F-03** | GNU `timeout` without `--foreground` makes its own process group. `guest-cycle/host-leads/g01-timeout-pgid` (GNU 9.7): after a TERM to the script's group, the script is gone and `timeout` and its child run on to `timeout`'s own deadline. So a group stop does not end an automatic transfer either (`cloud_restore:359`, `cloud_backup:372`); only a stop that reaches `timeout`'s group, or the whole session, does |
| G-02 migration markers after an unchecked `sed` | **confirmed, Medium** | `cloud_sync_helper:576-577`: `sed -i` then `touch` the marker, whatever `sed` returned. A rewrite that fails (a full card) leaves `BACKUPMETHOD="sync"`, the mirror that deleted another device's 70 saves (`:548-552`), and the marker stops every retry. The two option migrations (`:594-596`, `:613-615`) have the same shape, with less at stake |
| G-03 card identity by path prefix | **confirmed, Low** | `cloud_saves_root:56-68` matches `/proc/mounts` by prefix, unresolved and unescaped. The shipped layout binds the card over `/storage/roms` (`:53-55`), which this reads right. A `SAVESPATH` through a symlink, or a mount point with a space, is the owner's own setting |
| G-04 `dev:unknown` accepted | **confirmed, Low** | `:83` gives `dev:unknown` when `stat` fails; with no record, `check` passes it (`:143-164`), and `record` can keep it. The next run with the path present reads `uuid:` and refuses, so it fails closed one run late |
| G-05 unchecked writes to `/tmp` | **confirmed, Low** | `cloud_sync_helper:81-94`: `: >` and `echo >>` into `/tmp/cloud_sync-rules.user` are unchecked. A failed write drops the player's rules, and `rules_whole` (`:145`) cannot see it. `/tmp` is tmpfs, so a full one is rare |
| G-06 a truncated rules file merged | **confirmed, Low** | `:79-98` merges whatever `${rules}` holds. `:168-173` keeps the last whole `.bak` and does not overwrite it from a cut file, so the lost lines are recoverable by hand |
| G-07 a backslash in a trailing comment | **confirmed, Low** | `cloud_sync_cleanup_duplicates.sh:15,22-24` treats any trailing `\` as a continuation, and bash does not continue a comment. A repeated assignment whose comment ends in `\` removes the next line. The owner's own conf, in an unusual shape |
| G-08 no FIFO, no ceiling | **design, Low** | `cloud_restore:241-249` (and the twin) runs rclone unbounded when no FIFO can be made. The comment at `:242-245` gives the reason: on a device `/var/run` is tmpfs, and refusing the backup would be worse. The trade is written down |
| G-09 deadlines on the wall clock | **confirmed, Low** | `cloud_backup:8,1403` and `cloud_restore:347` (and `cloud_saves_root:108-110`) count from `date +%s`. **The likelier shape is a forward step**, not Astra's backward one: a handheld with no RTC is stepped forward by NTP near the startup sync, so `left` goes below 1 and the run ends at once with 124 (`:353-355`). No save is lost; the next sync carries it. The guest can step the clock mid-run (stage E) |
| G-10 `restore-tree-clean` after a failed sweep | **confirmed, Low** | `cloud_restore:1597` hides `find -exec rm`'s failures, and `:1912-1913` writes the marker regardless. A card that refuses the delete leaves `.partial`s that later runs do not look for, and that the allowlist admits (F-14) |
| G-11 the helper has no lock of its own | **narrowed, Low** | The fixed names are at `:81-82,119`. Its callers are the twins, under `cloud_sync.lock` (`cloud_backup:1199`, `cloud_restore:1248`), and `post-update:111` after an update (`git grep` at `8ebaf8daad`). An overlap needs `post-update` during a twin's run |
| G-12 the database sidecars | **confirmed, Low** | `cloud_sync-rules.txt:10-15` excludes `*.db-wal`, `*.db-shm` and `*.db-journal`, but not `*.sqlite-wal`, `-shm` or `-journal`, nor `*.sqlite3`'s. A lone WAL restored beside a different database is applied on its next open. No shipped emulator is named as writing one there |
| G-13 the sweep's pattern | **confirmed, Low** | `cloud_restore:1597` removes any `*.????????.partial` under the saves tree, so a file of that shape the cloud holds is removed after a dirty-tree restore. Contrived |
| G-14 the empty record cannot be retried away | **confirmed, Medium** | `cloud_saves_root:131-141` refuses on an empty record, and says "try again". The twins refuse at `check` (`cloud_restore:1648-1651`) and call `record` only after a completed transfer (`:1931-1940`), so no run can ever rewrite it. The only exit is `cloud_setup --accept-saves-root`, a command, and `:154-155` says no menu offers one. The comment at `:135` ("until a good run rewrites it") cannot come true. Today's `write_record` is temp-and-rename (`:94-101`); a record left empty by an older build's in-place write is the `Already written:` |
| G-15 `cloud_net_ready`'s bound | **confirmed, Low** | `NOW` is sampled at `:131`, before up to two 5 s `nmcli` calls (`:107-108,167-169`), and `timeout 5` has no `-k`. A slow NetworkManager stretches `N + GRACE` by up to about 10 s a round |
| G-16 a fresh device's first `sync` | **confirmed, Low** | `cloud_sync_helper:569-577` sets its marker only when it rewrites, so a device that never had `sync` has none. The owner's first deliberate `sync` is rewritten once, against `cloud_sync.conf:124-126` ("honoured if set here") |
| G-17 `unpack()` | **confirmed, Low; joins F-10** | `package.mk:54-58`: no `set -e` reaches `scripts/unpack` at `8ebaf8daad` (`git grep`), so a failed `unzip` runs on into the `rm`, which deletes the archive a retry needs |
| G-18 leading zeros | **confirmed, Low** | `cloud_net_ready:72-73` accepts `010`, and `:122` reads it as octal (8 s). `08` is an arithmetic error. Its callers pass fixed numbers |
| G-19 `CONTENT_REMOTE`'s comment | **confirmed, Low; joins F-09** | `cloud_sync.conf:40-45` (and its `.defaults`) says the key is derived for an upgrading config. `cloud_sync_helper:463-466` says a missing key takes the fresh default, as D-CLOUD-175 decided |

**The first reader's findings, as Astra graded them:**

| Finding | Astra | Graded |
| --- | --- | --- |
| F-01 | agree, Medium; "the defect is a read" is wrong | **correction taken.** A refused line runs as root when the put-back fails (the fixture's planted line ran). `Already written:` now says so |
| F-02 | narrow the empty path (Low); raise the readers' disagreement to Medium | **taken: F-02 is Medium, in two parts.** The empty path stays Low: nothing written, the wrong why. The disagreement is Medium. A non-default `SAVESPATH` with a trailing comment is sourced by the twins, while `cloud_saves_root:48` and `cloud_capture:193-198` miss it and read `/storage/roms`. The card guard then checks the wrong card (`02` § The configuration, the fixture) |
| F-03 | agree, High; the condition is wider (G-01) | **taken.** Any stop that does not reach `timeout`'s group leaves the transfer running. That is a signal to the script or to its group. The ES slice reads which stop ES makes |
| F-04 | narrow, Low | **taken.** Only exit 7's words are shown in a run (`b-empty-savespath`); the rest of the inventory is in excerpt |
| F-05 | Medium to Low: no measurement | **taken: Low until lead (c) measures it.** The probes' futility stands (`d-terminal-width`) |
| F-06 | narrow: `logged_moved`'s stderr half works | **taken.** The log half sees only what is appended after the transfer; the stderr half (`cloud_backup:349-354`) stands |
| F-07 | Low to Medium: the `-v` edit can rename a folder | **disagree with the re-grade, Low.** Both shapes are at `:462` and `:536-542`, but the folder change needs two things in the owner's own conf: a `-v` or `--verbose` somewhere, and a double space or `-v ` inside a value |
| F-08 | Low to Medium: the seals are preservation copies | **narrowed: Low today, Medium once a reader exists.** No consumer of `stage/` exists (#1057), so nothing a player has is lost today. The item carries to #1057 |
| F-09 | agree, Low | taken |
| F-10 | narrow: a rebuild needing the archive | **taken**, with G-17 |
| F-11 | agree, a design | taken |
| F-12 | narrow, Low: no shutdown measured | **taken.** It stays `(window)` |
| F-13 | agree, Low | taken |
| F-14 | Medium to High; narrow "every save before any transfer" | **taken, both.** A save the game needs is absent until a completed restore, which is High under the lens. The ordering claim narrows to what was observed: the saves are moved aside early, before their replacements land. On the host, all three moved before the first copy completed. `02` and Q3 say so |
| F-15 | agree; G-14 is separate | taken |

**What Astra could not judge** (its § 3): the bodies the trimming left out, namely `conf_valid` (twins), `clean_exit`, most of `cloud_backup`'s main and its settings phase, the restore's pre-flight and card handling, the capture's seal and commit protocol, and `why_for`. It also lacked EmulationStation's stop, the guest's timings, power-cut durability, T17's callees and the whole oracle. None of its items rests on an omitted line except F-04's inventory. The ES stop and the guest timings are `(window)`-pending already.
