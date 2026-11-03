from prooflib import *
import functools,collections,re
errors=[];facts={};checked=[];unresolved=[]
def check(ok,label,detail=None):
 if not ok:errors.append({'check':label,'detail':detail})
@functools.lru_cache(None)
def b(path):return blob(path)
names=git('ls-tree','-r','--name-only',FINAL,'--',A).decode().splitlines()
m=json.loads(ext('MANIFEST.json'));external={n:ext(n) for n in m['members']}
# Separate declared appendices; never infer they are core-manifest members.
appendices={}
for name in m['future_delivery_appendices']:
 try:appendices[name]=ext(name)
 except FileNotFoundError:unresolved.append({'appendix_not_present':name})
def ej(name):return json.loads(external[name] if name in external else appendices[name])
programs={};program_paths=[n for n in names if n.endswith('.py')]
for path in program_paths:programs.setdefault(sha(b(path)),[]).append(path)
recorder=sha(b(A+'tools/record.py'))
def path_hash(path):
 if path.startswith(A) or path in names or path.startswith('tools/'):
  try:return sha(b(path)),path
  except RuntimeError:return None,path
 if path.startswith(EXT+'/'):
  rel=path[len(EXT)+1:]
  if rel in external:return sha(external[rel]),'external:'+rel
  if rel in appendices:return sha(appendices[rel]),'appendix:'+rel
 return None,path
def receipt(label,x,getstream):
 if not isinstance(x,dict) or not all(k in x for k in ('argv','exit','stdout_sha256','stderr_sha256')):return
 for stream in ('stdout','stderr'):
  data=getstream(stream);check(sha(data)==x[stream+'_sha256'],'command output binding',label+'/'+stream)
 if 'producer_sha256' in x:check(x['producer_sha256']==recorder,'command recorder identity',label)
 if 'affinity' in x:check(x['affinity']==list(range(8,24)),'receipt affinity',label)
 if 'locale' in x:check(x['locale']=='C','receipt locale',label)
 if 'started' in x and 'finished' in x:check(x['started']<=x['finished'],'command time ordering',label)
 matches=[]
 for path,wanted in x.get('program_and_direct_inputs',{}).items():
  actual,where=path_hash(path)
  if actual==wanted:matches.append({'path':path,'bound_at':where,'sha256':wanted})
  elif wanted in programs:matches.append({'path':path,'bound_at_preserved_snapshot':programs[wanted],'sha256':wanted})
  else:errors.append({'check':'unmatched direct program/input hash','detail':{'receipt':label,'path':path,'expected':wanted,'final_hash':actual}})
 checked.append({'receipt':label,'argv':x['argv'],'exit':x['exit'],'started':x.get('started'),'finished':x.get('finished'),'direct_bindings':matches})
for n in names:
 if not n.startswith(tuple(A+'stage-'+s+'/' for s in 'efgh')) or not n.endswith('.json'):continue
 x=json.loads(b(n))
 if isinstance(x,dict) and all(k in x for k in ('argv','exit','stdout_sha256','stderr_sha256')):
  stem=n[:-5]
  if stem+'.stdout' in names and stem+'.stderr' in names:receipt(n,x,lambda s,stem=stem:b(stem+'.'+s))
for n,bb in external.items():
 if not n.endswith('.json'):continue
 x=json.loads(bb)
 if isinstance(x,dict) and all(k in x for k in ('argv','exit','stdout_sha256','stderr_sha256')):
  stem=n[:-5]
  if stem+'.stdout' in external and stem+'.stderr' in external:receipt('external:'+n,x,lambda s,stem=stem:external[stem+'.'+s])
for n,bb in appendices.items():
 if not n.endswith('.json'):continue
 try:x=json.loads(bb)
 except json.JSONDecodeError:continue
 stem=n[:-5]
 if stem+'.stdout' in appendices and stem+'.stderr' in appendices:receipt('appendix:'+n,x,lambda s,stem=stem:appendices[stem+'.'+s])
pub=ej('publication.json')
for name,claim in pub['checks'].items():
 x=ej(claim['receipt'])
 check(all(x[k]==claim[k] for k in ['exit','started','finished']),'publication named check',name)
for name in ['final-resolution.stdout','final-issue-resolution.stdout']:
 check('PASS' in external[name].decode(),'recorded resolution PASS',name)
for name in ['final-box-audit.stdout','final-box-slice-headers-v2.stdout']:
 check('0 fail' in external[name].decode(),'recorded issue check PASS',name)
check(external['status-final.stdout']==b'','recorded final status empty')
check(external['remote-final.stdout'].decode().split()[0]==FINAL,'recorded remote final hash')
# Tracker/readback comparisons use retained bytes and the full live owning issue reads.
def bodies(x):
 if isinstance(x,dict):
  if isinstance(x.get('body'),str):yield x['body']
  for v in x.values():yield from bodies(v)
 elif isinstance(x,list):
  for v in x:yield from bodies(v)
def body(x):return max(bodies(x),key=len)
live690=json.loads((P/'issue-690.stdout').read_text());live1412=json.loads((P/'issue-1412.stdout').read_text())
check(body(ej('source-header-readback-v2.json'))==live690['body'],'live690 final header readback')
check(body(ej('audit-final-readback.json'))==live1412['body'],'live1412 final readback')
original=body(ej('source-header-before.json'))
stripheads=lambda x:re.sub(r'^(reviewed-at|fixed-at):[^\n]*',lambda m:m.group(1)+':',x,flags=re.M)
check(stripheads(original)==stripheads(live690['body']),'690 only header values changed')
check(re.search(r'^reviewed-at: '+SEED+r'$',live690['body'],re.M) is not None and re.search(r'^fixed-at: '+FINAL+r'$',live690['body'],re.M) is not None,'live seed/final headers')
check(len(re.findall(r'^- \[ \]',live690['body'],re.M))==20 and len(re.findall(r'^- \[[xX]\]',live690['body'],re.M))==0,'20 root criteria unchecked')
check(len(re.findall(r'^- \[[xX]\]',live1412['body'],re.M))==1 and live1412['state']=='OPEN' and live690['state']=='OPEN','audit open custody checked')
check(A+'audit-completion.json' not in names,'completion marker absent')
retro='docs/retros/2026-11-02-m6-patches-unshipped.md';rbody=body(ej('retro-readback.json'));livecomments={x['url'].split('-')[-1]:x['body'] for x in live690['comments']}
check(rbody==livecomments['6591200156'],'retro exact live readback')
check(rbody.split('\n\n',1)[1]==b(retro).decode(),'retro exact file after dated post preface')
if 'handback-readback.json' in appendices:
 check(body(ej('handback-readback.json'))==livecomments['6591247872'],'handback exact live readback')
check(appendices.get('handback-request.md',b'').decode()==livecomments['6591247872'],'handback exact request body')
facts['receipts_checked']=len(checked);facts['receipt_exits']=dict(collections.Counter(str(x['exit']) for x in checked))
facts['core_files']=len(external);facts['core_bytes']=sum(map(len,external.values()));facts['appendices']={k:{'bytes':len(v),'sha256':sha(v)} for k,v in appendices.items()}
facts['publication_checks']=len(pub['checks']);facts['tracker']={'690_state':live690['state'],'690_unchecked':20,'1412_state':live1412['state'],'1412_checked':1,'marker_absent':True}
facts['retained_check_outputs']={n:external[n].decode() for n in ['final-resolution.stdout','final-issue-resolution.stdout','final-box-audit.stdout','final-box-slice-headers-v2.stdout','remote-final.stdout','status-final.stdout']}
(P/'reconcile-bindings-results.json').write_text(json.dumps({'errors':errors,'limits':unresolved,'facts':facts,'receipts':checked},indent=2)+'\n')
print(json.dumps({'errors':errors,'limits':unresolved,'facts':facts},indent=2))
