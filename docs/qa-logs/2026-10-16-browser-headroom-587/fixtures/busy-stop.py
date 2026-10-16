import subprocess,json,time,os
from pathlib import Path
R=Path('/storage/qa587');start=time.monotonic();p=subprocess.run(['systemctl','stop','raofflineproxy.service'],capture_output=True,text=True,timeout=23)
s=subprocess.run(['systemctl','show','raofflineproxy.service','-p','Result','-p','ExecMainStatus','-p','ExecMainCode','-p','MainPID','-p','ActiveState'],capture_output=True,text=True,timeout=5);assert s.returncode==0
os.environ['RAOFFLINEPROXY_CONFIG_DIR']='/storage/.config/raofflineproxy'
from raofflineproxy import storage,flusher
store=storage.Storage();pending=store.get_pending_awards();v={'stop_rc':p.returncode,'elapsed':time.monotonic()-start,'stdout':p.stdout,'stderr':p.stderr,'unit':s.stdout,'pending':pending,'chain':flusher.verify_chain(pending),'integrity':store._connection.execute('PRAGMA integrity_check').fetchone()[0]};store.close()
(R/'busy-stop.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v))
