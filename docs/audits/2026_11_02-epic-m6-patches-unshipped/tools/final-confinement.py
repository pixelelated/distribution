#!/usr/bin/env python3
"""New final confinement and immutable-identity reader; executes no old producer."""
import hashlib,json,os,pathlib,stat,subprocess,sys
R='docs/audits/2026_11_02-epic-m6-patches-unshipped/'
D='676115271e9bbaa9e8db81f6de73a7b49094c5b4';SEED='601e4694f9726b2228d3571efdb5cfc061c6d442'
NARR={R+x for x in ['00-running-log.md','04-analysis.md','05-punch-list.md','06-audit-summary.md','07-questions-for-the-maintainer.md','README.md']}
EXACT={'.github/sessions/saved-session-state-feature-m6-patches-unshipped-690.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md','docs/retros/2026-11-02-m6-patches-unshipped.md'}
NEW_TOOLS={'s1-input-contract.py','check-owner-outcomes.py','prepare-owner-outcomes.py','final-confinement.py','retirement.py','retirement-controls.py','retirement-owner-scope.py','final-record-scan.py','final-record-controls.py'}
def allowed(p):return p in NARR|EXACT or any(p.startswith(R+'stage-'+s+'/') for s in 'efgh') or p in {R+'tools/'+x for x in NEW_TOOLS}
def check_paths(paths):
 bad=[p for p in paths if not allowed(p)];assert not bad,'frozen or out-of-scope path: '+repr(bad)
def git(*a):return subprocess.check_output(['git',*a])
def tree(ref,paths):
 out={}
 for line in git('ls-tree','-rz',ref,'--',*paths).split(b'\0'):
  if line:
   meta,p=line.decode().split('\t',1);out[p]=tuple(meta.split())
 return out
def blob_on_disk(path):
 p=pathlib.Path(path);s=p.lstat()
 if stat.S_ISLNK(s.st_mode):mode='120000';b=os.readlink(p).encode()
 else:
  assert stat.S_ISREG(s.st_mode),'not ordinary '+path
  mode='100755' if s.st_mode&0o111 else '100644';b=p.read_bytes()
 return mode,'blob',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
if '--fixture' in sys.argv:
 check_paths(json.loads(pathlib.Path(sys.argv[sys.argv.index('--fixture')+1]).read_text()));print('PASS new confinement fixture');sys.exit(0)
assert str(pathlib.Path.cwd())=='/workspace/repos/pixelelated/distribution.worktrees/m6-patches-unshipped-690'
assert set(os.sched_getaffinity(0))<=set(range(8,24))
subprocess.run(['git','merge-base','--is-ancestor',D,'HEAD'],check=True)
current=git('diff','--name-only',D).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();check_paths(current)
commits=git('rev-list',D+'..HEAD').decode().splitlines()
for c in commits:
 assert len(git('show','-s','--format=%P',c).split())==1,'coordinator merge forbidden'
 check_paths(git('diff-tree','--no-commit-id','--name-only','-r',c).decode().splitlines())
 assert not git('diff-tree','--no-commit-id','--diff-filter=DR','--name-only','-r',c).strip(),'record deletion/rename'
baseline=tree(D,[R]);frozen={p:v for p,v in baseline.items() if p not in NARR}
for p,v in frozen.items():assert blob_on_disk(p)==v,'accepted artifact changed: '+p
summary=json.loads(git('show',D+':'+R+'stage-a/source/summary.json'));source=json.loads(git('show',D+':'+R+'stage-a/source/tree.json'))
selected=set(source)|set(summary['recipe_sha256'])|set(summary['selector_sha256'])
seeds=tree(SEED,sorted(selected));heads=tree('HEAD',sorted(selected));ds=tree(D,sorted(selected));assert seeds==heads==ds,'selected source/ref identity drift'
for p,v in seeds.items():assert blob_on_disk(p)==v,'source worktree identity drift: '+p
# The complete seed diff also confines paths, independently of selected-source lists.
allpaths=git('diff','--name-only',SEED).decode().splitlines()
assert all(p.startswith(R) or p in EXACT for p in allpaths),'source/rule/register/survey edit'
result={'accepted_at':D,'head':git('rev-parse','HEAD').decode().strip(),'commits_after_D':commits,'frozen_artifacts_compared':len(frozen),'selected_sources':len(source),'recipes':len(summary['recipe_sha256']),'selectors':len(summary['selector_sha256']),'selected_union':len(selected),'frozen_modes_blobs_equal':True,'source_seed_D_HEAD_worktree_equal':True,'changed_paths':sorted(set(current)),'qualification':'Metadata identity reconciliation only; no accepted producer/control/application replay. Original whitespace and stored transport bytes preserved.'}
if '--out' in sys.argv:pathlib.Path(sys.argv[sys.argv.index('--out')+1]).write_text(json.dumps(result,indent=2)+'\n')
print('PASS final confinement:',len(commits),'record commits;',len(frozen),'frozen D artifacts;',len(source),'source keys/31recipes/6selectors; original modes/blobs/transport unchanged; no merge/source/removal edit')
