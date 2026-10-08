#!/bin/sh
# Synthetic UI callback fixture only. No credentials or provider network.
printf '%s\n' "$*" >> /storage/qa512/oauth-fixture.calls
case "$1" in
 serve|cancel) exit 0 ;;
 info) printf 'STATUS=waiting\nURL=http://127.0.0.1:9869/qa\nON_DEVICE=no\n' ;;
 status) echo signed-in ;;
 *) exit 2 ;;
esac
