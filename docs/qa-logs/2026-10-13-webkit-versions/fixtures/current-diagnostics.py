from pathlib import Path
import subprocess,json,shlex,hashlib,datetime
r=Path(__file__).parent;ssh=json.loads((r/'ssh-command.json').read_text());result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':[]}
try:
 with (r/'measure.py').open('rb') as f:subprocess.run(ssh+['cat > /tmp/qa-570-measure.py'],stdin=f,check=True)
 for spec in [{'name':'current-public-clean','engine':'2.54.1','url':'https://www.dropbox.com/login','seconds':120},{'name':'current-simple-sampler','engine':'2.54.1','url':'https://example.org','seconds':45,'env':{'WEBKIT_SAMPLE_MEMORY':'1','JSC_logGC':'1'}},{'name':'current-public-sampler','engine':'2.54.1','url':'https://www.dropbox.com/login','seconds':120,'env':{'WEBKIT_SAMPLE_MEMORY':'1','JSC_logGC':'1'}}]:
  name=spec['name'];print('START',name,flush=True)
  with (r/(name+'.json')).open('wb') as o,(r/(name+'.stderr')).open('wb') as e:p=subprocess.run(ssh+['python3 /tmp/qa-570-measure.py '+shlex.quote(json.dumps(spec))],stdout=o,stderr=e,timeout=seconds if False else spec['seconds']+80)
  result['cases'].append({'name':name,'rc':p.returncode});assert p.returncode==0
  j=json.loads((r/(name+'.json')).read_text());assert not j['error']
  for frame in j['frames']:
   assert frame['rc']==0
   with (r/(name+'-'+Path(frame['file']).name)).open('wb') as o:subprocess.run(ssh+['cat '+shlex.quote(frame['file'])],stdout=o,check=True)
  print('END',name,j['stop_reason'],'min_available_kib',min(x['mem']['MemAvailable'] for x in j['samples']),flush=True)
 result['rc']=0
except BaseException as e:result.update(rc=1,error=str(e));raise
finally:
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'current-diagnostics-result.json').write_text(json.dumps(result,indent=2)+'\n')
