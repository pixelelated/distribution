import os,subprocess,pathlib,datetime,json
owner=pathlib.Path(__file__).parent
run=pathlib.Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN']
(owner/'run.path').write_text(str(run)+'\n')
(owner/'start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
e=os.environ.copy();e['FRESHNESS_HEAD']='d6e8390c93bed87efe2dcc23cd402a271cacd1c7'
r=subprocess.run(['tools/fork-package-freshness'],env=e).returncode
(owner/'inner.rc').write_text(str(r)+'\n')
raise SystemExit(r)
