import pathlib,subprocess,json,hashlib
A=pathlib.Path(__file__).resolve().parents[1];R=A.parents[2];rec=A/'tools/record.py';table=A/'tools/table.py';out=[]
common=[A/'stage-a/summary.json',A/'stage-a/groups.json',A/'stage-b/ranges.json',A/'stage-b/observations.json',A/'stage-b/route-inputs.json',R/'docs/qa-logs/2026-11-03-m6-records-preparation/t1-report.json',R/'docs/qa-logs/2026-11-03-m6-records-preparation/p1-routes/entrypoints.json']
def run(name,program,args,expected,inputs=[]):
 argv=['python3','-B',str(rec),'--name','stage-c/'+name,'--input',str(program)]
 for p in inputs:argv+=['--input',str(p)]
 argv+=['--','python3','-B',str(program),*map(str,args)];p=subprocess.run(argv,cwd=R);out.append({'name':name,'rc':p.returncode,'expected':expected,'receipt':'stage-c/'+name+'/receipt.json'})
 if p.returncode!=expected:raise SystemExit('Unexpected control result '+name)
run('table-fixture-generation',table,['fixtures'],0,[A/'stage-b/table.json'])
for p in sorted((A/'stage-c/table-fixtures').glob('*.json')):run('table-'+p.stem,table,['validate',p],0 if p.stem=='positive' else 1,[p,*common])
f=A/'tools/make-control-fixtures.py';run('new-fixture-generation',f,[],0)
for p in sorted((A/'stage-c/link-fixtures').glob('*.json')):run('link-'+p.stem,A/'tools/link.py',[p],0 if p.stem=='positive' else 2 if p.stem=='unsupported' else 1,[p])
x=json.loads((A/'stage-c/confinement-fixtures.json').read_text())
for k in ['positive','source_edit','edit_then_revert']:run('confinement-'+k,A/'tools/confinement.py',['--repo',x['repo'],'--seed',x['seed'],'--tip',x[k]],0 if k=='positive' else 1,[A/'stage-c/confinement-fixtures.json'])
p=A/'stage-c/control-summary.json'
if p.exists():raise SystemExit('refuse overwrite')
p.write_text(json.dumps({'runs':out,'all_expected':True,'no_accepted_replay':True},indent=2)+'\n');print('PASS new T46 controls: '+str(len(out))+' actual expected exits')
