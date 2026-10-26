#!/bin/bash
# T19 (#666): the brief's § 5 runs, each recorded with its exit and wall time.
#   bash docs/audits/2026_10_26-epic-m6-offline-achievements/tools/t19-runs.sh <dispatch tip> > <out>
# Run from the lane's worktree after the membership block (.qa-scratch/t19/paths.txt).
# Reads only: git objects at 8ebaf8daad, the ES checkout by `git -C ... show`/`grep <rev>`,
# the cache's tarball by name; writes only under $TMPDIR (/workspace/tmp/m6-t19/tmp).
# The ctl is never executed: it is written to $TMPDIR and given to `bash -n` only.
DTIP=${1:?the dispatch tip}
export LC_ALL=C; C=8ebaf8daad; P=projects/ROCKNIX/packages/network/raofflineproxy; G=/usr/bin/grep
D=$(pwd); export TMPDIR=/workspace/tmp/m6-t19/tmp; mkdir -p "$TMPDIR"
ES=/home/max/Development/emulationstation-next.worktrees/qa-integration
run() { local id=$1; shift; local t0 t1; t0=$(date +%s.%N); echo "=== $id ($(date -u +%H:%M:%SZ))"; ( eval "$*" ); local rc=$?; t1=$(date +%s.%N); printf -- '--- %s rc=%d wall=%.2fs\n' "$id" "$rc" "$(echo "$t1 - $t0" | bc)"; }
run R0-df 'df -i /workspace | tail -n 1'
run R1-membership-bytes 'tr "\n" "\0" < .qa-scratch/t19/paths.txt | xargs -0 -I{} sh -c '"'"'printf "%6d %s\n" "$(git show '"$C"':{} | wc -l)" "{}"'"'"' | tee "$TMPDIR/perfile.txt" | awk "{s+=\$1} END{print NR\" paths \"s\" lines\"}"'
run R2-ctl-shape 'git show $C:$P/sources/raofflineproxy-ctl | $G -n -E "^\s*set -" | wc -l; git show $C:$P/sources/raofflineproxy-ctl | $G -c pipefail; git show $C:$P/sources/raofflineproxy-ctl | $G -c -E "^[a-z_]+\(\)"; git show $C:$P/sources/raofflineproxy-ctl | $G -n -E "^EX_[A-Z]+=" ; git show $C:$P/sources/raofflineproxy-ctl | $G -n -o -E "\bexit [0-9]+"'
run R3-unit 'git show $C:$P/system.d/raofflineproxy.service | $G -n -E "^(ExecStart|ExecStartPost|ConditionPathExists|Restart|RestartSec|TimeoutStopSec|User|Group)="; git show $C:$P/system.d/raofflineproxy.service | $G -c -E "^(Protect|Private|NoNewPrivileges|CapabilityBoundingSet|Memory|CPU|Tasks|DynamicUser|IPAddress|RestrictAddressFamilies|SystemCallFilter|ReadWritePaths|ReadOnlyPaths|UMask)"'
run R4-port 'git grep -n -E "127\.0\.0\.1:8080" $C -- packages projects ":!$P" | sed "s/^$C://" | cut -c1-120; git grep -n -E "\b8080\b" $C -- projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth | sed "s/^$C://" | cut -c1-100'
run R5-credential 'git show $C:$P/sources/raofflineproxy-ctl | $G -n -E "USER_KEY|TOKEN_KEY|PASSWORD_KEY|RA_SCAN_USER" | $G -v -E "^[0-9]+:\s*#" | cut -c1-110; git show $C:$P/sources/raofflineproxy-ctl | $G -c -E "umask|chmod|chown"'
run R6-stamps 'git show $C:$P/sources/raofflineproxy-ctl | $G -n -E "mv -f|touch |> *\"\\\$\{?(SCAN_STAMP|RUNNING|INDEX_PENDING|TOPUP_MARK|FLUSH_STAMP)" | cut -c1-120'
run R7-helpers-writes 'for f in raofflineproxy-cache-images raofflineproxy-refresh raofflineproxy-cache-indexed; do echo "== $f"; git show $C:$P/sources/$f | $G -n -E "write_text|os\.replace|rename\(|sys\.stdout|print\(" | cut -c1-110 | head -n 12; done'
run R8-tokens 'for f in raofflineproxy-ctl raofflineproxy-refresh raofflineproxy-cache-images raofflineproxy-cache-indexed; do printf "%s: " "$f"; git show $C:$P/sources/$f | $G -o -E "\"(why|note|doing|done|total|game|cached|refresh|verified|errors) [A-Z_]{2,}" | sort -u | wc -l; done'
run R9-deletions 'git show $C:$P/sources/raofflineproxy-ctl | $G -n -E "rm -rf|find .*-delete|(^|[^a-z])(: *>)" | cut -c1-100; git show $C:$P/package.mk | $G -n -E "rm -rf|rm -f" | cut -c1-100'
run R10-patches 'git ls-tree -r --name-only $C -- $P/patches | wc -l; git show $C:$P/package.mk | $G -n -i "patches" | head -n 3 | cut -c1-120; git show $C:$P/package.mk | $G -n -E "^PKG_(VERSION|SHA256)="; for s in rcheevos libchdr; do git show $C:projects/ROCKNIX/packages/network/raofflineproxy-$s/package.mk | $G -n -E "^PKG_VERSION="; done; git show $C:$P/sources/raofflineproxy-ctl | $G -n -E "^# package\.mk pins" | cut -c1-100'
run R11-proxy-schema 'tools/rc-preflight --only proxy-schema --tree "$D" 2>&1 | tail -n 2'
run R12-tarball 'PIN=$(git show $C:$P/package.mk | sed -n -E "s/^PKG_VERSION=\"([0-9a-f]{40})\".*/\1/p"); T=/workspace/cache/rocknix-sources/raofflineproxy/raofflineproxy-$PIN.tar.gz; ls /workspace/cache/rocknix-sources/raofflineproxy/ | wc -l; [ -f "$T" ] && sha256sum "$T" | cut -c1-16 || echo "CANNOT: $T absent"; git show $C:$P/package.mk | sed -n -E "s/^PKG_SHA256=\"([0-9a-f]{16}).*/\1/p"'
run R13-neighbours 'git grep -c -w raofflineproxy $C -- packages projects ":!$P" ":!projects/ROCKNIX/packages/network/raofflineproxy-rcheevos" ":!projects/ROCKNIX/packages/network/raofflineproxy-libchdr" | sed "s/^$C://"; git -C $ES grep -c -w raofflineproxy 16dbac5211 -- es-app/src es-core/src | sed "s/^16dbac5211://" | sort -t: -k2 -n -r | head -n 11'
run R14-have-account 'git -C $ES grep -n have_account 16dbac5211 -- es-app/src | sed "s/^16dbac5211://" | cut -c1-100; git show $C:$P/sources/raofflineproxy-ctl | $G -n have_account | cut -c1-80; git show $C:$P/sources/raofflineproxy-ctl | sed -n "2434,2450p" | $G -c have_account'
run R15-tools 'for t in raofflineproxy-integration-test raofflineproxy-installed-native-test raofflineproxy-consent-test; do printf "%s: " "$t"; tools/$t --help >/dev/null 2>&1; echo "rc=$?"; done; $G -c -w raofflineproxy tools/last-good-scripts-test; tools/qa-accounts 2>&1 | head -n 2 | cut -c1-100'
run R16-syntax 'bash --version | head -n 1; git show $C:$P/sources/raofflineproxy-ctl > "$TMPDIR/ctl"; bash -n "$TMPDIR/ctl"; echo "bash -n rc=$?"; python3 --version; for f in raofflineproxy-refresh raofflineproxy-cache-images raofflineproxy-cache-indexed; do git show $C:$P/sources/$f > "$TMPDIR/$f"; python3 -I -m py_compile "$TMPDIR/$f"; echo "$f py_compile rc=$?"; done'
run R17-removal-check 'git diff --stat $DTIP HEAD -- packages projects tools | tail -n 1; echo "(empty above = nothing changed since the dispatch tip $DTIP)"'
