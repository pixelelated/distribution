"""Preserve #494 compact custody and source inputs; never remove a build tree."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,stat,subprocess,time,zipfile
owner=Path(__file__).resolve().parent
review=Path('/workspace/tmp/pixelelated-m7-device-retention-review-01')
store=Path('/workspace/artifacts/pixelelated-build-custody/issue-494-device-capacity-01')
root=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01/build.pixelelated-H700.arm')
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def capacity():
    allocated=int(subprocess.check_output(['du','-sx','--block-size=1',str(root)],text=True).split()[0])
    required=158*1024**3+max(0,30044336128-allocated)
    fs=os.statvfs('/workspace');available=fs.f_bavail*fs.f_frsize
    assert available>=required+512*1024**2,(available,required)
    return {'available':available,'remaining_arm_budget':required,'preservation_ceiling':512*1024**2}
assert json.loads((review/'owner-verification.json').read_text())['result']=='PASS'
report=json.loads((review/'artifacts/report.json').read_text())
objects=json.loads((review/'artifacts/objects.json').read_text())
assert report['new_unique_copy_bytes']==sum(v['bytes'] for v in objects.values() if not v['verified_prior_object'])
before=capacity();store.mkdir();(store/'objects').mkdir();(store/'manifests').mkdir()
retained={};copied=0;tick=time.monotonic()
for sha,item in objects.items():
    src=Path(item['source']);assert identity(src)==item['source_identity']
    dest=Path(item['verified_prior_object']) if item['verified_prior_object'] else store/'objects'/sha
    if not item['verified_prior_object']:
        assert not dest.exists();shutil.copyfile(src,dest);os.chmod(dest,0o444);copied+=item['bytes']
    assert digest(dest)==sha and digest(src)==sha
    assert identity(src)==item['source_identity']
    assert identity(src)[:2]!=identity(dest)[:2]
    retained[sha]={'object':str(dest),'bytes':item['bytes'],'independent_inode':True}
    if time.monotonic()-tick>10:print('Verified custody objects',len(retained),'/',len(objects),flush=True);tick=time.monotonic()
(store/'objects.json').write_text(json.dumps(retained,indent=2)+'\n')
trees=[]
for row in report['trees']:
    tree=Path(row['tree']);number=tree.name[-2:];p=Path(row['custody_plan'])
    assert digest(p)==row['custody_plan_sha256']
    plan=json.loads(p.read_text())
    assert subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()==row['head']
    for entry in plan['entries']:
        source=tree/entry['path'];s=source.lstat()
        assert stat.S_IMODE(s.st_mode)==entry['mode'] and s.st_mtime_ns==entry['mtime_ns']
        if entry['kind']=='file':
            assert digest(source)==entry['sha256'] and s.st_size==entry['bytes']
            dest=Path(retained[entry['sha256']]['object']);assert (s.st_dev,s.st_ino)!=(dest.stat().st_dev,dest.stat().st_ino)
        elif entry['kind']=='symlink':assert source.is_symlink() and os.readlink(source)==entry['target']
        else:assert source.is_dir()
    shutil.copy2(p,store/'manifests'/p.name)
    shutil.copy2(review/'artifacts'/(number+'-tracked.diff'),store/'manifests'/(number+'-tracked.diff'))
    inputs=Path('/workspace/tmp/pixelelated-m7-replacement-'+number)/'inputs.json'
    assert digest(inputs)==row['inputs_sha256'];shutil.copy2(inputs,store/'manifests'/(number+'-inputs.json'))
    output=store/('source-inventory-'+number+'.json')
    subprocess.run(['python3','-I',str(owner/'source-inventory.py'),str(tree),str(inputs),str(output)],check=True)
    inventory=json.loads(output.read_text());assert not inventory['errors']
    recovered=Path('/workspace/artifacts/pixelelated-build-inputs/m7-cold-01-consumed/0d5570db7b689e96fb5e3d33293a5275e92d6df244acbcb8a1db1929bc3f491b/rclone-v1.75.1-linux-amd64.zip')
    assert digest(recovered)=='982b5aa772841168f8e380f139e9e787b2a105403e32b94da8676a0e1c0a13ab'
    rec=next(r for r in inventory['records'] if r['package']=='rclone')
    with zipfile.ZipFile(recovered) as z:
        content=z.read('rclone-v1.75.1-linux-amd64/rclone')
    assert hashlib.sha256(content).hexdigest()==rec['unpacked_binary_sha256']
    rec['archive_retention']={'path':str(recovered),'sha256':digest(recovered),'member_matches_unpacked_binary':True}
    output.write_text(json.dumps(inventory,indent=2,sort_keys=True)+'\n')
    trees.append({'tree':str(tree),'head':row['head'],'custody_entries':len(plan['entries']),'manifest_sha256':digest(store/'manifests'/p.name),'source_inventory':str(output),'source_inventory_sha256':digest(output),'source_roots':len(inventory['records']),'source_errors':len(inventory['errors'])})
    print('PASS preserved and qualified source inventory',number,flush=True)
allocated=int(subprocess.check_output(['du','-sx','--block-size=1',str(store)],text=True).split()[0])
assert allocated<512*1024**2
result={'utc':datetime.now(timezone.utc).isoformat(),'result':'PRESERVED','store':str(store),'trees':trees,'unique_objects':len(objects),'new_content_bytes':copied,'new_store_allocated_bytes':allocated,'gross_candidate_bytes':report['gross_allocated_bytes'],'estimated_net_recovery_bytes':report['gross_allocated_bytes']-allocated,'capacity_before':before,'deleted_files':0,'remaining':'Fresh full backing/reference/container/root-process dependency review and exact deletion approval; no removal authorized by this receipt.'}
(owner/'artifacts/result.json').write_text(json.dumps(result,indent=2)+'\n');(store/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='trees'}),flush=True)
