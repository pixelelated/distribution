#!/usr/bin/env python3
"""UNRUN: exact pinned archive to private scratch; regular files/directories; omit two exact zstd test aliases."""
import hashlib
import os
from pathlib import Path
import sys
import tarfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import command, read, require, safe_member, sha, write

WORK=Path('/work/format-tools'); RECORDS=Path('/receipts'); PLAN=Path('/plan')
ARCHIVE=Path('/mame-source.tar.gz')
OMITTED_TEST_ALIASES={
    '3rdparty/zstd/tests/cli-tests/bin/unzstd': 'zstd',
    '3rdparty/zstd/tests/cli-tests/bin/zstdcat': 'zstd',
}


def main():
    spec=read(PLAN/'input-bindings.json')['chdman'];archive=spec['archive']
    require(archive['bytes']==213471628 and archive['sha256']==
            '4867bee5dbd4129e6eea095fe8f8e9725563998710cc9620190e90529ef8931b','wrong archive binding')
    root=WORK/spec['archive_root'];require(not root.exists() and not root.is_symlink(),'export already exists')
    require(ARCHIVE.stat().st_size==archive['bytes'] and sha(ARCHIVE)==archive['sha256'],'archive size/hash changed')
    # Inspect all headers from the hash-bound archive BEFORE writing source files.
    # No tar extract/extractall, stored links, devices, sparse files or path rewriting.
    with ARCHIVE.open('rb') as raw:
        before=os.fstat(raw.fileno())
        digest=hashlib.sha256()
        while chunk:=raw.read(1024**2):digest.update(chunk)
        require(digest.hexdigest()==archive['sha256'],'opened archive identity/hash differs')
        raw.seek(0)
        with tarfile.open(fileobj=raw,mode='r:gz') as archive_stream:
            members=archive_stream.getmembers()
            require(len(members)==spec['members']==33835,'archive member count differs')
            names=set();regular_bytes=0;omissions=[]
            for member in members:
                path=safe_member(member.name)
                require(path.parts[0]==spec['archive_root'] and member.name not in names,'unexpected root/duplicate member')
                relative=str(Path(member.name).relative_to(spec['archive_root']))
                if member.issym():
                    require(relative in OMITTED_TEST_ALIASES and member.linkname==OMITTED_TEST_ALIASES[relative]
                            and member.size==0 and member.mode==0o777 and not member.issparse(),
                            'unapproved archive link refused')
                    names.add(member.name)
                    omissions.append({'path':relative,'type':'symlink','target':member.linkname,
                                      'bytes':member.size,'mode':member.mode})
                    continue  # No link creation, dereference or linked content extraction.
                require(member.isdir() or member.isreg(),'special archive member refused')
                require(not member.issparse() and not member.linkname and member.mode & ~0o777==0,
                        'sparse/link/privileged source member refused')
                require(all(ord(c)>=32 and ord(c)!=127 for c in member.name),'control character in source path')
                require(member.size>=0 and (member.isreg() or member.size==0),'invalid archive length')
                names.add(member.name);regular_bytes+=member.size if member.isreg() else 0
            require(regular_bytes==spec['regular_bytes']==897821359,'archive source byte total differs')
            require({r['path'] for r in omissions}==set(OMITTED_TEST_ALIASES) and len(omissions)==2,
                    'exact test alias inventory differs')
            omissions.sort(key=lambda r:r['path'])
            write(WORK/'omitted-test-aliases.json',{'archive_sha256':archive['sha256'],
                  'scope':'chdman build source; these two zstd CLI test aliases are not exported',
                  'omitted_members':omissions})
            root.mkdir(mode=0o755)
            files={}
            for member in members:
                if member.issym():continue  # Already matched the complete exact omission inventory.
                relative=Path(member.name).relative_to(spec['archive_root'])
                dest=root/relative
                require(dest.resolve()==dest and dest.is_relative_to(root),'source traversal/alias')
                if member.isdir():
                    dest.mkdir(parents=True,exist_ok=True);continue
                dest.parent.mkdir(parents=True,exist_ok=True)
                remaining=member.size;digest=hashlib.sha256()
                with archive_stream.extractfile(member) as source, dest.open('xb') as output:
                    while remaining:
                        block=source.read(min(1024**2,remaining))
                        require(block and len(block)<=remaining,'truncated member')
                        output.write(block);digest.update(block);remaining-=len(block)
                    require(source.read(1)==b'','oversized member')
                dest.chmod(member.mode)
                files[str(relative)]={'sha256':digest.hexdigest(),'bytes':member.size,'mode':member.mode}
        after=os.fstat(raw.fileno())
        require((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==
                (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),'archive identity changed')
    require(sha(ARCHIVE)==archive['sha256'],'archive changed during export')
    for name,row in spec['source_files'].items():
        require(files[name]['sha256']==row['sha256'] and files[name]['bytes']==row['bytes'],'selected original source differs: '+name)
    write(WORK/'pristine-source-inventory.json',{'archive_sha256':archive['sha256'],'files':files})
    patch=spec['private_source_adjustment'];target=root/patch['file']
    require(sha(target)==patch['before_sha256'],'pre-patch source differs')
    code,_,_=command(RECORDS/'patch-original',['patch','--batch','--forward','--fuzz=0','-d',root,'-p1','-i',PLAN/patch['patch']],30)
    require(code==0 and sha(target)==patch['after_sha256'],'exact existing patch failed')
    files[patch['file']]={'sha256':sha(target),'bytes':target.stat().st_size,'mode':target.stat().st_mode&0o777}
    osd_patch=spec['private_osd_adjustment'];osd_target=root/osd_patch['file']
    require(sha(osd_target)==osd_patch['before_sha256'],'pre-OSD-patch source differs')
    code,_,_=command(RECORDS/'patch-osd',['patch','--batch','--forward','--fuzz=0','-d',root,'-p1','-i',PLAN/osd_patch['patch']],30)
    require(code==0 and sha(osd_target)==osd_patch['after_sha256'],'exact OSD selection patch failed')
    files[osd_patch['file']]={'sha256':sha(osd_target),'bytes':osd_target.stat().st_size,'mode':osd_target.stat().st_mode&0o777}
    write(WORK/'source-inventory.json',{'family':'chdman','archive_sha256':archive['sha256'],
          'archive_members':len(members),'pristine_regular_bytes':regular_bytes,'omitted_members':omissions,
          'omissions_receipt_sha256':sha(WORK/'omitted-test-aliases.json'),
          'pristine_inventory_sha256':sha(WORK/'pristine-source-inventory.json'),
          'adjustment':patch,'osd_adjustment':osd_patch,'files':files})
    print('Exported all MAME regular source; exactly two zstd CLI test aliases omitted; '+str(len(files))+' regular files; sealed link-policy and OSD-selection patches applied')


if __name__=='__main__':main()
