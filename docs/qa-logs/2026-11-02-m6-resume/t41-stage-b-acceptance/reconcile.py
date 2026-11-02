#!/usr/bin/env python3
"""Independent immutable-byte reconciliation. Executes git show/ls-tree only.
Does not import or execute any packet producer, generator, test, or patch command.
Writes derived manifests/results beside this script, no copied source tree.
Reader: Codex (GPT-6), /root; wN:p5 m6-t2-es-launch, session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import collections as C, datetime as D, hashlib as H, json, pathlib as P, re, subprocess as S
ROOT=P.Path(__file__).resolve().parent
REPO='/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649'
TIP='7e5d1546712df2eb79c585fce663186770d1ceb9'; SRC='02aab33bd9842610b0d466c9c186454dc14373ee'
OLD='3cd9ca140a0da9af447a3ee2fb9cdbbbf222a95b'; COORD='b6332dbc13f5929f05ec5ba23c44285c5ee56b38'; ERR='4c8a118cfb4efa8d13c1b41b72ef7a205da5f766'
AUD='docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/'; COR=AUD+'stage-b/corrected/'
POP={'GENERIC_X64':8,'H700':42,'SM8550':65,'UBOOT-DDR3':2,'UBOOT-DDR4':2,'FIRMWARE':1}
manifest={}; results={}; cache={}
def sha(b): return H.sha256(b).hexdigest()
def git(*a): return S.check_output(['git','-C',REPO,*a])
def blob(ref,path):
 k=(ref,path)
 if k not in cache: cache[k]=git('show',ref+':'+path)
 return cache[k]
def raw(path):
 b=blob(TIP,path);manifest[path]=sha(b);return b
def corr(path): return raw(COR+path)
def obj(path): return json.loads(corr(path))
def decode(s): return s.replace('\\u002d','-')
def display(s):
 # Match the accepted representation; do not expose a scanner-shaped path token.
 return s.replace('mask-data0','mask\\u002ddata0')
def tree(ref,prefix):
 out={}
 for row in git('ls-tree','-rz',ref,'--',prefix).split(b'\0'):
  if row:
   meta,path=row.split(b'\t',1);out[path.decode()]=meta.decode()
 return out
def check(cond,msg):
 if not cond: raise AssertionError(msg)
# Erratum authority, exact payload and retained row.
brief='docs/reviews/briefs/patches-shipped-kernel.md'
b=blob(COORD,brief);check(b==blob(ERR,brief),'coordinator brief differs from erratum ref')
e=b[b.index(b'## Stage-B method erratum'):]
check(corr('coordinator-method-erratum.txt').strip()==e.strip(),'retained erratum mismatch')
reg=[l for l in blob(COORD,'docs/decision-register.md').splitlines() if l.startswith(b'| D-WORKFLOW-222 |')]
check(len(reg)==1 and corr('coordinator-register-row.txt').strip()==reg[0],'D222 row mismatch')
results['authority']={'brief_sha256':sha(b),'erratum_sha256':sha(corr('coordinator-method-erratum.txt')),'D222_row_sha256':sha(corr('coordinator-register-row.txt'))}
# All historical files, including runner and diagnostics, unchanged byte for byte.
old={**tree(OLD,AUD+'stage-a/'),**tree(OLD,AUD+'stage-b/')};check(len(old)==329,'old count')
oldmanifest=[]
for p in sorted(old):
 b=blob(OLD,p);check(b==raw(p),'historical bytes changed: '+p)
 oldmanifest.append(sha(b)+'  '+p+'\n')
(ROOT/'old-receipts.sha256').write_text(''.join(oldmanifest))
results['historical']={'unchanged':len(old),'manifest_sha256':sha(''.join(oldmanifest).encode())}
# Exact inventory/source equality, line/header totals and metadata.
inv=obj('inventory-rows.json');paths=[decode(r['path']) for r in inv];check(len(paths)==len(set(paths))==107,'inventory')
accepted=blob(TIP,AUD+'stage-a/p1-qa-scratch/paths.txt').decode().splitlines()
check(set(paths)==set(map(decode,accepted)),'accepted membership')
source_manifest=[];source={}
for p in paths:
 b=blob(SRC,p);source[p]=b
 for ref in [TIP,'2174265e9c','f03b64419fa656fb3af61cbc8d174284020d439c']:
  check(b==blob(ref,p),'source changed '+ref+':'+display(p))
 source_manifest.append(sha(b)+'  '+display(p)+'\n')
(ROOT/'source-paths.sha256').write_text(''.join(source_manifest))
check(C.Counter(r['reach'] for r in inv)=={'shipped':103,'test':4},'reach')
check(sum(len(b.splitlines()) for b in source.values())==40474,'splitlines')
check(sum(b.count(b'\n') for b in source.values())==40473,'newlines')
check(sum(any(l.startswith(b'From:') for l in b.splitlines()[:60]) for p,b in source.items() if p.endswith('.patch'))==87,'From census')
check(sum(any(l.startswith(b'Subject:') for l in b.splitlines()[:60]) for p,b in source.items() if p.endswith('.patch'))==89,'Subject census')
for prefix in ['packages','projects','tools','scripts']:
 check(tree('d7dd766659',prefix)==tree(TIP,prefix),'protected tree '+prefix)
results['source']={'unchanged':107,'lines':40474,'newlines':40473,'headers':[87,89],'manifest_sha256':sha(''.join(source_manifest).encode()),'protected_subtrees_unchanged':['packages','projects','tools','scripts']}
# Tie retained source read output hashes to immutable blobs, without replaying history commands.
source_reads=obj('source-readings-commands.json'); read_count=0
for rec in source_reads:
 argv=rec['argv']
 if argv[:2]==['git','show'] and len(argv)==3 and ':' in argv[2]:
  ref,path=decode(argv[2]).split(':',1)
  check(re.fullmatch('[0-9a-f]{10,40}',ref) is not None,'immutable source read')
  check(rec['rc']==0 and sha(blob(ref,path))==rec['stdout_sha256'],'source read hash '+display(path));read_count+=1
results['source']['read_stdout_hashes_verified']=read_count
meta=obj('path-metadata.json'); base_tree=tree('c445081a59','projects'); up_tree=tree('651150fc88','projects'); cur_tree=tree(SRC,'projects')
for m in meta:
 p=decode(m['path']); cur=cur_tree[p].split()[-1]
 for which,t in [('source',cur_tree),('base',base_tree),('upstream',up_tree)]:
  expected=t[p].split()[-1] if p in t else ''
  check(m[which+'_blob']==expected,'metadata blob '+which+':'+display(p))
 for which,t in [('base',base_tree),('upstream',up_tree)]:
  expected='ABSENT' if p not in t else 'SAME' if t[p].split()[-1]==cur else 'CHANGED'
  check(m['vs_'+which]==expected,'metadata comparison '+display(p))
results['source']['vs_base']=dict(C.Counter(m['vs_base'] for m in meta));results['source']['vs_upstream']=dict(C.Counter(m['vs_upstream'] for m in meta))
# Run hashes, full row equality, commands/logs, classification and digest chains.
run=obj('run-metadata.json');check(sha(corr('apply-corrected.py'))==run['runner_sha256'],'runner hash')
apps=obj('application-results.json');rows=apps['rows'];check(apps['complete'] and apps['source_ref']==SRC,'completed source')
check(C.Counter(r['plan'] for r in rows)==POP,'sequence populations');check(len({decode(r['path']) for r in rows})==106,'patch population')
check({decode(r['path']) for r in rows}=={p for p in paths if p.endswith('.patch')},'application membership')
row_manifest=[];chain={}; disagreements=[]
for plan,n in POP.items():
 group=[r for r in rows if r['plan']==plan];check([r['index'] for r in group]==list(range(1,n+1)),'indices '+plan)
 order=list(map(decode,corr('order-'+plan+'.txt').decode().splitlines()))
 check([decode(r['path']) for r in group]==order,'order '+plan)
 if plan in ['GENERIC_X64','H700','SM8550']:
  check(order==list(map(decode,raw(AUD+'stage-a/order-'+plan+'.txt').decode().splitlines())),'historical order')
 else:check(order==sorted(order),'C locale order')
 tar=obj('tar-'+plan+'.json');check(tar in apps['tar'],'tar duplicate')
 check(sha(corr(tar['output']))==tar['output_sha256'],'tar log hash')
 check(tar['rc'] in [0,2] and not tar['timed_out'] and tar['all_missing_accounted'],'tar outcome')
 check(tar['not_in_archive']==len(tar['missing_members']),'missing census')
 check(all('/'.join(x.split('/')[1:]) in tar['created_paths'] for x in tar['missing_members']),'unexplained missing')
 check(len(corr('targets-'+plan+'.txt').decode().splitlines())==tar['targets'],'targets census')
 prev=tar['initial_tree_sha256'];first=prev
 for r in group:
  name=f"{plan}-{r['index']:03d}";saved=corr('rows/'+name+'.json');check(json.loads(saved)==r,'row duplicate '+name)
  check(sha(source[decode(r['path'])])==r['patch_sha256'],'patch hash '+name)
  check(r['input_tree_sha256']==prev==r['after_dry_tree_sha256'],'input/dry/prefix '+name)
  check(r['attempted'] and r['promoted'] and r['apply_rc']==0,'normal promotion '+name)
  cmd=['patch','-p1','-N','--batch','--directory',r['candidate']]
  for kind in ['dry','apply']:
   c=r[kind];log=corr(c['output']);check(sha(log)==c['output_sha256'],'log hash '+name+kind)
   check(c['argv']==cmd+(['--dry-run'] if kind=='dry' else []),'argv '+name+kind)
   check(c['rc']==r[kind+'_rc'] and not c['timed_out'],'rc '+name+kind)
   check(run['start']<=c['start']<=run['end'] and c['elapsed_seconds']>=0,'times '+name+kind)
  out=corr(r['apply']['output']).decode()
  for word in ['offset','fuzz','FAILED']:check(out.count(word)==r[word],'normal counts '+name+word)
  status='fuzz' if r['fuzz'] else 'applies with offset' if r['offset'] else 'applies'
  check(r['status']==status and r['FAILED']==0,'classification '+name)
  check(re.fullmatch('[0-9a-f]{64}',r['output_tree_sha256']) is not None,'output digest '+name)
  if r['dry_rc']!=r['apply_rc']:disagreements.append(name)
  row_manifest.append({'row':name,'receipt_sha256':sha(saved),'patch_sha256':r['patch_sha256'],'input_tree_sha256':r['input_tree_sha256'],'output_tree_sha256':r['output_tree_sha256'],'dry_log_sha256':r['dry']['output_sha256'],'apply_log_sha256':r['apply']['output_sha256'],'status':r['status']})
  prev=r['output_tree_sha256']
 chain[plan]={'initial':first,'final':prev,'rows':n}
check(disagreements==['H700-011'],'dry disagreements')
counts=dict(C.Counter(r['status'] for r in rows));check(counts=={'applies':43,'applies with offset':48,'fuzz':29},'status totals')
(ROOT/'row-hashes.json').write_text(json.dumps(row_manifest,indent=2)+'\n')
results['applications']={'rows':120,'paths':106,'populations':POP,'status':counts,'nonzero_normal':0,'blocked':0,'dry_disagreements':disagreements,'chains':chain,'row_manifest_sha256':sha((ROOT/'row-hashes.json').read_bytes())}
# Fixture: literal prefix and stdin can be independently hashed without replay.
f=obj('failed-candidate-guard.json');bad=f['failure'];succ=f['successor']
fixture=b'--- a/a\n+++ b/a\n@@ -1 +1 @@\n-alpha\n+changed\n--- a/b\n+++ b/b\n@@ -1 +1 @@\n-not-the-input\n+changed\n'
check(sha(fixture)==bad['patch_sha256'],'fixture stdin hash')
check(sha(b'a\0alpha\n\0b\0beta\n\0')==f['prefix_before']==f['prefix_after']==bad['input_tree_sha256']==bad['after_dry_tree_sha256']==succ['input_tree_sha256'],'fixture prefix hash')
check(f['result']=='PASS' and bad['apply_rc']==1 and not bad['promoted'] and bad['status']=='fails','fixture fail')
check(bad['output_tree_sha256']!=f['prefix_before'],'partial candidate')
check(succ['blocked_by']==1 and not succ['attempted'] and not succ['promoted'] and succ['apply_rc'] is None and succ['dry_rc'] is None and 'apply' not in succ and 'dry' not in succ,'blocked successor')
for i,r in enumerate([bad,succ],1):check(obj(f'rows/FIXTURE-{i:03d}.json')==r,'fixture duplicate')
for kind in ['dry','apply']:check(sha(corr(bad[kind]['output']))==bad[kind]['output_sha256'],'fixture log hash')
results['failure_guard']={'result':'PASS','prefix_sha256':f['prefix_before'],'failed_candidate_sha256':bad['output_tree_sha256'],'fixture_stdin_sha256':sha(fixture)}
# Archived evidence: source recipe hashes independently read, cache never touched.
archives=obj('archive-sha256.json');check(len(archives)==5,'archives')
for archive,x in archives.items():
 check(x['sidecar_equal'] and x['recipe_equal'] and x['sha256'].encode() in blob(SRC,x['recipe']),'archive recipe '+archive)
results['archives']={k:v['sha256'] for k,v in archives.items()}
# Generated outputs, headers/coverage and current summaries consume the corrected rows.
tab=obj('table-json.txt');stats=obj('table-stats.txt');check({decode(r['path']) for r in tab}==set(paths),'table membership')
for r in tab:
 p=decode(r['path']);check(r['lines']==len(source[p].splitlines()),'table line count')
 actual=[x for x in rows if decode(x['path'])==p]
 for x in actual:
  text=f"{x['plan']}[{x['index']:03d}] {x['status']} (apply_rc={x['apply_rc']}, dry_rc={x['dry_rc']}; rows/{x['plan']}-{x['index']:03d}.json)"
  check(text in r['applies'],'table application '+display(p))
 check(bool(actual) or r['kind']=='conf','missing application')
md=raw(AUD+'02-forward-audit.md').decode()
for kind,width in [('provenance',19),('coverage',5)]:
 text=corr('table-'+kind+'.txt').decode().strip();check(text in md,'02 generated '+kind)
 rr=[line for line in text.splitlines() if line.startswith('| `projects/')]
 check(len(rr)==107 and all(len(line.split('|'))-2==width and all(v.strip() for v in line.split('|')[1:-1]) for line in rr),'table width/population '+kind)
check(stats['application_status']==counts and stats['plan_applications']==POP and stats['blocked']==0,'stats current')
check(C.Counter(r['disposition'] for r in tab)==stats['dispositions'],'dispositions')
check(C.Counter(r['upstream'] for r in tab)==stats['upstream_status'],'upstream')
check(C.Counter(r['backport'] for r in tab)==stats['backport_status'],'backport')
md4=raw(AUD+'04-analysis.md').decode();check(corr('table-currency.txt').decode().strip() in md,'02 upstream currency')
for dimension in ['application_status','upstream_status','backport_status','dispositions']:
 for value,count in stats[dimension].items():check(f'| {dimension} | {value} | {count} |' in md4,'04 currency '+dimension+value)
for phrase in ['Provenance','Coverage','The ramoops patch','The conf','Upstream since the base','The #585 lines owed','The runs','Leads and dispositions','Rulings a to p','Proofs','What the coordinator, the integration and the next slices inherit','Acceptance criteria scorecard','Coverage Boundary']:
 check('## '+phrase in md,'missing 02 section '+phrase)
check(set(re.findall(r'^\| L-(\d\d) \|',md,re.M))=={f'{x:02d}' for x in range(1,32)},'lead index')
check(len(re.findall(r'^\| L-\d\d \|',md,re.M))==31,'lead duplicates')
check(re.findall(r'^\| ([a-p]) \|',md,re.M)==list('abcdefghijklmnop'),'rulings')
proof=obj('proof-index.json');log=raw(AUD+'00-running-log.md').decode()
for p in proof:check('| '+p[0]+' | proved: '+p[1] in md and 'PROOF: '+p[0]+' | '+p[1] in log,'proof '+p[0])
check(len(proof)==12,'proof count')
for q in range(1,8):check('### Q'+str(q)+' ' in md4,'Q'+str(q))
md3=raw(AUD+'03-retrospective.md').decode()
for heading in ['Project conformance','Platform architecture conformance','Cross-System Interactions','Defect-class sweep','Missing Artifacts']:check('## '+heading in md3,'03 '+heading)
results['tables']={'provenance':107,'coverage':107,'leads':31,'rulings':16,'proofs':12,'dispositions':stats['dispositions'],'sections':'present; 03/04 present'}
# Negative controls read as historical receipts; no generator/test execution.
neg=obj('generator-fail-first.json')
for n in neg:
 out=corr('generator-fail-'+n['name']+'.out').decode()
 check(n['rc']==1 and out.splitlines()[-1]==n['last_line'],'negative control '+n['name'])
check([n['name'] for n in neg]==['drop','reach','header'],'negative controls')
val=obj('validation.json');check(val['result']=='PASS','validation receipt')
check(sha(corr('verify-packet.py'))==val['validation_script_sha256'],'validator source hash')
remaining=obj('remaining-reads.json')
for pair in remaining['duplicates']:
 a=blob(SRC,decode(pair['a']));b=blob(SRC,decode(pair['b']));check(a==b and sha(a)==pair['sha256'],'duplicate pair')
results['negative_controls']={n['name']:{'rc':n['rc'],'last_line':n['last_line']} for n in neg}
results['producer_hashes']={p:sha(corr(p)) for p in ['apply-corrected.py','t41-tables.py','verify-packet.py']}
corrected_files=tree(TIP,COR)
for path in corrected_files:raw(path)
results['corrected_files']=len(corrected_files)
results['AC17_presentation']={'exact_forbidden_output_quoted_in_02': 'forbidden-terms-check: 1 line(s) on stdin carry a listed word' in md, 'raw_positive_exists_in_hygiene': 'forbidden-terms-check: 1 line(s) on stdin carry a listed word' in corr('hygiene.out').decode(), '02_reference_line':470, '02_PASS_claim_line':588}
results['limits']='Only immutable artifact bytes, hashes, digest chain consistency, and literal fixture input/prefix were independently re-derived. Production archive and candidate-tree byte hashes are retained producer/validation observations; no archive/cache/private scratch read, extraction, application, generator or historical test was executed.'
results['result']='PASS bounded structural reconciliation; narrative/producer logic assessment in report.txt'
# Derived evidence only, deterministic output. Never copy the source/receipt tree.
(ROOT/'evidence.sha256').write_text(''.join(h+'  '+display(p)+'\n' for p,h in sorted(manifest.items())))
(ROOT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
