#!/bin/bash
# T17 (#664) stage A: the brief's section 5 runs, each with its exit and wall time.
# Read-only: no fetch, no build, no compiler, no plan, no guest, nothing on a
# handheld, no M7 build root or worktree, no tools/council/run call. Counts are
# taken unfiltered; every run that prints source lines passes them through the
# read filter (D-QA-021).
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-setup-content-664
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t17/tmp
OUT=/workspace/tmp/m6-t17/runner/out
RUN=/workspace/tmp/m6-t17/runner
R=8ebaf8daad; P=projects/ROCKNIX/packages/network/rclone/sources
BT=projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
DISPATCH=f3803436b8
mkdir -p "$TMPDIR" "$OUT" .qa-scratch/t17
printf 'id\trc\tseconds\tstarted_utc\n' > "$OUT/runs.tsv"
F() { grep -v -i -E 'key|pass|token|user|psk'; }
run() {
  local id=$1; shift
  local t0 t1 rc started
  started=$(date -u +%H:%M:%S); t0=$(date +%s.%N)
  ( "$@" ) > "$OUT/$id.out" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  printf '%s\t%s\t%.2f\t%s\n' "$id" "$rc" "$(echo "$t1 - $t0" | bc)" "$started" >> "$OUT/runs.tsv"
}
paths() { tr '\n' ' ' < .qa-scratch/t17/paths.txt; }
r01_block() { python3 -I "$RUN/scope.py"; wc -l < .qa-scratch/t17/paths.txt; }
r02_modes() { tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git ls-tree -l $R -- | awk '{print $1}' | sort | uniq -c; }
r03_lines() { while IFS= read -r p; do printf '%6d %s\n' "$(git show "$R:$p" | wc -l)" "$p"; done < .qa-scratch/t17/paths.txt | awk '{s+=$1; print} END {print "lines", s}'; }
r04_shell_functions() { for f in cloud_content_backup cloud_content_restore cloud_content_transfer cloud_device_id cloud_log_scrub cloud_scan cloud_setup; do printf '%s strict %s loose %s\n' "$f" "$(git show "$R:$P/$f" | grep -c -E '^[a-z_]+\(\) \{$')" "$(git show "$R:$P/$f" | grep -c -E '^[a-z_]+\(\)')"; done; printf 'backuptool strict %s loose %s\n' "$(git show "$R:$BT" | grep -c -E '^[a-z_]+\(\) \{$')" "$(git show "$R:$BT" | grep -c -E '^[a-z_]+\(\)')"; }
r05_python_defs() { for f in cloud_oauth cloud_remote cloud_folder_validate cloud_connections.py; do printf '%s %s defs %s classes\n' "$f" "$(git show "$R:$P/$f" | grep -c -E '^\s*def ')" "$(git show "$R:$P/$f" | grep -c -E '^class ')"; done; }
r06_set_discipline() { tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git grep -n -E '^\s*set -[eux]|set -o pipefail|\beval\b' $R -- | sed "s/^$R://" | grep -v -E '^[^:]+:[0-9]+:\s*#' | F; }
r07_exit_constants() { git grep -n -E 'readonly EXIT_|^EXIT_[A-Z_]+=' $R -- "$P" | sed "s/^$R://" | F; }
r08_writer_rclone_conf() { git grep -n -E 'rclone\.conf|mkstemp|os\.replace|chmod\(0o600\)|umask' $R -- $(paths) | sed "s/^$R://" | F | grep -v -E ':[0-9]+:\s*#'; }
r09_setup_remote_config() { git show "$R:$P/cloud_setup" | grep -n 'rclone config' | grep -v -E '^[0-9]+:\s*#' | F | cut -c1-120; echo '--- cloud_remote'; git show "$R:$P/cloud_remote" | grep -n -E 'connections\.(save|select|remove)|rclone\(|^import |^from ' | F | cut -c1-120; }
r10_deleting_statements() { git grep -n -E 'rclone (delete|purge|sync|move|rmdir)|bounded_content_rclone (sync|delete|move|purge)' $R -- $(paths) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#' | F; }
r11_delete_excluded() { git grep -n -- '--delete-excluded' $R -- $(paths) | sed "s/^$R://" | F; }
r12_rm_rf() { git grep -n -E 'rm -rf' $R -- $(paths) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#' | wc -l; git grep -n -E 'rm -rf' $R -- $(paths) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#' | F | cut -c1-160; }
r13_match_refusals() { git show "$R:$P/cloud_content_restore" | sed -n '886p;890,893p;898,900p;904,906p;1046,1049p' | F; }
r14_pattern_kills() { git grep -n -E 'pkill|killall' $R -- $(paths) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#' | F; }
r15_unquoted() { git grep -n -E '\[ -[a-z] \$\{[A-Z_]+\} |>> \$\{[A-Z_]+\}$' $R -- $(paths) | sed "s/^$R://" | F; }
r16_dollar_dollar() { git grep -n -E '\.\$\$' $R -- $(paths) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#' | wc -l; git grep -n -E '\.\$\$' $R -- $(paths) | sed "s/^$R://" | grep -v -E ':[0-9]+:\s*#' | F | cut -c1-160; }
r17_oauth_bounds() { git show "$R:$P/cloud_oauth" | grep -n -E '^(STATE_DIR|RCLONE|LOCAL_AUTH|LOG_FILE|MAX_BODY|REQUEST_TIMEOUT|MAX_CONNECTIONS) =|0o600|secrets\.(randbelow|compare_digest)|def (log|state_path|_write_whole|write_state|write_owned|read_state|lan_address|serve_with|cmd_serve)\b|class BoundedHTTPServer' | F; }
r18_backuptool_lists() { git show "$R:$BT" | sed -n '690,760p' | grep -v -E '^\s*#' | grep -v -E '^\s*$' | F; }
r19_backuptool_shape() { git show "$R:$BT" | grep -n -E '^ARCHIVE_KEEP=|A SIGN-IN WAS FOUND|\.partial|^[a-z_]+\(\)' | F | head -60; }
r20_backuptool_logger() { git show "$R:$BT" | grep -c 'logger -t backuptool'; }
r21_device_id() { git show "$R:$P/cloud_device_id" | sed -n '54p;58p;144p;170p;175p;289,292p' | F; }
r22_validate_bounds() { git show "$R:$P/cloud_folder_validate" | grep -n -E 'MAX_BYTES|MAX_ENTRIES|TOTAL_SECONDS|contimeout|max-duration|DEVNULL|class Unreadable' | F; }
r23_scan_routing() { git show "$R:$P/cloud_scan" | sed -n '43p;150,166p' | F; }
r24_scrub_hook() { git grep -n 'cloud_log_scrub' $R -- projects/ROCKNIX/packages/network/rclone/autostart/102-cloud-saves | sed "s/^$R://"; git show "$R:$P/cloud_log_scrub" | grep -n -E 'log-scrubbed|^SCRUB_SED|set -o pipefail'; }
r25_history() { tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git log --no-merges --format='%h %an' c445081a59..$R -- > "$TMPDIR/hist.txt"; wc -l < "$TMPDIR/hist.txt"; cut -d' ' -f2- "$TMPDIR/hist.txt" | sort | uniq -c | sort -rn; }
r26_history_span() { tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git log --no-merges --format='%ad' --date=short c445081a59..$R -- | sort | sed -n '1p;$p'; }
r27_history_june() { tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git log --no-merges --format=%h --since='2026-06-01T00:00:00Z' $R -- | wc -l; }
r28_history_backuptool() { git log --no-merges --format=%h c445081a59..$R -- "$BT" | wc -l; }
r29_upstream_presence() { for c in 651150fc88 c445081a59; do tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git ls-tree --name-only $c -- 2>/dev/null; done | sort | uniq -c; }
r30_upstream_backuptool() { git show 651150fc88:$BT | wc -l; git diff --quiet 651150fc88 c445081a59 -- $BT && echo identical; }
r31_upstream_diffstat() { tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git diff --stat $R 651150fc88 -- | tail -1; }
r32_callers() { for n in cloud_oauth cloud_setup cloud_remote cloud_connections cloud_content_backup cloud_content_restore cloud_content_transfer cloud_scan cloud_folder_validate cloud_device_id cloud_log_scrub cloud-signin-window backuptool; do git grep -l -w "$n" $R -- projects packages | sed "s/^$R://"; done | sort -u | grep -v -x -F -f .qa-scratch/t17/paths.txt > "$TMPDIR/callers.txt"; wc -l < "$TMPDIR/callers.txt"; cat "$TMPDIR/callers.txt"; }
r33_install_lines() { git grep -n -E 'cp cloud_|cloud-signin-window' $R -- projects/ROCKNIX/packages/network/rclone/package.mk | sed "s/^$R://"; }
r34_tools() { for t in cloud-connections-test cloud-input-test pixelelated-cloud-validator-test pixelelated-content-scope-test pixelelated-save-layout-test signin-memory cloud-round-trip cloud-census vm-qa pixelelated-vm-cloud-boundaries last-good-scripts-test; do printf '%s %s\n' "$t" "$(git show "$R:tools/$t" | grep -c -w -E 'cloud_oauth|cloud_setup|cloud_remote|cloud_connections|cloud_content_backup|cloud_content_restore|cloud_content_transfer|cloud_scan|cloud_folder_validate|cloud_device_id|cloud_log_scrub|cloud-signin-window|backuptool')"; done; }
r35_t13_rows() { git show feature/m6-cloud-harness-660:docs/audits/2026_10_25-epic-m6-cloud-harness/02-forward-audit.md | awk '/^## Assertion shapes/{p=1;next} /^## /{p=0} p' | grep -c -w -E 'cloud_oauth|cloud_setup|cloud_remote|cloud_connections|cloud_content_backup|cloud_content_restore|cloud_content_transfer|cloud_scan|cloud_folder_validate|cloud_device_id|cloud_log_scrub|backuptool'; }
r36_back_up_words() { tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git grep -o -h -w -E 'BACK UP|BACKUP' $R -- | sort | uniq -c; }
r37_vocabulary_check() { grep -n -E 'cloud_|backuptool|--es|ES_SRC' tools/vocabulary-check | head -n 12; if [ -n "${ES_SRC:-}" ]; then tools/vocabulary-check --es "$ES_SRC" 2>&1 | tail -n 3; else echo "CANNOT: no EmulationStation checkout named (ES_SRC); the four scripts it reads are read by hand against es-player-text.md"; fi; }
r38_sourced() { for f in cloud_content_backup cloud_content_restore cloud_content_transfer cloud_device_id cloud_log_scrub cloud_scan cloud_setup; do printf '%s: ' "$f"; git show "$R:$P/$f" | grep -n -E '^\s*(\.|source) ' | tr '\n' ' '; echo; done; printf 'backuptool: '; git show "$R:$BT" | grep -n -E '^\s*(\.|source) ' | tr '\n' ' '; echo; }
r39_removal_rule() { echo "[$(git diff --stat $DISPATCH HEAD -- packages projects tools | tail -1)]"; }
r40_branch_vs_read() { echo "[$(tr '\n' '\0' < .qa-scratch/t17/paths.txt | xargs -0 git diff --stat $R HEAD -- | tail -1)]"; }
for f in $(declare -F | awk '{print $3}' | grep -E '^r[0-9]{2}_' | sort); do run "$f" "$f"; done
