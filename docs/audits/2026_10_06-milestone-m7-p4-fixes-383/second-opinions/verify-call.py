#!/usr/bin/env python3
"""Verify one finished audit call against its frozen inputs and actual host state."""
from pathlib import Path
import argparse, datetime, hashlib, json, re

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--owner', type=Path, required=True)
p.add_argument('--prompt', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--receipt', type=Path, required=True)
a = p.parse_args()
owner = a.owner.resolve(); run = Path((owner/'run.path').read_text().strip())
assert not a.receipt.exists(), 'Do not overwrite an accepted verification receipt'
channels = {n:(owner/n).read_text().strip() for n in ['inner.rc','outer.rc','tool-wrapper.rc','provider.rc']}
channels['build.rc'] = (run/'build.rc').read_text().strip()
assert set(channels.values()) == {'0'}, channels
seal = json.loads((owner/'seal.json').read_text())
for path,digest in seal.items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
actual = {}
for name,file in [('launcher',owner/'launcher-pid.json'),('runner',run/'build.pid'),('watcher',run/'watcher.pid'),('command',run/'command.pid')]:
    pid = json.loads(file.read_text())['pid'] if file.suffix == '.json' else int(file.read_text())
    assert not Path(f'/proc/{pid}').exists(), f'{name} PID still exists: {pid}'
    actual[name] = {'pid':pid,'absent':True}
receipt = json.loads(Path(str(a.output)+'.provenance.json').read_text())
final = receipt['final']; identity = final['verification']; effort = final['effort_verification']
model = 'anthropic/claude-fable-5.1'
assert receipt['facilitator_version'] == 'council-facilitator@1.14.0'
assert receipt['member'] == 'claude' and receipt['declared_model'].split(' ',1)[0] == model
assert final['outcome'] == 'success' and identity['result'] == 'PASS'
assert identity['model_identity_source'] == 'provider_response'
assert re.fullmatch(re.escape(model)+r'(?:-\d{8})?',identity['observed'])
assert effort['result'] == 'PASS' and effort['declared'] == 'xhigh' and effort['observed_reasoning_tokens'] > 0
assert final['provider_verification']['result'] == 'NOT_PINNED'
assert final['assurance_tier'] == 'local_capture_provider_attested'
assert receipt['request']['user_prompt_sha256'] == hashlib.sha256(a.prompt.read_bytes()).hexdigest()
content = a.output.read_bytes(); assert content.strip()
digest = hashlib.sha256(content).hexdigest()
assert receipt['output_file_sha256'] == digest == final['file_artifact_sha256']
result = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':str(owner),'run':str(run),'result':'PASS','channels':channels,'actual_host_processes':actual,'sealed_inputs':len(seal),'prompt_sha256':receipt['request']['user_prompt_sha256'],'output_sha256':digest,'output_bytes':len(content),'facilitator_version':receipt['facilitator_version'],'verification':identity,'effort_verification':effort,'provider_verification':final['provider_verification'],'duration_ms':final['total_duration_ms'],'retries_used':final['retries_used'],'tokens':final.get('tokens')}
a.receipt.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
