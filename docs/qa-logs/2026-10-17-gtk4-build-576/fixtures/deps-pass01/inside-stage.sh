#!/bin/bash
set -euo pipefail
case "$1" in gtk4|libseccomp|bubblewrap|xdg-dbus-proxy) exec ./scripts/build "$1";; *) exit 64;; esac
