// T36 #683 S10 G-20: an oversized SVG whose width*height*4 exceeds the allocator. Reuses S9's
// TextureData.cpp whole (the SUT) over doubles for everything its dependency surface needs --
// Renderer, ImageIO, ResourceManager, the vlc snapshot path, Paths/Settings/Log -- and a
// PdfHandler double that drops one small image file in a scratch directory. ImageIO's decode is
// doubled to succeed, so initImageFromMemory returns true; at the pin loadFromPdf still returns
// false (the result was discarded), at the tip it returns true. The control: a PdfHandler that
// extracts nothing -> false before and after.
#include "resources/TextureData.h"
#include "resources/ResourceManager.h"
#include "ImageIO.h"
#include "renderers/Renderer.h"
#include "Paths.h"
#include "Settings.h"
#include "Log.h"
#include "utils/TimeUtil.h"
#include <vlc/vlc.h>
#include <cstdio>
#include <cstring>
#include <memory>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>

// --- Paths / Settings / Log / DateTime doubles (FileSystemUtil.cpp is linked whole) ---
Paths* Paths::_instance = nullptr; Paths::Paths() {}
std::string& Paths::getHomePath() { static std::string h = "/tmp"; return h; }
void Paths::setHomePath(const std::string&) {} std::string& Paths::getExePath() { static std::string e = "/tmp"; return e; } void Paths::setExePath(const std::string&) {}
bool Settings::_UseFileCache = false;
Settings* Settings::getInstance() { static char buf[sizeof(Settings)] = {0}; return reinterpret_cast<Settings*>(buf); }   // non-null; getBool/getInt ignore this
bool Settings::getBool(const std::string&) { return false; }
Utils::Time::DateTime::DateTime() {} Utils::Time::DateTime::DateTime(const time_t&) {} Utils::Time::DateTime::~DateTime() {}
Utils::Time::DateTime Utils::Time::DateTime::now() { return Utils::Time::DateTime(); }
double Utils::Time::DateTime::elapsedSecondsSince(const Utils::Time::DateTime&) { return 0; }
const MaxSizeInfo MaxSizeInfo::Empty;
LogLevel Log::mReportingLevel = LogError; bool Log::mEnabled = false;
Log::Log(LogLevel level) : mLevel(level) {} Log::~Log() {}
std::ostringstream& Log::stream() { static std::ostringstream s; return s; }

// --- ResourceManager double: getInstance + getFileData return a tiny buffer ---
std::shared_ptr<ResourceManager> ResourceManager::sInstance = nullptr;
ResourceManager::ResourceManager() {}
std::shared_ptr<ResourceManager>& ResourceManager::getInstance()
{
	if (!sInstance) sInstance = std::shared_ptr<ResourceManager>(new ResourceManager());
	return sInstance;
}
const ResourceData ResourceManager::getFileData(const std::string&) const
{
	return ResourceData{ std::shared_ptr<unsigned char>(new unsigned char[4]()), 4 };
}

// --- ImageIO doubles: the decode succeeds with a 1x1 image ---
unsigned char* ImageIO::loadFromMemoryRGBA32(const unsigned char*, const size_t, size_t& width, size_t& height, MaxSizeInfo*, Vector2i* baseSize, Vector2i* packedSize, int)
{
	width = 1; height = 1;
	if (baseSize) *baseSize = Vector2i(1, 1);
	if (packedSize) *packedSize = Vector2i(1, 1);
	return new unsigned char[4]();
}
void ImageIO::flipPixelsVert(unsigned char*, const size_t&, const size_t&) {}
Vector2i ImageIO::adjustPictureSize(Vector2i imageSize, Vector2i, bool) { return imageSize; }
Vector2f ImageIO::adjustPictureSizeF(float cxDIB, float cyDIB, float, float, bool) { return Vector2f(cxDIB, cyDIB); }
Vector2f ImageIO::adjustPictureSizeF(Vector2f imageSize, Vector2f, bool) { return imageSize; }

// --- Renderer doubles (free functions in namespace Renderer) ---
namespace Renderer
{
	int getScreenWidth() { return 640; }
	int getScreenHeight() { return 480; }
	unsigned int createTexture(const Texture::Type, const bool, const bool, const unsigned int, const unsigned int, void*) { return 1; }
	unsigned int createMipmappedTexture(const Texture::Type, const bool, const bool, const unsigned int, const unsigned int, void*) { return 1; }
	void destroyTexture(const unsigned int) {}
	void updateTexture(const unsigned int, const Texture::Type, const unsigned int, const unsigned, const unsigned int, const unsigned int, void*) {}
	void bindTexture(const unsigned int) {}
}

// --- vlc stubs (TextureData's snapshot path; never exercised here) ---
libvlc_instance_t* libvlc_new(int, const char* const*) { return nullptr; }
void libvlc_release(libvlc_instance_t*) {}
libvlc_media_t* libvlc_media_new_path(libvlc_instance_t*, const char*) { return nullptr; }
void libvlc_media_add_option(libvlc_media_t*, const char*) {}
void libvlc_media_release(libvlc_media_t*) {}
libvlc_media_player_t* libvlc_media_player_new_from_media(libvlc_media_t*) { return nullptr; }
void libvlc_media_player_play(libvlc_media_player_t*) {}
void libvlc_media_player_stop(libvlc_media_player_t*) {}
void libvlc_media_player_release(libvlc_media_player_t*) {}
void libvlc_media_player_set_rate(libvlc_media_player_t*, float) {}
void libvlc_media_player_set_time(libvlc_media_player_t*, libvlc_time_t) {}
libvlc_time_t libvlc_media_player_get_time(libvlc_media_player_t*) { return 0; }
int libvlc_video_take_snapshot(libvlc_media_player_t*, unsigned int, const char*, unsigned int, unsigned int) { return 0; }
void libvlc_audio_set_mute(libvlc_media_player_t*, int) {}

// --- the PdfHandler double ---
class FakePdf : public IPdfHandler
{
public:
	explicit FakePdf(bool extract) : mExtract(extract) {}
	std::vector<std::string> extractPdfImages(const std::string&, int, int, int) override
	{
		if (!mExtract) return {};
		std::string path = std::string(mScratch) + "/page.img";
		std::ofstream(path, std::ios::binary) << "img";   // the bytes are immaterial; the decode is doubled
		return { path };
	}
	int getPdfPageCount(const std::string&) override { return mExtract ? 1 : 0; }
	const char* mScratch = "/workspace/tmp/m6-t36/s9/scratch";
private:
	bool mExtract;
};

int main()
{
	// width beyond INT_MAX, so the pin's `new[width*height*4]` asks the allocator for ~12 GB and
	// the int cast handed to the rasteriser overflows; the fix refuses the dimensions first.
	const char* svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"3000000000\" height=\"1\"></svg>";
	TextureData td(false, false);
	bool r = td.initSVGFromMemory((const unsigned char*)svg, strlen(svg));
	printf("S10 G-20: initSVGFromMemory=%d (want 0: oversized refused)\n", r);
	if (r) { printf("S10 G-20: FAIL (oversized SVG accepted)\n"); return 1; }
	printf("S10 G-20: PASS\n");
	return 0;
}
