#!/usr/bin/env python3
"""Read/hash/source validation only; optionally emit C. No compile or execution.

Default stdout is a JSON receipt. --emit-candidate emits the derived C bytes.
No network, process launch, import of target code, or filesystem writes.
"""
import argparse
import ast
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import sys

PACKET = Path(__file__).resolve().parent
BASE_PATH = "projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c"
OLD = b"    WebKitWebContext *context =\n        webkit_web_context_new_ephemeral();\n"
NEW = b"    WebKitWebContext *context = m7_memory_policy_context();\n"
MAIN = b"int main(int argc, char **argv)\n"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--webkit-root", type=Path, required=True)
    parser.add_argument("--emit-candidate", action="store_true")
    args = parser.parse_args()
    roots = {"repo": args.repo.resolve(), "webkit": args.webkit_root.resolve()}
    manifest = json.loads((PACKET / "inputs.json").read_text())
    checked = 0
    for entry in manifest["files"]:
        path = roots[entry["root"]] / entry["path"]
        data = path.read_bytes()
        if digest(data) != entry["sha256"]:
            raise ValueError(f"source hash mismatch: {entry['root']}:{entry['path']}")
        for anchor in entry.get("anchors", []):
            if anchor.encode() not in data:
                raise ValueError(f"missing source anchor: {entry['path']}: {anchor}")
        checked += 1
    historical = json.loads((PACKET / "historical-input.json").read_text())
    archived = (roots["repo"] / historical["source_path"]).read_bytes()
    if digest(archived) != historical["source_sha256"]:
        raise ValueError("historical evidence source mismatch")
    archived_rows = json.loads(gzip.decompress(archived))
    for point in historical["points"]:
        row = min(archived_rows[point["case"]], key=lambda item: abs(item["elapsed"] - 30))
        actual = {"case": point["case"], "elapsed": row["elapsed"],
                  "MemTotal_KiB": row["mem"]["MemTotal"],
                  "WebKitWebProcess": [item for item in row["processes"]
                                       if item["exe"] == "WebKitWebProcess"]}
        if actual != point:
            raise ValueError("historical point transcription mismatch")
    baseline = (roots["repo"] / BASE_PATH).read_bytes()
    fragment = (PACKET / "context-policy.c.inc").read_bytes()
    if baseline.count(OLD) != 1 or baseline.count(MAIN) != 1:
        raise ValueError("unexpected baseline context/main structure")
    candidate = baseline.replace(MAIN, fragment + b"\n" + MAIN).replace(OLD, NEW)
    # Removing only the added helper and restoring the single call must recover
    # every byte of the original security, popup, input, and JavaScript code.
    if candidate.replace(fragment + b"\n", b"", 1).replace(NEW, OLD, 1) != baseline:
        raise ValueError("unrelated source delta")
    patch = "".join(difflib.unified_diff(
        baseline.decode().splitlines(keepends=True),
        candidate.decode().splitlines(keepends=True),
        fromfile="a/" + BASE_PATH, tofile="b/" + BASE_PATH)).encode()
    binding = json.loads((PACKET / "candidate.json").read_text())
    compressed = (PACKET / binding["patch_artifact"]).read_bytes()
    if digest(compressed) != binding["patch_gzip_sha256"]:
        raise ValueError("compressed patch hash mismatch")
    if digest(baseline) != binding["baseline_sha256"]:
        raise ValueError("baseline binding mismatch")
    stored = gzip.decompress(compressed)
    if patch != stored or digest(patch) != binding["uncompressed_patch_sha256"]:
        raise ValueError("patch bytes differ from the source transformation")
    if digest(candidate) != binding["candidate_sha256"]:
        raise ValueError("candidate hash mismatch")
    if digest(fragment) != binding["fragment_sha256"]:
        raise ValueError("fragment hash mismatch")
    ast.parse(Path(__file__).read_text(), filename=str(Path(__file__)))
    if args.emit_candidate:
        sys.stdout.buffer.write(candidate)
    else:
        print(json.dumps({"evidence": "static-source-only", "source_files": checked,
                          "baseline_sha256": digest(baseline),
                          "candidate_sha256": digest(candidate),
                          "uncompressed_patch_sha256": digest(patch),
                          "candidate_compiled": False, "runtime_executed": False}, indent=2))


if __name__ == "__main__":
    main()
