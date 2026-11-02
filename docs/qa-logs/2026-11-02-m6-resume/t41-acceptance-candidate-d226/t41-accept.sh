#!/bin/bash
# GENERATED D226 candidate. Accepted producers are reconciled, never replayed.
# Not installed, not a final acceptance; coordinator retains rulings and acceptance.
# Shared verdict/mask/summary from t36-accept.sh, exact pinned SHA below.
# SOURCE_SHA=e32e28e0145570008d08493594795a878c442e88ed9fb3aac70f95e10d6b5b1b
# Author: Codex (GPT-6), /root, wN:p5; session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
# AUDIT_ISSUE=N BUGS="N ..." DISPATCH_TIP=HASH bash t41-accept.sh LANE_TIP COORD_TIP
# ACCEPT_ONLY and ACCEPT_FIXTURE_ROOT select constructed section fixtures only.
# New final gates run in disposable owned clones. Never execute accepted producers.
set -u
set -o pipefail
umask 077
export LC_ALL=C
OWN=/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12
ACCEPT_DIR=${ACCEPT_DIR:-$OWN/run}
OUT=${OUT:-$OWN/run.out}
ACCEPT_ONLY=${ACCEPT_ONLY:-}
export DIST_REPO=${DIST_REPO:-/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649}
export ACCEPT_ONLY ACCEPT_DIR
# Refuse before any write. Both destination files and ancestors must resolve inside
# the assigned root, with no symlink or hardlink targets. No cleanup/deletion.
python3 -I - "$OWN" "$ACCEPT_DIR" "$OUT" "${ACCEPT_FIXTURE_ROOT:-}" <<'T41_PATH_GUARD'
import os,pathlib,sys
root=P=pathlib.Path(sys.argv[1]);root=root.absolute()
try:
 if root.resolve()!=root:raise ValueError()
 accept=pathlib.Path(sys.argv[2]);out=pathlib.Path(sys.argv[3])
 if accept.exists() and not accept.is_dir():raise ValueError()
 if out.exists() and not out.is_file():raise ValueError()
 if out.absolute()==(accept/'verdicts.tsv').absolute():raise ValueError()
 for raw in sys.argv[2:]:
  if not raw:continue
  p=pathlib.Path(raw).absolute()
  if p==root or not p.is_relative_to(root) or p.resolve()!=p:raise ValueError()
  if p.exists() and p.is_file() and p.stat().st_nlink!=1:raise ValueError()
 for raw in [sys.argv[2]+'/verdicts.tsv']:
  p=pathlib.Path(raw)
  if p.is_symlink() or (p.exists() and (not p.is_file() or p.stat().st_nlink!=1)):raise ValueError()
except (ValueError,OSError):sys.exit(1)
T41_PATH_GUARD
rc=$?
if [ "$rc" -ne 0 ]; then
 printf 'VERDICT FAIL confinement -- output or fixture path is not private to the assigned directory\nSUMMARY: pass 0, fail 1, cannot 0, absent 0, ran 0\nACCEPT-RC 1\n'
 exit 1
fi
if [ "$#" -ne 2 ] || [ -z "${DISPATCH_TIP:-}" ] || [ -z "${AUDIT_ISSUE+x}" ] || [ -z "${BUGS+x}" ]; then
 printf 'VERDICT FAIL arguments -- two tips, DISPATCH_TIP, AUDIT_ISSUE and BUGS required\nSUMMARY: pass 0, fail 1, cannot 0, absent 0, ran 0\nACCEPT-RC 1\n'
 exit 1
fi
TIP=$1
COORD=$2
mkdir -p -- "$ACCEPT_DIR" "$(dirname -- "$OUT")"
rc=$?
[ "$rc" -eq 0 ] || exit 1

MASK='s/((token|key|pass(w[a-z]*)?|psk|user) *[=:] *)[^ ]*/\1***/Ig; s/(--(token|key|pass(w[a-z]*)?|psk|user)[= ]+)[^ ]+/\1***/Ig'
np=0; nf=0; nc=0; na=0; nr=0; S=
want() { [ -z "$ACCEPT_ONLY" ] && return 0; case " $ACCEPT_ONLY " in *" $1 "*) return 0;; *) return 1;; esac; }
section() { S=$1; printf '\n== %s\n' "$2"; }
verdict() {
  local v=$1; shift
  case $v in PASS) np=$((np+1));; FAIL) nf=$((nf+1));; CANNOT) nc=$((nc+1));; ABSENT) na=$((na+1));; RAN) nr=$((nr+1));; esac
  printf 'VERDICT %s %s -- %s\n' "$v" "$S" "$*"
}

main() {
printf 'T41 D226 candidate: retained producer reconciliation and executable final gates\n'
[ -n "${ACCEPT_FIXTURE_ROOT:-}$ACCEPT_ONLY" ] && printf 'SELF-TEST MODE: section fixtures; never final acceptance\n'
python3 -I - "$TIP" "$COORD" > "$ACCEPT_DIR/verdicts.tsv" <<'T41_CANDIDATE_PREDICATES'
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
"""D226 accepted-producer reconciliation: object reads only, no replay.
Immutable anchors bind commands, fixtures and observations. New measurements are
limited to stored bytes; historical archive/tree digests remain observations.
"""
STAGE_A='cffe3f869c5ced124e26befa36505350b4964f77'
STAGE_A_PROGRAM='f03b64419fa656fb3af61cbc8d174284020d439c'
STAGE_B='7e5d1546712df2eb79c585fce663186770d1ceb9'
STAGE_C='94b5b1c0b983313325dba101217761c6e5c9bca0'
P1='2174265e9c'
T4='6ec78bbf8c'
T4_FOLDER='docs/audits/2026_10_24-epic-m6-doctrine-rules'
BLOCK_SHA='4d300124a6bf116f9c0177712e8f0a824b35db45cc5a042acbd4cc58445192a3'

def unchanged(r,path,ref):
    a=r.tree(ref,path);b=r.tree(r.tip,path)
    if not a:raise Absent('accepted identity absent: '+path+' at '+ref)
    need(a==b,'changed accepted input/program/mode: '+fmt(path)+' (anchor '+ref[:12]+')')
    return r.blob(path,ref)

def frozen_receipt(r,path,ref):
    expected=r.blob(r.af+'/'+path,ref)
    actual=r.audit(path)
    need(expected==actual,'accepted receipt changed: '+path)
    return actual

def reconcile_membership(r):
    brief=r.blob(BRIEF,AUTH).decode()
    def extract(name,lang):
        a='<!-- t41 '+name+' begin -->';b='<!-- t41 '+name+' end -->'
        need(brief.count(a)==brief.count(b)==1,'membership brief marker shape')
        chunk=brief.split(a,1)[1].split(b,1)[0]
        m=re.search(r'\n```'+lang+r'\n(.*?)\n```\n',chunk,re.S)
        need(m is not None,'membership brief fence shape');return (m.group(1)+'\n').encode()
    block=extract('block.sh','bash');expected=extract('block expected','')
    need(sha(block)==BLOCK_SHA or (r.fixture and block==r.blob(r.af+'/stage-a/p1-qa-scratch/block.sh',STAGE_A)),'membership block SHA mismatch')
    need(len(block.splitlines())==148 and len(expected.splitlines())==99,'membership 148/99 shape differs')
    for p in ['block.out','block-tip.out','p1-qa-scratch/block-expected.txt']:
        need(dec(frozen_receipt(r,'stage-a/'+p,STAGE_A).decode())==dec(expected.decode()),'retained 99-line output differs')
    need(frozen_receipt(r,'stage-a/p1-qa-scratch/block.sh',STAGE_A)==block,'retained block differs from authority')
    for name in ['slices','inventory','areas']:
        path='docs/reviews/'+name+'.json';unchanged(r,path,P1)
    paths=None
    for side in ['p1','tip']:
        for name in ['paths','text']:
            b=frozen_receipt(r,f'stage-a/{side}-qa-scratch/{name}.txt',STAGE_A)
            ps=dec(b.decode()).splitlines()
            need(len(ps)==len(set(ps))==107 and ps==sorted(ps),'membership paths not 107 sorted unique')
            if paths is None:paths=ps
            need(ps==paths,'P1/tip/text selected paths differ')
    need(paths==sorted(dec(x['path']) for x in r.inventory()),'corrected inventory membership differs')
    # Modes and objects, not a re-execution of the historical membership program.
    all_p1=r.tree(P1,'');all_tip=r.tree(r.tip,'')
    for p in paths:
        need(p in all_p1 and all_p1[p].split()[0] in ['100644','100755'],'selected path is not a regular blob')
        need(all_tip.get(p)==all_p1[p],'selected immutable mode/blob changed: '+fmt(p))
    check(r,'tree-counts')
    combined=frozen_receipt(r,'stage-a/run/stage-a.out',STAGE_A).decode()
    for t in ['block rc=0','block at the tip rc=0','block = the brief\'s expected lines','the same lines at the tip']:need(t in combined,'membership command/exit evidence absent')
    return 'D226: 148-line retained block, identical 99-line outputs, three P1 inputs, 107 selected modes/blobs/counts reconciled; no replay'

def reconcile_lint(r):
    # The accepted command names an immutable full T4 folder plus one exact JSON
    # deletion. This identifies the fixture without opening its retired scratch.
    brief=r.blob(BRIEF,AUTH).decode()
    for text in ['F=$(git ls-tree -d --name-only 6ec78bbf8c','d.pop("tier_exception",None)','tools/lint-audit-artifacts "$L/pass/$F"','tools/lint-audit-artifacts "$L/fail/$F"']:
        need(text in brief,'historical Local fixture command identity changed')
    unchanged(r,'tools/lint-audit-artifacts',STAGE_A_PROGRAM)
    tree=r.tree(T4,T4_FOLDER+'/');need(bool(tree),'T4 fixture identity absent')
    # No archive/export: hash selected committed blobs, including the plan, in memory.
    for p in tree:unchanged(r,p,T4)
    plan=json.loads(r.blob(T4_FOLDER+'/second-opinions/review-plan.json',T4))
    need(plan.get('depth')=='local' and plan.get('tier_exception')=='D-WORKFLOW-184' and plan.get('reviewers')==[],'historical Local fixture has wrong plan')
    positive=frozen_receipt(r,'stage-a/lint-local-pass.out',STAGE_A).decode()
    negative=frozen_receipt(r,'stage-a/lint-local-fail.out',STAGE_A).decode()
    raw=frozen_receipt(r,'stage-a/run/stage-a.out',STAGE_A).decode()
    need(positive.rstrip().endswith('\nPASS'),'historical Local positive lacks PASS')
    need('FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone' in negative and negative.rstrip().endswith('1 CONTRACT FAILURE(S)'),'historical Local refusal differs')
    for t in ['t4 plan: local D-WORKFLOW-184 0','lint, a Local plan, rc=0','lint, tier_exception removed, rc=1']:need(t in raw,'historical Local exit/fixture receipt absent')
    return 'D226: exact unchanged lint/T4 immutable fixture, tier_exception deletion command, positive/refusal and rc receipts reconciled; no replay'

def reconcile_generator(r):
    # Read-only Stage-C promotion packet. It does not certify newly changed inputs.
    validation=json.loads(frozen_receipt(r,'stage-c/validation.json',STAGE_C))
    promotion=json.loads(frozen_receipt(r,'stage-c/promotion.json',STAGE_C))
    program=unchanged(r,r.af+'/tools/t41-tables.py',STAGE_C)
    need(sha(program)==validation['checked_program_sha256']==promotion['formal_sha256'],'formal generator identity differs')
    draft=unchanged(r,r.af+'/stage-b/corrected/t41-tables.py',STAGE_B)
    need(sha(draft)==promotion['draft_sha256'],'draft generator identity differs')
    # All retained corrected inputs/source bytes must still be identical. No private
    # negative-fixture directory is opened and no historical generator is invoked.
    for p in r.tree(STAGE_C,r.af+'/stage-b/corrected/'):
        unchanged(r,p,STAGE_C)
    for row in r.inventory():unchanged(r,dec(row['path']),SOURCE)
    checks=validation['checks']
    modes=['stats','provenance','coverage','currency','json']
    names=['formal-generator-negative-'+x for x in ['drop','reach','header']]+['formal-generator-'+x for x in modes]
    selected=[x for x in checks if x.get('name') in names]
    need([x['name'] for x in selected]==names,'three negatives must precede five positives')
    assertions=['membership: expected 107 rows','reach: expected shipped 103/test 4','From header census: expected 87']
    for i,x in enumerate(selected):
        out=frozen_receipt(r,'stage-c/'+relpath(x['output']),STAGE_C)
        need(sha(out)==x['sha256'],'formal generator output hash differs')
        need(x['argv'][:3]==['python3','-I',r.af+'/tools/t41-tables.py'],'formal generator command differs')
        need(x['start'] and x['elapsed_seconds']>=0,'generator command timing absent')
        if i<3:
            kind=['drop','reach','header'][i];opt='--bytes-from' if kind=='header' else '--rows-from'
            suffix='/bytes' if kind=='header' else '/'+kind+'.json'
            need(x['rc']==1 and x['argv'][3:5]==['stats',opt] and len(x['argv'])==6 and x['argv'][5].endswith(suffix),'negative control command/exit differs')
            need(out.decode().splitlines()[-1]=='AssertionError: '+assertions[i],'negative control assertion differs')
        else:
            mode=modes[i-3];need(x['rc']==0 and x['argv'][3:]==[mode],'positive command/exit differs')
            need(out==r.corrected('table-'+mode+'.txt'),'positive not equal to accepted corrected table')
    need(validation['outputs_equal_accepted_tables'] is True,'formal output comparison absent')
    # The published packet binds program and OUTPUT hashes, but not exact negative
    # INPUT bytes. D226 explicitly requires those identities. Do not infer them
    # from an absolute argv path or recreate fixtures. Await coordinator disposition.
    missing=[x['name'] for x in selected[:3] if not x.get('input_identity')]
    if missing:raise Cannot('D226 exact negative input identities absent in accepted stage-c/validation.json: '+', '.join(missing)+'; paths and assertions do not identify bytes; coordinator evidence/ruling required, no replay')
    # Reserved executable seam for a future coordinator-authorized identity record.
    # No current producer supplies one, so a foreign shape cannot silently pass.
    raise Cannot('D226 negative input identity record now present but its schema/authority is not ruled; coordinator integration required, no replay')

def reconcile_check(r,s):
    if s=='membership':return reconcile_membership(r)
    if s=='lint-proof':return reconcile_lint(r)
    if s=='checker-run':return reconcile_generator(r)
    if s=='runs':
        validate_applications(r);check(r,'tarball-hashes');check(r,'runs-record')
        return 'D226: accepted 120/106 normal-application receipts, log/source hashes, prefix links/control and H700-011 reconciled; archive/tree digests are retained observations'
    raise Invalid('unknown reconciliation gate')

"""D226 final gates. Embedded after receipt predicates; never run an accepted producer.
Only new final checks execute, in a fresh disposable local clone below ACCEPT_DIR.
Author: Codex (GPT-6), /root, wN:p5, session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
"""
import datetime, time, tempfile, signal
TOOL_REF='c9fe606e8d7e7e0f6c70cc686764d1503029d278'
TOOL_PATHS=['tools/lint-audit-artifacts','tools/rules-check','tools/register-check','tools/work-log-index','tools/ceremony-check','tools/box-check','tools/forbidden-terms-check']
SECRET_CMD='. .githooks/secret-patterns; /usr/bin/grep -a -c -E -e "${SECRET_PATTERNS}"'
CHECK_CMDS=[['tools/register-check'],['tools/work-log-index','--check'],['tools/rules-check','--quiet'],['tools/ceremony-check','--gate'],['.githooks/hooks-test']]
OWN=P.Path('/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12')
def private_path(p):
    p=P.Path(p).absolute()
    need(p.is_relative_to(OWN) and p!=OWN and p.resolve()==p,'execution write path outside owned scratch or symlink')
    if p.exists() and p.is_file():need(p.stat().st_nlink==1,'execution write hardlink')
    return p

def mask_log(b):
    # Same two permitted masks as t36's outer filter, applied before persistence too.
    t=b.decode('utf-8',errors='replace')
    t=re.sub(r'((?:token|key|pass(?:w[a-z]*)?|psk|user) *[=:] *)[^ \n\r]*',r'\1***',t,flags=re.I)
    t=re.sub(r'(--(?:token|key|pass(?:w[a-z]*)?|psk|user)[= ]+)[^ \n\r]+',r'\1***',t,flags=re.I)
    return t.encode()

class FinalGates:
    def __init__(self,r):
        self.r=r;self.n=0;self.clones={};self.history_refs=None
        root=private_path(os.environ['ACCEPT_DIR']);root.mkdir(parents=True,exist_ok=True)
        self.root=private_path(tempfile.mkdtemp(prefix='final-gates-',dir=root))
        self.tmp=self.root/'tmp';self.tmp.mkdir()
        # Do not inherit ES_SRC, shell startup, Git overrides, arbitrary Python paths,
        # or credentials in argv. gh alone retains its existing authentication context.
        keep=['PATH','HOME','GH_TOKEN','GITHUB_TOKEN','GH_HOST','GH_CONFIG_DIR','XDG_CONFIG_HOME','SSL_CERT_FILE','SSL_CERT_DIR','FORBIDDEN_PATTERNS']
        self.env={k:os.environ[k] for k in keep if k in os.environ}
        self.env.update(LC_ALL='C',TMPDIR=str(self.tmp),TMP=str(self.tmp),TEMP=str(self.tmp),PYTHONDONTWRITEBYTECODE='1',
            GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_TERMINAL_PROMPT='0',GIT_OPTIONAL_LOCKS='0',
            GIT_AUTHOR_NAME='Codex acceptance simulation',GIT_AUTHOR_EMAIL='codex-acceptance@invalid',
            GIT_COMMITTER_NAME='Codex acceptance simulation',GIT_COMMITTER_EMAIL='codex-acceptance@invalid')
        opts={'core.hooksPath':'/dev/null','core.fsmonitor':'false','core.attributesFile':'/dev/null','init.templateDir':'',
              'commit.gpgsign':'false','tag.gpgsign':'false','protocol.allow':'never','protocol.file.allow':'always',
              'submodule.recurse':'false','core.quotePath':'true'}
        self.env['GIT_CONFIG_COUNT']=str(len(opts))
        for i,(k,v) in enumerate(opts.items()):self.env['GIT_CONFIG_KEY_'+str(i)]=k;self.env['GIT_CONFIG_VALUE_'+str(i)]=v
    def command(self,label,argv,cwd=None,data=None,expect=(0,),last=None,env=None,timeout=120):
        """Persist masked stdout/stderr plus hashes of actual bytes, argv/input/exit/time.
        Missing executable/timeouts => CANNOT; a completed wrong rc/output => FAIL.
        Never invoke a shell except the literal secret-patterns interface above.
        """
        need(re.fullmatch('[a-z0-9-]+',label),'invalid command receipt label')
        cwd=private_path(cwd or self.root);need(cwd.is_dir(),'command cwd absent')
        need(isinstance(argv,list) and all(isinstance(a,str) and '\x00' not in a for a in argv),'invalid argv')
        allowed={'git','gh','python3','bash',*TOOL_PATHS,'.githooks/hooks-test'}
        need(argv[0] in allowed,'unreviewed executable')
        if argv[0]=='bash':need(argv==['bash','--noprofile','--norc','-c',SECRET_CMD],'unreviewed shell program')
        if argv[0]=='python3':need(argv[1:4]==['-I','-m','py_compile'] and len(argv)==5,'producer execution forbidden')
        if argv[0]=='gh':need(argv[1]=='api' and len(argv)>2 and argv[2].startswith('repos/pixelelated/distribution/issues/'),'non-read GitHub command')
        e=dict(self.env);e.update(env or {})
        self.n+=1;stem=f'{self.n:04d}-{label}';started=datetime.datetime.now(datetime.timezone.utc).isoformat();start=time.monotonic()
        rc=None;out=b'';err=b'';problem=None;timed=False
        try:
            p=subprocess.Popen(argv,cwd=cwd,env=e,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            try:out,err=p.communicate(data,timeout=timeout)
            except subprocess.TimeoutExpired:
                timed=True;os.killpg(p.pid,signal.SIGKILL);out,err=p.communicate();problem='command timed out'
            rc=p.returncode
        except OSError as x:problem='executable unavailable ('+type(x).__name__+')'
        record={'schema':1,'identity':'Codex (GPT-6), /root, wN:p5','label':label,'argv':argv,'cwd':str(cwd),
            'start':started,'elapsed_seconds':round(time.monotonic()-start,6),'rc':rc,'timed_out':timed,'problem':problem,
            'stdin_sha256':None if data is None else sha(data),'stdin_bytes':0 if data is None else len(data),
            'stdout_sha256':sha(out),'stderr_sha256':sha(err),'stdout':stem+'.stdout','stderr':stem+'.stderr',
            'stdout_masked_sha256':sha(mask_log(out)),'stderr_masked_sha256':sha(mask_log(err)),
            'lane_tip':self.r.tip,'coordinator_tip':self.r.coord,'fixture':bool(self.r.fixture)}
        for suffix,content in [('stdout',mask_log(out)),('stderr',mask_log(err)),('json',(json.dumps(record,indent=2)+'\n').encode())]:
            path=private_path(self.root/(stem+'.'+suffix))
            with path.open('xb') as f:f.write(content)
        if problem:raise Cannot(label+': '+problem+'; receipt '+str(self.root/(stem+'.json')))
        need(rc in expect,label+': unexpected rc '+str(rc)+'; receipt '+str(self.root/(stem+'.json')))
        if last is not None:need(out.decode(errors='replace').rstrip().splitlines()[-1:]==[last],label+': required final output line absent')
        return out,rc
    def verified_tools(self,ref):
        r=self.r
        paths=TOOL_PATHS+list(r.tree(TOOL_REF,'.githooks/'))
        for p in paths:
            expected=r.tree(TOOL_REF,p);actual=r.tree(ref,p)
            if not expected or expected!=actual:raise Cannot('final executable changed from reviewed '+TOOL_REF[:12]+': '+p)
        # Audit-local generator is syntax-checked only, never executed here.
    def clone(self,integrated=False):
        key='integration' if integrated else 'lane'
        if key in self.clones:return self.clones[key]
        r=self.r;r.final_artifacts();self.verified_tools(r.tip)
        if integrated:self.verified_tools(r.coord)
        repo=P.Path(r.repo).resolve();need(repo.is_dir(),'local object store absent')
        dest=self.root/key
        need(not dest.exists(),'simulation destination exists')
        self.command(key+'-clone',['git','clone','--quiet','--shared','--no-checkout','--no-hardlinks','--template=',str(repo),str(dest)])
        # ceremony-check's actual interface resolves next and upstream/next, not
        # HEAD. Snapshot those existing local refs once; never fetch or silently
        # rebind them to the lane. Both simulations get identical recorded hashes.
        if self.history_refs is None:
            self.history_refs={}
            for ref in ['refs/heads/next','refs/remotes/upstream/next']:
                out,rc=self.command('source-history-ref',['git','-C',str(repo),'rev-parse','--verify',ref+'^{commit}'],expect=tuple(range(256)))
                if rc:raise Cannot('ceremony-check required local history ref unavailable: '+ref)
                full=out.decode().strip();need(re.fullmatch('[0-9a-f]{40}',full),'history ref is not a full commit')
                self.history_refs[ref]=full
        for ref,full in self.history_refs.items():
            self.command(key+'-history-ref',['git','update-ref',ref,full],dest)
        self.command(key+'-checkout',['git','checkout','--quiet','--detach',r.coord if integrated else r.tip],dest)
        before,_=self.command(key+'-head-before',['git','rev-parse','HEAD'],dest)
        expected=r.git('rev-parse',(r.coord if integrated else r.tip)+'^{commit}').strip()
        need(before.strip()==expected,'checkout did not select exact immutable tip')
        if integrated:
            # No commit, no hooks, no live refs and no conflict auto-resolution.
            self.command('integration-merge',['git','-c','merge.autoStash=false','merge','--no-edit','--no-commit','--no-ff',r.tip],dest)
            unmerged,_=self.command('integration-unmerged',['git','ls-files','-u'],dest)
            need(not unmerged,'integration contains unresolved entries')
            self.command('integration-whitespace',['git','diff','--check','--cached'],dest)
        self.validate_clone_paths(dest)
        self.clones[key]=dest
        return dest
    def validate_clone_paths(self,dest):
        # Readers only traverse their checked record/tool roots. No symlink or held
        # output is allowed in those inputs, including nested audit evidence.
        for roof in ['docs','.claude','tools','.githooks']:
            d=dest/roof
            if not d.exists():continue
            for p in d.rglob('*'):
                if p.is_symlink():raise Cannot('checker input is a symlink: '+str(p.relative_to(dest)))
        for p in (dest/'docs/audits').rglob('*.held.json'):
            v=json.loads(p.read_text());reply=p.parent/v.get('reply','')
            need(reply.resolve().is_relative_to(p.parent.resolve()),'held declaration path escapes records')
            if reply.is_file():raise Cannot('held reply is present in checker input; no held read authorized')
    def lint(self,dest,prefix='lane'):
        n=os.environ.get('AUDIT_ISSUE','')
        if not n or n=='0':raise Absent('no final audit issue for resolution lint')
        need(n.isdigit(),'audit issue must be numeric')
        # Validate Local-only scope before invoking the checker.
        v=json.loads((dest/self.r.af/'second-opinions/review-plan.json').read_bytes())
        need(v.get('depth')=='local' and v.get('reviewers')==[] and v.get('tier_exception')=='D-WORKFLOW-184','not the authorized Local review')
        for suffix,args in [('default',[]),('issue',['--issue',n])]:
            self.command(prefix+'-lint-'+suffix,['tools/lint-audit-artifacts',self.r.af,*args],dest,last='PASS')
    def forbidden(self,dest,prefix='lane',whole=False):
        # The checker alone may read its normal private wordlist; it is never copied,
        # opened or sourced by this harness. Positive uses an explicitly public regex.
        self.command(prefix+'-forbidden-positive',['tools/forbidden-terms-check','--stdin'],dest,
            b'synthetic t41 sentinel\n',expect=(1,),last='forbidden-terms-check: 1 line(s) on stdin carry a listed word',env={'FORBIDDEN_PATTERNS':'synthetic[ ]t41[ ]sentinel'})
        if whole:self.command(prefix+'-forbidden-tree',['tools/forbidden-terms-check'],dest)
        paths=self.record_paths()
        for i,p in enumerate(paths):
            self.command(prefix+'-forbidden-record-'+str(i),['tools/forbidden-terms-check','--stdin'],dest,
                self.checked_record(dest,p),last='forbidden-terms-check: 0 hits on stdin')
    def record_paths(self):
        r=self.r;ps=r.git('diff','--name-only','--diff-filter=ACMR','-z',r.dispatch,r.tip).split(b'\0')
        paths=[p.decode() for p in ps if p]
        # Include complete final audit records even if unchanged from dispatch.
        paths=sorted(set(paths)|set(r.tree(r.tip,r.af+'/')))
        need(bool(paths),'no final records to scan')
        for p in paths:
            relpath(p);need(p.startswith(('docs/','.github/sessions/',r.af+'/')),'unexpected final changed path')
        return paths
    def checked_record(self,dest,p):
        q=dest/p;need(q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(dest),'record absent or unsafe')
        need(not q.name.endswith('.held.json') and '/held/' not in p,'held input outside scope')
        return q.read_bytes()
    def secret(self,dest,prefix='lane'):
        cmd=['bash','--noprofile','--norc','-c',SECRET_CMD]
        self.command(prefix+'-secret-compile',cmd,dest,b'',expect=(1,),last='0')
        positive=('dev'+'password='+'QwErTyUiOpAsDfGh'+'\n').encode()
        self.command(prefix+'-secret-positive',cmd,dest,positive,last='1')
        for i,p in enumerate(self.record_paths()):self.command(prefix+'-secret-record-'+str(i),cmd,dest,self.checked_record(dest,p),expect=(1,),last='0')
    def checkers(self,dest,prefix='lane'):
        for cmd in CHECK_CMDS:
            self.command(prefix+'-'+P.PurePosixPath(cmd[0]).name,cmd,dest,last='PASS' if cmd[0]=='.githooks/hooks-test' else None,timeout=240)
        # --gate tolerates CI-only debt. Its text is retained for coordinator judgment;
        # its documented exit is the criterion, never a historical checker receipt.
        self.forbidden(dest,prefix,whole=True)
        self.lint(dest,prefix)
    def issues(self,n,comments=False):
        need(str(n).isdigit(),'invalid issue number')
        argv=['gh','api','repos/pixelelated/distribution/issues/'+str(n)+('/comments?per_page=100' if comments else '')]
        if comments:argv+=['--paginate','--slurp']
        raw,rc=self.command('live-'+str(n)+('-comments' if comments else ''),argv,expect=tuple(range(256)))
        if rc:raise Cannot('live issue read unavailable #'+str(n)+'; command/exit receipt retained')
        v=json.loads(raw)
        if comments:
            need(isinstance(v,list) and all(isinstance(x,list) for x in v),'invalid paginated comments')
            v=sum(v,[])
        else:need(isinstance(v,dict) and v.get('number')==int(n) and isinstance(v.get('body'),str),'invalid live issue response')
        return v

def final_gates(r):
    if not hasattr(r,'final'):r.final=FinalGates(r)
    return r.final

def executable_check(r,s):
    f=final_gates(r)
    if s in ['audit-boxes','bug-boxes','lane-boxes']:
        items=[r.audit_issue()] if s=='audit-boxes' else r.bugs() if s=='bug-boxes' else [r.issues(688)]
        # An inherited bug may remain open for the integration. box-check validates
        # its criteria; only the audit's Phase-7 outcomes must all be disposed.
        for i in items:
            if s=='audit-boxes':need(not re.search(r'^\s*- \[ \]',i['body'],re.M),'audit has unresolved outcome checkbox')
            num=i.get('number',i.get('issue_number'));need(isinstance(num,int),'issue number absent')
            d=f.clone();f.command('checkbox-'+str(num),['tools/box-check','--issue',str(num)],d)
        return 'live issue criteria and executable box-check receipts retained'
    d=f.clone(s=='merge')
    if s=='lint':f.lint(d)
    elif s=='forbidden':f.forbidden(d)
    elif s=='secret':f.secret(d)
    elif s in ['checkers','merge']:
        f.checkers(d,'integration' if s=='merge' else 'lane')
        if s=='merge':f.secret(d,'integration')
    elif s=='generators':
        # py_compile parses bytes without importing or executing the generator.
        f.command('generator-syntax',['python3','-I','-m','py_compile',str(d/r.af/'tools/t41-tables.py')],d)
    else:raise Invalid('unknown executable gate')
    return 'new final '+s+' commands completed; masked evidence '+str(f.root)

if __name__=='__main__':
    try:main()
    except Exception:print('FAIL\targuments\tinvalid candidate invocation');sys.exit(1)

T41_CANDIDATE_PREDICATES
rc=$?
if [ "$rc" -ne 0 ]; then
 section internal "candidate predicate process"
 verdict FAIL "predicate process did not finish"
else
 while IFS=$'\t' read -r state name reason; do
  case "$state" in PASS|FAIL|CANNOT|ABSENT|RAN) ;; *) state=FAIL; reason="invalid predicate state";; esac
  section "$name" "$name"
  verdict "$state" "$reason"
 done < "$ACCEPT_DIR/verdicts.tsv"
 if [ $((np + nf + nc + na + nr)) -eq 0 ]; then
  section internal "empty candidate result"
  verdict FAIL "no sections checked"
 fi
fi
# ---------------------------------------------------------------- summary
# No host/runtime census in T41.
printf '\nSUMMARY: pass %s, fail %s, cannot %s, absent %s, ran %s; done at %s UTC\n' "$np" "$nf" "$nc" "$na" "$nr" "$(date -u +%H:%M:%S)"
if [ "$nf" -gt 0 ]; then final=1; elif [ $((nc + na)) -gt 0 ]; then final=2; else final=0; fi
printf 'ACCEPT-RC %s\n' "$final"
return "$final"
}

main "$@" 2>&1 | sed -E "$MASK" | tee -a "$OUT"
exit "${PIPESTATUS[0]}"
