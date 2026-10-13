from ui import *
import traceback
r=Path(__file__).parent
agents={
 'handset':'',
 'desktop':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/60.5 Safari/605.1.15',
 'ipad':'Mozilla/5.0 (iPad; CPU OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
 'android':'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'}
(r/'agents.json').write_text(json.dumps(agents,indent=2)+'\n')
results=[]
def identity():
 return json.loads(out("python3 - <<'P'\nfrom pathlib import Path\nimport json\nprint(json.dumps({'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'es':[int(p.name) for p in Path('/proc').glob('[0-9]*') if (p/'exe').resolve().name=='emulationstation']}))\nP"))
def trial(name,agent,width):
 d=r/name;d.mkdir();guest='/storage/qa570ua/'+name;before=identity();res={'name':name,'agent':agent,'requested_width':width,'before':before};sampler=None
 try:
  remote('cat > /storage/qa570ua/ua.txt',input=agents[agent].encode(),capture_output=True)
  remote('cat > /storage/qa570ua/width.txt',input=str(width).encode(),capture_output=True)
  f=(d/'sampler.log').open('wb');sampler=subprocess.Popen(ssh+['python3 /storage/qa570/sampler.py '+guest],stdout=f,stderr=f)
  time.sleep(5);shot(d/'before.png');start=time.monotonic();key('x');frames=set();guard=False
  while time.monotonic()-start<65:
   t=time.monotonic()-start
   for n in [12,60]:
    if t>=n and n not in frames:shot(d/('page-'+str(n)+'.png'));frames.add(n)
   if out('test -f '+guest+'/guard.json && echo guard || echo clear').strip()=='guard':guard=True;break
   time.sleep(2)
  res['elapsed']=time.monotonic()-start;res['guarded']=guard
  key('esc');time.sleep(7);shot(d/'returned.png')
  remote('cat /var/run/cloud_oauth/window.log',stdout=(d/'window.log').open('wb'))
  key('x');time.sleep(2);shot(d/'ready.png');res['after']=identity();assert before==res['after'] and before['es']
  metrics=[json.loads(l[8:]) for l in (d/'window.log').read_text().splitlines() if l.startswith('QA_JSON ')];assert metrics,'missing metrics'
  page=metrics[-1]['page'];res['viewport']={k:page[k] for k in ['width','height','dpr','screenWidth','screenHeight','small','tablet']};assert abs(page['width']-width)<=1, res['viewport']
  res['rc']=0
 except BaseException as e:res.update(rc=1,error=repr(e));raise
 finally:
  if sampler:
   remote('touch '+guest+'/stop',capture_output=True)
   try:sampler.wait(timeout=10)
   except subprocess.TimeoutExpired:sampler.terminate();sampler.wait(timeout=5)
   f.close();remote('tar -czf '+guest+'.tgz -C '+guest+' .',capture_output=True)
   with (d/'guest.tgz').open('wb') as f:remote('cat '+guest+'.tgz',stdout=f)
  (d/'result.json').write_text(json.dumps(res,indent=2)+'\n');results.append(res);(r/'progress.json').write_text(json.dumps(results,indent=2)+'\n')
 print('DONE '+name,flush=True)
result={'started':time.time()}
try:
 for n,a,w in [('desktop360','desktop',360),('handset768','handset',768),('desktop480','desktop',480),('handset640','handset',640),('desktop640','desktop',640),('handset480','handset',480),('desktop768','desktop',768),('handset360','handset',360)]:
  print('START '+n,flush=True);trial(n,a,w)
 result.update(rc=0,cases=results)
except BaseException as e:result.update(rc=1,error=repr(e),cases=results);raise
finally:
 remote('/usr/bin/cloud_oauth cancel',capture_output=True)
 result['ended']=time.time();(r/'matrix-result.json').write_text(json.dumps(result,indent=2)+'\n')
