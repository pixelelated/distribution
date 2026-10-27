"""3.27 (#679): SystemView's fast move leaves the carousel cursor out of range.

    python3 -I l327-cursor-range.py <SystemView.cpp> [--control]

_moveCursorInRange is extracted as written and run for every carousel of 1 to
12 systems, every cursor, and the four steps moveCursorFast passes (+-1, +-10).
The value it leaves must be an index, 0 <= value < size, and moveCursorFast
returns it as one. At the pin a backward step of 10 on fewer than 10 systems
adds the size once and stops: (2, -10, 5) leaves -3 -- FAIL.
Also printed: whether the caller's delta (cursor - mCursor, the only use the
input handler makes of it, SystemView.cpp:407/413/431/437) is congruent to the
right move modulo the size. When it is, a carousel that wraps hides the defect,
which is what G-04 saw on the image.
--control runs a constructed modulo body, to show the case can pass.
History: 1d9212bec (upstream, "systemview : better scroll when sorted by
manufacturer") wrote it; nothing since.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
fn = function(src, r"^static void _moveCursorInRange\(int& value, int count, int sz\)", "3.27")
if "--control" in sys.argv:
    fn = "static void _moveCursorInRange(int& value, int count, int sz)\n{ if (sz <= 0) return; value = ((value + count) % sz + sz) % sz; }"
harness = "#include <cstdio>\n#include <initializer_list>\n" + fn + r'''
int main() {
    int bad = 0, cases = 0, congruent = 0;
    for (int sz = 1; sz <= 12; sz++)
        for (int c = 0; c < sz; c++)
            for (int step : {-10, -1, 1, 10}) {
                int v = c; _moveCursorInRange(v, step, sz); cases++;
                int want = ((c + step) % sz + sz) % sz;
                if (((v - c) % sz + sz) % sz == ((want - c) % sz + sz) % sz) congruent++;
                if (v < 0 || v >= sz) { if (bad < 6) printf("out of range: (%d, %d, %d) leaves %d\n", c, step, sz, v); bad++; }
            }
    printf("%d cases, %d out of range, %d with the caller's delta congruent to the right move\n", cases, bad, congruent);
    if (bad) { printf("FAIL 3.27: the fast move leaves the carousel cursor outside 0..size-1\n"); return 1; }
    return 0;
}
'''
run(harness, "l327")
