from pathlib import Path
import hashlib,json,subprocess,datetime
O=Path(__file__).parent;B=Path('/workspace/tmp/pixelelated-m7-replacement-17');R=Path.cwd();W=Path((B/'run.path').read_text().strip())
channels={n:(B/n).read_text().strip() for n in ['inner.rc','outer.rc','tool-wrapper.rc']};channels['build.rc']=(W/'build.rc').read_text().strip();assert set(channels.values())=={'1'},channels
pids=[json.loads((B/'launcher-pid.json').read_text())['pid']]+[int((W/n).read_text()) for n in ['build.pid','watcher.pid','command.pid']]
assert all(not Path('/proc',str(p)).exists() for p in pids),pids
assert json.loads((B/'launcher-result.json').read_text())['runner_returncode']==1
log=(B/'console.log').read_text();assert '[643/643]' in log and 'Successful build, creating image...' in log and 'FileNotFoundError' in log
assert 'PASS frozen inputs, host options, container and 24/4 concurrency' in log
original={'channels':channels,'pids_absent':pids,'original_result':'FAILED post-build fixture; unchanged','cause':'host opened guest-runtime absolute symlink instead of staged catalog','build_tasks':'643/643','container_observation':'live inspect missed; pinned digest bound by actual logged invocation and pre/post image-ID checks; no observed container ID claimed'}
(O/'original-failure.json').write_text(json.dumps(original,indent=2)+'\n')
for line in (B/'harness.sha256').read_text().splitlines():
 h,n=line.split('  ',1);assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
subprocess.run(['python3','-I',str(B/'verify-source.py')],check=True)
files=sorted((R/'target').iterdir());assert len(files)==4 and all(p.is_file() for p in files),files
def digests():
 return {p.name:{'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest(),'bytes':p.stat().st_size} for p in files}
before=digests();(O/'artifacts-before.json').write_text(json.dumps(before,indent=2)+'\n')
subprocess.run(['python3','-I',str(O/'assembled-checks.py')],check=True)
after=digests();assert after==before
(O/'artifacts-after.json').write_text(json.dumps(after,indent=2)+'\n')
subprocess.run(['python3','-I',str(B/'verify-source.py')],check=True)
containers=[]
for cid in subprocess.check_output(['docker','ps','-aq','--no-trunc'],text=True).splitlines():
 j=json.loads(subprocess.check_output(['docker','inspect',cid]))[0]
 if any(m.get('Source')==str(R) for m in j.get('Mounts',[])):containers.append(cid)
assert not containers,containers
(O/'verification.json').write_text(json.dumps({'result':'PASS','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_attempt':original,'all_assembled_assertions':True,'firmware_unchanged':before==after,'artifacts':after,'containers_mounting_frozen_tree':containers,'frozen_source_unchanged':True,'correction':'host catalog path only; runtime link assertions added'},indent=2)+'\n')
print('PASS all corrected assembled assertions; all original firmware bytes unchanged; original failed attempt retained',flush=True)
