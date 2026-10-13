#!/usr/bin/env python3
"""UNRUN: render one synthetic case in a fresh directory, never install it.

The coordinator stops its allocated guest frontend, supplies that guest's
settings, then installs the rendered inputs and starts the frontend itself.
Do not use with owner settings. The output includes the supplied settings.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True)
    parser.add_argument("--settings", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    fixtures = Path(__file__).resolve().parent
    spec = json.loads((fixtures / "collections.json").read_text())
    cases = {case["id"]: case for case in spec["cases"]}
    if args.case not in cases:
        raise SystemExit("unknown fixture case")
    case = cases[args.case]
    text = args.settings.read_text(encoding="utf-8-sig")
    text = re.sub(r"^\s*<\?xml[^?]*\?>", "", text, count=1)
    wrapper = ET.fromstring("<fixture>" + text + "</fixture>")
    children = list(wrapper)
    if len(children) == 1 and children[0].tag == "config":
        root = children[0]
    else:
        root = wrapper
        root.tag = "config"
    if any(node.tag not in ("bool", "int", "float", "string") for node in root):
        raise SystemExit("unexpected settings structure")
    # These controls isolate collection loading from achievement/network work.
    for node in list(root):
        if node.get("name") in ("CollectionSystemsAuto", "CheevosCheckIndexesAtStart",
                                "NetPlayCheckIndexesAtStart"):
            root.remove(node)
    if case["selection"] is not None:
        ET.SubElement(root, "string", name="CollectionSystemsAuto", value=case["selection"])
    for setting in ("CheevosCheckIndexesAtStart", "NetPlayCheckIndexesAtStart"):
        ET.SubElement(root, "bool", name=setting, value="false")
    args.out.mkdir(mode=0o700, parents=False, exist_ok=False)
    ET.ElementTree(root).write(args.out / "es_settings.cfg", encoding="utf-8", xml_declaration=True)
    (args.out / "es_settings.cfg").chmod(0o600)
    shutil.copyfile(fixtures / spec["rom_name"], args.out / spec["rom_name"])
    if case["history"]:
        shutil.copyfile(fixtures / "history.gamelist.xml", args.out / "gamelist.xml")
    # No gamelist.xml in the ROM-only case; remove only an owned prior fixture
    # gamelist between cases, with ES stopped, or use a fresh disposable guest.
    receipt = {"case": args.case, "source_commit": spec["source_commit"],
               "history": case["history"], "status": "inputs only; not installed or tested"}
    (args.out / "input-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print("PREPARED " + args.case)


if __name__ == "__main__":
    main()
