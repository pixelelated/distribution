#!/usr/bin/env python3
"""UNRUN #577 disposable-VM command fixture; never calls NetworkManager.

The coordinator must create a fresh /storage/qa-wifi-577-* directory containing
ALLOW-SYNTHETIC-WIFI (exactly '577\n'), plan.json and state.json, and arrange a
private wifictl wrapper/bind exporting PIXELELATED_WIFI_577_DIR. No setup,
service restart, mount or cleanup is performed by this file. Credentials are
never logged or persisted, including synthetic keys passed to connect.
"""
import fcntl
import json
import os
from pathlib import Path
import sys
import time
from contextlib import contextmanager


@contextmanager
def locked(root):
    with (root / "lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def save(root, state):
    target = root / f"state.{os.getpid()}.new"
    target.write_text(json.dumps(state) + "\n")
    target.replace(root / "state.json")


def event(root, command, phase, **fields):
    with (root / "calls.jsonl").open("a") as log:
        log.write(json.dumps({"command": command, "phase": phase,
                              "pid": os.getpid(), "pgid": os.getpgrp(),
                              "time_ns": time.monotonic_ns(), **fields}) + "\n")


def escaped(value):
    return value.replace("\\", "\\\\").replace("\t", "\\t")


def main():
    root = Path(os.environ["PIXELELATED_WIFI_577_DIR"]).resolve(strict=True)
    if root.parent != Path("/storage") or not root.name.startswith("qa-wifi-577-"):
        raise ValueError("fixture requires its allocated disposable-VM directory")
    if (root / "ALLOW-SYNTHETIC-WIFI").read_text() != "577\n":
        raise ValueError("missing fixture marker")
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    # Only the SSID/profile argument is used. No key or full argv is recorded.
    name = sys.argv[2] if len(sys.argv) > 2 else ""
    with locked(root):
        plan = json.loads((root / "plan.json").read_text())
        state = json.loads((root / "state.json").read_text())
        event(root, command, "start")
        if command in ("list", "scanlist"):
            index = state.get("next_scan", 0)
            scans = plan["scans"]
            if index >= len(scans):
                event(root, command, "end", rc=2, error="unexpected-extra-scan")
                return 2
            scan = scans[index]
            delay = float(scan.get("delay", 0))
            if not 0 <= delay <= 60:
                raise ValueError("scan delay exceeds fixture bound")
            state["next_scan"] = index + 1
            save(root, state)
        else:
            scan = None

    if scan is not None:
        time.sleep(delay)
        with locked(root):
            state = json.loads((root / "state.json").read_text())
            state["view"] = scan
            save(root, state)
            rc = int(scan.get("rc", 0))
            event(root, command, "end", rc=rc, scan_index=index)
        # Nonzero scans may emit partial output; the picker must discard it.
        for ssid in scan.get("networks", []):
            print(ssid)
        return rc

    with locked(root):
        state = json.loads((root / "state.json").read_text())
        view = state.get("view", {})
        profiles = state.get("profiles", [])
        current = state.get("current", "")
        rc = 2
        if command == "saved":
            rc = int(view.get("saved_rc", 0))
            if rc == 0:
                for profile in profiles:
                    mark = "active" if profile["name"] == state.get("active_profile") else "saved"
                    print(f'{escaped(profile["name"])}\t{escaped(profile["ssid"])}\t{mark}')
        elif command == "current":
            rc = int(view.get("current_rc", 0 if current else 1))
            if rc == 0:
                print(current)
        elif command == "has_ap_mode":
            rc = 1
        elif command == "security":
            security = plan.get("security", {}).get(name, "unknown")
            print(security)
            rc = 0 if security in ("open", "protected") else 1
        elif command == "join":
            profile = next((p for p in profiles if p["name"] == name), None)
            rc = int(plan.get("join_rc", 0 if profile else 1))
            if rc == 0 and profile:
                state["current"] = profile["ssid"]
                state["active_profile"] = profile["name"]
                print("joined")
            elif rc == 0:
                rc = 1
        elif command in ("connect", "connect-open"):
            rc = int(plan.get("connect_rc", 0))
            if command == "connect-open" and (plan.get("security", {}).get(name) != "open"
                                                or plan.get("open_changed", False)):
                rc = 2
            if rc == 0:
                state["current"] = name
                state["active_profile"] = name
                if not any(p["name"] == name for p in profiles):
                    state["profiles"] = profiles + [{"name": name, "ssid": name}]
        elif command == "forget":
            rc = int(plan.get("forget_rc", 0))
            if rc == 0:
                state["profiles"] = [p for p in profiles if p["name"] != name]
                print("forgotten")
                if state.get("active_profile") == name:
                    state["current"] = ""
                    state["active_profile"] = ""
                    print("disconnected")
        save(root, state)
        event(root, command, "end", rc=rc)
        return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, ValueError, TypeError) as error:
        print("Wi-Fi fixture refused: " + type(error).__name__, file=sys.stderr)
        sys.exit(2)
