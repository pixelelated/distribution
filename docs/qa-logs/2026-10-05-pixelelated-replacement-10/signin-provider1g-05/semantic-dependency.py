from pathlib import Path
import json
p=Path('/workspace/tmp/pixelelated-m7-signin-ui-14')
assert json.loads((p/'completion.json').read_text())['job_rc']==0
assert json.loads((p/'completion.json').read_text())['qemu_absent']
assert json.loads((p/'visual-review.json').read_text())['passed']
print('PASS actual full sign-in semantic qualification prerequisite')
