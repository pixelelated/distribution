"""Owned host process/serial utilities; no action at import."""
import base64,datetime,fcntl,hashlib,importlib.machinery,importlib.util,json,os,signal,subprocess,sys,threading,time,uuid,shlex
from pathlib import Path
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def write(p,v,exclusive=False):
 p=Path(p);raw=json.dumps(v,indent=2)+'\n'
 if exclusive:
  with p.open('x') as f:f.write(raw)
 else:
  t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.new');t.write_text(raw);t.replace(p)
def identity(pid):
 p=Path('/proc')/str(pid);s=(p/'stat').read_text().rsplit(')',1)[1].split()
 return {'pid':pid,'start_ticks':s[19],'state':s[0],'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
def same(i):
 try:return all(identity(i['pid'])[k]==i[k] for k in ('pid','start_ticks','boot_id'))
 except (FileNotFoundError,ProcessLookupError):return False
def terminate(proc,ident):
 if proc.poll() is not None:return False
 if not same(ident):raise RuntimeError('process identity changed; refuse signal')
 # Only a session this code created; recheck leader identity before signalling.
 os.killpg(proc.pid,signal.SIGTERM)
 try:proc.wait(timeout=8)
 except subprocess.TimeoutExpired:
  if not same(ident):raise RuntimeError('identity changed before KILL')
  os.killpg(proc.pid,signal.SIGKILL);proc.wait(timeout=5)
 return True
def load(path,name):
 loader=importlib.machinery.SourceFileLoader(name,str(path));spec=importlib.util.spec_from_loader(name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m);return m
class Context:
 def __init__(self,owner,kind):
  self.o=Path(owner);self.c=json.loads((self.o/'config.json').read_text());self.kind=kind;self.phase='starting';self.stop=threading.Event();self.started=time.monotonic();self.serial_api=None
  self.thread=threading.Thread(target=self.heartbeat,daemon=True);self.thread.start()
 def heartbeat(self):
  while not self.stop.is_set():
   row={'utc':now(),'kind':self.kind,'pid':os.getpid(),'phase':self.phase,'elapsed_seconds':round(time.monotonic()-self.started,3),'note':'host liveness only; no guest poll and no success inference'}
   write(self.o/(self.kind+'-progress.json'),row);print(json.dumps(row),flush=True);self.stop.wait(30)
 def set(self,p):
  self.phase=p;row={'utc':now(),'kind':self.kind,'pid':os.getpid(),'phase':p,'note':'host phase transition only'}
  write(self.o/(self.kind+'-progress.json'),row);print(json.dumps(row),flush=True)
 def close(self):self.stop.set();self.thread.join(2)
 def spawn(self,argv,log):
  f=Path(log).open('xb',buffering=0)
  try:
   p=subprocess.Popen([sys.executable,'-I','-B',str(self.o/'code/pdeath.py'),str(os.getpid()),*map(str,argv)],stdout=f,stderr=subprocess.STDOUT,start_new_session=True,stdin=subprocess.DEVNULL,close_fds=True)
  finally:f.close()
  i=identity(p.pid);write(Path(str(log)+'.pid.json'),i,True);return p,i
 def command(self,name,argv,seconds):
  self.set(name);p,i=self.spawn(argv,self.o/'records'/(name+'.log'));forced=False;timed=False
  try:
   try:p.wait(timeout=seconds)
   except subprocess.TimeoutExpired:timed=True;forced=terminate(p,i)
  finally:
   if p.poll() is None:forced=terminate(p,i)
   row={'argv':list(map(str,argv)),'original_returncode':p.returncode,'timed_out':timed,'forced_cleanup':forced,'identity':i}
   write(self.o/'records'/(name+'.json'),row,True)
  if timed or forced or p.returncode:raise RuntimeError(name+' failed; original result retained')
  return row
 def serial(self,name,cmd,seconds=30):
  # All owner/child console use shares an exclusive flock; timeout cannot
  # become a successful command because the serial tool returned an END marker.
  if self.serial_api is None:self.serial_api=load(self.c['tools']['serial'],'m7_serial')
  lock=(self.o/'serial.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  tag='M7RC'+uuid.uuid4().hex;client=None;raw='';ok=False;rc=None
  self.set(name)
  try:
   client=self.serial_api.Serial(str(self.o/'vm/s.sock'),seconds)
   encoded=base64.b64encode(cmd.encode()).decode()
   raw,ok=client.run('( printf %s '+shlex.quote(encoded)+' | base64 -d | /bin/sh ); m7_child_rc=$?; printf "\\n'+tag+':%s\\n" "$m7_child_rc"')
   lines=raw.splitlines();found=[x for x in lines if x.startswith(tag+':')]
   if ok and len(found)==1:rc=int(found[0].split(':',1)[1])
   body='\n'.join(x for x in lines if not x.startswith(tag+':'))
   return body,rc
  finally:
   if client:client.close()
   lock.close()
   (self.o/'records'/(name+'.serial')).write_text(raw)
   write(self.o/'records'/(name+'.serial.json'),{'completed_transport':ok,'original_guest_rc':rc,'command':cmd,'utc':now()},True)
 def serial_ok(self,name,cmd,seconds=30):
  body,rc=self.serial(name,cmd,seconds)
  if rc!=0:raise RuntimeError(name+' guest rc '+str(rc))
  return body
 def readiness(self,name):
  return json.loads(self.serial_ok(name,'python3 -I -B '+shlex.quote(self.c['guest_root']+'/guest-guard.py')+' installed',45))
def verify_inputs(o,c):
 for p,h in c['inputs'].items():
  if sha(p)!=h:raise RuntimeError('changed frozen input: '+p)
 for rel,h in c['owner_files'].items():
  if sha(Path(o)/rel)!=h:raise RuntimeError('changed owner file: '+rel)
def parse_utc(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
