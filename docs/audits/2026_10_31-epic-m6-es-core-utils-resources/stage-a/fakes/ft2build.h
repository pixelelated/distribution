/* T36 (#683) S0: a stand-in for FreeType, declarations and the record types Font.cpp reads
   (the opaque FT_FaceRec_/FT_GlyphSlotRec_ the real header hides). Syntax only; nothing runs. */
#ifndef T36_FAKE_FT2BUILD_H
#define T36_FAKE_FT2BUILD_H
#define FT_FREETYPE_H "ft2build.h"
typedef unsigned int FT_UInt;
typedef int FT_Int;
typedef long FT_Long;
typedef unsigned long FT_ULong;
typedef int FT_Error;
typedef signed long FT_Pos;
typedef struct { unsigned int width, rows; unsigned char* buffer; int pitch; } FT_Bitmap;
typedef struct { FT_Pos horiAdvance, vertAdvance, horiBearingX, horiBearingY, width, height; } FT_Glyph_Metrics;
typedef struct { FT_Pos x, y; } FT_Vector;
typedef struct FT_GlyphSlotRec_ { FT_Bitmap bitmap; FT_Glyph_Metrics metrics; FT_Vector advance; int bitmap_left, bitmap_top; } FT_GlyphSlotRec;
typedef FT_GlyphSlotRec* FT_GlyphSlot;
typedef struct FT_FaceRec_ { FT_GlyphSlot glyph; FT_Long num_glyphs; FT_UInt units_per_EM; } FT_FaceRec;
typedef FT_FaceRec* FT_Face;
typedef struct FT_LibraryRec_* FT_Library;
#define FT_LOAD_RENDER 0x4
FT_Error FT_Init_FreeType(FT_Library*);
FT_Error FT_New_Memory_Face(FT_Library, const unsigned char*, FT_Long, FT_Long, FT_Face*);
FT_Error FT_Set_Pixel_Sizes(FT_Face, FT_UInt, FT_UInt);
FT_UInt  FT_Get_Char_Index(FT_Face, FT_ULong);
FT_Error FT_Load_Char(FT_Face, FT_ULong, FT_Int);
FT_Error FT_Done_Face(FT_Face);
#endif
