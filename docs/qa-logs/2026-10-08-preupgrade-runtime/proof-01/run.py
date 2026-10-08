import subprocess,pathlib,json
O=pathlib.Path('/workspace/tmp/pixelelated-m7-alignment-proof-01')
ssh=['ssh', '-i', '/workspace/tmp/pixelelated-m7-alignment-runtime-01/qa-key', '-p', '10251', '-o', 'LogLevel=ERROR', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=5', 'root@127.0.0.1']
p=subprocess.run(ssh+["python3 -I -B - --synthetic-only"],input=(O/"guest-proof.py").read_bytes(),stdout=(O/"artifacts/guest-proof.log").open("wb"),stderr=subprocess.STDOUT)
(O/"guest-command.rc").write_text(str(p.returncode)+"\n")
subprocess.run(ssh+["tar -C /storage/qa519 -czf - --exclude=original --exclude=observe --exclude=cloud --exclude=baseline --exclude=archive-\\* ."],stdout=(O/"artifacts/results.tar.gz").open("wb"),check=True)
raise SystemExit(p.returncode)
