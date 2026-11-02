#!/usr/bin/env python3
"""Narrow pure issue-body predicate; supplied root capture only, no live API/gates.
Codex (GPT-6), /root, wN:p5, session01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import ast,copy,hashlib,json,pathlib as P,re,sys,types
OWN=P.Path(__file__).parent;OUT=OWN/'issue-body-review';OUT.mkdir(exist_ok=True)
phase=sys.argv[1];assert re.fullmatch('[a-z0-9-]+',phase);receipt=OUT/(phase+'.json');assert not receipt.exists()
TIP='e481e4a4a5c296c8f12e9654b6a45c4fb27bd3b0';COORD='afdec2bf8b88135befcb7ec56efb3a7ea327bd73';DISPATCH='d7dd76665983cb87dba62397691500fcf409fafe'
CAPTURE=P.Path('/tmp/m6-lane-progress/t41-issue-live-final-gate.json');ROOT=OWN/'root-final-e481-20261102T2023';RAW=ROOT/'evidence/final-gates-_n6wydcg/0001-live-688.stdout'
sha=lambda b:hashlib.sha256(b).hexdigest();a=CAPTURE.read_bytes();b=RAW.read_bytes();assert a==b
issue=json.loads(a);assert issue['number']==688
frozen_paths=[CAPTURE,RAW,*[p for p in ROOT.iterdir() if p.is_file()]]
# The installed shared runner is read for identity only and is never edited.
installed=P.Path('/workspace/tmp/m6-coordinator/kit/t41-accept.sh')
if installed.is_file():frozen_paths.append(installed)
frozen=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in frozen_paths]
source=(OWN/'t41_checks.py').read_text();tree=ast.parse(source)
names={'check','fixed_header','need','Absent','Cannot','Invalid'}
nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names];assert {n.name for n in nodes}==names
ns={'re':re};exec(compile(ast.Module(body=nodes,type_ignores=[]),'pure-issue-body','exec'),ns)
if phase=='before':
 with (OUT/'before-t41_checks.py').open('x') as f:f.write(source)
RESULTS=[]
def test(label,change=None,expected='PASS',reason_contains=None):
 v=copy.deepcopy(issue)
 if change:change(v)
 calls=[]
 def issues(n,comments=False):
  assert n==688 and not comments;calls.append(n);return v
 r=types.SimpleNamespace(tip=TIP,coord=COORD,dispatch=DISPATCH,issues=issues)
 try:reason=ns['check'](r,'issue-body');state='PASS'
 except ns['Invalid'] as e:reason=str(e);state='FAIL'
 except ns['Absent'] as e:reason=str(e);state='ABSENT'
 except Exception as e:reason=type(e).__name__+': '+str(e);state='UNEXPECTED'
 ok=state==expected and calls==[688] and (reason_contains is None or reason_contains in reason)
 RESULTS.append(dict(label=label,ok=ok,state=state,reason=reason,expected=expected,issue_calls=calls));print(('PASS' if ok else 'FAIL')+' TEST '+label+': '+state,flush=True)

test('captured root issue688 at exact e481/afdec',None,'FAIL' if phase=='before' else 'PASS','ES header present' if phase=='before' else None)
if phase!='before':
 for text in [
  'Prose says no reviewed-at-es: and no fixed-at-es: apply here.',
  '- This criterion says no `fixed-at-es:` and no `reviewed-at-es:`.',
  '**Prose:** no fixed-at-es: field is required.',
  'not-fixed-at-es: this is a different field name.',
 ]:test('prose mention allowed: '+text,lambda v,text=text:v.update(body=text+'\n'+v['body']))
 for key in ['reviewed-at-es','fixed-at-es']:
  for line in [key+': '+TIP,'- **'+key+':** `'+TIP+'`','- `'+key+'`: `'+TIP+'`',' \t**'+key+'**:\t'+TIP,key+':',key+': not-a-hash']:
   test('actual ES header refused: '+repr(line),lambda v,line=line:v.update(body=line+'\n'+v['body']),'FAIL','ES header present')
  test('actual ES header after criteria refused: '+key,lambda v,key=key:v.update(body=v['body']+'\n'+key+': '+TIP+'\n'),'FAIL','ES header present')
 def replace_header(v,key,value):
  pattern=r'^[-* `]*'+re.escape(key)+r'\*{0,2}:\*{0,2}[^\n]*$'
  body,count=re.subn(pattern,key+': '+value,v['body'],flags=re.M);assert count==1;v['body']=body
 def remove_header(v,key):
  pattern=r'^[-* `]*'+re.escape(key)+r'\*{0,2}:\*{0,2}[^\n]*\n?'
  body,count=re.subn(pattern,'',v['body'],flags=re.M);assert count==1;v['body']=body
 test('wrong current distribution tip remains refused',lambda v:replace_header(v,'fixed-at','61a1a674c10d520f9d93748c5a73deaadb08b158'),'FAIL','fixed-at not submitted tip')
 test('wrong reviewed dispatch remains refused',lambda v:replace_header(v,'reviewed-at','0'*40),'FAIL','reviewed-at not dispatch')
 for key in ['reviewed-at','fixed-at']:test('missing '+key+' remains ABSENT',lambda v,key=key:remove_header(v,key),'ABSENT','unfilled '+key)
 test('wrong slice title remains refused',lambda v:v.update(title=v['title'].replace('E1054/T41','E1054/T42')),'FAIL','wrong title')
 for token in ['D-WORKFLOW-222','openai/gpt-6-astra','\\u002d']:
  test('missing current requirement remains refused: '+token,lambda v,token=token:v.update(body=v['body'].replace(token,'removed-requirement')),'FAIL','current method/reader/path criterion missing')
 test('ordinary bold Markdown distribution headers remain accepted',lambda v:v.update(body=re.sub(r'^(reviewed-at|fixed-at): ([0-9a-f]+)$',r'- **\1:** `\2`',v['body'],flags=re.M)))
for x in frozen:assert sha(P.Path(x['path']).read_bytes())==x['sha256'],x['path']
packet=dict(identity='Codex (GPT-6), /root, wN:p5',session='01a19d12-1c5f-7022-8053-102f6a94b7fe',scope='pure issue-body against supplied captured root data; not a live final gate',tip=TIP,coordinator=COORD,dispatch=DISPATCH,source_sha256=sha(source.encode()),captured_issue_sha256=sha(a),root_artifacts_unchanged=frozen,results=RESULTS)
with receipt.open('x') as f:json.dump(packet,f,indent=2);f.write('\n')
bad=sum(not x['ok'] for x in RESULTS);print('PURE ISSUE-BODY SUMMARY',len(RESULTS)-bad,'passed,',bad,'failed',receipt,sha(receipt.read_bytes()));raise SystemExit(bool(bad))
