from pathlib import Path
import subprocess,json,hashlib,os,time,stat
base=Path('/tmp/pix581-mounted');out=Path('/storage/qa581-mounted');base.mkdir();out.mkdir();records={'rc':1,'started':time.time(),'cases':[]};helper=Path('/run/qa581-source/projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/dolphin-save-paths')
assert hashlib.sha256(helper.read_bytes()).hexdigest()=='9a30fb496132411444b8d3a0b4cb4b3f2fba6e0e6e688667a0083136c3d59895'
def call(args):return subprocess.run(args,check=True,capture_output=True,text=True,timeout=15)
def protected(root):
 return {str(p.relative_to(root)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'inode':p.stat().st_ino,'mode':stat.S_IMODE(p.stat().st_mode)} for p in root.rglob('*') if p.is_file() and not p.is_symlink()}
def run(root,system,name,expected):
 before=protected(root);p=subprocess.run(['python3','-I','-S','-B',str(helper),'prepare',system,'--storage',str(root),'--lock',str(out/'lock'),'--error-file',str(out/'launch_error.log')],capture_output=True,text=True,timeout=40)
 (out/(name+'.stdout')).write_text(p.stdout);(out/(name+'.stderr')).write_text(p.stderr);after=protected(root)
 records['cases'].append({'name':name,'rc':p.returncode,'expected':expected,'before':before,'after':after})
 assert p.returncode==expected,(name,p.returncode,p.stderr)
 for k,v in before.items():assert after[k]==v,(name,k)
 if expected==250:assert (out/'launch_error.log').read_text().startswith('DOLPHIN DID NOT START\n')
try:
 call(['mount','--make-rprivate','/']);call(['mount','-t','tmpfs','-o','size=128M,mode=700','tmpfs',str(base)])
 root=base/'storage';(root/'roms').mkdir(parents=True);conf=root/'.config/dolphin-emu';(conf/'GC').mkdir(parents=True);(conf/'GC/font_western.bin').write_bytes(b'synthetic resource')
 call(['mount','--bind',str(root/'roms'),str(root/'roms')])
 records['mountinfo_before']=Path('/proc/self/mountinfo').read_text();records['helper_sha256']=hashlib.sha256(helper.read_bytes()).hexdigest()
 run(root,'gamecube','clean-gc',0)
 for region in ['EUR','JAP','USA']:
  for slot in ['A','B']:
   p=conf/'GC'/('MemoryCard'+slot+'.'+region+'.raw');assert p.is_symlink();data=('synthetic card '+region+slot).encode();p.write_bytes(data);assert (root/'roms/bios/GC'/p.name).read_bytes()==data
 records['card_link_writes']=6
 (root/'roms/savestates/gamecube/retained.state').write_bytes(b'GC state')
 run(root,'wii','switch-wii',0);assert (conf/'StateSaves').resolve()==root/'roms/savestates/wii'
 (root/'roms/savestates/wii/retained.state').write_bytes(b'Wii state')
 run(root,'gamecube','switch-back-gc',0);assert (conf/'StateSaves').resolve()==root/'roms/savestates/gamecube'
 (conf/'StateSaves').unlink();(conf/'StateSaves').mkdir();(conf/'StateSaves/ambiguous.state').write_bytes(b'keep real save')
 run(root,'gamecube','retained-real-state',250)
 # Leave real conflicting data untouched in this tree. A second clean root tests mounts.
 second=base/'second';(second/'roms').mkdir(parents=True);(second/'.config/dolphin-emu/GC').mkdir(parents=True)
 call(['mount','--bind',str(second/'roms'),str(second/'roms')]);run(second,'gamecube','second-clean',0)
 call(['mount','--bind',str(second/'roms/savestates'),str(second/'roms/savestates')]);run(second,'gamecube','nested-save-mount',250);call(['umount',str(second/'roms/savestates')])
 call(['mount','-o','remount,bind,ro',str(second/'roms')]);run(second,'gamecube','read-only-roms',250);call(['mount','-o','remount,bind,rw',str(second/'roms')]);call(['umount',str(second/'roms')]);run(second,'gamecube','missing-roms-mount',250)
 records['rc']=0
finally:
 records['ended']=time.time();(out/'result.json').write_text(json.dumps(records,indent=2)+'\n')
raise SystemExit(records['rc'])
