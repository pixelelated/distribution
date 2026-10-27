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

Revised at stage E with S2 (D-WORKFLOW-210, #1262): a site is keyed by its
file and its order in that file (lines move under a fix), and a site is
"bounded" when the options it passes set `stallTimeout` -- `&mOptions` when the
file assigns `mOptions.stallTimeout`; a local `options` when that variable's
`.stallTimeout` is assigned in the 60 lines before the construction; no
options argument, never. Its line is printed beside it. At the pin this
reads `bounded=0`, as the stage-B rule did; after S2, `bounded=9`.
Exits 1 when a site has no entry, an entry has no site, or a count differs.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t32lib import call_args, in_comment_or_string, show  # noqa: E402

SITES = {
    ("GamesDBJSONScraperResources.cpp", 1): ("TheGamesDBJSONRequestResources::fetchResource", "the platform, genre and developer lists from api.thegamesdb.net (under GAMESDB_APIKEY)"),
    ("Scraper.cpp", 1): ("ScraperHttpRequest's constructor", "every search request of the four upstream scrapers"),
    ("Scraper.cpp", 2): ("ScraperHttpRequest::update, the 429 retry", "the same request again after `Retry-After`"),
    ("Scraper.cpp", 3): ("ScraperHttpRequest::update, the dependency queue", "TheGamesDB's dependent requests (`preProcess`)"),
    ("Scraper.cpp", 4): ("ImageDownloadHandle's constructor (ScreenScraper media, resized)", "a media download from ScreenScraper with maxwidth/maxheight"),
    ("Scraper.cpp", 5): ("ImageDownloadHandle's constructor (every other media)", "every scraper's media download"),
    ("Scraper.cpp", 6): ("ImageDownloadHandle::update, the 429 retry", "the media download again after `Retry-After`"),
    ("HfsDBScraper.cpp", 1): ("HfsDBScraper::ensureToken, on the stack, then `request.wait()`", "the token, from `generateRequests`"),
    ("IGDBScraper.cpp", 1): ("IGDBScraper::ensureToken, on the stack, then `request.wait()`", "the token, from `generateRequests`; not made without a client id and a secret"),
}

tree, commit, paths_file = sys.argv[1:4]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[4].split(","))) if len(sys.argv) > 4 else {}
found, kinds, lines, opts, bounded = [], {}, {}, {}, {}
for path in [l.strip() for l in open(paths_file) if l.strip()]:
    src = show(tree, commit, path)
    f = path.rsplit("/", 1)[1]
    hits = []
    for kind, pat in (("new", r"\bnew\s+HttpReq\s*\("), ("stack", r"\bHttpReq\s+[A-Za-z_]\w*\s*\(")):
        for m in re.finditer(pat, src):
            if not in_comment_or_string(src, m.start()):
                hits.append((m.start(), m.end() - 1, kind))
    member_bound = bool(re.search(r"\bmOptions\.stallTimeout\s*=", src))
    for n, (start, paren, kind) in enumerate(sorted(hits), 1):
        site = (f, n)
        found.append(site); kinds[site] = kind
        line = src.count("\n", 0, start) + 1
        lines[site] = line
        args, _ = call_args(src, paren)
        arg = args[1] if len(args) > 1 else ""
        opts[site] = arg or "none"
        if arg == "&mOptions":
            bounded[site] = member_bound
        elif arg.startswith("&"):
            var = re.escape(arg[1:])
            window = "\n".join(src[:start].split("\n")[-60:])
            bounded[site] = bool(re.search(r"\b%s\.stallTimeout\s*=" % var, window))
        else:
            bounded[site] = False
fail = ["%s, construction %d (line %d), has no entry" % (s_[0], s_[1], lines[s_]) for s_ in found if s_ not in SITES]
fail += ["an entry names %s construction %d, which is not there" % s_ for s_ in SITES if s_ not in found]
print("| Site | Function | Options passed | Connect | Stall bound | Requests |")
print("| --- | --- | --- | --- | --- | --- |")
for s_ in sorted(found):
    fn, what = SITES.get(s_, ("?", "?"))
    print("| `%s:%d` | %s | `%s` | 10 s | %s | %s |" % (s_[0], lines[s_], fn, opts[s_], "set" if bounded[s_] else "none", what))
counts = {"constructions": len(found), "new": sum(1 for k in kinds.values() if k == "new"), "stack": sum(1 for k in kinds.values() if k == "stack"), "bounded": sum(1 for v in bounded.values() if v)}
print()
print("generated, asserted: %d constructions in %d files (%d `new HttpReq(`, %d on the stack); %d set a stall bound" % (counts["constructions"], len(set(f for f, _ in found)), counts["new"], counts["stack"], counts["bounded"]))
fail += ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t32-bounds: " + "; ".join(fail))
    sys.exit(1)
