#!/usr/bin/env python3
"""UNRUN: bytecode-only import attribution with the executing interpreter.

Run only after runtime allocation. No database, listener, provider or service.
Uses check.py's deny-all network/file-write guard before proxy imports.
"""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import py_compile
import shutil
import sqlite3
import ssl
import subprocess
import sys
import time

from check import install_guard


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new private path")
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    prepared, output = args.prepared.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    if args.worker:
        for key in list(os.environ):
            if key.startswith("RAOFFLINEPROXY_"):
                os.environ.pop(key)
        os.environ["RAOFFLINEPROXY_CONFIG_DIR"] = str(output)
        os.environ["RAOFFLINEPROXY_CACHE_IMAGES"] = "0"
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(prepared))
        install_guard(prepared, output)
        started = time.perf_counter_ns()
        module = importlib.import_module("raofflineproxy.main")
        elapsed = time.perf_counter_ns() - started
        expected = prepared / "raofflineproxy/main.pyc"
        assert Path(module.__file__).resolve() == expected
        modules = sorted(n for n in sys.modules if n.startswith("raofflineproxy."))
        stats = {}
        for line in Path("/proc/self/smaps_rollup").read_text().splitlines():
            name, _, value = line.partition(":")
            if name in {"Pss", "Rss", "Pss_Anon", "Pss_File", "Private_Clean", "Private_Dirty"}:
                stats[name + "_KiB"] = int(value.split()[0])
        print(json.dumps({"memory": stats, "import_ns": elapsed, "modules": modules,
                          "main_pyc_sha256": sha(expected), "pygame_loaded": "pygame" in sys.modules}))
        return
    started = time.monotonic()
    manifest = json.loads((prepared / "source.json").read_text())
    bytecode = {}
    for variant in ("baseline", "candidate"):
        for name, digest in manifest[variant].items():
            assert sha(prepared / variant / name) == digest, name
        root = output / variant
        shutil.copytree(prepared / variant / "linux/raofflineproxy", root / "raofflineproxy")
        for source in sorted(root.rglob("*.py")):
            py_compile.compile(str(source), cfile=str(source.with_suffix(".pyc")),
                               dfile=str(source.relative_to(root)), doraise=True)
            source.unlink()  # Only the freshly created diagnostic copy.
        assert not list(root.rglob("*.py"))
        bytecode[variant] = {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*.pyc"))}
    records = []
    report = {"python": sys.version, "executable": sys.executable,
              "executable_sha256": sha(Path(sys.executable)), "sqlite": sqlite3.sqlite_version,
              "openssl": ssl.OPENSSL_VERSION, "source_manifest_sha256": sha(prepared / "source.json"),
              "fixture_sha256": sha(Path(__file__)), "guard_sha256": sha(Path(__file__).with_name("check.py")),
              "bytecode": bytecode, "results": records, "scope": "bytecode-only imports; no service"}
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", MALLOC_ARENA_MAX="2")
    for index, variant in enumerate(("baseline", "candidate", "candidate", "baseline", "baseline", "candidate")):
        remaining = 55 - (time.monotonic() - started)
        assert remaining > 0, "budget exceeded"
        cmd = [sys.executable, "-B", str(Path(__file__).resolve()), "--worker",
               "--prepared", str(output / variant), "--output", str(output / f"state-{index}")]
        with subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as child:
            try:
                stdout, stderr = child.communicate(timeout=min(8, remaining))
            except subprocess.TimeoutExpired:
                child.kill()
                stdout, stderr = child.communicate()
            item = {"variant": variant, "pid": child.pid, "rc": child.returncode,
                    "exited": child.poll() is not None, "stderr": stderr}
            if child.returncode == 0:
                item["result"] = json.loads(stdout)
            else:
                item["stdout"] = stdout
            records.append(item)
        report["elapsed_seconds"] = time.monotonic() - started
        report["scratch_bytes"] = sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
        (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
        assert child.returncode == 0, item
        assert report["scratch_bytes"] < 20 * 1024 * 1024
        loaded = "raofflineproxy.menu_sdl" in item["result"]["modules"]
        assert loaded == (variant == "baseline")
        assert not item["result"]["pygame_loaded"]
    print(json.dumps({"result": "PASS", "seconds": time.monotonic() - started,
                      "scope": report["scope"]}))


if __name__ == "__main__":
    main()
