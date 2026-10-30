/* T34 (#681) stage C: the tenth stand-in, for BatteryIndicatorComponent.cpp:7,
   which includes <SDL_power.h> and uses none of its symbols; the two SDL
   declarations are here so a later use fails at link, not at parse. */
#include "SDL_joystick.h"
typedef enum { SDL_POWERSTATE_UNKNOWN, SDL_POWERSTATE_ON_BATTERY, SDL_POWERSTATE_NO_BATTERY, SDL_POWERSTATE_CHARGING, SDL_POWERSTATE_CHARGED } SDL_PowerState;
SDL_PowerState SDL_GetPowerInfo(int* seconds, int* percent);
