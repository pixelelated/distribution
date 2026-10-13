from pathlib import Path
import subprocess,shutil,json,hashlib,os,time,threading,datetime
r=Path(__file__).parent;records=r/'records';src=Path(json.loads((records/'size.json').read_text())['root']);out=r/'scratch/es';source=Path('/home/max/Development/emulationstation-next.worktrees/m7-rc-setup-570');frozen=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20');repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');contract=json.loads((records/'source.json').read_text());samples=[];done=threading.Event();result={'rc':1,'stages':[],'started':time.time()};name='pix-m7-setup-20261013-compile01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(root):
 rows={}
 for d,ds,fs in os.walk(root):
  if '.git' in ds:ds.remove('.git')
  for n in fs:
   if n=='.git':continue
   p=Path(d)/n;rows[str(p.relative_to(root))]={'symlink':os.readlink(p)} if p.is_symlink() else {'sha256':sha(p),'bytes':p.stat().st_size}
 return rows
def sample():
 with (r/'host-resources.jsonl').open('x') as stream:
  while not done.is_set():
   row={'monotonic':time.monotonic(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
   for label,path in [('meminfo','/proc/meminfo'),('vmstat','/proc/vmstat'),('memory_pressure','/proc/pressure/memory'),('io_pressure','/proc/pressure/io')]:row[label]=Path(path).read_text()
   row['available_bytes']=os.statvfs(r).f_bavail*os.statvfs(r).f_frsize;stream.write(json.dumps(row)+'\n');stream.flush();samples.append(row);done.wait(1)
thread=threading.Thread(target=sample);thread.start()
try:
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()==contract['candidate']
 assert not subprocess.check_output(['git','status','--porcelain'],cwd=source,text=True).strip()
 assert all(sha(source/p)==v['sha256'] for p,v in contract['files'].items())
 before=manifest(src);(records/'baseline-files.json').write_text(json.dumps(before,indent=2)+'\n')
 shutil.copytree(src,out,symlinks=True,ignore=shutil.ignore_patterns('.git'))
 assert manifest(out)==before,'copy differs from retained baseline';result['stages'].append({'stage':'verified-independent-copy','rc':0})
 for p,v in contract['files'].items():
  shutil.copyfile(source/p,out/p)
  assert sha(out/p)==v['sha256']
 preflight=subprocess.run([str(repo/'tools/build-preflight')],capture_output=True,text=True);(r/'post-copy-preflight.txt').write_text(preflight.stdout+preflight.stderr);assert preflight.returncode==0,'post-copy resource preflight refused'
 old='/workspace/repos/rocknix.worktrees/m7-pixelelated';dest=old+'/build.pixelelated-GENERIC_X64.x86_64/build/'+src.name
 args=['docker','run','--rm','--name',name,'--cidfile',str(r/'container.cid'),'--network','none','--read-only','--memory','8g','--memory-swap','8g','--cpus','2','--user','1000:1000','-v',str(frozen)+':'+old+':ro','-v',str(out)+':'+dest+':rw','-v',str(r)+':/work:rw','-v',str(source)+':/source:ro',contract['builder'],'python3','/work/inner.py']
 (records/'docker-command.json').write_text(json.dumps(args,indent=2)+'\n');p=subprocess.run(args,timeout=900);result['stages'].append({'stage':'container-build','rc':p.returncode});assert p.returncode==0,'container failed'
 compiled=json.loads((r/'compile-result.json').read_text());assert compiled['rc']==0
 after=manifest(src);assert after==before,'frozen baseline changed';result['frozen_baseline_unchanged']=True
 result['binary_sha256']=sha(r/'scratch/emulationstation');assert result['binary_sha256']==compiled['binary_sha256']
 result['rc']=0
finally:
 cid=r/'container.cid'
 if cid.exists():
  container_id=cid.read_text().strip()
  probe=subprocess.run(['docker','inspect','--format','{{.State.Running}}',container_id],capture_output=True,text=True)
  if probe.returncode==0 and probe.stdout.strip()=='true':
   stopped=subprocess.run(['docker','stop','--time','10',container_id],capture_output=True,text=True,timeout=25)
   result['forced_container_stop_rc']=stopped.returncode;result['rc']=1
 done.set();thread.join(timeout=5);result['sampler_complete']=not thread.is_alive() and len(samples)>1;result['ended']=time.time()
 if not result['sampler_complete']:result['rc']=1
 (r/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
