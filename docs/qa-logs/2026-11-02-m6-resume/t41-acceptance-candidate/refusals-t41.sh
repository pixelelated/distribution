#!/bin/bash
set -eu
OWN=/workspace/tmp/m6-coordinator/kit/selftest/accept-t41-candidate-01a19d12
exec python3 -I "$OWN/test_candidate.py" refusals
