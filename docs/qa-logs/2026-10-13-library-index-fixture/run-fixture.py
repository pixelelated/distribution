#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""UNRUN. One bounded #567 case inside an already allocated disposable VM.

No service management, host launcher, installation or external network fallback.
The coordinator must stop the frontend and supply a live Wayland socket first.
"""
import argparse
import errno
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import resource
import shutil
import signal
import socket
import ssl
import stat
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ES = Path("/usr/bin/emulationstation")
CTL = Path("/usr/bin/raofflineproxy-ctl")
HOST_FILES = [Path(p) for p in ("/etc/hosts", "/etc/resolv.conf", "/etc/nsswitch.conf")]
CA = Path("/run/rocknix/cacert.pem")
STUB = "Synthetic metadata-only fixture. NOT A ROM. Never launch.\n"
LIMIT = 240


def save(path, data):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    tmp.replace(path)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def census():
    # Public hosts/trust, installed code and mount identity only; no user config.
    return {"files": {str(p): digest(p) for p in HOST_FILES + [CA, ES, CTL]},
            "storage": [os.stat("/storage").st_dev, os.stat("/storage").st_ino],
            "mountinfo": digest(Path("/proc/self/mountinfo"))}


def clean_env(a):
    # Allowlist, not a copy: no proxy variables, account data, preload or TLS keys.
    return {"PATH": "/usr/bin:/usr/sbin:/bin:/sbin", "HOME": "/storage",
            "LANG": a.language + ".UTF-8", "LC_ALL": a.language + ".UTF-8",
            "XDG_RUNTIME_DIR": a.xdg_runtime_dir,
            "WAYLAND_DISPLAY": a.wayland_display, "SDL_VIDEODRIVER": "wayland",
            "PIX567_ROOT": str(a.output), "PYTHONDONTWRITEBYTECODE": "1",
            "NO_PROXY": "*", "no_proxy": "*"}


def command(root, label, argv):
    with (root / (label + ".stdout")).open("wb") as out, (root / (label + ".stderr")).open("wb") as err:
        proc = subprocess.Popen(argv, stdout=out, stderr=err)
        try:
            code = proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
            code = proc.wait()
            save(root / (label + ".exit.json"), {"exit": code, "timeout": True})
            raise RuntimeError(label + " timed out") from None
    save(root / (label + ".exit.json"), {"exit": code, "timeout": False})
    check(code == 0, label + " failed; original exit retained")


def pidfile(root, name, proc):
    # /proc stat's comm can contain spaces; field 22 follows its closing ')'.
    start = Path(f"/proc/{proc.pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
    save(root / (name + ".pid.json"), {"pid": proc.pid, "start_ticks": start})


def wait_for(predicate, seconds, description, children=()):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        for proc in children:
            check(proc.poll() is None, description + ": child exited early")
        if predicate():
            return
        time.sleep(0.1)
    raise RuntimeError(description + " timed out")


def api(path):
    conn = http.client.HTTPConnection("127.0.0.1", 1234, timeout=2)
    try:
        conn.request("GET", path)
        response = conn.getresponse()
        body = response.read(65536)
        check(response.status == 200, "ES API refused " + path)
        return body
    finally:
        conn.close()


def idle():
    try:
        return json.loads(api("/isIdle")) == [True]
    except (OSError, http.client.HTTPException, ValueError):
        return False


def tls_controls(root):
    context = ssl.create_default_context(cafile=str(root / "cert.pem"))

    def request(path, host="retroachievements.org"):
        # Resolves through the actual private hosts bind; TLS checks the DNS name.
        conn = http.client.HTTPSConnection("retroachievements.org", 443, context=context, timeout=4)
        try:
            conn.request("GET", path, headers={"Host": host})
            reply = conn.getresponse()
            body = reply.read(8192)
            return reply.status, body
        finally:
            conn.close()

    status, body = request("/dorequest.php?r=officialgameslist")
    check(status == 200 and "4242001" in json.loads(body)["Response"], "local TLS readiness failed")
    check(request("/dorequest.php?r=login")[0] == 403, "unknown endpoint not refused")
    check(request("/dorequest.php?r=hashlibrary", "other.invalid")[0] == 403, "wrong Host not refused")
    try:
        with socket.create_connection(("127.0.0.1", 443), timeout=4) as raw:
            with context.wrap_socket(raw, server_hostname="other.invalid"):
                pass
    except ssl.SSLError:
        pass
    else:
        raise RuntimeError("wrong TLS name accepted")
    try:
        socket.getaddrinfo("other.invalid", 443)
    except socket.gaierror as error:
        dns_errno = error.errno
    else:
        raise RuntimeError("unknown DNS name unexpectedly resolved")
    # TEST-NET, only after loopback-only namespace verification. No public probe.
    with socket.socket() as probe:
        probe.settimeout(1)
        blocked = probe.connect_ex(("203.0.113.1", 443))
    check(blocked in (errno.ENETUNREACH, errno.EHOSTUNREACH), "non-loopback route exists")
    wait_for(lambda: json.loads((root / "tls-counts.json").read_text())["tls_errors"] == 1,
             4, "TLS refusal receipt")
    baseline = json.loads((root / "tls-counts.json").read_text())
    check(baseline == {"hashlibrary": 0, "officialgameslist": 1, "denied": 2,
                       "connections": 4, "tls_errors": 1}, "TLS controls count mismatch")
    save(root / "tls-controls.json", {"baseline": baseline, "unknown_dns_errno": dns_errno,
                                       "non_loopback_connect_errno": blocked})
    return baseline


def prepare_storage(root, a):
    storage = root / "storage"
    es = storage / ".config/emulationstation"
    for p in [es, storage / ".config/system/configs", storage / ".config/raofflineproxy",
              storage / ".cache", storage / "roms/gb"]:
        p.mkdir(parents=True, exist_ok=True)
    (storage / ".emulationstation").symlink_to(".config/emulationstation")
    (storage / ".config/locale").symlink_to("/usr/config/locale")
    (es / "resources").symlink_to("/usr/config/emulationstation/resources")
    (es / "locale").symlink_to("/usr/config/locale")
    (es / "themes").symlink_to("/usr/share/themes")
    for name in ["es_systems.cfg", "es_features.cfg"]:
        shutil.copyfile(HERE / "fixtures" / name, es / name)
    (es / "es_settings.cfg").write_text(
        '<config>\n<bool name="CheevosCheckIndexesAtStart" value="true"/>\n'
        '<bool name="NetPlayCheckIndexesAtStart" value="false"/>\n'
        '<bool name="SaveGamelistsOnExit" value="true"/>\n'
        '<bool name="PublicWebAccess" value="false"/>\n'
        '<bool name="IgnoreGamelist" value="false"/>\n'
        '<bool name="ParseGamelistOnly" value="false"/>\n'
        '<string name="CheevosLookupOnlyLast" value="0"/>\n'
        '<string name="CollectionSystemsAuto" value=""/>\n'
        '<string name="ThemeSet" value="es-theme-art-book-next"/>\n'
        '<int name="ScreenSaverTime" value="0"/>\n'
        f'<string name="Language" value="{a.language}"/>\n</config>\n')
    (storage / ".config/system/configs/system.cfg").write_text(
        "global.retroachievements=0\nglobal.retroachievements.offlineproxy=1\n"
        "global.netplay=0\ncloudsaves.startup=0\ncloudsaves.gameexit=0\n"
        f"audio.bgmusic=0\nsystem.language={a.language}\n")
    # No account fields are written, including in the simulated-success case.
    (storage / ".config/raofflineproxy/cached_game_ids.txt").write_text(
        "" if a.case == "no-account" else "4242002\n")
    (storage / "roms/gb/existing.gb").write_text(STUB)
    shutil.copyfile(HERE / "fixtures/base.gamelist.xml", storage / "roms/gb/gamelist.xml")
    return storage


def observe(root):
    tls = json.loads((root / "tls-counts.json").read_text())
    events_path = root / "ctl-events.jsonl"
    events = [json.loads(line) for line in events_path.read_text().splitlines()] if events_path.exists() else []
    return tls, events


def worker(a):
    root = a.output
    resource.setrlimit(resource.RLIMIT_FSIZE, (8 * 1024 * 1024, 8 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    os.umask(0o077)
    os.unshare(os.CLONE_NEWNS | os.CLONE_NEWNET)
    save(root / "namespaces.json", {kind: os.readlink("/proc/self/ns/" + kind) for kind in ["mnt", "net"]})
    command(root, "private-mounts", ["mount", "--make-rprivate", "/"])
    command(root, "loopback-up", ["ip", "link", "set", "lo", "up"])
    check(socket.if_nameindex() == [(1, "lo")], "namespace is not loopback only")
    command(root, "ipv4-routes", ["ip", "-4", "route", "show", "table", "all"])
    command(root, "ipv6-routes", ["ip", "-6", "route", "show", "table", "all"])
    storage = prepare_storage(root, a)
    (root / "hosts").write_text("127.0.0.1 localhost retroachievements.org\n::1 localhost\n")
    (root / "resolv.conf").write_text("nameserver 127.0.0.1\noptions attempts:1 timeout:1\n")
    (root / "nsswitch.conf").write_text("passwd: files\ngroup: files\nhosts: files\n")
    bindings = [(storage, Path("/storage"))] + list(zip(
        [root / "hosts", root / "resolv.conf", root / "nsswitch.conf"], HOST_FILES)) + [(HERE / "raofflineproxy-ctl", CTL)]
    for i, (source, target) in enumerate(bindings):
        check(target.exists(), "missing bind target " + str(target))
        command(root, "bind-" + str(i), ["mount", "--bind", str(source), str(target)])
    # /proc mountinfo, never mountpoint -q for file mounts. Read-back hashes also
    # catch symlinks into /storage that a storage bind might otherwise hide.
    (root / "private-mountinfo.txt").write_text(Path("/proc/self/mountinfo").read_text())
    for source, target in bindings[1:]:
        check(digest(source) == digest(target), "bind content mismatch: " + str(target))
    (root / "openssl.cnf").write_text(
        "[req]\nprompt=no\ndistinguished_name=dn\nx509_extensions=ext\n"
        "[dn]\nCN=retroachievements.org\n[ext]\nsubjectAltName=DNS:retroachievements.org\n"
        "basicConstraints=critical,CA:TRUE\nkeyUsage=critical,keyCertSign,digitalSignature,keyEncipherment\n"
        "subjectKeyIdentifier=hash\nauthorityKeyIdentifier=keyid:always\n")
    command(root, "certificate", ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
                                  "-config", str(root / "openssl.cnf"), "-keyout", str(root / "key.pem"),
                                  "-out", str(root / "cert.pem")])
    (root / "logs").mkdir()
    listener = es = None
    result = {"case": a.case, "trigger": a.trigger, "passed": False, "scope": "ES lookup + simulated ctl contract"}
    try:
        with (root / "tls.stdout").open("wb") as out, (root / "tls.stderr").open("wb") as err:
            listener = subprocess.Popen([sys.executable, str(HERE / "tls-endpoints.py"), str(root)], stdout=out, stderr=err)
        pidfile(root, "listener", listener)
        wait_for(lambda: (root / "tls-ready.json").exists(), 8, "listener readiness", [listener])
        baseline = tls_controls(root)
        with (root / "es.stdout").open("wb") as out, (root / "es.stderr").open("wb") as err:
            es = subprocess.Popen([str(ES), "--log-path", str(root / "logs"), "--no-splash"],
                                  cwd="/storage", env=clean_env(a), stdout=out, stderr=err)
        pidfile(root, "es", es)
        wait_for(idle, 40, "ES API readiness", [es, listener])
        log = root / "logs/es_log.txt"
        check(log.exists(), "missing ES log")
        load_line = "Loading system config file /storage/.config/emulationstation/es_systems.cfg"
        initial_loads = log.read_text().count(load_line)
        check(initial_loads == 1, "unexpected initial library load count")
        check(observe(root)[0] == baseline, "startup consumed the stimulus")
        if a.case != "no-new-work":
            (storage / "roms/gb/new.gb").write_text(STUB)
            shutil.copyfile(HERE / "fixtures/new.gamelist.xml", storage / "roms/gb/gamelist.xml")
        save(root / "armed.json", {"ready": True, "es_pid": es.pid, "trigger": a.trigger,
                                   "instruction": "UI mode: capture confirmation, choose YES or NO, then write ui-choice.txt"})
        choice = "YES"
        if a.trigger == "api":
            api("/reloadgames")
        else:
            wait_for(lambda: (root / "ui-choice.txt").exists(), 100, "coordinator UI choice", [es, listener])
            choice = (root / "ui-choice.txt").read_text().strip()
            check(choice in ("YES", "NO"), "ui-choice.txt must contain YES or NO")
        if choice == "YES":
            wait_for(lambda: log.read_text().count(load_line) >= initial_loads + 1, 40,
                     "actual library rescan", [es, listener])
            if a.case in ("success", "no-account"):
                wait_for(lambda: any(e["category"] == "after-index" for e in observe(root)[1]),
                         15, "top-up call", [es, listener])
                real_exit = 0 if a.case == "success" else 77
                wait_for(lambda: f"OfflineAchievements: topup --after-index exited {real_exit}" in log.read_text(),
                         5, "ES-observed ctl exit", [es, listener])
            elif a.case == "failure":
                wait_for(lambda: "Game Hash failed :" in log.read_text(), 15,
                         "hash library refusal", [es, listener])
        wait_for(idle, 15, "ES idle after stimulus", [es, listener])
        # Observe a quiet interval; count == 0 is meaningful only after the rescan
        # log barrier (or coordinator's NO receipt), never immediately after GET.
        time.sleep(3)
        tls, events = observe(root)
        delta = {key: tls[key] - baseline[key] for key in tls}
        after = [e for e in events if e["category"] == "after-index"]
        work = choice == "YES" and a.case != "no-new-work"
        expected_requests = 1 if work else 0
        check(delta["hashlibrary"] == delta["officialgameslist"] == expected_requests, "endpoint counts differ")
        check(delta["connections"] == expected_requests * 2 and delta["tls_errors"] == delta["denied"] == 0,
              "unexpected TLS traffic")
        expected_code = 0 if a.case == "success" else 77
        expect_topup = work and a.case in ("success", "no-account")
        check([e["exit"] for e in after] == ([expected_code] if expect_topup else []), "top-up count/exit differ")
        observed_exits = re.findall(r"OfflineAchievements: topup --after-index exited (\d+)", log.read_text())
        check([int(code) for code in observed_exits] == [e["exit"] for e in after], "ES and seam exits differ")
        check(not any(e["category"] == "unexpected" for e in events), "unexpected ctl verb")
        recovery = storage / ".config/emulationstation/recovery/gb/new.xml"
        identified = False
        if recovery.exists():
            identified = ET.parse(recovery).findtext(".//cheevosId") == "4242001"
        check(identified == expect_topup, "identified-game count differs")
        expected_prepared = int(expect_topup and a.case == "success")
        check(sum(e["prepared"] for e in events) == expected_prepared, "simulated prepared count differs")
        stamp = storage / ".config/raofflineproxy/last-scan"
        check(stamp.exists() == bool(expected_prepared), "unexpected/missing simulated cache stamp")
        expected_loads = initial_loads + int(choice == "YES")
        check(log.read_text().count(load_line) == expected_loads, "extra/missing library reload")
        for game in (storage / "roms/gb").glob("*.gb"):
            check(game.read_text() == STUB, "synthetic game stub changed")
        result.update({"passed": True, "choice": choice, "endpoint_delta": delta,
                       "identified": int(identified), "topup_exits": [e["exit"] for e in after],
                       "simulated_prepared": expected_prepared, "library_loads": expected_loads})
        save(root / "observed.json", result)
        if a.trigger == "ui":
            save(root / "frame-ready.json", {"ready": True, "seconds_to_release": 25})
            wait_for(lambda: (root / "frames-done").exists(), 25, "coordinator frame release", [es, listener])
    except Exception as error:
        result.update({"passed": False, "failure": str(error)})
    finally:
        if es is not None:
            forced = False
            if es.poll() is None:
                try:
                    api("/quit")
                    es.wait(timeout=12)
                except (OSError, RuntimeError, http.client.HTTPException, subprocess.TimeoutExpired):
                    forced = True
                    es.kill()
                    es.wait()
            result["es_exit"] = es.returncode
            result["es_forced"] = forced
            result["passed"] &= es.returncode == 0 and not forced
        if listener is not None:
            if listener.poll() is None:
                listener.terminate()
                try:
                    listener.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    listener.kill()
                    listener.wait()
            result["listener_exit"] = listener.returncode
            result["passed"] &= listener.returncode == 0
        if result["passed"]:
            final_tls, final_events = observe(root)
            final_after = [e["exit"] for e in final_events if e["category"] == "after-index"]
            result["passed"] &= final_tls == tls and final_after == result["topup_exits"]
            result["passed"] &= not any(e["category"] == "unexpected" for e in final_events)
        # Ephemeral private key is never an evidence artifact.
        (root / "key.pem").unlink(missing_ok=True)
        save(root / "worker-result.json", result)
    return 0 if result["passed"] else 1


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case", required=True, choices=["success", "failure", "no-account", "no-new-work"])
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--expected-build", required=True)
    p.add_argument("--expected-es-sha256", required=True)
    p.add_argument("--es-source-commit", required=True)
    p.add_argument("--xdg-runtime-dir", required=True)
    p.add_argument("--wayland-display", required=True)
    p.add_argument("--language", choices=["en_US", "fr_FR"], default="en_US")
    p.add_argument("--trigger", choices=["api", "ui"], default="api")
    p.add_argument("--disposable-guest", action="store_true", required=True)
    p.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    a = p.parse_args()
    check(os.geteuid() == 0, "disposable guest root required")
    check(re.fullmatch(r"[0-9a-f]{64}", a.expected_es_sha256), "exact binary SHA256 required")
    check(re.fullmatch(r"[0-9a-f]{40}", a.es_source_commit), "full coordinator-declared ES source commit required")
    check(a.output.parent.resolve() == Path("/tmp") and re.fullmatch(r"pix567-[a-zA-Z0-9_-]+", a.output.name),
          "output must be a new /tmp/pix567-NAME directory")
    a.output = a.output.absolute()
    identity = dict(line.split("=", 1) for line in Path("/etc/os-release").read_text().splitlines() if "=" in line)
    check(identity.get("BUILD_ID", "").strip('"') == a.expected_build, "BUILD_ID mismatch")
    check(digest(ES) == a.expected_es_sha256, "installed ES hash mismatch")
    check(hasattr(os, "unshare") and hasattr(os, "CLONE_NEWNET") and hasattr(os, "CLONE_NEWNS"),
          "Python os.unshare with mount/network namespace support required")
    check(hasattr(os, "pidfd_open") and hasattr(signal, "pidfd_send_signal"), "pidfd cleanup support required")
    check(socket.if_nameindex() == [(1, "lo")], "allocate VM with no NIC; parent namespace must have only lo")
    if a.worker:
        return worker(a)
    # Also refuse a NIC in the guest's parent namespace. This closes escape via
    # an existing privileged broker (systemd/D-Bus), outside the child's netns.
    check(not a.output.exists(), "refusing reused output")
    for proc in Path("/proc").glob("[0-9]*"):
        try:
            executable = os.readlink(proc / "exe").removesuffix(" (deleted)")
            check(Path(executable).name != "emulationstation", "coordinator must stop the existing ES first")
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            pass
    for tool in ["mount", "ip", "openssl"]:
        check(shutil.which(tool, path=clean_env(a)["PATH"]) is not None, "missing installed prerequisite: " + tool)
    check(os.access(HERE / "raofflineproxy-ctl", os.X_OK), "ctl seam must be executable")
    check(Path(a.xdg_runtime_dir).is_absolute() and "/" not in a.wayland_display,
          "explicit runtime directory and socket basename required")
    check(stat.S_ISSOCK((Path(a.xdg_runtime_dir) / a.wayland_display).stat().st_mode), "Wayland socket missing")
    for path in [Path("/usr/config/emulationstation/resources"), Path("/usr/share/themes/es-theme-art-book-next"),
                 Path("/usr/config/locale"), *HOST_FILES, CA, CTL]:
        check(path.exists(), "missing installed prerequisite: " + str(path))
    before = census()
    a.output.mkdir(mode=0o700)
    save(a.output / "case.json", {"case": a.case})
    save(a.output / "before.json", before)
    save(a.output / "binding.json", {"build_id": a.expected_build, "es_sha256": a.expected_es_sha256,
                                     "declared_es_source": a.es_source_commit,
                                     "fixture_sha256": {str(f.relative_to(HERE)): digest(f) for f in sorted(HERE.rglob("*")) if f.is_file()}})
    with (a.output / "worker.stdout").open("wb") as out, (a.output / "worker.stderr").open("wb") as err:
        child = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), *sys.argv[1:], "--worker"],
                                 env=clean_env(a), stdout=out, stderr=err, start_new_session=True)
    pidfile(a.output, "owner", child)
    forced = False
    interrupted = None

    def interrupt(signum, frame):
        raise InterruptedError(signum)
    signal.signal(signal.SIGTERM, interrupt)
    signal.signal(signal.SIGINT, interrupt)
    try:
        code = child.wait(timeout=LIMIT)
    except (subprocess.TimeoutExpired, InterruptedError) as error:
        forced = isinstance(error, subprocess.TimeoutExpired)
        interrupted = error.args[0] if isinstance(error, InterruptedError) else None
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        code = child.wait()
    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    # Retire stragglers by unique namespace inode, not an argv pattern. Never
    # signal a process just because its PID was recorded earlier.
    ns_path = a.output / "namespaces.json"
    retired = []
    if ns_path.exists():
        namespaces = json.loads(ns_path.read_text())
        for proc in Path("/proc").glob("[0-9]*"):
            fd = None
            try:
                fd = os.pidfd_open(int(proc.name))
                if os.readlink(proc / "ns/mnt") == namespaces["mnt"] and os.readlink(proc / "ns/net") == namespaces["net"]:
                    signal.pidfd_send_signal(fd, signal.SIGKILL)
                    retired.append(int(proc.name))
            except (FileNotFoundError, ProcessLookupError):
                pass
            finally:
                if fd is not None:
                    os.close(fd)
    def still_in_namespace():
        if not ns_path.exists():
            return []
        remaining = []
        for proc in Path("/proc").glob("[0-9]*"):
            try:
                if os.readlink(proc / "ns/mnt") == namespaces["mnt"] and os.readlink(proc / "ns/net") == namespaces["net"]:
                    remaining.append(int(proc.name))
            except (FileNotFoundError, ProcessLookupError):
                pass
        return remaining
    end = time.monotonic() + 3
    remaining = still_in_namespace()
    while remaining and time.monotonic() < end:
        time.sleep(0.1)
        remaining = still_in_namespace()
    (a.output / "key.pem").unlink(missing_ok=True)
    after = census()
    save(a.output / "after.json", after)
    result = {"worker_exit": code, "timeout": forced, "interrupted_signal": interrupted, "stragglers_killed": retired,
              "namespace_processes_remaining": remaining,
              "parent_unchanged": before == after, "runtime_test_was_run": True}
    result["passed"] = code == 0 and not forced and interrupted is None and not retired and not remaining and before == after
    save(a.output / "result.json", result)
    print(json.dumps(result), flush=True)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
