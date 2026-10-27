"""L-07 (#680): ScraperAsyncRequestsBuilder's thread outlives the builder.

    python3 -I l07-search-builder.py <components/ScraperSearchComponent.cpp> [--control]

The class (the pin's :196-258) extracted as written, over a
ScraperSearchHandle base with a virtual destructor (the AsyncHandle shape)
and a Scraper double whose search() takes 200 ms, as a token request or a
ROM hash can (the class's own comment, :194-195). The builder is created
and then dropped while its search runs, as ScraperSearchComponent::stop()
(:358-361, `engine->searchHandle.reset()`) and the destructor (:96-100)
drop it. Asserted: nothing writes into the freed builder. At the pin, under
ASan: a heap-use-after-free in loadSearchHandleAsync (:213-220), because
the class has no destructor and its `std::thread*` is never joined or
deleted (:206, and `mThread = nullptr` at :231 leaks the object). --control
gives the builder a destructor that joins and deletes its thread, deletes
the thread after the join in update(), and makes mFinished atomic: the
lane's proposed fix, which must PASS.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import block, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
body = block(src, r"^class ScraperAsyncRequestsBuilder : public ScraperSearchHandle\n", "L-07")
if "--control" in sys.argv:
    body = body.replace("\tvoid loadSearchHandleAsync()", "\t~ScraperAsyncRequestsBuilder() { if (mThread) { mThread->join(); delete mThread; } }\n\n\tvoid loadSearchHandleAsync()", 1)
    assert body.count("\t\t\tmThread = nullptr;") == 1
    body = body.replace("\t\t\tmThread = nullptr;", "\t\t\tdelete mThread;\n\t\t\tmThread = nullptr;")
    assert body.count("\tbool\t\t\tmFinished;") == 1
    body = body.replace("\tbool\t\t\tmFinished;", "\tstd::atomic<bool> mFinished;")
harness = r'''
#include <atomic>
#include <chrono>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <string>
#include <thread>
enum AsyncHandleStatus { ASYNC_IN_PROGRESS, ASYNC_ERROR, ASYNC_DONE };
struct ScraperSearchHandle { AsyncHandleStatus st = ASYNC_IN_PROGRESS; std::string err; virtual ~ScraperSearchHandle() {}
    virtual void update() {} void setError(const std::string& e) { st = ASYNC_ERROR; err = e; } void setStatus(AsyncHandleStatus s) { st = s; } };
struct ScraperSearchParams {};
struct ScraperSearch { ScraperSearchParams params; };
struct Scraper { std::unique_ptr<ScraperSearchHandle> search(const ScraperSearchParams&) {
    std::this_thread::sleep_for(std::chrono::milliseconds(200)); return std::unique_ptr<ScraperSearchHandle>(new ScraperSearchHandle()); } };
class ScraperAsyncRequestsBuilder : public ScraperSearchHandle
''' + body + r''';
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    Scraper s; ScraperSearch ss;
    {
        std::unique_ptr<ScraperSearchHandle> handle(new ScraperAsyncRequestsBuilder(&s, &ss));
        printf("a search started on the builder's thread; the page stops it at once (searchHandle.reset(), :358-361)\n");
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    printf("the search's 200 ms are over: nothing wrote into the freed builder\n");
    return 0;
}
'''
run(harness, "l07", ("-fsanitize=address,undefined",))
