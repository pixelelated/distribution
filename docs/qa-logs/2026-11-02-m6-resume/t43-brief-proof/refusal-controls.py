import os, subprocess, pathlib, json, hashlib, time, datetime
P = pathlib.Path(__file__).resolve().parent
R = P/'proof'
BASE = 'afdec2bf8b88135befcb7ec56efb3a7ea327bd73'
assert sorted(os.sched_getaffinity(0)) == list(range(8,24))
ENV = os.environ.copy()
ENV.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1',
           GIT_AUTHOR_NAME='Codex GPT-6 synthetic T43 proof',GIT_AUTHOR_EMAIL='t43-proof@example.invalid',
           GIT_COMMITTER_NAME='Codex GPT-6 synthetic T43 proof',GIT_COMMITTER_EMAIL='t43-proof@example.invalid',
           GIT_AUTHOR_DATE='2026-11-02T21:00:00Z',GIT_COMMITTER_DATE='2026-11-02T21:00:00Z')
def git(*a, data=None):
    return subprocess.check_output(['git','-C',str(R),*a],input=data,env=ENV)
def blob(path): return git('show',BASE+':'+path)
def entries(tree):
    return {x.split(b'\t',1)[1]:x.split(b'\t',1)[0].split() for x in git('ls-tree','-z',tree).split(b'\0') if x}
def change(tree, parts, replacement):
    es=entries(tree); name=parts[0].encode()
    if len(parts)>1:
        es[name]=[b'040000',b'tree',change(es[name][2].decode(),parts[1:],replacement).encode()]
    elif replacement is None: del es[name]
    else: es[name]=replacement
    raw=b''.join(b' '.join(v)+b'\t'+k+b'\0' for k,v in es.items())
    return git('mktree','-z',data=raw).decode().strip()
def make(path,kind):
    old=git('ls-tree',BASE,'--',path).split(b'\t',1)[0].split()
    if kind=='missing': new=None
    elif kind=='mode': new=[b'100755' if old[0]!=b'100755' else b'100644',old[1],old[2]]
    else:
        data=blob(path)+b'\n# SYNTHETIC T43 drift refusal only\n'
        new=[old[0],b'blob',git('hash-object','-w','--stdin',data=data).strip()]
    tree=change(git('rev-parse',BASE+'^{tree}').decode().strip(),path.split('/'),new)
    commit=git('-c','commit.gpgSign=false','commit-tree',tree,'-p',BASE,data=('T43 private negative '+kind+' '+path+'\n').encode()).decode().strip()
    diff=git('diff-tree','--no-commit-id','--name-only','-r',BASE,commit).decode().splitlines()
    assert diff==[path],diff
    return commit,old,new
head=git('rev-parse','HEAD'); refs=git('show-ref','--head')
outroot=pathlib.Path((P/'membership-output-path.txt').read_text().strip())
rows=json.loads((outroot/'source/rows.json').read_text())
links=json.loads((outroot/'source/symlinks.json').read_text())
summary=json.loads((outroot/'source/summary.json').read_text())
cases=[]
for path in summary['selector_sha256']: cases.append(('selector-bytes',path,'bytes','selector/input bytes drift: '+path))
cases.append(('selector-missing','docs/reviews/slices.json','missing','does not exist'))
config=next(r['path'] for r in rows if r['language']=='kernel-config')
for kind in ['bytes','mode','missing']: cases.append(('source-'+kind,config,kind,'source mode/blob drift'))
for kind in ['bytes','mode','missing']: cases.append(('link-'+kind,links[0]['path'],kind,'source mode/blob drift'))
for kind in ['bytes','mode','missing']: cases.append(('referent-'+kind,links[0]['resolved'],kind,'source mode/blob drift'))
for path in summary['recipe_sha256']: cases.append(('recipe-bytes',path,'bytes','context recipe drift: '+path))
recipe=next(iter(summary['recipe_sha256']))
cases.extend([('recipe-mode',recipe,'mode',recipe),('recipe-missing',recipe,'missing','does not exist')])
results=[]
for n,(label,path,kind,expected) in enumerate(cases,1):
    ident=f'{n:02d}-{label}'
    commit,old,new=make(path,kind)
    dest=P/'fixtures'/ident
    argv=['python3',str(R/'docs/qa-logs/2026-11-02-m6-resume/t43-brief-inputs.py'),'--repo',str(R),'--ref',commit,'--out',str(dest)]
    start=time.monotonic(); started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    x=subprocess.run(argv,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
    (P/'receipts'/f'{ident}.stdout').write_bytes(x.stdout);(P/'receipts'/f'{ident}.stderr').write_bytes(x.stderr)
    ok=x.returncode!=0 and expected.encode() in x.stderr and not dest.exists()
    row={'id':ident,'path':path,'mutation':kind,'commit':commit,'base':BASE,'before':[v.decode() for v in old],'after':None if new is None else [v.decode() for v in new],
         'argv':argv,'expected_diagnostic':expected,'rc':x.returncode,'PASS':ok,'output_absent':not dest.exists(),'started':started,'elapsed_seconds':time.monotonic()-start,
         'cpus':sorted(os.sched_getaffinity(0)),'stdout_sha256':hashlib.sha256(x.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(x.stderr).hexdigest()}
    results.append(row);(P/'receipts'/f'{ident}.json').write_text(json.dumps(row,indent=2)+'\n')
    print(ident, 'PASS' if ok else 'FAIL',flush=True)
    if not ok: print(x.stderr.decode(),flush=True);break
assert head==git('rev-parse','HEAD') and refs==git('show-ref','--head')
(P/'refusal-results.json').write_text(json.dumps({'cases':results,'count':len(results),'pass':sum(x['PASS'] for x in results),'expected':len(cases),'private_refs_unchanged':True,
 'referent_guard_note':'Both referents are selected T43 members; their mutations refuse at the earlier source mode/blob guard, not an independently exercised later referent assertion.'},indent=2)+'\n')
assert len(results)==len(cases) and all(x['PASS'] for x in results)
print('TOTAL',len(results),'PASS; private HEAD/refs unchanged',flush=True)
