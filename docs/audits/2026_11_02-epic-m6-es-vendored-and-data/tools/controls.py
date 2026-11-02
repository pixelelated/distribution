"""T44 new metadata controls. No ES program, compiler, configuration or producer executes."""
import pathlib,sys,json,hashlib,subprocess,datetime,os,copy,importlib.util
sys.dont_write_bytecode=True
A=pathlib.Path(__file__).resolve().parents[1]
def module(name):
    s=importlib.util.spec_from_file_location(name,A/'tools'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(b):return hashlib.sha256(b).hexdigest()
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def mutate(m,case):
    if case=='missing-native':m['coverage'].pop()
    elif case=='gitlink-credit':next(r for r in m['coverage'] if r['kind']=='gitlink')['read_lines']=1
    elif case=='doctest-authorship':next(r for r in m['provenance'] if r['path']=='external/doctest/doctest.h')['fork_written']=True
    elif case=='missing-supplement':m['supplemental'].pop()
    elif case=='missing-companion':m['companions'].pop()
    elif case=='false-integration':m['companions'][0]['integrated']=True
    elif case=='source-drift':m['source_tree']='0'*40
    elif case!='positive':raise ValueError('UNKNOWN_CASE')
def worker(f):
    f=json.loads(pathlib.Path(f).read_bytes());kind=f['kind']
    if kind=='table':
        b=(A/'stage-b/tables.json').read_bytes();assert sha(b)==f['base_sha256'],'FIXTURE_BASE_HASH'
        m=json.loads(b);mutate(m,f['case']);module('tables').validate(m)
    elif kind=='catalogue':
        b=(A/f['path']).read_bytes();assert sha(b)==f['input_sha256'];c=module('catalogue').counts(b)
        assert c==f['expected_counts'],(c,f['expected_counts']);print('PASS PO synthetic counters and escaped backslash')
    elif kind=='confinement':
        module('confinement').validate_paths(f['rows']);print('PASS confinement metadata')
    else:raise ValueError('UNKNOWN_KIND')
def run():
    out=A/'stage-c';out.mkdir(exist_ok=True);fx=out/'fixtures';fx.mkdir(exist_ok=True)
    base_sha=sha((A/'stage-b/tables.json').read_bytes())
    cases=[]
    for case,predicate in [('positive',None),('missing-native','NATIVE_KEYS:coverage'),('gitlink-credit','GITLINK_READ_CREDIT'),('doctest-authorship','DOCTEST_AUTHORSHIP'),('missing-supplement','SUPPLEMENTAL_KEYS'),('missing-companion','COMPANION_KEYS'),('false-integration','COMPANION_INTEGRATION'),('source-drift','SOURCE_IDENTITY')]:
        cases.append(('table-'+case,dict(kind='table',case=case,base_sha256=base_sha),predicate))
    po='msgid ""\nmsgstr "header\\n"\n\n#, fuzzy, c-format\nmsgctxt "menu"\nmsgid "%d item"\nmsgid_plural "%d items"\nmsgstr[0] "un"\nmsgstr[1] ""\n\nmsgid "slash \\\\ end"\nmsgstr "barre"\n\n#~ msgid "obsolete"\n#~ msgstr "ancien"\n'
    counts=dict(entries=2,headers=1,plural=1,context=1,format_flagged=1,fuzzy=1,untranslated=1,obsolete_lines=2)
    for name,s,pred in [('positive',po,None),('missing-msgstr','msgid "x"\n','entry lacks msgid/msgstr'),('duplicate','msgid "x"\nmsgstr "a"\n\nmsgid "x"\nmsgstr "b"\n','duplicate active context/msgid'),('bad-quote','msgid "unfinished\nmsgstr "x"\n','unrecognized PO syntax'),('plural-gap','msgid "x"\nmsgid_plural "xs"\nmsgstr[1] "xs"\n','invalid plural indices')]:
        p=fx/f'po-{name}.txt';p.write_text(s);cases.append(('po-'+name,dict(kind='catalogue',path=str(p.relative_to(A)),input_sha256=sha(p.read_bytes()),expected_counts=counts),pred))
    prefix=module('confinement').AUDIT
    for name,rows,pred in [('positive',[[prefix+'note.md','100644']],None),('source-edit',[['projects/ROCKNIX/packages/ui/emulationstation/package.mk','100644']],'FORBIDDEN_PATH'),('prefix-neighbor',[[prefix.rstrip('/')+'-other/note.md','100644']],'FORBIDDEN_PATH'),('traversal',[[prefix+'../source.cpp','100644']],'NONCANONICAL_PATH'),('symlink',[[prefix+'link','120000']],'NONRECORD_MODE')]:
        cases.append(('guard-'+name,dict(kind='confinement',rows=rows),pred))
    results=[]
    for name,fixture,predicate in cases:
        p=fx/(name+'.json');p.write_text(json.dumps(fixture,indent=2)+'\n');argv=[sys.executable,'-I',str(pathlib.Path(__file__).resolve()),'--case',str(p)]
        start=stamp();r=subprocess.run(argv,capture_output=True,env=dict(os.environ,LC_ALL='C',PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'));end=stamp()
        (out/(name+'.stdout')).write_bytes(r.stdout);(out/(name+'.stderr')).write_bytes(r.stderr)
        ok=r.returncode==0 if predicate is None else r.returncode!=0 and predicate in r.stderr.decode()
        receipt=dict(name=name,argv=argv,start=start,end=end,rc=r.returncode,expected_predicate=predicate,assertion_pass=ok,fixture_sha256=sha(p.read_bytes()),programs={p.name:sha(p.read_bytes()) for p in (A/'tools').glob('*.py')},stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr),python=sys.version,locale='C',cpus=sorted(os.sched_getaffinity(0)))
        (out/(name+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n');results.append(receipt);print(('PASS' if ok else 'FAIL'),name,'rc',r.returncode,'expected',predicate)
    assert all(x['assertion_pass'] for x in results),'CONTROL_FAILURE'
    print('PASS new T44 controls: table positive + 7 independent refusals; PO positive + 4 malformed refusals; confinement positive + 4 refusals')
if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--case':worker(sys.argv[2])
    elif len(sys.argv)==1:run()
    else:raise SystemExit('invalid arguments')
