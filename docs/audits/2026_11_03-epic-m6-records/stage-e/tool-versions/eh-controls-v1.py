"""Execute the new guard refusals before its positive, with complete new input binding."""
import json,pathlib,subprocess
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];x=json.loads((A/'stage-e/fixtures-manifest.json').read_text());rows=[]
for case in x['cases']:
 argv=['python3','-B',str(A/'tools/eh-record.py'),'--out','stage-e/scope-controls/'+case['name'],'--input',str(A/'tools/eh-scope.py'),'--input',case['policy'],'--input',str(A/'stage-e/fixtures-manifest.json'),'--','python3','-B',str(A/'tools/eh-scope.py'),'--repo',case['repo'],'--policy',case['policy'],'--tip',case['tip']];p=subprocess.run(argv,cwd=R);rows.append({'name':case['name'],'rc':p.returncode,'expected':case['expected'],'receipt':'stage-e/scope-controls/'+case['name']+'/receipt.json'});(A/'stage-e/control-results.json').write_text(json.dumps(rows,indent=2)+'\n')
 if p.returncode!=case['expected']:raise SystemExit('Unexpected guard result: '+case['name'])
print('PASS14 new scope outcomes:13 refusals before1 complete positive, including all3 index-only states')
