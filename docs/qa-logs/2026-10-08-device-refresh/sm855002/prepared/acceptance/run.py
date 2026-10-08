from pathlib import Path
import hashlib,json,os,subprocess,sys
O=Path(__file__).resolve().parent;B=Path('/workspace/tmp/pixelelated-m7-sm8550-refresh-02')
(O/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n');rc=1
try:
 for n,h in json.loads((O/'seal.json').read_text()).items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
 assert json.loads((B/'build-consumption.json').read_text())['result']=='PASS'
 subprocess.run(['python3','-I',str(O/'verify-firmware.py')],check=True);rc=0
finally:
 (O/'inner.rc').write_text(str(rc)+'\n');(O/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
