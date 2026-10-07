from pathlib import Path
import datetime,hashlib,json,subprocess
owner=Path('/workspace/tmp/pixelelated-m7-replacement-16');tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16');run=Path((owner/'run.path').read_text().strip())
channels={n:(owner/n).read_text().strip() for n in ['inner.rc','outer.rc','tool-wrapper.rc']};channels['build.rc']=(run/'build.rc').read_text().strip();assert set(channels.values())=={'0'},channels
pids=[json.loads((owner/'launcher-pid.json').read_text())['pid']]+[int((run/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']]
for pid in pids:assert not Path('/proc',str(pid)).exists(),pid
for line in (owner/'harness.sha256').read_text().splitlines():
 h,n=line.split('  ',1);assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
subprocess.run(['python3','-I',str(owner/'verify-source.py')],cwd=tree,check=True)
containers=subprocess.check_output(['docker','ps','-aq','--no-trunc'],text=True).splitlines()
matching=[]
for cid in containers:
 info=json.loads(subprocess.check_output(['docker','inspect',cid],text=True))[0]
 if any(m.get('Source')==str(tree) for m in info.get('Mounts',[])):matching.append(cid)
assert not matching,matching
changed=subprocess.check_output(['git','status','--porcelain'],cwd=tree,text=True).splitlines();allowed='documentation/PER_DEVICE_DOCUMENTATION/GENERIC_X64/SUPPORTED_EMULATORS_AND_CORES.md';assert all(l[3:]==allowed for l in changed),changed
log=(owner/'console.log').read_text();assert '[642/642]' in log and 'PASS repaired installed scripts and rebuilt ES; unchanged sign-in window' in log
receipt=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),result='PASS',channels=channels,pids_absent=pids,containers_with_frozen_tree_mount=matching,manifest_sha256=hashlib.sha256((owner/'inputs.json').read_bytes()).hexdigest(),harness_sha256=hashlib.sha256((owner/'harness.sha256').read_bytes()).hexdigest(),generated_tracked_changes=changed,launcher_result=json.loads((owner/'launcher-result.json').read_text()),verification_note='Actual Docker inventory has no container mounting the frozen16 worktree; all source seals and owner exits verified.')
with (owner/'completion.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt))
