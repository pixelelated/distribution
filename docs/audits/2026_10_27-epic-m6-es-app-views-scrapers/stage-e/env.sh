# T32 (#679) stage E: the paths every stream's command uses. Source it, then run.
export D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-app-views-scrapers-679
export W=/home/max/Development/emulationstation-next.worktrees/m6-es-app-views-scrapers-679
export A=$D/docs/audits/2026_10_27-epic-m6-es-app-views-scrapers
export P=/workspace/tmp/m6-t32/pin
export RAPIDJSON_INCLUDE_DIR=/workspace/tmp/m6-t32/rj/rapidjson-1.1.0/include
export PUGIXML_INCLUDE_DIR=/workspace/cache/rocknix-sources/emulationstation/emulationstation-16dbac5211eea7e70db7394372033be2be7df829/external
export CPATH=$PUGIXML_INCLUDE_DIR/pugixml/src
export TMPDIR=/workspace/tmp/m6-t32/tmp
# The stand-in syntax check over every .cpp a stream may edit.
SRCS="es-app/src/scrapers/ThreadedScraper.cpp es-app/src/scrapers/Scraper.cpp es-app/src/scrapers/IGDBScraper.cpp es-app/src/scrapers/HfsDBScraper.cpp es-app/src/scrapers/GamesDBJSONScraper.cpp es-app/src/scrapers/GamesDBJSONScraperResources.cpp es-app/src/scrapers/ArcadeDBJSONScraper.cpp es-app/src/views/gamelist/GameNameFormatter.cpp es-app/src/views/gamelist/ISimpleGameListView.cpp es-app/src/views/gamelist/GridGameListView.cpp es-app/src/views/gamelist/DetailedContainer.cpp es-app/src/views/SystemView.cpp es-app/src/services/HttpServerThread.cpp"
