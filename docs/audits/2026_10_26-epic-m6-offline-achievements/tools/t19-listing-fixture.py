"""T19 (#666), Q6: one ROM name with a byte invalid in UTF-8 fails the scan's
whole listing -- and, since S9 (#1165), the job list's other ways of losing a
name.

    python3 -I -B docs/audits/2026_10_26-epic-m6-offline-achievements/tools/t19-listing-fixture.py \
        <patched proxy tree> <scratch dir> [<rev>]
    python3 -I -B .../t19-listing-fixture.py <patched proxy tree> <scratch dir> \
        --ctl <raofflineproxy-ctl> --helper <raofflineproxy-cache-indexed> --expect unfixed|fixed

The first form is stage B's: it takes the listing's python -- the heredoc
`list_jobs` hands to python3 in raofflineproxy-ctl at <rev> (default
8ebaf8daad) -- unchanged, and runs it the way the ctl does (argv: the job
file, mode all, the ROM root, the interface's folder, the walked systems,
the cursor; RA_SCAN_USER in the environment) against the patched client
(PYTHONPATH=<tree>/linux) with RAOFFLINEPROXY_CONFIG_DIR a fresh folder
under <scratch dir>, over two fixture libraries: one whose ROM names
decode, and one that adds a name with the byte 0xff. Exit 0 when the
decodable library lists (rc 0) and the undecodable one does not: the
defect as read; 1 otherwise.

The second form is S9's (T29's t29-takeback.py shape). It takes the
listing's python from the <ctl> file, and runs four cases, each in
bubblewrap with --clearenv and --unshare-net, nothing outside <scratch dir>
written:
  A. a library with a name holding 0xff: does the listing finish?
  B. a library with a name holding a newline: one job a file?
  C. an index job with no game id (a malformed job file, written in the
     shape case B's listing wrote): refused, or hashed?
  D. an index job for a file named "Hash failed.nes" whose lookup really
     fails (no network): run_jobs lifted whole from <ctl>, with the real
     <helper> -- an error, or a skip?
--expect fixed exits 0 when all four behave as #1165 says, --expect
unfixed exits 0 when all four show the defect; each exits 1 otherwise,
and 2 when a case could not be run.
"""
import os, re, subprocess, sys

ACCOUNT_CFG = ("global.retroachievements.username=t19player\n"
               + "global.retroachievements." + "token=" + "".join(("syn", "tok", "one")) + "\n")


def listing_of(ctl_text):
    m = re.search(r"^list_jobs\(\) \{.*?<<'PY'\n(.*?)\nPY\n", ctl_text, re.S | re.M)
    assert m, "the listing's heredoc was not found"
    return m.group(1) + "\n"


def stage_b(tree, scratch, rev):
    ctl = subprocess.run(["git", "show", f"{rev}:projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl"],
                         capture_output=True, text=True, check=True).stdout
    os.makedirs(scratch, exist_ok=True)
    prog = os.path.join(scratch, "listing.py")
    open(prog, "w").write(listing_of(ctl))
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
    return 0 if met else 1


def sandboxed(scratch, tree, argv, timeout=180):
    """argv in bubblewrap: the host read-only, <scratch> writable, no network, a cleared environment."""
    env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "HOME": scratch,
           "PYTHONPATH": os.path.join(tree, "linux"), "PYTHONDONTWRITEBYTECODE": "1",
           "RAOFFLINEPROXY_CONFIG_DIR": os.path.join(scratch, "config"), "XDG_CONFIG_HOME": scratch,
           "RAOFFLINEPROXY_ROCKNIX_SYSTEM_CFG": os.path.join(scratch, "system.cfg"), "RA_SCAN_USER": "t19player",
           "RAOFFLINEPROXY_IMAGE_WAIT": "0"}
    cmd = ["bwrap", "--clearenv", "--unshare-net", "--die-with-parent", "--ro-bind", "/", "/", "--dev", "/dev",
           "--proc", "/proc", "--tmpfs", "/tmp", "--bind", scratch, scratch]
    for k, v in env.items():
        cmd += ["--setenv", k, v]
    return subprocess.run(cmd + argv, capture_output=True, timeout=timeout)


def library(scratch, case, names):
    root = os.path.join(scratch, case)
    roms = os.path.join(root, "roms", "nes")
    os.makedirs(roms, exist_ok=True)
    for i, n in enumerate(names):
        open(os.path.join(roms.encode(), n), "wb").write(b"NES\x1a" + bytes([i]) * 64)
    os.makedirs(os.path.join(root, "es"), exist_ok=True)
    return root


def entries_of(data):
    """The job file's entries, in whichever shape it was written."""
    if b"\0" in data:
        return [e for e in data.split(b"\0") if e.strip()], "NUL-separated"
    return [e for e in data.split(b"\n") if e.strip()], "newline-separated"


def stage_e(tree, scratch, ctl_path, helper_path, expect):
    scratch = os.path.realpath(scratch)
    if not scratch.startswith("/workspace/tmp/") or (os.path.exists(scratch) and os.listdir(scratch)):
        print(f"CANNOT: scratch {scratch} must be a fresh folder under /workspace/tmp")
        return 2
    os.makedirs(os.path.join(scratch, "config"), exist_ok=True)
    open(os.path.join(scratch, "system.cfg"), "w").write(ACCOUNT_CFG)
    ctl_text = open(ctl_path).read()
    prog = os.path.join(scratch, "listing.py")
    open(prog, "w").write(listing_of(ctl_text))
    fixed = {}
    print(f"host python {sys.version.split()[0]} (image recipe 3.14.7); bwrap --clearenv --unshare-net; "
          f"ctl {ctl_path}; helper {helper_path}")

    def listing(root):
        return sandboxed(scratch, tree, ["python3", "-B", prog, os.path.join(root, "jobs"), "all", os.path.join(root, "roms"),
                                         os.path.join(root, "es"), "nes", os.path.join(root, "cursor")])

    # A. 0xff
    root = library(scratch, "a", [b"good.nes", b"bad-\xff-name.nes"])
    r = listing(root)
    tail = (r.stdout if r.returncode == 0 else r.stderr).decode("utf-8", "replace").strip().splitlines() or [""]
    fixed["A"] = r.returncode == 0
    print(f"A. a name with 0xff: listing rc={r.returncode}; {tail[-1][:160]}")

    # B. newline
    root = library(scratch, "b", [b"good.nes", b"new\nline.nes"])
    r = listing(root)
    if r.returncode != 0:
        print(f"CANNOT: case B's listing failed: {r.stderr.decode('utf-8', 'replace')[-200:]}")
        return 2
    entries, shape = entries_of(open(os.path.join(root, "jobs"), "rb").read())
    fixed["B"] = len(entries) == 2
    print(f"B. a name with a newline: 2 files, {len(entries)} job entries ({shape})")

    # C. an index job with no game id
    target = os.path.join(scratch, "b", "roms", "nes", "good.nes")
    sep = b"\0" if shape == "NUL-separated" else b"\n"
    jobs = os.path.join(scratch, "c-jobs")
    open(jobs, "wb").write(b"I\t\t\t" + target.encode() + sep)
    r = sandboxed(scratch, tree, ["python3", "-B", helper_path, jobs])
    out, err = r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")
    first = (out.strip().splitlines() or [""])[0]
    fixed["C"] = "refused, not hashed" in out and "hashed 1/1" not in err
    print(f"C. an index job with no id: rc={r.returncode}; first line {first[:150]!r}; "
          f"hashed in its stead: {'yes' if 'hashed 1/1' in err else 'no'}")

    # D. a stop word in a file name, its lookup failing for real: an index
    # job (the game id and hash the interface's index gave), so the file is
    # not hashed -- the host has no hashing module -- and the lookup goes to
    # a network that is not there. Written in the shape case B's listing wrote.
    root = library(scratch, "d", [b"Hash failed.nes"])
    rom = os.path.join(root, "roms", "nes", "Hash failed.nes").encode()
    open(os.path.join(root, "jobs"), "wb").write(b"I\t1\t0123456789abcdef0123456789abcdef\t" + rom + sep)
    total = "1"
    funcs = []
    for name in ("say", "slog", "tell", "count_of", "mark_running", "unmark_running", "run_jobs"):
        m = (re.search(rf"^{name}\(\) \{{\n.*?^\}}\n", ctl_text, re.S | re.M)
             or re.search(rf"^{name}\(\) \{{ .*\}}\n", ctl_text, re.M))
        if not m:
            print(f"CANNOT: {name} not found in the ctl")
            return 2
        funcs.append(m.group(0))
    driver = os.path.join(scratch, "d-run.sh")
    open(driver, "w").write(
        "logger() { :; }\n"
        f"PROXY_DIR={scratch}/config; SCAN_LOG={scratch}/d-scan.log; RUNNING={scratch}/config/running\n"
        f"HELPER={helper_path}; ERRORS_IN_A_ROW=3; RUN_ROUTE=scan\n"
        + "".join(funcs)
        + f'run_jobs quiet {root}/jobs {total} 0\n'
        + 'echo "cached=${R_CACHED} skipped=${R_SKIPPED} errors=${R_ERRORS} why=${R_WHY} done=${R_DONE}"\n')
    r = sandboxed(scratch, tree, ["bash", driver])
    verdict = (r.stdout.decode("utf-8", "replace").strip().splitlines() or [""])[-1]
    log_path = os.path.join(scratch, "d-scan.log")
    log = open(log_path, "rb").read().decode("utf-8", "replace") if os.path.exists(log_path) else ""
    client = [l for l in log.splitlines() if "client: FAIL" in l or "client: OK" in l]
    fixed["D"] = "skipped=0" in verdict and "errors=1" in verdict
    print(f"D. 'Hash failed.nes' whose lookup fails: {verdict}; the helper said {client[-1][-160:] if client else 'nothing'!r}")

    want = expect == "fixed"
    held = all(v == want for v in fixed.values())
    print(f"expect {expect}: " + ", ".join(f"{k} {'fixed' if v else 'unfixed'}" for k, v in sorted(fixed.items()))
          + f" -- {'as expected' if held else 'NOT as expected'}")
    return 0 if held else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--expect" in a:
        try:
            tree, scratch = a[0], a[1]
            ctl, helper, expect = a[a.index("--ctl") + 1], a[a.index("--helper") + 1], a[a.index("--expect") + 1]
        except (IndexError, ValueError):
            print(__doc__); sys.exit(2)
        if expect not in ("fixed", "unfixed"):
            print(__doc__); sys.exit(2)
        sys.exit(stage_e(tree, scratch, ctl, helper, expect))
    if len(a) < 2:
        print(__doc__); sys.exit(2)
    sys.exit(stage_b(a[0], a[1], a[2] if len(a) > 2 else "8ebaf8daad"))
