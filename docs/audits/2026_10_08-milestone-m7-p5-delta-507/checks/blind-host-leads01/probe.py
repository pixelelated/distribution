import copy,datetime as dt,hashlib,importlib.machinery,importlib.util,json,sys
from pathlib import Path
owner=Path(__file__).resolve().parent;root=owner/'fixture';audit=root/'docs/audits/probe';audit.mkdir(parents=True)
source=Path.cwd()/'tools/ceremony-check';loader=importlib.machinery.SourceFileLoader('ceremony_probe',str(source));spec=importlib.util.spec_from_loader(loader.name,loader);mod=importlib.util.module_from_spec(spec);loader.exec_module(mod)
ended='2026-10-07T02:53:02.029760+00:00';now=dt.datetime(2026,10,8,tzinfo=dt.timezone.utc)
files={'docs/audits/probe/04-analysis.md':'analysis','docs/audits/probe/05-punch-list.md':'outcomes','tracker.json':json.dumps(dict(number=471,state='closed',state_reason='completed',body='- [x] PL-001: resolved')),'completion.json':json.dumps(dict(result='PASS',exact_bodies_and_states=True,closed_completed=[471],verified_utc=ended))}
base=dict(schema=1,issue=471,completed_at=ended,tracker_readback='tracker.json',tracker_completion='completion.json',evidence={n:hashlib.sha256(v.encode()).hexdigest() for n,v in files.items()})
rows=[]
for shape in ['valid','marker-list','evidence-list','tracker-list','completion-list']:
 for n,v in files.items():(root/n).write_text(v)
 data=copy.deepcopy(base)
 if shape=='marker-list':data=[]
 elif shape=='evidence-list':data['evidence']=list(data['evidence'])
 elif shape in ['tracker-list','completion-list']:
  n='tracker.json' if shape=='tracker-list' else 'completion.json';(root/n).write_text('[]');data['evidence'][n]=hashlib.sha256((root/n).read_bytes()).hexdigest()
 marker=audit/'audit-completion.json';marker.write_text(json.dumps(data))
 try:
  result=mod.completed_audit_marker(marker,root,now);kind='accepted';detail=str(result)
 except Exception as e:kind=type(e).__name__;detail=str(e)
 rows.append(dict(shape=shape,observed=kind,detail=detail,expected='accepted' if shape=='valid' else 'handled invalid marker (ValueError/KeyError/TypeError/OSError)',matches_bug_control=kind==('accepted' if shape=='valid' else 'AttributeError')))
result=dict(utc=dt.datetime.now(dt.timezone.utc).isoformat(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scope='Host-only checker; no VM/runtime/provider claims. Native host is the correct target for this Python host guard.',checks=rows,confirmed=all(v['matches_bug_control'] for v in rows));(owner/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(0 if result['confirmed'] else 1)
