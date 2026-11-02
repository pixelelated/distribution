#!/usr/bin/env python3
import collections,datetime,hashlib,json,pathlib,runpy
R=pathlib.Path(__file__).resolve().parents[1];C=R/'stage-b';ns=runpy.run_path(str(R/'tools/table.py'),run_name='t43_table');rows=json.loads((C/'observations.json').read_text());plans=json.loads((C/'plans.json').read_text());links={x['path']:x for x in json.loads((C/'links.json').read_text())['native']};reports={};ownerids={'devices-unshipped':'T25 #672','image-packages':'T8 #655','emulators-standalone':'T30 #677','packages-dead-ends':'T23 #670','device-generic-x64-and-kernel':'T11 #658'}
for p in plans:
 f=C/'application-overlay'/(p['id']+'.json')
 if not f.exists():f=C/'application'/(p['id']+'.json')
 reports[p['id']]=(json.loads(f.read_text()),str(f.relative_to(R)))
allcalls=collections.Counter();nativecalls=collections.Counter();positives=set();opens=set();fuzz=set();groups=collections.Counter();out=[]
for p in plans:
 rr,receipt=reports[p['id']];groups[rr['status']]+=1
 for r in rr.get('rows',[]):
  if r.get('normal_called'):allcalls[r['status']]+=1
  if r['native'] and r.get('normal_called'):
   nativecalls[r['status']]+=1;positives.add(r['path'])
   if r['status']=='fuzz':fuzz.add(r['path'])
 if rr['status']=='open-item':opens.update(p['native_paths'])
for e in rows:
 x=dict(e);rp=e['source_recipe'];ps=[p for p in plans if p['recipe']==rp and p['consumer'] in e['buildable_by']];assert ps;owner=', '.join(ownerids[a] for a in e['recipe_owner']);application=[];receipts=['[source observations](stage-b/observations.json)'];stacks=[]
 for p in ps:
  rr,receipt=reports[p['id']];receipts.append('['+p['id']+']('+receipt+')');pr=[r for r in rr.get('rows',[]) if r['path']==e['path']]
  if e['kind']=='config':application.append(p['id']+' '+p['consumer']+': source configuration only; final .config and runtime unmeasured');stacks.append(p['id']+': config/functions:1449-1471 -> '+e['path']);continue
  positions=[str(i+1)+'/'+str(len(p['stack'])) for i,path in enumerate(p['stack']) if path==e['path']];assert positions
  stacks.append(p['id']+' '+p['consumer']+': '+','.join(positions)+'; '+','.join(p['selectors'] or ['default patterns']))
  if pr:
   application += [p['id']+' '+p['consumer']+': '+r['status']+'; '+('normal rc '+str(r['normal']['exit'])+'; target-member source projection only' if r.get('normal_called') else r['reason']) for r in pr]
  else:application.append(p['id']+' '+p['consumer']+': open-item; '+'; '.join(rr['limits']))
 status=e['upstream']['status'];disposition='upstream-changed' if status=='changed-at-path' else ('open-item' if e['path'] in opens or status.startswith('absent') else 'keep')
 header_subject=' '.join(t for n,t in e['header'] if t.startswith('Subject:'))
 reason=header_subject or ('Source config for '+', '.join(e['buildable_by']) if e['kind']=='config' else ('Shared referent '+links[e['path']]['resolved'] if e['kind']=='symlink' else 'File intent label: '+pathlib.PurePosixPath(e['path']).name+'; original carrying rationale not independently established'))
 x.update(link=links.get(e['path'],'not a symlink'),recipe_pins=rp+'; '+owner+'; '+'; '.join(p['consumer']+' @ '+p['pin'] for p in ps),selected_stack='; '.join(stacks),origin=ns['origin'](e),target_summary='; '.join('L'+str(n)+': '+t for n,t in e['targets'][:8]) or ('source configuration input' if e['kind']=='config' else 'literal link to '+links[e['path']]['resolved']),application='; '.join(application),upstream_status='651150fc88a8ee40e3f8e69c6d36feb6b005bde5: '+status+'; '+json.dumps(e['upstream'],sort_keys=True)+'; fork base identical',backport_status='Literal header/backport statements retained in observations.json; component-upstream absorption not verified; fixed ROCKNIX identity is a separate comparison',carrying_reason=reason+'; retained pending existing-owner qualification; no removal',disposition=disposition,next_owner=owner+': preserve selected source; resolve each receipt-qualified input before claiming application on that plan'+('; #563/#559 integration owns fixed-upstream delta' if status!='identical-at-path' else ''),receipts='; '.join(receipts),coverage='Mechanical source hash/mode/header/target extraction and static selection; primary grouped header/target and recipe mechanism read. Vendor body not read line by line; '+('configuration source and writers only' if e['kind']=='config' else 'exact source application limited to named receipts'))
 out.append(x)
ns['assert_input'](out);(C/'table-input.json').write_text(json.dumps(out,indent=2)+'\n');stats={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'paths':432,'regular_patches':418,'symlinks':2,'configs':12,'groups':dict(groups),'normal_calls_including_context':dict(allcalls),'normal_native_calls':dict(nativecalls),'positive_native_paths':len(positives),'open_native_paths':len(opens),'mixed_native_paths':len(positives&opens),'wholly_open_native_paths':len(opens-positives),'fully_qualified_native_paths':len(positives-opens),'native_fuzz_paths':len(fuzz),'disposition':dict(collections.Counter(x['disposition'] for x in out)),'headerless_regular_patch_paths':[x['path'] for x in rows if x['kind']=='patch' and not x['header']],'unknown_recognized_attribution_paths':[x['path'] for x in rows if x['kind']=='patch' and not any(t.startswith(('From:','Author:','commit ')) for n,t in x['header'])]};(C/'table-summary.json').write_text(json.dumps(stats,indent=2)+'\n')
(C/'open-inputs.json').write_text(json.dumps([{'path':x['path'],'owner':x['next_owner'],'application':x['application'],'receipts':x['receipts']} for x in out if x['path'] in opens],indent=2)+'\n');print(json.dumps({k:v for k,v in stats.items() if not k.endswith('_paths') or isinstance(v,int)},indent=2))
