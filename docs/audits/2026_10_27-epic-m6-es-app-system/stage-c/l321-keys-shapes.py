"""S3 (#680; #1282 PL-12, EP-10): l321's extension, KeyMappingFile::load over malformed shapes, built as the image is (NDEBUG).

    python3 -I l321-keys-shapes.py <es-app/src dir> <rapidjson include dir> <case>

The pin's whole KeyboardMapping.cpp compiled with -DNDEBUG (the recipe's,
config/functions:384-388: rapidjson's asserts compiled out) under ASan, over
stage-c/fakes-l321/. One malformed .keys per run, so a wild read is the
case's own:
  typenum    "type": 5            (a GetString on a number, :251)
  trignum    "trigger": ["up", 7] (a GetString on an array member, :265-266)
  targetobj  "target": {"a": 1}   (a GetString on an object, :288-289)
  actionstr  an action that is the string "up" (HasMember on a non-object, :250)
  chord      "trigger": ["up", "t33unknown"]: the chord must be kept whole
             or dropped whole and logged, never kept on "up" alone (EP-10)
Each must return with no sanitizer report and, for chord, no mapping on
"up" alone. At the pin the four shapes are reads the shipped build does
not check, and the chord loads on its known key.
"""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import run  # noqa: E402

srcdir = Path(sys.argv[1]); rj = sys.argv[2]; case = sys.argv[3]
cpp = (srcdir / "KeyboardMapping.cpp").read_text()
fakes = str(Path(__file__).resolve().parent / "fakes-l321")
BODY = {
 "typenum": '{ "actions_player1": [ { "type": 5, "trigger": "up", "target": "KEY_UP" } ] }',
 "trignum": '{ "actions_player1": [ { "type": "key", "trigger": ["up", 7], "target": "KEY_UP" } ] }',
 "targetobj": '{ "actions_player1": [ { "type": "key", "trigger": "up", "target": {"a": 1} } ] }',
 "actionstr": '{ "actions_player1": [ "up" ] }',
 "chord": '{ "actions_player1": [ { "type": "key", "trigger": ["up", "t33unknown"], "target": "KEY_UP", "description": "CHORD" } ] }',
}[case].replace('"', '\\"')
harness = r'''
#include "KeyboardMapping.h"
#include "Log.h"
#include <cstdio>
#include <fstream>
''' + cpp.replace('#include "KeyboardMapping.h"', "", 1) + r'''
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0);
    std::string f = std::string(argv[1]) + "/Alpha.gb.keys"; std::ofstream(f) << "''' + BODY + r'''";
    KeyMappingFile k = KeyMappingFile::load(f);
    size_t n = 0; bool upAlone = false;
    for (auto& p : k.players) for (auto& m : p.mappings) { n++; if (m.triggers.size() == 1 && m.triggers.count("up") && m.description == "CHORD") upAlone = true; }
    printf("''' + case + r''': loaded %zu mapping(s)%s; %zu log line(s)\n", n, upAlone ? ", the chord kept on \"up\" alone" : "", gLogLines().size());
    if (upAlone) { printf("FAIL chord: a chord with one refused key loads on its other key, its meaning changed (EP-10)\n"); return 1; }
    return 0;
}
'''
d = tempfile.mkdtemp(prefix="l321s-data-", dir="/workspace/tmp/m6-t33/tmp")
run(harness, "l321s", ("-fsanitize=address,undefined", "-DNDEBUG", "-I" + fakes, "-I" + str(srcdir), "-I" + rj), args=(d,))
