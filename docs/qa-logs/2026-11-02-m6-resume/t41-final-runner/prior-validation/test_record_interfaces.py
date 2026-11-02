#!/usr/bin/env python3
"""Immutable-record interface regressions exposed by actual-tip readback.
Synthetic bytes only. Codex GPT-6 /root wN:p5, session01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import copy,json,re,pathlib as P,runpy,types
OWN=P.Path(__file__).parent;lib=runpy.run_path(str(OWN/'test_reconcile.py'),run_name='fixture_library');ns=lib['ns'];RESULTS=[]

def run(label,fn,expected='PASS'):
 try:fn();state='PASS';reason=''
 except Exception as e:state=type(e).__name__;reason=str(e)
 ok=state==expected;RESULTS.append(dict(label=label,ok=ok,state=state,reason=reason));print(('PASS' if ok else 'FAIL')+' TEST '+label+': '+state)
def member(extra):
 r=lib['setup']();p=ns['BRIEF'];b=r.blob(p,ns['AUTH']);r.put(p,b+extra,[ns['AUTH']]);return ns['reconcile_membership'](r)
run('marker strings inside extraction command are not delimiters',lambda:member(b'quoted = "<!-- t41 block.sh begin -->"\nquoted = "<!-- t41 block.sh end -->"\n'))
run('duplicate standalone marker refuses',lambda:member(b'<!-- t41 block.sh begin -->\n'),'Invalid')
def lint_bad():
 r=lib['setup']();p=ns['T4_FOLDER']+'/second-opinions/review-plan.json';r.refs[ns['T4']][p]=b'{"depth":"epic","reviewers":[]}';return ns['reconcile_lint'](r)
run('wrong immutable historical Local plan refuses',lint_bad,'Invalid')
PUNCH='''# Synthetic punch
## PL-001 — synthetic finding
question: Q3
punch_index:
## Phase 7 resolution gate

| Item | Outcome | Evidence / next owner |
| --- | --- | --- |
| PL-001 | Deferred | Open High bug #1408, integration #563/#559. |
'''
def records(path,text,section):
 r=lib['setup']();r.put(path,text);r.text=lambda p:r.audit(p).decode();r.read=lambda p:r.data[p];return ns['check'](r,section)
for label,text,expected in [
 ('Deferred audit outcome with Open bug evidence is disposed',PUNCH,'PASS'),
 ('Open outcome remains unresolved',PUNCH.replace('| Deferred |','| Open |'),'Invalid'),
 ('Deferred outcome without follow-up refuses',PUNCH.replace('#1408','missing').replace('#563/#559','missing'),'Invalid'),
 ('unlisted punch item refuses',PUNCH.replace('question: Q3','## PL-002 — unresolved\nquestion: Q3'),'Invalid'),
 ('duplicate gate row refuses',PUNCH+ '| PL-001 | Deferred | #1408 |\n','Invalid')]:run(label,lambda t=text:records('audit/05-punch-list.md',t,'punch-list'),expected)
run('capitalized Nothing keeps same retro meaning',lambda:records('retro.md','Nothing T42 T43 T27 T11 integration','retro'))
run('missing retro obligation remains refusal',lambda:records('retro.md','T42 T43 T27 T11 integration','retro'),'Invalid')
# Prospective root ruling: whole unchanged recipe, ten exact assignments, five
# case labels, exact source ref; only selected row pins use the four-value list.
kernel=runpy.run_path(str(OWN/'fixture_kernel_recipe.py'))
def pins(change=None):
 r=lib['setup']();rows=[dict(pin='7.2') for _ in range(107)];r.rows=lambda:rows
 r.put(kernel['PATH'],kernel['RECIPE'],[ns['SOURCE']]);r.put('audit/02-forward-audit.md',kernel['QUOTE']);r.text=lambda p:r.audit(p).decode()
 if change:change(r,rows)
 return ns['check'](r,'pins-read')
run('ten assignments plus five case contexts and exact source positive',pins)
run('nl tab delimiter preserves literal source bytes',lambda:pins(lambda r,rows:r.put('audit/02-forward-audit.md',re.sub(r'^(\d+):',r'\1\t',kernel['QUOTE'],flags=re.M))))
for n in [16,18,22,23,27,29,30,36,37,40,42,43,46,48,49]:
 run('missing numbered quotation '+str(n),lambda n=n:pins(lambda r,rows:r.put('audit/02-forward-audit.md','\n'.join(x for x in kernel['QUOTE'].splitlines() if not x.startswith(str(n)+':'))+'\n')),'Invalid')
run('changed assignment quotation refuses',lambda:pins(lambda r,rows:r.put('audit/02-forward-audit.md',kernel['QUOTE'].replace('30:    PKG_VERSION="7.2"','30:    PKG_VERSION="9.9"'))),'Invalid')
run('unselected branch must still be quoted exactly',lambda:pins(lambda r,rows:r.put('audit/02-forward-audit.md',kernel['QUOTE'].replace('6.18.49','7.2'))),'Invalid')
run('wrong source ref refuses',lambda:pins(lambda r,rows:r.put('audit/02-forward-audit.md',kernel['QUOTE'].replace(ns['SOURCE'],'0'*40))),'Invalid')
run('extra source assignment refuses despite matching new quote',lambda:pins(lambda r,rows:(r.put(kernel['PATH'],kernel['RECIPE']+'PKG_VERSION="9.9"\n'),r.put('audit/02-forward-audit.md',kernel['QUOTE']+'55:PKG_VERSION="9.9"\n'))),'Invalid')
run('changed source byte outside quotation refuses',lambda:pins(lambda r,rows:r.put(kernel['PATH'],kernel['RECIPE']+'# changed\n')),'Invalid')
run('unselected branch pin in provenance refuses',lambda:pins(lambda r,rows:rows[0].update(pin='6.18.49')),'Invalid')
(OWN/'checks-record-interfaces.json').write_text(json.dumps(RESULTS,indent=2)+'\n');bad=sum(not x['ok'] for x in RESULTS);print('RECORD INTERFACES',len(RESULTS)-bad,'passed,',bad,'failed');raise SystemExit(bool(bad))
