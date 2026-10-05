from pathlib import Path
import subprocess,hashlib,json,sys
bundle=Path(sys.argv[1]);assert bundle==Path('/workspace/artifacts/rasteratops-candidates/sha256/87b8c01d65dc22b4f29049bd0d69307a59c14c16f5223534e95058b2234ca5cd')
assert hashlib.sha256((bundle/'manifest.json').read_bytes()).hexdigest()=='87b8c01d65dc22b4f29049bd0d69307a59c14c16f5223534e95058b2234ca5cd'
assert json.loads((bundle/'manifest.json').read_text())['inputs']['distribution_commit']=='61b64817bf8ab48237e51abb395484e36cbf924b'
subprocess.run(['python3',str(Path(__file__).parent/'verify-current-inputs.py'),'/workspace/artifacts/pixelelated-candidates/sha256/79d560046ee52e28b72f16588168dd7c8fb2637c1cc585713216a8ec828e9d81'],check=True)
print('PASS old baseline manifest identity and unchanged current frozen inputs')
