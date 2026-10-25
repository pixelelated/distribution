#!/bin/bash
# #1031: a broken lock and a broken acknowledgement. Must FAIL on the fixed file:
#   "F-PB-21" (the keeper's flock no longer waits; the shim still marks the step)
#   "gpt G-D-03: a marker an index writes while a top-up is at its jobs outlives
#    that top-up" (the ack removes whatever marker is there)
. "$(dirname "$0")/alter-lib.sh"
change "${R}/rocknix/sources/scripts/rocknix-corekeep" 'flock 8 && LOCKED=1$' 's/flock 8 && LOCKED=1$/flock -n 8 || true \&\& LOCKED=1   # T15 #1031 constructed: no wait/'
change "${R}/network/raofflineproxy/sources/raofflineproxy-ctl" '^ack_index_pending\(\) *\{$' \
    's/^(ack_index_pending\(\) *\{)$/\1\n    rm -f "${INDEX_PENDING}"; return 0   # T15 #1031 constructed: the ack takes any marker/' \
    'T15 #1031 constructed: the ack takes any marker'
