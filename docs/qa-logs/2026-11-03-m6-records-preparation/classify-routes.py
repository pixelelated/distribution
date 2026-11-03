#!/usr/bin/env python3
"""Join the coordinator's exact selectors to P1's finite retained route table."""
import argparse
import hashlib
import json
from pathlib import Path

PREFIXES = ["docs/qa-logs/", "docs/qa-frames/", "docs/audits/", "docs/work-logs/",
            "docs/retros/", "docs/retrospective/", "docs/futros/", "research/", ".github/sessions/"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packet", type=Path, default=Path(__file__).parent / "p1-routes")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    rows = json.loads((a.packet / "routes.json").read_bytes())
    metadata = json.loads((a.packet / "target-metadata.json").read_bytes())
    selected = []
    for row in rows:
        p = row.get("resolved_path")
        if p and (p == "docs/reviews/inventory.json" or
                  any(p == q.rstrip("/") or p.startswith(q) for q in PREFIXES)):
            selected.append({**row, "classification": "literal-records-route", "target": metadata[p]})
    paths = sorted({r["resolved_path"] for r in selected})
    summary = {
        "source_ref": "d707c82ab8c48b674acc1f95a9571f0cb24d226a",
        "selector_clarification": "https://github.com/pixelelated/distribution/issues/693#issuecomment-6602413967",
        "occurrences": len(selected), "targets": len(paths),
        "ordinary": sum(metadata[p].get("type") == "blob" for p in paths),
        "directories": sum(metadata[p].get("type") == "tree" for p in paths),
        "missing": sum(metadata[p].get("missing", False) for p in paths),
        "path_sha256": hashlib.sha256(b"".join(p.encode() + b"\0" for p in paths)).hexdigest(),
        "paths": paths,
        "note": "Root selector join only. Original P1 pending-classification report remains unchanged; no target body reading or link verdict.",
    }
    with a.out.open("x") as f:
        json.dump({"summary": summary, "routes": selected}, f, indent=2)
        f.write("\n")
    print(f"T46 route join: {len(selected)} occurrences / {len(paths)} targets")


if __name__ == "__main__":
    main()
