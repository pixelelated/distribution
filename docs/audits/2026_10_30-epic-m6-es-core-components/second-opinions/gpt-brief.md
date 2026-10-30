# Independent review: M6 T34, EmulationStation's core components (#681)

You are the independent reviewer for one slice of a code audit. You come from another lab than the first reader (Claude Opus 5.5). The subject is **the 80 files of `es-core/src/components/**`** at the pin `16dbac5211eea7e70db7394372033be2be7df829`: 21,984 lines, 21 modified by the fork and 59 carried from ROCKNIX. The packet below carries:
- the 21 fork-modified files whole, line-numbered at the pin;
- of the 59 upstream-carried files, only the line ranges the first reader cites, each with 8 lines of context, line-numbered;
- the first reader's `02`, `03`, `04` and `05` whole;
- the brief's § 4, the seven questions.

Every excerpt is hashed in `packet-manifest.json`. Neighbouring files (`Window.cpp`, `HttpReq.cpp`, `FileSystemUtil.cpp`, `Font.cpp`) are not in the packet; the first reader cites their lines. Judge their claims as citations, or say you cannot tell.

**If you need other ranges to judge a claim, name them by file and line range at the end of your reply, under `## Sections I need`.** They will come in a second packet.

**Answer these first, each with the lines you read:**
1. **PL-01, the card's closing race** (`AsyncNotificationComponent.cpp:117-121`, `:261-299`; the header's members). Is `close()` really called from worker threads while `update()` runs on the interface thread, with no lock or atomic between them? Is there any happens-before the first reader missed?
2. **PL-02, the card after the window deletes it.** Can the component detect or refuse a late `close()` or `updateText()`? What would the smallest change on the component's side be?
3. **PL-03, the field's two posts** (`TextEditComponent.cpp:39`, `:47`). Is a use after free reachable, given what the component itself guarantees?
4. **PL-04 and PL-05, the help bar.** At the pin, does `ComponentList.cpp:568`'s `_("up/down")` reach `HelpComponent::getIconTexture` as a translated key? Would a tabbed `MenuComponent` (`MenuComponent.cpp:531-533`, `ComponentGrid.cpp:519-553`, `ComponentTab.cpp:320-345`) offer SWITCH TAB while its strip holds focus? The guest showed neither on M7's image.
5. **The seven leads the brief expects to FAIL at the pin** (3.4, 3.6, 3.7, 3.8, 3.16, 3.21, 3.26 in `02` § The leads). For each: does the code at the pin do what the lead says? 3.21's first half is claimed sound (L-09).

**Then grade every punch item PL-01 to PL-26 in `05`.** One line each:
- `confirmed`, `confirmed with narrowing`, `refuted`, or `cannot tell from the packet`;
- why, and the line;
- the severity, if you would change it.

**Add any defect the first reader missed, as G-n**, with its lines. Be concrete and cite lines. Do not restate the packet.

---

# T34 (#681) packet: EmulationStation's core components at the pin 16dbac5211eea7e70db7394372033be2be7df829


## AsyncNotificationComponent.cpp (whole, fork-modified, at the pin)

```text
    1  #include "AsyncNotificationComponent.h"
    2  #include "math/Misc.h"
    3  #include "ThemeData.h"
    4  #include "components/ComponentGrid.h"
    5  #include "components/NinePatchComponent.h"
    6  #include "components/TextComponent.h"
    7  #include "LocaleES.h"
    8  #include "Window.h"
    9  // The choosing itself is pure and lives with the rest of the cloud text, so
   10  // a test binary can reach it (es-app/tests/unit). Reached the way Window.cpp
   11  // reaches ApiSystem: es-core's include path does not carry es-app.
   12  #include "../../es-app/src/CloudText.h"
   13  #include <SDL_timer.h>
   14  
   15  #define PADDING_PX  (Renderer::getScreenWidth()*0.01)
   16  
   17  // How solid the card is over whatever it covers.
   18  //
   19  // It was 200 of 255, and at that weight the themed panel -- 0x111111 in the
   20  // shipped theme -- washes out to roughly a fifth of the game art behind it, so
   21  // a progress line sat on a mid-grey smear that changed with the artwork. Every
   22  // other themed surface in the app (menus, dialogs, and GuiInfoPopup once its
   23  // fade-in completes) draws its background at full opacity and lets the theme
   24  // decide how solid to be; this was the one that did not, and it is the one
   25  // that is hard to read.
   26  //
   27  // Full opacity is therefore the standard, not a new choice. The card still
   28  // reads as an overlay rather than a page: frame.png's corners fade to nothing,
   29  // so the panel keeps its soft rounded edge, and the fade in and out below
   30  // still animates through this value.
   31  #define NOTIFICATION_OPACITY  255
   32  
   33  AsyncNotificationComponent::AsyncNotificationComponent(Window* window, bool actionLine)
   34  	: GuiComponent(window)
   35  {
   36  	mRunning = true;
   37  	mFadeTime = 0;
   38  	mFadeOut = 0;
   39  	mPercent = -1;
   40  	mClosing = false;
   41  
   42  	auto theme = ThemeData::getMenuTheme();
   43  
   44  	// Note : Don't localize this text -> It is only used to guess width calculation for the component.
   45  	//
   46  	// Wide enough for what actually goes in it. The card was sized to fit
   47  	// thirty characters, which suits "Scraping: <short name>" and truncates
   48  	// everything else -- an rclone stats line ("Transferred: 12.3 MiB / 45.6
   49  	// MiB, 27%, 1.2 MiB/s, ETA 27s") is twice that, so the one number
   50  	// somebody wants was always off the end. A share of the screen rather
   51  	// than a character count, because these panels run from 640x480 to
   52  	// 1920x1080 and a fixed width is right on exactly one of them; the
   53  	// measured width stays as the floor so nothing gets narrower than it was.
   54  	//
   55  	// 0.9 is GuiInfoPopup's cap -- the widest this app lets a non-blocking
   56  	// overlay get -- and taking it settles a question the in-between sizes
   57  	// kept asking. Past half the screen a card pinned to one corner stops
   58  	// reading as a deliberate placement and starts reading as a panel that
   59  	// failed to fit; at the same width centred (see renderAsyncNotifications)
   60  	// it reads as one. It also puts this card where the message that follows
   61  	// it already appears, so nothing jumps.
   62  	float width = Math::max(
   63  		theme->TextSmall.font->sizeText("TEXT FOR SIZE CALCULATION TEST").x(),
   64  		Renderer::getScreenWidth() * 0.9f);
   65  
   66  	mTitle = std::make_shared<TextComponent>(mWindow, "", theme->TextSmall.font, theme->TextSmall.color, ALIGN_LEFT);
   67  	mGameName = std::make_shared<TextComponent>(mWindow, "", theme->TextSmall.font, theme->Text.color, ALIGN_LEFT);
   68  
   69  	if (actionLine)
   70  		mAction = std::make_shared<TextComponent>(mWindow, "", theme->TextSmall.font, theme->Text.color, ALIGN_LEFT);
   71  
   72  	Vector2f fullSize(width + 2 * PADDING_PX, 2 * PADDING_PX + mTitle->getSize().y() + mGameName->getSize().y() + (mAction == nullptr ? 0 : mAction->getSize().y()));
   73  	Vector2f gridSize(width, mTitle->getSize().y() + mGameName->getSize().y() + (mAction == nullptr ? 0 : mAction->getSize().y()));
   74  
   75  	setSize(fullSize);
   76  	mFullSize = fullSize;
   77  
   78  	mFrame = new NinePatchComponent(window);
   79  	mFrame->setImagePath(theme->Background.path);
   80  	// The theme's own edge colour, like every other panel in the app.
   81  	//
   82  	// A drawn-in rim was tried here and was wrong: this card is what a
   83  	// RetroAchievements sync, a scrape and a theme install all appear in, and
   84  	// giving it a stroke no menu or dialog has made those look like a
   85  	// different application's widget. The card was hard to read because it was
   86  	// translucent, not because it lacked an outline -- NOTIFICATION_OPACITY
   87  	// above is the fix that was actually needed, and a long transfer that
   88  	// really does need to dominate the screen now has a page of its own
   89  	// (GuiCloudTransfer) instead of asking this card to shout.
   90  	mFrame->setEdgeColor(theme->Background.color);
   91  	mFrame->setCenterColor(theme->Background.centerColor);
   92  	mFrame->setCornerSize(theme->Background.cornerSize);
   93  	mFrame->setPostProcessShader(theme->Background.menuShader, false);
   94  	mFrame->fitTo(mSize, Vector3f::Zero(), Vector2f(-32, -32));
   95  	addChild(mFrame);
   96  
   97  	mGrid = new ComponentGrid(window, Vector2i(1, mAction == nullptr ? 2 : 3));
   98  	mGrid->setPosition((fullSize.x() - gridSize.x()) / 2.0, (fullSize.y() - gridSize.y()) / 2.0);
   99  	mGrid->setSize(gridSize);
  100  	mGrid->setEntry(mTitle, Vector2i(0, 0), false, true);
  101  	mGrid->setEntry(mGameName, Vector2i(0, 1), false, true);
  102  
  103  	if (mAction != nullptr)
  104  		mGrid->setEntry(mAction, Vector2i(0, 2), false, true);
  105  
  106  	addChild(mGrid);
  107  
  108  	// Centred at the top, like GuiInfoPopup. Window::renderAsyncNotifications
  109  	// re-applies this every frame (it has to, to stack several of them), so
  110  	// this is only the position the card holds before its first render --
  111  	// but the two must agree, or the card lands in one place and moves.
  112  	setPosition(Renderer::getScreenWidth() * 0.5f - mSize.x() * 0.5f,
  113  		Renderer::getScreenHeight() * 0.02f, 0);
  114  	setOpacity(NOTIFICATION_OPACITY);
  115  }
  116  
  117  void AsyncNotificationComponent::close()
  118  {
  119  	mClosing = true;	
  120  	mFadeTime = -1;
  121  }
  122  
  123  AsyncNotificationComponent::~AsyncNotificationComponent()
  124  {
  125  	delete mFrame;
  126  	delete mGrid;	
  127  }
  128  
  129  // The first candidate that fits the row, else the last one offered.
  130  //
  131  // Sizing text is a glyph lookup per character and the font atlas is a GL
  132  // resource, so this runs on the interface thread (render) and never on the
  133  // worker that composed the strings. A row that has not been sized yet gets
  134  // the first candidate: the full form is the right answer when nothing is
  135  // known, and the row is re-chosen when the candidates next change.
  136  std::string AsyncNotificationComponent::chooseThatFits(const std::shared_ptr<TextComponent>& row, const std::vector<std::string>& candidates)
  137  {
  138  	const float width = (row == nullptr) ? 0.0f : row->getSize().x();
  139  
  140  	std::function<float(const std::string&)> measure;
  141  	if (row != nullptr && row->getFont() != nullptr)
  142  		measure = [row](const std::string& candidate) { return row->getFont()->sizeText(candidate).x(); };
  143  
  144  	return CloudText::chooseThatFits(candidates, width, measure);
  145  }
  146  
  147  void AsyncNotificationComponent::updateText(const std::string text, const std::string action)
  148  {
  149  	std::unique_lock<std::mutex> lock(mMutex);
  150  
  151  	mNextGameName.clear();
  152  	mNextGameName.push_back(text);
  153  	mNextAction.clear();
  154  	mNextAction.push_back(action);
  155  }
  156  
  157  void AsyncNotificationComponent::updateText(const std::string text, const std::vector<std::string>& actionCandidates)
  158  {
  159  	std::unique_lock<std::mutex> lock(mMutex);
  160  
  161  	mNextGameName.clear();
  162  	mNextGameName.push_back(text);
  163  	mNextAction = actionCandidates;
  164  	if (mNextAction.empty())
  165  		mNextAction.push_back("");
  166  }
  167  
  168  void AsyncNotificationComponent::updateText(const std::vector<std::string>& textCandidates, const std::vector<std::string>& actionCandidates)
  169  {
  170  	std::unique_lock<std::mutex> lock(mMutex);
  171  
  172  	mNextGameName = textCandidates;
  173  	if (mNextGameName.empty())
  174  		mNextGameName.push_back("");
  175  	mNextAction = actionCandidates;
  176  	if (mNextAction.empty())
  177  		mNextAction.push_back("");
  178  }
  179  
  180  void AsyncNotificationComponent::updatePercent(int percent)
  181  {
  182  	std::unique_lock<std::mutex> lock(mMutex);
  183  
  184  	mPercent = percent;
  185  }
  186  
  187  void AsyncNotificationComponent::updateTitle(const std::string text)
  188  {
  189  	std::unique_lock<std::mutex> lock(mMutex);
  190  
  191  	mNextTitle = text;
  192  }
  193  
  194  void AsyncNotificationComponent::render(const Transform4x4f& parentTrans)
  195  {
  196  	std::unique_lock<std::mutex> lock(mMutex);
  197  
  198  	Transform4x4f trans = parentTrans * getTransform();
  199  
  200  	// Both rows re-chosen only when their candidates change: sizing text is
  201  	// a glyph lookup per character, and this runs every frame.
  202  	if (mGameName != nullptr)
  203  	{
  204  		std::string key;
  205  		for (auto& c : mNextGameName)
  206  			key += c + "\n";
  207  		if (key != mAppliedGameName)
  208  		{
  209  			mAppliedGameName = key;
  210  			mGameName->setText(chooseThatFits(mGameName, mNextGameName));
  211  		}
  212  	}
  213  
  214  	if (mAction != nullptr)
  215  	{
  216  		std::string key;
  217  		for (auto& c : mNextAction)
  218  			key += c + "\n";
  219  		if (key != mAppliedAction)
  220  		{
  221  			mAppliedAction = key;
  222  			mAction->setText(chooseThatFits(mAction, mNextAction));
  223  		}
  224  	}
  225  
  226  	if (mTitle != nullptr && mNextTitle != mTitle->getText())
  227  		mTitle->setText(mNextTitle);
  228  
  229  	mFrame->render(trans);
  230  
  231  	auto lastControl = mGameName;
  232  	if (mAction != nullptr)
  233  		lastControl = mAction;
  234  
  235  	float x = mGrid->getPosition().x() + lastControl->getPosition().x();
  236  	float y = mGrid->getPosition().y() + lastControl->getPosition().y();
  237  	float w = lastControl->getSize().x();
  238  	float h = lastControl->getSize().y();
  239  
  240  	h /= 10.0;
  241  	y += lastControl->getSize().y();
  242  
  243  	Renderer::setMatrix(trans);
  244  
  245  	if (mPercent >= 0)
  246  	{
  247  		float percent = mPercent / 100.0;
  248  		if (percent < 0)
  249  			percent = 0;
  250  		else if (percent > 1)
  251  			percent = 1;
  252  
  253  		auto theme = ThemeData::getMenuTheme();
  254  		auto color = theme->Text.color & 0xFFFFFF00 | (unsigned char)((theme->Text.color & 0xFF) * (getOpacity() / 255.0));
  255  		Renderer::drawRect(x, y, (w*percent), h, color);
  256  	}
  257  
  258  	mGrid->render(trans);
  259  }
  260  
  261  void AsyncNotificationComponent::update(int deltaTime)
  262  {
  263  	GuiComponent::update(deltaTime);
  264  
  265  	// compute fade effects
  266  
  267  	if (mClosing && mFadeTime == -1)
  268  	{
  269  		mFadeOutOpacity = getOpacity();
  270  		mFadeTime = 0;
  271  		return;
  272  	}
  273  	else if (mFadeTime < 500000)
  274  		mFadeTime += deltaTime;
  275  
  276  	int alpha = NOTIFICATION_OPACITY;
  277  	int duration = 500;
  278  
  279  	if (mClosing)
  280  	{
  281  		if (mFadeTime <= duration)
  282  		{
  283  			alpha = ((duration - mFadeTime) * 255 / duration);
  284  			mFadeOut = (float)(255 - alpha) / 255.0;
  285  			alpha = (alpha * mFadeOutOpacity) / 255;
  286  		}
  287  		else
  288  		{
  289  			mRunning = false;
  290  			mFadeOut = 0;
  291  		}
  292  	}
  293  	else
  294  	{
  295  		if (mFadeTime <= duration)
  296  		{
  297  			int dt = ((duration - mFadeTime) * 255 / duration);
  298  			mFadeOut = (float)(255 - dt) / 255.0;
  299  			alpha = (mFadeTime * alpha / duration);
  300  		}
  301  		else
  302  			mFadeOut = 0;
  303  	}
  304  
  305  	setOpacity((unsigned char)alpha);
  306  }
```

## AsyncNotificationComponent.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  
    3  #include <mutex>
    4  #include "GuiComponent.h"
    5  #include <string>
    6  #include <vector>
    7  
    8  class ComponentGrid;
    9  class NinePatchComponent;
   10  class TextComponent;
   11  class Window;
   12  
   13  class AsyncNotificationComponent : public GuiComponent
   14  {
   15  	friend class Window;
   16  
   17  protected:
   18  	AsyncNotificationComponent(Window* window, bool actionLine = true);
   19  	~AsyncNotificationComponent();
   20  
   21  public:
   22  	void update(int deltaTime) override;
   23  	void render(const Transform4x4f& parentTrans) override;
   24  
   25  	void updateTitle(const std::string text);
   26  	void updateText(const std::string text, const std::string action = "");
   27  	// The action row from a list of candidates, longest first: the first
   28  	// that fits the row's width is the one shown, else the last. Measured
   29  	// in render(), on the interface thread, with the row's own font --
   30  	// callers on a worker thread have no safe way to size text, and the
   31  	// fonts' glyph atlas is a GL resource. Written for the cloud sync
   32  	// card's outcome line (D-UI-028): what is in place plus how to recover
   33  	// where both fit, the recovery alone where they do not.
   34  	void updateText(const std::string text, const std::vector<std::string>& actionCandidates);
   35  	// Both rows from candidates. The text row is composed too -- the
   36  	// outcome word and then a whole sentence saying why -- so it runs off
   37  	// a 640x480 panel and was clipped mid-word with an ellipsis, which is
   38  	// the one thing a reason line must not do (#115). Same rule as the
   39  	// action row: longest first, first that fits.
   40  	void updateText(const std::vector<std::string>& textCandidates, const std::vector<std::string>& actionCandidates);
   41  	void updatePercent(int percent);
   42  
   43  	float getFading() { return mFadeOut; }
   44  	bool isClosing() { return mClosing; };
   45  	bool isRunning() { return mRunning; };
   46  	Vector2f getFullSize() { return mFullSize; };
   47  
   48  	void close();
   49  	
   50  private:
   51  	std::shared_ptr<TextComponent> mTitle;
   52  	std::shared_ptr<TextComponent> mGameName;
   53  	std::shared_ptr<TextComponent> mAction;
   54  
   55  	std::vector<std::string> mNextGameName; // candidates, longest first
   56  	std::string mAppliedGameName;           // the candidates the row was last chosen from, joined
   57  	std::string mNextTitle;
   58  	std::vector<std::string> mNextAction;   // candidates, longest first
   59  	std::string mAppliedAction;             // the candidates the row was last chosen from, joined
   60  
   61  	// The first candidate that fits the row, else the last one offered.
   62  	static std::string chooseThatFits(const std::shared_ptr<TextComponent>& row, const std::vector<std::string>& candidates);
   63  
   64  	ComponentGrid* mGrid;
   65  	NinePatchComponent* mFrame;
   66  
   67  	std::mutex					mMutex;
   68  
   69  	int mPercent;
   70  
   71  	bool                mRunning;
   72  	bool				mClosing;
   73  	float				mFadeOut;
   74  	int                 mFadeTime;
   75  	int                 mFadeOutOpacity;
   76  
   77  	Vector2f			mFullSize;
   78  };
```

## BatteryIndicatorComponent.cpp `:44-56` (an excerpt, upstream-carried, at the pin)

```text
   44  		mAt25 = ResourceManager::getInstance()->getResourcePath(":/battery/25.svg");
   45  
   46  	if (ResourceManager::getInstance()->fileExists(":/battery/empty.svg"))
   47  		mEmpty = ResourceManager::getInstance()->getResourcePath(":/battery/empty.svg");	
   48  
   49  	if (ResourceManager::getInstance()->fileExists(":/network.svg"))
   50  	{
   51  		mView |= ActivityView::NETWORK;
   52  		mNetworkImage = TextureResource::get(ResourceManager::getInstance()->getResourcePath(":/network.svg"), false, true);
   53  	}
   54  
   55  	updateBatteryInfo();
   56  }
```

## BusyComponent.cpp `:27-43` (an excerpt, upstream-carried, at the pin)

```text
   27  	mBackground.setCenterColor(theme->Background.centerColor);
   28  	mBackground.setCornerSize(theme->Background.cornerSize);
   29  	mBackground.setPostProcessShader(theme->Background.menuShader, false);
   30  
   31  	mutex = SDL_CreateMutex();
   32  	mAnimation = std::make_shared<AnimatedImageComponent>(mWindow);
   33  	mAnimation->load(&BUSY_ANIMATION_DEF);
   34  	
   35  	mText = std::make_shared<TextComponent>(mWindow, text == "__default__" ? _("WORKING...") : text, ThemeData::getMenuTheme()->Text.font, ThemeData::getMenuTheme()->Text.color); 	
   36  	mText->setLineSpacing(1.2f);
   37  
   38  	// col 0 = animation, col 1 = spacer, col 2 = text
   39  	mGrid.setEntry(mAnimation, Vector2i(1, 1), false, true);
   40  	mGrid.setEntry(mText, Vector2i(3, 1), false, false);
   41  
   42  	addChild(&mBackground);
   43  	addChild(&mGrid);
```

## ButtonComponent.cpp `:2-18` (an excerpt, upstream-carried, at the pin)

```text
    2  #include "resources/Font.h"
    3  #include "utils/StringUtil.h"
    4  #include "LocaleES.h"
    5  #include "TextToSpeech.h"
    6  #include "Settings.h"
    7  #include "Window.h"
    8  #include "utils/HtmlColor.h"
    9  
   10  #define TEXT_PADDING Math::max(12, Renderer::getScreenWidth() * 0.014)
   11  
   12  ButtonComponent::ButtonComponent(Window* window, const std::string& text, const std::string& helpText, const std::function<void()>& func, bool upperCase) : GuiComponent(window),
   13  	mBox(window, ThemeData::getMenuTheme()->Button.path),	
   14  	mFocused(false), 
   15  	mEnabled(true),
   16  	mMousePressed(false)	
   17  {
   18  	auto menuTheme = ThemeData::getMenuTheme();
```

## ButtonComponent.cpp `:41-98` (an excerpt, upstream-carried, at the pin)

```text
   41  		Vector3f(mPadding.x(), mPadding.y()), 
   42  		Vector2f(-sz.x() * 2, -sz.y() * 2));
   43  }
   44  
   45  void ButtonComponent::setPressedFunc(std::function<void()> f)
   46  {
   47  	mPressedFunc = f;
   48  }
   49  
   50  bool ButtonComponent::input(InputConfig* config, Input input)
   51  {
   52  	if (config->isMappedTo(BUTTON_OK, input) && input.value != 0)
   53  	{
   54  		if (mPressedFunc && mEnabled)
   55  			mPressedFunc();
   56  
   57  		return true;
   58  	}
   59  
   60  	return GuiComponent::input(config, input);
   61  }
   62  
   63  void ButtonComponent::onOpacityChanged()
   64  {
   65  	mBox.setOpacity(getOpacity());
   66  
   67  	if (mTextCache)
   68  		mTextCache->setColor(getCurTextColor());
   69  }
   70  
   71  void ButtonComponent::setText(const std::string& text, const std::string& helpText, bool upperCase)
   72  {
   73  	mText = upperCase ? Utils::String::toUpper(text) : text;
   74  	mHelpText = helpText;
   75  	
   76  	mTextCache = std::unique_ptr<TextCache>(mFont->buildTextCache(mText, 0, 0, getCurTextColor()));
   77  
   78  	float padding = TEXT_PADDING;
   79  	float minWidth = mFont->sizeText("DELETE").x() + padding;
   80  	setSize(Math::max(mTextCache->metrics.size.x() + padding, minWidth), mTextCache->metrics.size.y());
   81  
   82  	updateHelpPrompts();
   83  }
   84  
   85  void ButtonComponent::onFocusGained()
   86  {
   87  	if (mFocused)
   88  		return;
   89  
   90  	mFocused = true;
   91  	updateImage();
   92  
   93  	TextToSpeech::getInstance()->say(mText, true);
   94  }
   95  
   96  void ButtonComponent::onFocusLost()
   97  {
   98  	if (!mFocused)
```

## ButtonComponent.cpp `:136-152` (an excerpt, upstream-carried, at the pin)

```text
  136  	Transform4x4f trans = parentTrans * getTransform();
  137  
  138  	if (mRenderNonFocusedBackground || mFocused)
  139  		mBox.render(trans);
  140  	else
  141  	{
  142  		Renderer::setMatrix(trans);
  143  		Renderer::drawRect(mPadding.x(), mPadding.y(), mSize.x() - mPadding.x() - mPadding.z(), mSize.y() - mPadding.y() - mPadding.w(), 0x60606025);
  144  	}
  145  
  146  	if (mMousePressed && mIsMouseOver)
  147  	{
  148  		Renderer::setMatrix(trans);
  149  		Renderer::drawRect(0.0f, 0.0f, mSize.x(), mSize.y(), 0x00000010, 0x00000010);
  150  	}
  151  	else if (mIsMouseOver)
  152  	{
```

## ButtonComponent.cpp `:178-225` (an excerpt, upstream-carried, at the pin)

```text
  178  	return Utils::HtmlColor::applyColorOpacity(mFocused ? mTextColorFocused : mTextColorUnfocused, getOpacity());
  179  }
  180  
  181  unsigned int ButtonComponent::getCurBackColor() const
  182  {
  183  	return Utils::HtmlColor::applyColorOpacity(mFocused ? mColorFocused : mColor, getOpacity());
  184  }
  185  
  186  std::vector<HelpPrompt> ButtonComponent::getHelpPrompts()
  187  {
  188  	std::vector<HelpPrompt> prompts;
  189  	prompts.push_back(HelpPrompt(BUTTON_OK, mHelpText.empty() ? mText.c_str() : mHelpText.c_str()));
  190  	return prompts;
  191  }
  192  
  193  void ButtonComponent::onPaddingChanged()
  194  {
  195  	onSizeChanged();
  196  }
  197  
  198  bool ButtonComponent::onMouseClick(int button, bool pressed, int x, int y)
  199  {
  200  	if (button == 1)
  201  	{
  202  		if (pressed)
  203  		{
  204  			mMousePressed = true;
  205  			mWindow->setMouseCapture(this);
  206  		}
  207  		else if (mMousePressed)
  208  		{
  209  			mWindow->releaseMouseCapture();
  210  
  211  			mMousePressed = false;
  212  
  213  			if (mIsMouseOver)
  214  			{
  215  				if (mPressedFunc && mEnabled)
  216  					mPressedFunc();
  217  			}
  218  		}
  219  
  220  		return true;
  221  	}	
  222  
  223  	return false;
  224  }
  225  
```

## CarouselComponent.cpp `:66-100` (an excerpt, upstream-carried, at the pin)

```text
   66  }
   67  
   68  void CarouselComponent::clearEntries()
   69  {
   70  	mWasRendered = false;
   71  	mEntries.clear();
   72  }
   73  
   74  int CarouselComponent::moveCursorFast(bool forward)
   75  {
   76  	int value = mCursor;
   77  	int count = forward ? 10 : -10;
   78  	int sz = mEntries.size();
   79  
   80  	if (count >= sz)
   81  		return value;
   82  
   83  	value += count;
   84  	if (value < 0) 
   85  		value += sz;
   86  	if (value >= sz) 
   87  		value -= sz;
   88  
   89  	return value;
   90  }
   91  
   92  bool CarouselComponent::input(InputConfig* config, Input input)
   93  {
   94  	if(input.value != 0)
   95  	{	
   96  		switch (mType)
   97  		{
   98  		case CarouselType::VERTICAL:
   99  		case CarouselType::VERTICAL_WHEEL:
  100  			if (config->isMappedLike("up", input) || config->isMappedLike("lefttrigger", input))
```

## CarouselComponent.cpp `:105-127` (an excerpt, upstream-carried, at the pin)

```text
  105  			if (config->isMappedLike("down", input) || config->isMappedLike("righttrigger", input))
  106  			{
  107  				listInput(1);
  108  				return true;
  109  			}
  110  			if (config->isMappedTo("pagedown", input))
  111  			{
  112  				int cursor = moveCursorFast(true);
  113  				listInput(cursor - mCursor);				
  114  				return true;
  115  			}
  116  			if (config->isMappedTo("pageup", input))
  117  			{
  118  				int cursor = moveCursorFast(false);
  119  				listInput(cursor - mCursor);
  120  				return true;
  121  			}
  122  
  123  			break;
  124  		case CarouselType::HORIZONTAL:
  125  		case CarouselType::HORIZONTAL_WHEEL:
  126  		default:
  127  			if (config->isMappedLike("left", input) || config->isMappedLike("lefttrigger", input))
```

## CarouselComponent.cpp `:175-208` (an excerpt, upstream-carried, at the pin)

```text
  175  			comp->update(deltaTime);
  176  	}
  177  	
  178  	listUpdate(deltaTime);	
  179  
  180  	GuiComponent::update(deltaTime);
  181  }
  182  
  183  void CarouselComponent::onCursorChanged(const CursorState& state)
  184  {
  185  	// update help style
  186  	updateHelpPrompts();
  187  
  188  	float startPos = mCamOffset;
  189  
  190  	float posMax = (float)mEntries.size();
  191  	float target = (float)mCursor;
  192  
  193  	// what's the shortest way to get to our target?
  194  	// it's one of these...
  195  
  196  	float endPos = target; // directly
  197  	float dist = abs(endPos - startPos);
  198  
  199  	if(abs(target + posMax - startPos) < dist)
  200  		endPos = target + posMax; // loop around the end (0 -> max)
  201  	if(abs(target - posMax - startPos) < dist)
  202  		endPos = target - posMax; // loop around the start (max - 1 -> -1)
  203  
  204  	cancelAnimation(1);
  205  	cancelAnimation(2);
  206  	
  207  	if (mLastCursor == mCursor)
  208  	{
```

## CarouselComponent.cpp `:346-369` (an excerpt, upstream-carried, at the pin)

```text
  346  
  347  	if (!mWasRendered && mShowing)
  348  	{
  349  		mWasRendered = true;
  350  		onShow();
  351  	}
  352  }
  353  
  354  std::vector<HelpPrompt> CarouselComponent::getHelpPrompts()
  355  {
  356  	std::vector<HelpPrompt> prompts;
  357  
  358  	if (mType == CarouselType::VERTICAL || mType == CarouselType::VERTICAL_WHEEL)
  359  		prompts.push_back(HelpPrompt("up/down", _("CHOOSE")));
  360  	else
  361  		prompts.push_back(HelpPrompt("left/right", _("CHOOSE")));
  362  
  363  	return prompts;
  364  }
  365  
  366  void CarouselComponent::setDefaultBackground(unsigned int color, unsigned int colorEnd, bool gradientHorizontal)
  367  {
  368  	mColor = color;
  369  	mColorEnd = colorEnd;
```

## CarouselComponent.cpp `:755-773` (an excerpt, upstream-carried, at the pin)

```text
  755  		case CarouselImageSource::BOXART:    mediaName = "boxart";    break;
  756  		case CarouselImageSource::BOXBACK:   mediaName = "boxback";   break;
  757  		case CarouselImageSource::MARQUEE:   mediaName = "marquee";   break;
  758  		case CarouselImageSource::FANART:    mediaName = "fanart";    break;
  759  		case CarouselImageSource::CARTRIDGE: mediaName = "cartridge"; break;
  760  		case CarouselImageSource::MIX:       mediaName = "mix";       break;
  761  		}
  762  
  763  		std::string marqueePath = entry.object->getProperty(mediaName).toString();
  764  
  765  		if (mImageSource != CarouselImageSource::TEXT && !marqueePath.empty() && Utils::FileSystem::exists(marqueePath))
  766  		{
  767  			ImageComponent* logo = new ImageComponent(mWindow, false, true);
  768  			logo->setMaxSize(mLogoSize * mLogoScale);
  769  
  770  			if (mImageSource == CarouselImageSource::IMAGE) // If it's of type image, it's probably the systemview
  771  				logo->setIsLinear(true);
  772  
  773  			logo->applyTheme(mTheme, mThemeViewName, mThemeLogoName, ThemeFlags::COLOR | ThemeFlags::ALIGNMENT | ThemeFlags::VISIBLE); //  ThemeFlags::PATH | 
```

## ComponentGrid.cpp (whole, fork-modified, at the pin)

```text
    1  #include "components/ComponentGrid.h"
    2  
    3  #include "Settings.h"
    4  #include "LocaleES.h"
    5  #include "ThemeData.h"
    6  
    7  using namespace GridFlags;
    8  
    9  ComponentGrid::ComponentGrid(Window* window, const Vector2i& gridDimensions) : GuiComponent(window), 
   10  	mGridSize(gridDimensions), mCursor(0, 0)
   11  {
   12  	assert(gridDimensions.x() > 0 && gridDimensions.y() > 0);
   13  
   14  	mSeparatorColor = ThemeData::getMenuTheme()->Grid.hasSeparatorColor ? ThemeData::getMenuTheme()->Grid.separatorColor : ThemeData::getMenuTheme()->Text.separatorColor;
   15  	mCells.reserve(gridDimensions.x() * gridDimensions.y());
   16  
   17  	for(int x = 0; x < gridDimensions.x(); x++)
   18  		mColWidths.push_back(new GridSizeInfo());
   19  
   20  	for (int y = 0; y < gridDimensions.y(); y++)
   21  		mRowHeights.push_back(new GridSizeInfo());
   22  }
   23  
   24  ComponentGrid::~ComponentGrid()
   25  {
   26  	for (auto ptr : mRowHeights)
   27  		delete ptr;
   28  
   29  	for (auto ptr : mColWidths)
   30  		delete ptr;	
   31  }
   32  
   33  float ComponentGrid::getColWidth(int col)
   34  {
   35  	if (col < 0 || col >= mColWidths.size())
   36  		return 0;
   37  
   38  	if (mColWidths[col]->value != 0 || mColWidths[col]->absolute)
   39  		return mColWidths[col]->compute(mSize.x());
   40  
   41  	// calculate automatic width
   42  	float freeWidth = mSize.x();
   43  
   44  	int autoSizeCols = 0;
   45  	for (int x = 0; x < mGridSize.x(); x++)
   46  	{
   47  		if (mColWidths[x]->value == 0 && !mColWidths[x]->absolute)
   48  			autoSizeCols++;
   49  		else
   50  			freeWidth -= mColWidths[x]->compute(mSize.x());
   51  	}
   52  
   53  	return freeWidth / (float)std::max(1, autoSizeCols);
   54  }
   55  
   56  float ComponentGrid::getRowHeight(int row)
   57  {
   58  	if (row < 0 || row >= mRowHeights.size())
   59  		return 0;
   60  
   61  	if (mRowHeights[row]->value != 0 || mRowHeights[row]->absolute)
   62  		return mRowHeights[row]->compute(mSize.y());
   63  
   64  	// calculate automatic height
   65  	float freeHeight = mSize.y();
   66  
   67  	int autoSizeRows = 0;
   68  	for (int y = 0; y < mGridSize.y(); y++)
   69  	{
   70  		if (mRowHeights[y]->value == 0 && !mRowHeights[y]->absolute)
   71  			autoSizeRows++;
   72  		else
   73  			freeHeight -= mRowHeights[y]->compute(mSize.y());
   74  	}
   75  
   76  	return freeHeight / (float) std::max(1, autoSizeRows);
   77  }
   78  
   79  void ComponentGrid::setColWidthPerc(int col, float width, bool update)
   80  {
   81  	assert(width >= 0 && width <= 1);
   82  	assert(col >= 0 && col < mGridSize.x());
   83  
   84  	mColWidths[col]->value = width;
   85  	mColWidths[col]->absolute = false;
   86  
   87  	if (update)
   88  		onSizeChanged();
   89  }
   90  
   91  void ComponentGrid::setRowHeightPerc(int row, float height, bool update)
   92  {
   93  	assert(height >= 0 && height <= 1);
   94  	assert(row >= 0 && row < mGridSize.y());
   95  
   96  	mRowHeights[row]->value = height;
   97  	mRowHeights[row]->absolute = false;
   98  
   99  	if (update)
  100  		onSizeChanged();
  101  }
  102  
  103  void ComponentGrid::setColWidth(int col, float width, bool update)
  104  {
  105  //	assert(width >= 0 && width <= 1);
  106  	assert(col >= 0 && col < mGridSize.x());
  107  
  108  	mColWidths[col]->value = width;
  109  	mColWidths[col]->absolute = true;
  110  
  111  	if (update)
  112  		onSizeChanged();
  113  }
  114  
  115  void ComponentGrid::setRowHeight(int row, float height, bool update)
  116  {
  117  //	assert(height >= 0 && height <= 1);
  118  	assert(row >= 0 && row < mGridSize.y());
  119  
  120  	mRowHeights[row]->value = height;
  121  	mRowHeights[row]->absolute = true;
  122  
  123  	if (update)
  124  		onSizeChanged();
  125  }
  126  
  127  void ComponentGrid::setEntry(const std::shared_ptr<GuiComponent>& comp, const Vector2i& pos, bool canFocus, bool resize, const Vector2i& size,
  128  	unsigned int border, GridFlags::UpdateType updateType)
  129  {
  130  	assert(pos.x() >= 0 && pos.x() < mGridSize.x() && pos.y() >= 0 && pos.y() < mGridSize.y());
  131  	assert(comp != nullptr);
  132  	assert(comp->getParent() == NULL);
  133  
  134  	GridEntry entry(pos, size, comp, canFocus, resize, updateType, border);
  135  	mCells.push_back(entry);
  136  
  137  	addChild(comp.get());
  138  
  139  	if(!cursorValid() && canFocus)
  140  	{
  141  		auto origCursor = mCursor;
  142  		mCursor = pos;
  143  		onCursorMoved(origCursor, mCursor);
  144  	}
  145  
  146  	updateCellComponent(mCells.back());
  147  	updateSeparators();
  148  }
  149  
  150  bool ComponentGrid::removeEntry(const std::shared_ptr<GuiComponent>& comp)
  151  {
  152  	for(auto it = mCells.cbegin(); it != mCells.cend(); it++)
  153  	{
  154  		if(it->component == comp)
  155  		{
  156  			removeChild(comp.get());
  157  			mCells.erase(it);
  158  			return true;
  159  		}
  160  	}
  161  
  162  	return false;
  163  }
  164  
  165  void ComponentGrid::updateCellComponent(const GridEntry& cell)
  166  {
  167  	// size
  168  	Vector2f size(0, 0);
  169  	for(int x = cell.pos.x(); x < cell.pos.x() + cell.dim.x(); x++)
  170  		size[0] += getColWidth(x);
  171  	for(int y = cell.pos.y(); y < cell.pos.y() + cell.dim.y(); y++)
  172  		size[1] += getRowHeight(y);
  173  
  174  	if(cell.resize)
  175  		cell.component->setSize(size);
  176  
  177  	// position
  178  	// find top left corner
  179  	Vector3f pos(0, 0, 0);
  180  	for(int x = 0; x < cell.pos.x(); x++)
  181  		pos[0] += getColWidth(x);
  182  	for(int y = 0; y < cell.pos.y(); y++)
  183  		pos[1] += getRowHeight(y);
  184  
  185  	// center component
  186  
  187  	if (cell.component->getThemeTypeName() == "image")
  188  	{
  189  		pos[0] = pos.x() + size.x() * cell.component->getOrigin().x();
  190  		pos[1] = pos.y() + size.y() * cell.component->getOrigin().y();
  191  	}
  192  	else
  193  	{
  194  		pos[0] = pos.x() + (size.x() - cell.component->getSize().x()) / 2;
  195  		pos[1] = pos.y() + (size.y() - cell.component->getSize().y()) / 2;
  196  	}
  197  	
  198  	cell.component->setPosition(pos);
  199  }
  200  
  201  void ComponentGrid::updateSeparators()
  202  {
  203  	mLines.clear();
  204  
  205  	unsigned int color = Renderer::convertColor(mSeparatorColor);
  206  
  207  	bool drawAll = Settings::DebugGrid();
  208  	if (drawAll)
  209  		color = 0xFF00FFFF;
  210  
  211  	Vector2f pos;
  212  	Vector2f size;
  213  	for(auto it = mCells.cbegin(); it != mCells.cend(); it++)
  214  	{
  215  		if(!it->border && !drawAll)
  216  			continue;
  217  
  218  		// find component position + size
  219  		pos = Vector2f(0, 0);
  220  		size = Vector2f(0, 0);
  221  		for(int x = 0; x < it->pos.x(); x++)
  222  			pos[0] += getColWidth(x);
  223  		for(int y = 0; y < it->pos.y(); y++)
  224  			pos[1] += getRowHeight(y);
  225  		for(int x = it->pos.x(); x < it->pos.x() + it->dim.x(); x++)
  226  			size[0] += getColWidth(x);
  227  		for(int y = it->pos.y(); y < it->pos.y() + it->dim.y(); y++)
  228  			size[1] += getRowHeight(y);
  229  
  230  		if(it->border & BORDER_TOP || drawAll)
  231  		{
  232  			mLines.push_back( { { pos.x(),               pos.y()               }, { 0.0f, 0.0f }, color } );
  233  			mLines.push_back( { { pos.x() + size.x(),    pos.y()               }, { 0.0f, 0.0f }, color } );
  234  		}
  235  		if(it->border & BORDER_BOTTOM || drawAll)
  236  		{
  237  			mLines.push_back( { { pos.x(),               pos.y() + size.y()    }, { 0.0f, 0.0f }, color } );
  238  			mLines.push_back( { { pos.x() + size.x(),    mLines.back().pos.y() }, { 0.0f, 0.0f }, color } );
  239  		}
  240  		if(it->border & BORDER_LEFT || drawAll)
  241  		{
  242  			mLines.push_back( { { pos.x(),               pos.y()               }, { 0.0f, 0.0f }, color } );
  243  			mLines.push_back( { { pos.x(),               pos.y() + size.y()    }, { 0.0f, 0.0f }, color } );
  244  		}
  245  		if(it->border & BORDER_RIGHT || drawAll)
  246  		{
  247  			mLines.push_back( { { pos.x() + size.x(),    pos.y()               }, { 0.0f, 0.0f }, color } );
  248  			mLines.push_back( { { mLines.back().pos.x(), pos.y() + size.y()    }, { 0.0f, 0.0f }, color } );
  249  		}
  250  	}
  251  }
  252  
  253  void ComponentGrid::onSizeChanged()
  254  {
  255  	GuiComponent::onSizeChanged();
  256  
  257  	for(auto it = mCells.cbegin(); it != mCells.cend(); it++)
  258  		updateCellComponent(*it);
  259  
  260  	updateSeparators();
  261  }
  262  
  263  const ComponentGrid::GridEntry* ComponentGrid::getCellAt(int x, int y) const
  264  {
  265  	assert(x >= 0 && x < mGridSize.x() && y >= 0 && y < mGridSize.y());
  266  	
  267  	for(auto it = mCells.cbegin(); it != mCells.cend(); it++)
  268  	{
  269  		int xmin = it->pos.x();
  270  		int xmax = xmin + it->dim.x();
  271  		int ymin = it->pos.y();
  272  		int ymax = ymin + it->dim.y();
  273  
  274  		if(x >= xmin && y >= ymin && x < xmax && y < ymax)
  275  			return &(*it);
  276  	}
  277  
  278  	return NULL;
  279  }
  280  
  281  bool ComponentGrid::input(InputConfig* config, Input input)
  282  {
  283  	const GridEntry* cursorEntry = getCellAt(mCursor);
  284  	if(cursorEntry && cursorEntry->component->input(config, input))
  285  		return true;
  286  
  287  	if(!input.value)
  288  		return false;
  289  
  290  	bool result = false;
  291  
  292  	if (config->isMappedLike("down", input))
  293  		result = moveCursor(Vector2i(0, 1));
  294  	if (config->isMappedLike("up", input))
  295  		result = moveCursor(Vector2i(0, -1));
  296  	if (config->isMappedLike("left", input))
  297  		result = moveCursor(Vector2i(-1, 0));
  298  	if (config->isMappedLike("right", input))
  299  		result = moveCursor(Vector2i(1, 0));
  300  
  301  	if (!result && mUnhandledInputCallback)
  302  		return mUnhandledInputCallback(config, input);	
  303  
  304  	return result;
  305  }
  306  
  307  void ComponentGrid::resetCursor()
  308  {
  309  	if(!mCells.size())
  310  		return;
  311  
  312  	for(auto it = mCells.cbegin(); it != mCells.cend(); it++)
  313  	{
  314  		if(it->canFocus)
  315  		{
  316  			Vector2i origCursor = mCursor;
  317  			mCursor = it->pos;
  318  			onCursorMoved(origCursor, mCursor);
  319  			break;
  320  		}
  321  	}
  322  }
  323  
  324  Vector2i ComponentGrid::getCursor()
  325  {
  326  	return mCursor;
  327  }
  328  
  329  bool ComponentGrid::moveCursor(Vector2i dir)
  330  {
  331  	assert(dir.x() || dir.y());
  332  
  333  	const Vector2i origCursor = mCursor;
  334  
  335  	const GridEntry* currentCursorEntry = getCellAt(mCursor);
  336  
  337  	Vector2i searchAxis(dir.x() == 0, dir.y() == 0);
  338  	
  339  	while(mCursor.x() >= 0 && mCursor.y() >= 0 && mCursor.x() < mGridSize.x() && mCursor.y() < mGridSize.y())
  340  	{
  341  		mCursor = mCursor + dir;
  342  
  343  		Vector2i curDirPos = mCursor;
  344  
  345  		const GridEntry* cursorEntry;
  346  		//spread out on search axis+
  347  		while(mCursor.x() < mGridSize.x() && mCursor.y() < mGridSize.y() && mCursor.x() >= 0 && mCursor.y() >= 0)
  348  		{
  349  			cursorEntry = getCellAt(mCursor);
  350  			if(cursorEntry && cursorEntry->canFocus && cursorEntry != currentCursorEntry)
  351  			{
  352  				onCursorMoved(origCursor, mCursor);
  353  				return true;
  354  			}
  355  
  356  			mCursor += dir;
  357  		}
  358  		/*
  359  		//now again on search axis-
  360  		mCursor = curDirPos;
  361  		while(mCursor.x() >= 0 && mCursor.y() >= 0 && mCursor.x() < mGridSize.x() && mCursor.y() < mGridSize.y())
  362  		{
  363  			cursorEntry = getCellAt(mCursor);
  364  			if(cursorEntry && cursorEntry->canFocus && cursorEntry != currentCursorEntry)
  365  			{
  366  				onCursorMoved(origCursor, mCursor);
  367  				return true;
  368  			}
  369  
  370  			mCursor -= dir;
  371  		}
  372  		*/
  373  		mCursor = curDirPos;
  374  	}
  375  
  376  	//failed to find another focusable element in this direction
  377  	mCursor = origCursor;
  378  	return false;
  379  }
  380  
  381  // Would a press in this direction move the focus? The linear scan
  382  // moveCursor() does -- first focusable cell along dir that is not the one
  383  // under the cursor already -- with nothing moved and nothing signalled.
  384  //
  385  // getHelpPrompts() below used to answer that question from the grid's
  386  // dimensions alone: more than one column means left/right, more than one
  387  // row means up/down. A grid is routinely larger than the set of cells
  388  // anybody can reach, so that claim is often false. A GuiMsgBox is a 2x2
  389  // whose only focusable cell is the button row, and the button row is
  390  // itself an Nx2 grid whose second row is a two-pixel spacer -- so both
  391  // grids offered a direction that leads nowhere, and every one-button
  392  // dialog in the application drew OK CHOOSE CHOOSE (#115).
  393  //
  394  // A help prompt is a promise that a key does something. Ask the cursor
  395  // what the key would do, not the shape of the grid it sits in.
  396  bool ComponentGrid::canMoveCursor(const Vector2i& dir) const
  397  {
  398  	if (dir.x() == 0 && dir.y() == 0)
  399  		return false;
  400  
  401  	const GridEntry* current = getCellAt(mCursor);
  402  
  403  	Vector2i cursor = mCursor + dir;
  404  	while (cursor.x() >= 0 && cursor.y() >= 0 && cursor.x() < mGridSize.x() && cursor.y() < mGridSize.y())
  405  	{
  406  		const GridEntry* candidate = getCellAt(cursor);
  407  		if (candidate && candidate->canFocus && candidate != current)
  408  			return true;
  409  
  410  		cursor += dir;
  411  	}
  412  
  413  	return false;
  414  }
  415  
  416  void ComponentGrid::setCursorTo(Vector2i pos)
  417  {
  418  	assert(pos.x() >= 0 && pos.x() < mGridSize.x() && pos.y() >= 0 && pos.y() < mGridSize.y());
  419  
  420  	const Vector2i origCursor = mCursor;
  421  	mCursor = pos;
  422  
  423  	onCursorMoved(origCursor, pos);
  424  }
  425  
  426  void ComponentGrid::onFocusLost()
  427  {
  428  	const GridEntry* cursorEntry = getCellAt(mCursor);
  429  	if(cursorEntry)
  430  		cursorEntry->component->onFocusLost();
  431  }
  432  
  433  void ComponentGrid::onFocusGained()
  434  {
  435  	const GridEntry* cursorEntry = getCellAt(mCursor);
  436  	if(cursorEntry)
  437  		cursorEntry->component->onFocusGained();
  438  }
  439  
  440  bool ComponentGrid::cursorValid()
  441  {
  442  	const GridEntry* e = getCellAt(mCursor);
  443  	return (e != NULL && e->canFocus);
  444  }
  445  
  446  void ComponentGrid::update(int deltaTime)
  447  {
  448  	// update ALL THE THINGS
  449  	const GridEntry* cursorEntry = getCellAt(mCursor);
  450  	for(auto it = mCells.cbegin(); it != mCells.cend(); it++)
  451  	{
  452  		if(it->updateType == UPDATE_ALWAYS || (it->updateType == UPDATE_WHEN_SELECTED && cursorEntry == &(*it)))
  453  			it->component->update(deltaTime);
  454  	}
  455  }
  456  
  457  void ComponentGrid::render(const Transform4x4f& parentTrans)
  458  {
  459  	Transform4x4f trans = parentTrans * getTransform();
  460  
  461  	auto rect = Renderer::getScreenRect(trans, mSize);
  462  	if (!Renderer::isVisibleOnScreen(rect))
  463  		return;
  464  
  465  	renderChildren(trans);
  466  	
  467  	// draw cell separators
  468  	if(mLines.size())
  469  	{
  470  		Renderer::setMatrix(trans);
  471  		Renderer::bindTexture(0);
  472  		Renderer::drawLines(&mLines[0], mLines.size());
  473  	}
  474  }
  475  
  476  void ComponentGrid::textInput(const char* text)
  477  {
  478  	const GridEntry* selectedEntry = getCellAt(mCursor);
  479  	if(selectedEntry != NULL && selectedEntry->canFocus)
  480  		selectedEntry->component->textInput(text);
  481  }
  482  
  483  void ComponentGrid::onCursorMoved(Vector2i from, Vector2i to)
  484  {
  485  	const GridEntry* cell = getCellAt(from);
  486  	if(cell)
  487  		cell->component->onFocusLost();
  488  
  489  	cell = getCellAt(to);
  490  	if(cell)
  491  		cell->component->onFocusGained();
  492  
  493  	updateHelpPrompts();
  494  }
  495  
  496  bool ComponentGrid::isCursorTo(const std::shared_ptr<GuiComponent>& comp)
  497  {
  498  	for (auto it = mCells.cbegin(); it != mCells.cend(); it++)
  499  		if (it->component == comp && mCursor == it->pos)
  500  			return true;
  501  
  502  	return false;
  503  }
  504  
  505  void ComponentGrid::setCursorTo(const std::shared_ptr<GuiComponent>& comp)
  506  {
  507  	for(auto it = mCells.cbegin(); it != mCells.cend(); it++)
  508  	{
  509  		if(it->component == comp)
  510  		{
  511  			Vector2i oldCursor = mCursor;
  512  			mCursor = it->pos;
  513  			onCursorMoved(oldCursor, mCursor);
  514  			return;
  515  		}
  516  	}
  517  }
  518  
  519  std::vector<HelpPrompt> ComponentGrid::getHelpPrompts()
  520  {
  521  	std::vector<HelpPrompt> prompts;
  522  	const GridEntry* e = getCellAt(mCursor);
  523  	if(e)
  524  		prompts = e->component->getHelpPrompts();
  525  	
  526  	// Only a direction that actually leads to another focusable cell.
  527  	bool canScrollVert = canMoveCursor(Vector2i(0, 1)) || canMoveCursor(Vector2i(0, -1));
  528  	bool canScrollHoriz = canMoveCursor(Vector2i(1, 0)) || canMoveCursor(Vector2i(-1, 0));
  529  	for(auto it = prompts.cbegin(); it != prompts.cend(); it++)
  530  	{
  531  		if(it->first == "up/down/left/right")
  532  		{
  533  			canScrollHoriz = false;
  534  			canScrollVert = false;
  535  			break;
  536  		}else if(it->first == "up/down")
  537  		{
  538  			canScrollVert = false;
  539  		}else if(it->first == "left/right")
  540  		{
  541  			canScrollHoriz = false;
  542  		}
  543  	}
  544  
  545  	if(canScrollHoriz && canScrollVert)
  546  	  prompts.push_back(HelpPrompt("up/down/left/right", _("CHOOSE"))); 
  547  	else if(canScrollHoriz)
  548  	  prompts.push_back(HelpPrompt("left/right", _("CHOOSE"))); 
  549  	else if(canScrollVert)
  550  	  prompts.push_back(HelpPrompt("up/down", _("CHOOSE"))); 
  551  
  552  	return prompts;
  553  }
```

## ComponentGrid.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_COMPONENTS_COMPONENT_GRID_H
    3  #define ES_CORE_COMPONENTS_COMPONENT_GRID_H
    4  
    5  #include "math/Vector2i.h"
    6  #include "renderers/Renderer.h"
    7  #include "GuiComponent.h"
    8  
    9  namespace GridFlags
   10  {
   11  	enum UpdateType
   12  	{
   13  		UPDATE_ALWAYS,
   14  		UPDATE_WHEN_SELECTED,
   15  		UPDATE_NEVER
   16  	};
   17  
   18  	enum Border : unsigned int
   19  	{
   20  		BORDER_NONE = 0,
   21  
   22  		BORDER_TOP = 1,
   23  		BORDER_BOTTOM = 2,
   24  		BORDER_LEFT = 4,
   25  		BORDER_RIGHT = 8
   26  	};
   27  };
   28  
   29  // Used to arrange a bunch of components in a spreadsheet-esque grid.
   30  class ComponentGrid : public GuiComponent
   31  {
   32  public:
   33  	ComponentGrid(Window* window, const Vector2i& gridDimensions);
   34  	virtual ~ComponentGrid();
   35  
   36  	bool removeEntry(const std::shared_ptr<GuiComponent>& comp);
   37  
   38  	void setEntry(const std::shared_ptr<GuiComponent>& comp, const Vector2i& pos, bool canFocus, bool resize = true, 
   39  		const Vector2i& size = Vector2i(1, 1), unsigned int border = GridFlags::BORDER_NONE, GridFlags::UpdateType updateType = GridFlags::UPDATE_ALWAYS);
   40  
   41  	void textInput(const char* text) override;
   42  	bool input(InputConfig* config, Input input) override;
   43  	void update(int deltaTime) override;
   44  	void render(const Transform4x4f& parentTrans) override;
   45  	void onSizeChanged() override;
   46  
   47  	void resetCursor();
   48  	bool cursorValid();
   49  
   50  	float getColWidth(int col);
   51  	float getRowHeight(int row);
   52  
   53  	void setColWidthPerc(int col, float width, bool update = true); // if update is false, will not call an onSizeChanged() which triggers a (potentially costly) repositioning + resizing of every element
   54  	void setRowHeightPerc(int row, float height, bool update = true); // if update is false, will not call an onSizeChanged() which triggers a (potentially costly) repositioning + resizing of every element
   55  
   56  	void setColWidth(int col, float width, bool update = true); // if update is false, will not call an onSizeChanged() which triggers a (potentially costly) repositioning + resizing of every element
   57  	void setRowHeight(int row, float height, bool update = true); // if update is false, will not call an onSizeChanged() which triggers a (potentially costly) repositioning + resizing of every element
   58  
   59  	Vector2i getCursor();
   60  	bool moveCursor(Vector2i dir);
   61  	// Would a press in this direction move the focus? The same search
   62  	// moveCursor() runs, with nothing moved.
   63  	bool canMoveCursor(const Vector2i& dir) const;
   64  	void setCursorTo(Vector2i pos);
   65  	void setCursorTo(const std::shared_ptr<GuiComponent>& comp);
   66  	bool isCursorTo(const std::shared_ptr<GuiComponent>& comp);
   67  
   68  	inline std::shared_ptr<GuiComponent> getSelectedComponent()
   69  	{
   70  		const GridEntry* e = getCellAt(mCursor);
   71  		if(e)
   72  			return e->component;
   73  		else
   74  			return nullptr;
   75  	}
   76  
   77  	void onFocusLost() override;
   78  	void onFocusGained() override;
   79  
   80  	virtual std::vector<HelpPrompt> getHelpPrompts() override;
   81  
   82  	void setSeparatorColor(unsigned int separatorColor) { mSeparatorColor = separatorColor; updateSeparators(); }
   83  	inline void setUnhandledInputCallback(const std::function<bool(InputConfig* config, Input input)>& func) { mUnhandledInputCallback = func; }
   84  
   85  	Vector2i getGridSize() { return mGridSize; }
   86  
   87  private:
   88  	class GridEntry
   89  	{
   90  	public:
   91  		Vector2i pos;
   92  		Vector2i dim;
   93  		std::shared_ptr<GuiComponent> component;
   94  		bool canFocus;
   95  		bool resize;
   96  		GridFlags::UpdateType updateType;
   97  		unsigned int border;
   98  
   99  		GridEntry(const Vector2i& p = Vector2i::Zero(), const Vector2i& d = Vector2i::Zero(),
  100  			const std::shared_ptr<GuiComponent>& cmp = nullptr, bool f = false, bool r = true, 
  101  			GridFlags::UpdateType u = GridFlags::UPDATE_ALWAYS, unsigned int b = GridFlags::BORDER_NONE) : 
  102  			pos(p), dim(d), component(cmp), canFocus(f), resize(r), updateType(u), border(b)
  103  		{};
  104  
  105  		operator bool() const
  106  		{
  107  			return component != NULL;
  108  		}
  109  	};
  110  
  111  	class GridSizeInfo
  112  	{
  113  	public:
  114  		GridSizeInfo()
  115  		{
  116  			value = 0.f;
  117  			absolute = false;
  118  		}
  119  
  120  		float value;
  121  		bool absolute;
  122  
  123  		float compute(const float& size) { return absolute ? value : value * size; }
  124  	};
  125  
  126  	std::vector<GridSizeInfo*> mRowHeights;
  127  	std::vector<GridSizeInfo*> mColWidths;
  128  	
  129  	std::vector<Renderer::Vertex> mLines;
  130  
  131  	unsigned int mSeparatorColor;
  132  
  133  	// Update position & size
  134  	void updateCellComponent(const GridEntry& cell);
  135  	void updateSeparators();
  136  
  137  	const GridEntry* getCellAt(int x, int y) const;
  138  	inline const GridEntry* getCellAt(const Vector2i& pos) const { return getCellAt(pos.x(), pos.y()); }
  139  	
  140  	Vector2i mGridSize;
  141  
  142  	std::vector<GridEntry> mCells;
  143  
  144  	void onCursorMoved(Vector2i from, Vector2i to);
  145  	Vector2i mCursor;
  146  
  147  	std::function<bool(InputConfig* config, Input input)> mUnhandledInputCallback;
  148  };
  149  
  150  #endif // ES_CORE_COMPONENTS_COMPONENT_GRID_H
```

## ComponentList.cpp (whole, fork-modified, at the pin)

```text
    1  #include "components/ComponentList.h"
    2  #include "LocaleES.h"
    3  #include "TextToSpeech.h"
    4  
    5  #include "components/TextComponent.h"
    6  #include "components/SwitchComponent.h"
    7  #include "components/SliderComponent.h"
    8  #include "components/OptionListComponent.h"
    9  #include "InputManager.h"
   10  
   11  #define TOTAL_HORIZONTAL_PADDING_PX 20
   12  
   13  ComponentList::ComponentList(Window* window) : IList<ComponentListRow, std::string>(window, LIST_SCROLL_STYLE_SLOW, LIST_NEVER_LOOP), mScrollbar(window)
   14  {
   15  	mHotRow = -1;
   16  	mPressedRow = -1;
   17  	mPressedPoint = Vector2i(-1, -1);
   18  	mIsDragging = false;
   19  
   20  	mSelectorBarOffset = 0;
   21  	mCameraOffset = 0;
   22  	mFocused = false;
   23  	mOldCursor = -1; 
   24  	mReadOnly = false;
   25  
   26  	mScrollbar.loadFromMenuTheme();	
   27  }
   28  
   29  void ComponentList::addRow(const ComponentListRow& row, bool setCursorHere, bool updateSize, const std::string& userData)
   30  {
   31  	IList<ComponentListRow, std::string>::Entry e;
   32  	e.name = "";
   33  	e.object = userData;
   34  	e.data = row;
   35  
   36  	this->add(e);
   37  
   38  	ComponentListRow& data = mEntries.back().data;
   39  
   40  	for(auto it = data.elements.cbegin(); it != data.elements.cend(); it++)
   41  		addChild(it->component.get());
   42  
   43  	if (updateSize)
   44  	{
   45  		updateElementSize(data);
   46  		updateElementPosition(data);
   47  	}
   48  
   49  	// Fix group initial cursor position
   50  	if (mCursor == 0 && mEntries.size() == 2 && !mEntries[0].data.selectable)
   51  		setCursorHere = true;
   52  
   53  	if(setCursorHere)
   54  	{
   55  		mCursor = (int)mEntries.size() - 1;
   56  		onCursorChanged(CURSOR_STOPPED);
   57  	}
   58  	else if (mFocused && mCursor == 0 && mEntries.size() == 1)
   59  		onCursorChanged(CURSOR_STOPPED);
   60  }
   61  
   62  void ComponentList::removeLastRowIfGroup()
   63  {
   64  	int index = mEntries.size() - 1;
   65  	if (index < 0)
   66  		return;
   67  
   68  	if (mEntries.at(index).data.group)
   69  		mEntries.erase(mEntries.begin() + index);
   70  }
   71  
   72  void ComponentList::addGroup(const std::string& label, bool forceVisible)
   73  {	
   74  	auto theme = ThemeData::getMenuTheme();
   75  	if (!forceVisible && !theme->Group.visible)
   76  		return;
   77  
   78  	ComponentListRow row;
   79  
   80  	auto group = std::make_shared<TextComponent>(mWindow, label, theme->Group.font, theme->Group.color);
   81  
   82  	if (EsLocale::isRTL() && ((Alignment)theme->Group.alignment) == Alignment::ALIGN_LEFT)
   83  		group->setHorizontalAlignment(Alignment::ALIGN_RIGHT);
   84  	else
   85  		group->setHorizontalAlignment((Alignment) theme->Group.alignment);
   86  
   87  	group->setBackgroundColor(theme->Group.backgroundColor); // 0x00000010	
   88  	if (theme->Group.backgroundColor != 0)
   89  		group->setRenderBackground(true);
   90  
   91  	group->setLineSpacing(theme->Group.lineSpacing);
   92  	group->setPadding(Vector4f(TOTAL_HORIZONTAL_PADDING_PX / 2, 0, TOTAL_HORIZONTAL_PADDING_PX / 2, 0));
   93  
   94  	row.addElement(group, true);
   95  	row.selectable = false;
   96  	row.group = true;
   97  	addRow(row);
   98  }
   99  
  100  void ComponentList::onSizeChanged()
  101  {
  102  	IList::onSizeChanged();
  103  
  104  	float yOffset = 0;
  105  	for(auto it = mEntries.cbegin(); it != mEntries.cend(); it++)
  106  	{
  107  		updateElementSize(it->data);
  108  		updateElementPosition(it->data, yOffset);
  109  		yOffset += getRowHeight(it->data);
  110  	}
  111  
  112  	updateCameraOffset();
  113  }
  114  
  115  void ComponentList::onFocusLost()
  116  {
  117  	mFocused = false;
  118  
  119  	if (size())
  120  	{
  121  		for (auto it = mEntries.cbegin(); it != mEntries.cend(); it++)
  122  			for (auto elt : it->data.elements)
  123  				elt.component->onFocusLost();
  124  	}
  125  }
  126  
  127  void ComponentList::onFocusGained()
  128  {
  129  	mFocused = true;
  130  
  131  	if (size())
  132  	{
  133  		for (auto it = mEntries.cbegin(); it != mEntries.cend(); it++)
  134  			for (auto elt : it->data.elements)
  135  				elt.component->onFocusLost();
  136  
  137  		for (auto elt : mEntries.at(mCursor).data.elements)
  138  			elt.component->onFocusGained();
  139  	}
  140  }
  141  
  142  bool ComponentList::input(InputConfig* config, Input input)
  143  {
  144  	if (mReadOnly || size() == 0)
  145  		return false;
  146  
  147  	// give it to the current row's input handler
  148  	if(mEntries.at(mCursor).data.input_handler)
  149  	{
  150  		if(mEntries.at(mCursor).data.input_handler(config, input))
  151  			return true;
  152  	}else{
  153  		// no input handler assigned, do the default, which is to give it to the rightmost element in the row
  154  		auto& row = mEntries.at(mCursor).data;
  155  		if(row.elements.size())
  156  		{
  157  			if (EsLocale::isRTL())
  158  			{
  159  				if (row.elements.front().component->input(config, input))
  160  					return true;
  161  			}
  162  			else
  163  			{
  164  				if (row.elements.back().component->input(config, input))
  165  					return true;
  166  			}
  167  		}
  168  	}
  169  
  170  	// input handler didn't consume the input - try to scroll
  171  	if(config->isMappedLike("up", input))
  172  	{
  173  		return listInput(input.value != 0 ? -1 : 0);
  174  	}else if(config->isMappedLike("down", input))
  175  	{
  176  		return listInput(input.value != 0 ? 1 : 0);
  177  
  178  	}else if(config->isMappedTo("leftshoulder", input))
  179  	{
  180  		return listInput(input.value != 0 ? -6 : 0);
  181  	}else if(config->isMappedTo("rightshoulder", input)){
  182  		return listInput(input.value != 0 ? 6 : 0);
  183  	}
  184  
  185  	return false;
  186  }
  187  
  188  void ComponentList::update(int deltaTime)
  189  {
  190  	mScrollbar.update(deltaTime);
  191  
  192  	listUpdate(deltaTime);
  193  
  194  	if(size())
  195  	{
  196  		if (mUpdateType == ComponentListFlags::UpdateType::UPDATE_ALWAYS)
  197  		{
  198  			for (auto& entry : mEntries)
  199  				for (auto it = entry.data.elements.cbegin(); it != entry.data.elements.cend(); it++)
  200  					it->component->update(deltaTime);
  201  		}
  202  		else if (mUpdateType == ComponentListFlags::UpdateType::UPDATE_WHEN_SELECTED)
  203  		{
  204  			// update our currently selected row
  205  			for (auto it = mEntries.at(mCursor).data.elements.cbegin(); it != mEntries.at(mCursor).data.elements.cend(); it++)
  206  				it->component->update(deltaTime);
  207  		}
  208  	}
  209  }
  210  
  211  void ComponentList::onCursorChanged(const CursorState& state)
  212  {
  213  	mScrollbar.onCursorChanged();
  214  
  215  	// update the selector bar position
  216  	// in the future this might be animated
  217  	mSelectorBarOffset = 0;
  218  	for (int i = 0; i < mCursor; i++)
  219  		mSelectorBarOffset += getRowHeight(mEntries.at(i).data);
  220  
  221  	updateCameraOffset();
  222  
  223  	// this is terribly inefficient but we don't know what we came from so...
  224  	if (mFocused && mCursor >= 0 && mCursor < size())
  225  	{
  226  		for (auto it = mEntries.cbegin(); it != mEntries.cend(); it++)
  227  			for (auto elt : it->data.elements)
  228  				elt.component->onFocusLost();
  229  
  230  		for (auto elt : mEntries.at(mCursor).data.elements)
  231  			elt.component->onFocusGained();
  232  	}
  233  
  234  	if (mCursorChangedCallback)
  235  		mCursorChangedCallback(state);
  236  
  237  	updateHelpPrompts();
  238  
  239  	// tts
  240  	if (state == CURSOR_STOPPED && mOldCursor != mCursor)
  241  		saySelectedLine();
  242  }
  243  
  244  void ComponentList::saySelectedLine()
  245  {
  246  	if (mReadOnly)
  247  		return;
  248  
  249  	int n = 0;
  250  
  251  	if (!(mCursor >= 0 && mCursor < mEntries.size())) 
  252  		return;
  253  
  254  	mOldCursor = mCursor;
  255  	for (auto& element : mEntries.at(mCursor).data.elements)
  256  	{
  257  		if (element.component->isKindOf<TextComponent>())
  258  		{
  259  			TextToSpeech::getInstance()->say(element.component->getValue(), n > 0);
  260  			n++;
  261  		}
  262  		if (element.component->isKindOf<SliderComponent>())
  263  		{
  264  			SliderComponent* slider = dynamic_cast<SliderComponent*>(element.component.get());
  265  			if (slider == nullptr)
  266  				continue;
  267  
  268  			float v = slider->getValue();
  269  			char strval[32];
  270  			snprintf(strval, 32, "%.0f", v);
  271  			TextToSpeech::getInstance()->say(std::string(strval) + _(slider->getSuffix().c_str()), n > 0);
  272  			n++;
  273  		}
  274  		if (element.component->isKindOf<SwitchComponent>())
  275  		{
  276  			TextToSpeech::getInstance()->say(((SwitchComponent*)element.component.get())->getState() ? _("ENABLED") : _("DISABLED"), n > 0);
  277  			n++;
  278  		}
  279  		if (element.component->isKindOf<OptionListComponent<std::string>>())
  280  		{
  281  			OptionListComponent<std::string>* optionList = dynamic_cast<OptionListComponent<std::string>*>(element.component.get());
  282  			if (optionList == nullptr)
  283  				continue;
  284  
  285  			if (optionList->IsMultiSelect())
  286  				TextToSpeech::getInstance()->say(Utils::String::join(optionList->getSelectedObjects(), ", "));
  287  			else
  288  				TextToSpeech::getInstance()->say(optionList->getSelectedName(), n > 0);
  289  
  290  			n++;
  291  		}
  292  	}
  293  }
  294  
  295  void ComponentList::updateCameraOffset()
  296  {
  297  	// move the camera to scroll
  298  	const float totalHeight = getTotalRowHeight();
  299  	if(totalHeight > mSize.y() && mCursor < mEntries.size())
  300  	{
  301  		float target = mSelectorBarOffset + getRowHeight(mEntries.at(mCursor).data)/2 - (mSize.y() / 2);
  302  
  303  		// clamp it
  304  		mCameraOffset = 0;
  305  		unsigned int i = 0;
  306  		while(mCameraOffset < target && i < mEntries.size())
  307  		{
  308  			mCameraOffset += getRowHeight(mEntries.at(i).data);
  309  			i++;
  310  		}
  311  
  312  		if(mCameraOffset < 0)
  313  			mCameraOffset = 0;
  314  		else if(mCameraOffset + mSize.y() > totalHeight)
  315  			mCameraOffset = totalHeight - mSize.y();
  316  	}
  317  	else
  318  		mCameraOffset = 0;
  319  }
  320  
  321  void ComponentList::render(const Transform4x4f& parentTrans)
  322  {
  323  	if (!size())
  324  		return;
  325  
  326  	float opacity = getOpacity() / 255.0;
  327  	auto menuTheme = ThemeData::getMenuTheme();
  328  	unsigned int selectorColor = menuTheme->Text.selectorColor;
  329  	unsigned int selectorGradientColor = menuTheme->Text.selectorGradientColor;
  330  	unsigned int selectedColor = menuTheme->Text.selectedColor;
  331  	unsigned int bgColor = menuTheme->Background.color;
  332  	unsigned int separatorColor = menuTheme->Text.separatorColor;
  333  	unsigned int textColor = menuTheme->Text.color;
  334  	bool selectorGradientHorz = menuTheme->Text.selectorGradientType;
  335  
  336  	Transform4x4f trans = parentTrans * getTransform();
  337  
  338  	// clip everything to be inside our bounds
  339  	Vector3f dim(mSize.x(), mSize.y(), 0);
  340  	dim = trans * dim - trans.translation();
  341  
  342  	Renderer::pushClipRect(trans.translation().x(), trans.translation().y(), Math::round(dim.x()), Math::round(dim.y() + 1));
  343  
  344  	// scroll the camera
  345  	trans.translate(Vector3f(0, -Math::round(mCameraOffset), 0));
  346  
  347  	float y = 0;
  348  
  349  	std::vector<float> rowHeights(mEntries.size(), -1.0f);
  350  	std::vector<GuiComponent*> drawAfterCursor;
  351  
  352  	for (unsigned int i = 0; i < mEntries.size(); i++)
  353  	{
  354  		auto& entry = mEntries.at(i);
  355  
  356  		float rowHeight = getRowHeight(entry.data);
  357  		rowHeights[i] = rowHeight;
  358  
  359  		if (y - mCameraOffset + rowHeight >= 0)
  360  		{
  361  			if (!mReadOnly && mFocused && entry.data.selectable && i == mCursor)
  362  			{
  363  				Renderer::setMatrix(trans);
  364  
  365  				if (selectorColor != bgColor && (selectorColor & 0xFF) != 0)
  366  				{
  367  					Renderer::setMatrix(trans);
  368  					Renderer::drawRect(0.0f, mSelectorBarOffset, mSize.x(), rowHeight,
  369  						selectorColor & 0xFFFFFF00 | (unsigned char)((selectorColor & 0xFF) * opacity),
  370  						selectorGradientColor & 0xFFFFFF00 | (unsigned char)((selectorGradientColor & 0xFF) * opacity),
  371  						selectorGradientHorz);
  372  				}
  373  			}
  374  
  375  			if (!mReadOnly && i == mHotRow)
  376  			{
  377  				Renderer::setMatrix(trans);
  378  
  379  				float hotOpacity = 0.1f;
  380  				Renderer::drawRect(0.0f, y, mSize.x(), rowHeight,
  381  					selectorColor & 0xFFFFFF00 | (unsigned char)((selectorColor & 0xFF) * opacity * hotOpacity),
  382  					selectorGradientColor & 0xFFFFFF00 | (unsigned char)((selectorGradientColor & 0xFF) * opacity * hotOpacity),
  383  					selectorGradientHorz);
  384  
  385  			//	Renderer::drawRect(0.0f, y, mSize.x(), rowHeight, 0x00000010, 0x00000010);
  386  			}
  387  
  388  			for (auto& element : entry.data.elements)
  389  			{				
  390  				if (!mReadOnly && Settings::DebugMouse() && i == mHotRow)
  391  					element.component->setColor(0xFFFF00FF);
  392  				else 
  393  				if (entry.data.group)
  394  					element.component->setColor(menuTheme->Group.color);
  395  				else
  396  				{
  397  					if (!mReadOnly && entry.data.selectable && mFocused && i == mCursor)
  398  						element.component->setColor(selectedColor);
  399  					else
  400  						element.component->setColor(textColor);
  401  				}
  402  					
  403  				if (element.component->isKindOf<TextComponent>())
  404  					drawAfterCursor.push_back(element.component.get());
  405  				else
  406  					element.component->render(trans);
  407  			}
  408  		}
  409  		
  410  		y += rowHeight;
  411  		if (y - mCameraOffset > mSize.y())
  412  			break;
  413  	}
  414  
  415  	for (auto it : drawAfterCursor)
  416  		it->render(trans);
  417  
  418  	// draw separators
  419  	if (separatorColor != 0 ||  menuTheme->Group.separatorColor != 0)
  420  	{		
  421  		Renderer::setMatrix(trans);
  422  
  423  		bool prevIsGroup = false;
  424  
  425  		y = 0;
  426  		for (unsigned int i = 0; i < mEntries.size(); i++)
  427  		{
  428  			auto height = rowHeights[i];
  429  			if (height >= 0)
  430  			{
  431  				if (y - mCameraOffset + height >= 0)
  432  				{
  433  					if (prevIsGroup && menuTheme->Group.separatorColor != separatorColor)
  434  						Renderer::drawRect(0.0f, y - 2.0f, mSize.x(), 1.0f, menuTheme->Group.separatorColor & 0xFFFFFF00 | (unsigned char)((menuTheme->Group.separatorColor & 0xFF) * opacity));
  435  					else if (separatorColor != 0)
  436  						Renderer::drawRect(0.0f, y, mSize.x(), 1.0f, separatorColor & 0xFFFFFF00 | (unsigned char)((separatorColor & 0xFF) * opacity));
  437  				}
  438  
  439  				y += height; // getRowHeight(mEntries.at(i).data);
  440  				if (y - mCameraOffset > mSize.y())
  441  					break;
  442  			}
  443  
  444  			prevIsGroup = mEntries[i].data.group;
  445  		}
  446  
  447  		Renderer::drawRect(0.0f, y, mSize.x(), 1.0f, separatorColor & 0xFFFFFF00 | (unsigned char)((separatorColor & 0xFF) * opacity));
  448  	}
  449  
  450  	Renderer::popClipRect();
  451  
  452  	if (mScrollbar.isEnabled() && mEntries.size() > 0)
  453  	{
  454  		mScrollbar.setContainerBounds(getPosition(), getSize());
  455  		mScrollbar.setRange(0, getTotalRowHeight(), mSize.y());
  456  		mScrollbar.setScrollPosition(mCameraOffset);
  457  		mScrollbar.render(parentTrans);
  458  	}
  459  }
  460  
  461  float ComponentList::getRowHeight(const ComponentListRow& row) const
  462  {
  463  	int sz = row.elements.size();
  464  	if (sz == 0)
  465  		return 0;
  466  	else if (sz == 1)
  467  		return row.elements[0].component->getSize().y();
  468  
  469  	// returns the highest component height found in the row
  470  	float height = 0;
  471  
  472  	for(auto& elem : row.elements)
  473  	{
  474  		float h = elem.component->getSize().y();
  475  		if (h > height)
  476  			height = h;
  477  	}
  478  
  479  	return height;
  480  }
  481  
  482  float ComponentList::getTotalRowHeight() const
  483  {
  484  	float height = 0;
  485  	for(auto it = mEntries.cbegin(); it != mEntries.cend(); it++)
  486  		height += getRowHeight(it->data);
  487  
  488  	return height;
  489  }
  490  
  491  float ComponentList::rowInset()
  492  {
  493  	return TOTAL_HORIZONTAL_PADDING_PX / 2;
  494  }
  495  
  496  void ComponentList::updateElementPosition(const ComponentListRow& row, float yOffset)
  497  {
  498  	if (yOffset < 0)
  499  	{
  500  		yOffset = 0;
  501  		for (auto it = mEntries.cbegin(); it != mEntries.cend() && &it->data != &row; it++)
  502  			yOffset += getRowHeight(it->data);
  503  	}
  504  
  505  	// assumes updateElementSize has already been called
  506  	float rowHeight = getRowHeight(row);
  507  
  508  	float x = row.selectable ? TOTAL_HORIZONTAL_PADDING_PX / 2 : 0;
  509  	for(unsigned int i = 0; i < row.elements.size(); i++)
  510  	{
  511  		const auto comp = row.elements.at(i).component;
  512  		
  513  		// center vertically
  514  		comp->setPosition(x, (rowHeight - comp->getSize().y()) / 2 + yOffset);
  515  		x += comp->getSize().x();
  516  	}
  517  }
  518  
  519  void ComponentList::updateElementSize(const ComponentListRow& row)
  520  {
  521  	float width = mSize.x() - (row.selectable ? TOTAL_HORIZONTAL_PADDING_PX : 0);
  522  	std::vector< std::shared_ptr<GuiComponent> > resizeVec;
  523  
  524  	for(auto it = row.elements.cbegin(); it != row.elements.cend(); it++)
  525  	{
  526  		if(it->resize_width)
  527  			resizeVec.push_back(it->component);
  528  		else
  529  			width -= it->component->getSize().x();
  530  	}
  531  
  532  	// redistribute the "unused" width equally among the components with resize_width set to true
  533  	width = width / resizeVec.size();
  534  	for(auto it = resizeVec.cbegin(); it != resizeVec.cend(); it++)
  535  	{
  536  		(*it)->setSize(width, (*it)->getSize().y());
  537  	}
  538  }
  539  
  540  void ComponentList::textInput(const char* text)
  541  {
  542  	if(!size())
  543  		return;
  544  
  545  	mEntries.at(mCursor).data.elements.back().component->textInput(text);
  546  }
  547  
  548  std::vector<HelpPrompt> ComponentList::getHelpPrompts()
  549  {
  550  	if(!size())
  551  		return std::vector<HelpPrompt>();
  552  
  553  	std::vector<HelpPrompt> prompts = mEntries.at(mCursor).data.elements.back().component->getHelpPrompts();
  554  
  555  	if(size() > 1)
  556  	{
  557  		bool addMovePrompt = true;
  558  		for(auto it = prompts.cbegin(); it != prompts.cend(); it++)
  559  		{
  560  			if(it->first == "up/down" || it->first == "up/down/left/right")
  561  			{
  562  				addMovePrompt = false;
  563  				break;
  564  			}
  565  		}
  566  
  567  		if(addMovePrompt)
  568  			prompts.push_back(HelpPrompt(_("up/down"), _("CHOOSE")));
  569  	}
  570  
  571  	return prompts;
  572  }
  573  
  574  bool ComponentList::moveCursor(int amt)
  575  {
  576  	bool ret = listInput(amt);
  577  	listInput(0);
  578  	return ret;
  579  }
  580  
  581  std::string ComponentList::getSelectedUserData()
  582  {
  583  	if (mCursor >= 0 && mCursor < mEntries.size())
  584  		return mEntries[mCursor].object;
  585  
  586  	return "";
  587  }
  588  
  589  bool ComponentList::hitTest(int x, int y, Transform4x4f& parentTransform, std::vector<GuiComponent*>* pResult)
  590  {
  591  	Transform4x4f trans = parentTransform * getTransform();
  592  
  593  	bool ret = false;
  594  
  595  	mHotRow = -1;
  596  		
  597  	auto rect = Renderer::getScreenRect(trans, getSize(), true);
  598  	if (x != -1 && y != -1 && rect.contains(x, y))
  599  	{
  600  		ret = true;
  601  
  602  		Transform4x4f ti = trans;
  603  		ti.translate(0, -mCameraOffset);
  604  
  605  		float ry = 0;
  606  
  607  		for (unsigned int i = 0; i < mEntries.size(); i++)
  608  		{
  609  			auto& entry = mEntries.at(i);
  610  			float rowHeight = getRowHeight(entry.data);
  611  
  612  			if (entry.data.selectable && ry - mCameraOffset + rowHeight >= 0)
  613  			{
  614  				rect = Renderer::getScreenRect(ti, Vector2f(getSize().x(), rowHeight), true);
  615  				if (rect.contains(x, y))
  616  				{
  617  					mHotRow = i;
  618  					break;
  619  				}
  620  			}
  621  
  622  			ti.translate(0, rowHeight);
  623  			ry += rowHeight;
  624  			if (ry - mCameraOffset > mSize.y())
  625  				break;
  626  		}
  627  
  628  		if (pResult != nullptr)
  629  			pResult->push_back(this);
  630  	}
  631  
  632  	trans.translate(0, -mCameraOffset);
  633  
  634  	for (int i = 0; i < getChildCount(); i++)
  635  		ret |= getChild(i)->hitTest(x, y, trans, pResult);
  636  
  637  	return ret;
  638  }
  639  
  640  bool ComponentList::onMouseClick(int button, bool pressed, int x, int y)
  641  {
  642  	if (button == 1)
  643  	{
  644  		if (pressed)
  645  		{
  646  			if (mHotRow >= 0)
  647  			{
  648  				float camOffset = mCameraOffset;
  649  				mCursor = mHotRow;
  650  				onCursorChanged(CURSOR_STOPPED);
  651  				mCameraOffset = camOffset;
  652  				mPressedRow = mHotRow;
  653  			}
  654  
  655  			mIsDragging = false;
  656  			mPressedPoint = Vector2i(x, y);
  657  			mWindow->setMouseCapture(this);
  658  		}
  659  		else if (mWindow->hasMouseCapture(this))
  660  		{
  661  			mWindow->releaseMouseCapture();
  662  
  663  			auto row = mPressedRow;
  664  			mPressedRow = -1;
  665  			mPressedPoint = Vector2i(-1, -1);
  666  
  667  			auto dragging = mIsDragging;
  668  			mIsDragging = false;
  669  
  670  			if (!dragging && row == mHotRow && mCursor == row)
  671  				InputManager::getInstance()->sendMouseClick(mWindow, 1);				
  672  		}
  673  
  674  		return true;
  675  	}
  676  
  677  	return false;
  678  }
  679  
  680  void ComponentList::onMouseMove(int x, int y)
  681  {
  682  	if (mPressedPoint.x() != -1 && mPressedPoint.y() != -1 && mWindow->hasMouseCapture(this))
  683  	{
  684  		mIsDragging = true;
  685  		mHotRow = -1;
  686  
  687  		float yOffset = 0;
  688  		for (auto entry : mEntries)
  689  			yOffset += getRowHeight(entry.data);
  690  
  691  		yOffset -= getSize().y();
  692  		if (yOffset <= 0)
  693  			return;
  694  
  695  		mCameraOffset += mPressedPoint.y() - y;
  696  
  697  		if (mCameraOffset < 0 )
  698  			mCameraOffset = 0;
  699  
  700  		if (mCameraOffset > yOffset)
  701  			mCameraOffset = yOffset;
  702  
  703  		mPressedPoint = Vector2i(x, y);
  704  	}
  705  }
  706  
  707  bool ComponentList::onMouseWheel(int delta)
  708  {
  709  	int newCursor = mCursor - delta;
  710  	
  711  	if (newCursor < 0)
  712  		newCursor = 0;
  713  
  714  	if (newCursor >= mEntries.size())
  715  		newCursor = mEntries.size() - 1;
  716  
  717  	while (newCursor >= 0 && newCursor < mEntries.size() && !mEntries[newCursor].data.selectable)
  718  		newCursor += delta > 0 ? -1 : 1;
  719  
  720  	if (newCursor >= 0 && newCursor < mEntries.size() && newCursor != mCursor)
  721  	{
  722  		mCursor = newCursor;
  723  		onCursorChanged(CURSOR_STOPPED);
  724  	}
  725  
  726  	return true;
  727  }
  728  
```

## ComponentList.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_COMPONENTS_COMPONENT_LIST_H
    3  #define ES_CORE_COMPONENTS_COMPONENT_LIST_H
    4  
    5  #include "IList.h"
    6  #include "LocaleES.h"
    7  #include "components/ScrollbarComponent.h"
    8  #include "math/Vector2i.h"
    9  
   10  namespace ComponentListFlags
   11  {
   12  	enum UpdateType
   13  	{
   14  		UPDATE_ALWAYS,
   15  		UPDATE_WHEN_SELECTED,
   16  		UPDATE_NEVER
   17  	};
   18  
   19  	// A row that cannot act yet is dimmed, not hidden (es-ui-style-guide.md):
   20  	// the theme's colour at this alpha. ComponentList::render sets every
   21  	// element's colour from the theme every frame, so a dim that is to last
   22  	// is applied inside the element's own setColor -- MultiLineMenuEntry and
   23  	// SwitchComponent carry setDimmed for it -- and never once at
   24  	// construction, which the first frame undoes (fork #182).
   25  	const unsigned char DIMMED_ALPHA = 0x50;
   26  	inline unsigned int dimmed(unsigned int color) { return (color & 0xFFFFFF00) | DIMMED_ALPHA; }
   27  };
   28  
   29  struct ComponentListElement
   30  {
   31  	ComponentListElement(const std::shared_ptr<GuiComponent>& cmp = nullptr, bool resize_w = true)
   32  		: component(cmp), resize_width(resize_w) { };
   33  
   34  	std::shared_ptr<GuiComponent> component;
   35  	bool resize_width;	
   36  };
   37  
   38  struct ComponentListRow
   39  {
   40  	ComponentListRow() 
   41  	{
   42  		selectable = true;
   43  		group = false;
   44  	};
   45  
   46  	bool group;
   47  	bool selectable;
   48  	std::vector<ComponentListElement> elements;
   49  
   50  	// The input handler is called when the user enters any input while this row is highlighted (including up/down).
   51  	// Return false to let the list try to use it or true if the input has been consumed.
   52  	// If no input handler is supplied (input_handler == nullptr), the default behavior is to forward the input to 
   53  	// the rightmost element in the currently selected row.
   54  	std::function<bool(InputConfig*, Input)> input_handler;
   55  	
   56  	inline void addElement(const std::shared_ptr<GuiComponent>& component, bool resize_width)
   57  	{
   58  		if (EsLocale::isRTL())
   59  			elements.insert(elements.begin(), ComponentListElement(component, resize_width));
   60  		else
   61  			elements.push_back(ComponentListElement(component, resize_width));
   62  	}
   63  
   64  	// Utility method for making an input handler for "when the users presses A on this, do func."
   65  	inline void makeAcceptInputHandler(const std::function<void()>& func, bool onButtonRelease = false)
   66  	{
   67  		if (func == nullptr)
   68  			return;
   69  
   70  		input_handler = [func, onButtonRelease](InputConfig* config, Input input) -> bool 
   71  		{
   72  			if(config->isMappedTo(BUTTON_OK, input) && (onButtonRelease ? input.value == 0 : input.value != 0)) 
   73  			{
   74  				func();
   75  				return true;
   76  			}
   77  			return false;
   78  		};
   79  	}
   80  };
   81  
   82  class ComponentList : public IList<ComponentListRow, std::string>
   83  {
   84  public:
   85  	ComponentList(Window* window);
   86  
   87  	void addRow(const ComponentListRow& row, bool setCursorHere = false, bool updateSize = true, const std::string& userData = "");
   88  	void addGroup(const std::string& label, bool forceVisible = false);
   89  	void removeLastRowIfGroup();
   90  
   91  	void textInput(const char* text) override;
   92  	bool input(InputConfig* config, Input input) override;
   93  	void update(int deltaTime) override;
   94  	void render(const Transform4x4f& parentTrans) override;
   95  	virtual std::vector<HelpPrompt> getHelpPrompts() override;
   96  
   97  	void onSizeChanged() override;
   98  	void onFocusGained() override;
   99  	void onFocusLost() override;
  100  
  101  	void setUpdateType(ComponentListFlags::UpdateType updateType) { mUpdateType = updateType;  }
  102  
  103  	bool moveCursor(int amt);
  104  	inline int getCursorId() const { return mCursor; }
  105  
  106  	std::string getSelectedUserData();
  107  	
  108  	float getTotalRowHeight() const;
  109  
  110  	// The inset a selectable row's elements are laid out with, on each
  111  	// side. A row that is not selectable gets none and pads itself, as
  112  	// addGroup's header does (updateElementPosition, updateElementSize).
  113  	static float rowInset();
  114  	inline float getRowHeight(int row) const { return getRowHeight(mEntries.at(row).data); }
  115  
  116  	inline void setCursorChangedCallback(const std::function<void(CursorState state)>& callback) { mCursorChangedCallback = callback; };
  117  	inline const std::function<void(CursorState state)>& getCursorChangedCallback() const { return mCursorChangedCallback; };
  118  
  119  	void saySelectedLine();
  120  
  121  	virtual bool onMouseClick(int button, bool pressed, int x, int y) override;
  122  	virtual void onMouseMove(int x, int y) override;
  123  	virtual bool onMouseWheel(int delta) override;
  124  	virtual bool hitTest(int x, int y, Transform4x4f& parentTransform, std::vector<GuiComponent*>* pResult = nullptr) override;
  125  
  126  	inline void setReadOnly(bool value) { mReadOnly = value; }
  127  
  128  protected:
  129  	void onCursorChanged(const CursorState& state) override;
  130  
  131  	virtual int onBeforeScroll(int cursor, int direction) override
  132  	{ 
  133  		int looped = cursor;
  134  		while (cursor >= 0 && cursor < mEntries.size() && !mEntries[cursor].data.selectable)
  135  		{
  136  			cursor += direction;
  137  			if (cursor == looped || cursor < 0 || cursor >= mEntries.size())
  138  				return mCursor;
  139  		}
  140  		
  141  		return cursor; 
  142  	}
  143  
  144  private:
  145  	bool mFocused;
  146  	int mOldCursor;
  147  
  148  	void updateCameraOffset();
  149  	void updateElementPosition(const ComponentListRow& row, float yOffset = -1.0);
  150  	void updateElementSize(const ComponentListRow& row);
  151  	
  152  	float getRowHeight(const ComponentListRow& row) const;
  153  
  154  	float mSelectorBarOffset;
  155  	float mCameraOffset;
  156  
  157  	ComponentListFlags::UpdateType mUpdateType;
  158  
  159  	std::function<void(CursorState state)> mCursorChangedCallback;
  160  
  161  	ScrollbarComponent mScrollbar;
  162  	int		  mHotRow;
  163  	int		  mPressedRow;
  164  	Vector2i  mPressedPoint;
  165  	bool	  mIsDragging;
  166  	bool	  mReadOnly;
  167  };
  168  
  169  #endif // ES_CORE_COMPONENTS_COMPONENT_LIST_H
```

## ComponentTab.cpp (whole, fork-modified, at the pin)

```text
    1  #include "components/ComponentTab.h"
    2  #include "components/TextComponent.h"
    3  #include "Window.h"
    4  #include "InputManager.h"
    5  #include "LocaleES.h"
    6  
    7  #define PADDING_PX (Renderer::getScreenWidth() * 0.015f)
    8  #define SELECTOR_PX (Renderer::getScreenWidth() * 0.0025f)
    9  
   10  ComponentTab::ComponentTab(Window* window) : IList<ComponentTabItem, std::string>(window, LIST_SCROLL_STYLE_SLOW, LIST_NEVER_LOOP)
   11  {
   12  	mHotTab = -1;
   13  	mPressedTab = -1;
   14  
   15  	mSelectorBarOffset = 0;
   16  	mCameraOffset = 0;
   17  	mFocused = false;
   18  }
   19  
   20  void ComponentTab::addTab(const std::string label, const std::string value, bool setCursorHere)
   21  {
   22  	auto theme = ThemeData::getMenuTheme();
   23  
   24  	ComponentTabItem tab;
   25  	auto grid = std::make_shared<TextComponent>(mWindow, label, theme->Text.font, theme->Text.color, ALIGN_CENTER);
   26  	grid->setPadding(Vector4f(PADDING_PX, 0, PADDING_PX, 0));
   27  	tab.addElement(grid, true);
   28  	
   29  	addTab(tab, value.empty() ? label : value, setCursorHere);
   30  }
   31  
   32  void ComponentTab::addTab(const ComponentTabItem& row, const std::string value, bool setCursorHere)
   33  {
   34  	IList<ComponentTabItem, std::string>::Entry e;
   35  	e.name = "";
   36  	e.object = value;
   37  	e.data = row;
   38  
   39  	this->add(e);
   40  
   41  	for(auto it = mEntries.back().data.elements.cbegin(); it != mEntries.back().data.elements.cend(); it++)
   42  		addChild(it->component.get());
   43  
   44  	updateElementSize(mEntries.back().data);
   45  	updateElementPosition(mEntries.back().data);
   46  
   47  	if(setCursorHere)
   48  	{
   49  		mCursor = (int)mEntries.size() - 1;
   50  		onCursorChanged(CURSOR_STOPPED);
   51  	}
   52  }
   53  
   54  void ComponentTab::onSizeChanged()
   55  {
   56  	IList::onSizeChanged();
   57  
   58  	for(auto it = mEntries.cbegin(); it != mEntries.cend(); it++)
   59  	{
   60  		updateElementSize(it->data);
   61  		updateElementPosition(it->data);
   62  	}
   63  
   64  	updateCameraOffset();
   65  }
   66  
   67  void ComponentTab::onFocusLost()
   68  {
   69  	mFocused = false;
   70  }
   71  
   72  void ComponentTab::onFocusGained()
   73  {
   74  	mFocused = true;
   75  }
   76  
   77  bool ComponentTab::input(InputConfig* config, Input input)
   78  {
   79  	if(size() == 0)
   80  		return false;
   81  	
   82  	// input handler didn't consume the input - try to scroll
   83  	if(config->isMappedLike("left", input))
   84  		return listInput(input.value != 0 ? -1 : 0);
   85  	else if(config->isMappedLike("right", input))
   86  		return listInput(input.value != 0 ? 1 : 0);
   87  
   88  	return false;
   89  }
   90  
   91  void ComponentTab::update(int deltaTime)
   92  {
   93  	listUpdate(deltaTime);
   94  
   95  	if(size())
   96  	{
   97  		// update our currently selected row
   98  		for(auto it = mEntries.at(mCursor).data.elements.cbegin(); it != mEntries.at(mCursor).data.elements.cend(); it++)
   99  			it->component->update(deltaTime);
  100  	}
  101  }
  102  
  103  void ComponentTab::onCursorChanged(const CursorState& state)
  104  {
  105  	// update the selector bar position
  106  	// in the future this might be animated
  107  	mSelectorBarOffset = 0;
  108  	for(int i = 0; i < mCursor; i++)
  109  		mSelectorBarOffset += getTabWidth(mEntries.at(i).data);
  110  
  111  	updateCameraOffset();
  112  
  113  	// this is terribly inefficient but we don't know what we came from so...
  114  	if(size())
  115  	{
  116  		for(auto it = mEntries.cbegin(); it != mEntries.cend(); it++)
  117  			it->data.elements.back().component->onFocusLost();
  118  
  119  		mEntries.at(mCursor).data.elements.back().component->onFocusGained();
  120  	}
  121  
  122  	if(mCursorChangedCallback)
  123  		mCursorChangedCallback(state);
  124  
  125  	updateHelpPrompts();
  126  }
  127  
  128  void ComponentTab::updateCameraOffset()
  129  {
  130  	const float totalWidth = mSize.x();
  131  
  132  	if (mCursor >= 0 && mCursor < mEntries.size())
  133  	{
  134  		int right = mSelectorBarOffset + getTabWidth(mEntries.at(mCursor).data);
  135  		if (right > totalWidth)
  136  			mCameraOffset = right - totalWidth;
  137  		else 
  138  			mCameraOffset = 0;
  139  	}
  140  	else 
  141  		mCameraOffset = 0;
  142  }
  143  
  144  void ComponentTab::render(const Transform4x4f& parentTrans)
  145  {
  146  	if(!size())
  147  		return;
  148  
  149  	auto menuTheme = ThemeData::getMenuTheme();
  150  	unsigned int selectorColor = menuTheme->Text.selectorColor;
  151  	unsigned int selectorGradientColor = menuTheme->Text.selectorGradientColor;
  152  	unsigned int selectedColor = menuTheme->Title.color;
  153  	unsigned int bgColor = menuTheme->Background.color;
  154  	unsigned int separatorColor = menuTheme->Text.separatorColor;
  155  	unsigned int textColor = menuTheme->Text.color;
  156  	bool selectorGradientHorz = menuTheme->Text.selectorGradientType;
  157  
  158  	Transform4x4f trans = parentTrans * getTransform();
  159  
  160  	// clip everything to be inside our bounds
  161  	Vector3f dim(mSize.x(), mSize.y(), 0);
  162  	dim = trans * dim - trans.translation();
  163  	
  164  	Renderer::pushClipRect(
  165  		Vector2i((int)trans.translation().x(), (int)trans.translation().y()),
  166  		Vector2i((int)Math::round(dim.x()), (int)Math::round(dim.y() + 1)));
  167  
  168  	// scroll the camera
  169  	trans.translate(Vector3f(-Math::round(mCameraOffset), 0, 0));
  170  
  171  	// draw our entries
  172  	std::vector<GuiComponent*> drawAfterCursor;
  173  	
  174  	float x = 0;
  175  
  176  	for(unsigned int i = 0; i < mEntries.size(); i++)
  177  	{
  178  		auto& entry = mEntries.at(i);
  179  
  180  		float tabWidth = getTabWidth(entry.data);
  181  
  182  		if (i == mHotTab)
  183  		{
  184  			Renderer::setMatrix(trans);
  185  			Renderer::drawRect(x, 0.0f, tabWidth, mSize.y(), 0x00000010, 0x00000010);
  186  		}
  187  
  188  		bool drawAll = (i != (unsigned int)mCursor);
  189  		for(auto it = entry.data.elements.cbegin(); it != entry.data.elements.cend(); it++)
  190  		{
  191  			if(drawAll || it->invert_when_selected)
  192  			{
  193  				it->component->setColor(menuTheme->Text.color);
  194  				it->component->render(trans);
  195  			}
  196  			else
  197  				drawAfterCursor.push_back(it->component.get());			
  198  		}
  199  
  200  		x += tabWidth;
  201  		if (x - mCameraOffset > mSize.x())
  202  			break;
  203  	}
  204  
  205  	// custom rendering
  206  	Renderer::setMatrix(trans);
  207  
  208  	const float selectedTabWidth = getTabWidth(mEntries.at(mCursor).data);
  209  
  210  	auto& entry = mEntries.at(mCursor);
  211  		
  212  	if ((selectorColor != bgColor) && ((selectorColor & 0xFF) != 0x00)) 
  213  	{			
  214  		if (mFocused)
  215  		{				
  216  			Renderer::drawRect(mSelectorBarOffset, 0.0f, selectedTabWidth, mSize.y(), bgColor, Renderer::Blend::ZERO, Renderer::Blend::ONE_MINUS_SRC_COLOR);
  217  			Renderer::drawRect(mSelectorBarOffset, 0.0f, selectedTabWidth, mSize.y(), selectorColor, selectorColor, selectorGradientHorz, Renderer::Blend::ONE, Renderer::Blend::ONE);
  218  		}
  219  		else
  220  		{
  221  			Renderer::drawRect(mSelectorBarOffset, mSize.y() - SELECTOR_PX, selectedTabWidth, SELECTOR_PX, bgColor, Renderer::Blend::ZERO, Renderer::Blend::ONE_MINUS_SRC_COLOR);
  222  			Renderer::drawRect(mSelectorBarOffset, mSize.y() - SELECTOR_PX, selectedTabWidth, SELECTOR_PX, selectorColor, selectorColor, selectorGradientHorz, Renderer::Blend::ONE, Renderer::Blend::ONE);
  223  		}
  224  	}
  225  
  226  	for (auto& element : entry.data.elements)
  227  	{
  228  		element.component->setColor(selectedColor);
  229  		drawAfterCursor.push_back(element.component.get());
  230  	}
  231  
  232  	for(auto it = drawAfterCursor.cbegin(); it != drawAfterCursor.cend(); it++)
  233  		(*it)->render(trans);
  234  
  235  	// reset matrix if one of these components changed it
  236  	if(drawAfterCursor.size())
  237  		Renderer::setMatrix(trans);
  238  
  239  	// draw separators
  240  	x = 0;
  241  	for(unsigned int i = 0; i < mEntries.size(); i++)
  242  	{
  243  		Renderer::drawRect(x, 0.0f, 1.0f, mSize.y(), separatorColor);
  244  		x += getTabWidth(mEntries.at(i).data);
  245  	}
  246  
  247  	Renderer::drawRect(x , 0.0f, 1.0f, mSize.y(), separatorColor);
  248  	Renderer::popClipRect();
  249  }
  250  
  251  float ComponentTab::getTabWidth(const ComponentTabItem& row) const
  252  {
  253  	float width = 0;
  254  
  255  	for(unsigned int i = 0; i < row.elements.size(); i++)
  256  		if(row.elements.at(i).component->getSize().x() > width)
  257  			width = row.elements.at(i).component->getSize().x();
  258  
  259  	return width;
  260  }
  261  
  262  float ComponentTab::getTotalTabWidth() const
  263  {
  264  	float width = 0;
  265  
  266  	for(auto it = mEntries.cbegin(); it != mEntries.cend(); it++)
  267  		width += getTabWidth(it->data);
  268  
  269  	return width;
  270  }
  271  
  272  void ComponentTab::updateElementPosition(const ComponentTabItem& row)
  273  {
  274  	float xOffset = 0;
  275  
  276  	for(auto it = mEntries.cbegin(); it != mEntries.cend() && &it->data != &row; it++)
  277  		xOffset += getTabWidth(it->data);
  278  	
  279  	// assumes updateElementSize has already been called
  280  	float colWidth = getTabWidth(row);
  281  
  282  	float y = 0.0f;
  283  	for(unsigned int i = 0; i < row.elements.size(); i++)
  284  	{
  285  		const auto comp = row.elements.at(i).component;
  286  		
  287  		// center vertically
  288  		comp->setPosition((colWidth - comp->getSize().x()) / 2 + xOffset, y);
  289  		y += comp->getSize().y();
  290  	}
  291  }
  292  
  293  void ComponentTab::updateElementSize(const ComponentTabItem& row)
  294  {
  295  	float height = mSize.y();
  296  	std::vector< std::shared_ptr<GuiComponent> > resizeVec;
  297  
  298  	for(auto it = row.elements.cbegin(); it != row.elements.cend(); it++)
  299  	{
  300  		if(it->resize_height)
  301  			resizeVec.push_back(it->component);
  302  		else
  303  			height -= it->component->getSize().y();
  304  	}
  305  
  306  	// redistribute the "unused" width equally among the components with resize_width set to true
  307  	height = height / resizeVec.size();
  308  	for(auto item : resizeVec)
  309  		item->setSize(item->getSize().x() , height); // + 2 * PADDING_PX
  310  }
  311  
  312  void ComponentTab::textInput(const char* text)
  313  {
  314  	if(!size())
  315  		return;
  316  
  317  	mEntries.at(mCursor).data.elements.back().component->textInput(text);
  318  }
  319  
  320  std::vector<HelpPrompt> ComponentTab::getHelpPrompts()
  321  {
  322  	if(!size())
  323  		return std::vector<HelpPrompt>();
  324  
  325  	std::vector<HelpPrompt> prompts = mEntries.at(mCursor).data.elements.back().component->getHelpPrompts();
  326  
  327  	if(size() > 1)
  328  	{
  329  		bool addMovePrompt = true;
  330  		for(auto it = prompts.cbegin(); it != prompts.cend(); it++)
  331  		{
  332  			if(it->first == "left/right" || it->first == "up/down/left/right")
  333  			{
  334  				addMovePrompt = false;
  335  				break;
  336  			}
  337  		}
  338  
  339  		// The strip runs sideways; "up/down" is the grid's business.
  340  		if(addMovePrompt)
  341  			prompts.push_back(HelpPrompt("left/right", _("SWITCH TAB")));
  342  	}
  343  
  344  	return prompts;
  345  }
  346  
  347  bool ComponentTab::moveCursor(int amt)
  348  {
  349  	bool ret = listInput(amt);
  350  	listInput(0);
  351  	return ret;
  352  }
  353  
  354  
  355  
  356  bool ComponentTab::hitTest(int x, int y, Transform4x4f& parentTransform, std::vector<GuiComponent*>* pResult)
  357  {
  358  	Transform4x4f trans = parentTransform * getTransform();
  359  
  360  	bool ret = false;
  361  
  362  	mHotTab = -1;
  363  
  364  	auto rect = Renderer::getScreenRect(trans, getSize(), true);
  365  	if (x != -1 && y != -1 && rect.contains(x, y))
  366  	{
  367  		ret = true;
  368  
  369  		float rx = 0;
  370  
  371  		for (unsigned int i = 0; i < mEntries.size(); i++)
  372  		{
  373  			auto& entry = mEntries.at(i);
  374  			float tabWidth = getTabWidth(entry.data);
  375  
  376  			if (rx - mCameraOffset + tabWidth >= 0)
  377  			{
  378  				rect.x = (rx - mCameraOffset) * trans.r0().x() + trans.translation().x(); // +Math::round(mCameraOffset);
  379  				rect.w = tabWidth * trans.r0().x();
  380  
  381  				if (rect.contains(x, y))
  382  				{
  383  					mHotTab = i;
  384  					break;
  385  				}
  386  			}
  387  
  388  			rx += tabWidth;
  389  			if (rx - mCameraOffset > mSize.x())
  390  				break;
  391  		}
  392  
  393  		if (pResult != nullptr)
  394  			pResult->push_back(this);
  395  	}
  396  
  397  	trans.translate(-mCameraOffset, 0);
  398  
  399  	for (int i = 0; i < getChildCount(); i++)
  400  		ret |= getChild(i)->hitTest(x, y, trans, pResult);
  401  
  402  	return ret;
  403  }
  404  
  405  bool ComponentTab::onMouseClick(int button, bool pressed, int x, int y)
  406  {
  407  	if (button == 1)
  408  	{
  409  		if (pressed)
  410  		{
  411  			if (mHotTab >= 0)
  412  			{
  413  				float camOffset = mCameraOffset;
  414  				mCursor = mHotTab;
  415  				onCursorChanged(CURSOR_STOPPED);
  416  				mCameraOffset = camOffset;
  417  				mPressedTab = mHotTab;
  418  			}
  419  
  420  			mWindow->setMouseCapture(this);
  421  		}
  422  		else if (mWindow->hasMouseCapture(this))
  423  		{
  424  			mWindow->releaseMouseCapture();
  425  
  426  			auto row = mHotTab;
  427  			mHotTab = -1;
  428  
  429  			if (row == mHotTab && mCursor == row)
  430  				InputManager::getInstance()->sendMouseClick(mWindow, 1);
  431  		}
  432  
  433  		return true;
  434  	}
  435  
  436  	return false;
  437  }
```

## ControllerActivityComponent.cpp `:130-146` (an excerpt, upstream-carried, at the pin)

```text
  130  
  131  	if (mSize.y() > 0 && mWheelTexture)
  132  	{
  133  		size_t heightPx = (size_t)Math::round(mSize.y());
  134  		mWheelTexture->rasterizeAt(heightPx, heightPx);
  135  	}
  136  }
  137  
  138  bool ControllerActivityComponent::input(InputConfig* config, Input input)
  139  {
  140  	if (config->getDeviceIndex() != -1 && (input.type == TYPE_BUTTON || input.type == TYPE_HAT))
  141  	{
  142  		int idx = config->getDeviceIndex();
  143  		if (idx >= 0 && idx < MAX_PLAYERS)
  144  		{
  145  			for (int i = 0; i < MAX_PLAYERS; i++)
  146  			{
```

## ControllerActivityComponent.cpp `:395-437` (an excerpt, upstream-carried, at the pin)

```text
  395  	const ThemeData::ThemeElement* elem = theme->getElement(view, element, element);
  396  	if (elem == nullptr)
  397  		return;
  398  
  399  	if (properties & PATH)
  400  	{		
  401  		// Controllers
  402  		if (elem->has("imagePath") && ResourceManager::getInstance()->fileExists(elem->get<std::string>("imagePath")))
  403  			mPadTexture = TextureResource::get(elem->get<std::string>("imagePath"), false, true);
  404  
  405  		if (elem->has("gunPath") && ResourceManager::getInstance()->fileExists(elem->get<std::string>("gunPath")))
  406  			mGunTexture = TextureResource::get(elem->get<std::string>("gunPath"), false, true);
  407  
  408  		if (elem->has("wheelPath") && ResourceManager::getInstance()->fileExists(elem->get<std::string>("wheelPath")))
  409  		  mWheelTexture = TextureResource::get(elem->get<std::string>("wheelPath"), false, true);
  410  
  411  		// Wifi
  412  		if (elem->has("networkIcon"))
  413  		{
  414  			if (ResourceManager::getInstance()->fileExists(elem->get<std::string>("networkIcon")))
  415  			{
  416  				mView |= ActivityView::NETWORK;
  417  				mNetworkImage = TextureResource::get(elem->get<std::string>("networkIcon"), false, true);
  418  			}
  419  			else
  420  				mNetworkImage = nullptr;
  421  		}
  422  
  423  		// planeMode
  424  		if (elem->has("planemodeIcon"))
  425  		{
  426  			if (ResourceManager::getInstance()->fileExists(elem->get<std::string>("planemodeIcon")))
  427  			{
  428  				mView |= ActivityView::PLANEMODE;
  429  				mPlanemodeImage = TextureResource::get(elem->get<std::string>("planemodeIcon"), false, true);
  430  			}
  431  			else
  432  				mPlanemodeImage = nullptr;
  433  		}
  434  
  435  		// Battery
  436  		if (elem->has("incharge") && ResourceManager::getInstance()->fileExists(elem->get<std::string>("incharge")))
  437  		{
```

## ControllerActivityComponent.cpp `:538-554` (an excerpt, upstream-carried, at the pin)

```text
  538  
  539  		if (mCurrentBatteryTexture != txName)
  540  		{
  541  			mCurrentBatteryTexture = txName;
  542  
  543  			if (mCurrentBatteryTexture.empty())
  544  				mBatteryImage = nullptr;
  545  			else
  546  				mBatteryImage = TextureResource::get(mCurrentBatteryTexture, false, true);
  547  		}
  548  	}
  549  }
  550  
  551  Vector2f ControllerActivityComponent::getTextureSize(std::shared_ptr<TextureResource> texture)
  552  {
  553  	if (texture == nullptr)
  554  		return Vector2f::Zero();
```

## DateTimeComponent.cpp `:47-63` (an excerpt, upstream-carried, at the pin)

```text
   47  }
   48  
   49  std::string DateTimeComponent::getDisplayString() const
   50  {
   51  	if (mDisplayRelative) 
   52  		return Utils::Time::getElapsedSinceString(mTime.getTime());
   53  
   54  	if (mTime.getTime() == 0)
   55  		return _("Unknown");
   56  
   57  	return Utils::Time::timeToString(mTime.getTime(), mFormat);
   58  }
   59  
   60  void DateTimeComponent::render(const Transform4x4f& parentTrans)
   61  {
   62  	TextComponent::render(parentTrans);
   63  }
```

## DateTimeEditComponent.cpp `:72-88` (an excerpt, upstream-carried, at the pin)

```text
   72  
   73  			pc++;
   74  		}
   75  	}
   76  
   77  	updateTextCache();
   78  }
   79  
   80  bool DateTimeEditComponent::input(InputConfig* config, Input input)
   81  {
   82  	if (input.value == 0)
   83  		return false;
   84  
   85  	if (config->isMappedTo(BUTTON_OK, input))
   86  	{
   87  		if (mDisplayMode != DISP_RELATIVE_TO_NOW) //don't allow editing for relative times
   88  			mEditing = !mEditing;
```

## DateTimeEditComponent.cpp `:116-168` (an excerpt, upstream-carried, at the pin)

```text
  116  		int incDir = 0;
  117  		if (config->isMappedLike("up", input) || config->isMappedTo("leftshoulder", input))
  118  			incDir = 1;
  119  		else if (config->isMappedLike("down", input) || config->isMappedTo("rightshoulder", input))
  120  			incDir = -1;
  121  
  122  		if (incDir != 0)
  123  		{
  124  			tm new_tm = mTime;
  125  
  126  			if (mEditIndex == mMonthIndex)
  127  			{
  128  				new_tm.tm_mon += incDir;
  129  
  130  				if (new_tm.tm_mon > 11)
  131  					new_tm.tm_mon = 0;
  132  				else if (new_tm.tm_mon < 0)
  133  					new_tm.tm_mon = 11;
  134  
  135  			}
  136  			else if (mEditIndex == mDayIndex)
  137  			{
  138  				const int days_in_month = Utils::Time::daysInMonth(new_tm.tm_year + 1900, new_tm.tm_mon + 1);
  139  				new_tm.tm_mday += incDir;
  140  
  141  				if (new_tm.tm_mday > days_in_month)
  142  					new_tm.tm_mday = 1;
  143  				else if (new_tm.tm_mday < 1)
  144  					new_tm.tm_mday = days_in_month;
  145  
  146  			}
  147  			else if (mEditIndex == mYearIndex)
  148  			{
  149  				new_tm.tm_year += incDir;
  150  
  151  				if (new_tm.tm_year < 0)
  152  					new_tm.tm_year = 0;
  153  			}
  154  
  155  			//validate day
  156  			const int days_in_month = Utils::Time::daysInMonth(new_tm.tm_year + 1900, new_tm.tm_mon + 1);
  157  			if (new_tm.tm_mday > days_in_month)
  158  				new_tm.tm_mday = days_in_month;
  159  
  160  			mTime = new_tm;
  161  
  162  			updateTextCache();
  163  			return true;
  164  		}
  165  
  166  		if (config->isMappedLike("right", input))
  167  		{
  168  			mEditIndex++;
```

## DateTimeEditComponent.cpp `:243-268` (an excerpt, upstream-carried, at the pin)

```text
  243  	return mTime;
  244  }
  245  
  246  DateTimeEditComponent::DisplayMode DateTimeEditComponent::getCurrentDisplayMode() const
  247  {
  248  	return mDisplayMode;
  249  }
  250  
  251  std::string DateTimeEditComponent::getDisplayString() const
  252  {
  253  	if (mDisplayMode == DISP_RELATIVE_TO_NOW)
  254  		return Utils::Time::getElapsedSinceString(mTime.getTime());
  255  
  256  	if (mTime.getTime() == 0)
  257  		return "";
  258  
  259  	return Utils::Time::timeToString(mTime, mDateFormat);
  260  }
  261  
  262  std::shared_ptr<Font> DateTimeEditComponent::getFont() const
  263  {
  264  	return mFont ? mFont : Font::get(FONT_SIZE_MEDIUM);
  265  }
  266  
  267  void DateTimeEditComponent::updateTextCache()
  268  {
```

## GridTileComponent.cpp (whole, fork-modified, at the pin)

```text
    1  #include "GridTileComponent.h"
    2  
    3  #include "resources/TextureResource.h"
    4  #include "ThemeData.h"
    5  
    6  #include <algorithm>
    7  
    8  #include "animations/LambdaAnimation.h"
    9  #include "ImageIO.h"
   10  
   11  #ifdef _RPI_
   12  #include "components/VideoPlayerComponent.h"
   13  #endif
   14  #include "components/VideoVlcComponent.h"
   15  #include "utils/FileSystemUtil.h"
   16  
   17  #include "Settings.h"
   18  #include "ImageGridComponent.h"
   19  
   20  #define VIDEODELAY	100
   21  
   22  GridTileComponent::GridTileComponent(Window* window) : GuiComponent(window), mBackground(window), mLabel(window), mVideo(nullptr), mVideoPlaying(false), mHasItemTemplate(false)
   23  {
   24  	mHasStandardMarquee = false;
   25  	mSelectedZoomPercent = 1.0f;
   26  	mAnimPosition = Vector3f(0, 0);
   27  	mVideo = nullptr;
   28  	mMarquee = nullptr;
   29  	mFavorite = nullptr;
   30  	mCheevos = nullptr;
   31  	mImageOverlay = nullptr;
   32  	mIsDefaultImage = false;
   33  	mImageLoaded = false;
   34  
   35  	mLabelMerged = false;
   36  
   37  	resetProperties();
   38  
   39  	mImage = new ImageComponent(mWindow);
   40  	mImage->setOrigin(0.5f, 0.5f);
   41  
   42  	mLabel.setFont(Font::get(FONT_SIZE_SMALL));
   43  	mLabel.setDefaultZIndex(10);
   44  
   45  	addChild(&mBackground);
   46  	addChild(&(*mImage));
   47  	addChild(&mLabel);
   48  
   49  	setSelected(false);
   50  	setVisible(true);
   51  }
   52  
   53  void GridTileComponent::resetProperties()
   54  {
   55  	mDefaultProperties.Size = getDefaultTileSize();
   56  	mDefaultProperties.Padding = Vector4f(16.0f, 16.0f, 16.0f, 16.0f);
   57  
   58  	mSelectedProperties.Size = getSelectedTileSize();
   59  	mSelectedProperties.Padding = mDefaultProperties.Padding;
   60  
   61  	mDefaultProperties.Label = mSelectedProperties.Label = GridTextProperties();	
   62  	mDefaultProperties.Image = mSelectedProperties.Image = GridImageProperties();	
   63  	mDefaultProperties.Marquee = mSelectedProperties.Marquee = GridImageProperties();
   64  	mDefaultProperties.Favorite = mSelectedProperties.Favorite = GridImageProperties();
   65  	mDefaultProperties.Cheevos = mSelectedProperties.Cheevos = GridImageProperties();
   66  	mDefaultProperties.Background = mSelectedProperties.Background = GridNinePatchProperties();
   67  
   68  	mDefaultProperties.Background.centerColor = mDefaultProperties.Background.edgeColor = 0xAAAAEEFF;
   69  	mDefaultProperties.Image.color = mDefaultProperties.Image.colorEnd = 0xFFFFFFDD;
   70  
   71  	mVideoPlayingProperties = mSelectedProperties;
   72  }
   73  
   74  void GridTileComponent::forceSize(Vector2f size, float selectedZoom)
   75  {
   76  	mSize = size;
   77  	mDefaultProperties.Size = size;
   78  	mSelectedProperties.Size = size * selectedZoom;
   79  	mVideoPlayingProperties.Size = mSelectedProperties.Size;
   80  }
   81  
   82  GridTileComponent::~GridTileComponent()
   83  {
   84  	if (mImage != nullptr)
   85  		delete mImage;
   86  
   87  	if (mImageOverlay != nullptr)
   88  		delete mImageOverlay;
   89  
   90  	if (mFavorite != nullptr)
   91  		delete mFavorite;
   92  
   93  	if (mCheevos != nullptr)
   94  		delete mCheevos;
   95  
   96  	if (mMarquee != nullptr)
   97  		delete mMarquee;
   98  
   99  	if (mVideo != nullptr)
  100  		delete mVideo;
  101  
  102  	mFavorite = nullptr;
  103      mCheevos = nullptr;
  104  	mMarquee = nullptr;
  105  	mImage = nullptr;
  106  	mVideo = nullptr;
  107  	mImageOverlay = nullptr;
  108  }
  109  
  110  std::shared_ptr<TextureResource> GridTileComponent::getTexture(bool marquee) 
  111  { 
  112  	if (marquee && mMarquee  != nullptr)
  113  		return mMarquee->getTexture();
  114  	else if (!marquee && mImage != nullptr)
  115  		return mImage->getTexture();
  116  
  117  	return nullptr; 
  118  }
  119  
  120  void GridTileComponent::resize()
  121  {
  122  	if (mHasItemTemplate)
  123  		return;
  124  
  125  	auto& currentProperties = getCurrentProperties();
  126  
  127  	Vector2f& size = currentProperties.Size;
  128  	if (mSize != size)
  129  		setSize(size);
  130  
  131  	bool isDefaultImage = mIsDefaultImage; // && (mCurrentPath == ":/folder.svg" || mCurrentPath == ":/cartridge.svg");
  132  
  133  	float height = (int) (size.y() * currentProperties.Label.size.y());
  134  	float labelHeight = height;
  135  
  136  	if (!currentProperties.Label.Visible || mLabelMerged || currentProperties.Label.size.x() == 0)
  137  		height = 0;
  138  
  139  	float topPadding = currentProperties.Padding.y();
  140  	float bottomPadding = std::max(currentProperties.Padding.w(), height);
  141  
  142  	Vector2f imageOffset = Vector2f(currentProperties.Padding.x(), currentProperties.Padding.y());
  143  	Vector2f imageSize(size.x() - currentProperties.Padding.x() - currentProperties.Padding.z(), size.y() - topPadding - bottomPadding);
  144  
  145  	// Image
  146  	if (currentProperties.Image.Loaded)
  147  	{
  148  		if (isDefaultImage)
  149  		{
  150  			imageOffset.x() += imageSize.x() * 0.05;
  151  			imageSize.x() *= 0.90;
  152  		}
  153  
  154  		currentProperties.Image.updateImageComponent(mImage, imageOffset, imageSize, false);
  155  
  156  		if (mImage != nullptr && isDefaultImage)
  157  			mImage->setRoundCorners(0);
  158  
  159  		if (mImage != nullptr && currentProperties.Image.sizeMode != "maxSize" && isDefaultImage)
  160  			mImage->setMaxSize(imageSize.x(), imageSize.y());
  161  	}	
  162  	else if (mImage != nullptr)
  163  	{
  164  		// Retrocompatibility : imagegrid.image is not defined
  165  		mImage->setOrigin(0.5f, 0.5f);
  166  		mImage->setPosition(imageOffset.x() + imageSize.x() / 2.0f, imageOffset.y() + imageSize.y() / 2.0f);
  167  		mImage->setColorShift(currentProperties.Image.color);
  168  		mImage->setMirroring(currentProperties.Image.reflexion);
  169  
  170  		if (currentProperties.Image.sizeMode == "minSize" && !isDefaultImage)
  171  			mImage->setMinSize(imageSize.x(), imageSize.y());
  172  		else if (currentProperties.Image.sizeMode == "size")
  173  			mImage->setSize(imageSize.x(), imageSize.x());
  174  		else
  175  			mImage->setMaxSize(imageSize.x(), imageSize.y());
  176  
  177  //		imageOffset = Vector2f::Zero();
  178  	}
  179  	
  180  	// Recompute final image size if necessary
  181  	if (mImage != nullptr && currentProperties.Image.sizeMode == "maxSize")
  182  	{
  183  		// If the overlay zindex < image zindex, then keep dimensions
  184  		if (mImageOverlay != nullptr && mImageOverlay->hasImage() && mImageOverlay->isVisible() && mImageOverlay->getZIndex() < mImage->getZIndex())
  185  			;
  186  		else
  187  		{
  188  			auto origin = mImage->getOrigin();
  189  			auto pos = mImage->getPosition();
  190  			imageSize = mImage->getSize();
  191  			imageOffset = Vector2f(pos.x() - imageSize.x() * origin.x(), pos.y() - imageSize.y() * origin.y());
  192  		}
  193  	}
  194  	
  195  	// Text	
  196  	mLabel.setVisible(!mLabel.getText().empty() && (currentProperties.Label.Visible || mIsDefaultImage));
  197  
  198  	if (currentProperties.Label.Visible)
  199  	{
  200  		auto szRef = mLabelMerged ? mSize - imageOffset : mSize;
  201  
  202  		currentProperties.Label.updateTextComponent(&mLabel, szRef);
  203  		
  204  		// Automatic layout for not merged labels 
  205  		if (currentProperties.Label.pos.x() < 0)
  206  		{			
  207  			if (currentProperties.Padding.x() == 0 && !mLabelMerged)
  208  			{
  209  				mLabel.setPosition(mImage->getPosition().x() - mImage->getSize().x() / 2, mImage->getSize().y());
  210  				mLabel.setSize(mImage->getSize().x(), labelHeight);
  211  			}
  212  			else
  213  			{
  214  				mLabel.setPosition(0, szRef.y() - labelHeight);
  215  				mLabel.setSize(size.x(), labelHeight);
  216  			}
  217  		}
  218  	}
  219  	else if (mIsDefaultImage)
  220  	{
  221  		mLabel.setColor(0xFFFFFFFF);
  222  		mLabel.setGlowColor(0x00000010);
  223  		mLabel.setGlowSize(2);
  224  		mLabel.setOpacity(255);
  225  		mLabel.setPosition(mSize.x() * 0.1, mSize.y() * 0.2);
  226  		mLabel.setSize(mSize.x() - mSize.x() * 0.2, mSize.y() - mSize.y() * 0.3);
  227  	}
  228  
  229  	// Other controls ( Favorite / Marquee / Overlay )
  230  	if (currentProperties.Favorite.Loaded)
  231  		currentProperties.Favorite.updateImageComponent(mFavorite, imageOffset, imageSize, false);
  232  	
  233      if (currentProperties.Cheevos.Loaded)
  234  		currentProperties.Cheevos.updateImageComponent(mCheevos, imageOffset, imageSize, false);
  235  
  236  	if (currentProperties.Marquee.Loaded)
  237  		currentProperties.Marquee.updateImageComponent(mMarquee, imageOffset, imageSize, true);
  238  
  239  	if (currentProperties.ImageOverlay.Loaded)
  240  		currentProperties.ImageOverlay.updateImageComponent(mImageOverlay, imageOffset, imageSize, false);
  241  
  242  	// Video
  243  	if (mVideo != nullptr && mVideo->isPlaying())
  244  	{
  245  		if (currentProperties.Image.sizeMode != "size")
  246  		{
  247  			mVideo->setOrigin(0.5, 0.5);			
  248  			mVideo->setPosition(imageOffset.x() + imageSize.x() / 2.0f, imageOffset.y() + imageSize.y() / 2.0f);
  249  			mVideo->setMinSize(imageSize.x(), imageSize.y());
  250  
  251  			if (mImage != nullptr)
  252  				mVideo->setRoundCorners(mImage->getRoundCorners());
  253  		}
  254  		else
  255  		{
  256  			mVideo->setOrigin(0.5f, 0.5f);
  257  			mVideo->setPosition(size.x() / 2.0f, (size.y() - height) / 2.0f);
  258  
  259  			if (currentProperties.Image.sizeMode == "size")
  260  				mVideo->setSize(imageSize.x(), size.y() - topPadding - bottomPadding);
  261  			else
  262  				mVideo->setMaxSize(imageSize.x(), size.y() - topPadding - bottomPadding);
  263  		}
  264  	}
  265  
  266  	// Background when SelectionMode == "image"
  267  	Vector3f bkPosition = Vector3f::Zero();
  268  	Vector2f bkSize = size;
  269  
  270  	if (mImage != NULL && currentProperties.SelectionMode == "image" && mImage->getSize() != Vector2f(0, 0))
  271  	{
  272  		if (currentProperties.Image.sizeMode == "minSize")
  273  		{
  274  			if (!mLabelMerged && currentProperties.Label.Visible)
  275  				bkSize = Vector2f(size.x(), size.y() - bottomPadding + topPadding);
  276  		}
  277  		else
  278  		{
  279  			bkPosition = Vector3f(imageOffset.x() - mSelectedProperties.Padding.x(), imageOffset.y() - mSelectedProperties.Padding.y(), 0);
  280  			bkSize = Vector2f(imageSize.x() + 2 * mSelectedProperties.Padding.x(), imageSize.y() + 2 * mSelectedProperties.Padding.y());
  281  		}
  282  	}
  283  	
  284  	// Background when animating
  285  	if (mSelectedZoomPercent != 1.0f && mAnimPosition.x() != 0 && mAnimPosition.y() != 0 && mSelected)
  286  	{
  287  		float x = mPosition.x() + bkPosition.x();
  288  		float y = mPosition.y() + bkPosition.y();
  289  
  290  		x = mAnimPosition.x() * (1.0 - mSelectedZoomPercent) + x * mSelectedZoomPercent;
  291  		y = mAnimPosition.y() * (1.0 - mSelectedZoomPercent) + y * mSelectedZoomPercent;
  292  
  293  		bkPosition = Vector3f(x - mPosition.x(), y - mPosition.y(), 0);
  294  	}	
  295  	
  296  	mBackground.setPosition(bkPosition);
  297  	mBackground.setSize(bkSize);
  298  
  299  	currentProperties.Background.updateNinePatchComponent(&mBackground);
  300  	/*
  301  	mBackground.setCornerSize(currentProperties.Background.cornerSize);
  302  	mBackground.setCenterColor(currentProperties.Background.centerColor);
  303  	mBackground.setEdgeColor(currentProperties.Background.edgeColor);
  304  	mBackground.setImagePath(currentProperties.Background.path);
  305  	*/
  306  	if (mSelected && mAnimPosition == Vector3f(0, 0, 0) && mSelectedZoomPercent != 1.0)
  307  		mBackground.setOpacity(mSelectedZoomPercent * 255);
  308  	else
  309  		mBackground.setOpacity(255);
  310  }
  311  
  312  void GridTileComponent::update(int deltaTime)
  313  {
  314  	GuiComponent::update(deltaTime);
  315  	
  316  	if (hasStoryBoard() && !isStoryBoardRunning())
  317  		deselectStoryboard(false);
  318  
  319  	for (auto comp : enumerateExtraChildrens())
  320  		if (comp->hasStoryBoard() && !comp->isStoryBoardRunning())
  321  			comp->deselectStoryboard(false);
  322  			
  323  	if (mVideo != nullptr && mVideo->isPlaying() && (mVideo->isFading() || !ALLOWANIMATIONS))
  324  		resize();
  325  }
  326  
  327  void GridTileComponent::renderBackground(const Transform4x4f& parentTrans)
  328  {
  329  	if (mHasItemTemplate)
  330  		return;
  331  
  332  	if (!mVisible)
  333  		return;
  334  
  335  	Transform4x4f trans = parentTrans * getTransform();
  336  	mBackground.render(trans);
  337  
  338  	if (Settings::DebugMouse() && mIsMouseOver)
  339  	{
  340  		Renderer::setMatrix(trans);
  341  		Renderer::drawRect(0.0f, 0.0f, mSize.x(), mSize.y(), 0xFF000033, 0xFF000033);
  342  	}
  343  }
  344  
  345  bool GridTileComponent::hasMarquee()
  346  {
  347  	return mHasStandardMarquee;
  348  }
  349  
  350  bool GridTileComponent::isMinSizeTile()
  351  {
  352  	auto& currentProperties = getCurrentProperties(false);
  353  	return (currentProperties.Image.sizeMode == "minSize");
  354  }
  355  
  356  void GridTileComponent::renderContent(const Transform4x4f& parentTrans, bool renderBackground)
  357  {
  358  	if (!mVisible)
  359  		return;
  360  
  361  	bool isMaxSizing = getCurrentProperties().Image.sizeMode == "maxSize";
  362  
  363  	if (!mImageLoaded && mImage != nullptr && mImage->getTextureSize() != Vector2i::Zero())
  364  	{
  365  		if (isMaxSizing)
  366  		{
  367  			mImage->onPaddingChanged();
  368  			resize();
  369  		}
  370  		mImageLoaded = true;
  371  	}
  372  
  373  	Transform4x4f trans = parentTrans * getTransform();
  374  
  375  	if (renderBackground && ((isMaxSizing && mImageLoaded) || !isMaxSizing))
  376  		mBackground.render(trans);
  377  
  378  	auto rect = Renderer::getScreenRect(trans, mSize);
  379  
  380  	if (mRotation == 0 && trans.r0().y() == 0 && !Renderer::isVisibleOnScreen(rect))
  381  		return;
  382  
  383  	if (mHasItemTemplate)
  384  	{
  385  		for (auto child : mChildren)
  386  			if (child->isVisible() && child->getExtraType() == ExtraType::EXTRACHILDREN)
  387  				child->render(trans);
  388  
  389  		return;
  390  	}
  391  
  392  	auto& currentProperties = getCurrentProperties(false);
  393  
  394  	bool isMinSize = !mIsDefaultImage && currentProperties.Image.sizeMode == "minSize";
  395  	if (isMinSize)
  396  	{
  397  		float padding = currentProperties.Padding.x();
  398  		float topPadding = currentProperties.Padding.y();
  399  		float bottomPadding = topPadding;
  400  
  401  		if (currentProperties.Label.Visible && !mLabelMerged)
  402  			bottomPadding = std::max((int)topPadding, (int)(mSize.y() * currentProperties.Label.size.y()));
  403  
  404  		Transform4x4f tx = trans;
  405  		tx.translate(padding, topPadding);
  406  
  407  		int x = (int)Math::round(tx.translation()[0]);
  408  		int y = (int)Math::round(tx.translation()[1]);
  409  		int w = (int)Math::round((mSize.x() - 2 * padding) * tx.r0().x());
  410  		int h = (int)Math::round((mSize.y() - topPadding - bottomPadding) * tx.r1().y());
  411  		
  412  		Renderer::pushClipRect(x, y, w, h);
  413  	}
  414  
  415  	float refZindex = mImage != NULL ? mImage->getZIndex() : mVideo != nullptr ? mVideo->getZIndex() : 10.0f;
  416  
  417  	bool overlayDrawn = false;
  418  	if (mImageOverlay != nullptr && mImageOverlay->hasImage() && mImageOverlay->isVisible() && mImage != nullptr && mImageOverlay->getZIndex() < refZindex)
  419  	{
  420  		mImageOverlay->render(trans);
  421  		overlayDrawn = true;
  422  	}
  423  
  424  	for (auto child : mChildren)
  425  		if (child->isVisible() && child->getExtraType() == ExtraType::EXTRACHILDREN && child->getZIndex() < refZindex)
  426  			child->render(trans);
  427  
  428  	if (mImage != NULL)
  429  	{
  430  		if (!isMinSize || !mSelected || mVideo == nullptr || !(mVideo->isPlaying() && !mVideo->isFading()))
  431  			mImage->render(trans);
  432  	}
  433  
  434  	if (mSelected && !mVideoPath.empty() && mVideo != nullptr)
  435  		mVideo->render(trans);
  436  
  437  	if (!mLabelMerged && isMinSize)
  438  		Renderer::popClipRect();
  439  
  440  	std::vector<GuiComponent*> zOrdered;
  441  
  442  	for (auto child : mChildren)
  443  		if (child->isVisible() && child->getExtraType() == ExtraType::EXTRACHILDREN && child->getZIndex() >= refZindex)
  444  			zOrdered.push_back(child);
  445  
  446  	if (mMarquee != nullptr && mMarquee->hasImage())
  447  		zOrdered.push_back(mMarquee);
  448  	else
  449  		zOrdered.push_back(&mLabel);
  450  
  451  	if (mFavorite != nullptr && mFavorite->hasImage() && mFavorite->isVisible())
  452  		zOrdered.push_back(mFavorite);
  453  
  454  	if (mCheevos != nullptr && mCheevos->hasImage() && mCheevos->isVisible())
  455  		zOrdered.push_back(mCheevos);
  456  
  457  	if (mImageOverlay != nullptr && mImageOverlay->hasImage() && mImageOverlay->isVisible() && !overlayDrawn)
  458  		zOrdered.push_back(mImageOverlay);
  459  
  460  	if (zOrdered.size() > 1)
  461  		std::stable_sort(zOrdered.begin(), zOrdered.end(), [](GuiComponent* a, GuiComponent* b) { return b->getZIndex() > a->getZIndex(); });
  462  
  463  	for (auto comp : zOrdered)
  464  		comp->render(trans);
  465  
  466  	if (mLabelMerged && isMinSize)
  467  		Renderer::popClipRect();
  468  }
  469  
  470  void GridTileComponent::render(const Transform4x4f& parentTrans)
  471  {
  472  	if (!mVisible)
  473  		return;
  474  
  475  	if (Settings::DebugMouse() && mIsMouseOver)
  476  	{
  477  		Transform4x4f trans = parentTrans * getTransform();
  478  		Renderer::setMatrix(trans);
  479  		Renderer::drawRect(0.0f, 0.0f, mSize.x(), mSize.y(), 0xFF000033, 0xFF000033);
  480  	}
  481  
  482  	renderContent(parentTrans, true);
  483  }
  484  
  485  void GridTileComponent::createMarquee()
  486  {
  487  	if (mMarquee != nullptr)
  488  		return;
  489  
  490  	mMarquee = new ImageComponent(mWindow);
  491  	mMarquee->setOrigin(0.5f, 0.5f);
  492  	mMarquee->setDefaultZIndex(20);
  493  	addChild(mMarquee);
  494  }
  495  
  496  void GridTileComponent::createFavorite()
  497  {
  498  	if (mFavorite != nullptr)
  499  		return;
  500  
  501  	mFavorite = new ImageComponent(mWindow);
  502  	mFavorite->setOrigin(0.5f, 0.5f);
  503  	mFavorite->setDefaultZIndex(15);
  504  	mFavorite->setVisible(false);
  505  	
  506  	addChild(mFavorite);
  507  }
  508  
  509  void GridTileComponent::createCheevos()
  510  {
  511  	if (mCheevos != nullptr)
  512  		return;
  513  
  514  	mCheevos = new ImageComponent(mWindow);
  515  	mCheevos->setOrigin(0.5f, 0.5f);
  516  	mCheevos->setDefaultZIndex(15);
  517  	mCheevos->setVisible(false);
  518  	
  519  	addChild(mCheevos);
  520  }
  521  
  522  void GridTileComponent::createImageOverlay()
  523  {
  524  	if (mImageOverlay != nullptr)
  525  		return;
  526  
  527  	mImageOverlay = new ImageComponent(mWindow);
  528  	mImageOverlay->setOrigin(0.5f, 0.5f);
  529  	mImageOverlay->setDefaultZIndex(25);
  530  	mImageOverlay->setVisible(false);
  531  
  532  	addChild(mImageOverlay);
  533  }
  534  
  535  void GridTileComponent::createVideo()
  536  {
  537  	if (mVideo != nullptr)
  538  		return;
  539  
  540  	auto vlc = new VideoVlcComponent(mWindow);
  541  	vlc->setEffect(VideoVlcFlags::SIZE);
  542  
  543  	// video
  544  	mVideo = vlc;
  545  	mVideo->setOrigin(0.5f, 0.5f);
  546  	mVideo->setStartDelay(VIDEODELAY);
  547  	mVideo->setDefaultZIndex(11);
  548  	addChild(mVideo);
  549  }
  550  
  551  void GridTileComponent::applyThemeToProperties(const ThemeData::ThemeElement* elem, GridTileProperties& properties)
  552  {
  553  	if (elem == nullptr)
  554  		return;
  555  
  556  	Vector2f screen = Vector2f((float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
  557  
  558  	if (elem->has("size"))
  559  		properties.Size = elem->get<Vector2f>("size") * screen;
  560  
  561  	if (elem->has("padding"))
  562  	{
  563  		properties.Padding = elem->get<Vector4f>("padding");
  564  		
  565  		if (abs(properties.Padding.x()) < 1 && abs(properties.Padding.y()) < 1 && abs(properties.Padding.w()) < 1 && abs(properties.Padding.y()) < 1)
  566  			properties.Padding *= screen;
  567  	}
  568  
  569  	if (elem && elem->has("selectionMode"))
  570  		properties.SelectionMode = elem->get<std::string>("selectionMode");		
  571  
  572  	// Retrocompatibility for Background properties
  573  	if (elem->has("backgroundImage"))
  574  		properties.Background.setImagePath(elem->get<std::string>("backgroundImage"));
  575  
  576  	if (elem->has("backgroundCornerSize"))
  577  		properties.Background.cornerSize = elem->get<Vector2f>("backgroundCornerSize");
  578  
  579  	if (elem->has("backgroundColor"))
  580  	{
  581  		properties.Background.centerColor = elem->get<unsigned int>("backgroundColor");
  582  		properties.Background.edgeColor = elem->get<unsigned int>("backgroundColor");
  583  	}
  584  
  585  	if (elem->has("backgroundCenterColor"))
  586  		properties.Background.centerColor = elem->get<unsigned int>("backgroundCenterColor");
  587  
  588  	if (elem->has("backgroundEdgeColor"))
  589  		properties.Background.edgeColor = elem->get<unsigned int>("backgroundEdgeColor");
  590  
  591  	// Retrocompatibility for Image properties
  592  	if (elem && elem->has("reflexion"))
  593  		properties.Image.reflexion = elem->get<Vector2f>("reflexion");
  594  
  595  	if (elem->has("imageColor"))
  596  		properties.Image.color = properties.Image.colorEnd = elem->get<unsigned int>("imageColor");
  597  
  598  	if (elem && elem->has("imageSizeMode"))
  599  		properties.Image.sizeMode = elem->get<std::string>("imageSizeMode");
  600  }
  601  
  602  bool GridImageProperties::applyTheme(const ThemeData::ThemeElement* elem)
  603  {
  604  	if (!elem)
  605  		return false;
  606  
  607  	Loaded = true;
  608  	Visible = true;
  609  
  610  	if (elem && elem->has("visible"))
  611  		Visible = elem->get<bool>("visible");
  612  
  613  	if (elem && elem->has("origin"))
  614  		origin = elem->get<Vector2f>("origin");
  615  
  616  	if (elem && elem->has("pos"))
  617  		pos = elem->get<Vector2f>("pos");
  618  
  619  	if (elem && elem->has("size"))
  620  	{
  621  		sizeMode = "size";
  622  		size = elem->get<Vector2f>("size");
  623  	}
  624  	else if (elem && elem->has("minSize"))
  625  	{
  626  		sizeMode = "minSize";
  627  		size = elem->get<Vector2f>("minSize");
  628  	}
  629  	else if (elem && elem->has("maxSize"))
  630  	{
  631  		sizeMode = "maxSize";
  632  		size = elem->get<Vector2f>("maxSize");
  633  	}
  634  
  635  	if (elem && elem->has("color"))
  636  		color = colorEnd = elem->get<unsigned int>("color");
  637  
  638  	if (elem && elem->has("colorEnd"))
  639  		colorEnd = elem->get<unsigned int>("colorEnd");
  640  
  641  	if (elem && elem->has("reflexion"))
  642  		reflexion = elem->get<Vector2f>("reflexion");
  643  
  644  	if (elem && elem->has("roundCorners"))
  645  		roundCorners = elem->get<float>("roundCorners");
  646  
  647  	ThemeData::parseCustomShader(elem, &customShader);
  648  
  649  	return true;
  650  }
  651  
  652  bool GridTextProperties::applyTheme(const ThemeData::ThemeElement* elem)
  653  {
  654  	if (!elem)
  655  	{
  656  		Visible = false;
  657  		return false;
  658  	}
  659  
  660  	Loaded = true;
  661  	Visible = true;
  662  
  663  	if (elem && elem->has("visible"))
  664  		Visible = elem->get<bool>("visible");
  665  
  666  	if (elem && elem->has("pos"))
  667  		pos = elem->get<Vector2f>("pos");
  668  
  669  	if (elem && elem->has("size"))
  670  	{
  671  		size = elem->get<Vector2f>("size");
  672  		if (size.y() == 0)
  673  			Visible = false;
  674  	}
  675  
  676  	if (elem && elem->has("color"))
  677  		color = elem->get<unsigned int>("color");
  678  
  679  	if (elem && elem->has("backgroundColor"))
  680  		backColor = elem->get<unsigned int>("backgroundColor");
  681  
  682  	if (elem && elem->has("glowColor"))
  683  		glowColor = elem->get<unsigned int>("glowColor");
  684  
  685  	if (elem && elem->has("glowSize"))
  686  		glowSize = elem->get<float>("glowSize");
  687  
  688  	if (elem && elem->has("fontSize"))
  689  		fontSize = elem->get<float>("fontSize");
  690  
  691  	if (elem && elem->has("fontPath"))
  692  		fontPath = elem->get<std::string>("fontPath");
  693  
  694  	if (elem && elem->has("padding"))
  695  		padding = elem->get<Vector4f>("padding");
  696  
  697  	if (elem->has("singleLineScroll"))
  698  		autoScroll = elem->get<bool>("singleLineScroll");
  699  
  700  	if (elem->has("multiLine"))
  701  		multiLine = elem->get<std::string>("multiLine");
  702  
  703  	return true;
  704  }
  705  
  706  bool GridNinePatchProperties::applyTheme(const ThemeData::ThemeElement* elem)
  707  {
  708  	if (!elem)
  709  	{
  710  		Visible = false;
  711  		return false;
  712  	}
  713  
  714  	Loaded = true;
  715  	Visible = true;
  716  
  717  	if (elem && elem->has("visible"))
  718  		Visible = elem->get<bool>("visible");
  719  	/*
  720  	if (elem && elem->has("pos"))
  721  		pos = elem->get<Vector2f>("pos");
  722  
  723  	if (elem && elem->has("size"))
  724  		size = elem->get<Vector2f>("size");
  725  		*/
  726  	if (elem && elem->has("color"))
  727  		centerColor = edgeColor = elem->get<unsigned int>("color");
  728  
  729  	if (elem && elem->has("centerColor"))
  730  		centerColor = elem->get<unsigned int>("centerColor");
  731  
  732  	if (elem && elem->has("edgeColor"))
  733  		edgeColor = elem->get<unsigned int>("edgeColor");
  734  
  735  	if (elem && elem->has("cornerSize"))
  736  		cornerSize = elem->get<Vector2f>("cornerSize");
  737  
  738  	if (elem && elem->has("path"))
  739  		setImagePath(elem->get<std::string>("path"));
  740  
  741  	if (elem && elem->has("animateColor"))
  742  		animateColor = elem->get<unsigned int>("animateColor");
  743  
  744  	if (elem && elem->has("animateColorTime"))
  745  		animateTime = elem->get<float>("animateColorTime");
  746  
  747  	if (elem && elem->has("padding"))
  748  		padding = elem->get<Vector4f>("padding");
  749  
  750  	return true;
  751  }
  752  
  753  void GridTileComponent::applyTheme(const std::shared_ptr<ThemeData>& theme, const std::string& view, const std::string& element, unsigned int properties)
  754  {
  755  	if (mSize == Vector2f::Zero())
  756  		setSize(getDefaultTileSize());
  757  
  758  	resetProperties();
  759  
  760  	const ThemeData::ThemeElement* grid = theme->getElement(view, view == "system" ? "imagegrid" : "gamegrid", "imagegrid");
  761  	if (grid)
  762  	{
  763  		auto itemTemplate = std::find_if(grid->children.cbegin(), grid->children.cend(), [](const std::pair<std::string, ThemeData::ThemeElement> ss) { return ss.first == "itemTemplate"; });
  764  		if (itemTemplate != grid->children.cend())
  765  		{
  766  			mHasItemTemplate = true;
  767  			mScaleOrigin = Vector2f::Zero();
  768  
  769  			applyStoryboard(&itemTemplate->second);
  770  			loadThemedChildren(&itemTemplate->second);
  771  
  772  			mBackground.setVisible(false);
  773  
  774  			if (mImage != nullptr)
  775  			{
  776  				removeChild(mImage);
  777  				delete mImage;
  778  				mImage = nullptr;
  779  			}
  780  
  781  			if (mVideo != nullptr)
  782  			{
  783  				removeChild(mVideo);
  784  				delete mVideo;
  785  				mVideo = nullptr;
  786  			}
  787  
  788  			removeChild(&mBackground);
  789  			removeChild(&mLabel);
  790  
  791  			return;
  792  		}
  793  	}
  794  
  795  	// Old Non-Templated grid
  796  	if (grid && grid->has("showVideoAtDelay"))
  797  	{
  798  		createVideo();
  799  
  800  		if (theme->getElement(view, "gridtile", "video"))
  801  			mVideo->applyTheme(theme, view, "gridtile", ThemeFlags::ALL ^ (ThemeFlags::PATH));
  802  		else if (theme->getElement(view, "gridtile.video", "video"))
  803  			mVideo->applyTheme(theme, view, "gridtile.video", ThemeFlags::ALL ^ (ThemeFlags::PATH));
  804  	}
  805  	else if (mVideo != nullptr)
  806  	{
  807  		removeChild(mVideo);
  808  		delete mVideo;
  809  		mVideo = nullptr;
  810  	}
  811  
  812  	// Apply theme to the default gridtile
  813  	const ThemeData::ThemeElement* elem = theme->getElement(view, "default", "gridtile");
  814  	if (elem)
  815  	{
  816  		applyThemeToProperties(elem, mDefaultProperties);
  817  		applyThemeToProperties(elem, mSelectedProperties);		
  818  		loadThemedChildren(elem);
  819  	}
  820  
  821  	// Apply theme to the selected gridtile
  822  	elem = theme->getElement(view, "selected", "gridtile");
  823  	if (elem)
  824  		applyThemeToProperties(elem, mSelectedProperties);
  825  		
  826  
  827  	// Apply theme to the <image name="gridtile.image"> element
  828  	elem = theme->getElement(view, "gridtile.image", "image");
  829  	if (elem)
  830  	{
  831  		mImage->applyTheme(theme, view, "gridtile.image", ThemeFlags::ALL ^ (ThemeFlags::PATH));
  832  
  833  		mDefaultProperties.Image.applyTheme(elem);
  834  		mSelectedProperties.Image.applyTheme(elem);
  835  	}	
  836  
  837  	// Apply theme to the <image name="gridtile.image:selected"> element
  838  	elem = theme->getElement(view, "gridtile.image:selected", "image");
  839  	if (elem)
  840  		mSelectedProperties.Image.applyTheme(elem);
  841  	
  842  
  843  	// Apply theme to the <image name="gridtile.marquee"> element
  844  	elem = theme->getElement(view, "gridtile.marquee", "image");
  845  	if (elem)
  846  	{
  847  		mHasStandardMarquee = true;
  848  		createMarquee();
  849  		mMarquee->applyTheme(theme, view, "gridtile.marquee", ThemeFlags::ALL ^ (ThemeFlags::PATH));
  850  
  851  		mDefaultProperties.Marquee.applyTheme(elem);
  852  		mSelectedProperties.Marquee = mDefaultProperties.Marquee;
  853  
  854  		// Apply theme to the <image name="gridtile.marquee:selected"> element
  855  		elem = theme->getElement(view, "gridtile.marquee:selected", "image");
  856  		if (elem)
  857  			mSelectedProperties.Marquee.applyTheme(elem);
  858  	}
  859  	else if (mMarquee != nullptr)
  860  	{
  861  		mHasStandardMarquee = false;
  862  		removeChild(mMarquee);
  863  		delete mMarquee;
  864  		mMarquee = nullptr;
  865  	}
  866  
  867  
  868  	// Apply theme to the <image name="gridtile.marquee"> element
  869  	elem = theme->getElement(view, "gridtile.favorite", "image");
  870  	if (elem)
  871  	{
  872  		createFavorite();
  873  		mFavorite->applyTheme(theme, view, "gridtile.favorite", ThemeFlags::ALL);
  874  
  875  		mDefaultProperties.Favorite.sizeMode = "size";
  876  		mDefaultProperties.Favorite.applyTheme(elem);
  877  		mSelectedProperties.Favorite = mDefaultProperties.Favorite;
  878  
  879  		// Apply theme to the <image name="gridtile.favorite:selected"> element
  880  		elem = theme->getElement(view, "gridtile.favorite:selected", "image");
  881  		if (elem)
  882  			mSelectedProperties.Favorite.applyTheme(elem);
  883  	}
  884  	else if (mFavorite != nullptr)
  885  	{
  886  		removeChild(mFavorite);
  887  		delete mFavorite;
  888  		mFavorite = nullptr;
  889  	}
  890      
  891  	// Apply theme to the <image name="gridtile.cheevos"> element
  892  	elem = theme->getElement(view, "gridtile.cheevos", "image");
  893  	if (elem)
  894  	{
  895  		createCheevos();
  896  		mCheevos->applyTheme(theme, view, "gridtile.cheevos", ThemeFlags::ALL);
  897  
  898  		mDefaultProperties.Cheevos.sizeMode = "size";
  899  		mDefaultProperties.Cheevos.applyTheme(elem);
  900  		mSelectedProperties.Cheevos = mDefaultProperties.Cheevos;
  901  
  902  		// Apply theme to the <image name="gridtile.cheevos:selected"> element
  903  		elem = theme->getElement(view, "gridtile.cheevos:selected", "image");
  904  		if (elem)
  905  			mSelectedProperties.Cheevos.applyTheme(elem);
  906  	}
  907  	else if (mCheevos != nullptr)
  908  	{
  909  		removeChild(mCheevos);
  910  		delete mCheevos;
  911  		mCheevos = nullptr;
  912  	}
  913  
  914  
  915  	// Apply theme to the <image name="gridtile.overlay"> element
  916  	elem = theme->getElement(view, "gridtile.overlay", "image");
  917  	if (elem)
  918  	{
  919  		createImageOverlay();
  920  		mImageOverlay->applyTheme(theme, view, "gridtile.overlay", ThemeFlags::ALL);
  921  
  922  		mDefaultProperties.ImageOverlay.sizeMode = "size";
  923  		mDefaultProperties.ImageOverlay.applyTheme(elem);
  924  		mSelectedProperties.ImageOverlay = mDefaultProperties.ImageOverlay;
  925  
  926  		// Apply theme to the <image name="gridtile.favorite:selected"> element
  927  		elem = theme->getElement(view, "gridtile.overlay:selected", "image");
  928  		if (elem)
  929  			mSelectedProperties.ImageOverlay.applyTheme(elem);
  930  	}
  931  	else if (mImageOverlay != nullptr)
  932  	{
  933  		removeChild(mImageOverlay);
  934  		delete mImageOverlay;
  935  		mImageOverlay = nullptr;
  936  	}
  937  	
  938  
  939  	// Apply theme to the <text name="gridtile"> element
  940  	elem = theme->getElement(view, "gridtile", "text");
  941  	if (elem == nullptr) // Apply theme to the <text name="gridtile.text"> element		
  942  		elem = theme->getElement(view, "gridtile.text", "text");
  943  
  944  	if (elem != NULL)
  945  	{
  946  		mLabel.applyTheme(theme, view, element, properties);
  947  
  948  		mDefaultProperties.Label.applyTheme(elem);
  949  		mSelectedProperties.Label.applyTheme(elem);		
  950  
  951  		bool hasVisible = elem->has("visible");
  952  		mLabelMerged = elem->has("pos");
  953  		if (!mLabelMerged && elem->has("size"))
  954  			mLabelMerged = mDefaultProperties.Label.size.x() == 0;
  955  
  956  		// Apply theme to the <text name="gridtile:selected"> element
  957  		elem = theme->getElement(view, "gridtile_selected", "text");
  958  		if (elem == nullptr)
  959  			elem = theme->getElement(view, "gridtile:selected", "text");
  960  		if (elem == nullptr) // Apply theme to the <text name="gridtile.text:selected"> element
  961  			elem = theme->getElement(view, "gridtile.text:selected", "text");
  962  
  963  		if (elem)
  964  		{
  965  			mSelectedProperties.Label.applyTheme(elem);
  966  			if (hasVisible && !elem->has("visible"))
  967  				mSelectedProperties.Label.Visible = mDefaultProperties.Label.Visible;
  968  		}
  969  	}
  970  
  971  	// Apply theme to the <ninepatch name="gridtile"> element
  972  	elem = theme->getElement(view, "gridtile", "ninepatch");
  973  	if (elem == nullptr) // Apply theme to the <ninepatch name="gridtile.background"> element		
  974  		elem = theme->getElement(view, "gridtile.background", "ninepatch");
  975  
  976  	if (elem != NULL)
  977  	{
  978  		mBackground.applyTheme(theme, view, element, properties);
  979  		mDefaultProperties.Background.applyTheme(elem);		
  980  		mSelectedProperties.Background.applyTheme(elem);
  981  	}
  982  
  983  	// Apply theme to the <ninepatch name="gridtile:selected"> element
  984  	elem = theme->getElement(view, "gridtile:selected", "ninepatch");
  985  	if (elem == nullptr) // Apply theme to the <ninepatch name="gridtile.background:selected"> element
  986  		elem = theme->getElement(view, "gridtile.background:selected", "ninepatch");
  987  
  988  	if (elem)
  989  		mSelectedProperties.Background.applyTheme(elem);
  990  
  991  	mVideoPlayingProperties = mSelectedProperties;
  992  
  993  	if (!mVideoPlayingProperties.Label.applyTheme(theme->getElement(view, "gridtile:videoplaying", "text")))
  994  		if (!mVideoPlayingProperties.Label.applyTheme(theme->getElement(view, "gridtile.text:videoplaying", "text")))
  995  			mVideoPlayingProperties.Label = mSelectedProperties.Label;
  996  
  997  	mVideoPlayingProperties.Image.applyTheme(theme->getElement(view, "gridtile.image:videoplaying", "image"));
  998  	mVideoPlayingProperties.Marquee.applyTheme(theme->getElement(view, "gridtile.marquee:videoplaying", "image"));
  999  	mVideoPlayingProperties.Favorite.applyTheme(theme->getElement(view, "gridtile.favorite:selected", "image"));
 1000  	mVideoPlayingProperties.Cheevos.applyTheme(theme->getElement(view, "gridtile.cheevos:selected", "image"));
 1001  	mVideoPlayingProperties.ImageOverlay.applyTheme(theme->getElement(view, "gridtile.overlay:videoplaying", "image"));
 1002  }
 1003  
 1004  // Made this a static function because the ImageGridComponent need to know the default tile size
 1005  // to calculate the grid dimension before it instantiate the GridTileComponents
 1006  Vector2f GridTileComponent::getDefaultTileSize()
 1007  {
 1008  	Vector2f screen = Vector2f((float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
 1009  	return screen * 0.22f;
 1010  }
 1011  
 1012  Vector2f GridTileComponent::getSelectedTileSize() const
 1013  {
 1014  	return mDefaultProperties.Size * 1.2f;
 1015  }
 1016  
 1017  bool GridTileComponent::isSelected() const
 1018  {
 1019  	return mSelected;
 1020  }
 1021  
 1022  void GridTileComponent::setImage(const std::string& path, bool isDefaultImage)
 1023  {
 1024  	if (mImage == nullptr)
 1025  		return;
 1026  
 1027  	if (path == ":/folder.svg" || path == ":/cartridge.svg")
 1028  		mIsDefaultImage = true;
 1029  	else
 1030  		mIsDefaultImage = isDefaultImage;
 1031  
 1032  	if (mCurrentPath == path)
 1033  		return;
 1034  
 1035  	mCurrentPath = path;
 1036  
 1037  	if (mSelectedProperties.Size.x() > mSize.x())
 1038  		mImage->setImage(path, false, MaxSizeInfo(mSelectedProperties.Size, mSelectedProperties.Image.sizeMode != "maxSize"), false);
 1039  	else
 1040  		mImage->setImage(path, false, MaxSizeInfo(mSize, mSelectedProperties.Image.sizeMode != "maxSize"), false);
 1041  
 1042  	mImage->setDisplayAspect(mDisplayAspect);
 1043  		mImage->setDisplayRotation(mDisplayRotation);
 1044  	mImageLoaded = mImage->getTextureSize() != Vector2i::Zero();
 1045  	resize();
 1046  }
 1047  
 1048  void GridTileComponent::setDisplayAspect(float ratio)
 1049  {
 1050  	mDisplayAspect = ratio;
 1051  	if (mImage != nullptr)
 1052  		mImage->setDisplayAspect(ratio);
 1053  }
 1054  
 1055  void GridTileComponent::setDisplayRotation(int quarterTurns)
 1056  {
 1057  	quarterTurns = ((quarterTurns % 4) + 4) % 4;
 1058  	if (mDisplayRotation == quarterTurns)
 1059  		return;
 1060  	mDisplayRotation = quarterTurns;
 1061  	if (mImage != nullptr)
 1062  		mImage->setDisplayRotation(mDisplayRotation);
 1063  }
 1064  
 1065  void GridTileComponent::setMarquee(const std::string& path)
 1066  {
 1067  	if (mMarquee == nullptr)
 1068  		return;
 1069  
 1070  	if (mCurrentMarquee == path)
 1071  		return;
 1072  
 1073  	mCurrentMarquee = path;
 1074  
 1075  	if (mSelectedProperties.Size.x() > mSize.x())
 1076  		mMarquee->setImage(path, false, MaxSizeInfo(mSelectedProperties.Size), false);
 1077  	else
 1078  		mMarquee->setImage(path, false, MaxSizeInfo(mSize), false);
 1079  
 1080  	resize();
 1081  }
 1082  
 1083  void GridTileComponent::setCheevos(bool cheevos)
 1084  {
 1085  	if (mCheevos == nullptr)
 1086  		return;
 1087  
 1088  	mCheevos->setVisible(cheevos);
 1089  	resize();
 1090  }
 1091  
 1092  void GridTileComponent::setFavorite(bool favorite)
 1093  {
 1094  	if (mFavorite == nullptr)
 1095  		return;
 1096  
 1097  	mFavorite->setVisible(favorite);
 1098  	resize();
 1099  }
 1100  
 1101  void GridTileComponent::resetImages()
 1102  {
 1103  	updateBindings(nullptr);
 1104  
 1105  	setLabel("");
 1106  	setImage("");
 1107  	setMarquee("");
 1108  	stopVideo();
 1109  }
 1110  
 1111  void GridTileComponent::setLabel(std::string name)
 1112  {
 1113  	if (mLabel.getText() == name)
 1114  		return;
 1115  
 1116  	mLabel.setText(name);
 1117  	resize();
 1118  }
 1119  
 1120  void GridTileComponent::setVideo(const std::string& path, float defaultDelay)
 1121  {
 1122  	if (mVideoPath == path)
 1123  		return;
 1124  
 1125  	mVideoPath = path;
 1126  
 1127  	if (mVideo != nullptr)
 1128  	{
 1129  		if (defaultDelay >= 0.0)
 1130  			mVideo->setStartDelay(defaultDelay);
 1131  
 1132  		if (mVideoPath.empty())
 1133  			stopVideo();
 1134  	}
 1135  
 1136  	resize();
 1137  }
 1138  
 1139  void GridTileComponent::handleStoryBoard(bool activate)
 1140  {
 1141  	if (hasStoryBoard() && (isStoryBoardRunning("activate") || isStoryBoardRunning("deactivate")))
 1142  		deselectStoryboard(false);
 1143  
 1144  	if (selectStoryboard(activate ? "activate" : "deactivate"))
 1145  		startStoryboard();
 1146  	else if (selectStoryboard())
 1147  		startStoryboard();
 1148  
 1149  	for (auto comp : enumerateExtraChildrens())
 1150  	{
 1151  		if (comp->isStoryBoardRunning("activate") || comp->isStoryBoardRunning("deactivate"))
 1152  			comp->deselectStoryboard(false);
 1153  
 1154  		if (comp->selectStoryboard(activate ? "activate" : "deactivate"))
 1155  		{
 1156  			comp->startStoryboard();
 1157  			comp->update(0);
 1158  		}
 1159  		else if (comp->selectStoryboard())
 1160  		{
 1161  			if (!comp->isStoryBoardRunning())
 1162  			{
 1163  				comp->startStoryboard();
 1164  				comp->update(0);
 1165  			}
 1166  		}
 1167  		else if (!activate)
 1168  		{
 1169  			if (comp->isStoryBoardRunning("scroll"))
 1170  				comp->deselectStoryboard(false);
 1171  
 1172  			if (comp->selectStoryboard("scroll"))
 1173  			{
 1174  				comp->startStoryboard();
 1175  				comp->update(0);
 1176  			}
 1177  		}
 1178  	}
 1179  }
 1180  
 1181  void GridTileComponent::onShow()
 1182  {
 1183  	GuiComponent::onShow();	
 1184  
 1185  	if (mSelected)
 1186  		handleStoryBoard(true);
 1187  	else
 1188  	{
 1189  		if (selectStoryboard())
 1190  			startStoryboard();
 1191  
 1192  		for (auto comp : enumerateExtraChildrens())
 1193  		{
 1194  			if (comp->selectStoryboard())
 1195  				comp->startStoryboard();
 1196  			else if (comp->selectStoryboard("scroll"))
 1197  				comp->startStoryboard();
 1198  		}
 1199  	}
 1200  
 1201  	resize();
 1202  }
 1203  
 1204  void GridTileComponent::onHide()
 1205  {
 1206  	GuiComponent::onHide();		
 1207  
 1208  	if (mSelected)
 1209  	{
 1210  		if (hasStoryBoard() && isStoryBoardRunning())
 1211  			deselectStoryboard(true);
 1212  
 1213  		for (auto comp : enumerateExtraChildrens())
 1214  		{
 1215  			if (comp->hasStoryBoard() && comp->isStoryBoardRunning())
 1216  				comp->deselectStoryboard(true);
 1217  		}
 1218  	}
 1219  }
 1220  
 1221  void GridTileComponent::startVideo()
 1222  {
 1223  	if (mVideo != nullptr)
 1224  	{
 1225  		// Inform video component about size before staring in order to be able to use OptimizeVideo parameter
 1226  		if (mSelectedProperties.Image.sizeMode == "minSize")
 1227  			mVideo->setMinSize(mSelectedProperties.Size);
 1228  		else
 1229  			mVideo->setResize(mSelectedProperties.Size);
 1230  
 1231  		mVideo->setVideo(mVideoPath, false);
 1232  	}
 1233  }
 1234  
 1235  void GridTileComponent::stopVideo()
 1236  {
 1237  	if (mVideo != nullptr)
 1238  		mVideo->setVideo("");
 1239  }
 1240  
 1241  void GridTileComponent::setSelected(bool selected, bool allowAnimation, Vector3f* pPosition, bool force, bool startsVideo)
 1242  {
 1243  	if (!isShowing() || !ALLOWANIMATIONS)
 1244  		allowAnimation = false;
 1245  
 1246  	if (mSelected == selected && !force)
 1247  	{
 1248  		if (mHasItemTemplate && !mSelected)
 1249  		{
 1250  			if (selectStoryboard("scroll"))
 1251  				startStoryboard();
 1252  
 1253  			for (auto comp : enumerateExtraChildrens())
 1254  			{
 1255  				if (comp->isStoryBoardRunning("scroll"))
 1256  					comp->deselectStoryboard(false);
 1257  
 1258  				if (comp->selectStoryboard("scroll"))
 1259  					comp->startStoryboard();
 1260  			}
 1261  		}
 1262  		else if (mSelected && startsVideo)
 1263  			startVideo();
 1264  
 1265  		return;
 1266  	}
 1267  
 1268  	if (mSelected != selected)
 1269  		handleStoryBoard(selected);
 1270  
 1271  	mSelected = selected;
 1272  
 1273  	if (mHasItemTemplate)
 1274  		return;
 1275  
 1276  	if (!mSelected)
 1277  	{
 1278  		mBackground.setAnimateTiming(0);
 1279  		stopVideo();
 1280  	}
 1281  
 1282  	if (selected)
 1283  	{
 1284  		if (pPosition == NULL || !allowAnimation)
 1285  		{
 1286  			cancelAnimation(3);
 1287  
 1288  			this->setSelectedZoom(1);
 1289  			mAnimPosition = Vector3f(0, 0, 0);
 1290  
 1291  			if (startsVideo)
 1292  				startVideo();
 1293  
 1294  			resize();
 1295  		}
 1296  		else
 1297  		{
 1298  			if (pPosition == NULL)
 1299  				mAnimPosition = Vector3f(0, 0, 0);
 1300  			else
 1301  				mAnimPosition = Vector3f(pPosition->x(), pPosition->y(), pPosition->z());
 1302  
 1303  			auto func = [this](float t)
 1304  			{
 1305  				t -= 1; // cubic ease out
 1306  				float pct = Math::lerp(0, 1, t*t*t + 1);
 1307  
 1308  				this->setSelectedZoom(pct);
 1309  			};
 1310  
 1311  			cancelAnimation(3);
 1312  			setAnimation(new LambdaAnimation(func, 250), 0, [this, startsVideo] {
 1313  				this->setSelectedZoom(1);
 1314  				mAnimPosition = Vector3f(0, 0, 0);
 1315  				if (startsVideo)
 1316  					startVideo();
 1317  			}, false, 3);
 1318  		}
 1319  	}
 1320  	else // if (!selected)
 1321  	{
 1322  		if (!allowAnimation)
 1323  		{
 1324  			cancelAnimation(3);
 1325  			this->setSelectedZoom(0);
 1326  			stopVideo();
 1327  			resize();
 1328  		}
 1329  		else
 1330  		{
 1331  			this->setSelectedZoom(1);
 1332  			stopVideo();
 1333  
 1334  			auto func = [this](float t)
 1335  			{
 1336  				t -= 1; // cubic ease out
 1337  				float pct = Math::lerp(0, 1, t*t*t + 1);
 1338  				this->setSelectedZoom(1.0 - pct);
 1339  			};
 1340  
 1341  			cancelAnimation(3);
 1342  			setAnimation(new LambdaAnimation(func, 250), 0, [this] {
 1343  				this->setSelectedZoom(0);
 1344  			}, false, 3);
 1345  		}
 1346  	}
 1347  }
 1348  
 1349  void GridTileComponent::setSelectedZoom(float percent)
 1350  {
 1351  	if (mSelectedZoomPercent == percent)
 1352  		return;
 1353  
 1354  	mSelectedZoomPercent = percent;
 1355  	resize();
 1356  }
 1357  
 1358  Vector3f GridTileComponent::getBackgroundPosition()
 1359  {
 1360  	return Vector3f(mBackground.getPosition().x() + mPosition.x(), mBackground.getPosition().y() + mPosition.y(), 0);
 1361  }
 1362  
 1363  static Vector2f mixVectors(const Vector2f& def, const Vector2f& sel, float percent)
 1364  {
 1365  	if (def == sel || percent == 0)
 1366  		return def;
 1367  		
 1368  	if (percent == 1)
 1369  		return sel;
 1370  
 1371  	float x = def.x() * (1.0 - percent) + sel.x() * percent;
 1372  	float y = def.y() * (1.0 - percent) + sel.y() * percent;
 1373  	return Vector2f(x, y);	
 1374  }
 1375  
 1376  static Vector4f mixVectors(const Vector4f& def, const Vector4f& sel, float percent)
 1377  {
 1378  	if (def == sel || percent == 0)
 1379  		return def;
 1380  
 1381  	if (percent == 1)
 1382  		return sel;
 1383  
 1384  	float x = def.x() * (1.0 - percent) + sel.x() * percent;
 1385  	float y = def.y() * (1.0 - percent) + sel.y() * percent;
 1386  	float z = def.z() * (1.0 - percent) + sel.z() * percent;
 1387  	float w = def.w() * (1.0 - percent) + sel.w() * percent;
 1388  	return Vector4f(x, y, z, w);
 1389  }
 1390  
 1391  static unsigned int mixUnsigned(const unsigned int def, const unsigned int sel, float percent)
 1392  {
 1393  	if (def == sel || percent == 0)
 1394  		return def;
 1395  
 1396  	if (percent == 1)
 1397  		return sel;
 1398  
 1399  	return def * (1.0 - percent) + sel * percent;
 1400  }
 1401  
 1402  static float mixFloat(const float def, const float sel, float percent)
 1403  {
 1404  	if (def == sel || percent == 0)
 1405  		return def;
 1406  
 1407  	if (percent == 1)
 1408  		return sel;
 1409  
 1410  	return def * (1.0 - percent) + sel * percent;
 1411  }
 1412  
 1413  void GridImageProperties::mixProperties(GridImageProperties& def, GridImageProperties& sel, float percent)
 1414  {
 1415  	if (!def.Loaded)
 1416  		return;
 1417  
 1418  	using namespace Renderer;
 1419  
 1420  	pos = mixVectors(def.pos, sel.pos, percent);
 1421  	size = mixVectors(def.size, sel.size, percent);
 1422  	origin = mixVectors(def.origin, sel.origin, percent);
 1423  	color = mixColors(def.color, sel.color, percent);
 1424  	colorEnd = mixColors(def.colorEnd, sel.colorEnd, percent);
 1425  	reflexion = mixVectors(def.reflexion, sel.reflexion, percent);
 1426  	roundCorners = mixFloat(def.roundCorners, sel.roundCorners, percent);
 1427  
 1428  	customShader = percent >= 0.02f ? sel.customShader : def.customShader;
 1429  }
 1430  
 1431  void GridTextProperties::mixProperties(GridTextProperties& def, GridTextProperties& sel, float percent)
 1432  {
 1433  	if (!def.Loaded)
 1434  		return;
 1435  
 1436  	using namespace Renderer;
 1437  
 1438  	pos = mixVectors(def.pos, sel.pos, percent);
 1439  	size = mixVectors(def.size, sel.size, percent);
 1440  	color = mixColors(def.color, sel.color, percent);
 1441  	backColor = mixColors(def.backColor, sel.backColor, percent);
 1442  	glowColor = mixColors(def.glowColor, sel.glowColor, percent);
 1443  	glowSize = mixFloat(def.glowSize, sel.glowSize, percent);
 1444  	fontSize = mixFloat(def.fontSize, sel.fontSize, percent);
 1445  	padding = mixVectors(def.padding, sel.padding, percent);
 1446  }
 1447  
 1448  GridTileProperties& GridTileComponent::getCurrentProperties(bool mixValues)
 1449  {
 1450  	GridTileProperties& prop = mSelected ? mSelectedProperties : mDefaultProperties;
 1451  
 1452  	if (mSelectedZoomPercent == 0.0f || mSelectedZoomPercent == 1.0f)
 1453  		if (!mSelected || (mVideo != nullptr && !mVideo->isPlaying()))
 1454  			return prop;
 1455  
 1456  	if (mixValues)
 1457  	{
 1458  		mMixedProperties = prop;
 1459  
 1460  		GridTileProperties* from = &mDefaultProperties;
 1461  		GridTileProperties* to = &mSelectedProperties;
 1462  		float pc = mSelectedZoomPercent;
 1463  		
 1464  		if (mSelected && mVideo != nullptr && mVideo->isPlaying())
 1465  		{
 1466  			if (!mVideo->isFading() || !ALLOWANIMATIONS)
 1467  				return mVideoPlayingProperties;
 1468  
 1469  			from = &mSelectedProperties;
 1470  			to = &mVideoPlayingProperties;
 1471  
 1472  			float t = mVideo->getFade() - 1; // cubic ease in
 1473  			pc = Math::lerp(0, 1, t*t*t + 1);
 1474  		}
 1475  
 1476  		mMixedProperties.Size = mixVectors(from->Size, to->Size, pc);
 1477  		mMixedProperties.Padding = mixVectors(from->Padding, to->Padding, pc);
 1478  
 1479  		mMixedProperties.Label.mixProperties(from->Label, to->Label, pc);
 1480  		mMixedProperties.Image.mixProperties(from->Image, to->Image, pc);
 1481  		mMixedProperties.Marquee.mixProperties(from->Marquee, to->Marquee, pc);
 1482  				
 1483  		mMixedProperties.Favorite.mixProperties(from->Favorite, to->Favorite, pc);
 1484  		mMixedProperties.Cheevos.mixProperties(from->Cheevos, to->Cheevos, pc);
 1485  		mMixedProperties.ImageOverlay.mixProperties(from->ImageOverlay, to->ImageOverlay, pc);
 1486  		
 1487  		return mMixedProperties;
 1488  	}
 1489  	else if (mSelected && mVideo != nullptr && mVideo->isPlaying() && !mVideo->isFading())
 1490  		return mVideoPlayingProperties;
 1491  
 1492  	return prop;
 1493  }
 1494  
 1495  void GridTileComponent::onScreenSaverActivate()
 1496  {
 1497  	GuiComponent::onScreenSaverActivate();
 1498  
 1499  	if (mVideo)
 1500  		mVideo->onScreenSaverActivate();
 1501  }
 1502  
 1503  void GridTileComponent::onScreenSaverDeactivate()
 1504  {
 1505  	GuiComponent::onScreenSaverDeactivate();
 1506  
 1507  	if (mVideo)
 1508  		mVideo->onScreenSaverDeactivate();
 1509  }
 1510  
 1511  void GridTileComponent::forceMarquee(const std::string& path)
 1512  {
 1513  	if (mHasStandardMarquee)
 1514  	{
 1515  		setMarquee(path);
 1516  		return;
 1517  	}
 1518  
 1519  	bool isMarqueeForced = !path.empty();
 1520  
 1521  	if (isMarqueeForced)
 1522  	{
 1523  		if (mMarquee == nullptr)
 1524  		{
 1525  			createMarquee();
 1526  
 1527  			mMarquee->setOrigin(0.5, 0.5);
 1528  			mMarquee->setPosition(0.5, 0.5);
 1529  			mMarquee->setSize(0.5, 0.5);
 1530  			mMarquee->setIsLinear(true);
 1531  
 1532  			mDefaultProperties.Marquee = GridImageProperties();
 1533  			mDefaultProperties.Marquee.size = Vector2f(0.55f, 0.55f);
 1534  			mDefaultProperties.Marquee.Visible = true;
 1535  			mDefaultProperties.Marquee.Loaded = true;
 1536  			mSelectedProperties.Marquee = mDefaultProperties.Marquee;
 1537  			mSelectedProperties.Marquee.size = Vector2f(0.65f, 0.65f);
 1538  		}
 1539  
 1540  		setMarquee(path);
 1541  	}
 1542  	else if (mMarquee != nullptr)
 1543  	{
 1544  		removeChild(mMarquee);
 1545  		delete mMarquee;
 1546  		mMarquee = nullptr;
 1547  
 1548  		mCurrentMarquee = "";
 1549  	}	
 1550  }
 1551  
 1552  Vector3f GridTileComponent::getLaunchTarget()
 1553  {
 1554  	return Vector3f(getCenter().x(), getCenter().y(), 0);
 1555  }
 1556  
 1557  void GridTileComponent::updateBindings(IBindable* bindable)
 1558  {
 1559  	if (bindable != nullptr)
 1560  	{
 1561  		std::vector<IBindable*> bindables;
 1562  
 1563  		IBindable* currentParent = bindable;
 1564  
 1565  		auto childs = enumerateExtraChildrens();
 1566  		for (auto comp : childs)
 1567  		{
 1568  			auto id = comp->getTag();
 1569  			if (id.empty() || id == comp->getThemeTypeName())
 1570  				continue;
 1571  
 1572  			IBindable* bindable = new ComponentBinding(comp, currentParent);
 1573  			bindables.push_back(bindable);
 1574  
 1575  			currentParent = bindable;
 1576  		}
 1577  
 1578  		GridTemplateBinding localBinding(this, Utils::String::trim(mLabel.getText()), currentParent);
 1579  		GuiComponent::updateBindings(&localBinding);
 1580  
 1581  		for (auto bindable : bindables)
 1582  			delete bindable;
 1583  	}
 1584  	else
 1585  		GuiComponent::updateBindings(bindable);
 1586  }
 1587  
 1588  bool GridTileComponent::hasFavoriteMedia() 
 1589  { 	
 1590  	for (auto comp : enumerateExtraChildrens())
 1591  		for (auto xp : comp->getBindingExpressions())
 1592  			if (xp.second == "{game:favorite}")
 1593  				return true;
 1594  
 1595  	return mFavorite != nullptr; 
 1596  }
```

## GridTileComponent.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_COMPONENTS_GRID_TILE_COMPONENT_H
    3  #define ES_CORE_COMPONENTS_GRID_TILE_COMPONENT_H
    4  
    5  #include "NinePatchComponent.h"
    6  #include "ImageComponent.h"
    7  #include "TextComponent.h"
    8  #include "ThemeData.h"
    9  #include "resources/TextureResource.h"
   10  #include "renderers/Renderer.h"
   11  
   12  class VideoComponent;
   13  
   14  struct GridImageProperties
   15  {
   16  public:
   17  	GridImageProperties()
   18  	{
   19  		Loaded = false;
   20  		Visible  = false;
   21  
   22  		reflexion = Vector2f::Zero();
   23  		pos = Vector2f(0.5f, 0.5f);
   24  		size = Vector2f(1.0f, 1.0f);
   25  		origin = Vector2f(0.5f, 0.5f);
   26  		color = colorEnd = 0xFFFFFFFF;		
   27  		sizeMode = "maxSize";
   28  		roundCorners = 0;
   29  	}
   30  
   31  	void mixProperties(GridImageProperties& def, GridImageProperties& sel, float percent);
   32  	bool applyTheme(const ThemeData::ThemeElement* elem);
   33  
   34  	void updateImageComponent(ImageComponent* image, Vector2f offsetPos, Vector2f parentSize, bool disableSize = false)
   35  	{
   36  		if (image == nullptr)
   37  			return;
   38  
   39  		image->setPosition(offsetPos.x() + pos.x() * parentSize.x(), offsetPos.y() + pos.y() * parentSize.y());
   40  		
   41  		if (!disableSize && sizeMode == "size")
   42  			image->setSize(size.x() * parentSize.x(), size.y() * parentSize.y());
   43  		else if (sizeMode == "minSize")
   44  			image->setMinSize(size.x() * parentSize.x(), size.y() * parentSize.y());
   45  		else
   46  			image->setMaxSize(size.x() * parentSize.x(), size.y() * parentSize.y());
   47  
   48  		image->setOrigin(origin);
   49  		image->setColorShift(color);
   50  		image->setColorShiftEnd(colorEnd);
   51  		image->setMirroring(reflexion);
   52  		image->setRoundCorners(roundCorners);
   53  		image->setCustomShader(customShader);
   54  	}
   55  
   56  	bool Loaded;
   57  	bool Visible;
   58  
   59  	Vector2f pos;
   60  	Vector2f size;
   61  	Vector2f origin;
   62  	Vector2f reflexion;
   63  	
   64  	unsigned int color;
   65  	unsigned int colorEnd;
   66  
   67  	std::string  sizeMode;
   68  
   69  	Renderer::ShaderInfo customShader;
   70  
   71  	float roundCorners;
   72  };
   73  
   74  struct GridTextProperties
   75  {
   76  public:
   77  	GridTextProperties()
   78  	{
   79  		Loaded = false;
   80  		Visible = false;
   81  		
   82  		pos = Vector2f(-1, -1);
   83  		size = Vector2f(1.0f, 0.30f);		
   84  		color = 0xFFFFFFFF;
   85  		backColor = 0;		
   86  		fontSize = 0;
   87  		glowColor = 0;
   88  		glowSize = 0;
   89  		padding = Vector4f::Zero();
   90  	}
   91  
   92  	void mixProperties(GridTextProperties& def, GridTextProperties& sel, float percent);
   93  	bool applyTheme(const ThemeData::ThemeElement* elem);
   94  
   95  	void updateTextComponent(TextComponent* text, Vector2f parentSize, bool disableSize = false)
   96  	{
   97  		if (text == nullptr)
   98  			return;
   99  
  100  		text->setPosition(pos.x() * parentSize.x(), pos.y() * parentSize.y());
  101  		text->setSize(size.x() * parentSize.x(), size.y() * parentSize.y());
  102  	//	text->setPadding(padding);
  103  		text->setColor(color);
  104  		text->setBackgroundColor(backColor);
  105  		text->setGlowColor(glowColor);
  106  		text->setGlowSize(glowSize);
  107  		text->setAutoScroll(autoScroll);
  108  		// "true" / "false" force the mode; anything else leaves TextComponent's
  109  		// AUTO, which wraps only when the area clears 1.8 lines of the font's
  110  		// tallest glyph seen so far -- a moving threshold (see GuiSaveState).
  111  		if (multiLine == "true")
  112  			text->setMultiLine(TextComponent::MultiLineType::MULTILINE);
  113  		else if (multiLine == "false")
  114  			text->setMultiLine(TextComponent::MultiLineType::SINGLELINE);
  115  		else
  116  			text->setMultiLine(TextComponent::MultiLineType::AUTO);
  117  		text->setFont(fontPath, fontSize * Math::min(Renderer::getScreenHeight(), Renderer::getScreenWidth()));
  118  	}
  119  	
  120  	bool Loaded;
  121  	bool Visible;
  122  
  123  	Vector2f pos;
  124  	Vector2f size;
  125  
  126  	unsigned int color;
  127  	unsigned int backColor;
  128  
  129  	unsigned int glowColor;
  130  	float glowSize;
  131  
  132  	std::string  fontPath;
  133  	float fontSize;
  134  	bool autoScroll;
  135  	std::string multiLine;
  136  	Vector4f padding;
  137  };
  138  
  139  struct GridNinePatchProperties
  140  {
  141  public:
  142  	GridNinePatchProperties()
  143  	{
  144  		Loaded = false;
  145  		Visible = false;
  146  
  147  		edgeColor = centerColor = animateColor = 0xFFFFFFFF;
  148  		cornerSize = Vector2f(16, 16);
  149  		path = ":/frame.png";
  150  		animateTime = 0;
  151  		padding = Vector4f::Zero();
  152  		mTexture = TextureResource::get(path, false, true);
  153  	}
  154  
  155  	void setImagePath(const std::string _path)
  156  	{
  157  		path = _path;
  158  		mTexture = TextureResource::get(path, false, true);
  159  	}
  160  
  161  	bool applyTheme(const ThemeData::ThemeElement* elem);
  162  
  163  	void updateNinePatchComponent(NinePatchComponent* ctl)
  164  	{
  165  		if (ctl == nullptr)
  166  			return;
  167  
  168  		ctl->setCenterColor(centerColor);
  169  		ctl->setEdgeColor(edgeColor);
  170  		ctl->setCornerSize(cornerSize);
  171  		ctl->setAnimateTiming(animateTime);
  172  		ctl->setAnimateColor(animateColor);
  173  		ctl->setImagePath(path);
  174  		ctl->setPadding(padding);
  175  	}
  176  
  177  	bool Loaded;
  178  	bool Visible;
  179  
  180  	Vector2f	 cornerSize;
  181  	unsigned int centerColor;
  182  	unsigned int edgeColor;
  183  	std::string  path;
  184  	Vector4f	 padding;
  185  
  186  	unsigned int animateColor;
  187  	float animateTime;
  188  
  189  	// Store texture to avoid unloading & flickering
  190  	std::shared_ptr<TextureResource> mTexture;
  191  };
  192  
  193  struct GridTileProperties
  194  {
  195  	Vector2f				Size;
  196  	Vector4f				Padding;
  197  	std::string				SelectionMode;
  198  
  199  	GridNinePatchProperties Background;
  200  
  201  	GridTextProperties		Label;
  202  	GridImageProperties		Image;
  203  	GridImageProperties		Marquee;
  204  	GridImageProperties		Favorite;
  205  	GridImageProperties		Cheevos;
  206  	GridImageProperties		ImageOverlay;
  207  };
  208  
  209  class GridTileComponent : public GuiComponent
  210  {
  211  public:
  212  	GridTileComponent(Window* window);
  213  	~GridTileComponent();
  214  
  215  	std::string getThemeTypeName() override { return "gridtile"; }
  216  
  217  	void render(const Transform4x4f& parentTrans) override;
  218  
  219  	virtual void applyTheme(const std::shared_ptr<ThemeData>& theme, const std::string& view, const std::string& element, unsigned int properties);
  220  
  221  	// Made this a static function because the ImageGridComponent need to know the default tile max size
  222  	// to calculate the grid dimension before it instantiate the GridTileComponents
  223  	static Vector2f getDefaultTileSize();
  224  	Vector2f getSelectedTileSize() const;
  225  	bool isSelected() const;
  226  
  227  	void resetImages();
  228  
  229  	void setLabel(std::string name);
  230  	void setVideo(const std::string& path, float defaultDelay = -1.0);
  231  
  232  	void setImage(const std::string& path, bool isDefaultImage = false);
  233  	// The width-to-height the tile's picture is drawn at (fork #243; 0 =
  234  	// the file's own). Kept across setImage.
  235  	void setDisplayAspect(float ratio);
  236  	void setDisplayRotation(int quarterTurns);
  237  	void setMarquee(const std::string& path);
  238  	
  239  	void setFavorite(bool favorite);
  240  	void setCheevos(bool favorite);
  241  	bool hasFavoriteMedia();
  242  
  243  	void setSelected(bool selected, bool allowAnimation = true, Vector3f* pPosition = NULL, bool force = false, bool startsVideo = true);
  244  
  245  	void forceSize(Vector2f size, float selectedZoom = 1.0);
  246  
  247  	void renderBackground(const Transform4x4f& parentTrans);
  248  	void renderContent(const Transform4x4f& parentTrans, bool renderBackground = false);
  249  
  250  	bool shouldSplitRendering() { return isAnimationPlaying(3); };
  251  
  252  	Vector3f getBackgroundPosition();
  253  
  254  	virtual void onShow();
  255  	virtual void onHide();
  256  	virtual void update(int deltaTime);
  257  	virtual void onScreenSaverActivate();
  258  	virtual void onScreenSaverDeactivate();
  259  
  260  	bool isMinSizeTile();
  261  	bool hasMarquee();
  262  	void setIsDefaultImage(bool value = true) { mIsDefaultImage = value; }
  263  
  264  	void forceMarquee(const std::string& path);
  265  
  266  	std::shared_ptr<TextureResource> getTexture(bool marquee = false);
  267  
  268  	Vector3f getLaunchTarget();
  269  
  270  	void	startVideo();
  271  
  272  	void	updateBindings(IBindable* bindable) override;
  273  	bool    hasItemTemplate() { return mHasItemTemplate; }
  274  
  275  private:
  276  	void	handleStoryBoard(bool activate);
  277  	void	resetProperties();
  278  	void	createVideo();
  279  	void	createMarquee();
  280  	void	createFavorite();
  281  	void	createCheevos();
  282  	void	createImageOverlay();
  283  	void	stopVideo();
  284  
  285  	void resize();
  286  
  287  	static void applyThemeToProperties(const ThemeData::ThemeElement* elem, GridTileProperties& properties);
  288  
  289  	GridTileProperties& getCurrentProperties(bool mixValues = true);
  290  
  291  	TextComponent mLabel;
  292  
  293  	// bool mLabelVisible;
  294  	bool mLabelMerged;
  295  
  296  	NinePatchComponent mBackground;
  297  
  298  	GridTileProperties mDefaultProperties;
  299  	GridTileProperties mSelectedProperties;
  300  	GridTileProperties mMixedProperties;
  301  	GridTileProperties mVideoPlayingProperties;
  302  
  303  	std::string mCurrentMarquee;
  304  	std::string mCurrentPath;
  305  	float mDisplayAspect = 0.0f;
  306  	int mDisplayRotation = 0;
  307  	std::string mVideoPath;
  308  
  309  	void setSelectedZoom(float percent);
  310  
  311  	float mSelectedZoomPercent;
  312  	bool mSelected;	
  313  
  314  	bool mIsDefaultImage;
  315  
  316  	Vector3f mAnimPosition;
  317  
  318  	VideoComponent* mVideo;
  319  	ImageComponent* mImage;
  320  	ImageComponent* mMarquee;
  321  	ImageComponent* mFavorite;
  322  	ImageComponent* mCheevos;
  323  	ImageComponent* mImageOverlay;
  324  
  325  	bool mVideoPlaying;	
  326  	bool mHasStandardMarquee;
  327  	bool mHasItemTemplate;
  328  
  329  	bool mImageLoaded;
  330  };
  331  
  332  #endif // ES_CORE_COMPONENTS_GRID_TILE_COMPONENT_H
```

## HelpComponent.cpp (whole, fork-modified, at the pin)

```text
    1  #include "components/HelpComponent.h"
    2  
    3  #include "components/ComponentGrid.h"
    4  #include "components/ImageComponent.h"
    5  #include "components/TextComponent.h"
    6  #include "resources/TextureResource.h"
    7  #include "utils/StringUtil.h"
    8  #include "Log.h"
    9  #include "Settings.h"
   10  #include "InputConfig.h"
   11  
   12  // space between [icon] and [text] (px)
   13  #define ICON_TEXT_SPACING Renderer::getScreenWidth() * 0.0042f
   14  
   15  // space between [text] and next [icon] (px)
   16  #define ENTRY_SPACING (ICON_TEXT_SPACING * 2.0f)
   17  
   18  static const std::map<std::string, std::string> ICON_PATH_MAP
   19  {
   20  	{ "up/down", ":/help/dpad_updown.svg" },
   21  	{ "left/right", ":/help/dpad_leftright.svg" },
   22  	{ "up/down/left/right", ":/help/dpad_all.svg" },
   23  	{ "a", ":/help/button_a.svg" },
   24  	{ "b", ":/help/button_b.svg" },
   25  	{ "x", ":/help/button_x.svg" },
   26  	{ "y", ":/help/button_y.svg" },
   27  	{ "l", ":/help/button_l.svg" },
   28  	{ "r", ":/help/button_r.svg" },
   29  	{ "lr", ":/help/button_lr.svg" },
   30  	{ "start", ":/help/button_start.svg" },
   31  	{ "select", ":/help/button_select.svg" },
   32  	{ "F1", ":/help/F1.svg" }
   33  };
   34  
   35  HelpComponent::HelpComponent(Window* window) : GuiComponent(window)
   36  {
   37  	mHotItem = -1;
   38  }
   39  
   40  void HelpComponent::clearPrompts()
   41  {
   42  	mGrid.reset();
   43  	mPrompts.clear();
   44  	updateGrid();
   45  }
   46  
   47  void HelpComponent::setPrompts(const std::vector<HelpPrompt>& prompts)
   48  {
   49  	mGrid.reset();
   50  	mPrompts = prompts;
   51  	updateGrid();
   52  }
   53  
   54  void HelpComponent::setStyle(const HelpStyle& style)
   55  {
   56  	mGrid.reset();
   57  
   58  	if (mStyle.iconMap != style.iconMap)
   59  		mIconCache.clear();
   60  
   61  	mStyle = style;
   62  	updateGrid();
   63  }
   64  
   65  void HelpComponent::updateGrid()
   66  {
   67  	if (!Settings::getInstance()->getBool("ShowHelpPrompts") || mPrompts.empty())
   68  	{
   69  		mGrid.reset();
   70  		return;
   71  	}
   72  
   73  	std::shared_ptr<Font>& font = mStyle.font;
   74  
   75  	// [icon] [spacer1] [text] [spacer2]
   76  
   77  	std::vector<std::pair<std::shared_ptr<ImageComponent>, std::shared_ptr<TextComponent>>> items;
   78  
   79  	int maxWidth = Renderer::getScreenWidth() - ENTRY_SPACING;
   80  	
   81  	if (Settings::DrawClock())
   82  	{
   83  		std::string clockBuf;
   84  		if (Settings::ClockMode12())
   85  			clockBuf = "__00:00_AM_";
   86  		else
   87  			clockBuf = "__00:00_";
   88  
   89  		auto size = mStyle.font->sizeText(clockBuf);
   90  		maxWidth = Renderer::getScreenWidth() - size.x();
   91  	}
   92  
   93  	bool is43screen = Renderer::getScreenProportion() < 1.4;
   94  
   95  	float width = 0;
   96  	const float height = Math::round(font->getLetterHeight() * 1.25f);
   97  	for (auto it = mPrompts.cbegin(); it != mPrompts.cend(); it++)
   98  	{
   99  		auto icon = std::make_shared<ImageComponent>(mWindow, false);
  100  		icon->setIsLinear(true);
  101  
  102  		auto label = InputConfig::buttonLabel(it->first);
  103  
  104  		icon->setImage(getIconTexture(label));
  105  		icon->setColorShift(mStyle.iconColor);
  106  		icon->setResize(0, height);		
  107  
  108  		std::string text = Utils::String::toUpper(it->second);
  109  		
  110  		if (is43screen)
  111  		{
  112  			// Remove splitted help for 4:3 screens
  113  			auto split = text.find("/");
  114  			if (split != std::string::npos)
  115  				text = text.substr(0, split);
  116  
  117  			split = text.find("(");
  118  			if (split != std::string::npos)
  119  				text = text.substr(0, split);
  120  		}
  121  
  122  		auto lbl = std::make_shared<TextComponent>(mWindow, text, font, mStyle.textColor);
  123  		
  124  		// Measure the candidate, then keep it only if it fits. The width used
  125  		// to grow before the test, so the entry that did not fit stayed in the
  126  		// total, the grid was sized to a box wider than what it draws, and with
  127  		// origin 0.5 the prompts sat left of centre by half the dropped entry
  128  		// -- 138 px on a 640x480 French game list, where the sixth prompt also
  129  		// vanished without a word (#210).
  130  		const float entryWidth = icon->getSize().x() + lbl->getSize().x() + ICON_TEXT_SPACING + ENTRY_SPACING;
  131  		if (width + entryWidth >= maxWidth)
  132  			break;
  133  
  134  		width += entryWidth;
  135  
  136  		if (mStyle.glowSize)
  137  		{
  138  			lbl->setGlowSize(mStyle.glowSize);
  139  			lbl->setGlowColor(mStyle.glowColor);
  140  			lbl->setGlowOffset(mStyle.glowOffset.x(), mStyle.glowOffset.y());
  141  		}
  142  
  143  		items.push_back({ icon, lbl });
  144  	}
  145  
  146  	// The box is what the row draws, so the trailing spacer of the last entry
  147  	// is not part of it either: inside the size it shifted every prompt left
  148  	// of centre by half a spacer, on every screen and every page (#210).
  149  	float rowWidth = width;
  150  	if (!items.empty())
  151  		rowWidth -= ENTRY_SPACING;
  152  	if (rowWidth < 1.0f)
  153  		rowWidth = 1.0f;
  154  
  155  	mGrid = std::make_shared<ComponentGrid>(mWindow, Vector2i(items.size() * 4, 1));
  156  	mGrid->setSize(rowWidth, height);
  157  	for (unsigned int i = 0; i < items.size(); i++)
  158  	{
  159  		auto item = items.at(i);
  160  		const bool isLast = (i + 1 == items.size());
  161  
  162  		const int col = i * 4;
  163  		mGrid->setColWidthPerc(col, item.first->getSize().x() / rowWidth);
  164  		mGrid->setColWidthPerc(col + 1, ICON_TEXT_SPACING / rowWidth);
  165  		mGrid->setColWidthPerc(col + 2, item.second->getSize().x() / rowWidth);
  166  		mGrid->setColWidthPerc(col + 3, isLast ? 0.0f : ENTRY_SPACING / rowWidth);
  167  
  168  		mGrid->setEntry(item.first, Vector2i(col, 0), false, false);
  169  		mGrid->setEntry(item.second, Vector2i(col + 2, 0), false, false);
  170  	}
  171  
  172  	mGrid->setPosition(Vector3f(mStyle.position.x(), mStyle.position.y(), 0.0f));
  173  	mGrid->setOrigin(mStyle.origin);
  174  }
  175  
  176  std::shared_ptr<TextureResource> HelpComponent::getIconTexture(const std::string& name)
  177  {
  178  	auto it = mIconCache.find(name);
  179  	if (it != mIconCache.cend())
  180  		return it->second;
  181  
  182  	auto itMap = mStyle.iconMap.find(name);
  183  	if (itMap != mStyle.iconMap.end() && ResourceManager::getInstance()->fileExists(itMap->second))
  184  	{
  185  		auto tmp = TextureResource::get(itMap->second, false, false, true);
  186  		mIconCache[name] = tmp;
  187  		return tmp;
  188  	}
  189  
  190  	auto pathLookup = ICON_PATH_MAP.find(name);
  191  	if (pathLookup == ICON_PATH_MAP.cend())
  192  	{
  193  		LOG(LogError) << "Unknown help icon \"" << name << "\"!";
  194  		return nullptr;
  195  	}
  196  
  197  	if (!ResourceManager::getInstance()->fileExists(pathLookup->second))
  198  	{
  199  		LOG(LogError) << "Help icon \"" << name << "\" - corresponding image file \"" << pathLookup->second << "\" misisng!";
  200  		return nullptr;
  201  	}
  202  
  203  	std::shared_ptr<TextureResource> tex = TextureResource::get(pathLookup->second, false, false, true);
  204  	mIconCache[name] = tex;
  205  	return tex;
  206  }
  207  
  208  void HelpComponent::setOpacity(unsigned char opacity)
  209  {
  210  	GuiComponent::setOpacity(opacity);
  211  
  212  	for (auto i = 0; i < mGrid->getChildCount(); i++)
  213  		mGrid->getChild(i)->setOpacity(opacity);
  214  }
  215  
  216  void HelpComponent::render(const Transform4x4f& parentTrans)
  217  {
  218  	if (mGrid)
  219  	{		
  220  		// Optimize Help rendering by splitting texts & images rendering ( TextComponents use the same shaders programs ) // mGrid->render(trans);
  221  		Transform4x4f trans = parentTrans * getTransform() * mGrid->getTransform();
  222  		
  223  		std::vector<GuiComponent*> textComponents;
  224  
  225  		if (Settings::DebugMouse() && mHotItem >= 0)
  226  		{
  227  			auto rect = GetComponentScreenRect(trans, mGrid->getSize());
  228  
  229  			Renderer::setMatrix(trans);
  230  
  231  			int gx = 0;
  232  
  233  			for (int i = 0; i < mGrid->getGridSize().x(); i += 4)
  234  			{
  235  				int width = mGrid->getColWidth(i) + mGrid->getColWidth(i + 1) + mGrid->getColWidth(i + 2);
  236  				int spacing = mGrid->getColWidth(i + 3);
  237  
  238  				rect.x = gx - spacing / 2.0f;
  239  				rect.w = width + spacing / 2.0f;
  240  
  241  				if (mHotItem == i / 4)
  242  				{
  243  					Renderer::drawRect(rect.x, 0.0f, rect.w, rect.h, 0xFFFFFF10, 0xFFFFFF10);
  244  					break;
  245  				}
  246  
  247  				gx += width + spacing;
  248  			}
  249  		}
  250  
  251  		for (auto i = 0; i < mGrid->getChildCount(); i++)
  252  		{
  253  			auto child = mGrid->getChild(i);
  254  
  255  			if (!child->isKindOf<TextComponent>())
  256  				child->render(trans);
  257  			else
  258  				textComponents.push_back(child);
  259  		}
  260  
  261  		for (auto child : textComponents)
  262  			child->render(trans);
  263  	}
  264  }
  265  
  266  bool HelpComponent::hitTest(int x, int y, Transform4x4f& parentTransform, std::vector<GuiComponent*>* pResult)
  267  {	
  268  	bool ret = false;
  269  
  270  	if (mGrid)
  271  	{
  272  		Transform4x4f trans = parentTransform * getTransform() * mGrid->getTransform();
  273  
  274  		auto rect = Renderer::getScreenRect(trans, mGrid->getSize(), true);
  275  
  276  		if (mStyle.font->getHeight(1.5f) > Renderer::getScreenHeight() - mGrid->getPosition().y())
  277  			rect.h = Renderer::getScreenHeight() - rect.y;
  278  
  279  		if (rect.x < 20)
  280  		{
  281  			rect.w += rect.x;
  282  			rect.x = 0;
  283  		}
  284  
  285  		if (rect.contains(x, y))
  286  		{
  287  			mIsMouseOver = true;
  288  
  289  			ret = true;
  290  
  291  			if (pResult != nullptr)
  292  				pResult->push_back(this);
  293  		}
  294  		else 
  295  			mIsMouseOver = false;
  296  
  297  		mHotItem = -1;
  298  
  299  		for (int i = 0; i < mGrid->getGridSize().x(); i += 4)
  300  		{			
  301  			int width = mGrid->getColWidth(i) + mGrid->getColWidth(i + 1) + mGrid->getColWidth(i + 2) + mGrid->getColWidth(i + 3);
  302  
  303  			auto rcItem = Renderer::getScreenRect(trans, Vector2f(width, rect.h), true);
  304  			if (rcItem.contains(x, y))
  305  			{
  306  				mHotItem = i / 4;
  307  				break;
  308  			}
  309  
  310  			trans.translate(width, 0);
  311  		}
  312  	}
  313  	else
  314  		mIsMouseOver = false;
  315  
  316  	return ret;
  317  }
  318  
  319  bool HelpComponent::onMouseClick(int button, bool pressed, int x, int y)
  320  {
  321  	if (button == 1 && pressed && mHotItem >= 0 && mHotItem < mPrompts.size())
  322  	{
  323  		auto action = mPrompts[mHotItem].action;
  324  		if (action != nullptr)
  325  			action();
  326  
  327  		return true;
  328  	}
  329  
  330  	return button == 1 && mIsMouseOver;
  331  }
```

## IList.h `:259-338` (an excerpt, upstream-carried, at the pin)

```text
  259  			if (index < mCursor || mCursor >= mEntries.size())
  260  				mCursor--;
  261  
  262  			onCursorChanged(CURSOR_STOPPED);
  263  		}
  264  	}
  265  
  266  
  267  	bool listInput(int velocity) // a velocity of 0 = stop scrolling
  268  	{
  269  		PowerSaver::lock(velocity == 0);
  270  
  271  		bool sendCursorChanged = false;
  272  
  273  		// generate an onCursorChanged event in the stopped state when the user lets go of the key
  274  		if (velocity == 0 && mScrollVelocity != 0)
  275  			sendCursorChanged = true; // onCursorChanged(CURSOR_STOPPED);
  276  
  277  		mScrollVelocity = velocity;
  278  		mScrollTier = 0;
  279  		mScrollTierAccumulator = 0;
  280  		mScrollCursorAccumulator = 0;
  281  		
  282  		int prevCursor = mCursor;
  283  
  284  		if (sendCursorChanged)
  285  			onCursorChanged(CURSOR_STOPPED);
  286  		else
  287  			scroll(mScrollVelocity);
  288  
  289  		return (prevCursor != mCursor);
  290  	}
  291  
  292  	void listUpdate(int deltaTime)
  293  	{
  294  		// update the title overlay opacity
  295  		const int dir = (mScrollTier >= mTierList.count - 1) ? 1 : -1; // fade in if scroll tier is >= 1, otherwise fade out
  296  		int op = mTitleOverlayOpacity + deltaTime*dir; // we just do a 1-to-1 time -> opacity, no scaling
  297  		if(op >= 255)
  298  			mTitleOverlayOpacity = 255;
  299  		else if(op <= 0)
  300  			mTitleOverlayOpacity = 0;
  301  		else
  302  			mTitleOverlayOpacity = (unsigned char)op;
  303  
  304  		if(mScrollVelocity == 0 || size() < 2)
  305  			return;
  306  
  307  		mScrollCursorAccumulator += deltaTime;
  308  		mScrollTierAccumulator += deltaTime;
  309  
  310  		// we delay scrolling until after scroll tier has updated so isScrolling() returns accurately during onCursorChanged callbacks
  311  		// we don't just do scroll tier first because it would not catch the scrollDelay == tier length case
  312  		int scrollCount = 0;
  313  		while(mScrollCursorAccumulator >= mTierList.tiers[mScrollTier].scrollDelay)
  314  		{
  315  			mScrollCursorAccumulator -= mTierList.tiers[mScrollTier].scrollDelay;
  316  			scrollCount++;
  317  		}
  318  
  319  		// are we ready to go even FASTER?
  320  		while(mScrollTier < mTierList.count - 1 && mScrollTierAccumulator >= mTierList.tiers[mScrollTier].length)
  321  		{
  322  			mScrollTierAccumulator -= mTierList.tiers[mScrollTier].length;
  323  			mScrollTier++;
  324  		}
  325  
  326  		// actually perform the scrolling
  327  		for(int i = 0; i < scrollCount; i++)
  328  			scroll(mScrollVelocity);
  329  	}
  330  
  331  	void listRenderTitleOverlay(const Transform4x4f& /*trans*/)
  332  	{
  333  		if(size() == 0 || !mTitleOverlayFont || mTitleOverlayOpacity == 0)
  334  			return;
  335  
  336  		// we don't bother caching this because it's only two letters and will change pretty much every frame if we're scrolling
  337  		// const std::string text = getSelectedName().size() >= 2 ? getSelectedName().substr(0, 2) : "??";
  338  		
```

## IList.h `:368-408` (an excerpt, upstream-carried, at the pin)

```text
  368  		mGradient.setOpacity(mTitleOverlayOpacity);
  369  		mGradient.render(identTrans);
  370  
  371  		TextCache* cache = mTitleOverlayFont->buildTextCache(text, off.x(), off.y(), 0xFFFFFF00 | mTitleOverlayOpacity);
  372  		mTitleOverlayFont->renderTextCache(cache); // relies on mGradient's render for Renderer::setMatrix()
  373  		delete cache;
  374  	}
  375  
  376  	void scroll(int amt)
  377  	{
  378  		if(mScrollVelocity == 0 || size() < 2)
  379  			return;
  380  
  381  		int cursor = mCursor + amt;
  382  		int absAmt = amt < 0 ? -amt : amt;
  383  
  384  		// stop at the end if we've been holding down the button for a long time or
  385  		// we're scrolling faster than one item at a time (e.g. page up/down)
  386  		// otherwise, loop around
  387  		if((mLoopType == LIST_PAUSE_AT_END && (mScrollTier > 0 || absAmt > 1)) ||
  388  			mLoopType == LIST_NEVER_LOOP)
  389  		{
  390  			if(cursor < 0)
  391  			{
  392  				cursor = 0;
  393  				mScrollVelocity = 0;
  394  				mScrollTier = 0;
  395  			}else if(cursor >= size())
  396  			{
  397  				cursor = size() - 1;
  398  				mScrollVelocity = 0;
  399  				mScrollTier = 0;
  400  			}
  401  		}else{
  402  			while(cursor < 0)
  403  				cursor += size();
  404  			while(cursor >= size())
  405  				cursor -= size();
  406  		}
  407  
  408  		if (amt != 0)
```

## ImageComponent.cpp (whole, fork-modified, at the pin)

```text
    1  #include "components/ImageComponent.h"
    2  
    3  #include "resources/TextureResource.h"
    4  #include "Log.h"
    5  #include "Settings.h"
    6  #include "ThemeData.h"
    7  #include "LocaleES.h"
    8  #include "utils/FileSystemUtil.h"
    9  #include "playlists/AnimatedGifPlaylist.h"
   10  #include "playlists/M3uPlaylist.h"
   11  #include "utils/StringUtil.h"
   12  
   13  Vector2i ImageComponent::getTextureSize() const
   14  {
   15  	if (mTexture/* && mTexture->isLoaded()*/)
   16  		return mTexture->getSize();	
   17  
   18  	return Vector2i::Zero();
   19  }
   20  
   21  Vector2f ImageComponent::getSize() const
   22  {
   23  	if (mTargetIsMax && mPadding != Vector4f::Zero())
   24  	{
   25  		auto targetSize = mTargetSize - mPadding.xy() - mPadding.zw();
   26  
   27  		if (mSize.x() == targetSize.x())
   28  			return Vector2f(mSize.x() + mPadding.x() + mPadding.z(), mSize.y());
   29  		else if (mSize.y() == targetSize.y())
   30  			return Vector2f(mSize.x(), mSize.y() + mPadding.y() + mPadding.w());
   31  	}
   32  
   33  	return GuiComponent::getSize() * (mBottomRightCrop - mTopLeftCrop);
   34  }
   35  
   36  ImageComponent::ImageComponent(Window* window, bool forceLoad, bool dynamic) : GuiComponent(window),
   37  	mTargetIsMax(false), mTargetIsMin(false), mFlipX(false), mFlipY(false), mTargetSize(0, 0), mColorShift(0xFFFFFFFF),
   38  	mColorShiftEnd(0xFFFFFFFF), mColorGradientHorizontal(true), mForceLoad(forceLoad), mDynamic(dynamic),
   39  	mFadeOpacity(0), mFading(false), mRotateByTargetSize(false), mTopLeftCrop(0.0f, 0.0f), mBottomRightCrop(1.0f, 1.0f),
   40  	mReflection(0.0f, 0.0f), mSharedTexture(true), mCustomShaderEnabled(true)
   41  {
   42  	mTextureLoaded = false;
   43  	mLoadingTextureLoaded = false;
   44  	mSaturation = 1.0f;
   45  	mScaleOrigin = Vector2f::Zero();
   46  	mCheckClipping = true;
   47  
   48  	mLinear = false;
   49  	mHorizontalAlignment = ALIGN_CENTER;
   50  	mVerticalAlignment = ALIGN_CENTER;
   51  	mReflectOnBorders = false;
   52  	mAllowFading = true;
   53  	mRoundCorners = 0.0f;
   54  	
   55  	mPlaylistTimer = 0;
   56  	updateColors();
   57  }
   58  
   59  ImageComponent::~ImageComponent()
   60  {
   61  	if (mTexture != nullptr)
   62  		mTexture->setRequired(false);
   63  }
   64  
   65  void ImageComponent::setSize(float w, float h)
   66  {
   67  	if (!mTexture)
   68  	{
   69  		GuiComponent::setSize(w, h);
   70  		return;
   71  	}
   72  
   73  	auto clientSize = getClientRect();
   74  
   75  	mTargetSize = Vector2f(w, h);
   76  	mSize = mTargetSize;
   77  
   78  	resize();
   79  	onSizeChanged();
   80  
   81  	if (mChildren.size() && clientSize  != getClientRect())
   82  		recalcChildrenLayout();
   83  }
   84  
   85  void ImageComponent::resize()
   86  {
   87  	if (!mTexture || mTexture->getSize() == Vector2i::Zero()) // !mTexture->isLoaded())
   88  		return;
   89  
   90  	const Vector2f physicalSize = mTexture->getPhysicalSize();
   91  	if (physicalSize == Vector2f::Zero())
   92  		return;
   93  	// The proportions the picture is fitted at: the file's, unless a display
   94  	// aspect was set for it (fork #243) -- then the file's height at that
   95  	// width-to-height. The texture itself is untouched; only the quad is.
   96  	Vector2f textureSize = (mDisplayAspect > 0.0f && physicalSize.y() > 0.0f)
   97  		? Vector2f(physicalSize.y() * mDisplayAspect, physicalSize.y())
   98  		: physicalSize;
   99  	// A quarter turn swaps the picture's width and height (fork #245).
  100  	const bool turned = (mDisplayRotation % 2) != 0;
  101  	if (turned)
  102  		textureSize = Vector2f(textureSize.y(), textureSize.x());
  103  
  104  	auto targetSize = mTargetSize - mPadding.xy() - mPadding.zw();
  105  
  106  	if (mTexture->isTiled())
  107  	{
  108  		uncrop();
  109  		mSize = targetSize;
  110  	}
  111  	else
  112  	{
  113  		// SVG rasterization is determined by height (see SVGResource.cpp), and rasterization is done in terms of pixels
  114  		// if rounding is off enough in the rasterization step (for images with extreme aspect ratios), it can cause cutoff when the aspect ratio breaks
  115  		// so, we always make sure the resultant height is an integer to make sure cutoff doesn't happen, and scale width from that 
  116  		// (you'll see this scattered throughout the function)
  117  		// this is probably not the best way, so if you're familiar with this problem and have a better solution, please make a pull request!
  118  
  119  		if (mTargetIsMax)
  120  		{
  121  			uncrop();
  122  			mSize = textureSize;
  123  
  124  			Vector2f resizeScale((targetSize.x() / mSize.x()), (targetSize.y() / mSize.y()));
  125  
  126  			if (resizeScale.x() < resizeScale.y())
  127  			{
  128  				mSize[0] *= resizeScale.x(); // this will be mTargetSize.x(). We can't exceed it, nor be lower than it.
  129  				// we need to make sure we're not creating an image larger than max size
  130  				//mSize[1] = Math::min(Math::round(mSize[1] *= resizeScale.x()), mTargetSize.y());
  131  				mSize[1] = Math::min(mSize[1] *= resizeScale.x(), targetSize.y());
  132  			}
  133  			else
  134  			{
  135  				//mSize[1] = Math::round(mSize[1] * resizeScale.y()); // this will be mTargetSize.y(). We can't exceed it.
  136  				mSize[1] = mSize[1] * resizeScale.y(); // this will be mTargetSize.y(). We can't exceed it.
  137  
  138  				// for SVG rasterization, always calculate width from rounded height (see comment above)
  139  				// we need to make sure we're not creating an image larger than max size
  140  				mSize[0] = Math::min((mSize[1] / textureSize.y()) * textureSize.x(), targetSize.x());
  141  			}
  142  		}
  143  		else if (mTargetIsMin)
  144  		{
  145  			// mSize = ImageIO::getPictureMinSize(textureSize, mTargetSize);			
  146  			mSize = textureSize;
  147  
  148  			Vector2f resizeScale((targetSize.x() / mSize.x()), (targetSize.y() / mSize.y()));
  149  
  150  			if (resizeScale.x() > resizeScale.y())
  151  			{
  152  				mSize[0] *= resizeScale.x();
  153  				mSize[1] *= resizeScale.x();
  154  
  155  				float cropPercent = (mSize.y() - targetSize.y()) / (mSize.y() * 2);
  156  				if (turned)
  157  					crop(cropPercent, 0, cropPercent, 0);
  158  				else
  159  					crop(0, cropPercent, 0, cropPercent);
  160  			}
  161  			else
  162  			{
  163  				mSize[0] *= resizeScale.y();
  164  				mSize[1] *= resizeScale.y();
  165  
  166  				float cropPercent = (mSize.x() - targetSize.x()) / (mSize.x() * 2);
  167  				if (turned)
  168  					crop(0, cropPercent, 0, cropPercent);
  169  				else
  170  					crop(cropPercent, 0, cropPercent, 0);
  171  			}
  172  
  173  			// for SVG rasterization, always calculate width from rounded height (see comment above)
  174  			// we need to make sure we're not creating an image smaller than min size
  175  			// mSize[1] = Math::max(Math::round(mSize[1]), mTargetSize.y());
  176  			// mSize[0] = Math::max((mSize[1] / textureSize.y()) * textureSize.x(), mTargetSize.x());
  177  		}
  178  		else
  179  		{
  180  			uncrop();
  181  			// if both components are set, we just stretch
  182  			// if no components are set, we don't resize at all
  183  			mSize = targetSize == Vector2f::Zero() ? textureSize : targetSize;
  184  
  185  			// if only one component is set, we resize in a way that maintains aspect ratio
  186  			// for SVG rasterization, we always calculate width from rounded height (see comment above)
  187  			if (!targetSize.x() && targetSize.y())
  188  			{
  189  				//mSize[1] = Math::round(mTargetSize.y());
  190  				mSize[1] = targetSize.y();
  191  				mSize[0] = (mSize.y() / textureSize.y()) * textureSize.x();
  192  			}
  193  			else if (targetSize.x() && !targetSize.y())
  194  			{
  195  				//mSize[1] = Math::round((mTargetSize.x() / textureSize.x()) * textureSize.y());
  196  				mSize[1] = (targetSize.x() / textureSize.x()) * textureSize.y();
  197  				mSize[0] = (mSize.y() / textureSize.y()) * textureSize.x();
  198  			}
  199  		}
  200  	}
  201  
  202  	//mSize[0] = Math::round(mSize.x());
  203  	//mSize[1] = Math::round(mSize.y());	
  204  	//mTexture->rasterizeAt((size_t)mSize.x(), (size_t)mSize.y());
  205  
  206  	mTexture->rasterizeAt((size_t)Math::round(mSize.x()), (size_t)Math::round(mSize.y()));
  207  	onSizeChanged();
  208  }
  209  
  210  void ImageComponent::updateVertices()
  211  {
  212  	if (!mTexture || mTexture->getSize() == Vector2i::Zero())
  213  	//if (mTexture == nullptr || !mTexture->isLoaded())
  214  		return;
  215  
  216  	Vector2f     topLeft = mSize * mTopLeftCrop;
  217  	Vector2f     bottomRight = mSize * mBottomRightCrop;
  218  
  219  	Vector2f paddingOffset;
  220  
  221  	if (mPadding != Vector4f::Zero())
  222  	{
  223  		paddingOffset = mPadding.xy() - (mPadding.xy() + mPadding.zw()) * mOrigin;
  224  		topLeft += paddingOffset;
  225  		bottomRight += paddingOffset;
  226  	}
  227  
  228  	const float        px = mTexture->isTiled() ? mSize.x() / getTextureSize().x() : 1.0f;
  229  	const float        py = mTexture->isTiled() ? mSize.y() / getTextureSize().y() : 1.0f;
  230  	const unsigned int color = Renderer::convertColor(mColorShift);
  231  	const unsigned int colorEnd = Renderer::convertColor(mColorShiftEnd);
  232  
  233  	mVertices[0] = {
  234  		{ topLeft.x(),					topLeft.y()  },
  235  		{ mTopLeftCrop.x(),				py - mTopLeftCrop.y()     }, color };
  236  
  237  	mVertices[1] = {
  238  		{ topLeft.x(),					bottomRight.y() },
  239  		{ mTopLeftCrop.x(),				1.0f - mBottomRightCrop.y() }, mColorGradientHorizontal ? colorEnd : color };
  240  
  241  	mVertices[2] = {
  242  		{ bottomRight.x(),				topLeft.y()	},
  243  		{ mBottomRightCrop.x() * px,	py - mTopLeftCrop.y()     }, mColorGradientHorizontal ? color : colorEnd };
  244  
  245  	mVertices[3] = {
  246  		{ bottomRight.x(),				bottomRight.y() },
  247  		{ mBottomRightCrop.x() * px,    1.0f - mBottomRightCrop.y() }, color };
  248  
  249  	// Fix vertices for min Target
  250  	if (mTargetIsMin)
  251  	{
  252  		auto targetSize = mTargetSize - mPadding.xy() - mPadding.zw();
  253  		Vector2f targetSizePos = (mSize - targetSize) * mOrigin + paddingOffset;
  254  
  255  		float x = targetSizePos.x();
  256  		float y = targetSizePos.y();
  257  		float r = x + targetSize.x();
  258  		float b = y + targetSize.y();
  259  
  260  		mVertices[0].pos[0] = x;
  261  		mVertices[0].pos[1] = y;
  262  
  263  		mVertices[1].pos[0] = x;
  264  		mVertices[1].pos[1] = b;
  265  
  266  		mVertices[2].pos[0] = r;
  267  		mVertices[2].pos[1] = y;
  268  
  269  		mVertices[3].pos[0] = r;
  270  		mVertices[3].pos[1] = b;
  271  	}
  272  	
  273  	// Turn the picture inside the quad (fork #245): the four corners keep
  274  	// their places, the texture corners move round. The vertices are TL,
  275  	// BL, TR, BR; one turn counter-clockwise puts the picture's right edge
  276  	// at the top, so TL shows what was TR, TR what was BR, BL what was TL,
  277  	// BR what was BL. This is how RetroArch turns a core's frame for the
  278  	// display (rotation 1 = 90 degrees counter-clockwise), applied to the
  279  	// capture it did not turn.
  280  	if (mDisplayRotation != 0)
  281  	{
  282  		const Vector2f tTL = mVertices[0].tex, tBL = mVertices[1].tex, tTR = mVertices[2].tex, tBR = mVertices[3].tex;
  283  		switch (mDisplayRotation)
  284  		{
  285  		case 1: mVertices[0].tex = tTR; mVertices[2].tex = tBR; mVertices[1].tex = tTL; mVertices[3].tex = tBL; break;
  286  		case 2: mVertices[0].tex = tBR; mVertices[2].tex = tBL; mVertices[1].tex = tTR; mVertices[3].tex = tTL; break;
  287  		case 3: mVertices[0].tex = tBL; mVertices[2].tex = tTL; mVertices[1].tex = tBR; mVertices[3].tex = tTR; break;
  288  		default: break;
  289  		}
  290  	}
  291  
  292  	if (mTexture && mTexture->isScalable())
  293  	{
  294  		// For SVG images we need to round vertices in order to be precisely aligned
  295  		for (int i = 0; i < 4; ++i)
  296  			mVertices[i].pos.round();
  297  	}
  298  
  299  	if (mFlipX)
  300  	{
  301  		for (int i = 0; i < 4; ++i)
  302  			mVertices[i].tex[0] = px - mVertices[i].tex[0];
  303  	}
  304  
  305  	if (mFlipY)
  306  	{
  307  		for (int i = 0; i < 4; ++i)
  308  			mVertices[i].tex[1] = py - mVertices[i].tex[1];
  309  	}
  310  
  311  	updateColors();
  312  	updateRoundCorners();
  313  }
  314  
  315  void ImageComponent::onSizeChanged()
  316  {
  317  	GuiComponent::onSizeChanged();	
  318  	updateVertices();
  319  	recalcChildrenLayout();
  320  }
  321  
  322  void ImageComponent::setDefaultImage(const std::string& path)
  323  {
  324  	mDefaultPath = path;
  325  }
  326  
  327  void ImageComponent::setImage(const std::string&  path, bool tile, const MaxSizeInfo& maxSize, bool checkFileExists, bool allowMultiImagePlaylist)
  328  {
  329  	std::string canonicalPath = (path[0] == '{' ? "" : Utils::FileSystem::getCanonicalPath(path));
  330  	if (!mPath.empty() && mPath == canonicalPath)
  331  		return;
  332  	
  333  	if (allowMultiImagePlaylist && !canonicalPath.empty())
  334  	{
  335  		auto ext = Utils::String::toLower(Utils::FileSystem::getExtension(canonicalPath));
  336  		if (ext == ".gif" || ext == ".apng")
  337  		{
  338  			int totalFrames, frameTime;
  339  			if (ImageIO::getMultiBitmapInformation(canonicalPath, totalFrames, frameTime) && totalFrames > 0)
  340  			{
  341  				mPath = "";
  342  				mForceLoad = true; // Disable async for animated gifs
  343  
  344  				setAllowFading(false);
  345  				setPlaylist(std::make_shared<AnimatedGifPlaylist>(canonicalPath, totalFrames, frameTime));
  346  				if (!mPath.empty())
  347  					return;
  348  			}
  349  		}
  350  		else if (ext == ".m3u")
  351  		{
  352  			mPath = "";
  353  			setAllowFading(false);
  354  			setPlaylist(std::make_shared<M3uPlaylist>(canonicalPath));
  355  			if (!mPath.empty())
  356  				return;
  357  		}
  358  	}
  359  
  360  	mPath = canonicalPath;
  361  
  362  	if (mTexture != nullptr)
  363  		mTexture->setRequired(false);
  364  
  365  	// If the previous image is in the async queue, remove it
  366  	if (mLoadingTexture && mLoadingTexture.use_count() == 1 && !mLoadingTexture->isLoaded())
  367  		TextureResource::cancelAsync(mLoadingTexture);
  368  
  369  	if (mTexture && mTexture.use_count() == 1 && !mTexture->isLoaded())
  370  		TextureResource::cancelAsync(mTexture);
  371  
  372  	mLoadingTexture.reset();
  373  
  374  	MaxSizeInfo defMaxSize = MaxSizeInfo::Empty;
  375  	MaxSizeInfo* pDefaultMaxSize = nullptr;
  376  	if (maxSize.empty())
  377  	{
  378  		defMaxSize = getMaxSizeInfo();
  379  		pDefaultMaxSize = defMaxSize.empty() ? nullptr : &defMaxSize;
  380  	}
  381  
  382  	std::string shareId;
  383  
  384  	if (!mSharedTexture)
  385  	{
  386  		shareId = getTag(); // Use tag ( element name ) as the share id -> It can be shared only with elements with same exact name
  387  
  388  		if (shareId.empty())
  389  		{
  390  			uintptr_t intAddress = reinterpret_cast<uintptr_t>(this);
  391  			shareId = std::to_string(intAddress);
  392  		}
  393  	}
  394  
  395  	if (mPath.empty() || (checkFileExists && !ResourceManager::getInstance()->fileExists(mPath)))
  396  	{
  397  		if (mDefaultPath.empty() || !ResourceManager::getInstance()->fileExists(mDefaultPath))
  398  			mTexture.reset();
  399  		else
  400  			mTexture = TextureResource::get(mDefaultPath, tile, mLinear, mForceLoad, mDynamic, true, maxSize.empty() ? pDefaultMaxSize : &maxSize, shareId);
  401  	} 
  402  	else
  403  	{
  404  		if (mPlaylist != nullptr && mPlaylistCache.find(mPath) != mPlaylistCache.cend())
  405  			mTexture = mPlaylistCache[mPath];
  406  		else
  407  		{
  408  			std::shared_ptr<TextureResource> texture = TextureResource::get(mPath, tile, mLinear, mForceLoad, mDynamic, true, maxSize.empty() ? pDefaultMaxSize : &maxSize, shareId);
  409  
  410  			if (mPlaylist != nullptr)
  411  				mPlaylistCache[mPath] = texture;
  412  
  413  			if (mShowing && !mForceLoad && mDynamic && !mAllowFading && texture != nullptr && !texture->isLoaded())
  414  			{
  415  				mLoadingTexture = texture;
  416  				mLoadingTexture->reload();
  417  			}
  418  			else
  419  				mTexture = texture;
  420  		}
  421  	}
  422  
  423  	if (mShowing && mTexture != nullptr)
  424  	{
  425  		mTexture->reload();
  426  		mTexture->setRequired(true);
  427  	}
  428  
  429  	mLoadingTextureLoaded = mLoadingTexture != nullptr && mLoadingTexture->isLoaded();
  430  	mTextureLoaded = mTexture != nullptr && mTexture->isLoaded();
  431  
  432  	if (mLoadingTexture == nullptr && !mTargetSize.empty())
  433  		resize();
  434  }
  435  
  436  void ImageComponent::setImage(const char* path, size_t length, bool tile)
  437  {
  438  	mPath = "";
  439  	if (mTexture != nullptr)
  440  		mTexture->setRequired(false);
  441  
  442  	mTexture.reset();
  443  
  444  	if (path != nullptr)
  445  	{
  446  		mTexture = TextureResource::get("", tile);
  447  		mTexture->initFromMemory(path, length);
  448  	}
  449  
  450  	mTextureLoaded = mTexture != nullptr && mTexture->isLoaded();
  451  
  452  	resize();
  453  }
  454  
  455  void ImageComponent::setImage(const std::shared_ptr<TextureResource>& texture)
  456  {
  457  	if (mTexture != nullptr)
  458  		mTexture->setRequired(false);
  459  
  460  	mTexture = texture;
  461  	mTextureLoaded = mTexture != nullptr && mTexture->isLoaded();
  462  
  463  	if (isShowing() && mTexture != nullptr)
  464  		mTexture->setRequired(true);
  465  
  466  	resize();
  467  }
  468  
  469  void ImageComponent::setResize(float width, float height)
  470  {
  471  	if (mSize.x() != 0 && mSize.y() != 0 && !mTargetIsMax && !mTargetIsMin && mTargetSize.x() == width && mTargetSize.y() == height)
  472  		return;
  473  
  474  	mTargetSize = Vector2f(width, height);
  475  	mSize = mTargetSize;
  476  	mTargetIsMax = false;
  477  	mTargetIsMin = false;
  478  	resize();
  479  }
  480  
  481  void ImageComponent::setDisplayAspect(float ratio)
  482  {
  483  	if (ratio < 0.0f)
  484  		ratio = 0.0f;
  485  	if (mDisplayAspect == ratio)
  486  		return;
  487  	mDisplayAspect = ratio;
  488  	resize();
  489  }
  490  
  491  void ImageComponent::setDisplayRotation(int quarterTurns)
  492  {
  493  	quarterTurns = ((quarterTurns % 4) + 4) % 4;
  494  	if (mDisplayRotation == quarterTurns)
  495  		return;
  496  	mDisplayRotation = quarterTurns;
  497  	resize();
  498  }
  499  
  500  void ImageComponent::setMaxSize(float width, float height)
  501  {
  502  	if (mSize.x() != 0 && mSize.y() != 0 && mTargetIsMax && !mTargetIsMin && mTargetSize.x() == width && mTargetSize.y() == height)
  503  		return;
  504  	
  505  	mTargetSize = Vector2f(width, height);
  506  	mSize = mTargetSize;
  507  	mTargetIsMax = true;
  508  	mTargetIsMin = false;
  509  	resize();
  510  }
  511  
  512  void ImageComponent::setMinSize(float width, float height)
  513  {
  514  	if (mSize.x() != 0 && mSize.y() != 0 && mTargetIsMin && !mTargetIsMax && mTargetSize.x() == width && mTargetSize.y() == height)
  515  		return;
  516  
  517  	mTargetSize = Vector2f(width, height);
  518  	mSize = mTargetSize;
  519  	mTargetIsMax = false;
  520  	mTargetIsMin = true;
  521  	resize();
  522  }
  523  
  524  Vector2f ImageComponent::getRotationSize() const
  525  {
  526  	return mRotateByTargetSize ? mTargetSize : mSize;
  527  }
  528  
  529  void ImageComponent::setRotateByTargetSize(bool rotate)
  530  {
  531  	if (mRotateByTargetSize == rotate)
  532  		return;
  533  
  534  	mRotateByTargetSize = rotate;
  535  	onRotationChanged();
  536  }
  537  
  538  void ImageComponent::cropLeft(float percent)
  539  {
  540  	if (percent < 0.0f) percent = 0.0f; else if (percent > 1.0f) percent = 1.0f;
  541  	mTopLeftCrop.x() = percent;
  542  }
  543  
  544  void ImageComponent::cropTop(float percent)
  545  {
  546  	if (percent < 0.0f) percent = 0.0f; else if (percent > 1.0f) percent = 1.0f;
  547  	mTopLeftCrop.y() = percent;
  548  }
  549  
  550  void ImageComponent::cropRight(float percent)
  551  {
  552  	if (percent < 0.0f) percent = 0.0f; else if (percent > 1.0f) percent = 1.0f;
  553  	mBottomRightCrop.x() = 1.0f - percent;
  554  }
  555  
  556  void ImageComponent::cropBot(float percent)
  557  {
  558  	if (percent < 0.0f) percent = 0.0f; else if (percent > 1.0f) percent = 1.0f;
  559  	mBottomRightCrop.y() = 1.0f - percent;
  560  }
  561  
  562  void ImageComponent::crop(float left, float top, float right, float bot)
  563  {
  564  	cropLeft(left);
  565  	cropTop(top);
  566  	cropRight(right);
  567  	cropBot(bot);
  568  }
  569  
  570  void ImageComponent::uncrop()
  571  {
  572  	crop(0, 0, 0, 0);
  573  }
  574  
  575  void ImageComponent::setFlipX(bool flip)
  576  {
  577  	if (mFlipX == flip)
  578  		return;
  579  
  580  	mFlipX = flip;
  581  	updateVertices();
  582  }
  583  
  584  void ImageComponent::setFlipY(bool flip)
  585  {
  586  	if (mFlipY == flip)
  587  		return;
  588  
  589  	mFlipY = flip;
  590  	updateVertices();
  591  }
  592  
  593  void ImageComponent::setColorShift(unsigned int color)
  594  {
  595  	if (mColorShift == color && mColorShiftEnd == color)
  596  		return;
  597  
  598  	mColorShift = color;
  599  	mColorShiftEnd = color;
  600  	updateColors();
  601  }
  602  
  603  void ImageComponent::setColorShiftEnd(unsigned int color)
  604  {
  605  	if (mColorShiftEnd == color)
  606  		return;
  607  
  608  	mColorShiftEnd = color;
  609  	updateColors();
  610  }
  611  
  612  void ImageComponent::setColorGradientHorizontal(bool horizontal)
  613  {
  614  	if (mColorGradientHorizontal == horizontal)
  615  		return;
  616  
  617  	mColorGradientHorizontal = horizontal;
  618  	updateColors();
  619  }
  620  
  621  void ImageComponent::onOpacityChanged()
  622  {
  623  	updateColors();
  624  }
  625  
  626  void ImageComponent::onPaddingChanged()
  627  { 
  628  	GuiComponent::onPaddingChanged();
  629  	resize();
  630  	updateVertices(); 
  631  }
  632  
  633  void ImageComponent::updateColors()
  634  {
  635  	float opacity = (getOpacity() * (mFading ? mFadeOpacity / 255.0 : 1.0)) / 255.0;
  636  
  637  	const unsigned int color = Renderer::convertColor(mColorShift & 0xFFFFFF00 | (unsigned char)((mColorShift & 0xFF) * opacity));
  638  	const unsigned int colorEnd = Renderer::convertColor(mColorShiftEnd & 0xFFFFFF00 | (unsigned char)((mColorShiftEnd & 0xFF) * opacity));
  639  	
  640  	mVertices[0].col = color;
  641  	mVertices[1].col = mColorGradientHorizontal ? colorEnd : color;
  642  	mVertices[2].col = mColorGradientHorizontal ? color : colorEnd;
  643  	mVertices[3].col = colorEnd;
  644  }
  645  
  646  void ImageComponent::updateRoundCorners()
  647  {
  648  	if (mRoundCorners <= 0 || Renderer::shaderSupportsCornerSize(mCustomShader.path))
  649  	{
  650  		mRoundCornerStencil.clear();
  651  		return;
  652  	}
  653  
  654  	float x = 0;
  655  	float y = 0;
  656  	float size_x = mSize.x();
  657  	float size_y = mSize.y();
  658  	
  659  	if (mTargetIsMin)
  660  	{
  661  		auto targetSize = mTargetSize - mPadding.xy() - mPadding.zw();
  662  
  663  		Vector2f targetSizePos = (targetSize - mSize) * mOrigin * -1;
  664  
  665  		x = targetSizePos.x();
  666  		y = targetSizePos.y();
  667  		size_x = targetSize.x();
  668  		size_y = targetSize.y();
  669  	}
  670  
  671  	float radius = mRoundCorners < 1 ? Math::max(size_x, size_y) * mRoundCorners : mRoundCorners;
  672  	mRoundCornerStencil = Renderer::createRoundRect(x, y, size_x, size_y, radius);
  673  }
  674  
  675  void ImageComponent::render(const Transform4x4f& parentTrans)
  676  {
  677  	if (!mVisible)
  678  		return;
  679  
  680  	watchTextureLoading(); // Required when hosted in a grid/list
  681  
  682  	if (!mTextureLoaded && mTexture && !mTexture->isLoaded())
  683  	{
  684  		mTexture->bind();
  685  		return;
  686  	}
  687  
  688  	Transform4x4f trans = parentTrans * getTransform();
  689  	
  690  	// Don't use soft clip if rotation applied : let renderer do the work
  691  	if (mCheckClipping && mRotation == 0 && trans.r0().y() == 0)
  692  	{
  693  		auto rect = Renderer::getScreenRect(trans, mSize);
  694  		if (!Renderer::isVisibleOnScreen(rect))
  695  			return;
  696  	}
  697  
  698  	if (mColorShift == 0)
  699  	{
  700  		GuiComponent::renderChildren(trans);
  701  		return;
  702  	}
  703  
  704  	if (Settings::DebugMouse() && mIsMouseOver)
  705  	{
  706  		Renderer::setMatrix(trans);
  707  		Renderer::drawRect(0.0f, 0.0f, mSize.x(), mSize.y(), 0xFF000033, 0xFF000033);
  708  	}
  709  	else if (Settings::DebugImage() || (Settings::DebugMouse() && mIsMouseOver))
  710  	{
  711  		Renderer::setMatrix(trans);
  712  		Renderer::drawRect(0.0f, 0.0f, mSize.x(), mSize.y(), 0x00000033, 0x00000033);
  713  	}
  714  
  715  	if (mTexture && getOpacity() > 0)
  716  	{
  717  		Vector2f targetSizePos = (mTargetSize - mSize) * mOrigin * -1;
  718  
  719  		if(Settings::DebugImage())
  720  			Renderer::drawRect(targetSizePos.x(), targetSizePos.y(), mTargetSize.x(), mTargetSize.y(), 0xFF000033, 0xFF000033);
  721  
  722  		// actually draw the image
  723  		// The bind() function returns false if the texture is not currently loaded. A blank
  724  		// texture is bound in this case but we want to handle a fade so it doesn't just 'jump' in
  725  		// when it finally loads
  726  		if (!mTexture->bind())
  727  		{
  728  			fadeIn(false);
  729  			return;
  730  		}
  731  
  732  		beginCustomClipRect();
  733  
  734  		// Align left
  735  		if (mVerticalAlignment == ALIGN_TOP)
  736  			trans.translate(0, targetSizePos.y());
  737  		else if (mVerticalAlignment == ALIGN_BOTTOM)
  738  			trans.translate(targetSizePos.x(), targetSizePos.y() + mTargetSize.y() - mSize.y());
  739  
  740  		if (mHorizontalAlignment == ALIGN_LEFT)
  741  			trans.translate(targetSizePos.x(), 0);
  742  		else if (mHorizontalAlignment == ALIGN_RIGHT)
  743  			trans.translate(targetSizePos.x() + mTargetSize.x() - mSize.x(), targetSizePos.y());
  744  
  745  		Renderer::setMatrix(trans);
  746  
  747  		fadeIn(true);
  748  
  749  		mVertices->saturation = mSaturation;
  750  		mVertices->customShader = !mCustomShaderEnabled || mCustomShader.path.empty() ? nullptr : &mCustomShader;
  751  
  752  		if (mRoundCorners > 0 && mRoundCornerStencil.size() > 0)
  753  		{
  754  			Renderer::setStencil(mRoundCornerStencil.data(), mRoundCornerStencil.size());
  755  			Renderer::drawTriangleStrips(&mVertices[0], 4);
  756  			Renderer::disableStencil();
  757  		}
  758  		else
  759  		{
  760  			mVertices->cornerRadius = mRoundCorners < 1 ? Math::max(mSize.x(), mSize.y()) * mRoundCorners : mRoundCorners;			
  761  			Renderer::drawTriangleStrips(&mVertices[0], 4);
  762  		}
  763  
  764  		if (mReflection.x() != 0 || mReflection.y() != 0)
  765  		{
  766  			float baseOpacity = (getOpacity() * (mFading ? mFadeOpacity / 255.0 : 1.0)) / 255.0;
  767  
  768  			float alpha = baseOpacity * ((mColorShift & 0x000000ff)) / 255.0;
  769  			float alpha2 = baseOpacity * alpha * mReflection.y();
  770  
  771  			alpha *= mReflection.x();
  772  
  773  			const unsigned int colorT = Renderer::convertColor((mColorShift & 0xffffff00) + (unsigned char)(255.0*alpha));
  774  			const unsigned int colorB = Renderer::convertColor((mColorShift & 0xffffff00) + (unsigned char)(255.0*alpha2));
  775  
  776  			int h = mVertices[1].pos.y() - mVertices[0].pos.y();
  777  
  778  			if (mReflectOnBorders)
  779  				h = mTargetSize.y();
  780  
  781  			Renderer::Vertex mirrorVertices[4];
  782  
  783  			mirrorVertices[0] = {
  784  				{ mVertices[0].pos.x(), mVertices[0].pos.y() + h },
  785  				{ mVertices[0].tex.x(), mVertices[1].tex.y() },
  786  				colorT };
  787  
  788  			mirrorVertices[1] = {
  789  				{ mVertices[1].pos.x(), mVertices[1].pos.y() + h },
  790  				{ mVertices[1].tex.x(), mVertices[0].tex.y() },
  791  				colorB };
  792  
  793  			mirrorVertices[2] = {
  794  				{ mVertices[2].pos.x(), mVertices[2].pos.y() + h },
  795  				{ mVertices[2].tex.x(), mVertices[3].tex.y() },
  796  				colorT };
  797  
  798  			mirrorVertices[3] = {
  799  				{ mVertices[3].pos.x(), mVertices[3].pos.y() + h },
  800  				{ mVertices[3].tex.x(), mVertices[2].tex.y() },
  801  				colorB };
  802  
  803  			Renderer::drawTriangleStrips(&mirrorVertices[0], 4);
  804  		}
  805  
  806  		GuiComponent::renderChildren(trans);
  807  
  808  		endCustomClipRect();
  809  	}
  810  	else
  811  		GuiComponent::renderChildren(trans);
  812  }
  813  
  814  bool ImageComponent::watchTextureLoading()
  815  {
  816  	if (!mLoadingTextureLoaded && mLoadingTexture && mLoadingTexture->isLoaded())
  817  	{
  818  		if (mTexture != nullptr)
  819  			mTexture->setRequired(false);
  820  
  821  		mTexture = mLoadingTexture;
  822  		mTexture->setRequired(isShowing());
  823  		mLoadingTexture.reset();
  824  
  825  		resize();
  826  		updateVertices();
  827  		updateColors();
  828  
  829  		mLoadingTextureLoaded = true;
  830  		mTextureLoaded = true;
  831  		return true;
  832  	}
  833  
  834  	if (mTexture == nullptr)
  835  		return false;
  836  
  837  	if (!mTextureLoaded && mTexture->getSize() != Vector2i::Zero())
  838  	{
  839  		mTexture->setRequired(isShowing());
  840  
  841  		resize();
  842  		updateVertices();
  843  		updateColors();
  844  
  845  		mTextureLoaded = true;
  846  
  847  		return true;
  848  	}
  849  
  850  	return false;
  851  }
  852  
  853  void ImageComponent::fadeIn(bool textureLoaded)
  854  {
  855  	if (!mAllowFading)
  856  		return;
  857  
  858  	if (!mForceLoad)
  859  	{
  860  		if (!textureLoaded)
  861  		{
  862  			// Start the fade if this is the first time we've encountered the unloaded texture
  863  			if (!mFading)
  864  			{
  865  				// Start with a zero opacity and flag it as fading
  866  				mFadeOpacity = 0;
  867  				mFading = true;
  868  				
  869  				updateColors();
  870  			}
  871  		}
  872  		else if (mFading && textureLoaded)
  873  		{
  874  			// The texture is loaded and we need to fade it in. The fade is based on the frame rate
  875  			// and is 1/4 second if running at 60 frames per second although the actual value is not
  876  			// that important
  877  			int opacity = mFadeOpacity + 255 / 10;
  878  			// See if we've finished fading
  879  			if (opacity >= 255)
  880  			{
  881  				mFadeOpacity = 255;
  882  				mFading = false;
  883  			}
  884  			else
  885  			{
  886  				mFadeOpacity = (unsigned char)opacity;
  887  			}
  888  
  889  			// Apply the combination of the target opacity and current fade			
  890  			updateColors();
  891  		}
  892  	}
  893  }
  894  
  895  bool ImageComponent::hasImage()
  896  {
  897  	return (bool)mTexture;
  898  }
  899  
  900  void ImageComponent::applyTheme(const std::shared_ptr<ThemeData>& theme, const std::string& view, const std::string& element, unsigned int properties)
  901  {
  902  	using namespace ThemeFlags;
  903  
  904  	const ThemeData::ThemeElement* elem = theme->getElement(view, element, getThemeTypeName());
  905  	if (!elem)
  906  		return;
  907  
  908  	if (properties & ThemeFlags::SIZE)
  909  	{
  910  		Vector4f clientRectangle = getParent() ? getParent()->getClientRect() : Vector4f(0, 0, (float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
  911  		Vector2f scale = Vector2f(clientRectangle.z(), clientRectangle.w());
  912  
  913  		if (elem->has("size"))
  914  		{
  915  			auto sz = mSourceBounds.zw() = elem->get<Vector2f>("size");
  916  			setResize(elem->get<Vector2f>("size") * scale);
  917  		}
  918  		else if (elem->has("maxSize"))
  919  		{
  920  			auto sz = mSourceBounds.zw() = elem->get<Vector2f>("maxSize");
  921  			setMaxSize(elem->get<Vector2f>("maxSize") * scale);
  922  		}
  923  		else if (elem->has("minSize"))
  924  		{
  925  			auto sz = mSourceBounds.zw() = elem->get<Vector2f>("minSize");
  926  			setMinSize(elem->get<Vector2f>("minSize") * scale);
  927  		}
  928  
  929  		if (elem->has("w"))
  930  		{
  931  			auto w = mSourceBounds.z() = elem->get<float>("w");
  932  			mTargetSize = Vector2f(elem->get<float>("w") * scale.x(), mTargetSize.y());
  933  			resize();
  934  		}
  935  
  936  		if (elem->has("h"))
  937  		{
  938  			auto h = mSourceBounds.w() = elem->get<float>("h");
  939  			mTargetSize = Vector2f(mTargetSize.x(), elem->get<float>("h") * scale.y());
  940  			resize();
  941  		}
  942  	}
  943  
  944  	if (properties & COLOR)
  945  	{
  946  		if (elem->has("color"))
  947  		{
  948  			setColorShift(elem->get<unsigned int>("color"));
  949  			setColorShiftEnd(elem->get<unsigned int>("color"));
  950  		}
  951  
  952  		if (elem->has("colorEnd"))
  953  			setColorShiftEnd(elem->get<unsigned int>("colorEnd"));
  954  
  955  		if (elem->has("gradientType"))
  956  			setColorGradientHorizontal(elem->get<std::string>("gradientType").compare("horizontal"));
  957  
  958  		if (elem->has("reflexion"))
  959  			mReflection = elem->get<Vector2f>("reflexion");
  960  		else
  961  			mReflection = Vector2f::Zero();
  962  
  963  		if (elem->has("reflexionOnFrame"))
  964  			mReflectOnBorders = elem->get<bool>("reflexionOnFrame");
  965  		else
  966  			mReflectOnBorders = false;
  967  
  968  		if (elem->has("linearSmooth"))
  969  			mLinear = elem->get<bool>("linearSmooth");
  970  
  971  		if (elem->has("saturation"))
  972  			setSaturation(Math::clamp(elem->get<float>("saturation"), 0.0f, 1.0f));
  973  
  974  		if (ThemeData::parseCustomShader(elem, &mCustomShader))
  975  			updateRoundCorners();
  976  	}
  977  
  978  	if (elem->has("shared"))
  979  		mSharedTexture = elem->get<bool>("shared");
  980  
  981  	if (properties & ThemeFlags::ROTATION && elem->has("flipX"))
  982  		setFlipX(elem->get<bool>("flipX"));
  983  
  984  	if (properties & ThemeFlags::ROTATION && elem->has("flipY"))
  985  		setFlipY(elem->get<bool>("flipY"));
  986  
  987  	if (elem->has("autoFade"))
  988  		setAllowFading(elem->get<bool>("autoFade"));
  989  
  990  	if (properties & ALIGNMENT && elem->has("horizontalAlignment"))
  991  	{
  992  		std::string str = elem->get<std::string>("horizontalAlignment");
  993  		if (str == "left")
  994  			setHorizontalAlignment(ALIGN_LEFT);
  995  		else if (str == "right")
  996  			setHorizontalAlignment(ALIGN_RIGHT);
  997  		else
  998  			setHorizontalAlignment(ALIGN_CENTER);
  999  	}
 1000  
 1001  	if (properties & ALIGNMENT && elem->has("verticalAlignment"))
 1002  	{
 1003  		std::string str = elem->get<std::string>("verticalAlignment");
 1004  		if (str == "top")
 1005  			setVerticalAlignment(ALIGN_TOP);
 1006  		else if (str == "bottom")
 1007  			setVerticalAlignment(ALIGN_BOTTOM);
 1008  		else
 1009  			setVerticalAlignment(ALIGN_CENTER);
 1010  	}
 1011  
 1012  	if (properties & ALIGNMENT && elem->has("roundCorners"))
 1013  		setRoundCorners(elem->get<float>("roundCorners"));
 1014  
 1015  	GuiComponent::applyTheme(theme, view, element, properties & ~ThemeFlags::SIZE);
 1016  
 1017  	if (elem->has("default"))
 1018  		setDefaultImage(elem->get<std::string>("default"));
 1019  
 1020  	if (properties & PATH)
 1021  	{
 1022  		if (elem->has("path"))
 1023  		{
 1024  			auto path = elem->get<std::string>("path");
 1025  
 1026  			if (!path.empty() && path[0] != '{')
 1027  			{
 1028  				mPath = "";
 1029  
 1030  				if (mPlaylist == nullptr)
 1031  				{
 1032  					bool tile = (elem->has("tile") && elem->get<bool>("tile"));
 1033  					setImage(path, tile);
 1034  				}
 1035  			}
 1036  		}		
 1037  		else if (!mDefaultPath.empty() && mPlaylist == nullptr)
 1038  			setImage("");
 1039  	}
 1040  
 1041  	for (auto child : elem->children)
 1042  	{
 1043  		if (child.second.type != "shader")
 1044  			continue;
 1045  
 1046  		if (child.second.has("enabled"))
 1047  			mCustomShaderEnabled = child.second.get<bool>("enabled");
 1048  
 1049  		for (auto prop : child.second.properties)
 1050  		{
 1051  			if (prop.second.type == ThemeData::ThemeElement::Property::PropertyType::String && Utils::String::endsWith(prop.first, "_binding"))
 1052  				mBindingExpressions["shader." + Utils::String::replace(prop.first, "_binding", "")] = prop.second.s;				
 1053  		}
 1054  	}	
 1055  }
 1056  
 1057  std::vector<HelpPrompt> ImageComponent::getHelpPrompts()
 1058  {
 1059  	std::vector<HelpPrompt> ret;
 1060  	ret.push_back(HelpPrompt(BUTTON_OK, _("SELECT")));
 1061  	return ret;
 1062  }
 1063  
 1064  void ImageComponent::setPlaylist(std::shared_ptr<IPlaylist> playList)
 1065  {
 1066  	mPlaylistCache.clear();
 1067  	mPlaylist = playList;
 1068  	if (mPlaylist == nullptr)
 1069  		return;
 1070  
 1071  	auto image = mPlaylist->getNextItem();
 1072  	if (!image.empty())
 1073  		setImage(image);
 1074  	else if (!mDefaultPath.empty())
 1075  		setImage("");
 1076  }
 1077  
 1078  void ImageComponent::onShow()
 1079  {
 1080  	mPlaylistTimer = 0;
 1081  
 1082  	if (!isShowing() && mPlaylist != nullptr && !mPath.empty() && mPlaylist->getRotateOnShow())
 1083  	{
 1084  		auto item = mPlaylist->getNextItem();
 1085  		if (!item.empty())
 1086  			setImage(item); // , false, getMaxSizeInfo(), true, false);
 1087  	}
 1088  
 1089  	GuiComponent::onShow();	
 1090  
 1091  	if (mTexture != nullptr)
 1092  	{
 1093  		mTexture->reload();			
 1094  		mTexture->setRequired(true);
 1095  	}
 1096  }
 1097  
 1098  void ImageComponent::onHide()
 1099  {
 1100  	if (mTexture)
 1101  		mTexture->setRequired(false);
 1102  
 1103  	if (mShowing)
 1104  	{
 1105  		if (mLoadingTexture)
 1106  		{
 1107  			int count = mLoadingTexture.use_count();
 1108  			if (count == 1 && !mLoadingTexture->isLoaded())
 1109  				TextureResource::cancelAsync(mLoadingTexture);
 1110  		}
 1111  
 1112  		if (mTexture)
 1113  		{
 1114  			int count = mTexture.use_count();
 1115  			if (count == 1 && !mTexture->isLoaded())
 1116  				TextureResource::cancelAsync(mTexture);
 1117  		}
 1118  	}
 1119  
 1120  	GuiComponent::onHide();
 1121  }
 1122  
 1123  void ImageComponent::update(int deltaTime)
 1124  {
 1125  	GuiComponent::update(deltaTime);
 1126  
 1127  	watchTextureLoading(); // Required when preloading
 1128  
 1129  	if (mPlaylist && isShowing())
 1130  	{
 1131  		mPlaylistTimer += deltaTime;
 1132  
 1133  		if (mPlaylistTimer >= mPlaylist->getDelay())
 1134  		{
 1135  			auto item = mPlaylist->getNextItem();
 1136  			if (!item.empty())
 1137  			{
 1138  				// LOG(LogDebug) << "getNextItem: " << item;
 1139  				setImage(item); // , false, getMaxSizeInfo(), true, false);
 1140  			}
 1141  
 1142  			mPlaylistTimer = 0.0;
 1143  		}
 1144  	}
 1145  }
 1146  
 1147  bool ImageComponent::isTiled()
 1148  { 
 1149  	return mTexture != nullptr && mTexture->isTiled(); 
 1150  }
 1151  
 1152  ThemeData::ThemeElement::Property ImageComponent::getProperty(const std::string name)
 1153  {
 1154  	Vector2f scale = getParent() ? getParent()->getSize() : Vector2f((float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
 1155  
 1156  	if (name == "size" || name == "maxSize" || name == "minSize")
 1157  		return mSize / scale;
 1158  	else if (name == "color")
 1159  		return mColorShift;
 1160  	else if (name == "colorEnd")
 1161  		return mColorShiftEnd;
 1162  	else if (name == "reflexion")
 1163  		return mReflection;
 1164  	else if (name == "roundCorners")
 1165  		return mRoundCorners;
 1166  	else if (name == "path")
 1167  		return mPath;
 1168  	else if (name == "default")
 1169  		return mDefaultPath;
 1170  	else if (name == "saturation")
 1171  		return mSaturation;
 1172  	else if (name == "autoFade")
 1173  		return mAllowFading;
 1174  	else if (name == "shader.enabled")
 1175  		return mCustomShaderEnabled;
 1176  	else if (Utils::String::startsWith(name, "shader."))
 1177  	{
 1178  		auto prop = name.substr(7);
 1179  
 1180  		auto it = mCustomShader.parameters.find(prop);
 1181  		if (it != mCustomShader.parameters.cend())
 1182  			return Utils::String::toFloat(it->second);
 1183  
 1184  		return 0.0f;
 1185  	}
 1186  	
 1187  	return GuiComponent::getProperty(name);
 1188  }
 1189  
 1190  void ImageComponent::setProperty(const std::string name, const ThemeData::ThemeElement::Property& value)
 1191  {	
 1192  	Vector2f scale = getParent() ? getParent()->getSize() : Vector2f((float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
 1193  	
 1194  	if (value.type == ThemeData::ThemeElement::Property::PropertyType::Float && name == "w")
 1195  	{
 1196  		mSourceBounds.z() = value.f;
 1197  		mTargetSize = Vector2f(value.f * scale.x(), mTargetSize.y());
 1198  		resize();
 1199  	}
 1200  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Float && name == "h")
 1201  	{
 1202  		mSourceBounds.w() = value.f;
 1203  		mTargetSize = Vector2f(mTargetSize.x(), value.f * scale.y());
 1204  		resize();
 1205  	}	
 1206  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Pair && (name == "maxSize" || name == "minSize"))
 1207  	{
 1208  		mSourceBounds.zw() = value.v;
 1209  		mTargetSize = Vector2f(value.v.x() * scale.x(), value.v.y() * scale.y());
 1210  		resize();
 1211  	}
 1212  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Int && name == "color")
 1213  	{
 1214  		if (mColorShift == mColorShiftEnd)
 1215  			setColorShift(value.i);
 1216  		else
 1217  		{
 1218  			mColorShift = value.i;			
 1219  			updateColors();
 1220  		}
 1221  	}
 1222  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Bool && name == "autoFade")
 1223  		setAllowFading(value.b);
 1224  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Int && name == "colorEnd")
 1225  		setColorShiftEnd(value.i);
 1226  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Pair && name == "reflexion")
 1227  		mReflection = value.v;
 1228  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Float && name == "roundCorners")
 1229  		setRoundCorners(value.f);
 1230  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::String && name == "default")
 1231  	{
 1232  		if (mDefaultPath != value.s && !value.s.empty() && Utils::FileSystem::exists(value.s) && mPath.empty())
 1233  		{
 1234  			setDefaultImage(value.s);
 1235  			setImage("");
 1236  		}
 1237  		else
 1238  			mDefaultPath = value.s;
 1239  	}
 1240  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::String && name == "path")
 1241  		setImage(value.s); // , false, getMaxSizeInfo()
 1242  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Float && name == "saturation")
 1243  		setSaturation(value.f);
 1244  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Bool && name == "shader.enabled")
 1245  		mCustomShaderEnabled = (bool)(int)value.b;
 1246  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Float && Utils::String::startsWith(name, "shader."))
 1247  	{
 1248  		auto prop = name.substr(7);
 1249  
 1250  		if (prop == "enabled")
 1251  			mCustomShaderEnabled = (bool) (int) value.f;
 1252  		else
 1253  		{
 1254  			 auto it = mCustomShader.parameters.find(prop);
 1255  			 if (it != mCustomShader.parameters.cend())
 1256  				 it->second = std::to_string(value.f);
 1257  			// mCustomShader.parameters[prop] = std::to_string(value.f);
 1258  		}
 1259  	}
 1260  	else
 1261  		GuiComponent::setProperty(name, value);
 1262  }
 1263  
 1264  void ImageComponent::setRoundCorners(float value) 
 1265  { 
 1266  	if (mRoundCorners == value)
 1267  		return;
 1268  		
 1269  	mRoundCorners = value; 
 1270  	updateRoundCorners();
 1271  }
 1272  
 1273  void ImageComponent::setCustomShader(const Renderer::ShaderInfo& customShader)
 1274  { 
 1275  	Renderer::ShaderInfo sav = mCustomShader;
 1276  	mCustomShader = customShader; 
 1277  
 1278  	// Restore property values that were set by evaluator
 1279  	if (sav.path == customShader.path)
 1280  	{
 1281  		for (auto param : customShader.parameters)
 1282  		{
 1283  			if (param.second.empty())
 1284  			{
 1285  				auto it = sav.parameters.find(param.first);
 1286  				if (it != sav.parameters.cend() && !it->second.empty())
 1287  				{
 1288  					mCustomShader.parameters[it->first] = it->second;
 1289  				}
 1290  			}
 1291  		}
 1292  	}
 1293  
 1294  	updateRoundCorners();
 1295  }
 1296  
 1297  void ImageComponent::setSaturation(float saturation)
 1298  {
 1299  	mSaturation = saturation;
 1300  }
 1301  
 1302  void ImageComponent::recalcLayout()
 1303  {
 1304  	if (mExtraType != ExtraType::EXTRACHILDREN || !getParent())
 1305  		return;
 1306  
 1307  	Vector4f clientRectangle = getParent()->getClientRect();
 1308  	Vector2f newPos = mSourceBounds.xy() * clientRectangle.zw() + clientRectangle.xy();
 1309  	Vector2f newSize = mSourceBounds.zw() * clientRectangle.zw();
 1310  
 1311  	if (mPosition.v2() != newPos)
 1312  		setPosition(newPos.x(), newPos.y());
 1313  
 1314  	if (mSize != newSize)
 1315  	{
 1316  		if (mTargetIsMax)
 1317  			setMaxSize(newSize);
 1318  		else if (mTargetIsMin)
 1319  			setMinSize(newSize);
 1320  		else
 1321  			setResize(newSize);
 1322  	}
 1323  }
 1324  
 1325  const MaxSizeInfo ImageComponent::getMaxSizeInfo()
 1326  {
 1327  	if (!mSize.empty())
 1328  	{
 1329  		float maxScale = 1.0f;
 1330  
 1331  		/*
 1332  		float maxScale = Math::max(1.0f, mScale);
 1333  
 1334  		GuiComponent* comp = this;
 1335  		while (comp != nullptr)
 1336  		{
 1337  			for (auto storyBoard : comp->getStoryBoards())
 1338  			{
 1339  				if (storyBoard.second == nullptr)
 1340  					continue;
 1341  
 1342  				for (auto anim : storyBoard.second->animations)
 1343  				{
 1344  					if (anim->propertyName != "scale")
 1345  						continue;
 1346  
 1347  					if (comp == this)
 1348  					{
 1349  						if (anim->from.type == ThemeData::ThemeElement::Property::PropertyType::Float && anim->from.f > maxScale)
 1350  							maxScale = anim->from.f;
 1351  
 1352  						if (anim->to.type == ThemeData::ThemeElement::Property::PropertyType::Float && anim->to.f > maxScale)
 1353  							maxScale = anim->to.f;
 1354  					}
 1355  					else
 1356  					{
 1357  						float localScale = 1.0f;
 1358  
 1359  						if (anim->from.type == ThemeData::ThemeElement::Property::PropertyType::Float && anim->from.f > localScale)
 1360  							localScale = anim->from.f;
 1361  
 1362  						if (anim->to.type == ThemeData::ThemeElement::Property::PropertyType::Float && anim->to.f > localScale)
 1363  							localScale = anim->to.f;
 1364  
 1365  						maxScale *= localScale;
 1366  					}
 1367  				}
 1368  			}
 1369  
 1370  			comp = comp->getParent();
 1371  		}
 1372  		*/
 1373  		if (mTargetSize.empty())
 1374  		{
 1375  			auto size = mSize - mPadding.xy() - mPadding.zw();
 1376  			size *= maxScale;
 1377  
 1378  			// Make sure it's not bigger that screen res
 1379  			if (size.x() > Renderer::getScreenWidth() || size.y() > Renderer::getScreenHeight())
 1380  				size = ImageIO::adjustPictureSizeF(size, Vector2f(Renderer::getScreenWidth(), Renderer::getScreenHeight()), mTargetIsMin);
 1381  
 1382  			if (size.x() > 32 && size.y() > 32)
 1383  				return MaxSizeInfo(size, mTargetIsMin);
 1384  
 1385  			return MaxSizeInfo::Empty;
 1386  		}
 1387  
 1388  		auto targetSize = mTargetSize - mPadding.xy() - mPadding.zw();
 1389  		targetSize *= maxScale;
 1390  
 1391  		// Make sure it's not bigger that screen res
 1392  		if (targetSize.x() > Renderer::getScreenWidth() || targetSize.y() > Renderer::getScreenHeight())
 1393  			targetSize = ImageIO::adjustPictureSizeF(targetSize, Vector2f(Renderer::getScreenWidth(), Renderer::getScreenHeight()), mTargetIsMin);
 1394  
 1395  		if (targetSize.x() > 32 && targetSize.y() > 32)
 1396  			return MaxSizeInfo(targetSize, mTargetIsMin);
 1397  	}
 1398  
 1399  	return MaxSizeInfo::Empty;
 1400  }
```

## ImageComponent.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_COMPONENTS_IMAGE_COMPONENT_H
    3  #define ES_CORE_COMPONENTS_IMAGE_COMPONENT_H
    4  
    5  #include "renderers/Renderer.h"
    6  #include "math/Vector2i.h"
    7  #include "GuiComponent.h"
    8  #include "ImageIO.h"
    9  #include "resources/Font.h"
   10  
   11  class TextureResource;
   12  class MaxSizeInfo;
   13  
   14  class IPlaylist
   15  {
   16  public:
   17  	virtual std::string getNextItem() = 0;
   18  	virtual int getDelay() { return 10000; }
   19  	virtual bool getRotateOnShow() { return false; }
   20  };
   21  
   22  class ImageComponent : public GuiComponent
   23  {
   24  public:
   25  	ImageComponent(Window* window, bool forceLoad = false, bool dynamic = true);
   26  	virtual ~ImageComponent();
   27  
   28  	std::string getThemeTypeName() override { return "image"; }
   29  
   30  	std::string getValue() const override { return mPath.empty() ? mDefaultPath : mPath; }
   31  
   32  	void setDefaultImage(const std::string& path);
   33  
   34  	//Loads the image at the given filepath. Will tile if tile is true (retrieves texture as tiling, creates vertices accordingly).
   35  	virtual void setImage(const std::string& path, bool tile = false, const MaxSizeInfo& maxSize = MaxSizeInfo::Empty, bool checkFileExists = true, bool allowMultiImagePlaylist = true);
   36  
   37  	//Loads an image from memory.
   38  	void setImage(const char* image, size_t length, bool tile = false);
   39  	//Use an already existing texture.
   40  	void setImage(const std::shared_ptr<TextureResource>& texture);
   41  
   42  	void onSizeChanged() override;
   43  	void onOpacityChanged() override;
   44  
   45  	// Resize the image to fit this size. If one axis is zero, scale that axis to maintain aspect ratio.
   46  	// If both are non-zero, potentially break the aspect ratio.  If both are zero, no resizing.
   47  	// Can be set before or after an image is loaded.
   48  	// setMaxSize() and setResize() are mutually exclusive.
   49  	void setResize(float width, float height);
   50  	inline void setResize(const Vector2f& size) { setResize(size.x(), size.y()); }
   51  
   52  	// Resize the image to be as large as possible but fit within a box of this size.
   53  	// Can be set before or after an image is loaded.
   54  	// Never breaks the aspect ratio. setMaxSize() and setResize() are mutually exclusive.
   55  	void setMaxSize(float width, float height);
   56  	inline void setMaxSize(const Vector2f& size) { setMaxSize(size.x(), size.y()); }
   57  
   58  	void setMinSize(float width, float height);
   59  	inline void setMinSize(const Vector2f& size) { setMinSize(size.x(), size.y()); }
   60  
   61  	Vector2f getRotationSize() const override;
   62  
   63  	// Applied AFTER image positioning and sizing
   64  	// cropTop(0.2) will crop 20% of the top of the image.
   65  	void cropLeft(float percent);
   66  	void cropTop(float percent);
   67  	void cropRight(float percent);
   68  	void cropBot(float percent);
   69  	void crop(float left, float top, float right, float bot);
   70  	void uncrop();
   71  
   72  	// Multiply all pixels in the image by this color when rendering.
   73  	void setColorShift(unsigned int color);
   74  	void setColorShiftEnd(unsigned int color);
   75  	void setColorGradientHorizontal(bool horizontal);
   76  	virtual void setColor(unsigned int color) { setColorShift(color); }
   77  
   78  	void setFlipX(bool flip); // Mirror on the X axis.
   79  	void setFlipY(bool flip); // Mirror on the Y axis.
   80  
   81  	void setRotateByTargetSize(bool rotate);  // Flag indicating if rotation should be based on target size vs. actual size.
   82  
   83  	// Returns the size of the current texture, or (0, 0) if none is loaded.  May be different than drawn size (use getSize() for that).
   84  	Vector2i getTextureSize() const;
   85  
   86  	Vector2f getSize() const override;
   87  	void	 setSize(float w, float h) override;
   88  	void	 setSize(const Vector2f& size) override { setSize(size.x(), size.y()); }
   89  
   90  	bool hasImage();
   91  
   92  	void render(const Transform4x4f& parentTrans) override;
   93  
   94  	virtual void applyTheme(const std::shared_ptr<ThemeData>& theme, const std::string& view, const std::string& element, unsigned int properties) override;
   95  
   96  	virtual std::vector<HelpPrompt> getHelpPrompts() override;
   97  
   98  	void setAllowFading(bool fade) { mAllowFading = fade; };
   99  	void setMirroring(Vector2f mirror) { mReflection = mirror; };
  100  
  101  	std::shared_ptr<TextureResource> getTexture() { return mTexture; };
  102  
  103  	const MaxSizeInfo getMaxSizeInfo();
  104  	void setHorizontalAlignment(Alignment align) { mHorizontalAlignment = align; }
  105  	void setVerticalAlignment(Alignment align) { mVerticalAlignment = align; }
  106  
  107  	float getRoundCorners() { return mRoundCorners; }
  108  	void setRoundCorners(float value);
  109  
  110  	void onShow() override;
  111  	void onHide() override;
  112  	void update(int deltaTime) override;
  113  	void onPaddingChanged() override;
  114  
  115  	void setPlaylist(std::shared_ptr<IPlaylist> playList);
  116  
  117  	std::string getImagePath() { return mPath; }
  118  	bool isTiled();
  119  
  120  	bool isLinear() { return mLinear; }
  121  	void setIsLinear(bool value) { mLinear = value; }
  122  
  123  	ThemeData::ThemeElement::Property getProperty(const std::string name) override;
  124  	void setProperty(const std::string name, const ThemeData::ThemeElement::Property& value) override;
  125  	void setTargetIsMax() { mTargetIsMax = true; }
  126  	bool getTargetIsMax() { return mTargetIsMax; }
  127  	// Draw the picture at this width-to-height instead of the file's own
  128  	// (0 = the file's). For a screenshot or a save-state thumbnail RetroArch
  129  	// wrote at the core's native size -- NES 256x240 for a 4:3 picture --
  130  	// the file's proportions are the pixel grid, not what was on screen
  131  	// (fork #243, D-UI-080). Every sizing mode respects it; the picture is
  132  	// scaled, never cropped differently.
  133  	void setDisplayAspect(float ratio);
  134  	float getDisplayAspect() const { return mDisplayAspect; }
  135  	// Quarter turns counter-clockwise the picture is shown at inside its
  136  	// layout box (fork #245, D-UI-081): a vertical arcade game's capture is
  137  	// the core's landscape frame, which RetroArch turns for the display and
  138  	// the capture does not. The texture coordinates turn, the quad stays.
  139  	void setDisplayRotation(int quarterTurns);
  140  	int getDisplayRotation() const { return mDisplayRotation; }
  141  
  142  	void setSaturation(float saturation);
  143  	void setCustomShader(const Renderer::ShaderInfo& customShader);
  144  
  145  	Vector2f& getTargetSize() { return mTargetSize; }
  146  
  147  protected:
  148  	std::shared_ptr<TextureResource> mTexture;
  149  	bool mTextureLoaded;
  150  
  151  	std::shared_ptr<TextureResource> mLoadingTexture;
  152  	bool mLoadingTextureLoaded;
  153  	
  154  	Vector2f mTargetSize;
  155  
  156  	void	recalcLayout() override;
  157  
  158  private:
  159  	bool mFlipX, mFlipY, mTargetIsMax, mTargetIsMin;
  160  
  161  	// Calculates the correct mSize from our resizing information (set by setResize/setMaxSize).
  162  	// Used internally whenever the resizing parameters or texture change.
  163  
  164  	Renderer::Vertex mVertices[4];
  165  
  166  	void updateVertices();
  167  	void updateColors();
  168  	void updateRoundCorners();
  169  	bool watchTextureLoading();
  170  
  171  	void fadeIn(bool textureLoaded);
  172  
  173  	unsigned int mColorShift;
  174  	unsigned int mColorShiftEnd;
  175  	bool mColorGradientHorizontal;
  176  
  177  	std::string mDefaultPath;
  178  
  179  	unsigned char			mFadeOpacity;
  180  	bool					mFading;
  181  	bool					mForceLoad;
  182  	bool					mDynamic;
  183  	bool					mRotateByTargetSize;
  184  
  185  	Vector2f mTopLeftCrop;
  186  	Vector2f mBottomRightCrop;
  187  
  188  	Vector2f mReflection;
  189  	bool     mReflectOnBorders;
  190  	bool	 mSharedTexture;
  191  	bool mAllowFading;
  192  
  193  	std::string mPath;
  194  	float mDisplayAspect = 0.0f;
  195  	int mDisplayRotation = 0;
  196  
  197  	Alignment mHorizontalAlignment;
  198  	Alignment mVerticalAlignment;
  199  
  200  	float mRoundCorners;
  201  	float mSaturation;
  202  
  203  	Renderer::ShaderInfo mCustomShader;
  204  	bool				 mCustomShaderEnabled;
  205  	
  206  	std::shared_ptr<IPlaylist> mPlaylist;
  207  	std::map<std::string, std::shared_ptr<TextureResource>> mPlaylistCache;
  208  
  209  	float mPlaylistTimer;
  210  
  211  	bool mLinear;	
  212  
  213  	std::vector<Renderer::Vertex>	mRoundCornerStencil;
  214  
  215  protected:
  216  	virtual void resize();
  217  	bool mCheckClipping;
  218  };
  219  
  220  #endif // ES_CORE_COMPONENTS_IMAGE_COMPONENT_H
```

## ImageGridComponent.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #include <functional>
    3  #ifndef ES_CORE_COMPONENTS_IMAGE_GRID_COMPONENT_H
    4  #define ES_CORE_COMPONENTS_IMAGE_GRID_COMPONENT_H
    5  
    6  #include "Log.h"
    7  #include "components/IList.h"
    8  #include "resources/TextureResource.h"
    9  #include "GridTileComponent.h"
   10  #include "animations/LambdaAnimation.h"
   11  #include "Settings.h"
   12  #include "Sound.h"
   13  #include <algorithm>
   14  #include "LocaleES.h"
   15  #include "components/ScrollbarComponent.h"
   16  #include <set>
   17  #include "InputManager.h"
   18  #include "utils/Delegate.h"
   19  #include "BindingManager.h"
   20  
   21  #define EXTRAITEMS 2
   22  #define ALLOWANIMATIONS (Settings::PowerSaverMode() != "instant" && Settings::TransitionStyle() != "instant")
   23  #define HOLD_TIME 1000
   24  
   25  enum ScrollDirection
   26  {
   27  	SCROLL_VERTICALLY,
   28  	SCROLL_HORIZONTALLY
   29  };
   30  
   31  enum ImageSource
   32  {
   33  	THUMBNAIL,
   34  	IMAGE,
   35  	MARQUEE,
   36  	MARQUEEORTEXT,
   37  	FANART,
   38  	TITLESHOT,
   39  	BOXART,
   40  	CARTRIDGE,
   41  	BOXBACK,
   42  	MIX
   43  };
   44  
   45  enum CenterSelection
   46  {
   47  	FULL,
   48  	PARTIAL,
   49  	NEVER
   50  };
   51  
   52  
   53  struct ImageGridData
   54  {
   55  	std::shared_ptr<GridTileComponent> tile;
   56  	std::string texturePath;
   57  };
   58  
   59  // Type trait to check if a type derives from IBindable
   60  template <typename T>
   61  struct is_bindable : std::is_base_of<IBindable, std::remove_pointer_t<T>> {};
   62  
   63  template<typename T>
   64  class ImageGridComponent : public IList<ImageGridData, T>
   65  {
   66  protected:
   67  	using IList<ImageGridData, T>::mEntries;
   68  	using IList<ImageGridData, T>::mScrollTier;
   69  	using IList<ImageGridData, T>::listUpdate;
   70  	using IList<ImageGridData, T>::listInput;
   71  	using IList<ImageGridData, T>::listRenderTitleOverlay;
   72  	using IList<ImageGridData, T>::getTransform;
   73  	using IList<ImageGridData, T>::mSize;
   74  	using IList<ImageGridData, T>::mCursor;
   75  	using IList<ImageGridData, T>::mShowing;
   76  	using IList<ImageGridData, T>::mVisible;
   77  	using IList<ImageGridData, T>::Entry;
   78  	using IList<ImageGridData, T>::mWindow;
   79  
   80  public:
   81  	using IList<ImageGridData, T>::size;
   82  	using IList<ImageGridData, T>::isScrolling;
   83  	using IList<ImageGridData, T>::stopScrolling;
   84  	using IList<ImageGridData, T>::updateBindings;
   85  
   86  	ImageGridComponent(Window* window);
   87  
   88  	std::string getThemeTypeName() override { return "imagegrid"; }
   89  
   90  	void add(const std::string& name, const std::string& imagePath, const T& obj);
   91  	virtual void clear();
   92  
   93  	void setImage(const std::string& imagePath, const T& obj);
   94  	// Every tile's picture drawn at this width-to-height (fork #243; 0 =
   95  	// each file's own): the save state manager's thumbnails are one
   96  	// system's, and RetroArch wrote them at the core's native size.
   97  	// Called for each tile once it has its entry, for a grid whose tiles
   98  	// differ one from the next (the SCREENSHOTS system: each file its own
   99  	// game's aspect and rotation, fork #245).
  100  	void setTileDecorator(const std::function<void(GridTileComponent*, const T&)>& decorator) { mTileDecorator = decorator; }
  101  	std::string getImage(const T& obj);
  102  
  103  	bool input(InputConfig* config, Input input) override;
  104  	void update(int deltaTime) override;
  105  	void render(const Transform4x4f& parentTrans) override;
  106  	virtual void applyTheme(const std::shared_ptr<ThemeData>& theme, const std::string& view, const std::string& element, unsigned int properties) override;
  107  
  108  	void onSizeChanged() override;
  109  	inline void setCursorChangedCallback(const std::function<void(CursorState state)>& func) { mCursorChangedCallback = func; }
  110  
  111  	void setThemeName(std::string name) { mName = name; };
  112  
  113  	virtual void topWindow(bool isTop);
  114  	virtual void onShow();
  115  	virtual void onHide();
  116  	virtual void onScreenSaverActivate();
  117  	virtual void onScreenSaverDeactivate();
  118  
  119  	virtual void setOpacity(unsigned char opacity);
  120  
  121  	ImageSource		getImageSource() { return mImageSource; };
  122  
  123  	void setGridSizeOverride(Vector2f size);
  124  
  125  	std::shared_ptr<GridTileComponent> getSelectedTile();
  126  
  127  	void resetLastCursor() { mLastCursor = -1; mLastCursorState = CursorState::CURSOR_STOPPED; }
  128  	int getLastCursor() { return mLastCursor; }
  129  
  130  	virtual bool onMouseClick(int button, bool pressed, int x, int y) override;
  131  	virtual void onMouseMove(int x, int y) override;
  132  	virtual bool onMouseWheel(int delta) override;
  133  	virtual bool hitTest(int x, int y, Transform4x4f& parentTransform, std::vector<GuiComponent*>* pResult = nullptr) override;
  134  
  135  	Vector3f getCameraOffset() 
  136  	{ 
  137  		if (isVertical())
  138  			return Vector3f(0, mCameraOffset, 0);
  139  
  140  		return Vector3f(mCameraOffset,  0, 0);
  141  	}
  142  
  143  	Delegate<ILongMouseClickEvent> longMouseClick;
  144  
  145  	void		preloadTiles();
  146  
  147  protected:
  148  	virtual void onCursorChanged(const CursorState& state) override;
  149  	virtual void onScroll(int /*amt*/) { if (!mScrollSound.empty()) Sound::get(mScrollSound)->play(); }
  150  
  151  private:
  152  	void		resetGrid();
  153  	void		calcGridDimension();
  154  	
  155  	void		ensureVisibleTileExist();
  156  	Vector2i	getVisibleRange();
  157  	void		loadTile(std::shared_ptr<GridTileComponent> tile, typename IList<ImageGridData, T>::Entry& entry);
  158  	std::shared_ptr<GridTileComponent> createTile(int i, int dimOpposite, Vector2f tileDistance, Vector2f startPosition);
  159  
  160  	inline bool isVertical() { return mScrollDirection == SCROLL_VERTICALLY; };
  161  
  162  	bool mEntriesDirty;
  163  
  164  	int mLastCursor;
  165  	CursorState mLastCursorState;
  166  
  167  	std::string mDefaultGameTexture;
  168  	std::string mDefaultFolderTexture;
  169  	std::string mDefaultLogoBackgroundTexture;
  170  
  171  	std::vector<std::shared_ptr<GridTileComponent>> mVisibleTiles;
  172  
  173  	// TILES
  174  	bool mLastRowPartial;
  175  	bool mAnimateSelection;
  176  	Vector2f mAutoLayout;
  177  	float mAutoLayoutZoom;
  178  	Vector4f mPadding;
  179  	Vector2f mMargin;
  180  	Vector2f mTileSize;
  181  	std::function<void(GridTileComponent*, const T&)> mTileDecorator;
  182  	Vector2i mGridDimension;
  183  	Vector2f mGridSizeOverride;
  184  
  185  	std::string mScrollSound;
  186  
  187  	std::shared_ptr<ThemeData> mTheme;
  188  
  189  	std::string mName;
  190  
  191  	int mStartPosition;
  192  
  193  	bool mAllowVideo;
  194  	float mVideoDelay;
  195  
  196  	// MISCELLANEOUS
  197  	CenterSelection mCenterSelection;
  198  
  199  	bool mScrollLoop;
  200  
  201  	ScrollDirection mScrollDirection;
  202  	ImageSource		mImageSource;
  203  
  204  	ScrollbarComponent mScrollbar;
  205  
  206  	std::function<void(CursorState state)> mCursorChangedCallback;
  207  
  208  	// Mouse
  209  	int		  mPressedCursor;
  210  	Vector2i  mPressedPoint;
  211  	bool	  mIsDragging;
  212  	int		  mTimeHoldingButton;
  213  
  214  	float mTotalHeight;
  215  	float mCameraOffset;
  216  
  217  	std::map<int, std::shared_ptr<GridTileComponent>> mScrollLoopTiles;
  218  
  219  	// Handle pointer types derived from IBindable
  220  	template <typename U = T>
  221  	typename std::enable_if<is_bindable<U>::value, IBindable*>::type
  222  		getBindable(const typename IList<ImageGridData, T>::Entry& entry)
  223  	{
  224  		IBindable* bindingPtr = static_cast<IBindable*>(entry.object);
  225  		return bindingPtr;
  226  	}
  227  
  228  	// Handle other types
  229  	template <typename U = T>
  230  	typename std::enable_if<!is_bindable<U>::value, IBindable*>::type
  231  		getBindable(const typename IList<ImageGridData, T>::Entry& entry)
  232  	{
  233  		return nullptr;
  234  	}
  235  };
  236  
  237  
  238  
  239  template<typename T>
  240  Vector2i ImageGridComponent<T>::getVisibleRange()
  241  {
  242  	int dimExt = isVertical() ? mGridDimension.y() : mGridDimension.x();
  243  	int dimOpposite = Math::max(1, isVertical() ? mGridDimension.x() : mGridDimension.y());
  244  
  245  	Vector2f tileDistance = mTileSize + mMargin;
  246  
  247  	int position = mCameraOffset / (isVertical() ? tileDistance.y() : tileDistance.x()) * dimOpposite;
  248  
  249  	int startIndex = position - EXTRAITEMS * dimOpposite;
  250  	int endIndex = startIndex + dimExt * dimOpposite;
  251  
  252  	return Vector2i(startIndex, endIndex);
  253  }
  254  
  255  template<typename T>
  256  std::shared_ptr<GridTileComponent> ImageGridComponent<T>::createTile(int i, int dimOpposite, Vector2f tileDistance, Vector2f startPosition)
  257  {
  258  	// Create tiles
  259  	auto tile = std::make_shared<GridTileComponent>(mWindow);
  260  
  261  	int X = i % (int)dimOpposite;
  262  	int Y = i / (int)dimOpposite;
  263  
  264  	if (i < 0)
  265  	{
  266  		X = (i + mEntries.size() - 1) % (int)dimOpposite;
  267  		Y = ((i + mEntries.size() - 1) / (int)dimOpposite) - ((mEntries.size() - 1) / (int)dimOpposite);
  268  	}
  269  
  270  	if (!isVertical())
  271  		std::swap(X, Y);
  272  
  273  	tile->setOrigin(0.5f, 0.5f);
  274  	tile->setPosition(X * tileDistance.x() + startPosition.x(), Y * tileDistance.y() + startPosition.y());
  275  	tile->setSize(mTileSize);
  276  
  277  	if (mTheme)
  278  		tile->applyTheme(mTheme, mName, "gridtile", ThemeFlags::ALL);
  279  
  280  	if (mAutoLayout.x() != 0 && mAutoLayout.y() != 0)
  281  		tile->forceSize(mTileSize, mAutoLayoutZoom);
  282  
  283  	return tile;
  284  }
  285  
  286  template<typename T>
  287  void ImageGridComponent<T>::preloadTiles()
  288  {
  289  	int dimOpposite = Math::max(1, isVertical() ? mGridDimension.x() : mGridDimension.y());
  290  
  291  	Vector2f startPosition = mTileSize / 2;
  292  	startPosition += Vector2f(mPadding.x(), mPadding.y());
  293  
  294  	Vector2f tileDistance = mTileSize + mMargin;
  295  
  296  	for (int i = 0; i < mEntries.size(); i++)
  297  	{
  298  		typename IList<ImageGridData, T>::Entry& entry = mEntries[i];
  299  		if (entry.data.tile != nullptr)
  300  			continue;
  301  
  302  		auto tile = createTile(i, dimOpposite, tileDistance, startPosition);
  303  		tile->setVisible(false);
  304  
  305  		loadTile(tile, entry);
  306  		
  307  		entry.data.tile = tile;
  308  		if (mTileDecorator)
  309  			mTileDecorator(tile.get(), entry.object);
  310  	}
  311  }
  312  
  313  template<typename T>
  314  void ImageGridComponent<T>::ensureVisibleTileExist()
  315  {
  316  	if (mEntries.size() == 0 || mGridDimension.y() == 0 || mGridDimension.x() == 0)
  317  		return;
  318  
  319  	int dimOpposite = Math::max(1, isVertical() ? mGridDimension.x() : mGridDimension.y());
  320  
  321  	Vector2f tileDistance = mTileSize + mMargin;
  322  
  323  	auto range = getVisibleRange();
  324  	int startIndex = range.x(); // position - EXTRAITEMS * dimOpposite;
  325  	int endIndex = range.y(); // startIndex + dimExt * dimOpposite;
  326  
  327  	if (startIndex < 0)
  328  		startIndex = 0;
  329  
  330  	if (endIndex > mEntries.size() - 1)
  331  		endIndex = mEntries.size() - 1;
  332  
  333  	int totalCols = Math::max(0, mEntries.size() - 1) / dimOpposite;
  334  	mTotalHeight = Math::max(0.0f, (float) (isVertical() ? tileDistance.y() : tileDistance.x()) * (totalCols - 1));
  335  
  336  	Vector2f startPosition = mTileSize / 2;
  337  	startPosition += Vector2f(mPadding.x(), mPadding.y());
  338  
  339  	auto oldScrollLoopTiles = mScrollLoopTiles;	
  340  	mScrollLoopTiles.clear();
  341  
  342  	int from = mScrollLoop ? Math::min(range.x(), 0) : 0;
  343  	int to = mScrollLoop ? Math::max(range.y(), mEntries.size()) : mEntries.size();
  344  
  345  	for (int idx = from; idx < to; idx++)
  346  	{
  347  		int i = idx;
  348  
  349  		if (mScrollLoop)
  350  		{
  351  			int min = dimOpposite == 1 ? 0 : (mEntries.size() % dimOpposite) - dimOpposite;
  352  			int max = mEntries.size() - min;
  353  
  354  			if (i < min)
  355  			{
  356  				while (i < min)
  357  					i += max;
  358  			}
  359  			else if (i >= max)
  360  			{
  361  				while (i >= max)
  362  					i -= max;
  363  			}
  364  
  365  			if (i < 0 || i >= mEntries.size())
  366  				continue;
  367  		}
  368  
  369  		typename IList<ImageGridData, T>::Entry& entry = mEntries[i];
  370  
  371  		if ((mScrollLoop && idx >= range.x() && idx <= range.y()) || (!mScrollLoop && i >= startIndex && i <= endIndex))
  372  		{
  373  			if (entry.data.tile == nullptr)
  374  			{
  375  				// Create tiles
  376  				auto tile = createTile(i, dimOpposite, tileDistance, startPosition);
  377  				loadTile(tile, entry);
  378  
  379  				entry.data.tile = tile;
  380  		if (mTileDecorator)
  381  			mTileDecorator(tile.get(), entry.object);
  382  
  383  				if (tile->isVisible())
  384  					mVisibleTiles.push_back(tile);
  385  
  386  				if (mCursor == i)
  387  				{
  388  					auto curTile = getSelectedTile();
  389  					while (curTile != nullptr)
  390  					{
  391  						curTile->setSelected(false, false, nullptr, true);
  392  						curTile = getSelectedTile();
  393  					}
  394  
  395  					mLastCursor = mCursor;
  396  					tile->setSelected(true, true, nullptr, true);
  397  				}
  398  
  399  				if (mShowing)
  400  					tile->onShow();
  401  			}
  402  			else if (!entry.data.tile->isVisible())
  403  			{
  404  				loadTile(entry.data.tile, entry);
  405  				entry.data.tile->setVisible(true);
  406  
  407  				mVisibleTiles.push_back(entry.data.tile);
  408  
  409  				if (mShowing)
  410  					entry.data.tile->onShow();
  411  			}
  412  
  413  			if (mScrollLoop && i < startIndex || i > endIndex)
  414  			{
  415  				auto tile = createTile(idx, dimOpposite, tileDistance, startPosition);
  416  				loadTile(tile, entry);
  417  				// The loop copy is the same entry drawn again at the other end,
  418  				// so it takes the same decoration (a screenshot's turn and
  419  				// aspect, fork #243/#245); the two creation sites above did
  420  				// and this one did not (audit #258 PL-017).
  421  				if (mTileDecorator)
  422  					mTileDecorator(tile.get(), entry.object);
  423  				mScrollLoopTiles[idx] = tile;
  424  			}
  425  		}
  426  		else if (entry.data.tile != nullptr)
  427  		{
  428  			if (entry.data.tile->isVisible())
  429  				entry.data.tile->setVisible(false);
  430  
  431  			auto it = std::find(mVisibleTiles.cbegin(), mVisibleTiles.cend(), entry.data.tile);
  432  			if (it != mVisibleTiles.cend())
  433  				mVisibleTiles.erase(it);
  434  
  435  			if (!mShowing)
  436  			{				
  437  				entry.data.tile->resetImages();
  438  				entry.data.tile = nullptr;
  439  			}
  440  			else if (entry.data.tile->isShowing())
  441  				entry.data.tile->onHide();
  442  		}
  443  	}
  444  }
  445  
  446  template<typename T>
  447  ImageGridComponent<T>::ImageGridComponent(Window* window) : IList<ImageGridData, T>(window), mScrollbar(window)
  448  {
  449  	Vector2f screen = Vector2f((float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
  450  
  451  	mCameraOffset = 0;
  452  	mTotalHeight = 0;
  453  
  454  	mPressedCursor = -1;
  455  	mPressedPoint = Vector2i(-1, -1);
  456  	mIsDragging = false;
  457  	mTimeHoldingButton = -1;
  458  
  459  	mGridSizeOverride = Vector2f::Zero();
  460  	mAutoLayout = Vector2f::Zero();
  461  	mAutoLayoutZoom = 1.0;
  462  
  463  	mVideoDelay = 750;
  464  	mAllowVideo = false;
  465  	mName = "grid";
  466  	mStartPosition = 0;
  467  	mEntriesDirty = true;
  468  
  469  	mLastCursor = -1;
  470  	mLastCursorState = CursorState::CURSOR_STOPPED;
  471  
  472  	mDefaultGameTexture = ":/cartridge.svg";
  473  	mDefaultFolderTexture = ":/folder.svg";
  474  	mDefaultLogoBackgroundTexture = "";
  475  
  476  	mAnimateSelection = true;
  477  	mSize = screen * 0.80f;
  478  	mMargin = screen * 0.07f;
  479  	mPadding = Vector4f::Zero();
  480  	mTileSize = GridTileComponent::getDefaultTileSize();
  481  
  482  	mImageSource = THUMBNAIL;
  483  
  484  	mCenterSelection = CenterSelection::NEVER;
  485  	mScrollLoop = false;
  486  	mScrollDirection = SCROLL_VERTICALLY;
  487  
  488  	mCursorChangedCallback = nullptr;
  489  }
  490  
  491  template<typename T>
  492  void ImageGridComponent<T>::add(const std::string& name, const std::string& imagePath, const T& obj)
  493  {
  494  	typename IList<ImageGridData, T>::Entry entry;
  495  	entry.name = name;
  496  	entry.object = obj;
  497  	entry.data.texturePath = imagePath;
  498  
  499  	static_cast<IList< ImageGridData, T >*>(this)->add(entry);
  500  
  501  	mEntriesDirty = true;
  502  }
  503  
  504  template<typename T>
  505  void ImageGridComponent<T>::clear()
  506  {	
  507  	IList<ImageGridData, T>::clear();
  508  	resetGrid();
  509  }
  510  
  511  template<typename T>
  512  std::string ImageGridComponent<T>::getImage(const T& obj)
  513  {
  514  	IList<ImageGridData, T>* list = static_cast<IList< ImageGridData, T >*>(this);
  515  	auto entry = list->findEntry(obj);
  516  	if (entry != list->end())
  517  		return (*entry).data.texturePath;
  518  
  519  	return "";
  520  }
  521  
  522  template<typename T>
  523  void ImageGridComponent<T>::setImage(const std::string& imagePath, const T& obj)
  524  {
  525  	IList<ImageGridData, T>* list = static_cast<IList< ImageGridData, T >*>(this);
  526  	auto entry = list->findEntry(obj);
  527  	if (entry != list->end() && (*entry).data.texturePath != imagePath)
  528  	{
  529  		(*entry).data.texturePath = imagePath;
  530  		(*entry).data.tile = nullptr;
  531  
  532  		mEntriesDirty = true;
  533  	}
  534  }
  535  
  536  template<typename T>
  537  bool ImageGridComponent<T>::input(InputConfig* config, Input input)
  538  {
  539  	if (input.value != 0)
  540  	{
  541  		int idx = isVertical() ? 0 : 1;
  542  		float dimScrollable = isVertical() ? mGridDimension.y() - 2 * EXTRAITEMS : mGridDimension.x() - 2 * EXTRAITEMS;
  543  
  544  		Vector2i dir = Vector2i::Zero();
  545  
  546  		if (config->isMappedLike("up", input))
  547  			dir[1 ^ idx] = -1;
  548  		else if (config->isMappedLike("down", input))
  549  			dir[1 ^ idx] = 1;
  550  		else if (config->isMappedLike("left", input))
  551  			dir[0 ^ idx] = -1;
  552  		else if (config->isMappedLike("right", input))
  553  			dir[0 ^ idx] = 1;
  554  		else  if (config->isMappedTo("leftshoulder", input))
  555  		{
  556  			if (isVertical())
  557  				dir[1 ^ idx] = -dimScrollable;
  558  			else
  559  				dir[0 ^ idx] = -dimScrollable;
  560  		}
  561  		else if (config->isMappedTo("rightshoulder", input))
  562  		{
  563  			if (isVertical())
  564  				dir[1 ^ idx] = dimScrollable;
  565  			else
  566  				dir[0 ^ idx] = dimScrollable;
  567  		}
  568  
  569  		if (dir != Vector2i::Zero())
  570  		{
  571  			if (isVertical())
  572  				listInput(dir.x() + dir.y() * mGridDimension.x());
  573  			else
  574  				listInput(dir.x() + dir.y() * mGridDimension.y());
  575  
  576  			return true;
  577  		}
  578  	}
  579  	else
  580  	{
  581  		if (config->isMappedLike("up", input) || config->isMappedLike("down", input) ||
  582  			config->isMappedLike("left", input) || config->isMappedLike("right", input) ||
  583  			config->isMappedTo("rightshoulder", input) || config->isMappedTo("leftshoulder", input))
  584  		{
  585  			stopScrolling();
  586  		}
  587  	}
  588  
  589  	return GuiComponent::input(config, input);
  590  }
  591  
  592  template<typename T>
  593  void ImageGridComponent<T>::update(int deltaTime)
  594  {
  595  	GuiComponent::update(deltaTime);
  596  
  597  	if (mTimeHoldingButton >= 0)
  598  	{
  599  		mTimeHoldingButton += deltaTime;
  600  
  601  		if (mTimeHoldingButton >= HOLD_TIME)
  602  		{
  603  			mTimeHoldingButton = -1;
  604  			mPressedCursor = -1;
  605  			mPressedPoint = Vector2i(-1, -1);
  606  
  607  			longMouseClick.invoke([&](ILongMouseClickEvent* c) { c->onLongMouseClick(this); });
  608  		}
  609  	}
  610  
  611  	mScrollbar.update(deltaTime);
  612  
  613  	listUpdate(deltaTime);
  614  
  615  	if (mEntriesDirty)
  616  	{
  617  		ensureVisibleTileExist();
  618  		mEntriesDirty = false;
  619  	}
  620  
  621  	for (auto tile : mVisibleTiles)
  622  		tile->update(deltaTime);
  623  	/*
  624  	for (auto entry : mEntries)
  625  		if (entry.data.tile != nullptr && entry.data.tile->isVisible())
  626  			entry.data.tile->update(deltaTime);
  627  	*/
  628  }
  629  
  630  template<typename T>
  631  void ImageGridComponent<T>::topWindow(bool isTop)
  632  {
  633  	GuiComponent::topWindow(isTop);
  634  
  635  	for (auto entry : mEntries)
  636  		if (entry.data.tile != nullptr)
  637  			entry.data.tile->topWindow(isTop);
  638  }
  639  
  640  template<typename T>
  641  void ImageGridComponent<T>::setOpacity(unsigned char opacity)
  642  {
  643  	GuiComponent::setOpacity(opacity);
  644  
  645  	for (auto entry : mEntries)
  646  		if (entry.data.tile != nullptr)
  647  			entry.data.tile->setOpacity(opacity);
  648  }
  649  
  650  template<typename T>
  651  void ImageGridComponent<T>::onShow()
  652  {
  653  	GuiComponent::onShow();
  654  
  655  	for (auto entry : mEntries)
  656  		if (entry.data.tile != nullptr)
  657  			entry.data.tile->onShow();
  658  }
  659  
  660  template<typename T>
  661  void ImageGridComponent<T>::onHide()
  662  {
  663  	GuiComponent::onHide();
  664  
  665  	for (auto entry : mEntries)
  666  		if (entry.data.tile != nullptr)
  667  			entry.data.tile->onHide();
  668  
  669  	ensureVisibleTileExist();
  670  	mEntriesDirty = false;
  671  }
  672  
  673  template<typename T>
  674  void ImageGridComponent<T>::onScreenSaverActivate()
  675  {
  676  	GuiComponent::onScreenSaverActivate();
  677  
  678  	for (auto entry : mEntries)
  679  		if (entry.data.tile != nullptr)
  680  			entry.data.tile->onScreenSaverActivate();
  681  }
  682  
  683  template<typename T>
  684  void ImageGridComponent<T>::onScreenSaverDeactivate()
  685  {
  686  	GuiComponent::onScreenSaverDeactivate();
  687  
  688  	for (auto entry : mEntries)
  689  		if (entry.data.tile != nullptr)
  690  			entry.data.tile->onScreenSaverDeactivate();
  691  }
  692  
  693  
  694  template<typename T>
  695  void ImageGridComponent<T>::setGridSizeOverride(Vector2f size)
  696  {
  697  	mGridSizeOverride = size;
  698  }
  699  
  700  template<typename T>
  701  std::shared_ptr<GridTileComponent> ImageGridComponent<T>::getSelectedTile()
  702  {
  703  	for (auto tile : mVisibleTiles)
  704  		if (tile->isSelected())
  705  			return tile;
  706  
  707  	for (auto entry : mEntries)
  708  		if (entry.data.tile != nullptr)
  709  			if (entry.data.tile->isSelected())
  710  				return entry.data.tile;
  711  
  712  	return nullptr;
  713  }
  714  
  715  template<typename T>
  716  void ImageGridComponent<T>::render(const Transform4x4f& parentTrans)
  717  {
  718  	if (!mVisible)
  719  		return;
  720  
  721  	Transform4x4f trans = parentTrans * getTransform();
  722  	Transform4x4f tileTrans = trans;
  723  
  724  	auto rect = Renderer::getScreenRect(trans, mSize);
  725  	if (!Renderer::isVisibleOnScreen(rect))
  726  		return;
  727  
  728  	if (Settings::DebugGrid())
  729  	{
  730  		Renderer::setMatrix(trans);
  731  		Renderer::drawRect(0.0f, 0.0f, mSize.x(), mSize.y(), 0xFF000033);
  732  
  733  		for (auto tile : mVisibleTiles)
  734  		{
  735  			auto tt = trans * tile->getTransform();
  736  			tt.translate(isVertical() ? 0 : -mCameraOffset, isVertical() ? -mCameraOffset : 0);
  737  
  738  			Renderer::setMatrix(tt);
  739  			Renderer::drawRect(0.0, 0.0, tile->getSize().x(), tile->getSize().y(), 0x00FF0033);
  740  		}
  741  
  742  		Renderer::setMatrix(parentTrans);
  743  	}
  744  
  745  	bool splittedRendering = (mAnimateSelection && mAutoLayout.x() != 0);
  746  
  747  	Vector2i pos(rect.x, rect.y);
  748  	Vector2i size(rect.w, rect.h);
  749  
  750  	if (mAutoLayout == Vector2f::Zero() && mLastRowPartial) // If the last row is partial in Retropie, extend clip to show the entire last row 
  751  		size.y() = (mTileSize + mMargin).y() * (mGridDimension.y() - 2 * EXTRAITEMS);
  752  
  753  	Renderer::pushClipRect(pos, size);
  754  
  755  	float dimScrollable = isVertical() ? mGridDimension.y() - 2 * EXTRAITEMS : mGridDimension.x() - 2 * EXTRAITEMS;
  756  	float dimOpposite = Math::max(1, isVertical() ? mGridDimension.x() : mGridDimension.y());
  757  	
  758  	tileTrans.translate(isVertical() ? 0 : -mCameraOffset, isVertical() ? -mCameraOffset : 0);
  759  
  760  	std::shared_ptr<GridTileComponent> selectedTile;
  761  
  762  	for (auto scrollLoopTile : mScrollLoopTiles)
  763  		scrollLoopTile.second->render(tileTrans);
  764  
  765  	for (auto tile : mVisibleTiles)
  766  	{
  767  		if (tile->isSelected())
  768  		{
  769  			selectedTile = tile;
  770  			if (splittedRendering && tile->shouldSplitRendering())
  771  				tile->renderBackground(tileTrans);
  772  		}
  773  		else
  774  			tile->render(tileTrans);
  775  	}
  776  
  777  	// Render the selected image content on top of the others
  778  	if (selectedTile != nullptr)
  779  	{
  780  		if (splittedRendering && selectedTile->shouldSplitRendering())
  781  			selectedTile->renderContent(tileTrans);
  782  		else
  783  			selectedTile->render(tileTrans);
  784  	}
  785  
  786  	Renderer::popClipRect();
  787  
  788  	listRenderTitleOverlay(trans);
  789  	GuiComponent::renderChildren(trans);
  790  
  791  	if (mScrollbar.isEnabled() && !mScrollLoop)
  792  	{
  793  		Vector3f pos = GuiComponent::getPosition();
  794  		Vector2f sz = GuiComponent::getSize();
  795  
  796  		if (isVertical())
  797  		{
  798  			pos.y() += mPadding.y();
  799  			sz.y() -= mPadding.y() + mPadding.w();
  800  		}
  801  		else
  802  		{
  803  			pos.x() += mPadding.x();
  804  			sz.x() -= mPadding.x() + mPadding.z();
  805  		}
  806  
  807  		auto scrollableSize = mTileSize + mMargin;
  808  
  809  		mScrollbar.setContainerBounds(pos, sz, isVertical());
  810  		mScrollbar.setRange(0, mTotalHeight + (isVertical() ? scrollableSize.y() : scrollableSize.y()), isVertical() ? scrollableSize.y() : scrollableSize.y());
  811  		mScrollbar.setScrollPosition(mCameraOffset);
  812  		mScrollbar.render(parentTrans);
  813  	}
  814  }
  815  
  816  template<typename T>
  817  void ImageGridComponent<T>::applyTheme(const std::shared_ptr<ThemeData>& theme, const std::string& view, const std::string& element, unsigned int properties)
  818  {
  819  	// Keep the theme pointer to apply it on the tiles later on
  820  	mTheme = nullptr;
  821  
  822  	// Apply theme to GuiComponent but not size property, which will be applied at the end of this function
  823  	GuiComponent::applyTheme(theme, view, element, properties ^ ThemeFlags::SIZE);
  824  
  825  	Vector2f screen = Vector2f((float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
  826  
  827  	mScrollbar.fromTheme(theme, view, element, "imagegrid");
  828  
  829  	const ThemeData::ThemeElement* elem = theme->getElement(view, element, "imagegrid");
  830  	if (elem)
  831  	{
  832  		if (elem->has("margin"))
  833  		{
  834  			auto margin = elem->get<Vector2f>("margin");
  835  			if (abs(margin.x()) < 1 && abs(margin.y()) < 1)
  836  				mMargin = margin * screen;
  837  			else
  838  				mMargin = margin; // Pixel size
  839  		}
  840  
  841  		if (elem->has("padding"))
  842  		{
  843  			auto padding = elem->get<Vector4f>("padding");
  844  			if (abs(padding.x()) < 1 && abs(padding.y()) < 1 && abs(padding.z()) < 1 && abs(padding.w()) < 1)
  845  				mPadding = padding * Vector4f(screen.x(), screen.y(), screen.x(), screen.y());
  846  			else 
  847  				mPadding = padding; // Pixel size
  848  		}
  849  
  850  		if (elem->has("autoLayout"))
  851  		{
  852  			mAutoLayout = elem->get<Vector2f>("autoLayout");
  853  
  854  			float screenProportion = (float)Renderer::getScreenWidth() / (float)Renderer::getScreenHeight();
  855  
  856  			if (properties & ThemeFlags::SIZE && elem->has("size"))
  857  			{
  858  				Vector2f scale = GuiComponent::getParent() ? GuiComponent::getParent()->getSize() : Vector2f((float)Renderer::getScreenWidth(), (float)Renderer::getScreenHeight());
  859  				auto size = elem->get<Vector2f>("size") * scale;
  860  				if (size.y() != 0)
  861  					screenProportion = size.x() / size.y();
  862  			}
  863  
  864  			float cellProportion = 1;
  865  			if (elem->has("cellProportion"))
  866  			{
  867  				cellProportion = elem->get<float>("cellProportion");
  868  				if (cellProportion == 0)
  869  					cellProportion = 1;
  870  			}
  871  
  872  			if (mAutoLayout.y() == 0)
  873  				mAutoLayout.y() = Math::round(mAutoLayout.x() / screenProportion * cellProportion);
  874  			else if (mAutoLayout.x() == 0)
  875  				mAutoLayout.x() = Math::round(mAutoLayout.y() * screenProportion / cellProportion);
  876  		}
  877  
  878  		if (elem->has("animateSelection"))
  879  			mAnimateSelection = elem->get<bool>("animateSelection");
  880  
  881  		if (elem->has("autoLayoutSelectedZoom"))
  882  			mAutoLayoutZoom = elem->get<float>("autoLayoutSelectedZoom");
  883  
  884  		if (elem->has("imageSource"))
  885  		{
  886  			auto direction = elem->get<std::string>("imageSource");
  887  			if (direction == "image")
  888  				mImageSource = IMAGE;
  889  			else if (direction == "marquee")
  890  				mImageSource = MARQUEE;
  891  			else if (direction == "marqueeortext")
  892  				mImageSource = MARQUEEORTEXT;
  893  			else if (direction == "fanart")
  894  				mImageSource = FANART;
  895  			else if (direction == "titleshot")
  896  				mImageSource = TITLESHOT;
  897  			else if (direction == "boxart")
  898  				mImageSource = BOXART;
  899  			else if (direction == "cartridge")
  900  				mImageSource = CARTRIDGE;
  901  			else if (direction == "boxback")
  902  				mImageSource = BOXBACK;
  903  			else if (direction == "mix")
  904  				mImageSource = MIX;
  905  			else
  906  				mImageSource = THUMBNAIL;
  907  		}
  908  		else
  909  			mImageSource = THUMBNAIL;
  910  
  911  		if (elem->has("scrollDirection"))
  912  		{
  913  			auto direction = elem->get<std::string>("scrollDirection");
  914  			if (direction == "horizontal")
  915  			{
  916  				mCenterSelection = CenterSelection::PARTIAL;
  917  				mScrollDirection = SCROLL_HORIZONTALLY;
  918  			}
  919  			else if (direction == "horizontalCenter")
  920  			{
  921  				mCenterSelection = CenterSelection::FULL;
  922  				mScrollDirection = SCROLL_HORIZONTALLY;
  923  			}
  924  			else if (direction == "verticalCenter")
  925  			{
  926  				mCenterSelection = CenterSelection::FULL;
  927  				mScrollDirection = SCROLL_VERTICALLY;
  928  			}
  929  			else
  930  			{
  931  				mCenterSelection = CenterSelection::NEVER;
  932  				mScrollDirection = SCROLL_VERTICALLY;
  933  			}
  934  		}
  935  
  936  		if (elem->has("showVideoAtDelay"))
  937  		{
  938  			mVideoDelay = elem->get<float>("showVideoAtDelay");
  939  			mAllowVideo = (mVideoDelay >= 0);
  940  		}
  941  		else
  942  			mAllowVideo = false;
  943  
  944  		if (elem->has("centerSelection"))
  945  		{
  946  			if (!(elem->get<std::string>("centerSelection").compare("true")))
  947  				mCenterSelection = CenterSelection::FULL;
  948  			else if (!(elem->get<std::string>("centerSelection").compare("partial")))
  949  				mCenterSelection = CenterSelection::PARTIAL;
  950  			else
  951  				mCenterSelection = CenterSelection::NEVER;
  952  		}
  953  
  954  		if (mCenterSelection != CenterSelection::NEVER && elem->has("scrollLoop"))
  955  			mScrollLoop = (elem->get<bool>("scrollLoop"));
  956  		else
  957  			mScrollLoop = false;
  958  
  959  		if (elem->has("gameImage"))
  960  		{
  961  			std::string path = elem->get<std::string>("gameImage");
  962  
  963  			if (!ResourceManager::getInstance()->fileExists(path))
  964  				LOG(LogWarning) << "Could not replace default game image, check path: " << path;
  965  			else
  966  			{
  967  				std::string oldDefaultGameTexture = mDefaultGameTexture;
  968  				mDefaultGameTexture = path;
  969  
  970  				// mEntries are already loaded at this point,
  971  				// so we need to update them with new game image texture
  972  				for (auto it = mEntries.begin(); it != mEntries.end(); it++)
  973  				{
  974  					if ((*it).data.texturePath == oldDefaultGameTexture)
  975  						(*it).data.texturePath = mDefaultGameTexture;
  976  				}
  977  			}
  978  		}
  979  
  980  		if (elem->has("folderImage"))
  981  		{
  982  			std::string path = elem->get<std::string>("folderImage");
  983  
  984  			if (!ResourceManager::getInstance()->fileExists(path))
  985  				LOG(LogWarning) << "Could not replace default folder image, check path: " << path;
  986  			else
  987  			{
  988  				std::string oldDefaultFolderTexture = mDefaultFolderTexture;
  989  				mDefaultFolderTexture = path;
  990  
  991  				// mEntries are already loaded at this point,
  992  				// so we need to update them with new folder image texture
  993  				for (auto it = mEntries.begin(); it != mEntries.end(); it++)
  994  				{
  995  					if ((*it).data.texturePath == oldDefaultFolderTexture)
  996  						(*it).data.texturePath = mDefaultFolderTexture;
  997  				}
  998  			}
  999  		}
 1000  
 1001  		if (elem->has("logoBackgroundImage"))
 1002  		{
 1003  			std::string path = elem->get<std::string>("logoBackgroundImage");
 1004  
 1005  			if (!ResourceManager::getInstance()->fileExists(path))
 1006  				LOG(LogWarning) << "Could not replace default folder image, check path: " << path;
 1007  			else
 1008  			{
 1009  				std::string oldDefaultFolderTexture = mDefaultLogoBackgroundTexture;
 1010  				mDefaultLogoBackgroundTexture = path;
 1011  
 1012  				// mEntries are already loaded at this point,
 1013  				// so we need to update them with new folder image texture
 1014  				for (auto it = mEntries.begin(); it != mEntries.end(); it++)
 1015  					if ((*it).data.texturePath == oldDefaultFolderTexture)
 1016  						(*it).data.texturePath = mDefaultLogoBackgroundTexture;
 1017  			}
 1018  		}
 1019  
 1020  		if (elem->has("scrollSound"))
 1021  			mScrollSound = elem->get<std::string>("scrollSound");
 1022  	}
 1023  
 1024  
 1025  	// We still need to manually get the grid tile size here,
 1026  	// so we can recalculate the new grid dimension, and THEN (re)build the tiles
 1027  	elem = theme->getElement(view, "default", "gridtile");
 1028  
 1029  	mTileSize = elem && elem->has("size") ?
 1030  		elem->get<Vector2f>("size") * screen :
 1031  		GridTileComponent::getDefaultTileSize();
 1032  
 1033  	// Apply size property, will trigger a call to onSizeChanged() which will build the tiles
 1034  	GuiComponent::applyTheme(theme, view, element, ThemeFlags::SIZE | ThemeFlags::Z_INDEX);
 1035  
 1036  	// Keep the theme pointer to apply it on the tiles later on
 1037  	mTheme = theme;
 1038  
 1039  	// Trigger the call manually if the theme have no "imagegrid" element
 1040  	resetGrid();
 1041  
 1042  	if (mEntries.size())
 1043  	{
 1044  		for (auto& entry : mEntries)
 1045  		{
 1046  			if (entry.data.tile != nullptr && entry.data.tile->isVisible())
 1047  				mVisibleTiles.push_back(entry.data.tile);
 1048  		}
 1049  	}
 1050  }
 1051  
 1052  template<typename T>
 1053  void ImageGridComponent<T>::onSizeChanged()
 1054  {
 1055  	IList<ImageGridData, T>::onSizeChanged();
 1056  
 1057  	if (mTheme == nullptr || mSize.x() <= 0 || mSize.y() <= 0)
 1058  		return;
 1059  
 1060  	calcGridDimension();
 1061  	mEntriesDirty = true;
 1062  }
 1063  
 1064  template<typename T>
 1065  void ImageGridComponent<T>::onCursorChanged(const CursorState& state)
 1066  {
 1067  	if (mEntries.size() == 0)
 1068  		return;
 1069  
 1070  	if (mCursor == mLastCursor && state == mLastCursorState)
 1071  		return;
 1072  
 1073  	mLastCursorState = state;
 1074  
 1075  	if (mLastCursor == mCursor)
 1076  	{
 1077  		if (state == CURSOR_STOPPED && mCursorChangedCallback)
 1078  			mCursorChangedCallback(state);
 1079  
 1080  		return;
 1081  	}
 1082  
 1083  	mScrollbar.onCursorChanged();
 1084  
 1085  	bool direction = mCursor >= mLastCursor;
 1086  	bool isScrollLooping = false;
 1087  
 1088  	if (mScrollLoop)
 1089  	{
 1090  		int diff = direction ? mCursor - mLastCursor : mLastCursor - mCursor;
 1091  		if (mScrollLoop && diff == mEntries.size() - 1)
 1092  		{
 1093  			direction = !direction;
 1094  			isScrollLooping = true;
 1095  		}
 1096  	}
 1097  
 1098  	int oldStart = mStartPosition;
 1099  
 1100  	float dimScrollable = isVertical() ? mGridDimension.y() - 2 * EXTRAITEMS : mGridDimension.x() - 2 * EXTRAITEMS;
 1101  	float dimOpposite = Math::max(1, isVertical() ? mGridDimension.x() : mGridDimension.y());
 1102  	
 1103  	int centralCol = (int)(dimScrollable - 0.5) / 2;
 1104  	int maxCentralCol = (int)(dimScrollable) / 2;
 1105  
 1106  	int oldCol = (mLastCursor / dimOpposite);
 1107  	int col = (mCursor / dimOpposite);
 1108  
 1109  	int lastCol = ((mEntries.size() - 1) / dimOpposite);
 1110  
 1111  	int lastScroll = std::max(0, (int)(lastCol + 1 - dimScrollable));
 1112  
 1113  	float startPos = 0;
 1114  	float endPos = 1;
 1115  
 1116  	Vector3f oldPos = Vector3f::Zero();
 1117  
 1118  	if (mLastCursor >= 0 && mLastCursor < mEntries.size() && mEntries[mLastCursor].data.tile != nullptr)
 1119  	{
 1120  		if (ALLOWANIMATIONS && mAnimateSelection)
 1121  			oldPos = mEntries[mLastCursor].data.tile->getBackgroundPosition();
 1122  	}
 1123  
 1124  	if (mCursor >= 0 && mCursor < mEntries.size() && mEntries[mCursor].data.tile != nullptr)
 1125  	{
 1126  		if (!mEntries[mCursor].data.tile->isSelected())
 1127  		{
 1128  			auto selectedTile = getSelectedTile();
 1129  			while (selectedTile != nullptr)
 1130  			{
 1131  				selectedTile->setSelected(false, true, nullptr, true);
 1132  				selectedTile = getSelectedTile();
 1133  			}
 1134  
 1135  			if (!mAnimateSelection)
 1136  			{
 1137  				oldPos = Vector3f(0, 0);
 1138  				mEntries[mCursor].data.tile->setSelected(true, true, &oldPos, true);
 1139  			}
 1140  			else
 1141  				mEntries[mCursor].data.tile->setSelected(true, true, oldPos == Vector3f::Zero() ? nullptr : &oldPos, true);
 1142  
 1143  			auto selected = mEntries[mCursor].data.tile;
 1144  			auto old = mLastCursor >= 0 && mLastCursor < mEntries.size() ? mEntries[mLastCursor].data.tile : nullptr;
 1145  
 1146  			for (auto tile : mVisibleTiles)
 1147  				if (tile != selected && tile != old)
 1148  					if (tile->hasItemTemplate())
 1149  						tile->setSelected(false);
 1150  		}
 1151  		else if (mLastCursor = -9999)
 1152  			mEntries[mCursor].data.tile->startVideo();
 1153  	}
 1154  
 1155  	int firstVisibleCol = mStartPosition / dimOpposite;
 1156  
 1157  	auto oldStartPosition = mStartPosition;
 1158  
 1159  	if (mCenterSelection == CenterSelection::NEVER)
 1160  	{
 1161  		if (col == 0)
 1162  			mStartPosition = 0;
 1163  		if (col < firstVisibleCol)
 1164  			mStartPosition = col * dimOpposite;
 1165  		else if (col >= firstVisibleCol + dimScrollable)
 1166  			mStartPosition = (col - dimScrollable + 1) * dimOpposite;
 1167  	}
 1168  	else
 1169  	{
 1170  		if ((col < centralCol || (col == 0 && col == centralCol)) && mCenterSelection == CenterSelection::PARTIAL)
 1171  			mStartPosition = 0;
 1172  		else if ((col - centralCol) > lastScroll && mCenterSelection == CenterSelection::PARTIAL && !mScrollLoop)
 1173  			mStartPosition = lastScroll * dimOpposite;
 1174  		else if (maxCentralCol != centralCol && col == firstVisibleCol + maxCentralCol || col == firstVisibleCol + centralCol)
 1175  		{
 1176  			if (col == firstVisibleCol + maxCentralCol)
 1177  				mStartPosition = (col - maxCentralCol) * dimOpposite;
 1178  			else
 1179  				mStartPosition = (col - centralCol) * dimOpposite;
 1180  		}
 1181  		else
 1182  		{
 1183  			if (oldCol == firstVisibleCol + maxCentralCol)
 1184  				mStartPosition = (col - maxCentralCol) * dimOpposite;
 1185  			else
 1186  				mStartPosition = (col - centralCol) * dimOpposite;
 1187  		}
 1188  	}
 1189  
 1190  	float newCameraOffset = mCameraOffset;
 1191  
 1192  	if (mStartPosition != oldStartPosition)
 1193  	{
 1194  		auto tileDistance = mTileSize + mMargin;
 1195  		newCameraOffset = (isVertical() ? tileDistance.y() : tileDistance.x()) * (mStartPosition / dimOpposite);
 1196  	}
 1197  
 1198  	auto lastCursor = mLastCursor;
 1199  
 1200  	if (lastCursor != -9999 && (lastCursor < 0 || !ALLOWANIMATIONS))
 1201  	{
 1202  		mCameraOffset = newCameraOffset;
 1203  		mEntriesDirty = true;
 1204  
 1205  		if (mCursorChangedCallback)
 1206  			mCursorChangedCallback(state);
 1207  
 1208  		mLastCursor = mCursor;
 1209  
 1210  		return;
 1211  	}
 1212  
 1213  	if (lastCursor != -9999)
 1214  	{
 1215  		if (mCursorChangedCallback)
 1216  			mCursorChangedCallback(state);
 1217  	}
 1218  
 1219  	if (isScrollLooping)
 1220  	{
 1221  		Vector2f tileDistance = mTileSize + mMargin;
 1222  		int totalCols = ((Math::max(0, mEntries.size() - 1)) / dimOpposite);
 1223  		float totalSize = (isVertical() ? tileDistance.y() : tileDistance.x()) * (totalCols + 1);
 1224  
 1225  		if (direction)
 1226  			mCameraOffset -= totalSize;
 1227  		else
 1228  			mCameraOffset += totalSize;
 1229  
 1230  		mEntriesDirty = true;
 1231  	}
 1232  
 1233  	mLastCursor = mCursor;
 1234  
 1235  	if (newCameraOffset != mCameraOffset)
 1236  	{
 1237  		if (ALLOWANIMATIONS)
 1238  		{
 1239  			float oldCameraoffset = mCameraOffset;
 1240  
 1241  			auto func = [this, newCameraOffset, oldCameraoffset](float t)
 1242  			{
 1243  				t -= 1; // cubic ease out
 1244  				float pct = Math::lerp(0, 1, t*t*t + 1);
 1245  
 1246  				mCameraOffset = newCameraOffset * pct + oldCameraoffset * (1.0 - pct);
 1247  				mEntriesDirty = true;
 1248  			};
 1249  
 1250  			((GuiComponent*)this)->setAnimation(new LambdaAnimation(func, 250), 0, [this, newCameraOffset] {
 1251  				mCameraOffset = newCameraOffset;
 1252  				mEntriesDirty = true;
 1253  			}, false, 2);
 1254  		}
 1255  		else
 1256  		{
 1257  			mCameraOffset = newCameraOffset;
 1258  			mEntriesDirty = true;
 1259  		}
 1260  	}
 1261  }
 1262  
 1263  template<typename T>
 1264  void ImageGridComponent<T>::loadTile(std::shared_ptr<GridTileComponent> tile, typename IList<ImageGridData, T>::Entry& entry)
 1265  {
 1266  	std::string name = entry.name;
 1267  
 1268  	IBindable* bindable = getBindable(entry);
 1269  	
 1270  	// tile->setFavorite(entry.data.favorite); //	tile->setCheevos(entry.data.cheevos);
 1271  	bool favorite = bindable ? bindable->getProperty("favorite").toBoolean() : false;
 1272  
 1273  	// Label
 1274  	if (!favorite || tile->hasFavoriteMedia())
 1275  	{
 1276  		// Remove favorite text glyph
 1277  		if (Utils::String::startsWith(name, _U("\uF006 ")))
 1278  			tile->setLabel(name.substr(4));
 1279  		else
 1280  			tile->setLabel(name);
 1281  	}
 1282  	else
 1283  		tile->setLabel(name);
 1284  
 1285  	if (bindable != nullptr)
 1286  		tile->updateBindings(bindable);
 1287  	
 1288  	if (tile->hasItemTemplate())
 1289  		return;
 1290  
 1291  	std::string imagePath = entry.data.texturePath;
 1292  	std::string marqueePath = bindable ? bindable->getProperty("marquee").toString() : ""; // entry.data.marqueePath;
 1293  	std::string videoPath = bindable ? bindable->getProperty("video").toString() : ""; // entry.data.marqueePath;
 1294  	
 1295  	if (Utils::FileSystem::isAudio(imagePath) && videoPath.empty())
 1296  	{
 1297  		videoPath = imagePath;
 1298  
 1299  		if (ResourceManager::getInstance()->fileExists(":/mp3.jpg"))
 1300  			imagePath = ":/mp3.jpg";
 1301  	}
 1302  	else if (Utils::FileSystem::isVideo(imagePath) && videoPath.empty())
 1303  	{
 1304  		videoPath = imagePath;
 1305  		imagePath = "";
 1306  	}
 1307  
 1308  	bool cheevos = bindable ? bindable->getProperty("cheevos").toBoolean() : false;
 1309  	bool folder = bindable ? bindable->getProperty("folder").toBoolean() : false;
 1310  	bool virtualFolder = bindable ? bindable->getProperty("virtualfolder").toBoolean() : false; 
 1311  
 1312  	bool preloadMedias = Settings::PreloadMedias();
 1313  
 1314  	bool setMarquee = true;
 1315  
 1316  	// Image
 1317  	if ((preloadMedias && !imagePath.empty()) || (!preloadMedias && ResourceManager::getInstance()->fileExists(imagePath)))
 1318  	{
 1319  		if (virtualFolder)
 1320  		{
 1321  			tile->setLabel("");
 1322  
 1323  			if (!mDefaultLogoBackgroundTexture.empty() && tile->isMinSizeTile())
 1324  			{
 1325  				tile->setImage(mDefaultLogoBackgroundTexture);
 1326  				tile->forceMarquee(imagePath);
 1327  				setMarquee = false;
 1328  			}
 1329  			else
 1330  				tile->setImage(imagePath, true);
 1331  		}
 1332  		else
 1333  			tile->setImage(imagePath, false);
 1334  
 1335  		if (mImageSource == MARQUEEORTEXT)
 1336  			tile->setLabel("");
 1337  	}
 1338  	else if (mImageSource == MARQUEEORTEXT)
 1339  		tile->setImage("");
 1340  	else if (folder)
 1341  		tile->setImage(mDefaultFolderTexture, mDefaultFolderTexture == ":/folder.svg");
 1342  	else
 1343  	{
 1344  		if (!mDefaultLogoBackgroundTexture.empty() && tile->hasMarquee() && !marqueePath.empty() && ResourceManager::getInstance()->fileExists(marqueePath))
 1345  			tile->setImage(mDefaultLogoBackgroundTexture);
 1346  		else
 1347  			tile->setImage(mDefaultGameTexture, mDefaultGameTexture == ":/cartridge.svg");
 1348  	}
 1349  
 1350  	if (setMarquee)
 1351  	{
 1352  		if (!mDefaultLogoBackgroundTexture.empty() && tile->isMinSizeTile())
 1353  			tile->forceMarquee("");
 1354  
 1355  		// Marquee		
 1356  		if (tile->hasMarquee())
 1357  		{
 1358  			if ((preloadMedias && !marqueePath.empty()) || (!preloadMedias && ResourceManager::getInstance()->fileExists(marqueePath)))
 1359  				tile->setMarquee(marqueePath);
 1360  			else
 1361  				tile->setMarquee("");
 1362  		}
 1363  	}
 1364  
 1365  	tile->setFavorite(favorite);
 1366  	tile->setCheevos(cheevos);
 1367  
 1368  	// Video
 1369  	if (mAllowVideo)
 1370  	{
 1371  		if ((preloadMedias && !videoPath.empty()) || (!preloadMedias && ResourceManager::getInstance()->fileExists(videoPath)))
 1372  			tile->setVideo(videoPath, mVideoDelay);
 1373  		else
 1374  			tile->setVideo("");
 1375  	}
 1376  	else
 1377  		tile->setVideo("");
 1378  }
 1379  
 1380  template<typename T>
 1381  void ImageGridComponent<T>::resetGrid()
 1382  {
 1383  	mVisibleTiles.clear();
 1384  
 1385  	if (mGridSizeOverride.x() != 0 && mGridSizeOverride.y() != 0)
 1386  		mAutoLayout = mGridSizeOverride;
 1387  
 1388  	calcGridDimension();
 1389  
 1390  	float dimOpposite = Math::max(1, isVertical() ? mGridDimension.x() : mGridDimension.y());
 1391  
 1392  	mStartPosition = 0;
 1393  	if (mCenterSelection != CenterSelection::NEVER)
 1394  	{
 1395  		int dimScrollable = (isVertical() ? mGridDimension.y() : mGridDimension.x()) - 2 * EXTRAITEMS;
 1396  		mStartPosition -= (int)Math::floorf(dimScrollable / 2.0f);
 1397  		
 1398  		int centralCol = (int)(dimScrollable - 0.5) / 2;
 1399  		int maxCentralCol = (int)(dimScrollable) / 2;
 1400  		int firstVisibleCol = 0 / dimOpposite; // mStartPosition
 1401  
 1402  		int lastCol = ((mEntries.size() - 1) / dimOpposite);
 1403  		int lastScroll = std::max(0, (int)(lastCol + 1 - dimScrollable));
 1404  
 1405  		int oldCol = 0;
 1406  		int col = 0;
 1407  
 1408  		if ((col < centralCol || (col == 0 && col == centralCol)) && mCenterSelection == CenterSelection::PARTIAL)
 1409  			mStartPosition = 0;
 1410  		else if ((col - centralCol) > lastScroll && mCenterSelection == CenterSelection::PARTIAL && !mScrollLoop)
 1411  			mStartPosition = lastScroll * dimOpposite;
 1412  		else if (maxCentralCol != centralCol && col == firstVisibleCol + maxCentralCol || col == firstVisibleCol + centralCol)
 1413  		{
 1414  			if (col == firstVisibleCol + maxCentralCol)
 1415  				mStartPosition = (col - maxCentralCol) * dimOpposite;
 1416  			else
 1417  				mStartPosition = (col - centralCol) * dimOpposite;
 1418  		}
 1419  		else
 1420  		{
 1421  			if (oldCol == firstVisibleCol + maxCentralCol)
 1422  				mStartPosition = (col - maxCentralCol) * dimOpposite;
 1423  			else
 1424  				mStartPosition = (col - centralCol) * dimOpposite;
 1425  		}
 1426  	}
 1427  	
 1428  	auto tileDistance = mTileSize + mMargin;
 1429  	mCameraOffset = (isVertical() ? tileDistance.y() : tileDistance.x()) * (mStartPosition / dimOpposite);
 1430  	mEntriesDirty = true;
 1431  
 1432  	mLastCursor = -1;
 1433  	mLastCursorState = CursorState::CURSOR_STOPPED;
 1434  	onCursorChanged(CURSOR_STOPPED);
 1435  }
 1436  
 1437  // Calculate how much tiles of size mTileSize we can fit in a grid of size mSize using a margin of size mMargin
 1438  template<typename T>
 1439  void ImageGridComponent<T>::calcGridDimension()
 1440  {
 1441  	Vector2f gridDimension = (mSize + mMargin) / (mTileSize + mMargin);
 1442  	if (mAutoLayout.x() != 0 && mAutoLayout.y() != 0)
 1443  		gridDimension = mAutoLayout;
 1444  
 1445  	mLastRowPartial = Math::floorf(gridDimension.y()) != gridDimension.y();
 1446  	mGridDimension = Vector2i((int)gridDimension.x(), Math::ceilf(gridDimension.y()));
 1447  
 1448  	// Grid dimension validation
 1449  	if (mGridDimension.x() < 1)
 1450  		LOG(LogError) << "Theme defined grid X dimension below 1";
 1451  	if (mGridDimension.y() < 1)
 1452  		LOG(LogError) << "Theme defined grid Y dimension below 1";
 1453  
 1454  	// Add extra tiles to both sides : Add EXTRAITEMS before, EXTRAITEMS after
 1455  	if (isVertical())
 1456  		mGridDimension.y() += 2 * EXTRAITEMS;
 1457  	else
 1458  		mGridDimension.x() += 2 * EXTRAITEMS;
 1459  
 1460  	// Auto layout
 1461  	if (mAutoLayout.x() != 0 && mAutoLayout.y() != 0)
 1462  	{
 1463  		auto x = (mSize.x() - (mMargin.x() * (mAutoLayout.x() - 1)) - mPadding.x() - mPadding.z()) / (int)mAutoLayout.x();
 1464  		auto y = (mSize.y() - (mMargin.y() * (mAutoLayout.y() - 1)) - mPadding.y() - mPadding.w()) / (int)mAutoLayout.y();
 1465  
 1466  		mTileSize = Vector2f(x, y);
 1467  	}
 1468  };
 1469  
 1470  template<typename T>
 1471  bool ImageGridComponent<T>::hitTest(int x, int y, Transform4x4f& parentTransform, std::vector<GuiComponent*>* pResult)
 1472  {
 1473  	auto ret = GuiComponent::hitTest(x, y, parentTransform, pResult);
 1474  
 1475  	Transform4x4f trans = parentTransform * getTransform();
 1476  	
 1477  	trans.translate(isVertical() ? 0 : -mCameraOffset, isVertical() ? -mCameraOffset : 0);
 1478  	
 1479  	for (auto tile : mVisibleTiles)
 1480  		tile->hitTest(x, y, trans, pResult);
 1481  
 1482  	return ret;
 1483  }
 1484  
 1485  template<typename T>
 1486  bool ImageGridComponent<T>::onMouseWheel(int delta)
 1487  {
 1488  	float dimOpposite = Math::max(1, isVertical() ? mGridDimension.x() : mGridDimension.y());
 1489  
 1490  	auto newCursor = mCursor - delta * dimOpposite;
 1491  	/*
 1492  	if (newCursor < 0)
 1493  		newCursor += mEntries.size();
 1494  	else if (newCursor >= mEntries.size())
 1495  		newCursor -= mEntries.size();
 1496  	*/
 1497  	if (mScrollLoop)
 1498  	{
 1499  		if (newCursor < 0)
 1500  			newCursor += mEntries.size();
 1501  		else if (newCursor >= mEntries.size())
 1502  			newCursor -= mEntries.size();
 1503  	}
 1504  	else
 1505  	{
 1506  		if (newCursor < 0)
 1507  			newCursor = 0;
 1508  		else if (newCursor >= mEntries.size())
 1509  			newCursor = mEntries.size() - 1;
 1510  	}
 1511  	
 1512  	if (newCursor != mCursor && newCursor >= 0 && newCursor < mEntries.size())
 1513  	{
 1514  		mCursor = newCursor;
 1515  		onCursorChanged(CURSOR_STOPPED);
 1516  	}
 1517  
 1518  	return true;
 1519  }
 1520  
 1521  
 1522  template<typename T>
 1523  bool ImageGridComponent<T>::onMouseClick(int button, bool pressed, int x, int y)
 1524  {
 1525  	if (button == 1)
 1526  	{
 1527  		mTimeHoldingButton = -1;
 1528  
 1529  		if (pressed)
 1530  		{
 1531  			mPressedCursor = -1;
 1532  
 1533  			std::shared_ptr<GridTileComponent> hotTile;
 1534  
 1535  			int tileIndex = 0;
 1536  
 1537  			for (auto entry : mEntries)
 1538  			{
 1539  				if (entry.data.tile != nullptr && entry.data.tile->isVisible() && entry.data.tile->isMouseOver())
 1540  				{
 1541  					hotTile = entry.data.tile;
 1542  					break;
 1543  				}
 1544  
 1545  				tileIndex++;
 1546  			}
 1547  
 1548  			if (hotTile)
 1549  			{
 1550  				auto cursor = tileIndex;
 1551  				if (cursor != mCursor && mCenterSelection == CenterSelection::NEVER)
 1552  				{
 1553  					mCursor = cursor;
 1554  
 1555  					if (mCursor >= 0 && mCursor < mEntries.size() && mEntries[mCursor].data.tile != nullptr)
 1556  					{
 1557  						auto selectedTile = getSelectedTile();
 1558  						while (selectedTile != nullptr)
 1559  						{
 1560  							selectedTile->setSelected(false, true, nullptr, true);
 1561  							selectedTile = getSelectedTile();
 1562  						}
 1563  
 1564  						Vector3f oldPos = Vector3f::Zero();
 1565  						mEntries[mCursor].data.tile->setSelected(true, true, mAnimateSelection ? nullptr : &oldPos, true);
 1566  					}
 1567  
 1568  					if (mCursorChangedCallback)
 1569  						mCursorChangedCallback(CURSOR_STOPPED);
 1570  
 1571  					mLastCursor = mCursor;
 1572  				}
 1573  				else
 1574  					mPressedCursor = mCursor;
 1575  
 1576  				mTimeHoldingButton = 0;
 1577  			}
 1578  
 1579  			mIsDragging = false;
 1580  			mPressedPoint = Vector2i(x, y);
 1581  			mWindow->setMouseCapture(this);
 1582  		}
 1583  		else if (mWindow->hasMouseCapture(this))
 1584  		{
 1585  			mWindow->releaseMouseCapture();
 1586  
 1587  			auto btnDownCursor = mPressedCursor;
 1588  			mPressedCursor = -1;
 1589  			mPressedPoint = Vector2i(-1, -1);
 1590  
 1591  			if (mCenterSelection != CenterSelection::NEVER)
 1592  			{
 1593  				float dimScrollable = isVertical() ? mGridDimension.y() - 2 * EXTRAITEMS : mGridDimension.x() - 2 * EXTRAITEMS;
 1594  				float dimOpposite = Math::max(1, isVertical() ? mGridDimension.x() : mGridDimension.y());
 1595  
 1596  				float tileDist = isVertical() ? (mTileSize + mMargin).y() : (mTileSize + mMargin).x();
 1597  				int newCursor = ((mCameraOffset + tileDist * dimScrollable / 2.0f)  * dimOpposite) / tileDist;
 1598  
 1599  				if (mCursor != newCursor && newCursor >= 0 && newCursor < mEntries.size())
 1600  				{
 1601  					mCursor = newCursor;
 1602  					onCursorChanged(CURSOR_STOPPED);
 1603  				}
 1604  				else
 1605  				{
 1606  					mLastCursor = -9999;
 1607  					mStartPosition = -9999;
 1608  					onCursorChanged(CURSOR_STOPPED);
 1609  				}
 1610  			}
 1611  
 1612  			auto dragging = mIsDragging;
 1613  			mIsDragging = false;
 1614  
 1615  			if (!dragging && btnDownCursor == mCursor)
 1616  				InputManager::getInstance()->sendMouseClick(mWindow, 1);
 1617  		}
 1618  
 1619  		return true;
 1620  	}
 1621  
 1622  	return false;
 1623  }
 1624  
 1625  template<typename T>
 1626  void ImageGridComponent<T>::onMouseMove(int x, int y)
 1627  {
 1628  	if (mPressedPoint.x() != -1 && mPressedPoint.y() != -1 && mWindow->hasMouseCapture(this))
 1629  	{
 1630  		mIsDragging = true;
 1631  		mTimeHoldingButton = -1;
 1632  
 1633  		if (isVertical())
 1634  			mCameraOffset += mPressedPoint.y() - y;
 1635  		else
 1636  			mCameraOffset += mPressedPoint.x() - x;
 1637  
 1638  		if (mCenterSelection == CenterSelection::NEVER)
 1639  		{
 1640  			if (mCameraOffset < 0)
 1641  				mCameraOffset = 0;
 1642  
 1643  			if (mCameraOffset > mTotalHeight)
 1644  				mCameraOffset = mTotalHeight;
 1645  		}
 1646  		else
 1647  		{
 1648  
 1649  			float dimScrollable = isVertical() ? mGridDimension.y() - 2 * EXTRAITEMS : mGridDimension.x() - 2 * EXTRAITEMS;
 1650  			float dimOpposite = Math::max(1, isVertical() ? mGridDimension.x() : mGridDimension.y());
 1651  			float tileDist = isVertical() ? (mTileSize + mMargin).y() : (mTileSize + mMargin).x();
 1652  
 1653  			float min = tileDist * (float)(int)(dimScrollable / 2);
 1654  
 1655  			int totalToScroll = mTotalHeight + tileDist;
 1656  
 1657  			if (mScrollLoop)
 1658  			{
 1659  				if (mCameraOffset < -min)
 1660  					mCameraOffset += totalToScroll + tileDist;
 1661  
 1662  				if (mCameraOffset > totalToScroll - min)
 1663  					mCameraOffset -= totalToScroll + tileDist;
 1664  			}
 1665  			else
 1666  			{
 1667  				if (mCameraOffset < -min)
 1668  					mCameraOffset = -min;
 1669  
 1670  				if (mCameraOffset > mTotalHeight)
 1671  					mCameraOffset = mTotalHeight;
 1672  			}
 1673  
 1674  			int newCursor = ((mCameraOffset + tileDist * dimScrollable / 2.0f)  * dimOpposite) / tileDist;
 1675  
 1676  			if (mCursor != newCursor && newCursor >= 0 && newCursor < mEntries.size())
 1677  			{
 1678  				mCursor = newCursor;
 1679  				if (mCursor >= 0 && mCursor < mEntries.size() && mEntries[mCursor].data.tile != nullptr)
 1680  				{
 1681  					auto selectedTile = getSelectedTile();
 1682  					while (selectedTile != nullptr)
 1683  					{
 1684  						selectedTile->setSelected(false, true, nullptr, true);
 1685  						selectedTile = getSelectedTile();
 1686  					}
 1687  
 1688  					Vector3f oldPos = Vector3f::Zero();
 1689  					mEntries[mCursor].data.tile->setSelected(true, true, mAnimateSelection ? nullptr : &oldPos, true, false);
 1690  				}
 1691  
 1692  				if (mCursorChangedCallback)
 1693  					mCursorChangedCallback(CURSOR_STOPPED);
 1694  
 1695  				mLastCursor = mCursor;
 1696  			}
 1697  		}
 1698  
 1699  
 1700  		mEntriesDirty = true;
 1701  		mPressedPoint = Vector2i(x, y);
 1702  	}
 1703  }
 1704  
 1705  #endif // ES_CORE_COMPONENTS_IMAGE_GRID_COMPONENT_H
```

## MenuComponent.cpp (whole, fork-modified, at the pin)

```text
    1  #include "components/MenuComponent.h"
    2  #include "components/ButtonComponent.h"
    3  #include "components/MultiLineMenuEntry.h"
    4  #include "TextToSpeech.h"
    5  
    6  #define BUTTON_GRID_VERT_PADDING  (Renderer::getScreenHeight()*0.0296296)
    7  // The gap between two buttons on a menu's button bar, and the one place it is
    8  // defined -- every ES screen ends in this bar, so a value set here is the
    9  // house style rather than a per-page decision.
   10  //
   11  // It was 0.0052 of the screen width, which is 3px on a 640px handheld panel:
   12  // two buttons that read as one control, and a destructive choice one thumb's
   13  // width from a safe one. 0.022 gives 14px there and scales with the panel.
   14  #define BUTTON_GRID_HORIZ_PADDING (Renderer::getScreenWidth()*0.022)
   15  
   16  #define TITLE_HEIGHT (mTitle->getFont()->getLetterHeight() + (mSubtitle ? TITLE_WITHSUB_VERT_PADDING : TITLE_VERT_PADDING) + (mSubtitle ? mSubtitle->getSize().y() + SUBTITLE_VERT_PADDING : 0))
   17  
   18  MenuComponent::MenuComponent(Window* window, 
   19  	const std::string& title, const std::shared_ptr<Font>& titleFont,
   20  	const std::string& subTitle, bool tabbedUI) 
   21  	: GuiComponent(window),
   22  	mBackground(window), mGrid(window, Vector2i(1, 4)), mTabIndex(0)
   23  {
   24  	if (tabbedUI)
   25  	{
   26  		// Tabs
   27  		mTabs = std::make_shared<ComponentTab>(mWindow);
   28  		mTabs->setCursorChangedCallback([&](const CursorState& /*state*/)
   29  			{
   30  				int idx = mTabs->getCursorIndex();
   31  				if (mTabIndex != idx)
   32  				{
   33  					mTabIndex = idx;
   34  					OnTabChanged(idx);					
   35  				}
   36  			});
   37  	}
   38  
   39  	mMaxHeight = 0;
   40  
   41  	auto theme = ThemeData::getMenuTheme();
   42  
   43  	addChild(&mBackground);
   44  	addChild(&mGrid);
   45  
   46  	mGrid.setZIndex(10);
   47  
   48  	mBackground.setImagePath(theme->Background.path, false);
   49  	mBackground.setEdgeColor(theme->Background.color);
   50  	mBackground.setCenterColor(theme->Background.centerColor);
   51  	mBackground.setCornerSize(theme->Background.cornerSize);
   52  	mBackground.setPostProcessShader(theme->Background.menuShader);
   53  	mBackground.setZIndex(2);
   54  
   55  	// set up title
   56  	mTitle = std::make_shared<TextComponent>(mWindow);
   57  	mTitle->setHorizontalAlignment(ALIGN_CENTER);
   58  	mTitle->setColor(theme->Title.color); // 0x555555FF
   59  
   60  	if (theme->Title.selectorColor != 0x555555FF)
   61  	{
   62  		mTitle->setBackgroundColor(theme->Title.selectorColor);
   63  		mTitle->setRenderBackground(true);
   64  	}
   65  
   66  	mHeaderGrid = std::make_shared<ComponentGrid>(mWindow, Vector2i(2, 2));
   67  	mHeaderGrid->setColWidthPerc(0, 1);
   68  	mHeaderGrid->setColWidthPerc(1, 0);
   69  
   70  	mHeaderGrid->setEntry(mTitle, Vector2i(0, 0), false, true);
   71  
   72  	setTitle(title, theme->Title.font); //  titleFont
   73  	setSubTitle(subTitle);
   74  
   75  	mGrid.setEntry(mHeaderGrid, Vector2i(0, 0), false, true, Vector2i(1, 1), mTabs == nullptr ? GridFlags::BORDER_BOTTOM : GridFlags::BORDER_NONE);
   76  	//mGrid.setEntry(mTitle, Vector2i(0, 0), false);
   77  
   78  	// Wrap-around between the focus stops: tab strip (if any), rows, buttons.
   79  	// The grid gets here only when the focused stop could not move that way.
   80  	mGrid.setUnhandledInputCallback([this](InputConfig* config, Input input) -> bool {
   81  		if (config->isMappedLike("down", input)) {
   82  			// past the bottom: back to the top stop
   83  			if (mTabs != nullptr && mTabs->size())
   84  				mGrid.setCursorTo(mTabs);
   85  			else {
   86  				mGrid.setCursorTo(mList);
   87  				mList->setCursorIndex(0);
   88  			}
   89  			return true;
   90  		}
   91  		if (config->isMappedLike("up", input)) {
   92  			// past the top: down to the bottom stop, with the last row ready
   93  			// for the next press up from the buttons
   94  			mList->setCursorIndex(mList->size() - 1);
   95  			if (mButtonGrid)
   96  				mGrid.setCursorTo(mButtonGrid);
   97  			else
   98  				mGrid.setCursorTo(mList);
   99  			return true;
  100  		}
  101  		return false;
  102  	});
  103  
  104  	// set up list which will never change (externally, anyway)
  105  	mList = std::make_shared<ComponentList>(mWindow);
  106  
  107  	// The strip is a focus stop of its own (#65): up from the first row lands
  108  	// on it, left/right there switch tabs, down returns to the rows. Rows keep
  109  	// left/right for themselves, which is how an option row cycles in place.
  110  	// It becomes a stop only once it has a tab (addTab): every menu is built
  111  	// with the strip (tabbedUI defaults to true), and an empty strip took the
  112  	// cursor with nothing to show for it, so up from the MAIN MENU's first row
  113  	// landed on nothing before BACK (fork #325).
  114  	if (mTabs != nullptr)
  115  		mGrid.setEntry(mTabs, Vector2i(0, 1), false, true, Vector2i(1, 1), GridFlags::BORDER_BOTTOM);
  116  
  117  	mGrid.setEntry(mList, Vector2i(0, 2), true);
  118  
  119  	updateGrid();
  120  	updateSize();
  121  
  122  	// A page opens on its first row, not on the strip.
  123  	mGrid.setCursorTo(mList);
  124  }
  125  
  126  bool MenuComponent::input(InputConfig* config, Input input)
  127  {
  128  	// Left/right go to whichever stop is focused. The strip only sees them
  129  	// while it holds the focus (#65); before, it took every left/right on the
  130  	// page, and no row ever cycled in place.
  131  	return GuiComponent::input(config, input);
  132  }
  133  
  134  void MenuComponent::addTab(const std::string label, const std::string value, bool setCursorHere)
  135  {
  136  	if (mTabs == nullptr)
  137  		return;
  138  	mTabs->addTab(label, value, setCursorHere);
  139  	// The first tab makes the strip a focus stop (fork #325): the cell is
  140  	// re-entered as focusable, in the same place, with the same border.
  141  	if (mTabs->size() == 1)
  142  	{
  143  		mGrid.removeEntry(mTabs);
  144  		mGrid.setEntry(mTabs, Vector2i(0, 1), true, true, Vector2i(1, 1), GridFlags::BORDER_BOTTOM);
  145  	}
  146  }
  147  
  148  void MenuComponent::addMenuIcon(Window* window, ComponentListRow& row, const std::string& iconName)
  149  {
  150  	if (iconName.empty())
  151  		return;
  152  		
  153  	auto theme = ThemeData::getMenuTheme();
  154  
  155  	std::string iconPath = theme->getMenuIcon(iconName);
  156  	if (!iconPath.empty())
  157  	{
  158  		// icon
  159  		auto icon = std::make_shared<ImageComponent>(window, true);
  160  		icon->setImage(iconPath);
  161  		icon->setColorShift(theme->Text.color);
  162  		icon->setResize(0, theme->Text.font->getLetterHeight() * 1.25f);
  163  		row.addElement(icon, false);
  164  
  165  		// spacer between icon and text
  166  		auto spacer = std::make_shared<GuiComponent>(window);
  167  		spacer->setSize(10, 0);
  168  		row.addElement(spacer, false);
  169  
  170  		return;
  171  	}
  172  
  173  	std::string label;
  174  	if (iconName == "audio")
  175  		label = _U("\uf028");
  176  	else if (iconName == "keyboard")
  177  		label = _U("\uf11c");
  178  	else if (iconName == "joystick")
  179  		label = _U("\uf11b");
  180  	else if (iconName == "mouse")
  181  		label = _U("\uf124");
  182  	else if (iconName == "unknown")
  183  		label = _U("\uf1de");
  184  	
  185  	if (!label.empty())
  186  	{
  187  		auto text = std::make_shared<TextComponent>(window, label, theme->Text.font, theme->Text.color, ALIGN_CENTER);
  188  		row.addElement(text, false);
  189  
  190  		// spacer between icon and text
  191  		auto spacer = std::make_shared<GuiComponent>(window);
  192  		spacer->setSize(10, 0);
  193  		row.addElement(spacer, false);
  194  	}
  195  }
  196  
  197  void MenuComponent::addWithLabel(const std::string& label, const std::shared_ptr<GuiComponent>& comp, const std::function<void()>& func, const std::string& iconName, bool setCursorHere)
  198  {
  199  	auto theme = ThemeData::getMenuTheme();
  200  
  201  	ComponentListRow row;
  202  
  203  	addMenuIcon(mWindow, row, iconName);
  204  
  205  	auto text = std::make_shared<TextComponent>(mWindow, Utils::String::toUpper(label), theme->Text.font, theme->Text.color);
  206  	row.addElement(text, true);
  207  
  208  	if (EsLocale::isRTL())
  209  		text->setHorizontalAlignment(Alignment::ALIGN_RIGHT);
  210  
  211  	if (comp != nullptr)
  212  		row.addElement(comp, false);
  213  
  214  	if (func != nullptr)
  215  		row.makeAcceptInputHandler(func);
  216  
  217  	addRow(row, setCursorHere);
  218  }
  219  
  220  void MenuComponent::addWithDescription(const std::string& label, const std::string& description, const std::shared_ptr<GuiComponent>& comp, const std::function<void()>& func, const std::string& iconName, bool setCursorHere, bool multiLine, const std::string& userData, bool doUpdateSize)
  221  {
  222  	auto theme = ThemeData::getMenuTheme();
  223  
  224  	ComponentListRow row;
  225  
  226  	addMenuIcon(mWindow, row, iconName);
  227  
  228  	if (!description.empty())
  229  	{
  230  		if (!multiLine)
  231  			mList->setUpdateType(ComponentListFlags::UpdateType::UPDATE_ALWAYS);			
  232  
  233  		row.addElement(std::make_shared<MultiLineMenuEntry>(mWindow, Utils::String::toUpper(label), description, multiLine), true);
  234  	}
  235  	else
  236  		row.addElement(std::make_shared<TextComponent>(mWindow, Utils::String::toUpper(label), theme->Text.font, theme->Text.color), true);
  237  
  238  	if (comp != nullptr)
  239  		row.addElement(comp, false);
  240  
  241  	if (func != nullptr)
  242  		row.makeAcceptInputHandler(func);
  243  
  244  
  245  	addRow(row, setCursorHere, doUpdateSize, userData);
  246  }
  247  
  248  void MenuComponent::addEntry(const std::string& name, bool add_arrow, const std::function<void()>& func, const std::string& iconName, bool setCursorHere, bool onButtonRelease, const std::string& userData, bool doUpdateSize)
  249  {
  250  	auto theme = ThemeData::getMenuTheme();
  251  	std::shared_ptr<Font> font = theme->Text.font;
  252  	unsigned int color = theme->Text.color;
  253  
  254  	// populate the list
  255  	ComponentListRow row;
  256  
  257  	addMenuIcon(mWindow, row, iconName);
  258  
  259  	auto text = std::make_shared<TextComponent>(mWindow, name, font, color);
  260  	row.addElement(text, true);
  261  
  262  	if (EsLocale::isRTL())
  263  		text->setHorizontalAlignment(Alignment::ALIGN_RIGHT);
  264  
  265  	if (add_arrow)
  266  	{
  267  		auto arrow = makeArrow(mWindow);
  268  
  269  		if (EsLocale::isRTL())
  270  			arrow->setFlipX(true);
  271  
  272  		row.addElement(arrow, false);
  273  	}
  274  
  275  	if (func != nullptr)
  276  		row.makeAcceptInputHandler(func, onButtonRelease);
  277  
  278  	addRow(row, setCursorHere, doUpdateSize, userData);
  279  }
  280  
  281  void MenuComponent::setTitle(const std::string& title, const std::shared_ptr<Font>& font)
  282  {
  283  	mTitle->setText(Utils::String::toUpper(title));
  284  	
  285  	if (font != nullptr)
  286  		mTitle->setFont(font);
  287  }
  288  
  289  void MenuComponent::setTitleImage(std::shared_ptr<ImageComponent> titleImage, bool replaceTitle)
  290  {
  291  	if (titleImage == nullptr)
  292  	{
  293  		if (mTitleImage != nullptr)
  294  		{
  295  			mHeaderGrid->removeEntry(mTitleImage);
  296  			mTitleImage = nullptr;
  297  		}
  298  
  299  		mHeaderGrid->setColWidthPerc(0, 1);
  300  		mHeaderGrid->setColWidthPerc(1, 0);
  301  
  302  		return;
  303  	}
  304  
  305  	mTitleImage = titleImage;	
  306  	mTitleImage->setPadding(TITLE_HEIGHT * 0.15f);
  307  	
  308  	if (replaceTitle)
  309  	{		
  310  		mTitleImage->setMaxSize(mSize.x() * 0.85f, TITLE_HEIGHT);
  311  
  312  		mHeaderGrid->setColWidthPerc(0, 0);
  313  		mHeaderGrid->setColWidthPerc(1, 1);
  314  		mHeaderGrid->setEntry(mTitleImage, Vector2i(0, 0), false, false, Vector2i(2, 2));
  315  		
  316  		if (mTitle)
  317  			mTitle->setVisible(false);
  318  
  319  		if (mSubtitle)
  320  			mSubtitle->setVisible(false);
  321  	}
  322  	else
  323  	{
  324  		float width = (float)Math::min((int)Renderer::getScreenHeight(), (int)(Renderer::getScreenWidth() * 0.90f));
  325  		float iw = TITLE_HEIGHT / width;
  326  
  327  		mTitleImage->setMaxSize(1.3f * iw * mSize.x(), TITLE_HEIGHT);
  328  
  329  		mHeaderGrid->setColWidthPerc(0, 1 - iw);
  330  		mHeaderGrid->setColWidthPerc(1, iw);
  331  		mHeaderGrid->setEntry(mTitleImage, Vector2i(1, 0), false, false, Vector2i(1, 2));
  332  	}
  333  
  334  	updateSize();	
  335  }
  336  
  337  void MenuComponent::setSubTitle(const std::string& text)
  338  {
  339  	if (text.empty())
  340  	{
  341  		if (mSubtitle != nullptr)
  342  		{
  343  			mHeaderGrid->removeEntry(mSubtitle);
  344  			mSubtitle = nullptr;			
  345  		}
  346  
  347  		mHeaderGrid->setRowHeightPerc(0, 1);
  348  		mHeaderGrid->setRowHeightPerc(1, 0);
  349  
  350  		return;
  351  	}
  352  	
  353  	if (mSubtitle == nullptr)
  354  	{
  355  		auto theme = ThemeData::getMenuTheme();
  356  
  357  		mSubtitle = std::make_shared<TextComponent>(mWindow, 
  358  			Utils::String::toUpper(Utils::FileSystem::getFileName(text)),
  359  			theme->TextSmall.font, theme->TextSmall.color, ALIGN_CENTER);
  360  
  361  		mHeaderGrid->setEntry(mSubtitle, Vector2i(0, 1), false, true);
  362  	}
  363  	
  364  	mSubtitle->setText(text);
  365  	mSubtitle->setVerticalAlignment(Alignment::ALIGN_TOP);
  366  	mSubtitle->setSize(Renderer::getScreenWidth() * 0.88f, 0);
  367  	mSubtitle->setLineSpacing(1.1);
  368  	
  369  	const float titleHeight = mTitle->getFont()->getLetterHeight() + (mSubtitle ? TITLE_WITHSUB_VERT_PADDING : TITLE_VERT_PADDING);
  370  	const float subtitleHeight = mSubtitle->getSize().y() + SUBTITLE_VERT_PADDING;
  371  
  372  	mHeaderGrid->setRowHeightPerc(0, titleHeight / TITLE_HEIGHT);	
  373  
  374  	if (mTitleImage != nullptr)
  375  		setTitleImage(mTitleImage);
  376  
  377  	updateSize();
  378  }
  379  
  380  float MenuComponent::getTitleHeight() const
  381  {
  382  	return TITLE_HEIGHT;
  383  }
  384  
  385  float MenuComponent::getHeaderGridHeight() const
  386  {
  387  	return mHeaderGrid->getRowHeight(0);
  388  }
  389  
  390  float MenuComponent::getButtonGridHeight() const
  391  {
  392  	auto menuTheme = ThemeData::getMenuTheme();
  393  	return (mButtonGrid ? mButtonGrid->getSize().y() : menuTheme->Text.font->getHeight() + BUTTON_GRID_VERT_PADDING);	
  394  }
  395  
  396  void MenuComponent::updateSize()
  397  {
  398  	// GPI: a full-screen menu is the screen, there is nothing to fit.
  399  	if (Renderer::ScreenSettings::fullScreenMenus())
  400  		setSize(Renderer::getScreenWidth(), Renderer::getScreenHeight());
  401  	else
  402  	{
  403  		const float maxHeight = mMaxHeight <= 0 ? Renderer::getScreenHeight() * 0.75f : mMaxHeight;
  404  
  405  		float height = TITLE_HEIGHT + mList->getTotalRowHeight() + getButtonGridHeight() + 2;
  406  		if (mTabs != nullptr && mTabs->size())
  407  			height += mTabs->getSize().y();
  408  
  409  		if(height > maxHeight)
  410  		{
  411  			height = TITLE_HEIGHT + getButtonGridHeight();
  412  			int i = 0;
  413  			while(i < mList->size())
  414  			{
  415  				float rowHeight = mList->getRowHeight(i);
  416  				if(height + rowHeight < maxHeight)
  417  					height += rowHeight;
  418  				else
  419  					break;
  420  				i++;
  421  			}
  422  		}
  423  
  424  		float width = (float)Math::min((int)Renderer::getScreenHeight(), (int)(Renderer::getScreenWidth() * 0.90f));
  425  		setSize(width, height);
  426  	}
  427  
  428  	// A header with an image beside it reads from the left: title and
  429  	// subtitle line up on the column's edge instead of centring in it, and
  430  	// the subtitle's tabs become columns (a centred text draws a tab as a
  431  	// space). In both modes -- this block used to sit behind the full-screen
  432  	// return above, so on every handheld panel the lines stayed centred while
  433  	// GuiGameAchievements measured their right edge as if they were not, and
  434  	// placed its bar over them (#160).
  435  	if (mTitleImage != nullptr && mTitle != nullptr && mTitle->isVisible())
  436  	{
  437  		float pad = Renderer::getScreenWidth() * 0.012;
  438  		mTitle->setPadding(Vector4f(pad, 0.0f, pad, 0.0f));
  439  		mTitle->setHorizontalAlignment(ALIGN_LEFT);
  440  
  441  		if (mSubtitle != nullptr)
  442  		{
  443  			mSubtitle->setPadding(Vector4f(pad, 0.0f, pad, 0.0f));
  444  			mSubtitle->setHorizontalAlignment(ALIGN_LEFT);
  445  		}
  446  	}
  447  }
  448  
  449  void MenuComponent::onSizeChanged()
  450  {
  451  	GuiComponent::onSizeChanged();
  452  
  453  	mBackground.fitTo(mSize, Vector3f::Zero(), Vector2f(-32, -32));
  454  
  455  	// update grid row/col sizes
  456  	mGrid.setRowHeight(0, TITLE_HEIGHT, false);
  457  	mGrid.setRowHeight(3, getButtonGridHeight(), false);
  458  
  459  	if (mTabs == nullptr || mTabs->size() == 0)
  460  		mGrid.setRowHeight(1, 0.00001f);
  461  	else
  462  	{
  463  		const float titleHeight = mTitle->getFont()->getLetterHeight();
  464  		mGrid.setRowHeight(1, titleHeight * 2);
  465  	}
  466  
  467  	mGrid.setSize(mSize);
  468  
  469  	// Fix size if the Title Image replaces the title
  470  	if (mTitleImage != nullptr && (mTitle == nullptr || !mTitle->isVisible()))
  471  	{		
  472  		mTitleImage->setOrigin(0.5f, 0.5f);
  473  		mTitleImage->setPosition(getPosition().x() + mSize.x() / 2.0f, getPosition().y() + TITLE_HEIGHT / 2.0f);
  474  		mTitleImage->setMaxSize(mSize.x() * 0.85f, TITLE_HEIGHT);
  475  	}
  476  }
  477  
  478  void MenuComponent::clearButtons()
  479  {
  480  	mButtons.clear();
  481  	updateGrid();
  482  	updateSize();
  483  }
  484  
  485  void MenuComponent::addButton(const std::string& name, const std::string& helpText, const std::function<void()>& callback)
  486  {
  487  	mButtons.push_back(std::make_shared<ButtonComponent>(mWindow, Utils::String::toUpper(name), helpText, callback));
  488  	updateGrid();
  489  	updateSize();
  490  }
  491  
  492  void MenuComponent::setButtonGrid(std::shared_ptr<GuiComponent> grid)
  493  {
  494  	if (mButtonGrid)
  495  		mGrid.removeEntry(mButtonGrid);
  496  
  497  	mButtonGrid.reset();
  498  
  499  	if (grid)
  500  	{
  501  		mButtonGrid = grid;
  502  		mGrid.setEntry(mButtonGrid, Vector2i(0, 3), true, false, Vector2i(1, 1), GridFlags::BORDER_TOP);
  503  	}
  504  }
  505  
  506  void MenuComponent::setCursorToButton(int index)
  507  {
  508  	if (!mButtonGrid || index < 0 || index >= (int) mButtons.size())
  509  		return;
  510  	// The inner cursor first, then the outer focus, so the focus event that
  511  	// the outer move raises lands on the button asked for.
  512  	std::static_pointer_cast<ComponentGrid>(mButtonGrid)->setCursorTo(Vector2i(index, 0));
  513  	mGrid.setCursorTo(mButtonGrid);
  514  	updateHelpPrompts();
  515  }
  516  
  517  void MenuComponent::updateGrid()
  518  {
  519  	if (mButtonGrid)
  520  		mGrid.removeEntry(mButtonGrid);
  521  
  522  	mButtonGrid.reset();
  523  
  524  	if (mButtons.size())
  525  	{
  526  		mButtonGrid = makeButtonGrid(mWindow, mButtons);
  527  		mGrid.setEntry(mButtonGrid, Vector2i(0, 3), true, false, Vector2i(1, 1), GridFlags::BORDER_TOP);
  528  	}
  529  }
  530  
  531  std::vector<HelpPrompt> MenuComponent::getHelpPrompts()
  532  {
  533  	return mGrid.getHelpPrompts();
  534  }
  535  
  536  void MenuComponent::onShow()
  537  {
  538    GuiComponent::onShow();
  539    //TextToSpeech::getInstance()->say(mTitle->getText());
  540    getList()->saySelectedLine();
  541  }
  542  
  543  std::shared_ptr<ComponentGrid> makeButtonGrid(Window* window, const std::vector< std::shared_ptr<ButtonComponent> >& buttons)
  544  {
  545  	std::shared_ptr<ComponentGrid> buttonGrid = std::make_shared<ComponentGrid>(window, Vector2i((int)buttons.size(), 2));
  546  
  547  	float buttonGridWidth = (float)BUTTON_GRID_HORIZ_PADDING * buttons.size(); // initialize to padding
  548  	for(int i = 0; i < (int)buttons.size(); i++)
  549  	{
  550  		buttonGrid->setEntry(buttons.at(i), Vector2i(i, 0), true, false);
  551  		buttonGridWidth += buttons.at(i)->getSize().x();
  552  	}
  553  	for(unsigned int i = 0; i < buttons.size(); i++)
  554  	{
  555  		buttonGrid->setColWidthPerc(i, (buttons.at(i)->getSize().x() + BUTTON_GRID_HORIZ_PADDING) / buttonGridWidth);
  556  	}
  557  
  558  	buttonGrid->setSize(buttonGridWidth, buttons.at(0)->getSize().y() + BUTTON_GRID_VERT_PADDING + 2);
  559  	buttonGrid->setRowHeightPerc(1, 2 / buttonGrid->getSize().y()); // spacer row to deal with dropshadow to make buttons look centered
  560  
  561  	return buttonGrid;
  562  }
  563  
  564  std::shared_ptr<ImageComponent> makeArrow(Window* window)
  565  {
  566  	auto menuTheme = ThemeData::getMenuTheme();
  567  
  568  	auto bracket = std::make_shared<ImageComponent>(window);
  569  	bracket->setImage(ThemeData::getMenuTheme()->Icons.arrow); // ":/arrow.svg");
  570  	bracket->setColorShift(menuTheme->Text.color);
  571  	bracket->setResize(0, round(menuTheme->Text.font->getLetterHeight()));
  572  
  573  	return bracket;
  574  }
```

## MenuComponent.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_COMPONENTS_MENU_COMPONENT_H
    3  #define ES_CORE_COMPONENTS_MENU_COMPONENT_H
    4  
    5  #include "components/ComponentGrid.h"
    6  #include "components/ComponentList.h"
    7  #include "components/NinePatchComponent.h"
    8  #include "components/TextComponent.h"
    9  #include "utils/StringUtil.h"
   10  #include "components/ComponentTab.h"
   11  
   12  class ButtonComponent;
   13  class ImageComponent;
   14  
   15  std::shared_ptr<ComponentGrid> makeButtonGrid(Window* window, const std::vector< std::shared_ptr<ButtonComponent> >& buttons);
   16  std::shared_ptr<ImageComponent> makeArrow(Window* window);
   17  
   18  #define TITLE_VERT_PADDING (Renderer::getScreenHeight()*0.0637f)
   19  #define TITLE_WITHSUB_VERT_PADDING (Renderer::getScreenHeight()*0.05f)
   20  #define SUBTITLE_VERT_PADDING (Renderer::getScreenHeight()*0.019f)
   21  
   22  class MenuComponent : public GuiComponent
   23  {
   24  public:
   25  	MenuComponent(Window* window, 
   26  		const std::string& title, const std::shared_ptr<Font>& titleFont = Font::get(FONT_SIZE_LARGE),
   27  		const std::string& subTitle = "", bool tabbedUI = true);
   28  
   29  	void onSizeChanged() override;
   30  
   31  	inline void setUpdateType(ComponentListFlags::UpdateType updateType) { mList->setUpdateType(updateType); }
   32  
   33  	inline void addRow(const ComponentListRow& row, bool setCursorHere = false, bool doUpdateSize = true, const std::string& userData = "") { mList->addRow(row, setCursorHere, true, userData); if (doUpdateSize) updateSize(); }
   34  	inline void clear() { mList->clear(); }
   35  
   36  	void addWithLabel(const std::string& label, const std::shared_ptr<GuiComponent>& comp, const std::function<void()>& func = nullptr, const std::string& iconName = "", bool setCursorHere = false);
   37  	void addWithDescription(const std::string& label, const std::string& description, const std::shared_ptr<GuiComponent>& comp, const std::function<void()>& func = nullptr, const std::string& iconName = "", bool setCursorHere = false, bool multiLine = false, const std::string& userData = "", bool doUpdateSize = true);
   38  	void addEntry(const std::string& name, bool add_arrow = false, const std::function<void()>& func = nullptr, const std::string& iconName = "", bool setCursorHere = false, bool onButtonRelease = false, const std::string& userData = "", bool doUpdateSize = true);
   39  	void addGroup(const std::string& label, bool forceVisible = false, bool doUpdateSize = true) { mList->addGroup(label, forceVisible); if (doUpdateSize) updateSize(); }
   40  	void removeLastRowIfGroup(bool doUpdateSize = true) { mList->removeLastRowIfGroup(); if (doUpdateSize) updateSize(); }
   41  	void removeEntry(const std::string& userData, bool doUpdateSize = true) { mList->remove(userData); if (doUpdateSize) updateSize(); }
   42  
   43  	void addButton(const std::string& label, const std::string& helpText, const std::function<void()>& callback);
   44  
   45  	void setButtonGrid(std::shared_ptr<GuiComponent> grid);
   46  
   47  	void setTitle(const std::string& title, const std::shared_ptr<Font>& font = nullptr);
   48  	void setSubTitle(const std::string& text);
   49  	void setTitleImage(std::shared_ptr<ImageComponent> titleImage, bool replaceTitle = false);
   50  
   51  	inline void setCursorToList() { mGrid.setCursorTo(mList); }
   52  	inline void setCursorToButtons() { if (mButtonGrid) mGrid.setCursorTo(mButtonGrid); }
   53  	// Focus one button by index. A bar rebuilt with clearButtons()/addButton()
   54  	// comes back with its cursor on the first button and nothing highlighted;
   55  	// a page that relabels a button in place hands the focus back to it here.
   56  	void setCursorToButton(int index);
   57  	inline bool isCursorToButtons() { return mButtonGrid && mGrid.isCursorTo(mButtonGrid); }
   58  
   59  	inline int getCursorIndex() const { return mList->getCursorIndex(); }
   60  
   61  	inline int size() const { return mList->size(); }
   62  	std::string getSelected() { return mList->getSelected(); }
   63  
   64  	virtual std::vector<HelpPrompt> getHelpPrompts() override;
   65  
   66  	void onShow() override;
   67  
   68  	float getHeaderGridHeight() const;
   69  	float getTitleHeight() const;
   70  	float getButtonGridHeight() const;
   71  
   72  	void setMaxHeight(float maxHeight) 
   73  	{ 
   74  		if (mMaxHeight == maxHeight)
   75  			return;
   76  
   77  		mMaxHeight = maxHeight; 
   78  		updateSize();
   79  	}
   80  
   81  	virtual void updateSize();
   82  	void clearButtons();
   83  
   84  	std::shared_ptr<ComponentList> getList() { return mList; };
   85  	// The subtitle as the header lays it out -- its font, text, padding,
   86  	// position and the width of the header's text column (the game image's
   87  	// column begins where it ends). A page that draws beside or under the
   88  	// header lines measures them here rather than guessing a fraction (#160).
   89  	std::shared_ptr<TextComponent> getSubTitle() { return mSubtitle; };
   90  	
   91  	static void addMenuIcon(Window* window, ComponentListRow& row, const std::string& iconName);
   92  
   93  	void addTab(const std::string label, const std::string value = "", bool setCursorHere = false);
   94  	inline void setOnTabIndexChanged(const std::function<void()>& callback) { mOnTabIndexChanged = callback; };
   95  	int getTabIndex() { return mTabIndex; }
   96  
   97  	bool input(InputConfig* config, Input input) override;
   98  
   99  protected:
  100  	virtual void OnTabChanged(int newIndex) { if (mOnTabIndexChanged != nullptr) mOnTabIndexChanged();  };
  101  
  102  private:
  103  	void updateGrid();
  104  
  105  	NinePatchComponent mBackground;
  106  	ComponentGrid mGrid;
  107  
  108  	std::shared_ptr<ComponentGrid> mHeaderGrid;
  109  	std::shared_ptr<TextComponent> mTitle;
  110  	std::shared_ptr<TextComponent> mSubtitle;
  111  	std::shared_ptr<ImageComponent> mTitleImage;
  112  	std::shared_ptr<ComponentList> mList;
  113  	std::shared_ptr<GuiComponent>  mButtonGrid;
  114  	std::shared_ptr<ComponentTab>	mTabs;
  115  	int mTabIndex;
  116  	std::vector< std::shared_ptr<ButtonComponent> > mButtons;
  117  
  118  	float mMaxHeight;
  119  	std::function<void()> mOnTabIndexChanged;
  120  };
  121  
  122  #endif // ES_CORE_COMPONENTS_MENU_COMPONENT_H
```

## MultiLineMenuEntry.cpp (whole, fork-modified, at the pin)

```text
    1  #include "MultiLineMenuEntry.h"
    2  #include "Window.h"
    3  #include "components/TextComponent.h"
    4  #include "components/ComponentGrid.h"
    5  #include "components/ComponentList.h"
    6  #include "math/Vector2i.h"
    7  #include "math/Vector2f.h"
    8  #include "ThemeData.h"
    9  #include "utils/HtmlColor.h"
   10  
   11  #define SUBSTRING_OPACITY	192
   12  
   13  MultiLineMenuEntry::MultiLineMenuEntry(Window* window, const std::string& text, const std::string& substring, bool multiLine) :
   14  	ComponentGrid(window, Vector2i(1, 2))
   15  {
   16  	mMultiLine = multiLine;
   17  	mSizeChanging = false;
   18  	mDimmed = false;
   19  
   20  	auto theme = ThemeData::getMenuTheme();
   21  	mColor = theme->Text.color;
   22  
   23  	mText = std::make_shared<TextComponent>(mWindow, text.c_str(), theme->Text.font, theme->Text.color);
   24  	mText->setMultiLine(TextComponent::MultiLineType::SINGLELINE);
   25  	mText->setVerticalAlignment(ALIGN_TOP);
   26  
   27  	mSubstring = std::make_shared<TextComponent>(mWindow, substring.c_str(), theme->TextSmall.font, Utils::HtmlColor::applyColorOpacity(theme->Text.color, SUBSTRING_OPACITY));
   28  	mSubstring->setVerticalAlignment(ALIGN_TOP);
   29  
   30  	if (!multiLine)
   31  		mSubstring->setMultiLine(TextComponent::MultiLineType::SINGLELINE);
   32  
   33  	setEntry(mText, Vector2i(0, 0), true, true);
   34  	setEntry(mSubstring, Vector2i(0, 1), false, true);
   35  
   36  	layoutRows();
   37  }
   38  
   39  // The two rows from the texts' natural heights, which for a single-line
   40  // text is its font's height plus its padding. Not from the components'
   41  // current sizes: the grid hands each text its cell -- 0.9 and 1.1 of the
   42  // natural heights, below -- and TextComponent stops sizing itself once it
   43  // has been given a height, so reading the cells back here made every
   44  // setDescription shrink the label and grow the line by ten percent. A row
   45  // refreshed once looked a little tight; one refreshed per game of a
   46  // 37-game scan was a screen tall with the two texts drawn on top of each
   47  // other (fork #241, 2026-09-22). The multi-line substring keeps its own
   48  // measured height: onSizeChanged gives it a zero height first, so the
   49  // value read is fresh.
   50  static float naturalHeight(const std::shared_ptr<TextComponent>& text)
   51  {
   52  	if (text->getFont() == nullptr)
   53  		return text->getSize().y();
   54  	const Vector4f padding = text->getPadding();
   55  	return text->getFont()->getHeight() + padding.y() + padding.w();
   56  }
   57  
   58  void MultiLineMenuEntry::layoutRows()
   59  {
   60  	float th = naturalHeight(mText);
   61  
   62  	if (mSubstring->getText().empty())
   63  	{
   64  		setRowHeight(0, th);
   65  		setRowHeight(1, 0);
   66  
   67  		setSize(Vector2f(mSize.x(), th));
   68  	}
   69  	else
   70  	{
   71  		float sh = mMultiLine ? mSubstring->getSize().y() : naturalHeight(mSubstring);
   72  		float h = th + sh;
   73  
   74  		setRowHeightPerc(0, (th * 0.9) / h);
   75  		setRowHeightPerc(1, (sh * 1.1) / h);
   76  
   77  		setSize(Vector2f(mSize.x(), h));
   78  	}
   79  }
   80  
   81  void MultiLineMenuEntry::setColor(unsigned int color)
   82  {
   83  	mColor = color;
   84  	const unsigned int shown = mDimmed ? ComponentListFlags::dimmed(color) : color;
   85  	mText->setColor(shown);
   86  	mSubstring->setColor(Utils::HtmlColor::applyColorOpacity(shown, SUBSTRING_OPACITY));
   87  }
   88  
   89  void MultiLineMenuEntry::setDimmed(bool dimmed)
   90  {
   91  	mDimmed = dimmed;
   92  	setColor(mColor);
   93  }
   94  
   95  // A ComponentGrid draws nothing of its own, so padding set on the entry has
   96  // to reach the two text components inside it. Without this, an entry placed
   97  // in a non-selectable row sits flush against the left edge while selectable
   98  // rows and group headers are inset by ComponentList (which only offsets
   99  // selectable rows -- see TOTAL_HORIZONTAL_PADDING_PX there).
  100  void MultiLineMenuEntry::setPadding(const Vector4f padding)
  101  {
  102  	GuiComponent::setPadding(padding);
  103  	mText->setPadding(padding);
  104  	mSubstring->setPadding(padding);
  105  }
  106  
  107  std::string MultiLineMenuEntry::getDescription()
  108  {
  109  	return mSubstring->getText();
  110  }
  111  
  112  void MultiLineMenuEntry::setDescription(const std::string& description)
  113  {
  114  	mSubstring->setText(description);
  115  	if (mMultiLine)
  116  		onSizeChanged();
  117  	else
  118  		layoutRows();
  119  }
  120  
  121  void MultiLineMenuEntry::onSizeChanged()
  122  {		
  123  	ComponentGrid::onSizeChanged();
  124  
  125  	if (mMultiLine && mSubstring && mSize.x() > 0 && !mSizeChanging)
  126  	{
  127  		mSizeChanging = true;
  128  
  129  		mText->setSize(mSize.x(), 0);
  130  		mSubstring->setSize(mSize.x(), 0);
  131  
  132  		layoutRows();
  133  
  134  		mSizeChanging = false;
  135  	}
  136  }
  137  
  138  void MultiLineMenuEntry::onFocusGained()
  139  {
  140  	ComponentGrid::onFocusGained();
  141  
  142  	if (!mMultiLine && mSubstring)
  143  		mSubstring->setAutoScroll(TextComponent::AutoScrollType::HORIZONTAL);
  144  
  145  }
  146  
  147  void MultiLineMenuEntry::onFocusLost()
  148  {
  149  	ComponentGrid::onFocusLost();
  150  
  151  	if (!mMultiLine && mSubstring)
  152  		mSubstring->setAutoScroll(TextComponent::AutoScrollType::NONE);
  153  }
```

## MultiLineMenuEntry.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  
    3  #include <string>
    4  #include "components/ComponentGrid.h"
    5  
    6  class TextComponent;
    7  class Window;
    8  
    9  class MultiLineMenuEntry : public ComponentGrid
   10  {
   11  public:
   12  	MultiLineMenuEntry(Window* window, const std::string& text, const std::string& substring, bool multiLine = false);
   13  
   14  	void setColor(unsigned int color) override;
   15  	// A dimmed entry stays dimmed: the dim is applied on every setColor,
   16  	// which ComponentList calls each frame (ComponentListFlags::dimmed,
   17  	// fork #182).
   18  	void setDimmed(bool dimmed);
   19  	bool isDimmed() const { return mDimmed; }
   20  	void setPadding(const Vector4f padding) override;
   21  	void onSizeChanged() override;
   22  	void onFocusGained() override;
   23  	void onFocusLost() override;
   24  	
   25  	std::string getDescription();
   26  	// A line set later re-lays the entry: an entry built with no line is
   27  	// one line high and grows when one arrives, and shrinks when it goes
   28  	// (the WI-FI NETWORK row, whose line is asked off the interface thread and
   29  	// is often nothing -- fork #191). The list holding the row still has to
   30  	// be re-laid by the caller (GuiSettings::updateSize).
   31  	void setDescription(const std::string& description);
   32  
   33  protected:
   34  	// The two rows' heights from the two texts: the label alone when the
   35  	// line under it is empty, both otherwise. The constructor, a later
   36  	// setDescription and the multi-line relayout all go through here.
   37  	void layoutRows();
   38  
   39  	bool mMultiLine;
   40  	bool mSizeChanging;
   41  	bool mDimmed;
   42  	// The colour the row last gave us, so setDimmed can re-apply it.
   43  	unsigned int mColor;
   44  	std::shared_ptr<TextComponent> mText;
   45  	std::shared_ptr<TextComponent> mSubstring;
   46  };
```

## NinePatchComponent.cpp `:169-185` (an excerpt, upstream-carried, at the pin)

```text
  169  	Transform4x4f trans = parentTrans * getTransform();
  170  
  171  	auto rect = Renderer::getScreenRect(trans, mSize);
  172  	if (mRotation == 0 && trans.r0().y() == 0 && !Renderer::isVisibleOnScreen(rect))
  173  		return;
  174  
  175  	if (!mCustomShader.path.empty() && mCustomShaderIsPostProcess)
  176  	{
  177  		int margin = 50; // Apply pixel margin for postProcessShader
  178  
  179  		int x = Math::max(0.0f, rect.x + mCornerSize.x() / 2.0f - margin);
  180  		int y = Math::max(0.0f, rect.y + mCornerSize.y() / 2.0f - margin);
  181  		int w = Math::min((float) Renderer::getScreenWidth(), rect.w - mCornerSize.x() + 2 * margin);
  182  		int h = Math::min((float) Renderer::getScreenHeight(), rect.h - mCornerSize.y() + 2 * margin);
  183  
  184  		if (Renderer::getScreenRotate() == 0)
  185  		{
```

## NinePatchComponent.cpp `:318-334` (an excerpt, upstream-carried, at the pin)

```text
  318  		return;
  319  
  320  	mPath = path;
  321  
  322  	if (mTexture != nullptr)
  323  		mTexture->setRequired(false);
  324  
  325  	auto prev = mTexture;
  326  	mTexture = TextureResource::get(mPath, false, true, !asyncLoading);
  327  	mTextureLoaded = mTexture != nullptr && mTexture->isLoaded();
  328  
  329  	if (isShowing() && mTexture != nullptr)
  330  		mTexture->setRequired(true);
  331  
  332  	buildVertices();
  333  }
  334  
```

## NinePatchComponent.cpp `:407-423` (an excerpt, upstream-carried, at the pin)

```text
  407  	if (mTexture != nullptr)
  408  		mTexture->setRequired(true);	
  409  }
  410  
  411  void NinePatchComponent::onHide()
  412  {
  413  	GuiComponent::onHide();
  414  
  415  #if defined(USE_OPENGLES_30)
  416  	// Post-process textures are raw renderer objects rather than reloadable
  417  	// TextureResources. Release the cache while the context is still valid so a
  418  	// renderer/context restart cannot leave this component holding a stale name.
  419  	if (mPostProcessTextureId != (unsigned int)-1)
  420  	{
  421  		Renderer::destroyTexture(mPostProcessTextureId);
  422  		mPostProcessTextureId = (unsigned int)-1;
  423  	}
```

## OptionListComponent.h `:80-108` (an excerpt, upstream-carried, at the pin)

```text
   80  
   81  					if (mParent->mMultiSelect)
   82  					{
   83  						row.makeAcceptInputHandler([this, &e]
   84  						{
   85  							e.selected = !e.selected;														
   86  							mParent->onSelectedChanged();
   87  						});
   88  					}
   89  					else
   90  					{
   91  						row.makeAcceptInputHandler([this, &e]
   92  						{
   93  							mParent->mEntries.at(mParent->getSelectedId()).selected = false;
   94  							e.selected = true;
   95  							mParent->onSelectedChanged();
   96  							delete this;
   97  						});
   98  					}
   99  				}
  100  				else
  101  				{
  102  					if (!it->description.empty())
  103  						row.addElement(std::make_shared<MultiLineMenuEntry>(mWindow, Utils::String::toUpper(it->name), it->description), true);
  104  					else
  105  					{
  106  						auto text = std::make_shared<TextComponent>(mWindow, e.treeChild ? "      " + Utils::String::toUpper(it->name) : Utils::String::toUpper(it->name), font, color);
  107  						if (EsLocale::isRTL())
  108  							text->setHorizontalAlignment(Alignment::ALIGN_RIGHT);
```

## OptionListComponent.h `:132-213` (an excerpt, upstream-carried, at the pin)

```text
  132  						el.item = &e;
  133  
  134  						// for select all/none
  135  						mCheckBoxes.push_back(el);
  136  					}
  137  					else {
  138  						// input handler for non-multiselect
  139  						// update selected value and close
  140  						row.makeAcceptInputHandler([this, &e]
  141  						{
  142  							mParent->mEntries.at(mParent->getSelectedId()).selected = false;
  143  							e.selected = true;
  144  							mParent->onSelectedChanged();
  145  							delete this;
  146  						});
  147  					}
  148  				}
  149  
  150  
  151  				if (!e.group.empty())
  152  					mMenu.addGroup(e.group);
  153  
  154  				// also set cursor to this row if we're not multi-select and this row is selected
  155  				mMenu.addRow(row, (!mParent->mMultiSelect && it->selected), false);
  156  			}
  157  
  158  			mMenu.addButton(_("BACK"), _("accept"), [this] { delete this; }); 
  159  
  160  			if (mParent->mMultiSelect)
  161  			{
  162  				mMenu.addButton(_("SELECT ALL"), _("select all"), [this]
  163  				{
  164  					for (unsigned int i = 0; i < mParent->mEntries.size(); i++)
  165  					{
  166  						mParent->mEntries.at(i).selected = true;
  167  						mCheckBoxes.at(i).checkbox->setImage(CHECKED_PATH);
  168  					}
  169  					mParent->onSelectedChanged();
  170  				});
  171  
  172  				mMenu.addButton(_("SELECT NONE"), _("select none"), [this]
  173  				{
  174  					for (unsigned int i = 0; i < mParent->mEntries.size(); i++)
  175  					{
  176  						mParent->mEntries.at(i).selected = false;
  177  						mCheckBoxes.at(i).checkbox->setImage(UNCHECKED_PATH);
  178  					}
  179  					mParent->onSelectedChanged();
  180  				});
  181  			}
  182  
  183  			if (Renderer::ScreenSettings::fullScreenMenus())
  184  				mMenu.setPosition((Renderer::getScreenWidth() - mMenu.getSize().x()) / 2, (Renderer::getScreenHeight() - mMenu.getSize().y()) / 2);
  185  			else
  186  				mMenu.setPosition((Renderer::getScreenWidth() - mMenu.getSize().x()) / 2, Renderer::getScreenHeight() * 0.15f);
  187  
  188  			addChild(&mMenu);
  189  		}
  190  
  191  		bool input(InputConfig* config, Input input) override
  192  		{
  193  			if(config->isMappedTo(BUTTON_BACK, input) && input.value != 0) 
  194  			{
  195  				delete this;
  196  				return true;
  197  			}
  198  
  199  			return GuiComponent::input(config, input);
  200  		}
  201  
  202  		std::vector<HelpPrompt> getHelpPrompts() override
  203  		{
  204  			auto prompts = mMenu.getHelpPrompts();
  205  			prompts.push_back(HelpPrompt(BUTTON_BACK, _("BACK")));
  206  			return prompts;
  207  		}
  208  	};
  209  
  210  public:
  211  	OptionListComponent(Window* window, const std::string& name, bool multiSelect = false, bool multiSelectShowNames = false) : GuiComponent(window), mMultiSelect(multiSelect), mName(name),
  212  		 mText(window), mLeftArrow(window), mRightArrow(window), mMultiSelectShowNames(multiSelectShowNames)
  213  	{
```

## OptionListComponent.h `:247-263` (an excerpt, upstream-carried, at the pin)

```text
  247  			mLeftArrow.setFlipX(true);
  248  			addChild(&mLeftArrow);
  249  
  250  			mRightArrow.setImage(ThemeData::getMenuTheme()->Icons.option_arrow); // ":/option_arrow.svg");
  251  			mRightArrow.setColorShift(theme->Text.color);
  252  			addChild(&mRightArrow);
  253  		}
  254  
  255  		setSize(mLeftArrow.getSize().x() + mRightArrow.getSize().x(), theme->Text.font->getHeight());
  256  	}
  257  
  258  	virtual void setColor(unsigned int color)
  259  	{
  260  		mText.setColor(color);
  261  		mLeftArrow.setColorShift(color);
  262  		mRightArrow.setColorShift(color);
  263  	}
```

## OptionListComponent.h `:268-292` (an excerpt, upstream-carried, at the pin)

```text
  268  		GuiComponent::onSizeChanged();
  269  
  270  		mLeftArrow.setResize(0, mText.getFont()->getLetterHeight());
  271  		mRightArrow.setResize(0, mText.getFont()->getLetterHeight());
  272  
  273  		if(mSize.x() < (mLeftArrow.getSize().x() + mRightArrow.getSize().x()))
  274  			LOG(LogWarning) << "OptionListComponent too narrow!";
  275  
  276  		mText.setSize(mSize.x() - mLeftArrow.getSize().x() - mRightArrow.getSize().x(), mText.getFont()->getHeight());
  277  
  278  		// position
  279  		mLeftArrow.setPosition(0, (mSize.y() - mLeftArrow.getSize().y()) / 2);
  280  		mText.setPosition(mLeftArrow.getPosition().x() + mLeftArrow.getSize().x(), (mSize.y() - mText.getSize().y()) / 2);
  281  		mRightArrow.setPosition(mText.getPosition().x() + mText.getSize().x(), (mSize.y() - mRightArrow.getSize().y()) / 2);
  282  	}
  283  
  284  	bool input(InputConfig* config, Input input) override
  285  	{
  286  		if(input.value != 0)
  287  		{
  288  			if(config->isMappedTo(BUTTON_OK, input))
  289  			{
  290  				if (mEntries.size() > 0)
  291  					open();
  292  
```

## OptionListComponent.h `:302-332` (an excerpt, upstream-carried, at the pin)

```text
  302  					// move selection to previous
  303  					unsigned int i = getSelectedId();
  304  					int next = (int)i - 1;
  305  					if(next < 0)
  306  						next += (int)mEntries.size();
  307  
  308  					mEntries.at(i).selected = false;
  309  					mEntries.at(next).selected = true;
  310  					onSelectedChanged();
  311  					return true;
  312  
  313  				}else if(config->isMappedLike("right", input))
  314  				{
  315  					if (mEntries.size() == 0)
  316  						return true;
  317  
  318  					// move selection to next
  319  					unsigned int i = getSelectedId();
  320  					int next = (i + 1) % mEntries.size();
  321  					mEntries.at(i).selected = false;
  322  					mEntries.at(next).selected = true;
  323  					onSelectedChanged();
  324  					return true;
  325  
  326  				}
  327  			}
  328  		}
  329  		return GuiComponent::input(config, input);
  330  	}
  331  
  332  	std::vector<T> getSelectedObjects()
```

## OptionListComponent.h `:624-661` (an excerpt, upstream-carried, at the pin)

```text
  624  					onSizeChanged();
  625  					if(mParent) // hack since theres no "on child size changed" callback atm...
  626  						mParent->onSizeChanged();
  627  					break;
  628  				}
  629  			}
  630  		}
  631          
  632  		if (mSelectedChangedCallback)
  633  			mSelectedChangedCallback(mEntries.at(getSelectedId()).object);		
  634  	}
  635  
  636  	std::vector<HelpPrompt> getHelpPrompts() override
  637  	{
  638  		std::vector<HelpPrompt> prompts;
  639  		if(!mMultiSelect)
  640  			prompts.push_back(HelpPrompt("left/right", _("CHANGE")));
  641  
  642  		prompts.push_back(HelpPrompt(BUTTON_OK, _("SELECT")));
  643  		return prompts;
  644  	}
  645  
  646  	bool mMultiSelect;
  647  	bool mMultiSelectShowNames;
  648  
  649  	std::string mName;
  650  	std::string mGroup;
  651  
  652  	T firstSelected;
  653  	TextComponent mText;
  654  	ImageComponent mLeftArrow;
  655  	ImageComponent mRightArrow;
  656  
  657  	std::vector<OptionListData> mEntries;
  658  	std::function<void(const T&)> mSelectedChangedCallback;
  659  };
  660  
  661  #endif // ES_CORE_COMPONENTS_OPTION_LIST_COMPONENT_H
```

## RatingComponent.cpp `:150-169` (an excerpt, upstream-carried, at the pin)

```text
  150  	const unsigned int unFilledColor = Renderer::convertColor(mUnfilledColor & 0xFFFFFF00 | (unsigned char)((mUnfilledColor & 0xFF) * opacity));
  151  	for (int i = 4; i < 8; i++)
  152  		mVertices[i].col = unFilledColor;
  153  }
  154  
  155  void RatingComponent::render(const Transform4x4f& parentTrans)
  156  {
  157  	if (mFilledTexture == nullptr)
  158  		mFilledTexture = TextureResource::get(":/star_filled.svg", true, true);
  159  
  160  	if (mUnfilledTexture == nullptr)
  161  		mUnfilledTexture = TextureResource::get(":/star_unfilled.svg", true, true);
  162  
  163  	if (!isVisible() || mFilledTexture == nullptr || mUnfilledTexture == nullptr)
  164  		return;
  165  
  166  	Transform4x4f trans = parentTrans * getTransform();
  167  
  168  	auto rect = Renderer::getScreenRect(trans, mSize);
  169  	if (mRotation == 0 && trans.r0().y() == 0 && !Renderer::isVisibleOnScreen(rect))
```

## RatingComponent.cpp `:184-234` (an excerpt, upstream-carried, at the pin)

```text
  184  	{
  185  		Renderer::drawTriangleStrips(&mVertices[0], 4);
  186  		Renderer::bindTexture(0);
  187  	}
  188  
  189  	renderChildren(trans);
  190  }
  191  
  192  bool RatingComponent::input(InputConfig* config, Input input)
  193  {
  194  	if (config->isMappedTo(BUTTON_OK, input) && input.value != 0)
  195  	{
  196  		mValue += 1.f / NUM_RATING_STARS;
  197  		if (mValue > 1.0f)
  198  			mValue = 0.0f;
  199  
  200  		updateVertices();
  201  	}
  202  
  203  	return GuiComponent::input(config, input);
  204  }
  205  
  206  void RatingComponent::applyTheme(const std::shared_ptr<ThemeData>& theme, const std::string& view, const std::string& element, unsigned int properties)
  207  {
  208  	GuiComponent::applyTheme(theme, view, element, properties);
  209  
  210  	using namespace ThemeFlags;
  211  
  212  	const ThemeData::ThemeElement* elem = theme->getElement(view, element, "rating");
  213  	if (!elem)
  214  		return;
  215  
  216  	bool imgChanged = false;
  217  
  218  	if (properties & PATH && elem->has("filledPath"))
  219  	{
  220  		mFilledTexture = TextureResource::get(elem->get<std::string>("filledPath"), true, true);
  221  		imgChanged = true;
  222  	}
  223  
  224  	if (properties & PATH && elem->has("unfilledPath"))
  225  	{
  226  		mUnfilledTexture = TextureResource::get(elem->get<std::string>("unfilledPath"), true, true);
  227  		imgChanged = true;
  228  	}
  229  
  230  	if (properties & COLOR)
  231  	{
  232  		if (elem->has("color"))
  233  			setColorShift(elem->get<unsigned int>("color"));
  234  
```

## RatingComponent.cpp `:254-274` (an excerpt, upstream-carried, at the pin)

```text
  254  		mValue = Math::clamp(0.0f, 1.0f, elem->get<float>("value"));		
  255  		updateVertices();
  256  	}
  257  
  258  	if (imgChanged)
  259  		onSizeChanged();
  260  }
  261  
  262  std::vector<HelpPrompt> RatingComponent::getHelpPrompts()
  263  {
  264  	std::vector<HelpPrompt> prompts;
  265  	prompts.push_back(HelpPrompt(BUTTON_OK, "add star"));
  266  	return prompts;
  267  }
  268  
  269  void RatingComponent::setHorizontalAlignment(Alignment align)
  270  {
  271  	if (mHorizontalAlignment == align)
  272  		return;
  273  
  274  	mHorizontalAlignment = align;
```

## RectangleComponent.cpp `:30-46` (an excerpt, upstream-carried, at the pin)

```text
   30  
   31  	Renderer::setMatrix(trans);
   32  
   33  	bool rendered = false;
   34  
   35  	if (Renderer::supportShaders() && mRoundCorners != 0 && !mCustomShader.path.empty())
   36  	{
   37  		if (mWhiteTexture == nullptr)
   38  			mWhiteTexture = TextureResource::get(":/white.png");			
   39  
   40  		if (mWhiteTexture->bind())
   41  		{
   42  			if (mColor != 0)
   43  			{
   44  				const unsigned int color = Renderer::convertColor(mColor);
   45  
   46  				Renderer::Vertex mVertices[4];
```

## ScrollableContainer.cpp `:54-132` (an excerpt, upstream-carried, at the pin)

```text
   54  	return mScrollPos;
   55  }
   56  
   57  void ScrollableContainer::setScrollPos(const Vector2f& pos)
   58  {
   59  	mScrollPos = pos;
   60  }
   61  
   62  void ScrollableContainer::update(int deltaTime)
   63  {
   64  	if(mAutoScrollSpeed != 0)
   65  	{
   66  		mAutoScrollAccumulator += deltaTime;
   67  
   68  		//scale speed by our width! more text per line = slower scrolling
   69  		const float widthMod = (680.0f / getSize().x());
   70  		while(mAutoScrollAccumulator >= mAutoScrollSpeed)
   71  		{
   72  			mScrollPos += mScrollDir;
   73  			mAutoScrollAccumulator -= mAutoScrollSpeed;
   74  		}
   75  	}
   76  
   77  	//clip scrolling within bounds
   78  	if(mScrollPos.x() < 0)
   79  		mScrollPos[0] = 0;
   80  	if(mScrollPos.y() < 0)
   81  		mScrollPos[1] = 0;
   82  
   83  	const Vector2f contentSize = getContentSize();
   84  	if(mScrollPos.x() + getSize().x() > contentSize.x())
   85  	{
   86  		mScrollPos[0] = contentSize.x() - getSize().x();
   87  		mAtEnd = true;
   88  	}
   89  
   90  	if(contentSize.y() < getSize().y())
   91  	{
   92  		mScrollPos[1] = 0;
   93  	}else if(mScrollPos.y() + getSize().y() > contentSize.y())
   94  	{
   95  		mScrollPos[1] = contentSize.y() - getSize().y();
   96  		mAtEnd = true;
   97  	}
   98  
   99  	if(mAtEnd)
  100  	{
  101  		mAutoScrollResetAccumulator += deltaTime;
  102  		if(mAutoScrollResetAccumulator >= AUTO_SCROLL_RESET_DELAY)
  103  			reset();
  104  	}
  105  
  106  	GuiComponent::update(deltaTime);
  107  }
  108  
  109  //this should probably return a box to allow for when controls don't start at 0,0
  110  Vector2f ScrollableContainer::getContentSize()
  111  {
  112  	Vector2f max(0, 0);
  113  	for(unsigned int i = 0; i < mChildren.size(); i++)
  114  	{
  115  		Vector2f pos(mChildren.at(i)->getPosition()[0], mChildren.at(i)->getPosition()[1]);
  116  		Vector2f bottomRight = mChildren.at(i)->getSize() + pos;
  117  		if(bottomRight.x() > max.x())
  118  			max.x() = bottomRight.x();
  119  		if(bottomRight.y() > max.y())
  120  			max.y() = bottomRight.y();
  121  	}
  122  
  123  	return max;
  124  }
  125  
  126  void ScrollableContainer::reset()
  127  {
  128  	mScrollPos = Vector2f(0, 0);
  129  	mAutoScrollResetAccumulator = 0;
  130  	mAutoScrollAccumulator = -mAutoScrollDelay + mAutoScrollSpeed;
  131  	mAtEnd = false;
  132  }
```

## SliderComponent.cpp `:36-66` (an excerpt, upstream-carried, at the pin)

```text
   36  	mKnob.setColorShift(mColor);
   37  	
   38  	if (Renderer::isSmallScreen())
   39  		setSize(Renderer::getScreenWidth() * 0.25f, menuTheme->Text.font->getLetterHeight());
   40  	else
   41  		setSize(Renderer::getScreenWidth() * 0.15f, menuTheme->Text.font->getLetterHeight());
   42  }
   43  
   44  int calculatePrecision(float step)
   45  {
   46  	std::string stepStr = std::to_string(step); // Convert the float to string to inspect its representation
   47  	size_t decimalPointPos = stepStr.find('.'); // Find the position of the decimal point
   48  
   49  	if (decimalPointPos == std::string::npos) {
   50  		// No decimal point found, return 0 (no decimals)
   51  		return 0;
   52  	}
   53  
   54  	// Remove trailing zeros by trimming the string from the right
   55  	stepStr.erase(stepStr.find_last_not_of('0') + 1, std::string::npos);
   56  
   57  	// The number of decimal places is the number of characters after the decimal point
   58  	return stepStr.length() - decimalPointPos - 1;
   59  }
   60  
   61  void SliderComponent::setAutoMode(bool isAuto)
   62  {
   63  	mIsAutoMode = isAuto;
   64  	if (isAuto)
   65  	{
   66  		if (mValue < mMin)
```

## SliderComponent.cpp `:110-126` (an excerpt, upstream-carried, at the pin)

```text
  110  
  111  void SliderComponent::setColor(unsigned int color) 
  112  {
  113  	mColor = color;
  114  	mKnob.setColorShift(mColor);
  115  	onValueChanged();
  116  }
  117  
  118  bool SliderComponent::input(InputConfig* config, Input input)
  119  {
  120  	if(config->isMappedLike("left", input))
  121  	{
  122  		if (input.value)
  123  		{
  124  			if (mIsAutoMode && getAuto())
  125  			{
  126  				// If currently at AUTO, do nothing
```

## SliderComponent.cpp `:226-327` (an excerpt, upstream-carried, at the pin)

```text
  226  	Renderer::drawRect(mKnob.getSize().x() / 2, mSize.y() / 2 - lineWidth / 2, width, lineWidth, getCurColor());
  227  
  228  	//render knob
  229  	mKnob.render(trans);
  230  	
  231  	GuiComponent::renderChildren(trans);
  232  }
  233  
  234  void SliderComponent::setValue(float value)
  235  {
  236  	if (mValue == value)
  237  		return;
  238  
  239  	if (mIsAutoMode && value == (mMin - mSingleIncrement))
  240  	{
  241  		mValue = mMin - mSingleIncrement;  // AUTO
  242  	}
  243  	else
  244  	{
  245  		if (value < mMin)
  246  			mValue = mMin;
  247  		else if (value > mMax)
  248  			mValue = mMax;
  249  		else
  250  			mValue = value;
  251  	}
  252  
  253  	onValueChanged();
  254  
  255  	if (mValueChanged)
  256  		mValueChanged(mValue);
  257  }
  258  
  259  float SliderComponent::getValue()
  260  {
  261  	return mValue;
  262  }
  263  
  264  void SliderComponent::onSizeChanged()
  265  {
  266  	GuiComponent::onSizeChanged();
  267  	mFont = Font::get((int)(mSize.y()), FONT_PATH_LIGHT);
  268  	onValueChanged();
  269  }
  270  
  271  void SliderComponent::onValueChanged()
  272  {
  273  	// update suffix textcache
  274  	if (mFont)
  275  	{
  276  		std::stringstream ss;
  277  
  278  		int precision = calculatePrecision(mSingleIncrement);
  279  
  280  		if (mIsAutoMode && getAuto())
  281  		{
  282  			ss << "Auto";  // Display "AUTO"
  283  		}
  284  		else
  285  		{
  286  			ss << std::fixed;
  287  			if (mSingleIncrement < 1)
  288  			{
  289  				ss.precision(precision);
  290  			}
  291  			else
  292  			{
  293  				ss.precision(0);
  294  			}
  295  			ss << mValue;
  296  			ss << mSuffix;
  297  		}
  298  
  299  		const std::string val = ss.str();
  300  
  301  		ss.str("");
  302  		ss.clear();
  303  		ss << std::fixed;
  304  		if (mSingleIncrement < 1)
  305  		{
  306  			ss.precision(precision);
  307  		}
  308  		else
  309  		{
  310  			ss.precision(0);
  311  		}
  312  		ss << mMax;
  313  		ss << mSuffix;
  314  		const std::string max = ss.str();
  315  
  316  		Vector2f textSize = mFont->sizeText(max);
  317  		mValueCache = std::shared_ptr<TextCache>(mFont->buildTextCache(val, mSize.x() - textSize.x(), (mSize.y() - textSize.y()) / 2, getCurColor()));
  318  		mValueCache->metrics.size[0] = textSize.x(); // fudge the width
  319  	}
  320  
  321  	mKnob.setResize(0, mSize.y() * 0.7f);
  322  	float lineLength = mSize.x() - mKnob.getSize().x() - (mValueCache ? mValueCache->metrics.size.x() + 4 : 0);
  323  
  324  	if (mIsAutoMode && getAuto())
  325  	{
  326  		mKnob.setOpacity(0.0f);
  327  		mKnob.setPosition(-mKnob.getSize().x(), mSize.y() / 2);
```

## SliderComponent.cpp `:329-348` (an excerpt, upstream-carried, at the pin)

```text
  329  	else
  330  	{
  331  		mKnob.setOpacity(getOpacity());
  332  		mKnob.setPosition(((mValue - mMin) / (mMax - mMin)) * lineLength, mSize.y() / 2);
  333  	}
  334  
  335  }
  336  
  337  std::vector<HelpPrompt> SliderComponent::getHelpPrompts()
  338  {
  339  	std::vector<HelpPrompt> prompts;
  340  	prompts.push_back(HelpPrompt("left/right", _("CHANGE")));
  341  	return prompts;
  342  }
  343  
  344  bool SliderComponent::hitTest(int x, int y, Transform4x4f& parentTransform, std::vector<GuiComponent*>* pResult)
  345  {
  346  	auto ret = false; // GuiComponent::hitTest(x, y, parentTransform, pResult);
  347  
  348  	auto trans = getTransform() * parentTransform;
```

## SwitchComponent.cpp (whole, fork-modified, at the pin)

```text
    1  #include "SwitchComponent.h"
    2  
    3  #include "resources/Font.h"
    4  #include "components/ComponentList.h"
    5  #include "LocaleES.h"
    6  
    7  SwitchComponent::SwitchComponent(Window* window, bool state, bool hasAuto, bool autoState) : GuiComponent(window), mImage(window), mState(state), mInitialState(state), mHasAuto(hasAuto), mAutoState(autoState), mInitialAutoState(autoState),
    8  	mDimmed(false), mColor(0)
    9  {
   10  	float height = Font::get(FONT_SIZE_MEDIUM)->getLetterHeight();
   11  
   12  	auto menuTheme = ThemeData::getMenuTheme();
   13  	if (menuTheme->Text.font != nullptr)
   14  		height = menuTheme->Text.font->getHeight(1.1f);
   15  
   16  	mColor = menuTheme->Text.color;
   17  	mImage.setImage(menuTheme->Icons.off);
   18  	mImage.setColorShift(mColor);
   19  	mImage.setResize(0, height);
   20  
   21  	if (EsLocale::isRTL())
   22  		mImage.setFlipX(true);
   23  
   24  	mSize = mImage.getSize();
   25  }
   26  
   27  void SwitchComponent::setColor(unsigned int color) 
   28  {
   29  	mColor = color;
   30  	mImage.setColorShift(mDimmed ? ComponentListFlags::dimmed(color) : color);
   31  }
   32  
   33  void SwitchComponent::setDimmed(bool dimmed)
   34  {
   35  	mDimmed = dimmed;
   36  	setColor(mColor);
   37  }
   38  
   39  void SwitchComponent::onOpacityChanged()
   40  {
   41  	mImage.setOpacity(getOpacity());
   42  }
   43  
   44  void SwitchComponent::onSizeChanged()
   45  {
   46  	GuiComponent::onSizeChanged();
   47  	mImage.setSize(mSize);
   48  }
   49  
   50  bool SwitchComponent::input(InputConfig* config, Input input)
   51  {
   52  	if(config->isMappedTo(BUTTON_OK, input) && input.value)
   53  	{
   54  		if(mHasAuto) {
   55  			if(mAutoState) {
   56  				mAutoState = false;
   57  				mState     = true;
   58  			} else if(mState) {
   59  			       mState = false;
   60  			} else {
   61  			       mAutoState = true;
   62  			}
   63  		} else {
   64  			mState = !mState;
   65  		}
   66  		onStateChanged();
   67  		return true;
   68  	}
   69  
   70  	if (config->isMappedLike("left", input) && input.value && (mState || (mHasAuto && mAutoState)))
   71  	{
   72  		if(mHasAuto && !mAutoState) {
   73  			mAutoState = true;
   74  		} else {
   75  			mAutoState = false;
   76  			mState = false;
   77  		}
   78  		onStateChanged();
   79  		return true;
   80  	}
   81  
   82  	if (config->isMappedLike("right", input) && input.value && (!mState || (mHasAuto && mAutoState)))
   83  	{
   84  		if(mHasAuto && !mAutoState) {
   85  			mAutoState = true;
   86  		} else {
   87  			mAutoState = false;
   88  			mState = true;
   89  		}
   90  		onStateChanged();
   91  		return true;
   92  	}
   93  
   94  	return false;
   95  }
   96  
   97  void SwitchComponent::render(const Transform4x4f& parentTrans)
   98  {
   99  	Transform4x4f trans = parentTrans * getTransform();
  100  	
  101  	mImage.render(trans);
  102  
  103  	renderChildren(trans);
  104  }
  105  
  106  bool SwitchComponent::getState() const
  107  {
  108  	return mState;
  109  }
  110  
  111  void SwitchComponent::setState(bool state)
  112  {
  113  	mState = state;
  114  	mInitialState = mState;
  115  	onStateChanged();
  116  }
  117  
  118  std::string SwitchComponent::getValue() const
  119  {
  120  	if(mHasAuto && mAutoState) return "auto";
  121  	return mState ?  "true" : "false";
  122  }
  123  
  124  void SwitchComponent::setValue(const std::string& statestring)
  125  {
  126  	if(mHasAuto && statestring == "auto") {
  127  		mAutoState = true;
  128  	} else {
  129  		if (statestring == "true")
  130  		{
  131  			mState = true;
  132  		}else
  133  		{
  134  			mState = false;
  135  		}
  136  	}
  137  	onStateChanged();
  138  }
  139  
  140  bool SwitchComponent::hasAuto() const {
  141       return mHasAuto;
  142  }
  143  
  144  void SwitchComponent::setHasAuto(bool hasAuto) {
  145       mHasAuto = hasAuto;
  146  }
  147  
  148  bool SwitchComponent::getAutoState() const {
  149       return mAutoState;
  150  }
  151  
  152  void SwitchComponent::setAutoState(bool bAuto) {
  153       mAutoState = bAuto;
  154  }
  155  
  156  void SwitchComponent::onStateChanged()
  157  {
  158  	auto theme = ThemeData::getMenuTheme();
  159  	mImage.setImage((mHasAuto && mAutoState) ? theme->Icons.onoffauto : (mState ? theme->Icons.on : theme->Icons.off));
  160  
  161  	if (mOnChangedCallback != nullptr)
  162  		mOnChangedCallback();
  163  }
  164  
  165  std::vector<HelpPrompt> SwitchComponent::getHelpPrompts()
  166  {
  167  	std::vector<HelpPrompt> prompts;
  168  	prompts.push_back(HelpPrompt(BUTTON_OK, _("CHANGE")));
  169  	return prompts;
  170  }
  171  
  172  bool SwitchComponent::changed() 
  173  {
  174  	return mInitialState != mState || (mHasAuto && mInitialAutoState != mAutoState);
  175  }
```

## SwitchComponent.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_COMPONENTS_SWITCH_COMPONENT_H
    3  #define ES_CORE_COMPONENTS_SWITCH_COMPONENT_H
    4  
    5  #include "components/ImageComponent.h"
    6  #include "GuiComponent.h"
    7  
    8  // A very simple "on/off" switch.
    9  // Should hopefully be switched to use images instead of text in the future.
   10  class SwitchComponent : public GuiComponent
   11  {
   12  public:
   13  	SwitchComponent(Window* window, bool state = false, bool hasAuto = false, bool autoState = false);
   14  
   15  	bool input(InputConfig* config, Input input) override;
   16  	void render(const Transform4x4f& parentTrans) override;
   17  	void onSizeChanged() override;
   18  	void onOpacityChanged();
   19  
   20  	bool getState() const;
   21  	void setState(bool state);
   22  	std::string getValue() const;
   23  	void setValue(const std::string& statestring) override;
   24  	bool changed();
   25  
   26  	bool hasAuto() const;
   27  	void setHasAuto(bool hasAuto);
   28  	bool getAutoState() const;
   29  	void setAutoState(bool bAuto);
   30  
   31  	virtual std::vector<HelpPrompt> getHelpPrompts() override;
   32  
   33  	void setColor(unsigned int color) override;
   34  	// The same rule as MultiLineMenuEntry::setDimmed: the dim is applied on
   35  	// every setColor, which ComponentList calls each frame (fork #182).
   36  	void setDimmed(bool dimmed);
   37  	bool isDimmed() const { return mDimmed; }
   38  
   39  	inline void setOnChangedCallback(const std::function<void()>& callback) {
   40  		mOnChangedCallback = callback;
   41  	}
   42  
   43  private:
   44  	void onStateChanged();
   45  
   46  	ImageComponent mImage;
   47  	bool mState;
   48  	bool mInitialState;
   49  	bool mHasAuto;
   50  	bool mAutoState;
   51  	bool mInitialAutoState;
   52  
   53  	std::function<void()> mOnChangedCallback; 
   54  
   55  	bool mDimmed;
   56  	// The colour the row last gave us, so setDimmed can re-apply it.
   57  	unsigned int mColor;
   58  };
   59  
   60  #endif // ES_CORE_COMPONENTS_SWITCH_COMPONENT_H
```

## TextComponent.cpp `:168-184` (an excerpt, upstream-carried, at the pin)

```text
  168  
  169  	bool popClipRect = false;
  170  
  171  	if (mRotation == 0 && trans.r0().y() == 0)
  172  	{
  173  		if (mExtraType == ExtraType::EXTRACHILDREN && mVerticalAlignment == Alignment::ALIGN_TOP && mMultiline == MultiLineType::MULTILINE && mAutoScroll == AutoScrollType::NONE)
  174  		{
  175  			// Clip multiline - non partial lines
  176  			auto lineHeight = mFont->getHeight(mLineSpacing);
  177  			if (lineHeight > 0)
  178  			{
  179  				auto lines = (int)(rect.h / lineHeight);
  180  				rect.h = lineHeight * lines + 1;
  181  			}
  182  
  183  			Renderer::pushClipRect(rect);
  184  			popClipRect = true;
```

## TextComponent.cpp `:192-208` (an excerpt, upstream-carried, at the pin)

```text
  192  				shader.parameters["s_offset"] = std::to_string((float)mMarqueeOffset);
  193  				shader.parameters["s_height"] = std::to_string(rect.h);
  194  				shader.parameters["s_forcetop"] = "4";
  195  				shader.parameters["s_forcebottom"] = "4";
  196  				mTextCache->setCustomShader(&shader);
  197  
  198  				// Clip multiline - non partial lines
  199  				/*
  200  				auto lineHeight = mFont->getHeight(mLineSpacing);
  201  				if (lineHeight > 0)
  202  				{
  203  					auto nonPartialLines = (int)(rect.h / lineHeight);
  204  					int decal = rect.h - (lineHeight * nonPartialLines);
  205  					shader.parameters["s_forcebottom"] = std::to_string(Math::max(4, decal));
  206  				}*/
  207  			}
  208  
```

## TextComponent.cpp `:307-367` (an excerpt, upstream-carried, at the pin)

```text
  307  	GuiComponent::renderChildren(drawTrans);
  308  
  309  	endCustomClipRect();
  310  
  311  	if (popClipRect)
  312  		Renderer::popClipRect();
  313  }
  314  
  315  void TextComponent::onTextChanged()
  316  {
  317  	mTextLength = -1;
  318  	mTextCache = nullptr;
  319  
  320  	if (mAutoCalcExtent.x())
  321  	{
  322  		auto text = mUppercase ? Utils::String::toUpper(mText) : mText;
  323  		if (mMultiline == MultiLineType::SINGLELINE)
  324  		{
  325  			size_t newline = text.find('\n');
  326  			if (newline != std::string::npos)
  327  				text = text.substr(0, newline); // single line of text - stop at the first newline since it'll mess everything up
  328  		}
  329  
  330  		mSize = mFont->sizeText(text, mLineSpacing);
  331  		mSize[0] += mPadding.x() + mPadding.z();
  332  	}
  333  	else if (mAutoCalcExtent.y())
  334  	{
  335  		if (mMultiline == MultiLineType::SINGLELINE)
  336  			mSize[1] = mFont->getHeight() + mPadding.y() + mPadding.w();
  337  		else
  338  			mSize[1] = mFont->sizeWrappedText(mUppercase ? Utils::String::toUpper(mText) : mText, getSize().x(), mLineSpacing).y() + mPadding.y() + mPadding.w();
  339  	}
  340  }
  341  
  342  void TextComponent::buildTextCache()
  343  {	
  344  	if(!mFont || mText.empty())
  345  	{
  346  		mTextCache.reset();
  347  		return;
  348  	}
  349  
  350  	int sx = mSize.x() - mPadding.x() - mPadding.z();
  351  	int sy = mSize.y() - mPadding.y() - mPadding.w();
  352  
  353  	std::string text = mUppercase ? Utils::String::toUpper(mText) : mText;
  354  
  355  	std::shared_ptr<Font> f = mFont;
  356  	
  357  	bool isMultiline = mMultiline == MultiLineType::MULTILINE;
  358  	if (mMultiline == MultiLineType::AUTO)
  359  		isMultiline = (mAutoScroll != AutoScrollType::HORIZONTAL) && (mSize.y() == 0 || sy > mFont->getHeight(mLineSpacing) * 1.8f);
  360  
  361  	bool addAbbrev = false;
  362  	if (!isMultiline)
  363  	{
  364  		size_t newline = text.find('\n');
  365  		if (newline != std::string::npos)
  366  			text = text.substr(0, newline); // single line of text - stop at the first newline since it'll mess everything up
  367  
```

## TextComponent.cpp `:420-440` (an excerpt, upstream-carried, at the pin)

```text
  420  	if (!mShowing)
  421  	{
  422  		mMarqueeTime = 0;
  423  		mMarqueeOffset = 0;
  424  		mMarqueeOffset2 = 0;
  425  		return;
  426  	}
  427  
  428  	int sy = mSize.y() - mPadding.y() - mPadding.w();
  429  
  430  	bool isMultiline = mMultiline == MultiLineType::MULTILINE;
  431  	if (mMultiline == MultiLineType::AUTO)
  432  		isMultiline = (mAutoScroll != AutoScrollType::HORIZONTAL) && (mSize.y() == 0 || sy > mFont->getHeight(mLineSpacing) * 1.8f); // 1.95f
  433  
  434  	if (mAutoScroll == AutoScrollType::HORIZONTAL && !isMultiline && mSize.x() > 0)
  435  	{
  436  		// always reset the marquee offsets
  437  		mMarqueeOffset = 0;
  438  		mMarqueeOffset2 = 0;
  439  
  440  		std::string text = mUppercase ? Utils::String::toUpper(mText) : mText;
```

## TextComponent.cpp `:475-494` (an excerpt, upstream-carried, at the pin)

```text
  475  	}
  476  	else if(mAutoScroll == AutoScrollType::VERTICAL && mSize.y() > 0)
  477  	{
  478  		std::string text = mUppercase ? Utils::String::toUpper(mText) : mText;
  479  
  480  		// if we're not scrolling and this object's text goes outside our size, marquee it!
  481  
  482  		if (mTextLength < 0)
  483  			mTextLength = mFont->sizeWrappedText(mUppercase ? Utils::String::toUpper(mText) : mText, getSize().x(), mLineSpacing).y();
  484  
  485  		int textLength = mTextLength;
  486  		int limit = mSize.y() - mPadding.y() - mPadding.y();
  487  
  488  		if (textLength > limit)
  489  		{
  490  			mMarqueeTime += deltaTime;
  491  
  492  			while (mMarqueeTime >= mAutoScrollSpeed)
  493  			{
  494  				mMarqueeOffset += 1;
```

## TextComponent.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_COMPONENTS_TEXT_COMPONENT_H
    3  #define ES_CORE_COMPONENTS_TEXT_COMPONENT_H
    4  
    5  #include "resources/Font.h"
    6  #include "GuiComponent.h"
    7  
    8  class ThemeData;
    9  
   10  
   11  // Used to display text.
   12  // TextComponent::setSize(x, y) works a little differently than most components:
   13  //  * (0, 0)                     - will automatically calculate a size that fits the text on one line (expand horizontally)
   14  //  * (x != 0, 0)                - wrap text so that it does not reach beyond x. Will automatically calculate a vertical size (expand vertically).
   15  //  * (x != 0, y <= fontHeight)  - will truncate text so it fits within this box.
   16  class TextComponent : public GuiComponent
   17  {
   18  public:
   19  	TextComponent(Window* window);
   20  	TextComponent(Window* window, const std::string& text, const std::shared_ptr<Font>& font, unsigned int color = 0x000000FF, Alignment align = ALIGN_LEFT,
   21  		Vector3f pos = Vector3f::Zero(), Vector2f size = Vector2f::Zero(), unsigned int bgcolor = 0x00000000);
   22  
   23  	std::string getThemeTypeName() override { return "text"; }
   24  
   25  	void setFont(const std::shared_ptr<Font>& font);
   26  	void setFont(std::string path, int size);
   27  	void setUppercase(bool uppercase);
   28  	void onSizeChanged() override;
   29  	const std::string getText() { return mText; }
   30  	void setText(const std::string& text);
   31  	void setColor(unsigned int color);
   32  	void setHorizontalAlignment(Alignment align);
   33  	void setVerticalAlignment(Alignment align);
   34  	void setLineSpacing(float spacing);
   35  	void setBackgroundColor(unsigned int color);
   36  	void setRenderBackground(bool render);
   37  
   38  	void update(int deltaTime) override;
   39  	void render(const Transform4x4f& parentTrans) override;
   40  
   41  	std::string getValue() const override;
   42  	void setValue(const std::string& value) override;
   43  	
   44  	void onOpacityChanged() override;
   45  	void onPaddingChanged() override;
   46  
   47  	inline std::shared_ptr<Font> getFont() const { return mFont; }
   48  	inline float getLineSpacing() const { return mLineSpacing; }
   49  	inline Alignment getHorizontalAlignment() const { return mHorizontalAlignment; }
   50  
   51  	virtual void applyTheme(const std::shared_ptr<ThemeData>& theme, const std::string& view, const std::string& element, unsigned int properties) override;
   52  
   53  	void setGlowColor(unsigned int color) { mGlowColor = color; };
   54  	void setGlowSize(unsigned int size) { mGlowSize = size; };
   55  	void setGlowOffset(float x, float y) { mGlowOffset = Vector2f(x,y); };
   56  
   57  	enum AutoScrollType : unsigned int
   58  	{
   59  		NONE = 0,
   60  		HORIZONTAL = 1,
   61  		VERTICAL = 2
   62  	};
   63  
   64  	AutoScrollType getAutoScroll() { return mAutoScroll; }
   65  	void setAutoScroll(AutoScrollType value);
   66  	void setAutoScroll(bool scroll);
   67  
   68  	unsigned int getColor() { return mColor; }
   69  
   70  	std::string getOriginalThemeText() { return mSourceText; }
   71  
   72  	ThemeData::ThemeElement::Property getProperty(const std::string name) override;
   73  	void setProperty(const std::string name, const ThemeData::ThemeElement::Property& value) override;
   74  
   75  	virtual void onShow() override;
   76  
   77  	enum MultiLineType : unsigned int
   78  	{
   79  		AUTO = 0,
   80  		MULTILINE = 1,
   81  		SINGLELINE = 2
   82  	};
   83  
   84  	MultiLineType getMultiLine() { return mMultiline; }
   85  	void setMultiLine(MultiLineType value);
   86  
   87  	bool getBindingDefaults() { return mBindingDefaults; }
   88  
   89  	void setBonusTextColor(unsigned int color);
   90  
   91  protected:
   92  	void buildTextCache();
   93  	virtual void onTextChanged();
   94  
   95  	std::string mText;
   96  	std::shared_ptr<Font> mFont;
   97  	std::string mSourceText;
   98  
   99  	bool		mBindingDefaults;
  100  
  101  	Vector2i mAutoCalcExtent;
  102  
  103  private:	
  104  	void onColorChanged();
  105  
  106  	unsigned int mColor;
  107  	unsigned int mBgColor;
  108  
  109  	bool mRenderBackground;
  110  	
  111  	bool mUppercase;
  112  	
  113  	std::shared_ptr<TextCache> mTextCache;
  114  	Alignment mHorizontalAlignment;
  115  	Alignment mVerticalAlignment;
  116  	float mLineSpacing;
  117  
  118  	unsigned int mGlowColor;
  119  	unsigned int mGlowSize;
  120  	Vector2f	 mGlowOffset;
  121  	
  122  	Vector2f	mReflection;
  123  	bool		mReflectOnBorders;
  124  
  125  	int mMarqueeOffset;
  126  	int mMarqueeOffset2;
  127  	int mMarqueeTime;
  128  
  129  	int mTextLength;
  130  
  131  	int mAutoScrollDelay;
  132  	int mAutoScrollSpeed;
  133  
  134  	unsigned int mBonusColor;
  135  	bool mHasBonusColor;
  136  
  137  	AutoScrollType mAutoScroll;
  138  	MultiLineType  mMultiline;
  139  };
  140  
  141  #endif // ES_CORE_COMPONENTS_TEXT_COMPONENT_H
```

## TextEditComponent.cpp `:1-17` (an excerpt, upstream-carried, at the pin)

```text
    1  #include "components/TextEditComponent.h"
    2  
    3  #include "resources/Font.h"
    4  #include "utils/StringUtil.h"
    5  #include "LocaleES.h"
    6  #include "Window.h"
    7  
    8  #define TEXT_PADDING_HORIZ 10
    9  #define TEXT_PADDING_VERT 2
   10  
   11  #define CURSOR_REPEAT_START_DELAY 500
   12  #define CURSOR_REPEAT_SPEED 28 // lower is faster
   13  
   14  #define BLINKTIME	1000
   15  
   16  TextEditComponent::TextEditComponent(Window* window) : GuiComponent(window),
   17  	mBox(window, ":/textinput_ninepatch.png"), mFocused(false), 
```

## TextEditComponent.cpp `:23-61` (an excerpt, upstream-carried, at the pin)

```text
   23  
   24  	auto theme = ThemeData::getMenuTheme();
   25  	mBox.setImagePath(ThemeData::getMenuTheme()->Icons.textinput_ninepatch);
   26  
   27  	addChild(&mBox);
   28  	
   29  	onFocusLost();
   30  
   31  	setSize(4096, mFont->getHeight() + TEXT_PADDING_VERT);
   32  }
   33  
   34  void TextEditComponent::onFocusGained()
   35  {
   36  	mFocused = true;
   37  	mBox.setImagePath(ThemeData::getMenuTheme()->Icons.textinput_ninepatch_active);	
   38  
   39  	mWindow->postToUiThread([this]() { startEditing(); });
   40  }
   41  
   42  void TextEditComponent::onFocusLost()
   43  {
   44  	mFocused = false;
   45  	mBox.setImagePath(ThemeData::getMenuTheme()->Icons.textinput_ninepatch);
   46  	
   47  	mWindow->postToUiThread([this]() { stopEditing(); });
   48  }
   49  
   50  void TextEditComponent::onSizeChanged()
   51  {
   52  	GuiComponent::onSizeChanged();
   53  	mBox.fitTo(mSize, Vector3f::Zero(), Vector2f(-34, -32 - TEXT_PADDING_VERT));
   54  	onTextChanged(); // wrap point probably changed
   55  }
   56  
   57  void TextEditComponent::setValue(const std::string& val)
   58  {
   59  	mText = val;
   60  	onTextChanged();
   61  }
```

## TextEditComponent.cpp `:132-148` (an excerpt, upstream-carried, at the pin)

```text
  132  		return;
  133  
  134  	SDL_StopTextInput();
  135  	mEditing = false;
  136  	mDeferTextInputStart = false;
  137  	updateHelpPrompts();
  138  }
  139  
  140  bool TextEditComponent::input(InputConfig* config, Input input)
  141  {	
  142  	bool const cursor_left = (config->getDeviceId() != DEVICE_KEYBOARD && config->isMappedLike("left", input)) ||
  143  		(config->getDeviceId() == DEVICE_KEYBOARD && input.id == SDLK_LEFT);
  144  	bool const cursor_right = (config->getDeviceId() != DEVICE_KEYBOARD && config->isMappedLike("right", input)) ||
  145  		(config->getDeviceId() == DEVICE_KEYBOARD && input.id == SDLK_RIGHT);
  146  
  147  	if(input.value == 0)
  148  	{
```

## TextEditComponent.cpp `:259-279` (an excerpt, upstream-carried, at the pin)

```text
  259  	mCursorRepeatTimer += deltaTime;
  260  	while(mCursorRepeatTimer >= CURSOR_REPEAT_SPEED)
  261  	{
  262  		moveCursor(mCursorRepeatDir);
  263  		mCursorRepeatTimer -= CURSOR_REPEAT_SPEED;
  264  	}
  265  }
  266  
  267  void TextEditComponent::moveCursor(int amt)
  268  {
  269  	mCursor = (unsigned int)Utils::String::moveCursor(mText, mCursor, amt);
  270  	onCursorChanged();
  271  }
  272  
  273  void TextEditComponent::setCursor(size_t pos)
  274  {
  275  	if(pos == std::string::npos)
  276  		mCursor = (unsigned int)mText.length();
  277  	else
  278  		mCursor = (int)pos;
  279  
```

## TextEditComponent.cpp `:290-308` (an excerpt, upstream-carried, at the pin)

```text
  290  }
  291  
  292  void TextEditComponent::onCursorChanged()
  293  {
  294  	if(isMultiline())
  295  	{
  296  		Vector2f textSize = mFont->getWrappedTextCursorOffset(mText, getTextAreaSize().x(), mCursor); 
  297  
  298  		if(mScrollOffset.y() + getTextAreaSize().y() < textSize.y() + mFont->getHeight()) //need to scroll down?
  299  		{
  300  			mScrollOffset[1] = textSize.y() - getTextAreaSize().y() + mFont->getHeight();
  301  		}else if(mScrollOffset.y() > textSize.y()) //need to scroll up?
  302  		{
  303  			mScrollOffset[1] = textSize.y();
  304  		}
  305  	}else{
  306  		Vector2f cursorPos = mFont->sizeText(mText.substr(0, mCursor));
  307  
  308  		if(mScrollOffset.x() + getTextAreaSize().x() < cursorPos.x())
```

## TextEditComponent.cpp `:356-400` (an excerpt, upstream-carried, at the pin)

```text
  356  		else
  357  		{
  358  			cursorPos = mFont->sizeText(mText.substr(0, mCursor));
  359  			cursorPos[1] = 0;
  360  		}
  361  
  362  		if (!mEditing || mBlinkTime < BLINKTIME / 2 || mCursorRepeatDir != 0)
  363  		{
  364  			float cursorHeight = mFont->getHeight() * 0.8f;
  365  
  366  			auto cursorColor = (ThemeData::getMenuTheme()->Text.color & 0xFFFFFF00) | getOpacity();
  367  			if (!mEditing)
  368  				cursorColor = (ThemeData::getMenuTheme()->Text.color & 0xFFFFFF00) | (unsigned char) (getOpacity() * 0.25f);
  369  
  370  			Renderer::drawRect(cursorPos.x(), cursorPos.y() + (mFont->getHeight() - cursorHeight) / 2, 2.0f, cursorHeight, cursorColor, cursorColor); // 0x000000FF
  371  		}
  372  	}
  373  }
  374  
  375  bool TextEditComponent::isMultiline()
  376  {
  377  	return (getSize().y() > mFont->getHeight() * 1.25f);
  378  }
  379  
  380  Vector2f TextEditComponent::getTextAreaPos() const
  381  {
  382  	return Vector2f(TEXT_PADDING_HORIZ / 2.0f, TEXT_PADDING_VERT / 2.0f);
  383  }
  384  
  385  Vector2f TextEditComponent::getTextAreaSize() const
  386  {
  387  	return Vector2f(mSize.x() - TEXT_PADDING_HORIZ, mSize.y() - TEXT_PADDING_VERT);
  388  }
  389  
  390  std::vector<HelpPrompt> TextEditComponent::getHelpPrompts()
  391  {
  392  	std::vector<HelpPrompt> prompts;
  393  	
  394  	if(mEditing)
  395  		prompts.push_back(HelpPrompt("up/down/left/right", _("MOVE CURSOR")));
  396  	else
  397  		prompts.push_back(HelpPrompt(BUTTON_OK, _("EDIT")));
  398  	
  399  	return prompts;
  400  }
```

## TextListComponent.h `:254-277` (an excerpt, upstream-carried, at the pin)

```text
  254  	if (Settings::DebugMouse() && mIsMouseOver)
  255  	{
  256  		Renderer::setMatrix(trans);
  257  		Renderer::drawRect(0.0f, 0.0f, mSize.x(), mSize.y(), 0xFF000033, 0xFF000033);
  258  	}
  259  
  260  	float opacity = getOpacity() / 255.0;
  261  	
  262  	float entrySize = getRowHeight();
  263  	int startEntry = mCameraOffset / entrySize;
  264  	int screenCount = mLineCount > 0 ? mLineCount : (int)(mSize.y() / entrySize);
  265  	int lastEntry = Math::min((int) mEntries.size(), startEntry + screenCount + 1);
  266  	
  267  	int listCutoff = startEntry + screenCount;
  268  	if (listCutoff > size())
  269  		listCutoff = size();
  270  
  271  	int loopStart = startEntry;
  272  	int loopEnd = lastEntry;
  273  
  274  	if (!mItemTemplate.type.empty())
  275  	{
  276  		startEntry = Math::max(0, startEntry - 2);
  277  		lastEntry = Math::min((int) mEntries.size(), lastEntry + 2);
```

## TextListComponent.h `:450-466` (an excerpt, upstream-carried, at the pin)

```text
  450  		mScrollbar.setContainerBounds(GuiComponent::getPosition(), GuiComponent::getSize());
  451  		mScrollbar.setRange(0, entrySize * mEntries.size(), mSize.y());
  452  		mScrollbar.setScrollPosition(startEntry * entrySize);
  453  		mScrollbar.render(parentTrans);
  454  	}
  455  }
  456  
  457  template <typename T>
  458  bool TextListComponent<T>::input(InputConfig* config, Input input)
  459  {
  460  	if (size() > 0)
  461  	{
  462  		if (input.value != 0)
  463  		{
  464  			if (config->isMappedLike("down", input))
  465  			{
  466  				listInput(1);
```

## TextListComponent.h `:583-621` (an excerpt, upstream-carried, at the pin)

```text
  583  template <typename T>
  584  void TextListComponent<T>::onSizeChanged()
  585  {
  586  	IList<TextListData, T>::onSizeChanged();
  587  	updateCameraOffset();
  588  }
  589  
  590  template <typename T>
  591  void TextListComponent<T>::updateCameraOffset()
  592  {
  593  	auto rowHeight = getRowHeight();
  594  	auto totalHeight = rowHeight * mEntries.size();
  595  
  596  	// move the camera to scroll
  597  	if (totalHeight > mSize.y() && mCursor < mEntries.size())
  598  	{
  599  		mCameraOffset = (rowHeight * mCursor) + ((rowHeight - mSize.y()) / 2.0f);
  600  
  601  		if (mCameraOffset < 0)
  602  			mCameraOffset = 0;
  603  		else if (mCameraOffset + mSize.y() > totalHeight)
  604  			mCameraOffset = totalHeight - mSize.y();
  605  	}
  606  	else
  607  		mCameraOffset = 0;
  608  }
  609  
  610  template <typename T>
  611  float TextListComponent<T>::getRowHeight() const
  612  {
  613  	return mLineCount > 0 ? (mSize.y() / (float) mLineCount) : (Math::max(mFont->getHeight(1.0), (float)mFont->getSize()) * mLineSpacing);
  614  }
  615  
  616  template <typename T>
  617  float TextListComponent<T>::getTotalRowHeight() const
  618  {
  619  	return getRowHeight() * mEntries.size();
  620  }
  621  
```

## TextListComponent.h `:717-733` (an excerpt, upstream-carried, at the pin)

```text
  717  		if (elem->has("glowSize"))
  718  			mGlowSize = (int)elem->get<float>("glowSize");
  719  
  720  		if (elem->has("glowOffset"))
  721  			mGlowOffset = elem->get<Vector2f>("glowOffset");
  722  	}
  723  
  724  	setFont(Font::getFromTheme(elem, properties, mFont));
  725  	const float selectorHeight = Math::max(mFont->getHeight(1.0), (float)mFont->getSize()) * mLineSpacing;
  726  	setSelectorHeight(selectorHeight);
  727  
  728  	if (properties & SOUND && elem->has("scrollSound"))
  729  		mScrollSound = elem->get<std::string>("scrollSound");
  730  
  731  	if (properties & ALIGNMENT)
  732  	{
  733  		if (elem->has("alignment"))
```

## VideoComponent.cpp `:14-30` (an excerpt, upstream-carried, at the pin)

```text
   14  std::string getTitlePath() 
   15  {
   16  	std::string titleFolder = getTitleFolder();
   17  	return titleFolder + "subtitle.srt";
   18  }
   19  
   20  std::string getTitleFolder() 
   21  {
   22  #if WIN32
   23  	return Utils::FileSystem::getGenericPath(Paths::getUserEmulationStationPath() + "/tmp/");
   24  #endif
   25  
   26  	return "/tmp/";
   27  }
   28  
   29  void writeSubtitle(const char* gameName, const char* systemName, bool always)
   30  {
```

## VideoComponent.cpp `:319-359` (an excerpt, upstream-carried, at the pin)

```text
  319  	{
  320  		if (elem->has("default"))
  321  			mConfig.defaultVideoPath = elem->get<std::string>("default");
  322  
  323  		if (elem->has("path"))
  324  		{
  325  			auto path = elem->get<std::string>("path");
  326  
  327  			if (path[0] == '{' || Utils::FileSystem::exists(path))
  328  				mVideoPath = path;
  329  			else
  330  				mVideoPath = mConfig.defaultVideoPath;
  331  
  332  			mThemedPath = mVideoPath;
  333  		}
  334  		else if (!mConfig.defaultVideoPath.empty())
  335  		{
  336  			mVideoPath = mConfig.defaultVideoPath;
  337  			mThemedPath = mVideoPath;
  338  		}
  339  	}
  340  
  341  	if (elem->has("defaultSnapshot"))
  342  		mStaticImage.setDefaultImage(elem->get<std::string>("defaultSnapshot"));
  343  
  344  	mStaticImage.applyStoryboard(elem, "snapshot");
  345  }
  346  
  347  std::vector<HelpPrompt> VideoComponent::getHelpPrompts()
  348  {
  349  	std::vector<HelpPrompt> ret;
  350  	ret.push_back(HelpPrompt(BUTTON_BACK, _("SELECT")));
  351  	return ret;
  352  }
  353  
  354  void VideoComponent::handleStartDelay()
  355  {
  356  	// Only play if any delay has timed out
  357  	if (!mStartDelayed || mIsWaitingForVideoToStart)
  358  		return;
  359  
```

## VideoComponent.cpp `:583-599` (an excerpt, upstream-carried, at the pin)

```text
  583  	if (hasStoryBoard() && !mStaticImage.hasStoryBoard("snapshot"))
  584  	{
  585  		if (name == "offset" || name == "offsetX" || name == "offsetY" || name == "scale")
  586  			mStaticImage.setProperty(name, value);
  587  	}
  588  
  589  	if (value.type == ThemeData::ThemeElement::Property::PropertyType::String && name == "path")
  590  	{
  591  		if (Utils::FileSystem::exists(value.s))
  592  			setVideo(value.s, false);
  593  		else
  594  			setVideo(mConfig.defaultVideoPath);		
  595  
  596  		mThemedPath = mVideoPath;
  597  	}
  598  	else if (value.type == ThemeData::ThemeElement::Property::PropertyType::Bool && name == "enabled")
  599  	{
```

## VideoPlayerComponent.cpp `:1-9` (an excerpt, upstream-carried, at the pin)

```text
    1  #ifdef _RPI_
    2  #include "components/VideoPlayerComponent.h"
    3  
    4  #include "renderers/Renderer.h"
    5  #include "utils/StringUtil.h"
    6  #include "AudioManager.h"
    7  #include "Settings.h"
    8  #include "math/Misc.h"
    9  #include <fcntl.h>
```

## VideoPlayerComponent.h `:1-9` (an excerpt, upstream-carried, at the pin)

```text
    1  #ifdef _RPI_
    2  #pragma once
    3  #ifndef ES_CORE_COMPONENTS_VIDEO_PLAYER_COMPONENT_H
    4  #define ES_CORE_COMPONENTS_VIDEO_PLAYER_COMPONENT_H
    5  
    6  #include "components/VideoComponent.h"
    7  
    8  void catch_child(int sig_num);
    9  
```

## VideoVlcComponent.cpp `:1-104` (an excerpt, upstream-carried, at the pin)

```text
    1  #include "components/VideoVlcComponent.h"
    2  
    3  #include "renderers/Renderer.h"
    4  #include "resources/TextureResource.h"
    5  #include "utils/StringUtil.h"
    6  #include "PowerSaver.h"
    7  #include "Settings.h"
    8  #include <vlc/vlc.h>
    9  #include <vlc/libvlc_version.h>
   10  #include <SDL_mutex.h>
   11  #include <cmath>
   12  #include "SystemConf.h"
   13  #include "ThemeData.h"
   14  #include <SDL_timer.h>
   15  #include "AudioManager.h"
   16  
   17  #ifdef WIN32
   18  #include <codecvt>
   19  #endif
   20  
   21  #include "ImageIO.h"
   22  
   23  #define MATHPI          3.141592653589793238462643383279502884L
   24  
   25  libvlc_instance_t* VideoVlcComponent::mVLC = NULL;
   26  
   27  // VLC prepares to render a video frame.
   28  static void *lock(void *data, void **p_pixels) 
   29  {
   30  	struct VideoContext *c = (struct VideoContext *)data;
   31  
   32  	int frame = (c->surfaceId ^ 1);
   33  	
   34  	c->mutexes[frame].lock();
   35  	c->hasFrame[frame] = false;
   36  	*p_pixels = c->surfaces[frame];
   37  	return NULL; // Picture identifier, not needed here.
   38  }
   39  
   40  // VLC just rendered a video frame.
   41  static void unlock(void *data, void* /*id*/, void *const* /*p_pixels*/) 
   42  {
   43  	struct VideoContext *c = (struct VideoContext *)data;
   44  
   45  	int frame = (c->surfaceId ^ 1);	
   46  
   47  	c->surfaceId = frame;
   48  	c->hasFrame[frame] = true;
   49  	c->mutexes[frame].unlock();
   50  }
   51  
   52  // VLC wants to display a video frame.
   53  static void display(void* data, void* id)
   54  {
   55  	if (data == NULL)
   56  		return;
   57  
   58  	struct VideoContext *c = (struct VideoContext *)data;
   59  	if (c->component != nullptr && !c->component->isPlaying() && c->component->isWaitingForVideoToStart())
   60  		c->component->onVideoStarted();
   61  }
   62  
   63  VideoVlcComponent::VideoVlcComponent(Window* window) : VideoComponent(window), 
   64  	mMediaPlayer(nullptr), mMedia(nullptr),
   65  	mTopLeftCrop(0.0f, 0.0f), mBottomRightCrop(1.0f, 1.0f), mContext(nullptr)
   66  {
   67  	mIsParsing = false;
   68  	mSaturation = 1.0f;
   69  	mElapsed = 0;
   70  	mColorShift = 0xFFFFFFFF;
   71  	mLinearSmooth = false;
   72  
   73  	mLoops = -1;
   74  	mCurrentLoop = 0;
   75  
   76  	// Get an empty texture for rendering the video
   77  	mTexture = nullptr;// TextureResource::get("");
   78  	mEffect = VideoVlcFlags::VideoVlcEffect::BUMP;
   79  
   80  	// Make sure VLC has been initialised
   81  	init();
   82  }
   83  
   84  static void mediaplayer_release_async(VideoContext* ctx, libvlc_media_player_t* p_mi)
   85  {
   86  	if (p_mi == nullptr)
   87  		return;
   88  
   89  	ctx->component = nullptr;
   90  
   91  	std::thread([p_mi, ctx]()
   92  		{			
   93  			libvlc_media_player_release(p_mi);
   94  			if (ctx) delete ctx;
   95  		}).detach();
   96  }
   97  
   98  VideoVlcComponent::~VideoVlcComponent()
   99  {
  100  	stopVideo();
  101  }
  102  
  103  Vector2f VideoVlcComponent::getSize() const
  104  {
```

## VideoVlcComponent.cpp `:471-502` (an excerpt, upstream-carried, at the pin)

```text
  471  	// Build a texture for the video frame
  472  	if (initFromPixels)
  473  	{		
  474  		int frame = mContext->surfaceId;
  475  		if (mContext->hasFrame[frame])
  476  		{
  477  			if (mTexture == nullptr)
  478  			{
  479  				mTexture = TextureResource::get("", false, mLinearSmooth);
  480  
  481  				resize();
  482  				trans = parentTrans * getTransform();
  483  			}
  484  
  485  #ifdef _RPI_
  486  			// Rpi : A lot of videos are encoded in 60fps on screenscraper
  487  			// Try to limit transfert to opengl textures to 30fps to save CPU
  488  			if (!Settings::getInstance()->getBool("OptimizeVideo") || mElapsed >= 40) // 40ms = 25fps, 33.33 = 30 fps
  489  #endif
  490  			{
  491  				mContext->mutexes[frame].lock();
  492  				mTexture->updateFromExternalPixels(mContext->surfaces[frame], mVideoWidth, mVideoHeight);
  493  				mContext->hasFrame[frame] = false;
  494  				mContext->mutexes[frame].unlock();
  495  
  496  				mElapsed = 0;
  497  			}
  498  		}
  499  	}
  500  
  501  	if (mTexture == nullptr)
  502  		return;
```

## VideoVlcComponent.cpp `:584-613` (an excerpt, upstream-carried, at the pin)

```text
  584  	ctx->hasFrame[1] = false;
  585  	ctx->component = this;
  586  
  587  	resize();	
  588  
  589  	return ctx;
  590  }
  591  
  592  #if WIN32
  593  #include <Windows.h>
  594  #pragma comment(lib, "Version.lib")
  595  
  596  // If Vlc2 dlls have been upgraded with vlc3 dlls, libqt4_plugin.dll is not compatible, so check if libvlc is 3.x then delete obsolete libqt4_plugin.dll
  597  void _checkUpgradedVlcVersion()
  598  {
  599  	char str[1024] = { 0 };
  600  	if (GetModuleFileNameA(NULL, str, 1024) == 0)
  601  		return;
  602  
  603  	auto dir = Utils::FileSystem::getParent(str);
  604  	auto path = Utils::FileSystem::getPreferredPath(Utils::FileSystem::combine(dir, "libvlc.dll"));
  605  	if (Utils::FileSystem::exists(path))
  606  	{
  607  		// Get the version information for the file requested
  608  		DWORD dwSize = GetFileVersionInfoSize(path.c_str(), NULL);
  609  		if (dwSize == 0)
  610  		{
  611  			printf("Error in GetFileVersionInfoSize: %d\n", GetLastError());
  612  			return;
  613  		}
```

## VideoVlcComponent.cpp `:631-647` (an excerpt, upstream-carried, at the pin)

```text
  631  			delete[] pbVersionInfo;
  632  			return;
  633  		}
  634  
  635  		// FileVersion for libvlc.dll is >= 3.x.x.x ???
  636  		if (HIWORD(pFileInfo->dwFileVersionMS) >= 3)
  637  		{
  638  			auto badV2PluginPath = Utils::FileSystem::getPreferredPath(Utils::FileSystem::combine(dir, "plugins/gui/libqt4_plugin.dll"));
  639  			if (Utils::FileSystem::exists(badV2PluginPath))
  640  				Utils::FileSystem::removeFile(badV2PluginPath);
  641  		}
  642  	}
  643  }
  644  #endif
  645  
  646  void VideoVlcComponent::init()
  647  {
```

## VideoVlcComponent.cpp `:660-676` (an excerpt, upstream-carried, at the pin)

```text
  660  			cmdline.push_back(token);
  661  	}
  662  
  663  	const char* *theArgs = new const char*[cmdline.size()];
  664  
  665  	for (int i = 0 ; i < cmdline.size() ; i++)
  666  		theArgs[i] = cmdline[i].c_str();
  667  
  668  #if WIN32
  669  	_checkUpgradedVlcVersion();
  670  #endif
  671  
  672  	mVLC = libvlc_new(cmdline.size(), theArgs);
  673  
  674  	delete[] theArgs;
  675  }
  676  
```

## VideoVlcComponent.cpp `:771-790` (an excerpt, upstream-carried, at the pin)

```text
  771  	if (mVideoWidth <= 0 || mVideoHeight <= 0)
  772  		return;
  773  
  774  	if (mVideoWidth > 1 && Settings::getInstance()->getBool("OptimizeVideo"))
  775  	{
  776  		// Avoid videos bigger than resolution
  777  		Vector2f maxSize(Renderer::getScreenWidth(), Renderer::getScreenHeight());
  778  
  779  #ifdef _RPI_
  780  		// Temporary -> RPI -> Try to limit videos to 400x300 for performance benchmark
  781  		if (!Renderer::isSmallScreen())
  782  			maxSize = Vector2f(400, 300);
  783  #endif
  784  
  785  		if (!mTargetSize.empty() && (mTargetSize.x() < maxSize.x() || mTargetSize.y() < maxSize.y()))
  786  			maxSize = mTargetSize;
  787  
  788  		// If video is bigger than display, ask VLC for a smaller image
  789  		auto sz = ImageIO::adjustPictureSize(Vector2i(mVideoWidth, mVideoHeight), Vector2i(maxSize.x(), maxSize.y()), mTargetIsMin);
  790  		if (sz.x() < mVideoWidth || sz.y() < mVideoHeight)
```

## VideoVlcComponent.cpp `:828-844` (an excerpt, upstream-carried, at the pin)

```text
  828  	if (mVideoPath.empty())
  829  	{
  830  		stopVideo();
  831  		return;
  832  	}
  833  
  834  	StopWatch stopWatch("[VideoVlcComponent] startVideo", LogDebug);
  835  
  836  #ifdef WIN32
  837  	std::string path = Utils::String::replace(mVideoPath, "/", "\\");
  838  #else
  839  	std::string path = mVideoPath;
  840  #endif
  841  
  842  	mMedia = libvlc_media_new_path(mVLC, path.c_str());
  843  	if (!mMedia)
  844  	{
```

## VideoVlcComponent.cpp `:851-883` (an excerpt, upstream-carried, at the pin)

```text
  851  
  852  	mTexture = nullptr;
  853  	mCurrentLoop = 0;
  854  	mIsParsing = false;
  855  	mPlayingVideoPath = mVideoPath;
  856  
  857  	PowerSaver::pause();
  858  
  859  	// use : vlc long-help
  860  	// WIN32 ? libvlc_media_add_option(mMedia, ":avcodec-hw=dxva2");
  861  	// RPI/OMX ? libvlc_media_add_option(mMedia, ":codec=mediacodec,iomx,all"); .
  862  
  863  	std::string options = SystemConf::getInstance()->get("vlc.options");
  864  	if (!options.empty())
  865  	{
  866  		for (auto token : Utils::String::split(options, ' '))
  867  			libvlc_media_add_option(mMedia, token.c_str());
  868  	}
  869  
  870  	// If we have a playlist : most videos have a fader, skip it 1 second
  871  	if (mPlaylist != nullptr && mConfig.startDelay == 0 && !mConfig.showSnapshotDelay && !mConfig.showSnapshotNoVideo)
  872  		libvlc_media_add_option(mMedia, ":start-time=0.7");
  873  
  874  #if LIBVLC_VERSION_MAJOR >= 3
  875  	#if WIN32
  876  		const char* vlc_ver = libvlc_get_version();
  877  		if (vlc_ver[0] < '3')
  878  			libvlc_media_parse(mMedia);
  879  		else
  880  	#endif
  881  	{
  882  		libvlc_media_parse_with_options(mMedia, libvlc_media_parse_local, 0);
  883  		if ((int)libvlc_media_get_parsed_status(mMedia) == 0)
```

## VideoVlcComponent.cpp `:903-919` (an excerpt, upstream-carried, at the pin)

```text
  903  
  904  	mIsPlaying = false;
  905  	mIsWaitingForVideoToStart = false;
  906  	mStartDelayed = false;
  907  
  908  	// Release the media player so it stops calling back to us
  909  	if (mMediaPlayer)
  910  	{
  911  		mediaplayer_release_async(mContext, mMediaPlayer);
  912  		mMediaPlayer = nullptr;		
  913  	}
  914  	else if (mContext)
  915  		delete mContext;
  916  
  917  	mContext = nullptr;
  918  
  919  	// Release the media
```

## VolumeInfoComponent.cpp `:37-53` (an excerpt, upstream-carried, at the pin)

```text
   37  	setSize(fullSize);
   38  
   39  	mFrame = new NinePatchComponent(window);
   40  	mFrame->setImagePath(theme->Background.path);
   41  	mFrame->setEdgeColor(theme->Background.color);
   42  	mFrame->setCenterColor(theme->Background.centerColor);
   43  	mFrame->setCornerSize(theme->Background.cornerSize);
   44  	mFrame->setPostProcessShader(theme->Background.menuShader, false);
   45  	mFrame->fitTo(mSize, Vector3f::Zero(), Vector2f(-32, -32));
   46  	addChild(mFrame);
   47  
   48  	mLabel = new TextComponent(mWindow, "", font, theme->Text.color, ALIGN_CENTER);
   49  	
   50  	int h = font->sizeText("100%").y() + PADDING_PX;
   51  	mLabel->setPosition(0, fullSize.y() - h);
   52  	mLabel->setSize(fullSize.x(), h);
   53  	addChild(mLabel);
```

## WebImageComponent.cpp (whole, fork-modified, at the pin)

```text
    1  #include "WebImageComponent.h"
    2  #include "utils/StringUtil.h"
    3  #include "HttpReq.h"
    4  #include "utils/ZipFile.h"
    5  #include "resources/TextureResource.h"
    6  #include "Paths.h"
    7  #include "utils/OfflineProxyUrl.h"
    8  
    9  #include <algorithm>
   10  #include <cctype>
   11  #include <functional>
   12  
   13  struct url
   14  {
   15  public:
   16  	static url parse(const std::string& url_s)
   17  	{
   18  		url ret;
   19  
   20  		using namespace std;
   21  
   22  		const std::string prot_end("://");
   23  		std::string::const_iterator prot_i = search(url_s.begin(), url_s.end(), prot_end.begin(), prot_end.end());
   24  		ret.protocol.reserve(distance(url_s.begin(), prot_i));
   25  		std::transform(url_s.begin(), prot_i, std::back_inserter(ret.protocol), [](unsigned char c) { return std::tolower(c); });
   26  		if (prot_i == url_s.end())
   27  			return ret;
   28  
   29  		advance(prot_i, prot_end.length());
   30  		string::const_iterator path_i = find(prot_i, url_s.end(), '/');
   31  		ret.host.reserve(distance(prot_i, path_i));
   32  		std::transform(prot_i, path_i, std::back_inserter(ret.host), [](unsigned char c) { return std::tolower(c); }); // host is icase
   33  		string::const_iterator query_i = find(path_i, url_s.end(), '?');
   34  		ret.path.assign(path_i, query_i);
   35  		if (query_i != url_s.end())
   36  			++query_i;
   37  		ret.query.assign(query_i, url_s.end());
   38  		return ret;
   39  	}
   40  
   41  	std::string protocol, host, path, query;
   42  };
   43  
   44  // keepInCacheDuration = 0 -> image expire immediately
   45  // keepInCacheDuration = -1 -> image expire never
   46  // keepInCacheDuration = 600 -> image expire in 10 minutes ( 60*10 )
   47  // keepInCacheDuration = 86400 -> image expire in 24 hours ( 60*60*10 )
   48  
   49  WebImageComponent::WebImageComponent(Window* window, double keepInCacheDuration) : ImageComponent(window, false), 
   50  	mRequest(nullptr), mKeepInCacheDuration(keepInCacheDuration), mMaxSize(MaxSizeInfo::Empty),
   51  	mBusyAnim(nullptr)
   52  {
   53  	mWaitLoaded = false;
   54  	mOnLoaded = nullptr;
   55  }
   56  
   57  void WebImageComponent::resize()
   58  {
   59  	ImageComponent::resize();
   60  	
   61  	if (mBusyAnim != nullptr)
   62  	{
   63  		if (mSize.x() == 0)
   64  			mBusyAnim->setSize(mTargetSize);
   65  		else
   66  			mBusyAnim->setSize(mSize);
   67  	}
   68  
   69  	if (getParent() != nullptr && getParent()->isKindOf<ComponentGrid>())
   70  		getParent()->onSizeChanged();
   71  }
   72  
   73  WebImageComponent::~WebImageComponent()
   74  {
   75  	if (mRequest != nullptr)
   76  		delete mRequest;
   77  
   78  	if (mBusyAnim != nullptr)
   79  		delete mBusyAnim;
   80  	
   81  	if (mKeepInCacheDuration == 0 && Utils::FileSystem::exists(mLocalFile))
   82  	{
   83  		Utils::FileSystem::removeFile(mLocalFile);
   84  
   85  		auto root = Utils::FileSystem::getGenericPath(Paths::getUserEmulationStationPath() + "/tmp");
   86  		auto file = Utils::FileSystem::getParent(Utils::FileSystem::getGenericPath(mLocalFile));
   87  
   88  		while (!file.empty() && file != root && file != mLocalFile)
   89  		{
   90  			Utils::FileSystem::removeFile(file);
   91  			file = Utils::FileSystem::getParent(file);
   92  		}
   93  	}
   94  }
   95  
   96  void WebImageComponent::setImage(const std::string& path, bool tile, const MaxSizeInfo& maxSize, bool checkFileExists, bool allowMultiImagePlaylist)
   97  {
   98  	if (mRequest != nullptr)
   99  	{
  100  		delete mRequest;
  101  		mRequest = nullptr;
  102  	}
  103  
  104  	mWaitLoaded = true;
  105  
  106  	if (!Utils::String::startsWith(path, "http://") && !Utils::String::startsWith(path, "https://"))
  107  	{
  108  		if (path.empty())
  109  			ImageComponent::setImage(nullptr, 0);
  110  		else
  111  		{
  112  			ImageComponent::setImage(path, tile, maxSize, checkFileExists, allowMultiImagePlaylist);
  113  			resize();
  114  		}
  115  		return;
  116  	}
  117  
  118  	url uri = url::parse(path);
  119  	if (uri.host.empty() || uri.path.empty())
  120  		return;
  121  
  122  	if (Utils::String::startsWith(uri.path, "/"))
  123  		uri.path = uri.path.substr(1);
  124  
  125  	std::string queryCrc;
  126  
  127  	if (!uri.query.empty())
  128  	{
  129  		auto file_crc32 = Utils::Zip::ZipFile::computeCRC(0, uri.query.data(), uri.query.size());
  130  		queryCrc = "-" + Utils::String::toHexString(file_crc32);
  131  	}
  132  
  133  	std::string localFile = Paths::getUserEmulationStationPath() + "/tmp/" + uri.host + "/" + uri.path + queryCrc;	
  134  	if (Utils::FileSystem::exists(localFile))
  135  	{
  136  		bool keepLoadingLocal = true;
  137  
  138  		if (mKeepInCacheDuration == 0)
  139  		{
  140  			keepLoadingLocal = false;
  141  			Utils::FileSystem::removeFile(localFile);
  142  		}
  143  		else if (mKeepInCacheDuration > 0)
  144  		{
  145  			auto date = Utils::FileSystem::getFileCreationDate(localFile);
  146  			auto duration = Utils::Time::DateTime::now().elapsedSecondsSince(date);
  147  			if (duration > mKeepInCacheDuration)
  148  			{
  149  				keepLoadingLocal = false;
  150  				Utils::FileSystem::removeFile(localFile);
  151  			}
  152  		}
  153  
  154  		if (keepLoadingLocal)
  155  		{
  156  			ImageComponent::setImage(localFile, tile, maxSize, checkFileExists, allowMultiImagePlaylist);
  157  			resize();
  158  			return;
  159  		}
  160  	}
  161  
  162  	mMaxSize = maxSize;
  163  	mUrlToLoad = path;
  164  	mLocalFile = localFile;
  165  }
  166  
  167  void WebImageComponent::update(int deltaTime)
  168  {
  169  	ImageComponent::update(deltaTime);
  170  
  171  	if (mRequest == nullptr)
  172  		return;
  173  
  174  	if (mBusyAnim != nullptr)
  175  		mBusyAnim->update(deltaTime);
  176  
  177  	auto status = mRequest->status();
  178  	if (status == HttpReq::REQ_IN_PROGRESS)
  179  		return;
  180  
  181  	if (mBusyAnim != nullptr)
  182  	{
  183  		delete mBusyAnim;
  184  		mBusyAnim = nullptr;
  185  	}
  186  
  187  	delete mRequest;
  188  	mRequest = nullptr;	
  189  
  190  	if (status == HttpReq::REQ_SUCCESS && Utils::FileSystem::exists(mLocalFile))
  191  	{
  192  		// A 204, or a 200 with nothing in it, is a download that succeeded
  193  		// with no image: the offline RetroAchievements proxy answers so for
  194  		// a badge it has not cached yet (#180). Kept, an empty file would be
  195  		// this component's copy for as long as the cache lasts -- forever by
  196  		// default -- and the badge would stay blank after the proxy had it.
  197  		if (Utils::FileSystem::getFileSize(mLocalFile) == 0)
  198  		{
  199  			Utils::FileSystem::removeFile(mLocalFile);
  200  			return;
  201  		}
  202  
  203  		ImageComponent::setImage(mLocalFile, false, mMaxSize, false);
  204  		resize();
  205  	}
  206  }
  207  
  208  void WebImageComponent::render(const Transform4x4f& parentTrans)
  209  {
  210  	if (!isVisible())
  211  		return;
  212  
  213  	Transform4x4f trans = parentTrans * getTransform();
  214  
  215  	float xClipMargin = mSize.x() / 2.0f;
  216  	int yClipMargin = mSize.y() / 2.0f;
  217  
  218  	if (!Renderer::isVisibleOnScreen(
  219  		trans.translation().x() - xClipMargin,
  220  		trans.translation().y() - yClipMargin, 
  221  		mSize.x() + 2 * xClipMargin,
  222  		mSize.y() + 2 * yClipMargin))
  223  		return;
  224  
  225  	if (mRequest == nullptr && !mUrlToLoad.empty() && !mLocalFile.empty())
  226  	{
  227  		std::string localPath = Utils::FileSystem::getParent(mLocalFile);
  228  		if (!Utils::FileSystem::exists(localPath))
  229  			Utils::FileSystem::createDirectory(localPath);
  230  		
  231  		// An image on the offline RetroAchievements proxy is asked for from
  232  		// its store and nothing else (fork #199): the icon or badge it has
  233  		// cached, or a 404 at once. Without the header, a proxy that still
  234  		// believes it is online -- up to fifteen seconds after a link drops,
  235  		// or on a link that is up and leads nowhere -- fetches an image it
  236  		// does not hold from the web with a ten-second timeout, one per
  237  		// visible row, while the page shows the device's copy. Every other
  238  		// host is asked exactly as before.
  239  		HttpReqOptions options(mLocalFile);
  240  		if (Utils::OfflineProxy::isProxyUrl(mUrlToLoad))
  241  			options.customHeaders.push_back(Utils::OfflineProxy::StoreOnlyHeader);
  242  
  243  		mRequest = new HttpReq(mUrlToLoad, &options);
  244  		mUrlToLoad = "";
  245  
  246  		if (mBusyAnim != nullptr)
  247  			delete mBusyAnim;
  248  
  249  		mBusyAnim = new BusyComponent(mWindow, "");
  250  		mBusyAnim->setBackgroundVisible(false);
  251  		mBusyAnim->setSize(mSize);
  252  	}
  253  	
  254  	if (mRequest == nullptr && mWaitLoaded && mOnLoaded != nullptr && mLoadingTexture == nullptr && mTexture && mTexture->bind())
  255  	{
  256  		resize();
  257  		mOnLoaded();
  258  		mWaitLoaded = false;
  259  	}
  260  
  261  	ImageComponent::render(parentTrans);
  262  
  263  	if (mRequest != nullptr && mBusyAnim != nullptr)
  264  		mBusyAnim->render(trans);
  265  }
```

## WebImageComponent.h `:1-10` (an excerpt, upstream-carried, at the pin)

```text
    1  #pragma once
    2  
    3  #include "ImageComponent.h"
    4  #include "BusyComponent.h"
    5  
    6  class HttpReq;
    7  
    8  class WebImageComponent : public ImageComponent
    9  {
   10  public:		
```

## The first reader's 02-forward-audit.md (whole)

# Forward audit — M6.P2 T34, EmulationStation's core components (#681)

Composed by `tools/t34-02.py` from this template and the generators under `tools/`. Each generated section ends with its generator's own "generated, asserted" line. Each generator was seen to exit 1 on a constructed drift before it was trusted (`stage-b/generator-drifts.txt`).

The read is the pin `16dbac5211eea7e70db7394372033be2be7df829`'s bytes, through `git -C <W> show`; the ES worktree stays at the pin until stage E. Every proof carries `proved:` in #681's vocabulary: `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`. A row whose proof is still owed says `pending:` and names the stage that owes it.

## Coverage

The 80 paths, one row each. The read tier comes from `git diff` against the fork's base `bccd715707`: added, modified, or neither. The inventory tier is fork-own for the first two and upstream-carried for the third. The fork's numstat is the same against the merge base `cada856d86` (asserted per row).

| Path | Lines (`grep -c ''`) | Inventory tier | Read tier | Fork +/- (against `bccd715707`, equal against `cada856d86`) | Leads naming it |
| --- | ---: | --- | --- | ---: | --- |
| `es-core/src/components/AnimatedImageComponent.cpp` | 86 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/AnimatedImageComponent.h` | 47 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/AsyncNotificationComponent.cpp` | 306 | fork-own | fork-modified | 128/17 | L-07, L-19, 3.18 |
| `es-core/src/components/AsyncNotificationComponent.h` | 78 | fork-own | fork-modified | 23/2 | - |
| `es-core/src/components/BatteryIconComponent.cpp` | 101 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryIconComponent.h` | 38 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryIndicatorComponent.cpp` | 56 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryIndicatorComponent.h` | 19 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryTextComponent.cpp` | 64 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BatteryTextComponent.h` | 30 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BusyComponent.cpp` | 134 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/BusyComponent.h` | 41 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ButtonComponent.cpp` | 225 | upstream-carried | upstream-carried | 0/0 | L-04, L-18, 3.26 |
| `es-core/src/components/ButtonComponent.h` | 73 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/CarouselComponent.cpp` | 1128 | upstream-carried | upstream-carried | 0/0 | L-13, 3.34, 3.8 |
| `es-core/src/components/CarouselComponent.h` | 183 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ClockComponent.cpp` | 52 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ClockComponent.h` | 24 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ComponentGrid.cpp` | 553 | fork-own | fork-modified | 38/2 | L-04, 3.1, 3.2, 3.3 |
| `es-core/src/components/ComponentGrid.h` | 150 | fork-own | fork-modified | 3/0 | - |
| `es-core/src/components/ComponentList.cpp` | 728 | fork-own | fork-modified | 5/0 | L-01, L-06, 3.28 |
| `es-core/src/components/ComponentList.h` | 169 | fork-own | fork-modified | 14/0 | 3.25 |
| `es-core/src/components/ComponentTab.cpp` | 437 | fork-own | fork-modified | 3/2 | 3.17 |
| `es-core/src/components/ComponentTab.h` | 82 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ControllerActivityComponent.cpp` | 603 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ControllerActivityComponent.h` | 135 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/DateTimeComponent.cpp` | 110 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/DateTimeComponent.h` | 41 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/DateTimeEditComponent.cpp` | 363 | upstream-carried | upstream-carried | 0/0 | 3.12, 3.13 |
| `es-core/src/components/DateTimeEditComponent.h` | 77 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/GridTileComponent.cpp` | 1596 | fork-own | fork-modified | 22/0 | L-14, 3.24 |
| `es-core/src/components/GridTileComponent.h` | 332 | fork-own | fork-modified | 16/0 | - |
| `es-core/src/components/HelpComponent.cpp` | 331 | fork-own | fork-modified | 25/7 | L-01, 3.16 |
| `es-core/src/components/HelpComponent.h` | 44 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/IExternalActivity.cpp` | 3 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/IExternalActivity.h` | 14 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/IList.h` | 431 | upstream-carried | upstream-carried | 0/0 | 3.15, 3.8 |
| `es-core/src/components/ImageComponent.cpp` | 1400 | fork-own | fork-modified | 58/4 | L-20, 3.22, 3.23, 3.24 |
| `es-core/src/components/ImageComponent.h` | 220 | fork-own | fork-modified | 16/0 | - |
| `es-core/src/components/ImageGridComponent.h` | 1705 | fork-own | fork-modified | 19/0 | L-14, 3.10, 3.9 |
| `es-core/src/components/MenuComponent.cpp` | 574 | fork-own | fork-modified | 86/49 | L-04, L-05, L-15, L-16, L-18, 3.26, 3.27 |
| `es-core/src/components/MenuComponent.h` | 122 | fork-own | fork-modified | 9/0 | - |
| `es-core/src/components/MultiLineMenuEntry.cpp` | 153 | fork-own | fork-modified | 58/26 | L-02, L-03, 3.4 |
| `es-core/src/components/MultiLineMenuEntry.h` | 46 | fork-own | fork-modified | 19/0 | - |
| `es-core/src/components/NetworkIconComponent.cpp` | 79 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/NetworkIconComponent.h` | 34 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/NinePatchComponent.cpp` | 495 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/NinePatchComponent.h` | 88 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/OptionListComponent.h` | 661 | upstream-carried | upstream-carried | 0/0 | L-11, L-13, L-16, 3.19 |
| `es-core/src/components/PostProcessShaderComponent.cpp` | 105 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/PostProcessShaderComponent.h` | 28 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/RatingComponent.cpp` | 295 | upstream-carried | upstream-carried | 0/0 | 3.32 |
| `es-core/src/components/RatingComponent.h` | 63 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/RectangleComponent.cpp` | 166 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/RectangleComponent.h` | 37 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ScrollableContainer.cpp` | 132 | upstream-carried | upstream-carried | 0/0 | 3.14 |
| `es-core/src/components/ScrollableContainer.h` | 32 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ScrollbarComponent.cpp` | 215 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/ScrollbarComponent.h` | 64 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/SliderComponent.cpp` | 408 | upstream-carried | upstream-carried | 0/0 | 3.31, 3.7 |
| `es-core/src/components/SliderComponent.h` | 67 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/StackPanelComponent.cpp` | 226 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/StackPanelComponent.h` | 37 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/SwitchComponent.cpp` | 175 | fork-own | fork-modified | 13/3 | L-16, 3.30 |
| `es-core/src/components/SwitchComponent.h` | 60 | fork-own | fork-modified | 9/1 | - |
| `es-core/src/components/TextComponent.cpp` | 857 | upstream-carried | upstream-carried | 0/0 | L-17, 3.5, 3.6 |
| `es-core/src/components/TextComponent.h` | 141 | fork-own | fork-modified | 2/0 | - |
| `es-core/src/components/TextEditComponent.cpp` | 400 | upstream-carried | upstream-carried | 0/0 | L-12, L-16, 3.20, 3.33 |
| `es-core/src/components/TextEditComponent.h` | 72 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/TextListComponent.h` | 981 | upstream-carried | upstream-carried | 0/0 | L-16, 3.11, 3.29 |
| `es-core/src/components/VideoComponent.cpp` | 657 | upstream-carried | upstream-carried | 0/0 | L-20 |
| `es-core/src/components/VideoComponent.h` | 228 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VideoPlayerComponent.cpp` | 274 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VideoPlayerComponent.h` | 42 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VideoVlcComponent.cpp` | 1113 | upstream-carried | upstream-carried | 0/0 | L-10 |
| `es-core/src/components/VideoVlcComponent.h` | 170 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VolumeInfoComponent.cpp` | 143 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/VolumeInfoComponent.h` | 30 | upstream-carried | upstream-carried | 0/0 | - |
| `es-core/src/components/WebImageComponent.cpp` | 265 | fork-own | fork-modified | 25/1 | L-08, L-09, L-21, 3.21 |
| `es-core/src/components/WebImageComponent.h` | 40 | upstream-carried | upstream-carried | 0/0 | - |

Generated, asserted by `tools/t34-coverage.py`: 80 rows; 38 `.cpp`, 42 `.h`; fork-added 0 / fork-modified 21 / upstream-carried 59 (inventory fork-own 21 / upstream-carried 59); 21984 lines by `grep -c ''`; fork +591/-114; 55 brief leads, each naming a path in the 80.

## The leads

The brief's L-01 to L-21 and floor rows 3.1 to 3.34, plus three the read found (L-22 to L-24). A lines cell is the brief's own (the new three are the read's). Each row answers in one of the seven families of the brief's § 4. Bold floor rows are the seven the brief expects to FAIL at the pin. Each is seen to FAIL against the unfixed extract at stage C before it is trusted, and a candidate that PASSes at the pin is recorded as such.

| Lead | Lines at the pin | Family | Owner | Disposition | proved | question: |
| --- | --- | --- | --- | --- | --- | --- |
| L-01 | `ComponentList.cpp:568`; `HelpComponent.cpp:102-104`, `:190-194`; `es-core/src/InputConfig.cpp:353-366`; fr po `:3708-3709` | a player sentence outside the vocabulary or without French | T34 (`ComponentList.cpp:568`, upstream's line); `InputConfig.cpp` T35's, cited | a defect in an upstream line: under French every settings list's CHOOSE prompt draws no icon and logs `Unknown help icon`; 3.16's case FAILs at the pin, G-04 under French is the frame; contained fix under rule 6 (drop the `_()`), a `bug` at stage D, a #585 line; the catalog's orphan is a row for the pause | tree | Q3, Q6 |
| L-02 | `MultiLineMenuEntry.cpp:52-56`; `resources/Font.cpp:754-756`, `:420-421`, `:107` | layout from what it produced / a moving number | T34; `resources/Font.cpp` T36's, cited | the moving number at a row's construction; a read trace and G-05's reopened-page pair; a rasterise-first in the component or a record is the pause's | tree | Q1 |
| L-03 | `MultiLineMenuEntry.cpp:74-75` | layout from what it produced / a moving number | T34 (upstream's formula, moved whole by the fork's `48d43c0fb`) | 3.4 FAILs at the pin (the shares sum to 0.987 and 1.013); `git log -S` first at stage C; the pause rules whether the component's shares are made to sum to 1 (a register row) | tree | Q1 |
| L-04 | `MenuComponent.cpp:14`, `:547-558`, `:527`; `ComponentGrid.cpp:174-175`, `:194`; `ButtonComponent.cpp:10`, `:80` | a house constant a surface does not keep | T34; the pages with wide bars T26's and T31's | 3.26's arithmetic; the widest bars framed at 640 (G-03); a bar that fits its cell, or the pages' labels, is the pause's | tree | Q2 |
| L-05 | `MenuComponent.cpp:7-13` against `es-core/src/guis/GuiTextEditPopupKeyboard.cpp:14`, `:220` | a house constant a surface does not keep | the comment T34's; the popup T35's | recorded, not deleted (`engineering-practices.md:576`); the comment corrected or the claim kept at the pause | tree | Q2, Q7 |
| L-06 | `ComponentList.cpp:11`, `:491-494`; `guis/GuiMenu.cpp:4091`, `:4097`; `guis/GuiWifi.cpp:103` | a house constant a surface does not keep | T34 (upstream's constant); `rowInset()`'s two fork pages T26's and T31's | framed at both sizes (G-04, G-11); a screen fraction under D-UI-012's family is a register row for the pause | tree | Q2 |
| L-07 | `AsyncNotificationComponent.cpp:12`; `es-core/src/Window.cpp:29` | a structure or merge-debt fact | T34 (the include line); `CloudText` T18's, the CMake T35's | recorded with how it resolves; a `CloudText` that moves to es-core is T18's and T35's call | tree | Q7 |
| L-08 | `WebImageComponent.cpp:197-200`, `:244` | a read of a file another process writes | T34 | by design per `:191-196`; the player sees a blank badge for the page's life with no word; a re-ask on the next page build, or a word on the row, is the pause's; `tools/ra-ui-test`'s fixture shape at stage C | tree | Q5 |
| L-09 | `WebImageComponent.cpp:190` (and `:81`, `:134`, `:228`); `utils/FileSystemUtil.cpp:144`, `:203-220` | a read of a file another process writes | T34; `HttpReq` T21's, `FileSystemUtil` T36's, cited | sound at the pin: the writer's `removeFile` (`HttpReq.cpp:344`) and `renameFile` (`:479` -> `FileSystemUtil.cpp:1457-1458`) erase the cached miss before `:190` asks; 3.21's first half a candidate that PASSes at the pin | tree | Q5 |
| L-10 | `VideoVlcComponent.cpp:84-95`, `:53-61`, `:28-49`, `:491-494`, `:911` | a lifetime or a thread | T34 (upstream surface, outside the lanes) | a data race on `ctx->component` and a call into a component being destroyed; recorded with the two threads named (§ The lifetimes); G-10 `CANNOT` (no media); a contained fix (an atomic, or a wait) under rule 6 only if the pause opens it | tree | Q4 |
| L-11 | `OptionListComponent.h:96`, `:145`, `:158`, `:195`; `:310-311`, `:323-324` | a lifetime or a thread | T34 | sound by the invariant: each `delete this` is the last thing its handler does; 3.19's ASan harness at stage C | tree | Q4 |
| L-12 | `TextEditComponent.cpp:39`, `:47` | a lifetime or a thread | T34; `Window::postToUiThread` T35's, `AppWindow` T33's | a use after free if the field dies before the post runs; 3.20's case at stage C with the fakes' `Window.h`; a weak token the posts check is the pause's | tree | Q4 |
| L-13 | `CarouselComponent.cpp:354-361`; `OptionListComponent.h:639-640` | a prompt where the key moves nothing | T34 (upstream surfaces) | recorded; framed if a one-system carousel or a one-value option row is reachable on the guest | tree | Q3 |
| L-14 | `GridTileComponent.cpp:1043`; `ImageGridComponent.h:2`, `:380-381` | a structure or merge-debt fact | T34 | a one-commit tidy if the pause opens it | tree | Q7 |
| L-15 | `MenuComponent.cpp:506-515`, `:492-503`; `guis/GuiMenu.cpp:591` | a structure or merge-debt fact | T34; `GuiMenu.cpp:591` T26's | an unstated invariant: the cast is safe only because the MAIN MENU's `mButtons` is empty and the index guard `:508` returns first; written into `02` beside `MenuComponent.h:53-56`; a `dynamic_pointer_cast` plus a null check is the contained fix | tree | Q3 |
| L-16 | `SwitchComponent.cpp:14`; `OptionListComponent.h:255`, `:276`; `TextEditComponent.cpp:31`; `MenuComponent.cpp:393`; `TextListComponent.h:613`, `:725` | layout from what it produced / a moving number | T34; `TextListComponent.h` an upstream surface | the seven reads tabled in § The layouts with their surfaces; disposition with L-02's | tree | Q1 |
| L-17 | `TextComponent.cpp:338` against `:350` | layout from what it produced / a moving number | T34 (upstream's `TextComponent.cpp`) | #48's root, unchanged at the pin: 3.5's case, a 640x480 frame of a padded auto-height text that is not a `GuiMsgBox`, the reproducer for #585; the root fix (re-heights every padded auto-height text) is the pause's, a register row | tree | Q1 |
| L-18 | `MenuComponent.cpp:205`, `:233`, `:236`, `:283`, `:487`; `ButtonComponent.cpp:73` | a player sentence outside the vocabulary or without French | T34 | a reading, not a check: no fork label carries the brand through the six formatters at the pin; a `tools/vocabulary-check` rule (the brand inside `addEntry|addButton|setTitle|addWithDescription|addGroup` arguments) proposed for the coordinator | tree | Q6 |
| L-19 | `AsyncNotificationComponent.cpp:63-65` | a house constant a surface does not keep | T34 | dead text, harmless; recorded | tree | Q2 |
| L-20 | `VideoComponent.cpp:327`, `:591`; `ImageComponent.cpp:1232` | a read of a file another process writes | T34 (upstream surfaces); the scraper T32's | recorded with the scraper as the writer; a frame only if a scrape then a game open fits the window, else `CANNOT` | tree | Q5 |
| L-21 | `WebImageComponent.cpp:239-243`; `es-core/src/HttpReq.cpp:119-123`, `:131-132`, `:172-176` | a lifetime or a thread | T34; `HttpReq` T21's | sound; recorded so the next reader does not re-derive it | tree | Q4 |
| L-22 | `AsyncNotificationComponent.cpp:117-121`, `:261-299`; h `:72`, `:74` | a lifetime or a thread | T34 (a lane surface); the holders T18's and T20's | **new:** `close()` writes `mClosing` and `mFadeTime` unlocked from the holders' threads while `update()` reads them on the interface thread; a host ThreadSanitizer case at stage C; a `bug` at stage D if it fires; § 1 (b)'s component half beside it | tree | Q4 |
| L-23 | `RatingComponent.cpp:262-266` | a player sentence outside the vocabulary or without French | T34 (upstream's line) | **new:** the rating's OK prompt `"add star"` is outside `_()`; contained under rule 6 with its French in the same commit; a #585 line | tree | Q6 |
| L-24 | `VideoComponent.cpp:347-351` | a prompt where the key moves nothing | T34 (upstream's line) | **new:** a focused video component's help bar names BACK as `SELECT`; reached only where a video component holds focus; recorded, contained under rule 6 if the pause opens it | tree | Q3, Q6 |
| 3.1 | `ComponentGrid.cpp:396-414` | a prompt where the key moves nothing | T34 | a case at stage C; expected PASS (D-UI-034's fix) | pending: fixture at stage C | Q3 |
| 3.2 | `ComponentGrid.cpp:519-553` | a prompt where the key moves nothing | T34 | a case at stage C; expected PASS | pending: fixture at stage C | Q3 |
| 3.3 | `ComponentGrid.cpp:329-379` | a prompt where the key moves nothing | T34 | a case at stage C; expected PASS | pending: fixture at stage C | Q3 |
| **3.4** | `MultiLineMenuEntry.cpp:50-80` (**`:74-75`**) | layout from what it produced / a moving number | T34 | FAIL at the pin (L-03); 300 `setDescription` calls hold the height (#241) | pending: fixture at stage C | Q1 |
| 3.5 | `TextComponent.cpp:315-340` | layout from what it produced / a moving number | T34 | L-17's case: the measured height one line short | pending: fixture at stage C | Q1 |
| **3.6** | `TextComponent.cpp:486` | layout from what it produced / a moving number | T34 | FAIL at the pin: the limit 20 px too large | pending: fixture at stage C | Q1 |
| **3.7** | `SliderComponent.cpp:44-58`, `:271-319` (**`:282`**) | a player sentence outside the vocabulary or without French | T34 | FAIL at the pin: `"Auto"`; the precision cases expected PASS | pending: fixture at stage C | Q6 |
| **3.8** | `CarouselComponent.cpp:74-90` with `:113`, `:119`; `IList.h:376-400` | a prompt where the key moves nothing | T34 | FAIL candidate: `listInput(-7)` on a size-3 carousel; the landing index asserted in `[0, sz)` per loop type | pending: fixture at stage C | Q3 |
| 3.9 | `ImageGridComponent.h:1437-1468` | layout from what it produced / a moving number | T34 | a case; a 0 tile size is guarded only by a `LOG` | pending: fixture at stage C | Q1 |
| 3.10 | `ImageGridComponent.h` from `:1065` (`:1162-1186`) | layout from what it produced / a moving number | T34 | a case on the partial last row | pending: fixture at stage C | Q1 |
| 3.11 | `TextListComponent.h:262-269` | layout from what it produced / a moving number | T34 | a case on the extra row past the cutoff | pending: fixture at stage C | Q1 |
| 3.12 | `DateTimeEditComponent.cpp:124-160` | a structure or merge-debt fact | T34 | a case on the date steps (an extraction or a fake `InputConfig`) | pending: fixture at stage C | Q7 |
| 3.13 | `DateTimeEditComponent.cpp:251-260` | a player sentence outside the vocabulary or without French | T34 | PASS at the pin as written: a blank, not `<NOT SET>`; a style question for the pause | pending: fixture at stage C | Q6 |
| 3.14 | `ScrollableContainer.cpp:62-107`, `:110-124`, `:126-131` | a structure or merge-debt fact | T34 | a case; `:69`'s unused `680.0f` is lint | pending: fixture at stage C | Q7 |
| 3.15 | `IList.h:267-330`, `:376-400` | a prompt where the key moves nothing | T34 | a case, the landing index for 3.8 | pending: fixture at stage C | Q3 |
| **3.16** | `HelpComponent.cpp:73-130`, `:121-169`, `:176-200` | a player sentence outside the vocabulary or without French | T34 | FAIL at the pin: `haut/bas` -> `nullptr` and the `Unknown help icon` line (L-01) | pending: fixture at stage C | Q3, Q6 |
| 3.17 | `ComponentTab.cpp:77-96`, `:320-345` | a prompt where the key moves nothing | T34 | a case; expected PASS | pending: fixture at stage C | Q3 |
| 3.18 | `AsyncNotificationComponent.cpp:136-145`, `:63-65` | a house constant a surface does not keep | T34 | a case: the width handed to `chooseThatFits` is the row's cell, never 0.9 W | pending: fixture at stage C | Q6 |
| 3.19 | `OptionListComponent.h:88-100`, `:140-160`, `:188-200` (ASan) | a lifetime or a thread | T34 | ASan over an extracted popup (L-11) | pending: fixture at stage C | Q4 |
| 3.20 | `TextEditComponent.cpp:39`, `:47` | a lifetime or a thread | T34 | post, delete, drain (L-12) | pending: fixture at stage C | Q4 |
| **3.21** | `WebImageComponent.cpp:134`, `:190`, `:197-200`; `utils/FileSystemUtil.cpp:144` | a read of a file another process writes | T34 | first half a candidate that PASSes at the pin (L-09); second half: the 204 then 200 is never asked again (L-08, by design) | pending: fixture at stage C | Q5 |
| 3.22 | `ImageComponent.cpp:85-180` | layout from what it produced / a moving number | T34 | a case on the fit after a turn | pending: fixture at stage C | Q5 |
| 3.23 | `ImageComponent.cpp:273-291` | layout from what it produced / a moving number | T34 | a case; turn 1 four times is identity | pending: fixture at stage C | Q5 |
| 3.24 | `ImageComponent.cpp:491-499`, `GridTileComponent.cpp:1055-1063` | layout from what it produced / a moving number | T34 | a case on the normaliser | pending: fixture at stage C | Q5 |
| 3.25 | `ComponentList.h:26` | a house constant a surface does not keep | T34 | a case; expected PASS | pending: fixture at stage C | Q2 |
| **3.26** | `MenuComponent.cpp:543-562`; `ButtonComponent.cpp:10` | a house constant a surface does not keep | T34 | FAIL candidate: five 128 px buttons at 640 overhang (L-04) | pending: fixture at stage C | Q2 |
| 3.27 | `MenuComponent.cpp:396-424` | layout from what it produced / a moving number | T34 | a case on the strict `<` | pending: fixture at stage C | Q1 |
| 3.28 | `ComponentList.cpp:295-319` | layout from what it produced / a moving number | T34 | a case incl. the signed/unsigned compare | pending: fixture at stage C | Q1 |
| 3.29 | `TextListComponent.h:591-608` | layout from what it produced / a moving number | T34 | the same for the game list | pending: fixture at stage C | Q1 |
| 3.30 | `SwitchComponent.cpp:50-80`, `:118-138` | a prompt where the key moves nothing | T34 | a case on the tri-state cycle | pending: fixture at stage C | Q3 |
| 3.31 | `SliderComponent.cpp:234-257` | a house constant a surface does not keep | T34 | a case on the clamp and the sentinel | pending: fixture at stage C | Q3 |
| 3.32 | `RatingComponent.cpp:192-204` | a structure or merge-debt fact | T34 | a case on the accumulation's drift | pending: fixture at stage C | Q7 |
| 3.33 | `TextEditComponent.cpp:267-271` | a structure or merge-debt fact | T34 | a case on a cursor inside a UTF-8 sequence (T21's `moveCursor`) | pending: fixture at stage C | Q7 |
| 3.34 | `CarouselComponent.cpp:183-200` | a prompt where the key moves nothing | T34 | a case incl. a count of 1 and a divide by 0 | pending: fixture at stage C | Q3 |

**The brief's § 1 rulings, each with its row:**

| Ruling | Its row in this file |
| --- | --- |
| (a) T32 PL-07 / #1263, the caller's half | § The reads, `ImageComponent.cpp:408` |
| (b) T2 PC-1, the card's half | § The lifetimes, `AsyncNotificationComponent.cpp:123`, with L-22 at `:119` |
| (c) T26 PL-27, the callback types | § The lifetimes, `SwitchComponent.h:53` and `OptionListComponent.h:658` |
| (d) T31 L-03 / #1243's invariant | § The lifetimes, `OptionListComponent.h:310` and `:323` |
| (e) #1266's grid after `clear()` | § The lifetimes, `ImageGridComponent.h:91` |
| (f) #48's `TextComponent` root | § The layouts, `TextComponent.cpp:338` and `:483` |
| (g) batocera's `setOpacity` guard | § The structure: `HelpComponent.cpp:212-213` dereference `mGrid` unguarded, `:251` is inside `render`'s `if (mGrid)` (`:218`); `mGrid` is null when `ShowHelpPrompts` is off or there are no prompts (`:67-70`); nothing calls `HelpComponent::setOpacity` on the fork's images (`Window.cpp` constructs the one bar at `:41` and never calls it; the bar is no component's child): unreachable at the pin, recorded; the guard arrives with batocera's `9dbd4b9bf` at the reconciliation |
| (h) `UntintedImageComponent` | § The structure: it lives at `es-app/src/guis/GuiMenu.cpp:6401` (T26's file; the QR at `:6425`), not under `components/`; lifting an untinted mode into `ImageComponent` (h `:76`) is the pause's question |
| (i) `ComponentList.cpp:568`'s `_("up/down")` | § The words, L-01, and § The input, `ComponentList.cpp:548` |
| (j) the two lanes' `AsyncNotificationComponent.h` doubles | § The structure: a header change in T34 is named as a collision at the hand-back; the fakes are not the lane's |

Generated, asserted by `tools/t34-leads.py`: 24 L leads (the brief's 21 and the read's L-22 to L-24), 34 floor rows (the seven FAIL-at-pin in bold), each answered; 10 rulings, each with its row.

## The layouts

**Every font-height read** (`Font::getHeight` is the tallest ASCII glyph rasterised so far (`resources/Font.cpp:754-756`, `:420-421`, from 0 `:107`; T36's): a size taken before the font has drawn its tallest glyph is a few px short of one taken after (`es-code-traps.md:118`)):

| Site | Kind | What it sizes | The surface that shows it | Disposition | proved |
| --- | --- | --- | --- | --- | --- |
| `HelpComponent.cpp:276` | layout | whether the help bar fits below its grid (`getHeight(1.5f)`) | the help bar on every page | the moving number; not in the brief's eight; recorded beside them | tree |
| `MenuComponent.cpp:393` (brief) | layout | the button bar's height when there is no bar yet | every settings page's footer | L-16 | tree |
| `MultiLineMenuEntry.cpp:55` (brief) | layout (constructor) | a label-and-description row's text height (`naturalHeight`, `:50-56`) | every cloud, achievements and settings row built on `MultiLineMenuEntry`; G-05's reopened page | **L-02**: `Font::getHeight` is the tallest ASCII glyph rasterised so far (`resources/Font.cpp:754-756`, `:420-421`, from 0 `:107`; T36's): a size taken before the font has drawn its tallest glyph is a few px short of one taken after (`es-code-traps.md:118`); a rasterise-first in the component or a record, the pause's | tree |
| `OptionListComponent.h:255` (brief) | layout (constructor) | the option row's height | every option row | L-16 | tree |
| `OptionListComponent.h:276` (brief) | layout | the option text's height on a resize | every option row | L-16 | tree |
| `SwitchComponent.cpp:14` (brief) | layout (constructor) | the switch image's height (`getHeight(1.1f)`) | every on/off row; G-04 | L-16: the moving number | tree |
| `TextComponent.cpp:336` | layout | a single-line auto-height text's height | every auto-height single-line label | the moving number; not in the brief's eight (it is `TextComponent`'s own, L-17's file); recorded | tree |
| `TextComponent.cpp:359` | layout (decision) | AUTO's one-line-or-wrap choice: `sy > getHeight * 1.8` where `sy` is the height `:336`/`:338` wrote | every AUTO text | the rule's shape (a decision from the size the auto pass wrote, and a moving number): stable at the pin (a text that wrapped to one line is drawn as one) -- 3.5's case confirms at stage C | tree |
| `TextComponent.cpp:432` | layout (decision) | the same decision in `buildTextCache`'s second form | every AUTO text | as `:359` | tree |
| `TextEditComponent.cpp:31` (brief) | layout (constructor) | the text field's height | the key popups' fields (T35's pages) | L-16 | tree |
| `TextEditComponent.cpp:377` | layout (decision) | whether the field is multi-line (`getSize().y() > getHeight * 1.25`) | - | a decision from the size its owner set; recorded | tree |
| `TextListComponent.h:613` (brief) | layout | a game-list row's height when no line count is themed | the text game list | L-16; upstream surface outside the lanes | tree |
| `TextListComponent.h:725` (brief) | layout | the game list's selector bar height | the text game list | L-16; upstream surface outside the lanes | tree |
| `TextComponent.cpp:176` | render | a line's height while drawing | - | per frame: re-read each draw | tree |
| `TextComponent.cpp:200` | render | the same, the second draw path | - | per frame | tree |
| `TextEditComponent.cpp:298` | scroll | whether the field must scroll down | - | per input | tree |
| `TextEditComponent.cpp:300` | scroll | the scroll offset | - | per input | tree |
| `TextEditComponent.cpp:364` | render | the cursor's height | - | per frame | tree |
| `TextEditComponent.cpp:370` | render | the cursor's position | - | per frame | tree |

**Every size computed from a size a pass wrote, or measured at one width and drawn at another:**

| Site | What it computes, and from what | The surface | Disposition | proved |
| --- | --- | --- | --- | --- |
| `MultiLineMenuEntry.cpp:74` | the two rows' shares, `th*0.9/h` and `sh*1.1/h` of `h = th + sh` (`:72-75`), measured from the fonts since #241 (`7c7ffab43`), not from the cells | every two-line row | **L-03**: the shares sum to 1 only when `th == sh`: a taller Text font underfills, a taller TextSmall overflows by `0.1*(sh-th)/h`; upstream's formula moved whole into `layoutRows`; 3.4's `rowPercs(26, 20)` and `(20, 26)` FAIL at the pin; the fix (a pair that sums to 1) is the pause's | tree |
| `MultiLineMenuEntry.cpp:71` | in multi-line mode, the description's height read back from the text (`:71`) | the multi-line rows (re-laid in `onSizeChanged`, `:121-136`) | the rule's shape (a size the text's own auto pass wrote); stable while the width is: 3.4's 300 `setDescription` calls at stage C | tree |
| `TextComponent.cpp:338` | the auto height, wrapped at the full width `getSize().x()` | every padded auto-height text that is not a `GuiMsgBox` | **L-17** (#48's root): drawn at `mSize.x() - padding` (`:350`), so a wrap in that band paints a line the height never budgeted; 3.5's case; a 640x480 frame of a padded auto-height text; the reproducer for #585; the root fix the pause's (§ 1 f) | tree |
| `TextComponent.cpp:483` | the vertical marquee's text length, wrapped at the full width | a vertically scrolling text with padding | L-17's second site: the same full-width measure | tree |
| `TextComponent.cpp:486` | the vertical marquee's limit, `mSize.y() - mPadding.y() - mPadding.y()` | a vertically scrolling text with unequal top and bottom padding | **3.6**: `:351` and `:428` subtract `.y()` and `.w()`; with padding (0,10,0,30) the limit is 20 px too large; a contained one-token fix under rule 6 and a #585 line | tree |
| `MenuComponent.cpp:396` | `updateSize`'s row-fit loop: rows added while `height + rowHeight < maxHeight` (`:396-424`) | every settings page's height | 3.27: the strict `<` drops a row that fits exactly; a case at stage C | tree |
| `ComponentList.cpp:521` | each element's width from the list's own width less the inset | every row | sound: from the parent's size, not the element's | tree |
| `HelpComponent.cpp:143` | the bar's grid width from the entries kept (`:143-152`), floored at 1 | the help bar | sound since `7dc8bf373` (#210): measured before an entry is added; 3.16 | tree |
| `AsyncNotificationComponent.cpp:63` | the card's width, `max(sizeText(30 chars), 0.9 W)` | the card | L-19: the floor never binds at 640 or wider; dead text, harmless | tree |
| `ScrollableContainer.cpp:69` | `widthMod = 680.0f / getSize().x()`, computed and never used | - | 3.14: lint, recorded | tree |

Generated, asserted by `tools/t34-layouts.py`: 19 font-height reads (13 layout, 6 render or scroll), the brief's eight among the layout rows; 10 size rows, each cited line asserted to hold its code or be non-blank.

## The constants

**The house values:**

| Value | Its one definition | Value at the panels | Every reader in the 80 | The frame that shows it | Disposition | proved |
| --- | --- | --- | --- | --- | --- | --- |
| `BUTTON_GRID_HORIZ_PADDING` | `MenuComponent.cpp:14` | 0.022 W (14.08 px at 640, 28.16 at 1280) | `MenuComponent.cpp:547`, `MenuComponent.cpp:555` | G-03 (640), G-11 (1280): the gap between YES's and NO's nine-patch edges, read in the frame's columns | D-UI-012; L-04 (a bar wider than its cell overhangs: 3.26), L-05 (the second copy, below) | tree |
| `BUTTON_GRID_VERT_PADDING` | `MenuComponent.cpp:6` | 0.0296 H (14.2 px at 480) | `MenuComponent.cpp:393`, `MenuComponent.cpp:558` | G-03 | upstream's; recorded | tree |
| `NOTIFICATION_OPACITY` | `AsyncNotificationComponent.cpp:31` | 255 | `AsyncNotificationComponent.cpp:114`, `AsyncNotificationComponent.cpp:276` | G-02: a pixel inside the card over the game art equals the panel colour, not a blend | D-UI-016; sound | tree |
| `DIMMED_ALPHA` | `ComponentList.h:25` | 0x50 of 0xFF | `ComponentList.h:26` | G-04: the unconfigured rows' text against the selectable rows' over one panel | #182's mechanism (`dimmed()` h `:26`, applied in each element's own `setColor`); 3.25 | tree |
| `TOTAL_HORIZONTAL_PADDING_PX` | `ComponentList.cpp:11` | 20 px (10 a side) | `ComponentList.cpp:92`, `ComponentList.cpp:493`, `ComponentList.cpp:508`, `ComponentList.cpp:521` | G-04 (640), G-11 (1280): the row inset | L-06: upstream's pixel constant the fork exported through `rowInset()` to two pages; a screen fraction is the pause's | tree |
| `ICON_TEXT_SPACING` | `HelpComponent.cpp:13` | 0.0042 W (2.7 px at 640) | `HelpComponent.cpp:16`, `HelpComponent.cpp:130`, `HelpComponent.cpp:164` | G-03, G-04, G-11: the help bar | upstream's; sound | tree |
| `ENTRY_SPACING` | `HelpComponent.cpp:16` | 0.0084 W | `HelpComponent.cpp:79`, `HelpComponent.cpp:130`, `HelpComponent.cpp:151`, `HelpComponent.cpp:166` | the same | upstream's; the last entry's trailing spacer 0 (fork `7dc8bf373`, #210) | tree |
| the card's width | `AsyncNotificationComponent.cpp:64` | 0.9 W | - | the card's width, `max(sizeText(30 chars), 0.9 W)` (`:63-65`); G-02: edges at x 32 and x 608 at 640 (0.9 W centred); L-19: the measured floor never binds on a panel 640 or wider, dead text | D-UI-016; sound | tree |
| the card's position | `AsyncNotificationComponent.cpp:112` | 0.9 W | - | the card centred at the top (`:112-113`); `Window::renderAsyncNotifications` re-applies the position every frame (`Window.cpp:1183`, `:1192`, T35's, cited); G-02 | D-UI-016; sound | tree |
| `BUTTON_GRID_HORIZ_PADDING`, the second copy | `guis/GuiTextEditPopupKeyboard.cpp:14` (T35's) | 0.0052083333 W (3.3 px at 640) | that popup's key buttons (`:220`) | - | **L-05:** `MenuComponent.cpp:7-13` says the gap is defined in "the one place"; the keyboard popup keeps its own at the old value; recorded, not deleted (`engineering-practices.md:576`); the comment is this slice's, the popup T35's | tree |

**The pixel constants** (`es-native-ui.md:299`: fractions, never pixel constants; each with its share of a 640 and a 1920 panel's width):

| Site | Pixels | Share of 640 / 1920 | What it sizes | Disposition |
| --- | ---: | --- | --- | --- |
| `ComponentList.cpp:11` | 20 | 3.1% / 1.0% | every row's horizontal inset | L-06; read by two fork pages through `rowInset()` |
| `TextEditComponent.cpp:8` | 10 | 1.6% / 0.5% | the text field's horizontal padding | upstream's; outside the lanes unless a fork page reads it (the Wi-Fi and cloud key fields do, through the popups, T35's) |
| `TextEditComponent.cpp:9` | 2 | 0.3% / 0.1% | the text field's vertical padding | as `:8` |
| `TextEditComponent.cpp:31` | 4096 | 640.0% / 213.3% | the field's initial width, replaced by its owner's layout | harmless: a placeholder width |
| `ButtonComponent.cpp:10` | 12 | 1.9% / 0.6% | a button's text padding floor, `max(12, 0.014 W)`: the 12 wins below 857 px | upstream's; G-03's bar at 640 is built on it |
| `GridTileComponent.cpp:56` | 16 | 2.5% / 0.8% | a grid tile's default padding | upstream's; G-08 if a grid theme exists |
| `GridTileComponent.h:148` | 16 | 2.5% / 0.8% | a tile frame's corner size | upstream's |
| `MenuComponent.cpp:167` | 10 | 1.6% / 0.5% | the spacer before a row's right-hand component | upstream's |
| `MenuComponent.cpp:192` | 10 | 1.6% / 0.5% | the same, the second builder | upstream's |
| `VideoVlcComponent.cpp:782` | 400 | 62.5% / 20.8% | a video's default max size | upstream surface outside the lanes; recorded |
| `NinePatchComponent.cpp:177` | 50 | 7.8% / 2.6% | the post-process shader's margin | upstream's; recorded |
| `AsyncNotificationComponent.cpp:94` | 32 | 5.0% / 1.7% | the card's nine-patch corner (`fitTo(..., -32, -32)`) | the corner of every framed surface; outside a fraction by design (the frame image's corner) |
| `MenuComponent.cpp:453` | 32 | 5.0% / 1.7% | the menu's background corner | as above |
| `VolumeInfoComponent.cpp:45` | 32 | 5.0% / 1.7% | the volume overlay's corner | as above |
| `TextEditComponent.cpp:53` | 32 | 5.0% / 1.7% | the text field's frame corner (`-34, -32 - 2`) | as above |

Generated, asserted by `tools/t34-constants.py`: 7 house values, each defined once in the 80 with 18 readers in all; the card's width and position; the keyboard popup's second copy and `MenuComponent.cpp`'s one-place claim, both asserted present; 15 pixel constants, each cited line asserted to hold its code.

## The input

**The inputs** (the keys each names, read from its body):

| `input()` | Form | Keys it names (`isMappedTo` / `isMappedLike`) | Body lines |
| --- | --- | --- | ---: |
| `ButtonComponent.cpp:50` | out-of-line | `BUTTON_OK` | 12 |
| `CarouselComponent.cpp:92` | out-of-line | `"down"`, `"left"`, `"lefttrigger"`, `"pagedown"`, `"pageup"`, `"right"`, `"righttrigger"`, `"up"` | 76 |
| `ComponentGrid.cpp:281` | out-of-line | `"down"`, `"left"`, `"right"`, `"up"` | 25 |
| `ComponentList.cpp:142` | out-of-line | `"down"`, `"leftshoulder"`, `"rightshoulder"`, `"up"` | 45 |
| `ComponentTab.cpp:77` | out-of-line | `"left"`, `"right"` | 13 |
| `ControllerActivityComponent.cpp:138` | out-of-line | `"hotkey"` | 21 |
| `DateTimeEditComponent.cpp:80` | out-of-line | `"down"`, `"left"`, `"leftshoulder"`, `"right"`, `"rightshoulder"`, `"up"`, `BUTTON_BACK`, `BUTTON_OK` | 107 |
| `ImageGridComponent.h:537` | out-of-line | `"down"`, `"left"`, `"leftshoulder"`, `"right"`, `"rightshoulder"`, `"up"` | 54 |
| `MenuComponent.cpp:126` | out-of-line | - (delegates) | 7 |
| `OptionListComponent.h:191` | inline | `BUTTON_BACK` | 10 |
| `OptionListComponent.h:284` | inline | `"left"`, `"right"`, `BUTTON_OK` | 47 |
| `RatingComponent.cpp:192` | out-of-line | `BUTTON_OK` | 13 |
| `SliderComponent.cpp:118` | out-of-line | `"left"`, `"right"` | 66 |
| `SwitchComponent.cpp:50` | out-of-line | `"left"`, `"right"`, `BUTTON_OK` | 46 |
| `TextEditComponent.cpp:140` | out-of-line | `"down"`, `"left"`, `"right"`, `"up"`, `BUTTON_OK` | 94 |
| `TextListComponent.h:458` | out-of-line | `"down"`, `"leftshoulder"`, `"rightshoulder"`, `"up"` | 40 |

**The help prompts** (the condition under which each offers a direction):

| `getHelpPrompts()` | Form | What it offers, and when | Disposition | proved |
| --- | --- | --- | --- | --- |
| `ButtonComponent.cpp:186` | out-of-line | OK with the button's help text; no direction | sound | tree |
| `CarouselComponent.cpp:354` | out-of-line | `up/down` or `left/right` CHOOSE by the carousel's type alone (`:358-361`), whatever its size | L-13: a one-entry carousel offers a direction that moves nothing; upstream surface, recorded; framed if a one-system carousel is reachable | tree |
| `ComponentGrid.cpp:519` | out-of-line | `up/down`, `left/right` or both CHOOSE only where `canMoveCursor` finds a focusable cell (`:527-528`, `:546-550`); a child's own `up/down` suppresses the grid's (`:536-538`) | sound (D-UI-034, fork `aa8c5da4c`); 3.1 to 3.3, G-03, G-06 | tree |
| `ComponentList.cpp:548` | out-of-line | `up/down` CHOOSE when `size() > 1` and no child names `up/down` (`:555-568`) | **L-01:** the icon key goes through `_()` (`:568`), so under French it is `haut/bas`, which `getIconTexture` does not know: a null icon and `Unknown help icon`; 3.16, G-04 under French | tree |
| `ComponentTab.cpp:320` | out-of-line | `left/right` SWITCH TAB when `size() > 1`, not when a child already names `left/right` (`:327-341`) | sound (fork `8927b1760`); 3.17, G-05 | tree |
| `ImageComponent.cpp:1057` | out-of-line | OK SELECT; no direction | sound | tree |
| `MenuComponent.cpp:531` | out-of-line | the grid's (`mGrid.getHelpPrompts()`) | sound: `ComponentGrid`'s rule | tree |
| `OptionListComponent.h:202` | inline | the popup's menu prompts plus BACK BACK | sound | tree |
| `OptionListComponent.h:636` | inline | `left/right` CHANGE whenever `!mMultiSelect` (`:639-640`), whatever the count; OK SELECT | L-13: a one-value option row offers CHANGE that changes nothing; upstream surface, recorded | tree |
| `RatingComponent.cpp:262` | out-of-line | OK `"add star"`; no direction | **L-23 (new):** a help label outside `_()`, untranslated under every language; upstream's line; a words lead (Q6), contained under rule 6 | tree |
| `SliderComponent.cpp:337` | out-of-line | `left/right` CHANGE always | sound: a slider at either end still moves the other way | tree |
| `SwitchComponent.cpp:165` | out-of-line | OK CHANGE; no direction | sound | tree |
| `TextEditComponent.cpp:390` | out-of-line | `up/down/left/right` MOVE CURSOR while editing, else OK EDIT (`:395-397`) | read at stage C against `input()`: whether up and down move the cursor in a single-line field | tree |
| `VideoComponent.cpp:347` | out-of-line | BACK labelled `_("SELECT")` (`:350`) | **L-24 (new):** the back button's prompt names SELECT; upstream's line; a words and input lead (Q3, Q6); reached only where a video component holds focus | tree |

Generated, asserted by `tools/t34-input.py`: 16 `input()` (14 `::input(InputConfig`, 2 inline), their keys read from each body; 14 `getHelpPrompts()` (12 out of line, 2 inline), each with its reading.

## The lifetimes

| Site | Shape | Who joins, drains or owns it | What it touches after | Disposition | proved |
| --- | --- | --- | --- | --- | --- |
| `OptionListComponent.h:96` | delete this | the popup, deleted from its own row's accept handler (a `std::function` inside `mMenu`'s row) | nothing: the handler's last statement (`:97`) | L-11: sound by the invariant (nothing above it touches the popup after the call returns); 3.19's ASan case at stage C | tree |
| `OptionListComponent.h:145` | delete this | the same, the second row template | nothing: the handler's last statement (`:146`) | L-11, as `:96` | tree |
| `OptionListComponent.h:158` | delete this | the popup, deleted from its own BACK button's callback: the button's `std::function` is destroyed while it runs (`es-code-traps.md:22`'s shape) | nothing: the lambda is `{ delete this; }` | L-11: sound only while `ButtonComponent` and the grids above it return without touching their members; 3.19 | tree |
| `OptionListComponent.h:195` | delete this | the popup, deleted from its own `input()` | nothing: `return true` (`:196`) | L-11, sound | tree |
| `TextEditComponent.cpp:39` | postToUiThread | `Window`'s post queue (T35's `postToUiThread`), drained later on the interface thread | raw `this` (`startEditing()`): a text edit destroyed before the post runs is a use after free | L-12: 3.20's case at stage C with the fakes' `Window.h`; a weak token the posts check is the pause's, with T33's `AppWindow` named | tree |
| `TextEditComponent.cpp:47` | postToUiThread | the same queue | raw `this` (`stopEditing()`) | L-12, as `:39` | tree |
| `VideoVlcComponent.cpp:91` | std::thread | a detached thread that releases the media player and deletes the `VideoContext` (`:93-94`) | VLC's thread may still be in `display` (`:53-61`) reading `ctx->component`, nulled at `:89` on the interface thread with no lock | L-10: a data race, and a call into a component being destroyed (`~VideoVlcComponent` -> `stopVideo` `:911`); upstream surface outside the lanes; recorded (G-10 `CANNOT`: no media) | tree |
| `VideoVlcComponent.cpp:95` | .detach( | the same thread, joined by nobody | `ctx`, after the release returns | L-10 | tree |
| `AsyncNotificationComponent.cpp:119` | read | `close()` writes `mClosing` and `mFadeTime` (`:119-120`) with no lock, from the holders' worker threads (`ThreadedCloudSync`, `ProxyCards`, `ThreadedBluetooth`, ...), while the interface thread's `update()` reads and writes both (`:267-299`; plain `bool` and `int`, h `:72`, `:74`); `mMutex` guards the text only (`:149`-`:196`) | - | **L-22 (new): a data race on the card's closing state**, in a lane surface; a host ThreadSanitizer case at stage C (a card double-free of `Window`, `close()` on one thread, `update()` on the other); a `bug` at stage D if it fires | tree |
| `AsyncNotificationComponent.cpp:123` | read | the card is owned by `Window` (`Window.h:123`, a vector of raw pointers) and deleted once it stops running (`Window.cpp:1242-1252`, T35's); every holder keeps the raw pointer `createAsyncNotificationComponent` returned (`Window.cpp:1152-1169`) | - | **§ 1 (b), T2 PC-1, the component's half:** the card promises a holder nothing after the window deletes it, and it cannot refuse a late `close()` or `updateText()` (no handle, no generation); the window's teardown order is T35's, the holders' half T18's and T20's; a handle the window keeps alive until the holder lets go is the pause's | tree |
| `MenuComponent.cpp:478` | read | `clearButtons()` (`:478-483`) deletes the button bar, whose buttons own their callbacks | - | `es-code-traps.md:22`'s rule restated beside the lines; no component-side guard exists at the pin, and the rule's `postToUiThread` with a weak handle is the callers' discipline | tree |
| `SwitchComponent.h:53` | read | the switch stores its callback by value | - | **§ 1 (c), T26 PL-27:** a page's lambda that captures a `shared_ptr` to the component that stores it makes a cycle the page's `onFinalize` must break; the type is not weak by design; LeakSanitizer over an extracted builder at stage C; a design ruling at the pause | tree |
| `OptionListComponent.h:658` | read | the option list stores its callback by value, called from `onSelectedChanged` (`:632-633`) | - | § 1 (c), as the switch's | tree |
| `OptionListComponent.h:310` | read | `input()` left: the callback, then `return true` (`:311`) | - | **§ 1 (d), T31 L-03 / #1243's invariant, kept:** a page that deletes the option list's owner inside the callback is safe only because nothing after the callback touches the component (`:311`, `:324`) | tree |
| `OptionListComponent.h:323` | read | `input()` right: the callback, then `return true` (`:324`) | - | § 1 (d), as `:310` | tree |
| `ImageGridComponent.h:91` | read | `clear()` and `resetGrid()` (#207) drop the entries and the tiles | - | **§ 1 (e), #1266's contract:** after `clear()` the grid holds no tile and no entry the cursor may name; T32's `s4-views.py` is the harness shape; the view's fix is T32's `1655e2f4c`; the contract is read at stage C against the two functions' bodies | tree |
| `WebImageComponent.cpp:243` | read | a stack `HttpReqOptions` (`:239`) handed by pointer to a heap `HttpReq` | - | L-21: sound, the constructor consumes the options before it returns (`HttpReq.cpp:119-123`, `:131-132`, `:172-176`, T21's) | tree |

Generated, asserted by `tools/t34-lifetimes.py`: 8 shape rows (`delete this` 4, `std::thread` 1, `.detach(` 1, `postToUiThread` 2), each with a disposition; 9 read rows, each cited line asserted to hold its code at the pin.

## The reads

| Site | Kind | What is read | Its writer while ES runs | A stale answer reads as | Disposition | proved |
| --- | --- | --- | --- | --- | --- | --- |
| `CarouselComponent.cpp:765` | exists | a system or game entry's `marquee`/`fanart`/`cartridge`/`mix` image (`:763`) | the scraper, writing media while ES runs | a cached miss draws the entry as text until a game launch or a restart clears the cache | L-20, recorded; upstream surface outside the lanes | tree |
| `ImageComponent.cpp:1232` | exists | the theme's `default` image path | a theme install or update (the theme installer) while ES runs | a cached miss leaves no default image until the theme reloads | L-20, recorded | tree |
| `VideoComponent.cpp:327` | exists | the theme's video `path` (a `{`-binding is taken without the check) | a theme install or update (the theme installer) while ES runs | a cached miss falls back to `defaultVideoPath` (`:330`) | L-20, recorded | tree |
| `VideoComponent.cpp:591` | exists | a `path` property, the bound `{game:video}` among them | the scraper, writing videos while ES runs | a video scraped mid-session reads as absent until a launch clears the cache (`es-native-ui.md:107`) | L-20, recorded; a frame only if a scrape fits the window (G-08's guest has no media: `CANNOT`) | tree |
| `VideoVlcComponent.cpp:605` | exists | `libvlc.dll` beside the executable | Windows-only: inside `#if WIN32` (`:592`), compiled to nothing on every image | - | dead on the images (Q7's gates) | tree |
| `VideoVlcComponent.cpp:639` | exists | `plugins/gui/libqt4_plugin.dll` | Windows-only: inside `#if WIN32` (`:592`), compiled to nothing on every image | - | dead on the images (Q7's gates) | tree |
| `WebImageComponent.cpp:81` | exists | the downloaded copy `mLocalFile`, at destruction when the cache lasts 0 s | `HttpReq` (tmp file, then `renameFile`, which erases the key: `FileSystemUtil.cpp:1457-1458`) | fresh: every writer of the path erases its key | sound | tree |
| `WebImageComponent.cpp:134` | exists | the cached copy `localFile`, before a request (`setImage`) | `HttpReq` for an earlier component; `removeFile` here (`:141`, `:150`) | a remembered miss here is erased when the request starts (`HttpReq.cpp:344` `removeFile(outputFilename)`) and when it lands (`:479` `renameFile`) | sound; 3.21's first half a candidate that PASSes at the pin (stage C proves it with the real `FileSystemUtil`) | tree |
| `WebImageComponent.cpp:190` | exists | `mLocalFile` after `REQ_SUCCESS` | `HttpReq`, `renameFile` into the path (`HttpReq.cpp:479`; the `copyFile` fallback `:501` erases too, `FileSystemUtil.cpp:1506-1507`) | fresh at the pin: the key cached as a miss at `:134` is erased by the writer before `:190` asks (L-09 answered) | L-09: sound, by the writer's erase; 3.21's case | tree |
| `WebImageComponent.cpp:228` | exists | the cache directory, before a request | `createDirectory` here (`:229`) | a cached miss calls `createDirectory` again: idempotent | sound | tree |
| `WebImageComponent.cpp:197` | getFileSize | the size of `mLocalFile` after a success | `HttpReq` | uncached (`stat64`, `FileSystemUtil.cpp:1319-1335`) | L-08: a 0-byte answer (the proxy's 204, #180) removes the file and returns; `mUrlToLoad` was cleared at `:244`, so the component never asks again for the page's life -- by design per `:191-196`; the disposition (re-ask on the next page build, or a word on the row) is the pause's | tree |
| `WebImageComponent.cpp:243` | HttpReq | `new HttpReq(mUrlToLoad, &options)`, the offline proxy's URLs with `X-RA-Store-Only` (`:240-241`, #199) | writes `mLocalFile` through `<path>.tmp` and `renameFile` (T21's `HttpReq.cpp:324-344`, `:479`) | - | L-21: the stack `HttpReqOptions` is consumed by the constructor before it returns; sound | tree |
| `BatteryIndicatorComponent.cpp:52` | texture | `:/network.svg` | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `ControllerActivityComponent.cpp:403` | texture | the theme's `imagePath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:406` | texture | the theme's `gunPath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:409` | texture | the theme's `wheelPath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:417` | texture | the theme's `networkIcon` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:429` | texture | the theme's `planemodeIcon` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ControllerActivityComponent.cpp:546` | texture | `mCurrentBatteryTexture`, a theme or resource battery glyph | a theme install, else none | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `GridTileComponent.h:152` | texture | a tile's background `path` (theme) | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `GridTileComponent.h:158` | texture | a tile's selected-background `path` (theme) | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `HelpComponent.cpp:185` | texture | a help icon from the theme's icon map | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `HelpComponent.cpp:203` | texture | a help icon from `ICON_PATH_MAP` (`:/help/...`) | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `ImageComponent.cpp:400` | texture | `mDefaultPath`, the theme's default | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `ImageComponent.cpp:408` | texture | `mPath`, any image a page shows by path | the scraper, the save-state writer, the sign-in's QR (T26 #1221), any file rewritten under its path | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | § 1 (a): the caller's half of #1263 -- the component asks by path once per `setImage` and holds the texture; a file rewritten under the same path while the texture lives is not re-read; the cache's half named for T36 (#683) | tree |
| `ImageComponent.cpp:446` | texture | `""`, an empty texture | - | - | recorded | tree |
| `NinePatchComponent.cpp:326` | texture | `mPath`, the frame image (theme or `:/frame.png`) | a theme install, else none | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `RatingComponent.cpp:158` | texture | `:/star_filled.svg` | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `RatingComponent.cpp:161` | texture | `:/star_unfilled.svg` | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `RatingComponent.cpp:220` | texture | the theme's `filledPath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `RatingComponent.cpp:226` | texture | the theme's `unfilledPath` | a theme install or update (the theme installer) while ES runs | a live texture under the same key is reused; a rewrite on disk under that path is not seen until the key is dropped (`TextureResource.cpp:100-131`, T36's) | recorded | tree |
| `RectangleComponent.cpp:38` | texture | `:/white.png` | none: a resource inside the image (`:/...`), read-only | - | recorded | tree |
| `VideoVlcComponent.cpp:479` | texture | `""`, the frame texture a video draws into | - | - | recorded | tree |

Generated, asserted by `tools/t34-reads.py`: 33 rows -- 10 `exists(` lines in 5 files, 0 of them uncached; 1 `getFileSize(`; 1 `new HttpReq(`; 21 live `TextureResource::get(` (the commented one at `VideoVlcComponent.cpp:77` excluded); every row has a disposition and every disposition a row.

## The words

**The 22 `_("` lines** (each msgid's French read from `locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the pin):

| Line | msgid -> French |
| --- | --- |
| `BusyComponent.cpp:35` | `WORKING...` -> `EN COURS…` |
| `CarouselComponent.cpp:359` | `CHOOSE` -> `CHOISIR` |
| `CarouselComponent.cpp:361` | `CHOOSE` -> `CHOISIR` |
| `ComponentGrid.cpp:546` | `CHOOSE` -> `CHOISIR` |
| `ComponentGrid.cpp:548` | `CHOOSE` -> `CHOISIR` |
| `ComponentGrid.cpp:550` | `CHOOSE` -> `CHOISIR` |
| `ComponentList.cpp:276` | `ENABLED` -> `ACTIVÉ`; `DISABLED` -> `DÉSACTIVÉ` |
| `ComponentList.cpp:568` | `up/down` -> `haut/bas`; `CHOOSE` -> `CHOISIR` |
| `ComponentTab.cpp:341` | `SWITCH TAB` -> `CHANGER D’ONGLET` |
| `DateTimeComponent.cpp:55` | `Unknown` -> `Inconnu` |
| `ImageComponent.cpp:1060` | `SELECT` -> `SELECT` |
| `OptionListComponent.h:158` | `BACK` -> `RETOUR`; `accept` -> `accepter` |
| `OptionListComponent.h:162` | `SELECT ALL` -> `TOUT SÉLECTIONNER`; `select all` -> `tout sélectionner` |
| `OptionListComponent.h:172` | `SELECT NONE` -> `AUCUN`; `select none` -> `aucun` |
| `OptionListComponent.h:205` | `BACK` -> `RETOUR` |
| `OptionListComponent.h:640` | `CHANGE` -> `CHANGER` |
| `OptionListComponent.h:642` | `SELECT` -> `SELECT` |
| `SliderComponent.cpp:340` | `CHANGE` -> `CHANGER` |
| `SwitchComponent.cpp:168` | `CHANGE` -> `CHANGER` |
| `TextEditComponent.cpp:395` | `MOVE CURSOR` -> `DÉPLACER LE CURSEUR` |
| `TextEditComponent.cpp:397` | `EDIT` -> `ÉDITER` |
| `VideoComponent.cpp:350` | `SELECT` -> `SELECT` |

**Player text outside `_()`:**

| Site | Text | Disposition | proved |
| --- | --- | --- | --- |
| `SliderComponent.cpp:282` | `"Auto"`, the AUTO sentinel's value text | **3.7:** neither `_()` nor the placeholder `AUTO` (`es-ui-style-guide.md:164`); upstream's line; the contained fix `_("AUTO")` with its French in the same commit; G-09 if an auto slider is reachable | tree |
| `RatingComponent.cpp:265` | `"add star"`, the rating's OK prompt | **L-23 (new):** a help label outside `_()`, English under every language; upstream's line; contained under rule 6 | tree |

**L-01:** `ComponentList.cpp:568`'s `_("up/down")` is an icon key, not a label: the catalog translates it (`haut/bas`), `InputConfig::buttonLabel` returns it unchanged (`es-core/src/InputConfig.cpp:353-366`, T35's), and `HelpComponent::getIconTexture`'s `ICON_PATH_MAP` has no such key (`:190-194`): a null icon and `Unknown help icon "haut/bas"` under French on every settings list. The fork's own key sites write it untranslated (`ComponentTab.cpp:341`, `ComponentGrid.cpp:546-550`). The contained fix drops the `_()`; whether the catalog's orphan `msgid "up/down"` stays is one of the four rows put to the pause.

**L-18, the up-casing formatters** (D-WORKFLOW-144: the brand is never upper-cased through a formatter; a reading, not a check -- a `tools/vocabulary-check` rule is proposed in § The leads):

| Site | What it upper-cases |
| --- | --- |
| `MenuComponent.cpp:205` | `addGroup`'s label |
| `MenuComponent.cpp:233` | `addWithDescription`'s label |
| `MenuComponent.cpp:236` | `addEntry`'s label |
| `MenuComponent.cpp:283` | `setTitle` |
| `MenuComponent.cpp:487` | `addButton`'s name |
| `ButtonComponent.cpp:73` | the button's text |

Generated, asserted by `tools/t34-words.py`: 22 `_("` lines in 12 files, 27 occurrences, 17 distinct msgids, each with a non-empty French `msgstr` at the pin; 2 player texts outside `_()`; 6 formatters; every cited line asserted to hold its code.

## The structure

- **Includes inside the 80:** 352 quoted lines over 91 distinct headers (most: `GuiComponent.h` 28, `Settings.h` 20, `ThemeData.h` 19, `LocaleES.h` 18, `utils/StringUtil.h` 17, `components/TextComponent.h` 13), 37 angle-bracket lines; **one to es-app:** AsyncNotificationComponent.cpp:12 `../../es-app/src/CloudText.h` (**L-07**: resolves only through `-I es-core/src` plus `../../`; the unit build links `CloudText.cpp` for `:144`; a `CloudText` that moves to es-core is T18's and T35's call).
- **Includes into the 80 from outside:** 274 lines in 112 files (es-app 215, es-core 58, tests 1); most-included: `MenuComponent.h` 32, `TextComponent.h` 24, `OptionListComponent.h` 22, `ComponentGrid.h` 21, `BusyComponent.h` 17, `ImageComponent.h` 16.
- **`es-core/CMakeLists.txt`:** every one of the 80 named exactly once and unconditionally: the 42 headers at `:49-90`, the 38 sources at `:186-223`; `if(` only at `:278` and `:287`.
- **The in-source platform gates** (13 lines): `GridTileComponent.cpp:11`, `NinePatchComponent.cpp:415`, `VideoComponent.cpp:22`, `VideoPlayerComponent.cpp:1`, `VideoPlayerComponent.h:1`, `VideoVlcComponent.cpp:17`, `VideoVlcComponent.cpp:485`, `VideoVlcComponent.cpp:592`, `VideoVlcComponent.cpp:668`, `VideoVlcComponent.cpp:779`, `VideoVlcComponent.cpp:836`, `VideoVlcComponent.cpp:874`, `VideoVlcComponent.cpp:875`. `VideoPlayerComponent.{cpp,h}` sit whole under `#ifdef _RPI_` and compile to nothing on every image; the `WIN32` blocks are dead on the images; D-WORKFLOW-209's disposition: a dead-end table removes nothing.
- **The non-ASCII byte:** `VideoVlcComponent.cpp:859`, 0x96 (a Windows-1252 en dash) in the comment `// use: vlc<0x96>long-help`; `git grep -P` sees it only under a C locale; an upstream hit, recorded and not fixed (`es-code-traps.md:60`); 0 in the 21 fork-modified files.

Generated, asserted by `tools/t34-includes.py`: 352 quoted include lines over 91 headers, 37 angle, 1 to es-app; 274 outside lines in 112 files; the 80 each named once in `es-core/CMakeLists.txt`, `if(` at 278 and 287; 13 gate lines; 1 non-ASCII line.

- **L-14:** `GridTileComponent.cpp:1043` is indented one level deeper than `:1042`, `ImageGridComponent.h:380-381` sit shallower than their block, and `ImageGridComponent.h:2`'s `#include <functional>` stands above the include guard (`:3`). Each reads as part of a block it is not in. A one-commit tidy if the pause opens it.
- **L-05:** the second `BUTTON_GRID_HORIZ_PADDING` (`guis/GuiTextEditPopupKeyboard.cpp:14`, T35's) is recorded in § The constants. It is not deleted here (`engineering-practices.md:576`).
- **`UntintedImageComponent`:** `es-app/src/guis/GuiMenu.cpp:6401` (T26's file), used for the QR at `:6425`. Whether `ImageComponent` (h `:76`) gains an untinted mode is the pause's question (§ 1 h).
- **The menu map:** `tools/es-menu-map-check --es-src <W> --ref 16dbac5211...` prints `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (rc 0, `stage-a/runs.txt`). The components have no page of their own, so this slice proposes no row. A stream that adds, moves or renames a row on a page it touches changes `docs/es-menu-map.md` in the same commit (D-UI-039).
- **The two lanes' `AsyncNotificationComponent.h` doubles** (`tests/app-unit/fakes/components/AsyncNotificationComponent.h`, T18's; T33's build names the same fake): a header change in this slice is named as a collision at the hand-back. The fakes are not this lane's to edit (§ 1 j).
- **The other lanes' ES tips inside the 80** (`stage-a/runs.txt`): T2 `55158d2a64`, T18 `d55235d4b3`, T20 `5c0ddaaeef`, T21 `3ae9610b0f`, T26 `757f5370ea`, T31 `95852f8736`, T32 `b52245036f`, and T33 now at `f802c55c62c1` (the brief read `dd86d7ce20a5`). Each diff against the pin is empty: no collision inside the 80 at stage A. The diffs run again at the hand-back.

## The merge debt

**None:** the merge base `cada856d86` (with `rocknix/master` `f6c542872e`; `bccd715707` is its parent and the commit the never-fetched `upstream/master` still names) is the base of 0 of the 14 upstream commits since it that touch the 80. 80 of 80 blobs are identical between the base and `rocknix/master`, and 59 of 80 between the pin and `rocknix/master`; the 21 that differ are the fork's 21. Batocera's eight commits since `1750dded8c` on ten files (seven of them fork-modified) are **not ROCKNIX's**: a reconciliation list for the integration, never a debt figure. They are `0806a0c5c`, `9dbd4b9bf` (the `setOpacity` guard, § 1 g: unreachable at the pin), `308221458`, `ac4baceaf`, `09f5f708f`, `b728ac99d`, `ab218fba1` and `ad104860f`. One overlaps by hunk: `09f5f708f` and the fork's `7dc8bf373` both rewrite `HelpComponent::updateGrid()` (base lines 121-125 and 139-151).

## The runs

Stage A's runs are in `stage-a/first-commands.txt` (the brief's § 1) and `stage-a/runs.txt` (the brief's § 5 block, each line's rc and wall time), and the membership block is in `stage-a/membership-block.txt`. Every expectation printed as the brief says, with one erratum (the gates line).

| Run | Figure (the command's own lines) | A FAIL would mean | Where |
| --- | --- | --- | --- |
| the membership block | `mine: 80 paths.txt: 80 equal: True`; `lines: 21984 reach: {'shipped': 80} tier: {'upstream-carried': 59, 'fork-own': 21} lang: {'c++': 38, 'c-header': 42}`; `fork-own lines: 9541`; `read lines: 21984` | the slice's membership moved since the brief | `stage-a/membership-block.txt` |
| the scope | 80; 38; 42; 0 | a path added or dropped | `stage-a/runs.txt` |
| the bases | `16dbac5211`, 0, `cada856d86`, `f6c542872e`, `b2ceb55a7e`, `1750dded8c`, 725, 14, 1, 15 | the ES worktree off the pin, or the refs moved | `stage-a/runs.txt` |
| the lines two ways | `wc -l 21971`; `grep -c 21984`; `no trailing newline: 13` | a file changed at the pin | `stage-a/runs.txt` |
| the fork's delta | `21 files changed, 591 insertions(+), 114 deletions(-)` three times; added 0; the 21 numstat rows; 33, 33, 0 | the tiers would need two tables | `stage-a/runs.txt` |
| upstream's delta | 0 rc=1; 0 rc=1; 59; 59; 80; 8; 10; 7 | merge debt this slice would owe | `stage-a/runs.txt` |
| the other lanes' tips inside the 80 | eight empty stat lines | a collision to name | `stage-a/runs.txt` |
| the strings | `_(" lines TOTAL 22 in 12 files`; 27; the per-file line | a string added or dropped | `stage-a/runs.txt`; `tools/t34-words.py` |
| the threads and lifetimes | `std::thread` 1 (`VideoVlcComponent.cpp:91`), `.detach(` 1 (`:95`), `delete this` 4 (`OptionListComponent.h:96 :145 :158 :195`), `postToUiThread` 2 (`TextEditComponent.cpp:39 :47`) | a lifetime the table misses | `stage-a/runs.txt`; `tools/t34-lifetimes.py` |
| the reads | `exists( lines TOTAL 10 in 5 files`; 10; uncached 0 rc=1; `WebImageComponent.cpp:5 WebImageComponent.h:2` (`HttpReq`, 7 lines in 2 files) | a read the table misses | `stage-a/runs.txt`; `tools/t34-reads.py` |
| the input | 12; `202 636`; 14; 0 rc=1 | a prompt or an input the table misses | `stage-a/runs.txt`; `tools/t34-input.py` |
| the constants | nine lines, `GuiTextEditPopupKeyboard.cpp:14`'s second copy among them | a house value defined twice in the 80 | `stage-a/runs.txt`; `tools/t34-constants.py` |
| the pixel constants | `MenuComponent.cpp:11`, `:13` (comments); `screen-relative 86`; fontScale 0 rc=1 | a pixel constant the table misses | `stage-a/runs.txt` |
| the includes | 352; 37; `AsyncNotificationComponent.cpp:12`; 274; 112; `named-0-times (or more than once): 0`; `278 287` | the structure moved | `stage-a/runs.txt`; `tools/t34-includes.py` |
| the in-source gates | 13 lines (the brief's comment says twelve; its § 4 Q7 list is the same 13, `VideoPlayerComponent.{cpp,h}:1` being two) | a unit compiled differently | `stage-a/runs.txt` |
| the non-ASCII byte | `git grep -P` 1 rc 0 (C locale); `VideoVlcComponent.cpp:1`; `files with a non-ascii byte: 1`; the comment form 1; `od -c` shows `226` (0x96) | a second byte, or one in a fork-modified file | `stage-a/runs.txt` |
| the French | `4929:msgid "SWITCH TAB"` with `CHANGER D’ONGLET`; `3708:msgid "up/down"` with `haut/bas`; `:2207`; `SliderComponent.cpp:282` | the catalog moved | `stage-a/runs.txt` |
| `es-untranslated` | `es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without` rc 0 (against `bccd715707`); `703 ... 703 with French, 0 without` rc 0 (against `cada856d86`) | a fork string without French | `stage-a/runs.txt` |
| the FAIL-at-pin lines | `74 75`; `486`; `568`; `208 210 212 213 251`; `74`; `81 190 197` | a lead's line moved | `stage-a/runs.txt` |
| the `setOpacity` callers | `745 1001 1009 1011 1012 1077 1397 1398`; 107 | a caller of the bar's `setOpacity` | `stage-a/runs.txt` |
| the menu map | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0; 989 lines | a screen unmapped | `stage-a/runs.txt` |
| the compile | `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2; plain `g++`: `.../es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory` rc 1; `pugixml root present` | a toolchain on the host, or a header found | `stage-a/runs.txt` |
| the removal check | empty against `00d490e654` and against `dff4fbd61d`; the ES diff against the pin empty | a change under `packages/`, `projects/` or `tools/`, or the ES tree off the pin | `stage-a/runs.txt` |
| the generators' drifts | each of the nine generators exit 1 on its constructed drift, rc 0 on the 80 | a table trusted before its check fired | `stage-b/generator-drifts.txt` |
| the stand-in syntax check over the 37 | pending: stage C (the fakes, the tenth `SDL_power.h`, the pugixml root) | a component's own C++ that does not parse | - |
| the unit build | pending: stage C (`tools/t34-build-tests.sh`, its `TOTAL:` line) | a pure seam's defect | - |

## The guest cycle

Not yet run. The window is asked for on #681 at stage B's end, with its plan and bound (`stage-b/window-plan.md`), and it runs only on the coordinator's grant there and in the host file's queue. The host file's 14:21 entry places T34's window after every M7 window.

## The streams

Written by the coordinator after stage D. The lane leaves this heading and the pause's dispositions.

## Positives

None yet. Each fix's positive is recorded here at stage E: its covering case's FAIL before and PASS after, or its frame `fix-walk-pending-image`.

## The #585 lines owed

One line per upstream-carried defect closed under rule 6, in the shape the lane writes, never sent. Owed only if a stream closes them; the candidates at stage B:

- **3.6**, `TextComponent.cpp:486`: the vertical marquee's limit subtracts the top padding twice (`mPadding.y() - mPadding.y()`), where `:351` and `:428` subtract top and bottom; with padding (0,10,0,30) the limit is 20 px too large.
- **3.7**, `SliderComponent.cpp:282`: the AUTO sentinel prints `"Auto"`, outside `_()` and not the placeholder `AUTO`.
- **L-01**, `ComponentList.cpp:568`: the `up/down` icon key goes through `_()`, so a translated catalog turns it into a key the help bar does not know.
- **L-23**, `RatingComponent.cpp:265`: the OK prompt `"add star"` is outside `_()`.
- **L-17**, `TextComponent.cpp:338` against `:350`: the auto height is measured at the full width and the text drawn at the padded one; the reproducer is written here at stage C.

The six fork candidates the brief names for the coordinator (none sent; `engineering-practices.md` § Consider contributing every applicable fix upstream): `aa8c5da4c` (the grid's `canMoveCursor`, the strongest), `7c7ffab43` (the row measured from the fonts), `b6eb26980`, `8927b1760` with `f1ae6bc25` as a pair (the strip as a focus stop), `7dc8bf373` only after the RTL reconciliation (the help bar's fit), and `2088eadb9` (the tile label's multi-line).

## What T35 to T37 inherit

Written, not tested here (the brief's § 5 item 3):

1. **The provenance table:** § Coverage, 0 / 21 / 59 against `bccd715707` and `cada856d86`, which agree.
2. **The layouts table:** § The layouts, the 19 font-height reads with the brief's eight, and the 10 size rows.
3. **The constants table:** § The constants, the seven house values with their one definition and readers, and the 15 pixel constants.
4. **The input table:** § The input, the 16 `input()` and the 14 `getHelpPrompts()` with their conditions.
5. **The lifetimes table:** § The lifetimes, with the card's closing race (L-22) and its window-side half for T35.
6. **The reads table:** § The reads, 33 rows with their writers.
7. **The `components-tests` build recipe:** the doubles, the tenth fake `SDL_power.h` and the pugixml root, in `tools/t34-build-tests.sh` at stage C.
8. **The `setOpacity` callers' read, for T35:** § The leads' ruling (g).
9. **The texture-cache contract, for T36:** § The reads, `ImageComponent.cpp:408` (a path is a cache key for the texture's lifetime).
10. **The es-core to es-app include's disposition:** § The structure, L-07.


## The first reader's 03-retrospective.md (whole)

# Retrospective: M6.P2 T34, EmulationStation's core components (#681)

What the 80 paths were for, how the fork's 33 commits changed them, and where the seams are. This is the audit's retrospective (code-auditor Phase 3), not the lane's mini-retro, which is stage G's.

## 3.1 What the components are for

Every page the player sees is built from these: the menu and its button bar, the row list and its rows, the tab strip, the cell grid, the help bar, the progress card, the images and the text. The fork's lanes (D-UI-079) run through ten of them. The other surfaces (video, carousel, rating, date editor, text list, glyphs) are upstream's, read for cost and brittleness and left as upstream has them.

## 3.2 What the fork changed, and what drifted

The fork's 33 commits (2026-08-28 to 2026-10-01) are mostly fixes found on frames:
- the button gap (D-UI-012);
- the strip as a focus stop (D-UI-021, #65, #325);
- the help bar that offers only a direction that moves (D-UI-034, #115);
- the dim that survives the list's re-tint (#182);
- the row measured from its fonts (#241);
- the help bar's fit (#210);
- the image's aspect and turn (#243, #245, #250);
- the card's candidate rows (D-UI-035), opacity (D-UI-016) and width.

Little drifted from what each fix claimed. The one claim the tree contradicts is `MenuComponent.cpp:7-13`'s "the one place", which T35's keyboard popup does not honour (PL-16).

## 3.3 What none of the fixes noticed

- The card's `close()` is called from worker threads and was never made thread-safe; only its text is locked (PL-01).
- Two upstream lines put player text outside `_()` (PL-09, PL-10).
- One puts an icon key inside it (PL-04).
- Upstream's `TextComponent` keeps #48's measurement root, which `GuiMsgBox` works around and nothing else does (PL-08).

## 3.4 What the record says about catches

Each fork fix was caught on a frame, by a person or a walk, after it shipped once. No unit case has ever linked a component: the only component in a test tree is a double. The 34 seam cases this slice owes would be the first.

## 3.5 The seams

The floor's 3.1 to 3.34 (`02` § The leads), each a pure function a case can pin: the grid's cursor scan, the row shares, the marquee limit, the slider's text, the carousel's fast move, the help bar's fit, the card's chooser width, the image's fit and turn, the dim, the bar's widths. The lifetimes need sanitizers rather than cases: the popup's `delete this`, the field's posts, the card's race.


## The first reader's 04-analysis.md (whole)

# Analysis: M6.P2 T34, EmulationStation's core components (#681)

## Executive summary

The 80 paths of `es-core/src/components/**` at the pin `16dbac5211` were read whole: 21 modified by the fork (+591/-114 over 33 commits) and 59 carried byte-identical from ROCKNIX's master. There is no merge debt: 0 of the 14 upstream commits since the base touch the 80. `02-forward-audit.md` tables every layout read, house constant, input, lifetime, read and string, each table generated and asserted by a script under `tools/` that was seen to fail on a constructed drift. The guest window (19:28 to 19:39) confirmed on the image that the house constants hold: the button bar's gap at 14 px and 28 px, and the dim at 0x50.

**26 punch items, none Critical or High, 5 Medium.** The five Medium items:
- **PL-01:** a data race on the progress card's closing state, in a lane surface.
- **PL-02:** the card's lifetime against its holders once the window deletes it (T2 PC-1's component half).
- **PL-03:** the text field's two raw-`this` posts.
- **PL-04:** the `up/down` icon key through `_()`. It did not reproduce on the image.
- **PL-05:** a tabbed page's help bar that carried no component prompt on the image, unread at the pin.

The rest are Low: three contained upstream fixes under rule 6, four register-row rulings the brief expects, and recorded upstream surfaces.

**What this analysis does not yet carry:**
- **The unit build:** `tools/t34-build-tests.sh` and the 34 seam cases, with the seven FAIL-at-pin pairs.
- **The sanitizer cases** for PL-01 and PL-03.
- **The stand-in syntax check** over the 37 sources.

Each proof below is `tree` or `guest` until those run. They are named as owed in § Coverage boundary and on #681.

## Acceptance-criteria scorecard

#681's 21 criteria, as they stand at the stage-D pause:

| # | Criterion (short) | State at the pause | Evidence |
| --- | --- | --- | --- |
| 1 | the audit folder's files and directories | partial: `stage-d/`, `stage-e/` owed | `ls` at the hand-back |
| 2 | the lint at both phases and with `--issue` | pre-issue PASS owed this stage; resolution at close | `tools/lint-audit-artifacts` |
| 3 | `review-plan.json` and the two provenance files | after the seat this stage | `second-opinions/` |
| 4 | the punch-list issue at Phase 7 | the issue at stage D; outcomes at stage F | `05` |
| 5 | the four header fields | `reviewed-at:` at the hand-back | #681's body |
| 6 | `01` § Scope with the block's lines | met | `01-research-notes.md` |
| 7 | the coverage table's 80 rows | met | `02` § Coverage |
| 8 | `02` § The runs with both counting rules | met | `02` § The runs |
| 9 | the generated sections, each drift-proven | met | `stage-b/generator-drifts.txt` |
| 10 | § The layouts' rows and the reproducer | rows met; the #585 reproducer owed (3.5) | `02` § The layouts |
| 11 | § The constants' rows and frames at both sizes | met for the bar and the dim; the card's frame CANNOT (G-02) | `02`, `guest-cycle/` |
| 12 | § The merge debt's one line | met | `02` § The merge debt |
| 13 | § The runs: every command, the unit build's `TOTAL:` | the unit build owed | `02` § The runs |
| 14 | § The guest cycle | the window's record; `02` § The guest cycle filled at stage E's recompose | `guest-cycle/`, #681 START and RETURN |
| 15 | `00` shows no build, fetch, device or account | met so far | `00-running-log.md` |
| 16 | `04` answers Q1 to Q7; bugs with their three lines | this file; bugs filed at stage D | this file |
| 17 | every proof's `proved:` cell; § What T35 to T37 inherit | met in `02`; owed cells marked `pending:` | `02` |
| 18 | the retro | stage G | - |
| 19 | the map rows | no row proposed; the checker's line quoted | `02` § The structure |
| 20 | the five checkers and the ES pre-push test | at the hand-back | - |
| 21 | the unit build's `TOTAL:` line with 0 failed | owed | - |

## Risk assessment

- **The card's closing race (PL-01)** sits under every automatic sync and every achievements card. Its likely symptom is a fade that starts late, not a crash, but it is undefined behaviour. The fix is small and the covering case is a host ThreadSanitizer run.
- **The holders' raw pointers (PL-02)** are the larger risk. A worker that outlives its card writes into freed memory. The component cannot refuse the call; only a handle the window keeps alive can. That is a design ruling across T34, T35, T18 and T20, so it waits for the pause.
- **The image is M7's composition, not the pin.** PL-04 did not reproduce there, and PL-05 appeared only there. Neither is a finding about the pin until the pin's code is read for it.
- **No proof yet runs the components' own code.** Every case is owed to the unit build. Until it runs, a `tree` proof is a reading, and the seven FAIL-at-pin leads are expectations.

## Coverage boundary

- **Read:** all 80 paths at the pin, whole; their neighbours (`Window.cpp`, `HttpReq.cpp`, `FileSystemUtil.cpp`, `Font.cpp`, `GuiTextEditPopupKeyboard.cpp`, `GuiMenu.cpp`) read only where a row cites them, never edited.
- **Run on the host:** the membership block, the brief's § 5 block, the nine generators, the packet's scan.
- **Run on the guest:** G-01, G-03, G-04, G-05, G-09 and G-11, at 640x480 and 1280x800.
- **Not run:**
  - the unit build, and with it every 3.x case;
  - the sanitizer cases (3.19, 3.20, PL-01's);
  - the stand-in syntax check over the 37;
  - G-02, G-06, G-07, G-08 and G-10 (`CANNOT`, each with its reason on #681).
- **Out of scope:** the neighbours' own defects, named for their owners in `05`.

## The questions

### Q1 Layout: computed from what it last produced, or from a moving number

The rule's shape survives in two places: L-03's shares (PL-07), and the font height every layout reads before the tallest glyph has drawn (PL-17, 13 layout reads in § The layouts, the brief's eight among them). #241's self-feeding row is fixed: `layoutRows` measures from the fonts. L-17 (PL-08) is a different shape, measured at one width and drawn at another, and 3.6 (PL-06) is a one-token slip in the same file. G-05's reopened page matched its first paint on the image because the menus had already drawn, so the moving number is not shown there.

### Q2 The house constants

On the image the bar's gap is 14 px at 640 and 28 px at 1280 (0.022 W), and the dim's ratio is 0.314 (0x50). The card's width and position are read in the tree (0.9 W, centred); its frame is `CANNOT` this window (G-02). The open items are L-04's overhang (PL-14), L-06's 20 px inset (PL-15), and L-05's second copy against the comment's "one place" (PL-16). L-19's floor is dead text, recorded.

### Q3 Input and the help bar

`canMoveCursor` decides the grid's prompts, so D-UI-034 holds in the tree. The strip is a focus stop on the image: four frames and the wrap. The open items:
- PL-04: the icon key through `_()`;
- PL-05: the tabbed page's empty bar, on the image;
- PL-11: BACK labelled SELECT;
- PL-12: the unstated cast;
- PL-19: directions offered by type.

PL-24, the carousel's negative count, is 3.8's to decide.

### Q4 Lifetime

The four `delete this` in the option list are sound by T31's invariant, which is kept (§ 1 d). The card's race (PL-01), its holders (PL-02, § 1 b) and the field's posts (PL-03) are the defects. The VLC release thread (PL-18) is recorded outside the lanes. The callback types (PL-22, § 1 c) and the grid's contract after `clear()` (§ 1 e) are written in § The lifetimes for the pause.

### Q5 Reads and the network

All ten `exists(` reads are cached. L-09's feared miss is sound at the pin: `HttpReq`'s `removeFile` and `renameFile` erase the cached key. L-20's media reads are recorded. L-08's never-again badge (PL-13) is by design and goes to the pause. § 1 (a)'s contract is written: a path is a cache key for a texture's lifetime, and the cache's half belongs to T36.

### Q6 The words

The 17 msgids each have French at the pin. Three strings sit outside `_()` or the vocabulary: `"Auto"` (PL-09), `"add star"` (PL-10) and the blank date (PL-25). The brand's guard is a reading, not a check (PL-23).

### Q7 The structure and the merge debt

There is no merge debt. Batocera's eight commits are a reconciliation list, with the one `updateGrid()` overlap. The es-app include (PL-21), the 13 gates and the one non-ASCII byte are recorded. The `setOpacity` guard is unreachable at the pin (§ 1 g). `UntintedImageComponent`'s lift is a question for the pause (PL-26). The tidy is PL-20.

## The take-up table (brief § 2), each row disposed

| Row | Disposition | Where |
| --- | --- | --- |
| T32 PL-07 / #1263 | the caller's half stated: one ask per `setImage`, a live texture reused | `02` § The reads, `ImageComponent.cpp:408` |
| T2 PC-1 | the component's half: PL-02 | `05` |
| T26 L-02 / #1221 | the contract stated beside #1263's row | `02` § The reads |
| T26 PL-27 | PL-22 | `05` |
| T31 L-03 / #1243 | the invariant kept | `02` § The lifetimes, `OptionListComponent.h:310`, `:323` |
| T31, #63, #65 | the component half of #65 shown on the image (G-05); the pages are T31's | `guest-cycle/g05-*` |
| T31 L-26 / #1245 | read; the checker proposal is the coordinator's | - |
| T31 retro, T26; `es-code-traps.md:22` | the rule restated beside `clearButtons` | `02` § The lifetimes |
| T32 S4 / #1266 | the grid's contract after `clear()` | `02` § The lifetimes |
| T32 PL-16, T31 PL-26 | not reached on the image (no grid theme, G-08) | `guest-cycle/g01-identity.txt` |
| T32 PL-10 / #1265 | read; the views' fix | - |
| #585 / #48 | PL-08, the reproducer owed | `05` |
| #182 | the dim measured on the image | `guest-cycle/g04-1-cloud-hub-en.png` |
| #325 | the wrap shown (G-05) | `guest-cycle/g05-4-after-up-up.png` |
| #210 | the bar's fit; read | `02` § The layouts |
| #27 | read; no grid theme | - |
| #243 | 3.22, 3.23 owed | `02` § The leads |
| #157 | read | - |
| #1112 | read-only context | - |
| T21 L-11 / #1199 | read; `SystemConf`'s | - |
| T21 PL-26 / #1192 | the field's masking named for T35's pause | - |
| T18's double | a collision named at the hand-back | `02` § The structure |
| T20's SCAN GAMES row | 3.4 owed | `02` § The leads |
| T31's func-form rows | the per-frame cost, priced in the retro | - |
| `es-ui-style-guide.md:202` | read as it stands | - |
| #585 | the lines owed | `02` § The #585 lines owed |

## Renovation face

### Q1 Modernize

Nothing to modernize for its own sake. The fork's 21 files follow the house patterns, and the 59 are upstream's, kept as upstream has them (D-UI-079).

### Q2 Standards

The house constants hold on the image. The standards gaps are words outside `_()` (PL-09, PL-10), pixel constants where fractions belong (PL-15, and the table in `02`), and the brand's guard by reading (PL-23).

### Q3 Bugs

PL-01, PL-03 and PL-04 are the bug candidates. Each is filed at stage D with its trace, its `Already written:` line (nothing inherited: a component writes no file) and its VM line, once its case is seen to FAIL. PL-05 and PL-24 wait on a read and a case.

### Q4 Package currency

None: the slice carries no package. ROCKNIX's master is level for the 80, and batocera's eight are a reconciliation list.

### Q5 Efficiency

`ComponentList::render` re-tints every element every frame, and three func-form rows force per-frame updates. Their price on the guest is the retro's, and the window gave no frame time to read: `CANNOT` with the harness's reason.

### Q6 Dead ends

`VideoPlayerComponent` compiles to nothing on every image (`_RPI_`), the `WIN32` blocks are dead, and `ScrollableContainer.cpp:69` computes a value it never uses. Recorded only: a dead-end table removes nothing (D-WORKFLOW-209).

### Q7 Clarity and structure

The es-app include (PL-21), the misleading indentation (PL-20), the cast's unstated invariant (PL-12) and the "one place" claim (PL-16).

## Instruction File Recommendations

- `es-code-traps.md` could carry the card's rule: a component a worker holds by raw pointer must not be written from that worker without the card's lock (PL-01, PL-02). Proposed for the coordinator; not written by this lane.
- `generic-x64-vm-testing.md` could say that at 640x480 a menu page draws no help bar, so a help-bar proof belongs at 1280x800. This window spent G-04's French half learning that.

## Second opinion

Depth **independent**: one seat, `gpt` (`openai/gpt-6-astra`, effort `max`), a probe and one refutation over `second-opinions/t34-packet.md` (`review-plan.json`). The outcome is recorded here after the refutation returns.

## Quality self-check

- Every count in `02` is a generator's or a command's own line. None is summed by hand.
- Every `tree` proof cites its lines at the pin. Every guest reading names its frame and is labelled `image`.
- The owed proofs are named, not implied: the unit build, the sanitizer cases, and the syntax check.
- The scorecard above has no total row; its states are words, not sums.


## The first reader's 05-punch-list.md (whole)

# Punch list (Phases 5 and 6) — M6.P2 T34, EmulationStation's core components (#681)

Written by `tools/t34-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 layout, Q2 constants, Q3 input, Q4 lifetime, Q5 reads, Q6 words, Q7 structure); `04` § Renovation face maps them to the plan's seven. Every item is Open until the stage-D pause disposes it.

## PL-01: The progress card's close() writes its closing state unlocked from the holders' threads

- **Severity:** Medium; **category:** Lifetime; **question:** Q4
- **Source finding:** L-22 (new)
- **Lines at the pin:** `AsyncNotificationComponent.cpp:117-121`, `:261-299`; h `:72`, `:74`
- **Owner:** T34 (a lane surface); the holders T18's and T20's
- **What is wrong:** `close()` sets `mClosing` and `mFadeTime` from the cloud and achievements worker threads while the interface thread's `update()` reads and writes both, with no lock and no atomic (`mMutex` guards only the text). A data race is undefined behaviour; in practice a fade that starts late or twice.
- **Proposed disposition:** a `bug`; the two members atomic, or `close()` under `mMutex` with `update()` reading under it; a ThreadSanitizer case over an extracted card first (stage E's covering case)
- **proved:** tree

## PL-02: The card promises a holder nothing once the window deletes it, and cannot refuse a late call

- **Severity:** Medium; **category:** Lifetime; **question:** Q4
- **Source finding:** § 1 (b), T2 PC-1
- **Lines at the pin:** `AsyncNotificationComponent.cpp:123-127`; `Window.cpp:1152-1169`, `:1242-1252` (T35's)
- **Owner:** T34 (the component's half); `Window` T35's; the holders T18's and T20's
- **What is wrong:** Every holder keeps the raw pointer `createAsyncNotificationComponent` returned; `Window::update` deletes a card once it stops running; a holder's `close()` or `updateText()` after that is a use after free the card cannot detect.
- **Proposed disposition:** a design ruling at the pause: a handle the window keeps alive until the holder lets go (the component's half), with `Window`'s teardown order T35's
- **proved:** tree

## PL-03: The text field posts raw `this` to the interface queue on focus

- **Severity:** Medium; **category:** Lifetime; **question:** Q4
- **Source finding:** L-12
- **Lines at the pin:** `TextEditComponent.cpp:39`, `:47`
- **Owner:** T34; `Window::postToUiThread` T35's; `AppWindow` T33's
- **What is wrong:** `onFocusGained` and `onFocusLost` post `[this] { startEditing(); }` and `stopEditing()`; a field destroyed before the post runs is a use after free.
- **Proposed disposition:** a weak token the posts check; 3.20's case (post, delete, drain) with the fakes' `Window.h` as the covering case
- **proved:** tree

## PL-04: The `up/down` help icon key goes through `_()`

- **Severity:** Medium; **category:** Words; **question:** Q3
- **Source finding:** L-01, 3.16
- **Lines at the pin:** `ComponentList.cpp:568`; `HelpComponent.cpp:176-200`; fr po `:3708-3709`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** Under a catalog that translates `up/down` (French: `haut/bas`) the list's CHOOSE prompt carries a key `getIconTexture` does not know: a null icon and `Unknown help icon`. Not reproduced on the image at 1280x800 (one CHOISIR with its icon, 0 log lines, the catalog carrying `haut/bas`): something between the list and the bar hides it there (L-25's neighbour).
- **Proposed disposition:** drop the `_()` (a contained fix, a #585 line); 3.16 as the covering case; the catalog's orphan `msgid` is a row for the pause
- **proved:** tree; guest (image): not reproduced

## PL-05: The tabbed SCRAPEUR page's help bar carries no component prompt

- **Severity:** Medium; **category:** Input; **question:** Q3
- **Source finding:** L-25 (new, the guest)
- **Lines at the pin:** `ComponentTab.cpp:320-345`; `MenuComponent.cpp:531-533`; `ComponentGrid.cpp:519-553`
- **Owner:** T34 (if the pin's components drop them); `Window`'s bar T35's
- **What is wrong:** At 1280x800 the bar reads only FERMER and RETOUR, pixel-identical with a row focused and with the strip focused: no SWITCH TAB, no row prompt. Shown on the image only; whether the pin's tabbed `MenuComponent` loses its children's prompts, or the image's composition does, is unread.
- **Proposed disposition:** read at the pin before a fix (the grid's prompt collection with a tab strip cell; when `updateHelpPrompts` runs on a focus move inside the menu); a `bug` only if the pin's code drops them
- **proved:** guest (image)

## PL-06: The vertical marquee's limit subtracts the top padding twice

- **Severity:** Low; **category:** Correctness; **question:** Q1
- **Source finding:** 3.6
- **Lines at the pin:** `TextComponent.cpp:486`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** `mSize.y() - mPadding.y() - mPadding.y()` where `:351` and `:428` take `.y()` and `.w()`: with padding (0,10,0,30) the limit is 20 px too large, so a text that overflows by less never scrolls.
- **Proposed disposition:** the one token (`.w()`), a #585 line; 3.6's case FAIL then PASS
- **proved:** tree

## PL-07: A two-line row's shares do not sum to 1 when its fonts differ

- **Severity:** Low; **category:** Layout; **question:** Q1
- **Source finding:** L-03, 3.4
- **Lines at the pin:** `MultiLineMenuEntry.cpp:74-75`
- **Owner:** T34 (upstream's formula, moved by the fork's `48d43c0fb`)
- **What is wrong:** `th*0.9/h + sh*1.1/h` is 1 only when `th == sh`: a taller Text font leaves a gap, a taller TextSmall overflows by `0.1*(sh-th)/h`.
- **Proposed disposition:** a pause ruling (a register row): shares that sum to 1, or the gap recorded; 3.4's case
- **proved:** tree

## PL-08: The auto height is measured at the full width and drawn at the padded one

- **Severity:** Low; **category:** Layout; **question:** Q1
- **Source finding:** L-17, #48
- **Lines at the pin:** `TextComponent.cpp:338` against `:350`; `:483`
- **Owner:** T34 (upstream's file)
- **What is wrong:** A wrap that falls between the two widths paints a line the height never budgeted; `GuiMsgBox` works around it, nothing else does.
- **Proposed disposition:** a pause ruling (a register row): the root fixed in the component (it re-heights every padded auto-height text) or recorded with the reproducer for #585; 3.5's case
- **proved:** tree

## PL-09: The slider's AUTO value reads `Auto`, outside `_()`

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** 3.7
- **Lines at the pin:** `SliderComponent.cpp:282`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** Neither translated nor the placeholder `AUTO` the style guide names.
- **Proposed disposition:** `_("AUTO")` with its French in the same commit, a #585 line; 3.7's case
- **proved:** tree

## PL-10: The rating's OK prompt `add star` is outside `_()`

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-23 (new)
- **Lines at the pin:** `RatingComponent.cpp:265`
- **Owner:** T34 (upstream's line, rule 6)
- **What is wrong:** English under every language.
- **Proposed disposition:** `_()` with its French in the same commit, a #585 line
- **proved:** tree

## PL-11: A focused video component labels BACK as SELECT

- **Severity:** Low; **category:** Input; **question:** Q3
- **Source finding:** L-24 (new)
- **Lines at the pin:** `VideoComponent.cpp:347-351`
- **Owner:** T34 (upstream's line)
- **What is wrong:** The help bar names the back button's action SELECT.
- **Proposed disposition:** recorded; contained under rule 6 if the pause opens it
- **proved:** tree

## PL-12: `setCursorToButton` casts any button grid to `ComponentGrid` on an unstated invariant

- **Severity:** Low; **category:** Structure; **question:** Q3
- **Source finding:** L-15
- **Lines at the pin:** `MenuComponent.cpp:492-515`; `GuiMenu.cpp:591` (T26's)
- **Owner:** T34
- **What is wrong:** `setButtonGrid` accepts any `GuiComponent` (the MAIN MENU hands it a text); the static cast is safe only because `mButtons` is empty there and the index guard returns first.
- **Proposed disposition:** a `dynamic_pointer_cast` with a null check, the invariant written beside `MenuComponent.h:53-56`
- **proved:** tree

## PL-13: A web image answered with 0 bytes is never asked for again on that page

- **Severity:** Low; **category:** Reads; **question:** Q5
- **Source finding:** L-08, 3.21
- **Lines at the pin:** `WebImageComponent.cpp:197-200`, `:244`
- **Owner:** T34
- **What is wrong:** By design per `:191-196`; the badge stays blank for the page's life with no word on the row.
- **Proposed disposition:** a pause ruling: a re-ask on the next page build, or a word on the row; `tools/ra-ui-test`'s fixture shape
- **proved:** tree

## PL-14: A button bar wider than its cell overhangs the menu

- **Severity:** Low; **category:** Constants; **question:** Q2
- **Source finding:** L-04, 3.26
- **Lines at the pin:** `MenuComponent.cpp:543-562`; `ButtonComponent.cpp:10`
- **Owner:** T34; the wide pages T26's and T31's
- **What is wrong:** The bar is `sum(text + max(12, 0.014 W)) + N * 0.022 W` and its cell does not resize it; five 128 px buttons at 640 overhang both edges.
- **Proposed disposition:** a pause ruling: a bar that fits its cell, or the pages' labels; 3.26's arithmetic per page
- **proved:** tree

## PL-15: Two pages read a 20 px row inset at every panel

- **Severity:** Low; **category:** Constants; **question:** Q2
- **Source finding:** L-06
- **Lines at the pin:** `ComponentList.cpp:11`, `:491-494`
- **Owner:** T34 (upstream's constant); the pages T26's and T31's
- **What is wrong:** `rowInset()` exports `TOTAL_HORIZONTAL_PADDING_PX` 20 to two fork pages: 3.1 % of 640, 1.0 % of 1920.
- **Proposed disposition:** a pause ruling (a register row): a screen fraction under D-UI-012's family, or upstream's constant kept
- **proved:** tree; guest (image) at both sizes

## PL-16: The bar's gap is claimed to be defined in one place; the keyboard popup keeps a second

- **Severity:** Low; **category:** Constants; **question:** Q2
- **Source finding:** L-05
- **Lines at the pin:** `MenuComponent.cpp:7-13`; `GuiTextEditPopupKeyboard.cpp:14` (T35's)
- **Owner:** the comment T34's; the popup T35's
- **What is wrong:** Two definitions, one claim.
- **Proposed disposition:** the comment corrected or the claim kept at the pause; the second copy is not deleted here
- **proved:** tree

## PL-17: Rows and fields are sized from a font height that grows as glyphs rasterise

- **Severity:** Low; **category:** Layout; **question:** Q1
- **Source finding:** L-02, L-16
- **Lines at the pin:** `MultiLineMenuEntry.cpp:55`, and the 12 other layout reads in § The layouts
- **Owner:** T34; `Font.cpp` T36's
- **What is wrong:** A size taken before the tallest glyph has drawn is a few px short. G-05's reopened pair was identical on the image because the menus had already drawn.
- **Proposed disposition:** a pause ruling: a rasterise-first in the component, or recorded
- **proved:** tree; guest (image): no difference shown

## PL-18: The VLC release thread nulls `component` without a lock while VLC's thread reads it

- **Severity:** Low; **category:** Lifetime; **question:** Q4
- **Source finding:** L-10
- **Lines at the pin:** `VideoVlcComponent.cpp:53-61`, `:84-96`, `:911`
- **Owner:** T34 (upstream surface, outside the lanes)
- **What is wrong:** A data race, and a `display` call into a component being destroyed.
- **Proposed disposition:** recorded (G-10 `CANNOT`: no media); a contained fix only if the pause opens it
- **proved:** tree

## PL-19: A carousel and an option row offer a direction by type, whatever their count

- **Severity:** Low; **category:** Input; **question:** Q3
- **Source finding:** L-13
- **Lines at the pin:** `CarouselComponent.cpp:354-361`; `OptionListComponent.h:636-643`
- **Owner:** T34 (upstream surfaces)
- **What is wrong:** A one-entry carousel offers CHOOSE; a one-value option row offers CHANGE.
- **Proposed disposition:** recorded
- **proved:** tree

## PL-20: Indentation and an include outside the guard read as blocks they are not in

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-14
- **Lines at the pin:** `GridTileComponent.cpp:1043`; `ImageGridComponent.h:2`, `:380-381`
- **Owner:** T34
- **What is wrong:** Cosmetic; misleads a reader.
- **Proposed disposition:** a one-commit tidy if the pause opens it
- **proved:** tree

## PL-21: es-core includes es-app's `CloudText.h`

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-07
- **Lines at the pin:** `AsyncNotificationComponent.cpp:12`
- **Owner:** T34 (the line); `CloudText` T18's; the CMake T35's
- **What is wrong:** Resolves only through `-I es-core/src` plus `../../`; es-core does not build alone.
- **Proposed disposition:** recorded; a `CloudText` that moves to es-core is T18's and T35's call
- **proved:** tree

## PL-22: The switch's and the option list's callbacks are stored by value, not weak by design

- **Severity:** Low; **category:** Lifetime; **question:** Q4
- **Source finding:** § 1 (c), T26 PL-27
- **Lines at the pin:** `SwitchComponent.h:53`; `OptionListComponent.h:658`
- **Owner:** T34; the pages' clearing T26's and T31's
- **What is wrong:** A page's lambda capturing a `shared_ptr` to the component that stores it makes a cycle only the page's `onFinalize` breaks.
- **Proposed disposition:** a design ruling at the pause; LeakSanitizer over an extracted builder
- **proved:** tree

## PL-23: The brand is kept lowercase by reading, not by a check

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-18
- **Lines at the pin:** `MenuComponent.cpp:205`, `:233`, `:236`, `:283`, `:487`; `ButtonComponent.cpp:73`
- **Owner:** the coordinator (a tool rule)
- **What is wrong:** Six formatters upper-case every label they see; no fork label passes the brand through them at the pin.
- **Proposed disposition:** a `tools/vocabulary-check` rule proposed (the brand inside those builders' arguments)
- **proved:** tree

## PL-24: The carousel's fast move can hand `listInput` a negative count

- **Severity:** Low; **category:** Correctness; **question:** Q3
- **Source finding:** 3.8
- **Lines at the pin:** `CarouselComponent.cpp:74-90`, `:113`, `:119`; `IList.h:376-400`
- **Owner:** T34 (upstream surface)
- **What is wrong:** Size 3, cursor 0, page up: `count = -10`, one `+= sz` gives `-7`; whether `listInput(-7)` lands in `[0, sz)` for every loop type is 3.8's case.
- **Proposed disposition:** 3.8's case at stage C decides; a `bug` only if it FAILs
- **proved:** tree

## PL-25: An unset date reads blank, not `<NOT SET>`

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** 3.13
- **Lines at the pin:** `DateTimeEditComponent.cpp:256-257`
- **Owner:** T34 (upstream surface)
- **What is wrong:** `getTime() == 0` returns `""`.
- **Proposed disposition:** a style question for the pause
- **proved:** tree

## PL-26: Whether `ImageComponent` gains the untinted mode the fork wrote as a subclass

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** § 1 (h)
- **Lines at the pin:** `GuiMenu.cpp:6401` (T26's); `ImageComponent.h:76`
- **Owner:** the pause
- **What is wrong:** `UntintedImageComponent` lives in a page file; every untinted image needs the same subclass.
- **Proposed disposition:** a question for the pause; nothing changed here
- **proved:** tree

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | proposed: a `bug`; the two members atomic, or `close()` under `mMutex` with `update()` reading under it; a ThreadSanitizer case over an extracted card first (stage E's covering case) |
| PL-02 | Open | proposed: a design ruling at the pause: a handle the window keeps alive until the holder lets go (the component's half), with `Window`'s teardown order T35's |
| PL-03 | Open | proposed: a weak token the posts check; 3.20's case (post, delete, drain) with the fakes' `Window.h` as the covering case |
| PL-04 | Open | proposed: drop the `_()` (a contained fix, a #585 line); 3.16 as the covering case; the catalog's orphan `msgid` is a row for the pause |
| PL-05 | Open | proposed: read at the pin before a fix (the grid's prompt collection with a tab strip cell; when `updateHelpPrompts` runs on a focus move inside the menu); a `bug` only if the pin's code drops them |
| PL-06 | Open | proposed: the one token (`.w()`), a #585 line; 3.6's case FAIL then PASS |
| PL-07 | Open | proposed: a pause ruling (a register row): shares that sum to 1, or the gap recorded; 3.4's case |
| PL-08 | Open | proposed: a pause ruling (a register row): the root fixed in the component (it re-heights every padded auto-height text) or recorded with the reproducer for #585; 3.5's case |
| PL-09 | Open | proposed: `_("AUTO")` with its French in the same commit, a #585 line; 3.7's case |
| PL-10 | Open | proposed: `_()` with its French in the same commit, a #585 line |
| PL-11 | Open | proposed: recorded; contained under rule 6 if the pause opens it |
| PL-12 | Open | proposed: a `dynamic_pointer_cast` with a null check, the invariant written beside `MenuComponent.h:53-56` |
| PL-13 | Open | proposed: a pause ruling: a re-ask on the next page build, or a word on the row; `tools/ra-ui-test`'s fixture shape |
| PL-14 | Open | proposed: a pause ruling: a bar that fits its cell, or the pages' labels; 3.26's arithmetic per page |
| PL-15 | Open | proposed: a pause ruling (a register row): a screen fraction under D-UI-012's family, or upstream's constant kept |
| PL-16 | Open | proposed: the comment corrected or the claim kept at the pause; the second copy is not deleted here |
| PL-17 | Open | proposed: a pause ruling: a rasterise-first in the component, or recorded |
| PL-18 | Open | proposed: recorded (G-10 `CANNOT`: no media); a contained fix only if the pause opens it |
| PL-19 | Open | proposed: recorded |
| PL-20 | Open | proposed: a one-commit tidy if the pause opens it |
| PL-21 | Open | proposed: recorded; a `CloudText` that moves to es-core is T18's and T35's call |
| PL-22 | Open | proposed: a design ruling at the pause; LeakSanitizer over an extracted builder |
| PL-23 | Open | proposed: a `tools/vocabulary-check` rule proposed (the brand inside those builders' arguments) |
| PL-24 | Open | proposed: 3.8's case at stage C decides; a `bug` only if it FAILs |
| PL-25 | Open | proposed: a style question for the pause |
| PL-26 | Open | proposed: a question for the pause; nothing changed here |

## punch_index

```yaml
punch_index:
- id: PL-01
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "L-22 (new)"
  outcome: "open"
- id: PL-02
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "§ 1 (b), T2 PC-1"
  outcome: "open"
- id: PL-03
  severity: "Medium"
  category: Lifetime
  question: Q4
  source_finding: "L-12"
  outcome: "open"
- id: PL-04
  severity: "Medium"
  category: Words
  question: Q3
  source_finding: "L-01, 3.16"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: Input
  question: Q3
  source_finding: "L-25 (new, the guest)"
  outcome: "open"
- id: PL-06
  severity: "Low"
  category: Correctness
  question: Q1
  source_finding: "3.6"
  outcome: "open"
- id: PL-07
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "L-03, 3.4"
  outcome: "open"
- id: PL-08
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "L-17, #48"
  outcome: "open"
- id: PL-09
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "3.7"
  outcome: "open"
- id: PL-10
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-23 (new)"
  outcome: "open"
- id: PL-11
  severity: "Low"
  category: Input
  question: Q3
  source_finding: "L-24 (new)"
  outcome: "open"
- id: PL-12
  severity: "Low"
  category: Structure
  question: Q3
  source_finding: "L-15"
  outcome: "open"
- id: PL-13
  severity: "Low"
  category: Reads
  question: Q5
  source_finding: "L-08, 3.21"
  outcome: "open"
- id: PL-14
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "L-04, 3.26"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "L-06"
  outcome: "open"
- id: PL-16
  severity: "Low"
  category: Constants
  question: Q2
  source_finding: "L-05"
  outcome: "open"
- id: PL-17
  severity: "Low"
  category: Layout
  question: Q1
  source_finding: "L-02, L-16"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Lifetime
  question: Q4
  source_finding: "L-10"
  outcome: "open"
- id: PL-19
  severity: "Low"
  category: Input
  question: Q3
  source_finding: "L-13"
  outcome: "open"
- id: PL-20
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-14"
  outcome: "open"
- id: PL-21
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-07"
  outcome: "open"
- id: PL-22
  severity: "Low"
  category: Lifetime
  question: Q4
  source_finding: "§ 1 (c), T26 PL-27"
  outcome: "open"
- id: PL-23
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-18"
  outcome: "open"
- id: PL-24
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "3.8"
  outcome: "open"
- id: PL-25
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "3.13"
  outcome: "open"
- id: PL-26
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "§ 1 (h)"
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
leads are § 2's L-01 to L-21, cited here by number (their lines are the
table's and are not restated), and the floor's pure leads tabled at the end
of this section; each is read at its lines before it is called anything,
and the seven that FAIL at the pin (§ 5) get their `git log -S` first
(`engineering-practices.md:83`); the upstream surfaces outside the lanes are
§ 1's list, read and recorded, fixed only under rule 6 (D-UI-079).

- **Q1 Layout: computed from what it last produced, or from a moving
  number** (`es-native-ui.md:324`; `es-code-traps.md:91`, `:118`;
  blindspot 44; D-UI-050; the layouts run). **L-03**: 3.4's case,
  `rowPercs(26, 20)` and `(20, 26)` seen to FAIL at the pin (the sum is not
  1), the `git log -S` of the 0.9/1.1 first, the contained fix a pair of
  percentages that sum to 1 (or the second row the remainder); G-07 is
  `CANNOT`, 3.4's 300 `setDescription` calls are the hundreds the rule
  asks for. **L-02** and **L-16**: the eight constructor reads of
  `Font::getHeight` tabled with what each sizes and whether a page reopened
  after its tallest glyph has drawn differs from its first paint; the proof
  is a read trace and a 640x480 frame pair (G-05's page opened twice); the
  disposition a rasterise-first (`font->sizeText(<ASCII 32..126>)`,
  `es-code-traps.md:118`) in the component or a record, ruled at the pause.
  **L-17**: 3.5's case on `onTextChanged` with a `Font` double (padding 32
  px on a 640 px box, a word at the wrap point: the measured height one
  line short), a 640x480 frame of a padded auto-height text that is not a
  `GuiMsgBox`, and the reproducer written into `02` for #585's line; the
  root fix is the pause's (§ 1 f). **3.6** (`TextComponent.cpp:486`'s
  `mPadding.y()` twice): the case seen to FAIL, the lines `:480-500` read
  whole first (the stub checked against the unfixed code,
  `engineering-practices.md:464`), a contained one-token fix under rule 6
  and a #585 line. A table: every size in the 80 computed from a size the
  pass wrote (the rule's shape) and every layout read of `Font::getHeight`,
  with the surface that shows it.
- **Q2 The house constants, and the surfaces that keep them**
  (`es-native-ui.md:175-299`; `es-ui-style-guide.md:136`, `:197-204`;
  D-UI-012, D-UI-016, D-UI-078; `time-to-play.md`; the constants run).
  **`BUTTON_GRID_HORIZ_PADDING` 0.022** (`MenuComponent.cpp:14`): G-03's
  14 px at 640 and G-11's 28 px at 1280 measured in the frames' columns;
  **L-04**: 3.26's case (`makeButtonGrid`'s widths: four 128 px buttons at
  640 fit, five do not) and the arithmetic per candidate page at 640 (the
  14 + 4 + 3 + 3 `addButton` sites named), the widest bars framed on the
  guest, the disposition (a bar that fits its cell, or the pages' labels)
  ruled at the pause; **L-05**: the second copy at
  `GuiTextEditPopupKeyboard.cpp:14` recorded against the comment's "one
  place" (the popup is T35's; the comment is this slice's to correct or the
  claim to keep); **L-19**: the dead floor, recorded. **`NOTIFICATION_OPACITY`
  255, 0.9 W, centred** (`AsyncNotificationComponent.cpp:31`, `:64`,
  `:112`): G-02's pixel reads (edges at x 32 and x 608; a panel-colour
  pixel over box art, not a blend); the agreement with `Window.cpp:1183`,
  `:1192` cited from T35's file, not re-read. **`DIMMED_ALPHA` 0x50**
  (`ComponentList.h:25-26`): G-04's luminance ratio over the same panel;
  **L-06**: the 20 px inset at both sizes framed, recorded as upstream's
  constant the fork exposed, the fraction a pause ruling. **The pixel
  constants in nine upstream sites** (`ComponentList.cpp:11`,
  `TextEditComponent.cpp:8-9`, `:31`, `ButtonComponent.cpp:10`,
  `GridTileComponent.cpp:56`, `.h:148`, `MenuComponent.cpp:167`, `:192`,
  `VideoVlcComponent.cpp:782`, `NinePatchComponent.cpp:177`, the `-32`
  nine-patch corner in four files): tabled against `es-native-ui.md:299`,
  each with the panel it is right on; outside the lanes unless a fork page
  reads it (L-06). **The per-frame cost** (`es-ui-style-guide.md:96`): the
  three func-form rows T31 listed, `ComponentList::render`'s re-tint, and
  the card's `render`, each priced in the retro from the guest (a frame
  time read from `tools/vm-visual-qa`'s `settle` is the only number the
  harness gives; a `CANNOT` with that reason is allowed). A table: every
  house constant, its one definition, every site that reads it, and the
  frame that shows it.
- **Q3 Input and the help bar** (`es-code-traps.md:79`, `:136`; D-UI-034,
  D-UI-021; `es-ui-style-guide.md:171`, `:178`, `:232`; menu map
  `:567-568`; the input run). **`canMoveCursor`**: 3.1 to 3.3's cases (the
  `GuiMsgBox` shape false in all four; the Nx2 button row left/right only;
  `(0,0)` false), G-06's OK-only dialog reading `OK` and no `CHOOSE`, and
  G-03's YES/NO box reading exactly one. **The strip's focus stop**:
  G-05's four frames (the selector bar over SCRAPE, SWITCH TAB in the bar,
  OPTIONS after right, the first row after down, the wrap strip -> rows ->
  buttons -> strip); 3.17's de-duplication case; #65's component half
  proved there and put to the pause (§ 2's row). **`getHelpPrompts` per
  component** (12 `.cpp` definitions, 2 inline): a table of each with the
  condition under which it offers a direction, and **L-13**'s two that
  offer by type or by mode alone (the carousel, the option list) framed
  on the guest if a one-system carousel or a one-value option row is
  reachable, else recorded; **L-01**: the icon key through `_()` --
  3.16's case over `getIconTexture`'s key table with `haut/bas`, the
  `es_log.txt` line `Unknown help icon "haut/bas"` and a French settings
  page's help bar at 640x480 (G-04 or G-05 run under French) are the
  positives; the contained fix drops the `_()` on `ComponentList.cpp:568`
  (the catalog's `msgid "up/down"` then an orphan the stream leaves or
  removes, D-UI-051's same-commit rule either way). **L-15**:
  `setCursorToButton`'s unstated invariant, a `dynamic_pointer_cast` plus a
  null check as the contained fix, the invariant written into `02` beside
  `MenuComponent.h:53-56`. **The back-button accelerator** is `GuiMsgBox`'s
  (T35's) and is cited, not read; what this slice owns is the bar's order
  (`MenuComponent::addButton` `:487`, BACK last) and the grid's cursor.
- **Q4 Lifetime** (`es-code-traps.md:22`, `:191`; `es-native-ui.md:94`;
  D-UI-078, D-UI-093; the lifetimes run). **L-11** and § 1 (d): the four
  `delete this` and the two return-straight-after lines read, the
  invariant stated, 3.19's ASan harness in `cloud-oauth-lifetime.py`'s
  shape run on the host over an extracted popup if a `Window` double
  suffices, else `CANNOT` with the reason. **L-12**: 3.20's case (post,
  delete, drain) with the fakes' `Window.h`; a contained fix is a weak
  token the posts check, put to the pause with T33's `AppWindow` named.
  **L-10**: the detached release thread, the unlocked `component = nullptr`
  write, the destructor's `stopVideo()`: a read trace with the two threads
  and the two reads named; TSan on a guest with a video theme is G-10's
  `CANNOT` (no media); outside the lanes, recorded. **§ 1 (b)**, T2's
  PC-1: what the card promises a holder after `window.deinit()` -- the
  destructor `:125-126`, the mutex, `Window`'s teardown order (cited from
  T35's file) -- and whether the component can refuse a late `close()`;
  the lane files the `bug` if the read proves the window, naming the
  callers' half for T18 and T20. **§ 1 (c)**, T26 PL-27: the callback
  types of `SwitchComponent::setOnChangedCallback` and
  `OptionListComponent`'s, whether a weak-by-design type is the
  component's answer or the pages' `onFinalize` clearing stays the fix;
  LeakSanitizer over an extracted builder; a design ruling at the pause.
  **§ 1 (e)**, #1266: `ImageGridComponent::clear()` / `resetGrid()` read
  for what the grid may still point at after `clear()`, the contract
  written, T32's `s4-views.py` shape named as the harness. **L-21**:
  recorded, sound. A table: every `delete this` (4), every `std::thread`
  (1), every `.detach(` (1), every `postToUiThread` (2), every raw pointer
  a component hands out or holds across a rebuild, who joins or drains it,
  what it touches on the interface thread.
- **Q5 Reads and the network** (`es-native-ui.md:107`;
  `es-code-traps.md:127`, `:164`, `:238`; `engineering-practices.md:111`;
  D-RA-009; the reads run). **The reads**: 10 `exists(` lines, 10
  occurrences, **0 uncached**: each with its file, its writer while ES
  runs (the scraper for the media paths, `HttpReq` for the badge, a theme
  install for the theme paths), and whether a remembered miss changes the
  screen. **L-08**: `tools/ra-ui-test`'s fixture shape (a 204 then a 200
  on the same badge URL) and a frame of the row; by design per the comment,
  and the player sees nothing, so the disposition (a re-ask on the next
  page build, or a word on the row) is the pause's; **L-09**: 3.21's case
  with the real `FileSystemUtil` (the miss cached at `:134`, the file
  written, `:190` read), seen to FAIL or PASS at the pin, the answer about
  the writer's erase cited from T21's and T36's rows; **L-20**: recorded
  with the scraper named as the writer, a frame if a scrape then a game
  open before any launch fits the window, else `CANNOT`. **§ 1 (a)**,
  #1263's caller half: `ImageComponent.cpp:408` read with
  `TextureResource.cpp:100-131` (T36's, cited): what the component asks
  by path, when it re-asks, what a live texture under the key gives it
  (T26 #1221's shape); the contract stated in `02`; the cache's half named
  for T36. A table: every `exists`, `getFileSize`, `HttpReq` and texture
  lookup reachable from the 80 with its writer and what a stale answer
  reads as.
- **Q6 The words** (`es-player-text.md:25`, `:29-31`, `:135`, `:141`,
  `:236`; `es-ui-style-guide.md:88`, `:144`, `:164`; D-UI-051,
  D-WORKFLOW-144; the strings and French runs). **The 17 msgids** against
  the catalog (the proof's parser shape, re-run); `SWITCH TAB` and its
  French read in G-05's frames under EN and FR; **`"Auto"`**
  (`SliderComponent.cpp:282`): 3.7's case, G-09's frame, the contained fix
  `_("AUTO")` with its French in the same commit (the placeholder word the
  style guide names) -- upstream's line, rule 6, a #585 line; **the slider's
  suffix** glued (`:295-296`, `:312-313`) read against `es-ui-style-guide.md:88`
  and framed; **3.13**: a row with no date reads blank, not `<NOT SET>`
  (`DateTimeEditComponent.cpp:256-257`), recorded against `:164`, a style
  question for the pause; **L-18**: the five up-casing formatters tabled
  with the one word they must never see, and a `tools/vocabulary-check`
  rule proposed in `02` (a grep for the brand inside `addEntry|addButton|
  setTitle|addWithDescription|addGroup` arguments) for the coordinator;
  **L-01**'s French half is Q3's; the 0 non-ASCII comment lines in the 21
  fork-modified files and the one upstream byte at
  `VideoVlcComponent.cpp:859` (Q7). The card's candidate rows
  (D-UI-035, D-UI-107) are read for the shape the component imposes (at
  least one candidate per row; the width it hands the chooser, 3.18), the
  words themselves being T18's and T20's.
- **Q7 The structure and the merge debt** (`es-native-ui.md:32`;
  `es-code-traps.md:60`; `engineering-practices.md:28`, `:576`;
  D-WORKFLOW-162, D-WORKFLOW-209; the membership, scope, delta and
  non-ASCII runs). **L-07**: the es-core to es-app include recorded with
  how it resolves (`-I es-core/src` plus `../../`), the unit build's
  `CloudText.cpp` link, and the question for the pause (a `CloudText`
  that moves to es-core is T18's and T35's call, not the lane's). **The
  in-source platform gates** (`GridTileComponent.cpp:11`,
  `NinePatchComponent.cpp:415`, `VideoComponent.cpp:22`,
  `VideoPlayerComponent.{cpp,h}:1`, `VideoVlcComponent.cpp:17`, `:485`,
  `:592`, `:668`, `:779`, `:836`, `:874`, `:875`) tabled against
  `es-core/CMakeLists.txt`'s unconditional lists (`:49-90`, `:186-223`;
  `if(` only at `:278` and `:287`): which units compile to nothing on an
  image (`VideoPlayerComponent` whole), D-WORKFLOW-209's disposition (a
  dead-end table removes nothing). **The non-ASCII byte**
  (`VideoVlcComponent.cpp:859`): recorded, not fixed (`es-code-traps.md:60`,
  an upstream hit), with the fact that `git grep -P` does not see it and a
  C-locale grep does, and `:860` read for what sits next to it. **L-14**:
  the two indentations and the include above the guard, a stream's
  one-commit tidy if the pause opens it. **L-05**'s second copy: recorded,
  not deleted (`engineering-practices.md:576`). **Merge debt: none**, the
  one line; **batocera's eight** as the reconciliation list with the one
  `updateGrid()` overlap and the six fork candidates for #585 named in
  `02` § The #585 lines owed (`aa8c5da4c` the strongest; `7c7ffab43`;
  `b6eb26980`; `8927b1760` with `f1ae6bc25` as a pair; `7dc8bf373` only
  after the RTL reconciliation; `2088eadb9`); **the `setOpacity` null
  guard**: `git grep -n 'setOpacity' PIN -- es-core/src es-app/src` for
  every caller, whether `mGrid` can be null at `HelpComponent.cpp:212` or
  `:251` on the fork's images (`ShowHelpPrompts` off, or a page with no
  prompts, while something fades the bar), a contained guard under rule 6
  if reachable, recorded with the read if not; **`UntintedImageComponent`**'s
  home found by `git grep` and the lift question put to the pause (§ 1 h).
  **The map**: no row; the checker's line quoted (§ 3 item 3).

### The floor's pure leads, carried

The floor and fork-changes digests are in no tree, so their seams are here
in the shape `file:line at the pin | the function | what a case would
catch`; rows 3.1 to 3.21 are the floor's, 3.22 to 3.34 the fork-changes
digest's § 5 seams that the floor does not carry; the seven that FAIL at
the pin, or are the candidates the drafter marks as such, are in bold.
Each is a case in `CloudText`'s shape (§ 5 item 1) with a `Window` or
`Font` double where the lines consult one (the fakes' `Window.h` exists; a
`Font` double is the lane's), unless marked ASan or guest.

| # | At the pin | Function | What a case would catch |
| --- | --- | --- | --- |
| 3.1 | `ComponentGrid.cpp:396-414` | `canMoveCursor(dir)` | a 2x2 whose only focusable cell is one row answers false in all four directions; an Nx2 button row with a 2 px spacer row answers left/right true, up/down false; `(0,0)` false (`:398-399`) |
| 3.2 | `ComponentGrid.cpp:519-553` | `getHelpPrompts()` | a child prompt named `up/down` suppresses the grid's vertical CHOOSE (`:536-538`); `up/down/left/right` both (`:532-535`); otherwise exactly one of the three (`:546-551`) |
| 3.3 | `ComponentGrid.cpp:329-379` | `moveCursor(dir)` | from the only focusable cell every direction returns false and `mCursor` is unchanged (`:377-378`); in a 1x3 with (0,2) the only other focusable, down from (0,0) lands on (0,2); the reverse scan (`:359-373`) stays off |
| **3.4** | `MultiLineMenuEntry.cpp:50-80` (**`:74-75`**) | `naturalHeight`, `layoutRows()` | font height 20, padding 0: label only -> rows 20 and 0; with a substring -> `0.9*20/40`, `1.1*20/40`; **`rowPercs(26, 20)` -> 0.987 and `(20, 26)` -> 1.013, a sum other than 1 (L-03)**; 300 `setDescription` calls leave `size.y` at 40 (#241) |
| 3.5 | `TextComponent.cpp:315-340` | `onTextChanged()` | SINGLELINE with `"a\nb"` measures `"a"` (`:325-327`); with padding 32 px on a 640 px box and a word at the wrap point the measured height is one line short (`:338` against `:350`, L-17) |
| **3.6** | `TextComponent.cpp:486` | `update()`'s vertical marquee limit | **`int limit = mSize.y() - mPadding.y() - mPadding.y();` where `:428` and `:351` subtract `.w()`: with padding (0,10,0,30) the limit is 20 px too large** -- the lines `:480-500` read whole before the stub |
| **3.7** | `SliderComponent.cpp:44-58`, `:271-319` (**`:282`**) | `calculatePrecision(step)`, the value text | step 0.1 -> `1.5%`; step 1 -> `15%` (suffix glued); step 0.25 -> 2; **AUTO prints `"Auto"`, neither `_()` nor the placeholder `AUTO`**; `std::to_string(step)` prints six decimals so a step under 1e-6 yields 0 |
| **3.8** | `CarouselComponent.cpp:74-90` with `:113`, `:119`; `IList.h:376-400` | `moveCursorFast(forward)` | **size 3, cursor 0, `pageup`: `count=-10`, `value = -10 + 3 = -7` after one `+= sz` (`:84-85`), `listInput(-7)`**; the case asserts the landing index is in `[0, sz)` for every loop type (3.15) |
| 3.9 | `ImageGridComponent.h:1437-1468` | `calcGridDimension()` | 640x480, tile 100x100, margin 10 -> x 5, y `ceil(4.45)` = 5, `mLastRowPartial`; a tile size of 0 when `mTileSize + mMargin` is 0 (only `LOG(LogError)` guards `<1`, `:1449-1452`) |
| 3.10 | `ImageGridComponent.h` from `:1065` (`:1162-1186`) | `onCursorChanged`'s `mStartPosition` | first, middle and last row -> 0, `(col - centralCol) * dimOpposite`, `lastScroll * dimOpposite`; an off-by-one on the partial last row |
| 3.11 | `TextListComponent.h:262-269` | the visible range in `render` | offset 0, row 20, height 480 -> `screenCount` 24, `lastEntry min(n, 25)`, `listCutoff` 24; the extra row past the cutoff (the arithmetic extracted first) |
| 3.12 | `DateTimeEditComponent.cpp:124-160` | the month/day/year step inside `input()` | 31 Jan +1 month -> 28/29 Feb (`:156-158`); Dec +1 -> Jan (`:131-132`); day 1 -1 -> days in month (`:144-145`); `tm_year` 0 -1 -> 0 (`:152-153`); a fake `InputConfig` or an extraction |
| 3.13 | `DateTimeEditComponent.cpp:251-260` | `getDisplayString()` | `getTime() == 0` -> `""` (`:256-257`): a row with no date reads blank, not `<NOT SET>` (Q6) |
| 3.14 | `ScrollableContainer.cpp:62-107`, `:110-124`, `:126-131` | `update`, `getContentSize`, `reset` | content 1000 px in a 480 px box, speed 150, delay 6000: the first step at 6000 ms (`reset` seeds `-delay + speed`, `:130`); `mAtEnd` then `reset()` after `AUTO_SCROLL_RESET_DELAY` (`:6`); `:69`'s unused `680.0f` is lint |
| 3.15 | `IList.h:267-330`, `:376-400` | `listInput`, `scroll` | `LIST_NEVER_LOOP` clamps and zeroes velocity and tier (`:388-399`); `LIST_PAUSE_AT_END` clamps only at tier > 0 or `\|amt\| > 1`; else wraps -- the landing index for 3.8 |
| **3.16** | `HelpComponent.cpp:73-130`, `:121-169`, `:176-200` | the prompt row's layout; `getIconTexture` | `maxWidth = width - ENTRY_SPACING` (`:79`), the clock's width subtracted (`:89-90`), height `round(letterHeight * 1.25)` (`:96`); `[100, 100, 100]` at max 250 -> 2 kept; `[300]` -> 0 kept, `rowWidth = 1`; **a key `haut/bas` -> `nullptr` and the `Unknown help icon` line (L-01)** |
| 3.17 | `ComponentTab.cpp:77-96`, `:320-345` | `input` left/right, `getHelpPrompts` | a child prompt already naming `left/right` or `up/down/left/right` gets no second SWITCH TAB (`:332-341`); a one-tab strip offers none |
| 3.18 | `AsyncNotificationComponent.cpp:136-145`, `:63-65` | the width handed to `chooseThatFits` | the row's own `getSize().x()` (`:138`; 0 for a null row), measured with the row's font (`:142`): a row the grid has not sized yet gets the first candidate, the full form (`:133-135`); the case asserts the width is the row's cell, never the screen's 0.9 W (`:64`) (the chooser itself is `CloudTextTests.cpp:832-854`) |
| 3.19 | `OptionListComponent.h:88-100`, `:140-160`, `:188-200` (ASan) | the popup's four `delete this` | select a row (`:96`), press BACK (`:158`), the back button (`:195`): the popup is gone and nothing touches it after; the `cloud-oauth-lifetime.py` shape |
| 3.20 | `TextEditComponent.cpp:39`, `:47` | the two posted raw `this` | post, delete the component, drain the queue: `startEditing()` on freed memory (the fakes' `Window.h` queues posts) |
| **3.21** | `WebImageComponent.cpp:134`, `:190`, `:197-200`; `utils/FileSystemUtil.cpp:144` | the cached `exists` around a download; the 0-byte answer | **the miss cached at `:134`, the file written, `:190` asserted true**; **a 204 then a 200 on the same URL: the second never asked (L-08)** -- `queryCacheEntry :203-220` and `Settings::UseFileCache()`'s default read first |
| 3.22 | `ImageComponent.cpp:85-180` | `resize`'s fit (aspect, turn, min/max modes) | `256x240` at `4/3` -> `320x240`; turned -> `240x320`; a crop applied to the wrong axis after a turn (`:156-159`, `:167-170`); an aspect of 0 changing anything |
| 3.23 | `ImageComponent.cpp:273-291` | the texture-corner permutation | turn 1 applied four times is identity; turn 2 is turn 1 twice; turn 3 its inverse |
| 3.24 | `ImageComponent.cpp:491-499`, `GridTileComponent.cpp:1055-1063` | the quarter-turn normaliser | `-1 -> 3`, `5 -> 1`, `-4 -> 0`; a negative record left negative |
| 3.25 | `ComponentList.h:26` | `ComponentListFlags::dimmed` | `dimmed(0xAABBCCFF) == 0xAABBCC50`; idempotent |
| **3.26** | `MenuComponent.cpp:543-562`; `ButtonComponent.cpp:10` | `makeButtonGrid`'s widths | **four 128 px buttons at 640 -> 568 <= 576; five -> 710 > 576 (L-04)**; a column percentage sum other than 1 |
| 3.27 | `MenuComponent.cpp:396-424` | `updateSize`'s row-fit loop | a first row taller than the budget -> zero rows; rows exactly filling; the `height + rowHeight < maxHeight` test excluding the row that fits exactly |
| 3.28 | `ComponentList.cpp:295-319` | `updateCameraOffset` | a cursor on the last row -> `total - view`; rows shorter than the view -> 0; the `mCursor < mEntries.size()` signed/unsigned compare |
| 3.29 | `TextListComponent.h:591-608` | `updateCameraOffset` | the same three, for the game list |
| 3.30 | `SwitchComponent.cpp:50-80`, `:118-138` | the tri-state cycle, `getValue`/`setValue` | auto -> on -> off -> auto; `setValue("auto")` without `hasAuto` -> off; `"AUTO"` (case) read as off |
| 3.31 | `SliderComponent.cpp:234-257` | `setValue`'s clamp and the AUTO sentinel | `setValue(max + 1) == max`; the sentinel (`mMin - mSingleIncrement`) accepted without auto mode |
| 3.32 | `RatingComponent.cpp:192-204` | the OK-press accumulation `+= 1/5` | five presses from 0.0 reach 1.0 exactly, the sixth wraps; from a parsed `0.35` the steps drift |
| 3.33 | `TextEditComponent.cpp:267-271` | `moveCursor` through `Utils::String::moveCursor` (T21's) | a 4-byte glyph and a two-character CJK name: a cursor inside a UTF-8 sequence |
| 3.34 | `CarouselComponent.cpp:183-200` | the shortest-path target | from 0 to N-1 -> `-1`; from N-1 to 0 -> `N`; a count of 1; a divide by 0 |


