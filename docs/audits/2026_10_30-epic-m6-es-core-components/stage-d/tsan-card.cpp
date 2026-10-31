// T34 (#681) PL-01: the card's close() and update(), lifted verbatim
// (AsyncNotificationComponent.cpp:119-120, :267-274), called from two threads
// as the holders and the interface thread call them. Built with
// -fsanitize=thread: a reported data race is the defect's positive.
#include <thread>
struct Card {
	bool mClosing = false; int mFadeTime = 0; unsigned char mFadeOutOpacity = 0;
	unsigned char getOpacity() const { return 255; }
	void close() {
#include "x_card_close.inc"
	}
	void update(int deltaTime) {
#include "x_card_update.inc"
	}
};
int main() {
	Card c;
	std::thread worker([&] { for (int i = 0; i < 20000; i++) c.close(); });
	for (int i = 0; i < 20000; i++) c.update(16);
	worker.join();
	return 0;
}
