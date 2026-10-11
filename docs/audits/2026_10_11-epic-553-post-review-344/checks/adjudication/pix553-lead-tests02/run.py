from pathlib import Path
import subprocess,os,json,re
P=Path(__file__).resolve().parent;R=Path('/workspace/repos/rocknix.worktrees/m7-component-inputs')
env={**os.environ,'TMPDIR':str(P/'tmp'),'RAOFFLINEPROXY_RCHASH_LIB':'/workspace/tmp/pix541-refresh72/final-patched/.host-qualification-541/libraproxy_rchash.so'}
runner=R/'tools/raofflineproxy-integration-test'
args=['--source','/workspace/tmp/pix541-refresh72/final-patched','--predecessor-source','/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-879b158995d412af434301ebdae581f66b8b6d57']
with (P/'upstream-injected.log').open('w') as f:q=subprocess.run(['python3',str(P/'injector.py'),*args],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=90)
t=(P/'upstream-injected.log').read_text();assert q.returncode==1 and 'UPSTREAM BASE MUST NOT BE COLLECTED' in t and 'Ran ' in t
with (P/'old-rehearsal.log').open('w') as f:z=subprocess.run(['tools/vm-upgrade-readiness-test','--rehearsal',str(P/'old-rehearsal.sh')],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=20)
u=(P/'old-rehearsal.log').read_text();assert z.returncode!=0 and 'IndexError' in u and 'Traceback' in u
result={'result':'CONFIRMED ORIGINAL TOOL GAPS','upstream_base_injection_returncode':q.returncode,'upstream_base_injection_tests':re.search(r'Ran (\d+) tests',t).group(1),'old_rehearsal_returncode':z.returncode,'old_rehearsal_traceback':True}
(P/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
