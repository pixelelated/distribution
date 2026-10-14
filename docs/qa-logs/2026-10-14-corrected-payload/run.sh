#!/bin/bash
# Additive actual image02 binding of accepted payload02 command family.
set -u
python3 -I -S -B - /workspace/tmp/pix-m7-payload-chain-20261014-03/inputs.json <<'CHECK_BINDINGS'
from pathlib import Path
import hashlib,json,sys
b=json.loads(Path(sys.argv[1]).read_text())
for p,h in b['source_sha256'].items():
 assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
CHECK_BINDINGS
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pix-m7-payload-chain-20261014-03/binding.rc
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
bash /tmp/pix-m7-corrected-payload-continuation-20261014/payload-check.sh /workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02 /workspace/tmp/pix-m7-payload-chain-20261014-03 /workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261014T230300Z.gfac608ff8994-from-ROCKNIX.tar e409bc18236cebfe12b24cdaede092c338d51cfe601ea6b89b486ff5578a2e42 /workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261014T230300Z.gfac608ff8994-from-ROCKNIX.img.gz d816d36abc66b292500b0719e672c98c33eb0cd4fc7fc0bf19f7e26e4108bb16 > /workspace/tmp/pix-m7-payload-chain-20261014-03/payload.stdout 2> /workspace/tmp/pix-m7-payload-chain-20261014-03/payload.stderr
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pix-m7-payload-chain-20261014-03/payload.rc
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
timeout --kill-after=5s 30s python3 -I -S -B /tmp/pix-m7-corrected-payload-continuation-20261014/check-shared-identity.py --update /workspace/tmp/pix-m7-payload-chain-20261014-03/update.json --install /workspace/tmp/pix-m7-payload-chain-20261014-03/install.json > /workspace/tmp/pix-m7-payload-chain-20261014-03/shared-identity.stdout 2> /workspace/tmp/pix-m7-payload-chain-20261014-03/shared-identity.stderr
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pix-m7-payload-chain-20261014-03/shared-identity.rc
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
exit 0
