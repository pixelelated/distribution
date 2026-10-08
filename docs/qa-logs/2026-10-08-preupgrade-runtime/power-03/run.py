import subprocess,pathlib,hashlib,json
O=pathlib.Path('/workspace/tmp/pixelelated-m7-alignment-power-03')
ssh=['ssh', '-i', '/workspace/tmp/pixelelated-m7-alignment-runtime-01/qa-key', '-p', '10251', '-o', 'LogLevel=ERROR', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=5', 'root@127.0.0.1']
source=(O/"transaction-source.py").read_bytes()
subprocess.run(ssh+["cat > /storage/qa519/power2/transaction-source.py && sync"],input=source,check=True)
got=subprocess.check_output(ssh+["sha256sum /storage/qa519/power2/transaction-source.py"],text=True).split()[0]
assert got==hashlib.sha256(source).hexdigest()
(O/"artifacts/continuation-binding.json").write_text(json.dumps({"source_sha256":got,"power_event_owner":"pixelelated-m7-alignment-power-02","new_power_event":False,"original_failed_result_unchanged":True},indent=2)+"\n")
p=subprocess.run(ssh+["python3 -I -B -"],input=(O/"guest-proof.py").read_bytes(),stdout=(O/"artifacts/guest-proof.log").open("wb"),stderr=subprocess.STDOUT)
(O/"guest-command.rc").write_text(str(p.returncode)+"\n")
subprocess.run(ssh+["tar -C /storage/qa519/power2 -czf - ."],stdout=(O/"artifacts/results.tar.gz").open("wb"),check=True)
raise SystemExit(p.returncode)
