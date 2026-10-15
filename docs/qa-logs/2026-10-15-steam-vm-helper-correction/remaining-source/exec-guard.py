#!/usr/bin/env python3
"""UNRUN x86_64 ptrace boundary: deny only the exact synthetic client exec."""
import argparse
import ctypes
import errno
import json
import os
from pathlib import Path
import signal
import sys
import time

LIBC = ctypes.CDLL(None, use_errno=True)
LIBC.ptrace.restype = ctypes.c_long
TRACEME, PEEKDATA, SYSCALL, GETREGS, SETREGS, SETOPTIONS, GETEVENTMSG = 0, 2, 24, 12, 13, 0x4200, 0x4201
GET_SYSCALL_INFO = 0x420e
OPTIONS = 1 | 2 | 4 | 8 | 16 | (1 << 20)  # TRACESYSGOOD/fork/vfork/clone/exec/EXITKILL.
FIELDS = "r15 r14 r13 r12 rbp rbx r11 r10 r9 r8 rax rcx rdx rsi rdi orig_rax rip cs eflags rsp ss fs_base gs_base ds es fs gs".split()


class Registers(ctypes.Structure):
    _fields_ = [(name, ctypes.c_ulonglong) for name in FIELDS]


def trace(request, pid, addr=0, data=0):
    ctypes.set_errno(0)
    value = LIBC.ptrace(ctypes.c_uint(request), ctypes.c_uint(pid),
                       ctypes.c_void_p(addr) if isinstance(addr, int) else addr,
                       ctypes.c_void_p(data) if isinstance(data, int) else data)
    if value == -1 and ctypes.get_errno():
        raise OSError(ctypes.get_errno(), "ptrace request " + str(request))
    return value


def read_text(pid, address, bound=4096):
    raw = bytearray()
    for offset in range(0, bound, 8):
        word = trace(PEEKDATA, pid, address + offset)
        raw.extend((word & ((1 << 64) - 1)).to_bytes(8, "little"))
        if 0 in raw:
            return raw.split(b"\0", 1)[0].decode("utf-8", errors="strict")
    raise RuntimeError("Unterminated exec filename")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--client", required=True)
    parser.add_argument("--seconds", type=int, required=True)
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.argv[1:] if args.argv[:1] == ["--"] else args.argv
    assert command and command[0].startswith("/") and args.client in ("/storage/.local/share/Steam/steamrtarm64/steam", "/qa/guard-should-not-run")
    assert os.uname().machine == "x86_64" and 1 <= args.seconds <= 240 and not args.receipt.exists()
    started = time.monotonic()
    report = {"status": "RUNNING", "client_executed": False, "native_client_success": False,
              "argv": command, "denied_execs": [], "original_exits": [], "original_caller_exit": None,
              "meaning": "ptrace returns EACCES at synthetic client exec; normal caller sees its failure"}
    child = os.fork()
    if child == 0:
        try:
            trace(TRACEME, 0)
            os.kill(os.getpid(), signal.SIGSTOP)
            os.execv(command[0], command)
        except BaseException:
            os._exit(125)
    live, denied = {child}, set()
    code = 1
    report.update(wait_calls=0, syscall_stops=0, wait_seconds=0.0,
                  main_loop_poll_sleeps=0, cleanup_exits=[])
    def expired(signum, frame):
        raise RuntimeError("Exec boundary deadline")
    previous_alarm = signal.signal(signal.SIGALRM, expired)
    # A raising signal handler interrupts Python's otherwise-restarted waitpid.
    # Preserve the original bound, including initial stop/readiness time.
    signal.setitimer(signal.ITIMER_REAL, max(0.000001, args.seconds - (time.monotonic() - started)))
    try:
        pid, status = os.waitpid(child, 0)
        assert pid == child and os.WIFSTOPPED(status)
        trace(SETOPTIONS, child, 0, OPTIONS)
        trace(SYSCALL, child)
        while live:
            if time.monotonic() - started > args.seconds:
                raise RuntimeError("Exec boundary deadline")
            waiting = time.monotonic()
            report["wait_calls"] += 1
            try:
                pid, status = os.waitpid(-1, 0x40000000)  # Blocking __WALL; alarm bounds idle tracees.
            finally:
                report["wait_seconds"] += time.monotonic() - waiting
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                exitcode = os.waitstatus_to_exitcode(status)
                report["original_exits"].append({"pid": pid, "exit": exitcode})
                live.discard(pid)
                denied.discard(pid)
                if pid == child:
                    report["original_caller_exit"] = exitcode
                continue
            assert os.WIFSTOPPED(status)
            live.add(pid)
            sig, event = os.WSTOPSIG(status), status >> 16
            deliver = 0
            if event in (1, 2, 3):
                newpid = ctypes.c_ulonglong()
                trace(GETEVENTMSG, pid, 0, ctypes.byref(newpid))
                live.add(newpid.value)
            elif sig == (signal.SIGTRAP | 0x80):
                report["syscall_stops"] += 1
                info = ctypes.create_string_buffer(128)
                size = trace(GET_SYSCALL_INFO, pid, 128, ctypes.byref(info))
                assert size >= 24
                op = info.raw[0]
                registers = Registers()
                trace(GETREGS, pid, 0, ctypes.byref(registers))
                if op == 1 and registers.orig_rax in (59, 322):  # execve / execveat
                    path = read_text(pid, registers.rdi if registers.orig_rax == 59 else registers.rsi)
                    if path == args.client:
                        assert pid not in denied
                        registers.orig_rax = (1 << 64) - 1
                        trace(SETREGS, pid, 0, ctypes.byref(registers))
                        denied.add(pid)
                        report["denied_execs"].append({"pid": pid, "path": path, "forced_errno": errno.EACCES,
                                                       "syscall_not_executed": True})
                elif op == 2 and pid in denied:
                    registers.rax = (1 << 64) - errno.EACCES
                    trace(SETREGS, pid, 0, ctypes.byref(registers))
                    denied.remove(pid)
            elif sig not in (signal.SIGSTOP, signal.SIGTRAP):
                deliver = sig
            trace(SYSCALL, pid, 0, deliver)
        assert report["original_caller_exit"] is not None
        code = report["original_caller_exit"]
        report["status"] = "RETURNED"
    except BaseException as error:
        report.update(status="FAIL", error=repr(error))
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_alarm)
        # EXITKILL is the primary guarantee; explicitly reap on boundary failure.
        for pid in live:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        deadline = time.monotonic() + 5
        while live and time.monotonic() < deadline:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG | 0x40000000)
            except ChildProcessError:
                live.clear()
                break
            if pid and (os.WIFEXITED(status) or os.WIFSIGNALED(status)):
                report["cleanup_exits"].append({"pid": pid, "exit": os.waitstatus_to_exitcode(status),
                                                "meaning": "guard cleanup; not an original caller result"})
                live.discard(pid)
            elif pid:
                try:
                    trace(SYSCALL, pid, 0, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                time.sleep(0.01)
        report["remaining_traced"] = sorted(live)
        report["elapsed_seconds"] = time.monotonic() - started
        args.receipt.write_text(json.dumps(report, indent=2) + "\n")
    return code if code >= 0 else 128 - code


if __name__ == "__main__":
    sys.exit(main())
