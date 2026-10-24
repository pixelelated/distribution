#!/bin/bash
# identity-reasons-case.sh -- T14 S1's control for #989's second half: a
# refusal for the wrong reason. Two doubles, each in a scratch root copied
# from the tree: the preparer (fork-publish-release) wrapped so that every
# refusal it makes says "wrong reason", and the identity policy
# (config/build-identity) with every message replaced. The fixed test must
# fail its refusal cases; the same test with refused() reverted to "any
# non-zero" (the stage-D rule) must credit them. Nothing outside the scratch.
#   identity-reasons-case.sh <tree> <scratch>
set -u
T="$(cd "$1" && pwd)"; S="$2"; rm -rf "$S"; mkdir -p "$S"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
mkroot() {  # <dir>: config, scripts and the tools the test reaches, copied
  mkdir -p "$1/tools"; cp -r "$T/config" "$T/scripts" "$1/"
  for t in build-identity-test fork-publish-release pixelelated-state-check pixelelated-state-check-test rasteratops-candidate-store; do cp "$T/tools/$t" "$1/tools/$t"; done
}
wrong_preparer() {  # the real preparer, its refusal reason replaced
  mv "$1/tools/fork-publish-release" "$1/tools/fork-publish-release.real"
  printf '#!/bin/sh\nout=$("$(dirname "$0")/fork-publish-release.real" "$@" 2>/dev/null); rc=$?\n[ "$rc" -eq 0 ] && { printf "%%s\\n" "$out"; exit 0; }\necho "release preparation: wrong reason" >&2; exit 1\n' > "$1/tools/fork-publish-release"
  chmod +x "$1/tools/fork-publish-release"
}
wrong_policy() { sed -i 's/echo "build identity: [^"]*"/echo "build identity: wrong reason"/' "$1/config/build-identity"; }
revert() { python3 -I - "$1/tools/build-identity-test" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
a='        return result.returncode == code and reason in result.stderr'
assert a in s; open(p,'w').write(s.replace(a,'        return result.returncode != 0'))
PY
}
run() { rm -f "$1.json"; python3 -I "$1/tools/build-identity-test" --output "$1.json" > "$1.out" 2>&1; echo $?; }
for double in preparer policy; do
  for side in fixed reverted; do
    R="$S/$double-$side"; mkroot "$R"; wrong_$double "$R"; [ "$side" = reverted ] && revert "$R"
    rc=$(run "$R"); n=$(python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); print(sum(1 for c in d['checks'] if not c['passed']))" "$R.json" 2>/dev/null || echo "?")
    echo "  $double double, $side test: rc $rc, failed checks $n | $(tail -1 "$R.out" | cut -c1-80)"
    if [ "$side" = fixed ]; then check "the fixed test fails a refusal given for the wrong reason ($double)" "$([ "$rc" = 1 ] && echo 0 || echo 1)"
    else check "the any-non-zero rule credits the same wrong reason ($double): the positive" "$([ "$rc" = 0 ] && echo 0 || echo 1)"; fi
  done
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
