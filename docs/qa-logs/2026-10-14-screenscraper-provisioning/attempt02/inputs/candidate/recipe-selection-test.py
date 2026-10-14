#!/usr/bin/env python3
"""Synthetic recipe selection; no compiler, provider, real credentials or device."""
import argparse
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument("--recipe", type=Path, required=True)
a = p.parse_args()
shared = "jelos"
expected = "devid=" + shared + "&devpassword=" + shared
custom = "devid=synthetic-local&devpassword=" + "synthetic-local"
script = r'''set -e
source "$1"
pre_configure_target >/dev/null
[[ "$SCREENSCRAPER_DEV_LOGIN" == "$EXPECTED" ]]
[[ "$PKG_CMAKE_OPTS_TARGET" == *"-DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1"* ]]
[[ "$(/usr/bin/env | /usr/bin/sed -n 's/^SCREENSCRAPER_DEV_LOGIN=//p')" == "$EXPECTED" ]]
'''
rows = []
for name, value, want in [("unset", None, expected), ("empty", "", expected),
                          ("explicit-shared", expected, expected),
                          ("explicit-local-override", custom, custom)]:
    env = {"PATH": "/usr/bin:/bin", "DEVICE": "GENERIC_X64", "EXPECTED": want}
    if value is not None:
        env["SCREENSCRAPER_DEV_LOGIN"] = value
    result = subprocess.run(["/bin/bash", "-c", script, "recipe-fixture", str(a.recipe)],
                            env=env, capture_output=True, timeout=10)
    rows.append({"case": name, "exit": result.returncode,
                 "empty_output": not result.stdout and not result.stderr})
    if result.returncode or result.stdout or result.stderr:
        print(json.dumps({"status": "FAIL", "cases": rows}))
        raise SystemExit(1)
print(json.dumps({"status": "PASS", "cases": rows}))
