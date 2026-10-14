#!/bin/sh
set -eu
mkdir /tmp/pix-output/checks
cd /tmp/pix-output/checks
mkdir scratch
export TMPDIR=/tmp/pix-output/checks/scratch
set +e
timeout --signal=TERM --kill-after=5s 180s python3 -I -B /tmp/pix-input/baseline/pixelelated-state-check-test --self-test > baseline.stdout 2> baseline.stderr
rc=$?; printf '%s\n' "$rc" > baseline.rc
test "$rc" -eq 2 || exit 1
timeout --signal=TERM --kill-after=5s 180s python3 -I -B /tmp/pix-input/candidate/pixelelated-state-check-test --self-test > candidate.stdout 2> candidate.stderr
rc=$?; printf '%s\n' "$rc" > candidate.rc
test "$rc" -eq 0 || exit 1
timeout --signal=TERM --kill-after=5s 30s python3 -I -B /tmp/pix-input/candidate/recipe-selection-test.py --recipe /tmp/pix-input/baseline/package.mk > baseline-recipe.stdout 2> baseline-recipe.stderr
rc=$?; printf '%s\n' "$rc" > baseline-recipe.rc
test "$rc" -eq 1 || exit 1
timeout --signal=TERM --kill-after=5s 30s python3 -I -B /tmp/pix-input/candidate/recipe-selection-test.py --recipe /tmp/pix-input/candidate/package.mk > recipe.stdout 2> recipe.stderr
rc=$?; printf '%s\n' "$rc" > recipe.rc
test "$rc" -eq 0 || exit 1
python3 -I -B - <<'PY_RESULT'
import json
from pathlib import Path
p=Path('/tmp/pix-output/checks')
result={'status':'PASS','root_controls':json.loads((p/'candidate.stdout').read_text()),'recipe':json.loads((p/'recipe.stdout').read_text()),'baseline_gate_exit':int((p/'baseline.rc').read_text()),'baseline_recipe_exit':int((p/'baseline-recipe.rc').read_text())}
assert not (p/'candidate.stderr').read_bytes() and not (p/'recipe.stderr').read_bytes()
(p/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('SCREEN_SCRAPER_CONTROLS_PASS',result['root_controls']['control_count'],len(result['recipe']['cases']))
PY_RESULT
