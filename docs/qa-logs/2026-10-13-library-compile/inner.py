from pathlib import Path
import subprocess,json,os,time,resource,hashlib,shutil
r=Path('/work');old='/workspace/repos/rocknix.worktrees/m7-pixelelated';b=Path(old)/'build.pixelelated-GENERIC_X64.x86_64';es=b/'build/emulationstation-c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78';cwd=es/'.x86_64-rocknix-linux-gnu';tc=b/'toolchain';cmake=tc/'bin/cmake';ninja=tc/'bin/ninja';toolchain=tc/'etc/cmake-x86_64-rocknix-linux-gnu.conf'
result={'stages':[],'started':time.time(),'rc':1};commands={}
env=dict(os.environ,TMPDIR='/work/tmp',CCACHE_DISABLE='1',CCACHE_DIR='/work/tmp/ccache',PATH=str(tc/'bin')+':'+os.environ['PATH'])
def run(label,args,timeout=600,where=cwd):
 args=[str(x) for x in args];commands[label]=args;print('START '+label,flush=True);start=time.time();p=subprocess.run(args,cwd=where,env=env,timeout=timeout);result['stages'].append({'stage':label,'rc':p.returncode,'seconds':time.time()-start});print('END '+label+' '+str(p.returncode),flush=True);assert p.returncode==0,label
try:
 files=['es-app/src/ApiSystem.cpp','es-app/src/guis/GuiMenu.cpp','es-app/src/guis/GuiWifi.cpp','es-core/src/Settings.cpp','es-app/src/ThreadedHasher.cpp']
 run('syntax',['bash',r/'records/es-syntax-check','--root',b,'--tree','/source',*['/source/'+f for f in files]])
 run('configure ES',[cmake,'-S',es,'-B',cwd,'-DENABLE_RVZ_HASH=ON'])
 run('build ES',[ninja,'-j2','emulationstation'])
 shutil.copyfile(es/'emulationstation',r/'scratch/emulationstation')
 run('strip',[tc/'bin/x86_64-rocknix-linux-gnu-strip',r/'scratch/emulationstation'])
 for lang in ['fr','en_GB']:
  run('catalog '+lang,[tc/'bin/msgfmt','--check','-o',r/f'scratch/{lang}.mo',es/f'locale/lang/{lang}/LC_MESSAGES/emulationstation2.po'])
 fixture=r/'records/2026-10-13-rvz-source'
 for name,source,enabled in [('candidate','/source','ON'),('baseline','/baseline','OFF')]:
  build=r/'controls'/name
  run('configure hash '+name,[cmake,'-S',fixture,'-B',build,'-G','Ninja','-DCMAKE_TOOLCHAIN_FILE='+str(toolchain),'-DES_SOURCE='+source,'-DENABLE_RVZ_HASH='+enabled],where=r)
  run('compile hash '+name,[cmake,'--build',build,'--target','pix574-hash-control','--parallel','2'],where=r)
 retry=r/'controls/retry'
 run('configure retry',[cmake,'-S',fixture/'retry','-B',retry,'-G','Ninja','-DCMAKE_TOOLCHAIN_FILE='+str(toolchain),'-DES_SOURCE=/source'],where=r)
 run('compile retry',[cmake,'--build',retry,'--target','pix574-retry-control','--parallel','2'],where=r)
 run('save capabilities ASan UBSan',['python3',r/'records/2026-10-13-save-capability-source/capability_fixture.py','--es-src','/source','--output',r/'capability/run','--cxx','/usr/bin/g++'],timeout=100,where=r)
 result.update(rc=0,binary_sha256=hashlib.sha256((r/'scratch/emulationstation').read_bytes()).hexdigest(),binary_bytes=(r/'scratch/emulationstation').stat().st_size,catalogs={l:hashlib.sha256((r/f'scratch/{l}.mo').read_bytes()).hexdigest() for l in ['fr','en_GB']},target_controls={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [r/'controls/candidate/pix574-hash-control',r/'controls/baseline/pix574-hash-control',r/'controls/retry/pix574-retry-control']})
finally:
 result['ended']=time.time();result['max_child_rss_kib']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
 for label,path in [('cgroup_memory_peak','/sys/fs/cgroup/memory.peak'),('cgroup_memory_events','/sys/fs/cgroup/memory.events')]:
  p=Path(path);result[label]=p.read_text() if p.exists() else None
 (r/'compile-result.json').write_text(json.dumps(result,indent=2)+'\n');(r/'records/commands.json').write_text(json.dumps(commands,indent=2)+'\n')
raise SystemExit(result['rc'])
