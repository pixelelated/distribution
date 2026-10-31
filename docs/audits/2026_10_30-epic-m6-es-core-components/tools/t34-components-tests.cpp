// T34 (#681): components-tests. Each case lifts the pin's lines verbatim
// (tools/t34-extract.py, each extract refused unless its first and last lines
// hold the code they were written for) into the smallest double that compiles
// them, and asserts the behaviour the component should have: a defect at the
// pin is a FAIL here, the case's "seen to FAIL against the unfixed extract".
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"
#include <atomic>
#include <functional>
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

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

// 3.16: HelpComponent.cpp:18-33, the icon key the list passes under French.
#include "x_help_map.inc"
TEST_CASE("3.16 the list's CHOOSE key resolves to an icon under French (ComponentList.cpp:568; HelpComponent.cpp:18-33, :190-194)") {
	// _("up/down") under the pin's French catalog (po :3708-3709, read at stage A)
	const std::map<std::string, std::string> fr = {{"up/down", "haut/bas"}};
	CHECK(ICON_PATH_MAP.count("up/down") == 1);
	CHECK(ICON_PATH_MAP.count(fr.at("up/down")) == 1);
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
struct BusyD { void setSize(const Vec2f&) {} };
struct WebImg : ImgBase {
	using GuiComponent = ImgBase; using ImageComponent = ImgBase; using Vector2f = Vec2f;
	std::shared_ptr<TexD> mTexture = std::make_shared<TexD>(); bool mTextureLoaded = false; Vec2f mTargetSize; BusyD* mBusyAnim = nullptr;
	bool isShowing() const { return true; }
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
