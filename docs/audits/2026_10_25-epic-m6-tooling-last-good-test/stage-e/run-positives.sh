#!/bin/bash
# run-positives.sh -- T15 stage E (#662): S3's constructed positives, the
# coordinator's 06:05 ruling. For each bug: a throwaway `git clone --shared` of
# the tree at TIP under ${S}/<bug>/src, altered by alter-<bug>.sh (never
# committed); the suite run against it (LAST_GOOD_SOURCE_ROOT) twice, by the
# harness from the commit before the fix and by the fixed one; the lines of the
# checks the alteration targets extracted; the clones removed. One run at a
# time, on M6's donor root, a PAUSE T15 directive in the host file honoured at
# each boundary, the census beside each wall time.
#   run-positives.sh <worktree> <tip> [bug...]
set -u
W="$(cd "$1" && pwd)"; TIP="$2"; shift 2
E="$(cd "$(dirname "$0")" && pwd)"
S=/workspace/tmp/m6-t15/s3
H=/workspace/tmp/m7-m6-host-coordination.txt   # the durable host file since 2026-10-29 (/tmp's went with the reboot)
LOG=/workspace/tmp/m6-t15/s2/queue.log
export TMPDIR=/workspace/tmp/m6-t15/tmp PYTHONDONTWRITEBYTECODE=1
export QA_SYSTEM_ROOT=/workspace/artifacts/m6-donor/1a0266484423/image/system
SIGDFL='import os, signal, sys; signal.signal(signal.SIGINT, signal.SIG_DFL); signal.signal(signal.SIGPIPE, signal.SIG_DFL); os.execv(sys.argv[1], sys.argv[1:])'
census() { echo "cc1plus=$(pgrep -c -x cc1plus) qemu=$(pgrep -c -x qemu-system-x86) load=$(cut -d' ' -f1-3 /proc/loadavg)"; }
paused() { command grep -E '(^|: )(PAUSE|RESUME) T15\b' "${H}" 2>/dev/null | tail -1 | command grep -q -E '(^|: )PAUSE T15\b'; }
boundary() { while paused; do echo "$(date -u +%H:%M:%S) PAUSED by the host file before: $1" >> "${LOG}"; sleep 60; done; }
counts() { printf 'PASS=%s FAIL=%s SKIP=%s CANNOT=%s' "$(command grep -c '^    PASS  ' "$1")" "$(command grep -c '^    FAIL  ' "$1")" "$(command grep -c '^    SKIP  ' "$1")" "$(command grep -c '^    CANNOT  ' "$1")"; }
# section <out> <from banner> <to banner>: the result lines between two banners
section() { awk -v a="$2" -v b="$3" 'index($0, a) == 1 {f = 1; next} index($0, b) == 1 {f = 0} f && /^    (PASS|FAIL|SKIP|N\/A|CANNOT)/' "$1"; }
extract() { # <bug> <out>
    case "$1" in
        1037) section "$2" "  S3F. " "  aa. " ;;
        1037-ack) section "$2" "  S3F. " "  aa. " | command grep -E 'ack for token|rc=|marker' ;;
        1027) section "$2" "  v. " "  w. " ;;
        1034) section "$2" "  b. " "  c. " | command grep -i 'wifi key' ;;
        1036) { section "$2" "  q. " "  r. "; command grep -E '^    (PASS|FAIL)  .*(each compiled|does not compile|mode 100755|modes:)' "$2"; } ;;
        1036-gate) command grep -E 'cannot test selected source|historical migration cases|NOT APPLICABLE' "$2"; tail -1 "$2" ;;
        1036-frag) section "$2" "  q. " "  r. "; command grep -E '^--old ' "$2" ;;
        1031) command grep -E '^    (PASS|FAIL)  .*(F-PB-21|gpt G-D-03: )' "$2" ;;
    esac
}
unfixed_of() { case "$1" in 1037|1037-ack) echo 5429e27e72 ;; 1027) echo 60066e21f8 ;; 1034) echo 32ba775765 ;; 1036|1036-gate|1036-frag) echo 65bdd1a717 ;; 1031) echo 812d09e3af ;; esac; }
# qcut <harness file> <out file>: the harness, section q and the verdict (1036-frag)
qcut() {
    local f="$1" a q r v
    a=$(command grep -n '^# ---------------------------------------------------------------- a\.' "$f" | cut -d: -f1)
    q=$(command grep -n '^section q ' "$f" | cut -d: -f1); r=$(command grep -n '^section r ' "$f" | cut -d: -f1)
    # The verdict from the trap's disarm where the harness has one (#1023,
    # e430d61cfa): a cut that starts below VERDICT_REACHED=1 prints its verdict
    # and is then reported ABORTED, rc 2 (the coordinator's acceptance read,
    # 2026-10-30). An older harness has no trap, and starts where it always did.
    v=$(command grep -n '^VERDICT_REACHED=1' "$f" | cut -d: -f1)
    [ -n "$v" ] || v=$(command grep -n '^if \[ "${NOT_APPLICABLE}" -ne 0 \]' "$f" | cut -d: -f1)
    { sed -n "1,$((a - 1))p" "$f"; sed -n "${q},$((r - 1))p" "$f"; sed -n "${v},\$p" "$f"; } > "$2"; chmod +x "$2"
}
run() { # <bug> <side> <harness dir> <script> [args...]
    local bug="$1" side="$2" hd="$3" sc="$4" out s rc; shift 4
    out="${S}/${bug}/${side}.out"
    boundary "${bug}-${side}"
    echo "$(date -u +%H:%M:%S) START pos-${bug}-${side} harness $(git -C "${hd}" log --oneline -1 | cut -c1-10) source ${S}/${bug}/src census: $(census)" >> "${LOG}"
    s=$(date +%s)
    ( cd "${hd}" && env LAST_GOOD_SOURCE_ROOT="${S}/${bug}/src" ${BASE_REF:+BASE_REF="${BASE_REF}"} python3 -c "${SIGDFL}" "${sc}" "$@" ) > "${out}" 2>&1 &
    echo "$(date -u +%H:%M:%S) PID pos-${bug}-${side} $! (runner $$)" >> "${LOG}"
    wait $!; rc=$?
    { echo "$(date -u +%H:%M:%S) END pos-${bug}-${side} rc=${rc} $(( $(date +%s) - s ))s $(counts "${out}") census: $(census)"
      extract "${bug}" "${out}" | cut -c1-260 | sed 's/^/    /'
      echo "    verdict: $(tail -1 "${out}" | cut -c1-200)"; } >> "${LOG}"
}
echo "$(date -u +%H:%M:%S) POSITIVES START pid $$ tip ${TIP} root ${QA_SYSTEM_ROOT}" >> "${LOG}"
for bug in "${@:-1037 1027 1034 1036 1036-gate 1036-frag 1031}"; do
  for b in ${bug}; do
    mkdir -p "${S}/${b}"
    git clone -q --shared --no-checkout "${W}" "${S}/${b}/src" && git -C "${S}/${b}/src" checkout -q --detach "${TIP}" || { echo "$(date -u +%H:%M:%S) CANNOT pos-${b}: no clone" >> "${LOG}"; continue; }
    git clone -q --shared --no-checkout "${W}" "${S}/${b}/h-unfixed" && git -C "${S}/${b}/h-unfixed" checkout -q --detach "$(unfixed_of "${b}")"
    git clone -q --shared --no-checkout "${W}" "${S}/${b}/h-fixed" && git -C "${S}/${b}/h-fixed" checkout -q --detach "${TIP}"
    bash "${E}/alter-${b}.sh" "${S}/${b}/src" > "${S}/${b}/alter.log" 2>&1; arc=$?
    { echo "$(date -u +%H:%M:%S) ALTER ${b} rc=${arc}:"; sed 's/^/    /' "${S}/${b}/alter.log"; } >> "${LOG}"
    if [ "${arc}" -ne 0 ] || ! git -C "${S}/${b}/src" status --short | command grep -q .; then
        echo "$(date -u +%H:%M:%S) CANNOT pos-${b}: the alteration did not apply" >> "${LOG}"; continue
    fi
    if [ "${b}" = 1036-frag ]; then
        qcut "${S}/${b}/h-unfixed/tools/last-good-scripts-test" "${S}/${b}/h-unfixed/tools/lgst-q"
        qcut "${S}/${b}/h-fixed/tools/last-good-scripts-test" "${S}/${b}/h-fixed/tools/lgst-q"
        BASE_REF=717bc04449 run "${b}" unfixed "${S}/${b}/h-unfixed" tools/lgst-q --old
        BASE_REF=717bc04449 run "${b}" fixed "${S}/${b}/h-fixed" tools/lgst-q --old
    else
        run "${b}" unfixed "${S}/${b}/h-unfixed" tools/last-good-scripts-test
        run "${b}" fixed "${S}/${b}/h-fixed" tools/last-good-scripts-test
    fi
    rm -rf -- "${S:?}/${b:?}/src"
    rm -rf -- "${S:?}/${b:?}/h-unfixed"
    rm -rf -- "${S:?}/${b:?}/h-fixed"
    echo "$(date -u +%H:%M:%S) REMOVED pos-${b}'s three clones (outputs kept in ${S}/${b}/)" >> "${LOG}"
  done
done
echo "$(date -u +%H:%M:%S) POSITIVES END" >> "${LOG}"
