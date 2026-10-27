"""02 § The bounds: every HttpReq construction in T32's slice (#679, Q2, L-06).

    python3 -I t32-bounds.py <es worktree> <commit> <paths.txt> [constructions=9,new=7,stack=2,bounded=0]

The sites are `new HttpReq(` and an HttpReq constructed on the stack
(`HttpReq name(...)`), read by t32lib (comments and strings skipped). The
brief's count is the first kind, 7; the two token requests are the second
(HfsDBScraper.cpp:195, IGDBScraper.cpp:150), each ended by `request.wait()`,
HttpReq.cpp:638-644's 20 ms sleep loop with no bound of its own.
The bounds come from es-core/src/HttpReq.h:45-90 and HttpReq.cpp:204-213 at
the pin (T21's files, read): HttpReqOptions' constructors set
connectTimeout 10000 ms, timeout 0 (none) and stallTimeout 0 (none); with
no options, HttpReq.cpp:204 still sets the 10 s connect and nothing else.
So a request's total and stall bounds are whatever its options say, and
SITES records what each site's options carry, read at its lines. A row is
"bounded" when its options set timeout or stallTimeout.

Exits 1 when a site has no entry, an entry has no site, a site's options
set a bound the entry does not record, or a count differs.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t32lib import call_args, in_comment_or_string, show  # noqa: E402

SITES = {
    ("GamesDBJSONScraperResources.cpp", 153): ("TheGamesDBJSONRequestResources::fetchResource", "none (`new HttpReq(path)`)", "the platform, genre and developer lists from api.thegamesdb.net (under GAMESDB_APIKEY)"),
    ("Scraper.cpp", 267): ("ScraperHttpRequest's constructor", "the scraper's own, copied into `mOptions` (`:265-266`): headers and the POST body only -- HfsDB `:179`, `:287`; IGDB `:146`, `:189`, `:205`, `:215`; none for ArcadeDB and TheGamesDB", "every search request of the four upstream scrapers"),
    ("Scraper.cpp", 302): ("ScraperHttpRequest::update, the 429 retry", "`mOptions`, as `:267`", "the same request again after `Retry-After`"),
    ("Scraper.cpp", 332): ("ScraperHttpRequest::update, the dependency queue", "`mOptions`, as `:267`", "TheGamesDB's dependent requests (`preProcess`)"),
    ("Scraper.cpp", 564): ("ImageDownloadHandle's constructor (ScreenScraper media, resized)", "`options` (`:539`): `outputFilename`, the ScreenScraper `Referer` header (`:541-546`)", "a media download from ScreenScraper with maxwidth/maxheight"),
    ("Scraper.cpp", 567): ("ImageDownloadHandle's constructor (every other media)", "`options` (`:539`): `outputFilename`, and the `Referer` for a ScreenScraper media path", "every scraper's media download"),
    ("HfsDBScraper.cpp", 195): ("HfsDBScraper::ensureToken, on the stack, then `request.wait()` (`:196`)", "`options` (`:179`): the Basic authorization header only", "the token, from `generateRequests` (`:214`) -- the batch scrape's thread, or `ScraperSearchComponent::search` (`components/ScraperSearchComponent.cpp:261`, outside the 42) for one game"),
    ("IGDBScraper.cpp", 150): ("IGDBScraper::ensureToken, on the stack, then `request.wait()` (`:151`)", "`options` (`:146`): the Content-Type header and the POST body only", "the token, from `generateRequests` (`:169`), as HfsDB's; not made without a client id (`:143-144`)"),
    ("Scraper.cpp", 596): ("ImageDownloadHandle::update, the 429 retry", "none: `new HttpReq(url, mSavePath)`, the two-string constructor -- the first request's `Referer` header is not carried", "the media download again after `Retry-After`"),
}

tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
found, bounds_set, kinds = [], [], {}
for path in [l.strip() for l in open(paths_file) if l.strip()]:
    src = show(tree, commit, path)
    f = path.rsplit("/", 1)[1]
    for kind, pat in (("new", r"\bnew\s+HttpReq\s*\("), ("stack", r"\bHttpReq\s+[A-Za-z_]\w*\s*\(")):
        for m in re.finditer(pat, src):
            if not in_comment_or_string(src, m.start()):
                site = (f, src.count("\n", 0, m.start()) + 1)
                found.append(site)
                kinds[site] = kind
    for m in re.finditer(r"\.(timeout|stallTimeout)\s*=", src):
        if not in_comment_or_string(src, m.start()):
            bounds_set.append((f, src.count("\n", 0, m.start()) + 1, m.group(1)))
fail = ["%s:%d has no entry" % s for s in found if s not in SITES]
fail += ["an entry names %s:%d, where there is no HttpReq construction" % s for s in SITES if s not in found]
fail += ["%s:%d sets %s, which no entry records" % b for b in bounds_set]
print("| Site | Function | Options | Connect | Total | Stall | Requests |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for s in sorted(found):
    fn, opts, what = SITES.get(s, ("?", "?", "?"))
    print("| `%s:%d` | %s | %s | 10 s | none | none | %s |" % (s[0], s[1], fn, opts, what))
counts = {"constructions": len(found), "new": sum(1 for k in kinds.values() if k == "new"), "stack": sum(1 for k in kinds.values() if k == "stack"), "bounded": len(bounds_set)}
print()
print("generated, asserted: %d constructions in %d files (%d `new HttpReq(`, %d on the stack); %d set a total or stall bound" % (counts["constructions"], len(set(f for f, _ in found)), counts["new"], counts["stack"], counts["bounded"]))
fail += ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t32-bounds: " + "; ".join(fail))
    sys.exit(1)
