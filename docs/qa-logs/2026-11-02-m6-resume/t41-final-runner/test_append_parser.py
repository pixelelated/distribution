#!/usr/bin/env python3
"""Pure append parser only: immutable git show/merge-base reads, in-memory bytes.
No FinalGates, Git merge, checker, generator, producer or index write is invoked.
Codex (GPT-6), /root, wN:p5, session01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import ast,datetime,hashlib,json,os,pathlib as P,re,subprocess,sys
OWN=P.Path(__file__).parent;OUT=OWN/'append-parser-review';OUT.mkdir(exist_ok=True)
BASE_REF='d7dd76665983cb87dba62397691500fcf409fafe';COORD='afdec2bf8b88135befcb7ec56efb3a7ea327bd73';TIP='e481e4a4a5c296c8f12e9654b6a45c4fb27bd3b0';PATH='docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md'
REPO='/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649';phase=sys.argv[1];assert re.fullmatch(r'[a-z0-9-]+',phase)
receipt=OUT/(phase+'.json');assert not receipt.exists(),'retain each prior result'
sha=lambda b:hashlib.sha256(b).hexdigest()
source=(OWN/'t41_execution.py').read_text();module=ast.parse(source);function=next(x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='merge_append_bytes');pure=ast.Module(body=[function],type_ignores=[])
fragment=ast.get_source_segment(source,function)+'\n'
if phase=='before':(OUT/'before-function.py').write_text(fragment)
class Invalid(Exception):pass
def need(ok,reason):
 if not ok:raise Invalid(reason)
ns=dict(need=need,sha=sha,re=re,datetime=datetime,Invalid=Invalid)
exec(compile(pure,'isolated-merge-append-bytes','exec'),ns);merge=ns['merge_append_bytes']
env=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_COUNT='0',GIT_OPTIONAL_LOCKS='0');reads=[]
def git(*args):
 assert args[0] in ['show','merge-base']
 p=subprocess.run(['git','--no-optional-locks','-C',REPO,*args],env=env,capture_output=True);assert p.returncode==0,p.stderr
 reads.append(dict(argv=list(args),rc=p.returncode,stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr)));return p.stdout
need(git('merge-base','--all',COORD,TIP).strip().decode()==BASE_REF,'unexpected merge-base')
raw=[git('show',ref+':'+PATH) for ref in [BASE_REF,COORD,TIP]]
identities=[dict(ref=ref,path=PATH,size_bytes=len(b),sha256=sha(b),base_prefix=b.startswith(raw[0])) for ref,b in zip([BASE_REF,COORD,TIP],raw)]
RESULTS=[]
def test(label,fn,expected='PASS'):
 try:details=fn();state='PASS';reason=''
 except Invalid as e:state='Invalid';reason=str(e);details=None
 except Exception as e:state=type(e).__name__;reason=str(e);details=None
 ok=state==expected;RESULTS.append(dict(label=label,ok=ok,state=state,reason=reason,details=details));print(('PASS' if ok else 'FAIL')+' TEST '+label+': '+state,flush=True)

def actual():
 out,sequences=merge(*raw);assert out.startswith(raw[0]);assert b'<<<<<<<' not in out
 # Independent byte conservation: keep each original suffix entry's separator,
 # heading and full body. Each original sequence must remain a subsequence.
 def entries(suffix):
  heads=list(re.finditer(rb'^## ',suffix,re.M));cuts=[0]
  for h in heads[1:]:
   i=h.start()
   while suffix[i-1:i]==b'\n':i-=1
   cuts.append(i+1)
  return [suffix[a:b] for a,b in zip(cuts,cuts[1:]+[len(suffix)])] if suffix else []
 merged=entries(out[len(raw[0]):]);assert len(merged)==len(set(merged))
 for side in raw[1:]:
  blocks=entries(side[len(raw[0]):]);positions=[merged.index(b) for b in blocks];assert positions==sorted(positions)
 assert set(merged)==set(entries(raw[1][len(raw[0]):])+entries(raw[2][len(raw[0]):]))
 assert sequences==[[sha(b) for b in entries(side[len(raw[0]):])] for side in raw[1:]]
 # Persist identities only, never the merged real log or exported source tree.
 return dict(output_sha256=sha(out),output_bytes=len(out),appended_entries=len(merged),coordinator_entries=len(sequences[0]),lane_entries=len(sequences[1]),entry_sequences=sequences,all_original_entry_bytes_and_orders_preserved=True)

test('actual immutable base/coordinator/lane log bytes',actual,'Invalid' if phase=='before' else 'PASS')
if phase!='before':
 BASE=b'# Synthetic work log\n\n## 00:01 UTC -- base\n\nbase body\n'
 def entry(stamp,title='new',body='body',sep='\n',dash='—'):return (sep+'## '+stamp+' '+dash+' '+title+'\n\n'+body+'\n').encode()
 def case(left,right=b''):
  out,seq=merge(BASE,BASE+left,BASE+right);assert out.startswith(BASE);return dict(output_sha256=sha(out),sequence_lengths=list(map(len,seq)))
 for stamp in ['23:59 UTC','2026-11-02 19:21:17 UTC','2026-11-02T20:04:47.930461+00:00','2026-11-02T20:04:47+00:00','2026-11-02T20:04:47Z','2024-02-29 00:00:00 UTC']:
  test('valid UTC timestamp '+stamp,lambda stamp=stamp:case(entry(stamp)))
 test('mixed forms and separator bytes preserved',lambda:case(entry('11:00 UTC','first',sep='\n\n')+entry('2026-11-02T20:04:47.930461+00:00','last'),entry('2026-11-02 19:21:17 UTC','other')))
 for stamp in ['24:00 UTC','12:60 UTC','9:05 UTC','2026-02-29 19:21:17 UTC','2026-11-31 19:21:17 UTC','0000-11-02 19:21:17 UTC','2026-11-02 24:00:00 UTC','2026-11-02 19:21:60 UTC','2026-11-02 19:21 UTC','2026-11-02T20:04:47.930461+01:00','2026-11-02T20:04:47-00:00','2026-11-02T20:04:47','2026-11-02T20:04:47z','2026-11-02T20:04:47.1234567+00:00','2026-13-02T20:04:47Z','2026-11-02T25:04:47Z','2026-11-02 19:21:17 PST','not-a-timestamp','00:25-05:15 UTC']:
  test('invalid timestamp '+stamp,lambda stamp=stamp:case(entry(stamp)),'Invalid')
 X=entry('2026-11-02 19:21:17 UTC','shared');Y=entry('2026-11-02T20:04:47.930461+00:00','later')
 test('identical complete entry deduplicates',lambda:case(X,X))
 test('same timestamp distinct titles preserved',lambda:case(X,entry('2026-11-02 19:21:17 UTC','distinct')))
 test('same heading changed body refused',lambda:case(X,entry('2026-11-02 19:21:17 UTC','shared','different')),'Invalid')
 test('opposed append orders refused',lambda:case(X+Y,Y+X),'Invalid')
 test('duplicate heading in same suffix refused',lambda:case(X+X),'Invalid')
 test('duplicate base heading refused',lambda:case(entry('00:01 UTC','base',dash='--')),'Invalid')
 test('base byte edited refused',lambda:merge(BASE,BASE.replace(b'base body',b'edited')+X,BASE+Y),'Invalid')
 test('base entry removed refused',lambda:merge(BASE,b'# Synthetic work log\n'+X,BASE+Y),'Invalid')
 test('partial body lacks final newline refused',lambda:case(X[:-1]),'Invalid')
 test('missing blank separator refused',lambda:case(X.lstrip(b'\n')),'Invalid')
 test('bodyless entry refused',lambda:case(entry('2026-11-02 19:21:17 UTC','empty','')),'Invalid')
 test('trailing unexplained blank line refused',lambda:case(X+b'\n'),'Invalid')
 test('heading without title refused',lambda:case(entry('2026-11-02 19:21:17 UTC','')),'Invalid')
 test('no suffix on one side preserves other',lambda:case(b'',Y))
 test('no suffix on either side preserves base',lambda:case(b'',b''))
packet=dict(identity='Codex (GPT-6), /root, wN:p5',session='01a19d12-1c5f-7022-8053-102f6a94b7fe',scope='pure parser and immutable reads only; no Git merge or final gates',phase=phase,source_sha256=sha(source.encode()),pure_function_sha256=sha(fragment.encode()),inputs=identities,git_reads=reads,results=RESULTS)
with receipt.open('x') as f:json.dump(packet,f,indent=2);f.write('\n')
bad=sum(not x['ok'] for x in RESULTS);print('PURE PARSER SUMMARY',len(RESULTS)-bad,'passed,',bad,'failed',receipt,sha(receipt.read_bytes()));raise SystemExit(bool(bad))
