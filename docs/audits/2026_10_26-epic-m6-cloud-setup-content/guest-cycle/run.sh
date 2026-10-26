#!/bin/bash
# T17 (#664): the one guest window (granted 07:5x UTC on #664, under T13's
# conditions). One GENERIC_X64 guest from M6's read-only image, the WebDAV QA
# backend, both on this lane's isolation under /workspace/tmp/m6-t17/. The
# guest runs the installed, unfixed files, so every fixture is run with
# --expect unfixed. Every output is kept whole under guest-cycle/, masked.
#
#   bash docs/audits/2026_10_26-epic-m6-cloud-setup-content/guest-cycle/run.sh <stage>
#   stages: pre up hashes fixtures f02 f03 down
#
# Stops by pidfile only (vm-pair down, the backend's down). No rm -rf here:
# a removal is its own short command outside this script.
set -uo pipefail
A=docs/audits/2026_10_26-epic-m6-cloud-setup-content
G=$A/guest-cycle
IMG=/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz
export VM_PAIR_DIR=/workspace/tmp/m6-t17/vm-pair VM_QEMU_RUNTIME_DIR=/workspace/tmp/m6-t17/run
export CLOUD_QA_STATE=/workspace/tmp/m6-t17/cloud-qa CLOUD_QA_NAME=m6-t17-cloud-qa CLOUD_QA_BACKEND=webdav
R=8ebaf8daad
RC=projects/ROCKNIX/packages/network/rclone/sources
INSTALLED=(cloud_connections.py cloud_content_backup cloud_content_restore cloud_content_transfer cloud_device_id
           cloud_folder_validate cloud_log_scrub cloud_oauth cloud_remote cloud_scan cloud_setup)
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
now() { date -u +%H:%M:%SZ; }
guest() { tools/vm-pair ssh a "$@"; }
mkdir -p "$G" "$VM_PAIR_DIR" "$VM_QEMU_RUNTIME_DIR" "$CLOUD_QA_STATE"

case "${1:-}" in
  pre)
    { echo "\$ sha256sum -c <the image's .sha256>  ($(now))"
      ( cd "$(dirname "$IMG")" && sha256sum -c "$(basename "$IMG").sha256" ); echo "exit $?"
      stat -c '%s bytes  %n' "$IMG"
      echo "census: qemu $(pgrep -x qemu-system-x86 -r R,S,D,T | wc -l); listeners 9010-9099/10022-10023: $(ss -ltn | grep -cE ':(90[1-9][0-9]|1002[23])\b')"
    } 2>&1 | mask | tee "$G/pre.out" ;;
  up)
    { echo "\$ cloud-test-backend --backend webdav up  ($(now))"; tools/cloud-test-backend --backend webdav up; echo "exit $?"
      echo "\$ vm-pair reimage a <the image>  ($(now))"; tools/vm-pair reimage a "$IMG"; echo "exit $?"
      echo "\$ the guest's identity  ($(now))"
      guest 'grep -E "^(BUILD_ID|VERSION|BUILD_BRANCH)=" /etc/os-release; python3 --version; /usr/bin/rclone version | head -1; /usr/bin/busybox | head -1; ls -l /usr/bin/cloud-signin-window /usr/bin/backuptool'
      echo "exit $?"
    } 2>&1 | mask | tee "$G/up.out" ;;
  hashes)
    { echo "\$ the installed files against git show $R:<path>  ($(now))"
      same=0; diff=0
      for f in "${INSTALLED[@]}" backuptool; do
        if [ "$f" = backuptool ]; then src=projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool; else src=$RC/$f; fi
        want=$(git show "$R:$src" | sha256sum | cut -d' ' -f1)
        got=$(guest "sha256sum /usr/bin/$f" | cut -d' ' -f1)
        if [ "$want" = "$got" ]; then echo "same      /usr/bin/$f  $got"; same=$((same + 1))
        else echo "DIFFERENT /usr/bin/$f  installed $got  tree $want"; diff=$((diff + 1))
          guest "cat /usr/bin/$f" | mask > "/workspace/tmp/m6-t17/g-installed-$f"
          git show "$R:$src" | mask | diff - "/workspace/tmp/m6-t17/g-installed-$f" | sed 's/^/    /'
        fi
      done
      echo "installed and hashed: $((same + diff)) ($same same, $diff different)"
      echo "not installed as source: $RC/../../cloud-signin-window/sources/cloud-signin-window.c and its package.mk (the binary /usr/bin/cloud-signin-window, compiled; listed in up.out)"
    } 2>&1 | tee "$G/hashes.out" ;;
  fixtures)
    { echo "\$ the fixtures copied to the guest's /storage/t17  ($(now))"
      guest 'mkdir -p /storage/t17/tmp'
      for t in pin option-key selection content archive; do tools/vm-pair scp a "$A/tools/t17-$t-fixture.py" "/storage/t17/t17-$t-fixture.py" || echo "scp $t failed"; done
      run() { local name="$1"; shift
        echo "\$ (guest) python3 -I -B t17-$name-fixture.py $*  ($(now))"
        guest "cd /storage/t17 && TMPDIR=/storage/t17/tmp python3 -I -B t17-$name-fixture.py $*" 2>&1 | grep -v '^Traceback\|^  File\|^    '
        echo "exit ${PIPESTATUS[0]}"; }
      run pin --file /usr/bin/cloud_oauth --expect unfixed
      run option-key --sources /usr/bin --rclone /usr/bin/rclone --expect unfixed
      run selection --sources /usr/bin --busybox /usr/bin/busybox --expect unfixed
      run content --sources /usr/bin --busybox /usr/bin/busybox --real-rclone /usr/bin/rclone --expect unfixed
      run archive --file /usr/bin/backuptool --busybox /usr/bin/busybox
    } 2>&1 | mask | tee "$G/fixtures.out" ;;
  f02)
    # The stage-B condition: the flag in the guest's conf only, over the seeded
    # synthetic root only (/storage/roms/snes, written here), the conf put back.
    root=$(tools/cloud-test-backend shipped-default CONTENT_REMOTE); root="${root#/}"
    fx=/workspace/tmp/m6-t17/f02-cloud; mkdir -p "$fx/ROMs/snes"; printf 'rom\n' > "$fx/ROMs/snes/a.zip"
    { echo "\$ the cloud side: <root>/ROMs/snes/a.zip at the QA backend  ($(now))"
      tools/cloud-test-backend put "$fx" "$root"; echo "exit $?"
      echo "\$ the guest's connection: seed-device's configuration lines only (the stanza piped, never printed)"
      tools/cloud-test-backend seed-device | sed '/^mkdir -p \/storage\/roms/,$d' | guest 'bash -s' 2>&1 | grep -v -i -E 'key|pass|token|user|psk'
      echo "exit ${PIPESTATUS[2]}"
      guest 'set -u
        ls -A /storage/roms/snes 2>/dev/null | wc -l | sed "s/^/files already in roms\/snes: /"
        cp -p /storage/.config/cloud_sync.conf /storage/t17/cloud_sync.conf.base
        echo "base conf: $(sha256sum < /storage/t17/cloud_sync.conf.base | cut -c1-16)"
        /usr/bin/cloud_content_restore --set-systems snes'
      for case in control delete-excluded include; do
        case "$case" in
          control) v="" ;;
          delete-excluded) v="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1 --delete-excluded" ;;
          include) v="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1 --include=*" ;;
        esac
        echo "\$ (guest) case $case  ($(now))"
        guest "set -u
          mkdir -p /storage/roms/snes
          printf 'rom\n' > /storage/roms/snes/a.zip; printf 'only on this device\n' > /storage/roms/snes/b.zip; printf 'a save\n' > /storage/roms/snes/a.srm
          if [ -n '$v' ]; then grep -v '^RCLONE_NET_OPTS=' /storage/t17/cloud_sync.conf.base > /storage/.config/cloud_sync.conf; printf 'RCLONE_NET_OPTS=\"%s\"\n' '$v' >> /storage/.config/cloud_sync.conf; fi
          echo \"RCLONE_NET_OPTS line: \$(grep -c '^RCLONE_NET_OPTS=' /storage/.config/cloud_sync.conf), carries the flag: \$(grep -c -e '--delete-excluded' -e '--include' /storage/.config/cloud_sync.conf)\"
          /usr/bin/cloud_content_restore --match > /storage/t17/f02-$case-preview.out 2>&1; echo \"preview rc \$?\"
          echo \"plan: \$(sed -n '2,\$p' /storage/.cache/cloud_sync/content-match-plan 2>/dev/null | tr '\n' ' ')\"
          /usr/bin/cloud_content_restore --match --apply > /storage/t17/f02-$case-apply.out 2>&1; echo \"apply rc \$?\"
          echo \"left in roms/snes: \$(ls /storage/roms/snes | tr '\n' ' ')\"
          cp -p /storage/t17/cloud_sync.conf.base /storage/.config/cloud_sync.conf
          echo \"conf put back: \$(cmp -s /storage/t17/cloud_sync.conf.base /storage/.config/cloud_sync.conf && echo identical || echo DIFFERS)\""
        echo "exit $?"
        guest "tail -n 15 /storage/t17/f02-$case-apply.out" | sed 's/^/    apply: /'
      done
    } 2>&1 | mask | tee "$G/f02.out" ;;
  f03)
    { echo "\$ the QA backend's data before  ($(now))"
      tools/cloud-test-backend ls 2>&1 | sort > /workspace/tmp/m6-t17/f03-before.txt; cat /workspace/tmp/m6-t17/f03-before.txt
      echo "\$ (guest) cloud_content_backup ../.config  ($(now))"
      guest '/usr/bin/cloud_content_backup ../.config > /storage/t17/f03.out 2>&1; echo "rc $?"; grep -E "^(>>>|Backing)" /storage/t17/f03.out | head -5'
      echo "\$ the QA backend's data after  ($(now))"
      tools/cloud-test-backend ls 2>&1 | sort > /workspace/tmp/m6-t17/f03-after.txt; cat /workspace/tmp/m6-t17/f03-after.txt
      echo "\$ what the backup carried there (after minus before)"
      comm -13 /workspace/tmp/m6-t17/f03-before.txt /workspace/tmp/m6-t17/f03-after.txt
      echo "\$ cloud-test-backend path"; tools/cloud-test-backend path
    } 2>&1 | mask | tee "$G/f03.out" ;;
  down)
    { echo "\$ vm-pair down  ($(now))"; tools/vm-pair down; echo "exit $?"
      echo "\$ cloud-test-backend --backend webdav down  ($(now))"; tools/cloud-test-backend --backend webdav down; echo "exit $?"
      sleep 2
      echo "leftover at $(now):"
      echo "  qemu: $(pgrep -x qemu-system-x86 -r R,S,D,T | wc -l)"
      echo "  ss -ltn 9010-9099: $(ss -ltn | grep -cE ':90[1-9][0-9]\b')"
      echo "  ss 10022-10023: $(ss -ltn | grep -cE ':1002[23]\b')"
      echo "  pgrep rclone serve: $(pgrep -f 'rclon[e] serve' | wc -l)"
      echo "  docker ps -a m6-t17-cloud-qa*: $(docker ps -a --filter name=m6-t17-cloud-qa -q 2>/dev/null | wc -l)"
    } 2>&1 | mask | tee "$G/down.out" ;;
  *) echo "usage: $0 pre|up|hashes|fixtures|f02|f03|down" >&2; exit 2 ;;
esac
