"""3.13 (#679): a scraper request that never reached its server ends as done.

    python3 -I l313-request-outcome.py <Scraper.cpp> <es-core AsyncHandle.h dir> [--control]

ScraperHttpRequest's constructor and ::update are extracted as written, with the
pin's OVERQUOTA_RETRY_DELAY / _COUNT, over es-core's AsyncHandle.h as written
and a doubled HttpReq whose status the case sets (and a clock the case moves).
ThreadedScraper.cpp:157-173 at the pin is the reader: an ASYNC_ERROR whose code
is not in its fatal list is counted in the page's errors and the run goes on;
ASYNC_DONE with no result is a game with no match.
- REQ_IO_ERROR (no network, a refused or reset connection, a timeout) must end
  as ASYNC_ERROR with its code, so the page can count it. At the pin it ends
  ASYNC_DONE -- the "Ignored errors" branch (:372-376, a631e8c84, upstream,
  2020, "Secure requests") -- FAIL. G-05 is this on the image: offline, the
  page said COMPLETED, GAMES SCRAPED: 9 with nothing written.
- A 429 whose retries are spent must end as an error the page can count. At
  the pin it is ASYNC_DONE, "Ignore error" (:350-352) -- FAIL. The same for a
  Retry-After over 5 s on a scraper whose retryOn249() is false (:357-361).
- REQ_404_NOTFOUND ends ASYNC_DONE (no match) and a 403 ends ASYNC_ERROR with
  its code: both already right, run as the cases that must keep passing.
- A body whose process() returns false: printed only. :336's comment says an
  error in process() changes the status; only setError does, and :337 drops
  the return. 3.16 is that case for IGDB.
The 2020 intent -- a batch must not stop on one game's failure -- is kept by
the reader, which stops only on its fatal list; the fix shape below keeps it.
--control makes the IO error and the spent 429s call setError with their codes.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
inc = sys.argv[2]
defs = "\n".join(re.findall(r"^#define OVERQUOTA_RETRY_\w+ \d+$", src, re.M))
assert defs.count("#define") == 2, defs
ctor = function(src, r"^ScraperHttpRequest::ScraperHttpRequest\(std::vector<ScraperSearchResult>& resultsWrite, const std::string& url, HttpReqOptions\* options\)", "3.13")
upd = function(src, r"^void ScraperHttpRequest::update\(\)", "3.13")
if "--control" in sys.argv:
    for a, b in [
        ("\t\tif (mRetryCount >= mOverQuotaRetryCount)\n\t\t{\n\t\t\tsetStatus(ASYNC_DONE); // Ignore error",
         "\t\tif (mRetryCount >= mOverQuotaRetryCount)\n\t\t{\n\t\t\tsetError(status, \"TOO MANY REQUESTS\");"),
        ("\t\t\t\tsetStatus(ASYNC_DONE); // Ignore error if delay > 5 seconds",
         "\t\t\t\tsetError(status, \"TOO MANY REQUESTS\");"),
        ("if (status == HttpReq::REQ_404_NOTFOUND || status == HttpReq::REQ_IO_ERROR)",
         "if (status == HttpReq::REQ_404_NOTFOUND)")]:
        assert a in upd, a
        upd = upd.replace(a, b)
harness = r'''
#include <cstdio>
#include <map>
#include <queue>
#include <string>
#include <vector>
#include "AsyncHandle.h"
struct NullLog { template<typename T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()
static int gTicks = 0;
static int SDL_GetTicks() { return gTicks; }
namespace Utils { namespace String {
    std::string removeHtmlTags(const std::string& s) { return s; }
    int toInteger(const std::string& s) { return atoi(s.c_str()); } } }
struct HttpReqOptions {};
static int gNextStatus = 0; static std::string gRetryAfter; static int gCreated = 0;
struct HttpReq {
    enum Status { REQ_IN_PROGRESS = 0, REQ_IO_ERROR = 3, REQ_FILESTREAM_ERROR = 4, REQ_SUCCESS = 200, REQ_403_BADLOGIN = 403,
        REQ_404_NOTFOUND = 404, REQ_429_TOOMANYREQUESTS = 429 };
    std::string url; HttpReq(const std::string& u, HttpReqOptions*) : url(u) { gCreated++; }
    Status status() { return (Status)gNextStatus; }
    std::string getContent() { return "{}"; } std::string getUrl() { return url; }
    std::string getErrorMsg() { return "curl's words"; }
    std::string getResponseHeader(const std::string&) { return gRetryAfter; }
};
struct ScraperSearchResult {};
''' + defs + r'''
struct ScraperRequest : public AsyncHandle {
    ScraperRequest(std::vector<ScraperSearchResult>& r) : mResults(r) {}
    std::vector<ScraperSearchResult>& mResults; };
struct ScraperHttpRequest : public ScraperRequest {
    ScraperHttpRequest(std::vector<ScraperSearchResult>& resultsWrite, const std::string& url, HttpReqOptions* options);
    ~ScraperHttpRequest() { delete mRequest; }
    void update() override;
    bool processReturns = true, on249 = true;
    virtual bool retryOn249() { return on249; }
    bool process(const std::string&, std::vector<ScraperSearchResult>&) { return processReturns; }
    void preProcess(const std::string&) {}
    HttpReq* mRequest; HttpReqOptions mOptions; std::string mUrl; int mRetryCount, mOverQuotaPendingTime, mOverQuotaRetryDelay, mOverQuotaRetryCount;
    std::map<std::string, std::string> mResponses; std::string mDependencyId; std::queue<std::pair<std::string, std::string>> mDependencyQueue;
    AsyncHandleStatus st() { return mStatus; } int code() { return mErrorCode; }
};
''' + ctor + "\n" + upd + r'''
static const char* name(AsyncHandleStatus s) { return s == ASYNC_DONE ? "ASYNC_DONE" : s == ASYNC_ERROR ? "ASYNC_ERROR" : "ASYNC_IN_PROGRESS"; }
// Drive one request until it leaves IN_PROGRESS, moving the clock past each retry delay.
static std::vector<ScraperSearchResult> gRes;
static ScraperHttpRequest* drive(int status, const std::string& retryAfter, bool on249, bool processReturns, int& requests) {
    std::vector<ScraperSearchResult>* res = &gRes;
    gNextStatus = status; gRetryAfter = retryAfter; gCreated = 0; gTicks = 1;
    auto r = new ScraperHttpRequest(*res, "http://scraper/", nullptr);
    r->on249 = on249; r->processReturns = processReturns;
    for (int i = 0; i < 200 && r->st() == ASYNC_IN_PROGRESS; i++) { r->update(); gTicks += 100000; }
    requests = gCreated; return r;
}
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    int bad = 0;
    struct C { const char* what; int status; const char* ra; bool on249; bool proc; bool wantError; } cases[] = {
        {"IO error (no network)", 3, "", true, true, true},
        {"429, retries spent", 429, "", true, true, true},
        {"429, Retry-After 60, retryOn249 false", 429, "60", false, true, true},
        {"404 (no match)", 404, "", true, true, false},
        {"403 (bad login)", 403, "", true, true, true},
    };
    for (auto& c : cases) {
        int n; auto r = drive(c.status, c.ra, c.on249, c.proc, n);
        bool isErr = r->st() == ASYNC_ERROR;
        printf("%-40s -> %-11s code %3d after %d request(s)%s\n", c.what, name(r->st()), r->code(), n, isErr == c.wantError ? "" : (c.wantError ? "   (want an error the page counts)" : "   (want done)"));
        if (isErr != c.wantError) bad++;
        delete r;
    }
    int n; auto r = drive(200, "", true, false, n);
    printf("%-40s -> %-11s (printed only; 3.16)\n", "a body whose process() returns false", name(r->st()));
    delete r;
    if (bad) { printf("FAIL 3.13: %d outcome(s) with no usable answer read as done\n", bad); return 1; }
    return 0;
}
'''
run(harness, "l313", ("-fsanitize=address,undefined", "-I" + inc))
