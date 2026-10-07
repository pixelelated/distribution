from pathlib import Path
import hashlib,json,os,shlex,subprocess,time
O=Path('/tmp/pixelelated-m7-migration-copy02'); E=Path('/home/max/Development/emulationstation-next.worktrees/m7-migration-copy')
B=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64'); D=B/'build/emulationstation-72494bc72e3d64d4dcfeb4e6478052bbdf166c5b/.x86_64-rocknix-linux-gnu'
OLD='/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64'
def sha(p):return hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
def record(inputs,path):
 vals=[]
 for p in sorted(set(inputs)):
  p=Path(p)
  if p.is_file(): vals.append(dict(path=str(p),sha256=sha(p),size=p.stat().st_size))
 path.write_text(json.dumps(vals,indent=2)+'\n');return vals
ninja=B/'toolchain/bin/ninja'; obj='es-app/CMakeFiles/emulationstation.dir/src/guis/GuiMenu.cpp.o'
cmds={}
for name,target in [('compile',obj),('link','emulationstation')]:
 raw=subprocess.check_output([str(ninja),'-C',str(D),'-t','commands',target],text=True).splitlines()[-1]
 cmds[name]=raw
 a=shlex.split(raw.replace(OLD,str(B)))
 if name=='link':
  assert a[:2]==[':','&&'] and a[-2:]==['&&',':'];a=a[2:-2]
  assert a.count(obj)==1;a[a.index(obj)]=str(O/'GuiMenu.cpp.o')
  a[a.index('-o')+1]=str(O/'emulationstation')
  a+=['-Wl,-t']
 else:
  a[a.index('-o')+1]=str(O/'GuiMenu.cpp.o')
  a[a.index('-c')+1]=str(E/'es-app/src/guis/GuiMenu.cpp')
  a[a.index('-MF')+1]=str(O/'GuiMenu.cpp.o.d')
  a[a.index('-MT')+1]=str(O/'GuiMenu.cpp.o')
  firstI=next(i for i,t in enumerate(a) if t.startswith('-I'))
  a[firstI:firstI]=['-I'+str(E/'es-core/src'),'-I'+str(E/'es-app/src')]
 cmds[name+'_argv']=a
(O/'artifacts/commands.json').write_text(json.dumps(dict(cwd=str(D),commands=cmds),indent=2)+'\n')
originals=[D/t for t in cmds['link_argv'] if not t.startswith('-') and (D/t).is_file()]
originals += [E/'es-app/src/guis/GuiMenu.cpp',E/'locale/lang/fr/LC_MESSAGES/emulationstation2.po',D/'build.ninja']
prior=record(originals,O/'artifacts/inputs-before.json')
for name in ['compile','link']:
 print(time.strftime('%FT%TZ',time.gmtime()),name,flush=True)
 with open(O/('artifacts/'+name+'.log'),'w') as f:
  subprocess.run(cmds[name+'_argv'],cwd=D,env={**os.environ,'CCACHE_DISABLE':'1'},stdout=f,stderr=subprocess.STDOUT,check=True)
 print(name,'PASS',flush=True)
after=record(originals,O/'artifacts/inputs-after.json');assert prior==after,'a reused input changed during compile/link'
record([O/'GuiMenu.cpp.o',O/'emulationstation'],O/'artifacts/outputs.json')
print('PASS owner-local ES compiled and linked; reused explicit objects/library inputs unchanged',flush=True)
