"""T18 (#665, #1148): the two readers' wrappers with the reader gone, and a
protocol line after rclone's last progress block (PL-19).

    python3 -I -B docs/audits/2026_10_26-epic-m6-es-cloud-pages/tools/t18-wrapper-fixture.py \
        <es tree> <rev or WORKTREE> <scratch dir> --expect unfixed|fixed [--rclone <path>]

Part 1, the wrappers. The wrapper each reader builds is read out of its
source at <rev> (`ThreadedCloudSync.cpp`, the card; `CloudTransferJob.cpp`,
the job): the C++ string concatenation handed to Utils::String::shellQuote,
with mCommand replaced by a test script, then run as the reader runs it,
`sh -c "setsid sh -c '<wrapped>' 2>&1"`, its stdout a pipe. The script
writes a line, waits, writes another, then its stamp. Two cases per wrapper:
  late    the reader takes the first line, then closes (the interface gone
          mid-sync): the script's second write meets a closed pipe;
  at-once the reader closes before reading anything: the wrapper's own
          pid echo meets a closed pipe (the seats' A-3: the trap after it).
A wrapper survives a case when the script's stamp exists afterwards.
`--expect unfixed` is met when the job's wrapper survives `late` and the
card's does not (#1148 as filed); `--expect fixed` when both survive both.

Part 2, the glued line (PL-19, A-35). With --rclone, `rclone copy` between
two scratch folders with the content scripts' flags (`--progress --stats 1s
--log-file ... --log-level INFO`), piped, followed in the same shell by
`echo '>>> tier T|0'`: the byte before `>>> ` is read. A newline or a
carriage return there means the readers see the marker at a line's start;
anything else means it is glued and lost. Recorded, not asserted: the
stream fixes PL-19 only if this falls.

Writes only under <scratch dir>. Exit 0 when the expectation is met; 1 when
not; 2 when it cannot run.
"""
import os, re, shutil, subprocess, sys, time

ES, REV, S = sys.argv[1:4]
assert sys.argv[4] == "--expect"
EXPECT = sys.argv[5]
RCLONE = sys.argv[sys.argv.index("--rclone") + 1] if "--rclone" in sys.argv else None
os.makedirs(S, exist_ok=True)


def src(path):
    if REV == "WORKTREE":
        return open(os.path.join(ES, path)).read()
    r = subprocess.run(["git", "-C", ES, "show", f"{REV}:{path}"], capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr); sys.exit(2)
    return r.stdout


def cstr(lit):
    """A C++ string literal's value (the escapes these lines use)."""
    return bytes(lit[1:-1], "utf-8").decode("unicode_escape")


def wrapper(path):
    text = src(path)
    m = re.search(r'"setsid sh -c "\s*\+\s*Utils::String::shellQuote\((.*?)\)\s*\+\s*" 2>&1"', text, re.S)
    if not m:
        sys.stderr.write(f"no wrapper found in {path}\n"); sys.exit(2)
    parts = re.findall(r'"(?:[^"\\]|\\.)*"|mCommand', m.group(1))
    return lambda cmd: "".join(cmd if p == "mCommand" else cstr(p) for p in parts)


def run(wrap, case, tag):
    d = os.path.join(S, f"{tag}-{case}")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    stamp = os.path.join(d, "stamp")
    script = f"echo first; sleep 0.4; echo second; echo done > '{stamp}'"
    inner = wrap(script)
    quoted = "'" + inner.replace("'", "'\\''") + "'"
    p = subprocess.Popen(["sh", "-c", f"setsid sh -c {quoted} 2>&1"], stdout=subprocess.PIPE)
    if case == "late":
        p.stdout.readline()
        p.stdout.readline()
    p.stdout.close()
    p.wait()
    time.sleep(1.2)
    return os.path.exists(stamp)


card = wrapper("es-app/src/ThreadedCloudSync.cpp")
job = wrapper("es-app/src/CloudTransferJob.cpp")
print(f"rev {REV}; the shell: {os.path.realpath(shutil.which('sh'))}; setsid: {os.path.realpath(shutil.which('setsid'))}")
print(f"the card's wrapper: {card('CMD')!r}")
print(f"the job's wrapper:  {job('CMD')!r}")
res = {}
for tag, w in (("card", card), ("job", job)):
    for case in ("late", "at-once"):
        res[(tag, case)] = run(w, case, tag)
        print(f"{tag:4} {case:7}: the script's stamp {'WRITTEN' if res[(tag, case)] else 'not written'}")

if EXPECT == "unfixed":
    met = res[("job", "late")] and not res[("card", "late")]
else:
    met = all(res.values())
print(f"{EXPECT}-expectation-{'met' if met else 'NOT met'}")

if RCLONE:
    d = os.path.join(S, "glued")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "src"))
    for i in range(40):
        with open(os.path.join(d, "src", f"f{i:02}.bin"), "wb") as f:
            f.write(os.urandom(256 * 1024))
    cmd = (f"'{RCLONE}' copy '{d}/src' '{d}/dst' --progress --stats 1s --bwlimit 2M "
           f"--log-file '{d}/rclone.log' --log-level INFO --config /dev/null; echo '>>> tier T|0'")
    out = subprocess.run(["sh", "-c", cmd + " 2>&1"], capture_output=True).stdout
    i = out.rfind(b">>> tier")
    before = out[i - 1:i] if i > 0 else b""
    tail = out[max(0, i - 60):i]
    print(f"glued: {len(out)} bytes of output; the marker at byte {i}; the byte before it {before!r}; "
          f"the 60 before: {tail!r}")
    print("glued: the marker " + ("starts a line: PL-19 does not fall" if before in (b"\n", b"\r") or i == 0 else "IS GLUED: PL-19 falls"))
sys.exit(0 if met else 1)
