import pathlib,subprocess,json,time
P=pathlib.Path;R=P('/workspace/repos/rocknix.worktrees/conflict-resolution');V=P('/workspace/tmp/pixelelated-m7-alignment-runtime-01');O=P('/workspace/tmp/pixelelated-m7-alignment-power-02')
ssh=['ssh','-i',str(V/'qa-key'),'-p','10251','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
with (O/'artifacts/prepare.log').open('wb') as f:
 subprocess.run(ssh+['python3 -I -B -'],input=(O/'prepare.py').read_bytes(),stdout=f,stderr=subprocess.STDOUT,check=True)
subprocess.run(ssh+['cat > /storage/qa519/power2/transaction-source.py'],input=(O/'transaction-source.py').read_bytes(),check=True)
old=int((V/'vm.pid').read_text());g=json.loads((V/'guest.json').read_text())
subprocess.run([str(R/'tools/vm-stop'),str(V/'vm.pid'),str(V/'vm.qcow2')],check=True)
assert not P('/proc',str(old)).exists() or not P('/proc',str(old),'cmdline').read_bytes()
subprocess.run(g['command'],check=True);new=int((V/'vm.pid').read_text());assert new!=old
subprocess.run([str(R/'tools/vm-serial'),'--socket','/tmp/pix519-01-ser.sock','wait','--for','test -f /storage/qa519/power2/checkpoint.json','--up-to','180'],check=True)
for _ in range(60):
 p=subprocess.run(ssh+['test -f /storage/qa519/power2/checkpoint.json'],capture_output=True)
 if p.returncode==0:break
 time.sleep(.5)
else:raise RuntimeError('SSH did not return')
subprocess.run(ssh+['ip route replace blackhole 0.0.0.0/1 && ip route replace blackhole 128.0.0.0/1 && ip -6 route replace blackhole ::/1 && ip -6 route replace blackhole 8000::/1'],check=True)
p=subprocess.run(ssh+['python3 -I -B -'],input=(O/'guest-proof.py').read_bytes(),stdout=(O/'artifacts/guest-proof.log').open('wb'),stderr=subprocess.STDOUT)
(O/'guest-command.rc').write_text(str(p.returncode)+'\n')
subprocess.run(ssh+['tar -C /storage/qa519/power2 -czf - .'],stdout=(O/'artifacts/results.tar.gz').open('wb'),check=True)
(O/'artifacts/qemu-lifecycle.json').write_text(json.dumps({'old_pid':old,'new_pid':new,'old_exited_before_restart':True,'command':g['command'],'no_guest_shutdown_requested':True},indent=2)+'\n')
raise SystemExit(p.returncode)
