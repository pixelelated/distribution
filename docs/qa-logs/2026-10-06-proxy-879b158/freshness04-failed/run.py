import os,subprocess,pathlib,datetime,json,hashlib
owner=pathlib.Path(__file__).parent
run=pathlib.Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN']
(owner/'run.path').write_text(str(run)+'\n')
(owner/'start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
j=json.loads(pathlib.Path('/workspace/tmp/pixelelated-m7-replacement-13/inputs.json').read_text())
def verify():
 n=0
 for p,h in j['source_files'].items():
  if p.endswith('/package.mk'):
   assert hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h,p;n+=1
 p='tools/fork-package-freshness';assert hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==j['qa_source_files'][p]
 print('PASS exact frozen recipes and freshness tool',n,flush=True)
verify()
e=os.environ.copy();e['FRESHNESS_HEAD']=j['distribution_commit']
r=subprocess.run(['tools/fork-package-freshness'],env=e).returncode
verify()
(owner/'inner.rc').write_text(str(r)+'\n')
raise SystemExit(r)
