#!/usr/bin/env python3
"""UNRUN. Three installed Dolphin startup observations in an allocated no-NIC guest."""
import hashlib,http.server,json,os,signal,struct,subprocess,sys,threading,time,urllib.parse
from pathlib import Path
R=Path('/run/pix-installed-native');PACKET=Path(__file__).resolve().parent
USER='m7_synthetic_only';TOKEN='_'.join(('m7','synthetic','invalid'));PORT=8080

def require(ok,why):
 if not ok:raise AssertionError(why)
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def identity(pid):
 p=Path('/proc')/str(pid);s=(p/'stat').read_text().rsplit(')',1)[1].split()
 return {'pid':pid,'start_ticks':int(s[19]),'exe':os.readlink(p/'exe'),'exe_sha256':sha(p/'exe'),'cpu_ticks':int(s[11])+int(s[12]),'tasks':[{'tid':int(t.name),'comm':(t/'comm').read_text().strip()} for t in sorted((p/'task').iterdir())]}
def census():
 out=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:
   exe=os.readlink(p/'exe')
   if Path(exe).name.startswith('dolphin-emu'):out.append(identity(int(p.name)))
  except (FileNotFoundError,ProcessLookupError):continue
 return out
class Endpoint(http.server.HTTPServer):
 allow_reuse_address=True
 def __init__(self):
  super().__init__(('127.0.0.1',PORT),Handler);self.timeout=.1;self.records=[];self.errors=[];self.stop=threading.Event();self.thread=threading.Thread(target=self.loop,name='synthetic-loopback')
 def loop(self):
  try:
   while not self.stop.is_set():self.handle_request()
  except BaseException as e:self.errors.append(repr(e))
 def close(self):
  self.stop.set();self.thread.join(timeout=3);require(not self.thread.is_alive(),'endpoint thread survived');self.server_close()
class Handler(http.server.BaseHTTPRequestHandler):
 def setup(self):super().setup();self.connection.settimeout(2)
 def log_message(self,*args):pass
 def do_POST(self):
  try:
   n=int(self.headers.get('Content-Length','0'));require(0<n<=8192,'request size')
   body=self.rfile.read(n);require(len(body)==n,'short request')
   form=urllib.parse.parse_qs(body.decode('ascii'),strict_parsing=True)
   self.server.records.append({'path':self.path,'method':'POST','host':self.headers.get('Host'),'form':form,'peer':self.client_address[0],'monotonic':time.monotonic()})
   require(len(self.server.records)<=4,'unexpected request storm')
   data=b'{"Success":false,"Error":"Synthetic endpoint only"}'
   self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
  except BaseException as e:self.server.errors.append(repr(e));self.close_connection=True

def observe(name,binary,enabled,badboot=False):
 case=R/name;case.mkdir();user=case/'user';config=user/'Config';config.mkdir(parents=True)
 (config/'RetroAchievements.ini').write_text('[Achievements]\nEnabled = '+str(enabled)+'\nHostUrl = 127.0.0.1:8080\nUsername = '+USER+'\nApiToken = '+TOKEN+'\nHardcoreEnabled = False\n')
 (config/'Logger.ini').write_text('[Options]\nWriteToFile = True\nWriteToConsole = True\nVerbosity = 4\n[Logs]\nRetroAchievements = True\nBOOT = True\nCORE = True\nCONSOLE = True\n')
 (config/'Dolphin.ini').write_text('[Core]\nCPUThread = True\nCPUCore = 0\nSlotA = 255\nSlotB = 255\n[Analytics]\nEnabled = False\nPermissionAsked = True\n[DSP]\nBackend = No Audio Output\n')
 before={str(p.relative_to(user)):sha(p) for p in config.iterdir()};write(case/'config-before.json',before)
 game=R/('absent-file.iso' if badboot else 'loop.dol');require(not game.exists() if badboot else game.exists(),'wrong boot fixture')
 argv=[str(binary),'-p','headless','-v','Null','-a','HLE','-u',str(user),'-e',str(game)]
 row={'case':name,'status':'FAIL','argv':argv,'binary_sha256':sha(binary),'enabled':enabled,'badboot':badboot,'signals':[],'original_exit':None}
 server=None;child=None;pidfd=None;started=time.monotonic()
 try:
  require(census()==[],'Dolphin already running');server=Endpoint();server.thread.start()
  with (case/'stdout').open('xb') as out,(case/'stderr').open('xb') as err:
   child=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
   pidfd=os.pidfd_open(child.pid);row['pid']=child.pid
   if badboot:
    row['original_exit']=child.wait(timeout=8)
   else:
    deadline=time.monotonic()+15;live=None
    while time.monotonic()<deadline:
     require(child.poll() is None,'Dolphin exited before running')
     live=identity(child.pid)
     if any(t['comm']=='CPU thread' for t in live['tasks']):break
     time.sleep(.1)
    require(live and any(t['comm']=='CPU thread' for t in live['tasks']),'no successful CPU thread')
    row['running_before']=live
    # Positive running interval also bounds the disabled absence observation.
    until=time.monotonic()+2
    while time.monotonic()<until:
     require(child.poll() is None,'Dolphin exited during running observation');time.sleep(.1)
    row['running_after']=identity(child.pid)
    require(row['running_after']['start_ticks']==live['start_ticks'] and row['running_after']['exe_sha256']==row['binary_sha256'],'process/executable changed')
    require(row['running_after']['cpu_ticks']>live['cpu_ticks'],'CPU time did not advance')
    require(not server.errors,'endpoint failed')
    signal.pidfd_send_signal(pidfd,signal.SIGTERM);row['signals'].append('normal SIGTERM');row['original_exit']=child.wait(timeout=8)
  stderr=(case/'stderr').read_text(errors='replace')
  row['badge_load_failures']={message:stderr.count(message) for message in BADGE_FAILURES}
  require(not any(row['badge_load_failures'].values()),'original stderr contains a prior badge-load failure')
  text=stderr+(case/'stdout').read_text(errors='replace')
  row['initialized']=text.count('Achievement Manager Initialized')
  row['shutdown']=text.count('Achievement Manager shut down.')
  row['boot_error']='Could not boot the specified file' in text
  row['requests']=server.records
  require(row['original_exit']==(1 if badboot else 0),'unexpected original exit')
  if enabled:
   require(row['initialized']==row['shutdown']==1,'missing or duplicate lifecycle')
   if badboot:require(row['boot_error'],'not the BootCore failure path')
   else:require(len(row['requests'])==1,'expected one synthetic startup login')
   # Failed boot can cancel the queued login before dispatch; lifecycle, not an HTTP count, is its criterion.
   require(len(row['requests'])<=1,'duplicate startup request')
   for req in row['requests']:
    require(req['method']=='POST' and req['path']=='/dorequest.php' and req['host']=='127.0.0.1:8080' and req['peer']=='127.0.0.1','wrong HTTP destination')
    require(req['form'].get('r')==['login2'] and req['form'].get('u')==[USER] and req['form'].get('t')==[TOKEN],'wrong synthetic login')
  else:require(not row['initialized'] and not row['shutdown'] and not row['requests'],'disabled achievements started')
  row['status']='PASS'
 except BaseException as e:row['error']=repr(e)
 finally:
  if child and child.poll() is None:
   row['status']='FAIL';row['signals'].append('forced SIGKILL cleanup')
   if pidfd is not None:signal.pidfd_send_signal(pidfd,signal.SIGKILL)
   else:child.kill()
   row['original_exit']=child.wait(timeout=3)
  if pidfd is not None:os.close(pidfd)
  if server:
   row['requests']=server.records;row['endpoint_errors']=server.errors
   try:server.close()
   except BaseException as e:row['status']='FAIL';row['endpoint_close_error']=repr(e)
   if server.errors:row['status']='FAIL'
  row['remaining_dolphin']=census()
  if row['remaining_dolphin']:row['status']='FAIL'
  row['elapsed_seconds']=time.monotonic()-started;write(case/'result.json',row)
 return row

BADGE_FAILURES=[
 "Default player badge 'achievements_player.png' failed to load",
 "Default game badge 'achievements_game.png' failed to load",
 "Default unlocked achievement badge 'achievements_unlocked.png' failed to load",
 "Default locked achievement badge 'achievements_locked.png' failed to load",
]

def installed_snapshot(readback,bindings):
 installed=Path('/usr/bin/dolphin-emu-nogui');expected=bindings['installed_executable']
 require(not installed.is_symlink() and installed.resolve(strict=True)==installed,'installed executable must be the actual path')
 require(sha(installed)==expected['sha256'] and installed.stat().st_size==expected['bytes'],'installed executable changed')
 require(os.statvfs(installed).f_flag&os.ST_RDONLY,'installed executable filesystem not read-only')
 link=Path('/usr/share/dolphin-emu/sys')
 require(link.is_symlink() and os.readlink(link)=='../../config/dolphin-emu' and link.resolve(strict=True)==Path('/usr/config/dolphin-emu'),'wrong installed Sys link')
 roots=[installed,link,Path('/usr/config/dolphin-emu')]
 mounts=Path('/proc/self/mountinfo').read_text()
 for line in mounts.splitlines():
  target=Path(line.split()[4])
  require(not any(target==r or target.is_relative_to(r) for r in roots),'unexpected installed-path overlay')
 rows=[]
 for r in json.loads((PACKET/'resources.json').read_text())['resources']:
  path=Path('/'+r['installed']);resolved=path.resolve(strict=True)
  require(str(resolved)==r['resolved'] and not resolved.is_symlink(),'resource resolution changed')
  require(os.statvfs(path).f_flag&os.ST_RDONLY,'resource filesystem not read-only')
  digest=sha(path);size=path.stat().st_size
  require(digest==r['sha256'] and size==r['bytes'] and sha(resolved)==digest,'resource bytes differ from exact pinned Data/Sys')
  expected_resource=readback['products'][r['installed']]
  require(expected_resource['mode']=='-rw-r--r--','unexpected installed resource mode')
  require(expected_resource['sha256']==digest and expected_resource['bytes']==size and expected_resource['link_chain']==r['link_chain'],'resource final readback mismatch')
  rows.append({'path':str(path),'resolved':str(resolved),'bytes':size,'sha256':digest,'source_pin':r['source_pin'],'link_target':os.readlink(link)})
 return {'executable':{'path':str(installed),'bytes':installed.stat().st_size,'sha256':sha(installed)},'resources':rows,'mountinfo':mounts}

def main():
 result={'status':'FAIL','rows':[],'runtime_claim':'Actual final-image installed executable and immutable Sys resources; three startup cases only'}
 readback=None;bindings=None
 try:
  require(len(sys.argv)==2,'final image verification SHA required')
  require(os.geteuid()==0 and sorted(p.name for p in Path('/sys/class/net').iterdir())==['lo'],'root no-NIC guest required')
  require(os.statvfs(PACKET).f_flag&os.ST_RDONLY,'read-only input required')
  for line in (PACKET/'SHA256SUMS').read_text().splitlines():
   digest,name=line.split('  ',1);require(sha(PACKET/name)==digest,'packet changed')
  final=PACKET.parent/'final-image-result.json';require(sha(final)==sys.argv[1],'image verification changed')
  readback=json.loads(final.read_text());bindings=json.loads((PACKET/'inputs.json').read_text())
  require(readback['status']=='PASS' and readback['source']==bindings['source_commit'] and readback['es_commit']==bindings['es_commit'],'final image/source receipt mismatch')
  require(bindings['staged']=={} and readback['products']['usr/bin/dolphin-emu-nogui']==bindings['installed_executable'],'no substitute inputs allowed')
  result['installed_before']=installed_snapshot(readback,bindings);result['source_commit']=bindings['source_commit']
  installed=Path('/usr/bin/dolphin-emu-nogui')
  # Self-authored four-byte GameCube branch-to-self. No external game, BIOS or account.
  dol=bytearray(0x104)
  for off,value in [(0,0x100),(0x48,0x80003100),(0x90,4),(0xe0,0x80003100),(0x100,0x48000000)]:struct.pack_into('>I',dol,off,value)
  (R/'loop.dol').write_bytes(dol);result['fixture_sha256']=sha(R/'loop.dol')
  for args in [('installed-enabled',installed,True,False),('installed-disabled',installed,False,False),('installed-failed-boot',installed,True,True)]:
   row=observe(*args);result['rows'].append(row);require(row['status']=='PASS','original case failed; no retry')
  result['status']='PASS'
 except BaseException as e:result['error']=repr(e)
 finally:
  if 'installed_before' in result:
   try:
    result['installed_after']=installed_snapshot(readback,bindings)
    require(all(result['installed_after'][key]==result['installed_before'][key] for key in ['executable','resources']),'installed paths changed during cases')
   except BaseException as e:result['status']='FAIL';result['custody_error']=repr(e)
  write(R/'result.json',result)
 return 0 if result['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
