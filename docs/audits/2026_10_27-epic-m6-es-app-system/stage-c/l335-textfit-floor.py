"""3.35 (#680, L-20): TextFit::fitOneLine's floor, the header as written.

    python3 -I l335-textfit-floor.py <TextFit.h> [--control]

The pin's TextFit.h, included whole, with a measure of one pixel per UTF-8
character. The rule asserted: when the width is too small for anything, the
floor keeps the same number of characters whatever the script (L-20: the
floor `text.size() > 4` at :34 counts bytes). At the pin an ASCII name
keeps four characters and a Japanese one keeps one; a two-character ASCII
name keeps both and a two-character Japanese name keeps one. --control
counts characters in the floor, the lane's proposed fix, and must PASS.
The header's own three cases (tests/app-unit/TextFitTests.cpp) passed in
the stage-C build.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import run  # noqa: E402

hdr = Path(sys.argv[1]).read_text()
if "--control" in sys.argv:
    assert hdr.count("while (text.size() > 4 && ") == 1
    hdr = hdr.replace("while (text.size() > 4 && ", "while (characters(text) > 4 && ")
    hdr = hdr.replace("\ttemplate <class Measure>", "\tinline size_t characters(const std::string& s) { size_t n = 0; for (unsigned char c : s) n += (c & 0xC0) != 0x80; return n; }\n\n\ttemplate <class Measure>")
harness = hdr + r'''
#include <cstdio>
static size_t chars(const std::string& s) { size_t n = 0; for (unsigned char c : s) n += (c & 0xC0) != 0x80; return n; }
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    auto m = [](const std::string& s) { return (float)chars(s); };
    struct { const char* what; const char* text; } cs[] = {{"ASCII, 8", "ABCDEFGH"}, {"Japanese, 6", "\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e\xe6\x96\x87\xe5\xad\x97\xe5\x88\x97"},
        {"ASCII, 2", "AB"}, {"Japanese, 2", "\xe6\x97\xa5\xe6\x9c\xac"}};
    size_t kept[4];
    for (int i = 0; i < 4; i++) {
        std::string r = TextFit::fitOneLine(cs[i].text, 1.0f, m);
        kept[i] = chars(r) - (r.size() >= 3 && r.compare(r.size() - 3, 3, "...") == 0 ? 3 : 0);
        printf("%-12s width 1 -> %zu character(s) kept, then \"...\"\n", cs[i].what, kept[i]);
    }
    int bad = (kept[0] != kept[1]) + (kept[2] != kept[3]);
    if (bad) { printf("FAIL 3.35: the floor keeps a different number of characters by script (it counts bytes, :34; L-20)\n"); return 1; }
    return 0;
}
'''
run(harness, "l335", ("-fsanitize=address,undefined",))
