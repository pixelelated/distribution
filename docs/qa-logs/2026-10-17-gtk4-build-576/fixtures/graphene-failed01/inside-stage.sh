#!/bin/bash
set -euo pipefail
python3 -I /build-owner/copy-cache.py
exec ./scripts/build graphene
