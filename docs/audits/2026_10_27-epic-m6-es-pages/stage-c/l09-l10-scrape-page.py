"""L-09 and L-10 (#678): the scrape page's finished state, as the pin writes it.

    python3 -I l09-l10-scrape-page.py <GuiScraperRun.cpp> [--control]

GuiScraperRun::update, ::input, ::outcomeWord and ::countsLine are extracted as
written and compiled over doubles: ThreadedScraper::progress() returns a
Progress the case sets; the page's TextComponents record their text;
TextFit::fitOneLine and CloudText::chooseThatFits return the first candidate.

L-09: a run of 5 games, all errored, the scraper not failed. The finished rows
must carry an outcome word, a why (line 4) and what to do next (line 5)
(es-player-text.md § Outcome vocabulary: then a why, what is in place, and how
to recover). At the pin lines 4 and 5 are empty -- FAIL.
L-10: the run finished; an axis event past its deadzone (TYPE_AXIS, value -1)
must not dismiss the outcome; a button press must. At the pin `delete this`
follows any non-zero input -- FAIL on the axis.
--control runs constructed variants (line 4 and 5 filled for p.errors, and the
dismissal on TYPE_BUTTON only), to show both cases can pass.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
control = "--control" in sys.argv
upd = function(src, r"^void GuiScraperRun::update\(int deltaTime\)", "scrape")
inp = function(src, r"^bool GuiScraperRun::input\(InputConfig\* config, Input input\)", "scrape")
word = function(src, r"^std::string GuiScraperRun::outcomeWord\(", "scrape")
counts = function(src, r"^std::string GuiScraperRun::countsLine\(", "scrape")
if control:
    a = 'mDetail  ->setText(p.failed ? fitOneLine(mSmallFont, p.failure, mLineWidth) : "");'
    assert a in upd
    upd = upd.replace(a, 'mDetail  ->setText(p.failed ? fitOneLine(mSmallFont, p.failure, mLineWidth) : (p.errors > 0 ? std::string("NO MATCH FOR SOME GAMES") : std::string("")));')
    b = "mNote    ->setText(p.done - p.errors > 0 ? CloudText::chooseThatFits("
    assert b in upd
    upd = upd.replace(b, "mNote    ->setText(p.done > 0 ? CloudText::chooseThatFits(")
    c = "\tdelete this;\n\treturn true;\n}"
    assert c in inp
    inp = inp.replace(c, "\tif (input.type == TYPE_BUTTON)\n\t\tdelete this;\n\treturn true;\n}")
harness = r'''
#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <vector>
#define _(x) std::string(x)
enum InputType { TYPE_AXIS, TYPE_BUTTON };
struct Input { int type = TYPE_BUTTON; int value = 1; };
#define BUTTON_BACK "back"
struct InputConfig { bool isMappedTo(const std::string&, Input) { return false; } };
struct V2 { float v; float x() const { return v; } };
struct Font { float w = 1; V2 sizeText(const std::string& t) const { return V2{(float)t.size()}; } };
struct TextComponent { std::string text; void setText(const std::string& t) { text = t; } };
namespace ThreadedScraper {
    struct Progress { bool finished = false, failed = false, cancelled = false; int done = 0, total = 0, errors = 0; long elapsedMs = 0; std::string game, failure; };
    static Progress gP;
    Progress progress() { return gP; }
}
namespace CloudText { std::string chooseThatFits(const std::vector<std::string>& c, float, std::function<float(const std::string&)>) { return c.empty() ? "" : c[0]; } }
struct BusyComponent { void update(int) {} };
static bool gDeleted = false;
struct GuiScraperRun {
    BusyComponent mBusyAnim;
    std::shared_ptr<TextComponent> mTitle = std::make_shared<TextComponent>(), mStatus = std::make_shared<TextComponent>(),
        mCounter = std::make_shared<TextComponent>(), mActivity = std::make_shared<TextComponent>(), mDetail = std::make_shared<TextComponent>(),
        mNote = std::make_shared<TextComponent>(), mElapsed = std::make_shared<TextComponent>(), mFooter = std::make_shared<TextComponent>();
    std::shared_ptr<Font> mTextFont = std::make_shared<Font>(), mSmallFont = std::make_shared<Font>();
    float mLineWidth = 100; bool mShownFinished = false;
    ~GuiScraperRun() { gDeleted = true; }
    void updateHelpPrompts() {}
    void askCancel() {}
    static std::string fitOneLine(const std::shared_ptr<Font>&, std::string t, float) { return t; }
    static std::string outcomeWord(const ThreadedScraper::Progress& p);
    static std::string countsLine(const ThreadedScraper::Progress& p);
    void update(int deltaTime);
    bool input(InputConfig* config, Input input);
};
struct GuiComponentBase { static void update(int) {} };
#define GuiComponent GuiComponentBase
''' + word + "\n" + counts + "\n" + upd + "\n#undef GuiComponent\n" + inp + r'''
static int failed = 0;
static void check(bool ok, const std::string& what) { if (!ok) { std::cout << "FAIL scrape: " << what << "\n"; failed++; } }
int main()
{
    // L-09: five games, every one errored, the scraper not failed.
    ThreadedScraper::gP = ThreadedScraper::Progress(); auto& p = ThreadedScraper::gP;
    p.finished = true; p.done = 5; p.total = 5; p.errors = 5; p.elapsedMs = 61000;
    auto* page = new GuiScraperRun(); page->update(16);
    std::cout << "L-09 rows: [" << page->mStatus->text << "] [" << page->mCounter->text << "] [" << page->mDetail->text << "] [" << page->mNote->text << "] [" << page->mFooter->text << "]\n";
    check(!page->mDetail->text.empty(), "L-09: an all-errored run says no why (line 4 empty)");
    check(!page->mNote->text.empty(), "L-09: an all-errored run says nothing to do next (line 5 empty)");
    // L-10: finished; an axis event, then a button.
    InputConfig cfg; Input axis; axis.type = TYPE_AXIS; axis.value = -1;
    gDeleted = false; page->input(&cfg, axis);
    std::cout << "L-10 an axis past its deadzone: the outcome " << (gDeleted ? "dismissed" : "kept") << "\n";
    check(!gDeleted, "L-10: an axis event dismissed the finished outcome");
    if (!gDeleted) { Input button; gDeleted = false; page->input(&cfg, button);
        std::cout << "L-10 a button: the outcome " << (gDeleted ? "dismissed" : "kept") << "\n";
        check(gDeleted, "L-10: a button did not dismiss the outcome"); if (!gDeleted) delete page; }
    if (failed) return 1;
    std::cout << "3 checks\n";
    return 0;
}
'''
run(harness, "scrape")
