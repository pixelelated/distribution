from pathlib import Path
import datetime,hashlib,json,os,shutil,stat,struct,subprocess,time
out=Path(__file__).parent;store=Path('/workspace/artifacts/pixelelated-build-custody/issue-456-runtime-01');store.mkdir(parents=True,exist_ok=False)
objects=store/'objects';objects.mkdir();prior=Path('/workspace/artifacts/pixelelated-build-custody/issue-456-es-logs-01/objects')
last=time.monotonic();visited=0;selected=0;total=0;checked=set();summaries=[]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
for n in ['03','05','06','07','08']:
 tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement'+n);build=next(tree.glob('build.*'))
 head=subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip();rows=[];disks=[];errors=[]
 for base,dirs,files in os.walk(build,followlinks=False,onerror=lambda e:errors.append(str(e))):
  for name in files:
   p=Path(base)/name;visited+=1
   if name.endswith('.qcow2'):disks.append(str(p))
   if time.monotonic()-last>10:
    print('Inspected',visited,'file names; retained',selected,'runtime ELF files;',total,'unique bytes',flush=True);last=time.monotonic()
   if p.is_symlink():continue
   s=p.stat()
   if not stat.S_ISREG(s.st_mode):continue
   # Object/static archives/compiler cache are reproducible intermediates.
   # Inspect all executable regular files and all library/module/debug names.
   if not (s.st_mode&0o111 or '.so' in name or name.endswith(('.ko','.debug')) or name=='vmlinux'):continue
   with p.open('rb') as f:h=f.read(20)
   if len(h)<20 or h[:4]!=b'\x7fELF':continue
   assert h[5] in (1,2),str(p)
   kind=int.from_bytes(h[16:18],'little' if h[5]==1 else 'big')
   if kind not in (2,3) and not (kind==1 and name.endswith(('.ko','.debug'))):continue
   digest=sha(p);dest=prior/digest if (prior/digest).is_file() else objects/digest
   if not dest.exists():
    assert shutil.disk_usage(store).free-s.st_size>20*2**30,'Refuse below20GiB free'
    tmp=objects/(digest+'.partial');shutil.copyfile(p,tmp);assert sha(tmp)==digest;tmp.rename(dest);total+=s.st_size
   elif dest not in checked:assert sha(dest)==digest
   after=p.stat();assert (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),str(p)
   assert dest.stat().st_dev!=s.st_dev or dest.stat().st_ino!=s.st_ino
   checked.add(dest);selected+=1;rows.append({'path':str(p.relative_to(tree)),'sha256':digest,'bytes':s.st_size,'mode':stat.S_IMODE(s.st_mode),'object':str(dest),'elf_type':kind})
 assert not errors,errors
 assert head==subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()
 m=store/(tree.name+'.json');m.write_text(json.dumps({'tree':str(tree),'head':head,'runtime_elf':rows,'qcow2_found':disks},indent=2)+'\n')
 summaries.append({'tree':str(tree),'manifest':str(m),'manifest_sha256':sha(m),'runtime_elf_count':len(rows),'qcow2_found':disks})
 print('Preserved runtime ELF outputs',tree.name,len(rows),flush=True)
for p in checked:assert sha(p)==p.name
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'store':str(store),'trees':summaries,'file_names_inspected':visited,'runtime_elf_files':selected,'unique_objects':len(checked),'new_independent_bytes':total,'all_destination_hashes_verified':True,'deletion_performed':False,'scope':'Executable ELF plus library/module/debug filenames; excludes relocatable object intermediates and static archives; independent copies, original trees unchanged'}
(out/'summary.json').write_text(json.dumps(r,indent=2)+'\n');(store/'summary.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS independent runtime ELF preservation; no deletion',flush=True)
