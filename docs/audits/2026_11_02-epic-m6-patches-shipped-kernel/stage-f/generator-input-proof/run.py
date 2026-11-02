#!/usr/bin/env python3
"""D228: four NEW controls; never identify historical fixtures or replay a stage."""
from pathlib import Path
import copy,datetime,hashlib,json,os,stat,subprocess,time,traceback
R=Path('/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688')
A=R/'docs/audits/2026_11_02-epic-m6-patches-shipped-kernel'
P=A/'stage-f/generator-input-proof'
SOURCE='02aab33bd9842610b0d466c9c186454dc14373ee'
CREF='94b5b1c0b983313325dba101217761c6e5c9bca0'
os.chdir(R);os.environ.update(LC_ALL='C',TMPDIR='/workspace/tmp/m6-t41/tmp')
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def dec(s):return s.replace(chr(92)+'u002d','-')
def dump(obj):return (json.dumps(obj,indent=2)+'\n').replace('mask'+'-data0','mask'+chr(92)+'u002ddata0')
def emit(rel,b):
    f=P/rel;f.parent.mkdir(parents=True,exist_ok=True)
    assert not f.exists(),str(f)
    f.write_bytes(b);f.chmod(0o644)
    return dict(path=rel,mode='100644',size_bytes=len(b),sha256=h(b))
assert not P.exists() or not any(P.iterdir()),'refuse existing nonempty proof output'
P.mkdir(parents=True,exist_ok=True)
builder=Path(__file__).read_bytes();emit('run.py',builder)
program=A/'tools/t41-tables.py';baseline=A/'stage-b/corrected/inventory-rows.json'
assert h(program.read_bytes())=='ac6fe1ea48775d0c4c3b285b9b6811c1d12a83ed4ca2414d466ab6490989e558'
runhead=git('rev-parse','HEAD').decode().strip()
assert program.read_bytes()==git('show',CREF+':'+str(program.relative_to(R)))
assert baseline.read_bytes()==git('show',CREF+':'+str(baseline.relative_to(R)))
manifest=dict(schema='t41-final-generator-controls-v1',authority='D-WORKFLOW-228',historical_input_identity='unavailable; new controls only',source_ref=SOURCE,stage_c_ref=CREF,run_head=runhead,program=dict(path=str(program.relative_to(A)),sha256=h(program.read_bytes())),baseline_rows=dict(path=str(baseline.relative_to(A)),sha256=h(baseline.read_bytes())),inputs=[],checks=[],result='INCOMPLETE')
def save(): (P/'manifest.json').write_text(dump(manifest))
save()
try:
    rows=json.loads(baseline.read_bytes());assert len(rows)==107
    identities=[]
    for row in rows:
        path=dec(row['path'])
        assert not Path(path).is_absolute() and '..' not in Path(path).parts
        old=git('ls-tree','-z',SOURCE,'--',path);new=git('ls-tree','-z',runhead,'--',path)
        assert old and old==new,('selected source mode/blob changed',path)
        meta,name=old.rstrip(b'\0').split(b'\t',1);mode,kind,oid=meta.decode().split()
        assert mode=='100644' and kind=='blob' and name.decode()==path
        identities.append(dict(path=path,mode=mode,blob_id=oid))
    emit('source-identities.json',dump(identities).encode())
    drop=copy.deepcopy(rows);drop.pop()
    reach=copy.deepcopy(rows);first=next(i for i,r in enumerate(reach) if r['reach']=='shipped');reach[first]['reach']='test'
    for kind,obj in [('drop',drop),('reach',reach)]:
        rec=emit('fixtures/'+kind+'.json',dump(obj).encode())
        rec['kind']=kind;manifest['inputs'].append(rec)
    eligible=[]
    for path in sorted(dec(r['path']) for r in rows if dec(r['path']).endswith('.patch')):
        b=git('show',SOURCE+':'+path);lines=b.splitlines(keepends=True)
        ids=[i for i,line in enumerate(lines[:60]) if line.startswith(b'From: ')]
        if ids:
            selected=path;original=b;idx=ids[0];break
    assert idx>=0
    lines=original.splitlines(keepends=True)
    lines[idx]=b'X-Proof-From: '+lines[idx][len(b'From: '):]
    mutated=b''.join(lines)
    rec=emit('fixtures/bytes/'+selected,mutated)
    rec.update(kind='header',source_path=selected,baseline_blob_id=git('rev-parse',SOURCE+':'+selected).decode().strip(),baseline_sha256=h(original))
    manifest['inputs'].append(rec)
    overlay=P/'fixtures/bytes'
    assert [x.relative_to(P).as_posix() for x in overlay.rglob('*') if x.is_file()]==[rec['path']]
    assert not any(x.is_symlink() for x in P.rglob('*'))
    assert len(drop)==106 and drop==rows[:-1]
    expected=copy.deepcopy(rows);expected[first]['reach']='test';assert reach==expected
    assert mutated==original.replace(b'From: ',b'X-Proof-From: ',1)
    save()
    expected_errors=dict(drop='AssertionError: membership: expected 107 rows',reach='AssertionError: reach: expected shipped 103/test 4',header='AssertionError: From header census: expected 87')
    for kind in ['drop','reach','header','stats']:
        argv=['python3','-I',str(program),'stats']
        if kind in ['drop','reach']:argv+=['--rows-from',str(P/'fixtures'/(kind+'.json'))]
        if kind=='header':argv+=['--bytes-from',str(overlay)]
        start=stamp();tic=time.monotonic()
        process=subprocess.run(argv,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
        end=stamp();elapsed=round(time.monotonic()-tic,6)
        so='outputs/'+kind+'.stdout';se='outputs/'+kind+'.stderr'
        emit(so,process.stdout);emit(se,process.stderr)
        manifest['checks'].append(dict(kind=kind,argv=argv,cwd=str(R),start=start,end=end,elapsed_seconds=elapsed,rc=process.returncode,stdout=so,stderr=se,stdout_sha256=h(process.stdout),stderr_sha256=h(process.stderr)))
        save();print(kind,'rc',process.returncode,flush=True)
        if kind=='stats':
            assert process.returncode==0 and process.stderr==b''
            assert process.stdout==(A/'stage-c/tables/stats.txt').read_bytes(),'positive stats differ'
        else:
            assert process.returncode==1
            assert process.stderr.decode().splitlines()[-1]==expected_errors[kind]
            assert process.stdout==b''
    manifest['result']='PASS';save()
except BaseException:
    manifest['result']='FAIL';save();raise
files=sorted(p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file())
readme='# New final generator input controls — '+stamp()+'\n\nAuthority: D-WORKFLOW-228, full #688 comment 6586375296 and coordinator 10e055e3043b7bd41f9dcca3e04abce9d979817e, docs/qa-logs/2026-11-02-m6-resume/t41-generator-input-ruling.md.\n\nHistorical Stage-C negative input identities are unavailable; these are new controls only. No old fixture bytes were read or inferred. Accepted formal program, selected source modes/blobs and A–D receipts are unchanged. No application, extraction or whole-stage replay. Actual Codex / GPT-6-Astra / xhigh, T3 wN:p6; observed identity, not provider-attested.\n\nBuilder SHA256: '+h(builder)+'. Producer command: python3 /workspace/tmp/m6-t41/tmp/run-final-control.py, cwd '+str(R)+'. The sealed copy is run.py. It refuses existing nonempty output. Validation consists of run.py deterministic input assertions, all 107 immutable mode/blob comparisons, complete single-file overlay membership and the four exact argv/rc/output assertions in manifest.json. Result: PASS. Negative exits 1/1/1 with the exact required final assertions; positive exit0, empty stderr and stdout byte-equal to retained stage-c/tables/stats.txt. No other generator mode or call ran.\n\nComplete sealed file list (this README included):\n\n'+''.join('- '+x+'\n' for x in sorted(files+['README.md']))+'\nAll manifest artifact paths are relative, with no symlink or parent traversal. Input modes are 100644. Git bytes, not extracted source, supply the single overlay. Future acceptance reconciles these records; it does not rerun this builder.\n'
emit('README.md',readme.encode())
print('D228 four-control proof PASS',flush=True)
