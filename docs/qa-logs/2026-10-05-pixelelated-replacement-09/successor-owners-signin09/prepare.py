from pathlib import Path
import ast,hashlib,json,subprocess,datetime
prefix='/workspace/tmp/pixelelated-m7-'
names=[('signin-ui-08','signin-ui-09'),('signin-1g-08','signin-1g-09'),('signin-1g-08','signin-provider1g-01')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads(Path(prefix+'signin-ui-08/completion.json').read_text());assert c['job_rc']==0 and c['qemu_absent']
assert not Path(prefix+'signin-1g-08/qa.start').exists()
stable='''from pathlib import Path
import json,re,subprocess

def wait_stable(out,name,negative=False):
    def run(timeout):
        p=subprocess.run(['./tools/vm-visual-qa','--monitor','/tmp/rocknix-qemu-monitor-d.sock','settle','--timeout',str(timeout),'--quiet','2'],capture_output=True,text=True,timeout=timeout+15)
        ok=p.returncode==0 and re.fullmatch(r'settle: still after [0-9]+\\.[0-9]+s\\n?',p.stdout) is not None
        return {'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'timeout_seconds':timeout,'quiet_seconds':2,'passed':ok}
    if negative:
        r=run(0);(out/(name+'-unstable-control.json')).write_text(json.dumps(r,indent=2)+'\\n')
        assert r['returncode']==0 and not r['passed'] and 'still moving at the bound' in r['stdout'],'zero-exit unsettled result must be rejected'
    r=run(30);(out/(name+'-stability.json')).write_text(json.dumps(r,indent=2)+'\\n')
    assert r['passed'],'page did not reach a stable rendered surface'
'''
rows=[]
for old,new in names:
 src=Path(prefix+old);dst=Path(prefix+new);assert not dst.exists();dst.mkdir(mode=0o700)
 for line in (src/'harness.sha256').read_text().splitlines():
  h,n=line.split(None,1);p=Path(n);assert sha(p)==h;s=p.read_text()
  s=s.replace(prefix+'signin-ui-08',prefix+'signin-ui-09').replace(prefix+'signin-1g-08',prefix+'signin-1g-09')
  if new=='signin-provider1g-01':s=s.replace(prefix+'signin-1g-09',prefix+new)
  (dst/p.name).write_text(s)
 (dst/'stable_panel.py').write_text(stable)
 if new=='signin-ui-09':
  p=dst/'signin-proof.py';s=p.read_text();s=s.replace('owner = Path(__file__).parent','from stable_panel import wait_stable\n\nowner = Path(__file__).parent');s=s.replace("def shot(name):\n    path", "def shot(name):\n    wait_stable(out,name,negative=(name=='01-local-redirect'))\n    check(True,name+' rendered surface is stable')\n    path")
  p.write_text(s)
 else:
  p=dst/'measure-1g.py';s=p.read_text().replace('owner=Path(__file__).parent;', 'from stable_panel import wait_stable\nowner=Path(__file__).parent;')
  s=s.replace("subprocess.run(['./tools/vm-visual-qa'", "wait_stable(out,'loaded');subprocess.run(['./tools/vm-visual-qa'")
  if new=='signin-provider1g-01':
   s=s.replace("'--seconds','30','--json'", "'--seconds','30','--url','https://www.dropbox.com/login','--json'")
   s=s.replace("'numerical_rss_ceiling_enforced':False", "'numerical_rss_ceiling_enforced':False,'url':'https://www.dropbox.com/login'")
   p2=dst/'run.sh';s2=p2.read_text().replace(prefix+'signin-ui-09/outer.rc',prefix+'signin-1g-09/outer.rc');p2.write_text(s2)
  p.write_text(s)
 (dst/'render-provenance.json').write_text(json.dumps({'issues':[447,362],'prior_owner':str(src),'old_seal_sha256':sha(src/'harness.sha256'),'scope':'Require bounded stable compositor result, retain actual zero-exit unsettled negative control, unchanged product/functional assertions; separate simple-page and public-provider1GiB owners.'},indent=2)+'\n')
 subprocess.run(['python3','-I',str(dst/'prepare-dirs.py')],check=True)
 for p in dst.iterdir():
  if p.suffix=='.py':ast.parse(p.read_text())
  if p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
 files=sorted(p for p in dst.iterdir() if p.is_file());(dst/'harness.sha256').write_text(''.join(f'{sha(p)}  {p}\n' for p in files))
 for p in files+[dst/'harness.sha256']:p.chmod(0o500 if p.suffix=='.sh' else 0o400)
 rows.append({'prior':str(src),'owner':str(dst),'sealed_members':len(files),'seal_sha256':sha(dst/'harness.sha256')})
Path('/tmp/pixelelated-signin09-chain.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'issues':[447,362],'owners':rows,'product_unchanged':True},indent=2)+'\n')
print('PASS fresh sealed sign-in and two1GiB owners with required stable rendered frames')
