#!/bin/bash
# T17 (#664): the second guest window (granted 08:2x UTC on #664, 15 minutes
# from START), for the five proofs the first did not reach. Same conditions
# as the first (run.sh): one guest from M6's read-only image, the WebDAV QA
# backend, isolation under /workspace/tmp/m6-t17/, outputs whole and masked
# under guest-cycle/w2-*.out, the installed unfixed files.
#
#   bash docs/audits/2026_10_26-epic-m6-cloud-setup-content/guest-cycle/run2.sh <stage>
#   stages: up refusal exit5 mode signin phone down
#
# Stops by pidfile only. No rm -rf here.
set -uo pipefail
A=docs/audits/2026_10_26-epic-m6-cloud-setup-content
G=$A/guest-cycle
IMG=/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz
export VM_PAIR_DIR=/workspace/tmp/m6-t17/vm-pair VM_QEMU_RUNTIME_DIR=/workspace/tmp/m6-t17/run
export CLOUD_QA_STATE=/workspace/tmp/m6-t17/cloud-qa CLOUD_QA_NAME=m6-t17-cloud-qa CLOUD_QA_BACKEND=webdav
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
now() { date -u +%H:%M:%SZ; }
guest() { tools/vm-pair ssh a "$@"; }
mkdir -p "$G" "$VM_PAIR_DIR" "$VM_QEMU_RUNTIME_DIR" "$CLOUD_QA_STATE"

case "${1:-}" in
  up)
    { echo "\$ cloud-test-backend --backend webdav up  ($(now))"; tools/cloud-test-backend --backend webdav up; echo "exit $?"
      echo "\$ vm-pair reimage a <the image, .sha256 checked OK at 07:59:18>  ($(now))"; tools/vm-pair reimage a "$IMG"; echo "exit $?"
      guest 'grep -E "^BUILD_ID=" /etc/os-release; python3 --version'
      echo "\$ the guest's connection: seed-device's configuration lines only (the stanza piped, never printed)"
      tools/cloud-test-backend seed-device | sed '/^mkdir -p \/storage\/roms/,$d' | guest 'bash -s' 2>&1 | grep -v -i -E 'key|pass|token|user|psk'
      echo "exit ${PIPESTATUS[2]}"
    } 2>&1 | mask | tee "$G/w2-up.out" ;;
  refusal)
    # The match's refusal: the count made to exceed the preview's.
    root=$(tools/cloud-test-backend shipped-default CONTENT_REMOTE); root="${root#/}"
    fx=/workspace/tmp/m6-t17/w2-cloud; mkdir -p "$fx/ROMs/snes"; printf 'rom\n' > "$fx/ROMs/snes/a.zip"
    { echo "\$ the cloud side: <root>/ROMs/snes/a.zip  ($(now))"; tools/cloud-test-backend put "$fx" "$root"; echo "exit $?"
      guest 'set -u
        mkdir -p /storage/roms/snes /storage/t17
        printf "rom\n" > /storage/roms/snes/a.zip; printf "only here\n" > /storage/roms/snes/b.zip
        /usr/bin/cloud_content_restore --set-systems snes
        /usr/bin/cloud_content_restore --match > /storage/t17/w2-preview.out 2>&1; echo "preview rc $?"
        echo "plan: $(sed -n "2,\$p" /storage/.cache/cloud_sync/content-match-plan | tr "\n" " ")"
        printf "added after the preview\n" > /storage/roms/snes/c.zip; printf "added after the preview\n" > /storage/roms/snes/d.zip
        /usr/bin/cloud_content_restore --match --apply > /storage/t17/w2-apply.out 2>&1; echo "apply rc $?"
        grep -E "^(>>> why|Nothing was removed)" /storage/t17/w2-apply.out
        grep "match: snes refused" /var/log/cloud_sync.log | tail -1 | sed "s/^.*\] //"
        echo "left in roms/snes: $(ls /storage/roms/snes | tr "\n" " ")"'
      echo "exit $?"
    } 2>&1 | mask | tee "$G/w2-refusal.out" ;;
  exit5)
    # backuptool's exit 5 on a run-time-assembled credential-shaped line; the archive unchanged.
    { echo "\$ (guest) a baseline backup, then a credential-shaped line assembled at run time, then a second backup  ($(now))"
      guest 'set -u
        /usr/bin/backuptool backup > /storage/t17/w2-b1.out 2>&1; echo "baseline backup rc $?"
        newest=$(ls -1 /storage/roms/backup/*_SETTINGS.tar.gz 2>/dev/null | sort | tail -1)
        echo "newest archive: ${newest##*/}  $(sha256sum < "$newest" | cut -c1-16)"
        k="t17_pass""word"; v=$(head -c 12 /dev/urandom | od -An -tx1 | tr -d " \n")
        printf "%s = %s\n" "$k" "$v" > /storage/.config/game/t17-scan.cfg; unset v
        /usr/bin/backuptool backup > /storage/t17/w2-b2.out 2>&1; rc=$?; echo "second backup rc $rc"
        grep -E "^>>> why" /storage/t17/w2-b2.out
        after=$(ls -1 /storage/roms/backup/*_SETTINGS.tar.gz 2>/dev/null | sort | tail -1)
        echo "newest archive after: ${after##*/}  $(sha256sum < "$after" | cut -c1-16); archives at the root: $(ls -1 /storage/roms/backup/*_SETTINGS.tar.gz | wc -l); .partial left: $(ls /storage/roms/backup/*.partial 2>/dev/null | wc -l)"
        rm -f /storage/.config/game/t17-scan.cfg; echo "the planted file removed: $(test -e /storage/.config/game/t17-scan.cfg && echo no || echo yes)"'
      echo "exit $?"
    } 2>&1 | mask | tee "$G/w2-exit5.out" ;;
  mode)
    { echo "\$ (guest) atomic()'s observed mode: a real cloud_remote create on /storage/.config/rclone/rclone.conf, and atomic() under the image's python  ($(now))"
      guest 'set -u; umask
        stat -c "before: %a %n" /storage/.config/rclone/rclone.conf
        /usr/bin/cloud_remote create t17mode local nounc=true; echo "cloud_remote create rc $?"
        stat -c "after a save through atomic(): %a %n" /storage/.config/rclone/rclone.conf /storage/.config/rclone/active-connection
        python3 -I -B - <<PY
import os, stat, sys
from pathlib import Path
sys.path.insert(0, "/usr/bin")
import cloud_connections as c
os.umask(0o022)
d = Path("/var/tmp/t17-mode"); d.mkdir(parents=True, exist_ok=True)
c.CONFIG = d / "rclone.conf"; c.ACTIVE = d / "active-connection"
m = lambda p: oct(stat.S_IMODE(os.stat(p).st_mode))
c.atomic(c.CONFIG, b"[qa]\ntype = local\n"); print("atomic() new file under umask 022:", m(c.CONFIG))
os.chmod(c.CONFIG, 0o644); c.atomic(c.CONFIG, b"[qa]\ntype = local\n"); print("atomic() over an existing 0644 file:", m(c.CONFIG))
PY'
      echo "exit $?"
    } 2>&1 | mask | tee "$G/w2-mode.out" ;;
  signin)
    { echo "\$ tools/signin-memory 10022 --url http://10.0.2.2:9010/ --key <vm-pair key>  ($(now))"
      echo "  the page is the QA backend's own listing on the host: a real load, no network beyond the host (the slice's rule; the tool's default is example.org)"
      timeout 300 tools/signin-memory 10022 --url http://10.0.2.2:9010/ --key "$VM_PAIR_DIR/qa-key"; echo "exit $?"
    } 2>&1 | mask | tee "$G/w2-signin.out" ;;
  phone)
    { echo "\$ the phone page from the host: CANNOT, the gap named  ($(now))"
      echo "  the guest is behind QEMU user-mode NAT; vm-pair forwards only its ssh port (10022 for guest a). cloud_oauth serve listens on the guest's port 8080, which nothing forwards, so no host or LAN client can reach it."
      echo "  a probe of 127.0.0.1:8080 from the host: $(timeout 3 bash -c 'exec 3<>/dev/tcp/127.0.0.1/8080' 2>&1 && echo connected || echo refused)"
      echo "  the handler itself is proved by tools/t17-pin-fixture.py over loopback on the guest (window 1, fixtures.out). The gap: a hostfwd for the serve's port, or a second guest on the same NAT as the phone."
    } 2>&1 | mask | tee "$G/w2-phone.out" ;;
  down)
    { echo "\$ vm-pair down  ($(now))"; tools/vm-pair down; echo "exit $?"
      echo "\$ cloud-test-backend --backend webdav down  ($(now))"; tools/cloud-test-backend --backend webdav down; echo "exit $?"
      sleep 2
      echo "leftover at $(now):"
      echo "  qemu: $(pgrep -x qemu-system-x86 -r R,S,D,T | wc -l)"
      echo "  ss -ltn 9010-9099: $(ss -ltn | grep -cE ':90[1-9][0-9]\b')"
      echo "  ss 10022-10023: $(ss -ltn | grep -cE ':1002[23]\b')"
      echo "  pgrep rclone serve: $(pgrep -f 'rclon[e] serve' | wc -l)"
    } 2>&1 | mask | tee "$G/w2-down.out" ;;
  *) echo "usage: $0 up|refusal|exit5|mode|signin|phone|down" >&2; exit 2 ;;
esac
