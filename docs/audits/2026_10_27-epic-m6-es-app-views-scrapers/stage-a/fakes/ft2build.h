/* T21 (#668) stage E: a stand-in for FreeType; declarations only. */
#ifndef T21_FAKE_FT2BUILD_H
#define T21_FAKE_FT2BUILD_H
#define FT_FREETYPE_H "ft2build.h"
typedef struct FT_LibraryRec_* FT_Library;
typedef struct FT_FaceRec_* FT_Face;
typedef unsigned int FT_UInt;
typedef long FT_Long;
typedef int FT_Error;
#endif
