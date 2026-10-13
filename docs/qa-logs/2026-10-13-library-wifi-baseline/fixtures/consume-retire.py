from pathlib import Path
import subprocess,json,re,datetime,os,stat
r=Path('/workspace/tmp/pix-m7-baseline-tests-20261013');co=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');ssh=json.loads((r/'ssh-command.json').read_text())
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owners':[],'rc':1}
for o in sorted(r.glob('*-owner')):
 expected=1 if o.name in ['library-owner','collection-library02-owner'] else 0
 j=json.loads((o/'launcher-result.json').read_text());wr=int((o/'tool-wrapper.rc').read_text())
 log=(o/'console.log').read_text();p=Path(re.search(r'watch-build: recording in ([^\n]+)',log).group(1));br=int((p/'build.rc').read_text())
 assert j['runner_returncode']==wr==br==expected,(o,j,wr,br)
 pids=[j['pid']]+[int((p/x).read_text()) for x in ['build.pid','command.pid','watcher.pid','build.status.pid'] if (p/x).exists()]
 states=[]
 for pid in sorted(set(pids)):
  proc=Path('/proc')/str(pid)
  absent=not proc.exists();cmd=(proc/'cmdline').read_bytes() if not absent else b''
  assert absent or not cmd,('Live owner',o,pid)
  states.append({'pid':pid,'process_absent':absent,'exited_zombie':not absent and not cmd})
 result['owners'].append({'owner':o.name,'expected_rc':expected,'launcher_rc':j['runner_returncode'],'wrapper_rc':wr,'watcher_rc':br,'run':str(p),'actual_host_processes':states})
# Restore enumeration tool before shutting down disposable guest.
p=subprocess.run(ssh+['umount /usr/bin/wifictl && sha256sum /usr/bin/wifictl && systemctl show essway.service -p ActiveState -p NRestarts'],capture_output=True,timeout=20,check=True)
(r/'guest-final.txt').write_bytes(p.stdout)
vm_pid=int((r/'vm.pid').read_text());result['vm_pid']=vm_pid
paths=['disk.qcow2','OVMF.fd','qa-key','qa-key.pub','known_hosts']
ident={}
for n in paths:
 p=r/n;s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink();ident[n]=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_blocks*512)
result['before_available_bytes']=os.statvfs(r).f_bavail*os.statvfs(r).f_frsize
subprocess.run([str(co/'tools/vm-stop'),str(r/'vm.pid'),str(r/'disk.qcow2')],check=True,timeout=30)
assert not (Path('/proc')/str(vm_pid)/'cmdline').exists() or not (Path('/proc')/str(vm_pid)/'cmdline').read_bytes()
result['removed']=[]
for n in paths:
 p=r/n;s=p.lstat();assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_blocks*512)==ident[n],('Identity changed',n)
 p.unlink();result['removed'].append({'path':n,'allocated_bytes':ident[n][4],'absent':not p.exists()})
result['released_allocated_bytes']=sum(x['allocated_bytes'] for x in result['removed']);result['after_available_bytes']=os.statvfs(r).f_bavail*os.statvfs(r).f_frsize
result['rc']=0;result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'consumption-retirement.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'rc':0,'owners_consumed':len(result['owners']),'retired_vm_pid':vm_pid,'released_allocated_bytes':result['released_allocated_bytes']}))
