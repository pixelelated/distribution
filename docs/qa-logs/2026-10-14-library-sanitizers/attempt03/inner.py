from pathlib import Path
import subprocess,json,os,time,hashlib,shutil,resource,shlex
r=Path('/work');old=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated');b=old/'build.pixelelated-GENERIC_X64.x86_64';tc=b/'toolchain';packet=r/'records/wii-composition/docs/qa-logs/2026-10-13-rvz-regression-source';result={'rc':1,'stages':[],'started':time.time()};commands={}
env=dict(os.environ,TMPDIR='/work/tmp',CCACHE_DISABLE='1',CCACHE_DIR='/work/tmp/ccache',PATH=str(tc/'bin')+':'+os.environ['PATH'])
def run(label,args,timeout=480):
 args=[str(x) for x in args];commands[label]=args;print('START '+label,flush=True);start=time.time();p=subprocess.run(args,env=env,cwd=r,timeout=timeout);result['stages'].append({'stage':label,'rc':p.returncode,'seconds':time.time()-start});assert p.returncode==0,label
try:
 for name,source,enabled,probe in [('candidate','/source','ON','ON'),('baseline','/baseline','OFF','OFF')]:
  build=r/'builds'/name
  run('configure '+name,[tc/'bin/cmake','-S',packet/'cmake-all-direct-contracts','-B',build,'-G','Ninja','-DCMAKE_TOOLCHAIN_FILE='+str(tc/'etc/cmake-x86_64-rocknix-linux-gnu.conf'),'-DES_SOURCE='+source,'-DENABLE_RVZ_HASH='+enabled,'-DPIX574_SANITIZE=ON','-DPIX574_READER_PROBE='+probe,'-DCMAKE_EXPORT_COMPILE_COMMANDS=ON'])
  # Inspect actual evaluated compiler contract before another compiler is started.
  database=json.loads((build/'compile_commands.json').read_text())
  def flags(e):
   words=shlex.split(e['command']);return {w for w in words if w.startswith(('-I','-D'))}
  checks=[]
  pairs=[('hash_disc.c','wii-partition-probe.c')]
  if name=='candidate':pairs.append(('rvz_hash.cpp','rvz-reader-probe.cpp'))
  for product,consumer in pairs:
   prod=next(e for e in database if Path(e['file']).name==product)
   use=next(e for e in database if Path(e['file']).name==consumer)
   missing=sorted(flags(prod)-flags(use));checks.append({'product':product,'consumer':consumer,'missing':missing})
  bad=[e['file'] for e in database if '-fsanitize=address,undefined' not in shlex.split(e['command'])]
  report={'direct_source_contracts':checks,'uninstrumented_translation_units':bad,'translation_units':len(database)}
  (r/'records'/('contract-'+name+'.json')).write_text(json.dumps(report,indent=2)+'\n')
  assert not bad and all(not e['missing'] for e in checks),report
  assert (name=='candidate')==any(Path(e['file']).name=='rvz-reader-probe.cpp' for e in database)
  assert all(('-DHAVE_RVZ_HASH' in flags(e))==(name=='candidate') for e in database if Path(e['file']).name in ('hash_disc.c','wii-partition-probe.c'))
  targets=['pix574-regression-hash','pix574-wii-partition-probe','pix574-public-wii-trace']
  if name=='candidate':targets+=['pix574-fixture-writer','pix574-rvz-reader-probe','pix574-padding-oracle']
  run('compile '+name,[tc/'bin/cmake','--build',build,'--parallel','1','--target',*targets])
  dest=r/'artifacts'/name;dest.mkdir()
  for target in targets:
   compiled=build/'wii-controls'/target if target=='pix574-public-wii-trace' else build/'wii-controls/sealed-controls'/target
   shutil.copyfile(compiled,dest/target);(dest/target).chmod(0o755)
  shutil.copyfile(build/'compile_commands.json',r/'records'/('compile_commands-'+name+'.json'))
 # Exact target sanitizer runtimes are staged with the probes, never installed globally.
 libdir=tc/'x86_64-rocknix-linux-gnu/lib';dest=r/'artifacts/lib';dest.mkdir()
 result['sanitizer_runtime_sources']={}
 for soname,filename in [('libasan.so.8','libasan.so.8.0.0'),('libubsan.so.1','libubsan.so.1.0.0')]:
  src=libdir/filename;shutil.copyfile(src,dest/soname)
  result['sanitizer_runtime_sources'][soname]={'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
 run('French catalog',[tc/'bin/msgfmt','--check','-o',r/'artifacts/fr.mo','/copy/locale/lang/fr/LC_MESSAGES/emulationstation2.po'],timeout=30)
 result['artifacts']={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (r/'artifacts').rglob('*') if p.is_file()}
 result['rc']=0
finally:
 result['ended']=time.time();result['max_child_rss_kib']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
 for key,path in [('memory_peak','/sys/fs/cgroup/memory.peak'),('memory_events','/sys/fs/cgroup/memory.events')]:
  p=Path(path);result[key]=p.read_text() if p.exists() else None
 (r/'compile-result.json').write_text(json.dumps(result,indent=2)+'\n');(r/'records/commands.json').write_text(json.dumps(commands,indent=2)+'\n')
raise SystemExit(result['rc'])
