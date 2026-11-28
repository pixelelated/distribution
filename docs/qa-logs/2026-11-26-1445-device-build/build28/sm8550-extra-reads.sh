#!/bin/bash
# Build 28's SM8550-only image reads (#1459 c2, #1422's installed quirk, #1448's FEX).
# Each read is a positive assertion; exit 1 names the first that failed, exit 2 a read that could not run.
set -o pipefail
WT=/workspace/repos/rocknix.worktrees/m7-round-sm8550-20261128
RD=$WT/.build-runs/20261128T064843Z-a7b15e8b
HEAD=6169621a4b
X=/workspace/tmp/rocknix-session/sm8550-sys
fail=0
bad() { echo "FAIL: $*"; fail=1; }
echo "== $(date -u +%FT%TZ) SM8550 extra reads (#1459, #1422, #1448)"
tar=$(ls "$WT"/target/*.g${HEAD}*.tar 2>/dev/null | head -1); [ -n "$tar" ] || { echo "no update tar"; exit 2; }
echo "update tar: $(basename "$tar")"
rm -rf "${X:?}"; mkdir -p "$X"
( cd "$X" && tar -xf "$tar" --wildcards '*/target/SYSTEM' ) || { echo "cannot extract SYSTEM"; exit 2; }
sys=$(find "$X" -name SYSTEM -type f | head -1); [ -n "$sys" ] || { echo "no SYSTEM in the tar"; exit 2; }
echo "SYSTEM sha256: $(sha256sum "$sys" | cut -c1-64)"
unsquashfs -l "$sys" > "$X/listing.txt" 2>/dev/null || { echo "unsquashfs -l failed"; exit 2; }
n=$(wc -l < "$X/listing.txt"); echo "SYSTEM listing: $n entries"
[ "$n" -gt 10000 ] || { echo "listing too short to judge"; exit 2; }

echo "-- #1459: no AetherSX2 binary"
grep -c 'usr/share/aethersx2-sa/aethersx2$' "$X/listing.txt" | sed 's/^/usr\/share\/aethersx2-sa\/aethersx2 entries: /'
grep -q 'usr/share/aethersx2-sa/aethersx2$' "$X/listing.txt" && bad "the image lists usr/share/aethersx2-sa/aethersx2"
echo "every path naming aethersx2:"; grep -i 'aethersx2' "$X/listing.txt" | sed 's/^squashfs-root\//  /'

echo "-- #1422: the Nova headphone Class-AB quirk (ROCKNIX #3481, 0007) in the installed UCM files"
U=usr/share/alsa/ucm2
for f in codecs/wcd938x/HeadphoneEnableSeq.conf Retroid/Nova/HeadphoneMode.conf AYN/Odin2/AYN-Odin2.conf; do
    grep -q "$U/$f\$" "$X/listing.txt" || bad "the image lists no $U/$f"
done
unsquashfs -q -d "$X/u" "$sys" "$U/codecs/wcd938x/HeadphoneEnableSeq.conf" "$U/Retroid/Nova/HeadphoneMode.conf" "$U/AYN/Odin2/AYN-Odin2.conf" > /dev/null 2>&1 \
    || { echo "cannot extract the UCM files"; exit 2; }
E=$X/u/$U/codecs/wcd938x/HeadphoneEnableSeq.conf; M=$X/u/$U/Retroid/Nova/HeadphoneMode.conf; O=$X/u/$U/AYN/Odin2/AYN-Odin2.conf
for f in "$E" "$M" "$O"; do echo "  ${f#$X/u/} sha256 $(sha256sum "$f" | cut -c1-64)"; done
grep -n 'WcdHphMode\|Include.nova\|RX HPH Mode' "$E" | sed 's/^/  HeadphoneEnableSeq.conf:/'
grep -q 'Define.WcdHphMode "CLS_H_LOHIFI"' "$E" || bad "the enable sequence does not default WcdHphMode to CLS_H_LOHIFI"
grep -q "cset \"name='RX HPH Mode' \${var:WcdHphMode}\"" "$E" || bad "the enable sequence does not set RX HPH Mode from WcdHphMode"
grep -q "cset \"name='RX HPH Mode' CLS_H_LOHIFI\"" "$E" && bad "the enable sequence still hard-codes CLS_H_LOHIFI"
grep -n 'Retroid Pocket Nova\|CLS_AB_LOHIFI' "$M" | sed 's/^/  HeadphoneMode.conf:/'
grep -q 'String2 "Retroid Pocket Nova"' "$M" && grep -q 'True.Define.WcdHphMode "CLS_AB_LOHIFI"' "$M" || bad "HeadphoneMode.conf does not set CLS_AB_LOHIFI for the Nova"
grep -n 'nova-rx-init\|rx-macro/init.conf\|Retroid Pocket Nova' "$O" | sed 's/^/  AYN-Odin2.conf:/'
grep -q 'True.Include.rx-init.File "/codecs/qcom-lpass/rx-macro/init.conf"' "$O" || bad "AYN-Odin2.conf does not include the RX macro init for the Nova"

echo "-- #1448: fex-emu built and shipped"
B=$RD/build.log; [ -f "$B" ] || B=$(ls "$RD"/*.log 2>/dev/null | head -1)
grep -E '\[DONE\] +(build|install) +fex-emu:(host|target)' "$B" | sed 's/^/  /'
grep -q -E '\[DONE\] +build +fex-emu:host' "$B" || bad "no [DONE] build fex-emu:host in $(basename "$B")"
grep -q -E '\[DONE\] +install +fex-emu:target' "$B" || bad "no [DONE] install fex-emu:target in $(basename "$B")"
for s in build_host build_target; do
    f=$(ls -d "$WT"/build.pixelelated-SM8550.aarch64/.stamps/fex-emu/$s* 2>/dev/null | head -1)
    [ -n "$f" ] && echo "  stamp $(stat -c '%y' "$f" | cut -c1-19) ${f#$WT/}" || bad "no fex-emu $s stamp"
done
grep -E 'usr/bin/FEX$|usr/lib/binfmt.d/FEX-x86(_64)?.conf$' "$X/listing.txt" | sed 's/^squashfs-root\//  /'
grep -q -E 'usr/bin/FEX$' "$X/listing.txt" || bad "the image lists no usr/bin/FEX (the interpreter)"
for c in FEX-x86 FEX-x86_64; do grep -q "usr/lib/binfmt.d/$c.conf\$" "$X/listing.txt" || bad "the image lists no usr/lib/binfmt.d/$c.conf"; done
t=$(grep -c -i 'GuestThunks' "$X/listing.txt"); echo "  GuestThunks entries: $t"
grep -i 'GuestThunks' "$X/listing.txt" | head -4 | sed 's/^squashfs-root\//  /'
[ "$t" -gt 0 ] || bad "the image lists no x86 guest thunks"

rm -rf "${X:?}"
[ "$fail" = 0 ] && echo "== all SM8550 extra reads pass" || echo "== a read failed"
exit $fail
