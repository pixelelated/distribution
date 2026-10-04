import hashlib,json,os,pathlib,subprocess
j=json.loads(pathlib.Path('/workspace/tmp/pixelelated-m7-replacement-06/inputs.json').read_text())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==j['distribution_commit']
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()==j['distribution_branch']
for p,h in j['source_files'].items():assert hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h,p
for p,h in j['qa_source_files'].items():assert hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h,p
for p,t in j['source_symlinks'].items():assert pathlib.Path(p).is_symlink() and os.readlink(p)==t,p
assert hashlib.sha256(pathlib.Path(j['host_options_path']).read_bytes()).hexdigest()==j['host_options_sha256']
assert subprocess.check_output(['docker','image','inspect',j['container'],'--format','{{.Id}}'],text=True).strip()==j['container_image_id']
assert int(subprocess.check_output(['nproc'],text=True))==j['global_jobs']
assert '-j4' in pathlib.Path('packages/web/webkitgtk/package.mk').read_text()
print('PASS frozen inputs, host options, container and 24/4 concurrency',flush=True)
