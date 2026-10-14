#!/usr/bin/env python3
"""Source-only preparation after final build receipts exist; launches nothing."""
import argparse, hashlib, json, re, shutil, subprocess, tarfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
for name in ['checkout','custody','owner']:p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--expected-commit',required=True);p.add_argument('--expected-es',required=True)
p.add_argument('--vnc',type=int,required=True)
a=p.parse_args();tree=a.checkout.resolve(strict=True);out=a.owner.absolute()
assert out.parent==Path('/workspace/tmp') and not out.exists() and re.fullmatch(r'pix[A-Za-z0-9_-]+',out.name)
assert re.fullmatch('[0-9a-f]{40}',a.expected_commit) and re.fullmatch('[0-9a-f]{40}',a.expected_es)
assert 100<=a.vnc<=199

def sha(f):
    with f.open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
def write(f,x):f.write_text(json.dumps(x,indent=2)+'\n')
def checked(row,limit=None):
    f=Path(row['path']).resolve(strict=True)
    assert f.is_file() and re.fullmatch('[0-9a-f]{64}',row['sha256'])
    if limit is not None:assert f.stat().st_size<=limit and sha(f)==row['sha256']
    return f
def seal(root,expected):
    assert sha(root/'SHA256SUMS')==expected
    names=set()
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);f=Path(name)
        assert not f.is_absolute() and '..' not in f.parts and name not in names
        assert sha(root/f)==digest;names.add(name)
    assert {str(f.relative_to(root)) for f in root.rglob('*') if f.is_file()}==names|{'SHA256SUMS'}
def extract(archive,out,archive_hash,manifest_hash):
    assert sha(archive)==archive_hash;out.mkdir()
    with tarfile.open(archive) as tar:
        members=tar.getmembers();assert sum(x.size for x in members)<=1024**2
        for m in members:
            name=Path(m.name);assert not name.is_absolute() and '..' not in name.parts
            assert m.isfile() or m.isdir()
            if m.isdir():(out/name).mkdir(parents=True,exist_ok=True)
            else:
                target=out/name;target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('xb') as stream:stream.write(tar.extractfile(m).read())
    seal(out,manifest_hash)
assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()==a.expected_commit
recipe=(tree/'projects/ROCKNIX/packages/ui/emulationstation/package.mk').read_text()
assert re.search(r'^PKG_VERSION="([0-9a-f]{40})"$',recipe,re.M).group(1)==a.expected_es
custody=json.loads(a.custody.read_text())
assert custody['status']=='PASS' and custody['distribution_commit']==a.expected_commit and custody['es_commit']==a.expected_es
assert custody['reviewed_install_to_system_identity'] is True
for name in ['image','system']:checked(custody[name]) # Full reads occur only under the admitted runtime owner.
assert 0<custody['image']['raw_bytes']<=16*1024**3
root=Path(custody['system']['root']).resolve(strict=True);assert root!=Path('/') and root.is_dir()
for name in ['boot_config','source_receipt','update_report','install_report']:checked(custody[name],2*1024**2)
source=json.loads(Path(custody['source_receipt']['path']).read_text())
assert source['status']=='PASS' and source['distribution_commit']==a.expected_commit
assert source['reviewed_source_to_bytecode_and_strip_chain'] is True
for row in source['evidence']:checked(row,32*1024**2)
helper=Path('/workspace/repos/rocknix.worktrees/m7-offline-vm-567/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm')
assert sha(helper)=='5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d'
# Bind exact existing helper dependencies and frozen command sources, including profile.
tools=[helper,helper.parent/'profile.json']+[tree/x for x in ['tools/vm-serial','tools/vm-stop','tools/watch-build','tools/watch-job','tools/watch-build-submit','tools/pixelelated-state-check-test','tools/pixelelated-state-check','docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh']]
assert sha(tools[-1])=='a49a0bb3f8b5ed937dafc7524c70e2ce9ce74e925478d421dc0f7e3a20e957da'
# Verify this new packet independently before carrying it into the owner.
for line in (HERE/'SHA256SUMS').read_text().splitlines():
    digest,name=line.split('  ',1);assert sha(HERE/name)==digest
out.mkdir(mode=0o700)
for name in ['records','scan','vm','lifecycle-owner','clean','source']:(out/name).mkdir()
extract(tree/'docs/qa-logs/2026-10-14-proxy-installed-startup-plan/source-originals.tar.gz',out/'source/installed588',
 '13fe8cffc164bff77ea9b0b66dd788ed8c0b5ee5a5a303f558fdd306c1006e31','dcbee145f6f7c41da944416bcdd4cb4868be91aeaf1a7935b52d1e1db68f4301')
extract(tree/'docs/qa-logs/2026-10-14-installed-state-correction/source-originals.tar.gz',out/'source/correction',
 '5e1255cbf9d22d1b2f0ff7b128be9f657d82be2d6e38870fccc284d7bc4111dd','bc4a76241fc24c40a61be59821c15ce5d9eb9514e4e8a34f203a5306b6431b08')
# Existing positive-identity post-check, never a replacement for original payload checks.
cmd=['python3','-I','-S','-B',str(out/'source/correction/check-shared-identity.py'),'--update',custody['update_report']['path'],'--install',custody['install_report']['path']]
r=subprocess.run(cmd,capture_output=True,timeout=10)
(out/'records/shared-identity.stdout').write_bytes(r.stdout);(out/'records/shared-identity.stderr').write_bytes(r.stderr)
write(out/'records/shared-identity-exit.json',{'original_returncode':r.returncode,'argv':cmd});assert r.returncode==0
# Prepare corrected retained derivative for a SEPARATE later upgrade allocation; do not seed this guest.
cmd=['python3','-I','-S','-B',str(out/'source/correction/materialize.py'),'--original',str(tree/'docs/qa-logs/2026-10-14-m7-installed-state-plan/retained-fixture'),'--output',str(out/'source/retained-corrected')]
r=subprocess.run(cmd,capture_output=True,timeout=15)
(out/'records/retained-prepare.stdout').write_bytes(r.stdout);(out/'records/retained-prepare.stderr').write_bytes(r.stderr)
write(out/'records/retained-prepare-exit.json',{'original_returncode':r.returncode,'argv':cmd});assert r.returncode==0
for name in ['vm-lifecycle.py','run-guest.py','close.py']:shutil.copy2(HERE/name,out/name)
shutil.copy2(a.custody,out/'records/final-custody.original.json')
shutil.copy2(custody['source_receipt']['path'],out/'records/source-receipt.original.json')
config={'status':'PREPARED_UNRUN','checkout':str(tree),'commit':a.expected_commit,'es_commit':a.expected_es,'vnc':a.vnc,
 'helper':str(helper),'custody':custody,'custody_sha256':sha(a.custody),'tools':{str(f):sha(f) for f in tools},
 'code':{name:sha(out/name) for name in ['vm-lifecycle.py','run-guest.py','close.py']},'work_seconds':900,'cleanup_seconds':90}
write(out/'config.json',config)
write(out/'records/inputs.json',{'installed588_manifest':'dcbee145f6f7c41da944416bcdd4cb4868be91aeaf1a7935b52d1e1db68f4301','correction_manifest':'bc4a76241fc24c40a61be59821c15ce5d9eb9514e4e8a34f203a5306b6431b08','source_packets_unchanged':True,'config_sha256':sha(out/'config.json')})
plan={'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],
 'protected':[str(out/'records'),str(out/'source'),str(tree/'tools/host-maintenance'),custody['image']['path'],custody['system']['path'],str(root)],'candidates':[],
 'builds':[{'name':'m7-installed-clean-then-588','terms_bytes':{'raw_image':custody['image']['raw_bytes'],'guest_disk':16*1024**3,'media_records':512*1024**2},
 'basis':'One fresh unchanged default-boot no-NIC 4CPU/8GiB guest. Clean check before fixture media or seeding. 900s work alarm plus <=90s cleanup; proxy command310s +10s grace. Single owned QEMU; existing serial/watch/admission/stop tools. No host or per-service cgroup memory cap presumed. Export original receipts before explicit consumption/retirement.',
 'evidence':[{'path':str(out/x),'sha256':sha(out/x)} for x in ['config.json','records/inputs.json','vm-lifecycle.py','run-guest.py']]}]}
write(out/'retention-plan.json',plan)
write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-installed-clean-then-588','profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],
 'outputs':[{'path':str(out/'vm'),'issue':588,'kind':'qa-scratch','release_when':'Original clean/proxy/owner/watch/stop receipts exported and reviewed, actual owners gone; consume admission then explicitly retire disk/media/UEFI.'}]})
print(json.dumps({'owner':str(out),'status':'PREPARED_ONLY_UNRUN','next':'review and admit the existing lifecycle; preparation is not runtime evidence'}))
