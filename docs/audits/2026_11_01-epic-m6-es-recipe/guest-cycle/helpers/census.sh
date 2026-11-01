#!/bin/bash
# T37 (#684): the census by the kernel's 15-character process names (qemu-system-x86_64 is
# qemu-system-x86 in comm; a pattern of the full name never matches -- the stage-A/B correction).
q=$(pgrep -c -x qemu-system-x86); c=$(( $(pgrep -x cc1plus | wc -l) + $(pgrep -x cc1 | wc -l) ))
echo "qemu ${q:-0}, compilers ${c:-0}"
