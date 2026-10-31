"""Lift the seams' lines from the pin, verbatim, into <out>/x_<name>.inc for
T34's components-tests and sanitizer cases (#681). Each spec names its file,
its line range and the code its first and last lines must hold; a range that
no longer holds it is refused (exit 1, nothing written), so a case never runs
against lines it was not written for.
    t34-extract.py <ES worktree> <pin> <out dir>"""
import os, subprocess, sys
W, PIN, OUT = sys.argv[1:4]
C = "es-core/src/components/"
def where(f):  # a component by its name; anything else (read only, other lanes' files) by its tree path
    return f if f.startswith("es-") else C + f
SPECS = [  # name, file, first, last, the first line holds, the last line holds
 ("mlme_shares", "MultiLineMenuEntry.cpp", 72, 76, "float h = th + sh;", "setRowHeightPerc(1, sh / h);"),
 ("text_limit", "TextComponent.cpp", 488, 488, "int limit = mSize.y() - mPadding.y() - mPadding.w();", "int limit"),
 ("slider_text", "SliderComponent.cpp", 276, 299, "std::stringstream ss;", "const std::string val = ss.str();"),
 ("slider_precision", "SliderComponent.cpp", 44, 59, "int calculatePrecision(float step)", "}"),
 ("button_pad", "MenuComponent.cpp", 15, 15, "#define BUTTON_GRID_HORIZ_PADDING", "0.022"),
 ("button_width", "MenuComponent.cpp", 553, 558, "float buttonGridWidth = (float)BUTTON_GRID_HORIZ_PADDING * buttons.size();", "}"),
 ("carousel_fast", "CarouselComponent.cpp", 76, 89, "int value = mCursor;", "return value;"),
 ("ilist_scroll", "IList.h", 381, 406, "int cursor = mCursor + amt;", "}"),
 ("textlist_range", "TextListComponent.h", 262, 269, "float entrySize = getRowHeight();", "listCutoff = size();"),
 ("textlist_camera", "TextListComponent.h", 593, 607, "auto rowHeight = getRowHeight();", "mCameraOffset = 0;"),
 ("scroll_defines", "ScrollableContainer.cpp", 6, 8, "#define AUTO_SCROLL_RESET_DELAY 6000", "#define AUTO_SCROLL_SPEED 150"),
 ("scroll_update", "ScrollableContainer.cpp", 64, 104, "if(mAutoScrollSpeed != 0)", "}"),
 ("scroll_reset", "ScrollableContainer.cpp", 128, 131, "mScrollPos = Vector2f(0, 0);", "mAtEnd = false;"),
 ("help_map", "HelpComponent.cpp", 18, 33, "static const std::map<std::string, std::string> ICON_PATH_MAP", "};"),
 ("card_close", "AsyncNotificationComponent.cpp", 122, 122, "mCloseRequested.store(true, std::memory_order_release);", "mCloseRequested.store"),
 ("card_update", "AsyncNotificationComponent.cpp", 268, 283, "if (!mClosing && mCloseRequested.load(std::memory_order_acquire))", "mFadeTime += deltaTime;"),
 ("card_update_full", "AsyncNotificationComponent.cpp", 265, 314, "GuiComponent::update(deltaTime);", "setOpacity((unsigned char)alpha);"),
 ("card_choose", "AsyncNotificationComponent.cpp", 138, 147, "std::string AsyncNotificationComponent::chooseThatFits(", "}"),
 ("textedit_move", "TextEditComponent.cpp", 267, 281, "void TextEditComponent::moveCursor(int amt)", "}"),
 ("str_cursor", "es-core/src/utils/StringUtil.cpp", 278, 327, "size_t nextCursor(const std::string& _string, const size_t _cursor)", "} // moveCursor"),
 ("textedit_focuslost", "TextEditComponent.cpp", 44, 47, "mFocused = false;", "mWindow->postToUiThread([this, alive = std::weak_ptr<void>(mAlive)]() { if (alive.lock()) stopEditing(); });"),
 ("text_measure", "TextComponent.cpp", 340, 340, "mSize[1] = mFont->sizeWrappedText(", "getSize().x() - mPadding.x() - mPadding.z(), mLineSpacing).y() + mPadding.y() + mPadding.w();"),
 ("text_drawn", "TextComponent.cpp", 352, 352, "int sx = mSize.x() - mPadding.x() - mPadding.z();", "int sx"),
 ("text_marquee_len", "TextComponent.cpp", 485, 485, "mTextLength = mFont->sizeWrappedText(", "getSize().x() - mPadding.x() - mPadding.z(), mLineSpacing).y();"),
 ("list_inset_define", "ComponentList.cpp", 15, 15, "#define ROW_INSET_FRACTION 0.015625", "#define"),
 ("list_inset", "ComponentList.cpp", 495, 498, "float ComponentList::rowInset()", "}"),
 ("list_dimmed", "ComponentList.h", 25, 26, "const unsigned char DIMMED_ALPHA = 0x50;", "inline unsigned int dimmed(unsigned int color)"),
 ("list_camera", "ComponentList.cpp", 302, 322, "const float totalHeight = getTotalRowHeight();", "mCameraOffset = 0;"),
 ("image_setsize", "ImageComponent.cpp", 67, 89, "if (!mTexture)", "recalcChildrenLayout();"),
 ("image_settexture", "ImageComponent.cpp", 478, 489, "cancelPendingLoad();", "resize();"),
 ("web_resize", "WebImageComponent.cpp", 101, 112, "ImageComponent::resize();", "getParent()->onSizeChanged();"),
 ("list_prompt", "ComponentList.cpp", 571, 572, "if(addMovePrompt)", "prompts.push_back(HelpPrompt("),
 ("rating_prompts", "RatingComponent.cpp", 265, 267, "std::vector<HelpPrompt> prompts;", "return prompts;"),
 ("rating_step", "RatingComponent.cpp", 197, 199, "mValue += 1.f / NUM_RATING_STARS;", "mValue = 0.0f;"),
 ("video_prompts", "VideoComponent.cpp", 351, 352, "std::vector<HelpPrompt> ret;", "return ret;"),
 ("carousel_prompts", "CarouselComponent.cpp", 356, 367, "std::vector<HelpPrompt> prompts;", "return prompts;"),
 ("carousel_path", "CarouselComponent.cpp", 188, 202, "float startPos = mCamOffset;", "endPos = target - posMax;"),
 ("option_prompts", "OptionListComponent.h", 638, 643, "std::vector<HelpPrompt> prompts;", "return prompts;"),
 ("date_display", "DateTimeEditComponent.cpp", 254, 260, "if (mDisplayMode == DISP_RELATIVE_TO_NOW)", "return Utils::Time::timeToString(mTime, mDateFormat);"),
 ("date_step", "DateTimeEditComponent.cpp", 125, 161, "tm new_tm = mTime;", "mTime = new_tm;"),
 ("help_spacing", "HelpComponent.cpp", 12, 16, "// space between [icon] and [text] (px)", "#define ENTRY_SPACING"),
 ("help_fit", "HelpComponent.cpp", 95, 172, "float width = 0;", "mGrid->setSize(rowWidth, height);"),
 ("help_opacity", "HelpComponent.cpp", 226, 232, "GuiComponent::setOpacity(opacity);", "mGrid->getChild(i)->setOpacity(opacity);"),
 ("grid_move", "ComponentGrid.cpp", 331, 378, "assert(dir.x() || dir.y());", "return false;"),
 ("grid_canmove", "ComponentGrid.cpp", 398, 413, "if (dir.x() == 0 && dir.y() == 0)", "return false;"),
 ("grid_prompts", "ComponentGrid.cpp", 521, 552, "std::vector<HelpPrompt> prompts;", "return prompts;"),
 ("tab_prompts", "ComponentTab.cpp", 322, 344, "if(!size())", "return prompts;"),
 ("slider_set", "SliderComponent.cpp", 236, 251, "if (mValue == value)", "}"),
 ("web_url", "WebImageComponent.cpp", 14, 43, "struct url", "};"),
 ("web_key", "WebImageComponent.cpp", 50, 84, "static std::string cacheDirectory()", "}"),
 ("web_setimage", "WebImageComponent.cpp", 130, 200, "if (mRequest != nullptr)", "mLocalFile = localFile;"),
 ("web_update", "WebImageComponent.cpp", 205, 244, "ImageComponent::update(deltaTime);", "}"),
 ("web_render_req", "WebImageComponent.cpp", 264, 291, "if (mRequest == nullptr && !mUrlToLoad.empty() && !mLocalFile.empty())", "}"),
 ("img_setmem", "ImageComponent.cpp", 457, 473, "cancelPendingLoad();", "resize();"),
 ("img_cancel", "ImageComponent.cpp", 448, 452, "if (mLoadingTexture && mLoadingTexture.use_count() == 1 && !mLoadingTexture->isLoaded())", "mLoadingTextureLoaded = false;"),
 ("img_watch", "ImageComponent.cpp", 839, 855, "if (!mLoadingTextureLoaded && mLoadingTexture && mLoadingTexture->isLoaded())", "}"),
 ("img_turn_fit", "ImageComponent.cpp", 103, 109, "Vector2f textureSize = (mDisplayAspect > 0.0f && physicalSize.y() > 0.0f)", "textureSize = Vector2f(textureSize.y(), textureSize.x());"),
 ("img_turn_corners", "ImageComponent.cpp", 287, 297, "if (mDisplayRotation != 0)", "}"),
 ("img_turn_norm", "ImageComponent.cpp", 516, 516, "quarterTurns = ((quarterTurns % 4) + 4) % 4;", "quarterTurns"),
 ("grid_calcdim", "ImageGridComponent.h", 1458, 1484, "Vector2f gridDimension = (mSize + mMargin) / (mTileSize + mMargin);", "}"),
 ("grid_reset", "ImageGridComponent.h", 1399, 1451, "mVisibleTiles.clear();", "onCursorChanged(CURSOR_STOPPED);"),
 ("grid_setimage", "ImageGridComponent.h", 526, 549, "auto entry = list->findEntry(obj);", "}"),
 ("grid_select", "ImageGridComponent.h", 1140, 1169, "if (mCursor >= 0 && mCursor < mEntries.size() && mEntries[mCursor].data.tile != nullptr)", "}"),
 ("grid_callback", "ImageGridComponent.h", 1214, 1233, "auto lastCursor = mLastCursor;", "}"),
 ("sw_ctor", "SwitchComponent.cpp", 10, 24, "float height = Font::get(FONT_SIZE_MEDIUM)->getLetterHeight();", "mSize = mImage.getSize();"),
 ("sw_getvalue", "SwitchComponent.cpp", 120, 121, "if(mHasAuto && mAutoState) return \"auto\";", "return mState ?"),
 ("sw_setvalue", "SwitchComponent.cpp", 126, 137, "if(mHasAuto && statestring == \"auto\") {", "onStateChanged();"),
 ("sw_statechanged", "SwitchComponent.cpp", 169, 172, "updateImage();", "mOnChangedCallback();"),
 ("sw_updateimage", "SwitchComponent.cpp", 163, 164, "auto theme = ThemeData::getMenuTheme();", "mImage.setImage((mHasAuto && mAutoState)"),
 ("sw_press", "SwitchComponent.cpp", 54, 65, "if(mHasAuto) {", "}"),
 ("sw_setauto", "SwitchComponent.cpp", 154, 155, "mAutoState = bAuto;", "updateImage();"),
 ("menu_titleimage", "MenuComponent.cpp", 292, 340, "if (titleImage == nullptr)", "updateSize();"),
 ("menu_fit", "MenuComponent.cpp", 415, 428, "if(height > maxHeight)", "}"),
 ("list_updatetype", "ComponentList.h", 157, 157, "ComponentListFlags::UpdateType mUpdateType", "mUpdateType"),
 ("tile_selected", "GridTileComponent.h", 313, 313, "bool mSelected", "mSelected"),
 ("tile_autoscroll", "GridTileComponent.h", 135, 135, "bool autoScroll", "autoScroll"),
 ("tile_textprops", "GridTileComponent.h", 79, 90, "Loaded = false;", "autoScroll = false;"),
 ("tile_ctor_select", "GridTileComponent.cpp", 49, 49, "setSelected(false", "setSelected(false"),
 ("card_handle", "AsyncNotificationComponent.h", 53, 54, "using Handle = std::weak_ptr<AsyncNotificationComponent>;", "Handle handle() { return weak_from_this(); }"),
]
os.makedirs(OUT, exist_ok=True)
for old in os.listdir(OUT):  # nothing a spec no longer names survives into this build
    if old.startswith("x_") and old.endswith(".inc"):
        os.remove(os.path.join(OUT, old))
lines_of = {}
for name, f, a, b, first, last in SPECS:
    if f not in lines_of:
        lines_of[f] = subprocess.run(["git", "-C", W, "show", "%s:%s" % (PIN, where(f))], capture_output=True, check=True).stdout.decode("latin-1").split("\n")
    L = lines_of[f]
    if (first and first not in L[a - 1]) or last not in L[b - 1]:
        print("t34-extract: %s:%d-%d no longer holds %r ... %r" % (f, a, b, first, last), file=sys.stderr); sys.exit(1)
specs_ok = []
for name, f, a, b, first, last in SPECS:
    L = lines_of[f]
    body = "\n".join(L[a - 1:b])
    open(os.path.join(OUT, "x_%s.inc" % name), "w").write("// lifted from %s:%d-%d at %s, verbatim\n#line %d \"%s\"\n%s\n" % (where(f), a, b, PIN[:10], a, f, body))
    specs_ok.append("%s %s:%d-%d" % (name, f, a, b))
print("t34-extract: %d extracts, each holding its first and last line: %s" % (len(SPECS), "; ".join(specs_ok)))
