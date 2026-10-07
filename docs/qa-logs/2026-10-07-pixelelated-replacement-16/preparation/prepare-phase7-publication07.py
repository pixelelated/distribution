from pathlib import Path
import ast
import hashlib
import json
import subprocess

repo=Path.cwd()
old=Path('/workspace/tmp/pixelelated-m7-build16-recovery-publication-06')
owner=Path('/workspace/tmp/pixelelated-m7-phase7-publication-07')
assert not owner.exists()
assert (repo/'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/05-punch-list.md').read_text().count('  outcome: resolved')==8
owner.mkdir(mode=0o700)
for name in ['tmp','artifacts']:(owner/name).mkdir(mode=0o700)
s=(old/'publish.py').read_text()
s=s.replace('3af6d5192bc4905f4b814faa7de142f795e387c0','9b4e91b832489a5852950c77cf5fc8eef0c49691')
s=s.replace('7ce442d53aea3d7998b9e939443ecc9f771b240c','32fb5a613df15df5bc30ec7dddcdf2adf3dfbc82')
s=s.replace("'audit-pre-issue'","'audit-resolution'").replace("'--phase', 'pre-issue'","'--phase', 'resolution'")
needle="    paths = ["
assert needle in s
s=s.replace(needle,"    paths = ['docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/10-closure-reconciliation.md', ",1)
start=s.index("scope='Candidate16 EN/FR recovery");end=s.index("')",start)
s=s[:start]+"scope='Candidate16 full qualification and eight resolved audit findings: QA20 defaults/actual RC2 upgrade, cloud318, exact installed legacy content and bilingual routing, original-state dispositions, dependency custody and source readback. Product unchanged. Tracker closure and device capacity/builds follow; no RC designation or release publication."+s[end:]
ast.parse(s);(owner/'publish.py').write_text(s)
(owner/'message.txt').write_text('qa: complete candidate16 software qualification and audit\n\nRetain final default/actual ROCKNIX upgrade and WebDAV/SFTP/S3 results,\ninstalled legacy-content restores and bilingual folder-routing frames.\nRecord all eight command-backed audit resolutions and existing-state\ndispositions. Preserve failed runs and remaining device/publication gates.\n\nRefs #471, #467, #468, #478, #479, #361, #386, #327, #383, #409, #487, #488.\n')
names=set(subprocess.check_output(['git','diff','--name-only','-z'],text=True).split('\0'))
names.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],text=True).split('\0'))
files=[]
for name in sorted(names-{''}):
    assert name.startswith(('docs/','.github/sessions/')),name
    p=repo/name
    if p.is_file():files.append(p)
files += [owner/'publish.py',owner/'message.txt']
(owner/'seal.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
print(owner,len(files),'sealed inputs; final accepted evidence ready for normal guarded publication')
