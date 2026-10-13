from pathlib import Path
import subprocess,json,time,datetime
r=Path('/workspace/tmp/pix-m7-baseline-tests-20261013');ssh=json.loads((r/'ssh-command.json').read_text());result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rc':1}
def run(args,timeout=120,**kw):return subprocess.run(args,check=True,timeout=timeout,**kw)
try:
 run(['tools/vm-stop',str(r/'vm.pid'),str(r/'disk.qcow2')])
 run(['python3','projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm','run',str(r/'disk.qcow2'),'--headless','--daemonize','--gl','auto','--res','1280x800','--ssh-port','10580','--vnc','74','--pidfile',str(r/'vm.pid'),'--serial',str(r/'serial.sock'),'--monitor',str(r/'monitor.sock'),'--ovmf-vars',str(r/'OVMF.fd')])
 run(['tools/vm-serial','--socket',str(r/'serial.sock'),'wait','--up-to','180'],timeout=190)
 run(ssh+['mount --bind /storage/qa-m7-baseline/wifictl /usr/bin/wifictl'])
 run(ssh+['cat > /storage/qa-m7-baseline/wifi-mode.json'],input=json.dumps({'delay':12,'outcome':'networks','count':3}).encode())
 (r/'large-identities.txt').write_bytes(run(ssh+['cat /proc/sys/kernel/random/boot_id; sha256sum /usr/bin/emulationstation'],capture_output=True).stdout)
 steps=r/'wifi-large.steps';steps.write_text('wake\nkey ret\nwait-for-change\nkey up x6\nkey x\nwait-for-change\nsettle\nshot network-settings\nkey down x5\nkey x\nwait 1\nshot initial-search\nwait 13\nsettle\nshot initial-results\n')
 run(['tools/vm-visual-qa','--monitor',str(r/'monitor.sock'),'run',str(steps),'--outdir',str(r/'wifi-large')],timeout=80)
 (r/'wifi-large-calls.jsonl').write_bytes(run(ssh+['cat /storage/qa-m7-baseline/wifi-calls.jsonl'],capture_output=True).stdout)
 result['rc']=0
finally:
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'wifi-large-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
