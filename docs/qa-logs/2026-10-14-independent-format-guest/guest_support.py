#!/usr/bin/env python3
"""Prepared guest-only file/identity helpers. No subprocess at import time."""
import hashlib
import json
import os
from pathlib import Path
import struct

HERE=Path(__file__).resolve().parent
INPUT=Path('/tmp/pix-input/pix574-format')
SCRATCH=Path('/run/pix574-scratch')
OUTPUT=Path('/tmp/pix-output')
LIMIT=2*1024**3


def require(value,message):
    if not value:raise RuntimeError(message)


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk:=stream.read(1024*1024):h.update(chunk)
    return h.hexdigest()


def read(path):return json.loads(Path(path).read_text())


def write(path,value):
    with Path(path).open('x') as stream:json.dump(value,stream,indent=2);stream.write('\n')


def relative(name):
    p=Path(name)
    require(p.parts and not p.is_absolute() and '..' not in p.parts and str(p)==name and '\x00' not in name,'unsafe input member')
    return p


def identity(pid):
    try:
        words=Path('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split()
        return {'pid':pid,'ppid':int(words[1]),'pgrp':int(words[2]),'session':int(words[3]),
                'start_ticks':int(words[19]),'state':words[0]}
    except FileNotFoundError:return None


def same(before):
    now=identity(before['pid'])
    return now is not None and now['start_ticks']==before['start_ticks']


def census():
    rows={}
    for path in Path('/proc').iterdir():
        if path.name.isdecimal():
            row=identity(int(path.name))
            if row is not None:rows[row['pid']]=row
    return rows


def descendants(rows,parent):
    selected={parent};changed=True
    while changed:
        old=len(selected)
        selected.update(pid for pid,row in rows.items() if row['ppid'] in selected)
        changed=len(selected)!=old
    return {pid:rows[pid] for pid in selected if pid!=parent and pid in rows}


def usage(roots):
    apparent=allocated=files=0
    for root in roots:
        if not root.exists():continue
        for directory,dirs,names in os.walk(root,followlinks=False):
            for name in names:
                try:st=(Path(directory)/name).lstat()
                except FileNotFoundError:continue
                apparent+=st.st_size;allocated+=st.st_blocks*512;files+=1
    return {'apparent':apparent,'allocated':allocated,'files':files}


def interpreter(path):
    with Path(path).open('rb') as stream:
        header=stream.read(64)
        require(len(header)==64 and header[:7]==b'\x7fELF\x02\x01\x01' and struct.unpack_from('<H',header,18)[0]==62,
                'expected x86_64 ELF64 target')
        offset=struct.unpack_from('<Q',header,32)[0];size,count=struct.unpack_from('<HH',header,54)
        require(size==56 and 0<count<=128,'unsupported program headers')
        found=[]
        for i in range(count):
            stream.seek(offset+i*size);row=stream.read(size);require(len(row)==size,'truncated program header')
            if struct.unpack_from('<I',row)[0]==3:
                start=struct.unpack_from('<Q',row,8)[0];length=struct.unpack_from('<Q',row,32)[0]
                require(1<length<=256,'invalid interpreter length');stream.seek(start);raw=stream.read(length)
                require(len(raw)==length and raw.endswith(b'\0') and b'\0' not in raw[:-1],'malformed interpreter')
                found.append(raw[:-1].decode('ascii'))
    require(len(found)==1 and found[0] in ('/lib64/ld-linux-x86-64.so.2','/usr/lib/ld-linux-x86-64.so.2'),
            'unsupported target interpreter')
    return found[0]


def verify_packet():
    names=set()
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);require(Path(name).name==name and sha(HERE/name)==digest,'packet changed: '+name);names.add(name)
    require({p.name for p in HERE.iterdir()}==names|{'SHA256SUMS'},'unexpected packet members')


def verify_input():
    verify_packet();binding=read(HERE/'input-bindings.json')
    require(INPUT.resolve()==INPUT and os.statvfs(INPUT).f_flag&os.ST_RDONLY,'exact read-only public input required')
    manifest=INPUT/'bundle/manifest.json';require(sha(manifest)==binding['bundle_manifest_sha256'],'bundle manifest changed')
    bundle=read(manifest)
    require(bundle['bytes']==50726779 and len(bundle['files'])==2680,'accepted bundle shape changed')
    allowed={'bundle/manifest.json'}|{'bundle/'+name for name in bundle['files']}
    for name,item in binding['files'].items():
        path=INPUT/relative(name)
        require(path.resolve()==path and path.stat().st_size==item['bytes'] and sha(path)==item['sha256'],'input changed: '+name)
        allowed.add(name)
    allowed|={'packet/'+p.name for p in HERE.iterdir()}
    actual=set()
    for path in INPUT.rglob('*'):
        require(not path.is_symlink(),'public input symlink refused')
        if path.is_dir():continue
        require(path.is_file(),'unsupported input member');actual.add(str(path.relative_to(INPUT)))
    require(actual==allowed,'public input file set differs')
    # Immutable guest-stage.py subsequently checks every bundle content hash too.
    return binding,bundle
