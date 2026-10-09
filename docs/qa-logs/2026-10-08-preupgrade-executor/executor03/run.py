import pathlib,subprocess,json
O=pathlib.Path('/workspace/tmp/pixelelated-m7-alignment-executor-03')
subprocess.run(['python3','-I','-u',str(O/'create.py')],check=True)
ssh=['ssh','-i',str(O/'qa-key'),'-p','10252','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','root@127.0.0.1']
subprocess.run(ssh+['mkdir -m 700 /storage/qa519-operation'],check=True)
for name in ['operation.py','inspect.py','guest-proof.py']:
 subprocess.run(ssh+['cat > /storage/qa519-operation/'+name],input=(O/name).read_bytes(),check=True)
p=subprocess.run(ssh+['python3 -I -B /storage/qa519-operation/guest-proof.py'],stdout=(O/'artifacts/guest-proof.log').open('wb'),stderr=subprocess.STDOUT)
(O/'guest-command.rc').write_text(str(p.returncode)+'\n')
subprocess.run(ssh+['tar -C /storage -czf - qa519-operation .cache/pixelelated-owner-alignment-519 2>/dev/null'],stdout=(O/'artifacts/results.tar.gz').open('wb'))
raise SystemExit(p.returncode)
