from pathlib import Path
import subprocess,json,os,time,resource,hashlib
r=Path('/work'); commands=json.loads((r/'records/commands.json').read_text()); old='/workspace/repos/rocknix.worktrees/m7-pixelelated'; b=Path(old)/'build.pixelelated-GENERIC_X64.x86_64';es=b/'build/emulationstation-c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78';cwd=es/'.x86_64-rocknix-linux-gnu'
result={'stages':[],'started':time.time(),'rc':1}
def run(label,args,where=cwd):
 print('START '+label,flush=True);p=subprocess.run(args,cwd=where,env=dict(os.environ,TMPDIR='/work/tmp'),timeout=600);result['stages'].append({'stage':label,'rc':p.returncode});print('END '+label+' '+str(p.returncode),flush=True);assert p.returncode==0,label
try:
 run('syntax',['bash','/work/records/es-syntax-check','--root',str(b),'--tree','/source','/source/es-app/src/ApiSystem.cpp'])
 run('compile',['bash','-euc',commands['object']])
 run('link',['bash','-euc',commands['link']])
 candidate=es/'emulationstation';output=r/'scratch/emulationstation'
 run('strip',['/bin/cp',str(candidate),str(output)])
 run('strip-debug',[str(b/'toolchain/bin/x86_64-rocknix-linux-gnu-strip'),str(output)])
 dump=subprocess.check_output([str(b/'toolchain/bin/x86_64-rocknix-linux-gnu-objdump'),'-dC',str(es/'.x86_64-rocknix-linux-gnu/es-app/CMakeFiles/emulationstation.dir/src/ApiSystem.cpp.o')],text=True)
 (r/'records/ApiSystem.disassembly.txt').write_text(dump)
 symbols=subprocess.check_output([str(b/'toolchain/bin/x86_64-rocknix-linux-gnu-readelf'),'-Ws',str(output)],text=True)
 assert 'malloc_trim@' in symbols,'missing trim symbol'
 (r/'records/binary-symbols.txt').write_text(symbols)
 result.update(rc=0,binary_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),binary_bytes=output.stat().st_size)
finally:
 result['ended']=time.time();result['max_child_rss_kib']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
 for label,path in [('cgroup_memory_peak','/sys/fs/cgroup/memory.peak'),('cgroup_memory_events','/sys/fs/cgroup/memory.events')]:
  p=Path(path);result[label]=p.read_text() if p.exists() else None
 (r/'compile-result.json').write_text(json.dumps(result,indent=2)+'\n')
