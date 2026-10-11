from pathlib import Path
import subprocess,os,hashlib,json,datetime
p=Path(__file__).resolve().parent;r=Path.cwd();src=Path('/workspace/tmp/pix541-refresh72/final-patched')
(p/'run.path').write_text(str(r/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
seal=json.loads((p/'seal.json').read_text())
def verify():
 for n,h in seal.items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
verify()
env={**os.environ,'TMPDIR':str(p),'RAOFFLINEPROXY_RCHASH_LIB':str(src/'.host-qualification-541/libraproxy_rchash.so'),'RAOFFLINEPROXY_CONFIG_DIR':str(p/'config')}
steps=[('native',['bash',str(p/'build-native.sh')],r),('upstream',['python3','-m','unittest','discover','-v','-s','linux/tests','-p','test_linux_*.py'],src),('integration',[str(r/'tools/raofflineproxy-integration-test'),'--source',str(src),'--predecessor-source','/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-879b158995d412af434301ebdae581f66b8b6d57'],r)]
results=[]
for name,cmd,cwd in steps:
 print('START',name,flush=True)
 with (p/(name+'.log')).open('w') as log:rc=subprocess.run(cmd,cwd=cwd,env={**env,'PYTHONPATH':str(src)},stdout=log,stderr=subprocess.STDOUT).returncode
 results.append({'step':name,'returncode':rc});(p/'result.json').write_text(json.dumps(results,indent=2)+'\n')
 print('END',name,rc,flush=True)
 if rc:raise SystemExit(rc)
 if name=='upstream':
  text=(p/'upstream.log').read_text();assert 'skipped=' not in text and ' skipped ' not in text
verify();print('PASS native-enabled upstream and actual-predecessor fork integration',flush=True)
