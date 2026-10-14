#!/bin/bash
# Coordinator-only final payload inspection; no build, VM, mount or publishing.
set -eu
repo=${1:?frozen distribution checkout}
owner=${2:?fresh allocated owner directory}
update=${3:?actual final update tar}
update_sha=${4:?accepted update SHA256}
image=${5:?actual final install img.gz}
image_sha=${6:?accepted install SHA256}
packet=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
test -d "$owner"
case "$update" in /*.tar) ;; *) exit 2;; esac
case "$image" in /*.img.gz) ;; *) exit 2;; esac
[[ "$update_sha" =~ ^[0-9a-f]{64}$ && "$image_sha" =~ ^[0-9a-f]{64}$ ]]
test ! -e "$owner/payload-scratch"
test ! -e "$owner/payload-bin"
python3 -I - "$repo" "$packet/source-inputs.json" <<'PY'
from pathlib import Path
import hashlib,json,sys
root=Path(sys.argv[1]); bound=json.loads(Path(sys.argv[2]).read_text())
name='tools/pixelelated-state-check'
assert hashlib.sha256((root/name).read_bytes()).hexdigest()==bound['distribution_files'][name]
p=Path(bound['mcopy']['path'])
assert hashlib.sha256(p.read_bytes()).hexdigest()==bound['mcopy']['sha256']
PY
mcopy=$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["mcopy"]["path"])' "$packet/source-inputs.json")
mkdir -m 700 "$owner/payload-scratch" "$owner/payload-bin"
ln -s "$mcopy" "$owner/payload-bin/mcopy"
export TMPDIR="$owner/payload-scratch"
export PATH="$owner/payload-bin:/usr/bin:/bin"
for kind in update install; do
  if [ "$kind" = update ]; then input=$update; expected=$update_sha; else input=$image; expected=$image_sha; fi
  test ! -e "$owner/$kind.json"
  test ! -e "$owner/$kind.rc"
  printf '%s  %s\n' "$expected" "$input" | sha256sum --check --status
  set +e
  timeout --signal=TERM --kill-after=15s 600s python3 -I "$repo/tools/pixelelated-state-check" --payload "$input" > "$owner/$kind.json" 2> "$owner/$kind.stderr"
  rc=$?
  set -e
  printf '%s\n' "$rc" > "$owner/$kind.rc"
  [ "$rc" -eq 0 ] || exit "$rc"
  printf '%s  %s\n' "$expected" "$input" | sha256sum --check --status
  python3 -I - "$owner/$kind.json" "$kind" <<'PY'
import json,sys
r=json.load(open(sys.argv[1]))
assert r['schema']==1 and r['policy']=='pixelelated-selected-state-v1'
assert r['status']=='pass' and r['blocked_count']==0 and r['error_count']==0
assert r['input_kind']==('update-tar' if sys.argv[2]=='update' else 'install-image')
PY
done
# Successful gate calls retire their private TemporaryDirectory themselves.
test -z "$(ls -A "$owner/payload-scratch")"
printf '%s\n' 'PASS: actual update and install payload selected-state checks'
