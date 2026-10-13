from pathlib import Path
import os,json,subprocess,datetime
r=Path(__file__).parent
pre=json.loads((r/'prepare-owner/launcher-result.json').read_text());assert pre['runner_returncode']==0 and not Path('/proc',str(pre['pid'])).exists()
assert json.loads((r/'prepare-result.json').read_text())['rc']==0
image='ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39'
old='/workspace/repos/rocknix.worktrees/m7-pixelelated';cache='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20';pkg=old+'/build.pixelelated-GENERIC_X64.x86_64/build/webkitgtk-2.54.1'
cmd=['docker','run','--rm','--name','pixelelated-webkit-570-2540','--network','none','--user',f'{os.getuid()}:{os.getgid()}','--memory','24g','--memory-swap','24g','--mount',f'type=bind,src={cache},dst={old},readonly','--mount',f'type=bind,src={r}/package-2.54.0,dst={pkg}','--mount',f'type=bind,src={r},dst=/work','--workdir',pkg,image,'bash','/work/build-2540.sh']
(r/'build-command.json').write_text(json.dumps(cmd,indent=2)+'\n');res={'started':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 p=subprocess.run(cmd);res['rc']=p.returncode
 if p.returncode:raise SystemExit(p.returncode)
finally:
 res['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'build-2540-result.json').write_text(json.dumps(res,indent=2)+'\n')
