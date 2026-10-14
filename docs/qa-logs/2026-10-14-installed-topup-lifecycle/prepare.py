#!/usr/bin/env python3
"""Prepare one installed #567 owner from completed image/source custody; launches nothing."""
import argparse,hashlib,json,re,shutil,subprocess,tarfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ARCHIVE='f4bf36374f52dca36f5823404974affc9b8d0ad5c303fcbf3f25180ec0509eb4'
SEAL='f4af7321d227950b4b658efb20dc30fa7862998960ae8cd9da5dd65a4cb9d8c8'
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024**2),b''):h.update(chunk)
    return h.hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def seal(root,want=None):
    if want:assert sha(root/'SHA256SUMS')==want
    names=set()
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);p=Path(name)
        assert not p.is_absolute() and '..' not in p.parts and name not in names
        assert sha(root/p)==digest;names.add(name)
    assert {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}==names|{'SHA256SUMS'}
p=argparse.ArgumentParser(description=__doc__)
for name in ['checkout','verification','custody','adapter-archive','owner']:p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--vnc',type=int,required=True)
a=p.parse_args();tree=a.checkout.resolve(strict=True);verify=a.verification.resolve(strict=True);out=a.owner.absolute()
assert out.parent==Path('/workspace/tmp') and re.fullmatch('pix[A-Za-z0-9_-]+',out.name) and not out.exists()
assert 100<=a.vnc<=199
commit=subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True,timeout=10).strip()
assert re.fullmatch('[0-9a-f]{40}',commit)
assert not subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True,timeout=10).strip()
v=json.loads((verify/'result.json').read_text());i=json.loads((verify/'inputs.json').read_text());custody=json.loads(a.custody.read_text())
assert v['status']==custody['status']=='PASS' and v['source']==i['source']==custody['distribution_commit']==commit
assert v['es_commit']==i['es_commit']==custody['es_commit']
assert i['identity']['device']=='GENERIC_X64' and i['identity']['arch']=='x86_64'
assert custody['reviewed_install_to_system_identity'] is True
image=Path(custody['image']['path']).resolve(strict=True);system=Path(custody['system']['path']).resolve(strict=True)
assert image.is_file() and system.is_file() and image.name.endswith('.img.gz')
assert i['artifacts'][str(image)]['sha256']==custody['image']['sha256'] and image.stat().st_size==i['artifacts'][str(image)]['bytes']
assert v['payload']['SYSTEM']['sha256']==custody['system']['sha256'] and system.stat().st_size==v['payload']['SYSTEM']['bytes']
raw=verify/'candidate.img';assert raw.is_file() and raw.stat().st_size==custody['image']['raw_bytes'] and 0<raw.stat().st_size<=16*1024**3
root=Path(custody['system']['root']).resolve(strict=True);assert root!=Path('/') and root.is_dir()
for name in ['source_receipt','boot_config','update_report','install_report']:
    row=custody[name];f=Path(row['path']);assert f.is_file() and f.stat().st_size<=2*1024**2 and sha(f)==row['sha256']
source_path=Path(custody['source_receipt']['path']);source=json.loads(source_path.read_text())
assert source['status']=='PASS' and source['distribution_commit']==commit and source['reviewed_source_to_bytecode_and_strip_chain'] is True
assert source['package_build_original_exit']==source['python_compile_original_exit']==0 and source['prepared_python_files']==112
assert source['post_strip_rchash_sha256']==v['products']['usr/lib/libraproxy_rchash.so']['sha256']
assert source['evidence']
for row in source['evidence']:
    f=Path(row['path']);assert f.is_file() and f.stat().st_size==row['bytes'] and row['bytes']<=32*1024**2 and sha(f)==row['sha256']
es=v['products']['usr/bin/emulationstation']['sha256']
assert source.get('es_source_commit',v['es_commit'])==v['es_commit'] and source.get('post_strip_es_sha256',es)==es
helper=Path('/workspace/repos/rocknix.worktrees/m7-offline-vm-567/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm')
assert sha(helper)=='5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d'
tools=[helper,helper.parent/'profile.json']+[tree/name for name in ['tools/vm-serial','tools/vm-stop','tools/watch-build','tools/watch-job','tools/watch-build-submit','tools/pixelelated-state-check-test','tools/pixelelated-state-check','docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh']]
assert sha(tools[-1])=='a49a0bb3f8b5ed937dafc7524c70e2ce9ce74e925478d421dc0f7e3a20e957da'
archive=a.adapter_archive.resolve(strict=True);assert sha(archive)==ARCHIVE;seal(HERE)
out.mkdir(mode=0o700)
for name in ['records','scan','logs','source','clean','vm','lifecycle-owner']:(out/name).mkdir()
adapter=out/'source/installed567';adapter.mkdir()
with tarfile.open(archive) as tar:
    members=tar.getmembers();assert len(members)<=64 and sum(m.size for m in members)<=1024**2
    seen=set()
    for m in members:
        name=Path(m.name);assert not name.is_absolute() and '..' not in name.parts and m.name not in seen and (m.isfile() or m.isdir());seen.add(m.name)
        dest=adapter/name
        if m.isdir():dest.mkdir(parents=True,exist_ok=True)
        else:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(tar.extractfile(m).read())
seal(adapter,SEAL)
for name in ['vm-lifecycle.py','run-guest.py','close.py','census.py']:shutil.copy2(HERE/name,out/name)
shutil.copy2(a.custody,out/'records/custody.original.json');shutil.copy2(source_path,out/'records/source-receipt.original.json')
for name in ['inputs.json','result.json']:shutil.copy2(verify/name,out/'records'/('verification-'+name))
source.update(es_source_commit=v['es_commit'],post_strip_es_sha256=es)
source['evidence']=source['evidence']+[{'path':str(verify/'result.json'),'bytes':(verify/'result.json').stat().st_size,'sha256':sha(verify/'result.json')}]
write(out/'records/source-receipt.es-bound.json',source)
write(out/'records/source-extension.json',{'original_sha256':sha(source_path),'verification_sha256':sha(verify/'result.json'),'fields_from_verifier':['es_source_commit','post_strip_es_sha256'],'reviewed_proxy_chain_unchanged':True})
config={'checkout':str(tree),'commit':commit,'es_commit':v['es_commit'],'vnc':a.vnc,'helper':str(helper),'custody':custody,
 'custody_sha256':sha(a.custody),'verification':{str(verify/name):sha(verify/name) for name in ['inputs.json','result.json']},
 'source_receipt_sha256':sha(out/'records/source-receipt.es-bound.json'),'adapter_manifest':SEAL,'adapter_archive':{'path':str(archive),'sha256':ARCHIVE},
 'tools':{str(f):sha(f) for f in tools},'code':{name:sha(out/name) for name in ['vm-lifecycle.py','run-guest.py','close.py','census.py']},
 'work_seconds':2100,'cleanup_seconds':150}
write(out/'config.json',config)
write(out/'retention-plan.json',{'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],
 'protected':[str(out/'records'),str(out/'source'),str(tree/'tools/host-maintenance'),str(image),str(system),str(root),str(verify)],'candidates':[],
 'builds':[{'name':'m7-installed567-topup','terms_bytes':{'raw_image':raw.stat().st_size,'guest_disk':16*1024**3,'media':512*1024**2,'compact_exports':256*1024**2},
 'basis':'One normal no-NIC8GiB/4CPU guest; untouched clean before fixture media; one unchanged installed success/API case.2100s work+150s fail-stop; original worker240s and command310s. Source preparation is not runtime acceptance.',
 'evidence':[{'path':str(out/name),'sha256':sha(out/name)} for name in ['config.json','vm-lifecycle.py','run-guest.py','records/source-extension.json']]}]})
write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-installed567-topup',
 'profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],
 'outputs':[{'path':str(out/'vm'),'issue':567,'kind':'qa-scratch','release_when':'Export/review original clean, fixture, worker, ES, peer, owner, monitor and stop exits; owners absent; consume admission before exact disk/media/UEFI retirement.'}]})
print(json.dumps({'status':'PREPARED_UNRUN','owner':str(out),'commit':commit,'es_commit':v['es_commit'],'adapter_manifest':SEAL}))
