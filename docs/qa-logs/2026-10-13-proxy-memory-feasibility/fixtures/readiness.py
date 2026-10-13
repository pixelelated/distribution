#!/usr/bin/env python3
"""UNRUN: synthetic loopback listener/DB preservation probe for an allocated VM.

Never use a live proxy config. This exercises ProxyRuntimeServer, not systemd,
the connectivity worker, ES, a browser, an emulator or the real RA provider.
"""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import signal
import socket
import sys
import threading
import time
from unittest import mock


class Denied(BaseException):
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared", type=Path, required=True)
    parser.add_argument("--variant", choices=["baseline", "candidate"], required=True)
    parser.add_argument("--state", type=Path, required=True, help="new synthetic directory")
    parser.add_argument("--port", type=int, required=True, help="coordinator-allocated loopback port")
    args = parser.parse_args()
    assert 1024 <= args.port <= 65535
    state = args.state.resolve()
    assert not state.exists(), "refuse existing data"
    assert not any(state.is_relative_to(Path(p)) for p in ("/storage", "/userdata", "/mnt", str(Path.home() / ".config")))
    tree = args.prepared.resolve() / args.variant
    manifest = json.loads((args.prepared / "source.json").read_text())
    for name, digest in manifest[args.variant].items():
        assert hashlib.sha256((tree / name).read_bytes()).hexdigest() == digest, name
    state.mkdir(parents=True, exist_ok=False)
    for name in list(os.environ):
        if name.startswith("RAOFFLINEPROXY_"):
            os.environ.pop(name)
    os.environ["RAOFFLINEPROXY_CONFIG_DIR"] = str(state)
    os.environ["RAOFFLINEPROXY_CACHE_IMAGES"] = "0"
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(tree / "linux"))

    def guard(event, values):
        if event in {"socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr",
                     "socket.sendto", "subprocess.Popen", "os.system"}:
            raise Denied(event)
        if event in {"socket.bind", "socket.connect"}:
            assert values[1] == ("127.0.0.1", args.port), "only the allocated endpoint is allowed"
        if event == "socket.__new__":
            if values[1:3] != (socket.AF_INET, socket.SOCK_STREAM):
                raise Denied("only TCP/IPv4 fixture sockets are allowed")
        if event == "sqlite3.connect":
            if not Path(values[0]).resolve().is_relative_to(state):
                raise Denied("non-fixture database")
        if event == "open" and not isinstance(values[0], int):
            path = Path(values[0]).resolve()
            write = values[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)
            if write and not path.is_relative_to(state):
                raise Denied("non-fixture write")
            if not write and any(path.is_relative_to(Path(p)) for p in (
                    "/storage", "/userdata", "/mnt", str(Path.home() / ".config"))):
                raise Denied("production config read")
    sys.addaudithook(guard)
    for event, values in (("socket.getaddrinfo", ("fixture.invalid", 1)),
                          ("sqlite3.connect", ("/storage/forbidden.sqlite3",))):
        try:
            sys.audit(event, *values)
        except Denied:
            continue
        raise AssertionError("guard did not deny " + event)
    # One process owns every socket/thread; the deadline exits it even on a hang.
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("45-second deadline")))
    signal.alarm(45)
    importlib.import_module("raofflineproxy.main")
    from raofflineproxy import cache_keys, config, flusher, proxy_service, storage
    assert config.CONFIG_DIR == state
    cfg = {"proxy_host": "127.0.0.1", "proxy_port": args.port, "cache_images": False, "upload_logs": False}
    store = storage.Storage(state / "fixture.sqlite3")
    assert store.backend == "sqlite"
    for game, aid in ((10, 101), (20, 201)):
        store.upsert_cache(cache_keys.patch(game, "fixture"), json.dumps({"Success": True,
            "PatchData": {"ID": game, "Title": "Synthetic", "Achievements": [{"ID": aid}]}}))
    store.upsert_cache(cache_keys.login("fixture"), '{"Success":true,"User":"fixture","Token":"fixture-only"}')
    records = []

    def request(body):
        payload = body.encode()
        started = time.monotonic()
        # Use numeric socket.connect directly; no name-resolution API is allowed.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect(("127.0.0.1", args.port))
            sock.sendall((f"POST /dorequest.php HTTP/1.0\r\nHost: 127.0.0.1\r\nContent-Length: {len(payload)}\r\n\r\n").encode() + payload)
            chunks = []
            while chunk := sock.recv(65536):
                chunks.append(chunk)
        head, data = b"".join(chunks).split(b"\r\n\r\n", 1)
        status = int(head.split()[1])
        records.append({"action": body.split("&", 1)[0], "status": status,
                        "elapsed_ms": (time.monotonic() - started) * 1000})
        return status, json.loads(data)

    try:
        with mock.patch.object(proxy_service.ProxyRuntimeServer, "is_online", return_value=False), \
             mock.patch.object(proxy_service.ProxyRuntimeServer, "forward_to_upstream_result", return_value=("network_error",)) as upstream:
            for round_number in range(2):
                server = proxy_service.ProxyRuntimeServer(cfg, store)
                serving = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
                serving.start()
                try:
                    # Protocol readiness includes offline login and the next game's
                    # patch; a listening socket alone cannot satisfy these checks.
                    assert request("r=login2&u=fixture&t=fixture-only")[0] == 200
                    assert request("r=patch&g=20&u=fixture")[1]["PatchData"]["ID"] == 20
                    if round_number == 0:
                        assert request("r=awardachievement&a=101&g=10&u=fixture&t=fixture-only&h=0")[1]["Error"] == "queued_offline"
                    response = request("r=startsession&g=10&u=fixture")[1]
                    assert [a["ID"] for a in response["Unlocks"]] == [101]
                    assert request("r=startsession&g=20&u=fixture")[1]["Unlocks"] == []
                    # An upstream auth rejection must not become offline success.
                    upstream.return_value = ("http_error", 401, "Unauthorized", b'{"Success":false}', "application/json", '{"Success":false}')
                    assert request("r=login2&u=fixture&t=fixture-only")[0] == 401
                    upstream.return_value = ("network_error",)
                finally:
                    server.shutdown()
                    serving.join(timeout=2)
                    server.server_close()
                    assert not serving.is_alive()
                pending = store.get_pending_awards()
                assert len(pending) == 1 and flusher.verify_chain(pending)[0]
                assert store._connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
                store.close()
                store = storage.Storage(state / "fixture.sqlite3")
                assert store.get_pending_awards() == pending
        result = {"result": "PASS", "variant": args.variant, "requests": records,
                  "scope": "synthetic loopback listener close/reopen only; no full service/ES lifecycle",
                  "pending_awards_preserved": 1, "provider": "mock; all DNS/outside endpoints denied"}
        print(json.dumps(result, indent=2))
        (state / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    finally:
        store.close()
        signal.alarm(0)


if __name__ == "__main__":
    main()
