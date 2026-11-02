#!/usr/bin/env python3
"""Constructed fixture validation only. No historical tests/programs are run.
All commits belong to a tiny synthetic git repository under this owned directory.
Synthetic receipts are explicitly fixture data, never accepted audit evidence.
"""
import collections as C, copy, hashlib, json, os, pathlib as P, re, shutil, subprocess as S, sys, runpy
OWN=P.Path('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12')
os.environ['ACCEPT_EXECUTOR_JSON']=json.dumps({'harness': 'Codex', 'model': 'GPT-6', 'effort': 'not exposed by this harness', 'session': '01a19d12-1c5f-7022-8053-102f6a94b7fe', 'pane': 'wN:p5', 'identity_source': 'actual harness and recovered Herdr identity'})
FIX=OWN/'fixtures';R=FIX/'repo';A=FIX/'audit';COR=A/'stage-b/corrected';RESULTS=[]
SOURCE='02aab33bd9842610b0d466c9c186454dc14373ee';UP='651150fc88'
OLD='3cd9ca140a0da9af447a3ee2fb9cdbbbf222a95b'
POP={'GENERIC_X64':8,'H700':42,'SM8550':65,'UBOOT-DDR3':2,'UBOOT-DDR4':2,'FIRMWARE':1}
D=['projects/ROCKNIX/packages/linux/patches/'+v for v in ['7.0','7.2','mainline']]+['projects/ROCKNIX/devices/H700/patches/linux','projects/ROCKNIX/devices/SM8550/patches/linux','projects/ROCKNIX/devices/SM8550/linux','projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches','projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/patches','projects/ROCKNIX/packages/linux-firmware/kernel-firmware/patches']
GITENV=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_AUTHOR_NAME='Codex fixture',GIT_AUTHOR_EMAIL='codex-fixture@invalid',GIT_COMMITTER_NAME='Codex fixture',GIT_COMMITTER_EMAIL='codex-fixture@invalid',GIT_AUTHOR_DATE='2026-11-02T00:00:00Z',GIT_COMMITTER_DATE='2026-11-02T00:00:00Z')
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,data):
    p=P.Path(p);assert p.absolute().is_relative_to(OWN) and p.resolve()==p.absolute()
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data.encode() if isinstance(data,str) else data)
def js(p,obj):write(p,json.dumps(obj,indent=2)+'\n')
def git(*args):
    p=S.run(['git','-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false','-C',str(R),*args],capture_output=True,env=GITENV)
    if p.returncode:raise RuntimeError('synthetic git command failed: '+repr(args)+' '+p.stderr.decode()[:300])
    return p.stdout.decode().strip()
def commit(msg):git('add','-A');git('commit','-qm',msg);return git('rev-parse','HEAD')
def setup():
    if FIX.exists():raise RuntimeError('fixture directory already exists; use retained results or remove only owned fixture directory explicitly')
    R.mkdir(parents=True);git('init','-q')
    inv=[];raw={};index=0
    for d,n in zip(D,[4,6,4,32,55,1,2,2,1]):
        for i in range(n):
            p=d+('/linux.aarch64.conf' if d==D[5] else '/%04d-fixture.patch'%i)
            if d==D[3] and i==31:p=d+'/0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch'
            if d==D[2] and i==0:p=d+'/0002-input-add-input-polldev-driver.patch'
            if d==D[3] and i==0:p=d+'/0158-mmc-sunxi-mmc-mask-data0-fixture.patch'
            b=(('From: fixture <fixture@invalid>\n' if index<87 else '')+('Subject: [PATCH] fixture\n' if index<89 else '')+'fixture source\n').encode()
            raw[p]=b;inv.append(dict(path=p.replace('mask-data0','mask\\u002ddata0'),lines=len(b.splitlines()),reach='shipped' if index<103 else 'test',reachable_by=[]));index+=1
    padding=40474-sum(x['lines'] for x in inv);p0=inv[0]['path'];raw[p0]+=b'x\n'*padding;inv[0]['lines']+=padding
    last=inv[-1]['path'];raw[last]=raw[last].rstrip(b'\n')
    k=0
    for g,n in enumerate([4,32,56,1,4,6,4]):
        for x in inv[k:k+n]:x['reachable_by']=['group-'+str(g)]
        k+=n
    for p,b in raw.items():write(R/p,b)
    archives={}
    recipe='projects/ROCKNIX/packages/linux/package.mk'
    kernel=runpy.run_path(str(OWN/'fixture_kernel_recipe.py'));recipe_text=kernel['RECIPE']
    for name in ['linux/linux-7.1.2.tar.xz','linux/linux-7.2.tar.xz','u-boot-DDR3/u-boot.tar.gz','u-boot-DDR4/u-boot.tar.gz','kernel-firmware/fw.tar.gz']:
        h=sha(name.encode());archives[name]=dict(sha256=h,sidecar_equal=True,recipe=recipe,recipe_equal=True);recipe_text+='# '+h+'\n'
    write(R/recipe,recipe_text)
    for i in range(329):write(R/f'docs/audits/fixture-epic-m6-patches-shipped-kernel/stage-a/original-{i:03d}.txt','synthetic old receipt '+str(i)+'\n')
    base=commit('synthetic dispatch fixture')
    absent=[p for p in raw if '0950-' in p or 'polldev' in p]
    changed=list(raw)[:4]
    for p in absent:(R/p).unlink()
    for p in changed:write(R/p,raw[p]+b'upstream change\n')
    up=commit('synthetic upstream fixture')
    git('checkout','-q',base)
    write(R/'audit/marker','fixture\n');good=commit('synthetic lane record #688')
    write(R/p0,raw[p0]+b'x\n');bad=commit('synthetic protected path change #688')
    git('checkout','-q',good)
    js(FIX/'fixture-refs.json',{SOURCE:base,UP:up,OLD:base})
    js(COR/'inventory-rows.json',inv);js(COR/'archive-sha256.json',archives)
    groups={d:[p for p in raw if str(P.PurePosixPath(p).parent)==d] for d in D}
    orders={'GENERIC_X64':groups[D[2]]+groups[D[0]],'H700':groups[D[2]]+groups[D[1]]+groups[D[3]],'SM8550':groups[D[2]]+groups[D[1]]+groups[D[4]],'UBOOT-DDR3':groups[D[6]],'UBOOT-DDR4':groups[D[7]],'FIRMWARE':groups[D[8]]}
    rows=[];tars=[];num=0
    def receipt(name,kind,rc,log,candidate):
        path='logs/'+name+'.'+kind+'.out';write(COR/path,log)
        return dict(argv=['patch','-p1','-N','--batch','--directory',candidate]+(['--dry-run'] if kind=='dry' else []),start='2026-11-02T00:00:01+00:00',elapsed_seconds=.001,rc=rc,timed_out=False,output=path,output_sha256=sha(log.encode()))
    for plan,order in orders.items():
        prev=sha(('initial'+plan).encode());write(COR/('tar-'+plan+'.out'),'')
        tar=dict(plan=plan,initial_tree_sha256=prev,all_missing_accounted=True,not_in_archive=0,missing_members=[],created_paths=[],output='tar-'+plan+'.out',output_sha256=sha(b''))
        js(COR/('tar-'+plan+'.json'),tar);tars.append(tar);write(COR/('order-'+plan+'.txt'),'\n'.join(order).replace('mask-data0','mask\\u002ddata0')+'\n')
        for i,p in enumerate(order,1):
            name=f'{plan}-{i:03d}';status='applies' if num<43 else 'applies with offset' if num<91 else 'fuzz'
            if name=='H700-011':status='fuzz'
            if num==119:status='applies'
            log={'applies':'patching fixture\n','applies with offset':'patching fixture with offset\n','fuzz':'patching fixture with fuzz\n'}[status]
            dryrc=1 if name=='H700-011' else 0;candidate='/synthetic/'+name
            x=dict(plan=plan,index=i,path=p.replace('mask-data0','mask\\u002ddata0'),patch_sha256=sha(raw[p]),produced_at='2026-11-02T00:00:00+00:00',input_tree_sha256=prev,after_dry_tree_sha256=prev,output_tree_sha256=sha(name.encode()),candidate=candidate,attempted=True,promoted=True,apply_rc=0,dry_rc=dryrc,status=status,offset=log.count('offset'),fuzz=log.count('fuzz'),FAILED=0)
            x['dry']=receipt(name,'dry',dryrc,'diagnostic FAILED\n' if dryrc else 'diagnostic\n',candidate);x['apply']=receipt(name,'apply',0,log,candidate)
            rows.append(x);js(COR/('rows/'+name+'.json'),x);prev=x['output_tree_sha256'];num+=1
    app=dict(source_ref=SOURCE,complete=True,rows=rows,tar=tars,counts=dict(C.Counter(x['status'] for x in rows)),dry_apply_disagreements=['H700-011']);js(COR/'application-results.json',app)
    prefix=sha(b'fixture-prefix');candidate='/synthetic/fail'
    badrow=dict(plan='FIXTURE',index=1,status='fails',apply_rc=1,dry_rc=1,promoted=False,input_tree_sha256=prefix,output_tree_sha256=sha(b'partial'),attempted=True)
    badrow['dry']=receipt('FIXTURE-001','dry',1,'FAILED\n',candidate);badrow['apply']=receipt('FIXTURE-001','apply',1,'partial FAILED\n',candidate)
    succ=dict(status='open item',index=2,blocked_by=1,attempted=False,promoted=False,input_tree_sha256=prefix,apply_rc=None,dry_rc=None)
    js(COR/'failed-candidate-guard.json',dict(result='PASS',prefix_before=prefix,prefix_after=prefix,failure=badrow,successor=succ));js(COR/'rows/FIXTURE-001.json',badrow);js(COR/'rows/FIXTURE-002.json',succ)
    write(COR/'apply-corrected.py','# synthetic fixture producer bytes, NEVER executed\n');js(COR/'run-metadata.json',dict(runner_sha256=sha((COR/'apply-corrected.py').read_bytes()),source_ref=SOURCE,locale='C'))
    tab=[]
    for idx,x in enumerate(inv):
        p=x['path'].replace('\\u002d','-');non='/u-boot-' in p or '/kernel-firmware/' in p;conf=p.endswith('.conf')
        aa=[z for z in rows if z['path']==x['path']];applies='; '.join(f'{z["plan"]}[{z["index"]:03d}] {z["status"]} (apply_rc={z["apply_rc"]}, dry_rc={z["dry_rc"]}; rows/{z["plan"]}-{z["index"]:03d}.json)' for z in aa) or 'open item: configuration selection'
        pin='v2026.01' if '/u-boot-' in p else '20260309' if '/kernel-firmware/' in p else '7.2'
        disp='upstream-changed' if p in changed else '#585' if '0950-' in p else 'upstream-moved' if p in absent else 'keep'
        tab.append(dict(path=x['path'],lines=x['lines'],kind='conf' if conf else 'non-kernel' if non else 'patch',owner='T27' if '/u-boot-' in p else 'T11' if '/kernel-firmware/' in p else 'T41',origin='fixture' if idx<87 else 'unknown',subject='fixture' if idx<89 else 'hand-made',pin=pin,applies=applies,disposition=disp,upstream='changed upstream' if p in changed else 'fork-written' if '0950-' in p else 'moved upstream' if p in absent else 'carried',backport='unknown',note='no header claim'))
    js(COR/'table-json.txt',tab)
    stats=dict(rows=107,dispositions=dict(C.Counter(x['disposition'] for x in tab)),application_status=app['counts'],plan_applications=POP,blocked=0,upstream_status=dict(C.Counter(x['upstream'] for x in tab)),backport_status={'unknown':107});js(COR/'table-stats.txt',stats)
    prov='| path | '+' | '.join('c'+str(i) for i in range(18))+' |\n| '+' | '.join(['---']*19)+' |\n'+'\n'.join('| `'+x['path']+'` | '+' | '.join([str(x['lines']),x['kind'],x['origin'],x['pin'],x['applies']]+['fixture']*13)+' |' for x in tab)+'\n'
    coverage='| Path | Lines | Kind | Reach | Disposition |\n| --- | --- | --- | --- | --- |\n'+'\n'.join('| `'+x['path']+'` | '+str(x['lines'])+' | '+x['kind']+' | shipped | '+x['disposition']+' |' for x in tab)+'\n'
    write(COR/'table-provenance.txt',prov);write(COR/'table-coverage.txt',coverage)
    owed='0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch cbf75c0b06 #585 never sent\n=~ #585 never sent\n'
    text='D-WORKFLOW-222\n## Provenance\n'+prov+'\n## Coverage\n'+coverage+'\n## The #585 lines owed\n'+owed+'\n## The runs\n120 106 H700 dry_rc=1 apply_rc=0 43 48 29\nforbidden-terms-check: 0 hits on stdin\nforbidden-terms-check: 1 line(s) on stdin carry a listed word\n'+kernel['QUOTE']
    for name,x in archives.items():
        if name.startswith('linux/'):text+=name+' = its .sha256 '+x['sha256'][:16]+'\n'
    text+='## What the coordinator, the integration and the next slices inherit\nT27 T11 T43 #563 #559 coordinator #585 L-09 L-17 L-21\n'+' '.join('L-%02d'%i for i in range(1,32))+'\n'
    text+='## Rulings a to p\n'+'\n'.join('| '+c+' | fixture disposition |' for c in 'abcdefghijklmnop')+'\n## Proofs\n| P01 | proved: tree | fixture | source |\n'
    write(A/'02-forward-audit.md',text);write(A/'00-running-log.md','census: no build no compiler no guest\nPROOF: P01 | tree | fixture\nStage H: /workspace/tmp/m6-t41/src retired\n');js(COR/'proof-index.json',[['P01','tree','fixture','source']])
    write(A/'01-research-notes.md','## Scope\n107 40474 40473 4d300124a6bf116f TREE-SIDE GROUPS TOTAL reachable_by 4 32 56 1 4 6 4\n')
    analysis='## Renovation face\n'
    for q in range(1,8):
        analysis+=f'### Q{q} fixture\n\n'+('~~Nothing changes time to play.~~\n' if q==5 else 'fixture answer\n')
        if q==4:
            analysis+='ramoops #585 =~ never sent\n'
            for dim in ['application_status','upstream_status','backport_status','dispositions']:
                analysis+='\n'.join(f'| {dim} | {v} | {n} |' for v,n in stats[dim].items())+'\n'
    analysis+='packaging-and-patches.md:91 CLAUDE.md:148 interface-to-first-frame exit-to-next-first-frame\n';write(A/'04-analysis.md',analysis)
    neg=[]
    for name,msg in zip(['drop','reach','header'],['membership: expected 107 rows','reach: expected shipped 103/test 4','From header census: expected 87']):
        line='AssertionError: '+msg;neg.append(dict(name=name,rc=1,last_line=line));write(COR/('generator-fail-'+name+'.out'),line+'\n')
    js(COR/'generator-fail-first.json',neg)
    js(A/'second-opinions/review-plan.json',dict(depth='local',reviewers=[],tier_exception='D-WORKFLOW-184',primary=dict(model='openai/gpt-6-astra',lab='openai',harness='Codex'),identity_source='Observed live footer; historical Opus execution and Argon write-up',reason='plan section 6c provenance table'))
    write(A/'tools/t41-tables.py','# synthetic future-C file; never run\n')
    # 05 deliberately absent: expected final-run ABSENT, never invented for a pass.
    js(FIX/'state.json',dict(base=base,good=good,bad=bad))
    return json.loads((FIX/'state.json').read_text())

def runner(label,section,expected,state,tip=None,extra=None):
    env=dict(os.environ,DIST_REPO=str(R),DISPATCH_TIP=state['base'],AUDIT_ISSUE='0',BUGS='',ACCEPT_FIXTURE_ROOT=str(FIX),ACCEPT_DIR=str(OWN/'test-run'),OUT=str(OWN/'test-run.out'),ACCEPT_ONLY=section)
    if extra:env.update(extra)
    p=S.run(['bash',str(OWN/'t41-accept.sh'),tip or state['good'],state['base']],env=env,capture_output=True)
    text=p.stdout.decode();vs=re.findall(r'^VERDICT (PASS|FAIL|CANNOT|ABSENT|RAN) ([a-z-]+) -- (.*)$',text,re.M)
    c=C.Counter(x[0] for x in vs);want='SUMMARY: pass %d, fail %d, cannot %d, absent %d, ran %d'%tuple(c[x] for x in ['PASS','FAIL','CANNOT','ABSENT','RAN'])
    rc=1 if c['FAIL'] else 2 if c['CANNOT'] or c['ABSENT'] else 0
    ok=bool(vs) and all(x[0]==expected for x in vs) and want in text and f'ACCEPT-RC {rc}' in text and p.returncode==rc and not re.search(r'Traceback|unbound variable|syntax error',text)
    RESULTS.append(dict(label=label,expected=expected,verdicts=vs,rc=p.returncode,summary=want,ok=ok))
    print(('PASS' if ok else 'FAIL')+' TEST '+label+' => '+','.join(x[0]+':'+x[1] for x in vs))
    if not ok:print(text[:1600],p.stderr.decode()[:300])

def mutate_json(label,section,path,fn,state):
    path=P.Path(path);old=path.read_bytes();v=json.loads(old);fn(v);js(path,v)
    try:runner(label,section,'FAIL',state)
    finally:path.write_bytes(old)
    runner(label+' control',section,'PASS',state)
def mutate_text(label,section,path,old,new,state):
    b=path.read_bytes();need=old in b.decode();assert need,label;write(path,b.decode().replace(old,new,1))
    try:runner(label,section,'FAIL',state)
    finally:path.write_bytes(b)
    runner(label+' control',section,'PASS',state)

def positives(state):
    runner('lane-shaped protected patch byte','patch-untouched product-paths','FAIL',state,tip=state['bad'])
    runner('records-only lane commit','patch-untouched product-paths dist-tip','PASS',state)
    mutate_json('wrong current pin','pins-read',COR/'table-json.txt',lambda v:v[0].update(pin='9.9.9'),state)
    mutate_json('empty origin','headers',COR/'table-json.txt',lambda v:v[0].update(origin=''),state)
    mutate_json('superseded dry stats','applies-record',COR/'table-stats.txt',lambda v:v.update(application_status={'fails':6,'applies':114}),state)
    mutate_json('yes applicability','applies-record',COR/'table-json.txt',lambda v:v[0].update(applies='yes'),state)
    mutate_json('unsupported mainline claim','upstream-status',COR/'table-json.txt',lambda v:v[0].update(upstream='claims mainline',note=''),state)
    mutate_json('mismatched recipe SHA','tarball-hashes',COR/'archive-sha256.json',lambda v:next(iter(v.values())).update(sha256='0'*64),state)
    mutate_json('one reach group changed','device-groups',COR/'inventory-rows.json',lambda v:v[0].update(reachable_by=['wrong']),state)
    mutate_text('ramoops contribution removed','fork-written',A/'02-forward-audit.md','0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch cbf75c0b06 #585 never sent','missing',state)
    mutate_json('non-kernel mislabeled','non-kernel',COR/'table-json.txt',lambda v:next(x for x in v if x['kind']=='non-kernel').update(kind='patch'),state)
    (FIX/'lane-scratch/src').mkdir(parents=True);runner('source scratch present','scratch-retired','FAIL',state);(FIX/'lane-scratch/src').rmdir();runner('source scratch absent and retired','scratch-retired','PASS',state)
    mutate_json('wrong primary harness','review-plan-local',A/'second-opinions/review-plan.json',lambda v:v['primary'].update(harness='Claude'),state)
    mutate_json('wrong live reader','review-plan-local',A/'second-opinions/review-plan.json',lambda v:v['primary'].update(model='anthropic/opus'),state)
    mutate_json('header negative control passed','checker-record',COR/'generator-fail-first.json',lambda v:v[2].update(rc=0),state)
    coverage_row=(A/'02-forward-audit.md').read_text().split('## Coverage\n')[1].splitlines()[2]
    mutate_text('coverage omitted path','tables',A/'02-forward-audit.md',coverage_row,'',state)
    runner('escaped path normalization','tables tree-counts read-order generated','PASS',state)
    mutate_text('old dry result consumed','runs-record',A/'02-forward-audit.md','120 106 H700 dry_rc=1 apply_rc=0','120 106 H700 dry_rc=1 normal unknown',state)
    mutate_text('AC17 line not quoted','runs-record',A/'02-forward-audit.md','forbidden-terms-check: 1 line(s) on stdin carry a listed word','see receipt',state)
    # Change same duplicate row too, so each refusal tests D222 logic, not JSON-copy mismatch.
    appp=COR/'application-results.json';original=appp.read_bytes();app=json.loads(original);idx=next(i for i,x in enumerate(app['rows']) if x['plan']=='H700' and x['index']==11)
    rp=COR/'rows/H700-011.json';rb=rp.read_bytes()
    for label,fn in [('dry-run-authoritative promotion',lambda x:x.update(promoted=False,status='fails')),('broken prefix chain',lambda x:x.update(input_tree_sha256='0'*64)),('normal failure promoted',lambda x:x.update(apply_rc=1)),('misclassified normal fuzz',lambda x:x.update(status='applies'))]:
        a=copy.deepcopy(app);fn(a['rows'][idx]);js(appp,a);js(rp,a['rows'][idx]);runner(label,'applies-record','FAIL',state);write(appp,original);write(rp,rb)
    runner('dry=1 normal=0 positive retained','applies-record','PASS',state)
    original_path='docs/audits/fixture-epic-m6-patches-shipped-kernel/stage-a/original-000.txt'
    write(R/original_path,'changed old receipt\n');old_bad=commit('synthetic receipt tamper #688');runner('historical receipt changed','applies-record','FAIL',state,tip=old_bad);git('checkout','-q',state['good']);runner('all 329 originals restored','applies-record','PASS',state)
    logp=COR/'logs/H700-011.apply.out';lb=logp.read_bytes();write(logp,lb+b'changed\n');runner('raw log tamper','applies-record','FAIL',state);write(logp,lb);runner('raw log restored','applies-record','PASS',state)
    g=COR/'failed-candidate-guard.json';gb=g.read_bytes();v=json.loads(gb);v['prefix_after']='0'*64;js(g,v);runner('failed candidate contaminated prefix','applies-record','FAIL',state);write(g,gb);runner('failed prefix control restored','applies-record','PASS',state)
    v=json.loads(gb);v['successor']['apply']={'rc':0};js(g,v);runner('invented blocked successor command','applies-record','FAIL',state);write(g,gb)
    runner('missing future C/D artifacts','folder lint punch-list','ABSENT',state)
    js(FIX/'issues/688.comments.json',[])
    runner('missing future Stage-D questions','question-comments','ABSENT',state)
    plan=A/'second-opinions/review-plan.json';pb=plan.read_bytes();plan.unlink();runner('missing future reader plan','review-plan-local','ABSENT',state);write(plan,pb)
    runner('accepted D222 runs reconciled without replay','runs','PASS',state)
    runner('missing retained membership packet','membership','ABSENT',state)
    runner('missing retained formal generator packet','checker-run','ABSENT',state)
    # Final absent path + unresolved replay yields rc2, never a clean acceptance.
    runner('retained packet absence never green','membership checker-run','ABSENT',state)
    sentinel=OWN/'outside-sentinel';write(sentinel,'unchanged\n');link=OWN/'out-link';link.symlink_to(sentinel)
    runner('symlink OUT refused','headers','FAIL',state,extra={'OUT':str(link)});assert sentinel.read_text()=='unchanged\n';link.unlink()
    runner('outside owned output refused','headers','FAIL',state,extra={'OUT':'/tmp/t41-must-not-write.out'})
    runner('directory OUT refused','headers','FAIL',state,extra={'OUT':str(FIX)})
    runner('file ACCEPT_DIR refused','headers','FAIL',state,extra={'ACCEPT_DIR':str(sentinel)})
    runner('unknown section refused','not-a-section','FAIL',state)
    link=OWN/'hardlink-out';os.link(sentinel,link);runner('hardlink OUT refused','headers','FAIL',state,extra={'OUT':str(link)});link.unlink();assert sentinel.read_text()=='unchanged\n'

def refusals():
    out=OWN/'refusals';out.mkdir(exist_ok=True);source=P.Path('/workspace/tmp/m6-coordinator/kit/t36-accept.sh');derive=OWN/'derive-t41.py';dest=out/'refused.sh'
    def run(label,d,src,expected):
        p=S.run(['python3','-I',str(d),str(src),str(dest)],capture_output=True)
        ok=p.returncode!=0 and expected in p.stdout.decode() and not dest.exists();RESULTS.append(dict(label=label,ok=ok,rc=p.returncode,refusal=p.stdout.decode().strip()));print(('PASS' if ok else 'FAIL')+' TEST '+label)
    changed=out/'changed-source.sh';write(changed,source.read_bytes()+b'\n# fixture drift\n');run('changed shared source',derive,changed,'changed shared-source SHA256')
    mutated=out/'derive-shape.py';text=derive.read_text();old='unique(s,old);return s.replace(old,new)';assert old in text;write(mutated,text.replace(old,"unique(s,old+' shape-drift');return s.replace(old,new)",1));run('unmatched replacement shape',mutated,source,'unmatched replacement shape')
    # Valid inputs must regenerate byte-identically without installation.
    control=out/'control.sh';p=S.run(['python3','-I',str(derive),str(source),str(control)],capture_output=True)
    ok=p.returncode==0 and control.read_bytes()==(OWN/'t41-accept.sh').read_bytes();RESULTS.append(dict(label='deterministic derivation',ok=ok));print(('PASS' if ok else 'FAIL')+' TEST deterministic derivation')
    p=S.run(['python3','-I',str(derive),str(source),'/workspace/tmp/m6-coordinator/kit/t41-accept.sh'],capture_output=True)
    ok=p.returncode!=0 and b'destination escapes owned' in p.stdout;RESULTS.append(dict(label='shared-kit destination refused',ok=ok));print(('PASS' if ok else 'FAIL')+' TEST shared-kit destination refused')
    # No generated programs are run by this validation: parse Python in memory.
    compile((OWN/'t41_checks.py').read_bytes(),'candidate-predicates','exec')
    p=S.run(['bash','-n',str(OWN/'t41-accept.sh')],capture_output=True);RESULTS.append(dict(label='bash syntax',ok=p.returncode==0))

if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'all'
    if mode in ['all','positives']:
        state=setup() if not FIX.exists() else json.loads((FIX/'state.json').read_text());positives(state)
    if mode in ['all','refusals']:refusals()
    js(OWN/('checks-'+mode+'.json'),RESULTS)
    bad=sum(not x['ok'] for x in RESULTS);print('TEST SUMMARY:',len(RESULTS)-bad,'passed,',bad,'failed');sys.exit(bool(bad))
