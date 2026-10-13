from pathlib import Path
import json,subprocess,shlex,time,tarfile,datetime,hashlib
r=Path(__file__).parent;root=r.parent;vm=root/'vm';ssh=json.loads((vm/'ssh-command.json').read_text());result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat()}
def remote(cmd,**kw):return subprocess.run(ssh+[cmd],check=True,**kw)
try:
 owner=vm/'version-owner03';deadline=time.monotonic()+7200
 while not (owner/'launcher-result.json').exists():
  assert time.monotonic()<deadline,'engine matrix dependency timed out'
  print('WAIT',datetime.datetime.now(datetime.timezone.utc).isoformat(),'engine matrix',flush=True);time.sleep(30)
 launch=json.loads((owner/'launcher-result.json').read_text());assert launch['runner_returncode']==1 and (owner/'tool-wrapper.rc').read_text().strip()=='1'
 assert json.loads((vm/'version-matrix-result02.json').read_text())['rc']==1
 result['independent_of_failed_engine_matrix']=True
 while Path('/proc',str(launch['pid'])).exists() and time.monotonic()<deadline:time.sleep(1)
 assert not Path('/proc',str(launch['pid'])).exists()
 assert json.loads((r/'result.json').read_text())['rc']==0
 archive=r/'runtime.tar'
 with tarfile.open(archive,'w') as t:
  for rel in ['usr/lib','usr/bin']:t.add(r/'installed-new'/rel,arcname=rel)
 remote('mkdir -p /storage/qa-572/package')
 with archive.open('rb') as f:remote('tar -xf - -C /storage/qa-572/package',stdin=f)
 with (r/'guest-proof02.py').open('rb') as f:remote('cat > /storage/qa-572/proof.py',stdin=f)
 with (r/'vm-proof.json').open('wb') as o,(r/'vm-proof.stderr').open('wb') as e:remote('python3 /storage/qa-572/proof.py',stdout=o,stderr=e,timeout=150)
 j=json.loads((r/'vm-proof.json').read_text());assert j['rc']==0
 print('Plugin controls PASS',flush=True)
 result['library_mount_restored']=remote("if mountpoint -q /usr/lib; then exit 1; else echo restored; fi",capture_output=True,text=True).stdout.strip()=='restored'
 result['rc']=0
except BaseException as e:result.update(rc=1,error=repr(e));raise
finally:
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'plugin-result04.json').write_text(json.dumps(result,indent=2)+'\n')
