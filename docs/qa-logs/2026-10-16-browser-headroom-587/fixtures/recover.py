import subprocess,json,time,os
from pathlib import Path
R=Path('/storage/qa587');(R/'peer-mode').write_text('fast\n');start=time.monotonic()
p=subprocess.run(['systemctl','start','raofflineproxy.service'],capture_output=True,text=True,timeout=20)
assert p.returncode==0,(p.returncode,p.stderr)
ready=time.monotonic()-start
os.environ['RAOFFLINEPROXY_CONFIG_DIR']='/storage/.config/raofflineproxy'
from raofflineproxy import storage,flusher
s=storage.Storage();deadline=time.monotonic()+25
while time.monotonic()<deadline:
 pending=s.get_pending_awards()
 if not pending:break
 time.sleep(.25)
integrity=s._connection.execute('PRAGMA integrity_check').fetchone()[0];s.close()
unit=subprocess.run(['systemctl','show','raofflineproxy.service','-p','Result','-p','ExecMainStatus','-p','MainPID','-p','ActiveState'],capture_output=True,text=True,timeout=5);assert unit.returncode==0
v={'status':'PASS' if not pending and integrity=='ok' and 'Result=success' in unit.stdout else 'FAIL','ready_seconds':ready,'queue_empty_seconds':time.monotonic()-start,'pending':pending,'integrity':integrity,'unit':unit.stdout,'peer_events':[json.loads(x) for x in (R/'peer-events.jsonl').read_text().splitlines()]}
(R/'recovery.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v));assert v['status']=='PASS',v
