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

**Graded at stage C** (§ The host leads, below): KILL15's FAIL is the harness's (F-15, the coordinator's Backlog #1296); KILL2's absent saves are F-14 (#1299). The `.partial` FAIL's "nothing removes it" is the cell's word, not the code's: the re-run's `sweep_partials` removes them (`cloud_restore:1898-1913`; the cell's own last check reads the tree clean).

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
| `k15-at-the-run` (KILL15) | an empty saves-root record; `cloud_saves_root check` alone, then each twin `--yes --saves-only`, in the sandbox | check alone ends `If both cards are in the device, try again.` Both twins end `Couldn't finish: couldn't tell which card your saves are on. Try again.`, rc 1, stamp `1 COULDN'T_TELL_WHICH_CARD_YOUR_SAVES_ARE_ON`; the local save untouched | **KILL15's FAIL is the harness's.** `fx_kill15` (`tools/cloud-round-trip:7747-7772`) asserts a run's outcome line on a helper whose lines reach a player only through the twins, which end on an outcome sentence (F-15, #1296) | fixture |

**Still `(window)`-pending (stage E and the integration window, `fix-walk-pending-image`):**
- lead (c), every timing on the image (F-05);
- F-03 under the image's own bash 5.3 and coreutils 9.4. The host ran 5.3.9 and 9.7: the trap's deferral is bash's documented order, and the orphan's bound is `timeout`'s own;
- how EmulationStation stops an automatic run, which is the ES slice's. A group kill gives F-14; a signal to the script alone gives F-03.

**No second window is asked for.** No host lead found a fact that only the guest can settle, beyond the three named here.

## The ES stop and the why texts (stage D, read at the ES pin)

The ruling asks for these two reads; nothing in EmulationStation is changed here. **The pin:** the distribution's `emulationstation/package.mk` at `8ebaf8daad` names `PKG_VERSION="16dbac5211eea7e70db7394372033be2be7df829"`. That commit was read with `git show` from the local clone `~/Development/emulationstation-next`, with no fetch.

**How STOP IT AND PLAY stops a sync** (#1298, PL-01):

| What | Where (`16dbac5211`) | What it shows | proved: |
| --- | --- | --- | --- |
| the startup sync's command | `es-app/src/main.cpp:681-684` | `cloud_restore --yes --method=copy --update --saves-only --automatic`, then `cloud_backup ... --automatic`, in one shell | tree |
| the exit sync's command | `es-app/src/FileData.cpp:1310`, `es-app/src/ProxyCards.cpp:34` | `cloud_backup --yes --saves-only --recent --automatic` | tree |
| how every command runs | `es-app/src/ThreadedCloudSync.cpp:198-207` | `setsid sh -c 'echo ">>> pid $$"; <command>' 2>&1` through `popen`: the shell leads a process group, and its pid names it | tree |
| which signal, to which pid | `ThreadedCloudSync.cpp:809-818`, `:845-850`, `:857-861` | SIGTERM to the group (`::kill(-pid, SIGTERM)`), SIGKILL to the group at 1.5 s | tree |
| when the stop counts as done | `ThreadedCloudSync.cpp:820-833`, `:836-856` | only when `pclose` returns (every writer to the pipe gone), within 2 s; otherwise `false` | tree |
| STOP IT AND PLAY's branch | `es-app/src/FileData.cpp:993-1006` | `cancelForLaunch(&again, true)`; on `false`, `launchWhenGone` | tree |
| the wait behind the spinner | `FileData.cpp:812-850` | STOPPING IT SO YOU CAN PLAY... up to 20 s for `isRunning()` to clear; then IT DIDN'T STOP IN TIME. TRY AGAIN IN A MOMENT., and no launch | tree |

**What that means with #1298's defect:**
- The automatic call's `timeout` and `rclone` are outside the shell's group (`host-leads/g01-timeout-pgid`), so neither signal reaches them.
- They hold the pipe, so `pclose` waits for them. **At the pin the gate holds the launch until the orphan's transfer ends:** the player waits up to 20 s, or is refused.
- The stop stops nothing, and the run's stamp says it was stopped.
- The host's `out-game` arm (a game writing under the orphan) needs a launch this gate does not hold. None was found at the pin.

**The why texts** (PL-11; the ruling's rule: the six rc-keyed sentences change on both sides or on neither):

| rclone rc | The scripts (`8ebaf8daad`) | ES's fallback map (`16dbac5211`) | `es-player-text.md` (`.claude/rules/`, on this branch) |
| --- | --- | --- | --- |
| 3, 4 | `COULDN'T FIND YOUR CLOUD FOLDER` (`cloud_restore:836`, `cloud_backup:830`) | `COULDN'T FIND YOUR CLOUD FOLDER` (`ThreadedCloudSync.cpp:84`; `CloudText.cpp:439`) | `YOUR CLOUD FOLDER WASN'T FOUND` (`:270-271`) |
| 7, 8 | `YOUR CLOUD WOULDN'T TAKE THE FILES` (`cloud_restore:839`, `cloud_backup:833`) | `YOUR CLOUD WOULDN'T TAKE THE FILES` (`ThreadedCloudSync.cpp:86`; `CloudText.cpp:441`) | `YOUR CLOUD REFUSED THE TRANSFER` (`:271-272`). The rule's own D-UI-031 table at `:228` gives `WOULDN'T TAKE THE FILES` as the replacement |
| the sign-in check | `COULDN'T REACH YOUR CLOUD - CHECK YOUR SIGN-IN` (`cloud_restore:1032`, `cloud_backup:979`) | the same (`CloudText.cpp:426`) | `COULDN'T REACH YOUR CLOUD. YOU MAY NEED TO SIGN IN AGAIN` (`:272-273`) |
| the ceiling (124) | `THE CLOUD TOOK TOO LONG - IT'LL TRY AGAIN NEXT TIME` (`cloud_restore:846`, `cloud_backup:840`) | the same (`CloudText.cpp:443`) | in no table |

**The outcome, under the ruling:**
- For 3/4 and 7/8, **the scripts and ES's map agree, and the rule differs**. So the rule is the coordinator's to correct, named in the hand-back.
- The two sentences F-04 found in no table go to #909 with their texts:
  - the ceiling's;
  - the sign-in check's, whose exact words the rule does not carry. The scripts and ES agree on it; the rule words it otherwise (`:272-273`).

KILL15's FAIL (F-15) is the coordinator's Backlog #1296.

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
