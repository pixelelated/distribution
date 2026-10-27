"""3.13, L-07, EP-1, EP-5 (#679; #1259, PL-02): a scraper request or a media
download that reached nothing ends as done.

    python3 -I l313-request-outcome.py <Scraper.cpp> <es-core AsyncHandle.h dir> [--control]

ScraperHttpRequest's constructor and ::update, and ImageDownloadHandle's
constructor and ::update, are extracted as written, with the pin's
OVERQUOTA_RETRY_DELAY / _COUNT, over es-core's AsyncHandle.h as written and a
doubled HttpReq. Each request the code constructs takes the next status of
the case's sequence; a clock the case moves stands in for SDL_GetTicks.
ThreadedScraper.cpp:155-173 at the pin is the reader: an ASYNC_ERROR whose
code is not on its fatal list is counted and the run goes on.

The search request:
- an IO error, a 429 whose retries are spent, and a Retry-After of 60 s with
  retryOn249() false must end ASYNC_ERROR with their codes. At the pin they
  end ASYNC_DONE (a631e8c84's "Ignored errors") -- FAIL;
- a 404 ends ASYNC_DONE (no match) and a 403 ASYNC_ERROR: right at the pin;
- a dependency request's 404 (TheGamesDB's images) must still process the
  primary response (EP-1). At the pin the primary is never processed -- FAIL;
- a process() that returns false once, then true, must be retried once
  (ScreenScraper's per-minute limit). At the pin the false is dropped (`:337`)
  and the game reads as no match -- FAIL.
The media download (L-07, EP-5):
- a 404, an IO error, a 429 whose retries are spent, a rename that fails and a
  resize that fails must each end ASYNC_ERROR. At the pin each is ASYNC_DONE
  -- FAIL.
--control rewrites the pin's three search branches (stage C's control); it is
CANNOT against a file without them.
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
ictor = function(src, r"^ImageDownloadHandle::ImageDownloadHandle\(const std::string& url, const std::string& path, int maxWidth, int maxHeight\)", "L-07")
iupd = function(src, r"^void ImageDownloadHandle::update\(\)", "L-07")
if "--control" in sys.argv:
    pairs = [
        ("\t\tif (mRetryCount >= mOverQuotaRetryCount)\n\t\t{\n\t\t\tsetStatus(ASYNC_DONE); // Ignore error",
         "\t\tif (mRetryCount >= mOverQuotaRetryCount)\n\t\t{\n\t\t\tsetError(status, \"TOO MANY REQUESTS\");"),
        ("\t\t\t\tsetStatus(ASYNC_DONE); // Ignore error if delay > 5 seconds",
         "\t\t\t\tsetError(status, \"TOO MANY REQUESTS\");"),
        ("if (status == HttpReq::REQ_404_NOTFOUND || status == HttpReq::REQ_IO_ERROR)",
         "if (status == HttpReq::REQ_404_NOTFOUND)")]
    if any(a not in upd for a, _ in pairs):
        print("CANNOT l313 --control: the pin's branches are not in this file (the control is the pin's)")
        sys.exit(2)
    for a, b in pairs:
        upd = upd.replace(a, b)
harness = r'''
#include <cstdio>
#include <functional>
#include <map>
#include <queue>
#include <string>
#include <vector>
#include "AsyncHandle.h"
struct NullLog { template<typename T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()
static int gTicks = 0;
static int SDL_GetTicks() { return gTicks; }
namespace Utils {
  namespace String {
    std::string removeHtmlTags(const std::string& s) { return s; }
    int toInteger(const std::string& s) { return atoi(s.c_str()); }
    std::string toLower(std::string s) { for (auto& c : s) c = (char) tolower((unsigned char) c); return s; }
    bool startsWith(const std::string& s, const std::string& p) { return s.compare(0, p.size(), p) == 0; }
    std::vector<std::string> split(const std::string& s, char d, bool) { std::vector<std::string> v; std::string c; for (char x : s) { if (x == d) { v.push_back(c); c.clear(); } else c += x; } v.push_back(c); return v; } }
  namespace FileSystem {
    std::string getExtension(const std::string& p) { auto i = p.rfind('.'); return i == std::string::npos ? "" : p.substr(i); }
    std::string changeExtension(const std::string& p, const std::string& e) { auto i = p.rfind('.'); return (i == std::string::npos ? p : p.substr(0, i)) + e; }
    static bool gRenameOk = true;
    bool renameFile(const std::string&, const std::string&) { return gRenameOk; } }
  struct Uri { struct Args { void set(const std::string&, const std::string&) {} } arguments; std::string u; Uri(const std::string& s) : u(s) {} std::string toString() { return u; } };
}
static bool gResizeOk = true;
bool resizeImage(const std::string&, int, int) { return gResizeOk; }
struct HttpReqOptions { std::string outputFilename; std::vector<std::string> customHeaders; std::string dataToPost; long connectTimeout = 10000, timeout = 0, stallTimeout = 0;
    HttpReqOptions() {} HttpReqOptions(const std::string& f) : outputFilename(f) {} };
#ifndef SCRAPER_STALL_TIMEOUT
#define SCRAPER_STALL_TIMEOUT 30L
#endif
static std::vector<int> gSeq; static size_t gNext = 0; static std::string gRetryAfter, gContentType; static int gCreated = 0;
struct HttpReq {
    enum Status { REQ_IN_PROGRESS = 0, REQ_IO_ERROR = 3, REQ_FILESTREAM_ERROR = 4, REQ_SUCCESS = 200, REQ_403_BADLOGIN = 403,
        REQ_404_NOTFOUND = 404, REQ_429_TOOMANYREQUESTS = 429 };
    std::string url; int st;
    HttpReq(const std::string& u, HttpReqOptions*) : url(u) { st = gNext < gSeq.size() ? gSeq[gNext++] : 200; gCreated++; }
    HttpReq(const std::string& u, const std::string&) : HttpReq(u, (HttpReqOptions*) nullptr) {}
    Status status() { return (Status) st; }
    std::string getContent() { return "{}"; } std::string getUrl() { return url; }
    std::string getErrorMsg() { return "curl's words"; } int getPercent() { return 0; }
    std::string getResponseHeader(const std::string& h) { return h == "Content-Type" ? gContentType : gRetryAfter; }
};
struct ScraperSearchResult {};
''' + defs + r'''
struct ScraperRequest : public AsyncHandle {
    ScraperRequest(std::vector<ScraperSearchResult>& r) : mResults(r) {}
    std::vector<ScraperSearchResult>& mResults; };
static int gProcessed = 0, gFalseFirst = 0; static std::string gProcessedBody;
struct ScraperHttpRequest : public ScraperRequest {
    ScraperHttpRequest(std::vector<ScraperSearchResult>& resultsWrite, const std::string& url, HttpReqOptions* options);
    ~ScraperHttpRequest() { delete mRequest; }
    void update() override;
    bool on249 = true, dependency = false;
    virtual bool retryOn249() { return on249; }
    bool process(const std::string& body, std::vector<ScraperSearchResult>&) {
        gProcessed++; gProcessedBody = body; if (gFalseFirst > 0) { gFalseFirst--; return false; } return true; }
    void preProcess(const std::string&) { if (dependency) mDependencyQueue.push({"1", "http://scraper/images"}); }
    HttpReq* mRequest; HttpReqOptions mOptions; std::string mUrl, mRetryUrl; bool mProcessRetried = false;
    int mRetryCount, mOverQuotaPendingTime, mOverQuotaRetryDelay, mOverQuotaRetryCount;
    std::map<std::string, std::string> mResponses; std::string mDependencyId; std::queue<std::pair<std::string, std::string>> mDependencyQueue;
    AsyncHandleStatus st() { return mStatus; } int code() { return mErrorCode; }
};
struct ImageDownloadHandle : public AsyncHandle {
    ImageDownloadHandle(const std::string& url, const std::string& path, int maxWidth, int maxHeight);
    ~ImageDownloadHandle() { delete mRequest; }
    void update() override;
    HttpReq* mRequest; int mRetryCount, mOverQuotaPendingTime, mOverQuotaRetryDelay, mOverQuotaRetryCount;
    std::string mSavePath; int mMaxWidth, mMaxHeight; HttpReqOptions mOptions; std::string mRequestUrl;
    AsyncHandleStatus st() { return mStatus; } int code() { return mErrorCode; }
};
''' + ctor + "\n" + upd + "\n" + ictor + "\n" + iupd + r'''
static const char* name(AsyncHandleStatus s) { return s == ASYNC_DONE ? "ASYNC_DONE" : s == ASYNC_ERROR ? "ASYNC_ERROR" : "ASYNC_IN_PROGRESS"; }
static std::vector<ScraperSearchResult> gRes;
template<class H> static void drive(H* r) { for (int i = 0; i < 300 && r->st() == ASYNC_IN_PROGRESS; i++) { r->update(); gTicks += 100000; } }
static void seq(std::vector<int> s) { gSeq = s; gNext = 0; gCreated = 0; gTicks = 1; gProcessed = 0; gProcessedBody.clear(); }
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    int bad = 0;
    struct C { const char* what; std::vector<int> s; const char* ra; bool on249; bool wantError; } cases[] = {
        {"IO error (no network)", {3}, "", true, true},
        {"429, retries spent", {429, 429, 429, 429, 429, 429, 429}, "", true, true},
        {"429, Retry-After 60, retryOn249 false", {429}, "60", false, true},
        {"404 (no match)", {404}, "", true, false},
        {"403 (bad login)", {403}, "", true, true},
    };
    for (auto& c : cases) {
        seq(c.s); gRetryAfter = c.ra; gFalseFirst = 0;
        auto r = new ScraperHttpRequest(gRes, "http://scraper/", nullptr); r->on249 = c.on249; drive(r);
        bool isErr = r->st() == ASYNC_ERROR;
        printf("search %-38s -> %-11s code %3d after %d request(s)%s\n", c.what, name(r->st()), r->code(), gCreated, isErr == c.wantError ? "" : (c.wantError ? "   (want an error the page counts)" : "   (want done)"));
        if (isErr != c.wantError) bad++;
        delete r;
    }
    { seq({200, 404}); gRetryAfter = ""; gFalseFirst = 0;
      auto r = new ScraperHttpRequest(gRes, "http://scraper/", nullptr); r->dependency = true; drive(r);
      bool ok = gProcessed == 1 && r->st() == ASYNC_DONE;
      printf("search %-38s -> %-11s processed %d time(s)%s\n", "a dependency's 404 (EP-1)", name(r->st()), gProcessed, ok ? "" : "   (want the primary processed, done)");
      if (!ok) bad++; delete r; }
    { seq({200, 200}); gRetryAfter = ""; gFalseFirst = 1;
      auto r = new ScraperHttpRequest(gRes, "http://scraper/", nullptr); drive(r);
      bool ok = gCreated == 2 && gProcessed == 2 && r->st() == ASYNC_DONE;
      printf("search %-38s -> %-11s %d request(s), processed %d time(s)%s\n", "process() false once, then true", name(r->st()), gCreated, gProcessed, ok ? "" : "   (want one retry)");
      if (!ok) bad++; delete r; }
    struct M { const char* what; std::vector<int> s; bool rename, resize; const char* ct; } media[] = {
        {"404", {404}, true, true, ""},
        {"IO error", {3}, true, true, ""},
        {"429, retries spent", {429, 429, 429, 429, 429, 429, 429}, true, true, ""},
        {"a rename that fails", {200}, false, true, "image/png"},
        {"a resize that fails", {200}, true, false, "image/jpeg"},
    };
    for (auto& m : media) {
        seq(m.s); gRetryAfter = ""; Utils::FileSystem::gRenameOk = m.rename; gResizeOk = m.resize; gContentType = m.ct;
        auto h = new ImageDownloadHandle("http://media/x.jpg", "/roms/gb/images/x-image.jpg", 0, 0); drive(h);
        bool isErr = h->st() == ASYNC_ERROR;
        printf("media  %-38s -> %-11s code %3d%s\n", m.what, name(h->st()), h->code(), isErr ? "" : "   (want an error the run counts)");
        if (!isErr) bad++; delete h;
    }
    if (bad) { printf("FAIL 3.13/L-07: %d outcome(s) with no usable answer read as done, or a usable one discarded\n", bad); return 1; }
    return 0;
}
'''
run(harness, "l313", ("-fsanitize=address,undefined", "-I" + inc))
