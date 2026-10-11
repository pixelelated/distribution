from pathlib import Path
import hashlib,json,os,re,subprocess
p=Path(__file__).resolve().parent;r=Path('/workspace/repos/rocknix.worktrees/m7-component-inputs');pkg=r/'projects/ROCKNIX/packages/emulators/libretro/retroarch'
recipe=(pkg/'package.mk').read_text();pin=re.search(r'^PKG_VERSION="([0-9a-f]+)"',recipe,re.M).group(1)
archive=Path('/workspace/cache/rocknix-sources/retroarch')/('retroarch-'+pin+'.tar.gz')
subprocess.run(['tar','-xzf',str(archive),'-C',str(p/'src'),'--strip-components=1','--wildcards','*.h','*.c','*.cpp','*/version.all'],check=True,stderr=subprocess.DEVNULL)
rows=[];oldenv=dict(os.environ);oldenv.pop('TMPDIR',None);newenv={**oldenv,'TMPDIR':str(p/'tmp')}
for patch in list(sorted((pkg/'patches').glob('*.patch')))+list(sorted((pkg/'patches/batteryplus').glob('*.patch'))):
 name=str(patch.relative_to(pkg/'patches'));entry={'patch':name,'sha256':hashlib.sha256(patch.read_bytes()).hexdigest()};cmd=['patch','-d',str(p/'src'),'-p1','-N','--fuzz=0','--dry-run','-r','-']
 if patch.name.startswith('0011-video-thread-') or re.match(r'00(1[3-9]|[2-9][0-9])-',patch.name):
  for label,env in [('original',oldenv),('owned-temp',newenv)]:
   result=subprocess.run(cmd,input=patch.read_bytes(),env=env,capture_output=True);(p/(name.replace('/','_')+'.'+label+'.log')).write_bytes(result.stdout+result.stderr);entry[label]=result.returncode
  assert entry['owned-temp']==0,entry
  assert b'with fuzz' not in (p/(name.replace('/','_')+'.owned-temp.log')).read_bytes()
 result=subprocess.run(['patch','-d',str(p/'src'),'-p1','-N','--no-backup-if-mismatch','-r','-'],input=patch.read_bytes(),env=newenv,capture_output=True)
 (p/(name.replace('/','_')+'.apply.log')).write_bytes(result.stdout+result.stderr);entry['apply']=result.returncode;assert result.returncode==0,entry
 rows.append(entry);(p/'result.json').write_text(json.dumps(rows,indent=2)+'\n')
failed=[x for x in rows if x.get('original',0)!=0]
assert {x['patch'] for x in failed}=={'0013-cheevos-offline-proxy-toast.patch','0018-auto-slot-survives-content-load.patch'},failed
for x in failed:
 log=(p/(x['patch']+'.original.log')).read_text();assert 'Disk quota exceeded' in log or 'No space left on device' in log,log
print('PASS original failures are host temporary-file quota; all ordered patches and zero-fuzz controls pass with owned temporary directory',flush=True)
