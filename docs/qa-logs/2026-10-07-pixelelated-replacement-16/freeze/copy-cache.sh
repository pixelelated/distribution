#!/bin/bash
set -euo pipefail
TASK_OLD=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15
TASK_NEW=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16
TASK_OWNER=/workspace/tmp/pixelelated-m7-replacement-16
TASK_ROOT=build.pixelelated-GENERIC_X64.x86_64
[ "$(id -u)" = 1000 ]
[ ! -e "$TASK_OWNER/copy.start" ]
[ ! -e "$TASK_NEW/$TASK_ROOT" ]
[ "$(git -C "$TASK_NEW" rev-parse HEAD)" = ee014909137e03706e0b3020b8396be589aaa705 ]
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/copy.start"
printf '%s\n' "$TASK_NEW/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/copy.run"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/copy.rc"' EXIT
python3 - "$TASK_OLD" "$TASK_NEW" "$TASK_OWNER" <<'PY'
import hashlib,json,os,pathlib,subprocess,sys
old,new,out=map(pathlib.Path,sys.argv[1:])
j=json.loads(pathlib.Path('/workspace/tmp/pixelelated-m7-replacement-15/inputs.json').read_text())
for p,h in j['source_files'].items():assert hashlib.sha256((old/p).read_bytes()).hexdigest()==h,p
for p,t in j['source_symlinks'].items():assert (old/p).is_symlink() and os.readlink(old/p)==t,p
product=subprocess.check_output(['git','-C',str(new),'diff','--no-renames','--name-only',j['distribution_commit'],'HEAD','--','packages','projects','scripts','config','distributions','Makefile'],text=True).splitlines()
assert product==['projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore', 'projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout', 'projects/ROCKNIX/packages/ui/emulationstation/package.mk'],product
preserved=0
for raw in subprocess.check_output(['git','-C',str(new),'ls-files','-z']).split(b'\0'):
 if not raw:continue
 p=os.fsdecode(raw); a=old/p; b=new/p
 if a.is_file() and b.is_file() and not a.is_symlink() and not b.is_symlink() and a.read_bytes()==b.read_bytes():
  s=a.stat(); os.utime(b,ns=(s.st_atime_ns,s.st_mtime_ns)); preserved+=1
(out/'copy-input-proof.json').write_text(json.dumps({'original_source_hashes_pass':True,'product_delta':product,'unchanged_tracked_file_timestamps_preserved':preserved,'copy_mode':'independent rsync -aH files; no links to original root'},indent=2)+'\n')
print('PASS original source hashes and isolated reviewed product delta',flush=True)
PY
rsync -aH --numeric-ids --info=progress2 "$TASK_OLD/$TASK_ROOT/" "$TASK_NEW/$TASK_ROOT/" | python3 "$TASK_OWNER/progress.py"
echo 'Copy finished; checksum comparison begins'
rsync -aHnc --numeric-ids --delete --itemize-changes "$TASK_OLD/$TASK_ROOT/" "$TASK_NEW/$TASK_ROOT/" > "$TASK_OWNER/cache-compare.txt"
[ ! -s "$TASK_OWNER/cache-compare.txt" ]
python3 - "$TASK_OLD/$TASK_ROOT" "$TASK_NEW/$TASK_ROOT" <<'PY'
import pathlib,sys
old,new=map(pathlib.Path,sys.argv[1:])
n=0
for p in new.rglob('*'):
 if p.is_file() and not p.is_symlink():
  a=(old/p.relative_to(new)).stat(); b=p.stat()
  assert (a.st_dev,a.st_ino)!=(b.st_dev,b.st_ino),p
  n+=1
  if n%250000==0:print('Verified independent inodes:',n,flush=True)
pathlib.Path('/workspace/tmp/pixelelated-m7-replacement-16/cache-ready.json').write_text(__import__('json').dumps({'checksum_equal':True,'independent_regular_files':n,'old':str(old),'new':str(new)},indent=2)+'\n')
print('PASS cache checksum equality and independent inodes:',n,flush=True)
PY
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/copy.finish"

printf "0\n" > "$TASK_OWNER/cache-ready.rc"
