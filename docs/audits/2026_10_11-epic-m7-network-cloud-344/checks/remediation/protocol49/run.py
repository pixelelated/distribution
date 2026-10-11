from pathlib import Path
import importlib.util,importlib.machinery,subprocess,os,json,hashlib,types
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections');O=Path('/workspace/tmp/pix540-protocol49')
os.environ['CLOUD_QA_STATE']='/tmp/pix537-qa-backends'

# Disposable local endpoint readiness, including an authenticated listing.
for protocol in ('webdav','sftp'):
 env=dict(os.environ,CLOUD_QA_BACKEND=protocol,CLOUD_QA_GUEST_HOST='127.0.0.1')
 with (O/(protocol+'-startup.log')).open('w') as log:
  subprocess.run([str(D/'tools/cloud-test-backend'),'up'],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 conf=O/(protocol+'-private.conf')
 try:
  conf.write_bytes(subprocess.check_output([str(D/'tools/cloud-test-backend'),'rclone-conf'],env=env));conf.chmod(0o600)
  name=subprocess.check_output([str(D/'tools/cloud-test-backend'),'remote-name'],env=env,text=True).strip()
  with (O/(protocol+'-readiness-private.log')).open('w') as log:
   r=subprocess.run(['rclone','--config',str(conf),'lsf',name+':','--max-depth','1','--contimeout','5s','--timeout','10s','--retries','1'],stdout=log,stderr=subprocess.STDOUT,timeout=30)
  assert r.returncode==0,protocol+' authenticated listing failed'
 finally:
  conf.unlink(missing_ok=True)
 print('PASS local '+protocol+' authenticated readiness',flush=True)

v.remote('cloud_oauth cancel >/dev/null 2>&1 || true; cp /storage/qa537/rclone-real /usr/bin/rclone; chmod 755 /usr/bin/rclone')
installed=[]
for name in ['cloud_connections.py','cloud_remote','cloud_oauth','cloud_setup','cloud_scan','cloud_backup','cloud_restore','cloud_content_backup','cloud_content_restore']:
 installed.append(v.install(D/'projects/ROCKNIX/packages/network/rclone/sources'/name,name))
installed.append(v.install(D/'projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool','backuptool'))
(O/'installed.json').write_text(json.dumps(installed,indent=2)+'\n')
subprocess.run(['python3','/tmp/pix537-reset-ui.py','en_US'],check=True)
def snapshot():
 return v.remote("python3 - <<'END'\nfrom pathlib import Path\nimport json,hashlib\nr=Path('/storage/.config/rclone');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None\nkeys=('SAVESPATH','SETTINGS_BACKUPS','SAVES_REMOTE','SETTINGS_REMOTE','CONTENT_REMOTE')\nprint(json.dumps({'config':h(r/'rclone.conf'),'active':h(r/'active-connection'),'paths':[x for x in Path('/storage/.config/cloud_sync.conf').read_text().splitlines() if x.partition('=')[0] in keys],'payload':h(Path('/storage/qa537/provider/save.srm'))},sort_keys=True))\nEND")
for backend,selection in [('webdav','spare'),('sftp','')]:
 if selection:v.remote('cloud_remote select '+selection)
 else:v.remote("printf '\\n' > /storage/.config/rclone/active-connection")
 before=snapshot();args=[str(D/'tools/cloud-round-trip'),'--host','root@127.0.0.1','--port',str(v.G['ssh_port']),'--identity',v.G['ssh_identity'],'--backend',backend]
 print('START actual transfer suite',backend,flush=True)
 with (O/(backend+'.log')).open('w') as log:p=subprocess.run(args,env=os.environ,stdout=log,stderr=subprocess.STDOUT)
 after=snapshot();(O/(backend+'-result.json')).write_text(json.dumps({'returncode':p.returncode,'before':json.loads(before),'after':json.loads(after),'restored':before==after},indent=2)+'\n')
 assert before==after,'prior configuration/selection/folders/payload not restored'
 p.check_returncode();print('PASS actual transfer and previous selection restored',backend,flush=True)
# Exercise the third on-disk shape through the real prepare/restore functions.
os.environ['CLOUD_QA_BACKEND']='webdav'
loader=importlib.machinery.SourceFileLoader('roundtrip',str(D/'tools/cloud-round-trip'));spec=importlib.util.spec_from_loader(loader.name,loader);rt=importlib.util.module_from_spec(spec);loader.exec_module(rt)
v.remote('rm -f /storage/.config/rclone/active-connection');before=snapshot();prepared=[];args=types.SimpleNamespace(real_roms=False,keep=False)
dev=rt.Device('root@127.0.0.1',v.G['ssh_port'],v.G['ssh_identity'])
try:
 p=rt.prepare_device(dev,rt.backend('remote-name').strip(),rt.SCRATCH,args,prepared)
 assert dev.run('stat -c %a /storage/.config/rclone/active-connection').strip()=='600'
finally:
 for p in prepared:rt.restore_device(p,args,rt.SCRATCH+'/backup/'+rt.ARCHIVE_NAME)
after=snapshot();assert before==after
(O/'absent-selection-result.json').write_text(json.dumps({'before':json.loads(before),'after':json.loads(after),'restored':True},indent=2)+'\n')
print('PASS absent, explicit empty and selected connection restoration',flush=True)
