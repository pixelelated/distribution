from pathlib import Path
import hashlib,json,sys
p=Path('/workspace/tmp/pixelelated-m7-qa-14/pair/vm-a.qcow2');out=Path(__file__).parent/'artifacts/backing.json'
h=hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
if sys.argv[1]=='before':
 assert not out.exists();out.write_text(json.dumps({'path':str(p),'sha256':h})+'\n')
else:assert json.loads(out.read_text())['sha256']==h
print('PASS original actual upgraded backing bytes',sys.argv[1])
