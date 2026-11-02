"""T41 candidate predicates; embedded by derive-t41.py, never a producer runner.
Codex (GPT-6), /root, wN:p5, session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
D226 reconciles accepted producers. Final gates execute only through FinalGates.
"""
import collections as C, hashlib, json, os, pathlib as P, re, subprocess, sys
SECTIONS='pointer folder dist-tip product-paths membership tree-counts issue-body bug-bodies lint review-plan-local lint-proof punch-list ladder audit-boxes bug-boxes scope-record read-order tables generated analysis-face forbidden secret checker-run checker-record fixes-record inherited-record proof-lines lane-boxes proved rulings analysis last-comments record-lines generators runs-record running-log no-compile handback retro checkers merge runs scratch question-comments patch-untouched pins-read headers applies-record upstream-status tarball-hashes device-groups fork-written non-kernel scratch-retired'.split()
POP={'GENERIC_X64':8,'H700':42,'SM8550':65,'UBOOT-DDR3':2,'UBOOT-DDR4':2,'FIRMWARE':1}
DIRS=['projects/ROCKNIX/packages/linux/patches/'+v for v in ['7.0','7.2','mainline']]+['projects/ROCKNIX/devices/H700/patches/linux','projects/ROCKNIX/devices/SM8550/patches/linux','projects/ROCKNIX/devices/SM8550/linux','projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/patches','projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/patches','projects/ROCKNIX/packages/linux-firmware/kernel-firmware/patches']
POINTER='.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md'
BRIEF='docs/reviews/briefs/patches-shipped-kernel.md'
AUTH='329011b9eae20922b4d0727e13bf1626b2e1c04f'
SOURCE='02aab33bd9842610b0d466c9c186454dc14373ee'
UPSTREAM='651150fc88'
OLD_RECEIPTS='3cd9ca140a0da9af447a3ee2fb9cdbbbf222a95b'
class Absent(Exception): pass
class Cannot(Exception): pass
class Invalid(Exception): pass
def need(c,why):
    if not c: raise Invalid(why)
def sha(b): return hashlib.sha256(b).hexdigest()
def dec(s): return s.replace('\\u002d','-')
def fmt(s): return s.replace('mask-data0','mask\\u002ddata0')
def lines(s): return s.splitlines()
def relpath(s):
    p=P.PurePosixPath(s)
    need(bool(s) and not p.is_absolute() and '..' not in p.parts and '\\' not in s,'unsafe receipt path')
    return s
def table(s):
    return [[c.strip().strip('`') for c in re.split(r'(?<!\\)\|',l)[1:-1]] for l in lines(s) if l.startswith('| `projects/')]
def section_text(s,name):
    m=re.search(r'^## '+re.escape(name)+r'\s*\n(.*?)(?=^## |\Z)',s,re.M|re.S)
    if not m: raise Absent('missing section '+name)
    return m[1]
def fixed_header(s,key):
    head=s.split('## Acceptance criteria')[0]
    m=re.search(r'^[-* `]*'+re.escape(key)+r'\*{0,2}:\*{0,2}[ `]*([0-9a-f]{7,40})\b',head,re.M)
    if not m: raise Absent('unfilled '+key)
    return m[1]
class Reader:
    def __init__(self):
        self.tip,self.coord=sys.argv[1:3];self.repo=os.environ['DIST_REPO'];self.dispatch=os.environ['DISPATCH_TIP'];self.cache={}
        for r in [self.tip,self.coord,self.dispatch]: need(re.fullmatch('[0-9a-f]{7,40}',r),'immutable commit required')
        self.fixture=os.environ.get('ACCEPT_FIXTURE_ROOT','')
        if self.fixture:
            self.root=P.Path(self.fixture).resolve();self.af='audit'
        else:
            allpaths=self.tree(self.tip,'docs/audits/')
            roots={p.split('/')[2] for p in allpaths if len(p.split('/'))>3 and p.split('/')[2].endswith('-epic-m6-patches-shipped-kernel')}
            if len(roots)!=1: raise Absent('expected one T41 audit folder')
            self.af='docs/audits/'+next(iter(roots))
    def git(self,*args,missing=False):
        env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_NOSYSTEM='1')
        p=subprocess.run(['git','--no-optional-locks','-C',self.repo,*args],capture_output=True,env=env)
        if p.returncode:
            if missing:return None
            raise Cannot('git object read failed')
        return p.stdout
    def tree(self,ref,path):
        if self.fixture:ref=json.loads(self.read('fixture-refs.json')).get(ref,ref)
        b=self.git('ls-tree','-rz',ref,'--',path);return {row.split(b'\t',1)[1].decode():row.split(b'\t',1)[0].decode() for row in b.split(b'\0') if row}
    def blob(self,path,ref=None):
        relpath(path)
        selected=ref or self.tip
        if self.fixture:
            aliases=json.loads(self.read('fixture-refs.json'));selected=aliases.get(selected,selected)
        key=(selected,path)
        if key not in self.cache:
            b=self.git('show',key[0]+':'+path,missing=True)
            if b is None: raise Absent('missing immutable path '+fmt(path))
            self.cache[key]=b
        return self.cache[key]
    def read(self,path):
        relpath(path)
        if self.fixture:
            p=self.root/path
            need(p.resolve().is_relative_to(self.root) and not p.is_symlink(),'fixture read escapes root')
            if not p.is_file(): raise Absent('missing '+path)
            return p.read_bytes()
        return self.blob(path)
    def audit(self,path):return self.read(self.af+'/'+relpath(path))
    def text(self,path):return self.audit(path).decode()
    def obj(self,path):return json.loads(self.audit(path))
    def corrected(self,path):return self.audit('stage-b/corrected/'+relpath(path))
    def co(self,path):return json.loads(self.corrected(path))
    def inventory(self):
        rows=self.co('inventory-rows.json');ps=[dec(x['path']) for x in rows]
        need(len(ps)==len(set(ps))==107,'membership must be 107 unique paths')
        need(C.Counter(x['reach'] for x in rows)=={'shipped':103,'test':4},'reach must be 103/4')
        return rows
    def issues(self,n,comments=False):
        name=str(n)+('.comments.json' if comments else '.json')
        if self.fixture:return json.loads(self.read('issues/'+name))
        return final_gates(self).issues(n,comments)
    def bugs(self):
        nums=os.environ.get('BUGS','').split()
        if not nums: raise Absent('no Stage-D bug numbers')
        need(all(n.isdigit() for n in nums),'BUGS must be issue numbers')
        return [self.issues(n) for n in nums]
    def audit_issue(self):
        n=os.environ.get('AUDIT_ISSUE','')
        if not n or n=='0':raise Absent('no Stage-D audit issue')
        need(n.isdigit(),'AUDIT_ISSUE must be numeric');return self.issues(n)
    def rows(self):return self.co('table-json.txt')
    def final_artifacts(self):
        self.audit('05-punch-list.md');self.audit('second-opinions/review-plan.json')
        self.audit('tools/t41-tables.py')

def validate_applications(r):
    prefix='docs/audits/fixture-epic-m6-patches-shipped-kernel' if r.fixture else r.af
    old={**r.tree(OLD_RECEIPTS,prefix+'/stage-a/'),**r.tree(OLD_RECEIPTS,prefix+'/stage-b/')}
    need(len(old)==329,'historical receipt census differs')
    for p in old:need(r.blob(p,OLD_RECEIPTS)==r.blob(p),'historical receipt changed')
    app=r.co('application-results.json');need(app.get('complete') is True,'incomplete corrected application packet')
    need(app['source_ref']==SOURCE,'wrong application source ref')
    rr=app['rows'];need(C.Counter(x['plan'] for x in rr)==POP,'application populations differ')
    need(len({dec(x['path']) for x in rr})==106,'application unique paths differ')
    need({dec(x['path']) for x in rr}=={dec(x['path']) for x in r.inventory() if x['path'].endswith('.patch')},'application membership differs')
    disagreements=[];counts=C.Counter()
    for plan,n in POP.items():
        group=[x for x in rr if x['plan']==plan]
        need([x['index'] for x in group]==list(range(1,n+1)),'sequence indices differ')
        tar=r.co('tar-'+plan+'.json');prev=tar['initial_tree_sha256'];failed=None
        need(tar in app['tar'],'tar receipt differs')
        need(sha(r.corrected(tar['output']))==tar['output_sha256'],'tar log hash differs')
        need(tar['all_missing_accounted'] and tar['not_in_archive']==len(tar['missing_members']),'missing targets unaccounted')
        need(all('/'.join(m.split('/')[1:]) in tar['created_paths'] for m in tar['missing_members']),'missing target not patch-created')
        for x in group:
            name=f'{plan}-{x["index"]:03d}'
            need(r.co('rows/'+name+'.json')==x,'individual row differs '+name)
            need(sha(r.blob(dec(x['path']),SOURCE))==x['patch_sha256'],'patch SHA differs '+name)
            need(x['input_tree_sha256']==prev,'prefix digest chain broken '+name)
            if failed is not None:
                need(x['status']=='open item' and x['blocked_by']==failed and x['attempted'] is False and x['promoted'] is False,'invalid blocked row')
                need(x['apply_rc'] is None and x['dry_rc'] is None and 'apply' not in x and 'dry' not in x and x['output_tree_sha256'] is None,'invented blocked result')
            else:
                need(x['attempted'] is True and x['after_dry_tree_sha256']==prev,'diagnostic changed candidate')
                cmd=['patch','-p1','-N','--batch','--directory',x['candidate']]
                for key in ['dry','apply']:
                    a=x[key];need(a['argv']==cmd+(['--dry-run'] if key=='dry' else []),'command differs')
                    need(a['rc']==x[key+'_rc'] and sha(r.corrected(a['output']))==a['output_sha256'],'rc/log hash differs')
                    need(isinstance(a['elapsed_seconds'],(float,int)) and a['elapsed_seconds']>=0 and a['start'] and x['produced_at'],'missing command timing')
                text=r.corrected(x['apply']['output']).decode()
                need(all(x[k]==text.count(k) for k in ['offset','fuzz','FAILED']),'counts are not normal-output counts')
                good=x['apply_rc']==0 and not x['apply']['timed_out']
                status='fails' if not good else 'fuzz' if x['fuzz'] else 'applies with offset' if x['offset'] else 'applies'
                need(x['status']==status and x['promoted']==good,'D222 promotion/classification mismatch')
                need(re.fullmatch('[a-f0-9]{64}',x['output_tree_sha256']),'invalid output digest')
                if good:prev=x['output_tree_sha256']
                else:failed=x['index']
                if x['dry_rc']!=x['apply_rc']:disagreements.append(name)
            counts[x['status']]+=1
    need(app['counts']==dict(counts) and app['dry_apply_disagreements']==disagreements,'summary consumes different verdicts')
    stats=r.co('table-stats.txt');need(stats['application_status']==dict(counts) and stats['plan_applications']==POP and stats['blocked']==0,'current stats consume superseded verdicts')
    # Current accepted packet: a later genuine failure must be a new lead, not silently accepted.
    need(counts=={'applies':43,'applies with offset':48,'fuzz':29} and disagreements==['H700-011'],'accepted Stage-B result changed')
    guard=r.co('failed-candidate-guard.json');bad=guard['failure'];succ=guard['successor']
    need(guard['result']=='PASS' and bad['apply_rc']!=0 and bad['promoted'] is False,'failed fixture promoted')
    need(guard['prefix_before']==guard['prefix_after']==bad['input_tree_sha256']==succ['input_tree_sha256'],'failed fixture contaminated prefix')
    need(bad['output_tree_sha256']!=guard['prefix_before'],'fixture did not partially change candidate')
    need(succ['status']=='open item' and succ['blocked_by']==bad['index'] and succ['attempted'] is False and succ['promoted'] is False and succ['apply_rc'] is None and succ['dry_rc'] is None and 'apply' not in succ and 'dry' not in succ,'fixture successor not blocked')
    for k in ['dry','apply']:need(sha(r.corrected(bad[k]['output']))==bad[k]['output_sha256'],'fixture log SHA differs')
    need(r.co('rows/FIXTURE-001.json')==bad and r.co('rows/FIXTURE-002.json')==succ,'fixture row mismatch')
    meta=r.co('run-metadata.json');need(sha(r.corrected('apply-corrected.py'))==meta['runner_sha256'],'runner hash differs')
    need(meta['source_ref']==SOURCE and meta['locale']=='C','runner inputs differ')
    return rr

def check(r,s):
    if s in ['dist-tip','product-paths','patch-untouched','fixes-record']:
        need(r.git('merge-base','--is-ancestor',r.dispatch,r.tip,missing=True) is not None,'dispatch not ancestor')
        commits=r.git('log','--no-merges','--format=%H',r.dispatch+'..'+r.tip,'^'+r.coord).decode().splitlines()
        if s=='dist-tip':
            if not commits:raise Absent('no lane commit')
            for c in commits:need('#688' in r.git('show','-s','--format=%B',c).decode(),'lane commit lacks #688')
        else:
            for c in commits:
                paths=r.git('diff-tree','--no-commit-id','--name-only','-r',c).decode().splitlines()
                for p in paths:
                    need(not re.search(r'\.(patch|conf)$',p) and not p.startswith(('packages/','projects/','tools/','scripts/')),'lane changed protected path')
                    if s=='product-paths':need(bool(re.match(r'^(docs/audits/[^/]*-epic-m6-patches-shipped-kernel/|docs/retros/[^/]*-m6-patches-shipped-kernel\.md$|\.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688\.md$|docs/work-logs/|docs/(decision-register|blindspot-register|friction-log)\.md$)',p)),'outside lane records scope')
        return 'lane-owned commits checked; no protected product edit'
    if s=='pointer':
        t=r.read(POINTER).decode()
        for k in ['Branch (distribution):','Worktree (distribution):','Worktree (EmulationStation):','Executor:','Epic:','Depth:','The lens:','The rule:','The host:','Register:','The brief:']:need(k in t,'pointer key absent '+k)
        for v in ['feature/m6-patches-shipped-kernel-688','#1054','Local','107','D-WORKFLOW-221',BRIEF]:need(v in t,'pointer value absent')
        need(not re.search(r'__[A-Z0-9_]+__',t),'unfilled pointer placeholder');return 'eleven keys/current T41 values'
    if s=='folder':
        for p in ['00-running-log.md','01-research-notes.md','02-forward-audit.md','03-retrospective.md','04-analysis.md','05-punch-list.md','second-opinions/review-plan.json','stage-a/README.md','stage-b/README.md','tools/t41-tables.py']:r.audit(p)
        need(not any('/guest-cycle/' in p for p in (r.tree(r.tip,r.af) if not r.fixture else [str(p.relative_to(r.root)) for p in r.root.rglob('*')])),'forbidden guest-cycle');return 'required final folder entries present'
    if s in ['membership','runs','checker-run','lint-proof']:return reconcile_check(r,s)
    if s=='tree-counts':
        inv=r.inventory();bs=[r.blob(dec(x['path'])) for x in inv]
        need(all(b==r.blob(dec(x['path']),SOURCE) for x,b in zip(inv,bs)),'one of 107 frozen sources changed')
        need(sum(len(b.splitlines()) for b in bs)==40474 and sum(b.count(b'\n') for b in bs)==40473,'line totals differ')
        need(C.Counter(P.PurePosixPath(dec(x['path'])).suffix for x in inv)=={'.patch':106,'.conf':1},'kinds differ')
        need([sum(str(P.PurePosixPath(dec(x['path'])).parent)==d for x in inv) for d in DIRS]==[4,6,4,32,55,1,2,2,1],'directory groups differ')
        need(sorted(C.Counter(tuple(x['reachable_by']) for x in inv).values())==sorted([4,32,56,1,4,6,4]),'reach groups differ');return '107 / 40474 / 40473; kinds, reach and groups match'
    if s=='issue-body':
        i=r.issues(688);t=i['body'];need('E1054/T41' in i['title'],'wrong title')
        need('reviewed-at-es:' not in t and 'fixed-at-es:' not in t,'ES header present')
        rev,fixed=fixed_header(t,'reviewed-at'),fixed_header(t,'fixed-at')
        need(r.dispatch.startswith(rev) or rev.startswith(r.dispatch),'reviewed-at not dispatch')
        need(r.tip.startswith(fixed) or fixed.startswith(r.tip),'fixed-at not submitted tip')
        need('D-WORKFLOW-222' in t and 'openai/gpt-6-astra' in t and '\\u002d' in t,'current method/reader/path criterion missing');return 'current issue headers/method/identity'
    if s=='review-plan-local':
        v=r.obj('second-opinions/review-plan.json');need(v['depth'].lower()=='local' and v['reviewers']==[] and v['tier_exception']=='D-WORKFLOW-184','not Local exception')
        p=v['primary'];need(isinstance(p,dict) and p.get('model')=='openai/gpt-6-astra' and p.get('lab')=='openai','wrong actual reader')
        need('codex' in json.dumps(p).lower(),'primary is not Codex')
        t=json.dumps(v).lower();need(all(x in t for x in ['codex','opus','argon','identity_source','footer']),'actual/historical identity missing')
        need('6c' in t or '6 c' in t,'Local reason missing')
        files=[str(p.relative_to(r.root/r.af/'second-opinions')) for p in (r.root/r.af/'second-opinions').rglob('*') if p.is_file()] if r.fixture else [p.split('/second-opinions/')[1] for p in r.tree(r.tip,r.af+'/second-opinions/')]
        need(files==['review-plan.json'],'unexpected reviewer artifacts');return 'actual Codex/Astra primary, historical identities, zero reviewers'
    if s=='bug-bodies':
        for b in r.bugs():
            for token in ['Already written:','Can this be done on the VM?','9416eec2c2','0010','7.0','7.2']:need(token in b['body'],'bug trace/acceptance line missing')
        return 'filed bug trace and ownership fields present'
    if s in ['lint','forbidden','secret','checkers','merge','generators','audit-boxes','bug-boxes','lane-boxes']:return executable_check(r,s)
    if s=='punch-list':
        t=r.text('05-punch-list.md');need('punch_index' in t and 'question:' in t,'punch index missing')
        need(not re.search(r'^\|.*\bOpen\b',t,re.M),'unresolved punch gate')
        need('fixed-at-es:' not in t,'ES field in table slice');return 'punch gate/index present; final lint remains separate'
    if s=='ladder':
        t=r.text('05-punch-list.md');need(re.search(r'ladder|Phase 7',t,re.I) and re.search(r'tool|no tool can',t,re.I),'ladder/tool absent');return 'ladder and next-tool field present'
    if s=='scope-record':
        t=section_text(r.text('01-research-notes.md'),'Scope')
        for v in ['107','40474','40473','4d300124a6bf116f','TREE-SIDE','GROUPS TOTAL']:need(v in t,'scope missing '+v)
        return 'accepted membership/line records named; replay not inferred'
    if s=='read-order':
        rr=r.co('application-results.json')['rows']
        for p,n in POP.items():
            order=list(map(dec,r.corrected('order-'+p+'.txt').decode().splitlines()))
            need(order==[dec(x['path']) for x in rr if x['plan']==p] and len(order)==n,'order differs')
        return 'all six retained sequences match row order'
    if s=='tables':
        t=r.text('02-forward-audit.md');inv={dec(x['path']) for x in r.inventory()}
        for title,width in [('Provenance',19),('Coverage',5)]:
            rows=table(section_text(t,title));need(len(rows)==107 and {dec(x[0]) for x in rows}==inv,'table membership differs')
            need(all(len(x)==width and all(x) for x in rows),'empty/wrong table cell')
        return '107 provenance and coverage rows with escaped-path normalization'
    if s=='generated':
        t=r.text('02-forward-audit.md')
        for k in ['provenance','coverage']:need(r.corrected('table-'+k+'.txt').decode().strip() in t,'generated table differs')
        stats=r.co('table-stats.txt');need(stats['rows']==107 and sum(stats['dispositions'].values())==107,'generated count differs');return 'generated table bytes and disposition total match'
    if s in ['analysis','analysis-face']:
        t=r.text('04-analysis.md')
        for q in range(1,8):need(re.search(r'^#{2,4} .*\bQ'+str(q)+r'\b',t,re.M),'missing Q'+str(q))
        need(re.search(r'Q5[^\n]*\n+(?:\n)?~~[^\n]+~~',t),'Q5 not struck in one sentence')
        if s=='analysis-face':
            stats=r.co('table-stats.txt')
            for dim in ['application_status','upstream_status','backport_status','dispositions']:
                for val,n in stats[dim].items():need(f'| {dim} | {val} | {n} |' in t,'currency count differs')
            for x in ['packaging-and-patches.md:91','CLAUDE.md:148','interface-to-first-frame','exit-to-next-first-frame']:need(x in t,'analysis obligation absent')
        return 'seven analysis faces/current counts present'
    if s=='checker-record':
        ns=r.co('generator-fail-first.json');need([x['name'] for x in ns]==['drop','reach','header'],'negative controls missing')
        expected=['membership: expected 107 rows','reach: expected shipped 103/test 4','From header census: expected 87']
        for n,msg in zip(ns,expected):
            text=r.corrected('generator-fail-'+n['name']+'.out').decode()
            need(n['rc']!=0 and text.splitlines()[-1]==n['last_line'] and msg in n['last_line'],'invalid negative control')
        return 'three distinct nonzero negative receipts match raw assertions; not rerun'
    if s=='inherited-record':
        t=section_text(r.text('02-forward-audit.md'),'What the coordinator, the integration and the next slices inherit')
        for x in ['T27','T11','T43','#563','#559','coordinator','#585','L-09','L-17','L-21']:need(x in t,'inherited owner/lead missing '+x)
        need(len(set(re.findall(r'\bL-\d\d\b',r.text('02-forward-audit.md'))))==31,'31 lead census differs');return 'all leads and inherited-owner matrix'
    if s in ['proof-lines','proved']:
        t=r.text('02-forward-audit.md');log=r.text('00-running-log.md');proofs=r.co('proof-index.json')
        need(len(proofs)>0,'no proof rows')
        for i,kind,claim,path in proofs:
            need(kind in ['tree','history','tool-run','fixture','design'],'invalid proof vocabulary')
            need('| '+i+' | proved: '+kind in t and 'PROOF: '+i+' | '+kind in log,'unpaired proof')
        need(len(re.findall(r'proved:',t))==len(re.findall(r'^PROOF:',log,re.M))==len(proofs),'proof counts differ');return 'classified proof lines paired'
    if s=='rulings':
        t=r.text('02-forward-audit.md');need(re.findall(r'^\| ([a-p]) \|',t,re.M)==list('abcdefghijklmnop'),'a-p missing/duplicated');return 'sixteen ruling rows'
    if s=='last-comments':
        for n in [688,1054]:
            cs=r.issues(n,True)
            if not cs:raise Absent('no comments #'+str(n))
        return 'live last comments read; content judgment remains coordinator'
    if s in ['record-lines','fork-written']:
        t=r.text('02-forward-audit.md');p=section_text(t,'The #585 lines owed');need('0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch' in p and '=~' in p and p.lower().count('never sent')>=2,'two never-sent contributions absent')
        need('cbf75c0b06' in t,'ramoops adding commit absent')
        if s=='fork-written':
            q=section_text(r.text('04-analysis.md'),'Renovation face');need('#585' in q and 'ramoops' in q.lower() and '=~' in q,'Q4 lacks both contribution lines')
        return 'two contribution lines with explicit unsent status'
    if s=='runs-record':
        t=section_text(r.text('02-forward-audit.md'),'The runs')
        for x in ['120','106','H700','dry_rc=1','apply_rc=0','43','48','29','D-WORKFLOW-222']:need(x in (t+r.text('02-forward-audit.md')[:1500] if x=='D-WORKFLOW-222' else t),'current runs summary missing '+x)
        for x in ['forbidden-terms-check: 0 hits on stdin','forbidden-terms-check: 1 line(s) on stdin carry a listed word']:need(x in t,'AC17 current output not quoted')
        return 'corrected run counts and AC17 actual output lines'
    if s in ['running-log','no-compile']:
        t=r.text('00-running-log.md');need('census' in t.lower(),'no closing census')
        # Only explicit command records, not prohibitions or quoted source text.
        cmds='\n'.join(l for l in lines(t) if re.match(r'^\s*(?:\+ |\$ |COMMAND: )',l))
        need(not re.search(r'\b(make|kernel_make|scripts/unpack|scripts/build|tools/adjust_kernel_config|tools/check_kernel_config|git fetch|tools/council/run|npm install)\b|config/options.*(?:source|\.)',cmds),'forbidden execution record')
        return 'explicit command census has no prohibited invocation; prose exclusions not counted as commands'
    if s=='handback':
        cs=r.issues(688,True);matches=[c['body'] for c in cs if re.search(r'hand.?back',c['body'],re.I) and r.tip[:10] in c['body']]
        if not matches:raise Absent('no final hand-back naming submitted tip')
        t='\n'.join(matches)
        for x in ['02-forward-audit.md','04-analysis.md','05-punch-list.md']:need(x in t,'hand-back artifact omitted')
        need(not re.search(r'__[A-Z0-9_]+__',t),'hand-back placeholder');return 'single-tip hand-back artifact references'
    if s=='retro':
        if r.fixture:t=r.read('retro.md').decode()
        else:
            fs=[p for p in r.tree(r.tip,'docs/retros/') if p.endswith('-m6-patches-shipped-kernel.md')]
            if len(fs)!=1:raise Absent('final retro absent/ambiguous')
            t=r.blob(fs[0]).decode()
        for x in ['nothing','T42','T43','T27','T11','integration']:need(x in t,'retro obligation absent');
        return 'final retro exists with owner/time-to-play text'
    if s=='question-comments':
        t=r.text('04-analysis.md');cs=r.issues(688,True);found=[]
        for c in cs:
            b=c['body'].lower()
            if '?' in b and (('symlink' in b and '7.0' in b) or ('ramoops' in b and 'mainline' in b)):found.append(c)
        if len(found)<2:raise Absent('two Stage-D question comments absent')
        t2=r.text('02-forward-audit.md');need(all(str(c['id']) in t2 for c in found[-2:]),'question readback IDs absent');return 'two question comments/IDs read back'
    if s=='pins-read':
        rows=r.rows();need(len(rows)==107,'pin table row count')
        for x in rows:
            need(re.search(r'(?<![\d.])(7\.2|7\.1\.2|v2026\.01|20260309)(?![\d.])',x['pin']),'invalid current pin')
            for match in re.findall(r'(?<![\d.])(?:v?\d+(?:\.\d+)+|20260309)(?![\d.])',x['pin']):need(match in ['7.2','7.1.2','v2026.01','20260309'],'unexpected pin value')
        t=r.text('02-forward-audit.md');recipe=r.blob('projects/ROCKNIX/packages/linux/package.mk').decode()
        assignments=[l.strip() for l in recipe.splitlines() if re.match(r'^\s*PKG_(?:VERSION|PATCH_DIRS)\+?=',l)]
        need(sum(l.startswith('PKG_VERSION=') for l in assignments)==5 and sum(l.startswith('PKG_PATCH_DIRS') for l in assignments)==2,'recipe assignment shape differs')
        need(all(l in t for l in assignments),'02 does not quote all five version/two patch-dir assignments');return 'current pins closed vocabulary; all recipe assignments quoted'
    if s=='headers':
        for x in r.rows():
            need(x['origin'].strip() and x['subject'].strip(),'empty origin/subject')
            if x['kind']=='conf':continue
            raw=r.blob(dec(x['path']),SOURCE).decode();head='\n'.join(raw.splitlines()[:60])
            if not re.search(r'^Subject:',head,re.M):need('hand-made' in x['subject'],'missing Subject not marked hand-made')
        inv=r.inventory();heads=[r.blob(dec(x['path']),SOURCE).splitlines()[:60] for x in inv if x['path'].endswith('.patch')]
        need(sum(any(l.startswith(b'From:') for l in h) for h in heads)==87 and sum(any(l.startswith(b'Subject:') for l in h) for h in heads)==89,'header census differs');return 'header census 106/87/89 and explicit unknown/hand-made cells'
    if s=='applies-record':
        rr=validate_applications(r);tab=r.rows()
        for x in tab:
            for a in [z for z in rr if dec(z['path'])==dec(x['path'])]:
                token=f'{a["plan"]}[{a["index"]:03d}] {a["status"]} (apply_rc={a["apply_rc"]}, dry_rc={a["dry_rc"]}; rows/{a["plan"]}-{a["index"]:03d}.json)'
                need(token in x['applies'],'provenance does not consume corrected row')
        return 'D222 corrected rows, source/log hashes, chain, normal rc, diagnostic mismatch and prefix guard verified'
    if s=='upstream-status':
        inv=r.inventory();cnt=C.Counter();rows={dec(x['path']):x for x in r.rows()}
        for x in inv:
            p=dec(x['path'])
            try:b=r.blob(p,UPSTREAM)
            except Absent:b=None
            status='ABSENT' if b is None else 'SAME' if b==r.blob(p,SOURCE) else 'CHANGED';cnt[status]+=1
            expect='upstream-changed' if status=='CHANGED' else '#585' if '0950-' in p else 'upstream-moved' if status=='ABSENT' else 'keep'
            need(rows[p]['disposition']==expect,'upstream disposition differs')
            if rows[p]['upstream']=='claims mainline':need('Upstream-Status' in rows[p]['note'],'unsupported mainline claim')
        need(cnt=={'SAME':101,'CHANGED':4,'ABSENT':2},'upstream census differs');return '101/4/2 immutable comparison and dispositions'
    if s=='tarball-hashes':
        a=r.co('archive-sha256.json');need(len(a)==5,'five archive receipts required')
        for x in a.values():need(x['sidecar_equal'] and x['recipe_equal'] and x['sha256'].encode() in r.blob(x['recipe'],SOURCE),'archive/sidecar/recipe hash mismatch')
        t=r.text('02-forward-audit.md');need(t.count('= its .sha256')>=2,'two archive hash lines not quoted')
        for k,x in a.items():
            if k.startswith('linux/'):need(x['sha256'][:16] in t,'quoted archive prefix differs')
        return 'retained archive hashes match immutable recipe and quoted prefixes; no archive read'
    if s=='device-groups':
        inv=r.inventory();counts=C.Counter(tuple(x['reachable_by']) for x in inv)
        need(sorted(counts.values())==sorted([4,32,56,1,4,6,4]),'device group sizes differ')
        scope=section_text(r.text('01-research-notes.md'),'Scope');need('reachable_by' in scope and '107' in scope,'scope group record absent');return 'seven reach groups sum to 107'
    if s=='non-kernel':
        rs=[x for x in r.rows() if '/u-boot-' in x['path'] or '/kernel-firmware/patches/' in x['path']]
        need(len(rs)==5,'non-kernel census differs')
        for x in rs:need(x['kind']=='non-kernel' and x['owner']==('T27' if '/u-boot-' in x['path'] else 'T11'),'non-kernel kind/owner wrong')
        return 'four U-Boot T27 / firmware T11 rows'
    if s in ['scratch','scratch-retired']:
        t=r.text('00-running-log.md')
        if not re.search(r'/workspace/tmp/m6-t41/src/?[^\n]*retired|retired[^\n]*/workspace/tmp/m6-t41/src',t,re.I):raise Absent('Stage-H retirement record absent')
        path=r.root/'lane-scratch/src' if r.fixture else P.Path('/workspace/tmp/m6-t41/src')
        need(not path.exists() and not path.is_symlink(),'source scratch still present');return 'retirement record plus source-directory absence (no contents read)'
    raise Invalid('unimplemented section '+s)

def main():
    selected=os.environ.get('ACCEPT_ONLY','').split() or SECTIONS
    need(len(selected)==len(set(selected)) and set(selected)<=set(SECTIONS),'unknown/duplicate selected section')
    try:r=Reader()
    except (Absent,Cannot,Invalid) as e:
        state='ABSENT' if isinstance(e,Absent) else 'CANNOT' if isinstance(e,Cannot) else 'FAIL'
        for s in selected:print(state+'\t'+s+'\t'+str(e))
        return
    for s in selected:
        try:msg=check(r,s);state='PASS'
        except Absent as e:state,msg='ABSENT',str(e)
        except Cannot as e:state,msg='CANNOT',str(e)
        except (Invalid,KeyError,ValueError,TypeError,IndexError,UnicodeError,OSError) as e:state,msg='FAIL',str(e) if isinstance(e,Invalid) else 'malformed or unreadable artifact: '+type(e).__name__
        print(state+'\t'+s+'\t'+fmt(str(msg).replace('\n',' ').replace('\t',' ')))
if __name__=='__main__':
    try:main()
    except Exception:print('FAIL\targuments\tinvalid candidate invocation');sys.exit(1)
