from pathlib import Path
import datetime,hashlib,json,tarfile,shutil,subprocess
repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');root=repo/'docs/qa-logs/2026-10-14-screenscraper-rejection-runtime';packet=root/'attempt02';packet.mkdir()
owner=Path('/workspace/tmp/pix566-es-component-20261014-02');stage=owner/'stages/es-component';work=owner/'work';run=Path(json.loads((stage/'host-completion.json').read_text())['run'])
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def dump(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
assert (run/'admission-consumed.json').exists();assert Path('/proc/self/ns/pid').stat().st_ino==4026531836
v=json.loads((stage/'host-completion.json').read_text());assert all(not Path('/proc',str(x)).exists() for x in v['actual_host_pids_absent'])
compiled=json.loads((work/'component-result.json').read_text());assert compiled['rc']==0 and all(x['rc']==0 for x in compiled['stages'])
assert compiled['source_commit']=='3178b832b8d134198b2b4eede4f725d4ed283f8c'
for n,row in compiled['artifacts'].items():assert sha(work/'artifacts'/n)==row['sha256']
files=[]
with tarfile.open(packet/'original-records.tar.gz','w:gz') as archive:
 for prefix,folder in [('stage',stage),('run',run)]:
  for p in sorted(folder.rglob('*')):
   if not p.is_file():continue
   name=prefix+'/'+str(p.relative_to(folder));archive.add(p,arcname=name,recursive=False);files.append({'path':name,'sha256':sha(p),'bytes':p.stat().st_size})
 for p in sorted(work.iterdir()):
  if not p.is_file():continue
  name='work/'+p.name;archive.add(p,arcname=name,recursive=False);files.append({'path':name,'sha256':sha(p),'bytes':p.stat().st_size})
dump(packet/'original-records.json',{'archive_sha256':sha(packet/'original-records.tar.gz'),'files':files})
for name in ['component-result.json','source-staging.json']:shutil.copy2(work/name,packet/name)
for name in ['result.json','container-result.json','host-completion.json','acceptance.json']:shutil.copy2(stage/name,packet/name)
shutil.copy2(run/'admission-consumed.json',packet/'admission-consumed.json')
inner=json.loads((stage/'container-result.json').read_text())
dump(packet/'analysis.json',{'status':'PASS','es_commit':compiled['source_commit'],'syntax_modes':['runtime-only','compiled-plus-runtime'],'all_seven_component_stages_exit0':True,'build_seconds':next(x['seconds'] for x in compiled['stages'] if x['stage']=='build'),'memory_peak_bytes':int(inner['final_cgroup']['memory.peak']),'memory_events':inner['final_cgroup']['memory.events'],'original_container_runner_launcher_watchdog_exit0':True,'target_execution':'UNRUN','artifacts':compiled['artifacts']})
for label,source in [('source01',Path('/tmp/m7-screenscraper-rejection-20261014')),('source02',Path('/tmp/m7-screenscraper-rejection-20261014-02'))]:
 target=root/(label+'.tar.gz')
 with tarfile.open(target,'w:gz') as archive:
  for p in sorted(source.rglob('*')):
   if p.is_file():archive.add(p,arcname=str(p.relative_to(source)),recursive=False)
 dump(root/(label+'.json'),{'execution_path':str(source),'execution_manifest_sha256':sha(source/'SHA256SUMS'),'archive_sha256':sha(target),'exact_original_bytes_preserved':True})
scratch=work/'es';assert scratch.resolve()==scratch and not scratch.is_symlink()
allocated=int(subprocess.check_output(['du','-s','-B1',str(scratch)]).split()[0]);shutil.rmtree(scratch)
dump(packet/'retirement.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'removed':str(scratch),'allocated_bytes_released':allocated,'exists_after':scratch.exists(),'artifacts_retained':str(work/'artifacts'),'release_when':'Immediately queued exact-source frontend screen proof accepted; bind final firmware separately.'})
shutil.copy2(Path(__file__),packet/'preserve-component.py')
(root/'README.md').write_text('ES3178b832b8d134198b2b4eede4f725d4ed283f8c passes both credential-mode syntax checks, a full345-task component build, strip and English/French catalogs. Build206.998s; peak3,765,743,616B; no OOM events. Original container/runner/launcher/watchdog0, actual owners exited, admission consumed and private compiler objects retired. Small binary/catalogs remain for immediately queued UI proof. Attempt01 retains its original limit-mismatch failure and closeout wording failure; no compiler/product test ran there. Original source packets and raw receipts are archived byte-preserving with identity manifests. Actual UI/provider/final firmware remain unqualified.\n')
(root/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(root))+'\n' for p in sorted(root.rglob('*')) if p.is_file() and p!=root/'SHA256SUMS'))
print(json.dumps({'status':'PASS','retired_bytes':allocated,'artifact_holder':str(work/'artifacts'),'packet':str(root)}))
