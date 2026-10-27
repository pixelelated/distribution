"""3.9 (#680, L-27): FileFilterIndex's rating and year keys, extracted as written.

    python3 -I l309-rating-year.py <FileFilterIndex.cpp> [--control]

The RATINGS_FILTER and YEAR_FILTER blocks of getIndexableKey (the pin's
:321-340 and :364-369) are lifted into string-in/string-out helpers,
ratingKey(rating) and yearKey(releaseDate), over the metadata value they
read. The rule asserted:
- a rating above zero never reads "0 STARS" (the labels are UNKNOWN and
  1 to 5 STARS; "0.05" is a rating a scraper gave, and the filter offers
  no 0 STARS row that would mean anything);
- a release date whose first four characters are digits reads that year,
  whatever its first digit ("3000...", "0999...").
At the pin "0.05" reads 0 STARS and both dates read "". --control applies
the lane's proposed fix (a floor of one star; four digits) and must PASS.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import block, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
rating = block(src, r"^\tcase RATINGS_FILTER:\s*\n", "3.9")
year = block(src, r"^\tcase YEAR_FILTER:\s*\n", "3.9")
if "--control" in sys.argv:
    rating = rating.replace("ratingNumber = (int)Math::round(rating * 5);", "ratingNumber = std::max(1, (int)Math::round(rating * 5));")
    year = year.replace("key[0] >= '1' && key[0] <= '2'", "isdigit(key[0]) && isdigit(key[1]) && isdigit(key[2]) && isdigit(key[3])")
harness = r'''
#include <algorithm>
#include <cctype>
#include <cmath>
#include <cstdio>
#include <string>
static const std::string UNKNOWN_LABEL = "UNKNOWN";
namespace Math { float round(float v) { return std::round(v); } }
namespace Utils { namespace String { float toFloat(const std::string& s) { try { return std::stof(s); } catch (...) { return 0; } } } }
enum class MetaDataId { Rating, ReleaseDate };
struct Game { std::string v; std::string getMetadata(MetaDataId) { return v; } };
static std::string ratingKey(const std::string& value) { Game g{value}; Game* game = &g; bool getSecondary = false; std::string key;
''' + rating + r'''
}
static std::string yearKey(const std::string& value) { Game g{value}; Game* game = &g; std::string key;
    do ''' + year + r''' while (0);   // the case's `break` ends this, as it ended the switch
    return key; }
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    int bad = 0;
    for (auto r : {"", "0", "0.05", "0.1", "0.5", "1"}) {
        std::string k = ratingKey(r);
        bool wrong = std::string(r) != "" && std::string(r) != "0" && k == "0 STARS";
        printf("rating %-5s -> %s%s\n", r, k.c_str(), wrong ? "   (a positive rating reads 0 STARS)" : "");
        bad += wrong;
    }
    struct { const char* d; const char* want; } ys[] = {{"19920101T000000", "1992"}, {"20240101T000000", "2024"}, {"30000101T000000", "3000"}, {"09990101T000000", "0999"}, {"", ""}};
    for (auto& y : ys) {
        std::string k = yearKey(y.d);
        printf("year %-16s -> \"%s\"%s\n", y.d, k.c_str(), k != y.want ? "   (want the year)" : "");
        bad += k != y.want;
    }
    if (bad) { printf("FAIL 3.9: %d key(s) read against the rule\n", bad); return 1; }
    return 0;
}
'''
run(harness, "l309", ("-fsanitize=address,undefined",))
