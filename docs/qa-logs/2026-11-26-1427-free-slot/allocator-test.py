#!/usr/bin/env python3
# #1427 criterion 1: the production allocator, SaveStateRepository::getNextFreeSlot,
# compiled from the exact bytes of two EmulationStation revisions against stub
# collaborators, and run over the same cases.
#
#   python3 -I allocator-test.py --es <ES checkout> --baseline <rev> --candidate <rev> --out <dir>
#
# The function body is cut from `git show <rev>:es-app/src/SaveStateRepository.cpp`
# (from its definition line to the first closing brace at column 0) and
# compiled unchanged inside a stub SaveStateRepository. Only the collaborators
# are synthetic: isEnabled(), the FileData -> SystemData -> repository chain,
# and getSaveStates(), which hands back the case's slots (-1 is the AUTO SAVE).
#
# Exit 0: the candidate answers every case as expected. 1: it does not.
# 2: cannot run. The baseline is expected to fail the autosave-only cases;
# its own exit is recorded, not judged.
import argparse, hashlib, json, os, subprocess, sys

CASES = [
    # name, enabled, firstslot (None = no config), slots present, expected
    ("disabled",                 False, None, [],            -99),
    ("empty, no config",         True,  None, [],            0),
    ("empty, firstslot 0",       True,  0,    [],            0),
    ("empty, firstslot 1",       True,  1,    [],            1),
    ("empty, firstslot 7",       True,  7,    [],            7),
    ("autosave only, no config", True,  None, [-1],          0),
    ("autosave only, firstslot 0", True, 0,   [-1],          0),
    ("autosave only, firstslot 1", True, 1,   [-1],          1),
    ("autosave only, firstslot 7", True, 7,   [-1],          7),
    ("slot 0",                   True,  None, [0],           1),
    ("slots 0 1 2",              True,  None, [0, 1, 2],     3),
    ("gap 0 2",                  True,  None, [0, 2],        3),
    ("autosave and slot 3",      True,  None, [-1, 3],       4),
    ("high bound 99999",         True,  None, [99999],       100000),
]

HARNESS = r'''
#include <algorithm>
#include <cstdio>
#include <memory>
#include <vector>

struct SaveStateConfig { int firstslot; };
struct SaveState { int slot; };
struct SaveStateRepository;
struct SystemData { SaveStateRepository* repo; SaveStateRepository* getSaveStateRepository() { return repo; } };
struct FileData { SystemData* sys; FileData* getSourceFileData() { return this; } SystemData* getSystem() { return sys; } };

static bool g_enabled = true;
static std::vector<SaveState*> g_states;

struct SaveStateRepository {
    static bool isEnabled(FileData*) { return g_enabled; }
    std::vector<SaveState*> getSaveStates(FileData*, std::shared_ptr<SaveStateConfig> = nullptr) { return g_states; }
    static int getNextFreeSlot(FileData* game, std::shared_ptr<SaveStateConfig> config);
};

#include "allocator-body.inc"

int main()
{
    SaveStateRepository repo; SystemData sys{&repo}; FileData game{&sys};
    struct C { const char* name; bool enabled; int firstslot; bool hasConfig; std::vector<int> slots; };
    const C cases[] = {
%CASES%
    };
    for (const C& c : cases)
    {
        g_enabled = c.enabled;
        std::vector<SaveState> backing; backing.reserve(c.slots.size());
        g_states.clear();
        for (int s : c.slots) { backing.push_back(SaveState{s}); }
        for (auto& b : backing) g_states.push_back(&b);
        std::shared_ptr<SaveStateConfig> cfg = c.hasConfig ? std::make_shared<SaveStateConfig>(SaveStateConfig{c.firstslot}) : nullptr;
        std::printf("%s\t%d\n", c.name, SaveStateRepository::getNextFreeSlot(&game, cfg));
    }
    return 0;
}
'''


def sha(b):
    return hashlib.sha256(b).hexdigest()


def body(es, rev):
    src = subprocess.run(["git", "-C", es, "show", f"{rev}:es-app/src/SaveStateRepository.cpp"],
                         check=True, capture_output=True).stdout
    lines = src.decode("utf-8").splitlines(keepends=True)
    start = next(i for i, l in enumerate(lines) if l.startswith("int SaveStateRepository::getNextFreeSlot("))
    end = next(i for i in range(start, len(lines)) if lines[i].rstrip("\r\n") == "}")
    text = "".join(lines[start:end + 1])
    return src, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--es", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    a.out = os.path.abspath(a.out)
    if os.path.exists(a.out):
        print(f"cannot run: {a.out} exists", file=sys.stderr)
        return 2
    os.makedirs(a.out)
    rows = ",\n".join(
        '        {"%s", %s, %d, %s, {%s}}' % (n, "true" if e else "false", 0 if f is None else f,
                                             "false" if f is None else "true", ", ".join(map(str, s)))
        for n, e, f, s, _ in CASES)
    harness = HARNESS.replace("%CASES%", rows)
    record = {"cases": [{"name": n, "enabled": e, "firstslot": f, "slots": s, "expected": x}
                        for n, e, f, s, x in CASES], "modes": {}}
    candidate_ok = None
    for mode, rev in (("baseline", a.baseline), ("candidate", a.candidate)):
        full = subprocess.run(["git", "-C", a.es, "rev-parse", rev], check=True, capture_output=True, text=True).stdout.strip()
        src, text = body(a.es, rev)
        d = os.path.join(a.out, mode)
        os.makedirs(d)
        with open(os.path.join(d, "allocator-body.inc"), "w") as f:
            f.write(text)
        with open(os.path.join(d, "harness.cpp"), "w") as f:
            f.write(harness)
        cc = subprocess.run(["g++", "-std=c++17", "-Wall", "-o", os.path.join(d, "test"), os.path.join(d, "harness.cpp")],
                            capture_output=True, text=True, cwd=d)
        with open(os.path.join(d, "compile.txt"), "w") as f:
            f.write(f"rc {cc.returncode}\n{cc.stdout}{cc.stderr}")
        if cc.returncode != 0:
            print(f"cannot run: {mode} did not compile (see {d}/compile.txt)", file=sys.stderr)
            return 2
        run = subprocess.run([os.path.join(d, "test")], capture_output=True, text=True)
        os.remove(os.path.join(d, "test"))  # the record keeps its output, not the binary
        with open(os.path.join(d, "stdout.txt"), "w") as f:
            f.write(run.stdout)
        got = dict(l.split("\t") for l in run.stdout.splitlines())
        mism = [{"name": n, "expected": x, "got": int(got[n])} for n, _, _, _, x in CASES if int(got.get(n, "-12345")) != x]
        if len(got) != len(CASES):
            print(f"cannot run: {mode} printed {len(got)} of {len(CASES)} cases", file=sys.stderr)
            return 2
        record["modes"][mode] = {
            "rev": full, "file_sha256": sha(src), "body_sha256": sha(text.encode()),
            "run_rc": run.returncode, "stdout_sha256": sha(run.stdout.encode()),
            "matching": len(CASES) - len(mism), "mismatches": mism,
        }
        if mode == "candidate":
            candidate_ok = run.returncode == 0 and not mism
    with open(os.path.join(a.out, "RESULT.json"), "w") as f:
        json.dump(record, f, indent=2)
    for mode, m in record["modes"].items():
        print(f"{mode} {m['rev'][:10]} body {m['body_sha256'][:16]}: {m['matching']} of {len(CASES)} as expected"
              + "".join(f"\n  {x['name']}: got {x['got']}, want {x['expected']}" for x in m["mismatches"]))
    print("PASS: the candidate answers every case" if candidate_ok else "FAIL: the candidate does not answer every case")
    return 0 if candidate_ok else 1


sys.exit(main())
