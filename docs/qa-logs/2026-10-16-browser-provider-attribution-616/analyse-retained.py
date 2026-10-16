#!/usr/bin/env python3
"""Read retained #570 samples; emit a source-bound summary, without a runtime test."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, required=True)
args = parser.parse_args()
packet = args.repo / "docs/qa-logs/2026-10-13-dropbox-user-agents"
inputs = {}


def read(name):
    path = packet / name
    data = path.read_bytes()
    inputs[str(path.relative_to(args.repo))] = hashlib.sha256(data).hexdigest()
    return json.loads(gzip.decompress(data) if name.endswith(".gz") else data)


samples = read("samples.json.gz")
analysis = read("analysis.json")
script_sets = read("script-sets.json")
browser_exes = {"cloud-signin-window", "WebKitWebProcess", "WebKitNetworkProcess"}
rows = []
for original in analysis:
    name = original["name"]
    live = []
    for sample in samples[name]:
        processes = [p for p in sample["processes"] if p["exe"] in browser_exes]
        if any(p["exe"] == "cloud-signin-window" for p in processes):
            live.append((sum(p["pss"] for p in processes), sample, processes))
    assert live, name
    total, peak_sample, peak_processes = max(live, key=lambda row: row[0])
    assert abs(total / 1024 - original["peak_browser_pss_mib"]) < 1e-6, name
    by_process = {}
    for exe in sorted(browser_exes):
        selected = [p for p in peak_processes if p["exe"] == exe]
        by_process[exe] = {
            "pss_mib": sum(p["pss"] for p in selected) / 1024,
            "anonymous_mib": sum(p["anon"] for p in selected) / 1024,
        }
    def counter_delta(key):
        return samples[name][-1]["vmstat"][key] - samples[name][0]["vmstat"][key]
    families = sorted({"fallback" if "rspb_fallback/" in url else "modern"
                       for url in script_sets[name] if "oauth2_authorize_page_rspb_" in url})
    rows.append({
        "case": name,
        "peak_browser_pss_mib": total / 1024,
        "peak_sample_elapsed_s": peak_sample["elapsed"],
        "at_peak": by_process,
        "max_heartbeat_gap_ms": original["max_heartbeat_ms"],
        "page_load_ms": original["load_ms"],
        "bundle_families": families,
        "whole_observer_window_direct_scan_pages": counter_delta("pgscan_direct"),
        "whole_observer_window_file_refaults": counter_delta("workingset_refault_file"),
        "whole_observer_window_allocation_stalls": sum(counter_delta(k) for k in
            samples[name][0]["vmstat"] if k.startswith("allocstall_")),
    })

print(json.dumps({
    "issue": 616,
    "type": "reanalysis_of_existing_october13_evidence_not_new_runtime",
    "input_sha256": inputs,
    "limits": [
        "1280 MiB assigned / 1042.625 MiB visible, software VM, no proxy service; not H700 or 1 GiB results",
        "Per-process attribution is at the aggregate browser PSS peak; peaks of individual processes may differ",
        "Anonymous process memory includes more than JavaScript; no script CPU/heap attribution or leak established",
        "Reclaim counters cover the whole observer window including startup and return, not only page stalls",
        "Heartbeat maximum is cumulative; page metrics and process sampler do not supply an exact common event clock here",
        "Cookie overlay obscures the form; no authentication or input-to-paint proof",
        "Two observations per UA, uncontrolled live-provider/network variation and unisolated observer overhead",
    ],
    "cases": rows,
}, indent=2, sort_keys=True))
