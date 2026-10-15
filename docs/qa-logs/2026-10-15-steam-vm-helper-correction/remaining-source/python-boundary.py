#!/usr/bin/python3 -B
"""UNRUN interpreter/fault boundary: execute exact embedded source, never replace its result."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import time

QA = Path("/qa")


def event(row):
    row.update(pid=os.getpid(), monotonic_ns=time.monotonic_ns())
    raw = (json.dumps(row, sort_keys=True) + "\n").encode()
    fd = os.open(QA / "events.ndjson", os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW)
    try:
        assert os.write(fd, raw) == len(raw)
        os.fsync(fd)
    finally:
        os.close(fd)


def main():
    args = sys.argv[1:]
    native = "/system" + json.loads((QA / "native-tools.json").read_text())["python3"]["resolved_path"]
    scan = list(args)
    while scan and scan[0] in ("-I", "-S", "-B"):
        scan.pop(0)
    if not scan or scan[0] != "-":
        assert scan and scan[0] in ("/qa/boundary.py",), "Unapproved Python script"
        os.execv(native, [native, *args])
    raw = sys.stdin.buffer.read(256 * 1024 + 1)
    assert len(raw) <= 256 * 1024
    sha = hashlib.sha256(raw).hexdigest()
    binding = json.loads((QA / "source.json").read_text())
    matches = [name for name, row in binding["helpers"].items() if row["stdin_sha256"] == sha]
    assert len(matches) == 1, "Embedded helper source changed"
    helper = matches[0]
    mode = scan[1] if helper == "client" else None
    case = json.loads((QA / "case.json").read_text())["name"]
    attempt = json.loads((QA / "attempt.json").read_text())["attempt"]
    event({"kind": "helper-start", "helper": helper, "mode": mode, "stdin_sha256": sha, "attempt": attempt})
    if helper == "client" and mode == "install" and attempt == 1:
        if case in ("detached-transfer-child", "proc-census-error", "transport-timeout"):
            def visibility_fault(name, args):
                if name != "open" or not isinstance(args[0], (str, bytes)):
                    return
                value = os.fsdecode(args[0])
                if value == "children" or value.endswith("/children"):
                    event({"kind": "fault", "point": "optional-children-absent", "attempt": attempt})
                    raise FileNotFoundError(2, "synthetic optional proc file absent")
                if (case == "proc-census-error" and value == "stat"
                        and (QA / "detached-child-ready-1.json").exists()):
                    event({"kind": "fault", "point": "proc-stat-visibility-gap", "errno": 13, "attempt": attempt})
                    raise PermissionError(13, "synthetic mandatory proc identity unreadable")
            sys.addaudithook(visibility_fault)
        if case == "metadata-failure-retry":
            def fail_metadata(name, args):
                if name == "open" and args[0] == "beta" and args[2] & os.O_CREAT:
                    event({"kind": "fault", "point": "metadata-beta-open", "errno": 28, "attempt": attempt})
                    raise OSError(28, "synthetic metadata ENOSPC")
            sys.addaudithook(fail_metadata)
        original_fsync = os.fsync
        def fsync(fd):
            original_fsync(fd)
            target = os.readlink("/proc/self/fd/" + str(fd))
            if target.endswith("/.steam-client-update/owner.jsonl"):
                raw_state = Path(target).read_bytes()
                phase = json.loads(raw_state.splitlines()[-1])["op"]
                wanted = {"interrupt-prepared-retry": "prepared", "committed-self-update-retry": "committed"}.get(case)
                if phase == wanted:
                    event({"kind": "fault", "point": "after-journal-fsync-" + phase,
                           "original_signal": 9, "attempt": attempt})
                    os.kill(os.getpid(), signal.SIGKILL)
        if case in ("interrupt-prepared-retry", "committed-self-update-retry"):
            os.fsync = fsync
        if case in ("interrupt-published-retry", "publication-failure-retry"):
            original_cdll = ctypes.CDLL
            def cdll(*args, **kwargs):
                lib = original_cdll(*args, **kwargs)
                original_rename = lib.renameat2
                def rename(a, source, b, target, flags):
                    if case == "publication-failure-retry" and source == b"steamrtarm64" and target == b"steamrtarm64" and flags == 1:
                        event({"kind": "fault", "point": "publication-rename", "errno": 28, "attempt": attempt})
                        ctypes.set_errno(28)
                        return -1
                    code = original_rename(a, source, b, target, flags)
                    if code == 0 and source == b"steamrtarm64" and target == b"steamrtarm64" and flags == 1:
                        original_fsync(a)
                        original_fsync(b)
                        event({"kind": "fault", "point": "after-client-rename-fsync",
                               "original_signal": 9, "attempt": attempt})
                        os.kill(os.getpid(), signal.SIGKILL)
                    return code
                lib.renameat2 = rename
                return lib
            ctypes.CDLL = cdll
    sys.argv = ["-", *scan[1:]]
    code = 0
    try:
        exec(compile(raw, "<stdin>", "exec"), {"__name__": "__main__", "__file__": "<stdin>"})
    except SystemExit as error:
        code = 0 if error.code is None else error.code if isinstance(error.code, int) else 1
    except BaseException:
        code = 1
        raise
    finally:
        event({"kind": "helper-exit", "helper": helper, "mode": mode,
               "stdin_sha256": sha, "attempt": attempt, "original_exit": code})
    return code


if __name__ == "__main__":
    sys.exit(main())
