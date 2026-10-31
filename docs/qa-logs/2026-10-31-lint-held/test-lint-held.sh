#!/usr/bin/env bash
# test-lint-held.sh -- #1308: tools/lint-audit-artifacts' held mode, on scratch copies.
#
# Builds scratch roots from the coordinator's tree with `git archive` (no
# worktree is made or written), applies lint-held.patch with `patch -p1`, and
# runs each case on a synthetic audit folder derived from an existing one
# (BASE). Every reply is printf'd here. No held file is ever opened: the
# synthetic hold's path_at_hold is a file at mode 000, so a lint that tried to
# read it would fail case 1. T34's folder is linted exactly as committed (its
# reply absent), then with the sidecar this script writes from the receipt.
#
#   ./test-lint-held.sh     # exit 0 only when every check is as expected
#
# Overrides: COORD (the coordinator's worktree), REF (its ref), T34_WT and
# T34_REF (where T34's folder and its lint are read).
set -u -o pipefail

K=$(cd "$(dirname "$0")" && pwd)
COORD=${COORD:-/workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346}
REF=${REF:-HEAD}
T34_WT=${T34_WT:-/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-components-681}
T34_REF=${T34_REF:-308d0f7571}
BASE=docs/audits/2026_10_11-epic-553-post-review-344
REPLY=claude-audit.md
T34=docs/audits/2026_10_30-epic-m6-es-core-components
PATCH=$K/lint-held.patch
W=$K/work
OUT=$K/out

GOOD='synthetic seat reply for #1308 -- a made-up text, not a review'
OTHER='synthetic seat reply for #1308 -- a different, made-up copy'
S=$(printf '%s\n' "$GOOD" | sha256sum | cut -d' ' -f1)

[ -f "$PATCH" ] || { echo "no $PATCH"; exit 2; }
if [ -d "$W" ]; then chmod -R u+rwX "$W"; fi
rm -rf "${W:?}"
rm -rf "${OUT:?}"
mkdir -p "$W" "$OUT"

echo "test-lint-held: $(date -u +%FT%TZ); coordinator $(git -C "$COORD" rev-parse --short=10 "$REF"); T34 $T34_REF; patch $(sha256sum "$PATCH" | cut -c1-16)"

pass=0
total=0
# check <label> <want rc> <rc> <output file> <want last line> [<line it must contain>...]
check() {
  local label=$1 want_rc=$2 rc=$3 file=$4 want_last=$5 last missing="" l
  shift 5
  last=$(tail -n 1 "$file")
  for l in "$@"; do grep -q -F -- "$l" "$file" || missing="$missing [$l]"; done
  total=$((total + 1))
  if [ "$rc" -eq "$want_rc" ] && [ "$last" = "$want_last" ] && [ -z "$missing" ]; then
    pass=$((pass + 1))
    echo "  ok    $label: rc=$rc, last line '$last'"
    for l in "$@"; do grep -F -m1 -- "$l" "$file" | sed 's/^ */          /'; done
  else
    echo "  FAIL  $label: wanted rc=$want_rc and '$want_last'; got rc=$rc and '$last'; missing:${missing:- none}"
  fi
}

# mkroot <dir> <git dir> <ref> <audit folder> <patch|nopatch>
mkroot() {
  mkdir -p "$1"
  git -C "$2" archive "$3" tools/lint-audit-artifacts tools/ceremony-check "$4" | tar -x -C "$1" || return 1
  if [ "$5" = patch ]; then
    patch -p1 -s --batch --forward -d "$1" < "$PATCH" || return 1
  fi
}

# json <file> <python statement over j> -- edit a scratch JSON in place
json() {
  python3 -I -B - "$1" "$2" <<'PY'
import json, sys
path, stmt = sys.argv[1], sys.argv[2]
try:
    j = json.load(open(path))
except FileNotFoundError:
    j = {}
exec(stmt, {}, {'j': j})
open(path, 'w').write(json.dumps(j, indent=2) + '\n')
PY
}

# lint <root> <folder> <out label>; sets rc
lint() {
  "$1/tools/lint-audit-artifacts" "$2" > "$OUT/$3.txt" 2>&1
  rc=$?
}

# marker <root> <folder> <out label>; sets rc -- tools/ceremony-check's marker
# loop (its lines 371-381 at the coordinator's HEAD) through the module's own
# completed_audit_marker() and sh(), its ROOT the scratch root; gh is not asked.
marker() {
  python3 -I -B - "$1/tools/ceremony-check" "$1/$2/audit-completion.json" > "$OUT/$3.txt" 2>&1 <<'PY'
import datetime as dt, importlib.machinery, importlib.util, os, sys
loader = importlib.machinery.SourceFileLoader('ceremony_check', sys.argv[1])
spec = importlib.util.spec_from_loader('ceremony_check', loader)
cc = importlib.util.module_from_spec(spec)
loader.exec_module(cc)
marker = sys.argv[2]
try:
    ended, issue = cc.completed_audit_marker(marker, cc.ROOT, dt.datetime.now(dt.timezone.utc))
    rc, out, err = cc.sh([os.path.join(cc.ROOT, 'tools/lint-audit-artifacts'),
                          os.path.dirname(marker), '--phase', 'resolution'])
    if rc:
        raise ValueError('resolution lint failed: ' + (out or err)[-160:])
    print('audit marker valid: #%d %s, completed %s' % (issue, os.path.relpath(marker, cc.ROOT), ended.isoformat()))
except (OSError, ValueError, KeyError, TypeError) as error:
    print('audit marker invalid: %s: %s' % (os.path.relpath(marker, cc.ROOT), str(error).replace('\n', ' ')))
    sys.exit(1)
PY
  rc=$?
}

# The roots: the coordinator's tools and BASE, patched and not.
mkroot "$W/root-patched" "$COORD" "$REF" "$BASE" patch || { echo "cannot build the patched root"; exit 2; }
mkroot "$W/root-unpatched" "$COORD" "$REF" "$BASE" nopatch || { echo "cannot build the unpatched root"; exit 2; }

# The synthetic hold's off-tree file: mode 000, so reading it would fail.
mkdir -p "$W/synthetic-held"
printf '%s\n' "$GOOD" > "$W/synthetic-held/$REPLY"
chmod 000 "$W/synthetic-held/$REPLY"
chmod 700 "$W/synthetic-held"
HELD_AT=$W/synthetic-held/$REPLY

# newcase <name> <patched|unpatched>: a root copy whose BASE reply is absent and
# whose receipt binds the synthetic sha S. Sets F (folder) and SO (second-opinions).
newcase() {
  cp -a "$W/root-$2" "$W/$1"
  F=$W/$1/$BASE
  SO=$F/second-opinions
  rm -f -- "${SO:?}/$REPLY"
  json "$SO/$REPLY.provenance.json" "j['final']['file_artifact_sha256'] = '$S'
if 'output_file_sha256' in j: j['output_file_sha256'] = '$S'"
  printf 'the reply is held off the tree; its sha256 is %s\n' "$S" > "$F/held-record.txt"
}

# hold <sidecar> [<python statement to apply after the full declaration>]
hold() {
  json "$1" "j.update({'schema_version': 1, 'reply': '$REPLY', 'sha256': '$S', 'path_at_hold': '$HELD_AT',
  'mode': '0600', 'reason': 'synthetic: a reply too sensitive for the tree (#1308 test)',
  'recorded_in': ['held-record.txt', 'second-opinions/$REPLY.provenance.json']})
${2:-pass}"
}

echo
echo "== regression: the unchanged folder, both tools"
lint "$W/root-patched" "$W/root-patched/$BASE" r0-patched
rc_p=$rc
lint "$W/root-unpatched" "$W/root-patched/$BASE" r0-unpatched
check "R0 patched on the existing folder" 0 "$rc_p" "$OUT/r0-patched.txt" PASS
total=$((total + 1))
if cmp -s "$OUT/r0-patched.txt" "$OUT/r0-unpatched.txt"; then
  pass=$((pass + 1)); echo "  ok    R0 patched and unpatched print identical output on it"
else
  echo "  FAIL  R0 the patched tool's output differs from the unpatched on a folder with no hold"
fi

echo
echo "== the six cases"
newcase case1 patched
hold "$SO/$REPLY.held.json"
lint "$W/case1" "$F" case1
check "1 held + sidecar, no reply" 0 "$rc" "$OUT/case1.txt" PASS \
  "HELD second-opinions/$REPLY (off-tree; sha256 bound): held off the tree, sha256 recorded, PASS"

newcase case2 patched
hold "$SO/$REPLY.held.json"
printf '%s\n' "$GOOD" > "$SO/$REPLY"
lint "$W/case2" "$F" case2
check "2 held, the reply present and matching" 0 "$rc" "$OUT/case2.txt" PASS \
  "HELD second-opinions/$REPLY: the copy present matches its held sha256 (content checked here)"

newcase case3 patched
hold "$SO/$REPLY.held.json"
printf '%s\n' "$OTHER" > "$SO/$REPLY"
lint "$W/case3" "$F" case3
check "3 held, the reply present and differing" 1 "$rc" "$OUT/case3.txt" "1 CONTRACT FAILURE(S)" \
  "the copy of a held reply differs from its held sha256"

newcase case4 patched
hold "$SO/$REPLY.held.json" "del j['sha256']"
lint "$W/case4" "$F" case4
check "4 held without sha256" 1 "$rc" "$OUT/case4.txt" "1 CONTRACT FAILURE(S)" \
  "hold declares no sha256 of 64 hex"

newcase case5 patched
lint "$W/case5" "$F" case5
lint "$W/root-unpatched" "$F" case5-unpatched
check "5 no hold, no reply (patched)" 1 "$rc" "$OUT/case5.txt" "1 CONTRACT FAILURE(S)" \
  "second-opinions/review-plan.json or its call evidence is invalid: [Errno 2] No such file or directory"
total=$((total + 1))
if cmp -s "$OUT/case5.txt" "$OUT/case5-unpatched.txt"; then
  pass=$((pass + 1)); echo "  ok    5 the patched FAIL is byte-identical to the unpatched tool's on the same folder"
else
  echo "  FAIL  5 the patched tool's FAIL differs from the unpatched tool's"
fi

newcase case6 unpatched
hold "$SO/$REPLY.held.json"
lint "$W/case6" "$F" case6
check "6 the unpatched tool on case 1 (the positive before the fix)" 1 "$rc" "$OUT/case6.txt" "1 CONTRACT FAILURE(S)" \
  "No such file or directory: '$F/second-opinions/$REPLY'"

echo
echo "== the declaration's other refusals"
newcase case7 patched
hold "$SO/$REPLY.held.json" "del j['reason']"
lint "$W/case7" "$F" case7
check "7 held without a reason" 1 "$rc" "$OUT/case7.txt" "1 CONTRACT FAILURE(S)" "hold declares no reason"

newcase case8 patched
hold "$SO/$REPLY.held.json" "j['sha256'] = '0' * 64"
lint "$W/case8" "$F" case8
check "8 the hold's sha256 is not the receipt's" 1 "$rc" "$OUT/case8.txt" "1 CONTRACT FAILURE(S)" \
  "held sha256 differs from the digest its receipt records"

newcase case9 patched
json "$SO/$REPLY.provenance.json" "j['held'] = True"
lint "$W/case9" "$F" case9
check "9 'held' written into the Facilitator receipt" 1 "$rc" "$OUT/case9.txt" "1 CONTRACT FAILURE(S)" \
  "a hold belongs in $REPLY.held.json, not in the Facilitator receipt"

newcase case10 patched
hold "$SO/$REPLY.held.json" "j['recorded_in'] = ['03-retrospective.md']"
lint "$W/case10" "$F" case10
check "10 recorded_in names a file without the sha256" 1 "$rc" "$OUT/case10.txt" "1 CONTRACT FAILURE(S)" \
  "hold record 03-retrospective.md does not carry the held sha256"

newcase case11 patched
hold "$SO/$REPLY.held.json" "j['path_at_hold'] = '$F/second-opinions/$REPLY'"
lint "$W/case11" "$F" case11
check "11 path_at_hold inside the audit folder" 1 "$rc" "$OUT/case11.txt" "1 CONTRACT FAILURE(S)" \
  "hold declares no absolute path_at_hold outside the audit folder"

echo
echo "== tools/ceremony-check's marker validation (the same lint, through its own functions)"
# BASE's completion marker seals its receipt among the evidence, so these
# cases leave the receipt as committed: the reply is taken out of the scratch
# copy and the hold declares the digest the receipt already records (copied
# by command). The committed reply's bytes are not read.
for side in patched unpatched; do
  cp -a "$W/root-$side" "$W/m-$side"
  SO=$W/m-$side/$BASE/second-opinions
  rm -f -- "${SO:?}/$REPLY"
  python3 -I -B - "$SO/$REPLY.provenance.json" "$SO/$REPLY.held.json" "$HELD_AT" <<'PY'
import json, sys
sha = json.load(open(sys.argv[1]))['final']['file_artifact_sha256']
open(sys.argv[2], 'w').write(json.dumps({
    "schema_version": 1, "reply": "claude-audit.md", "sha256": sha, "path_at_hold": sys.argv[3],
    "mode": "0600", "reason": "synthetic: the committed reply taken out of a scratch copy (#1308 test)",
    "recorded_in": ["second-opinions/claude-audit.md.provenance.json"]}, indent=2) + '\n')
PY
done
MARKER=$W/m-patched/$BASE/audit-completion.json
WANT_VALID="audit marker valid: #$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["issue"])' "$MARKER") $BASE/audit-completion.json, completed $(python3 -I -c 'import datetime as d,json,sys; print(d.datetime.fromisoformat(json.load(open(sys.argv[1]))["completed_at"].replace("Z","+00:00")).isoformat())' "$MARKER")"
marker "$W/m-patched" "$BASE" m-patched
check "M1 patched root, BASE held off the scratch tree" 0 "$rc" "$OUT/m-patched.txt" "$WANT_VALID"
marker "$W/m-unpatched" "$BASE" m-unpatched
check "M2 unpatched root, the same folder" 1 "$rc" "$OUT/m-unpatched.txt" \
  "$(tail -n 1 "$OUT/m-unpatched.txt")" "audit marker invalid: $BASE/audit-completion.json: resolution lint failed:" \
  "1 CONTRACT FAILURE(S)"

echo
echo "== T34's folder at $T34_REF, its reply absent as committed"
mkroot "$W/t34" "$T34_WT" "$T34_REF" "$T34" patch || { echo "cannot build the T34 root"; exit 2; }
lint "$W/t34" "$W/t34/$T34" t34-nohold
check "T1 no sidecar: the contract fails as on next today" 1 "$rc" "$OUT/t34-nohold.txt" "1 CONTRACT FAILURE(S)" \
  "No such file or directory: '$W/t34/$T34/second-opinions/gpt-audit.md'"
marker "$W/t34" "$T34" t34-m-nohold
check "T2 no sidecar: the ceremony marker invalid" 1 "$rc" "$OUT/t34-m-nohold.txt" \
  "$(tail -n 1 "$OUT/t34-m-nohold.txt")" "audit marker invalid: $T34/audit-completion.json: resolution lint failed:"

# The sidecar, its sha256 copied from the receipt by command, never typed.
python3 -I -B - "$W/t34/$T34/second-opinions/gpt-audit.md.provenance.json" "$K/t34-gpt-audit.md.held.json" <<'PY'
import json, sys
receipt = json.load(open(sys.argv[1]))
sha = receipt['final']['file_artifact_sha256']
assert receipt['output_file_sha256'] == sha
hold = {
    "schema_version": 1,
    "reply": "gpt-audit.md",
    "sha256": sha,
    "path_at_hold": "/workspace/tmp/m6-t34/held/gpt-audit.md",
    "mode": "0600",
    "reason": "one finding (PL-27, #1323) is security-sensitive and this repository is public; "
              "the reply stays off the tree until the maintainer decides where its details go (#681 stage-D post)",
    "recorded_in": [
        "second-opinions/gpt-audit.md.provenance.json",
        "second-opinions/review-plan.json",
        "04-analysis.md"
    ],
    "refs": ["#681", "#1307", "#1308"]
}
open(sys.argv[2], 'w').write(json.dumps(hold, indent=2) + '\n')
PY
cp "$K/t34-gpt-audit.md.held.json" "$W/t34/$T34/second-opinions/gpt-audit.md.held.json"

lint "$W/t34" "$W/t34/$T34" t34-held
check "T3 with the sidecar, T34's patched lint" 0 "$rc" "$OUT/t34-held.txt" PASS \
  "HELD second-opinions/gpt-audit.md (off-tree; sha256 bound): held off the tree, sha256 recorded, PASS"
lint "$W/root-patched" "$W/t34/$T34" t34-held-coord
check "T4 with the sidecar, the coordinator's patched lint" 0 "$rc" "$OUT/t34-held-coord.txt" PASS \
  "HELD second-opinions/gpt-audit.md (off-tree; sha256 bound): held off the tree, sha256 recorded, PASS"
marker "$W/t34" "$T34" t34-m-held
check "T5 with the sidecar: the ceremony marker valid" 0 "$rc" "$OUT/t34-m-held.txt" \
  "$(tail -n 1 "$OUT/t34-m-held.txt")" "audit marker valid: #1307 $T34/audit-completion.json"

echo
echo "TOTAL: $pass of $total checks as expected"
[ "$pass" -eq "$total" ]
