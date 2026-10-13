#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""Compile the #576 API fixture only. Never execute the resulting program.

Caller supplies a correctly isolated compiler/pkg-config environment. There is
no package install, download, fallback to another version, or cache mutation.
"""
import argparse
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys


def run_bounded(command, *, timeout, capture_output=False, check=False):
    """Run in a private POSIX group; kill the group and reap its leader on error.

    The coordinator's outer runner still owns escaped groups, forced termination
    of this script, and teardown if the five-second reap deadline fails. Other
    group members are reaped by their parents or the environment's init/reaper.
    """
    process = subprocess.Popen(
        command, start_new_session=True, text=True,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE if capture_output else None,
    )
    try:
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            result = subprocess.CompletedProcess(
                command, process.returncode, stdout, stderr)
            if check:
                result.check_returncode()
            return result
        except BaseException:
            try:
                try:
                    # Do not skip this when the leader has exited: descendants
                    # may still hold captured pipes open in the original group.
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass  # The entire group has already gone away.
                finally:
                    # Wait even when signalling fails, and reap the direct child.
                    # Do not communicate() again: escaped descendants could keep
                    # a pipe open indefinitely. Close our read ends below instead.
                    process.wait(timeout=5)
            except (OSError, subprocess.TimeoutExpired) as cleanup_error:
                raise subprocess.SubprocessError(
                    f"cleanup failed for process group {process.pid}; "
                    f"coordinator must tear down the allocated job: {cleanup_error}"
                ) from cleanup_error
            raise
    finally:
        for pipe in (process.stdout, process.stderr):
            if pipe is not None:
                pipe.close()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cc", default="cc", help="compiler executable, no shell expression")
    p.add_argument("--pkg-config", default="pkg-config")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    for module, expected in (("gtk4", "4.24.1"), ("webkitgtk-6.0", "2.54.1")):
        result = run_bounded([args.pkg_config, "--modversion", module],
                             capture_output=True, timeout=15)
        if result.returncode or result.stdout.strip() != expected:
            print(f"BLOCKED: {module} must resolve to {expected}; "
                  f"pkg-config rc={result.returncode}, version={result.stdout.strip()!r}")
            print(result.stderr.strip())
            return 2
    result = run_bounded([args.pkg_config, "--cflags", "--libs", "gtk4", "webkitgtk-6.0"],
                         capture_output=True, check=True, timeout=15)
    source = Path(__file__).resolve().with_name("api-smoke.c")
    args.output.parent.resolve(strict=True)
    # Exclusive creation prevents this fixture replacing an existing binary.
    fd = os.open(args.output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    command = [args.cc, "-Wall", "-Wextra", "-Werror=implicit-function-declaration",
               "-Werror=incompatible-pointer-types", str(source), "-o", str(args.output),
               *shlex.split(result.stdout), "-latomic"]
    try:
        run_bounded(command, check=True, timeout=60)
    except BaseException:
        args.output.unlink(missing_ok=True)
        raise
    print("COMPILED (NOT RUN): " + str(args.output))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError) as error:
        print("compile probe failed: " + str(error), file=sys.stderr)
        sys.exit(1)
