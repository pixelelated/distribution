from pathlib import Path
import datetime,hashlib,json,os,subprocess,shutil
out=Path('/workspace/tmp/pixelelated-m7-replacement-12');prior=Path('/workspace/tmp/pixelelated-m7-replacement-11');j=json.loads((out/'inputs.json').read_text());root=j['build_root'];staging=Path(j['cache_staging_worktree']);dest=Path(j['host_worktree']);old=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement10')
proof=json.loads((prior/'copy-completion.json').read_text());assert proof['durable_runner_rc']==0 and set(proof['result_channels'].values())=={0}
assert not (prior/'build.start').exists() and not (prior/'run.path').exists()
assert not (staging/'target').exists()
assert hashlib.sha256((prior/'inputs.json').read_bytes()).hexdigest()==j['cache_staging_manifest_sha256']
for row in proof['owned_processes']:assert not (Path('/proc')/str(row['pid'])).exists(),row
for name in ['copy-completion.json','cache-ready.json','copy-input-proof.json']:shutil.copyfile(prior/name,out/('staging-'+name))
ready=json.loads((prior/'cache-ready.json').read_text());assert ready['checksum_equal'] and ready['independent_regular_files']>2500000
src=staging/root;dst=dest/root;assert src.is_dir() and not dst.exists()
oldmanifest=json.loads(Path('/workspace/tmp/pixelelated-m7-replacement-10/inputs.json').read_text())
for p,h in oldmanifest['source_files'].items():assert hashlib.sha256((old/p).read_bytes()).hexdigest()==h,p
for p,t in oldmanifest['source_symlinks'].items():assert (old/p).is_symlink() and os.readlink(old/p)==t,p
n=0
for raw in subprocess.check_output(['git','-C',str(dest),'ls-files','-z']).split(b'\0'):
 if not raw:continue
 p=os.fsdecode(raw);a=old/p;b=dest/p
 if a.is_file() and b.is_file() and not a.is_symlink() and not b.is_symlink() and a.read_bytes()==b.read_bytes():
  s=a.stat();os.utime(b,ns=(s.st_atime_ns,s.st_mtime_ns));n+=1
before=src.stat();assert before.st_dev==dest.stat().st_dev
os.rename(src,dst)
after=dst.stat();assert (before.st_dev,before.st_ino)==(after.st_dev,after.st_ino) and not src.exists()
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'old':str(old/root),'new':str(dst),'staging':str(src),'staging_unbuilt':True,'rename_preserved_directory_inode':{'device':before.st_dev,'inode':before.st_ino},'independent_regular_files':ready['independent_regular_files'],'original_copy_receipt_sha256':hashlib.sha256((prior/'copy-completion.json').read_bytes()).hexdigest(),'unchanged_tracked_file_timestamps_preserved':n}
(out/'cache-relocation.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS completed unbuilt cache renamed with original copy custody retained',flush=True)
