"""Exact qualified #584 numeric proc/pidfd helpers; no fixture import."""
import os
from pathlib import Path
import signal


def require(value,message):
    if not value:raise AssertionError(message)


def proc_identity(pid):
    """Read PID/PPID/start ticks only. A vanished directory is the sole benign read race."""
    directory=Path('/proc')/str(pid)
    try:
        with (directory/'stat').open('rb') as stream:
            raw=stream.read(65537)
    except (FileNotFoundError, ProcessLookupError):
        try: directory.stat()
        except (FileNotFoundError, ProcessLookupError): return None
        raise RuntimeError('stat unavailable for a still-present proc PID '+str(pid))
    require(len(raw)<=65536, 'oversized proc stat for PID '+str(pid))
    # comm may contain spaces, newlines and closing parentheses. It is never
    # matched or retained; numeric fields start after its final closing paren.
    prefix,separator,tail=raw.rpartition(b')')
    require(separator and prefix.split(b' (',1)[0]==str(pid).encode(),
            'malformed proc stat PID '+str(pid))
    fields=tail.split()
    require(len(fields)>=20, 'short proc stat PID '+str(pid))
    return {'pid':pid,'ppid':int(fields[1]),'start_ticks':int(fields[19])}


def direct_children(parent):
    """Census this subreaper's direct/adopted children; errors never mean empty."""
    require(proc_identity(parent) is not None, 'cannot observe fixture owner in proc')
    found=[]
    for entry in Path('/proc').iterdir():
        if not entry.name.isascii() or not entry.name.isdigit(): continue
        identity=proc_identity(int(entry.name))
        if identity is not None and identity['ppid']==parent:
            found.append(identity)
    return sorted(found,key=lambda item:item['pid'])


def signal_child(identity,parent):
    """Only an identity-checked child pidfd may receive a signal; never numeric kill."""
    require(identity['ppid']==parent, 'refusing a non-child signal')
    current=proc_identity(identity['pid'])
    if current is None: return {'identity':identity,'outcome':'already-gone'}
    require(current==identity, 'child identity changed before pidfd acquisition')
    try: fd=os.pidfd_open(identity['pid'],0)
    except ProcessLookupError: return {'identity':identity,'outcome':'gone-before-pidfd'}
    try:
        # Refuse reuse/reparenting between the census and the acquired handle.
        current=proc_identity(identity['pid'])
        if current is None: return {'identity':identity,'outcome':'gone-after-pidfd'}
        require(current==identity, 'child identity changed after pidfd acquisition')
        try: signal.pidfd_send_signal(fd,signal.SIGKILL,None,0)
        except ProcessLookupError: return {'identity':identity,'outcome':'gone-before-signal'}
        return {'identity':identity,'outcome':'pidfd-kill'}
    finally:
        os.close(fd)
