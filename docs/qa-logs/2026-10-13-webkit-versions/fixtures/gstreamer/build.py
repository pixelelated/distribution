from pathlib import Path
import subprocess,os,json,datetime,hashlib
r=Path(__file__).parent
old='/workspace/repos/rocknix.worktrees/m7-pixelelated';cache='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20';pkg=old+'/build.pixelelated-GENERIC_X64.x86_64/build/gstreamer-1.29.2'
cmd=['docker','run','--rm','--name','pixelelated-gst-572','--network','none','--user',f'{os.getuid()}:{os.getgid()}','--memory','2g','--memory-swap','2g','--mount',f'type=bind,src={cache},dst={old},readonly','--mount',f'type=bind,src={r}/package,dst={pkg}','--mount',f'type=bind,src={r},dst=/work','--workdir',pkg,'ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39','bash','/work/build.sh']
result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd}
try:
 p=subprocess.run(cmd);result['build_rc']=p.returncode;assert p.returncode==0
 old=r/'installed-old';new=r/'installed-new';rel='usr/lib/libgstcontroller-1.0.so.0'
 assert not (old/rel).exists() and (new/rel).is_file()
 scanner=new/'usr/lib/gstreamer-1.0/gst-plugin-scanner';assert scanner.is_file() and os.access(scanner,os.X_OK)
 result['controller_old_removed']=True;result['controller_new_preserved']=True;result['scanner_present']=True
 files={}
 for p in new.rglob('*'):
  if p.is_file() and not p.is_symlink():
   with p.open('rb') as f:files[str(p.relative_to(new))]=hashlib.file_digest(f,'sha256').hexdigest()
 result['installed_manifest']=files;result['rc']=0
except BaseException as e:result.update(rc=1,error=repr(e));raise
finally:
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'result.json').write_text(json.dumps(result,indent=2)+'\n')
