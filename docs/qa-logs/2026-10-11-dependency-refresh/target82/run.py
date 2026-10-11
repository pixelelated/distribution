from pathlib import Path
import hashlib,json,subprocess,os
p=Path(__file__).resolve().parent;r=Path('/workspace/repos/rocknix.worktrees/m7-component-inputs');tool=r/'tools/last-good-scripts-test';src=tool.read_text()
start=src.index('echo "  F2-4. RetroArch');end=src.index('GW="${RX}/src/gfx/gfx_widgets.c"',start)
section=src[start:end];assert 'TMPDIR="${RX}" patch' in section
header='set -uo pipefail\nROOT='+str(r)+'\nF2='+str(p/'fixture')+'\nOLD=0\nBASE_REF=next\nSOURCES_DIR=/workspace/cache/rocknix-sources\nFAIL=0\ncheck() { if [ "$1" -eq 0 ]; then echo "PASS $2"; else echo "FAIL $3"; FAIL=$((FAIL+1)); fi; }\n'
(p/'actual-section.sh').write_text(header+section+'\nfi\n[ "$FAIL" -eq 0 ]\n')
sha=hashlib.sha256(tool.read_bytes()).hexdigest()
with (p/'proof.log').open('w') as f:rc=subprocess.run(['bash',str(p/'actual-section.sh')],env={**os.environ,'TMPDIR':str(p)},stdout=f,stderr=subprocess.STDOUT).returncode
assert hashlib.sha256(tool.read_bytes()).hexdigest()==sha
(p/'result.json').write_text(json.dumps({'returncode':rc,'harness_sha256':sha,'scope':'exact current F2-4 source section through ordered patch/fuzz check; original80 retains failing default-temp controls'},indent=2)+'\n')
print((p/'proof.log').read_text(),flush=True);raise SystemExit(rc)
