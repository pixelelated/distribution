from pathlib import Path
import json,subprocess,time
from ui import out,remote,shot
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');case=r/'wifi-fr1280-bb9e-branches';case.mkdir();result={'rc':1,'started':time.time(),'branches':[]}
def walk(label,steps,timeout=35):
 f=case/(label+'.steps');f.write_text(steps);p=subprocess.run([str(repo/'tools/vm-visual-qa'),'--monitor',str(r/'vm/monitor.sock'),'run',str(f),'--outdir',str(case/label)],timeout=timeout);assert p.returncode==0,label
try:
 result['before']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation').strip()
 plan=json.loads(out('cat /storage/qa-wifi-577-fr1280-bb9e/plan.json'));assert json.loads(out('cat /storage/qa-wifi-577-fr1280-bb9e/state.json'))['next_scan']==1
 plan['scans'][2:] = [{'delay':3,'rc':2,'networks':['DISCARD FAILED PARTIAL']},{'delay':3,'networks':[]},{'delay':8,'networks':['Long network %02d'%i for i in range(1,37)]},{'delay':8,'networks':['Long network %02d'%i for i in range(1,37)]}]
 remote('cat > /storage/qa-wifi-577-fr1280-bb9e/plan.json',input=json.dumps(plan),text=True,capture_output=True)
 walk('refresh','key down x3\nkey x\nwait 1\nshot pending\nkey x\nkey x\nwait 9\nsettle\nshot complete\n')
 result['branches'].append('refresh plus duplicate activation input')
 walk('failure','key x\nwait 1\nshot pending\nwait 4\nsettle\nshot complete\n');result['branches'].append('failed enumeration retains prior rows')
 walk('empty','key x\nwait 1\nshot pending\nwait 4\nsettle\nshot complete\n');result['branches'].append('successful zero replaces rows')
 walk('back-reopen','key x\nwait 1\nshot pending\nkey z\nwait-for-change\nsettle\nshot returned\nkey x\nwait 1\nshot reattached\nwait 8\nsettle\nshot complete\n',45);result['branches'].append('Back/reopen attaches one pending scan')
 walk('long-scroll','key down x24\nsettle\nshot selected\nkey down x12\nkey x\nwait 1\nshot pending\nwait 9\nsettle\nshot complete\n',40);result['branches'].append('long list and same-result refresh')
 events=out('cat /storage/qa-wifi-577-fr1280-bb9e/calls.jsonl');(case/'calls.jsonl').write_text(events);rows=[json.loads(x) for x in events.splitlines()];starts=[x for x in rows if x['phase']=='start' and x['command'] in ['list','scanlist']];ends=[x for x in rows if x['phase']=='end' and x['command'] in ['list','scanlist']];assert len(starts)==len(ends)==6,(len(starts),len(ends));assert [x['rc'] for x in ends]==[0,0,2,0,0,0]
 result['after']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation').strip();assert result['before']==result['after'];result['rc']=0
finally:
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
