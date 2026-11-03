#!/usr/bin/env python3
"""Retain only the five new manifest-bound continuation packets; no producer replay."""
import datetime, hashlib, json, os, pathlib, stat
OUT=pathlib.Path(__file__).resolve().parent/'continuation-inputs'
PACKETS=[
 ('p1','/tmp/m6-p1-endpoints-4mw3hvmb','SHA256SUMS','237e7a72ed5fc3b8fc08d1e9a8ada6603f3fadd57686720b39495d18d9a611b6'),
 ('t1','/tmp/m6-t1-doctrine-hunks-20261103-aayfw062','MANIFEST.json','2af0c87a15a142e1c6ffc7016853e7b4875771be48681653ca2146ca1c0e8cc7'),
 ('t2','/tmp/m6-es-textual-intersections-caz3od3g','SHA256SUMS','f21a8a3fce0b7e6548fa1cfd728ecbe82742de29ff32a8e90a96f9c36bae7e25'),
 ('t3','/tmp/m6-t3-m7-boundary-20261103-5ddz45ub','MANIFEST.json','00eb4aa2a6fe31863cf34cf4581aa5631d70f6e33a964f1cc952b4450bae7b15'),
 ('t5','/tmp/m6-integration-hunk-inputs-t5-20261103','MANIFEST.sha256','1b888e607e2ac567db632c60d64f53a0f2c9cf13e3dd6b8f407603d1b1169671')]
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

OUT.mkdir(exist_ok=False)
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

result={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','packets':summary,
'scope':'Named continuation packet hashes, lengths, regular files and lossless storage round trip only; no source, producer or semantic re-review.',
'program_sha256':sha(pathlib.Path(__file__).read_bytes())}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
