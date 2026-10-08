from pathlib import Path
import hashlib,json,datetime,subprocess,zipfile,shutil,os,sqlite3,re,sys
O=Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
def write(name,obj):
    p=O/'artifacts'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
(O/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
    profiles=[]
    for owner,names in [('02',['vm18-x86_64','h70002-arm','sm855003-arm']),('03',['h70002-aarch64']),('05',['sm855003-aarch64'])]:
        prev=Path('/workspace/tmp/pixelelated-m7-final-inventory-'+owner)
        for p in json.loads((prev/'profiles.json').read_text()):
            if p['name'] not in names:continue
            d=prev/'artifacts'/p['name'];components=json.loads((d/'components.json').read_text());inputs=json.loads(Path(p['inputs']).read_text())
            assert components['input_manifest_sha256']==sha(p['inputs'])
            assert components['consumed_inventory_sha256']==sha(d/'source-inventory.json')
            assert inputs['distribution_commit']==components['distribution_commit']
            assert sha(p['original_inputs'])==p['original_inputs_sha256']
            assert json.loads(Path(p['bundle'],'manifest.json').read_text())['inputs']==json.loads(Path(p['original_inputs']).read_text())
            p.update(inventory_owner=str(prev),components_path=str(d/'components.json'),components_sha256=sha(d/'components.json'),source_inventory_path=str(d/'source-inventory.json'),source_inventory_sha256=sha(d/'source-inventory.json'),counts=components['counts'],missing_recipe_license=components['missing_recipe_license'])
            profiles.append(p)
    assert len(profiles)==5
    write('profiles.json',profiles)
    print('PASS five exact-image profiles composed with original report hashes',flush=True)
    archives=O/'retained-inputs';archives.mkdir()
    rclones=[]
    for arch,wanted in [('amd64','982b5aa772841168f8e380f139e9e787b2a105403e32b94da8676a0e1c0a13ab'),('arm64','03f2504174034b6d004152ed7369251c9a9ec1f7e0836eda420f5c7a5ec0dff9')]:
        name='rclone-v1.75.1-linux-'+arch+'.zip';dest=archives/name;url='https://downloads.rclone.org/v1.75.1/'+name
        if arch=='amd64':
            prior=Path('/workspace/artifacts/pixelelated-build-inputs/m7-cold-01-consumed/0d5570db7b689e96fb5e3d33293a5275e92d6df244acbcb8a1db1929bc3f491b')/name
            assert sha(prior)==wanted;shutil.copy2(prior,dest)
        else:
            subprocess.run(['curl','--fail','--location','--proto','=https','--retry','2','--max-time','90','--output',str(dest),url],check=True)
        assert sha(dest)==wanted
        with zipfile.ZipFile(dest) as z:
            binary=z.read('rclone-v1.75.1-linux-'+arch+'/rclone');h=hashlib.sha256(binary).hexdigest()
        matches=[]
        for p in profiles:
            if p['arch']!=('x86_64' if arch=='amd64' else 'aarch64'):continue
            inp=json.loads(Path(p['inputs']).read_text());f=Path(p['tree'])/inp['build_root']/'build/rclone-1.75.1'/('rclone-v1.75.1-linux-'+arch)/'rclone'
            assert sha(f)==h;matches.append(p['name'])
        rclones.append({'arch':arch,'archive_path':str(dest),'archive_sha256':wanted,'url':url,'unpacked_binary_sha256':h,'matching_profiles':matches,'claim':'Exact versioned prebuilt archive recovered and matches unpacked binary; source/licence publication remains separate'})
    write('rclone-archives.json',rclones);print('PASS amd64 and arm64 rclone archives match frozen recipe and unpacked binaries',flush=True)
    notices=[];extra=[]
    for p in profiles:
        components=json.loads(Path(p['components_path']).read_text());inp=json.loads(Path(p['inputs']).read_text());b=Path(p['tree'])/inp['build_root']
        for c in components['components']:
            r=c['unpacked_source']
            if c['component'] in components['missing_recipe_license']:
                roots=[]
                if r and r.get('unpacked'):roots.append(b/'build'/r['unpacked'])
                roots.append(Path(p['tree'])/Path(c['recipe']).parent)
                files={}
                for root in roots:
                    for f in list(root.glob('*'))+list(root.glob('*/*')):
                        if not f.is_file() or f.is_symlink() or not re.match(r'(?i)^(copying|copyright|licen[cs]e|notice|authors)([._-]|$)',f.name):continue
                        if f.stat().st_size>1024*1024:continue
                        h=sha(f);dest=O/'artifacts/notices'/h;dest.parent.mkdir(exist_ok=True)
                        if not dest.exists():shutil.copy2(f,dest)
                        files[str(f)]={'sha256':h,'retained_notice':str(dest.relative_to(O/'artifacts'))}
                notices.append({'profile':p['name'],'component':c['component'],'recipe':c['recipe'],'recipe_sha256':c['recipe_sha256'],'notice_candidates':files,'disposition':'HOLD for source review; candidate notice presence is not a licence conclusion. Empty candidates require upstream source/notice retrieval.'})
            if r and r.get('downloaded_asset'):
                a=r['downloaded_asset'];src=Path(a['installed_path']);dest=archives/(a['sha256']+'-doom.tar.gz')
                assert sha(src)==a['sha256']
                if not dest.exists():shutil.copy2(src,dest)
                assert sha(dest)==a['sha256'];extra.append({'profile':p['name'],'component':c['component'],'retained_path':str(dest),**a})
    write('missing-license-notices.json',notices);write('install-time-assets.json',extra)
    print('PASS notice candidates and exact install-time shareware bytes retained',flush=True)
    inp=json.loads(Path('/workspace/tmp/pixelelated-m7-sm8550-refresh-03/inputs.json').read_text());store=Path(inp['nix_private_store'])
    archive_rows=[]
    for name,h in inp['nix_archive_hashes'].items():
        assert sha(name)==h;archive_rows.append({'path':name,'sha256':h,'bytes':Path(name).stat().st_size})
    toolchains=[];roots={'/nix/store/hymgd36hiy3g3pj7pyj6a53q7rbaip3i-fex-dev-rootfs'}
    for name,h in inp['nix_toolchain_hashes'].items():
        path=store/Path(name).relative_to('/nix');assert sha(path)==h
        refs=sorted(set(re.findall(r'/nix/store/[a-z0-9]{32}-[a-zA-Z0-9_.+-]+',path.read_text())));roots.update(refs);roots.add(name)
        toolchains.append({'store_path':name,'sha256':h,'referenced_roots':refs})
    db=store/'var/nix/db/db.sqlite';con=sqlite3.connect('file:'+str(db)+'?mode=ro',uri=True);con.row_factory=sqlite3.Row
    paths={r['path']:dict(r) for r in con.execute('select id,path,hash,deriver,narSize from ValidPaths')};ids={r['id']:r for r in paths.values()};edges={}
    for row in con.execute('select referrer,reference from Refs'):edges.setdefault(row[0],[]).append(row[1])
    reached=set();todo=[paths[n]['id'] for n in roots]
    while todo:
        node=todo.pop()
        if node in reached:continue
        reached.add(node);todo.extend(edges.get(node,[]))
    rows=[]
    for node in sorted(reached):
        item=ids[node];host=store/Path(item['path']).relative_to('/nix');assert host.exists() or host.is_symlink(),str(host)
        item={**item,'references':[ids[n]['path'] for n in edges.get(node,[])]}
        if item['deriver']:
            drv=store/Path(item['deriver']).relative_to('/nix');item['deriver_retained']=drv.is_file();item['deriver_sha256']=sha(drv) if drv.is_file() else None
        rows.append(item)
    write('nix-input-closure.json',{'nix_version':inp['nix_version'],'snapshot_url':inp['nixpkgs_url'],'archives':archive_rows,'store':str(store),'toolchains':toolchains,'roots':sorted(roots),'referenced_store_paths':rows,'scope':'Read-only Nix database reference closure with exact toolchain/archive hashes and retained derivations. Registered NAR hashes are metadata, not independently rehashed NARs. This is build-input custody evidence, not corresponding-source or licence clearance.'})
    print('PASS Nix toolchains, archives and '+str(len(rows))+' referenced store paths recorded',flush=True)
    write('result.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_COMPONENT_INPUT_MAPPING_WITH_PUBLICATION_HOLDS','profiles':len(profiles),'unique_missing_recipe_license':sorted(set(n for p in profiles for n in p['missing_recipe_license'])),'notice_rows':len(notices),'recovered_archives':len(rclones),'install_time_assets':len(extra),'nix_reference_paths':len(rows),'publication_bundle_complete':False,'remaining':'Review notices and redistribution/source disposition, retain/retrieve complete corresponding-source bundle in fork-owned backed-up custody, complete release/physical gates.'})
    rc=0
finally:
    (O/'inner.rc').write_text(str(rc)+'\n');(O/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
