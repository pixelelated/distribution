"""S14 (#678, #1256): std::sort under libstdc++'s debug mode over SaveStateOrder::newestFirst.

    python3 -I s14-sort-debug.py <es tree>

Compiles es-app/src/SaveStateOrder.h with -D_GLIBCXX_DEBUG and sorts forty
states, three dates among them, as the manager's grid would; the debug mode
checks the comparator's irreflexivity and aborts when it fails. PASS when
the sort finishes."""
import subprocess
import sys
import tempfile
from pathlib import Path

ES = Path(sys.argv[1])
prog = r'''
#include "SaveStateOrder.h"
#include <algorithm>
#include <cstdio>
#include <vector>
struct State { long date; int slot; };
int main() {
  std::vector<State> v;
  for (int i = 0; i < 40; i++) v.push_back({ 1789000000 + (i % 3) * 60, 40 - i });
  std::sort(v.begin(), v.end(), [](const State& a, const State& b) { return SaveStateOrder::newestFirst(a.date, a.slot, b.date, b.slot); });
  std::printf("sorted %zu states under _GLIBCXX_DEBUG\n", v.size());
}
'''
with tempfile.TemporaryDirectory(prefix="s14-", dir="/workspace/tmp/m6-t31/tmp") as d:
    (Path(d) / "a.cpp").write_text(prog)
    b = subprocess.run(["g++", "-std=c++17", "-D_GLIBCXX_DEBUG", "-I", str(ES / "es-app/src"), str(Path(d) / "a.cpp"), "-o", str(Path(d) / "a")], capture_output=True, text=True)
    if b.returncode:
        print("FAIL s14: does not compile\n" + b.stderr[-1500:]); sys.exit(2)
    r = subprocess.run([str(Path(d) / "a")], capture_output=True, text=True, timeout=30)
    out = (r.stdout + r.stderr).strip().splitlines()
    print("\n".join(l for l in out if l.strip())[:600])
    if r.returncode:
        print("FAIL s14: rc %d -- the debug mode refused the comparator" % r.returncode); sys.exit(1)
print("s14: PASS")
