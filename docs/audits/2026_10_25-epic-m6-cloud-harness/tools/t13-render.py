#!/usr/bin/env python3
"""T13 (#660): render 02 § Assertion shapes from t13-shapes.py's JSON.

    python3 -I t13-render.py <shapes.json> <docs/vm-qa-log.md>

The generator's rule decides each row's oracle; OVERRIDES below are the
lane's hand review, each with its reason, and the rendered row says
"(reviewed)" where one applies. The recorded verdict is the newest ledger
row (a line of docs/vm-qa-log.md starting "| 20") naming the cell or its
registry's range; the single-device suite's steps share the suite's rows.
"""
import json
import re
import sys

OVERRIDES = {
    "run_steps.3": ("device report", "a round trip: the device's own restore reads the second backup back; no host read of the endpoint"),
    "run_steps.4": ("device report", "a round trip: local copies removed, the device's own restore, bytes compared on the device"),
    "run_steps.6": ("device report", "a round trip through the device's own settings backup and restore"),
    "run_steps.29": ("synthetic", "the dead-port stanza is planted (backend dead-conf); the scan's exit and rows are the device's"),
    "LINK1": ("synthetic", "the seed is checked at the endpoint (backend_sizes); the cut's verdict is the device's receiving side"),
    "A5": ("device report", "the reader is device b's own rclone (lsf, cat); FAILS by construction: APPLY calls cloud_reconcile, which has never existed (line 1771)"),
    "RETENTION": (None, "FAILS by construction (cloud_reconcile, line 2433); when nothing ran, its head-unchanged and device-copy checks PASS vacuously"),
    "prepare_device.2": (None, "setup: points the device at the QA endpoint; its one check is the device's active remote"),
}
CONTRACT = {"id": "CONTRACT", "line": 4617, "end": 5128, "claim": "#9's transport contract under the reconciler (--transport copy,bisync)",
            "checks": 16, "device_remote_reads": 3, "caps_keys": [], "oracle_rule": "both ends",
            "note": "not a registry cell: --list prints it beside PAIR; the Transport class reads the endpoint by cloud_sha (8) and backend_files/bytes (3)"}
RANGES = {"CAP": [r"CAP1-CAP14", r"CAP1-14", r"CAP1\.\.CAP14", r"capture fixtures"],
          "LINK": [r"LINK1-7", r"LINK1-LINK7", r"LINK1\.\.LINK7"],
          "KILL": [r"KILL cells"]}
SUITE = [r"round[- ]trip", r"\b10[0-9] PASS"]


def ledger_rows(path):
    rows = []
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        m = re.match(r"\| (20\d\d-\d\d-\d\d) \|", line)
        if m:
            rows.append((m.group(1), n, line))
    return rows


def newest(rows, patterns):
    hits = [(d, n, l) for d, n, l in rows if any(re.search(p, l) for p in patterns)]
    if not hits:
        return "none recorded"
    d, n, l = max(hits)
    # The row is cited, never summarised: a ledger row's free text carries
    # other cells' and suites' words, so a PASS/FAIL read off it is a claim.
    return "named %s (`vm-qa-log.md:%d`; %d row(s))" % (d, n, len(hits))


def main():
    data = json.load(open(sys.argv[1]))
    rows = ledger_rows(sys.argv[2])
    out = []
    head = "| Row | Lines | Claim | Oracle | Device-rclone reads | `check()` | `caps()` | Recorded verdict | Note | proved: |"
    out.append(head)
    out.append("| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |")
    counts = {}
    suite_verdict = ("2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` "
                     "(`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`)")
    entries = data["rows"] + [dict(CONTRACT, kind="extra")]
    for r in entries:
        rid = r["id"]
        oracle, note = OVERRIDES.get(rid, (None, r.get("note", "")))
        if rid.startswith(("LINK", "KILL")) and r["checks"] == 0:
            note = (note + "; " if note else "") + "its checks are Link.exercise's, shared by every LINK cell"
        o = oracle or r["oracle_rule"]
        reviewed = " (reviewed)" if rid in OVERRIDES and oracle else ""
        counts[o] = counts.get(o, 0) + (0 if r.get("kind") == "extra" else 1)
        if r.get("kind") == "step":
            verdict = "the suite's: " + suite_verdict
        else:
            prefix = re.match(r"[A-Z]+", rid).group(0)
            pats = [r"\b%s\b" % re.escape(rid)] + RANGES.get(prefix, [])
            verdict = newest(rows, pats)
        caps = ", ".join(r.get("caps_keys") or []) or "not read"
        claim = r["claim"].strip("'\"").replace("|", "\\|")
        out.append("| `%s` | %d-%d | %s | %s%s | %d | %d | %s | %s | %s | tree |" % (
            rid, r["line"], r["end"], claim[:150], o, reviewed, r.get("device_remote_reads", 0),
            r["checks"], caps, verdict, note.replace("|", "\\|")))
    print("\n".join(out))
    print()
    print("Rows: %d (34 steps + 44 cells) + `CONTRACT` = %d. By oracle over the 78: %s." % (
        len(data["rows"]), len(data["rows"]) + 1,
        ", ".join("%s %d" % (k, v) for k, v in sorted(counts.items()))))


if __name__ == "__main__":
    main()
