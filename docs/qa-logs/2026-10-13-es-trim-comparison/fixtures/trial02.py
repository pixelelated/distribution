from ui import *
import hashlib,shlex,tarfile,io
name=sys.argv[1];mode=sys.argv[2];assert mode in ['baseline','candidate'];d=r/name;d.mkdir(exist_ok=False);guest='/storage/qa570compare/'+name;res={'name':name,'mode':mode,'rc':1,'started':time.time()};sampler=None;stream=None;opened=False

def identity():
 c="from pathlib import Path; import json,hashlib; p=next(p for p in Path('/proc').glob('[0-9]*') if (p/'exe').resolve().name in ['emulationstation','baseline','candidate']); print(json.dumps({'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'pid':int(p.name),'start':(p/'stat').read_text().rsplit(')',1)[1].split()[19],'sha256':hashlib.file_digest((p/'exe').open('rb'),'sha256').hexdigest()}))"
 return json.loads(out('python3 -c '+shlex.quote(c)))
def wait_idle():
 deadline=time.monotonic()+45
 while time.monotonic()<deadline:
  p=subprocess.run(ssh+['curl -fsS http://127.0.0.1:1234/isIdle'],capture_output=True,text=True,timeout=5)
  if p.returncode==0 and json.loads(p.stdout)==[True]:return
  time.sleep(.5)
 raise RuntimeError('frontend not idle')
def keys(seq):
 for k in seq.split():key(k);time.sleep(.75)
try:
 remote('/usr/bin/cloud_oauth cancel; systemctl stop essway.service',capture_output=True)
 # Only this disposable guest owns these mounts. Never modify baseline/candidate files while mapped.
 with (r/'clear-owned-mounts.py').open('rb') as f:remote('python3 -',stdin=f,stdout=(d/'mount-cleanup.json').open('w'))
 remote('mount --bind /storage/qa570compare/'+mode+' /usr/bin/emulationstation; mount --make-private /usr/bin/emulationstation; systemctl start essway.service',capture_output=True)
 wait_idle();res['before']=identity();assert res['before']['boot']==json.loads((r/'setup-result.json').read_text())['boot']
 assert res['before']['sha256']==json.loads((r/'setup-result.json').read_text())['hashes']['/storage/qa570compare/'+mode]
 shot(d/'initial.png');keys('shift ret x up up up x down down down down down x x x down x')
 deadline=time.monotonic()+45
 while time.monotonic()<deadline:
  state=out('/usr/bin/cloud_oauth status').strip()
  if state=='waiting':break
  if state=='failed':raise RuntimeError('authorization broker failed')
  time.sleep(1)
 else:raise RuntimeError('authorization broker timeout')
 # Pause for actual model review of keyboard choice before sending the next UI input.
 time.sleep(2);shot(d/'keyboard-choice.png');print('REVIEW keyboard choice '+name,flush=True)
 deadline=time.monotonic()+180
 while not (d/'choice-reviewed').exists():
  if time.monotonic()>deadline:raise RuntimeError('keyboard review deadline')
  time.sleep(.5)
 keys('down x');time.sleep(2);keys('down right');shot(d/'continue-private.png')
 stream=(d/'sampler.log').open('wb');sampler=subprocess.Popen(ssh+['python3 /storage/qa570compare/sampler.py '+guest],stdout=stream,stderr=stream)
 time.sleep(3);assert sampler.poll() is None,'sampler failed before launch';remote('test -s '+guest+'/samples.jsonl',capture_output=True)
 res['launch_wall_ms']=time.time()*1000;key('x');opened=True;start=time.monotonic();frames=set();page_hosts=[]
 while time.monotonic()-start<60:
  elapsed=time.monotonic()-start
  if out('test -f '+guest+'/guard.json && echo guard || echo clear').strip()=='guard':raise RuntimeError('memory guard tripped')
  assert sampler.poll() is None,'sampler died'
  for n in [12,55]:
   if elapsed>=n and n not in frames:shot(d/('page-'+str(n)+'.png'));frames.add(n)
  time.sleep(1)
 res['elapsed']=time.monotonic()-start
 res['during']=identity();assert res['during']==res['before']
 key('esc');opened=False;time.sleep(3);wait_idle();shot(d/'returned-private.png');res['after']=identity();assert res['after']==res['before']
 assert not out('pidof cloud-signin-window || true').strip(),'browser persists after normal return'
 res.update(rc=0,guarded=False);print('COMPLETE '+name+' same frontend and boot; review provider/return frames',flush=True)
except BaseException as e:res.update(rc=1,error=repr(e));raise
finally:
 if opened:
  try:remote('/usr/bin/cloud_oauth close',capture_output=True)
  except BaseException:pass
 if sampler:
  try:
   remote('touch '+guest+'/stop',capture_output=True);sampler.wait(timeout=10)
  except BaseException:
   if sampler.poll() is None:sampler.terminate();sampler.wait(timeout=5)
  stream.close();res['sampler_rc']=sampler.returncode
  if sampler.returncode:res['rc']=1
  remote('tar -czf '+guest+'.tgz -C '+guest+' .',capture_output=True)
  with (d/'guest.tgz').open('wb') as f:remote('cat '+guest+'.tgz',stdout=f)
 remote('/usr/bin/cloud_oauth cancel',capture_output=True)
 res['ended']=time.time();(d/'result.json').write_text(json.dumps(res,indent=2)+'\n')
raise SystemExit(res['rc'])
