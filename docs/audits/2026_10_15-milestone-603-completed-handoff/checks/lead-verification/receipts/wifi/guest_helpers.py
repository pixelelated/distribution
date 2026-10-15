#!/usr/bin/env python3
"""Selected unchanged command/API helpers from accepted native owner; no controller/game provisioning."""
import hashlib,json,os,signal,subprocess,time,urllib.request,uuid
from pathlib import Path
R=Path('/tmp/pix-output/audit-ui')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,x):
 t=p.with_suffix('.pending');t.write_text(json.dumps(x,indent=2)+'\n');os.replace(t,p)
def identity(pid):
 p=Path('/proc',str(pid));f=(p/'stat').read_text().rsplit(')',1)[1].split()
 return {'pid':pid,'start_ticks':int(f[19]),'state':f[0],'argv':[x.decode(errors='replace') for x in (p/'cmdline').read_bytes().split(b'\0') if x]}
def natives():
 result=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:
   row=identity(int(p.name))
   if row['argv'] and Path(row['argv'][0]).name in ('flycast','dolphin-emu-nogui','dolphin-emu'):result.append(row)
  except (FileNotFoundError,ProcessLookupError):pass
 return result
def run(label,args,seconds=30):
 stem=R/(label+'-'+uuid.uuid4().hex[:8]);row={'argv':list(map(str,args)),'original_returncode':None,'timed_out':False}
 with Path(str(stem)+'.stdout').open('xb') as out,Path(str(stem)+'.stderr').open('xb') as err:
  child=subprocess.Popen(row['argv'],stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
  try:row['original_returncode']=child.wait(timeout=seconds)
  except subprocess.TimeoutExpired:
   row['timed_out']=True;os.killpg(child.pid,signal.SIGKILL);row['original_returncode']=child.wait(timeout=5)
 save(Path(str(stem)+'.json'),row);assert row['original_returncode']==0 and not row['timed_out'],label
 return Path(str(stem)+'.stdout').read_text()
def api(path,data=None):
 before=time.monotonic();req=urllib.request.Request('http://127.0.0.1:1234'+path,data=data.encode() if data else None,headers={'Content-Type':'text/plain'})
 with urllib.request.urlopen(req,timeout=5) as response:row={'path':path,'http_status':response.status,'body':response.read(1024*1024).decode(),'before_monotonic':before,'after_monotonic':time.monotonic()}
 save(R/('http-'+uuid.uuid4().hex+'.json'),row);assert row['http_status'] in (200,201);return row
