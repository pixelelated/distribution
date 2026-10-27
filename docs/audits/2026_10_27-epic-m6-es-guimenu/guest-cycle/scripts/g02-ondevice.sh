#!/bin/sh
# T26 (#673) G02: what cloud_oauth reports about hosting the sign-in page here. No session is started.
echo "== G02 ($(date -u +%H:%M:%SZ))"
/usr/bin/cloud_oauth info 2>&1 | grep -E '^(STATUS|ON_DEVICE|EXIT_HINT)=' ; echo "info rc $?"
W=$(grep -m1 -E '^SIGNIN_WINDOW *=' /usr/bin/cloud_oauth | sed 's/.*= *//; s/["'\'']//g'); echo "SIGNIN_WINDOW=$W"; ls -l "$W" 2>&1 | cut -c1-120
ls -d /tmp/cloud-oauth-qr.png 2>&1; command -v qrencode
echo "-- the installed browser_stack_available (cloud_oauth differs from 8ebaf8daad)"
grep -n -A4 'def browser_stack_available' /usr/bin/cloud_oauth | cut -c1-120
grep -n -E 'state\["on_device"\]' /usr/bin/cloud_oauth | cut -c1-120
