from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
repo=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
feature=Path('/home/max/Development/emulationstation-next.worktrees/m7-audit-remediation')
integration=feature.with_name('qa-integration')
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
base='8beab9090c73ccc47da49f29f31fa73584fc0877'
files={'es-app/src/guis/GuiMenu.cpp': 'f37e239656b25dbb3ebaacbb74c37a4d4e97d1198c1072a9cafe42d3d03a2586', 'locale/lang/fr/LC_MESSAGES/emulationstation2.po': '9384ea95ee7b57594ed31e49caac7aad61bf888eb843ab27589b95f1d2701268'}
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],text=True).strip()
def run(label,path,args):
    with (owner/(label+'.log')).open('x') as f:r=subprocess.run(args,cwd=path,stdout=f,stderr=subprocess.STDOUT)
    assert r.returncode==0,label
    print('PASS '+label,flush=True)
rc=1
try:
    for p,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
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
    assert git(feature,'branch','--show-current')=='feature/m7-audit-remediation'
    assert git(integration,'branch','--show-current')=='test/qa-integration'
    assert git(feature,'rev-parse','HEAD')==git(integration,'rev-parse','HEAD')==base
    assert not git(integration,'status','--porcelain')
    assert git(feature,'diff','--name-only').splitlines()==list(files)
    assert not git(feature,'diff','--cached','--name-only')
    for p,h in files.items():assert hashlib.sha256((feature/p).read_bytes()).hexdigest()==h
    proof=Path('/workspace/tmp/pixelelated-m7-p4-interruption-copy-host-03')
    assert set(json.loads((proof/'owner-verification.json').read_text())['channels'].values())=={'0'}
    assert (proof/'artifacts/fr.mo').stat().st_size>0
    for rel,h in files.items():assert json.loads((proof/'provenance.json').read_text())['source_sha256'][str(feature/rel)]==h
    run('diff-check',feature,['git','diff','--check'])
    subprocess.run(['git','-C',str(feature),'add','--',*files],check=True)
    run('commit',feature,['git','commit','-F',str(owner/'message.txt')])
    commit=git(feature,'rev-parse','HEAD')
    run('integration',integration,['git','merge','--ff-only',commit])
    for label,path,branch in [('feature',feature,'feature/m7-audit-remediation'),('integration',integration,'test/qa-integration')]:
        assert git(path,'rev-parse','HEAD')==commit and not git(path,'status','--porcelain')
        run(label+'-push',path,['git','push','origin',commit+':refs/heads/'+branch])
        assert git(path,'ls-remote','origin','refs/heads/'+branch).split()[0]==commit
        for p,h in files.items():assert hashlib.sha256((path/p).read_bytes()).hexdigest()==h
    receipt=dict(verified_utc=datetime.now(timezone.utc).isoformat(),commit=commit,source_sha256=files,source_checks='Exact-byte interruption-copy-host03 image compiler,164 vocabulary strings, msgfmt and diff checks pass. Refused01/failed02 retained.',normal_hooks=True,remote_refs_verified=True,scope='Owner-requested English/French interruption guidance and retry prompt; actions unchanged. Actual rebuilt640/1280 visual and retry acceptance remains required under#482.')
    (owner/'publication.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True);rc=0
finally:
    (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
