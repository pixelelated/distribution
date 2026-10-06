import datetime,hashlib,json,socket,subprocess
from pathlib import Path
owner=Path('/workspace/tmp/pixelelated-m7-cloud-01')
run=Path((owner/'run.path').read_text().strip())
rcs={n:int((owner/n).read_text()) for n in ['inner.rc','outer.rc','tool-wrapper.rc']}
rcs['build.rc']=int((run/'build.rc').read_text());assert all(v==0 for v in rcs.values()),rcs
status=(run/'build.status').read_text();assert 'state:       finished' in status
pids=set()
for name in ['launcher-pid.json','launcher-start.json']:
 pids.add(json.loads((owner/name).read_text())['pid'])
for name in ['build.pid','watcher.pid']:pids.add(int((run/name).read_text()))
for line in (owner/'actual-process-observations.jsonl').read_text().splitlines():
 for proc in json.loads(line)['processes']:pids.add(proc['pid'])
pids.add(json.loads((owner/'artifacts/minio-container.json').read_text())['pid'])
for pid in pids:assert not Path(f'/proc/{pid}').exists(),pid
for f in Path('/proc').glob('[0-9]*/cmdline'):
 try:first=f.read_bytes().split(b'\0',1)[0].decode()
 except (OSError,UnicodeError):continue
 assert not Path(first).name.startswith('qemu-system-'),f
assert subprocess.run(['docker','inspect','pixelelated-m7-cloud-01-s3'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
for path in ['cloud/webdav.pid','cloud/sftp/sftp.pid','cloud/s3/s3.pid']:assert not (owner/path).exists(),path
ports=[9010,9011,9012,9013,10022,10023]
for port in ports:
 with socket.socket() as s:s.bind(('127.0.0.1',port))
results={}
for backend in ['webdav','sftp','s3']:
 paths=list((owner/'artifacts/rocknix-images').glob(f'qa-7afa9efcfc-{backend}-a-*/report.md'));assert len(paths)==1
 report=paths[0];text=report.read_text();log=report.with_name('round-trip.log');s=log.read_text()
 assert '| round-trip | PASS |' in text and '\nPASSED\n' in s
 counts={v:sum(line.strip().startswith(v+' ') for line in s.splitlines()) for v in ['PASS','FAIL','SKIP']}
 assert counts['PASS']>0 and counts['FAIL']==counts['SKIP']==0
 results[backend]={'report':str(report),'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'counts':counts}
subprocess.run(['sha256sum','-c',str(owner/'harness.sha256')],check=True,stdout=subprocess.DEVNULL)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':str(owner),'run':str(run),'results':rcs,'watcher_state':'finished','recorded_pids_absent':sorted(pids),'qemu_processes_absent':True,'minio_container_absent':True,'backend_pidfiles_absent':True,'ports_unbound':ports,'suites':results,'harness_verified':True,'source':'7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2','image_sha256':'c7df6a6f428086f79a377ca1b049f20694f34a868987cf12c493c78eab7b2254','scope':'Three local round-trip suites; no hosted OAuth/Dropbox or RA award execution.'}
with (owner/'completion.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
