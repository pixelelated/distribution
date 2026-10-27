#!/bin/bash
# readstores <label> <key regex> <output file>: run stores.sh on the guest with its two arguments set.
G=/workspace/tmp/m6-t26/guest; D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-guimenu-673; A=$D/docs/audits/2026_10_27-epic-m6-es-guimenu
s=/workspace/tmp/m6-t26/tmp/stores-run.sh; { printf 'set -- %q %q\n' "$1" "$2"; cat $A/guest-cycle/scripts/stores.sh; } > $s
cd $D && tools/vm-serial --socket $G/serial.sock --timeout 60 script $s >> "$3" 2>&1
