from pathlib import Path
import subprocess,os,json,time,shlex,sys
r=Path(__file__).parent
ssh=['ssh','-i',str(r/'qa-key'),'-p','10570','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(r/'known_hosts'),'root@127.0.0.1']
# Submitted only after consuming matrix completion; never change a live experiment.
assert json.loads((r/'matrix-owner/launcher-result.json').read_text())['runner_returncode']==0
for name,dest in [('gst-probe','/tmp/gst-probe'),('gst-plugin-scanner','/tmp/gst-plugin-scanner'),('libgstcontroller-1.0.so.0.2902.0','/tmp/qa-gst/libgstcontroller-1.0.so.0')]:
 with (r/name).open('rb') as f:subprocess.run(ssh+['mkdir -p /tmp/qa-gst && cat > '+dest+' && chmod 700 '+dest],stdin=f,check=True)
controls=[]
for name,env in [('missing',{'GST_REGISTRY':'/tmp/gst-original-registry.bin'}),('supplied',{'GST_REGISTRY':'/tmp/gst-supplied-registry.bin','GST_PLUGIN_SCANNER':'/tmp/gst-plugin-scanner','LD_LIBRARY_PATH':'/tmp/qa-gst'})]:
 cmd='env '+' '.join(k+'='+shlex.quote(v) for k,v in env.items())+' /tmp/gst-probe'
 p=subprocess.run(ssh+[cmd],capture_output=True,text=True,timeout=30)
 x=dict(case=name,rc=p.returncode,stdout=p.stdout,stderr=p.stderr);controls.append(x);print(name,p.returncode,p.stdout.strip(),flush=True)
(r/'gst-controls.json').write_text(json.dumps(controls,indent=2))
assert controls[0]['rc']==1 and controls[1]['rc']==0,controls
case='public-gst-supplied';spec=json.dumps([case,'/usr/bin/cloud-signin-window','https://www.dropbox.com/login',150,{'GST_REGISTRY':'/tmp/gst-browser-registry.bin','GST_PLUGIN_SCANNER':'/tmp/gst-plugin-scanner','LD_LIBRARY_PATH':'/tmp/qa-gst'}])
print('START '+case,flush=True)
with (r/(case+'.json')).open('wb') as out,(r/(case+'.stderr')).open('wb') as err:
 p=subprocess.run(ssh+['python3 /tmp/pressure-measure.py '+shlex.quote(spec)],stdout=out,stderr=err,timeout=210)
(r/'gst-browser-result.json').write_text(json.dumps({'rc':p.returncode}));assert p.returncode==0
x=json.loads((r/(case+'.json')).read_text())
for f in x['frames']:
 with (r/(case+'-'+Path(f['file']).name)).open('wb') as out:subprocess.run(ssh+['cat '+shlex.quote(f['file'])],stdout=out,check=True)
print('GST COMPARISON COMPLETE',flush=True)
