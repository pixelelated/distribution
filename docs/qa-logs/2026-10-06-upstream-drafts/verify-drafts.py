#!/usr/bin/env python3
"""Qualify #168's independent drafts against the exact cached source archive.

Usage: python3 verify-drafts.py --archive SOURCE.tar.gz --output NEW_DIRECTORY
Requires local sockets for upstream's award tests, but no provider access.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile

BASE = "879b158995d412af434301ebdae581f66b8b6d57"
ARCHIVE_SHA256 = "984957322337d1325f1b0fc11502336a80241ec511fd041c969bb0103c231664"
CASES = {
    "client-errors": ("test_linux_client_errors", ["test_linux_award_parity"]),
    "warning-sets": ("test_linux_warning_sets", ["test_linux_award_parity"]),
    "configured-login": ("test_linux_configured_login", []),
    "refresh-resilience": ("test_linux_refresh_resilience", ["test_linux_refresh_scope"]),
    "log-consent": ("test_linux_storage_corruption_retry", []),
    "image-completeness": ("test_linux_image_completeness", ["test_linux_image_cache_shutdown"]),
    "bounded-dns": ("test_linux_bounded_dns", ["test_linux_network"]),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, cwd, env, log):
    result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, timeout=30)
    log.write_text(result.stdout)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--draft", choices=CASES, action="append", help="Only selected drafts (default: all)")
    args = parser.parse_args()
    if digest(args.archive) != ARCHIVE_SHA256:
        raise SystemExit("Source archive hash mismatch")
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    pristine = out / "pristine"
    with tarfile.open(args.archive) as archive:
        for member in archive.getmembers():
            parts = Path(member.name).parts
            if len(parts) > 1 and parts[1] == "linux":
                member.name = "/".join(parts[1:])
                archive.extract(member, pristine, filter="data")
    repo = Path(__file__).resolve().parents[3]
    rows = []
    for name, (test, related) in CASES.items():
        if args.draft and name not in args.draft:
            continue
        patch = repo / "docs/upstream/raofflineproxy" / name / "fix.patch"
        parts = re.split(r"(?=^--- (?:a/|/dev/null))", patch.read_text(), flags=re.M)
        tests_only = "".join(p for p in parts if re.search(r"^\+\+\+ b/linux/tests/", p, re.M))
        if not tests_only:
            raise SystemExit(f"No regression in {name}")
        (out / (name + "-tests-only.patch")).write_text(tests_only)
        before = out / (name + "-before")
        shutil.copytree(pristine, before)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
                   RAOFFLINEPROXY_CONFIG_DIR=str(out / (name + "-config")))
        applied = run(["patch", "--batch", "--fuzz=0", "-p1", "-i", str(out / (name + "-tests-only.patch"))],
                      before, env, out / (name + "-before-apply.log"))
        if applied.returncode:
            raise SystemExit(f"Test-only patch failed: {name}")
        for source in (pristine / "linux/raofflineproxy").rglob("*.py"):
            if digest(source) != digest(before / source.relative_to(pristine)):
                raise SystemExit(f"Pristine production code changed: {name}")
        target = "linux.tests." + test
        if name == "log-consent":
            target += ".RetryStorageCorruptionReportTests.test_default_does_not_upload_unreported_incident"
        if name == "bounded-dns":
            target += ".BoundedDnsTests.test_head_does_not_attempt_connection_after_dns_failure"
        old = run(["python3", "-m", "unittest", "-v", target], before, env, out / (name + "-before.log"))
        if old.returncode != 1 or "FAILED (" not in old.stdout:
            raise SystemExit(f"Expected behavioral regression not observed: {name}")
        fixed = out / (name + "-fixed")
        shutil.copytree(pristine, fixed)
        applied = run(["patch", "--batch", "--fuzz=0", "-p1", "-i", str(patch)],
                      fixed, env, out / (name + "-fixed-apply.log"))
        if applied.returncode:
            raise SystemExit(f"Standalone patch failed: {name}")
        new = run(["python3", "-m", "unittest", "-v", *["linux.tests." + t for t in [test, *related]]],
                  fixed, env, out / (name + "-fixed.log"))
        if new.returncode or not re.search(r"\nOK\n\Z", new.stdout):
            raise SystemExit(f"Fixed tests did not pass without skips: {name}")
        row = {"draft": name, "patch_sha256": digest(patch), "before_rc": old.returncode,
               "before_summary": old.stdout.splitlines()[-1], "fixed_rc": new.returncode,
               "fixed_executions": int(re.search(r"Ran (\d+) tests", new.stdout)[1]),
               "production_unchanged_before": True}
        rows.append(row)
        print(json.dumps(row), flush=True)
    (out / "result.json").write_text(json.dumps({"base": BASE, "archive_sha256": ARCHIVE_SHA256,
                                                "drafts": rows}, indent=2) + "\n")


if __name__ == "__main__":
    main()
