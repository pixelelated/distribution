#!/usr/bin/env python3
"""#1093's host positive: do A15's two log checks pass what cloud_restore
logs today?

    python3 -I -B drive.py <path to cloud-round-trip> unfixed|fixed

Runs this tree's select_settings_archives (rasteratops-settings-archive) over
A15's layout on a local rclone remote -- first only the old (poisoned)
folder, then the old folder and the device's own -- with the image's rclone
($T13_CLIENT, default the M6 donor's), renders cloud_restore's own folder
line and the previous tier's WARN from this tree, and the same lines as
cloud_restore wrote them before f864baac02 (git show f864baac02^). Each of
A15's two checks is taken from the tool's AST as written and evaluated on
both. Writes only under $TMPDIR.
"""
import ast, importlib.machinery, importlib.util, os, pathlib, re, shutil, subprocess, sys

tool, want = sys.argv[1], sys.argv[2]
REPO = pathlib.Path(__file__).resolve().parents[5]
SRC = REPO / "projects/ROCKNIX/packages/network/rclone/sources"
client = os.environ.get("T13_CLIENT", "/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone")
W = pathlib.Path(os.environ["TMPDIR"]) / "pos1093"
shutil.rmtree(W, ignore_errors=True)
(W / "bin").mkdir(parents=True)
os.symlink(client, W / "bin/rclone")

poisoned, legacy, expected = "GENERIC-X64-15ca-ee5013fc56", "GENERIC-X64-15ca-15ca35b6b4", "GENERIC-X64-15ca35b6b4"
idtool = W / "cloud_device_id"
idtool.write_text("#!/bin/sh\ncase \"$1\" in\n"
                  f"  --legacy) echo {legacy} ;;\n"
                  f"  --previous) printf '%s\\n' {poisoned} GENERIC-X64-ee5013fc56 ;;\n"
                  f"  *) echo {expected} ;;\nesac\n")
idtool.chmod(0o755)


def select(layout):
    root = W / "cloud"
    shutil.rmtree(root, ignore_errors=True)
    for folder, name in layout:
        (root / "Backups" / folder).mkdir(parents=True, exist_ok=True)
        (root / "Backups" / folder / name).write_bytes(b"x")
    env = dict(os.environ, PATH=f"{W / 'bin'}:{os.environ['PATH']}", RCLONE_CONFIG_QA_TYPE="local")
    out = subprocess.run(["bash", "-c", f'RCLONE_LIST_OPTS=(); . "{SRC}/rasteratops-settings-archive"; '
                          f'select_settings_archives "qa:{root}/Backups" "{idtool}"; rc=$?; '
                          'printf "%s|%s|%s\\n" "$rc" "$SETTINGS_ARCHIVE_SOURCE" "$SETTINGS_ARCHIVE_KIND"'],
                         capture_output=True, text=True, env=env).stdout.strip()
    rc, source, kind = out.split("|")
    if rc != "0" or not source:
        sys.exit(f"pos1093: UNEXPECTED (the selector returned rc {rc}, source {source!r})")
    return source, kind


def fmt(script_text, needle):
    line = next(l for l in script_text.splitlines() if needle in l and "log_message" in l)
    return re.search(r'log_message "([^"]*)"', line).group(1)


def logged(msg, level="INFO"):
    return f"[2026-10-25 04:04:26] [{level}] [cloud_restore] {msg}\n"


tail_end = logged("Completed.") + logged("Script completed in 2 seconds with exit code 0")
now = (SRC / "cloud_restore").read_text()
then = subprocess.run(["git", "-C", str(REPO), "show", "f864baac02^:projects/ROCKNIX/packages/network/rclone/sources/cloud_restore"],
                      capture_output=True, text=True, check=True).stdout

src1, kind1 = select([(poisoned, "2026_01_01-000000-ROCKNIX_SETTINGS.tar.gz")])
src2, kind2 = select([(poisoned, "2026_01_01-000000-ROCKNIX_SETTINGS.tar.gz"),
                      (expected, "2026_01_02-000000-GENERIC-X64-ROCKNIX_SETTINGS.tar.gz")])
print(f"selector: old folder only -> {kind1} {src1.rsplit('/', 1)[-1]}; with its own -> {kind2} {src2.rsplit('/', 1)[-1]}")
line = fmt(now, "device folder)")
warn = fmt(now, "may have shared with another")
shipped = {
    "c1": logged(line.replace("${restore_src}", src1).replace("${SETTINGS_ARCHIVE_KIND}", kind1))
          + (logged(warn, "WARN") if kind1 == "previous" else "") + tail_end,
    "c2": logged(line.replace("${restore_src}", src2).replace("${SETTINGS_ARCHIVE_KIND}", kind2)) + tail_end,
}
old = {
    "c1": logged(fmt(then, "while its id was the shared constant").replace("${previous_name}", poisoned), "WARN") + tail_end,
    "c2": logged(fmt(then, "own cloud folder (").replace("${own_name}", expected)) + tail_end,
}

loader = importlib.machinery.SourceFileLoader("crt", tool)
spec = importlib.util.spec_from_loader("crt", loader)
crt = importlib.util.module_from_spec(spec)
loader.exec_module(crt)
source = open(tool).read()
fn = next(n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.FunctionDef) and n.name == "fx_a15")
preds = {}
for call in ast.walk(fn):
    if isinstance(call, ast.Call) and getattr(call.func, "id", "") == "check" and len(call.args) == 3:
        msg = ast.get_source_segment(source, call.args[2])
        for key, start in (("c1", 'f"the log did not name the folder'), ("c2", 'f"the log did not:')):
            if msg.startswith(start):
                preds[key] = ast.get_source_segment(source, call.args[0])
if set(preds) != {"c1", "c2"}:
    sys.exit(f"pos1093: UNEXPECTED (found the checks {sorted(preds)})")

res = {}
for key in ("c1", "c2"):
    for which, tails in (("shipped", shipped), ("old", old)):
        ok = bool(eval(preds[key], vars(crt), {"tail": tails[key], "poisoned": poisoned, "expected": expected}))
        res[(key, which)] = ok
        print(f"{key} ({'names the folder and why' if key == 'c1' else 'its own folder'}) on the {which} wording: {'passes' if ok else 'fails'}")
shipped_ok = res[("c1", "shipped")] and res[("c2", "shipped")]
old_ok = res[("c1", "old")] or res[("c2", "old")]
detail = f"shipped {'pass' if shipped_ok else 'fail'}, old wording {'passes' if old_ok else 'fails'}"
if want == "fixed" and shipped_ok and not old_ok:
    print(f"pos1093: fixed-expectation-met ({detail})")
elif want == "unfixed" and not res[("c1", "shipped")] and not res[("c2", "shipped")]:
    print(f"pos1093: unfixed-expectation-met ({detail})")
else:
    print(f"pos1093: UNEXPECTED ({want}: {detail})")
    sys.exit(1)
