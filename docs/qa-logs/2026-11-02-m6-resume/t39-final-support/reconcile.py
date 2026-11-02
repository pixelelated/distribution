#!/usr/bin/env python3
"""Immutable metadata/receipt reconciliation only; does not execute project code."""
import collections,hashlib,json,pathlib,re,subprocess
P=pathlib.Path(__file__).resolve().parent
R='/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641'
T='4eb5dfab8e745914a55e7de3e5a43c5b91ebc608'; B='86ebb6dffce7bec2dda6296bd84dd225a28b1347'
K='329011b9eae20922b4d0727e13bf1626b2e1c04f'; M='24a5e0e294607bc6fc99025873cb063d26c9a4da'
AD='96ef183aae39da587e5dc51d19d7c1fc9e850704'; A='docs/audits/2026_11_01-epic-m6-doctrine-reference/'
commands=[];hashes={}
def g(*args):
 commands.append(['git','-C',R,*args]);return subprocess.check_output(commands[-1])
def b(ref,p):return g('show',ref+':'+p)
def h(x):return hashlib.sha256(x).hexdigest()
def read(p):
 raw=b(T,A+p);hashes[A+p]=h(raw);return raw
def j(p):return json.loads(read(p))
def tree(ref,paths):
 out={}
 for row in g('ls-tree','-rz',ref,'--',*paths).split(b'\0'):
  if row:
   meta,path=row.split(b'\t',1);out[path.decode()]=meta.decode()
 return out
def snap(n):return json.loads((P/f'issue-{n}.json').read_text())
res={'identity':'Codex / OpenAI; session 01a19d11-dda5-72e3-86f9-416f36341c24; wN:p3 m6-p1-survey',
 'refs':{'tip':T,'reviewed':B,'coordinator':K,'merge':M,'accepted_ad':AD}}
res['merge_parents']=g('show','-s','--format=%P',M).decode().split()
full=g('log','--no-merges','--format=%H',B+'..'+T).decode().splitlines()
lane=g('log','--no-merges','--format=%H',B+'..'+T,'--not',K).decode().splitlines()
res['history']={'unfiltered_count':len(full),'lane_count':len(lane),'imported_count':len(set(full)-set(lane)), 'lane_commits':lane}
ledger=['docs/reviews','docs/releases/catalog.md','docs/pr-series/map.txt','docs/releases/rc-accept.txt','docs/vm-qa-log.md','docs/cloud-sync-changelog.md','docs/rasteratops/p0-sweep-hits.txt','plans']
ro=['licenses','documentation','LICENSE.md','docs/upstream']
protected=ledger+ro+['.claude','CLAUDE.md','AGENTS.md','NAMING.md','tools','scripts','packages','projects']
res['criterion5_protected_diff_stat']=g('diff','--stat',B,T,'--',*protected).decode()
res['criterion5_protected_paths']=g('diff','--name-only',B,T,'--',*protected).decode().splitlines()
res['criterion12_unfiltered_commits']=g('log','--no-merges','--format=%H',B+'..'+T,'--',*ledger).decode().splitlines()
res['criterion12_excluding_coordinator']=g('log','--no-merges','--format=%H',B+'..'+T,'--not',K,'--',*ledger).decode().splitlines()
res['criterion13_unfiltered_commits']=g('log','--no-merges','--format=%H',B+'..'+T,'--',*ro).decode().splitlines()
regdiff=g('diff','--no-ext-diff',B,T,'--','docs/decision-register.md','docs/blindspot-register.md','docs/friction-log.md').decode()
res['removed_register_lines']=len([l for l in regdiff.splitlines() if l.startswith('-') and not l.startswith('---')])
mf=j('stage-f/source-diff-manifest.json'); rows=mf['source_paths']; paths=[r['path'] for r in rows]
res['source']={'manifest_count':len(paths),'sha_mismatch':[],'mode_blob_mismatch_F_merge_final':[]}
ts=[tree(ref,paths) for ref in [mf['checked_commit'],M,T]]
for row in rows:
 p=row['path']
 if h(b(B,p))!=row['before_sha256'] or h(b(T,p))!=row['after_sha256']:res['source']['sha_mismatch'].append(p)
 if not ts[0][p]==ts[1][p]==ts[2][p]:res['source']['mode_blob_mismatch_F_merge_final'].append(p)
res['source']['source_rows_by_stream']=dict(collections.Counter(s for r in rows for s in r['streams']))
members=read('stage-a/paths.txt').decode().splitlines()
changed=set(g('diff','--name-only',B,T,'--',*members).decode().splitlines())
res['source']['changed_membership_paths']=len(changed)
res['source']['changed_membership_outside_manifest']=sorted(changed-set(paths))
res['source']['final_vs_coordinator_membership']=g('diff','--name-only',K,T,'--',*members).decode().splitlines()
held=j('stage-f/binary-art-comparisons.json')['rows']; hp=[r['path'] for r in held]
tb=tree(B,hp);tt=tree(T,hp)
res['protected']={'count':len(held),'classes':dict(collections.Counter(r['class'] for r in held)),
 'mode_blob_mismatch':[p for p in hp if tb[p]!=tt[p]],'recorded_hash_mismatch':[r['path'] for r in held if r['before_sha256']!=r['after_sha256']]}
pp=[A+x for x in ['stage-a','stage-b','stage-c','stage-d','second-opinions']]
ta=tree(AD,pp); tf=tree(T,pp)
res['accepted_preservation']={'count':len(ta),'missing_changed':[p for p in ta if ta[p]!=tf.get(p)],'added':sorted(set(tf)-set(ta))}
out=j('stage-f/outcomes.json')['outcomes']; punch=read('05-punch-list.md').decode(); live=snap(1406)['body']
gate=punch.split('## Phase 7 resolution gate',1)[1]
res['outcomes']={'count':len(out),'counts':dict(collections.Counter(r['outcome'] for r in out)),
 'missing_gate':[r['item'] for r in out if f"| {r['item']} | {r['outcome']} |" not in gate],
 'live_checkboxes':dict(collections.Counter(re.findall(r'^- \[([ xX])\] PL-\d+',live,re.M))),
 'live_outcome_mismatch':[]}
for r in out:
 part=live.split('### '+r['item']+':',1)[1].split('\n### ',1)[0]
 if '**'+r['outcome']+'**' not in part:res['outcomes']['live_outcome_mismatch'].append(r['item'])
q=j('stage-e/S5/dispositions.json');res['q5']={'rows':len(q),'lines':sum(r['accepted_logical_lines'] for r in q),
 'decisions':dict(collections.Counter(r['decision'] for r in q))}
forward=read('02-forward-audit.md').decode();log=read('00-running-log.md').decode()
proof=re.findall(r'`proved: (tree|history|tool-run|fixture|design)`',forward)
plog=re.findall(r'^PROOF: .*proved: (tree|history|tool-run|fixture|design)$',log,re.M)
res['proofs']={'forward':len(proof),'log':len(plog),'classes_equal_in_order':proof==plog}
res['checker_hashes']={p:h(read(p))==v['current_sha256'] for p,v in j('stage-h/checker-changes.json')['files'].items()}
res['raw_receipts']=[]
for part in ['stage-f','stage-h']:
 for row in j(part+'/raw-receipt-map.json'):
  raw=b(T,row['exact_raw']); hashes[row['exact_raw']]=h(raw); obj=json.loads(raw); display=b(T,row['display'])
  normalized='\n'.join(x.rstrip() for x in obj['raw'].splitlines())+'\n'
  res['raw_receipts'].append({'path':row['exact_raw'],'sha_matches':h(obj['raw'].encode())==obj['sha256'], 'display_matches':display.decode()==normalized})
res['h_controls']=j('stage-h/provenance-controls.json')['cases']
res['harness_receipts']=[]
for part in ['stage-e','stage-f','stage-h']:
 files=g('ls-tree','-r','--name-only',T,'--',A+part).decode().splitlines()
 for p in files:
  if p.endswith('/harness.out'):
   raw=b(T,p);hashes[p]=h(raw);text=raw.decode();cmd=text.splitlines()[0]
   res['harness_receipts'].append({'path':p,'command':cmd,'rc':re.findall(r'^rc=(\d+)$',text,re.M),
    'total':re.findall(r'^TOTAL: .+$',text,re.M),'commit':re.findall(r'--commit ([a-f0-9]+)',cmd),
    'step_results':re.findall(r'^(?:ok  |FAIL)\s+\w+.*$',text,re.M)})
res['streams']=[]
for n in range(1,6):
 r=j(f'stage-e/S{n}/result.json');cand=g('rev-parse',r['candidate']+'^{tree}').decode().strip();commit=g('rev-parse',r['commit']+'^{tree}').decode().strip()
 s=[p for p in r['staged_paths'] if p in members]
 res['streams'].append({'stream':n,'commit':r['commit'],'candidate_rc':r['candidate_rc'],'committed_rc':r['committed_rc'],
  'candidate_tree_matches_record':cand==r['tree'],'committed_tree_equals_candidate':commit==cand,
  'source_paths':len(s),'candidate_source_equals_committed':tree(r['candidate'],s)==tree(r['commit'],s)})
res['h_checks']=j('stage-h/checks/results.json')
for r in res['h_checks']:
 raw=b(T,r['receipt']);hashes[r['receipt']]=h(raw);r['actual_tail_rc']=re.findall(r'^rc=(\d+)$',raw.decode(),re.M)
res['final_tip_harness_receipts']=[r['path'] for r in res['harness_receipts'] if r['commit']==[T]]
res['actual_final_nonowned_delta']=g('diff','--name-only',K,T,'--',*protected).decode().splitlines()
for name,data in [('results.json',res),('commands.json',commands),('artifact-hashes.json',hashes)]:
 (P/name).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k not in ['harness_receipts','h_checks','raw_receipts','h_controls']},indent=2))
print('raw-companions',len(res['raw_receipts']),'mismatches',[r for r in res['raw_receipts'] if not(r['sha_matches'] and r['display_matches'])])
print('harness receipts',len(res['harness_receipts']))
