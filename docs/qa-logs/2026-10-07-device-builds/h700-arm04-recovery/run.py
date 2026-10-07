from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,tarfile,sys
owner=Path(__file__).resolve().parent
failed=Path('/workspace/tmp/pixelelated-m7-h700-arm-04');tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01');root=tree/'build.pixelelated-H700.arm'
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n');rc=1
try:
 for path,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
 assert json.loads((failed/'owner-verification.json').read_text())['result']=='FAILED'
 assert json.loads(Path('/workspace/tmp/pixelelated-m7-h700-arm04-acceptance-01/artifacts/acceptance.json').read_text())['container_exited'] is True
 assert json.loads(Path('/workspace/tmp/pixelelated-m7-build-root-controls-02/owner-verification.json').read_text())['result']=='PASS'
 subprocess.run(['python3','-I',str(failed/'verify-source.py')],cwd=tree,check=True)
 assert not subprocess.check_output(['git','-C',str(tree),'status','--porcelain'],text=True).strip()
 archive=owner/'artifacts/failure-threads-stamps.tar.gz'
 with tarfile.open(archive,'w:gz') as out:
  for n in ['.threads','.stamps']:out.add(root/n,arcname=n,recursive=True)
 with tarfile.open(archive) as check:assert check.getmember('.threads/status').isfile() and check.getmember('.stamps').isdir()
 interrupted={'box86','SDL2_net','harfbuzz','mpg123','xterm','wlroots'}
 changed={'box86','lib32','retroarch','gpsp-lr','desmume-lr','daedalusx64-sa'}
 found=set();paths=[];fixture_count=0
 for d in sorted((root/'build').iterdir()):
  info=d/'.rocknix-package'
  if not info.is_file():continue
  name=re.search(r'INFO_PKG_NAME="([^"]+)"',info.read_text())[1]
  stamps=list((root/'.stamps'/name).glob('build_*'))
  contexts=[p for p in d.iterdir() if p.is_dir() and p.name.startswith('.') and 'linux-gnu' in p.name]
  compiled=[]
  if not stamps:
   for base,dirs,files in os.walk(d):compiled.extend(Path(base,f) for f in files if f.endswith(('.o','.a')))
  if name=='binutils-gold' and compiled and not contexts:
   source=Path('/workspace/cache/rocknix-sources/binutils-gold/binutils-gold-2.46.1.tar.xz')
   with tarfile.open(source) as tf:
    members={m.name.split('/',1)[-1]:m for m in tf.getmembers() if m.isfile()}
    for p in compiled:
     m=members[str(p.relative_to(d))];assert hashlib.file_digest(tf.extractfile(m),'sha256').hexdigest()==hashlib.sha256(p.read_bytes()).hexdigest();fixture_count+=1
   compiled=[]
  if not stamps and (contexts or compiled):found.add(name)
  if name in interrupted|changed:
   paths.append(d)
   for p in [root/'.stamps'/name,root/'install_pkg'/d.name]:
    if p.exists():paths.append(p)
 assert found==interrupted,(found,interrupted)
 assert not list((root/'.unpack').iterdir()),'Preserve/classify unexpected incomplete unpack before resumption'
 if (root/'image').exists():paths.append(root/'image')
 preserved=owner/'preserved';preserved.mkdir();plan=[]
 for p in sorted(set(paths)):
  s=p.stat();dest=preserved/p.relative_to(root);assert not dest.exists() and s.st_dev==preserved.stat().st_dev
  plan.append({'source':str(p),'destination':str(dest),'device':s.st_dev,'inode':s.st_ino})
 (owner/'artifacts/recovery-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
 for row in plan:
  p=Path(row['source']);d=Path(row['destination']);d.parent.mkdir(parents=True,exist_ok=True);p.rename(d)
  assert not p.exists() and (d.stat().st_dev,d.stat().st_ino)==(row['device'],row['inode'])
 new='43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa'
 assert subprocess.check_output(['git','-C',str(tree),'rev-parse','next'],text=True).strip()==new
 subprocess.run(['git','-C',str(tree),'merge','--ff-only',new],check=True)
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','interrupted_scopes':sorted(interrupted),'changed_recipe_scopes_recreated':sorted(changed),'preserved_by_rename':plan,'archive':str(archive),'archive_sha256':hashlib.file_digest(archive.open('rb'),'sha256').hexdigest(),'verified_bundled_archive_fixture_files':fixture_count,'deleted_payloads':0,'advanced_stopped_tree_to':new}
 (owner/'artifacts/recovery.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='preserved_by_rename'}),flush=True);rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
