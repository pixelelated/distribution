#!/bin/bash
# #1111/#1115 phase B, the host half: guest-b.py on a fresh vm-pair guest from
# build 12, a clean phase, a reboot, a retained phase.
#
#   phase-b.sh --round <round worktree> --image <build 12 img.gz> --outdir DIR
#
# The WebDAV account is the host's QA backend (tools/cloud-test-backend): its
# stanza is generated at run time into a 0600 temp file, copied to the guest's
# /storage/m7-qa/qa-webdav.conf, deleted on the host at once and on the guest
# at the end; the tree never holds it. QA guest only.
# Exit 0 both phases PASS, 1 a check failed, 2 cannot run.
set -uo pipefail
round= image= out=
while [ "$#" -ge 2 ]; do
    case "$1" in --round) round=$2 ;; --image) image=$2 ;; --outdir) out=$2 ;; *) exit 2 ;; esac; shift 2
done
[ -x "$round/tools/vm-pair" ] && [ -r "$image" ] && [ -n "$out" ] || { echo "usage: $0 --round TREE --image IMG --outdir DIR" >&2; exit 2; }
! [ -e "$out" ] || { echo "cannot run: $out exists" >&2; exit 2; }
mkdir -p "$out" && out=$(cd "$out" && pwd) || exit 2
here=$(cd "$(dirname "$0")" && pwd)
KEY=/tmp/rocknix-vm-pair/qa-key
SSHO=(-F /dev/null -p 10022 -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no
      -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
SCPO=(-F /dev/null -P 10022 -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no
      -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
S() { timeout 300 ssh -n "${SSHO[@]}" root@127.0.0.1 ". /etc/profile >/dev/null 2>&1; $*"; }
log() { echo "$*" | tee -a "$out/RESULT.txt"; }
die() { log "CANNOT RUN: $*"; S 'rm -f /storage/m7-qa/qa-webdav.conf' >/dev/null 2>&1; exit 2; }

log "== #1111/#1115 phase B, $(date -u +%FT%TZ)"
pgrep -f 'qemu-system-x86_6[4]' >/dev/null && die "a QEMU guest is already up; bring the pair down first"
( cd "$round" && VM_RES=640x480 timeout 900 tools/vm-pair up "$image" ) > "$out/vm-pair-up.log" 2>&1 || die "vm-pair up failed (vm-pair-up.log)"
S 'grep -E "^(BUILD_ID|VERSION)=" /etc/os-release' > "$out/os-release.txt" || die "the guest does not answer"
cat "$out/os-release.txt" >> "$out/RESULT.txt"
S 'command -v python3 && test ! -e /storage/m7-qa && mkdir -m 700 /storage/m7-qa' > /dev/null || die "no python3 on the guest, or /storage/m7-qa exists"
scp -q "${SCPO[@]}" "$here/guest-b.py" root@127.0.0.1:/storage/m7-qa/guest-b.py || die "copy of guest-b.py failed"
conf=$(mktemp); chmod 600 "$conf"
"$round/tools/cloud-test-backend" rclone-conf > "$conf" 2>/dev/null && grep -q '^type = webdav' "$conf" ||
    { rm -f "$conf"; die "the QA backend gave no WebDAV stanza (is it running?)"; }
scp -q "${SCPO[@]}" "$conf" root@127.0.0.1:/storage/m7-qa/qa-webdav.conf; rc=$?; rm -f "$conf"
[ "$rc" = 0 ] && S 'chmod 600 /storage/m7-qa/qa-webdav.conf' || die "copy of the WebDAV stanza failed"

fetch() {  # the guest's results and witnesses, never the stanza
    S 'cd /storage/m7-qa && ls result-*.json witness-*.json validator-*.json expected-retained.json 2>/dev/null' |
        while read -r f; do scp -q "${SCPO[@]}" "root@127.0.0.1:/storage/m7-qa/$f" "$out/$f" < /dev/null; done
}
failed=0
log "-- clean"
S 'python3 /storage/m7-qa/guest-b.py clean' > "$out/clean.console" 2>&1 || failed=1
tail -1 "$out/clean.console" | tee -a "$out/RESULT.txt"
fetch
log "-- reboot"
b0=$(S 'cat /proc/sys/kernel/random/boot_id')
S 'sync; systemctl reboot' >/dev/null 2>&1
for i in $(seq 1 60); do sleep 5; b=$(S 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null); [ -n "$b" ] && [ "$b" != "$b0" ] && break; done
[ -n "${b:-}" ] && [ "$b" != "$b0" ] || die "the guest did not come back from the reboot"
log "   boot id changed"
sleep 20
log "-- retained"
S 'python3 /storage/m7-qa/guest-b.py retained' > "$out/retained.console" 2>&1 || failed=1
tail -1 "$out/retained.console" | tee -a "$out/RESULT.txt"
fetch
S 'rm -f /storage/m7-qa/qa-webdav.conf; test ! -e /storage/m7-qa/qa-webdav.conf' && log "   the WebDAV stanza is removed from the guest" || { log "   FAILED to remove the WebDAV stanza"; failed=1; }
python3 -I - "$out" <<'PY' | tee -a "$out/RESULT.txt"
import json, sys, pathlib
d = pathlib.Path(sys.argv[1])
for ph in ('clean', 'retained'):
    f = d / f'result-{ph}.json'
    if not f.exists():
        print(f'{ph}: no result'); continue
    r = json.loads(f.read_text())
    print(f"{ph}: {r['status']}, {sum(x['pass'] for x in r['checks'])} of {len(r['checks'])} checks" + (f"; error {r.get('error')}" if r.get('error') else ''))
    for x in r['checks']:
        print(f"  {'PASS' if x['pass'] else 'FAIL'}  {x['name']} [{x['criteria']}]" + ('' if x['pass'] else f"  {x['detail']}"))
PY
[ "$failed" = 0 ] && { log PASSED; exit 0; }
log FAILED; exit 1
