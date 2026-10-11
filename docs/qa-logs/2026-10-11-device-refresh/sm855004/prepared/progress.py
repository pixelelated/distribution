import os,re,time
buf=b'';last=0;pending=b''
def line(raw,force=False):
 global last,pending
 raw=raw.strip()
 if not raw:return
 if re.match(rb'[0-9,]+ +[0-9]+%',raw):
  pending=raw
  if not force and time.monotonic()-last<5:return
  last=time.monotonic()
 print(raw.decode('utf-8','replace'),flush=True)
while True:
 chunk=os.read(0,65536)
 if not chunk:break
 parts=re.split(rb'[\r\n]',buf+chunk);buf=parts.pop()
 for part in parts:line(part)
line(buf,True)
line(pending,True)
