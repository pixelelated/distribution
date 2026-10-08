#!/usr/bin/python3
"""Disposable guest-only Xbox-compatible uinput fixture for the shipped hotkey.

Creates no host device. The native DuckStation configured binding stays
SDL-0/Guide & SDL-0/B; this fixture emits those two controls and nothing else.
"""
import fcntl,json,os,pathlib,struct,time
base=pathlib.Path('/storage/qa521');fifo=base/'pad.commands';log=base/'pad.events.jsonl'
fd=os.open('/dev/uinput',os.O_WRONLY|os.O_NONBLOCK)
def ioctl(n,v):fcntl.ioctl(fd,n,v)
for event in (1,3):ioctl(0x40045564,event)
keys=[304,305,307,308,310,311,314,315,316,317,318]
for key in keys:ioctl(0x40045565,key)
axes=[0,1,2,3,4,5,16,17]
for axis in axes:ioctl(0x40045567,axis)
hi=[0]*64;lo=[0]*64;fuzz=[0]*64;flat=[0]*64
for axis in axes:
 hi[axis]=1 if axis in (16,17) else 255 if axis in (2,5) else 32767
 lo[axis]=-1 if axis in (16,17) else 0 if axis in (2,5) else -32768
 flat[axis]=0
raw=struct.pack('80sHHHHI',b'QA521 Synthetic Xbox 360 Controller',3,0x045e,0x028e,0x0114,0)+struct.pack('256i',*(hi+lo+fuzz+flat));assert len(raw)==1116
os.write(fd,raw);ioctl(0x5501,0)
def event(kind,code,value):
 now=time.time();seconds=int(now);os.write(fd,struct.pack('llHHi',seconds,int((now-seconds)*1e6),kind,code,value))
def sync():event(0,0,0)
def record(x):
 with log.open('a') as f:f.write(json.dumps({'time':time.time(),**x})+'\n')
try:
 for axis in axes:event(3,axis,0)
 sync();(base/'pad.pid').write_text(str(os.getpid())+'\n');os.mkfifo(fifo,0o600);record({'state':'created','vendor':'045e','product':'028e','binding':'SDL-0/Guide & SDL-0/B'})
 stop=False
 while not stop:
  with fifo.open() as stream:
   for line in stream:
    command=line.strip()
    if command=='capture':
     event(1,316,1);sync();time.sleep(0.08);event(1,305,1);sync();time.sleep(0.12);event(1,305,0);sync();time.sleep(0.08);event(1,316,0);sync();record({'command':'capture','key_sequence':[[316,1],[305,1],[305,0],[316,0]]})
    elif command=='quit':stop=True;break
    else:record({'refused_command':command})
finally:
 ioctl(0x5502,0);os.close(fd)
 if fifo.exists():fifo.unlink()
 record({'state':'destroyed'})
