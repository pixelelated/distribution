from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

owner = Path(__file__).resolve().parent
tree = Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
bundle = Path('/workspace/artifacts/pixelelated-candidates/sha256/b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1')
assert Path.cwd() == tree
assert not (owner / 'qa.start').exists()
(owner / 'qa.start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat() + '\n')
(owner / 'run.path').write_text(str(tree / os.environ['RASTERATOPS_BUILD_RUN']) + '\n')
code = 1
try:
    seal = json.loads((owner / 'seal.json').read_text())
    for path, digest in seal.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
    subprocess.run(['git', 'diff', '--quiet', '7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2', '--', 'projects', 'packages', 'distributions', 'config'], check=True)
    subprocess.run([str(tree / 'tools/rasteratops-candidate-store'), 'verify', str(bundle)], check=True)
    code = subprocess.run([sys.executable, '-I', str(owner / 'probe.py'), '--tree', str(tree),
        '--image', str(bundle / 'pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz'),
        '--build-id', '7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2', '--output', str(owner / 'proof')]).returncode
    for path, digest in seal.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
except BaseException:
    code = 1
    raise
finally:
    (owner / 'inner.rc').write_text(str(code) + '\n')
    (owner / 'outer.rc').write_text(str(code) + '\n')
sys.exit(code)
