from pathlib import Path
import tempfile,subprocess,json,hashlib,os,sys,time,threading,importlib.util,importlib.machinery
sys.path.insert(0,'/usr/bin')
import cloud_connections as c
P=Path('/storage/qa537/lead30');P.mkdir(exist_ok=True)
c.CONFIG=P/'rclone.conf';c.ACTIVE=P/'active-connection';c.LOCK=P/'lock';c.SYSTEM=P/'system.cfg';c.RCLONE='/storage/qa537/rclone-real'
(P/'files').mkdir(exist_ok=True)
c.CONFIG.write_text('[two words]\ntype = alias\nremote = '+str(P/'files')+'\n')
c.ACTIVE.write_text('missing\n');before=c.CONFIG.read_bytes()
try:c.save('new','alias',[('remote',str(P/'files'))])
except c.Refused as e:missing=str(e)
results={'dangling':{'error':missing,'unchanged':c.CONFIG.read_bytes()==before}}
c.ACTIVE.unlink()
env=dict(os.environ,RCLONE_CONFIG=str(c.CONFIG))
for name,cmd in [('unquoted','/usr/bin/cloud_setup --check two words:'),('quoted',"/usr/bin/cloud_setup --check 'two words:'")]:
 p=subprocess.run(['/bin/bash','-c',cmd],capture_output=True,text=True,env=env,timeout=15)
 results[name]={'rc':p.returncode,'stdout':p.stdout.strip()}
loader=importlib.machinery.SourceFileLoader('qa_oauth','/usr/bin/cloud_oauth');spec=importlib.util.spec_from_loader(loader.name,loader);oauth=importlib.util.module_from_spec(spec);loader.exec_module(oauth)
oauth.STATE_DIR=str(P/'oauth-state');oauth.LOG_FILE=str(P/'oauth.log')
h=oauth.SessionHolder('alias','new','QA',120)
h.session=oauth.Session('alias','new',120);h.session.attempt='lead30';h.session.gen='lead30';h.session.token='synthetic-token'
oauth.reset_state(attempt='lead30',session='lead30',status='waiting')
original=c.run;entered=threading.Event()
def delayed(args):
 entered.set();time.sleep(24)
 return original(args)
c.run=delayed
h.session.collector=threading.Thread(target=h.session._create_remote,daemon=True);h.session.collector.start();assert entered.wait(5)
# This is the real holder.end's 45-second join against two bounded 24-second calls.
t=time.monotonic();h.end()
results['shutdown']={'seconds':round(time.monotonic()-t,3),'collector_alive_at_return':h.session.collector.is_alive(),'staged_config_count':len(list(P.glob('.connection-*/rclone.conf'))),'live_config_unchanged':c.CONFIG.read_bytes()==before}
(P/'result.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2),flush=True)
