#!/bin/bash
set -eu
exec taskset -c 0 prlimit --as=8589934592 --fsize=17179869184 -- timeout --signal=TERM --kill-after=15s 1500s python3 -I /workspace/tmp/pix-m7-image-readback-20261014-02/verify-image.py --build-owner /workspace/tmp/pix-m7-engineering-build-20261014-02 --output /workspace/tmp/pix-m7-image-readback-20261014-02/artifacts
