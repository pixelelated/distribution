"""Retained-only census of exact named T46 roots; descriptor-relative NOFOLLOW."""
import datetime,hashlib,json,os,pathlib,stat
A=pathlib.Path(__file__).resolve().parents[1];fixture=json.loads((A/'stage-e/fixtures-manifest.json').read_text())['root'];assert fixture=='/tmp/m6-t46-eh-fixtures-kbnfwd30';roots=['/tmp/m6-t46-inputs.svbcPP','/tmp/m6-t46-confinement-s69_op77',fixture];result=[]
def open_root(path):
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
 try:
  for part in pathlib.PurePosixPath(path).parts[1:]:
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  return fd
 except:os.close(fd);raise
def visit(fd,prefix,rows):
 for name in sorted(os.listdir(fd)):
  rel=prefix+name
  try:
   s=os.stat(name,dir_fd=fd,follow_symlinks=False);row={'path':rel,'mode':oct(stat.S_IMODE(s.st_mode)),'size':s.st_size,'inode_observed_now':s.st_ino}
   if stat.S_ISDIR(s.st_mode):
    row['type']='directory';rows.append(row);child=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
    try:visit(child,rel+'/',rows)
    finally:os.close(child)
   elif stat.S_ISREG(s.st_mode):
    child=os.open(name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd);h=hashlib.sha256()
    with os.fdopen(child,'rb') as f:
     assert os.fstat(f.fileno()).st_ino==s.st_ino
     for b in iter(lambda:f.read(1048576),b''):h.update(b)
    row.update(type='ordinary-file',sha256=h.hexdigest());rows.append(row)
   else:row.update(type='symlink-not-followed' if stat.S_ISLNK(s.st_mode) else 'nonordinary-not-opened',retained=True);rows.append(row)
  except OSError as e:rows.append({'path':rel,'retained':True,'limitation':type(e).__name__+': '+str(e.errno)})
for root in roots:
 rows=[]
 try:
  fd=open_root(root)
  try:visit(fd,'',rows)
  finally:os.close(fd)
  status='retained; observed current metadata and ordinary-file hashes'
 except OSError as e:status='retained; inaccessible '+type(e).__name__+': '+str(e.errno)
 result.append({'root':root,'status':status,'entries':rows,'ordinary_files':sum(x.get('type')=='ordinary-file' for x in rows),'ordinary_bytes':sum(x.get('size',0) for x in rows if x.get('type')=='ordinary-file'),'directories':sum(x.get('type')=='directory' for x in rows),'symlinks_not_followed':sum(x.get('type')=='symlink-not-followed' for x in rows),'entry_metadata_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
out={'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':'T3 wN:p6, bounded explicit dispatch custody only','action':'retain everything; no deletion','roots':result,'separately_retained_publication_packets':['/tmp/m6-t46-d-publication-pqw4z0xj','/tmp/m6-t46-eh-publication-kmr8zpxj'],'limitations':'Current inode/count/hash observations only. No historical creation/process evidence; no global path/process/host/cache census; symlinks never followed. Root owns later retirement.'};p=A/'stage-h/retained-census.json';p.parent.mkdir(exist_ok=True);assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps([{k:v for k,v in x.items() if k!='entries'} for x in result]));print('PASS retained-only exact-root census; no deletion')
