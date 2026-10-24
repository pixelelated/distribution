#!/bin/bash
# duckstation-case.sh -- T14 S3's control for #998: where the installed payload
# runs, and whether an unknown --cases name is refused. Scratch copies of the
# stage-D test (its version literal patched, so it runs against the package's
# rclone) and the fixed one, each with one named substitution: the synthetic
# payload also writes a marker to the host path a caller variable names. On the
# host the marker appears; inside the sandbox (its environment cleared, the
# host path not mounted) it cannot. Nothing outside the scratch.
#   duckstation-case.sh <tree> <stage-D tools dir> <rclone> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; RC="$3"; S="$4"; rm -rf "${S:?}"; mkdir -p "$S"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
copy() {  # <src> <dst>: the test, its payload marked
  python3 -I - "$1" "$2" <<'PY'
import re, sys; s = open(sys.argv[1]).read()
s = s.replace("rclone v1.75.1'", "rclone v1.75.2'")
marked = r"""        payload=b'#!/bin/bash\nprintf "%s\\n" synthetic-executable-permission-witness\nprintf x > "${PAYLOAD_HOST_MARKER:-/nonexistent/marker}" 2>/dev/null\nexit 0\n'"""
s, n = re.subn(r"^        payload=b'#!/bin/(?:ba)?sh\\n.*$", lambda m: marked, s, count=1, flags=re.M)
assert n == 1, "payload line not found"; open(sys.argv[2], "w").write(s)
PY
}
for side in old:"$OLD/pixelelated-duckstation-capture-test" new:"$T/tools/pixelelated-duckstation-capture-test"; do
  n=${side%%:*}; src=${side#*:}; copy "$src" "$S/$n-test"
  marker="$S/$n-host-marker"
  PAYLOAD_HOST_MARKER="$marker" python3 -I "$S/$n-test" --source-root "$T" --rclone "$RC" --output "$S/$n-run" --cases package-executable-mode > "$S/$n-run.txt" 2>&1; rc=$?
  echo "  $n: payload case rc $rc, host marker $([ -e "$marker" ] && echo present || echo absent) | $(tail -1 "$S/$n-run.txt" | cut -c1-70)"
  python3 -I "$S/$n-test" --source-root "$T" --rclone "$RC" --output "$S/$n-typo" --cases package-executable-mode,no-such-case > "$S/$n-typo.txt" 2>&1; rt=$?
  echo "  $n: --cases package-executable-mode,no-such-case rc $rt | $(tail -1 "$S/$n-typo.txt" | cut -c1-70)"
  if [ "$n" = old ]; then
    check "stage-D: the payload ran on the host (the marker is there): the positive" "$([ -e "$marker" ] && echo 0 || echo 1)"
    check "stage-D: an unknown --cases name is silently dropped (rc 0): the positive" "$([ "$rt" = 0 ] && echo 0 || echo 1)"
  else
    check "fixed: the payload ran inside the sandbox (passes, no host marker)" "$([ "$rc" = 0 ] && [ ! -e "$marker" ] && echo 0 || echo 1)"
    check "fixed: an unknown --cases name exits 2" "$([ "$rt" = 2 ] && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
