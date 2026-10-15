import os,json,subprocess,datetime
from pathlib import Path
r=Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01/build.pixelelated-GENERIC_X64.x86_64');assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
root=str(r);matches=[];errors=[];scanned=0;inaccessible_other_uid=0
for p in Path('/proc').iterdir():
 if not p.name.isdigit() or int(p.name)==os.getpid():continue
 try:
  uid=p.stat().st_uid;args=(p/'cmdline').read_bytes();sources=[]
  if root.encode() in args:sources.append('argv')
  if uid==os.getuid():
   scanned+=1
   for n in ['cwd','root']:
    try:
     s=os.readlink(p/n)
     if s==root or s.startswith(root+'/'):sources.append(n)
    except (FileNotFoundError,ProcessLookupError):pass
   for fd in (p/'fd').iterdir():
    try:
     s=os.readlink(fd)
     if s==root or s.startswith(root+'/'):sources.append('fd')
    except (FileNotFoundError,ProcessLookupError):pass
   if root in (p/'maps').read_text(errors='replace'):sources.append('maps')
  else:inaccessible_other_uid+=1
  if sources:matches.append({'pid':int(p.name),'uid':uid,'sources':sorted(set(sources))})
 except (FileNotFoundError,ProcessLookupError):pass
 except OSError as e:errors.append({'pid':int(p.name),'error':type(e).__name__})
ids=subprocess.check_output(['docker','ps','-aq'],text=True,timeout=20).split();containers=[]
if ids:
 for c in json.loads(subprocess.check_output(['docker','inspect',*ids],text=True,timeout=30)):
  mounts=[m['Source'] for m in c['Mounts'] if m['Source']==root or m['Source'].startswith(root+'/') or root.startswith(m['Source'].rstrip('/')+'/')]
  if mounts:containers.append({'id':c['Id'],'running':c['State']['Running'],'sources':mounts})
registry=json.loads(Path('/workspace/repos/rocknix/.git/pixelelated-build-admission/jobs.json').read_text());active=[{'id':i,'state':v['state'],'stage':v.get('stage')} for i,v in registry['jobs'].items() if v['state'] not in ['consumed']]
stat=r.stat();result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':root,'identity':{'device':stat.st_dev,'inode':stat.st_ino,'mode':stat.st_mode},'host_pid_namespace':4026531836,'own_uid_processes_scanned':scanned,'other_uid_processes_without_fd_census':inaccessible_other_uid,'matches':matches,'errors':errors,'container_references':containers,'active_admissions':active,'scope':'All readable host argv; same-UID cwd/root/fd/maps; all Docker container mounts. No whole-host root-only FD census. Atomic relocation of completed owned build cache, not deletion.','prepared_baseline':'/workspace/tmp/pix-m7-final-baseline-20261014-01 is prepared only and will not run; fresh owner must bind corrected image and new build root.','status':'CLEAR_WITH_STATED_SCOPE' if not matches and not errors and not containers and not active else 'REVIEW_REQUIRED'}
p=Path('/tmp/pix572-cache-dependencies.json');p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
