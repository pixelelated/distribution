#!/bin/bash
# T19's stand-in for a running scan: takes the scan lock as take_lock does.
exec 9<>/var/run/raofflineproxy-scan.lock
flock -n 9 || exit 3
printf '%s\n' "$$" >&9
echo "$$" > /storage/t19/holder.pid
sleep 90
