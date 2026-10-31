/* T21 (#668) stage E: a stand-in for SDL's headers, declarations only, so
 * g++ -fsyntax-only can read ApiSystem.cpp on a host without SDL. It links
 * nothing and proves nothing about SDL. */
#ifndef T21_FAKE_SDL_JOYSTICK_H
#define T21_FAKE_SDL_JOYSTICK_H
#include <stdint.h>
typedef uint8_t Uint8; typedef uint16_t Uint16; typedef uint32_t Uint32; typedef int32_t Sint32; typedef int16_t Sint16; typedef uint64_t Uint64;
typedef int32_t SDL_JoystickID;
typedef int32_t SDL_Keycode;
typedef struct _SDL_Joystick SDL_Joystick;
typedef struct _SDL_GameController SDL_GameController;
typedef struct { uint8_t data[16]; } SDL_JoystickGUID;
typedef struct { uint32_t type; uint32_t timestamp; SDL_JoystickID which; uint8_t button; uint8_t state; } SDL_JoyButtonEvent;
typedef struct { uint32_t type; uint32_t timestamp; uint32_t windowID; uint8_t event; int32_t data1; int32_t data2; } SDL_WindowEvent;
#include "t35-sdl-more.h" /* T35 (#682): the events, keys and macros the slice reads */
typedef union SDL_Event { uint32_t type; SDL_JoyButtonEvent jbutton; SDL_WindowEvent window; SDL_KeyboardEvent key; SDL_JoyAxisEvent jaxis; SDL_JoyHatEvent jhat; SDL_JoyDeviceEvent jdevice; SDL_MouseMotionEvent motion; SDL_MouseButtonEvent button; SDL_MouseWheelEvent wheel; SDL_TextInputEvent text; SDL_UserEvent user; uint8_t padding[56]; } SDL_Event;
enum { SDL_QUIT = 0x100, SDL_WINDOWEVENT = 0x200, SDL_JOYBUTTONDOWN = 0x603, SDL_JOYBUTTONUP = 0x604 };
enum { SDL_WINDOWEVENT_RESIZED = 5 };
#define SDL_PRESSED 1
enum { SDLK_F3 = 0x4000003c, SDLK_F5 = 0x4000003e };
#define SDL_RELEASED 0
typedef enum { SDL_FALSE = 0, SDL_TRUE = 1 } SDL_bool;
#define SDL_HAT_CENTERED 0x00
#define SDL_HAT_UP 0x01
#define SDL_HAT_RIGHT 0x02
#define SDL_HAT_DOWN 0x04
#define SDL_HAT_LEFT 0x08
typedef struct SDL_mutex SDL_mutex;
typedef struct _Mix_Music Mix_Music;
typedef struct Mix_Chunk Mix_Chunk;
typedef struct _snd_mixer snd_mixer_t;
typedef struct _snd_mixer_elem snd_mixer_elem_t;
typedef struct _snd_mixer_selem_id snd_mixer_selem_id_t;
#ifdef __cplusplus
extern "C" {
#endif
const char* SDL_GetKeyName(SDL_Keycode);
Uint32 SDL_GetTicks(void);
void SDL_Delay(Uint32);
int SDL_PollEvent(SDL_Event*);
int SDL_WaitEvent(SDL_Event*);
int SDL_WaitEventTimeout(SDL_Event*, int);
void SDL_StopTextInput(void);
/* T35 (#682) stage C: the calls the slice's InputManager, PowerSaver, AudioManager, Sound and Splash make. */
int SDL_InitSubSystem(Uint32); void SDL_QuitSubSystem(Uint32); const char* SDL_GetError(void); void SDL_free(void*);
int SDL_PushEvent(SDL_Event*); Uint32 SDL_RegisterEvents(int); SDL_bool SDL_SetHint(const char*, const char*); SDL_bool SDL_IsTextInputActive(void);
int SDL_GL_SetSwapInterval(int);
int SDL_NumJoysticks(void); SDL_Joystick* SDL_JoystickOpen(int); void SDL_JoystickClose(SDL_Joystick*); int SDL_JoystickEventState(int);
SDL_JoystickID SDL_JoystickInstanceID(SDL_Joystick*); SDL_JoystickID SDL_JoystickGetDeviceInstanceID(int); SDL_JoystickGUID SDL_JoystickGetGUID(SDL_Joystick*);
SDL_JoystickGUID SDL_JoystickGetDeviceGUID(int); void SDL_JoystickGetGUIDString(SDL_JoystickGUID, char*, int);
const char* SDL_JoystickName(SDL_Joystick*); const char* SDL_JoystickNameForIndex(int); int SDL_JoystickNumAxes(SDL_Joystick*); int SDL_JoystickNumButtons(SDL_Joystick*); int SDL_JoystickNumHats(SDL_Joystick*);
const char* SDL_JoystickPathForIndex(int); SDL_bool SDL_JoystickGetAxisInitialState(SDL_Joystick*, int, Sint16*);
SDL_bool SDL_IsGameController(int); char* SDL_GameControllerMappingForDeviceIndex(int); int SDL_GameControllerAddMapping(const char*);
#ifdef __cplusplus
}
#endif
#endif
