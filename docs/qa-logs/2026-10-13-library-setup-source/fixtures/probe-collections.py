#!/usr/bin/env python3
"""UNRUN read-only guest probe; coordinator stages one collections.json case.

No service control, settings writes, game launch, account use, or cleanup.
Only the named output is written. Supply a compiled-binary identity from the
coordinator's build receipt: a source string alone does not bind a binary.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

SOURCE = "6b1dd68246c89f4c1c0fa17c3d8941ffd3b3d420"
SETTINGS = Path("/storage/.config/emulationstation/es_settings.cfg")
ROM_NAME = "pixelelated-library-setup.gb"


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def binary_digest(path):
    with path.open("rb") as binary:
        return hashlib.file_digest(binary, "sha256").hexdigest()


def fetch(path):
    # Never inherit an environment HTTP proxy for a guest-local query.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open("http://127.0.0.1:1234" + path, timeout=3) as response:
            raw = response.read(1024 * 1024 + 1)
            require(len(raw) <= 1024 * 1024, "oversized API response")
            return response.status, json.loads(raw)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return 404, None
        raise RuntimeError("unexpected API status") from None


def settings_selection():
    # ES accepts both a config root and legacy top-level setting elements.
    text = SETTINGS.read_text(encoding="utf-8-sig")
    text = re.sub(r"^\s*<\?xml[^?]*\?>", "", text, count=1)
    doc = ET.fromstring("<fixture>" + text + "</fixture>")
    roots = list(doc)
    root = roots[0] if len(roots) == 1 and roots[0].tag == "config" else doc
    matches = [node for node in root if node.get("name") == "CollectionSystemsAuto"]
    require(len(matches) <= 1, "duplicate collection preference")
    if not matches:
        return None
    require(matches[0].tag == "string" and "value" in matches[0].attrib,
            "malformed collection preference")
    return matches[0].get("value")


def fixture_rows(rows):
    require(isinstance(rows, list), "games response is not a list")
    require(all(isinstance(row, dict) for row in rows), "malformed game row")
    return [row for row in rows if str(row.get("path", "")).endswith("/" + ROM_NAME)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True)
    parser.add_argument("--pid", type=int, required=True)
    parser.add_argument("--boot-id", required=True)
    parser.add_argument("--binary-sha256", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), "output already exists")
    spec = json.loads(Path(__file__).with_name("collections.json").read_text())
    require(spec["source_commit"] == SOURCE, "fixture source mismatch")
    cases = {case["id"]: case for case in spec["cases"]}
    require(args.case in cases, "unknown case")
    case = cases[args.case]
    report = {"source_commit": SOURCE, "case": args.case, "rc": 1,
              "scope": "synthetic collection membership; no gameplay or upgrade proof"}
    try:
        require(re.fullmatch(r"[0-9a-f]{64}", args.binary_sha256) is not None,
                "invalid expected binary identity")
        require(Path("/proc/sys/kernel/random/boot_id").read_text().strip() == args.boot_id,
                "boot identity mismatch")
        require(args.pid > 1, "invalid frontend PID")
        exe = Path("/proc") / str(args.pid) / "exe"
        require(exe.resolve().name == "emulationstation", "unexpected frontend executable")
        actual = binary_digest(exe)
        require(actual == args.binary_sha256, "running binary identity mismatch")
        report.update(boot_id=args.boot_id, pid=args.pid, binary_sha256=actual)
        require(fetch("/isIdle") == (200, [True]), "frontend not idle")

        selected = settings_selection()
        # ES may omit a saved value equal to its compiled default. Other saved
        # choices, including the inherited spaced form, must remain exact.
        allowed = [case["selection"]]
        if case["selection"] == spec["compiled_default"]:
            allowed = [None, spec["compiled_default"]]
        require(selected in allowed, "saved collection choice changed")

        status, systems = fetch("/systems")
        require(status == 200 and isinstance(systems, list), "systems API unavailable")
        require(all(isinstance(row, dict) for row in systems), "malformed system row")
        names = [row.get("name") for row in systems]
        code, games = fetch("/systems/gb/games")
        require(code == 200, "fixture system absent")
        rows = fixture_rows(games)
        require(len(rows) == 1 and len(games) == 1, "requires one isolated GB fixture")
        require(int(rows[0].get("playcount", "0")) == (5 if case["history"] else 0),
                "fixture playcount mismatch")
        last = str(rows[0].get("lastplayed", "0"))
        require(last == "20260908T031024" if case["history"] else last in ("", "0"),
                "fixture lastplayed mismatch")
        report["collections"] = {}
        for name in ("favorites", "recent"):
            expected = case[name + "_status"]
            code, collection = fetch("/systems/" + name + "/games")
            require(code == expected, name + " HTTP status mismatch")
            require((name in names) == (expected == 200), name + " systems membership mismatch")
            found = fixture_rows(collection) if code == 200 else []
            require(len(found) == (1 if expected == 200 and case["history"] else 0),
                    name + " fixture membership mismatch")
            if code == 200:
                require(len(collection) == len(found), "unexpected collection data")
            report["collections"][name] = {"http_status": code, "fixture_count": len(found)}
        if case["selection"] == "all":
            code, all_games = fetch("/systems/all/games")
            require(code == 200 and len(fixture_rows(all_games)) == 1,
                    "retained all-games choice missing")
        require(fetch("/isIdle") == (200, [True]), "frontend lost readiness")
        require(binary_digest(exe) == actual,
                "frontend changed during observation")
        report.update(rc=0, saved_choice_preserved=True)
    except Exception as error:
        # Do not print settings, response bodies, or exception values.
        report["failure_type"] = type(error).__name__
        if type(error) is RuntimeError:
            report["failure"] = str(error)  # only the fixed labels above
    with args.out.open("x", encoding="utf-8") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(("PASS " if report["rc"] == 0 else "FAIL ") + args.case)
    return report["rc"]


if __name__ == "__main__":
    raise SystemExit(main())
