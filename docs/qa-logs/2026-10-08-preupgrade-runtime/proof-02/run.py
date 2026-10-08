import subprocess,pathlib
O=pathlib.Path('/workspace/tmp/pixelelated-m7-alignment-proof-02')
ssh=['ssh', '-i', '/workspace/tmp/pixelelated-m7-alignment-runtime-01/qa-key', '-p', '10251', '-o', 'LogLevel=ERROR', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=5', 'root@127.0.0.1']
p=subprocess.run(ssh+["python3 -I -B -"],input=(O/"guest-proof.py").read_bytes(),stdout=(O/"artifacts/guest-proof.log").open("wb"),stderr=subprocess.STDOUT)
(O/"guest-command.rc").write_text(str(p.returncode)+"\n")
subprocess.run(ssh+["tar -C /storage/qa519/followup -czf - ."],stdout=(O/"artifacts/results.tar.gz").open("wb"),check=True)
raise SystemExit(p.returncode)
