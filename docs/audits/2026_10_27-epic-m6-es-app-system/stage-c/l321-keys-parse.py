"""3.21 (#680, L-28): KeyMappingFile::load with a trigger the table refuses.

    python3 -I l321-keys-parse.py <es-app/src dir> <rapidjson include dir> [--control]

The pin's whole KeyboardMapping.cpp is compiled over three fakes under
stage-c/fakes-l321/ (FileSystemUtil.h on the host's files; StringUtil.h's
five calls; a Log.h that records each LOG line). A .keys file holding one
mapping on `up` and one on `t33unknown` is loaded. The rule asserted (the
brief's Q3: "a logged line or a refused load"): a mapping dropped because
its trigger is refused is either named in a log line, or the load is
refused (no mappings). At the pin the second mapping is dropped (`:262-272`,
then `:292` keeps a mapping only with a trigger) and nothing is logged:
the guest's G-08 showed the same on the image. --control adds one LOG line
where checkTriggerExists refuses, the lane's proposed fix, and must PASS.
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import run  # noqa: E402

srcdir = Path(sys.argv[1])
rj = sys.argv[2]
cpp = (srcdir / "KeyboardMapping.cpp").read_text()
if "--control" in sys.argv:
    cpp, n = re.subn(r"if \(checkTriggerExists\(([^,]+), map\.type\)\)\n(\t+)(map\.triggers\.insert\([^;]+;)",
                     r'if (checkTriggerExists(\1, map.type))\n\2\3\n\2else LOG(LogWarning) << "KeyMappingFile - unknown trigger " << \1 << " in " << fileName;', cpp)
    assert n == 2, n
fakes = str(Path(__file__).resolve().parent / "fakes-l321")
harness = r'''
#include "KeyboardMapping.h"
#include "Log.h"
#include <cstdio>
#include <fstream>
''' + cpp.replace('#include "KeyboardMapping.h"', "", 1) + r'''
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0);
    std::string f = std::string(argv[1]) + "/Alpha.gb.keys";
    std::ofstream(f) << "{ \"actions_player1\": [ { \"type\": \"key\", \"trigger\": \"up\", \"target\": \"KEY_UP\", \"description\": \"KNOWN\" },"
                        " { \"type\": \"key\", \"trigger\": \"t33unknown\", \"target\": \"KEY_DOWN\", \"description\": \"UNKNOWN TRIGGER\" } ] }";
    KeyMappingFile k = KeyMappingFile::load(f);
    size_t n = k.players.empty() ? 0 : k.players[0].mappings.size();
    printf("loaded: player 1 holds %zu mapping(s)", n);
    for (auto& m : k.players.empty() ? std::vector<KeyMappingFile::KeyMapping>() : k.players[0].mappings) printf(" [%s]", m.description.c_str());
    printf("\n");
    bool said = false;
    for (auto& l : gLogLines()) { printf("log: %s\n", l.c_str()); if (l.find("t33unknown") != std::string::npos) said = true; }
    if (n == 1 && !said) { printf("FAIL 3.21: a mapping whose trigger the table refuses is dropped and nothing says so (L-28)\n"); return 1; }
    return 0;
}
'''
d = tempfile.mkdtemp(prefix="l321-data-", dir="/workspace/tmp/m6-t33/tmp")
run(harness, "l321", ("-fsanitize=address,undefined", "-I" + fakes, "-I" + str(srcdir), "-I" + rj), args=(d,))
