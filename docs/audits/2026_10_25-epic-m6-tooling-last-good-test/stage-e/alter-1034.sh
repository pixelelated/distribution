#!/bin/bash
# #1034: backuptool's member list leaves system.cfg out, so the archive has no
# such member. Must FAIL on the fixed file: "with the wifi key stripped" (the
# unfixed negated pipeline reads nothing from the missing member and PASSes).
. "$(dirname "$0")/alter-lib.sh"
change "${R}/rocknix/sources/scripts/backuptool" 'find storage -type f \) 2>/dev/null > "\$\{MEMBERLIST\}"' \
    's/find storage -type f \) 2>\/dev\/null > "\$\{MEMBERLIST\}"/find storage -type f ! -name system.cfg ) 2>\/dev\/null > "${MEMBERLIST}"/'
