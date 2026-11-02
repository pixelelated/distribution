set -eu
export LC_ALL=C
ES_REPO=/home/max/Development/emulationstation-next
INPUT_HELPER=docs/qa-logs/2026-11-02-m6-resume/t44-brief-inputs.py
INPUT_OUT=$(mktemp -d /tmp/m6-t44-inputs.XXXXXX)
python3 "$INPUT_HELPER" --repo "$PWD" --ref c348d43dddc4bddbe1055d20d37431503283b817 --es-repo "$ES_REPO" --out "$INPUT_OUT/source"
python3 "$INPUT_HELPER" --repo "$PWD" --ref HEAD --es-repo "$ES_REPO" --es-ref 55158d2a64c69fe295fb4e67fd174424a71b1b4d --out "$INPUT_OUT/seed"
python3 - "$INPUT_OUT" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
for name in ('native.json', 'additions.json', 'companions.json'):
    assert (p/'source'/name).read_bytes() == (p/'seed'/name).read_bytes(), name
a = json.loads((p/'source/summary.json').read_bytes())
b = json.loads((p/'seed/summary.json').read_bytes())
for x in (a, b):
    x.pop('distribution_ref'); x.pop('es_ref')
assert a == b
print('PASS T44 immutable input equality; native594 / additions3 / companions4')
PY
