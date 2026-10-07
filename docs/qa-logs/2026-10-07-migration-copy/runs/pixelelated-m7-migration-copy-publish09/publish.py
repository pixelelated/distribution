import datetime,json,pathlib,subprocess
owner=pathlib.Path(__file__).resolve().parent
es='/home/max/Development/emulationstation-next.worktrees/qa-integration'
sha='5d2fcb9b71f363cfa4813d5356f02c48ab58e139'
base='72494bc72e3d64d4dcfeb4e6478052bbdf166c5b'
def git(*args):
 cmd=['git','-C',es,*args]
 print('+ '+' '.join(cmd),flush=True)
 r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 print(r.stdout,end='',flush=True)
 if r.returncode: raise SystemExit(r.returncode)
 return r.stdout.strip()
assert git('status','--porcelain') == ''
assert git('branch','--show-current') == 'test/qa-integration'
assert git('rev-parse','HEAD') == base
assert git('rev-parse','feature/m7-migration-copy') == sha
assert git('remote','get-url','origin') == 'git@github-blitterbot:pixelelated/emulationstation.git'
hooks=pathlib.Path(git('config','--get','core.hooksPath'))
assert hooks.is_absolute() and (hooks/'pre-push').is_file()
git('merge','--ff-only',sha)
assert git('status','--porcelain') == ''
git('push','--atomic','origin','feature/m7-migration-copy','test/qa-integration')
remote=git('ls-remote','origin','refs/heads/feature/m7-migration-copy','refs/heads/test/qa-integration')
refs=dict(line.split()[::-1] for line in remote.splitlines())
assert refs == {'refs/heads/feature/m7-migration-copy':sha,'refs/heads/test/qa-integration':sha},refs
result={'result':'PASS','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':sha,'base':base,'remote':refs,'hooks_path':str(hooks),'distribution_pin':'unchanged by this lane'}
(owner/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS exact source integrated, normal hooks passed, both remote branches verified',flush=True)
