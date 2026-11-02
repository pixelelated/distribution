"""T42 audit-local guards: immutable evidence and allowed-path custody only."""
import pathlib,subprocess,json,hashlib,os,sys,datetime
R=pathlib.Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-689');REL='docs/audits/2026_11_02-epic-m6-patches-shipped';A=R/REL;B=A/'stage-b';C=A/'stage-c';SEED='9dd0716033f8831ffbd0b5ee8efbb5e5a066cfb1';S=pathlib.Path('/workspace/tmp/m6-t42')
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def cmd(argv,cwd):return subprocess.run(argv,cwd=cwd,capture_output=True)
def git(repo,*a):
 q=cmd(['git',*a],repo);assert q.returncode==0,(a,q.stderr.decode());return q.stdout
ALLOWED=[REL+'/', '.github/sessions/saved-session-state-feature-m6-patches-shipped-689.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md','docs/retros/2026-11-02-m6-patches-shipped.md']
def allowed(p):return any(p.startswith(x) if x.endswith('/') else p==x for x in ALLOWED)
def guard(repo,base):
 working=set(git(repo,'diff','--name-only','-z',base).decode().strip('\0').split('\0'))|set(git(repo,'ls-files','--others','--exclude-standard','-z').decode().strip('\0').split('\0'));working.discard('')
 bad=sorted(p for p in working if not allowed(p));assert not bad,'tree protected-path assertion: '+', '.join(bad)
 commits=[]
 for c in git(repo,'rev-list',base+'..HEAD').decode().splitlines():
  parents=git(repo,'rev-list','--parents','-n','1',c).decode().split();assert len(parents)==2,'lane merge requires explicit guard review'
  paths=git(repo,'diff-tree','--no-commit-id','--name-only','-r','-z',c).decode().strip('\0').split('\0');bad=[p for p in paths if p and not allowed(p)];assert not bad,'commit protected-path assertion: '+', '.join(bad);commits.append({'commit':c,'paths':paths})
 return {'working_paths':sorted(working),'commits':commits}
if len(sys.argv)>1 and sys.argv[1]=='guard':
 try:r=guard(pathlib.Path(sys.argv[2]),sys.argv[3]);print('PASS source-preserving tree and commit paths');sys.exit(0)
 except AssertionError as e:print('FAIL',e);sys.exit(1)
def snap(d):
 rows=[]
 for p in sorted(d.rglob('*')):
  assert not p.is_symlink(),'unexpected link in retained diagnostic projection'
  if p.is_file():rows.append({'path':str(p.relative_to(d)),'sha256':sha(p.read_bytes()),'mode':oct(p.stat().st_mode&0o777)})
 return {'files':rows,'sha256':sha(json.dumps(rows,sort_keys=True).encode())}
C.mkdir(exist_ok=True)
# Disposable fixture contains only synthetic bytes, never a repository/source export.
fixture=S/'path-guard-fixture';fixture.mkdir(exist_ok=False)
for argv in [['git','init','-q'],['git','config','user.name','T42 guard fixture'],['git','config','user.email','noreply@example.invalid'],['git','config','core.hooksPath','/dev/null']]:assert cmd(argv,fixture).returncode==0
(fixture/'scripts').mkdir();(fixture/'scripts/unpack').write_text('synthetic original\n');assert cmd(['git','add','scripts/unpack'],fixture).returncode==0;assert cmd(['git','commit','-qm','fixture baseline'],fixture).returncode==0;base=git(fixture,'rev-parse','HEAD').decode().strip()
controls=[]
(fixture/'scripts/unpack').write_text('synthetic forbidden edit\n')
argv=[sys.executable,str(A/'tools/validate.py'),'guard',str(fixture),base];q=cmd(argv,R);assert q.returncode==1 and b'tree protected-path assertion' in q.stdout;controls.append({'name':'planted-working-source-edit','argv':argv,'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()})
assert cmd(['git','add','scripts/unpack'],fixture).returncode==0;assert cmd(['git','commit','-qm','fixture planted source edit'],fixture).returncode==0
# Restore the original bytes in a second commit: current-tree equality must not hide history.
(fixture/'scripts/unpack').write_text('synthetic original\n');assert cmd(['git','add','scripts/unpack'],fixture).returncode==0;assert cmd(['git','commit','-qm','fixture restore bytes'],fixture).returncode==0
q=cmd(argv,R);assert q.returncode==1 and b'commit protected-path assertion' in q.stdout;controls.append({'name':'planted-committed-source-edit-restored','argv':argv,'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()})
dump(C/'protected-path-controls.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fixture':str(fixture),'baseline':base,'controls':controls})
print('PASS planted working-tree and reverted committed source edits each rejected with actual rc 1')
protected=guard(R,SEED);dump(C/'protected-path-positive.json',protected);print('PASS source-preserving tree and commit paths')
rows=json.loads((B/'native-inputs.json').read_text())
for n in rows:
 p=R/n['path'];raw=os.readlink(p).encode() if p.is_symlink() else p.read_bytes();assert sha(raw)==n['sha256'],'native working byte mismatch '+n['path'];assert ('120000' if p.is_symlink() else '100755' if p.stat().st_mode&0o111 else '100644')==n['mode'],'native working mode mismatch';assert sha((R/n['referent']).read_bytes())==n['patch_sha256'],'referent byte mismatch'
print('PASS native working bytes, modes and resolved referents: 384')
groups=json.loads((B/'selection.json').read_text());count=0;stream_count=0;archive_count=0;link_gap=[]
for g in groups:
 r=json.loads((B/'application'/f"{g['id']}.json").read_text())
 for row in r['rows']:
  if row.get('invoked') and 'normal' in row:
   assert row['diagnostic']['argv']==['patch','--dry-run','-p1','-N','--batch'];assert row['normal']['argv']==['patch','-p1','-N','--batch'];assert row['normal']['rc']==0 if row['promoted'] else row['normal']['rc']!=0
   literal=git(R,'show',SEED+':'+row['referent']);rendered=literal.replace(b'@DEVICE@',g['device'].encode());assert sha(literal)==row['literal_sha256'];assert sha(rendered)==row['rendered_sha256']==row['patch_sha256'];assert b'@TARGET_CPU@' not in rendered
   assert snap(pathlib.Path(row['diagnostic']['cwd']))==row['before'],'diagnostic equivalent-input assertion'
   for stage in ['diagnostic','normal']:
    for s in ['stdout','stderr']:assert sha((A/row[stage][s]).read_bytes())==row[stage][s+'_sha256'];stream_count+=1
   assert row['normal']['locale']==row['diagnostic']['locale']=='C';count+=1
 if g['id'] in ['G202','G203']:link_gap.append({'group':g['id'],'recorded_rows':len(r['rows']),'unclaimed_normal_exit':'Candidate created a relative UCM link; snapshot asserted before receipt serialization; no exit reconstructed.'})
for p in (B/'application').glob('archive-*.json'):
 r=json.loads(p.read_text());assert r['sha256']==r['recipe_sha256'];assert snap(pathlib.Path(r['base']))==r['source_tree'];archive_count+=1
p=json.loads((B/'application/partial-failure-control.json').read_text());assert p['normal']['rc']!=0 and not p['promoted'] and p['after']['sha256']!=p['before']['sha256'] and p['successor']['invoked']==False
print(f'PASS {count} normal/diagnostic pairs, {stream_count} output hashes, {archive_count} retained source projections; missing UCM exits excluded')
dump(C/'receipt-validation.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_bytes_checked':384,'application_pairs':count,'output_hashes':stream_count,'archive_projections':archive_count,'limitations':link_gap,'scope':'No application rerun. Validates retained receipts and diagnostic input projection against recorded prefix. Not a full source-tree or runtime result.'})
