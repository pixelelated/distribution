from pathlib import Path
import os,json,datetime,re
owner=Path(__file__).resolve().parent
roots=json.loads((owner/'roots.json').read_text())
assert roots and all(r.startswith('/workspace/') for r in roots)
pattern=re.compile('(?:'+'|'.join(re.escape(r) for r in sorted(roots,key=len,reverse=True))+r')(?=/|$|[\s\x00])')
hits=[];unreadable=[];examined=0;kernel=0;gone=0
for p in Path('/proc').glob('[0-9]*'):
 if int(p.name)==os.getpid():continue
 try:fields=dict(l.split(':',1) for l in (p/'status').read_text().splitlines() if ':' in l)
 except FileNotFoundError:gone+=1;continue
 except PermissionError:unreadable.append({'pid':int(p.name),'fields':['status']});continue
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
 matched=sorted({(kind,m.group(0)) for kind,value in refs for m in pattern.finditer(value)})
 if matched:hits.append({'pid':int(p.name),'references':[{'kind':k,'tree':v} for k,v in matched]})
 if fail and p.exists():unreadable.append({'pid':int(p.name),'fields':sorted(set(fail))})
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'effective_uid':os.geteuid(),'roots':roots,'userspace_examined':examined,'kernel_threads_excluded':kernel,'disappeared':gone,'matches':hits,'unreadable':unreadable,'readonly':True,'scope':'Matches are classification input, not permission to stop processes or delete files.'},indent=2))
raise SystemExit(1 if unreadable or os.geteuid()!=0 else 0)
