from pathlib import Path
import subprocess,os,json,hashlib,datetime
p=Path(__file__).resolve().parent
root=Path.cwd()
(p/'run.path').write_text(str(root/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
for n,h in json.loads((p/'seal.json').read_text()).items():
 assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
cmd=['docker','run','--rm','--user',f'{os.getuid()}:{os.getgid()}','-v',str(root)+':/src:ro','-v',str(p)+':/proof','-v','/workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git:ro','-w','/src','ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39','bash','/proof/inside.sh']
rc=subprocess.run(cmd).returncode
(p/'result.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':rc,'command':cmd},indent=2)+'\n')
raise SystemExit(rc)
