"""Read-only full dependency discovery for #494; no removal authority."""
from pathlib import Path
import datetime,hashlib,json,os,runpy,subprocess,time
owner=Path(__file__).resolve().parent
library=runpy.run_path(str(owner/'retention-report.py'))
plan=json.loads((owner/'plan.json').read_text())
targets=[Path(c['path']) for c in plan['candidates']]
observed=library['inventory'](plan)
within=library['within']
external_edges=[r for r in observed['references'] if any(within(r['target'],t) for t in targets) and not any(within(r['source'],t) for t in targets)]
mounts=[r for r in observed['container_mounts'] if any(within(r['source'],t) or within(t,r['source']) for t in targets)]
references=[];errors=[];count=0;tick=time.monotonic()
def examine(value,path,keypath):
    if isinstance(value,str):
        for t in targets:
            if value==str(t) or value.startswith(str(t)+'/'):
                references.append({'manifest':str(path),'key':keypath,'value':value})
    elif isinstance(value,list):
        for i,v in enumerate(value):examine(v,path,keypath+[i])
    elif isinstance(value,dict):
        for k,v in value.items():
            examine(k,path,keypath+['<key>']);examine(v,path,keypath+[k])
for base,dirs,files in os.walk('/workspace/artifacts',followlinks=False,onerror=lambda e:errors.append(str(e))):
    for name in files:
        p=Path(base)/name
        if p.suffix!='.json' or p.is_symlink():continue
        try:examine(json.loads(p.read_text()),p,[]);count+=1
        except (OSError,ValueError) as e:errors.append(str(e))
    if time.monotonic()-tick>10:print('Inspected',count,'artifact manifests;',len(references),'historical/path references',flush=True);tick=time.monotonic()
proc=subprocess.run(['python3','-I',str(owner/'readonly-process-dependencies.py')],capture_output=True,text=True)
(owner/'artifacts/process-readback.json').write_text(proc.stdout)
(owner/'artifacts/process-readback.err').write_text(proc.stderr)
assert proc.returncode in [0,1] and not proc.stderr
process=json.loads(proc.stdout)
payload={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inventory':observed,'external_edges':external_edges,'container_matches':mounts,'artifact_reference_scan_errors':errors,'artifact_manifests':count,'artifact_path_references':references,'process_readback':process,'deletion_performed':False}
p=owner/'artifacts/dependencies.json';p.write_text(json.dumps(payload,indent=2)+'\n')
summary={'utc':payload['utc'],'result':'REVIEW_REQUIRED','directories':observed['directories'],'disk_chains':len(observed['disks']),'inventory_errors':len(observed['errors']),'external_edges':len(external_edges),'container_matches':len(mounts),'active_matches':len(observed['active']),'artifact_manifests':count,'artifact_reference_errors':len(errors),'artifact_path_references':len(references),'process_uid':process['effective_uid'],'process_matches':len(process['matches']),'process_unreadable':len(process['unreadable']),'report_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'deletion_performed':False,'remaining':'Classify all external provenance/runtime references and obtain fresh root-only process readback before a concrete proposal; no removal yet.'}
(owner/'artifacts/summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
