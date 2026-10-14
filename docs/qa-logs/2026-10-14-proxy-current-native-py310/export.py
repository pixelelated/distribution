#!/usr/bin/env python3
"""UNRUN exact three hash-bound archives into private scratch; no compiler."""
import hashlib
import os
from pathlib import Path
import sys
import tarfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import read, require, safe_member, sha
WORK=Path('/work/proxy-native');PLAN=Path('/plan')

def main():
    binding=read(PLAN/'input-bindings.json');expected=read(PLAN/'source-files.json')
    root=WORK/'sources';require(not root.exists(),'export already exists')
    root.mkdir();actual={}
    for name,spec in binding['archives'].items():
        archive=Path('/archives')/(name+'.tar.gz')
        require(archive.stat().st_size==spec['archive']['bytes'] and sha(archive)==spec['archive']['sha256'],'archive changed')
        with archive.open('rb') as raw:
            before=os.fstat(raw.fileno())
            digest=hashlib.sha256()
            while block:=raw.read(1024**2):digest.update(block)
            require(digest.hexdigest()==spec['archive']['sha256'],'opened archive changed');raw.seek(0)
            with tarfile.open(fileobj=raw,mode='r:gz') as stream:
                members=stream.getmembers();names=set()
                require(len(members)==spec['members'],'member count changed')
                for m in members:
                    path=safe_member(m.name)
                    require(path.parts[0]==spec['archive_root'] and m.name not in names,'wrong root/duplicate')
                    require((m.isdir() or m.isreg()) and not m.issparse() and not m.linkname and m.mode & ~0o777==0,'special archive member')
                    require(all(ord(c)>=32 and ord(c)!=127 for c in m.name),'control character in path')
                    require(m.size>=0 and (m.isreg() or m.size==0),'invalid member length')
                    if m.isreg():require(m.name in expected and expected[m.name]['bytes']==m.size and expected[m.name]['mode']==m.mode,'member inventory differs')
                    names.add(m.name)
                require(sum(m.size for m in members if m.isreg())==spec['regular_bytes'],'regular bytes differ')
                for m in members:
                    dest=root/safe_member(m.name)
                    require(dest.resolve()==dest and dest.is_relative_to(root),'alias/traversal')
                    if m.isdir():dest.mkdir(parents=True,exist_ok=True);continue
                    dest.parent.mkdir(parents=True,exist_ok=True);remaining=m.size;digest=hashlib.sha256()
                    with stream.extractfile(m) as source,dest.open('xb') as output:
                        while remaining:
                            block=source.read(min(1024**2,remaining));require(block and len(block)<=remaining,'truncated member')
                            output.write(block);digest.update(block);remaining-=len(block)
                        require(source.read(1)==b'','oversized member')
                    dest.chmod(m.mode)
                    actual[m.name]={'sha256':digest.hexdigest(),'bytes':m.size,'mode':m.mode}
                    require(actual[m.name]==expected[m.name],'member bytes changed')
            after=os.fstat(raw.fileno())
            require((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),'opened archive identity changed')
        require(sha(archive)==spec['archive']['sha256'],'archive changed during export')
    require(actual==expected,'complete source inventory differs')
    with (WORK/'source-inventory.json').open('xb') as out:out.write((PLAN/'source-files.json').read_bytes())
    print('Exact current source export: '+str(len(actual))+' files; no native patches')
if __name__=='__main__':main()
