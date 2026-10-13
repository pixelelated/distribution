from pathlib import Path
import subprocess,json,datetime
r=Path('/workspace/tmp/pix-m7-baseline-tests-20261013');ssh=json.loads((r/'ssh-command.json').read_text());tool=Path('/workspace/repos/rocknix.worktrees/m7-player-setup/tools/vm-visual-qa')
result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rc':1,'cases':[]}
def run(*args):subprocess.run(args,check=True,timeout=65)
def mode(outcome,delay):
 data=json.dumps({'outcome':outcome,'delay':delay,'count':3})
 subprocess.run(ssh+['cat > /storage/qa-m7-baseline/wifi-mode.json'],input=data.encode(),check=True,timeout=15)
try:
 for name,outcome,delay,enter in [('refresh','networks',12,'key x'),('empty','empty',3,'key x'),('failure','failure',3,'key x')]:
  mode(outcome,delay)
  steps=r/('wifi-'+name+'.steps');steps.write_text(enter+'\nwait 1\nshot '+name+'-pending\nwait '+str(delay+2)+'\nsettle\nshot '+name+'-complete\n')
  run(str(tool),'--monitor',str(r/'monitor.sock'),'run',str(steps),'--outdir',str(r/('wifi-'+name)))
  result['cases'].append({'case':name,'walk_rc':0})
 result['rc']=0
finally:
 p=subprocess.run(ssh+['cat /storage/qa-m7-baseline/wifi-calls.jsonl'],capture_output=True,timeout=15)
 if p.returncode==0:(r/'wifi-calls.jsonl').write_bytes(p.stdout)
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'wifi-branches-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
