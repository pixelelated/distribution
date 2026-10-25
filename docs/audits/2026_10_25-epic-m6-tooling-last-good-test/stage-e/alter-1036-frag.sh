#!/bin/bash
# #1036, q's historical pass: 007-syncthing removed from the working tree (not
# from history). Run q under BASE_REF=717bc04449 --old: the fixed file lists the
# ref's fragments, includes 007-syncthing, and q's promise fires (its
# raofflineproxy.conf check FAILs); the unfixed one listed the working tree's,
# left it out, and PASSed.
. "$(dirname "$0")/alter-lib.sh"
F="${R}/network/syncthing/daemons/007-syncthing"
[ -f "${F}" ] || { echo "alter: no ${F#${C}/}" >&2; exit 2; }
rm -- "${F}"; echo "  ${F#${C}/}: removed from the working tree (still at the ref)"
