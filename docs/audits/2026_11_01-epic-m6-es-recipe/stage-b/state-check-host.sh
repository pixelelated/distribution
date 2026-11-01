#!/bin/bash
# T37 (#684) stage B, G-05's host half (the coordinator's answer 2, 6551707733): the selected-state
# check, read-only, against M6's artifact copy of the candidate; TMPDIR in the lane's scratch.
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
I=/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz
df -h /workspace | tail -n 1
s=$(date +%s); sha256sum "$I" | cut -d' ' -f1; cat "$I.sha256" | cut -d' ' -f1; e=$(date +%s); echo "sha wall=$((e-s))s"
command -v sfdisk mcopy unsquashfs
s=$(date +%s); TMPDIR=/workspace/tmp/m6-t37/tmp python3 -B -I tools/pixelelated-state-check --payload "$I" > /workspace/tmp/m6-t37/tmp/state-check.json; rc=$?
e=$(date +%s); echo "state-check rc=$rc wall=$((e-s))s"
python3 -B -I -c 'import json,sys; r=json.load(open(sys.argv[1])); print("status", r["status"], "input_kind", r.get("input_kind"), "error_count", r.get("error_count"), "checks", len(r["checks"])); import collections; print("by status", dict(collections.Counter(c["status"] for c in r["checks"]))); [print("  ", c["path"], c["category"], c["status"], "count", c.get("count")) for c in r["checks"] if c["status"]!="absent"]' /workspace/tmp/m6-t37/tmp/state-check.json
ls /workspace/tmp/m6-t37/tmp | /usr/bin/grep -c '^pix-state-'
