#!/usr/bin/env python3
"""Owned qa19/20 continuation; existing tools/cases unchanged, SOURCE-ONLY UNRUN."""
import ctypes,hashlib,json,os,re,signal,socket,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent;C=json.loads((R/'config.json').read_text());TREE=Path(C['checkout'])
assert not (R/'result.json').exists(),'fresh owner required'
result={'rc':1,'started':time.time(),'commands':[],'reports':[],'qemu':[],'backend_owners':{},'cleanup_errors':[]};seq=0;next_sample=0;owned={};attempted=[];pair_attempted=False
STANDARD=['scripts','lifetime','wrapper','vocabulary','french','quoting','menumap','register','pair-identity','fresh','round-trip','exit','time-to-play','walks','frame-diff']
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
assert sha(R/'census.py')==C['code']['census.py'];sys.path.insert(0,str(R))
from census import direct_children,signal_child,proc_identity
BASE={k:v for k,v in os.environ.items() if not k.startswith('CLOUD_QA_')}
BASE.update(LAST_GOOD_SOURCE_ROOT=str(TREE),TMPDIR=str(R/'tmp'),VM_PAIR_DIR=str(R/'pair'),VM_QEMU_RUNTIME_DIR=str(R/'runtime'),VM_GL='auto',ES_SRC=C['es_source'],RETROARCH_SRC=C['retroarch_source'],QA_SYSTEM_ROOT=C['system_root'],WALK_BASELINE=C['baseline'],PYTHONDONTWRITEBYTECODE='1')
def env(backend):return dict(BASE,CLOUD_QA_BACKEND=backend,CLOUD_QA_STATE=str(R/'cloud'/backend),CLOUD_QA_NAME=C['minio_name'],CLOUD_QA_IMAGE=C['minio_image'],CLOUD_QA_USER='qauser',CLOUD_QA_PASS='qa-password',CLOUD_QA_BIND='127.0.0.1',CLOUD_QA_GUEST_HOST='10.0.2.2',CLOUD_QA_DEAD_PORT='9011',ROCKNIX_ARTIFACTS=str(R/'artifacts'/backend))
def proc(pid):
 row=proc_identity(pid)
 if row is None:return None
 try:
  stat=Path('/proc',str(pid),'stat').read_bytes().rpartition(b')')[2].split()
  if stat[0]==b'Z':return None
  row['argv']=[x.decode(errors='replace') for x in Path('/proc',str(pid),'cmdline').read_bytes().split(b'\0') if x]
  return row
 except (FileNotFoundError,ProcessLookupError):return None
def same(row):
 now=proc(row['pid']);return now if now and now['start_ticks']==row['start_ticks'] else None
def managed(row):
 # Existing vm-pair and backend helpers stop these exact long-lived owners.
 args=row.get('argv',[])
 if args and Path(args[0]).name.startswith('qemu-system-') and any('if=none,id=rocknix,format=qcow2,file='+str(R/'pair'/('vm-'+g+'.qcow2')) in args for g in ['a','b']):return 'qemu'
 if str(R/'cloud/webdav/data') in args and 'serve' in args and 'webdav' in args:return 'webdav'
 if any(str(R/'cloud/sftp/sftp/sshd_config') in a.split() for a in args) and any('sshd' in a for a in args):return 'sftp'
 return None
def observe(active):
 global next_sample
 # Adopted helper exits must become absent before the existing kill-0 checks.
 # Never reap Popen's stage: poll()/wait() own that original status. WNOHANG
 # collects only terminated children; no signal or blocking wait occurs here.
 for identity in direct_children(os.getpid()):
  if identity['pid']==active.pid:continue
  try:pid,status=os.waitpid(identity['pid'],os.WNOHANG)
  except ChildProcessError:continue
  if pid:
   receipt=dict(identity,wait_status=status,returncode=os.waitstatus_to_exitcode(status),phase='observation',epoch=time.time())
   result.setdefault('reaped_children',[]).append(receipt)
   with (R/'records/adopted-exits.jsonl').open('a') as f:f.write(json.dumps(receipt)+'\n')
 children=direct_children(os.getpid())
 for identity in children:
  row=proc(identity['pid'])
  if row:owned[(row['pid'],row['start_ticks'])]=row
 if time.monotonic()<next_sample:return
 files=[f for root in [R/'records',R/'artifacts'] for f in root.rglob('*') if f.is_file() and not f.is_symlink()]
 total=0;vanished=0
 for f in files:
  try:total+=f.stat().st_size
  except FileNotFoundError:vanished+=1
 assert total<=C['record_limit_bytes'] and len(files)<=4096,'original records bound'
 sample={'epoch':time.time(),'vanished_during_record_sample':vanished,'record_bytes':total,'record_files':len(files),'direct_children':children,'meminfo':Path('/proc/meminfo').read_text(),'memory_pressure':Path('/proc/pressure/memory').read_text(),'io_pressure':Path('/proc/pressure/io').read_text(),'filesystem_available_bytes':os.statvfs(R).f_bavail*os.statvfs(R).f_frsize,'qemu_status':{}}
 for row in owned.values():
  if managed(row)=='qemu' and same(row):sample['qemu_status'][str(row['pid'])]=Path('/proc',str(row['pid']),'status').read_text()
 with (R/'records/resources.jsonl').open('a') as f:f.write(json.dumps(sample)+'\n')
 next_sample=time.monotonic()+5

def reap(active=None):
 deadline=time.monotonic()+13;grace=time.monotonic()+2;interventions=[]
 while True:
  if active:active.poll()
  for identity in direct_children(os.getpid()):
   row=proc(identity['pid'])
   if row and managed(row):continue # never signal a live VM/backend through generic cleanup
   if active and identity['pid']==active.pid:continue
   try:pid,status=os.waitpid(identity['pid'],os.WNOHANG)
   except ChildProcessError:continue
   if pid:result.setdefault('reaped_children',[]).append({'pid':pid,'wait_status':status})
  children=[]
  for identity in direct_children(os.getpid()):
   row=proc(identity['pid'])
   if row and managed(row):continue
   children.append(identity)
  if not children:return interventions
  assert time.monotonic()<deadline,'adopted host cleanup deadline'
  if not active and time.monotonic()<grace:time.sleep(.05);continue
  for identity in children:
   row=proc(identity['pid'])
   if row:owned[(row['pid'],row['start_ticks'])]=row
   action=signal_child(identity,os.getpid())
   if action['outcome']=='pidfd-kill':interventions.append(action);result.setdefault('forced_child_cleanup',[]).append(action)
  time.sleep(.02)
def call(name,args,seconds,backend='webdav',check=True):
 global seq
 seq+=1;stem=R/'records'/('%03d-%s'%(seq,name));row={'name':name,'argv':list(map(str,args)),'backend':backend,'timeout_seconds':seconds,'timed_out':False,'original_returncode':None};result['commands'].append(row);child=None
 try:
  with Path(str(stem)+'.stdout').open('xb') as out,Path(str(stem)+'.stderr').open('xb') as err:
   child=subprocess.Popen(row['argv'],cwd=TREE,env=env(backend),stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True);row['pid']=child.pid;deadline=time.monotonic()+seconds
   while child.poll() is None:
    observe(child);assert out.tell()<=16*1024**2 and err.tell()<=16*1024**2,'stage stream bound'
    if time.monotonic()>=deadline:row['timed_out']=True;raise TimeoutError(name)
    time.sleep(.25)
   row['original_returncode']=child.wait()
  if check:assert row['original_returncode']==0,name
  return Path(str(stem)+'.stdout').read_text()
 except BaseException as exc:
  row['error']=type(exc).__name__+': '+str(exc)
  if child:
   try:row['forced_cleanup']=reap(active=child)
   finally:row['original_returncode']=child.wait(timeout=3)
  raise
 finally:write(Path(str(stem)+'.exit.json'),row)
def free(port):
 with socket.socket() as sock:sock.bind(('127.0.0.1',port))
def backend_identity(backend):
 if backend=='s3':
  obj=json.loads(call('s3-identity',['docker','inspect',C['minio_name']],15,backend))[0]
  assert obj['Name']=='/'+C['minio_name'] and obj['Image']==C['minio_image'] and obj['State']['Running']
  assert obj['HostConfig']['PortBindings']=={'9000/tcp':[{'HostIp':'127.0.0.1','HostPort':'9012'}]}
  row={k:obj[k] for k in ['Id','Name','Image','State','Mounts']}
 else:
  pidfile=R/'cloud'/backend/('webdav.pid' if backend=='webdav' else 'sftp/sftp.pid');row=proc(int(pidfile.read_text()));assert row and managed(row)==backend
 old=result['backend_owners'].get(backend)
 if old:assert (row['Id']==old['Id'] if backend=='s3' else row['pid']==old['pid'] and row['start_ticks']==old['start_ticks'])
 result['backend_owners'][backend]=row;return row

def report(backend,required):
 reports=list((R/'artifacts'/backend/'rocknix-images').glob('qa-*/report.md'));assert len(reports)==1
 p=reports[0];text=p.read_text();assert text.startswith('# vm-qa on '+C['commit'][:10]+'\n')
 rows=[]
 for line in text.splitlines():
  parts=[x.strip() for x in line.split('|')]
  if len(parts)==6 and parts[1] in STANDARD:rows.append({'suite':parts[1],'result':parts[2],'time':parts[3],'log':parts[4]})
 assert [r['suite'] for r in rows]==required and all(r['result']=='PASS' for r in rows),'required original suite row failed/skipped/missing'
 assert '**PASSED** -- every suite that ran passed.' in text
 if 'round-trip' in required:
  rt=p.with_name('round-trip.log').read_text();assert not re.search(r'WARN.*clean-?up incomplete',rt,re.I),'round-trip original cleanup warning'
  assert "scratch tree and bucket emptied; the device's own remote, paths and settings-backup setting restored" in rt
 result['reports'].append({'backend':backend,'path':str(p),'sha256':sha(p),'rows':rows})
def expire(_sig,_frame):raise TimeoutError('whole owner deadline or termination')
signal.signal(signal.SIGALRM,expire);signal.signal(signal.SIGINT,expire);signal.signal(signal.SIGTERM,expire);signal.alarm(C['work_seconds'])
try:
 assert hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal')
 libc=ctypes.CDLL(None,use_errno=True);assert libc.prctl(36,1,0,0,0)==0
 flag=ctypes.c_int();assert libc.prctl(37,ctypes.byref(flag),0,0,0)==0 and flag.value==1
 assert Path('/proc/self/ns/pid').stat().st_ino==C['host_pid_namespace']
 run=Path(os.environ['RASTERATOPS_BUILD_RUN']);run=run if run.is_absolute() else TREE/run
 assert run.parent==TREE/'.build-runs';admission=json.loads((run/'admission.json').read_text());assert admission['source']['head']==C['commit'] and admission['submission_owner']==str(R/'lifecycle-owner')
 (R/'run.path').write_text(str(run)+'\n');write(R/'records/owner.json',{'owner':proc(os.getpid()),'watcher':proc(int((run/'watcher.pid').read_text())),'run':str(run),'subreaper':True})
 for p,h in C['dependencies'].items():assert sha(Path(p))==h,p
 for n,h in C['code'].items():assert sha(R/n)==h,n
 for n,target in C['harness_links'].items():assert (R/n).is_symlink() and os.readlink(R/n)==target,n
 assert sha(R/'records/image-verification.original.json')==C['verification_sha256'] and sha(R/'records/image-inputs.original.json')==C['image_inputs_sha256']
 for path,commit in [(TREE,C['commit']),(Path(C['es_source']),C['es_commit'])]:
  assert call('source-identity',['git','-C',path,'rev-parse','HEAD'],15).strip()==commit
  assert not call('source-clean',['git','-C',path,'status','--porcelain=v1','--untracked-files=no'],15).strip()
 for p in Path('/proc').iterdir():
  if p.name.isascii() and p.name.isdigit():
   row=proc(int(p.name));assert not (row and row['argv'] and Path(row['argv'][0]).name.startswith('qemu-system-')),'existing guest: root must serialize standard allocation'
 for port in [10022,10023,5909,5910,9010,9011,9012,9013]:free(port)
 for port in [10022,10023]:
  call('preexisting-ssh-master-'+str(port),['ssh','-p',str(port),'-o','ControlPath=/tmp/crt-'+str(os.getuid())+'-%C','-O','check','root@127.0.0.1'],10,check=False)
  assert result['commands'][-1]['original_returncode']!=0,'existing SSH master at reserved pair address'
 containers=call('existing-containers',['docker','ps','-a','--format','{{.Names}}'],20).splitlines();assert C['minio_name'] not in containers
 im=json.loads(call('local-minio-image',['docker','image','inspect',C['minio_image']],20))[0];assert im['Id']==C['minio_image']
 result['prior_docker_volumes']=call('existing-volumes',['docker','volume','ls','--format','{{.Name}}'],15).splitlines()
 write(R/'records/minio-local-image.json',{k:im[k] for k in ['Id','RepoDigests','Created']})
 call('host-rclone-version',['rclone','version'],15)
 image=Path(C['image']['path']);assert image.stat().st_size==C['image']['bytes'] and sha(image)==C['image']['sha256']
 pair_attempted=True;call('pair-up',[TREE/'tools/vm-pair','up',image],C['bounds_seconds']['pair-up'])
 for g,suffix in [('a',''),('b','-b')]:
  row=proc(int((R/'runtime'/('rocknix-qemu'+suffix+'.pid')).read_text()));assert row and managed(row)=='qemu'
  args=row['argv'];assert args[args.index('-m')+1]=='8192' and args[args.index('-smp')+1]=='4' and '-append' not in args and '-kernel' not in args
  assert 'if=none,id=rocknix,format=qcow2,file='+str(R/'pair'/('vm-'+g+'.qcow2')) in args
  result['qemu'].append(row)
  identity=call('guest-'+g+'-identity',[TREE/'tools/vm-pair','ssh',g,'cat /etc/os-release; cat /proc/sys/kernel/random/boot_id'],20)
  assert 'BUILD_ID="'+C['commit']+'"' in identity
 for backend in ['webdav','sftp','s3']:
  attempted.append(backend)
  call(backend+'-up',[TREE/'tools/cloud-test-backend','up'],C['bounds_seconds']['backend-up'],backend);backend_identity(backend)
  qa=R/'harness/tools/vm-qa' if backend=='webdav' else TREE/'tools/vm-qa'
  args=[qa,'--skip-up','--only','scripts' if backend=='webdav' else 'round-trip']
  if backend!='webdav':args+=['--backend',backend]
  args.append(image)
  call('standard' if backend=='webdav' else backend,args,C['bounds_seconds']['standard' if backend=='webdav' else backend],backend)
  backend_identity(backend);report(backend,['scripts'] if backend=='webdav' else ['round-trip'])
 assert sha(image)==C['image']['sha256']
 for path,commit in [(TREE,C['commit']),(Path(C['es_source']),C['es_commit'])]:
  assert call('source-after',['git','-C',path,'rev-parse','HEAD'],15).strip()==commit
  assert not call('source-clean-after',['git','-C',path,'status','--porcelain=v1','--untracked-files=no'],15).strip()
 for p,h in C['dependencies'].items():assert sha(Path(p))==h,p
 for n,h in C['code'].items():assert sha(R/n)==h,n
 for n,target in C['harness_links'].items():assert (R/n).is_symlink() and os.readlink(R/n)==target,n
 result['rc']=0
except BaseException as exc:result['error']=type(exc).__name__+': '+str(exc)
finally:
 signal.alarm(C['cleanup_seconds'])
 try:
  # cloud-round-trip's accepted ControlPersist connection is closed normally.
  # These exact key/host/ports belong to this fresh pair; nonzero means already gone.
  if pair_attempted and (R/'pair/qa-key').exists():
   for port in [10022,10023]:
    try:call('ssh-master-exit-'+str(port),['ssh','-i',R/'pair/qa-key','-p',str(port),'-o','BatchMode=yes','-o','ControlPath=/tmp/crt-'+str(os.getuid())+'-%C','-O','exit','root@127.0.0.1'],10,check=False)
    except BaseException as exc:result['cleanup_errors'].append('SSH master: '+str(exc))
  for backend in reversed(attempted):
   try:
    # Helpers retain their original down behavior. Scope its numeric PID/port
    # sweep to the private owner before invoking it; never stop a shared endpoint.
    if backend=='s3':
     names=call('s3-pre-down-list',['docker','ps','-a','--format','{{.Names}}'],15,backend).splitlines()
     if C['minio_name'] in names:
      obj=json.loads(call('s3-pre-down-identity',['docker','inspect',C['minio_name']],15,backend))[0]
      assert obj['Image']==C['minio_image'] and (not result['backend_owners'].get('s3') or obj['Id']==result['backend_owners']['s3']['Id'])
      result['s3_final_mounts']=obj['Mounts']
    else:
     pidfile=R/'cloud'/backend/('webdav.pid' if backend=='webdav' else 'sftp/sftp.pid')
     if pidfile.exists():
      current=proc(int(pidfile.read_text()))
      if current:assert managed(current)==backend
     port=9010 if backend=='webdav' else 9013
     listeners=call(backend+'-listeners',['ss','-ltnp','sport','=',':'+str(port)],10,backend)
     for pid in re.findall(r'pid=(\d+)',listeners):assert managed(proc(int(pid)) or {})==backend,'foreign backend listener'
     if len(listeners.strip().splitlines())>1:assert re.search(r'pid=\d+',listeners),'listener ownership unavailable'
    call(backend+'-down',[TREE/'tools/cloud-test-backend','down'],C['bounds_seconds']['backend-down'],backend)
    if backend=='s3':
     for mount in result.get('s3_final_mounts',[]):
      assert mount['Type']=='volume' and mount['Name'] not in result['prior_docker_volumes'],'refuse shared/non-volume backend data retirement'
      call('retire-owned-s3-volume',['docker','volume','rm',mount['Name']],15,backend)
   except BaseException as exc:result['cleanup_errors'].append(backend+' stop: '+str(exc))
  if pair_attempted:
   try:call('pair-down',[TREE/'tools/vm-pair','down'],C['bounds_seconds']['pair-down'])
   except BaseException as exc:result['cleanup_errors'].append('pair stop: '+str(exc))
  try:
   reap();result['remaining_children']=direct_children(os.getpid())
   if result['remaining_children']:result['cleanup_errors'].append('remaining owned children')
   for port in [10022,10023,5909,5910,9010,9011,9012,9013]:free(port)
   names=call('final-container-list',['docker','ps','-a','--format','{{.Names}}'],15).splitlines();assert C['minio_name'] not in names
   result['backend_name_absent']=True
  except BaseException as exc:result['cleanup_errors'].append('final ownership check: '+str(exc))
 except BaseException as exc:result['cleanup_errors'].append('cleanup deadline: '+str(exc))
 finally:
  signal.alarm(0);result['surviving_owned_processes']=[r for r in owned.values() if same(r)]
  result['qemu_still_live']=[r for r in result['qemu'] if same(r)]
  if result['cleanup_errors'] or result.get('forced_child_cleanup') or result['surviving_owned_processes'] or result['qemu_still_live']:result['rc']=1
  result['ended']=time.time();write(R/'records/process-identities.json',list(owned.values()));write(R/'result.json',result)
raise SystemExit(result['rc'])
