/* T36 (#683) S0: a stand-in for <vlc/vlc.h> (TextureData.cpp's snapshot path). Syntax only. */
#ifndef T36_FAKE_VLC_H
#define T36_FAKE_VLC_H
#include <cstdint>
typedef struct libvlc_instance_t libvlc_instance_t;
typedef struct libvlc_media_t libvlc_media_t;
typedef struct libvlc_media_player_t libvlc_media_player_t;
typedef int64_t libvlc_time_t;
libvlc_instance_t* libvlc_new(int, const char* const*);
void libvlc_release(libvlc_instance_t*);
libvlc_media_t* libvlc_media_new_path(libvlc_instance_t*, const char*);
void libvlc_media_add_option(libvlc_media_t*, const char*);
void libvlc_media_release(libvlc_media_t*);
libvlc_media_player_t* libvlc_media_player_new_from_media(libvlc_media_t*);
void libvlc_media_player_play(libvlc_media_player_t*);
void libvlc_media_player_stop(libvlc_media_player_t*);
void libvlc_media_player_release(libvlc_media_player_t*);
void libvlc_media_player_set_rate(libvlc_media_player_t*, float);
void libvlc_media_player_set_time(libvlc_media_player_t*, libvlc_time_t);
libvlc_time_t libvlc_media_player_get_time(libvlc_media_player_t*);
int libvlc_video_take_snapshot(libvlc_media_player_t*, unsigned int, const char*, unsigned int, unsigned int);
void libvlc_audio_set_mute(libvlc_media_player_t*, int);
#endif
