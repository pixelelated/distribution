from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('/workspace/repos/rocknix.worktrees/conflict-resolution');D=R/'docs/qa-logs/2026-10-08-source-custody/git-complete';P=R/'docs/qa-logs/2026-10-08-final-inventory/supplement/artifacts';basis=json.loads((P/'missing-license-notices.json').read_text());B=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/build');N=D/'notice-basis';N.mkdir()
labels={
'enet':('MIT','Root LICENSE carries the permission and notice terms.'),
'freej2me-lr':('GPL-3.0-or-later; bundled works require separate terms','Source Java headers explicitly allow version3 or later. README identifies JLayer, libsdl4j, ASM and libretro; retain their individual notices and confirm included outputs.'),
'harfbuzz-icu':('MIT-old; per-directory exceptions','Root COPYING names Old MIT and directs readers to per-directory COPYING. test/COPYING applies OFL1.1 to many test fonts, not a blanket licence for the library. Source is shared with harfbuzz.'),
'libretro-database':('CC-BY-SA-4.0','Root LICENSE carries Creative Commons Attribution ShareAlike4.0. Attribute the included databases and preserve notices.'),
'libspeexdsp':('BSD-3-Clause','COPYING supplies source/binary notice conditions and non-endorsement clause.'),
'libxmp-lite':('MIT','Full permission and notice text is in README, missed by the earlier two-level filename collector.'),
'openbor':('BSD-3-Clause for recorded root/engine/tools notices','Root, engine and tools LICENSE files have different copyright holders; preserve each rather than only a generic template.'),
'opusfile':('BSD-3-Clause','COPYING supplies Xiph notices and three conditions; applies also to ARM profiles.'),
'wildmidi':('LGPL-3.0-or-later library; GPL-3.0-or-later player','COPYING splits library/player; source header explicitly permits later versions. Map installed output before applying the relevant branch.'),
'zerotier-one':('MPL-2.0 core; ext/ and nonfree/ separate','LICENSE.txt excludes ext/ and nonfree/ from its blanket MPL statement. make-linux.mk includes nonfree controller objects only under ZT_NONFREE=1 (also set by ZT_CONTROLLER=1). Directory presence alone does not show they shipped; actual build/output disposition remains.'),
'glsl-shaders':('LGPL-3.0 root licence text; per-shader review open','The root file supplies LGPLv3 text. Do not flatten per-shader copyright/exception headers into one aggregate label.'),
'common-shaders':(None,'No top-level notice candidate. Review exact included shader headers and collection provenance.'),
'retropie-shaders':(None,'No top-level notice candidate. Review exact included shader headers and collection provenance.'),
'slang-shaders':(None,'No top-level notice candidate. Review exact included shader headers and collection provenance.'),
'rclone':('MIT root; dependency terms separate','Exact upstream COPYING retained with pinned source. Binary names same commit, with vcs.modified=true.244 embedded module entries are retained; full dependency notices/release modification disposition remain.'),
 'tailscale':('BSD-3-Clause root; dependency terms separate','Exact version LICENSE and licenses/tailscale.md retained. Embedded module inventories contain58 CLI and72 daemon entries; no embedded vcs.revision. Verify bundled dependency notice coverage before publication.'),
'rocknix-abl':(None,'HOLD: release identifies LinuxLoader4588733123554b1f7bf935b04e494e4284894546, but bot source read returned404. Public abl tag contains packaging/docs only. No implementation licence/source disposition inferred from recipe GPL header.')}
records=[]
for name,(label,note) in sorted(labels.items()):
 rows=[r for r in basis if r['component']==name];assert rows;notices={}
 for row in rows:
  for p,v in row['notice_candidates'].items():
   src=P/v['retained_notice'];assert hashlib.sha256(src.read_bytes()).hexdigest()==v['sha256'];notices[v['sha256']]={'observed_source':p,'sha256':v['sha256'],'retained_in_existing_packet':str(src.relative_to(R))}
 for rel in {'libxmp-lite':['README'],'freej2me-lr':['README.md','src/mmpp/media/Vibration.java'],'wildmidi':['COPYING','src/wildmidi_lib.c','docs/license/GPLv3.txt','docs/license/LGPLv3.txt'],'zerotier-one':['make-linux.mk','objects.mk','objects-nonfree.mk']}.get(name,[]):
  src=next(B.glob(name+'-*'))/rel;raw=src.read_bytes();h=hashlib.sha256(raw).hexdigest();target=N/h;target.write_bytes(raw);notices[h]={'observed_source':str(src),'sha256':h,'retained_in_completion_packet':str(target.relative_to(R))}
 if name in ('rclone','tailscale','rocknix-abl'):
  m=json.loads((D/'prebuilt-review/custody-manifest.json').read_text());key='abl-packaging' if name=='rocknix-abl' else name;row=next(c for c in m['components'] if c['component']==key)
  for n in row['notices']:notices[n['sha256']]={'upstream_path':n['path'],'commit':row['commit'],'repository':row['repository'],'custody_manifest':'aeef83ae3a4de7ebaca3816508e804bf935e87285efdcff6226cb52bd2fc4827','member':n['member'],'sha256':n['sha256']}
 records.append({'component':name,'profiles':sorted(set(r['profile'] for r in rows)),'observed_licence_basis':label,'scope_and_remaining_work':note,'notice_evidence':list(notices.values()),'release_disposition':'OPEN: integrate scoped licence and exact notices into final release materials; this basis review is not full component/vendor/source/backup clearance.'})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Source-cited licence basis for17 missing recipe metadata fields; no package recipe or firmware mutation. Presence of a root licence does not settle all vendored or data-file terms.','components':records,'components_with_identified_root_or_scoped_basis':sum(r['observed_licence_basis'] is not None for r in records),'components_without_aggregate_basis':[r['component'] for r in records if r['observed_licence_basis'] is None],'publication_bundle_complete':False};(D/'licence-basis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='components'},indent=2))
shutil.copy2('/tmp/m7-license-basis.py',D/'collect-licence-basis.py')
