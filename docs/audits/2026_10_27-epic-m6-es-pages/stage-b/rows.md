| Site | Builder | Label | Key | Store | Form |
| --- | --- | --- | --- | --- | --- |
| `GuiBluetoothDevices.cpp:60` | addWithDescription | <name + status> | `-` | - | MenuComponent func form: multiLine = false |
| `GuiBluetoothPair.cpp:93` | addWithDescription | <name> | `-` | - | func form: multiLine = false |
| `GuiCollectionSystemsOptions.cpp:363` | addSwitch | SHOW EMPTY SYSTEMS | `LoadEmptySystems` | Settings | no description |
| `GuiCollectionSystemsOptions.cpp:364` | addSwitch | DON'T SHOW GROUPS WITH ONLY ONE SYSTEM | `HideUniqueGroups` | Settings | no description |
| `GuiControllersSettings.cpp:198` | addSwitch | SHOW CONTROLLER NOTIFICATIONS | `ShowControllerNotifications` | Settings | no description |
| `GuiControllersSettings.cpp:215` | addSwitch | SHOW CONTROLLER BATTERY LEVEL | `ShowControllerBattery` | Settings | no description |
| `GuiControllersSettings.cpp:217` | addSwitch | SHOW GUN NOTIFICATIONS | `ShowGunsNotifications` | Settings | no description |
| `GuiControllersSettings.cpp:218` | addSwitch | DRAW GUN CROSSHAIR | `DrawGunCrosshair` | Settings | no description |
| `GuiControllersSettings.cpp:704` | addOptionList | BORDER SIZE | `controllers.guns.borderssize` | SystemConf | no description |
| `GuiControllersSettings.cpp:712` | addOptionList | BORDER MODE | `controllers.guns.bordersmode` | SystemConf | no description |
| `GuiControllersSettings.cpp:721` | addOptionList | BORDER COLOR | `controllers.guns.borderscolor` | SystemConf | no description |
| `GuiFavoriteMusicSelector.cpp:47` | addWithDescription | <file.second> | `-` | - | GuiSettings func form: multiLine = false |
| `GuiGameOptions.cpp:126` | addWithDescription | VIEW THIS GAME'S ACHIEVEMENTS | `-` | - | func form: multiLine = true |
| `GuiGameOptions.cpp:203` | addInputTextConfigRow | NETPLAY NICKNAME | `global.netplay.nickname` | SystemConf (default) | plain |
| `GuiGameOptions.cpp:204` | addInputTextConfigRow | PLAYER PASSWORD | `global.netplay.password` | SystemConf (default) | plain |
| `GuiGameOptions.cpp:215` | addInputTextConfigRow | NETPLAY HOST | `global.netplay.host` | SystemConf (default) | plain |
| `GuiGameOptions.cpp:216` | addInputTextConfigRow | NETPLAY PORT | `global.netplay.port` | SystemConf (default) | plain |
| `GuiGamelistOptions.cpp:77` | addWithDescription | OTHER FILTERS | `-` | - | MenuComponent func form: multiLine = false |
| `GuiGamelistOptions.cpp:174` | addWithDescription | EDIT DYNAMIC COLLECTION FILTERS | `-` | - | MenuComponent func form: multiLine = false |
| `GuiKeyboardtopads.cpp:168` | addInputTextRow | JOYSTICK NAME | `-` | caller's onsave | plain |
| `GuiMoonlight.cpp:341` | addInputTextConfigRow | SERVER IP | `moonlight.host` | SystemConf (default) | plain |
| `GuiNetPlaySettings.cpp:26` | addInputTextConfigRow | NICKNAME | `global.netplay.nickname` | SystemConf (default) | plain |
| `GuiNetPlaySettings.cpp:33` | addInputTextConfigRow | HOST | `global.netplay.host` | SystemConf (default) | plain |
| `GuiNetPlaySettings.cpp:34` | addInputTextConfigRow | PORT | `global.netplay.port` | SystemConf (default) | plain |
| `GuiNetPlaySettings.cpp:38` | addSwitch | AUTOMATICALLY CREATE LOBBY | `NetPlayAutomaticallyCreateLobby` | Settings | with description |
| `GuiNetPlaySettings.cpp:39` | addSwitch | SHOW RELAY SERVER GAMES ONLY | `NetPlayShowOnlyRelayServerGames` | Settings | with description |
| `GuiNetPlaySettings.cpp:40` | addSwitch | SHOW UNAVAILABLE GAMES | `NetPlayShowMissingGames` | Settings | with description |
| `GuiNetPlaySettings.cpp:45` | addSwitch | INDEX NEW GAMES AT STARTUP | `NetPlayCheckIndexesAtStart` | Settings | no description |
| `GuiNetPlaySettings.cpp:191` | addInputTextConfigRow | CUSTOM RELAY SERVER | `global.netplay.customserver` | SystemConf (default) | plain |
| `GuiScraperStart.cpp:346` | addSwitch | OVERWRITE NAMES | `ScrapeNames` | Settings | no description |
| `GuiScraperStart.cpp:347` | addSwitch | OVERWRITE DESCRIPTIONS | `ScrapeDescription` | Settings | no description |
| `GuiScraperStart.cpp:348` | addSwitch | OVERWRITE MEDIAS | `ScrapeOverWrite` | Settings | no description |
| `GuiScraperStart.cpp:353` | addSwitch | SHORT NAME | `ScrapeShortTitle` | Settings | no description |
| `GuiScraperStart.cpp:356` | addSwitch | COMMUNITY RATING | `ScrapeRatings` | Settings | no description |
| `GuiScraperStart.cpp:359` | addSwitch | VIDEO | `ScrapeVideos` | Settings | no description |
| `GuiScraperStart.cpp:362` | addSwitch | FAN ART | `ScrapeFanart` | Settings | no description |
| `GuiScraperStart.cpp:365` | addSwitch | BOX BACKSIDE | `ScrapeBoxBack` | Settings | no description |
| `GuiScraperStart.cpp:368` | addSwitch | MAP | `ScrapeMap` | Settings | no description |
| `GuiScraperStart.cpp:372` | addSwitch | SCRAPE TITLESHOT | `ScrapeTitleShot` | Settings | no description |
| `GuiScraperStart.cpp:375` | addSwitch | SCRAPE CARTRIDGE | `ScrapeCartridge` | Settings | no description |
| `GuiScraperStart.cpp:379` | addSwitch | MANUAL | `ScrapeManual` | Settings | no description |
| `GuiScraperStart.cpp:382` | addSwitch | PADTOKEY SETTINGS | `ScrapePadToKey` | Settings | no description |
| `GuiScraperStart.cpp:413` | addInputTextConfigRow | USERNAME | `ScreenScraperUser` | Settings | plain |
| `GuiScraperStart.cpp:414` | addInputTextConfigRow | PASSWORD | `ScreenScraperPass` | Settings | password |
| `GuiScraperStart.cpp:419` | addInputTextConfigRow | DEVELOPER ID | `ScreenScraperDevId` | Settings | plain |
| `GuiScraperStart.cpp:420` | addInputTextConfigRow | DEVELOPER PASSWORD | `ScreenScraperDevPass` | Settings | password |
| `GuiScraperStart.cpp:424` | addInputTextConfigRow | CLIENT ID | `IGDBClientID` | Settings | plain |
| `GuiScraperStart.cpp:425` | addInputTextConfigRow | CLIENT SECRET | `IGDBSecret` | Settings | password |
| `GuiSettings.cpp:401` | addWithDescription | <title> | `-` | - | GuiSettings comp form: multiLine = true |
| `GuiSettings.cpp:428` | addWithDescription | <title> | `-` | - | GuiSettings comp form: multiLine = true |

calls 50: addInputTextConfigRow 15, addInputTextRow 1, addOptionList 3, addSwitch 23, addWithDescription 8
