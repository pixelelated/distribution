#!/bin/bash
set -uo pipefail
ssh -i /workspace/tmp/pixelelated-524-path-refusal/guest01/qa-key -p 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes root@127.0.0.1 'set -e; ! pgrep -f '"'"'^/usr/bin/retroarch'"'"'; cloud_setup --validation-context; sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; find /storage/qa524/provider /storage/qa524/local-witness -type f -exec sha256sum '"'"'{}'"'"' '"'"';'"'"' | sort' > /workspace/tmp/pixelelated-524-path-refusal/walk-en640-invalid02/before.txt
rc=$?
if [ "$rc" = 0 ]; then
python3 /workspace/repos/rocknix/tools/vm-visual-qa --monitor /tmp/pix524-mon.sock run /workspace/tmp/pixelelated-524-path-refusal/walk-en640-invalid02/steps.txt --outdir /workspace/tmp/pixelelated-524-path-refusal/walk-en640-invalid02/frames
rc=$?
fi
ssh -i /workspace/tmp/pixelelated-524-path-refusal/guest01/qa-key -p 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes root@127.0.0.1 'set -e; ! pgrep -f '"'"'^/usr/bin/retroarch'"'"'; cloud_setup --validation-context; sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; find /storage/qa524/provider /storage/qa524/local-witness -type f -exec sha256sum '"'"'{}'"'"' '"'"';'"'"' | sort' > /workspace/tmp/pixelelated-524-path-refusal/walk-en640-invalid02/after.txt
post=$?
if [ "$post" != 0 ]; then rc=$post; fi
if ! cmp -s /workspace/tmp/pixelelated-524-path-refusal/walk-en640-invalid02/before.txt /workspace/tmp/pixelelated-524-path-refusal/walk-en640-invalid02/after.txt; then rc=1; fi
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/walk-en640-invalid02/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/walk-en640-invalid02/outer.rc
exit "$rc"
