from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
root=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
op=root/'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/second-opinions'
assert Path.cwd()==root
assert not (owner/'qa.start').exists()
(owner/'qa.start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
(owner/'run.path').write_text(str(root/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
    seal=json.loads((owner/'seal.json').read_text())
    for path,digest in seal.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
    subprocess.run(['git','diff','--quiet','7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2','--','projects','packages','distributions','config'],check=True)
    for command in ['verify-pins','efforts','drift']:
        with (owner/'activity'/('preflight-'+command+'.log')).open('xb',buffering=0) as log:
            subprocess.run([str(root/'tools/council/run'),command],stdout=log,stderr=subprocess.STDOUT,check=True)
    assert not (op/'claude-blind.md').exists()
    (owner/'provider.start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
    with (owner/'activity/facilitator.log').open('xb',buffering=0) as log:
        rc=subprocess.run([str(root/'tools/council/run'),'invoke','--member','claude','--provider','openrouter','--prompt-file',str(op/'claude-blind-brief.md'),'--output',str(op/'claude-blind.md')],stdout=log,stderr=subprocess.STDOUT).returncode
    (owner/'provider.rc').write_text(str(rc)+'\n')
    for path,digest in seal.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
except BaseException:
    rc=1
    raise
finally:
    (owner/'inner.rc').write_text(str(rc)+'\n')
    (owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
