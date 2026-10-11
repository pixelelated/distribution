from pathlib import Path
import importlib.util,sys,json,subprocess,time
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
lang,size=sys.argv[1:3];O=Path('/tmp/pix537-ui21')/(lang[:2]+size);O.mkdir(parents=True,exist_ok=True)
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections')
def walk(label,steps):
 p=O/(label+'.steps');p.write_text(steps)
 subprocess.run([str(D/'tools/vm-visual-qa'),'--monitor',str(v.O/'monitor.sock'),'run',str(p),'--outdir',str(O/label)],check=True)
def prep():subprocess.run(['python3','/tmp/pix537-forms-prepare21.py',lang,size],check=True)
prep()
before=v.remote('sha256sum /storage/.config/rclone/active-connection /storage/.config/cloud_sync.conf /storage/qa537/provider/save.srm')
walk('edit',Path('/tmp/pix537-edit.steps').read_text())
walk('saved',Path('/tmp/pix537-edit-save.steps').read_text())
after=v.remote('sha256sum /storage/.config/rclone/active-connection /storage/.config/cloud_sync.conf /storage/qa537/provider/save.srm')
assert before==after
assert v.remote('cloud_remote active').strip()=='dropbox:'
result=json.loads(v.remote("rclone config dump"))
assert result['spare']['remote']=='/storage/qa537/provider' and result['dropbox']['type']=='dropbox'
receipt={'unchanged_selection_paths_and_payload':before.splitlines(),'blank_edit_kept_alias_path':True,'es_sha256':v.remote('sha256sum /usr/bin/emulationstation').split()[0],'fr_catalog_sha256':v.remote('sha256sum /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo').split()[0]}
prep()
walk('add-name',Path('/tmp/pix537-add09.steps').read_text())
(O/'forms.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS form save, retained settings and separate add page',lang,size,flush=True)
