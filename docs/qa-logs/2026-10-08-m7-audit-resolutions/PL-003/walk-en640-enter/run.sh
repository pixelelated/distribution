#!/bin/bash
set -uo pipefail
ssh -i /workspace/tmp/pixelelated-524-path-refusal/guest01/qa-key -p 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes root@127.0.0.1 'set -e; ! pgrep -f '"'"'^/usr/bin/retroarch'"'"'; cloud_setup --validation-context; sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; find /storage/qa524/provider /storage/qa524/local-witness -type f -exec sha256sum '"'"'{}'"'"' '"'"';'"'"' | sort' > /workspace/tmp/pixelelated-524-path-refusal/walk-en640-enter/before.txt
rc=$?
if [ "$rc" = 0 ]; then
python3 /workspace/repos/rocknix/tools/vm-visual-qa --monitor /tmp/pix524-mon.sock run /workspace/tmp/pixelelated-524-path-refusal/walk-en640-enter/steps.txt --outdir /workspace/tmp/pixelelated-524-path-refusal/walk-en640-enter/frames
rc=$?
fi
ssh -i /workspace/tmp/pixelelated-524-path-refusal/guest01/qa-key -p 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes root@127.0.0.1 'set -e; ! pgrep -f '"'"'^/usr/bin/retroarch'"'"'; cloud_setup --validation-context; sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; find /storage/qa524/provider /storage/qa524/local-witness -type f -exec sha256sum '"'"'{}'"'"' '"'"';'"'"' | sort' > /workspace/tmp/pixelelated-524-path-refusal/walk-en640-enter/after.txt
post=$?
if [ "$post" != 0 ]; then rc=$post; fi
if ! cmp -s /workspace/tmp/pixelelated-524-path-refusal/walk-en640-enter/before.txt /workspace/tmp/pixelelated-524-path-refusal/walk-en640-enter/after.txt; then rc=1; fi
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/walk-en640-enter/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/walk-en640-enter/outer.rc
exit "$rc"
