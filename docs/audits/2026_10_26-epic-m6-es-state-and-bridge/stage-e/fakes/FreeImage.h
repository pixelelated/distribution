/* T21 (#668) stage E: a stand-in for FreeImage, declarations only, so
 * g++ -fsyntax-only can read the scraper's sources. It links nothing. */
#ifndef T21_FAKE_FREEIMAGE_H
#define T21_FAKE_FREEIMAGE_H
#include <stddef.h>
#include <wchar.h>
typedef struct FIBITMAP FIBITMAP;
typedef enum { FIF_UNKNOWN = -1, FIF_BMP = 0, FIF_JPEG = 2, FIF_PNG = 13 } FREE_IMAGE_FORMAT;
typedef enum { FILTER_BOX = 0, FILTER_BICUBIC = 1, FILTER_BILINEAR = 2, FILTER_BSPLINE = 3, FILTER_CATMULLROM = 4, FILTER_LANCZOS3 = 5 } FREE_IMAGE_FILTER;
#ifdef __cplusplus
extern "C" {
#endif
FREE_IMAGE_FORMAT FreeImage_GetFileType(const char*, int);
FREE_IMAGE_FORMAT FreeImage_GetFileTypeU(const wchar_t*, int);
FREE_IMAGE_FORMAT FreeImage_GetFIFFromFilename(const char*);
FREE_IMAGE_FORMAT FreeImage_GetFIFFromFilenameU(const wchar_t*);
int FreeImage_FIFSupportsReading(FREE_IMAGE_FORMAT);
FIBITMAP* FreeImage_Load(FREE_IMAGE_FORMAT, const char*, int flags = 0);
FIBITMAP* FreeImage_LoadU(FREE_IMAGE_FORMAT, const wchar_t*, int flags = 0);
int FreeImage_Save(FREE_IMAGE_FORMAT, FIBITMAP*, const char*, int flags = 0);
int FreeImage_SaveU(FREE_IMAGE_FORMAT, FIBITMAP*, const wchar_t*, int flags = 0);
unsigned FreeImage_GetWidth(FIBITMAP*);
unsigned FreeImage_GetHeight(FIBITMAP*);
FIBITMAP* FreeImage_Rescale(FIBITMAP*, int, int, FREE_IMAGE_FILTER filter = FILTER_CATMULLROM);
void FreeImage_Unload(FIBITMAP*);
#ifdef __cplusplus
}
#endif
#endif
