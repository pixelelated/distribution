from pathlib import Path
import subprocess,os,json,re,hashlib,datetime
P=Path(__file__).resolve().parent;R=Path('/workspace/repos/rocknix.worktrees/m7-component-inputs')
env={**os.environ,'TMPDIR':str(P/'tmp'),'PYTHONDONTWRITEBYTECODE':'1','RAOFFLINEPROXY_RCHASH_LIB':'/workspace/tmp/pix541-refresh72/final-patched/.host-qualification-541/libraproxy_rchash.so'}
results=[]
def run(name,cmd,rc=0,required=(),extra=None):
    with (P/(name+'.log')).open('w') as f:
        q=subprocess.run(cmd,cwd=R,env={**env,**(extra or {})},stdout=f,stderr=subprocess.STDOUT,timeout=100)
    t=(P/(name+'.log')).read_text()
    results.append({'name':name,'command':cmd,'returncode':q.returncode,'expected':rc})
    assert q.returncode==rc,(name,q.returncode,t[-4000:])
    for token in required:assert token in t,(name,token,t[-4000:])
    print('PASS '+name,flush=True);return t
args=['--source','/workspace/tmp/pix541-refresh72/final-patched','--predecessor-source','/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/build/raofflineproxy-879b158995d412af434301ebdae581f66b8b6d57']
run('proxy-baseline',['tools/raofflineproxy-integration-test',*args],required=['Ran 12 tests','\nOK\n'])
run('proxy-upstream-injected',['python3',str(P/'injector.py'),*args],required=['Ran 12 tests','\nOK\n'])
run('proxy-new-fork',['python3',str(P/'injector.py'),*args],required=['Ran 13 tests','test_new_fork_method','\nOK\n'],extra={'ADD_FORK_TEST':'1'})
run('proxy-wrong-cooldown',['tools/raofflineproxy-integration-test',*args,'--helper','/workspace/tmp/pix553-proof01/negative-helper'],1,['Ran 12 tests','FAILED (failures=1)'])
run('readiness',['tools/vm-upgrade-readiness-test'],required=['PASS 7 storage-readiness controls'])
fixtures={'historical':Path('/workspace/tmp/pix553-lead-tests02/old-rehearsal.sh'),'missing':P/'missing.sh','unterminated':P/'unterminated.sh','unreadable':P/'absent.sh','encoding':P/'encoding.sh'}
fixtures['missing'].write_text('#!/bin/bash\necho historical\n')
fixtures['unterminated'].write_text('wait_for_storage() {\n echo incomplete\n')
fixtures['encoding'].write_bytes(b'\xff')
for name,p in fixtures.items():
    text=run('readiness-'+name,['tools/vm-upgrade-readiness-test','--rehearsal',str(p)],2,['error:', 'cannot read rehearsal' if name in ('unreadable','encoding') else 'missing or incomplete wait_for_storage function'])
    assert 'Traceback' not in text
run('pair-syntax',['bash','-n','tools/vm-pair'])
run('pair-controls',['tools/vm-pair-test'],required=['PASS 9'])
patch='projects/ROCKNIX/packages/network/raofflineproxy/patches/004-no-cap-on-cached-games.patch'
payload=lambda data:data.split(b'diff --git ',1)[1]
assert payload((R/patch).read_bytes())==payload((P/'before'/patch).read_bytes())
pair='tools/vm-pair'
code=lambda data:[line for line in data.splitlines() if line.strip() and not line.lstrip().startswith('#')]
assert code((R/pair).read_text())==code((P/'before'/pair).read_text())
result={'result':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':results,'patch_diff_payload_unchanged':True,'vm_pair_only_comments_changed':True,'source_hashes':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['tools/raofflineproxy-integration-test','tools/vm-upgrade-readiness-test','tools/vm-pair',patch]}}
(P/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
