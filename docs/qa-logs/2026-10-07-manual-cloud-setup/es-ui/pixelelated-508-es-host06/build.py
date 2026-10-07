from pathlib import Path
import hashlib,json,os,shlex,subprocess,time
O=Path('/tmp/pixelelated-508-es-host06'); E=Path('/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup')
B=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64'); D=B/'build/emulationstation-72494bc72e3d64d4dcfeb4e6478052bbdf166c5b/.x86_64-rocknix-linux-gnu'
OLD='/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64'
def sha(p):return hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
def record(inputs,path):
 vals=[dict(path=str(p),sha256=sha(p),size=p.stat().st_size) for p in sorted(set(Path(i) for i in inputs)) if p.is_file()];path.write_text(json.dumps(vals,indent=2)+'\n');return vals
files=[x for x in subprocess.check_output(['git','diff','--name-only'],cwd=E,text=True).splitlines() if x.startswith('es-app/src/') and x.endswith('.cpp')]
cmds={};replacements={};ninja=B/'toolchain/bin/ninja'
for f in files:
 obj='es-app/CMakeFiles/emulationstation.dir/'+f.removeprefix('es-app/')+'.o';out=(O if f.endswith('/GuiMenu.cpp') else Path('/tmp/pixelelated-508-es-host04'))/(Path(f).name+'.o');replacements[obj]=str(out)
 raw=subprocess.check_output([ninja,'-C',D,'-t','commands',obj],text=True).splitlines()[-1]
 a=shlex.split(raw.replace(OLD,str(B)));a[a.index('-o')+1]=str(out);a[a.index('-c')+1]=str(E/f);a[a.index('-MF')+1]=str(out)+'.d';a[a.index('-MT')+1]=str(out)
 firstI=next(i for i,t in enumerate(a) if t.startswith('-I'));a[firstI:firstI]=['-I'+str(E/'es-core/src'),'-I'+str(E/'es-app/src')];a+=['--sysroot='+str(B/'toolchain/x86_64-rocknix-linux-gnu/sysroot')];cmds[f]=a
raw=subprocess.check_output([ninja,'-C',D,'-t','commands','emulationstation'],text=True).splitlines()[-1];a=shlex.split(raw.replace(OLD,str(B)));assert a[:2]==[':','&&'] and a[-2:]==['&&',':'];a=a[2:-2];a=[replacements.get(t,t) for t in a];a=[('-Wl,--dependency-file='+str(O/'link.d')) if t.startswith('-Wl,--dependency-file=') else t for t in a];a[a.index('-o')+1]=str(O/'emulationstation');a+=['-Wl,-t','--sysroot='+str(B/'toolchain/x86_64-rocknix-linux-gnu/sysroot')];cmds['link']=a
inputs=[D/t for t in a if not t.startswith('-') and (D/t).is_file()]+[E/f for f in files]+[D/'build.ninja',E/'es-app/src/CloudText.h',E/'es-app/src/guis/GuiMenu.h',E/'locale/lang/fr/LC_MESSAGES/emulationstation2.po']
(O/'artifacts/commands.json').write_text(json.dumps({'cwd':str(D),'commands':cmds},indent=2)+'\n');before=record(inputs,O/'artifacts/inputs-before.json')
for name,args in cmds.items():
 if name not in ['es-app/src/guis/GuiMenu.cpp','link']:continue
 print(time.strftime('%FT%TZ',time.gmtime()),name,flush=True)
 with open(O/'artifacts'/(Path(name).name+'.log'),'w') as f:subprocess.run(args,cwd=D,env={**os.environ,'CCACHE_DISABLE':'1'},stdout=f,stderr=subprocess.STDOUT,check=True)
 print(name,'PASS',flush=True)
after=record(inputs,O/'artifacts/inputs-after.json');assert before==after,'reused input modified'
record([O/'emulationstation',O/'artifacts/fr.mo'],O/'artifacts/outputs.json');print('PASS compile/link and unchanged accepted inputs',flush=True)
