from pathlib import Path
import subprocess,json,hashlib,os,time,threading,datetime
r=Path(__file__).parent;contract=json.loads((r/'records/source.json').read_text());source=Path('/home/max/Development/emulationstation-next.worktrees/m7-rc-library-setup');baseline=Path('/home/max/Development/emulationstation-next.worktrees/m7-rc-setup-570');copy=Path('/home/max/Development/emulationstation-next.worktrees/m7-library-copy-575');frozen=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20');packet=r/'records/wii-composition/docs/qa-logs/2026-10-13-rvz-regression-source';name='pix-m7-rvz-sanitizer-20261013-compile01';done=threading.Event();samples=[];result={'rc':1,'started':time.time()}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_sources():
 bindings=json.loads((packet/'source-bindings.json').read_text())
 for root,key in [(source,'candidate'),(baseline,'baseline'),(copy,'copy')]:
  assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==contract[key]
  assert not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip()
  if key in bindings:assert all(sha(root/p)==h for p,h in bindings[key]['files'].items()),key
 return {str(root):subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip() for root in (source,baseline,copy)}
def sample():
 with (r/'host-resources.jsonl').open('x') as f:
  while not done.is_set():
   row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'monotonic':time.monotonic()}
   for label,path in [('meminfo','/proc/meminfo'),('vmstat','/proc/vmstat'),('memory_pressure','/proc/pressure/memory'),('io_pressure','/proc/pressure/io')]:row[label]=Path(path).read_text()
   st=os.statvfs(r);row['available_bytes']=st.f_bavail*st.f_frsize;f.write(json.dumps(row)+'\n');f.flush();samples.append(row);done.wait(1)
t=threading.Thread(target=sample);t.start()
try:
 result['sources_before']=verify_sources()
 for sub in [packet,packet/'wii-public-path']:
  for line in (sub/'SHA256SUMS').read_text().splitlines():
   expected,path=line.split('  ',1);assert sha(sub/path)==expected,path
 assert sha(Path(contract['archive']))==contract['packet_tar_sha256']
 old='/workspace/repos/rocknix.worktrees/m7-pixelelated'
 args=['docker','run','--rm','--name',name,'--cidfile',str(r/'container.cid'),'--network','none','--read-only','--memory','4g','--memory-swap','4g','--cpus','2','--user','1000:1000','-v',str(frozen)+':'+old+':ro','-v',str(r)+':/work:rw','-v',str(source)+':/source:ro','-v',str(baseline)+':/baseline:ro','-v',str(copy)+':/copy:ro',contract['builder'],'python3','/work/inner.py']
 (r/'records/docker-command.json').write_text(json.dumps(args,indent=2)+'\n');p=subprocess.run(args,timeout=900);result['container_rc']=p.returncode;assert p.returncode==0
 result['sources_after']=verify_sources();assert result['sources_before']==result['sources_after']
 compiled=json.loads((r/'compile-result.json').read_text());assert compiled['rc']==0
 assert all(sha(r/p)==h for p,h in compiled['artifacts'].items())
 result['rc']=0
finally:
 cid=r/'container.cid'
 if cid.exists():
  ident=cid.read_text().strip();q=subprocess.run(['docker','inspect','--format','{{.State.Running}}',ident],capture_output=True,text=True)
  if q.returncode==0 and q.stdout.strip()=='true':
   q=subprocess.run(['docker','stop','--time','10',ident],capture_output=True,text=True,timeout=25);result['forced_container_stop_rc']=q.returncode;result['rc']=1
 done.set();t.join(timeout=5);result['sampler_complete']=not t.is_alive() and len(samples)>1;result['ended']=time.time()
 if not result['sampler_complete']:result['rc']=1
 (r/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
