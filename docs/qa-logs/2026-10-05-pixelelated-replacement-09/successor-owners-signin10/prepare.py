from pathlib import Path
import ast,hashlib,json,subprocess,datetime
prefix='/workspace/tmp/pixelelated-m7-'
names=[('signin-ui-09','signin-ui-10'),('signin-1g-09','signin-1g-10'),('signin-provider1g-01','signin-provider1g-02')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads(Path(prefix+'signin-ui-09/completion.json').read_text())['qemu_absent']
assert json.loads(Path(prefix+'signin-ui-09/visual-review.json').read_text())['passed'] is False
observer='''def finishing_state():
    code = """from pathlib import Path
import hashlib,json,time,urllib.parse
p=Path('/tmp/m7-signin-page');raw=p.read_text() if p.exists() else ''
uri=urllib.parse.unquote(raw)
kind='finishing' if uri.startswith('data:text/html,') and '<h1>Connected</h1>' in uri and 'Finishing up on your handheld' in uri else 'local-form' if urllib.parse.urlparse(raw).path=='/mobile-form' else 'other-or-missing'
log=Path('/tmp/m7-signin-log').read_text(errors='replace')
print(json.dumps({'guest_monotonic':time.monotonic(),'kind':kind,'page_sha256':hashlib.sha256(raw.encode()).hexdigest(),'done_exists':Path('/tmp/m7-signin-done').exists(),'load_finished_count':log.count('load finished'),'window_exists':Path('/proc/PID').exists()}))
""".replace('PID', str(window_pid))
    state=json.loads(guest('python3 -',input=code.encode()))
    state['host_observed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    transition_samples.append(state)
    (out/'finishing-transition.json').write_text(json.dumps(transition_samples,indent=2)+'\\n')
    return state

transition_samples=[]
'''
rows=[]
for old,new in names:
 src=Path(prefix+old);dst=Path(prefix+new);assert not dst.exists();dst.mkdir(mode=0o700)
 if old!='signin-ui-09':assert not (src/'qa.start').exists()
 for line in (src/'harness.sha256').read_text().splitlines():
  h,n=line.split(None,1);p=Path(n);assert sha(p)==h;s=p.read_text()
  for a,b in names:s=s.replace(prefix+a,prefix+b)
  (dst/p.name).write_text(s)
 if new=='signin-ui-10':
  p=dst/'signin-proof.py';s=p.read_text();needle='try:\n    check(guest(';assert s.count(needle)==1;s=s.replace(needle,observer+'\n'+needle)
  oldblock="""    guest('touch /tmp/m7-signin-done')
    time.sleep(2)
    shot('02-finishing-marker-stand-in')"""
  newblock="""    before=finishing_state()
    check(before['kind']=='local-form' and not before['done_exists'], 'finishing predicate rejects actual prior local page')
    guest('touch /tmp/m7-signin-done')
    time.sleep(2)
    old_timing=finishing_state()
    check(old_timing['done_exists'] and old_timing['window_exists'], 'actual done marker reached the running installed window')
    wait_for(lambda: finishing_state()['kind']=='finishing', 60, 'installed finishing document load completion')
    check(True, 'installed page record changed to the exact Connected/Finishing document')
    shot('02-finishing-marker-stand-in')"""
  assert s.count(oldblock)==1;s=s.replace(oldblock,newblock);p.write_text(s)
 (dst/'transition-provenance.json').write_text(json.dumps({'issue':447,'prior_owner':str(src),'old_seal_sha256':sha(src/'harness.sha256'),'scope':'Record actual prior/2second/subsequent page-kind transitions without URI values; require exact finishing document load before stable capture. Earlier zero command results/semantic rejection retained.'},indent=2)+'\n')
 subprocess.run(['python3','-I',str(dst/'prepare-dirs.py')],check=True)
 for p in dst.iterdir():
  if p.suffix=='.py':ast.parse(p.read_text())
  if p.suffix=='.sh':subprocess.run(['bash','-n',str(p)],check=True)
 files=sorted(p for p in dst.iterdir() if p.is_file());(dst/'harness.sha256').write_text(''.join(f'{sha(p)}  {p}\n' for p in files))
 for p in files+[dst/'harness.sha256']:p.chmod(0o500 if p.suffix=='.sh' else 0o400)
 rows.append({'prior':str(src),'owner':str(dst),'sealed_members':len(files),'seal_sha256':sha(dst/'harness.sha256')})
Path('/tmp/pixelelated-signin10-chain.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'issue':447,'owners':rows,'product_unchanged':True},indent=2)+'\n')
print('PASS fresh transition diagnostic and1GiB chain prepared and sealed')
