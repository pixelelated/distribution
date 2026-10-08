#!/bin/bash
set -uo pipefail
bash /workspace/tmp/pixelelated-524-path-refusal/stage01/stage.sh
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/stage01/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/stage01/outer.rc
exit "$rc"
