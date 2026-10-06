from pathlib import Path
import os,json,datetime
roots=['/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement'+n for n in ['03','05','06','07','08']]
hits=[];unreadable=[];examined=0;kernel=0;gone=0
for p in Path('/proc').glob('[0-9]*'):
 try:fields=dict(l.split(':',1) for l in (p/'status').read_text().splitlines() if ':' in l)
 except FileNotFoundError:gone+=1;continue
 if fields.get('Kthread','').strip()=='1':kernel+=1;continue
 examined+=1;refs=[];fail=[]
 for key in ['cwd','exe','root']:
  try:refs.append((key,os.readlink(p/key)))
  except FileNotFoundError:pass
  except PermissionError:fail.append(key)
 try:refs.extend(('argument',os.fsdecode(x)) for x in (p/'cmdline').read_bytes().split(b'\0') if x)
 except FileNotFoundError:pass
 except PermissionError:fail.append('cmdline')
 try:
  for fd in (p/'fd').iterdir():
   try:refs.append(('fd',os.readlink(fd)))
   except FileNotFoundError:pass
   except PermissionError:fail.append('fd')
 except FileNotFoundError:pass
 except PermissionError:fail.append('fd-directory')
 try:
  for line in (p/'maps').read_text().splitlines():
   parts=line.split(None,5)
   if len(parts)==6:refs.append(('mapping',parts[5]))
 except FileNotFoundError:pass
 except PermissionError:fail.append('maps')
 matched=sorted({(kind,root) for kind,value in refs for root in roots if value==root or value.startswith(root+'/') or root+'/' in value})
 if matched:hits.append({'pid':int(p.name),'references':[{'kind':k,'tree':v} for k,v in matched]})
 if fail and p.exists():unreadable.append({'pid':int(p.name),'fields':sorted(set(fail))})
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'effective_uid':os.geteuid(),'roots':roots,'userspace_examined':examined,'kernel_threads_excluded':kernel,'disappeared':gone,'matches':hits,'unreadable':unreadable,'readonly':True},indent=2))
raise SystemExit(1 if hits or unreadable else 0)
