"""Retain the exact named T44 ordinary receipt packet, without executing it."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import stat

SOURCE = Path('/tmp/m6-t44-eh-publication-qhf1l0l6')
DEST = Path(__file__).parent/'t44-final/publication'
sha = lambda b: hashlib.sha256(b).hexdigest()

def read(name):
    parts = PurePosixPath(name).parts
    assert parts and not name.startswith('/') and all(x not in ('.','..') for x in parts)
    fd = os.open(SOURCE, os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            nxt = os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
            os.close(fd);fd=nxt
        item=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
        with os.fdopen(item,'rb') as stream:
            assert stat.S_ISREG(os.fstat(stream.fileno()).st_mode)
            return stream.read()
    finally:
        os.close(fd)

def main():
    manifest=read('SHA256SUMS')
    assert sha(manifest)=='07d40168cb238a2f3fc667766499fab6332965145469d70fbf138e751685a1e0'
    expected={}
    for line in manifest.decode().splitlines():
        m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line);assert m
        digest,path=m.groups();assert path not in expected;expected[path]=digest
    assert len(expected)==135
    expected['SHA256SUMS']=sha(manifest)
    actual=set()
    for folder,dirs,files in os.walk(SOURCE,followlinks=False):
        assert all(not (Path(folder)/d).is_symlink() for d in dirs)
        actual.update(str((Path(folder)/f).relative_to(SOURCE)) for f in files)
    assert actual==set(expected), ('packet key drift',actual^set(expected))
    DEST.mkdir(parents=True,exist_ok=False);(DEST/'objects').mkdir()
    index=[]
    for name,digest in expected.items():
        raw=read(name);assert sha(raw)==digest,name
        raw.decode('utf-8')
        encoded=digest in {'9d285b5b3024d225a3818b4284256d100faa776deb488ae5d30acb65daae2547', 'f6f5167b1476ca4d5008902bf47671b14141c3b33d4a435af151094cc0be1fd4', 'fd31702886aad207a6b638c253068cc85b2754e955ff289bccfd81b3e0d698de'}
        target=DEST/'objects'/(digest+('.json' if encoded else ''))
        stored=(json.dumps({'encoding':'utf8-json','raw':raw.decode(),'sha256':digest,'bytes':len(raw)},indent=2)+'\n').encode() if encoded else raw
        if target.exists():assert target.read_bytes()==stored
        else:target.write_bytes(stored)
        index.append({'path':name,'bytes':len(raw),'sha256':digest,'stored':'objects/'+target.name, 'encoding':'utf8-json' if encoded else 'raw'})
    report={'source':str(SOURCE),'manifest_sha256':sha(manifest),'files':len(index),
            'bytes':sum(x['bytes'] for x in index),'entries':index,'scope':'ordinary record files only; no producer execution'}
    (DEST/'index.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='entries'}))

if __name__=='__main__':main()
