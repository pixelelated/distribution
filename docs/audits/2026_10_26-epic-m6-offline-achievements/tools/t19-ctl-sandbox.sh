# T19 stage E (#666): the sandbox every ctl stream's fixture runs the real
# raofflineproxy-ctl in. Sourced, not run. The shape is
# tools/last-good-scripts-test's sections p and t: bubblewrap started with
# --clearenv over a tmpfs root; the host's /usr read-only; a stub
# /etc/profile carrying get_setting and set_setting lifted whole from the
# tree's 001-functions, with J_CONF at the fake /storage's system.cfg; the
# image's busybox (a copy of QA_SYSTEM_ROOT's, the retained donor) for every
# applet the image takes from it; shims on PATH for systemctl and logger; a
# fake /storage, /run and /var/run. bash is the host's (the image's bash is a
# package, not busybox).
#
#   t19_setup <ctl-file> <workdir>   build the sandbox around a copy of <ctl-file>
#   t19_ctl <verb> [args...]         run it: stdout $OUT, stderr $ERR, rc $RC
#   T19_BINDS=(...)                  extra bwrap arguments for the next t19_ctl
#   T19_ENV=(...)                    extra --setenv pairs for the next t19_ctl
#
# The workdir must be fresh and under /workspace/tmp/m6-t19/; nothing is
# written outside it. Under the sandbox, /storage is <workdir>/storage, /run is
# <workdir>/run, /var/run is <workdir>/varrun and /shim is <workdir>/shim.

T19_QA_SYSTEM_ROOT="${QA_SYSTEM_ROOT:-/workspace/artifacts/m6-donor/1a0266484423/image/system}"
T19_APPLETS="find chmod stat flock sed awk mv cp head tail tr wc cut cat readlink mktemp touch ls rm mkdir sort grep date ln"

t19_setup() {
    local ctl="$1" w="$2" real tree fns
    real="$(realpath -m "${w}")"
    case "${real}" in
        /workspace/tmp/m6-t19/*) ;;
        *) echo "CANNOT: workdir ${real} is not under /workspace/tmp/m6-t19/" >&2; return 2 ;;
    esac
    case "${real}" in /storage*|/etc*|/usr*|/var*|/run*|/root*|/home*) echo "CANNOT: ${real} is a real prefix" >&2; return 2 ;; esac
    if [ -e "${real}" ] && [ -n "$(ls -A "${real}" 2>/dev/null)" ]; then
        echo "CANNOT: workdir ${real} is not empty" >&2; return 2
    fi
    [ -f "${ctl}" ] || { echo "CANNOT: no ctl at ${ctl}" >&2; return 2; }
    [ -x "${T19_QA_SYSTEM_ROOT}/usr/bin/busybox" ] || { echo "CANNOT: no busybox under ${T19_QA_SYSTEM_ROOT}" >&2; return 2; }
    T19_W="${real}"
    tree="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)" || return 2
    fns="${tree}/projects/ROCKNIX/packages/rocknix/profile.d/001-functions"
    mkdir -p "${T19_W}/storage/.config/system/configs" "${T19_W}/storage/.cache" \
             "${T19_W}/storage/.config/raofflineproxy" "${T19_W}/repo" "${T19_W}/shim" \
             "${T19_W}/run" "${T19_W}/varrun" "${T19_W}/bb" "${T19_W}/bbin" || return 2
    cp "${ctl}" "${T19_W}/repo/raofflineproxy-ctl" || return 2
    sed -n '/^function get_setting() {/,/^}/p; /^function wait_lock_say() {/,/^}/p; /^function wait_lock() {/,/^}/p; /^function settings_base() {/,/^}/p; /^function prepare_settings_temp() {/,/^}/p; /^function write_setting_line() {/,/^}/p; /^function del_setting() {/,/^}/p; /^function set_setting() {/,/^}/p' \
        "${fns}" > "${T19_W}/repo/fns.sh"
    grep -q '^function set_setting() {' "${T19_W}/repo/fns.sh" || { echo "CANNOT: set_setting not lifted from ${fns}" >&2; return 2; }
    cp "${T19_QA_SYSTEM_ROOT}/usr/bin/busybox" "${T19_W}/bb/busybox" || return 2
    local a
    for a in ${T19_APPLETS}; do
        # Only what the image's busybox provides; the rest (grep, a package
        # of its own on the image) is the host's.
        "${T19_W}/bb/busybox" --list | grep -qx "${a}" || continue
        printf '#!/bin/sh\nexec /t19bb/busybox %s "$@"\n' "${a}" > "${T19_W}/bbin/${a}"
        chmod +x "${T19_W}/bbin/${a}"
    done
    printf 'export PATH=/shim:/bbin:/usr/bin:/bin\nexport OS_NAME=ROCKNIX\nJ_CONF=/storage/.config/system/configs/system.cfg\nJ_CONF_LOCK=/tmp/.system.cfg.lock\n. /repo/fns.sh\n' > "${T19_W}/profile"
    cat >> "${T19_W}/profile" <<'EOS'
# A write can be made to fail: /run/fail-set.d/<key> holds how many writes
# of that key still succeed before every later one writes nothing and
# returns 1 (0: the first fails).
if [ -d /run/fail-set.d ]; then
    eval "$(declare -f set_setting | sed '1s/^set_setting/real_set_setting/')"
    set_setting() {
        local f="/run/fail-set.d/${1}" n
        if [ -e "${f}" ]; then
            n="$(cat "${f}")"
            if [ "${n:-0}" -gt 0 ]; then echo "$((n - 1))" > "${f}"; else return 1; fi
        fi
        real_set_setting "$@"
    }
fi
EOS
    cat > "${T19_W}/shim/systemctl" <<'EOS'
#!/bin/sh
echo "systemctl $*" >> /run/systemctl.log
case "$1" in
    start) [ -e /run/fail-start ] && exit 1
           # the unit's ExecStartPost, when a fixture asks for it
           if [ -e /run/start-runs-listening ]; then /usr/bin/bash /repo/raofflineproxy-ctl listening --wait 2 || exit 1; fi
           touch /run/active; exit 0 ;;
    stop) [ -e /run/fail-stop ] && exit 1; rm -f /run/active; exit 0 ;;
    is-active) if [ -e /run/active ]; then echo active; exit 0; else echo inactive; exit 3; fi ;;
    show) if [ -e /run/mainpid ]; then cat /run/mainpid; else echo 0; fi; exit 0 ;;
esac
exit 0
EOS
    # say() is logger: on the device its lines go to the journal, whatever the
    # script's stderr has become, so they are kept in /run/say.log too.
    printf '#!/bin/sh\necho "logger $*" >&2\necho "logger $*" >> /run/say.log\n' > "${T19_W}/shim/logger"
    chmod +x "${T19_W}/shim/systemctl" "${T19_W}/shim/logger"
    : > "${T19_W}/storage/.config/system/configs/system.cfg"
    OUT="${T19_W}/out"; ERR="${T19_W}/err"
    T19_BINDS=(); T19_ENV=()
    T19_USR=(); local u
    for u in bin sbin lib lib64 libexec share; do [ -e "/usr/${u}" ] && T19_USR+=(--ro-bind "/usr/${u}" "/usr/${u}"); done
    return 0
}

t19_ctl() {
    RC=$( ( bwrap --die-with-parent --clearenv --tmpfs / --tmpfs /usr "${T19_USR[@]}" \
        --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
        --ro-bind /etc /etc --ro-bind "${T19_W}/profile" /etc/profile \
        --ro-bind "${T19_W}/bb" /t19bb --ro-bind "${T19_W}/bbin" /bbin \
        --bind "${T19_W}/storage" /storage --ro-bind "${T19_W}/repo" /repo --bind "${T19_W}/shim" /shim \
        --bind "${T19_W}/run" /run --tmpfs /var --bind "${T19_W}/varrun" /var/run \
        --dev /dev --proc /proc --tmpfs /tmp \
        --setenv PATH /shim:/bbin:/usr/bin:/bin "${T19_ENV[@]}" "${T19_BINDS[@]}" \
        /usr/bin/bash /repo/raofflineproxy-ctl "$@" > "${OUT}" 2> "${ERR}"; echo $? ) 2>/dev/null )
    T19_BINDS=(); T19_ENV=()
}

# One verdict line; FAILS counts the ones that did not hold.
FAILS=0
t19_check() { # <0|nonzero> <what held> <what was seen>
    if [ "$1" -eq 0 ]; then echo "    PASS  $2"; else echo "    FAIL  $2 -- $3"; FAILS=$((FAILS + 1)); fi
}

t19_versions() {
    echo "host bash ${BASH_VERSION} (the tree pins bash 5.3); applets from $("${T19_W}/bb/busybox" 2>&1 | head -1 | cut -d' ' -f1-2) (a copy of ${T19_QA_SYSTEM_ROOT}/usr/bin/busybox, the image's); host python $(python3 -c 'import sys;print(sys.version.split()[0])') (image recipe 3.14.7)"
}

# t19_run <command> [args...]: the same sandbox, any command (the ctl is at
# /repo/raofflineproxy-ctl), so a fixture can start a process beside the ctl
# in one namespace -- with T19_BINDS=(--unshare-net) a listener the host
# never sees. stdout $OUT, stderr $ERR, rc $RC.
t19_run() {
    RC=$( ( bwrap --die-with-parent --clearenv --tmpfs / --tmpfs /usr "${T19_USR[@]}" \
        --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
        --ro-bind /etc /etc --ro-bind "${T19_W}/profile" /etc/profile \
        --ro-bind "${T19_W}/bb" /t19bb --ro-bind "${T19_W}/bbin" /bbin \
        --bind "${T19_W}/storage" /storage --ro-bind "${T19_W}/repo" /repo --bind "${T19_W}/shim" /shim \
        --bind "${T19_W}/run" /run --tmpfs /var --bind "${T19_W}/varrun" /var/run \
        --dev /dev --proc /proc --tmpfs /tmp \
        --setenv PATH /shim:/bbin:/usr/bin:/bin "${T19_ENV[@]}" "${T19_BINDS[@]}" \
        "$@" > "${OUT}" 2> "${ERR}"; echo $? ) 2>/dev/null )
    T19_BINDS=(); T19_ENV=()
}
