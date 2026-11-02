#!/bin/bash
set -u
set -o pipefail
OWN=/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12
python3 -I "$OWN/derive-t41.py" /workspace/tmp/m6-coordinator/kit/t36-accept.sh "$OWN/t41-accept.sh"
rc=$?
[ "$rc" -eq 0 ] || exit "$rc"
python3 -I "$OWN/test_candidate.py" all | tee "$OWN/selftest.out"
exit "${PIPESTATUS[0]}"
