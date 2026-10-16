import collections, json, subprocess, sys, time
from pathlib import Path
root=Path(__file__).resolve().parent
head=sys.argv[1]
deadline=time.monotonic()+900
for attempt in range(1,91):
    if time.monotonic()>=deadline:
        break
    try:
        result=subprocess.run(['gh','api',f'repos/pixelelated/distribution/commits/{head}/check-runs'],capture_output=True,text=True,timeout=30)
    except subprocess.TimeoutExpired:
        (root/f'ci-recovery-timeout-{attempt:03d}.json').write_text(json.dumps({'poll_timeout_seconds':30,'head':head})+'\n')
        print('GitHub poll timed out; retained, retrying within overall deadline',flush=True)
        time.sleep(10)
        continue
    (root/f'ci-recovery-{attempt:03d}.json').write_text(result.stdout if result.returncode==0 else json.dumps({'rc':result.returncode,'stderr':result.stderr}))
    if result.returncode:
        raise SystemExit(result.returncode)
    checks=json.loads(result.stdout)['check_runs']
    if any(x['head_sha']!=head for x in checks):
        raise SystemExit('Unexpected CI source identity')
    compact=[{k:x[k] for k in ['id','name','status','conclusion']} for x in checks]
    print(json.dumps(compact),flush=True)
    counts=collections.Counter(x['name'] for x in checks)
    if counts['record']>=1 and counts['wordlist']>=2 and all(x['status']=='completed' for x in checks):
        rc=0 if all(x['conclusion']=='success' for x in checks) else 1
        (root/'ci-result.json').write_text(json.dumps({'rc':rc,'head':head,'checks':checks},indent=2)+'\n')
        raise SystemExit(rc)
    time.sleep(10)
(root/'ci-result.json').write_text(json.dumps({'rc':124,'head':head,'reason':'deadline; checks not all complete'})+'\n')
raise SystemExit(124)
