// T34 (#681): components-tests. Each case lifts the pin's lines verbatim
// (tools/t34-extract.py, each extract refused unless its first and last lines
// hold the code they were written for) into the smallest double that compiles
// them, and asserts the behaviour the component should have: a defect at the
// pin is a FAIL here, the case's "seen to FAIL against the unfixed extract".
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"
#include <algorithm>
#include <atomic>
#include <cassert>
#include <cmath>
#include <cstdio>
#include <functional>
#include <ctime>
#include <map>
#include <memory>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

// The catalog double (S4): _() records each msgid it is asked for and, under
// gFrench, answers with the pin's French for the two these cases reach (po
// :3708-3709 and CHOOSE's, read at stage A); every other msgid is returned as
// it came. And the prompt type and the two button names the lines use.
static bool gFrench = false;
static std::set<std::string> gSeen;
static std::string t34_tr(const char* s) {
	static const std::map<std::string, std::string> fr = {{"up/down", "haut/bas"}, {"CHOOSE", "CHOISIR"}};
	gSeen.insert(s);
	if (gFrench) { auto it = fr.find(s); if (it != fr.end()) return it->second; }
	return s;
}
#define _(x) t34_tr(x)
struct HelpPrompt { std::string first, second; HelpPrompt(const std::string& b, const std::string& l) : first(b), second(l) {} };
static const char* BUTTON_OK = "a";
static const char* BUTTON_BACK = "b";

// 3.4: MultiLineMenuEntry.cpp:72-75, the two rows' shares.
struct Shares {
	float p0 = -1, p1 = -1;
	void setRowHeightPerc(int r, float v) { (r == 0 ? p0 : p1) = v; }
	void layout(float th, float sh) {
#include "x_mlme_shares.inc"
	}
};
TEST_CASE("3.4 a two-line row's shares sum to 1 whatever its two fonts (MultiLineMenuEntry.cpp:72-75)") {
	for (auto p : std::vector<std::pair<float, float>>{{20, 20}, {26, 20}, {20, 26}}) {
		Shares s; s.layout(p.first, p.second);
		CAPTURE(p.first); CAPTURE(p.second);
		CHECK(s.p0 + s.p1 == doctest::Approx(1.0f));
	}
}

// 3.6: TextComponent.cpp:486, the vertical marquee's limit.
struct V2 { float a, b; float x() const { return a; } float y() const { return b; } };
struct V4 { float a, b, c, d; float x() const { return a; } float y() const { return b; } float z() const { return c; } float w() const { return d; } };
struct Marquee {
	V2 mSize; V4 mPadding;
	int lim() {
#include "x_text_limit.inc"
		return limit;
	}
};
TEST_CASE("3.6 the marquee's limit is the height less the top and the bottom padding (TextComponent.cpp:486)") {
	Marquee m{{640, 100}, {0, 10, 0, 30}};
	CHECK(m.lim() == 100 - 10 - 30);
}

// 3.7: SliderComponent.cpp:44-59 and :276-299, the value text.
#include "x_slider_precision.inc"
struct Slider {
	bool mIsAutoMode = false, autoOn = false; float mSingleIncrement = 1, mValue = 0; std::string mSuffix;
	bool getAuto() { return autoOn; }
	std::string text() {
#include "x_slider_text.inc"
		return val;
	}
};
TEST_CASE("3.7 the slider's AUTO value reads the placeholder AUTO (SliderComponent.cpp:280-283)") {
	Slider s; s.mIsAutoMode = true; s.autoOn = true;
	CHECK(s.text() == "AUTO");
}
TEST_CASE("3.7 the slider's value and suffix, glued, at its step's precision (SliderComponent.cpp:44-59, :286-296)") {
	Slider a; a.mSingleIncrement = 1; a.mValue = 15; a.mSuffix = "%"; CHECK(a.text() == "15%");
	Slider b; b.mSingleIncrement = 0.1f; b.mValue = 1.5f; b.mSuffix = "%"; CHECK(b.text() == "1.5%");
	CHECK(calculatePrecision(0.25f) == 2);
}

// 3.8: CarouselComponent.cpp:76-89 into IList.h:381-406 (scroll's landing).
enum LoopType { LIST_ALWAYS_LOOP, LIST_PAUSE_AT_END, LIST_NEVER_LOOP };
struct Carousel {
	int mCursor = 0; std::vector<int> mEntries;
	int moveCursorFast(bool forward) {
#include "x_carousel_fast.inc"
	}
};
struct ListScroll {
	int mCursor = 0, mScrollVelocity = 0, mScrollTier = 0, n = 0; LoopType mLoopType = LIST_ALWAYS_LOOP;
	int size() const { return n; }
	int land(int amt) {
		mScrollVelocity = amt;
		if (mScrollVelocity == 0 || size() < 2) return mCursor; // IList.h:378, scroll's guard
#include "x_ilist_scroll.inc"
		return cursor;
	}
};
TEST_CASE("3.8 a carousel's page up or down lands inside the list for every loop type (CarouselComponent.cpp:74-90, :113, :119; IList.h:376-406)") {
	for (int sz : {1, 2, 3, 5, 12})
		for (int cur = 0; cur < sz; cur++)
			for (bool fwd : {true, false})
				for (LoopType lt : {LIST_ALWAYS_LOOP, LIST_PAUSE_AT_END, LIST_NEVER_LOOP}) {
					Carousel c; c.mEntries.assign(sz, 0); c.mCursor = cur;
					int amt = c.moveCursorFast(fwd) - cur;
					ListScroll l; l.n = sz; l.mCursor = cur; l.mLoopType = lt;
					int at = l.land(amt);
					CAPTURE(sz); CAPTURE(cur); CAPTURE(fwd); CAPTURE((int)lt); CAPTURE(amt);
					CHECK(at >= 0); CHECK(at < sz);
				}
}

// 3.16: the list's move prompt (ComponentList.cpp:568 at the pin), its key
// under French, against HelpComponent.cpp:18-33. Since S4 the key is read
// from the list's own line through the catalog double; at stage D it was the
// catalog's translation written into the case.
#include "x_help_map.inc"
struct ListPrompts { std::vector<HelpPrompt> prompts; bool addMovePrompt = true;
	void run() {
#include "x_list_prompt.inc"
	} };
TEST_CASE("3.16 the list's CHOOSE key resolves to an icon under French (ComponentList.cpp:568; HelpComponent.cpp:18-33, :190-194)") {
	gFrench = true; ListPrompts l; l.run(); gFrench = false;
	REQUIRE(l.prompts.size() == 1);
	CHECK(ICON_PATH_MAP.count("up/down") == 1);
	CHECK(ICON_PATH_MAP.count(l.prompts[0].first) == 1);
}

// 3.26: MenuComponent.cpp:14 and :547-552, the bar's width against the menu's.
static int gW = 640;
namespace Renderer { inline int getScreenWidth() { return gW; } }
#include "x_button_pad.inc"
struct Vector2i { Vector2i(int, int) {} };
struct Btn { float w; struct S { float wx; float x() const { return wx; } }; S getSize() const { return S{w}; } };
struct BarGrid { void setEntry(const std::shared_ptr<Btn>&, Vector2i, bool, bool) {} };
static float barWidth(const std::vector<std::shared_ptr<Btn>>& buttons) {
	auto buttonGrid = std::make_shared<BarGrid>();
#include "x_button_width.inc"
	return buttonGridWidth;
}
TEST_CASE("3.26 a button bar fits the menu at 640 (MenuComponent.cpp:543-562)") {
	gW = 640; const float menu = 0.9f * 640; // the brief's budget; a windowed menu is narrower (the seat)
	std::vector<std::shared_ptr<Btn>> four, five;
	for (int i = 0; i < 5; i++) { auto b = std::make_shared<Btn>(Btn{128}); if (i < 4) four.push_back(b); five.push_back(b); }
	CHECK(barWidth(four) <= menu);
	CHECK(barWidth(five) <= menu);
}

// ---- S0 (stage E): the floor cases no stream's file holds, run at the pin ----
namespace Math { template <typename T> T min(T a, T b) { return a < b ? a : b; } }
struct Vec2f { float v[2]; Vec2f(float a = 0, float b = 0) { v[0] = a; v[1] = b; } float x() const { return v[0]; } float y() const { return v[1]; }
	float& operator[](int i) { return v[i]; } Vec2f& operator+=(const Vec2f& o) { v[0] += o.v[0]; v[1] += o.v[1]; return *this; } };

// 3.11: TextListComponent.h:262-269, the visible range in render.
struct TextListRange {
	float mCameraOffset = 0, rowH = 20; int mLineCount = 0; Vec2f mSize; std::vector<int> mEntries;
	float getRowHeight() const { return rowH; } int size() const { return (int)mEntries.size(); }
	struct R { int startEntry, screenCount, lastEntry, listCutoff; };
	R range() {
#include "x_textlist_range.inc"
		return R{startEntry, screenCount, lastEntry, listCutoff};
	}
};
TEST_CASE("3.11 the text list draws one row past its cutoff, never past the list (TextListComponent.h:262-269)") {
	TextListRange a; a.mSize = Vec2f(300, 480); a.mEntries.assign(100, 0);
	auto r = a.range(); CHECK(r.screenCount == 24); CHECK(r.lastEntry == 25); CHECK(r.listCutoff == 24);
	TextListRange b; b.mSize = Vec2f(300, 480); b.mEntries.assign(10, 0);
	auto q = b.range(); CHECK(q.lastEntry == 10); CHECK(q.listCutoff == 10);
}

// 3.29: TextListComponent.h:593-607, updateCameraOffset.
struct TextListCamera {
	float mCameraOffset = -1, rowH = 20; Vec2f mSize; std::vector<int> mEntries; int mCursor = 0;
	float getRowHeight() const { return rowH; }
	void update() {
#include "x_textlist_camera.inc"
	}
};
TEST_CASE("3.29 the game list's camera: the last row at the bottom, a short list at 0 (TextListComponent.h:591-608)") {
	TextListCamera c; c.mSize = Vec2f(300, 480); c.mEntries.assign(100, 0); c.mCursor = 99; c.update();
	CHECK(c.mCameraOffset == doctest::Approx(100 * 20 - 480));
	TextListCamera s; s.mSize = Vec2f(300, 480); s.mEntries.assign(10, 0); s.mCursor = 9; s.update();
	CHECK(s.mCameraOffset == doctest::Approx(0));
	TextListCamera n; n.mSize = Vec2f(300, 480); n.mEntries.assign(100, 0); n.mCursor = -1; n.update();
	CHECK(n.mCameraOffset == doctest::Approx(0)); // the signed/unsigned compare reads -1 as past the end
}

// 3.14: ScrollableContainer.cpp:6-8, :64-104, :128-131, the auto scroll's timing.
#include "x_scroll_defines.inc"
struct Scroller {
	int mAutoScrollSpeed = AUTO_SCROLL_SPEED, mAutoScrollDelay = AUTO_SCROLL_DELAY, mAutoScrollAccumulator = 0, mAutoScrollResetAccumulator = 0;
	bool mAtEnd = false; Vec2f mScrollPos, mScrollDir = Vec2f(0, 1), size_ = Vec2f(300, 480), content = Vec2f(300, 1000);
	using Vector2f = Vec2f;
	Vec2f getSize() const { return size_; } Vec2f getContentSize() const { return content; }
	void reset() {
#include "x_scroll_reset.inc"
	}
	void update(int deltaTime) {
#include "x_scroll_update.inc"
	}
};
TEST_CASE("3.14 the auto scroll starts after its delay and resets after the end (ScrollableContainer.cpp:62-131)") {
	Scroller s; s.reset();
	CHECK(s.mAutoScrollAccumulator == -AUTO_SCROLL_DELAY + AUTO_SCROLL_SPEED);
	// reset() starts the accumulator at -delay + speed, so the first step lands at the delay itself
	s.update(AUTO_SCROLL_DELAY - 1); CHECK(s.mScrollPos.y() == doctest::Approx(0));
	s.update(1); CHECK(s.mScrollPos.y() == doctest::Approx(1));
	for (int i = 0; i < 1000 && !s.mAtEnd; i++) s.update(AUTO_SCROLL_SPEED);
	CHECK(s.mAtEnd); CHECK(s.mScrollPos.y() == doctest::Approx(1000 - 480));
	s.update(AUTO_SCROLL_RESET_DELAY); CHECK(!s.mAtEnd); CHECK(s.mScrollPos.y() == doctest::Approx(0));
}
TEST_CASE("3.14 PL-40: content narrower than the container still scrolls down (ScrollableContainer.cpp:78-96)") {
	Scroller s; s.content = Vec2f(290, 1000); s.reset();
	float most = 0;
	for (int t = 0; t < 10000; t += 16) { s.update(16); if (s.mScrollPos.y() > most) most = s.mScrollPos.y(); }
	CHECK(s.mScrollPos.x() >= 0);
	CHECK(most > 1);
}

// 3.15: IList.h:381-406, scroll's clamp or wrap per loop type (the extract 3.8 uses).
TEST_CASE("3.15 IList clamps under NEVER_LOOP and under PAUSE_AT_END past one step, and wraps otherwise (IList.h:376-406)") {
	ListScroll never; never.n = 5; never.mCursor = 4; never.mLoopType = LIST_NEVER_LOOP; CHECK(never.land(1) == 4); CHECK(never.mScrollVelocity == 0);
	ListScroll pause1; pause1.n = 5; pause1.mCursor = 4; pause1.mLoopType = LIST_PAUSE_AT_END; CHECK(pause1.land(1) == 0);
	ListScroll pause2; pause2.n = 5; pause2.mCursor = 4; pause2.mLoopType = LIST_PAUSE_AT_END; CHECK(pause2.land(3) == 4); CHECK(pause2.mScrollVelocity == 0);
	ListScroll always; always.n = 5; always.mCursor = 4; always.mLoopType = LIST_ALWAYS_LOOP; CHECK(always.land(3) == 2);
}

// ---- S2 (stage E): the card's close, the floor's 3.18 and 3.33 ----

// PL-01 (#1309): update() run inside close(), at the interleaving the seat
// named. The double's flags call update() once, the first time close() writes
// a true -- between its two writes at the pin -- and record whether a closing
// frame was drawn before the fade's opacity was captured.
#define NOTIFICATION_OPACITY 255
struct CardGui { unsigned char opacity = 255; void update(int) {} unsigned char getOpacity() const { return opacity; } void setOpacity(unsigned char o) { opacity = o; } };
struct CardI;
struct HookBool { CardI* c = nullptr; bool v = false; HookBool& operator=(bool b); operator bool() const { return v; } };
struct HookReq { CardI* c = nullptr; bool v = false; void store(bool b, std::memory_order = std::memory_order_seq_cst); bool load(std::memory_order = std::memory_order_seq_cst) const { return v; } };
struct CardI : CardGui {
	using GuiComponent = CardGui;
	bool mRunning = true; HookBool mClosing; float mFadeOut = 0; int mFadeTime = 300; int mFadeOutOpacity = -999; HookReq mCloseRequested;
	bool inClose = false, hooked = false, earlyFrame = false;
	CardI() { mClosing.c = this; mCloseRequested.c = this; }
	void hook() { if (inClose && !hooked) { hooked = true; update(16); } }
	void setOpacity(unsigned char o) { if (mClosing && mFadeOutOpacity == -999) earlyFrame = true; CardGui::setOpacity(o); }
	void close() {
		inClose = true;
#include "x_card_close.inc"
		inClose = false;
	}
	void update(int deltaTime) {
#include "x_card_update_full.inc"
	}
};
HookBool& HookBool::operator=(bool b) { v = b; if (b) c->hook(); return *this; }
void HookReq::store(bool b, std::memory_order) { v = b; if (b) c->hook(); }
TEST_CASE("PL-01 the card's fade starts from its captured opacity whenever update() sees the close (AsyncNotificationComponent.cpp:117-121, :261-306)") {
	CardI c; c.close();
	CHECK(c.hooked);
	CHECK(!c.earlyFrame);
	for (int i = 0; i < 40 && c.mRunning; i++) c.update(16);
	CHECK(!c.mRunning);
}

// 3.18: AsyncNotificationComponent.cpp:136-145, the width chooseThatFits is given.
struct FontD { Vec2f sizeText(const std::string& s) const { return Vec2f(10.0f * s.size(), 20); } };
struct TextComponent { Vec2f size; std::shared_ptr<FontD> font; Vec2f getSize() const { return size; } std::shared_ptr<FontD> getFont() const { return font; } };
namespace CloudText { float gWidth = -1;
	std::string chooseThatFits(const std::vector<std::string>& c, float w, std::function<float(const std::string&)> m) {
		gWidth = w; for (auto& x : c) if (!m || m(x) <= w) return x; return c.empty() ? "" : c.back(); } }
struct AsyncNotificationComponent { static std::string chooseThatFits(const std::shared_ptr<TextComponent>& row, const std::vector<std::string>& candidates); };
#include "x_card_choose.inc"
TEST_CASE("3.18 the card's chooser is given the row's cell, never 0.9 W (AsyncNotificationComponent.cpp:136-145)") {
	auto row = std::make_shared<TextComponent>(); row->size = Vec2f(300, 20); row->font = std::make_shared<FontD>();
	auto got = AsyncNotificationComponent::chooseThatFits(row, {"A LONG SENTENCE THAT IS TOO WIDE", "SHORT"});
	CHECK(CloudText::gWidth == doctest::Approx(300)); CHECK(got == "SHORT");
	CHECK(AsyncNotificationComponent::chooseThatFits(nullptr, {"X"}) == "X"); CHECK(CloudText::gWidth == doctest::Approx(0));
}

// 3.33: TextEditComponent.cpp:267-281 over StringUtil.cpp:278-327 (T21's, read only).
namespace Utils { namespace String {
#include "x_str_cursor.inc"
} }
struct TextEditComponent { std::string mText; unsigned int mCursor = 0; int changed = 0; void onCursorChanged() { changed++; }
	void moveCursor(int amt); void setCursor(size_t pos); };
#include "x_textedit_move.inc"
TEST_CASE("3.33 the text field's cursor moves by whole UTF-8 sequences (TextEditComponent.cpp:267-281)") {
	TextEditComponent t; t.mText = "a\xC3\xA9" "b"; // a, e-acute (two bytes), b
	t.moveCursor(1); CHECK(t.mCursor == 1);
	t.moveCursor(1); CHECK(t.mCursor == 3);
	t.moveCursor(-1); CHECK(t.mCursor == 1);
	t.setCursor(std::string::npos); CHECK(t.mCursor == 4);
	t.mCursor = 2; t.moveCursor(1); CHECK(t.mCursor == 3); // from inside the sequence, the next whole boundary
	t.mCursor = 2; t.moveCursor(-1); CHECK(t.mCursor == 1);
}

// ---- S3 (stage E): the layout ----

// PL-07 (#1314): MultiLineMenuEntry.cpp:72-75 again, a description far taller
// than its label; ComponentGrid.cpp:93 asserts each share is in [0, 1].
TEST_CASE("PL-07 a long description keeps both shares in [0, 1] and their sum at 1 (MultiLineMenuEntry.cpp:72-75)") {
	for (float k : {10.0f, 20.0f}) {
		Shares s; s.layout(26, 26 * k);
		CAPTURE(k);
		CHECK(s.p0 >= 0); CHECK(s.p1 <= 1.0f);
		CHECK(s.p0 + s.p1 == doctest::Approx(1.0f));
	}
}

// 3.5 / PL-08 (#1315): TextComponent.cpp:338 (the automatic height), :350
// (the width the glyphs are laid out at, :413) and :483 (the marquee's
// length). A font that wraps words greedily at a width, 10 px a character.
namespace Utils { namespace String { std::string toUpper(const std::string& s) { std::string r = s; for (auto& c : r) if (c >= 'a' && c <= 'z') c = c - 'a' + 'A'; return r; } } }
struct WrapFont {
	float cw = 10, lh = 20;
	std::string wrapText(const std::string& t, float w) const {
		std::string out, line, word; std::istringstream in(t);
		while (in >> word) {
			std::string next = line.empty() ? word : line + " " + word;
			if (!line.empty() && next.size() * cw > w) { out += line + "\n"; line = word; } else line = next;
		}
		return out + line;
	}
	Vec2f sizeWrappedText(const std::string& t, float w, float = 1.5f) const {
		auto s = wrapText(t, w); int n = 1; for (char c : s) n += c == '\n'; return Vec2f(w, n * lh);
	}
};
struct TextMeasure {
	Vec2f mSize; V4 mPadding; std::shared_ptr<WrapFont> mFont = std::make_shared<WrapFont>(); bool mUppercase = false; std::string mText; float mLineSpacing = 1.5f; int mTextLength = -1;
	Vec2f getSize() const { return mSize; }
	void measure() {
#include "x_text_measure.inc"
	}
	int drawnWidth() {
#include "x_text_drawn.inc"
		return sx;
	}
	void marqueeLength() {
#include "x_text_marquee_len.inc"
	}
	float drawnLines() { return mFont->sizeWrappedText(mText, drawnWidth()).y(); }
};
TEST_CASE("3.5 PL-08 a padded text is measured at the width it is drawn at (TextComponent.cpp:338, :350, :483)") {
	TextMeasure t; t.mSize = Vec2f(640, 0); t.mPadding = V4{16, 4, 16, 4};
	t.mText = "abcdefgh abcdefgh abcdefgh abcdefgh abcdefgh abcdefgh abcdefgh"; // 620 px: one line at 640, two at 608
	t.measure();
	CHECK(t.mSize.y() == doctest::Approx(t.drawnLines() + 4 + 4));
	t.marqueeLength();
	CHECK((float)t.mTextLength == doctest::Approx(t.drawnLines()));
}

// PL-15 (#1320): ComponentList.cpp:11 and :491-494, the row inset.
#include "x_list_inset_define.inc"
struct ComponentList { static float rowInset(); };
#include "x_list_inset.inc"
TEST_CASE("PL-15 the row inset is 10 px at 640 and scales with the panel (ComponentList.cpp:11, :491-494)") {
	gW = 640; CHECK(ComponentList::rowInset() == doctest::Approx(10));
	gW = 1280; CHECK(ComponentList::rowInset() == doctest::Approx(20));
	gW = 640;
}

// PL-30 (#1326): ImageComponent.cpp:67-82 (setSize) under
// WebImageComponent.cpp's resize(), in a resizing cell of a grid whose
// onSizeChanged sizes the cell again (ComponentGrid.cpp:174-175).
inline bool operator==(const Vec2f& a, const Vec2f& b) { return a.x() == b.x() && a.y() == b.y(); }
inline bool operator!=(const Vec2f& a, const Vec2f& b) { return !(a == b); }
struct Rect4 { float v[4]; bool operator!=(const Rect4& o) const { for (int i = 0; i < 4; i++) if (v[i] != o.v[i]) return true; return false; } };
struct ComponentGrid;
struct ImgBase {
	Vec2f mSize; std::vector<int> mChildren; ComponentGrid* parent = nullptr; int baseResizes = 0;
	void setSize(float w, float h) { mSize = Vec2f(w, h); }
	Rect4 getClientRect() const { return Rect4{{0, 0, mSize.x(), mSize.y()}}; }
	void recalcChildrenLayout() {}
	void onSizeChanged() {}
	void resize() { baseResizes++; }
	ComponentGrid* getParent() const { return parent; }
};
struct ComponentGrid {
	struct WebImg* cell = nullptr; Vec2f cellSize = Vec2f(200, 150); int depth = 0, most = 0;
	template <typename T> bool isKindOf() const { return true; }
	void onSizeChanged();
};
struct TexD { void setRequired(bool) {} bool isLoaded() const { return true; } };
// S5 (#1328): the fixed setImage(texture) also cancels a pending load; the
// double carries what those lines read, unused by the pin's lines.
struct TextureResource { static void cancelAsync(const std::shared_ptr<TexD>&) {} };
struct BusyD { void setSize(const Vec2f&) {} };
struct WebImg : ImgBase {
	using GuiComponent = ImgBase; using ImageComponent = ImgBase; using Vector2f = Vec2f;
	std::shared_ptr<TexD> mTexture = std::make_shared<TexD>(), mLoadingTexture; bool mTextureLoaded = false, mLoadingTextureLoaded = false; Vec2f mTargetSize; BusyD* mBusyAnim = nullptr;
	bool isShowing() const { return true; }
	void cancelPendingLoad() {
#if __has_include("x_img_cancel.inc")
#include "x_img_cancel.inc"
#endif
	}
	void setSize(float w, float h) {
#include "x_image_setsize.inc"
	}
	void setImage(const std::shared_ptr<TexD>& texture) {
#include "x_image_settexture.inc"
	}
	void resize() {
#include "x_web_resize.inc"
	}
	void onSizeChanged() {}
};
void ComponentGrid::onSizeChanged() {
	depth++; if (depth > most) most = depth;
	if (depth <= 4) cell->setSize(cellSize.x(), cellSize.y()); // the cell's setSize (ComponentGrid.cpp:174-175)
	depth--;
}
TEST_CASE("PL-30 an image in a resizing cell is sized once, not again from its own notice (ImageComponent.cpp:65-83)") {
	ComponentGrid g; WebImg img; img.parent = &g; g.cell = &img;
	img.setSize(200, 150);
	CHECK(g.most <= 2);
	// ruling 3: a texture change at the same size still resizes (setImage calls resize() itself, ImageComponent.cpp:455-467)
	g.most = 0; int before = img.baseResizes;
	img.setImage(std::make_shared<TexD>());
	CHECK(img.baseResizes > before); CHECK(g.most <= 2);
	// a new size still sizes the image (the grid then sizes it back to its cell)
	int r = img.baseResizes; img.setSize(300, 150); CHECK(img.baseResizes > r);
}

// 3.25: ComponentList.h:25-26, the dim.
namespace ComponentListFlagsD {
#include "x_list_dimmed.inc"
}
TEST_CASE("3.25 a dimmed colour keeps its RGB and takes alpha 0x50 (ComponentList.h:25-26)") {
	CHECK(ComponentListFlagsD::dimmed(0xFFFFFFFF) == 0xFFFFFF50u);
	CHECK(ComponentListFlagsD::dimmed(0x11223344) == 0x11223350u);
	CHECK(ComponentListFlagsD::DIMMED_ALPHA == 0x50);
}

// 3.28: ComponentList.cpp:298-318, updateCameraOffset.
struct ListCamera {
	struct Row { float h; }; struct Entry { Row data; };
	std::vector<Entry> mEntries; int mCursor = 0; float mSelectorBarOffset = 0, mCameraOffset = -1; Vec2f mSize = Vec2f(300, 300);
	float getRowHeight(const Row& r) const { return r.h; }
	float getTotalRowHeight() const { float t = 0; for (auto& e : mEntries) t += e.data.h; return t; }
	void update() {
#include "x_list_camera.inc"
	}
};
TEST_CASE("3.28 the menu list's camera: the last row at the bottom, the first at 0, a cursor of -1 at 0 (ComponentList.cpp:295-319)") {
	ListCamera c; c.mEntries.assign(20, ListCamera::Entry{{30}});
	c.mCursor = 15; c.mSelectorBarOffset = 15 * 30; c.update(); CHECK(c.mCameraOffset == doctest::Approx(300));
	c.mCursor = 0; c.mSelectorBarOffset = 0; c.update(); CHECK(c.mCameraOffset == doctest::Approx(0));
	c.mCursor = -1; c.update(); CHECK(c.mCameraOffset == doctest::Approx(0)); // the signed/unsigned compare reads -1 as past the end
}

// ---- S4 (stage E): the words and the prompts ----

// PL-10 (#1317): RatingComponent.cpp:262-267, the rating's OK prompt.
static std::vector<HelpPrompt> ratingPrompts() {
#include "x_rating_prompts.inc"
}
TEST_CASE("PL-10 the rating's prompt is a translated upper-case verb (RatingComponent.cpp:262-267)") {
	gSeen.clear(); auto p = ratingPrompts();
	REQUIRE(p.size() == 1);
	CHECK(gSeen.count(p[0].second) == 1);
	CHECK(p[0].second == "ADD STAR");
}

// PL-11 (#1318): VideoComponent.cpp:347-352; the component takes no input.
static std::vector<HelpPrompt> videoPrompts() {
#include "x_video_prompts.inc"
}
TEST_CASE("PL-11 a video component offers no prompt, since it takes no input (VideoComponent.cpp:347-352)") {
	auto p = videoPrompts();
	CHECK(p.empty());
	for (auto& h : p) CHECK_FALSE((h.first == BUTTON_BACK && h.second == "SELECT"));
}

// PL-19 (#1321): CarouselComponent.cpp:354-364 and OptionListComponent.h:636-644.
struct CarouselP { enum class CarouselType { HORIZONTAL, VERTICAL, VERTICAL_WHEEL, HORIZONTAL_WHEEL }; CarouselType mType = CarouselType::HORIZONTAL; int n = 1;
	int size() const { return n; }
	std::vector<HelpPrompt> prompts() {
#include "x_carousel_prompts.inc"
	} };
struct OptionP { bool mMultiSelect = false; std::vector<int> mEntries;
	std::vector<HelpPrompt> prompts() {
#include "x_option_prompts.inc"
	} };
TEST_CASE("PL-19 a one-entry carousel and a one-value option row offer no direction (CarouselComponent.cpp:358-361, OptionListComponent.h:639-640)") {
	CarouselP one; CHECK(one.prompts().empty());
	CarouselP three; three.n = 3; CHECK(three.prompts().size() == 1);
	OptionP o; o.mEntries = {1};
	for (auto& h : o.prompts()) CHECK(h.first != "left/right");
	OptionP o2; o2.mEntries = {1, 2}; CHECK(o2.prompts().size() == 2);
}

// 3.13 / PL-25 (#1322): DateTimeEditComponent.cpp:251-260, an unset date.
enum DisplayModeD { DISP_DATE, DISP_RELATIVE_TO_NOW };
struct TimeD { long t = 0; long getTime() const { return t; } };
namespace Utils { namespace Time {
	std::string getElapsedSinceString(long) { return "AGO"; }
	std::string timeToString(const TimeD& t, const std::string&) { return std::to_string(t.t); }
	int daysInMonth(int year, int month) { static const int d[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}; return month == 2 && ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) ? 29 : d[month - 1]; }
} }
struct DateD { DisplayModeD mDisplayMode = DISP_DATE; TimeD mTime; std::string mDateFormat = "%Y";
	std::string getDisplayString() const {
#include "x_date_display.inc"
	} };
TEST_CASE("3.13 PL-25 an unset date reads <NOT SET> (DateTimeEditComponent.cpp:251-260)") {
	DateD d; gSeen.clear();
	CHECK(d.getDisplayString() == "<NOT SET>");
	CHECK(gSeen.count("<NOT SET>") == 1);
	d.mTime.t = 42; CHECK(d.getDisplayString() == "42");
}

// PL-29 (#1325): HelpComponent.cpp:95-156 (the fit and the grid) and
// :208-214 (setOpacity), over doubles that record a grid built with no
// column and a dereference of a null grid instead of crashing.
namespace helpns {
static bool gZeroColumnGrid = false;
namespace Math { inline float round(float v) { return std::floor(v + 0.5f); } }
namespace Renderer { inline int getScreenWidth() { return 640; } }
#include "x_help_spacing.inc"
struct Window {};
struct FontH { float getLetterHeight() const { return 16; } Vec2f sizeText(const std::string& t) const { return Vec2f(10.0f * t.size(), 20); } };
struct ImageComponent { float w = 0; ImageComponent(Window*, bool) {} void setIsLinear(bool) {} void setImage(int) {} void setColorShift(unsigned) {} void setResize(float, float h) { w = h; } Vec2f getSize() const { return Vec2f(w, w); } void setOpacity(unsigned char) {} };
struct TextComponent { std::string text; float w; TextComponent(Window*, const std::string& t, const std::shared_ptr<FontH>& f, unsigned) : text(t), w(f->sizeText(t).x()) {}
	Vec2f getSize() const { return Vec2f(w, 20); } void setSize(float nw, float) { w = nw; } void setGlowSize(int) {} void setGlowColor(unsigned) {} void setGlowOffset(float, float) {} void setOpacity(unsigned char) {} };
struct InputConfig { static std::string buttonLabel(const std::string& b) { return b; } };
struct Vector2i { int a, b; Vector2i(int x, int y) : a(x), b(y) {} int x() const { return a; } int y() const { return b; } };
struct Child { void setOpacity(unsigned char) {} };
struct ComponentGrid { int cols; std::vector<Child> kids;
	ComponentGrid(Window*, const Vector2i& d) : cols(d.x()) { if (d.x() <= 0) gZeroColumnGrid = true; kids.resize(cols > 0 ? cols : 0); }
	void setSize(float, float) {} int getChildCount() const { return (int)kids.size(); } Child* getChild(int i) { return &kids[i]; } };
struct GridPtr { std::shared_ptr<ComponentGrid> p; bool nullDeref = false;
	GridPtr& operator=(std::shared_ptr<ComponentGrid> q) { p = q; return *this; } void reset() { p.reset(); } explicit operator bool() const { return (bool)p; }
	ComponentGrid* operator->() { static ComponentGrid dummy(nullptr, Vector2i(1, 1)); if (!p) { nullDeref = true; return &dummy; } return p.get(); } };
struct Style { std::shared_ptr<FontH> font = std::make_shared<FontH>(); unsigned iconColor = 0, textColor = 0, glowColor = 0; int glowSize = 0; Vec2f glowOffset; };
struct GuiBase { void setOpacity(unsigned char) {} };
struct HelpD : GuiBase { using GuiComponent = GuiBase;
	Window* mWindow = nullptr; Style mStyle; GridPtr mGrid; std::vector<std::pair<std::string, std::string>> mPrompts;
	int getIconTexture(const std::string&) { return 0; }
	size_t kept = 0; float firstWidth = -1;
	void fit(int maxWidth) {
		std::shared_ptr<FontH>& font = mStyle.font;
		std::vector<std::pair<std::shared_ptr<ImageComponent>, std::shared_ptr<TextComponent>>> items;
		bool is43screen = false;
#include "x_help_fit.inc"
		kept = items.size(); if (!items.empty()) firstWidth = items[0].second->getSize().x();
	}
	void setOpacity(unsigned char opacity) {
#include "x_help_opacity.inc"
	}
};
}
TEST_CASE("PL-29 a first prompt wider than the bar is kept and clipped, and a bar with no grid takes an opacity (HelpComponent.cpp:95-156, :208-214)") {
	helpns::gZeroColumnGrid = false;
	helpns::HelpD h; h.mPrompts = {{"a", "A LABEL FAR WIDER THAN THIS BAR CAN EVER HOLD"}, {"b", "BACK"}};
	h.fit(200);
	CHECK(h.kept == 1);
	CHECK_FALSE(helpns::gZeroColumnGrid);
	CHECK(h.firstWidth < 200);
	helpns::HelpD none; none.mGrid.reset(); none.setOpacity(128);
	CHECK_FALSE(none.mGrid.nullDeref);
}

// 3.1-3.3: ComponentGrid.cpp:329-379 (moveCursor), :396-414 (canMoveCursor), :519-553 (getHelpPrompts).
namespace gridns {
struct Vector2i { int a, b; Vector2i(int x = 0, int y = 0) : a(x), b(y) {} int x() const { return a; } int y() const { return b; }
	Vector2i operator+(const Vector2i& o) const { return Vector2i(a + o.a, b + o.b); } Vector2i& operator+=(const Vector2i& o) { a += o.a; b += o.b; return *this; } };
struct Comp { std::vector<HelpPrompt> p; std::vector<HelpPrompt> getHelpPrompts() { return p; } };
struct GridEntry { bool canFocus; Comp* component; };
struct Grid { Vector2i mGridSize, mCursor; std::map<std::pair<int, int>, GridEntry> cells; int moved = 0;
	const GridEntry* getCellAt(const Vector2i& c) const { auto it = cells.find({c.x(), c.y()}); return it == cells.end() ? nullptr : &it->second; }
	void onCursorMoved(Vector2i, Vector2i) { moved++; }
	bool moveCursor(Vector2i dir) {
#include "x_grid_move.inc"
	}
	bool canMoveCursor(const Vector2i& dir) const {
#include "x_grid_canmove.inc"
	}
	std::vector<HelpPrompt> getHelpPrompts() {
#include "x_grid_prompts.inc"
	} };
}
TEST_CASE("3.1-3.3 the grid offers a direction only where a focusable cell lies, and moves there (ComponentGrid.cpp:329-414, :519-553)") {
	gridns::Comp c; gridns::Grid g; g.mGridSize = gridns::Vector2i(3, 1);
	g.cells[{0, 0}] = {true, &c}; g.cells[{1, 0}] = {false, &c}; g.cells[{2, 0}] = {true, &c};
	CHECK(g.canMoveCursor(gridns::Vector2i(1, 0)));
	CHECK_FALSE(g.canMoveCursor(gridns::Vector2i(-1, 0)));
	CHECK_FALSE(g.canMoveCursor(gridns::Vector2i(0, 1)));
	auto p = g.getHelpPrompts(); REQUIRE(p.size() == 1); CHECK(p[0].first == "left/right");
	CHECK(g.moveCursor(gridns::Vector2i(1, 0))); CHECK(g.mCursor.x() == 2); CHECK(g.moved == 1);
	CHECK_FALSE(g.moveCursor(gridns::Vector2i(1, 0))); CHECK(g.mCursor.x() == 2);
	gridns::Grid one; one.mGridSize = gridns::Vector2i(1, 1); one.cells[{0, 0}] = {true, &c};
	CHECK(one.getHelpPrompts().empty());
}

// 3.12: DateTimeEditComponent.cpp:124-160, a step through the date.
struct DateStep { tm mTime{}; int mEditIndex = 0, mMonthIndex = 0, mDayIndex = 1, mYearIndex = 2, cache = 0;
	void updateTextCache() { cache++; }
	void step(int incDir) {
#include "x_date_step.inc"
	} };
TEST_CASE("3.12 the date steps wrap the month and the day and keep the day inside its month (DateTimeEditComponent.cpp:124-160)") {
	DateStep d; d.mTime.tm_year = 124; d.mTime.tm_mon = 0; d.mTime.tm_mday = 31; // 31 January 2024
	d.mEditIndex = d.mMonthIndex; d.step(1); CHECK(d.mTime.tm_mon == 1); CHECK(d.mTime.tm_mday == 29);
	d.mEditIndex = d.mMonthIndex; d.step(-1); d.step(-1); CHECK(d.mTime.tm_mon == 11);
	d.mEditIndex = d.mDayIndex; d.mTime.tm_mday = 1; d.step(-1); CHECK(d.mTime.tm_mday == 31);
	d.mEditIndex = d.mYearIndex; d.mTime.tm_year = 0; d.step(-1); CHECK(d.mTime.tm_year == 0);
}

// 3.17: ComponentTab.cpp:320-345, the strip's prompts.
struct TabP { struct Elem { gridns::Comp* component; }; struct Data { std::vector<Elem> elements; }; struct Entry { Data data; };
	std::vector<Entry> mEntries; int mCursor = 0;
	int size() const { return (int)mEntries.size(); }
	std::vector<HelpPrompt> prompts() {
#include "x_tab_prompts.inc"
	} };
TEST_CASE("3.17 the tab strip offers SWITCH TAB only with two tabs and no sideways prompt of its own (ComponentTab.cpp:320-345)") {
	gridns::Comp c; TabP one; one.mEntries = {TabP::Entry{{{TabP::Elem{&c}}}}};
	CHECK(one.prompts().empty());
	TabP two = one; two.mEntries.push_back(two.mEntries[0]);
	auto p = two.prompts(); REQUIRE(p.size() == 1); CHECK(p[0].second == "SWITCH TAB");
	gridns::Comp side; side.p = {HelpPrompt("left/right", "CHANGE")};
	TabP s2; s2.mEntries = {TabP::Entry{{{TabP::Elem{&side}}}}, TabP::Entry{{{TabP::Elem{&side}}}}};
	CHECK(s2.prompts().size() == 1);
}

// 3.31: SliderComponent.cpp:234-257, the clamp and the AUTO sentinel.
struct SliderSet { float mValue = 0, mMin = 0, mMax = 100, mSingleIncrement = 1; bool mIsAutoMode = false;
	void set(float value) {
#include "x_slider_set.inc"
	} };
TEST_CASE("3.31 the slider clamps to its range and keeps its AUTO sentinel only in auto mode (SliderComponent.cpp:234-257)") {
	SliderSet s; s.set(-5); CHECK(s.mValue == 0); s.set(250); CHECK(s.mValue == 100); s.set(42); CHECK(s.mValue == 42);
	s.set(-1); CHECK(s.mValue == 0);
	SliderSet a; a.mIsAutoMode = true; a.set(-1); CHECK(a.mValue == -1);
}

// 3.32: RatingComponent.cpp:192-204, five presses make five stars.
#define NUM_RATING_STARS 5
struct RatingStep { float mValue = 0; int verts = 0; void updateVertices() { verts++; }
	void press() {
#include "x_rating_step.inc"
	} };
TEST_CASE("3.32 five presses reach five stars and the sixth wraps to none (RatingComponent.cpp:192-204)") {
	RatingStep r; for (int i = 0; i < 5; i++) r.press();
	CHECK(r.mValue == doctest::Approx(1.0f)); r.press(); CHECK(r.mValue == doctest::Approx(0.0f));
}

// 3.34: CarouselComponent.cpp:183-202, the shortest way round.
struct CarouselPath { float mCamOffset = 0; int mCursor = 0; std::vector<int> mEntries; float endPosOut = -99;
	void path() {
#include "x_carousel_path.inc"
		endPosOut = endPos;
	} };
TEST_CASE("3.34 the carousel takes the shortest way round, with one entry and with none (CarouselComponent.cpp:183-202)") {
	CarouselPath c; c.mEntries.assign(10, 0); c.mCamOffset = 9; c.mCursor = 0; c.path(); CHECK(c.endPosOut == doctest::Approx(10));
	CarouselPath one; one.mEntries.assign(1, 0); one.path(); CHECK(one.endPosOut == doctest::Approx(0));
	CarouselPath none; none.path(); CHECK(none.endPosOut == doctest::Approx(0));
}

// ---- S5 (stage E): the web image ----

// 3.21, PL-13 (#1319), PL-31 (#1327): WebImageComponent's setImage, update
// and render's request, over a file system whose exists() caches its
// answers and whose writes and removals erase the cached one (FileCache,
// FileSystemUtil.cpp:144, :182-197), and a server scripted per request.
struct LogD { template <typename T> LogD& operator<<(const T&) { return *this; } };
#define LOG(level) LogD()
namespace webns {
std::map<std::string, std::string> gFiles; std::map<std::string, bool> gExistsCache; std::vector<std::string> gAsked, gAnswers;
std::string md5(const std::string& s) { char b[32]; snprintf(b, sizeof b, "%016zx", std::hash<std::string>()(s)); return b; }
struct Paths { static std::string getUserEmulationStationPath() { return "/es"; } };
namespace Utils {
	namespace String { bool startsWith(const std::string& s, const std::string& p) { return s.rfind(p, 0) == 0; } }
	namespace FileSystem {
		bool exists(const std::string& p) { auto it = gExistsCache.find(p); if (it != gExistsCache.end()) return it->second; bool e = gFiles.count(p) > 0 || p == "/es/tmp"; gExistsCache[p] = e; return e; }
		bool removeFile(const std::string& p) { gFiles.erase(p); gExistsCache.erase(p); return true; }
		void serverWrite(const std::string& p, const std::string& bytes) { gFiles[p] = bytes; gExistsCache.erase(p); } // HttpReq's .tmp then renameFile
		size_t getFileSize(const std::string& p) { return gFiles.count(p) ? gFiles[p].size() : 0; }
		std::string getGenericPath(const std::string& p) { return p; }
		std::string getCanonicalPath(const std::string& p) { return p; }
		std::string getParent(const std::string& p) { auto i = p.find_last_of('/'); return i == std::string::npos ? "" : p.substr(0, i); }
		bool createDirectory(const std::string&) { return true; }
		long getFileCreationDate(const std::string&) { return 0; }
	}
	namespace Time { struct DateTime { static DateTime now() { return DateTime(); } double elapsedSecondsSince(long) const { return 0; } }; }
	namespace OfflineProxy { inline bool isProxyUrl(const std::string&) { return false; } const std::string StoreOnlyHeader = "X-Store-Only: 1"; }
}
struct HttpReqOptions { std::string out; std::vector<std::string> customHeaders; HttpReqOptions(const std::string& o) : out(o) {} };
struct HttpReq { enum Status { REQ_IN_PROGRESS, REQ_SUCCESS, REQ_FAILED }; Status st = REQ_SUCCESS;
	HttpReq(const std::string& url, HttpReqOptions* o) { gAsked.push_back(url); std::string a = gAnswers.empty() ? "" : gAnswers.front(); if (!gAnswers.empty()) gAnswers.erase(gAnswers.begin()); Utils::FileSystem::serverWrite(o->out, a); }
	Status status() const { return st; } };
struct MaxSizeInfo { bool e = true; bool empty() const { return e; } };
struct BusyComponent { BusyComponent(void*, const std::string&) {} void setBackgroundVisible(bool) {} void setSize(const Vec2f&) {} void update(int) {} };
#include "x_web_url.inc"
#include "x_web_key.inc"
struct WebBase { std::string shown = "-"; void setImage(const std::string& p, bool = false, const MaxSizeInfo& = MaxSizeInfo(), bool = true, bool = false) { shown = p; }
	void setImage(const char*, size_t) { shown = ""; } void update(int) {} };
struct WebD : WebBase { using ImageComponent = WebBase;
	HttpReq* mRequest = nullptr; std::string mUrlToLoad, mLocalFile; MaxSizeInfo mMaxSize; double mKeepInCacheDuration = -1; bool mWaitLoaded = false; BusyComponent* mBusyAnim = nullptr; void* mWindow = nullptr; Vec2f mSize = Vec2f(64, 64);
	void resize() {}
	void setImage(const std::string& path, bool tile = false, const MaxSizeInfo& maxSize = MaxSizeInfo(), bool checkFileExists = true, bool allowMultiImagePlaylist = false) {
#include "x_web_setimage.inc"
	}
	void update(int deltaTime) {
#include "x_web_update.inc"
	}
	void renderRequest() {
#include "x_web_render_req.inc"
	}
	void frame() { renderRequest(); update(16); }
};
void reset() { gFiles.clear(); gExistsCache.clear(); gAsked.clear(); gAnswers.clear(); }
}
TEST_CASE("3.21 a badge the cache missed once is shown when the image arrives (WebImageComponent.cpp:164, :220; L-09)") {
	webns::reset(); webns::gAnswers = {"PNG"};
	webns::WebD w; w.setImage("http://h/b/1.png"); w.frame();
	CHECK(webns::gAsked.size() == 1); CHECK(w.shown != "-"); CHECK(w.shown != "");
}
TEST_CASE("3.21 PL-13 a 0-byte answer is not kept as done: the page asks nothing more, and the next bind asks again (WebImageComponent.cpp:220-231)") {
	webns::reset(); webns::gAnswers = {"", "PNG"};
	webns::WebD w; w.setImage("http://h/b/1.png"); w.frame();
	CHECK(webns::gAsked.size() == 1); CHECK(w.shown == "-");
	CHECK(w.mLocalFile.empty()); // the uncached state: the component keeps no cache path for an answer it did not keep
	w.frame(); w.frame(); CHECK(webns::gAsked.size() == 1); // ruling 5: no timer on the page
	w.setImage("http://h/b/1.png"); w.frame();
	CHECK(webns::gAsked.size() == 2); CHECK(w.shown != "-");
}
TEST_CASE("PL-31 a rebind to a local or cached image leaves no queued URL behind (WebImageComponent.cpp:128-195)") {
	webns::reset(); webns::gAnswers = {"PNG", "PNG"};
	webns::WebD w; w.setImage("http://h/b/1.png"); w.setImage("/roms/x.png"); w.frame();
	CHECK(webns::gAsked.empty()); CHECK(w.shown == "/roms/x.png");
	webns::reset(); webns::gAnswers = {"PNG"};
	webns::WebD seed; seed.setImage("http://h/b/2.png"); seed.frame(); // 2.png now in the cache
	webns::gAsked.clear();
	webns::WebD v; v.setImage("http://h/b/3.png"); v.setImage("http://h/b/2.png"); v.frame();
	CHECK(webns::gAsked.empty());
}

// PL-32 (#1328): ImageComponent.cpp's two setImage overloads (from memory
// and from a shared texture) against a load pending from an earlier path,
// then watchTextureLoading's install (:821-839).
namespace imgns {
struct TexR { bool loaded = false, required = false; int id = 0; void setRequired(bool r) { required = r; } bool isLoaded() const { return loaded; } void initFromMemory(const char*, size_t) { loaded = true; } };
std::vector<int> gCancelled;
struct TextureResource { static std::shared_ptr<TexR> get(const std::string&, bool) { auto t = std::make_shared<TexR>(); t->id = 99; return t; } static void cancelAsync(const std::shared_ptr<TexR>& t) { gCancelled.push_back(t->id); } };
struct ImgD { std::string mPath = "/old.png"; std::shared_ptr<TexR> mTexture, mLoadingTexture; bool mTextureLoaded = false, mLoadingTextureLoaded = false;
	bool isShowing() const { return true; } void resize() {} void updateVertices() {} void updateColors() {}
	void cancelPendingLoad() {
#if __has_include("x_img_cancel.inc")
#include "x_img_cancel.inc"
#endif
	}
	void setImageMem(const char* path, size_t length, bool tile = false) {
#include "x_img_setmem.inc"
	}
	void setImageTex(const std::shared_ptr<TexR>& texture) {
#include "x_image_settexture.inc"
	}
	bool watch() {
#include "x_img_watch.inc"
		return false;
	} };
}
TEST_CASE("PL-32 an image set from memory or a shared texture is not replaced by an earlier path's pending load (ImageComponent.cpp:443-474, :821-839)") {
	for (int overload = 0; overload < 2; overload++) {
		CAPTURE(overload);
		imgns::ImgD i; auto pending = std::make_shared<imgns::TexR>(); pending->id = 7; i.mLoadingTexture = pending;
		auto mine = std::make_shared<imgns::TexR>(); mine->id = 5; mine->loaded = true;
		if (overload == 0) i.setImageMem("bytes", 5); else i.setImageTex(mine);
		auto set = i.mTexture;
		pending->loaded = true; i.watch();
		CHECK(i.mTexture == set);
		CHECK(i.mTexture != pending);
	}
}

// 3.22-3.24: ImageComponent.cpp:103-109 (the size a turn fits), :287-297
// (the corners' turn), :500 (the normaliser).
struct TurnD { using Vector2f = Vec2f; float mDisplayAspect = 0; int mDisplayRotation = 0; struct V { Vec2f tex; } mVertices[4];
	Vec2f fitSize(Vec2f physicalSize) {
#include "x_img_turn_fit.inc"
		return textureSize;
	}
	void corners() {
#include "x_img_turn_corners.inc"
	}
	int norm(int quarterTurns) {
#include "x_img_turn_norm.inc"
		return quarterTurns;
	} };
TEST_CASE("3.22-3.24 a quarter turn swaps the fitted size, four turns are the identity, and turns normalise to 0-3 (ImageComponent.cpp:103-109, :287-297, :500)") {
	TurnD t; t.mDisplayRotation = 1; Vec2f s = t.fitSize(Vec2f(320, 240)); CHECK(s.x() == 240); CHECK(s.y() == 320);
	t.mDisplayAspect = 4.0f / 3.0f; s = t.fitSize(Vec2f(256, 224)); CHECK(s.x() == doctest::Approx(224)); CHECK(s.y() == doctest::Approx(224 * 4.0f / 3.0f));
	TurnD c; c.mDisplayRotation = 1; c.mVertices[0].tex = Vec2f(0, 0); c.mVertices[1].tex = Vec2f(0, 1); c.mVertices[2].tex = Vec2f(1, 0); c.mVertices[3].tex = Vec2f(1, 1);
	for (int k = 0; k < 4; k++) c.corners();
	CHECK(c.mVertices[0].tex == Vec2f(0, 0)); CHECK(c.mVertices[1].tex == Vec2f(0, 1)); CHECK(c.mVertices[2].tex == Vec2f(1, 0)); CHECK(c.mVertices[3].tex == Vec2f(1, 1));
	CHECK(t.norm(-1) == 3); CHECK(t.norm(5) == 1); CHECK(t.norm(4) == 0); CHECK(t.norm(0) == 0);
}

// ---- S6 (stage E): the image grid ----
// The template ImageGridComponent<T> (ImageGridComponent.h) is not compiled
// whole; each case lifts the member's body into a double of the grid with
// its tiles, its entries and the fields that body reads.
namespace igrid {
#define EXTRAITEMS 2
#define ALLOWANIMATIONS (gAnimations)
static bool gAnimations = true;
enum CursorState { CURSOR_STOPPED, CURSOR_SCROLLING };
enum class CenterSelection { NEVER, ALWAYS, PARTIAL };
namespace Math {
	template <typename A, typename B> auto max(A a, B b) -> decltype(a + b) { return a > b ? a : b; }
	inline float floorf(float v) { return std::floor(v); } inline float ceilf(float v) { return std::ceil(v); } }
struct V2f { float a = 0, b = 0; V2f(float x = 0, float y = 0) : a(x), b(y) {} float& x() { return a; } float& y() { return b; } float x() const { return a; } float y() const { return b; }
	V2f operator+(const V2f& o) const { return V2f(a + o.a, b + o.b); } V2f operator/(const V2f& o) const { return V2f(a / o.a, b / o.b); } V2f operator/(float d) const { return V2f(a / d, b / d); } };
struct V2i { int a = 0, b = 0; V2i(int x = 0, int y = 0) : a(x), b(y) {} int& x() { return a; } int& y() { return b; } int x() const { return a; } int y() const { return b; } operator V2f() const { return V2f(a, b); } };
struct V3f { float a = 0, b = 0, c = 0; V3f(float x = 0, float y = 0, float z = 0) : a(x), b(y), c(z) {} static V3f Zero() { return V3f(); } bool operator==(const V3f& o) const { return a == o.a && b == o.b && c == o.c; } };
struct V4f { float p[4] = {0, 0, 0, 0}; float x() const { return p[0]; } float y() const { return p[1]; } float z() const { return p[2]; } float w() const { return p[3]; } };
struct Tile { bool visible = true, selected = false, item = true; int videos = 0, id = 0;
	bool isVisible() const { return visible; } void setVisible(bool v) { visible = v; } bool isSelected() const { return selected; }
	void setSelected(bool s, bool = true, V3f* = nullptr, bool = false) { selected = s; } bool hasItemTemplate() const { return item; } void startVideo() { videos++; } V3f getBackgroundPosition() const { return V3f(); } void render(int) {} };
struct Data { std::shared_ptr<Tile> tile; std::string texturePath; };
struct Entry { Data data; int object = 0; };
struct Grid {
	using Vector2f = V2f; using Vector2i = V2i; using Vector3f = V3f;
	std::vector<Entry> mEntries; std::vector<std::shared_ptr<Tile>> mVisibleTiles; std::map<int, std::shared_ptr<Tile>> mScrollLoopTiles;
	int mCursor = 0, mLastCursor = -1, mStartPosition = 0; CursorState mLastCursorState = CURSOR_STOPPED; bool mEntriesDirty = false, mScrollLoop = false, mAnimateSelection = false, mLastRowPartial = false, vertical = true;
	float mCameraOffset = 0; V2f mSize = V2f(640, 480), mMargin = V2f(10, 10), mTileSize = V2f(100, 100); V2i mGridDimension, mGridSizeOverride, mAutoLayout; V4f mPadding;
	CenterSelection mCenterSelection = CenterSelection::NEVER; int callbacks = 0; std::function<void(CursorState)> mCursorChangedCallback = [this](CursorState) { callbacks++; };
	bool isVertical() const { return vertical; } void onCursorChanged(CursorState) {}
	std::shared_ptr<Tile> getSelectedTile() { for (auto& t : mVisibleTiles) if (t->isSelected()) return t; for (auto& e : mEntries) if (e.data.tile && e.data.tile->isSelected()) return e.data.tile; return nullptr; }
	void calcGridDimension() {
#include "x_grid_calcdim.inc"
	}
	void resetGrid() {
#include "x_grid_reset.inc"
	}
	// IList's findEntry and end, for setImage
	std::vector<Entry>::iterator findEntry(int obj) { for (auto it = mEntries.begin(); it != mEntries.end(); ++it) if (it->object == obj) return it; return mEntries.end(); }
	std::vector<Entry>::iterator end() { return mEntries.end(); }
	void setImage(const std::string& imagePath, int obj) {
		Grid* list = this;
#include "x_grid_setimage.inc"
	}
	// ensureVisibleTileExist's tile made for an entry with none (:373-384), as a remake
	void remake() { static int ids = 0; for (auto& e : mEntries) if (!e.data.tile) { e.data.tile = std::make_shared<Tile>(); e.data.tile->id = ++ids; mVisibleTiles.push_back(e.data.tile); } mEntriesDirty = false; }
	void cursorSelection() {
		Vector3f oldPos = Vector3f::Zero();
#include "x_grid_select.inc"
	}
	void cursorCallback(CursorState state) {
		float newCameraOffset = mCameraOffset;
#include "x_grid_callback.inc"
	}
	void cursorMoved(CursorState state) { cursorSelection(); cursorCallback(state); mLastCursor = mCursor; }
};
}
TEST_CASE("PL-33 a reset grid keeps no loop-copy tile to draw (ImageGridComponent.h:505-509, :1381-1435, :762-763)") {
	igrid::Grid g; g.mScrollLoop = true; g.mEntries.resize(3); g.mScrollLoopTiles[-1] = std::make_shared<igrid::Tile>(); g.mScrollLoopTiles[3] = std::make_shared<igrid::Tile>();
	g.mEntries.clear(); g.resetGrid(); // clear(): IList's clear, then resetGrid()
	CHECK(g.mScrollLoopTiles.empty());
	CHECK(g.mVisibleTiles.empty());
}
TEST_CASE("PL-34 an entry's image changed three times leaves one tile in the visible list (ImageGridComponent.h:522-534)") {
	igrid::Grid g; g.mEntries.resize(1); g.mEntries[0].object = 7; g.remake();
	for (auto p : {"a.png", "b.png", "c.png"}) { g.setImage(p, 7); g.remake(); }
	CHECK(g.mVisibleTiles.size() == 1);
	CHECK(g.mVisibleTiles[0] == g.mEntries[0].data.tile);
}
TEST_CASE("PL-35 the cursor reaching an already selected tile still runs the cursor callback (ImageGridComponent.h:1124-1153, :1198-1217)") {
	igrid::gAnimations = true;
	igrid::Grid g; g.mEntries.resize(3); g.remake();
	g.mLastCursor = 0; g.mCursor = 1; g.mEntries[1].data.tile->selected = true; // the tile kept its selected state
	g.cursorMoved(igrid::CURSOR_STOPPED);
	CHECK(g.callbacks == 1);
	CHECK(g.mEntries[1].data.tile->videos == 0); // the restart is the drag's, on the -9999 sentinel only
	g.mLastCursor = -9999; g.mEntries[1].data.tile->selected = true; g.cursorSelection();
	CHECK(g.mEntries[1].data.tile->videos == 1);
}
TEST_CASE("3.9 3.10 the grid's dimensions and its partial last row (ImageGridComponent.h:1439-1468)") {
	igrid::Grid g; g.calcGridDimension();
	CHECK(g.mGridDimension.x() == 5); CHECK(g.mGridDimension.y() == 5 + 2 * EXTRAITEMS); CHECK(g.mLastRowPartial);
	igrid::Grid h; h.mSize = igrid::V2f(650, 440); h.calcGridDimension(); // 660/110 = 6, 450/110 = 4.09
	CHECK(h.mGridDimension.x() == 6); CHECK(h.mGridDimension.y() == 5 + 2 * EXTRAITEMS); CHECK(h.mLastRowPartial);
	igrid::Grid e; e.mSize = igrid::V2f(540, 430); e.calcGridDimension(); // 550/110 = 5, 440/110 = 4: no partial row
	CHECK(e.mGridDimension.y() == 4 + 2 * EXTRAITEMS); CHECK_FALSE(e.mLastRowPartial);
}
