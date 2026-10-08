#!/bin/bash
set -uo pipefail
BASE=/workspace/tmp/pixelelated-510-coverage02
SSH=(ssh -i "$BASE/guest01/qa-key" -p 10212 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1)
SCP=(scp -q -i "$BASE/guest01/qa-key" -P 10212 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null)
"${SSH[@]}" 'systemctl stop essway.service' && "${SCP[@]}" "$BASE/build05/emulationstation" root@127.0.0.1:/storage/qa512/es513 && "${SCP[@]}" "$BASE/build05/artifacts/fr.mo" root@127.0.0.1:/storage/qa512/fr513.mo && "${SSH[@]}" 'umount /usr/bin/emulationstation; umount /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; chmod 755 /storage/qa512/es513; mount --bind /storage/qa512/es513 /usr/bin/emulationstation; mount --bind /storage/qa512/fr513.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; sha256sum /usr/bin/emulationstation /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; systemctl start essway.service'
rc=$?
printf "%s\n" "$rc" > "$BASE/ui03/inner.rc"
exit "$rc"
