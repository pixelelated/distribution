"""Verify and retain the five returned metadata packets without executing them."""
import hashlib, json, os, pathlib, stat, datetime

OUT = pathlib.Path(__file__).resolve().parent / 'inputs'
PACKETS = [
    ('p1','/tmp/m6-delivery-manifest-a5d6xpjx','SHA256SUMS','a4a329347f123db2e1ff3496bff49db50e471a12ffd0a4fd1d7b1ee1092f2180'),
    ('t1','/tmp/m6-t1-doctrine-overlap-20261103-nk9mqtnb','MANIFEST.json','d77e2ef859b0a1876c5f2fa9d46dc674337cc73f1ba8e3075158ac9e1cf3cc4b'),
    ('t2','/tmp/m6-es-integration-intersections-0x3gu858','SHA256SUMS','60016e3b16328473f04c8b9d29d45cd930518879dc3f654eb60a5b50bdafabec'),
    ('t3','/tmp/m6-t3-closure-matrix-905z7j9g','final-manifest.json','f9176e19dd33f9f3dc7bbea3391569e407ebf6aa68830e142df553e0d3021281'),
    ('t5','/tmp/m6-integration-source-intersections-t5-20261103','MANIFEST.sha256','61c6a20e1751d8fa969d82a1ac48635d0fc3ce12a3a37799d2d4597abaa62008'),
]

def sha(b):
    return hashlib.sha256(b).hexdigest()

def read(root, name):
    rel=pathlib.PurePosixPath(name)
    assert not rel.is_absolute() and all(p not in ('..','.') for p in rel.parts)
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
    try:
        for part in pathlib.Path(root).parts[1:]+rel.parts[:-1]:
            new=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
            os.close(fd);fd=new
        f=os.open(rel.parts[-1],os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
        with os.fdopen(f,'rb') as stream:
            assert stat.S_ISREG(os.fstat(stream.fileno()).st_mode)
            return stream.read()
    finally:
        os.close(fd)

OUT.mkdir(exist_ok=True)
summary=[]
loaded={}
for lane, root, manifest_name, expected in PACKETS:
    mb=read(root,manifest_name)
    assert sha(mb)==expected,(lane,'manifest')
    if manifest_name.endswith('.json'):
        x=json.loads(mb)['files']
        rows=([dict(path=p,**v) for p,v in x.items()] if isinstance(x,dict) else x)
    else:
        rows=[]
        for line in mb.decode().splitlines():
            digest,name=line.split('  ',1)
            assert len(digest)==64
            rows.append({'path':name,'sha256':digest})
    assert len({x['path'] for x in rows})==len(rows)
    files={}
    for row in rows:
        b=read(root,row['path']);assert sha(b)==row['sha256'],(lane,row['path'])
        if 'bytes' in row:assert len(b)==row['bytes']
        files[row['path']]=b
    loaded[lane]=files
    assert manifest_name not in files
    files[manifest_name]=mb
    archive={'schema':1,'original_root':root,'manifest':manifest_name,'manifest_sha256':expected,
             'encoding':'Each utf8 string encodes original bytes exactly; JSON escapes are storage representation only.',
             'files':[{'path':p,'bytes':len(b),'sha256':sha(b),'utf8':b.decode('utf8')} for p,b in sorted(files.items())]}
    stored=(json.dumps(archive,indent=2,ensure_ascii=True).replace('-','\\u002d')+'\n').encode()
    recovered=json.loads(stored)
    assert all(x['utf8'].encode()==files[x['path']] and sha(x['utf8'].encode())==x['sha256'] for x in recovered['files'])
    (OUT/(lane+'.json')).write_bytes(stored)
    summary.append({'lane':lane,'manifest_sha256':expected,'files_including_manifest':len(files),
                    'logical_bytes':sum(map(len,files.values())),'stored_sha256':sha(stored),'round_trip':'PASS'})

p1=json.loads(loaded['p1']['manifest.json']);assert len(p1['rows'])==46
t1=json.loads(loaded['t1']['report.json']);assert len(t1['source_rows'])==86 and not t1['unresolved_inputs']
t2=json.loads(loaded['t2']['pairwise-intersections.json']);rem=[x for x in t2 if not x['includes_read_only_reference']]
assert len(t2)==66 and len(rem)==55 and sum(x['intersection_count'] for x in rem)==89
t3=json.loads(loaded['t3']['remaining-closure-matrix.json']);assert len(t3['unchecked'])==28 and len(t3['condition_context'])==81
t5=json.loads(loaded['t5']['result/pairwise-intersections.json']);assert len(t5['pair_counts'])==406
result={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','packets':summary,
        'scope':'Original manifest membership/length/hash/ordinary-file custody and reported table populations; no producer execution or new semantic verdict.',
        'counts':{'delivery_rows':46,'doctrine_source_rows':86,'es_remediation_pairs':55,'es_pair_paths':89,
                  'unchecked_criteria':28,'condition_contexts':81,'distribution_pairs_before_T22':406},
        'program_sha256':sha(pathlib.Path(__file__).read_bytes())}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
