from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys
owner=Path(__file__).parent
tree=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15')
root=Path('/workspace/tmp/pixelelated-m7-image-15/root')
build=tree/'build.pixelelated-GENERIC_X64.x86_64'
bundle=Path(sys.argv[1])
assert bundle.name=='43a698bcd7d570c63ebdd5db015e5302463f7ee4a15438fd9ef2359437be19da'
assert not (owner/'start').exists()
(owner/'start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
run=Path(os.environ['RASTERATOPS_BUILD_RUN'])
if not run.is_absolute():run=Path.cwd()/run
(owner/'run.path').write_text(str(run.resolve())+'\n')
def call(args,cwd=tree): subprocess.run([str(x) for x in args],cwd=cwd,check=True)
def verify():
 call(['sha256sum','-c',owner/'harness.sha256'])
 call(['python3','-I',owner/'verify-inputs.py',bundle])
 call([tree/'tools/rasteratops-candidate-store','verify',bundle])
shadow=root/'usr/cache/shadow';mode=None;rc=1
try:
 os.environ['ES_SRC']='/home/max/Development/emulationstation-next.worktrees/qa-integration'
 assert Path('/workspace/tmp/pixelelated-m7-image-15/outer.rc').read_text().strip()=='0'
 verify()
 mode=stat.S_IMODE(shadow.stat().st_mode)
 assert mode==0 and shadow.stat().st_uid==os.getuid() and not shadow.is_symlink()
 shadow.chmod(0o400)
 digest=hashlib.sha256(shadow.read_bytes()).hexdigest()
 receipt={'path':str(shadow),'original_mode':'0000','temporary_mode':'0400','content_sha256':digest,'scope':'owner-created extracted copy only; immutable SYSTEM, bundle and source unchanged'}
 (owner/'artifacts/extraction-read-permissions.json').write_text(json.dumps(receipt,indent=2)+'\n')
 call(['python3','-I',owner/'context-controls.py'])
 call(['python3','-I',owner/'check-controls.py','--scanner',owner/'scan-artifact.py','--patterns',owner/'secret-patterns','--output',owner/'artifacts/controls.json'])
 call(['python3','-I','-u',owner/'scan-artifact.py','--root',root,'--allowlist',owner/'allowlist.json','--patterns',owner/'secret-patterns','--output',owner/'artifacts/artifact-report.json'])
 call(['g++','-O2','-I',build/'build/pugixml-1.16/src',owner/'parse-theme.cpp',build/'build/pugixml-1.16/src/pugixml.cpp','-o',owner/'parse-theme'])
 call([owner/'parse-theme',root/'usr/share/themes/es-theme-art-book-next/theme.xml',owner/'artifacts/parsed-theme.xml'])
 call(['python3','-I',owner/'reconcile-locales.py','--root',root,'--es',os.environ['ES_SRC'],'--es-build',build/'build/emulationstation-bab4df649f48847cc43d21c77c058107ad902754','--tree',tree,'--parsed-theme',owner/'artifacts/parsed-theme.xml','--output',owner/'artifacts/localisation.json'])
 j=json.loads((owner/'artifacts/localisation.json').read_text())
 assert j['installed_tools_xml_valid'] and j['installed_tools_matches_corrected_source'] and not j['known_image_corrections']
 rc=0
finally:
 if mode is not None and stat.S_IMODE(shadow.stat().st_mode)==0o400:
  assert hashlib.sha256(shadow.read_bytes()).hexdigest()==digest
  shadow.chmod(mode)
  receipt['restored_mode']=format(stat.S_IMODE(shadow.stat().st_mode),'04o')
  (owner/'artifacts/extraction-read-permissions.json').write_text(json.dumps(receipt,indent=2)+'\n')
 try: verify()
 except Exception: rc=1;raise
 finally:(owner/'inner.rc').write_text(str(rc)+'\n')
print('PASS candidate15 whole-image sweep and exact installed localization')
