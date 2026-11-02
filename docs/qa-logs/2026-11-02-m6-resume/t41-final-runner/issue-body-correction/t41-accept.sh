#!/bin/bash
# GENERATED D226 candidate. Accepted producers are reconciled, never replayed.
# Not installed, not a final acceptance; coordinator retains rulings and acceptance.
# Shared verdict/mask/summary from t36-accept.sh, exact pinned SHA below.
# SOURCE_SHA=e32e28e0145570008d08493594795a878c442e88ed9fb3aac70f95e10d6b5b1b
# Author: Codex (GPT-6), /root, wN:p5; session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
# Final executable gates require ACCEPT_EXECUTOR_JSON with actual harness/model/effort/session/pane/identity_source.
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
printf 'T41 D226/D228 candidate: retained producer reconciliation and executable final gates\n'
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
        b=self.git('ls-tree','-rz',ref,*(['--',path] if path else []));return {row.split(b'\t',1)[1].decode():row.split(b'\t',1)[0].decode() for row in b.split(b'\0') if row}
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
            # Every changed commit is checked, so editing and restoring a product
            # or proof blob does not disappear in an aggregate-tip diff.
            selected={dec(x['path']) for x in r.inventory()}
            for p in selected:
                need(r.tree(SOURCE,p)==r.tree(r.tip,p),'selected source mode/blob changed')
            for c in commits:
                paths=[p.decode() for p in r.git('diff-tree','--no-commit-id','--no-renames','--name-only','-z','-r',c).split(b'\0') if p]
                for p in paths:
                    need(p not in selected and not p.startswith(('packages/','projects/','tools/','scripts/')),'lane changed protected product/source path')
                    if p in ['docs/decision-register.md','docs/blindspot-register.md']:
                        changes=r.git('diff-tree','--no-commit-id','--no-renames','--numstat','-z','-r',c,'--',p).split(b'\0')
                        need(all(row.split(b'\t',2)[1:2]==[b'0'] for row in changes if row),'lane removed register lines')
                    if re.search(r'\.(patch|conf)$',p):
                        allowed=d228_overlay_paths(r)
                        need(p in allowed,'lane changed protected suffix outside the two validated D228 inputs')
                        need(r.tree(c,p)=={p:allowed[p]},'D228 overlay mode/blob differs at changed commit')
                    if s=='product-paths':need((p=='.github/sessions/archived/saved-session-state-feature-m6-patches-shipped-kernel-688-20261102T052600Z.md' and r.tree(c,p)==r.tree(STAGE_A,p)) or p.startswith(r.af+'/') or bool(re.match(r'^(docs/retros/[^/]*-m6-patches-shipped-kernel\.md$|\.github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688\.md$|docs/work-logs/|docs/(decision-register|blindspot-register|friction-log)\.md$)',p)),'outside lane records scope: '+fmt(p))
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
        need(not re.search(r'^[ \t*`-]*(?:reviewed-at-es|fixed-at-es)[*`]*[ \t]*:',t,re.M),'ES header present')
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
        gate=section_text(t,'Phase 7 resolution gate')
        items=set(re.findall(r'^## (PL-[0-9]+)\b',t,re.M));need(bool(items),'punch item headings absent')
        rows=[x for x in gate.splitlines() if re.match(r'^\|\s*PL-[0-9]+\s*\|',x)]
        seen=[]
        for row in rows:
            cells=[x.strip().strip('*') for x in row.strip().strip('|').split('|')]
            need(len(cells)>=3 and cells[1] in ['Resolved','Deferred','Withdrawn'],'unresolved punch outcome')
            need(bool(re.search(r'#[0-9]+|`[0-9a-f]{7,40}`',' | '.join(cells[2:]))),'punch outcome lacks evidence/follow-up')
            seen.append(cells[0])
        need(len(seen)==len(set(seen)) and set(seen)==items,'punch outcomes missing/duplicate')
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
        for x in ['nothing','T42','T43','T27','T11','integration']:need(x.lower() in t.lower(),'retro obligation absent: '+x);
        return 'final retro exists with owner/time-to-play text'
    if s=='question-comments':
        t=r.text('04-analysis.md');cs=r.issues(688,True);found=[]
        for c in cs:
            b=c['body'].lower()
            if '?' in b and (('symlink' in b and '7.0' in b) or ('ramoops' in b and 'mainline' in b)):found.append(c)
        if len(found)<2:raise Absent('two Stage-D question comments absent')
        t2=r.text('02-forward-audit.md');need(all(str(c['id']) in t2 for c in found[-2:]),'question readback IDs absent');return 'two question comments/IDs read back'
    # Pins quotation authority: 239808e3724ba9ead52fd92d5d5e0c517f0cedf1, #688 comment6587194285.
    if s=='pins-read':
        rows=r.rows();need(len(rows)==107,'pin table row count')
        for x in rows:
            need(re.search(r'(?<![\d.])(7\.2|7\.1\.2|v2026\.01|20260309)(?![\d.])',x['pin']),'invalid current pin')
            for match in re.findall(r'(?<![\d.])(?:v?\d+(?:\.\d+)+|20260309)(?![\d.])',x['pin']):need(match in ['7.2','7.1.2','v2026.01','20260309'],'unexpected pin value')
        t=r.text('02-forward-audit.md');path='projects/ROCKNIX/packages/linux/package.mk'
        recipe=unchanged(r,path,SOURCE).decode();numbered=dict(enumerate(recipe.splitlines(),1))
        versions=[n for n,line in numbered.items() if re.match(r'^\s*PKG_VERSION=',line)]
        dirs=[n for n,line in numbered.items() if re.match(r'^\s*PKG_PATCH_DIRS\+?=',line)]
        conditional=[n for n,line in numbered.items() if 'PKG_PATCH_DIRS' in line and re.match(r'^\[\[ .* \]\] && PKG_PATCH_DIRS\+=',line)]
        need(versions==[23,30,37,43,49] and dirs==[16,27,40,46] and conditional==[18],'whole recipe assignment identity differs from the coordinator five/four/one contract')
        case_end=next((n for n,line in numbered.items() if line=='esac'),None)
        labels=[n for n,line in numbered.items() if case_end and n<case_end and re.fullmatch(r'  [A-Z0-9_|]+\)',line)]
        need(labels==[22,29,36,42,48],'five kernel case-label context lines differ')
        need(SOURCE in t and path in t,'02 must name exact recipe source ref and path')
        required=sorted(versions+dirs+conditional+labels)
        for n in required:
            # git grep -n (colon) and nl -ba (tab) are both numbered literal
            # source quotations. Preserve every source character after the delimiter.
            need(bool(re.search(r'^[ \t]*'+str(n)+r'[:\t]'+re.escape(numbered[n])+r'$',t,re.M)),'02 missing or changed literal numbered recipe quotation at line '+str(n))
        return 'four selected provenance pins; unchanged whole recipe and exact source ref; all ten numbered assignments and five case labels quoted'
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
        starts=list(re.finditer(r'^'+re.escape(a)+r'$',brief,re.M));ends=list(re.finditer(r'^'+re.escape(b)+r'$',brief,re.M))
        need(len(starts)==len(ends)==1 and starts[0].end()<ends[0].start(),'membership brief standalone marker shape')
        chunk=brief[starts[0].end():ends[0].start()]
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
    for p,entry in tree.items():
        need(entry.split()[0] in ['100644','100755'] and entry.split()[1]=='blob' and not p.endswith('.held.json') and '/held/' not in p,'unsafe historical T4 fixture input')
        r.blob(p,T4)  # input was git archive at T4, never the mutable final T4 copy
    plan=json.loads(r.blob(T4_FOLDER+'/second-opinions/review-plan.json',T4))
    need(plan.get('depth')=='local' and plan.get('tier_exception')=='D-WORKFLOW-184' and plan.get('reviewers')==[],'historical Local fixture has wrong plan')
    positive=frozen_receipt(r,'stage-a/lint-local-pass.out',STAGE_A).decode()
    negative=frozen_receipt(r,'stage-a/lint-local-fail.out',STAGE_A).decode()
    raw=frozen_receipt(r,'stage-a/run/stage-a.out',STAGE_A).decode()
    need(positive.rstrip().endswith('\nPASS'),'historical Local positive lacks PASS')
    need('FAIL  second-opinions/review-plan.json or its call evidence is invalid: local-only cannot satisfy Epic/Milestone' in negative and negative.rstrip().endswith('1 CONTRACT FAILURE(S)'),'historical Local refusal differs')
    for t in ['t4 plan: local D-WORKFLOW-184 0','lint, a Local plan, rc=0','lint, tier_exception removed, rc=1']:need(t in raw,'historical Local exit/fixture receipt absent')
    return 'D226: unchanged lint plus exact immutable T4 historical fixture, tier_exception deletion command, positive/refusal and rc receipts reconciled; no replay'

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
    return supplemental_generator(r,validation)

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
TOOL_AUTHOR={'harness':'Codex','model':'GPT-6','agent':'/root','pane':'wN:p5','session':'01a19d12-1c5f-7022-8053-102f6a94b7fe'}
ROOT_EXECUTOR={'harness':'Codex','model':'GPT-6-Astra','effort':'xhigh','session':'01a19d11-f5c8-7bb0-80f3-49ad28732af2','pane':'wN:p2','identity_source':'observed footer'}
DAY_LOG='docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md'
LOG_INDEX='docs/work-logs/INDEX.md'
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
        raw=os.environ.get('ACCEPT_EXECUTOR_JSON')
        if not raw:raise Cannot('mandatory actual executor identity missing: ACCEPT_EXECUTOR_JSON')
        self.executor=proof_json(raw)
        need(isinstance(self.executor,dict) and set(self.executor)==set(ROOT_EXECUTOR) and all(isinstance(v,str) and v.strip() for v in self.executor.values()),'executor metadata shape differs')
        need(bool(re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}',self.executor['session'])) and bool(re.fullmatch(r'wN:p[0-9]+',self.executor['pane'])),'executor session/pane invalid')
        # Fixture processes must identify their actual author, not impersonate root.
        if not r.fixture:need(self.executor==ROOT_EXECUTOR,'final executor differs from the observed coordinator identity')
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
              'submodule.recurse':'false','core.quotePath':'true','core.whitespace':'blank-at-eol,blank-at-eof,space-before-tab'}
        self.env['GIT_CONFIG_COUNT']=str(len(opts))
        for i,(k,v) in enumerate(opts.items()):self.env['GIT_CONFIG_KEY_'+str(i)]=k;self.env['GIT_CONFIG_VALUE_'+str(i)]=v
    def command(self,label,argv,cwd=None,data=None,expect=(0,),last=None,env=None,timeout=120,raw_public=False):
        """Persist masked stdout/stderr plus hashes of actual bytes, argv/input/exit/time.
        Missing executable/timeouts => CANNOT; a completed wrong rc/output => FAIL.
        Never invoke a shell except the literal secret-patterns interface above.
        """
        need(type(timeout) in [int,float] and 0<timeout<=1200,'command timeout must be bounded at most 1200 seconds')
        if raw_public:need(argv[:3]==['git','diff','--check'],'raw evidence restricted to public Git whitespace diagnostics')
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
        record={'schema':2,'tool_author':dict(TOOL_AUTHOR),'executor':dict(self.executor),'label':label,'argv':argv,'cwd':str(cwd),
            'timeout_seconds':timeout,'start':started,'elapsed_seconds':round(time.monotonic()-start,6),'rc':rc,'timed_out':timed,'problem':problem,
            'stdin_sha256':None if data is None else sha(data),'stdin_bytes':0 if data is None else len(data),
            'stdout_sha256':sha(out),'stderr_sha256':sha(err),'stdout':stem+'.stdout','stderr':stem+'.stderr',
            'stdout_masked_sha256':sha(mask_log(out)),'stderr_masked_sha256':sha(mask_log(err)),
            'lane_tip':self.r.tip,'coordinator_tip':self.r.coord,'fixture':bool(self.r.fixture)}
        if raw_public:
            for kind,b in [('stdout',out),('stderr',err)]:
                filename=stem+'.raw.'+kind;record['raw_'+kind]=filename
                with private_path(self.root/filename).open('xb') as f:f.write(b)
        for suffix,content in [('stdout',mask_log(out)),('stderr',mask_log(err)),('json',(json.dumps(record,indent=2)+'\n').encode())]:
            path=private_path(self.root/(stem+'.'+suffix))
            with path.open('xb') as f:f.write(content)
        if raw_public:need(not err,'public Git whitespace diagnostics included unexpected stderr')
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
            self.integration_whitespace(dest,cached=False)
            _,rc=self.command('integration-merge',['git','-c','merge.autoStash=false','merge','--no-edit','--no-commit','--no-ff',r.tip],dest,expect=(0,1))
            if rc:self.merge_worklogs(dest)
            unmerged,_=self.command('integration-unmerged',['git','ls-files','-u'],dest)
            need(not unmerged,'integration contains unresolved entries')
            self.integration_whitespace(dest,cached=True)
        self.validate_clone_paths(dest)
        self.clones[key]=dest
        return dest

    def merge_worklogs(self,dest):
        """Resolve only whole appended entries, using immutable base and both tips.
        Never use conflict-marker text or a general ours/theirs strategy.
        """
        raw,_=self.command('append-unmerged',['git','ls-files','-u','-z'],dest)
        conflicts={x.split(b'\t',1)[1].decode() for x in raw.split(b'\0') if x}
        need(conflicts and conflicts<={DAY_LOG,LOG_INDEX},'integration conflict outside exact daily log/generated index')
        raw,_=self.command('append-base',['git','merge-base','--all',self.r.coord,self.r.tip],dest)
        bases=raw.decode().splitlines();need(len(bases)==1 and re.fullmatch('[0-9a-f]{40}',bases[0]),'append merge requires one exact merge-base')
        base=bases[0];bodies=[];identities=[]
        for label,ref in [('base',base),('coordinator',self.r.coord),('lane',self.r.tip)]:
            entry,_=self.command('append-'+label+'-identity',['git','ls-tree','-z',ref,'--',DAY_LOG],dest)
            rows=[x for x in entry.split(b'\0') if x]
            need(len(rows)==1 and rows[0].split(b'\t')[0].split()[:2]==[b'100644',b'blob'],'append log must exist as a regular 100644 file at base and both tips')
            b,_=self.command('append-'+label+'-bytes',['git','show',ref+':'+DAY_LOG],dest)
            bodies.append(b);identities.append(dict(ref=ref,entry=entry.decode(),sha256=sha(b)))
        merged,sequences=merge_append_bytes(*bodies)
        # Index conflicts are generated state, but every tip still needs a regular
        # index. Rebuild it after the immutable daily entries have been united.
        for ref in [base,self.r.coord,self.r.tip]:
            entry,_=self.command('append-index-identity',['git','ls-tree','-z',ref,'--',LOG_INDEX],dest)
            need(entry.split(b'\t')[0].split()[:2]==[b'100644',b'blob'],'append index is absent/nonregular')
        before,_=self.command('append-before-status',['git','status','--porcelain=v1','-z','--untracked-files=all'],dest)
        # Write only these two exact paths below this private simulation clone.
        day=private_path(dest/DAY_LOG);need(day.is_file() and not day.is_symlink(),'unsafe daily log destination')
        index=private_path(dest/LOG_INDEX);need(index.is_file() and not index.is_symlink(),'unsafe index destination')
        day.write_bytes(merged)
        # Bind the expected index to the tool's actual print interface before write.
        rendered,_=self.command('append-index-render',['tools/work-log-index'],dest)
        self.command('append-index-write',['tools/work-log-index','--write'],dest)
        need(day.read_bytes()==merged,'index tool changed whole daily append entries')
        need(index.read_bytes()==rendered,'index --write differs from its exact render')
        self.command('append-index-check',['tools/work-log-index','--check'],dest)
        after,_=self.command('append-after-status',['git','status','--porcelain=v1','-z','--untracked-files=all'],dest)
        # Guard file contents too, not just status membership: the reviewed index
        # tool has only this one output; a fixture trying any other write fails.
        def status_except(raw):return [x for x in raw.split(b'\0') if x and x[3:].decode() not in [DAY_LOG,LOG_INDEX]]
        need(status_except(before)==status_except(after),'index generation changed other path status')
        unstaged,_=self.command('append-other-unstaged',['git','diff','--name-only','-z','--','.',':(exclude,literal)'+DAY_LOG,':(exclude,literal)'+LOG_INDEX],dest)
        need(not unstaged,'index generation changed another tracked file')
        self.command('append-add',['git','add','--',DAY_LOG,LOG_INDEX],dest)
        unmerged,_=self.command('append-resolved',['git','ls-files','-u'],dest);need(not unmerged,'append merge left conflicts')
        staged,_=self.command('append-staged-bytes',['git','show',':'+DAY_LOG],dest)
        need(staged==merged,'staged append bytes differ')
        receipt=dict(schema=1,tool_author=TOOL_AUTHOR,executor=self.executor,base_and_tips=identities,
            path=DAY_LOG,merged_sha256=sha(merged),entry_sequences=sequences,index_sha256=sha(rendered),result='PASS')
        with private_path(self.root/'append-merge.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')

    def integration_whitespace(self,dest,cached=False):
        """Six exact public records only. Preserve full original rc/diagnostics,
        then require rc0 for every remaining path; never normalize evidence.
        """
        r=self.r;allowed=d228_overlay_paths(r)
        need(len(allowed)==2,'integration requires the exact current and retained D228 header inputs')
        for tail in ['01-research-notes.md','stage-a/order.out','stage-a/run/stage-a-extra.out','stage-a/run/stage-a.out']:
            path=r.af+'/'+tail;expected=r.tree(STAGE_D,path)
            need(bool(expected) and expected==r.tree(r.tip,path),'whitespace accepted record changed: '+path)
            allowed=dict(allowed,**expected)
        need(len(allowed)==6,'whitespace exception census differs')
        identities=[]
        for path,entry in sorted(allowed.items()):
            need(r.tree(r.tip,path)=={path:entry},'whitespace input mode/blob differs')
            identities.append(dict(path=path,mode_blob=entry,sha256=sha(r.blob(path))))
            if cached:
                raw,_=self.command('whitespace-index-identity',['git','ls-files','--stage','-z','--',path],dest)
                rows=[x.split(b'\t',1)[0].split() for x in raw.split(b'\0') if x]
                parts=entry.split();need(rows==[[parts[0].encode(),parts[2].encode(),b'0']],'integrated whitespace record differs from validated input')
        mode='cached' if cached else 'tips'
        base=['git','diff','--check','--no-ext-diff','--no-textconv']+(['--cached'] if cached else [r.coord,r.tip])
        full,rc=self.command('whitespace-'+mode+'-full',base,dest,expect=(0,2),raw_public=True)
        diagnostics={m.group(1) for m in re.finditer(r'^([^+\n][^\n]*?):[0-9]+: (?:trailing whitespace|space before tab|new blank line at EOF)\.',full.decode(),re.M)}
        need((rc==0 and full==b'') or (rc==2 and diagnostics and diagnostics<=set(allowed)),'whitespace diagnostics outside exact preserved inputs')
        if not cached:need(rc==2 and diagnostics==set(allowed),'immutable T41 whitespace diagnostic census differs from the measured six paths')
        rest=base+['--','.',*[':(exclude,literal)'+path for path in sorted(allowed)]]
        self.command('whitespace-'+mode+'-remaining',rest,dest,raw_public=True)
        receipt=dict(schema=1,tool_author=TOOL_AUTHOR,executor=self.executor,tip=r.tip,coordinator=r.coord,
            cached=cached,rc=rc,stdout_sha256=sha(full),excluded=identities,diagnostic_paths=sorted(diagnostics),remaining_rc=0)
        with private_path(self.root/('whitespace-'+mode+'.json')).open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')

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
        if whole:self.command(prefix+'-forbidden-tree',['tools/forbidden-terms-check'],dest,timeout=1200)
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


def merge_append_bytes(base,coordinator,lane):
    need(base.endswith(b'\n'),'append base must end at a line boundary')
    # Timestamp syntax is validated without normalizing any header/body byte.
    # Existing time-only, full-date UTC and ISO UTC forms are all published in
    # this exact daily log. Calendar/time ranges are checked separately below.
    stamp=(rb'(?:[0-9]{2}:[0-9]{2} UTC|'
           rb'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} UTC|'
           rb'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|\+00:00))')
    heading=rb'^## (?P<stamp>'+stamp+rb') (?:--|\xe2\x80\x94|\xe2\x80\x93|-)+ .+\n'
    def valid_stamp(raw):
        text=raw.decode('ascii')
        try:
            if re.fullmatch(r'[0-9]{2}:[0-9]{2} UTC',text):
                datetime.datetime.strptime(text,'%H:%M UTC')
            elif text.endswith(' UTC'):
                datetime.datetime.strptime(text,'%Y-%m-%d %H:%M:%S UTC')
            else:
                value=datetime.datetime.fromisoformat(text.replace('Z','+00:00'))
                need(value.utcoffset()==datetime.timedelta(0),'append timestamp is not UTC')
        except ValueError:raise Invalid('append timestamp has an invalid calendar date or UTC time')
    def parse(raw):
        if not raw:return []
        starts=[m.start() for m in re.finditer(rb'^## ',raw,re.M)]
        need(starts and raw[:starts[0]] and not raw[:starts[0]].strip(b'\n') and raw.endswith(b'\n') and not raw.endswith(b'\n\n'),'append suffix lacks whole entries or exact terminal newline')
        boundaries=[0]
        for i in starts[1:]:
            j=i
            while j>0 and raw[j-1:j]==b'\n':j-=1
            need(i-j>=2,'appended entries lack blank-line separation')
            boundaries.append(j+1)  # retain one newline on the preceding body
        blocks=[raw[a:b] for a,b in zip(boundaries,boundaries[1:]+[len(raw)])]
        for block in blocks:
            body=block.lstrip(b'\n');m=re.match(heading,body)
            need(len(block)>len(body) and m is not None and block.endswith(b'\n') and body[len(m.group(0)):].strip(),'append entry heading/body/boundary invalid')
            valid_stamp(m.group('stamp'))
        return blocks
    base_headings={x for x in base.splitlines() if x.startswith(b'## ')}
    allblocks={};seqs=[]
    for tip in [coordinator,lane]:
        need(tip.startswith(base),'work-log changed pre-existing bytes instead of whole append')
        blocks=parse(tip[len(base):]);keys=[]
        for b in blocks:
            key=b.lstrip(b'\n').splitlines()[0];need(key not in base_headings and key not in keys,'duplicate append/base heading')
            need(key not in allblocks or allblocks[key]==b,'same append heading has conflicting entry bytes')
            allblocks[key]=b;keys.append(key)
        seqs.append(keys)
    edges={k:set() for k in allblocks};degree={k:0 for k in allblocks}
    for seq in seqs:
        for a,b in zip(seq,seq[1:]):
            if b not in edges[a]:edges[a].add(b);degree[b]+=1
    ordered=[]
    while degree:
        ready=sorted(k for k,v in degree.items() if v==0);need(ready,'append entry orders conflict')
        k=ready[0];ordered.append(k);degree.pop(k)
        for b in edges[k]:degree[b]-=1
    for seq in seqs:need([k for k in ordered if k in seq]==seq,'append sequence not preserved')
    merged=base+b''.join(allblocks[k] for k in ordered)
    need(parse(merged[len(base):])==[allblocks[k] for k in ordered],'whole append bytes lost')
    return merged,[[sha(allblocks[k]) for k in seq] for seq in seqs]

"""D228 supplemental-proof consumer. Git/record reads only; never invoke a producer.
Codex (GPT-6), /root, wN:p5, session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
Historical negative inputs remain unavailable; new controls cannot identify them.
"""
import copy, datetime as DT, math, base64
PROOF_AUTH='10e055e3043b7bd41f9dcca3e04abce9d979817e'
PROOF_SCHEMA='t41-final-generator-controls-v1'
PROOF_PROGRAM_SHA='ac6fe1ea48775d0c4c3b285b9b6811c1d12a83ed4ca2414d466ab6490989e558'
STAGE_D='c9fe606e8d7e7e0f6c70cc686764d1503029d278'
PROOF_ROOT='stage-f/generator-input-proof'

def proof_relative(value):
    need(isinstance(value,str),'D228 artifact path must be text')
    p=dec(value);q=P.PurePosixPath(p)
    need(p and '\x00' not in p and '\\' not in p and not q.is_absolute() and '..' not in q.parts and str(q)==p and p!='.','D228 unsafe relative artifact path')
    return p

def proof_json(raw):
    def pairs(items):
        obj={}
        for k,v in items:
            need(k not in obj,'D228 duplicate JSON key');obj[k]=v
        return obj
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _: (_ for _ in ()).throw(Invalid('D228 nonfinite JSON number')))

def proof_utc(value):
    need(isinstance(value,str) and bool(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|\+00:00)',value)),'D228 timestamp must be explicit UTC')
    return DT.datetime.fromisoformat(value.replace('Z','+00:00'))

def supplemental_generator(r,historical,retained=True):
    """Only this supplement may close the failed historical input-binding predicate."""
    root=r.af+'/'+PROOF_ROOT
    # Manifest absence is an honest future-artifact ABSENT. After it exists, a
    # missing fixture/output is a malformed proof and FAIL, never a partial PASS.
    try:raw_manifest=r.audit(PROOF_ROOT+'/manifest.json')
    except Absent:raise Absent('D228 supplemental manifest absent; historical negative input identities remain unavailable')
    manifest=proof_json(raw_manifest);need(isinstance(manifest,dict),'D228 manifest must be an object')
    need(manifest['schema']==PROOF_SCHEMA and manifest['authority']=='D-WORKFLOW-228','D228 schema/authority differs')
    need(manifest['historical_input_identity']=='unavailable; new controls only','D228 must preserve the historical unknown')
    need(manifest['source_ref']==SOURCE and manifest['stage_c_ref']==STAGE_C,'D228 source/Stage-C ref differs')
    need(manifest['result']=='PASS','D228 producer did not assert a completed PASS')
    run_head=manifest['run_head'];need(isinstance(run_head,str) and re.fullmatch('[0-9a-f]{40}',run_head),'D228 run_head must be a full commit')
    need(r.git('cat-file','-t',run_head).strip()==b'commit','D228 run_head is not a commit')
    need(r.git('merge-base','--is-ancestor',run_head,r.tip,missing=True) is not None,'D228 run_head is not an ancestor of candidate')
    listing=r.tree(r.tip,root+'/')
    need(root+'/manifest.json' in listing,'D228 manifest is not committed at candidate tip')
    for path,entry in listing.items():
        proof_relative(path[len(root)+1:]);need(entry.split()[0] in ['100644','100755'] and entry.split()[1]=='blob','D228 proof contains a symlink or nonregular artifact')
    def read(path):
        path=proof_relative(path);full=root+'/'+path
        need(full in listing,'D228 missing committed proof artifact: '+fmt(path))
        try:b=r.blob(full)
        except Absent:raise Invalid('D228 missing proof artifact: '+fmt(path))
        return b
    need(read('manifest.json')==raw_manifest,'D228 manifest read differs from committed bytes')
    # The new packet supplements the immutable historical packet, never edits it.
    for stage in ['stage-a','stage-b','stage-c','stage-d']:
        p=r.af+'/'+stage+'/'
        expected=r.tree(STAGE_D,p)
        need(bool(expected) and r.tree(r.tip,p)==expected,'D228 accepted '+stage+' modes/blobs changed or absent')
    program=manifest['program'];rows_record=manifest['baseline_rows']
    need(proof_relative(program['path'])=='tools/t41-tables.py','D228 program path differs')
    need(proof_relative(rows_record['path'])=='stage-b/corrected/inventory-rows.json','D228 baseline rows path differs')
    program_path=r.af+'/'+proof_relative(program['path']);rows_path=r.af+'/'+proof_relative(rows_record['path'])
    pb=unchanged(r,program_path,STAGE_C);rb=unchanged(r,rows_path,STAGE_C)
    need(program['sha256']==PROOF_PROGRAM_SHA==sha(pb),'D228 exact accepted formal program hash differs')
    need(rows_record['sha256']==sha(rb),'D228 baseline rows hash differs')
    for path in [program_path,rows_path]:
        need(r.tree(run_head,path)==r.tree(r.tip,path),'D228 program/baseline differs at recorded run_head')
    base=proof_json(rb);need(isinstance(base,list) and len(base)==107,'D228 baseline is not 107 rows')
    selected=[proof_relative(x['path']) for x in base]
    need(len(set(selected))==107,'D228 duplicate selected source path')
    need(set(selected)=={dec(x['path']) for x in r.inventory()},'D228 baseline membership differs')
    source_tree=r.tree(SOURCE,'');final_tree=r.tree(r.tip,'');run_tree=r.tree(run_head,'')
    for p in selected:
        need(p in source_tree and source_tree[p].split()[0] in ['100644','100755'] and source_tree[p].split()[1]=='blob','D228 selected source is not a regular blob')
        need(source_tree[p]==final_tree.get(p)==run_tree.get(p),'D228 selected source mode/blob drift: '+fmt(p))
    # Lexicographic selection and the first-60-lines rule are computed from immutable
    # bytes. No filesystem source tree and no historical negative bytes are read.
    eligible=[]
    for p in sorted(selected):
        if not p.endswith('.patch'):continue
        data=r.blob(p,SOURCE);parts=data.splitlines(keepends=True)
        indices=[i for i,line in enumerate(parts[:60]) if line.startswith(b'From: ')]
        if indices:eligible.append((p,data,parts,indices[0]))
    need(bool(eligible),'D228 no eligible header source')
    hp,hb,parts,first=eligible[0];changed=list(parts);changed[first]=b'X-Proof-From: '+changed[first][len(b'From: '):]
    expected_header=b''.join(changed)
    mutations={'drop':base[:-1],'reach':copy.deepcopy(base)}
    shipped=next((i for i,x in enumerate(base) if x.get('reach')=='shipped'),None)
    need(shipped is not None,'D228 baseline has no shipped row');mutations['reach'][shipped]['reach']='test'
    records=manifest['inputs'];need(isinstance(records,list) and len(records)==3 and all(isinstance(x,dict) for x in records),'D228 requires exactly three inputs')
    need([x.get('kind') for x in records].count('drop')==1 and {x.get('kind') for x in records}=={'drop','reach','header'},'D228 input kinds duplicated or missing')
    inputs={x['kind']:x for x in records};input_paths={}
    for kind,expected_path in [('drop','fixtures/drop.json'),('reach','fixtures/reach.json'),('header','fixtures/bytes/'+hp)]:
        entry=inputs[kind];path=proof_relative(entry['path']);need(path==expected_path,'D228 wrong '+kind+' input path')
        data=read(path);input_paths[kind]=path
        need(entry['mode']=='100644' and listing[root+'/'+path].split()[0]=='100644' and type(entry['size_bytes']) is int and entry['size_bytes']==len(data),'D228 input mode/size differs')
        need(isinstance(entry['sha256'],str) and entry['sha256']==sha(data),'D228 input hash differs')
        if kind in mutations:
            # JSON Unicode escapes are syntax; only the known filename escape is
            # normalized semantically. Every non-path field and row order is exact.
            actual=proof_json(data);wanted=copy.deepcopy(mutations[kind])
            need(isinstance(actual,list) and all(isinstance(x,dict) for x in actual),'D228 mutated rows must be objects')
            for rows in [actual,wanted]:
                for row in rows:row['path']=proof_relative(row['path'])
            need(json.dumps(actual,sort_keys=True,ensure_ascii=False)==json.dumps(wanted,sort_keys=True,ensure_ascii=False),'D228 deterministic '+kind+' mutation differs')
        else:
            need(proof_relative(entry['source_path'])==hp,'D228 header selected a different source')
            need(entry['source_path']==hp,'D228 header source_path must be decoded')
            need(entry['baseline_blob_id']==source_tree[hp].split()[2] and re.fullmatch('[0-9a-f]{40}',entry['baseline_blob_id']),'D228 header baseline blob id differs')
            need(entry['baseline_sha256']==sha(hb),'D228 header baseline hash differs')
            need(data==expected_header,'D228 header mutation changed more than the first From prefix')
    fixture_files={p[len(root)+1:] for p in listing if p.startswith(root+'/fixtures/')}
    need(fixture_files==set(input_paths.values()),'D228 missing or extra fixture/overlay file')
    overlay={p for p in fixture_files if p.startswith('fixtures/bytes/')}
    need(overlay=={'fixtures/bytes/'+hp},'D228 overlay is not exactly the selected one regular file')
    checks=manifest['checks'];need(isinstance(checks,list) and all(isinstance(x,dict) for x in checks) and [x.get('kind') for x in checks]==['drop','reach','header','stats'],'D228 requires ordered drop/reach/header/stats commands only')
    assertions={'drop':'AssertionError: membership: expected 107 rows','reach':'AssertionError: reach: expected shipped 103/test 4','header':'AssertionError: From header census: expected 87'}
    outputs=[];previous=None;cwd_seen=None
    historical_end=max(proof_utc(x['start']) for x in historical['checks'] if x.get('name','').startswith('formal-generator-'))
    for x in checks:
        kind=x['kind'];argv=x['argv'];cwd=x['cwd']
        need(isinstance(cwd,str) and P.PurePosixPath(cwd).is_absolute() and str(P.PurePosixPath(cwd))==cwd and '..' not in P.PurePosixPath(cwd).parts and '\\' not in cwd and '\x00' not in cwd,'D228 unsafe command cwd')
        if cwd_seen is None:cwd_seen=cwd
        need(cwd==cwd_seen,'D228 commands changed cwd')
        def arg_path(a,expected):
            need(isinstance(a,str),'D228 command path must be text')
            a=dec(a);need(a in [expected,cwd.rstrip('/')+'/'+expected],'D228 command does not address the bound artifact')
        need(isinstance(argv,list) and len(argv)==(4 if kind=='stats' else 6) and argv[:2]==['python3','-I'] and argv[3]=='stats','D228 command shape differs')
        arg_path(argv[2],program_path)
        if kind!='stats':
            need(argv[4]==('--bytes-from' if kind=='header' else '--rows-from'),'D228 wrong negative input flag')
            arg_path(argv[5],root+'/'+('fixtures/bytes' if kind=='header' else input_paths[kind]))
        start,end=proof_utc(x['start']),proof_utc(x['end']);elapsed=x['elapsed_seconds']
        need(start>historical_end and end>=start and (previous is None or start>=previous),'D228 controls not dated as new ordered checks')
        need(type(elapsed) in [float,int] and math.isfinite(elapsed) and elapsed>=0,'D228 elapsed time invalid');previous=end
        out_path,err_path=proof_relative(x['stdout']),proof_relative(x['stderr']);outputs += [out_path,err_path]
        out,err=read(out_path),read(err_path)
        need(x['stdout_sha256']==sha(out) and x['stderr_sha256']==sha(err),'D228 raw output hash differs')
        need(type(x['rc']) is int and x['rc']==(0 if kind=='stats' else 1),'D228 command rc differs')
        if kind=='stats':need(err==b'' and out==r.audit('stage-c/tables/stats.txt'),'D228 positive is not exact Stage-C stats/empty stderr')
        else:
            # An uncaught Python AssertionError is the final stderr line. Treat a
            # stdout claim alone as insufficient; it could be printed by any code.
            need(err.decode().splitlines()[-1:]==[assertions[kind]],'D228 negative final assertion differs')
    need(len(set(outputs))==8 and not (set(outputs)&set(input_paths.values())),'D228 output paths reused or alias an input')
    need(not set(outputs)&{'manifest.json','run.py','README','README.md'},'D228 output aliases metadata/builder')
    builder=read('run.py');readmes=[p for p in ['README','README.md'] if root+'/'+p in listing]
    need(len(readmes)==1,'D228 exactly one README required');readme=dec(read(readmes[0]).decode())
    need(sha(builder) in readme,'D228 README does not bind exact builder SHA')
    need(all(p in readme for p in list(input_paths.values())+outputs+['run.py','manifest.json']),'D228 README input/output file list incomplete')
    need(any(t in readme for t in ['python3','sha256sum','git ']),'D228 README validation commands absent')
    allowed={root+'/'+input_paths['header']:listing[root+'/'+input_paths['header']]}
    if retained:allowed.update(retained_generator_attempt(r,historical,manifest,listing))
    r.d228_headers=allowed
    return 'D226 historical Stage-C program/outputs reconciled; original negative inputs remain unavailable. D228 new sealed drop/reach/header refusals plus stats positive verified; no producer invoked'


def retained_generator_attempt(r,historical,current,current_listing):
    """Losslessly reconstruct only the TWO committed base64 input streams in memory.
    Reuse every supplemental predicate on a virtual view of the first attempt.
    No scratch path in its error record is ever accessed, and no builder executes.
    """
    canonical=r.af+'/'+PROOF_ROOT;attempt=canonical+'-attempt-1'
    listing=r.tree(r.tip,attempt+'/')
    if not listing:return {}
    def read(p):
        full=attempt+'/'+proof_relative(p)
        need(full in listing and listing[full].split()[:2]==['100644','blob'],'D228 retained artifact absent/nonregular: '+fmt(p))
        return r.blob(full)
    old=proof_json(read('manifest.json'));error=proof_json(read('serialization-error.json'))
    need(error['result']=='generator controls passed; publication hygiene failed','D228 retained failure disposition differs')
    when=proof_utc(error['timestamp'])
    need(proof_utc(old['checks'][-1]['end'])<when<proof_utc(current['checks'][0]['start']),'D228 retained failure/correction time order differs')
    for key in ['schema','authority','historical_input_identity','source_ref','stage_c_ref','run_head','program','baseline_rows','result']:
        need(old[key]==current[key],'D228 retained attempt identity differs: '+key)
    old_inputs={x['kind']:x for x in old['inputs']};new_inputs={x['kind']:x for x in current['inputs']}
    need(old_inputs['header']==new_inputs['header'],'D228 retained header source/identity differs')
    hp=proof_relative(new_inputs['header']['path'])
    need(read(hp)==r.blob(canonical+'/'+hp),'D228 retained header bytes differ')
    identities=read('source-identities.json')
    need(identities==r.blob(canonical+'/source-identities.json'),'D228 retained source identities differ')
    expected=[];source_entries=r.tree(SOURCE,'')
    for path in sorted(dec(x['path']) for x in r.inventory()):
        entry=source_entries[path].split();expected.append(dict(path=path,mode=entry[0],blob_id=entry[2]))
    need(proof_json(identities)==expected,'D228 retained source identity census differs')
    encoded=error['encoded_original_files']
    need(isinstance(encoded,list) and len(encoded)==2 and [x['original_path'] for x in encoded]==['fixtures/drop.json','fixtures/reach.json'],'D228 retained encoding manifest differs')
    virtual={}
    for x,kind in zip(encoded,['drop','reach']):
        path=x['original_path'];stored=path+'.base64'
        need(x['stored_path']==stored and x['encoding']=='base64; exact original bytes, not a rewritten input','D228 retained encoding path/type differs')
        raw=read(stored)
        try:decoded=base64.b64decode(b''.join(raw.split()),validate=True)
        except ValueError:raise Invalid('D228 retained input invalid base64')
        entry=old_inputs[kind]
        need(entry['path']==path and type(x['size_bytes']) is int and x['size_bytes']==len(decoded)==entry['size_bytes'] and x['sha256']==sha(decoded)==entry['sha256'],'D228 retained input identity differs')
        # Only the known filename serialization is different; no semantic rewrite.
        newer=r.blob(canonical+'/'+path)
        need(newer.replace(b'\\u002d',b'-')==decoded,'D228 retained input is not the exact serialization-only predecessor')
        virtual[canonical+'/'+path]=decoded
    before=read('run.py');after=r.blob(canonical+'/run.py')
    old_line=br"        rec=emit('fixtures/'+kind+'.json',(json.dumps(obj,indent=2)+'\n').encode())"
    new_line=b"        rec=emit('fixtures/'+kind+'.json',dump(obj).encode())"
    need(before.count(old_line)==1 and before.replace(old_line,new_line)==after,'D228 retained builder change is not the exact serialization correction')
    class AttemptView:
        def __init__(self):self.tip=r.tip;self.af=r.af
        def __getattr__(self,name):return getattr(r,name)
        def blob(self,path,ref=None):
            if (ref is None or ref==r.tip) and path.startswith(canonical+'/'):
                if path in virtual:return virtual[path]
                return read(path[len(canonical)+1:])
            return r.blob(path,ref)
        def audit(self,path):return self.blob(self.af+'/'+path)
        def tree(self,ref,path):
            if ref==r.tip and path.startswith(canonical+'/'):
                out={}
                for p,entry in listing.items():
                    q=canonical+p[len(attempt):]
                    if q.endswith('.json.base64'):q=q[:-7]
                    if q in virtual:
                        b=virtual[q];entry='100644 blob '+hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
                    if q==path or q.startswith(path.rstrip('/')+'/'):out[q]=entry
                return out
            return r.tree(ref,path)
    supplemental_generator(AttemptView(),historical,retained=False)
    return {attempt+'/'+hp:listing[attempt+'/'+hp]}


def d228_overlay_paths(r):
    if not hasattr(r,'d228_headers'):reconcile_generator(r)
    return r.d228_headers

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
