#!/usr/bin/env python3
"""New T46 coordinator exact-tip integration. Never invokes lane producers."""
import argparse, datetime, hashlib, json, os, pathlib, re, subprocess, time, traceback
P=pathlib.Path
ROOT=P('/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346')
COORD='2ab42922be8d0b693e41a9fcfa9e8c666beae462'
TIP='17a064e6110306dd2b692cfd1b13d4f518d8def5'
D='a0d4c4fda7a0c16c04d57edf921ffeb741eff19b'
AUDIT='docs/audits/2026_11_03-epic-m6-records'
LOG='docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md'
INDEX='docs/work-logs/INDEX.md'
README='docs/audits/README.md'
AFTER='410e4432c01a38cda578a68fdaa730129c15a8e3e60c7305001bb40bd5a71b6c'
TOOLS=['tools/rules-check','tools/register-check','tools/work-log-index','tools/ceremony-check','tools/forbidden-terms-check','tools/lint-audit-artifacts','tools/box-check','.githooks']
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--resume',action='store_true');args=ap.parse_args()
OUT=P(args.out);assert OUT.is_relative_to('/workspace/tmp/m6-coordinator')
if not args.resume:OUT.mkdir(mode=0o700,parents=True,exist_ok=False)
CLONE=OUT/'integration';commands=json.loads((OUT/'commands.json').read_text()) if args.resume else []
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,v):
    (OUT/n).write_text(json.dumps(v,indent=2,ensure_ascii=True)+'\n')
def mask(b):
    return subprocess.run(['sed','-E','-f','/workspace/tmp/m6-coordinator/kit/mask.sed'],input=b,capture_output=True,check=True).stdout
def run(name,argv,cwd=ROOT,ok=(0,),timeout=1200,stdin=None,inputs=()):
    snapshots=[]
    for f in inputs:
        p=P(cwd)/f; data=p.read_bytes();snapshots.append({'path':f,'bytes':len(data),'sha256':sha(data)})
    begin=now();start=time.monotonic();timedout=False
    try:r=subprocess.run(argv,cwd=cwd,input=stdin,capture_output=True,timeout=timeout)
    except subprocess.TimeoutExpired as e:
        timedout=True;r=subprocess.CompletedProcess(argv,124,e.stdout or b'',e.stderr or b'')
    stem=f'{len(commands)+1:03d}-{name}';stdout=mask(r.stdout);stderr=mask(r.stderr)
    (OUT/(stem+'.stdout')).write_bytes(stdout);(OUT/(stem+'.stderr')).write_bytes(stderr)
    item={'name':name,'argv':argv,'cwd':str(cwd),'start':begin,'end':now(),'seconds':time.monotonic()-start,'rc':r.returncode,'timeout':timedout,'stdout':stem+'.stdout','stderr':stem+'.stderr','stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'stored_stdout_sha256':sha(stdout),'stored_stderr_sha256':sha(stderr),'stdin_sha256':sha(stdin) if stdin is not None else None,'inputs':snapshots}
    commands.append(item);save('commands.json',commands)
    print(name,'rc',r.returncode,flush=True)
    if r.returncode not in ok:raise RuntimeError(f'{name}: exit {r.returncode}; retained {stem}')
    return r.stdout
def git(name,*argv,cwd=ROOT,**kw):return run(name,['git',*argv],cwd=cwd,**kw)
def tree(raw):
    result={}
    for row in raw.split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);mode,typ,oid=meta.decode().split();result[path.decode()]={'mode':mode,'type':typ,'oid':oid}
    return result
def merge_entries(base,left,right):
    assert base.endswith(b'\n')
    def parse(tip):
        assert tip.startswith(base),'existing log bytes changed'
        suffix=tip[len(base):]
        if not suffix:return []
        starts=[x.start() for x in re.finditer(rb'^## ',suffix,re.M)]
        assert starts and suffix[:starts[0]].strip(b'\n')==b'' and starts[0]>0 and suffix.endswith(b'\n'),'not whole entries'
        boundaries=[0]
        for i in starts[1:]:
            j=i
            while j>0 and suffix[j-1:j]==b'\n':j-=1
            assert i-j>=2,'missing blank separator';boundaries.append(j+1)
        parts=[suffix[a:b] for a,b in zip(boundaries,boundaries[1:]+[len(suffix)])]
        for part in parts:
            title=part.lstrip(b'\n').split(b'\n',1)[0].decode()
            m=re.fullmatch(r'## (\d{2}:\d{2}(?::\d{2})?) UTC (?:—|–|--|-) .+',title)
            assert m,'unsupported timestamp heading'
            datetime.datetime.strptime(m[1],'%H:%M:%S' if len(m[1])==8 else '%H:%M')
            assert part.lstrip(b'\n').split(b'\n',1)[1].strip(),'empty entry'
        return parts
    base_heads={x for x in base.splitlines() if x.startswith(b'## ')}
    by_key={};seqs=[]
    for tip in [left,right]:
        seq=[]
        for part in parse(tip):
            key=part.lstrip(b'\n').split(b'\n',1)[0]
            assert key not in base_heads and key not in seq,'duplicate heading'
            assert key not in by_key or by_key[key]==part,'conflicting same-heading bytes'
            by_key[key]=part;seq.append(key)
        seqs.append(seq)
    edges={k:set() for k in by_key};degree={k:0 for k in by_key};ordered=[]
    for seq in seqs:
        for a,b in zip(seq,seq[1:]):
            if b not in edges[a]:edges[a].add(b);degree[b]+=1
    while degree:
        ready=sorted(k for k,v in degree.items() if v==0);assert ready,'incompatible order'
        key=ready[0];ordered.append(key);degree.pop(key)
        for k in edges[key]:degree[k]-=1
    for seq in seqs:assert [k for k in ordered if k in seq]==seq
    merged=base+b''.join(by_key[k] for k in ordered)
    assert parse(merged)==[by_key[k] for k in ordered]
    return merged,[[{'heading':k.decode(),'entry_sha256':sha(by_key[k])} for k in seq] for seq in seqs]
def helper_controls():
    b=b'# day\n';a=b+b'\n## 10:01 UTC -- left\n\nleft body\n'
    c=b+b'\n## 10:02:03 UTC -- right\n\nright body\n'
    positive=merge_entries(b,a,c)[0];rows=[]
    cases={'base-edited':(b,a.replace(b'# day',b'# other'),c),'missing-newline':(b,a,c[:-1]),'invalid-time':(b,a,c.replace(b'10:02:03',b'10:99:03')),'same-heading-conflict':(b,a,a.replace(b'left body',b'different body')),'duplicate-heading':(b,a+a[len(b):],c),'nonentry-tail':(b,a,c+b'unheaded tail\n## broken\n')}
    for name,params in cases.items():
        try:merge_entries(*params)
        except (AssertionError,ValueError) as e:rows.append({'case':name,'refused':True,'reason':str(e)})
        else:raise AssertionError('helper failed to refuse '+name)
    save('log-helper-controls.json',{'new_small_coordinator_controls':True,'cases':rows,'positive_sha256':sha(positive)})
start=now()
if args.resume:
    prior=json.loads((OUT/'result.json').read_text());assert prior['state']=='FAIL' and prior['commands']==14
    assert not (OUT/'initial-result.json').exists();save('initial-result.json',prior)
save('continuation-start.json' if args.resume else 'start.json',{'start':start,'coordinator':COORD,'lane':TIP,'D':D,'executor':{'harness':'Codex','model':'GPT-6-Astra','effort':'xhigh','identity_source':'own observed footer; not provider-attested','session':'01a19d11-f5c8-7bb0-80f3-49ad28732af2','pane':'wN:p2'},'affinity':sorted(os.sched_getaffinity(0)),'runner_sha256':sha(P(__file__).read_bytes()),'scope':'New disposable exact-tip record/integration checks only; no lane producers or accepted fixtures replayed.'})
try:
    assert set(os.sched_getaffinity(0))==set(range(8,24))
    if not args.resume:
        run('inode-capacity',['df','-i','/workspace/tmp/m6-coordinator'])
        run('disk-capacity',['df','-h','/workspace/tmp/m6-coordinator'])
        assert git('coordinator-head','rev-parse','HEAD').decode().strip()==COORD
        assert git('coordinator-clean','status','--porcelain=v1')==b''
        refs={r:git('history-ref','rev-parse','--verify',r+'^{commit}').decode().strip() for r in ['refs/heads/next','refs/remotes/upstream/next']}
        a=git('lane-tool-identities','ls-tree','-rz',TIP,'--',*TOOLS)
        b=git('coordinator-tool-identities','ls-tree','-rz',COORD,'--',*TOOLS);assert a==b
        helper_controls()
        run('clone',['git','clone','--quiet','--shared','--no-checkout','--no-hardlinks','--template=',str(ROOT),str(CLONE)])
        for r,v in refs.items():git('history-pin','update-ref',r,v,cwd=CLONE)
        git('checkout','checkout','--quiet','--detach',COORD,cwd=CLONE)
    assert git('clone-head','rev-parse','HEAD',cwd=CLONE).decode().strip()==COORD
    assert git('clone-premerge-clean','status','--porcelain=v1',cwd=CLONE)==b''
    name=git('configured-name','config','--get','user.name').decode().strip()
    email=git('configured-email','config','--get','user.email').decode().strip()
    assert name and email
    git('merge','-c','user.name='+name,'-c','user.email='+email,'merge','--no-commit','--no-ff','--no-edit',TIP,cwd=CLONE,ok=(0,1))
    raw=git('unmerged','ls-files','-u','-z',cwd=CLONE)
    conflicts={x.split(b'\t',1)[1].decode() for x in raw.split(b'\0') if x};assert conflicts<={LOG,INDEX},conflicts
    base=git('merge-base','merge-base','--all',COORD,TIP,cwd=CLONE).decode().strip();assert re.fullmatch('[0-9a-f]{40}',base)
    bodies=[git('log-'+label,'show',ref+':'+LOG,cwd=CLONE) for label,ref in [('base',base),('coordinator',COORD),('lane',TIP)]]
    merged,sequences=merge_entries(*bodies);(CLONE/LOG).write_bytes(merged)
    save('log-resolution.json',{'base':base,'coordinator':COORD,'lane':TIP,'input_sha256':[sha(x) for x in bodies],'input_bytes':[len(x) for x in bodies],'sequences':sequences,'merged_bytes':len(merged),'merged_sha256':sha(merged),'whole_entries_preserved':True})
    run('index-render',['tools/work-log-index'],CLONE,inputs=('tools/work-log-index',LOG))
    run('index-write',['tools/work-log-index','--write'],CLONE,inputs=('tools/work-log-index',LOG))
    assert (CLONE/LOG).read_bytes()==merged
    assert git('other-unstaged','diff','--name-only','-z','--','.',':(exclude,literal)'+LOG,':(exclude,literal)'+INDEX,cwd=CLONE)==b''
    git('stage-ledgers','add','--',LOG,INDEX,cwd=CLONE)
    assert git('final-unmerged','ls-files','-u',cwd=CLONE)==b''
    # Exact merged index: every coordinator byte stays; all lane branch additions
    # and the authorized README are copied by Git, only the two ledgers combine.
    coord=tree(git('coordinator-tree','ls-tree','-rz',COORD,cwd=CLONE))
    lane=tree(git('lane-tree','ls-tree','-rz',TIP,cwd=CLONE))
    base_tree=tree(git('base-tree','ls-tree','-rz',base,cwd=CLONE))
    idx=git('merged-index','ls-files','-sz',cwd=CLONE);index={}
    for row in idx.split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0';index[path.decode()]={'mode':mode,'type':'blob' if mode!='160000' else 'commit','oid':oid}
    delta={p for p in set(base_tree)|set(lane) if base_tree.get(p)!=lane.get(p)}
    expected=dict(coord)
    for p in delta:
        if p not in [LOG,INDEX]:assert p in lane;expected[p]=lane[p]
    for p in [LOG,INDEX]:expected[p]=index[p]
    assert expected==index,'unexpected integration index drift'
    frozen=tree(git('D-audit','ls-tree','-rz',D,'--',AUDIT,cwd=CLONE))
    mutable={AUDIT+'/'+x for x in ['00-running-log.md','02-forward-audit.md','04-analysis.md','05-punch-list.md','06-audit-summary.md','07-questions-for-the-maintainer.md']}
    frozen={p:v for p,v in frozen.items() if p not in mutable};assert len(frozen)==305
    assert all(index[p]==v for p,v in frozen.items())
    source=(CLONE/README).read_bytes();assert len(source)==813 and sha(source)==AFTER
    save('integrated-identities.json',{'index_paths':len(index),'lane_delta_paths':len(delta),'frozen305_unchanged':True,'README_bytes':len(source),'README_sha256':sha(source),'all_nonledger_index_entries_exact':True,'index_canonical_sha256':sha(json.dumps(index,sort_keys=True,separators=(',',':')).encode()),'no_actual_integration':True})
    git('whitespace','diff','--cached','--check',cwd=CLONE)
    for name,cmd in [('rules',['tools/rules-check','--quiet']),('register',['tools/register-check']),('index',['tools/work-log-index','--check']),('ceremony',['tools/ceremony-check','--gate']),('hooks',['.githooks/hooks-test']),('forbidden',['tools/forbidden-terms-check']),('lint',['tools/lint-audit-artifacts',AUDIT]),('lint-issue',['tools/lint-audit-artifacts',AUDIT,'--issue','1417']),('slice-check',['tools/box-check','--issue','693']),('audit-check',['tools/box-check','--issue','1417']),('bug-check',['tools/box-check','--issue','1416'])]:
        inputs=[cmd[0]]
        if name.startswith('lint'):inputs += [AUDIT+'/04-analysis.md',AUDIT+'/05-punch-list.md',AUDIT+'/second-opinions/review-plan.json',README]
        run(name,cmd,CLONE,inputs=inputs)
    assert git('final-unstaged','diff','--name-only','-z',cwd=CLONE)==b''
    assert git('final-untracked','ls-files','--others','--exclude-standard','-z',cwd=CLONE)==b''
    save('result.json',{'state':'PASS','start':start,'end':now(),'coordinator':COORD,'lane':TIP,'commands':len(commands),'all_final_gates_pass':True,'actual_integration':False,'accepted_producers_replayed':False})
    print('PASS new T46 exact-tip integration',flush=True)
except BaseException as e:
    save('result.json',{'state':'FAIL','start':start,'end':now(),'coordinator':COORD,'lane':TIP,'commands':len(commands),'error':repr(e),'traceback':traceback.format_exc()})
    print('FAIL',repr(e),flush=True);raise
