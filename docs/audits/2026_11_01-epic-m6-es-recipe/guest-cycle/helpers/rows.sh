#!/bin/bash
# T37 (#684): the window's rows G-01 to G-06, over vm-serial sh only, every output through the device
# read filter (FILTER) or, where a line's presence is the evidence, the masking sed. Writes nothing on
# the guest. Each row's output goes to guest-cycle/gNN-*.txt with its start and end times.
. "$(dirname "$0")/run-sheet.sh"
M='s/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'
row() { local id=$1 name=$2; shift 2; local f="$GC/$id-$name.txt"; { echo "== $id $(date -u +%FT%TZ)"; "$@"; echo "== end $(date -u +%FT%TZ)"; } > "$f" 2>&1; echo "$id done $(date -u +%FT%TZ) lines=$(wc -l < "$f")"; }
g01() {
  echo "-- host: the image file"; ls -l /workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz | awk '{print $5, $9}'
  echo "-- guest"; ser "grep -E '^(BUILD_ID|BUILD_BRANCH|BUILD_VERSION)=' /etc/os-release; sha256sum /usr/bin/emulationstation" | grep -v -i -E "$FILTER"
}
g02() {
  ser "ls /usr/share/themes/; cd /usr/share/themes/es-theme-art-book-next && ls pixelelated-wordmark.svg Tiny5-OFL.txt; ls -d _inc/systems/artwork-* 2>&1 | head -20; echo removed-includes=\$(grep -c -E 'include name=\"(noir|nintendont|circuit|outline)\"' theme.xml); echo zh-blocks=\$(grep -c 'lang=\"zh\"' fonts.xml); echo patch0001-logoText=\$(grep -c 'name=\"logoText\"' theme.xml); echo patch001-splash-include=\$(grep -c 'displayName=\"pixelelated\"' theme.xml) splash-wordmark=\$(grep -c 'pixelelated-wordmark.svg' splash.xml); echo patch001-tools=\$(grep -c \"system.theme} == 'tools'\" theme.xml); ls -l _inc/fonts/; ls -l /usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf; echo themes-link=\$(readlink /etc/emulationstation/themes); cat /usr/config/emulationstation/es_settings.cfg; grep -i theme /storage/.config/emulationstation/es_settings.cfg" | grep -v -i -E "$FILTER"
}
g03() {
  echo "-- host: the tree's cfg digests at 2174265e9c"; for c in es_features es_input es_savestates es_settings; do printf '%s  %s\n' "$(git -C "$D" show 2174265e9c:projects/ROCKNIX/packages/ui/emulationstation/config/common/$c.cfg | sha256sum | cut -d' ' -f1)" "$c.cfg"; done
  echo "-- guest"; ser "cd /usr/config/emulationstation && sha256sum es_features.cfg es_input.cfg es_savestates.cfg es_settings.cfg; echo vulkan-lines=\$(grep -c -i vulkan es_features.cfg); echo link=\$(readlink /etc/emulationstation/es_systems.cfg); test -e /etc/emulationstation/es_systems.cfg; echo resolves rc=\$?; stat -c '%a %n' /usr/config/emulationstation/*.cfg; ls -l /usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo; echo share-locale=\$(readlink /usr/share/locale) lib-locale=\$(readlink /usr/lib/locale); ls -d /usr/config/locale/en_US.UTF-8; ls /usr/config/locale | wc -l" | grep -v -i -E "$FILTER"
}
g04() {
  echo "-- host: the tree's script digests at 2174265e9c"; for s in sources/start_es.sh sources/es_settings sources/serial_number_check; do printf '%s  %s\n' "$(git -C "$D" show 2174265e9c:projects/ROCKNIX/packages/ui/emulationstation/$s | sha256sum | cut -d' ' -f1)" "${s#sources/}"; done
  echo "-- guest"; ser "systemctl show -p ActiveState,FragmentPath essway.service emustation.service; systemctl cat essway.service | sed -n '1,25p'; ls -l /usr/lib/systemd/system/rocknix.target.wants/ 2>/dev/null | grep -E 'essway|emustation'; sha256sum /usr/bin/start_es.sh /usr/bin/es_settings /usr/bin/serial_number_check; ls -l /var/log/es_log.txt; echo es-pid=\$(pidof emulationstation)" | grep -v -i -E "$FILTER"
  echo "-- guest: the running ES's argv (masked)"; ser "tr '\\0' ' ' < /proc/\$(pidof emulationstation | cut -d' ' -f1)/cmdline; echo" | sed -E "$M"
  echo "-- guest: boot to interface (journal, filtered)"; ser "journalctl -b -o short-monotonic --no-pager | grep -E 'Started (essway|emustation|sway)|Starting (essway|emustation)|Reached target|start_es|Startup finished' | head -20; cat /proc/uptime" | grep -v -i -E "$FILTER"
}
g05() {
  ser "head -n 5 /usr/bin/es_settings /usr/bin/serial_number_check; echo names=\$(strings /usr/bin/emulationstation | grep -c -E 'SCREENSCRAPER_DEV_LOGIN|SCREENSCRAPER_RUNTIME_DEV_LOGIN|GAMESDB_APIKEY|CHEEVOS_DEV_LOGIN|HFS_DEV_LOGIN'); echo cpugov-string=\$(strings /usr/bin/emulationstation | grep -c 100-amd64-freqfunctions); ls -l /usr/config/emulationstation/resources/logo.png; echo cjk-link=\$(readlink /usr/config/emulationstation/resources/DroidSansFallbackFull.ttf); test -e /usr/config/emulationstation/resources/DroidSansFallbackFull.ttf; echo cjk-resolves rc=\$?" | grep -v -i -E "$FILTER"
  echo "-- the state check on the guest: CANNOT -- the tool is not on the image and the window writes nothing (its host half: stage-b/state-check-root.out)"
}
g06() { ser "ls /usr/share/lowerdeck; ls /usr/share/lowerdeck | wc -l" | grep -v -i -E "$FILTER"; }
case "${1:-all}" in all) row g01 identity g01; row g02 themes g02; row g03 configs g03; row g04 services g04; row g05 sources g05; row g06 lowerdeck g06;; *) row "$1" "$2" "$1";; esac
