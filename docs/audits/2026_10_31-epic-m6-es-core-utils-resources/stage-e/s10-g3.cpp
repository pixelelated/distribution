// T36 #683 S10 G-3: Font::rebuildTextures lifted (Font.cpp links heavily). A cached glyph whose
// getFaceForChar returns null: the pin does `face->glyph` and dereferences null (ASan SEGV);
// the fix skips a glyph whose face is missing or whose FT_Load_Char failed.
#include <map>
#include <vector>
#include <cstdio>
struct FT_Bitmap_ { unsigned char* buffer; };
struct FT_GlyphSlotRec_ { FT_Bitmap_ bitmap; };
typedef FT_GlyphSlotRec_* FT_GlyphSlot;
struct FT_FaceRec_ { FT_GlyphSlot glyph; };
typedef FT_FaceRec_* FT_Face;
#define FT_LOAD_RENDER 1
static int g_loadResult = 0;              // 0 = success
int FT_Load_Char(FT_Face, unsigned long, int) { return g_loadResult; }
struct Vector2i { int mx,my; Vector2i(){mx=my=0;} Vector2i(int a,int b):mx(a),my(b){} int x()const{return mx;} int y()const{return my;} };
namespace Renderer { struct Texture { enum Type { ALPHA }; };
	void updateTexture(unsigned, Texture::Type, unsigned, unsigned, unsigned, unsigned, void*) {} }
struct FontTexture { unsigned textureId = 1; void initTexture() {} };
struct Glyph { FontTexture* texture; Vector2i cursor; Vector2i glyphSize; };
struct Font {
	std::vector<FontTexture*> mTextures;
	std::map<unsigned int, Glyph*> mGlyphMap;
	FT_Face mFace = nullptr;
	FT_Face getFaceForChar(unsigned int) { return mFace; }   // G-3: the glyph's face is missing
	void rebuildTextures();
};
#include T36G3_INC   // void Font::rebuildTextures() { ... }
int main()
{
	Font f;
	FontTexture tx; f.mTextures.push_back(&tx);
	Glyph g; g.texture = &tx; g.cursor = Vector2i(0,0); g.glyphSize = Vector2i(4,4);
	f.mGlyphMap[65] = &g;
	f.mFace = nullptr;        // getFaceForChar returns null for the cached glyph
	f.rebuildTextures();      // pin: face->glyph derefs null; tip: skipped
	printf("S10 G-3: PASS (a glyph with a missing face is skipped)\n");
	return 0;
}
