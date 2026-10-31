#!/bin/bash
q=$(pgrep -c -x qemu-system-x86); c=$(( $(pgrep -x cc1plus | wc -l) + $(pgrep -x cc1 | wc -l) ))
echo "qemu ${q:-0}, compilers ${c:-0}"
