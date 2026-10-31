/* T21 (#668) stage E: stand-in; see SDL_joystick.h. */
#include "SDL_joystick.h"
/* T35 (#682) stage C: what VolumeControl.cpp reads of ALSA's mixer (alsa-lib's names). */
#include <alloca.h>
typedef enum { SND_MIXER_SCHN_UNKNOWN = -1, SND_MIXER_SCHN_FRONT_LEFT = 0, SND_MIXER_SCHN_FRONT_RIGHT, SND_MIXER_SCHN_MONO = 0 } snd_mixer_selem_channel_id_t;
#ifdef __cplusplus
extern "C" {
#endif
size_t snd_mixer_selem_id_sizeof(void);
#define snd_mixer_selem_id_alloca(ptr) do { *(ptr) = (snd_mixer_selem_id_t*)alloca(snd_mixer_selem_id_sizeof()); } while (0)
int snd_mixer_open(snd_mixer_t**, int); int snd_mixer_close(snd_mixer_t*); int snd_mixer_attach(snd_mixer_t*, const char*); int snd_mixer_detach(snd_mixer_t*, const char*);
int snd_mixer_selem_register(snd_mixer_t*, void*, void*); int snd_mixer_load(snd_mixer_t*); void snd_mixer_free(snd_mixer_t*); int snd_mixer_handle_events(snd_mixer_t*);
snd_mixer_elem_t* snd_mixer_first_elem(snd_mixer_t*); snd_mixer_elem_t* snd_mixer_elem_next(snd_mixer_elem_t*); snd_mixer_elem_t* snd_mixer_find_selem(snd_mixer_t*, const snd_mixer_selem_id_t*);
void snd_mixer_selem_id_set_index(snd_mixer_selem_id_t*, unsigned int); void snd_mixer_selem_id_set_name(snd_mixer_selem_id_t*, const char*); const char* snd_mixer_selem_id_get_name(const snd_mixer_selem_id_t*);
void snd_mixer_selem_get_id(snd_mixer_elem_t*, snd_mixer_selem_id_t*); int snd_mixer_selem_is_active(snd_mixer_elem_t*); int snd_mixer_selem_has_playback_volume(snd_mixer_elem_t*);
int snd_mixer_selem_get_playback_volume_range(snd_mixer_elem_t*, long*, long*); int snd_mixer_selem_get_playback_volume(snd_mixer_elem_t*, snd_mixer_selem_channel_id_t, long*);
int snd_mixer_selem_set_playback_volume(snd_mixer_elem_t*, snd_mixer_selem_channel_id_t, long); int snd_mixer_selem_set_playback_volume_all(snd_mixer_elem_t*, long);
#ifdef __cplusplus
}
#endif
