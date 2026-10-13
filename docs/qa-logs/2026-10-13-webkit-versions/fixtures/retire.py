from pathlib import Path
import json,subprocess,shlex,time,datetime,hashlib
r=Path(__file__).parent;ssh=json.loads((r/'ssh-command.json').read_text());result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retired':[]}
def remote(cmd,**kw):return subprocess.run(ssh+[cmd],check=True,timeout=30,**kw)
try:
 launch=json.loads((r/'headroom-owner/launcher-result.json').read_text());assert launch['runner_returncode']==0 and not Path('/proc',str(launch['pid'])).exists()
 assert json.loads((r/'headroom-result.json').read_text())['library_mount_restored']
 code="""from pathlib import Path
import json
names={'cloud-signin-window','WebKitWebProcess','WebKitNetworkProcess','WebKitGPUProcess'}
browsers=[]
for p in Path('/proc').glob('[0-9]*'):
 try:
  if (p/'exe').resolve().name in names:browsers.append(p.name)
 except OSError:pass
assert not browsers,browsers
mounts=[l for l in Path('/proc/mounts').read_text().splitlines() if l.split()[1] in ['/usr/lib','/usr/libexec/webkit2gtk-4.1','/usr/lib/webkit2gtk-4.1']]
assert not mounts,mounts
print(json.dumps({'browser_processes':browsers,'temporary_mounts':mounts,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip()}))
"""
 result['guest_readback']=json.loads(remote('python3 -c '+shlex.quote(code),capture_output=True,text=True).stdout)
 for f in ['frame0.png','frame1.png']:
  with (r/('repeat-1-2540-'+f)).open('wb') as out:remote('cat /storage/qa-570/repeat-1-2540/'+f,stdout=out)
 with (r/'streamed-samples.tar').open('wb') as out:remote('tar -cf - /storage/qa-570/headroom-2540/samples.jsonl /storage/qa-570/headroom-2541/samples.jsonl /storage/qa-570/headroom-2541-gst/samples.jsonl',stdout=out)
 remote('sync; poweroff');time.sleep(8)
 subprocess.run(['tools/vm-stop',str(r/'vm.pid'),str(r/'disk.qcow2')],check=True)
 for name in ['disk.qcow2','OVMF.fd','qa-key','qa-key.pub','known_hosts']:
  p=r/name
  if p.exists():
   st=p.stat();result['retired'].append({'path':str(p),'logical_bytes':st.st_size,'allocated_bytes':st.st_blocks*512});p.unlink()
 result['rc']=0
except BaseException as e:result.update(rc=1,error=repr(e));raise
finally:
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'retirement.json').write_text(json.dumps(result,indent=2)+'\n')
