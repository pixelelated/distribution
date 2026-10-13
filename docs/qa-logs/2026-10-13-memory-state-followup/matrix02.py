from ui import *
import traceback
results=[]
def identity():
 return json.loads(out("python3 - <<'P'\nfrom pathlib import Path\nimport json\nprint(json.dumps({'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'es':[int(p.name) for p in Path('/proc').glob('[0-9]*') if (p/'exe').resolve().name=='emulationstation']}))\nP"))
def keys(sequence):
 for k in sequence.split():key(k);time.sleep(.75)
def prepare(mode,d):
 remote('/usr/bin/cloud_oauth cancel; printf '+str(mode)+' > /storage/qa570trim/mode; rm -f /storage/qa570trim/probe.jsonl; systemctl restart essway.service',capture_output=True)
 time.sleep(6)
 before=identity();assert len(before['es'])==1
 keys('ret x up up up x down down down down down x x x down x')
 deadline=time.monotonic()+45
 while time.monotonic()<deadline:
  state=out('/usr/bin/cloud_oauth status').strip()
  if state=='waiting':break
  if state=='failed':raise RuntimeError('broker failed')
  time.sleep(1)
 else:raise RuntimeError('broker timeout')
 time.sleep(2);shot(d/'keyboard-choice.png');keys('down x');time.sleep(2);shot(d/'phone-qr-private.png')
 keys('down right');shot(d/'before-private.png');return before

def trial(name,mode):
 d=r/name;d.mkdir();guest='/storage/qa570trim/'+name;res={'name':name,'mode':mode};sampler=None;f=None
 try:
  before=prepare(mode,d);res['before']=before
  f=(d/'sampler.log').open('wb');sampler=subprocess.Popen(ssh+['python3 /storage/qa570trim/sampler02.py '+guest],stdout=f,stderr=f)
  time.sleep(4)
  if sampler.poll() is not None:raise RuntimeError('sampler failed before browser launch')
  remote('test -s '+guest+'/samples.jsonl',capture_output=True)
  start=time.monotonic();key('x');frames=set();guard=False
  while time.monotonic()-start<65:
   elapsed=time.monotonic()-start
   for n in [12,60]:
    if elapsed>=n and n not in frames:shot(d/('page-'+str(n)+'.png'));frames.add(n)
   if out('test -f '+guest+'/guard.json && echo guard || echo clear').strip()=='guard':guard=True;break
   if sampler.poll() is not None:raise RuntimeError('sampler stopped during measurement')
   time.sleep(2)
  res['elapsed']=time.monotonic()-start;res['guarded']=guard
  probe=json.loads(out('cat /storage/qa570trim/probe.jsonl'));res['probe']=probe
  assert probe['mode']==mode and probe['pid']==before['es'][0] and probe['pss_before_kib']>0 and probe['pss_after_kib']>0
  # No child may retain the probe mapping. Do not emit child argv/environment.
  res['probe_mapping_pids']=json.loads(out("python3 - <<'P'\nfrom pathlib import Path\nimport json\na=[]\nfor p in Path('/proc').glob('[0-9]*'):\n try:\n  if 'trim-probe.so' in (p/'maps').read_text():a.append(int(p.name))\n except OSError:pass\nprint(json.dumps(a))\nP"))
  assert res['probe_mapping_pids']==before['es']
  key('esc');time.sleep(7);shot(d/'returned.png');res['after']=identity();assert res['after']==before
  remote('cat /var/run/cloud_oauth/window.log',stdout=(d/'window-private.log').open('wb'))
  qa=[]
  for line in (d/'window-private.log').read_text(errors='replace').splitlines():
   if line.startswith('QA_JSON '):qa.append(json.loads(line[8:]))
  (d/'page-metrics.json').write_text(json.dumps(qa,indent=2)+'\n');assert any(x.get('page',{}).get('host','').endswith('dropbox.com') for x in qa)
  assert not guard
  res['rc']=0
 except BaseException as e:res.update(rc=1,error=repr(e));raise
 finally:
  if sampler:
   remote('touch '+guest+'/stop',capture_output=True)
   try:sampler.wait(timeout=10)
   except subprocess.TimeoutExpired:sampler.terminate();sampler.wait(timeout=5)
   f.close();remote('tar -czf '+guest+'.tgz -C '+guest+' .',capture_output=True)
   with (d/'guest.tgz').open('wb') as stream:remote('cat '+guest+'.tgz',stdout=stream)
   res['sampler_rc']=sampler.returncode
   if sampler.returncode!=0:res.update(rc=1,sampler_error=True)
  remote('/usr/bin/cloud_oauth cancel',capture_output=True)
  (d/'result.json').write_text(json.dumps(res,indent=2)+'\n');results.append(res);(r/'progress02.json').write_text(json.dumps(results,indent=2)+'\n')
 if res.get('sampler_error'):raise RuntimeError('sampler failed')
 print('DONE '+name+' pss delta KiB '+str(probe['pss_before_kib']-probe['pss_after_kib']),flush=True)
report={'started':time.time()}
try:
 for name,mode in [('run02-sham1',0),('run02-trim1',1),('run02-trim2',1),('run02-sham2',0)]:
  print('START '+name,flush=True);trial(name,mode)
 report.update(rc=0,cases=results)
except BaseException as e:report.update(rc=1,error=repr(e),cases=results);raise
finally:
 report['ended']=time.time();(r/'matrix02-result.json').write_text(json.dumps(report,indent=2)+'\n')
