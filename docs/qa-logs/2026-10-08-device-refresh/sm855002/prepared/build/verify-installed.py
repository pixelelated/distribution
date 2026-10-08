from pathlib import Path
import datetime,gettext,hashlib,json,os,subprocess
O=Path(__file__).resolve().parent;j=json.loads((O/'inputs.json').read_text());T=Path(j['host_worktree']);root=T/j['build_root']/'image/system'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
release=(root/'etc/os-release').read_text();assert 'OS_NAME="pixelelated"' in release and j['distribution_commit'] in release and j['distribution_branch'] in release
manifest=json.loads((T/'docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/stage01/install-manifest.json').read_text());installed={}
for e in manifest['installed_files']:
 source=T/Path(e['source']).relative_to('/workspace/repos/rocknix');target=root/e['destination'].lstrip('/')
 assert target.read_bytes()==source.read_bytes(),target
 if e['destination'].startswith('/usr/bin/'):assert target.stat().st_mode&0o111
 installed[e['destination']]=sha(target)
for target,source in [('usr/share/post-update','projects/ROCKNIX/packages/rocknix/sources/post-update'),('usr/bin/duckstation_screenshot_path','projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/scripts/duckstation_screenshot_path'),('usr/bin/start_duckstation.sh','projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/scripts/start_duckstation.sh'),('usr/config/duckstation/settings.ini','projects/ROCKNIX/packages/emulators/standalone/duckstation-sa/config/SM8550/settings.ini')]:
 assert (root/target).read_bytes()==(T/source).read_bytes(),target;installed['/'+target]=sha(root/target)
assert not (root/'usr/bin/cloud_migrate_layout').exists() and not (root/'usr/bin/cloud_migrate_layout').is_symlink()
assert (root/'usr/bin/duckstation-sa').stat().st_mode&0o777==0o755
assert (root/'usr/lib/libcom_err.so.2').exists()
es=T/j['build_root']/'build'/('emulationstation-'+j['emulationstation_commit'])
for n in ['es-app/src/CloudText.cpp','es-app/src/CloudText.h','es-app/src/guis/GuiMenu.cpp']:
 assert (es/n).read_bytes()==subprocess.check_output(['git','-C','/home/max/Development/emulationstation-next.worktrees/qa-integration','show',j['emulationstation_commit']+':'+n]),n
messages=json.loads((T/'docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/host01/new-messages.json').read_text())
with (root/'usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo').open('rb') as f:catalog=gettext.GNUTranslations(f)
for en,fr in messages.items():assert catalog.gettext(en)==fr,en
installed['/usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo']=sha(root/'usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo')
for n in ['LICENSE.md','TRADEMARK.md']:
 assert (root/'usr/share/licenses/pixelelated'/n).read_bytes()==(T/n).read_bytes()
 installed['/usr/share/licenses/pixelelated/'+n]=sha(root/'usr/share/licenses/pixelelated'/n)
for n in ['emulationstation','retroarch']:
 p=root/'usr/bin'/n
 with p.open('rb') as f:header=f.read(20)
 assert header[:6]==b'\x7fELF\x02\x01' and header[18:20]==b'\xb7\x00';installed['/usr/bin/'+n]=sha(p)
arm=T/'build.pixelelated-SM8550.arm';a=arm/'image/system';assert (arm/'.stamps/arm/build_target').exists();files={};links={};elf=[]
for p in sorted(a.rglob('*')):
 n=str(p.relative_to(a))
 if p.is_symlink():links[n]=os.readlink(p)
 elif p.is_file():
  files[n]=sha(p)
  with p.open('rb') as f:h=f.read(20)
  if h[:5]==b'\x7fELF\x01' and h[18:20]==b'\x28\x00':elf.append(n)
stamps={str(p.relative_to(arm)):sha(p) for p in sorted((arm/'.stamps').rglob('build_*')) if p.is_file()}
assert len(files)>=7800 and len(elf)>=900 and len(stamps)>=240
old=json.loads(Path(j['cache_parent_provenance']['arm_manifest']).read_text());diff=[n for n,h in files.items() if old['files'].get(n)!=h]
(O/'artifacts/arm-output-manifest.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','files':files,'symlinks':links,'arm_elf':elf,'stamps':stamps,'changed_from_prior_arm':diff},indent=2)+'\n')
(O/'artifacts/installed-inclusion.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','sha256':installed,'exact_ES_source':j['emulationstation_commit'],'french_translations_checked':len(messages),'no_retired_migration':True,'duckstation_mode':'755','libcom_err_present':True,'arm_files':len(files),'arm_elf':len(elf),'arm_stamps':len(stamps)},indent=2)+'\n')
print('PASS SM8550 exact installed helper/default/native/post-update/ES/catalog/identity/ARM output inclusion',flush=True)
