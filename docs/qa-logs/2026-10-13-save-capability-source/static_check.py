#!/usr/bin/env python3
"""Static hashes, Python AST, XML declarations and exact ES edit-scope checks only."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--es-src", type=Path, required=True)
    args = parser.parse_args()
    binding = json.loads((HERE / "source.json").read_text())
    for tree, entries in ((args.es_src, binding["es_files"]),
                          (ROOT, binding["distribution_files"])):
        for path, info in entries.items():
            assert hashlib.sha256((tree / path).read_bytes()).hexdigest() == info["sha256"], path
    assert [path for path, info in binding["es_files"].items()
            if info["sha256"] != info["base_sha256"]] == ["es-app/src/guis/GuiMenu.cpp"]
    menu_path = "es-app/src/guis/GuiMenu.cpp"
    source = (args.es_src / menu_path).read_text()
    base = subprocess.run(["git", "-C", str(args.es_src), "show",
                           binding["es_base_commit"] + ":" + menu_path],
                          check=True, capture_output=True, text=True).stdout
    start = source.index('#if defined(ROCKNIX)\n\t// Resolve AUTO through the same')
    end = source.index("#endif\n\n", start) + len("#endif\n\n")
    block = source[start:end]
    assert 'fileData->getEmulator() : systemData->getEmulator()' in block
    assert 'saveStateEmulator == "dolphin" || saveStateEmulator == "flycast"' in block
    assert '[mWindow]' in block and '_("OK")' in block
    assert all(word not in block for word in ('addSaveFunc', 'SystemConf', 'setEmulator',
                                              'runSystemCommand', 'remove(', 'delete '))
    normalized = source[:start] + source[end:]
    descriptions = (
        ('AUTO SAVE/LOAD', 'Supported emulators only. Save on exit and load on launch.',
         'Load latest save state on game launch and save state when exiting game.', 'autosave_enabled'),
        ('SHOW SAVE STATE MANAGER', 'RetroArch only. Show the manager before launching a game.',
         'Display save state manager before launching a game.', 'showSaveStates'))
    for label, new, old, component in descriptions:
        old_line = f'\ts->addWithDescription(_("{label}"), _("{old}"), {component});'
        guard = f'#if defined(ROCKNIX)\n\ts->addWithDescription(_("{label}"), _("{new}"), {component});\n#else\n{old_line}\n#endif'
        assert normalized.count(guard) == 1
        normalized = normalized.replace(guard, old_line)
    assert normalized == base, "change escaped the three reviewed blocks"
    feature_path = ROOT / "projects/ROCKNIX/packages/ui/emulationstation/config/common/es_features.cfg"
    features = ET.parse(feature_path).getroot()
    for name in ("dolphin", "flycast"):
        emulator = features.find(f".//emulator[@name='{name}']")
        assert emulator is not None
        assert all('autosave' not in [f.strip() for f in node.get('features', '').split(',')]
                   for node in emulator.iter())
        assert emulator.find(".//feature[@name='autosave']") is None
    manager = ET.parse(ROOT / "projects/ROCKNIX/packages/ui/emulationstation/config/common/es_savestates.cfg").getroot()
    assert [e.get("name") for e in manager.findall("emulator")] == ["retroarch"]
    assert manager.find("emulator").get("autosave") == "true"
    for package, script in (("dolphin-sa", "start_dolphin_gc.sh"),
                            ("dolphin-sa", "start_dolphin_wii.sh"),
                            ("flycast-sa", "start_flycast.sh")):
        path = ROOT / ("projects/ROCKNIX/packages/emulators/standalone/" + package + "/scripts/" + script)
        assert not re.search(r'get_setting[^\n]*autosave|global\.autosave', path.read_text())
    for path in HERE.glob("*.py"):
        ast.parse(path.read_bytes(), filename=str(path))
    cases = json.loads((HERE / "capability-cases.json").read_text())
    assert len(cases["cases"]) * len(cases["preferences"]) == 64
    assert cases["runtime"] == "UNRUN"
    print(json.dumps({"status": "PASS", "evidence": "STATIC ONLY",
                      "es_candidate_commit": binding["es_candidate_commit"],
                      "es_product_changed": [menu_path], "changed_blocks": 3,
                      "other_es_bytes_and_settings_callbacks_unchanged": True,
                      "source_hashes": "8 ES + 18 distribution files match",
                      "standalone_feature_declarations": "no autosave",
                      "manager_declaration": "retroarch only",
                      "fixture_python_ast_and_case_json": "parsed, not imported or executed",
                      "cpp_syntax_compiler_fixture_vm_frames": "UNRUN"}, indent=2))


if __name__ == "__main__":
    main()
