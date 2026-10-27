| Page | Class : base | Opened from | Starts (census) | Dialogs (site, buttons, back) | Title | The map |
| --- | --- | --- | --- | --- | --- | --- |
| `GuiAnalogSticksLedControls` | GuiAnalogSticksLedControls : GuiSettings | GuiMenu.cpp | runSystemCommand 1 | - | ANALOG STICKS LEDS | ANALOG STICKS LEDS: declared |
| `GuiAutoScrape` | GuiAutoScrape : GuiComponent | nothing | std::thread 2 | :68 OK, back OK; :78 OK, back OK | - | - |
| `GuiBackup` | GuiBackup : GuiComponent | GuiBackupStart.cpp | std::thread 2 | :61 OK, back OK; :71 OK, back OK | - | - |
| `GuiBackupStart` | GuiBackupStart : GuiComponent | GuiMenu.cpp | - | - | BACKUP USER DATA | BACKUP USER DATA: neither |
| `GuiBatoceraStore` | GuiBatoceraStoreEntry : ComponentGrid; GuiBatoceraStore : GuiComponent | GuiMenu.cpp | GuiLoading< 1, postToUiThread 2 | - | CONTENT DOWNLOADER | CONTENT DOWNLOADER: neither |
| `GuiBezelInstaller` | GuiBatoceraBezelEntry : ComponentGrid; GuiBezelInstaller : GuiComponent | GuiMenu.cpp | GuiLoading< 1 | - | THE BEZEL PROJECT | THE BEZEL PROJECT: neither |
| `GuiBios` | GuiBios : GuiComponent | GuiMenu.cpp | GuiLoading< 2 | - | BIOS CHECK | BIOS CHECK: neither |
| `GuiBluetoothDeviceOptions` | GuiBluetoothDeviceOptions : GuiComponent | GuiBluetoothDevices.cpp | GuiLoading< 3 | :56 YES / NO, back NO; :81 YES / NO, back NO; :106 YES / NO, back NO | DEVICE OPTIONS | DEVICE OPTIONS: neither |
| `GuiBluetoothDevices` | GuiBluetoothDevices : GuiComponent | GuiControllersSettings.cpp | GuiLoading< 2 | :120 OK, back OK; :144 YES / NO, back NO | BLUETOOTH DEVICE LIST | BLUETOOTH DEVICE LIST: neither |
| `GuiBluetoothPair` | GuiBluetoothPair : MenuComponent | GuiControllersSettings.cpp | std::thread 2, GuiLoading< 1, postToUiThread 1 | - | PAIR A BLUETOOTH DEVICE | PAIR A BLUETOOTH DEVICE: declared |
| `GuiCollectionSystemsOptions` | GuiCollectionSystemsOptions : GuiSettings | GuiMenu.cpp | postToUiThread 1 | - | GAME COLLECTION SETTINGS | GAME COLLECTION SETTINGS: mapped |
| `GuiControllersSettings` | GuiControllersSettings : GuiSettings | GuiMenu.cpp | runSystemCommand 2, GuiLoading< 1 | :76 OK / CANCEL, back OK; :182 OK, back OK; :687 OK, back OK; :689 OK, back OK | GLOBAL HOTKEYS, JOYSTICKS HOTKEYS, KEYBOARDTOPADS | GLOBAL HOTKEYS: declared; JOYSTICKS HOTKEYS: declared; KEYBOARDTOPADS: declared |
| `GuiFavoriteMusicSelector` | GuiFavoriteMusicSelector : GuiComponent | GuiMenu.cpp | - | - | FAVORITE SONGS | FAVORITE SONGS: declared |
| `GuiFileBrowser` | GuiFileBrowser : GuiComponent | GuiGeneralScreensaverOptions.cpp, GuiMetaDataEd.cpp, GuiSettings.cpp | - | - | - | - |
| `GuiGameOptions` | GuiGameOptions : GuiComponent | ISimpleGameListView.cpp | GuiLoading< 1 | :182 OK, back OK; :194 OK, back OK; :253 YES / NO, back NO; :274 WRITE / CANCEL, back CANCEL; :289 CLOSE, back CLOSE; :292 OK, back OK; :549 OK, back OK; :630 YES / NO, back NO | ADD TO CUSTOM COLLECTION..., NETPLAY | ADD TO CUSTOM COLLECTION...: declared; NETPLAY: mapped |
| `GuiGameScraper` | GuiGameScraper : GuiComponent | GuiGameOptions.cpp, GuiMetaDataEd.cpp | - | - | - | - |
| `GuiGamelistFilter` | GuiGamelistFilter : GuiComponent | GuiCollectionSystemsOptions.cpp, GuiGamelistOptions.cpp | - | - | EDIT DYNAMIC COLLECTION FILTERS, FILTER GAMELIST BY | EDIT DYNAMIC COLLECTION FILTERS: neither; FILTER GAMELIST BY: neither |
| `GuiGamelistOptions` | GuiGamelistOptions : GuiComponent | GridGameListView.cpp, ISimpleGameListView.cpp | - | :461 OK, back OK; :660 YES / NO, back NO | VIEW OPTIONS | VIEW OPTIONS: mapped |
| `GuiGeneralScreensaverOptions` | GuiGeneralScreensaverOptions : GuiSettings | GuiMenu.cpp | - | - | SCREENSAVER SETTINGS | SCREENSAVER SETTINGS: declared |
| `GuiHashStart` | GuiHashStart : GuiComponent | GuiNetPlaySettings.cpp, GuiRetroAchievementsSettings.cpp | - | - | INDEX GAMES | INDEX GAMES: mapped |
| `GuiImageViewer` | GuiImageViewer : GuiComponent; GuiVideoViewer : GuiComponent; ZoomableImageComponent : ImageComponent | GuiGameOptions.cpp, GuiMenu.cpp, ViewController.cpp | GuiLoading< 3, postToUiThread 4 | - | - | - |
| `GuiInstall` | GuiInstall : GuiComponent | GuiInstallStart.cpp | std::thread 2 | :62 OK, back OK; :72 OK, back OK | - | - |
| `GuiInstallStart` | GuiInstallStart : GuiComponent | GuiMenu.cpp | - | :82 OK, back OK | INSTALL ON A NEW DISK | INSTALL ON A NEW DISK: neither |
| `GuiKeyMappingEditor` | GuiKeyMappingEditorEntry : ComponentGrid; GuiKeyMappingEditor : GuiComponent | GuiMenu.cpp | - | :455 YES / NO, back NO; :497 YES / NO, back NO; :506 YES / NO, back NO | PAD TO KEYBOARD CONFIGURATION | PAD TO KEYBOARD CONFIGURATION: neither |
| `GuiKeyboardLayout` | GuiKeyboardLayout : GuiComponent | GuiKeyMappingEditor.cpp | - | - | - | - |
| `GuiKeyboardtopads` | GuiKeyboardtopads : GuiSettings | GuiControllersSettings.cpp | GuiLoading< 1 | - | KEYBOARDTOPADS | KEYBOARDTOPADS: declared |
| `GuiMetaDataEd` | GuiMetaDataEd : GuiComponent | GuiGameOptions.cpp, GuiGamelistOptions.cpp | - | :365 YES / NO, back NO; :524 YES / NO / CANCEL, back NO; :629 YES / NO, back NO | EDIT METADATA | EDIT METADATA: neither |
| `GuiMoonlight` | GuiMoonlight : GuiSettings | GuiMenu.cpp | runSystemCommand 3, executeScript 5, popen 1 | :295 OK, back OK; :315 OK, back OK; :333 OK, back OK; :336 OK, back OK | not a _() literal: `"MOONLIGHT GAME STREAMING"` | - |
| `GuiNetPlay` | GuiNetPlay : GuiComponent; NetPlayLobbyListEntry : ComponentGrid | SystemView.cpp | std::thread 2 | :336 OK, back OK | CONNECT TO NETPLAY | CONNECT TO NETPLAY: declared |
| `GuiNetPlaySettings` | GuiNetPlaySettings : GuiSettings | GuiMenu.cpp | - | - | NETPLAY SETTINGS | NETPLAY SETTINGS: declared |
| `GuiSaveState` | GuiSaveState : GuiComponent | GuiGameOptions.cpp, ISimpleGameListView.cpp | - | :442 OK, back OK; :449 YES / NO, back NO; :457 OK, back OK; :503 OK, back OK | SAVE STATE MANAGER | SAVE STATE MANAGER: mapped |
| `GuiScraperRun` | GuiScraperRun : GuiComponent | GuiScraperStart.cpp | - | :112 YES / NO, back NO | SCRAPING GAMES | SCRAPING GAMES: neither |
| `GuiScraperStart` | GuiScraperStart : GuiSettings | GuiMenu.cpp | GuiLoading< 1 | :438 OK, back OK; :449 YES / NO, back NO; :467 YES / NO, back NO; :483 OK, back OK | SCRAPER | SCRAPER: mapped |
| `GuiSettings` | GuiSettings : GuiComponent | GuiBatoceraStore.cpp, GuiBezelInstaller.cpp, GuiBios.cpp, GuiCollectionSystemsOptions.cpp, GuiControllersSettings.cpp | - | :449 OK, back OK | not a _() literal: `title` | - |
| `GuiSystemInformation` | GuiSystemInformation : GuiSettings | GuiMenu.cpp | - | - | INFORMATION | INFORMATION: mapped |
| `GuiThemeInstaller` | GuiBatoceraThemeEntry : ComponentGrid; GuiThemeInstaller : GuiComponent | GuiMenu.cpp | GuiLoading< 1, postToUiThread 1 | - | THEMES DOWNLOADER | THEMES DOWNLOADER: neither |
| `GuiUpdate` | GuiUpdate : GuiComponent | GuiMenu.cpp | std::thread 6 | :97 YES / NO, back NO; :113 OK, back OK; :123 OK, back OK | - | - |
| `GuiLoading (header only)` | GuiLoading : GuiComponent | CloudOffer.cpp, FileData.cpp, GuiBatoceraStore.cpp, GuiBezelInstaller.cpp, GuiBios.cpp, GuiBluetoothDeviceOptions.cpp | std::thread 2 | - | - | - |
| `WifiScanProcess (header only)` | - | GuiWifi.cpp | - | - | - | - |

pages 37, header-only units 2; runSystemCommand 6, executeScript 5, std::thread 18, GuiLoading< 18, postToUiThread 9, popen 1, system 0
