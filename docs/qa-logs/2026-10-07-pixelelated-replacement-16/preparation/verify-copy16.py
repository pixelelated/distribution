from pathlib import Path
import datetime,hashlib,json,subprocess
owner=Path('/workspace/tmp/pixelelated-m7-replacement-16');copy=owner/'cache-copy'
run=Path((owner/'copy.run').read_text().strip())
channels={n:(owner/n).read_text().strip() for n in ['copy.rc','copy.outer.rc','cache-ready.rc']}
channels['tool-wrapper.rc']=(copy/'tool-wrapper.rc').read_text().strip();channels['build.rc']=(run/'build.rc').read_text().strip()
assert set(channels.values())=={'0'},channels
for line in (owner/'harness.sha256').read_text().splitlines():
 h,n=line.split('  ',1);assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
assert (owner/'cache-compare.txt').read_bytes()==b''
facts=json.loads((owner/'cache-ready.json').read_text());assert facts['checksum_equal'] and facts['independent_regular_files']>1000000,facts
pids=[json.loads((copy/'launcher-pid.json').read_text())['pid']]+[int((run/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']]
for pid in pids:assert not Path('/proc',str(pid)).exists(),pid
subprocess.run(['python3','-I',str(owner/'verify-source.py')],cwd='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16',check=True)
receipt=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),result='PASS',channels=channels,pids_absent=pids,cache=facts,harness_sha256=hashlib.sha256((owner/'harness.sha256').read_bytes()).hexdigest())
with (owner/'copy-verification.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt))
