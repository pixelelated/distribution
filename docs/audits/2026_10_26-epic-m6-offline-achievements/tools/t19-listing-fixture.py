"""T19 (#666), Q6: one ROM name with a byte invalid in UTF-8 fails the scan's
whole listing.

    python3 -I -B docs/audits/2026_10_26-epic-m6-offline-achievements/tools/t19-listing-fixture.py \
        <patched proxy tree> <scratch dir> [<rev>]

Takes the listing's python -- the heredoc `list_jobs` hands to python3 in
raofflineproxy-ctl at <rev> (default 8ebaf8daad) -- unchanged, and runs it
the way the ctl does (argv: the job file, mode all, the ROM root, the
interface's folder, the walked systems, the cursor; RA_SCAN_USER in the
environment) against the patched client (PYTHONPATH=<tree>/linux) with
RAOFFLINEPROXY_CONFIG_DIR a fresh folder under <scratch dir>, over two
fixture libraries: one whose ROM names decode, and one that adds a name
with the byte 0xff. The ctl itself is not run; nothing outside <scratch
dir> is read for state or written. Prints each case's exit and the
listing's last stdout line or its error's last line. Exit 0 when the
decodable library lists (rc 0) and the undecodable one does not (rc != 0):
the defect as read; 1 otherwise.
"""
import os, re, subprocess, sys
tree, scratch = sys.argv[1], sys.argv[2]
rev = sys.argv[3] if len(sys.argv) > 3 else "8ebaf8daad"
ctl = subprocess.run(["git", "show", f"{rev}:projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl"],
                     capture_output=True, text=True, check=True).stdout
m = re.search(r"^list_jobs\(\) \{.*?<<'PY'\n(.*?)\nPY\n", ctl, re.S | re.M)
assert m, "the listing's heredoc was not found"
os.makedirs(scratch, exist_ok=True)
prog = os.path.join(scratch, "listing.py")
open(prog, "w").write(m.group(1) + "\n")
res = {}
for case, extra in (("decodable", None), ("undecodable", b"bad-\xff-name.nes")):
    root = os.path.join(scratch, case)
    roms = os.path.join(root, "roms", "nes")
    os.makedirs(roms, exist_ok=True)
    open(os.path.join(roms, "good.nes"), "wb").write(b"NES\x1a" + b"\0" * 64)
    if extra:
        open(os.path.join(roms.encode(), extra), "wb").write(b"NES\x1a" + b"\1" * 64)
    cfg = os.path.join(root, "config"); os.makedirs(cfg, exist_ok=True)
    esd = os.path.join(root, "es"); os.makedirs(esd, exist_ok=True)
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "HOME": root,
           "PYTHONPATH": os.path.join(tree, "linux"), "PYTHONDONTWRITEBYTECODE": "1",
           "RAOFFLINEPROXY_CONFIG_DIR": cfg, "XDG_CONFIG_HOME": root, "RA_SCAN_USER": "fixture"}
    r = subprocess.run(["python3", "-B", prog, os.path.join(root, "jobs"), "all", os.path.join(root, "roms"), esd, "nes",
                        os.path.join(root, "cursor")], capture_output=True, text=True, env=env, timeout=120)
    last = (r.stdout.strip().splitlines() or [""])[-1] if r.returncode == 0 else (r.stderr.strip().splitlines() or [""])[-1]
    res[case] = r.returncode
    print(f"{case}: rc={r.returncode}; {last[:200]}")
met = res["decodable"] == 0 and res["undecodable"] != 0
print("the defect as read: " + ("REPRODUCED" if met else "not reproduced"))
sys.exit(0 if met else 1)
