"""D228 supplemental-proof consumer. Git/record reads only; never invoke a producer.
Codex (GPT-6), /root, wN:p5, session 01a19d12-1c5f-7022-8053-102f6a94b7fe.
Historical negative inputs remain unavailable; new controls cannot identify them.
"""
import copy, datetime as DT, math, base64
PROOF_AUTH='10e055e3043b7bd41f9dcca3e04abce9d979817e'
PROOF_SCHEMA='t41-final-generator-controls-v1'
PROOF_PROGRAM_SHA='ac6fe1ea48775d0c4c3b285b9b6811c1d12a83ed4ca2414d466ab6490989e558'
STAGE_D='c9fe606e8d7e7e0f6c70cc686764d1503029d278'
PROOF_ROOT='stage-f/generator-input-proof'

def proof_relative(value):
    need(isinstance(value,str),'D228 artifact path must be text')
    p=dec(value);q=P.PurePosixPath(p)
    need(p and '\x00' not in p and '\\' not in p and not q.is_absolute() and '..' not in q.parts and str(q)==p and p!='.','D228 unsafe relative artifact path')
    return p

def proof_json(raw):
    def pairs(items):
        obj={}
        for k,v in items:
            need(k not in obj,'D228 duplicate JSON key');obj[k]=v
        return obj
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _: (_ for _ in ()).throw(Invalid('D228 nonfinite JSON number')))

def proof_utc(value):
    need(isinstance(value,str) and bool(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|\+00:00)',value)),'D228 timestamp must be explicit UTC')
    return DT.datetime.fromisoformat(value.replace('Z','+00:00'))

def supplemental_generator(r,historical,retained=True):
    """Only this supplement may close the failed historical input-binding predicate."""
    root=r.af+'/'+PROOF_ROOT
    # Manifest absence is an honest future-artifact ABSENT. After it exists, a
    # missing fixture/output is a malformed proof and FAIL, never a partial PASS.
    try:raw_manifest=r.audit(PROOF_ROOT+'/manifest.json')
    except Absent:raise Absent('D228 supplemental manifest absent; historical negative input identities remain unavailable')
    manifest=proof_json(raw_manifest);need(isinstance(manifest,dict),'D228 manifest must be an object')
    need(manifest['schema']==PROOF_SCHEMA and manifest['authority']=='D-WORKFLOW-228','D228 schema/authority differs')
    need(manifest['historical_input_identity']=='unavailable; new controls only','D228 must preserve the historical unknown')
    need(manifest['source_ref']==SOURCE and manifest['stage_c_ref']==STAGE_C,'D228 source/Stage-C ref differs')
    need(manifest['result']=='PASS','D228 producer did not assert a completed PASS')
    run_head=manifest['run_head'];need(isinstance(run_head,str) and re.fullmatch('[0-9a-f]{40}',run_head),'D228 run_head must be a full commit')
    need(r.git('cat-file','-t',run_head).strip()==b'commit','D228 run_head is not a commit')
    need(r.git('merge-base','--is-ancestor',run_head,r.tip,missing=True) is not None,'D228 run_head is not an ancestor of candidate')
    listing=r.tree(r.tip,root+'/')
    need(root+'/manifest.json' in listing,'D228 manifest is not committed at candidate tip')
    for path,entry in listing.items():
        proof_relative(path[len(root)+1:]);need(entry.split()[0] in ['100644','100755'] and entry.split()[1]=='blob','D228 proof contains a symlink or nonregular artifact')
    def read(path):
        path=proof_relative(path);full=root+'/'+path
        need(full in listing,'D228 missing committed proof artifact: '+fmt(path))
        try:b=r.blob(full)
        except Absent:raise Invalid('D228 missing proof artifact: '+fmt(path))
        return b
    need(read('manifest.json')==raw_manifest,'D228 manifest read differs from committed bytes')
    # The new packet supplements the immutable historical packet, never edits it.
    for stage in ['stage-a','stage-b','stage-c','stage-d']:
        p=r.af+'/'+stage+'/'
        expected=r.tree(STAGE_D,p)
        need(bool(expected) and r.tree(r.tip,p)==expected,'D228 accepted '+stage+' modes/blobs changed or absent')
    program=manifest['program'];rows_record=manifest['baseline_rows']
    need(proof_relative(program['path'])=='tools/t41-tables.py','D228 program path differs')
    need(proof_relative(rows_record['path'])=='stage-b/corrected/inventory-rows.json','D228 baseline rows path differs')
    program_path=r.af+'/'+proof_relative(program['path']);rows_path=r.af+'/'+proof_relative(rows_record['path'])
    pb=unchanged(r,program_path,STAGE_C);rb=unchanged(r,rows_path,STAGE_C)
    need(program['sha256']==PROOF_PROGRAM_SHA==sha(pb),'D228 exact accepted formal program hash differs')
    need(rows_record['sha256']==sha(rb),'D228 baseline rows hash differs')
    for path in [program_path,rows_path]:
        need(r.tree(run_head,path)==r.tree(r.tip,path),'D228 program/baseline differs at recorded run_head')
    base=proof_json(rb);need(isinstance(base,list) and len(base)==107,'D228 baseline is not 107 rows')
    selected=[proof_relative(x['path']) for x in base]
    need(len(set(selected))==107,'D228 duplicate selected source path')
    need(set(selected)=={dec(x['path']) for x in r.inventory()},'D228 baseline membership differs')
    source_tree=r.tree(SOURCE,'');final_tree=r.tree(r.tip,'');run_tree=r.tree(run_head,'')
    for p in selected:
        need(p in source_tree and source_tree[p].split()[0] in ['100644','100755'] and source_tree[p].split()[1]=='blob','D228 selected source is not a regular blob')
        need(source_tree[p]==final_tree.get(p)==run_tree.get(p),'D228 selected source mode/blob drift: '+fmt(p))
    # Lexicographic selection and the first-60-lines rule are computed from immutable
    # bytes. No filesystem source tree and no historical negative bytes are read.
    eligible=[]
    for p in sorted(selected):
        if not p.endswith('.patch'):continue
        data=r.blob(p,SOURCE);parts=data.splitlines(keepends=True)
        indices=[i for i,line in enumerate(parts[:60]) if line.startswith(b'From: ')]
        if indices:eligible.append((p,data,parts,indices[0]))
    need(bool(eligible),'D228 no eligible header source')
    hp,hb,parts,first=eligible[0];changed=list(parts);changed[first]=b'X-Proof-From: '+changed[first][len(b'From: '):]
    expected_header=b''.join(changed)
    mutations={'drop':base[:-1],'reach':copy.deepcopy(base)}
    shipped=next((i for i,x in enumerate(base) if x.get('reach')=='shipped'),None)
    need(shipped is not None,'D228 baseline has no shipped row');mutations['reach'][shipped]['reach']='test'
    records=manifest['inputs'];need(isinstance(records,list) and len(records)==3 and all(isinstance(x,dict) for x in records),'D228 requires exactly three inputs')
    need([x.get('kind') for x in records].count('drop')==1 and {x.get('kind') for x in records}=={'drop','reach','header'},'D228 input kinds duplicated or missing')
    inputs={x['kind']:x for x in records};input_paths={}
    for kind,expected_path in [('drop','fixtures/drop.json'),('reach','fixtures/reach.json'),('header','fixtures/bytes/'+hp)]:
        entry=inputs[kind];path=proof_relative(entry['path']);need(path==expected_path,'D228 wrong '+kind+' input path')
        data=read(path);input_paths[kind]=path
        need(entry['mode']=='100644' and listing[root+'/'+path].split()[0]=='100644' and type(entry['size_bytes']) is int and entry['size_bytes']==len(data),'D228 input mode/size differs')
        need(isinstance(entry['sha256'],str) and entry['sha256']==sha(data),'D228 input hash differs')
        if kind in mutations:
            # JSON Unicode escapes are syntax; only the known filename escape is
            # normalized semantically. Every non-path field and row order is exact.
            actual=proof_json(data);wanted=copy.deepcopy(mutations[kind])
            need(isinstance(actual,list) and all(isinstance(x,dict) for x in actual),'D228 mutated rows must be objects')
            for rows in [actual,wanted]:
                for row in rows:row['path']=proof_relative(row['path'])
            need(json.dumps(actual,sort_keys=True,ensure_ascii=False)==json.dumps(wanted,sort_keys=True,ensure_ascii=False),'D228 deterministic '+kind+' mutation differs')
        else:
            need(proof_relative(entry['source_path'])==hp,'D228 header selected a different source')
            need(entry['source_path']==hp,'D228 header source_path must be decoded')
            need(entry['baseline_blob_id']==source_tree[hp].split()[2] and re.fullmatch('[0-9a-f]{40}',entry['baseline_blob_id']),'D228 header baseline blob id differs')
            need(entry['baseline_sha256']==sha(hb),'D228 header baseline hash differs')
            need(data==expected_header,'D228 header mutation changed more than the first From prefix')
    fixture_files={p[len(root)+1:] for p in listing if p.startswith(root+'/fixtures/')}
    need(fixture_files==set(input_paths.values()),'D228 missing or extra fixture/overlay file')
    overlay={p for p in fixture_files if p.startswith('fixtures/bytes/')}
    need(overlay=={'fixtures/bytes/'+hp},'D228 overlay is not exactly the selected one regular file')
    checks=manifest['checks'];need(isinstance(checks,list) and all(isinstance(x,dict) for x in checks) and [x.get('kind') for x in checks]==['drop','reach','header','stats'],'D228 requires ordered drop/reach/header/stats commands only')
    assertions={'drop':'AssertionError: membership: expected 107 rows','reach':'AssertionError: reach: expected shipped 103/test 4','header':'AssertionError: From header census: expected 87'}
    outputs=[];previous=None;cwd_seen=None
    historical_end=max(proof_utc(x['start']) for x in historical['checks'] if x.get('name','').startswith('formal-generator-'))
    for x in checks:
        kind=x['kind'];argv=x['argv'];cwd=x['cwd']
        need(isinstance(cwd,str) and P.PurePosixPath(cwd).is_absolute() and str(P.PurePosixPath(cwd))==cwd and '..' not in P.PurePosixPath(cwd).parts and '\\' not in cwd and '\x00' not in cwd,'D228 unsafe command cwd')
        if cwd_seen is None:cwd_seen=cwd
        need(cwd==cwd_seen,'D228 commands changed cwd')
        def arg_path(a,expected):
            need(isinstance(a,str),'D228 command path must be text')
            a=dec(a);need(a in [expected,cwd.rstrip('/')+'/'+expected],'D228 command does not address the bound artifact')
        need(isinstance(argv,list) and len(argv)==(4 if kind=='stats' else 6) and argv[:2]==['python3','-I'] and argv[3]=='stats','D228 command shape differs')
        arg_path(argv[2],program_path)
        if kind!='stats':
            need(argv[4]==('--bytes-from' if kind=='header' else '--rows-from'),'D228 wrong negative input flag')
            arg_path(argv[5],root+'/'+('fixtures/bytes' if kind=='header' else input_paths[kind]))
        start,end=proof_utc(x['start']),proof_utc(x['end']);elapsed=x['elapsed_seconds']
        need(start>historical_end and end>=start and (previous is None or start>=previous),'D228 controls not dated as new ordered checks')
        need(type(elapsed) in [float,int] and math.isfinite(elapsed) and elapsed>=0,'D228 elapsed time invalid');previous=end
        out_path,err_path=proof_relative(x['stdout']),proof_relative(x['stderr']);outputs += [out_path,err_path]
        out,err=read(out_path),read(err_path)
        need(x['stdout_sha256']==sha(out) and x['stderr_sha256']==sha(err),'D228 raw output hash differs')
        need(type(x['rc']) is int and x['rc']==(0 if kind=='stats' else 1),'D228 command rc differs')
        if kind=='stats':need(err==b'' and out==r.audit('stage-c/tables/stats.txt'),'D228 positive is not exact Stage-C stats/empty stderr')
        else:
            # An uncaught Python AssertionError is the final stderr line. Treat a
            # stdout claim alone as insufficient; it could be printed by any code.
            need(err.decode().splitlines()[-1:]==[assertions[kind]],'D228 negative final assertion differs')
    need(len(set(outputs))==8 and not (set(outputs)&set(input_paths.values())),'D228 output paths reused or alias an input')
    need(not set(outputs)&{'manifest.json','run.py','README','README.md'},'D228 output aliases metadata/builder')
    builder=read('run.py');readmes=[p for p in ['README','README.md'] if root+'/'+p in listing]
    need(len(readmes)==1,'D228 exactly one README required');readme=dec(read(readmes[0]).decode())
    need(sha(builder) in readme,'D228 README does not bind exact builder SHA')
    need(all(p in readme for p in list(input_paths.values())+outputs+['run.py','manifest.json']),'D228 README input/output file list incomplete')
    need(any(t in readme for t in ['python3','sha256sum','git ']),'D228 README validation commands absent')
    allowed={root+'/'+input_paths['header']:listing[root+'/'+input_paths['header']]}
    if retained:allowed.update(retained_generator_attempt(r,historical,manifest,listing))
    r.d228_headers=allowed
    return 'D226 historical Stage-C program/outputs reconciled; original negative inputs remain unavailable. D228 new sealed drop/reach/header refusals plus stats positive verified; no producer invoked'


def retained_generator_attempt(r,historical,current,current_listing):
    """Losslessly reconstruct only the TWO committed base64 input streams in memory.
    Reuse every supplemental predicate on a virtual view of the first attempt.
    No scratch path in its error record is ever accessed, and no builder executes.
    """
    canonical=r.af+'/'+PROOF_ROOT;attempt=canonical+'-attempt-1'
    listing=r.tree(r.tip,attempt+'/')
    if not listing:return {}
    def read(p):
        full=attempt+'/'+proof_relative(p)
        need(full in listing and listing[full].split()[:2]==['100644','blob'],'D228 retained artifact absent/nonregular: '+fmt(p))
        return r.blob(full)
    old=proof_json(read('manifest.json'));error=proof_json(read('serialization-error.json'))
    need(error['result']=='generator controls passed; publication hygiene failed','D228 retained failure disposition differs')
    when=proof_utc(error['timestamp'])
    need(proof_utc(old['checks'][-1]['end'])<when<proof_utc(current['checks'][0]['start']),'D228 retained failure/correction time order differs')
    for key in ['schema','authority','historical_input_identity','source_ref','stage_c_ref','run_head','program','baseline_rows','result']:
        need(old[key]==current[key],'D228 retained attempt identity differs: '+key)
    old_inputs={x['kind']:x for x in old['inputs']};new_inputs={x['kind']:x for x in current['inputs']}
    need(old_inputs['header']==new_inputs['header'],'D228 retained header source/identity differs')
    hp=proof_relative(new_inputs['header']['path'])
    need(read(hp)==r.blob(canonical+'/'+hp),'D228 retained header bytes differ')
    identities=read('source-identities.json')
    need(identities==r.blob(canonical+'/source-identities.json'),'D228 retained source identities differ')
    expected=[];source_entries=r.tree(SOURCE,'')
    for path in sorted(dec(x['path']) for x in r.inventory()):
        entry=source_entries[path].split();expected.append(dict(path=path,mode=entry[0],blob_id=entry[2]))
    need(proof_json(identities)==expected,'D228 retained source identity census differs')
    encoded=error['encoded_original_files']
    need(isinstance(encoded,list) and len(encoded)==2 and [x['original_path'] for x in encoded]==['fixtures/drop.json','fixtures/reach.json'],'D228 retained encoding manifest differs')
    virtual={}
    for x,kind in zip(encoded,['drop','reach']):
        path=x['original_path'];stored=path+'.base64'
        need(x['stored_path']==stored and x['encoding']=='base64; exact original bytes, not a rewritten input','D228 retained encoding path/type differs')
        raw=read(stored)
        try:decoded=base64.b64decode(b''.join(raw.split()),validate=True)
        except ValueError:raise Invalid('D228 retained input invalid base64')
        entry=old_inputs[kind]
        need(entry['path']==path and type(x['size_bytes']) is int and x['size_bytes']==len(decoded)==entry['size_bytes'] and x['sha256']==sha(decoded)==entry['sha256'],'D228 retained input identity differs')
        # Only the known filename serialization is different; no semantic rewrite.
        newer=r.blob(canonical+'/'+path)
        need(newer.replace(b'\\u002d',b'-')==decoded,'D228 retained input is not the exact serialization-only predecessor')
        virtual[canonical+'/'+path]=decoded
    before=read('run.py');after=r.blob(canonical+'/run.py')
    old_line=br"        rec=emit('fixtures/'+kind+'.json',(json.dumps(obj,indent=2)+'\n').encode())"
    new_line=b"        rec=emit('fixtures/'+kind+'.json',dump(obj).encode())"
    need(before.count(old_line)==1 and before.replace(old_line,new_line)==after,'D228 retained builder change is not the exact serialization correction')
    class AttemptView:
        def __init__(self):self.tip=r.tip;self.af=r.af
        def __getattr__(self,name):return getattr(r,name)
        def blob(self,path,ref=None):
            if (ref is None or ref==r.tip) and path.startswith(canonical+'/'):
                if path in virtual:return virtual[path]
                return read(path[len(canonical)+1:])
            return r.blob(path,ref)
        def audit(self,path):return self.blob(self.af+'/'+path)
        def tree(self,ref,path):
            if ref==r.tip and path.startswith(canonical+'/'):
                out={}
                for p,entry in listing.items():
                    q=canonical+p[len(attempt):]
                    if q.endswith('.json.base64'):q=q[:-7]
                    if q in virtual:
                        b=virtual[q];entry='100644 blob '+hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
                    if q==path or q.startswith(path.rstrip('/')+'/'):out[q]=entry
                return out
            return r.tree(ref,path)
    supplemental_generator(AttemptView(),historical,retained=False)
    return {attempt+'/'+hp:listing[attempt+'/'+hp]}


def d228_overlay_paths(r):
    if not hasattr(r,'d228_headers'):reconcile_generator(r)
    return r.d228_headers
