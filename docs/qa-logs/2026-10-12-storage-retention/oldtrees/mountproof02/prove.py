from pathlib import Path
from datetime import datetime,timezone
import json,os,subprocess,sys,hashlib,stat
O=Path(__file__).resolve().parent
REVIEW=Path('/workspace/tmp/pixelelated-m7-retention-20261012-oldtrees01')
def read(p):return json.loads(Path(p).read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def ident(p):
 s=p.stat();return {'device':s.st_dev,'inode':s.st_ino,'size':s.st_size,'mtime_ns':s.st_mtime_ns,'mode':s.st_mode}
def main():
 (O/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
 links=read(REVIEW/'external-reference-leads.json')['links'];summaries=[];classified=[]
 for label,base in [('h700','pixelelated-m7-h700-refresh-03'),('sm8550','pixelelated-m7-sm8550-refresh-05'),('vm20','pixelelated-m7-build20b')]:
  ip=Path('/workspace/tmp')/base/'inputs.json';i=read(ip);host=i['host_worktree'];guest=i['container_worktree'];rows=[]
  for r in links:
   if r['source'].startswith(host+'/'):
    p=Path(r['source']);assert p.is_symlink() and os.readlink(p)==r['link'];rows.append(r)
  assert rows
  write(O/(label+'-input.json'),{'host':host,'guest':guest,'links':rows})
  command=['docker','run','--rm','--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--user',str(os.getuid())+':'+str(os.getgid()),'--mount',f'type=bind,source={host},target={guest},readonly','--mount',f'type=bind,source={O},target=/proof,readonly','--workdir',guest,'--entrypoint','/usr/bin/python3',i['container'],'-I','/proof/inside.py','/proof/'+label+'-input.json']
  with (O/(label+'-stdout.json')).open('x') as out,(O/(label+'-stderr.log')).open('x') as err:subprocess.run(command,stdout=out,stderr=err,check=True,timeout=300)
  actual=read(O/(label+'-stdout.json'));assert len(actual['rows'])==len(rows)
  counts={'references':len(rows),'resolved':0,'already_missing':0};proofrows=[]
  for r,c in zip(rows,actual['rows']):
   assert c['link']==r['link'];assert c['path']==guest+r['source'][len(host):]
   assert c['resolved'].startswith(guest+'/'),c
   mapped=Path(host+c['resolved'][len(guest):]);host_was_missing=not Path(r['source']).exists()
   if c['identity'] is not None:
    assert ident(mapped)==c['identity'],('inode mapping mismatch',mapped);counts['resolved']+=1
   else:
    assert not mapped.exists() and host_was_missing,('new missing target',mapped);counts['already_missing']+=1
   proofrows.append({**r,'classification':'CURRENT_CACHE_CONTAINER_BIND','guest_path':c['path'],'guest_resolved':c['resolved'],'retained_host_target':str(mapped),'identity':c['identity'],'missing_before_cleanup':host_was_missing})
  write(O/(label+'-links.json'),proofrows);classified+=proofrows
  summary={'label':label,'host_worktree':host,'container_worktree':guest,'input_sha256':hashlib.sha256(ip.read_bytes()).hexdigest(),'image':i['container'],'command':command,**counts,'result':'PASS_BIND_MOUNT_WITHOUT_OLD_PHYSICAL_TREE','mountinfo':actual['mountinfo']};summaries.append(summary);print(json.dumps({k:v for k,v in summary.items() if k not in ['command','mountinfo']}),flush=True)
 write(O/'classified-cache-links.json',classified);write(O/'result.json',{'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','caches':summaries,'deletion_performed':False})
rc=1
try:main();rc=0
finally:
 (O/'inner.rc').write_text(str(rc)+'\n');(O/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
