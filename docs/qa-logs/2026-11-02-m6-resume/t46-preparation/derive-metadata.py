import ast,collections,datetime,hashlib,json,pathlib,subprocess
P='2174265e9cc1b248c0fbe27fa101875984d46d6b'
C='92e8d07b6163ec5ddd3e9b67f1c42a472b2911d1'
T39='7994f760fe1f4df6744844e80433bc49295cb94e'
OUT=pathlib.Path(__file__).parent
ROOTS=['docs/'+x for x in ['qa-logs','qa-frames','audits','work-logs','retros','retrospective','futros']]+['research','.github/sessions','docs/reviews/inventory.json']
COMMANDS=[]
def git(*args):
    COMMANDS.append(['git',*args])
    return subprocess.check_output(['git',*args])
def sha(b):return hashlib.sha256(b).hexdigest()
def meta(ref,path):
    h,p=git('ls-tree','-l','-z',ref,'--',path).rstrip(b'\0').split(b'\t',1)
    m,t,o,n=h.split()
    return dict(path=p.decode(),mode=m.decode(),type=t.decode(),blob=o.decode(),bytes=int(n))
def tree(ref):
    raw=git('ls-tree','-r','-l','-z',ref,'--',*ROOTS);d={}
    for entry in raw.split(b'\0'):
        if not entry:continue
        h,p=entry.split(b'\t',1);m,t,o,n=h.split()
        assert t==b'blob' and n!=b'-'
        d[p]=(m.decode(),t.decode(),o.decode(),int(n))
    return d,dict(raw_ls_tree_sha256=sha(raw),canonical_metadata_sha256=sha(canonical(d)))
def canonical(d):
    return b''.join(p+b'\0'+('\0'.join(map(str,d[p]))).encode()+b'\0' for p in sorted(d))
def stats(d):
    u={v[2]:v[3] for v in d.values()}
    return dict(paths=len(d),logical_bytes=sum(v[3] for v in d.values()),unique_blobs=len(u),unique_blob_logical_bytes=sum(u.values()),modes=dict(sorted(collections.Counter(v[0] for v in d.values()).items())),git_types=dict(sorted(collections.Counter(v[1] for v in d.values()).items())))
def folder(p):return '/'.join(p.decode().split('/')[:2])
def suffix(p):return pathlib.PurePosixPath(p.decode()).suffix.lower() or '(no suffix)'
def compact(d,limit=25):
    items=sorted(d.items(),key=lambda kv:(-kv[1].get('c_paths',kv[1].get('paths',0)),kv[0]))
    if len(items)<=limit:return dict(items)
    rest=collections.Counter()
    for k,v in items[limit:]:rest.update(v)
    return dict(items[:limit]+[('(remaining '+str(len(items)-limit)+' groups)',dict(rest))])
inputs={}
for path in ['docs/reviews/inventory.json','docs/reviews/areas.json','docs/reviews/slices.json','tools/renovation-inventory']:
    b=git('show',P+':'+path);m=meta(P,path)
    assert m==meta(C,path)
    inputs[path]={**m,'sha256':sha(b),'identical_at_both_pins':True}
    if path.endswith('inventory.json'):inv=json.loads(b)
    elif path.endswith('areas.json'):areas=json.loads(b)
    elif path.endswith('slices.json'):slices=json.loads(b)
    else:generator=b
area=next(x for x in areas if x['area']=='records')
assert area['globs']==['docs/{qa-logs,qa-frames,audits,work-logs,retros,retrospective,futros}/**','research/**','.github/sessions/**','docs/reviews/inventory.json']
sl=next(x for x in slices['slices'] if x['id']=='records')
assert sl['select']=={} and sl['kind']=='table' and sl['k']==46
for node in ast.parse(generator).body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CODE' for t in node.targets):CODE=ast.literal_eval(node.value)
def isread(r):return r['language'] in CODE and r['tier']!='vendor-carried' and r['reach']!='unreached'
rows=[dict(zip(inv['columns'],r)) for r in inv['rows'] if r[inv['columns'].index('area')]=='records']
assert len(rows)==126149 and sum(r['lines'] or 0 for r in rows)==22984582
assert sum(r['lines'] or 0 for r in rows if isread(r))==15392661
def counted(key):
    d=collections.defaultdict(lambda:dict(paths=0,inventory_lines=0,generated_read_lines=0))
    for r in rows:
        v=d[key(r)];v['paths']+=1;v['inventory_lines']+=r['lines'] or 0
        if isread(r):v['generated_read_lines']+=r['lines'] or 0
    return dict(sorted(d.items(),key=lambda kv:(-kv[1]['paths'],kv[0])))
survey={r['path'].encode() for r in rows};assert len(survey)==len(rows)
p,ph=tree(P);c,ch=tree(C);assert not survey-p.keys()
added=c.keys()-p.keys();deleted=p.keys()-c.keys();changed={k for k in p.keys()&c.keys() if p[k]!=c[k]}
unchanged=(p.keys()&c.keys())-changed
raw=git('diff-tree','--no-commit-id','-r','--raw','--no-abbrev','-z','--no-renames',P,C,'--',*ROOTS)
rs=raw.split(b'\0');rawsets=collections.defaultdict(set)
for i in range(0,len(rs)-1,2):rawsets[rs[i].split()[-1].decode()].add(rs[i+1])
assert rawsets=={'A':added,'D':deleted,'M':changed}
def empty():return dict(p1_paths=0,p1_bytes=0,c_paths=0,c_bytes=0,added=0,deleted=0,changed=0)
groups=collections.defaultdict(empty);types=collections.defaultdict(empty)
for data,tag in [(p,'p1'),(c,'c')]:
    for path,v in data.items():
        for g in [groups[folder(path)],types[suffix(path)]]:
            g[tag+'_paths']+=1;g[tag+'_bytes']+=v[3]
for paths,tag in [(added,'added'),(deleted,'deleted'),(changed,'changed')]:
    for path in paths:groups[folder(path)][tag]+=1;types[suffix(path)][tag]+=1
adds=collections.defaultdict(lambda:dict(paths=0,logical_bytes=0))
for path in added:
    g='/'.join(path.decode().split('/')[:3]);adds[g]['paths']+=1;adds[g]['logical_bytes']+=c[path][3]
roots={}
for ref in [P,C,T39]:
    assert git('rev-parse',ref+'^{commit}').decode().strip()==ref
    roots[ref]=git('rev-parse',ref+'^{tree}').decode().strip()
entrypoints=[
 ('docs/reviews/README.md','1-45; ownership and inventory conventions',C),
 ('docs/reviews/order.md','1-29; 673-681 T39; 743-751 T46',C),
 ('docs/reviews/plan-for-the-plan.md','sections 5, 6b, 7, 8 and 9',C),
 ('docs/audits/README.md','all 20 lines; placement convention',C),
 ('docs/retros/README.md','all 3 lines; placement convention',C),
 ('docs/futros/README.md','all 3 lines; placement convention',C),
 ('docs/work-logs/INDEX.md','1-45; generated-index convention/current month; no day-file body sweep',C),
 ('docs/decision-register.md','D-WORKFLOW-223 and D-WORKFLOW-224 only',C),
 ('.github/sessions/saved-session-state-feature-m6-renovation-plan-346.md','current short pointer; named accepted T39 source/completion',C),
 ('.github/sessions/saved-session-state-feature-m6-doctrine-reference-686.md','Current focus and completion boundary; historical commands not executed',T39)]
entries=[dict(ref=ref,read_scope=scope,**meta(ref,path)) for path,scope,ref in entrypoints]
r={
 'schema':1,'purpose':'Bounded T3 T46 #693 planning inputs; not an execution baseline, audit, final population recut, brief or disposition',
 'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'identity':{'harness':'Codex','model_label':'GPT-6-Astra','effort_label':'xhigh','basis':'actual harness identity recovered in this session; not provider attestation','session':'01a19d12-29e3-7fe0-9f41-038dac0a5deb','lane':'m6-t3-emulators','pane':'wN:p6','recipient':'m6-coordinator wN:p2'},
 'cpu_affinity':'8-23, inherited by child commands',
 'pins':{'P1':P,'coordinator_frozen':C,'root_trees':roots,'inventory_distribution_source':inv['header']['distribution']['head'],'inventory_generation_fields':{k:v for k,v in inv['header'].items() if k.startswith('generated')},'T39_completion':T39,'T39_accepted_source':'4eb5dfab8e745914a55e7de3e5a43c5b91ebc608','T41_accepted_source_unchanged':'e481e4a4a5c296c8f12e9654b6a45c4fb27bd3b0','T41_completion_unchanged':'83304388db49e24231158380910067c47ead3f12'},
 'api_sources':json.loads((OUT/'api-source-digests.json').read_text()),'immutable_input_files':inputs,'entrypoints':entries,
 'selector':{'area':area,'slice':sl,'metadata_root_arguments':ROOTS,'interpretation':'inventory area == records; empty slice selector adds no reach/tier/glob filter. Expanded roots implement the unchanged records area globs as an observational frozen metadata boundary, not a final population decision.'},
 'survey':{'inventory_total_rows':len(inv['rows']),'selected_rows':len(rows),'unique_selected_paths':len(survey),'inventory_lines':sum(r['lines'] or 0 for r in rows),'generated_read_lines':sum(r['lines'] or 0 for r in rows if isread(r)),'generated_read_predicate':'language in CODE and tier != vendor-carried and reach != unreached; sum (lines or 0)','CODE':sorted(CODE),'table_budget':'table kind has no code-read line bound; order displays -- (126149 rows)','line_origin':'Stored inventory column: generator line_counts uses git diff-tree --numstat EMPTY_TREE HEAD; binary - becomes null. Not re-counted here.','tree_counts':dict(collections.Counter(r['tree'] for r in rows)),'tier_counts':dict(collections.Counter(r['tier'] for r in rows)),'reach_counts':dict(collections.Counter(r['reach'] for r in rows)),'null_line_rows':sum(r['lines'] is None for r in rows),'path_set_sha256':sha(b''.join(x+b'\0' for x in sorted(survey))),'by_folder':counted(lambda r:'/'.join(r['path'].split('/')[:2])),'by_language':counted(lambda r:r['language']),'inventory_self_row':next(r for r in rows if r['path']=='docs/reviews/inventory.json')},
 'frozen_metadata':{'P1':{**stats(p),**ph},'coordinator':{**stats(c),**ch},'canonical_encoding':'sort by raw path bytes; each entry path NUL mode NUL type NUL blob_oid NUL decimal_size NUL; SHA256 concatenation. Raw digest covers exact ls-tree -r -l -z output for ordered ROOTS.','by_folder':dict(sorted(groups.items())),'by_filename_suffix_top25_plus_remainder':compact(types)},
 'reconciliation':{'survey_absent_P1':len(survey-p.keys()),'P1_outside_survey':len(p.keys()-survey),'P1_outside_survey_paths':[x.decode() for x in sorted(p.keys()-survey)],'survey_absent_coordinator':len(survey-c.keys()),'coordinator_outside_survey':len(c.keys()-survey),'equation':'126149 survey +1 later P1 retro =126150 P1; +522 adds -2 deletions =126670 coordinator. 3 changes do not change path count. Coordinator retained survey=126147, outside survey=523.'},
 'delta':{'added':len(added),'deleted':len(deleted),'changed':len(changed),'unchanged':len(unchanged),'blob_changed':sum(p[x][2]!=c[x][2] for x in changed),'mode_changed':sum(p[x][0]!=c[x][0] for x in changed),'logical_byte_delta':sum(v[3] for v in c.values())-sum(v[3] for v in p.values()),'raw_diff_sha256':sha(raw),'raw_diff_matches_tree_comparison':True,'rename_detection':False,'added_by_subfolder_top25_plus_remainder':compact(adds),'changed_paths':[{'path':x.decode(),'P1':dict(zip(['mode','type','blob','bytes'],p[x])),'coordinator':dict(zip(['mode','type','blob','bytes'],c[x]))} for x in sorted(changed)],'deleted_metadata_sha256':sha(canonical({x:p[x] for x in deleted})),'deletion_note':'Two existing deletions under research/council-runs/verification have credential-labelled filenames. Only path/mode/blob/size metadata observed; no content read/recovery, exported path list or proposed cleanup.'},
 'limits':[
 'Only new private report scratch is written; no repository/tracker/kit edit, commit, push, merge, checkout, tree export, live worktree scan, cleanup or final membership recut.',
 'No audit-log body sweep, held/private directory or credential-content read, host/cache/process inspection, runtime/build/guest, fetch/provider/device/cloud action, accepted replay or permission answer.',
 'Complete metadata path lists exist only in memory. No 120000 symlinks or 160000 gitlinks in either frozen selected set; no target resolution or broad Markdown link traversal.',
 'Coordinator snapshot is not the integrated final tree. Accepted T39/T41 references are not inferred merged content. No lane-branch union measured.',
 'Inventory is hosted at P1 but describes eb4763e3cc9bcd729830cd85f1719bbd4f28db10. Stored lines, languages and reach are survey facts; not new source semantic or execution findings.',
 'Logical bytes and unique-blob logical bytes do not measure pack/disk use, compression, runtime cost or attainable deletion savings.',
 'Plan/register/reviews README context paths outside records remain context, not added members. Generated inventory and work-log index remain members; source links remain separate and untraversed.',
 'T39 completed corrections remain complete. D223/D224 and #1407 reserve later monthly indexing and individual Q5 disposition: 33 documents/2770 lines, 32 T39 scope plus one table-only plan. Low links are not nonuse.',
 'T46 stays last. Root retains scope, final baseline/membership, brief, criteria, dispatch, dispositions and integration. Frozen pointer state text cannot substitute for live root scheduling.'
 ],
 'future_inputs_not_decisions':[
 'Compact binding option: pin inventory/areas/slices blobs and source commits; retain the survey path-set digest and frozen metadata digests with the stated NUL-safe encoding. Root chooses whether original survey or integrated additions form final membership.',
 'Keep stored survey, later P1 additions and frozen coordinator delta separate. Use fixed input commits before output generation. This preparation does not regenerate inventory/order or receipt programs.',
 'Avoid recursive self-counting: prior inventory self-row is historical (134637 stored lines); new report output stays outside the measured input tree. Bind a future census to its input commit rather than its own output. Label generated indexes without silently excluding their paths.',
 'Candidate substantive reader routes: reviews README to plan/order and source maps, audit/retro/futro conventions, generated work-log index to selected days, and current coordinator/producer pointers. Root selects paths and acceptance criteria; this is not a link or factual-currency audit.',
 'Metadata now measures paths/modes, inventory language/line totals, logical bytes, unique blobs, frozen additions/deletions/changes and group distributions. Suffixes label filenames, not semantic purpose.',
 'Later authorized proof is needed for reader use/value, currency versus history, path/anchor/line-citation resolution, full integrated population, packed/disk costs and runtime costs. Repeated blob references or large byte totals are not retirement evidence.',
 '#1407 owns monthly-index organization and individual rarely linked reference dispositions, preserving dates/content, provenance and caller/anchor/line mappings. Future T46 ownership must not duplicate completed T39 corrections or preempt the backlog.'
 ],
 'commands':{'cwd':'/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688','wrapper':'taskset -c 8-23 python3 /workspace/tmp/m6-t46-t3-20261102-planning/derive-metadata.py','git_argv':COMMANDS,'not_run':['renovation-inventory','renovation-status','renovation-drift','accepted controls','git archive','git diff --numstat','source/config evaluation']},
 'checks':{'inventory_counts_exact':True,'all_survey_paths_resolve_P1_without_decode':True,'selectors_and_generator_unchanged':True,'raw_metadata_diff_matches_two_trees':True,'all_selected_objects_are_blobs':True}
}
r['derivation_script_sha256']=sha(pathlib.Path(__file__).read_bytes())
output=(json.dumps(r,sort_keys=True,indent=2)+'\n').encode()
(OUT/'report.json').write_bytes(output)
print(json.dumps({'report_json_sha256':sha(output),'script_sha256':r['derivation_script_sha256'],'report_bytes':len(output),'P1':stats(p),'coordinator':stats(c),'delta':{k:v for k,v in r['delta'].items() if k in ['added','deleted','changed','unchanged','logical_byte_delta']},'inventory_generation':r['pins']['inventory_generation_fields']},indent=2))
