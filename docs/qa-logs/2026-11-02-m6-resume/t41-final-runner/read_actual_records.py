#!/usr/bin/env python3
"""Bounded immutable predicates only; no executable gates or live tracker reads.
Codex (GPT-6), /root, wN:p5, session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import datetime,hashlib,json,os,pathlib as P,sys,time
OWN=P.Path('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12')
TIP='61a1a674c10d520f9d93748c5a73deaadb08b158';COORD='10e055e3043b7bd41f9dcca3e04abce9d979817e';DISPATCH='d7dd76665983cb87dba62397691500fcf409fafe'
ALLOWED=set('pointer folder dist-tip product-paths membership tree-counts review-plan-local lint-proof punch-list ladder scope-record read-order tables generated analysis-face checker-run checker-record fixes-record inherited-record proof-lines proved rulings analysis record-lines runs-record running-log no-compile retro patch-untouched pins-read headers applies-record upstream-status tarball-hashes device-groups fork-written non-kernel runs'.split())
# Optional exact refs retain old default commands and receipts. No mutable refs.
if sys.argv[1:2]==['--tips']:
 TIP,COORD=sys.argv[2:4]
 assert all(len(ref)==40 and all(c in '0123456789abcdef' for c in ref) for ref in [TIP,COORD])
 sys.argv=[sys.argv[0],*sys.argv[4:]]
phase=sys.argv[1];sections=sys.argv[2:];assert phase.replace('-','').isalnum() and sections and set(sections)<=ALLOWED
out=OWN/'immutable-final-readback'/('readback-'+phase+'.json');out.parent.mkdir(exist_ok=True);assert not out.exists()
os.environ['DIST_REPO']='/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649';os.environ['DISPATCH_TIP']=DISPATCH;os.environ['GIT_CONFIG_GLOBAL']='/dev/null';os.environ.pop('ACCEPT_FIXTURE_ROOT',None)
ns={'__name__':'bounded_library'};sources={}
for name in ['t41_checks.py','t41_reconcile.py','t41_supplement.py']:
 raw=(OWN/name).read_bytes();sources[name]=hashlib.sha256(raw).hexdigest();source=raw.decode().split("\nif __name__=='__main__':")[0];exec(compile(source,name,'exec'),ns)
sys.argv=['bounded-reader',TIP,COORD];trace=[];base_git=ns['Reader'].git

def immutable_git(self,*args,missing=False):
 assert args[0] in ['ls-tree','show','merge-base','log','diff-tree','rev-parse','cat-file','diff']
 assert not any(x in args for x in ['--write-tree','--output','--textconv','--ext-diff'])
 start=time.monotonic();result=base_git(self,*args,missing=missing);trace.append(dict(argv=list(args),missing=missing,result_absent=result is None,output_sha256=None if result is None else hashlib.sha256(result).hexdigest(),elapsed_seconds=round(time.monotonic()-start,6)));return result
ns['Reader'].git=immutable_git
ns['Reader'].issues=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('live issue interface forbidden'))
r=ns['Reader']();results=[]
for section in sections:
 try:reason=ns['check'](r,section);state='PASS'
 except ns['Absent'] as e:state,reason='ABSENT',str(e)
 except ns['Cannot'] as e:state,reason='CANNOT',str(e)
 except Exception as e:state,reason='FAIL',type(e).__name__+': '+str(e)
 results.append(dict(section=section,state=state,reason=ns['fmt'](reason)));print(section,state,ns['fmt'](reason),flush=True)
evidence={}
if any(x['section']=='checker-run' and x['state']=='PASS' for x in results):
 headers=ns['d228_overlay_paths'](r)
 paths=[r.af+'/'+x for x in ['01-research-notes.md','stage-a/order.out','stage-a/run/stage-a-extra.out','stage-a/run/stage-a.out']]
 records=[]
 for path in paths+sorted(headers):
  anchor=ns['STAGE_D'] if path in paths else r.tip
  actual=r.tree(r.tip,path);expected=r.tree(anchor,path) if path in paths else {path:headers[path]}
  records.append(dict(path=path,mode_blob=actual.get(path),sha256=ns['sha'](r.blob(path)),anchor=anchor,identical=actual==expected))
 evidence['six_whitespace_input_identities']=records
 proof_paths=['stage-f/generator-input-proof/manifest.json','stage-f/generator-input-proof-attempt-1/manifest.json','stage-f/generator-input-proof-attempt-1/serialization-error.json','stage-f/generator-input-proof/source-identities.json','stage-f/generator-input-proof/run.py','stage-f/generator-input-proof-attempt-1/run.py','stage-h/first-validation-attempt/failure.txt']
 evidence['named_public_records']=[dict(path=r.af+'/'+path,sha256=ns['sha'](r.audit(path)),size_bytes=len(r.audit(path))) for path in proof_paths]
 selected=sorted(ns['dec'](x['path']) for x in r.inventory());before=r.tree(ns['SOURCE'],'');after=r.tree(r.tip,'')
 evidence['selected_sources']=dict(count=len(selected),unchanged=all(before[p]==after[p] for p in selected),identity_digest=ns['sha'](('\n'.join(p+'\t'+before[p]+'\t'+ns['sha'](r.blob(p,ns['SOURCE'])) for p in selected)+'\n').encode()))
 old={**r.tree(ns['OLD_RECEIPTS'],r.af+'/stage-a/'),**r.tree(ns['OLD_RECEIPTS'],r.af+'/stage-b/')}
 evidence['old_receipts']=dict(count=len(old),unchanged=all(after[p]==entry and r.blob(p)==r.blob(p,ns['OLD_RECEIPTS']) for p,entry in old.items()),identity_digest=ns['sha'](('\n'.join(p+'\t'+old[p] for p in sorted(old))+'\n').encode()))
packet=dict(identity='Codex (GPT-6), /root, wN:p5',session='01a19d12-1c5f-7022-8053-102f6a94b7fe',immutable_evidence=evidence,scope='immutable receipt/record predicates only; not final acceptance',tip=TIP,coordinator=COORD,dispatch=DISPATCH,time=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate_sha256=sources,results=results,git_reads=trace)
with out.open('x') as f:json.dump(packet,f,indent=2);f.write('\n')
print('receipt',out,'SHA256',hashlib.sha256(out.read_bytes()).hexdigest())
sys.exit(1 if any(x['state']=='FAIL' for x in results) else 2 if any(x['state']!='PASS' for x in results) else 0)
