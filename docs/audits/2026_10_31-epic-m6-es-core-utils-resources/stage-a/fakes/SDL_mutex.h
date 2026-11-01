/* T21 (#668) stage E: stand-in; see SDL_joystick.h. */
#include "SDL_joystick.h"
/* T34 (#681) stage C: the four calls BusyComponent.cpp makes (:31, :62, :67, and the unlock). */
SDL_mutex* SDL_CreateMutex(void);
void SDL_DestroyMutex(SDL_mutex* mutex);
int SDL_LockMutex(SDL_mutex* mutex);
int SDL_UnlockMutex(SDL_mutex* mutex);
