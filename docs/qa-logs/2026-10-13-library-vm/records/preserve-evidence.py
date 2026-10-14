from pathlib import Path
import shutil,json,hashlib,gzip,struct,datetime
r=Path(__file__).parent;d=Path('/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-13-library-vm');d.mkdir(exist_ok=True)
def copy(p,q):
 q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert p.read_bytes()==q.read_bytes()
# Original small result records, drivers, logs, steps and manifests. No VM disk/key,
# installed executable, credential file or generated ROM/save payload is copied.
for p in r.iterdir():
 if p.is_file() and (p.suffix=='.py' or p.name.endswith('-result.json') or p.name in ['original-identities.txt','original-identities1280.txt']):copy(p,d/'records'/p.name)
for name in ['rvz-results','steam-results','steam-corrected-results','dolphin-results','dolphin-mounted-results','dolphin-followup-results']:
 for p in (r/name).rglob('*'):
  if not p.is_file() or p.is_symlink():continue
  rel=p.relative_to(r)
  if p.suffix=='.tar':
   q=d/'results'/Path(str(rel)+'.gz');q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(gzip.compress(p.read_bytes(),mtime=0));assert gzip.decompress(q.read_bytes())==p.read_bytes()
  else:copy(p,d/'results'/rel)
for p in r.glob('capability-*'):
 if p.is_dir() and 'owner' not in p.name:
  for f in p.rglob('*'):
   if f.is_file() and f.suffix in ('.json','.steps','.txt') and f.stat().st_size<1024*1024:copy(f,d/'results'/f.relative_to(r))
for p in r.glob('wifi-*'):
 if p.is_dir():
  for f in p.rglob('*'):
   if f.is_file() and f.suffix in ('.json','.steps','.txt') and f.stat().st_size<1024*1024:copy(f,d/'results'/f.relative_to(r))
for p in (r/'records').glob('*.json'):
 if not p.name.startswith('milestone'):copy(p,d/'records/source'/p.name)
# Explicit visual review inventory. A reviewed defective frame is retained as
# rejected evidence, never as the accepted replacement for its later copy fix.
selected=[]
def add(dirname,branch,verdict='accepted',note=''):
 matches=list((r/dirname/branch).glob('*.png'));assert len(matches)==1,(dirname,branch,matches)
 selected.append((matches[0],verdict,note))
for size in ['640','1280']:
 for lang in ['en_US','fr_FR']:
  for mode in ['gc-auto','gc-retro-override','dc-auto','dc-standalone-override','dc-retro-override']:
   # All listed advanced frames were explicitly reviewed across this continuation
   # and its preceding checkpoint, except the already reviewed auto-dialog subset.
   dirname=f'capability-{mode}-{lang}-{size}-03'
   branch='support-dialog' if mode=='gc-auto' else 'advanced-options'
   verdict='rejected-copy' if size=='1280' and lang=='fr_FR' and 'retro-override' in mode else 'accepted'
   add(dirname,branch,verdict,'Inherited French per-game description wraps; replacement09afa remains unqualified.' if verdict!='accepted' else '')
for name in ['capability-global-en640','capability-global-fr640','capability-global-fr1280']:
 for branch in ['global-autosave','global-manager']:
  add(name,branch,'rejected-copy' if '-fr' in name else 'accepted','French replacement09afa catalog/frame qualification pending.' if '-fr' in name else '')
add('capability-global-en1280','global-manager')
for branch in ['auto-standalone','retroarch-after']:add('capability-selection-fr640',branch)
add('capability-collection-gc-fr1280','collection')
for branch in ['open','systems','gamecube','support-dialog','retroarch-selection','auto-restored','returned']:add('capability-system-fr1280',branch)
# Reviewed French prompt proof at larger resolution and initial small layout.
for p in [r/'wifi-fr1280-bb9e-branches/refresh/01-pending.png',r/'wifi-fr1280-bb9e-branches/failure/02-complete.png']:
 assert p.is_file();selected.append((p,'accepted','Corrected French footer hints.'))
contract=json.loads((r/'records/candidate.json').read_text());index={'scope':'Selected reviewed installed-overlay frames; no full image or engine qualification','source':contract,'frames':[]}
for p,verdict,note in selected:
 rel=p.relative_to(r);q=d/'frames'/rel;copy(p,q);raw=q.read_bytes();width,height=struct.unpack('>II',raw[16:24]);language='fr_FR' if '-fr' in str(rel) else 'en_US'
 index['frames'].append({'path':str(q.relative_to(d)),'flow':str(rel.parent),'locale':language,'width':width,'height':height,'sha256':hashlib.sha256(raw).hexdigest(),'reviewed':True,'verdict':verdict,'note':note,'es_source':contract['source'],'es_binary':contract['sha256'],'catalog_sha256':contract['catalogs']['fr' if language=='fr_FR' else 'en_GB']})
(d/'frame-index.json').write_text(json.dumps(index,indent=2)+'\n')
print('Preserved',len(index['frames']),'reviewed frames; lifecycle remains ACTIVE, final packet not yet sealed.')
