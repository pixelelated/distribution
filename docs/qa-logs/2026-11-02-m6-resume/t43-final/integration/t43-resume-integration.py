#!/usr/bin/env python3
"""Continue only the failed T43 log-control fixture and unrun final gates."""
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import signal
import subprocess
import time

REPO = Path('/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346')
ROOT = Path('/workspace/tmp/m6-coordinator/t43-final-20261102T2355')
COORD = '749e5c7f2df2c8444b07f8521493d12b7f7a962b'
TIP = '8282cbcade3be32b437f7391be7e216d9a6b1074'
AUDIT = 'docs/audits/2026_11_02-epic-m6-patches-unshipped'
LOG = 'docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md'
INDEX = 'docs/work-logs/INDEX.md'
sha = lambda b: hashlib.sha256(b).hexdigest()
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

def need(ok, why):
    if not ok:
        raise ValueError(why)

def main():
    previous = json.loads((ROOT/'result.json').read_bytes())
    need(previous['state']=='FAIL' and previous['error']=='log control accepted same-heading-conflict' and previous['commands']==16, 'unexpected original result')
    for rec in json.loads((ROOT/'commands.json').read_bytes()):
        for stream in ('stdout','stderr'):
            need(sha((ROOT/rec[stream]).read_bytes())==rec[stream+'_masked_sha256'], 'original output changed')
    out = ROOT/'continuation'; out.mkdir(exist_ok=False)
    merged = ROOT/'integration'; events=[]
    pure = (REPO/'docs/qa-logs/2026-11-02-m6-resume/t41-final-runner/t41_execution.py').read_bytes()
    need(sha(pure)=='bab9838ac263f976ba73a73ab162614e132cf97a0dcfd8a781d1ed243e54bfd9','pure helper drift')
    nodes=[x for x in ast.parse(pure).body if isinstance(x,ast.FunctionDef) and x.name in ('mask_log','merge_append_bytes')]
    ns=dict(re=re,datetime=datetime,sha=sha,need=need,Invalid=ValueError)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'<unchanged historical helper>','exec'),ns)
    resolver=Path(__file__).with_name('t43-merge-log.py'); resolve=runpy.run_path(str(resolver))['merge_append_bytes']
    env=dict(os.environ,LC_ALL='C',GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='core.hooksPath',GIT_CONFIG_VALUE_0='/dev/null')
    env.pop('ES_SRC',None)
    (out/'start.json').write_text(json.dumps({'at':stamp(),'executor':previous['executor'],'lane':TIP,'coordinator':COORD,'prior_result_sha256':sha((ROOT/'result.json').read_bytes()),'runner_sha256':sha(Path(__file__).read_bytes()),'resolver_sha256':sha(resolver.read_bytes()),'affinity':sorted(os.sched_getaffinity(0))},indent=2)+'\n')
    def command(name,argv,expected=(0,),timeout=240):
        start=stamp();clock=time.monotonic();timed=False
        p=subprocess.Popen(argv,cwd=merged,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        try: stdout,stderr=p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed=True;os.killpg(p.pid,signal.SIGKILL);stdout,stderr=p.communicate()
        stem=f'{len(events)+1:03d}-{name}'
        rec={'name':name,'argv':argv,'cwd':str(merged),'start':start,'end':stamp(),'elapsed_seconds':time.monotonic()-clock,'rc':p.returncode,'timed_out':timed}
        for label,raw in [('stdout',stdout),('stderr',stderr)]:
            masked=ns['mask_log'](raw);file=stem+'.'+label;(out/file).write_bytes(masked)
            rec.update({label:file,label+'_sha256':sha(raw),label+'_masked_sha256':sha(masked)})
        events.append(rec);(out/'commands.json').write_text(json.dumps(events,indent=2)+'\n');print(name,p.returncode,flush=True)
        need(not timed and p.returncode in expected,name+' failed');return stdout,p.returncode
    try:
        b,_=command('head',['git','rev-parse','HEAD']);need(b.decode().strip()==COORD,'wrong root')
        b,_=command('merge-head',['git','rev-parse','MERGE_HEAD']);need(b.decode().strip()==TIP,'wrong lane')
        b,_=command('unmerged',['git','ls-files','-u','-z']);conflicts={x.split(b'\t')[1].decode() for x in b.split(b'\0') if x}
        need(conflicts and conflicts<={LOG,INDEX},'unexpected conflicts')
        b,_=command('base',['git','merge-base','--all',COORD,TIP]);bases=b.decode().splitlines();need(len(bases)==1,'ambiguous base')
        bodies=[command('log-source',['git','show',ref+':'+LOG])[0] for ref in [bases[0],COORD,TIP]]
        try:ns['merge_append_bytes'](*bodies)
        except ValueError as error:original_failure=str(error)
        else:raise ValueError('unexpected old-parser positive')
        need(original_failure=='append entry heading/body/boundary invalid','unexpected historical parser refusal')
        combined,sequences=resolve(*bodies)
        # Original fixture changed a heading, producing two valid distinct
        # entries. Correct the fixture by changing body bytes only, so the
        # two entries now have the same heading and conflicting bodies.
        i=bodies[1].index(b'\n',bodies[1].index(b'## ',len(bodies[0])))+1
        while bodies[1][i:i+1]==b'\n':i+=1
        changed_body=bodies[1][:i]+(b'X' if bodies[1][i:i+1]!=b'X' else b'Y')+bodies[1][i+1:]
        mutations=[
            ('old-bytes-edited',(bodies[0],bodies[1],b'x'+bodies[2][1:])),
            ('missing-terminal-newline',(bodies[0],bodies[1],bodies[2].rstrip(b'\n'))),
            ('legacy-body-edited',(bodies[0],bodies[1],bodies[2]+b'x\n')),
            ('invalid-seconds',(bodies[0],bodies[1].replace(b'22:12:19 UTC',b'22:12:99 UTC'),bodies[2])),
            ('unrecognized-legacy-heading',(bodies[0],bodies[1],bodies[2].replace(b'## 23:00 #690:',b'## 23:01 #690:'))),
            ('same-heading-conflict',(bodies[0],bodies[1],changed_body)),
        ]
        controls=[]
        for label,args in mutations:
            try:resolve(*args)
            except ValueError as error:controls.append({'case':label,'input_sha256':[sha(x) for x in args],'refused':True,'reason':str(error)})
            else:raise ValueError('control accepted '+label)
        (out/'log-proof.json').write_text(json.dumps({'base':bases[0],'coordinator':COORD,'lane':TIP,'input_sha256':[sha(x) for x in bodies],'original_parser_failure':original_failure,'original_fixture_failure_preserved':True,'fixture_correction':'Modify body under identical heading, not heading itself. Resolver unchanged.','entry_sequences':sequences,'merged_sha256':sha(combined),'controls':controls},indent=2)+'\n')
        (merged/LOG).write_bytes(combined)
        rendered,_=command('index-render',['tools/work-log-index']);command('index-write',['tools/work-log-index','--write'])
        need((merged/LOG).read_bytes()==combined and (merged/INDEX).read_bytes()==rendered,'log/index drift')
        other,_=command('other-unstaged',['git','diff','--name-only','-z','--','.',':(exclude,literal)'+LOG,':(exclude,literal)'+INDEX]);need(not other,'unexpected edit')
        command('stage-log-index',['git','add','--',LOG,INDEX])
        b,_=command('protected-paths',['git','diff','--cached','--name-only',COORD,'--','packages','projects','tools','scripts','.claude','.githooks','docs/reviews','docs/decision-register.md']);need(not b,'protected bytes changed')
        b,_=command('unmerged-final',['git','ls-files','-u']);need(not b,'unmerged paths')
        _,whitespace=command('whitespace',['git','diff','--cached','--check'],expected=(0,2))
        checks=[('rules',['tools/rules-check','--quiet']),('register',['tools/register-check']),('index',['tools/work-log-index','--check']),('ceremony',['tools/ceremony-check','--gate']),('hooks',['.githooks/hooks-test']),('forbidden',['tools/forbidden-terms-check']),('lint',['tools/lint-audit-artifacts',AUDIT]),('lint-issue',['tools/lint-audit-artifacts',AUDIT,'--issue','1412']),('slice',['tools/box-check','--issue','690']),('audit',['tools/box-check','--issue','1412']),('bug1408',['tools/box-check','--issue','1408']),('bug1410',['tools/box-check','--issue','1410'])]
        for name,argv in checks:
            b,_=command(name,argv,timeout=1200 if name=='forbidden' else 240)
            if name.startswith('lint'):need(b.decode().rstrip().endswith('PASS'),'resolution PASS absent')
        result={'state':'PASS' if whitespace==0 else 'REVIEW_WHITESPACE','at':stamp(),'lane':TIP,'coordinator':COORD,'executor':previous['executor'],'commands':len(events),'whitespace_rc':whitespace,'no_actual_integration':True,'accepted_producers_replayed':False,'original_failure_preserved':True}
    except Exception as error:
        result={'state':'FAIL','at':stamp(),'error':str(error),'commands':len(events)}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
    return 0 if result['state']=='PASS' else 1

if __name__=='__main__':
    raise SystemExit(main())
