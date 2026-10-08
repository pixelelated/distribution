from pathlib import Path
import hashlib,json,subprocess
R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17')
B=Path('/workspace/tmp/pixelelated-m7-cf10-17');O=B/'guest01'
O.mkdir(parents=True);B.chmod(0o700);O.chmod(0o700)
old=(R/'docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/guest01/create.py').read_text()
s=old.replace('import pathlib,hashlib,json,subprocess,socket,time,gzip,shutil,os','import pathlib,hashlib,json,subprocess,socket,time,gzip,shutil,os,sys')
s=s.replace('/workspace/tmp/pixelelated-524-path-refusal/guest01',str(O)).replace('/workspace/repos/rocknix.worktrees/conflict-resolution',str(R))
a=s.index("IMG=pathlib.Path(");z=s.index('started=time.monotonic()',a)
s=s[:a]+'''bundle=pathlib.Path(sys.argv[1]).resolve(strict=True)
subprocess.run([str(R/'tools/rasteratops-candidate-store'),'verify',str(bundle)],check=True)
manifest=json.loads((bundle/'manifest.json').read_text())
assert manifest['inputs']['distribution_commit']=='3756fde50e52b71b101a892a5b2862b708ad7b32'
assert manifest['inputs']['emulationstation_commit']=='1d76b3da7da75794066df1c089931b890304da7a'
name='pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz'
IMG=bundle/name
'''+s[z:]
s=s.replace('10220','10230').replace('5940','5950').replace('pix524','pix508-cf10-17').replace("'40'","'50'").replace('display\':40','display\':50')
s=s.replace("assert digest=='74e57ad8957b1c719c18db098d5713577a952af8802524658d0ada7dee1b6b12'","assert digest==manifest['files'][name]['sha256']")
s=s.replace('pixelelated-524-qa','pixelelated-508-cf10-qa').replace("'--res','640x480'","'--gl','none','--res','640x480'").replace('52:54:00:52:52:24','52:54:00:52:05:17')
s=s.replace("'owner':'root PL-003 exclusive'","'owner':'root CF10 exclusive'").replace("'purpose':'#524 path-refusal UI proof followed by auditor L-03 inspection'","'purpose':'#508 assembled-image clean/public configuration adoption; no source overlays'")
s=s.replace("subprocess.run(ssh+['ip route", "assert '3756fde50e52b71b101a892a5b2862b708ad7b32' in ready.stdout,ready.stdout\nsubprocess.run(ssh+['ip route")
# The source and expected assembled file mapping is independently read after SSH.
pos=s.index("record={'image':")
verify='''installed=json.loads((R/'docs/qa-logs/2026-10-08-m7-audit-resolutions/PL-003/stage01/install-manifest.json').read_text())
proof={}
for entry in installed['installed_files']:
 dest=entry['destination'];local=R/pathlib.Path(entry['source']).relative_to('/workspace/repos/rocknix')
 expected=hashlib.sha256(local.read_bytes()).hexdigest()
 got=subprocess.check_output(ssh+['sha256sum '+dest],text=True).split()[0]
 assert got==expected,(dest,got,expected);proof[dest]=got
for rel in ['usr/bin/emulationstation','usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo','usr/bin/duckstation_screenshot_path','usr/bin/start_duckstation.sh','usr/lib/libcom_err.so.2']:
 local=R/'build.pixelelated-GENERIC_X64.x86_64/image/system'/rel
 expected=hashlib.sha256(local.read_bytes()).hexdigest()
 got=subprocess.check_output(ssh+['sha256sum /'+rel],text=True).split()[0]
 assert got==expected,(rel,got,expected);proof['/'+rel]=got
subprocess.run(ssh+['test ! -e /usr/bin/cloud_migrate_layout && test "$(stat -c %a /usr/bin/duckstation-sa)" = 755'],check=True)
(O/'installed-inclusion.json').write_text(json.dumps({'sha256':proof,'retired_migration_absent':True,'duckstation_mode':'755','source_overlays':False},indent=2)+'\\n')
'''
s=s[:pos]+verify+s[pos:]
compile(s,str(O/'create.py'),'exec');(O/'create.py').write_text(s)
run=f'''#!/bin/bash
set -euo pipefail
cd {R}
test ! -e {O}/qa.start
sha256sum -c {O}/harness.sha256
printf '%s\\n' "$PWD/${{RASTERATOPS_BUILD_RUN:?use watch-build}}" > {O}/run.path
date -u +%Y-%m-%dT%H:%M:%SZ > {O}/qa.start
trap 'result=$?; printf "%s\\n" "$result" > {O}/inner.rc' EXIT
python3 -I -u {O}/create.py "${{1:?immutable bundle required}}"
'''
outer=f'''#!/bin/bash
set -uo pipefail
{O}/run.sh "${{1:?immutable bundle required}}"
result=$?
printf '%s\\n' "$result" > {O}/outer.rc
exit "$result"
'''
for name,text in [('run.sh',run),('outer.sh',outer)]:
 (O/name).write_text(text);(O/name).chmod(0o500);subprocess.run(['bash','-n',str(O/name)],check=True)
(O/'create.py').chmod(0o400)
(O/'harness.sha256').write_text(''.join(hashlib.sha256((O/n).read_bytes()).hexdigest()+'  '+str(O/n)+'\n' for n in ['create.py','run.sh','outer.sh']))
(B/'prepared.json').write_text(json.dumps({'status':'prepared, not executed','stage':'fresh immutable-image guest and installed bytes only; CF10 actions are a separate subsequent owner','image_required':True,'ports':[10230,5950],'memory_gib':8,'product_source_overlays':False},indent=2)+'\n')
print('Prepared CF10 fresh-guest owner; no VM started')
