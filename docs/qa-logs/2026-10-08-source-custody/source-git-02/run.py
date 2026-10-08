from pathlib import Path
import datetime,gzip,hashlib,json,os,re,shutil,subprocess,sys,tarfile
O=Path(__file__).resolve().parent
BASE=Path('/workspace/artifacts/pixelelated-release-sources/m7-archives-a7022b76da76a9f6771bb7693d6f6e25854c6731db0750bb46dde29f14d49fce')
DEST=BASE.parent/'.staging-m7-git-01'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args])
(O/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n');rc=1
try:
    assert sha(BASE/'manifest.json')=='a7022b76da76a9f6771bb7693d6f6e25854c6731db0750bb46dde29f14d49fce'
    inputs=json.loads((BASE/'manifest.json').read_text())['pending_git_inputs']
    assert DEST.is_dir();(DEST/'trees').mkdir(exist_ok=True);(DEST/'metadata').mkdir(exist_ok=True);(DEST/'extra-cache-content').mkdir(exist_ok=True)
    scratch=O/'scratch';scratch.mkdir();records={};root_map={};edges=[];extra_content=[];observed_sources=set()
    todo=[]
    for name,item in inputs.items():
        p=Path(item['source']);assert git(p,'rev-parse','HEAD').decode().strip()==item['git_head']
        observed=git(p,'submodule','status','--recursive').decode().strip().splitlines()
        # Leading spaces on the first line were stripped by the original inventory.
        assert observed==item['submodules'],name
        root_map[name]=item['git_head'];todo.append((p,item['git_head']))
    while todo:
        path,commit=todo.pop()
        assert git(path,'rev-parse','HEAD').decode().strip()==commit
        assert git(path,'diff','--name-only','HEAD','--ignore-submodules=untracked').strip()==b'',str(path)
        if str(path) not in observed_sources:
            observed_sources.add(str(path))
            extras={}
            for rawname in git(path,'ls-files','--others','-z').split(b'\0'):
                if not rawname:continue
                rel=os.fsdecode(rawname).rstrip('/');p=path/rel
                assert not rel.startswith('/') and '..' not in Path(rel).parts
                candidates=[p]
                if p.is_dir() and not p.is_symlink():
                    candidates=[]
                    for base,dirs,names in os.walk(p,followlinks=False):
                        dirs[:]=[n for n in dirs if n!='.git']
                        for n in names+[n for n in dirs if (Path(base)/n).is_symlink()]:candidates.append(Path(base)/n)
                for f in candidates:
                    relative=str(f.relative_to(path))
                    if '.git' in Path(relative).parts:continue
                    if f.is_symlink():extras[relative]={'symlink':os.readlink(f)}
                    elif f.is_file():extras[relative]={'sha256':sha(f),'bytes':f.stat().st_size}
                    else:raise AssertionError(str(f))
            if extras:
                key=hashlib.sha256(str(path).encode()).hexdigest();archive=DEST/'extra-cache-content'/(key+'.tar.gz')
                assert not archive.exists()
                with tarfile.open(archive,'w:gz',dereference=False) as tar:
                    for relative in sorted(extras):tar.add(path/relative,arcname=relative,recursive=False)
                with tarfile.open(archive,'r:gz') as tar:
                    assert len(tar.getmembers())==len(extras)
                    for member in tar:
                        wanted=extras[member.name]
                        if 'symlink' in wanted:assert member.issym() and member.linkname==wanted['symlink']
                        else:assert hashlib.sha256(tar.extractfile(member).read()).hexdigest()==wanted['sha256']
                archive.chmod(0o444);extra_content.append({'source_cache':str(path),'tracked_commit':commit,'archive_member':'extra-cache-content/'+archive.name,'sha256':sha(archive),'files':extras,'disposition':'Preserved untracked/ignored source-cache content separately because scripts/extract copies the cache tree. Inclusion/use/licence requires review; never silently folded into the pinned Git tree.'})
                print('EXTRA_CACHE '+str(path)+' files='+str(len(extras)),flush=True)
        if commit in records:continue
        entries={};submods=[]
        for line in git(path,'ls-tree','-r','-z',commit).split(b'\0'):
            if not line:continue
            meta,name=line.split(b'\t',1);mode,kind,oid=meta.decode().split();name=os.fsdecode(name)
            assert not name.startswith('/') and '..' not in Path(name).parts
            if mode=='160000':
                assert kind=='commit';submods.append({'path':name,'commit':oid});todo.append((path/name,oid));edges.append({'parent_commit':commit,'path':name,'commit':oid})
            else:
                assert kind=='blob' and mode in ('100644','100755','120000');entries[name]={'mode':mode,'git_blob':oid}
        # A private bare view uses the source objects read-only. Highest-priority
        # attributes disable export-ignore/subst so archive bytes are exact blobs.
        view=scratch/'view.git';subprocess.run(['git','init','--bare','-q',str(view)],check=True)
        objects=git(path,'rev-parse','--path-format=absolute','--git-path','objects').decode().strip()
        (view/'objects/info/alternates').write_text(objects+'\n');(view/'info/attributes').write_text('* -export-ignore -export-subst\n')
        raw=scratch/'tree.tar';subprocess.run(['git','--git-dir',str(view),'archive','--format=tar','--output',str(raw),commit],check=True)
        dest=DEST/'trees'/(commit+'.tar.gz')
        prior_hash=sha(dest) if dest.exists() else None
        if dest.exists():dest.chmod(0o600)
        with raw.open('rb') as src,dest.open('wb') as out,gzip.GzipFile(filename='',fileobj=out,mode='wb',mtime=0,compresslevel=6) as z:shutil.copyfileobj(src,z,4*1024*1024)
        witnessed=set();lfs=[]
        with tarfile.open(dest,'r:gz') as archive:
            for member in archive:
                if member.isdir():continue
                assert member.name in entries,member.name;expected=entries[member.name]
                if member.issym():
                    assert expected['mode']=='120000';data=os.fsencode(member.linkname)
                    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
                else:
                    assert member.isfile() and expected['mode'] in ('100644','100755');assert bool(member.mode&0o111)==(expected['mode']=='100755')
                    h=hashlib.sha1(b'blob '+str(member.size).encode()+b'\0');stream=archive.extractfile(member);first=stream.read(4*1024*1024);h.update(first)
                    if first.startswith(b'version https://git-lfs.github.com/spec/v1\n'):lfs.append(member.name)
                    for chunk in iter(lambda:stream.read(4*1024*1024),b''):h.update(chunk)
                    blob=h.hexdigest()
                assert blob==expected['git_blob'],member.name;witnessed.add(member.name)
        assert witnessed==set(entries),(commit,len(witnessed),len(entries))
        if prior_hash:assert sha(dest)==prior_hash
        metadata={'commit':commit,'source_cache':str(path),'commit_object':git(path,'cat-file','commit',commit).decode(),'entries':entries,'submodules':submods,'lfs_pointer_paths':lfs,'archive_member':'trees/'+dest.name,'archive_sha256':sha(dest),'archive_bytes':dest.stat().st_size,'verified_blob_entries':len(witnessed),'claim':'Every tracked non-gitlink blob, mode and symlink matches the exact Git tree; submodule commits are separate mapped snapshots; no export-ignore/substitution omissions.'}
        meta=DEST/'metadata'/(commit+'.json')
        if meta.exists():meta.chmod(0o600)
        meta.write_text(json.dumps(metadata,sort_keys=True,indent=2)+'\n');meta.chmod(0o444);dest.chmod(0o444)
        records[commit]={'archive_member':metadata['archive_member'],'archive_sha256':metadata['archive_sha256'],'archive_bytes':metadata['archive_bytes'],'metadata_member':'metadata/'+meta.name,'metadata_sha256':sha(meta),'tracked_blobs':len(entries),'lfs_pointer_paths':lfs}
        raw.unlink();shutil.rmtree(view)
        print('SNAPSHOT '+str(len(records))+' '+commit+' blobs='+str(len(entries))+' queued='+str(len(todo)),flush=True)
    assert all(e['commit'] in records and e['parent_commit'] in records for e in edges)
    manifest={'schema':1,'scope':'Exact tracked Git source trees and recursive submodule snapshots; corresponding-source publication/licence review remains separate','archive_custody_manifest':'a7022b76da76a9f6771bb7693d6f6e25854c6731db0750bb46dde29f14d49fce','root_inputs':root_map,'extra_source_cache_content':extra_content,'submodule_edges':edges,'snapshots':records,'publication_bundle_complete':False,'pending':['LFS payload disposition if pointers exist','licence/notice review and prebuilt corresponding-source inputs','Nix/FEX and install-time shareware disposition','full source-member mapping and independent retrieval/backup custody']}
    raw=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode();h=hashlib.sha256(raw).hexdigest();(DEST/'manifest.json').write_bytes(raw);(DEST/'manifest.json').chmod(0o444);final=DEST.parent/('m7-git-'+h);assert not final.exists();DEST.rename(final)
    for d in [final/'trees',final/'metadata',final/'extra-cache-content',final]:d.chmod(0o555)
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_TRACKED_GIT_SNAPSHOT_CUSTODY','path':str(final),'manifest_sha256':h,'root_inputs':len(root_map),'extra_cache_archives':len(extra_content),'unique_snapshots':len(records),'submodule_edges':len(edges),'total_compressed_bytes':sum(v['archive_bytes'] for v in records.values()),'lfs_pointer_count':sum(len(v['lfs_pointer_paths']) for v in records.values()),'publication_bundle_complete':False}
    (O/'artifacts/result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);rc=0
finally:
    (O/'inner.rc').write_text(str(rc)+'\n');(O/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
