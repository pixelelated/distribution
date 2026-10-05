from pathlib import Path
import subprocess,struct,json
subprocess.run(['modprobe','dmi-sysfs'],check=True)
rows=[]
for p in sorted(Path('/sys/firmware/dmi/entries').glob('17-*/raw')):
 b=p.read_bytes();assert len(b)>=14 and b[0]==17
 code=struct.unpack_from('<H',b,12)[0];assert code!=0xffff,'unknown physical memory size'
 if code==0x7fff:
  assert len(b)>=32;size=(struct.unpack_from('<I',b,28)[0]&0x7fffffff)*1024
 else:size=(code&0x7fff)*(1 if code&0x8000 else 1024)
 rows.append({'entry':p.parent.name,'size_kib':size})
assert rows,'no firmware memory-device entries'
print(json.dumps({'devices':rows,'physical_kib':sum(x['size_kib'] for x in rows)}))
