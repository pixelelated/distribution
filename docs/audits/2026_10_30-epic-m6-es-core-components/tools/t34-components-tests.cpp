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
