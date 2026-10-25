#!/bin/bash
# #1027: set_autosave writes the third case's output on every run (setsettings.sh,
# its first body line). Must FAIL on the fixed file: the first two "without a
# state file" cases and "and without a state file no -e is spliced"; the
# unfixed file's joined check reads only the last case and PASSes.
. "$(dirname "$0")/alter-lib.sh"
change "${R}/rocknix/sources/scripts/setsettings.sh" '^function set_autosave\(\) \{$' \
    's/^function set_autosave\(\) \{$/function set_autosave() {\n  AUTOSAVE=0; SNAPSHOT=2; STATEFILE=""; SETTING_AUTOSAVE=1   # T15 #1027 constructed: every run is the third case/' \
    'T15 #1027 constructed'
