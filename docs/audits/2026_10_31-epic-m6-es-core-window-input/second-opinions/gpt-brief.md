# Independent review: M6 T35, EmulationStation's window, input and the rest of es-core (#682)

You are the independent reviewer for one slice of a code audit. You come from another lab than the first reader (Claude Opus 5.5). The subject is **the 96 paths of `es-core/**` outside the components** at the pin `16dbac5211eea7e70db7394372033be2be7df829`: 22,575 lines, 13 added or modified by the fork and 83 carried from ROCKNIX. The packet below carries:
- the 13 fork-added and fork-modified files whole, line-numbered at the pin;
- of the 83 upstream-carried files, only the line ranges the first reader cites, each with 8 lines of context, line-numbered;
- the first reader's `02`, `03`, `04` and `05` whole;
- the brief's § 4, the seven questions.

Every excerpt is hashed in `packet-manifest.json`. Neighbouring files (`utils/FileSystemUtil.cpp`, `utils/Platform.cpp`, the components, es-app's `main.cpp`) are not in the packet; the first reader cites their lines. Judge those claims as citations, or say you cannot tell.

**If you need other ranges to judge a claim, name them by file and line range at the end of your reply, under `## Sections I need`.** No second packet will be sent in this cycle; name them so the record shows what was missing.

**Answer these first, each with the lines you read:**
1. **PL-01, the watchers' lock** (`watchers/WatchersManager.cpp:159-203`, `:64-104`, `:126-157`). Is `mWatchersLock` held across every `check()`, and do the entry points named wait for it? Is the order list-then-observers, and can an observer's callback re-enter a locked entry point (a deadlock)?
2. **PL-02, the toast queue's order** (`Window.cpp:324-351`, `:1152-1175`). Does the queue drain newest first, and does the fix the first reader proposes (pop the front, reverse the re-queue loop) keep a toast returned under a new card in its place?
3. **PL-03, the script quoting** (`Scripting.cpp:88-149`). Which characters in an argument reach the shell unquoted at the pin? Is single-quoting every argument (with `'` escaped) sufficient for `system()` and `/bin/sh -c`?
4. **PL-04, the cache after `save_file`** (`InputManager.cpp:889-905`, `:1179-1284`). Is the second-pad overwrite reachable as described, given the cited cache lines?
5. **PL-05 and PL-06, the screensaver and the teardown** (`Window.cpp:777-792`, `:1091-1138`, `:188-207`, `:49-63`, `:1236-1260`). Is the window's half of #1305 as stated? Can a card alive at `deinit` be drawn again at the next `init()`?

**Then grade every punch item PL-01 to PL-24 in `05`.** One line each:
- `confirmed`, `confirmed with narrowing`, `refuted`, or `cannot tell from the packet`;
- why, and the line;
- the severity, if you would change it.

**Add any defect the first reader missed, as G-n**, with its lines. Be concrete and cite lines. Do not restate the packet.

---
# T35 (#682) packet: EmulationStation's window, input and the rest of es-core at the pin 16dbac5211eea7e70db7394372033be2be7df829


## CMakeLists.txt (whole, fork-modified, at the pin)

```text
    1  project("core")
    2  
    3  set(CORE_HEADERS	
    4  	${CMAKE_CURRENT_SOURCE_DIR}/src/AsyncHandle.h
    5  	${CMAKE_CURRENT_SOURCE_DIR}/src/AudioManager.h
    6      ${CMAKE_CURRENT_SOURCE_DIR}/src/FavoriteMusicManager.h
    7  	${CMAKE_CURRENT_SOURCE_DIR}/src/BindingManager.h
    8  	${CMAKE_CURRENT_SOURCE_DIR}/src/CECInput.h
    9  	${CMAKE_CURRENT_SOURCE_DIR}/src/GuiComponent.h
   10  	${CMAKE_CURRENT_SOURCE_DIR}/src/HelpStyle.h
   11  	${CMAKE_CURRENT_SOURCE_DIR}/src/HttpReq.h
   12  	${CMAKE_CURRENT_SOURCE_DIR}/src/ImageIO.h
   13  	${CMAKE_CURRENT_SOURCE_DIR}/src/InputConfig.h
   14  	${CMAKE_CURRENT_SOURCE_DIR}/src/InputManager.h
   15  	${CMAKE_CURRENT_SOURCE_DIR}/src/GunManager.h	
   16  	${CMAKE_CURRENT_SOURCE_DIR}/src/Log.h
   17  	${CMAKE_CURRENT_SOURCE_DIR}/src/LogPolicy.h
   18  	${CMAKE_CURRENT_SOURCE_DIR}/src/MameNames.h
   19  	${CMAKE_CURRENT_SOURCE_DIR}/src/gettext.h # batocera
   20  	${CMAKE_CURRENT_SOURCE_DIR}/src/LocaleES.h # batocera
   21      ${CMAKE_CURRENT_SOURCE_DIR}/src/SystemConf.h # batocera	
   22  	${CMAKE_CURRENT_SOURCE_DIR}/src/PowerSaver.h
   23  	${CMAKE_CURRENT_SOURCE_DIR}/src/Settings.h
   24  	${CMAKE_CURRENT_SOURCE_DIR}/src/Sound.h
   25  	${CMAKE_CURRENT_SOURCE_DIR}/src/Splash.h
   26  	${CMAKE_CURRENT_SOURCE_DIR}/src/ThemeData.h
   27  	${CMAKE_CURRENT_SOURCE_DIR}/src/ThemeVariables.h	
   28  	${CMAKE_CURRENT_SOURCE_DIR}/src/VolumeControl.h
   29  	${CMAKE_CURRENT_SOURCE_DIR}/src/Window.h
   30  	${CMAKE_CURRENT_SOURCE_DIR}/src/MultiStateInput.h
   31  	${CMAKE_CURRENT_SOURCE_DIR}/src/TextToSpeech.h
   32  	${CMAKE_CURRENT_SOURCE_DIR}/src/Paths.h
   33  
   34  	# Animations
   35  	${CMAKE_CURRENT_SOURCE_DIR}/src/animations/Animation.h
   36  	${CMAKE_CURRENT_SOURCE_DIR}/src/animations/AnimationController.h
   37  	${CMAKE_CURRENT_SOURCE_DIR}/src/animations/LambdaAnimation.h
   38  
   39  	# Playlists
   40  	${CMAKE_CURRENT_SOURCE_DIR}/src/playlists/AnimatedGifPlaylist.h
   41  	${CMAKE_CURRENT_SOURCE_DIR}/src/playlists/M3uPlaylist.h
   42  
   43  	# Theme animations
   44  	${CMAKE_CURRENT_SOURCE_DIR}/src/anim/ThemeAnimation.h	
   45  	${CMAKE_CURRENT_SOURCE_DIR}/src/anim/ThemeStoryboard.h	
   46  	${CMAKE_CURRENT_SOURCE_DIR}/src/anim/StoryboardAnimator.h
   47  	
   48  	# GuiComponents
   49  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/AnimatedImageComponent.h
   50      ${CMAKE_CURRENT_SOURCE_DIR}/src/components/AsyncNotificationComponent.h
   51  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/BatteryIndicatorComponent.h	
   52  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/BatteryIconComponent.h	
   53  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/BatteryTextComponent.h
   54  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/NetworkIconComponent.h	
   55  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/PostProcessShaderComponent.h
   56  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/StackPanelComponent.h
   57  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/BusyComponent.h
   58  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ButtonComponent.h
   59  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ClockComponent.h
   60  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ControllerActivityComponent.h
   61  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/IExternalActivity.h	
   62  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ComponentGrid.h
   63  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ComponentList.h
   64  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/DateTimeComponent.h
   65  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/DateTimeEditComponent.h
   66  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/HelpComponent.h
   67  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/GridTileComponent.h
   68  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/IList.h
   69  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ImageComponent.h
   70  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ImageGridComponent.h
   71  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/MenuComponent.h
   72  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/NinePatchComponent.h
   73  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/OptionListComponent.h
   74  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ScrollableContainer.h
   75  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/SliderComponent.h
   76  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/RatingComponent.h
   77  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/RectangleComponent.h
   78  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/SwitchComponent.h
   79  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/TextComponent.h
   80  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/TextEditComponent.h
   81  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/VideoComponent.h
   82  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/VideoPlayerComponent.h
   83  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/VideoVlcComponent.h
   84  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/VolumeInfoComponent.h
   85  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/MultiLineMenuEntry.h
   86  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ScrollbarComponent.h	
   87  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ComponentTab.h
   88  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/WebImageComponent.h
   89  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/TextListComponent.h
   90  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/CarouselComponent.h
   91  
   92  	# Guis
   93  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiDetectDevice.h
   94  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiInputConfig.h
   95  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiMsgBox.h
   96          ${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiInfoPopup.h # batocera
   97  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiTextEditPopup.h
   98  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiTextEditPopupKeyboard.h # batocera
   99  
  100  	# Math
  101  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Misc.h
  102  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Transform4x4f.h
  103  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Vector2f.h
  104  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Vector2i.h
  105  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Vector3f.h
  106  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Vector4f.h
  107  
  108  	# Renderers
  109  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer.h
  110  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GL21.h
  111  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES10.h
  112  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/GlExtensions.h	
  113  
  114  	# Resources
  115  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/Font.h
  116  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/ResourceManager.h
  117  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/TextureResource.h
  118  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/TextureData.h
  119  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/TextureDataManager.h
  120  
  121  	# Utils
  122  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/AtomicFileUtil.h
  123  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/FileSystemUtil.h
  124  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/StringUtil.h
  125  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/StringListLock.h
  126  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/TimeUtil.h
  127  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/TimeText.h
  128  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/OfflineProxyUrl.h
  129  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/ThreadPool.h
  130  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/Platform.h
  131  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/zip_file.hpp
  132  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/ZipFile.h
  133  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/md5.h
  134  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/MathExpr.h
  135  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/Delegate.h
  136  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/Randomizer.h
  137  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/VectorEx.h
  138  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/HtmlColor.h
  139  
  140  	# Watchers
  141  	${CMAKE_CURRENT_SOURCE_DIR}/src/watchers/WatchersManager.h
  142  	${CMAKE_CURRENT_SOURCE_DIR}/src/watchers/BatteryLevelWatcher.h
  143  	${CMAKE_CURRENT_SOURCE_DIR}/src/watchers/NetworkStateWatcher.h
  144  )
  145  
  146  set(CORE_SOURCES	
  147  	${CMAKE_CURRENT_SOURCE_DIR}/src/AudioManager.cpp
  148      ${CMAKE_CURRENT_SOURCE_DIR}/src/FavoriteMusicManager.cpp
  149  	${CMAKE_CURRENT_SOURCE_DIR}/src/BindingManager.cpp	
  150  	${CMAKE_CURRENT_SOURCE_DIR}/src/CECInput.cpp
  151  	${CMAKE_CURRENT_SOURCE_DIR}/src/GuiComponent.cpp
  152  	${CMAKE_CURRENT_SOURCE_DIR}/src/HelpStyle.cpp
  153  	${CMAKE_CURRENT_SOURCE_DIR}/src/HttpReq.cpp
  154  	${CMAKE_CURRENT_SOURCE_DIR}/src/ImageIO.cpp
  155  	${CMAKE_CURRENT_SOURCE_DIR}/src/InputConfig.cpp
  156  	${CMAKE_CURRENT_SOURCE_DIR}/src/InputManager.cpp
  157  	${CMAKE_CURRENT_SOURCE_DIR}/src/GunManager.cpp
  158  	${CMAKE_CURRENT_SOURCE_DIR}/src/Log.cpp
  159  	${CMAKE_CURRENT_SOURCE_DIR}/src/MameNames.cpp
  160  	${CMAKE_CURRENT_SOURCE_DIR}/src/LocaleES.cpp # batocera	
  161  	${CMAKE_CURRENT_SOURCE_DIR}/src/PowerSaver.cpp
  162  	${CMAKE_CURRENT_SOURCE_DIR}/src/Scripting.cpp
  163  	${CMAKE_CURRENT_SOURCE_DIR}/src/Settings.cpp
  164  	${CMAKE_CURRENT_SOURCE_DIR}/src/Sound.cpp
  165  	${CMAKE_CURRENT_SOURCE_DIR}/src/Splash.cpp
  166  	${CMAKE_CURRENT_SOURCE_DIR}/src/ThemeData.cpp
  167  	${CMAKE_CURRENT_SOURCE_DIR}/src/ThemeVariables.cpp
  168  	${CMAKE_CURRENT_SOURCE_DIR}/src/VolumeControl.cpp
  169  	${CMAKE_CURRENT_SOURCE_DIR}/src/Window.cpp
  170  	${CMAKE_CURRENT_SOURCE_DIR}/src/MultiStateInput.cpp
  171  	${CMAKE_CURRENT_SOURCE_DIR}/src/TextToSpeech.cpp
  172  	${CMAKE_CURRENT_SOURCE_DIR}/src/Paths.cpp
  173  
  174  	# Animations
  175  	${CMAKE_CURRENT_SOURCE_DIR}/src/animations/AnimationController.cpp	
  176  	
  177  	# Theme animations
  178  	${CMAKE_CURRENT_SOURCE_DIR}/src/anim/ThemeStoryboard.cpp
  179  	${CMAKE_CURRENT_SOURCE_DIR}/src/anim/StoryboardAnimator.cpp
  180  	
  181  	# Playlists
  182  	${CMAKE_CURRENT_SOURCE_DIR}/src/playlists/AnimatedGifPlaylist.cpp
  183  	${CMAKE_CURRENT_SOURCE_DIR}/src/playlists/M3uPlaylist.cpp
  184  
  185  	# GuiComponents
  186  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/AnimatedImageComponent.cpp
  187  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/AsyncNotificationComponent.cpp
  188  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/BatteryIndicatorComponent.cpp
  189  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/BatteryIconComponent.cpp
  190  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/BatteryTextComponent.cpp		
  191  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/NetworkIconComponent.cpp
  192  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/PostProcessShaderComponent.cpp
  193  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/StackPanelComponent.cpp
  194  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/BusyComponent.cpp
  195  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ButtonComponent.cpp	
  196  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ClockComponent.cpp	
  197  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ControllerActivityComponent.cpp
  198  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/IExternalActivity.cpp
  199  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ComponentGrid.cpp
  200  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ComponentList.cpp
  201  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/DateTimeComponent.cpp
  202  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/DateTimeEditComponent.cpp
  203  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/HelpComponent.cpp
  204  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/GridTileComponent.cpp
  205  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ImageComponent.cpp
  206  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/MenuComponent.cpp
  207  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/NinePatchComponent.cpp
  208  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ScrollableContainer.cpp
  209  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/SliderComponent.cpp
  210  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/RatingComponent.cpp
  211  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/RectangleComponent.cpp		
  212  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/SwitchComponent.cpp
  213  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/TextComponent.cpp
  214  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/TextEditComponent.cpp
  215  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/VideoComponent.cpp
  216  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/VideoPlayerComponent.cpp
  217  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/VideoVlcComponent.cpp
  218  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/VolumeInfoComponent.cpp
  219  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ScrollbarComponent.cpp
  220  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/MultiLineMenuEntry.cpp
  221  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/ComponentTab.cpp
  222  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/WebImageComponent.cpp	
  223  	${CMAKE_CURRENT_SOURCE_DIR}/src/components/CarouselComponent.cpp
  224  
  225  	# Guis
  226  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiDetectDevice.cpp
  227  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiInputConfig.cpp
  228  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiMsgBox.cpp
  229      ${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiInfoPopup.cpp # batocera
  230  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiTextEditPopup.cpp
  231  	${CMAKE_CURRENT_SOURCE_DIR}/src/guis/GuiTextEditPopupKeyboard.cpp # batocera
  232      ${CMAKE_CURRENT_SOURCE_DIR}/src/SystemConf.cpp # batocera
  233  
  234  	# Math
  235  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Misc.cpp
  236  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Transform4x4f.cpp
  237  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Vector2f.cpp
  238  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Vector2i.cpp
  239  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Vector3f.cpp
  240  	${CMAKE_CURRENT_SOURCE_DIR}/src/math/Vector4f.cpp
  241  
  242  	# Renderer
  243  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer.cpp
  244  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GL21.cpp
  245  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES10.cpp
  246  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/GlExtensions.cpp	
  247  	${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Shader.cpp	
  248  
  249  	# Resources
  250  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/Font.cpp
  251  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/ResourceManager.cpp
  252  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/TextureResource.cpp
  253  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/TextureData.cpp
  254  	${CMAKE_CURRENT_SOURCE_DIR}/src/resources/TextureDataManager.cpp
  255  
  256  	# Utils
  257  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/AtomicFileUtil.cpp
  258  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/FileSystemUtil.cpp
  259  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/StringUtil.cpp
  260  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/StringListLock.cpp
  261  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/TimeUtil.cpp
  262  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/TimeText.cpp
  263  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/OfflineProxyUrl.cpp
  264  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/ThreadPool.cpp	
  265  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/Platform.cpp
  266  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/MathExpr.cpp
  267  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/ZipFile.cpp
  268  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/md5.cpp
  269  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/Randomizer.cpp
  270  	${CMAKE_CURRENT_SOURCE_DIR}/src/utils/HtmlColor.cpp
  271  
  272  	# Watchers
  273  	${CMAKE_CURRENT_SOURCE_DIR}/src/watchers/WatchersManager.cpp
  274  	${CMAKE_CURRENT_SOURCE_DIR}/src/watchers/BatteryLevelWatcher.cpp
  275  	${CMAKE_CURRENT_SOURCE_DIR}/src/watchers/NetworkStateWatcher.cpp
  276  )
  277  
  278  if(${GLSystem} MATCHES "OpenGL ES 3.0")
  279  	LIST(APPEND CORE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES30.h)
  280  	LIST(APPEND CORE_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES30.cpp)
  281  else()
  282  	LIST(APPEND CORE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES20.h)
  283  	LIST(APPEND CORE_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/renderers/Renderer_GLES20.cpp)
  284  endif()
  285  
  286  # Keep Directory structure in Visual Studio
  287  if(MSVC)
  288  	file(
  289  		 GLOB_RECURSE source_list RELATIVE
  290  		 "${CMAKE_CURRENT_SOURCE_DIR}"
  291  		 *.cpp *.c
  292  		)
  293  	foreach(source IN LISTS source_list)
  294  		get_filename_component(source_path "${source}" PATH)
  295  		string(REPLACE "/" "\\" source_path_msvc "${source_path}")
  296  		string(REPLACE "src" "" source_path_final "${source_path_msvc}")
  297  		source_group("${source_path_final}" FILES "${source}")
  298  	endforeach()  	
  299  endif()
  300  
  301  include_directories(${COMMON_INCLUDE_DIRS})
  302  add_library(es-core STATIC ${CORE_SOURCES} ${CORE_HEADERS})
  303  target_link_libraries(es-core ${COMMON_LIBRARIES})
```

## src/AudioManager.cpp `:1-11` (an excerpt, upstream-carried, at the pin)

```text
    1  #include "FavoriteMusicManager.h"
    2  #include "AudioManager.h"
    3  
    4  #include "Log.h"
    5  #include "Settings.h"
    6  #include "Sound.h"
    7  #include <SDL.h>
    8  #include "utils/FileSystemUtil.h"
    9  #include "utils/StringUtil.h"
   10  #include "utils/Randomizer.h"
   11  #include "SystemConf.h"
```

## src/AudioManager.cpp `:14-30` (an excerpt, upstream-carried, at the pin)

```text
   14  #include "id3v2lib/include/id3v2lib.h"
   15  
   16  #include <fstream>
   17  #include <sstream>
   18  #include <vector>
   19  #include <string>
   20  #include <algorithm>
   21  
   22  #ifdef WIN32
   23  #include <time.h>
   24  #else
   25  #include <unistd.h>
   26  #endif
   27  
   28  // batocera
   29  // Size of last played music history as a percentage of file total
   30  #define LAST_PLAYED_SIZE 0.4
```

## src/AudioManager.cpp `:531-547` (an excerpt, upstream-carried, at the pin)

```text
  531  				title_break = 20;
  532  				break;
  533  			default:
  534  				LOG(LogError) << "Error AudioManager unexpected case while loading mofile " << song;
  535  				setSongName(Utils::FileSystem::getStem(song.c_str()));				
  536  				return;
  537  		}
  538  
  539  		FILE* file = fopen(song.c_str(), "r");
  540  		if (file != NULL)
  541  		{
  542  			if (fseek(file, title_offset, SEEK_SET) < 0)
  543  				LOG(LogError) << "Error AudioManager seeking " << song;
  544  			else if (fread(&info, sizeof(info), 1, file) != 1)
  545  				LOG(LogError) << "Error AudioManager reading " << song;
  546  			else  
  547  			{
```

## src/AudioManager.cpp `:602-618` (an excerpt, upstream-carried, at the pin)

```text
  602  		char title[30];
  603  		char artist[30];
  604  		char album[30];
  605  		char year[4];
  606  		char comment[30];
  607  		unsigned char genre;
  608  	} info;
  609  
  610  	FILE* file = fopen(song.c_str(), "r");
  611  	if (file != NULL)
  612  	{
  613  		if (fseek(file, -128, SEEK_END) < 0)
  614  			LOG(LogError) << "Error AudioManager seeking " << song;
  615  		else if (fread(&info, sizeof(info), 1, file) != 1)
  616  			LOG(LogError) << "Error AudioManager reading " << song;
  617  		else if (strncmp(info.tag, "TAG", 3) == 0) 
  618  		{
```

## src/BindingManager.cpp `:1-10` (an excerpt, upstream-carried, at the pin)

```text
    1  #include "BindingManager.h"
    2  #include "utils/StringUtil.h"
    3  #include "LocaleES.h"
    4  #include <time.h>
    5  
    6  #include "components/TextComponent.h"
    7  #include "components/ImageComponent.h"
    8  #include "components/VideoComponent.h"
    9  #include "components/StackPanelComponent.h"
   10  
```

## src/BindingManager.cpp `:128-158` (an excerpt, upstream-carried, at the pin)

```text
  128  		switch (value.type)
  129  		{
  130  		case BindablePropertyType::String:
  131  		case BindablePropertyType::Path:
  132  			dataAsString = value.s;
  133  			dataAsEvaluable = "\"" + Utils::String::replace(value.s, "\"", "") + "\""; // Should be managed differenty
  134  			break;
  135  		case BindablePropertyType::Bool:
  136  			dataAsString = value.b ? _("YES") : _("NO");
  137  			dataAsEvaluable = value.b ? "1" : "0";
  138  			break;
  139  		case BindablePropertyType::Int:
  140  			dataAsString = std::to_string(value.i);
  141  			dataAsEvaluable = dataAsString;
  142  			break;
  143  		case BindablePropertyType::Float:
  144  			dataAsString = std::to_string(value.f);
  145  			dataAsEvaluable = dataAsString;
  146  			break;
  147  		}
  148  
  149  		if (showDefaultText && value.type != BindablePropertyType::Path)
  150  			dataAsString = dataAsString.empty() ? _("Unknown") : dataAsString == "0" ? _("None") : dataAsString;
  151  
  152  		xp = Utils::String::replace(xp, "{" + typeName + ":" + name + "}", dataAsString);
  153  		evaluableExpression = Utils::String::replace(evaluableExpression, "{" + typeName + ":" + name + "}", dataAsEvaluable);
  154  	}
  155  }
  156  
  157  std::string BindingManager::updateBoundExpression(std::string& xp, IBindable* bindable, bool showDefaultText)
  158  {
```

## src/CECInput.cpp `:1-31` (an excerpt, upstream-carried, at the pin)

```text
    1  #include "CECInput.h"
    2  
    3  #ifdef HAVE_LIBCEC
    4  #include "Log.h"
    5  #include <SDL_events.h>
    6  #include <iostream> // bad bad cecloader
    7  #include <libcec/cecloader.h>
    8  #ifdef _RPI_
    9  extern "C" {
   10  #include <interface/vmcs_host/vc_cecservice.h>
   11  #include <interface/vmcs_host/vc_tvservice.h>
   12  #include <interface/vmcs_host/vchost.h>
   13  }
   14  #endif // _RPI_
   15  #endif // HAVE_LIBCEC
   16  
   17  // hack for cec support
   18  extern int SDL_USER_CECBUTTONDOWN;
   19  extern int SDL_USER_CECBUTTONUP;
   20  
   21  CECInput* CECInput::sInstance = nullptr;
   22  
   23  #ifdef HAVE_LIBCEC
   24  static void onAlert(void* /*cbParam*/, const CEC::libcec_alert type, const CEC::libcec_parameter param)
   25  {
   26  	LOG(LogDebug) << "CECInput::onAlert type: " << CECInput::getAlertTypeString(type) << " parameter: " << (char*)(param.paramData);
   27  
   28  } // onAlert
   29  
   30  static void onCommand(void* /*cbParam*/, const CEC::cec_command* command)
   31  {
```

## src/CECInput.cpp `:45-61` (an excerpt, upstream-carried, at the pin)

```text
   45  } // onKeyPress
   46  
   47  static void onLogMessage(void* /*cbParam*/, const CEC::cec_log_message* message)
   48  {
   49  	LOG(LogDebug) << "CECInput::onLogMessage message: " << message->message;
   50  
   51  } // onLogMessage
   52  
   53  #ifdef _RPI_
   54  static void vchi_tv_and_cec_init()
   55  {
   56  	VCHI_INSTANCE_T vchi_instance;
   57  	VCHI_CONNECTION_T* vchi_connection;
   58  	vc_host_get_vchi_state(&vchi_instance, &vchi_connection);
   59  
   60  	vc_vchi_tv_init(vchi_instance, &vchi_connection, 1);
   61  	vc_vchi_cec_init(vchi_instance, &vchi_connection, 1);
```

## src/CECInput.cpp `:86-103` (an excerpt, upstream-carried, at the pin)

```text
   86  		sInstance = nullptr;
   87  	}
   88  
   89  } // deinit
   90  
   91  CECInput::CECInput() : mlibCEC(nullptr)
   92  {
   93  
   94  #ifdef HAVE_LIBCEC
   95  #ifdef _RPI_
   96  	// restart vchi tv and cec in case we just came back from another app using cec (like Kodi)
   97  	vchi_tv_and_cec_deinit();
   98  	vchi_tv_and_cec_init();
   99  #endif // _RPI_
  100  
  101  	// CEC::ICECCallbacks        callbacks;
  102  	// CEC::libcec_configuration config;
  103  
```

## src/CECInput.cpp `:146-183` (an excerpt, upstream-carried, at the pin)

```text
  146  	}
  147  #endif // HAVE_LIBCEC
  148  
  149  } // CECInput
  150  
  151  CECInput::~CECInput()
  152  {
  153  
  154  #ifdef HAVE_LIBCEC
  155  	if(mlibCEC)
  156  	{
  157  		mlibCEC->Close();
  158  		UnloadLibCec(mlibCEC);
  159  		mlibCEC = nullptr;
  160  	}
  161  
  162  #ifdef _RPI_
  163  	// deinit vchi tv and cec in case we are going to launch another app using cec (like Kodi)
  164  	vchi_tv_and_cec_deinit();
  165  #endif // _RPI_
  166  #endif // HAVE_LIBCEC
  167  
  168  } // ~CECInput
  169  
  170  std::string CECInput::getAlertTypeString(const unsigned int _type)
  171  {
  172  	switch(_type)
  173  	{
  174  
  175  #ifdef HAVE_LIBCEC
  176  		case CEC::CEC_ALERT_SERVICE_DEVICE:         { return "Service-Device";         } break;
  177  		case CEC::CEC_ALERT_CONNECTION_LOST:        { return "Connection-Lost";        } break;
  178  		case CEC::CEC_ALERT_PERMISSION_ERROR:       { return "Permission-Error";       } break;
  179  		case CEC::CEC_ALERT_PORT_BUSY:              { return "Port-Busy";              } break;
  180  		case CEC::CEC_ALERT_PHYSICAL_ADDRESS_ERROR: { return "Physical-Address-Error"; } break;
  181  		case CEC::CEC_ALERT_TV_POLL_FAILED:         { return "TV-Poll-Failed";         } break;
  182  #else // HAVE_LIBCEC
  183  		case 0:
```

## src/CECInput.cpp `:188-204` (an excerpt, upstream-carried, at the pin)

```text
  188  
  189  } // getAlertTypeString
  190  
  191  std::string CECInput::getOpCodeString(const unsigned int _opCode)
  192  {
  193  	switch(_opCode)
  194  	{
  195  
  196  #ifdef HAVE_LIBCEC
  197  		case CEC::CEC_OPCODE_ACTIVE_SOURCE:                 { return "Active-Source";                 } break;
  198  		case CEC::CEC_OPCODE_IMAGE_VIEW_ON:                 { return "Image-View-On";                 } break;
  199  		case CEC::CEC_OPCODE_TEXT_VIEW_ON:                  { return "Text-View-On";                  } break;
  200  		case CEC::CEC_OPCODE_INACTIVE_SOURCE:               { return "Inactive-Source";               } break;
  201  		case CEC::CEC_OPCODE_REQUEST_ACTIVE_SOURCE:         { return "Request-Active-Source";         } break;
  202  		case CEC::CEC_OPCODE_ROUTING_CHANGE:                { return "Routing-Change";                } break;
  203  		case CEC::CEC_OPCODE_ROUTING_INFORMATION:           { return "Routing-Information";           } break;
  204  		case CEC::CEC_OPCODE_SET_STREAM_PATH:               { return "Set-Stream-Path";               } break;
```

## src/CECInput.cpp `:273-289` (an excerpt, upstream-carried, at the pin)

```text
  273  
  274  } // getOpCodeString
  275  
  276  std::string CECInput::getKeyCodeString(const unsigned int _keyCode)
  277  {
  278  	switch(_keyCode)
  279  	{
  280  
  281  #ifdef HAVE_LIBCEC
  282  		case CEC::CEC_USER_CONTROL_CODE_SELECT:                      { return "Select";                      } break;
  283  		case CEC::CEC_USER_CONTROL_CODE_UP:                          { return "Up";                          } break;
  284  		case CEC::CEC_USER_CONTROL_CODE_DOWN:                        { return "Down";                        } break;
  285  		case CEC::CEC_USER_CONTROL_CODE_LEFT:                        { return "Left";                        } break;
  286  		case CEC::CEC_USER_CONTROL_CODE_RIGHT:                       { return "Right";                       } break;
  287  		case CEC::CEC_USER_CONTROL_CODE_RIGHT_UP:                    { return "Right-Up";                    } break;
  288  		case CEC::CEC_USER_CONTROL_CODE_RIGHT_DOWN:                  { return "Right-Down";                  } break;
  289  		case CEC::CEC_USER_CONTROL_CODE_LEFT_UP:                     { return "Left-Up";                     } break;
```

## src/CECInput.h `:1-32` (an excerpt, upstream-carried, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_CECINPUT_H
    3  #define ES_CORE_CECINPUT_H
    4  
    5  #include <string>
    6  
    7  #ifdef HAVE_LIBCEC
    8  #include <libcec/cec.h>
    9  #endif
   10  
   11  namespace CEC { class ICECAdapter; }
   12  
   13  class CECInput
   14  {
   15  public:
   16  
   17  	static void        init              ();
   18  	static void        deinit            ();
   19  	static std::string getAlertTypeString(const unsigned int _type);
   20  	static std::string getOpCodeString   (const unsigned int _opCode);
   21  	static std::string getKeyCodeString  (const unsigned int _keyCode);
   22  
   23  private:
   24  #ifdef HAVE_LIBCEC
   25  	CEC::ICECCallbacks        callbacks;
   26  	CEC::libcec_configuration config;
   27  #endif
   28  
   29  	 CECInput();
   30  	~CECInput();
   31  
   32  	static CECInput*  sInstance;
```

## src/FavoriteMusicManager.cpp `:26-42` (an excerpt, upstream-carried, at the pin)

```text
   26  
   27      return Paths::getMusicPath();
   28  }
   29  
   30  
   31  std::vector<std::pair<std::string, std::string>> FavoriteMusicManager::loadFavoriteSongs(const std::string& favoritesFile)
   32  {
   33      std::vector<std::pair<std::string, std::string>> favorites;
   34      std::list<std::string> lines = Utils::FileSystem::readAllLines(favoritesFile);
   35      for (const auto& line : lines)
   36      {
   37          if (line.empty())
   38              continue;
   39          size_t pos = line.find(';');
   40          if (pos != std::string::npos)
   41          {
   42              std::string path = line.substr(0, pos);
```

## src/FavoriteMusicManager.cpp `:63-79` (an excerpt, upstream-carried, at the pin)

```text
   63      }
   64      infile.close();
   65  
   66      if (alreadyExists)
   67      {
   68          return false;
   69      }
   70  
   71      std::ofstream ofs(favoritesFile, std::ios::app);
   72      if (!ofs.is_open())
   73      {
   74          return false;
   75      }
   76  
   77      ofs << path << ";" << name << "\n";
   78      ofs.close();
   79  
```

## src/FavoriteMusicManager.cpp `:81-127` (an excerpt, upstream-carried, at the pin)

```text
   81  }
   82  
   83  bool FavoriteMusicManager::removeSongFromFavorites(const std::string& path, const std::string& name, Window* window)
   84  {
   85      std::string favoritesFile = getFavoriteMusicFilePath();
   86      if (!Utils::FileSystem::exists(favoritesFile))
   87          return false;
   88  
   89      auto lines = Utils::FileSystem::readAllLines(favoritesFile);
   90      bool found = false;
   91      for (auto it = lines.begin(); it != lines.end(); ++it)
   92      {
   93          if (*it == path + ";" + name)
   94          {
   95              lines.erase(it);
   96              found = true;
   97              break;
   98          }
   99      }
  100  
  101      if (!found)
  102          return false;
  103  
  104      if (lines.empty())
  105      {
  106          Utils::FileSystem::removeFile(favoritesFile);
  107          if (Settings::getInstance()->getBool("audio.useFavoriteMusic"))
  108          {
  109              Settings::getInstance()->setBool("audio.useFavoriteMusic", false);
  110              Settings::getInstance()->saveFile();
  111          }
  112      }
  113      else
  114      {
  115          std::ofstream ofs(favoritesFile, std::ios::trunc);
  116          if (!ofs.is_open())
  117          {
  118              return false;
  119          }
  120  
  121          for (auto& l : lines)
  122              ofs << l << "\n";
  123          ofs.close();
  124      }
  125  
  126      return true;
  127  }
```

## src/GuiComponent.cpp `:22-38` (an excerpt, upstream-carried, at the pin)

```text
   22  	mSize(Vector2f::Zero()), mTransform(Transform4x4f::Identity()), mVisible(true), mShowing(false), mPadding(Vector4f(0, 0, 0, 0)), mClipChildren(false),
   23  	mExtraType(ExtraType::BUILTIN), mStoryboardAnimator(nullptr), mScreenOffset(0.0f), mTransformDirty(true), mIsMouseOver(false), mMousePressed(false), mChildZIndexDirty(false)
   24  {
   25  	mClipRect = Vector4f();
   26  }
   27  
   28  GuiComponent::~GuiComponent()
   29  {
   30  	mWindow->removeGui(this);
   31  
   32  	cancelAllAnimations();
   33  
   34  	if (mStoryboardAnimator != nullptr)
   35  	{
   36  		delete mStoryboardAnimator;
   37  		mStoryboardAnimator = nullptr;
   38  	}
```

## src/GunManager.cpp (whole, fork-modified, at the pin)

```text
    1  #include "GunManager.h"
    2  #include "Log.h"
    3  #include "utils/Platform.h"
    4  #include "Window.h"
    5  #include <SDL.h>
    6  #include <iostream>
    7  #include <assert.h>
    8  #include <algorithm>
    9  #include "utils/StringUtil.h"
   10  #include "LocaleES.h"
   11  #include "renderers/Renderer.h"
   12  #include "InputManager.h"
   13  #include <vector>
   14  
   15  #ifdef HAVE_UDEV
   16  #include <poll.h>
   17  #include <fcntl.h>
   18  #include <sys/ioctl.h>
   19  #include <linux/input.h>
   20  #include <unistd.h>
   21  #define test_bit(array, bit)    (array[bit/8] & (1<<(bit%8)))
   22  #elif WIN32
   23  
   24  #include <set>
   25  #include <SDL_syswm.h>
   26  #include <hidsdi.h>
   27  #pragma comment(lib, "Hid.lib")
   28  
   29  #define WIIMOTE_GUN "Wiimote Gun"
   30  
   31  // Uncomment FORCE_REPLACEMOUSE to force using the mouse with GunManager ( for testing purpose )
   32  // #define FORCE_REPLACEMOUSE 1
   33  
   34  // Warning : never call SDL_SetRelativeMouseMode(true) with Windows or RAWINPUT will be managed by SDL
   35  
   36  enum class LightGunType
   37  {
   38  	Mouse,
   39  	SindenLightgun,
   40  	Gun4Ir,
   41  	MayFlashWiimote,
   42  	RetroShooter,
   43  	Blamcon,
   44  	Aimtrak,
   45  	AELightgun,
   46  	Xgunner,
   47  	VirtualHID
   48  };
   49  
   50  class RawInputManager
   51  {
   52  public:
   53  	static bool sWiimoteGunRunning;
   54  
   55  	static LightGunType getLightGunType(const std::string& name)
   56  	{
   57  		std::string sindenDeviceIds[] = { "VID_16C0&PID_0F01", "VID_16C0&PID_0F02", "VID_16C0&PID_0F38", "VID_16C0&PID_0F39" };
   58  		for (auto id : sindenDeviceIds)
   59  			if (name.find(id) != std::string::npos)
   60  				return LightGunType::SindenLightgun;
   61  
   62  		std::string gun4irDeviceIds[] = { "VID_2341&PID_8042", "VID_2341&PID_8043", "VID_2341&PID_8044", "VID_2341&PID_8045", "VID_2341&PID_8046", "VID_2341&PID_8047" };
   63  		for (auto id : gun4irDeviceIds)
   64  			if (name.find(id) != std::string::npos)
   65  				return LightGunType::Gun4Ir;
   66  
   67  		std::string mayFlashWiimoteIds[] = { "VID_0079&PID_1802" };  // Mayflash Wiimote, using mode 1
   68  		for (auto id : mayFlashWiimoteIds)
   69  			if (name.find(id) != std::string::npos)
   70  				return LightGunType::MayFlashWiimote;
   71  
   72  		std::string rsDeviceIds[] = { "VID_0483&PID_5750", "VID_0483&PID_5751", "VID_0483&PID_5752", "VID_0483&PID_5753" };
   73  		for (auto id : rsDeviceIds)
   74  			if (name.find(id) != std::string::npos)
   75  				return LightGunType::RetroShooter;
   76  
   77  		std::string blamconDeviceIds[] = { "VID_3673&PID_0100", "VID_3673&PID_0101", "VID_3673&PID_0102", "VID_3673&PID_0103", "VID_3673&PID_0104" };
   78  		for (auto id : blamconDeviceIds)
   79  			if (name.find(id) != std::string::npos)
   80  				return LightGunType::Blamcon;
   81  
   82  		std::string aimtrakDeviceIds[] = { "VID_D209&PID_1601", "VID_D209&PID_1602", "VID_D209&PID_1603" };
   83  		for (auto id : aimtrakDeviceIds)
   84  			if (name.find(id) != std::string::npos)
   85  				return LightGunType::Aimtrak;
   86  
   87  		std::string xgunnerDeviceIds[] = { "VID_1209&PID_0001", "VID_1209&PID_0002", "VID_1209&PID_0003", "VID_1209&PID_0004" };
   88  		for (auto id : xgunnerDeviceIds)
   89  			if (name.find(id) != std::string::npos)
   90  				return LightGunType::Xgunner;
   91  
   92  		std::string aeDeviceIds[] = { "VID_2341&PID_8037", "VID_2341&PID_8038" };
   93  		for (auto id : aeDeviceIds)
   94  			if (name.find(id) != std::string::npos)
   95  				return LightGunType::AELightgun;
   96  
   97  		if (sWiimoteGunRunning && name.find("vmulti") != std::string::npos)
   98  			return LightGunType::VirtualHID;
   99  
  100  		return LightGunType::Mouse;
  101  	}
  102  
  103  	static LightGunType getLightGunType(HANDLE hDevice)
  104  	{
  105  		return getLightGunType(GetRawInputDevicePath(hDevice));
  106  	}
  107  
  108  	static std::string GetRawInputDevicePath(HANDLE hDevice)
  109  	{
  110  		UINT bufferSize = 0;
  111  
  112  		// Required size. With pData == nullptr, the API returns 0 on success.
  113  		if (GetRawInputDeviceInfoA(hDevice, RIDI_DEVICENAME, nullptr, &bufferSize) != 0)
  114  			return "";
  115  
  116  		// Safeguard: a device path is never 4 KB.
  117  		if (bufferSize == 0 || bufferSize > 4096)
  118  			return "";
  119  
  120  		std::vector<char> buffer(bufferSize + 1, '\0');
  121  
  122  		if (GetRawInputDeviceInfoA(hDevice, RIDI_DEVICENAME, buffer.data(), &bufferSize) == (UINT)-1)
  123  			return "";
  124  
  125  		buffer[buffer.size() - 1] = '\0';   // guaranteed termination
  126  		return std::string(buffer.data());
  127  	}
  128  
  129  	static std::string GetRawInputDeviceName(HANDLE hDevice)
  130  	{
  131  		std::string path = GetRawInputDevicePath(hDevice);
  132  		if (path.empty())
  133  			return "";
  134  
  135  		std::string ret;
  136  
  137  		HANDLE hhid = CreateFileA(path.c_str(), 0,
  138  			FILE_SHARE_READ | FILE_SHARE_WRITE, nullptr,
  139  			OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
  140  
  141  		if (hhid != INVALID_HANDLE_VALUE)
  142  		{
  143  			wchar_t buf[256] = { 0 };
  144  
  145  			// HidD_GetProductString attend une longueur en OCTETS, pas en caractères.
  146  			if (HidD_GetProductString(hhid, &buf[0], sizeof(buf) - sizeof(wchar_t)))
  147  			{
  148  				buf[255] = L'\0';
  149  				ret = Utils::String::convertFromWideString(buf);
  150  			}
  151  
  152  			CloseHandle(hhid);
  153  		}
  154  
  155  		return ret;
  156  	}
  157  };
  158  bool RawInputManager::sWiimoteGunRunning = false;
  159  #endif
  160  
  161  GunManager::GunManager()
  162  {
  163  #ifdef HAVE_UDEV
  164  	udev = udev_new();
  165  	if (udev != NULL)
  166  	{
  167  		udev_monitor = udev_monitor_new_from_netlink(udev, "udev");
  168  		if (udev_monitor)
  169  		{
  170  			udev_monitor_filter_add_match_subsystem_devtype(udev_monitor, "input", NULL);
  171  			udev_monitor_enable_receiving(udev_monitor);
  172  		}
  173  	}
  174  	udev_initial_gunsList();
  175  #endif
  176  }
  177  
  178  GunManager::~GunManager()
  179  {
  180  #ifdef HAVE_UDEV
  181  	if (udev != NULL)
  182  	{
  183  		// close guns
  184  		for (auto gun : mGuns) 
  185  		{
  186  		  udev_closeGun(gun);
  187  		  delete gun;
  188  		}
  189  
  190  		mGuns.clear();
  191  
  192  		if (udev_monitor)
  193  			udev_monitor_unref(udev_monitor);
  194  		
  195  		udev_unref(udev);
  196  	}
  197  #elif WIN32
  198  	enableRawInputCapture(false);
  199  	for (auto gun : mGuns)
  200  		delete gun;
  201  
  202  	mGuns.clear();
  203  #endif
  204  }
  205  
  206  int GunManager::readGunEvents(Gun* gun)
  207  {
  208  #ifdef HAVE_UDEV
  209  	int len;
  210  	struct input_event input_events[64];
  211  
  212  	while ((len = read(gun->fd, input_events, sizeof(input_events))) > 0) {
  213  	  for (unsigned i = 0; i<len/sizeof(input_event); i++) {
  214  			if (input_events[i].type == EV_KEY) {
  215  				//printf("key, code=%i, value=%i\n", input_events[i].code, input_events[i].value);
  216  				gun->m_lastTick = SDL_GetTicks();
  217  
  218  				switch (input_events[i].code) 
  219  				{
  220  				case KEY_CONFIG:
  221  					if (input_events[i].value == 1) {
  222  						// starting calibration
  223  						gun->mIsCalibrating = true;
  224  						return 1;
  225  					}
  226  					else {
  227  						// stopping calibration
  228  						gun->mIsCalibrating = false;
  229  						return 2;
  230  					}
  231  					break;
  232  				case BTN_LEFT:
  233  					gun->mLButtonDown = (input_events[i].value != 0);
  234  					break;
  235  				case BTN_RIGHT:
  236  					gun->mRButtonDown = (input_events[i].value != 0);
  237  					break;
  238  				case BTN_MIDDLE:
  239  					gun->mStartButtonDown = (input_events[i].value != 0);
  240  					break;
  241  				case BTN_1:
  242  					gun->mSelectButtonDown = (input_events[i].value != 0);
  243  					break;
  244  				case BTN_5:
  245  					gun->mDPadUpButtonDown = (input_events[i].value != 0);
  246  					break;
  247  				case BTN_6:
  248  					gun->mDPadDownButtonDown = (input_events[i].value != 0);
  249  					break;
  250  				case BTN_7:
  251  					gun->mDPadLeftButtonDown = (input_events[i].value != 0);
  252  					break;
  253  				case BTN_8:
  254  					gun->mDPadRightButtonDown = (input_events[i].value != 0);
  255  					break;
  256  				}
  257  			}
  258  		}
  259  	}
  260  #endif
  261  
  262  	return 0;
  263  }
  264  
  265  class Stabilizer
  266  {
  267  public:
  268  	Stabilizer()
  269  	{
  270  		mWindowSize = 6;
  271  		mBuffer.resize(mWindowSize);
  272  	}
  273  
  274  	void add(float x, float y)
  275  	{
  276  		mBuffer.push_back({ x, y });
  277  		if (mBuffer.size() > mWindowSize)
  278  			mBuffer.pop_front();
  279  	}
  280  
  281  	std::pair<float, float> getStabilizedPosition()
  282  	{
  283  		if (mBuffer.empty())
  284  			return { 0.0f, 0.0f };
  285  
  286  		float sumX = 0.0f, sumY = 0.0f;
  287  		for (const auto& pos : mBuffer)
  288  		{
  289  			sumX += pos.first;
  290  			sumY += pos.second;
  291  		}
  292  
  293  		return { sumX / (float)mBuffer.size(), sumY / (float)mBuffer.size() };
  294  	}
  295  
  296  private:
  297  	int mWindowSize;
  298  	std::deque<std::pair<float, float>> mBuffer;
  299  };
  300  
  301  Stabilizer* Gun::getStabilizer()
  302  {
  303  	if (m_pStabilizer == nullptr)
  304  		m_pStabilizer = new Stabilizer();
  305  
  306  	return m_pStabilizer;
  307  }
  308  
  309  bool Gun::isLastTickElapsed()
  310  {
  311  #ifdef HAVE_UDEV
  312  	if (mIsCalibrating)
  313  		return false;
  314  #endif
  315  
  316  	return m_lastTick == 0 || (SDL_GetTicks() - m_lastTick) > 5000;
  317  }
  318  
  319  #if WIN32
  320  
  321  bool GunManager::mMessageHookRegistered = false;
  322  
  323  
  324  
  325  void GunManager::enableRawInputCapture(bool enable)
  326  {
  327  	if (mMessageHookRegistered == enable)
  328  		return;
  329  
  330  	// Register to receive raw input from mice
  331  	RAWINPUTDEVICE rid[1];
  332  	rid[0].usUsagePage = HID_USAGE_PAGE_GENERIC;
  333  	rid[0].usUsage = HID_USAGE_GENERIC_MOUSE;
  334  	rid[0].dwFlags = enable ? 0 : RIDEV_REMOVE;
  335  	rid[0].hwndTarget = NULL;
  336  
  337  	if (enable)
  338  	{
  339  		SDL_SysWMinfo wmInfo;
  340  		SDL_VERSION(&wmInfo.version);
  341  		if (SDL_GetWindowWMInfo(Renderer::getSDLWindow(), &wmInfo))
  342  		{
  343  			rid[0].dwFlags = RIDEV_INPUTSINK;
  344  			rid[0].hwndTarget = (HWND)wmInfo.info.win.window;
  345  		}
  346  	}
  347  
  348  	RegisterRawInputDevices(rid, 1, sizeof(RAWINPUTDEVICE));
  349  
  350  	if (enable)
  351  		SDL_SetWindowsMessageHook(&GunManager::WindowsMessageHook, this);
  352  	else 
  353  		SDL_SetWindowsMessageHook(nullptr, nullptr);
  354  
  355  	mMessageHookRegistered = enable;
  356  }
  357  
  358  static bool _isScreenPointOverWindow(HWND hWnd, int x, int y)
  359  {
  360  	POINT cursorPos{ x, y };
  361  	if (x == -9999 && y == -9999)
  362  		GetCursorPos(&cursorPos);
  363  
  364  	// Get the client rectangle of the window
  365  	RECT rc;
  366  	GetClientRect(hWnd, &rc);
  367  	ClientToScreen(hWnd, reinterpret_cast<POINT*>(&rc.left)); // convert top-left
  368  	ClientToScreen(hWnd, reinterpret_cast<POINT*>(&rc.right));
  369  
  370  	// Check if the cursor is within the client area
  371  	return PtInRect(&rc, cursorPos);
  372  }
  373  
  374  void GunManager::WindowsMessageHook(void* userdata, void* hWnd, unsigned int message, Uint64 wParam, Sint64 lParam)
  375  {
  376  	if (message != WM_INPUT || userdata == nullptr)
  377  		return;
  378  
  379  	RAWINPUT rawInput;
  380  	UINT size = sizeof(RAWINPUT);
  381  	UINT ret = GetRawInputData(reinterpret_cast<HRAWINPUT>(lParam), RID_INPUT, &rawInput, &size, sizeof(RAWINPUTHEADER));
  382  	if (ret == (UINT)-1)
  383  		return;
  384  
  385  	if (rawInput.header.dwType != RIM_TYPEMOUSE)
  386  		return;
  387  
  388  	GunManager* mgr = (GunManager*)userdata;
  389  
  390  	auto path = RawInputManager::GetRawInputDevicePath(rawInput.header.hDevice);	
  391  	auto it = std::find_if(mgr->mGuns.cbegin(), mgr->mGuns.cend(), [path](Gun* pGun) { return pGun->mPath == path; });
  392  	if (it == mgr->mGuns.cend())
  393  		return;
  394  
  395  	Gun* gun = *it;
  396  
  397  	if (gun->m_isMouse)
  398  	{
  399  		auto itFirstMouse = std::find_if(mgr->mGuns.cbegin(), mgr->mGuns.cend(), [path](Gun* pGun) { return pGun->m_isMouse; });
  400  		if (itFirstMouse != mgr->mGuns.cend())
  401  			gun = *itFirstMouse;
  402  	}
  403  
  404  	// Handle mouse input
  405  	RAWMOUSE& rawMouse = rawInput.data.mouse;
  406  
  407  	RECT rect;
  408  	::GetWindowRect((HWND)hWnd, &rect);
  409  	RECT rectClient;
  410  	::GetClientRect((HWND)hWnd, &rectClient);
  411  
  412  	if (gun->m_isMouse)
  413  	{
  414  		POINT cursorPos;
  415  		GetCursorPos(&cursorPos);		
  416  		ScreenToClient((HWND)hWnd, &cursorPos);
  417  
  418  		if (gun->m_internalX != cursorPos.x || gun->m_internalY != cursorPos.y)
  419  		{
  420  			gun->m_internalX = cursorPos.x;
  421  			gun->m_internalY = cursorPos.y;
  422  			gun->m_lastTick = SDL_GetTicks();
  423  		}
  424  	}
  425  	else if (rawMouse.lLastX != 0 && rawMouse.lLastY != 0)
  426  	{
  427  		if ((rawMouse.usFlags & 0x01) == MOUSE_MOVE_ABSOLUTE)
  428  		{
  429  			bool isVirtualDesktop = (rawMouse.usFlags & MOUSE_VIRTUAL_DESKTOP) == MOUSE_VIRTUAL_DESKTOP;
  430  
  431  			int width = GetSystemMetrics(isVirtualDesktop ? SM_CXVIRTUALSCREEN : SM_CXSCREEN);
  432  			int height = GetSystemMetrics(isVirtualDesktop ? SM_CYVIRTUALSCREEN : SM_CYSCREEN);
  433  
  434  			POINT cursorPos;
  435  			cursorPos.x = int((rawMouse.lLastX / 65535.0f) * width);
  436  			cursorPos.y = int((rawMouse.lLastY / 65535.0f) * height);
  437  			ScreenToClient((HWND)hWnd, &cursorPos);
  438  
  439  			gun->getStabilizer()->add(cursorPos.x, cursorPos.y);
  440  
  441  			auto stabilizedPos = gun->getStabilizer()->getStabilizedPosition();
  442  
  443  			if (gun->m_internalX != stabilizedPos.first || gun->m_internalY != stabilizedPos.second)
  444  			{
  445  				gun->m_internalX = stabilizedPos.first;
  446  				gun->m_internalY = stabilizedPos.second;
  447  				gun->m_lastTick = SDL_GetTicks();
  448  			}
  449  		}
  450  		else if ((rawMouse.usFlags & 0x01) == MOUSE_MOVE_RELATIVE)
  451  		{
  452  			gun->m_internalX = Math::clamp(gun->mX + rawMouse.lLastX, -1, rectClient.right - rectClient.left + 1);
  453  			gun->m_internalY = Math::clamp(gun->mY + rawMouse.lLastY, -1, rectClient.bottom - rectClient.top + 1);
  454  			gun->m_lastTick = SDL_GetTicks();
  455  		}
  456  	}
  457  
  458  	// https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawmouse
  459  	if (rawMouse.usButtonFlags)
  460  	{
  461  		bool clickEnabled = true;
  462  
  463  		if (GetActiveWindow() != hWnd)
  464  			clickEnabled = false;
  465  		else
  466  		{
  467  			POINT ptScreen{ gun->m_internalX, gun->m_internalY };
  468  			ClientToScreen((HWND)hWnd, &ptScreen);
  469  			clickEnabled = _isScreenPointOverWindow((HWND)hWnd, ptScreen.x, ptScreen.y) && ::WindowFromPoint(ptScreen) == (HWND)hWnd;
  470  		}
  471  
  472  		int	buttonState = gun->m_internalButtonState;
  473  
  474  		// Check the button flags
  475  		if (rawMouse.usButtonFlags & RI_MOUSE_LEFT_BUTTON_DOWN && clickEnabled)
  476  			buttonState |= 1;
  477  
  478  		if (rawMouse.usButtonFlags & RI_MOUSE_LEFT_BUTTON_UP)
  479  			buttonState &= ~1;
  480  
  481  		if (rawMouse.usButtonFlags & RI_MOUSE_RIGHT_BUTTON_DOWN && clickEnabled)
  482  			buttonState |= 2;
  483  
  484  		if (rawMouse.usButtonFlags & RI_MOUSE_RIGHT_BUTTON_UP)
  485  			buttonState &= ~2;
  486  
  487  		if (rawMouse.usButtonFlags & RI_MOUSE_MIDDLE_BUTTON_DOWN && clickEnabled)
  488  			buttonState |= 4;
  489  
  490  		if (rawMouse.usButtonFlags & RI_MOUSE_MIDDLE_BUTTON_UP)
  491  			buttonState &= ~4;
  492  
  493  		if (rawMouse.usButtonFlags & RI_MOUSE_BUTTON_4_DOWN && clickEnabled)
  494  			buttonState |= 8;
  495  
  496  		if (rawMouse.usButtonFlags & RI_MOUSE_BUTTON_4_UP)
  497  			buttonState &= ~8;
  498  
  499  		if (rawMouse.usButtonFlags & RI_MOUSE_BUTTON_5_DOWN && clickEnabled)
  500  			buttonState |= 16;
  501  
  502  		if (rawMouse.usButtonFlags & RI_MOUSE_BUTTON_5_UP)
  503  			buttonState &= ~16;
  504  
  505  		if (buttonState != gun->m_internalButtonState)
  506  		{
  507  			gun->m_internalButtonState = buttonState;
  508  			gun->m_lastTick = SDL_GetTicks();
  509  		}
  510  	}
  511  }
  512  #endif
  513  
  514  void GunManager::updateGuns(Window* window)
  515  {	
  516  #ifdef HAVE_UDEV
  517  	const char* val_gun;
  518  	const char* val_gunborder;
  519  	bool bGunborder;
  520  	const char* action;
  521  
  522  	while (udev_monitor && udev_input_poll_hotplug_available(udev_monitor)) 
  523  	{
  524  		struct udev_device *dev = udev_monitor_receive_device(udev_monitor);
  525  		bool dev_handled = false;
  526  
  527  		if (dev != NULL) 
  528  		{
  529  			val_gun = udev_device_get_property_value(dev, "ID_INPUT_GUN"); // ID_INPUT_GUN and ID_INPUT_MOUSE for some tests
  530  			val_gunborder = udev_device_get_property_value(dev, "ID_INPUT_GUN_NEED_BORDERS");
  531  			bGunborder = false;
  532  
  533  			if (val_gunborder != NULL && strncmp(val_gunborder, "1", 1) == 0)
  534  				bGunborder = true;
  535  
  536  			action = udev_device_get_action(dev);
  537  
  538  			if (action != NULL && val_gun != NULL && strncmp(val_gun, "1", 1) == 0)
  539  			{
  540  				if (strncmp(action, "add", 3) == 0)
  541  				{
  542  				  if (udev_addGun(dev, window, bGunborder))
  543  						dev_handled = true;
  544  				}
  545  				else if (strncmp(action, "remove", 6) == 0)
  546  				{
  547  					if (udev_removeGun(dev, window)) 
  548  						dev_handled = true;
  549  				}
  550  			}
  551  
  552  			if (!dev_handled) 
  553  				udev_device_unref(dev); // not handled, clean it
  554  		}
  555  	}
  556  #elif WIN32
  557  
  558  	static int updateGunCheck = 0;
  559  
  560  	// Check gun changed every 10 times it's called
  561  	if (updateGunCheck++ > 10)
  562  	{
  563  		updateGunCheck = 0;
  564  
  565  		std::vector<RAWINPUTDEVICELIST> deviceList;
  566  		UINT numDevices = 0;
  567  
  568  		for (int attempt = 0; attempt < 3; attempt++)
  569  		{
  570  			UINT count = 0;
  571  			if (GetRawInputDeviceList(nullptr, &count, sizeof(RAWINPUTDEVICELIST)) == (UINT)-1 || count == 0)
  572  				return;
  573  
  574  			deviceList.resize(count);
  575  
  576  			UINT ret = GetRawInputDeviceList(deviceList.data(), &count, sizeof(RAWINPUTDEVICELIST));
  577  			if (ret != (UINT)-1)
  578  			{
  579  				numDevices = ret;   // number actually written, not the allocated size
  580  				break;
  581  			}
  582  
  583  			deviceList.clear();
  584  
  585  			if (GetLastError() != ERROR_INSUFFICIENT_BUFFER)
  586  				return;             // real failure, no need to retry
  587  		}
  588  
  589  		if (numDevices == 0)
  590  			return;                 // unstable list: will try again in 11 frames
  591  
  592  		// Only one GetRawInputDeviceInfo call per device and per pass.
  593  		std::vector<std::string> devicePaths(numDevices);
  594  		for (UINT i = 0; i < numDevices; i++)
  595  			devicePaths[i] = RawInputManager::GetRawInputDevicePath(deviceList[i].hDevice);
  596  
  597  		// Diagnostic : trace rawinput list when it changes.
  598  		{
  599  			static std::set<std::string> lastKnownRawPaths;
  600  			std::set<std::string> currentRawPaths;
  601  
  602  			for (UINT i = 0; i < numDevices; i++)
  603  				currentRawPaths.insert(std::to_string(deviceList[i].dwType) + "|" + devicePaths[i]);
  604  
  605  			if (currentRawPaths != lastKnownRawPaths)
  606  			{
  607  				LOG(LogInfo) << "[RawInput] device list changed (" << numDevices << " device(s))";
  608  				for (const auto& p : currentRawPaths)
  609  					LOG(LogInfo) << "[RawInput]   " << p;
  610  
  611  				lastKnownRawPaths = currentRawPaths;
  612  			}
  613  		}
  614  
  615  		Window* notifyWindow = mInitialScan ? nullptr : window;
  616  
  617  		std::set<std::string> knownPaths;
  618  
  619  		// WiimoteGun must be detected BEFORE classifying devices:
  620  		// it allows interpreting "vmulti" as a lightgun.
  621  		bool hasWiimoteGun = false;
  622  
  623  		HWND hWndWiimoteGun = FindWindow("WiimoteGun", NULL);
  624  		if (hWndWiimoteGun)
  625  		{
  626  			int mode = (int)GetProp(hWndWiimoteGun, "mode");
  627  			hasWiimoteGun = (mode == 1);
  628  		}
  629  
  630  		RawInputManager::sWiimoteGunRunning = hasWiimoteGun;
  631  
  632  		bool hasPhysicalGuns = false;
  633  
  634  #if FORCE_REPLACEMOUSE
  635  		hasPhysicalGuns = true;
  636  #else
  637  		for (UINT i = 0; i < numDevices; i++)
  638  		{
  639  			if (deviceList[i].dwType != RIM_TYPEMOUSE &&
  640  				RawInputManager::getLightGunType(devicePaths[i]) != LightGunType::Mouse)
  641  			{
  642  				hasPhysicalGuns = true;
  643  				break;
  644  			}
  645  		}
  646  #endif
  647  
  648  		if (hasPhysicalGuns || hasWiimoteGun)
  649  		{
  650  			for (UINT i = 0; i < numDevices; i++)
  651  			{
  652  				if (deviceList[i].dwType != RIM_TYPEMOUSE)
  653  					continue;
  654  
  655  				HANDLE hDevice = deviceList[i].hDevice;
  656  				const std::string& devicePath = devicePaths[i];
  657  
  658  				if (devicePath.empty())
  659  					continue;
  660  
  661  				auto gunType = RawInputManager::getLightGunType(devicePath);
  662  				if (hasWiimoteGun && gunType == LightGunType::Mouse)
  663  					continue;
  664  
  665  				knownPaths.insert(devicePath);
  666  
  667  				if (std::any_of(mGuns.cbegin(), mGuns.cend(), [&devicePath](Gun* pGun) { return pGun->mPath == devicePath; }))
  668  					continue;
  669  
  670  				Gun* newgun = new Gun();
  671  				newgun->mIndex = mGuns.size();
  672  				newgun->mName = RawInputManager::GetRawInputDeviceName(hDevice);
  673  				newgun->mPath = devicePath;
  674  				newgun->mNeedBorders = gunType == LightGunType::SindenLightgun;
  675  				newgun->m_isMouse = gunType == LightGunType::Mouse;
  676  				newgun->m_lastTick = SDL_GetTicks();
  677  
  678  				if (newgun->m_isMouse)
  679  				{
  680  					int x, y;
  681  					auto buttons = SDL_GetMouseState(&x, &y);
  682  					newgun->mX = newgun->m_internalX = x;
  683  					newgun->mY = newgun->m_internalY = y;
  684  				}
  685  				else if (notifyWindow != NULL && !newgun->mName.empty() && Settings::getInstance()->getBool("ShowGunsNotifications"))
  686  					notifyWindow->displayNotificationMessage(_U("\uF05B ") + Utils::String::format(_("%s connected").c_str(), Utils::String::trim(newgun->mName).c_str()));
  687  
  688  				mGuns.push_back(newgun);
  689  			}
  690  		}
  691  
  692  		// Remove guns
  693  		auto iter = mGuns.cbegin();
  694  		while (iter != mGuns.cend())
  695  		{
  696  			Gun* gun = *iter;
  697  
  698  			if (gun->mName == WIIMOTE_GUN || knownPaths.find(gun->mPath) != knownPaths.cend())
  699  				iter++;
  700  			else
  701  			{
  702  				if (notifyWindow != NULL && !gun->m_isMouse && Settings::getInstance()->getBool("ShowGunsNotifications"))
  703  					notifyWindow->displayNotificationMessage(_U("\uF05B ") + Utils::String::format(_("%s disconnected").c_str(), Utils::String::trim(gun->mName).c_str()));
  704  
  705  				LOG(LogInfo) << "Gun removed found at " << gun->mPath;
  706  
  707  				iter = mGuns.erase(iter);
  708  				delete gun;
  709  				renumberGuns();
  710  			}
  711  		}
  712  
  713  		if (hasWiimoteGun && !std::any_of(mGuns.cbegin(), mGuns.cend(), [](Gun* pGun) { return pGun->mName == WIIMOTE_GUN; }))
  714  		{
  715  			Gun* newgun = new Gun();
  716  			newgun->mIndex = mGuns.size();
  717  			newgun->mName = WIIMOTE_GUN;
  718  			newgun->m_isMouse = false;
  719  			newgun->m_lastTick = SDL_GetTicks();
  720  
  721  			mGuns.push_back(newgun);
  722  
  723  			if (notifyWindow != NULL && Settings::getInstance()->getBool("ShowGunsNotifications"))
  724  				notifyWindow->displayNotificationMessage(_U("\uF05B ") + Utils::String::format(_("%s connected").c_str(), Utils::String::trim(newgun->mName).c_str()));
  725  		}
  726  		else if (!hasWiimoteGun && mGuns.size())
  727  		{
  728  			for (auto it = mGuns.cbegin(); it != mGuns.cend(); it++)
  729  			{
  730  				Gun* gun = *it;
  731  				if (gun->mName == WIIMOTE_GUN)
  732  				{
  733  					if (notifyWindow != NULL && Settings::getInstance()->getBool("ShowGunsNotifications"))
  734  						notifyWindow->displayNotificationMessage(_U("\uF05B ") + Utils::String::format(_("%s disconnected").c_str(), Utils::String::trim(gun->mName).c_str()));
  735  
  736  					mGuns.erase(it);
  737  					delete gun;
  738  
  739  					renumberGuns();
  740  					break;
  741  				}
  742  			}
  743  		}
  744  
  745  		if (hasPhysicalGuns && !mMessageHookRegistered)
  746  		{
  747  			SDL_ShowCursor(0);
  748  			enableRawInputCapture(true);			
  749  		}
  750  		else if (!hasPhysicalGuns && mMessageHookRegistered)
  751  			enableRawInputCapture(false);
  752  
  753  		mInitialScan = false;
  754  	}
  755  #endif
  756  
  757  	float gunMoveTolerence = Settings::getInstance()->getFloat("GunMoveTolerence") / 100.0;
  758  
  759  	int gunEvent = 0;
  760  	for (Gun* gun : mGuns)
  761  	{
  762  		GunData* data = gun;
  763  		GunData oldGun = *data;
  764  
  765  		int evt = readGunEvents(gun);
  766  		if (evt != 0)
  767  			gunEvent = evt;
  768  
  769  		updateGunPosition(gun);
  770  		
  771  		if (fabsf(oldGun.mX - gun->mX) > gunMoveTolerence || fabsf(oldGun.mY - gun->mY) > gunMoveTolerence)		
  772  			window->processMouseMove(gun->x(), gun->y(), true);
  773  		
  774  #ifdef HAVE_UDEV
  775  		// gun pads
  776  		if(gun->isDPadUpButtonDown() != oldGun.isDPadUpButtonDown())
  777  		  window->input(InputManager::getInstance()->getInputConfigByDevice(DEVICE_GUN), Input(DEVICE_GUN, TYPE_BUTTON, BTN_5, gun->isDPadUpButtonDown() ? 1 : 0, true));
  778  
  779  		if(gun->isDPadDownButtonDown() != oldGun.isDPadDownButtonDown())
  780  		  window->input(InputManager::getInstance()->getInputConfigByDevice(DEVICE_GUN), Input(DEVICE_GUN, TYPE_BUTTON, BTN_6, gun->isDPadDownButtonDown() ? 1 : 0, true));
  781  
  782  		if(gun->isDPadLeftButtonDown() != oldGun.isDPadLeftButtonDown())
  783  		  window->input(InputManager::getInstance()->getInputConfigByDevice(DEVICE_GUN), Input(DEVICE_GUN, TYPE_BUTTON, BTN_7, gun->isDPadLeftButtonDown() ? 1 : 0, true));
  784  
  785  		if(gun->isDPadRightButtonDown() != oldGun.isDPadRightButtonDown())
  786  		  window->input(InputManager::getInstance()->getInputConfigByDevice(DEVICE_GUN), Input(DEVICE_GUN, TYPE_BUTTON, BTN_8, gun->isDPadRightButtonDown() ? 1 : 0, true));
  787  
  788  		// start / select
  789  		if(gun->isStartButtonDown() != oldGun.isStartButtonDown())
  790  		  window->input(InputManager::getInstance()->getInputConfigByDevice(DEVICE_GUN), Input(DEVICE_GUN, TYPE_BUTTON, BTN_MIDDLE, gun->isStartButtonDown() ? 1 : 0, true));
  791  
  792  		if(gun->isSelectButtonDown() != oldGun.isSelectButtonDown())
  793  		  window->input(InputManager::getInstance()->getInputConfigByDevice(DEVICE_GUN), Input(DEVICE_GUN, TYPE_BUTTON, BTN_1, gun->isSelectButtonDown() ? 1 : 0, true));
  794  #elif WIN32
  795  		// gun pads
  796  		if (gun->isLButtonDown() != oldGun.isLButtonDown())
  797  		{
  798  			if (!window->processMouseButton(1, gun->isLButtonDown(), gun->x(), gun->y()))
  799  				window->input(InputManager::getInstance()->getInputConfigByDevice(DEVICE_MOUSE), Input(DEVICE_MOUSE, TYPE_BUTTON, 1, gun->isLButtonDown() ? 1 : 0, false));
  800  		}
  801  
  802  		if (gun->isRButtonDown() != oldGun.isRButtonDown())
  803  		{
  804  			if (!window->processMouseButton(3, gun->isRButtonDown(), gun->x(), gun->y()))
  805  				window->input(InputManager::getInstance()->getInputConfigByDevice(DEVICE_MOUSE), Input(DEVICE_MOUSE, TYPE_BUTTON, 3, gun->isRButtonDown() ? 1 : 0, false));
  806  		}
  807  
  808  		if (gun->isMButtonDown() != oldGun.isMButtonDown())
  809  		{
  810  			auto config = InputManager::getInstance()->getInputConfigByDevice(DEVICE_KEYBOARD);
  811  			if (config == nullptr)
  812  				continue;
  813  
  814  			Input input;
  815  			if (config->getInputByName(BUTTON_OK, &input))
  816  				window->input(config, Input(input.device, input.type, input.id, gun->isMButtonDown() ? 1 : 0, true));
  817  		}
  818  
  819  		if (gun->isStartButtonDown() != oldGun.isStartButtonDown())
  820  		{
  821  			auto config = InputManager::getInstance()->getInputConfigByDevice(DEVICE_KEYBOARD);
  822  			if (config == nullptr)
  823  				continue;
  824  
  825  			Input input;
  826  			if (config->getInputByName("start", &input))
  827  				window->input(config, Input(input.device, input.type, input.id, gun->isStartButtonDown() ? 1 : 0, true));
  828  		}
  829  
  830  		if (gun->isSelectButtonDown() != oldGun.isSelectButtonDown())
  831  		{
  832  			auto config = InputManager::getInstance()->getInputConfigByDevice(DEVICE_KEYBOARD);
  833  			if (config == nullptr)
  834  				continue;
  835  
  836  			Input input;
  837  			if (config->getInputByName("select", &input))
  838  				window->input(config, Input(input.device, input.type, input.id, gun->isSelectButtonDown() ? 1 : 0, true));
  839  		}
  840  #endif
  841  	}
  842  
  843  	if (gunEvent == 1 || gunEvent == 2)
  844  		window->setGunCalibrationState(gunEvent == 1);
  845  }
  846  
  847  void GunManager::renumberGuns()
  848  {
  849  	// Renumber guns
  850  	int idx = 0;
  851  	for (Gun* gun : mGuns) 
  852  		gun->mIndex = idx++;	
  853  }
  854  
  855  bool GunManager::isReplacingMouse()
  856  {
  857  #if WIN32
  858  	return mGuns.size();
  859  #endif
  860  	return false;
  861  }
  862  
  863  bool GunManager::updateGunPosition(Gun* gun) 
  864  {
  865  #ifdef HAVE_UDEV
  866  	struct input_absinfo absinfo;
  867  
  868  	float x = gun->mX;
  869  	float y = gun->mY;
  870  
  871  	if (ioctl(gun->fd, EVIOCGABS(ABS_X), &absinfo) == -1) 
  872  		return false;
  873  
  874  	x = ((float)(absinfo.value - absinfo.minimum)) / ((float)(absinfo.maximum - absinfo.minimum));
  875  
  876  	if (ioctl(gun->fd, EVIOCGABS(ABS_Y), &absinfo) == -1) 
  877  		return false;
  878  
  879  	y = ((float)(absinfo.value - absinfo.minimum)) / ((float)(absinfo.maximum - absinfo.minimum));
  880  
  881  	if (x != gun->mX || y != gun->mY)
  882  	{
  883  		gun->mX = x;
  884  		gun->mY = y;
  885  		gun->m_lastTick = SDL_GetTicks();
  886  	}
  887  
  888  	return true;
  889  #endif
  890  
  891  #ifdef WIN32
  892  	if (gun->mName == WIIMOTE_GUN)
  893  	{
  894  		int x, y;
  895  		auto buttons = SDL_GetMouseState(&x, &y);
  896  
  897  		if (x != gun->mX || y != gun->mY)
  898  			gun->m_lastTick = SDL_GetTicks();
  899  
  900  		gun->mX = x;
  901  		gun->mY = y;
  902  		gun->mLButtonDown = (buttons & SDL_BUTTON_LMASK) != 0;
  903  		gun->mRButtonDown = (buttons & SDL_BUTTON_RMASK) != 0;
  904  		gun->mMButtonDown = (buttons & SDL_BUTTON_MMASK) != 0;
  905  		return true;
  906  	}
  907  
  908  	gun->mX = gun->m_internalX;
  909  	gun->mY = gun->m_internalY;
  910  	gun->mLButtonDown = (gun->m_internalButtonState & 1) == 1;
  911  	gun->mRButtonDown = (gun->m_internalButtonState & 2) == 2;
  912  	gun->mMButtonDown = (gun->m_internalButtonState & 4) == 4;
  913  	gun->mStartButtonDown = (gun->m_internalButtonState & 8) == 8;
  914  	gun->mSelectButtonDown = (gun->m_internalButtonState & 16) == 16;	
  915  #endif
  916  
  917  	return false;
  918  }
  919  
  920  #ifdef HAVE_UDEV
  921  // function from retroarch
  922  bool GunManager::udev_input_poll_hotplug_available(struct udev_monitor *dev)
  923  {
  924  	struct pollfd fds;
  925  
  926  	fds.fd = udev_monitor_get_fd(dev);
  927  	fds.events = POLLIN;
  928  	fds.revents = 0;
  929  
  930  	return (poll(&fds, 1, 0) == 1) && (fds.revents & POLLIN);
  931  }
  932  
  933  void GunManager::udev_initial_gunsList()
  934  {
  935  	struct udev_list_entry *devs = NULL;
  936  	struct udev_list_entry *item = NULL;
  937  	const char* val_gunborder;
  938  	bool bGunborder;
  939  
  940  	struct udev_enumerate *enumerate = udev_enumerate_new(udev);
  941  	if (enumerate == NULL) return;
  942  	udev_enumerate_add_match_property(enumerate, "ID_INPUT_GUN", "1");
  943  	udev_enumerate_add_match_subsystem(enumerate, "input");
  944  	udev_enumerate_scan_devices(enumerate);
  945  	devs = udev_enumerate_get_list_entry(enumerate);
  946  
  947  	for (item = devs; item; item = udev_list_entry_get_next(item)) 
  948  	{
  949  		const char         *name = udev_list_entry_get_name(item);
  950  		struct udev_device *dev = udev_device_new_from_syspath(udev, name);
  951  
  952  		val_gunborder = udev_device_get_property_value(dev, "ID_INPUT_GUN_NEED_BORDERS"); // ID_INPUT_GUN and ID_INPUT_MOUSE for some tests
  953  		bGunborder = false;
  954  
  955  		if (val_gunborder != NULL && strncmp(val_gunborder, "1", 1) == 0)
  956  		  bGunborder = true;
  957  
  958  		if (udev_addGun(dev, NULL, bGunborder) == false) udev_device_unref(dev); // unhandled device
  959  	}
  960  	udev_enumerate_unref(enumerate);
  961  }
  962  
  963  bool GunManager::udev_addGun(struct udev_device *dev, Window* window, bool needGunBorder)
  964  {
  965  	char ident[256];
  966  	const char* devnode;
  967  	unsigned char abscaps[(ABS_MAX / 8) + 1] = { '\0' };
  968  
  969  	// check that devnode is of form /dev/input/eventXX (to not include devices aliases)
  970  	devnode = udev_device_get_devnode(dev);
  971  	if (devnode == NULL) return false;
  972  	if (strncmp(devnode, "/dev/input/event", 16) != 0) return false;
  973  
  974  	int fd = open(devnode, O_RDONLY | O_NONBLOCK);
  975  	if (fd < 0) return false;
  976  
  977  	// check absolute capabilities
  978  	if (ioctl(fd, EVIOCGBIT(EV_ABS, sizeof(abscaps)), abscaps) == -1) {
  979  		close(fd);
  980  		return false;
  981  	}
  982  
  983  	// check absolute capabilities x and y
  984  	if (((test_bit(abscaps, ABS_X)) && (test_bit(abscaps, ABS_Y))) == false) {
  985  		close(fd);
  986  		return false;
  987  	}
  988  
  989  	LOG(LogInfo) << "Gun found at " << devnode;
  990  
  991  	if (ioctl(fd, EVIOCGNAME(sizeof(ident)), ident) < 0)
  992  		ident[0] = '\0';
  993  
  994  	Gun* newgun = new Gun();
  995  	newgun->mIndex = mGuns.size();
  996  	newgun->mName = std::string(ident);
  997  	newgun->devpath = devnode;
  998  	newgun->dev = dev;
  999  	newgun->fd = fd;
 1000  	newgun->mNeedBorders = needGunBorder;
 1001  	newgun->m_lastTick = SDL_GetTicks();
 1002  
 1003  	if (!newgun->mName.empty() && window != NULL && Settings::getInstance()->getBool("ShowGunsNotifications"))
 1004  		window->displayNotificationMessage(_U("\uF05B ") + Utils::String::format(_("%s connected").c_str(), Utils::String::trim(newgun->mName).c_str()));
 1005  
 1006  	mGuns.push_back(newgun);
 1007  
 1008  	return true;
 1009  }
 1010  
 1011  void GunManager::udev_closeGun(Gun* gun) {
 1012    close(gun->fd);
 1013    udev_device_unref(gun->dev);
 1014  }
 1015  
 1016  bool GunManager::udev_removeGun(struct udev_device *dev, Window* window)
 1017  {
 1018  	const char* devnode;
 1019  
 1020  	devnode = udev_device_get_devnode(dev);
 1021  	LOG(LogInfo) << "Gun removed at " << devnode;
 1022  
 1023  	if (devnode == NULL) return false;
 1024  
 1025  	for (auto iter = mGuns.begin(); iter != mGuns.end(); iter++)
 1026  	{
 1027  		if ((*iter)->devpath == devnode)
 1028  		{
 1029  			LOG(LogInfo) << "Gun removed found at " << devnode;
 1030  			if (window != NULL && Settings::getInstance()->getBool("ShowGunsNotifications"))
 1031  				window->displayNotificationMessage(_U("\uF05B ") + Utils::String::format(_("%s disconnected").c_str(), Utils::String::trim((*iter)->mName).c_str()));
 1032  
 1033  			udev_closeGun(*iter);
 1034  			delete *iter;
 1035  			mGuns.erase(iter);
 1036  
 1037  			renumberGuns();
 1038  			return true;
 1039  		}
 1040  	}
 1041  	return false;
 1042  }
 1043  float GunData::x() { return mX * Renderer::getScreenWidth(); }
 1044  float GunData::y() { return mY * Renderer::getScreenHeight(); }
 1045  #else 
 1046  float GunData::x() { return mX; }
 1047  float GunData::y() { return mY; }
 1048  #endif
 1049  
 1050  Gun::~Gun()
 1051  {
 1052  	if (m_pStabilizer != nullptr)
 1053  	{
 1054  		delete m_pStabilizer;
 1055  		m_pStabilizer = nullptr;
 1056  	}
 1057  }
```

## src/InputConfig.cpp (whole, fork-modified, at the pin)

```text
    1  #include "InputConfig.h"
    2  
    3  #include "Log.h"
    4  #include <pugixml/src/pugixml.hpp>
    5  #include "Settings.h"
    6  #include "utils/StringUtil.h"
    7  
    8  #ifdef HAVE_UDEV
    9  #include <libudev.h>
   10  #include "utils/FileSystemUtil.h"
   11  #endif
   12  
   13  
   14  //some util functions
   15  std::string inputTypeToString(InputType type)
   16  {
   17  	switch(type)
   18  	{
   19  	case TYPE_AXIS:
   20  		return "axis";
   21  	case TYPE_BUTTON:
   22  		return "button";
   23  	case TYPE_HAT:
   24  		return "hat";
   25  	case TYPE_KEY:
   26  		return "key";
   27  	case TYPE_CEC_BUTTON:
   28  		return "cec-button";
   29  	default:
   30  		return "error";
   31  	}
   32  }
   33  
   34  InputType stringToInputType(const std::string& type)
   35  {
   36  	if(type == "axis")
   37  		return TYPE_AXIS;
   38  	if(type == "button")
   39  		return TYPE_BUTTON;
   40  	if(type == "hat")
   41  		return TYPE_HAT;
   42  	if(type == "key")
   43  		return TYPE_KEY;
   44  	if(type == "cec-button")
   45  		return TYPE_CEC_BUTTON;
   46  	return TYPE_COUNT;
   47  }
   48  
   49  
   50  std::string toLower(std::string str)
   51  {
   52  	for(unsigned int i = 0; i < str.length(); i++)
   53  	{
   54  		str[i] = (char)tolower(str[i]);
   55  	}
   56  
   57  	return str;
   58  }
   59  
   60  #ifdef HAVE_UDEV
   61  
   62  std::string getDeviceParentSyspath(const std::string& path) {
   63    struct udev *udev;
   64    struct udev_list_entry *devs = NULL;
   65    struct udev_list_entry *item = NULL;
   66    std::string res;
   67  
   68    udev = udev_new();
   69    if (udev != NULL)
   70      {
   71        struct udev_enumerate *enumerate = udev_enumerate_new(udev);
   72        if (enumerate == NULL) { udev_unref(udev); return res; }
   73        udev_enumerate_add_match_subsystem(enumerate, "input");
   74        udev_enumerate_scan_devices(enumerate);
   75        devs = udev_enumerate_get_list_entry(enumerate);
   76  
   77        for (item = devs; item; item = udev_list_entry_get_next(item)) {
   78  	  const char *name = udev_list_entry_get_name(item);
   79  	  if(Utils::FileSystem::getFileName(name) == Utils::FileSystem::getFileName(path)) {
   80  
   81  	    struct udev_device* ud = udev_device_new_from_syspath(udev, name);
   82  	    if(ud != NULL) {
   83  	      // have a bluetooth parent ?
   84  	      udev_device* bt_parent = udev_device_get_parent_with_subsystem_devtype(ud, "bluetooth", NULL);
   85  	      if(bt_parent != NULL) {
   86  		const char *bt_parent_sysname = udev_device_get_syspath(bt_parent);
   87  		res = bt_parent_sysname;
   88  		udev_device_unref(ud);
   89  		udev_enumerate_unref(enumerate);
   90  		udev_unref(udev);
   91  		return res;
   92  	      }
   93  
   94  	      // have a usb parent ?
   95  	      udev_device* usb_parent = udev_device_get_parent_with_subsystem_devtype(ud, "usb", NULL);
   96  	      if(usb_parent != NULL) {
   97  		const char *usb_parent_sysname = udev_device_get_syspath(usb_parent);
   98  		res = usb_parent_sysname;
   99  		udev_device_unref(ud);
  100  		udev_enumerate_unref(enumerate);
  101  		udev_unref(udev);
  102  		return res;
  103  	      }
  104  	      udev_device_unref(ud);
  105  	    }
  106  
  107  	    // fallback (should not happen) ; return the device path
  108  	    res = name;
  109  	    udev_enumerate_unref(enumerate);
  110  	    udev_unref(udev);
  111  	    return res;
  112  	  }
  113  	}
  114        udev_enumerate_unref(enumerate);
  115        udev_unref(udev);
  116      }
  117    return "";
  118  }
  119  
  120  #endif
  121  
  122  //end util functions
  123  
  124  InputConfig::InputConfig(int deviceId, int deviceIndex, const std::string& deviceName, const std::string& deviceGUID, int deviceNbButtons, int deviceNbHats, int deviceNbAxes, const std::string& devicePath) 
  125  	: mDeviceId(deviceId), mDeviceIndex(deviceIndex), mDeviceName(deviceName), mDeviceGUID(deviceGUID), mDeviceNbButtons(deviceNbButtons), mDeviceNbHats(deviceNbHats), mDeviceNbAxes(deviceNbAxes), mDevicePath(devicePath)
  126  {
  127  	mBatteryLevel = -1;
  128  	mIsWheel = false;
  129  	mDeviceParentSysPath = "";
  130  #ifdef HAVE_UDEV
  131  	mIsWheel = isWheel(devicePath);
  132  	mDeviceParentSysPath = getDeviceParentSyspath(devicePath);
  133  	LOG(LogInfo) << "INFO: device syspath for " << devicePath << " is " << mDeviceParentSysPath << "\n";
  134  #endif
  135  }
  136  
  137  #ifdef HAVE_UDEV
  138  bool InputConfig::isWheel(const std::string path) {
  139  	struct udev *udev;
  140  	struct udev_list_entry *devs = NULL;
  141  	struct udev_list_entry *item = NULL;
  142  	bool res = false;
  143  
  144  	udev = udev_new();
  145  	if (udev != NULL)
  146  	  {
  147  	    struct udev_enumerate *enumerate = udev_enumerate_new(udev);
  148  	    if (enumerate == NULL) { udev_unref(udev); return false; }
  149  	    udev_enumerate_add_match_property(enumerate, "ID_INPUT_WHEEL", "1");
  150  	    udev_enumerate_add_match_subsystem(enumerate, "input");
  151  	    udev_enumerate_scan_devices(enumerate);
  152  	    devs = udev_enumerate_get_list_entry(enumerate);
  153  
  154  	    for (item = devs; item; item = udev_list_entry_get_next(item))
  155  	      {
  156  	    	const char *name = udev_list_entry_get_name(item);
  157  	    	struct udev_device *dev = udev_device_new_from_syspath(udev, name);
  158  
  159  		const char* devnode;
  160  	    	devnode = udev_device_get_devnode(dev);
  161  	    	if (devnode != NULL) {
  162  		  std::string strdevnode = devnode;
  163  		  if(strdevnode == path) {
  164  		    res = true;
  165  		  }
  166  	    	}
  167  	    	udev_device_unref(dev);
  168  	      }
  169  	    udev_enumerate_unref(enumerate);
  170  	    udev_unref(udev);
  171  	  }
  172  	return res;
  173  }
  174  #endif
  175  
  176  void InputConfig::clear()
  177  {
  178  	mNameMap.clear();
  179  }
  180  
  181  bool InputConfig::isConfigured()
  182  {
  183  	return mNameMap.size() > 0;
  184  }
  185  
  186  void InputConfig::mapInput(const std::string& name, Input input)
  187  {
  188  	mNameMap[toLower(name)] = input;
  189  }
  190  
  191  void InputConfig::unmapInput(const std::string& name)
  192  {
  193  	auto it = mNameMap.find(toLower(name));
  194  	if(it != mNameMap.cend())
  195  		mNameMap.erase(it);
  196  }
  197  
  198  bool InputConfig::getInputByName(const std::string& name, Input* result)
  199  {
  200  	auto it = mNameMap.find(toLower(name));
  201  	if(it != mNameMap.cend())
  202  	{
  203  		*result = it->second;
  204  		return true;
  205  	}
  206  
  207  	return false;
  208  }
  209  
  210  bool InputConfig::isMappedTo(const std::string& name, Input input, bool reversedAxis)
  211  {
  212  	Input comp;
  213  	if (!getInputByName(name, &comp))
  214  		return false;
  215  
  216  	if (reversedAxis)
  217  		comp.value *= -1;
  218  
  219  	if (comp.configured && comp.type == input.type && comp.id == input.id)
  220  	{
  221  		if (comp.type == TYPE_HAT)
  222  			return (input.value == 0 || input.value & comp.value);
  223  
  224  		if (comp.type == TYPE_AXIS)
  225  			return input.value == 0 || comp.value == input.value;
  226  
  227  		return true;		
  228  	}
  229  
  230  	return false;
  231  }
  232  
  233  bool InputConfig::isMappedLike(const std::string& name, Input input)
  234  {
  235  	if (name == "left")
  236  		return isMappedTo("left", input) || isMappedTo("leftanalogleft", input) || isMappedTo("rightanalogleft", input);
  237  
  238  	if (name == "right")
  239  		return isMappedTo("right", input) || isMappedTo("leftanalogright", input) || isMappedTo("rightanalogright", input);
  240  
  241  	if (name == "up")
  242  		return isMappedTo("up", input) || isMappedTo("leftanalogup", input) || isMappedTo("rightanalogup", input);
  243  
  244  	if (name == "down")
  245  		return isMappedTo("down", input) || isMappedTo("leftanalogdown", input) || isMappedTo("rightanalogdown", input);
  246  
  247  	return isMappedTo(name, input);
  248  }
  249  
  250  std::vector<std::string> InputConfig::getMappedTo(Input input)
  251  {
  252  	std::vector<std::string> maps;
  253  
  254  	typedef std::map<std::string, Input>::const_iterator it_type;
  255  	for (it_type iterator = mNameMap.cbegin(); iterator != mNameMap.cend(); iterator++)
  256  	{
  257  		Input chk = iterator->second;
  258  
  259  		if (!chk.configured)
  260  			continue;
  261  
  262  		if (chk.device == input.device && chk.type == input.type && chk.id == input.id)
  263  		{
  264  			if (chk.type == TYPE_HAT)
  265  			{
  266  				if (input.value == 0 || input.value & chk.value)
  267  					maps.push_back(iterator->first);
  268  
  269  				continue;
  270  			}
  271  
  272  			if (input.type == TYPE_AXIS)
  273  			{
  274  				if (input.value == 0 || chk.value == input.value)
  275  					maps.push_back(iterator->first);
  276  			}
  277  			else
  278  				maps.push_back(iterator->first);
  279  		}
  280  	}
  281  
  282  	return maps;
  283  }
  284  
  285  void InputConfig::loadFromXML(pugi::xml_node& node)
  286  {
  287  	clear();
  288  
  289  	for(pugi::xml_node input = node.child("input"); input; input = input.next_sibling("input"))
  290  	{
  291  		std::string name = input.attribute("name").as_string();
  292  		std::string type = input.attribute("type").as_string();
  293  		InputType typeEnum = stringToInputType(type);
  294  
  295  		if(typeEnum == TYPE_COUNT)
  296  		{
  297  			LOG(LogError) << "InputConfig load error - input of type \"" << type << "\" is invalid! Skipping input \"" << name << "\".\n";
  298  			continue;
  299  		}
  300  
  301  		int id = input.attribute("id").as_int();
  302  		int value = input.attribute("value").as_int();
  303  
  304  		if(value == 0)
  305  			LOG(LogWarning) << "WARNING: InputConfig value is 0 for " << type << " " << id << "!\n";
  306  
  307  		mNameMap[toLower(name)] = Input(mDeviceId, typeEnum, id, value, true);
  308  	}
  309  }
  310  
  311  void InputConfig::writeToXML(pugi::xml_node& parent)
  312  {
  313  	pugi::xml_node cfg = parent.append_child("inputConfig");
  314  
  315  	if(mDeviceId == DEVICE_KEYBOARD)
  316  	{
  317  		cfg.append_attribute("type") = "keyboard";
  318  		cfg.append_attribute("deviceName") = "Keyboard";
  319  	}
  320  	else if(mDeviceId == DEVICE_CEC)
  321  	{
  322  		cfg.append_attribute("type") = "cec";
  323  		cfg.append_attribute("deviceName") = "CEC";
  324  	}
  325  	else
  326  	{
  327  		cfg.append_attribute("type") = "joystick";
  328  		cfg.append_attribute("deviceName") = mDeviceName.c_str();
  329  	}
  330  
  331  	cfg.append_attribute("deviceGUID") = mDeviceGUID.c_str();
  332  
  333  	typedef std::map<std::string, Input>::const_iterator it_type;
  334  	for(it_type iterator = mNameMap.cbegin(); iterator != mNameMap.cend(); iterator++)
  335  	{
  336  		if(!iterator->second.configured)
  337  			continue;
  338  
  339  		pugi::xml_node input = cfg.append_child("input");
  340  		input.append_attribute("name") = iterator->first.c_str();
  341  		input.append_attribute("type") = inputTypeToString(iterator->second.type).c_str();
  342  		input.append_attribute("id").set_value(iterator->second.id);
  343  		input.append_attribute("value").set_value(iterator->second.value);
  344  	}
  345  }
  346  
  347  static char ABUTTON[2] = "a";
  348  static char BBUTTON[2] = "b";
  349  
  350  char* BUTTON_OK = ABUTTON;
  351  char* BUTTON_BACK = BBUTTON;
  352  
  353  std::string InputConfig::buttonLabel(const std::string& button)
  354  {
  355  #ifdef INVERTEDINPUTCONFIG
  356  	if (!Settings::getInstance()->getBool("InvertButtons"))
  357  	{
  358  		if (button == "a")
  359  			return "b";
  360  		else if (button == "b")
  361  			return "a";
  362  	}
  363  #endif
  364  
  365  	return button;
  366  }
  367  
  368  std::string InputConfig::buttonDisplayName(const std::string& button)
  369  {
  370  #ifdef INVERTEDINPUTCONFIG
  371  	if (!Settings::getInstance()->getBool("InvertButtons"))
  372  	{
  373  		return button == "a" ? "SOUTH" : button == "b" ? "EAST" : button;
  374  	}
  375  #endif
  376  
  377  	return button == "a" ? "EAST" : button == "b" ? "SOUTH" : button;
  378  }
  379  
  380  std::string InputConfig::buttonImage(const std::string& button)
  381  {
  382  #ifdef INVERTEDINPUTCONFIG
  383  	if (!Settings::getInstance()->getBool("InvertButtons"))
  384  	{
  385  		if (button == "a")
  386  			return ":/help/buttons_south.svg";		
  387  		if (button == "b")
  388  			return ":/help/buttons_east.svg";
  389  	}
  390  #endif
  391  	if (button == "a")
  392  		return ":/help/buttons_east.svg";
  393  	if (button == "b")
  394  		return ":/help/buttons_south.svg";
  395  	if (button == "x")
  396  		return ":/help/buttons_north.svg";
  397  	if (button == "y")
  398  		return ":/help/buttons_west.svg";
  399  	
  400  	return button;
  401  }
  402  
  403  void InputConfig::AssignActionButtons()
  404  {
  405  	bool invertButtons = Settings::getInstance()->getBool("InvertButtons");
  406  	
  407  #ifdef INVERTEDINPUTCONFIG
  408  	BUTTON_OK = invertButtons ? BBUTTON : ABUTTON;
  409  	BUTTON_BACK = invertButtons ? ABUTTON : BBUTTON;
  410  #else
  411  	BUTTON_OK = invertButtons ? ABUTTON : BBUTTON;
  412  	BUTTON_BACK = invertButtons ? BBUTTON : ABUTTON;
  413  #endif
  414  }
  415  
  416  std::string InputConfig::getSortDevicePath()
  417  {
  418  #ifdef WIN32
  419  	if (Utils::String::startsWith(Utils::String::toUpper(mDevicePath), "USB\\"))
  420  	{
  421  		auto lastSplit = mDevicePath.rfind("\\");
  422  		if (lastSplit != std::string::npos)
  423  		{
  424  			auto lastAnd = mDevicePath.rfind("&");
  425  			if (lastAnd != std::string::npos && lastAnd > lastSplit)
  426  			{
  427  				// Keep only last part which is probably some kind of MAC address
  428  				// Ex : USB\VID_045E&PID_02FF&IG_00\01&00&0000B7234380ED7E -> USB\VID_045E&PID_02FF&IG_00\0000B7234380ED7E
  429  				// 01 is some kind of a system device index, but can change upon reboot & we sometimes have 00&00&0000B7234380ED7E, and the order changes !
  430  				// Sort only with 0000B7234380ED7E ignoring 01&00 part
  431  
  432  				std::string ret = mDevicePath;
  433  				ret = ret.substr(0, lastSplit + 1) + ret.substr(lastAnd + 1);				
  434  				return ret;
  435  			}
  436  		}
  437  	}
  438  #endif
  439  
  440  #ifdef HAVE_UDEV
  441  	if (!mDeviceParentSysPath.empty()) return mDeviceParentSysPath;
  442  #endif
  443  
  444  	return mDevicePath;
  445  }
  446  
```

## src/InputConfig.h `:1-14` (an excerpt, upstream-carried, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_INPUT_CONFIG_H
    3  #define ES_CORE_INPUT_CONFIG_H
    4  
    5  #include <CECInput.h>
    6  #include <SDL_joystick.h>
    7  #include <SDL_keyboard.h>
    8  #include <map>
    9  #include <sstream>
   10  #include <vector>
   11  
   12  #ifdef WIN32
   13  #define INVERTEDINPUTCONFIG
   14  #endif
```

## src/InputManager.cpp (whole, fork-modified, at the pin)

```text
    1  #include "InputManager.h"
    2  
    3  #include "utils/FileSystemUtil.h"
    4  #include "utils/StringUtil.h"
    5  #include "CECInput.h"
    6  #include "Log.h"
    7  #include "utils/Platform.h"
    8  #include "Scripting.h"
    9  #include "Window.h"
   10  #include <pugixml/src/pugixml.hpp>
   11  #include <SDL.h>
   12  #include <iostream>
   13  #include <assert.h>
   14  #include "Settings.h"
   15  #include <algorithm>
   16  #include <mutex>
   17  #include "utils/StringUtil.h"
   18  #include "LocaleES.h"
   19  #include "Paths.h"
   20  #include "GunManager.h"
   21  #include "renderers/Renderer.h"
   22  #include <fstream>
   23  #include <set>
   24  
   25  #ifdef HAVE_UDEV
   26  #include <libudev.h>
   27  #include <fcntl.h>
   28  #include <sys/ioctl.h>
   29  #include <linux/input.h>
   30  #include <unistd.h>
   31  #endif
   32  
   33  #define KEYBOARD_GUID_STRING "-1"
   34  #define CEC_GUID_STRING      "-2"
   35  #define GUN_GUID_STRING      "-4"
   36  
   37  // SO HEY POTENTIAL POOR SAP WHO IS TRYING TO MAKE SENSE OF ALL THIS (by which I mean my future self)
   38  // There are like four distinct IDs used for joysticks (crazy, right?)
   39  // 1. Device index - this is the "lowest level" identifier, and is just the Nth joystick plugged in to the system (like /dev/js#).
   40  //    It can change even if the device is the same, and is only used to open joysticks (required to receive SDL events).
   41  // 2. SDL_JoystickID - this is an ID for each joystick that is supposed to remain consistent between plugging and unplugging.
   42  //    ES doesn't care if it does, though.
   43  // 3. "Device ID" - this is something I made up and is what InputConfig's getDeviceID() returns.  
   44  //    This is actually just an SDL_JoystickID (also called instance ID), but -1 means "keyboard" instead of "error."
   45  // 4. Joystick GUID - this is some squashed version of joystick vendor, version, and a bunch of other device-specific things.
   46  //    It should remain the same across runs of the program/system restarts/device reordering and is what I use to identify which joystick to load.
   47  
   48  // hack for cec support
   49  int SDL_USER_CECBUTTONDOWN = -1;
   50  int SDL_USER_CECBUTTONUP   = -1;
   51  
   52  static std::mutex mJoysticksLock;
   53  
   54  InputManager* InputManager::mInstance = NULL;
   55  Delegate<IJoystickChangedEvent> InputManager::joystickChanged;
   56  
   57  InputManager::InputManager() : mKeyboardInputConfig(nullptr), mMouseButtonsInputConfig(nullptr), mCECInputConfig(nullptr), mGunInputConfig(nullptr), mGunManager(nullptr)
   58  {
   59  
   60  }
   61  
   62  InputManager::~InputManager()
   63  {
   64  	deinit();
   65  }
   66  
   67  InputManager* InputManager::getInstance()
   68  {
   69  	if (!mInstance)
   70  		mInstance = new InputManager();
   71  
   72  	return mInstance;
   73  }
   74  
   75  
   76  void InputManager::init()
   77  {
   78  	if (initialized())
   79  		deinit();
   80  
   81  	mKeyboardInputConfig = new InputConfig(DEVICE_KEYBOARD, -1, "Keyboard", KEYBOARD_GUID_STRING, 0, 0, 0); 
   82  	loadInputConfig(mKeyboardInputConfig);
   83  
   84    rebuildAllJoysticks(false);
   85  
   86  #ifdef HAVE_LIBCEC
   87  	SDL_USER_CECBUTTONDOWN = SDL_RegisterEvents(2);
   88  	SDL_USER_CECBUTTONUP   = SDL_USER_CECBUTTONDOWN + 1;
   89  	CECInput::init();
   90  	mCECInputConfig = new InputConfig(DEVICE_CEC, -1, "CEC", CEC_GUID_STRING, 0, 0, 0); 
   91  	loadInputConfig(mCECInputConfig);
   92  #else
   93  	mCECInputConfig = nullptr;
   94  #endif
   95  
   96  	mGunInputConfig = new InputConfig(DEVICE_GUN, -1, "Gun", GUN_GUID_STRING, 0, 0, 0);
   97  	loadDefaultGunConfig();
   98  
   99  	// Mouse input, hardcoded not configurable with es_input.cfg
  100  	mMouseButtonsInputConfig = new InputConfig(DEVICE_MOUSE, -1, "Mouse", CEC_GUID_STRING, 0, 0, 0);
  101  	mMouseButtonsInputConfig->mapInput(BUTTON_OK, Input(DEVICE_MOUSE, TYPE_BUTTON, 1, 1, true));
  102  	mMouseButtonsInputConfig->mapInput(BUTTON_BACK, Input(DEVICE_MOUSE, TYPE_BUTTON, 3, 1, true));
  103  
  104  	mGunManager = new GunManager();
  105  }
  106  
  107  std::vector<std::string> InputManager::getMice() {
  108    std::vector<std::string> mice;
  109  
  110    #ifdef HAVE_UDEV
  111    struct udev *udev;
  112    struct udev_list_entry *devs = NULL;
  113    struct udev_list_entry *item = NULL;
  114    char ident[256];
  115  
  116    udev = udev_new();
  117    if (udev != NULL)
  118      {
  119        struct udev_enumerate *enumerate = udev_enumerate_new(udev);
  120        if (enumerate == NULL) { udev_unref(udev); return mice; }
  121        udev_enumerate_add_match_property(enumerate, "ID_INPUT_MOUSE", "1");
  122        udev_enumerate_add_match_subsystem(enumerate, "input");
  123        udev_enumerate_scan_devices(enumerate);
  124        devs = udev_enumerate_get_list_entry(enumerate);
  125  
  126        for (item = devs; item; item = udev_list_entry_get_next(item))
  127  	{
  128  	  const char *name = udev_list_entry_get_name(item);
  129  	  struct udev_device *dev = udev_device_new_from_syspath(udev, name);
  130  
  131  	  const char* devnode;
  132  	  devnode = udev_device_get_devnode(dev);
  133  	  if (devnode != NULL) {
  134  	    int fd = open(devnode, O_RDONLY | O_NONBLOCK);
  135  	    if (fd >= 0) {
  136  	      if (ioctl(fd, EVIOCGNAME(sizeof(ident)), ident) > 0) {
  137  		mice.push_back(std::string(ident));
  138  	      }
  139  	      close(fd);
  140  	    }
  141  	  }
  142  	  udev_device_unref(dev);
  143  	}
  144  
  145        udev_enumerate_unref(enumerate);
  146        udev_unref(udev);
  147      }
  148    #endif
  149    return mice;
  150  }
  151  
  152  
  153  void InputManager::deinit()
  154  {
  155  	if(!initialized())
  156  		return;
  157  
  158  	clearJoysticks();
  159  
  160  	if(mKeyboardInputConfig != NULL)
  161  	{
  162  		delete mKeyboardInputConfig;
  163  		mKeyboardInputConfig = NULL;
  164  	}
  165  
  166  	if(mCECInputConfig != NULL)
  167  	{
  168  		delete mCECInputConfig;
  169  		mCECInputConfig = NULL;
  170  	}
  171  
  172  	if (mMouseButtonsInputConfig != NULL)
  173  	{
  174  		delete mMouseButtonsInputConfig;
  175  		mMouseButtonsInputConfig = NULL;
  176  	}
  177  
  178  	if(mGunInputConfig != NULL)
  179  	{
  180  		delete mGunInputConfig;
  181  		mGunInputConfig = NULL;
  182  	}
  183  
  184  #ifdef HAVE_LIBCEC
  185  	CECInput::deinit();
  186  #endif
  187  
  188  	SDL_JoystickEventState(SDL_DISABLE);
  189  	SDL_QuitSubSystem(SDL_INIT_JOYSTICK);
  190  
  191  	if (mGunManager != nullptr)
  192  	{
  193  		delete mGunManager;
  194  		mGunManager = nullptr;
  195  	}
  196  }
  197  
  198  int InputManager::getNumJoysticks() 
  199  { 
  200  	std::unique_lock<std::mutex> lock(mJoysticksLock);
  201  	return (int)mJoysticks.size(); 
  202  }
  203  
  204  InputConfig* InputManager::getInputConfigByDevice(int device)
  205  {
  206  	if(device == DEVICE_KEYBOARD)
  207  		return mKeyboardInputConfig;
  208  
  209  	if(device == DEVICE_CEC)
  210  		return mCECInputConfig;
  211  
  212  	if(device == DEVICE_MOUSE)
  213  		return mMouseButtonsInputConfig;
  214  
  215  	if(device == DEVICE_GUN)
  216  		return mGunInputConfig;
  217  	
  218  	auto it = mInputConfigs.find(device);
  219  	if (it == mInputConfigs.cend())
  220  		return nullptr;
  221  
  222  	return it->second;
  223  }
  224  
  225  void InputManager::clearJoysticks()
  226  {
  227  	mJoysticksLock.lock();
  228  
  229  	for (auto iter = mJoysticks.begin(); iter != mJoysticks.end(); iter++)
  230  		SDL_JoystickClose(iter->second);
  231  
  232  	mJoysticks.clear();
  233  
  234  	for (auto iter = mInputConfigs.begin(); iter != mInputConfigs.end(); iter++)
  235  		if (iter->second)
  236  			delete iter->second;
  237  
  238  	mInputConfigs.clear();
  239  
  240  	mPrevAxisValues.clear();
  241  
  242  	mJoysticksLock.unlock();
  243  }
  244  
  245  #if defined(WIN32)
  246  #include <cfgmgr32.h>
  247  
  248  class Win32RawInputApi
  249  {
  250  public:
  251  	Win32RawInputApi()
  252  	{		
  253  		m_hSDL2 = ::LoadLibrary("SDL2.dll");
  254  		if (m_hSDL2 != NULL)
  255  		{
  256  			m_JoystickPathForIndex = (SDL_JoystickPathForIndexPtr) ::GetProcAddress(m_hSDL2, "SDL_JoystickPathForIndex");
  257  		}
  258  
  259  		m_hSetupapi = ::LoadLibrary("setupapi.dll");
  260  		if (m_hSetupapi != NULL)
  261  		{
  262  			m_CM_Locate_DevNodeA = (CM_Locate_DevNodeAPtr) ::GetProcAddress(m_hSetupapi, "CM_Locate_DevNodeA");
  263  			m_CM_Get_Parent = (CM_Get_ParentPtr) ::GetProcAddress(m_hSetupapi, "CM_Get_Parent");
  264  			m_CM_Get_Device_IDA = (CM_Get_Device_IDAPtr) ::GetProcAddress(m_hSetupapi, "CM_Get_Device_IDA");
  265  		}
  266  	}
  267  
  268  	~Win32RawInputApi()
  269  	{
  270  		if (m_hSDL2 != NULL)
  271  			::FreeLibrary(m_hSDL2);
  272  
  273  		m_hSDL2 = NULL;
  274  
  275  		if (m_hSetupapi != NULL)
  276  			::FreeLibrary(m_hSetupapi);
  277  
  278  		m_hSetupapi = NULL;
  279  	}
  280  	
  281  	std::string SDL_JoystickPathForIndex(int device_index)
  282  	{
  283  		if (m_JoystickPathForIndex != NULL)
  284  		{
  285  			const char* path = m_JoystickPathForIndex(device_index);
  286  			if (path != NULL)
  287  				return std::string(path);
  288  		}
  289  
  290  		return "";
  291  	}
  292  
  293  	std::string getHidCollectionSuffix(const std::string& devicePath)
  294  	{
  295  		std::string upper = Utils::String::toUpper(devicePath);
  296  
  297  		size_t idx = upper.find("&COL");
  298  		if (idx == std::string::npos)
  299  			return "";
  300  
  301  		size_t start = idx + 4;
  302  		size_t end = start;
  303  		while (end < upper.size() && upper[end] >= '0' && upper[end] <= '9')
  304  			end++;
  305  
  306  		if (end == start)
  307  			return "";
  308  
  309  		return "#COL" + upper.substr(start, end - start);
  310  	}
  311  
  312  	std::string getInputDeviceParent(const std::string& devicePath)
  313  	{
  314  		if (m_CM_Locate_DevNodeA == NULL || m_CM_Get_Parent == NULL || m_CM_Get_Device_IDA == NULL)
  315  			return devicePath;
  316  
  317  		std::string path = devicePath;
  318  
  319  		auto vidindex = path.find("VID_");
  320  		if (vidindex == std::string::npos)
  321  			vidindex = path.find("vid_");
  322  
  323  		if (vidindex != std::string::npos)
  324  		{
  325  			auto cut = path.find("#{", vidindex);
  326  			if (cut != std::string::npos)
  327  				path = path.substr(0, cut);
  328  		}
  329  
  330  		path = Utils::String::replace(path, "\\\\?\\", "");
  331  		path = Utils::String::replace(path, "#", "\\");
  332  
  333  		// Multi-collection HID devices (Xin-Mo / Xinmotek dual arcade encoders, DragonRise and
  334  		// "Twin USB" 2-players boards, ...) expose one joystick per top-level collection, and all
  335  		// these collections share the exact same parent device node. Keep the collection index,
  336  		// otherwise every player would be given the very same device path.
  337  		std::string collection = getHidCollectionSuffix(devicePath);
  338  
  339  		DEVINST nDevInst;
  340  		int apiResult = m_CM_Locate_DevNodeA(&nDevInst, (DEVINSTID_A)path.c_str(), CM_LOCATE_DEVNODE_NORMAL);
  341  		if (apiResult == CR_SUCCESS)
  342  		{
  343  			if (m_CM_Get_Parent(&nDevInst, nDevInst, 0) == CR_SUCCESS)
  344  			{
  345  				char buf[255];
  346  				if (m_CM_Get_Device_IDA(nDevInst, buf, 255, 0) == CR_SUCCESS)
  347  					return std::string(buf) + collection;
  348  			}
  349  		}
  350  
  351  		return devicePath;
  352  	}
  353  
  354  private:	
  355  	HMODULE m_hSDL2;
  356  	HMODULE m_hSetupapi;
  357  
  358  	typedef const char *(SDLCALL *SDL_JoystickPathForIndexPtr)(int);
  359  	SDL_JoystickPathForIndexPtr m_JoystickPathForIndex;
  360  	
  361  	typedef CONFIGRET(WINAPI* CM_Locate_DevNodeAPtr)(PDEVINST pdnDevInst, DEVINSTID_A pDeviceID, ULONG ulFlags);
  362  	CM_Locate_DevNodeAPtr m_CM_Locate_DevNodeA;
  363  
  364  	typedef CONFIGRET(WINAPI* CM_Get_ParentPtr)(PDEVINST pdnDevInst, DEVINST dnDevInst, ULONG ulFlags);
  365  	CM_Get_ParentPtr m_CM_Get_Parent;
  366  
  367  	typedef CONFIGRET(WINAPI* CM_Get_Device_IDAPtr)(DEVINST dnDevInst, PSTR Buffer, ULONG BufferLen, ULONG ulFlags);
  368  	CM_Get_Device_IDAPtr m_CM_Get_Device_IDA;
  369  };
  370  
  371  Win32RawInputApi Win32RawInput;
  372  #endif
  373  
  374  void InputManager::rebuildAllJoysticks(bool deinit)
  375  {
  376  	if (deinit)
  377  		SDL_JoystickEventState(SDL_DISABLE);
  378  
  379  	clearJoysticks();
  380  
  381  	if (deinit)
  382  		SDL_QuitSubSystem(SDL_INIT_JOYSTICK);
  383  
  384  #if WIN32
  385  	if (!Settings::getInstance()->getBool("HidJoysticks"))
  386  		SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI, "0");
  387  
  388  	SDL_SetHint("SDL_JOYSTICK_HIDAPI_WII", "0");
  389  
  390  	// Disable PS5 enhanced feature reports (rumble, LED, haptics).
  391  	// On Windows, SDL attempts these HID exchanges during HIDAPI init.
  392  	// If the Bluetooth audio endpoint isn't ready yet, SDL gets an error,
  393  	// marks the controller disconnected, and retries endlessly — causing
  394  	// the infinite "DualSense connected" notification loop. Disabling them
  395  	// prevents that cycle and also allows the controller to be detected
  396  	// when it is already paired before ES starts.
  397  	SDL_SetHint("SDL_JOYSTICK_HIDAPI_PS5_RUMBLE", "0");
  398  	SDL_SetHint("SDL_JOYSTICK_HIDAPI_PS5_PLAYER_LED", "0");
  399  #endif
  400  			
  401  	SDL_SetHint(SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS, Settings::getInstance()->getBool("BackgroundJoystickInput") ? "1" : "0");
  402  	SDL_InitSubSystem(SDL_INIT_JOYSTICK);
  403  
  404  #if WIN32
  405  	// Load additional controller mappings into SDL, before enumerating the devices.
  406  	// SDL_QuitSubSystem(SDL_INIT_JOYSTICK) frees every mapping added at runtime, so this has to be
  407  	// done on every rebuild, not once at startup.
  408  	// Load order defines priority : a mapping added later overrides the previous one for the same
  409  	// GUID, and any file entry overrides SDL's built-in database.
  410  	// 1. Community database shipped next to the ES executable.
  411  	// 2. User file, in the user configuration folder, so it is never overwritten by an update.
  412  	const std::string mappingFiles[] =
  413  	{
  414  		Paths::getEmulationStationPath() + "/gamecontrollerdb.txt",
  415  		Paths::getUserEmulationStationPath() + "/gamecontrollerdb.txt"
  416  	};
  417  
  418  	for (auto& mappingFile : mappingFiles)
  419  	{
  420  		if (!Utils::FileSystem::exists(mappingFile))
  421  			continue;
  422  
  423  		// The file is read line by line instead of using SDL_GameControllerAddMappingsFromFile,
  424  		// only to be tolerant on the platform field : SDL requires it and silently drops every line
  425  		// that does not declare one, which is a common mistake when a mapping is pasted by hand.
  426  		// Everything else, and above all the GUID matching, is left to SDL.
  427  		std::ifstream dbFile(mappingFile);
  428  		std::string line;
  429  		int added = 0;
  430  		int failed = 0;
  431  
  432  		while (std::getline(dbFile, line))
  433  		{
  434  			line = Utils::String::trim(line);
  435  
  436  			if (line.empty() || line[0] == '#')
  437  				continue;
  438  
  439  			if (line.find("platform:") == std::string::npos)
  440  			{
  441  				// Assume Windows when the platform is not specified
  442  				if (line.back() != ',')
  443  					line += ",";
  444  
  445  				line += "platform:Windows,";
  446  			}
  447  			else if (line.find("platform:Windows,") == std::string::npos)
  448  				continue; // Another platform, or a custom tag like WindowsWheel / WindowsGun
  449  
  450  			if (SDL_GameControllerAddMapping(line.c_str()) >= 0)
  451  				added++;
  452  			else
  453  			{
  454  				failed++;
  455  				LOG(LogWarning) << "Invalid controller mapping in " << mappingFile << " : " << SDL_GetError();
  456  			}
  457  		}
  458  
  459  		LOG(LogInfo) << "Loaded " << added << " controller mapping(s) from " << mappingFile << " (" << failed << " rejected)";
  460  	}
  461  
  462  	// SDL's HIDAPI thread enumerates devices asynchronously after SDL_InitSubSystem.
  463  	// For DualSense/DS4 over Bluetooth, the HID handshake is not complete by the
  464  	// time SDL_NumJoysticks() is called immediately after init, so the controller
  465  	// is missed. Poll until the count stabilises (max 500ms) instead of a fixed sleep.
  466  	if (!deinit)
  467  	{
  468  		int prevCount = -1;
  469  		int stableCount = SDL_NumJoysticks();
  470  		int attempts = 0;
  471  		while (stableCount != prevCount && attempts < 10)
  472  		{
  473  			prevCount = stableCount;
  474  			SDL_Delay(50);
  475  			SDL_PumpEvents();
  476  			stableCount = SDL_NumJoysticks();
  477  			attempts++;
  478  		}
  479  
  480  		if (attempts >= 10)
  481  			LOG(LogWarning) << "Joystick count did not stabilise after 500ms, continuing with " << stableCount << " joystick(s)";
  482  	}
  483  #endif
  484  
  485  	mJoysticksLock.lock();
  486  
  487  	int numJoysticks = SDL_NumJoysticks();
  488  
  489  #if WIN32
  490  	// SDL can expose the same physical pad twice when its internal deduplication
  491  	// between RAWINPUT and XInput loses the race during a hotplug: XInput enumerates before
  492  	// RAWINPUT_IsDevicePresent() can respond true, and the WINDOWS backend only
  493  	// re-enumerates on the next WM_DEVICECHANGE notification, so the duplicate remains
  494  	// until restart. Cold SDL only keeps the RAWINPUT view: we restore the
  495  	// same result hot. The redundant XInput view exposes no HID path, the RAWINPUT view does.
  496  	SDL_version sdlVer;
  497  	SDL_GetVersion(&sdlVer);
  498  	bool hasPathApi = (sdlVer.major > 2 || (sdlVer.major == 2 && sdlVer.minor >= 24));
  499  
  500  	std::vector<std::string> sdlDevicePaths;
  501  	std::set<std::string> vendorProductWithPath;
  502  
  503  	for (int i = 0; i < numJoysticks; i++)
  504  	{
  505  		std::string path = hasPathApi ? Win32RawInput.SDL_JoystickPathForIndex(i) : "";
  506  		sdlDevicePaths.push_back(path);
  507  
  508  		if (path.empty())
  509  			continue;
  510  
  511  		char preGuid[40];
  512  		SDL_JoystickGetGUIDString(SDL_JoystickGetDeviceGUID(i), preGuid, 40);
  513  		vendorProductWithPath.insert(std::string(preGuid).substr(8, 16)); // vendor + product
  514  	}
  515  #endif
  516  
  517  	for (int idx = 0; idx < numJoysticks; idx++)
  518  	{
  519  		// open joystick & add to our list
  520  		SDL_Joystick* joy = SDL_JoystickOpen(idx);
  521  		if (joy == nullptr)
  522  			continue;
  523  
  524  		// add it to our list so we can close it again later
  525  		SDL_JoystickID joyId = SDL_JoystickInstanceID(joy);
  526  
  527  		char guid[40];
  528  		SDL_JoystickGetGUIDString(SDL_JoystickGetGUID(joy), guid, 40);
  529  
  530  		// SDL_JoystickName can return NULL. InputConfig takes a const std::string&,
  531  		// and operator<<(const char*) with NULL is undefined behaviour too.
  532  		const char* joyName = SDL_JoystickName(joy);
  533  		std::string deviceName = (joyName != nullptr) ? joyName : "Unknown joystick";
  534  
  535  #if WIN32
  536  		// SDL 2.26 + -> Remove new CRC-16 name hash encoding
  537  		for (int i = 4; i < 8; i++) guid[i] = '0';
  538  
  539  		// Drop the redundant XInput view : it carries no HID device path while the
  540  		// RAWINPUT view of the same VID/PID does.
  541  		if (hasPathApi && sdlDevicePaths[idx].empty() && vendorProductWithPath.count(std::string(guid).substr(8, 16)) > 0)
  542  		{
  543  			LOG(LogWarning) << "Skipping redundant XInput view of " << deviceName << " (GUID: " << guid << ", instance ID: " << joyId << ", device index: " << idx << ")";
  544  			SDL_JoystickClose(joy);
  545  			continue;
  546  		}
  547  #endif
  548  
  549  		mJoysticks.erase(joyId);
  550  		mJoysticks[joyId] = joy;
  551  
  552  		// create the InputConfig
  553  		auto cfg = mInputConfigs.find(joyId);
  554  		if (cfg != mInputConfigs.cend())
  555  		{
  556  			if (cfg->second != nullptr)
  557  				delete cfg->second;
  558  
  559  			mInputConfigs.erase(joyId);
  560  		}
  561  
  562  		// if SDL_JoystickPathForIndex does not exist, store a value containing index + guid
  563  		std::string devicePath = Utils::String::padLeft(std::to_string(idx), 4, '0') + "@" + std::string(guid);
  564  
  565  #if WIN32
  566  		if (hasPathApi)
  567  		{
  568  			if (!sdlDevicePaths[idx].empty())
  569  				devicePath = Win32RawInput.getInputDeviceParent(sdlDevicePaths[idx]);
  570  			else
  571  				LOG(LogWarning) << "SDL_JoystickPathForIndex returned no path for index " << idx << ", falling back to index@guid";
  572  		}
  573  #elif SDL_VERSION_ATLEAST(2, 24, 0)
  574  		{
  575  			const char* sdlPath = SDL_JoystickPathForIndex(idx);
  576  			if (sdlPath != nullptr)
  577  				devicePath = sdlPath;
  578  		}
  579  #endif
  580  
  581  		mInputConfigs[joyId] = new InputConfig(joyId, idx, deviceName, guid, SDL_JoystickNumButtons(joy), SDL_JoystickNumHats(joy), SDL_JoystickNumAxes(joy), devicePath);
  582  
  583  		if (!loadInputConfig(mInputConfigs[joyId]))
  584  		{
  585  #if !defined(BATOCERA) || !defined(ROCKNIX)
  586  			std::string mappingString;
  587  			
  588  			// The gamecontrollerdb.txt files are loaded into SDL itself (see rebuildAllJoysticks,
  589  			// right after SDL_InitSubSystem), so SDL applies them with its own GUID matching rules
  590  			// and with the right priority. Those files must never be parsed by hand : SDL compares
  591  			// the full GUID, including the backend byte, and a DirectInput entry must not be applied
  592  			// to the same pad seen through XInput, RAWINPUT or HIDAPI.
  593  			if (SDL_IsGameController(idx))
  594  			{
  595  				char* sdlMapping = SDL_GameControllerMappingForDeviceIndex(idx);
  596  				if (sdlMapping != nullptr)
  597  				{
  598  					mappingString = sdlMapping;
  599  					SDL_free(sdlMapping); // SDL allocates this string, the caller owns it
  600  				}
  601  			}
  602  
  603  			if (!mappingString.empty() && loadFromSdlMapping(mInputConfigs[joyId], mappingString))
  604  			{
  605  				InputManager::getInstance()->writeDeviceConfig(mInputConfigs[joyId]);
  606  				LOG(LogInfo) << "Creating joystick from SDL Game Controller mapping " << deviceName << " (GUID: " << guid << ", instance ID: " << joyId << ", device index: " << idx << ", device path : " << devicePath << ").";
  607  			}
  608  			else
  609  #endif
  610  				LOG(LogInfo) << "Added unconfigured joystick " << deviceName << " (GUID: " << guid << ", instance ID: " << joyId << ", device index: " << idx << ", device path : " << devicePath << ").";
  611  		}
  612  		else
  613  			LOG(LogInfo) << "Added known joystick " << deviceName << " (GUID: " << guid << ", instance ID: " << joyId << ", device index: " << idx << ", device path : " << devicePath << ").";
  614  
  615  		// set up the prevAxisValues
  616  		int numAxes = SDL_JoystickNumAxes(joy);
  617  		if (numAxes < 0)
  618  			numAxes = 0;
  619  
  620  		mPrevAxisValues[joyId] = std::vector<int>(numAxes, 0);
  621  	}	
  622  
  623  	mJoysticksLock.unlock();
  624  
  625  	computeLastKnownPlayersDeviceIndexes();
  626  
  627  	joystickChanged.invoke([](IJoystickChangedEvent* c) { c->onJoystickChanged(); });
  628  
  629  	SDL_JoystickEventState(SDL_ENABLE);
  630  }
  631  
  632  #if WIN32
  633  // Retrocompatible declaration for SDL_JoyBatteryEvent
  634  typedef struct SDL_JoyBatteryEventX
  635  {
  636  	Uint32 type;        
  637  	Uint32 timestamp;   
  638  	SDL_JoystickID which; 
  639  	SDL_JoystickPowerLevel level;
  640  } SDL_JoyBatteryEventX;
  641  #endif
  642  
  643  bool InputManager::parseEvent(const SDL_Event& ev, Window* window)
  644  {
  645  	bool causedEvent = false;
  646  
  647  	switch (ev.type)
  648  	{
  649  #if WIN32
  650  	case 1543: // SDL_JOYBATTERYUPDATED, new event with SDL 2.24+
  651  	{
  652  		SDL_JoyBatteryEventX* jbattery = (SDL_JoyBatteryEventX*)&ev;
  653  
  654  		auto inputConfig = mInputConfigs.find(jbattery->which);
  655  		if (inputConfig != mInputConfigs.cend() && inputConfig->second != nullptr && inputConfig->second->isConfigured() && jbattery->level != SDL_JoystickPowerLevel::SDL_JOYSTICK_POWER_UNKNOWN)
  656  		{
  657  			int level = 0;
  658  
  659  			switch (jbattery->level)
  660  			{
  661  			case SDL_JoystickPowerLevel::SDL_JOYSTICK_POWER_LOW:
  662  				level = 25;
  663  				break;
  664  			case SDL_JoystickPowerLevel::SDL_JOYSTICK_POWER_MEDIUM:
  665  				level = 50;
  666  				break;
  667  			case SDL_JoystickPowerLevel::SDL_JOYSTICK_POWER_MAX:
  668  				level = 75;
  669  				break;
  670  			case SDL_JoystickPowerLevel::SDL_JOYSTICK_POWER_FULL:
  671  				level = 100;
  672  				break;
  673  			case SDL_JoystickPowerLevel::SDL_JOYSTICK_POWER_WIRED:
  674  				level = -1;
  675  				break;
  676  			}
  677  
  678  			inputConfig->second->updateBatteryLevel(level);
  679  			computeLastKnownPlayersDeviceIndexes();
  680  		}
  681  	}
  682  	break;
  683  #endif
  684  
  685  	case SDL_JOYAXISMOTION:
  686  	{		
  687  	// some axes are "full" : from -32000 to +32000
  688  	// in this case, their unpressed state is not 0
  689  	// SDL provides a function to get this value
  690  	// in es, the trick is to minus this value to the value to do as if it started at 0
  691  		int initialValue = 0;
  692  		Sint16 x;
  693  
  694  #if SDL_VERSION_ATLEAST(2, 0, 9)
  695  		// SDL_JoystickGetAxisInitialState doesn't work with 8bitdo start+b
  696  		// required for several pads like xbox and 8bitdo
  697  
  698  		auto inputConfig = mInputConfigs.find(ev.jaxis.which);
  699  		if (inputConfig != mInputConfigs.cend() && inputConfig->second != nullptr)
  700  		{
  701  			std::string guid = std::to_string(ev.jaxis.axis) + "@" + inputConfig->second->getDeviceGUIDString();
  702  
  703  			auto it = mJoysticksInitialValues.find(guid);
  704  			if (it != mJoysticksInitialValues.cend())
  705  				initialValue = it->second;
  706  			else
  707  			{
  708  				// Do not use operator[] here : it would insert a null SDL_Joystick*
  709  				// for a removed instance id, which clearJoysticks() would then pass
  710  				// to SDL_JoystickClose().
  711  				auto joy = mJoysticks.find(ev.jaxis.which);
  712  				if (joy != mJoysticks.cend() && joy->second != nullptr && SDL_JoystickGetAxisInitialState(joy->second, ev.jaxis.axis, &x))
  713  				{
  714  					mJoysticksInitialValues[guid] = x;
  715  					initialValue = x;
  716  				}
  717  			}
  718  		}
  719  #endif
  720  
  721  		auto prevAxis = mPrevAxisValues.find(ev.jaxis.which);
  722  		if (prevAxis != mPrevAxisValues.cend() && (size_t)ev.jaxis.axis < prevAxis->second.size())
  723  		{
  724  			int& prevValue = prevAxis->second[ev.jaxis.axis];
  725  
  726  			//if it switched boundaries
  727  			if ((abs(ev.jaxis.value - initialValue) > DEADZONE) != (abs(prevValue) > DEADZONE))
  728  			{
  729  				int normValue;
  730  				if (abs(ev.jaxis.value - initialValue) <= DEADZONE)
  731  					normValue = 0;
  732  				else
  733  					if (ev.jaxis.value - initialValue > 0)
  734  						normValue = 1;
  735  					else
  736  						normValue = -1;
  737  
  738  				window->input(getInputConfigByDevice(ev.jaxis.which), Input(ev.jaxis.which, TYPE_AXIS, ev.jaxis.axis, normValue, false));
  739  				causedEvent = true;
  740  			}
  741  
  742  			prevValue = ev.jaxis.value - initialValue;
  743  		}
  744  
  745  		return causedEvent;
  746  	}
  747  	case SDL_JOYBUTTONDOWN:
  748  	case SDL_JOYBUTTONUP:
  749  		window->input(getInputConfigByDevice(ev.jbutton.which), Input(ev.jbutton.which, TYPE_BUTTON, ev.jbutton.button, ev.jbutton.state == SDL_PRESSED, false));
  750  		return true;
  751  	
  752  	case SDL_MOUSEBUTTONDOWN:        
  753  	case SDL_MOUSEBUTTONUP:
  754  		if (Settings::getInstance()->getBool("DisableTouchscreen"))
  755  			return false;
  756  
  757  		if (!getGunManager()->isReplacingMouse())
  758  			if (!window->processMouseButton(ev.button.button, ev.type == SDL_MOUSEBUTTONDOWN, ev.button.x, ev.button.y))
  759  				window->input(getInputConfigByDevice(DEVICE_MOUSE), Input(DEVICE_MOUSE, TYPE_BUTTON, ev.button.button, ev.type == SDL_MOUSEBUTTONDOWN, false));
  760  
  761  		return true;
  762  
  763  	case SDL_MOUSEMOTION:
  764  #if !WIN32
  765  	  if (!Utils::Platform::isBuildroot() || ev.motion.which == SDL_TOUCH_MOUSEID)
  766  #endif
  767  		if (Settings::getInstance()->getBool("DisableTouchscreen"))
  768  			return false;
  769  
  770  		if (!getGunManager()->isReplacingMouse())
  771  			window->processMouseMove(ev.motion.x, ev.motion.y, ev.motion.which == SDL_TOUCH_MOUSEID);
  772  	  
  773  		return true;
  774  
  775  	case SDL_MOUSEWHEEL:
  776  		if (ev.wheel.which != SDL_TOUCH_MOUSEID)
  777  			window->processMouseWheel(ev.wheel.y);
  778  
  779  		return true;
  780  
  781  	case SDL_JOYHATMOTION:
  782  		window->input(getInputConfigByDevice(ev.jhat.which), Input(ev.jhat.which, TYPE_HAT, ev.jhat.hat, ev.jhat.value, false));
  783  		return true;
  784  
  785  	case SDL_KEYDOWN:
  786  		if (ev.key.keysym.sym == SDLK_BACKSPACE && SDL_IsTextInputActive())
  787  			window->textInput("\b");
  788  
  789  		if (ev.key.repeat)
  790  			return false;
  791  
  792  #if !WIN32
  793  		if (ev.key.keysym.sym == SDLK_F4)
  794  		{
  795  			SDL_Event* quit = new SDL_Event();
  796  			quit->type = SDL_QUIT;
  797  			SDL_PushEvent(quit);
  798  			return false;
  799  		}
  800  #endif
  801  
  802  		window->input(getInputConfigByDevice(DEVICE_KEYBOARD), Input(DEVICE_KEYBOARD, TYPE_KEY, ev.key.keysym.sym, 1, false));
  803  		return true;
  804  
  805  	case SDL_KEYUP:
  806  		window->input(getInputConfigByDevice(DEVICE_KEYBOARD), Input(DEVICE_KEYBOARD, TYPE_KEY, ev.key.keysym.sym, 0, false));
  807  		return true;
  808  
  809  	case SDL_TEXTINPUT:
  810  		window->textInput(ev.text.text);
  811  		break;
  812  
  813  	case SDL_JOYDEVICEADDED:
  814  		{
  815  			std::string addedDeviceName;
  816  			bool isWheel = false;
  817  			int deviceIndex = ev.jdevice.which;
  818  			if (deviceIndex < 0 || deviceIndex >= SDL_NumJoysticks())
  819  			{
  820  				LOG(LogWarning) << "SDL_JOYDEVICEADDED : stale device index " << deviceIndex << ", event ignored";
  821  				return false;
  822  			}
  823  
  824  			auto id = SDL_JoystickGetDeviceInstanceID(deviceIndex);
  825  			if (id < 0)
  826  			{
  827  				LOG(LogWarning) << "SDL_JOYDEVICEADDED : no instance id for device index " << deviceIndex << ", event ignored";
  828  				return false;
  829  			}
  830  			
  831  			auto it = std::find_if(mInputConfigs.cbegin(), mInputConfigs.cend(), [id](const std::pair<SDL_JoystickID, InputConfig*>& t) { return t.second != nullptr && t.second->getDeviceId() == id; });
  832  			if (it == mInputConfigs.cend())
  833  			{
  834  				const char* addedName = SDL_JoystickNameForIndex(deviceIndex);
  835  				if (addedName != nullptr)
  836  					addedDeviceName = addedName;
  837  			}
  838  
  839  #ifdef HAVE_UDEV
  840  #ifdef SDL_JoystickDevicePathById
  841                          SDL_Joystick* joy = SDL_JoystickOpen(deviceIndex);
  842  		        if (joy != nullptr) {
  843                            SDL_JoystickID joyId = SDL_JoystickInstanceID(joy);
  844                            isWheel = InputConfig::isWheel(SDL_JoystickDevicePathById(joyId));
  845                            SDL_JoystickClose(joy);
  846  			}
  847  #endif
  848  #endif
  849  #if WIN32
  850  			rebuildAllJoysticks(false);
  851  #else
  852  			rebuildAllJoysticks();
  853  #endif
  854  			if (Settings::getInstance()->getBool("ShowControllerNotifications") && !addedDeviceName.empty()) {
  855  			  if(isWheel) {
  856  			    window->displayNotificationMessage(_U("\uF1B9 ") + Utils::String::format(_("%s connected").c_str(), Utils::String::trim(addedDeviceName).c_str()));
  857  			  } else {
  858  			    window->displayNotificationMessage(_U("\uF11B ") + Utils::String::format(_("%s connected").c_str(), Utils::String::trim(addedDeviceName).c_str()));
  859  			  }
  860  			}
  861  		}
  862  		return true;
  863  
  864  	case SDL_JOYDEVICEREMOVED:
  865  		{
  866  			auto it = mInputConfigs.find(ev.jdevice.which);
  867  			if (Settings::getInstance()->getBool("ShowControllerNotifications") && it != mInputConfigs.cend() && it->second != nullptr) {
  868  			  if(it->second->isWheel()) {
  869  			    window->displayNotificationMessage(_U("\uF1B9 ") + Utils::String::format(_("%s disconnected").c_str(), Utils::String::trim(it->second->getDeviceName()).c_str()));
  870  			  } else {
  871  			    window->displayNotificationMessage(_U("\uF11B ") + Utils::String::format(_("%s disconnected").c_str(), Utils::String::trim(it->second->getDeviceName()).c_str()));
  872  			  }
  873  			}
  874  	
  875  			rebuildAllJoysticks();
  876  		}
  877  		return false;
  878  	}
  879  
  880  	if (mCECInputConfig && (ev.type == (unsigned int)SDL_USER_CECBUTTONDOWN || ev.type == (unsigned int)SDL_USER_CECBUTTONUP))
  881  	{
  882  		window->input(getInputConfigByDevice(DEVICE_CEC), Input(DEVICE_CEC, TYPE_CEC_BUTTON, ev.user.code, ev.type == (unsigned int)SDL_USER_CECBUTTONDOWN, false));
  883  		return true;
  884  	}
  885  
  886  	return false;
  887  }
  888  
  889  bool InputManager::tryLoadInputConfig(std::string path, InputConfig* config, bool allowApproximate)
  890  {
  891  	pugi::xml_node configNode(NULL);
  892  
  893  	if (!Utils::FileSystem::exists(path))
  894  		return false;
  895  
  896  	pugi::xml_document doc;
  897  	pugi::xml_parse_result res = doc.load_file(WINSTRINGW(path).c_str());
  898  
  899  	if (!res)
  900  	{
  901  		LOG(LogError) << "Error parsing input config: " << res.description();
  902  		return false;
  903  	}
  904  
  905  	pugi::xml_node root = doc.child("inputList");
  906  	if (!root)
  907  		return false;
  908  	
  909  	// Search for exact match guid + name
  910  	for (pugi::xml_node item = root.child("inputConfig"); item; item = item.next_sibling("inputConfig"))
  911  	{
  912  		if (strcmp(config->getDeviceGUIDString().c_str(), item.attribute("deviceGUID").value()) == 0 && strcmp(config->getDeviceName().c_str(), item.attribute("deviceName").value()) == 0)
  913  		{
  914  			configNode = item;
  915  			break;
  916  		}
  917  	}
  918  
  919  	// Search for guid + name match but test guid without the new crc16 bytes (SDL2 2.26)
  920  	// Cf. https://github.com/libsdl-org/SDL/commit/c1e087394020a8cb9d2a04a1eabbcc23a6a5b20d
  921  	if (!configNode)
  922  	{
  923  		for (pugi::xml_node item = root.child("inputConfig"); item; item = item.next_sibling("inputConfig"))
  924  		{
  925  			// Remove CRC-16 encoding from SDL2 2.26+ guids
  926  			std::string guid = config->getDeviceGUIDString();
  927  			for (int i = 4; i < 8 && i < guid.length(); i++)
  928  				guid[i] = '0';
  929  
  930  			if (guid != config->getDeviceGUIDString())
  931  			if (strcmp(guid.c_str(), item.attribute("deviceGUID").value()) == 0 && strcmp(config->getDeviceName().c_str(), item.attribute("deviceName").value()) == 0)
  932  			{
  933  				configNode = item;
  934  				break;
  935  			}
  936  		}
  937  	}
  938  
  939  	// Search for exact match guid
  940  	if (!configNode && allowApproximate)
  941  	{
  942  		for (pugi::xml_node item = root.child("inputConfig"); item; item = item.next_sibling("inputConfig"))
  943  		{
  944  			if (strcmp(config->getDeviceGUIDString().c_str(), item.attribute("deviceGUID").value()) == 0)
  945  			{
  946  				LOG(LogInfo) << "Approximative device found using guid=" << configNode.attribute("deviceGUID").value() << " name=" << configNode.attribute("deviceName").value() << ")";
  947  				configNode = item;
  948  				break;
  949  			}
  950  		}
  951  	}
  952  
  953  	// Search for name match
  954  	if (!configNode && allowApproximate)
  955  	{
  956  		for (pugi::xml_node item = root.child("inputConfig"); item; item = item.next_sibling("inputConfig"))
  957  		{
  958  			if (strcmp(config->getDeviceName().c_str(), item.attribute("deviceName").value()) == 0)
  959  			{
  960  				LOG(LogInfo) << "Approximative device found using guid=" << configNode.attribute("deviceGUID").value() << " name=" << configNode.attribute("deviceName").value() << ")";
  961  				configNode = item;
  962  				break;
  963  			}
  964  		}
  965  	}
  966  
  967  	if (!configNode)
  968  		return false;
  969  
  970  	config->loadFromXML(configNode);
  971  	return true;
  972  }
  973  
  974  static std::map<std::string, std::string> _sdlToEsMapping =
  975  {
  976  #ifdef INVERTEDINPUTCONFIG
  977     { "a",             "a" },
  978     { "b",             "b" },
  979  #else
  980     { "a",             "b" },
  981     { "b",             "a" },
  982  #endif
  983     { "x",             "y" },
  984     { "y",             "x" },
  985     { "back",          "select" },
  986     { "start",         "start" },
  987     { "leftshoulder",  "pageup" },
  988     { "rightshoulder", "pagedown" },
  989     { "dpup",          "up" },
  990     { "dpright",       "right" },
  991     { "dpdown",        "down" },
  992     { "dpleft",        "left" },
  993     { "leftx",         "joystick1left" },
  994     { "lefty",         "joystick1up" },
  995     { "rightx",        "joystick2left" },
  996     { "righty",        "joystick2up" },
  997     { "lefttrigger",   "l2" },
  998     { "righttrigger",  "r2" },
  999     { "leftstick",     "l3" },
 1000     { "rightstick",    "r3" }
 1001     // { "guide",         "hotkey" } // Better take select for hotkey ?
 1002  };
 1003  
 1004  bool InputManager::loadFromSdlMapping(InputConfig* config, const std::string& mapping)
 1005  {	
 1006  	bool isConfigured = false;
 1007  
 1008  	auto mapArray = Utils::String::split(mapping, ',', true);
 1009  	for (auto tt : mapArray)
 1010  	{
 1011  		size_t pos = tt.find(':');
 1012  		if (pos == std::string::npos) 
 1013  			continue;
 1014  
 1015  		std::string key = tt.substr(0, pos);
 1016  		std::string value = tt.substr(pos + 1);
 1017  
 1018  		auto inputName = _sdlToEsMapping.find(key);
 1019  		if (inputName == _sdlToEsMapping.cend())
 1020  		{
 1021  			// Fields that are part of a valid SDL mapping but that ES does not use. They are present
 1022  			// in almost every gamecontrollerdb entry, so reporting them as errors only pollutes the log.
 1023  			static const std::set<std::string> ignoredKeys =
 1024  			{
 1025  				"platform", "crc", "hint", "sdk", "guide", "touchpad",
 1026  				"paddle1", "paddle2", "paddle3", "paddle4",
 1027  				"misc1", "misc2", "misc3", "misc4", "misc5", "misc6"
 1028  			};
 1029  
 1030  			if (ignoredKeys.count(key) == 0)
 1031  				LOG(LogError) << "[InputDevice] Unknown mapping: " << key;
 1032  
 1033  			continue;
 1034  		}
 1035  
 1036  		int valueSign = 1;
 1037  		int idx = 0;
 1038  				
 1039  		switch (value[idx])
 1040  		{
 1041  		case '-': 
 1042  			valueSign = -1;
 1043  			idx++;
 1044  			break;
 1045  		case '+': 
 1046  			idx++;
 1047  			break;
 1048  		}
 1049  
 1050  		Input input;
 1051  		input.device = config->getDeviceId();
 1052  		input.type = InputType::TYPE_COUNT;
 1053  		input.configured = false;		
 1054  
 1055  		switch (value[idx])
 1056  		{
 1057  		case 'a':
 1058  			{
 1059  				input.type = InputType::TYPE_AXIS;
 1060  				input.id = Utils::String::toInteger(value.substr(idx + 1));				
 1061  				input.value = 1 * valueSign;
 1062  				input.configured = true;
 1063  
 1064  				// Invert directions for these mappings
 1065  				if (inputName->second == "joystick1up" || inputName->second == "joystick1left" || inputName->second == "joystick2up" || inputName->second == "joystick2left")
 1066  					input.value *= -1;
 1067  			}
 1068  			break;
 1069  		case 'b':
 1070  			{
 1071  				input.type = InputType::TYPE_BUTTON;
 1072  				input.id = Utils::String::toInteger(value.substr(idx + 1));
 1073  				input.value = 1;
 1074  				input.configured = true;
 1075  			}
 1076  			break;
 1077  		case 'h':
 1078  			{
 1079  				auto hatIds = Utils::String::split(value.substr(idx + 1), '.', true);
 1080  				if (hatIds.size() > 1)
 1081  				{
 1082  					input.type = InputType::TYPE_HAT;
 1083  					input.id = Utils::String::toInteger(hatIds[0]);
 1084  					input.value = Utils::String::toInteger(hatIds[1]);
 1085  					input.configured = true;
 1086  				}
 1087  			}
 1088  			break;
 1089  		}
 1090  
 1091  		if (input.configured)
 1092  		{
 1093  			// BATOCERA : Uncomment the next line using a patch to compute the code
 1094  			// input.computeCode();
 1095  			
 1096  			config->mapInput(inputName->second, input);
 1097  			isConfigured = true;
 1098  		}
 1099  	}
 1100  
 1101  	if (isConfigured)
 1102  	{
 1103  		// Use select button if hotkey is undefined
 1104  		Input tmp;
 1105  		if (!config->getInputByName("hotkey", &tmp))
 1106  			if (config->getInputByName("select", &tmp))
 1107  				config->mapInput("hotkey", tmp);
 1108  	}
 1109  
 1110  	return isConfigured;
 1111  }
 1112  
 1113  bool InputManager::loadInputConfig(InputConfig* config)
 1114  {
 1115  	std::string path = getConfigPath();
 1116  
 1117  #if WIN32
 1118  	// Find exact device
 1119  	if (tryLoadInputConfig(path, config, false))
 1120  		return true;
 1121  #else
 1122  	// Find exact device
 1123  	if (tryLoadInputConfig(path, config, false))
 1124  		return true;
 1125  
 1126  	// Find system exact device
 1127  	std::string sharedPath = Paths::getEmulationStationPath() + "/es_input.cfg";
 1128  	if (tryLoadInputConfig(sharedPath, config, false))
 1129  		return true;
 1130  
 1131  	// Find user Approximative device
 1132  	if (tryLoadInputConfig(path, config, true))
 1133  		return true;
 1134  
 1135  	// Find system Approximative device
 1136  	if (tryLoadInputConfig(sharedPath, config, true))
 1137  		return true;
 1138  #endif
 1139  
 1140  	return false;
 1141  }
 1142  
 1143  //used in an "emergency" where no keyboard config could be loaded from the inputmanager config file
 1144  //allows the user to select to reconfigure in menus if this happens without having to delete es_input.cfg manually
 1145  void InputManager::loadDefaultKBConfig()
 1146  {
 1147  	InputConfig* cfg = getInputConfigByDevice(DEVICE_KEYBOARD);
 1148  
 1149  	cfg->clear();
 1150  	cfg->mapInput("up", Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_UP, 1, true));
 1151  	cfg->mapInput("down", Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_DOWN, 1, true));
 1152  	cfg->mapInput("left", Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_LEFT, 1, true));
 1153  	cfg->mapInput("right", Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_RIGHT, 1, true));
 1154  
 1155  	cfg->mapInput(BUTTON_OK, Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_RETURN, 1, true));
 1156  	cfg->mapInput(BUTTON_BACK, Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_ESCAPE, 1, true));
 1157  	cfg->mapInput("start", Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_F1, 1, true));
 1158  	cfg->mapInput("select", Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_F2, 1, true));
 1159  
 1160  	cfg->mapInput("leftshoulder", Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_RIGHTBRACKET, 1, true));
 1161  	cfg->mapInput("rightshoulder", Input(DEVICE_KEYBOARD, TYPE_KEY, SDLK_LEFTBRACKET, 1, true));
 1162  }
 1163  
 1164  void InputManager::loadDefaultGunConfig()
 1165  {
 1166  #ifdef HAVE_UDEV
 1167  	InputConfig* cfg = getInputConfigByDevice(DEVICE_GUN);
 1168  
 1169  	cfg->clear();
 1170  	cfg->mapInput("up",    Input(DEVICE_GUN, TYPE_BUTTON, BTN_5, 1, true));
 1171  	cfg->mapInput("down",  Input(DEVICE_GUN, TYPE_BUTTON, BTN_6, 1, true));
 1172  	cfg->mapInput("left",  Input(DEVICE_GUN, TYPE_BUTTON, BTN_7, 1, true));
 1173  	cfg->mapInput("right", Input(DEVICE_GUN, TYPE_BUTTON, BTN_8, 1, true));
 1174  	cfg->mapInput("start",  Input(DEVICE_GUN, TYPE_BUTTON, BTN_MIDDLE, 1, true));
 1175  	cfg->mapInput("select", Input(DEVICE_GUN, TYPE_BUTTON, BTN_1, 1, true));
 1176  #endif
 1177  }
 1178  
 1179  void InputManager::writeDeviceConfig(InputConfig* config)
 1180  {
 1181  	assert(initialized());
 1182  
 1183  	std::string path = getConfigPath();
 1184  
 1185  	pugi::xml_document doc;
 1186  
 1187  	if (Utils::FileSystem::exists(path))
 1188  	{
 1189  		// merge files
 1190  		pugi::xml_parse_result result = doc.load_file(WINSTRINGW(path).c_str());
 1191  		if (!result)
 1192  		{
 1193  			LOG(LogError) << "Error parsing input config: " << result.description();
 1194  		}
 1195  		else
 1196  		{
 1197  			// successfully loaded, delete the old entry if it exists
 1198  			pugi::xml_node root = doc.child("inputList");
 1199  			if (root)
 1200  			{				
 1201  				pugi::xml_node oldEntry(NULL);
 1202  				for (pugi::xml_node item = root.child("inputConfig"); item; item = item.next_sibling("inputConfig")) 
 1203  				{
 1204  					if (strcmp(config->getDeviceGUIDString().c_str(), item.attribute("deviceGUID").value()) == 0
 1205  #if !WIN32
 1206  						&& strcmp(config->getDeviceName().c_str(), item.attribute("deviceName").value()) == 0
 1207  #endif
 1208  						) 
 1209  					{
 1210  						oldEntry = item;
 1211  						break;
 1212  					}
 1213  				}
 1214  				if (oldEntry)
 1215  					root.remove_child(oldEntry);
 1216  			}
 1217  		}
 1218  	}
 1219  
 1220  	pugi::xml_node root = doc.child("inputList");
 1221  	if(!root)
 1222  		root = doc.append_child("inputList");
 1223  
 1224  	config->writeToXML(root);
 1225  	doc.save_file(WINSTRINGW(path).c_str());
 1226          
 1227  	/* create a es_last_input.cfg so that people can easily share their config */
 1228  	pugi::xml_document lastdoc;
 1229  	pugi::xml_node lastroot = lastdoc.append_child("inputList");
 1230  	config->writeToXML(lastroot);
 1231  	std::string lastpath = getTemporaryConfigPath();
 1232  	lastdoc.save_file(WINSTRINGW(lastpath).c_str());
 1233  
 1234  	Scripting::fireEvent("config-changed");
 1235  	Scripting::fireEvent("controls-changed");
 1236  	
 1237  	// execute any onFinish commands and re-load the config for changes
 1238  	doOnFinish();
 1239  	loadInputConfig(config);
 1240  }
 1241  
 1242  void InputManager::doOnFinish()
 1243  {
 1244  	if (!initialized())
 1245  		return;
 1246  
 1247  	std::string path = getConfigPath();
 1248  	pugi::xml_document doc;
 1249  
 1250  	if(Utils::FileSystem::exists(path))
 1251  	{
 1252  		pugi::xml_parse_result result = doc.load_file(WINSTRINGW(path).c_str());
 1253  		if(!result)
 1254  		{
 1255  			LOG(LogError) << "Error parsing input config: " << result.description();
 1256  		}
 1257  		else
 1258  		{
 1259  			pugi::xml_node root = doc.child("inputList");
 1260  			if(root)
 1261  			{
 1262  				root = root.find_child_by_attribute("inputAction", "type", "onfinish");
 1263  				if(root)
 1264  				{
 1265  					for(pugi::xml_node command = root.child("command"); command;
 1266  							command = command.next_sibling("command"))
 1267  					{
 1268  						std::string tocall = command.text().get();
 1269  
 1270  						LOG(LogInfo) << "	" << Utils::String::maskSecrets(tocall);
 1271  						std::cout << "==============================================\ninput config finish command:\n";						
 1272  						int exitCode = Utils::Platform::ProcessStartInfo(tocall).run();
 1273  						std::cout << "==============================================\n";
 1274  
 1275  						if(exitCode != 0)
 1276  						{
 1277  							LOG(LogWarning) << "...launch terminated with nonzero exit code " << exitCode << "!";
 1278  						}
 1279  					}
 1280  				}
 1281  			}
 1282  		}
 1283  	}
 1284  }
 1285  
 1286  std::string InputManager::getConfigPath()
 1287  {
 1288  	return Paths::getUserEmulationStationPath() + "/es_input.cfg";
 1289  }
 1290  
 1291  std::string InputManager::getTemporaryConfigPath()
 1292  {
 1293  	return Paths::getUserEmulationStationPath() + "/es_last_input.cfg";
 1294  }
 1295  
 1296  bool InputManager::initialized() const
 1297  {
 1298  	return mKeyboardInputConfig != NULL;
 1299  }
 1300  
 1301  int InputManager::getNumConfiguredDevices()
 1302  {
 1303  	int num = 0;
 1304  
 1305  	for(auto it = mInputConfigs.cbegin(); it != mInputConfigs.cend(); it++)
 1306  		if(it->second && it->second->isConfigured())
 1307  			num++;
 1308  
 1309  	if (mKeyboardInputConfig && mKeyboardInputConfig->isConfigured())
 1310  		num++;
 1311  
 1312  	if (mCECInputConfig && mCECInputConfig->isConfigured())
 1313  		num++;
 1314  
 1315  	// Mouse input is hardcoded & not configurable with es_input.cfg
 1316  	// Gun input is hardcoded & not configurable with es_input.cfg
 1317  
 1318  	return num;
 1319  }
 1320  
 1321  void InputManager::computeLastKnownPlayersDeviceIndexes() 
 1322  {
 1323  	std::map<int, InputConfig*> playerJoysticks = computePlayersConfigs();
 1324  
 1325  	m_lastKnownPlayersDeviceIndexes.clear();
 1326  	for (int player = 0; player < MAX_PLAYERS; player++)
 1327  	{
 1328  		auto playerJoystick = playerJoysticks[player];
 1329  		if (playerJoystick != nullptr)
 1330  		{
 1331  			PlayerDeviceInfo dev;
 1332  			dev.index = playerJoystick->getDeviceIndex();
 1333  			dev.batteryLevel = playerJoystick->getBatteryLevel();
 1334  			dev.isWheel = playerJoystick->isWheel();
 1335  
 1336  			m_lastKnownPlayersDeviceIndexes[player] = dev;
 1337  		}
 1338  	}
 1339  }
 1340  
 1341  std::map<int, InputConfig*> InputManager::computePlayersConfigs()
 1342  {
 1343  	std::unique_lock<std::mutex> lock(mJoysticksLock);
 1344  
 1345  	// 1. Recuperer les configurated
 1346  	std::vector<InputConfig *> availableConfigured;
 1347  	for (auto conf : mInputConfigs)
 1348  		if (conf.second != nullptr && conf.second->isConfigured())
 1349  			availableConfigured.push_back(conf.second);
 1350  
 1351  	// sort available configs
 1352  	// Two joysticks belonging to the same physical board can end up with the same path, so fall
 1353  	// back on the device index to keep a deterministic order across reboots, otherwise std::sort
 1354  	// would swap the players randomly.
 1355  	std::sort(availableConfigured.begin(), availableConfigured.end(), [](InputConfig* a, InputConfig* b) -> bool
 1356  	{
 1357  		std::string pathA = a->getSortDevicePath();
 1358  		std::string pathB = b->getSortDevicePath();
 1359  
 1360  		if (pathA != pathB)
 1361  			return pathA < pathB;
 1362  
 1363  		return a->getDeviceIndex() < b->getDeviceIndex();
 1364  	});
 1365  
 1366  	// 2. Pour chaque joueur verifier si il y a un configurated
 1367  	// associer le input au joueur
 1368  	// enlever des disponibles
 1369  	std::map<int, InputConfig*> playerJoysticks;
 1370  
 1371  	// First loop, search for PATH. Ultra High Priority
 1372  	for (int player = 0; player < MAX_PLAYERS; player++)
 1373  	{
 1374  		std::string playerConfigPath = Settings::getInstance()->getString(Utils::String::format("INPUT P%iPATH", player + 1));
 1375  		if (!playerConfigPath.empty())
 1376  		{
 1377  			for (auto it1 = availableConfigured.begin(); it1 != availableConfigured.end(); ++it1)
 1378  			{
 1379  				InputConfig* config = *it1;
 1380  				if (playerConfigPath == config->getSortDevicePath())
 1381  				{
 1382  					availableConfigured.erase(it1);
 1383  					playerJoysticks[player] = config;
 1384  					break;
 1385  				}
 1386  			}
 1387  		}
 1388  	}
 1389  
 1390  	// First loop, search for GUID + NAME. High Priority
 1391  	for (int player = 0; player < MAX_PLAYERS; player++) 
 1392  	{
 1393  		if (playerJoysticks.find(player) != playerJoysticks.cend())
 1394  			continue;
 1395  
 1396  		std::string playerConfigName = Settings::getInstance()->getString(Utils::String::format("INPUT P%iNAME", player + 1));
 1397  		std::string playerConfigGuid = Settings::getInstance()->getString(Utils::String::format("INPUT P%iGUID", player + 1));
 1398  
 1399  		for (auto it1 = availableConfigured.begin(); it1 != availableConfigured.end(); ++it1)
 1400  		{
 1401  			InputConfig* config = *it1;
 1402  			if (playerConfigName == config->getDeviceName() && playerConfigGuid == config->getDeviceGUIDString())
 1403  			{
 1404  				availableConfigured.erase(it1);
 1405  				playerJoysticks[player] = config;
 1406  				break;
 1407  			}
 1408  		}
 1409  	}
 1410  
 1411  	// Second loop, search for NAME. Low Priority
 1412  	for (int player = 0; player < MAX_PLAYERS; player++) 
 1413  	{
 1414  		if (playerJoysticks.find(player) != playerJoysticks.cend())
 1415  			continue;
 1416  
 1417  		std::string playerConfigName = Settings::getInstance()->getString(Utils::String::format("INPUT P%dNAME", player + 1));
 1418  
 1419  		for (auto it1 = availableConfigured.begin(); it1 != availableConfigured.end(); ++it1)
 1420  		{
 1421  			InputConfig * config = *it1;
 1422  			if (playerConfigName == config->getDeviceName())
 1423  			{
 1424  				availableConfigured.erase(it1);
 1425  				playerJoysticks[player] = config;
 1426  				break;
 1427  			}
 1428  		}
 1429  	}
 1430  
 1431  	// Last loop, search for free controllers for remaining players.
 1432  	for (int player = 0; player < MAX_PLAYERS; player++) 
 1433  	{
 1434  		if (playerJoysticks.find(player) != playerJoysticks.cend())
 1435  			continue;
 1436  
 1437  		// si aucune config a été trouvé pour le joueur, on essaie de lui filer un libre
 1438  		for (auto it1 = availableConfigured.begin(); it1 != availableConfigured.end(); ++it1)
 1439  		{
 1440  			playerJoysticks[player] = *it1;
 1441  			availableConfigured.erase(it1);
 1442  			break;
 1443  		}
 1444  	}
 1445  
 1446  	// in case of hole (player 1 missing, but player 4 set, fill the holes with last players joysticks)
 1447  	for (int player = 0; player < MAX_PLAYERS; player++) 
 1448  	{
 1449  		if (playerJoysticks.find(player) != playerJoysticks.cend())
 1450  			continue;
 1451  
 1452  		for (int repplayer = MAX_PLAYERS; repplayer > player; repplayer--) 
 1453  		{
 1454  			if (playerJoysticks[player] == NULL && playerJoysticks[repplayer] != NULL) 
 1455  			{
 1456  				playerJoysticks[player] = playerJoysticks[repplayer];
 1457  				playerJoysticks[repplayer] = NULL;
 1458  			}
 1459  		}		
 1460  	}
 1461  
 1462  	for (int player = 0; player < MAX_PLAYERS; player++)
 1463  	{
 1464  		auto it = playerJoysticks.find(player);
 1465  		if (it == playerJoysticks.cend() || it->second == nullptr)
 1466  			continue;
 1467  
 1468  		LOG(LogInfo) << "computePlayersConfigs : Player " << player << " => " << it->second->getDevicePath();
 1469  	}
 1470  
 1471  	return playerJoysticks;
 1472  }
 1473  
 1474  std::string InputManager::configureEmulators() {
 1475    std::map<int, InputConfig*> playerJoysticks = computePlayersConfigs();
 1476    std::stringstream command;
 1477  
 1478    for (int player = 0; player < MAX_PLAYERS; player++) {
 1479      InputConfig * playerInputConfig = playerJoysticks[player];
 1480      if(playerInputConfig != NULL){
 1481        command << " -p" << player+1 << "index "      << playerInputConfig->getDeviceIndex();
 1482        command << " -p" << player+1 << "guid "       << playerInputConfig->getDeviceGUIDString();
 1483        command << " ";
 1484      }
 1485    }
 1486    LOG(LogInfo) << "Configure emulators command : " << Utils::String::maskSecrets(command.str());
 1487    return command.str();
 1488  }
 1489  
 1490  void InputManager::updateBatteryLevel(int id, const std::string& device, const std::string& devicePath, int level)
 1491  {
 1492  	bool changed = false;
 1493  
 1494  	mJoysticksLock.lock();
 1495  
 1496  	for (auto joy : mJoysticks) 
 1497  	{
 1498  		InputConfig* config = getInputConfigByDevice(joy.first);
 1499  		if (config != NULL && config->isConfigured())
 1500  		{
 1501  			if (!devicePath.empty())
 1502  			{
 1503  				if (Utils::String::compareIgnoreCase(config->getDevicePath(), devicePath) == 0)
 1504  				{
 1505  					config->updateBatteryLevel(level);
 1506  					changed = true;
 1507  				}
 1508  			}
 1509  			else
 1510  			{
 1511  				if (Utils::String::compareIgnoreCase(config->getDeviceGUIDString(), device) == 0)
 1512  				{
 1513  					config->updateBatteryLevel(level);
 1514  					changed = true;
 1515  				}
 1516  			}
 1517  		}
 1518  	}
 1519  
 1520  	mJoysticksLock.unlock();
 1521  
 1522  	if (changed)
 1523  		computeLastKnownPlayersDeviceIndexes();
 1524  }
 1525  
 1526  std::vector<InputConfig*> InputManager::getInputConfigs()
 1527  {
 1528  	std::vector<InputConfig*> ret;
 1529  
 1530  	std::map<int, InputConfig*> playerJoysticks = computePlayersConfigs();
 1531  
 1532  	for (int player = 0; player < MAX_PLAYERS; player++)
 1533  	{
 1534  		auto playerJoystick = playerJoysticks[player];
 1535  		if (playerJoystick != nullptr && playerJoystick->isConfigured())
 1536  			ret.push_back(playerJoystick);
 1537  	}
 1538  
 1539  	return ret;
 1540  }
 1541  
 1542  void InputManager::updateGuns(Window* window)
 1543  {
 1544  	if (mGunManager)
 1545  		mGunManager->updateGuns(window);
 1546  }
 1547  
 1548  void InputManager::sendMouseClick(Window* window, int button)
 1549  {
 1550  	window->input(getInputConfigByDevice(DEVICE_MOUSE), Input(DEVICE_MOUSE, TYPE_BUTTON, button, true, false));
 1551  	window->input(getInputConfigByDevice(DEVICE_MOUSE), Input(DEVICE_MOUSE, TYPE_BUTTON, button, false, false));
 1552  }
```

## src/Log.cpp (whole, fork-modified, at the pin)

```text
    1  #include "Log.h"
    2  #include "LogPolicy.h"
    3  
    4  #include "utils/FileSystemUtil.h"
    5  #include "utils/Platform.h"
    6  #include "Settings.h"
    7  #include "Paths.h"
    8  
    9  #include <iostream>
   10  #include <mutex>
   11  #include <SDL_timer.h>
   12  #include <iomanip> 
   13  #include <fstream>
   14  #include <iomanip>
   15  #include <csignal>
   16  
   17  #include <thread>
   18  #include <condition_variable>
   19  
   20  #if WIN32
   21  #include <Windows.h>
   22  #endif
   23  
   24  LogLevel Log::mReportingLevel = (LogLevel) -1;
   25  bool     Log::mEnabled = false;
   26  
   27  static thread_local std::ostringstream tl_stream;
   28  
   29  class AsyncLogger
   30  {
   31  public:
   32      static AsyncLogger& instance()
   33      {
   34          static AsyncLogger inst;
   35          return inst;
   36      }
   37  
   38      struct Entry
   39      {
   40          LogLevel    level;
   41          std::string msg;  
   42      };
   43  
   44      void open(const std::string& path, LogLevel level, bool debugToStderr)
   45      {
   46          mFile.open(path, std::ios::out | std::ios::trunc);
   47          if (!mFile.is_open()) 
   48          {
   49              std::cerr << "[Log] Cannot open: " << path << "\n";
   50              return;
   51          }
   52  
   53          mBufA.reserve(256);
   54          mBufB.reserve(256);
   55  
   56          mLevel.store(level, std::memory_order_relaxed);
   57          mDebugToStderr = debugToStderr;
   58          mShutdown = false;
   59          mEnabled.store(true, std::memory_order_release);
   60          mThread = std::thread(&AsyncLogger::workerLoop, this);
   61      }
   62  
   63      void close()
   64      {
   65          if (!mEnabled.load(std::memory_order_acquire)) 
   66              return;
   67  
   68          mEnabled.store(false, std::memory_order_release);
   69          {
   70              std::lock_guard<std::mutex> lk(mMutex);
   71              mShutdown = true;
   72          }
   73  
   74          mCV.notify_one();
   75  
   76          if (mThread.joinable()) 
   77              mThread.join();
   78  
   79          drainBuffer();
   80          mFile.flush();
   81          mFile.close();
   82      }
   83  
   84      void emergencyFlush()
   85      {
   86          if (!mEnabled.load(std::memory_order_acquire))
   87              return;
   88  
   89          if (!mFile.is_open())
   90              return;
   91  
   92          mEmergency.store(true, std::memory_order_release);
   93          mCV.notify_one();
   94  
   95          for (int i = 0; i < 200 && mEmergency.load(std::memory_order_acquire); ++i)
   96              std::this_thread::sleep_for(std::chrono::microseconds(50));
   97  
   98          mFile.flush();
   99      }
  100  
  101      void enqueue(LogLevel level, std::string&& msg)
  102      {
  103          {
  104              std::lock_guard<std::mutex> lk(mMutex);
  105              mWriteBuf->push_back({ level, std::move(msg) });
  106          }
  107          mCV.notify_one();
  108      }
  109  
  110      void     setLevel(LogLevel l) { mLevel.store(l, std::memory_order_relaxed); }
  111      LogLevel getLevel()     const { return mLevel.load(std::memory_order_relaxed); }
  112      bool     isEnabled()    const { return mEnabled.load(std::memory_order_relaxed); }
  113  
  114  private:
  115      AsyncLogger() : mWriteBuf(&mBufA), mDrainBuf(&mBufB) {}
  116  
  117      void workerLoop()
  118      {
  119          while (true)
  120          {
  121              {
  122                  std::unique_lock<std::mutex> lk(mMutex);
  123                  mCV.wait(lk, [this] 
  124                      {
  125                      return !mWriteBuf->empty()
  126                          || mShutdown
  127                          || mEmergency.load(std::memory_order_acquire);
  128                      });
  129                  
  130                  std::swap(mWriteBuf, mDrainBuf);
  131              }
  132  
  133              drainBuffer();
  134  
  135              // Every batch reaches the file before the worker sleeps again
  136              // (fork #178). It used to be one flush in eight batches, which on
  137              // an idle carousel left a line waiting for seven more wakes -- up
  138              // to 100 s observed -- and a WARNING, with no second channel,
  139              // waiting nowhere else. A flush is one write(2) of the buffered
  140              // bytes to /var/log (a bind mount of /storage/.cache/log: page
  141              // cache, no fsync), on this thread and never the render thread.
  142              // Measured on a GENERIC_X64 guest at Info: about 195 lines in the
  143              // first two seconds of boot, then a line every few seconds on the
  144              // carousel. The worker coalesces what arrives while it writes, so
  145              // flushes a second never exceed wakes a second; a hundred
  146              // write(2)s in the busiest second of boot is nothing worth saving.
  147              mFile.flush();
  148  
  149              if (mEmergency.load(std::memory_order_acquire))
  150                  mEmergency.store(false, std::memory_order_release);
  151  
  152              if (mShutdown) break;
  153          }
  154      }
  155  
  156      void drainBuffer()
  157      {
  158          for (const auto& e : *mDrainBuf)
  159              writeLine(e);
  160  
  161          mDrainBuf->clear();
  162      }
  163  
  164      void writeLine(const Entry& e)
  165      {
  166          mFile << e.msg << '\n';
  167  
  168          if (LogPolicy::mirrorToStderr(e.level, mDebugToStderr))
  169          {
  170  #if WIN32
  171              OutputDebugStringA(e.msg.c_str());
  172              OutputDebugStringA("\n");
  173  #else
  174              std::cerr << e.msg << '\n';
  175  #endif
  176          }
  177      }
  178  
  179      std::ofstream  mFile;
  180      std::thread    mThread;
  181  
  182      // Double buffer
  183      std::vector<Entry>  mBufA, mBufB;
  184      std::vector<Entry>* mWriteBuf;
  185      std::vector<Entry>* mDrainBuf;
  186  
  187      std::mutex              mMutex;
  188      std::condition_variable mCV;
  189      bool                    mShutdown{ false };
  190      bool                    mDebugToStderr{ false };
  191  
  192      std::atomic<LogLevel>   mLevel{ LogInfo };
  193      std::atomic<bool>       mEnabled{ false };
  194      std::atomic<bool>       mEmergency{ false };
  195  
  196  };
  197  
  198  static inline uint64_t getOsThreadId()
  199  {
  200  #if defined(_WIN32)
  201      return static_cast<uint64_t>(GetCurrentThreadId());
  202  #elif defined(__linux__)
  203      return static_cast<uint64_t>(::gettid());
  204  #elif defined(__APPLE__)
  205      uint64_t tid;
  206      pthread_threadid_np(nullptr, &tid);
  207      return tid;
  208  #else
  209      return static_cast<uint64_t>(::pthread_self());
  210  #endif
  211  }
  212  
  213  std::ostringstream& Log::stream()
  214  {
  215      auto now = std::chrono::system_clock::now();
  216      auto tt = std::chrono::system_clock::to_time_t(now);
  217      struct tm tm_buf {};
  218  #if WIN32
  219      localtime_s(&tm_buf, &tt);
  220  #else
  221      localtime_r(&tt, &tm_buf);
  222  #endif
  223      tl_stream << std::put_time(&tm_buf, "%F %T") << '\t';
  224  
  225      tl_stream << "[" << std::to_string(getOsThreadId()) << "]\t";
  226  
  227      tl_stream << LogPolicy::levelTag(mLevel) << '\t';
  228      return tl_stream;
  229  }
  230  
  231  Log::Log(LogLevel level) : mLevel(level)
  232  {
  233      tl_stream.str("");
  234      tl_stream.clear();    
  235  }
  236  
  237  static void crashHandler(int sig)
  238  {
  239      AsyncLogger::instance().emergencyFlush();
  240      signal(sig, SIG_DFL);
  241      raise(sig);
  242  }
  243  
  244  void Log::init()
  245  {
  246      AsyncLogger::instance().close();
  247  
  248      LogLevel lvl = LogInfo;
  249      if (Settings::getInstance()->getBool("Debug"))
  250      {
  251          lvl = LogDebug;
  252      }
  253      else
  254      {
  255          lvl = (LogLevel) LogPolicy::parseLogLevel(Settings::getInstance()->getString("LogLevel"));
  256      }
  257  
  258      auto base = Paths::getLogPath() + "/es_log";
  259      auto logPath = base + ".txt";
  260  
  261      if ((int)lvl < 0)
  262      {
  263          Utils::FileSystem::removeFile(logPath);
  264          mEnabled = false;
  265          return;
  266      }
  267  
  268      static constexpr int kMaxArchives = 4; // Keep 5 logs ( current + 4 latest )
  269  
  270      Utils::FileSystem::removeFile(base + "." + std::to_string(kMaxArchives - 1) + ".txt");
  271  
  272      for (int i = kMaxArchives - 2; i >= 0; --i)
  273      {
  274          Utils::FileSystem::renameFile(
  275              base + "." + std::to_string(i) + ".txt",
  276              base + "." + std::to_string(i + 1) + ".txt", true);
  277      }
  278  
  279      Utils::FileSystem::renameFile(logPath, base + ".0.txt", true);
  280  
  281      // signal(SIGSEGV, crashHandler); // It's already managed by main()
  282      signal(SIGABRT, crashHandler);
  283  
  284  #ifndef WIN32
  285      signal(SIGTERM, crashHandler);
  286  #endif
  287  
  288      bool debugToStderr = (lvl >= LogDebug);
  289      AsyncLogger::instance().open(logPath, lvl, debugToStderr);
  290  
  291      mReportingLevel = lvl;
  292      mEnabled = true;
  293  }
  294  
  295  void Log::flush()
  296  {
  297      AsyncLogger::instance().emergencyFlush();
  298  }
  299  
  300  void Log::close()
  301  {
  302      mEnabled = false;
  303      AsyncLogger::instance().close();
  304  }
  305  
  306  Log::~Log()
  307  {
  308      AsyncLogger::instance().enqueue(mLevel, tl_stream.str());
  309  }
  310  
  311  StopWatch::StopWatch(const std::string& elapsedMillisecondsMessage, LogLevel level)
  312  { 
  313  	mMessage = elapsedMillisecondsMessage; 
  314  	mLevel = level;
  315  	mStartTicks = SDL_GetTicks();
  316  }
  317  
  318  StopWatch::~StopWatch()
  319  {
  320  	int elapsed = SDL_GetTicks() - mStartTicks;
  321  	LOG(mLevel) << mMessage << " " << elapsed << "ms";
  322  }
```

## src/LogPolicy.h (whole, fork-added, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_LOG_POLICY_H
    3  #define ES_CORE_LOG_POLICY_H
    4  
    5  // The log's pure rules, kept apart from Log.cpp's file, thread and Settings
    6  // so a unit test can hold them (es-app/tests/unit/LogPolicyTests.cpp, fork
    7  // #178). The shape of a line is a contract: tools/vm-qa and the fork's proofs
    8  // grep es_log.txt for the level tags, so a word here is a word nothing else
    9  // may change.
   10  
   11  #include "Log.h"
   12  
   13  #include <string>
   14  
   15  namespace LogPolicy
   16  {
   17  	// The word a line carries for its level -- byte for byte what the file
   18  	// has always held.
   19  	inline const char* levelTag(LogLevel level)
   20  	{
   21  		switch (level)
   22  		{
   23  		case LogError:   return "ERROR";
   24  		case LogWarning: return "WARNING";
   25  		case LogDebug:   return "DEBUG";
   26  		default:         return "INFO";
   27  		}
   28  	}
   29  
   30  	// The LogLevel setting as Log::init reads it: "debug", "information",
   31  	// "warning" (Settings.cpp's default, what a device runs at), "error";
   32  	// no setting at all is "error"; any other word turns the log off (-1).
   33  	// The Debug switch overrides all of this, but that is Settings'
   34  	// business, not this rule's.
   35  	inline int parseLogLevel(const std::string& setting)
   36  	{
   37  		if (setting == "debug")       return LogDebug;
   38  		if (setting == "information") return LogInfo;
   39  		if (setting == "warning")     return LogWarning;
   40  		if (setting == "error")       return LogError;
   41  		if (setting.empty())          return LogError;
   42  		return -1;
   43  	}
   44  
   45  	// Which lines also go to stderr -- on a device, the journal: ERROR and
   46  	// WARNING always (fork #178: a warning used to have the file alone, and
   47  	// the file used to be eight batches late), and every line when the level
   48  	// is debug, as before.
   49  	inline bool mirrorToStderr(LogLevel level, bool debugToStderr)
   50  	{
   51  		return level <= LogWarning || debugToStderr;
   52  	}
   53  }
   54  
   55  #endif // ES_CORE_LOG_POLICY_H
```

## src/MameNames.cpp `:1-14` (an excerpt, upstream-carried, at the pin)

```text
    1  #include "MameNames.h"
    2  
    3  #include "resources/ResourceManager.h"
    4  #include "utils/FileSystemUtil.h"
    5  #include "Log.h"
    6  #include <pugixml/src/pugixml.hpp>
    7  #include "utils/StringUtil.h"
    8  #include <string.h>
    9  
   10  MameNames* MameNames::sInstance = nullptr;
   11  
   12  void MameNames::init()
   13  {
   14  	if(!sInstance)
```

## src/Paths.cpp `:11-56` (an excerpt, upstream-carried, at the pin)

```text
   11  
   12  #ifdef WIN32
   13  #define SETTINGS_FILENAME "emulatorLauncher.cfg"
   14  #else
   15  #define SETTINGS_FILENAME "emulationstation.ini"
   16  #endif
   17  
   18  
   19  
   20  
   21  Paths::Paths()
   22  {	
   23  
   24  #ifdef BATOCERA
   25  	LOG(LogInfo) << "BATOCERA is defined";
   26  #else
   27  	LOG(LogInfo) << "BATOCERA is NOT defined";
   28  #endif
   29  
   30  	mEmulationStationPath = getExePath();
   31  	mUserEmulationStationPath = Utils::FileSystem::getCanonicalPath(getHomePath() + "/.emulationstation");
   32  	mRootPath = Utils::FileSystem::getParent(getHomePath());
   33  
   34  	mLogPath = mUserEmulationStationPath;
   35  	mThemesPath = mUserEmulationStationPath + "/themes";
   36  	mMusicPath = mUserEmulationStationPath + "/music";
   37  	mKeyboardMappingsPath = mUserEmulationStationPath + "/padtokey";
   38  	mUserManualPath = mUserEmulationStationPath + "/notice.pdf";
   39  
   40  #if defined(WIN32) && defined(_DEBUG)
   41  	mSystemConfFilePath = mUserEmulationStationPath + "/batocera.conf";
   42  #endif
   43  
   44  	loadCustomConfiguration(false); // Try to detect alternate paths ( Decorations, Shaders... ) without loading overrides
   45  
   46  	// Here, BATOCERA & Forks can define their own paths
   47  
   48  #if BATOCERA
   49  	mRootPath = "/userdata";
   50  	mEmulationStationPath = "/usr/share/emulationstation";
   51  	mUserEmulationStationPath = "/userdata/system/configs/emulationstation";
   52  
   53  	mLogPath = "/userdata/system/logs";
   54  	mScreenShotsPath = "/userdata/screenshots";
   55  	mSaveStatesPath = "/userdata/saves";
   56  	mMusicPath = "/usr/share/batocera/music";
```

## src/Paths.cpp `:68-84` (an excerpt, upstream-carried, at the pin)

```text
   68  	mUserRetroachivementSounds = "/userdata/sounds/retroachievements";
   69  	
   70  	mSystemConfFilePath = "/userdata/system/batocera.conf";
   71  	mUserManualPath = "/usr/share/batocera/doc/notice.pdf";
   72  	mVersionInfoPath = "/usr/share/batocera/batocera.version";
   73  	mKodiPath = "/usr/bin/kodi";
   74  #endif
   75  
   76  #if defined(ROCKNIX)
   77  	mRootPath = "/storage";
   78  	mEmulationStationPath = getExePath();
   79  	mUserEmulationStationPath = "/storage/.config/emulationstation";
   80  
   81  	mLogPath = "/var/log";
   82  	mScreenShotsPath = "/storage/roms/screenshots";
   83  	mSaveStatesPath = "/storage/roms/savestates";
   84  	mMusicPath = mUserEmulationStationPath + "/music";
```

## src/Paths.cpp `:88-106` (an excerpt, upstream-carried, at the pin)

```text
   88  	mDecorationsPath = "/storage/roms/bezels";
   89  	mUserDecorationsPath = "/tmp/overlays/bezels";
   90  	mTimeZonesPath = "/usr/share/zoneinfo";
   91  	mRetroachivementSounds = "/usr/share/libretro/sounds";
   92  	mUserRetroachivementSounds = "/storage/roms/music/retroachievements";
   93  
   94  	mSystemConfFilePath = "/storage/.config/system/configs/system.cfg";
   95  #endif
   96  
   97  /* EmuElec sample locations.
   98  #ifdef _ENABLEEMUELEC
   99  	mRootPath = "/storage/roms"; // ?
  100  	mEmulationStationPath = Utils::FileSystem::getExePath();
  101  	mUserEmulationStationPath = Utils::FileSystem::getCanonicalPath(Utils::FileSystem::getHomePath() + "/.emulationstation");
  102  	mLogPath = "/storage/.config/emuelec/logs";
  103  	mThemesPath = mEmulationStationPath + "/themes";
  104  	mUserThemesPath = "/emuelec/themes";
  105  	mMusicPath = "/storage/roms/BGM";
  106  	mUserMusicPath = "/storage/.config/emuelec/BGM";
```

## src/Paths.cpp `:152-168` (an excerpt, upstream-carried, at the pin)

```text
  152  	};
  153  
  154  	std::map<std::string, std::string> ret;
  155  
  156  	std::string path = mEmulationStationPath + std::string("/") + SETTINGS_FILENAME;
  157  	if (!Utils::FileSystem::exists(path))
  158  		path = mUserEmulationStationPath + std::string("/") + SETTINGS_FILENAME;
  159  	if (!Utils::FileSystem::exists(path))
  160  		path = Utils::FileSystem::getParent(mUserEmulationStationPath) + std::string("/") + SETTINGS_FILENAME;
  161  
  162  	if (!Utils::FileSystem::exists(path))
  163  		return;
  164  		
  165  	std::string relativeTo = Utils::FileSystem::getParent(path);
  166  
  167  	if (!overridesOnly)
  168  	{
```

## src/Paths.cpp `:221-239` (an excerpt, upstream-carried, at the pin)

```text
  221  					if (Utils::FileSystem::isDirectory(dir))
  222  						ret[variable] = dir;
  223  				}
  224  			}
  225  		}
  226  
  227  		for (auto var : files)
  228  		{
  229  			auto file = Utils::FileSystem::resolveRelativePath(var.first, relativeTo, true);
  230  			if (Utils::FileSystem::exists(file) && !Utils::FileSystem::isDirectory(file))
  231  				ret[var.first] = file;
  232  		}
  233  	}
  234  	else
  235  	{
  236  		std::string line;
  237  		std::ifstream systemConf(path);
  238  		if (systemConf && systemConf.is_open())
  239  		{
```

## src/Paths.cpp `:270-295` (an excerpt, upstream-carried, at the pin)

```text
  270  	{
  271  		auto it = ret.find(vv.first);
  272  		if (it == ret.cend())
  273  			continue;
  274  
  275  		(*vv.second) = it->second;
  276  	}
  277  }
  278  
  279  static std::string homePath;
  280  
  281  std::string& Paths::getHomePath()
  282  {
  283  	if (homePath.length())
  284  		return homePath;
  285  
  286  #ifdef WIN32
  287  	// Is it a portable installation ? Check if ".emulationstation/es_systems.cfg" exists in the exe's path
  288  	if (!homePath.length())
  289  	{
  290  		std::string portableCfg = getExePath() + "/.emulationstation/es_systems.cfg";
  291  		if (Utils::FileSystem::exists(portableCfg))
  292  			homePath = getExePath();
  293  	}
  294  #endif
  295  
```

## src/Scripting.cpp (whole, fork-modified, at the pin)

```text
    1  #include "Scripting.h"
    2  #include "Log.h"
    3  #include "utils/Platform.h"
    4  #include "utils/FileSystemUtil.h"
    5  #include "utils/StringUtil.h"
    6  #include "utils/VectorEx.h"
    7  #include "Paths.h"
    8  #include <thread>
    9  #include <set>
   10  #include <map>
   11  #include <mutex>
   12  
   13  using namespace Utils::Platform;
   14  
   15  namespace Scripting
   16  {
   17  #if WIN32
   18      static std::thread*                 mScriptQueueThread = nullptr;
   19      static std::list<std::string>       mScriptQueue;
   20      static std::mutex			        mScriptQueueLock;
   21      static std::condition_variable		mScriptQueueEvent;
   22      static bool                         mExitScriptQueue = false;
   23  
   24      static void executeCommandsThread()
   25      {
   26          while (true)
   27          {
   28              // Wait for an event to say there is something in the queue
   29              std::unique_lock<std::mutex> lock(mScriptQueueLock);
   30              mScriptQueueEvent.wait(lock, []() { return mExitScriptQueue || !mScriptQueue.empty(); });
   31  
   32              if (mExitScriptQueue)
   33                  break;
   34  
   35              if (!mScriptQueue.empty())
   36              {
   37                  auto command = mScriptQueue.front();
   38                  mScriptQueue.pop_front();
   39  
   40                  lock.unlock();
   41                  std::this_thread::yield();
   42  
   43                  ProcessStartInfo psi;
   44                  psi.command = command;
   45                  psi.waitForExit = false;
   46                  psi.showWindow = false;
   47                  psi.run();
   48  
   49                  LOG(LogDebug) << "  executing: " << Utils::String::maskSecrets(command);
   50  
   51                  std::this_thread::yield();
   52              }
   53          }
   54      }
   55  
   56      static std::string _lastCommand;
   57  
   58      static void pushCommand(const std::string& command)
   59      {
   60          std::unique_lock<std::mutex> lock(mScriptQueueLock);
   61  
   62          if (command == _lastCommand && _lastCommand.find("-selected") != std::string::npos)
   63              return;
   64  
   65          _lastCommand = command;
   66  
   67          if (mScriptQueueThread == nullptr)
   68              mScriptQueueThread = new std::thread(&executeCommandsThread);
   69  
   70          mScriptQueue.push_back(command);
   71          mScriptQueueEvent.notify_one();
   72      }
   73  #endif
   74  
   75      void exitScriptingEngine()
   76      {
   77  #if WIN32
   78          std::unique_lock<std::mutex> lock(mScriptQueueLock);
   79          mExitScriptQueue = true;
   80          mScriptQueueEvent.notify_one();
   81  #endif
   82      }
   83  
   84      static std::set<std::string> _asyncEvents = { "game-start", "game-end", "game-selected", "system-selected", "screensaver-start", "screensaver-stop", "sleep", "wake" };
   85  
   86      static inline bool isAsyncEvent(const std::string& eventName) { return _asyncEvents.find(eventName) != _asyncEvents.cend(); }
   87  
   88      static void executeScript(const std::string& script, const std::string& eventName, const std::string& arg1, const std::string& arg2, const std::string& arg3, bool allowAsync = true)
   89      {
   90          std::string command = script;
   91  
   92          if (script.find(" ") != std::string::npos)
   93              command = "\"" + script + "\"";
   94  
   95          if (!eventName.empty())
   96              command += " " + eventName;
   97  
   98          for (auto arg : { arg1, arg2, arg3 })
   99          {
  100              if (arg.empty())
  101                  break;
  102  
  103              std::string data = arg;
  104              if (Utils::String::startsWith(data, "\"") && Utils::String::startsWith(data, "\""))
  105                  data = Utils::String::replace(data.substr(1, data.size() - 2), "\"", "");
  106  
  107              data = Utils::String::replace(data, "\"", "");
  108  
  109              if (data.find(" ") != std::string::npos)
  110                  command += " \"" + data + "\"";
  111              else
  112                  command += " " + data;
  113          }
  114  
  115  #if WIN32
  116          if (Utils::FileSystem::getExtension(script) == ".ps1")
  117              command = "powershell " + command;
  118  
  119          std::string stem = Utils::FileSystem::getStem(script);       
  120          if ((allowAsync && !Utils::String::endsWith(stem, "-wait")) || (eventName != "quit" && Utils::String::endsWith(stem, "-nowait")))
  121          {            
  122              LOG(LogDebug) << "  queuing: " << Utils::String::maskSecrets(command);
  123  
  124              // Start using a thread to avoid lags
  125              pushCommand(command);
  126          }
  127          else
  128          {
  129              LOG(LogDebug) << "  executing: " << Utils::String::maskSecrets(command);
  130  
  131              ProcessStartInfo psi;
  132              psi.command = command;
  133              psi.waitForExit = true;
  134              psi.showWindow = false;
  135              psi.run();
  136          }       
  137  #else            
  138          LOG(LogDebug) << "  executing: " << script;
  139  
  140          ProcessStartInfo psi;
  141          psi.command = command;
  142          psi.waitForExit = (eventName == "quit");
  143          psi.showWindow = false;
  144          // Don't clobber game logs when running scripts
  145          psi.stderrFilename = "es_script_stderr.log";
  146          psi.stdoutFilename = "es_script_stdout.log";
  147          psi.run();
  148  #endif
  149      }
  150  
  151      static std::set<std::string> _supportedExtensions = { ".exe", ".cmd", ".bat", ".ps1", ".sh", ".py" };
  152  
  153      void fireEvent(const std::string& eventName, const std::string& arg1, const std::string& arg2, const std::string& arg3)
  154      {
  155          LOG(LogDebug) << "fireEvent: " << eventName << " " << arg1 << " " << arg2 << " " << arg3;
  156  
  157          // Process splitted paths scripts
  158          std::vector<std::string> scriptDirList =
  159          {
  160              Paths::getUserEmulationStationPath() + "/scripts/" + eventName,
  161              Paths::getEmulationStationPath() + "/scripts/" + eventName,
  162  #ifndef WIN32
  163              "/var/run/emulationstation/scripts/" + eventName
  164  #endif
  165          };
  166  
  167          for (auto dir : VectorHelper::distinct(scriptDirList, [](auto x) { return x; }))
  168          {
  169              auto scripts = Utils::FileSystem::getDirContent(dir);
  170              for (auto script : scripts)
  171              {
  172  #if WIN32
  173                  auto ext = Utils::String::toLower(Utils::FileSystem::getExtension(script));
  174                  if (_supportedExtensions.find(ext) == _supportedExtensions.cend())
  175                      continue;
  176  #endif
  177                  executeScript(script, "", arg1, arg2, arg3, isAsyncEvent(eventName));
  178              }
  179          }
  180  
  181          // Process single scripts. This type of scripts are called with the event name as 1st arg
  182          std::vector<std::string> paths =
  183          {
  184              Paths::getUserEmulationStationPath() + "/scripts",
  185              Paths::getEmulationStationPath() + "/scripts",
  186  #ifndef WIN32
  187              "/var/run/emulationstation/scripts"
  188  #endif
  189          };
  190  
  191          for (auto dir : VectorHelper::distinct(paths, [](auto x) { return x; }))
  192          {
  193              if (!Utils::FileSystem::exists(dir))
  194                  continue;
  195  
  196              for (auto script : Utils::FileSystem::getDirectoryFiles(dir))
  197              {
  198                  if (script.directory)
  199                      continue;
  200  
  201                  auto ext = Utils::String::toLower(Utils::FileSystem::getExtension(script.path));
  202                  if (_supportedExtensions.find(ext) == _supportedExtensions.cend())
  203                      continue;
  204  
  205                  executeScript(script.path, eventName, arg1, arg2, arg3, isAsyncEvent(eventName));
  206              }
  207          }
  208      }
  209  } // Scripting::
```

## src/Splash.cpp `:95-111` (an excerpt, upstream-carried, at the pin)

```text
   95  	if (useOldSplashLayout)
   96  		mText.setColor(0xFFFFFFD0);
   97  	else
   98  		mText.setColor(0xFFFFFFFF);
   99  
  100  	mText.setHorizontalAlignment(ALIGN_CENTER);
  101  	mText.setFont(font);
  102  
  103  #ifdef BATOCERA
  104  	if (fullScreenBackGround)
  105  		mText.setPosition(0, Renderer::getScreenHeight() * 0.83f);
  106  	else
  107  		mText.setPosition(0, Renderer::getScreenHeight() * 0.86f);
  108  #else
  109  	if (fullScreenBackGround)
  110  		mText.setPosition(0, Renderer::getScreenHeight() * 0.78f);
  111  	else
```

## src/Splash.cpp `:323-337` (an excerpt, upstream-carried, at the pin)

```text
  323  	for (auto extra : mExtras)
  324  		if (extra->getZIndex() >= 10)
  325  			extra->render(trans);
  326  
  327  	if (swapBuffers)
  328  	{
  329  		Renderer::swapBuffers();
  330  
  331  #if defined(_WIN32)
  332  		// Avoid Window Freezing on Windows
  333  		SDL_Event event;
  334  		while (SDL_PollEvent(&event));
  335  #endif
  336  	}
  337  }
```

## src/Splash.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  
    3  #include <string>
    4  #include "components/ImageComponent.h"
    5  #include "components/TextComponent.h"
    6  
    7  class Window;
    8  class TextureResource;
    9  
   10  #if defined(ROCKNIX)
   11  #define DEFAULT_SPLASH_IMAGE ":/pixelelated-wordmark.svg"
   12  #define OLD_SPLASH_LAYOUT true
   13  #elif WIN32
   14  #define DEFAULT_SPLASH_IMAGE ":/splash.svg"
   15  #define OLD_SPLASH_LAYOUT true
   16  #else
   17  #define DEFAULT_SPLASH_IMAGE ":/logo.png"
   18  #define OLD_SPLASH_LAYOUT false
   19  #endif
   20  
   21  class Splash
   22  {
   23  public:
   24  	Splash(Window* window, const std::string image, bool fullScreenBackGround = true, IBindable* bindable = nullptr);
   25  	~Splash();
   26  
   27  	void update(std::string text, float percent = -1);
   28  	void render(float opacity, bool swapBuffers = true);
   29  
   30  private:
   31  	ImageComponent  mBackground;
   32  	TextComponent   mText;
   33  	float			mPercent;
   34  
   35  	ImageComponent  mInactiveProgressbar;
   36  	ImageComponent  mActiveProgressbar;
   37  
   38  	unsigned int	mBackgroundColor;
   39  	float			mRoundCorners;
   40  
   41  	std::shared_ptr<TextureResource> mTexture;
   42  
   43  	std::vector<GuiComponent*> mExtras;
   44  } ;
```

## src/TextToSpeech.cpp `:1-9` (an excerpt, upstream-carried, at the pin)

```text
    1  #include "TextToSpeech.h"
    2  #include "Log.h"
    3  #include "LocaleES.h"
    4  
    5  #if WIN32
    6  #include "SystemConf.h"
    7  #include <sapi.h>
    8  #include <sphelper.h>
    9  #include <thread>
```

## src/TextToSpeech.cpp `:19-61` (an excerpt, upstream-carried, at the pin)

```text
   19  	HRESULT hr = CoCreateInstance(CLSID_SpVoice, NULL, CLSCTX_ALL, IID_ISpVoice, (void **)&pVoice);
   20  	if (!SUCCEEDED(hr))
   21  		return;
   22  
   23  	m_isAvailable = true;
   24  	
   25  	while (true)
   26  	{
   27  		std::unique_lock<std::mutex> lock(mMutex);
   28  		mEvent.wait(lock, [this]() { return mShouldTerminate || !mSpeechQueue.empty(); });
   29  
   30  		if (mShouldTerminate)
   31  			break;
   32  
   33  		SpeakItem* item = nullptr;
   34  
   35  		if (!mSpeechQueue.empty())
   36  		{
   37  			item = mSpeechQueue.front();
   38  			mSpeechQueue.pop_front();
   39  		}
   40  
   41  		lock.unlock();
   42  
   43  		if (item != nullptr)
   44  		{
   45  			pVoice->Speak(Utils::String::convertToWideString(item->text).c_str(), SPF_ASYNC | SPF_IS_XML | (item->expand ? 0 : SPF_PURGEBEFORESPEAK), NULL);
   46  			delete item;
   47  		}
   48  	}
   49  
   50  	pVoice->Pause();
   51  	pVoice->Release();
   52  }
   53  #elif defined(_ENABLE_TTS_)
   54  #include <espeak/speak_lib.h>
   55  #endif
   56  
   57  std::weak_ptr<TextToSpeech> TextToSpeech::sInstance;
   58  
   59  TextToSpeech::TextToSpeech()
   60  {
   61  	m_isAvailable = false;
```

## src/TextToSpeech.cpp `:68-102` (an excerpt, upstream-carried, at the pin)

```text
   68  TextToSpeech::~TextToSpeech()
   69  {
   70  	deinit();
   71  }
   72  
   73  std::shared_ptr<TextToSpeech> & TextToSpeech::getInstance()
   74  {
   75  	//check if an TextToSpeech instance is already created, if not create one
   76  	static std::shared_ptr<TextToSpeech> sharedInstance = sInstance.lock();
   77  	if (sharedInstance == nullptr) 
   78  	{
   79  		sharedInstance.reset(new TextToSpeech);
   80  		sInstance = sharedInstance;
   81  	}
   82  	return sharedInstance;
   83  }
   84  
   85  void TextToSpeech::init()
   86  {
   87  	if (m_initialized)
   88  		return;
   89  
   90  #if WIN32
   91  	mShouldTerminate = false;
   92  	mSpeakThread = new std::thread(&TextToSpeech::SpeakThread, this);
   93  	m_initialized = true;
   94  #elif defined(_ENABLE_TTS_)	
   95  	m_isAvailable = espeak_Initialize(AUDIO_OUTPUT_PLAYBACK, 0, NULL, 0) != EE_INTERNAL_ERROR;
   96  	if (!m_isAvailable)
   97  		return;
   98  
   99  	m_initialized = true;
  100  
  101  	char* envv = getenv("LANGUAGE");
  102  	if (envv != nullptr && std::string(envv).length() >= 4) 
```

## src/TextToSpeech.cpp `:120-146` (an excerpt, upstream-carried, at the pin)

```text
  120  #if WIN32
  121  
  122  	if (mSpeakThread != nullptr)
  123  	{
  124  		mShouldTerminate = true;
  125  
  126  		mEvent.notify_all();
  127  
  128  		mSpeakThread->join();
  129  		delete mSpeakThread;
  130  		mSpeakThread = nullptr;
  131  	}
  132  
  133  	for (auto item : mSpeechQueue)
  134  		delete item;
  135  
  136  	mSpeechQueue.clear();
  137  
  138  #elif defined(_ENABLE_TTS_)
  139  	if (espeak_Terminate() != EE_OK) {
  140  		LOG(LogError) << "TTS::deinit() - Failed to terminate";
  141  	}
  142  #endif
  143  	m_initialized = false;
  144  }
  145  
  146  bool TextToSpeech::isAvailable()
```

## src/TextToSpeech.cpp `:169-185` (an excerpt, upstream-carried, at the pin)

```text
  169  
  170  		if (!m_initialized)
  171  			return;
  172  	}
  173  
  174  	if (m_isAvailable && playSay)
  175  	{
  176  		m_enabled = true; // Force
  177  		say(v ? _("SCREEN READER ENABLED") : _("SCREEN READER DISABLED"));
  178  	}
  179  
  180  	m_enabled = v;
  181  
  182  	if (!v)
  183  		deinit();
  184  }
  185  
```

## src/TextToSpeech.cpp `:189-205` (an excerpt, upstream-carried, at the pin)

```text
  189  	return m_enabled;
  190  }
  191  
  192  void TextToSpeech::setLanguage(const std::string language) 
  193  {
  194  	if (m_isAvailable == false)
  195  		return;
  196  
  197  #ifdef _ENABLE_TTS_
  198  	std::string voice = "default";
  199  	std::string language_part1 = language.substr(0, 5);
  200  
  201  	// espeak --voices
  202  	//if(language_part1 == "ar_YE") voice = "";
  203  	if (language_part1 == "ca_ES") voice = "catalan";
  204  	if (language_part1 == "cy_GB") voice = "welsh";
  205  	if (language_part1 == "de_DE") voice = "german";
```

## src/TextToSpeech.cpp `:248-276` (an excerpt, upstream-carried, at the pin)

```text
  248  	if (language.empty())
  249  		language = SystemConf::getInstance()->get("system.language");
  250  		
  251  	if (language.empty() || language == "en")
  252  		language = "en-US";
  253  
  254  	std::string full = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='" + language + "'>" + text + "</speak>";
  255  		
  256  	std::unique_lock<std::mutex> lock(mMutex);
  257  
  258  	if (!expand)
  259  		mSpeechQueue.clear();
  260  
  261  	SpeakItem* item = new SpeakItem();
  262  	item->text = full;
  263  	item->expand = expand;
  264  	mSpeechQueue.push_back(item);
  265  
  266  	mEvent.notify_one();
  267  
  268  #elif defined(_ENABLE_TTS_)
  269  
  270  	if (expand == false && espeak_IsPlaying() == 1)
  271  		espeak_Cancel();
  272  	
  273  	if (espeak_Synth(text.c_str(),
  274  		text.length() * 4 /* potentially 4 bytes by char */,
  275  		0,
  276  		POS_CHARACTER,
```

## src/TextToSpeech.h `:4-35` (an excerpt, upstream-carried, at the pin)

```text
    4  
    5  #include <string>
    6  #include <memory>
    7  
    8  #if WIN32
    9  #include <thread>
   10  #include <mutex>
   11  #include <list>
   12  #include <condition_variable>
   13  #endif
   14  
   15  /*!
   16  Singleton pattern. Call getInstance() to get an object.
   17  */
   18  class TextToSpeech
   19  {
   20  public:
   21  	~TextToSpeech();
   22  	static std::shared_ptr<TextToSpeech>& getInstance();
   23  
   24  	bool isAvailable();
   25  	bool isEnabled();
   26  	void enable(bool v, bool playSay = true);
   27  	bool toogle();
   28  
   29  	void setLanguage(const std::string language);
   30  	void say(const std::string text, bool expand = false, const std::string lang = "");
   31  
   32  private:
   33  	TextToSpeech();
   34  	
   35  	static std::weak_ptr<TextToSpeech> sInstance;
```

## src/TextToSpeech.h `:39-57` (an excerpt, upstream-carried, at the pin)

```text
   39  	bool m_enabled;
   40  
   41  	void init();
   42  	void deinit();
   43  
   44  #if WIN32
   45  	void SpeakThread();
   46  
   47  	std::thread*				mSpeakThread;
   48  	std::mutex					mMutex;
   49  	std::condition_variable		mEvent;
   50  	bool						mShouldTerminate;
   51  
   52  	class SpeakItem
   53  	{
   54  	public:
   55  		std::string text;
   56  		bool expand;
   57  	};
```

## src/ThemeData.cpp `:708-864` (an excerpt, upstream-carried, at the pin)

```text
  708  
  709  	mLanguage = Utils::String::toLower(language);
  710  }
  711  
  712  ThemeFileCache* ThemeFileCache::_instance;
  713  
  714  std::string& ThemeFileCache::getXmlDocument(const std::string& path)
  715  {
  716  	std::unique_lock<std::mutex> lock(_lock);
  717  
  718  	auto it = _cache.find(path);
  719  	if (it != _cache.cend())
  720  		return it->second;
  721  	/*
  722  	pugi::xml_document* doc = new pugi::xml_document();
  723  	pugi::xml_parse_result res = doc->load_file(WINSTRINGW(path).c_str());
  724  	if (!res)
  725  	{
  726  		ThemeException error;
  727  		throw error << "XML parsing error: \n    " << res.description();
  728  	}
  729  	*/
  730  	_cache[path] = Utils::FileSystem::readAllText(path);
  731  	std::string& buffer = _cache[path];	
  732  	return buffer;
  733  }
  734  
  735  void ThemeFileCache::clear()
  736  {
  737  	std::unique_lock<std::mutex> lock(_lock);
  738  	
  739  //	for (auto& item : _cache)
  740  //		delete item.second;
  741  
  742  	_cache.clear();
  743  }
  744  
  745  void ThemeData::loadFile(const std::string& system, const std::map<std::string, std::string>& sysDataMap, const std::string& path, bool fromFile)
  746  {
  747  	mPaths.push_back(path);
  748  
  749  	ThemeException error;
  750  	error.setFiles(mPaths);
  751  
  752  	if (fromFile && !Utils::FileSystem::exists(path))
  753  		throw error << "File does not exist!";
  754  	
  755  	mVersion = 0;
  756  	mViews.clear();
  757  
  758  	mSystemThemeFolder = system;
  759  
  760  	mVariables.clear();
  761  	mVariables.insert(sysDataMap.cbegin(), sysDataMap.cend());
  762  
  763  	mVariables["lang"] = mLanguage;
  764  	mVariables["global.language"] = mLangAndRegion;
  765  	mVariables["currentPath"] = Utils::FileSystem::getParent(mPaths.back());
  766  	mVariables["themePath"] = Utils::FileSystem::getParent(mPaths.back());
  767  	mVariables["region"] = mRegion;
  768  	mVariables["root"] = Utils::FileSystem::getParent(mPaths.back());
  769  
  770  	for (auto name : Settings::getInstance()->getSettingsNames())
  771  	{
  772  		if (name.find(".") != std::string::npos)
  773  			continue;
  774  
  775  		std::string variableName = "settings." + name;
  776  
  777  		SettingType type = Settings::getInstance()->getSettingType(name);
  778  		switch (type)
  779  		{
  780  		case SettingType::String:
  781  			mVariables[variableName] = Settings::getInstance()->getString(name);
  782  			break;
  783  		case SettingType::Bool:
  784  			mVariables[variableName] = Settings::getInstance()->getBool(name) ? "true" : "false";
  785  			break;
  786  		case SettingType::Int:
  787  			mVariables[variableName] = std::to_string(Settings::getInstance()->getInt(name));
  788  			break;
  789  		case SettingType::Float:
  790  			mVariables[variableName] = std::to_string(Settings::getInstance()->getFloat(name));
  791  			break;
  792  		}
  793  	}
  794  
  795  	for (auto var : mVariables)
  796  	{
  797  		if (var.first == "screen.height" || var.first == "screen.width")
  798  			mEvaluatorVariables[var.first] = Utils::String::toFloat(var.second);
  799  		else if (var.second == "true" || var.second == "false")
  800  			mEvaluatorVariables[var.first] = var.second == "true" ? 1 : 0;
  801  		else
  802  			mEvaluatorVariables[var.first] = var.second;		
  803  	}
  804  
  805  	pugi::xml_document doc;
  806  	
  807  	if (fromFile)
  808  	{
  809  		const std::string& xmlData = ThemeFileCache::getInstance().getXmlDocument(path);
  810  		doc.load_buffer(xmlData.c_str(), xmlData.size());
  811  	}
  812  	else
  813  	{
  814  		pugi::xml_parse_result res = fromFile ? doc.load_file(WINSTRINGW(path).c_str()) : doc.load_string(path.c_str());
  815  		if (!res)
  816  			throw error << "XML parsing error: \n    " << res.description();
  817  	}
  818  
  819  	pugi::xml_node root = doc.child("theme");
  820  	if(!root)
  821  		throw error << "Missing <theme> tag!";
  822  
  823  	// parse version
  824  	mVersion = root.child("formatVersion").text().as_float(-404);
  825  	if(mVersion == -404)
  826  		throw error << "<formatVersion> tag missing!\n   It's either out of date or you need to add <formatVersion>" << CURRENT_THEME_FORMAT_VERSION << "</formatVersion> inside your <theme> tag.";
  827  
  828  	if(mVersion < MINIMUM_THEME_FORMAT_VERSION)
  829  		throw error << "Theme uses format version " << mVersion << ". Minimum supported version is " << MINIMUM_THEME_FORMAT_VERSION << ".";
  830  		
  831  	parseSubsetsDefaults(root);
  832  	parseVariables(root);
  833  	parseTheme(root);
  834  	
  835  	std::string themeName = Utils::String::toLower(Settings::getInstance()->getString("ThemeSet"));
  836  	if (themeName.find("next-pixel") != std::string::npos || themeName.find("alekfull") != std::string::npos)
  837  	{
  838  		auto systemView = mViews.find("system");
  839  		if (systemView != mViews.cend())
  840  		{
  841  			auto systemcarousel = systemView->second.elements.find("systemcarousel");
  842  			if (systemcarousel != systemView->second.elements.cend())
  843  			{
  844  				auto defaultTransition = systemcarousel->second.properties.find("defaultTransition");
  845  				if (defaultTransition == systemcarousel->second.properties.cend() || defaultTransition->second.s == "instant")
  846  					systemcarousel->second.properties["defaultTransition"] = std::string("fade & slide");
  847  			}
  848  		}
  849  	}
  850  
  851  	if (system != "splash" && system != "imageviewer" && system != "default")
  852  	{
  853  		mMenuTheme = nullptr;
  854  		mDefaultTheme = this;
  855  	}
  856  }
  857  
  858  const std::shared_ptr<ThemeData::ThemeMenu>& ThemeData::getMenuTheme()
  859  {
  860  	if (mMenuTheme == nullptr)
  861  	{
  862  		if (mDefaultTheme != nullptr)
  863  			mMenuTheme = std::shared_ptr<ThemeData::ThemeMenu>(new ThemeMenu(mDefaultTheme));
  864  		else
```

## src/ThemeData.cpp `:1086-1158` (an excerpt, upstream-carried, at the pin)

```text
 1086  				return true;
 1087  			}
 1088  		}
 1089  	}
 1090  
 1091  	return false;
 1092  }
 1093  
 1094  void ThemeData::parseInclude(const pugi::xml_node& node)
 1095  {
 1096  	if (!parseFilterAttributes(node))
 1097  		return;
 1098  
 1099  	if (!parseSubset(node))
 1100  		return;
 1101  
 1102  	std::string relPath = resolvePlaceholders(node.text().as_string());
 1103  	if (relPath.empty())
 1104  		return;
 1105  
 1106  	std::string path = Utils::FileSystem::resolveRelativePath(resolveSystemVariable(mSystemThemeFolder, relPath), Utils::FileSystem::getParent(mPaths.back()), true);
 1107  
 1108  	if (!ResourceManager::getInstance()->fileExists(path))
 1109  	{
 1110  		if (relPath.find("$") != std::string::npos && relPath.find("${") == std::string::npos)
 1111  		{
 1112  			path = Utils::FileSystem::resolveRelativePath(resolveSystemVariable("default", relPath), Utils::FileSystem::getParent(mPaths.back()), true);
 1113  			if (ResourceManager::getInstance()->fileExists(path))
 1114  			{
 1115  				if (mPaths.size() == 1)
 1116  					mSystemThemeFolder = "default";
 1117  			}
 1118  			else
 1119  			{
 1120  				LOG(LogWarning) << "Included file \"" << relPath << "\" not found! (resolved to \"" << path << "\")";
 1121  				return;
 1122  			}
 1123  		}
 1124  		else
 1125  		{
 1126  			LOG(LogWarning) << "Included file \"" << relPath << "\" not found! (resolved to \"" << path << "\")";
 1127  			return;
 1128  		}
 1129  	}
 1130  
 1131  	appendFile(path);
 1132  	/*
 1133  	mPaths.push_back(path);
 1134  
 1135  	pugi::xml_document includeDoc;
 1136  	pugi::xml_parse_result result = includeDoc.load_file(WINSTRINGW(path).c_str());
 1137  	if (!result)
 1138  	{
 1139  		LOG(LogWarning) << "Error parsing file: \n    " << result.description() << "    from included file \"" << relPath << "\":\n    ";
 1140  		return;
 1141  	}
 1142  
 1143  	pugi::xml_node theme = includeDoc.child("theme");
 1144  	if (!theme)
 1145  	{
 1146  		LOG(LogWarning) << "Missing <theme> tag!" << "    from included file \"" << relPath << "\":\n    ";
 1147  		return;
 1148  	}
 1149  
 1150  	parseVariables(theme);
 1151  	parseTheme(theme);
 1152  
 1153  	mPaths.pop_back();
 1154  	*/	
 1155  }
 1156  
 1157  void ThemeData::parseFeature(const pugi::xml_node& node)
 1158  {
```

## src/ThemeData.h `:586-599` (an excerpt, upstream-carried, at the pin)

```text
  586  	}
  587  
  588  public:
  589  	std::string& getXmlDocument(const std::string& path);
  590  	void clear();
  591  
  592  private:
  593  	std::unordered_map<std::string, std::string> _cache;
  594  	std::mutex _lock;
  595  
  596  	static ThemeFileCache* _instance;
  597  };
  598  
  599  #endif // ES_CORE_THEME_DATA_H
```

## src/VolumeControl.cpp `:3-21` (an excerpt, upstream-carried, at the pin)

```text
    3  #include "math/Misc.h"
    4  #include "Log.h"
    5  #include "Settings.h"
    6  
    7  #ifdef WIN32
    8  #include <mmdeviceapi.h>
    9  #endif
   10  
   11  #ifdef _ENABLE_PULSE_
   12  #include <thread>
   13  #include <condition_variable>
   14  #include <pulse/pulseaudio.h>
   15  #include "utils/StringUtil.h"
   16  #include "SystemConf.h"
   17  
   18  class PulseAudioControl
   19  {
   20  #define DEFAULT_SINK_NAME "@DEFAULT_SINK@"
   21  
```

## src/VolumeControl.cpp `:24-40` (an excerpt, upstream-carried, at the pin)

```text
   24  	{
   25  		mContext = nullptr;
   26      	mMainLoop = nullptr;
   27  
   28  	  	mReady   = 0;
   29  		mMute    = 0;
   30  		mVolume  = 100;
   31  
   32  		mThread = new std::thread(&PulseAudioControl::run, this);
   33  		WaitEvent();
   34  
   35  		LOG(LogDebug) << "PulseAudioControl. Ready = " << mReady;
   36  	}
   37  
   38  	 ~PulseAudioControl()
   39  	{
   40  		exit();
```

## src/VolumeControl.cpp `:60-81` (an excerpt, upstream-carried, at the pin)

```text
   60  	}
   61  
   62  	void exit()
   63  	{
   64  		LOG(LogDebug) << "PulseAudioControl.exit";
   65  
   66  		mReady = false;
   67  
   68  		if(mThread != nullptr) {
   69  		  if (mMainLoop != nullptr) {
   70  		    pa_mainloop_quit(mMainLoop, 0);
   71  		  }
   72  		  mThread->join();
   73  		  mThread = nullptr;
   74  		}
   75  	}
   76  
   77  	void run()	
   78  	{
   79  		mMainLoop = pa_mainloop_new();
   80  		pa_mainloop_api* pa_mlapi = pa_mainloop_get_api(mMainLoop);
   81  
```

## src/VolumeControl.cpp `:191-277` (an excerpt, upstream-carried, at the pin)

```text
  191  
  192  	void FireEvent()
  193  	{
  194  		mEvent.notify_one();
  195  	}
  196  
  197  	void WaitEvent()
  198  	{
  199  		std::unique_lock<std::mutex> lock(mLock);
  200  		mEvent.wait(lock);
  201  	}
  202  
  203  	std::thread*	mThread;
  204  
  205  	std::mutex					mLock;
  206  	std::condition_variable		mEvent;		
  207  
  208  	pa_context* 	mContext;
  209      pa_mainloop* 	mMainLoop;
  210  };
  211  
  212  static PulseAudioControl PulseAudio;
  213  
  214  #endif
  215  
  216  #if defined(__linux__)
  217  #if defined(_RPI_) || defined(_VERO4K_)
  218  		std::string VolumeControl::mixerName = "PCM";
  219  #else
  220  		std::string VolumeControl::mixerName = "Master";
  221  #endif
  222  	std::string VolumeControl::mixerCard = "default";
  223  #endif
  224  
  225  std::weak_ptr<VolumeControl> VolumeControl::sInstance;
  226  
  227  
  228  VolumeControl::VolumeControl()
  229  	: internalVolume(0)
  230  #if defined (__APPLE__)
  231  	#error TODO: Not implemented for MacOS yet!!!
  232  #elif defined(__linux__)
  233  	, mixerIndex(0), mixerHandle(nullptr), mixerElem(nullptr), mixerSelemId(nullptr)
  234  #elif defined(WIN32) || defined(_WIN32)
  235  	, mixerHandle(nullptr), endpointVolume(nullptr)
  236  #endif
  237  {
  238  	init();
  239  }
  240  
  241  VolumeControl::~VolumeControl()
  242  {
  243  #ifdef _ENABLE_PULSE_
  244  	if (PulseAudio.isReady())
  245  		PulseAudio.exit();
  246  #endif
  247  
  248  	deinit();
  249  }
  250  
  251  std::shared_ptr<VolumeControl> & VolumeControl::getInstance()
  252  {
  253  	//check if an VolumeControl instance is already created, if not create one
  254  	static std::shared_ptr<VolumeControl> sharedInstance = sInstance.lock();
  255  	if (sharedInstance == nullptr) {
  256  		sharedInstance.reset(new VolumeControl);
  257  		sInstance = sharedInstance;
  258  	}
  259  	return sharedInstance;
  260  }
  261  
  262  void VolumeControl::init()
  263  {
  264  	//initialize audio mixer interface
  265  #if defined (__APPLE__)
  266  	#error TODO: Not implemented for MacOS yet!!!
  267  #elif defined(__linux__)
  268  
  269  #ifdef _ENABLE_PULSE_
  270  	// Read initial volume from systemconf
  271  	std::string volume = SystemConf::getInstance()->get("audio.volume");
  272  	PulseAudio.setVolume(volume.empty() ? 100 : Utils::String::toInteger(volume), false);
  273  	return;
  274  #endif
  275  
  276  	//try to open mixer device
  277  	if (mixerHandle == nullptr)
```

## src/VolumeControl.cpp `:370-386` (an excerpt, upstream-carried, at the pin)

```text
  370  				mixerHandle = nullptr;
  371  			}
  372  		}
  373  		else
  374  		{
  375  			LOG(LogError) << "VolumeControl::init() - Failed to open ALSA mixer!";
  376  		}
  377  	}
  378  #elif defined(WIN32) || defined(_WIN32)
  379  	//get windows version information
  380  	OSVERSIONINFOEXA osVer = {sizeof(OSVERSIONINFO)};
  381  	::GetVersionExA(reinterpret_cast<LPOSVERSIONINFOA>(&osVer));
  382  	//check windows version
  383  	if(osVer.dwMajorVersion < 6)
  384  	{
  385  		//Windows older than Vista. use mixer API. open default mixer
  386  		if (mixerHandle == nullptr)
```

## src/VolumeControl.cpp `:448-500` (an excerpt, upstream-carried, at the pin)

```text
  448  		}
  449  	}
  450  #endif
  451  }
  452  
  453  void VolumeControl::deinit()
  454  {
  455  	//deinitialize audio mixer interface
  456  #if defined (__APPLE__)
  457  	#error TODO: Not implemented for MacOS yet!!!
  458  #elif defined(__linux__)
  459  
  460  #ifdef _ENABLE_PULSE_
  461  	return;
  462  #endif
  463  
  464  	if (mixerHandle != nullptr) {
  465  		snd_mixer_detach(mixerHandle, mixerCard.c_str());
  466  		snd_mixer_free(mixerHandle);
  467  		snd_mixer_close(mixerHandle);
  468  		mixerHandle = nullptr;
  469  		mixerElem = nullptr;
  470  	}
  471  #elif defined(WIN32) || defined(_WIN32)
  472  	if (mixerHandle != nullptr) {
  473  		mixerClose(mixerHandle);
  474  		mixerHandle = nullptr;
  475  	}
  476  	else if (endpointVolume != nullptr) {
  477  		endpointVolume->Release();
  478  		endpointVolume = nullptr;
  479  		CoUninitialize();
  480  	}
  481  #endif
  482  }
  483  
  484  int VolumeControl::getVolume() const
  485  {
  486  	int volume = 0;
  487  
  488  #if defined (__APPLE__)
  489  	#error TODO: Not implemented for MacOS yet!!!
  490  #elif defined(__linux__)
  491  
  492  #ifdef _ENABLE_PULSE_
  493  	return PulseAudio.getVolume();	
  494  #endif
  495  
  496  	if (mixerElem != nullptr)
  497  	{
  498  		if (mixerHandle != nullptr)
  499  			snd_mixer_handle_events(mixerHandle);
  500  		/*
```

## src/VolumeControl.cpp `:525-541` (an excerpt, upstream-carried, at the pin)

```text
  525  				LOG(LogError) << "VolumeControl::getVolume() - Failed to get mixer volume!";
  526  			}
  527  		}
  528  		else
  529  		{
  530  			LOG(LogError) << "VolumeControl::getVolume() - Failed to get volume range!";
  531  		}
  532  	}
  533  #elif defined(WIN32) || defined(_WIN32)
  534  	if (mixerHandle != nullptr)
  535  	{
  536  		//Windows older than Vista. use mixer API. get volume from line control
  537  		MIXERCONTROLDETAILS_UNSIGNED value;
  538  		MIXERCONTROLDETAILS mixerControlDetails;
  539  		mixerControlDetails.cbStruct = sizeof(MIXERCONTROLDETAILS);
  540  		mixerControlDetails.dwControlID = mixerControl.dwControlID;
  541  		mixerControlDetails.cChannels = 1; //always 1 for a MIXERCONTROL_CONTROLF_UNIFORM control
```

## src/VolumeControl.cpp `:581-601` (an excerpt, upstream-carried, at the pin)

```text
  581  		volume = 0;
  582  	}
  583  	if (volume > 100)
  584  	{
  585  		volume = 100;
  586  	}
  587  	//store values in internal variables
  588  	internalVolume = volume;
  589  #if defined (__APPLE__)
  590  	#error TODO: Not implemented for MacOS yet!!!
  591  #elif defined(__linux__)
  592  
  593  #ifdef _ENABLE_PULSE_
  594  	if (PulseAudio.isReady())
  595  	{
  596  		PulseAudio.setVolume(volume);
  597  	}
  598  	return;
  599  #endif
  600  
  601  	if (mixerElem != nullptr)
```

## src/Window.cpp (whole, fork-modified, at the pin)

```text
    1  #include "Window.h"
    2  
    3  #include "components/HelpComponent.h"
    4  #include "components/ImageComponent.h"
    5  #include "components/TextComponent.h"
    6  #include "resources/Font.h"
    7  #include "resources/TextureResource.h"
    8  #include "InputManager.h"
    9  #include "Log.h"
   10  #include "Scripting.h"
   11  #include <algorithm>
   12  #include <iomanip>
   13  #include "guis/GuiInfoPopup.h"
   14  #include "SystemConf.h"
   15  #include "LocaleES.h"
   16  #include "AudioManager.h"
   17  #include <SDL_events.h>
   18  #include "ThemeData.h"
   19  #include <mutex>
   20  #include "components/AsyncNotificationComponent.h"
   21  #include "components/ControllerActivityComponent.h"
   22  #include "components/BatteryIndicatorComponent.h"
   23  #include "guis/GuiMsgBox.h"
   24  #include "components/VolumeInfoComponent.h"
   25  #include "Splash.h"
   26  #include "PowerSaver.h"
   27  #include "renderers/Renderer.h"
   28  #include <thread>
   29  #include "../es-app/src/ApiSystem.h"
   30  #include "utils/StringUtil.h"
   31  
   32  #if WIN32
   33  #include <SDL_syswm.h>
   34  #endif
   35  
   36  Window::Window() : mNormalizeNextUpdate(false), mFrameTimeElapsed(0), mFrameCountElapsed(0), mAverageDeltaTime(10),
   37    mAllowSleep(true), mSleeping(false), mTimeSinceLastInput(0), mScreenSaver(NULL), mRenderScreenSaver(false), mClockElapsed(0), mMouseCapture(nullptr), mMenuBackgroundShaderTextureCache(-1)
   38  {			
   39  	mTransitionOffset = 0;
   40  
   41  	mHelp = new HelpComponent(this);
   42  	mBackgroundOverlay = new ImageComponent(this);
   43  	mBackgroundOverlay->setImage(":/scroll_gradient.png"); 
   44  
   45  	mSplash = nullptr;
   46  	mLastShowCursor = -2;
   47  }
   48  
   49  Window::~Window()
   50  {
   51  	resetMenuBackgroundShader();
   52  
   53  	for (auto extra : mScreenExtras)
   54  		delete extra;
   55  
   56  	delete mBackgroundOverlay;
   57  
   58  	// delete all our GUIs
   59  	while(peekGui())
   60  		delete peekGui();
   61  
   62  	delete mHelp;
   63  }
   64  
   65  void Window::pushGui(GuiComponent* gui)
   66  {
   67  	resetMenuBackgroundShader();
   68  
   69  	if (mGuiStack.size() > 0)
   70  	{
   71  		auto& top = mGuiStack.back();
   72  		top->topWindow(false);		
   73  	}
   74  
   75  	hitTest(-1, -1);
   76  
   77  	gui->onShow();
   78  	mGuiStack.push_back(gui);
   79  	gui->updateHelpPrompts();
   80  }
   81  
   82  void Window::removeGui(GuiComponent* gui)
   83  {
   84  	resetMenuBackgroundShader();
   85  
   86  	if (mMouseCapture == gui)
   87  		mMouseCapture = nullptr;
   88  
   89  	for(auto i = mGuiStack.cbegin(); i != mGuiStack.cend(); i++)
   90  	{
   91  		if(*i == gui)
   92  		{						
   93  			gui->onHide();
   94  			i = mGuiStack.erase(i);
   95  
   96  			if(i == mGuiStack.cend() && mGuiStack.size()) // we just popped the stack and the stack is not empty
   97  			{
   98  				mGuiStack.back()->updateHelpPrompts();
   99  				mGuiStack.back()->topWindow(true);
  100  			}
  101  
  102  			return;
  103  		}
  104  	}
  105  }
  106  
  107  GuiComponent* Window::peekGui()
  108  {
  109  	if(mGuiStack.size() == 0)
  110  		return NULL;
  111  
  112  	return mGuiStack.back();
  113  }
  114  
  115  bool Window::init(bool initRenderer, bool initInputManager)
  116  {
  117  	LOG(LogInfo) << "Window::init";
  118  
  119  	if (initRenderer)
  120  	{
  121  		if (!Renderer::init())
  122  		{
  123  			LOG(LogError) << "Renderer failed to initialize!";
  124  			return false;
  125  		}
  126  	}
  127  	else 
  128  		Renderer::activateWindow();
  129  
  130  	if (initInputManager)
  131  		InputManager::getInstance()->init();
  132  
  133  	ResourceManager::getInstance()->reloadAll();
  134  
  135  	//keep a reference to the default fonts, so they don't keep getting destroyed/recreated
  136  	if(mDefaultFonts.empty())
  137  	{
  138  		mDefaultFonts.push_back(Font::get(FONT_SIZE_SMALL));
  139  		mDefaultFonts.push_back(Font::get(FONT_SIZE_MEDIUM));
  140  		mDefaultFonts.push_back(Font::get(FONT_SIZE_LARGE));
  141  		mDefaultFonts.push_back(Font::get(FONT_SIZE_MINI));
  142  	}
  143  
  144  	mBackgroundOverlay->setImage(":/scroll_gradient.png");
  145  	mBackgroundOverlay->setResize((float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
  146  
  147  	if (mClock == nullptr)
  148  	{
  149  		mClock = std::make_shared<TextComponent>(this);
  150  		mClock->setFont(Font::get(FONT_SIZE_SMALL));
  151  		mClock->setHorizontalAlignment(ALIGN_RIGHT);
  152  		mClock->setVerticalAlignment(ALIGN_TOP);
  153  		mClock->setPosition(Renderer::getScreenWidth()*0.94, Renderer::getScreenHeight()*0.9965 - Font::get(FONT_SIZE_SMALL)->getHeight());
  154  		mClock->setSize(Renderer::getScreenWidth()*0.05, 0);
  155  		mClock->setColor(0x777777FF);
  156  	}
  157  
  158  	if (mControllerActivity == nullptr)
  159  		mControllerActivity = std::make_shared<ControllerActivityComponent>(this);
  160  
  161  	if (mBatteryIndicator == nullptr)
  162  		mBatteryIndicator = std::make_shared<BatteryIndicatorComponent>(this);
  163  	
  164  	if (mVolumeInfo == nullptr)
  165  		mVolumeInfo = std::make_shared<VolumeInfoComponent>(this);
  166  	else
  167  		mVolumeInfo->reset();
  168  
  169  	// update our help because font sizes probably changed
  170  	if (peekGui())
  171  		peekGui()->updateHelpPrompts();
  172  
  173  	return true;
  174  }
  175  
  176  void Window::reactivateGui()
  177  {
  178  	for (auto extra : mScreenExtras)
  179  		extra->onShow();
  180  
  181  	for (auto i = mGuiStack.cbegin(); i != mGuiStack.cend(); i++)
  182  		(*i)->onShow();
  183  
  184  	if (peekGui())
  185  		peekGui()->updateHelpPrompts();
  186  }
  187  
  188  void Window::deinit(bool deinitRenderer)
  189  {
  190  	resetMenuBackgroundShader();
  191  
  192  	for (auto extra : mScreenExtras)
  193  		extra->onHide();
  194  
  195  	// Hide all GUI elements on uninitialisation - this disable
  196  	for(auto i = mGuiStack.cbegin(); i != mGuiStack.cend(); i++)
  197  		(*i)->onHide();
  198  
  199  	if (deinitRenderer)
  200  		InputManager::getInstance()->deinit();
  201  
  202  	TextureResource::clearQueue();
  203  	ResourceManager::getInstance()->unloadAll();
  204  
  205  	if (deinitRenderer)
  206  		Renderer::deinit();
  207  }
  208  
  209  void Window::textInput(const char* text)
  210  {
  211  	if(peekGui())
  212  		peekGui()->textInput(text);
  213  }
  214  
  215  void Window::input(InputConfig* config, Input input)
  216  {
  217  	if (config == nullptr)
  218  		return;
  219  	
  220  	if (config->getDeviceIndex() >= 0 && Settings::getInstance()->getBool("FirstJoystickOnly"))
  221  	{
  222  		// Find first player controller info
  223  		auto playerDevices = InputManager::getInstance()->lastKnownPlayersDeviceIndexes();
  224  		auto playerDevice = playerDevices.find(0); 
  225  		if (playerDevice != playerDevices.cend())
  226  		{
  227  			if (config->getDeviceIndex() != playerDevice->second.index)
  228  				return;
  229  		}
  230  		else if (config->getDeviceIndex() > 0) // Not found ? Use SDL device index
  231  			return;
  232  	}
  233  
  234  	if (mScreenSaver) 
  235  	{
  236  		if (mScreenSaver->isScreenSaverActive() && Settings::getInstance()->getBool("ScreenSaverControls") &&
  237  			((Settings::getInstance()->getString("ScreenSaverBehavior") == "slideshow") || 			
  238  			(Settings::getInstance()->getString("ScreenSaverBehavior") == "random video")))
  239  		{
  240  			if (config->isMappedLike("right", input) || config->isMappedTo("select", input))
  241  			{
  242  				if (input.value != 0) // handle screensaver control
  243  					mScreenSaver->nextVideo();
  244  					
  245  				mTimeSinceLastInput = 0;
  246  				return;
  247  			}
  248  			else if (config->isMappedTo("start", input) && input.value != 0 && mScreenSaver->getCurrentGame() != nullptr)
  249  			{
  250  				// launch game!				
  251  				cancelScreenSaver();
  252  				mScreenSaver->launchGame();
  253  				// to force handling the wake up process
  254  				mSleeping = true;
  255  			}
  256  		}
  257  	}
  258  
  259  	if (cancelScreenSaver())
  260  		return;
  261  
  262  	if (config->getDeviceId() == DEVICE_KEYBOARD && input.value && input.id == SDLK_g && SDL_GetModState() & KMOD_LCTRL) // && Settings::getInstance()->getBool("Debug"))
  263  	{
  264  		// toggle debug grid with Ctrl-G
  265  		Settings::setDebugGrid(!Settings::DebugGrid());
  266  	}
  267  	else if (config->getDeviceId() == DEVICE_KEYBOARD && input.value && input.id == SDLK_t && SDL_GetModState() & KMOD_LCTRL) // && Settings::getInstance()->getBool("Debug"))
  268  	{
  269  		// toggle TextComponent debug view with Ctrl-T
  270  		Settings::setDebugText(!Settings::DebugText());
  271  	}
  272  	else if (config->getDeviceId() == DEVICE_KEYBOARD && input.value && input.id == SDLK_i && SDL_GetModState() & KMOD_LCTRL) // && Settings::getInstance()->getBool("Debug"))
  273  	{
  274  		// toggle TextComponent debug view with Ctrl-I
  275  		Settings::setDebugImage(!Settings::DebugImage());
  276  	}
  277  	else if (config->getDeviceId() == DEVICE_KEYBOARD && input.value && input.id == SDLK_m && SDL_GetModState() & KMOD_LCTRL) // && Settings::getInstance()->getBool("Debug"))
  278  	{
  279  		// toggle TextComponent debug view with Ctrl-I
  280  		Settings::setDebugMouse(!Settings::DebugMouse());
  281  	}
  282  	else
  283  	{
  284  		if (mControllerActivity != nullptr)
  285  			mControllerActivity->input(config, input);
  286  
  287  		if (peekGui())
  288  			peekGui()->input(config, input); // this is where the majority of inputs will be consumed: the GuiComponent Stack
  289  	}
  290  }
  291  
  292  // Notification messages
  293  static std::mutex mNotificationMessagesLock;
  294  
  295  // The default duration of a toast, in ms: the "display titles" setting
  296  // within 2..120 s, else 10 s. Shared by displayNotificationMessage and the
  297  // re-queue in createAsyncNotificationComponent.
  298  static int notificationDuration(int duration)
  299  {
  300  	if (duration <= 0)
  301  	{
  302  		duration = Settings::getInstance()->getInt("audio.display_titles_time");
  303  		if (duration <= 2 || duration > 120)
  304  			duration = 10;
  305  
  306  		duration *= 1000;
  307  	}
  308  	return duration;
  309  }
  310  
  311  void Window::displayNotificationMessage(std::string message, int duration)
  312  {
  313  	std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
  314  
  315  	duration = notificationDuration(duration);
  316  
  317  	NotificationMessage msg;
  318  	msg.first = message;
  319  	msg.second = duration;
  320  	mNotificationMessages.push_back(msg);
  321  }
  322  
  323  
  324  void Window::processNotificationMessages()
  325  {
  326  	std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
  327  
  328  	if (mNotificationMessages.empty())
  329  		return;
  330  
  331  	// One floating surface at a time (fork #283, D-UI-093): a toast waits
  332  	// while a progress card is up -- both sit at the top centre, and the
  333  	// SENT toast drew over the sync card on a handheld -- and shows once
  334  	// the card has gone. Nothing is dropped; the order is the order things
  335  	// happened.
  336  	if (!mAsyncNotificationComponent.empty())
  337  		return;
  338  	
  339  	NotificationMessage msg = mNotificationMessages.back();
  340  	mNotificationMessages.pop_back();
  341  
  342  	LOG(LogDebug) << "Notification message :" << msg.first.c_str();
  343  	
  344  	if (mNotificationPopups.size() == 0)
  345  		PowerSaver::pause();
  346  
  347  	auto infoPopup = new GuiInfoPopup(this, msg.first, msg.second);
  348  	mNotificationPopups.push_back(infoPopup);
  349  
  350  	layoutNotificationPopups();
  351  }
  352  
  353  void Window::stopNotificationPopups()
  354  {
  355  	if (mNotificationPopups.size() == 0)
  356  		return;
  357  
  358  	for (auto ip : mNotificationPopups)
  359  		delete ip;
  360  
  361  	mNotificationPopups.clear();
  362  	PowerSaver::resume();
  363  }
  364  
  365  void Window::updateNotificationPopups(int deltaTime)
  366  {
  367  	bool changed = false;
  368  
  369  	for (int i = mNotificationPopups.size() - 1 ; i >= 0 ; i--)
  370  	{
  371  		mNotificationPopups[i]->update(deltaTime);
  372  
  373  		if (!mNotificationPopups[i]->isRunning())
  374  		{
  375  			delete mNotificationPopups[i];
  376  
  377  			auto it = mNotificationPopups.begin();
  378  			std::advance(it, i);
  379  			mNotificationPopups.erase(it);
  380  
  381  			changed = true;
  382  		}
  383  		else if (mNotificationPopups[i]->getFadeOut() != 0)
  384  			changed = true;
  385  	}
  386  
  387  	if (changed)
  388  	{
  389  		if (mNotificationPopups.size() == 0)
  390  			PowerSaver::resume();
  391  		else
  392  			layoutNotificationPopups();
  393  	}
  394  }
  395  
  396  void Window::layoutNotificationPopups()
  397  {
  398  	float posY = Renderer::getScreenHeight() * 0.02f;
  399  	int paddingY = (int)posY;
  400  
  401  	for (auto popup : mNotificationPopups)
  402  	{
  403  		float fadingOut = popup->getFadeOut();
  404  		if (fadingOut != 0)
  405  		{
  406  			// cubic ease in
  407  			fadingOut = fadingOut - 1;
  408  			fadingOut = Math::lerp(0, 1, fadingOut*fadingOut*fadingOut + 1);
  409  
  410  			posY -= (popup->getSize().y() + paddingY) * fadingOut;
  411  		}
  412  
  413  		popup->setPosition(popup->getPosition().x(), posY, 0);
  414  		posY += popup->getSize().y() + paddingY;
  415  	}
  416  }
  417  
  418  void Window::processSongTitleNotifications()
  419  {
  420  	if (AudioManager::getInstance()->songNameChanged())
  421  	{
  422  		if (Settings::getInstance()->getBool("audio.display_titles"))
  423  		{
  424  			std::string songName = AudioManager::getInstance()->getSongName();
  425  			if (!songName.empty())
  426  			{
  427  				std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
  428  
  429  				for (int i = mNotificationPopups.size() - 1; i >= 0; i--)
  430  				{
  431  					if (mNotificationPopups[i]->getMessage().find(_U("\uF028")) != std::string::npos)
  432  					{
  433  						delete mNotificationPopups[i];
  434  
  435  						auto it = mNotificationPopups.begin();
  436  						std::advance(it, i);
  437  						mNotificationPopups.erase(it);
  438  					}
  439  				}
  440  
  441  				lock.unlock();
  442  				displayNotificationMessage(_U("\uF028  ") + songName); // _("Now playing: ") + 
  443  			}
  444  		}
  445  
  446  		AudioManager::getInstance()->resetSongNameChangedFlag();
  447  	}	
  448  }
  449  
  450  void Window::update(int deltaTime)
  451  {
  452  	TextureResource::cleanupVRAM();
  453  
  454  	if (mLastShowCursor >= 0)
  455  	{
  456  		mLastShowCursor += deltaTime;
  457  		if (mLastShowCursor > 5000)
  458  		{
  459  			SDL_ShowCursor(0);
  460  			mLastShowCursor = -1;
  461  		}
  462  	}
  463  
  464  	processPostedFunctions();
  465  	processSongTitleNotifications();
  466  	processNotificationMessages();
  467  
  468  	if (mNormalizeNextUpdate)
  469  	{
  470  		mNormalizeNextUpdate = false;
  471  		if (deltaTime > mAverageDeltaTime)
  472  			deltaTime = mAverageDeltaTime;
  473  	}
  474  
  475  	for (auto extra : mScreenExtras)
  476  		extra->update(deltaTime);
  477  
  478  	if (mVolumeInfo)
  479  		mVolumeInfo->update(deltaTime);
  480  
  481  	mFrameTimeElapsed += deltaTime;
  482  	mFrameCountElapsed++;
  483  	if (mFrameTimeElapsed > 250)
  484  	{
  485  		mAverageDeltaTime = mFrameTimeElapsed / mFrameCountElapsed;
  486  
  487  		if (Settings::DrawFramerate())
  488  		{
  489  			std::stringstream ss;
  490  
  491  			// fps
  492  			ss << std::fixed << std::setprecision(1) << (1000.0f * (float)mFrameCountElapsed / (float)mFrameTimeElapsed) << "fps, ";
  493  			ss << std::fixed << std::setprecision(2) << ((float)mFrameTimeElapsed / (float)mFrameCountElapsed) << "ms";
  494  
  495  			// vram
  496  			float textureVramUsageMb = TextureResource::getTotalMemoryUsage(MemoryUsageType::VRAM) / 1024.0f / 1024.0f;
  497  			float textureKnownUsageMb = TextureResource::getTotalMemoryUsage(MemoryUsageType::Estimated) / 1024.0f / 1024.0f;
  498  			float textureCacheUsageMb = TextureResource::getTotalMemoryUsage(MemoryUsageType::RAM) / 1024.0f / 1024.0f;
  499  			float fontVramUsageMb = Font::getTotalMemoryUsage() / 1024.0f / 1024.0f;
  500  			size_t max_texture = Settings::getInstance()->getInt("MaxVRAM");
  501  
  502  			int queueSize = TextureResource::getQueueSize();
  503  
  504  			ss << "\nFont VRAM: " << fontVramUsageMb << " Tex VRAM: " << textureVramUsageMb << " Cached Tex RAM: " << textureCacheUsageMb << " Known Tex: " << textureKnownUsageMb << " Max VRAM: " << max_texture << " Queued : " << queueSize;
  505  			
  506  			mFrameDataText = std::unique_ptr<TextCache>(mDefaultFonts[3]->buildTextCache(ss.str(), Vector2f(50.f, 50.f), 0xFFFF40FF, 0.0f, ALIGN_LEFT, 1.2f));
  507  		}
  508  
  509  		mFrameTimeElapsed = 0;
  510  		mFrameCountElapsed = 0;
  511  	}
  512  
  513  	/* draw the clock */ 
  514  	if (Settings::DrawClock() && mClock) 
  515  	{
  516  		mClockElapsed -= deltaTime;
  517  		if (mClockElapsed <= 0)
  518  		{
  519  			time_t     clockNow = time(0);
  520  			struct tm  clockTstruct = *localtime(&clockNow);
  521  
  522  			if (clockTstruct.tm_year > 100) 
  523  			{ 
  524  				// Display the clock only if year is more than 1900+100 ; rpi have no internal clock and out of the networks, the date time information has no value
  525  				// Visit http://en.cppreference.com/w/cpp/chrono/c/strftime for more information about date/time format
  526  
  527  				std::string clockBuf;
  528  				if (Settings::ClockMode12())
  529  					clockBuf = Utils::Time::timeToString(clockNow, "%I:%M %p");
  530  				else
  531  					clockBuf = Utils::Time::timeToString(clockNow, "%H:%M");
  532  
  533  				mClock->setText(clockBuf);
  534  			}
  535  
  536  			mClockElapsed = 1000; // next update in 1000ms
  537  		}
  538  	}
  539  
  540  	mTimeSinceLastInput += deltaTime;
  541  
  542  	if (peekGui())
  543  		peekGui()->update(deltaTime);
  544  
  545  	// Update the screensaver
  546  	if (mScreenSaver)
  547  		mScreenSaver->update(deltaTime);
  548  
  549  	// update pads 
  550  	if (mControllerActivity)
  551  		mControllerActivity->update(deltaTime);
  552  
  553  	if (mBatteryIndicator)
  554  		mBatteryIndicator->update(deltaTime);
  555  
  556  	updateAsyncNotifications(deltaTime);
  557  	updateNotificationPopups(deltaTime);
  558  
  559  	AudioManager::update(deltaTime);
  560  }
  561  
  562  static std::vector<unsigned int> _gunAimColors = { 0xFFFFFF00, 0xFFFF00FF, 0xFF00FFFF, 0xFF0000FF, 0xFFFF0000, 0xFF00FF00 };
  563  
  564  void Window::renderSindenBorders()
  565  {
  566  	bool drawGunBorders = false;
  567  
  568  	for (auto gun : InputManager::getInstance()->getGuns())
  569  		if (gun->needBorders()) 
  570  			drawGunBorders = true;		
  571  
  572  	// normal (default) : draw borders when required
  573  	// hidden : the border are not displayed (assume that there are provided by an other way like bezels)
  574  	// force  : force even if no gun requires it (or even no gun at all)
  575  	// gameonly : borders are not visible in es, just in game (for boards having a sinden gun alway plugged in)
  576  	auto bordersMode = SystemConf::getInstance()->get("controllers.guns.bordersmode");
  577  	if (drawGunBorders)
  578  	  if(bordersMode == "hidden" || bordersMode == "gameonly")
  579  	    drawGunBorders = false;
  580  
  581  	if (!drawGunBorders)
  582  	  if(bordersMode == "force")
  583  	    // SETTING FOR DEBUGGING BORDERS
  584  	    drawGunBorders = true;
  585  
  586  	if (drawGunBorders && !mRenderScreenSaver)
  587  	{
  588  		int outerBorderWidth = ceil(Renderer::getScreenWidth() * 0.00f);
  589  		int innerBorderWidth = ceil(Renderer::getScreenWidth() * 0.02f);
  590  
  591  		// sinden.bordersize=thin/big/medium
  592  		auto bordersize = SystemConf::getInstance()->get("controllers.guns.borderssize");
  593  		if (bordersize == "thin")
  594  		{
  595  			outerBorderWidth = ceil(Renderer::getScreenWidth() * 0.00f);
  596  			innerBorderWidth = ceil(Renderer::getScreenWidth() * 0.01f);
  597  		}
  598  		else if (bordersize == "big")
  599  		{
  600  			outerBorderWidth = ceil(Renderer::getScreenWidth() * 0.01f);
  601  			innerBorderWidth = ceil(Renderer::getScreenWidth() * 0.02f);
  602  		}
  603  
  604  		Renderer::setScreenMargin(0, 0);
  605  		Renderer::setMatrix(Transform4x4f::Identity());
  606  
  607  		const unsigned int outerBorderColor = 0x000000FF;
  608  		unsigned int innerBorderColor = 0xFFFFFFFF;
  609  		unsigned int externalBorderColor = 0x000000CC;
  610  
  611  		auto bordersColor = SystemConf::getInstance()->get("controllers.guns.borderscolor");
  612  		if (bordersColor == "red")   innerBorderColor = 0xFF0000FF;
  613  		if (bordersColor == "green") innerBorderColor = 0x00FF00FF;
  614  		if (bordersColor == "blue")  innerBorderColor = 0x0000FFFF;
  615  		if (bordersColor == "white") innerBorderColor = 0xFFFFFFFF;
  616  
  617  		int borderWidth = 0;
  618  		int borderOffset = 0;
  619  
  620  		std::string bordersRatio = SystemConf::getInstance()->get("controllers.guns.bordersratio");
  621  		if(bordersRatio == "4:3") {
  622  		  borderWidth = Renderer::getScreenHeight() / 3 * 4;
  623  		  borderOffset = (Renderer::getScreenWidth() - borderWidth) / 2;
  624  		} else {
  625  		  borderWidth = Renderer::getScreenWidth();
  626  		  borderOffset = 0;
  627  		}
  628  
  629  		// outer border
  630  		Renderer::drawRect(borderOffset, 0, borderWidth, outerBorderWidth, outerBorderColor);
  631  		Renderer::drawRect(borderOffset + borderWidth - outerBorderWidth, 0, outerBorderWidth, Renderer::getScreenHeight(), outerBorderColor);
  632  		Renderer::drawRect(borderOffset, Renderer::getScreenHeight() - outerBorderWidth, borderWidth, outerBorderWidth, outerBorderColor);
  633  		Renderer::drawRect(borderOffset, 0, outerBorderWidth, Renderer::getScreenHeight(), outerBorderColor);
  634  
  635  		// inner border
  636  		Renderer::drawRect(borderOffset + outerBorderWidth, outerBorderWidth, borderWidth - outerBorderWidth * 2, innerBorderWidth, innerBorderColor);
  637  		Renderer::drawRect(borderOffset + borderWidth - outerBorderWidth - innerBorderWidth, outerBorderWidth, innerBorderWidth, Renderer::getScreenHeight() - outerBorderWidth * 2, innerBorderColor);
  638  		Renderer::drawRect(borderOffset + outerBorderWidth, Renderer::getScreenHeight() - outerBorderWidth - innerBorderWidth, borderWidth - outerBorderWidth * 2, innerBorderWidth, innerBorderColor);
  639  		Renderer::drawRect(borderOffset + outerBorderWidth, outerBorderWidth, innerBorderWidth, Renderer::getScreenHeight() - outerBorderWidth * 2, innerBorderColor);
  640  
  641  		Renderer::setScreenMargin(borderOffset + outerBorderWidth + innerBorderWidth, outerBorderWidth + innerBorderWidth);
  642  		Renderer::setMatrix(Transform4x4f::Identity());
  643  	}
  644  	else
  645  		Renderer::setScreenMargin(0, 0);
  646  }
  647  
  648  void Window::renderMenuBackgroundShader()
  649  {
  650  	auto menuBackground = ThemeData::getMenuTheme()->Background;
  651  
  652  	const Renderer::ShaderInfo& info = menuBackground.shader;
  653  	if (!info.path.empty())
  654  	{
  655  		if (mMenuBackgroundShaderTextureCache == -1)
  656  			Renderer::postProcessShader(info.path, 0, 0, Renderer::getScreenWidth(), Renderer::getScreenHeight(), info.parameters, &mMenuBackgroundShaderTextureCache);
  657  
  658  		if (mMenuBackgroundShaderTextureCache != -1)
  659  		{
  660  			Renderer::bindTexture(mMenuBackgroundShaderTextureCache);
  661  			Renderer::setMatrix(Transform4x4f::Identity());
  662  
  663  			int w = Renderer::getScreenWidth();
  664  			int h = Renderer::getScreenHeight();
  665  
  666  			Renderer::Vertex vertices[4];
  667  			vertices[0] = { { (float)0    , (float)0       }, { 0.0f, 1.0f }, 0xFFFFFFFF };
  668  			vertices[1] = { { (float)0    , (float)0 + h   }, { 0.0f, 0.0f }, 0xFFFFFFFF };
  669  			vertices[2] = { { (float)0 + w, (float)0       }, { 1.0f, 1.0f }, 0xFFFFFFFF };
  670  			vertices[3] = { { (float)0 + w, (float)0 + h   }, { 1.0f, 0.0f }, 0xFFFFFFFF };
  671  
  672  			Renderer::drawTriangleStrips(&vertices[0], 4, Renderer::Blend::ONE, Renderer::Blend::ONE);
  673  			Renderer::bindTexture(0);
  674  		}
  675  	}
  676  	else
  677  		resetMenuBackgroundShader();
  678  }
  679  
  680  void Window::resetMenuBackgroundShader()
  681  {
  682  	if (mMenuBackgroundShaderTextureCache != -1)
  683  	{
  684  		Renderer::destroyTexture(mMenuBackgroundShaderTextureCache);
  685  		mMenuBackgroundShaderTextureCache = -1;
  686  	}
  687  }
  688  
  689  void Window::render()
  690  {
  691  	Transform4x4f transform = Transform4x4f::Identity();
  692  
  693  	mRenderedHelpPrompts = false;
  694  	
  695  	// draw only bottom and top of GuiStack (if they are different)
  696  	if (mGuiStack.size())
  697  	{
  698  		auto& bottom = mGuiStack.front();
  699  		auto& top = mGuiStack.back();
  700  
  701  		auto menuBackground = ThemeData::getMenuTheme()->Background;
  702  
  703  		// Don't render bottom if we have a MenuBackgroundShaderTextureCache
  704  		if (mMenuBackgroundShaderTextureCache == -1)
  705  			bottom->render(transform);
  706  
  707  		if (bottom != top)
  708  		{
  709  			if ((top->getTag() == "GuiLoading") && mGuiStack.size() > 2)
  710  			{
  711  				mBackgroundOverlay->render(transform);
  712  				renderMenuBackgroundShader();
  713  
  714  				auto& middle = mGuiStack.at(mGuiStack.size() - 2);
  715  				if (middle != bottom)
  716  					middle->render(transform);
  717  
  718  				top->render(transform);
  719  			}
  720  			else
  721  			{
  722  				if ((top->isKindOf<GuiMsgBox>() || top->getTag() == "popup") && mGuiStack.size() > 2)
  723  				{
  724  					auto& middle = mGuiStack.at(mGuiStack.size() - 2);
  725  					if (middle != bottom)
  726  						middle->render(transform);
  727  				}
  728  
  729  				mBackgroundOverlay->render(transform);
  730  				renderMenuBackgroundShader();
  731  
  732  				top->render(transform);
  733  			}
  734  		}
  735  		else  
  736  			resetMenuBackgroundShader();
  737  	}
  738  	else 
  739  		resetMenuBackgroundShader();
  740  
  741  	renderSindenBorders();
  742  
  743  	if (mGuiStack.size() < 2 || !Renderer::ScreenSettings::fullScreenMenus())
  744  		if (!mRenderedHelpPrompts)
  745  			mHelp->render(transform);
  746  
  747  	// FPS overlay
  748  	if (Settings::DrawFramerate() && mFrameDataText)
  749  	{
  750  		Renderer::setMatrix(transform);
  751  		Renderer::drawSolidRectangle(40.f, 45.f, mFrameDataText->metrics.size.x() + 10.f, mFrameDataText->metrics.size.y() + 10.f, 0x00000080, 0xFFFFFF30, 2.0f, 3.0f);
  752  
  753  		auto trans = transform;
  754  		trans.translate(1, 1);
  755  		Renderer::setMatrix(trans);
  756  
  757  		mFrameDataText->setColor(0x000000FF);
  758  		mDefaultFonts.at(1)->renderTextCache(mFrameDataText.get());
  759  		Renderer::setMatrix(transform);
  760  
  761  		mFrameDataText->setColor(0xFFFF40FF);		
  762  		mDefaultFonts.at(1)->renderTextCache(mFrameDataText.get());
  763  	}
  764  
  765  	// clock 
  766  	if (Settings::DrawClock() && mClock && (mGuiStack.size() < 2 || !Renderer::ScreenSettings::fullScreenMenus()))
  767  		mClock->render(transform);
  768  
  769  	if (Settings::ShowControllerActivity() && mControllerActivity != nullptr && (mGuiStack.size() < 2 || !Renderer::isSmallScreen()))
  770  		mControllerActivity->render(transform);
  771  
  772  	if (mBatteryIndicator != nullptr && (mGuiStack.size() < 2 || !Renderer::ScreenSettings::fullScreenMenus()))
  773  		mBatteryIndicator->render(transform);
  774  
  775  	Renderer::setMatrix(transform);
  776  
  777  	unsigned int screensaverTime = (unsigned int)Settings::ScreenSaverTime();
  778  	if (mTimeSinceLastInput >= screensaverTime && screensaverTime != 0)
  779  		startScreenSaver();
  780  
  781  	// Render notifications
  782  	if (!mRenderScreenSaver)
  783  	{
  784  		for (auto popup : mNotificationPopups)
  785  			popup->render(transform);
  786  
  787  		renderAsyncNotifications(transform);
  788  	}
  789  
  790  	// Always call the screensaver render function regardless of whether the screensaver is active
  791  	// or not because it may perform a fade on transition
  792  	renderScreenSaver();
  793  
  794  	if (!mRenderScreenSaver)
  795  	{
  796  		for (auto extra : mScreenExtras)
  797  			extra->render(transform);
  798  	}
  799  
  800  	if (mVolumeInfo && Settings::VolumePopup())
  801  		mVolumeInfo->render(transform);
  802  
  803  	if (mTimeSinceLastInput >= screensaverTime && screensaverTime != 0)
  804  	{
  805  		if (mAllowSleep && (!mScreenSaver || mScreenSaver->allowSleep()))
  806  		{
  807  			// go to sleep
  808  			if (mSleeping == false) {
  809  				mSleeping = true;
  810  				onSleep();
  811  			}
  812  		}
  813  	}
  814  
  815  	// Render calibration dark background & text
  816  	if (mCalibrationText)
  817  	{
  818  		Renderer::setMatrix(transform);
  819  		Renderer::drawRect(0, 0, Renderer::getScreenWidth(), Renderer::getScreenHeight(), 0x000000A0);
  820  		mCalibrationText->render(transform);
  821  	}
  822  
  823  	// Render guns aims
  824  	auto guns = InputManager::getInstance()->getGuns();
  825  	if (!mRenderScreenSaver && guns.size() && Settings::DrawGunCrosshair())
  826  	{
  827  		auto margin = Renderer::setScreenMargin(0, 0);
  828  		Renderer::setMatrix(Transform4x4f::Identity());
  829  
  830  		bool hasMousePointer = false;
  831  
  832  		if (mGunAimTexture == nullptr)
  833  			mGunAimTexture = TextureResource::get(":/gun.png", false, false, true, false);
  834  
  835  		if (mGunAimTexture->bind())
  836  		{
  837  			for (auto gun : guns)
  838  			{
  839  				if (gun->isMouse())
  840  				{
  841  					hasMousePointer = true;
  842  					continue;
  843  				}
  844  
  845  				if (gun->isLastTickElapsed())
  846  					continue;
  847  
  848  				int pointerSize = (Renderer::isVerticalScreen() ? Renderer::getScreenWidth() : Renderer::getScreenHeight()) / 32;
  849  
  850  				Vector2f topLeft = { gun->x() - pointerSize, gun->y() - pointerSize };
  851  				Vector2f bottomRight = { gun->x() + pointerSize, gun->y() + pointerSize };
  852  
  853  				auto aimColor = guns.size() == 1 ? 0xFFFFFFFF : _gunAimColors[gun->index() % _gunAimColors.size()];
  854  
  855  				if (gun->isLButtonDown() || gun->isRButtonDown())
  856  				{
  857  					auto mixIndex = (gun->index() + 3) % _gunAimColors.size();
  858  					auto invertColor = _gunAimColors[mixIndex];
  859  
  860  					aimColor = Renderer::mixColors(aimColor, invertColor, 0.5);
  861  				}
  862  
  863  				Renderer::Vertex vertices[4];
  864  				vertices[0] = { { topLeft.x() ,     topLeft.y() }, { 0.0f,          0.0f }, aimColor };
  865  				vertices[1] = { { topLeft.x() ,     bottomRight.y() }, { 0.0f,          1.0f }, aimColor };
  866  				vertices[2] = { { bottomRight.x(), topLeft.y() }, { 1.0f, 0.0f }, aimColor };
  867  				vertices[3] = { { bottomRight.x(), bottomRight.y() }, { 1.0f, 1.0f }, aimColor };
  868  
  869  				Renderer::drawTriangleStrips(&vertices[0], 4);
  870  			}
  871  		}	
  872  
  873  #if WIN32
  874  		if (hasMousePointer)
  875  		{
  876  			if (mMouseCursorTexture == nullptr)
  877  				mMouseCursorTexture = TextureResource::get(":/cursor.png", false, true, true, false);
  878  
  879  			if (mMouseCursorTexture->bind())
  880  			{
  881  				for (auto gun : guns)
  882  				{
  883  					if (!gun->isMouse())
  884  						continue;
  885  
  886  					if (gun->isLastTickElapsed())
  887  						break;
  888  
  889  					SDL_SysWMinfo wmInfo;
  890  					SDL_VERSION(&wmInfo.version);
  891  					if (SDL_GetWindowWMInfo(Renderer::getSDLWindow(), &wmInfo))
  892  					{
  893  						HWND hWnd = wmInfo.info.win.window;
  894  
  895  						POINT cursorPos;
  896  						GetCursorPos(&cursorPos);
  897  
  898  						// Convert screen coordinates to client coordinates
  899  						ScreenToClient(hWnd, &cursorPos);
  900  
  901  						// Get the client rectangle of the window
  902  						RECT clientRect;
  903  						GetClientRect(hWnd, &clientRect);
  904  
  905  						// Check if the cursor is within the client area
  906  						if (!PtInRect(&clientRect, cursorPos))
  907  							continue;
  908  					}					
  909  
  910  					int pointerSize = (Renderer::isVerticalScreen() ? Renderer::getScreenWidth() : Renderer::getScreenHeight()) / 38;
  911  					
  912  					Vector2i sz = ImageIO::adjustPictureSize(mMouseCursorTexture->getSize(), Vector2i(pointerSize, pointerSize));
  913  
  914  					Vector2f topLeft = { gun->x(), gun->y() };
  915  					Vector2f bottomRight = { gun->x() + sz.x(), gun->y() + sz.y() };
  916  
  917  					auto aimColor = 0xFFFFFFFF;
  918  					
  919  					if (gun->isLButtonDown() || gun->isRButtonDown())
  920  						aimColor = 0xC0FAFAFF;
  921  
  922  					Renderer::Vertex vertices[4];
  923  					vertices[0] = { { topLeft.x() ,     topLeft.y() }, { 0.0f,          1.0f }, aimColor };
  924  					vertices[1] = { { topLeft.x() ,     bottomRight.y() }, { 0.0f,          0.0f }, aimColor };
  925  					vertices[2] = { { bottomRight.x(), topLeft.y() }, { 1.0f, 1.0f }, aimColor };
  926  					vertices[3] = { { bottomRight.x(), bottomRight.y() }, { 1.0f, 0.0f }, aimColor };
  927  
  928  					Renderer::drawTriangleStrips(&vertices[0], 4);
  929  					break;
  930  				}
  931  			}
  932  		}
  933  #endif
  934  
  935  		Renderer::setScreenMargin(margin.x(), margin.y());
  936  	}
  937  }
  938  
  939  void Window::normalizeNextUpdate()
  940  {
  941  	mNormalizeNextUpdate = true;
  942  }
  943  
  944  bool Window::getAllowSleep()
  945  {
  946  	return mAllowSleep;
  947  }
  948  
  949  void Window::setAllowSleep(bool sleep)
  950  {
  951  	mAllowSleep = sleep;
  952  }
  953  
  954  std::string Window::getCustomSplashScreenImage() {
  955    std::string alternateSplashScreen = Settings::getInstance()->getString("AlternateSplashScreen");
  956    if(alternateSplashScreen != "" && Utils::FileSystem::exists(alternateSplashScreen))
  957      return alternateSplashScreen;
  958    return DEFAULT_SPLASH_IMAGE;
  959  }
  960  
  961  void Window::setCustomSplashScreen(std::string imagePath, std::string customText, IBindable* bindable)
  962  {
  963  	if (Settings::getInstance()->getBool("HideWindow"))
  964  		return;
  965  
  966  	if (!Utils::FileSystem::exists(imagePath))
  967  		mSplash = std::make_shared<Splash>(this, getCustomSplashScreenImage(), false, bindable);
  968  	else
  969  		mSplash = std::make_shared<Splash>(this, imagePath, false, bindable);
  970  
  971  	mSplash->update(customText);
  972  }
  973  
  974  void Window::renderSplashScreen(std::string text, float percent, float opacity)
  975  {
  976  	if (mSplash == NULL)
  977  		mSplash = std::make_shared<Splash>(this, getCustomSplashScreenImage());
  978  
  979  	mSplash->update(text, percent);
  980  	mSplash->render(opacity);
  981  
  982  #if WIN32
  983  	SDL_Event evt;
  984  	SDL_PollEvent(&evt);
  985  #endif
  986  }
  987  
  988  void Window::renderSplashScreen(float opacity, bool swapBuffers)
  989  {
  990  	if (mSplash != nullptr)
  991  		mSplash->render(opacity, swapBuffers);
  992  }
  993  
  994  void Window::closeSplashScreen()
  995  {
  996  	mSplash = nullptr;
  997  }
  998  
  999  void Window::renderHelpPromptsEarly(const Transform4x4f& transform)
 1000  {
 1001  	mHelp->render(transform);
 1002  	mRenderedHelpPrompts = true;
 1003  }
 1004  
 1005  void Window::setHelpPrompts(const std::vector<HelpPrompt>& prompts, const HelpStyle& style)
 1006  {
 1007  	// Keep a temporary reference to the previous grid.
 1008  	// It avoids unloading/reloading images if they are the same, and avoids flickerings
 1009  	auto oldGrid = mHelp->getGrid();
 1010  
 1011  	mHelp->clearPrompts();
 1012  	mHelp->setStyle(style);
 1013  
 1014  	mClockElapsed = -1;
 1015  
 1016  	std::vector<HelpPrompt> addPrompts;
 1017  
 1018  	std::map<std::string, bool> inputSeenMap;
 1019  	std::map<std::string, int> mappedToSeenMap;
 1020  	for(auto it = prompts.cbegin(); it != prompts.cend(); it++)
 1021  	{
 1022  		// only add it if the same icon hasn't already been added
 1023  		if(inputSeenMap.emplace(it->first, true).second)
 1024  		{
 1025  			// this symbol hasn't been seen yet, what about the action name?
 1026  			auto mappedTo = mappedToSeenMap.find(it->second);
 1027  			if(mappedTo != mappedToSeenMap.cend())
 1028  			{
 1029  				// yes, it has!
 1030  
 1031  				// can we combine? (dpad only)
 1032  				if((it->first == "up/down" && addPrompts.at(mappedTo->second).first != "left/right") ||
 1033  					(it->first == "left/right" && addPrompts.at(mappedTo->second).first != "up/down"))
 1034  				{
 1035  					// yes!
 1036  					addPrompts.at(mappedTo->second).first = "up/down/left/right";
 1037  					// don't need to add this to addPrompts since we just merged
 1038  				}else{
 1039  					// no, we can't combine!
 1040  					addPrompts.push_back(*it);
 1041  				}
 1042  			}else{
 1043  				// no, it hasn't!
 1044  				mappedToSeenMap.emplace(it->second, (int)addPrompts.size());
 1045  				addPrompts.push_back(*it);
 1046  			}
 1047  		}
 1048  	}
 1049  
 1050  	// sort prompts so it goes [dpad_all] [dpad_u/d] [dpad_l/r] [a/b/x/y/l/r] [start/select]
 1051  	std::sort(addPrompts.begin(), addPrompts.end(), [](const HelpPrompt& a, const HelpPrompt& b) -> bool {
 1052  
 1053  		static const char* map[] = {
 1054  			"up/down/left/right",
 1055  			"up/down",
 1056  			"left/right",
 1057  			BUTTON_OK, "x", "y", "l", "r", BUTTON_BACK,
 1058  			"start", "select",
 1059  			NULL
 1060  		};
 1061  
 1062  		int i = 0;
 1063  		int aVal = 0;
 1064  		int bVal = 0;
 1065  		while(map[i] != NULL)
 1066  		{
 1067  			if(a.first == map[i])
 1068  				aVal = i;
 1069  			if(b.first == map[i])
 1070  				bVal = i;
 1071  			i++;
 1072  		}
 1073  
 1074  		return aVal > bVal;
 1075  	});
 1076  
 1077  	mHelp->setPrompts(addPrompts);
 1078  }
 1079  
 1080  
 1081  void Window::onSleep()
 1082  {
 1083  	Scripting::fireEvent("sleep");
 1084  }
 1085  
 1086  void Window::onWake()
 1087  {
 1088  	Scripting::fireEvent("wake");
 1089  }
 1090  
 1091  void Window::startScreenSaver()
 1092  {
 1093  	if (mScreenSaver && !mRenderScreenSaver)
 1094  	{
 1095  		for (auto extra : mScreenExtras)
 1096  			extra->onScreenSaverActivate();
 1097  
 1098  		// Tell the GUI components the screensaver is starting
 1099  		for(auto i = mGuiStack.cbegin(); i != mGuiStack.cend(); i++)
 1100  			(*i)->onScreenSaverActivate();
 1101  
 1102  		mScreenSaver->startScreenSaver();
 1103  		mRenderScreenSaver = true;
 1104  	}
 1105  }
 1106  
 1107  bool Window::cancelScreenSaver()
 1108  {
 1109  	bool ret = false;
 1110  
 1111  	mTimeSinceLastInput = 0;
 1112  
 1113  	if (mScreenSaver && mRenderScreenSaver)
 1114  	{		
 1115  		mScreenSaver->stopScreenSaver();
 1116  		mRenderScreenSaver = false;
 1117  		mScreenSaver->resetCounts();
 1118  
 1119  		// Tell the GUI components the screensaver has stopped
 1120  		for(auto i = mGuiStack.cbegin(); i != mGuiStack.cend(); i++)
 1121  			(*i)->onScreenSaverDeactivate();
 1122  
 1123  		for (auto extra : mScreenExtras)
 1124  			extra->onScreenSaverDeactivate();
 1125  
 1126  		ret = true;
 1127  	}
 1128  
 1129  	if (mSleeping)
 1130  	{
 1131  		mSleeping = false;
 1132  		onWake();
 1133  
 1134  		ret = true;
 1135  	}
 1136  
 1137  	return ret;
 1138  }
 1139  
 1140  void Window::renderScreenSaver()
 1141  {
 1142  	if (mScreenSaver)
 1143  		mScreenSaver->renderScreenSaver();
 1144  }
 1145  
 1146  bool Window::hasAsyncNotifications()
 1147  {
 1148  	std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
 1149  	return !mAsyncNotificationComponent.empty();
 1150  }
 1151  
 1152  AsyncNotificationComponent* Window::createAsyncNotificationComponent(bool actionLine)
 1153  {
 1154  	std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
 1155  
 1156  	// The other half of one-surface-at-a-time (fork #283, D-UI-093): a card
 1157  	// created while a toast is up takes the toast's place, and the toast's
 1158  	// words go back on the queue to show after the card -- a toast is short
 1159  	// and the card's run would otherwise pass unseen behind it. The queue is
 1160  	// read from its back, so a toast returned last shows first.
 1161  	if (!mNotificationPopups.empty())
 1162  	{
 1163  		for (auto ip : mNotificationPopups)
 1164  			mNotificationMessages.push_back(NotificationMessage(ip->getMessage(), notificationDuration(-1)));
 1165  		stopNotificationPopups();
 1166  	}
 1167  
 1168  	AsyncNotificationComponent* pc = new AsyncNotificationComponent(this, actionLine);
 1169  	mAsyncNotificationComponent.push_back(pc);
 1170  	
 1171  	if (mAsyncNotificationComponent.size() == 1)
 1172  		PowerSaver::pause();
 1173  
 1174  	return pc;
 1175  }
 1176  
 1177  void Window::renderAsyncNotifications(const Transform4x4f& trans)
 1178  {
 1179  	std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
 1180  
 1181  #define PADDING_H  (Renderer::getScreenWidth()*0.01)
 1182  
 1183  	float posY = Renderer::getScreenHeight() * 0.02f;
 1184  
 1185  	bool first = true;
 1186  	for (auto child : mAsyncNotificationComponent)
 1187  	{		
 1188  		// Centred, matching GuiInfoPopup -- which is what the app shows
 1189  		// immediately after one of these finishes. At 0.9 of the screen a
 1190  		// card hugging the right edge leaves a sliver of margin on one side
 1191  		// and none of the balance that made a corner placement look chosen.
 1192  		float posX = Renderer::getScreenWidth() * 0.5f - child->getSize().x() * 0.5f;
 1193  
 1194  		float offset = child->getSize().y() + PADDING_H;
 1195  
 1196  		float fadingOut = child->getFading();
 1197  		if (fadingOut != 0)
 1198  		{
 1199  			// cubic ease in
 1200  			fadingOut = fadingOut - 1;
 1201  			fadingOut = Math::lerp(0, 1, fadingOut*fadingOut*fadingOut + 1);
 1202  						
 1203  			if (child->isClosing())
 1204  			{
 1205  				child->setPosition(posX, posY - (offset * fadingOut), 0);
 1206  				offset = offset - (offset * fadingOut);
 1207  
 1208  				auto sz = child->getSize();
 1209  				Renderer::pushClipRect(Vector2i(
 1210  					(int)trans.translation()[0] + posX - PADDING_H, 
 1211  					(int)trans.translation()[1] + (first ? 0 : posY)), 
 1212  					Vector2i(
 1213  					(int)sz.x() + 2 * PADDING_H, 
 1214  					(int)sz.y() + (first ? posY : 0)));
 1215  			}
 1216  			else
 1217  				// Appearing: fade in place. The slide this used to do came
 1218  				// in off the right edge, which only reads as motion for a
 1219  				// card anchored there; from the centre it is a lurch.
 1220  				// AsyncNotificationComponent::update already ramps opacity.
 1221  				child->setPosition(posX, posY, 0);
 1222  		}
 1223  		else 
 1224  			child->setPosition(posX, posY, 0);
 1225  
 1226  		child->render(trans);
 1227  
 1228  		if (fadingOut != 0 && child->isClosing())
 1229  			Renderer::popClipRect();
 1230  
 1231  		posY += offset;
 1232  		first = false;
 1233  	}
 1234  }
 1235  
 1236  void Window::updateAsyncNotifications(int deltaTime)
 1237  {
 1238  	std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
 1239  
 1240  	bool changed = false;
 1241  
 1242  	for (int i = mAsyncNotificationComponent.size() - 1; i >= 0; i--)
 1243  	{
 1244  		mAsyncNotificationComponent[i]->update(deltaTime);
 1245  
 1246  		if (!mAsyncNotificationComponent[i]->isRunning())
 1247  		{
 1248  			delete mAsyncNotificationComponent[i];
 1249  
 1250  			auto it = mAsyncNotificationComponent.begin();
 1251  			std::advance(it, i);
 1252  			mAsyncNotificationComponent.erase(it);
 1253  
 1254  			changed = true;
 1255  		}
 1256  	}
 1257  
 1258  	if (changed && mAsyncNotificationComponent.size() == 0)
 1259  		PowerSaver::resume();
 1260  }
 1261  
 1262  void Window::unregisterPostedFunctions(void* data)
 1263  {
 1264  	if (data == nullptr)
 1265  		return;
 1266  
 1267  	for (auto it = mFunctions.cbegin(); it != mFunctions.cend(); )
 1268  	{
 1269  		if ((*it).container == data)
 1270  			it = mFunctions.erase(it);
 1271  		else
 1272  			it++;
 1273  	}
 1274  }
 1275  
 1276  void Window::postToUiThread(const std::function<void()>& func, void* data)
 1277  {	
 1278  	std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
 1279  
 1280  	PostedFunction pf;
 1281  	pf.func = func;
 1282  	pf.container = data;
 1283  	mFunctions.push_back(pf);
 1284  	if (mSleeping || !PowerSaver::getState())
 1285  	{
 1286  		mSleeping = false;
 1287  		mTimeSinceLastInput = 0;
 1288  		PowerSaver::pushRefreshEvent();
 1289  	}
 1290  }
 1291  
 1292  void Window::processPostedFunctions()
 1293  {
 1294  	std::vector<PostedFunction> functions;
 1295  
 1296  	mNotificationMessagesLock.lock();
 1297  
 1298  	for (auto func : mFunctions)
 1299  		functions.push_back(func);
 1300  
 1301  	mFunctions.clear();
 1302  
 1303  	mNotificationMessagesLock.unlock();
 1304  
 1305  	for (auto func : functions)
 1306  		TRYCATCH("processPostedFunction", func.func())
 1307  }
 1308  
 1309  void Window::onThemeChanged(const std::shared_ptr<ThemeData>& theme)
 1310  {
 1311  	for (auto extra : mScreenExtras)
 1312  		delete extra;
 1313  
 1314  	mScreenExtras.clear();
 1315  	mScreenExtras = ThemeData::makeExtras(theme, "screen", this);
 1316  	
 1317  	std::stable_sort(mScreenExtras.begin(), mScreenExtras.end(), [](GuiComponent* a, GuiComponent* b) { return b->getZIndex() > a->getZIndex(); });
 1318  
 1319  	if (mBackgroundOverlay)
 1320  	{
 1321  		mBackgroundOverlay->setImage(ThemeData::getMenuTheme()->Background.fadePath);
 1322  		mBackgroundOverlay->setResize((float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
 1323  	}
 1324  
 1325  	if (mClock)
 1326  	{
 1327  		mClock->setFont(Font::get(FONT_SIZE_SMALL));
 1328  		mClock->setColor(0x777777FF);		
 1329  		mClock->setOrigin(Vector2f::Zero());
 1330  		mClock->setHorizontalAlignment(ALIGN_RIGHT);
 1331  		mClock->setVerticalAlignment(ALIGN_TOP);
 1332  		
 1333  		// if clock element does not exist in screen view -> <view name="screen"><text name="clock"> 
 1334  		// skin it from system.helpsystem -> <view name="system"><helpsystem name="help"> )
 1335  		if (!theme->getElement("screen", "clock", "text"))
 1336  		{
 1337  			auto elem = theme->getElement("system", "help", "helpsystem");
 1338  			if (elem && elem->has("textColor"))
 1339  				mClock->setColor(elem->get<unsigned int>("textColor"));
 1340  
 1341  			if (elem && (elem->has("fontPath") || elem->has("fontSize")))
 1342  				mClock->setFont(Font::getFromTheme(elem, ThemeFlags::ALL, Font::get(FONT_SIZE_MEDIUM)));
 1343  		}
 1344  		
 1345  		mClock->setPosition(Renderer::getScreenWidth()*0.94, Renderer::getScreenHeight()*0.9965 - mClock->getFont()->getHeight());
 1346  		mClock->setSize(Renderer::getScreenWidth()*0.05, 0);
 1347  
 1348  		mClock->applyTheme(theme, "screen", "clock", ThemeFlags::ALL ^ (ThemeFlags::TEXT));
 1349  	}
 1350  
 1351  	if (mControllerActivity)
 1352  		mControllerActivity->applyTheme(theme, "screen", "controllerActivity", ThemeFlags::ALL ^ (ThemeFlags::TEXT));
 1353  
 1354  	if (mBatteryIndicator)
 1355  		mBatteryIndicator->applyTheme(theme, "screen", "batteryIndicator", ThemeFlags::ALL);
 1356  	
 1357  	mVolumeInfo = std::make_shared<VolumeInfoComponent>(this);
 1358  }
 1359  
 1360  void Window::setGunCalibrationState(bool isCalibrating)
 1361  {
 1362  	if (isCalibrating)
 1363  	{
 1364  		if (mCalibrationText == nullptr)
 1365  		{
 1366  			mCalibrationText = std::make_shared<TextComponent>(this);
 1367  			mCalibrationText->setText(_("CALIBRATING GUN\nFire on targets to calibrate"));
 1368  			mCalibrationText->setFont(Font::get(FONT_SIZE_MEDIUM));
 1369  			mCalibrationText->setHorizontalAlignment(ALIGN_CENTER);
 1370  			mCalibrationText->setVerticalAlignment(ALIGN_CENTER);
 1371  			mCalibrationText->setPosition(0.0f, 0.0f);
 1372  			mCalibrationText->setSize(Renderer::getScreenWidth(), Renderer::getScreenHeight() / 2.1f);
 1373  			mCalibrationText->setColor(0xFFFFFFFF);
 1374  			mCalibrationText->setGlowSize(1);
 1375  			mCalibrationText->setGlowColor(0x00000040);			
 1376  		}
 1377  	}
 1378  	else
 1379  		mCalibrationText = nullptr;	
 1380  }
 1381  
 1382  std::vector<GuiComponent*> Window::hitTest(int x, int y)
 1383  {
 1384  	GuiComponent* gui = peekGui();
 1385  	if (!gui)
 1386  		return std::vector<GuiComponent*>();
 1387  
 1388  	auto trans = Transform4x4f::Identity();
 1389  
 1390  	std::vector<GuiComponent*> ret;
 1391  
 1392  	gui->hitTest(x, y, trans, &ret);
 1393  
 1394  	if (mClock && mClock->isVisible())
 1395  		mClock->hitTest(x, y, trans, &ret);
 1396  
 1397  	if (mHelp && mHelp->isVisible())
 1398  		mHelp->hitTest(x, y, trans, &ret);
 1399  
 1400  	return ret;
 1401  }
 1402  
 1403  void Window::processMouseWheel(int delta)
 1404  {
 1405  	GuiComponent* gui = peekGui();
 1406  	if (!gui)
 1407  		return;
 1408  
 1409  	auto hits = hitTest(mLastMousePoint.x(), mLastMousePoint.y());
 1410  
 1411  	if (mMouseCapture != nullptr)
 1412  	{
 1413  		mMouseCapture->onMouseWheel(delta);
 1414  		return;
 1415  	}
 1416  	else
 1417  	{
 1418  		std::reverse(hits.begin(), hits.end());
 1419  
 1420  		for (auto hit : hits)
 1421  			if (hit->onMouseWheel(delta))
 1422  				break;
 1423  
 1424  		hitTest(mLastMousePoint.x(), mLastMousePoint.y());
 1425  	}
 1426  }
 1427  
 1428  void Window::processMouseMove(int x, int y, bool touchScreen)
 1429  {
 1430  	if (!touchScreen && (mLastShowCursor != -2 || x != 0 || y != 0))
 1431  	{
 1432  #if WIN32
 1433  		auto guns = InputManager::getInstance()->getGuns();
 1434  		if (guns.size() == 0 || std::find_if(guns.cbegin(), guns.cend(), [](Gun* x) { return x->name() == "Wiimote Gun"; }) == guns.cend())
 1435  #endif
 1436  		SDL_ShowCursor(1);
 1437  
 1438  		mLastShowCursor = 0;
 1439  	}
 1440  
 1441  	auto point = Renderer::physicalScreenToRotatedScreen(x, y);
 1442  
 1443  	mLastMousePoint.x() = point.x(); mLastMousePoint.y() = point.y();
 1444  
 1445  	GuiComponent* gui = peekGui();
 1446  	if (!gui)
 1447  		return;
 1448  
 1449  	auto hits = hitTest(point.x(), point.y());
 1450  
 1451  	if (mMouseCapture != nullptr)
 1452  	{
 1453  		mMouseCapture->onMouseMove(point.x(), point.y());
 1454  		return;
 1455  	}
 1456  	else
 1457  	{
 1458  		std::reverse(hits.begin(), hits.end());
 1459  
 1460  		for(auto hit : hits)
 1461  			hit->onMouseMove(point.x(), point.y());
 1462  	}
 1463  }
 1464  
 1465  bool Window::processMouseButton(int button, bool down, int x, int y)
 1466  {
 1467  	auto point = Renderer::physicalScreenToRotatedScreen(x, y);
 1468  
 1469  	mLastMousePoint.x() = point.x(); mLastMousePoint.y() = point.y();
 1470  
 1471  	if (mMouseCapture != nullptr)
 1472  	{
 1473  	//	auto hits = hitTest(x, y);
 1474  		mMouseCapture->onMouseClick(button, down, point.x(), point.y());
 1475  		return true;
 1476  	}
 1477  
 1478  	auto ctrls = hitTest(point.x(), point.y());
 1479  	std::reverse(ctrls.begin(), ctrls.end());
 1480  
 1481  	for (auto ctrl : ctrls)		
 1482  		if (ctrl->onMouseClick(button, down, point.x(), point.y()))
 1483  			return true;
 1484  
 1485  	return false;
 1486  }
 1487  
 1488  void Window::setReloadGamelistsCallback(const std::function<void()>& func)
 1489  {
 1490      mReloadGamelistsCallback = func;
 1491  }
 1492  
 1493  void Window::processStorageRequest(std::string line)
 1494  {
 1495  	static std::vector<std::string> storageQueue;
 1496  	static bool isProcessing = false;
 1497  	static bool needReload = false;
 1498  
 1499  	// Helper function to process the next item in the queue
 1500  	auto processNext = [this]() {
 1501  		if (storageQueue.empty()) {
 1502  			isProcessing = false;
 1503  			if (needReload && mReloadGamelistsCallback) {
 1504  				mReloadGamelistsCallback();
 1505  				this->displayNotificationMessage(_("Reloaded the games list..."));
 1506  				needReload = false;
 1507  			}
 1508  			return;
 1509  		}
 1510  		
 1511  		// Trigger the logic for the next item
 1512  		this->processStorageRequest(""); 
 1513  	};
 1514  
 1515  	// Add new incoming API request to the queue
 1516  	if (!line.empty()) {
 1517  		LOG(LogInfo) << "Storage Request Received via API: " << line;
 1518  		storageQueue.push_back(line);
 1519  		if (isProcessing) return;
 1520  	}
 1521  
 1522  	if (storageQueue.empty()) return;
 1523  
 1524  	// Start processing the front of the queue
 1525  	isProcessing = true;
 1526  	std::string currentTask = storageQueue.front();
 1527  	storageQueue.erase(storageQueue.begin());
 1528  
 1529  	std::vector<std::string> parts = Utils::String::split(currentTask, ':');
 1530  	if (parts.empty()) { processNext(); return; }
 1531  
 1532  	std::string type = parts[0];
 1533  	
 1534  	if (type == "REQUEST_MERGE" && parts.size() >= 5)
 1535  	{
 1536  		std::string deviceName  = parts[1];
 1537  		std::string deviceModel = parts[2];
 1538  		std::string deviceSize  = parts[3];
 1539  		std::string mountPoint  = parts[4];
 1540  		std::string uniqueId    = (parts.size() > 5 && !parts[5].empty()) ? parts[5] : "";
 1541  
 1542  		std::string message = _("GAME DRIVE DETECTED") + "\n\n" +
 1543  							  _("DEVICE") + ": " + deviceName + "\n" +
 1544  							  _("MODEL")  + ": " + deviceModel + "\n" +
 1545  							  _("SIZE")   + ": " + deviceSize + "\n" +
 1546  							  _("MOUNT")  + ": " + mountPoint + "\n\n" +
 1547  							  _("Merge games from this drive partition now?") + "\n" + 
 1548  							  _("(This will also apply on future boots)");
 1549  
 1550  		auto mergeLambda = [this, mountPoint, processNext] {
 1551  				this->displayNotificationMessage(_("Merge requested... Please wait."));
 1552  				needReload = true;
 1553  
 1554  				std::thread([this, mountPoint, processNext]() {
 1555  					bool success = ApiSystem::getInstance()->mergeDrive(mountPoint);
 1556  					this->postToUiThread([this, success, processNext]() {
 1557  						if (!success) {
 1558  							this->pushGui(new GuiMsgBox(this, _("MERGE FAILED") + "\n" + _("Please check the logs."), _("OK"), [processNext] { processNext(); }));
 1559  						} else {
 1560  							processNext(); 
 1561  						}
 1562  					});
 1563  				}).detach();
 1564  		};
 1565  
 1566  		if (!uniqueId.empty())
 1567  		{
 1568  			auto* msg = new GuiMsgBox(this, message,
 1569  				_("NO, IGNORE THIS TIME"), [processNext] { processNext(); },
 1570  				_("NO, IGNORE FOREVER"), [this, uniqueId, processNext] {
 1571  					this->displayNotificationMessage(_("Adding drive to ignore list..."));
 1572  					std::thread([uniqueId, processNext, this]() {
 1573  						ApiSystem::getInstance()->ignoreDevicePermanently(uniqueId);
 1574  						this->postToUiThread([processNext] { processNext(); });
 1575  					}).detach();
 1576  				},
 1577  				_("YES, MERGE DRIVE"), mergeLambda
 1578  			);
 1579  			pushGui(msg);
 1580  		}
 1581  		else
 1582  		{
 1583  			auto* msg = new GuiMsgBox(this, message,
 1584  				_("YES"), mergeLambda, 
 1585  				_("NO"), [processNext] { processNext(); }
 1586  			);
 1587  			pushGui(msg);
 1588  		}
 1589  	}
 1590  	else if (type == "REQUEST_FORMAT" && parts.size() >= 2)
 1591  	{
 1592  		std::string deviceName = parts[1];
 1593  		std::string deviceModel = (parts.size() > 2 && !parts[2].empty()) ? parts[2] : _("N/A");
 1594  		std::string deviceSize = (parts.size() > 3 && !parts[3].empty()) ? parts[3] : _("N/A");
 1595  		std::string uniqueId = (parts.size() > 4 && !parts[4].empty()) ? parts[4] : "";
 1596  
 1597  		std::string message = _("NEW DRIVE DETECTED") + "\n\n" +
 1598  							_("DEVICE") + ": " + deviceName + "\n" +
 1599  							_("MODEL") + ": " + deviceModel + "\n" +
 1600  							_("SIZE") + ": " + deviceSize + "\n\n" +
 1601  							_("Format and prepare this drive for game storage?") + "\n" +
 1602  							_("(ALL EXISTING DATA WILL BE ERASED)");
 1603  		
 1604  		auto formatLambda = [this, deviceName, processNext] {
 1605  			this->displayNotificationMessage(_("Starting format process..."));
 1606  			needReload = true;
 1607  
 1608  			std::thread([this, deviceName, processNext]() {
 1609  				std::string fsType = SystemConf::getInstance()->get("system.external_disk_format");
 1610  				if (fsType.empty()) fsType = "btrfs";
 1611  				bool success = ApiSystem::getInstance()->prepareDrive(deviceName, fsType);
 1612  				this->postToUiThread([this, success, processNext]() {
 1613  					if (!success) {
 1614  						this->pushGui(new GuiMsgBox(this, _("FORMAT FAILED") + "\n" + _("Please check the logs."), _("OK"), [processNext] { processNext(); }));
 1615  					} else {
 1616  						processNext();
 1617  					}
 1618  				});
 1619  			}).detach(); 
 1620  		};
 1621  
 1622  		auto confirmLambda = [this, formatLambda, processNext] {
 1623  			this->pushGui(new GuiMsgBox(this, _("ARE YOU SURE?"), 
 1624  				_("NO"), [processNext] { processNext(); }, 
 1625  				_("YES"), formatLambda));
 1626  		};
 1627  
 1628  		if (!uniqueId.empty())
 1629  		{
 1630  			auto* msg = new GuiMsgBox(this, message,
 1631  				_("NO, IGNORE THIS TIME"), [processNext] { processNext(); },
 1632  				_("NO, IGNORE FOREVER"), [this, uniqueId, processNext] {
 1633  					this->displayNotificationMessage(_("Adding drive to ignore list..."));
 1634  					std::thread([uniqueId, processNext, this]() {
 1635  						ApiSystem::getInstance()->ignoreDevicePermanently(uniqueId);
 1636  						this->postToUiThread([processNext] { processNext(); });
 1637  					}).detach();
 1638  				},
 1639  				_("YES, FORMAT & MERGE"), confirmLambda
 1640  			);
 1641  			pushGui(msg);
 1642  		}
 1643  		else
 1644  		{
 1645  			auto* msg = new GuiMsgBox(this, message,
 1646  				_("NO, IGNORE"), [processNext] { processNext(); },
 1647  				_("YES, FORMAT & MERGE"), confirmLambda
 1648  			);
 1649  			pushGui(msg);
 1650  		}
 1651  	}
 1652  	else {
 1653  		// Cleanup
 1654  		processNext();
 1655  	}
 1656  }
```

## src/Window.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_WINDOW_H
    3  #define ES_CORE_WInDOW_H
    4  
    5  #include "HelpPrompt.h"
    6  #include "InputConfig.h"
    7  #include "Settings.h"
    8  #include "math/Vector2f.h"
    9  #include "math/Vector2i.h"
   10  #include <memory>
   11  #include <functional>
   12  
   13  class FileData;
   14  class Font;
   15  class GuiComponent;
   16  class HelpComponent;
   17  class ImageComponent;
   18  class InputConfig;
   19  class TextCache;
   20  class Transform4x4f;
   21  struct HelpStyle;
   22  class TextureResource;
   23  class GuiInfoPopup;
   24  class AsyncNotificationComponent;
   25  class ThemeData;
   26  class TextComponent;
   27  class ControllerActivityComponent;
   28  class VolumeInfoComponent;
   29  class BatteryIndicatorComponent;
   30  class Splash;
   31  class IBindable;
   32  
   33  class Window
   34  {
   35  public:
   36  	class ScreenSaver {
   37  	public:
   38  		virtual void startScreenSaver() = 0;
   39  		virtual void stopScreenSaver() = 0;
   40  		virtual void nextVideo() = 0;
   41  		virtual void renderScreenSaver() = 0;
   42  		virtual bool allowSleep() = 0;
   43  		virtual void update(int deltaTime) = 0;
   44  		virtual bool isScreenSaverActive() = 0;
   45  		virtual FileData* getCurrentGame() = 0;
   46  		virtual void launchGame() = 0;
   47  		virtual void resetCounts() = 0;
   48  	};
   49  
   50  	Window();
   51  	~Window();
   52  
   53  	void pushGui(GuiComponent* gui);
   54  	void displayNotificationMessage(std::string message, int duration = -1); 
   55  	void removeGui(GuiComponent* gui);
   56  	GuiComponent* peekGui();
   57  	inline int getGuiStackSize() { return (int)mGuiStack.size(); }
   58  
   59  	void textInput(const char* text);
   60  	void input(InputConfig* config, Input input);
   61  	void update(int deltaTime);
   62  	void render();
   63  
   64  	bool init(bool initRenderer = true, bool initInputManager = true);
   65  	void deinit(bool deinitRenderer = true);
   66  
   67  	void normalizeNextUpdate();
   68  
   69  	inline bool isSleeping() const { return mSleeping; }
   70  	bool getAllowSleep();
   71  	void setAllowSleep(bool sleep);
   72  	
   73  	// Splash screen
   74  	std::string getCustomSplashScreenImage();
   75  	void setCustomSplashScreen(std::string imagePath, std::string customText, IBindable* bindable = nullptr);
   76  	void renderSplashScreen(std::string text, float percent = -1, float opacity = 1);
   77  	void renderSplashScreen(float opacity = 1, bool swapBuffers = true);
   78  	void closeSplashScreen();
   79  
   80  	void renderHelpPromptsEarly(const Transform4x4f& transform); // used to render HelpPrompts before a fade
   81  	void setHelpPrompts(const std::vector<HelpPrompt>& prompts, const HelpStyle& style);
   82  
   83  	void setScreenSaver(ScreenSaver* screenSaver) { mScreenSaver = screenSaver; }
   84  
   85  	void stopNotificationPopups();
   86  
   87  	void startScreenSaver();
   88  	bool cancelScreenSaver();
   89  	void renderScreenSaver();
   90  
   91  	void postToUiThread(const std::function<void()>& func, void* data = nullptr);
   92  	void unregisterPostedFunctions(void* data);
   93  	void reactivateGui();
   94  
   95  	void onThemeChanged(const std::shared_ptr<ThemeData>& theme);
   96  
   97  	std::shared_ptr<BatteryIndicatorComponent>	getBatteryIndicator() { return mBatteryIndicator; }
   98  
   99  	AsyncNotificationComponent* createAsyncNotificationComponent(bool actionLine = false);
  100  	// Includes queued, lingering and fading cards until the window removes them.
  101  	bool hasAsyncNotifications();
  102  
  103  	bool isCalibratingGun() { return mCalibrationText != nullptr; }
  104  	void setGunCalibrationState(bool isCalibrating);
  105  
  106  	// Mouse management
  107  	void processMouseMove(int x, int y, bool touchScreen);
  108  	void processMouseWheel(int delta);	
  109  	bool processMouseButton(int button, bool down, int x, int y);
  110  	void releaseMouseCapture() { mMouseCapture = nullptr; }
  111  	void setMouseCapture(GuiComponent* mouseCapture) { mMouseCapture = mouseCapture; }
  112  	bool hasMouseCapture(GuiComponent* mouseCapture) { return mMouseCapture == mouseCapture; }
  113  
  114  	void processStorageRequest(std::string line);
  115  	void setReloadGamelistsCallback(const std::function<void()>& func);
  116  
  117  private:
  118  	std::vector<GuiComponent*> hitTest(int x, int y);
  119  
  120  	void processPostedFunctions();
  121  	void renderSindenBorders();
  122  
  123  	std::vector<AsyncNotificationComponent*> mAsyncNotificationComponent;
  124  	void updateAsyncNotifications(int deltaTime);
  125  	void renderAsyncNotifications(const Transform4x4f& trans);
  126  	
  127  	struct PostedFunction
  128  	{
  129  		std::function<void()> func;
  130  		void* container;
  131  	};
  132  
  133  	std::vector<PostedFunction> mFunctions;
  134  
  135  	std::vector<GuiInfoPopup*> mNotificationPopups;
  136  	void updateNotificationPopups(int deltaTime);
  137  	void layoutNotificationPopups();
  138  
  139  	void processNotificationMessages();
  140  	void processSongTitleNotifications();
  141  
  142  	void onSleep();
  143  	void onWake();
  144  
  145  	HelpComponent*	mHelp;
  146  	ImageComponent* mBackgroundOverlay;
  147  	ScreenSaver*	mScreenSaver;	
  148  	bool			mRenderScreenSaver;
  149  
  150  	std::vector<GuiComponent*> mScreenExtras;
  151  	std::vector<GuiComponent*> mGuiStack;
  152  
  153  	typedef std::pair<std::string, int> NotificationMessage;
  154  	std::vector<NotificationMessage> mNotificationMessages; 
  155  
  156  	std::vector< std::shared_ptr<Font> > mDefaultFonts;
  157  	std::shared_ptr<Splash> mSplash;
  158  
  159  	int mFrameTimeElapsed;
  160  	int mFrameCountElapsed;
  161  	int mAverageDeltaTime;
  162  
  163  	std::unique_ptr<TextCache> mFrameDataText;
  164  
  165  	int mClockElapsed;
  166  	std::shared_ptr<TextComponent>	mClock;
  167  	std::shared_ptr<ControllerActivityComponent>	mControllerActivity;
  168  	std::shared_ptr<VolumeInfoComponent> mVolumeInfo;
  169  	std::shared_ptr<BatteryIndicatorComponent>	mBatteryIndicator;	
  170  
  171  	bool mNormalizeNextUpdate;
  172  
  173  	bool mAllowSleep;
  174  	bool mSleeping;
  175  	unsigned int mTimeSinceLastInput;
  176  
  177  	bool mRenderedHelpPrompts;
  178  
  179  	std::shared_ptr<TextComponent>	mCalibrationText;
  180  
  181  	int mTransitionOffset;
  182  
  183  	std::shared_ptr<TextureResource> mGunAimTexture;
  184  	std::shared_ptr<TextureResource> mMouseCursorTexture;
  185  
  186  	GuiComponent* mMouseCapture;
  187  	Vector2i	  mLastMousePoint;
  188  	int			  mLastShowCursor;
  189  
  190  	void renderMenuBackgroundShader();
  191  	void resetMenuBackgroundShader();
  192  	unsigned int mMenuBackgroundShaderTextureCache;
  193  
  194  	std::function<void()> mReloadGamelistsCallback;
  195  };
  196  
  197  #endif // ES_CORE_WINDOW_H
```

## src/guis/GuiDetectDevice.cpp `:1-13` (an excerpt, upstream-carried, at the pin)

```text
    1  #include "guis/GuiDetectDevice.h"
    2  
    3  #include "components/TextComponent.h"
    4  #include "guis/GuiInputConfig.h"
    5  #include "utils/FileSystemUtil.h"
    6  #include "utils/StringUtil.h"
    7  #include "InputManager.h"
    8  #include "PowerSaver.h"
    9  #include "Window.h"
   10  #include "LocaleES.h"
   11  
   12  #define HOLD_TIME 1000
   13  
```

## src/guis/GuiDetectDevice.cpp `:24-66` (an excerpt, upstream-carried, at the pin)

```text
   24  	mHoldingConfig = NULL;
   25  	mHoldTime = 0;
   26  	mDoneCallback = doneCallback;
   27  
   28  	addChild(&mBackground);
   29  	addChild(&mGrid);
   30  	
   31  	// title
   32  	mTitle = std::make_shared<TextComponent>(mWindow, firstRun ? _("WELCOME") : _("CONFIGURE INPUT"), theme->Title.font, theme->Title.color, ALIGN_CENTER);
   33  	mGrid.setEntry(mTitle, Vector2i(0, 0), false, true, Vector2i(1, 1), GridFlags::BORDER_BOTTOM);
   34  
   35  	// device info
   36  	std::stringstream deviceInfo;
   37  	int numDevices = InputManager::getInstance()->getNumJoysticks();
   38  	
   39  	if(numDevices > 0) 
   40  	{
   41  	  char strbuf[256];
   42  	  snprintf(strbuf, 256, ngettext("%i GAMEPAD DETECTED", "%i GAMEPADS DETECTED", numDevices), numDevices); 
   43  	  deviceInfo << strbuf;
   44  	}
   45  	else
   46  		deviceInfo << _("NO GAMEPADS DETECTED"); 
   47  
   48  	mDeviceInfo = std::make_shared<TextComponent>(mWindow, deviceInfo.str(), theme->TextSmall.font, theme->TextSmall.color, ALIGN_CENTER);
   49  	mGrid.setEntry(mDeviceInfo, Vector2i(0, 1), false, true);
   50  
   51  	// message
   52  	mMsg1 = std::make_shared<TextComponent>(mWindow, _("HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT."), theme->TextSmall.font, theme->Text.color, ALIGN_CENTER); 
   53  	mGrid.setEntry(mMsg1, Vector2i(0, 2), false, true);
   54  	
   55  	if(firstRun)
   56  	  mMsg2 = std::make_shared<TextComponent>(mWindow, _("PRESS ESC TO CANCEL."), theme->TextSmall.font, theme->Text.color, ALIGN_CENTER);
   57  	else
   58  	  mMsg2 = std::make_shared<TextComponent>(mWindow, _("PRESS ESC OR A HOTKEY TO CANCEL."), theme->TextSmall.font, theme->Text.color, ALIGN_CENTER);
   59  	
   60  	mGrid.setEntry(mMsg2, Vector2i(0, 3), false, true);
   61  
   62  	// currently held device
   63  	mDeviceHeld = std::make_shared<TextComponent>(mWindow, "", theme->Text.font, theme->Text.selectedColor, ALIGN_CENTER);
   64  	mGrid.setEntry(mDeviceHeld, Vector2i(0, 4), false, true);
   65  
   66  	if (Renderer::ScreenSettings::fullScreenMenus())
```

## src/guis/GuiDetectDevice.cpp `:91-107` (an excerpt, upstream-carried, at the pin)

```text
   91  	if (input.device == DEVICE_MOUSE)
   92  		return true;
   93  
   94  	if(!mFirstRun && (input.device == DEVICE_KEYBOARD && input.type == TYPE_KEY && input.value && input.id == SDLK_ESCAPE) ||
   95  	                 (input.device != DEVICE_KEYBOARD && config->isMappedTo("HotKeyEnable", input)))
   96  	{
   97  		// cancel configuring
   98  		PowerSaver::resume();
   99  		delete this;
  100  		return true;
  101  	}
  102  
  103  	if(input.type == TYPE_BUTTON || input.type == TYPE_KEY ||input.type == TYPE_CEC_BUTTON)
  104  	{
  105  		if(input.value && mHoldingConfig == NULL)
  106  		{
  107  			// started holding
```

## src/guis/GuiDetectDevice.cpp `:119-149` (an excerpt, upstream-carried, at the pin)

```text
  119  	return true;
  120  }
  121  
  122  void GuiDetectDevice::update(int deltaTime)
  123  {
  124  	if(mHoldingConfig)
  125  	{
  126  		// If ES starts and if a known device is connected after startup skip controller configuration
  127  		if(mFirstRun && Utils::FileSystem::exists(InputManager::getConfigPath()) && InputManager::getInstance()->getNumConfiguredDevices() > 0)
  128  		{
  129  			if(mDoneCallback)
  130  				mDoneCallback();
  131  			PowerSaver::resume();
  132  			delete this; // delete GUI element
  133  		}
  134  		else
  135  		{
  136  			mHoldTime -= deltaTime;
  137  			const float t = (float)mHoldTime / HOLD_TIME;
  138  			unsigned int c = (unsigned char)(t * 255);
  139  			mDeviceHeld->setColor((c << 24) | (c << 16) | (c << 8) | 0xFF);
  140  			if(mHoldTime <= 0)
  141  			{
  142  				// picked one!
  143  				mWindow->pushGui(new GuiInputConfig(mWindow, mHoldingConfig, true, mDoneCallback));
  144  				PowerSaver::resume();
  145  				delete this;
  146  			}
  147  		}
  148  	}
  149  }
```

## src/guis/GuiInfoPopup.cpp `:90-106` (an excerpt, upstream-carried, at the pin)

```text
   90  	else if (curTime - mStartTime > mDuration || curTime < mStartTime)
   91  	{
   92  		// If we're past the popup duration, no need to render or if SDL reset : Stop
   93  		mRunning = false;
   94  		mFadeOut = 1.0;
   95  		return;
   96  	}
   97  
   98  	#define FADE_DURATION 250
   99  
  100  	// compute fade in effect
  101  	int alpha = 255;
  102  
  103  	if (curTime - mStartTime <= FADE_DURATION)
  104  		alpha = ((curTime - mStartTime) * 255 / FADE_DURATION);
  105  	else if (curTime - mStartTime >= mDuration - FADE_DURATION)
  106  	{
```

## src/guis/GuiInputConfig.cpp `:3-48` (an excerpt, upstream-carried, at the pin)

```text
    3  
    4  #include "components/ButtonComponent.h"
    5  #include "components/MenuComponent.h"
    6  #include "guis/GuiMsgBox.h"
    7  #include "InputManager.h"
    8  #include "Log.h"
    9  #include "Window.h"
   10  
   11  #define fake_gettext_north pgettext("joystick", "NORTH")
   12  #define fake_gettext_south pgettext("joystick", "SOUTH")
   13  #define fake_gettext_east  pgettext("joystick", "EAST")
   14  #define fake_gettext_west  pgettext("joystick", "WEST")
   15  
   16  #define fake_gettext_start  pgettext("joystick", "START")
   17  #define fake_gettext_select pgettext("joystick", "SELECT")
   18  
   19  #define fake_gettext_up    pgettext("joystick", "D-PAD UP")
   20  #define fake_gettext_down  pgettext("joystick", "D-PAD DOWN")
   21  #define fake_gettext_left  pgettext("joystick", "D-PAD LEFT")
   22  #define fake_gettext_right pgettext("joystick", "D-PAD RIGHT")
   23  
   24  #define fake_gettext_left_a_up     pgettext("joystick", "LEFT ANALOG UP")
   25  #define fake_gettext_left_a_down   pgettext("joystick", "LEFT ANALOG DOWN")
   26  #define fake_gettext_left_a_left   pgettext("joystick", "LEFT ANALOG LEFT")
   27  #define fake_gettext_left_a_right  pgettext("joystick", "LEFT ANALOG RIGHT")
   28  #define fake_gettext_right_a_up    pgettext("joystick", "RIGHT ANALOG UP")
   29  #define fake_gettext_right_a_down  pgettext("joystick", "RIGHT ANALOG DOWN")
   30  #define fake_gettext_right_a_left  pgettext("joystick", "RIGHT ANALOG LEFT")
   31  #define fake_gettext_right_a_right pgettext("joystick", "RIGHT ANALOG RIGHT")
   32  
   33  #define fake_gettext_pageup   pgettext("joystick", "LEFT SHOULDER")
   34  #define fake_gettext_pagedown pgettext("joystick", "RIGHT SHOULDER")
   35  #define fake_gettext_l2       pgettext("joystick", "LEFT TRIGGER")
   36  #define fake_gettext_r2       pgettext("joystick", "RIGHT TRIGGER")
   37  #define fake_gettext_l3       pgettext("joystick", "LEFT STICK PRESS")
   38  #define fake_gettext_r3       pgettext("joystick", "RIGHT STICK PRESS")
   39  
   40  #define fake_gettext_hotkey        pgettext("joystick", "HOTKEY")
   41  
   42  //MasterVolUp and MasterVolDown are also hooked up, but do not appear on this screen.
   43  //If you want, you can manually add them to es_input.cfg.
   44  
   45  #define HOLD_TO_SKIP_MS 1000
   46  
   47  void GuiInputConfig::initInputConfigStructure(InputConfig* target)
   48  {
```

## src/guis/GuiInputConfig.cpp `:65-81` (an excerpt, upstream-carried, at the pin)

```text
   65  		{ "LeftTrigger",      true,  "LEFT TRIGGER",       ":/help/button_lt.svg" },
   66  		{ "RightTrigger",     true,  "RIGHT TRIGGER",      ":/help/button_rt.svg" },
   67  		{ "LeftThumb",        true,  "LEFT THUMB",         ":/help/analog_thumb.svg" },
   68  		{ "RightThumb",       true,  "RIGHT THUMB",        ":/help/analog_thumb.svg" },
   69  		{ "LeftAnalogUp",     true,  "LEFT ANALOG UP",     ":/help/analog_up.svg" },
   70  		{ "LeftAnalogDown",   true,  "LEFT ANALOG DOWN",   ":/help/analog_down.svg" },
   71  		{ "LeftAnalogLeft",   true,  "LEFT ANALOG LEFT",   ":/help/analog_left.svg" },
   72  		{ "LeftAnalogRight",  true,  "LEFT ANALOG RIGHT",  ":/help/analog_right.svg" },
   73  		{ "HotKeyEnable",     true,  "HOTKEY ENABLE",      ":/help/button_hotkey.svg" },
   74  		{ "RightAnalogUp",    true,  "RIGHT ANALOG UP",    ":/help/analog_up.svg" },
   75  		{ "RightAnalogDown",  true,  "RIGHT ANALOG DOWN",  ":/help/analog_down.svg" },
   76  		{ "RightAnalogLeft",  true,  "RIGHT ANALOG LEFT",  ":/help/analog_left.svg" },
   77  		{ "RightAnalogRight", true,  "RIGHT ANALOG RIGHT", ":/help/analog_right.svg" }
   78  	};
   79  	
   80  #ifdef INVERTEDINPUTCONFIG
   81  	GUI_INPUT_CONFIG_LIST[0].name = "a";
```

## src/guis/GuiInputConfig.cpp `:117-147` (an excerpt, upstream-carried, at the pin)

```text
  117  	mConfiguringRow = mConfiguringAll;
  118  
  119  	addChild(&mBackground);
  120  	addChild(&mGrid);
  121  
  122  	// 0 is a spacer row
  123  	mGrid.setEntry(std::make_shared<GuiComponent>(mWindow), Vector2i(0, 0), false);
  124  
  125  	mTitle = std::make_shared<TextComponent>(mWindow, _("CONFIGURING"), theme->Title.font, theme->Title.color, ALIGN_CENTER); 
  126  	mGrid.setEntry(mTitle, Vector2i(0, 1), false, true);
  127  
  128  	char strbuf[256];
  129  	if(target->getDeviceId() == DEVICE_KEYBOARD)
  130  	  strncpy(strbuf, _("KEYBOARD").c_str(), 256); 
  131  	else if(target->getDeviceId() == DEVICE_CEC)
  132  	  strncpy(strbuf, _("CEC").c_str(), 256); 
  133  	else {
  134  	  snprintf(strbuf, 256, _("GAMEPAD %i").c_str(), target->getDeviceId() + 1); 
  135  	}
  136  	mSubtitle1 = std::make_shared<TextComponent>(mWindow, Utils::String::toUpper(strbuf), theme->Text.font, theme->Title.color, ALIGN_CENTER); 
  137  	mGrid.setEntry(mSubtitle1, Vector2i(0, 2), false, true);
  138  
  139  	mSubtitle2 = std::make_shared<TextComponent>(mWindow, _("HOLD ANY BUTTON TO SKIP"), theme->TextSmall.font, theme->TextSmall.color, ALIGN_CENTER); 
  140  	mGrid.setEntry(mSubtitle2, Vector2i(0, 3), false, true);
  141  
  142  	// 4 is a spacer row
  143  
  144  	mList = std::make_shared<ComponentList>(mWindow);
  145  	mGrid.setEntry(mList, Vector2i(0, 5), true, true);
  146  	for(int i = 0; i < GUI_INPUT_CONFIG_LIST.size(); i++)
  147  	{
```

## src/guis/GuiInputConfig.cpp `:155-174` (an excerpt, upstream-carried, at the pin)

```text
  155  		icon->setResize(0, Font::get(FONT_SIZE_MEDIUM)->getLetterHeight() * 1.25f);
  156  		row.addElement(icon, false);
  157  
  158  		// spacer between icon and text
  159  		auto spacer = std::make_shared<GuiComponent>(mWindow);
  160  		spacer->setSize(16, 0);
  161  		row.addElement(spacer, false);
  162  
  163  		auto text = std::make_shared<TextComponent>(mWindow, pgettext("joystick", Utils::String::toUpper(GUI_INPUT_CONFIG_LIST[i].dispName).c_str()), theme->Text.font, theme->Text.color);
  164  		row.addElement(text, true);
  165  
  166  		auto mapping = std::make_shared<TextComponent>(mWindow, _("-NOT DEFINED-"), theme->Text.font, theme->TextSmall.color, ALIGN_RIGHT); 
  167  		setNotDefined(mapping); // overrides text and color set above
  168  		row.addElement(mapping, true);
  169  		mMappings.push_back(mapping);
  170  
  171  		row.input_handler = [this, i, mapping](InputConfig* config, Input input) -> bool
  172  		{
  173  			// ignore input not from our target device
  174  			if(config != mTargetConfig)
```

## src/guis/GuiInputConfig.cpp `:250-296` (an excerpt, upstream-carried, at the pin)

```text
  250  	});
  251  
  252  	// make the first one say "PRESS ANYTHING" if we're re-configuring everything
  253  	if(mConfiguringAll)
  254  		setPress(mMappings.front());
  255  
  256  	// buttons
  257  	std::vector< std::shared_ptr<ButtonComponent> > buttons;
  258  	std::function<void()> okFunction = [this, okCallback] {
  259  		InputManager::getInstance()->writeDeviceConfig(mTargetConfig); // save
  260  		if(okCallback)
  261  			okCallback();
  262  		delete this; 
  263  	};
  264  	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, _("OK"), "ok", [this, okFunction] { 
  265  		// check if the hotkey enable button is set. if not prompt the user to use select or nothing.
  266  		Input input;
  267  		if (!mTargetConfig->getInputByName("HotKeyEnable", &input)) {
  268  			mWindow->pushGui(new GuiMsgBox(mWindow,
  269  				_("NO HOTKEY BUTTON HAS BEEN ASSIGNED. THIS IS REQUIRED FOR EXITING GAMES WITH A CONTROLLER. DO YOU WANT TO USE THE SELECT BUTTON AS YOUR HOTKEY?"),  
  270  				_("SET SELECT AS HOTKEY"), [this, okFunction] { 
  271  					Input input;
  272  					mTargetConfig->getInputByName("Select", &input);
  273  					mTargetConfig->mapInput("HotKeyEnable", input);
  274  					okFunction();
  275  					},
  276  				_("DO NOT ASSIGN HOTKEY"), [this, okFunction] { 
  277  					// for a disabled hotkey enable button, set to a key with id 0,
  278  					// so the input configuration script can be backwards compatible.
  279  					mTargetConfig->mapInput("HotKeyEnable", Input(DEVICE_KEYBOARD, TYPE_KEY, 0, 1, true));
  280  					okFunction();
  281  				}
  282  			));
  283  		} else {
  284  			okFunction();
  285  		}
  286  	}));
  287  
  288  	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, _("CANCEL"), "cancel", [this] { delete this; }));
  289  
  290  	mButtonGrid = makeButtonGrid(mWindow, buttons);
  291  	mGrid.setEntry(mButtonGrid, Vector2i(0, 6), true, false);
  292  
  293  	if (Renderer::ScreenSettings::fullScreenMenus())
  294  		setSize(Renderer::getScreenWidth(), Renderer::getScreenHeight());
  295  	else
  296  		setSize(Renderer::getScreenWidth() * 0.6f, Renderer::getScreenHeight() * 0.75f);
```

## src/guis/GuiInputConfig.cpp `:339-355` (an excerpt, upstream-carried, at the pin)

```text
  339  			mHoldingInput = false;
  340  			rowDone();
  341  		}else{
  342  			if(prevSec != curSec)
  343  			{
  344  				// crossed the second boundary, update text
  345  				const auto& text = mMappings.at(mHeldInputId);
  346  				char strbuf[256];
  347  				snprintf(strbuf, 256, ngettext("HOLD FOR %iS TO SKIP", "HOLD FOR %iS TO SKIP", HOLD_TO_SKIP_MS/1000 - curSec), HOLD_TO_SKIP_MS/1000 - curSec); 
  348  				text->setText(strbuf);
  349  				text->setColor(ThemeData::getMenuTheme()->Text.color);
  350  			}
  351  		}
  352  	}
  353  }
  354  
  355  // move cursor to the next thing if we're configuring all, 
```

## src/guis/GuiInputConfig.cpp `:371-405` (an excerpt, upstream-carried, at the pin)

```text
  371  	}else{
  372  		// only configuring one row, so stop
  373  		mConfiguringRow = false;
  374  	}
  375  }
  376  
  377  void GuiInputConfig::setPress(const std::shared_ptr<TextComponent>& text)
  378  {
  379    text->setText(_("PRESS ANYTHING")); 
  380  	text->setColor(0x656565FF);
  381  }
  382  
  383  void GuiInputConfig::setNotDefined(const std::shared_ptr<TextComponent>& text)
  384  {
  385    text->setText(_("-NOT DEFINED-")); 
  386  	text->setColor(0x999999FF);
  387  }
  388  
  389  void GuiInputConfig::setAssignedTo(const std::shared_ptr<TextComponent>& text, Input input)
  390  {
  391  	text->setText(Utils::String::toUpper(input.string()));
  392  	text->setColor(0x777777FF);
  393  }
  394  
  395  void GuiInputConfig::error(const std::shared_ptr<TextComponent>& text, const std::string& /*msg*/)
  396  {
  397    text->setText(_("ALREADY TAKEN")); 
  398  	text->setColor(0x656565FF);
  399  }
  400  
  401  bool GuiInputConfig::assign(Input input, int inputId)
  402  {
  403  	// input is from InputConfig* mTargetConfig
  404  
  405  	// if this input is mapped to something other than "nothing" or the current row, error
```

## src/guis/GuiMsgBox.cpp (whole, fork-modified, at the pin)

```text
    1  #include "guis/GuiMsgBox.h"
    2  
    3  #include "components/ButtonComponent.h"
    4  #include "components/MenuComponent.h"
    5  #include "components/ImageComponent.h"
    6  #include "resources/ResourceManager.h"
    7  #include "LocaleES.h"
    8  #include "TextToSpeech.h"
    9  
   10  #define HORIZONTAL_PADDING_PX  (Renderer::getScreenWidth()*0.01)
   11  
   12  // A dialog is 0.6 of the screen wide, and 0.8 when it has a paragraph to
   13  // say. The switch is measured, never matched on a string: a message that
   14  // would wrap past MSGBOX_WIDE_LINES lines at the standard width is laid out
   15  // at the wide one, so a confirmation that has to say several things -- what
   16  // goes, what arrives, what is never touched -- reads as lines and not as a
   17  // block (maintainer, 2026-09-07, the match preview on a 640-wide panel). A
   18  // short message never widens; the box still shrinks to the text's own width
   19  // when that is narrower than either cap. 0.8 is under the 0.9 that menus and
   20  // the toast use, so a dialog still reads as a dialog over the page behind it.
   21  #define MSGBOX_WIDTH           (Renderer::getScreenWidth() * 0.6f)
   22  #define MSGBOX_WIDE_WIDTH      (Renderer::getScreenWidth() * 0.8f)
   23  #define MSGBOX_WIDE_LINES      4
   24  
   25  GuiMsgBox::GuiMsgBox(Window* window, const std::string& text, const std::string& name1, const std::function<void()>& func1, GuiMsgBoxIcon icon) 
   26  	: GuiMsgBox(window, text, name1, func1, "", nullptr, "", nullptr, icon) { }
   27  
   28  GuiMsgBox::GuiMsgBox(Window* window, const std::string& text,
   29  	const std::string& name1, const std::function<void()>& func1,
   30  	const std::string& name2, const std::function<void()>& func2,
   31  	GuiMsgBoxIcon icon)
   32  	: GuiMsgBox(window, text, name1, func1, name2, func2, "", nullptr, icon) { }
   33  
   34  GuiMsgBox::GuiMsgBox(Window* window, const std::string& text, 
   35  	const std::string& name1, const std::function<void()>& func1,
   36  	const std::string& name2, const std::function<void()>& func2, 
   37  	const std::string& name3, const std::function<void()>& func3,
   38  	GuiMsgBoxIcon icon) : GuiComponent(window),
   39  	mBackground(window, ":/frame.png"), mGrid(window, Vector2i(2, 2))
   40  	
   41  {
   42  	auto theme = ThemeData::getMenuTheme();
   43  
   44  	TextToSpeech::getInstance()->say(text);
   45  
   46  	mBackground.setImagePath(theme->Background.path);
   47  	mBackground.setEdgeColor(theme->Background.color);
   48  	mBackground.setCenterColor(theme->Background.centerColor);
   49  	mBackground.setCornerSize(theme->Background.cornerSize);
   50  	mBackground.setPostProcessShader(theme->Background.menuShader);
   51  
   52  	float width = MSGBOX_WIDTH; // max width
   53  	float minWidth = Renderer::getScreenWidth() * 0.3f; // minimum width
   54  	
   55  	mImage = nullptr;
   56  
   57  	std::string imageFile;
   58  
   59  	switch (icon)
   60  	{
   61  	case ICON_INFORMATION:
   62  		imageFile = ":/info.svg";
   63  		break;
   64  	case ICON_QUESTION:
   65  		imageFile = ":/question.svg";
   66  		break;
   67  	case ICON_WARNING:
   68  		imageFile = ":/warning.svg";
   69  		break;
   70  	case ICON_ERROR:
   71  		imageFile = ":/alert.svg";
   72  		break;
   73  	case ICON_AUTOMATIC:
   74  
   75  		if (text.rfind("?") != std::string::npos || name1 == _("YES"))
   76  			imageFile = ":/question.svg";
   77  		else if (name1 == _("OK"))
   78  		{
   79  			if (name2.empty())
   80  				imageFile = ":/info.svg";
   81  			else
   82  				imageFile = ":/question.svg";
   83  		}
   84  
   85  		break;
   86  	}
   87  
   88    // ensure the tailscale message doesn't wrap, and no icon (for more room)
   89  	if (text.find("tailscale.com") != std::string::npos)
   90  	{
   91  			width = Renderer::getScreenWidth() * 0.9f; // max width
   92  	} else if (!imageFile.empty() && ResourceManager::getInstance()->fileExists(imageFile) && !Renderer::isSmallScreen())
   93  	{
   94  		mImage = std::make_shared<ImageComponent>(window);
   95  		mImage->setImage(imageFile);
   96  		mImage->setIsLinear(true);
   97  		mImage->setColorShift(theme->Text.color);
   98  		mImage->setOrigin(0.5f, 0.5f);
   99  		mImage->setMaxSize(theme->Text.font->getLetterHeight() * 2.0f, theme->Text.font->getLetterHeight() * 2.0f);		
  100  
  101  		mGrid.setEntry(mImage, Vector2i(0, 0), false, false);
  102  	}
  103  
  104  	mMsg = std::make_shared<TextComponent>(mWindow, text, ThemeData::getMenuTheme()->Text.font, ThemeData::getMenuTheme()->Text.color, mImage == nullptr || Renderer::isSmallScreen() ? ALIGN_CENTER : ALIGN_LEFT); // CENTER
  105  	mMsg->setPadding(Vector4f(Renderer::getScreenWidth()*0.015f, 0, Renderer::getScreenWidth()*0.015f, 0));
  106  	
  107  	mGrid.setEntry(mMsg, Vector2i(mImage == nullptr ? 0 : 1, 0), false, false, Vector2i(mImage == nullptr ? 2 : 1, 1));
  108  
  109  	// create the buttons
  110  	mButtons.push_back(std::make_shared<ButtonComponent>(mWindow, name1, name1, std::bind(&GuiMsgBox::deleteMeAndCall, this, func1)));
  111  	if(!name2.empty())
  112  		mButtons.push_back(std::make_shared<ButtonComponent>(mWindow, name2, name2, std::bind(&GuiMsgBox::deleteMeAndCall, this, func2)));
  113  	if(!name3.empty())
  114  		mButtons.push_back(std::make_shared<ButtonComponent>(mWindow, name3, name3, std::bind(&GuiMsgBox::deleteMeAndCall, this, func3)));
  115  
  116  	// set accelerator automatically (button to press when BUTTON_BACK is pressed)
  117  	if(mButtons.size() == 1)
  118  	{
  119  		mAcceleratorFunc = mButtons.front()->getPressedFunc();
  120  	}
  121  	else if (mButtons.size() > 0)
  122  	{
  123  		for(auto it = mButtons.cbegin(); it != mButtons.cend(); it++)
  124  		{
  125  			if(Utils::String::toUpper((*it)->getText()) == _("OK") || Utils::String::toUpper((*it)->getText()) == _("NO"))
  126  			{
  127  				mAcceleratorFunc = (*it)->getPressedFunc();
  128  				break;
  129  			}
  130  		}
  131  
  132  		if (mAcceleratorFunc == nullptr)
  133  			mAcceleratorFunc = mButtons.back()->getPressedFunc();
  134  	}
  135  
  136  	// put the buttons into a ComponentGrid
  137  	mButtonGrid = makeButtonGrid(mWindow, mButtons);
  138  	mGrid.setEntry(mButtonGrid, Vector2i(0, 1), true, false, Vector2i(2, 1), GridFlags::BORDER_TOP);
  139  
  140  	// A paragraph gets the wide box (see MSGBOX_WIDE_LINES). Measured with
  141  	// the text's own font at the width the text would actually get.
  142  	if (width < MSGBOX_WIDE_WIDTH)
  143  	{
  144  		float textWidth = width - 3 * HORIZONTAL_PADDING_PX;
  145  		if (mImage != nullptr)
  146  			textWidth -= mImage->getSize().x() + 2 * HORIZONTAL_PADDING_PX;
  147  		const float lineHeight = mMsg->getFont()->getHeight();
  148  		if (lineHeight > 0 && mMsg->getFont()->sizeWrappedText(text, textWidth).y() > lineHeight * MSGBOX_WIDE_LINES)
  149  			width = MSGBOX_WIDE_WIDTH;
  150  	}
  151  
  152  	// decide final width
  153  	if(mMsg->getSize().x() < width && mButtonGrid->getSize().x() < width)
  154  	{
  155  		// mMsg and buttons are narrower than width
  156  		width = Math::max(mButtonGrid->getSize().x(), mMsg->getSize().x() + 3 * HORIZONTAL_PADDING_PX);
  157  
  158  		if (mImage != nullptr)
  159  			width += mImage->getSize().x() + 2 * HORIZONTAL_PADDING_PX;
  160  
  161  		width = Math::max(width, minWidth);
  162  	}
  163  	
  164  	// now that we know width, we can find height
  165  	mMsg->setSize(width, 0); // mMsg->getSize.y() now returns the proper length
  166  
  167  	// ...except that it does not, and on a small panel the difference puts
  168  	// the OK button on top of the message (#48).
  169  	//
  170  	// A TextComponent measures its automatic height by wrapping at its full
  171  	// width -- onTextChanged() calls sizeWrappedText(text, getSize().x()) --
  172  	// and draws by wrapping at its width minus its own horizontal padding:
  173  	// buildTextCache() lays the glyphs out at sx = mSize.x() - mPadding.x()
  174  	// - mPadding.z(). mMsg carries 0.015 of the screen on each side, so on a
  175  	// 640-wide panel the glyphs wrap at 364.8px in a box measured at 384 --
  176  	// 5% narrower than the height was measured for, 3.75% in the wide box --
  177  	// and the drawn text gains a line whenever a wrap point falls in that
  178  	// band.
  179  	//
  180  	// Nothing catches the extra line: a TextComponent with no autoscroll
  181  	// pushes no clip rect, so it paints straight through whatever is under
  182  	// it, which here is the button row.
  183  	//
  184  	// The 1.225 below is what hid it. It buys 0.225 of a line per line, so
  185  	// a message of five drawn lines or more absorbs one extra line and a
  186  	// shorter one does not -- and how many lines a message has depends on
  187  	// the panel, since the box is a fraction of the screen and the font is
  188  	// not scaled with it in the same proportion. That is why the same
  189  	// dialog is fine on a 1080p VM and has its button sitting on the text
  190  	// of an RG35XX SP. The bug is not the small screen; it is that the
  191  	// dialog measured one thing and drew another.
  192  	//
  193  	// So measure the height at the width the glyphs are actually laid out
  194  	// at. sizeWrappedText is sizeText(wrapText(text, xLen)) and
  195  	// buildTextCache is buildTextCache(wrapText(text, sx)), so the two agree
  196  	// exactly once they are given the same xLen. This is also the width the
  197  	// wide-box test above already measures at.
  198  	const Vector4f msgPadding = mMsg->getPadding();
  199  	const float drawnWidth = width - msgPadding.x() - msgPadding.z();
  200  	float drawnHeight = mMsg->getSize().y();
  201  	if (mMsg->getFont() != nullptr && drawnWidth > 0)
  202  		drawnHeight = mMsg->getFont()->sizeWrappedText(text, drawnWidth).y() + msgPadding.y() + msgPadding.w();
  203  
  204  	float msgHeight = Math::max(Font::get(FONT_SIZE_LARGE)->getHeight(), drawnHeight*1.225f);
  205  	
  206  	if (msgHeight + mButtonGrid->getSize().y() > Renderer::getScreenHeight())
  207  	{
  208  		// The message alone is taller than the screen. onSizeChanged() does
  209  		// constrain mMsg to the grid row left above the buttons, but a
  210  		// TextComponent renders at its natural height regardless of that
  211  		// bound unless it is scrolling -- so the text painted straight
  212  		// through the button row and the buttons appeared on top of it.
  213  		// Seen on an RG35XX SP with a two-paragraph message; a
  214  		// desktop-resolution VM never reaches this branch, which is why it
  215  		// survived to hardware.
  216  		//
  217  		// Set before setSize so the flag is live when onSizeChanged() runs.
  218  		// The grid still owns the geometry; this only makes the text respect it.
  219  		mMsg->setAutoScroll(TextComponent::AutoScrollType::VERTICAL);
  220  
  221  		setSize(Renderer::getScreenWidth(), Renderer::getScreenHeight());
  222  		if (mImage != nullptr)
  223  			mMsg->setSize(Renderer::getScreenWidth() - mImage->getSize().x() - 4* HORIZONTAL_PADDING_PX, 0);
  224  	}
  225  	else
  226  		setSize(width + HORIZONTAL_PADDING_PX*2, msgHeight + mButtonGrid->getSize().y());
  227  
  228  	// center for good measure
  229  	setPosition((Renderer::getScreenWidth() - mSize.x()) / 2.0f, (Renderer::getScreenHeight() - mSize.y()) / 2.0f);
  230  
  231  	addChild(&mBackground);
  232  	addChild(&mGrid);
  233  
  234  	TextToSpeech::getInstance()->say(text);
  235  
  236  	for (auto btn : mButtons)
  237  	{
  238  		if (btn->hasFocus())
  239  		{
  240  			TextToSpeech::getInstance()->say(btn->getText(), true);
  241  			break;
  242  		}
  243  	}
  244  }
  245  
  246  bool GuiMsgBox::input(InputConfig* config, Input input)
  247  {
  248  	// special case for when GuiMsgBox comes up to report errors before anything has been configured
  249  	if(config->getDeviceId() == DEVICE_KEYBOARD && !config->isConfigured() && input.value && 
  250  		(input.id == SDLK_RETURN || input.id == SDLK_ESCAPE || input.id == SDLK_SPACE))
  251  	{
  252  		mAcceleratorFunc();
  253  		return true;
  254  	}
  255  
  256  	/* when it's not configured, allow to remove the message box too to allow the configdevice window a chance */
  257  	if(mAcceleratorFunc && ((config->isMappedTo(BUTTON_BACK, input) && input.value != 0) || (config->isConfigured() == false && input.type == TYPE_BUTTON))) 
  258  	{
  259  		mAcceleratorFunc();
  260  		return true;
  261  	}
  262  
  263  	return GuiComponent::input(config, input);
  264  }
  265  
  266  void GuiMsgBox::onSizeChanged()
  267  {
  268  	GuiComponent::onSizeChanged();
  269  
  270  	mGrid.setSize(mSize);
  271  
  272  	if (mImage != nullptr)
  273  	{
  274  		auto width = mImage->getSize().x() + (Renderer::isSmallScreen() ? 5 : 2) * HORIZONTAL_PADDING_PX;
  275  		mGrid.setColWidthPerc(0, width / mSize.x(), true);
  276  	}
  277  
  278  	mGrid.setRowHeightPerc(1, mButtonGrid->getSize().y() / mSize.y());
  279  			
  280  	mMsg->setSize(mSize.x() - HORIZONTAL_PADDING_PX*2, mGrid.getRowHeight(0));
  281  	mGrid.onSizeChanged();
  282  
  283  	mBackground.fitTo(mSize, Vector3f::Zero(), Vector2f(-32, -32));
  284  }
  285  
  286  void GuiMsgBox::deleteMeAndCall(const std::function<void()>& func)
  287  {
  288  	auto funcCopy = func;
  289  	delete this;
  290  
  291  	if(funcCopy)
  292  		funcCopy();
  293  
  294  }
  295  
  296  std::vector<HelpPrompt> GuiMsgBox::getHelpPrompts()
  297  {
  298  	return mGrid.getHelpPrompts();
  299  }
```

## src/guis/GuiTextEditPopup.cpp (whole, fork-modified, at the pin)

```text
    1  #include "guis/GuiTextEditPopup.h"
    2  
    3  #include "components/ButtonComponent.h"
    4  #include "components/MenuComponent.h"
    5  #include "LocaleES.h"
    6  #include "components/TextEditComponent.h"
    7  
    8  GuiTextEditPopup::GuiTextEditPopup(Window* window, const std::string& title, const std::string& initValue, 
    9  	const std::function<void(const std::string&)>& okCallback, bool multiLine, const char* acceptBtnText)
   10  	: GuiComponent(window), mBackground(window, ":/frame.png"), mGrid(window, Vector2i(1, 3)), mMultiLine(multiLine)
   11  {
   12  	setTag("popup");
   13  
   14  	auto theme = ThemeData::getMenuTheme();
   15  	mBackground.setImagePath(theme->Background.path);
   16  	mBackground.setEdgeColor(theme->Background.color);
   17  	mBackground.setCenterColor(theme->Background.centerColor);
   18  	mBackground.setCornerSize(theme->Background.cornerSize);
   19  	mBackground.setPostProcessShader(theme->Background.menuShader);
   20  
   21  	addChild(&mBackground);
   22  	addChild(&mGrid);
   23  
   24  	mTitle = std::make_shared<TextComponent>(mWindow, Utils::String::toUpper(title), theme->Title.font, theme->Title.color, ALIGN_CENTER);
   25  
   26  	mText = std::make_shared<TextEditComponent>(mWindow);
   27  	mText->setValue(initValue);
   28  
   29  	if(!multiLine)
   30  		mText->setCursor(initValue.size());
   31  
   32  	std::vector< std::shared_ptr<ButtonComponent> > buttons;
   33  	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, acceptBtnText, acceptBtnText, [this, okCallback] { okCallback(mText->getValue()); delete this; }));
   34  	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, _("CLEAR"), _("CLEAR"), [this, okCallback] { okCallback(""); delete this; }));
   35  	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, _("CANCEL"), _("DISCARD CHANGES"), [this] { delete this; })); 
   36  
   37  	mButtonGrid = makeButtonGrid(mWindow, buttons);
   38  
   39  	mGrid.setEntry(mTitle, Vector2i(0, 0), false, true);
   40  	mGrid.setEntry(mText, Vector2i(0, 1), true, false, Vector2i(1, 1), GridFlags::BORDER_TOP | GridFlags::BORDER_BOTTOM);
   41  	mGrid.setEntry(mButtonGrid, Vector2i(0, 2), true, false);
   42  
   43  	float textHeight = mText->getFont()->getHeight();
   44  	if(multiLine)
   45  		textHeight *= 6;
   46  	mText->setSize(0, textHeight);
   47  
   48  	setSize(Renderer::getScreenWidth() * 0.5f, mTitle->getFont()->getHeight() + textHeight + mButtonGrid->getSize().y() + 40);
   49  	setPosition((Renderer::getScreenWidth() - mSize.x()) / 2, (Renderer::getScreenHeight() - mSize.y()) / 2);
   50  }
   51  
   52  void GuiTextEditPopup::onSizeChanged()
   53  {
   54  	GuiComponent::onSizeChanged();
   55  
   56  	mBackground.fitTo(mSize, Vector3f::Zero(), Vector2f(-32, -32));
   57  
   58  	mText->setSize(mSize.x() - 40, mText->getSize().y());
   59  
   60  	// update grid
   61  	mGrid.setRowHeightPerc(0, mTitle->getFont()->getHeight() / mSize.y());
   62  	mGrid.setRowHeightPerc(2, mButtonGrid->getSize().y() / mSize.y());
   63  	mGrid.setSize(mSize);
   64  }
   65  
   66  bool GuiTextEditPopup::input(InputConfig* config, Input input)
   67  {
   68  	if(GuiComponent::input(config, input))
   69  		return true;
   70  
   71  	// pressing back when not text editing closes us
   72  	if(config->isMappedTo(BUTTON_BACK, input) && input.value)
   73  	{
   74  		delete this;
   75  		return true;
   76  	}
   77  
   78  	return false;
   79  }
   80  
   81  std::vector<HelpPrompt> GuiTextEditPopup::getHelpPrompts()
   82  {
   83  	std::vector<HelpPrompt> prompts = mGrid.getHelpPrompts();
   84  	prompts.push_back(HelpPrompt(BUTTON_BACK, _("BACK")));
   85  	return prompts;
   86  }
```

## src/guis/GuiTextEditPopup.h `:7-24` (an excerpt, upstream-carried, at the pin)

```text
    7  #include "GuiComponent.h"
    8  
    9  class TextComponent;
   10  class TextEditComponent;
   11  
   12  class GuiTextEditPopup : public GuiComponent
   13  {
   14  public:
   15  	GuiTextEditPopup(Window* window, const std::string& title, const std::string& initValue, 
   16  		const std::function<void(const std::string&)>& okCallback, bool multiLine, const char* acceptBtnText = "OK");
   17  
   18  	bool input(InputConfig* config, Input input);
   19  	void onSizeChanged();
   20  	std::vector<HelpPrompt> getHelpPrompts() override;
   21  
   22  private:
   23  	NinePatchComponent mBackground;
   24  	ComponentGrid mGrid;
```

## src/guis/GuiTextEditPopupKeyboard.cpp (whole, fork-modified, at the pin)

```text
    1  #include "guis/GuiTextEditPopupKeyboard.h"
    2  #include "components/MenuComponent.h"
    3  #include "utils/StringUtil.h"
    4  #include "Log.h"
    5  #include "LocaleES.h"
    6  #include "SystemConf.h"
    7  
    8  #define OSK_WIDTH (Renderer::ScreenSettings::fullScreenMenus() ? Renderer::getScreenWidth() : Renderer::getScreenWidth() * 0.78f)
    9  #define OSK_HEIGHT (Renderer::ScreenSettings::fullScreenMenus() ? Renderer::getScreenHeight() : Renderer::getScreenHeight() * 0.60f)
   10  
   11  #define OSK_PADDINGX (Renderer::getScreenWidth() * 0.02f)
   12  #define OSK_PADDINGY (Renderer::getScreenWidth() * 0.01f)
   13  
   14  #define BUTTON_GRID_HORIZ_PADDING (Renderer::getScreenWidth()*0.0052083333)
   15  #define BUTTON_LAYER_SIZE (4)
   16  
   17  std::vector<std::vector<const char*>> kbUs {
   18  
   19  	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_", "+", "DEL" },
   20  	{ "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "DEL" },
   21  	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_", "+", "DEL" },
   22  	{ "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "DEL" },
   23  
   24  	{ "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "{", "}", "OK" },
   25  	{ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "OK" },
   26  	{ "à", "ä", "è", "ë", "ì", "ï", "ò", "ö", "ù", "ü", "¨", "¿", "OK" },
   27  	{ "à", "ä", "è", "ë", "ì", "ï", "ò", "ö", "ù", "ü", "¨", "¿", "OK" },
   28  
   29  	{ "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "\"", "|", "-rowspan-" },
   30  	{ "A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "'", "\\", "-rowspan-" },
   31  	{ "á", "â", "é", "ê", "í", "î", "ó", "ô", "ú", "û", "ñ", "¡", "-rowspan-" },
   32  	{ "á", "â", "é", "ê", "í", "î", "ó", "ô", "ú", "û", "ñ", "¡", "-rowspan-" },
   33  
   34  	{ "~", "z", "x", "c", "v", "b", "n", "m", ",", ".", "?", "ALT", "-colspan-" },
   35  	{ "`", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "/", "ALT", "-colspan-" },
   36  	{ "€", "", "", "", "", "", "", "", "", "", "", "ALT", "-colspan-" },
   37  	{ "€", "", "", "", "", "", "", "", "", "", "", "ALT", "-colspan-" },
   38  
   39  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
   40  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
   41  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
   42  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" }
   43  };
   44  
   45  std::vector<std::vector<const char*>> kbFr {
   46  	{ "&", "é", "\"", "'", "(", "#", "è", "!", "ç", "à", ")", "-", "DEL" },
   47  	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "_", "DEL" },
   48  	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "_", "DEL" },
   49  	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "_", "DEL" },
   50  
   51  	{ "a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "^", "$", "OK" },
   52  	{ "A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "¨", "*", "OK" },
   53  	{ "à", "ä", "ë", "ì", "ï", "ò", "ö", "ü", "\\", "|", "§", "°", "OK" },
   54  	{ "à", "ä", "ë", "ì", "ï", "ò", "ö", "ü", "\\", "|", "§", "°", "OK" },
   55  
   56  	{ "q", "s", "d", "f", "g", "h", "j", "k", "l", "m", "ù", "`", "-rowspan-" },
   57  	{ "Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "%", "£", "-rowspan-" },
   58  	{ "á", "â", "ê", "í", "î", "ó", "ô", "ú", "û", "ñ", "¡", "¿", "-rowspan-" },
   59  	{ "á", "â", "ê", "í", "î", "ó", "ô", "ú", "û", "ñ", "¡", "¿", "-rowspan-" },
   60  
   61  	{ "<", "w", "x", "c", "v", "b", "n", ",", ";", ":", "=", "ALT", "-colspan-" },
   62  	{ ">", "W", "X", "C", "V", "B", "N", "?", ".", "/", "+", "ALT", "-colspan-" },
   63  	{ "€", "[", "]", "{", "}", "", "", "", "", "", "", "ALT", "-colspan-" },
   64  	{ "€", "[", "]", "{", "}", "", "", "", "", "", "", "ALT", "-colspan-" },
   65  
   66  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
   67  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
   68  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
   69  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" }
   70  };
   71  
   72  std::vector<std::vector<const char*>> kbKr{
   73  	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "DEL" },
   74  	{ "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "DEL" },
   75  	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "DEL" },
   76  	{ "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "DEL" },
   77  
   78  	{ "ㅂ", "ㅈ", "ㄷ", "ㄱ", "ㅅ", "ㅛ", "ㅕ", "ㅑ", "ㅐ", "ㅔ", "[", "]", "OK" },
   79  	{ "ㅃ", "ㅉ", "ㄸ", "ㄲ", "ㅆ", "ㅛ", "ㅕ", "ㅑ", "ㅒ", "ㅖ", "{", "}", "OK" },
   80  	{ "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "OK" },
   81  	{ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "OK" },
   82  
   83  	{ "ㅁ", "ㄴ", "ㅇ", "ㄹ", "ㅎ", "ㅗ", "ㅓ", "ㅏ", "ㅣ", ";", "'", "\\", "-rowspan-" },
   84  	{ "ㅁ", "ㄴ", "ㅇ", "ㄹ", "ㅎ", "ㅗ", "ㅓ", "ㅏ", "ㅣ", ":", "\"", "|", "-rowspan-" },
   85  	{ "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "\\", "-rowspan-" },
   86  	{ "A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\"", "|", "-rowspan-" },
   87  
   88  	{ "ㅋ", "ㅌ", "ㅊ", "ㅍ", "ㅠ", "ㅜ", "ㅡ", ",", ".", "/", "`", "ALT", "-colspan-" },
   89  	{ "ㅋ", "ㅌ", "ㅊ", "ㅍ", "ㅠ", "ㅜ", "ㅡ", "<", ">", "?", "~", "ALT", "-colspan-" },
   90  	{ "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "`", "ALT", "-colspan-" },
   91  	{ "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "~", "ALT", "-colspan-" },
   92  
   93  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
   94  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
   95  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
   96  	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" }
   97  };
   98  
   99  GuiTextEditPopupKeyboard::GuiTextEditPopupKeyboard(Window* window, const std::string& title, const std::string& initValue,
  100  	const std::function<void(const std::string&)>& okCallback, bool multiLine, const std::string acceptBtnText)
  101  	: GuiComponent(window), mBackground(window, ":/frame.png"), mGrid(window, Vector2i(1, 6)), mMultiLine(multiLine)
  102  {
  103  	setTag("popup");
  104  
  105  	mOkCallback = okCallback;
  106  
  107  	auto theme = ThemeData::getMenuTheme();
  108  	mBackground.setImagePath(theme->Background.path);
  109  	mBackground.setEdgeColor(theme->Background.color);
  110  	mBackground.setCenterColor(theme->Background.centerColor);
  111  	mBackground.setCornerSize(theme->Background.cornerSize);
  112  	mBackground.setPostProcessShader(theme->Background.menuShader);
  113  
  114  	addChild(&mBackground);
  115  	addChild(&mGrid);
  116  
  117  	mTitle = std::make_shared<TextComponent>(mWindow, Utils::String::toUpper(title), theme->Title.font, theme->Title.color, ALIGN_CENTER);
  118  	
  119  	mKeyboardGrid = std::make_shared<ComponentGrid>(mWindow, Vector2i(kbUs[0].size(), kbUs.size() / BUTTON_LAYER_SIZE));
  120  
  121  	mText = std::make_shared<TextEditComponent>(mWindow);
  122  	mText->setValue(initValue);
  123  
  124  	if (!multiLine)
  125  		mText->setCursor(initValue.size());
  126  
  127  	// Header
  128  	mGrid.setEntry(mTitle, Vector2i(0, 0), false, true);
  129  
  130  	// Text edit add
  131  	mGrid.setEntry(mText, Vector2i(0, 1), true, false, Vector2i(1, 1), GridFlags::BORDER_TOP);
  132  
  133  	std::vector< std::vector< std::shared_ptr<ButtonComponent> > > buttonList;
  134  
  135  	// Keyboard
  136  	// Case for if multiline is enabled, then don't create the keyboard.
  137  	// if (!mMultiLine) 
  138  	{
  139  		std::vector<std::vector<const char*>>* layout = &kbUs;
  140  
  141  		std::string language = SystemConf::getInstance()->get("system.language");
  142  		if (!language.empty())
  143  		{
  144  			auto shortNameDivider = language.find("_");
  145  			if (shortNameDivider != std::string::npos)
  146  				language = Utils::String::toLower(language.substr(0, shortNameDivider));
  147  		}
  148  
  149  		if (language == "fr")
  150  			layout = &kbFr;
  151  		else if (language == "ko")
  152  			layout = &kbKr;
  153  
  154  		for (unsigned int i = 0; i < layout->size() / BUTTON_LAYER_SIZE; i++)
  155  		{			
  156  			std::vector<std::shared_ptr<ButtonComponent>> buttons;
  157  			for (unsigned int j = 0; j < (*layout)[i].size(); j++)
  158  			{
  159  				std::string lower = (*layout)[BUTTON_LAYER_SIZE * i][j];
  160  				if (lower.empty() || lower == "-rowspan-" || lower == "-colspan-")
  161  					continue;
  162  
  163  				std::string upper = (*layout)[BUTTON_LAYER_SIZE * i + 1][j];
  164  				std::string lowerAlted = (*layout)[BUTTON_LAYER_SIZE * i + 2][j];
  165  				std::string upperAlted = (*layout)[BUTTON_LAYER_SIZE * i + 3][j];
  166  
  167  				std::shared_ptr<ButtonComponent> button = nullptr;
  168  
  169  				if (lower == "DEL")
  170  				{
  171  					lower = _U("\uF177");
  172  					upper = _U("\uF177");
  173  					lowerAlted = _U("\uF177");
  174  					upperAlted = _U("\uF177");
  175  				}
  176  				else if (lower == "OK")
  177  				{
  178  					lower = _U("\uF058");
  179  
  180  					if (mMultiLine)
  181  					{
  182  						upper = _U("\uF149");
  183  						lowerAlted = _U("\uF149");
  184  						upperAlted = _U("\uF149");
  185  					}
  186  					else
  187  					{
  188  						upper = _U("\uF058");
  189  						lowerAlted = _U("\uF058");
  190  						upperAlted = _U("\uF058");
  191  					}
  192  				}
  193  				else if (lower == "SPACE")
  194  				{
  195  					lower = " ";
  196  					upper = " ";
  197  				}
  198  				else if (lower != "SHIFT" && lower.length() > 1)
  199  				{
  200  					lower = _(lower.c_str());
  201  					upper = _(upper.c_str());
  202  					lowerAlted = _(lowerAlted.c_str());
  203  					upperAlted = _(upperAlted.c_str());
  204  				}
  205  
  206  				if (lower == "SHIFT")
  207  				{
  208  					// Special case for shift key
  209  					mShiftButton = std::make_shared<ButtonComponent>(mWindow, _U("\uF176"), _("SHIFTS FOR UPPER, LOWER, AND SPECIAL"), [this] { shiftKeys(); }, false);					
  210  					button = mShiftButton;
  211  				}
  212  				else if (lower == "ALT")
  213  				{
  214  					mAltButton = std::make_shared<ButtonComponent>(mWindow, _U("\uF141"), _("ALT GR"), [this] { altKeys(); }, false);
  215  					button = mAltButton;
  216  				}
  217  				else
  218  					button = makeButton(lower, upper, lowerAlted, upperAlted);
  219  
  220  				button->setPadding(Vector4f(BUTTON_GRID_HORIZ_PADDING / 4.0f, BUTTON_GRID_HORIZ_PADDING / 4.0f, BUTTON_GRID_HORIZ_PADDING / 4.0f, BUTTON_GRID_HORIZ_PADDING / 4.0f));
  221  				button->setRenderNonFocusedBackground(false);
  222  				buttons.push_back(button);
  223  
  224  				int colSpan = 1;
  225  				for (unsigned int cs = j + 1; cs < (*layout)[i].size(); cs++)
  226  				{
  227  					if (std::string((*layout)[BUTTON_LAYER_SIZE * i][cs]) == "-colspan-")
  228  						colSpan++;
  229  					else
  230  						break;
  231  				}
  232  				
  233  				int rowSpan = 1;
  234  				for (unsigned int cs = (BUTTON_LAYER_SIZE * i) + BUTTON_LAYER_SIZE; cs < layout->size(); cs += BUTTON_LAYER_SIZE)
  235  				{
  236  					if (std::string((*layout)[cs][j]) == "-rowspan-")
  237  						rowSpan++;
  238  					else
  239  						break;
  240  				}
  241  
  242  				mKeyboardGrid->setEntry(button, Vector2i(j, i), true, true, Vector2i(colSpan, rowSpan));
  243  
  244  				buttonList.push_back(buttons);
  245  			}
  246  		}		
  247  		// END KEYBOARD IF
  248  	}
  249  
  250  	// Add keyboard keys
  251  	mGrid.setEntry(mKeyboardGrid, Vector2i(0, 2), true, true, Vector2i(2, 4));
  252  
  253  	// Determine size from text size
  254  	float textHeight = mText->getFont()->getHeight();
  255  	if (multiLine)
  256  		textHeight *= 4;
  257  
  258  	mText->setSize(0, textHeight);
  259  
  260  	mGrid.setUnhandledInputCallback([this](InputConfig* config, Input input) -> bool 
  261  	{		
  262  		if (config->isMappedLike("down", input)) 
  263  		{
  264  			mGrid.setCursorTo(mText);
  265  			return true;
  266  		}
  267  		else if (config->isMappedLike("up", input)) 
  268  		{
  269  			mGrid.setCursorTo(mKeyboardGrid);
  270  			return true;
  271  		}
  272  		else if (config->isMappedLike("left", input))
  273  		{		
  274  			if (mGrid.getSelectedComponent() == mKeyboardGrid)
  275  			{
  276  				Vector2i curCursor = mKeyboardGrid->getCursor();
  277  				mKeyboardGrid->setCursorTo(Vector2i(kbUs[0].size() - 1, curCursor.y()));
  278  				return true;
  279  			}
  280  		}
  281  		else if (config->isMappedLike("right", input))
  282  		{
  283  			if (mGrid.getSelectedComponent() == mKeyboardGrid)
  284  			{
  285  				Vector2i curCursor = mKeyboardGrid->getCursor();
  286  				mKeyboardGrid->setCursorTo(Vector2i(0, curCursor.y()));
  287  				return true;
  288  			}
  289  		}
  290  
  291  		return false;
  292  	});
  293  
  294  	
  295  	// If multiline, set all diminsions back to default, else draw size for keyboard.
  296  	if (mMultiLine) 
  297  	{
  298  		if (Renderer::ScreenSettings::fullScreenMenus())
  299  			setSize(OSK_WIDTH, Renderer::getScreenHeight());
  300  		else
  301  			setSize(OSK_WIDTH, OSK_HEIGHT - mText->getFont()->getHeight() + textHeight);
  302  
  303  		setPosition((Renderer::getScreenWidth() - mSize.x()) / 2, (Renderer::getScreenHeight() - mSize.y()) / 2);
  304  	}
  305  	else
  306  	{
  307  		//setSize(OSK_WIDTH, mTitle->getFont()->getHeight() + textHeight + 40 + (Renderer::getScreenHeight() * 0.085f) * 6);
  308  		setSize(OSK_WIDTH, OSK_HEIGHT);
  309  		setPosition((Renderer::getScreenWidth() - mSize.x()) / 2, (Renderer::getScreenHeight() - mSize.y()) / 2);
  310  		animateTo(Vector2f((Renderer::getScreenWidth() - mSize.x()) / 2, (Renderer::getScreenHeight() - mSize.y()) / 2));
  311  	}
  312  }
  313  
  314  void GuiTextEditPopupKeyboard::onSizeChanged()
  315  {
  316  	GuiComponent::onSizeChanged();
  317  
  318  	mBackground.fitTo(mSize, Vector3f::Zero(), Vector2f(-32, -32));
  319  
  320  	mText->setSize(mSize.x() - (2 * OSK_PADDINGX), mText->getSize().y());
  321  
  322  	// update grid
  323  	mGrid.setRowHeight(0, mTitle->getFont()->getHeight() + OSK_PADDINGY);
  324  	mGrid.setRowHeight(1, mText->getSize().y() + 2 * OSK_PADDINGY);
  325  	mGrid.setRowHeight(2, mKeyboardGrid->getSize().y());
  326  	mGrid.setSize(mSize);
  327  
  328  	auto pos = mKeyboardGrid->getPosition();
  329  	auto sz = mKeyboardGrid->getSize();
  330  
  331  	mKeyboardGrid->setSize(mSize.x() - OSK_PADDINGX - OSK_PADDINGX, sz.y() - OSK_PADDINGY); // Small margin between buttons
  332  	mKeyboardGrid->setPosition(OSK_PADDINGX, pos.y());	
  333  }
  334  
  335  bool GuiTextEditPopupKeyboard::input(InputConfig* config, Input input)
  336  {
  337  	if (GuiComponent::input(config, input))
  338  		return true;
  339  
  340  	// pressing start
  341  	if (config->isMappedTo("start", input) && input.value)
  342  	{
  343  		if (mOkCallback)
  344  			mOkCallback(mText->getValue());
  345  
  346  		delete this;
  347  		return true;
  348  	}
  349  
  350  	if ((config->getDeviceId() == DEVICE_KEYBOARD && input.id == SDLK_ESCAPE))
  351  	{
  352  		delete this;
  353  		return true;
  354  	}
  355  
  356  	// pressing back when not text editing closes us
  357  	if (config->isMappedTo(BUTTON_BACK, input) && input.value)
  358  	{
  359  		delete this;
  360  		return true;
  361  	}
  362  
  363  	// For deleting a chara (Left Top Button)
  364  	if (config->isMappedTo("leftshoulder", input) && input.value) {
  365  		bool editing = mText->isEditing();
  366  		if (!editing)
  367  			mText->startEditing();
  368  
  369  		mText->textInput("\b");
  370  
  371  		if (!editing)
  372  			mText->stopEditing();
  373  	}
  374  
  375  	// For Adding a space (Right Top Button)
  376  	if (config->isMappedTo("rightshoulder", input) && input.value)
  377  	{
  378  		bool editing = mText->isEditing();
  379  		if (!editing)
  380  			mText->startEditing();
  381  
  382  		mText->textInput(" ");
  383  
  384  		if (!editing)
  385  			mText->stopEditing();
  386  	}
  387  
  388  	// For Shifting (Y)
  389  	if (config->isMappedTo("y", input) && input.value) 
  390  		shiftKeys();
  391  
  392  	if (config->isMappedTo("x", input) && input.value && mOkCallback != nullptr)
  393  	{
  394  		mOkCallback(""); 
  395  		delete this;
  396  		return true;
  397  	}
  398  
  399  	return false;
  400  }
  401  
  402  void GuiTextEditPopupKeyboard::toggleKeyState(bool& state, std::shared_ptr<ButtonComponent>& button)
  403  {
  404  	state = !state;
  405  
  406  	if (state)
  407  	{
  408  		button->setRenderNonFocusedBackground(true);
  409  		button->setColorShift(0xFF0000FF);
  410  	}
  411  	else
  412  	{
  413  		button->setRenderNonFocusedBackground(false);
  414  		button->removeColorShift();
  415  	}
  416  
  417  	updateKeyboardButtons();
  418  }
  419  
  420  void GuiTextEditPopupKeyboard::updateKeyboardButtons()
  421  {
  422  	for (auto& kb : keyboardButtons)
  423  	{
  424  		const std::string& text = (mAlt && mShift) ? kb.altedShiftedKey
  425  			: (mAlt) ? kb.altedKey
  426  			: (mShift) ? kb.shiftedKey
  427  			: kb.key;
  428  
  429  		auto sz = kb.button->getSize();
  430  		kb.button->setText(text, text, false);
  431  		kb.button->setSize(sz);
  432  	}
  433  }
  434  
  435  // Shifts the keys when user hits the shift button.
  436  void GuiTextEditPopupKeyboard::shiftKeys() 
  437  {
  438  	toggleKeyState(mShift, mShiftButton);
  439  }
  440  
  441  void GuiTextEditPopupKeyboard::altKeys()
  442  {
  443  	if (mShift)
  444  		toggleKeyState(mShift, mShiftButton);
  445  
  446  	toggleKeyState(mAlt, mAltButton);
  447  }
  448  
  449  std::vector<HelpPrompt> GuiTextEditPopupKeyboard::getHelpPrompts()
  450  {
  451  	std::vector<HelpPrompt> prompts = mGrid.getHelpPrompts();
  452  
  453  	if (mOkCallback != nullptr)
  454  		prompts.push_back(HelpPrompt("x", _("CLEAR")));
  455  
  456  	prompts.push_back(HelpPrompt("y", _("SHIFT")));
  457  	prompts.push_back(HelpPrompt("start", _("OK")));
  458  	prompts.push_back(HelpPrompt(BUTTON_BACK, _("BACK")));
  459  	prompts.push_back(HelpPrompt("r", _("SPACE")));
  460  	prompts.push_back(HelpPrompt("l", _("DELETE")));
  461  	return prompts;
  462  }
  463  
  464  std::shared_ptr<ButtonComponent> GuiTextEditPopupKeyboard::makeButton(const std::string& key, const std::string& shiftedKey, const std::string& altedKey, const std::string& altedShiftedKey)
  465  {
  466  	std::shared_ptr<ButtonComponent> button = std::make_shared<ButtonComponent>(mWindow, key, key, [this, key, shiftedKey, altedKey, altedShiftedKey]
  467  	{						
  468  		if (key == _U("\uF058") || key.find("OK") != std::string::npos)
  469  		{	
  470  			if (mMultiLine && (mShift || mAlt))
  471  			{
  472  				mText->startEditing(); mText->textInput("\r\n"); mText->stopEditing();
  473  			}
  474  			else
  475  			{
  476  				mOkCallback(mText->getValue());
  477  				delete this;
  478  			}
  479  			return;
  480  		}
  481  		else if (key == _U("\uF177") || key == "DEL")
  482  		{
  483  			mText->startEditing(); mText->textInput("\b"); mText->stopEditing();
  484  			return;
  485  		}
  486  		else if (key == _("SPACE") || key == " ")
  487  		{
  488  			mText->startEditing(); mText->textInput(" "); mText->stopEditing();
  489  			return;
  490  		}
  491  		else if (key == _("CLEAR"))
  492  		{
  493  			mOkCallback(""); 
  494  			delete this;
  495  			return;
  496  		}
  497  		else if (key == _("CANCEL"))
  498  		{
  499  			delete this;
  500  			return;
  501  		}
  502  
  503  		if (mAlt)
  504  		{
  505  			if (mShift && altedShiftedKey.empty())
  506  				return;
  507  			if (altedKey.empty())
  508  				return;
  509  		}
  510  
  511  		mText->startEditing();
  512  
  513  		const char* text;
  514  		if (mAlt && mShift)
  515  			text = altedShiftedKey.c_str();
  516  		else if (mAlt)
  517  			text = altedKey.c_str();
  518  		else if (mShift)
  519  			text = shiftedKey.c_str();
  520  		else
  521  			text = key.c_str();
  522  		mText->textInput(text);
  523  
  524  		mText->stopEditing();
  525  
  526  		if (Utils::String::isKorean(text) && mShift)
  527  			shiftKeys();
  528  	}, false);
  529  	
  530  	KeyboardButton kb(button, key, shiftedKey, altedKey, altedShiftedKey);
  531  	keyboardButtons.push_back(kb);
  532  	return button;
  533  }
```

## src/guis/GuiTextEditPopupKeyboard.h `:5-22` (an excerpt, upstream-carried, at the pin)

```text
    5  #include "components/ComponentGrid.h"
    6  #include "components/TextEditComponent.h"
    7  #include "components/TextComponent.h"
    8  #include <functional>
    9  
   10  class GuiTextEditPopupKeyboard : public GuiComponent
   11  {
   12  public:
   13  	GuiTextEditPopupKeyboard(Window* window, const std::string& title, const std::string& initValue,
   14  		const std::function<void(const std::string&)>& okCallback, bool multiLine, const std::string acceptBtnText = "OK");
   15  
   16  	bool input(InputConfig* config, Input input);
   17  	//void update(int deltatime) override;
   18  	void onSizeChanged();
   19  	std::vector<HelpPrompt> getHelpPrompts() override;
   20  
   21  private:
   22  	class KeyboardButton
```

## src/watchers/WatchersManager.cpp `:1-203` (an excerpt, upstream-carried, at the pin)

```text
    1  #include "WatchersManager.h"
    2  #include "Log.h"
    3  #include <chrono>
    4  
    5  std::mutex											WatchersManager::mNotificationLock;
    6  std::list<IWatcherNotify*>							WatchersManager::mNotification;
    7  std::mutex											WatchersManager::mWatchersLock;
    8  std::list<WatchersManager::WatcherInfo*>			WatchersManager::mWatchers;
    9  
   10  WatchersManager* WatchersManager::mInstance = nullptr;
   11  
   12  WatchersManager* WatchersManager::getInstance()
   13  {
   14  	if (mInstance == nullptr)
   15  		mInstance = new WatchersManager();
   16  
   17  	return mInstance;
   18  }
   19  
   20  void WatchersManager::stop()
   21  {
   22  	if (mInstance != nullptr)
   23  	{
   24  		delete mInstance;
   25  		mInstance = nullptr;
   26  	}
   27  }
   28  
   29  void WatchersManager::pause()
   30  {
   31  	if (mInstance == nullptr)
   32  		return;
   33  
   34  	{
   35  		std::unique_lock<std::mutex> lock(mInstance->mThreadLock);
   36  		mInstance->mPaused = true;
   37  	}
   38  
   39  	mInstance->mEvent.notify_all();
   40  }
   41  
   42  void WatchersManager::resume()
   43  {
   44  	if (mInstance == nullptr)
   45  		return;
   46  
   47  	{
   48  		std::unique_lock<std::mutex> lock(mInstance->mThreadLock);
   49  		mInstance->mPaused = false;
   50  	}
   51  
   52  	mInstance->mEvent.notify_all();
   53  }
   54  
   55  WatchersManager::WatchersManager()
   56  {
   57  	LOG(LogDebug) << "WatchersManager : Starting";
   58  
   59  	mRunning = true;
   60  	mPaused = false;
   61  	mThread = new std::thread(&WatchersManager::run, this);
   62  }
   63  
   64  void WatchersManager::RegisterComponent(IWatcher* instance)
   65  {
   66  	std::unique_lock<std::mutex> lock(mWatchersLock);
   67  
   68  	WatcherInfo* info = new WatcherInfo();
   69  	info->component = instance;
   70  	info->nextCheckTime =
   71  		std::chrono::steady_clock::now() + std::chrono::milliseconds(instance->initialUpdateTime());
   72  
   73  	mWatchers.push_back(info);
   74  }
   75  
   76  void WatchersManager::UnregisterComponent(IWatcher* instance)
   77  {
   78  	std::unique_lock<std::mutex> lock(mWatchersLock);
   79  
   80  	for (auto it = mWatchers.cbegin(); it != mWatchers.cend(); it++)
   81  	{
   82  		WatcherInfo* info = *it;
   83  		if (info->component == instance)
   84  		{
   85  			mWatchers.erase(it);
   86  			delete info;
   87  			return;
   88  		}
   89  	}
   90  }
   91  
   92  void WatchersManager::ResetComponent(IWatcher* instance)
   93  {
   94  	std::unique_lock<std::mutex> lock(mWatchersLock);
   95  
   96  	for (auto comp : mWatchers)
   97  	{
   98  		if (comp->component == instance)
   99  		{
  100  			comp->nextCheckTime = std::chrono::steady_clock::now();
  101  			return;
  102  		}
  103  	}
  104  }
  105  
  106  void WatchersManager::RegisterNotify(IWatcherNotify* instance)
  107  {
  108  	std::unique_lock<std::mutex> lock(mNotificationLock);
  109  	mNotification.push_back(instance);
  110  }
  111  
  112  void WatchersManager::UnregisterNotify(IWatcherNotify* instance)
  113  {
  114  	std::unique_lock<std::mutex> lock(mNotificationLock);
  115  
  116  	for (auto it = mNotification.cbegin(); it != mNotification.cend(); it++)
  117  	{
  118  		if ((*it) == instance)
  119  		{
  120  			mNotification.erase(it);
  121  			return;
  122  		}
  123  	}
  124  }
  125  
  126  void WatchersManager::NotifyComponentChanged(IWatcher* component)
  127  {
  128  	std::unique_lock<std::mutex> lock(mNotificationLock);
  129  
  130  	for (IWatcherNotify* n : mNotification)
  131  		n->OnWatcherChanged(component);
  132  }
  133  
  134  WatchersManager::~WatchersManager()
  135  {
  136  	if (mThread == nullptr)
  137  		return;
  138  
  139  	LOG(LogDebug) << "WatchersManager : Exit";
  140  
  141  	// Remove locks
  142  	{
  143  		std::unique_lock<std::mutex> lock(mWatchersLock);
  144  
  145  		for (auto comp : mWatchers)
  146  			delete comp;
  147  
  148  		mWatchers.clear();
  149  	}
  150  
  151  	mRunning = false;
  152  	mEvent.notify_all();
  153  
  154  	mThread->join();
  155  	delete mThread;
  156  	mThread = nullptr;
  157  }
  158  
  159  void WatchersManager::run()
  160  {
  161  	while (mRunning)
  162  	{
  163  		// ThreadLock
  164  		{
  165  			std::unique_lock<std::mutex> lock(mThreadLock);
  166  
  167  			if (mPaused)
  168  				mEvent.wait(lock, [this]() { return !mPaused || !mRunning; });
  169  			else
  170  				mEvent.wait_for(lock, std::chrono::seconds(1));
  171  
  172  			if (!mRunning)
  173  				return;
  174  
  175  			if (mPaused)
  176  				continue;
  177  		}
  178  
  179  		// Notification Lock
  180  		{
  181  			std::unique_lock<std::mutex> lock(mWatchersLock);
  182  
  183  			auto now = std::chrono::steady_clock::now();
  184  
  185  			for (auto item : mWatchers)
  186  			{
  187  				if (!mRunning)
  188  					return;
  189  
  190  				if (!item->component->enabled())
  191  					continue;
  192  
  193  				if (now < item->nextCheckTime)
  194  					continue;
  195  
  196  				if (item->component->check())
  197  					NotifyComponentChanged(item->component);
  198  
  199  				item->nextCheckTime = now + std::chrono::milliseconds(item->component->updateTime());
  200  			}
  201  		}
  202  	}
  203  }
```

## src/watchers/WatchersManager.h `:1-12` (an excerpt, upstream-carried, at the pin)

```text
    1  #pragma once
    2  
    3  #include <thread>
    4  #include <condition_variable>
    5  #include <mutex>
    6  #include <list>
    7  #include <chrono>
    8  
    9  class WatchersManager;
   10  
   11  class IWatcher
   12  {
```

## src/watchers/WatchersManager.h `:27-56` (an excerpt, upstream-carried, at the pin)

```text
   27  };
   28  
   29  class WatchersManager
   30  {
   31  public:
   32  	template <typename T>
   33  	static T* GetComponent()
   34  	{
   35  		std::unique_lock<std::mutex> lock(mWatchersLock);
   36  
   37  		for (auto cp : mWatchers)
   38  		{
   39  			T* sgview = dynamic_cast<T*>(cp->component);
   40  			if (sgview != nullptr)
   41  				return sgview;
   42  		}
   43  
   44  		return nullptr;
   45  	}
   46  
   47  	static void RegisterComponent(IWatcher* instance);
   48  	static void UnregisterComponent(IWatcher* instance);
   49  
   50  	static void RegisterNotify(IWatcherNotify* instance);
   51  	static void UnregisterNotify(IWatcherNotify* instance);
   52  
   53  	static void ResetComponent(IWatcher* instance);
   54  
   55  	static WatchersManager* getInstance();
   56  	static void             stop();
```

## src/watchers/WatchersManager.h `:69-92` (an excerpt, upstream-carried, at the pin)

```text
   69  		WatcherInfo() { component = nullptr; nextCheckTime = std::chrono::steady_clock::now(); }
   70  
   71  		IWatcher*	component;
   72  		std::chrono::steady_clock::time_point nextCheckTime;
   73  	};
   74  
   75  	void NotifyComponentChanged(IWatcher* component);
   76  
   77  	static std::mutex								mWatchersLock;
   78  	static std::list<WatcherInfo*>					mWatchers;
   79  
   80  	static std::mutex								mNotificationLock;
   81  	static std::list<IWatcherNotify*>				mNotification;
   82  
   83  	std::mutex										mThreadLock;
   84  	std::condition_variable							mEvent;
   85  	bool											mRunning;
   86  	bool											mPaused;
   87  	
   88  	std::thread*									mThread;
   89  
   90  	void run();	
   91  };
   92  
```

## The first reader's 02-forward-audit.md (whole)

# Forward audit — M6.P2 T35, EmulationStation's window, input and the rest of es-core (#682)

- **reviewed-at:** `b1f2908a55` (the distribution worktree at stage A); **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`, the 96 paths of `.qa-scratch/t35/paths.txt`, read by `git -C <W> show` and never from a working tree.
- **Stage B, composed by `tools/t35-02.py` from this template**: every generated section is the named script's output at the pin, and its last line is `generated, asserted: ...`. Each script was seen to exit 1 on three constructed drifts before it was trusted (§ The runs).
- Every proof carries a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`. Stage C (the host's cases and builds) and the guest window come after this composition, and their rows say `owed` until they run.

## Coverage

| Path | Lines | Read tier | Inventory tier | Fork stat (vs `bccd715707`) | What | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| `es-core/CMakeLists.txt` | 303 | fork-modified | fork-own | +7/-0 | the build lists | tree |
| `es-core/src/AsyncHandle.h` | 57 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/AudioManager.cpp` | 749 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/AudioManager.h` | 86 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/BindingManager.cpp` | 522 | upstream-carried | upstream-carried | -- | the theme bindings | tree |
| `es-core/src/BindingManager.h` | 118 | upstream-carried | upstream-carried | -- | the theme bindings | tree |
| `es-core/src/CECInput.cpp` | 376 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/CECInput.h` | 38 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/FavoriteMusicManager.cpp` | 127 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/FavoriteMusicManager.h` | 27 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/GuiComponent.cpp` | 1540 | upstream-carried | upstream-carried | -- | the component base | tree |
| `es-core/src/GuiComponent.h` | 298 | upstream-carried | upstream-carried | -- | the component base | tree |
| `es-core/src/GunManager.cpp` | 1057 | fork-modified | fork-own | +2/-0 | the light guns | tree |
| `es-core/src/GunManager.h` | 155 | upstream-carried | upstream-carried | -- | the light guns | tree |
| `es-core/src/HelpPrompt.h` | 27 | upstream-carried | upstream-carried | -- | the help prompts | tree |
| `es-core/src/HelpStyle.cpp` | 87 | upstream-carried | upstream-carried | -- | the help prompts | tree |
| `es-core/src/HelpStyle.h` | 31 | upstream-carried | upstream-carried | -- | the help prompts | tree |
| `es-core/src/ImageIO.cpp` | 394 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/ImageIO.h` | 54 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/InputConfig.cpp` | 446 | fork-modified | fork-own | +8/-1 | the input manager and its config | tree |
| `es-core/src/InputConfig.h` | 176 | upstream-carried | upstream-carried | -- | the input manager and its config | tree |
| `es-core/src/InputManager.cpp` | 1552 | fork-modified | fork-own | +5/-2 | the input manager and its config | tree |
| `es-core/src/InputManager.h` | 109 | upstream-carried | upstream-carried | -- | the input manager and its config | tree |
| `es-core/src/LocaleES.cpp` | 427 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/LocaleES.h` | 83 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/Log.cpp` | 322 | fork-modified | fork-own | +19/-40 | the log | tree |
| `es-core/src/Log.h` | 56 | upstream-carried | upstream-carried | -- | the log | tree |
| `es-core/src/LogPolicy.h` | 55 | fork-added | fork-own | +55/-0 | the log | tree |
| `es-core/src/MameNames.cpp` | 461 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/MameNames.h` | 62 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/MultiStateInput.cpp` | 53 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/MultiStateInput.h` | 19 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/Paths.cpp` | 363 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/Paths.h` | 112 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/PowerSaver.cpp` | 122 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/PowerSaver.h` | 84 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/Scripting.cpp` | 209 | fork-modified | fork-own | +3/-3 | the script runner | tree |
| `es-core/src/Scripting.h` | 13 | upstream-carried | upstream-carried | -- | the script runner | tree |
| `es-core/src/Sound.cpp` | 115 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/Sound.h` | 38 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/Splash.cpp` | 337 | upstream-carried | upstream-carried | -- | the splash | tree |
| `es-core/src/Splash.h` | 44 | fork-modified | fork-own | +4/-1 | the splash | tree |
| `es-core/src/TextToSpeech.cpp` | 284 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/TextToSpeech.h` | 64 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/ThemeData.cpp` | 2891 | upstream-carried | upstream-carried | -- | the theme parser | tree |
| `es-core/src/ThemeData.h` | 599 | upstream-carried | upstream-carried | -- | the theme parser | tree |
| `es-core/src/ThemeVariables.cpp` | 44 | upstream-carried | upstream-carried | -- | the theme parser | tree |
| `es-core/src/ThemeVariables.h` | 15 | upstream-carried | upstream-carried | -- | the theme parser | tree |
| `es-core/src/VolumeControl.cpp` | 668 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/VolumeControl.h` | 61 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/Window.cpp` | 1656 | fork-modified | fork-own | +49/-6 | the window and its surfaces | tree |
| `es-core/src/Window.h` | 197 | fork-modified | fork-own | +2/-0 | the window and its surfaces | tree |
| `es-core/src/anim/StoryboardAnimator.cpp` | 237 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/anim/StoryboardAnimator.h` | 192 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/anim/ThemeAnimation.h` | 146 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/anim/ThemeStoryboard.cpp` | 242 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/anim/ThemeStoryboard.h` | 28 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/animations/Animation.h` | 12 | upstream-carried | upstream-carried | -- | the animations | tree |
| `es-core/src/animations/AnimationController.cpp` | 38 | upstream-carried | upstream-carried | -- | the animations | tree |
| `es-core/src/animations/AnimationController.h` | 35 | upstream-carried | upstream-carried | -- | the animations | tree |
| `es-core/src/animations/LambdaAnimation.h` | 27 | upstream-carried | upstream-carried | -- | the animations | tree |
| `es-core/src/gettext.h` | 300 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/guis/GuiDetectDevice.cpp` | 149 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiDetectDevice.h` | 37 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiInfoPopup.cpp` | 115 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiInfoPopup.h` | 37 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiInputConfig.cpp` | 433 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiInputConfig.h` | 72 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiMsgBox.cpp` | 299 | fork-modified | fork-own | +78/-3 | the es-core dialogs | tree |
| `es-core/src/guis/GuiMsgBox.h` | 61 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiTextEditPopup.cpp` | 86 | fork-modified | fork-own | +1/-1 | the es-core dialogs | tree |
| `es-core/src/guis/GuiTextEditPopup.h` | 33 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiTextEditPopupKeyboard.cpp` | 533 | fork-modified | fork-own | +14/-14 | the es-core dialogs | tree |
| `es-core/src/guis/GuiTextEditPopupKeyboard.h` | 57 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/math/Misc.cpp` | 159 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Misc.h` | 40 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Transform4x4f.cpp` | 329 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Transform4x4f.h` | 53 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector2f.cpp` | 39 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector2f.h` | 73 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector2i.cpp` | 1 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector2i.h` | 61 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector3f.cpp` | 21 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector3f.h` | 104 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector4f.cpp` | 107 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector4f.h` | 101 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/playlists/AnimatedGifPlaylist.cpp` | 33 | upstream-carried | upstream-carried | -- | the playlists | tree |
| `es-core/src/playlists/AnimatedGifPlaylist.h` | 18 | upstream-carried | upstream-carried | -- | the playlists | tree |
| `es-core/src/playlists/M3uPlaylist.cpp` | 87 | upstream-carried | upstream-carried | -- | the playlists | tree |
| `es-core/src/playlists/M3uPlaylist.h` | 26 | upstream-carried | upstream-carried | -- | the playlists | tree |
| `es-core/src/watchers/BatteryLevelWatcher.cpp` | 9 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/BatteryLevelWatcher.h` | 21 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/NetworkStateWatcher.cpp` | 21 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/NetworkStateWatcher.h` | 25 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/WatchersManager.cpp` | 203 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/WatchersManager.h` | 92 | upstream-carried | upstream-carried | -- | the watchers | tree |

generated, asserted: 96 rows, 22575 lines (grep -c rule); read tiers fork-added 1 / fork-modified 12 / upstream-carried 83; inventory fork-own 13 / upstream-carried 83

## The leads

L-01 to L-29 are the brief's § 2 lead table. L-28 and L-29 are T34's PL-05 and PL-04, carried in version 2; § 6 still says *L-01 to L-27*, an erratum. 3.1 to 3.27 are the floor's cases. Each anchor line is checked for its text at the pin.

| Lead | Lines | Family | Owner | Disposition (stage B) | Proof | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| L-01 | `Window.cpp:339-340` against `:334-335`; `:1159-1160`; `:1164` | the queue | this lane (rule 6) | **confirmed at the tree:** the pop is from the back (upstream's, `back()`/`pop_back()` at the base `bccd715707`), **D-UI-093's decided row (`decision-register.md:404`) and the fork's comment at `c1c0d6ddc` both say *the order is the order things happened***, while its own `:1159-1160` says *a toast returned last shows first*: a defect against a decided row; a re-queued toast takes a fresh default duration (`:1164`). A contained fix (pop the front) for the pause | 3.14; G-02; G-03 `CANNOT` | tree |
| L-02 | `Window.cpp:188-207`, `:49-63`, `:1246-1248`; the raw holders in es-app | lifetimes | this lane (the teardown), T18/T20/T34 (the holders) | **confirmed:** `deinit` and `~Window` free no card or popup; the one free is `:1248`. T34's `s2-window.patch` (#1310) is the input: a `weak_ptr` return changes 10 es-app callers and 3 doubles -- **a collision for the pause** (§ 1 i), § The surfaces' last row | Q4; the pause | tree |
| L-03 | `Window.cpp:1262-1274` against `:1278`, `:1296` | lifetimes | this lane (rule 6) | **confirmed:** no lock in `unregisterPostedFunctions`; the two others take it. A contained fix (take the lock) for the pause | 3.17 (TSan) | tree |
| L-04 | `Window.cpp:1554-1637`; `:29` | lifetimes, structure | upstream ROCKNIX's (outside the lanes, D-UI-079) | **confirmed:** four detached workers capture `this` and post back; `:29` reaches into es-app. Recorded as upstream's, not changed; `Window.cpp:29`'s disposition is *recorded* | -- | tree |
| L-05 | `Window.cpp:262-281` | input | upstream's | **confirmed:** four Ctrl chords with the gate commented out on each line. Recorded (cost: a keyboard on a handheld; value: debugging) | -- | tree |
| L-06 | `InputManager.cpp:1225`, `:1232`; `FavoriteMusicManager.cpp:115` | input (writes) | this lane (rule 6) for `es_input.cfg`; the pause for the rest | **confirmed:** five writes, none atomic, `AtomicFile::` 0 (§ The input); the grep's seven include two read-mode `fopen`s. The `es_input.cfg` write through the fork's `AtomicFile` is a candidate for the pause (D-CLOUD-078's family) | § The input | tree |
| L-07 | `InputManager.cpp:893`, `:1187`, `:1225`, `:1250`; T36's cache | input (reads) | this lane (the read passes `false`), T36 (the cache) | **supported by the tree:** the cache stores misses (`FileSystemUtil.cpp:296`, `:323`, T36's) and `save_file` bypasses it; the hypothesis stands until 3.11 runs; G-01 reads the precondition | 3.11; G-01 | tree |
| L-08 | `InputManager.cpp:1242-1284` | scripts | upstream's; recorded | **confirmed:** synchronous on the interface thread, inside the rebuild's lock when reached from the hot-plug write (§ The locks) | 3.13; G-01's count | tree |
| L-09 | `InputManager.cpp:1101-1108`; `GuiInputConfig.cpp:73`, `:270-281`; `InputConfig.cpp:186-189` | input | T3 (which name the templates read) | **confirmed:** two names, `hotkey` and `hotkeyenable`; no verdict here | 3.12 | tree |
| L-10 | `InputManager.cpp:946`, `:960` | input | this lane (rule 6) | **confirmed:** both lines read `configNode` before `configNode = item` (`:947`, `:961`). A one-word fix (log `item`) for the pause | 3.10 | tree |
| L-11 | `WatchersManager.cpp:181-199` and the entry points | locks | this lane (#1283's es-core half) | **confirmed:** the list lock is held across every probe; five interface-thread entry points wait (§ The locks). The fix (snapshot, then probe unlocked, re-validating) for the pause | 3.1, 3.2, 3.3 | tree |
| L-12 | `GuiMsgBox.cpp:116-134`, `:246-264` | dialogs | upstream's; the callers pick their labels | **confirmed:** the third branch binds back to the last button; an unconfigured pad's any button fires it (`:257`). Read; G-04 and G-05 frame it | 3.18; G-04; G-05 | tree |
| L-13 | `GuiTextEditPopupKeyboard.cpp:14`, `:220` against `MenuComponent.cpp:14` (T34's) | dialogs | this lane (the define) | **confirmed:** one macro name, two values in two files. A rename for the pause (the keyboard's own name); the value is the keyboard's design | 3.19; G-06 | tree |
| L-14 | `GuiTextEditPopupKeyboard.cpp:392-397`, `:453-454`, `:491-496`; `GuiTextEditPopup.cpp:34` | dialogs | the pause (the lanes' fields: the cloud folder, the Wi-Fi key) | **confirmed:** `x` and CLEAR commit `""` and close with no question | G-06 | tree |
| L-15 | `GuiTextEditPopup.h:15-16`, `GuiTextEditPopupKeyboard.h:13-14` | dialogs | Backlog #1192 | **confirmed:** no masking parameter in either constructor. Deferred to #1192 | -- | tree |
| L-16 | `GuiMsgBox.cpp:44`, `:234`, `:240` | words | upstream's | **confirmed:** three `say(` calls (TTS compiled out on the image); recorded | 3.20 | tree |
| L-17 | `GuiInputConfig.cpp:134` | words | this lane (rule 6) | **confirmed:** the subtitle's number is the SDL instance id plus one | 3.21; G-08 | tree |
| L-18 | `Scripting.cpp:88-149`, `:169-178` | scripts | this lane (rule 6) with T2 (FD-9/FD-19) | **confirmed:** quoting only on a space, `"` stripped, `$`/backtick unquoted to `/bin/sh -c`; every file in a per-event folder runs (§ The scripts) | 3.4, 3.5, 3.6 | tree |
| L-19 | `Scripting.cpp:158-207`; `WatchersManager.cpp:29-53` | scripts | time to play | **confirmed:** three folder listings and three directory scans per event; priced on the guest (the retro's time-to-play) | the guest | tree |
| L-20 | `InputManager.cpp` `configureEmulators` (`:1474-1488`) | scripts | T2 (the launch path), T3 (the templates) | **contradicted at the pin for es-core:** the blob is `-pNindex <int> -pNguid <hex>`, no device name (`:1481-1482`); built unconditionally at `FileData.cpp:547` (T2's). The quoting half is where a name enters, not here | -- | tree |
| L-21 | `Window.cpp:743-745`, `:999-1003`; the eight `mHelp->` lines | help bar | read | **confirmed:** no Window bar under a second full-screen page; none of the eight calls `setOpacity`, so batocera's guard has no caller here | G-04 | tree |
| L-22 | `.claude/rules/es-native-ui.md:30` against `Window.cpp:1192` (the rule's line is checked by `t35-includes.py`) | record | the coordinator's sweep | **confirmed:** *top-right progress card* against a centred card; § The structure | -- | tree |
| L-23 | `ThemeData.cpp:745-856`, `:1094-1150` | structure | upstream's | **read:** the throw/warn asymmetry recorded; parse-only on the host | 3.26 | tree |
| L-24 | `InputManager.cpp:792-800` | input | this lane (rule 6) | **confirmed:** a `new SDL_Event` per F4 press, never freed (`SDL_PushEvent` copies). A one-line fix (a stack event) for the pause | -- | tree |
| L-25 | `guis/GuiTextEditPopupKeyboard.h` | record | § The merge debt | **confirmed:** byte-identical to `cada856d86`; a footnote | -- | tree |
| L-26 | `es-core/CMakeLists.txt` at T21's `3ae9610b0` | structure | the integration (§ 1 h) | **confirmed:** five added lines in four hunks; named in the hand-back | -- | tree |
| L-27 | `Window.cpp:777-779`, `:1091-1138`; T33's and T2's | lifetimes | this lane's half, T33's, T2's | **confirmed (the window's half):** the start from `render()` on idle time alone, with no way for a page to refuse; § The lifetimes' three halves | 3.27; G-09 | tree |
| L-28 | `Window.cpp:743-745`, `:1005-1078`; T34's chain | help bar | read; the pause with G-11 | **read:** the window's collection drops only a repeated icon (`:1023`) and merges the two dpad halves (`:1031-1041`); it adds nothing and drops no other prompt, so an empty bar comes from the prompts it was given -- the components or the image's composition. G-11 frames the page | 3.16; G-11 | tree |
| L-29 | `Window.cpp:1005-1078`; `ComponentList.cpp:568` (T34's) | help bar | read | **read:** a key `setHelpPrompts` does not know passes through untouched and sorts with index 0 (`:1062-1074`); it neither translates nor drops it -- whether its icon draws is `HelpComponent`'s (T34's) | 3.16 | tree |

**The floor's cases** (the seven candidates and 3.27 in bold; every case runs at stage C against the unfixed extract first; `proved: design` until it has):

| Case | Anchor | What it checks | Expected at the pin | When | proved: |
| --- | --- | --- | --- | --- | --- |
| **3.1** | `watchers/WatchersManager.cpp:196` | a probe that sleeps; `ResetComponent` from a second thread waits for it | FAIL at the pin expected (L-11) | stage C | design |
| 3.2 | `watchers/WatchersManager.cpp:86` | ASan: unregister during a running probe | FAIL expected (EP-13) | stage C | design |
| 3.3 | `watchers/WatchersManager.cpp:151` | TSan: `mRunning` written and read unsynchronised | a race report expected | stage C | design |
| **3.4** | `Scripting.cpp:109` | `a$(id)b.zip` unquoted, `a b.zip` quoted, `"` stripped | FAIL expected (L-18) | stage C | design |
| **3.5** | `Scripting.cpp:172` | a `notes.txt` in a per-event folder handed to the executor | FAIL expected (L-18) | stage C | design |
| 3.6 | `Scripting.cpp:202` | the single-script pass filters by extension | PASS expected (contract) | stage C | design |
| 3.7 | `InputConfig.cpp:188` | `mapInput` lower-cases; the XML round trip keeps every mapping | PASS expected (contract) | stage C | design |
| 3.8 | `InputConfig.cpp:353` | `buttonLabel` returns an unknown key unchanged | PASS expected (contract) | stage C | design |
| 3.9 | `InputConfig.cpp:347` | `AssignActionButtons` swaps once and is idempotent | PASS expected (contract) | stage C | design |
| **3.10** | `InputManager.cpp:960` | the two lines print empty attributes | FAIL expected (L-10) | stage C | design |
| **3.11** | `InputManager.cpp:893` | miss, `save_file`, `exists` again: false while the miss is cached | FAIL expected if the cache holds (L-07) | stage C | design |
| 3.12 | `InputManager.cpp:1107` | `select` copied to `hotkey` | PASS expected (documents the two names) | stage C | design |
| 3.13 | `InputManager.cpp:1262` | every `onfinish` command handed to the executor, synchronously | PASS expected (contract) | stage C | design |
| **3.14** | `Window.cpp:340` | queue [A, B] under a card: B then A; the re-queued duration | FAIL expected (L-01) | stage C | design |
| 3.15 | `Window.cpp:298` | the duration's three branches | PASS expected (contract) | stage C | design |
| 3.16 | `Window.cpp:1036` | the dedup, the merge, the sort | PASS expected (contract) | stage C | design |
| 3.17 | `Window.cpp:1267` | TSan: unregister against a post | a race report expected (L-03) | stage C | design |
| 3.18 | `guis/GuiMsgBox.cpp:125` | the three accelerator branches in the text | PASS expected (text) | stage C | design |
| **3.19** | `guis/GuiTextEditPopupKeyboard.cpp:220` | the macro defined in two files with two factors | FAIL expected (L-13) | stage C | design |
| 3.20 | `guis/GuiMsgBox.cpp:240` | three `say(` in the constructor | recorded (L-16) | stage C | design |
| 3.21 | `guis/GuiInputConfig.cpp:134` | `getDeviceId() + 1` is the argument | recorded (L-17) | stage C | design |
| 3.22 | `guis/GuiInfoPopup.cpp:98` | the fade's alpha curve and `mRunning` | PASS expected (contract) | stage C | design |
| 3.23 | `Log.cpp:60` | every batch reaches the file (#178) | PASS expected (the natural first binary) | stage C | design |
| 3.24 | `FavoriteMusicManager.cpp:115` | the rewrite is truncate-then-write | recorded (L-06) | stage C | design |
| 3.25 | `MameNames.cpp:6` | a malformed file: warned or thrown | recorded | stage C | design |
| 3.26 | `ThemeData.cpp:1094` | parse-only; the asymmetry recorded | no host case (L-23) | stage C | design |
| **3.27** | `Window.cpp:778` | T33's `pl25-screensaver.py`, unchanged | FAIL at the pin expected (#1305) | stage C | design |

generated, asserted: 29 leads (24 confirmed at the tree, 1 contradicted, the rest read or supported), 27 floor cases anchored

## The surfaces

| Site | Kind | Function | Container | Lock | What it does | Invariant | Proof or frame | proved: |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Window.h:123` | container | -- | the card vector | the lock below | raw pointers the window `new`s at `:1168` and frees at `:1248`; the caller keeps the same raw pointer | a card is owned by the window and freed only once `isRunning()` is false | Q4's lifetimes table; L-02 | tree |
| `Window.h:133` | container | -- | the posted functions | the lock below (not in `unregisterPostedFunctions`) | each a `std::function` and an owner token `void* container` (`:127-131`) | a post runs once, on the interface thread, at the next update | L-03 | tree |
| `Window.h:135` | container | -- | the toasts on screen | taken where they are removed under a card or a song; not in `update`/`render` | raw `GuiInfoPopup` pointers, top-centred, stacked | one floating surface at a time with the cards (D-UI-093) | G-02 | tree |
| `Window.h:154` | container | -- | the toast queue | the lock below | pairs of words and a duration in ms (`:153`) | nothing is dropped (D-UI-093's sentence) | 3.14 | tree |
| `Window.cpp:293` | lock | -- | the queue, the cards, the posts | -- | one file-static mutex | every enqueue and dequeue of the queue, the cards and the posts takes it, except `unregisterPostedFunctions` | Q3's locks table | tree |
| `Window.cpp:311` | enqueue | displayNotificationMessage | the toast queue | taken (`:313`) | `push_back` of the words with `notificationDuration(duration)` (`:298-309`: `<= 0` is the display-titles setting within 2..120 s, else 10 s) | kept: any thread may call it | 3.15 | tree |
| `Window.cpp:324` | dequeue | processNotificationMessages (update `:466`) | the queue -> the popups | taken (`:326`) | returns while any card is up (`:336-337`); takes the **back** of the queue (`:339-340`), builds a `GuiInfoPopup`, lays out | one surface at a time: kept; *the order is the order things happened* (`:334-335`): **not kept** -- the newest first (L-01) | 3.14; G-02 (the toast after the card); G-03 `CANNOT` | tree |
| `Window.cpp:353` | free | stopNotificationPopups | the popups | the caller's (`:1165` holds it) | deletes every popup and clears the vector | kept: called with the lock from the card's creation | -- | tree |
| `Window.cpp:365` | free | updateNotificationPopups (update `:557`) | the popups | not taken | updates each popup, deletes one whose fade has ended (`:373-379`), lays out | kept while every card is created on the interface thread (each caller at the pin does; a read, Q4) | Q4's caller read | tree |
| `Window.cpp:396` | layout | layoutNotificationPopups | the popups | the caller's | stacks from 0.02 H with a 0.02 H gap, a fading popup sliding up by its eased height | kept | G-02 | tree |
| `Window.cpp:418` | free + enqueue | processSongTitleNotifications (update `:465`) | the popups, the queue | taken (`:427`), released before the enqueue (`:441`) | removes an on-screen song toast, then queues the new title through `displayNotificationMessage` (`:442`) | kept: a song toast queues like any other | -- | tree |
| `Window.cpp:782` | draw | render | the popups, the cards | the cards' pass takes it (`:1179`); the popups' loop does not | popups then cards, both only while no screensaver draws (`:782-788`) | kept: the screensaver hides both | G-09 | tree |
| `Window.cpp:1146` | read | hasAsyncNotifications | the card vector | taken (`:1148`) | true while any card is queued, lingering or fading (`.h:100-101`) | kept | -- | tree |
| `Window.cpp:1152` | enqueue | createAsyncNotificationComponent | the cards; the queue | taken (`:1154`) | a toast on screen goes back on the queue with `notificationDuration(-1)` (`:1164`) -- **a fresh default duration, not its remainder** -- and the popups stop (`:1165`); the card is `new`ed and its raw pointer returned (`:1168-1174`) | one surface at a time: kept; the toast's words: kept whole | 3.14's second half; G-02 | tree |
| `Window.cpp:1177` | layout + draw | renderAsyncNotifications | the cards | taken for the whole pass (`:1179`) | each card centred, `posX = W*0.5 - w*0.5` (`:1192`), from 0.02 H (`:1183`), stacked by height + 0.01 W (`:1194`, `:1231`); fades in place (`:1217-1221`), slides up under a clip when closing (`:1203-1215`) | the position re-applied every frame agrees with the component's own (next row) | G-02's two edges | tree |
| `components/AsyncNotificationComponent.cpp:112` (T34's) | position (T34's) | AsyncNotificationComponent ctor | the card | -- | the card's own position before its first render, centred at 0.02 H (`:112-113`); its width `max(text, 0.9 W)` (`:62-64`); the comment `:110-111` asks the two to agree | kept at the pin: `:1192` and `:112` compute the same x | G-02 measures the edges at 640 | tree |
| `Window.cpp:1236` | free | updateAsyncNotifications (update `:556`) | the card vector | taken (`:1238`) | **the one place a card is freed** (`:1246-1248`), once `isRunning()` is false | kept while the caller stops using its raw pointer before the card ends; `deinit` (`:188-207`) and `~Window` (`:49-63`) never free a card, a popup or the queue (L-02) | Q4 | tree |
| `Window.cpp:1262` | free | unregisterPostedFunctions | the posted functions | **not taken** | erases the owner's posts while iterating `mFunctions` (`:1267-1273`) | **not kept**: `postToUiThread` (`:1278`) and `processPostedFunctions` (`:1296`) take the lock (L-03) | 3.17 (TSan) | tree |
| `Window.cpp:1276` | enqueue | postToUiThread | the posted functions | taken (`:1278`) | appends the function and its owner token, and wakes a sleeping window (`:1284-1289`) | kept; it promises nothing to a poster that dies before the drain (L-03, T34 L-12) | Q4 | tree |
| `Window.cpp:1292` | dequeue | processPostedFunctions (update `:464`) | the posted functions | taken to copy and clear (`:1296-1303`), released to run | runs each copied function under `TRYCATCH` (`:1305-1306`) | kept: a post may post again without a deadlock | -- | tree |
| T34's `stage-e/s2-window.patch` (#1310) | held patch | createAsyncNotificationComponent, updateAsyncNotifications | the card vector | taken, as now | the window owns each card through a `shared_ptr` whose deleter frees it on the interface thread; the caller gets a `weak_ptr`; a stopped card is retired until the window holds the last reference | would make the card's free safe against a holder's late use (L-02's half); **changes `createAsyncNotificationComponent`'s return type**, so the 10 callers in es-app (`ContentInstaller.cpp:60`, `ProxyCards.cpp:215`, `:257`, `:514`, `ThreadedBluetooth.cpp:15`, `:72`, `ThreadedCloudSync.cpp:46`, `ThreadedHasher.cpp:126`, `guis/GuiMenu.cpp:11717`, `guis/GuiUpdate.cpp:162`: five lanes) and the three doubles (`tests/app-unit/fakes/Window.h:11`, `ProxyCardsTests.cpp:154`, `tests/hasher-offline-index.py:65`) change with it | proposed for the pause: adopted into a stage-E stream only with its callers' half named for their owners, else a collision named (§ 1 i) | design |
| T34's `stage-e/s3-msgbox.patch` (S3, 06:12; Q6) | held patch | `GuiMsgBox` constructor | -- (the dialog's height) | -- | removes `GuiMsgBox`'s #48 workaround -- the height measured again at the drawn width (`guis/GuiMsgBox.cpp:167-202` at the pin) -- because T34's `TextComponent` fix (#1315, D-UI-130) measures at the width it draws at; proven by T34 on a scratch copy of the pin's file, not applied | **ordered after #1315**: applied without T34's `TextComponent` change it returns #48 (the OK button over the message on a small panel); it touches one of the 96 and depends on a file of T34's 80, so it lands with T34's fix or after it, at the integration | a collision named for the pause (§ 1 i's family): not adopted by this lane; G-04 and G-11 frame the pin's dialog either way | design |

generated, asserted: 22 rows: 5 containers and the lock, 15 sites (one of them T34's component's, outside the 96), and T34's two held patches

**The queue's order (`:339-340`).** The queue drains **newest first**. The pop is upstream's: the base `bccd715707` pops from the back at its `:322-323`. **D-UI-093's decided row says it plainly** (`decision-register.md:404`: *Nothing is dropped; the order is the order things happened.*), as does the fork's comment (`c1c0d6ddc`, `:334-335`). The fork's own re-queue comment (`:1159-1160`) relies on the opposite. **Disposition: a defect against a decided row, contained in `processNotificationMessages`**, the order cited and not re-argued (`decision-register.md` § Read it when), proposed for the pause as a rule-6 fix (pop the front, and reverse the re-queue loop so a returned toast keeps its place). 3.14's FAIL line at stage C is the evidence. G-03 is `CANNOT`.

**The re-queued toast's duration (`:1164`).** A toast taken off the screen by a new card comes back with `notificationDuration(-1)`, a fresh default, not its remainder. **Disposition: by design, recorded.** A toast half-read and then re-shown whole costs the player seconds and loses no words. The pause may rule otherwise (a register row, brief § 9).

**F-ES-24** (the 2026-09-25 audit `02:199`, Low, never dispositioned): every toast waits while *any* card is up (`:336-337`), including the hasher's minutes-long upstream card that D-UI-079 keeps as upstream has it. **Disposition: stands as recorded, with a bound proposed for the pause.** It is the one surface D-UI-093 and D-UI-078 together did not decide, so it is put to the coordinator as brief § 9's first register row, not decided here.

**Item 13, the card's position:** `:1183` (0.02 H from the top) and `:1192` (centred) are re-applied every frame. They agree with the component's own first position (`AsyncNotificationComponent.cpp:112-113`, T34's) and its width `max(text, 0.9 W)` (`:62-64`). G-02 measures the edges at 640 (x 32 and x 608).

## The input

**The write sites** (the writes grep's 9 hits less the two CMake registrations `:122`, `:257`; `AtomicFile::` 0):

| Site | Kind | File | Mechanism | Atomic | A cut file reads as | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| `InputManager.cpp:1225` | write | `es_input.cfg` (`getConfigPath()`) | pugixml `save_file`: the path opened for writing and the document written in place | no | `load_file` fails: at load `tryLoadInputConfig` logs `Error parsing input config` and returns false (`:899-903`), the pad reads as unconfigured; at the next write the merge is skipped (`:1191-1193`) and the file is rewritten with that one device | tree |
| `InputManager.cpp:1232` | write | `es_last_input.cfg` (`getTemporaryConfigPath()`, `:1291-1293`) | pugixml `save_file`, in place; the last device alone, *so that people can easily share their config* (`:1227`) | no | nothing in es-core or es-app reads it back (the two lines that name it are `:1231`, `:1293`); a cut file is a cut share | tree |
| `FavoriteMusicManager.cpp:71` | write | the favourites file (`getFavoriteMusicFilePath()`) | `std::ofstream`, `std::ios::app`: one `path;name` line appended | no (an append) | a cut last line: `readAllLines` (`:34`, `:89`) returns it as one more line that matches no song | tree |
| `FavoriteMusicManager.cpp:115` | write | the favourites file | `std::ofstream`, `std::ios::trunc` then the remaining lines (`:121-123`); the last removal deletes the file instead (`:104-106`) | no | the file emptied or cut at a line: favourites lost from that line on, with no error | tree |
| `Log.cpp:179` | write | the log (`es_log.txt`) | the member, opened `std::ios::out \| std::ios::trunc` at `:46`; the worker flushes per batch (`:98`, `:147`) | no (a log, rewritten each start) | a shorter log; nothing reads it back (#178's proof is the batch reaching the file) | tree |
| `AudioManager.cpp:539` | read | a song file | `fopen(..., "r")`: **a read**, counted by the grep's `fopen\(` alternation | -- | -- | tree |
| `AudioManager.cpp:610` | read | a song file (its ID3 tag) | `fopen(..., "r")`: **a read**, as above | -- | -- | tree |

**Every `exists(` of an input file** (none passes `false`; the § 5 reads run: 41 `FileSystem::exists(` lines, 0 uncached):

| Site | File checked | Writer | Cache | proved: |
| --- | --- | --- | --- | --- |
| `InputManager.cpp:420` | the SDL mapping files (`gamecontrollerdb.txt`, shipped and user) | none in ES | **WIN32 only**: the block `:404-483` is `#if WIN32`; it never runs on the device | tree; 3.11 at stage C |
| `InputManager.cpp:893` | `es_input.cfg` (`tryLoadInputConfig`) | `:1225` | cached; a miss is remembered, and `loadInputConfig` after a write (`:1239`) reads it | tree; 3.11 at stage C |
| `InputManager.cpp:1187` | `es_input.cfg` (`writeDeviceConfig`'s merge) | `:1225` | cached; a remembered miss skips the merge and the save keeps only this device (L-07) | tree; 3.11 at stage C |
| `InputManager.cpp:1250` | `es_input.cfg` (`doOnFinish`) | `:1225` | cached; a remembered miss skips the `onfinish` commands written a line earlier | tree; 3.11 at stage C |
| `guis/GuiDetectDevice.cpp:127` | `es_input.cfg` (the detect page's first-run skip) | `InputManager.cpp:1225` | cached | tree; 3.11 at stage C |

**3.11, the cache's answer, read:** `exists(p)` with the cache on (`Settings.cpp:155`, T36's) asks the cache first (`FileSystemUtil.cpp:1127-1131`) and on a miss stores what `stat64` found, **absence included** (`:296`, `:306`, `:323`); `pugi::xml_document::save_file` writes through `fopen`, never through `Utils::FileSystem`, so nothing clears the entry. On a device whose `es_input.cfg` was absent at the first check, every later `exists(` of it in the session reads false until a cache reset. The unit case 3.11 proves the sequence at stage C; G-01 reads whether the user file exists before any configuration on the image (L-07's precondition). For T36's `FileSystemUtil`: the cache remembers misses; a writer outside `Utils::FileSystem` is invisible to it.

**The two hotkey names:** the SDL-mapping fallback copies `select` to **`hotkey`** (`InputManager.cpp:1105-1107`); the configuration page maps **`HotKeyEnable`** (`GuiInputConfig.cpp:73`, `:273`, `:279`), stored as `hotkeyenable` (`InputConfig.cpp:188`). Which one the launch scripts read is T3's templates; the two names are a fact of these lines (L-09, 3.12). `proved: tree`.

**`doOnFinish`'s `<command>`** (`:1242-1284`): every `<inputAction type="onfinish">` `<command>` text runs through `ProcessStartInfo(tocall).run()` at `:1272`, **synchronously, on the interface thread**, from `writeDeviceConfig` (`:1238`); a non-zero exit is a `LogWarning` (`:1277`). The shipped `es_input.cfg`'s `inputAction` count is G-01's line (owed). `proved: tree`.

**The hot-plug rebuild's cost:** a pad added (`:813`) or removed (`:864`) rebuilds every joystick on the interface thread (`:852`, `:875`): the joystick subsystem quit and re-initialised (`:376-382`, `:402`), every device reopened (`:517-`), each configuration re-read from `es_input.cfg` (`loadInputConfig`, `:583`), and an SDL-mapped device written back (`:605`, the hot-plug write); the mapping-file pass and the 500 ms settle poll are WIN32-only (`:404-483`). One file parse per pad per event; G-10 is `CANNOT` (no pad on the guest). `proved: tree`.

**The controllers blob, for T3's half:** `configureEmulators` (`:1474-1488`) writes `-pNindex <int> -pNguid <hex>` per seat and **no device name**; the GUID string is SDL's hex. The quoting T2 FD-6/FD-7 describe is where a name enters, not here; the blob is built on every launch (`FileData.cpp:547`, T2's) whether `includeControllers` is set or not (L-20). `proved: tree`.

generated, asserted: 7 write-site rows (5 writes, 2 reads the grep counts), 5 exists rows; the writes grep 9 hits

## The locks

**The grep:** `git grep -n -E 'std::(recursive_|shared_|timed_)?mutex|lock_guard|unique_lock|scoped_lock|shared_lock|\.lock\(\)|\.unlock\(\)|condition_variable'` over the 96 at the pin.

| Site | Kind | Lock | Function | proved: |
| --- | --- | --- | --- | --- |
| `InputManager.cpp:52` | declaration | mJoysticksLock | -- | tree |
| `InputManager.cpp:200` | acquire (RAII) | mJoysticksLock | InputManager::getNumJoysticks | tree |
| `InputManager.cpp:227` | acquire (manual) | mJoysticksLock | InputManager::clearJoysticks | tree |
| `InputManager.cpp:242` | release (manual) | mJoysticksLock | InputManager::clearJoysticks | tree |
| `InputManager.cpp:485` | acquire (manual) | mJoysticksLock | InputManager::rebuildAllJoysticks | tree |
| `InputManager.cpp:623` | release (manual) | mJoysticksLock | InputManager::rebuildAllJoysticks | tree |
| `InputManager.cpp:1343` | acquire (RAII) | mJoysticksLock | InputManager::computePlayersConfigs | tree |
| `InputManager.cpp:1494` | acquire (manual) | mJoysticksLock | InputManager::updateBatteryLevel | tree |
| `InputManager.cpp:1520` | release (manual) | mJoysticksLock | InputManager::updateBatteryLevel | tree |
| `Log.cpp:18` | include | -- | -- | tree |
| `Log.cpp:70` | acquire (RAII) | mMutex | AsyncLogger::close | tree |
| `Log.cpp:104` | acquire (RAII) | mMutex | AsyncLogger::enqueue | tree |
| `Log.cpp:122` | acquire (RAII) | mMutex | AsyncLogger::workerLoop | tree |
| `Log.cpp:187` | declaration | mMutex | -- | tree |
| `Log.cpp:188` | declaration | mMutex | -- | tree |
| `Scripting.cpp:20` | declaration | mScriptQueueLock | -- | tree |
| `Scripting.cpp:21` | declaration | mScriptQueueLock | -- | tree |
| `Scripting.cpp:29` | acquire (RAII) | mScriptQueueLock | executeCommandsThread | tree |
| `Scripting.cpp:40` | release (manual) | mScriptQueueLock | executeCommandsThread | tree |
| `Scripting.cpp:60` | acquire (RAII) | mScriptQueueLock | pushCommand | tree |
| `Scripting.cpp:78` | acquire (RAII) | mScriptQueueLock | exitScriptingEngine | tree |
| `TextToSpeech.cpp:27` | acquire (RAII) | mMutex | TextToSpeech::SpeakThread | tree |
| `TextToSpeech.cpp:41` | release (manual) | mMutex | TextToSpeech::SpeakThread | tree |
| `TextToSpeech.cpp:76` | `weak_ptr::lock`, not a mutex | -- | TextToSpeech::getInstance | tree |
| `TextToSpeech.cpp:256` | acquire (RAII) | mMutex | TextToSpeech::say | tree |
| `TextToSpeech.h:12` | include | -- | -- | tree |
| `TextToSpeech.h:48` | declaration | mMutex | -- | tree |
| `TextToSpeech.h:49` | declaration | mMutex | -- | tree |
| `ThemeData.cpp:716` | acquire (RAII) | _lock | ThemeFileCache::getXmlDocument | tree |
| `ThemeData.cpp:737` | acquire (RAII) | _lock | ThemeFileCache::clear | tree |
| `ThemeData.h:594` | declaration | _lock | -- | tree |
| `VolumeControl.cpp:13` | include | -- | -- | tree |
| `VolumeControl.cpp:199` | acquire (RAII) | mLock | PulseAudioControl::WaitEvent | tree |
| `VolumeControl.cpp:205` | declaration | mLock | -- | tree |
| `VolumeControl.cpp:206` | declaration | mLock | -- | tree |
| `VolumeControl.cpp:254` | `weak_ptr::lock`, not a mutex | -- | VolumeControl::getInstance | tree |
| `Window.cpp:293` | declaration | mNotificationMessagesLock | -- | tree |
| `Window.cpp:313` | acquire (RAII) | mNotificationMessagesLock | Window::displayNotificationMessage | tree |
| `Window.cpp:326` | acquire (RAII) | mNotificationMessagesLock | Window::processNotificationMessages | tree |
| `Window.cpp:427` | acquire (RAII) | mNotificationMessagesLock | Window::processSongTitleNotifications | tree |
| `Window.cpp:441` | release (manual) | mNotificationMessagesLock | Window::processSongTitleNotifications | tree |
| `Window.cpp:1148` | acquire (RAII) | mNotificationMessagesLock | Window::hasAsyncNotifications | tree |
| `Window.cpp:1154` | acquire (RAII) | mNotificationMessagesLock | Window::createAsyncNotificationComponent | tree |
| `Window.cpp:1179` | acquire (RAII) | mNotificationMessagesLock | Window::renderAsyncNotifications | tree |
| `Window.cpp:1238` | acquire (RAII) | mNotificationMessagesLock | Window::updateAsyncNotifications | tree |
| `Window.cpp:1278` | acquire (RAII) | mNotificationMessagesLock | Window::postToUiThread | tree |
| `Window.cpp:1296` | acquire (manual) | mNotificationMessagesLock | Window::processPostedFunctions | tree |
| `Window.cpp:1303` | release (manual) | mNotificationMessagesLock | Window::processPostedFunctions | tree |
| `watchers/WatchersManager.cpp:5` | declaration | mNotificationLock | -- | tree |
| `watchers/WatchersManager.cpp:7` | declaration | mWatchersLock | -- | tree |
| `watchers/WatchersManager.cpp:35` | acquire (RAII) | mThreadLock | WatchersManager::pause | tree |
| `watchers/WatchersManager.cpp:48` | acquire (RAII) | mThreadLock | WatchersManager::resume | tree |
| `watchers/WatchersManager.cpp:66` | acquire (RAII) | mWatchersLock | WatchersManager::RegisterComponent | tree |
| `watchers/WatchersManager.cpp:78` | acquire (RAII) | mWatchersLock | WatchersManager::UnregisterComponent | tree |
| `watchers/WatchersManager.cpp:94` | acquire (RAII) | mWatchersLock | WatchersManager::ResetComponent | tree |
| `watchers/WatchersManager.cpp:108` | acquire (RAII) | mNotificationLock | WatchersManager::RegisterNotify | tree |
| `watchers/WatchersManager.cpp:114` | acquire (RAII) | mNotificationLock | WatchersManager::UnregisterNotify | tree |
| `watchers/WatchersManager.cpp:128` | acquire (RAII) | mNotificationLock | WatchersManager::NotifyComponentChanged | tree |
| `watchers/WatchersManager.cpp:143` | acquire (RAII) | mWatchersLock | WatchersManager::~WatchersManager | tree |
| `watchers/WatchersManager.cpp:165` | acquire (RAII) | mThreadLock | WatchersManager::run | tree |
| `watchers/WatchersManager.cpp:181` | acquire (RAII) | mWatchersLock | WatchersManager::run | tree |
| `watchers/WatchersManager.h:4` | include | -- | -- | tree |
| `watchers/WatchersManager.h:35` | acquire (RAII) | mWatchersLock | WatchersManager::GetComponent | tree |
| `watchers/WatchersManager.h:77` | declaration | mWatchersLock | -- | tree |
| `watchers/WatchersManager.h:80` | declaration | mNotificationLock | -- | tree |
| `watchers/WatchersManager.h:83` | declaration | mThreadLock | -- | tree |
| `watchers/WatchersManager.h:84` | declaration | mThreadLock | -- | tree |

**Each lock, its acquisition sites, its order, and who waits:**

| Lock | Guards | Acquired at | Order and what it is held across | Who blocks on it |
| --- | --- | --- | --- | --- |
| `mNotificationMessagesLock` (`Window.cpp:293`) | toasts, cards, posts | `:313`, `:326`, `:427`, `:1148`, `:1154`, `:1179`, `:1238`, `:1278`, `:1296` | none nested; the cards' render pass holds it for the whole pass (`:1179`); `unregisterPostedFunctions` (`:1262-1274`) walks `mFunctions` **without it** (L-03) | a worker's `displayNotificationMessage` or `postToUiThread` waits out one render pass (bounded); the interface thread never waits on a worker here |
| `mJoysticksLock` (`InputManager.cpp:52`) | joysticks, input configs | `:200`, `:227`, `:485`, `:1343`, `:1494` | three manual lock/unlock pairs (`:227-242`, `:485-623`, `:1494-1520`) with no `return` between them (read), and no RAII; the rebuild's pair spans `writeDeviceConfig` (`:605`), which fires two events (`:1234-1235`) and runs `doOnFinish`'s commands **synchronously** (`:1272`) with the lock held | interface thread only: SDL events, the launch path's `computePlayersConfigs` (`:1343`), and `updateBatteryLevel` posted from `NetworkThread.cpp:206`; no second thread takes it |
| `mWatchersLock` (`WatchersManager.cpp:7`) | the watcher list | `:66`, `:78`, `:94`, `:143`, `:181`, `.h:35` | **held across every `check()`** (`:181`, `:196`) and then `mNotificationLock` inside it (`:197` -> `:128`): order **mWatchersLock -> mNotificationLock**, and the observers' `OnWatcherChanged` runs on the watcher thread under both | **`RegisterComponent` `:66`, `UnregisterComponent` `:78`, `ResetComponent` `:94`, `GetComponent` `.h:35` and the destructor `:143` wait for a running probe** (L-11, #1283's es-core half; 3.1 at stage C) |
| `mNotificationLock` (`WatchersManager.cpp:5`) | observers | `:108`, `:114`, `:128` | inner to `mWatchersLock` when taken from `run()` | `UnregisterNotify` `:114` waits for a callback in flight |
| `mThreadLock` (`WatchersManager.h:83`) | pause and wake | `:35`, `:48`, `:165` | its own scope before `mWatchersLock` in `run()` (`:164-171`), never nested with it; `mRunning` and `mPaused` are plain `bool`s read outside it (`:161`, `:187`; 3.3) | `pause` `:35` and `resume` `:48` take it briefly |
| `mMutex` (`Log.cpp:187`) | the log buffer | `:70`, `:104`, `:122` | none nested | any thread's `LOG(...)` takes it briefly to enqueue |
| `mScriptQueueLock` (`Scripting.cpp:20`) | script queue | `:29`, `:60`, `:78` | WIN32 only | -- |
| `mMutex` (`TextToSpeech.h:48`) | speech queue | `:27`, `:256` | the speak thread is WIN32 only; TTS is compiled out on the image (§ 5) | -- |
| `_lock` (`ThemeData.h:594`) | theme file cache | `:716`, `:737` | held across `load_file` of a theme file (`ThemeData.cpp:716-723`) | a theme load |
| `mLock` (`VolumeControl.cpp:205`) | PulseAudio wait | `:199` | `_ENABLE_PULSE_` only (the pulse branch, not parsed on the host) | -- |

**The threads' start and stop against `main.cpp`'s order** (es-app's, read at the pin):

| Thread | Started | Stopped | proved: |
| --- | --- | --- | --- |
| the logger's worker | `Log.cpp:60`, from `Log::init` (`main.cpp:788`) | `AsyncLogger::close` joins (`:76-77`) from `onExit` (`main.cpp:353`, registered `:793`) -- after `window.deinit()` (`:1358`) | tree |
| the watcher thread | `WatchersManager.cpp:61`, on the first `getInstance()` (`:15`) | `WatchersManager::stop()` at `main.cpp:1330` joins (`:154`) -- **before** `window.deinit()`; the join waits for a probe in flight and the 1 s `wait_for` (`:170`) | tree |
| the PulseAudio loop | `VolumeControl.cpp:32` (`_ENABLE_PULSE_`) | `exit()` joins (`:68-73`) from `~PulseAudioControl` | tree (branch not parsed) |
| the speak thread | `TextToSpeech.cpp:92` (**WIN32**) | `:128` | tree |
| the script queue | `Scripting.cpp:68` (**WIN32**, `new std::thread`, not a detach) | `exitScriptingEngine` (`main.cpp:1347`) | tree |
| four storage workers | `Window.cpp:1554`, `:1572`, `:1608`, `:1634` (`processStorageRequest`) | **detached** (`:1563`, `:1575`, `:1619`, `:1637`); each captures `this` and posts back (L-04); nothing joins them | tree |
| `NetworkThread` (es-app's) | `main.cpp:898` | not deleted at exit; named for its owner, outside the 96 | tree |

generated, asserted: 67 lock lines in 11 files (4 includes, 2 `weak_ptr::lock`), 10 locks summarised, 7 threads

## The lifetimes

**Every thread line** (the § 5 threads run's grep, recomputed):

| Site | What | Who joins it | What it touches on the interface thread | proved: |
| --- | --- | --- | --- | --- |
| `Log.cpp:60` | start: the logger's worker | `AsyncLogger::close` joins (`:76-77`), from `onExit` at exit | nothing; it writes the file | tree |
| `Log.cpp:180` | the member `std::thread mThread` | as above | -- | tree |
| `Scripting.cpp:18` | the member `std::thread* mScriptQueueThread` (**WIN32**) | `exitScriptingEngine` | -- | tree |
| `Scripting.cpp:68` | start: `new std::thread(&executeCommandsThread)` (**WIN32**; not a detach) | `exitScriptingEngine` (`:75-81`) | nothing | tree |
| `TextToSpeech.cpp:92` | start: the speak thread (**WIN32**) | `~TextToSpeech` (`:128`) | nothing | tree |
| `TextToSpeech.h:47` | the member `std::thread* mSpeakThread` | as above | -- | tree |
| `VolumeControl.cpp:32` | start: `PulseAudioControl::run` (`_ENABLE_PULSE_`) | `exit()` (`:68-73`) | nothing; the volume is read under `mLock` | tree |
| `VolumeControl.cpp:203` | the member `std::thread* mThread` | as above | -- | tree |
| `Window.cpp:1554` | start: a storage worker for `mergeDrive` in `processStorageRequest`, capturing `this` | **nobody: detached** | posts back to the window (`postToUiThread`) and, on failure, pushes a `GuiMsgBox` | tree |
| `Window.cpp:1563` | the detach | -- | -- | tree |
| `Window.cpp:1572` | start: a storage worker for `ignoreDevicePermanently` in `processStorageRequest`, capturing `this` | **nobody: detached** | posts back to the window (`postToUiThread`) and, on failure, pushes a `GuiMsgBox` | tree |
| `Window.cpp:1575` | the detach | -- | -- | tree |
| `Window.cpp:1608` | start: a storage worker for `prepareDrive` (format) in `processStorageRequest`, capturing `this` | **nobody: detached** | posts back to the window (`postToUiThread`) and, on failure, pushes a `GuiMsgBox` | tree |
| `Window.cpp:1619` | the detach | -- | -- | tree |
| `Window.cpp:1634` | start: a storage worker for `ignoreDevicePermanently` in `processStorageRequest`, capturing `this` | **nobody: detached** | posts back to the window (`postToUiThread`) and, on failure, pushes a `GuiMsgBox` | tree |
| `Window.cpp:1637` | the detach | -- | -- | tree |
| `watchers/WatchersManager.cpp:61` | start: the watcher thread | `~WatchersManager` joins (`:154`) from `stop()` (`main.cpp:1330`) | **the observers' `OnWatcherChanged` runs on this thread** under two locks (`:197` -> `:128-131`) | tree |
| `watchers/WatchersManager.h:88` | the member `std::thread* mThread` | as above | -- | tree |

**Every `delete this`** (all in the six dialogs, all on the interface thread; none touches a member after the delete):

| Site | What reaches it, and what follows | What the delete does to the window | proved: |
| --- | --- | --- | --- |
| `guis/GuiDetectDevice.cpp:99` | `input`: back cancels; `return true` follows | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiDetectDevice.cpp:132` | `update`: the first-run skip after `mDoneCallback()`; the function ends (`:133-149`) and `Window::update` touches nothing after the call (`Window.cpp:542-543`) | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiDetectDevice.cpp:145` | `update`: the hold done, `GuiInputConfig` pushed first; the function ends | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiInputConfig.cpp:262` | `okFunction` (`:258-263`): after `writeDeviceConfig` (`:259`) and `okCallback()`; reached from the OK button and from the hotkey dialog's two buttons through `GuiMsgBox::deleteMeAndCall` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiInputConfig.cpp:288` | the CANCEL button's own closure: the button is destroyed while its `std::function` runs; nothing follows | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiMsgBox.cpp:289` | `deleteMeAndCall`: the callback copied first (`:288`), then called after the delete (`:291-292`) -- the safe shape | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopup.cpp:33` | the accept button's closure: `okCallback(value)` then the delete; nothing follows | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopup.cpp:34` | the CLEAR button's closure: `okCallback("")` then the delete, **no question asked** (L-14) | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopup.cpp:35` | the CANCEL button's closure | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopup.cpp:74` | `input`: back; `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:346` | `input`: START submits after `mOkCallback(value)`; `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:352` | `input`: ESC on the keyboard device; `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:359` | `input`: back; `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:395` | `input`: **`x` commits `""`** (`:392-397`, L-14); `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:477` | `pressedKey`: OK after `mOkCallback(value)`; `return` follows | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:494` | `pressedKey`: the CLEAR key commits `""` (L-14); `return` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:499` | `pressedKey`: CANCEL; `return` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |

**Every `postToUiThread` line** (a post runs once at the next update, on the interface thread; nothing promises a poster that dies before the drain anything; the four workers post with `this` captured, and the window outlives them only because it is `main`'s stack object until `return`):

| Site | What | proved: |
| --- | --- | --- |
| `Window.cpp:1276` | the definition: appended under the lock (`:1278`); the owner token `data` is what `unregisterPostedFunctions` (`:1262-1274`) erases by, **without the lock** (L-03) | tree |
| `Window.h:91` | the declaration (the signature § 1 i names with the three doubles) | tree |
| `Window.cpp:1556` | the merge worker's result: runs on the interface thread, pushes `GuiMsgBox` on failure | tree |
| `Window.cpp:1574` | the ignore worker's continuation | tree |
| `Window.cpp:1612` | the format worker's result | tree |
| `Window.cpp:1636` | the ignore worker's continuation | tree |

**The raw pointers the window hands out or holds:**

| Member | What | Handed out or held | Who frees it | proved: |
| --- | --- | --- | --- | --- |
| `Window.h:123` | the cards | handed out raw by `createAsyncNotificationComponent` (`Window.cpp:1168-1174`) | the window, at `:1248` only, once `isRunning()` is false; never in `deinit` or `~Window` (L-02) | tree |
| `Window.h:135` | the toasts | held | the window, at `:358` (stop) and `:377` (faded); never in `deinit` or `~Window` (L-02) | tree |
| `Window.h:147` | the screensaver | set by es-app (`SystemScreenSaver.cpp:49`, T33's) | its owner, es-app; the window only calls it | tree |
| `Window.h:151` | the page stack | `peekGui()` hands the top out raw | each page deletes itself or is deleted by its opener; `~GuiComponent` removes it (`removeGui`); `~Window` deletes what is left (`:59-60`) | tree |
| `Window.h:150` | the screen extras | held | `~Window` (`:53-54`) | tree |
| `Window.h:186` | the mouse capture | set by any component (`setMouseCapture`, `.h:111`) | cleared by `removeGui` (`:86-87`), which every `~GuiComponent` calls -- no dangling capture | tree |
| `Window.h:145` | the help bar | held | `~Window` (`:62`) | tree |
| `Window.h:146` | the overlay | held | `~Window` (`:56`) | tree |

**#1305's three halves** (read; the body was read to its last comment at stage A, `stage-a/issues.out`):

| Half | Lines | What it does | Disposition | proved: |
| --- | --- | --- | --- | --- |
| the window's (this slice's) | `Window.cpp:777-779`, `:1091-1105`, `:1107-1138` | the screensaver starts **from `render()`** on idle time alone (`:778-779`); each page is told (`onScreenSaverActivate`, `:1100`) but cannot refuse, so nothing holds it off while `GuiCloudTransfer` owns the screen; the slideshow's list is cleared only by `resetCounts` from `cancelScreenSaver` (`:1117`) -- a rescan or a `removeGui` does not clear it | a contained hold (the start refused while the top page asks for it) is a candidate for the pause; G-09 frames the start over the transfer page; 3.27 FAILs at the pin until one half lands | tree; 3.27 and G-09 owed |
| T33's (`SystemScreenSaver`) | `es-app/src/SystemScreenSaver.cpp:342-358`, `:378-380`, `:538-548` | the slideshow keeps `FileData*` across picks; its retirement on a rescan is T33's | named for T33's owner at the pause | design |
| T2's (the rescan) | `es-app/src/SystemData.cpp:459-473` | the rescan deletes a `FileData` gone from disk while a holder keeps it | named for T2's owner at the pause | design |

generated, asserted: 18 thread rows (4 detaches), 17 `delete this`, 6 posts, 8 raw pointers, 3 halves of #1305

## The scripts

**How every site's string reaches a shell** (`utils/Platform.cpp`, T36's, read): on Linux `run()` wraps the command as `((((<cmd> 2> <log>/<stderr> ; echo $? >&3) | head -300 > <log>/<stdout>) 3>&1) | (read xs; exit $xs))` (`:162`) and hands it to `system()` when it waits (`:167`) or to `/bin/sh -c` in a double-forked child when it does not (`:172-181`). So each of the four is a shell command line; the § 5 run's direct-spawn count (`system(`/`popen(`/`runSystemCommand(` in the 96) is 0 because the shell is inside `ProcessStartInfo`.

| Site | Function | What builds the string | What is quoted | Which thread | Waits | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| `InputManager.cpp:1272` | `doOnFinish` (`:1242-1284`) | `tocall` = the text of each `<command>` under `<inputAction type="onfinish">` in `es_input.cfg` (`:1262-1268`), as written | nothing quoted by ES: the text is the command line | the interface thread, from `writeDeviceConfig` (`:1238`) -- inside the rebuild's `mJoysticksLock` when reached from the hot-plug write (`:485-623`, `:605`) | **waits** (the constructor's `waitForExit = true`, `Platform.cpp:52`; `system()` at `:167`); the logged line is masked (`:1270`) | tree |
| `Scripting.cpp:140` | `executeScript`, non-WIN32 (`:137-148`) | the script path, quoted only when it has a space (`:92-93`); the event name; up to three arguments, each with every `"` stripped (`:104-107`) and quoted only when it has a space (`:109-112`) | **a `$`, a backtick, a `;` or a `'` in an argument reaches `sh` unquoted** (L-18, 3.4); a file name is a player's (a ROM, a scraped name) | the caller's: `fireEvent`, on the interface thread for the launch events | waits only for `quit` and only in the single-script pass -- the per-event pass passes `""` as the event name (`:177`), so `waitForExit = (eventName == "quit")` (`:142`) is false there even for `quit`; output to `es_script_stdout.log`, `head -300` (`Platform.cpp:162`) | tree |
| `Scripting.cpp:131` | `executeScript`, WIN32, the `-wait` branch (`:127-136`) | as above, with `powershell` prefixed for `.ps1` (`:116-117`) | as above | the caller's | waits (`:133`); WIN32 only, not on the image | tree |
| `Scripting.cpp:43` | `executeCommandsThread`, WIN32 (`:24-54`) | a command queued by `pushCommand` (`:58-`) | as above | the script queue's thread (WIN32) | does not wait (`:45`); WIN32 only | tree |

**The per-event pass runs every file** in `scripts/<event>/` on the device: the extension filter is inside `#if WIN32` (`:172-176`); only the single-script pass filters by extension (`:201-203`) (L-18, 3.5, 3.6).

generated, asserted: 4 sites (4 `ProcessStartInfo` lines in the 96), direct shell spawns 0

## The words

**The French catalog:** `locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the pin, 2173 entries parsed (context-less).

| Site | msgid(s) | French | Tier or verb words | proved: |
| --- | --- | --- | --- | --- |
| `BindingManager.cpp:136` | `YES` / `NO` | `OUI` / `NON` | -- | tree |
| `BindingManager.cpp:150` | `Unknown` / `None` | `Inconnu` / `Aucun` | -- | tree |
| `GunManager.cpp:686` | `%s connected` | `%s connectée` | -- | tree |
| `GunManager.cpp:703` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `GunManager.cpp:724` | `%s connected` | `%s connectée` | -- | tree |
| `GunManager.cpp:734` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `GunManager.cpp:1004` | `%s connected` | `%s connectée` | -- | tree |
| `GunManager.cpp:1031` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `InputManager.cpp:856` | `%s connected` | `%s connectée` | -- | tree |
| `InputManager.cpp:858` | `%s connected` | `%s connectée` | -- | tree |
| `InputManager.cpp:869` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `InputManager.cpp:871` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `TextToSpeech.cpp:177` | `SCREEN READER ENABLED` / `SCREEN READER DISABLED` | `LECTEUR D’ÉCRAN ACTIVÉ` / `LECTEUR D’ÉCRAN DÉSACTIVÉ` | -- | tree |
| `Window.cpp:442` | `Now playing: ` | `En cours : ` | -- | tree |
| `Window.cpp:1367` | `CALIBRATING GUN\nFire on targets to calibrate` | `CALIBRATION DU PISTOLET\nCalibrez en tirant sur les cibles` | -- | tree |
| `Window.cpp:1505` | `Reloaded the games list...` | `Rechargement de la liste des jeux…` | -- | tree |
| `Window.cpp:1542` | `GAME DRIVE DETECTED` | `DISQUE DE JEU DÉTECTÉ` | -- | tree |
| `Window.cpp:1543` | `DEVICE` | `APPAREIL` | -- | tree |
| `Window.cpp:1544` | `MODEL` | `MODÈLE` | -- | tree |
| `Window.cpp:1545` | `SIZE` | `TAILLE` | -- | tree |
| `Window.cpp:1546` | `MOUNT` | `MONTER` | -- | tree |
| `Window.cpp:1547` | `Merge games from this drive partition now?` | `Fusionner les jeux de cette partition du disque dur maintenant ?` | -- | tree |
| `Window.cpp:1548` | `(This will also apply on future boots)` | `(Cela s’appliquera également aux démarrages futurs)` | -- | tree |
| `Window.cpp:1551` | `Merge requested... Please wait.` | `Fusion demandée… Veuillez patienter.` | -- | tree |
| `Window.cpp:1558` | `MERGE FAILED` / `Please check the logs.` / `OK` | `ÉCHEC DE LA FUSION` / `Veuillez consulter les journaux.` / `OK` | -- | tree |
| `Window.cpp:1569` | `NO, IGNORE THIS TIME` | `NON, IGNORER CETTE FOIS` | -- | tree |
| `Window.cpp:1570` | `NO, IGNORE FOREVER` | `NON, IGNORER À JAMAIS` | -- | tree |
| `Window.cpp:1571` | `Adding drive to ignore list...` | `Ajout du disque à la liste d’exclusion…` | -- | tree |
| `Window.cpp:1577` | `YES, MERGE DRIVE` | `OUI, FUSIONNER LES DISQUES` | -- | tree |
| `Window.cpp:1584` | `YES` | `OUI` | -- | tree |
| `Window.cpp:1585` | `NO` | `NON` | -- | tree |
| `Window.cpp:1593` | `N/A` | `N/D` | -- | tree |
| `Window.cpp:1594` | `N/A` | `N/D` | -- | tree |
| `Window.cpp:1597` | `NEW DRIVE DETECTED` | `NOUVEAU DISQUE DÉTECTÉ` | -- | tree |
| `Window.cpp:1598` | `DEVICE` | `APPAREIL` | -- | tree |
| `Window.cpp:1599` | `MODEL` | `MODÈLE` | -- | tree |
| `Window.cpp:1600` | `SIZE` | `TAILLE` | -- | tree |
| `Window.cpp:1601` | `Format and prepare this drive for game storage?` | `Formater et préparer ce disque pour le stockage de jeux ?` | -- | tree |
| `Window.cpp:1602` | `(ALL EXISTING DATA WILL BE ERASED)` | `(TOUTES LES DONNÉES EXISTANTES SERONT EFFACÉES)` | -- | tree |
| `Window.cpp:1605` | `Starting format process...` | `Démarrage du processus de formatage…` | -- | tree |
| `Window.cpp:1614` | `FORMAT FAILED` / `Please check the logs.` / `OK` | `ÉCHEC DU FORMATTAGE` / `Veuillez consulter les journaux.` / `OK` | -- | tree |
| `Window.cpp:1623` | `ARE YOU SURE?` | `ÊTES-VOUS SÛR(E) ?` | -- | tree |
| `Window.cpp:1624` | `NO` | `NON` | -- | tree |
| `Window.cpp:1625` | `YES` | `OUI` | -- | tree |
| `Window.cpp:1631` | `NO, IGNORE THIS TIME` | `NON, IGNORER CETTE FOIS` | -- | tree |
| `Window.cpp:1632` | `NO, IGNORE FOREVER` | `NON, IGNORER À JAMAIS` | -- | tree |
| `Window.cpp:1633` | `Adding drive to ignore list...` | `Ajout du disque à la liste d’exclusion…` | -- | tree |
| `Window.cpp:1639` | `YES, FORMAT & MERGE` | `OUI, FORMATER & FUSIONNER` | -- | tree |
| `Window.cpp:1646` | `NO, IGNORE` | `NON, IGNORER` | -- | tree |
| `Window.cpp:1647` | `YES, FORMAT & MERGE` | `OUI, FORMATER & FUSIONNER` | -- | tree |
| `guis/GuiDetectDevice.cpp:32` | `WELCOME` / `CONFIGURE INPUT` | `BIENVENUE` / `CONFIGURER LES MANETTES` | -- | tree |
| `guis/GuiDetectDevice.cpp:46` | `NO GAMEPADS DETECTED` | `AUCUNE MANETTE DÉTECTÉE` | -- | tree |
| `guis/GuiDetectDevice.cpp:52` | `HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT.` | `MAINTENEZ UN BOUTON DE VOTRE MANETTE POUR LA CONFIGURER.` | -- | tree |
| `guis/GuiDetectDevice.cpp:56` | `PRESS ESC TO CANCEL.` | `APPUYEZ SUR ESC POUR ANNULER.` | -- | tree |
| `guis/GuiDetectDevice.cpp:58` | `PRESS ESC OR A HOTKEY TO CANCEL.` | `APPUYEZ SUR ESC OU UN RACCOURCI POUR ANNULER.` | -- | tree |
| `guis/GuiInputConfig.cpp:125` | `CONFIGURING` | `CONFIGURATION` | -- | tree |
| `guis/GuiInputConfig.cpp:130` | `KEYBOARD` | `CLAVIER` | -- | tree |
| `guis/GuiInputConfig.cpp:132` | `CEC` | `CEC` | -- | tree |
| `guis/GuiInputConfig.cpp:134` | `GAMEPAD %i` | `MANETTE %i` | -- | tree |
| `guis/GuiInputConfig.cpp:139` | `HOLD ANY BUTTON TO SKIP` | `MAINTENEZ UN BOUTON POUR PASSER` | -- | tree |
| `guis/GuiInputConfig.cpp:166` | `-NOT DEFINED-` | `-NON DÉFINI-` | -- | tree |
| `guis/GuiInputConfig.cpp:264` | `OK` | `OK` | -- | tree |
| `guis/GuiInputConfig.cpp:269` | `NO HOTKEY BUTTON HAS BEEN ASSIGNED. THIS IS REQUIRED FOR EXITING GAMES WITH A CONTROLLER. DO YOU WANT TO USE THE SELECT BUTTON AS YOUR HOTKEY?` | `VOUS N’AVEZ PAS ASSIGNÉ DE BOUTON DE RACCOURCI. CECI EST NÉCESSAIRE POUR QUITTER UN JEU AVEC UNE MANETTE. VOULEZ-VOUS UTILISER LE BOUTON SELECT COMME RACCOURCI ?` | -- | tree |
| `guis/GuiInputConfig.cpp:270` | `SET SELECT AS HOTKEY` | `DÉFINIR SELECT COMME RACCOURCI` | -- | tree |
| `guis/GuiInputConfig.cpp:276` | `DO NOT ASSIGN HOTKEY` | `NE PAS ASSIGNER DE RACCOURCI` | -- | tree |
| `guis/GuiInputConfig.cpp:288` | `CANCEL` | `ANNULER` | -- | tree |
| `guis/GuiInputConfig.cpp:379` | `PRESS ANYTHING` | `APPUYEZ SUR UN BOUTON` | -- | tree |
| `guis/GuiInputConfig.cpp:385` | `-NOT DEFINED-` | `-NON DÉFINI-` | -- | tree |
| `guis/GuiInputConfig.cpp:397` | `ALREADY TAKEN` | `DÉJÀ UTILISÉ` | -- | tree |
| `guis/GuiMsgBox.cpp:75` | `YES` | `OUI` | -- | tree |
| `guis/GuiMsgBox.cpp:77` | `OK` | `OK` | -- | tree |
| `guis/GuiMsgBox.cpp:125` | `OK` / `NO` | `OK` / `NON` | -- | tree |
| `guis/GuiTextEditPopup.cpp:34` | `CLEAR` / `CLEAR` | `EFFACER` / `EFFACER` | -- | tree |
| `guis/GuiTextEditPopup.cpp:35` | `CANCEL` / `DISCARD CHANGES` | `ANNULER` / `ANNULER LES CHANGEMENTS` | -- | tree |
| `guis/GuiTextEditPopup.cpp:84` | `BACK` | `RETOUR` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:209` | `SHIFTS FOR UPPER, LOWER, AND SPECIAL` | `MAJ POUR MAJUSCULE, MINUSCULE ET SPÉCIAL` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:214` | `ALT GR` | `ALT GR` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:454` | `CLEAR` | `EFFACER` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:456` | `SHIFT` | `MAJ` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:457` | `OK` | `OK` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:458` | `BACK` | `RETOUR` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:459` | `SPACE` | `ESPACE` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:460` | `DELETE` | `SUPPRIMER` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:486` | `SPACE` | `ESPACE` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:491` | `CLEAR` | `EFFACER` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:497` | `CANCEL` | `ANNULER` | -- | tree |

**msgids without a French entry:** none.

**`GAMEPAD %i`** (`guis/GuiInputConfig.cpp:134`): French `MANETTE %i`; the argument is `getDeviceId() + 1`, the SDL instance id, not the seat (L-17, 3.21).

**The glyph literals** (`\uF...`, outside `_()`; `es-ui-style-guide.md` § Glyphs): `GunManager.cpp:686`, `GunManager.cpp:703`, `GunManager.cpp:724`, `GunManager.cpp:734`, `GunManager.cpp:1004`, `GunManager.cpp:1031`, `InputManager.cpp:856`, `InputManager.cpp:858`, `InputManager.cpp:869`, `InputManager.cpp:871`, `Window.cpp:431`, `Window.cpp:442`, `guis/GuiTextEditPopupKeyboard.cpp:171`, `guis/GuiTextEditPopupKeyboard.cpp:172`, `guis/GuiTextEditPopupKeyboard.cpp:173`, `guis/GuiTextEditPopupKeyboard.cpp:174`, `guis/GuiTextEditPopupKeyboard.cpp:178`, `guis/GuiTextEditPopupKeyboard.cpp:182`, `guis/GuiTextEditPopupKeyboard.cpp:183`, `guis/GuiTextEditPopupKeyboard.cpp:184`, `guis/GuiTextEditPopupKeyboard.cpp:188`, `guis/GuiTextEditPopupKeyboard.cpp:189`, `guis/GuiTextEditPopupKeyboard.cpp:190`, `guis/GuiTextEditPopupKeyboard.cpp:209`, `guis/GuiTextEditPopupKeyboard.cpp:214`, `guis/GuiTextEditPopupKeyboard.cpp:468`, `guis/GuiTextEditPopupKeyboard.cpp:481` -- 27 lines: the twelve notifications carry the light-gun `\uF05B`, the wheel `\uF1B9` or the pad `\uF11B` with one space (a notification's single space) and the song `\uF028` with two; the rest are the keyboard's key faces (DEL `\uF177`, OK `\uF058` or the multi-line `\uF149`, and the shift and alt keys).

**The fork's read for the tiers and the verbs:** 0 of the 86 lines carry a tier or a verb word of D-UI-022's (the column above), so the slice's strings sit outside the cloud vocabulary and owe it nothing. **The sentence-case dialogs are upstream's** (the description dialect, `es-ui-style-guide.md` § Text): recorded, not changed.

The `ngettext` and `pgettext` lines in the 96 outside `LocaleES` and `gettext.h`, with the catalog's context and plural entries:

| Site | Call | French | proved: |
| --- | --- | --- | --- |
| `guis/GuiDetectDevice.cpp:42` | `ngettext` `%i GAMEPAD DETECTED` / `%i GAMEPADS DETECTED` | `%i MANETTE DÉTECTÉE` / `%i MANETTES DÉTECTÉES` | tree |
| `guis/GuiInputConfig.cpp:11` | `pgettext` `joystick` / `NORTH` | `NORD` | tree |
| `guis/GuiInputConfig.cpp:12` | `pgettext` `joystick` / `SOUTH` | `SUD` | tree |
| `guis/GuiInputConfig.cpp:13` | `pgettext` `joystick` / `EAST` | `EST` | tree |
| `guis/GuiInputConfig.cpp:14` | `pgettext` `joystick` / `WEST` | `OUEST` | tree |
| `guis/GuiInputConfig.cpp:16` | `pgettext` `joystick` / `START` | `START` | tree |
| `guis/GuiInputConfig.cpp:17` | `pgettext` `joystick` / `SELECT` | `SELECT` | tree |
| `guis/GuiInputConfig.cpp:19` | `pgettext` `joystick` / `D-PAD UP` | `D-PAD HAUT` | tree |
| `guis/GuiInputConfig.cpp:20` | `pgettext` `joystick` / `D-PAD DOWN` | `D-PAD BAS` | tree |
| `guis/GuiInputConfig.cpp:21` | `pgettext` `joystick` / `D-PAD LEFT` | `D-PAD GAUCHE` | tree |
| `guis/GuiInputConfig.cpp:22` | `pgettext` `joystick` / `D-PAD RIGHT` | `D-PAD DROITE` | tree |
| `guis/GuiInputConfig.cpp:24` | `pgettext` `joystick` / `LEFT ANALOG UP` | `STICK GAUCHE : HAUT` | tree |
| `guis/GuiInputConfig.cpp:25` | `pgettext` `joystick` / `LEFT ANALOG DOWN` | `STICK GAUCHE : BAS` | tree |
| `guis/GuiInputConfig.cpp:26` | `pgettext` `joystick` / `LEFT ANALOG LEFT` | `STICK GAUCHE : GAUCHE` | tree |
| `guis/GuiInputConfig.cpp:27` | `pgettext` `joystick` / `LEFT ANALOG RIGHT` | `STICK GAUCHE : DROITE` | tree |
| `guis/GuiInputConfig.cpp:28` | `pgettext` `joystick` / `RIGHT ANALOG UP` | `STICK DROIT : HAUT` | tree |
| `guis/GuiInputConfig.cpp:29` | `pgettext` `joystick` / `RIGHT ANALOG DOWN` | `STICK DROIT : BAS` | tree |
| `guis/GuiInputConfig.cpp:30` | `pgettext` `joystick` / `RIGHT ANALOG LEFT` | `STICK DROIT : GAUCHE` | tree |
| `guis/GuiInputConfig.cpp:31` | `pgettext` `joystick` / `RIGHT ANALOG RIGHT` | `STICK DROIT : DROITE` | tree |
| `guis/GuiInputConfig.cpp:33` | `pgettext` `joystick` / `LEFT SHOULDER` | `TRANCHE GAUCHE (L1)` | tree |
| `guis/GuiInputConfig.cpp:34` | `pgettext` `joystick` / `RIGHT SHOULDER` | `TRANCHE DROITE (R1)` | tree |
| `guis/GuiInputConfig.cpp:35` | `pgettext` `joystick` / `LEFT TRIGGER` | `GÂCHETTE GAUCHE (L2)` | tree |
| `guis/GuiInputConfig.cpp:36` | `pgettext` `joystick` / `RIGHT TRIGGER` | `GÂCHETTE DROITE (R2)` | tree |
| `guis/GuiInputConfig.cpp:37` | `pgettext` `joystick` / `LEFT STICK PRESS` | `CLIC STICK GAUCHE (L3)` | tree |
| `guis/GuiInputConfig.cpp:38` | `pgettext` `joystick` / `RIGHT STICK PRESS` | `CLIC STICK DROIT (R3)` | tree |
| `guis/GuiInputConfig.cpp:40` | `pgettext` `joystick` / `HOTKEY` | `RACCOURCI` | tree |
| `guis/GuiInputConfig.cpp:163` | `pgettext` with a runtime key (xgettext cannot see it; the `fake_gettext_*` macros above exist so it can) | -- | tree |
| `guis/GuiInputConfig.cpp:347` | `ngettext` `HOLD FOR %iS TO SKIP` / `HOLD FOR %iS TO SKIP` | `MAINTENEZ PENDANT %iS POUR PASSER` / `MAINTENEZ PENDANT %iS POUR PASSER` | tree |

generated, asserted: 86 lines in 10 files, 97 occurrences, 61 msgids, 0 without French; 27 glyph lines; 28 `pgettext`/`ngettext` lines, 0 without French

## The structure

**The include reach** (every header of the 96, ranked by its includers across `es-core/` and `es-app/` at the pin; a change to a header with outside includers is a change to their lanes):

| Header | Includers in the 96 | es-core outside the 96 | es-app | Total | proved: |
| --- | --- | --- | --- | --- | --- |
| `es-core/src/Log.h` | 21 | 30 | 57 | 108 | tool-run |
| `es-core/src/LocaleES.h` | 13 | 22 | 66 | 101 | tool-run |
| `es-core/src/GuiComponent.h` | 9 | 28 | 37 | 74 | tool-run |
| `es-core/src/Window.h` | 10 | 14 | 45 | 69 | tool-run |
| `es-core/src/guis/GuiMsgBox.h` | 4 | 0 | 43 | 47 | tool-run |
| `es-core/src/ThemeData.h` | 8 | 20 | 11 | 39 | tool-run |
| `es-core/src/Paths.h` | 8 | 9 | 16 | 33 | tool-run |
| `es-core/src/InputManager.h` | 5 | 7 | 6 | 18 | tool-run |
| `es-core/src/guis/GuiTextEditPopup.h` | 1 | 0 | 17 | 18 | tool-run |
| `es-core/src/guis/GuiTextEditPopupKeyboard.h` | 1 | 0 | 17 | 18 | tool-run |
| `es-core/src/math/Misc.h` | 7 | 6 | 2 | 15 | tool-run |
| `es-core/src/AudioManager.h` | 4 | 2 | 7 | 13 | tool-run |
| `es-core/src/ImageIO.h` | 1 | 8 | 4 | 13 | tool-run |
| `es-core/src/PowerSaver.h` | 4 | 6 | 3 | 13 | tool-run |
| `es-core/src/animations/LambdaAnimation.h` | 1 | 3 | 9 | 13 | tool-run |
| `es-core/src/math/Vector2i.h` | 4 | 8 | 1 | 13 | tool-run |
| `es-core/src/Scripting.h` | 3 | 2 | 7 | 12 | tool-run |
| `es-core/src/TextToSpeech.h` | 3 | 3 | 6 | 12 | tool-run |
| `es-core/src/math/Vector2f.h` | 6 | 5 | 1 | 12 | tool-run |
| `es-core/src/BindingManager.h` | 3 | 3 | 5 | 11 | tool-run |
| `es-core/src/Sound.h` | 3 | 3 | 4 | 10 | tool-run |
| `es-core/src/watchers/WatchersManager.h` | 3 | 4 | 3 | 10 | tool-run |
| `es-core/src/math/Transform4x4f.h` | 2 | 7 | 0 | 9 | tool-run |
| `es-core/src/VolumeControl.h` | 1 | 1 | 4 | 6 | tool-run |
| `es-core/src/animations/Animation.h` | 3 | 0 | 3 | 6 | tool-run |
| `es-core/src/InputConfig.h` | 3 | 1 | 1 | 5 | tool-run |
| `es-core/src/guis/GuiDetectDevice.h` | 1 | 0 | 4 | 5 | tool-run |
| `es-core/src/watchers/BatteryLevelWatcher.h` | 1 | 3 | 1 | 5 | tool-run |
| `es-core/src/FavoriteMusicManager.h` | 2 | 0 | 2 | 4 | tool-run |
| `es-core/src/HelpStyle.h` | 2 | 1 | 1 | 4 | tool-run |
| `es-core/src/MameNames.h` | 1 | 0 | 3 | 4 | tool-run |
| `es-core/src/anim/ThemeStoryboard.h` | 4 | 0 | 0 | 4 | tool-run |
| `es-core/src/math/Vector4f.h` | 4 | 0 | 0 | 4 | tool-run |
| `es-core/src/watchers/NetworkStateWatcher.h` | 1 | 2 | 1 | 4 | tool-run |
| `es-core/src/CECInput.h` | 3 | 0 | 0 | 3 | tool-run |
| `es-core/src/GunManager.h` | 3 | 0 | 0 | 3 | tool-run |
| `es-core/src/MultiStateInput.h` | 1 | 0 | 2 | 3 | tool-run |
| `es-core/src/ThemeVariables.h` | 3 | 0 | 0 | 3 | tool-run |
| `es-core/src/guis/GuiInfoPopup.h` | 2 | 0 | 1 | 3 | tool-run |
| `es-core/src/math/Vector3f.h` | 2 | 1 | 0 | 3 | tool-run |
| `es-core/src/playlists/M3uPlaylist.h` | 1 | 1 | 1 | 3 | tool-run |
| `es-core/src/AsyncHandle.h` | 0 | 0 | 2 | 2 | tool-run |
| `es-core/src/HelpPrompt.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/LogPolicy.h` | 1 | 0 | 1 | 2 | tool-run |
| `es-core/src/Splash.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/anim/StoryboardAnimator.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/anim/ThemeAnimation.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/animations/AnimationController.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/guis/GuiInputConfig.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/playlists/AnimatedGifPlaylist.h` | 1 | 1 | 0 | 2 | tool-run |
| `es-core/src/gettext.h` | 1 | 0 | 0 | 1 | tool-run |

**The guards** (every preprocessor condition naming a platform or feature macro; the host's stand-in parses one branch, stage C):

| Macro | Lines | First sites | On the host | proved: |
| --- | --- | --- | --- | --- |
| `WIN32` | 69 | `AudioManager.cpp:22`, `GunManager.cpp:22`, `GunManager.cpp:197`, `GunManager.cpp:319`, `GunManager.cpp:556`, `GunManager.cpp:794` ... | not the image's branch: the `#else` is parsed | tool-run |
| `HAVE_UDEV` | 23 | `GunManager.cpp:15`, `GunManager.cpp:163`, `GunManager.cpp:180`, `GunManager.cpp:208`, `GunManager.cpp:311`, `GunManager.cpp:516` ... | **not parsed** without libudev headers; G-01's `ldd` settles the image's | tool-run |
| `HAVE_LIBCEC` | 11 | `CECInput.cpp:3`, `CECInput.cpp:23`, `CECInput.cpp:94`, `CECInput.cpp:154`, `CECInput.cpp:175`, `CECInput.cpp:196` ... | **not parsed**; CEC compiled out | tool-run |
| `_WIN32` | 10 | `Log.cpp:200`, `Splash.cpp:331`, `VolumeControl.cpp:234`, `VolumeControl.cpp:378`, `VolumeControl.cpp:471`, `VolumeControl.cpp:533` ... | as WIN32 | tool-run |
| `APPLE` (double-underscore-wrapped: the compiler's predefined macro) | 9 | `Log.cpp:204`, `VolumeControl.cpp:230`, `VolumeControl.cpp:265`, `VolumeControl.cpp:456`, `VolumeControl.cpp:488`, `VolumeControl.cpp:589` ... | not the image's | tool-run |
| `_ENABLE_PULSE_` | 7 | `VolumeControl.cpp:11`, `VolumeControl.cpp:243`, `VolumeControl.cpp:269`, `VolumeControl.cpp:460`, `VolumeControl.cpp:492`, `VolumeControl.cpp:593` ... | **not parsed** on the host (no pulse headers); the ALSA branch is | tool-run |
| `_RPI_` | 5 | `CECInput.cpp:8`, `CECInput.cpp:53`, `CECInput.cpp:95`, `CECInput.cpp:162`, `VolumeControl.cpp:217` | not defined for these images: the other branch is parsed | tool-run |
| `_ENABLE_TTS_` | 5 | `TextToSpeech.cpp:53`, `TextToSpeech.cpp:94`, `TextToSpeech.cpp:138`, `TextToSpeech.cpp:197`, `TextToSpeech.cpp:268` | **not parsed**; compiled out on the image | tool-run |
| `BATOCERA` | 4 | `InputManager.cpp:585`, `Paths.cpp:24`, `Paths.cpp:48`, `Splash.cpp:103` | not defined in a ROCKNIX build: the other branch is parsed | tool-run |
| `ROCKNIX` | 3 | `InputManager.cpp:585`, `Paths.cpp:76`, `Splash.h:10` | parsed with `-DROCKNIX` in the stand-in (stage C) | tool-run |
| `SDL_JoystickDevicePathById` | 1 | `InputManager.cpp:840` | defined only by an SDL that carries it; the image's SDL decides, the host parses without it | tool-run |
| `_DEBUG` | 1 | `Paths.cpp:40` | not defined in a release build | tool-run |

**The CMake lists:** every `.cpp` of the 96 is named once in `es-core/CMakeLists.txt` (44 of 44); the headers it does not list: `es-core/src/HelpPrompt.h`, `es-core/src/Scripting.h`; 9 lines carry a trailing `# batocera`, 7 of them naming a path of the 96 (`:19`, `:20`, `:96`, `:98`, `:160`, `:229`, `:231`); the lists are unconditional but for the two `if(` blocks at `:278` (the GLES renderer pair) and `:287` (`MSVC`'s source groups). **T21's hunk** (the pin to T21's tip `3ae9610b0`): 5 added lines -- `HttpText.h`, `RecoveryOutcome.h` (`@@ -9`), `utils/DownloadFile.h` (`@@ -124`), `HttpText.cpp` (`@@ -151`), `utils/DownloadFile.cpp` (`@@ -259`); the integration's, named in the hand-back (§ 1 h, L-26). `proved: tool-run`.

**`Window.cpp:29`** includes `../es-app/src/ApiSystem.h` for `processStorageRequest`'s four workers (`:1554-1637`): es-core depending on es-app, upstream ROCKNIX's, outside the lanes (D-UI-079); **recorded as upstream's, not changed** (L-04). **The `ROCKNIX` lines:** `es-core/src/InputManager.cpp:585`, `es-core/src/Paths.cpp:76`, `es-core/src/Splash.h:10` (3).

**L-22, the stale rule sentence:** `.claude/rules/es-native-ui.md:30` calls `AsyncNotificationComponent` the *top-right progress card*; the card is centred at the pin (`Window.cpp:1192`, the fork's hunk) and the same rule says so at `:191-197` and `:208`. For the coordinator's sweep (`tools/archaeology --reversal`), not the lane's edit.

**L-25, the footnote:** the inventory records `last_fork_commit 1593c299f3 2026-09-10` on `guis/GuiTextEditPopupKeyboard.h`, which is byte-identical to the merge base `cada856d86` (`git diff --quiet` exit 0): a fork touch undone or merged away. Nothing to fix; § The merge debt carries it.

**The map:** `tools/es-menu-map-check`'s `SOURCE_DIRS` at its `:58` includes `es-core/src/guis`; at the pin it printed `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0 (stage A, `stage-a/runs.out`). Its three patterns over this slice's 6 dialogs: `guis/GuiDetectDevice.cpp` 0, `guis/GuiInfoPopup.cpp` 0, `guis/GuiInputConfig.cpp` 0, `guis/GuiMsgBox.cpp` 0, `guis/GuiTextEditPopup.cpp` 0, `guis/GuiTextEditPopupKeyboard.cpp` 0 -- **0 titles**: these dialogs build no `GuiSettings`/`MenuComponent` page, so the checker sees nothing here and has nothing to miss; a stream that adds a page must map it (D-UI-039).

generated, asserted: 51 headers' reach, 12 guard macros, 44 `.cpp` named once, 2 headers unregistered, 9 `# batocera` lines, 2 CMake `if(`, 3 `ROCKNIX` lines, 0 map titles

## The merge debt

`cada856d86` is the merge base against `rocknix/master` (`f6c542872e`), and `bccd715707` is its parent and the stale `upstream/master` (2026-09-22). Upstream has **0** commits on the 96 since the base (14 on any path; numstat 0), **96 of 96** blobs are identical between the base and master, and **83 of 96** between the pin and master. Batocera's **twelve** commits since `1750dded8c` touch **nine** files, six of them fork-modified (`GunManager.cpp`, `InputManager.cpp`, `Log.cpp`, `Window.cpp`, `Window.h`, `guis/GuiMsgBox.cpp`): the reconciliation list only. T21's `3ae9610b0` hunk in `es-core/CMakeLists.txt` (five added lines, § The structure) is the integration's. **T34's ES tip, read at stage B:** local `568ef099d` and `origin` `a9017ff50` at 06:29:09Z (`git -C <W> rev-parse`/`diff --name-only`): **empty inside the 96** (19 and 18 files on other paths). The first read, at 06:08:37Z, was local `db12b1598a` and `origin` `2cbb62d7bd`, also empty inside the 96; the hand-back reads it a third time. L-25's footnote: `guis/GuiTextEditPopupKeyboard.h` carries a fork commit in the inventory and is byte-identical to the base. `proved: tool-run` (stage A's run 5, `stage-a/runs.out`).

## The runs

**The § 5 runs** (stage A, `stage-a/runs.sh` -> `stage-a/runs.out`, 05:59:32Z to 05:59:35Z; each block wrapped in `rc=$?` and a `date +%s` pair; every figure as the brief expects but the deltas `00` names):

| # | Run | Exit | Wall | Figure (the command's own lines) | A FAIL would mean | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | the scope | 0 | 0 s | `96; 44; 51; 1` | the paths list is not the slice the brief names: a scope drift, stop (§ 8) | tool-run |
| 2 | the ES worktree at the pin, clean; the bases; the counts | 0 | 0 s | `16dbac5211; 0; cada856d86; f6c542872e; b2ceb55a7e; 1750dded8c; 725; 14; 1; 15` | the read is not the pin's, or a base moved: the merge debt is re-derived | tool-run |
| 3 | the lines two ways | 0 | 1 s | `wc -l 22567; grep -c 22575; no newline: es-core/src/MultiStateInput.cpp 52/53; no newline: es-core/src/MultiStateInput.h 18/19; no newline: es-core/src/anim/StoryboardAnimator.cpp 236/237; no newline: es-core/src/anim/ThemeAnimation.h 145/146; no newline: es-core/src/anim/ThemeStoryboard.cpp 241/242; no newline: es-core/src/math/Vector2f.cpp 38/39; no newline: es-core/src/math/Vector4f.cpp 106/107; no newline: es-cor ...` | a line rule differs: the coverage table's lines are wrong | tool-run |
| 4 | the fork's delta | 0 | 0 s | `13 files changed, 247 insertions(+), 71 deletions(-); 13 files changed, 247 insertions(+), 71 deletions(-); 13 files changed, 247 insertions(+), 71 deletions(-); 1; added rc=0; 7	0	es-core/CMakeLists.txt; 2	0	es-core/src/GunManager.cpp; 8	1	es-core/src/InputConfig.cpp; 5	2	es-core/src/InputManager.cpp; 19	40	es-core/src/Log.cpp; 3	3	es-core/src/Scripting.cpp; 4	1	es-core/src/Splash.h; 49	6	es-core/src/Window.cpp; 2	0 ...` | the fork changed the slice since the brief: the 13 are re-read | tool-run |
| 5 | upstream's delta: the merge-debt record | 0 | 0 s | `0; upstream commits rc=1; 0; upstream numstat rc=1; identical to rocknix/master: 83; identical to cada856d86: 83; MB-vs-master identical: 96; 12; 9; 6` | upstream moved on the 96: the merge debt grows | tool-run |
| 6 | the other lanes' deltas inside the 96 | 0 | 0 s | `== m6-es-launch-path-649; == m6-es-cloud-pages-665; == m6-es-achievements-pages-667; == m6-es-state-and-bridge-668; 1 file changed, 5 insertions(+); == m6-es-guimenu-673; == m6-es-pages-678; == m6-es-app-views-scrapers-679; == m6-es-app-system-680; == m6-es-core-components-681` | another lane edited inside the 96: a collision for the hand-back | tool-run |
| 7 | the strings, two ways | 0 | 0 s | `_(" lines TOTAL 86 in 10 files; 97; BindingManager.cpp:2 GunManager.cpp:6 InputManager.cpp:4 TextToSpeech.cpp:1 Window.cpp:37 guis/GuiDetectDevice.cpp:5 guis/GuiInputConfig.cpp:14 guis/GuiMsgBox.cpp:3 guis/GuiTextEditPopup.cpp:3 guis/GuiTextEditPopupKeyboard.cpp:11` | the strings moved: § The words is regenerated | tool-run |
| 8 | the log lines | 0 | 0 s | `LOG(Log lines TOTAL 158 in 20 files` | the log lines moved | tool-run |
| 9 | the threads and the lifetimes | 0 | 0 s | `es-core/src/Log.cpp:60 es-core/src/Log.cpp:180 es-core/src/Scripting.cpp:18 es-core/src/Scripting.cpp:68 es-core/src/TextToSpeech.cpp:92 es-core/src/TextToSpeech.h:47 es-core/src/VolumeControl.cpp:32 es-core/src/VolumeControl.cpp:203 es-core/src/Window.cpp:1554 es-core/src/Window.cpp:1563 es-core/src/Window.cpp:1572 es-core/src/Window.cpp:1575 es-core/src/Window.cpp:1608 es-core/src/Window.cpp:1619 es-core/src/Window ...` | a thread was added or removed: § The lifetimes' base | tool-run |
| 10 | the process spawns | 0 | 0 s | `es-core/src/InputManager.cpp:1272 es-core/src/Scripting.cpp:43 es-core/src/Scripting.cpp:131 es-core/src/Scripting.cpp:140; 0; shell spawns rc=1` | a new spawn: § The scripts' base | tool-run |
| 11 | the writes | 0 | 0 s | `es-core/CMakeLists.txt:122 es-core/CMakeLists.txt:257 es-core/src/AudioManager.cpp:539 es-core/src/AudioManager.cpp:610 es-core/src/FavoriteMusicManager.cpp:71 es-core/src/FavoriteMusicManager.cpp:115 es-core/src/InputManager.cpp:1225 es-core/src/InputManager.cpp:1232 es-core/src/Log.cpp:179; 9; 0; atomic rc=1` | a write was added: § The input's base | tool-run |
| 12 | the reads | 0 | 0 s | `41; 0; uncached rc=1` | a read changed its cache use: 3.11's base | tool-run |
| 13 | the input and the help bar | 0 | 0 s | `3; 6; 745 1001 1009 1011 1012 1077 1397 1398; 0; mHelp setOpacity rc=1` | a help-prompt definition or a `setOpacity` caller changed (L-21) | tool-run |
| 14 | the constants | 0 | 0 s | `es-core/src/components/MenuComponent.cpp:14:#define BUTTON_GRID_HORIZ_PADDING (Renderer::getScreenWidth()*0.022); es-core/src/components/MenuComponent.cpp:547:	float buttonGridWidth = (float)BUTTON_GRID_HORIZ_PADDING * buttons.size(); // initialize to padding; es-core/src/components/MenuComponent.cpp:555:		buttonGrid->setColWidthPerc(i, (buttons.at(i)->getSize().x() + BUTTON_GRID_HORIZ_PADDING) / buttonGridWidth);; e ...` | the two defines changed (L-13) | tool-run |
| 15 | the includes | 0 | 0 s | `18; 2; es-core/src/Window.cpp:29:#include "../es-app/src/ApiSystem.h"; not once: es-core/src/HelpPrompt.h; not once: es-core/src/LocaleES.cpp; not once: es-core/src/LocaleES.h; not once: es-core/src/Scripting.h; not once: es-core/src/gettext.h; not once: es-core/src/guis/GuiInfoPopup.cpp; not once: es-core/src/guis/GuiInfoPopup.h; not once: es-core/src/guis/GuiTextEditPopupKeyboard.cpp; not once: es-core/src/guis/Gui ...` | an include changed: the stand-in's fakes and `Window.cpp:29` | tool-run |
| 16 | the in-source gates | 0 | 1 s | `es-core/src/AudioManager.cpp:22 es-core/src/CECInput.cpp:3 es-core/src/CECInput.cpp:8 es-core/src/CECInput.cpp:23 es-core/src/CECInput.cpp:53 es-core/src/CECInput.cpp:94 es-core/src/CECInput.cpp:95 es-core/src/CECInput.cpp:154 es-core/src/CECInput.cpp:162 es-core/src/CECInput.cpp:175 es-core/src/CECInput.cpp:196 es-core/src/CECInput.cpp:281 es-core/src/CECInput.h:7 es-core/src/CECInput.h:24 es-core/src/GunManager.cpp ...` | a guard was added: the stand-in's branch list | tool-run |
| 17 | the non-ASCII bytes | 0 | 0 s | `28; git grep -P rc=0; AudioManager.cpp:3; GunManager.cpp:1; InputManager.cpp:2; guis/GuiTextEditPopupKeyboard.cpp:22; files with a non-ascii byte: 4; comment: AudioManager.cpp:3; comment: GunManager.cpp:1; comment: InputManager.cpp:2; files with a non-ascii comment line: 3` | a non-ASCII byte in a comment near `_()`: xgettext stops the image build (`es-code-traps.md`) | tool-run |
| 18 | the French | 0 | 0 s | `49:msgid "CANCEL" 3779:msgid "HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT." 3898:msgid "GAMEPAD %i" 3915:msgid "SET SELECT AS HOTKEY" 3918:msgid "DO NOT ASSIGN HOTKEY" 6923:msgid "CLEAR"; locale/lang/fr/LC_MESSAGES/emulationstation2.po:2207; es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without; es-untranslated rc=0; es-untranslated: 703 fork string(s) in the source, 703 with French, 0 withou ...` | a msgid lost its French (D-UI-051) | tool-run |
| 19 | the candidate lines | 0 | 0 s | `339 340; 1164; 66 78 94 143 181 196; 946 960; 1225 1232; 44 234 240; 134` | a lead's line moved: § The leads re-anchored | tool-run |
| 20 | the menu map | 0 | 1 s | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing; es-menu-map-check rc=0; 989 docs/es-menu-map.md; SOURCE_DIRS = ["es-app/src/guis", "es-core/src/guis"]` | a screen the map does not describe (D-UI-039) | tool-run |
| 21 | the compile | 0 | 0 s | `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root); es-syntax-check rc=2; /home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682/es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory; plain g++ rc=1; pugixml root present` | the host gained a toolchain, or the first error moved: the stand-in's fakes | tool-run |
| 22 | STAGE C -- the lane's scripts, which do not exist at stage A | CANNOT | -- | `CANNOT at stage A: the three scripts below are the lane's stage-C inputs (stage-a/syntax-check.sh, tools/t35-build-tests.sh, stage-c/pl25-screensaver.py) and do not exist yet; each runs at stage C; (not run) bash docs/audits/*-epic-m6-es-core-window-input/stage-a/syntax-check.sh 2>&1 \| tail -n 46; (not run) bash docs/audits/*-epic-m6-es-core-window-input/tools/t35-build-tests.sh "$W" 2>&1 \| tail -n 10; (not run) pyth ...` | -- | -- |
| 23 | STAGE A, after the pointer is read -- the removal check: the lane's own tip, b51dd8a805 at stage A (the merge commit the dispatch comment and the pointer name, filling the brief's placeholder) | 0 | 0 s | `(the lane's own tip is b51dd8a805 at stage A: the merge commit the dispatch comment and the pointer name)` | the lane wrote under `packages/`, `projects/` or `tools/`, or in the ES worktree: § 8 | tool-run |
| 24 | (added at stage A) the ROCKNIX lines over the 96, which the gates run's expectation names and the block does not run | 0 | 0 s | `es-core/src/InputManager.cpp:585 es-core/src/Paths.cpp:76 es-core/src/Splash.h:10; 3` | a `ROCKNIX` gate was added or removed | tool-run |
| 25 | (added at stage A) the gates run's line count, which the block prints as one line | one line | -- | `128` | the gates list changed | tool-run |

**The generators, each seen to exit 1 on a constructed drift before it was trusted** (`stage-b/drift.sh` -> `stage-b/generators.txt`; (a) a wrong expectation, (b) the paths list with a cited file dropped, (c) the pin's paths read at the base, where the cited lines have moved):

| Generator | Clean | Its last line | (a) | (b) | (c) | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| `tools/t35-coverage.py` | 0 | `generated, asserted: 96 rows, 22575 lines (grep -c rule); read tiers fork-added 1 / fork-modified 12 / upstream-carried 83; inventory fork-own 13 / upstream-carried 83` | `rows=95` -> 1: `FAIL t35-coverage: rows 96, expected 95` | without `Window.cpp` -> 1: `FAIL t35-coverage: rows 95, expected 96` | at `bccd715707` -> 1: `FAIL t35-coverage: es-core/CMakeLists.txt: 296 lines at bccd715707, inventory 303` | tool-run |
| `tools/t35-leads.py` | 0 | `generated, asserted: 29 leads (24 confirmed at the tree, 1 contradicted, the rest read or supported), 27 floor cases anchored` | `cases=26` -> 1: `FAIL t35-leads: cases 27, expected 26` | without `Window.cpp` -> 1: `FAIL t35-leads: es-core/src/Window.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-leads: es-core/src/Window.cpp:339 does not carry /mNotificationMessages\.back\(\)/ (reads: 'return;')` | tool-run |
| `tools/t35-surfaces.py` | 0 | `generated, asserted: 22 rows: 5 containers and the lock, 15 sites (one of them T34's component's, outside the 96), and T34's two held patches` | `sites=14` -> 1: `FAIL t35-surfaces: sites 15, expected 14` | without `Window.cpp` -> 1: `FAIL t35-surfaces: es-core/src/Window.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-surfaces: es-core/src/Window.h:123 does not carry /std::vector<AsyncNotificationComponent\*> mAsyncNo` | tool-run |
| `tools/t35-input.py` | 0 | `generated, asserted: 7 write-site rows (5 writes, 2 reads the grep counts), 5 exists rows; the writes grep 9 hits` | `real_writes=7` -> 1: `FAIL t35-input: real_writes 5, expected 7` | without `InputManager.cpp` -> 1: `FAIL t35-input: es-core/src/InputManager.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-input: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-locks.py` | 0 | `generated, asserted: 67 lock lines in 11 files (4 includes, 2 `weak_ptr::lock`), 10 locks summarised, 7 threads` | `lines=66` -> 1: `FAIL t35-locks: lines 67, expected 66` | without `Window.cpp` -> 1: `FAIL t35-locks: lines 55, expected 67` | at `bccd715707` -> 1: `FAIL t35-locks: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-lifetimes.py` | 0 | `generated, asserted: 18 thread rows (4 detaches), 17 `delete this`, 6 posts, 8 raw pointers, 3 halves of #1305` | `detach=5` -> 1: `FAIL t35-lifetimes: detach 4, expected 5` | without `Window.cpp` -> 1: `FAIL t35-lifetimes: es-core/src/Window.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-lifetimes: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-scripts.py` | 0 | `generated, asserted: 4 sites (4 `ProcessStartInfo` lines in the 96), direct shell spawns 0` | `shell_direct=1` -> 1: `FAIL t35-scripts: shell_direct 0, expected 1` | without `Scripting.cpp` -> 1: `FAIL t35-scripts: es-core/src/Scripting.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-scripts: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-words.py` | 0 | `generated, asserted: 86 lines in 10 files, 97 occurrences, 61 msgids, 0 without French; 27 glyph lines; 28 `pgettext`/`ngettext` lines, 0 without French` | `msgids=62` -> 1: `FAIL t35-words: msgids 61, expected 62` | without `Window.cpp` -> 1: `FAIL t35-words: lines 49, expected 86` | at `bccd715707` -> 1: `FAIL t35-words: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-includes.py` | 0 | `generated, asserted: 51 headers' reach, 12 guard macros, 44 `.cpp` named once, 2 headers unregistered, 9 `# batocera` lines, 2 CMake `if(`, 3 `ROCKNIX` lines, 0 map titles` | `rocknix=4` -> 1: `FAIL t35-includes: rocknix 3, expected 4` | without `Window.cpp` -> 1: `FAIL t35-includes: es-core/src/Window.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-includes: es-core/src/LogPolicy.h not at bccd715707` | tool-run |

**Owed at stage C and the window** (not run at stage B):

| Run | When | Figure expected |
| --- | --- | --- |
| the stand-in syntax check over the 44 (`stage-a/syntax-check.sh`, the 13 fakes, the pugixml root; the udev and pulse branches named as not parsed) | stage C | a `<file>: rc N` line per `.cpp` |
| the unit build (`tools/t35-build-tests.sh`, `window-input-tests` among the binaries) | stage C | `TOTAL: N test cases in B binaries`, 0 failed |
| the seven candidates' FAIL lines (3.1, 3.4, 3.5, 3.10, 3.11, 3.14, 3.19) against the unfixed extracts, or their PASS-at-pin record | stage C | one line each |
| 3.27, T33's `stage-c/pl25-screensaver.py` re-run unchanged | stage C | its FAIL line at the pin |
| the guest window G-01 to G-12 | after the grant on #682 | § The guest cycle |

generated, asserted: 25 run blocks, 9 generators with three drifts each

## The guest cycle

**Not run at stage B.** The window is asked for on #682 at stage B's end, with the plan and bound in `stage-b/window-plan.md`: 30 minutes plus 5 of grace, a 1,560 s plan, G-01 to G-12, two boots. It lands here once granted: the grant's time, the START and RETURN posts with their first lines, the timer's PID and the censuses, the host file's lines, the image's `BUILD_ID` read at 640x480, every frame read back at EN and FR and labelled by side, the second boot, the disk retired with path, size and sha, and the leftover check.

## The streams

Stage E: **written by the coordinator after stage D**, as for T21, T26, T32, T33 and T34. The lane leaves this heading and puts the following to the pause:

- **Four register rows expected** (brief § 9), each put to the coordinator and none decided by the lane: F-ES-24's toast behind a long card; the re-queued toast's duration (L-01, 3.14; the order itself is D-UI-093's, already decided, so the pause rules only whether the fix lands); the second `BUTTON_GRID_HORIZ_PADDING` (L-13); and the CLEAR without a question (L-14).
- **Rule-6 candidates, contained:** L-01 (pop the front), L-03 (take the lock), L-10 (log `item`), L-11 (probe outside the list lock, #1283's es-core half), L-24 (a stack event), L-06's `es_input.cfg` through `AtomicFile`, and L-07's read with `exists(path, false)` once 3.11 has run.
- **The collision:** T34's `s2-window.patch` (#1310), which changes `createAsyncNotificationComponent`'s return. It touches 10 es-app callers in five lanes and the three doubles, so § 1 i names it in the hand-back.
- **#1305:** the window's half (a start the top page can refuse) beside T33's and T2's halves, named for their owners.

## Positives

- `GuiMsgBox::deleteMeAndCall` copies the callback before `delete this` and calls the copy after (`guis/GuiMsgBox.cpp:286-292`): the safe shape, and the model for the other 16. None of them touches a member after the delete. `proved: tree`.
- Every `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), and `removeGui` clears the mouse capture (`Window.cpp:86-87`), so a captured component freed under its page leaves no dangling pointer. `proved: tree`.
- `processPostedFunctions` copies and clears under the lock, then runs outside it (`Window.cpp:1292-1307`), so a post may post again without a deadlock. `proved: tree`.
- One floating surface at a time holds both ways (D-UI-093): a toast waits for the card (`:336-337`), and a card puts the toast's words back (`:1161-1165`). `proved: tree`; G-02 frames it.
- The window and T34's component compute the same centred position (`:1192`, `AsyncNotificationComponent.cpp:112`). `proved: tree`.
- `doOnFinish` masks its logged command (`InputManager.cpp:1270`). `configureEmulators` carries no device name (`:1481-1482`), so the blob it splices is index and hex only. `proved: tree`.
- All 61 msgids and all 28 `pgettext`/`ngettext` entries have their French at the pin. `proved: tool-run`.
- The logger and the watcher thread are joined (`Log.cpp:76-77` from `onExit`; `WatchersManager.cpp:154` from `stop()`). Every `.cpp` of the 96 is registered once in `es-core/CMakeLists.txt`. `proved: tree`.

## The #585 lines owed

One line per upstream-carried defect closed under rule 6, in the lane's shape, **never sent** (D-WORKFLOW-164, D-WORKFLOW-165). At stage B none is closed yet, so each is a line owed **if** the pause rules its fix. They are listed for the coordinator, beginning with T33's never-posted candidate:

- `es-core/src/watchers/WatchersManager.cpp:181-199` (`rocknix/master`): the watcher list lock is held across every `check()`, so `ResetComponent`/`GetComponent`/`Register`/`Unregister` wait on the interface thread for a network probe. Fix: snapshot under the lock and probe outside it, re-validating. Evidence: 3.1. This is T33's candidate and this slice's lock line.
- `es-core/src/Scripting.cpp:88-113` (`rocknix/master`): arguments are quoted only on a space and `"` is stripped, so `$`/backtick reach `/bin/sh -c`. Fix: single-quote every argument. Evidence: 3.4.
- `es-core/src/Window.cpp:339-340` (upstream's queue): the toast queue pops its newest. Fix: pop the front. Evidence: 3.14.
- `es-core/src/Window.cpp:1262-1274`: `unregisterPostedFunctions` walks `mFunctions` without the lock its two siblings take. Fix: take it. Evidence: 3.17.
- `es-core/src/InputManager.cpp:946`, `:960`: the approximate-match log reads the node before it is assigned. Fix: log `item`. Evidence: 3.10.
- `es-core/src/InputManager.cpp:795`: a `new SDL_Event` per F4 press, never freed. Fix: a stack event.
- `es-core/src/guis/GuiTextEditPopupKeyboard.cpp:14`: the second `BUTTON_GRID_HORIZ_PADDING`, **only if** the pause deletes or renames it.
- **No line** for the controllers blob: at the pin it carries no device name (L-20, contradicted).

## What T36 and T37 inherit

Brief § 5 item 3's items, with their lines:

1. **The provenance table:** 1 / 12 / 83, with both bases named (`cada856d86` against `rocknix/master`, `1750dded8c` against `batocera/master`). § Coverage, § The merge debt.
2. **The surfaces table:** the queue's two containers and the lock, and every enqueue, dequeue, layout and free with its invariant (`Window.cpp:293-1307`). § The surfaces.
3. **The input table:** every write site with its mechanism and atomicity, and every `exists(` of the input files with its writer (`InputManager.cpp:893`, `:1187`, `:1225`, `:1232`, `:1250`; `GuiDetectDevice.cpp:127`). § The input.
4. **The locks table:** every lock, its sites and order, and the interface-thread entry points that block (`WatchersManager.cpp:66`, `:78`, `:94`, `:143`, `.h:35`). § The locks.
5. **The lifetimes table:** 18 thread lines, 4 detaches, 17 `delete this`, 6 posts and 8 raw pointers. § The lifetimes.
6. **The scripts table:** the four `ProcessStartInfo` sites and `Platform.cpp:162-181`'s shell. § The scripts.
7. **The `window-input-tests` build recipe** (the doubles, the extracts, the pugixml root, the fakes the first errors forced): owed at stage C, `tools/t35-build-tests.sh`.
8. **The stand-in's rc per file over the 44:** owed at stage C, `stage-a/syntax-check.out`.
9. **The branches it did not parse:** `HAVE_UDEV` (23 lines), `_ENABLE_PULSE_` (7), `_ENABLE_TTS_` (5), `HAVE_LIBCEC` (11), and the WIN32 branches. § The structure's guards.
10. **The `exists` cache's answer for T36's `FileSystemUtil`:** misses are stored (`FileSystemUtil.cpp:296`, `:323`), and a writer outside `Utils::FileSystem` is invisible to the cache. Read at stage B; 3.11 proves it at stage C.
11. **`Window.cpp:29`'s disposition:** recorded as upstream's (L-04, D-UI-079). § The structure.


## The first reader's 03-retrospective.md (whole)

# Retrospective: M6.P2 T35, EmulationStation's window, input and the rest of es-core (#682)

The code auditor's retrospective of the slice (the audit's Phase 3), not the lane's ceremony retro (that is `docs/retros/`, after stage E).

## 3.1 What the slice is for

The window is the one object every page, card and toast goes through: it owns the page stack, the floating surfaces, the posted functions and the screensaver. The input manager turns SDL's devices into configurations and writes `es_input.cfg`. The watchers poll the network and the battery on their own thread. The script runner fires the event hooks. The six es-core dialogs are the box, the two text popups, the toast, the detect page and the configuration page. Most of it is upstream's and unchanged since the base; the fork's 13 files carry one floating surface at a time (D-UI-093), the centred card, the log policy, the masked logs and the dialog's measured height.

## 3.2 What the fork changed, and what drifted

`13 files changed, 247 insertions(+), 71 deletions(-)` against `bccd715707`. The fork's own rule for the queue (D-UI-093) was written over an upstream pop that contradicts it (`Window.cpp:339-340`); the fork's comment beside the re-queue (`:1159-1160`) even relies on the contradiction. The card moved to the centre and one rule sentence did not follow (`es-native-ui.md:30`). Upstream has not touched the 96 since the base.

## 3.3 What none of the fixes noticed

- The D-UI-093 fix tested that a toast waits for a card; nothing tested two toasts.
- The input file's writer and its readers go through different layers (pugixml and `Utils::FileSystem`), so the cache that serves the readers never hears from the writer.
- The quoting rule in `executeScript` was written for spaces; the shell it feeds reads `$`, backticks and quotes.
- `WatchersManager`'s lock was sized for the list and held for the probe.

## 3.4 What the record says about catches

T33 found the watcher lock (#1283) and the screensaver use-after-free (#1305) from the es-app side; this slice proves the es-core halves with cases that fail at the pin. T34's held patches (the card handle, the dialog's height) land on files of this slice, which is why both are named collisions rather than adopted.

## 3.5 The seams

The slice's cases are extracts of the pin's lines in the smallest double that compiles them (`tools/t35-extract.py` refuses a range that moved), and `WatchersManager.cpp` linked whole behind the tree's own `Log.h` double. The next slice that touches `Window.cpp` or `InputManager.cpp` inherits those extracts and the stand-in's fakes.


## The first reader's 04-analysis.md (whole)

# Analysis: M6.P2 T35, EmulationStation's window, input and the rest of es-core (#682)

reviewed-at: `b1f2908a55` (distribution); reviewed-at-es: `16dbac5211eea7e70db7394372033be2be7df829` (the 96 paths). Written at stage C, before the stage-D pause. Every item in `05` is Open until the pause disposes it.

## Executive summary

The slice is `es-core/**` as `rest`: 96 paths (1 fork-added, 12 fork-modified, 83 upstream-carried; 22,575 lines) -- the window and its floating surfaces, the input manager and its configuration file, the watchers, the script runner, the log, the six es-core dialogs and the device layer. `02` was generated by ten scripts that assert every count and cited line at the pin; each was seen to fail on three constructed drifts before it was trusted.

**Twenty-four findings, 0 Critical, 0 High, 6 Medium, 18 Low** (`05`). The six Medium findings are each proven by a case that **fails at the pin** in `window-input-tests` or by T33's unchanged harness:

1. **The watchers' lock** (PL-01, #1283's es-core half): a probe holds the list lock and five interface-thread entry points wait for it -- `ResetComponent` returned after **1,491 ms** behind a 1.5 s probe (3.1).
2. **The toast queue drains newest first** (PL-02), against D-UI-093's decided row *the order is the order things happened* (3.14).
3. **Script arguments reach `/bin/sh` unquoted** (PL-03): `$( )` and backticks in a ROM or scraped name expand whenever an event folder holds a hook (3.4).
4. **The `exists` cache keeps a miss after `save_file`** (PL-04): the second pad configured in a session can replace the first in `es_input.cfg` (3.11).
5. **The window's half of #1305** (PL-05): the screensaver starts from `render()` over a page that owns the screen; T33's harness reports a heap-use-after-free at the pin (3.27).
6. **The teardown frees no card and no popup** (PL-06), with T34's `s2-window.patch` named a collision, not adopted.

The stand-in syntax check passes **44 of 44** at rc 0 with the fakes the first errors forced; the unit build prints **`TOTAL: 249 test cases in 6 binaries`** with the tree's 239 passing and `window-input-tests`' seven candidate cases failing at the pin, as designed. One lead was contradicted by the tree (L-20: the controllers blob carries no device name), and one brief read corrected (`InputManager.cpp:420` is WIN32-only). The guest window is granted and queued (slot 3 on the host); its rows are recorded in `02` § The guest cycle when it runs.

## Acceptance-criteria scorecard

#682's 21 criteria, at stage C (each ticked by the coordinator from the artifact, never from this table):

| # | Criterion (short) | State at stage C | Artifact |
| ---: | --- | --- | --- |
| 1 | the folder's files | `00` to `05`, `stage-a/` to `stage-c/`, `tools/`; `second-opinions/` with the calls; `guest-cycle/` after the window; `stage-d/`, `stage-e/` later | `ls` at the hand-back |
| 2 | the lint (pre-issue, then resolution, then `--issue`) | pre-issue after the seat's calls | `tools/lint-audit-artifacts` |
| 3 | the review plan, the seat's two calls | the probe and the refutation granted; run at stage C | `second-opinions/` |
| 4 | the punch list at Phase 7 | 24 items Open before stage D | `05` |
| 5 | `reviewed-at`/`fixed-at` headers; nothing under `packages/`, `projects/`, `tools/` | the lane's diff against `b51dd8a805` empty there; the ES worktree at the pin | `00` |
| 6 | `01` § Scope's block | done | `01` |
| 7 | `02` § Coverage 96 rows | done (the awk prints 96) | `02` |
| 8 | `02` § The runs' counts | done, both rules | `02` § The runs |
| 9 | the five sections generated, each with drifts | done | `02`, `stage-b/generators.txt` |
| 10 | § The surfaces' rows, the order, the duration, F-ES-24 | done (3.14's FAIL line at stage C) | `02`, `stage-c/build-tests.out` |
| 11 | § The input's rows, the hotkey names, `doOnFinish` | done; G-01's `inputAction` count owed | `02` |
| 12 | § The merge debt | done; T34's tip read twice, the third at the hand-back | `02` |
| 13 | § The runs: every § 5 command, the stand-in rc per file, the unit build's TOTAL, the candidates' FAIL-then-PASS | the FAIL half and the stand-in done; PASS halves after stage E | `stage-a/syntax-check.out`, `stage-c/build-tests.out` |
| 14 | § The guest cycle | queued (slot 3) | `guest-cycle/` |
| 15 | `00`'s record of what was not done | current | `00` |
| 16 | `04` § Q1 to Q7, bugs with traces, the take-up table | this file; bugs filed at stage D | here |
| 17 | `proved:` cells; `question:`; § What T36 and T37 inherit | done | `02`, `05` |
| 18 | the retro | after stage E | `docs/retros/` |
| 19 | the map | 0 titles from the slice's dialogs; a stream that adds a page maps it | `02` § The structure |
| 20 | the checks on both branches | at the hand-back | -- |
| 21 | the unit build's TOTAL with 0 failed after the fixes | after stage E | -- |

## Risk assessment

- **The lock (PL-01)** is the one finding a player can feel on a healthy device: every page that registers or resets a watcher (the network and battery rows) waits for whichever probe is running, for as long as its network call takes. #1283 tracks it; the fix is contained to `WatchersManager.cpp`.
- **The quoting (PL-03)** turns a file name into a command only where a hook script exists in an event folder. Whether the image ships one is G-01's read; with one shipped, the risk rises to High and the pause should know before it rules.
- **The cache (PL-04)** loses a pad's configuration only on a device whose user `es_input.cfg` was absent at startup and two pads are configured in one session; the fix is three `false` arguments.
- **The teardown and #1305 (PL-05, PL-06)** are use-after-free shapes: #1305's is proven by T33's harness; the teardown's needs a holder that outlives the window, which `main.cpp`'s order makes rare (the window is `main`'s stack object).
- **No finding is a data-loss path on the cloud lanes**; the writes that matter here are the input files, and none is atomic (PL-08).

## Coverage boundary

- **Read:** the 96 at the pin, whole for the 13 fork files, by line for the 83 where `02` cites them; the outside lines each generator asserts as `outside` (T36's `FileSystemUtil.cpp` and `Platform.cpp`, T34's components, es-app's `main.cpp`, `NetworkThread.cpp`, `FileData.cpp`, `SystemScreenSaver.cpp`).
- **Run on the host:** the stand-in over the 44 (`HAVE_UDEV`, `_ENABLE_PULSE_`, `_ENABLE_TTS_`, `HAVE_LIBCEC` and the WIN32 branches not parsed); the tree's five unit binaries; `window-input-tests` (10 cases); T33's PL-25 harness.
- **Not run:** a ThreadSanitizer case for 3.3 and 3.17, an ASan case for 3.2 (owed, named in `05`); the guest (queued); the pad's hot-plug, hold and axis paths (G-10 `CANNOT`, no pad on the guest -- an open item to test).
- **Outside the slice by ownership:** the holders of the card (T18, T20, T34), the rescan (T2), the screensaver's list (T33), the sign-in window (T18), the launch templates (T3), the file cache (T36).

## The questions

### Q1 The window's queue and its surfaces

One floating surface at a time holds both ways (`Window.cpp:336-337`, `:1161-1165`). **The order does not:** the queue pops its back (`:339-340`, upstream's), so toasts show newest first against D-UI-093's decided row (PL-02, 3.14 FAIL). A re-queued toast returns whole (`:1164`), recorded as by design (PL-13). F-ES-24 -- every toast waits behind any card, the hasher's included -- goes to the pause as a register question (PL-14). The card's position agrees between the window (`:1183`, `:1192`) and T34's component (`AsyncNotificationComponent.cpp:64`, `:112`).

### Q2 The input's writes and the `<command>` execution

Five writes, none atomic (`InputManager.cpp:1225`, `:1232`; `FavoriteMusicManager.cpp:71`, `:115`; `Log.cpp:46`); the grep's other two sites read (PL-08). **The cache keeps a miss after `save_file`** (PL-04, 3.11 FAIL): `:893`, `:1187`, `:1250` all read through it. `doOnFinish` runs each `onfinish` `<command>` synchronously on the interface thread, inside the joystick lock on a hot-plug write (`:1272`, `:485-623`, PL-19). The two hotkey names are `hotkey` (`:1105-1107`) and `hotkeyenable` (`GuiInputConfig.cpp:273`, `InputConfig.cpp:188`) (PL-20). The approximate-match log names nothing (PL-09, 3.10 FAIL). The SDL-mapping read at `:420` is WIN32-only.

### Q3 `WatchersManager`'s lock

`run()` holds `mWatchersLock` across every `check()` and takes `mNotificationLock` inside it (`WatchersManager.cpp:181-199`, `:128`): the order is list then observers, and the observers run on the watcher thread. Five entry points the interface thread calls wait for a probe (PL-01, 3.1 FAIL at 1,491 ms). `mRunning`/`mPaused` are plain `bool`s read outside any lock (`:161`, `:187`; 3.3 owed). The thread is joined at `WatchersManager::stop()` (`main.cpp:1330`) before `window.deinit()`.

### Q4 Lifetimes

`deinit` and `~Window` free no card or popup (PL-06); the posted functions' unregister walks without the lock (PL-07); the screensaver starts over any page and #1305's use-after-free follows (PL-05, 3.27 FAIL). Every `delete this` (17, all in the six dialogs) is followed by nothing that touches a member; `GuiMsgBox::deleteMeAndCall` copies first (`:286-292`). The mouse capture cannot dangle (`Window.cpp:86-87`, `GuiComponent.cpp:30`). **What `postToUiThread` promises** (take-up row 708): to run the function once, on the interface thread, at the next update; nothing to a poster that dies before the drain -- a weak token the posts check is T34's contained fix, `AppWindow` T33's.

### Q5 `Scripting`'s quoting, and what runs the shell

Every `ProcessStartInfo` line becomes a shell command (`utils/Platform.cpp:162-181`: `system()` when waiting, `/bin/sh -c` otherwise). `executeScript` quotes only on a space and strips `"` (`Scripting.cpp:98-113`): PL-03, 3.4 FAIL. The per-event pass runs every file (`:169-178`; the filter is WIN32-only): PL-18, 3.5 FAIL. The per-event `quit` scripts do not wait (`:142`, `:177`): PL-17. The masks: `:49`, `:122`, `:129` (WIN32), `InputManager.cpp:1270`, `:1486`; the non-WIN32 executor logs only the script's path (`:138`).

### Q6 The popups' accelerator and padding, the help bar, and the words

The accelerator binds the only button, else the first `OK`/`NO`, else the last (`GuiMsgBox.cpp:116-134`), and an unconfigured pad's any button fires it (`:257`) (PL-15). The keyboard's `BUTTON_GRID_HORIZ_PADDING` is a second definition with another value (PL-11, 3.19 FAIL). CLEAR and `x` commit `""` with no question (PL-12). `GAMEPAD %i` numbers the SDL instance (PL-16). **The words:** 86 lines, 97 occurrences, 61 msgids, every one with French; 28 `pgettext`/`ngettext` lines, every pair with French; 0 tier or verb words of D-UI-022's; the fork's one added msgid is `CLEAR` -> `EFFACER`. The window's help-bar collection drops only a repeated icon (`Window.cpp:1023`) and passes an unknown key through untouched (`:1062-1074`) -- L-28's empty bar and L-29's untranslated key are not the window's doing.

### Q7 Cost against value, the structure and the merge debt

`Window.cpp:29` reaches into es-app for four detached storage workers: upstream ROCKNIX's, recorded (PL-22, D-UI-079). The Ctrl debug chords run ungated (PL-21). Every `.cpp` of the 96 is registered once in `es-core/CMakeLists.txt`; T21's five-line hunk is the integration's. The merge debt is small: upstream has 0 commits on the 96 since the base; batocera's twelve on nine files are the reconciliation list. The cost on the launch path -- `fireEvent`'s three directory listings and three scans per event, `configureEmulators` built on every launch -- is priced from the guest when the window runs (L-19).

## The take-up table (brief § 2), each row disposed

| Row | Found by | Disposition |
| ---: | --- | --- |
| 706 | T33 L-01 / PL-14 / #1283 | **rule 6**: PL-01 (3.1 FAIL); a #585 line owed |
| 707 | T2 PC-1 | **read**: the teardown frees nothing (PL-06); **pause** with T34's `s2-window.patch` as a collision |
| 708 | T34 L-12 | **read**: the promise stated (Q4); T34's weak token to the pause, `AppWindow` T33's |
| 709 | #1276 | **read**: `AppWindow::closing()` (`main.cpp:1322`) and `WatchersManager::stop()` (`:1330`) precede `window.deinit()` (`:1358`); the fix is T33's S4a |
| 710 | T34 L-05 | **pause**: PL-11 (3.19 FAIL); the second copy is not deleted here |
| 711 | T21 PL-26 / #1192 | **pause**: neither popup takes a masking mode (`GuiTextEditPopup.h:15-16`, `GuiTextEditPopupKeyboard.h:13-14`); deferred to #1192 |
| 712 | T26 L-22 | **read**: the rule stated (Q6); **pause**: PL-15 |
| 713 | T26 | **read**: `deleteMeAndCall` copies before the delete (`GuiMsgBox.cpp:286-292`): kept |
| 714 | `es-code-traps.md`, D-UI-034 | **read**: the 2x2 shell over the N x 2 button row is this slice's; the grid's `canMoveCursor` T34's; T34's G-06 frames it |
| 715 | `es-code-traps.md`, #1245 | **read**: a second full-screen page draws no Window bar (`Window.cpp:743-745`); a page that wants one calls `renderHelpPromptsEarly` (`:999-1003`) |
| 716 | T34 § 5 item 3 | **read**: none of the eight `mHelp->` lines calls `setOpacity`; batocera's guard has no caller here |
| 717 | T34's brief | **read**: agree (`02` § The surfaces, item 13) |
| 718 | D-UI-093, F-ES-24 | **read** and **pause**: PL-02 (a defect against the row), PL-14 (F-ES-24 to the pause) |
| 719 | D-UI-105, D-UI-106 | **read**: the 0.9 W cap is `GuiInfoPopup`'s (3.22's anchor, `:17`); the words are the pages' |
| 720 | T34 L-07 | **read**: `Window.cpp:29` recorded as upstream's (PL-22) |
| 721 | #1212 | **read**: the window updates only the top page (`Window.cpp:542-543`) and feeds input only to it (`:287-288`) -- the invariant holds at the pin |
| 722 | T2 FD-9 / FD-19 | **rule 6**: PL-03 (3.4 FAIL); a #585 line owed |
| 723 | T2, time to play | **read**; the price from the guest (owed) |
| 724 | the 2026-09-24 audit's masks | **read**: five masked lines in the slice (Q5); the non-WIN32 executor logs only the path; `fireEvent`'s Debug line logs its arguments unmasked (`Scripting.cpp:155`), ROM paths, not secrets |
| 725 | T2 FD-6 / FD-7 | **read**: the blob carries index and GUID only (`InputManager.cpp:1481-1482`): L-20 contradicted for es-core; no #585 line |
| 726 | #54 | **read**: `deinit` calls `InputManager::deinit` when it deinitialises the renderer (`Window.cpp:199-200`); the handover is the sign-in window's (T18's) |
| 727 | T34 L-01 | **read**: `buttonLabel` returns an unknown key unchanged (`InputConfig.cpp:353-366`); the icon table is T34's |
| 728 | T26, T31 | **read**: the harness fact holds; the fakes the first errors forced are in `stage-a/fakes/` (`t35-sdl-more.h` and the T35 sections), and the stand-in passes 44 of 44 |
| 729 | T34's brief | **read**: `InputManager.h` brings `SDL_joystick.h`, pugixml and `GunManager.h` (`:5-10`); `GunManager.h` brings `<libudev.h>`, `<SDL.h>`, `<Windows.h>` under its guards (`:10-13`) |
| 730 | T34's brief | **carried**: the tile text's theme contract is T34's file; not re-read in this pass |
| 731 | D-UI-021, #63, #65 | **read**: the window hands a key to the top page and nothing else (`Window.cpp:287-288`) |
| 732 | #1178 | **no T35 action** |
| 733 | T32 | **no T35 action** |
| 734 | T34 PL-05 | **read**: the window's collection drops only a repeated icon (`:1023`); the empty bar is the prompts it was given or the image's composition; G-11 frames the page |
| 735 | T34 PL-04 / D-UI-133 | **read**: `setHelpPrompts` passes an unknown key untouched, sorted with index 0 (`:1062-1074`) |
| 736 | T33 PL-25 / #1305 | **read** then **pause**: PL-05 (3.27 FAIL); T33's and T2's halves named |
| 737 | #585 | the lines owed are in `02` § The #585 lines owed; never sent by the lane |

## Renovation face

### Q1 Modernize

`std::thread(...).detach()` with `this` captured (`Window.cpp:1554-1637`) and raw owning pointers for the cards and popups (`Window.h:123`, `:135`) are the pre-C++11 idioms here; a handle the window keeps (T34's `s2-window.patch`) is the modern shape, held for the integration.

### Q2 Standards

The house rules this slice touches: one floating surface at a time (kept), the order things happened (broken, PL-02), confirmations ask (CLEAR does not, PL-12), the last known good state (no atomic write of the input file, PL-08).

### Q3 Bugs

Six Medium findings with FAIL-at-pin cases (PL-01 to PL-05; PL-06 a design defect). Filed as `bug`s at stage D with their traces and `Already written:` lines.

### Q4 Package currency

The slice has no package of its own; its upstream-carried 83 are byte-identical to `rocknix/master`. Batocera's twelve commits are the reconciliation list in `02` § The merge debt.

### Q5 Efficiency

The hot-plug rebuild re-reads `es_input.cfg` once per pad per event on the interface thread; `fireEvent` lists six places per event on the launch path. Priced on the guest.

### Q6 Dead ends

The four Ctrl debug chords (PL-21) and the WIN32-only mapping-file pass are dead on the device; recorded, not removed (D-UI-079 for the chords).

### Q7 Clarity and structure

`Window.cpp:29`'s cross-tree include, the stale rule sentence (PL-23) and the two meanings of one macro name (PL-11).

## Instruction File Recommendations

- `es-code-traps.md` § Three things a font is not already says a marker written after startup reads as absent; PL-04 adds the input file to that list, and that **an uncached `exists(p, false)` rewrites the cache entry** (`FileSystemUtil.cpp:161-162`) -- worth a sentence when the fix lands.
- The stale sentence at `es-native-ui.md:30` is the coordinator's sweep (PL-23).

## Second opinion

Pending at the time of writing: depth `independent`, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`), the probe and the refutation granted on #682 (06:45 UTC). This section records the plan, the served model, the outcome and every finding's grade once the refutation returns.

## Quality self-check

- Every count in `02` is a tool's line, asserted by a generator seen to fail on a constructed drift.
- Every Medium finding has a case that fails at the pin, run on the host; none rests on a reading alone.
- One lead was contradicted by the tree and is withdrawn (L-20); one read was corrected (`:420`); 3.11's first ordering passed for a reason the case now records.
- Not done at the time of writing: the guest's rows, the sanitizer cases 3.2, 3.3 and 3.17, the PASS halves (after stage E).


## The first reader's 05-punch-list.md (whole)

# Punch list (Phases 5 and 6) — M6.P2 T35, EmulationStation's window, input and the rest of es-core (#682)

Written by `tools/t35-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 the queue and its surfaces, Q2 the input's writes and commands, Q3 the watchers' lock, Q4 lifetimes, Q5 scripts and the shell, Q6 the popups and the words, Q7 cost, structure and merge debt). Every item is **Open** until the stage-D pause disposes it.

reviewed-at-es: 16dbac5211eea7e70db7394372033be2be7df829

## PL-01: A watcher's probe holds the list lock, and the interface thread waits for it

- **Severity:** Medium; **category:** Locks; **question:** Q3
- **Source finding:** L-11, 3.1, #1283's es-core half
- **Lines at the pin:** `watchers/WatchersManager.cpp:181-199` against `:66`, `:78`, `:94`, `:143`, `.h:35`
- **Owner:** T35 (#1283's es-core half; the observers es-app's)
- **What is wrong:** `run()` holds `mWatchersLock` across every `check()` (a network or battery probe) and then takes `mNotificationLock` inside it; `RegisterComponent`, `UnregisterComponent`, `ResetComponent`, `GetComponent` and the destructor take the same lock from the interface thread. 3.1 at the pin: `ResetComponent` returned after **1,491 ms** behind a 1.5 s probe. A real probe's bound is its network timeout.
- **Proposed disposition:** a `bug` under rule 6: snapshot the due watchers under the lock, probe outside it, re-validate before writing back (EP-13's `WatcherInfo` lifetime kept); 3.1 the covering case, 3.2 (ASan) and 3.3 (TSan) beside it
- **proved:** fixture (3.1 FAIL at the pin)

## PL-02: The toast queue drains newest first, against D-UI-093's decided row

- **Severity:** Medium; **category:** Surfaces; **question:** Q1
- **Source finding:** L-01, 3.14
- **Lines at the pin:** `Window.cpp:339-340` against `:334-335` and `decision-register.md:404`; `:1159-1160`
- **Owner:** T35 (upstream's pop, the fork's rule)
- **What is wrong:** `processNotificationMessages` takes `back()` and `pop_back()`; D-UI-093 says *the order is the order things happened*. Two toasts queued under a card (a pad connected then disconnected) show in reverse. 3.14 at the pin: B shown before A.
- **Proposed disposition:** a `bug` under rule 6: pop the front, and reverse the re-queue loop at `:1163-1164` so a returned toast keeps its place; 3.14 the covering case; a #585 line
- **proved:** fixture (3.14 FAIL at the pin)

## PL-03: A script argument reaches /bin/sh unquoted, so $( ) and backticks in a file name run

- **Severity:** Medium; **category:** Scripts; **question:** Q5
- **Source finding:** L-18, 3.4, T2 FD-9/FD-19
- **Lines at the pin:** `Scripting.cpp:92-113`, `:137-148`; `utils/Platform.cpp:162-181` (T36's)
- **Owner:** T35 with T2 (the callers' arguments)
- **What is wrong:** `executeScript` quotes an argument only when it contains a space and strips every `"`; `ProcessStartInfo::run` hands the line to `system()` or `/bin/sh -c`. A ROM `a$(id)b.zip` or a scraped name with a backtick is expanded by the shell whenever any script sits in an event folder. 3.4 at the pin: the argument arrives unquoted. Medium because it needs a hook present; G-01 reads whether the image ships one under `/usr/bin/scripts/`.
- **Proposed disposition:** a `bug` under rule 6: single-quote every argument (with `'` escaped) and the script path; 3.4 the covering case; a #585 line
- **proved:** fixture (3.4 FAIL at the pin)

## PL-04: A file written by pugixml after a cached miss reads as absent for the rest of the session

- **Severity:** Medium; **category:** Input; **question:** Q2
- **Source finding:** L-07, 3.11
- **Lines at the pin:** `InputManager.cpp:893`, `:1187`, `:1225`, `:1239`, `:1250`; `utils/FileSystemUtil.cpp:296`, `:323` (T36's)
- **Owner:** T35 (the three reads); the cache T36's
- **What is wrong:** With the cache on, a first `exists(es_input.cfg)` that misses is remembered; `save_file` writes through `fopen`, so the cache never learns of the file. On a device whose user `es_input.cfg` did not exist at startup, the second pad configured in the session skips the merge at `:1187` and its save keeps that pad alone; `loadInputConfig` after the write (`:1239`) and `doOnFinish` (`:1250`) read the same miss. 3.11 at the pin: the cached read stays false after the write.
- **Proposed disposition:** a `bug` under rule 6: `exists(path, false)` at `:893`, `:1187`, `:1250` (the `es-code-traps.md` § Three things a font is not rule); 3.11 the covering case; G-01 reads the precondition on the image
- **proved:** fixture (3.11 FAIL at the pin)

## PL-05: The window's half of #1305: the screensaver starts over a page that owns the screen

- **Severity:** Medium; **category:** Lifetimes; **question:** Q4
- **Source finding:** L-27, 3.27, #1305
- **Lines at the pin:** `Window.cpp:777-779`, `:1091-1105`, `:1107-1138` (`:1117`); `SystemScreenSaver.cpp:342-358` (T33's); `SystemData.cpp:459-473` (T2's)
- **Owner:** T35 (the window's half); T33's and T2's halves
- **What is wrong:** The screensaver starts from `render()` on idle time alone; each page is told and cannot refuse; the slideshow's `FileData` list is cleared only when it stops. A transfer's rescan then deletes a game the next pick reads. 3.27 at the pin: `heap-use-after-free ... in FileData::getImagePath`.
- **Proposed disposition:** #1305 (open, `bug`): the window's half proposed for the pause (a start the top page can hold off); T33's and T2's halves named for their owners; 3.27 PASS when one half lands
- **proved:** fixture (3.27 FAIL at the pin)

## PL-06: The window's teardown frees no card and no popup, and the holders keep raw pointers

- **Severity:** Medium; **category:** Lifetimes; **question:** Q4
- **Source finding:** L-02, T2 PC-1
- **Lines at the pin:** `Window.cpp:188-207`, `:49-63`, `:1246-1248`; the holders in es-app (§ The surfaces)
- **Owner:** T35 (the teardown); the holders T18's, T20's, T34's
- **What is wrong:** `deinit` and `~Window` leave `mAsyncNotificationComponent` and `mNotificationPopups` as they are; the one free is `:1248`. A card alive at `deinit` is drawn again at the next `init()`; a holder's late call after `:1248` is a use after free the card cannot detect.
- **Proposed disposition:** a design ruling at the pause: T34's `s2-window.patch` (#1310) is a collision (10 es-app callers, 3 doubles); the window-side alternative frees cards and popups in `deinit` and refuses a close after it
- **proved:** tree

## PL-07: `unregisterPostedFunctions` walks the posted functions without their lock

- **Severity:** Low; **category:** Lifetimes; **question:** Q4
- **Source finding:** L-03, 3.17
- **Lines at the pin:** `Window.cpp:1262-1274` against `:1278`, `:1296`
- **Owner:** T35
- **What is wrong:** `postToUiThread` and `processPostedFunctions` take `mNotificationMessagesLock`; the erase loop does not. A worker posting while a page unregisters races the vector.
- **Proposed disposition:** a `bug` under rule 6: take the lock; 3.17 (TSan) the covering case
- **proved:** tree (3.17 owed)

## PL-08: The input files are written in place, none atomically

- **Severity:** Low; **category:** Input; **question:** Q2
- **Source finding:** L-06
- **Lines at the pin:** `InputManager.cpp:1225`, `:1232`; `FavoriteMusicManager.cpp:71`, `:115`
- **Owner:** T35
- **What is wrong:** Five writes, `AtomicFile::` 0. A cut `es_input.cfg` fails to parse: the pad reads as unconfigured and the next save keeps one device. The grep's seven sites include two read-mode `fopen`s.
- **Proposed disposition:** a pause ruling (D-CLOUD-078's family): `es_input.cfg` through the fork's `AtomicFile`, the rest recorded
- **proved:** tree

## PL-09: The approximate-match log reads the node before it is assigned

- **Severity:** Low; **category:** Input; **question:** Q2
- **Source finding:** L-10, 3.10
- **Lines at the pin:** `InputManager.cpp:946`, `:960`
- **Owner:** T35 (upstream's lines, rule 6)
- **What is wrong:** Both lines log `configNode`'s attributes one line before `configNode = item`: empty fields. 3.10 at the pin: no device named.
- **Proposed disposition:** log `item`; 3.10 the covering case; a #585 line
- **proved:** fixture (3.10 FAIL at the pin)

## PL-10: F4 leaks one SDL_Event per press

- **Severity:** Low; **category:** Input; **question:** Q2
- **Source finding:** L-24
- **Lines at the pin:** `InputManager.cpp:795`
- **Owner:** T35 (upstream's line, rule 6)
- **What is wrong:** `new SDL_Event()` is never freed; `SDL_PushEvent` copies.
- **Proposed disposition:** a stack event; a #585 line
- **proved:** tree

## PL-11: One macro name, two values: the keyboard's button padding

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-13, 3.19, T34 PL-16
- **Lines at the pin:** `guis/GuiTextEditPopupKeyboard.cpp:14`, `:220` against `components/MenuComponent.cpp:14` (T34's)
- **Owner:** T35 (the define); T34's comment names it
- **What is wrong:** `BUTTON_GRID_HORIZ_PADDING` is `0.022 W` in the menu and `0.0052083333 W` in the keyboard: 14.08 px against 3.33 px at 640. 3.19 at the pin: the two differ.
- **Proposed disposition:** a pause ruling: the keyboard's own name (the value is its design), or one definition
- **proved:** fixture (3.19 FAIL at the pin)

## PL-12: CLEAR and the keyboard's `x` commit an empty value with no question

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-14
- **Lines at the pin:** `guis/GuiTextEditPopupKeyboard.cpp:392-397`, `:491-496`; `guis/GuiTextEditPopup.cpp:34`
- **Owner:** the pause (the lanes' fields: the cloud folder, the Wi-Fi key)
- **What is wrong:** One press empties the field and submits it; `es-ui-style-guide.md` § Confirmations asks a consequential action to ask.
- **Proposed disposition:** a pause ruling (a register row); G-06 frames it on the image
- **proved:** tree; guest owed

## PL-13: The re-queued toast returns with a fresh default duration

- **Severity:** Low; **category:** Surfaces; **question:** Q1
- **Source finding:** L-01, 3.14 (second case)
- **Lines at the pin:** `Window.cpp:1164`
- **Owner:** T35
- **What is wrong:** A toast half-read and taken off by a new card comes back whole, not for its remainder. Recorded as by design; costs seconds, loses no words.
- **Proposed disposition:** recorded as written; the pause may rule otherwise
- **proved:** fixture (PASS, recorded)

## PL-14: F-ES-24: every toast waits while any card is up, a long upstream card included

- **Severity:** Low; **category:** Surfaces; **question:** Q1
- **Source finding:** F-ES-24, brief § 9
- **Lines at the pin:** `Window.cpp:336-337`
- **Owner:** the pause
- **What is wrong:** The hasher's minutes-long card holds every toast behind it (D-UI-079 keeps that card as upstream has it). Recorded Low on 2026-09-25 and never dispositioned.
- **Proposed disposition:** a pause ruling: stands, or a bound (brief § 9's first register row)
- **proved:** tree

## PL-15: Back on a dialog without OK or NO takes the last button, and an unconfigured pad's any button fires it

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-12, 3.18
- **Lines at the pin:** `guis/GuiMsgBox.cpp:116-134`, `:257`
- **Owner:** upstream's; the callers choose labels
- **What is wrong:** The accelerator's third branch binds the last button; `:257` fires it for any button of an unconfigured pad.
- **Proposed disposition:** recorded; G-04 and G-05 frame the behaviour
- **proved:** tree; guest owed

## PL-16: The configuration page's subtitle numbers the SDL instance, not the seat

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-17, 3.21
- **Lines at the pin:** `guis/GuiInputConfig.cpp:134`
- **Owner:** T35 (upstream's line, rule 6)
- **What is wrong:** `GAMEPAD %i` prints `getDeviceId() + 1`; a third pad plugged in reads GAMEPAD 3 whatever its seat.
- **Proposed disposition:** the seat or the name; a #585 line
- **proved:** tree

## PL-17: The per-event `quit` scripts do not wait

- **Severity:** Low; **category:** Scripts; **question:** Q5
- **Source finding:** L-18
- **Lines at the pin:** `Scripting.cpp:142`, `:177`
- **Owner:** T35
- **What is wrong:** The per-event pass passes `""` as the event name, so `waitForExit = (eventName == "quit")` is false there even for `quit`; only the single-script pass waits.
- **Proposed disposition:** a pause question; recorded
- **proved:** tree

## PL-18: A per-event folder runs every file in it

- **Severity:** Low; **category:** Scripts; **question:** Q5
- **Source finding:** L-18, 3.5
- **Lines at the pin:** `Scripting.cpp:169-178`
- **Owner:** T35
- **What is wrong:** The extension filter is inside `#if WIN32`; on the device a `notes.txt` is handed to the shell. 3.5 at the pin: it is run.
- **Proposed disposition:** a pause ruling: the single-script pass's filter for both passes; 3.5 the covering case
- **proved:** fixture (3.5 FAIL at the pin)

## PL-19: `doOnFinish` runs its commands synchronously on the interface thread, inside the joystick lock on a hot-plug write

- **Severity:** Low; **category:** Locks; **question:** Q3
- **Source finding:** L-08, 3.13
- **Lines at the pin:** `InputManager.cpp:1272`, `:485-623`, `:605`
- **Owner:** upstream's; recorded
- **What is wrong:** A slow `onfinish` command freezes the interface; reached from the rebuild it runs with `mJoysticksLock` held.
- **Proposed disposition:** recorded; G-01 counts the shipped `inputAction` lines
- **proved:** tree

## PL-20: Two names for the hotkey

- **Severity:** Low; **category:** Input; **question:** Q2
- **Source finding:** L-09, 3.12
- **Lines at the pin:** `InputManager.cpp:1105-1107`; `guis/GuiInputConfig.cpp:73`, `:273`, `:279`
- **Owner:** T3 (the templates)
- **What is wrong:** The SDL-mapping fallback writes `hotkey`, the configuration page `hotkeyenable`.
- **Proposed disposition:** recorded for T3
- **proved:** tree

## PL-21: Four keyboard debug chords run with their gate commented out

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-05
- **Lines at the pin:** `Window.cpp:262-281`
- **Owner:** upstream's (outside the lanes)
- **What is wrong:** Ctrl+G/T/I/M change the screen with no setting.
- **Proposed disposition:** recorded (D-UI-079)
- **proved:** tree

## PL-22: es-core reaches into es-app, and four detached workers capture the window

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-04
- **Lines at the pin:** `Window.cpp:29`, `:1554-1637`
- **Owner:** upstream ROCKNIX's (outside the lanes)
- **What is wrong:** `#include "../es-app/src/ApiSystem.h"`; `processStorageRequest`'s workers capture `this` and post back; nothing joins them.
- **Proposed disposition:** recorded (D-UI-079); `Window.cpp:29`'s disposition
- **proved:** tree

## PL-23: A rule sentence still calls the card top-right

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-22
- **Lines at the pin:** `.claude/rules/es-native-ui.md:30` against `Window.cpp:1192`
- **Owner:** the coordinator's sweep
- **What is wrong:** The card is centred at the pin, and the same rule says so at `:191-197`.
- **Proposed disposition:** the coordinator's sweep (`tools/archaeology --reversal`)
- **proved:** tree

## PL-24: A dialog speaks its text twice

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-16, 3.20
- **Lines at the pin:** `guis/GuiMsgBox.cpp:44`, `:234`, `:240`
- **Owner:** upstream's
- **What is wrong:** Three `say(` calls in the constructor (TTS compiled out on the image).
- **Proposed disposition:** recorded
- **proved:** tree

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | **Open** | the stage-D pause disposes it |
| PL-02 | **Open** | the stage-D pause disposes it |
| PL-03 | **Open** | the stage-D pause disposes it |
| PL-04 | **Open** | the stage-D pause disposes it |
| PL-05 | **Open** | the stage-D pause disposes it |
| PL-06 | **Open** | the stage-D pause disposes it |
| PL-07 | **Open** | the stage-D pause disposes it |
| PL-08 | **Open** | the stage-D pause disposes it |
| PL-09 | **Open** | the stage-D pause disposes it |
| PL-10 | **Open** | the stage-D pause disposes it |
| PL-11 | **Open** | the stage-D pause disposes it |
| PL-12 | **Open** | the stage-D pause disposes it |
| PL-13 | **Open** | the stage-D pause disposes it |
| PL-14 | **Open** | the stage-D pause disposes it |
| PL-15 | **Open** | the stage-D pause disposes it |
| PL-16 | **Open** | the stage-D pause disposes it |
| PL-17 | **Open** | the stage-D pause disposes it |
| PL-18 | **Open** | the stage-D pause disposes it |
| PL-19 | **Open** | the stage-D pause disposes it |
| PL-20 | **Open** | the stage-D pause disposes it |
| PL-21 | **Open** | the stage-D pause disposes it |
| PL-22 | **Open** | the stage-D pause disposes it |
| PL-23 | **Open** | the stage-D pause disposes it |
| PL-24 | **Open** | the stage-D pause disposes it |

## punch_index

```yaml
punch_index:
- id: PL-01
  severity: "Medium"
  category: Locks
  question: Q3
  source_finding: "L-11, 3.1, #1283's es-core half"
  outcome: "open"
- id: PL-02
  severity: "Medium"
  category: Surfaces
  question: Q1
  source_finding: "L-01, 3.14"
  outcome: "open"
- id: PL-03
  severity: "Medium"
  category: Scripts
  question: Q5
  source_finding: "L-18, 3.4, T2 FD-9/FD-19"
  outcome: "open"
- id: PL-04
  severity: "Medium"
  category: Input
  question: Q2
  source_finding: "L-07, 3.11"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: Lifetimes
  question: Q4
  source_finding: "L-27, 3.27, #1305"
  outcome: "open"
- id: PL-06
  severity: "Medium"
  category: Lifetimes
  question: Q4
  source_finding: "L-02, T2 PC-1"
  outcome: "open"
- id: PL-07
  severity: "Low"
  category: Lifetimes
  question: Q4
  source_finding: "L-03, 3.17"
  outcome: "open"
- id: PL-08
  severity: "Low"
  category: Input
  question: Q2
  source_finding: "L-06"
  outcome: "open"
- id: PL-09
  severity: "Low"
  category: Input
  question: Q2
  source_finding: "L-10, 3.10"
  outcome: "open"
- id: PL-10
  severity: "Low"
  category: Input
  question: Q2
  source_finding: "L-24"
  outcome: "open"
- id: PL-11
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-13, 3.19, T34 PL-16"
  outcome: "open"
- id: PL-12
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-14"
  outcome: "open"
- id: PL-13
  severity: "Low"
  category: Surfaces
  question: Q1
  source_finding: "L-01, 3.14 (second case)"
  outcome: "open"
- id: PL-14
  severity: "Low"
  category: Surfaces
  question: Q1
  source_finding: "F-ES-24, brief § 9"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-12, 3.18"
  outcome: "open"
- id: PL-16
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-17, 3.21"
  outcome: "open"
- id: PL-17
  severity: "Low"
  category: Scripts
  question: Q5
  source_finding: "L-18"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Scripts
  question: Q5
  source_finding: "L-18, 3.5"
  outcome: "open"
- id: PL-19
  severity: "Low"
  category: Locks
  question: Q3
  source_finding: "L-08, 3.13"
  outcome: "open"
- id: PL-20
  severity: "Low"
  category: Input
  question: Q2
  source_finding: "L-09, 3.12"
  outcome: "open"
- id: PL-21
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-05"
  outcome: "open"
- id: PL-22
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-04"
  outcome: "open"
- id: PL-23
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-22"
  outcome: "open"
- id: PL-24
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-16, 3.20"
  outcome: "open"
```


## The brief's § 4, the questions

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of the families the earlier ES briefs
used -- **a layout computed from what it last produced or from a moving
number**, **a house constant a surface does not keep**, **a prompt offered
where the key moves nothing**, **a lifetime or a thread**, **a read of a
file another process writes**, **a player sentence outside the vocabulary
or without its French**, **a structure or merge-debt fact** -- with the
lens, cost against value, asked of every upstream surface: what it costs
the player (a frame's work, a wait, a thread) against what it gives. The
leads are § 2's L-01 to L-27, cited here by number (their lines are the
table's and are not restated), and the floor's pure leads tabled at the end
of this section; each is read at its lines before it is called anything,
and the candidates marked FAIL-at-pin (§ 5) get their `git log -S` first
(`engineering-practices.md:83`); the upstream surfaces outside the lanes are
§ 1's list, read and recorded, fixed only under rule 6 (D-UI-079). For
this slice the natural homes (R3 § 5): the toast queue and the posted
functions under one lock, the watchers' lock and the detached storage
threads are *a lifetime or a thread*; the config file's in-place write and
the cached `exists` are *a read of a file another process writes*; the
second `BUTTON_GRID_HORIZ_PADDING` and the card's re-applied position are *a
house constant a surface does not keep*; the dialog's accelerator and the
help bar under a second page are *a prompt offered where the key moves
nothing*; the 86 `_("` lines and `GAMEPAD %i` are *a player sentence*;
`Window.cpp:29` and T21's CMake hunk are *a structure fact*.

- **Q1 The window's queue and its surfaces: one floating surface at a
  time** (`es-native-ui.md:144`, `:189-194`, `:207-222`;
  `es-player-text.md:135`, `:264`; D-UI-093, D-UI-105, D-UI-106, D-UI-109;
  the surfaces run). **L-01**: 3.14's extract seen to FAIL at the pin if
  two toasts queued under a card drain newest first (`back()`/`pop_back()`
  `:339-340`) against the comment's *"the order is the order things
  happened"* (`:334-335`) and D-UI-109's *"the order is the order things
  happened"*; the `git log -S 'pop_back'` of `c1c0d6ddc` first (the
  re-queue loop at `:1159-1166` pushes in popup order *because* the queue
  is LIFO, so a FIFO fix changes both); the contained fix a `front()`/`erase(begin())`
  with the re-queue loop reversed, or a record that the order is by
  design, ruled at the pause; a re-queued toast's **fresh default duration**
  `:1164` read against what the player was shown (a toast half-read then
  re-shown whole is defensible; said in `02`). **Item 14 / F-ES-24**: every
  toast is held while *any* card is up `:336-337`, the hasher's
  minutes-long card included (D-UI-079 keeps that card as upstream has
  it): the 2026-09-25 audit recorded it Low with no `04`/`05` line (R4
  item 14's `0`); this slice says whether it stands or is a bug, and the
  pause rules (a toast behind a long card is the one surface D-UI-093 and
  D-UI-078 together did not decide). **Item 13**: `:1183`, `:1192` read
  against `AsyncNotificationComponent.cpp:64`, `:112` (T34's): the 0.9 W
  centred position re-applied every frame, `:1192`, `:1205`, `:1221`,
  `:1224` the re-applications; G-02 measures the edges. **Item 15**:
  `GuiInfoPopup.cpp:17-18`, `:27-39`, `:47-50`, `:90-111`: the cap, the
  ellipsis, the fade (3.22); the words are the pages'. `notificationDuration`
  `:298-309` (3.15): the `audio.display_titles_time` setting's bounds.
  **L-22**: `es-native-ui.md:30`'s "top-right" against `:1192` -- a stale
  sentence for the coordinator's sweep (`tools/archaeology --reversal
  'top-right'`), not the lane's edit; recorded in `02` § The structure.
  A table: the queue's two containers and the lock, every enqueue, dequeue,
  layout and free (`:311`, `:324`, `:353`, `:365`, `:396`, `:418`, `:1152`,
  `:1177`, `:1236`), with the invariant each keeps and the frame that
  shows it.
- **Q2 The input's writes and the `<command>` execution**
  (`es-code-traps.md:127`; `upgrade-and-install.md:40`, `:58`; D-CLOUD-078;
  `handheld-evidence.md`; the input run). **L-06**: `es_input.cfg` and
  `es_last_input.cfg` written in place by `save_file` `:1225`, `:1232`
  while `AtomicFile::writeText` (`utils/AtomicFileUtil.h:42`, T21's) is
  registered in this slice's own CMake and called **zero** times in the 96
  (R2 cmd 13); a kill between the open and the write leaves a truncated
  mapping file -- the family of #102; the contained fix (`writeText` of
  pugixml's `save` to a string, or temp-and-rename) is put to the pause
  with T21 named for the API; **`Already written:`** is argued here, not
  assumed: a device with a half-written `es_input.cfg` today reads it as a
  parse error logged at `:1191-1194` and configures from scratch, which
  the fix does not change. **L-07**: 3.11's case with the real
  `FileSystemUtil.cpp` (T36's; T34's 3.21 shape): the miss at `:893`/`:1187`
  cached for the session, the file written at `:1225`, a second pad's
  `writeDeviceConfig` reading `exists` false and replacing the file with
  itself; seen to FAIL or PASS at the pin, the cache's erase cited from
  T36's rows (T34's brief names `FileSystemUtil.cpp:144`, `:185-195`,
  `:203-220`); a FAIL is a `bug` whose VM line is a unit case, since the
  guest has one keyboard device and no second pad (G-10's `CANNOT`).
  **L-08**: `doOnFinish` `:1242-1284` runs every `<inputAction
  type="onfinish">` `<command>` from `es_input.cfg` **synchronously on the
  UI thread** through `ProcessStartInfo(tocall).run()` `:1272` (3.13):
  what the distribution's `es_input.cfg` carries there (the lane greps
  `inputAction` in `projects/` and `packages/` -- a read, not a change),
  how long it holds the screen, and that a player's own edit of the file
  is an arbitrary command run by the interface: cost against value, and
  the quoting of its argument is Q5's executor. **L-09**: `hotkey` (the SDL
  fallback, `:1101-1108`) against `hotkeyenable` (the configuration page,
  `GuiInputConfig.cpp:73`, `:270-281`; `InputConfig.cpp:186-189`
  lower-cases): 3.12 documents both; which name the launch scripts read is
  T3's (`functions:128`), named for the pause, never read here as a defect
  of these lines alone. **L-10**: 3.10's extract: the two "Approximative
  device found" lines `:946`, `:960` print empty attributes (pugi's null
  node is safe); a one-line reorder under rule 6, a #585 line. **L-20**:
  `configureEmulators`'s blob (T2 FD-6/FD-7; the call `FileData.cpp:547`,
  T2's): the device names the kernel reports spliced inside the template's
  double quotes -- a name with `"`, `$` or a backtick breaks or expands the
  line; rule 6 on the blob's side (quote or reject the name), T3's on the
  template's; the cost of running it when `includeControllers == false` is
  priced (Q7). **Item 23 / #54**: `deinit` `:153-196` closes every joystick
  and `SDL_QuitSubSystem` `:188-189`; `Window::deinit` `:199-200` calls it
  when `deinitRenderer`; the sign-in window's grab is T18's lane, the
  handover named. **Item 24**: `buttonLabel` `:353-366` returns the key
  unchanged (3.8): the contract stated for T34's fix at
  `ComponentList.cpp:568`. **The hot-plug rebuild** `:374-630`:
  `mJoysticksLock` held `:485-623` while every joystick is opened and its
  config loaded, `writeDeviceConfig` called from inside it `:605` under
  `#if !defined(BATOCERA) || !defined(ROCKNIX)` `:585` (the lane states
  which branch the image compiles: `-DROCKNIX` is `CMakeLists.txt:132`'s,
  R3 § 3.2); `SDL_JOYDEVICEADDED` rebuilds then toasts, `REMOVED` toasts
  then rebuilds (`:849-877`): a frame's work on every hot-plug, priced. A
  table: every write site (R2 § 2.2's seven), its mechanism, atomic or
  not, the reader of what it writes and what a truncated file reads as;
  every `exists(` of the input files with its writer.
- **Q3 `WatchersManager`'s lock** (`handheld-evidence.md` § The
  hang-to-reboot path; `engineering-practices.md:111`; D-UI-078;
  #1283, #1276; the locks run). **L-11**: `run()` `:159-203` holds
  `mWatchersLock` `:181` across `item->component->check()` `:196`, so
  `GetComponent<T>()` (`.h:35`), `RegisterComponent` `:66`,
  `UnregisterComponent` `:78`, `ResetComponent` `:92-104` and the
  destructor `:143` -- every one called from the UI thread -- wait for a
  network or battery probe to return (T33 PL-14's es-core half; the
  callers `NetworkThread.cpp:58`, `:87-95`, T33's, and
  `GuiRetroAchievementsSettings.cpp:805-806`, R4 § 2); 3.1's case (a
  watcher whose `check()` sleeps; `ResetComponent` from a second thread
  measured to return only after it) seen to FAIL at the pin; the fix
  **named by T33 and shaped here under rule 6**: `check()` outside the
  lock with the `WatcherInfo`'s lifetime kept (EP-13: `UnregisterComponent`
  `:85-86` deletes it; a snapshot of due items under the lock, the
  `check()`s outside, a re-validation before `nextCheckTime` is written),
  `NotifyComponentChanged` `:197` still under `mNotificationLock` `:128`
  (lock order `mWatchersLock` -> `mNotificationLock`, never reversed by the
  fix); #1283's checkbox at its body line 18 waits for this slice's
  line-cited read of the fixed file in `stage-e/`. **`mRunning` and
  `mPaused`** plain `bool`s (`.h:85-86`), `mRunning = false` written `:151`
  outside any lock and read `:161`, `:172`, `:187`: a data race by the
  standard; 3.3's TSan run names it; `std::atomic<bool>` is a contained
  fix. **Notifications on the watcher thread** `:130-131`: what each
  `OnWatcherChanged` does (the fork's callers are T33's; this slice states
  the contract -- a listener that touches the interface must post). **The
  thread**: `new std::thread` `:61`, `join` `:154`, `stop()` `:20-27`
  deletes the singleton: against `main.cpp:1322` (`closing()`), `:1330`
  (`WatchersManager::stop()`), `:1358` (`window.deinit()`) (R4 § 2; #1276's
  context, the fix T33's S4a). **`pause`/`resume`** `:29-53` on the launch
  path (L-19): `mThreadLock` taken; priced with Q7. A table: every lock,
  every acquisition site with the thread that takes it and what it holds
  across, the lock order, and the UI-thread entry points that block.
- **Q4 Lifetimes: the window's teardown, its posted functions, its
  detached workers, and #1305** (`es-code-traps.md:22`, `:191`;
  `es-native-ui.md:358`; D-UI-078, D-UI-093; the lifetimes run).
  **L-02 / item 3 (T2 PC-1)**: `deinit` `:188-207` and `~Window` `:49-63`
  never free a card or a popup and leave the queue; the one free is
  `updateAsyncNotifications` `:1246-1248` when `isRunning()` goes false; a
  card alive at `deinit` is still in the vector at the next `init()`
  `:115-174` and drawn again; the raw holders are es-app's (R2 § 1.4's
  thirteen lines: `ContentInstaller.h:45`, `ProxyCards.cpp` x7,
  `ThreadedBluetooth.h:20`, `:43`, `ThreadedCloudSync.h:191`,
  `ThreadedHasher.h:50`, `GuiUpdate.h:59`) -- this slice states the
  teardown order against `main.cpp:1358` and what a holder may assume
  after it; T34 reads the card's half (its Q4, § 1 b) and files the `bug`
  if the window is proved, naming T18 and T20 for the callers; a
  contained fix (the cards freed in `deinit`, or a `close()` the component
  refuses after the window is gone) is the pause's. **L-03 / item 4 (T34
  L-12)**: `unregisterPostedFunctions` `:1262-1274` iterates and erases
  `mFunctions` **without** `mNotificationMessagesLock`, which
  `postToUiThread` `:1278` and `processPostedFunctions` `:1296` take;
  3.17's TSan extract names the race; the contract `postToUiThread`
  promises a poster that dies before the drain (nothing: the `void*` owner
  token and `unregisterPostedFunctions` are the poster's to call, and the
  fakes' `Window.h` runs posts at once, so no test at the pin exercises
  the queue) is written into `02`; T34's weak-token fix is put to the
  pause with T33's `AppWindow` gate (#1276, item 5) named. **L-04**: the
  four `std::thread(...).detach()` in `processStorageRequest`
  `:1554-1563`, `:1572-1575`, `:1608-1619`, `:1634-1637` capture `this`
  and call `ApiSystem` (es-core including es-app, `:29`, item 16): a read
  trace of what each touches on the interface thread after it finishes
  (its `GuiMsgBox` `:1558`, `:1614`, `:1623-1625`, `:1630-1640` posted or
  direct), upstream ROCKNIX's and outside the lanes -- recorded, a #585
  candidate only if a thread touches the window directly. **L-27 / #1305
  (T33 PL-25)**: the window's half of a three-sided fix -- `:777-779`
  starts the screensaver on `mTimeSinceLastInput` alone, so a slideshow
  can start while `GuiCloudTransfer` owns the screen; `cancelScreenSaver`
  `:1107-1138` (`resetCounts` `:1117`) is the only path that clears the
  screensaver's list; nothing in `removeGui` `:82-105` or in a rescan
  reaches the screensaver; T33's `stage-c/pl25-screensaver.py` FAILs at
  the pin with a heap-use-after-free in `selectGameMedia` (3.27, re-run
  unchanged); the rescan's half is T2's (`SystemData.cpp:459-473`), the
  list's own is T33's (`SystemScreenSaver.cpp:342-358`); the pause decides
  which half carries the fix (a window that holds the screensaver off
  while a page that owns the screen is top; a `resetCounts` on rescan; or
  the list's own clear), each named for its owner. **Item 9**:
  `deleteMeAndCall` `:286-294` copies the callback, `delete this`, then
  calls it -- the invariant T26's and T31's pages rest on; stated and kept.
  **Item 17 / #1212**: `:542-543` updates and `:287-288` feeds only the
  top page -- the invariant a T21 bug's "no wrong outcome" rests on;
  stated. **Item 30**: T32's `/quit` and `/messagebox` routes
  (`services/HttpServerThread.cpp:219`, `:545`) post their `GuiMsgBox`
  through `mWindow->postToUiThread` (`:229`, `:559`), so the constructor
  (fonts, the theme, `Renderer::getScreenWidth()` `:21-23`, `:53`) runs on
  the interface thread; recorded, no line for T32 (the proof).
  **L-24**: F4's `new SDL_Event()` never freed `:795`: one event per press,
  recorded (rule 6 if the pause wants it; a #585 line). A table: every
  `std::thread` (R2 cmd 10's 18 lines), every `.detach(` (4, all
  `Window.cpp`), every `delete this` in the slice (17 lines, the proof's grep:
  `GuiDetectDevice.cpp:99`, `:132`, `:145`; `GuiInputConfig.cpp:262`,
  `:288`; `GuiMsgBox.cpp:289`; `GuiTextEditPopup.cpp:33-35`, `:74`;
  `GuiTextEditPopupKeyboard.cpp:346`, `:352`, `:359`, `:395`, `:477`,
  `:494`, `:499`), every `postToUiThread` and its owner
  token, every raw pointer the window hands out (`createAsyncNotificationComponent`
  `:1169`) or holds (`mScreenSaver` `.h:147`, `mHelp`), who joins or frees
  it, what it touches on the interface thread.
- **Q5 `Scripting`'s quoting, and what runs the shell** (`es-native-ui.md:117`;
  `engineering-practices.md:111`; T2 FD-9/FD-19; #1192's second half;
  the scripts run). **L-18**: `executeScript` `:88-149` quotes the script
  path only when it has a space `:92-93`, strips `"` from every argument
  and quotes an argument only when it contains a space `:98-113`, no other
  escaping: 3.4's case with a `ProcessStartInfo` double shows `a$(id)b.zip`
  reaching the command string bare; the precondition is a player's own
  script in `scripts/<event>/` (the distribution ships none -- the lane
  greps `projects/` and `packages/` for `scripts/game-start` and records
  the count), so the class is a `bug` under rule 6 with a contained fix
  (`shellQuote` on every argument -- the tree's form is `FileData.cpp:1148-1151`,
  T2's; or an argv executor, #1192's second half, which is the better fix
  and the pause's call) and a #585 line. **L-18's second half**: on the
  device **every file** in a per-event directory runs (`:169-178`; the
  extension filter `:172-176` is WIN32-only), fire-and-forget except
  `quit` (`:142`), stdout/stderr to `es_script_stdout.log`/`es_script_stderr.log`
  `:145-146`; 3.5's case; a `.txt` left in the directory is executed by
  `sh` -- cost against value, recorded; the single-script pass `:182-207`
  filters to `.exe .cmd .bat .ps1 .sh .py` `:151` and passes the event
  name first `:205` (3.6). **L-19**: `fireEvent("game-start")` scans three
  per-event and three single-script directories on every launch, empty or
  not, the directory's `exists` cached `:193`: priced in Q7. **Item 20**:
  the fork's `maskSecrets` on the three WIN32-branch lines `:49`, `:122`,
  `:129`; the Linux branch `:138` logs the path only -- so the mask's reach
  on the image is nil and the 2026-09-24 audit's gap (*"a negative over
  the"* sweep) is answered here: the Linux log line carries no argument,
  the WIN32 lines are masked, the `LogDebug` at `:155` prints **the raw
  args** -- read whether a ROM path or a scraped name can carry a value
  (it cannot; a name is a name) and record it. **Q2's `<command>`**
  (`InputManager.cpp:1272`) shares the executor and is read with it. A
  table: the four `ProcessStartInfo` sites (R2 cmd 11), each with what
  builds its string, which parts are quoted, which thread runs it and
  whether it waits.
- **Q6 The popups' accelerator and padding, the help bar, and the words**
  (`es-ui-style-guide.md:169-178`, `:232`, `:296-304`; `es-code-traps.md:79-88`,
  `:134-136`; `es-native-ui.md:121`, `:179-183`; `es-player-text.md:29`,
  `:141`; D-UI-021, D-UI-034, D-UI-051, D-WORKFLOW-144; the input and
  strings runs). **L-12 / item 8**: the accelerator `:116-134` as the
  source has it (the only button; else the first named `OK` or `NO`; else
  **the last**), fired by an unconfigured keyboard's RETURN/ESC/SPACE
  `:249-254`, `BUTTON_BACK`, or **any `TYPE_BUTTON` from an unconfigured
  pad** `:257-261` -- a pad not yet configured presses *whatever is last*
  on any dialog it meets; 3.18's text lift states the three branches;
  G-04 and G-05 show the two outcomes; whether the fall-through stays in
  the component (T26 L-22's TRY AGAIN / CANCEL SIGN-IN lands on CANCEL
  SIGN-IN) is a style call for the pause, the component's half this
  slice's. **L-13 / item 6**: `GuiTextEditPopupKeyboard.cpp:14`'s
  `BUTTON_GRID_HORIZ_PADDING` at 0.0052083333 against `MenuComponent.cpp:14`'s
  0.022 (T34's) -- same macro name, two values, two files (3.19); the
  popup's per-key gap at 640 is 3.3 px against the bar's 14; the pause
  rules delete-and-widen (the key grid would grow 4.2x, R4 item 6) or keep
  the popup's own gap under its own name and correct T34's comment;
  recorded, not deleted here (`engineering-practices.md:576`); G-06's
  frame measures it. **L-14**: `x` on the keyboard `:392-397` and the CLEAR
  button `:491-496` commit `""` and delete the popup with no confirmation
  -- one press empties a cloud folder path, a hostname or a Wi-Fi key and
  submits it; `es-ui-style-guide.md:171` (a consequential action asks) and
  `least-surprise.md`: a `bug` candidate if G-06 shows the row's value
  gone after one `s`; the fix (CLEAR empties the field and leaves the
  popup open; or a YES/NO) is the pause's, with its French (D-UI-051).
  **L-15 / item 7 (#1192)**: neither popup class takes a masking mode
  (`.h:15-16`, `.h:13-14`); the field under them is `TextEditComponent`
  (T34's); the Backlog is the coordinator's, the lane states where the
  mode belongs. **L-16**: `TextToSpeech::say` three times in one constructor -- `:44` and
  `:234` say the text, `:240` the focused button's label (3.20): the second
  `say(text)` is a one-line fix under rule 6, a #585 line. **L-17**:
  `GAMEPAD %i` with `getDeviceId() + 1` `GuiInputConfig.cpp:134` -- the
  SDL instance id, not the player's seat (3.21): a player sentence that
  misleads; the fix (the player number from `computePlayersConfigs`, or
  the device name) is the pause's. **L-21 / items 10, 11, 12**: the help
  bar -- `:743-745` draws it only when `mGuiStack.size() < 2 ||
  !fullScreenMenus()`, `renderHelpPromptsEarly` `:999-1003` the hook a
  non-`MenuComponent` page uses (the save state manager, #149);
  `setHelpPrompts` `:1005-1078` merges and sorts (3.16); `GuiMsgBox::getHelpPrompts`
  `:296-299` delegates to `ComponentGrid` (T34's `canMoveCursor`, D-UI-034);
  the eight `mHelp->` lines (`:745`, `:1001`, `:1009`, `:1011`, `:1012`,
  `:1077`, `:1397`, `:1398`) call no `setOpacity`, so batocera's `9dbd4b9bf`
  guard has no caller here -- the callers' read is T34's for this slice
  (its § 5 item 3), taken up for the eight lines under D-WORKFLOW-162;
  G-04 and G-11 read which pages show a bar at 640 and 1280. **L-28 / T34 PL-05 (#1307, inherited)**: on the image at 1280x800 the
  tabbed SCRAPEUR page's help bar carried only FERMER and RETOUR, no SWITCH
  TAB and no row prompt, pixel-identical with a row or the strip focused;
  T34's seat traced SWITCH TAB through the pin's components
  (`ComponentTab.cpp:341`, `ComponentGrid.cpp:493`, `:522-552`,
  `MenuComponent.cpp:533`), so the empty bar is the window's bar collection
  (`setHelpPrompts` `:1005-1078`, the gate `:743-745`) or the image's
  composition: 3.16's extract over `setHelpPrompts` with a tabbed page's
  prompt list, and G-11's frame of a tabbed page's bar at 1280x800, say
  which -- the window's half is this slice's, the components' T34's. **L-29
  / T34 PL-04 / D-UI-133 (#1307, inherited)**: at 1280x800 the list's
  CHOISIR prompt drew its icon with 0 `Unknown help icon` lines in
  `es_log.txt` though the catalog carries `haut/bas` for `up/down` (po
  `:3708-3709`, T34's proof); why the window's bar did not show the
  component's `_()`-wrapped key (`ComponentList.cpp:568`, T34's fix site) is
  this slice's read: what `setHelpPrompts` `:1031-1041` does to a key it
  does not know (merged by icon, dropped, or passed through), stated for
  T34's fix. **Item 28**: `Window::input` `:215-290` hands a key to
  `peekGui()` alone `:287-288`
  after the `FirstJoystickOnly` filter `:220-232` and the screensaver block
  `:234-260`; `GuiComponent::input` `:54-63` iterates children with a
  saved `next_it`: the window's half of D-UI-021 stated, the strip T34's,
  the pages T31's. **The words**: the 86 `_("` lines (R2 cmd 8) against the
  catalog (item 7 of § 3; the parser run is the figure), the fork's own
  (`CLEAR` x3, the `Window.cpp` card lines) read for the four tiers and the
  two verbs (`es-player-text.md` § Conventions), `GuiDetectDevice.cpp:52`
  (HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT., with its period; po
  `:3779`) and `GuiInputConfig`'s 14
  prompts in both languages on the guest (G-07, G-08); `processStorageRequest`'s
  sentence-case dialogs `:1547-1548`, `:1601-1602` recorded as upstream's
  dialect (D-UI-079); the non-ASCII lines (the proof, `LC_ALL=C`): 28 lines in four files -- the
  keyboard's 22 glyph literals (`GuiTextEditPopupKeyboard.cpp:169-192`,
  which `es-code-traps.md:60` allows) and six upstream **comment** lines,
  `AudioManager.cpp:352`, `:362`, `:383`, `GunManager.cpp:145`,
  `InputManager.cpp:393`, `:1437` -- none on a line the fork added (its
  `-U0` diff against `cada856d86` adds 0), recorded and not fixed as
  `es-code-traps.md:60` says of an upstream hit; `InputManager.cpp:856`,
  `:869` are plain ASCII. A table: every `getHelpPrompts` and
  `input()` in the slice with the condition under which it offers or
  consumes a key; every `_("` line with its msgid and its French.
- **Q7 Cost against value, the structure and the merge debt**
  (`time-to-play.md`; `engineering-practices.md:12`, `:28`, `:576`;
  `es-code-traps.md:60`; D-UI-079, D-WORKFLOW-162, D-WORKFLOW-209; the
  membership, scope, delta, includes and non-ASCII runs). **The lens, asked
  of every upstream surface in § 1's list**: **L-05** the four
  keyboard-only Ctrl debug toggles `:262-281` with the `"Debug"` gate
  commented out -- a chord on an attached keyboard changes the screen with
  no setting; what each costs (a texture-debug overlay drawn every frame)
  against what it gives on a handheld (nothing: no keyboard); a `bug`
  candidate under rule 6 (the gate restored) or recorded, the pause's.
  **L-19** the six directory scans and `WatchersManager::pause` on every
  launch, priced from `docs/vm-qa-log.md`'s launch number and a
  `strace -c`-free read (the guest cannot time one `fireEvent`; `CANNOT`
  with that reason is allowed), **L-20**'s `configureEmulators` on every
  command build (T2 FD-6: *"small beside the launch"*), **L-23**
  `ThemeData::loadFile` throws on five conditions `:752-829` while
  `parseInclude` only warns on four `:1120-1146`, `getDefault` catches to
  `LogError` `:2246-2262` and `appendFile` to `LogWarning` `:2779-2798`: a
  broken include is a silent fallback, a broken root a logged one;
  upstream's parser, read for brittleness and recorded (no fork hunk, 25
  `LOG(Log` lines), `ThemeFileCache` `:719-743` under its mutex; **item
  27** `:267`'s `{ "multiLine", STRING }` entry read for T34's tile; the
  gun manager's `poll(..., 0)` every `updateGuns` `:922-930` and six
  `ioctl`s per gun `:978-991` on a device with no gun (the udev monitor
  idle); `VolumeControl`'s thread `:32`, `:203` and 32 `LOG` lines, the
  most in the slice; `FavoriteMusicManager.cpp:115`'s truncate-then-write
  (3.24, L-06's family, recorded); the on-screen keyboard's three layouts
  chosen from `system.language` `:141-152`. **The structure**: `Window.cpp:29`'s
  `#include "../es-app/src/ApiSystem.h"` (item 16, L-04) -- the one
  es-core to es-app include in the 96, resolving through `-I es-core/src`
  plus `../`, recorded with T34's disposition of its sibling; the include
  reach (R3 § 2.2: 18 SDL angle lines over the 101, 2 quoted `"SDL_mixer.h"`,
  51 non-standard angle includes with their guards -- `<libudev.h>` x3
  under `HAVE_UDEV`, `<pulse/pulseaudio.h>` under `_ENABLE_PULSE_` which
  the image takes (`package.mk:23`), `<libcec/*>` and `<espeak/*>` off);
  **whether `UDEV_FOUND` holds in the image build is `[unverified]`** (R3 §
  2.2: `package.mk:13` names no udev package; the proof found no
  `CMakeCache.txt` of an EmulationStation build under any
  `*/build.*/build/emulationstation-*/` on this host and M7's roots are
  never read, so the read that settles it is G-01's `ldd
  /usr/bin/emulationstation | grep -c udev` on the guest, `image` side --
  `CANNOT` until then); every
  T35 source named once and unconditionally in `es-core/CMakeLists.txt`
  (R3 cmd 21: `:147-171`, `if(` at `:278`, `:287`); **L-26** T21's
  `3ae9610b0` adds five registrations (R1 C21) -- the one lane-on-lane hunk
  inside the 96, the integration's, with `HttpText.{cpp,h}` and
  `RecoveryOutcome.h` falling to `rest` at T21's tip (§ 1 h); **L-25**
  `GuiTextEditPopupKeyboard.h`'s provenance footnote; the three `ROCKNIX` lines in the 96 (the proof's `git grep -n 'ROCKNIX'
  PIN -- <96>`): `Splash.h:10` `#if defined(ROCKNIX)`,
  `InputManager.cpp:585` `#if !defined(BATOCERA) || !defined(ROCKNIX)` and
  `Paths.cpp:76` `#if defined(ROCKNIX)` (R3 § 3.2 asked for the list). **Merge debt: none** on the 96 (§ 2's one
  line); **batocera's twelve** since `1750dded8c` on nine files, six of
  them fork-modified (R1 C17, C18; § 2), as the reconciliation list -- the
  input configs written for the launcher (`dbabd1adf`) against the fork's
  udev guards, the SIGTERM handler (`33016e55f`) and the logger build fix
  (`08ca272cb`) against the fork's per-batch flush, the `Window` and
  `GuiMsgBox` hunks against D-UI-093 and the wide box: the hunk ranges are
  the lane's `git diff 1750dded8c batocera/master -- <file>` per file,
  never a merge. **The #585 lines owed** (R4 § 5): T33's never-posted
  candidate for the lock; this slice's for the lock's fix, `Scripting`'s
  quoting, the controllers blob, the second padding constant if deleted,
  `GuiMsgBox`'s double `say`, the null-node logs, F4's leak -- each a line
  the lane writes in `02` for the coordinator to post, never sent
  (D-WORKFLOW-164/165). **The map**: no row of this slice's own; the
  checker's `SOURCE_DIRS` includes `es-core/src/guis` (§ 3 item 3), its
  per-file count quoted.

### The floor's pure leads, carried

The research ran no case (R3 § 7: *"no `-fsyntax-only` over any T35 file,
no build of any binary, no guest"*), so every row is a candidate until the
lane's stage C; the seams are in the shape `file:line at the pin | the
function | what a case would catch`, each a case in `CloudText`'s shape
(`es-code-traps.md:139`; § 5 item 1) built by the slice's binary with the
doubles R3 § 2.2 names -- the fakes' `Window.h`, `Log.h`, `LocaleES.h`
copied beside the source as `proxycards-tests` does, the test-defined
`Settings`/`Paths` bodies as `SystemConfTests.cpp` does, a
`ProcessStartInfo` double where a case must see the command string -- or
an *extract* (the function's text lifted into the case, `t33extract.py`'s
and `gpu-governor-save.py`'s shape) where the source is parse-only (R3
§ 2.2's third class: `Window.cpp`, `InputManager.cpp`, the six `guis/*`).
**The seven candidates the drafter marks FAIL-at-pin are in bold, and 3.27
is the one FAIL the research holds** (T33's record at `947ace1966`).

| # | At the pin | Function | What a case would catch |
| --- | --- | --- | --- |
| **3.1** | `watchers/WatchersManager.cpp:159-203` (`:181`, `:196`) | `run()` and `ResetComponent` `:92-104` | **a fake `IWatcher` whose `check()` sleeps 2 s; `ResetComponent` called from a second thread returns only after the sleep (L-11, #1283)**; pure, `Log.h` doubled; the fixed shape returns at once |
| 3.2 | `WatchersManager.cpp:76-90`, `:143-149`, `.h:67-73` | `UnregisterComponent`, the destructor | ASan: unregister during a running `check()`; the `WatcherInfo` freed `:86` while `:196` holds the item (EP-13); the fix's snapshot must re-validate |
| 3.3 | `WatchersManager.cpp:151`, `:161`, `:172`, `:187`, `.h:85-86` | `mRunning`, `mPaused` | TSan (`-fsanitize=thread`): the write at `:151` races the reads; `std::atomic<bool>` quiets it |
| **3.4** | `Scripting.cpp:88-149` (`:92-93`, `:98-113`) | `executeScript` with a `ProcessStartInfo` double | **`a$(id)b.zip` reaches the command string unquoted; `a b.zip` arrives quoted; a `"` inside an argument is stripped (L-18)**; the double records `tocall` |
| **3.5** | `Scripting.cpp:153-179` (`:169-178`) | `fireEvent`'s per-event pass | **a `notes.txt` placed in `<user ES>/scripts/game-start/` (a `Paths` double pointing at a temp dir) is handed to the executor on non-WIN32 (the filter `:172-176` is WIN32-only)**; the second pass `:182-207` refuses it (`:201-203`) |
| 3.6 | `Scripting.cpp:182-207` (`:151`, `:201-205`) | the single-script pass | `.sh`, `.py` run with the event name first; `.txt` skipped; a directory entry skipped `:198-199` |
| 3.7 | `InputConfig.cpp:186-189`, `:210-283`, `:285-345` | `mapInput`, `isMappedTo`, `isMappedLike`, `getMappedTo`, `loadFromXML`/`writeToXML` | `HotKeyEnable` stored as `hotkeyenable`; a hat is matched by bitmask, an axis by sign, else by id; a round trip through pugixml preserves every mapping; an unknown type is skipped with `LogError` `:297`, a value 0 warned `:305` (pugixml root, `SDL_joystick.h`/`SDL_keyboard.h` fakes, non-udev branch) |
| 3.8 | `InputConfig.cpp:353-366` | `buttonLabel` | the key returned unchanged for `up/down`, `haut/bas` and an unknown key (item 24; T34's fix is the caller's); PASS at the pin, the contract stated |
| 3.9 | `InputConfig.cpp:347-351`, `:403-414` | `AssignActionButtons` | `BUTTON_OK`/`BUTTON_BACK` swapped once under `InvertButtons`; called twice with the same setting, unchanged (idempotent) |
| **3.10** | `InputManager.cpp:889-972` (`:946`, `:960`) | `tryLoadInputConfig`'s approximate branches, extracted | **the two "Approximative device found" lines print empty `type`/`deviceGUID`/`deviceName` because `configNode` is read before `configNode = item` (L-10)**; pugixml, a `Log.h` double capturing the line |
| **3.11** | `InputManager.cpp:1179-1240` (`:1187`, `:1225`) with `utils/FileSystemUtil.cpp` (T36's) | `writeDeviceConfig`'s merge decision, extracted | **`exists(p)` miss, the file written by `save_file`, `exists(p)` again: false while the cache holds the miss (L-07; T34's 3.21 shape)** -- a second device's write then replaces the first's; PASS if the cache erases on the process's own write, cited from T36's rows |
| 3.12 | `InputManager.cpp:1004-1111` (`:1101-1108`) | `loadFromSdlMapping`, extracted | a mapping without `hotkey` gets `select` copied to `hotkey`; the configuration page writes `hotkeyenable` (L-09): the two names documented, no verdict |
| 3.13 | `InputManager.cpp:1242-1284` (`:1262`, `:1272`, `:1277`) | `doOnFinish`, extracted, with the `ProcessStartInfo` double | every `<inputAction type="onfinish">` `<command>` text handed to the executor as given, synchronously; a non-zero exit is a `LogWarning` (L-08) |
| **3.14** | `Window.cpp:324-351` (`:339-340`), `:1152-1175` (`:1164`) | `processNotificationMessages` and the re-queue, extracted | **queue [A, B] with a card up: nothing shown; card gone: B shown, then A (LIFO, L-01)**; a toast re-queued under a card returns with `notificationDuration(-1)`, not its remainder |
| 3.15 | `Window.cpp:298-309` | `notificationDuration` with a `Settings` double | `<= 0` -> `audio.display_titles_time` x 1000 when 2 < s <= 120, else 10,000; a positive value passed through |
| 3.16 | `Window.cpp:1005-1078` | `setHelpPrompts`, extracted | de-duplication by icon; `up/down` + `left/right` -> `up/down/left/right` `:1031-1041`; the sort dpad -> OK, x, y, l, r, BACK -> start/select `:1050-1075` |
| 3.17 | `Window.cpp:1262-1274` against `:1276-1290`, `:1292-1307` | `unregisterPostedFunctions` | TSan over an extract: unregister on one thread while `postToUiThread` runs on another (L-03); the fix takes the lock |
| 3.18 | `guis/GuiMsgBox.cpp:116-134`, `:246-264` | the back-button accelerator, lifted as text | the three branches present in the text (one button; `OK`/`NO`; the last); the behaviour is G-04's and G-05's (L-12) |
| **3.19** | `guis/GuiTextEditPopupKeyboard.cpp:14` against `components/MenuComponent.cpp:14` | the two `#define BUTTON_GRID_HORIZ_PADDING` | **a grep-shaped case: the macro defined in two files of the pin with the factors `0.0052083333` and `0.022` (L-13)**; the fix leaves one definition or two names |
| 3.20 | `guis/GuiMsgBox.cpp:44`, `:234`, `:240` | `TextToSpeech::say` in the constructor | the text count of `say(` in the constructor is 3 (L-16: the text twice, the focused button once); 2 after the fix |
| 3.21 | `guis/GuiInputConfig.cpp:134` | the `GAMEPAD %i` subtitle, lifted as text | `getDeviceId() + 1` is the argument (L-17); the fix's argument is the player's seat or the name |
| 3.22 | `guis/GuiInfoPopup.cpp:88-111` (`:98`, `:103-109`) | the fade, extracted | alpha 0 at t 0, 255 at 250 ms, falling from `duration - 250`, `mRunning` false past `mDuration`; `maxWidth` 0.9 W (`:17`) |
| 3.23 | `Log.cpp:60`, `:180`, `LogPolicy.h:1-55` | `AsyncLogger` against real files (the `SDL_timer.h` fake, `Settings`/`Paths` doubles as `SystemConfTests.cpp`) | every batch reaches the file before the worker sleeps (#178); WARNING and ERROR to stderr (`LogPolicyTests.cpp` holds the header's three functions already) -- the natural first binary (R3 § 2.2) |
| 3.24 | `FavoriteMusicManager.cpp:71`, `:115` | the favourites file's append and rewrite | parse-only (`Window.h`); lifted as text: `std::ios::trunc` then the write (L-06's family); recorded |
| 3.25 | `MameNames.cpp` (`:6` pugixml), `anim/ThemeStoryboard.cpp` | the parsers | a malformed file: what is warned, what throws; pugixml root, `ResourceManager.h` parsed and its `.cpp` doubled |
| 3.26 | `ThemeData.cpp:745-856`, `:1094-1150` | `loadFile`, `parseInclude` | parse-only (13 component headers to VLC): no host case; the throw/warn asymmetry recorded (L-23) |
| **3.27** | `Window.cpp:777-779`, `:1091-1138`; `SystemScreenSaver.cpp:342-358` (T33's); `SystemData.cpp:459-473` (T2's) | T33's `stage-c/pl25-screensaver.py`, re-run unchanged from `947ace1966` | **FAIL at the pin: a heap-use-after-free in `selectGameMedia` after the transfer's rescan (#1305)**; PASS only when one of the three halves lands |


