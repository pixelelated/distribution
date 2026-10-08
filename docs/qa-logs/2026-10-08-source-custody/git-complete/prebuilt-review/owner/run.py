from pathlib import Path
import base64,datetime,hashlib,json,os,subprocess,sys,tarfile
O=Path(__file__).resolve().parent;D=Path('/workspace/artifacts/pixelelated-release-sources/.staging-m7-prebuilt-01');rc=1
(O/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def api(path):return json.loads(subprocess.check_output(['gh','api',path]))
try:
 D.mkdir();(D/'archives').mkdir();(D/'metadata').mkdir();(D/'notices').mkdir();rows=[]
 for name,repo,tag,commit in [('rclone','rclone/rclone','v1.75.1','687d264b689b8c49a67e2e52a8a5e0caa01c04ce'),('tailscale','tailscale/tailscale','v1.98.8','05a91829316e055517a1e84f7b00016846ef4107'),('abl-packaging','ROCKNIX/abl','v1.1.9','0e755e154874f7e874919ab7e080935c1444df68')]:
  print('FETCH '+name+' '+commit,flush=True)
  tree=api(f'repos/{repo}/git/trees/{commit}?recursive=1');assert not tree['truncated'];expected={x['path']:x for x in tree['tree'] if x['type']=='blob'}
  archive=D/'archives'/(name+'-'+commit+'.tar.gz');url=f'https://codeload.github.com/{repo}/tar.gz/{commit}'
  subprocess.run(['curl','--fail','--location','--silent','--show-error','--connect-timeout','20','--max-time','240','--max-filesize','200000000','--output',str(archive),url],check=True)
  present=set();notices=[];transformed=[]
  with tarfile.open(archive) as tar:
   for member in tar:
    if member.isdir():continue
    rel=member.name.split('/',1)[1];assert rel in expected,rel;assert rel not in present;present.add(rel)
    if member.issym():data=os.fsencode(member.linkname);assert expected[rel]['mode']=='120000'
    else:data=tar.extractfile(member).read();assert bool(member.mode&0o111)==(expected[rel]['mode']=='100755')
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!=expected[rel]['sha']:transformed.append(rel)
    if (Path(rel).name.lower().startswith(('license','copying','notice','patents')) or rel in ('licenses/tailscale.md','.github/workflows/release-abl.yaml','README.md','go.mod','go.sum')):
     h=hashlib.sha256(data).hexdigest();n=D/'notices'/h
     if not n.exists():n.write_bytes(data)
     notices.append({'path':rel,'sha256':h,'member':'notices/'+h,'git_blob':blob})
  meta=D/'metadata'/(name+'-tree.json');meta.write_text(json.dumps(tree,sort_keys=True,indent=2)+'\n')
  row={'component':name,'repository':repo,'tag':tag,'commit':commit,'download_url':url,'archive_member':str(archive.relative_to(D)),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'tree_metadata_member':str(meta.relative_to(D)),'tree_metadata_sha256':sha(meta),'tracked_blob_count':len(expected),'archive_blob_count':len(present),'omitted_tracked_paths':sorted(set(expected)-present),'transformed_blob_paths':transformed,'gitlinks':[x for x in tree['tree'] if x['type']=='commit'],'notices':notices,'disposition':'Exact commit archive retained. This is source/notice evidence, not a reproducibility or complete licence claim.'}
  if name=='rclone':row['disposition']+=' Binary vcs.revision matches this commit but vcs.modified=true; original release modifications are not reconstructed.'
  if name=='tailscale':row['disposition']+=' Exact version tag observed; binary build metadata has no vcs.revision. Source-to-binary reproducibility is not asserted.'
  if name=='abl-packaging':
   release=api('repos/ROCKNIX/abl/releases/tags/v1.1.9');r=D/'metadata/abl-release.json';r.write_text(json.dumps(release,indent=2)+'\n');row['release_metadata_sha256']=sha(r);row['implementation_commit']='4588733123554b1f7bf935b04e494e4284894546';row['implementation_repository']='ROCKNIX/LinuxLoader';row['disposition']='HOLD: this archive is packaging/documentation, not ABL implementation source. Release records LinuxLoader4588733123554b1f7bf935b04e494e4284894546; current bot source read returned404. No third-party ABL licence granted by distribution recipe header.'
  rows.append(row);print('RETAINED '+name+' blobs='+str(len(present))+' omitted='+str(len(row['omitted_tracked_paths']))+' transformed='+str(len(transformed)),flush=True)
 manifest={'schema':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Public exact-version source/notice supplement for prebuilt inputs; outstanding vendor/provenance/backup/publication dispositions remain','components':rows,'publication_bundle_complete':False}
 p=D/'manifest.json';p.write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n');h=sha(p);final=D.parent/('m7-prebuilt-'+h);assert not final.exists();D.rename(final)
 for p in final.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
 final.chmod(0o555)
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_PREBUILT_SOURCE_NOTICE_RETENTION','custody':str(final),'manifest_sha256':h,'components':[{k:r[k] for k in ('component','commit','archive_blob_count','omitted_tracked_paths','transformed_blob_paths','disposition')} for r in rows],'publication_bundle_complete':False}
 (O/'artifacts/result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);rc=0
finally:
 (O/'inner.rc').write_text(str(rc)+'\n');(O/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
