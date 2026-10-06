from pathlib import Path
import json,hashlib,sys
owner=Path('/workspace/tmp/pixelelated-m7-replacement-14')
a=json.loads((owner/'accepted-build.json').read_text())
assert a['durable_runner_rc']==0
assert a['source_manifest_sha256']=='70cb0448872f39b5382939173b2182a783381142df6dd5630b9e00a2c3ba6ccc'
assert a['bundle']==str(Path(sys.argv[1]).resolve())
assert json.loads((owner/'completion.json').read_text())['job_rc']==0
assert json.loads((owner/'container-exited.json').read_text())['exited']
assert (owner/'bundle.path').read_text().strip()==a['bundle']
print('PASS accepted replacement14 build dependency; broader VM qualification is subsequent')
