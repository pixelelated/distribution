from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,tarfile
O=Path(__file__).resolve().parent
D=Path('/workspace/repos/rocknix/docs/qa-logs/2026-10-08-final-inventory')
DEST=Path('/workspace/artifacts/pixelelated-release-sources/.staging-m7-archives-01')
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
    return h.hexdigest()
(O/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n');rc=1
try:
    assert DEST.is_dir();(DEST/'archives').mkdir(exist_ok=True);(DEST/'distribution').mkdir(exist_ok=True)
    files={};mapping=[];git_inputs={};distro={}
    for directory in sorted((D/'profiles').iterdir()):
        bind=json.loads((directory/'binding.json').read_text());assert sha(directory/'components.json')==bind['components_sha256']
        inputs=json.loads(Path(bind['original_inputs']).read_text());assert sha(bind['original_inputs'])==bind['original_inputs_sha256'];distro[inputs['distribution_commit']]=inputs
        for c in json.loads((directory/'components.json').read_text())['components']:
            u=c['unpacked_source'];row={'profile':directory.name,'component':c['component'],'recipe':c['recipe'],'recipe_sha256':c['recipe_sha256'],'members':[]}
            if u:
                for record in u.get('cache',[]):
                    src=Path(inputs['source_cache'])/c['component']/record['name']
                    if 'sha256' in record:
                        h=record['sha256'];files.setdefault(h,{'source':str(src),'bytes':record['bytes'],'sha256':h});row['members'].append('archives/'+h)
                    else:
                        key=c['component']+'/'+record['name'];git_inputs[key]={'source':str(src),**record};row['members'].append('PENDING_GIT_SNAPSHOT:'+key)
            if not row['members']:row['members']=['REQUIRES_LOCAL_SHARED_PREBUILT_OR_GENERATED_DISPOSITION']
            mapping.append(row)
    print('BEGIN '+str(len(files))+' hashed archive inputs; '+str(sum(x['bytes'] for x in files.values()))+' bytes',flush=True)
    for i,(h,item) in enumerate(sorted(files.items()),1):
        src=Path(item['source']);assert src.is_file() and src.stat().st_size==item['bytes'];assert sha(src)==h
        target=DEST/'archives'/h
        assert target.is_file()
        assert target.stat().st_ino!=src.stat().st_ino;assert sha(target)==h;target.chmod(0o444)
        if i%25==0:print('ARCHIVE '+str(i)+'/'+str(len(files))+' copied and rehashed',flush=True)
    print('PASS all archive copies independent and hash-equal',flush=True)
    trees=[]
    for commit,inputs in sorted(distro.items()):
        root=Path(inputs['host_worktree']);assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==commit
        target=DEST/'distribution'/(commit+'.tar.gz')
        with tarfile.open(target,'w:gz',dereference=False) as tar:
            for name,h in sorted(inputs['source_files'].items()):
                p=root/name;assert not p.is_symlink() and sha(p)==h,name;tar.add(p,arcname=name,recursive=False)
            for name,link in sorted(inputs['source_symlinks'].items()):
                p=root/name;assert p.is_symlink() and os.readlink(p)==link,name;tar.add(p,arcname=name,recursive=False)
        # Independently read every member's bytes from the produced archive.
        with tarfile.open(target,'r:gz') as tar:
            members=tar.getmembers();assert len(members)==len(inputs['source_files'])+len(inputs['source_symlinks'])
            for member in members:
                if member.issym():assert inputs['source_symlinks'][member.name]==member.linkname
                else:assert hashlib.sha256(tar.extractfile(member).read()).hexdigest()==inputs['source_files'][member.name]
        target.chmod(0o444);trees.append({'distribution_commit':commit,'member':'distribution/'+target.name,'sha256':sha(target),'files':len(inputs['source_files']),'symlinks':len(inputs['source_symlinks'])})
        print('PASS distribution '+commit+' source files/patches/build scripts archive round-trip',flush=True)
    manifest={'schema':1,'scope':'Exact cached archive inputs and frozen distribution files/patches/build scripts; partial source custody, not publication clearance','archives':files,'component_members':mapping,'distribution_trees':trees,'pending_git_inputs':git_inputs,'publication_bundle_complete':False,'pending':['43 git roots and their recursive submodules','prebuilt rclone/ABL/tailscale corresponding source and notices','Nix/FEX inputs and source disposition','install-time shareware redistribution disposition','all component licence/notice review','independent external retrieval and backup custody']}
    raw=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode();h=hashlib.sha256(raw).hexdigest();(DEST/'manifest.json').write_bytes(raw);(DEST/'manifest.json').chmod(0o444)
    final=DEST.parent/('m7-archives-'+h);assert not final.exists();DEST.rename(final)
    for d in [final/'archives',final/'distribution',final]:d.chmod(0o555)
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_PARTIAL_ARCHIVE_CUSTODY','path':str(final),'manifest_sha256':h,'archive_count':len(files),'archive_bytes':sum(x['bytes'] for x in files.values()),'distribution_trees':trees,'pending_git_roots':len(git_inputs),'publication_bundle_complete':False}
    (O/'artifacts/result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);rc=0
finally:
    (O/'inner.rc').write_text(str(rc)+'\n');(O/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
