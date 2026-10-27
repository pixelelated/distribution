| Site | Message (first words) | Buttons in order | Back lands on | Its callback |
| --- | --- | --- | --- | --- |
| `GuiAutoScrape.cpp:68` | FINISHED | OK | OK | `[this] { mState = -1; }` |
| `GuiAutoScrape.cpp:78` | <mResult.first> | OK | OK | `[this] { mState = -1; }` |
| `GuiBackup.cpp:61` | FINISHED | OK | OK | `[this] { mState = -1; }` |
| `GuiBackup.cpp:71` | <mResult.first> | OK | OK | `[this] { mState = -1; }` |
| `GuiBluetoothDeviceOptions.cpp:56` | ARE YOU SURE YOU WANT TO FORGET ... | YES / NO | NO | `nullptr` |
| `GuiBluetoothDeviceOptions.cpp:81` | ARE YOU SURE YOU WANT TO CONNECT ... | YES / NO | NO | `nullptr` |
| `GuiBluetoothDeviceOptions.cpp:106` | ARE YOU SURE YOU WANT TO DISCONNECT ... | YES / NO | NO | `nullptr` |
| `GuiBluetoothDevices.cpp:120` | BLUETOOTH DEVICES HAVE BEEN DELETED. | OK | OK | `nullptr` |
| `GuiBluetoothDevices.cpp:144` | ARE YOU SURE YOU WANT TO REMOVE ... | YES / NO | NO | `nullptr` |
| `GuiControllersSettings.cpp:76` | YOU ARE GOING TO MAP A CONTROLLER. ... | OK / CANCEL | OK | `[window, this] { window->pushGui(new GuiDetectDevice(window,...` |
| `GuiControllersSettings.cpp:182` | BLUETOOTH SCAN IS ALREADY RUNNING. | OK | OK | `nullptr` |
| `GuiControllersSettings.cpp:687` | NO GLOBAL HOTKEY DETECTED | OK | OK | `nullptr` |
| `GuiControllersSettings.cpp:689` | MORE THAN ONE GLOBAL HOTKEY DETECTED | OK | OK | `nullptr` |
| `GuiGameOptions.cpp:182` | YOU ARE NOT CONNECTED TO A NETWORK | OK | OK | `nullptr` |
| `GuiGameOptions.cpp:194` | YOU ARE NOT CONNECTED TO A NETWORK | OK | OK | `nullptr` |
| `GuiGameOptions.cpp:253` | THIS WILL DELETE THE ACTUAL GAME FILE(S)! ... | YES / NO | NO | `nullptr` |
| `GuiGameOptions.cpp:274` | IN ORDER TO WRITE THE LAUNCH COMMAND ... | WRITE / CANCEL | CANCEL | `nullptr` |
| `GuiGameOptions.cpp:289` | AN ERROR OCCURRED | CLOSE | CLOSE | `nullptr` |
| `GuiGameOptions.cpp:292` | THE TAG WAS WRITTEN SUCCESSFULLY | OK | OK | `nullptr` |
| `GuiGameOptions.cpp:549` | THIS FUNCTION IS DISABLED WHILE THE SCRAPER ... | OK | OK | `nullptr` |
| `GuiGameOptions.cpp:630` | ARE YOU SURE YOU WANT TO DELETE ... | YES / NO | NO | `[this] { delete this; }` |
| `GuiGamelistOptions.cpp:461` | THIS FUNCTION IS DISABLED WHILE THE SCRAPER ... | OK | OK | `nullptr` |
| `GuiGamelistOptions.cpp:660` | ARE YOU SURE YOU WANT TO DELETE ... | YES / NO | NO | `nullptr` |
| `GuiInstall.cpp:62` | FINISHED | OK | OK | `[this] { mState = -1; }` |
| `GuiInstall.cpp:72` | <mResult.first> | OK | OK | `[this] { mState = -1; }` |
| `GuiInstallStart.cpp:82` | INVALID PARAMETERS | OK | OK | `nullptr` |
| `GuiKeyMappingEditor.cpp:455` | ARE YOU SURE YOU WANT TO DELETE ... | YES / NO | NO | `nullptr` |
| `GuiKeyMappingEditor.cpp:497` | SAVE CHANGES? | YES / NO | NO | `[this] { delete this; }` |
| `GuiKeyMappingEditor.cpp:506` | ARE YOU SURE? | YES / NO | NO | `[this] { }` |
| `GuiMetaDataEd.cpp:365` | THIS WILL DELETE THE ACTUAL GAME FILE(S)! ... | YES / NO | NO | `nullptr` |
| `GuiMetaDataEd.cpp:524` | SOME FILES YOU LINKED ARE LOCATED OUTSIDE ... | YES / NO / CANCEL | NO | `[this, performSave] { performSave(std::set<std::string>()); ...` |
| `GuiMetaDataEd.cpp:629` | SAVE CHANGES? | YES / NO | NO | `closeFunc` |
| `GuiMoonlight.cpp:295` | Unable to connect to server | OK | OK | `nullptr` |
| `GuiMoonlight.cpp:315` | Succesfully paired with server | OK | OK | `nullptr` |
| `GuiMoonlight.cpp:333` | Unpaired and settings cleared | OK | OK | `nullptr` |
| `GuiMoonlight.cpp:336` | Unpaired from server | OK | OK | `nullptr` |
| `GuiNetPlay.cpp:336` | FAILED : | OK | OK | `nullptr` |
| `GuiSaveState.cpp:442` | <busy> | OK | OK | `nullptr` |
| `GuiSaveState.cpp:449` | ARE YOU SURE YOU WANT TO DELETE ... | YES / NO | NO | `nullptr` |
| `GuiSaveState.cpp:457` | <busyNow> | OK | OK | `nullptr` |
| `GuiSaveState.cpp:503` | <busy> | OK | OK | `nullptr` |
| `GuiScraperRun.cpp:112` | CANCEL SCRAPING? WHAT'S SCRAPED SO FAR IS ... | YES / NO | NO | `nullptr` |
| `GuiScraperStart.cpp:438` | SCREENSCRAPER NEEDS A DEVELOPER ID AND PASSWORD. ... | OK | OK | `nullptr` |
| `GuiScraperStart.cpp:449` | WARNING: SOME OF YOUR SELECTED SYSTEMS DO ... | YES / NO | NO | `nullptr` |
| `GuiScraperStart.cpp:467` | SCRAPING IS RUNNING. DO YOU WANT TO ... | YES / NO | NO | `nullptr` |
| `GuiScraperStart.cpp:483` | NO GAMES FIT THAT CRITERIA. | OK | OK | `nullptr` |
| `GuiSettings.cpp:449` | YOU ARE NOT CONNECTED TO A NETWORK | OK | OK | `nullptr` |
| `GuiUpdate.cpp:97` | <message> | YES / NO | NO | `[this] { mState = -1; }` |
| `GuiUpdate.cpp:113` | NETWORK CONNECTION NEEDED | OK | OK | `[this] { mState = -1; }` |
| `GuiUpdate.cpp:123` | NO UPDATE AVAILABLE | OK | OK | `[this] { mState = -1; }` |

sites 50 in 18 files; back lands on: OK 30, NO 18, CANCEL 1, CLOSE 1
