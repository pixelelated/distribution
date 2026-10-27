"""02 § The scrapers: one row per entry of Scraper::scrapers (#679, Q2, Q3, Q7).

    python3 -I t32-scrapers.py <es worktree> <commit> [scrapers=5,gated=3]

The registry is read from es-app/src/scrapers/Scraper.cpp at the commit:
each `{ "Name", new XScraper() }` with the #if / #ifdef it sits under (the
macro NAME only; no value is read or printed). Per scraper, from its own
file: the host literals (scheme and host, the path cut), the lines its
request's `process()` returns on, and the `setError(` lines. The routing a
status takes is the same for every scraper but ScreenScraper (T21's) and
is written once below the table: ScraperHttpRequest::update (Scraper.cpp)
-> the search handle's status -> ThreadedScraper::processError (:155-175)
-> Progress -> GuiScraperRun's line 4 (T31's).

NOTES records, per scraper, what its requests' options carry and its
success-reads, read at the lines. Exits 1 when a registry entry has no
note, a note has no entry, or a count differs.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t32lib import in_comment_or_string, show  # noqa: E402

FILES = {"ScreenScraper": "ScreenScraper.cpp", "TheGamesDB": "GamesDBJSONScraper.cpp", "HfsDB": "HfsDBScraper.cpp",
         "IGDB": "IGDBScraper.cpp", "ArcadeDB": "ArcadeDBJSONScraper.cpp"}
NOTES = {
    "ScreenScraper": ("T21's (`ScreenScraper.*`, #668): read there; its probe `getThreadCount` without bounds (T21 `02:23`), its media `Referer` at `Scraper.cpp:541-546`", "T21's"),
    "TheGamesDB": ("none on search (`ScraperHttpRequest`, `:267`); the resources fetch with no options (`GamesDBJSONScraperResources.cpp:153`)",
                   "`process` `:576` returns `true` on a parse error after `setError` (`:585-587`) and on every early exit; `:605-607` reads `HasMember` before `IsObject` (3.10); `getBoxartImage` `:293-309` throws on an array whose first element has no `filename` (3.7)"),
    "HfsDB": ("the Basic authorization header (`:179`, `:190`) and the bearer token (`:287`)",
              "`process` `:584` returns `true` on a parse error after `setError` (`:592-594`); the token's failure throws `_(\"INVALID CREDENTIALS\")` (`:217`), raised by `ThreadedScraper::start` as AN ERROR OCCURRED"),
    "IGDB": ("the Content-Type header and the POST body (`:146`, `:189`, `:205`, `:215`); the client id and its secret from `Settings` (D-QA-003, #274), never a build macro",
             "`process` `:314` returns `false` on a parse error (`:322-324`) and on a non-array (`:331`) -- the one scraper that does (3.16's remainder); offered with no client id, `ensureToken` returns `false` at `:144` and `generateRequests` throws `_(\"INVALID CREDENTIALS\")` at `:172`"),
    "ArcadeDB": ("none", "`process` `:200` returns `true` on a parse error after `setError` (`:208-210`); its `:199` comment's contract (`false` only at the scrap-per-minute limit) is dead: `Scraper.cpp:337` discards the return (3.13)"),
}

tree, commit = sys.argv[1:3]
want = dict((k, int(v)) for k, v in (kv.split("=") for kv in sys.argv[3].split(","))) if len(sys.argv) > 3 else {}
src = show(tree, commit, "es-app/src/scrapers/Scraper.cpp")
a = src.index("Scraper::scrapers")
block = src[a:src.index("};", a)]
entries, gate = [], None
for raw in block.split("\n"):
    line = raw.strip()
    m = re.match(r"#if\s+(.*)|#ifdef\s+(\w+)", line)
    if m:
        gate = " ".join(re.findall(r"[A-Z][A-Z0-9_]{3,}", m.group(1) or m.group(2)))
        continue
    if line.startswith("#endif"):
        gate = None
        continue
    m = re.match(r'\{\s*"(\w+)",\s*new\s+(\w+)\(\)', line)
    if m:
        entries.append((m.group(1), m.group(2), gate or "always"))
fail = ["%s has no note" % e[0] for e in entries if e[0] not in NOTES]
fail += ["a note names %s, which the registry does not" % n for n in NOTES if n not in [e[0] for e in entries]]
print("| Scraper | Class | Compiled under | Hosts (scheme://host) | Options its requests carry | Success-reads |")
print("| --- | --- | --- | --- | --- | --- |")
for name, cls, g in entries:
    f = FILES.get(name)
    hosts = []
    if f and name != "ScreenScraper":
        s = show(tree, commit, "es-app/src/scrapers/" + f)
        for m in re.finditer(r'"(https?://[A-Za-z0-9.-]+)', s):
            h = "%s (`:%d`)" % (m.group(1), s.count("\n", 0, m.start()) + 1)
            if m.group(1) not in [x.split(" ")[0] for x in hosts]:
                hosts.append(h)
    opts, reads = NOTES.get(name, ("?", "?"))
    print("| %s | `%s` | %s | %s | %s | %s |" % (name, cls, "`" + g + "`" if g != "always" else "always", ", ".join(hosts) or "T21's", opts, reads))
counts = {"scrapers": len(entries), "gated": sum(1 for e in entries if e[2] != "always")}
print()
print("generated, asserted: %d scrapers in the registry, %d under a build macro (by name), %d always" % (counts["scrapers"], counts["gated"], counts["scrapers"] - counts["gated"]))
print()
print("The routing, every scraper but ScreenScraper: `ScraperHttpRequest::update` (`Scraper.cpp:289`) ends `ASYNC_DONE` with no error on a 404 or an IO error (`:372-376`, 3.13), retries a 429 (`:343-361`, `Retry-After` at `:351`; T21's `44d3c7e25` reads it through `ScraperReplies`, inherited), and calls `setError` on any other failure (`:638-640`, the body's words: L-05); `process()`'s return is discarded at `:337`. An error becomes the handle's status, `ThreadedScraper::processError` (`:155-175`) counts it in `errors` or, for its seven whole-run statuses (`:157`), sets `failed`, and the page's line 4 (T31's `GuiScraperRun`) shows `removeHtmlTags(getErrorMsg())`.")
fail += ["%s %d, expected %d" % (k, counts[k], v) for k, v in want.items() if counts.get(k) != v]
if fail:
    print("FAIL t32-scrapers: " + "; ".join(fail))
    sys.exit(1)
