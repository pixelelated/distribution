#!/bin/bash
# #1037, the acknowledgement case: ack_index_pending is there but answers 127 at
# once, as an absent function would. Must FAIL on the fixed file ("an ack for
# token A over a marker holding B keeps B in place"): the unfixed grep -q 'rc=1'
# matched rc=127 and PASSed, the marker untouched. (Removing the function, as
# alter-1037.sh does, leaves an empty extract and a syntax error both files FAIL.)
. "$(dirname "$0")/alter-lib.sh"
change "${R}/network/raofflineproxy/sources/raofflineproxy-ctl" '^ack_index_pending\(\) *\{$' \
    's/^(ack_index_pending\(\) *\{)$/\1\n    return 127   # T15 #1037 constructed: an ack that answers 127/' \
    'T15 #1037 constructed: an ack that answers 127'
