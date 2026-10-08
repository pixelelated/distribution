from pathlib import Path
import datetime,hashlib,json,os,subprocess
O=Path(__file__).resolve().parent;j=json.loads((O/'inputs.json').read_text());old=Path(j['cache_parent_tree']);new=Path(j['host_worktree'])
assert Path.cwd()==new
s=os.statvfs('/workspace');free=s.f_bavail*s.f_frsize
assert free>=500*1024**3,free
(O/'capacity.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'available_bytes':free,'copy_plus_build_required_bytes':500*1024**3,'measured_cache_allocated_bytes':137620140032,'result':'PASS'},indent=2)+'\n')
preserved=0
for raw in subprocess.check_output(['git','ls-files','-z']).split(b'\0'):
 if not raw:continue
 n=os.fsdecode(raw);a=old/n;b=new/n
 if a.is_file() and b.is_file() and not a.is_symlink() and not b.is_symlink() and a.read_bytes()==b.read_bytes():
  st=a.stat();os.utime(b,ns=(st.st_atime_ns,st.st_mtime_ns));preserved+=1
results=[]
for name in j['cache_roots']:
 a=old/name;b=new/name;assert a.is_dir() and not b.exists();print('Copying',name,flush=True)
 proc=subprocess.Popen(['rsync','-aH','--numeric-ids','--info=progress2',str(a)+'/',str(b)+'/'],stdout=subprocess.PIPE)
 stream=subprocess.run(['python3','-I',str(O/'progress.py')],stdin=proc.stdout);proc.stdout.close();assert proc.wait()==0 and stream.returncode==0
 print('Checksum comparison',name,flush=True)
 report=O/(name+'.compare.txt')
 with report.open('wb') as f:subprocess.run(['rsync','-aHnc','--numeric-ids','--delete','--itemize-changes',str(a)+'/',str(b)+'/'],stdout=f,check=True)
 assert report.stat().st_size==0
 n=0
 for p in b.rglob('*'):
  if p.is_file() and not p.is_symlink():
   sa=(a/p.relative_to(b)).stat();sb=p.stat();assert (sa.st_dev,sa.st_ino)!=(sb.st_dev,sb.st_ino),p;n+=1
   if n%250000==0:print('Independent inodes',name,n,flush=True)
 results.append({'root':name,'checksum_equal':True,'independent_regular_files':n})
 print('PASS',name,n,'independent files',flush=True)
(O/'cache-ready.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','roots':results,'unchanged_tracked_timestamps_preserved':preserved,'mode':'independent rsync files, internal hardlinks retained; no cross-root hardlinks'},indent=2)+'\n')
