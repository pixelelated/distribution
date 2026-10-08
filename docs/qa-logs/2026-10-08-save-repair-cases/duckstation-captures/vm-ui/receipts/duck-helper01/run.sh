#!/bin/bash
set -uo pipefail
scp -q -i /workspace/tmp/pixelelated-520-ui-20261008/guest01/qa-key -P 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /workspace/tmp/pixelelated-520-ui-20261008/duck-helper01/guest.py root@127.0.0.1:/storage/qa521/helper-controls.py
ssh -i /workspace/tmp/pixelelated-520-ui-20261008/guest01/qa-key -p 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1 'python3 /storage/qa521/helper-controls.py'
rc=$?
scp -q -i /workspace/tmp/pixelelated-520-ui-20261008/guest01/qa-key -P 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1:/storage/qa521/helper-controls/results.json /workspace/tmp/pixelelated-520-ui-20261008/duck-helper01/results.json
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-520-ui-20261008/duck-helper01/inner.rc
exit "$rc"
