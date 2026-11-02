import pathlib, subprocess, json, hashlib, csv, io, collections, posixpath, os, ast, re
P=pathlib.Path(__file__).resolve().parent; R=P/'proof'
B='afdec2bf8b88135befcb7ec56efb3a7ea327bd73'; P1='2174265e9cc1b248c0fbe27fa101875984d46d6b'
assert sorted(os.sched_getaffinity(0))==list(range(8,24))
env=os.environ.copy();env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_OPTIONAL_LOCKS='0')
commands=[]
def git(*a):
    x=subprocess.run(['git','-C',str(R),*a],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    commands.append({'argv':['git','-C',str(R),*a],'rc':x.returncode,'stdout_sha256':hashlib.sha256(x.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(x.stderr).hexdigest()})
    return x.stdout
def show(ref,path):return git('show',ref+':'+path)
prep='docs/qa-logs/2026-11-02-m6-resume/t43-preparation/'
packets={name:show(B,prep+name) for name in ['report.md','members.tsv','results.json','recipes.json','context-inputs.json']}
manifest=list(csv.DictReader(io.StringIO(packets['members.tsv'].decode()),delimiter='\t'))
manifest_actual=hashlib.sha256(packets['members.tsv']).hexdigest()
assert manifest_actual=='d89d6fe612587635c2bb6d1101362242f03b9f0c3c391015f5344c2357eb1c49'
assert packets['members.tsv'].count(b'\\u002d')==1
assert hashlib.sha256(packets['members.tsv'].replace(b'\\u002d',b'-')).hexdigest()=='ccbbe1543349e51f56545afc3e96aadc3fc3e965e19b1fdb18731ee809cc083e'
manifest=list(csv.DictReader(io.StringIO(packets['members.tsv'].decode().replace('\\u002d','-')),delimiter='\t'))
ret=json.loads(packets['results.json']); recipes=json.loads(packets['recipes.json'])
out=pathlib.Path((P/'membership-output-path.txt').read_text().strip())/'source'
rows=json.loads((out/'rows.json').read_text()); tree=json.loads((out/'tree.json').read_text()); summary=json.loads((out/'summary.json').read_text())
by={r['path']:r for r in rows}; assert set(by)=={r['path'] for r in manifest}
for row in manifest:
    path=row['path']; data=show(B,path); rc=by[path]; t=tree[path]
    assert t['mode']==row['mode'] and t['oid']==row['blob_at_both_refs']
    assert rc['lines']==int(row['inventory_lines'])==int(row['logical_lines'])==data.count(b'\n')+int(bool(data) and not data.endswith(b'\n'))
    assert len(data)==int(row['bytes']) and rc['reach']==row['reach'] and ','.join(rc['buildable_by'])==row['buildable_by']
    assert rc['tier_note'] is None and row['tier_note']=='-'
groups={k:collections.defaultdict(lambda:{'paths':0,'inventory_lines':0}) for k in ['directory_groups','scope_groups','buildable_combinations','per_target_nonadditive']}
for row in rows:
    path=row['path']; parts=path.split('/'); scope='/'.join(parts[:4]) if parts[2]=='devices' else path.split('/patches/')[0]
    keys={'directory_groups':[posixpath.dirname(path)],'scope_groups':[scope],'buildable_combinations':[','.join(row['buildable_by'])],'per_target_nonadditive':row['buildable_by']}
    for k,values in keys.items():
        for val in values:groups[k][val]['paths']+=1;groups[k][val]['inventory_lines']+=row['lines']
for k,expected in [('directory_groups',72),('scope_groups',31),('buildable_combinations',28),('per_target_nonadditive',21)]:
    assert dict(groups[k])==ret[k],k
    assert len(groups[k])==expected,k
paths=sorted(by)
delta=git('diff','--name-only','--no-ext-diff','--no-textconv','c445081a59518f37d9776e5412dd7b14910696f7',B,'--',*paths)
assert delta==b''
partition=collections.defaultdict(lambda:[0,0])
for row in rows:
    k='config' if row['language']=='kernel-config' else 'linux' if '/patches/linux/' in row['path'] or '/packages/linux/patches/' in row['path'] else 'other'
    partition[k][0]+=1; partition[k][1]+=row['lines']
assert dict(partition)=={'config':[12,101229],'other':[74,4793],'linux':[346,222494]},partition
source=show(P1,'tools/renovation-inventory').decode(); names={'glob_re','glob_body','load_areas','assign','slice_of'}
nodes=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in names]
ns={'re':re,'defaultdict':collections.defaultdict,'CannotRun':RuntimeError};exec(compile(ast.Module(body=nodes,type_ignores=[]),'<verified P1 selectors>','exec'),ns)
sl=json.loads(show(P1,'docs/reviews/slices.json')); compiled=[]
for s in sl['slices']:
    sels=s.get('select',{}); sels=sels if isinstance(sels,list) else [sels]; cs=[]
    for sel in sels:
        cs.append((set(sel.get('areas',[s['area']])),ns['load_areas']([{'area':s['id'],'globs':sel['globs']}])[0] if sel.get('globs') else None,set(sel['reach']) if sel.get('reach') else None,bool(sel.get('rest')),set(sel['tier']) if sel.get('tier') else None))
    compiled.append((s,cs))
inv=json.loads(show(P1,'docs/reviews/inventory.json')); invrows={r['path']:r for r in (dict(zip(inv['columns'],a)) for a in inv['rows']) if r['tree']=='distribution'}
ownership=collections.defaultdict(lambda:[0,0]); verified_recipes=[]; assigned=[]
for path,row in recipes.items():
    data=show(B,path); assert hashlib.sha256(data).hexdigest()==row['sha256_P1']==summary['recipe_sha256'][path]
    lines=data.decode().splitlines()
    for n,text in row['static_selector_excerpt']:assert lines[n-1]==text,(path,n)
    for n,text in row['version_lines']:assert lines[n-1]==text,(path,n)
    owner=ns['slice_of'](invrows[path],compiled);assert owner==row['owner_P1']==row['owner_coordinator']
    members=[r['path'] for r in rows if posixpath.dirname(r['path']) in row['member_directories']]
    assert len(members)==row['paths'],(path,len(members),row['paths']); assigned+=members
    ownership[owner[0]][0]+=1;ownership[owner[0]][1]+=len(members)
    verified_recipes.append({'path':path,'sha256':hashlib.sha256(data).hexdigest(),'owner':owner,'member_count':len(members),'mode_blob':tree.get(path) or git('ls-tree',B,'--',path).decode().strip(),'version_lines':row['version_lines']})
assert len(assigned)==len(set(assigned))==432
assert dict(ownership)=={'devices-unshipped':[12,25],'image-packages':[10,36],'emulators-standalone':[3,3],'packages-dead-ends':[5,10],'device-generic-x64-and-kernel':[1,358]}
links=[]
for row in json.loads((out/'symlinks.json').read_text()):
    assert by[row['resolved']]['lines'] in [34,37]
    links.append(dict(row,link_mode_blob=tree[row['path']],referent_mode_blob=tree[row['resolved']],referent_lines=by[row['resolved']]['lines']))
inbound='projects/ROCKNIX/packages/apps/mangohud/patches/SM8550/0002-SM8750-Battery.patch'
assert ns['slice_of'](invrows[inbound],compiled)==['patches-shipped']
target=show(B,inbound).decode();resolved=posixpath.normpath(posixpath.join(posixpath.dirname(inbound),target))
assert resolved==links[1]['resolved'];assert show(B,inbound)==show(P1,inbound)
inbound_record={'path':inbound,'target':target,'resolved':resolved,'mode_blob':git('ls-tree',B,'--',inbound).decode().strip(),'owner':'T42 patches-shipped','referent_owner':'T43 patches-unshipped'}
contexts=[]
for c in json.loads(packets['context-inputs.json']):
    data=show(c['ref'],c['path']); oid=git('rev-parse',c['ref']+':'+c['path']).decode().strip()
    assert hashlib.sha256(data).hexdigest()==c['sha256'] and oid==c['blob'];contexts.append(c)
result={'PASS':True,'paths':432,'logical_lines':328516,'newlines':328512,'bytes':10690267,'modes':dict(collections.Counter(x['mode'] for x in tree.values())),
 'manifest_sha256':hashlib.sha256(packets['members.tsv']).hexdigest(),'path_list_sha256':summary['path_list_sha256'],'fork_written':0,'fork_base_selected_delta':[],'partitions':partition,
 'groups':groups,'recipe_ownership':ownership,'recipes':verified_recipes,'links':links,'inbound':inbound_record,'contexts':contexts,'preparation_hashes':{k:hashlib.sha256(v).hexdigest() for k,v in packets.items()}}
(P/'reconciliation.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(P/'read-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
print('PASS 432 manifest rows, 328516 logical lines, modes, links, zero fork delta, 72/31/28/21 groups, 31 exact recipe ownership bindings, retained context hashes')
