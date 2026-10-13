#!/usr/bin/env python3
"""UNRUN coordinator fixture: compile exact extracted ES methods with GUI/data doubles.

Requires a separate compiler/runtime allocation. No emulator, storage, broker,
network, account or installed ES import. Does not certify real rendering/saves.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent


def function(text, signature):
    start = text.index(signature)
    return text[start:text.index("\n}", start) + 2]


STUBS = r'''
#include <cassert>
#include <functional>
#include <iostream>
#include <map>
#include <memory>
#include <string>
#include <utility>
#include <vector>
#define _(x) std::string(x)
struct SystemConf {
  std::map<std::string, std::string> values;
  static SystemConf* getInstance() { static SystemConf conf; return &conf; }
  std::string get(const std::string& key) {
    auto it = values.find(key); return it == values.end() ? "" : it->second;
  }
};
namespace PlatformIds { enum Platform { IMAGEVIEWER }; }
struct Core { bool isDefault; };
struct Emulator { std::string name; std::vector<Core> cores; };
struct SystemData {
  std::vector<Emulator> mEmulators;
  bool imageviewer = false, layout = true;
  std::string name = "fixture";
  std::string getName() { return name; }
  std::vector<Emulator> getEmulators() { return mEmulators; }
  std::string getDefaultEmulator();
  std::string getEmulator(bool resolveDefault = true);
  bool hasPlatformId(PlatformIds::Platform) { return imageviewer; }
};
struct FileData {
  SystemData* system;
  FileData* source = nullptr;
  FileData* getSourceFileData() { return source ? source : this; }
  SystemData* getSystem() { return system; }
  std::string getConfigurationName() { return "fixture.game"; }
  const std::string getEmulator(bool resolveDefault = true);
  std::string getCurrentGameSetting(const std::string& settingName);
};
struct SaveStateConfigFile {
  static std::vector<int> getSaveStateConfigs(SystemData* s) {
    return s->layout ? std::vector<int>{1} : std::vector<int>{};
  }
};
struct SaveStateRepository { static bool isEnabled(FileData* game); };
struct Window;
struct GuiMsgBox {
  std::string text, button;
  GuiMsgBox(Window*, std::string t, std::string b) : text(t), button(b) {}
};
struct Window {
  std::vector<std::unique_ptr<GuiMsgBox>> dialogs;
  void pushGui(GuiMsgBox* p) { dialogs.emplace_back(p); }
};
struct GuiSettings {
  std::vector<std::pair<std::string, std::function<void()>>> rows;
  void addEntry(std::string label, bool arrow, std::function<void()> cb) {
    assert(arrow); rows.emplace_back(label, cb);
  }
};
'''

MAIN = r'''
struct Case {
  const char *id, *def, *sys, *game, *expected;
  bool gamePage, help, manager, empty, layout, imageviewer, collection;
};
struct Preference { const char *global, *sys, *game, *expected; };
int main() {
  const std::vector<Case> cases = {@CASES@};
  const std::vector<Preference> preferences = {@PREFS@};
  int count = 0;
  for (const auto& c : cases) {
    for (const auto& p : preferences) {
      auto conf = SystemConf::getInstance();
      conf->values = {{"fixture.emulator", c.sys}, {"fixture.game.emulator", c.game},
                      {"global.autosave", p.global}, {"fixture.autosave", p.sys},
                      {"fixture.game.autosave", p.game}, {"global.savestates", "1"},
                      {"unrelated.preference", "retained"}};
      const auto before = conf->values;
      SystemData system;
      if (!c.empty)
        for (const char* name : {"retroarch", "dolphin", "flycast", "dsperate"})
          system.mEmulators.push_back({name, {{std::string(name) == c.def}}});
      system.imageviewer = c.imageviewer; system.layout = c.layout;
      SystemData collection;
      collection.name = "collection";
      FileData source{&system}, game{c.collection ? &collection : &system};
      if (c.collection) game.source = &source;
      FileData systemGame{&system};
      // Manager is a game-only decision. System cases use an inheriting game.
      if (!c.gamePage) conf->values["fixture.game.emulator"] = "";
      const auto input = conf->values;
      Window window;
      auto page = std::make_unique<GuiSettings>();
      addSupport(&window, &system, c.gamePage ? &game : nullptr, page.get());
      assert((c.gamePage ? game.getEmulator() : system.getEmulator()) == c.expected);
      assert(page->rows.size() == (c.help ? 1u : 0u));
      assert(SaveStateRepository::isEnabled(c.gamePage ? &game : &systemGame) == c.manager);
      assert(game.getCurrentGameSetting("autosave") == p.expected);
      if (c.help) {
        assert(page->rows.front().first == "SAVE STATE SUPPORT");
        auto callback = page->rows.front().second;
        page.reset(); // callback must capture only the long-lived Window
        callback();
        assert(window.dialogs.size() == 1);
        assert(window.dialogs.front()->button == "OK");
        assert(window.dialogs.front()->text == @HELP@);
        window.dialogs.clear(); // dismiss once, no reopening or other action
      }
      assert(conf->values == input);
      std::cout << "PASS " << c.id << " preference-" << (count % 4) << '\n';
      ++count;
    }
  }
  std::cout << "PASS " << count << "/" << cases.size() * preferences.size() << '\n';
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--es-src", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="fresh evidence directory")
    parser.add_argument("--cxx", default="c++")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    result = {"status": "RUNNING", "scope": "synthetic extracted ES methods only"}
    try:
        binding = json.loads((HERE / "source.json").read_text())
        sources = {}
        for relative, expected in binding["es_files"].items():
            raw = (args.es_src / relative).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == expected["sha256"], relative
            sources[relative] = raw.decode()
        menu = sources["es-app/src/guis/GuiMenu.cpp"]
        start = menu.index('#if defined(ROCKNIX)\n\t// Resolve AUTO through the same')
        block = menu[start:menu.index("#endif", start) + len("#endif")]
        definitions = [function(sources[path], sig) for path, sig in (
            ("es-app/src/FileData.cpp", "const std::string FileData::getEmulator(bool resolveDefault)"),
            ("es-app/src/FileData.cpp", "std::string FileData::getCurrentGameSetting(const std::string& settingName)"),
            ("es-app/src/SystemData.cpp", "std::string SystemData::getEmulator(bool resolveDefault)"),
            ("es-app/src/SystemData.cpp", "std::string SystemData::getDefaultEmulator()"),
            ("es-app/src/SaveStateRepository.cpp", "bool SaveStateRepository::isEnabled(FileData* game)"))]
        cases = json.loads((HERE / "capability-cases.json").read_text())
        quote = json.dumps
        boolean = lambda value: "true" if value else "false"
        rows = []
        for c in cases["cases"]:
            values = [quote(c[key] or "") for key in ("id", "default", "system", "game", "expected")]
            values += [boolean(c["game"] is not None), boolean(c["help"]), boolean(c["manager"])]
            values += [boolean(c.get(key, default)) for key, default in (
                ("empty", False), ("layout", True), ("imageviewer", False), ("collection", False))]
            rows.append("{" + ",".join(values) + "}")
        prefs = ["{" + ",".join(quote(p[key]) for key in ("global", "system", "game", "expected")) + "}"
                 for p in cases["preferences"]]
        text = STUBS + "\n".join(definitions) + '''
void addSupport(Window* mWindow, SystemData* systemData, FileData* fileData, GuiSettings* systemConfiguration) {
''' + block + "\n}\n" + MAIN.replace("@CASES@", ",\n".join(rows)).replace(
            "@PREFS@", ",\n".join(prefs)).replace("@HELP@", quote(binding["help_msgid"]))
        cpp = args.output / "capability.cpp"
        cpp.write_text(text)
        binary = args.output / "capability"
        command = [args.cxx, "-std=c++17", "-DROCKNIX=1", "-fsanitize=address,undefined",
                   "-fno-omit-frame-pointer", "-g", str(cpp), "-o", str(binary)]
        result["compile_command"] = command
        compile_run = subprocess.run(command, capture_output=True, text=True, timeout=60)
        (args.output / "compile.stdout").write_text(compile_run.stdout)
        (args.output / "compile.stderr").write_text(compile_run.stderr)
        result["compile_exit"] = compile_run.returncode
        assert compile_run.returncode == 0, "compile failed"
        run = subprocess.run([str(binary)], capture_output=True, text=True, timeout=20)
        (args.output / "stdout").write_text(run.stdout)
        (args.output / "stderr").write_text(run.stderr)
        result["exit"] = run.returncode
        assert run.returncode == 0 and not run.stderr, "fixture failed"
        assert run.stdout.endswith("PASS 64/64\n"), "missing complete result"
        result["status"] = "PASS"
        result["es_commit"] = binding["es_candidate_commit"]
        result["es_files"] = binding["es_files"]
    except BaseException as error:
        result["status"] = "FAIL"
        result["error"] = repr(error)
        raise
    finally:
        (args.output / "result.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
