from pathlib import Path
import hashlib,json,runpy,shutil,types
root=Path('/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders');out=Path('/tmp/pixelelated-508-edge-fixed01/artifacts')
m=runpy.run_path(str(root/'tools/pixelelated-cloud-folder-test'));args=types.SimpleNamespace(ref=None,rclone='/workspace/repos/rocknix.worktrees/generic-x64/build.ROCKNIX-GENERIC_X64.x86_64/image/system/usr/bin/rclone');results=[]
def finish(f,result):
 result['cloud_sha256']=m['digest_tree'](f.path/'cloud');result['config']=f.pointers();(f.path/'result.json').write_text(json.dumps(result,indent=2)+'\n');results.append(result)
 for name in ['argv','fired']:
  if (f.path/'ctl'/name).exists():shutil.copyfile(f.path/'ctl'/name,f.path/(name+'.log'))
 for name in ['repo','shim','storage','cloud','ctl','log','run']:shutil.rmtree(f.path/name)
 print('VERIFIED',result['source'],result['case'],result['rc'],flush=True)
for version in ['old','fixed']:
 source=(root/'projects/ROCKNIX/packages/network/rclone/sources/cloud_setup') if version=='old' else Path('/tmp/pixelelated-508-edge-fix/cloud_setup')
 for path in ['GAMES','Saves','/GAMES','Mine/Saves']:
  f=m['legacy'].Fixture(out/(version+'-empty-'+path.replace('/','_')),args);shutil.copyfile(source,f.path/'repo/cloud_setup');f.conf(path,'/Mine/Backups','/Mine/Content');f.directory(path);before=m['snapshot'](f);r=f.run('cloud_setup','--folder-state');state=m['facts'](r)['STATE'];expected='missing' if version=='old' and '/' not in path else 'ready';assert r.returncode==0 and state==expected and before==m['snapshot'](f),(version,path,r.stdout)
  finish(f,{'source':version,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'case':'empty '+path,'rc':r.returncode,'state':state,'expected':expected})
 for mode in ['direct','parent']:
  for rc in [3,4,5]:
   f=m['legacy'].Fixture(out/(version+'-'+mode+'-'+str(rc)),args);shutil.copyfile(source,f.path/'repo/cloud_setup');f.conf('/Mine/Saves','/Mine/Backups','/Mine/Content')
   if mode=='direct':inject='''if [ "$1 $2" = "lsf qa:/Mine/Saves" ]; then printf 'direct partial failure\\n' >> /ctl/fired; printf 'README.txt\\n'; exit RC; fi
'''
   else:inject='''if [ "$1 $2" = "lsf qa:/Mine/Saves" ]; then printf 'direct empty failure\\n' >> /ctl/fired; exit 5; fi
if [ "$1 $2 $3" = "lsf --dirs-only qa:/Mine/" ]; then printf 'parent partial failure\\n' >> /ctl/fired; printf 'Saves/\\n'; exit RC; fi
'''
   shim=f.path/'shim/rclone';shim.write_text(shim.read_text().replace('exec /rclone.real',inject.replace('RC',str(rc))+'exec /rclone.real'))
   r=f.run('cloud_setup','--seed-folders');assert (r.returncode==0)==(version=='old'),(version,mode,rc,r.returncode,r.stdout)
   assert (f.path/'ctl/fired').exists()
   if version=='fixed':assert 'OK /Mine/Saves' not in r.stdout and "COULDN'T BE CREATED" in r.stdout
   finish(f,{'source':version,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'case':mode+' partial listing exit'+str(rc),'rc':r.returncode,'output':r.stdout,'synthetic_provider_failure':True})
(out/'result.json').write_text(json.dumps({'status':'PASS expected old failures and fixed refusals','cases':results},indent=2)+'\n')
