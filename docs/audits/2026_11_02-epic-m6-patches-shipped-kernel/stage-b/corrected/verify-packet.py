#!/usr/bin/env python3
"""Verify the Stage-B packet without invoking the application runner or source helpers."""
from pathlib import Path
import collections,datetime,hashlib,json,os,re,subprocess,time
O=Path(__file__).resolve().parent; A=O.parent.parent; R=O.parents[4]
REF='02aab33bd9842610b0d466c9c186454dc14373ee'; OLD='3cd9ca140a0da9af447a3ee2fb9cdbbbf222a95b'
os.chdir(R);os.environ['LC_ALL']='C';os.environ['TMPDIR']='/workspace/tmp/m6-t41/tmp'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b):return hashlib.sha256(b).hexdigest()
def dec(s):return s.replace(chr(92)+'u002d','-')
def git(*args):return subprocess.check_output(['git',*args])
def obj(name):return json.loads((O/name).read_text())
def tree(root):
 d=hashlib.sha256()
 for p in sorted(Path(root).rglob('*')):
  if p.is_file():d.update(str(p.relative_to(root)).encode()+b'\0'+p.read_bytes()+b'\0')
 return d.hexdigest()
start=stamp();tic=time.monotonic();out={'start':start,'source_ref':REF,'preserved_at':OLD,'checks':[]}
oldpaths=git('ls-tree','-r','--name-only',OLD,'--',str((A/'stage-a').relative_to(R)),str((A/'stage-b').relative_to(R))).decode().splitlines()
for p in oldpaths:assert (R/p).read_bytes()==git('show',OLD+':'+p),('old receipt changed',p)
paths=[dec(p) for p in (A/'stage-a/p1-qa-scratch/paths.txt').read_text().splitlines()]
assert len(paths)==len(set(paths))==107
assert set(paths)==set((R/'.qa-scratch/t41/paths.txt').read_text().splitlines())
for p in paths:
 b=git('show',REF+':'+p)
 assert b==(R/p).read_bytes()==git('show','2174265e9c:'+p)==git('show','HEAD:'+p),('source changed',p)
assert not git('diff','d7dd766659','--','*.patch','*.conf','packages','projects','tools','scripts'), 'protected source diff'
meta=obj('run-metadata.json'); app=obj('application-results.json'); rows=app['rows']
assert h((O/'apply-corrected.py').read_bytes())==meta['runner_sha256']
assert app['source_ref']==REF and app['complete'] and len(rows)==120 and len({r['path'] for r in rows})==106
plans={'GENERIC_X64':8,'H700':42,'SM8550':65,'UBOOT-DDR3':2,'UBOOT-DDR4':2,'FIRMWARE':1}
assert collections.Counter(r['plan'] for r in rows)==plans
status=collections.Counter(); disagreements=[]
for plan,n in plans.items():
 tar=obj('tar-'+plan+'.json');previous=tar['initial_tree_sha256'];assert tree(tar['initial_tree'])==previous
 assert tar['all_missing_accounted'] and tar['not_in_archive']==len(tar['missing_members'])
 assert h((O/tar['output']).read_bytes())==tar['output_sha256']
 order=[dec(p) for p in (O/('order-'+plan+'.txt')).read_text().splitlines()]
 prs=[r for r in rows if r['plan']==plan];assert len(prs)==n and [r['index'] for r in prs]==list(range(1,n+1))
 assert [dec(r['path']) for r in prs]==order
 for r in prs:
  assert r==obj(f'rows/{plan}-{r["index"]:03d}.json')
  assert r['apply_rc']==0 and r['attempted'] and r['promoted'] and r['FAILED']==0
  assert r['input_tree_sha256']==r['after_dry_tree_sha256']==previous
  assert Path(r['candidate']).is_relative_to(meta['scratch'])
  assert tree(r['candidate'])==r['output_tree_sha256'];previous=r['output_tree_sha256']
  assert r['patch_sha256']==h(git('show',REF+':'+dec(r['path'])))
  for k in ['dry','apply']:
   c=r[k];assert c['rc']==r[k+'_rc'] and c['start'] and c['elapsed_seconds']>=0 and not c['timed_out']
   assert h((O/c['output']).read_bytes())==c['output_sha256']
  assert r['dry']['argv']==r['apply']['argv']+['--dry-run']
  txt=(O/r['apply']['output']).read_text();assert r['offset']==txt.count('offset') and r['fuzz']==txt.count('fuzz') and 'FAILED' not in txt
  expected='fuzz' if 'fuzz' in txt else 'applies with offset' if 'offset' in txt else 'applies'
  assert r['status']==expected;status[expected]+=1
  if r['dry_rc']!=r['apply_rc']:disagreements.append(f'{plan}-{r["index"]:03d}')
assert status=={'applies':43,'applies with offset':48,'fuzz':29} and disagreements==['H700-011']
guard=obj('failed-candidate-guard.json');f=guard['failure'];s=guard['successor']
assert guard['result']=='PASS' and guard['prefix_before']==guard['prefix_after']==f['input_tree_sha256']==s['input_tree_sha256']
assert f['apply_rc']==1 and not f['promoted'] and f['output_tree_sha256']!=f['input_tree_sha256']
assert s['blocked_by']==1 and not s['attempted'] and not s['promoted'] and s['apply_rc'] is None and 'apply' not in s
assert tree(f['candidate'])==f['output_tree_sha256']
assert tree(Path(f['candidate']).parents[1]/'prefix')==guard['prefix_before']
for c in [f['dry'],f['apply']]:assert h((O/c['output']).read_bytes())==c['output_sha256']
forward=(A/'02-forward-audit.md').read_text(); log=(A/'00-running-log.md').read_text();analysis=(A/'04-analysis.md').read_text()
for mode,size in [('provenance',19),('coverage',5)]:
 table=(O/f'table-{mode}.txt').read_text().strip();assert table in forward
 tablepaths=[]
 for line in table.splitlines()[2:]:
  cells=[x.strip() for x in re.split(r'(?<!\\)\|',line)[1:-1]];assert len(cells)==size and all(cells)
  tablepaths.append(dec(cells[0].strip('`')))
 assert len(tablepaths)==len(set(tablepaths))==107 and sorted(tablepaths)==sorted(paths)
assert re.findall(r'^\| (L-\d\d) \|',forward,re.M)==[f'L-{i:02d}' for i in range(1,32)]
assert re.findall(r'^\| ([a-p]) \|',forward,re.M)==list('abcdefghijklmnop')
assert len(re.findall(r'proved:',forward))==12 and len(re.findall(r'^PROOF:',log,re.M))==12
proofs=obj('proof-index.json');assert len(proofs)==12
for pid,kind,claim,evidence in proofs:assert f'PROOF: {pid} | {kind} | {claim}' in log and f'| {pid} | proved: {kind} | {claim}' in forward
assert re.findall(r'^### Q([1-7]) ',analysis,re.M)==list('1234567')
score=obj('scorecard.json');assert len(score)==28 and collections.Counter(r[1] for r in score)=={'PASS':14,'PARTIAL':14}
for p in ['02-forward-audit.md','03-retrospective.md','04-analysis.md']:assert (A/p).stat().st_size>1000
for r in obj('generator-fail-first.json'):
 assert r['rc']==1 and r['last_line'] in (O/f'generator-fail-{r["name"]}.out').read_text()
# Byte-identical pairs necessarily match at all three T40 normalization levels; verify the actual digests too.
def hashes(text):
 i=text.find('diff --git');i=text.find('--- ') if i<0 else i;b=text[i:].splitlines()
 hh=lambda ls:h('\n'.join(ls).encode())
 return [hh([l for l in b if not l.startswith('index ')]),hh([l for l in b if not l.startswith(('index ','diff --git','--- ','+++ ','@@'))]),hh([l for l in b if l[:1] in '+-' and not l.startswith(('+++ ','--- '))])]
pairs=obj('remaining-reads.json')['duplicates'];assert len(pairs)==5
for p in pairs:
 a=git('show',REF+':'+p['a']);b=git('show',REF+':'+p['b']);assert a==b and h(a)==p['sha256'] and hashes(a.decode())==hashes(b.decode())
# Explicit committed-byte encoding. JSON decoding alone is allowed to normalize the escaped filename.
for p in A.rglob('*'):
 if p.is_file():assert ('mask'+'-data0').encode() not in p.read_bytes(),('unescaped filename',str(p.relative_to(A)))
identity=(R/'.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md').read_text()
assert 'Codex / GPT-6-Astra / xhigh' in identity and '4c8a118cfb4efa8d13c1b41b72ef7a205da5f766' in identity
out['structural']={'rc':0,'start':start,'elapsed_seconds':round(time.monotonic()-tic,3),'old_receipts_unchanged':len(oldpaths),'source_paths_unchanged':107,'applications':120,'unique_patches':106,'status':dict(status),'disagreements':disagreements,'table_rows':107,'leads':31,'rulings':16,'proofs':12,'duplicate_pairs_all_three_levels':5,'scorecard':{'PASS':14,'PARTIAL':14}}
print('Structural PASS:',json.dumps(out['structural']),flush=True)
def run(label,argv,expected=0,data=None,env=None):
 t=stamp();t0=time.monotonic();p=subprocess.run(argv,input=data,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,timeout=120)
 row={'label':label,'argv':argv,'start':t,'elapsed_seconds':round(time.monotonic()-t0,3),'rc':p.returncode,'output':p.stdout.decode(errors='replace')};out['checks'].append(row)
 assert p.returncode==expected,(label,p.returncode,row['output'])
 print(label,'rc='+str(p.returncode),flush=True);return row
for argv in [['./tools/rules-check','--quiet'],['./tools/register-check'],['./tools/work-log-index','--check'],['git','diff','--check',OLD],['.githooks/hooks-test'],['./tools/ceremony-check','--gate']]:run(' '.join(argv),argv)
files=list(A.rglob('*'))+[R/'.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md',R/'docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md',R/'docs/work-logs/INDEX.md']
packet=b'\n'.join(p.read_bytes() for p in files if p.is_file() and p.name not in ['validation.json','hygiene.out'])
run('forbidden-terms actual packet',['./tools/forbidden-terms-check','--stdin'],data=packet)
env=os.environ.copy();probe='stageb'+'positivecontrol';env['FORBIDDEN_PATTERNS']=probe
run('forbidden-terms runtime positive',['./tools/forbidden-terms-check','--stdin'],expected=1,data=(probe+'\n').encode(),env=env)
scan=['bash','-c','. .githooks/secret-patterns; grep -a -c -E -e "${SECRET_PATTERNS}"']
run('secret regex compiles / empty input',scan,expected=1,data=b'')
row=run('secret runtime positive',scan,data=('s'+'k'+'-'+'a'*24+'\n').encode());assert row['output'].strip()=='1'
row=run('secret actual packet',scan,expected=1,data=packet);assert row['output'].strip()=='0'
out['end']=stamp();out['result']='PASS';out['validation_script_sha256']=h(Path(__file__).read_bytes())
(O/'hygiene.out').write_text('\n'.join(f'{x["start"]} {x["label"]} rc={x["rc"]}\n{x["output"]}' for x in out['checks']))
(O/'validation.json').write_text(json.dumps(out,indent=2)+'\n')
print('Stage-B validation PASS; actual producer results saved.',flush=True)
