#pragma once
/* T21 (#668) stage E: stand-in; see SDL_joystick.h. */
#include "SDL_joystick.h"
/* T35 (#682) stage C: what AudioManager.cpp and Sound.cpp read (SDL_mixer 2's names and values). */
#define MIX_MAX_VOLUME 128
#define MIX_DEFAULT_FORMAT 0x8010
struct Mix_Chunk { int allocated; Uint8* abuf; Uint32 alen; Uint8 volume; };
#ifdef __cplusplus
extern "C" {
#endif
int Mix_OpenAudio(int, Uint16, int, int); void Mix_CloseAudio(void); const char* Mix_GetError(void);
Mix_Music* Mix_LoadMUS(const char*); void Mix_FreeMusic(Mix_Music*); int Mix_FadeInMusic(Mix_Music*, int, int); int Mix_FadeOutMusic(int);
int Mix_HaltMusic(void); void Mix_HookMusicFinished(void (*)(void)); int Mix_PlayingMusic(void); int Mix_VolumeMusic(int);
Mix_Chunk* Mix_LoadWAV(const char*); void Mix_FreeChunk(Mix_Chunk*); int Mix_PlayChannel(int, Mix_Chunk*, int);
#ifdef __cplusplus
}
#endif
