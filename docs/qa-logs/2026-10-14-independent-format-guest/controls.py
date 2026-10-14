#!/usr/bin/env python3
"""UNRUN synthetic parsing/ownership controls. No child/target or mount calls.

Coordinator may admit separately; these do not qualify actual Linux cleanup.
"""
import importlib.util
from pathlib import Path
import struct
import sys
import tempfile
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('support',Path(__file__).with_name('guest_support.py'))
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
count=0


def expect(value):
    global count
    assert value;count+=1


def refused(fn):
    try:fn()
    except (RuntimeError,UnicodeError):return expect(True)
    raise AssertionError('required refusal absent')


def elf(interp):
    h=bytearray(64);h[:7]=b'\x7fELF\x02\x01\x01';struct.pack_into('<H',h,18,62)
    struct.pack_into('<Q',h,32,64);struct.pack_into('<HH',h,54,56,1)
    p=bytearray(56);struct.pack_into('<I',p,0,3);struct.pack_into('<Q',p,8,120)
    struct.pack_into('<Q',p,32,len(interp))
    return bytes(h+p)+interp


def main():
    for name in ('bundle/lib/libc.so.6','packet/guest-run.py'):expect(str(s.relative(name))==name)
    for name in ('','/lib/libc.so.6','../x','a/../b','a//b','a/./b','a\0b'):refused(lambda:s.relative(name))
    rows={1:{'ppid':0},10:{'ppid':1},11:{'ppid':10},12:{'ppid':11},13:{'ppid':1},14:{'ppid':12}}
    expect(set(s.descendants(rows,10))=={11,12,14})
    # New session/group does not remove descendant ownership; unrelated sibling
    # and a reused PID with another start tick are not ownership evidence.
    rows[12].update(pgrp=12,session=12);expect(12 in s.descendants(rows,10))
    original=s.identity
    try:
        s.identity=lambda pid:{'pid':pid,'start_ticks':21}
        expect(s.same({'pid':12,'start_ticks':21}));expect(not s.same({'pid':12,'start_ticks':20}))
        s.identity=lambda pid:None;expect(not s.same({'pid':12,'start_ticks':21}))
    finally:s.identity=original
    with tempfile.TemporaryDirectory(prefix='pix574-format-controls-') as directory:
        p=Path(directory)/'synthetic-elf'
        for path in ('/lib64/ld-linux-x86-64.so.2','/usr/lib/ld-linux-x86-64.so.2'):
            p.write_bytes(elf(path.encode()+b'\0'));expect(s.interpreter(p)==path)
        for data in (b'bad',elf(b'/host/loader\0'),elf(b'/lib64/ld-linux-x86-64.so.2'),
                     elf(b'/lib64/ld-linux-x86-64.so.2\0extra\0'),elf(b'x'*257)):
            p.write_bytes(data);refused(lambda:s.interpreter(p))
        p.write_bytes(b'abc');expect(s.sha(p)=='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
    print('PASS '+str(count)+' synthetic parsing/ownership controls; no guest loading/process cleanup proof')


if __name__=='__main__':main()
