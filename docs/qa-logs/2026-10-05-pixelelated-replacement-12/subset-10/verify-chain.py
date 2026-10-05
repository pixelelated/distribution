from pathlib import Path
import json,re
old=Path('/workspace/tmp/pixelelated-m7-qa-15')
follow=Path('/workspace/tmp/pixelelated-m7-qa-17')
assert json.loads((old/'completion.json').read_text())['job_rc']==1
assert json.loads((follow/'completion.json').read_text())['job_rc']==0
report=list((old/'artifacts/rocknix-images').glob('qa-*/report.md'))
assert len(report)==1 and len(re.findall(r'^\| [a-z-]+ \| PASS \|',report[0].read_text(),re.M))==15
upgrade=Path('/workspace/artifacts/rocknix-images/qa-55d8ee8f75-upgrade-from-69e6039f8f-20261005-2321')
assert (upgrade/'rc').read_text().strip()=='0'
assert len(re.findall(r'^PASS ',(upgrade/'rehearsal.log').read_text(),re.M))==26
reports=list((follow/'artifacts/rocknix-images').glob('qa-*/report.md'));assert len(reports)==1
assert '| walks | PASS |' in reports[0].read_text()
for system in ['nes','gb','fbn']:
 assert 'PASS actual selected manager system '+system in (reports[0].parent/'walks'/('manager-'+system+'-system-check.log')).read_text()
print('PASS explicit QA15 partial success plus QA17 completed continuation chain')
