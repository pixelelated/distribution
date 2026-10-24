"""cleanup-probe.py -- T14 S11's harness for #1011: load a pair tool, make a
Proof over a fresh output directory (no guest, no backend), and call its own
cleanup() as a run whose pair was started would. A stand-in pidfile names a
pid no process holds, standing for a guest a sandbox hides (#506). The tool's
local() is replaced by a recorder, so nothing is run. Prints the
cleanup.json it wrote and what it called. VM_QEMU_RUNTIME_DIR is set to the
given scratch directory, so the stand-in pidfile is written there, never under
/tmp; no bytecode is written beside the tool.
    python3 -I -B cleanup-probe.py <tool> <historical tree> <fresh output dir> <invisible pid> <runtime dir>
"""
import json, os, sys, types
sys.dont_write_bytecode = True
os.environ["VM_QEMU_RUNTIME_DIR"] = sys.argv[5]
from importlib.machinery import SourceFileLoader
from pathlib import Path
tool = SourceFileLoader("pair", sys.argv[1]).load_module()
args = types.SimpleNamespace(tree=Path(sys.argv[2]), output=Path(sys.argv[3]), image=None, build_id=None,
                             case=None, inject_failure=False)
proof = tool.Proof(args)
called = []
proof.local = lambda *a, **k: called.append(list(a))
proof.pair_attempted = True
runtime = getattr(proof, "runtime", None)
if runtime is not None:
    runtime.mkdir(mode=0o700, exist_ok=True)
    (runtime / "rocknix-qemu.pid").write_text(sys.argv[4] + "\n")
try:
    proof.cleanup()
    outcome = "returned"
except AssertionError as error:
    outcome = "refused: " + str(error)
print(json.dumps({"outcome": outcome, "called": called,
                  "cleanup": json.loads((Path(sys.argv[3]) / "cleanup.json").read_text())}))
