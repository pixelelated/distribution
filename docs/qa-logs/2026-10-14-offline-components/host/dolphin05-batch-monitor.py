from pathlib import Path
import subprocess,json,time
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-dolphin-preservation-581');helper=repo/'docs/qa-logs/2026-10-13-dolphin-preservation-source/installed-flow/remaining-two/host-serial.py';args=['--repo',str(repo),'--serial',str(r/'vm/serial.sock'),'--monitor',str(r/'vm/monitor.sock'),'--receipts',str(r/'dolphin05-frames')];result={'rc':1,'started':time.time()}
try:
 p=subprocess.run(['python3','-I','-S','-B',str(helper),'start',*args],capture_output=True,text=True,timeout=30);(r/'dolphin05-start.stdout').write_text(p.stdout);(r/'dolphin05-start.stderr').write_text(p.stderr);result['start_original_exit']=p.returncode;assert p.returncode==0,p.stderr
 print(p.stdout,flush=True);deadline=time.monotonic()+1800
 while not (r/'dolphin05-accepted.json').exists():
  if (r/'dolphin05-abort').exists():raise RuntimeError('Coordinator abort')
  if time.monotonic()>deadline:raise TimeoutError('Batch deadline')
  time.sleep(1)
 accepted=json.loads((r/'dolphin05-accepted.json').read_text());assert accepted['batch_session_exit']==0 and accepted['batch_session_alive'] is False and accepted['phase']=='done',accepted
 result['rc']=0
finally:
 if result['rc']!=0:
  p=subprocess.run(['python3','-I','-S','-B',str(helper),'abort',*args],capture_output=True,text=True,timeout=30);result['abort_original_exit']=p.returncode;(r/'dolphin05-abort.stdout').write_text(p.stdout);(r/'dolphin05-abort.stderr').write_text(p.stderr)
 result['ended']=time.time();(r/'dolphin05-monitor-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
