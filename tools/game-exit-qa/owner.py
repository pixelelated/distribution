#!/usr/bin/env python3
"""1800s watched host owner; no launch before frozen inputs + actual standing-slot activation/admission."""
import argparse,ctypes,datetime,fcntl,json,os,resource,shutil,signal,socket,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True;sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import Context,identity,load,now,parse_utc,same,sha,terminate,verify_inputs,write

from activation import check_activation
import menu_timing as T
import re

def headless_audio(argv):
 """One host discard backend; keep the existing guest HDA device and all other argv."""
 assert isinstance(argv,list) and all(isinstance(x,str) for x in argv)
 assert not any(x.lstrip('-').split('=',1)[0] in ('audiodev','audio','soundhw') or 'audiodev=' in x for x in argv),'pre-existing audio backend refused'
 codecs=[i for i,x in enumerate(argv) if x.split(',',1)[0]=='hda-duplex']
 assert len(codecs)==1,'exactly one hda-duplex required'
 i=codecs[0];assert i>0 and argv[i-1]=='-device' and argv[i]=='hda-duplex','unexpected codec properties refused'
 result=list(argv);result[i]='hda-duplex,audiodev=m7headless'
 result[i-1:i-1]=['-audiodev','none,id=m7headless']
 assert result.count('-audiodev')==1 and result.count('hda-duplex,audiodev=m7headless')==1
 return result

def harness(ctx,o):
 # Final argv and actual VARS exist. Preserve collector stdout and original rc.
 for name,flag,path in [('harness-capture','--spec',o/'harness-spec.json'),
                        ('harness-prelaunch','--check',o/'records/harness-capture.log')]:
  ctx.command(name,['/usr/bin/python3','-I','-B',ctx.c['tools']['manifest'],flag,str(path)],25)
 assert json.loads((o/'records/harness-capture.log').read_text())['status']=='IDENTITIES_READY'
 assert json.loads((o/'records/harness-prelaunch.log').read_text())['status']=='UNCHANGED'

def worker(o):
 ctx=Context(o,'owner');c=ctx.c;q=None;qi=None;result={'status':'FAIL','scope':'1433-armed-exit','cleanup':[]};began=time.monotonic();handled=[]
 def expire(s,f):raise TimeoutError('worker time budget or signal '+str(s))
 for sig in (signal.SIGTERM,signal.SIGINT,signal.SIGALRM):signal.signal(sig,expire)
 signal.alarm(T.WORKER_MAX)
 try:
  assert sha(o/'config.json')==(o/'config.sha256').read_text().strip();assert not sys.flags.optimize;verify_inputs(o,c)
  os.environ['TMPDIR']=str(o/'tmp');os.environ['PYTHONDONTWRITEBYTECODE']='1'
  run=Path(c['checkout'])/os.environ['RASTERATOPS_BUILD_RUN'];assert run.parent==Path(c['checkout'])/'.build-runs' and run.resolve()==run
  assert (run/'admission.json').is_file() and not (run/'build.rc').exists() and time.time()-(run/'build.status').stat().st_mtime<90
  admitted=json.loads((run/'admission.json').read_text());receipt=json.loads((run/'admission-input.json').read_text())
  assert admitted['state']=='running' and 0<=time.time()-parse_utc(admitted['admitted'])<900 and 0<=time.time()-parse_utc(receipt['utc'])<900
  assert admitted['id']==receipt['id'] and admitted['checkout']==c['checkout'] and any(x['path']==str(o) for x in admitted['outputs'])
  assert admitted['submission_owner'] is None and 'PIXELELATED_SUBMISSION_OWNER' not in os.environ and admitted['run']==str(run)
  sup=json.loads((o/'owner-start.json').read_text());assert os.getppid()==sup['identity']['pid'] and same(sup['identity']) and admitted['runner_pid']==sup['parent']
  assert identity(sup['parent'])['start_ticks']==admitted['runner_start'] and sha(o/'admission.json')==admitted['receipt_sha256']
  activation=check_activation(o,c)
  current=time.monotonic()
  work_remaining=int(T.work_remaining(current,began,activation['deadline_monotonic']))
  assert work_remaining > 0, 'no worker budget before reserved retirement'
  work_deadline=current+work_remaining
  signal.alarm(work_remaining)
  memory=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
  fs=os.statvfs(o);free=fs.f_bavail*fs.f_frsize
  write(o/'launch-preconditions.json',{'utc':now(),'mem_available_bytes':memory,'available_disk_bytes':free,'activation':activation,'admission_id':admitted['id'],'watch_run':str(run)},True)
  assert memory>=c['min_mem_available_bytes'] and free>=c['min_disk_headroom_bytes']
  (o/'vm').mkdir(mode=0o700) # Absent through slot request; created only inside validated activation.
  assert not list((o/'vm').iterdir()),'fresh VM directory required'
  assert str(Path(sys.executable).resolve())==c['host_inputs']['python']
  assert str(Path(shutil.which('qemu-img')).resolve())==c['host_inputs']['qemu_img']
  assert len(os.fsencode(o/'vm/display.sock'))<=107
  assert work_deadline-time.monotonic()>T.BOOT_RESERVE+T.WORK, 'no full boot, review and archive budget before QEMU'
  ctx.command('materialize-fresh-image',[sys.executable,'-I','-B',str(o/'code/materialize.py'),str(o)],300)
  os.environ['QEMU_SYSTEM_X86_64']=c['host_inputs']['qemu'];os.environ['TMPDIR']=str(o/'tmp')
  assert os.access('/dev/kvm',os.R_OK|os.W_OK),'standing functional owner requires KVM'
  vm=load(c['tools']['vm'],'m7_vm');parser=argparse.ArgumentParser();vm.add_qemu_options(parser)
  args=parser.parse_args(['--headless','--accel','kvm','--ovmf-code',c['host_inputs']['ovmf_code'],'--ovmf-vars-template',c['host_inputs']['ovmf_vars_template'],'--net','none','--gl','none','--res','640x480','--monitor',str(o/'vm/m.sock'),'--serial',str(o/'vm/s.sock'),'--pidfile',str(o/'vm/qemu.pid'),'--ovmf-vars',str(o/'vm/vars.fd'),'--vnc',str(c['vnc']),str(o/'vm/disk.qcow2')])
  profile=vm.load_profile();assert profile['cpu_count']==4 and profile['memory_mib']==8192
  vm.prepare_run(profile,args);argv=vm.qemu_command(profile,args)+['-drive','if=none,id=m7prep,format=raw,readonly=on,file='+str(o/'payload.tar'),'-device','virtio-blk-pci,drive=m7prep,serial=M7BOOTPREP']
  # Keep headless scanout while replacing the unused TCP listener.
  assert argv.count('-vnc')==1
  display=argv.index('-vnc')+1
  assert argv[display]=='127.0.0.1:'+str(c['vnc'])
  argv[display]='unix:'+str(o/'vm/display.sock')
  argv=headless_audio(argv)
  assert str(Path(argv[0]).resolve())==c['host_inputs']['qemu']
  assert '-netdev' not in argv and any(argv[i:i+2]==['-nic','none'] for i in range(len(argv)-1))
  assert not any('hostfwd=' in x or 'netdev=' in x for x in argv)
  write(o/'qemu-argv.json',argv,True)
  harness(ctx,o)
  if c.get('near_minute'):
   # One bounded wait before launch for the clock rollover qualification.
   # Recheck the original pre-QEMU work reserve after waiting.
   target=(int(time.time())//60+1)*60-5
   time.sleep(max(0,target-time.time()))
  # Existing child inherits the file-size ceiling before it can write.
  previous=resource.getrlimit(resource.RLIMIT_FSIZE)
  cap=c['overlay_file_ceiling_bytes']
  assert cap==768*1024**2 and all(x==resource.RLIM_INFINITY or x>=cap for x in previous)
  assert work_deadline-time.monotonic()>T.BOOT_RESERVE+T.WORK, 'no full boot, review and archive budget before QEMU'
  ctx.set('booting-no-NIC')
  resource.setrlimit(resource.RLIMIT_FSIZE,(cap,previous[1]))
  try:q,qi=ctx.spawn(argv,o/'records/qemu.log')
  finally:resource.setrlimit(resource.RLIMIT_FSIZE,(1024**2,previous[1]))
  wall=time.time_ns()
  if c.get('near_minute'):
   phase=wall%(60*T.NS)
   distance=min(phase,60*T.NS-phase)
   write(o/'records/minute-boundary.json',{'utc':now(),'host_wall_ns':wall,
       'distance_ns':distance,'qemu_pid':q.pid},True)
   assert distance<=10*T.NS, 'actual QEMU launch missed the requested minute boundary'
  write(o/'qemu-identity.json',qi,True)
  deadline=time.monotonic()+180;ready=False;attempt=0
  while time.monotonic()<deadline and attempt<32:
   assert q.poll() is None,'QEMU exited during boot';attempt+=1
   try:
    body,rc=ctx.serial('boot-'+str(attempt),'test -f /storage/.config/system/configs/system.cfg && pgrep emulationstation >/dev/null',4)
    if rc==0:ready=True;break
   except (OSError,TimeoutError):pass
   time.sleep(2)
  assert ready and int((o/'vm/qemu.pid').read_text())==q.pid
  from workflow import execute
  execute(ctx,q,o,work_deadline,admitted)
  result['status']='PASS_SCOPED_OWNER'
  result['phase']=c['phase']
  result['acceptance']='automatic scoped originals only; root retains frame/readback/final acceptance'
 except BaseException as e:result['error']=type(e).__name__+': '+str(e)
 finally:
  # Cleanup is reserved inside the independent1800s supervisor budget.
  signal.alarm(0);ctx.set('exact-owned-QEMU-cleanup')
  if q is not None:
   try:
    if q.poll() is None and result['status']=='PASS_SCOPED_OWNER':
     poweroff_rc=None
     try:_,poweroff_rc=ctx.serial('normal-poweroff','sync && systemctl poweroff',3)
     except OSError as e:result['cleanup'].append({'poweroff_transport_error':str(e)})
     result['cleanup'].append({'poweroff_shell_rc':poweroff_rc,'note':'None is unknown transport outcome, never rewritten zero'})
     try:q.wait(timeout=40)
     except subprocess.TimeoutExpired:
      result['status']='FAIL';result['cleanup'].append({'normal_shutdown_timeout':True})
    if q.poll() is None:
     pf=o/'vm/qemu.pid';assert same(qi) and pf.is_file() and pf.read_text().strip()==str(q.pid),'pidfile must name the recorded child'
     ctx.command('exact-vm-stop',[sys.executable,'-I','-B',c['tools']['stop'],'--timeout','35',str(o/'vm/qemu.pid'),str(o/'vm/disk.qcow2')],40)
    q.wait(timeout=5)
   except BaseException as e:
    result['status']='FAIL';result['cleanup'].append({'error':str(e)})
    if q.poll() is None and same(qi):
     # Popen child identity is independently recorded even if QEMU failed
     # before producing its own pidfile. Never match/kill by argv pattern.
     handle=os.pidfd_open(q.pid)
     try:signal.pidfd_send_signal(handle,signal.SIGKILL);q.wait(timeout=5)
     finally:os.close(handle)
     result['cleanup'].append({'forced_owned_QEMU_kill':True})
   result['qemu_original_wait']=q.returncode
   if q.returncode!=0:result['status']='FAIL'
   pidfile=o/'vm/qemu.pid'
   if pidfile.exists():
    if pidfile.read_text().strip()==str(q.pid) and not same(qi):pidfile.unlink()
    else:result['status']='FAIL';result['cleanup'].append({'pidfile':'retained: identity not proved absent'})
   result['cleanup'].append({'owned_qemu_gone':not same(qi),'pidfile_absent':not pidfile.exists()})
  result['elapsed_seconds']=time.monotonic()-began;write(o/'worker-result.json',result,True);ctx.close()
 return 0 if result['status']=='PASS_SCOPED_OWNER' else 1

def supervisor(o):
 o=Path(o).resolve(strict=True);lock=(o/'owner.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 parent=os.getppid();lib=ctypes.CDLL(None,use_errno=True);assert lib.prctl(1,signal.SIGTERM)==0 and os.getppid()==parent
 def interrupted(s,f):raise RuntimeError('supervisor interrupted '+str(s))
 for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,interrupted)
 ctx=Context(o,'supervisor');p=None;ident=None;result={'status':'FAIL','hard_budget_seconds':1800};started=time.monotonic()
 try:
  activation=check_activation(o,ctx.c)
  write(o/'owner-start.json',{'utc':now(),'identity':identity(os.getpid()),'parent':parent},True)
  p,ident=ctx.spawn([sys.executable,'-I','-B',str(o/'code/owner.py'),'--worker',str(o)],o/'records/worker.log')
  #1770s then8s TERM+5s KILL reserves time for original-result publication.
  remaining=min(1770-(time.monotonic()-started),activation['deadline_monotonic']-time.monotonic()-20);assert remaining>0
  try:p.wait(timeout=remaining)
  except subprocess.TimeoutExpired:result['watchdog_timeout']=True;terminate(p,ident)
  result['original_worker_returncode']=p.returncode
  if p.returncode==0 and not result.get('watchdog_timeout') and json.loads((o/'worker-result.json').read_text())['status']=='PASS_SCOPED_OWNER':result['status']='PASS_SCOPED_OWNER'
 except BaseException as e:result['error']=type(e).__name__+': '+str(e)
 finally:
  if p is not None and p.poll() is None:terminate(p,ident)
  if p is not None:result['original_worker_returncode']=p.returncode
  # Worker death triggers QEMU PDEATHSIGKILL. Prove recorded identity absent;
  # never invent cleanup success when the worker result is missing.
  qrecord=o/'qemu-identity.json'
  if qrecord.exists():
   qi=json.loads(qrecord.read_text());until=time.monotonic()+5
   while same(qi) and time.monotonic()<until:time.sleep(.1)
   result['owned_qemu_identity_absent']=not same(qi)
   if same(qi):result['status']='FAIL'
   pf=o/'vm/qemu.pid'
   if pf.exists() and pf.read_text().strip()==str(qi['pid']) and not same(qi):pf.unlink()
  result['elapsed_seconds']=time.monotonic()-started;write(o/'owner-result.json',result,True);(o/'owner.rc').write_text(str(0 if result['status']=='PASS_SCOPED_OWNER' else 1)+'\n');ctx.close()
 return 0 if result['status']=='PASS_SCOPED_OWNER' else 1
if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='--worker':sys.exit(worker(Path(sys.argv[2])))
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--owner',type=Path,required=True);args=parser.parse_args();sys.exit(supervisor(args.owner))
