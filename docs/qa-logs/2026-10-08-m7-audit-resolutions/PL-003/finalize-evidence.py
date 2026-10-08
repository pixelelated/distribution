from pathlib import Path
import hashlib,json,shutil,struct,datetime
B=Path('/workspace/tmp/pixelelated-524-path-refusal');D=Path('/workspace/repos/rocknix.worktrees/conflict-resolution/docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003')
# Only run after final owner completion has been independently verified.
final=json.loads((B/'matrix05/verified-completion.json').read_text());assert set(final['channels'].values())=={0}
accepted=[]
for owner,wanted in [('matrix02',5),('matrix04',2),('matrix05',37)]:
 rows=json.loads((B/owner/'results.json').read_text());assert len(rows)==wanted,(owner,len(rows),wanted)
 for row in rows:
  row=dict(row);row['owner']=owner
  if row['case']=='blank':row['proof_kind']='frontend empty field refusal'
  accepted.append(row)
assert len(accepted)==44
cases={'invalid-components','blank','root','invalid-name','invalid-characters','bucket','unreachable','busy','timeout','settings-write','unknown'}
assert {(x['locale'],x['resolution'],x['case']) for x in accepted}=={(l,r,c) for l in ['en_US','fr_FR'] for r in ['640x480','1280x800'] for c in cases}
# Retain scripts, lifecycle, raw bounded output, typed input, failed attempts and
# reviewed visual frames. No disk, binary, archive, key, or synthetic credential file.
owners=['restage01','matrix01','matrix02','matrix03','matrix04','matrix05','walk-en640-enter','walk-en640-invalid','walk-en640-reenter','walk-en640-reenter02','walk-en640-invalid02','walk-en640-reenter03','walk-en640-invalid03']
for owner in owners:
 for src in (B/owner).rglob('*'):
  if not src.is_file():continue
  rel=src.relative_to(B/owner)
  if rel.parts[0] in ['tools','.build-runs']:continue
  if src.suffix not in ['.json','.py','.sh','.log','.txt','.rc','.png']:continue
  if src.name.startswith('watch-build-submit'):continue
  dst=D/owner/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 # Actual watcher association follows recorded console root, not assumed cwd.
 line=(B/owner/'console.log').read_text().splitlines()[0]
 prefix='watch-build: recording in '
 if line.startswith(prefix):
  run=Path(line[len(prefix):]);assert (run/'build.rc').exists()
  dest=D/owner/'watcher';dest.mkdir(exist_ok=True)
  for n in ['build.rc','build.status','build.pid','command.pid','watcher.pid','watcher.err']:
   if (run/n).is_file():shutil.copy2(run/n,dest/n)
  (dest/'original-path.txt').write_text(str(run)+'\n')
for name in ['installed-readback.txt','installed-readback.json']:
 shutil.copy2(B/'stage01'/name,D/'stage01'/name)
for row in accepted:
 src=B/row['owner']/row['frame'];assert hashlib.sha256(src.read_bytes()).hexdigest()==row['frame_sha256']
 size=struct.unpack('>II',src.read_bytes()[16:24]);assert f'{size[0]}x{size[1]}'==row['resolution']
 case=src.parent.parent;assert (case/'before.txt').read_bytes()==(case/'after.txt').read_bytes()
 row['frame']=row['owner']+'/'+row['frame'];row['flow_id']='CF05';row['source_commit']='1d76b3da7da75794066df1c089931b890304da7a'
 row['expected']='Bounded localized refusal; selected paths/config and synthetic file bytes remain unchanged.'
 row['review_status']='pending final root visual review'
(D/'evidence-index.json').write_text(json.dumps({'schema_version':1,'canonical_reference':'docs/pixelelated/cloud-folder-flow-review.md#implemented-flow-and-visual-proof','es_commit':'1d76b3da7da75794066df1c089931b890304da7a','kind':'source-overlay UI qualification; not assembled firmware','cases':accepted},indent=2)+'\n')
manifest=[{'path':str(p.relative_to(D)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='sha256.json']
(D/'sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS index structure/44 combinations, frame hashes and dimensions, unchanged per-case state; semantic review not inferred.')
