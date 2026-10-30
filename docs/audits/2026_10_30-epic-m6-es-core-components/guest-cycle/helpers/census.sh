#!/bin/bash
q=$(pgrep -c -x qemu-system-x86); c=$(( $(pgrep -x cc1plus | wc -l) + $(pgrep -x cc1 | wc -l) )); l=$(ss -Hltn 2>/dev/null | awk '{split($4,a,":"); p=a[length(a)]; if ((p>=9010 && p<=9099) || p==10022 || p==10023 || p==5909) n++} END {print n+0}')
echo "qemu $q, compilers $c, listeners (9010-9099, 10022-10023, 5909) $l"
