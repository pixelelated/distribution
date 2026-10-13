
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
const std::string FileData::getEmulator(bool resolveDefault)
{
#if WIN32 && !_DEBUG
	std::string emulator = getMetadata(MetaDataId::Emulator);
#else
	std::string emulator = SystemConf::getInstance()->get(getConfigurationName() + ".emulator");
#endif

	if (emulator == "auto")
		emulator = "";

	if (!emulator.empty())
	{
		// Check emulator exists 
		bool exists = false;

		for (auto emul : getSourceFileData()->getSystem()->getEmulators())
			if (emul.name == emulator) { exists = true; break; }

		if (!exists)
			emulator = "";
	}

	if (resolveDefault && emulator.empty())
		emulator = getSourceFileData()->getSystem()->getEmulator();

	return emulator;
}
std::string FileData::getCurrentGameSetting(const std::string& settingName)
{
	FileData* src = getSourceFileData();

	std::string value = SystemConf::getInstance()->get(getConfigurationName() + "." + settingName);
	if (!value.empty() && value != "auto")
		return value;

	value = SystemConf::getInstance()->get(src->getSystem()->getName() + "." + settingName);
	if (!value.empty() && value != "auto")
		return value;

	return SystemConf::getInstance()->get("global." + settingName);
}
std::string SystemData::getEmulator(bool resolveDefault)
{
#if WIN32 && !_DEBUG
	std::string emulator = Settings::getInstance()->getString(getName() + ".emulator");
#else
	std::string emulator = SystemConf::getInstance()->get(getName() + ".emulator");
#endif

	for (auto emul : mEmulators)
		if (emul.name == emulator)
			return emulator;

	if (resolveDefault)
		return getDefaultEmulator();

	return "";
}
std::string SystemData::getDefaultEmulator()
{
	// Seeking default="true" attribute
	for (auto emul : mEmulators)
		for (auto core : emul.cores)
			if (core.isDefault)
				return emul.name;
		
	auto emulators = getEmulators();
	if (emulators.size() > 0)
		return emulators.begin()->name;

	return "";
}
bool SaveStateRepository::isEnabled(FileData* game)
{
	auto emulatorName = game->getEmulator();

	if (emulatorName != "retroarch")
		return false;

	auto system = game->getSourceFileData()->getSystem();

	if (system->hasPlatformId(PlatformIds::IMAGEVIEWER))
		return false;

	// Should we really keep this flag ?
	// if (!game->isFeatureSupported(EmulatorFeatures::autosave))
	//	 return false;

	return SaveStateConfigFile::getSaveStateConfigs(system).size() != 0;
}
void addSupport(Window* mWindow, SystemData* systemData, FileData* fileData, GuiSettings* systemConfiguration) {
#if defined(ROCKNIX)
	// Resolve AUTO through the same per-game/system selection used at launch.
	// These launchers do not consume autosave; engine-native options are separate.
	const std::string saveStateEmulator = fileData != nullptr ? fileData->getEmulator() : systemData->getEmulator();
	if (saveStateEmulator == "dolphin" || saveStateEmulator == "flycast")
	{
		systemConfiguration->addEntry(_("SAVE STATE SUPPORT"), true, [mWindow]
		{
			mWindow->pushGui(new GuiMsgBox(mWindow,
				_("THE AUTO SAVE/LOAD SETTING AND SAVE STATE MANAGER DO NOT APPLY TO THIS EMULATOR.\n\nUSE THE EMULATOR'S OWN SAVE OPTIONS. IN-GAME SAVES ARE SEPARATE."), _("OK")));
		});
	}
#endif
}

struct Case {
  const char *id, *def, *sys, *game, *expected;
  bool gamePage, help, manager, empty, layout, imageviewer, collection;
};
struct Preference { const char *global, *sys, *game, *expected; };
int main() {
  const std::vector<Case> cases = {{"system-default-retroarch","retroarch","","","retroarch",false,false,true,false,true,false,false},
{"system-default-dolphin","dolphin","auto","","dolphin",false,true,false,false,true,false,false},
{"system-default-flycast","flycast","","","flycast",false,true,false,false,true,false,false},
{"system-explicit-dolphin","retroarch","dolphin","","dolphin",false,true,false,false,true,false,false},
{"game-inherits-flycast","retroarch","flycast","","flycast",true,true,false,false,true,false,false},
{"game-auto-inherits-dolphin","retroarch","dolphin","auto","dolphin",true,true,false,false,true,false,false},
{"game-explicit-retroarch","dolphin","dolphin","retroarch","retroarch",true,false,true,false,true,false,false},
{"game-explicit-flycast","retroarch","retroarch","flycast","flycast",true,true,false,false,true,false,false},
{"invalid-game-falls-to-system","retroarch","dolphin","missing","dolphin",true,true,false,false,true,false,false},
{"invalid-system-falls-to-default","flycast","missing","","flycast",true,true,false,false,true,false,false},
{"other-standalone-not-claimed","retroarch","dsperate","","dsperate",true,false,false,false,true,false,false},
{"empty-emulator-list","","","","",true,false,false,true,true,false,false},
{"retroarch-missing-layout","retroarch","","","retroarch",true,false,false,false,false,false,false},
{"retroarch-imageviewer","retroarch","","","retroarch",true,false,false,false,true,true,false},
{"collection-source-flycast","retroarch","flycast","auto","flycast",true,true,false,false,true,false,true},
{"dolphin-layout-cannot-enable-manager","dolphin","","","dolphin",true,true,false,false,true,false,false}};
  const std::vector<Preference> preferences = {{"1","0","auto","0"},
{"0","1","0","0"},
{"1","auto","","1"},
{"0","","1","1"}};
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
        assert(window.dialogs.front()->text == "THE AUTO SAVE/LOAD SETTING AND SAVE STATE MANAGER DO NOT APPLY TO THIS EMULATOR.\n\nUSE THE EMULATOR'S OWN SAVE OPTIONS. IN-GAME SAVES ARE SEPARATE.");
        window.dialogs.clear(); // dismiss once, no reopening or other action
      }
      assert(conf->values == input);
      std::cout << "PASS " << c.id << " preference-" << (count % 4) << '\n';
      ++count;
    }
  }
  std::cout << "PASS " << count << "/" << cases.size() * preferences.size() << '\n';
}
