"""Record independently observed terminal results for durable M7 QA owners."""
from pathlib import Path
import datetime,hashlib,json,sys
owner=Path(sys.argv[1]).resolve();submission=sys.argv[2]
result=json.loads((owner/'launcher-result.json').read_text());code=result['runner_returncode']
run=Path((owner/'run.path').read_text().strip())
channels={str(p):int(p.read_text().strip()) for p in [owner/'inner.rc',owner/'outer.rc',owner/'tool-wrapper.rc',run/'build.rc']}
assert all(v==code for v in channels.values()),channels
assert (run/'build.status').read_text().startswith('state:       finished\n')
observed=[]
sources=[run/'build.pid',run/'watcher.pid',run/'command.pid',owner/'guest.pid']
for p in sources:
 if not p.exists():continue
 pid=int(p.read_text());proc=Path('/proc')/str(pid)
 state='absent' if not proc.exists() else (proc/'stat').read_text().rsplit(')',1)[1].split()[0]
 assert state in {'absent','Z'},(p,pid,state)
 observed.append({'source':str(p),'pid':pid,'state':state})
launcher=Path('/proc')/str(result['pid'])
if launcher.exists():assert (launcher/'stat').read_text().rsplit(')',1)[1].split()[0]=='Z'
for p in Path('/proc').glob('[0-9]*/cmdline'):
 try:first=p.read_bytes().split(b'\0',1)[0].decode()
 except (OSError,UnicodeError):continue
 assert not Path(first).name.startswith('qemu-system-'),p
receipt={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'submission_tool_chunk':submission,'submission_rc':0,'job_rc':code,
 'job_result_source':str(owner/'launcher-result.json'),'result_channels':channels,
 'owned_processes':observed,'qemu_absent':True,'run':str(run),
 'build_log_sha256':hashlib.sha256((run/'build.log').read_bytes()).hexdigest()}
with (owner/'completion.json').open('x') as f:f.write(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
