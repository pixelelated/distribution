"""3.32 (#679): the game name shows no year under a descending date sort, and a
25-hour game's time wraps to one hour.

    python3 -I l332-year-and-time.py <GameNameFormatter.cpp> <TimeUtil.cpp> [--control]

Two statements are extracted from GameNameFormatter.cpp as written: the
`mShowYear = ...;` initialiser (:84-90) and the `if (mShowGameTime)` block
(:171-185), and compiled over doubles. The second `atol` site,
DetailedContainer.cpp:1049, passes the time to Utils::Time::secondsToString
(es-core, extracted from TimeUtil.cpp as written, asTime false as the call
gives it); it is run beside as the comparison.
- mShowYear under RELEASEDATE_DESCENDING (11) must be true as it is under
  RELEASEDATE_ASCENDING (10). At the pin the initialiser tests ASCENDING twice
  (5cb43906b, upstream, wrote both lines in one commit) -- FAIL.
- 90000 s (25 h) must not read as one hour. At the pin the name carries
  [01:00:00] (2e4b5a9dc, upstream: `(seconds / 3600) % 24`, no day) -- FAIL.
  The detailed view's row reads "25 h": secondsToString folds the day back
  into the hours, so DetailedContainer.cpp:1049 does not wrap (02's run
  correction said both sites; this corrects it to one).
--control: DESCENDING in the second line and the hours without % 24.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
tu = Path(sys.argv[2]).read_text()
m = re.search(r"\tmShowYear =\n(?:\t\t.*\n)+?\t\t.*;\n", src)
if not m:
    sys.exit("FAIL l332: the mShowYear initialiser not found")
year = m.group(0)
gt = function(src, r"^\tif \(mShowGameTime\)\n", "3.32")
s2s = function(tu, r"^\t\tstd::string secondsToString\(const long seconds, bool asTime\)", "3.32")
if "--control" in sys.argv:
    a = "mSortId == FileSorts::RELEASEDATE_ASCENDING ||\n\t\tmSortId == FileSorts::RELEASEDATE_ASCENDING ||"
    assert a in year
    year = year.replace(a, "mSortId == FileSorts::RELEASEDATE_ASCENDING ||\n\t\tmSortId == FileSorts::RELEASEDATE_DESCENDING ||")
    assert "h = (seconds / 3600) % 24;" in gt
    gt = gt.replace("h = (seconds / 3600) % 24;", "h = seconds / 3600;")
harness = r'''
#include <cstdio>
#include <cstdlib>
#include <string>
#define _(x) std::string(x)
namespace FileSorts { enum { RELEASEDATE_ASCENDING = 10, RELEASEDATE_DESCENDING = 11, SYSTEM_RELEASEDATE_ASCENDING = 24,
    SYSTEM_RELEASEDATE_DESCENDING = 25, RELEASEDATE_SYSTEM_ASCENDING = 26, RELEASEDATE_SYSTEM_DESCENDING = 27 }; }
namespace Utils { namespace String { template<typename... A> std::string format(const char* f, A... a) { char b[64]; snprintf(b, 64, f, a...); return b; } } }
enum class MetaDataId { GameTime };
struct FD { std::string t; std::string getMetadata(MetaDataId) { return t; } };
namespace Utils { namespace Time {
''' + s2s + r'''
} }
static bool showYear(int mSortId) { bool mShowYear;
''' + year + r'''
    return mShowYear; }
static std::string nameWithTime(const std::string& t) { bool mShowGameTime = true; FD f{t}; FD* fd = &f; std::string name = "GAME";
''' + gt + r'''
    return name; }
int main() {
    int bad = 0;
    printf("mShowYear: RELEASEDATE_ASCENDING %d, RELEASEDATE_DESCENDING %d\n", showYear(10), showYear(11));
    if (!showYear(11)) { printf("FAIL 3.32: no year beside the name under RELEASEDATE_DESCENDING\n"); bad++; }
    for (const char* t : {"3599", "3600", "86399", "90000", "180000"}) {
        std::string n = nameWithTime(t);
        printf("%6s s: name \"%s\"   detailed row \"%s\"\n", t, n.c_str(), Utils::Time::secondsToString(atol(t), false).c_str());
    }
    if (nameWithTime("90000") == "GAME [01:00:00]") { printf("FAIL 3.32: 25 hours of play read as [01:00:00] beside the name\n"); bad++; }
    return bad ? 1 : 0;
}
'''
run(harness, "l332")
