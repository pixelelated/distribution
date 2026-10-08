"""Prepare the next engineering owner only after final audit publication is accepted."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,shutil,sys
repo=Path('/workspace/repos/rocknix'); tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17'); owner=Path('/workspace/tmp/pixelelated-m7-replacement-17'); prev=Path('/workspace/tmp/pixelelated-m7-replacement-16'); oldtree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16')
commit=sys.argv[1];assert re.fullmatch('[0-9a-f]{40}',commit)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(repo),*a],text=True).strip()
assert git('rev-parse','next')==commit and git('ls-remote','origin','refs/heads/next').split()[0]==commit
assert not git('status','--porcelain')
audit=repo/'docs/audits/2026_10_08-milestone-m7-p5-delta-507'
assert (audit/'audit-completion.json').is_file()
subprocess.run([str(repo/'tools/lint-audit-artifacts'),str(audit),'--phase','resolution'],check=True)
j=json.loads((prev/'inputs.json').read_text());assert json.loads((prev/'completion.json').read_text())['result']=='PASS'
assert git('show',commit+':projects/ROCKNIX/packages/ui/emulationstation/package.mk').count('PKG_VERSION="1d76b3da7da75794066df1c089931b890304da7a"')==1
es='1d76b3da7da75794066df1c089931b890304da7a'; esrepo=Path('/home/max/Development/emulationstation-next.worktrees/qa-integration')
assert subprocess.check_output(['git','-C',str(esrepo),'ls-remote','origin','refs/heads/test/qa-integration'],text=True).split()[0]==es
for name,h in j['source_files'].items():assert sha(oldtree/name)==h,name
for name,target in j['source_symlinks'].items():assert os.readlink(oldtree/name)==target,name
expected=sorted(x.split('\t',1)[1] for x in json.loads((repo/'docs/qa-logs/2026-10-08-m7-build-readiness/read-only-preparation.json').read_text())['candidate16_to_audit_input_paths'])
actual=git('diff','--no-renames','--name-only',j['distribution_commit'],commit,'--','packages','projects','scripts','config','distributions','Makefile').splitlines();assert actual==expected,(actual,expected)
assert not tree.exists() and not owner.exists()
subprocess.run(['git','-C',str(repo),'worktree','add','--quiet','-b','build/m7-pixelelated-replacement17',str(tree),commit],check=True);owner.mkdir()
files={};links={}
for raw in subprocess.check_output(['git','-C',str(tree),'ls-files','-z','--','packages','projects','scripts','config','distributions','Makefile','LICENSE.md','TRADEMARK.md','tools/watch-build','tools/watch-job']).split(b'\0'):
 if not raw:continue
 name=os.fsdecode(raw);p=tree/name
 if p.is_symlink():links[name]=os.readlink(p)
 else:assert p.is_file();files[name]=sha(p)
qa={os.fsdecode(p):sha(tree/os.fsdecode(p)) for p in subprocess.check_output(['git','-C',str(tree),'ls-files','-z','--','tools']).split(b'\0') if p and (tree/os.fsdecode(p)).is_file()}
assert sha(Path(j['host_options_path']))==j['host_options_sha256']
assert subprocess.check_output(['docker','image','inspect',j['container'],'--format','{{.Id}}'],text=True).strip()==j['container_image_id']
previous=j['distribution_commit'];j.update(distribution_commit=commit,distribution_branch='build/m7-pixelelated-replacement17',emulationstation_commit=es,frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),build_mode='Independent verified candidate16 cache copy; current manual cloud setup, DuckStation and audited ES; engineering image',source_files=files,source_symlinks=links,qa_source_files=qa,recipe_files=sum(p.endswith('/package.mk') for p in files),host_worktree=str(tree),cache_parent_distribution=previous,cache_parent_manifest_sha256=sha(prev/'inputs.json'),cache_parent_bundle=None,purpose='M7.P5 #508 assembled-image inclusion and CF10 clean/public ROCKNIX adoption after resolved #507/#524')
p=owner/'inputs.json';p.write_text(json.dumps(j,sort_keys=True,indent=2)+'\n');p.chmod(0o400)
receipt={'manifest_sha256':sha(p),'source_files':len(files),'source_symlinks':len(links),'qa_source_files':len(qa),'changed_inputs':expected,'commit':commit,'emulationstation_commit':es};(owner/'freeze-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
mapping={'m7-pixelelated-replacement15':'m7-pixelelated-replacement16','m7-pixelelated-replacement16':'m7-pixelelated-replacement17','pixelelated-m7-replacement-15':'pixelelated-m7-replacement-16','pixelelated-m7-replacement-16':'pixelelated-m7-replacement-17'};pattern=re.compile('|'.join(map(re.escape,mapping)))
def adapt(s):return pattern.sub(lambda m:mapping[m.group()],s)
for name in ['verify-source.py','outer.sh','copy-outer.sh','progress.py']:(owner/name).write_text(adapt((prev/name).read_text()))
s=adapt((prev/'copy-cache.sh').read_text()).replace(previous,commit);a,b=s.split('assert product==',1);_,c=b.split(',product',1);s=a+'assert product=='+repr(expected)+',product'+c;(owner/'copy-cache.sh').write_text(s)
s=adapt((prev/'build.sh').read_text()).replace('for TASK_PACKAGE in rclone emulationstation;','for TASK_PACKAGE in rclone emulationstation duckstation-sa;')
s=s.replace("['cloud_content_restore','cloud_migrate_layout','cloud_oauth','cloud_scan','cloud_setup']","['cloud_content_restore','cloud_folder_validate','cloud_oauth','cloud_scan','cloud_setup']")
anchor="print('PASS repaired installed scripts and rebuilt ES; unchanged sign-in window',flush=True)"
assert anchor in s
extra='''# Verify all current source-qualified helpers/defaults in the assembled root.
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
'''
s=s.replace(anchor,anchor+'\n'+extra);(owner/'build.sh').write_text(s)
for p in owner.glob('*.sh'):p.chmod(0o755);subprocess.run(['bash','-n',str(p)],check=True)
for p in owner.glob('*.py'):compile(p.read_text(),str(p),'exec')
subprocess.run(['python3',str(owner/'verify-source.py')],cwd=tree,check=True)
(owner/'harness.sha256').write_text(''.join(sha(owner/name)+'  '+str(owner/name)+'\n' for name in ['build.sh','outer.sh','verify-source.py','copy-cache.sh','copy-outer.sh','progress.py']))
print(json.dumps(receipt,indent=2))
