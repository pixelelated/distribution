#!/usr/bin/env python3
"""Protect all non-owned paths in the tree and every commit since the seed."""
import json,pathlib,subprocess,sys
ROOT='docs/audits/2026_11_02-epic-m6-patches-unshipped/';SEED='601e4694f9726b2228d3571efdb5cfc061c6d442'
EXACT={'.github/sessions/saved-session-state-feature-m6-patches-unshipped-690.md','docs/work-logs/2026_11-work_logs/2026_11_02-work_log.md','docs/work-logs/INDEX.md','docs/retros/2026-11-02-m6-patches-unshipped.md'}
def allowed(path):return path.startswith(ROOT) or path in EXACT
def check(paths):
 forbidden=[p for p in paths if not allowed(p)];assert not forbidden,'forbidden source/context/selector/rule/register path: '+repr(forbidden)
def git(*a):return subprocess.check_output(['git',*a]).decode()
if '--fixture' in sys.argv:
 p=pathlib.Path(sys.argv[sys.argv.index('--fixture')+1]);check(json.loads(p.read_text()));print('PASS fixture scope');sys.exit(0)
subprocess.run(['git','merge-base','--is-ancestor',SEED,'HEAD'],check=True)
check(git('diff','--name-only',SEED,'HEAD').splitlines());check(git('diff','--name-only','HEAD').splitlines());check(git('ls-files','--others','--exclude-standard').splitlines())
commits=git('rev-list',SEED+'..HEAD').splitlines()
for c in commits:
 assert len(git('show','-s','--format=%P',c).split())==1,'unauthorized merge '+c
 check(git('diff-tree','--no-commit-id','--name-only','-r',c).splitlines())
assert not git('diff','--diff-filter=DR','--name-only',SEED,'HEAD').strip(),'deletion/rename'
print('PASS owned-path tree and per-commit guard; '+str(len(commits))+' new commits; no merge/source/removal edit')
