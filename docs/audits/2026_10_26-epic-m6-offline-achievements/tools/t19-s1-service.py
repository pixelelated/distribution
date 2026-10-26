#!/usr/bin/env python3
"""T19 S1 (#666, #1157): the patched pin's real service, its offline login probed over HTTP.

    t19-s1-service.py <tree> <scratch>

<tree> is the pin unpacked with the series applied; <scratch> a fresh directory
under /workspace/tmp. The service runs in bubblewrap with --clearenv and
--unshare-net, so upstream is unreachable by construction and only the
sandbox's loopback exists. The store holds one login2 row for the configured
synthetic account and one for another; system.cfg names the configured one.
Every credential value is a short synthetic word assembled here at run time.
Nothing is printed but each case's status, whether a Token came back, and
whether X-RA-Offline did. Exit 0 when every case behaved as the patched
contract says, 1 when one did not (the unpatched tree's FAIL), 2 when the
run could not be made.
"""
import http.client
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REAL_PREFIXES = ("/storage", "/etc", "/usr", "/var", "/root", "/home", "/flash")
ACCOUNT, OTHER = "t19player", "t19other"


def word(*parts):
    return "".join(parts)


TOKEN, OTHER_TOKEN = word("syn", "tok", "one"), word("syn", "tok", "two")
LB = "127.0.0.1:8080"
# (name, query, headers, expected: True answered / False refused)
CASES = [
    ("no credential", f"u={ACCOUNT}", {"Host": LB}, False),
    ("wrong token", f"u={ACCOUNT}&t={OTHER_TOKEN}", {"Host": LB}, False),
    ("cached token", f"u={ACCOUNT}&t={TOKEN}", {"Host": LB}, True),
    ("password, no recorded hash", f"u={ACCOUNT}&p={word('syn', 'pw', 'one')}", {"Host": LB}, False),
    ("another account, its own token", f"u={OTHER}&t={OTHER_TOKEN}", {"Host": LB}, False),
    ("foreign Host", f"u={ACCOUNT}&t={TOKEN}", {"Host": "rebind.example:8080"}, False),
    ("an Origin", f"u={ACCOUNT}&t={TOKEN}", {"Host": LB, "Origin": "http://rebind.example"}, False),
    ("localhost Host", f"u={ACCOUNT}&t={TOKEN}", {"Host": "localhost:8080"}, True),
]


def inner(tree, scratch):
    cfg = Path(scratch) / "cfg"
    sys.path.insert(0, str(Path(tree) / "linux"))
    os.environ["RAOFFLINEPROXY_CONFIG_DIR"] = str(cfg)
    from raofflineproxy import cache_keys, storage  # noqa: E402
    store = storage.Storage(database_path=cfg / "proxy.sqlite3")
    for user, token in ((ACCOUNT, TOKEN), (OTHER, OTHER_TOKEN)):
        store.upsert_cache(cache_keys.login(user), json.dumps({"Success": True, "User": user, "Token": token}))
    store.close()
    log = open(Path(scratch) / "service.out", "wb")
    svc = subprocess.Popen([sys.executable, "-B", "-m", "raofflineproxy.main", "run-service"],
                           cwd=str(Path(tree) / "linux"), stdout=log, stderr=subprocess.STDOUT,
                           env=dict(os.environ, PYTHONPATH=str(Path(tree) / "linux")))
    try:
        deadline = time.monotonic() + 30
        while True:
            try:
                http.client.HTTPConnection("127.0.0.1", 8080, timeout=2).connect()
                break
            except OSError:
                if time.monotonic() > deadline or svc.poll() is not None:
                    print("CANNOT: the service did not listen (see service.out)")
                    return 2
                time.sleep(0.3)
        bad = 0
        for name, query, headers, answered in CASES:
            conn = http.client.HTTPConnection("127.0.0.1", 8080, timeout=20)
            conn.putrequest("GET", "/dorequest.php?r=login2&" + query, skip_host=True)
            for key, value in headers.items():
                conn.putheader(key, value)
            conn.endheaders()
            resp = conn.getresponse()
            raw = resp.read()
            try:
                payload = json.loads(raw.decode("utf-8"))
            except ValueError:
                payload = {}
            got = resp.status == 200 and bool(payload.get("Token"))
            offline = resp.getheader("X-RA-Offline") is not None
            ok = got == answered and offline == answered
            bad += not ok
            print(f"{'PASS' if ok else 'FAIL'} {name}: status {resp.status}, token {'yes' if payload.get('Token') else 'no'},"
                  f" X-RA-Offline {'yes' if offline else 'no'}; expected {'answered' if answered else 'refused'}")
            conn.close()
        return 1 if bad else 0
    finally:
        svc.terminate()
        try:
            svc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            svc.kill()
            svc.wait()


def outer(tree, scratch):
    tree, scratch = os.path.realpath(tree), os.path.realpath(scratch)
    if not scratch.startswith("/workspace/tmp/") or any(scratch.startswith(p + "/") for p in REAL_PREFIXES):
        print(f"CANNOT: scratch {scratch} is not under /workspace/tmp")
        return 2
    os.makedirs(scratch, exist_ok=True)
    if os.listdir(scratch):
        print(f"CANNOT: scratch {scratch} is not empty")
        return 2
    cmd = ["bwrap", "--clearenv", "--unshare-net", "--unshare-pid", "--die-with-parent",
           "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
           "--ro-bind", tree, tree, "--bind", scratch, scratch,
           "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "HOME", scratch,
           "--setenv", "XDG_CONFIG_HOME", scratch + "/xdg",
           "--setenv", "RAOFFLINEPROXY_ROCKNIX_SYSTEM_CFG", scratch + "/system.cfg",
           sys.executable, "-I", "-B", os.path.realpath(__file__), "--inner", tree, scratch]
    with open(scratch + "/system.cfg", "w") as f:
        f.write("global.retroachievements.username=" + ACCOUNT + "\n"
                + "global.retroachievements." + "token=" + TOKEN + "\n")
    print(f"host python {sys.version.split()[0]} (image recipe 3.14.7); bwrap --clearenv --unshare-net", flush=True)
    return subprocess.call(cmd)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--inner":
        sys.exit(inner(sys.argv[2], sys.argv[3]))
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(outer(sys.argv[1], sys.argv[2]))
