"""Passive readiness and bounded save readback for the one selected guest."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import time

WORK = Path("/tmp/m7-1433-armed-result")
INPUT = Path("/tmp/m7-1433-armed-input")
sys.path.insert(0, str(INPUT))
import menu_timing as T
OUT = Path("/tmp/m7-1433-owner-file-originals")
ROM = "/storage/roms/gb/ExitProbe.gb"
SAVE = "gb/ExitProbe.srm"
BOOT = Path("/proc/sys/kernel/random/boot_id")
PREFIX = "M7_EXIT_CPU="
TRACE_LIMIT = 2 * 1024**2
LIVE = Path("/tmp/m7-1433-owner-live-originals")
STAMPS = Path("/storage/.cache/cloud_sync")
STAMP_NAMES = ("last-capture", "last-backup", "last-sync-exit")



def emit(record):
    print(PREFIX + json.dumps(record, separators=(",", ":")), flush=True)


def traced_game():
    trace = WORK / "child-originals.jsonl"
    if not trace.is_file():
        return None
    with trace.open("rb") as stream:
        raw = stream.read(TRACE_LIMIT + 1)
    if len(raw) > TRACE_LIMIT:
        raise ValueError("trace limit")
    found = []
    for line in raw.split(b"\n")[:-1]:
        row = json.loads(line)
        if row["event"] == "exec" and row["role"] == "retroarch":
            found.append(row)
    if len(found) > 1:
        raise ValueError("multiple traced RetroArch executions")
    if not found:
        return None
    row = found[0]
    argv = row["argv"]
    if (row["exe"] != "/usr/bin/retroarch" or argv.count(ROM) != 1
            or argv.count("-L") != 1 or argv[argv.index("-L") + 1] != "/tmp/cores/gambatte_libretro.so"):
        raise ValueError("wrong traced cartridge/core")
    return row["pid"], row["start_ticks"]


def proc_ticks(pid, start):
    path = Path("/proc") / str(pid)
    fields = (path / "stat").read_text().rsplit(") ", 1)[1].split()
    if (int(fields[19]) != start or fields[0] in {"Z", "X", "x"}
            or not (path / "exe").samefile("/usr/bin/retroarch")):
        raise ValueError("traced emulator generation changed")
    return int(fields[11]) + int(fields[12])


def readiness():
    cutoff = time.monotonic() + T.ARM_SETUP + T.STARTUP + 2
    while time.monotonic() < cutoff:
        game = traced_game()
        if game is not None:
            break
        if (WORK / "result.json").exists():
            raise ValueError("armed case returned with no traced game")
        time.sleep(.125)
    else:
        raise ValueError("traced game not present in startup window")
    pid, start = game
    samples = []
    for _ in range(40):
        ticks = proc_ticks(pid, start)
        samples.append([time.monotonic_ns(), ticks])
        if ticks >= 200 or (sum(row[1] > 0 for row in samples) >= 4 and ticks >= 30):
            break
        time.sleep(1)
    else:
        raise ValueError("same-PID CPU threshold was not reached")
    time.sleep(3)
    final_ticks = proc_ticks(pid, start)
    return {"state": "ready", "pid": pid, "start_ticks": start, "samples": samples,
            "margin_end_ns": time.monotonic_ns(), "margin_end_ticks": final_ticks}


def ref(path, cap):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > cap:
            raise ValueError("nonregular or oversized file")
        raw = stream.read(cap + 1)
        after = os.fstat(stream.fileno())
    identity = ("st_dev", "st_ino", "st_mode", "st_size", "st_mtime_ns", "st_ctime_ns")
    if (len(raw) != before.st_size or any(getattr(before, key) != getattr(after, key) for key in identity)
            or (before.st_dev, before.st_ino) != (path.lstat().st_dev, path.lstat().st_ino)):
        raise ValueError("file changed during read")
    return raw, {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "mtime_ns": before.st_mtime_ns}


def document(path):
    return json.loads(ref(path, 128*1024)[0])


def file_readback(record):
    OUT.mkdir(mode=0o700)
    files = {}
    record.update(files=files, errors={})
    try:
        bash = Path("/usr/bin/bash").stat()
        alias = Path("/bin/bash").stat()
        if not stat.S_ISREG(bash.st_mode) or (bash.st_dev, bash.st_ino) != (alias.st_dev, alias.st_ino):
            raise ValueError("installed Bash alias identity")
        record["bash"] = {"dev": bash.st_dev, "ino": bash.st_ino, "bytes": bash.st_size,
                          "paths": ["/usr/bin/bash", "/bin/bash"]}
    except (OSError, ValueError) as error:
        record["errors"]["bash"] = str(error)[:256]

    try:
        result = document(WORK / "result.json")
        proof = document(WORK / "proof-inputs.json")
        after = document(WORK / "after.json")
        before = document(WORK / "before.json")
        for key in ("boot_id", "attempt"):
            if record[key] != result[key] or record[key] != proof[key]:
                raise ValueError("fresh arm identity changed")
        if after["boot_id"] != record["boot_id"]:
            raise ValueError("after census boot mismatch")
    except (OSError, ValueError, KeyError) as error:
        record["errors"]["after_binding"] = str(error)[:256]
        return

    remote = WORK / "remote"
    current = "m7-1433/Saves/" + SAVE
    history = [name for name in after.get("remote", {})
               if re.fullmatch(r"m7-1433/Saves-replaced/[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}/gb/ExitProbe[.]srm", name)
               and name not in before["remote"]]
    if len(history) != 1:
        record["errors"]["old.srm"] = f"replacement history count {len(history)}"
    operands = [
        ("local.srm", Path("/storage/roms") / SAVE, after.get("local", {}).get(SAVE)),
        ("current.srm", remote / current, after.get("remote", {}).get(current)),
    ]
    if len(history) == 1:
        operands.append(("old.srm", remote / history[0], after["remote"][history[0]]))
    for name, path, expected in operands:
        try:
            raw, identity = ref(path, 8192)
            if not expected or any(expected[key] != identity[key] for key in identity):
                raise ValueError("original bytes/mtime differ from live census")
            with (OUT / name).open("xb") as output:
                output.write(raw)
            files[name] = identity
        except (OSError, ValueError, KeyError) as error:
            record["errors"][name] = str(error)[:256]


def menu_guard(schedule, proof, before, record, sequence):
    import menu_readback

    identity = {key: record[key] for key in ("boot_id", "attempt", "pid", "start_ticks")}
    row = {**identity, "sequence": sequence, "schema": "m7-1433-menu-guard-v1"}
    try:
        if any(schedule[key] != value for key, value in identity.items()):
            raise ValueError("unbound menu window")
        if traced_game() != (identity["pid"], identity["start_ticks"]):
            raise ValueError("original traced game changed")
        manifest_raw, manifest = ref(INPUT / "fixture-manifest.json", 65536)
        if manifest["sha256"] != proof["fixture"]["sha256"]:
            raise ValueError("fixture changed after launch")
        expected = json.loads(manifest_raw)["files"]["after.srm"]
        row.update(menu_readback.menu_sample(identity, before["local"][SAVE], expected,
                   Path("/storage/roms") / SAVE, ref, proc_ticks,
                   document(WORK / "game-ready.json"), proof["ES"]))
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        row.update(state="REFUSED", error=str(error)[:180])
    sample = time.monotonic_ns()
    row.update(sample_ns=sample, menu_until_ns=schedule["menu_until_ns"],
               remaining_ms=(schedule["menu_until_ns"]-sample)//1000000)
    raw = json.dumps(row, separators=(",", ":"))
    if len(raw)+len("M7_MENU_GUARD=")+2 > T.GUARD_LINE:
        raise ValueError("menu guard record cap")
    print("M7_MENU_GUARD="+raw, flush=True)


def live_readback(record):
    LIVE.mkdir(mode=0o700)
    record = {**record, "files": {}, "errors": {}}
    try:
        proof = document(WORK / "proof-inputs.json")
        before = document(WORK / "before.json")
        if any(proof[key] != record[key] for key in ("boot_id", "attempt")):
            raise ValueError("live proof identity mismatch")
        backend = proof["backend"]
        proc = Path("/proc") / str(backend["pid"])
        def server():
            fields = (proc / "stat").read_text().rsplit(") ", 1)[1].split()
            if (fields[0] in {"Z", "X", "x"} or
                    os.readlink(proc / "ns/net") != backend["server_namespace"] or
                    not (proc / "exe").samefile("/usr/bin/rclone")):
                raise ValueError("selected WebDAV process changed")
            return int(fields[19])
        identity = server()
        until = time.monotonic() + T.STARTUP
        schedule = None
        sequence = 0
        next_sample = 0
        while time.monotonic() < until:
            if (WORK / "result.json").exists():
                raise ValueError("armed original returned before live file sampling")
            if schedule is None and (WORK / "menu-window.json").is_file():
                schedule = document(WORK / "menu-window.json")
                if any(schedule[key] != record[key] for key in ("boot_id", "attempt", "pid", "start_ticks")):
                    raise ValueError("live menu window identity mismatch")
                T.validate_window(schedule)
                until = schedule["archive_until_ns"] / T.NS
            now = time.monotonic_ns()
            if schedule is not None and now < schedule["menu_until_ns"] and now >= next_sample:
                sequence += 1
                if sequence > T.GUARD_ROWS:
                    raise ValueError("menu guard sample cap")
                menu_guard(schedule, proof, before, record, sequence)
                next_sample = now + T.GUARD_INTERVAL*T.NS
            stamps = {}
            for name in STAMP_NAMES:
                try:
                    stamps[name] = ref(STAMPS / name, 4096)[0].decode()
                except (FileNotFoundError, ValueError):
                    break
            if len(stamps) == 3 and all(value and value != before["stamps"][name] for name, value in stamps.items()):
                if server() != identity:
                    raise ValueError("WebDAV generation changed before files")
                record["stamps"] = stamps
                break
            time.sleep(.015)
        else:
            raise ValueError("live terminal stamp wait expired")

        remote = WORK / "remote/m7-1433"
        options = []
        history = remote / "Saves-replaced"
        if history.is_dir():
            for index, entry in enumerate(history.iterdir()):
                if index >= 16:
                    raise ValueError("replacement directory count")
                name = "m7-1433/Saves-replaced/" + entry.name + "/" + SAVE
                if re.fullmatch(r"[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}", entry.name) and name not in before["remote"]:
                    candidate = entry / SAVE
                    if candidate.is_file():
                        options.append(candidate)
        paths = [("local.srm", Path("/storage/roms") / SAVE), ("current.srm", remote / "Saves" / SAVE)]
        if len(options) == 1:
            paths.append(("old.srm", options[0]))
        else:
            record["errors"]["old.srm"] = f"replacement history count {len(options)}"
        for name, path in paths:
            try:
                raw, fact = ref(path, 8192)
                with (LIVE / name).open("xb") as output:
                    output.write(raw)
                record["files"][name] = fact
            except (OSError, ValueError) as error:
                record["errors"][name] = str(error)[:256]
        if server() != identity:
            raise ValueError("WebDAV generation changed after files")
        record["active_backend"] = {"pid": backend["pid"], "start_ticks": identity,
                                    "namespace": backend["server_namespace"]}
    except (OSError, ValueError, KeyError) as error:
        record["errors"]["live"] = str(error)[:256]
    finally:
        with (LIVE / "file-originals.json").open("x") as output:
            json.dump(record, output, indent=2)


def main():
    mode, boot, attempt = sys.argv[1:]
    record = {"boot_id": boot, "attempt": attempt}
    if not re.fullmatch(r"[a-f0-9]{32}", attempt) or BOOT.read_text().strip() != boot:
        raise ValueError("stale boot or attempt")
    if mode == "cpu":
        try:
            record.update(readiness())
        except (OSError, ValueError, KeyError, IndexError) as error:
            emit({**record, "state": "refused", "error": str(error)[:256]})
            return 2
        emit(record)
        live_readback(record)
        return 0
    if mode != "files":
        raise ValueError("unknown witness mode")
    try:
        file_readback(record)
    finally:
        with (OUT / "file-originals.json").open("x") as output:
            json.dump(record, output, indent=2)
    return 2 if record["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
