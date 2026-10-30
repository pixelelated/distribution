"""S4b (#680; #1284 PL-15): what CloudOffer's create box says, from the seed run's exit status and its lines.

    python3 -I s4b-cloudoffer.py <es-app/src>

The outcome is outcomeFor(rc, lines) in CloudOffer.cpp when the file has it
(the fix), extracted as written with CloudText's cleanLine and
classifyProtocolLine (and their wholeNumber) from CloudText.cpp as written;
_ and localizedWhy are the English interface's (identity). At the pin there
is no such function: the run's lines go to a callback that keeps none
(CloudOffer.cpp:37-38) and the box is `rc == 0 ? <DONE> : <the connection
sentence>` (:42-44); the harness builds outcomeFor from those two msgids as
the pin has them, the lines unread. Each case is a run cloud_setup
--seed-folders saves can end in (its --seed-folders branch: a why on every
failure, `OK <folder>` for the saves folder found, `MISSING` with exit 5,
`ERROR no remote` with 2, the lock's 75; timeout's 124).
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import function, run  # noqa: E402

src = Path(sys.argv[1])
offer = (src / "CloudOffer.cpp").read_text()
cloud = (src / "CloudText.cpp").read_text()
cloud_h = (src / "CloudText.h").read_text()
if re.search(r"^static std::string outcomeFor\(", offer, re.M):
    outcome = function(offer, r"^static std::string outcomeFor\(", "S4b")
    shape = "outcomeFor, as written"
else:
    m = re.search(r'rc == 0\s*\?\s*(_\("[^"]*"\))\s*:\s*(_\("[^"]*"\))', offer)
    assert m, "the pin's ternary"
    outcome = ("static std::string outcomeFor(int rc, const std::vector<std::string>& lines)\n{\n\t(void) lines;   // :38 keeps none\n"
               "\treturn rc == 0\n\t\t? %s\n\t\t: %s;\n}" % (m.group(1), m.group(2)))
    shape = "the pin's ternary (:42-44), the lines unread (:38)"
clean = function(cloud, r"^std::string cleanLine\(const std::string& raw\)", "S4b")
classify = function(cloud, r"^ProtocolLine classifyProtocolLine\(const std::string& clean\)", "S4b")
whole = function(cloud, r"^\s*(static )?bool wholeNumber\(", "S4b")
kinds = re.search(r"enum class ProtocolKind[^;]*;", cloud_h).group(0)
removed = function(cloud_h, r"^\s*struct RemovedSystem", "S4b") + ";"
pline = function(cloud_h, r"^\s*struct ProtocolLine", "S4b") + ";"
print("outcome: " + shape)

harness = r'''
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <cctype>
#include <cstdarg>
static std::string _(const char* s) { return s; }
namespace Utils { namespace String {
	std::string trim(const std::string& s) { size_t a = s.find_first_not_of(" \t\r\n"); if (a == std::string::npos) return ""; size_t b = s.find_last_not_of(" \t\r\n"); return s.substr(a, b - a + 1); }
	std::string toUpper(std::string s) { for (auto& c : s) c = (char) toupper((unsigned char) c); return s; }
	std::vector<std::string> split(const std::string& s, char c, bool = false) { std::vector<std::string> o; std::string cur; for (char x : s) { if (x == c) { o.push_back(cur); cur.clear(); } else cur += x; } o.push_back(cur); return o; }
	std::string format(const char* f, ...) { char b[1024]; va_list a; va_start(a, f); vsnprintf(b, sizeof b, f, a); va_end(a); return b; }
	bool startsWith(const std::string& s, const std::string& p) { return s.rfind(p, 0) == 0; }
} }
namespace CloudText {
''' + kinds + "\n" + removed + "\n" + pline + "\n" + whole + "\n" + clean + "\n" + classify + r'''
	std::string localizedWhy(const std::string& why) { return why; }
	bool isKnownWhy(const std::string&) { return true; }
}
''' + outcome + r'''

static int bad = 0;
static void expect(const char* name, int rc, std::vector<std::string> lines, const std::string& want)
{
	const std::string got = outcomeFor(rc, lines);
	const bool ok = got == want;
	printf("%s %s: rc %d -> \"%s\"%s\n", ok ? "PASS" : "FAIL", name, rc, got.c_str(), ok ? "" : (" (want \"" + want + "\")").c_str());
	if (!ok) bad++;
}

int main()
{
	setvbuf(stdout, nullptr, _IONBF, 0);
	const std::string DONE = "DONE. YOUR SAVES WILL GO THERE THE NEXT TIME YOU BACK THEM UP.";
	const std::string NOWHY = "COULDN'T CREATE IT. CHECK YOUR CONNECTION AND TRY AGAIN FROM MANAGE CLOUD STORAGE.";
	auto with = [](const char* why) { return std::string("COULDN'T CREATE IT. ") + why + ". TRY AGAIN FROM MANAGE CLOUD STORAGE."; };
	expect("created", 0, { "OK /pixelelated/saves" }, DONE);
	expect("rc0-no-ok", 0, {}, NOWHY);
	expect("rc0-why", 0, { "OK /pixelelated/saves", ">>> why YOUR CLOUD FOLDERS COULDN'T BE CREATED" }, with("YOUR CLOUD FOLDERS COULDN'T BE CREATED"));
	expect("timeout", 124, {}, with("YOUR CLOUD STOPPED ANSWERING"));
	expect("missing", 5, { "MISSING /pixelelated/saves", ">>> why YOUR CLOUD FOLDERS COULDN'T BE CREATED" }, with("YOUR CLOUD FOLDERS COULDN'T BE CREATED"));
	expect("locked", 75, { ">>> why ANOTHER CLOUD SYNC IS RUNNING" }, with("ANOTHER CLOUD SYNC IS RUNNING"));
	expect("no-remote", 2, { "ERROR no remote" }, NOWHY);
	if (bad)
		printf("FAIL S4b CloudOffer: %d case(s)\n", bad);
	return bad ? 1 : 0;
}
'''
run(harness, "s4b-offer")
