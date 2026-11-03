"""Read-only T46 completion reconciliation. No accepted producer is executed."""
import base64, datetime as dt, hashlib, json, os, pathlib, runpy, stat, subprocess, tempfile

R = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
TIP = 'df8058e4353c54b73d4eea4d356ce18df901aabf'
BASE = '17a064e6110306dd2b692cfd1b13d4f518d8def5'
COORD = 'e4dacd1812213da2c09e67e3a277121f3af8dd43'
A = 'docs/audits/2026_11_03-epic-m6-records/'
C = A + 'completion/'
LANE = '/workspace/repos/pixelelated/distribution.worktrees/m6-records-693/'
EXT = pathlib.Path('/tmp/m6-t46-completion-publication-0f2ysrpp')
checks, differences, commands = [], [], []
cache = {}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()

def check(label, actual, expected=True):
    assert actual == expected, (label, actual, expected)
    checks.append(label)

def git(*argv):
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    run = subprocess.run(['git', *argv], cwd=R, capture_output=True)
    commands.append({'argv':['git', *argv], 'cwd':str(R), 'start':start,
                     'end':dt.datetime.now(dt.timezone.utc).isoformat(), 'rc':run.returncode,
                     'stdout_sha256':sha(run.stdout), 'stderr_sha256':sha(run.stderr)})
    assert run.returncode == 0, (argv, run.stderr.decode())
    return run.stdout

def blob(path, ref=TIP):
    key = (ref, path)
    if key not in cache:
        cache[key] = git('show', ref + ':' + path)
    return cache[key]

def tree(ref):
    result = {}
    for row in git('ls-tree', '-rlz', ref, '--', A).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, kind, oid, size = meta.decode().split()
            result[path.decode()] = {'mode':mode, 'type':kind, 'oid':oid, 'bytes':int(size)}
    return result

def safe_read(rel):
    p = pathlib.PurePosixPath(rel)
    assert not p.is_absolute() and p.parts and all(x not in ('..', '.') for x in p.parts)
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in EXT.parts[1:] + p.parts[:-1]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        f = os.open(p.parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
        with os.fdopen(f, 'rb') as stream:
            check('ordinary external ' + rel, stat.S_ISREG(os.fstat(stream.fileno()).st_mode))
            return stream.read()
    finally:
        os.close(fd)

def decode(b, label):
    x = json.loads(b)
    data = base64.b64decode(x['base64'], validate=True)
    check(label + ' length', len(data), x['bytes'])
    check(label + ' digest', sha(data), x['sha256'])
    return x, data

check('direct child', git('show', '-s', '--format=%P', TIP).decode().strip(), BASE)
old, current = tree(BASE), tree(TIP)
check('accepted audit population', len(old), 976)
check('accepted audit mode/type/blob/size unchanged', {p:current.get(p) for p in old}, old)
readme = blob('docs/audits/README.md')
check('README bytes', len(readme), 813)
check('README hash', sha(readme), '410e4432c01a38cda578a68fdaa730129c15a8e3e60c7305001bb40bd5a71b6c')
check('README unchanged', readme, blob('docs/audits/README.md', BASE))
exact = {A+'audit-completion.json', '.github/sessions/saved-session-state-feature-m6-records-693.md',
         'docs/work-logs/2026_11-work_logs/2026_11_03-work_log.md', 'docs/work-logs/INDEX.md'}
parts = git('diff', '--raw', '--no-abbrev', '--no-renames', '-z', BASE, TIP).split(b'\0')
changed = []
for i in range(0, len(parts)-1, 2):
    meta, path = parts[i].decode().split(), parts[i+1].decode()
    check('allowed diff ' + path, meta[-1] in ('A','M') and meta[1]=='100644' and (path in exact or path.startswith(C)))
    changed.append(path)
check('completion diff population', len(changed), 226)
marker_bytes = blob(A+'audit-completion.json')
check('marker hash', sha(marker_bytes), '03bed5910a7f6cac95adb57a1379053e873f4c897f700aee38989fe159ec45e3')
marker = json.loads(marker_bytes)
for path, digest in marker['evidence'].items():
    check('marker evidence ' + path, sha(blob(path)), digest)
check('marker evidence count', len(marker['evidence']), 14)
coordinator = json.loads(blob(C+'coordinator-inputs.json'))
check('coordinator input count', len(coordinator), 7)
for row in coordinator:
    check('coordinator pin ' + row['source_path'], row['source_commit'], COORD)
    src, dst = blob(row['source_path'], COORD), blob(row['retained_path'])
    check('coordinator copied bytes ' + row['source_path'], dst, src)
    check('coordinator digest ' + row['source_path'], sha(dst), row['sha256'])
    check('coordinator size ' + row['source_path'], len(dst), row['bytes'])
    check('coordinator tree identity ' + row['source_path'], git('ls-tree', COORD, '--', row['source_path']).decode().strip(), row['ls_tree'])

# Invoke only the existing schema validator, on the selected documentary evidence.
with tempfile.TemporaryDirectory(prefix='m6-t46-marker-selected-') as selected:
    root = pathlib.Path(selected)
    for p in [A+'audit-completion.json', *marker['evidence']]:
        dest = root/p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(blob(p))
    api = runpy.run_path(str(R/'tools/ceremony-check'), run_name='completion_reader')
    ended, issue = api['completed_audit_marker'](root/A/'audit-completion.json', root, dt.datetime.now(dt.timezone.utc))
    check('existing schema validator issue', issue, 1417)
    check('existing schema validator timestamp', ended.isoformat(), marker['completed_at'])

manifest_bytes = safe_read('publication-manifest.json')
check('publication manifest hash', sha(manifest_bytes), 'cba07bd7788c0b8887e20edb515f7c16b8e591aecec250f11686d2f31eb745d6')
manifest = json.loads(manifest_bytes)
check('publication count', len(manifest['files']), 77)
check('publication key uniqueness', len({x['path'] for x in manifest['files']}), 77)
check('publication canonical manifest', sha(canonical(manifest['files'])), manifest['file_manifest_sha256'])
external = {}
for row in manifest['files']:
    b = safe_read(row['path']); external[row['path']] = b
    check('external length ' + row['path'], len(b), row['bytes'])
    check('external hash ' + row['path'], sha(b), row['sha256'])
check('external total bytes', sum(map(len,external.values())), 1752033)
scan = json.loads(external['final-scan/manifest.json'])
rows, chunks = [], []
for p in sorted(changed):
    b = blob(p)
    rows.append({'path':p,'mode':'100644','bytes':len(b),'sha256':sha(b),
                 'blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
    chunks.append((p+'\n').encode()+b+b'\n')
check('exact final scan file rows', rows, scan['files'])
check('exact final scan bytes', sum(x['bytes'] for x in rows), 4565297)
check('exact final scan manifest digest', sha(canonical(rows)), scan['file_manifest_sha256'])
check('exact final scan stdin digest', sha(b''.join(chunks)), scan['stdin_sha256'])
check('frozen metadata digest', sha(canonical(old)), scan['frozen_manifest_sha256'])
check('scan driver identity', sha(blob(C+'compare.py')), scan['driver_sha256'])
check('scanner identity', sha(blob('tools/forbidden-terms-check')), scan['scanner_sha256'])
check('scan retained exit', scan['rc'], 0)
for label in ['stdout','stderr']:
    _, data = decode(external['final-scan/'+label+'.json'], 'scan '+label)
    check('scan stream '+label, sha(data), scan[label+'_sha256'])

receipts, input_count = [], 0
recorder = sha(blob(C+'record.py'))
for origin, paths, read in [
    ('committed', sorted(p for p in current if p.startswith(C) and p.endswith('/receipt.json')), blob),
    ('external', sorted(p for p in external if p.endswith('/receipt.json')), lambda p:external[p])]:
    for p in paths:
        rec=json.loads(read(p)); prefix=p.rsplit('/',1)[0]+'/'
        check('recorder '+p, rec['recorder_sha256'], recorder)
        check('command chronology '+p, rec['start'] <= rec['end'])
        check('CPU scope '+p, rec['cpu_affinity'], list(range(8,24)))
        for label in ['stdout','stderr']:
            _, data=decode(read(prefix+label+'.json'), p+' '+label)
            check('receipt stream '+p+' '+label, sha(data), rec[label+'_sha256'])
        for i, declared in enumerate(rec['inputs']):
            x, data=decode(read(prefix+'input-'+str(i)+'.json'), p+' input'+str(i))
            check('input declaration '+p+' '+str(i), {k:v for k,v in x.items() if k!='base64'}, declared)
            input_count += 1
            if x['path'].startswith(LANE):
                relative=x['path'][len(LANE):]
                final=blob(relative)
                if final!=data:
                    differences.append({'receipt':p,'input':relative,'historical_sha256':sha(data),'final_sha256':sha(final),'historical_bytes':len(data),'final_bytes':len(final)})
        receipts.append({'origin':origin,'path':p,'argv':rec['argv'],'rc':rec['rc']})
check('completion receipt exits', all(x['rc']==0 for x in receipts))
for name in ['normal-resolution','issue-resolution']:
    rec=json.loads(blob(C+'gates/'+name+'/receipt.json'))
    for rel in ['04-analysis.md','05-punch-list.md']:
        hit=[x for x in rec['inputs'] if x['path']==LANE+A+rel]
        check(name+' final '+rel, len(hit)==1 and hit[0]['sha256']==sha(blob(A+rel)))

live=json.loads((OUT/'tracker-inputs.json').read_bytes())
for issue in live['issues']:
    n=issue['issue_number']; retained=json.loads(blob(C+'tracker-'+str(n)+'.json'))
    for key in ['body','state','state_reason','closed_at']:
        check('live tracker '+str(n)+' '+key, issue.get(key), retained.get(key))
for label, expected in [('tip',TIP+'\n'+BASE+'\nrecords: record accepted T46 audit completion\n'),('clean','')]:
    _, raw=decode(external[label+'/stdout.json'], label+' stdout')
    check('publication '+label, raw.decode(), expected)
_, remote=decode(external['remote/stdout.json'], 'remote stdout')
check('publication remote', remote.decode().split(), [TIP,'refs/heads/feature/m6-records-693'])
checkpoint=safe_read('checkpoint-readback.json'); cp=json.loads(checkpoint)
for stream in ['stdout','stderr']:
    check('checkpoint '+stream+' digest', sha(base64.b64decode(cp[stream+'_base64'],validate=True)), cp[stream+'_sha256'])
cp_raw=json.loads(base64.b64decode(cp['stdout_base64'],validate=True))
check('checkpoint actual exit', cp['rc'], 0)
check('checkpoint actual full body', sha(cp_raw['body'].encode()), 'bfef172ee58781631dbe90deaa0f110eb1ee674795f059ea478119a16a77d54a')
check('checkpoint live body', [x['body'] for x in live['comments'] if x['id']==6606526044], [cp_raw['body']])
for n in [6605921275,6605965227]:
    check('authority present '+str(n), any(x['id']==n and x['body'] for x in live['comments']))

result={'verified_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'result':'PASS',
        'completion_tip':TIP,'accepted_final':BASE,'marker_sha256':sha(marker_bytes),
        'checks':checks,'input_snapshots':input_count,'input_version_differences':differences,
        'receipts':receipts,'commands':commands,'program_sha256':sha(pathlib.Path(__file__).read_bytes()),
        'limits':['Retained producer receipts reconciled, not replayed. Existing marker validator only.',
                  'Source integration and slice closure remain pending. H roots were not read or cleaned.',
                  'Two initial root path guesses were absent (completion/RESULT.md and gates/ceremony/receipt.json); reads corrected from ls-tree, no producer failure.',
                  'Initial root reader expected rev-parse output for tip; actual recorded git show includes parent and subject. It refused before retention; original reader preserved as reader-attempt-1.utf8.json. Corrected exact output check covers all three lines.']}
(OUT/'verification.json').write_text(json.dumps(result,indent=2).replace('-','\\u002d')+'\n')
# Preserve only this authorized ordinary publication packet, losslessly, not historical roots.
retained=[]; dest=OUT/'publication'; dest.mkdir(exist_ok=True)
for i,(name,b) in enumerate(sorted({**external,'publication-manifest.json':manifest_bytes,'checkpoint-readback.json':checkpoint}.items())):
    target=dest/(f'{i:03d}.utf8.json'); stored=(json.dumps(b.decode('utf8'),ensure_ascii=True).replace('-','\\u002d')+'\n').encode()
    target.write_bytes(stored); check('retention round trip '+name, json.loads(stored).encode(), b)
    retained.append({'original_path':str(EXT/name),'stored_path':str(target.relative_to(R)),'bytes':len(b),'sha256':sha(b),'stored_sha256':sha(stored)})
(dest/'retention.json').write_text(json.dumps({'schema':1,'encoding':'JSON string -> UTF8 bytes; hyphen escapes are storage only','files':retained},indent=2).replace('-','\\u002d')+'\n')
print(json.dumps({'result':'PASS','checks':len(checks),'receipt_groups':len(receipts),'input_snapshots':input_count,'differences':differences,'retained_files':len(retained)},indent=2))
