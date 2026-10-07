from pathlib import Path
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01')
(owner/'run.path').write_text(str(tree/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
    for n,h in json.loads((owner/'seal.json').read_text()).items():
        assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h
    env=dict(os.environ,DOCKER_WORK_DIR=str(tree),DOCKER_EXTRA_OPTS=f'-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git:ro -v {owner}:{owner}')
    result=subprocess.run(['make','docker-H700','COMMAND=python3 -I '+str(owner/'probe.py')],cwd=tree,env=env)
    assert result.returncode==0,result.returncode
    subprocess.run(['python3','-I','/workspace/tmp/pixelelated-m7-h700-arm-01/verify-source.py'],cwd=tree,check=True)
    rc=0
finally:
    (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
