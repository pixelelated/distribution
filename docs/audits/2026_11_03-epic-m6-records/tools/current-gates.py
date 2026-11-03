"""Required new current-record checks; preserve each actual result."""
import json,pathlib,subprocess
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];rec=A/'tools/record.py';result=[]
checks=[('index-write',['tools/work-log-index','--write']),('rules',['tools/rules-check']),('register',['tools/register-check']),('index-check',['tools/work-log-index','--check']),('ceremony',['tools/ceremony-check','--gate']),('audit-issue-lint',['tools/lint-audit-artifacts','--phase','pre-issue',str(A.relative_to(R)),'--issue','1417']),('audit-checkboxes',['tools/box-check','--issue','1417']),('bug-checkboxes',['tools/box-check','--issue','1416']),('confinement-current',['python3','-B',str(A/'tools/confinement.py'),'--repo',str(R),'--seed','8710a6210a40de0110244d03a886161ee06faf29','--working']),('diff-check',['git','diff','--check'])]
for name,cmd in checks:
 program=cmd[0] if cmd[0].startswith('tools/') else str(A/'tools/confinement.py') if name=='confinement-current' else None
 argv=['python3','-B',str(rec),'--name','stage-d/gates/'+name]
 if program:argv+=['--input',program]
 argv+=['--',*cmd];p=subprocess.run(argv,cwd=R);result.append({'name':name,'rc':p.returncode,'receipt':'stage-d/gates/'+name+'/receipt.json'})
(A/'stage-d/gates-summary.json').write_text(json.dumps(result,indent=2)+'\n')
if any(x['rc'] for x in result):raise SystemExit('Current gates have failures; retain and investigate')
print('PASS all required current-record gates in this driver')
