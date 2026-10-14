from pathlib import Path
import hashlib,json,subprocess,ast
owner=Path('/workspace/tmp/pix588-startup-candidate-vm-20261014-02');assert not (owner/'admission.json').exists()
repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');packet=repo/'docs/qa-logs/2026-10-14-proxy-startup-race-internal';base=Path('/workspace/tmp/pix583-native-prepared-20261014-02')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
f=owner/'records/inputs.json';d=json.loads(f.read_text());d['files'] += [{'path':str(p),'destination':'component-packet/'+p.name,'sha256':sha(p)} for p in (packet/'component-fixture.py',packet/'bindings.json',packet/'check-results.py')]
d['files'] += [{'path':str(p),'destination':'component-baseline/'+str(p.relative_to(base)),'sha256':sha(p)} for p in base.rglob('*.py')]
dump(f,d)
f=owner/'run-guest.sh';t=f.read_text();t+='''
mkdir /run/pix588-components
mount -t tmpfs -o size=64M,mode=700,nosuid,nodev,noexec tmpfs /run/pix588-components
mkdir /tmp/pix-output/components
set +e
PIX588_ALLOCATED_VM=yes timeout --signal=TERM --kill-after=5s 245s python3 -I -B /tmp/pix-input/component-packet/component-fixture.py --source /tmp/pix-input/component-baseline --variant baseline --cases startup-window --output /run/pix588-components/baseline > /tmp/pix-output/components/baseline.stdout 2> /tmp/pix-output/components/baseline.stderr
brc=$?
printf '%s\\n' "$brc" > /tmp/pix-output/components/baseline.rc
PIX588_ALLOCATED_VM=yes timeout --signal=TERM --kill-after=5s 245s python3 -I -B /tmp/pix-input/component-packet/component-fixture.py --source /tmp/pix-input/service-prepared --variant candidate --cases all --output /run/pix588-components/candidate > /tmp/pix-output/components/candidate.stdout 2> /tmp/pix-output/components/candidate.stderr
crc=$?
printf '%s\\n' "$crc" > /tmp/pix-output/components/candidate.rc
python3 -I -B /tmp/pix-input/component-packet/check-results.py --kind component --baseline-result /run/pix588-components/baseline/result.json --baseline-rc /tmp/pix-output/components/baseline.rc --candidate-result /run/pix588-components/candidate/result.json --candidate-rc /tmp/pix-output/components/candidate.rc > /tmp/pix-output/components/check.stdout 2> /tmp/pix-output/components/check.stderr
checkrc=$?
printf '%s\\n' "$checkrc" > /tmp/pix-output/components/check.rc
set -e
tar -czf /tmp/pix-output/components/fixture-records.tar.gz -C /run/pix588-components .
sync
umount /run/pix588-components
printf 'PIX588_COMPONENT_BASELINE_RC:%s CANDIDATE_RC:%s CHECK_RC:%s\\n' "$brc" "$crc" "$checkrc"
test "$brc" -eq 1
test "$crc" -eq 0
test "$checkrc" -eq 0
''';f.write_text(t);subprocess.run(['sh','-n',str(f)],check=True)
f=owner/'vm-lifecycle.py';t=f.read_text();assert t.count('seconds=350)')==1;t=t.replace('seconds=350)','seconds=650)');ast.parse(t);f.write_text(t)
f=owner/'retention-plan.json';d=json.loads(f.read_text());d['builds'][0]['basis']+=' Before first admission, add serialized source-component baseline startup case and ten candidate cases after service succeeds. Original component exits retained separately (baseline1/candidate0/checker0); no sockets/subprocess in fixture, 512MiB address space/45s CPU/240s wall per process, 64MiB scratch tmpfs. Serial ceiling650s within unchanged900s total lifecycle. No running deadline extended.'
for e in d['builds'][0]['evidence']:e['sha256']=sha(Path(e['path']))
dump(f,d);print('Fresh candidate allocation updated, not yet admitted or launched')
