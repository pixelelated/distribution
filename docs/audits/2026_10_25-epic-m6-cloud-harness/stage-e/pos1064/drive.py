#!/usr/bin/env python3
"""#1064: step 25's probe where no es_systems.cfg exists (the host has none
at either path, asserted), so it reads no ES path (unfixed: the command from
the AST, its .split(); fixed: es_path_orphans()). Control on the fixed tool:
a stub rewriting only the config's path to a planted file of three paths
under $TMPDIR, and a fake backuptool naming one -> 3 read, 1 orphan.
    python3 -I -B pos1064/drive.py <cloud-round-trip> unfixed|fixed"""
import ast, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import args, load, scratch, verdict

tool, expect = args()
CFG = "/storage/.config/emulationstation/es_systems.cfg"
for p in (CFG, "/usr/config/emulationstation/es_systems.cfg"):
    if os.path.exists(p):
        sys.exit(f"{p} exists on this host; the empty-probe case needs neither path present")
class HostDev:
    host, port = "host", 0
    def __init__(self, cfg=None, path=None): self.cfg, self.path = cfg, path
    def run(self, cmd, check=True):
        if self.cfg: cmd = cmd.replace(CFG, self.cfg)
        env = dict(os.environ, PATH=self.path) if self.path else None
        return subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, env=env).stdout
crt = load(tool)
if hasattr(crt, "es_path_orphans"):
    n, orphans = crt.es_path_orphans(HostDev())
    passes = n > 0 and not orphans
    root = scratch("pos1064")
    os.makedirs(f"{root}/bin")
    open(f"{root}/es_systems.cfg", "w").write("<systemList>\n<system><path>/storage/roms/nes</path></system>\n"
        "<system><path>/storage/.config/foo</path></system>\n<system><path>/storage/.config/bar</path></system>\n</systemList>\n")
    open(f"{root}/bin/backuptool", "w").write("#!/bin/sh\n# carries /storage/.config/foo\n"); os.chmod(f"{root}/bin/backuptool", 0o755)
    control = crt.es_path_orphans(HostDev(f"{root}/es_systems.cfg", f"{root}/bin:/usr/bin:/bin"))
    print(f"paths read: {n}; orphans: {orphans}; step 25 would read {'PASS' if passes else 'FAIL'}; control: {control}")
    observed = "fixed" if not passes and control == (3, ["/storage/.config/bar"]) else "neither"
else:
    tree = ast.parse(open(tool).read())
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "orphans")
    cmd = eval(compile(ast.Expression(node.value.func.value.args[0]), tool, "eval"), {})
    orphans = HostDev().run(cmd).split()
    passes = not orphans
    print(f"orphans: {orphans}; step 25 ('not orphans') would read {'PASS' if passes else 'FAIL'}")
    observed = "unfixed" if passes else "neither"
verdict("pos1064", expect, observed, f"the empty probe {'passes' if passes else 'fails'} step 25")
