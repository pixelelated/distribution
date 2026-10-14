# #567 exact source inventory

Repository: `pixelelated/emulationstation`; baseline accepted ES c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78; frame-qualified a7dcdbb38009d8d2a81c7c2b4bc1d8c2d0d38a20; final 3178b832b8d134198b2b4eede4f725d4ed283f8c. These git object bytes are copied under `es-source/` and hashed in this packet.

| Surface | Baseline / final behavior and exact source |
| --- | --- |
| Entry | `GuiMenu.cpp:5756` in both baseline and final: `UPDATE GAMELISTS`, direct `addEntry` with no subtitle/help argument; callback `updateGameLists(window)`. The collection-settings entry shares the same function. |
| Before action, baseline | c8dc `GuiMenu.cpp:8467`: `REALLY UPDATE GAMELISTS?`, `YES`, `NO`. There is no advance offline-achievement explanation in this confirmation. |
| Before action, final | 3178 `GuiMenu.cpp:8527–8544`: retains the question/buttons and prefixes `THIS ALSO CHECKS NEW GAMES FOR OFFLINE ACHIEVEMENTS. AN INTERNET CONNECTION IS NEEDED TO DOWNLOAD THEIR ACHIEVEMENT DATA.` plus a blank line when ROCKNIX, backend availability, offline toggle and startup indexing are true. No connectivity probe or account lookup is added to the UI path. |
| Busy guards | `GuiMenu.cpp:8503/8512`: `SCRAPER IS RUNNING. DO YOU WANT TO STOP IT?` / `GAME HASHING IS RUNNING. DO YOU WANT TO STOP IT?`, original YES/NO. These precede the changed confirmation. |
| Reload progress | Final `ViewController.cpp:1440`: `Loading...`; existing reload helpers also use `Loading gamelists` at1290/1313 and `Loading theme` at1276. These are after accepting the action, so they do not fill the advance-explanation gap. |
| Index progress/completion | Final `ThreadedHasher.cpp:129/131`: `SEARCHING RETROACHIEVEMENTS` / `SEARCHING NETPLAY GAMES`; line146: `INDEXING COMPLETED. UPDATE GAMELISTS TO APPLY CHANGES.` when work exists. Progress is not a promise of offline-cache success. |
| Downstream branches | ThreadedHasher lines57–119 handles absent/failed hash library and returns without a card/thread for zero work; lines149–159 trigger after-index top-up only when identified, non-cancelled work exists. The existing offline card is delegated to `ProxyCards::indexRanOffline`; this review does not invent a new card or claim all downstream cards were freshly reviewed. |
| API path | `GuiMenu.cpp:8519–8524`: `confirm=false` reloads immediately. Later TLS/API receipts do not display the changed confirmation. |

The complete 1,628-byte `GuiMenu::updateGameLists` function is byte-identical between a7dc and3178, SHA256 `7a5da62b2c172a4577afa86a13ebaad24826b1a05e254f48b807085b1c581f43`. The exact notice English and French msgid/msgstr entries are also byte-identical (see `notice-source-continuity.json`). Other edits elsewhere in these files are not silently declared equivalent.

Existing canonical reference: distribution proof829b `docs/es-menu-map.md:770–788`, linking the source/component and installed frame index. The source proposal states that no conflict-wizard IA change is involved. No product source or canonical document was edited by this review.
