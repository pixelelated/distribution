"""Root immutable T44 record comparisons, without invoking accepted producers."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

ROOT=Path(__file__).parent/'t44-final'
TIP='f01abd480f4e0b337a9fcdde2cec9bc1746b525d'
D='923dd5371ded83fa965449a83f7a16d15a174772'
SEED='48a335700d05a733703e1b58536877b91b921259'
AUDIT='docs/audits/2026_11_02-epic-m6-es-vendored-and-data/'
sha=lambda b:hashlib.sha256(b).hexdigest()
calls=[]
def git(*args):
    p=subprocess.run(['git',*args],capture_output=True)
    calls.append({'argv':['git',*args],'rc':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)})
    assert p.returncode==0,args
    return p.stdout
def tree(ref):
    result={}
    for row in git('ls-tree','-r','-z',ref).split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);result[path.decode()]=meta.decode()
    return result

def main():
    index=json.loads((ROOT/'publication/index.json').read_bytes())
    entries={e['path']:e for e in index['entries']}
    def read(name):
        e=entries[name];b=(ROOT/'publication'/e['stored']).read_bytes()
        if e.get('encoding')=='utf8-json':b=json.loads(b)['raw'].encode()
        assert len(b)==e['bytes'] and sha(b)==e['sha256'],name
        return b
    pub=json.loads(read('publication-readback.json'));results=[]
    for c in pub['command_receipts']:
        b=read(c['path']);assert sha(b)==c['sha256'];r=json.loads(b);folder=str(Path(c['path']).parent)
        assert r['rc']==c['rc'] and r['argv'] and r['started_at']<=r['ended_at']
        assert r['cpus']==list(range(8,24))
        for label in ['stdout','stderr']:assert sha(read(folder+'/'+label))==r[label+'_sha256']
        results.append({'receipt':c['path'],'argv':r['argv'],'rc':r['rc'],'head':r['head']})
    assert read('published-head/stdout').decode().splitlines()==[TIP,'41606eaa375c6ef56d857c3ffc9e01d69e8a1e47']
    assert not read('published-status/stdout') and not read('final-es-status/stdout')
    assert read('final-es-identity/stdout').decode().splitlines()==['55158d2a64c69fe295fb4e67fd174424a71b1b4d','64b90eb8cb07bdfcd690c74ff6bc980ae490657c']
    remote=[x for x in results if 'ls-remote' in x['argv']];assert len(remote)==1 and remote[0]['rc']==0
    assert read(str(Path(remote[0]['receipt']).parent)+'/stdout').decode().split()[0]==TIP
    config=json.loads(git('show',TIP+':'+AUDIT+'stage-e/allowlist.json'))
    st,dt,tt=map(tree,[SEED,D,TIP])
    changed=[p for p in st.keys()|tt.keys() if st.get(p)!=tt.get(p)]
    assert all(p.startswith(AUDIT) or p in config['exact_paths'] for p in changed)
    assert all(p in tt and tt[p].startswith('100644 blob ') for p in changed)
    frozen=[p for p in dt if p.startswith(AUDIT) and p not in config['editable']]
    assert len(frozen)==268 and all(dt[p]==tt.get(p) for p in frozen)
    assert sum(p.startswith(AUDIT) for p in dt)==274 and sum(p.startswith(AUDIT) for p in tt)==440
    history=[]
    for rev in git('rev-list','--reverse',SEED+'..'+TIP).decode().splitlines():
        parents=git('rev-list','--parents','-n','1',rev).decode().split();assert len(parents)==2
        paths=git('diff-tree','--no-commit-id','--name-only','-r',rev).decode().splitlines()
        assert all(p.startswith(AUDIT) or p in config['exact_paths'] for p in paths)
        history.append({'commit':rev,'parent':parents[1],'paths':paths})
    guard=git('show',TIP+':'+AUDIT+'tools/final-confinement.py')
    controls=json.loads(git('show',TIP+':'+AUDIT+'stage-e/controls/results.json'))['controls']
    assert len(controls)==11 and sum(c['rc']==0 for c in controls)==1
    assert all(c['rc']==c['expected_rc'] and c['program_sha256']==sha(guard) for c in controls)
    summary={'result':'PASS','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'tip':TIP,'accepted_d':D,'seed':SEED,'publication_files':len(entries),'command_receipts':results,
        'commands_rc0':sum(c['rc']==0 for c in results),'commands_rc1':sum(c['rc']==1 for c in results),
        'frozen_D':len(frozen),'D_audit_files':274,'final_audit_files':440,'guard_controls':len(controls),
        'history':history,'git_reads':calls,'source_claim':'All seed-to-tip changes confined to allowed records; frozen accepted bytes unchanged.',
        'limits':'Original missing metadata remains missing. Controls reconciled, never replayed. No actual integration or cleanup.'}
    (ROOT/'root-reconciliation.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('history','git_reads','command_receipts')}))
if __name__=='__main__':main()
