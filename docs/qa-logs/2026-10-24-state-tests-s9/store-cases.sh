#!/bin/bash
# store-cases.sh -- T14 S9's control for #1002 (rasteratops-candidate-store
# verify): a scratch store under the given directory holds two synthetic
# bundles, A and B, made by the fixed tool's own `put`; then each tool runs
#   plain  -- verify B by its own path
#   link   -- verify a symlink named for A's digest that points at B
# Never the real store. Nothing outside the scratch.
#   store-cases.sh <tree> <stage-D tools dir> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; S="$3"
# put seals each bundle 0555/0444; a rerun restores owner write on this scratch alone first
[ -d "${S:?}" ] && chmod -R u+w "${S:?}"; rm -rf "${S:?}"; mkdir -p "$S/in-a" "$S/in-b" "$S/links"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
printf 'synthetic image A\n' > "$S/in-a/image.img"; printf 'synthetic image B\n' > "$S/in-b/image.img"
printf '{"source":"synthetic-a"}\n' > "$S/in-a/inputs.json"; printf '{"source":"synthetic-b"}\n' > "$S/in-b/inputs.json"
for x in a b; do python3 -I "$T/tools/rasteratops-candidate-store" put --store "$S/store" --inputs "$S/in-$x/inputs.json" "$S/in-$x/image.img" > "$S/put-$x.txt" 2>&1 || { echo "put $x failed"; cat "$S/put-$x.txt"; exit 2; }; done
mapfile -t B < <(ls "$S/store/sha256"); [ "${#B[@]}" = 2 ] || { echo "expected two bundles"; exit 2; }
A_ID=$(cd "$S/store/sha256" && grep -l synthetic-a */manifest.json | cut -d/ -f1); B_ID=$(cd "$S/store/sha256" && grep -l synthetic-b */manifest.json | cut -d/ -f1)
ln -s "$S/store/sha256/$B_ID" "$S/links/$A_ID"
for side in old:"$OLD/rasteratops-candidate-store" new:"$T/tools/rasteratops-candidate-store"; do
  n=${side%%:*}; t=${side#*:}
  python3 -I "$t" verify "$S/store/sha256/$B_ID" > "$S/$n-plain.txt" 2>&1; a=$?
  python3 -I "$t" verify "$S/links/$A_ID" > "$S/$n-link.txt" 2>&1; b=$?
  echo "  $n: plain rc $a | a link named A ($A_ID) to B ($B_ID) rc $b: $(head -1 "$S/$n-link.txt" | cut -c1-140)"
  check "$n: B verifies by its own path" "$([ "$a" = 0 ] && echo 0 || echo 1)"
  if [ "$n" = old ]; then
    check "stage-D vouches for A's name over B's bytes (the positive)" "$([ "$b" = 0 ] && echo 0 || echo 1)"
  else
    check "fixed refuses the link, naming both" "$([ "$b" = 1 ] && grep -q "$A_ID is not the directory it names: it resolves to .*$B_ID" "$S/$n-link.txt" && echo 0 || echo 1)"
  fi
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
