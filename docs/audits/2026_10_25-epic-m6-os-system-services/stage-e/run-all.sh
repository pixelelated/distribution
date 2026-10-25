#!/bin/bash
# T22 stage E: every stream's case, both ways and crossed.
#   T22_BUSYBOX=<initramfs busybox> run-all.sh <stage-D tree> <fixed tree>
# The trees are checkouts (or exports) whose files are read: the stage-D tip
# 0f7ece71e8 and the fixed tip. Writes only under $TMPDIR. Exit 0 when every
# expected line appears and every crossed run says UNEXPECTED.
set -u
U=${1:?stage-D tree}; F=${2:?fixed tree}; here=$(cd "$(dirname "$0")" && pwd)
: "${TMPDIR:?}" "${T22_BUSYBOX:?}"
INIT=projects/ROCKNIX/packages/sysutils/busybox/scripts/init
QUIRK=projects/ROCKNIX/packages/hardware/quirks/platforms/GENERIC_X64/095-cloud-ssh
bad=0
one() {  # one <driver> <file> <mode> <expect: met|UNEXPECTED>
  local line; line=$(T22_UNFIXED="$U/$QUIRK" bash "$1" "$2" "$3" | tail -1)
  printf '%-10s %-8s %s\n' "${1##*/stage-e/}" "$3" "$line"
  case "$4:$line" in met:*expectation-met*|UNEXPECTED:*UNEXPECTED*) ;; *) bad=1 ;; esac
}
one "$here/s1/drive.sh" "$U/$INIT" unfixed met
one "$here/s1/drive.sh" "$F/$INIT" fixed met
one "$here/s1/drive.sh" "$F/$INIT" unfixed UNEXPECTED
one "$here/s1/drive.sh" "$U/$INIT" fixed UNEXPECTED
one "$here/s3/drive.sh" "$U/$QUIRK" unfixed met
one "$here/s3/drive.sh" "$F/$QUIRK" fixed met
one "$here/s3/drive.sh" "$F/$QUIRK" unfixed UNEXPECTED
one "$here/s3/drive.sh" "$U/$QUIRK" fixed UNEXPECTED
[ $bad = 0 ] && echo "run-all: PASS (8 of 8)" || echo "run-all: FAIL"
exit $bad
