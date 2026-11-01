#!/bin/bash
# T37 (#684) stage B, G-05's host half by the second route: the payload mode needs mcopy, absent on
# this host (state-check-host.out: rc 2, input-invalid). So SYSTEM is taken from M6's artifact copy
# into the lane's scratch (gunzip, partition 1 by sfdisk's offsets, 7z for the FAT member), unsquashed
# there, and the check runs --root <tree> --mode clean-image. The artifact is read only.
set -u
I=/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz
S=/workspace/tmp/m6-t37/state; mkdir -p "$S"
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
s=$(date +%s); gunzip -c "$I" > "$S/disk.img"; rc=$?
echo "gunzip rc=$rc bytes=$(stat -c %s "$S/disk.img") wall=$(( $(date +%s)-s ))s"
sfdisk --json "$S/disk.img" > "$S/table.json"; rc=$?
read -r st sz < <(python3 -B -I -c 'import json,sys; p=json.load(open(sys.argv[1]))["partitiontable"]["partitions"][0]; print(p["start"], p["size"])' "$S/table.json")
echo "sfdisk rc=$rc partition1 start=$st size=$sz"
dd if="$S/disk.img" of="$S/part1.fat" bs=512 skip="$st" count="$sz" status=none; rc=$?
echo "dd rc=$rc"
7z l "$S/part1.fat" > "$S/part1.list" 2>&1; echo "7z list rc=$? SYSTEM entries=$(/usr/bin/grep -c -E ' SYSTEM$' "$S/part1.list")"
7z e -y -o"$S" "$S/part1.fat" SYSTEM > "$S/7z.out" 2>&1; rc=$?
echo "7z extract rc=$rc SYSTEM bytes=$(stat -c %s "$S/SYSTEM") sha256=$(sha256sum "$S/SYSTEM" | cut -d' ' -f1)"
s=$(date +%s); unsquashfs -no-xattrs -d "$S/root" "$S/SYSTEM" > "$S/unsquash.out" 2>&1; rc=$?
echo "unsquashfs rc=$rc wall=$(( $(date +%s)-s ))s files=$(find "$S/root" -xdev -type f | wc -l) errors=$(/usr/bin/grep -c -i -E 'failed|error|cannot' "$S/unsquash.out")"
/usr/bin/grep -i -E 'failed|error|cannot' "$S/unsquash.out" | sed -E 's#/workspace/tmp/m6-t37/state/root##' | sort | uniq -c | head -5
echo "BUILD_ID line: $(/usr/bin/grep -E '^BUILD_ID=' "$S/root/etc/os-release")"
s=$(date +%s); TMPDIR=/workspace/tmp/m6-t37/tmp python3 -B -I tools/pixelelated-state-check --root "$S/root" --mode clean-image > /workspace/tmp/m6-t37/tmp/state-check-root.json; rc=$?
echo "state-check --root --mode clean-image rc=$rc wall=$(( $(date +%s)-s ))s"
python3 -B -I -c 'import json,sys,collections; r=json.load(open(sys.argv[1])); print("status", r["status"], "mode", r.get("mode"), "error_count", r.get("error_count"), "checks", len(r["checks"])); print("by status", dict(collections.Counter(c["status"] for c in r["checks"]))); [print("  ", c["path"], c["category"], c["status"], "count", c.get("count")) for c in r["checks"] if c["status"] not in ("absent","clear")]; [print("  es:", c["path"], c["category"], c["status"], "count", c.get("count")) for c in r["checks"] if "emulationstation" in c["path"] and "/usr/bin" in c["path"]]' /workspace/tmp/m6-t37/tmp/state-check-root.json
