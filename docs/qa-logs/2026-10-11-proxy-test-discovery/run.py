from pathlib import Path
import subprocess,os,json,hashlib,re
p=Path(__file__).resolve().parent;r=Path.cwd();src=Path('/workspace/tmp/pix541-refresh72/final-patched')
helper=r/'projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed';before=hashlib.sha256(helper.read_bytes()).hexdigest()
env={**os.environ,'TMPDIR':str(p),'PYTHONDONTWRITEBYTECODE':'1','RAOFFLINEPROXY_RCHASH_LIB':str(src/'.host-qualification-541/libraproxy_rchash.so')}
base=['tools/raofflineproxy-integration-test','--source',str(src),'--predecessor-source','/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-879b158995d412af434301ebdae581f66b8b6d57']
rows=[]
for name,args,expected in [('negative',base+['--helper',str(p/'negative-helper/raofflineproxy-cache-indexed')],1),('fixed',base,0)]:
 with (p/(name+'.log')).open('w') as log:rc=subprocess.run(args,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 text=(p/(name+'.log')).read_text();assert rc==expected,(name,rc,text)
 assert 'Ran 12 tests' in text and 'test_existing_pause_boundaries_survive_removed_upstream_helper' in text
 if name=='negative':assert 'FAILED (failures=1)' in text and 'call(0.0)' in text
 else:assert text.rstrip().endswith('OK') and 'skipped=' not in text
 rows.append({'name':name,'returncode':rc,'expected_returncode':expected,'tests':12,'verdict':'PASS_CONTROL'});(p/'result.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS',name,'12 cases, expected result',rc,flush=True)
assert hashlib.sha256(helper.read_bytes()).hexdigest()==before
(p/'source.json').write_text(json.dumps({'helper_sha256':before,'helper_unchanged':True,'test_sha256':hashlib.sha256((r/'tools/raofflineproxy-integration-test').read_bytes()).hexdigest()},indent=2)+'\n')
