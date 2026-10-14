#!/usr/bin/env python3
"""UNRUN preparation of one retained20->candidate owner; no artifact reader or guest launch."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE_SHA='1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,value):p.write_text(json.dumps(value,indent=2)+'\n')
p=argparse.ArgumentParser(description=__doc__)
for key in ['checkout','baseline','verification','owner']:p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--expected-commit',required=True);p.add_argument('--id',required=True);p.add_argument('--vnc',type=int,required=True)
a=p.parse_args();tree=a.checkout.resolve(strict=True);out=a.owner.absolute();verify=a.verification.resolve(strict=True)
assert out.parent==Path('/workspace/tmp') and re.fullmatch('pix[A-Za-z0-9_-]+',out.name) and not out.exists()
assert re.fullmatch('[a-z0-9][a-z0-9-]{0,47}',a.id) and re.fullmatch('[0-9a-f]{40}',a.expected_commit) and 100<=a.vnc<=199
assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()==a.expected_commit
v=json.loads((verify/'result.json').read_text());i=json.loads((verify/'inputs.json').read_text())
assert v['status']=='PASS' and v['source']==i['source']==a.expected_commit and v['es_commit']==i['es_commit']
updates=[(Path(k),row) for k,row in i['artifacts'].items() if k.endswith('.tar')];assert len(updates)==1
update,ur=updates[0];update=update.resolve(strict=True);baseline=a.baseline.resolve(strict=True);system=verify/'SYSTEM'
assert baseline.is_file() and baseline.stat().st_size==2073682425 and not a.baseline.is_symlink()
assert update.is_file() and update.stat().st_size==ur['bytes'] and re.fullmatch('[A-Za-z0-9_.+-]+\.tar',update.name)
assert re.fullmatch('/[A-Za-z0-9_./+-]+',str(update)), 'debugfs input path must be unambiguous'
assert system.is_file() and system.stat().st_size==v['payload']['SYSTEM']['bytes']
helper=Path('/workspace/repos/rocknix.worktrees/m7-offline-vm-567/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm')
assert sha(helper)=='5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d'
parent=tree/'docs/qa-logs/2026-10-14-m7-installed-state-plan/retained-fixture'
assert sha(parent/'SHA256SUMS')=='f57c6a11bcc6daa98a7d3b2249a7deeb366afb44df5c44bcb0c0ead086ab3100'
for line in (parent/'SHA256SUMS').read_text().splitlines():
    digest,name=line.split('  ',1);assert sha(parent/name)==digest
correction=tree/'docs/qa-logs/2026-10-14-installed-state-correction/source-originals.tar.gz'
assert sha(correction)=='5e1255cbf9d22d1b2f0ff7b128be9f657d82be2d6e38870fccc284d7bc4111dd'
for line in (HERE/'SHA256SUMS').read_text().splitlines():
    digest,name=line.split('  ',1);assert sha(HERE/name)==digest
out.mkdir(mode=0o700)
for name in ['records','scan','logs','source','phases','guest','vm','reader-scratch','lifecycle-owner']:(out/name).mkdir()
for phase in ['seed','before','after','backup']:(out/'phases'/phase).mkdir()
for name in ['vm-lifecycle.py','close.py','census.py']:shutil.copy2(HERE/name,out/name)
shutil.copytree(parent,out/'source/retained-original');shutil.copy2(correction,out/'source/correction.tar.gz')
shutil.copy2(verify/'result.json',out/'records/image-verification.json');shutil.copy2(verify/'inputs.json',out/'records/image-inputs.json')
tools=[helper,helper.parent/'profile.json']+[tree/name for name in ['tools/vm-serial','tools/vm-stop','tools/watch-build','tools/watch-job','tools/watch-build-submit']]
media=((ur['bytes']+128*1024**2+1024**2-1)//(1024**2))*1024**2
config={'checkout':str(tree),'commit':a.expected_commit,'es_commit':v['es_commit'],'id':a.id,'vnc':a.vnc,'helper':str(helper),
 'baseline':{'path':str(baseline),'bytes':baseline.stat().st_size,'sha256':BASE_SHA},
 'update':{'path':str(update),**ur},'system':{'path':str(system),**v['payload']['SYSTEM']},
 'verification':{str(verify/name):sha(verify/name) for name in ['inputs.json','result.json']},
 'tools':{str(path):sha(path) for path in tools},'code':{name:sha(out/name) for name in ['vm-lifecycle.py','close.py','census.py']},
 'work_seconds':4200,'cleanup_seconds':180,'input_media_bytes':media,
 'guest_update_free_bytes':ur['bytes']+v['payload']['SYSTEM']['bytes']+v['payload']['KERNEL']['bytes']+1024**3}
write(out/'config.json',config)
write(out/'retention-plan.json',{'volume':'/workspace','scan_roots':[str(out/'scan')],'reference_stores':[],
 'protected':[str(out/'records'),str(out/'source'),str(tree/'tools/host-maintenance'),str(baseline),str(update),str(system),str(verify)],'candidates':[],
 'builds':[{'name':'m7-retained20-update-backup','terms_bytes':{'baseline_raw_ceiling':16*1024**3,'guest_disk':16*1024**3,'update_input_media':media,'fixture_backup_and_reader_scratch':1024**3},
 'basis':'One fresh accepted20 no-NIC 4CPU/8GiB guest; unchanged real update then corrected installed backup. 4200s work +180s cleanup; original phase bounds retained. Raw maximum16GiB, disk16GiB, dynamically sized read-only update medium; no new acceptance criteria.',
 'evidence':[{'path':str(out/name),'sha256':sha(out/name)} for name in ['config.json','vm-lifecycle.py','close.py','records/image-verification.json']]}]})
write(out/'admission-plan.json',{'checkout':str(tree),'retention_plan':str(out/'retention-plan.json'),'retention_report':str(out/'retention-report.json'),'stage':'m7-retained20-update-backup',
 'profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],
 'outputs':[{'path':str(out/'vm'),'issue':565,'kind':'qa-scratch','release_when':'Export and review original four phases/backup-child/update/host exits; actual owners absent; consume admission before retiring exact disk/input media/UEFI and private synthetic state.'}]})
print(json.dumps({'status':'PREPARED_UNRUN','owner':str(out),'work_seconds':4200,'cleanup_seconds':180}))
