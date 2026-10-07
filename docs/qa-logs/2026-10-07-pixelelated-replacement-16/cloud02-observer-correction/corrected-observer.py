from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,socket,subprocess,sys
owner=Path('/workspace/tmp/pixelelated-m7-cloud-02')
output=Path('/workspace/repos/rocknix.worktrees/conflict-resolution/docs/qa-logs/2026-10-07-pixelelated-replacement-16/cloud02-runtime-observation')
output.mkdir(exist_ok=True)
mode=sys.argv[1];name='pixelelated-m7-cloud-02-s3'
def process(pid):
 p=Path('/proc',str(pid)); raw=(p/'cmdline').read_bytes()
 stat=(p/'stat').read_text().rsplit(')',1)[1].split()
 try:
  executable=os.readlink(p/'exe');exe_error=None
 except OSError as error:
  executable=None;exe_error=dict(errno=error.errno,reason=error.strerror)
 direct=any(a==str(owner).encode() or a.startswith((str(owner)+'/').encode()) for a in raw.split(b'\0'))
 title=raw.rstrip(b'\0').decode(errors='strict')
 pattern=r'^sshd: /usr/sbin/sshd -f '+re.escape(str(owner/'cloud/sftp/sshd_config'))+r' -E '+re.escape(str(owner/'cloud/sftp/sftp.log'))+r' \[listener\] \d+ of \d+-\d+ startups$'
 rewritten=bool(re.fullmatch(pattern,title))
 return dict(pid=pid,start_ticks=stat[19],executable=executable,executable_read_error=exe_error,cmdline_sha256=hashlib.sha256(raw).hexdigest(),owned_path_in_arguments=direct or rewritten,identity_method='exact_owned_sshd_config_and_log_in_listener_title' if rewritten else 'direct_argv')
def inspect():
 fmt='{"id":{{json .Id}},"image_id":{{json .Image}},"image_reference":{{json .Config.Image}},"running":{{json .State.Running}},"pid":{{json .State.Pid}},"started_at":{{json .State.StartedAt}},"ports":{{json .NetworkSettings.Ports}}}'
 r=subprocess.run(['docker','container','inspect','--format',fmt,name],text=True,capture_output=True)
 return r, json.loads(r.stdout) if r.returncode==0 else None
if mode in ['webdav','sftp','s3']:
 dest=output/(mode+'-live.json');assert not dest.exists()
 record=dict(observed_utc=datetime.now(timezone.utc).isoformat(),backend=mode,owner=str(owner),result='LIVE',secret_values_recorded=False)
 port={'webdav':9010,'sftp':9013,'s3':9012}[mode]
 with socket.create_connection(('127.0.0.1',port),timeout=2):pass
 record['port_accepting']=port
 if mode=='s3':
  r,v=inspect();assert r.returncode==0 and v['running'] and v['pid']>0
  record['container']=v;record['process']=process(v['pid'])
  fmt='{"id":{{json .Id}},"repo_digests":{{json .RepoDigests}},"created":{{json .Created}},"architecture":{{json .Architecture}},"os":{{json .Os}}}'
  record['image']=json.loads(subprocess.check_output(['docker','image','inspect','--format',fmt,v['image_id']],text=True))
  assert record['image']['id']==v['image_id']
 else:
  pidfile=owner/'cloud'/('webdav.pid' if mode=='webdav' else 'sftp/sftp.pid')
  record['process']=process(int(pidfile.read_text()));assert record['process']['owned_path_in_arguments']
 with dest.open('x') as f:json.dump(record,f,indent=2);f.write('\n')
 print(json.dumps(record))
elif mode=='finished':
 completion=json.loads((owner/'owner-verification.json').read_text());assert completion['result']=='PASS'
 assert json.loads((owner/'guest-cleanup-verification.json').read_text())['passed']
 snapshots=[json.loads((output/(b+'-live.json')).read_text()) for b in ['webdav','sftp','s3']]
 for row in snapshots:
  old=row['process'];p=Path('/proc',str(old['pid']))
  if p.exists():assert process(old['pid'])['start_ticks']!=old['start_ticks'],old
 r,v=inspect();assert r.returncode!=0 and v is None and 'No such' in r.stderr,r.stderr
 with (output/'cleanup.json').open('x') as f:json.dump(dict(verified_utc=datetime.now(timezone.utc).isoformat(),result='PASS',recorded_processes_exited=True,exact_owned_container_absent=name,owner_result=completion['result']),f,indent=2);f.write('\n')
 print('PASS observed backend processes exited; exact owned MinIO container absent')
else:raise SystemExit('expected webdav, sftp, s3 or finished')
