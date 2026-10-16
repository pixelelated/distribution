import os,json,time,subprocess,urllib.request,urllib.parse,hashlib
from pathlib import Path
R=Path('/storage/qa587'); action=(R/'proxy-action').read_text().strip()
def call(args):
 begin=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,timeout=40)
 row={'action':action,'argv':args,'rc':p.returncode,'elapsed':time.monotonic()-begin,'stdout':p.stdout,'stderr':p.stderr}
 with (R/'proxy-control.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 assert p.returncode==0,(args,p.returncode,p.stderr)
 return row
if action in ['start','stop']:
 result=call(['systemctl',action,'raofflineproxy.service'])
 properties=call(['systemctl','show','raofflineproxy.service','-p','MainPID','-p','ActiveState','-p','SubState','-p','Result','-p','ExecMainCode','-p','ExecMainStatus'])
 assert 'Result=success' in properties['stdout']
 if action=='stop':assert 'MainPID=0' in properties['stdout'] and 'ActiveState=inactive' in properties['stdout']
 print(json.dumps({'action':action,'elapsed':result['elapsed'],'unit':properties['stdout']}))
else:
 os.environ['RAOFFLINEPROXY_CONFIG_DIR']='/storage/.config/raofflineproxy'
 from raofflineproxy import storage,flusher
 def post(**args):
  begin=time.monotonic();req=urllib.request.Request('http://127.0.0.1:8080/dorequest.php',data=urllib.parse.urlencode(args).encode())
  with urllib.request.urlopen(req,timeout=5) as res:assert res.status==200;v=json.load(res)
  with (R/'protocol.jsonl').open('a') as f:f.write(json.dumps({'action':args['r'],'elapsed':time.monotonic()-begin,'success':v.get('Success'),'error':v.get('Error')})+'\n')
  return v
 for who in ['fixture','alternate']:
  v=post(r='login2',u=who,t='fixture-only');assert v['Success'] is True and v['User']==who and v['Token']=='fixture-only'
  assert post(r='patch',g=20,u=who)['PatchData']['ID']==20
 if action=='queue':
  for who,game,aid in [('fixture',10,101),('alternate',20,201),('fixture',10,101)]:
   v=post(r='awardachievement',u=who,t='fixture-only',g=game,a=aid,h=0);assert v.get('Error')=='queued_offline',v
 s=storage.Storage();pending=s.get_pending_awards();assert len(pending)==2 and flusher.verify_chain(pending)[0]
 assert s._connection.execute('PRAGMA integrity_check').fetchone()[0]=='ok';s.close()
 if action=='queue':(R/'expected-pending.json').write_text(json.dumps(pending,sort_keys=True)+'\n')
 else:assert pending==json.loads((R/'expected-pending.json').read_text())
 for who,game,ids in [('fixture',10,[101]),('fixture',20,[]),('alternate',10,[]),('alternate',20,[201])]:
  v=post(r='startsession',u=who,g=game);assert [x['ID'] for x in v['Unlocks']]==ids,v
 print(json.dumps({'action':action,'signed_pending':len(pending),'integrity':'ok','cached_login_patch_session':'PASS','account_separation':'PASS','pending_sha256':hashlib.sha256(json.dumps(pending,sort_keys=True).encode()).hexdigest()}))
