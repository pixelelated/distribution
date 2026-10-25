#!/bin/bash
# #1036, the retirement gate: the rclone recipe names cloud_migrate_layout with an
# option (cp -f) while the source has no engine. Must be CANNOT (exit 2) on the
# fixed file; the unfixed gate knew only 'cp cloud_migrate_layout' and read it
# as retired (NOT APPLICABLE).
. "$(dirname "$0")/alter-lib.sh"
F="${R}/network/rclone/package.mk"
printf 'post_makeinstall_target() {\n  cp -f cloud_migrate_layout ${INSTALL}/usr/bin/   # T15 #1036 constructed\n}\n' >> "${F}"
echo "  ${F#${C}/}:$(grep -n 'cp -f cloud_migrate_layout' "${F}" | cut -d: -f1): a cp -f of the engine the source does not have"
