#!/usr/bin/env python3
import pathlib,hashlib,json,subprocess,socket,time,gzip,shutil,os,sys
O=pathlib.Path('/workspace/tmp/pixelelated-m7-walk527-03')
R=pathlib.Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18')
bundle=pathlib.Path(sys.argv[1]).resolve(strict=True)
subprocess.run([str(R/'tools/rasteratops-candidate-store'),'verify',str(bundle)],check=True)
manifest=json.loads((bundle/'manifest.json').read_text())
assert manifest['inputs']['distribution_commit']=='7f58b7b1c592908dcd0ba5987955e59aaa79fe66'
assert manifest['inputs']['emulationstation_commit']=='1d76b3da7da75794066df1c089931b890304da7a'
artifact_name='pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz'
IMG=bundle/artifact_name
started=time.monotonic()
for port in [10026,5912]:
 with socket.socket() as sock:sock.bind(('127.0.0.1',port))
for name in ['/tmp/rocknix-qemu-monitor-d.sock','/tmp/rocknix-qemu-serial-d.sock']:assert not pathlib.Path(name).exists(),name
with IMG.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
assert digest==manifest['files'][artifact_name]['sha256']
subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(O/'qa-key'),'-C','pixelelated-508-cf10-qa'],check=True)
with gzip.open(IMG,'rb') as src, (O/'image.img').open('wb') as dst:shutil.copyfileobj(src,dst,2**20)
subprocess.run(['qemu-img','convert','-f','raw','-O','qcow2',str(O/'image.img'),str(O/'vm.qcow2')],check=True)
subprocess.run(['qemu-img','resize',str(O/'vm.qcow2'),'16G'],check=True);(O/'image.img').unlink()
command=[str(R/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm'),'run','--headless','--daemonize','--gl','auto','--res','640x480','--ssh-port','10026','--vnc','12','--monitor','/tmp/rocknix-qemu-monitor-d.sock','--serial','/tmp/rocknix-qemu-serial-d.sock','--pidfile','/tmp/rocknix-qemu-d.pid','--mac','52:54:00:52:05:27',str(O/'vm.qcow2')]
subprocess.run(command,check=True)
subprocess.run([str(R/'tools/vm-serial'),'--socket','/tmp/rocknix-qemu-serial-d.sock','wait','--up-to','180'],check=True)
pub=(O/'qa-key.pub').read_text().strip()
subprocess.run([str(R/'tools/vm-serial'),'--socket','/tmp/rocknix-qemu-serial-d.sock','sh',"mkdir -p /storage/.ssh; chmod 700 /storage/.ssh; printf '%s\\n' '"+pub+"' > /storage/.ssh/authorized_keys; chmod 600 /storage/.ssh/authorized_keys"],check=True,stdout=subprocess.DEVNULL)
ssh=['ssh','-i',str(O/'qa-key'),'-p','10026','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
for i in range(30):
 ready=subprocess.run(ssh+['grep ^BUILD_ID= /etc/os-release'],capture_output=True,text=True)
 if ready.returncode==0:break
 time.sleep(2)
else:raise RuntimeError('QA SSH did not become ready')
assert '7f58b7b1c592908dcd0ba5987955e59aaa79fe66' in ready.stdout,ready.stdout
subprocess.run(ssh+['ip route replace blackhole 0.0.0.0/1; ip route replace blackhole 128.0.0.0/1; ip -6 route replace blackhole ::/1; ip -6 route replace blackhole 8000::/1; ip route; ip -6 route'],check=True,stdout=(O/'network-boundary.txt').open('w'))
installed=json.loads((R/'docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/stage01/install-manifest.json').read_text())
proof={}
for entry in installed['installed_files']:
 dest=entry['destination'];local=R/pathlib.Path(entry['source']).relative_to('/workspace/repos/rocknix')
 expected=hashlib.sha256(local.read_bytes()).hexdigest()
 got=subprocess.check_output(ssh+['sha256sum '+dest],text=True).split()[0]
 assert got==expected,(dest,got,expected);proof[dest]=got
for rel in ['usr/share/post-update','usr/bin/emulationstation','usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo','usr/bin/duckstation_screenshot_path','usr/bin/start_duckstation.sh','usr/lib/libcom_err.so.2']:
 local=R/'build.pixelelated-GENERIC_X64.x86_64/image/system'/rel
 expected=hashlib.sha256(local.read_bytes()).hexdigest()
 got=subprocess.check_output(ssh+['sha256sum /'+rel],text=True).split()[0]
 assert got==expected,(rel,got,expected);proof['/'+rel]=got
subprocess.run(ssh+['test ! -e /usr/bin/cloud_migrate_layout && test "$(stat -c %a /usr/bin/duckstation-sa)" = 755'],check=True)
runtime_catalog=subprocess.check_output(ssh+['sha256sum /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo'],text=True).split()[0]
assert runtime_catalog==proof['/usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo']
proof['/usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo']=runtime_catalog
(O/'installed-inclusion.json').write_text(json.dumps({'sha256':proof,'retired_migration_absent':True,'duckstation_mode':'755','source_overlays':False},indent=2)+'\n')
record={'image':str(IMG),'image_sha256':digest,'qemu_pid':int(pathlib.Path('/tmp/rocknix-qemu-d.pid').read_text()),'ssh_port':10026,'vnc_display':12,'monitor':'/tmp/rocknix-qemu-monitor-d.sock','serial':'/tmp/rocknix-qemu-serial-d.sock','resolution':'640x480','command':command,'elapsed_seconds':round(time.monotonic()-started,3),'disk_logical_bytes':(O/'vm.qcow2').stat().st_size,'disk_allocated_bytes':(O/'vm.qcow2').stat().st_blocks*512,'owner':'root527 exclusive','purpose':'#527 installed UI navigation; no product overlays','build_readback':ready.stdout.strip(),'qa_key':'guest01/qa-key; private key never archived'}
(O/'guest.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS',json.dumps(record),flush=True)
