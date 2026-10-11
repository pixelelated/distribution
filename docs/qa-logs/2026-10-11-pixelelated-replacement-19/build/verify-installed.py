from pathlib import Path
import hashlib,json,subprocess,gettext,xml.etree.ElementTree as ET
p=Path('/workspace/tmp/pixelelated-m7-build19');j=json.loads((p/'inputs.json').read_text());r=Path.cwd();root=r/j['build_root']/'image/system'
fields={k:v.strip('"') for k,v in (line.split('=',1) for line in (root/'etc/os-release').read_text().splitlines() if '=' in line)}
assert fields['OS_NAME']=='pixelelated' and fields['OS_BUILD']=='dev'
assert fields['BUILD_ID']==j['distribution_commit'] and fields['BUILD_BRANCH']==j['distribution_branch']
assert fields['OS_VERSION']=='0.0.1-dev' and fields['BUILD_TIMESTAMP']==j['build_timestamp']
assert fields['BUILD_VERSION']=='0.0.1-dev+'+j['build_timestamp']+'.g'+j['distribution_commit'][:12]
mappings={}
for name in ['LICENSE.md','TRADEMARK.md']:mappings['usr/share/licenses/pixelelated/'+name]=name
manifest=json.loads((r/'docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/stage01/install-manifest.json').read_text())
for e in manifest['installed_files']:mappings[e['destination'].lstrip('/')]=str(Path(e['source']).relative_to('/workspace/repos/rocknix'))
for folder in ['network/rclone/sources','network/raofflineproxy/sources']:
 for source in (r/'projects/ROCKNIX/packages'/folder).iterdir():
  if source.is_file() and (root/'usr/bin'/source.name).is_file():mappings['usr/bin/'+source.name]=str(source.relative_to(r))
for name in ['cloud_backup','cloud_restore','cloud_setup','cloud_remote','cloud_connections.py','cloud_oauth','cloud_scan','cloud_folder_validate','cloud_content_backup','cloud_content_restore']:
 mappings['usr/bin/'+name]='projects/ROCKNIX/packages/network/rclone/sources/'+name
for name in ['raofflineproxy-ctl','raofflineproxy-cache-indexed','raofflineproxy-cache-images','raofflineproxy-refresh']:
 mappings['usr/bin/'+name]='projects/ROCKNIX/packages/network/raofflineproxy/sources/'+name
for name in ['wifictl','usbgadget','rocknix-info','backuptool']:
 mappings['usr/bin/'+name]='projects/ROCKNIX/packages/rocknix/sources/scripts/'+name
mappings.update({'usr/bin/sway-ready':'projects/ROCKNIX/packages/wayland/compositor/sway/scripts/sway-ready','usr/lib/systemd/system/essway.service':'projects/ROCKNIX/packages/ui/emulationstation/system.d/essway.service','usr/share/post-update':'projects/ROCKNIX/packages/rocknix/sources/post-update','usr/lib/sway/sway-generic-x64':'projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/sway/sway-generic-x64','usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf':'projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf'})
for target,source in mappings.items():
 assert (root/target).read_bytes()==(r/source).read_bytes(),target
 if target.startswith('usr/bin/'):assert (root/target).stat().st_mode & 0o111,target
assert not (root/'usr/bin/cloud_migrate_layout').exists()
version=subprocess.check_output([str(root/'usr/bin/rclone'),'version'],text=True)
assert version.splitlines()[0]=='rclone v1.75.2';(p/'installed-rclone-version.txt').write_text(version)
proxy=r/j['build_root']/'build'/('raofflineproxy-'+j['proxy_commit'])
for name,digest in j['proxy_qualified_files'].items():assert hashlib.sha256((proxy/name).read_bytes()).hexdigest()==digest,name
es=r/j['build_root']/'build'/('emulationstation-'+j['emulationstation_commit'])
for name in ['es-app/src/guis/GuiMenu.cpp','es-app/src/guis/GuiWifi.cpp','es-app/src/CloudText.cpp','es-app/src/CloudText.h']:
 expected=subprocess.check_output(['git','-C','/home/max/Development/emulationstation-next.worktrees/qa-integration','show',j['emulationstation_commit']+':'+name]);assert (es/name).read_bytes()==expected,name
browser=r/j['build_root']/'build'
browsers=list(browser.glob('cloud-signin-window-*/cloud-signin-window.c'));assert len(browsers)==1,browsers
assert browsers[0].read_bytes()==(r/'projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c').read_bytes()
messages=json.loads((r/'docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/host01/new-messages.json').read_text())
with (root/'usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo').open('rb') as f:french=gettext.GNUTranslations(f)
for en,want in messages.items():assert french.gettext(en)==want,en
assert b'THE CLOUD FOLDER WAS NOT CHANGED.' in (root/'usr/bin/emulationstation').read_bytes()
assert (root/'usr/lib/libcom_err.so.2').exists()
oldroot=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18')/j['build_root']/'image/system'
assert hashlib.sha256((root/'usr/bin/duckstation-sa').read_bytes()).digest()==hashlib.sha256((oldroot/'usr/bin/duckstation-sa').read_bytes()).digest()
artifacts={str(x.relative_to(r)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (r/'target').iterdir() if x.is_file()}
(p/'installed-result.json').write_text(json.dumps({'result':'PASS','identity':fields,'mapped_files':mappings,'proxy_source_files':len(j['proxy_qualified_files']),'artifacts':artifacts},indent=2)+'\n')
print('PASS assembled identity, exact helpers, ES/browser/proxy source, retained DuckStation and catalogue translations',flush=True)
