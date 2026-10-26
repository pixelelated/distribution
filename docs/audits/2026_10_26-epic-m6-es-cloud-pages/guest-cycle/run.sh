#!/bin/bash
# T18 (#665): the one guest window (granted 10:02 UTC on #665, under T13's
# conditions: 30 minutes from START plus 5 of grace). One GENERIC_X64 guest
# from the M6 copy of 069fc2704421's image, the WebDAV QA backend local on
# the host, both on this lane's isolation under /workspace/tmp/m6-t18/.
# Every output is kept whole under guest-cycle/, through the mask.
#
#   bash docs/audits/2026_10_26-epic-m6-es-cloud-pages/guest-cycle/run.sh <stage>
#   stages, in order: pre up identity walks f08 ttp down
#
# Stops by pidfile only (vm-pair down, the backend's down). No rm -rf here:
# a removal is its own short command outside this script.
set -uo pipefail
A=docs/audits/2026_10_26-epic-m6-es-cloud-pages
G=$A/guest-cycle
S=/workspace/tmp/m6-t18
IMG=/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz
export VM_PAIR_DIR=$S/vm-pair VM_QEMU_RUNTIME_DIR=$S/run ROCKNIX_ARTIFACTS=$S/artifacts TMPDIR=$S/tmp
export CLOUD_QA_STATE=$S/cloud-qa CLOUD_QA_NAME=m6-t18-cloud-qa CLOUD_QA_BACKEND=webdav
LITERAL="FOLDERS ALREADY CREATED WILL STAY. YOU CAN TRY AGAIN LATER."
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
now() { date -u +%H:%M:%SZ; }
guest() { tools/vm-pair ssh a "$@"; }
census() { echo "census $(now): qemu $(pgrep -x qemu-system-x86 -r R,S,D,T | wc -l); listeners 9010-9099/10022-10023: $(ss -ltn | grep -cE ':(90[1-9][0-9]|1002[23])\b'); cc1plus $(pgrep -x cc1plus | wc -l)"; }
mkdir -p "$G" "$VM_PAIR_DIR" "$VM_QEMU_RUNTIME_DIR" "$CLOUD_QA_STATE" "$ROCKNIX_ARTIFACTS" "$TMPDIR"

case "${1:-}" in
  pre)
    { echo "\$ sha256sum -c <the image's .sha256>  ($(now))"
      ( cd "$(dirname "$IMG")" && sha256sum -c "$(basename "$IMG").sha256" ); echo "exit $?"
      stat -c '%s bytes  %n' "$IMG"
      census
    } 2>&1 | mask | tee "$G/pre.out" ;;
  up)
    { echo "\$ cloud-test-backend --backend webdav up  ($(now))"; tools/cloud-test-backend --backend webdav up; echo "exit $?"
      echo "\$ vm-pair reimage a <the image>  ($(now))"; tools/vm-pair reimage a "$IMG"; echo "exit $?"
      echo "\$ vm-pair info  ($(now))"; tools/vm-pair info
    } 2>&1 | mask | tee "$G/up.out" ;;
  identity)
    { echo "\$ the installed EmulationStation against the pin  ($(now))"
      guest 'grep -E "^(BUILD_ID|VERSION|BUILD_BRANCH)=" /etc/os-release; sha256sum /usr/bin/emulationstation; ls -l /usr/bin/setsid /bin/setsid 2>/dev/null; readlink -f "$(command -v setsid)"'
      echo "exit $?"
      for s in "$LITERAL" "STOPPING IT SO YOU CAN PLAY" "RECORDING YOUR LAST GAME" "CANCEL THIS BACKUP OR RESTORE?" "NOTHING NEW TO SEND UP" "COMPARING WITH THIS DEVICE..."; do
        printf 'strings | grep -c -F %-62s %s\n' "\"$s\"" "$(guest "strings /usr/bin/emulationstation | grep -c -F \"$s\"")"
      done
      echo "the pin's package.mk: 069fc2704421 is not in the distribution repository; the binary is named by its strings above"
    } 2>&1 | mask | tee "$G/identity.out" ;;
  walks)
    { echo "\$ vm-qa --skip-up --only walks --walk <the seven>  ($(now))"
      tools/vm-qa --skip-up --only walks \
        --walk to-manage-cloud-storage --walk restore-page --walk match-dialog --walk to-change-cloud-folder \
        --walk confirm-cloud-folder --walk run-transfer-frames --walk run-transfer
      echo "exit $?"
      echo "\$ run-transfer again, for the run with nothing new (F-09)  ($(now))"
      tools/vm-qa --skip-up --only walks --walk run-transfer
      echo "exit $?"
      ls -d "$ROCKNIX_ARTIFACTS"/rocknix-images/qa-* 2>/dev/null
    } 2>&1 | mask | tee "$G/walks.out" ;;
  f08)
    { M=$(tools/vm-pair info 2>/dev/null | grep -o -E '/[^ ]*rocknix-qemu-monitor\.sock' | head -1)
      echo "monitor: ${M:-NONE}"
      [ -n "$M" ] || { echo "CANNOT: no monitor socket"; exit 0; }
      echo "\$ the match's systems set, as the suite's match-dialog pre does  ($(now))"
      guest 'cloud_content_restore --set-systems "gb snes"'; echo "exit $?"
      echo "\$ vm-visual-qa dismiss; run to-manage-cloud-storage; run f08-cancel-match  ($(now))"
      tools/vm-visual-qa --monitor "$M" dismiss; echo "exit $?"
      tools/vm-visual-qa --monitor "$M" run --outdir "$S/f08" tools/vm-walks/to-manage-cloud-storage.steps; echo "exit $?"
      tools/vm-visual-qa --monitor "$M" run --outdir "$S/f08" "$G/f08-cancel-match.steps"; echo "exit $?"
      ls -l "$S/f08"
    } 2>&1 | mask | tee "$G/f08.out" ;;
  ttp)
    { M=$(tools/vm-pair info 2>/dev/null | grep -o -E '/[^ ]*rocknix-qemu-monitor\.sock' | head -1)
      echo "\$ time-to-play --vm --only launch,exit,g2g --repeat 3 --backend webdav  ($(now))"
      tools/time-to-play --port 10022 --identity "$VM_PAIR_DIR/qa-key" --monitor "$M" --backend webdav \
        --out "$S/ttp" --only launch,exit,g2g --repeat 3 --vm
      echo "exit $?"
    } 2>&1 | mask | tee "$G/ttp.out" ;;
  down)
    { echo "\$ vm-pair down  ($(now))"; tools/vm-pair down; echo "exit $?"
      echo "\$ cloud-test-backend --backend webdav down  ($(now))"; tools/cloud-test-backend --backend webdav down; echo "exit $?"
      sleep 2
      echo "leftover at $(now):"
      echo "  qemu: $(pgrep -x qemu-system-x86 -r R,S,D,T | wc -l)"
      echo "  ss -ltn 9010-9099: $(ss -ltn | grep -cE ':90[1-9][0-9]\b')"
      echo "  ss 10022-10023: $(ss -ltn | grep -cE ':1002[23]\b')"
      echo "  pgrep rclone serve: $(pgrep -f 'rclon[e] serve' | wc -l)"
      echo "  docker ps -a m6-t18-cloud-qa*: $(docker ps -a --filter name=m6-t18-cloud-qa -q 2>/dev/null | wc -l)"
      census
    } 2>&1 | mask | tee "$G/down.out" ;;
  *) echo "usage: $0 pre|up|identity|walks|f08|ttp|down" >&2; exit 2 ;;
esac
