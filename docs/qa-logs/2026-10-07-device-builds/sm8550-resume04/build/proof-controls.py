"""Exercise the retained failing helper and corrected helper in the real container."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
owner=Path(__file__).resolve().parent
j=json.loads((owner/'inputs.json').read_text())
failed=owner/'original-verifier.py';fixed=owner/'verify-fex.py'
with (owner/'artifacts/original-verifier.log').open('x') as log:
    original=subprocess.run([sys.executable,'-I',str(failed)],stdout=log,stderr=subprocess.STDOUT)
text=(owner/'artifacts/original-verifier.log').read_text()
missing=Path(j['host_worktree'])/j['build_root']/'build'/('fex-emu-'+j['fex_commit'])/'.aarch64-rocknix-linux-gnu/guest-libs/build.ninja'
assert original.returncode==1 and 'FileNotFoundError' in text and str(missing) in text,text
assert not (owner/'artifacts/fex-package.json').exists()
with (owner/'artifacts/corrected-verifier.log').open('x') as log:
    corrected=subprocess.run([sys.executable,'-I',str(fixed)],stdout=log,stderr=subprocess.STDOUT)
assert corrected.returncode==0,(owner/'artifacts/corrected-verifier.log').read_text()
proof=json.loads((owner/'artifacts/fex-package.json').read_text())
assert proof['result']=='PASS' and len(proof['files'])==14
receipt={'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','original_exit':original.returncode,'original_failure':'Expected FileNotFoundError at guest-libs/build.ninja','corrected_exit':corrected.returncode,'installed_elf_count':len(proof['files']),'actual_generated_directories':['Guest','Guest_32'],'scope':'Exact old-helper failing control and corrected actual installed-package proof; no source or package rebuild'}
with (owner/'artifacts/proof-controls.json').open('x') as out:json.dump(receipt,out,indent=2);out.write('\n')
print(json.dumps(receipt),flush=True)
