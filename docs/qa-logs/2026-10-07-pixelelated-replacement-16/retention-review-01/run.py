from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, importlib.machinery, importlib.util, json, os, subprocess, sys, tarfile

owner=Path(__file__).resolve().parent;repo=Path.cwd()
(owner/'run.path').write_text(str(repo/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
tool=repo/'tools/host-maintenance/retention-report'
loader=importlib.machinery.SourceFileLoader('retention',str(tool));spec=importlib.util.spec_from_loader(loader.name,loader)
mod=importlib.util.module_from_spec(spec);loader.exec_module(mod)
rc=1
try:
    for path,sha in json.loads((owner/'seal.json').read_text()).items():assert mod.digest(path)==sha,path
    device=Path('/workspace/repos/rocknix.worktrees/devices')
    measured={}
    for arch in ['arm','aarch64']:
        path=device/('build.ROCKNIX-H700.'+arch)
        measured[arch]=int(subprocess.check_output(['du','-s','-B1',str(path)],text=True).split()[0])
        print('Measured H700 '+arch+' root: '+str(measured[arch])+' allocated bytes',flush=True)
    assets=[];decoded=0;system=0
    for path in sorted((device/'target').glob('ROCKNIX-H700*')):
        if path.name.endswith('.sha256'):continue
        row={'path':str(path),'identity':mod.identity(path)}
        if path.name.endswith('.gz'):
            count=0
            with gzip.open(path,'rb') as stream:
                for block in iter(lambda:stream.read(16*1024*1024),b''):count+=len(block)
            row['decoded_bytes']=count;decoded+=count
        elif path.name.endswith('.tar'):
            with tarfile.open(path) as archive:
                system+=sum(m.size for m in archive.getmembers() if m.name.endswith('/target/SYSTEM'))
        assets.append(row)
    assert len(assets)==3 and decoded>0 and system>0
    compressed=sum(x['identity']['allocated_bytes'] for x in assets)
    # Own outputs, independent stored copy, both decoded DDR images, two SYSTEM
    # extractions. Round upward and add 25% for artifact growth against old H700.
    artifact_budget=((int((2*compressed+decoded+2*system)*1.25)+2**30-1)//2**30)*2**30
    measurement=dict(utc=datetime.now(timezone.utc).isoformat(),device_tree=str(device),
        device_head=subprocess.check_output(['git','-C',str(device),'rev-parse','HEAD'],text=True).strip(),
        roots_allocated_bytes=measured,artifacts=assets,system_bytes=system,artifact_budget_bytes=artifact_budget,
        operating_allowance_bytes=100*2**30,package_growth_allowance_bytes=40*2**30,
        basis='Independent cold worktree estimated from each actual H700 cache; preserve the old device tree. '
              'Artifacts: twice actual compressed allocation, actual decompressed DDR3/DDR4 lengths and twice SYSTEM, plus 25%, rounded up to GiB. '
              '40 GiB build growth and 100 GiB operating allowances carried from candidate16 preflight; these are conservative allowances, not measured future peaks. '
              'aarch64 forecast includes retained arm root, growth and artifact budget. Remeasure after arm.')
    mp=owner/'artifacts/measurements.json';mp.write_text(json.dumps(measurement,indent=2)+'\n')
    q=repo/'docs/qa-logs/2026-10-07-pixelelated-replacement-16';replacement=q/'qa20-acceptance/acceptance.json'
    rows=json.loads((q/'qa20-preparation/completed-owned-qa-metadata.json').read_text())['rows']
    candidates=[]
    for row in rows:
        name=Path(row['owner']).name.removeprefix('pixelelated-m7-')
        if name in ['qa-19','p4-no-join-negative-02','boot-qualification-09']:continue
        manifests=list((repo/'docs/qa-logs').glob('2026-10-0[67]-pixelelated-replacement-*/'+name+'/sha256.json'))
        assert len(manifests)==1,name
        retained=manifests[0].parent
        evidence=[dict(path=str(retained/path),sha256=sha) for path,sha in json.loads(manifests[0].read_text()).items()]
        evidence.append(dict(path=str(manifests[0]),sha256=mod.digest(manifests[0])))
        for record in row['files']:
            p=Path(record['path']);assert p.exists()
            candidates.append(dict(path=str(p),owner=row['owner'],classification='superseded-qa-disk',identity=mod.identity(p),
                evidence=evidence,superseded_by=dict(path=str(replacement),sha256=mod.digest(replacement)),
                owner_receipt=str(Path(row['owner'])/'owner-verification.json'),
                cleanup_receipt=str(Path(row['owner'])/'guest-cleanup-verification.json')))
    preserved=['/workspace/artifacts','/workspace/repos','/workspace/cache/rocknix-sources',
       '/workspace/tmp/pixelelated-m7-qa-19','/workspace/tmp/pixelelated-m7-qa-20',
       '/workspace/tmp/pixelelated-m7-p4-no-join-negative-02','/workspace/tmp/pixelelated-m7-boot-qualification-09']
    assert all(Path(p).exists() for p in preserved)
    common={'package_growth':40*2**30,'artifact_and_verification':artifact_budget,'operating_allowance':100*2**30}
    builds=[]
    for arch in ['arm','aarch64']:
        terms=dict(common,independent_build=measured[arch])
        if arch=='aarch64':terms['retained_new_arm_outputs']=measured['arm']+40*2**30+artifact_budget
        builds.append(dict(name='H700 DDR4 RG35XX SP '+arch,terms_bytes=terms,
                           evidence=[dict(path=str(mp),sha256=mod.digest(mp))],basis=measurement['basis']))
    plan=dict(scan_roots=['/workspace/tmp','/workspace/artifacts','/workspace/repos/rocknix.worktrees','/workspace/cache/rocknix-sources'],
              reference_stores=['/workspace/artifacts'],volume='/workspace',protected=preserved,candidates=candidates,builds=builds)
    pp=owner/'artifacts/plan.json';pp.write_text(json.dumps(plan,indent=2)+'\n')
    print('Prepared '+str(len(candidates))+' explicit QA disk candidates; production read-only scan starting',flush=True)
    subprocess.run(['python3','-I',str(tool),'--plan',str(pp),'--output',str(owner/'artifacts/report.json')],check=True)
    rc=0
finally:
    (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
