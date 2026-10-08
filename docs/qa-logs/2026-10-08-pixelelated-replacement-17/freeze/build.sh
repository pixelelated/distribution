#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17
TASK_OWNER=/workspace/tmp/pixelelated-m7-replacement-17
TASK_CONTAINER_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated
TASK_CACHE=/workspace/cache/rocknix-sources
# Refuse the wrong watcher root before cleaning any package (#435).
[ "$(pwd -P)" = "$TASK_TREE" ] || { echo "Refusing build: start watch-build from the frozen worktree" >&2; exit 2; }
cd "$TASK_TREE"
[ "$(id -u)" = 1000 ]
[ ! -e "$TASK_OWNER/build.start" ]
[ "$(cat "$TASK_OWNER/cache-ready.rc")" = 0 ]
[ -f "$TASK_OWNER/cache-ready.json" ]
[ -z "$(git status --porcelain)" ]
python3 "$TASK_OWNER/verify-source.py"
tools/rc-preflight --only proxy-schema
tools/build-preflight > "$TASK_OWNER/host-preflight.txt"
cat "$TASK_OWNER/host-preflight.txt"
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/build.start"
finish() {
  result=$?
  trap - EXIT
  printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
  exit "$result"
}
trap finish EXIT
export DOCKER_WORK_DIR="$TASK_CONTAINER_TREE"
export DOCKER_EXTRA_OPTS="-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v $TASK_CACHE:$TASK_CONTAINER_TREE/sources"
for TASK_PACKAGE in rclone emulationstation duckstation-sa; do
 PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 PACKAGE="$TASK_PACKAGE" make docker-package-clean
done
rm -f build.pixelelated-GENERIC_X64.x86_64/.stamps/image/build_target
make docker-GENERIC_X64
python3 "$TASK_OWNER/verify-source.py"
python3 - <<'PY'
from pathlib import Path
import json
j=json.loads(Path('/workspace/tmp/pixelelated-m7-replacement-17/inputs.json').read_text())
root=Path(j['build_root'])/'image/system'
release=(root/'etc/os-release').read_text()
assert 'OS_NAME="pixelelated"' in release and j['distribution_commit'] in release and j['distribution_branch'] in release
assert (root/'usr/bin/raofflineproxy-ctl').read_bytes()==Path('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl').read_bytes()
for p in ['LICENSE.md','TRADEMARK.md']:
 assert (root/'usr/share/licenses/pixelelated'/p).read_bytes()==Path(p).read_bytes(),p
import xml.etree.ElementTree as ET
for installed,source in [('etc/profile.d/999-export','projects/ROCKNIX/packages/hardware/quirks/profile.d/999-export'),('etc/profile.d/001-functions','projects/ROCKNIX/packages/rocknix/profile.d/001-functions'),('usr/bin/chksysconfig','projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig'),('usr/config/modules/gamelist.xml','projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml'),('usr/bin/cloud_setup','projects/ROCKNIX/packages/network/rclone/sources/cloud_setup'),('usr/bin/rocknix-memory-manager','projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-memory-manager')]:
 assert (root/installed).read_bytes()==Path(source).read_bytes(),installed
ET.parse(root/'usr/config/modules/gamelist.xml')
import subprocess
child=subprocess.run(['/bin/sh','-c',"OS_NAME=pixelelated; OS_VERSION=0.0.1; OS_BUILD=community; . \"$1\"; exec /bin/sh -c 'printf \"%s\\n\" \"${OS_NAME-unset}\" \"${OS_VERSION-unset}\" \"${OS_BUILD-unset}\"'",'assembled-export',str(root/'etc/profile.d/999-export')],env={'PATH':'/usr/bin:/bin'},text=True,capture_output=True)
assert child.returncode==0 and not child.stderr and child.stdout.splitlines()==['pixelelated','0.0.1','community'],(child.returncode,child.stdout,child.stderr)
init=(Path(j['build_root'])/'initramfs/init').read_text()
assert '[ \"GENERIC_X64\" = \"GENERIC_X64\" ] && [ \"${DEBUG}\" != \"yes\" ]' in init
assert '@DEVICENAME@' not in init
assert 'quiet console=ttyS0,115200 console=tty0' in Path('projects/ROCKNIX/devices/GENERIC_X64/options').read_text()
import hashlib
proxy_source=Path(j['build_root'])/'build'/('raofflineproxy-'+j['proxy_commit'])/'linux/raofflineproxy/config.py'
assert hashlib.sha256(proxy_source.read_bytes()).hexdigest()=='3184e88b2eac7b5da3a5e0f5906ae193f1dcda7df7e0849d05cd5ec91fe5e3bb'
usage_source=Path(j['build_root'])/'build'/('raofflineproxy-'+j['proxy_commit'])/'linux/raofflineproxy/usage_stats.py'
assert hashlib.sha256(usage_source.read_bytes()).hexdigest()=='cfb9bc5cb9da9432fa0531559e4915e9fd07eebcbf8d6eab19c88105436e24ff'
assert (root/'usr/lib/sway/sway-generic-x64').read_bytes()==Path('projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/sway/sway-generic-x64').read_bytes()
assert (root/'usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf').read_bytes()==Path('projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf').read_bytes()
assert (root/'usr/lib/sway/sway-generic-x64').stat().st_mode & 0o111
print('PASS assembled GENERIC_X64 renderer wrapper and service drop-in match frozen bytes',flush=True)
print('PASS assembled initramfs quiet fallback, OS_NAME export, XML/text, proxy, identity and licence payload',flush=True)

for name in ['cloud_content_restore','cloud_folder_validate','cloud_oauth','cloud_scan','cloud_setup']:
 assert (root/'usr/bin'/name).read_bytes()==Path('projects/ROCKNIX/packages/network/rclone/sources',name).read_bytes(),name
oldroot=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16')/j['build_root']/'image/system'
for name in ['emulationstation']:
 assert hashlib.sha256((root/'usr/bin'/name).read_bytes()).digest()!=hashlib.sha256((oldroot/'usr/bin'/name).read_bytes()).digest(),name
assert b'Connect&eacute;' in (root/'usr/bin/cloud-signin-window').read_bytes()
assert (root/'usr/bin/cloud-signin-window').read_bytes()==(oldroot/'usr/bin/cloud-signin-window').read_bytes()
print('PASS repaired installed scripts and rebuilt ES; unchanged sign-in window',flush=True)
# Verify all current source-qualified helpers/defaults in the assembled root.
manifest=json.loads(Path('docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/stage01/install-manifest.json').read_text())
for entry in manifest['installed_files']:
 source=Path(entry['source']).relative_to('/workspace/repos/rocknix')
 target=root/entry['destination'].lstrip('/')
 assert target.read_bytes()==source.read_bytes(),str(target)
 if entry['destination'].startswith('/usr/bin/'):assert target.stat().st_mode & 0o111
assert not (root/'usr/bin/cloud_migrate_layout').exists()
assert (root/'usr/bin/duckstation-sa').stat().st_mode & 0o777==0o755
for name in ['start_duckstation.sh','duckstation_screenshot_path']:
 assert (root/'usr/bin'/name).read_bytes()==Path('projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/scripts',name).read_bytes()
assert (root/'usr/lib/libcom_err.so.2').exists()
es_source=Path(j['build_root'])/'build'/('emulationstation-'+j['emulationstation_commit'])
es_git='/home/max/Development/emulationstation-next.worktrees/qa-integration'
for name in ['es-app/src/CloudText.cpp','es-app/src/CloudText.h','es-app/src/guis/GuiMenu.cpp']:
 expected=subprocess.check_output(['git','-C',es_git,'show',j['emulationstation_commit']+':'+name])
 assert (es_source/name).read_bytes()==expected,name
# CMake regenerates POT/PO during i18n; check installed translations by meaning.
import gettext
messages=json.loads(Path('docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/host01/new-messages.json').read_text())
with (root/'usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo').open('rb') as stream:
 french=gettext.GNUTranslations(stream)
for en,want in messages.items():assert french.gettext(en)==want,en
assert b'THE CLOUD FOLDER WAS NOT CHANGED.' in (root/'usr/bin/emulationstation').read_bytes()
print('PASS22 installed helper/default mappings, retired migration absence, DuckStation mode/helpers, libcom_err presence, exact ES source and11 installed French translations',flush=True)

PY
