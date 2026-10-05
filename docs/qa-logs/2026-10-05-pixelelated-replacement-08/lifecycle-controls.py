from pathlib import Path
import importlib.util,unittest.mock as mock,subprocess,tempfile,json
p=Path('/tmp/pixelelated-es-lifecycle-guard.py');spec=importlib.util.spec_from_file_location('guard',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
a=Path('/workspace/tmp/pixelelated-m7-identity-diagnostic-03/artifacts')
def stat(name):
 rows=[x for x in (a/(name+'-lifecycle.txt')).read_text().splitlines() if '(emulationstatio)' in x]
 # The guest loop emits nothing when no ES process exists, not a blank line.
 return ''.join(x+'\n' for x in rows)
before=stat('information');assert before.strip();cases=[('same-process',before,True),('actual-crash-empty',stat('back-two'),False),('actual-restart',stat('delayed'),False)];results=[]
assert stat('back-two')=='' and stat('delayed')!=before
for name,after,expected in cases:
 with tempfile.TemporaryDirectory() as d, mock.patch.object(m.subprocess,'check_output',side_effect=[before,after]), mock.patch.object(m.subprocess,'run',return_value=subprocess.CompletedProcess([],0,stdout='retained diagnostic journal\n',stderr='')):
  try:
   with m.Lifecycle(['fixture-transport'],Path(d)):pass
   ok=True
  except AssertionError:ok=False
  assert ok==expected,name
  result=json.loads((Path(d)/'result.json').read_text());assert result['passed']==expected
  results.append({'case':name,'expected_acceptance':expected,'actual_acceptance':ok,'result':result})
Path('/tmp/pixelelated-lifecycle-controls.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS lifecycle guard accepts original identity and rejects actual missing/restarted identities')
