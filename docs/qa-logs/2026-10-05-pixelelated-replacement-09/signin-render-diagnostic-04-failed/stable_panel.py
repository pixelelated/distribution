from pathlib import Path
import json,re,subprocess

def wait_stable(out,name,negative=False):
    def run(timeout):
        p=subprocess.run(['./tools/vm-visual-qa','--monitor','/tmp/rocknix-qemu-monitor-d.sock','settle','--timeout',str(timeout),'--quiet','2'],capture_output=True,text=True,timeout=timeout+15)
        ok=p.returncode==0 and re.fullmatch(r'settle: still after [0-9]+\.[0-9]+s\n?',p.stdout) is not None
        return {'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'timeout_seconds':timeout,'quiet_seconds':2,'passed':ok}
    if negative:
        r=run(0);(out/(name+'-unstable-control.json')).write_text(json.dumps(r,indent=2)+'\n')
        assert r['returncode']==0 and not r['passed'] and 'still moving at the bound' in r['stdout'],'zero-exit unsettled result must be rejected'
    r=run(30);(out/(name+'-stability.json')).write_text(json.dumps(r,indent=2)+'\n')
    assert r['passed'],'page did not reach a stable rendered surface'
