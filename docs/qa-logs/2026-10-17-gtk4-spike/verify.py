#!/usr/bin/env python3
"""Read-only packet checks plus disposable small source/lint staging; no compiler."""
import argparse
import ast
import hashlib
import gzip
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True)
    args = ap.parse_args()
    packet = Path(__file__).resolve().parent
    inputs = json.loads((packet / 'inputs.json').read_text())
    checks = {}
    for item in packet.glob('*.py'):
        ast.parse(item.read_text())
        checks['ast:' + item.name] = True
    manifest = packet / 'SHA256SUMS'
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            expected, name = line.split('  ', 1)
            path = (packet / name).resolve()
            if not path.is_relative_to(packet) or not path.is_file():
                raise RuntimeError('manifest path invalid')
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise RuntimeError('manifest hash mismatch: ' + name)
        checks['manifest'] = True
    with tempfile.TemporaryDirectory(prefix='pix-gtk4-source-check-') as raw:
        root = Path(raw)
        result = subprocess.run([sys.executable, '-I', str(packet / 'prepare-input-spike.py'),
                                 '--repo', str(args.repo), '--output', str(root / 'input')],
                                capture_output=True, text=True, timeout=20, check=True)
        checks['preparer'] = json.loads(result.stdout)
        ast.parse((root / 'input/native_keyboard.py').read_text())
        checks['generated_ast'] = True
        checks['prepared_bytes'] = sum(f.stat().st_size for f in (root / 'input').iterdir())
        overlay_result = subprocess.run([sys.executable, '-I', str(packet / 'prepare-overlay.py'),
                                         '--output', str(root / 'overlay')], capture_output=True,
                                        text=True, timeout=20, check=True)
        checks['overlay_materializer'] = json.loads(overlay_result.stdout)
        root = root / 'overlay'
        script = root / 'pkgcheck'
        script.write_bytes(subprocess.check_output(['git', '-C', str(args.repo), 'show',
                           inputs['source_ref'] + ':tools/pkgcheck'], timeout=20))
        recipes = sorted((root / 'projects').rglob('package.mk'))
        for item in recipes:
            subprocess.run(['bash', '-n', str(item)], capture_output=True, check=True, timeout=10)
        result = subprocess.run(['bash', str(script), 'graphene', 'gtk4', 'webkitgtk',
                                 'libseccomp', 'bubblewrap', 'xdg-dbus-proxy'], cwd=root,
                                env=dict(os.environ, TERM='dumb'), capture_output=True,
                                text=True, timeout=20, check=True)
        checks['recipe_count'] = len(recipes)
        checks['pkgcheck_stdout'] = result.stdout
        checks['pkgcheck_stderr'] = result.stderr
        checks['pkgcheck_exit'] = result.returncode
    for name, expected in inputs['source_sha256'].items():
        if '/patches/' in name:
            path = packet / 'source-patches' / (Path(name).name + '.gz')
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == expected
    checks['compiler'] = checks['runtime'] = 'UNRUN'
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
