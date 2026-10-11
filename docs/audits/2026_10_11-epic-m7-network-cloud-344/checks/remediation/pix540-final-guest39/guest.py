from pathlib import Path
import subprocess,json,hashlib,os,sys,time,threading,importlib.util,importlib.machinery
sys.path.insert(0,'/usr/bin')
import cloud_connections as c
P=Path('/storage/qa537/shutdown39');P.mkdir(exist_ok=True)
loader=importlib.machinery.SourceFileLoader('qa_oauth','/usr/bin/cloud_oauth');spec=importlib.util.spec_from_loader(loader.name,loader);oauth=importlib.util.module_from_spec(spec);loader.exec_module(oauth)
original=c.run;results=[]
for mode in ['collector','http-worker']:
 root=P/mode;root.mkdir(exist_ok=True);(root/'files').mkdir(exist_ok=True)
 c.CONFIG=root/'rclone.conf';c.ACTIVE=root/'active-connection';c.LOCK=root/'lock';c.SYSTEM=root/'system.cfg';c.RCLONE='/storage/qa537/rclone-real'
 c.CONFIG.write_text('[existing]\ntype = alias\nremote = '+str(root/'files')+'\n');before=c.CONFIG.read_bytes()
 oauth.STATE_DIR=str(root/'state');oauth.LOG_FILE=str(root/'oauth.log')
 h=oauth.SessionHolder('alias','new','QA',120);h.session=oauth.Session('alias','new',120);h.session.attempt='shutdown39';h.session.gen='shutdown39';h.session.token='synthetic-token'
 oauth.reset_state(attempt='shutdown39',session='shutdown39',status='waiting')
 entered=threading.Event();calls=[]
 def delayed(args):
  calls.append(args[2:5]);entered.set();time.sleep(24);return original(args)
 c.run=delayed
 worker=threading.Thread(target=h.session._create_remote,daemon=True)
 if mode=='collector':h.session.collector=worker
 worker.start();assert entered.wait(5)
 t=time.monotonic();h.end();elapsed=time.monotonic()-t
 # Lock release can precede the last Python return; join only that unwind.
 worker.join(1)
 assert not worker.is_alive() and not list(root.glob('.connection-*'))
 assert c.CONFIG.read_bytes()==before and len(calls)==1 and elapsed<40
 results.append({'mode':mode,'seconds':round(elapsed,3),'collector_or_worker_alive':worker.is_alive(),'staged_configs':0,'live_config_unchanged':True,'bounded_calls':len(calls)})
 print(json.dumps(results[-1]),flush=True)
(P/'result.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS both normal-shutdown transaction paths',flush=True)
