#!/bin/bash
# Future coordinator payload; no execution in the source-only lane.
set -euo pipefail
TASK_TREE=${1:?existing frozen build checkout}
TASK_OWNER=${2:?fresh cache owner}
TASK_EXPECTED=${3:?frozen source commit}
TASK_PARENT=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20
TASK_ROOT=build.pixelelated-GENERIC_X64.x86_64
[ "$(pwd -P)" = "$TASK_TREE" ]
[ "$(git rev-parse HEAD)" = "$TASK_EXPECTED" ]
[ -z "$(git status --porcelain)" ]
[ ! -e "$TASK_TREE/$TASK_ROOT" ]
[ -n "${RASTERATOPS_BUILD_RUN:?admitted watcher required}" ]
printf '%s\n' "$TASK_TREE/$RASTERATOPS_BUILD_RUN" > "$TASK_OWNER/run.path"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"' EXIT
rsync -aH --numeric-ids --info=progress2 "$TASK_PARENT/$TASK_ROOT/" "$TASK_TREE/$TASK_ROOT/"
rsync -aHnc --numeric-ids --delete --itemize-changes "$TASK_PARENT/$TASK_ROOT/" "$TASK_TREE/$TASK_ROOT/" > "$TASK_OWNER/cache-compare.txt"
[ ! -s "$TASK_OWNER/cache-compare.txt" ]
python3 -I - "$TASK_PARENT/$TASK_ROOT" "$TASK_TREE/$TASK_ROOT" "$TASK_OWNER/cache-ready.json" <<'PY'
import json, os, pathlib, sys
old, new, output = map(pathlib.Path, sys.argv[1:])
n = 0
for base, dirs, files in os.walk(new, followlinks=False):
    for name in files:
        p = pathlib.Path(base) / name
        if p.is_symlink() or not p.is_file():
            continue
        a = (old / p.relative_to(new)).stat()
        b = p.stat()
        assert (a.st_dev, a.st_ino) != (b.st_dev, b.st_ino), p
        n += 1
        if n % 250000 == 0:
            print('Verified independent regular files:', n, flush=True)
assert n > 0
with output.open('x') as f:
    json.dump({'checksum_equal': True, 'independent_regular_files': n,
               'old': str(old), 'new': str(new)}, f, indent=2)
    f.write('\n')
PY
[ "$(git rev-parse HEAD)" = "$TASK_EXPECTED" ]
[ -z "$(git status --porcelain)" ]
