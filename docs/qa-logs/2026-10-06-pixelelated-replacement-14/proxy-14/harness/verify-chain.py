from pathlib import Path
import json
p=Path('/workspace/tmp/pixelelated-m7-qa-18')
assert json.loads((p/'completion.json').read_text())['job_rc']==0
print('PASS current replacement14 prerequisite completion')
