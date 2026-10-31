#include "SDL_joystick.h"
/* T34 (#681) stage C: what TextEditComponent.cpp uses (:102, :122, :143 on): the
   keyboard state, text input, and the nine key constants, with SDL2's values. */
const Uint8* SDL_GetKeyboardState(int* numkeys);
void SDL_StartTextInput(void);
void SDL_StopTextInput(void);
enum { SDLK_RETURN = '\r', SDLK_ESCAPE = 27, SDLK_DELETE = 127, SDLK_RIGHT = 0x4000004F, SDLK_LEFT = 0x40000050, SDLK_DOWN = 0x40000051, SDLK_UP = 0x40000052, SDLK_HOME = 0x4000004A, SDLK_END = 0x4000004D };
/* T34 (#681) stage E S2: what es-core/src/Window.cpp also reads, for the
   stand-in over the Window patch's scratch copy (SDL2's values). */
enum { SDLK_g = 'g', SDLK_i = 'i', SDLK_m = 'm', SDLK_t = 't' };
enum { KMOD_LCTRL = 0x0040 };
int SDL_GetModState(void);
int SDL_ShowCursor(int toggle);
