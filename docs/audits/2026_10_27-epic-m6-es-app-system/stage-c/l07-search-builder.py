"""L-07 (#680): ScraperAsyncRequestsBuilder's thread outlives the builder.

    python3 -I l07-search-builder.py <components/ScraperSearchComponent.cpp> [--control] [case ...]

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

Cases (S5, #1273): `drop` is the above. `engine` deletes the ScraperSearch
that owns the builder while its search runs, as ~ScraperSearchComponent
(:96-100) and search() (:276-277) delete the engines: its params (declared
after searchHandle, ScraperSearchComponent.h) go first, then the builder;
asserted: the search reads nothing freed (the name held on the heap so ASan
sees the read; the product's empty name is undefined to read the same way,
out of ASan's sight). `l08` is L-08's shape: a search
that finished with no results takes the second search at :656-658, and the
extract (the `if (status == ASYNC_DONE && results.size() == 0 && ...)`
block, as written) records the thread search() ran on; asserted: not the
calling thread, the interface's (at the pin it is). After S5 --control is
guarded CANNOT.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import block, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
cases = [a for a in sys.argv[2:] if not a.startswith("--")] or ["drop", "engine", "l08"]
body = block(src, r"^class ScraperAsyncRequestsBuilder : public ScraperSearchHandle\n", "L-07")
second = block(src, r"if \(status == ASYNC_DONE && results\.size\(\) == 0 && engine->params\.nameOverride\.empty\(\)\)", "L-08")
if "--control" in sys.argv and "std::thread*\tmThread;" not in body:
    print("CANNOT: --control rewrites the pin's lines, which this file no longer has (S5: the default run is the positive)")
    sys.exit(2)
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
#include <vector>
enum AsyncHandleStatus { ASYNC_IN_PROGRESS, ASYNC_ERROR, ASYNC_DONE };
struct ScraperSearchHandle { AsyncHandleStatus st = ASYNC_IN_PROGRESS; std::string err; virtual ~ScraperSearchHandle() {}
    virtual void update() {} void setError(const std::string& e) { st = ASYNC_ERROR; err = e; } void setStatus(AsyncHandleStatus s) { st = s; } };
struct FileData { std::string getName() { return "Game"; } };
struct ScraperSearchParams { FileData* game = nullptr; std::string nameOverride; };
// Members in ScraperSearchComponent.h's order: params is destroyed before searchHandle.
struct ScraperSearch { std::string name; std::unique_ptr<ScraperSearchHandle> searchHandle; ScraperSearchParams params; };
static std::thread::id gSearchThread;
struct Scraper {
    static Scraper* getScraper(const std::string&) { static Scraper s; return &s; }
    std::unique_ptr<ScraperSearchHandle> search(const ScraperSearchParams& params) {
        gSearchThread = std::this_thread::get_id();
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        volatile char c = params.nameOverride.c_str()[0]; (void) c;   // search() reads its params to the end
        return std::unique_ptr<ScraperSearchHandle>(new ScraperSearchHandle()); } };
class ScraperAsyncRequestsBuilder : public ScraperSearchHandle
''' + body + r''';
static void secondSearch(ScraperSearch* engine, AsyncHandleStatus status, const std::vector<int>& results)
{
    if (status == ASYNC_DONE && results.size() == 0 && engine->params.nameOverride.empty())
''' + second + r'''
}
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0);
    int bad = 0;
    for (int a = 1; a < argc; a++) {
        std::string c = argv[a];
        if (c == "drop") {
            Scraper s; ScraperSearch ss;
            {
                std::unique_ptr<ScraperSearchHandle> handle(new ScraperAsyncRequestsBuilder(&s, &ss));
                printf("drop: a search started on the builder's thread; the page stops it at once (searchHandle.reset(), :358-361)\n");
            }
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
            printf("drop: the search's 200 ms are over: nothing wrote into the freed builder\n");
        } else if (c == "engine") {
            Scraper s; FileData g;
            ScraperSearch* ss = new ScraperSearch();
            ss->params.game = &g;
            // Held on the heap, so a read of the destroyed params is one ASan sees; the
            // product's builder is made with an empty name, which a destroyed string
            // keeps inside the object, out of ASan's sight (undefined all the same).
            ss->params.nameOverride = std::string(64, 'x');
            ss->searchHandle.reset(new ScraperAsyncRequestsBuilder(&s, ss));
            delete ss;   // ~ScraperSearchComponent (:96-100): params first, then the builder
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
            printf("engine: the engine deleted while its search ran; the search read nothing freed\n");
        } else if (c == "l08") {
            FileData g; ScraperSearch eng; eng.name = "t33"; eng.params.game = &g;
            eng.searchHandle.reset(new ScraperSearchHandle());   // a search that ended with no results (not the builder)
            const std::thread::id caller = std::this_thread::get_id();
            secondSearch(&eng, ASYNC_DONE, std::vector<int>());
            eng.searchHandle.reset();
            const bool here = gSearchThread == caller;
            printf("l08: the second search (:656-658) ran on %s\n", here ? "the calling thread, the interface's" : "another thread");
            if (here) { printf("FAIL L-08: the search with no results is searched again on the interface thread\n"); bad++; }
        }
    }
    return bad ? 1 : 0;
}
'''
run(harness, "l07", ("-fsanitize=address,undefined",), args=tuple(cases))
