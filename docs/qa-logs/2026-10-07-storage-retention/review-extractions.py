from pathlib import Path
import datetime,gzip,hashlib,json,os,stat,sys,tarfile,time
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
def digest(stream):
 h=hashlib.sha256()
 for block in iter(lambda:stream.read(8*1024**2),b''):h.update(block)
 return h.hexdigest()
def filehash(p):
 with p.open('rb') as stream:return digest(stream)
def identity(p):
 s=p.lstat();return dict(device=s.st_dev,inode=s.st_ino,size=s.st_size,allocated_bytes=s.st_blocks*512,mtime_ns=s.st_mtime_ns,mode=s.st_mode,uid=s.st_uid,links=s.st_nlink)
rc=1
try:
 for p,h in json.loads((owner/'seal.json').read_text()).items():assert filehash(Path(p))==h,p
 rows=[]
 for number in ['03','05','06','07','11','12','13','14','15','16']:
  parent=Path('/workspace/tmp/pixelelated-m7-image-'+number)
  equality=parent/'artifacts/payload-equality.json';proof=json.loads(equality.read_text());assert proof['same_bytes'] is True
  assert (parent/'outer.rc').read_text().strip()=='0'
  bundle=Path('/workspace/artifacts/pixelelated-candidates/sha256')/proof['candidate_bundle'];manifest=json.loads((bundle/'manifest.json').read_text())
  gz=next(bundle.glob('*.img.gz'));tar=next(bundle.glob('*.tar'))
  for p in [gz,tar]:assert filehash(p)==manifest['files'][p.name]['sha256'],str(p)
  raw=parent/'candidate.img';system=parent/'SYSTEM';root=parent/'root';assert root.is_dir() and not root.is_symlink()
  raw_before=identity(raw);system_before=identity(system)
  raw_hash=filehash(raw)
  with gzip.open(gz,'rb') as f:assert digest(f)==raw_hash,str(raw)
  system_hash=filehash(system);assert system_hash==proof['image_SYSTEM_sha256']
  with tarfile.open(tar) as tf:
   names=[n for n in tf.getnames() if n.endswith('/target/SYSTEM')];assert len(names)==1
   with tf.extractfile(names[0]) as f:assert digest(f)==system_hash
  assert identity(raw)==raw_before and identity(system)==system_before
  entries=[];inodes={};pending=[root];device=root.stat().st_dev
  while pending:
   p=pending.pop();s=p.lstat();assert s.st_dev==device,str(p)
   row={'path':str(p),'identity':identity(p)}
   if stat.S_ISLNK(s.st_mode):row['target']=os.readlink(p)
   elif stat.S_ISDIR(s.st_mode):
    with os.scandir(p) as iterator:pending.extend(Path(e.path) for e in iterator)
   else:assert stat.S_ISREG(s.st_mode),str(p)
   entries.append(row);key=(s.st_dev,s.st_ino)
   if key not in inodes:inodes[key]={'bytes':s.st_blocks*512,'seen':0,'links':s.st_nlink,'directory':stat.S_ISDIR(s.st_mode)}
   inodes[key]['seen']+=1
  allocated=sum(i['bytes'] for i in inodes.values() if i['directory'] or i['seen']==i['links'])
  external_links=[k for k,v in inodes.items() if not v['directory'] and v['seen']!=v['links']]
  assert not external_links,(str(root),external_links[:5])
  entry_path=owner/'artifacts'/f'image-{number}-tree.json';entry_path.write_text(json.dumps(entries,indent=2)+'\n')
  records=[]
  for p in [equality,parent/'extract.py',parent/'run.sh',parent/'verify-inputs.py',parent/'harness.sha256',parent/'inner.rc',parent/'outer.rc',parent/'tool-wrapper.rc'] + ([parent/'console.log'] if (parent/'console.log').is_file() else []):
   records.append({'path':str(p),'sha256':filehash(p),'identity':identity(p)})
  row={'owner':str(parent),'bundle':str(bundle),'bundle_manifest_sha256':filehash(bundle/'manifest.json'),'files':[{'path':str(raw),'identity':raw_before,'sha256':raw_hash},{'path':str(system),'identity':system_before,'sha256':system_hash}],'extracted_root':str(root),'tree_manifest':str(entry_path),'tree_manifest_sha256':filehash(entry_path),'root_allocated_bytes':allocated,'allocated_bytes':allocated+raw_before['allocated_bytes']+system_before['allocated_bytes'],'records_retained':records,'owner_console_present':(parent/'console.log').is_file(),'original_run_path':(parent/'run.path').read_text().strip(),'scope':'raw and SYSTEM bytes match retained immutable firmware; root is a disposable extraction, inventoried by exact entry metadata, not claimed freshly byte-compared file by file.'}
  rows.append(row);print('PASS extraction inputs',number,round(row['allocated_bytes']/2**30,2),'GiB',flush=True)
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','extractions':rows,'allocated_bytes':sum(r['allocated_bytes'] for r in rows),'deletion_performed':False,'scope':'Recreation and metadata review only; active-use checks and retirement execution remain separate.'}
 (owner/'artifacts/result.json').write_text(json.dumps(result,indent=2)+'\n');rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
