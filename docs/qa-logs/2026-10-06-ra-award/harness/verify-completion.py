import datetime,hashlib,json,socket,subprocess
from pathlib import Path
owner=Path('/workspace/tmp/pixelelated-m7-ra-01');run=Path((owner/'run.path').read_text().strip())
rcs={n:int((owner/n).read_text()) for n in ['inner.rc','outer.rc','tool-wrapper.rc']};rcs['build.rc']=int((run/'build.rc').read_text());assert all(v==0 for v in rcs.values()),rcs
assert 'state:       finished' in (run/'build.status').read_text()
pids={json.loads((owner/'launcher-pid.json').read_text())['pid'],int((run/'build.pid').read_text()),int((run/'watcher.pid').read_text())}
for line in (owner/'actual-process-observations.jsonl').read_text().splitlines():
 for p in json.loads(line)['processes']:pids.add(p['pid'])
for pid in pids:assert not Path(f'/proc/{pid}').exists(),pid
for f in Path('/proc').glob('[0-9]*/cmdline'):
 try:first=f.read_bytes().split(b'\0',1)[0].decode()
 except (OSError,UnicodeError):continue
 assert not Path(first).name.startswith('qemu-system-'),f
for port in [10022,10023,5909,5910]:
 with socket.socket() as s:s.bind(('127.0.0.1',port))
log=(owner/'artifacts/ra-offline.log').read_text();checks=['100359 Potato-tan Secret -- not earned','hardcore=0','28/28 achievements active','queued_offline','pending = 1','flushed=1','pending = 0','achievement 100359 earned by the QA account','27/28 achievements active','account cleared','PASSED (33)']
for text in checks:assert text in log,text
assert sum(x.strip().startswith('PASS ') for x in log.splitlines())==33
assert not any(x.strip().startswith('FAIL ') for x in log.splitlines())
assert (owner/'artifacts/account-cleanup.log').read_text().startswith('cleared:')
subprocess.run(['sha256sum','-c',str(owner/'harness.sha256')],stdout=subprocess.DEVNULL,check=True)
groups={}
for f in sorted((owner/'artifacts/frames').glob('*.png')):groups.setdefault(hashlib.sha256(f.read_bytes()).hexdigest(),[]).append(f.name)
assert sum(map(len,groups.values()))==40 and len(groups)==4
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':str(owner),'run':str(run),'results':rcs,'recorded_pids_absent':sorted(pids),'qemu_processes_absent':True,'ports_unbound':[10022,10023,5909,5910],'account_cleanup_verified_by_tool':True,'passes':33,'failures':0,'skips':0,'game_id':15738,'achievement_id':100359,'mode':'softcore/normal','initial_unearned':True,'offline_queue_after_exit':1,'after_flush_pending':0,'provider_earned_verified':True,'relaunch_active_before':28,'relaunch_active_after':27,'frame_groups':groups,'visual_review':'Four unique images directly inspected: complete ES carousel after exits, offline/online indicator changes; no credentials/account identity shown. No achievement send/queue card captured; no new card-layout claim.','harness_verified':True,'source':'7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2','image_sha256':'c7df6a6f428086f79a377ca1b049f20694f34a868987cf12c493c78eab7b2254'}
with (owner/'completion.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='frame_groups'},indent=2))
