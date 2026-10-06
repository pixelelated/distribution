#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-p4-interruption-copy-host-02/run.sh
rc=$?
printf '%s\n' "$rc" > /workspace/tmp/pixelelated-m7-p4-interruption-copy-host-02/outer.rc
exit "$rc"
