import os,json,subprocess,hashlib,collections,importlib.util,copy,traceback
from pathlib import Path
p=Path('/tmp/m6-t46-records-proof-t5-20261103'); repo=Path('/workspace/tmp/m6-t46-proof-t5-20261103/repo'); ref='e9d512a230cf8dbd2cd985ae7984a6ef7eb9f9fc'; source='d707c82ab8c48b674acc1f95a9571f0cb24d226a'
assert set(os.sched_getaffinity(0))==set(range(8,24)); receipts=[]; results={}
def sha(b):return hashlib.sha256(b).hexdigest()
def run(args,data=None,okay=True):
 q=subprocess.run(args,cwd=repo,input=data,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')); receipts.append({'argv':args,'rc':q.returncode,'stdin_sha256':sha(data) if data is not None else None,'stdout_bytes':len(q.stdout),'stdout_sha256':sha(q.stdout),'stderr_sha256':sha(q.stderr)})
 if okay:assert q.returncode==0,q.stderr
 return q
def git(*a,data=None):return run(['git',*a],data).stdout
def inp(n):return json.loads((p/'inputs'/n).read_bytes())
try:
 retention=inp('p1-routes/retention.json'); decoded={}; checks=[]
 for r in retention['files']:
  b=(p/'inputs/p1-routes'/r['stored_name']).read_bytes(); assert sha(b)==r['stored_sha256']
  original=json.loads(b)['text'].encode('utf-8') if r['encoding']!='original' else b
  assert sha(original)==r['original_sha256'] and len(original)==r['original_bytes'];decoded[r['original_name']]=original;checks.append(r['original_name'])
 results['p1_original_files_verified']=checks
 rv=inp('root-route-verification.json');results['retained_five_output_readback']=rv['equal'];assert len(rv['equal'])==5 and all(rv['equal'].values())
 rs=inp('p1-routes/routes.json'); md=inp('p1-routes/target-metadata.json'); rootrs=inp('reader-routes.json'); prefixes=['docs/qa-logs','docs/qa-frames','docs/audits','docs/work-logs','docs/retros','docs/retrospective','docs/futros','research','.github/sessions']
 chosen=[{**r,'classification':'literal-records-route','target':md[r['resolved_path']]} for r in rs if r.get('resolved_path') and (r['resolved_path']=='docs/reviews/inventory.json' or any(r['resolved_path']==x or r['resolved_path'].startswith(x+'/') for x in prefixes))]
 assert chosen==rootrs['routes']; paths=sorted({r['resolved_path'] for r in chosen});assert len(chosen)==95 and len(paths)==89
 days=[x for x in chosen if x['entrypoint']=='docs/work-logs/INDEX.md'];assert len(days)==86 and len({r['resolved_path'] for r in days})==86 and all(not r.get('anchor') and not r.get('line_suffix') for r in days)
 results['route_join']={'occurrences':len(chosen),'targets':len(paths),'day_logs':86,'other_targets':[x for x in paths if x not in {r['resolved_path'] for r in days}],'88_blobs_1_directory':collections.Counter(md[x]['type'] for x in paths)=={'blob':88,'tree':1},'path_sha256':sha(b''.join(x.encode()+b'\0' for x in paths))}
 results['p1_summary']=inp('p1-routes/summary.json'); results['shorthand_count']=len(inp('p1-routes/structural-findings.json')['handoff_shorthand'])
 helper=repo/'docs/qa-logs/2026-11-03-m6-records-preparation/inputs.py'
 ns={'__name__':'t5_source_binding'};exec(compile(helper.read_bytes(),str(helper),'exec'),ns)
 rows=ns['parse'](git('ls-tree','-r','-l','-z',source,'--',*ns['ROOTS'])); total=ns['check'](rows,ns['TREE'],ns['INPUTS']);results['metadata_positive']=total
 negatives={}
 first=b'docs/reviews/inventory.json';assert first in rows
 for name in ['missing','extra','mode','blob','size','canonical-input','empty-subtree-root']:
  changed=dict(rows);tree=ns['TREE'];inputs=dict(ns['INPUTS'])
  if name=='missing':changed.pop(first)
  elif name=='extra':changed[b'docs/qa-logs/t5-synthetic-only']=rows[first]
  elif name in ('mode','blob','size'):
   v=list(changed[first]);i={'mode':0,'blob':2,'size':3}[name];v[i]={'mode':'100755','blob':'0'*40,'size':v[3]+1}[name];changed[first]=tuple(v)
  elif name=='canonical-input':inputs['docs/reviews/areas.json']='0'*40
  else:tree='0'*40
  try:ns['check'](changed,tree,inputs);negatives[name]='UNEXPECTED ACCEPT'
  except ValueError as e:negatives[name]=str(e)
 assert all(v!='UNEXPECTED ACCEPT' for v in negatives.values());results['own_binding_refusals']=negatives
 empty=git('mktree',data=b'').decode().strip()
 base=git('ls-tree','-z',source)
 extra=git('mktree','-z',data=base+b'040000 tree '+empty.encode()+b'\tt5-proof-empty\0').decode().strip()
 def commit(tree):
  data=('tree '+tree+'\nparent '+source+'\nauthor Codex T5 <codex@local.invalid> 1793710000 +0000\ncommitter Codex T5 <codex@local.invalid> 1793710000 +0000\n\nT5 private metadata handoff fixture only\n').encode()
  return git('hash-object','-t','commit','-w','--stdin',data=data).decode().strip()
 drift=commit(extra);same=commit(ns['TREE'])
 leaf=git('ls-tree','-r','-l','-z',drift,'--',*ns['ROOTS']);assert ns['parse'](leaf)==rows
 for name,pin in [('empty-subtree',drift),('same-tree-new-commit',same)]:
  q=run(['python3','-B',str(helper),'--repo',str(repo),'--ref',pin,'--out',str(p/('fixture-'+name))],okay=False)
  results[name]={'commit':pin,'root_tree':extra if name=='empty-subtree' else ns['TREE'],'rc':q.returncode,'stdout':q.stdout.decode(),'stderr_final_line':q.stderr.decode().splitlines()[-1] if q.stderr else ''}
 bridge=inp('t1-report.json');observations=[]
 def meta(pin,paths):
  raw=git('ls-tree','-l','-z',pin,'--',*paths);out={}
  for line in raw.split(b'\0'):
   if not line:continue
   head,path=line.split(b'\t',1);mode,kind,oid,size=head.split();out[path.decode()]={'mode':mode.decode(),'type':kind.decode(),'oid':oid.decode(),'bytes':int(size)}
  return out
 print('BRIDGE METADATA FIELD SAMPLE',json.dumps(bridge['path_bridge'][0]['candidate']))
 for key in ['pins','boundaries']:print('BRIDGE',key,json.dumps(bridge[key])[:5000])
 results['bridge_retained']={'paths':len(bridge['path_bridge']),'counts':bridge['counts'],'accepted_equals_completion':bridge['completion_all_48_equal_accepted'],'root_readback':{k:v for k,v in inp('root-t39-bridge-verification.json').items() if k!='commands'}}
 candidate=meta(source,[x['path'] for x in bridge['path_bridge']])
 for row in bridge['path_bridge']:
  observed=candidate[row['path']]; expected=row['candidate']
  # Retained schemas use either oid/size or blob/bytes; normalize explicitly.
  eo=expected.get('oid',expected.get('blob')); es=expected.get('bytes',expected.get('size'))
  observations.append(observed['mode']==expected['mode'] and observed['type']==expected['type'] and observed['oid']==eo and observed['bytes']==es and expected==row['pre_correction'] and row['accepted_source']==row['completion_source'])
 assert len(observations)==48 and all(observations);results['t39_cutoff_readback']=48
 for file in ['tools/lint-audit-artifacts','tools/box-check','tools/work-log-index','tools/ceremony-check','tools/forbidden-terms-check']:
  b=git('show',ref+':'+file);ls=b.decode().splitlines();print('TOOL',file,'sha256',sha(b))
  if file.endswith('lint-audit-artifacts'):
   dst=p/'lint-audit-artifacts.py';dst.write_bytes(b)
   for i,line in enumerate(ls):
    if any(s in line for s in ['PRIMARY','MODEL','primary','reviewers','def check_review','def validate','Local','def lint']):
     print(str(i+1)+': '+' | '.join(ls[max(0,i-1):min(len(ls),i+3)]))
  else:
   for i,line in enumerate(ls):
    if any(s in line for s in ['add_argument','usage:','Usage:','--gate','--write','--check','--stdin']):print(str(i+1)+': '+line)
 print('ROOT HELP RESULTS',[(r['argv'],r['exit']) for r in inp('tool-help.json')])
 print('INITIAL CHECK RESULTS',[(r['argv'],r['exit']) for r in inp('candidate-checks-initial.json')])
 print('RULE DIFF',git('diff','--name-only','f1000e157c2f0248820e1b77055e81521b079a3f',ref,'--','.claude/rules','AGENTS.md','CLAUDE.md').decode())
 print('RESULTS',json.dumps(results,indent=2))
except Exception:
 results['failure']=traceback.format_exc();print(results['failure'])
finally:
 (p/'command-07.json').write_text(json.dumps(receipts,indent=2)+'\n');(p/'proof-07.json').write_text(json.dumps(results,indent=2)+'\n')
