"""L-05 and L-06 (#678): Moonlight's commands, run as the pin builds them.

    python3 -I l05-l06-moonlight.py <GuiMoonlight.cpp> [--control]

L-05: the three commands that carry the SERVER IP (`moonlight quit %s`,
`moonlight pair -pin %s %s`, the wayland form) are read from the source's
snprintf format strings, filled as snprintf does with a SERVER IP that is an
address, a command separator and a `touch` of the canary -- joined from
those parts when the case runs, so no injection string is at rest in this
file (S3, D-WORKFLOW-211) -- and run through `/bin/sh -c` -- popen's own
shell (ApiSystem.cpp:2269) -- in bubblewrap with --clearenv, a stub
`moonlight` on PATH recording its argv. The case FAILs when the canary is
made: the player's string ran as a command. --control quotes the IP the
way Utils::String::shellQuote does (single quotes, ' as '\\'') and expects
no canary and one argv with the whole string.

L-06: the UNPAIR commands (`rm -r "~/.cache/..."`, `rm -r "~/.config/..."`)
are read from the source's runSystemCommand literals and run through
`/bin/sh -c` with HOME pointing at a seeded fake home. The case FAILs when
the directories survive while the page would say "Unpaired and settings
cleared". --control writes the paths with $HOME outside the quotes'
tilde, and expects them removed.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

src = Path(sys.argv[1]).read_text()
control = "--control" in sys.argv
fmts = re.findall(r'snprintf\(cmd, sizeof cmd, "((?:QT_QPA_PLATFORM=wayland )?moonlight [^"]+)"', src)
rms = re.findall(r'runSystemCommand\("(rm -r \\"~/[^"\\]+(?:\\.[^"\\]*)*\\")"', src)
rms = [r.replace('\\"', '"') for r in rms]
if len(fmts) != 3 or len(rms) != 2:
    sys.exit("FAIL moonlight: the source no longer has the 3 commands and 2 removals this test reads (%d, %d)" % (len(fmts), len(rms)))

def shell_quote(s):
    return "'" + s.replace("'", "'\\''") + "'"

failures = []
base = Path("/workspace/tmp/m6-t31/tmp")
with tempfile.TemporaryDirectory(prefix="moonlight-", dir=base) as d:
    d = Path(d)
    (d / "bin").mkdir()
    stub = d / "bin" / "moonlight"
    stub.write_text('#!/bin/sh\nfor a in "$@"; do printf "[%s]" "$a"; done >> /w/argv.txt; echo >> /w/argv.txt\n')
    stub.chmod(0o755)
    def sh(cmd, home="/w/home"):
        return subprocess.run(["bwrap", "--clearenv", "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin",
                               "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64", "--proc", "/proc",
                               "--dev", "/dev", "--bind", str(d), "/w", "--ro-bind", str(d / "bin"), "/opt/bin",
                               "--setenv", "PATH", "/opt/bin:/usr/bin", "--setenv", "HOME", home,
                               "/bin/sh", "-c", cmd], capture_output=True, text=True, timeout=20)
    # L-05
    ip = "".join(["127.0.0.1", ";", "touch", " ", "/w/", "canary"])   # assembled at run time (S3, D-WORKFLOW-211)
    for f in fmts:
        canary = d / "canary"
        if canary.exists():
            canary.unlink()
        arg = shell_quote(ip) if control else ip
        cmd = f.replace("%s", "4269", 1) % (arg,) if f.count("%s") == 2 else f % (arg,)
        sh(cmd)
        made = canary.exists()
        print("L-05 %-48s canary %s" % (f.split(" ")[-3] + " " + " ".join(f.split(" ")[-2:]) if "pair" in f else f, "MADE" if made else "absent"))
        if made != False:
            failures.append("L-05: `%s` with SERVER IP %r ran the player's string as a command" % (f, ip))
    # L-06
    home = d / "home"
    for sub in (".cache/Moonlight Game Streaming Project", ".config/Moonlight Game Streaming Project"):
        (home / sub).mkdir(parents=True, exist_ok=True)
        (home / sub / "marker").write_text("x")
    for r in rms:
        cmd = r.replace('"~/', '"$HOME/') if control else r
        out = sh(cmd)
        print("L-06 %s -> rc %d" % (cmd, out.returncode))
    left = [sub for sub in (".cache/Moonlight Game Streaming Project", ".config/Moonlight Game Streaming Project") if (home / sub).exists()]
    print("L-06 directories left: %s" % (", ".join(left) or "none"))
    if left:
        failures.append("L-06: UNPAIR's removals left %s while the page says the settings were cleared" % ", ".join(left))
    if control and (d / "argv.txt").exists():
        print("argv seen: " + (d / "argv.txt").read_text().strip().replace("\n", " | "))
if failures:
    for f in failures:
        print("FAIL " + f)
    sys.exit(1)
print("moonlight: PASS")
