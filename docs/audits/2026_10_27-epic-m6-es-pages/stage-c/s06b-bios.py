"""S6b (#678, #1244): what is left of PL-09 on T21's BIOS page.

    python3 -I s06b-bios.py <es tree> <GuiBios.cpp>

Run against a scratch tree: this lane's tip with T21's StatusText.{h,cpp} and
ApiSystem.h at a73ed9efc read by `git show`, and GuiBios.{cpp,h} as the
integration will have them (the pin, S6a and a73ed9efc merged three ways,
stage-e/s6b-merge.txt). Two pieces of GuiBios.cpp, taken as written:
  zero-rows  the summary block (s06a's anchors) for a system whose header
             came with no files: NO FILES LISTED, not ALL PRESENT (0).
  not-run    the sentence row's text, the expression handed to its
             TextComponent, with T21's not-run sentence: it carries the next
             step, REFRESH TO TRY AGAIN. (the bar names REFRESH).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import run  # noqa: E402

ES = Path(sys.argv[1])
src = Path(sys.argv[2]).read_text()


def between(start, end, at=0):
    a = src.index(start, at) + len(start)
    return src[a:src.index(end, a)]


summary = between("row.addElement(spacer, false);\n", "\t\tauto line = std::make_shared<MultiLineMenuEntry>")
line = src[src.index("RETURNED NOTHING") - 300:]
text = between("auto text = std::make_shared<TextComponent>(mWindow, ", ", theme->Text.font", src.index("RETURNED NOTHING") - 300)

harness = r'''
#include <iostream>
#include <string>
static const char* ngettext(const char* one, const char* many, unsigned long n) { return n == 1 ? one : many; }
#define _(x) std::string(x)
#include "BiosText.h"
struct Entry { int missing = 0, untested = 0, present = 0; };
static std::string summaryOf(int missing, int untested, int present)
{
    Entry e; e.missing = missing; e.untested = untested; e.present = present;
''' + summary + r'''
    return summary;
}
static std::string sentenceRow(const std::string& notRun) { return ''' + text + r'''; }
static int failed = 0;
static void check(bool ok, const std::string& what) { std::cout << (ok ? "ok   " : "FAIL ") << what << std::endl; if (!ok) failed++; }
int main()
{
    const std::string zero = summaryOf(0, 0, 0);
    check(zero == "NO FILES LISTED", "zero-rows: a header with no files reads [" + zero + "]");
    const std::string row = sentenceRow("COULDN'T CHECK THE BIOS FILES RIGHT NOW.");
    check(row.find("REFRESH TO TRY AGAIN.") != std::string::npos, "not-run: the row reads [" + row + "]");
    const std::string nothing = sentenceRow("");
    check(nothing == "THE BIOS CHECK RETURNED NOTHING", "control: a check that ran and listed nothing reads [" + nothing + "]");
    if (failed) { std::cout << "FAIL s06b: " << failed << " of 3 checks" << std::endl; return 1; }
    std::cout << "s06b: PASS, 3 checks" << std::endl;
    return 0;
}
'''
run(harness, "s06b", flags=("-fsanitize=address,undefined", "-I", str(ES / "es-app/src")))
