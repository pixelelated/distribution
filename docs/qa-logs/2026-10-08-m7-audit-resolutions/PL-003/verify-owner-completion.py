import sys,pathlib,json,datetime,hashlib
p=pathlib.Path(sys.argv[1]);runs=[x for x in (p/'.build-runs').iterdir() if x.is_dir()];assert len(runs)==1;r=runs[0]
rc={n:int((p/n).read_text()) for n in ['inner.rc','outer.rc','tool-wrapper.rc']};rc['build.rc']=int((r/'build.rc').read_text());assert set(rc.values())=={0},rc
pids={n:int((r/n).read_text()) for n in ['build.pid','command.pid','watcher.pid']};pids['launcher']=json.loads((p/'launcher-pid.json').read_text())['pid'];assert all(not pathlib.Path('/proc',str(v)).exists() for v in pids.values())
x={'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channels':rc,'process_ids_verified_absent':pids,'owner':str(p)}
if (p/'inputs-before.json').exists():
 a=json.loads((p/'inputs-before.json').read_text());b=json.loads((p/'inputs-after.json').read_text());assert a==b;x['inputs_unchanged']=len(a)
 if isinstance(a,list):assert all(hashlib.sha256(pathlib.Path(e['path']).read_bytes()).hexdigest()==e['sha256'] for e in a)
 if isinstance(a,dict):assert all(hashlib.sha256(pathlib.Path(k).read_bytes()).hexdigest()==v for k,v in a.items())
if (p/'artifacts/outputs.json').exists():
 out=json.loads((p/'artifacts/outputs.json').read_text());assert all(hashlib.sha256(pathlib.Path(e['path']).read_bytes()).hexdigest()==e['sha256'] for e in out['outputs']);x['outputs']=out
(p/'verified-completion.json').write_text(json.dumps(x,indent=2)+'\n');print('PASS',json.dumps(x))
