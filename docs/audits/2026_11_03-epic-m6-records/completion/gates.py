"""Current completion gates; explicit current input/program bindings."""
import argparse,json,pathlib,subprocess
C=pathlib.Path(__file__).resolve().parent;R=C.parents[3];A=C.parent
p=argparse.ArgumentParser();p.add_argument('--dest',required=True);args=p.parse_args();dest=C/args.dest;dest.mkdir(parents=True,exist_ok=False)
common=[A/'04-analysis.md',A/'05-punch-list.md',A/'second-opinions/review-plan.json',R/'docs/audits/README.md',A/'audit-completion.json',C/'tracker-1417.json',C/'tracker-completion.json']
checks=[('index-write',['tools/work-log-index','--write']),('marker',['python3','-B',str(C/'validate-marker.py')]),('normal-resolution',['tools/lint-audit-artifacts',str(A.relative_to(R))]),('issue-resolution',['tools/lint-audit-artifacts',str(A.relative_to(R)),'--issue','1417']),('rules',['tools/rules-check']),('register',['tools/register-check']),('index',['tools/work-log-index','--check']),('ceremony-full',['tools/ceremony-check']),('ceremony-gate',['tools/ceremony-check','--gate'])]
checks += [('issue-'+str(n),['tools/box-check','--issue',str(n)]) for n in [1417,693,1416,1415]]
checks += [('staged-whitespace',['git','diff','--cached','--check']),('working-whitespace',['git','diff','--check'])]
results=[]
for name,cmd in checks:
 inputs=common+([R/cmd[0]] if cmd[0].startswith('tools/') else [C/'validate-marker.py',R/'tools/ceremony-check'] if name=='marker' else [])
 if name.startswith('ceremony'):inputs += [R/'tools/lint-audit-artifacts']
 argv=['python3','-B',str(C/'record.py'),'--out',args.dest+'/'+name]
 for f in inputs:argv+=['--input',str(f)]
 argv+=['--',*cmd];r=subprocess.run(argv,cwd=R);results.append({'name':name,'rc':r.returncode});(dest/'results.json').write_text(json.dumps(results,indent=2)+'\n');assert r.returncode==0,name
print('PASS '+str(len(results))+' current completion gates; explicit current04/05/plan/source/marker/tracker/checker inputs; no accepted controls replayed')
