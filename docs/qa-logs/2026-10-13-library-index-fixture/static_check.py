#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Read source/AST/XML only. Never import or execute the guest fixtures."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--es", required=True, type=Path)
    parser.add_argument("--distribution", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    binding = json.loads((root / "source-bindings.json").read_text())
    checked = []
    for label, source in [("es", args.es), ("distribution", args.distribution)]:
        for entry in binding[label]["files"]:
            # Read immutable Git objects, not another worktree's uncommitted edits.
            data = subprocess.check_output(["git", "-C", str(source), "show",
                                            binding[label]["commit"] + ":" + entry["path"]])
            if hashlib.sha256(data).hexdigest() != entry["sha256"]:
                raise ValueError("source hash mismatch: " + entry["path"])
            checked.append(label + ":" + entry["path"])
    trees = {}
    for name in ["run-fixture.py", "tls-endpoints.py", "raofflineproxy-ctl", "static_check.py"]:
        trees[name] = ast.parse((root / name).read_text(), filename=name)
    xml = {p.name: ET.parse(p).getroot() for p in (root / "fixtures").iterdir()}
    assert xml["es_systems.cfg"].findtext("system/command") == "/bin/false"
    assert xml["es_systems.cfg"].findtext("system/path") == "/storage/roms/gb"
    assert xml["es_features.cfg"].find("emulator/cores/core").attrib == {"name": "gambatte", "features": "cheevos"}
    base = xml["base.gamelist.xml"].findall("game")
    new = xml["new.gamelist.xml"].findall("game")
    assert len(base) == 1 and len(new) == 2
    assert new[0].findtext("cheevosId") == base[0].findtext("cheevosId") == "4242002"
    assert new[1].findtext("path") == "./new.gb"
    assert new[1].findtext("cheevosHash") == "1" * 32 and new[1].find("cheevosId") is None
    # Inspect literals/call names without eval(), exec() or fixture imports.
    listener_calls = {n.func.id for n in ast.walk(trees["tls-endpoints.py"])
                      if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "Server" in listener_calls
    imported = {a.name.split(".")[0] for n in ast.walk(trees["tls-endpoints.py"])
                if isinstance(n, ast.Import) for a in n.names}
    assert not imported.intersection({"subprocess", "requests", "urllib", "httpx"})
    literals = {n.value for n in ast.walk(trees["tls-endpoints.py"])
                if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    assert "/dorequest.php?r=hashlibrary" in literals
    assert "/dorequest.php?r=officialgameslist" in literals
    result = {"status": "PASS static only", "source_files": checked,
              "python_ast_files": sorted(trees), "xml_files": sorted(xml),
              "runtime_fixtures_executed": False, "runtime_fixtures_imported": False,
              "compiler_used": False, "listeners_started": False}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
