from pathlib import Path
import hashlib,json,subprocess,sys
bundle=Path(sys.argv[1]);assert bundle==Path('/workspace/artifacts/rocknix-images/x64-all-20260929-69e6039f8f')
expected={'ROCKNIX-GENERIC_X64.x86_64-20260929.img.gz': 'e2b662ba728a22cfb05b16779e4475d631b71645a91506261d4c09c3917a67d6', 'ROCKNIX-GENERIC_X64.x86_64-20260929.tar': '6cdf8a03d42b696b8f09b3bf5cfe4b76af29e6e4cb0e1c2530913e6685314147', 'RECORD.txt': '552d2de24a892f2af39fbc0745cdd95868b8264977a6e4cfe71e1d3519575ff1', 'SHA256SUMS': '911e84d827f410558f08af42c469ac220906ec7cf2f2ef4cfe9f426df4f5f051'}
for name,wanted in expected.items():
 with (bundle/name).open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
 assert actual==wanted,name
subprocess.run(['python3',str(Path(__file__).parent/'verify-current-inputs.py'),'/workspace/artifacts/pixelelated-candidates/sha256/79d560046ee52e28b72f16588168dd7c8fb2637c1cc585713216a8ec828e9d81'],check=True)
print('PASS exact ROCKNIX RC2 image/update/record hashes and unchanged current frozen inputs')
