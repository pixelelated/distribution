"""Execute the unchanged profile-choice callback with real deletion under ASan."""
from pathlib import Path
import subprocess,tempfile,sys
E=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]).read_text() if len(sys.argv)>1 else (E/'es-app/src/guis/GuiWifi.cpp').read_text()
start=source.index('void GuiWifi::chooseProfile(');end=source.index('\n}\n',start)+3
body=source[start:end]
test=r'''
#include "WifiText.h"
#include <cassert>
#include <functional>
#include <string>
#include <vector>
#define _(s) (s)
struct GuiSettings;
struct Window { GuiSettings* page; void pushGui(GuiSettings* p){page=p;} };
struct GuiSettings {
 std::vector<std::function<void()>> rows;
 GuiSettings(Window*, const std::string&) {}
 void addEntry(const std::string&,bool,std::function<void()> f){rows.push_back(f);}
 void close(){delete this;}
};
struct GuiWifi {
 Window* mWindow;
 std::vector<WifiText::SavedNetwork> mSaved;
 std::string network, profile;
 void chooseProfile(const std::string& name);
 void act(WifiText::PressAction a,const std::string& n,const std::string& p) {
  assert(a==WifiText::PressAction::ChooseSaved);network=n;profile=p;
 }
};
'''+body+r'''
int main(){Window w;GuiWifi picker{&w,{{"Renamed profile",false,"Cafe"},{"Another",false,"Cafe"}}};
 picker.chooseProfile("Cafe");assert(w.page->rows.size()==2);w.page->rows[0]();
 assert(picker.network=="Cafe" && picker.profile=="Renamed profile");}
'''
with tempfile.TemporaryDirectory() as t:
 p=Path(t);(p/'test.cpp').write_text(test)
 subprocess.run(['g++','-std=c++17','-g','-fsanitize=address','-fno-omit-frame-pointer','-I'+str(E/'es-app/src'),str(p/'test.cpp'),str(E/'es-app/src/WifiText.cpp'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
print('PASS profile-choice callback survives page deletion')
