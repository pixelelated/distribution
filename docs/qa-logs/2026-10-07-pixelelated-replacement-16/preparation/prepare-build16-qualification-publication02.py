from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,shutil,subprocess
repo=Path.cwd();primary=Path('/workspace/repos/rocknix');old=Path('/workspace/tmp/pixelelated-m7-build16-preparation-publication-02')
owner=Path('/workspace/tmp/pixelelated-m7-build16-qualification-publication-02')
assert not owner.exists();owner.mkdir(mode=0o700);(owner/'tmp').mkdir(mode=0o700);(owner/'artifacts').mkdir(mode=0o700)
text=(old/'publish.py').read_text()
text=text.replace('c9449570984365491c5197edf5cbf0030e818f67','0d70d093bad2281123306943d61bfec6222b13eb')
text=text.replace('ee014909137e03706e0b3020b8396be589aaa705','39a5c96980525341e20c1ea8c64b1e7e864982b4')
text=text.replace("paths = [", "paths = ['tools/pixelelated-vm-cloud-boundaries', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/09-remaining-evidence.md', ",1)
text=text.replace("p.startswith(('docs/', '.github/sessions/'))", "(p.startswith(('docs/', '.github/sessions/')) or p == 'tools/pixelelated-vm-cloud-boundaries')")
text=text.replace('Documentation-only approved two-file retirement receipts, candidate16 freeze, active independent cache copy and current M7 order. Product inputs frozen separately; no VM or RC claim. No new deletion scope.',
 'Candidate16 build/payload/sweep/inventory and installed matrix receipts; corrected collision observer with focused installed predecessor control; current serial VM continuation. Product image unchanged, no RC or device-readiness claim.')
ast.parse(text);(owner/'publish.py').write_text(text)
(owner/'message.txt').write_text('qa: verify candidate16 artifacts and collision refusal\n\nRetain the successful build and immutable payload checks, image scan and\nsource inventory. Preserve the original 84-pass/1-fail matrix and strengthen\nthe collision observer to require refusal before any writes. Record the\nfocused installed proof and continuing historical/UI qualification.\n\nRefs #383, #471, #479, #482, #484, #485.\n')
changed=subprocess.check_output(['git','diff','--name-only','-z'],text=True).split('\0')
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],text=True).split('\0')
files=[]
for name in sorted(set(changed+untracked)):
 if not name:continue
 assert name.startswith(('docs/','.github/sessions/')) or name=='tools/pixelelated-vm-cloud-boundaries',name
 p=repo/name
 if p.is_file():files.append(p)
files += [owner/'publish.py',owner/'message.txt']
(owner/'seal.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
print(owner,len(files),'sealed files')
