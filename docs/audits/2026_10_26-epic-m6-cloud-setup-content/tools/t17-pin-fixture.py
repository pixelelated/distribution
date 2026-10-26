#!/usr/bin/env python3
"""T17 (#664): what spends the phone listener's ten PIN attempts.

    python3 -I -B docs/audits/2026_10_26-epic-m6-cloud-setup-content/tools/t17-pin-fixture.py \
        [--file <cloud_oauth>] [--expect unfixed|fixed]

Loads the real cloud_oauth (default: the worktree's, which is 8ebaf8daad's
bytes) by SourceFileLoader, makes a real SessionHolder and the real
make_server() on 127.0.0.1 at an ephemeral port, and sends real HTTP requests
over loopback. No sign-in runs: the holder's session is never started, so no
rclone runs; log() is pointed at a scratch file. Nothing leaves the host.

Cases (each on a fresh holder and server):
  favicon      ten GET /favicon.ico, then GET /<pin>: the browser's own icon
               requests carry no PIN; does the right PIN still open the page?
  touch-icons  five GET /apple-touch-icon.png and five
               /apple-touch-icon-precomposed.png, then GET /<pin>
  control      nine GET /favicon.ico, then GET /<pin>: under the limit
  wrong-pins   ten GET /0000-style wrong PINs, then GET /<pin>: the designed
               lockout, the control that the limit exists
  non-ascii    POST pin=%C3%A9 (a decoded non-ASCII PIN): a refusal page, or
               an unhandled exception in the handler?

--expect unfixed asserts what the file at 8ebaf8daad does; --expect fixed what
a fix must do (icons spend nothing; a non-ASCII PIN is refused like any wrong
one). Writes only under a temporary directory.
"""
from pathlib import Path
import argparse, http.client, importlib.machinery, importlib.util, io, os, sys, tempfile, threading, contextlib

ap = argparse.ArgumentParser()
ap.add_argument("--file", type=Path,
                default=Path("projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth"))
ap.add_argument("--expect", choices=["unfixed", "fixed"])
a = ap.parse_args()
src_dir = a.file.resolve().parent
sys.path.insert(0, str(src_dir))
loader = importlib.machinery.SourceFileLoader("cloud_oauth_fixture", str(a.file.resolve()))
spec = importlib.util.spec_from_loader(loader.name, loader)
oauth = importlib.util.module_from_spec(spec)
loader.exec_module(oauth)
print(f"file: {a.file}")

tmp = tempfile.mkdtemp(prefix="t17-pin-", dir=os.environ.get("TMPDIR"))
oauth.LOG_FILE = os.path.join(tmp, "cloud_sync.log")
oauth.STATE_DIR = os.path.join(tmp, "state")


def serve():
    holder = oauth.SessionHolder("drive", None, None, 60)
    server = oauth.make_server("127.0.0.1", 0, holder, lambda: None)
    errors = io.StringIO()
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return holder, server, errors


def request(server, method, path, body=None):
    conn = http.client.HTTPConnection("127.0.0.1", server.server_address[1], timeout=10)
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"} if body is not None else {}
        conn.request(method, path, body=body, headers=headers)
        r = conn.getresponse()
        r.read()
        return r.status
    except (ConnectionError, http.client.HTTPException) as exc:
        return "dropped:" + type(exc).__name__
    finally:
        conn.close()


res = {}
for name, before in (
        ("favicon", ["/favicon.ico"] * 10),
        ("touch-icons", ["/apple-touch-icon.png"] * 5 + ["/apple-touch-icon-precomposed.png"] * 5),
        ("control", ["/favicon.ico"] * 9),
        ("wrong-pins", None)):
    holder, server, _ = serve()
    if before is None:
        wrong = [("%04d" % ((int(holder.pin) + k) % 10000)) for k in range(1, 11)]
        before = ["/" + p for p in wrong]
    statuses = [request(server, "GET", p) for p in before]
    final = request(server, "GET", "/" + holder.pin)
    res[name] = final
    print(f"{name}: {len(before)} requests before, statuses {sorted(set(map(str, statuses)))}, "
          f"attempts spent {holder.pin_attempts}; then GET /<the right pin> -> {final}")
    server.shutdown(); server.server_close()

holder, server, _ = serve()
captured = io.StringIO()
with contextlib.redirect_stderr(captured):
    status = request(server, "POST", "/", body="pin=%C3%A9&type=x")
server.shutdown(); server.server_close()
trace = captured.getvalue()
res["non-ascii"] = "exception" if "TypeError" in trace else str(status)
print(f"non-ascii: POST pin=%C3%A9 -> {status}; handler raised: "
      f"{'yes: ' + next(l for l in trace.splitlines() if 'TypeError' in l).strip()[:120] if 'TypeError' in trace else 'no'}; "
      f"attempts spent {holder.pin_attempts}")

want = {"unfixed": {"favicon": 403, "touch-icons": 403, "control": 200, "wrong-pins": 403, "non-ascii": "exception"},
        "fixed": {"favicon": 200, "touch-icons": 200, "control": 200, "wrong-pins": 403, "non-ascii": "200"}}
if a.expect:
    bad = [k for k, v in want[a.expect].items() if res[k] != v]
    if bad:
        print(f"t17-pin-fixture: UNEXPECTED on {a.expect}: " + ", ".join(f"{k}={res[k]}" for k in bad))
        sys.exit(1)
    print(f"t17-pin-fixture: {a.expect}-expectation-met")
