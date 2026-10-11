from pathlib import Path
import subprocess,os,json,hashlib
p=Path(__file__).resolve().parent;r=Path.cwd();src=Path('/workspace/tmp/pix541-refresh72/final-patched')
(p/'run.path').write_text(str(r/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
files=[x for folder in ['projects/ROCKNIX/packages/network/raofflineproxy','projects/ROCKNIX/packages/network/rclone'] for x in (r/folder).rglob('*') if x.is_file()]+[r/'tools/raofflineproxy-integration-test',r/'tools/last-good-scripts-test',r/'tools/fork-package-freshness']
seal={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in files};(p/'seal.json').write_text(json.dumps(seal,indent=2)+'\n')
env={**os.environ,'TMPDIR':str(p/'fixtures'),'RAOFFLINEPROXY_RCHASH_LIB':str(src/'.host-qualification-541/libraproxy_rchash.so'),'QA_SYSTEM_ROOT':'/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/image/system','ES_SRC':'/home/max/Development/emulationstation-next.worktrees/qa-integration'}
steps=[('proxy-lint',['tools/pkgcheck','raofflineproxy']),('rclone-lint',['tools/pkgcheck','rclone']),('schema',['tools/rc-preflight','--only','proxy-schema']),('integration',['tools/raofflineproxy-integration-test','--source',str(src),'--predecessor-source','/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-879b158995d412af434301ebdae581f66b8b6d57']),('regression',['tools/last-good-scripts-test'])]
rows=[]
for name,cmd in steps:
 print('START',name,flush=True)
 with (p/(name+'.log')).open('w') as f:rc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 rows.append({'step':name,'returncode':rc});(p/'result.json').write_text(json.dumps(rows,indent=2)+'\n');print('END',name,rc,flush=True)
 if rc:raise SystemExit(rc)
for n,h in seal.items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
print('PASS final source seal',flush=True)
