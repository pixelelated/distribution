from ui import *
art=P/'artifacts'
restart('en_US')
walk('information',(ROOT/'docs/qa-logs/2026-10-09-build-identity/ui01-failed-harness/information.steps').read_text())
(art/'information-script.txt').write_text(guest('/usr/bin/rocknix-info | grep -v -i -E "key|pass|token|user|psk"')+'\n')
# Explicit folder creation is independent of linking. Use a new tiny QA root.
pre={str(x.relative_to(P/'cloud/data')):hashlib.sha256(x.read_bytes()).hexdigest() for x in (P/'cloud/data').rglob('*') if x.is_file()}
conf=guest('cat /storage/.config/cloud_sync.conf')+'\n'
guest('. /etc/profile >/dev/null 2>&1; cloud_setup --set-saves-remote /Manual-QA/Saves; cloud_setup --set-settings-remote /Manual-QA/Backups; cloud_setup --set-content-remote /Manual-QA/Content')
assert not (P/'cloud/data/Manual-QA').exists()
(art/'manual-before.json').write_text(guest('/usr/bin/cloud_setup --validate-folders saves,settings,roms,bios,media ui19e-before')+'\n')
(art/'manual-create.log').write_text(guest('/usr/bin/cloud_setup --seed-folders saves,settings,roms,bios,media',120)+'\n')
(art/'manual-after.json').write_text(guest('/usr/bin/cloud_setup --validate-folders saves,settings,roms,bios,media ui19e-after')+'\n')
expected=['Saves','Saves/savefiles','Saves/savestates','Saves/screenshots','Backups','Content/ROMs','Content/BIOS']
assert all((P/'cloud/data/Manual-QA'/n).is_dir() for n in expected)
assert all((P/'cloud/data'/n).is_file() and hashlib.sha256((P/'cloud/data'/n).read_bytes()).hexdigest()==h for n,h in pre.items())
python("from pathlib import Path\np=Path('/storage/.config/cloud_sync.conf');p.write_text("+repr(conf)+")")
(art/'manual-creation-preservation.json').write_text(json.dumps({'folders':expected,'pointer_selection_alone_created_nothing':True,'prior_cloud_payload_hashes':pre,'prior_payloads_preserved':True},indent=2)+'\n')
print('PASS INFORMATION walk and explicit manual folder creation/preservation; frame review required',flush=True)
