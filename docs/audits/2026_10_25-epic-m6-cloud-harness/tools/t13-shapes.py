#!/usr/bin/env python3
"""T13 (#660): the assertion-shape table's skeleton, generated from
tools/cloud-round-trip's AST and registry literals at a named revision.

    python3 -I t13-shapes.py <path to cloud-round-trip> [--json out.json]

Rows: one per step() in run_steps and prepare_device (each step's span runs
to the next step() or the function's end), one per registry cell (the
fixture function's body, plus the bodies of module-level functions it calls
directly, one level). Per row: the check() count, the endpoint reads
(backend(...) calls by subcommand, epath()), the device commands (.run(),
.run_ok()), the synthetic-input markers, and the caps() keys read.

The oracle column is a rule, with this precedence, and the lane reviews every
row by hand in 02 § Assertion shapes:
  both ends     -- the span reads the endpoint from the host: backend('ls'),
                   backend('cat'), ... or a host run of the tool
                   ([BACKEND, 'cat', ...]); epath() alone is not a read
  synthetic     -- otherwise, the span plants its condition (a stub on PATH,
                   a held lock, a kill, a link or power cut, a put at the
                   endpoint, a config edited under the scripts) and reads
                   the device's reaction
  device report -- otherwise: the device's own exit code, output, log, stamp
                   or file, including a round trip through its own restore
Two method calls the one-level fold cannot reach are read by name: a
Pair's .cloud_sha(...) is backend_bytes(), a host cat of the endpoint; a
Link's (or Kill's) .exercise(key, cmd, marker, receiving, ...) reads its
receiving side from the host when that is ("cloud", ...) and from the device
when it is ("device", ...), and its condition is always a link cut.
A separate count, device_remote_reads, is the device's own rclone listing or
reading the remote (rclone lsf/ls/lsl/lsjson/cat/check/size on the guest):
it reads the other end, but through the client under test.

It asserts the counts it was written against (32 + 2 steps, 44 cells:
PAIR 10, SOLO 1, CAP 14, LINK 7, KILL 12) and exits 1 on a delta, printing
the delta, so a later reader re-running it on another revision sees the
table's premise break rather than a shorter table.
"""
import ast
import json
import sys

EXPECT_STEPS = {"run_steps": 32, "prepare_device": 2}
EXPECT_CELLS = {"PAIR_FIXTURES": 10, "SOLO_FIXTURES": 1, "CAPTURE_FIXTURES": 14,
                "LINK_FIXTURES": 7, "KILL_FIXTURES": 12}
ENDPOINT_SUBCOMMANDS = {"cat", "ls", "lsjson", "lsf", "path", "put", "reset",
                        "seed-content", "seed-device", "caps", "endpoint-prefix",
                        "saves-remote", "shipped-default", "rclone-conf"}
ENDPOINT_READS = {"cat", "ls", "lsjson", "lsf", "path", "exercise:cloud"}
SYNTHETIC_HINTS = ("stub", "PATH=", "fake", "plant", "/sbin/ip", "printf '#!/bin/sh",
                   "chmod +x", "truncate", "dd if=", ": >", "poison", "flock",
                   "kill", "sendkey", "rclone copyto", "rclone purge", "sed -i")
import re
DEVICE_REMOTE_READ = re.compile(r"rclone (lsf|ls|lsl|lsjson|lsd|cat|check|size|md5sum|sha1sum|hashsum)\b")


def call_name(node):
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def first_str(node):
    for a in node.args:
        if isinstance(a, ast.Constant) and isinstance(a.value, str):
            return a.value
        if isinstance(a, ast.JoinedStr):
            return ast.unparse(a)
    return None


def measure(nodes, fns, depth=1, seen=None):
    """Counts over a flat list of AST nodes (each counted once); module
    functions called directly are folded in once (depth 1), so a helper that
    reads the endpoint counts."""
    seen = set() if seen is None else seen
    m = {"checks": 0, "endpoint": {}, "epath": 0, "device_runs": 0, "device_remote_reads": 0,
         "caps_keys": set(), "synthetic": set(), "helpers": set()}
    for n in nodes:
        if True:
            if isinstance(n, ast.Call):
                name = call_name(n)
                if name == "check":
                    m["checks"] += 1
                elif name == "backend":
                    sub = first_str(n) or "?"
                    m["endpoint"][sub] = m["endpoint"].get(sub, 0) + 1
                elif name == "epath":
                    m["epath"] += 1
                elif name == "cloud_sha" and isinstance(n.func, ast.Attribute):
                    m["endpoint"]["cat"] = m["endpoint"].get("cat", 0) + 1
                elif name == "exercise" and isinstance(n.func, ast.Attribute):
                    recv = n.args[3] if len(n.args) > 3 else next((k.value for k in n.keywords if k.arg == "receiving"), None)
                    side = recv.elts[0].value if isinstance(recv, ast.Tuple) and recv.elts and isinstance(recv.elts[0], ast.Constant) else "?"
                    m["endpoint"]["exercise:" + side] = m["endpoint"].get("exercise:" + side, 0) + 1
                    m["synthetic"].add("link cut")
                elif name in ("run", "run_ok", "sh", "ssh") and isinstance(n.func, ast.Attribute):
                    m["device_runs"] += 1
                    a0 = n.args[0] if n.args else None
                    if isinstance(a0, (ast.Constant, ast.JoinedStr)) and DEVICE_REMOTE_READ.search(ast.unparse(a0)):
                        m["device_remote_reads"] += 1
                # a host run of the backend tool: [BACKEND, '<sub>', ...]
                for a in n.args:
                    if isinstance(a, ast.List) and len(a.elts) >= 2 and isinstance(a.elts[0], ast.Name) \
                            and a.elts[0].id == "BACKEND" and isinstance(a.elts[1], ast.Constant):
                        sub = a.elts[1].value
                        m["endpoint"][sub] = m["endpoint"].get(sub, 0) + 1
                if name == "backend" or any(isinstance(a, ast.List) and a.elts and isinstance(a.elts[0], ast.Name)
                                            and a.elts[0].id == "BACKEND" for a in n.args):
                    if "put" in m["endpoint"]:
                        m["synthetic"].add("put at the endpoint")
                if isinstance(n.func, ast.Name) and n.func.id in fns and n.func.id not in seen and depth > 0:
                    seen.add(n.func.id)
                    m["helpers"].add(n.func.id)
                    sub = measure(list(ast.walk(fns[n.func.id]))[1:], fns, depth - 1, seen)
                    m["checks"] += sub["checks"]
                    for k, v in sub["endpoint"].items():
                        m["endpoint"][k] = m["endpoint"].get(k, 0) + v
                    m["epath"] += sub["epath"]
                    m["device_runs"] += sub["device_runs"]
                    m["device_remote_reads"] += sub["device_remote_reads"]
                    m["caps_keys"] |= sub["caps_keys"]
                    m["synthetic"] |= sub["synthetic"]
            if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Call) and call_name(n.value) == "caps":
                if isinstance(n.slice, ast.Constant):
                    m["caps_keys"].add(n.slice.value)
            if isinstance(n, ast.Call) and call_name(n) == "get" and isinstance(n.func, ast.Attribute) \
                    and isinstance(n.func.value, ast.Call) and call_name(n.func.value) == "caps":
                k = first_str(n)
                if k:
                    m["caps_keys"].add(k)
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                for h in SYNTHETIC_HINTS:
                    if h in n.value:
                        m["synthetic"].add(h)
    return m


def oracle(m):
    if any(k in ENDPOINT_READS for k in m["endpoint"]):
        return "both ends"
    if m["synthetic"]:
        return "synthetic"
    return "device report"


def row(kind, ident, line, end, claim, m):
    return {"kind": kind, "id": ident, "line": line, "end": end, "claim": claim,
            "checks": m["checks"], "endpoint": dict(sorted(m["endpoint"].items())),
            "epath": m["epath"], "device_runs": m["device_runs"],
            "device_remote_reads": m["device_remote_reads"],
            "caps_keys": sorted(m["caps_keys"]), "synthetic": sorted(m["synthetic"]),
            "helpers": sorted(m["helpers"]), "oracle_rule": oracle(m)}


def main():
    path = sys.argv[1]
    out_json = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    tree = ast.parse(open(path, encoding="utf-8").read())
    fns = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    rows, deltas = [], []

    for fname, want in EXPECT_STEPS.items():
        fn = fns[fname]
        body = fn.body
        # step() calls are statements (Expr) at any depth; spans run between them
        marks = sorted((n.lineno, n) for n in ast.walk(fn)
                       if isinstance(n, ast.Call) and call_name(n) == "step")
        if len(marks) != want:
            deltas.append("%s: %d step() calls, expected %d" % (fname, len(marks), want))
        bounds = [ln for ln, _ in marks] + [fn.end_lineno + 1]
        nodes = [n for n in ast.walk(fn) if n is not fn and hasattr(n, "lineno")]
        for i, (ln, call) in enumerate(marks):
            lo, hi = ln, bounds[i + 1] - 1
            inside = [n for n in nodes if lo <= n.lineno <= hi]
            title = ast.unparse(call.args[0]) if call.args else "?"
            rows.append(row("step", "%s.%d" % (fname, i + 1), lo, hi, title, measure(inside, fns)))

    for reg, want in EXPECT_CELLS.items():
        node = next(n for n in tree.body if isinstance(n, ast.Assign)
                    and isinstance(n.targets[0], ast.Name) and n.targets[0].id == reg)
        elts = node.value.elts
        if len(elts) != want:
            deltas.append("%s: %d cells, expected %d" % (reg, len(elts), want))
        for e in elts:
            ident = e.elts[0].value
            desc = ast.literal_eval(e.elts[1])
            fx = e.elts[2].id
            fn = fns[fx]
            rows.append(row("cell:" + reg.split("_")[0], ident, fn.lineno, fn.end_lineno, desc,
                            measure(list(ast.walk(fn))[1:], fns, seen={fx})))

    steps = sum(1 for r in rows if r["kind"] == "step")
    cells = len(rows) - steps
    summary = {"steps": steps, "cells": cells, "rows": len(rows),
               "by_oracle_rule": {k: sum(1 for r in rows if r["oracle_rule"] == k)
                                  for k in ("both ends", "device report", "synthetic")},
               "deltas": deltas}
    if out_json:
        with open(out_json, "w") as fh:
            json.dump({"source": path, "summary": summary, "rows": rows}, fh, indent=1)
    print(json.dumps(summary))
    for r in rows:
        print("%-22s %5d-%-5d checks=%-3d endpoint=%s devremote=%d caps=%s synth=%s rule=%s | %s" % (
            r["id"], r["line"], r["end"], r["checks"], r["endpoint"], r["device_remote_reads"],
            ",".join(r["caps_keys"]) or "-", ",".join(r["synthetic"]) or "-", r["oracle_rule"],
            r["claim"][:70]))
    return 1 if deltas else 0


if __name__ == "__main__":
    sys.exit(main())
