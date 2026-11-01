/* T36 (#683) S0: SDL video/GL names the renderers use, beyond T35's SDL.h fake. Syntax only. */
#ifndef T36_FAKE_SDL_GL_H
#define T36_FAKE_SDL_GL_H
typedef void* SDL_GLContext;
typedef enum { SDL_GL_RED_SIZE, SDL_GL_GREEN_SIZE, SDL_GL_BLUE_SIZE, SDL_GL_DEPTH_SIZE,
  SDL_GL_DOUBLEBUFFER, SDL_GL_MULTISAMPLEBUFFERS, SDL_GL_MULTISAMPLESAMPLES,
  SDL_GL_ACCELERATED_VISUAL, SDL_GL_CONTEXT_MAJOR_VERSION, SDL_GL_CONTEXT_MINOR_VERSION,
  SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_RED, SDL_GL_GREEN, SDL_GL_BLUE, SDL_GL_DEPTH, SDL_GL_ACCELERATED,
  SDL_GL_STENCIL_SIZE, SDL_GL_CONTEXT_FLAGS, SDL_GL_SHARE_WITH_CURRENT_CONTEXT } SDL_GLattr;
typedef enum { SDL_GL_CONTEXT_PROFILE_CORE=1, SDL_GL_CONTEXT_PROFILE_ES=4, SDL_GL_CONTEXT_PROFILE_COMPATIBILITY=2 } SDL_GLprofile;
int SDL_GL_SetAttribute(SDL_GLattr, int);
int SDL_GL_GetAttribute(SDL_GLattr, int*);
SDL_GLContext SDL_GL_CreateContext(void*);
void SDL_GL_DeleteContext(SDL_GLContext);
int SDL_GL_MakeCurrent(void*, SDL_GLContext);
void* SDL_GL_GetProcAddress(const char*);
int SDL_GL_ExtensionSupported(const char*);
int SDL_GL_SetSwapInterval(int);
void SDL_GL_SwapWindow(void*);
#ifndef SDL_WINDOW_OPENGL
#define SDL_WINDOW_OPENGL 0x2
#define SDL_WINDOW_FULLSCREEN 0x1
#define SDL_WINDOWPOS_UNDEFINED 0x1FFF0000
#endif
#ifndef T36_FAKE_SDL_SURFACE
#define T36_FAKE_SDL_SURFACE
typedef struct SDL_Surface { int w, h; void* pixels; } SDL_Surface;
#endif
SDL_Surface* SDL_CreateRGBSurfaceFrom(void*, int, int, int, int, unsigned int, unsigned int, unsigned int, unsigned int);
void SDL_SetWindowIcon(void*, SDL_Surface*);
void SDL_FreeSurface(SDL_Surface*);
#endif
/* SDL window / display / surface API (Renderer.cpp) -- T35's SDL.h lacks it. */
#ifndef T36_FAKE_SDL_WINDOW
#define T36_FAKE_SDL_WINDOW
typedef struct SDL_Window SDL_Window;
typedef struct { int x, y, w, h; } SDL_Rect;
typedef struct { unsigned int format; int w, h, refresh_rate; void* driverdata; } SDL_DisplayMode;
typedef struct { unsigned int flags; int version; void* info; } SDL_SysWMinfo;
#define SDL_INIT_VIDEO 0x20u
#define SDL_WINDOW_FULLSCREEN 0x1u
#define SDL_WINDOW_OPENGL 0x2u
#define SDL_WINDOW_BORDERLESS 0x10u
#define SDL_WINDOW_RESIZABLE 0x20u
#define SDL_WINDOW_MINIMIZED 0x40u
#define SDL_WINDOW_MAXIMIZED 0x80u
#define SDL_WINDOW_ALLOW_HIGHDPI 0x2000u
#define SDL_WINDOW_ALWAYS_ON_TOP 0x8000u
int SDL_Init(unsigned int);
void SDL_Quit(void);
SDL_Window* SDL_CreateWindow(const char*, int, int, int, int, unsigned int);
void SDL_DestroyWindow(SDL_Window*);
unsigned int SDL_GetWindowFlags(SDL_Window*);
void SDL_GetWindowPosition(SDL_Window*, int*, int*);
void SDL_GetWindowSize(SDL_Window*, int*, int*);
void SDL_SetWindowPosition(SDL_Window*, int, int);
void SDL_SetWindowBordered(SDL_Window*, int);
void SDL_SetWindowResizable(SDL_Window*, int);
void SDL_SetWindowMinimumSize(SDL_Window*, int, int);
void SDL_SetWindowInputFocus(SDL_Window*);
void SDL_RaiseWindow(SDL_Window*);
void SDL_RestoreWindow(SDL_Window*);
int SDL_GetDesktopDisplayMode(int, SDL_DisplayMode*);
int SDL_GetCurrentDisplayMode(int, SDL_DisplayMode*);
int SDL_GetDisplayBounds(int, SDL_Rect*);
int SDL_GetNumVideoDisplays(void);
int SDL_GetWindowWMInfo(SDL_Window*, SDL_SysWMinfo*);
int SDL_ShowCursor(int);
#endif
