import hashlib,json,os,pathlib,subprocess,time
out=pathlib.Path('/tmp/pixelelated-host-rollout-20261004')
log=out/'busy.log'; rc=out/'busy.rc'; status=out/'busy.status'
assert not rc.exists()
log.write_text('owned busy guard probe started\n')
child=subprocess.Popen(['/usr/bin/python3','-I','-c','import time; time.sleep(18)'])
watch=subprocess.Popen(['tools/watch-job','--log',str(log),'--rc',str(rc),'--pid',str(child.pid),'--status',str(status),'--interval','1','--stall-min','1'],stdout=(out/'watch.out').open('w'),stderr=(out/'watch.err').open('w'))
try:
 for _ in range(30):
  if status.exists(): break
  time.sleep(.1)
 assert status.exists() and watch.poll() is None
 before=pathlib.Path('/proc/swaps').read_text(); (out/'swaps-before-busy.txt').write_text(before)
 env=os.environ.copy(); env['PYTHONPATH']=str(out/'hostile'); env['PYTHONSTARTUP']=str(out/'must-not-run.py')
 hostile=out/'hostile'; hostile.mkdir(exist_ok=True)
 (hostile/'sitecustomize.py').write_text("raise RuntimeError('caller Python path was imported')\n")
 checks=[]
 for name,args in [('busy',['/usr/local/sbin/pixelelated-reclaim-swap','--reclaim']),('extra-argument',['/usr/local/sbin/pixelelated-reclaim-swap','--reclaim','--extra']),('unrelated',['/usr/bin/true'])]:
  started=time.monotonic()
  r=subprocess.run(['/usr/bin/sudo','-n','-k','--']+args,env=env,text=True,capture_output=True,timeout=8)
  (out/(name+'.txt')).write_text(r.stdout+r.stderr)
  checks.append({'name':name,'rc':r.returncode,'seconds':round(time.monotonic()-started,3),'output':r.stdout+r.stderr})
  assert r.returncode!=0,name
  if name=='busy': assert 'REFUSED: active build, compiler, watcher or VM: PID '+str(watch.pid) in r.stderr,r.stderr
  else: assert 'REFUSED:' not in r.stderr,r.stderr
 after=pathlib.Path('/proc/swaps').read_text(); (out/'swaps-after-busy.txt').write_text(after)
 assert before.splitlines()[1].split()[:3]==after.splitlines()[1].split()[:3]
 assert 'Reclaiming' not in (out/'busy.txt').read_text()
 (out/'busy-proof.json').write_text(json.dumps({'observed_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'job_pid':child.pid,'watch_pid':watch.pid,'checks':checks},indent=2)+'\n')
 print(json.dumps(checks,indent=2),flush=True)
finally:
 child.wait(timeout=25)
 log.write_text('owned busy guard probe completed\n'); rc.write_text('0\n')
 watch.wait(timeout=8)
 print('Owned job and watcher exited',flush=True)
