from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
p=Path(__file__).resolve().parent;r=Path.cwd();head=sys.argv[1]
assert not (p/'inputs.json').exists()
assert str(r)=='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement19'
def git(*a):return subprocess.check_output(['git',*a],text=True).strip()
assert git('rev-parse','HEAD')==head and git('branch','--show-current')=='build/m7-pixelelated-replacement19'
assert not git('status','--porcelain')
assert git('ls-remote','origin','refs/heads/next').split()[0]==head
copy=Path('/workspace/tmp/pixelelated-m7-cache19-recheck')
assert json.loads((copy/'launcher-result.json').read_text())['runner_returncode']==0
assert (copy/'copy.rc').read_text().strip()=='0' and (copy/'cache-ready.rc').read_text().strip()=='0'
assert not (copy/'cache-compare.txt').read_bytes()
initial=Path('/workspace/tmp/pixelelated-m7-replacement-19/inputs.json');j=json.loads(initial.read_text())
now=datetime.datetime.now(datetime.timezone.utc)
j.update(distribution_commit=head,proxy_commit='c7ebd1b6e777f3751ff0ecdf8aba54045844e00d',rclone_version='1.75.2',frozen_at=now.isoformat(),build_timestamp=now.strftime('%Y%m%dT%H%M%SZ'),purpose='M7.P5 combined installed #529-#541 qualification; engineering dev, publication holds remain',superseded_initial_manifest_sha256=hashlib.sha256(initial.read_bytes()).hexdigest(),cache_acceptance_owner=str(copy),cache_acceptance_sha256=hashlib.sha256((copy/'cache-ready.json').read_bytes()).hexdigest())
# All tracked build inputs, including newly added paths; do not rely on old names.
files={};links={};qa={}
for raw in subprocess.check_output(['git','ls-files','-z']).split(b'\0'):
 if not raw:continue
 name=os.fsdecode(raw);f=r/name
 product=name.split('/')[0] in ['config','distributions','packages','projects','scripts'] or name in ['LICENSE.md','TRADEMARK.md','Makefile']
 if f.is_symlink():
  if product:links[name]=os.readlink(f)
 elif product:files[name]=hashlib.sha256(f.read_bytes()).hexdigest()
 elif name.startswith('tools/'):qa[name]=hashlib.sha256(f.read_bytes()).hexdigest()
j.update(source_files=files,source_symlinks=links,qa_source_files=qa,recipe_files=sum(n.endswith('/package.mk') for n in files))
qualified=Path('/workspace/tmp/pix541-refresh72/final-patched')
j['proxy_qualified_files']={str(f.relative_to(qualified)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (qualified/'linux').rglob('*.py') if '__pycache__' not in f.parts}
assert re.search(r'^PKG_VERSION="'+re.escape(j['proxy_commit'])+'"$',(r/'projects/ROCKNIX/packages/network/raofflineproxy/package.mk').read_text(),re.M)
assert 'PKG_VERSION="'+j['emulationstation_commit']+'"' in (r/'projects/ROCKNIX/packages/ui/emulationstation/package.mk').read_text()
assert hashlib.sha256(Path(j['host_options_path']).read_bytes()).hexdigest()==j['host_options_sha256']
(p/'inputs.json').write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')
delta=git('diff','--name-status',j['cache_parent_distribution'],'HEAD','--','config','distributions','packages','projects','scripts','Makefile')
(p/'product-delta.txt').write_text(delta+'\n')
(p/'superseded-freeze.json').write_text(json.dumps({'superseded':str(initial),'reason':'#541 latest dependencies; initial cache-only attempt produced no image','new_commit':head,'timestamp':j['build_timestamp']},indent=2)+'\n')
print('Frozen',head,j['build_timestamp'],len(files),'product files',len(links),'symlinks',len(qa),'QA files')
