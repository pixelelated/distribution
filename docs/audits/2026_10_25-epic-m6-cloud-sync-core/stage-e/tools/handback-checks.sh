#!/bin/bash
# T16's hand-back checks, each with its command, output and rc. Run from the lane worktree.
W=$(pwd); A=docs/audits/2026_10_25-epic-m6-cloud-sync-core; E=$A/stage-e; P=projects/ROCKNIX/packages/network/rclone
run() { echo "\$ $1"; bash -c "$1" 2>&1 | sed 's/\x1b\[K//g; s/\r/\n/g' | grep -v '^$' | tail -n "${2:-6}"; echo "rc=${PIPESTATUS[0]}"; echo; }
echo "# T16 hand-back checks ($(date -u +%FT%TZ)), the branch at $(git rev-parse --short HEAD); <W> is the lane worktree"
echo
run "git status --short | grep -v '^??' | wc -l"
run "git merge-base --is-ancestor 8476d6e889 HEAD && echo '8476d6e889 (the coordinator tip) is an ancestor of HEAD'"
run "git grep -n -I -E '^(<<<<<<<|>>>>>>>)( |\$)' | wc -l"
run "echo reviewed-at aeebe31248: \$(git diff --stat 8ebaf8daad aeebe31248 -- \$(cat .qa-scratch/t16/paths.txt) | wc -l) diff lines on the 14 against 8ebaf8daad"
run "echo fixed-at 23dfd53c0e: \$(git diff --shortstat 8ebaf8daad 23dfd53c0e -- $P)"
run "echo stage E commits on the first-parent line touching tools/: \$(git log --first-parent --no-merges --format=%h f05f5727e0^..HEAD -- tools | wc -l)"
run "echo paths the first-parent commits of the lane changed since stage E began outside the rclone package, the audit folder, its retro and the work logs: \$(git log --first-parent --no-merges --name-only --format= f05f5727e0^..HEAD | sort -u | grep -v '^\$' | grep -v -e '^$P/' -e '^$A/' -e '^docs/retros/2026-10-31-m6-cloud-sync-core.md\$' -e '^docs/work-logs/' | wc -l)"
run "for f in cloud_backup cloud_restore cloud_sync_helper cloud_saves_root cloud_capture cloud_sync_cleanup_duplicates.sh cloud_net_ready; do bash -n $P/sources/\$f && echo \"bash -n \$f: ok\"; done; bash -n $P/autostart/102-cloud-saves && echo 'bash -n 102-cloud-saves: ok'; /workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/busybox sh -n $P/sources/cloud_net_ready && echo 'busybox sh -n cloud_net_ready: ok'" 12
run "tools/pkgcheck rclone"
run "python3 tools/vocabulary-check | tail -1"
run "tools/register-check"
run "tools/work-log-index --check"
run "tools/rules-check --quiet; echo rules-check done"
run "python3 tools/lint-audit-artifacts $A | tail -1"
run "python3 tools/lint-audit-artifacts $A --phase resolution --issue 1295 | tail -1"
run "for n in 1295 1298 1299 1300 1301 1302 1303 1304; do echo \"#\$n \$(tools/box-check --issue \$n 2>&1 | tail -1)\"; done" 10
run "TMPDIR=/workspace/tmp/m6-t16/tmp tools/cloud-capture-stamp-test $P/sources/cloud_capture | tail -1"
run "tools/forbidden-terms-check | tail -2"
run ".githooks/hooks-test 2>&1 | tail -3" 4
run "grep -h -E '^(PASSED|[0-9]+ CHECK)' $E/suite-before.out $E/suite-after.out; for f in $E/suite-before.out $E/suite-after.out; do echo \"\$f: \$(head -1 \$f | cut -c1-70) ... PASS \$(grep -c '^    PASS  ' \$f) FAIL \$(grep -c '^    FAIL  ' \$f) SKIP \$(grep -c '^    SKIP  ' \$f); \$(tail -1 \$f)\"; done" 6
run "tools/ceremony-check | tail -3" 4
