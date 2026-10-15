#!/bin/bash
set -eu
READBACK_PACKET=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec taskset -c 0 prlimit --as=8589934592 --fsize=17179869184 -- timeout --signal=TERM --kill-after=15s 1500s python3 -I "$READBACK_PACKET/verify-image.py" --build-owner /workspace/tmp/pix-m7-engineering-build-20261015-01 --output /workspace/tmp/pix-m7-image-readback-20261015-01/artifacts
