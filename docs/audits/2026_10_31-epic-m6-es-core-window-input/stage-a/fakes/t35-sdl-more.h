/* T35 (#682) stage C: what the slice's InputManager.cpp, PowerSaver.cpp,
 * AudioManager.cpp, Sound.cpp and Splash.cpp also read (declarations only,
 * SDL2's names and values; it links nothing and proves nothing about SDL).
 * Included from SDL_joystick.h's T35 line. */
#ifndef T35_FAKE_SDL_MORE_H
#define T35_FAKE_SDL_MORE_H
#define SDL_VERSION_ATLEAST(X, Y, Z) 1
#define SDL_DISABLE 0
#define SDL_ENABLE 1
#define SDL_INIT_AUDIO 0x00000010u
#define SDL_INIT_JOYSTICK 0x00000200u
#define SDL_TOUCH_MOUSEID ((Uint32)-1)
#define SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS "SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"
enum { SDL_KEYDOWN = 0x300, SDL_KEYUP, SDL_TEXTEDITING, SDL_TEXTINPUT, SDL_MOUSEMOTION = 0x400, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDL_MOUSEWHEEL,
       SDL_JOYAXISMOTION = 0x600, SDL_JOYBALLMOTION, SDL_JOYHATMOTION, SDL_JOYDEVICEADDED = 0x605, SDL_JOYDEVICEREMOVED, SDL_USEREVENT = 0x8000 };
enum { SDLK_BACKSPACE = 8, SDLK_LEFTBRACKET = '[', SDLK_RIGHTBRACKET = ']', SDLK_F1 = 0x4000003a, SDLK_F2 = 0x4000003b, SDLK_F4 = 0x4000003d };
typedef struct { int scancode; SDL_Keycode sym; Uint16 mod; Uint32 unused; } SDL_Keysym;
typedef struct { Uint32 type; Uint32 timestamp; Uint32 windowID; Uint8 state; Uint8 repeat; SDL_Keysym keysym; } SDL_KeyboardEvent;
typedef struct { Uint32 type; Uint32 timestamp; SDL_JoystickID which; Uint8 axis; Sint16 value; } SDL_JoyAxisEvent;
typedef struct { Uint32 type; Uint32 timestamp; SDL_JoystickID which; Uint8 hat; Uint8 value; } SDL_JoyHatEvent;
typedef struct { Uint32 type; Uint32 timestamp; Sint32 which; } SDL_JoyDeviceEvent;
typedef struct { Uint32 type; Uint32 timestamp; Uint32 windowID; Uint32 which; Uint32 state; Sint32 x, y, xrel, yrel; } SDL_MouseMotionEvent;
typedef struct { Uint32 type; Uint32 timestamp; Uint32 windowID; Uint32 which; Uint8 button, state, clicks; Sint32 x, y; } SDL_MouseButtonEvent;
typedef struct { Uint32 type; Uint32 timestamp; Uint32 windowID; Uint32 which; Sint32 x, y; Uint32 direction; } SDL_MouseWheelEvent;
typedef struct { Uint32 type; Uint32 timestamp; Uint32 windowID; char text[32]; } SDL_TextInputEvent;
typedef struct { Uint32 type; Uint32 timestamp; Uint32 windowID; Sint32 code; void* data1; void* data2; } SDL_UserEvent;
#endif
