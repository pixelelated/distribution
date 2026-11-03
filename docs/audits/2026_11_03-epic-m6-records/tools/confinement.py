"""Inspect each new commit, including reverted changes; never check out source."""
import argparse,json,pathlib,subprocess,sys
AUDIT='docs/audits/2026_11_03-epic-m6-records/'
EXACT={'.github/sessions/saved-session-state-feature-m6-records-693.md','docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md','docs/work-logs/INDEX.md'}
def allowed(path):return path.startswith(AUDIT) or path in EXACT
def run(repo,seed,tip,working=False):
 def git(*args):return subprocess.check_output(['git','-C',repo,*args])
 if subprocess.run(['git','-C',repo,'merge-base','--is-ancestor',seed,tip],capture_output=True).returncode:print('REFUSE seed is not ancestor');return 1
 commits=git('rev-list','--reverse',seed+'..'+tip).decode().splitlines();rows=[];bad=[]
 for c in commits:
  parents=git('show','-s','--format=%P',c).decode().split()
  if len(parents)!=1:bad.append({'commit':c,'reason':'merge/root after seed'});continue
  paths=[p.decode() for p in git('diff-tree','--no-commit-id','--name-only','-r','-z',parents[0],c).split(b'\0') if p]
  rows.append({'commit':c,'paths':paths})
  bad += [{'commit':c,'path':p} for p in paths if not allowed(p)]
 if working:
  paths=set()
  for args in [('diff','--name-only','-z',seed),('ls-files','--others','--exclude-standard','-z')]:paths.update(p.decode() for p in git(*args).split(b'\0') if p)
  bad += [{'working':True,'path':p} for p in sorted(paths) if not allowed(p)]
  rows.append({'working_paths':sorted(paths)})
 print(json.dumps({'seed':seed,'tip':tip,'commits':rows,'refusals':bad,'allowlist':sorted(EXACT)+[AUDIT]},sort_keys=True))
 print(('REFUSE' if bad else 'PASS')+' T46 per-commit confinement; final diff alone is insufficient')
 return 1 if bad else 0
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--seed',required=True);p.add_argument('--tip',default='HEAD');p.add_argument('--working',action='store_true');a=p.parse_args();sys.exit(run(a.repo,a.seed,a.tip,a.working))
