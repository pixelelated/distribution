from pathlib import Path
import subprocess,json,hashlib,time,os
P=Path('/workspace/tmp/pixelelated-m7-usb-531-02')
R=Path('/workspace/repos/rocknix.worktrees/m7-p5-usb-revision')
opts=['-i',str(P/'qa-key'),'-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5']
def ssh(s): return subprocess.run(['ssh',*opts,'-p','10331','root@127.0.0.1',s],capture_output=True,text=True,timeout=60)
def copy(src,dst): subprocess.run(['scp','-q',*opts,'-P','10331',str(src),'root@127.0.0.1:'+dst],check=True,timeout=30)
def dump(name,obj): (P/name).write_text(json.dumps(obj,indent=2)+'\n')
try:
 subprocess.run(['/usr/bin/python3','-I','-u',str(P/'create.py')],check=True,timeout=300)
 protected='sha256sum /storage/.config/system/configs/system.cfg /storage/.config/emulationstation/es_settings.cfg /storage/.cache/systemd-machine-id'
 before=ssh(protected);assert before.returncode==0; (P/'protected-before.txt').write_text(before.stdout)
 kernel=ssh('zcat /proc/config.gz | grep CONFIG_USB_GADGET');dump('guest-kernel.json',{'returncode':kernel.returncode,'stdout':kernel.stdout,'stderr':kernel.stderr})
 # /proc/config.gz is optional; the frozen input config is retained separately.
 source_config=(P/'frozen-linux.config').read_text();assert '# CONFIG_USB_GADGET is not set' in source_config
 gadget=ssh('test -d /sys/kernel/config/usb_gadget');dump('guest-gadget-presence.json',{'returncode':gadget.returncode,'configfs_gadget_directory_present':gadget.returncode==0,'frozen_config_sha256':hashlib.sha256((P/'frozen-linux.config').read_bytes()).hexdigest(),'kernel_config_exposed':kernel.returncode==0})
 copy(R/'tools/usb-gadget-test','/tmp/pix531-test')
 copy(R/'projects/ROCKNIX/packages/rocknix/sources/scripts/usbgadget','/tmp/pix531-usbgadget')
 h=ssh('sha256sum /tmp/pix531-test /tmp/pix531-usbgadget');assert h.returncode==0;(P/'guest-source-hashes.txt').write_text(h.stdout)
 assert h.stdout.splitlines()[0].split()[0]==hashlib.sha256((R/'tools/usb-gadget-test').read_bytes()).hexdigest()
 assert h.stdout.splitlines()[1].split()[0]==hashlib.sha256((R/'projects/ROCKNIX/packages/rocknix/sources/scripts/usbgadget').read_bytes()).hexdigest()
 results=[]
 for name,source,expected in [('old','/usr/bin/usbgadget',1),('fixed','/tmp/pix531-usbgadget',0)]:
  r=ssh('python3 -I /tmp/pix531-test --source '+source+' --shell /bin/sh --output /tmp/pix531-'+name+'.json')
  results.append({'name':name,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});dump('test-results.json',results)
  print(name,r.returncode,r.stdout,flush=True);assert r.returncode==expected,results[-1]
  read=ssh('cat /tmp/pix531-'+name+'.json');assert read.returncode==0
  data=json.loads(read.stdout);dump(name+'.json',data)
  assert all(c['checks']['function_exited_zero'] and c['checks']['other_descriptor_bytes_and_links_preserved'] for c in data['cases'])
 after=ssh(protected);assert after.returncode==0 and after.stdout==before.stdout;(P/'protected-after.txt').write_text(after.stdout)
 dump('acceptance.json',{'passed':True,'old_control_exit':1,'fixed_exit':0,'fixed_checks':72,'fixture_only':True,'physical_enumeration':False,'protected_hashes_equal':True,'source_overlay_not_new_firmware':True})
 print('PASS guest source-bound USB fixture and retained settings; no hardware enumeration claim',flush=True)
finally:
 if (P/'vm.pid').exists():
  subprocess.run([str(R/'tools/vm-stop'),str(P/'vm.pid'),str(P/'vm.qcow2')],check=True,timeout=50)
 retired=[]
 for name in ['vm.qcow2','vm.vars.fd','vm.vars4.fd','vm.uefi-vars.fd','vm.ovmf-vars.fd','qa-key','qa-key.pub','image.img']:
  f=P/name
  if f.exists():
   retired.append({'path':str(f),'allocated_bytes':f.stat().st_blocks*512});f.unlink()
 dump('retirement.json',{'removed':retired,'allocated_bytes_released':sum(x['allocated_bytes'] for x in retired),'guest_stopped_by_bound_pidfile':not (P/'vm.pid').exists()})
