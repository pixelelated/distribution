// T36 #683 S1 (PL-06/#1359, G-1): the font atlas's dangling pointer. getTextureForNewGlyph is
// lifted verbatim from Font.cpp (T36_INC) and run with minimal doubles. A glyph too big for a
// fresh atlas makes findEmpty fail; at the pin the atlas is pushed to mTextures and then
// deleted, so the "destroy" loop double-frees it (ASan). The fixed order pushes only on success.
#include <vector>
#include <string>
#include <cstdio>
namespace Math { template<class T> T min(T a, T b){return a<b?a:b;} template<class T> T max(T a,T b){return a>b?a:b;} }
struct Vector2i { int mx, my; Vector2i(){mx=my=0;} Vector2i(int a,int b):mx(a),my(b){} int x() const {return mx;} int y() const {return my;} };
struct LogDummy { template<class T> LogDummy& operator<<(const T&){return *this;} };
enum { LogDebug, LogError };
static LogDummy LOG(int){ return LogDummy(); }
namespace Utils { namespace FileSystem { inline std::string getFileName(const std::string& p){return p;} } }
struct FontTexture {
	Vector2i textureSize;
	bool initCalled = false;
	void initTexture(){ initCalled = true; }
	// a fresh atlas: a glyph fits only if it is no larger than the texture.
	bool findEmpty(const Vector2i& g, Vector2i& cursor){ cursor = Vector2i(0,0); return g.x() <= textureSize.x() && g.y() <= textureSize.y(); }
};
struct Font {
	std::vector<FontTexture*> mTextures;
	std::string mPath = "f.ttf";
	int mSize = 16;
	void getTextureForNewGlyph(const Vector2i& glyphSize, FontTexture*& tex_out, Vector2i& cursor_out);
	~Font(){ for (auto t : mTextures) delete t; }   // ES's Font frees its atlases
};
#include T36_INC   // the verbatim getTextureForNewGlyph body
int main(){
	Font f;
	FontTexture* tex = nullptr; Vector2i cursor;
	// a glyph far larger than any atlas (>2048): a fresh atlas cannot hold it, findEmpty fails.
	f.getTextureForNewGlyph(Vector2i(99999, 99999), tex, cursor);
	// tex_out is NULL on failure; the real bug is what mTextures now holds.
	// Font's destructor runs here: at the pin it deletes the dangling pointer again.
	return 0;
}
