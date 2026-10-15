#!/bin/bash
set -eu
exec python3 -I -S -B "$(dirname "$0")/guest-proof.py" "$1"
