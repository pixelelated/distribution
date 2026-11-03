"""T3 bounded T46 metadata transition; no prior producer or source body replay."""
import argparse,collections,datetime,hashlib,json,os,pathlib,subprocess,sys
ROOT='/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346'
OLD='92e8d07b6163ec5ddd3e9b67f1c42a472b2911d1'
NEW='d707c82ab8c48b674acc1f95a9571f0cb24d226a'
PRIOR='docs/qa-logs/2026-11-02-m6-resume/t46-preparation/report.json'
PRIOR_SHA='713f999d552cdacce9e59bd062ac7b410b11ce26bf427860412b09de185a0b98'
CANONICAL=['docs/reviews/inventory.json','docs/reviews/areas.json','docs/reviews/slices.json','tools/renovation-inventory']
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--old',default=OLD)
ap.add_argument('--new',default=NEW)
ap.add_argument('--prior-ref',default=NEW)
ap.add_argument('--out',type=pathlib.Path,required=True)
args=ap.parse_args()
commands=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*argv):
    full=['git','-C',ROOT,*argv]
    b=subprocess.check_output(full,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    commands.append({'argv':full,'exit':0,'stdout_bytes':len(b),'stdout_sha256':sha(b)})
    return b
def parse_tree(raw):
    d={}
    for row in raw.split(b'\0'):
        if not row:continue
        h,p=row.split(b'\t',1);mode,kind,oid,size=h.split()
        if p in d:raise ValueError('duplicate tree key')
        d[p]=(mode.decode(),kind.decode(),oid.decode(),None if size==b'-' else int(size))
    return d
def canonical(d):
    return b''.join(p+b'\0'+('\0'.join(str(v) if v is not None else '-' for v in d[p])).encode()+b'\0' for p in sorted(d))
def canonical_sha(d):return sha(canonical(d))
def path_digest(paths):return sha(b''.join(p+b'\0' for p in sorted(paths)))
def stats(d):
    blobs={v[2]:v[3] for v in d.values() if v[1]=='blob'}
    return {'paths':len(d),'logical_bytes':sum(v[3] or 0 for v in d.values() if v[1]=='blob'),
            'unique_blobs':len(blobs),'unique_blob_logical_bytes':sum(v or 0 for v in blobs.values()),
            'modes':dict(sorted(collections.Counter(v[0] for v in d.values()).items())),
            'git_types':dict(sorted(collections.Counter(v[1] for v in d.values()).items())),
            'nonblob_paths':sum(v[1]!='blob' for v in d.values())}
prior_bytes=git('show',args.prior_ref+':'+PRIOR)
if sha(prior_bytes)!=PRIOR_SHA:raise ValueError('retained prior report identity differs')
prior=json.loads(prior_bytes)
if args.old!=prior['pins']['coordinator_frozen']:raise ValueError('old pin differs from retained baseline')
roots=prior['selector']['metadata_root_arguments']
expected_roots=['docs/qa-logs','docs/qa-frames','docs/audits','docs/work-logs','docs/retros','docs/retrospective','docs/futros','research','.github/sessions','docs/reviews/inventory.json']
if roots!=expected_roots:raise ValueError('retained roots differ')
if prior['selector']['slice']['select']!={} or prior['selector']['slice']['id']!='records':raise ValueError('selector differs')
bindings={}
for ref in [args.old,args.new]:
    d=parse_tree(git('ls-tree','-l','-z',ref,'--',*CANONICAL))
    if len(d)!=len(CANONICAL):raise ValueError('canonical input missing')
    for path in CANONICAL:
        was=prior['immutable_input_files'][path]
        expected=(was['mode'],was['type'],was['blob'],was['bytes'])
        if d[path.encode()]!=expected:raise ValueError('canonical inventory/selector/generator drift')
    bindings[ref]={p.decode():dict(zip(['mode','type','blob','bytes'],v)) for p,v in sorted(d.items())}
pin_trees={}
for ref in [args.old,args.new]:
    if git('rev-parse',ref+'^{commit}').decode().strip()!=ref:raise ValueError('require full immutable commit')
    pin_trees[ref]=git('rev-parse',ref+'^{tree}').decode().strip()
raw_old=git('ls-tree','-r','-l','-z',args.old,'--',*roots)
raw_new=git('ls-tree','-r','-l','-z',args.new,'--',*roots)
old,new=parse_tree(raw_old),parse_tree(raw_new)
old_stats,new_stats=stats(old),stats(new)
baseline=prior['frozen_metadata']['coordinator']
for k in ['paths','logical_bytes','unique_blobs','unique_blob_logical_bytes','modes','git_types']:
    if old_stats[k]!=baseline[k]:raise ValueError('old metadata differs from prior aggregate')
if sha(raw_old)!=baseline['raw_ls_tree_sha256'] or canonical_sha(old)!=baseline['canonical_metadata_sha256']:raise ValueError('old metadata digest differs from retained baseline')
added=new.keys()-old.keys();deleted=old.keys()-new.keys()
common=old.keys()&new.keys();changed={p for p in common if old[p]!=new[p]};unchanged=common-changed
diff=git('diff-tree','--no-commit-id','-r','--raw','--no-abbrev','-z','--no-renames',args.old,args.new,'--',*roots)
parts=diff.split(b'\0');status=collections.defaultdict(set)
for i in range(0,len(parts)-1,2):
    h=parts[i].decode().split();path=parts[i+1]
    if len(h)!=5 or h[4] not in ['A','D','M','T']:raise ValueError('unexpected raw metadata diff shape')
    status[h[4]].add(path)
    if path in old and (h[0].lstrip(':'),h[2])!=(old[path][0],old[path][2]):raise ValueError('raw old metadata differs')
    if path in new and (h[1],h[3])!=(new[path][0],new[path][2]):raise ValueError('raw new metadata differs')
if status['A']!=added or status['D']!=deleted or status['M']|status['T']!=changed:raise ValueError('raw diff and two-tree comparison disagree')
def selected(paths,d):return {p:d[p] for p in paths}
delta={
 'added':len(added),'deleted':len(deleted),'changed':len(changed),'unchanged':len(unchanged),
 'raw_status_counts':{k:len(v) for k,v in sorted(status.items())},
 'mode_changed':sum(old[p][0]!=new[p][0] for p in changed),
 'type_changed':sum(old[p][1]!=new[p][1] for p in changed),
 'object_changed':sum(old[p][2]!=new[p][2] for p in changed),
 'logical_byte_delta':new_stats['logical_bytes']-old_stats['logical_bytes'],
 'added_logical_bytes':stats(selected(added,new))['logical_bytes'],
 'deleted_logical_bytes':stats(selected(deleted,old))['logical_bytes'],
 'changed_before_logical_bytes':stats(selected(changed,old))['logical_bytes'],
 'changed_after_logical_bytes':stats(selected(changed,new))['logical_bytes'],
 'raw_diff_sha256':sha(diff),'raw_diff_equals_two_tree_metadata':True,
 'path_set_digests':{k:path_digest(v) for k,v in [('added',added),('deleted',deleted),('changed',changed),('unchanged',unchanged)]},
 'changed_old_metadata_sha256':canonical_sha(selected(changed,old)),
 'changed_new_metadata_sha256':canonical_sha(selected(changed,new)),
 'added_metadata_sha256':canonical_sha(selected(added,new)),
 'deleted_metadata_sha256':canonical_sha(selected(deleted,old)),
 'rename_detection':False
}
old_blobs={v[2]:v[3] for v in old.values() if v[1]=='blob'}
new_blobs={v[2]:v[3] for v in new.values() if v[1]=='blob'}
new_only=new_blobs.keys()-old_blobs.keys();old_only=old_blobs.keys()-new_blobs.keys()
delta['unique_blob_refs_new_to_selection']=len(new_only)
delta['unique_blob_refs_no_longer_in_selection']=len(old_only)
delta['unique_blob_ref_bytes_new_to_selection']=sum(new_blobs[x] or 0 for x in new_only)
delta['unique_blob_ref_bytes_no_longer_in_selection']=sum(old_blobs[x] or 0 for x in old_only)
groups={}
for root in roots:
    rb=root.encode()
    in_group=lambda p:p==rb or p.startswith(rb+b'/')
    od={p:v for p,v in old.items() if in_group(p)}
    nd={p:v for p,v in new.items() if in_group(p)}
    groups[root]={'old':stats(od),'current':stats(nd),
                  'added':sum(in_group(p) for p in added),'deleted':sum(in_group(p) for p in deleted),
                  'changed':sum(in_group(p) for p in changed),
                  'logical_byte_delta':stats(nd)['logical_bytes']-stats(od)['logical_bytes']}
for tag,total in [('old',old_stats),('current',new_stats)]:
    if sum(g[tag]['paths'] for g in groups.values())!=total['paths']:raise ValueError('root grouping not disjoint/exhaustive')
    if sum(g[tag]['logical_bytes'] for g in groups.values())!=total['logical_bytes']:raise ValueError('root grouping byte mismatch')
for k in ['added','deleted','changed']:
    if sum(g[k] for g in groups.values())!=delta[k]:raise ValueError('delta grouping mismatch')
if delta['added_logical_bytes']-delta['deleted_logical_bytes']+delta['changed_after_logical_bytes']-delta['changed_before_logical_bytes']!=delta['logical_byte_delta']:raise ValueError('byte delta mismatch')
prep=b'docs/qa-logs/2026-11-02-m6-resume/t46-preparation/'
prep_members={p:v for p,v in new.items() if p.startswith(prep)}
selfkey=b'docs/reviews/inventory.json'
report={
 'schema':1,'purpose':'Bounded T3 T46 new metadata transition only; factual input, not audit/baseline/recut/dispatch',
 'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'authority':'https://github.com/pixelelated/distribution/issues/693#issuecomment-6602308433',
 'identity':{'harness':'Codex','model_label':'GPT-6-Astra','effort_label':'xhigh','identity_source':'actual harness identity recovered in session; not provider attestation','session':'01a19d12-29e3-7fe0-9f41-038dac0a5deb','lane':'m6-t3-emulators','pane':'wN:p6','recipient':'m6-coordinator wN:p2'},
 'cpu_affinity':'8-23 for shell and child commands',
 'pins':{'old':args.old,'current_candidate':args.new,'root_trees':pin_trees,'prior_report_ref':args.prior_ref},
 'retained_report':{'path':PRIOR,'sha256':sha(prior_bytes),'bytes':len(prior_bytes),'old_deriver_read_not_run_sha256':prior['derivation_script_sha256']},
 'canonical_input_bindings':bindings,
 'retained_input_sha256_reused_by_identical_blob':{p:prior['immutable_input_files'][p]['sha256'] for p in CANONICAL},
 'selector_reused':prior['selector'],
 'reused_survey':{k:prior['survey'][k] for k in ['selected_rows','unique_selected_paths','inventory_lines','generated_read_lines','table_budget','line_origin','path_set_sha256','inventory_self_row']},
 'reused_source_pins':{k:prior['pins'][k] for k in ['P1','inventory_distribution_source','inventory_generation_fields']},
 'reused_P1_metadata':prior['frozen_metadata']['P1'],
 'reused_prior_reconciliation':prior['reconciliation'],
 'old_metadata':{**old_stats,'raw_ls_tree_sha256':sha(raw_old),'canonical_metadata_sha256':canonical_sha(old),'path_set_sha256':path_digest(old)},
 'current_metadata':{**new_stats,'raw_ls_tree_sha256':sha(raw_new),'canonical_metadata_sha256':canonical_sha(new),'path_set_sha256':path_digest(new)},
 'delta':delta,'by_records_root':groups,
 'inventory_self':{'stored_row_reused':prior['survey']['inventory_self_row'],'old_metadata':dict(zip(['mode','type','blob','bytes'],old[selfkey])),'current_metadata':dict(zip(['mode','type','blob','bytes'],new[selfkey])),'qualification':'134637 is the stored historical self-row line measure at the survey source; not a new measurement of current inventory content. No current source/log body lines counted.'},
 'prior_preparation_already_in_current_input':{'prefix':prep.decode(),'stats':stats(prep_members),'metadata_sha256':canonical_sha(prep_members),'qualification':'The previously committed report files are ordinary frozen-input records. This new comparator/report is outside the pinned source tree and is not recursively counted.'},
 'digest_encoding':'Sorted raw path bytes. Path-set: path + NUL per key. Canonical metadata: path NUL mode NUL type NUL full object OID NUL decimal size (or dash for unknown) NUL per key. Raw digests bind exact NUL-delimited Git output. No path normalization/decoding.',
 'commands':{'git_root':ROOT,'cwd':ROOT,'argv':commands,'invocation':['taskset','-c','8-23','python3','-B',str(pathlib.Path(__file__).absolute()),*sys.argv[1:]]},
 'comparator_sha256':sha(pathlib.Path(__file__).read_bytes()),
 'limits':[
 'Only OLD to CURRENT was newly compared; P1/survey quantities and self-row reused from exact retained prior report. Prior accepted producer was read, never invoked. No inventory/generator/checker/test replay.',
 'Complete path sets and raw listings stay in memory; report persists only public canonical roots, named input identities, group counts and digests. No credential-labelled individual paths or contents printed/exported.',
 'Only immutable Git reads via absolute coordinator root; no T41 or other historical worktree read/edit, live tree scan, repository/ledger/tracker/kit/shared-ref write, source/tree export or branch union.',
 'No record/source body sweep, private/held/cache/process/host inspection, cleanup, builds/guests/runtime/fetch/provider/device/cloud action or permission answer.',
 'Logical blob sizes are not pack/disk use or reclaimable savings. Unique blob references mean identity deduplication in this selected snapshot, not object-store deletion.',
 'Current candidate is not claimed integrated next. Root determines final reading set, cutoff, accepted-branch context, baseline/brief/criteria/epic/proof/acceptance/dispatch. Preparation does not start T46 A-D.',
 'P1 direct routes and T1 accepted T39 bridge remain their separately assigned inputs. No ownership decision or new currency/content verdict.'
 ],
 'checks':{'canonical_inputs_identical_to_prior':True,'old_metadata_matches_retained_prior_counts_and_digests':True,'raw_diff_matches_two_tree_keys_and_mode_object_pairs':True,'root_groups_sum_exactly':True,'logical_byte_delta_reconciles':True}
}
args.out.mkdir(mode=0o700,parents=False,exist_ok=False)
b=(json.dumps(report,indent=2,sort_keys=True)+'\n').encode()
(args.out/'report.json').write_bytes(b)
print(json.dumps({'report':str(args.out/'report.json'),'sha256':sha(b),'bytes':len(b),'current':report['current_metadata'],'delta':delta,'groups':{k:{'old_paths':v['old']['paths'],'current_paths':v['current']['paths'],'added':v['added'],'deleted':v['deleted'],'changed':v['changed'],'logical_byte_delta':v['logical_byte_delta']} for k,v in groups.items()},'comparator_sha256':report['comparator_sha256']},indent=2))
