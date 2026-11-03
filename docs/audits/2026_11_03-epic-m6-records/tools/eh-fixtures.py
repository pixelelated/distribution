"""Create only new tiny Git fixtures; retain all scratch and command receipts."""
import base64,copy,datetime,hashlib,json,os,pathlib,subprocess,tempfile
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];E=A/'stage-e';root=pathlib.Path(tempfile.mkdtemp(prefix='m6-t46-eh-fixtures-'));P=json.loads((E/'scope-policy.json').read_text());before=(E/'source/before.md').read_bytes();after=(E/'source/candidate.md').read_bytes();commands=[];cases=[];frozen=P['audit_root']+'stage-a/frozen.txt';record=P['audit_root']+'stage-e/fixture.txt'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(repo,*args):
 argv=['git','-C',str(repo),*args];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(argv,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat();commands.append({'argv':argv,'cwd':str(R),'start':start,'end':end,'rc':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'stdout_base64':base64.b64encode(p.stdout).decode(),'stderr_base64':base64.b64encode(p.stderr).decode()})
 if p.returncode:raise RuntimeError(p.stderr.decode())
 return p.stdout.decode().strip()
def put(repo,path,b):
 p=repo/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def commit(repo,msg):
 git(repo,'add','--all');git(repo,'-c','user.name=T46 synthetic fixture','-c','user.email=t46-fixture@example.invalid','commit','--quiet','-m',msg);return git(repo,'rev-parse','HEAD')
for name in ['index-source','index-frozen','index-readme','history-source','history-revert','history-frozen','history-wrong-readme-repair','unrelated-retro','unrelated-day','executable','symlink','merge','deletion','positive']:
 repo=root/name;repo.mkdir();git(repo,'init','--quiet','--initial-branch=main');put(repo,P['readme'],before);put(repo,frozen,b'synthetic frozen receipt\n');put(repo,'product.txt',b'synthetic protected source\n');base=commit(repo,'Synthetic baseline')
 meta=git(repo,'ls-tree',base,'--',frozen).split('\t')[0].split();policy=copy.deepcopy(P);policy['base']=base;policy['frozen']={frozen:dict(zip(['mode','type','oid'],meta))};policyfile=root/(name+'-policy.json');policyfile.write_text(json.dumps(policy,indent=2)+'\n')
 put(repo,P['readme'],after);put(repo,record,b'new synthetic record\n');put(repo,'docs/retros/2026-11-03-m6-records.md',b'authorized dated retro\n');put(repo,'docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md',b'authorized dated log\n');positive=commit(repo,'Synthetic exact authorized correction and records')
 if name.startswith('index-'):
  target={'index-source':'product.txt','index-frozen':frozen,'index-readme':P['readme']}[name];original=(repo/target).read_bytes();put(repo,target,b'forbidden staged bytes\n');git(repo,'add','--',target);put(repo,target,original)
 elif name in ('history-source','history-revert'):
  put(repo,'product.txt',b'forbidden source bytes\n');commit(repo,'Synthetic forbidden source edit')
  if name=='history-revert':put(repo,'product.txt',b'synthetic protected source\n');commit(repo,'Synthetic source edit then revert')
 elif name=='history-frozen':put(repo,frozen,b'changed frozen bytes\n');commit(repo,'Synthetic frozen receipt edit')
 elif name=='history-wrong-readme-repair':
  put(repo,P['readme'],b'wrong paragraph\n');commit(repo,'Synthetic wrong README');put(repo,P['readme'],after);commit(repo,'Synthetic later README repair')
 elif name=='unrelated-retro':put(repo,'docs/retros/2026-11-02-unrelated.md',b'unrelated record\n')
 elif name=='unrelated-day':put(repo,'docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md',b'unrelated record\n')
 elif name=='executable':os.chmod(repo/record,0o755);git(repo,'add','--',record)
 elif name=='symlink':os.symlink('does-not-exist',repo/(P['audit_root']+'stage-e/link'));git(repo,'add','--',P['audit_root']+'stage-e/link')
 elif name=='merge':
  git(repo,'checkout','--quiet','-b','side');put(repo,P['audit_root']+'stage-e/side.txt',b'side\n');commit(repo,'Synthetic side record');git(repo,'checkout','--quiet','main');put(repo,P['audit_root']+'stage-e/main.txt',b'main\n');commit(repo,'Synthetic main record');git(repo,'-c','user.name=T46 synthetic fixture','-c','user.email=t46-fixture@example.invalid','merge','--no-ff','--quiet','side','-m','Synthetic merge refusal')
 elif name=='deletion':
  git(repo,'update-index','--force-remove','--',record);git(repo,'-c','user.name=T46 synthetic fixture','-c','user.email=t46-fixture@example.invalid','commit','--quiet','-m','Synthetic index deletion; working file retained')
 cases.append({'name':name,'repo':str(repo),'policy':str(policyfile),'policy_sha256':sha(policyfile.read_bytes()),'base':base,'tip':git(repo,'rev-parse','HEAD'),'expected':0 if name=='positive' else 1,'index_only':name.startswith('index-')})
 (E/'fixture-creation-progress.json').write_text(json.dumps({'root':str(root),'cases':cases,'commands':commands},indent=2)+'\n')
(E/'fixtures-manifest.json').write_text(json.dumps({'root':str(root),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':'T3 wN:p6; T46 E-H new tiny synthetic Git only','cases':cases,'commands':commands,'custody':'Retain all; no deletion/cleanup. Tiny README proof input only, no product tree checkout/export.'},indent=2)+'\n');print('CREATED14 new scope fixtures at '+str(root)+'; three index-only states preserve restored working bytes; no old controls replayed')
