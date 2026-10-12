from pathlib import Path
import json,os,sys
j=json.loads(Path(sys.argv[1]).read_text());rows=[]
for r in j['links']:
 p=Path(j['guest']+r['source'][len(j['host']):]);real=str(p.resolve());identity=None
 try:
  s=p.stat();identity=dict(device=s.st_dev,inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=s.st_mode)
 except FileNotFoundError:pass
 rows.append(dict(path=str(p),link=os.readlink(p),resolved=real,identity=identity))
print(json.dumps(dict(rows=rows,mountinfo=[l for l in Path('/proc/self/mountinfo').read_text().splitlines() if '/workspace/repos/' in l])))
