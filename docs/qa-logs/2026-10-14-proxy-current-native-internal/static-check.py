#!/usr/bin/env python3
"""AST/hash/shell syntax only. Never import prepared runner or run a target."""
import ast,gzip,hashlib,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(p):
    with p.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def main():
    checks=[]
    for p in sorted(HERE.glob('*.py')):
        ast.parse(p.read_text(),filename=str(p));checks.append('AST '+p.name)
    for p in sorted((HERE/'plan').glob('*.sh')):
        subprocess.run(['bash','-n',str(p)],check=True);checks.append('bash -n '+p.name)
    b=json.loads((HERE/'plan/input-bindings.json').read_text())
    recipe=(HERE/'plan/raofflineproxy.mk').read_text()
    function=re.search(r'(?ms)^make_target\(\) \{\n.*?^\}',recipe)[0]+'\n'
    assert function==(HERE/'plan/make-target.sh').read_text();checks.append('make_target byte-identical current recipe')
    assert len(json.loads((HERE/'plan/patch-scope.json').read_text()))==16
    assert all(not x['native_effect'] for x in json.loads((HERE/'plan/patch-scope.json').read_text()));checks.append('16 local patches Python only')
    proof=json.loads((HERE/'template-evidence.json').read_text())
    for n in proof['unchanged']:assert sha(HERE/n)==proof['files'][n]
    checks.append('Docker owner and watchdog byte-identical accepted lifecycle')
    compressed=HERE/'plan/sdk-headers.json.gz';meta=b['toolchain']['header_and_support_inventory']
    assert sha(compressed)==meta['sha256'] and hashlib.sha256(gzip.decompress(compressed.read_bytes())).hexdigest()==meta['uncompressed_sha256']
    assert len(json.loads(gzip.decompress(compressed.read_bytes())))==meta['files'];checks.append('compressed SDK header/support inventory')
    assert sha(HERE/'plan/source-files.json')==b['source_inventory_sha256'];checks.append('857 original archive source file identities')
    source=(HERE/'run-stage.py').read_text();assert "'proxy-export'" in source and 'chdman-' not in source and 'configured-generated' not in source
    assert "SEQUENCES = {'proxy':['proxy-export','proxy-build']}" in (HERE/'common.py').read_text()
    for base in [HERE/'plan',HERE]:
        for line in (base/'SHA256SUMS').read_text().splitlines():
            digest,n=line.split('  ',1);assert sha(base/n)==digest,n
    checks.append('both sealed manifests')
    print(json.dumps({'status':'PASS','scope':'static only; export/build/provenance binder/VM UNRUN','checks':checks},indent=2))
if __name__=='__main__':main()
