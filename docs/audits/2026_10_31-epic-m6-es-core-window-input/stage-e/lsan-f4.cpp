// T35 (#682) stage E S6, PL-10 (#1350): F4's quit event (InputManager.cpp:792-800, lifted
// verbatim by tools/t35-extract.py as im_f4) under -fsanitize=address, whose LeakSanitizer
// reports at exit what was never freed. SDL_PushEvent copies the event into its queue, as
// SDL's does. Three presses; a leak report is the FAIL at the pin.
#include <vector>
enum { SDL_QUIT = 0x100, SDLK_F4 = 0x4000003D };
struct SDL_Keysym { int sym; };
struct SDL_KeyboardEvent { int type; SDL_Keysym keysym; };   // SDL's own begins with its type
union SDL_Event { int type; SDL_KeyboardEvent key; };
static std::vector<SDL_Event> queue;
static int SDL_PushEvent(SDL_Event* e) { queue.push_back(*e); return 1; }
static bool handle(const SDL_Event& ev)
{
#include "x_im_f4.inc"
	return true;
}
int main()
{
	SDL_Event f4 {};
	f4.key.keysym.sym = SDLK_F4;
	for (int i = 0; i < 3; i++)
		handle(f4);
	return queue.size() == 3 ? 0 : 1;
}
