#!/bin/bash
exec taskset -c 0 prlimit --as=8589934592 --fsize=17179869184 -- timeout --signal=TERM --kill-after=15s 1500s bash /workspace/tmp/pix-m7-payload-chain-20261014-03/run.sh
