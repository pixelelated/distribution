from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
repo=Path.cwd();primary=Path('/workspace/repos/rocknix');es=Path('/home/max/Development/emulationstation-next.worktrees/qa-integration')
frozen=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16');commit='ee014909137e03706e0b3020b8396be589aaa705';espin='72494bc72e3d64d4dcfeb4e6478052bbdf166c5b'
commands=[]
def git(where,*args):
 r=subprocess.run(['git','-C',str(where),*args],text=True,capture_output=True)
 commands.append(dict(repository=str(where),args=list(args),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));assert r.returncode==0,(args,r.stderr)
 return r.stdout
assert 'next' in git(primary,'branch','--contains',commit).split()
assert 'test/qa-integration' in git(es,'branch','--contains',espin).split()
assert git(es,'rev-parse','HEAD').strip()==espin
sources='projects/ROCKNIX/packages/network/rclone/sources/'
expected=json.loads((repo/'docs/qa-logs/2026-10-07-pixelelated-replacement-16/supplemental02-acceptance/acceptance.json').read_text())['installed_hashes']['a']
for name,digest in expected.items():
 path=sources+name
 assert hashlib.sha256((frozen/path).read_bytes()).hexdigest()==digest
 assert hashlib.sha256(git(primary,'show','next:'+path).encode()).hexdigest()==digest
 git(primary,'log','-1','--format=%H %s','next','--',path)
pinpath='projects/ROCKNIX/packages/ui/emulationstation/package.mk';assert espin in git(primary,'show','next:'+pinpath)
git(primary,'log','-1','--format=%H %s','next','--',pinpath)
for path in ['es-app/src/guis/GuiMenu.cpp','es-app/src/guis/GuiCloudTransfer.cpp','es-app/src/main.cpp','es-app/src/ThreadedCloudSync.cpp','locale/lang/fr/LC_MESSAGES/emulationstation2.po']:
 assert (es/path).is_file(),path;git(es,'log','-1','--format=%H %s',espin,'--',path)
dest=repo/'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/evidence/remediation-host/build16-integration-commands.json'
with dest.open('x') as f:json.dump(dict(verified_utc=datetime.now(timezone.utc).isoformat(),distribution=commit,emulationstation=espin,source_matches_installed=expected,commands=commands,scope='Source integration and candidate identity only. Does not resolve remaining audit findings or substitute for pending UI/clean/upgrade/protocol acceptance.'),f,indent=2);f.write('\n')
print('PASS landed-source ancestry, exact installed-source hashes and ES pin; remaining acceptance is separate')
