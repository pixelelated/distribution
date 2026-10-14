#!/usr/bin/env python3
"""Prepare two small, source-bound trees. Does not import or start the proxy."""
import argparse
import ast
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tarfile

PIN = "c7ebd1b6e777f3751ff0ecdf8aba54045844e00d"
ARCHIVE_SHA256 = "88eef31acfa4104b20258bd5cea514ade30e6cdf35767ffc958009851d61898b"
PACKET = Path(__file__).resolve().parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*.py"))}


def apply(root, patch):
    artifact = patch.read_bytes()
    payload = gzip.decompress(artifact) if patch.suffix == ".gz" else artifact
    name = patch.stem if patch.suffix == ".gz" else patch.name
    digest = hashlib.sha256(payload).hexdigest()
    if patch.suffix == ".gz":
        expected, expected_name = patch.with_suffix(".sha256").read_text().split()
        assert (digest, name) == (expected, expected_name), "compressed patch identity mismatch"
    result = subprocess.run(
        ["patch", "--batch", "--fuzz=0", "-p1"], input=payload,
        cwd=root, capture_output=True, timeout=15,
    )
    stdout, stderr = result.stdout.decode(), result.stderr.decode()
    if result.returncode or re.search(r"fuzz|FAILED|Reversed", stdout):
        raise RuntimeError(stdout + stderr)
    evidence = {"name": name, "sha256": digest, "output": stdout}
    if patch.suffix == ".gz":
        evidence.update(artifact_name=patch.name, artifact_sha256=sha(patch), encoding="gzip")
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new directory")
    args = parser.parse_args()
    package = args.repo.resolve() / "projects/ROCKNIX/packages/network/raofflineproxy"
    recipe = (package / "package.mk").read_text()
    assert f'PKG_VERSION="{PIN}"' in recipe
    assert f'PKG_SHA256="{ARCHIVE_SHA256}"' in recipe
    assert sha(args.archive) == ARCHIVE_SHA256, "wrong source archive"
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    baseline = output / "baseline"
    baseline.mkdir()
    # Extract only Python source and tests, never links, binary assets or bundles.
    total = 0
    with tarfile.open(args.archive) as archive:
        for member in archive:
            parts = PurePosixPath(member.name).parts
            if not parts or parts[0] != f"RAOfflineProxy-{PIN}":
                raise ValueError("unexpected archive root")
            rel = PurePosixPath(*parts[1:])
            if ".." in rel.parts or rel.is_absolute():
                raise ValueError("unsafe archive path")
            if not (member.isfile() and rel.suffix == ".py" and
                    (str(rel).startswith("linux/raofflineproxy/") or
                     str(rel).startswith("linux/tests/"))):
                continue
            total += member.size
            assert total < 10 * 1024 * 1024, "source budget exceeded"
            target = baseline / str(rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    upstream = manifest(baseline)
    patches = [apply(baseline, p) for p in sorted((package / "patches").glob("*.patch"))]
    candidate = output / "candidate"
    shutil.copytree(baseline, candidate)
    candidate_patch = apply(candidate, PACKET / "lazy-ui-imports.patch.gz")
    original, changed = manifest(baseline), manifest(candidate)
    assert [p for p in original if original[p] != changed[p]] == ["linux/raofflineproxy/main.py"]
    for root in (baseline, candidate):
        for path in root.rglob("*.py"):
            ast.parse(path.read_bytes(), filename=str(path))
    report = {
        "evidence_level": "source preparation and syntax only; no proxy execution",
        "pin": PIN, "archive_sha256": ARCHIVE_SHA256,
        "recipe_sha256": sha(package / "package.mk"),
        "extracted_bytes": total, "patches": patches, "candidate_patch": candidate_patch,
        "upstream": upstream, "baseline": original, "candidate": changed,
    }
    (output / "source.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"result": "PASS", "patches": len(patches), "source_bytes": total,
                      "manifest": str(output / "source.json")}))


if __name__ == "__main__":
    main()
