#!/usr/bin/env python3
"""Drive the installer's whiptail dialogs over a guest's serial socket (#894, #899; S3).

    python3 -I t8-installer-drive.py <socket> <installer> <device-index> <transcript> [--stub-poweroff] [--stub-gptokeyb]

Runs <installer> on the guest's serial console and waits for MAIN MENU. With
<device-index> -1 it stops there (the installer is left on MAIN MENU, to be
read and stopped by PID over SSH). Otherwise it picks the <device-index>th
entry of QUICK INSTALL MENU (0 is the first), answers Yes to both
confirmations, records the result dialog's title and text, dismisses it, and
waits for MAIN MENU again. The installer never exits on its own: whiptail
holds the console raw, so Ctrl-\\ is a key, and Close runs `poweroff -f`.

--stub-poweroff puts a `poweroff` that only prints first in the installer's
PATH; --stub-gptokeyb exports GPTOKEYB as a stub that records its argv. They
are #899's failing control and fixture, never part of #894's runs.

Every step waits for its dialog's words in the ANSI-stripped output and fails
on a timeout. The stripped transcript is written on every exit. Prints one
RESULT line; exits 0 when the expected screen was reached, 1 otherwise.
"""
import atexit, base64, re, socket, sys, time

SOCK, INSTALLER, INDEX, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
FLAGS = set(sys.argv[5:])
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.connect(SOCK); s.settimeout(0.5)
raw = bytearray()

def text(b):
    t = b.decode("utf-8", "replace")
    t = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", " ", t)          # cursor moves and colours become a gap
    t = re.sub(r"\x1b[()][0-9A-Za-z]|\x1b[=>78]", "", t)
    t = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", t)
    return re.sub(r"[ \t]+", " ", t)

def pump(seconds):
    end = time.time() + seconds
    while time.time() < end:
        try:
            c = s.recv(65536)
            if c: raw.extend(c)
        except (socket.timeout, TimeoutError):
            pass

def wait(pattern, timeout, mark):
    end = time.time() + timeout
    while time.time() < end:
        pump(0.5)
        m = re.search(pattern, text(bytes(raw[mark:])), re.S)
        if m: return m
    raise SystemExit(f"RESULT timeout waiting for {pattern!r}")

def send(keys, settle=1.0):
    s.sendall(keys.encode()); pump(settle)

atexit.register(lambda: open(OUT, "w").write(text(bytes(raw))))
pump(1.0)
env = ""
setup = "stty sane rows 24 cols 80; export TERM=vt100; mkdir -p /tmp/t8-stub; rm -f /tmp/t8-stub/gptokeyb.argv; "
if "--stub-poweroff" in FLAGS:
    b = base64.b64encode(b'#!/bin/sh\necho "T8-POWEROFF-STUB $*"\nexit 0\n').decode()
    setup += f"echo {b} | base64 -d > /tmp/t8-stub/poweroff; chmod 755 /tmp/t8-stub/poweroff; "
    env += "PATH=/tmp/t8-stub:$PATH "
if "--stub-gptokeyb" in FLAGS:
    b = base64.b64encode(b'#!/bin/sh\necho "$*" >> /tmp/t8-stub/gptokeyb.argv\nexit 0\n').decode()
    setup += f"echo {b} | base64 -d > /tmp/t8-stub/gptokeyb; chmod 755 /tmp/t8-stub/gptokeyb; "
    env += "GPTOKEYB=/tmp/t8-stub/gptokeyb "
m0 = len(raw)
send("\n" + setup + env + INSTALLER + "\n", 0.2)
wait(r"MAIN MENU.*Install pixelelated", 120, m0)
if INDEX < 0:
    print("RESULT on MAIN MENU"); sys.exit(0)
m1 = len(raw); send("\r")
if wait(r"QUICK INSTALL MENU|T8-POWEROFF-STUB", 60, m1).group(0) != "QUICK INSTALL MENU":
    raise SystemExit("RESULT the main menu took the key as Close (the stub poweroff ran)")
m2 = len(raw); send("\x1b[B" * INDEX + "\r")
wait(r"wiped out", 60, m2)
m3 = len(raw); send("\t", 0.5); send("\r")
wait(r"last chance", 60, m3)
m4 = len(raw); send("\t", 0.5); send("\r")
m = wait(r"(Install Complete|Install Couldn't Finish)(.*?)<\s*Ok\s*>", 1800, m4)
title = m.group(1); body = re.sub(r"\s+", " ", m.group(2)).strip()
m5 = len(raw); send("\r", 1.0)
wait(r"MAIN MENU", 120, m5)
print(f"RESULT {title} | {body[:500]}")
