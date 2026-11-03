import copy,json,pathlib,subprocess,tempfile,datetime,hashlib
A=pathlib.Path(__file__).resolve().parents[1];out=A/'stage-c';out.mkdir(exist_ok=True)
def save(p,x):
 p.parent.mkdir(exist_ok=True,parents=True)
 if p.exists():raise ValueError('refuse overwrite '+str(p))
 p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
x={'files':{'guide.md':'# Guide\n\n## Current status\nReady.\n'},'path':'guide.md','anchor':'current-status'}
for name,key,val in [('positive',None,None),('missing-target','path','absent.md'),('missing-anchor','anchor','absent'),('unsupported','files',{'guide.md':'<h2>Current status</h2>\n'})]:
 y=copy.deepcopy(x)
 if key:y[key]=val
 save(out/'link-fixtures'/(name+'.json'),y)
repo=pathlib.Path(tempfile.mkdtemp(prefix='m6-t46-confinement-'));commands=[]
def git(*args):
 argv=['git','-C',str(repo),*args];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(argv,capture_output=True);commands.append({'argv':argv,'cwd':str(pathlib.Path.cwd()),'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()})
 if p.returncode:raise RuntimeError(p.stderr.decode())
 return p.stdout.decode().strip()
def commit(message):
 git('add','--all');git('-c','user.name=T46 synthetic fixture','-c','user.email=t46-fixture@example.invalid','commit','-m',message);return git('rev-parse','HEAD')
git('init','--quiet');(repo/'product.txt').write_text('synthetic original\n');seed=commit('Synthetic seed')
p=repo/'docs/audits/2026_11_03-epic-m6-records/fixture.txt';p.parent.mkdir(parents=True);p.write_text('new record\n');positive=commit('Synthetic permitted record')
(repo/'product.txt').write_text('planted source edit\n');negative=commit('Synthetic forbidden source edit')
(repo/'product.txt').write_text('synthetic original\n');reverted=commit('Synthetic edit then revert')
save(out/'confinement-fixtures.json',{'repo':str(repo),'seed':seed,'positive':positive,'source_edit':negative,'edit_then_revert':reverted,'commands':commands,'custody':'New tiny synthetic Git fixture only; retained, no real source exported.'})
print('CREATED 4 new link fixtures and 3 synthetic confinement histories at '+str(repo))
