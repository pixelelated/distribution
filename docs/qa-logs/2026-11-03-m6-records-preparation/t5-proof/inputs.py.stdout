#!/usr/bin/env python3
"""Bind T46's frozen records metadata without reading/exporting record bodies."""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import subprocess

SOURCE = "d707c82ab8c48b674acc1f95a9571f0cb24d226a"
TREE = "b3ce6c6ea70d9d40ff2b74fff691a0a11f70e437"
ROOTS = ["docs/qa-logs", "docs/qa-frames", "docs/audits", "docs/work-logs",
         "docs/retros", "docs/retrospective", "docs/futros", "research",
         ".github/sessions", "docs/reviews/inventory.json"]
INPUTS = {
    "docs/reviews/inventory.json": "9133125cd2d28180aafdfda79668241943bf9e3d",
    "docs/reviews/areas.json": "ed033ea67c1ed0d147afbfcf1ab691aa46a5d8aa",
    "docs/reviews/slices.json": "e64965a5493ebd1da3829069e98a845a96de5b26",
    "tools/renovation-inventory": "af18e40cf8cb75496e7bb00b4059daed4792c94a",
}
EXPECTED_PATHS = "8fdb11cc06194fb1937f27d5eb7fefb70cbd5a0da0a1c6839eb1dd9fea6bf99f"
EXPECTED_META = "83198fe7208e0e4e6b70b13b0ebc78a02f54b67d18a16bd0ecfc6193ab4c6eb0"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(raw):
    rows = {}
    for row in raw.split(b"\0"):
        if not row:
            continue
        head, path = row.split(b"\t", 1)
        mode, kind, oid, size = head.split()
        if path in rows or kind != b"blob" or mode not in (b"100644", b"100755"):
            raise ValueError("duplicate key or unexpected mode/type")
        rows[path] = (mode.decode(), kind.decode(), oid.decode(), int(size))
    return rows


def digest(rows):
    return sha(b"".join(p + b"\0" + "\0".join(map(str, rows[p])).encode() + b"\0"
                        for p in sorted(rows)))


def stats(rows):
    unique = {v[2]: v[3] for v in rows.values()}
    return {"paths": len(rows), "logical_bytes": sum(v[3] for v in rows.values()),
            "unique_blobs": len(unique), "unique_blob_logical_bytes": sum(unique.values()),
            "modes": dict(sorted(collections.Counter(v[0] for v in rows.values()).items())),
            "canonical_metadata_sha256": digest(rows),
            "path_set_sha256": sha(b"".join(p + b"\0" for p in sorted(rows)))}


def check(rows, tree, inputs):
    if tree != TREE:
        raise ValueError("source root tree differs (including empty subtrees)")
    if inputs != INPUTS:
        raise ValueError("inventory/selector/generator identity differs")
    total = stats(rows)
    if total["canonical_metadata_sha256"] != EXPECTED_META or total["path_set_sha256"] != EXPECTED_PATHS:
        raise ValueError("records path/mode/type/blob/size binding differs")
    if total["paths"] != 127469 or total["logical_bytes"] != 2190843187:
        raise ValueError("records aggregate differs")
    return total


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--ref", default=SOURCE,
                    help="source object only; later execution seed is separately dispatched")
    ap.add_argument("--out", required=True, type=Path, help="new metadata-only output directory")
    args = ap.parse_args()
    receipts = []

    def git(*argv):
        import datetime
        command = ["git", "-C", str(Path(args.repo).resolve()), *argv]
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        p = subprocess.run(command, capture_output=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"))
        end = datetime.datetime.now(datetime.timezone.utc).isoformat()
        receipts.append({"argv": command, "started_at": start, "finished_at": end,
                         "exit": p.returncode, "stdout_bytes": len(p.stdout),
                         "stdout_sha256": sha(p.stdout), "stderr_bytes": len(p.stderr),
                         "stderr_sha256": sha(p.stderr)})
        if p.returncode:
            raise ValueError("Git input read failed; no record contents printed")
        return p.stdout

    commit = git("rev-parse", "--verify", args.ref + "^{commit}").decode().strip()
    tree = git("rev-parse", "--verify", args.ref + "^{tree}").decode().strip()
    inputs = parse(git("ls-tree", "-l", "-z", commit, "--", *INPUTS))
    input_oids = {p.decode(): v[2] for p, v in inputs.items()}
    rows = parse(git("ls-tree", "-r", "-l", "-z", commit, "--", *ROOTS))
    total = check(rows, tree, input_oids)
    groups = {}
    for root in ROOTS:
        rb = root.encode()
        group = {p: v for p, v in rows.items() if p == rb or p.startswith(rb + b"/")}
        groups[root] = stats(group)
    if sum(x["paths"] for x in groups.values()) != total["paths"]:
        raise ValueError("root groups not exhaustive/disjoint")
    if sum(x["logical_bytes"] for x in groups.values()) != total["logical_bytes"]:
        raise ValueError("root byte totals differ")
    args.out.mkdir(mode=0o700, parents=False, exist_ok=False)
    outputs = {"summary.json": {"source_commit": commit, "source_tree": tree, **total,
                               "input_oids": input_oids,
                               "limit": "Logical object bytes, not disk use/savings/read budget. Source cutoff precedes this output."},
               "groups.json": groups, "commands.json": receipts}
    for name, value in outputs.items():
        (args.out / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    print("PASS T46 source binding: 127469 paths / 2190843187 logical bytes / 10 roots")


if __name__ == "__main__":
    main()
