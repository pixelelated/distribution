"""T46 finite evidence join and independent input-bound table validator."""
import argparse,collections,copy,datetime,hashlib,json,pathlib,re,subprocess,sys
A=pathlib.Path(__file__).resolve().parents[1]; R=A.parents[2]; P=R/'docs/qa-logs/2026-11-03-m6-records-preparation'
SOURCE='d707c82ab8c48b674acc1f95a9571f0cb24d226a'; SEED='8710a6210a40de0110244d03a886161ee06faf29'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):
 if p.exists():raise ValueError('refuse overwrite '+str(p))
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def blob(path):return subprocess.check_output(['git','show',SOURCE+':'+path],cwd=R)
def assemble():
 summary=read(A/'stage-a/summary.json');groups=read(A/'stage-a/groups.json');ranges=read(A/'stage-b/ranges.json');obs=read(A/'stage-b/observations.json');entry=read(P/'p1-routes/entrypoints.json');direct=read(A/'stage-b/route-inputs.json')['routes'];allroutes=read(P/'p1-routes/routes.json');t39=read(P/'t1-report.json');t3=read(P/'t3-report.json')
 readings=[]
 for i,x in enumerate(ranges):
  x=copy.deepcopy(x);x['reading_id']=i;x['observation']=obs[str(i)];x['read_status']='metadata-only' if x['kind'] in ('directory-metadata','inventory-schema-only') else 'bounded-masked' if x.get('masked_lines') else 'bounded-read';x['unread']='All text outside named ranges; masked lines unread unredacted; earlier day bodies not credited. Inventory rows/directory descendants not read.'
  x['status']='historical-record' if x['kind'] in ('bounded-day-entry','historical-pointer','inventory-schema-only','directory-metadata') else 'current-entrypoint-at-cutoff'
  x['date_evidence']='Date in path/title and retained range receipt; heading timestamps are file-order syntax, not validated calendar or live status.' if x['kind']=='bounded-day-entry' else 'Literal source range and observation; cutoff 2026-11-03 is snapshot date, not authorship date.'
  x['purpose']='Dated work handoff/evidence navigation' if x['kind']=='bounded-day-entry' else x.get('purpose','Named reader entrypoint/status/navigation or schema metadata')
  x['next_owner']='#1407 for later monthly indexing; historical authorship/status retained' if x['kind']=='bounded-day-entry' else '#346 coordinator; #693 current records review; original owners retained in observation'
  if i==0:x['inherited_qualification']='README release wording is accepted T39 PL-02/#1400 correction pending #686/#807/#346 integration; initial independent observation is not the final verdict.'
  if i==10:
   x['ranges'] += [[184,225],[308,356]]; x['masked_lines'] += [324]
   x['supplemental_observation']={'receipt':'stage-b/pointer-navigation/receipt.json','observation':'Oct17 next queue, unsent requests and navigation were read. Pending questions remain untouched; dated instructions are not Nov3 authority. Lines121-183 and225-307 remain unread.'}
  readings.append(x)
 bypath={x['path']:x for x in readings};entries={x['path']:x for x in entry};routes=[]
 for r in direct:
  rr=copy.deepcopy(r);rr['referrer_identity']=entries[r['entrypoint']]['git'];rr['reading_id']=bypath[r['resolved_path']]['reading_id'];rr['interpretation']='intentional-historical-navigation';rr['defect_evidence']=[];rr['consequence']='N/A: target exists; bounded purpose/status evidence retained, no live replay or full-file credit.';rr['next_owner']=bypath[r['resolved_path']]['next_owner'];routes.append(rr)
 keys={r['id'] for r in direct};context=[]
 for x in allroutes:
  if x['id'] in keys:continue
  x=copy.deepcopy(x)
  if x['classification']=='literal-root-classification-pending':x['classification']='literal-outside-records-context'
  x['interpretation']='context-or-template-not-defect';x['body_read']='not followed';x['next_owner']='Existing scoped owner; no scope expansion or guessed target';context.append(x)
 # Metadata-only index alignment: no day-body output and no old generator invocation.
 index=blob('docs/work-logs/INDEX.md').decode();expected={m.group(1):int(m.group(2)) for m in re.finditer(r'^#### \[[^\]]+\]\(([^)]+)\) \((\d+)\)$',index,re.M)};alignment=[]
 for x in readings:
  if x['kind']!='bounded-day-entry':continue
  text=blob(x['path']).decode();heads=[(i,l) for i,l in enumerate(text.splitlines(),1) if re.match(r'^ {0,3}#{1,6}(?:\s|$)',l)]
  # Exact index convention is literal ## prefix, including any code-fenced line; separate from day-range semantic selector.
  count=sum(l.startswith('## ') for l in text.splitlines());rel=x['path'].removeprefix('docs/work-logs/')
  alignment.append({'path':x['path'],'oid':x['oid'],'literal_h2_count':count,'index_count':expected.get(rel),'aligned':count==expected.get(rel),'all_atx_candidate_metadata_sha256':sha(json.dumps(heads,separators=(',',':')).encode()),'atx_candidate_count':len(heads),'body_read_claim':False})
 trace={}
 for path in ['docs/audits/README.md','.claude/rules/instruction-files.md']:
  data=blob(path);lines=data.decode().splitlines();hits=[{'line':i,'text':l} for i,l in enumerate(lines,1) if 'applyTo' in l or 'paths:' in l]
  trace[path]={'sha256':sha(data),'matching_named_instruction_lines':hits}
 result={'schema':1,'seed':SEED,'source_summary':summary,'groups':groups,'cost_unit':'logical-object-bytes','disk_savings_claim':False,'survey':{'rows':126149,'stored_lines':22984582,'generated_code_lines':15392661,'historical_self_row_lines':134637,'source':'eb4763e3cc9bcd729830cd85f1719bbd4f28db10','host':'2174265e9cc1b248c0fbe27fa101875984d46d6b'},'retained_delta':t3['delta'],'entrypoints':entry,'readings':readings,'routes':routes,'context':context,'suppressed':{'occurrences':8,'sha256':read(P/'p1-routes/summary.json')['suppressed_metadata_sha256'],'identities_exported':False},'unresolved_coordinator_shorthands':13,'index_alignment':alignment,'inherited':{'status':'accepted-pending-integration','owners':[686,807,346],'path_bridge':t39['path_bridge'],'outcomes':t39['accepted_outcome_routes'],'counts':t39['outcome_counts_retained'],'later_owner':1407,'later_population':{'documents':33,'lines':2770,'edit_scope':32,'table_only':1}},'finding_trace':trace}
 dump(A/'stage-b/table.json',result)
 print('PASS table assembly: 10 groups, 10 entrypoints, 95 routes, 99 reading records, 701 context rows; index alignment',sum(x['aligned'] for x in alignment),'/',len(alignment))

def validate(t):
 errors=[]
 def check(b,msg):
  if not b:errors.append(msg)
 summary=read(A/'stage-a/summary.json');groups=read(A/'stage-a/groups.json');rr=read(A/'stage-b/route-inputs.json')['routes'];ranges=read(A/'stage-b/ranges.json');obs=read(A/'stage-b/observations.json');t39=read(P/'t1-report.json')
 check(t.get('source_summary')==summary and t.get('seed')==SEED,'source/seed metadata identity')
 check(t.get('groups')==groups,'exhaustive group keys and bound metadata')
 check(sum(x['paths'] for x in t.get('groups',{}).values())==127469 and sum(x['logical_bytes'] for x in t.get('groups',{}).values())==2190843187,'group sums')
 actual=t.get('routes',[]);check(len(actual)==len(rr) and len({r['id'] for r in actual})==len(rr) and {r['id'] for r in actual}=={r['id'] for r in rr},'unique exhaustive route keys')
 expected={r['id']:r for r in rr}
 for x in actual:
  check(x['id'] in expected and all(x.get(k)==v for k,v in expected.get(x['id'],{}).items()),'literal route identity '+str(x['id']))
  check(x.get('interpretation')=='intentional-historical-navigation' and x.get('defect_evidence')==[],'historical route unsupported defect '+str(x['id']))
 readings=t.get('readings',[]);check(len(readings)==99 and {r['reading_id'] for r in readings}==set(range(99)),'reading keys')
 for x in readings:
  i=x['reading_id'];y=ranges[i];expected_ranges=y['ranges']+([[184,225],[308,356]] if i==10 else [])
  check(x.get('whole_file_read') is False and x['ranges']==expected_ranges and x['oid']==y['oid'] and x.get('observation')==obs[str(i)],'bounded reading credit '+str(i))
  check(bool(x.get('purpose')) and bool(x.get('next_owner')) and bool(x.get('date_evidence')),'reading evidence cells '+str(i))
 inherited=t.get('inherited',{});check(inherited.get('status')=='accepted-pending-integration' and inherited.get('owners')==[686,807,346] and inherited.get('outcomes')==t39['accepted_outcome_routes'] and inherited.get('path_bridge')==t39['path_bridge'],'accepted T39 ownership/outcomes')
 check(t.get('cost_unit')=='logical-object-bytes' and t.get('disk_savings_claim') is False,'logical bytes are not savings')
 context=t.get('context',[]);check(len(context)==701 and all(x.get('interpretation')=='context-or-template-not-defect' for x in context),'context/template boundary')
 check(t.get('entrypoints')==read(P/'p1-routes/entrypoints.json'),'entrypoint identities')
 if errors:
  print('REFUSE '+ '; '.join(errors));return 1
 print('PASS complete T46 table: exact source/groups/routes/readings/inherited owners and cost units');return 0

def fixtures():
 original=read(A/'stage-b/table.json');out=A/'stage-c/table-fixtures';dump(out/'positive.json',original)
 mutations={
 'omitted-folder':lambda t:t['groups'].pop('research'),
 'changed-source':lambda t:t['source_summary'].__setitem__('source_tree','0'*40),
 'duplicate-route':lambda t:t['routes'].append(copy.deepcopy(t['routes'][0])),
 'omitted-route':lambda t:t['routes'].pop(),
 'whole-file-credit':lambda t:t['readings'][13].__setitem__('whole_file_read',True),
 'history-as-defect':lambda t:t['routes'][0].__setitem__('interpretation','current-defect'),
 't39-as-new':lambda t:t['inherited'].__setitem__('status','unreviewed-new'),
 'logical-as-savings':lambda t:t.__setitem__('cost_unit','disk-savings-bytes')}
 for name,fn in mutations.items():
  t=copy.deepcopy(original);fn(t);dump(out/(name+'.json'),t)
 print('CREATED complete positive and 8 separately mutated table fixtures (route duplicate and omission separately).')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['assemble','validate','fixtures']);p.add_argument('input',nargs='?');args=p.parse_args()
 if args.mode=='assemble':assemble()
 elif args.mode=='fixtures':fixtures()
 else:sys.exit(validate(read(pathlib.Path(args.input))))
