from pathlib import Path
import subprocess,json,datetime,hashlib,os
out=Path(__file__).parent
rows=[]
for n in ['03','05','06','07','08']:
 tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement'+n)
 roots=list(tree.glob('build.*'));assert len(roots)==1,(tree,roots)
 head=subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()
 print('Inspecting allocated bytes only',tree.name,flush=True)
 log=out/(tree.name+'.du.tsv')
 with log.open('x') as f:
  p=subprocess.Popen(['nice','-n','10','ionice','-c','3','du','-x','-B1','--max-depth=2',str(roots[0])],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  count=0
  for line in p.stdout:
   f.write(line);count+=1
   if count%50==0:
    f.flush();print('Observed',count,'completed directory size rows for',tree.name,flush=True)
  err=p.stderr.read();rc=p.wait()
 assert rc==0 and not err,(rc,err)
 assert head==subprocess.check_output(['git','-C',str(tree),'rev-parse','HEAD'],text=True).strip()
 rows.append({'tree':str(tree),'head':head,'build_root':str(roots[0]),'du_file':log.name,'sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'rows':count})
 print('Completed directory allocation scan',tree.name,flush=True)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trees':rows,'scope':'Read-only allocated block sizes; not preservation, dependency absence or deletion approval','preservation_performed':False,'deletion_performed':False}
(out/'summary.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS five-tree allocated-block breakdown complete',flush=True)
