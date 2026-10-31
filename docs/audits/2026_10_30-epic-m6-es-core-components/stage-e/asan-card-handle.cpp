// T34 (#681) PL-02 (#1310): a holder keeps what the window gave it for its
// progress card; the window's loop (Window.cpp:1242-1252, doubled) lets the
// card go once it stops running; the holder then calls close() and
// updateText() late, as a worker finishing after the card faded does.
//
// At the pin the window hands out the raw pointer and deletes the card: the
// late calls are a use after free (-fsanitize=address, rc 1). When the tree's
// card has its handle (x_card_handle.inc, lifted from the header), the window
// double takes stage-e/s2-window.patch's shape -- shared_ptrs, a retired list
// drained on its own thread once the window holds the last reference, a
// deleter that hands a last release on another thread back to it -- and the
// holder's lock() fails: the late calls are refused and counted, rc 0.
#include <cstdio>
#include <functional>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

struct AsyncNotificationComponent
#if __has_include("x_card_handle.inc")
	: public std::enable_shared_from_this<AsyncNotificationComponent>
#endif
{
#if __has_include("x_card_handle.inc")
#include "x_card_handle.inc"
#endif
	std::mutex mMutex; std::string mText; bool mClosing = false, mRunning = true; int mFadeTime = 0;
	void close() { mClosing = true; }
	void updateText(const std::string& t, const std::string& = "") { std::unique_lock<std::mutex> lock(mMutex); mText = t; }
	void updateText(const std::string& t, const std::vector<std::string>&) { updateText(t); }
	void updateText(const std::vector<std::string>& t, const std::vector<std::string>&) { updateText(t.empty() ? "" : t[0]); }
	void updateTitle(const std::string&) {}
	void updatePercent(int) {}
	void update(int dt) { if (mClosing && (mFadeTime += dt) > 500) mRunning = false; }
	bool isRunning() { return mRunning; }
};

#if __has_include("x_card_handle.inc")
struct WindowD {
	std::thread::id mUiThread = std::this_thread::get_id();
	std::vector<std::function<void()>> mFunctions;
	std::vector<std::shared_ptr<AsyncNotificationComponent>> mAsyncNotificationComponent, mRetiredAsyncNotifications;
	void postToUiThread(const std::function<void()>& f) { mFunctions.push_back(f); }
	AsyncNotificationComponent::Handle createAsyncNotificationComponent() {
		std::shared_ptr<AsyncNotificationComponent> pc(new AsyncNotificationComponent(), [this](AsyncNotificationComponent* p) {
			if (std::this_thread::get_id() == mUiThread) delete p; else postToUiThread([p] { delete p; }); });
		mAsyncNotificationComponent.push_back(pc);
		return pc->handle();
	}
	void updateAsyncNotifications(int deltaTime) {
		for (int i = mAsyncNotificationComponent.size() - 1; i >= 0; i--) {
			mAsyncNotificationComponent[i]->update(deltaTime);
			if (!mAsyncNotificationComponent[i]->isRunning()) {
				mRetiredAsyncNotifications.push_back(mAsyncNotificationComponent[i]);
				mAsyncNotificationComponent.erase(mAsyncNotificationComponent.begin() + i);
			}
		}
		for (int i = mRetiredAsyncNotifications.size() - 1; i >= 0; i--)
			if (mRetiredAsyncNotifications[i].use_count() == 1)
				mRetiredAsyncNotifications.erase(mRetiredAsyncNotifications.begin() + i);
	}
};
int main() {
	WindowD w;
	auto h = w.createAsyncNotificationComponent();
	if (auto c = h.lock()) { c->updateText("SYNCING"); c->close(); }
	for (int i = 0; i < 40; i++) w.updateAsyncNotifications(16);
	int refused = 0;
	if (auto c = h.lock()) c->close(); else refused++;
	if (auto c = h.lock()) c->updateText("COMPLETED"); else refused++;
	// The holders' own form since the S2 addendum: -> forwards, each call locks.
	h->close(); h->updateText("LATE"); h->updatePercent(100);
	// == nullptr keeps the pointer's meaning: never given a card.
	AsyncNotificationComponent::Handle none;
	bool nullMeaning = (none == nullptr) && !(h == nullptr);
	// A holder mid-call when the card retires: the retired list keeps it
	// until the window holds the last reference, then drops it on its thread.
	auto h2 = w.createAsyncNotificationComponent();
	std::shared_ptr<AsyncNotificationComponent> held = h2.lock();
	held->close();
	for (int i = 0; i < 40; i++) w.updateAsyncNotifications(16);
	size_t keptWhileHeld = w.mRetiredAsyncNotifications.size();
	std::thread([&] { held.reset(); }).join();
	w.updateAsyncNotifications(16);
	size_t afterDrain = w.mRetiredAsyncNotifications.size(), postedAfterDrain = w.mFunctions.size();
	// The one interleaving the drain's count cannot see (a lock() between the
	// count and the erase), modelled as the window letting go while a holder
	// still has it: the holder's release on its own thread hands the delete back.
	auto h3 = w.createAsyncNotificationComponent();
	held = h3.lock();
	w.mAsyncNotificationComponent.clear();
	std::thread([&] { held.reset(); }).join();
	size_t posted = w.mFunctions.size();
	for (auto& f : w.mFunctions) f();
	std::printf("late calls refused: %d of 2; kept while held: %zu, after the drain: %zu; deletes handed back to the window's thread: %zu\n", refused, keptWhileHeld, afterDrain, posted);
	return refused == 2 && nullMeaning && keptWhileHeld == 1 && afterDrain == 0 && postedAfterDrain == 0 && posted == 1 ? 0 : 1;
}
#else
struct WindowD {
	std::vector<AsyncNotificationComponent*> mAsyncNotificationComponent;
	AsyncNotificationComponent* createAsyncNotificationComponent() { auto pc = new AsyncNotificationComponent(); mAsyncNotificationComponent.push_back(pc); return pc; }
	void updateAsyncNotifications(int deltaTime) {
		for (int i = mAsyncNotificationComponent.size() - 1; i >= 0; i--) {
			mAsyncNotificationComponent[i]->update(deltaTime);
			if (!mAsyncNotificationComponent[i]->isRunning()) {
				delete mAsyncNotificationComponent[i];
				mAsyncNotificationComponent.erase(mAsyncNotificationComponent.begin() + i);
			}
		}
	}
};
int main() {
	WindowD w;
	AsyncNotificationComponent* card = w.createAsyncNotificationComponent();
	card->updateText("SYNCING"); card->close();
	for (int i = 0; i < 40; i++) w.updateAsyncNotifications(16);
	card->close();                  // the worker's late close, on the freed card
	card->updateText("COMPLETED");
	std::printf("late calls made through the raw pointer\n");
	return 0;
}
#endif
