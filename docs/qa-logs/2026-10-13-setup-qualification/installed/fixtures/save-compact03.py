from pathlib import Path
import json,hashlib,shutil,struct,datetime,re
r=Path(__file__).parent;dst=Path('/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-13-setup-qualification/installed')
dst.mkdir(exist_ok=True)
def copy(src,rel):
 target=dst/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
for p in r.glob('*.py'):copy(p,Path('fixtures')/p.name)
for p in r.glob('fake-rclone*'):
 if p.is_file():copy(p,Path('fixtures')/p.name)
copy(r/'browser-fail','fixtures/browser-fail')
for name in ['records/candidate.json','records/image-size.json','original-identities.txt','original-identities1280.txt','provision-result.json','provision1280-result.json','ready-640x480.json','ready-1280x800.json','qemu-640x480.json','qemu-1280x800.json','terminal-children-checkpoint.json','browser-branches-batch-result.json','notice-640-batch-result.json','notice-640-batch02-result.json','finish-small-result.json']:
 p=r/name
 if p.exists():copy(p,Path('records')/name.replace('/','--'))
for pattern in ['*/result.json','*/*/result.json','recent-en640/*.json','*/*/calls.jsonl','*/calls.jsonl','*/events.txt','*/events.jsonl']:
 for p in r.glob(pattern):
  if any(x.endswith('-owner') or x in ['vm','records','.build-runs'] for x in p.relative_to(r).parts):continue
  copy(p,Path('results')/p.relative_to(r))
for owner in (p.parent for p in r.glob('*/launcher-result.json')):
 if not (owner/'launcher-result.json').exists():continue
 for name in ['launcher-start.json','launcher-submission.json','launcher-pid.json','launcher-result.json','tool-wrapper.rc','console.log']:
  p=owner/name
  if p.exists():copy(p,Path('owners')/owner.name/name)
 text=(owner/'console.log').read_text(errors='replace') if (owner/'console.log').exists() else ''
 m=re.search(r'watch-build: recording in (\S+)',text)
 if m:
  run=Path(m.group(1))
  for name in ['runner-result.json','build.rc','build.status','build.pid','command.pid','watcher.pid','watcher.err','build.start']:
   p=run/name
   if p.exists():copy(p,Path('owners')/owner.name/'run'/name)
frames=json.loads((r/'reviewed-frames02.json').read_text());index=[]
for f in frames:
 p=r/f['path'];data=p.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n';width,height=struct.unpack('>II',data[16:24]);rel=Path('frames')/f['path'];copy(p,rel)
 index.append(dict(f,path=str(rel),sha256=hashlib.sha256(data).hexdigest(),width=width,height=height,reviewed=True,es_source='a7dcdbb38009d8d2a81c7c2b4bc1d8c2d0d38a20',es_binary='f6fd61b7bea859467f1a3b0e1f890c975bfef9aaafd1866e727752727de013b3',phone_source='95c626f8df07faef522683a857e48e31f85a58c6f738bcde24707574dc24d293'))
(dst/'frame-index.json').write_text(json.dumps({'scope':'Selected reviewed candidate frames; synthetic inputs; no full image promotion','frames':index},indent=2)+'\n')
(dst/'checkpoint.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lifecycle_complete':(r/'vm-result.json').exists(),'copied_files':sum(p.is_file() for p in dst.rglob('*'))},indent=2)+'\n')
print('saved',sum(p.is_file() for p in dst.rglob('*')),'compact artifacts,',len(index),'reviewed frames')
