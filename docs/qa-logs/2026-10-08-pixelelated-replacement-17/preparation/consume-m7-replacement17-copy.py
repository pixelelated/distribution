import datetime,hashlib,json,pathlib,subprocess
owner=pathlib.Path('/workspace/tmp/pixelelated-m7-replacement-17')
run=pathlib.Path((owner/'copy.run').read_text().strip())
assert run.parent==pathlib.Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17/.build-runs')
channels={str(p):int(p.read_text().strip()) for p in [owner/'copy.rc',owner/'copy.outer.rc',owner/'cache-ready.rc',owner/'cache-copy/tool-wrapper.rc',run/'build.rc']}
assert set(channels.values())=={0},channels
result=json.loads((owner/'cache-copy/launcher-result.json').read_text());assert result['runner_returncode']==0
pids=[json.loads((owner/'cache-copy/launcher-pid.json').read_text())['pid']]+[int((run/n).read_text().strip()) for n in ['build.pid','watcher.pid','command.pid']]
assert all(not pathlib.Path('/proc',str(p)).exists() for p in pids),pids
ready=json.loads((owner/'cache-ready.json').read_text());assert ready['checksum_equal'] is True and ready['independent_regular_files']>2000000
assert not (owner/'cache-compare.txt').read_bytes()
record={'result':'PASS','verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'channels':channels,'launcher_returncode':result['runner_returncode'],'actual_host_pids_absent':pids,'cache_ready':ready,'cache_compare_bytes':0,'copy_finished':(owner/'copy.finish').read_text().strip()}
with (owner/'copy-verification.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record,indent=2))
