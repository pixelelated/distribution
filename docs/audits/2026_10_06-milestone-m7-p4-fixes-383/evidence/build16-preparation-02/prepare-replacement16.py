"""Prepare candidate16 only after the serial candidate15 coverage is complete."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os,re,shutil,subprocess

repo=Path('/workspace/repos/rocknix')
old=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15')
new=old.with_name('m7-pixelelated-replacement16')
parent=Path('/workspace/tmp/pixelelated-m7-replacement-15')
owner=parent.with_name('pixelelated-m7-replacement-16')
expected_product=['projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore',
                  'projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout',
                  'projects/ROCKNIX/packages/ui/emulationstation/package.mk']
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()
assert git('branch','--show-current')=='next' and not git('status','--porcelain')
for name,want in [('pixelelated-m7-p4-coverage-ui-05','1'),('pixelelated-m7-p4-fresh-root-07','0'),('pixelelated-m7-p4-no-join-negative-02','0')]:
    p=Path('/workspace/tmp')/name
    v=json.loads((p/'owner-verification.json').read_text());assert set(v['channels'].values())=={want},name
    assert json.loads((p/'guest-cleanup-verification.json').read_text())['passed'],name
p=Path('/workspace/tmp/pixelelated-m7-p4-partial-retry-host-02')
assert set(json.loads((p/'owner-verification.json').read_text())['channels'].values())=={'0'}
assert json.loads((p/'host-cleanup-verification.json').read_text())['passed']
for group,count in [('focused',22),('full',398)]:
    rows=json.loads((p/'artifacts'/group/'results.json').read_text())
    assert len(rows)==count and all(x['status']=='PASS' for x in rows),(group,len(rows))
source=p/'artifacts/current-cloud_migrate_layout'
assert source.read_bytes()==(Path('/workspace/repos/rocknix.worktrees/conflict-resolution')/'projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout').read_bytes()
for p in Path('/proc').glob('[0-9]*/cmdline'):
    try:first=p.read_bytes().split(b'\0')[0].decode()
    except (OSError,UnicodeError):continue
    assert not Path(first).name.startswith('qemu-system-'),p
parent_inputs=json.loads((parent/'inputs.json').read_text());commit=git('rev-parse','HEAD')
delta=git('diff','--no-renames','--name-only',parent_inputs['distribution_commit'],commit,'--','packages','projects','scripts','config','distributions','Makefile').splitlines()
assert delta==expected_product,delta
es=re.search(r'^PKG_VERSION="([0-9a-f]{40})"', (repo/expected_product[-1]).read_text(),re.M)[1]
assert es!=parent_inputs['emulationstation_commit']
es_tree=Path('/home/max/Development/emulationstation-next.worktrees/qa-integration')
assert subprocess.check_output(['git','-C',str(es_tree),'rev-parse','HEAD'],text=True).strip()==es
assert not subprocess.check_output(['git','-C',str(es_tree),'status','--porcelain'],text=True).strip()
copy_owner=Path('/workspace/tmp/pixelelated-m7-p4-es-interruption-copy-publication-01')
assert set(json.loads((copy_owner/'owner-verification.json').read_text())['channels'].values())=={'0'}
assert es==json.loads((copy_owner/'publication.json').read_text())['commit']
assert set(json.loads(Path('/workspace/tmp/pixelelated-m7-p4-interruption-copy-host-03/owner-verification.json').read_text())['channels'].values())=={'0'}
assert not new.exists() and not owner.exists()
# Cache15 was measured under a watched owner; retain the original 40/80/100 GiB reserves.
cache=111663730688;budget=cache+(40+80+100)*1024**3
fs=os.statvfs('/workspace');available=fs.f_bavail*fs.f_frsize
assert available>budget,(available,budget)
owner.mkdir(mode=0o700);(owner/'cache-copy').mkdir(mode=0o700)
(owner/'capacity.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),available_bytes=available,measured_cache_bytes=cache,measurement_owner='/workspace/tmp/pixelelated-m7-replacement-16-capacity-01',package_growth_gib=40,qa_image_budget_gib=80,operating_margin_gib=100,required_bytes=budget,no_deletion=True),indent=2)+'\n')
subprocess.run(['git','-C',str(repo),'worktree','add',str(new),'-b','build/m7-pixelelated-replacement16',commit],check=True)
j=dict(parent_inputs)
j.update(distribution_commit=commit,distribution_branch='build/m7-pixelelated-replacement16',host_worktree=str(new),emulationstation_commit=es,frozen_at=datetime.now(timezone.utc).isoformat(),build_mode='independent checksum/inode-verified copy of replacement15; clean rclone and ES; rebuild image',cache_parent_distribution=parent_inputs['distribution_commit'],cache_parent_bundle='43a698bcd7d570c63ebdd5db015e5302463f7ee4a15438fd9ef2359437be19da',cache_parent_manifest_sha256=hashlib.sha256((parent/'inputs.json').read_bytes()).hexdigest(),purpose='M7.P4 remaining audit repairs; PL001/003/004/005 pending installed acceptance')
for key in ['source_files','qa_source_files']:j[key]={p:hashlib.sha256((new/p).read_bytes()).hexdigest() for p in parent_inputs[key]}
j['source_symlinks']={p:os.readlink(new/p) for p in parent_inputs['source_symlinks']}
(owner/'inputs.json').write_text(json.dumps(j,sort_keys=True,indent=2)+'\n')
(owner/'freeze-receipt.json').write_text(json.dumps(dict(manifest_sha256=hashlib.sha256((owner/'inputs.json').read_bytes()).hexdigest(),source_files=len(j['source_files']),qa_source_files=len(j['qa_source_files']),source_symlinks=len(j['source_symlinks']),changed_inputs=delta,commit=commit,emulationstation_commit=es),indent=2)+'\n')
def advance(text):
    return text.replace('m7-pixelelated-replacement15','m7-pixelelated-replacement16').replace('pixelelated-m7-replacement-15','pixelelated-m7-replacement-16').replace('m7-pixelelated-replacement14','m7-pixelelated-replacement15').replace('pixelelated-m7-replacement-14','pixelelated-m7-replacement-15')
for name in ['verify-source.py','progress.py','outer.sh','copy-outer.sh']:
    (owner/name).write_text(advance((parent/name).read_text()));shutil.copymode(parent/name,owner/name)
copy=advance((parent/'copy-cache.sh').read_text()).replace(parent_inputs['distribution_commit'],commit)
copy=re.sub(r'^assert product==.*$', 'assert product=='+repr(expected_product)+',product',copy,flags=re.M)
(owner/'copy-cache.sh').write_text(copy);(owner/'copy-cache.sh').chmod(0o755)
build=advance((parent/'build.sh').read_text()).replace('for TASK_PACKAGE in rclone cloud-signin-window emulationstation;','for TASK_PACKAGE in rclone emulationstation;')
build=build.replace("for name in ['emulationstation','cloud-signin-window']:","for name in ['emulationstation']:")
build=build.replace("print('PASS changed installed scripts and both rebuilt binaries',flush=True)","assert (root/'usr/bin/cloud-signin-window').read_bytes()==(oldroot/'usr/bin/cloud-signin-window').read_bytes()\nprint('PASS repaired installed scripts and rebuilt ES; unchanged sign-in window',flush=True)")
(owner/'build.sh').write_text(build);(owner/'build.sh').chmod(0o755)
for name in ['build.sh','copy-cache.sh','outer.sh','copy-outer.sh']:subprocess.run(['bash','-n',str(owner/name)],check=True)
for name in ['verify-source.py','progress.py']:ast.parse((owner/name).read_text())
subprocess.run(['python3','-I',str(owner/'verify-source.py')],cwd=new,check=True)
names=['build.sh','outer.sh','verify-source.py','copy-cache.sh','copy-outer.sh','progress.py','inputs.json','capacity.json']
(owner/'harness.sha256').write_text(''.join(hashlib.sha256((owner/n).read_bytes()).hexdigest()+'  '+str(owner/n)+'\n' for n in names))
print(json.dumps(dict(state='prepared, not submitted',owner=str(owner),tree=str(new),commit=commit,es=es)))
