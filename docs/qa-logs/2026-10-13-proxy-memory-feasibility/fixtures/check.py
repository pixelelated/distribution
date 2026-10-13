#!/usr/bin/env python3
"""Bounded host source checks, only after coordinator allocation. No listener.

Fresh processes isolate each import sample. Real storage/signing/queue code is
used; provider responses and CLI destinations are mocks. This is not VM proof.
"""
import argparse
from contextlib import ExitStack
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import sqlite3
import ssl
from unittest import mock

OPTIONAL = {"raofflineproxy.menu_sdl", "raofflineproxy.menu_input", "raofflineproxy.ui"}


class GuardViolation(BaseException):
    pass


def install_guard(tree, state):
    def guard(event, args):
        if event.startswith("socket.") or event in {"subprocess.Popen", "os.system"}:
            raise GuardViolation("fixture prohibits network and subprocess side effects: " + event)
        if event in {"open", "sqlite3.connect"}:
            if isinstance(args[0], int):
                return
            path = Path(args[0]).resolve()
            writes = event == "sqlite3.connect" or (len(args) > 2 and
                args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
            if writes:
                allowed = path.is_relative_to(state)
            else:
                allowed = (path.is_relative_to(tree) or path.is_relative_to(state) or
                    path.is_relative_to(Path(sys.base_prefix).resolve()) or
                    path in {Path("/etc/os-release").resolve(), Path("/proc/cpuinfo"),
                             Path("/proc/self/smaps_rollup").resolve()})
            if not allowed:
                raise GuardViolation("fixture prohibits file access: " + str(path))
    sys.addaudithook(guard)
    # Raise audit events, never create a socket or make a DNS request.
    for event, args in (("socket.connect", (None, ("127.0.0.1", 1))),
                        ("socket.getaddrinfo", ("fixture.invalid", 1)),
                        ("sqlite3.connect", ("/storage/forbidden.sqlite3",))):
        try:
            sys.audit(event, *args)
        except GuardViolation:
            continue
        raise AssertionError("denial guard did not fire: " + event)


def worker(tree, state, mode):
    # Never import against an installed proxy, or inherit a real config location.
    state.mkdir(parents=True, exist_ok=False)
    os.environ["RAOFFLINEPROXY_CONFIG_DIR"] = str(state)
    os.environ["RAOFFLINEPROXY_CACHE_IMAGES"] = "0"
    for name in list(os.environ):
        if name.startswith("RAOFFLINEPROXY_") and name not in {
                "RAOFFLINEPROXY_CONFIG_DIR", "RAOFFLINEPROXY_CACHE_IMAGES"}:
            os.environ.pop(name)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(tree / "linux"))
    install_guard(tree, state)
    started = time.perf_counter_ns()
    main = importlib.import_module("raofflineproxy.main")
    elapsed = time.perf_counter_ns() - started
    assert Path(main.__file__).resolve() == tree / "linux/raofflineproxy/main.py"
    from raofflineproxy import config
    assert config.CONFIG_DIR.resolve() == state
    for name in ("DATABASE_FILE", "CONFIG_FILE", "AWARD_SECRET_FILE", "PID_FILE", "LOG_FILE"):
        assert getattr(config, name).resolve().is_relative_to(state), name
    modules = sorted(name for name in sys.modules if name.startswith("raofflineproxy."))
    if mode == "import":
        stats = {}
        for line in Path("/proc/self/smaps_rollup").read_text().splitlines():
            name, _, value = line.partition(":")
            if name in {"Pss", "Rss", "Private_Clean", "Private_Dirty", "Pss_Anon", "Pss_File"}:
                stats[name + "_KiB"] = int(value.split()[0])
        return {"import_ns": elapsed, "memory": stats, "modules": modules,
                "optional_loaded": sorted(OPTIONAL.intersection(modules)),
                "pygame_loaded": "pygame" in sys.modules}
    if mode == "dispatch":
        return dispatch(main, state)
    if mode == "preservation":
        return preservation(state)
    raise ValueError(mode)


def dispatch(main, state):
    observed = []
    # Imports of these actual modules are harmless; pygame is lazy upstream too.
    menu = importlib.import_module("raofflineproxy.menu_sdl")
    ui = importlib.import_module("raofflineproxy.ui")
    commands = [
        (["run-service"], main, "run_service_foreground", mock.call({})),
        (["menu"], menu, "run_menu_sdl", mock.call("synthetic-cli")),
        (["menu-sdl"], menu, "run_menu_sdl", mock.call("synthetic-cli")),
        (["ui-image", "--output", "out.bmp", "--image-width", "64", "--image-height", "48"],
         ui, "write_status_image", mock.call("out.bmp", image_width=64, image_height=48)),
        (["text-image", "--output", "out.bmp", "--text", "Fixture", "--font-scale", "2"],
         ui, "write_text_image", mock.call("out.bmp", "Fixture", image_width=0, image_height=0, font_scale=2)),
    ]
    for argv, module, symbol, expected in commands:
        with ExitStack() as stack:
            target = stack.enter_context(mock.patch.object(module, symbol))
            # Baseline eager-imported names and candidate lazy names reach one spy.
            if module is not main and hasattr(main, symbol):
                stack.enter_context(mock.patch.object(main, symbol, target))
            stack.enter_context(mock.patch.object(main, "load_config", return_value={}))
            stack.enter_context(mock.patch.object(main, "configure_logging"))
            stack.enter_context(mock.patch.object(sys, "argv", ["synthetic-cli", *argv,
                                       "--retroarch-cfg", str(state / "retroarch.cfg")]))
            main.main()
            assert target.call_args_list == [expected], argv
        observed.append(argv[0])
    # Missing output/text still fail without invoking rendering.
    for argv in (["ui-image"], ["text-image", "--output", "out.bmp"]):
        with mock.patch.object(main, "load_config", return_value={}), \
             mock.patch.object(main, "configure_logging"), \
             mock.patch.object(sys, "argv", ["synthetic-cli", *argv, "--retroarch-cfg", str(state / "retroarch.cfg")]), \
             mock.patch("sys.stderr", new_callable=io.StringIO):
            try:
                main.main()
            except SystemExit as exc:
                assert exc.code == 1
            else:
                raise AssertionError("invalid command unexpectedly succeeded")
    return {"passed": observed + ["invalid UI arguments rejected"], "destination": "mock"}


def preservation(state):
    from raofflineproxy import cache_keys, cache_queue, flusher, proxy_service, storage
    checks = []
    store = storage.Storage(state / "fixture.sqlite3")
    assert store.backend == "sqlite", "must exercise packaged SQLite behavior"
    server = object.__new__(proxy_service.ProxyRuntimeServer)
    server.storage = store
    server.config_data = {"cache_images": False, "upload_logs": False}
    server.pending_award_lock = threading.Lock()
    server.is_online = lambda: False
    for game, achievement in ((10, 101), (20, 201)):
        store.upsert_cache(cache_keys.patch(game, "fixture"), json.dumps({
            "Success": True, "PatchData": {"ID": game, "Title": "Synthetic", "Achievements": [{"ID": achievement}]}}))
    queued_rom = cache_queue.QueuedRom(["synthetic-hash"], None, "Synthetic", 1)
    assert cache_queue.enqueue(store, queued_rom)
    bodies = []
    for game, achievement in ((10, 101), (20, 201)):
        body = f"r=awardachievement&a={achievement}&g={game}&u=fixture&t=fixture-only&h=0"
        bodies.append(body)
        response = server.handle_award_request("/dorequest.php", body, {})
        assert b'"queued_offline"' in response
    before = store.get_pending_awards()
    assert len(before) == 2 and flusher.verify_chain(before)[0]
    server.handle_award_request("/dorequest.php", bodies[0], {})
    assert store.get_pending_awards() == before, "duplicate award changed queue"
    assert b"403" in server.handle_award_request("/dorequest.php", bodies[0].replace("h=0", "h=1"), {})
    assert store.get_pending_awards() == before, "hardcore refusal changed queue"
    checks += ["two signed offline awards", "duplicate deduplicated", "hardcore refused"]
    for game, achievement in ((10, 101), (20, 201)):
        response = json.loads(server.build_offline_start_session_response(game, "fixture"))
        assert response["Success"] and [a["ID"] for a in response["Unlocks"]] == [achievement]
    assert json.loads(server.build_offline_start_session_response(10, "other"))["Unlocks"] == []
    checks += ["next-game offline startsession data", "other account has no pending unlocks"]
    store.close()
    store = storage.Storage(state / "fixture.sqlite3")
    assert store.get_pending_awards() == before and flusher.verify_chain(store.get_pending_awards())[0]
    assert cache_queue.oldest(store) == queued_rom
    assert store._connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    checks += ["close/reopen preserves signed queue and cache queue", "SQLite integrity_check ok"]
    # Mock only upstream credential/data/transport operations, keeping the real
    # flusher, validation hash, signer, state transitions and SQLite writes.
    try:
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(flusher, "resolve_credentials", return_value={"user": "fixture", "token": "fixture-only"}))
            stack.enter_context(mock.patch.object(flusher, "refresh_and_load_achievement_ids", return_value=({101, 201}, [10, 20], {101: 10, 201: 20})))
            stack.enter_context(mock.patch.object(flusher, "cache_unlocks"))
            stack.enter_context(mock.patch.object(flusher, "cache_session"))
            stack.enter_context(mock.patch.object(flusher.time, "sleep"))
            transport = stack.enter_context(mock.patch.object(flusher, "http_post", return_value=(401, "Unauthorized", '{"Success":false}')))
            result = flusher.flush_pending_awards(store, {})
            assert result.flushed == 0 and result.pending_remaining == 2
            assert all(a["status"] == "pending" for a in store.get_pending_awards())
            checks.append("auth rejection retains pending awards")
            transport.return_value = (503, "Unavailable", '{"Success":false}')
            result = flusher.flush_pending_awards(store, {})
            assert result.flushed == 0 and result.pending_remaining == 2
            assert flusher.verify_chain(store.get_pending_awards())[0]
            checks.append("network failure retains valid signed queue")
            transport.return_value = (200, "OK", '{"Success":true}')
            transport.reset_mock()
            result = flusher.flush_pending_awards(store, {})
            assert result.flushed == 2 and result.pending_remaining == 0
            assert transport.call_count == 2 and store.get_pending_awards() == []
            assert (state / "last-flush").read_text().split()[1] == "2"
            checks.append("mock successful flush delivers two and writes stamp")
        assert cache_queue.oldest(store) == queued_rom
        assert store._connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        store.close()
    return {"passed": checks, "transport": "mock only", "listener": "not created"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--worker", choices=["import", "dispatch", "preservation"])
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.prepared.resolve(), args.output.resolve(), args.worker)))
        return
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    prepared = args.prepared.resolve()
    manifest = json.loads((prepared / "source.json").read_text())
    for variant in ("baseline", "candidate"):
        for name, expected in manifest[variant].items():
            assert hashlib.sha256((prepared / variant / name).read_bytes()).hexdigest() == expected, name
    outcomes = []
    metadata = {"python": sys.version, "executable": sys.executable,
        "executable_sha256": hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
        "sqlite": sqlite3.sqlite_version, "openssl": ssl.OPENSSL_VERSION,
        "dependencies": "Python standard library only; no installs",
        "command": sys.argv, "network_policy": "deny all socket audit events including creation/DNS; negative events checked before proxy import",
        "scope": "host import/dispatch/in-process synthetic storage; no listener or service",
        "source_manifest_sha256": hashlib.sha256((prepared / "source.json").read_bytes()).hexdigest(),
        "fixture_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "max_seconds": 60, "scratch_limit_bytes": 20 * 1024 * 1024}
    (output / "run.json").write_text(json.dumps(metadata, indent=2) + "\n")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", MALLOC_ARENA_MAX="2")
    # Alternating order, including a reversed pair. This is import-only PSS,
    # never the real service's retained working set or pressure response.
    cases = [(v, "import") for v in ("baseline", "candidate", "candidate", "baseline", "baseline", "candidate")]
    cases += [(v, m) for v in ("baseline", "candidate") for m in ("dispatch", "preservation")]
    started = time.monotonic()
    for index, (variant, mode) in enumerate(cases):
        remaining = 55 - (time.monotonic() - started)
        assert remaining > 0, "55 second fixture budget exceeded"
        command = [sys.executable, "-B", str(Path(__file__).resolve()),
            "--prepared", str(prepared / variant), "--output", str(output / f"state-{index}"),
            "--worker", mode]
        with subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            timed_out = False
            try:
                stdout, stderr = process.communicate(timeout=min(8, remaining))
            except subprocess.TimeoutExpired:
                timed_out = True
                process.kill()
                stdout, stderr = process.communicate()
            record = {"variant": variant, "mode": mode, "pid": process.pid,
                      "rc": process.returncode, "exited": process.poll() is not None,
                      "timed_out": timed_out, "stderr": stderr}
        if process.returncode == 0:
            record["result"] = json.loads(stdout)
        else:
            record["stdout"] = stdout
        outcomes.append(record)
        (output / "result.json").write_text(json.dumps(outcomes, indent=2) + "\n")
        assert process.returncode == 0, record
        scratch_size = sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
        assert scratch_size < 20 * 1024 * 1024, "scratch budget exceeded"
    imports = [r for r in outcomes if r["mode"] == "import"]
    for record in imports:
        expected = sorted(OPTIONAL) if record["variant"] == "baseline" else []
        assert record["result"]["optional_loaded"] == expected, record
        assert not record["result"]["pygame_loaded"]
    print(json.dumps({"result": "PASS", "cases": len(outcomes), "seconds": time.monotonic() - started,
                      "evidence_level": "host source checks; no listener or real provider"}))


if __name__ == "__main__":
    main()
