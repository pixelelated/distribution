from pathlib import Path
import datetime,hashlib,json,os,shutil,stat,subprocess,time
out=Path(__file__).parent
store=Path('/workspace/artifacts/pixelelated-build-custody/issue-456-es-logs-01')
store.mkdir(parents=True,exist_ok=False)
objects=store/'objects';objects.mkdir()
checked=set();records=[];last=time.monotonic();total=0

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def keep(p,tree):
 global last,total
 s=p.lstat();row={'path':str(p.relative_to(tree)),'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns}
 if stat.S_ISLNK(s.st_mode):row.update(kind='symlink',target=os.readlink(p))
 elif stat.S_ISDIR(s.st_mode):row.update(kind='directory')
 elif stat.S_ISREG(s.st_mode):
  digest=sha(p);dest=objects/digest
  if not dest.exists():
   assert shutil.disk_usage(store).free-s.st_size>20*2**30,'Refuse below20GiB free'
   temp=objects/(digest+'.partial');shutil.copyfile(p,temp)
   assert sha(temp)==digest,('copy mismatch',str(p))
   temp.rename(dest);total+=s.st_size
  elif digest not in checked:assert sha(dest)==digest
  after=p.lstat();assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),('source changed',str(p))
  assert dest.stat().st_ino!=s.st_ino or dest.stat().st_dev!=s.st_dev,'Refuse shared inode'
  checked.add(digest);row.update(kind='file',sha256=digest,bytes=s.st_size)
 else:raise RuntimeError('Unsupported special file: '+str(p))
 records.append(row)
 if time.monotonic()-last>10:
  print('Preserved',len(records),'entries;',total,'independent unique bytes',flush=True);last=time.monotonic()

summaries=[]
for n in ['03','05','06','07','08']:
 tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement'+n);build=next(tree.glob('build.*'))
 head=subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()
 selected=list(build.glob('build/emulationstation-*'))+[build/'.threads',build/'.stamps',tree/'.build-runs']
 assert len(selected)==4,selected
 records=[]
 for root in selected:
  assert root.is_dir(),root
  keep(root,tree)
  for base,dirs,files in os.walk(root,followlinks=False):
   for name in dirs+files:keep(Path(base)/name,tree)
 assert head==subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()
 manifest={'tree':str(tree),'head':head,'scope':'Complete EmulationStation source/build directory plus thread logs, package stamps and watched build runs; other package debug/source custody remains separate','entries':records}
 path=store/(tree.name+'.json');path.write_text(json.dumps(manifest,indent=2)+'\n')
 summaries.append({'tree':str(tree),'head':head,'manifest':str(path),'manifest_sha256':sha(path),'entries':len(records)})
 print('Preserved scoped source/debug/log custody',tree.name,len(records),'entries',flush=True)
# Reverify every independent destination after all copies.
for digest in checked:assert sha(objects/digest)==digest
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'store':str(store),'trees':summaries,'unique_objects':len(checked),'unique_bytes':total,'all_destination_sha256_verified':True,'independent_files':True,'scope_complete_for_removal':False,'deletion_performed':False,'remaining':'Other package debugging/source custody, unreadable live dependencies and final net removal plan'}
(out/'summary.json').write_text(json.dumps(r,indent=2)+'\n');(store/'summary.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS scoped independent ES/source/log preservation; no deletion',flush=True)
