// T34 (#681): components-tests. Each case lifts the pin's lines verbatim
// (tools/t34-extract.py, each extract refused unless its first and last lines
// hold the code they were written for) into the smallest double that compiles
// them, and asserts the behaviour the component should have: a defect at the
// pin is a FAIL here, the case's "seen to FAIL against the unfixed extract".
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"
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
